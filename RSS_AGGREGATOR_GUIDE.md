# RSS Aggregator + Telegram Approval System

## What It Does

1. **Fetches news** from RSS feeds every hour
2. **Sends to Telegram** for your approval
3. **You choose:**
   - ✅ Approve (uses existing/default image)
   - 🖼 Approve + New Image (generates fresh image)
   - ❌ Reject (discards)
4. **Auto-publishes** to website
5. **Triggers rebuild** so story appears immediately

---

## Setup

### 1. Install Dependencies

```bash
cd /root/.openclaw/workspace
pip3 install feedparser requests --break-system-packages
```

### 2. Set Environment Variables

Edit `/root/.openclaw/workspace/.env`:

```
SUPABASE_URL=https://nahldyqwdqnifyljanxt.supabase.co
SUPABASE_ANON_KEY=your_key
TELEGRAM_BOT_TOKEN=your_bot_token
TELEGRAM_CHAT_ID=your_chat_id
GEMINI_API_KEY=your_gemini_key
```

### 3. Set Up Cron (Run Every Hour)

```bash
crontab -e
```

Add this line:
```
0 * * * * cd /root/.openclaw/workspace && python3 rss_aggregator.py >> logs/aggregator.log 2>&1
```

---

## How to Use

### When You Get a Telegram Message:

**Option 1: Quick Approve**
```
/approve_123
```
- Publishes immediately
- Uses default image

**Option 2: Approve with New Image**
```
/approve_image_123
```
- Generates fresh AI image
- Then publishes

**Option 3: Reject**
```
/reject_123 Wrong category
```
- Discards article
- Optional reason

---

## Workflow

```
RSS Feed → Aggregator → Telegram → You Approve → Supabase → Website
                ↓
         (Every Hour)
```

**Time from approval to website:** 2-3 minutes

---

## RSS Sources Monitored

| Source | Category | URL |
|--------|----------|-----|
| Journal Patriot | News | journalpatriot.com |
| Wilkes Record | News | thewilkesrecord.com |
| WXII12 | News | wxii12.com/wilkes-county |
| Wilkes County Gov | Government | wilkescounty.net |

**To add more:** Edit `RSS_SOURCES` in `rss_aggregator.py`

---

## Testing

### Test RSS Fetch:
```bash
python3 rss_aggregator.py
```

### Test Telegram Command:
```bash
python3 telegram_handler.py '/approve_123'
```

### Test Image Generation:
```bash
python3 telegram_handler.py '/approve_image_123'
```

---

## Troubleshooting

**No Telegram messages?**
- Check bot token
- Check chat ID
- Start chat with bot first

**Articles not publishing?**
- Check Supabase credentials
- Check article ID exists

**Images not generating?**
- Check Gemini API key
- Check rate limits

---

## Next Steps

1. ✅ Set up Telegram bot
2. ✅ Add credentials to .env
3. ✅ Test RSS aggregator
4. ✅ Set up cron job
5. 🔄 Start receiving approvals!

Ready to test?
