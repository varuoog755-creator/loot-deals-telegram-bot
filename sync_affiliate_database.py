import logging
from database import get_conn, init_db
from affiliate_engine import CURATED_AFFILIATE_DEALS, create_affiliate_deal_link

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("SyncAffiliateDB")

def sync_deals():
    init_db()
    with get_conn() as conn:
        cursor = conn.cursor()
        # Clear mock dummy deals
        cursor.execute("DELETE FROM deals")
        
        count = 0
        for item in CURATED_AFFILIATE_DEALS:
            aff = create_affiliate_deal_link(item["url"])
            aff_url = aff["affiliate_url"]
            cursor.execute(
                "INSERT INTO deals (title, price, mrp, discount, link, category) VALUES (?, ?, ?, ?, ?, ?)",
                (item["title"], item["price"], item["mrp"], item["discount"], aff_url, item["category"])
            )
            count += 1
            logger.info(f"Seeded: {item['title']} -> {aff_url}")
            
        conn.commit()
    print(f"Successfully synced {count} rich affiliate deals into SQLite database!")

if __name__ == "__main__":
    sync_deals()
