import json
import asyncio
import websockets

async def get_earnkaro_html():
    ws_url = 'ws://127.0.0.1:9100/devtools/page/3FE1A88FEA67C60FC142F6C8D7313899'
    
    async with websockets.connect(ws_url, max_size=10_000_000) as ws:
        # Scroll to load all images
        await ws.send(json.dumps({
            "id": 1,
            "method": "Runtime.evaluate",
            "params": {"expression": "window.scrollTo(0, document.body.scrollHeight); 'scrolled'"}
        }))
        await ws.recv()
        
        await asyncio.sleep(3)  # Wait for lazy images
        
        # Get full HTML
        await ws.send(json.dumps({
            "id": 2,
            "method": "Runtime.evaluate",
            "params": {
                "expression": "document.documentElement.outerHTML",
                "returnByValue": True
            }
        }))
        
        response = await ws.recv()
        result = json.loads(response)
        
        if 'result' in result and 'result' in result['result']:
            html = result['result']['result']['value']
            
            with open("earnkaro_full_page.html", "w", encoding="utf-8") as f:
                f.write(html)
            
            print(f"✅ Saved full page HTML ({len(html)} chars)")
            
            # Preview image URLs
            import re
            images = re.findall(r'<img[^>]*src=["\']([^"\']*)["\']', html)
            print(f"\n📸 Found {len(images)} image tags")
            
            # Find copy links
            copy_links = re.findall(r'href=["\']([^"\']*earnkaro\.com[^"\']*)["\']', html)
            print(f"🔗 Found {len(copy_links)} EarnKaro links")
            
            if images:
                print("\n🖼️ Sample images:")
                for img in images[:10]:
                    if 'http' in img and len(img) > 20:
                        print(f"   {img}")
            
            if copy_links:
                print("\n🔗 Sample copy links:")
                for link in copy_links[:5]:
                    print(f"   {link}")
        else:
            print("⚠️ Failed to extract HTML")

try:
    asyncio.run(get_earnkaro_html())
except Exception as e:
    print(f"❌ Error: {e}")
