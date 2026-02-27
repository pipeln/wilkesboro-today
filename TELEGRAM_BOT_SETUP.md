# Telegram Bot Setup - Step by Step

## Step 1: Create Your Bot

1. **Open Telegram** on your phone or computer
2. **Search for:** `@BotFather`
3. **Start a chat** with BotFather
4. **Send this message:** `/newbot`
5. **BotFather will ask for a name:**
   - Type: `Wilkesboro Today News`
6. **BotFather will ask for a username:**
   - Type: `wilkesboro_news_bot` (must end in 'bot', all lowercase)
7. **Copy the API token** BotFather gives you
   - Looks like: `123456789:ABCdefGHIjklMNOpqrSTUvwxyz`

## Step 2: Get Your Chat ID

1. **Search for:** `@userinfobot`
2. **Start a chat** with it
3. **It will reply with your info:**
   ```
   @yourusername
   Id: 123456789
   First: Your
   Last: Name
   ```
4. **Copy the number after "Id:"** - this is your chat ID

## Step 3: Add Credentials

**Edit the .env file:**

```bash
nano /root/.openclaw/workspace/.env
```

**Add these lines:**
```
TELEGRAM_BOT_TOKEN=123456789:ABCdefGHIjklMNOpqrSTUvwxyz
TELEGRAM_CHAT_ID=123456789
```

**Save:** Press Ctrl+X, then Y, then Enter

## Step 4: Test Your Bot

**Send a test message:**
```bash
curl -X POST "https://api.telegram.org/botYOUR_TOKEN/sendMessage" \
  -d "chat_id=YOUR_CHAT_ID" \
  -d "text=Test message from Wilkesboro Today"
```

**You should receive the message in Telegram.**

## Step 5: Start the Aggregator

**Run manually first:**
```bash
cd /root/.openclaw/workspace
python3 rss_aggregator.py
```

**You should receive Telegram notifications for new articles.**

## Step 6: Set Up Automatic Hourly Checks

```bash
crontab -e
```

**Add this line:**
```
0 * * * * cd /root/.openclaw/workspace && python3 rss_aggregator.py >> logs/aggregator.log 2>&1
```

**Save and exit.**

## Step 7: Test Approval

**When you get a Telegram message:**
1. Click or type: `/approve_123` (replace 123 with actual ID)
2. Article publishes immediately
3. Check website in 2-3 minutes

## Troubleshooting

**Bot not responding?**
- Make sure you started a chat with the bot
- Check token is correct
- Try: `curl https://api.telegram.org/botYOUR_TOKEN/getMe`

**Not receiving messages?**
- Verify chat ID is correct
- Check you sent `/start` to the bot

**Commands not working?**
- Make sure you're using the exact format: `/approve_123`
- Check article ID exists in message

## Your Bot Commands

Once set up, you can use:
- `/approve_ID` - Quick publish
- `/approve_image_ID` - Publish with new AI image
- `/reject_ID` - Discard article
- `/help` - Show commands

---

**Ready? Start with Step 1 - message @BotFather now!**
