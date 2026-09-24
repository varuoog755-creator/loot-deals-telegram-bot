import os
import sys
import logging
import asyncio
import threading
import urllib.parse
from http.server import HTTPServer, BaseHTTPRequestHandler
from dotenv import load_dotenv

from telegram import (
    Update,
    InlineKeyboardButton,
    InlineKeyboardMarkup,
    ReplyKeyboardMarkup,
    KeyboardButton,
    WebAppInfo,
    BotCommand
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
from affiliate_engine import create_affiliate_deal_link, detect_store

# Load environment
env_path = os.path.join(os.path.dirname(__file__), ".env")
load_dotenv(env_path)

BOT_TOKEN = os.getenv("BOT_TOKEN")
ADMIN_ID = int(os.getenv("ADMIN_ID", "8837364917"))
INITIAL_CHANNEL = os.getenv("CHANNEL_USERNAME", "").strip()

if INITIAL_CHANNEL and not database.get_setting("channel"):
    database.set_setting("channel", INITIAL_CHANNEL)

EARNKARO_REF_ID = os.getenv("EARNKARO_REF_ID", "1962062")
EARNKARO_REF = os.getenv("EARNKARO_REFERRAL", f"https://earnkaro.com?r={EARNKARO_REF_ID}")

_URL_CACHE = {}

def shorten_url(url: str) -> str:
    """Shortens any URL using TinyURL/Clck so that affiliate networks and tracking parameters are completely hidden."""
    if not url:
        return url
    if url in _URL_CACHE:
        return _URL_CACHE[url]
    
    # 1. TinyURL
    try:
        import urllib.request, urllib.parse
        api_url = "https://tinyurl.com/api-create.php?" + urllib.parse.urlencode({"url": url})
        req = urllib.request.Request(api_url, headers={"User-Agent": "Mozilla/5.0"})
        with urllib.request.urlopen(req, timeout=4) as resp:
            short = resp.read().decode("utf-8").strip()
            if short.startswith("http"):
                _URL_CACHE[url] = short
                return short
    except Exception:
        pass
        
    # 2. Clck.ru fallback
    try:
        import urllib.request, urllib.parse
        api_url = "https://clck.ru/--?url=" + urllib.parse.quote(url)
        req = urllib.request.Request(api_url, headers={"User-Agent": "Mozilla/5.0"})
        with urllib.request.urlopen(req, timeout=4) as resp:
            short = resp.read().decode("utf-8").strip()
            if short.startswith("http"):
                _URL_CACHE[url] = short
                return short
    except Exception:
        pass

    _URL_CACHE[url] = url
    return url

logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    level=logging.INFO
)
logger = logging.getLogger(__name__)

# Keyboards
MAIN_KEYBOARD = [
    [KeyboardButton("🛍️ Today's Top Loots"), KeyboardButton("⚡ Under ₹99 Store")],
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

DEFAULT_CHANNEL_LINK = "https://t.me/+vnry55FncIUxMDVl"
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

async def is_user_subscribed(user_id: int, context: ContextTypes.DEFAULT_TYPE) -> bool:
    if user_id == ADMIN_ID or is_verified_locally(user_id):
        return True
    channel = database.get_setting("channel")
    if not channel:
        return False
    
    # Ensure @ prefix
    ch = channel if channel.startswith("@") or channel.startswith("-100") else f"@{channel}"
    try:
        member = await context.bot.get_chat_member(chat_id=ch, user_id=user_id)
        if member.status in [ChatMemberStatus.MEMBER, ChatMemberStatus.ADMINISTRATOR, ChatMemberStatus.OWNER]:
            mark_user_verified(user_id)
            return True
        return False
    except Exception as e:
        logger.warning(f"Could not check subscription for user {user_id} in {ch}: {e}")
        return is_verified_locally(user_id)

async def send_force_sub_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    channel = database.get_setting("channel")
    if channel:
        if channel.startswith("http"):
            channel_url = channel
        else:
            ch_clean = channel.replace("@", "")
            channel_url = f"https://t.me/{ch_clean}"
    else:
        channel_url = DEFAULT_CHANNEL_LINK

    text = (
        "⚠️ **ACCESS LOCKED! Official Channel Join Zaroori Hai**\n\n"
        "Hamare Loot Deals & ₹99 Offers bot ko access karne ke liye aapko hamare official Deals Channel ko join karna compulsory hai!\n\n"
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
    if update.callback_query and update.callback_query.message:
        await update.callback_query.message.reply_text(text, reply_markup=markup, parse_mode=ParseMode.MARKDOWN)
    elif update.message:
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
            needed = max(0, 3 - ref_count)
            if ref_count >= 3:
                msg = (
                    f"🎉 <b>BOOM! Naya Referral Aaya!</b> 🎉\n\n"
                    f"Aapke friend <b>{first_name}</b> ne aapke invite link se bot join kar liya!\n\n"
                    f"👥 Total Invites: <b>{ref_count}</b>\n"
                    f"🌟 <b>Badhai Ho! Aapka VIP Secret Glitch Deals access UNLOCKED hai!</b>\n\n"
                    f"Deals dekhne ke liye bot me <b>'🌟 VIP Secret Glitch Deals'</b> button dabayein!"
                )
            else:
                msg = (
                    f"🔔 <b>BOOM! Naya Referral Aaya!</b> 🎉\n\n"
                    f"Aapke friend <b>{first_name}</b> ne aapke invite link se bot join kar liya!\n\n"
                    f"👥 Total Invites: <b>{ref_count}</b>\n"
                    f"🎯 VIP Glitch Deals unlock karne ke liye bas <b>{needed} invite</b> bache hain!\n\n"
                    f"Apna link WhatsApp aur groups par aur share karein!"
                )
            await context.bot.send_message(chat_id=referrer_id, text=msg, parse_mode=ParseMode.HTML)
        except Exception as e:
            logger.warning(f"Could not notify referrer {referrer_id}: {e}")

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
    inline_nav = InlineKeyboardMarkup([
        [InlineKeyboardButton("🛍️ Open Interactive Deals Store (Mini App)", web_app=WebAppInfo(url="https://loot-deals-telegram-bot.onrender.com/"))]
    ])
    await update.message.reply_text(welcome_text, reply_markup=get_main_markup(), parse_mode=ParseMode.MARKDOWN)
    await update.message.reply_text("⚡ **Quick Access:** Direct full-screen store open karne ke liye niche button dabayein 👇", reply_markup=inline_nav, parse_mode=ParseMode.MARKDOWN)

async def check_subscription_callback(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    if not query:
        return
    await query.answer()
    if not update.effective_user:
        return
    user_id = update.effective_user.id
    channel = database.get_setting("channel")

    verified = False
    if channel and (channel.startswith("@") or channel.startswith("-100")):
        ch = channel if channel.startswith("@") or channel.startswith("-100") else f"@{channel}"
        try:
            member = await context.bot.get_chat_member(chat_id=ch, user_id=user_id)
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
                    "🎉 **Verification Successful! Channel Join Confirmed!**\n\nAapka access unlock ho chuka hai. Niche menu se offers select karein:",
                    parse_mode=ParseMode.MARKDOWN
                )
            except Exception:
                pass
        await context.bot.send_message(
            chat_id=user_id,
            text="⚡ **Loot Deals Store Unlocked:** Browse karna shuru karein 👇",
            reply_markup=get_main_markup(),
            parse_mode=ParseMode.MARKDOWN
        )
    else:
        await query.answer("❌ Aapne abhi tak Channel join nahi kiya hai! Pehle join karein phir verify karein.", show_alert=True)

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
    bot_uname = (await context.bot.get_me()).username or "Roxk755_bot"
    ref_link = f"https://t.me/{bot_uname}?start=ref_{user_id}"

    for idx, d in enumerate(deals, 1):
        clean_link = shorten_url(d['link'])
        text += (
            f"**{idx}. {d['title']}**\n"
            f"💰 Loot Price: **{d['price']}** ~({d['mrp']})~ 🔥 **{d['discount']}**\n"
            f"🔗 [Buy / Grab Deal Now]({clean_link})\n\n"
        )
        share_msg = f"🔥 {d['title']} par {d.get('discount', '80% OFF')} chal raha hai! Check: {clean_link}\n\n🤖 Aur daily loot deals ke liye bot join karein: {ref_link}"
        tg_share = f"https://t.me/share/url?url={urllib.parse.quote(ref_link)}&text={urllib.parse.quote(share_msg)}"
        buttons.append([
            InlineKeyboardButton(f"👉 Grab Deal #{idx} ({d['price']})", url=clean_link),
            InlineKeyboardButton("🎁 Share & Earn ₹10", url=tg_share)
        ])

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
    bot_uname = (await context.bot.get_me()).username or "Roxk755_bot"
    ref_link = f"https://t.me/{bot_uname}?start=ref_{user_id}"

    for idx, d in enumerate(deals, 1):
        clean_link = shorten_url(d['link'])
        text += (
            f"**{idx}. {d['title']}**\n"
            f"💰 Steal Price: **{d['price']}** ~({d['mrp']})~\n"
            f"🔗 [Claim Under ₹99 Now]({clean_link})\n\n"
        )
        share_msg = f"⚡ {d['title']} sirf {d['price']} me! Check: {clean_link}\n\n🤖 Aur ₹1/₹99 deals ke liye bot join karein: {ref_link}"
        tg_share = f"https://t.me/share/url?url={urllib.parse.quote(ref_link)}&text={urllib.parse.quote(share_msg)}"
        buttons.append([
            InlineKeyboardButton(f"⚡ Buy #{idx} at {d['price']}", url=clean_link),
            InlineKeyboardButton("🎁 Share & Earn ₹10", url=tg_share)
        ])

    text += "💥 *Free delivery tricks & limited quantity available!*"
    markup = InlineKeyboardMarkup(buttons)
    await update.message.reply_text(text, reply_markup=markup, parse_mode=ParseMode.MARKDOWN, disable_web_page_preview=True)

async def vip_deals(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not update.effective_user or not update.message:
        return
    user_id = update.effective_user.id
    if not await is_user_subscribed(user_id, context):
        await send_force_sub_message(update, context)
        return

    ref_count = database.get_referral_count(user_id)
    if ref_count < 3 and user_id != ADMIN_ID:
        needed = 3 - ref_count
        bot_uname = (await context.bot.get_me()).username or "Roxk755_bot"
        ref_link = f"https://t.me/{bot_uname}?start=ref_{user_id}"
        wa_text = urllib.parse.quote(f"🔥 Best Telegram Loot Deals & 90% Discounts Bot! Join with my link: {ref_link}")
        tg_text = urllib.parse.quote(f"🔥 Join Loot Deals Bot for VIP Secret Price Errors: {ref_link}")
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
            f"⚡ <b>Sirf {needed} aur friend(s)</b> ko invite karein aur instantly VIP Glitch Deals unlock karein!\n\n"
            "Niche WhatsApp button par click karke dosto ya groups me share karein 👇"
        )
        await update.message.reply_text(text, reply_markup=InlineKeyboardMarkup(buttons), parse_mode=ParseMode.HTML)
        return

    # User is VIP!
    deals = database.get_recent_deals(limit=5, category="VIP")
    if not deals:
        deals = database.get_recent_deals(limit=5, category="Loot")
    if not deals:
        deals = database.get_recent_deals(limit=5)
    text = (
        "🌟 <b>VIP SECRET GLITCH DEALS UNLOCKED!</b> 🌟\n\n"
        "👑 <i>Congratulations VIP Member! Yahan hain aaj ki secret 85-95% OFF price error loot deals:</i>\n\n"
    )
    buttons = []
    bot_uname = (await context.bot.get_me()).username or "Roxk755_bot"
    ref_link = f"https://t.me/{bot_uname}?start=ref_{user_id}"

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
        share_msg = f"🔥 VIP Glitch Deal: {title} sirf {price} me! {clean_link}\n\n🤖 VIP Store access ke liye bot join karein: {ref_link}"
        tg_share = f"https://t.me/share/url?url={urllib.parse.quote(ref_link)}&text={urllib.parse.quote(share_msg)}"
        buttons.append([
            InlineKeyboardButton(f"⚡ Grab VIP #{idx} ({price})", url=clean_link),
            InlineKeyboardButton("🎁 Share & Earn ₹10", url=tg_share)
        ])
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

async def refer_and_earn(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user = update.effective_user
    if not user or not update.message:
        return
    user_id = user.id
    if not await is_user_subscribed(user_id, context):
        await send_force_sub_message(update, context)
        return

    bot_username = (await context.bot.get_me()).username or "Roxk755_bot"
    ref_link = f"https://t.me/{bot_username}?start=ref_{user_id}"
    ref_count = database.get_referral_count(user_id)
    progress_vip = make_progress_bar(ref_count, 3)

    text = (
        "🎁 <b>VIRAL REFER & EARN PROGRAM</b> 🎁\n\n"
        "Apne dosto aur WhatsApp groups mein apna referral link share karein aur special rewards payen!\n\n"
        f"👥 Total Invites: <b>{ref_count} Members</b>\n"
        f"📊 VIP Progress: <b>{progress_vip}</b>\n\n"
        "🎯 <b>Milestone Rewards:</b>\n"
        "• <b>3 Invites:</b> 🌟 VIP Secret Glitch Deals Unlocked (95% OFF)\n"
        "• <b>5 Invites:</b> ⚡ ₹50 Instant Cashback Voucher\n"
        "• <b>10 Invites:</b> 🏆 Weekly ₹500 Amazon Gift Voucher Lucky Draw\n\n"
        "🔗 <b>Aapka Personal Invite Link:</b>\n"
        f"<code>{ref_link}</code>\n\n"
        "👉 <i>Direct WhatsApp ya Telegram par share karne ke liye niche buttons dabayein:</i>"
    )
    share_text = f"🔥 Best Telegram Loot Deals & 90% Discounts Bot! Join with my link: {ref_link}"
    tg_share = f"https://t.me/share/url?url={ref_link}&text={urllib_quote('🔥 Join Loot Deals Hub for ₹1 to ₹99 deals and 90% discounts!')}"
    wa_share = f"https://api.whatsapp.com/send?text={urllib_quote(share_text)}"
    buttons = [
        [InlineKeyboardButton("🟢 Share on WhatsApp", url=wa_share)],
        [InlineKeyboardButton("📲 Share on Telegram", url=tg_share)],
        [InlineKeyboardButton("🌟 Check VIP Deals Status", callback_data="check_vip_status")]
    ]
    await update.message.reply_text(text, reply_markup=InlineKeyboardMarkup(buttons), parse_mode=ParseMode.HTML)

def urllib_quote(text: str):
    import urllib.parse
    return urllib.parse.quote(text)

async def user_profile(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user = update.effective_user
    user_id = user.id
    wallet = database.get_user_wallet(user_id)
    ref_count = wallet["referral_count"]
    balance = wallet["wallet_balance"]
    next_m = wallet["next_milestone"]
    badge = "🌟 Gold VIP Member" if wallet["vip_unlocked"] or user_id == ADMIN_ID else "🥉 Regular Member"

    text = (
        f"👤 <b>AFFILIATE USER PROFILE & WALLET</b>\n\n"
        f"• <b>Name:</b> {user.first_name}\n"
        f"• <b>User ID:</b> <code>{user_id}</code>\n"
        f"• <b>Status:</b> <b>{badge}</b>\n"
        f"• <b>Total Referrals:</b> <b>{ref_count} users</b>\n"
        f"• <b>Virtual Referral Wallet:</b> <b>₹{balance} Cash</b>\n"
        f"• <b>VIP Glitch Store Access:</b> {'✅ UNLOCKED' if wallet['vip_unlocked'] or user_id == ADMIN_ID else f'❌ Locked ({ref_count}/3 Invites)'}\n"
        f"• <b>Next Cash Milestone:</b> {next_m} Invites\n\n"
        f"🎁 <i>Har dost ko jodne par ₹10 wallet cash judta hai!</i>"
    )
    await update.message.reply_text(text, parse_mode=ParseMode.HTML)

async def earnkaro_info(update: Update, context: ContextTypes.DEFAULT_TYPE):
    text = (
        "💰 <b>Ghar Baithe Paise Kamayein (Cashback & Earning App)</b> 💰\n\n"
        "Kya aap bhi daily online shopping offers & deals share karke mahine ke ₹10,000–₹30,000 kamana chahte hain?\n\n"
        "1️⃣ <b>Cashback App Free Me Join Karein</b>\n"
        "2️⃣ Amazon, Flipkart, Myntra ka koi bhi product link convert karein\n"
        "3️⃣ WhatsApp & Telegram groups mein share karein\n"
        "4️⃣ Jab koi buy karega, seedha aapke bank account mein commission / cashback aayega!\n\n"
        "🎁 <b>Special Offer:</b> Abhi free register karne par <b>₹50 Welcome Bonus</b> milta hai!\n\n"
        "👉 <b>Free Account Banane Ke Liye Niche Button Par Click Karein:</b>"
    )
    clean_ref = "https://tinyurl.com/26gtkvfm"
    buttons = [
        [InlineKeyboardButton("🚀 Activate Free Cashback Account (₹50 Bonus)", url=clean_ref)],
        [InlineKeyboardButton("🟢 Share with Friends on WhatsApp", url=f"https://api.whatsapp.com/send?text={urllib.parse.quote('Ghar baithe shopping aur deals share karke extra cashback kamayein: ' + clean_ref)}")]
    ]
    await update.message.reply_text(text, reply_markup=InlineKeyboardMarkup(buttons), parse_mode=ParseMode.HTML)

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

async def leaderboard_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    leaders = database.get_referral_leaderboard(10)
    if not leaders:
        text = (
            "🏆 **TOP REFERRAL LEADERBOARD** 🏆\n\n"
            "Abhi tak leaderboard par koi data nahi hai.\n"
            "Aap sabse pehle apne dosto ko invite karke #1 Rank ban sakte hain! 🚀\n\n"
            "👉 Menu se **'🎁 Refer & Earn'** par click karein aur invite link payen!"
        )
    else:
        text = "🏆 **TOP 10 REFERRAL CHAMPIONS** 🏆\n\n"
        medals = ["🥇", "🥈", "🥉", "4️⃣", "5️⃣", "6️⃣", "7️⃣", "8️⃣", "9️⃣", "🔟"]
        for idx, row in enumerate(leaders):
            badge = medals[idx] if idx < len(medals) else f"#{idx+1}"
            name = row.get("first_name") or "User"
            uname = f"(@{row['username']})" if row.get("username") else ""
            cnt = row.get("ref_count", 0)
            text += f"{badge} **{name}** {uname} — **{cnt} Invites**\n"
        text += "\n🔥 **Rules:** Har week ke Top 3 referrers ko exclusive ₹500 Amazon Gift Vouchers diye jaate hain! Apna link share karein aur rank up karein!"

    await update.message.reply_text(text, parse_mode=ParseMode.MARKDOWN)

async def search_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = " ".join(context.args) if context.args else ""
    if not query:
        await update.message.reply_text(
            "🔍 **Deal Search Kaise Karein:**\n\n"
            "Kisi bhi item ko search karne ke liye command ke baad naam likhein. Example:\n"
            "`/search shoes`\n"
            "`/search tshirt`\n"
            "`/search earphone`",
            parse_mode=ParseMode.MARKDOWN
        )
        return

    deals = database.search_deals(query, limit=5)
    if not deals:
        await update.message.reply_text(
            f"❌ `{query}` ke liye koi deals nahi mili. Hamare Deals Channel me daily live flash deals aate hain, wahan check karein!",
            parse_mode=ParseMode.MARKDOWN
        )
        return

    await update.message.reply_text(f"🔍 **Search Results for '{query}':**", parse_mode=ParseMode.MARKDOWN)
    for d in deals:
        title = d.get('title', 'Deal')
        price = d.get('price', '')
        mrp = d.get('mrp', '')
        discount = d.get('discount', '')
        link = d.get('link', '')
        clean_link = shorten_url(link) if link else '#'
        deal_msg = (
            f"🔥 **{title}**\n"
            f"💰 **Loot Price:** {price} (MRP: ~{mrp}~)\n"
            f"⚡ **Discount:** {discount}\n\n"
            f"👉 [Click Here to Buy Now]({clean_link})"
        )
        buttons = [[InlineKeyboardButton("🛍️ Buy Now", url=clean_link)]]
        await update.message.reply_text(deal_msg, reply_markup=InlineKeyboardMarkup(buttons), parse_mode=ParseMode.MARKDOWN)

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
    if not update.message or not update.message.text:
        return
    text = update.message.text

    # Check if message contains a product link to convert
    import re, urllib.parse
    url_match = re.search(r'(https?://[^\s]+)', text)
    if url_match:
        raw_url = url_match.group(1)
        deal_info = create_affiliate_deal_link(raw_url)
        clean_short_url = deal_info["affiliate_url"]
        store = deal_info["store"]
        icon = deal_info["icon"]
        cashback = deal_info["cashback_rate"]
        
        wa_share = f"https://api.whatsapp.com/send?text={urllib.parse.quote(f'🔥 Loot Deal: Order karein direct cashback ke sath 👉 {clean_short_url}')}"

        reply = (
            f"🎉 <b>CASHBACK DEAL LINK GENERATED!</b> 🎉\n\n"
            f"🏬 <b>Store:</b> {icon} {store}\n"
            f"💰 <b>Cashback Rate:</b> <b>{cashback}</b>\n\n"
            f"👉 <b>Order Link:</b> <code>{clean_short_url}</code>\n\n"
            f"💡 <i>Is link se shopping karne par aapko exclusive discount aur direct cashback track hoga!</i>\n\n"
            f"<i>(Ise dosto aur family groups mein share karke bhi earning kar sakte hain!)</i>"
        )
        markup = InlineKeyboardMarkup([
            [InlineKeyboardButton(f"🛒 Buy on {store} & Grab Cashback", url=clean_short_url)],
            [InlineKeyboardButton("📲 Share Deal on WhatsApp", url=wa_share)]
        ])
        await update.message.reply_text(reply, reply_markup=markup, parse_mode=ParseMode.HTML, disable_web_page_preview=True)
        return

    if text == "🛍️ Today's Top Loots":
        await top_loots(update, context)
    elif text == "⚡ Under ₹99 Store":
        await under_99_loots(update, context)
    elif text in ["🌟 VIP Secret Glitch Deals", "🌟 VIP Secret Deals"]:
        await vip_deals(update, context)
    elif text in ["🎁 Refer & Win Free Rewards", "🎁 Refer & Earn (Free Gifts)", "🎁 Refer & Earn"]:
        await refer_and_earn(update, context)
    elif text == "🏆 Referral Leaderboard":
        await leaderboard_command(update, context)
    elif text == "🔍 Search Deals":
        await update.message.reply_text("🔍 Kisi bhi product ko search karne ke liye type karein: `/search <naam>`\nExample: `/search tshirt` ya `/search shoes`", parse_mode=ParseMode.MARKDOWN)
    elif text == "👤 My Profile":
        await user_profile(update, context)
    elif text in ["💰 Daily Cashback & Earning App", "💰 Earn Money Online (EarnKaro)"]:
        await earnkaro_info(update, context)
    elif text == "❓ Help & Support":
        await help_command(update, context)
    else:
        await update.message.reply_text("Niche menu se koi option chunein 👇", reply_markup=get_main_markup())

class HealthHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        if self.path in ["/healthz", "/ping"]:
            self.send_response(200)
            self.send_header('Content-type', 'text/plain')
            self.end_headers()
            self.wfile.write(b"OK")
            return

        landing_path = os.path.join(os.path.dirname(__file__), "landing.html")
        if os.path.exists(landing_path):
            with open(landing_path, "rb") as f:
                content = f.read()
            self.send_response(200)
            self.send_header('Content-type', 'text/html; charset=utf-8')
            self.send_header('Content-length', str(len(content)))
            self.end_headers()
            self.wfile.write(content)
        else:
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

def keep_alive():
    import time, urllib.request
    time.sleep(60)
    url = os.environ.get("RENDER_EXTERNAL_URL", "https://loot-deals-telegram-bot.onrender.com")
    while True:
        try:
            with urllib.request.urlopen(url, timeout=10) as _:
                pass
        except Exception:
            pass
        time.sleep(600)

def launch_under99_bot():
    import subprocess, time
    time.sleep(3)
    script = os.path.join(os.path.dirname(__file__), "under99_bot.py")
    if os.path.exists(script):
        while True:
            try:
                print("🚀 Spawning under99_bot.py in background...")
                proc = subprocess.Popen([sys.executable, script])
                proc.wait()
                print("⚠️ under99_bot.py stopped, restarting in 5s...")
                time.sleep(5)
            except Exception as e:
                print(f"Error managing under99_bot: {e}")
                time.sleep(10)

def launch_auto_publisher():
    import subprocess, time
    time.sleep(15)
    script = os.path.join(os.path.dirname(__file__), "auto_publisher.py")
    if os.path.exists(script):
        while True:
            try:
                print("📢 Spawning auto_publisher.py loop in background...")
                proc = subprocess.Popen([sys.executable, script])
                proc.wait()
                print("⚠️ auto_publisher.py exited, restarting in 30s...")
                time.sleep(30)
            except Exception as e:
                print(f"Error managing auto_publisher: {e}")
                time.sleep(30)

async def setup_bot_profile(application):
    try:
        desc = (
            "🔥 India's #1 Loot Deals, Cashback & Price Drop Bot!\n\n"
            "🛍️ Get 80-90% OFF steals on Amazon, Flipkart, Myntra & Ajio.\n"
            "⚡ ₹1 & Under ₹99 Deals, Price Errors & Daily Cashback Tricks.\n"
            "🎁 Refer Friends & Win ₹500 Free Amazon Vouchers.\n\n"
            "Tap START below to unlock exclusive loots! 👇"
        )
        short_desc = "🔥 India's Best Loot Deals, ₹1 & Under ₹99 Steals, Amazon Flipkart 90% Price Drops & Cashback!"
        commands = [
            BotCommand("start", "⚡ Launch Loot Deals & Offers"),
            BotCommand("today", "🔥 Today's 80-90% OFF Top Loots"),
            BotCommand("under99", "📦 Under ₹99 Steal Deals Store"),
            BotCommand("vip", "🌟 VIP Secret Glitch Deals (95% OFF)"),
            BotCommand("refer", "🎁 Refer & Win ₹500 Amazon Gift Cards"),
            BotCommand("leaderboard", "🏆 Top 10 Referral Champions"),
            BotCommand("search", "🔍 Search Deals (e.g. /search shirt)"),
            BotCommand("earn", "💰 Daily Cashback & Earning App"),
            BotCommand("help", "❓ Help & Support")
        ]
        await application.bot.set_my_description(desc)
        await application.bot.set_my_short_description(short_desc)
        await application.bot.set_my_commands(commands)
        logger.info("✅ BotFather SEO commands, description and short description registered successfully!")
    except Exception as e:
        logger.warning(f"Could not auto-register bot profile in BotFather: {e}")

def main():
    if not BOT_TOKEN:
        print("Error: BOT_TOKEN not found!")
        sys.exit(1)

    # Start lightweight health server for cloud platforms (Render, Koyeb, Railway)
    threading.Thread(target=start_health_server, daemon=True).start()
    threading.Thread(target=keep_alive, daemon=True).start()
    threading.Thread(target=launch_under99_bot, daemon=True).start()
    threading.Thread(target=launch_auto_publisher, daemon=True).start()

    while True:
        try:
            app = ApplicationBuilder().token(BOT_TOKEN).post_init(setup_bot_profile).build()

            app.add_handler(CommandHandler("start", start_command))
            app.add_handler(CommandHandler("today", top_loots))
            app.add_handler(CommandHandler("under99", under_99_loots))
            app.add_handler(CommandHandler("vip", vip_deals))
            app.add_handler(CommandHandler("refer", refer_and_earn))
            app.add_handler(CommandHandler("earn", earnkaro_info))
            app.add_handler(CommandHandler("help", help_command))
            app.add_handler(CommandHandler("leaderboard", leaderboard_command))
            app.add_handler(CommandHandler("search", search_command))
            app.add_handler(CommandHandler("stats", admin_stats))
            app.add_handler(CommandHandler("setchannel", admin_set_channel))
            app.add_handler(CommandHandler("broadcast", admin_broadcast))
            app.add_handler(CommandHandler("adddeal", admin_add_deal))

            app.add_handler(CallbackQueryHandler(check_subscription_callback, pattern="^check_subscription$"))
            app.add_handler(CallbackQueryHandler(check_vip_status_callback, pattern="^check_vip_status$"))
            app.add_handler(MessageHandler(filters.TEXT & (~filters.COMMAND), handle_message))

            print("🚀 Loot Deals Bot is running...")
            app.run_polling(drop_pending_updates=True)
        except Exception as e:
            print(f"Polling crashed: {e}. Auto-restarting in 5 seconds...")
            import time
            time.sleep(5)

if __name__ == "__main__":
    main()
