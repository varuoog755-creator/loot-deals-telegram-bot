# Loot Deals & Cashback Telegram Bot

Telegram affiliate bot with viral referral system, force subscribe channel verification, and EarnKaro deals.

## Features
- **Force Subscribe:** Requires joining Telegram channel before unlocking deals
- **Refer & Earn:** Unique referral tracking for viral growth
- **Affiliate Deals:** Top loots & Under ₹99 store
- **Admin Panel:** Broadcast messages, view user stats, add deals

## Environment Variables
- `BOT_TOKEN`: Telegram bot token from @BotFather
- `ADMIN_USER_ID`: Admin Telegram ID (8837364917)
- `CHANNEL_ID`: Channel ID or username (e.g. `@LootDealsCashbackHub`)
- `CHANNEL_INVITE_LINK`: Telegram channel invite link

## Free Hosting (Render / Koyeb)
1. Fork or push this repository to GitHub.
2. Create a new **Web Service** on [Render.com](https://render.com) or [Koyeb.com](https://koyeb.com).
3. Connect your GitHub repository.
4. Set Environment Variables:
   - `BOT_TOKEN`
   - `ADMIN_USER_ID`
   - `CHANNEL_INVITE_LINK`
5. Deploy! The built-in HTTP server responds on port `8080` (or `$PORT`) for health checks.
