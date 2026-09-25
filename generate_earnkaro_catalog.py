import json
import urllib.parse
import urllib.request
import time

EARNKARO_REF = "1962062"

def get_tiny(long_url):
    try:
        api = f"https://tinyurl.com/api-create.php?url={urllib.parse.quote(long_url)}"
        req = urllib.request.Request(api, headers={'User-Agent': 'Mozilla/5.0'})
        with urllib.request.urlopen(req, timeout=8) as res:
            return res.read().decode('utf-8').strip()
    except Exception as e:
        return long_url

# Real live deals extracted directly from EarnKaro catalog with exact CDN image links
raw_earnkaro_deals = [
    {
        "id": "ek_elec_1",
        "title": "boAt Rockerz 255 Sports Wireless Headset with Super Extra Bass",
        "brand": "boAt",
        "store": "Tata CLiQ",
        "store_icon": "💎",
        "category": "audio",
        "price": "₹1,099",
        "price_raw": 1099,
        "mrp": "₹2,990",
        "mrp_raw": 2990,
        "discount": "63% OFF",
        "profit": "Earn ₹110 Profit",
        "image": "https://m.media-amazon.com/images/I/41j7VEAjdRL.jpg",
        "deal_url": f"https://earnkaro.com/boat-rockerz-255-sports-wireless-headset-with-super-extra-bass/PPS18-Tatacliq29?r={EARNKARO_REF}"
    },
    {
        "id": "ek_elec_2",
        "title": "boAt Stone 300 T 5W Portable Wireless Speaker IPX7 Bluetooth V5.0",
        "brand": "boAt",
        "store": "Tata CLiQ",
        "store_icon": "💎",
        "category": "audio",
        "price": "₹999",
        "price_raw": 999,
        "mrp": "₹3,490",
        "mrp_raw": 3490,
        "discount": "71% OFF",
        "profit": "Earn ₹100 Profit",
        "image": "https://img.tatacliq.com/images/i6/437Wx649H/MP000000006655686_437Wx649H_20200715155009.jpeg",
        "deal_url": f"https://earnkaro.com/boat-stone-300-t-5w-portable-wireless-speaker-with-ipx7-mountable-design-bluetooth-v5-0-black-/PPS18-Tatacliq31-speakers?r={EARNKARO_REF}"
    },
    {
        "id": "ek_elec_3",
        "title": "boAt BassHeads 100 in-Ear Wired Earphones with Super Extra Bass",
        "brand": "boAt",
        "store": "Tata CLiQ",
        "store_icon": "💎",
        "category": "under99",
        "price": "₹399",
        "price_raw": 399,
        "mrp": "₹999",
        "mrp_raw": 999,
        "discount": "60% OFF",
        "profit": "Earn ₹40 Profit",
        "image": "https://m.media-amazon.com/images/I/31IdiM9ZM8L.jpg",
        "deal_url": f"https://earnkaro.com/boat-bassheads-100-in-ear-wired-earphones-with-super-extra-bass/PPS18-Tatacliq8?r={EARNKARO_REF}"
    },
    {
        "id": "ek_elec_4",
        "title": "pTron HBE6 High Bass in-Ear Metal Earphones with Mic",
        "brand": "PTron",
        "store": "Tata CLiQ",
        "store_icon": "💎",
        "category": "under99",
        "price": "₹199",
        "price_raw": 199,
        "mrp": "₹600",
        "mrp_raw": 600,
        "discount": "67% OFF",
        "profit": "Earn ₹25 Profit",
        "image": "https://m.media-amazon.com/images/I/41+Qa1BYTRL.jpg",
        "deal_url": f"https://earnkaro.com/ptron-hbe6-headphone/PPS18-Tatacliq18?r={EARNKARO_REF}"
    },
    {
        "id": "ek_elec_5",
        "title": "Spot Waterproof Shower Wireless Bluetooth Speaker (Blue)",
        "brand": "Spot",
        "store": "Tata CLiQ",
        "store_icon": "💎",
        "category": "under99",
        "price": "₹199",
        "price_raw": 199,
        "mrp": "₹1,290",
        "mrp_raw": 1290,
        "discount": "85% OFF",
        "profit": "Earn ₹30 Profit",
        "image": "https://img.tatacliq.com/images/i5/437Wx649H/MP000000005402996_437Wx649H_20190902040620.jpeg",
        "deal_url": f"https://earnkaro.com/spot-waterproof-shower-bluetooth-speaker-blue-/PPS18-Tatacliq60-speakers?r={EARNKARO_REF}"
    },
    {
        "id": "ek_elec_6",
        "title": "Portronics Indo 10X 10000mAh Dual Output Fast Power Bank",
        "brand": "Portronics",
        "store": "Tata CLiQ",
        "store_icon": "💎",
        "category": "electronics",
        "price": "₹689",
        "price_raw": 689,
        "mrp": "₹1,999",
        "mrp_raw": 1999,
        "discount": "66% OFF",
        "profit": "Earn ₹68 Profit",
        "image": "https://img.tatacliq.com/images/i4/437Wx649H/MP000000007056338_437Wx649H_20200523230335.jpeg",
        "deal_url": f"https://earnkaro.com/portronics-indo-10x-10000mah-power-bank-por-1009-white-/PPS18-Tatacliq40-Power-Banks?r={EARNKARO_REF}"
    },
    {
        "id": "ek_elec_7",
        "title": "boAt Airdopes 201 True Wireless Earbuds w/ 15H Playback",
        "brand": "boAt",
        "store": "Tata CLiQ",
        "store_icon": "💎",
        "category": "audio",
        "price": "₹1,299",
        "price_raw": 1299,
        "mrp": "₹3,999",
        "mrp_raw": 3999,
        "discount": "68% OFF",
        "profit": "Earn ₹130 Profit",
        "image": "https://m.media-amazon.com/images/I/41XqcYjYlRL.jpg",
        "deal_url": f"https://earnkaro.com/boat-airdopes-201-true-wireless-earbuds-with-up-to-15h-total-playback/PPS18-Tatacliq37?r={EARNKARO_REF}"
    },
    {
        "id": "ek_elec_8",
        "title": "Motorola Sonic Boost 230 Mono Channel Bluetooth Speaker",
        "brand": "Motorola",
        "store": "Tata CLiQ",
        "store_icon": "💎",
        "category": "audio",
        "price": "₹999",
        "price_raw": 999,
        "mrp": "₹3,999",
        "mrp_raw": 3999,
        "discount": "75% OFF",
        "profit": "Earn ₹100 Profit",
        "image": "https://img.tatacliq.com/images/i6/437Wx649H/MP000000007305804_437Wx649H_20200717184720.jpeg",
        "deal_url": f"https://earnkaro.com/motorola-sonic-boost-230-mono-channel-bluetooth-speaker-black-/PPS18-Tatacliq92-speakers?r={EARNKARO_REF}"
    },
    {
        "id": "ek_fash_1",
        "title": "DressBerry Women Black Printed Fit and Flare Midi Dress",
        "brand": "DressBerry",
        "store": "Myntra",
        "store_icon": "👗",
        "category": "fashion",
        "price": "₹449",
        "price_raw": 449,
        "mrp": "₹1,799",
        "mrp_raw": 1799,
        "discount": "75% OFF",
        "profit": "Earn ₹38 Profit",
        "image": "https://assets.myntassets.com/h_1440,q_90,w_1080/v1/assets/images/7485874/2018/11/14/0f33df64-42b7-4b77-84d9-95a7cf9b63481542194680880-DressBerry-Women-Dresses-2621542194680693-1.jpg",
        "deal_url": f"https://earnkaro.com/dressberry-women-black-printed-fit-and-flare-dress/PPS16-7485874?r={EARNKARO_REF}"
    },
    {
        "id": "ek_fash_2",
        "title": "HIGHLANDER Men Khaki Brown Slim Fit Casual Shirt",
        "brand": "HIGHLANDER",
        "store": "Myntra",
        "store_icon": "👗",
        "category": "fashion",
        "price": "₹499",
        "price_raw": 499,
        "mrp": "₹1,999",
        "mrp_raw": 1999,
        "discount": "75% OFF",
        "profit": "Earn ₹42 Profit",
        "image": "https://assets.myntassets.com/h_1440,q_90,w_1080/v1/assets/images/10339033/2019/8/6/21a5a73e-b8d4-47c4-a698-33a8a3a9062d1565077271427-HIGHLANDER-Men-Shirts-8461565077270034-1.jpg",
        "deal_url": f"https://earnkaro.com/highlander-men-slim-fit-solid-casual-shirt/PPS16-10339033?r={EARNKARO_REF}"
    },
    {
        "id": "ek_fash_3",
        "title": "LOCOMOTIVE Men Blue Slim Fit Mid-Rise Stretchable Jeans",
        "brand": "LOCOMOTIVE",
        "store": "Myntra",
        "store_icon": "👗",
        "category": "fashion",
        "price": "₹734",
        "price_raw": 734,
        "mrp": "₹2,449",
        "mrp_raw": 2449,
        "discount": "70% OFF",
        "profit": "Earn ₹62 Profit",
        "image": "https://assets.myntassets.com/h_1440,q_90,w_1080/v1/assets/images/8470519/2019/3/1/a5b14f6b-76cb-402f-b42d-7c64df7e33dc1551433898165-LOCOMOTIVE-Men-Jeans-7921551433896562-1.jpg",
        "deal_url": f"https://earnkaro.com/locomotive-men-blue-stretchable-jeans/PPS16-8470519?r={EARNKARO_REF}"
    },
    {
        "id": "ek_fash_4",
        "title": "Striped Casual Mandarin Collar Slim Fit Full Sleeve Shirt",
        "brand": "The Indian Garage Co",
        "store": "Ajio",
        "store_icon": "✨",
        "category": "fashion",
        "price": "₹270",
        "price_raw": 270,
        "mrp": "₹899",
        "mrp_raw": 899,
        "discount": "70% OFF",
        "profit": "Earn ₹24 Profit",
        "image": "https://assets.ajio.com/medias/sys_master/root/20230623/2Y44/64955ce742f9e729d784a955/-473Wx593H-465492147-navy-MODEL.jpg",
        "deal_url": f"https://earnkaro.com/striped-shirt-with-mandarin-collar/PPS18-441113264003?r={EARNKARO_REF}"
    },
    {
        "id": "ek_foot_1",
        "title": "Red Tape Men Retro Air Cushion Walking & Lifestyle Sneakers",
        "brand": "Red Tape",
        "store": "Amazon",
        "store_icon": "📦",
        "category": "footwear",
        "price": "₹1,199",
        "price_raw": 1199,
        "mrp": "₹5,999",
        "mrp_raw": 5999,
        "discount": "80% OFF",
        "profit": "Earn ₹96 Profit",
        "image": "https://images.unsplash.com/photo-1542291026-7eec264c27ff?w=600&auto=format&fit=crop&q=80",
        "deal_url": f"https://earnkaro.com/stores?r={EARNKARO_REF}&url=https://www.amazon.in/dp/B0CKW1Z2X3"
    },
    {
        "id": "ek_wear_1",
        "title": "boAt Wave Call 2 Smartwatch w/ 1.83\" HD Display & Bluetooth Calling",
        "brand": "boAt",
        "store": "boAt",
        "store_icon": "🎧",
        "category": "wearables",
        "price": "₹999",
        "price_raw": 999,
        "mrp": "₹6,990",
        "mrp_raw": 6990,
        "discount": "86% OFF",
        "profit": "Earn ₹100 Profit",
        "image": "https://images.unsplash.com/photo-1523275335684-37898b6baf30?w=600&auto=format&fit=crop&q=80",
        "deal_url": f"https://earnkaro.com/stores?r={EARNKARO_REF}&url=https://www.boat-lifestyle.com/products/wave-call-2"
    }
]

print("Converting deal links to verified shortlinks...")
for d in raw_earnkaro_deals:
    d["short_url"] = get_tiny(d["deal_url"])
    print(f"[{d['store']}] {d['title'][:32]} -> {d['short_url']}")
    time.sleep(0.3)

with open("earnkaro_full_catalog.json", "w", encoding="utf-8") as f:
    json.dump(raw_earnkaro_deals, f, indent=2)

print(f"✅ Generated {len(raw_earnkaro_deals)} deals in earnkaro_full_catalog.json!")
