import os
import sys
import logging
import urllib.parse
import urllib.request
import sqlite3
from telegram import (
    Update,
    InlineKeyboardButton,
    InlineKeyboardMarkup,
    ReplyKeyboardMarkup,
    KeyboardButton,
    WebAppInfo
)
from telegram.constants import ParseMode, ChatMemberStatus
from telegram.ext import (
    ApplicationBuilder,
    CommandHandler,
    MessageHandler,
    CallbackQueryHandler,
    ContextTypes,
    filters
)

logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    level=logging.INFO
)
logger = logging.getLogger("Under99Bot")

# Fallback DB and token loader
DB_PATH = os.path.join(os.path.dirname(__file__), "bot_data.db")

NEW_TOKEN = ""
token_file = os.path.join(os.path.dirname(__file__), "new_bot_env.txt")
if os.path.exists(token_file):
    try:
        with open(token_file, "r") as f:
            for line in f:
                if line.startswith("NEW_BOT_TOKEN="):
                    NEW_TOKEN = line.strip().split("=", 1)[1]
    except Exception:
        pass

BOT_TOKEN = os.getenv("UNDER99_BOT_TOKEN", NEW_TOKEN)
ADMIN_ID = int(os.getenv("ADMIN_ID", "8837364917"))
DEFAULT_CHANNEL_LINK = "https://t.me/+vnry55FncIUxMDVl"
MASKED_EARNKARO_LINK = "https://tinyurl.com/26gtkvfm"

# Local SQLite fallback for database module
try:
    import database
except ImportError:
    class MockDatabase:
        def get_conn(self):
            return sqlite3.connect(DB_PATH)
        def add_user(self, user_id, first_name, username, ref_by):
            try:
                conn = self.get_conn()
                c = conn.cursor()
                c.execute("INSERT OR IGNORE INTO users (user_id, first_name, username, referred_by) VALUES (?, ?, ?, ?)",
                          (user_id, first_name, username, ref_by))
                conn.commit()
                res = c.rowcount > 0
                conn.close()
                return res
            except Exception:
                return False
        def get_setting(self, key, default=None):
            try:
                conn = self.get_conn()
                c = conn.cursor()
                c.execute("CREATE TABLE IF NOT EXISTS settings (key TEXT PRIMARY KEY, value TEXT)")
                c.execute("SELECT value FROM settings WHERE key=?", (key,))
                row = c.fetchone()
                conn.close()
                return row[0] if row else default
            except Exception:
                return default
        def set_setting(self, key, value):
            try:
                conn = self.get_conn()
                c = conn.cursor()
                c.execute("CREATE TABLE IF NOT EXISTS settings (key TEXT PRIMARY KEY, value TEXT)")
                c.execute("INSERT OR REPLACE INTO settings (key, value) VALUES (?, ?)", (key, str(value)))
                conn.commit()
                conn.close()
            except Exception:
                pass
        def get_recent_deals(self, limit=5, category=None):
            try:
                conn = self.get_conn()
                c = conn.cursor()
                if category:
                    c.execute("SELECT title, price, mrp, discount, link, category FROM deals WHERE category=? ORDER BY id DESC LIMIT ?", (category, limit))
                else:
                    c.execute("SELECT title, price, mrp, discount, link, category FROM deals ORDER BY id DESC LIMIT ?", (limit,))
                rows = c.fetchall()
                conn.close()
                return [{"title": r[0], "price": r[1], "mrp": r[2], "discount": r[3], "link": r[4], "category": r[5]} for r in rows]
            except Exception:
                return []
        def search_deals(self, query, limit=5):
            try:
                conn = self.get_conn()
                c = conn.cursor()
                c.execute("SELECT title, price, mrp, discount, link, category FROM deals WHERE title LIKE ? ORDER BY id DESC LIMIT ?", (f"%{query}%", limit))
                rows = c.fetchall()
                conn.close()
                return [{"title": r[0], "price": r[1], "mrp": r[2], "discount": r[3], "link": r[4], "category": r[5]} for r in rows]
            except Exception:
                return []
        def get_referral_count(self, user_id):
            try:
                conn = self.get_conn()
                c = conn.cursor()
                c.execute("SELECT COUNT(*) FROM users WHERE referred_by=?", (user_id,))
                cnt = c.fetchone()[0]
                conn.close()
                return cnt
            except Exception:
                return 0
        def get_referral_leaderboard(self, limit=10):
            try:
                conn = self.get_conn()
                c = conn.cursor()
                c.execute("""
                    SELECT u.first_name, u.user_id, COUNT(r.user_id) as cnt
                    FROM users u
                    JOIN users r ON u.user_id = r.referred_by
                    GROUP BY u.user_id
                    ORDER BY cnt DESC
                    LIMIT ?
                """, (limit,))
                rows = c.fetchall()
                conn.close()
                return [{"first_name": r[0], "user_id": r[1], "ref_count": r[2]} for r in rows]
            except Exception:
                return []
    database = MockDatabase()

MAIN_KEYBOARD = [
    [KeyboardButton("⚡ Under ₹99 Steal Deals"), KeyboardButton("🔥 80-90% OFF Loots")],
    [KeyboardButton("🌟 VIP Secret Glitch Deals"), KeyboardButton("🎁 Refer & Win Free Rewards")],
    [KeyboardButton("🔍 Search Deals"), KeyboardButton("🏆 Referral Leaderboard")],
    [KeyboardButton("💰 Daily Cashback & Earning App"), KeyboardButton("👤 My Profile")]
]

def make_progress_bar(current: int, target: int = 3) -> str:
    current = max(0, current)
    filled = min(10, int((current / target) * 10))
    bar = "█" * filled + "░" * (10 - filled)
    return f"[{bar}] {current}/{target}"

def get_main_markup():
    return ReplyKeyboardMarkup(MAIN_KEYBOARD, resize_keyboard=True)

def shorten_url(long_url: str) -> str:
    if not long_url:
        return DEFAULT_CHANNEL_LINK
    try:
        api = f"https://tinyurl.com/api-create.php?url={urllib.parse.quote(long_url)}"
        req = urllib.request.Request(api, headers={"User-Agent": "Mozilla/5.0"})
        with urllib.request.urlopen(req, timeout=4) as res:
            if res.status == 200:
                return res.read().decode().strip()
    except Exception:
        pass
    return long_url

# Cache verified user IDs in memory & DB
VERIFIED_USERS = set([ADMIN_ID])

def is_verified_locally(user_id: int) -> bool:
    if user_id in VERIFIED_USERS:
        return True
    val = database.get_setting(f"verified_{user_id}")
    if val == "1":
        VERIFIED_USERS.add(user_id)
        return True
    return False

def mark_user_verified(user_id: int):
    VERIFIED_USERS.add(user_id)
    database.set_setting(f"verified_{user_id}", "1")

def get_active_channel_url():
    ch = database.get_setting("channel")
    if ch:
        if ch.startswith("http"):
            return ch
        clean = ch.replace("@", "")
        return f"https://t.me/{clean}"
    return DEFAULT_CHANNEL_LINK

async def is_user_subscribed(user_id: int, context: ContextTypes.DEFAULT_TYPE) -> bool:
    if user_id == ADMIN_ID or is_verified_locally(user_id):
        return True
    ch = database.get_setting("channel")
    if not ch:
        return False
    try:
        target = ch if ch.startswith("@") or ch.startswith("-100") else f"@{ch}"
        member = await context.bot.get_chat_member(chat_id=target, user_id=user_id)
        if member.status in [ChatMemberStatus.MEMBER, ChatMemberStatus.ADMINISTRATOR, ChatMemberStatus.OWNER]:
            mark_user_verified(user_id)
            return True
        return False
    except Exception as e:
        logger.warning(f"Subscription check error for {user_id} in {ch}: {e}")
        return is_verified_locally(user_id)

async def send_force_sub_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    channel_url = get_active_channel_url()
    first_name = update.effective_user.first_name if update.effective_user else "Dost"
    text = (
        f"🔒 <b>ACCESS LOCKED: Official Channel Join Zaroori Hai!</b>\n\n"
        f"Namaste {first_name}! 👋\n\n"
        f"Hamare bot se <b>Under ₹99 Steal Deals</b>, <b>₹1 Glitch Loots</b> aur daily price drops access karne ke liye pehle hamara Official Deals Channel join karna compulsory hai!\n\n"
        f"👉 <b>Kaise Unlock Karein:</b>\n"
        f"1️⃣ Niche <b>'📢 Join Deals Channel'</b> button par click karke channel join karein.\n"
        f"2️⃣ Phir <b>'✅ I Have Joined (Unlock Bot)'</b> button par tap karein!"
    )
    buttons = [
        [InlineKeyboardButton("📢 Join Deals Channel ⚡", url=channel_url)],
        [InlineKeyboardButton("✅ I Have Joined (Unlock Bot)", callback_data="verify_subscription")]
    ]
    markup = InlineKeyboardMarkup(buttons)
    if update.callback_query and update.callback_query.message:
        await update.callback_query.message.reply_text(text, reply_markup=markup, parse_mode=ParseMode.HTML)
    elif update.message:
        await update.message.reply_text(text, reply_markup=markup, parse_mode=ParseMode.HTML)

async def check_subscription_callback(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    if not query:
        return
    await query.answer()
    user_id = query.from_user.id
    ch = database.get_setting("channel")
    
    verified = False
    if ch and (ch.startswith("@") or ch.startswith("-100")):
        try:
            target = ch if ch.startswith("@") or ch.startswith("-100") else f"@{ch}"
            member = await context.bot.get_chat_member(chat_id=target, user_id=user_id)
            if member.status in [ChatMemberStatus.MEMBER, ChatMemberStatus.ADMINISTRATOR, ChatMemberStatus.OWNER]:
                verified = True
        except Exception:
            verified = True
    else:
        verified = True

    if verified:
        mark_user_verified(user_id)
        if query.message:
            try:
                await query.edit_message_text(
                    "🎉 <b>Badhai ho! Channel verify ho gaya hai!</b>\n\n"
                    "Aapka bot access ab permanently UNLOCKED hai! Niche diye gaye menu se deals browse karna shuru karein 👇",
                    parse_mode=ParseMode.HTML
                )
            except Exception:
                pass
        welcome_text = (
            f"⚡ <b>Under ₹99 Deals Store Me Aapka Swagat Hai!</b> ⚡\n\n"
            "📦 <b>₹1, ₹49 aur ₹99 ke Steal Deals</b> (Amazon, Flipkart, Meesho, Myntra)\n"
            "🔥 <b>80% se 90% Discount Price Error Glitches</b>\n"
            "🎁 <b>Free Delivery & Daily Cashback Offers</b>\n\n"
            "Menu buttons se deal chunein 👇"
        )
        inline_nav = InlineKeyboardMarkup([
            [InlineKeyboardButton("🛍️ Open Deals Mini App", web_app=WebAppInfo(url="https://loot-deals-telegram-bot.onrender.com/"))],
            [InlineKeyboardButton("📢 Deals Channel", url=get_active_channel_url())]
        ])
        await context.bot.send_message(
            chat_id=user_id,
            text=welcome_text,
            reply_markup=get_main_markup(),
            parse_mode=ParseMode.HTML
        )
        await context.bot.send_message(
            chat_id=user_id,
            text="⚡ <b>Instant Deals Mini App:</b>",
            reply_markup=inline_nav,
            parse_mode=ParseMode.HTML
        )
    else:
        await query.answer("❌ Pehle channel join karein, phir verify button dabayein!", show_alert=True)

async def start_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not update.effective_user or not update.message:
        return
    user = update.effective_user
    user_id = user.id
    first_name = user.first_name or "Friend"
    username = user.username or ""

    ref_by = None
    if context.args:
        try:
            arg = context.args[0].replace("ref_", "")
            potential_ref = int(arg)
            if potential_ref != user_id:
                ref_by = potential_ref
        except ValueError:
            pass

    is_new = database.add_user(user_id, first_name, username, ref_by)
    if is_new and ref_by:
        try:
            ref_count = database.get_referral_count(ref_by)
            needed = max(0, 3 - ref_count)
            if ref_count >= 3:
                msg = (
                    f"🎉 <b>BOOM! Naya Referral Aaya!</b> 🎉\n\n"
                    f"Aapke friend <b>{first_name}</b> ne aapke link se bot join kar liya hai!\n\n"
                    f"👥 Aapke Total Invites: <b>{ref_count}</b>\n"
                    f"🌟 <b>Badhai Ho! Aapka VIP Secret Glitch Deals access ab UNLOCKED hai!</b>\n\n"
                    f"VIP Deals dekhne ke liye bot me <b>'🌟 VIP Secret Glitch Deals'</b> button dabayein!"
                )
            else:
                msg = (
                    f"🔔 <b>BOOM! Naya Referral Aaya!</b> 🎉\n\n"
                    f"Aapke friend <b>{first_name}</b> ne aapke link se bot join kar liya hai!\n\n"
                    f"👥 Aapke Total Invites: <b>{ref_count}</b>\n"
                    f"🎯 VIP Secret Deals unlock karne ke liye bas <b>{needed} invite</b> bache hain!\n\n"
                    f"Apna link WhatsApp aur groups par aur share karein!"
                )
            await context.bot.send_message(chat_id=ref_by, text=msg, parse_mode=ParseMode.HTML)
        except Exception as e:
            logger.warning(f"Could not notify referrer {ref_by}: {e}")

    # FORCE-SUBSCRIBE CHECK
    sub = await is_user_subscribed(user_id, context)
    if not sub:
        await send_force_sub_message(update, context)
        return

    welcome_text = (
        f"⚡ <b>Namaste {first_name}! Welcome to Under ₹99 Loot Deals</b> ⚡\n\n"
        "India ka sabse sasta budget shopping bot!\n\n"
        "📦 <b>₹1, ₹49 aur ₹99 ke Steal Deals</b> (Amazon, Flipkart, Meesho, Myntra)\n"
        "🔥 <b>80% se 90% Discount Price Error Glitches</b>\n"
        "🎁 <b>Free Delivery & Daily Cashback Offers</b>\n\n"
        "Niche diye gaye buttons se browsing shuru karein 👇"
    )
    inline_nav = InlineKeyboardMarkup([
        [InlineKeyboardButton("🛍️ Open Deals Mini App", web_app=WebAppInfo(url="https://loot-deals-telegram-bot.onrender.com/"))],
        [InlineKeyboardButton("📢 Main Deals Channel", url=get_active_channel_url())]
    ])
    await update.message.reply_text(welcome_text, reply_markup=get_main_markup(), parse_mode=ParseMode.HTML)
    await update.message.reply_text("⚡ <b>Instant Store:</b> Full screen deal store ke liye niche tap karein:", reply_markup=inline_nav, parse_mode=ParseMode.HTML)

async def under99_deals(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not update.message or not update.effective_user:
        return
    user_id = update.effective_user.id
    if not await is_user_subscribed(user_id, context):
        await send_force_sub_message(update, context)
        return

    deals = database.get_recent_deals(limit=5, category="Under99")
    if not deals:
        deals = database.get_recent_deals(limit=5)
    
    text = "⚡ <b>UNDER ₹99 STEAL DEALS (Limited Stock)</b> ⚡\n\n"
    buttons = []
    for idx, d in enumerate(deals, 1):
        clean_link = shorten_url(d.get('link', ''))
        title = d.get('title', 'Deal')
        price = d.get('price', '₹99')
        mrp = d.get('mrp', '')
        text += (
            f"<b>{idx}. {title}</b>\n"
            f"💰 Steal Price: <b>{price}</b> (MRP: {mrp})\n"
            f"🔗 <a href='{clean_link}'>Claim Deal Now</a>\n\n"
        )
        buttons.append([InlineKeyboardButton(f"👉 Grab #{idx} ({price})", url=clean_link)])
    
    text += "⚠️ <i>Deals jaldi out of stock ho sakti hain!</i>"
    await update.message.reply_text(text, reply_markup=InlineKeyboardMarkup(buttons), parse_mode=ParseMode.HTML, disable_web_page_preview=True)

async def top_loots(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not update.message or not update.effective_user:
        return
    user_id = update.effective_user.id
    if not await is_user_subscribed(user_id, context):
        await send_force_sub_message(update, context)
        return

    deals = database.get_recent_deals(limit=5, category="Loot")
    if not deals:
        deals = database.get_recent_deals(limit=5)
    
    text = "🔥 <b>TODAY'S 80-90% OFF LOOT DEALS</b> 🔥\n\n"
    buttons = []
    for idx, d in enumerate(deals, 1):
        clean_link = shorten_url(d.get('link', ''))
        title = d.get('title', 'Deal')
        price = d.get('price', '')
        mrp = d.get('mrp', '')
        discount = d.get('discount', '80% OFF')
        text += (
            f"<b>{idx}. {title}</b>\n"
            f"💰 Loot Price: <b>{price}</b> (MRP: {mrp}) — <b>{discount}</b>\n"
            f"🔗 <a href='{clean_link}'>Buy Now</a>\n\n"
        )
        buttons.append([InlineKeyboardButton(f"👉 Grab Deal #{idx}", url=clean_link)])
        
    await update.message.reply_text(text, reply_markup=InlineKeyboardMarkup(buttons), parse_mode=ParseMode.HTML, disable_web_page_preview=True)

async def search_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not update.message or not update.effective_user:
        return
    user_id = update.effective_user.id
    if not await is_user_subscribed(user_id, context):
        await send_force_sub_message(update, context)
        return

    query = " ".join(context.args) if context.args else ""
    if not query:
        await update.message.reply_text("🔍 Product search ke liye likhein: <code>/search tshirt</code> ya <code>/search watch</code>", parse_mode=ParseMode.HTML)
        return
    deals = database.search_deals(query, limit=5)
    if not deals:
        await update.message.reply_text(f"❌ <b>'{query}'</b> ke liye koi deals nahi mili. Dusra keyword try karein.", parse_mode=ParseMode.HTML)
        return
    await update.message.reply_text(f"🔍 <b>Search Results for '{query}':</b>", parse_mode=ParseMode.HTML)
    for d in deals:
        clean_link = shorten_url(d.get('link', ''))
        msg = f"🔥 <b>{d.get('title')}</b>\n💰 Price: {d.get('price')} (MRP: {d.get('mrp')})\n⚡ {d.get('discount')}\n👉 <a href='{clean_link}'>Buy Now</a>"
        buttons = [[InlineKeyboardButton("🛍️ Buy Now", url=clean_link)]]
        await update.message.reply_text(msg, reply_markup=InlineKeyboardMarkup(buttons), parse_mode=ParseMode.HTML, disable_web_page_preview=True)

async def leaderboard_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not update.message:
        return
    leaders = database.get_referral_leaderboard(10)
    if not leaders:
        await update.message.reply_text("🏆 Leaderboard par abhi koi user nahi hai. Sabse pehle apne dosto ko invite karein!", parse_mode=ParseMode.HTML)
        return
    text = "🏆 <b>TOP 10 REFERRAL CHAMPIONS</b> 🏆\n\n"
    medals = ["🥇", "🥈", "🥉", "4️⃣", "5️⃣", "6️⃣", "7️⃣", "8️⃣", "9️⃣", "🔟"]
    for idx, r in enumerate(leaders):
        badge = medals[idx] if idx < len(medals) else f"#{idx+1}"
        name = r.get('first_name') or 'User'
        cnt = r.get('ref_count', 0)
        text += f"{badge} <b>{name}</b> — <b>{cnt} Invites</b>\n"
    await update.message.reply_text(text, parse_mode=ParseMode.HTML)

async def vip_deals(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not update.message or not update.effective_user:
        return
    user_id = update.effective_user.id
    if not await is_user_subscribed(user_id, context):
        await send_force_sub_message(update, context)
        return

    ref_count = database.get_referral_count(user_id)
    if ref_count < 3 and user_id != ADMIN_ID:
        needed = 3 - ref_count
        bot_uname = (await context.bot.get_me()).username or "Under99LootDeals_bot"
        ref_link = f"https://t.me/{bot_uname}?start=ref_{user_id}"
        wa_text = urllib.parse.quote(f"🔥 Bhai ye Telegram Bot try karo! ₹1 aur ₹99 ke secret loot deals milte hain: {ref_link}")
        tg_text = urllib.parse.quote(f"🔥 Join Under 99 Loot Deals Bot for Secret Price Glitches: {ref_link}")
        buttons = [
            [InlineKeyboardButton("🟢 Share on WhatsApp (Unlock VIP)", url=f"https://api.whatsapp.com/send?text={wa_text}")],
            [InlineKeyboardButton("📲 Share on Telegram", url=f"https://t.me/share/url?url={ref_link}&text={tg_text}")],
            [InlineKeyboardButton("🔄 Refresh Status", callback_data="check_vip_status")]
        ]
        progress = make_progress_bar(ref_count, 3)
        text = (
            "🔒 <b>VIP SECRET GLITCH DEALS: ACCESS LOCKED</b>\n\n"
            "Yeh 90-95% OFF price error glitches sirf hamare <b>VIP Members</b> ke liye hain!\n\n"
            f"📊 <b>Aapka Progress:</b> {progress}\n"
            f"🎯 <b>Status:</b> {ref_count}/3 Friends Invited\n"
            f"⚡ <b>Sirf {needed} aur friend</b> ko invite karein aur instantly VIP Glitch Deals unlock karein!\n\n"
            "Niche WhatsApp button par click karke dosto ya groups me share karein 👇"
        )
        await update.message.reply_text(text, reply_markup=InlineKeyboardMarkup(buttons), parse_mode=ParseMode.HTML)
        return

    # User is VIP!
    deals = database.get_recent_deals(limit=5, category="Loot")
    if not deals:
        deals = database.get_recent_deals(limit=5)
    text = (
        "🌟 <b>VIP SECRET GLITCH DEALS UNLOCKED!</b> 🌟\n\n"
        "👑 <i>Congratulations VIP Member! Yahan hain aaj ki secret 85-95% OFF price error loot deals:</i>\n\n"
    )
    buttons = []
    for idx, d in enumerate(deals, 1):
        clean_link = shorten_url(d.get('link', ''))
        title = d.get('title', 'Deal')
        price = d.get('price', '')
        mrp = d.get('mrp', '')
        text += (
            f"<b>{idx}. {title}</b>\n"
            f"💰 VIP Loot: <b>{price}</b> (MRP: {mrp}) 🔥 <b>90% GLITCH OFF</b>\n"
            f"🔗 <a href='{clean_link}'>Grab VIP Steal Now</a>\n\n"
        )
        buttons.append([InlineKeyboardButton(f"⚡ Grab VIP #{idx} ({price})", url=clean_link)])
    text += "⚠️ <i>VIP deals stock jaldi khatam ho jata hai, turant claim karein!</i>"
    await update.message.reply_text(text, reply_markup=InlineKeyboardMarkup(buttons), parse_mode=ParseMode.HTML, disable_web_page_preview=True)

async def check_vip_status_callback(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    if not query:
        return
    user_id = query.from_user.id
    ref_count = database.get_referral_count(user_id)
    if ref_count >= 3 or user_id == ADMIN_ID:
        await query.answer("🎉 Badhai ho! Aapka VIP Access UNLOCKED hai!", show_alert=True)
        # Call VIP deals
        deals = database.get_recent_deals(limit=5)
        text = "🌟 <b>VIP SECRET GLITCH DEALS UNLOCKED!</b> 🌟\n\n"
        buttons = []
        for idx, d in enumerate(deals, 1):
            clean_link = shorten_url(d.get('link', ''))
            buttons.append([InlineKeyboardButton(f"⚡ Grab VIP #{idx} ({d.get('price', '')})", url=clean_link)])
        if query.message:
            await query.message.reply_text(text, reply_markup=InlineKeyboardMarkup(buttons), parse_mode=ParseMode.HTML)
    else:
        needed = 3 - ref_count
        await query.answer(f"🔒 Abhi aapke {ref_count}/3 invites hain. Bas {needed} aur invite karein!", show_alert=True)

async def refer_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not update.message or not update.effective_user:
        return
    user_id = update.effective_user.id
    if not await is_user_subscribed(user_id, context):
        await send_force_sub_message(update, context)
        return
    bot_uname = (await context.bot.get_me()).username or "Under99LootDeals_bot"
    ref_link = f"https://t.me/{bot_uname}?start=ref_{user_id}"
    ref_count = database.get_referral_count(user_id)
    progress_vip = make_progress_bar(ref_count, 3)

    text = (
        "🎁 <b>VIRAL REFER & EARN PROGRAM</b> 🎁\n\n"
        "Apne dosto aur WhatsApp groups mein apna personal invite link share karein aur rewards payen!\n\n"
        f"👥 Total Invites: <b>{ref_count} Members</b>\n"
        f"📊 VIP Progress: <b>{progress_vip}</b>\n\n"
        "🎯 <b>Milestone Incentives & Rewards:</b>\n"
        f"• <b>3 Invites:</b> 🌟 VIP Secret Glitch Deals Unlocked (95% OFF)\n"
        f"• <b>5 Invites:</b> ⚡ ₹50 Welcome Bonus / Instant Cash Reward\n"
        f"• <b>10 Invites:</b> 🏆 Weekly ₹500 Amazon Gift Voucher Lucky Draw\n\n"
        "🔗 <b>Aapka Personal Invite Link:</b>\n"
        f"<code>{ref_link}</code>\n\n"
        "👉 <i>Direct WhatsApp ya Telegram par share karne ke liye niche buttons dabayein:</i>"
    )
    wa_msg = urllib.parse.quote(f"🔥 Bhai ye check karo! India ka best Under ₹99 Loot Deals Telegram Bot! ₹1, ₹49 & ₹99 ke deals milte hain: {ref_link}")
    tg_msg = urllib.parse.quote(f"🔥 Join Under 99 Loot Deals Bot for ₹1-₹99 deals: {ref_link}")
    buttons = [
        [InlineKeyboardButton("🟢 Share on WhatsApp", url=f"https://api.whatsapp.com/send?text={wa_msg}")],
        [InlineKeyboardButton("📲 Share on Telegram", url=f"https://t.me/share/url?url={ref_link}&text={tg_msg}")],
        [InlineKeyboardButton("🌟 Check VIP Deals Status", callback_data="check_vip_status")]
    ]
    await update.message.reply_text(text, reply_markup=InlineKeyboardMarkup(buttons), parse_mode=ParseMode.HTML)

async def earnkaro_info(update: Update, context: ContextTypes.DEFAULT_TYPE):
    text = (
        "💰 <b>Ghar Baithe Paise Kamayein (Cashback & Earning App)</b> 💰\n\n"
        "Kya aap bhi online shopping deals aur budget loots share karke mahine ke ₹10,000–₹30,000 kamana chahte hain?\n\n"
        "1️⃣ <b>Cashback App Free Me Join Karein</b>\n"
        "2️⃣ Amazon, Flipkart, Myntra ka koi bhi deal link convert karein\n"
        "3️⃣ WhatsApp & Telegram groups mein share karein\n"
        "4️⃣ Jab koi buy karega, seedha aapke bank account mein commission / cashback aayega!\n\n"
        "🎁 <b>Special Welcome Bonus:</b> Abhi free register karne par <b>₹50 Real Cash Bonus</b> milta hai!\n\n"
        "👉 <b>Free Account Banane Ke Liye Niche Button Par Click Karein:</b>"
    )
    buttons = [
        [InlineKeyboardButton("🚀 Activate Free Cashback Account (₹50 Bonus)", url=MASKED_EARNKARO_LINK)],
        [InlineKeyboardButton("🟢 Share with Friends on WhatsApp", url=f"https://api.whatsapp.com/send?text={urllib.parse.quote('Ghar baithe shopping aur deals share karke extra cashback kamayein: ' + MASKED_EARNKARO_LINK)}")]
    ]
    if update.message:
        await update.message.reply_text(text, reply_markup=InlineKeyboardMarkup(buttons), parse_mode=ParseMode.HTML)

async def admin_set_channel(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not update.effective_user or update.effective_user.id != ADMIN_ID:
        return
    if not context.args:
        await update.message.reply_text("Usage: `/setchannel @YourChannel` ya `/setchannel -100xxxxxxxxxx`", parse_mode=ParseMode.MARKDOWN)
        return
    ch = context.args[0].strip()
    database.set_setting("channel", ch)
    await update.message.reply_text(
        f"✅ <b>Active Channel Updated:</b> <code>{ch}</code>\n\n"
        "Ab sabhi users ko pehle ye channel join karna compulsory hoga!",
        parse_mode=ParseMode.HTML
    )

async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not update.message or not update.message.text or not update.effective_user:
        return
    user_id = update.effective_user.id
    text = update.message.text.strip()
    
    # Common commands that don't need force-sub
    if text == "❓ Help & Support":
        await update.message.reply_text(
            f"ℹ️ <b>Under 99 Deals Bot Support</b>\n\n"
            f"Official Deals Channel: {get_active_channel_url()}\n"
            f"Kisi bhi madad ke liye channel join karein!",
            parse_mode=ParseMode.HTML
        )
        return
    elif text in ["💰 Daily Cashback & Earning App", "💰 Earn Money Online"]:
        await earnkaro_info(update, context)
        return

    # Force sub check for deals actions
    if not await is_user_subscribed(user_id, context):
        await send_force_sub_message(update, context)
        return

    if text == "⚡ Under ₹99 Steal Deals":
        await under99_deals(update, context)
    elif text == "🔥 80-90% OFF Loots":
        await top_loots(update, context)
    elif text in ["🌟 VIP Secret Glitch Deals", "🌟 VIP Secret Deals"]:
        await vip_deals(update, context)
    elif text == "🔍 Search Deals":
        await update.message.reply_text("Type karein: <code>/search &lt;product&gt;</code> (Example: <code>/search watch</code>)", parse_mode=ParseMode.HTML)
    elif text == "🏆 Referral Leaderboard":
        await leaderboard_command(update, context)
    elif text in ["🎁 Refer & Win Free Rewards", "🎁 Refer & Earn (Free Gifts)", "🎁 Refer & Earn"]:
        await refer_command(update, context)
    elif text == "👤 My Profile":
        cnt = database.get_referral_count(user_id)
        vip_status = "✅ UNLOCKED (Gold VIP)" if cnt >= 3 or user_id == ADMIN_ID else "❌ Locked (Need 3 Invites)"
        await update.message.reply_text(
            f"👤 <b>Aapka Profile</b>\n\n"
            f"• <b>User ID:</b> <code>{user_id}</code>\n"
            f"• <b>Total Referrals:</b> <b>{cnt} Members</b>\n"
            f"• <b>VIP Glitch Deals:</b> {vip_status}\n\n"
            "Dosto ko invite karne ke liye <b>'🎁 Refer & Win Free Rewards'</b> dabayein!",
            parse_mode=ParseMode.HTML
        )
    else:
        await update.message.reply_text("Niche menu se option chunein 👇", reply_markup=get_main_markup())

def main():
    if not BOT_TOKEN:
        logger.error("BOT_TOKEN is missing!")
        sys.exit(1)
    
    app = ApplicationBuilder().token(BOT_TOKEN).build()
    app.add_handler(CommandHandler("start", start_command))
    app.add_handler(CommandHandler("today", top_loots))
    app.add_handler(CommandHandler("under99", under99_deals))
    app.add_handler(CommandHandler("vip", vip_deals))
    app.add_handler(CommandHandler("search", search_command))
    app.add_handler(CommandHandler("leaderboard", leaderboard_command))
    app.add_handler(CommandHandler("refer", refer_command))
    app.add_handler(CommandHandler("earn", earnkaro_info))
    app.add_handler(CommandHandler("setchannel", admin_set_channel))
    app.add_handler(CallbackQueryHandler(check_subscription_callback, pattern="^verify_subscription$"))
    app.add_handler(CallbackQueryHandler(check_vip_status_callback, pattern="^check_vip_status$"))
    app.add_handler(MessageHandler(filters.TEXT & (~filters.COMMAND), handle_message))
    
    logger.info("⚡ Under 99 Loot Deals Bot started polling with Force-Subscribe...")
    app.run_polling(drop_pending_updates=False)

if __name__ == "__main__":
    main()
