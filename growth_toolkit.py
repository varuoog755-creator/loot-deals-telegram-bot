"""
Growth Toolkit for Loot Deals Bot Ecosystem:
1. Discussion Group High-Value Deal Formatter (non-spammy value posts)
2. Channel Cross-Promotion (S4S / Shoutout Exchange Kit)
3. Viral Referral & Gamification Rewards Assistant
"""

import urllib.parse
from affiliate_engine import create_affiliate_deal_link

# 1. Discussion Group Value Post Generator
def format_discussion_group_post(deal_title: str, deal_price: str, mrp: str, original_url: str, bot_username: str = "Under99LootDeals_bot") -> str:
    """Formats a conversational, high-converting deal recommendation for public discussion groups."""
    aff_info = create_affiliate_deal_link(original_url)
    clean_url = aff_info["affiliate_url"]
    store = aff_info["store"]
    
    post = (
        f"⚡ <b>Bhai log, {store} par solid price drop / glitch mila hai:</b>\n\n"
        f"📦 <b>{deal_title}</b>\n"
        f"💰 <b>MRP:</b> <s>{mrp}</s> ➔ <b>Loot Price: {deal_price}</b>\n"
        f"🔗 <b>Direct Link:</b> {clean_url}\n\n"
        f"<i>(Price kisi bhi waqt badh sakta hai, jisko lena ho check kar lena!)</i>\n\n"
        f"👉 Daily ₹1 aur Under ₹99 hidden loots ke liye bot check karo: @{bot_username}"
    )
    return post

# 2. S4S (Share-for-Share) Outreach Pitch & Reciprocal Templates
def get_s4s_outreach_pitch(my_channel_link: str = "https://t.me/+vnry55FncIUxMDVl") -> str:
    """Cold outreach message to send to other channel admins for free cross-promotion."""
    pitch = (
        "Hey brother 👋\n\n"
        "Aapka Telegram channel check kiya, kaafi active community hai! "
        "Main bhi Indian shopping loot deals & cashback channel run kar raha hoon.\n\n"
        "Kya hum ek <b>Free 1-Hour / 24-Hour S4S (Cross-Promotion)</b> exchange kar sakte hain? "
        "Dono channels ki organic Indian audience cross-grow ho jayegi bina kisi cost ke.\n\n"
        f"Mera Channel: {my_channel_link}\n"
        "Agar interested ho toh batana, main ready-to-post message share kar deta hoon! 🤝"
    )
    return pitch

def get_s4s_promo_post(bot_username: str = "Under99LootDeals_bot", channel_link: str = "https://t.me/+vnry55FncIUxMDVl") -> str:
    """Eye-catching promotional post designed to be posted on partner channels."""
    promo = (
        "🔥 <b>BHAI LOG! KABHI MRP PAR ONLINE SHOPPING MAT KARO!</b> 🔥\n\n"
        "Kya aapko pata hai roz Amazon, Flipkart aur Myntra par <b>70% se 90% OFF</b> ke hidden price errors aur Under ₹99 loots aate hain jo 5-10 minute me khatam ho jate hain?\n\n"
        "⚡ <b>Is Telegram Bot par aapko milte hain:</b>\n"
        "📦 ₹1, ₹49 aur ₹99 ke Steal Deals Store\n"
        "📱 Electronics, T-Shirts, Earbuds par 85% Price Drops\n"
        "💰 Kisi bhi product link par Instant Cashback\n"
        "🎁 Friends invite karke ₹500 Amazon Voucher\n\n"
        f"👉 <b>Bot Launch Karein:</b> @{bot_username}\n"
        f"📢 <b>Official Channel Join Karein:</b> <a href='{channel_link}'><b>[TAP HERE TO JOIN]</b></a>\n\n"
        "<i>(Free for all Telegram users. Abhi join karo aur agla price glitch miss mat karo!)</i>"
    )
    return promo

# 3. Ready-Made High-Converting Deal Templates for Discussion Groups
SAMPLE_VALUE_SNIPPETS = [
    {
        "category": "Electronics & Cables",
        "title": "Fast Charging 65W Type-C Braided Cable (1.5 Meter)",
        "mrp": "₹499",
        "loot_price": "₹49",
        "url": "https://www.flipkart.com",
        "hook": "Bhai log jisko Type-C cable chahiye, Flipkart par 90% discount me ₹49 ki mil rahi hai!"
    },
    {
        "category": "Earbuds & Audio",
        "title": "Noise Pure Pods Wireless Earbuds (60H Battery)",
        "mrp": "₹2,999",
        "loot_price": "₹499",
        "url": "https://www.amazon.in",
        "hook": "Amazon par Noise earbuds ka solid price drop chal raha hai, ₹499 me mil rahe hain direct."
    },
    {
        "category": "Footwear",
        "title": "Puma / Campus Lightweight Running Shoes",
        "mrp": "₹3,499",
        "loot_price": "₹399",
        "url": "https://www.myntra.com",
        "hook": "Myntra secret glitch price: Running shoes flat ₹399 me live hain limited sizes me."
    }
]
