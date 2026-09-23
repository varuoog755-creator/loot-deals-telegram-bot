import os
import re
import json
import logging
import asyncio
import urllib.request
import urllib.parse
from datetime import datetime

logging.basicConfig(level=logging.INFO, format="%(asctime)s [%(levelname)s] %(message)s")
logger = logging.getLogger("DealsIntelligence")

ENV_PATH = os.path.join(os.path.dirname(__file__), ".env")
DB_JSON_PATH = os.path.join(os.path.dirname(__file__), "DIRECTORIES_DATABASE.json")

def get_env_var(key: str, default: str = "") -> str:
    if os.path.exists(ENV_PATH):
        with open(ENV_PATH, "r", encoding="utf-8") as f:
            for line in f:
                if line.startswith(f"{key}="):
                    return line.strip().split("=", 1)[1].strip("\"'")
    return os.environ.get(key, default)

BOT_TOKEN = get_env_var("BOT_TOKEN")
ADMIN_ID = get_env_var("ADMIN_ID", "8837364917")
EARNKARO_REF = get_env_var("EARNKARO_REFERRAL", "1962062")

def send_telegram_alert(text: str, parse_mode: str = "HTML") -> bool:
    if not BOT_TOKEN or not ADMIN_ID:
        logger.error("Missing BOT_TOKEN or ADMIN_ID")
        return False
    url = f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage"
    payload = {
        "chat_id": ADMIN_ID,
        "text": text,
        "parse_mode": parse_mode,
        "disable_web_page_preview": False
    }
    data = urllib.parse.urlencode(payload).encode("utf-8")
    req = urllib.request.Request(url, data=data)
    try:
        with urllib.request.urlopen(req, timeout=10) as resp:
            data = json.loads(resp.read().decode())
            return data.get("ok", False)
    except Exception as e:
        logger.error(f"Error sending Telegram alert: {e}")
        return False

def fetch_desidime_deals(limit: int = 10) -> list:
    """Scrapes latest hot deals from DesiDime."""
    deals = []
    url = "https://www.desidime.com/new"
    headers = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64)"}
    try:
        req = urllib.request.Request(url, headers=headers)
        with urllib.request.urlopen(req, timeout=10) as resp:
            html = resp.read().decode("utf-8", errors="ignore")
            matches = re.findall(r'<a[^>]*href=[\"\\\'](/deals/[^\"\\\']+)[\"\\\'][^>]*>(.*?)</a>', html)
            seen = set()
            for path, title_html in matches:
                clean_title = re.sub(r'<[^>]+>', '', title_html).strip()
                if clean_title and path not in seen and len(clean_title) > 10:
                    seen.add(path)
                    deals.append({
                        "source": "DesiDime",
                        "title": clean_title,
                        "url": f"https://www.desidime.com{path}"
                    })
                    if len(deals) >= limit:
                        break
    except Exception as e:
        logger.error(f"Error scraping DesiDime: {e}")
    return deals

def fetch_freekaamaal_deals(limit: int = 10) -> list:
    """Scrapes live flash deals from FreeKaaMaal RSS feed."""
    deals = []
    url = "https://freekaamaal.com/feed"
    headers = {"User-Agent": "Mozilla/5.0"}
    try:
        req = urllib.request.Request(url, headers=headers)
        with urllib.request.urlopen(req, timeout=10) as resp:
            raw = resp.read().decode("utf-8", errors="ignore")
            items = re.findall(r'<item>(.*?)</item>', raw, re.DOTALL)
            for item in items[:limit]:
                title = re.search(r'<title>(.*?)</title>', item)
                link = re.search(r'<link>(.*?)</link>', item)
                if title and link:
                    clean_title = re.sub(r'<!\[CDATA\[(.*?)\]\]>', r'\1', title.group(1)).strip()
                    deals.append({
                        "source": "FreeKaaMaal",
                        "title": clean_title,
                        "url": link.group(1).strip()
                    })
    except Exception as e:
        logger.error(f"Error fetching FreeKaaMaal: {e}")
    return deals

def mask_deal_link(raw_url: str) -> str:
    """Creates a masked, affiliate-enabled link."""
    affiliate_url = f"https://earnkaro.com?r={EARNKARO_REF}&url={urllib.parse.quote(raw_url)}"
    try:
        tiny_api = f"https://tinyurl.com/api-create.php?url={urllib.parse.quote(affiliate_url)}"
        with urllib.request.urlopen(tiny_api, timeout=5) as res:
            return res.read().decode().strip()
    except Exception:
        return affiliate_url

if __name__ == "__main__":
    logger.info("Running Indian Deals Intelligence check...")
    dd_deals = fetch_desidime_deals(limit=5)
    fkm_deals = fetch_freekaamaal_deals(limit=5)
    logger.info(f"Retrieved {len(dd_deals)} DesiDime deals and {len(fkm_deals)} FKM deals.")
    print("Intelligence engine ready!")
