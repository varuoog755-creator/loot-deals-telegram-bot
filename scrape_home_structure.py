import json
import asyncio
import websockets

WS_URL = 'ws://127.0.0.1:9100/devtools/page/3FE1A88FEA67C60FC142F6C8D7313899'

# Scrape homepage structure: banner slider (with links), store tiles, category sections
JS_HOME = """(() => {
    // Banner slider: find swiper/slider containers with big images and their links
    const slider = [];
    document.querySelectorAll('img[src*="staticpage_images"]').forEach(img => {
        const a = img.closest('a');
        slider.push({image: img.currentSrc || img.src, href: a ? a.href : ''});
    });
    // store tiles
    const stores = [];
    document.querySelectorAll('a[href*="/stores/"]').forEach(a => {
        const img = a.querySelector('img');
        if (!img) return;
        const src = img.currentSrc || img.src;
        if (/no-image|icon|logo.png$/.test(src)) return;
        stores.push({href: a.href, image: src, text: (a.innerText||'').replace(/\\n+/g,' ').trim().substring(0,60)});
    });
    // top selling / trending tiles
    const tiles = [];
    document.querySelectorAll('a[href*="/top-selling-products/"], a[href*="/product/trending-offers/"]').forEach(a => {
        const img = a.querySelector('img');
        tiles.push({href: a.href, image: img ? (img.currentSrc||img.src) : '', text: (a.innerText||'').replace(/\\n+/g,' ').trim().substring(0,80)});
    });
    // category grid with icons
    const cats = [];
    document.querySelectorAll('a[href*="/product/"]').forEach(a => {
        const img = a.querySelector('img');
        const t = (a.innerText||'').replace(/\\n+/g,' ').trim();
        if (img && t && t.length > 2 && t.length < 60) {
            cats.push({href: a.href, image: img.currentSrc||img.src, text: t});
        }
    });
    return JSON.stringify({url: location.href, slider, stores, tiles, cats});
})()"""

async def cdp(ws, method, params=None, msg_id=1):
    await ws.send(json.dumps({"id": msg_id, "method": method, "params": params or {}}))
    while True:
        msg = json.loads(await ws.recv())
        if msg.get("id") == msg_id:
            return msg

async def main():
    async with websockets.connect(WS_URL, max_size=100*1024*1024) as ws:
        await cdp(ws, "Page.navigate", {"url": "https://earnkaro.com/"}, 1)
        await asyncio.sleep(6)
        r = await cdp(ws, "Runtime.evaluate", {"expression": JS_HOME, "returnByValue": True}, 2)
        val = r["result"]["result"].get("value")
        d = json.loads(val)
        print("URL:", d["url"])
        print("SLIDER:", len(d["slider"]))
        for s in d["slider"][:12]:
            print(f"  {s['image'][:110]} -> {s['href'][:90]}")
        print("STORES:", len(d["stores"]))
        for s in d["stores"][:15]:
            print(f"  {s['image'][:100]} | {s['text']} | {s['href'][:80]}")
        print("TILES:", len(d["tiles"]))
        for s in d["tiles"][:15]:
            print(f"  {s['image'][:100]} | {s['text']} | {s['href'][:80]}")
        print("CATS:", len(d["cats"]))
        for s in d["cats"][:20]:
            print(f"  {s['image'][:100]} | {s['text']} | {s['href'][:80]}")
        with open("earnkaro_home_structure.json", "w", encoding="utf-8") as f:
            json.dump(d, f, indent=2, ensure_ascii=False)

asyncio.run(main())
