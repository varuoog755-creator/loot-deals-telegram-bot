import json
import asyncio
import websockets

async def check_earnkaro_architecture():
    ws_url = 'ws://127.0.0.1:9100/devtools/page/3FE1A88FEA67C60FC142F6C8D7313899'
    async with websockets.connect(ws_url, max_size=20*1024*1024) as ws:
        async def send_cmd(method, params={}):
            req_id = 999
            await ws.send(json.dumps({'id': req_id, 'method': method, 'params': params}))
            while True:
                msg = json.loads(await ws.recv())
                if msg.get('id') == req_id:
                    return msg.get('result', {})

        # 1. Let's inspect Partner Stores and Profit Rates
        await send_cmd('Page.navigate', {'url': 'https://earnkaro.com/stores'})
        await asyncio.sleep(3)
        
        stores_data = await send_cmd('Runtime.evaluate', {
            'expression': '''
            (() => {
                const storeCards = Array.from(document.querySelectorAll('.store_listing_box, .store_box, .partner_box, div[class*="store"], li[class*="store"]')).map(el => {
                    const name = el.querySelector('h2, h3, h4, .store_name, p, img[alt]')?.innerText || el.querySelector('img')?.alt || '';
                    const profit = el.querySelector('.profit_rate, .rates, span[class*="profit"], p[class*="profit"]')?.innerText || '';
                    const link = el.querySelector('a')?.href || '';
                    const logo = el.querySelector('img')?.src || '';
                    return { name: name.trim(), profit: profit.trim(), link, logo };
                }).filter(s => s.name && (s.profit || s.link));
                
                return {
                    title: document.title,
                    totalStores: storeCards.length,
                    sample: storeCards.slice(0, 15)
                };
            })()
            ''',
            'returnByValue': True
        })
        
        print("=== EARNKARO PARTNER STORES & PROFIT RATES ===")
        print(json.dumps(stores_data.get('result', {}).get('value'), indent=2))

asyncio.run(check_earnkaro_architecture())
