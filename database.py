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

def get_recent_deals(limit: int = 5, category: str = None):
    with get_conn() as conn:
        cursor = conn.cursor()
        if category:
            cursor.execute("SELECT * FROM deals WHERE category = ? ORDER BY id DESC LIMIT ?", (category, limit))
        else:
            cursor.execute("SELECT * FROM deals ORDER BY id DESC LIMIT ?", (limit,))
        return [dict(row) for row in cursor.fetchall()]

init_db()
