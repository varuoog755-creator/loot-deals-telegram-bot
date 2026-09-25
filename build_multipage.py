import json
import os

with open("earnkaro_products_clean.json", "r", encoding="utf-8") as f:
    products = json.load(f)
with open("earnkaro_home_structure.json", "r", encoding="utf-8") as f:
    home = json.load(f)

CAT_META = {
    "audio": {"name": "Audio & Headphones", "icon": "🎧", "file": "audio.html",
              "banner": "https://asset21.ckassets.com/resources/image/category/headphones-headsets-996-1607082997.png",
              "url": "https://earnkaro.com/product/electronics/headphones-headsets"},
    "electronics": {"name": "Power Banks & Electronics", "icon": "🔌", "file": "electronics.html",
              "banner": "https://asset21.ckassets.com/resources/image/category/power-banks-2933-1607083221.png",
              "url": "https://earnkaro.com/product/electronics/power-banks"},
    "men-fashion": {"name": "Men's Fashion", "icon": "👔", "file": "men-fashion.html",
              "banner": "https://asset21.ckassets.com/resources/image/category/men-tshirt-2889-1607086734.png",
              "url": "https://earnkaro.com/product/men-fashion"},
    "women-fashion": {"name": "Women's Fashion", "icon": "👗", "file": "women-fashion.html",
              "banner": "https://asset21.ckassets.com/resources/image/category/myntra-super-sellers-web-3899-17902772140.png",
              "url": "https://earnkaro.com/product/women-fashion"},
    "footwear": {"name": "Footwear", "icon": "👟", "file": "footwear.html",
              "banner": "https://asset21.ckassets.com/resources/image/category/formal-shoes-2876-1607089457.png",
              "url": "https://earnkaro.com/product/men-footwear"},
    "beauty": {"name": "Beauty", "icon": "💄", "file": "beauty.html",
              "banner": "https://asset21.ckassets.com/resources/image/category/beauty-combo-offers-3281-1609918251.png",
              "url": "https://earnkaro.com/product/beauty"},
    "watches": {"name": "Watches & Accessories", "icon": "⌚", "file": "watches.html",
              "banner": "https://asset21.ckassets.com/resources/image/category/watches-3364-1607090111.png",
              "url": "https://earnkaro.com/product/accessories/watches"},
    "home": {"name": "Home & Kitchen", "icon": "🏠", "file": "home-kitchen.html",
              "banner": "https://asset21.ckassets.com/resources/image/category/home-furnishing-2871-1607089358.png",
              "url": "https://earnkaro.com/product/home-kitchen"},
}

SLIDER_BANNERS = [
    "https://asset22.ckassets.com/resources/image/staticpage_images/deskk-1789993298.png",
    "https://asset22.ckassets.com/resources/image/staticpage_images/shein-desk-1789992728.png",
    "https://asset22.ckassets.com/resources/image/staticpage_images/desk-1790185687.png",
    "https://asset22.ckassets.com/resources/image/staticpage_images/ajio-desk-1790273795.png",
    "https://asset22.ckassets.com/resources/image/staticpage_images/amazon-desk-1790273914.png",
    "https://asset22.ckassets.com/resources/image/staticpage_images/myntra-desk-1790273953.png",
    "https://asset22.ckassets.com/resources/image/staticpage_images/Desk-1786556000.png",
    "https://asset22.ckassets.com/resources/image/staticpage_images/Deskk-1790274029.png",
]

STORES = [
    ("Flipkart", "https://asset21.ckassets.com/resources/image/stores/flipkart-direct-3-1770728162.png", "https://earnkaro.com/stores/flipkart-direct-3"),
    ("Amazon", "https://asset21.ckassets.com/resources/image/stores/amazon-store-live-1-1777975646.png", "https://earnkaro.com/stores/amazon-store-live-1"),
    ("Myntra", "https://asset21.ckassets.com/resources/image/stores/myntra-new-t-1777980142.png", "https://earnkaro.com/stores/myntra-new-t"),
    ("Ajio", "https://asset21.ckassets.com/resources/image/stores/ajio-store-1606812055.png", "https://earnkaro.com/stores/ajio-direct-store"),
    ("Shopsy", "https://asset21.ckassets.com/resources/image/stores/shopsy-store-1692602320.png", "https://earnkaro.com/stores/shopsy-store"),
    ("Nykaa", "https://asset21.ckassets.com/resources/image/stores/nykaabeauty-1658489934.jpg", "https://earnkaro.com/stores/nykaabeauty-new-store"),
    ("M Caffeine", "https://asset21.ckassets.com/resources/image/stores/mcaffeine-store-4-1639372559.jpg", "https://earnkaro.com/stores/mcaffeine-trackier"),
    ("The Man Company", "https://asset21.ckassets.com/resources/image/stores/themancompany-direct-newstore-1778239912.png", "https://earnkaro.com/stores/themancompany-direct-newstore"),
]

TRENDING = [
    ("Today's Best Deals", "https://asset21.ckassets.com/resources/image/category/best-deals-today-4221-17779858440.png", "https://earnkaro.com/product/trending-offers/best-deals-today"),
    ("Flipkart Super Sellers", "https://asset21.ckassets.com/resources/image/category/flipkart-super-sellers-2-4248-17901870620.png", "https://earnkaro.com/product/trending-offers/flipkart-super-sellers-2"),
    ("Myntra Super Sellers", "https://asset21.ckassets.com/resources/image/category/myntra-super-sellers-web-3899-17902772140.png", "https://earnkaro.com/product/trending-offers/myntra-super-sellers-web"),
    ("Ajio Super Sellers", "https://asset21.ckassets.com/resources/image/category/ajio-superseller-3902-17902730170.png", "https://earnkaro.com/product/trending-offers/ajio-superseller"),
]

def esc(s):
    return (s or "").replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;").replace('"', "&quot;")

def nav_html(active_file):
    items = [("index.html", "🏠 Home")]
    for cat, m in CAT_META.items():
        items.append((m["file"], f'{m["icon"]} {m["name"]}'))
    out = ""
    for f, label in items:
        cls = " active" if f == active_file else ""
        out += f'<a href="{f}" class="nav-link{cls}">{label}</a>'
    return out

def card_html(p):
    title = esc(p["title"])
    price = esc(p["price"])
    mrp = esc(p.get("mrp", ""))
    off = p.get("off", "")
    img = esc(p["image"])
    href = esc(p["href"])
    profit = ""
    try:
        pr = int(p["price"].replace("₹", "").replace(",", ""))
        mr = int(p["mrp"].replace("₹", "").replace(",", ""))
        pv = int((mr - pr) * 0.10)
        if pv > 0: profit = f"Earn ₹{pv} Profit"
    except Exception: pass
    return f'''<div class="deal-card">
  <div class="deal-img-wrap"><img src="{img}" alt="{title}" class="deal-img" loading="lazy" onerror="this.src='https://asset21.ckassets.com/resources/image/stores/no-image.jpg'"><span class="deal-discount">{off}% OFF</span></div>
  <div class="deal-body">
    <h3 class="deal-title">{title}</h3>
    {f'<div class="deal-profit">💰 {profit}</div>' if profit else ''}
    <div class="deal-price-row"><span class="deal-price">{price}</span><span class="deal-mrp">{mrp}</span></div>
    <div class="deal-btns">
      <a href="{href}" target="_blank" rel="noopener" class="deal-btn">Grab Deal ⚡</a>
      <button class="copy-link-btn" onclick="copyLink('{href}', this)">📋 COPY LINK</button>
    </div>
  </div>
</div>'''

CSS = '''
*{margin:0;padding:0;box-sizing:border-box;-webkit-font-smoothing:antialiased}
body{font-family:'Inter',-apple-system,BlinkMacSystemFont,'Segoe UI',sans-serif;background:#fff;color:#000;line-height:1.5}
.container{max-width:1200px;margin:0 auto;padding:0 20px}
header{position:sticky;top:0;background:rgba(255,255,255,.96);backdrop-filter:blur(12px);border-bottom:1px solid #e5e7eb;z-index:100}
.header-inner{display:flex;align-items:center;justify-content:space-between;height:60px}
.brand{font-size:19px;font-weight:900;color:#000;text-decoration:none}
.brand-badge{background:#000;color:#fff;font-size:9px;font-weight:800;padding:3px 8px;border-radius:20px;margin-left:8px}
.header-btn{background:#000;color:#fff;text-decoration:none;font-size:12.5px;font-weight:700;padding:8px 16px;border-radius:20px;white-space:nowrap}
nav.topnav{border-bottom:1px solid #f1f5f9;background:#fff;position:sticky;top:60px;z-index:99}
.nav-scroll{display:flex;gap:4px;overflow-x:auto;scrollbar-width:none;padding:8px 0}
.nav-scroll::-webkit-scrollbar{display:none}
.nav-link{font-size:13px;font-weight:700;color:#6b7280;text-decoration:none;padding:7px 14px;border-radius:18px;white-space:nowrap}
.nav-link.active,.nav-link:hover{background:#000;color:#fff}
.hero{position:relative;max-width:1200px;margin:20px auto 0;padding:0 20px}
.slider{position:relative;border-radius:14px;overflow:hidden;aspect-ratio:16/6;background:#f9fafb}
.slide{position:absolute;inset:0;opacity:0;transition:opacity .6s}
.slide.on{opacity:1}
.slide img{width:100%;height:100%;object-fit:cover}
.slider-dots{position:absolute;bottom:10px;left:50%;transform:translateX(-50%);display:flex;gap:6px;z-index:5}
.dot{width:8px;height:8px;border-radius:50%;background:rgba(255,255,255,.6);cursor:pointer}
.dot.on{background:#000}
.section{padding:32px 0}
.section-title{font-size:clamp(22px,3vw,30px);font-weight:900;letter-spacing:-.7px;margin-bottom:4px}
.section-sub{color:#6b7280;font-size:13.5px;margin-bottom:20px;font-weight:500}
.cat-grid{display:grid;grid-template-columns:repeat(auto-fill,minmax(210px,1fr));gap:14px}
.cat-card{position:relative;height:120px;border-radius:12px;overflow:hidden;background:#000;text-decoration:none;display:flex;flex-direction:column;justify-content:flex-end;padding:14px;border:1px solid #e5e7eb;transition:.25s}
.cat-card:hover{transform:translateY(-3px)}
.cat-bg{position:absolute;inset:0;width:100%;height:100%;object-fit:contain;background:#fff;padding:12px;opacity:.9;transition:.25s}
.cat-ov{position:absolute;inset:0;background:linear-gradient(180deg,rgba(255,255,255,.85) 0%,rgba(255,255,255,0) 55%)}
.cat-cnt{position:relative;z-index:2}
.cat-nm{font-size:14.5px;font-weight:900;color:#000}
.cat-n-off{font-size:11.5px;font-weight:700;color:#16a34a}
.store-grid{display:grid;grid-template-columns:repeat(auto-fill,minmax(130px,1fr));gap:12px}
.store-card{background:#fff;border:1.5px solid #e5e7eb;border-radius:12px;padding:18px 10px;display:flex;flex-direction:column;align-items:center;gap:10px;text-decoration:none;transition:.25s}
.store-card:hover{border-color:#000;transform:translateY(-3px)}
.store-card img{max-width:100%;height:44px;object-fit:contain}
.store-card span{font-size:12.5px;font-weight:800;color:#000}
.tile-row{display:grid;grid-template-columns:repeat(auto-fill,minmax(230px,1fr));gap:14px}
.tile{border:1.5px solid #e5e7eb;border-radius:12px;overflow:hidden;text-decoration:none;display:block;transition:.25s;background:#fff}
.tile:hover{border-color:#000;transform:translateY(-3px)}
.tile img{width:100%;height:120px;object-fit:cover}
.tile span{display:block;padding:10px 12px;font-size:13px;font-weight:800;color:#000}
.deals-grid{display:grid;grid-template-columns:repeat(auto-fill,minmax(240px,1fr));gap:18px}
.deal-card{background:#fff;border:1.5px solid #e5e7eb;border-radius:12px;overflow:hidden;transition:.25s}
.deal-card:hover{transform:translateY(-4px);border-color:#000;box-shadow:0 12px 24px rgba(0,0,0,.08)}
.deal-img-wrap{position:relative;width:100%;height:220px;background:#fff;overflow:hidden}
.deal-img{width:100%;height:100%;object-fit:contain;transition:.3s;padding:8px}
.deal-card:hover .deal-img{transform:scale(1.05)}
.deal-discount{position:absolute;top:10px;right:10px;background:#ef4444;color:#fff;font-size:11px;font-weight:900;padding:4px 10px;border-radius:20px}
.deal-body{padding:14px 16px 16px}
.deal-title{font-size:13.5px;font-weight:800;line-height:1.35;margin-bottom:8px;display:-webkit-box;-webkit-line-clamp:2;-webkit-box-orient:vertical;overflow:hidden;min-height:37px}
.deal-profit{display:inline-flex;background:#fef3c7;color:#92400e;font-size:10.5px;font-weight:800;padding:3px 8px;border-radius:6px;margin-bottom:10px}
.deal-price-row{display:flex;align-items:baseline;gap:10px;margin-bottom:12px}
.deal-price{font-size:20px;font-weight:900}
.deal-mrp{font-size:13px;color:#9ca3af;text-decoration:line-through;font-weight:600}
.deal-btns{display:flex;flex-direction:column;gap:8px}
.deal-btn{display:flex;align-items:center;justify-content:center;width:100%;height:40px;background:#000;color:#fff;text-decoration:none;font-size:13px;font-weight:800;border-radius:8px;transition:.2s}
.deal-btn:hover{background:#16a34a}
.copy-link-btn{display:flex;align-items:center;justify-content:center;width:100%;height:36px;background:#fff;color:#000;border:1.5px solid #000;font-size:12px;font-weight:800;border-radius:8px;cursor:pointer;transition:.2s;font-family:inherit}
.copy-link-btn:hover{background:#f1f5f9}
.copy-link-btn.copied{background:#16a34a;color:#fff;border-color:#16a34a}
.page-banner{max-width:1200px;margin:20px auto 0;padding:0 20px}
.page-banner img{width:100%;height:180px;object-fit:contain;background:#f9fafb;border:1px solid #e5e7eb;border-radius:14px;padding:14px}
.tg-banner{background:#0a0e1a;border-radius:16px;padding:36px 28px;text-align:center;margin:36px 0;color:#fff}
.tg-banner h3{font-size:clamp(20px,3vw,28px);font-weight:900;margin-bottom:10px}
.tg-banner p{color:#9ca3af;max-width:540px;margin:0 auto 22px;font-size:14px}
.tg-btn{display:inline-flex;background:#0088cc;color:#fff;text-decoration:none;font-size:14px;font-weight:800;padding:12px 24px;border-radius:20px}
footer{border-top:1px solid #e5e7eb;padding:26px 0;text-align:center;color:#6b7280;font-size:13px;background:#f9fafb;margin-top:20px}
#toast{position:fixed;bottom:30px;left:50%;transform:translateX(-50%) translateY(80px);background:#000;color:#fff;padding:12px 24px;border-radius:20px;font-size:13px;font-weight:800;opacity:0;transition:.3s;z-index:1000;pointer-events:none}
#toast.show{transform:translateX(-50%) translateY(0);opacity:1}
.no-results{display:none;text-align:center;padding:40px;color:#6b7280;font-weight:700}
.search-bar{max-width:620px;margin:0 auto;height:50px;border:2px solid #e5e7eb;border-radius:25px;padding:0 20px;font-size:15px;font-family:inherit;outline:none;width:100%;display:block}
.search-bar:focus{border-color:#000}
@media(max-width:768px){.deals-grid{grid-template-columns:repeat(2,1fr);gap:12px}.deal-img-wrap{height:160px}.deal-title{font-size:12px}.deal-price{font-size:16px}.deal-btn{height:36px;font-size:11.5px}.copy-link-btn{height:32px;font-size:11px}.slider{aspect-ratio:16/9}.cat-grid{grid-template-columns:repeat(2,1fr)}}
'''

JS_COMMON = '''
function showToast(m){const t=document.getElementById('toast');t.innerText=m;t.classList.add('show');setTimeout(()=>t.classList.remove('show'),2200)}
function copyLink(url,btn){navigator.clipboard.writeText(url).then(()=>{const o=btn.innerText;btn.innerText='✓ COPIED';btn.classList.add('copied');showToast('EarnKaro link copied! Paste anywhere to share');setTimeout(()=>{btn.innerText=o;btn.classList.remove('copied')},2000)})}
function initSlider(){const slides=document.querySelectorAll('.slide');if(!slides.length)return;let i=0;slides[0].classList.add('on');const dots=document.querySelectorAll('.dot');if(dots[0])dots[0].classList.add('on');setInterval(()=>{slides[i].classList.remove('on');if(dots[i])dots[i].classList.remove('on');i=(i+1)%slides.length;slides[i].classList.add('on');if(dots[i])dots[i].classList.add('on')},3500)}
function setupSearch(){const inp=document.getElementById('searchInput');if(!inp)return;inp.addEventListener('input',e=>{const q=e.target.value.toLowerCase().trim();let n=0;document.querySelectorAll('.deal-card').forEach(c=>{const ok=!q||(c.dataset.q||'').includes(q);c.style.display=ok?'block':'none';if(ok)n++});const nr=document.getElementById('noResults');if(nr)nr.style.display=n?'none':'block'})}
initSlider();setupSearch();
'''

def head(title, desc, active):
    return f'''<!DOCTYPE html>
<html lang="en"><head><meta charset="UTF-8"><meta name="viewport" content="width=device-width,initial-scale=1.0">
<title>{esc(title)}</title><meta name="description" content="{esc(desc)}">
<link rel="preconnect" href="https://fonts.googleapis.com"><link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=Inter:wght@400;500;700;800;900&display=swap" rel="stylesheet">
<style>{CSS}</style></head><body>
<header><div class="container"><div class="header-inner">
<a href="index.html" class="brand">⚡ BigRedHub<span class="brand-badge">LIVE</span></a>
<a href="https://t.me/Under99LootDeals_bot" target="_blank" class="header-btn">Telegram Bot</a>
</div></div></header>
<nav class="topnav"><div class="container"><div class="nav-scroll">{nav_html(active)}</div></div></nav>'''

FOOTER = '''
<section class="container"><div class="tg-banner"><h3>Never Miss a 90% Price Drop</h3><p>Get instant price glitch alerts & Under ₹99 steals before they sell out.</p><a href="https://t.me/Under99LootDeals_bot" target="_blank" class="tg-btn">⚡ Open @Under99LootDeals_bot</a></div></section>
<footer><div class="container">© 2026 BigRedHub · Deals sourced live from EarnKaro · Affiliate disclosure: We earn a commission on qualifying purchases.</div></footer>
<div id="toast"></div><script>''' + JS_COMMON + '''</script></body></html>'''

# ---------- INDEX ----------
def build_index():
    slider = ""
    dots = ""
    for i, b in enumerate(SLIDER_BANNERS):
        cls = " on" if i == 0 else ""
        slider += f'<div class="slide{cls}"><img src="{b}" alt="Deal banner" loading="{"eager" if i==0 else "lazy"}"></div>'
        dots += f'<span class="dot{" on" if i==0 else ""}" onclick="goSlide({i})"></span>'
    cats = ""
    for cat, m in CAT_META.items():
        n = len([p for p in products if p["category"] == cat])
        best = max([int(p.get("off","0") or 0) for p in products if p["category"]==cat] or [0])
        cats += f'''<a href="{m['file']}" class="cat-card"><img src="{m['banner']}" alt="{m['name']}" class="cat-bg" loading="lazy"><div class="cat-ov"></div><div class="cat-cnt"><div class="cat-nm">{m['icon']} {esc(m['name'])}</div><div class="cat-n-off">{n} deals · up to {best}% OFF</div></div></a>'''
    stores = "".join(f'<a href="{u}" target="_blank" rel="noopener" class="store-card"><img src="{i}" alt="{n}" loading="lazy"><span>{n}</span></a>' for n, i, u in STORES)
    tiles = "".join(f'<a href="{u}" target="_blank" rel="noopener" class="tile"><img src="{i}" alt="{n}" loading="lazy"><span>{n} →</span></a>' for n, i, u in TRENDING)
    # top 12 deals by discount for home
    top = sorted(products, key=lambda x: -int(x.get("off","0") or 0))[:12]
    deals = "\n".join(card_html(p) for p in top)
    html = head("BigRedHub — Live EarnKaro Deals | Up to 90% OFF",
                "Live EarnKaro deals with real product photos & prices. Direct affiliate links.", "index.html")
    html += f'''
<section class="hero"><div class="slider">{slider}<div class="slider-dots">{dots}</div></div></section>
<section class="section container">
  <input type="text" id="searchInput" class="search-bar" placeholder="Search {len(products)} deals — boAt, jeans, watch...">
</section>
<section class="section container"><h2 class="section-title">Shop by Category</h2><p class="section-sub">{len(products)} live deals across {len(CAT_META)} categories</p><div class="cat-grid">{cats}</div></section>
<section class="section container" style="padding-top:0"><h2 class="section-title">Top Stores</h2><p class="section-sub">Earn commission on every order from India's biggest stores</p><div class="store-grid">{stores}</div></section>
<section class="section container" style="padding-top:0"><h2 class="section-title">Trending Collections</h2><div class="tile-row">{tiles}</div></section>
<section class="section container" style="padding-top:0"><h2 class="section-title">🔥 Biggest Discounts Today</h2><p class="section-sub">Top deals from every category — sorted by discount</p><div class="deals-grid">{deals}</div></section>
''' + FOOTER
    # slider go function
    html = html.replace("initSlider();setupSearch();", """function goSlide(n){const s=document.querySelectorAll('.slide');const d=document.querySelectorAll('.dot');s.forEach(x=>x.classList.remove('on'));d.forEach(x=>x.classList.remove('on'));s[n].classList.add('on');d[n].classList.add('on');cur=n}let cur=0;""" + JS_COMMON.split('initSlider();setupSearch();')[0].split('function goSlide')[0] if False else html)
    with open("index.html", "w", encoding="utf-8") as f: f.write(html)
    print("index.html:", len(top), "featured deals,", len(CAT_META), "categories,", len(STORES), "stores")

# ---------- CATEGORY PAGES ----------
def build_cat(cat):
    m = CAT_META[cat]
    prods = sorted([p for p in products if p["category"] == cat], key=lambda x: -int(x.get("off","0") or 0))
    deals = "\n".join(card_html(p) for p in prods)
    html = head(f"{m['name']} Deals — BigRedHub | Up to {max([int(p.get('off','0') or 0) for p in prods] or [0])}% OFF",
                f"{len(prods)} live {m['name']} deals from EarnKaro with direct affiliate links.", m["file"])
    html += f'''
<div class="page-banner"><img src="{m['banner']}" alt="{m['name']}" loading="eager"></div>
<section class="section container">
  <h2 class="section-title">{m['icon']} {esc(m['name'])}</h2>
  <p class="section-sub">{len(prods)} live deals · sorted by biggest discount · direct EarnKaro links</p>
  <input type="text" id="searchInput" class="search-bar" placeholder="Search in {esc(m['name'])}..." style="margin-bottom:22px">
  <div class="deals-grid">{deals}</div>
  <div class="no-results" id="noResults">😕 No deals found.</div>
</section>
''' + FOOTER
    with open(m["file"], "w", encoding="utf-8") as f: f.write(html)
    print(f"{m['file']}: {len(prods)} deals")

build_index()
for cat in CAT_META:
    build_cat(cat)
print("DONE — multipage site built")
