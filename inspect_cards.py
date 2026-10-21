import json
import asyncio
import websockets

WS_URL = 'ws://127.0.0.1:9100/devtools/page/3FE1A88FEA67C60FC142F6C8D7313899'

JS_CARDS = """(() => {
    // Find all product cards - look for elements containing COPY LINK text
    const cards = [];
    const allEls = [...document.querySelectorAll('div, article, section, li')];
    const cardEls = allEls.filter(el =>
        el.innerText && el.innerText.includes('COPY LINK') &&
        el.innerText.includes('₹') &&
        el.innerText.length < 600 &&
        ![...el.children].some(c => c.innerText && c.innerText.includes('COPY LINK'))
    );
    cardEls.forEach(card => {
        const img = card.querySelector('img');
        const image = img ? (img.currentSrc || img.src) : null;
        const link = card.querySelector('a');
        const href = link ? link.href : null;
        // copy button may carry data attributes with the earn link
        const btns = [...card.querySelectorAll('button, a, [data-link], [data-clipboard-text], [data-href]')];
        const btnData = btns.map(b => ({
            tag: b.tagName,
            text: (b.innerText||'').trim().substring(0,30),
            dataLink: b.getAttribute('data-link'),
            clipboard: b.getAttribute('data-clipboard-text'),
            dataHref: b.getAttribute('data-href'),
            onclick: (b.getAttribute('onclick')||'').substring(0,200),
            href: b.href || null
        }));
        cards.push({
            text: card.innerText.replace(/\\n+/g,' | ').substring(0,400),
            image, href, btnData,
            htmlSnippet: card.outerHTML.substring(0, 1500)
        });
    });
    return JSON.stringify({url: location.href, count: cards.length, cards: cards.slice(0,3)});
})()"""

async def cdp(ws, method, params=None, msg_id=1):
    await ws.send(json.dumps({"id": msg_id, "method": method, "params": params or {}}))
    while True:
        msg = json.loads(await ws.recv())
        if msg.get("id") == msg_id:
            return msg

async def main():
    async with websockets.connect(WS_URL, max_size=100*1024*1024) as ws:
        r = await cdp(ws, "Runtime.evaluate", {"expression": JS_CARDS, "returnByValue": True}, 1)
        val = r["result"]["result"].get("value")
        d = json.loads(val)
        print("URL:", d["url"], "| CARDS:", d["count"])
        for c in d["cards"]:
            print("="*60)
            print("TEXT:", c["text"][:250])
            print("HREF:", c["href"])
            print("IMG:", c["image"])
            print("BTNS:", json.dumps(c["btnData"], indent=1)[:800])
            print("HTML:", c["htmlSnippet"][:1200])

asyncio.run(main())
