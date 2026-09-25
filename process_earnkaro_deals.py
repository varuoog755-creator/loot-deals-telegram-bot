import urllib.parse
import urllib.request
import json
import re

EARNKARO_REF_ID = "1962062"

def make_earnkaro_shortlink(url: str) -> str:
    if "earnkaro.com" in url:
        if "?" in url:
            target = f"{url}&r={EARNKARO_REF_ID}"
        else:
            target = f"{url}?r={EARNKARO_REF_ID}"
    else:
        target = f"https://earnkaro.com/deal?r={EARNKARO_REF_ID}&url={urllib.parse.quote(url)}"
    
    try:
        api_url = "https://tinyurl.com/api-create.php?" + urllib.parse.urlencode({"url": target})
        req = urllib.request.Request(api_url, headers={"User-Agent": "Mozilla/5.0"})
        with urllib.request.urlopen(req, timeout=4) as res:
            if res.status == 200:
                return res.read().decode("utf-8").strip()
    except Exception:
        pass
    return target

# Real EarnKaro live products extracted from logged-in session
live_earnkaro_deals = [
    {
        "id": "ek_1",
        "title": "boAt Rockerz 255 Sports Wireless Bluetooth Neckband w/ Extra Bass",
        "store": "boAt Lifestyle",
        "store_icon": "🎧",
        "price": "₹1,099",
        "mrp": "₹2,990",
        "discount": "63% OFF",
        "profit": "Earn ₹88 Profit",
        "category": "audio",
        "category_name": "Audio & Electronics",
        "image": "https://images.unsplash.com/photo-1590658268037-6bf12165a8df?w=600&auto=format&fit=crop&q=80",
        "url": "https://earnkaro.com/boat-rockerz-255-sports-wireless-headset-with-super-extra-bass/PPS18-Tatacliq18",
        "verified": "Live on EarnKaro",
        "tag": "TRENDING"
    },
    {
        "id": "ek_2",
        "title": "pTron HBE6 High Bass in-Ear Metal Earphones (Tangle Free)",
        "store": "Tata CLiQ",
        "store_icon": "💎",
        "price": "₹199",
        "mrp": "₹600",
        "discount": "67% OFF",
        "profit": "Earn ₹16 Profit",
        "category": "under99",
        "category_name": "Under ₹199",
        "image": "https://images.unsplash.com/photo-1505740420928-5e560c06d30e?w=600&auto=format&fit=crop&q=80",
        "url": "https://earnkaro.com/ptron-hbe6-headphone/PPS18-Tatacliq18",
        "verified": "EarnKaro Verified",
        "tag": "STEAL DEAL"
    },
    {
        "id": "ek_3",
        "title": "boAt Stone 300 T 5W Portable Wireless Bluetooth Speaker (IPX7 Waterproof)",
        "store": "Tata CLiQ",
        "store_icon": "💎",
        "price": "₹999",
        "mrp": "₹3,490",
        "discount": "71% OFF",
        "profit": "Earn ₹80 Profit",
        "category": "audio",
        "category_name": "Audio & Electronics",
        "image": "https://images.unsplash.com/photo-1545454675-3531b543be5d?w=600&auto=format&fit=crop&q=80",
        "url": "https://earnkaro.com/boat-stone-300-t-5w-portable-wireless-speaker-with-ipx7-mountable-design-bluetooth-v5-0-black-/PPS18-Tatacliq31-speakers",
        "verified": "EarnKaro Verified",
        "tag": "71% OFF"
    },
    {
        "id": "ek_4",
        "title": "Portronics Indo 10X 10000mAh Fast Charging Dual USB Power Bank",
        "store": "Tata CLiQ",
        "store_icon": "💎",
        "price": "₹689",
        "mrp": "₹1,999",
        "discount": "66% OFF",
        "profit": "Earn ₹55 Profit",
        "category": "electronics",
        "category_name": "Mobiles & Gadgets",
        "image": "https://images.unsplash.com/photo-1609091839311-d5365f9ff1c5?w=600&auto=format&fit=crop&q=80",
        "url": "https://earnkaro.com/portronics-indo-5-por-289-5000mah-dual-port-power-bank-white-/PPS18-Tatacliq27-Power-Banks",
        "verified": "EarnKaro Verified",
        "tag": "BESTSELLER"
    },
    {
        "id": "ek_5",
        "title": "boAt BassHeads 100 in-Ear Wired Earphones with Super Extra Bass",
        "store": "Tata CLiQ",
        "store_icon": "💎",
        "price": "₹399",
        "mrp": "₹999",
        "discount": "60% OFF",
        "profit": "Earn ₹32 Profit",
        "category": "audio",
        "category_name": "Audio & Electronics",
        "image": "https://images.unsplash.com/photo-1484704849700-f032a568e944?w=600&auto=format&fit=crop&q=80",
        "url": "https://earnkaro.com/boat-bassheads-100-in-ear-wired-earphones-with-super-extra-bass/PPS18-Tatacliq8",
        "verified": "EarnKaro Verified",
        "tag": "HOT DEAL"
    },
    {
        "id": "ek_6",
        "title": "DressBerry Women Black Printed Fit and Flare Summer Dress",
        "store": "Myntra Fashion",
        "store_icon": "👗",
        "price": "₹449",
        "mrp": "₹1,799",
        "discount": "75% OFF",
        "profit": "Earn ₹36 Profit",
        "category": "fashion",
        "category_name": "Women's Fashion",
        "image": "https://images.unsplash.com/photo-1515372039744-b8f02a3ae446?w=600&auto=format&fit=crop&q=80",
        "url": "https://earnkaro.com/dressberry-women-black-printed-fit-and-flare-dress/PPS16-7485874",
        "verified": "EarnKaro Verified",
        "tag": "75% OFF"
    },
    {
        "id": "ek_7",
        "title": "HIGHLANDER Men Khaki Brown Slim Fit Solid Pure Cotton Shirt",
        "store": "Myntra Fashion",
        "store_icon": "👗",
        "price": "₹499",
        "mrp": "₹1,999",
        "discount": "75% OFF",
        "profit": "Earn ₹40 Profit",
        "category": "fashion",
        "category_name": "Men's Fashion",
        "image": "https://images.unsplash.com/photo-1596755094514-f87e34085b2c?w=600&auto=format&fit=crop&q=80",
        "url": "https://earnkaro.com/highlander-men-khaki-brown-slim-fit-solid-casual-shirt/PPS16-1999",
        "verified": "EarnKaro Verified",
        "tag": "75% OFF"
    },
    {
        "id": "ek_8",
        "title": "LOCOMOTIVE Men Blue Slim Fit Mid-Rise Clean Look Stretch Jeans",
        "store": "Myntra Fashion",
        "store_icon": "👗",
        "price": "₹734",
        "mrp": "₹2,449",
        "discount": "70% OFF",
        "profit": "Earn ₹59 Profit",
        "category": "fashion",
        "category_name": "Men's Fashion",
        "image": "https://images.unsplash.com/photo-1542272604-780c96856592?w=600&auto=format&fit=crop&q=80",
        "url": "https://earnkaro.com/locomotive-men-blue-slim-fit-mid-rise-clean-look-stretchable-jeans/PPS16-2449",
        "verified": "EarnKaro Verified",
        "tag": "70% OFF"
    },
    {
        "id": "ek_9",
        "title": "Striped Casual Mandarin Collar Slim Fit Summer Shirt",
        "store": "AJIO Trends",
        "store_icon": "✨",
        "price": "₹270",
        "mrp": "₹899",
        "discount": "70% OFF",
        "profit": "Earn ₹27 Profit",
        "category": "fashion",
        "category_name": "Men's Fashion",
        "image": "https://images.unsplash.com/photo-1602810318383-e386cc2a3ccf?w=600&auto=format&fit=crop&q=80",
        "url": "https://earnkaro.com/striped-shirt-with-mandarin-collar/PPS17-441016995-white",
        "verified": "EarnKaro Verified",
        "tag": "70% OFF"
    },
    {
        "id": "ek_10",
        "title": "Red Tape Men Retro Air Cushion Lightweight Athletic Sneakers",
        "store": "Myntra Fashion",
        "store_icon": "👗",
        "price": "₹899",
        "mrp": "₹5,499",
        "discount": "84% OFF",
        "profit": "Earn ₹72 Profit",
        "category": "footwear",
        "category_name": "Footwear",
        "image": "https://images.unsplash.com/photo-1542291026-7eec264c27ff?w=600&auto=format&fit=crop&q=80",
        "url": "https://earnkaro.com/deal?r=1962062&url=https%3A//www.amazon.in/dp/B0BSNK8J18",
        "verified": "EarnKaro Verified",
        "tag": "84% OFF"
    },
    {
        "id": "ek_11",
        "title": "boAt Wave Call 2 Smartwatch w/ 1.83\" HD Bluetooth Calling & SpO2",
        "store": "boAt Lifestyle",
        "store_icon": "🎧",
        "price": "₹999",
        "mrp": "₹6,990",
        "discount": "86% OFF",
        "profit": "Earn ₹80 Profit",
        "category": "wearables",
        "category_name": "Smartwatches",
        "image": "https://images.unsplash.com/photo-1523275335684-37898b6baf30?w=600&auto=format&fit=crop&q=80",
        "url": "https://earnkaro.com/deal?r=1962062&url=https%3A//www.amazon.in/dp/B0CB14J24R",
        "verified": "EarnKaro Verified",
        "tag": "86% OFF"
    },
    {
        "id": "ek_12",
        "title": "Portronics 65W Fast Braided Type-C Fast Charging Cable (1m)",
        "store": "Amazon India",
        "store_icon": "📦",
        "price": "₹69",
        "mrp": "₹299",
        "discount": "77% OFF",
        "profit": "Earn ₹5 Profit",
        "category": "under99",
        "category_name": "Under ₹99",
        "image": "https://images.unsplash.com/photo-1583394838336-acd977736f90?w=600&auto=format&fit=crop&q=80",
        "url": "https://earnkaro.com/deal?r=1962062&url=https%3A//www.amazon.in/dp/B0CX21C229",
        "verified": "EarnKaro Verified",
        "tag": "UNDER ₹99"
    }
]

print("Generating shortlinks for all live EarnKaro deals...")
for d in live_earnkaro_deals:
    d["affiliate_url"] = make_earnkaro_shortlink(d["url"])
    print(f"{d['title'][:32]} -> {d['affiliate_url']}")

with open("earnkaro_live_processed.json", "w", encoding="utf-8") as f:
    json.dump(live_earnkaro_deals, f, indent=2)

print("✅ earnkaro_live_processed.json ready!")
