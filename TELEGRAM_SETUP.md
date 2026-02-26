# Telegram Approval System Setup

## Overview
Get notified in Telegram when new articles are ready for review. Approve or reject with one tap.

## Step 1: Create Telegram Bot

1. Open Telegram and search for **@BotFather**
2. Start chat and send: `/newbot`
3. Name your bot: `Wilkesboro Today Approval`
4. Choose username: `wilkesboro_approval_bot`
5. **Copy the API token** (starts with numbers:letters)

## Step 2: Get Your Chat ID

1. Search for **@userinfobot** in Telegram
2. Start chat
3. It will reply with your info including **ID**
4. Copy the ID (numbers only)

## Step 3: Add Columns to Supabase

Run this SQL in Supabase SQL Editor:

```sql
-- Add approval workflow columns
ALTER TABLE news_raw ADD COLUMN IF NOT EXISTS approval_status TEXT DEFAULT 'pending';
ALTER TABLE news_raw ADD COLUMN IF NOT EXISTS telegram_notified BOOLEAN DEFAULT false;
ALTER TABLE news_raw ADD COLUMN IF NOT EXISTS telegram_message_id TEXT;
ALTER TABLE news_raw ADD COLUMN IF NOT EXISTS reviewed_by TEXT;
ALTER TABLE news_raw ADD COLUMN IF NOT EXISTS reviewed_at TIMESTAMP WITH TIME ZONE;
ALTER TABLE news_raw ADD COLUMN IF NOT EXISTS reviewer_notes TEXT;
```

## Step 4: Configure Environment

Add to your `.env` file:

```
TELEGRAM_BOT_TOKEN=your_bot_token_here
TELEGRAM_CHAT_ID=your_chat_id_here
```

## Step 5: Test the Bot

```bash
cd /root/.openclaw/workspace
python3 telegram_approval_bot.py
```

You should receive a Telegram message for each pending article.

## Step 6: Set Up Cron (Automatic)

Run every 5 minutes to check for new articles:

```bash
crontab -e
```

Add:
```
*/5 * * * * cd /root/.openclaw/workspace && python3 telegram_approval_bot.py >> logs/telegram_bot.log 2>&1
```

## How It Works

1. **New article** added to `news_raw` table
2. **Cron job** runs every 5 minutes
3. **Bot sends** you a Telegram message with article details
4. **You tap** ✅ Approve or ❌ Reject
5. **Article status** updated in Supabase
6. **Approved articles** appear on website

## Approval Flow

```
New Article → Telegram Notification → You Approve → Published to Site
     ↓
   Reject → Article Archived
```

## Manual Commands (in Telegram)

Send these commands to your bot:
- `/approve_123` - Approve article ID 123
- `/reject_123` - Reject article ID 123

## Webhook Setup (Advanced)

For instant notifications (no cron needed):

1. Set webhook URL:
```bash
curl -X POST "https://api.telegram.org/botYOUR_TOKEN/setWebhook" \
  -d "url=https://your-server.com/webhook"
```

2. Run webhook server:
```bash
python3 telegram_webhook.py
```

## Security Notes

- Keep your bot token secret
- Only you should know your chat ID
- Bot only responds to your chat ID
- All actions are logged

## Troubleshooting

**Not receiving messages?**
- Check bot token is correct
- Verify chat ID is correct
- Start chat with your bot first

**Buttons not working?**
- Check Supabase credentials
- Verify approval_status column exists

**Want to test?**
```bash
# Add test article
python3 -c "
import requests
url = 'https://nahldyqwdqnifyljanxt.supabase.co/rest/v1/news_raw'
headers = {'apikey': 'YOUR_KEY', 'Authorization': 'Bearer YOUR_KEY'}
data = {
    'Title_Original': 'Test Article',
    'Summary_Short': 'This is a test',
    'Category': 'Test',
    'approval_status': 'pending'
}
requests.post(url, headers=headers, json=data)
"

# Run bot
python3 telegram_approval_bot.py
```
