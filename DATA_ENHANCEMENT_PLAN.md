# Wilkes County Data Enhancement Strategy

## The Problem

Current `populate_aitable.py` only sends:
- `Title` (minimal)
- `Source` (not even in schema — should be `Source_Name`)
- `Date` (should be `Date_Original`)
- `Category` 
- `Status` = "New"

**Missing:** URLs, full text, locations, proper categorization, summaries.

---

## Phase 1: Fix the Data Pipeline (Immediate - Free)

### A. Enhanced Web Scraping (No API Costs)

Use `web_fetch` tool which extracts readable content from any URL:

```python
# Enhanced scraping pattern
import requests
from bs4 import BeautifulSoup

def scrape_with_fallback(url):
    """Try multiple methods to get full content."""
    
    # Method 1: Direct fetch with newspaper3k-style extraction
    try:
        response = requests.get(url, headers={
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
        }, timeout=15)
        soup = BeautifulSoup(response.content, 'html.parser')
        
        # Remove noise
        for tag in soup(['script', 'style', 'nav', 'header', 'footer', 'aside']):
            tag.decompose()
        
        # Get article content
        article = soup.find('article') or soup.find('main') or soup.find('div', class_='content')
        if article:
            return {
                'title': soup.title.string if soup.title else '',
                'body': article.get_text(separator='\n', strip=True)[:5000],
                'url': url
            }
    except Exception as e:
        print(f"Direct scrape failed: {e}")
    
    return None
```

### B. RSS Feed Integration (Free & Reliable)

**Wilkes County RSS Sources:**

| Source | RSS URL | Type |
|--------|---------|------|
| Wilkes County Gov | `https://www.wilkescounty.net/RSSFeed.aspx?ModID=1&CID=All-news.xml` | News |
| Journal Patriot | `https://www.journalpatriot.com/search/?f=rss&t=article&c=news/local*&l=25&s=start_time&sd=desc` | Local News |
| Wilkes Record | `https://www.thewilkesrecord.com/search/?f=rss&t=article&c=news*&l=25&s=start_time&sd=desc` | News |
| WXII 12 | `https://www.wxii12.com/wilkes-county/rss` | TV News |
| NC Board of Elections | `https://www.ncsbe.gov/news/feed` | Elections |

**Python RSS Parser:**

```python
import feedparser
from datetime import datetime

def parse_rss_feed(feed_url, source_name):
    """Parse RSS and return structured records."""
    feed = feedparser.parse(feed_url)
    records = []
    
    for entry in feed.entries[:10]:  # Last 10 items
        record = {
            'Title_Original': entry.get('title', ''),
            'Body_Original': entry.get('summary', entry.get('description', ''))[:3000],
            'Source_URL': entry.get('link', ''),
            'Source_Name': source_name,
            'Date_Original': parse_date(entry.get('published', '')),
            'Source_Type': 'Local_Media',
            'Status': 'New',
            'Category': auto_categorize(entry.get('title', ''))
        }
        records.append(record)
    
    return records

def auto_categorize(title):
    """Auto-assign category based on keywords."""
    title_lower = title.lower()
    keywords = {
        'Schools': ['school', 'student', 'superintendent', 'education', 'teacher'],
        'Public_Safety': ['sheriff', 'police', 'fire', 'emergency', 'crash', 'shooting', 'arrest'],
        'Civics': ['commissioner', 'council', 'meeting', 'election', 'vote', 'board'],
        'Business': ['business', 'economy', 'jobs', 'hiring', 'store', 'restaurant']
    }
    for category, words in keywords.items():
        if any(word in title_lower for word in words):
            return category
    return 'Community'
```

---

## Phase 2: Facebook Group Monitoring (Free Workarounds)

**The Hard Truth:** Facebook actively blocks scraping. Official API requires $$$ and business verification.

### Workaround Options:

#### Option A: RSS Bridge (Self-Hosted, Free)

RSS-Bridge can convert Facebook pages/groups to RSS feeds:

```bash
# Deploy RSS-Bridge via Docker (free)
docker run -d -p 3000:80 rssbridge/rss-bridge:latest

# Then access:
# http://localhost:3000/?action=display&bridge=Facebook&context=Group&g=GROUP_ID&format=Atom
```

**Limitations:** 
- Only works for public groups
- Facebook rate-limits heavily
- Requires technical setup

#### Option B: Manual + Community Input (Recommended)

Create a simple submission workflow:

1. **AITable Form** for residents to submit events/tips
2. **Telegram Bot** for quick mobile submissions
3. **Email** for longer submissions

```python
# Check AITable Submissions table for new entries
def check_community_submissions():
    """Poll Submissions table for new Facebook-sourced tips."""
    # Query AITable for Status='New' and Source_Channel='Facebook'
    # Process and move to Events/News_Raw
```

#### Option C: Nitter-Style Alternative (Unreliable)

Some Facebook wrapper services exist but break often. Not recommended for production.

---

## Phase 3: Enhanced Data Pipeline Script

Here's a complete replacement for `populate_aitable.py`:

```python
#!/usr/bin/env python3
"""
Enhanced AITable population with full content extraction.
"""

import requests
import feedparser
import json
from datetime import datetime
from bs4 import BeautifulSoup

API_TOKEN = "uskNPM9fPVHOgAGbDepyKER"
BASE_URL = "https://aitable.ai/api/v1"
HEADERS = {
    "Authorization": f"Bearer {API_TOKEN}",
    "Content-Type": "application/json"
}

DATASHEETS = {
    "News_Raw": "dstjSJ3rvilwBd3Bae",
    "Events": "dstnnbs9qm9DZJkt8L",
    "Resources": "dstRRB7Fi8ZVP7eRcS"
}

# RSS Sources for Wilkes County
RSS_SOURCES = [
    {"url": "https://www.wilkescounty.net/RSSFeed.aspx?ModID=1&CID=All-news.xml", "name": "Wilkes County Gov", "type": "Gov"},
    {"url": "https://www.journalpatriot.com/search/?f=rss&t=article&c=news/local*&l=10&s=start_time&sd=desc", "name": "Journal Patriot", "type": "Local_Media"},
    {"url": "https://www.thewilkesrecord.com/search/?f=rss&t=article&c=news*&l=10&s=start_time&sd=desc", "name": "Wilkes Record", "type": "Local_Media"},
]

def fetch_full_content(url):
    """Extract full article content from URL."""
    try:
        resp = requests.get(url, headers={'User-Agent': 'Mozilla/5.0'}, timeout=15)
        soup = BeautifulSoup(resp.content, 'html.parser')
        
        # Remove script/style
        for tag in soup(['script', 'style', 'nav', 'header', 'footer']):
            tag.decompose()
        
        # Find main content
        content = soup.find('article') or soup.find('main') or soup.find('div', class_=re.compile('content|article'))
        if content:
            return content.get_text(separator='\n', strip=True)[:5000]
        return soup.body.get_text(separator='\n', strip=True)[:3000] if soup.body else ''
    except Exception as e:
        print(f"  ⚠ Could not fetch full content: {e}")
        return ''

def parse_date(date_str):
    """Parse various date formats to ISO."""
    formats = [
        '%a, %d %b %Y %H:%M:%S %z',
        '%Y-%m-%dT%H:%M:%S',
        '%B %d, %Y',
        '%m/%d/%Y'
    ]
    for fmt in formats:
        try:
            return datetime.strptime(date_str[:25], fmt).isoformat()
        except:
            continue
    return datetime.now().isoformat()

def auto_categorize(title, body=''):
    """Smart categorization based on content."""
    text = (title + ' ' + body).lower()
    categories = {
        'Schools': ['school', 'student', 'superintendent', 'education', 'teacher', 'graduation'],
        'Public_Safety': ['sheriff', 'police', 'fire', 'emergency', 'crash', 'shooting', 'arrest', 'death', 'investigation'],
        'Civics': ['commissioner', 'council', 'meeting', 'election', 'vote', 'board', 'hearing', 'ordinance'],
        'Business': ['business', 'economy', 'jobs', 'hiring', 'store', 'restaurant', 'opening', 'closing']
    }
    for cat, keywords in categories.items():
        if any(kw in text for kw in keywords):
            return cat
    return 'Community'

def extract_event_info(title, body, url):
    """Try to extract event details from news article."""
    import re
    
    # Date patterns
    date_patterns = [
        r'(January|February|March|April|May|June|July|August|September|October|November|December)\s+\d{1,2}',
        r'\d{1,2}/\d{1,2}/\d{2,4}',
        r'\d{1,2}-\d{1,2}-\d{2,4}'
    ]
    
    # Time patterns
    time_patterns = [
        r'\d{1,2}:\d{2}\s*(AM|PM|am|pm)',
        r'\d{1,2}\s*(AM|PM|am|pm)'
    ]
    
    dates_found = []
    times_found = []
    
    for pattern in date_patterns:
        matches = re.findall(pattern, body, re.IGNORECASE)
        dates_found.extend(matches)
    
    for pattern in time_patterns:
        matches = re.findall(pattern, body, re.IGNORECASE)
        times_found.extend(matches)
    
    return {
        'has_event': len(dates_found) > 0 and any(word in body.lower() for word in ['meeting', 'event', 'scheduled', 'hearing']),
        'dates': dates_found[:2],
        'times': times_found[:2]
    }

def process_rss_feeds():
    """Fetch and process all RSS sources."""
    all_records = []
    
    for source in RSS_SOURCES:
        print(f"\n📡 Processing: {source['name']}")
        try:
            feed = feedparser.parse(source['url'])
            
            for entry in feed.entries[:5]:  # Last 5 items per source
                print(f"  → {entry.get('title', 'Untitled')[:60]}...")
                
                # Get full content if possible
                full_body = entry.get('summary', '')
                article_url = entry.get('link', '')
                
                if article_url:
                    fetched = fetch_full_content(article_url)
                    if fetched:
                        full_body = fetched
                
                # Build complete record
                record = {
                    'Title_Original': entry.get('title', ''),
                    'Body_Original': full_body[:4000],
                    'Source_URL': article_url,
                    'Source_Name': source['name'],
                    'Source_Type': source['type'],
                    'Date_Original': parse_date(entry.get('published', '')),
                    'Category': auto_categorize(entry.get('title', ''), full_body),
                    'Status': 'New',
                    'Location': extract_location(full_body),
                    'Notes': f"Auto-imported from RSS on {datetime.now().strftime('%Y-%m-%d')}"
                }
                
                # Check if it's an event
                event_info = extract_event_info(record['Title_Original'], full_body, article_url)
                if event_info['has_event']:
                    record['Tags'] = 'Event_Detected'
                
                all_records.append(record)
                
        except Exception as e:
            print(f"  ✗ Error: {e}")
    
    return all_records

def extract_location(text):
    """Extract location mentions from text."""
    locations = ['Wilkesboro', 'North Wilkesboro', 'Ronda', 'Hays', 'Millers Creek', 
                 'Purlear', 'Ferguson', 'Moravian Falls']
    found = [loc for loc in locations if loc.lower() in text.lower()]
    return ', '.join(found) if found else 'Wilkes County'

def create_records(datasheet_id, records):
    """Batch create records in AITable."""
    url = f"{BASE_URL}/datasheets/{datasheet_id}/records"
    
    # AITable has batch limits, process in chunks
    chunk_size = 10
    created = 0
    
    for i in range(0, len(records), chunk_size):
        chunk = records[i:i + chunk_size]
        payload = {"records": [{"fields": r} for r in chunk]}
        
        try:
            response = requests.post(url, headers=HEADERS, json=payload)
            if response.status_code == 200:
                created += len(chunk)
                print(f"  ✓ Created {len(chunk)} records")
            else:
                print(f"  ✗ API error: {response.status_code} - {response.text[:200]}")
        except Exception as e:
            print(f"  ✗ Request failed: {e}")
    
    return created

def main():
    print("="*60)
    print("WILKES COUNTY - Enhanced AITable Population")
    print("="*60)
    
    # Process RSS feeds
    news_records = process_rss_feeds()
    
    print(f"\n📊 Found {len(news_records)} news items")
    
    # Create in AITable
    if news_records:
        print(f"\n💾 Saving to AITable...")
        created = create_records(DATASHEETS["News_Raw"], news_records)
        print(f"\n✅ Successfully created {created} records")
    
    # TODO: Process Events (from detected events)
    # TODO: Process Resources (from static list + submissions)
    
    print("\n" + "="*60)

if __name__ == "__main__":
    main()
```

---

## Phase 4: Deployment & Automation

### Install Dependencies

```bash
pip install feedparser beautifulsoup4 requests
```

### Cron Schedule

```bash
# Run every 2 hours during day
0 8,10,12,14,16,18 * * * cd /root/.openclaw/workspace && python3 enhanced_populate.py >> logs/populate.log 2>&1
```

---

## Summary: What You Get

| Before | After |
|--------|-------|
| Title only | Full article text |
| No URLs | Source URLs for everything |
| Manual categorization | Auto-categorized by keywords |
| No dates | Parsed publication dates |
| No location | Auto-extracted locations |
| Static data | Live RSS feeds |
| Missing events | Event detection from articles |

**Facebook:** Use community submissions via AITable form + Telegram bot instead of scraping.

Want me to implement any of these phases?
