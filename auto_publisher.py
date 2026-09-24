import os
import re
import time
import json
import logging
import asyncio
import urllib.request
import urllib.parse
from datetime import datetime
from dotenv import load_dotenv
from affiliate_engine import create_affiliate_deal_link

load_dotenv()

logging.basicConfig(level=logging.INFO, format="%(asctime)s [%(levelname)s] %(message)s")
logger = logging.getLogger("AutoPublisher")

BOT_TOKEN = os.getenv("BOT_TOKEN")
ADMIN_ID = int(os.getenv("ADMIN_ID", "8837364917"))
CHANNEL_USERNAME = os.getenv("CHANNEL_USERNAME", "")
EARNKARO_REF = os.getenv("EARNKARO_REFERRAL", "https://earnkaro.com?r=1962062")

def shorten_url(long_url: str) -> str:
    try:
        api = f"https://tinyurl.com/api-create.php?url={urllib.parse.quote(long_url)}"
        req = urllib.request.Request(api, headers={"User-Agent": "Mozilla/5.0"})
        with urllib.request.urlopen(req, timeout=5) as res:
            if res.status == 200:
                return res.read().decode().strip()
    except Exception:
        pass
    return long_url

def fetch_desidime_deals():
    deals = []
    try:
        url = "https://www.desidime.com/new"
        req = urllib.request.Request(url, headers={"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64)"})
        html = urllib.request.urlopen(req, timeout=10).read().decode('utf-8', errors='ignore')
        
        # Extract title and link patterns
        items = re.findall(r'href=[\'"](/deals/[^\'"]+)[\'"][^>]*>([^<]+)</a>', html)
        seen = set()
        for link, title in items:
            title = title.strip()
            if len(title) > 15 and title not in seen:
                seen.add(title)
                deals.append({
                    "title": title,
                    "url": f"https://www.desidime.com{link}",
                    "source": "DesiDime"
                })
                if len(deals) >= 10:
                    break
    except Exception as e:
        logger.error(f"Error fetching DesiDime deals: {e}")
    return deals

def send_telegram_channel_deal(bot_token: str, chat_id: str, deal: dict):
    title = deal["title"]
    source_url = deal["url"]
    
    # Advanced affiliate conversion engine
    deal_info = create_affiliate_deal_link(source_url)
    clean_buy_link = deal_info["affiliate_url"]
    store_name = deal_info["store"]
    store_icon = deal_info["icon"]
    cashback_rate = deal_info["cashback_rate"]
    
    wa_share = f"https://api.whatsapp.com/send?text={urllib.parse.quote(f'🔥 Loot Deal on {store_name}: {title} 👉 {clean_buy_link}')}"
    
    msg_html = (
        f"🔥 <b>FLASH LOOT DEAL ALERT!</b> 🔥\n\n"
        f"📦 <b>{title}</b>\n\n"
        f"🏬 <b>Store:</b> {store_icon} {store_name}\n"
        f"💰 <b>Cashback Rate:</b> <b>{cashback_rate}</b>\n"
        f"⚡ <i>Special Discounted Offer Live Now! Grab before stock ends.</i>\n\n"
        f"👉 <a href='{clean_buy_link}'><b>[TAP HERE TO BUY NOW]</b></a>\n\n"
        f"━━━━━━━━━━━━━━━━━━━\n"
        f"📲 <a href='{wa_share}'><b>[Share Deal on WhatsApp]</b></a>\n"
        f"🤖 Under ₹99: @Under99LootDeals_bot | ⚡ All Deals: @Roxk755_bot\n"
        f"📢 <a href='https://t.me/+vnry55FncIUxMDVl'><b>Join Deals Channel</b></a>"
    )
    
    url = f"https://api.telegram.org/bot{bot_token}/sendMessage"
    payload = {
        "chat_id": chat_id,
        "text": msg_html,
        "parse_mode": "HTML",
        "disable_web_page_preview": False
    }
    
    try:
        data = json.dumps(payload).encode("utf-8")
        req = urllib.request.Request(url, data=data, headers={"Content-Type": "application/json"})
        with urllib.request.urlopen(req, timeout=10) as res:
            res_data = json.loads(res.read().decode())
            return res_data.get("ok", False)
    except Exception as e:
        logger.error(f"Failed to post to channel: {e}")
        return False

def run_auto_publisher_cycle():
    logger.info("Starting automated deal publishing cycle...")
    deals = fetch_desidime_deals()
    logger.info(f"Discovered {len(deals)} candidate deals from Indian feeds.")
    
    # If channel is set or broadcast to admin for preview
    target_chat = CHANNEL_USERNAME if CHANNEL_USERNAME else str(ADMIN_ID)
    logger.info(f"Target destination: {target_chat}")
    
    posted_count = 0
    for d in deals[:3]: # Post top 3 high quality deals per cycle
        ok = send_telegram_channel_deal(BOT_TOKEN, target_chat, d)
        if ok:
            posted_count += 1
            logger.info(f"Successfully posted: {d['title']}")
            time.sleep(2)
            
    logger.info(f"Cycle completed. Posted {posted_count} deals.")
    return posted_count

if __name__ == "__main__":
    run_auto_publisher_cycle()
