import json
import asyncio
import websockets

WS_URL = 'ws://127.0.0.1:9100/devtools/page/3FE1A88FEA67C60FC142F6C8D7313899'

JS_PRODUCTS = """(() => {
    const out = [];
    // Product cards on EarnKaro category pages
    document.querySelectorAll('a').forEach(a => {
        const href = a.href || '';
        if (!href.includes('/product/')) return;
        // deep product link: /product/<cat>/<id or slug> with more depth or contains digits beyond category
        const parts = href.replace('https://earnkaro.com/product/', '').split('/');
        const img = a.querySelector('img') || (a.closest('div') && a.closest('div').querySelector('img'));
        const image = img ? (img.currentSrc || img.src) : null;
        const text = (a.innerText || '').replace(/\\s+\\n/g, ' | ').replace(/\\n+/g, ' | ').trim();
        // A real product card has price text like ₹ and an image
        if (!image || !text || text.length < 20) return;
        out.push({href, image, text: text.substring(0, 500)});
    });
    return JSON.stringify({url: location.href, count: out.length, products: out});
})()"""

async def cdp(ws, method, params=None, msg_id=1):
    await ws.send(json.dumps({"id": msg_id, "method": method, "params": params or {}}))
    while True:
        msg = json.loads(await ws.recv())
        if msg.get("id") == msg_id:
            return msg

async def main():
    async with websockets.connect(WS_URL, max_size=50*1024*1024) as ws:
        all_products = {}
        cats = ["electronics/headphones-headsets", "men-fashion/men-tshirt", "women-fashion",
                "men-footwear", "beauty", "home-kitchen", "accessories/watches"]
        mid = 10
        for cat in cats:
            url = f"https://earnkaro.com/product/{cat}"
            await cdp(ws, "Page.navigate", {"url": url}, mid); mid += 1
            await asyncio.sleep(4)
            r = await cdp(ws, "Runtime.evaluate", {"expression": JS_PRODUCTS, "returnByValue": True}, mid); mid += 1
            val = r.get("result", {}).get("result", {}).get("value")
            data = json.loads(val) if val else {}
            prods = data.get("products", [])
            all_products[cat] = prods
            print(f"{cat}: {len(prods)} products")
        with open("earnkaro_category_products.json", "w", encoding="utf-8") as f:
            json.dump(all_products, f, indent=2, ensure_ascii=False)
        print("Saved earnkaro_category_products.json")

asyncio.run(main())
