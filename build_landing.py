import json

with open("earnkaro_catalog.json", "r", encoding="utf-8") as f:
    catalog = json.load(f)

categories = catalog["categories"]
deals = catalog["deals"]

coupons = [
    {
        "id": "c1",
        "store": "Amazon India",
        "icon": "📦",
        "discount": "₹200 OFF",
        "desc": "Flat ₹200 OFF on Fashion & Lifestyle orders above ₹1,999",
        "code": "AMZ200",
        "verified": "Verified 2h ago",
        "used": "4.8k used",
        "expires": "30 Sep 2026",
        "link": "https://tinyurl.com/22ckzdaw"
    },
    {
        "id": "c2",
        "store": "Myntra Fashion",
        "icon": "👗",
        "discount": "EXTRA 40% OFF",
        "desc": "Extra 40% discount on top streetwear, sneakers & hoodies",
        "code": "MYNTRA40",
        "verified": "Verified 1h ago",
        "used": "8.2k used",
        "expires": "30 Sep 2026",
        "link": "https://tinyurl.com/2yt3xfz9"
    },
    {
        "id": "c3",
        "store": "Flipkart Big Billion",
        "icon": "🛍️",
        "discount": "FLAT ₹500 OFF",
        "desc": "Flat ₹500 instant discount on electronics & smart home devices",
        "code": "FLIP500",
        "verified": "Verified 45m ago",
        "used": "12.4k used",
        "expires": "02 Oct 2026",
        "link": "https://tinyurl.com/29ao7vn3"
    },
    {
        "id": "c4",
        "store": "boAt Lifestyle",
        "icon": "🎧",
        "discount": "FLAT ₹200 OFF",
        "desc": "Flat ₹200 extra discount on Airdopes & Smartwatches",
        "code": "BOAT200",
        "verified": "Verified 3h ago",
        "used": "3.1k used",
        "expires": "05 Oct 2026",
        "link": "https://tinyurl.com/2yv7onun"
    },
    {
        "id": "c5",
        "store": "Ajio Trends",
        "icon": "✨",
        "discount": "EXTRA 35% OFF",
        "desc": "Extra 35% off on orders above ₹1,490 on international brands",
        "code": "AJIO35",
        "verified": "Verified 2h ago",
        "used": "5.7k used",
        "expires": "01 Oct 2026",
        "link": "https://tinyurl.com/27866z3r"
    },
    {
        "id": "c6",
        "store": "Nykaa Beauty",
        "icon": "💄",
        "discount": "EXTRA 30% OFF",
        "desc": "Extra 30% off on premium perfumes, grooming & makeup",
        "code": "NYKAA30",
        "verified": "Verified 4h ago",
        "used": "2.9k used",
        "expires": "30 Sep 2026",
        "link": "https://tinyurl.com/2449ucyf"
    }
]

html_template = f"""<!DOCTYPE html>
<html lang="en" class="scroll-smooth">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0, maximum-scale=5.0">
  
  <!-- Primary Meta Tags -->
  <title>BigRedHub — Verified Indian Deals & Coupons | Up to 90% OFF</title>
  <meta name="title" content="BigRedHub — Verified Indian Deals & Coupons | Up to 90% OFF">
  <meta name="description" content="Discover verified EarnKaro loot deals, promo codes, under ₹99 steals and cashback from Amazon, Flipkart, Myntra, Ajio & boAt. Minimalist, fast, trusted.">
  <meta name="keywords" content="earnkaro deals, loot deals, under 99 deals, amazon coupons, flipkart offers, myntra promo code, bigredhub">
  <meta name="theme-color" content="#08080c">
  <link rel="canonical" href="https://bigredhub.info">

  <!-- Open Graph / Facebook -->
  <meta property="og:type" content="website">
  <meta property="og:url" content="https://bigredhub.info">
  <meta property="og:title" content="BigRedHub — Verified Indian Deals & Coupons">
  <meta property="og:description" content="Save up to 90% with verified promo codes & EarnKaro loot deals on Amazon, Flipkart, Myntra.">
  <meta property="og:image" content="https://images.unsplash.com/photo-1607082349566-187342175e2f?w=1200&q=80">

  <!-- Fonts: Apple SF Pro / Plus Jakarta Sans -->
  <link rel="preconnect" href="https://fonts.googleapis.com">
  <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
  <link href="https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:wght@400;500;600;700;800;900&display=swap" rel="stylesheet">

  <style>
    /* -------------------------------------------------------------
       APPLE / NIKE PRO MINIMALIST DESIGN SYSTEM
       Ultra-dark obsidian base, frosted glass, high-contrast neon accents
       ------------------------------------------------------------- */
    :root {{
      --bg-base: #08080c;
      --bg-surface: #111117;
      --bg-surface-elevated: #181822;
      --bg-glass: rgba(255, 255, 255, 0.035);
      --bg-glass-hover: rgba(255, 255, 255, 0.065);
      
      --border-subtle: rgba(255, 255, 255, 0.08);
      --border-focus: rgba(255, 255, 255, 0.22);
      --border-accent: rgba(0, 223, 129, 0.4);
      
      --accent-green: #00df81;
      --accent-green-glow: rgba(0, 223, 129, 0.25);
      --accent-orange: #ff4500;
      --accent-blue: #0a84ff;
      --accent-badge: #ff334b;
      
      --text-primary: #ffffff;
      --text-secondary: #a1a1aa;
      --text-muted: #71717a;
      
      --radius-sm: 8px;
      --radius-md: 14px;
      --radius-lg: 20px;
      --radius-full: 9999px;
      
      --transition-fast: 0.18s cubic-bezier(0.16, 1, 0.3, 1);
      --transition-smooth: 0.28s cubic-bezier(0.16, 1, 0.3, 1);
    }}

    * {{
      margin: 0;
      padding: 0;
      box-sizing: border-box;
      -webkit-font-smoothing: antialiased;
      -moz-osx-font-smoothing: grayscale;
    }}

    body {{
      font-family: 'Plus Jakarta Sans', -apple-system, BlinkMacSystemFont, sans-serif;
      background-color: var(--bg-base);
      color: var(--text-primary);
      line-height: 1.5;
      overflow-x: hidden;
      padding-bottom: 70px;
    }}

    /* Ambient Spotlight Background */
    .ambient-glow {{
      position: fixed;
      top: 0;
      left: 50%;
      transform: translateX(-50%);
      width: 100vw;
      max-width: 1200px;
      height: 480px;
      background: radial-gradient(circle at 50% 0%, rgba(0, 223, 129, 0.08) 0%, rgba(10, 132, 255, 0.04) 45%, transparent 75%);
      pointer-events: none;
      z-index: 0;
    }}

    .container {{
      max-width: 1240px;
      margin: 0 auto;
      padding: 0 20px;
      position: relative;
      z-index: 1;
    }}

    /* -------------------------------------------------------------
       HEADER / NAV
       ------------------------------------------------------------- */
    header {{
      position: sticky;
      top: 0;
      background: rgba(8, 8, 12, 0.85);
      backdrop-filter: blur(16px);
      -webkit-backdrop-filter: blur(16px);
      border-bottom: 1px solid var(--border-subtle);
      z-index: 100;
      transition: border-color var(--transition-fast);
    }}

    .header-inner {{
      display: flex;
      align-items: center;
      justify-content: space-between;
      height: 68px;
    }}

    .brand-logo {{
      display: flex;
      align-items: center;
      gap: 10px;
      text-decoration: none;
      color: var(--text-primary);
      font-weight: 900;
      font-size: 21px;
      letter-spacing: -0.5px;
    }}

    .logo-badge {{
      background: linear-gradient(135deg, #ff334b, #ff5722);
      color: #fff;
      font-size: 10px;
      font-weight: 800;
      padding: 2px 7px;
      border-radius: var(--radius-full);
      text-transform: uppercase;
      letter-spacing: 0.8px;
    }}

    .nav-links {{
      display: flex;
      align-items: center;
      gap: 28px;
    }}

    .nav-links a {{
      color: var(--text-secondary);
      text-decoration: none;
      font-size: 14px;
      font-weight: 600;
      transition: color var(--transition-fast);
    }}

    .nav-links a:hover, .nav-links a.active {{
      color: var(--text-primary);
    }}

    .header-actions {{
      display: flex;
      align-items: center;
      gap: 12px;
    }}

    .fav-btn-header {{
      background: var(--bg-glass);
      border: 1px solid var(--border-subtle);
      color: var(--text-primary);
      padding: 8px 14px;
      border-radius: var(--radius-full);
      font-size: 13px;
      font-weight: 600;
      display: flex;
      align-items: center;
      gap: 6px;
      cursor: pointer;
      transition: all var(--transition-fast);
    }}

    .fav-btn-header:hover {{
      background: var(--bg-glass-hover);
      border-color: var(--border-focus);
    }}

    .tg-header-btn {{
      background: #0088cc;
      color: #fff;
      text-decoration: none;
      font-size: 13px;
      font-weight: 700;
      padding: 9px 18px;
      border-radius: var(--radius-full);
      display: flex;
      align-items: center;
      gap: 6px;
      transition: transform var(--transition-fast), background var(--transition-fast);
    }}

    .tg-header-btn:hover {{
      background: #0099e6;
      transform: translateY(-1px);
    }}

    /* -------------------------------------------------------------
       HERO SECTION (Apple/Nike Restrained Simplicity)
       ------------------------------------------------------------- */
    .hero {{
      padding: 56px 0 36px;
      text-align: center;
    }}

    .hero-pill {{
      display: inline-flex;
      align-items: center;
      gap: 8px;
      background: rgba(0, 223, 129, 0.08);
      border: 1px solid rgba(0, 223, 129, 0.25);
      color: var(--accent-green);
      font-size: 12px;
      font-weight: 700;
      text-transform: uppercase;
      letter-spacing: 1px;
      padding: 6px 14px;
      border-radius: var(--radius-full);
      margin-bottom: 20px;
    }}

    .hero-title {{
      font-size: clamp(34px, 5.2vw, 58px);
      font-weight: 900;
      letter-spacing: -1.5px;
      line-height: 1.08;
      max-width: 820px;
      margin: 0 auto 16px;
    }}

    .hero-title .gradient-text {{
      background: linear-gradient(135deg, #ffffff 40%, #a1a1aa 100%);
      -webkit-background-clip: text;
      -webkit-text-fill-color: transparent;
    }}

    .hero-subtitle {{
      color: var(--text-secondary);
      font-size: clamp(15px, 2vw, 18px);
      max-width: 620px;
      margin: 0 auto 32px;
      font-weight: 500;
    }}

    /* Minimalist Search Bar */
    .search-wrapper {{
      max-width: 640px;
      margin: 0 auto 20px;
      position: relative;
    }}

    .search-bar {{
      width: 100%;
      height: 56px;
      background: var(--bg-surface);
      border: 1px solid var(--border-subtle);
      border-radius: var(--radius-full);
      padding: 0 54px 0 52px;
      color: #fff;
      font-size: 16px;
      font-family: inherit;
      outline: none;
      transition: all var(--transition-fast);
      box-shadow: 0 8px 32px rgba(0, 0, 0, 0.4);
    }}

    .search-bar:focus {{
      border-color: var(--accent-green);
      box-shadow: 0 0 0 3px var(--accent-green-glow), 0 8px 32px rgba(0, 0, 0, 0.6);
      background: var(--bg-surface-elevated);
    }}

    .search-icon-left {{
      position: absolute;
      left: 20px;
      top: 50%;
      transform: translateY(-50%);
      color: var(--text-muted);
      font-size: 18px;
      pointer-events: none;
    }}

    .search-clear-btn {{
      position: absolute;
      right: 18px;
      top: 50%;
      transform: translateY(-50%);
      background: transparent;
      border: none;
      color: var(--text-muted);
      cursor: pointer;
      font-size: 16px;
      display: none;
      padding: 4px;
    }}

    .popular-searches {{
      display: flex;
      align-items: center;
      justify-content: center;
      flex-wrap: wrap;
      gap: 8px;
    }}

    .popular-label {{
      color: var(--text-muted);
      font-size: 12px;
      font-weight: 600;
      text-transform: uppercase;
      letter-spacing: 0.5px;
    }}

    .search-chip {{
      background: var(--bg-glass);
      border: 1px solid var(--border-subtle);
      color: var(--text-secondary);
      text-decoration: none;
      font-size: 12px;
      font-weight: 600;
      padding: 5px 12px;
      border-radius: var(--radius-full);
      transition: all var(--transition-fast);
    }}

    .search-chip:hover {{
      color: var(--text-primary);
      border-color: var(--border-focus);
      background: var(--bg-glass-hover);
    }}

    /* -------------------------------------------------------------
       CATEGORIES SECTION (Clean Image Grid)
       ------------------------------------------------------------- */
    .section-block {{
      padding: 48px 0;
    }}

    .section-head {{
      display: flex;
      align-items: flex-end;
      justify-content: space-between;
      margin-bottom: 24px;
    }}

    .section-title {{
      font-size: clamp(22px, 3.5vw, 30px);
      font-weight: 800;
      letter-spacing: -0.8px;
    }}

    .section-subtitle {{
      color: var(--text-secondary);
      font-size: 14px;
      margin-top: 4px;
    }}

    .categories-grid {{
      display: grid;
      grid-template-columns: repeat(4, 1fr);
      gap: 16px;
    }}

    .category-card {{
      position: relative;
      border-radius: var(--radius-md);
      overflow: hidden;
      height: 140px;
      background: var(--bg-surface);
      border: 1px solid var(--border-subtle);
      cursor: pointer;
      text-decoration: none;
      color: #fff;
      display: flex;
      flex-direction: column;
      justify-content: flex-end;
      padding: 16px;
      transition: all var(--transition-smooth);
    }}

    .category-card:hover {{
      transform: translateY(-3px);
      border-color: var(--border-focus);
      box-shadow: 0 12px 30px rgba(0,0,0,0.5);
    }}

    .category-bg-img {{
      position: absolute;
      top: 0;
      left: 0;
      width: 100%;
      height: 100%;
      object-fit: cover;
      opacity: 0.38;
      transition: transform var(--transition-smooth), opacity var(--transition-smooth);
    }}

    .category-card:hover .category-bg-img {{
      transform: scale(1.06);
      opacity: 0.5;
    }}

    .category-overlay {{
      position: absolute;
      top: 0;
      left: 0;
      width: 100%;
      height: 100%;
      background: linear-gradient(180deg, rgba(8,8,12,0.1) 0%, rgba(8,8,12,0.88) 90%);
    }}

    .category-content {{
      position: relative;
      z-index: 2;
    }}

    .category-badge-chip {{
      display: inline-block;
      background: rgba(0, 223, 129, 0.15);
      color: var(--accent-green);
      font-size: 10px;
      font-weight: 800;
      padding: 2px 8px;
      border-radius: var(--radius-full);
      margin-bottom: 6px;
      border: 1px solid rgba(0, 223, 129, 0.3);
      text-transform: uppercase;
    }}

    .category-name {{
      font-size: 16px;
      font-weight: 800;
      letter-spacing: -0.3px;
    }}

    .category-count {{
      font-size: 12px;
      color: var(--text-secondary);
    }}

    /* -------------------------------------------------------------
       FILTER BAR & TABS
       ------------------------------------------------------------- */
    .filter-sticky-wrap {{
      display: flex;
      align-items: center;
      gap: 10px;
      overflow-x: auto;
      padding: 12px 0 20px;
      margin-bottom: 12px;
      scrollbar-width: none;
    }}
    .filter-sticky-wrap::-webkit-scrollbar {{ display: none; }}

    .filter-pill {{
      background: var(--bg-surface);
      border: 1px solid var(--border-subtle);
      color: var(--text-secondary);
      font-size: 13px;
      font-weight: 700;
      padding: 9px 18px;
      border-radius: var(--radius-full);
      cursor: pointer;
      white-space: nowrap;
      transition: all var(--transition-fast);
      display: inline-flex;
      align-items: center;
      gap: 6px;
    }}

    .filter-pill:hover {{
      color: var(--text-primary);
      border-color: var(--border-focus);
    }}

    .filter-pill.active {{
      background: #ffffff;
      color: #000000;
      border-color: #ffffff;
      font-weight: 800;
    }}

    /* -------------------------------------------------------------
       DEALS GRID (Nike/Apple Style Clean High-Impact Cards)
       ------------------------------------------------------------- */
    .deals-grid {{
      display: grid;
      grid-template-columns: repeat(auto-fill, minmax(280px, 1fr));
      gap: 20px;
    }}

    .deal-card {{
      background: var(--bg-surface);
      border: 1px solid var(--border-subtle);
      border-radius: var(--radius-md);
      overflow: hidden;
      display: flex;
      flex-direction: column;
      transition: all var(--transition-smooth);
      position: relative;
    }}

    .deal-card:hover {{
      transform: translateY(-4px);
      border-color: var(--border-focus);
      box-shadow: 0 16px 40px rgba(0, 0, 0, 0.6);
    }}

    .card-img-wrap {{
      position: relative;
      width: 100%;
      height: 220px;
      background: #000000;
      overflow: hidden;
    }}

    .card-product-img {{
      width: 100%;
      height: 100%;
      object-fit: cover;
      transition: transform var(--transition-smooth);
      background-color: #1a1a24;
    }}

    .deal-card:hover .card-product-img {{
      transform: scale(1.05);
    }}

    .card-tag-pill {{
      position: absolute;
      top: 12px;
      left: 12px;
      background: rgba(0, 0, 0, 0.75);
      backdrop-filter: blur(8px);
      border: 1px solid rgba(255, 255, 255, 0.15);
      color: #fff;
      font-size: 11px;
      font-weight: 800;
      padding: 4px 10px;
      border-radius: var(--radius-full);
      letter-spacing: 0.5px;
    }}

    .card-discount-badge {{
      position: absolute;
      top: 12px;
      right: 12px;
      background: var(--accent-badge);
      color: #fff;
      font-size: 12px;
      font-weight: 900;
      padding: 4px 10px;
      border-radius: var(--radius-full);
      letter-spacing: 0.5px;
      box-shadow: 0 4px 12px rgba(255, 51, 75, 0.4);
    }}

    .card-fav-btn {{
      position: absolute;
      bottom: 12px;
      right: 12px;
      width: 36px;
      height: 36px;
      border-radius: var(--radius-full);
      background: rgba(0, 0, 0, 0.7);
      backdrop-filter: blur(8px);
      border: 1px solid rgba(255, 255, 255, 0.15);
      color: #fff;
      display: flex;
      align-items: center;
      justify-content: center;
      cursor: pointer;
      font-size: 16px;
      transition: transform var(--transition-fast), background var(--transition-fast);
      z-index: 2;
    }}

    .card-fav-btn:hover {{
      transform: scale(1.1);
      background: rgba(255, 51, 75, 0.9);
      border-color: transparent;
    }}

    .card-body {{
      padding: 18px;
      display: flex;
      flex-direction: column;
      flex-grow: 1;
    }}

    .card-store-row {{
      display: flex;
      align-items: center;
      justify-content: space-between;
      margin-bottom: 8px;
    }}

    .store-label {{
      display: inline-flex;
      align-items: center;
      gap: 6px;
      font-size: 12px;
      color: var(--text-secondary);
      font-weight: 600;
    }}

    .verified-micro {{
      color: var(--accent-green);
      font-size: 11px;
      font-weight: 700;
      display: flex;
      align-items: center;
      gap: 3px;
    }}

    .deal-card-title {{
      font-size: 15px;
      font-weight: 700;
      line-height: 1.35;
      color: var(--text-primary);
      margin-bottom: 14px;
      display: -webkit-box;
      -webkit-line-clamp: 2;
      -webkit-box-orient: vertical;
      overflow: hidden;
      min-height: 40px;
    }}

    .card-price-row {{
      display: flex;
      align-items: baseline;
      gap: 10px;
      margin-top: auto;
      margin-bottom: 16px;
    }}

    .price-loot {{
      font-size: 24px;
      font-weight: 900;
      color: var(--accent-green);
      letter-spacing: -0.5px;
    }}

    .price-mrp {{
      font-size: 14px;
      color: var(--text-muted);
      text-decoration: line-through;
      font-weight: 600;
    }}

    .buy-btn-primary {{
      display: flex;
      align-items: center;
      justify-content: center;
      gap: 8px;
      width: 100%;
      height: 46px;
      background: #ffffff;
      color: #000000;
      text-decoration: none;
      font-size: 14px;
      font-weight: 800;
      border-radius: var(--radius-sm);
      transition: all var(--transition-fast);
    }}

    .buy-btn-primary:hover {{
      background: var(--accent-green);
      color: #000000;
      box-shadow: 0 4px 20px var(--accent-green-glow);
    }}

    /* -------------------------------------------------------------
       COUPONS SECTION
       ------------------------------------------------------------- */
    .coupons-grid {{
      display: grid;
      grid-template-columns: repeat(auto-fill, minmax(340px, 1fr));
      gap: 18px;
    }}

    .coupon-card {{
      background: var(--bg-surface);
      border: 1px solid var(--border-subtle);
      border-radius: var(--radius-md);
      padding: 20px;
      display: flex;
      flex-direction: column;
      justify-content: space-between;
      transition: all var(--transition-smooth);
    }}

    .coupon-card:hover {{
      border-color: var(--border-focus);
      transform: translateY(-2px);
    }}

    .coupon-top {{
      display: flex;
      align-items: flex-start;
      justify-content: space-between;
      margin-bottom: 12px;
    }}

    .coupon-store-info {{
      display: flex;
      align-items: center;
      gap: 10px;
    }}

    .store-icon-box {{
      width: 44px;
      height: 44px;
      background: var(--bg-surface-elevated);
      border: 1px solid var(--border-subtle);
      border-radius: var(--radius-sm);
      display: flex;
      align-items: center;
      justify-content: center;
      font-size: 22px;
    }}

    .coupon-store-name {{
      font-size: 16px;
      font-weight: 800;
    }}

    .coupon-disc-tag {{
      background: rgba(0, 223, 129, 0.12);
      color: var(--accent-green);
      font-size: 12px;
      font-weight: 800;
      padding: 4px 10px;
      border-radius: var(--radius-full);
      border: 1px solid rgba(0, 223, 129, 0.3);
    }}

    .coupon-desc-text {{
      font-size: 14px;
      color: var(--text-secondary);
      margin-bottom: 16px;
      line-height: 1.4;
    }}

    .coupon-code-box {{
      display: flex;
      align-items: center;
      justify-content: space-between;
      background: var(--bg-base);
      border: 1px dashed var(--border-focus);
      border-radius: var(--radius-sm);
      padding: 6px 6px 6px 14px;
      margin-bottom: 12px;
    }}

    .code-string {{
      font-family: 'SF Mono', Monaco, Consolas, monospace;
      font-size: 15px;
      font-weight: 800;
      letter-spacing: 1.5px;
      color: var(--accent-green);
    }}

    .copy-btn-action {{
      background: var(--bg-surface-elevated);
      border: 1px solid var(--border-subtle);
      color: #fff;
      font-size: 12px;
      font-weight: 800;
      padding: 8px 16px;
      border-radius: 6px;
      cursor: pointer;
      transition: all var(--transition-fast);
    }}

    .copy-btn-action:hover {{
      background: #fff;
      color: #000;
    }}

    .copy-btn-action.copied {{
      background: var(--accent-green);
      color: #000;
      border-color: var(--accent-green);
    }}

    .coupon-footer-meta {{
      display: flex;
      align-items: center;
      justify-content: space-between;
      font-size: 11px;
      color: var(--text-muted);
      font-weight: 600;
    }}

    /* -------------------------------------------------------------
       TELEGRAM BANNER (Ultra-Clean Dark CTA)
       ------------------------------------------------------------- */
    .tg-banner {{
      background: linear-gradient(135deg, #0f172a 0%, #090d16 100%);
      border: 1px solid rgba(0, 136, 204, 0.3);
      border-radius: var(--radius-lg);
      padding: 40px 32px;
      text-align: center;
      margin: 40px 0;
      position: relative;
      overflow: hidden;
    }}

    .tg-banner h3 {{
      font-size: clamp(22px, 3.5vw, 32px);
      font-weight: 900;
      margin-bottom: 12px;
    }}

    .tg-banner p {{
      color: var(--text-secondary);
      max-width: 580px;
      margin: 0 auto 24px;
      font-size: 15px;
    }}

    .tg-actions-row {{
      display: flex;
      align-items: center;
      justify-content: center;
      gap: 16px;
      flex-wrap: wrap;
    }}

    .tg-big-btn {{
      background: #0088cc;
      color: #fff;
      text-decoration: none;
      font-size: 15px;
      font-weight: 800;
      padding: 14px 28px;
      border-radius: var(--radius-full);
      display: inline-flex;
      align-items: center;
      gap: 8px;
      transition: all var(--transition-fast);
      box-shadow: 0 8px 24px rgba(0, 136, 204, 0.4);
    }}

    .tg-big-btn:hover {{
      background: #0099e6;
      transform: translateY(-2px);
    }}

    .tg-secondary-btn {{
      background: var(--bg-surface-elevated);
      border: 1px solid var(--border-subtle);
      color: #fff;
      text-decoration: none;
      font-size: 14px;
      font-weight: 700;
      padding: 13px 24px;
      border-radius: var(--radius-full);
      transition: all var(--transition-fast);
    }}

    .tg-secondary-btn:hover {{
      border-color: var(--border-focus);
      background: var(--bg-glass-hover);
    }}

    /* -------------------------------------------------------------
       TOAST NOTIFICATION
       ------------------------------------------------------------- */
    #toast {{
      position: fixed;
      bottom: 84px;
      left: 50%;
      transform: translateX(-50%) translateY(100px);
      background: rgba(17, 17, 23, 0.95);
      border: 1px solid var(--accent-green);
      color: #fff;
      padding: 12px 24px;
      border-radius: var(--radius-full);
      font-size: 14px;
      font-weight: 700;
      display: flex;
      align-items: center;
      gap: 10px;
      backdrop-filter: blur(12px);
      box-shadow: 0 12px 32px rgba(0, 0, 0, 0.6);
      opacity: 0;
      transition: all 0.3s cubic-bezier(0.16, 1, 0.3, 1);
      z-index: 1000;
      pointer-events: none;
    }}

    #toast.show {{
      transform: translateX(-50%) translateY(0);
      opacity: 1;
    }}

    /* -------------------------------------------------------------
       MOBILE BOTTOM NAVIGATION
       ------------------------------------------------------------- */
    .mobile-bottom-nav {{
      display: none;
      position: fixed;
      bottom: 0;
      left: 0;
      width: 100%;
      height: 64px;
      background: rgba(8, 8, 12, 0.92);
      backdrop-filter: blur(16px);
      -webkit-backdrop-filter: blur(16px);
      border-top: 1px solid var(--border-subtle);
      z-index: 200;
      justify-content: space-around;
      align-items: center;
    }}

    .bottom-nav-item {{
      display: flex;
      flex-direction: column;
      align-items: center;
      gap: 3px;
      color: var(--text-muted);
      text-decoration: none;
      font-size: 11px;
      font-weight: 700;
      transition: color var(--transition-fast);
      background: transparent;
      border: none;
      cursor: pointer;
    }}

    .bottom-nav-item.active, .bottom-nav-item:hover {{
      color: #fff;
    }}

    .bottom-nav-icon {{
      font-size: 18px;
    }}

    /* -------------------------------------------------------------
       FOOTER
       ------------------------------------------------------------- */
    footer {{
      border-top: 1px solid var(--border-subtle);
      padding: 48px 0 32px;
      text-align: center;
      color: var(--text-muted);
      font-size: 13px;
    }}

    footer a {{
      color: var(--text-secondary);
      text-decoration: none;
      margin: 0 10px;
      transition: color var(--transition-fast);
    }}

    footer a:hover {{
      color: #fff;
    }}

    /* -------------------------------------------------------------
       RESPONSIVE BREAKPOINTS
       ------------------------------------------------------------- */
    @media (max-width: 992px) {{
      .categories-grid {{ grid-template-columns: repeat(2, 1fr); }}
    }}

    @media (max-width: 768px) {{
      .nav-links {{ display: none; }}
      .mobile-bottom-nav {{ display: flex; }}
      .hero {{ padding: 36px 0 24px; }}
      .hero-title {{ font-size: 32px; }}
      .categories-grid {{ grid-template-columns: repeat(2, 1fr); gap: 12px; }}
      .category-card {{ height: 110px; padding: 12px; }}
      .deals-grid {{ grid-template-columns: 1fr; gap: 16px; }}
      .coupons-grid {{ grid-template-columns: 1fr; }}
      .card-img-wrap {{ height: 200px; }}
    }}
  </style>
</head>
<body>

  <div class="ambient-glow"></div>

  <!-- HEADER -->
  <header>
    <div class="container">
      <div class="header-inner">
        <a href="/" class="brand-logo">
          ⚡ BigRedHub
          <span class="logo-badge">Pro</span>
        </a>

        <nav class="nav-links">
          <a href="#categories">Categories</a>
          <a href="#deals" class="active">Trending Deals</a>
          <a href="#coupons">Verified Coupons</a>
          <a href="#telegram">Telegram Bot</a>
        </nav>

        <div class="header-actions">
          <button class="fav-btn-header" onclick="filterFavorites()">
            ❤️ <span id="favCountHeader">0</span>
          </button>
          <a href="https://t.me/Under99LootDeals_bot" target="_blank" class="tg-header-btn">
            ⚡ Bot
          </a>
        </div>
      </div>
    </div>
  </header>

  <!-- HERO SECTION -->
  <section class="hero">
    <div class="container">
      <div class="hero-pill">
        <span>● LIVE DEALS SYNCED</span>
      </div>

      <h1 class="hero-title">
        <span class="gradient-text">Save More on Every Online Order.</span>
      </h1>
      
      <p class="hero-subtitle">
        Verified promo codes, EarnKaro cashback links & 90% price drops from Amazon, Flipkart, Myntra & boAt.
      </p>

      <!-- Minimal Search Box -->
      <div class="search-wrapper">
        <span class="search-icon-left">🔍</span>
        <input 
          type="text" 
          id="searchInput" 
          class="search-bar" 
          placeholder="Search stores, earbuds, sneakers, watches..."
          autocomplete="off"
        >
        <button id="searchClear" class="search-clear-btn" onclick="clearSearch()">✕</button>
      </div>

      <!-- Quick Search Chips -->
      <div class="popular-searches">
        <span class="popular-label">Popular:</span>
        <a href="javascript:void(0)" onclick="quickSearch('Under99')" class="search-chip">⚡ Under ₹99</a>
        <a href="javascript:void(0)" onclick="quickSearch('Amazon')" class="search-chip">Amazon</a>
        <a href="javascript:void(0)" onclick="quickSearch('Flipkart')" class="search-chip">Flipkart</a>
        <a href="javascript:void(0)" onclick="quickSearch('Earbuds')" class="search-chip">Earbuds</a>
        <a href="javascript:void(0)" onclick="quickSearch('Smartwatch')" class="search-chip">Smartwatch</a>
        <a href="javascript:void(0)" onclick="quickSearch('Sneakers')" class="search-chip">Sneakers</a>
      </div>
    </div>
  </section>

  <!-- CATEGORIES SECTION (Real Images) -->
  <section class="section-block" id="categories">
    <div class="container">
      <div class="section-head">
        <div>
          <h2 class="section-title">Shop by Category</h2>
          <p class="section-subtitle">Curated Indian retail categories with highest cashback rates</p>
        </div>
      </div>

      <div class="categories-grid">
"""

for cat in categories:
    html_template += f"""        <div class="category-card" onclick="filterCategory('{cat['id']}')">
          <img src="{cat['image']}" alt="{cat['name']}" class="category-bg-img" loading="lazy">
          <div class="category-overlay"></div>
          <div class="category-content">
            <span class="category-badge-chip">{cat['badge']}</span>
            <div class="category-name">{cat['icon']} {cat['name']}</div>
            <div class="category-count">{cat['count']}</div>
          </div>
        </div>
"""

html_template += f"""      </div>
    </div>
  </section>

  <!-- DEALS SECTION -->
  <section class="section-block" id="deals">
    <div class="container">
      <div class="section-head">
        <div>
          <h2 class="section-title">🔥 Live Loot Deals</h2>
          <p class="section-subtitle">Real products with live pricing & verified shortlinks</p>
        </div>
      </div>

      <!-- Filter Sticky Bar -->
      <div class="filter-sticky-wrap" id="filterBar">
        <button class="filter-pill active" onclick="filterCategory('all', this)">All Deals</button>
        <button class="filter-pill" onclick="filterCategory('under99', this)">⚡ Under ₹99</button>
        <button class="filter-pill" onclick="filterCategory('audio', this)">🎧 Audio</button>
        <button class="filter-pill" onclick="filterCategory('wearables', this)">⌚ Smartwatches</button>
        <button class="filter-pill" onclick="filterCategory('footwear', this)">👟 Footwear</button>
        <button class="filter-pill" onclick="filterCategory('fashion', this)">👗 Fashion</button>
        <button class="filter-pill" onclick="filterCategory('beauty', this)">💄 Beauty</button>
        <button class="filter-pill" onclick="filterCategory('electronics', this)">📱 Electronics</button>
        <button class="filter-pill" onclick="filterCategory('home', this)">🏠 Home</button>
      </div>

      <!-- Deals Grid -->
      <div class="deals-grid" id="dealsContainer">
"""

for deal in deals:
    html_template += f"""        <div class="deal-card" data-category="{deal['category']}" data-title="{deal['title'].lower()}" data-store="{deal['store'].lower()}" data-id="{deal['id']}">
          <div class="card-img-wrap">
            <img src="{deal['image']}" alt="{deal['title']}" class="card-product-img" loading="lazy">
            <span class="card-tag-pill">{deal.get('tag', 'VERIFIED')}</span>
            <span class="card-discount-badge">{deal['discount']}</span>
            <button class="card-fav-btn" onclick="toggleFavorite('{deal['id']}', event)" title="Save deal">❤️</button>
          </div>

          <div class="card-body">
            <div class="card-store-row">
              <span class="store-label">{deal['store_icon']} {deal['store']}</span>
              <span class="verified-micro">✓ {deal['verified']}</span>
            </div>

            <h3 class="deal-card-title">{deal['title']}</h3>

            <div class="card-price-row">
              <span class="price-loot">{deal['price']}</span>
              <span class="price-mrp">{deal['mrp']}</span>
            </div>

            <a href="{deal['affiliate_url']}" target="_blank" rel="noopener noreferrer" class="buy-btn-primary">
              Grab Deal ⚡
            </a>
          </div>
        </div>
"""

html_template += f"""      </div>
    </div>
  </section>

  <!-- VERIFIED COUPONS SECTION -->
  <section class="section-block" id="coupons">
    <div class="container">
      <div class="section-head">
        <div>
          <h2 class="section-title">✓ Verified Promo Codes</h2>
          <p class="section-subtitle">100% active coupons with 1-click clipboard copy</p>
        </div>
      </div>

      <div class="coupons-grid">
"""

for c in coupons:
    html_template += f"""        <div class="coupon-card">
          <div>
            <div class="coupon-top">
              <div class="coupon-store-info">
                <div class="store-icon-box">{c['icon']}</div>
                <div>
                  <div class="coupon-store-name">{c['store']}</div>
                  <div class="verified-micro">✓ {c['verified']}</div>
                </div>
              </div>
              <span class="coupon-disc-tag">{c['discount']}</span>
            </div>

            <p class="coupon-desc-text">{c['desc']}</p>
          </div>

          <div>
            <div class="coupon-code-box">
              <span class="code-string">{c['code']}</span>
              <button class="copy-btn-action" onclick="copyCoupon('{c['code']}', '{c['link']}', this)">
                COPY CODE
              </button>
            </div>

            <div class="coupon-footer-meta">
              <span>👥 {c['used']}</span>
              <span>⏳ Expires {c['expires']}</span>
            </div>
          </div>
        </div>
"""

html_template += f"""      </div>
    </div>
  </section>

  <!-- TELEGRAM VIP BANNER -->
  <section class="container" id="telegram">
    <div class="tg-banner">
      <h3>Never Miss a 90% Price Drop</h3>
      <p>Join 50,000+ smart Indian shoppers getting instant price glitch alerts, EarnKaro flash deals and Under ₹99 steals before they sell out.</p>
      
      <div class="tg-actions-row">
        <a href="https://t.me/Under99LootDeals_bot" target="_blank" class="tg-big-btn">
          ⚡ Open @Under99LootDeals_bot
        </a>
        <a href="https://t.me/Roxk755_bot" target="_blank" class="tg-secondary-btn">
          🛍️ Open @Roxk755_bot Hub
        </a>
      </div>
    </div>
  </section>

  <!-- FOOTER -->
  <footer>
    <div class="container">
      <p>© 2026 BigRedHub. Minimalist Indian deals & verified promo codes discovery platform.</p>
      <p style="margin-top: 10px;">
        <a href="#categories">Categories</a>
        <a href="#deals">Deals</a>
        <a href="#coupons">Coupons</a>
        <a href="https://t.me/Under99LootDeals_bot" target="_blank">Telegram Bot</a>
      </p>
    </div>
  </footer>

  <!-- MOBILE BOTTOM NAV -->
  <div class="mobile-bottom-nav">
    <a href="#" class="bottom-nav-item active">
      <span class="bottom-nav-icon">🏠</span>
      <span>Home</span>
    </a>
    <a href="#categories" class="bottom-nav-item">
      <span class="bottom-nav-icon">📁</span>
      <span>Categories</span>
    </a>
    <a href="#deals" class="bottom-nav-item">
      <span class="bottom-nav-icon">⚡</span>
      <span>Deals</span>
    </a>
    <a href="#coupons" class="bottom-nav-item">
      <span class="bottom-nav-icon">🎟️</span>
      <span>Coupons</span>
    </a>
    <button class="bottom-nav-item" onclick="filterFavorites()">
      <span class="bottom-nav-icon">❤️</span>
      <span>Saved</span>
    </button>
  </div>

  <!-- TOAST COMPONENT -->
  <div id="toast">
    <span>✓</span>
    <span id="toastMsg">Code copied to clipboard!</span>
  </div>

  <!-- CLIENT-SIDE LOGIC -->
  <script>
    let activeCategory = 'all';
    let savedFavorites = JSON.parse(localStorage.getItem('brh_favs') || '[]');

    function updateFavCount() {{
      const countEl = document.getElementById('favCountHeader');
      if (countEl) countEl.innerText = savedFavorites.length;
    }}
    updateFavCount();

    function showToast(msg) {{
      const toast = document.getElementById('toast');
      const toastMsg = document.getElementById('toastMsg');
      toastMsg.innerText = msg;
      toast.classList.add('show');
      setTimeout(() => {{
        toast.classList.remove('show');
      }}, 2600);
    }}

    function copyCoupon(code, link, btn) {{
      navigator.clipboard.writeText(code).then(() => {{
        const oldText = btn.innerText;
        btn.innerText = 'COPIED ✓';
        btn.classList.add('copied');
        showToast('Code ' + code + ' copied! Opening merchant...');
        
        setTimeout(() => {{
          btn.innerText = oldText;
          btn.classList.remove('copied');
        }}, 2500);

        if (link) {{
          setTimeout(() => {{
            window.open(link, '_blank');
          }}, 800);
        }}
      }});
    }}

    function toggleFavorite(id, e) {{
      e.stopPropagation();
      const idx = savedFavorites.indexOf(id);
      if (idx > -1) {{
        savedFavorites.splice(idx, 1);
        showToast('Removed from Saved ❤️');
      }} else {{
        savedFavorites.push(id);
        showToast('Saved to Favorites ❤️');
      }}
      localStorage.setItem('brh_favs', JSON.stringify(savedFavorites));
      updateFavCount();
    }}

    function filterFavorites() {{
      const cards = document.querySelectorAll('.deal-card');
      if (savedFavorites.length === 0) {{
        showToast('No saved deals yet! Click ❤️ on any card.');
        return;
      }}
      cards.forEach(card => {{
        const id = card.getAttribute('data-id');
        card.style.display = savedFavorites.includes(id) ? 'flex' : 'none';
      }});
      showToast('Showing your ' + savedFavorites.length + ' saved deals');
      document.getElementById('deals').scrollIntoView({{ behavior: 'smooth' }});
    }}

    function filterCategory(cat, btn) {{
      activeCategory = cat;
      const pills = document.querySelectorAll('.filter-pill');
      pills.forEach(p => p.classList.remove('active'));
      if (btn) btn.classList.add('active');

      const cards = document.querySelectorAll('.deal-card');
      cards.forEach(card => {{
        const cardCat = card.getAttribute('data-category');
        if (cat === 'all' || cardCat === cat) {{
          card.style.display = 'flex';
        }} else {{
          card.style.display = 'none';
        }}
      }});

      if (cat !== 'all') {{
        document.getElementById('deals').scrollIntoView({{ behavior: 'smooth' }});
      }}
    }}

    // Real-time Search
    const searchInput = document.getElementById('searchInput');
    const searchClear = document.getElementById('searchClear');

    if (searchInput) {{
      searchInput.addEventListener('input', function(e) {{
        const query = e.target.value.toLowerCase().trim();
        searchClear.style.display = query ? 'block' : 'none';
        
        const cards = document.querySelectorAll('.deal-card');
        cards.forEach(card => {{
          const title = card.getAttribute('data-title') || '';
          const store = card.getAttribute('data-store') || '';
          const cat = card.getAttribute('data-category') || '';
          
          if (title.includes(query) || store.includes(query) || cat.includes(query)) {{
            card.style.display = 'flex';
          }} else {{
            card.style.display = 'none';
          }}
        }});
      }});
    }}

    function clearSearch() {{
      if (searchInput) {{
        searchInput.value = '';
        searchClear.style.display = 'none';
        filterCategory('all');
      }}
    }}

    function quickSearch(term) {{
      if (searchInput) {{
        searchInput.value = term;
        searchInput.dispatchEvent(new Event('input'));
        document.getElementById('deals').scrollIntoView({{ behavior: 'smooth' }});
      }}
    }}
  </script>
</body>
</html>
"""

with open("landing.html", "w", encoding="utf-8") as f:
    f.write(html_template)

print("✅ Successfully generated production Apple/Nike style landing.html!")
