import json
import asyncio
import websockets

async def inspect_page_dom():
    ws_url = 'ws://127.0.0.1:9100/devtools/page/3FE1A88FEA67C60FC142F6C8D7313899'
    async with websockets.connect(ws_url, max_size=20*1024*1024) as ws:
        async def send_cmd(method, params={}):
            req_id = 100
            await ws.send(json.dumps({'id': req_id, 'method': method, 'params': params}))
            while True:
                msg = json.loads(await ws.recv())
                if msg.get('id') == req_id:
                    return msg.get('result', {})

        # Navigate to top selling deals
        await send_cmd('Page.navigate', {'url': 'https://earnkaro.com/product/electronics'})
        await asyncio.sleep(4)
        
        dom_analysis = await send_cmd('Runtime.evaluate', {
            'expression': '''
            (() => {
                // Find all product containers
                const items = Array.from(document.querySelectorAll('div, li, article')).filter(el => {
                    const txt = el.innerText || '';
                    return (txt.includes('₹') || txt.includes('Rs.')) && (txt.includes('Profit') || txt.includes('Share') || txt.includes('OFF') || txt.includes('Buy'));
                }).filter(el => el.children.length > 2 && el.children.length < 15);
                
                // Inspect the first item in detail
                let sampleItem = null;
                if (items.length > 0) {
                    const el = items[0];
                    sampleItem = {
                        html: el.outerHTML.slice(0, 1000),
                        text: el.innerText,
                        classes: el.className,
                        imgs: Array.from(el.querySelectorAll('img')).map(i => ({ src: i.src, dataSrc: i.dataset.src, alt: i.alt })),
                        links: Array.from(el.querySelectorAll('a')).map(a => ({ text: a.innerText, href: a.href }))
                    };
                }
                
                // Find all images on the page
                const allImages = Array.from(document.querySelectorAll('img')).map(i => ({
                    src: i.src || i.dataset.src,
                    alt: i.alt,
                    w: i.naturalWidth,
                    h: i.naturalHeight
                })).filter(i => i.src && !i.src.includes('data:image/svg') && (i.src.includes('earnkaro') || i.src.includes('cloudinary') || i.src.includes('asset') || i.src.includes('product') || i.src.includes('banner'))).slice(0, 20);

                return {
                    title: document.title,
                    itemCount: items.length,
                    sampleItem,
                    allImages
                };
            })()
            ''',
            'returnByValue': True
        })
        
        print("DOM ANALYSIS:")
        print(json.dumps(dom_analysis.get('result', {}).get('value'), indent=2))

asyncio.run(inspect_page_dom())
