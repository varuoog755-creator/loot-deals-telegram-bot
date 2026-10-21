import json
import asyncio
import websockets

async def extract_exact_earnkaro_data():
    ws_url = 'ws://127.0.0.1:9100/devtools/page/3FE1A88FEA67C60FC142F6C8D7313899'
    
    async with websockets.connect(ws_url, max_size=10_000_000) as ws:
        # Enable DOM domain
        await ws.send(json.dumps({"id": 1, "method": "DOM.enable"}))
        await ws.recv()
        
        # Scroll page to load lazy images
        await ws.send(json.dumps({
            "id": 2,
            "method": "Runtime.evaluate",
            "params": {"expression": "window.scrollTo(0, document.body.scrollHeight)"}
        }))
        await ws.recv()
        
        await asyncio.sleep(2)  # Wait for images to load
        
        # Extract ALL product cards with images and copy links
        js_code = """
        (() => {
            const products = [];
            
            // Find all deal cards on page
            const cards = document.querySelectorAll('[class*="deal"], [class*="product"], [class*="card"]');
            
            cards.forEach((card, idx) => {
                try {
                    // Extract image
                    const img = card.querySelector('img');
                    const imgSrc = img ? (img.src || img.dataset.src || img.getAttribute('data-original')) : null;
                    
                    // Extract title
                    const titleEl = card.querySelector('[class*="title"], h3, h4, [class*="name"]');
                    const title = titleEl ? titleEl.innerText.trim() : '';
                    
                    // Extract price
                    const priceEl = card.querySelector('[class*="price"]:not([class*="strike"]):not([class*="original"])');
                    const price = priceEl ? priceEl.innerText.trim() : '';
                    
                    // Extract MRP
                    const mrpEl = card.querySelector('[class*="strike"], [class*="original"], del, s');
                    const mrp = mrpEl ? mrpEl.innerText.trim() : '';
                    
                    // Extract discount
                    const discEl = card.querySelector('[class*="discount"], [class*="off"]');
                    const discount = discEl ? discEl.innerText.trim() : '';
                    
                    // Extract store/brand
                    const storeEl = card.querySelector('[class*="store"], [class*="brand"], [class*="partner"]');
                    const store = storeEl ? storeEl.innerText.trim() : '';
                    
                    // Extract "Copy Link" button's data-url or href
                    const copyBtn = card.querySelector('[class*="copy"], [data-url], a[href*="earnkaro"]');
                    let copyLink = '';
                    
                    if (copyBtn) {
                        copyLink = copyBtn.getAttribute('data-url') || 
                                   copyBtn.getAttribute('href') || 
                                   copyBtn.dataset.link || '';
                    }
                    
                    // If no copy link found in button, find any earnkaro link in card
                    if (!copyLink) {
                        const links = card.querySelectorAll('a[href*="earnkaro"]');
                        if (links.length > 0) {
                            copyLink = links[0].href;
                        }
                    }
                    
                    if (imgSrc && title && copyLink) {
                        products.push({
                            id: `ek_${idx}`,
                            title: title,
                            price: price,
                            mrp: mrp,
                            discount: discount,
                            store: store,
                            image: imgSrc,
                            copy_link: copyLink
                        });
                    }
                } catch (e) {
                    console.error('Card parse error:', e);
                }
            });
            
            return products;
        })()
        """
        
        await ws.send(json.dumps({
            "id": 3,
            "method": "Runtime.evaluate",
            "params": {
                "expression": js_code,
                "returnByValue": True,
                "awaitPromise": False
            }
        }))
        
        response = await ws.recv()
        result = json.loads(response)
        
        if 'result' in result and 'result' in result['result']:
            products = result['result']['result']['value']
            
            with open("earnkaro_exact_products.json", "w", encoding="utf-8") as f:
                json.dump(products, f, indent=2, ensure_ascii=False)
            
            print(f"✅ Extracted {len(products)} products with exact images & copy links!")
            
            for p in products[:5]:  # Preview first 5
                print(f"\n📦 {p['title'][:50]}")
                print(f"   💰 {p['price']} (MRP {p['mrp']}) {p['discount']}")
                print(f"   🏪 {p['store']}")
                print(f"   🖼️  {p['image'][:60]}...")
                print(f"   🔗 {p['copy_link'][:70]}...")
        else:
            print("⚠️ No products found or parsing error")
            print(json.dumps(result, indent=2))

try:
    asyncio.run(extract_exact_earnkaro_data())
except Exception as e:
    print(f"❌ Error: {e}")
