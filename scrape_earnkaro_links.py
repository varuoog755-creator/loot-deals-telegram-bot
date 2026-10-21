import json
import asyncio
import websockets

WS_URL = 'ws://127.0.0.1:9100/devtools/page/3FE1A88FEA67C60FC142F6C8D7313899'

async def main():
    async with websockets.connect(WS_URL, max_size=50*1024*1024) as ws:
        # Extract ALL product cards with links, images, prices
        js = """(() => {
            const results = [];
            // Get every anchor that links to a deal/product
            document.querySelectorAll('a').forEach(a => {
                const href = a.href || '';
                if (!href || href === '#') return;
                // Only product/deal/store links
                const isProduct = /earnkaro\\.com\\//.test(href) &&
                    !/\\/(deals|stores|make-links|home|privacy|terms|faq|about|contact|login|signup|how-it-works|blog)(\\/?$|\\?)/.test(href);
                if (!isProduct) return;
                const card = a.closest('div[class]');
                // find image inside this anchor
                let img = a.querySelector('img');
                if (!img && card) img = card.querySelector('img');
                const image = img ? (img.currentSrc || img.src) : null;
                // text content
                const text = (a.innerText || card.innerText || '').replace(/\\n+/g, ' | ').trim();
                results.push({href, image, text: text.substring(0, 400)});
            });
            // Also capture any card-like blocks with images + prices even without anchor
            const imgs = [];
            document.querySelectorAll('img').forEach(img => {
                const src = img.currentSrc || img.src;
                if (src && !/logo|icon|avatar|svg/.test(src)) {
                    imgs.push({src, alt: img.alt || ''});
                }
            });
            return JSON.stringify({anchors: results, images: imgs, url: location.href, title: document.title});
        })()"""
        await ws.send(json.dumps({"id": 1, "method": "Runtime.evaluate",
                                  "params": {"expression": js, "returnByValue": True}}))
        while True:
            msg = json.loads(await ws.recv())
            if msg.get("id") == 1:
                val = msg["result"]["result"].get("value")
                data = json.loads(val) if val else {}
                print("PAGE:", data.get("url"), "|", data.get("title"))
                print("ANCHORS:", len(data.get("anchors", [])))
                print("IMAGES:", len(data.get("images", [])))
                with open("earnkaro_scrape_anchors.json", "w", encoding="utf-8") as f:
                    json.dump(data, f, indent=2, ensure_ascii=False)
                print("Saved earnkaro_scrape_anchors.json")
                break

asyncio.run(main())
