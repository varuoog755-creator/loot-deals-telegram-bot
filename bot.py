import os
import sys
import logging
import asyncio
import threading
from http.server import HTTPServer, BaseHTTPRequestHandler
from dotenv import load_dotenv

from telegram import (
    Update,
    InlineKeyboardButton,
    InlineKeyboardMarkup,
    ReplyKeyboardMarkup,
    KeyboardButton
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

# Load environment
env_path = os.path.join(os.path.dirname(__file__), ".env")
load_dotenv(env_path)

BOT_TOKEN = os.getenv("BOT_TOKEN")
ADMIN_ID = int(os.getenv("ADMIN_ID", "8837364917"))
INITIAL_CHANNEL = os.getenv("CHANNEL_USERNAME", "").strip()

if INITIAL_CHANNEL and not database.get_setting("channel"):
    database.set_setting("channel", INITIAL_CHANNEL)

EARNKARO_REF = os.getenv("EARNKARO_REFERRAL", "https://earnkaro.com")

logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    level=logging.INFO
)
logger = logging.getLogger(__name__)

# Keyboards
MAIN_KEYBOARD = [
    [KeyboardButton("🛍️ Today's Top Loots"), KeyboardButton("⚡ Under ₹99 Store")],
    [KeyboardButton("🎁 Refer & Earn (Free Gifts)"), KeyboardButton("👤 My Profile")],
    [KeyboardButton("💰 Earn Money Online (EarnKaro)"), KeyboardButton("❓ Help & Support")]
]

def get_main_markup():
    return ReplyKeyboardMarkup(MAIN_KEYBOARD, resize_keyboard=True)

async def is_user_subscribed(user_id: int, context: ContextTypes.DEFAULT_TYPE) -> bool:
    channel = database.get_setting("channel")
    if not channel:
        return True # No channel configured, allow through
    
    # Ensure @ prefix
    ch = channel if channel.startswith("@") or channel.startswith("-100") else f"@{channel}"
    try:
        member = await context.bot.get_chat_member(chat_id=ch, user_id=user_id)
        if member.status in [ChatMemberStatus.MEMBER, ChatMemberStatus.ADMINISTRATOR, ChatMemberStatus.OWNER]:
            return True
        return False
    except Exception as e:
        logger.warning(f"Could not check subscription for user {user_id} in {ch}: {e}")
        # If bot is not admin in channel, let user proceed so bot doesn't crash
        return True

async def send_force_sub_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    channel = database.get_setting("channel")
    ch_clean = channel.replace("@", "") if channel else ""
    channel_url = f"https://t.me/{ch_clean}" if ch_clean else "https://t.me"

    text = (
        "⚠️ **ACCESS LOCKED! Channel Join Zaroori Hai**\n\n"
        "Hamare Loot Deals & ₹99 Offers bot ko access karne ke liye aapko hamare official Deals Channel ko join karna hoga!\n\n"
        "👉 **Steps:**\n"
        "1. Niche **'📢 Join Deals Channel'** button par click karein.\n"
        "2. Channel Join karein.\n"
        "3. Wapas aakar **'✅ Joined / Unlock Loots'** par click karein!"
    )
    buttons = [
        [InlineKeyboardButton("📢 Join Deals Channel", url=channel_url)],
        [InlineKeyboardButton("✅ Joined / Unlock Loots", callback_data="check_subscription")]
    ]
    markup = InlineKeyboardMarkup(buttons)
    if update.callback_query:
        await update.callback_query.message.reply_text(text, reply_markup=markup, parse_mode=ParseMode.MARKDOWN)
    else:
        await update.message.reply_text(text, reply_markup=markup, parse_mode=ParseMode.MARKDOWN)

# Handlers
async def start_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user = update.effective_user
    user_id = user.id
    first_name = user.first_name or "User"
    username = user.username or ""

    # Check referral
    referrer_id = None
    if context.args and len(context.args) > 0:
        arg = context.args[0]
        if arg.startswith("ref_"):
            try:
                candidate_id = int(arg.replace("ref_", ""))
                if candidate_id != user_id:
                    referrer_id = candidate_id
            except ValueError:
                pass

    is_new = database.add_user(user_id, first_name, username, referrer_id)
    if is_new and referrer_id:
        try:
            ref_count = database.get_referral_count(referrer_id)
            await context.bot.send_message(
                chat_id=referrer_id,
                text=f"🎉 **Badhai ho!** Ek naye member ne aapke invite link se bot join kiya hai!\n\nAapke Total Referrals: **{ref_count}**"
            )
        except Exception:
            pass

    # Check channel subscription
    subscribed = await is_user_subscribed(user_id, context)
    if not subscribed:
        await send_force_sub_message(update, context)
        return

    welcome_text = (
        f"🔥 **Namaste {first_name}! Welcome to Loot Deals Hub** 🔥\n\n"
        "Yahan aapko roz milenge:\n"
        "🛍️ **80-90% OFF Loot Deals** (Amazon, Flipkart, Myntra, Ajio)\n"
        "⚡ **₹1 se ₹99 tak ke Hidden Offers**\n"
        "💰 **Daily Free Cashback Tricks & Coupons**\n\n"
        "Niche diye gaye buttons se apni pasandida deals dekhein 👇"
    )
    await update.message.reply_text(welcome_text, reply_markup=get_main_markup(), parse_mode=ParseMode.MARKDOWN)

async def check_subscription_callback(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    user_id = update.effective_user.id

    subscribed = await is_user_subscribed(user_id, context)
    if subscribed:
        await query.message.reply_text(
            "🎉 **Verification Successful!** Deals unlock ho chuki hain.\n\nNiche menu se offers select karein:",
            reply_markup=get_main_markup()
        )
    else:
        await query.message.reply_text(
            "❌ Aapne abhi tak Channel join nahi kiya hai! Pehle channel join karein phir verify karein.",
            parse_mode=ParseMode.MARKDOWN
        )

async def top_loots(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.effective_user.id
    if not await is_user_subscribed(user_id, context):
        await send_force_sub_message(update, context)
        return

    deals = database.get_recent_deals(limit=5, category="Loot")
    if not deals:
        await update.message.reply_text("Abhi naye deals update ho rahe hain, kripya thodi der baad check karein!")
        return

    text = "🔥 **TODAY'S TOP LOOT DEALS (Limited Time)** 🔥\n\n"
    buttons = []
    for idx, d in enumerate(deals, 1):
        text += (
            f"**{idx}. {d['title']}**\n"
            f"💰 Loot Price: **{d['price']}** ~({d['mrp']})~ 🔥 **{d['discount']}**\n"
            f"🔗 [Buy / Grab Deal Now]({d['link']})\n\n"
        )
        buttons.append([InlineKeyboardButton(f"👉 Grab Deal #{idx} ({d['price']})", url=d['link'])])

    text += "⚡ *Deals kabhi bhi out of stock ho sakti hain! Jaldi grab karein.*"
    markup = InlineKeyboardMarkup(buttons)
    await update.message.reply_text(text, reply_markup=markup, parse_mode=ParseMode.MARKDOWN, disable_web_page_preview=True)

async def under_99_loots(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.effective_user.id
    if not await is_user_subscribed(user_id, context):
        await send_force_sub_message(update, context)
        return

    deals = database.get_recent_deals(limit=5, category="Under99")
    if not deals:
        deals = database.get_recent_deals(limit=5)

    text = "⚡ **UNDER ₹99 MEGA STORE (Steal Deals)** ⚡\n\n"
    buttons = []
    for idx, d in enumerate(deals, 1):
        text += (
            f"**{idx}. {d['title']}**\n"
            f"💰 Steal Price: **{d['price']}** ~({d['mrp']})~\n"
            f"🔗 [Claim Under ₹99 Now]({d['link']})\n\n"
        )
        buttons.append([InlineKeyboardButton(f"⚡ Buy #{idx} at {d['price']}", url=d['link'])])

    text += "💥 *Free delivery tricks & limited quantity available!*"
    markup = InlineKeyboardMarkup(buttons)
    await update.message.reply_text(text, reply_markup=markup, parse_mode=ParseMode.MARKDOWN, disable_web_page_preview=True)

async def refer_and_earn(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user = update.effective_user
    user_id = user.id
    if not await is_user_subscribed(user_id, context):
        await send_force_sub_message(update, context)
        return

    bot_username = (await context.bot.get_me()).username
    ref_link = f"https://t.me/{bot_username}?start=ref_{user_id}"
    ref_count = database.get_referral_count(user_id)

    text = (
        "🎁 **VIRAL REFER & EARN PROGRAM** 🎁\n\n"
        "Apne dosto aur family groups mein apna referral link share karein aur special rewards payen!\n\n"
        f"👥 Aapke Total Invites: **{ref_count} Members**\n\n"
        "🎯 **Milestone Rewards:**\n"
        "• **3 Invites:** VIP Secret Deals Access\n"
        "• **10 Invites:** Monthly ₹500 Amazon Gift Card Entry\n\n"
        "🔗 **Aapka Personal Invite Link:**\n"
        f"`{ref_link}`\n\n"
        "*(Upar diye gaye link ko copy karke WhatsApp aur Telegram par forward karein!)*"
    )
    share_url = f"https://t.me/share/url?url={ref_link}&text={urllib_quote('🔥 Join Loot Deals Hub for ₹1 to ₹99 deals and 90% discounts!')}"
    buttons = [[InlineKeyboardButton("📲 Share on Telegram", url=share_url)]]
    await update.message.reply_text(text, reply_markup=InlineKeyboardMarkup(buttons), parse_mode=ParseMode.MARKDOWN)

def urllib_quote(text: str):
    import urllib.parse
    return urllib.parse.quote(text)

async def user_profile(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user = update.effective_user
    user_id = user.id
    ref_count = database.get_referral_count(user_id)
    badge = "🌟 Gold VIP Member" if ref_count >= 3 else "🥉 Regular Member"

    text = (
        f"👤 **USER PROFILE**\n\n"
        f"• **Name:** {user.first_name}\n"
        f"• **User ID:** `{user_id}`\n"
        f"• **Status:** {badge}\n"
        f"• **Total Referred:** **{ref_count} users**\n"
        f"• **VIP Channel Access:** {'✅ UNLOCKED' if ref_count >= 3 else '❌ Invite 3 friends to unlock'}"
    )
    await update.message.reply_text(text, parse_mode=ParseMode.MARKDOWN)

async def earnkaro_info(update: Update, context: ContextTypes.DEFAULT_TYPE):
    text = (
        "💰 **Ghar Baithe Paise Kamayein (EarnKaro Affiliate)** 💰\n\n"
        "Kya aap bhi daily online shopping links share karke mahine ke ₹10,000–₹30,000 kamana chahte hain?\n\n"
        "1️⃣ **EarnKaro App Download karein**\n"
        "2️⃣ Amazon, Flipkart, Myntra ka koi bhi product link convert karein\n"
        "3️⃣ WhatsApp & Telegram groups mein share karein\n"
        "4️⃣ Jab koi buy karega, seedha aapke bank account mein commission aayega!\n\n"
        "👉 **Free Account Banane Ke Liye Niche Button Par Click Karein:**"
    )
    buttons = [[InlineKeyboardButton("🚀 Download & Register Free on EarnKaro", url=EARNKARO_REF)]]
    await update.message.reply_text(text, reply_markup=InlineKeyboardMarkup(buttons), parse_mode=ParseMode.MARKDOWN)

async def help_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    text = (
        "❓ **HELP & COMMANDS**\n\n"
        "• /start - Bot shuru karein aur main menu dekhein\n"
        "• 🛍️ Today's Top Loots - Best discounts dekhein\n"
        "• ⚡ Under ₹99 - Saste budget deals dekhein\n"
        "• 🎁 Refer & Earn - Apna invite link banayein\n\n"
        "Admin help ke liye @BotFather ya bot support se sampark karein."
    )
    await update.message.reply_text(text, parse_mode=ParseMode.MARKDOWN)

# Admin Commands
async def admin_stats(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if update.effective_user.id != ADMIN_ID:
        return
    total_users = database.get_user_count()
    channel = database.get_setting("channel", "Not Set")
    deals_count = len(database.get_recent_deals(100))

    text = (
        "📊 **ADMIN DASHBOARD**\n\n"
        f"• **Total Bot Users:** {total_users}\n"
        f"• **Active Channel:** `{channel}`\n"
        f"• **Total Deals in DB:** {deals_count}\n\n"
        "**Admin Commands:**\n"
        "• `/setchannel @YourChannel` - Force subscribe channel set karein\n"
        "• `/broadcast <message>` - Sabhi users ko message bhejein\n"
        "• `/adddeal Title | Price | MRP | Discount | Link | [Loot/Under99]`"
    )
    await update.message.reply_text(text, parse_mode=ParseMode.MARKDOWN)

async def admin_set_channel(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if update.effective_user.id != ADMIN_ID:
        return
    if not context.args:
        await update.message.reply_text("Usage: `/setchannel @YourChannelUsername`", parse_mode=ParseMode.MARKDOWN)
        return
    ch = context.args[0].strip()
    database.set_setting("channel", ch)
    await update.message.reply_text(
        f"✅ **Channel successfully set to `{ch}`!**\n\n"
        "⚠️ *Zaroori Note:* Bot ko is channel mein **Administrator** banayein taaki bot users ki subscription verify kar sake.",
        parse_mode=ParseMode.MARKDOWN
    )

async def admin_broadcast(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if update.effective_user.id != ADMIN_ID:
        return
    if not context.args:
        await update.message.reply_text("Usage: `/broadcast Aapka message yahan`", parse_mode=ParseMode.MARKDOWN)
        return

    msg = " ".join(context.args)
    users = database.get_all_users()
    await update.message.reply_text(f"🚀 Broadcasting message to {len(users)} users...")

    success = 0
    failed = 0
    for uid in users:
        try:
            await context.bot.send_message(chat_id=uid, text=msg, parse_mode=ParseMode.MARKDOWN)
            success += 1
            await asyncio.sleep(0.05) # Prevent flood limits
        except Exception:
            failed += 1

    await update.message.reply_text(f"✅ **Broadcast Completed!**\nSuccess: {success}\nFailed/Blocked: {failed}")

async def admin_add_deal(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if update.effective_user.id != ADMIN_ID:
        return
    raw = " ".join(context.args)
    parts = [p.strip() for p in raw.split("|")]
    if len(parts) < 5:
        await update.message.reply_text(
            "Usage: `/adddeal Title | Price | MRP | Discount | Link | [Loot/Under99]`",
            parse_mode=ParseMode.MARKDOWN
        )
        return

    title = parts[0]
    price = parts[1]
    mrp = parts[2]
    discount = parts[3]
    link = parts[4]
    category = parts[5] if len(parts) > 5 else "Loot"

    database.add_deal(title, price, mrp, discount, link, category)
    await update.message.reply_text(f"✅ Deal added successfully:\n**{title}** ({price}) in `{category}`", parse_mode=ParseMode.MARKDOWN)

# Text router
async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    text = update.message.text
    if text == "🛍️ Today's Top Loots":
        await top_loots(update, context)
    elif text == "⚡ Under ₹99 Store":
        await under_99_loots(update, context)
    elif text == "🎁 Refer & Earn (Free Gifts)":
        await refer_and_earn(update, context)
    elif text == "👤 My Profile":
        await user_profile(update, context)
    elif text == "💰 Earn Money Online (EarnKaro)":
        await earnkaro_info(update, context)
    elif text == "❓ Help & Support":
        await help_command(update, context)
    else:
        await update.message.reply_text("Niche menu se koi option chunein 👇", reply_markup=get_main_markup())

class HealthHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        self.send_response(200)
        self.send_header('Content-type', 'text/plain')
        self.end_headers()
        self.wfile.write(b"Loot Deals Telegram Bot is running 24/7!")
    def log_message(self, format, *args):
        pass

def start_health_server():
    port = int(os.environ.get("PORT", 8080))
    server = HTTPServer(("0.0.0.0", port), HealthHandler)
    server.serve_forever()

def main():
    if not BOT_TOKEN:
        print("Error: BOT_TOKEN not found!")
        sys.exit(1)

    # Start lightweight health server for cloud platforms (Render, Koyeb, Railway)
    threading.Thread(target=start_health_server, daemon=True).start()

    while True:
        try:
            app = ApplicationBuilder().token(BOT_TOKEN).build()

            app.add_handler(CommandHandler("start", start_command))
            app.add_handler(CommandHandler("help", help_command))
            app.add_handler(CommandHandler("stats", admin_stats))
            app.add_handler(CommandHandler("setchannel", admin_set_channel))
            app.add_handler(CommandHandler("broadcast", admin_broadcast))
            app.add_handler(CommandHandler("adddeal", admin_add_deal))

            app.add_handler(CallbackQueryHandler(check_subscription_callback, pattern="^check_subscription$"))
            app.add_handler(MessageHandler(filters.TEXT & (~filters.COMMAND), handle_message))

            print("🚀 Loot Deals Bot is running...")
            app.run_polling(drop_pending_updates=True)
        except Exception as e:
            print(f"Polling crashed: {e}. Auto-restarting in 5 seconds...")
            import time
            time.sleep(5)

if __name__ == "__main__":
    main()
