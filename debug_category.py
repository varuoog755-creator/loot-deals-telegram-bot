import json
import asyncio
import websockets

WS_URL = 'ws://127.0.0.1:9100/devtools/page/3FE1A88FEA67C60FC142F6C8D7313899'

# Capture full outerHTML of one category page to understand product card structure
async def cdp(ws, method, params=None, msg_id=1):
    await ws.send(json.dumps({"id": msg_id, "method": method, "params": params or {}}))
    while True:
        msg = json.loads(await ws.recv())
        if msg.get("id") == msg_id:
            return msg

async def main():
    async with websockets.connect(WS_URL, max_size=100*1024*1024) as ws:
        await cdp(ws, "Page.navigate", {"url": "https://earnkaro.com/product/electronics/headphones-headsets"}, 1)
        await asyncio.sleep(6)
        r = await cdp(ws, "Runtime.evaluate", {
            "expression": "document.body.innerText.substring(0, 3000)",
            "returnByValue": True}, 2)
        print("INNER TEXT:")
        print(r["result"]["result"].get("value", "")[:3000])
        # count images on page
        r2 = await cdp(ws, "Runtime.evaluate", {
            "expression": """(() => {
                const imgs = [...document.querySelectorAll('img')];
                return JSON.stringify({
                    total: imgs.length,
                    srcs: imgs.slice(0, 30).map(i => ({s: (i.currentSrc||i.src).substring(0,130), w: i.width, h: i.height}))
                });
            })()""",
            "returnByValue": True}, 3)
        val = r2["result"]["result"].get("value")
        d = json.loads(val)
        print("TOTAL IMAGES:", d["total"])
        for x in d["srcs"]:
            print(f"  {x['w']}x{x['h']} {x['s']}")

asyncio.run(main())
