import json
import asyncio
import websockets

async def get_exact_earnkaro_deals():
    ws_url = 'ws://127.0.0.1:9100/devtools/page/3FE1A88FEA67C60FC142F6C8D7313899'
    async with websockets.connect(ws_url, max_size=50_000_000) as ws:
        # Extract individual deal cards from EarnKaro home page
        eval_script = """
        (() => {
            const deals = [];
            
            // Look for product/deal sections
            // On EarnKaro, each deal card has an image, title, price, profit and copy/share buttons
            document.querySelectorAll('div, section, li').forEach(el => {
                // Find cards with img and COPY LINK or SHARE NOW
                const hasCopy = Array.from(el.querySelectorAll('a, button')).some(b => (b.innerText || '').trim() === 'COPY LINK');
                const hasShare = Array.from(el.querySelectorAll('a, button')).some(b => (b.innerText || '').trim() === 'SHARE NOW');
                const img = el.querySelector('img');
                
                if ((hasCopy || hasShare) && img && img.src && !img.src.includes('home_icon') && !img.src.includes('avatar') && !img.src.includes('logo')) {
                    // Check if this is an innermost deal card container
                    const childCards = el.querySelectorAll('div, section, li');
                    const hasInnerCard = Array.from(childCards).some(c => c !== el && Array.from(c.querySelectorAll('a, button')).some(b => (b.innerText || '').trim() === 'COPY LINK') && c.querySelector('img'));
                    
                    if (!hasInnerCard) {
                        const titleEl = el.querySelector('h1, h2, h3, h4, h5, p, [class*="title"], [class*="hd"], [class*="name"], .catdeal_top');
                        const title = titleEl ? titleEl.innerText.trim() : (img.getAttribute('alt') || img.getAttribute('title') || '');
                        
                        const text = el.innerText || '';
                        
                        // Extract profit
                        let profit = '';
                        const profitMatch = text.match(/(?:YOU EARN|PER SALE YOU EARN|YOU MAKE|PROFIT)[\s:]*([^\n\r]+)/i) || text.match(/(?:Flat|Upto|Rs|₹)[\d.%]+ (?:Profit|Cashback)/i);
                        if (profitMatch) {
                            profit = profitMatch[0].trim();
                        }
                        
                        // Extract price
                        let price = '';
                        const priceMatch = text.match(/(?:STARTING FROM|PRICE|₹|Rs\.?)[\s:]*([₹\d,]+)/i) || text.match(/[₹Rs\.]+\s*([\d,]+)/);
                        if (priceMatch) {
                            price = priceMatch[0].trim();
                        }
                        
                        // Extract deal link
                        const linkEl = el.querySelector('a[href*="/"]');
                        let dealHref = linkEl ? linkEl.getAttribute('href') : '';
                        if (dealHref && !dealHref.startsWith('http') && !dealHref.startsWith('#')) {
                            dealHref = 'https://earnkaro.com' + (dealHref.startsWith('/') ? '' : '/') + dealHref;
                        }

                        // Get copy link target or onclick if any
                        const copyBtn = Array.from(el.querySelectorAll('a, button')).find(b => (b.innerText || '').trim() === 'COPY LINK');
                        let copyAction = copyBtn ? (copyBtn.getAttribute('href') || copyBtn.getAttribute('onclick') || copyBtn.getAttribute('data-url') || '') : '';

                        if (title && (img.src.includes('ckassets') || img.src.includes('http')) && !deals.some(d => d.img === img.src && d.title === title)) {
                            deals.push({
                                title: title.replace(/[\n\r]+/g, ' ').substring(0, 100),
                                image: img.src,
                                price: price || 'Special Deal',
                                profit: profit || 'High Profit',
                                dealUrl: dealHref || 'https://earnkaro.com/',
                                copyAction: copyAction
                            });
                        }
                    }
                }
            });

            return deals;
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
        deals = data.get("result", {}).get("result", {}).get("value", [])
        print(f"Extracted {len(deals)} exact EarnKaro live deals:")
        print(json.dumps(deals[:10], indent=2))
        
        with open("earnkaro_exact_live_deals.json", "w", encoding="utf-8") as f:
            json.dump(deals, f, indent=2)

asyncio.run(get_exact_earnkaro_deals())
