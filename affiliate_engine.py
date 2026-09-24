import os
import re
import urllib.parse
import urllib.request
import logging

logger = logging.getLogger("AffiliateEngine")

EARNKARO_REF_ID = os.getenv("EARNKARO_REF_ID", "1962062")

STORE_RATES = {
    "amazon": {"name": "Amazon India", "icon": "📦", "rate": "Up to 5% Cashback"},
    "flipkart": {"name": "Flipkart", "icon": "🛍️", "rate": "Up to 7% Cashback"},
    "myntra": {"name": "Myntra Fashion", "icon": "👗", "rate": "Up to 8.5% Cashback"},
    "ajio": {"name": "Ajio Trends", "icon": "✨", "rate": "Up to 9% Cashback"},
    "meesho": {"name": "Meesho Store", "icon": "🏷️", "rate": "Flat 6% Cashback"},
    "nykaa": {"name": "Nykaa Beauty", "icon": "💄", "rate": "Up to 6% Cashback"},
    "tata": {"name": "Tata CLiQ", "icon": "💎", "rate": "Up to 5.5% Cashback"},
    "croma": {"name": "Croma Electronics", "icon": "🔌", "rate": "Up to 4% Cashback"},
    "shopsy": {"name": "Shopsy Flipkart", "icon": "⚡", "rate": "Up to 7% Cashback"}
}

def detect_store(url: str) -> dict:
    url_lower = url.lower()
    for key, info in STORE_RATES.items():
        if key in url_lower:
            return info
    if "amzn.to" in url_lower or "amazon." in url_lower:
        return STORE_RATES["amazon"]
    if "fkrt.it" in url_lower or "flipkart." in url_lower:
        return STORE_RATES["flipkart"]
    return {"name": "Online Store", "icon": "🛒", "rate": "Flat 5% to 8% Cashback"}

def clean_store_url(raw_url: str) -> str:
    """Strips tracking query params (like competitor tags, fbclid, gclid, utm_*)"""
    try:
        parsed = urllib.parse.urlparse(raw_url)
        # Parse query params and filter out affiliate/ad tracking
        query_dict = urllib.parse.parse_qs(parsed.query)
        clean_params = {}
        for k, v in query_dict.items():
            k_lower = k.lower()
            if any(t in k_lower for t in ["tag", "affid", "fbclid", "gclid", "utm_", "ref", "aff_"]):
                continue
            clean_params[k] = v[0]
        
        new_query = urllib.parse.urlencode(clean_params)
        return urllib.parse.urlunparse((
            parsed.scheme,
            parsed.netloc,
            parsed.path,
            parsed.params,
            new_query,
            ""
        ))
    except Exception:
        return raw_url

def shorten_affiliate_url(long_url: str) -> str:
    """Shortens affiliate link using TinyURL with fallback"""
    try:
        api_url = "https://tinyurl.com/api-create.php?" + urllib.parse.urlencode({"url": long_url})
        req = urllib.request.Request(api_url, headers={"User-Agent": "Mozilla/5.0"})
        with urllib.request.urlopen(req, timeout=5) as response:
            if response.status == 200:
                return response.read().decode("utf-8").strip()
    except Exception as e:
        logger.warning(f"Shortener error: {e}")
    return long_url

def create_affiliate_deal_link(raw_url: str) -> dict:
    """
    Main conversion engine:
    1. Detects store
    2. Strips rival tracking tags
    3. Wraps with EarnKaro referral ID 1962062
    4. Masks with high-trust shortlink
    """
    store_info = detect_store(raw_url)
    cleaned = clean_store_url(raw_url)
    
    # Generate EarnKaro target
    earnkaro_url = f"https://earnkaro.com/deal?r={EARNKARO_REF_ID}&url={urllib.parse.quote(cleaned)}"
    masked_url = shorten_affiliate_url(earnkaro_url)
    
    return {
        "store": store_info["name"],
        "icon": store_info["icon"],
        "cashback_rate": store_info["rate"],
        "clean_url": cleaned,
        "affiliate_url": masked_url,
        "raw_url": raw_url
    }

CURATED_AFFILIATE_DEALS = [
    # Under ₹99 Mega Steals
    {
        "title": "Portronics Fast Braided Type-C Fast Charging Cable (1m)",
        "price": "₹69",
        "mrp": "₹299",
        "discount": "77% OFF",
        "category": "Under99",
        "url": "https://www.amazon.in/dp/B0CX21C229"
    },
    {
        "title": "Mobile Phone Desktop Stand & Foldable Cradle",
        "price": "₹49",
        "mrp": "₹399",
        "discount": "88% OFF",
        "category": "Under99",
        "url": "https://www.amazon.in/dp/B08L7V4QW6"
    },
    {
        "title": "Stainless Steel Unbreakable Water Bottle (1000ml)",
        "price": "₹89",
        "mrp": "₹599",
        "discount": "85% OFF",
        "category": "Under99",
        "url": "https://www.amazon.in/dp/B09J9H4F2L"
    },
    {
        "title": "Multipurpose Kitchen Silicone Spatula & Brush Set",
        "price": "₹39",
        "mrp": "₹249",
        "discount": "84% OFF",
        "category": "Under99",
        "url": "https://www.amazon.in/dp/B07Y7Z1K89"
    },
    {
        "title": "High Speed Dual USB 3.0 OTG Adapter for Android",
        "price": "₹29",
        "mrp": "₹199",
        "discount": "85% OFF",
        "category": "Under99",
        "url": "https://www.amazon.in/dp/B07N8M1Q4G"
    },
    
    # 80-90% OFF Gadgets & Electronics
    {
        "title": "Noise Buds VS102 Wireless Earbuds (50Hr Playtime, ENC)",
        "price": "₹799",
        "mrp": "₹2,999",
        "discount": "73% OFF",
        "category": "Loot",
        "url": "https://www.amazon.in/dp/B09D8PV67M"
    },
    {
        "title": "boAt Wave Call 2 Smartwatch with HD Bluetooth Calling",
        "price": "₹999",
        "mrp": "₹6,990",
        "discount": "86% OFF",
        "category": "Loot",
        "url": "https://www.amazon.in/dp/B0CB14J24R"
    },
    {
        "title": "Boult Audio BassBuds X1 in-Ear Wired Earphones with Mic",
        "price": "₹249",
        "mrp": "₹999",
        "discount": "75% OFF",
        "category": "Loot",
        "url": "https://www.amazon.in/dp/B071Z8M4KX"
    },
    {
        "title": "Ambrane 10000mAh Slim Fast Power Bank (20W PD Output)",
        "price": "₹699",
        "mrp": "₹1,999",
        "discount": "65% OFF",
        "category": "Loot",
        "url": "https://www.amazon.in/dp/B08HVG617S"
    },
    
    # VIP Secret Glitch Deals (90%+ OFF)
    {
        "title": "🔥 [PRICE GLITCH] Fastrack Revoltt FS1 Pro Smartwatch AMOLED",
        "price": "₹1,199",
        "mrp": "₹7,995",
        "discount": "85% OFF GLITCH",
        "category": "VIP",
        "url": "https://www.amazon.in/dp/B0C157X5C7"
    },
    {
        "title": "⚡ [BUG DEAL] Red Tape Men Running Athletic Shoes (Air Cushion)",
        "price": "₹899",
        "mrp": "₹5,499",
        "discount": "84% OFF GLITCH",
        "category": "VIP",
        "url": "https://www.amazon.in/dp/B0BSNK8J18"
    },
    {
        "title": "🎁 [₹1 SAMPLE OFFER] Premium Microfiber Cleaning Cloth 4-Pack",
        "price": "₹1",
        "mrp": "₹299",
        "discount": "99% OFF GLITCH",
        "category": "VIP",
        "url": "https://www.amazon.in/dp/B079Q5R4Z1"
    }
]
