import urllib.parse
import urllib.request
import json
import os

EARNKARO_REF_ID = "1962062"

def shorten_affiliate_url(long_url: str) -> str:
    try:
        api_url = "https://tinyurl.com/api-create.php?" + urllib.parse.urlencode({"url": long_url})
        req = urllib.request.Request(api_url, headers={"User-Agent": "Mozilla/5.0"})
        with urllib.request.urlopen(req, timeout=5) as response:
            if response.status == 200:
                return response.read().decode("utf-8").strip()
    except Exception as e:
        print("Shortener error:", e)
    return long_url

def make_earnkaro_link(url: str) -> str:
    earnkaro_url = f"https://earnkaro.com/deal?r={EARNKARO_REF_ID}&url={urllib.parse.quote(url)}"
    return shorten_affiliate_url(earnkaro_url)

deals = [
    {
        "id": "deal_1",
        "title": "Portronics Fast Braided Type-C Fast Charging Cable (1m, 65W)",
        "store": "Amazon India",
        "store_icon": "📦",
        "price": "₹69",
        "mrp": "₹299",
        "discount": "77% OFF",
        "category": "under99",
        "category_name": "Under ₹99",
        "image": "https://images.unsplash.com/photo-1583394838336-acd977736f90?w=600&auto=format&fit=crop&q=80",
        "url": "https://www.amazon.in/dp/B0CX21C229",
        "verified": "Verified 1h ago",
        "tag": "HOT DEAL"
    },
    {
        "id": "deal_2",
        "title": "Mobile Phone Desktop Stand & 360° Foldable Metallic Cradle",
        "store": "Amazon India",
        "store_icon": "📦",
        "price": "₹49",
        "mrp": "₹399",
        "discount": "88% OFF",
        "category": "under99",
        "category_name": "Under ₹99",
        "image": "https://images.unsplash.com/photo-1586105251261-72a756497a11?w=600&auto=format&fit=crop&q=80",
        "url": "https://www.amazon.in/dp/B08L7V4QW6",
        "verified": "Verified 2h ago",
        "tag": "STEAL DEAL"
    },
    {
        "id": "deal_3",
        "title": "High Speed Dual USB 3.0 Metallic OTG Adapter for Android/iOS",
        "store": "Flipkart",
        "store_icon": "🛍️",
        "price": "₹29",
        "mrp": "₹199",
        "discount": "85% OFF",
        "category": "under99",
        "category_name": "Under ₹99",
        "image": "https://images.unsplash.com/photo-1622445262464-84b14e414581?w=600&auto=format&fit=crop&q=80",
        "url": "https://www.amazon.in/dp/B07N8M1Q4G",
        "verified": "Verified 30m ago",
        "tag": "LOWEST PRICE"
    },
    {
        "id": "deal_4",
        "title": "Noise Buds VS102 Wireless ANC Earbuds (50Hr Battery, Low Latency)",
        "store": "Amazon India",
        "store_icon": "📦",
        "price": "₹799",
        "mrp": "₹2,999",
        "discount": "73% OFF",
        "category": "audio",
        "category_name": "Audio & Wearables",
        "image": "https://images.unsplash.com/photo-1590658268037-6bf12165a8df?w=600&auto=format&fit=crop&q=80",
        "url": "https://www.amazon.in/dp/B09D8PV67M",
        "verified": "Verified 45m ago",
        "tag": "TRENDING"
    },
    {
        "id": "deal_5",
        "title": "boAt Wave Call 2 Smartwatch w/ HD Bluetooth Calling & 1.83\" HD Display",
        "store": "boAt Lifestyle",
        "store_icon": "🎧",
        "price": "₹999",
        "mrp": "₹6,990",
        "discount": "86% OFF",
        "category": "wearables",
        "category_name": "Smartwatches",
        "image": "https://images.unsplash.com/photo-1523275335684-37898b6baf30?w=600&auto=format&fit=crop&q=80",
        "url": "https://www.amazon.in/dp/B0CB14J24R",
        "verified": "Verified 1h ago",
        "tag": "86% OFF"
    },
    {
        "id": "deal_6",
        "title": "Boult Audio BassBuds X1 in-Ear Deep Bass Heavy Metal Earphones",
        "store": "Flipkart",
        "store_icon": "🛍️",
        "price": "₹249",
        "mrp": "₹999",
        "discount": "75% OFF",
        "category": "audio",
        "category_name": "Audio & Wearables",
        "image": "https://images.unsplash.com/photo-1505740420928-5e560c06d30e?w=600&auto=format&fit=crop&q=80",
        "url": "https://www.amazon.in/dp/B071Z8M4KX",
        "verified": "Verified 2h ago",
        "tag": "POPULAR"
    },
    {
        "id": "deal_7",
        "title": "Ambrane 10000mAh Ultra-Slim 20W Fast Power Bank (Type C + USB)",
        "store": "Amazon India",
        "store_icon": "📦",
        "price": "₹699",
        "mrp": "₹1,999",
        "discount": "65% OFF",
        "category": "electronics",
        "category_name": "Electronics",
        "image": "https://images.unsplash.com/photo-1609091839311-d5365f9ff1c5?w=600&auto=format&fit=crop&q=80",
        "url": "https://www.amazon.in/dp/B08HVG617S",
        "verified": "Verified 4h ago",
        "tag": "FAST CHARGE"
    },
    {
        "id": "deal_8",
        "title": "Red Tape Men Retro Air Cushion Lightweight Running Sneakers",
        "store": "Myntra",
        "store_icon": "👗",
        "price": "₹899",
        "mrp": "₹5,499",
        "discount": "84% OFF",
        "category": "footwear",
        "category_name": "Footwear",
        "image": "https://images.unsplash.com/photo-1542291026-7eec264c27ff?w=600&auto=format&fit=crop&q=80",
        "url": "https://www.amazon.in/dp/B0BSNK8J18",
        "verified": "Verified 1h ago",
        "tag": "PRICE DROP"
    },
    {
        "id": "deal_9",
        "title": "Puma Solid Regular Fit Men Pure Cotton Breathable Athletic T-Shirt",
        "store": "AJIO",
        "store_icon": "✨",
        "price": "₹399",
        "mrp": "₹1,499",
        "discount": "73% OFF",
        "category": "fashion",
        "category_name": "Fashion",
        "image": "https://images.unsplash.com/photo-1521572267360-ee0c2909d518?w=600&auto=format&fit=crop&q=80",
        "url": "https://www.amazon.in/dp/B08XYZ1234",
        "verified": "Verified 2h ago",
        "tag": "BESTSELLER"
    },
    {
        "id": "deal_10",
        "title": "Beardo Dark Side Luxury Perfume for Men EDP (100ml Fragrance)",
        "store": "Nykaa Man",
        "store_icon": "💄",
        "price": "₹449",
        "mrp": "₹1,500",
        "discount": "70% OFF",
        "category": "beauty",
        "category_name": "Beauty & Grooming",
        "image": "https://images.unsplash.com/photo-1592945403244-b3fbafd7f539?w=600&auto=format&fit=crop&q=80",
        "url": "https://www.amazon.in/dp/B07P8R7W6X",
        "verified": "Verified 3h ago",
        "tag": "70% OFF"
    },
    {
        "id": "deal_11",
        "title": "Philips Multi-Grooming All-in-One Cordless Trimmer Series 3000",
        "store": "Amazon India",
        "store_icon": "📦",
        "price": "₹849",
        "mrp": "₹2,195",
        "discount": "61% OFF",
        "category": "beauty",
        "category_name": "Beauty & Grooming",
        "image": "https://images.unsplash.com/photo-1621607512214-68297480165e?w=600&auto=format&fit=crop&q=80",
        "url": "https://www.amazon.in/dp/B010X581VG",
        "verified": "Verified 1h ago",
        "tag": "TOP RATED"
    },
    {
        "id": "deal_12",
        "title": "Stainless Steel Insulated Unbreakable Thermal Flask Water Bottle (1L)",
        "store": "Amazon India",
        "store_icon": "📦",
        "price": "₹89",
        "mrp": "₹599",
        "discount": "85% OFF",
        "category": "home",
        "category_name": "Home & Kitchen",
        "image": "https://images.unsplash.com/photo-1602143407151-7111542de6e8?w=600&auto=format&fit=crop&q=80",
        "url": "https://www.amazon.in/dp/B09J9H4F2L",
        "verified": "Verified 3h ago",
        "tag": "UNDER ₹99"
    }
]

categories = [
    {
        "id": "under99",
        "name": "Under ₹99 Steals",
        "badge": "From ₹29",
        "count": "180+ Deals",
        "image": "https://images.unsplash.com/photo-1583394838336-acd977736f90?w=500&auto=format&fit=crop&q=80",
        "icon": "⚡"
    },
    {
        "id": "audio",
        "name": "Audio & Headphones",
        "badge": "Up to 80% OFF",
        "count": "95+ Deals",
        "image": "https://images.unsplash.com/photo-1505740420928-5e560c06d30e?w=500&auto=format&fit=crop&q=80",
        "icon": "🎧"
    },
    {
        "id": "wearables",
        "name": "Smartwatches",
        "badge": "Up to 85% OFF",
        "count": "64+ Deals",
        "image": "https://images.unsplash.com/photo-1523275335684-37898b6baf30?w=500&auto=format&fit=crop&q=80",
        "icon": "⌚"
    },
    {
        "id": "footwear",
        "name": "Sneakers & Footwear",
        "badge": "Up to 84% OFF",
        "count": "120+ Deals",
        "image": "https://images.unsplash.com/photo-1542291026-7eec264c27ff?w=500&auto=format&fit=crop&q=80",
        "icon": "👟"
    },
    {
        "id": "fashion",
        "name": "Fashion & Apparel",
        "badge": "Up to 75% OFF",
        "count": "240+ Deals",
        "image": "https://images.unsplash.com/photo-1521572267360-ee0c2909d518?w=500&auto=format&fit=crop&q=80",
        "icon": "👗"
    },
    {
        "id": "beauty",
        "name": "Beauty & Grooming",
        "badge": "Up to 70% OFF",
        "count": "88+ Deals",
        "image": "https://images.unsplash.com/photo-1592945403244-b3fbafd7f539?w=500&auto=format&fit=crop&q=80",
        "icon": "💄"
    },
    {
        "id": "electronics",
        "name": "Mobiles & Gadgets",
        "badge": "Up to 65% OFF",
        "count": "150+ Deals",
        "image": "https://images.unsplash.com/photo-1609091839311-d5365f9ff1c5?w=500&auto=format&fit=crop&q=80",
        "icon": "📱"
    },
    {
        "id": "home",
        "name": "Home & Kitchen",
        "badge": "Up to 85% OFF",
        "count": "110+ Deals",
        "image": "https://images.unsplash.com/photo-1602143407151-7111542de6e8?w=500&auto=format&fit=crop&q=80",
        "icon": "🏠"
    }
]

print("Generating shortlinks for all deals...")
for d in deals:
    d["affiliate_url"] = make_earnkaro_link(d["url"])
    print(f"{d['title'][:30]} -> {d['affiliate_url']}")

with open("earnkaro_catalog.json", "w", encoding="utf-8") as f:
    json.dump({"categories": categories, "deals": deals}, f, indent=2)

print("Saved earnkaro_catalog.json successfully!")
