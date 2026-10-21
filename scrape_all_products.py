import json
import asyncio
import re
import websockets

WS_URL = 'ws://127.0.0.1:9100/devtools/page/3FE1A88FEA67C60FC142F6C8D7313899'

JS_EXTRACT = """(() => {
    const out = [];
    document.querySelectorAll('li.prodlistDetail').forEach(li => {
        const nameEl = li.querySelector('a.product_name');
        const imgEl = li.querySelector('.product_img_mn img');
        const priceEl = li.querySelector('.p_totalprice');
        const mrpEl = li.querySelector('.price_strike del');
        const discEl = li.querySelector('.price_percentage');
        const brandEl = li.querySelector('.brand strong');
        const storeEl = li.querySelector('.product_seller img');
        if (!nameEl) return;
        const href = nameEl.getAttribute('href') || '';
        out.push({
            name: nameEl.innerText.trim(),
            href: href.startsWith('/') ? 'https://earnkaro.com' + href : href,
            image: imgEl ? (imgEl.currentSrc || imgEl.src) : null,
            price: priceEl ? priceEl.innerText.trim() : null,
            mrp: mrpEl ? mrpEl.innerText.trim() : null,
            discount: discEl ? discEl.innerText.replace(/[^0-9%]/g,'') : null,
            brand: brandEl ? brandEl.innerText.trim() : null,
            cardId: (li.querySelector('[id^="copylink_products_"]') || {}).id || null
        });
    });
    // also grab page's category url if present
    const pageEl = document.querySelector('#page_scroll');
    return JSON.stringify({url: location.href, dataUrl: pageEl ? pageEl.getAttribute('data-url') : null, count: out.length, products: out});
})()"""

CATS = [
    "electronics/headphones-headsets", "electronics/power-banks", "electronics/best-speakers",
    "men-fashion/men-tshirt", "men-fashion/men-jeans", "men-fashion/men-shirts",
    "women-fashion", "men-footwear", "women-footwear", "beauty",
    "accessories/watches", "home-kitchen", "mobile-phones-offers",
]

async def cdp(ws, method, params=None, msg_id=1):
    await ws.send(json.dumps({"id": msg_id, "method": method, "params": params or {}}))
    while True:
        msg = json.loads(await ws.recv())
        if msg.get("id") == msg_id:
            return msg

async def main():
    async with websockets.connect(WS_URL, max_size=100*1024*1024) as ws:
        mid = 100
        all_products = {}
        for cat in CATS:
            url = f"https://earnkaro.com/product/{cat}"
            await cdp(ws, "Page.navigate", {"url": url}, mid); mid += 1
            await asyncio.sleep(4.5)
            # scroll to trigger infinite scroll load
            for s in range(3):
                await cdp(ws, "Runtime.evaluate", {"expression": "window.scrollTo(0, document.body.scrollHeight)"}, mid); mid += 1
                await asyncio.sleep(1.5)
            r = await cdp(ws, "Runtime.evaluate", {"expression": JS_EXTRACT, "returnByValue": True}, mid); mid += 1
            val = r.get("result", {}).get("result", {}).get("value")
            d = json.loads(val) if val else {}
            prods = d.get("products", [])
            all_products[cat] = prods
            print(f"{cat}: {len(prods)} products")
        with open("earnkaro_all_products.json", "w", encoding="utf-8") as f:
            json.dump(all_products, f, indent=2, ensure_ascii=False)
        total = sum(len(v) for v in all_products.values())
        print(f"TOTAL: {total} products -> earnkaro_all_products.json")

asyncio.run(main())
