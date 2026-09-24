import sqlite3
import os

DB_PATH = os.path.join(os.path.dirname(__file__), "bot_data.db")

def get_conn():
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn

def init_db():
    with get_conn() as conn:
        cursor = conn.cursor()
        cursor.execute("""
        CREATE TABLE IF NOT EXISTS users (
            user_id INTEGER PRIMARY KEY,
            first_name TEXT,
            username TEXT,
            referred_by INTEGER,
            joined_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
        """)
        cursor.execute("""
        CREATE TABLE IF NOT EXISTS settings (
            key TEXT PRIMARY KEY,
            value TEXT
        )
        """)
        cursor.execute("""
        CREATE TABLE IF NOT EXISTS deals (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            title TEXT NOT NULL,
            price TEXT,
            mrp TEXT,
            discount TEXT,
            link TEXT NOT NULL,
            category TEXT DEFAULT 'Loot',
            image_url TEXT,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
        """)
        conn.commit()

        # Seed initial deals if empty
        cursor.execute("SELECT COUNT(*) FROM deals")
        if cursor.fetchone()[0] == 0:
            initial_deals = [
                ("Fastrack Smart Watch with BT Calling", "₹999", "₹3,995", "75% OFF", "https://tinyurl.com/2avn7vbq", "Loot"),
                ("Noise Buds VS102 Wireless Earbuds", "₹899", "₹2,999", "70% OFF", "https://tinyurl.com/2avn7vbq", "Loot"),
                ("Men Casual Slim Fit Cotton Shirt", "₹349", "₹1,499", "76% OFF", "https://tinyurl.com/2avn7vbq", "Loot"),
                ("Stainless Steel Water Bottle 1L", "₹89", "₹499", "82% OFF", "https://tinyurl.com/2avn7vbq", "Under99"),
                ("Mobile Phone Stand Holder for Desk", "₹49", "₹299", "83% OFF", "https://tinyurl.com/2avn7vbq", "Under99"),
                ("Braided Type-C Fast Charging Cable", "₹79", "₹399", "80% OFF", "https://tinyurl.com/2avn7vbq", "Under99"),
                ("Unisex Sports Running Shoes", "₹449", "₹1,999", "77% OFF", "https://tinyurl.com/2avn7vbq", "Loot")
            ]
            cursor.executemany(
                "INSERT INTO deals (title, price, mrp, discount, link, category) VALUES (?, ?, ?, ?, ?, ?)",
                initial_deals
            )
            conn.commit()

def add_user(user_id: int, first_name: str, username: str, referred_by: int = None):
    with get_conn() as conn:
        cursor = conn.cursor()
        cursor.execute("SELECT user_id FROM users WHERE user_id = ?", (user_id,))
        if not cursor.fetchone():
            cursor.execute(
                "INSERT INTO users (user_id, first_name, username, referred_by) VALUES (?, ?, ?, ?)",
                (user_id, first_name, username, referred_by)
            )
            conn.commit()
            return True # New user
        return False # Existing user

def get_user_count():
    with get_conn() as conn:
        cursor = conn.cursor()
        cursor.execute("SELECT COUNT(*) FROM users")
        return cursor.fetchone()[0]

def get_all_users():
    with get_conn() as conn:
        cursor = conn.cursor()
        cursor.execute("SELECT user_id FROM users")
        return [row[0] for row in cursor.fetchall()]

def get_referral_count(user_id: int):
    with get_conn() as conn:
        cursor = conn.cursor()
        cursor.execute("SELECT COUNT(*) FROM users WHERE referred_by = ?", (user_id,))
        return cursor.fetchone()[0]

def get_setting(key: str, default=None):
    with get_conn() as conn:
        cursor = conn.cursor()
        cursor.execute("SELECT value FROM settings WHERE key = ?", (key,))
        row = cursor.fetchone()
        return row[0] if row else default

def set_setting(key: str, value: str):
    with get_conn() as conn:
        cursor = conn.cursor()
        cursor.execute("INSERT OR REPLACE INTO settings (key, value) VALUES (?, ?)", (key, str(value)))
        conn.commit()

def add_deal(title: str, price: str, mrp: str, discount: str, link: str, category: str = "Loot"):
    with get_conn() as conn:
        cursor = conn.cursor()
        cursor.execute(
            "INSERT INTO deals (title, price, mrp, discount, link, category) VALUES (?, ?, ?, ?, ?, ?)",
            (title, price, mrp, discount, link, category)
        )
        conn.commit()

def get_user_wallet(user_id: int) -> dict:
    with get_conn() as conn:
        cursor = conn.cursor()
        cursor.execute("SELECT COUNT(*) FROM users WHERE referred_by = ?", (user_id,))
        ref_count = cursor.fetchone()[0]
        # ₹10 per referral virtual earnings incentive
        balance = ref_count * 10
        vip_unlocked = ref_count >= 3
        return {
            "referral_count": ref_count,
            "wallet_balance": balance,
            "vip_unlocked": vip_unlocked,
            "next_milestone": 3 if ref_count < 3 else (5 if ref_count < 5 else 10)
        }

def get_deals_by_category(category: str, limit: int = 10):
    with get_conn() as conn:
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM deals WHERE category = ? ORDER BY id DESC LIMIT ?", (category, limit))
        return [dict(row) for row in cursor.fetchall()]

def search_deals(query: str, limit: int = 5):
    with get_conn() as conn:
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM deals WHERE title LIKE ? ORDER BY id DESC LIMIT ?", (f"%{query}%", limit))
        return [dict(row) for row in cursor.fetchall()]

def get_referral_leaderboard(limit: int = 10):
    with get_conn() as conn:
        cursor = conn.cursor()
        cursor.execute("""
            SELECT u.user_id, u.first_name, u.username, COUNT(r.user_id) as ref_count
            FROM users u
            JOIN users r ON r.referred_by = u.user_id
            GROUP BY u.user_id
            ORDER BY ref_count DESC
            LIMIT ?
        """, (limit,))
        return [dict(row) for row in cursor.fetchall()]

init_db()
