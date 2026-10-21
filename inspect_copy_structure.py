import json
import asyncio
import websockets

async def inspect_earnkaro_html_structure():
    ws_url = 'ws://127.0.0.1:9100/devtools/page/3FE1A88FEA67C60FC142F6C8D7313899'
    async with websockets.connect(ws_url, max_size=50_000_000) as ws:
        eval_script = """
        (() => {
            // Find elements containing 'COPY LINK'
            const copyNodes = [];
            const walker = document.createTreeWalker(document.body, NodeFilter.SHOW_TEXT);
            let node;
            while (node = walker.nextNode()) {
                if (node.nodeValue && node.nodeValue.trim() === 'COPY LINK') {
                    const parent = node.parentElement;
                    // Find card ancestor (e.g. 3-6 levels up)
                    let ancestor = parent;
                    for (let i = 0; i < 6; i++) {
                        if (ancestor && ancestor.parentElement && ancestor.parentElement !== document.body) {
                            ancestor = ancestor.parentElement;
                        }
                    }
                    copyNodes.push({
                        parentTag: parent.tagName,
                        parentClass: parent.className,
                        parentAttrs: Array.from(parent.attributes).map(a => `${a.name}="${a.value}"`),
                        ancestorHTML: ancestor ? ancestor.outerHTML.substring(0, 1000) : ''
                    });
                }
            }
            return copyNodes.slice(0, 5);
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
        print(json.dumps(data.get("result", {}).get("result", {}).get("value", []), indent=2))

asyncio.run(inspect_earnkaro_html_structure())
