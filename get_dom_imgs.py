import json
import asyncio
import websockets

async def get_raw_earnkaro_dom():
    ws_url = 'ws://127.0.0.1:9100/devtools/page/3FE1A88FEA67C60FC142F6C8D7313899'
    async with websockets.connect(ws_url, max_size=50_000_000) as ws:
        eval_script = """
        (() => {
            // Get all img elements on the page with their src, alt, and surrounding text
            const imgs = Array.from(document.querySelectorAll('img')).map(img => {
                let card = img.closest('.slick-slide') || img.closest('.store_card') || img.closest('section') || img.parentElement.parentElement;
                return {
                    src: img.src,
                    alt: img.alt || img.title || '',
                    cardText: card ? card.innerText.substring(0, 300) : '',
                    parentTag: img.parentElement ? img.parentElement.tagName : ''
                };
            }).filter(i => i.src && (i.src.includes('ckassets') || i.src.includes('media-amazon') || i.src.includes('tatacliq') || i.src.includes('myntassets')));
            
            return imgs;
        })()
        """
        req = {
            "id": 1,
            "method": "Runtime.evaluate",
            "params": {
                "expression": eval_script,
                "returnByValue": True
            }
        }
        await ws.send(json.dumps(req))
        res = await ws.recv()
        data = json.loads(res)
        imgs = data.get("result", {}).get("result", {}).get("value", [])
        print(f"Found {len(imgs)} product images with surrounding text!")
        with open("earnkaro_dom_images.json", "w", encoding="utf-8") as f:
            json.dump(imgs, f, indent=2)
        print(json.dumps(imgs[:6], indent=2))

asyncio.run(get_raw_earnkaro_dom())
