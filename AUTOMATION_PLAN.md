# Wilkesboro Today - Content Automation Plan

## Current Status

✅ **Supabase Connected** - Database working with fallback to demo data
✅ **Website Live** - Deployed to Cloudflare Pages
✅ **Image Generation** - Cron job running hourly
⚠️ **Content Updates** - Manual process, needs automation

---

## The Perfect Automation System

### 1. NEWS PIPELINE (Every Hour)

```
RSS Feeds + Social Monitor → Filter → Telegram Approval → Supabase → Website
```

**Sources to Monitor:**
- Journal Patriot RSS
- Wilkes Record RSS
- WXII12 Wilkes County section
- WBTV local news
- NC Government press releases
- Twitter/X local accounts
- Facebook pages (town governments, schools)

**Automation:**
```bash
# Every hour
0 * * * * python3 content_aggregator.py
```

**Script:** `content_aggregator.py`
- Fetches RSS feeds
- Checks for new articles
- Sends to Telegram for approval
- Approved articles → Supabase
- Triggers website rebuild

---

### 2. WEATHER (Every 30 minutes)

```
NWS API → Supabase → Website Widget
```

**Source:** National Weather Service API
**Data:**
- Current conditions
- Hourly forecast
- Severe weather alerts
- 7-day forecast

**Automation:**
```bash
# Every 30 minutes
*/30 * * * * python3 weather_updater.py
```

---

### 3. JOBS (Every 6 hours)

```
NCWorks + County sites + Indeed API → Supabase → Jobs Board
```

**Sources:**
- wilkescounty.net/jobs
- NCWorks Career Center
- Indeed API (local search)
- LinkedIn (local search)

**Automation:**
```bash
# Every 6 hours
0 */6 * * * python3 jobs_scraper.py
```

---

### 4. EVENTS (Daily)

```
Calendar scrapers → Supabase → Events Page
```

**Sources:**
- wilkeschamber.org/events
- town websites
- Facebook events
- venue websites

**Automation:**
```bash
# Daily at 6 AM
0 6 * * * python3 events_scraper.py
```

---

### 5. ALERTS (Real-time)

```
NWS Alerts + County alerts → Immediate notification
```

**Sources:**
- NWS CAP alerts
- Wilkes County alert system
- School closing alerts
- Traffic alerts

**Automation:**
```bash
# Every 5 minutes
*/5 * * * * python3 alert_monitor.py
```

---

## Implementation Plan

### Phase 1: News Automation (This Week)

1. **Set up RSS aggregation**
   - Create `content_aggregator.py`
   - Connect to 10+ news sources
   - Filter by keywords (Wilkes County, local towns)

2. **Telegram approval workflow**
   - Send new stories to your phone
   - Approve/reject with one tap
   - Auto-post approved stories

3. **Auto-rebuild website**
   - New story approved → trigger Cloudflare rebuild
   - Website updates within minutes

### Phase 2: Weather & Jobs (Next Week)

1. **Weather widget**
   - Real-time NWS data
   - Severe weather alerts
   - 7-day forecast

2. **Jobs board**
   - Scrape county website
   - NCWorks integration
   - Filter by category

### Phase 3: Events & Alerts (Week 3)

1. **Events calendar**
   - Scrape multiple sources
   - Auto-categorize
   - Reminder system

2. **Alert system**
   - Real-time notifications
   - SMS/email alerts
   - Website banner alerts

---

## Technical Architecture

```
┌─────────────────┐     ┌──────────────┐     ┌─────────────┐
│  News Sources   │────▶│  Aggregator  │────▶│   Telegram  │
│  (RSS/API)      │     │   (Python)   │     │  (Approval) │
└─────────────────┘     └──────────────┘     └──────┬──────┘
                                                     │
                     ┌───────────────────────────────┘
                     ▼
┌─────────────────┐     ┌──────────────┐     ┌─────────────┐
│   Cloudflare    │◀────│   Supabase   │◀────│   Approved  │
│   Pages (Site)  │     │  (Database)  │     │   Content   │
└─────────────────┘     └──────────────┘     └─────────────┘
        ▲
        │
┌─────────────────┐
│  Rebuild Hook   │
│  (GitHub Action)│
└─────────────────┘
```

---

## Content Update Schedule

| Content Type | Frequency | Source | Automation |
|--------------|-----------|--------|------------|
| Breaking News | Immediate | RSS/Twitter | Telegram → Auto-post |
| Local News | Hourly | RSS feeds | Telegram approval |
| Weather | 30 min | NWS API | Auto-update |
| Jobs | 6 hours | County sites | Auto-scrape |
| Events | Daily | Calendars | Auto-scrape + approval |
| Alerts | 5 min | NWS/County | Immediate notification |

---

## Next Steps

**Want me to build:**

1. **News aggregator** - Pulls from RSS feeds, sends to Telegram
2. **Weather updater** - Real-time weather data
3. **Jobs scraper** - Automated job listings
4. **Alert monitor** - Severe weather/emergency alerts
5. **Auto-rebuild system** - Website updates on new content

Which should I start with?
