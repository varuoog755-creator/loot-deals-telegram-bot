import json
import asyncio
import websockets

WS_URL = 'ws://127.0.0.1:9100/devtools/page/3FE1A88FEA67C60FC142F6C8D7313899'

JS_CARDS = """(() => {
    const out = [];
    document.querySelectorAll('li.prodlistDetail').forEach(li => {
        const nameEl = li.querySelector('a.product_name');
        const imgEl = li.querySelector('.product_img_mn img');
        const priceEl = li.querySelector('.p_totalprice');
        const mrpEl = li.querySelector('.price_strike del');
        const offEl = li.querySelector('.price_percentage strong');
        const brandEl = li.querySelector('.brand strong');
        const sellerEl = li.querySelector('.product_seller img');
        const labelEl = li.querySelector('.product_cat_label span');
        if (!nameEl) return;
        out.push({
            title: nameEl.getAttribute('title') || nameEl.innerText,
            href: location.origin + nameEl.getAttribute('href'),
            brand: brandEl ? brandEl.innerText.trim() : '',
            price: priceEl ? priceEl.innerText.trim() : '',
            mrp: mrpEl ? mrpEl.innerText.trim() : '',
            off: offEl ? offEl.innerText.replace(/[()%]/g,'').replace('off','').trim() : '',
            image: imgEl ? (imgEl.currentSrc || imgEl.src) : '',
            seller: sellerEl ? (sellerEl.src || '') : '',
            label: labelEl ? labelEl.innerText.trim() : ''
        });
    });
    return JSON.stringify({url: location.href, count: out.length, products: out});
})()"""

CATS = [
    ("electronics/headphones-headsets", "audio"),
    ("electronics/power-banks", "electronics"),
    ("electronics/best-speakers", "audio"),
    ("men-fashion/men-tshirt", "men-fashion"),
    ("men-fashion/men-jeans", "men-fashion"),
    ("men-fashion/men-shirts", "men-fashion"),
    ("women-fashion", "women-fashion"),
    ("men-footwear", "footwear"),
    ("women-footwear", "footwear"),
    ("beauty", "beauty"),
    ("accessories/watches", "watches"),
    ("home-kitchen", "home"),
]

async def cdp(ws, method, params=None, msg_id=1):
    await ws.send(json.dumps({"id": msg_id, "method": method, "params": params or {}}))
    while True:
        msg = json.loads(await ws.recv())
        if msg.get("id") == msg_id:
            return msg

async def main():
    async with websockets.connect(WS_URL, max_size=100*1024*1024) as ws:
        all_products = []
        mid = 100
        for cat, label in CATS:
            url = f"https://earnkaro.com/product/{cat}"
            await cdp(ws, "Page.navigate", {"url": url}, mid); mid += 1
            await asyncio.sleep(5)
            r = await cdp(ws, "Runtime.evaluate", {"expression": JS_CARDS, "returnByValue": True}, mid); mid += 1
            val = r.get("result", {}).get("result", {}).get("value")
            d = json.loads(val) if val else {}
            prods = d.get("products", [])
            for p in prods:
                p["category"] = label
                p["category_url"] = url
            all_products.extend(prods)
            print(f"{cat}: {len(prods)}")
        # dedupe by href
        seen = set(); final = []
        for p in all_products:
            if p["href"] in seen: continue
            seen.add(p["href"]); final.append(p)
        with open("earnkaro_products_full.json", "w", encoding="utf-8") as f:
            json.dump(final, f, indent=2, ensure_ascii=False)
        print(f"TOTAL UNIQUE: {len(final)}")

asyncio.run(main())
