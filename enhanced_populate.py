#!/usr/bin/env python3
"""
Enhanced AITable population with full content extraction from RSS feeds.
Replaces the minimal populate_aitable.py with rich data.
"""

import requests
import feedparser
import json
import re
import time
import random
from datetime import datetime
from bs4 import BeautifulSoup

# AITable Configuration
API_TOKEN = "uskNPM9fPVHOgAGbDepyKER"
BASE_URL = "https://aitable.ai/api/v1"
HEADERS = {
    "Authorization": f"Bearer {API_TOKEN}",
    "Content-Type": "application/json"
}

DATASHEETS = {
    "News_Raw": "dstjSJ3rvilwBd3Bae",
    "Events": "dstnnbs9qm9DZJkt8L",
    "Resources": "dstRRB7Fi8ZVP7eRcS",
    "Submissions": "dstD2x1pp48NxsMCjs"
}

# RSS Sources for North Carolina State News
# Note: Some sources require residential IP or have aggressive bot protection
RSS_SOURCES = [
    # === LOCAL / WILKES COUNTY ===
    {
        "url": "https://www.wilkescounty.net/RSSFeed.aspx?ModID=1&CID=All-news.xml",
        "name": "Wilkes County Government",
        "type": "Gov",
        "category_map": {"meeting": "Civics", "board": "Civics", "commissioner": "Civics"},
        "delay": 0,
        "enabled": True
    },
    {
        "url": "https://www.journalpatriot.com/search/?f=rss&t=article&c=news/local*&l=10&s=start_time&sd=desc",
        "name": "Journal Patriot",
        "type": "Local_Media",
        "category_map": {},
        "delay": 10,
        "enabled": True,
        "fallback_method": "email_submissions"
    },
    {
        "url": "https://www.thewilkesrecord.com/search/?f=rss&t=article&c=news*&l=10&s=start_time&sd=desc",
        "name": "Wilkes Record",
        "type": "Local_Media",
        "category_map": {},
        "delay": 10,
        "enabled": True,
        "fallback_method": "email_submissions"
    },
    {
        "url": "https://www.wxii12.com/wilkes-county/rss",
        "name": "WXII 12 News",
        "type": "Local_Media",
        "category_map": {},
        "delay": 15,
        "enabled": False,
        "note": "Geo-blocked from server - use email forwarding instead"
    },
    
    # === ASHEVILLE / WNC ===
    {
        "url": "https://mountainx.com/feed/",
        "name": "Mountain Xpress",
        "type": "Local_Media",
        "category_map": {},
        "delay": 5,
        "enabled": True
    },
    {
        "url": "https://www.buncombenc.gov/CivicAlerts.aspx?CID=1",
        "name": "Buncombe County Government",
        "type": "Gov",
        "category_map": {},
        "delay": 5,
        "enabled": True
    },
    
    # === BOONE / WATAUGA ===
    {
        "url": "https://www.wataugademocrat.com/rss",
        "name": "Watauga Democrat",
        "type": "Local_Media",
        "category_map": {},
        "delay": 10,
        "enabled": True
    },
    
    # === CHARLOTTE ===
    {
        "url": "https://www.wcnc.com/rss",
        "name": "WCNC Charlotte",
        "type": "Local_Media",
        "category_map": {},
        "delay": 8,
        "enabled": True
    },
    {
        "url": "https://www.charlotteobserver.com/news/local/rss",
        "name": "Charlotte Observer",
        "type": "Local_Media",
        "category_map": {},
        "delay": 10,
        "enabled": True
    },
    
    # === WINSTON-SALEM / GREENSBORO ===
    {
        "url": "https://journalnow.com/rss",
        "name": "Winston-Salem Journal",
        "type": "Local_Media",
        "category_map": {},
        "delay": 10,
        "enabled": True
    },
    {
        "url": "https://www.greensboro.com/rss",
        "name": "Greensboro News & Record",
        "type": "Local_Media",
        "category_map": {},
        "delay": 10,
        "enabled": True
    },
    {
        "url": "https://www.wfmynews2.com/rss",
        "name": "WFMY News 2",
        "type": "Local_Media",
        "category_map": {},
        "delay": 8,
        "enabled": True
    },
    
    # === RALEIGH / TRIANGLE ===
    {
        "url": "https://www.newsobserver.com/news/local/rss",
        "name": "News & Observer",
        "type": "Local_Media",
        "category_map": {},
        "delay": 10,
        "enabled": True
    },
    {
        "url": "https://www.wral.com/rss",
        "name": "WRAL",
        "type": "Local_Media",
        "category_map": {},
        "delay": 8,
        "enabled": True
    },
    {
        "url": "https://abc11.com/rss",
        "name": "ABC11 WTVD",
        "type": "Local_Media",
        "category_map": {},
        "delay": 8,
        "enabled": True
    },
    
    # === STATEWIDE / NC GOVERNMENT ===
    {
        "url": "https://www.ncleg.gov/rss",
        "name": "NC Legislature",
        "type": "Gov",
        "category_map": {},
        "delay": 5,
        "enabled": True
    },
    {
        "url": "https://www.ncdoi.gov/ncdoigov-rss-feeds",
        "name": "NC Department of Insurance",
        "type": "Gov",
        "category_map": {},
        "delay": 5,
        "enabled": True
    },
    
    # === WEATHER ===
    {
        "url": "https://www.weather.gov/rss/",
        "name": "National Weather Service",
        "type": "Gov",
        "category_map": {},
        "delay": 10,
        "enabled": True
    }
]


def fetch_full_content(url, delay=0):
    """Extract full article content from URL with fallback and rate limiting."""
    if not url:
        return ""
    
    # Add delay before request if specified
    if delay > 0:
        time.sleep(delay + random.uniform(0.5, 1.5))  # Add jitter
    
    try:
        resp = requests.get(url, headers={
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
            'Accept-Language': 'en-US,en;q=0.5',
            'Accept-Encoding': 'gzip, deflate, br',
            'DNT': '1',
            'Connection': 'keep-alive',
        }, timeout=20)
        resp.raise_for_status()
        
        soup = BeautifulSoup(resp.content, 'html.parser')
        
        # Remove noise elements
        for tag in soup(['script', 'style', 'nav', 'header', 'footer', 'aside', 'iframe', 'noscript']):
            tag.decompose()
        
        # Try to find main content area
        content_selectors = [
            'article',
            'main',
            '[role="main"]',
            '.content',
            '.article-content',
            '.entry-content',
            '.post-content',
            '#content'
        ]
        
        content = None
        for selector in content_selectors:
            content = soup.select_one(selector)
            if content:
                break
        
        # Fallback to body if no content area found
        if not content and soup.body:
            content = soup.body
        
        if content:
            text = content.get_text(separator='\n', strip=True)
            # Clean up excessive whitespace
            text = re.sub(r'\n{3,}', '\n\n', text)
            return text[:5000]  # Limit to 5000 chars
            
    except Exception as e:
        print(f"    ⚠ Could not fetch full content: {e}")
    
    return ""


def parse_date(date_str):
    """Parse various date formats to ISO 8601."""
    if not date_str:
        return datetime.now().isoformat()
    
    formats = [
        '%a, %d %b %Y %H:%M:%S %z',
        '%a, %d %b %Y %H:%M:%S %Z',
        '%Y-%m-%dT%H:%M:%S%z',
        '%Y-%m-%dT%H:%M:%S',
        '%B %d, %Y',
        '%b %d, %Y',
        '%m/%d/%Y',
        '%m/%d/%y'
    ]
    
    for fmt in formats:
        try:
            # Try parsing with timezone info
            dt = datetime.strptime(date_str.strip()[:30], fmt)
            return dt.isoformat()
        except:
            continue
    
    # Fallback to current time
    return datetime.now().isoformat()


def auto_categorize(title, body=''):
    """Smart categorization based on content analysis."""
    text = (title + ' ' + body).lower()
    
    categories = {
        'Schools': ['school', 'student', 'superintendent', 'education', 'teacher', 'graduation', 'classroom', 'board of education'],
        'Public_Safety': ['sheriff', 'police', 'fire', 'emergency', 'crash', 'shooting', 'arrest', 'death', 'investigation', 'ambulance', 'rescue'],
        'Civics': ['commissioner', 'council', 'meeting', 'election', 'vote', 'board', 'hearing', 'ordinance', 'public hearing', 'town hall'],
        'Business': ['business', 'economy', 'jobs', 'hiring', 'store', 'restaurant', 'opening', 'closing', 'downtown', 'plaza'],
        'Community': ['festival', 'event', 'parade', 'concert', 'library', 'park', 'recreation']
    }
    
    scores = {}
    for cat, keywords in categories.items():
        score = sum(1 for kw in keywords if kw in text)
        if score > 0:
            scores[cat] = score
    
    if scores:
        return max(scores, key=scores.get)
    
    return 'Community'


def extract_location(text):
    """Extract location mentions from text."""
    locations = [
        'Wilkesboro', 'North Wilkesboro', 'Ronda', 'Hays', 
        'Millers Creek', 'Purlear', 'Ferguson', 'Moravian Falls',
        'Boomer', 'Traphill', 'Roaring River', 'McGrady'
    ]
    found = [loc for loc in locations if loc.lower() in text.lower()]
    return ', '.join(found) if found else 'Wilkes County'


def extract_event_details(title, body):
    """Extract potential event information from article."""
    text = title + ' ' + body
    
    # Date patterns
    date_patterns = [
        (r'(January|February|March|April|May|June|July|August|September|October|November|December)\s+(\d{1,2})(?:,\s+(\d{4}))?', 'month_day'),
        (r'(\d{1,2})/(\d{1,2})(?:/(\d{2,4}))?', 'mdy'),
        (r'(\d{1,2})-(\d{1,2})-(\d{2,4})', 'ymd_dash')
    ]
    
    # Time patterns
    time_patterns = [
        r'(\d{1,2}:\d{2}\s*(?:AM|PM|am|pm))',
        r'(\d{1,2}\s*(?:AM|PM|am|pm))'
    ]
    
    dates_found = []
    times_found = []
    
    for pattern, fmt in date_patterns:
        matches = re.findall(pattern, text, re.IGNORECASE)
        dates_found.extend(matches)
    
    for pattern in time_patterns:
        matches = re.findall(pattern, text, re.IGNORECASE)
        times_found.extend(matches)
    
    # Check if article mentions meetings/events
    event_keywords = ['meeting', 'hearing', 'scheduled', 'agenda', 'council', 'board', 'session']
    is_event = any(kw in text.lower() for kw in event_keywords) and len(dates_found) > 0
    
    return {
        'is_event': is_event,
        'dates': dates_found[:2],
        'times': times_found[:2]
    }


def create_short_summary(title, body, max_chars=120):
    """Create a short summary for quick scanning."""
    # Use first sentence or first 120 chars
    sentences = body.split('.')
    if sentences and len(sentences[0]) > 20:
        summary = sentences[0].strip()
    else:
        summary = body[:max_chars]
    
    return summary[:max_chars] + ('...' if len(summary) > max_chars else '')


def process_rss_feeds():
    """Fetch and process all RSS sources with rate limiting."""
    all_records = []
    
    for i, source in enumerate(RSS_SOURCES):
        # Skip disabled sources
        if not source.get('enabled', True):
            print(f"\n📡 {source['name']}: [DISABLED]")
            if 'note' in source:
                print(f"   ℹ {source['note']}")
            continue
        
        print(f"\n📡 Processing: {source['name']}")
        print(f"   URL: {source['url'][:60]}...")
        
        # Add delay between sources (not before first one)
        if i > 0:
            delay = source.get('delay', 3)
            jitter = random.uniform(1.0, 3.0)  # Increased jitter
            total_delay = delay + jitter
            print(f"   ⏱ Rate limit: waiting {total_delay:.1f}s...")
            time.sleep(total_delay)
        
        try:
            # Add headers to avoid being blocked
            feedparser_headers = {
                'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
                'Accept': 'application/rss+xml,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
                'Accept-Language': 'en-US,en;q=0.9',
                'Accept-Encoding': 'gzip, deflate, br',
                'Referer': 'https://www.google.com/',
                'DNT': '1',
            }
            
            # Parse feed
            feed = feedparser.parse(source['url'], request_headers=feedparser_headers)
            
            # Check for HTTP errors in feed
            if hasattr(feed, 'status') and feed.status >= 400:
                print(f"   ⚠ HTTP {feed.status} error")
                if feed.status == 429:
                    print(f"   ⚠ Rate limited - will retry next run")
                elif feed.status == 403:
                    print(f"   ⚠ Access forbidden (bot detection)")
                elif feed.status == 451:
                    print(f"   ⚠ Geo-blocked (requires US IP)")
                
                # Log fallback suggestion
                if source.get('fallback_method'):
                    print(f"   💡 Fallback: {source['fallback_method']}")
                continue
            
            if not feed.entries:
                print(f"   ⚠ No entries found")
                continue
            
            print(f"   ✓ Found {len(feed.entries)} entries")
            
            for entry in feed.entries[:5]:  # Reduced to 5 items per source to be gentle
                title = entry.get('title', 'Untitled')
                print(f"   → {title[:50]}...")
                
                # Get article URL
                article_url = entry.get('link', '')
                
                # Get summary from RSS
                rss_summary = entry.get('summary', entry.get('description', ''))
                
                # Try to fetch full content with source-specific delay
                content_delay = source.get('delay', 0)
                full_body = fetch_full_content(article_url, delay=content_delay)
                if not full_body:
                    full_body = rss_summary
                
                # Clean up HTML if present
                if '<' in full_body:
                    soup = BeautifulSoup(full_body, 'html.parser')
                    full_body = soup.get_text(separator=' ', strip=True)
                
                # Build complete record matching schema
                record = {
                    'Title_Original': title,
                    'Body_Original': full_body[:4000] if full_body else rss_summary[:2000],
                    'Source_URL': article_url,
                    'Source_Name': source['name'],
                    'Source_Type': source['type'],
                    'Date_Original': parse_date(entry.get('published', entry.get('pubDate', ''))),
                    'Category': auto_categorize(title, full_body),
                    'Status': 'New',
                    'Location': extract_location(full_body or title),
                    'Summary_Short': create_short_summary(title, full_body or rss_summary),
                    'Notes': f"Auto-imported via RSS on {datetime.now().strftime('%Y-%m-%d %H:%M')}"
                }
                
                # Check if this might be an event
                event_info = extract_event_details(title, full_body)
                if event_info['is_event']:
                    record['Notes'] += f" | EVENT_DETECTED: dates={event_info['dates']}, times={event_info['times']}"
                
                all_records.append(record)
                
                # Small delay between individual article fetches
                if content_delay > 0:
                    time.sleep(random.uniform(1.0, 2.0))
                
        except Exception as e:
            print(f"   ✗ Error processing feed: {e}")
    
    return all_records


def create_records(datasheet_id, records):
    """Batch create records in AITable with chunking."""
    url = f"{BASE_URL}/datasheets/{datasheet_id}/records"
    
    # AITable API has limits, process in chunks of 10
    chunk_size = 10
    created_count = 0
    
    for i in range(0, len(records), chunk_size):
        chunk = records[i:i + chunk_size]
        payload = {"records": [{"fields": r} for r in chunk]}
        
        try:
            response = requests.post(url, headers=HEADERS, json=payload)
            
            if response.status_code == 200:
                created_count += len(chunk)
                print(f"   ✓ Created {len(chunk)} records")
            else:
                print(f"   ✗ API error {response.status_code}: {response.text[:300]}")
                
        except Exception as e:
            print(f"   ✗ Request failed: {e}")
    
    return created_count


def main():
    print("="*70)
    print(" NORTH CAROLINA STATE NEWS - Enhanced AITable Population")
    print(" Rich data extraction from RSS feeds")
    print("="*70)
    
    # Process RSS feeds
    news_records = process_rss_feeds()
    
    print(f"\n📊 Total records to create: {len(news_records)}")
    
    if news_records:
        print(f"\n💾 Saving to AITable News_Raw...")
        created = create_records(DATASHEETS["News_Raw"], news_records)
        print(f"\n✅ Successfully created {created}/{len(news_records)} records")
        
        # Summary by source
        by_source = {}
        for r in news_records:
            src = r['Source_Name']
            by_source[src] = by_source.get(src, 0) + 1
        
        print("\n📈 By Source:")
        for src, count in by_source.items():
            print(f"   {src}: {count}")
        
        # Summary by category
        by_cat = {}
        for r in news_records:
            cat = r['Category']
            by_cat[cat] = by_cat.get(cat, 0) + 1
        
        print("\n📈 By Category:")
        for cat, count in by_cat.items():
            print(f"   {cat}: {count}")
    else:
        print("\n⚠ No records to create")
    
    print("\n" + "="*70)


if __name__ == "__main__":
    main()
