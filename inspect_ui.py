import json
import asyncio
import websockets

async def inspect_earnkaro_ui():
    ws_url = 'ws://127.0.0.1:9100/devtools/page/3FE1A88FEA67C60FC142F6C8D7313899'
    async with websockets.connect(ws_url, max_size=50_000_000) as ws:
        # Evaluate script to get UI elements, buttons, copy link buttons, image styling
        eval_script = """
        (() => {
            // Get all product cards
            const cards = [];
            document.querySelectorAll('div, a, section').forEach(el => {
                const text = el.innerText || '';
                // Check if element has price and copy/share
                if (text.includes('₹') && (text.toLowerCase().includes('copy') || text.toLowerCase().includes('share') || text.toLowerCase().includes('profit'))) {
                    // Look for card containers
                    const img = el.querySelector('img');
                    if (img && img.src && !cards.some(c => c.img === img.src)) {
                        const copyBtn = Array.from(el.querySelectorAll('button, a, div')).find(b => (b.innerText || '').toLowerCase().includes('copy'));
                        const shareBtn = Array.from(el.querySelectorAll('button, a, div')).find(b => (b.innerText || '').toLowerCase().includes('share'));
                        
                        cards.push({
                            title: (el.querySelector('h1, h2, h3, h4, h5, p, [class*="title"]') || {}).innerText || '',
                            img: img.src,
                            imgClass: img.className,
                            imgStyle: img.getAttribute('style') || '',
                            hasCopy: !!copyBtn,
                            copyText: copyBtn ? copyBtn.innerText : '',
                            hasShare: !!shareBtn,
                            fullSnippet: el.outerHTML.substring(0, 500)
                        });
                    }
                }
            });

            // Look specifically for copy buttons or copy link action
            const allButtons = Array.from(document.querySelectorAll('button, a')).map(b => ({
                tag: b.tagName,
                text: b.innerText.trim(),
                className: b.className,
                href: b.getAttribute('href') || ''
            })).filter(b => b.text.toLowerCase().includes('copy') || b.text.toLowerCase().includes('share') || b.text.toLowerCase().includes('link'));

            return {
                cardsCount: cards.length,
                sampleCards: cards.slice(0, 4),
                buttons: allButtons.slice(0, 15),
                documentTitle: document.title,
                url: window.location.href
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
        print(json.dumps(data.get("result", {}).get("result", {}).get("value", {}), indent=2))

asyncio.run(inspect_earnkaro_ui())
