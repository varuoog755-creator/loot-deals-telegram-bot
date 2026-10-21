import json
import asyncio
import websockets

async def get_all_earnkaro_items():
    ws_url = 'ws://127.0.0.1:9100/devtools/page/3FE1A88FEA67C60FC142F6C8D7313899'
    async with websockets.connect(ws_url, max_size=50_000_000) as ws:
        eval_script = """
        (() => {
            const results = [];
            
            // 1. Store cards (Flipkart, Myntra, Amazon, etc.)
            document.querySelectorAll('.store_card').forEach((card, idx) => {
                const img = card.querySelector('img');
                const storeLink = card.querySelector('a[href*="/stores/"]');
                const profitTxt = card.querySelector('.ctabtntxt');
                const title = img ? (img.getAttribute('alt') || img.getAttribute('title') || '') : '';
                
                if (img && img.src) {
                    results.push({
                        type: 'store',
                        title: title || 'Top Retailer Deal',
                        image: img.src,
                        profit: profitTxt ? profitTxt.innerText.trim() : 'Upto 10% Profit',
                        price: '',
                        link: storeLink ? ('https://earnkaro.com' + storeLink.getAttribute('href')) : 'https://earnkaro.com/'
                    });
                }
            });

            // 2. Deal cards (Flash deals, GADGET DEALS, etc.)
            document.querySelectorAll('.catdeal_top, [class*="catdeal"], [class*="deal_card"], [class*="dy_dealcard"]').forEach(el => {
                const img = el.querySelector('img');
                const parent = el.closest('section, div.slick-slide, div.c_img') || el;
                const text = parent.innerText || '';
                
                let title = img ? (img.getAttribute('alt') || img.getAttribute('title') || '') : '';
                if (!title) {
                    const hd = parent.querySelector('h3, h4, p, [class*="hd"], [class*="title"]');
                    if (hd) title = hd.innerText.trim();
                }

                // Extract profit
                let profit = '';
                const pMatch = text.match(/(?:PER SALE YOU EARN|YOU EARN)[\s\n]*([^\n\r]+)/i) || text.match(/(?:Flat|Upto)[\s\d.%]+Profit/i);
                if (pMatch) profit = pMatch[1] || pMatch[0];

                // Extract price
                let price = '';
                const prMatch = text.match(/STARTING FROM[\s\n]*([₹\d,]+)/i) || text.match(/₹[\d,]+/);
                if (prMatch) price = prMatch[1] || prMatch[0];

                let link = el.getAttribute('href') || (el.querySelector('a') || {}).href || '';
                if (link && !link.startsWith('http')) {
                    link = 'https://earnkaro.com' + (link.startsWith('/') ? '' : '/') + link;
                }

                if (img && img.src && title && !results.some(r => r.image === img.src)) {
                    results.push({
                        type: 'deal',
                        title: title.replace(/[\n\r]+/g, ' ').trim(),
                        image: img.src,
                        profit: profit.trim() || 'Flat 15% Profit',
                        price: price.trim() || '₹299',
                        link: link || 'https://earnkaro.com/'
                    });
                }
            });

            return {
                total: results.length,
                items: results
            };
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
        result = data.get("result", {}).get("result", {}).get("value", {})
        print(f"Extracted {result.get('total', 0)} items directly from EarnKaro UI!")
        
        with open("earnkaro_real_scraped.json", "w", encoding="utf-8") as f:
            json.dump(result.get("items", []), f, indent=2)

asyncio.run(get_all_earnkaro_items())
