import json

with open("earnkaro_products_clean.json", "r", encoding="utf-8") as f:
    products = json.load(f)

CAT_META = {
    "audio": {"name": "Audio & Headphones", "icon": "🎧"},
    "electronics": {"name": "Power & Electronics", "icon": "🔌"},
    "men-fashion": {"name": "Men's Fashion", "icon": "👔"},
    "women-fashion": {"name": "Women's Fashion", "icon": "👗"},
    "footwear": {"name": "Footwear", "icon": "👟"},
    "beauty": {"name": "Beauty", "icon": "💄"},
    "watches": {"name": "Watches", "icon": "⌚"},
    "home": {"name": "Home & Kitchen", "icon": "🏠"},
}

def esc(s):
    return (s or "").replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;").replace('"', "&quot;")

def card_html(p, idx):
    title = esc(p["title"])
    brand = esc(p.get("brand", ""))
    price = esc(p["price"])
    mrp = esc(p.get("mrp", ""))
    off = p.get("off", "")
    img = esc(p["image"])
    href = esc(p["href"])
    cat = p["category"]
    cat_name = CAT_META.get(cat, {}).get("name", cat)
    cat_icon = CAT_META.get(cat, {}).get("icon", "🛍️")
    profit = ""
    try:
        pr = int(p["price"].replace("₹", "").replace(",", ""))
        mr = int(p["mrp"].replace("₹", "").replace(",", ""))
        profit_val = int((mr - pr) * 0.10)
        if profit_val > 0:
            profit = f"Earn ₹{profit_val} Profit"
    except Exception:
        pass
    return f'''<div class="deal-card" data-cat="{cat}" data-q="{title.lower()} {brand.lower()}">
  <div class="deal-img-wrap">
    <img src="{img}" alt="{title}" class="deal-img" loading="lazy" onerror="this.src='https://asset21.ckassets.com/resources/image/stores/no-image.jpg'">
    <span class="deal-discount">{off}% OFF</span>
  </div>
  <div class="deal-body">
    <div class="deal-store">{cat_icon} {esc(cat_name)}</div>
    <h3 class="deal-title">{title}</h3>
    {f'<div class="deal-profit">💰 {profit}</div>' if profit else ''}
    <div class="deal-price-row">
      <span class="deal-price">{price}</span>
      <span class="deal-mrp">{mrp}</span>
    </div>
    <a href="{href}" target="_blank" rel="noopener noreferrer" class="deal-btn">Grab Deal ⚡</a>
  </div>
</div>'''

# Category chips
chips = '<button class="filter-pill active" onclick="filterCat(\'all\', this)">All ({})</button>'.format(len(products))
for cat, meta in CAT_META.items():
    n = len([p for p in products if p["category"] == cat])
    if n:
        chips += f'<button class="filter-pill" onclick="filterCat(\'{cat}\', this)">{meta["icon"]} {esc(meta["name"])} ({n})</button>'

# Cards grouped by category, price-sorted (best discounts first)
cards = []
for cat in CAT_META:
    cat_prods = sorted([p for p in products if p["category"] == cat],
                       key=lambda x: -int(x.get("off", "0") or 0))
    for p in cat_prods:
        cards.append(card_html(p, len(cards)))
cards_html = "\n".join(cards)

html = f'''<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>BigRedHub — Live EarnKaro Deals | Up to 90% OFF</title>
<meta name="description" content="Live EarnKaro deals with real product photos & prices from Myntra, Tata CLiQ, Ajio, Amazon, boAt. Direct affiliate links.">
<style>
*{{margin:0;padding:0;box-sizing:border-box;-webkit-font-smoothing:antialiased}}
body{{font-family:'Inter',-apple-system,BlinkMacSystemFont,'Segoe UI',sans-serif;background:#ffffff;color:#000;line-height:1.5;padding-bottom:70px}}
.container{{max-width:1200px;margin:0 auto;padding:0 20px}}
header{{position:sticky;top:0;background:rgba(255,255,255,.95);backdrop-filter:blur(12px);border-bottom:1px solid #e5e7eb;z-index:100}}
.header-inner{{display:flex;align-items:center;justify-content:space-between;height:64px}}
.brand{{font-size:20px;font-weight:900;color:#000;text-decoration:none;letter-spacing:-.5px}}
.brand-badge{{background:#000;color:#fff;font-size:9px;font-weight:800;padding:3px 8px;border-radius:20px;margin-left:8px}}
.header-btn{{background:#000;color:#fff;text-decoration:none;font-size:13px;font-weight:700;padding:9px 18px;border-radius:20px}}
.hero{{padding:44px 0 28px;text-align:center;background:linear-gradient(180deg,#f9fafb 0,#fff 100%);border-bottom:1px solid #e5e7eb}}
.hero-pill{{display:inline-flex;background:#dcfce7;border:1px solid #86efac;color:#166534;font-size:11px;font-weight:800;padding:5px 12px;border-radius:20px;margin-bottom:14px;text-transform:uppercase}}
.hero-title{{font-size:clamp(30px,5vw,50px);font-weight:900;letter-spacing:-1.2px;line-height:1.1;margin-bottom:12px}}
.hero-subtitle{{color:#6b7280;font-size:clamp(14px,2vw,17px);max-width:620px;margin:0 auto 24px;font-weight:500}}
.search-bar{{max-width:620px;margin:0 auto;height:52px;border:2px solid #e5e7eb;border-radius:26px;padding:0 20px;font-size:15px;font-family:inherit;outline:none;width:100%}}
.search-bar:focus{{border-color:#000}}
.section{{padding:40px 0}}
.section-title{{font-size:clamp(24px,3.5vw,32px);font-weight:900;letter-spacing:-.8px;margin-bottom:6px}}
.section-subtitle{{color:#6b7280;font-size:14px;margin-bottom:22px;font-weight:500}}
.filters{{display:flex;gap:10px;overflow-x:auto;margin-bottom:24px;padding-bottom:8px;scrollbar-width:none}}
.filters::-webkit-scrollbar{{height:0}}
.filter-pill{{background:#fff;border:1.5px solid #e5e7eb;color:#6b7280;font-size:13px;font-weight:700;padding:8px 16px;border-radius:20px;cursor:pointer;white-space:nowrap;transition:.2s;font-family:inherit}}
.filter-pill:hover,.filter-pill.active{{background:#000;color:#fff;border-color:#000}}
.deals-grid{{display:grid;grid-template-columns:repeat(auto-fill,minmax(250px,1fr));gap:18px}}
.deal-card{{background:#fff;border:1.5px solid #e5e7eb;border-radius:12px;overflow:hidden;transition:.25s}}
.deal-card:hover{{transform:translateY(-4px);border-color:#000;box-shadow:0 12px 24px rgba(0,0,0,.08)}}
.deal-img-wrap{{position:relative;width:100%;height:230px;background:#f9fafb;overflow:hidden}}
.deal-img{{width:100%;height:100%;object-fit:contain;transition:.3s;padding:8px}}
.deal-card:hover .deal-img{{transform:scale(1.05)}}
.deal-discount{{position:absolute;top:10px;right:10px;background:#ef4444;color:#fff;font-size:11px;font-weight:900;padding:4px 10px;border-radius:20px}}
.deal-body{{padding:14px 16px 16px}}
.deal-store{{color:#6b7280;font-size:11px;font-weight:700;margin-bottom:6px;text-transform:uppercase;letter-spacing:.4px}}
.deal-title{{font-size:14px;font-weight:800;line-height:1.35;margin-bottom:8px;display:-webkit-box;-webkit-line-clamp:2;-webkit-box-orient:vertical;overflow:hidden;min-height:38px}}
.deal-profit{{display:inline-flex;background:#fef3c7;color:#92400e;font-size:10.5px;font-weight:800;padding:3px 8px;border-radius:6px;margin-bottom:10px}}
.deal-price-row{{display:flex;align-items:baseline;gap:10px;margin-bottom:12px}}
.deal-price{{font-size:21px;font-weight:900;letter-spacing:-.4px}}
.deal-mrp{{font-size:13px;color:#9ca3af;text-decoration:line-through;font-weight:600}}
.deal-btn{{display:flex;align-items:center;justify-content:center;width:100%;height:42px;background:#000;color:#fff;text-decoration:none;font-size:13.5px;font-weight:800;border-radius:8px;transition:.2s}}
.deal-btn:hover{{background:#16a34a}}
.tg-banner{{background:#0a0e1a;border-radius:16px;padding:36px 28px;text-align:center;margin:36px 0;color:#fff}}
.tg-banner h3{{font-size:clamp(20px,3vw,28px);font-weight:900;margin-bottom:10px}}
.tg-banner p{{color:#9ca3af;max-width:540px;margin:0 auto 22px;font-size:14px}}
.tg-btn{{display:inline-flex;background:#0088cc;color:#fff;text-decoration:none;font-size:14px;font-weight:800;padding:12px 24px;border-radius:20px}}
footer{{border-top:1px solid #e5e7eb;padding:28px 0;text-align:center;color:#6b7280;font-size:13px;background:#f9fafb}}
#toast{{position:fixed;bottom:84px;left:50%;transform:translateX(-50%) translateY(100px);background:#000;color:#fff;padding:12px 24px;border-radius:20px;font-size:13px;font-weight:800;opacity:0;transition:.3s;z-index:1000;pointer-events:none}}
#toast.show{{transform:translateX(-50%) translateY(0);opacity:1}}
.no-results{{display:none;text-align:center;padding:40px;color:#6b7280;font-weight:700}}
@media(max-width:768px){{.deals-grid{{grid-template-columns:repeat(2,1fr);gap:12px}}.deal-img-wrap{{height:170px}}.deal-title{{font-size:12.5px}}.deal-price{{font-size:17px}}.deal-btn{{height:38px;font-size:12px}}.deal-mrp{{display:none}}.deal-profit{{display:none}}}}
</style>
</head>
<body>
<header><div class="container"><div class="header-inner">
<a href="/" class="brand">⚡ BigRedHub<span class="brand-badge">LIVE</span></a>
<a href="https://t.me/Under99LootDeals_bot" target="_blank" class="header-btn">Telegram Bot</a>
</div></div></header>

<section class="hero"><div class="container">
<div class="hero-pill">● {len(products)} LIVE EARNKARO DEALS SYNCED</div>
<h1 class="hero-title">India's Best Deals.<br>Real Products. Real Prices.</h1>
<p class="hero-subtitle">Direct from EarnKaro — Myntra, Tata CLiQ, Ajio, Amazon & boAt deals with verified pricing. Tap Grab Deal to buy via our affiliate link & support us.</p>
<input type="text" id="searchInput" class="search-bar" placeholder="Search boAt, jeans, watch, headphone...">
</div></section>

<section class="section"><div class="container">
<h2 class="section-title">🔥 All Live Deals</h2>
<p class="section-subtitle">Sorted by biggest discounts in every category</p>
<div class="filters" id="filters">{chips}</div>
<div class="deals-grid" id="dealsGrid">
{cards_html}
</div>
<div class="no-results" id="noResults">😕 No deals found. Try a different search.</div>
</div></section>

<section class="container"><div class="tg-banner">
<h3>Never Miss a 90% Price Drop</h3>
<p>Get instant price glitch alerts & Under ₹99 steals before they sell out.</p>
<a href="https://t.me/Under99LootDeals_bot" target="_blank" class="tg-btn">⚡ Open @Under99LootDeals_bot</a>
</div></section>

<footer><div class="container">© 2026 BigRedHub · Deals sourced live from EarnKaro · Affiliate disclosure: We earn a commission on qualifying purchases.</div></footer>

<div id="toast"></div>
<script>
function filterCat(cat, btn){{
  if(btn){{document.querySelectorAll('.filter-pill').forEach(p=>p.classList.remove('active'));btn.classList.add('active');}}
  let shown=0;
  document.querySelectorAll('.deal-card').forEach(c=>{{
    const ok=(cat==='all'||c.dataset.cat===cat);
    c.style.display=ok?'block':'none'; if(ok)shown++;
  }});
  document.getElementById('noResults').style.display=shown?'none':'block';
}}
document.getElementById('searchInput').addEventListener('input',function(e){{
  const q=e.target.value.toLowerCase().trim();
  let shown=0;
  document.querySelectorAll('.deal-card').forEach(c=>{{
    const ok=!q||c.dataset.q.includes(q);
    c.style.display=ok?'block':'none'; if(ok)shown++;
  }});
  document.getElementById('noResults').style.display=shown?'none':'block';
}});
</script>
</body>
</html>
'''

with open("landing.html", "w", encoding="utf-8") as f:
    f.write(html)

print(f"✅ landing.html rebuilt: {len(products)} real EarnKaro products, direct earnkaro.com links (no shortener)")
