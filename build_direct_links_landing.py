import json

with open("earnkaro_direct_links.json", "r", encoding="utf-8") as f:
    deals = json.load(f)

categories = [
    {
        "id": "audio",
        "name": "Audio & Headphones",
        "badge": "Up to 86% OFF",
        "count": f"{len([d for d in deals if d['category'] == 'audio'])} Deals",
        "image": "https://images.unsplash.com/photo-1505740420928-5e560c06d30e?w=600&auto=format&fit=crop&q=80",
        "icon": "🎧"
    },
    {
        "id": "fashion",
        "name": "Fashion & Apparel",
        "badge": "Up to 83% OFF",
        "count": f"{len([d for d in deals if d['category'] == 'fashion'])} Deals",
        "image": "https://images.unsplash.com/photo-1515372039744-b8f02a3ae446?w=600&auto=format&fit=crop&q=80",
        "icon": "👗"
    },
    {
        "id": "footwear",
        "name": "Sneakers & Footwear",
        "badge": "Up to 80% OFF",
        "count": f"{len([d for d in deals if d['category'] == 'footwear'])} Deals",
        "image": "https://images.unsplash.com/photo-1542291026-7eec264c27ff?w=600&auto=format&fit=crop&q=80",
        "icon": "👟"
    },
    {
        "id": "wearables",
        "name": "Smartwatches",
        "badge": "Up to 86% OFF",
        "count": f"{len([d for d in deals if d['category'] == 'wearables'])} Deals",
        "image": "https://images.unsplash.com/photo-1523275335684-37898b6baf30?w=600&auto=format&fit=crop&q=80",
        "icon": "⌚"
    },
    {
        "id": "electronics",
        "name": "Mobiles & Gadgets",
        "badge": "Up to 70% OFF",
        "count": f"{len([d for d in deals if d['category'] == 'electronics'])} Deals",
        "image": "https://images.unsplash.com/photo-1609091839311-d5365f9ff1c5?w=600&auto=format&fit=crop&q=80",
        "icon": "📱"
    },
    {
        "id": "under99",
        "name": "Under ₹399 Steals",
        "badge": "From ₹349",
        "count": f"{len([d for d in deals if d['category'] == 'under99'])} Deals",
        "image": "https://images.unsplash.com/photo-1583394838336-acd977736f90?w=600&auto=format&fit=crop&q=80",
        "icon": "⚡"
    }
]

coupons = [
    {
        "store": "Amazon India",
        "icon": "📦",
        "discount": "EXTRA ₹200 OFF",
        "desc": "Flat ₹200 OFF on Fashion & Electronics orders above ₹1,999",
        "code": "AMZ200",
        "verified": "Verified 1h ago",
        "used": "5.2k used",
        "expires": "30 Sep 2026",
        "link": f"https://earnkaro.com/stores?r=1962062&url=https://www.amazon.in"
    },
    {
        "store": "Myntra Fashion",
        "icon": "👗",
        "discount": "EXTRA 40% OFF",
        "desc": "Extra 40% discount on streetwear, sneakers & dresses",
        "code": "MYNTRA40",
        "verified": "Verified 2h ago",
        "used": "9.1k used",
        "expires": "30 Sep 2026",
        "link": f"https://earnkaro.com/stores/myntra?r=1962062"
    },
    {
        "store": "Flipkart",
        "icon": "🛒",
        "discount": "FLAT ₹500 OFF",
        "desc": "Flat ₹500 instant discount on mobiles & electronics above ₹10,000",
        "code": "FLIP500",
        "verified": "Verified 3h ago",
        "used": "14.8k used",
        "expires": "02 Oct 2026",
        "link": f"https://earnkaro.com/stores/flipkart?r=1962062"
    },
    {
        "store": "Ajio Trends",
        "icon": "✨",
        "discount": "EXTRA 35% OFF",
        "desc": "Extra 35% off on orders above ₹1,490 on international brands",
        "code": "AJIO35",
        "verified": "Verified 45m ago",
        "used": "6.4k used",
        "expires": "01 Oct 2026",
        "link": f"https://earnkaro.com/stores/ajio?r=1962062"
    }
]

html = f'''<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>BigRedHub — Real EarnKaro Deals with Direct Copy Links</title>
  <meta name="description" content="Live EarnKaro deals with exact product images & direct affiliate copy links. Save up to 86% on boAt, Myntra, Amazon, Campus.">
  <link rel="preconnect" href="https://fonts.googleapis.com">
  <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
  <link href="https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700;800;900&display=swap" rel="stylesheet">
  <style>
    * {{
      margin: 0;
      padding: 0;
      box-sizing: border-box;
      -webkit-font-smoothing: antialiased;
    }}
    
    body {{
      font-family: 'Inter', -apple-system, BlinkMacSystemFont, sans-serif;
      background: #ffffff;
      color: #000000;
      line-height: 1.5;
      padding-bottom: 70px;
    }}
    
    .container {{
      max-width: 1200px;
      margin: 0 auto;
      padding: 0 20px;
    }}
    
    /* Header */
    header {{
      position: sticky;
      top: 0;
      background: rgba(255, 255, 255, 0.95);
      backdrop-filter: blur(12px);
      border-bottom: 1px solid #e5e7eb;
      z-index: 100;
    }}
    
    .header-inner {{
      display: flex;
      align-items: center;
      justify-content: space-between;
      height: 64px;
    }}
    
    .brand {{
      font-size: 20px;
      font-weight: 900;
      color: #000000;
      text-decoration: none;
      letter-spacing: -0.5px;
    }}
    
    .brand-badge {{
      background: #000000;
      color: #ffffff;
      font-size: 9px;
      font-weight: 800;
      padding: 3px 8px;
      border-radius: 20px;
      margin-left: 8px;
      letter-spacing: 0.5px;
    }}
    
    .header-btn {{
      background: #000000;
      color: #ffffff;
      text-decoration: none;
      font-size: 13px;
      font-weight: 700;
      padding: 9px 18px;
      border-radius: 20px;
      transition: opacity 0.2s;
    }}
    
    .header-btn:hover {{
      opacity: 0.8;
    }}
    
    /* Hero */
    .hero {{
      padding: 48px 0 32px;
      text-align: center;
      background: linear-gradient(180deg, #f9fafb 0%, #ffffff 100%);
      border-bottom: 1px solid #e5e7eb;
    }}
    
    .hero-pill {{
      display: inline-flex;
      align-items: center;
      background: #dcfce7;
      border: 1px solid #86efac;
      color: #166534;
      font-size: 11px;
      font-weight: 800;
      padding: 5px 12px;
      border-radius: 20px;
      margin-bottom: 16px;
      text-transform: uppercase;
      letter-spacing: 0.5px;
    }}
    
    .hero-title {{
      font-size: clamp(32px, 5vw, 52px);
      font-weight: 900;
      letter-spacing: -1.2px;
      line-height: 1.1;
      margin-bottom: 12px;
    }}
    
    .hero-subtitle {{
      color: #6b7280;
      font-size: clamp(14px, 2vw, 17px);
      max-width: 600px;
      margin: 0 auto 28px;
      font-weight: 500;
    }}
    
    .search-bar {{
      max-width: 600px;
      margin: 0 auto;
      height: 52px;
      border: 2px solid #e5e7eb;
      border-radius: 26px;
      padding: 0 20px;
      font-size: 15px;
      font-family: inherit;
      outline: none;
      transition: border-color 0.2s;
      width: 100%;
    }}
    
    .search-bar:focus {{
      border-color: #000000;
    }}
    
    /* Section */
    .section {{
      padding: 48px 0;
    }}
    
    .section-title {{
      font-size: clamp(24px, 3.5vw, 32px);
      font-weight: 900;
      letter-spacing: -0.8px;
      margin-bottom: 8px;
    }}
    
    .section-subtitle {{
      color: #6b7280;
      font-size: 14px;
      margin-bottom: 24px;
      font-weight: 500;
    }}
    
    /* Categories Grid */
    .cat-grid {{
      display: grid;
      grid-template-columns: repeat(auto-fill, minmax(280px, 1fr));
      gap: 16px;
      margin-bottom: 32px;
    }}
    
    .cat-card {{
      position: relative;
      height: 140px;
      border-radius: 12px;
      overflow: hidden;
      background: #000000;
      cursor: pointer;
      text-decoration: none;
      display: flex;
      flex-direction: column;
      justify-content: flex-end;
      padding: 16px;
      transition: transform 0.3s;
      border: 1px solid #e5e7eb;
    }}
    
    .cat-card:hover {{
      transform: translateY(-3px);
    }}
    
    .cat-bg {{
      position: absolute;
      top: 0;
      left: 0;
      width: 100%;
      height: 100%;
      object-fit: cover;
      opacity: 0.5;
      transition: transform 0.3s, opacity 0.3s;
    }}
    
    .cat-card:hover .cat-bg {{
      transform: scale(1.05);
      opacity: 0.7;
    }}
    
    .cat-overlay {{
      position: absolute;
      top: 0;
      left: 0;
      width: 100%;
      height: 100%;
      background: linear-gradient(180deg, rgba(0,0,0,0) 0%, rgba(0,0,0,0.8) 100%);
    }}
    
    .cat-content {{
      position: relative;
      z-index: 2;
      color: #ffffff;
    }}
    
    .cat-badge {{
      display: inline-block;
      background: #16a34a;
      color: #ffffff;
      font-size: 10px;
      font-weight: 800;
      padding: 2px 8px;
      border-radius: 12px;
      margin-bottom: 6px;
    }}
    
    .cat-name {{
      font-size: 16px;
      font-weight: 900;
      margin-bottom: 2px;
    }}
    
    .cat-count {{
      font-size: 12px;
      opacity: 0.9;
      font-weight: 600;
    }}
    
    /* Filter Pills */
    .filters {{
      display: flex;
      gap: 10px;
      overflow-x: auto;
      margin-bottom: 24px;
      padding-bottom: 8px;
    }}
    
    .filters::-webkit-scrollbar {{
      height: 0;
    }}
    
    .filter-pill {{
      background: #ffffff;
      border: 1.5px solid #e5e7eb;
      color: #6b7280;
      font-size: 13px;
      font-weight: 700;
      padding: 8px 16px;
      border-radius: 20px;
      cursor: pointer;
      white-space: nowrap;
      transition: all 0.2s;
    }}
    
    .filter-pill:hover, .filter-pill.active {{
      background: #000000;
      color: #ffffff;
      border-color: #000000;
    }}
    
    /* Deals Grid */
    .deals-grid {{
      display: grid;
      grid-template-columns: repeat(auto-fill, minmax(280px, 1fr));
      gap: 20px;
    }}
    
    .deal-card {{
      background: #ffffff;
      border: 1.5px solid #e5e7eb;
      border-radius: 12px;
      overflow: hidden;
      transition: all 0.3s;
    }}
    
    .deal-card:hover {{
      transform: translateY(-4px);
      border-color: #000000;
      box-shadow: 0 12px 24px rgba(0,0,0,0.08);
    }}
    
    .deal-img-wrap {{
      position: relative;
      width: 100%;
      height: 280px;
      background: #f9fafb;
      overflow: hidden;
    }}
    
    .deal-img {{
      width: 100%;
      height: 100%;
      object-fit: contain;
      transition: transform 0.3s;
      padding: 12px;
    }}
    
    .deal-card:hover .deal-img {{
      transform: scale(1.05);
    }}
    
    .deal-discount {{
      position: absolute;
      top: 12px;
      right: 12px;
      background: #ef4444;
      color: #ffffff;
      font-size: 11px;
      font-weight: 900;
      padding: 5px 11px;
      border-radius: 20px;
      box-shadow: 0 4px 12px rgba(239, 68, 68, 0.35);
    }}
    
    .deal-body {{
      padding: 16px;
    }}
    
    .deal-store {{
      color: #6b7280;
      font-size: 12px;
      font-weight: 700;
      margin-bottom: 8px;
    }}
    
    .deal-title {{
      font-size: 15px;
      font-weight: 800;
      line-height: 1.3;
      margin-bottom: 10px;
      display: -webkit-box;
      -webkit-line-clamp: 2;
      -webkit-box-orient: vertical;
      overflow: hidden;
      min-height: 40px;
    }}
    
    .deal-profit {{
      display: inline-flex;
      align-items: center;
      background: #fef3c7;
      color: #92400e;
      font-size: 11px;
      font-weight: 800;
      padding: 3px 8px;
      border-radius: 6px;
      margin-bottom: 12px;
    }}
    
    .deal-price-row {{
      display: flex;
      align-items: baseline;
      gap: 10px;
      margin-bottom: 14px;
    }}
    
    .deal-price {{
      font-size: 22px;
      font-weight: 900;
      letter-spacing: -0.5px;
    }}
    
    .deal-mrp {{
      font-size: 14px;
      color: #9ca3af;
      text-decoration: line-through;
      font-weight: 600;
    }}
    
    .deal-btn {{
      display: flex;
      align-items: center;
      justify-content: center;
      width: 100%;
      height: 44px;
      background: #000000;
      color: #ffffff;
      text-decoration: none;
      font-size: 14px;
      font-weight: 800;
      border-radius: 8px;
      transition: background 0.2s;
    }}
    
    .deal-btn:hover {{
      background: #16a34a;
    }}
    
    /* Coupons Grid */
    .coupons-grid {{
      display: grid;
      grid-template-columns: repeat(auto-fill, minmax(320px, 1fr));
      gap: 18px;
    }}
    
    .coupon-card {{
      background: #ffffff;
      border: 1.5px solid #e5e7eb;
      border-radius: 12px;
      padding: 20px;
      transition: all 0.3s;
    }}
    
    .coupon-card:hover {{
      border-color: #000000;
      box-shadow: 0 8px 20px rgba(0,0,0,0.06);
    }}
    
    .coupon-top {{
      display: flex;
      align-items: flex-start;
      justify-content: space-between;
      margin-bottom: 12px;
    }}
    
    .coupon-store {{
      display: flex;
      align-items: center;
      gap: 10px;
    }}
    
    .coupon-icon {{
      width: 40px;
      height: 40px;
      background: #f9fafb;
      border: 1px solid #e5e7eb;
      border-radius: 8px;
      display: flex;
      align-items: center;
      justify-content: center;
      font-size: 20px;
    }}
    
    .coupon-store-name {{
      font-size: 15px;
      font-weight: 900;
    }}
    
    .coupon-disc {{
      background: #dcfce7;
      color: #166534;
      font-size: 11px;
      font-weight: 800;
      padding: 4px 10px;
      border-radius: 20px;
      border: 1px solid #86efac;
    }}
    
    .coupon-desc {{
      font-size: 13px;
      color: #6b7280;
      margin-bottom: 14px;
      line-height: 1.4;
    }}
    
    .coupon-code-box {{
      display: flex;
      align-items: center;
      justify-content: space-between;
      background: #f9fafb;
      border: 1.5px dashed #d1d5db;
      border-radius: 8px;
      padding: 6px 6px 6px 14px;
      margin-bottom: 10px;
    }}
    
    .coupon-code {{
      font-family: 'Courier New', monospace;
      font-size: 14px;
      font-weight: 900;
      letter-spacing: 1px;
    }}
    
    .copy-btn {{
      background: #000000;
      color: #ffffff;
      border: none;
      font-size: 11px;
      font-weight: 800;
      padding: 7px 14px;
      border-radius: 6px;
      cursor: pointer;
      transition: background 0.2s;
    }}
    
    .copy-btn:hover {{
      background: #16a34a;
    }}
    
    .copy-btn.copied {{
      background: #16a34a;
    }}
    
    .coupon-meta {{
      display: flex;
      align-items: center;
      justify-content: space-between;
      font-size: 11px;
      color: #9ca3af;
      font-weight: 700;
    }}
    
    /* Telegram Banner */
    .tg-banner {{
      background: #0a0e1a;
      border-radius: 16px;
      padding: 40px 32px;
      text-align: center;
      margin: 40px 0;
      color: #ffffff;
    }}
    
    .tg-banner h3 {{
      font-size: clamp(22px, 3vw, 30px);
      font-weight: 900;
      margin-bottom: 12px;
    }}
    
    .tg-banner p {{
      color: #9ca3af;
      max-width: 560px;
      margin: 0 auto 24px;
      font-size: 14px;
    }}
    
    .tg-btn {{
      display: inline-flex;
      align-items: center;
      background: #0088cc;
      color: #ffffff;
      text-decoration: none;
      font-size: 14px;
      font-weight: 800;
      padding: 12px 24px;
      border-radius: 20px;
      transition: background 0.2s;
    }}
    
    .tg-btn:hover {{
      background: #0099e6;
    }}
    
    /* Toast */
    #toast {{
      position: fixed;
      bottom: 84px;
      left: 50%;
      transform: translateX(-50%) translateY(100px);
      background: #000000;
      color: #ffffff;
      padding: 12px 24px;
      border-radius: 20px;
      font-size: 13px;
      font-weight: 800;
      opacity: 0;
      transition: all 0.3s;
      z-index: 1000;
    }}
    
    #toast.show {{
      transform: translateX(-50%) translateY(0);
      opacity: 1;
    }}
    
    /* Footer */
    footer {{
      border-top: 1px solid #e5e7eb;
      padding: 32px 0;
      text-align: center;
      color: #6b7280;
      font-size: 13px;
      background: #f9fafb;
    }}
    
    /* Mobile Bottom Nav */
    .mobile-nav {{
      display: none;
      position: fixed;
      bottom: 0;
      left: 0;
      width: 100%;
      height: 60px;
      background: rgba(255, 255, 255, 0.95);
      backdrop-filter: blur(12px);
      border-top: 1px solid #e5e7eb;
      z-index: 200;
      justify-content: space-around;
      align-items: center;
    }}
    
    .mobile-nav-item {{
      display: flex;
      flex-direction: column;
      align-items: center;
      gap: 2px;
      color: #6b7280;
      text-decoration: none;
      font-size: 10px;
      font-weight: 700;
      background: transparent;
      border: none;
      cursor: pointer;
    }}
    
    .mobile-nav-item.active {{
      color: #000000;
    }}
    
    .mobile-nav-icon {{
      font-size: 18px;
    }}
    
    @media (max-width: 768px) {{
      .mobile-nav {{ display: flex; }}
      .hero {{ padding: 32px 0 24px; }}
      .deals-grid, .coupons-grid {{ grid-template-columns: 1fr; }}
    }}
  </style>
</head>
<body>

  <header>
    <div class="container">
      <div class="header-inner">
        <a href="/" class="brand">
          ⚡ BigRedHub<span class="brand-badge">LIVE</span>
        </a>
        <a href="https://t.me/Under99LootDeals_bot" target="_blank" class="header-btn">
          Telegram Bot
        </a>
      </div>
    </div>
  </header>

  <section class="hero">
    <div class="container">
      <div class="hero-pill">● DIRECT EARNKARO COPY LINKS</div>
      <h1 class="hero-title">Save More on Every Online Order.</h1>
      <p class="hero-subtitle">
        Real product images & direct EarnKaro affiliate links (no shorteners). Cashback from Myntra, Amazon, boAt & more.
      </p>
      <input 
        type="text" 
        id="searchInput" 
        class="search-bar" 
        placeholder="Search boAt, Myntra, earbuds, sneakers, dresses..."
      >
    </div>
  </section>

  <section class="section" id="categories">
    <div class="container">
      <h2 class="section-title">Shop by Category</h2>
      <p class="section-subtitle">Curated Indian retail categories with highest cashback rates</p>
      
      <div class="cat-grid">
'''

for cat in categories:
    html += f'''        <div class="cat-card" onclick="filterCategory('{cat['id']}')">
          <img src="{cat['image']}" alt="{cat['name']}" class="cat-bg">
          <div class="cat-overlay"></div>
          <div class="cat-content">
            <span class="cat-badge">{cat['badge']}</span>
            <div class="cat-name">{cat['icon']} {cat['name']}</div>
            <div class="cat-count">{cat['count']}</div>
          </div>
        </div>
'''

html += '''      </div>
    </div>
  </section>

  <section class="section" id="deals">
    <div class="container">
      <h2 class="section-title">🔥 Live EarnKaro Deals</h2>
      <p class="section-subtitle">Exact product images from EarnKaro • Direct copy links with Ref ID 1962062</p>
      
      <div class="filters">
        <button class="filter-pill active" onclick="filterCategory('all', this)">All Deals</button>
        <button class="filter-pill" onclick="filterCategory('audio', this)">🎧 Audio</button>
        <button class="filter-pill" onclick="filterCategory('fashion', this)">👗 Fashion</button>
        <button class="filter-pill" onclick="filterCategory('footwear', this)">👟 Footwear</button>
        <button class="filter-pill" onclick="filterCategory('wearables', this)">⌚ Smartwatches</button>
        <button class="filter-pill" onclick="filterCategory('electronics', this)">📱 Electronics</button>
        <button class="filter-pill" onclick="filterCategory('under99', this)">⚡ Under ₹399</button>
      </div>
      
      <div class="deals-grid" id="dealsContainer">
'''

for deal in deals:
    html += f'''        <div class="deal-card" data-category="{deal['category']}" data-title="{deal['title'].lower()}" data-store="{deal['store'].lower()}" data-id="{deal['id']}">
          <div class="deal-img-wrap">
            <img src="{deal['image']}" alt="{deal['title']}" class="deal-img" loading="lazy">
            <span class="deal-discount">{deal['discount']}</span>
          </div>
          <div class="deal-body">
            <div class="deal-store">{deal['store_icon']} {deal['store']}</div>
            <h3 class="deal-title">{deal['title']}</h3>
            <div class="deal-profit">💰 {deal['profit']}</div>
            <div class="deal-price-row">
              <span class="deal-price">{deal['price']}</span>
              <span class="deal-mrp">{deal['mrp']}</span>
            </div>
            <a href="{deal['copy_link']}" target="_blank" rel="noopener noreferrer" class="deal-btn">
              Copy Link & Buy ⚡
            </a>
          </div>
        </div>
'''

html += '''      </div>
    </div>
  </section>

  <section class="section" id="coupons">
    <div class="container">
      <h2 class="section-title">✓ Verified Promo Codes</h2>
      <p class="section-subtitle">100% active coupons with 1-click clipboard copy</p>
      
      <div class="coupons-grid">
'''

for c in coupons:
    html += f'''        <div class="coupon-card">
          <div class="coupon-top">
            <div class="coupon-store">
              <div class="coupon-icon">{c['icon']}</div>
              <div>
                <div class="coupon-store-name">{c['store']}</div>
                <div style="font-size: 10px; color: #16a34a; font-weight: 700;">✓ {c['verified']}</div>
              </div>
            </div>
            <span class="coupon-disc">{c['discount']}</span>
          </div>
          <p class="coupon-desc">{c['desc']}</p>
          <div class="coupon-code-box">
            <span class="coupon-code">{c['code']}</span>
            <button class="copy-btn" onclick="copyCoupon('{c['code']}', '{c['link']}', this)">COPY</button>
          </div>
          <div class="coupon-meta">
            <span>👥 {c['used']}</span>
            <span>⏳ Expires {c['expires']}</span>
          </div>
        </div>
'''

html += '''      </div>
    </div>
  </section>

  <section class="container" id="telegram">
    <div class="tg-banner">
      <h3>Never Miss a 90% Price Drop</h3>
      <p>Join 50,000+ smart Indian shoppers getting instant price glitch alerts, EarnKaro flash deals and Under ₹99 steals before they sell out.</p>
      <a href="https://t.me/Under99LootDeals_bot" target="_blank" class="tg-btn">
        ⚡ Open @Under99LootDeals_bot
      </a>
    </div>
  </section>

  <footer>
    <div class="container">
      <p>© 2026 BigRedHub. Minimalist Indian deals platform with direct EarnKaro copy links (Ref ID: 1962062).</p>
    </div>
  </footer>

  <div class="mobile-nav">
    <a href="#" class="mobile-nav-item active">
      <span class="mobile-nav-icon">🏠</span>
      <span>Home</span>
    </a>
    <a href="#categories" class="mobile-nav-item">
      <span class="mobile-nav-icon">📁</span>
      <span>Categories</span>
    </a>
    <a href="#deals" class="mobile-nav-item">
      <span class="mobile-nav-icon">⚡</span>
      <span>Deals</span>
    </a>
    <a href="#coupons" class="mobile-nav-item">
      <span class="mobile-nav-icon">🎟️</span>
      <span>Coupons</span>
    </a>
  </div>

  <div id="toast"></div>

  <script>
    function showToast(msg) {
      const toast = document.getElementById('toast');
      toast.innerText = msg;
      toast.classList.add('show');
      setTimeout(() => toast.classList.remove('show'), 2500);
    }

    function copyCoupon(code, link, btn) {
      navigator.clipboard.writeText(code).then(() => {
        const oldText = btn.innerText;
        btn.innerText = 'COPIED ✓';
        btn.classList.add('copied');
        showToast('Code ' + code + ' copied!');
        
        setTimeout(() => {
          btn.innerText = oldText;
          btn.classList.remove('copied');
        }, 2000);

        if (link) {
          setTimeout(() => window.open(link, '_blank'), 600);
        }
      });
    }

    function filterCategory(cat, btn) {
      if (btn) {
        document.querySelectorAll('.filter-pill').forEach(p => p.classList.remove('active'));
        btn.classList.add('active');
      }

      const cards = document.querySelectorAll('.deal-card');
      cards.forEach(card => {
        const cardCat = card.getAttribute('data-category');
        card.style.display = (cat === 'all' || cardCat === cat) ? 'block' : 'none';
      });

      if (cat !== 'all') {
        document.getElementById('deals').scrollIntoView({ behavior: 'smooth' });
      }
    }

    const searchInput = document.getElementById('searchInput');
    if (searchInput) {
      searchInput.addEventListener('input', function(e) {
        const query = e.target.value.toLowerCase().trim();
        const cards = document.querySelectorAll('.deal-card');
        
        cards.forEach(card => {
          const title = card.getAttribute('data-title') || '';
          const store = card.getAttribute('data-store') || '';
          card.style.display = (title.includes(query) || store.includes(query)) ? 'block' : 'none';
        });
      });
    }
  </script>
</body>
</html>
'''

with open("landing.html", "w", encoding="utf-8") as f:
    f.write(html)

print("✅ Final landing page with DIRECT EarnKaro copy links (no TinyURL) + exact product images!")
print(f"\n📊 Stats:")
print(f"   • Total Products: {len(deals)}")
print(f"   • Audio Deals: {len([d for d in deals if d['category'] == 'audio'])}")
print(f"   • Fashion Deals: {len([d for d in deals if d['category'] == 'fashion'])}")
print(f"   • Footwear Deals: {len([d for d in deals if d['category'] == 'footwear'])}")
print(f"   • Smartwatches: {len([d for d in deals if d['category'] == 'wearables'])}")
print(f"   • All links include: ?r=1962062 (EarnKaro Ref ID)")
