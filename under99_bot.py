import os
import sys
import logging
import urllib.parse
import urllib.request
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
import database

logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    level=logging.INFO
)
logger = logging.getLogger("Under99Bot")

NEW_TOKEN = None
env_path = os.path.join(os.path.dirname(__file__), "new_bot_env.txt")
if os.path.exists(env_path):
    with open(env_path) as f:
        for line in f:
            if line.startswith("NEW_BOT_TOKEN="):
                NEW_TOKEN = line.strip().split("=", 1)[1]
                break

BOT_TOKEN = os.getenv("UNDER99_BOT_TOKEN", NEW_TOKEN)
ADMIN_ID = int(os.getenv("ADMIN_ID", "8837364917"))
CHANNEL_LINK = "https://t.me/+vnry55FncIUxMDVl"

MAIN_KEYBOARD = [
    [KeyboardButton("⚡ Under ₹99 Steal Deals"), KeyboardButton("🔥 80-90% OFF Loots")],
    [KeyboardButton("🔍 Search Deals"), KeyboardButton("🏆 Referral Leaderboard")],
    [KeyboardButton("🎁 Refer & Earn (Free Gifts)"), KeyboardButton("👤 My Profile")],
    [KeyboardButton("❓ Help & Support")]
]

def get_main_markup():
    return ReplyKeyboardMarkup(MAIN_KEYBOARD, resize_keyboard=True)

def shorten_url(long_url: str) -> str:
    if not long_url:
        return "https://t.me/+vnry55FncIUxMDVl"
    try:
        api = f"https://tinyurl.com/api-create.php?url={urllib.parse.quote(long_url)}"
        req = urllib.request.Request(api, headers={"User-Agent": "Mozilla/5.0"})
        with urllib.request.urlopen(req, timeout=4) as res:
            if res.status == 200:
                return res.read().decode().strip()
    except Exception:
        pass
    return long_url

async def is_user_subscribed(user_id: int, context: ContextTypes.DEFAULT_TYPE) -> bool:
    channel = database.get_setting("channel")
    if not channel:
        return True
    try:
        member = await context.bot.get_chat_member(chat_id=channel, user_id=user_id)
        return member.status in [
            ChatMemberStatus.MEMBER,
            ChatMemberStatus.ADMINISTRATOR,
            ChatMemberStatus.OWNER
        ]
    except Exception:
        return True

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
            await context.bot.send_message(
                chat_id=ref_by,
                text=f"🎉 Badhai ho! Ek naye member ne aapke link se Under ₹99 Bot join kiya!\nTotal Invites: {ref_count}"
            )
        except Exception:
            pass

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
        [InlineKeyboardButton("📢 Join Main Deals Channel", url=CHANNEL_LINK)]
    ])
    await update.message.reply_text(welcome_text, reply_markup=get_main_markup(), parse_mode=ParseMode.HTML)
    await update.message.reply_text("⚡ <b>Instant Store:</b> Full screen deal store ke liye niche tap karein:", reply_markup=inline_nav, parse_mode=ParseMode.HTML)

async def under99_deals(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not update.message:
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
    if not update.message:
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
    if not update.message:
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

async def refer_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not update.message or not update.effective_user:
        return
    user_id = update.effective_user.id
    ref_link = f"https://t.me/Under99LootDeals_bot?start=ref_{user_id}"
    ref_count = database.get_referral_count(user_id)
    text = (
        "🎁 <b>REFER & EARN PROGRAM</b> 🎁\n\n"
        f"Aapka Personal Invite Link:\n<code>{ref_link}</code>\n\n"
        f"👥 Total Invites: <b>{ref_count} Members</b>\n\n"
        "• <b>3 Invites</b> ➔ VIP Glitch Deals Access\n"
        "• <b>10 Invites</b> ➔ Weekly ₹500 Amazon Gift Voucher"
    )
    wa_msg = urllib.parse.quote(f"🔥 Join Under 99 Loot Deals Bot for ₹1 to ₹99 deals: {ref_link}")
    wa_share = f"https://api.whatsapp.com/send?text={wa_msg}"
    tg_share = f"https://t.me/share/url?url={ref_link}&text={urllib.parse.quote('🔥 Join Under 99 Loot Deals Bot!')}"
    buttons = [
        [InlineKeyboardButton("🟢 Share on WhatsApp", url=wa_share)],
        [InlineKeyboardButton("📲 Share on Telegram", url=tg_share)]
    ]
    await update.message.reply_text(text, reply_markup=InlineKeyboardMarkup(buttons), parse_mode=ParseMode.HTML)

async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not update.message or not update.message.text:
        return
    text = update.message.text.strip()
    if text == "⚡ Under ₹99 Steal Deals":
        await under99_deals(update, context)
    elif text == "🔥 80-90% OFF Loots":
        await top_loots(update, context)
    elif text == "🔍 Search Deals":
        await update.message.reply_text("Type karein: <code>/search &lt;product&gt;</code> (Example: <code>/search watch</code>)", parse_mode=ParseMode.HTML)
    elif text == "🏆 Referral Leaderboard":
        await leaderboard_command(update, context)
    elif text == "🎁 Refer & Earn (Free Gifts)":
        await refer_command(update, context)
    elif text == "👤 My Profile":
        cnt = database.get_referral_count(update.effective_user.id)
        await update.message.reply_text(f"👤 <b>Aapka Profile</b>\nID: <code>{update.effective_user.id}</code>\nReferrals: <b>{cnt}</b>", parse_mode=ParseMode.HTML)
    elif text == "❓ Help & Support":
        await update.message.reply_text("Help ke liye /start dabayein ya channel join karein.", parse_mode=ParseMode.HTML)
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
    app.add_handler(CommandHandler("search", search_command))
    app.add_handler(CommandHandler("leaderboard", leaderboard_command))
    app.add_handler(CommandHandler("refer", refer_command))
    app.add_handler(MessageHandler(filters.TEXT & (~filters.COMMAND), handle_message))
    
    logger.info("⚡ Under 99 Loot Deals Bot started polling...")
    app.run_polling(drop_pending_updates=False)

if __name__ == "__main__":
    main()
