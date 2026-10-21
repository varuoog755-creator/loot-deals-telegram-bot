import json
import asyncio
import websockets

WS_URL = 'ws://127.0.0.1:9100/devtools/page/3FE1A88FEA67C60FC142F6C8D7313899'

# Dump raw HTML around first COPY LINK occurrence
JS = """(() => {
    const html = document.documentElement.outerHTML;
    const idx = html.indexOf('COPY LINK');
    if (idx < 0) return JSON.stringify({found: false});
    // get surrounding 6000 chars
    return JSON.stringify({found: true, around: html.substring(Math.max(0, idx-3500), idx+1500)});
})()"""

async def cdp(ws, method, params=None, msg_id=1):
    await ws.send(json.dumps({"id": msg_id, "method": method, "params": params or {}}))
    while True:
        msg = json.loads(await ws.recv())
        if msg.get("id") == msg_id:
            return msg

async def main():
    async with websockets.connect(WS_URL, max_size=100*1024*1024) as ws:
        r = await cdp(ws, "Runtime.evaluate", {"expression": JS, "returnByValue": True}, 1)
        val = r["result"]["result"].get("value")
        d = json.loads(val)
        if d.get("found"):
            with open("card_html_sample.txt", "w", encoding="utf-8") as f:
                f.write(d["around"])
            print("Saved card_html_sample.txt, len:", len(d["around"]))
        else:
            print("COPY LINK not found in HTML")

asyncio.run(main())
