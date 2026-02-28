# Wilkesboro Today - Production Workflow

## Overview
Complete "set and forget" system for managing news, events, and community data with automated publishing workflow.

## Architecture

```
┌─────────────────┐     ┌──────────────┐     ┌─────────────────┐
│  Data Sources   │────▶│  Supabase    │────▶│  Astro Website  │
│  (Cron Jobs)    │     │  (Database)  │     │  (4hr refresh)  │
└─────────────────┘     └──────┬───────┘     └─────────────────┘
                               │
                               ▼
                        ┌──────────────┐
                        │   Telegram   │
                        │  (Approval)  │
                        └──────────────┘
```

## Data Flow

### 1. Data Collection (Every 4 hours)
- **Social Monitor**: Scans news sources → Inserts to `news_items` (status='New')
- **Election Monitor**: Updates candidate info → `candidates`, `races` tables
- **Resource Monitor**: Community resources → `resources` table
- **Job Monitor**: Job postings → `jobs` table

### 2. Approval Workflow (Real-time)
- New items trigger Telegram notification
- You approve/reject via Telegram buttons
- Approved items → status='Approved'
- Rejected items → status='Rejected'

### 3. Publishing (Every 4 hours)
- Astro site fetches approved items from Supabase
- Builds static pages with fresh content
- Deploys to production

### 4. Backup
- Supabase provides automatic backups
- All data centralized, no local markdown dependency

---

## Database Schema (Production)

### Core Tables

#### news_items
```sql
- id (uuid, primary)
- headline (text, required)
- summary (text)
- source (text) - e.g., 'Journal Patriot'
- source_url (text)
- published_date (date)
- category (text) - 'News', 'Event', 'Alert', 'Job'
- status (text) - 'New', 'Pending', 'Approved', 'Published', 'Rejected'
- community (text) - 'Wilkesboro', 'North Wilkesboro'
- county (text) - 'Wilkes', 'Caldwell'
- tags (text[])
- image_url (text)
- wordpress_post_id (int)
- published_url (text)
- sent_to_telegram (boolean)
- telegram_message_id (text)
- created_at (timestamp)
- approved_at (timestamp)
- approved_by (text)
```

#### events
```sql
- id (uuid)
- title (text)
- description (text)
- date_start (date)
- time_start (text)
- venue_name (text)
- city (text)
- status (text)
```

#### candidates (already exists)
```sql
- id (uuid)
- full_name (text)
- party (text)
- incumbent (boolean)
- biography (text)
- photo_url (text)
```

#### resources
```sql
- id (uuid)
- name (text)
- type (text) - 'Gov_Office', 'Nonprofit', 'Business'
- address (text)
- phone (text)
- website (text)
- description (text)
- tags (text[])
```

---

## Cron Jobs (Automated)

### Every 4 Hours
```bash
# 1. Collect new data
0 */4 * * * cd /workspace && python3 collect_news.py >> logs/news.log 2>&1

# 2. Send pending items to Telegram for approval
5 */4 * * * cd /workspace && python3 telegram_approval_bot.py >> logs/telegram.log 2>&1

# 3. Build and deploy website
10 */4 * * * cd /workspace && python3 build_website.py >> logs/build.log 2>&1
```

---

## Telegram Approval Workflow

### New Item Detected
1. System finds item with status='New'
2. Sends Telegram message:
   ```
   📰 New Article for Approval
   
   [Headline]
   [Summary]
   
   Source: [Source]
   Category: [Category]
   
   [✅ Approve] [❌ Reject] [📖 Read More]
   ```

### You Click Button
- **Approve**: status → 'Approved', added to next website build
- **Reject**: status → 'Rejected', archived
- **Read More**: Opens source URL

### Confirmation
```
✅ Article Approved
"[Headline]" will be published in the next build.
```

---

## Website Integration (Astro)

### Build Process
1. Fetch approved news: `SELECT * FROM news_items WHERE status='Approved'`
2. Generate static pages:
   - `/news/` - News listing
   - `/news/[slug]/` - Individual articles
   - `/events/` - Events calendar
   - `/elections/` - Candidate info
3. Deploy to hosting

### Real-time Updates
- Option 1: Static build every 4 hours (simple, reliable)
- Option 2: SSR with Supabase client (instant updates)
- Start with Option 1, upgrade to Option 2 later

---

## Data Cleanup

### Remove Test Data
```sql
-- Delete test records
DELETE FROM news_items WHERE headline LIKE '%Test%' OR headline LIKE '%test%';
DELETE FROM news_items WHERE source = 'System';

-- Delete items with no meaningful content
DELETE FROM news_items WHERE length(headline) < 20;
DELETE FROM news_items WHERE headline IN ('Date:', 'Source:', 'Classification:', '---');
```

### Standardize Data
```sql
-- Fix empty categories
UPDATE news_items SET category = 'News' WHERE category IS NULL OR category = '';

-- Set county based on community
UPDATE news_items SET county = 'Wilkes' WHERE community ILIKE '%wilkes%';
UPDATE news_items SET county = 'Caldwell' WHERE community ILIKE '%caldwell%';
```

---

## Monitoring & Alerts

### Daily Checks
- Database record counts
- Failed cron jobs
- Telegram delivery status
- Website build status

### Weekly Reports
- Articles published
- Approval rate
- Top sources
- Error summary

---

## Documentation

### For You (Operator)
1. **Daily**: Check Telegram for approvals (takes 2 minutes)
2. **Weekly**: Review analytics report
3. **Monthly**: Archive old data, verify backups

### For Developers
1. **Adding new data source**: See `docs/ADDING_SOURCES.md`
2. **Modifying schema**: See `docs/SCHEMA_CHANGES.md`
3. **Troubleshooting**: See `docs/TROUBLESHOOTING.md`

---

## Implementation Checklist

### Phase 1: Foundation (Today)
- [x] Create all database tables
- [x] Migrate existing data
- [ ] Clean test data
- [ ] Set up Telegram bot

### Phase 2: Automation (This Week)
- [ ] Update cron jobs to write to Supabase
- [ ] Build Telegram approval workflow
- [ ] Create Astro website connector
- [ ] Test end-to-end flow

### Phase 3: Production (Next Week)
- [ ] Deploy website
- [ ] Monitor for 48 hours
- [ ] Document everything
- [ ] Train users

---

## Files Created

| File | Purpose |
|------|---------|
| `collect_news.py` | Fetches news from sources |
| `telegram_approval_bot.py` | Sends notifications, handles approvals |
| `build_website.py` | Triggers Astro build and deploy |
| `cleanup_data.py` | Removes test/bad data |
| `monitor.py` | Daily health checks |

---

## Next Steps

1. **Clean the 972 records** in news_items (remove test data)
2. **Set up Telegram approval** workflow
3. **Connect Astro website** to Supabase
4. **Deploy and test**

Ready to proceed?
