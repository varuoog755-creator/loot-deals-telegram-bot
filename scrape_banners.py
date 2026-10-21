import json
import asyncio
import websockets

WS_URL = 'ws://127.0.0.1:9100/devtools/page/3FE1A88FEA67C60FC142F6C8D7313899'

JS_BANNERS = """(() => {
    const banners = [];
    // Homepage banner sliders - usually img inside <a>
    document.querySelectorAll('a').forEach(a => {
        const img = a.querySelector('img');
        if (!img) return;
        const src = img.currentSrc || img.src;
        if (!src || !/banner|slider|home|main|hero|web/i.test(src)) return;
        const w = img.naturalWidth || 0;
        if (w < 300) return; // banners are wide
        banners.push({href: a.href, image: src, w, h: img.naturalHeight});
    });
    // also any large images
    const large = [];
    document.querySelectorAll('img').forEach(img => {
        const src = img.currentSrc || img.src;
        const w = img.naturalWidth || 0;
        if (w >= 600 && !/logo|icon|store|category|svg/.test(src)) {
            large.push({src, w, h: img.naturalHeight, alt: img.alt || '', parentHref: (img.closest('a')||{}).href || ''});
        }
    });
    return JSON.stringify({url: location.href, banners, large: large.slice(0, 20)});
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
        r = await cdp(ws, "Runtime.evaluate", {"expression": JS_BANNERS, "returnByValue": True}, 2)
        val = r["result"]["result"].get("value")
        d = json.loads(val)
        print("URL:", d["url"])
        print("BANNERS:", len(d["banners"]))
        for b in d["banners"]:
            print(f"  {b['w']}x{b['h']} {b['image'][:120]} -> {b['href'][:80]}")
        print("LARGE:", len(d["large"]))
        for l in d["large"]:
            print(f"  {l['w']}x{l['h']} {l['src'][:120]} alt={l['alt'][:40]} href={l['parentHref'][:80]}")
        with open("earnkaro_banners.json", "w", encoding="utf-8") as f:
            json.dump(d, f, indent=2, ensure_ascii=False)

asyncio.run(main())
