import os
import sys
import logging
import asyncio
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

# Load token from new_bot_env.txt or environment
NEW_TOKEN = None
if os.path.exists("new_bot_env.txt"):
    with open("new_bot_env.txt") as f:
        for line in f:
            if line.startswith("NEW_BOT_TOKEN="):
                NEW_TOKEN = line.strip().split("=", 1)[1]
                break

BOT_TOKEN = os.getenv("UNDER99_BOT_TOKEN", NEW_TOKEN)
ADMIN_ID = int(os.getenv("ADMIN_ID", "8837364917"))
EARNKARO_REF = os.getenv("EARNKARO_REFERRAL", "https://earnkaro.com?r=1962062")

MAIN_KEYBOARD = [
    [KeyboardButton("⚡ Under ₹99 Steal Deals"), KeyboardButton("🔥 80-90% OFF Loots")],
    [KeyboardButton("🔍 Search Deals"), KeyboardButton("🏆 Referral Leaderboard")],
    [KeyboardButton("🎁 Refer & Earn (Free Gifts)"), KeyboardButton("👤 My Profile")],
    [KeyboardButton("❓ Help & Support")]
]

def get_main_markup():
    return ReplyKeyboardMarkup(MAIN_KEYBOARD, resize_keyboard=True)

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

def urllib_quote(text: str):
    return urllib.parse.quote(text)

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
    user = update.effective_user
    user_id = user.id
    first_name = user.first_name or "Friend"
    username = user.username or ""

    ref_by = None
    if context.args:
        try:
            potential_ref = int(context.args[0])
            if potential_ref != user_id:
                ref_by = potential_ref
        except ValueError:
            pass

    database.add_user(user_id, username, first_name, ref_by)

    welcome_text = (
        f"⚡ **Namaste {first_name}! Welcome to Under ₹99 Loot Deals** ⚡\n\n"
        "India ka sabse sasta budget shopping bot!\n"
        "📦 **₹1, ₹49 aur ₹99 ke Steal Deals** (Amazon, Flipkart, Meesho, Myntra)\n"
        "🔥 **80% se 90% Discount Price Error Glitches**\n"
        "🎁 **Free Delivery & Daily Cashback Offers**\n\n"
        "Niche diye gaye buttons se browsing shuru karein 👇"
    )
    inline_nav = InlineKeyboardMarkup([
        [InlineKeyboardButton("🛍️ Open Deals Mini App", web_app=WebAppInfo(url="https://loot-deals-telegram-bot.onrender.com/"))]
    ])
    await update.message.reply_text(welcome_text, reply_markup=get_main_markup(), parse_mode=ParseMode.MARKDOWN)
    await update.message.reply_text("⚡ **Instant Access:** Full screen deal store open karne ke liye tap karein 👇", reply_markup=inline_nav, parse_mode=ParseMode.MARKDOWN)

async def under99_deals(update: Update, context: ContextTypes.DEFAULT_TYPE):
    deals = database.get_recent_deals(limit=6, category="Under99")
    if not deals:
        deals = database.get_recent_deals(limit=6)
    
    text = "⚡ **UNDER ₹99 STEAL DEALS (Limited Stock)** ⚡\n\n"
    buttons = []
    for idx, d in enumerate(deals, 1):
        clean_link = shorten_url(d['link'])
        text += (
            f"**{idx}. {d['title']}**\n"
            f"💰 Steal Price: **{d['price']}** ~({d['mrp']})~\n"
            f"🔗 [Claim Under ₹99 Now]({clean_link})\n\n"
        )
        buttons.append([InlineKeyboardButton(f"👉 Grab #{idx} ({d['price']})", url=clean_link)])
    
    text += "⚠️ *Deals jaldi khatam ho sakti hain!*"
    await update.message.reply_text(text, reply_markup=InlineKeyboardMarkup(buttons), parse_mode=ParseMode.MARKDOWN, disable_web_page_preview=True)

async def top_loots(update: Update, context: ContextTypes.DEFAULT_TYPE):
    deals = database.get_recent_deals(limit=5, category="Loot")
    if not deals:
        deals = database.get_recent_deals(limit=5)
    
    text = "🔥 **TODAY'S 80-90% OFF LOOT DEALS** 🔥\n\n"
    buttons = []
    for idx, d in enumerate(deals, 1):
        clean_link = shorten_url(d['link'])
        text += (
            f"**{idx}. {d['title']}**\n"
            f"💰 Loot Price: **{d['price']}** ~({d['mrp']})~ 🔥 **{d['discount']}**\n"
            f"🔗 [Buy Now]({clean_link})\n\n"
        )
        buttons.append([InlineKeyboardButton(f"👉 Grab Deal #{idx}", url=clean_link)])
        
    await update.message.reply_text(text, reply_markup=InlineKeyboardMarkup(buttons), parse_mode=ParseMode.MARKDOWN, disable_web_page_preview=True)

async def search_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = " ".join(context.args) if context.args else ""
    if not query:
        await update.message.reply_text("🔍 Product search ke liye likhein: `/search tshirt` ya `/search shoes`", parse_mode=ParseMode.MARKDOWN)
        return
    deals = database.search_deals(query, limit=5)
    if not deals:
        await update.message.reply_text(f"❌ `{query}` ke liye koi deals nahi mili.", parse_mode=ParseMode.MARKDOWN)
        return
    await update.message.reply_text(f"🔍 **Search Results for '{query}':**", parse_mode=ParseMode.MARKDOWN)
    for d in deals:
        clean_link = shorten_url(d['link'])
        msg = f"🔥 **{d['title']}**\n💰 Price: {d['price']} ~({d['mrp']})~\n⚡ {d['discount']}\n👉 [Buy Now]({clean_link})"
        buttons = [[InlineKeyboardButton("🛍️ Buy Now", url=clean_link)]]
        await update.message.reply_text(msg, reply_markup=InlineKeyboardMarkup(buttons), parse_mode=ParseMode.MARKDOWN)

async def leaderboard_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    leaders = database.get_referral_leaderboard(10)
    if not leaders:
        await update.message.reply_text("🏆 Leaderboard par abhi koi user nahi hai. Sabse pehle apne dosto ko invite karein!", parse_mode=ParseMode.MARKDOWN)
        return
    text = "🏆 **TOP 10 REFERRAL CHAMPIONS** 🏆\n\n"
    medals = ["🥇", "🥈", "🥉", "4️⃣", "5️⃣", "6️⃣", "7️⃣", "8️⃣", "9️⃣", "🔟"]
    for idx, r in enumerate(leaders):
        badge = medals[idx] if idx < len(medals) else f"#{idx+1}"
        text += f"{badge} **{r.get('first_name') or 'User'}** — **{r.get('ref_count', 0)} Invites**\n"
    await update.message.reply_text(text, parse_mode=ParseMode.MARKDOWN)

async def refer_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.effective_user.id
    ref_link = f"https://t.me/Under99LootDeals_bot?start={user_id}"
    ref_count = database.get_referral_count(user_id)
    text = (
        "🎁 **REFER & EARN PROGRAM** 🎁\n\n"
        f"Aapka Personal Invite Link:\n`{ref_link}`\n\n"
        f"👥 Total Invites: **{ref_count} Members**\n\n"
        "• 3 Invites ➔ VIP Glitch Deals Access\n"
        "• 10 Invites ➔ Weekly ₹500 Amazon Gift Voucher"
    )
    wa_share = f"https://api.whatsapp.com/send?text={urllib_quote('🔥 Join Under 99 Loot Deals Bot for ₹1 to ₹99 deals: ' + ref_link)}"
    tg_share = f"https://t.me/share/url?url={ref_link}&text={urllib_quote('🔥 Join Under 99 Loot Deals Bot!')}"
    buttons = [
        [InlineKeyboardButton("🟢 Share on WhatsApp", url=wa_share)],
        [InlineKeyboardButton("📲 Share on Telegram", url=tg_share)]
    ]
    await update.message.reply_text(text, reply_markup=InlineKeyboardMarkup(buttons), parse_mode=ParseMode.MARKDOWN)

async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    text = update.message.text
    if text == "⚡ Under ₹99 Steal Deals":
        await under99_deals(update, context)
    elif text == "🔥 80-90% OFF Loots":
        await top_loots(update, context)
    elif text == "🔍 Search Deals":
        await update.message.reply_text("Type karein: `/search <product>` (Example: `/search watch`)", parse_mode=ParseMode.MARKDOWN)
    elif text == "🏆 Referral Leaderboard":
        await leaderboard_command(update, context)
    elif text == "🎁 Refer & Earn (Free Gifts)":
        await refer_command(update, context)
    elif text == "👤 My Profile":
        cnt = database.get_referral_count(update.effective_user.id)
        await update.message.reply_text(f"👤 **Aapka Profile**\nID: `{update.effective_user.id}`\nReferrals: **{cnt}**", parse_mode=ParseMode.MARKDOWN)
    elif text == "❓ Help & Support":
        await update.message.reply_text("Help ke liye /start dabayein ya admin se contact karein.", parse_mode=ParseMode.MARKDOWN)
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
    app.run_polling(drop_pending_updates=True)

if __name__ == "__main__":
    main()
