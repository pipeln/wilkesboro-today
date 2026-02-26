#!/usr/bin/env python3
"""
Sync blogwatcher articles to AITable
Scans for new articles and adds them to News_Raw datasheet
"""

import subprocess
import json
import re
import requests
from datetime import datetime

# AITable Configuration
AITABLE_TOKEN = "uskNPM9fPVHOgAGbDepyKER"
AITABLE_BASE = "https://aitable.ai/api/v1"
HEADERS = {
    "Authorization": f"Bearer {AITABLE_TOKEN}",
    "Content-Type": "application/json"
}

DATASHEET_ID = "dstjSJ3rvilwBd3Bae"  # News_Raw


def get_blogwatcher_articles():
    """Get unread articles from blogwatcher."""
    try:
        result = subprocess.run(
            ["blogwatcher", "articles", "--json"],
            capture_output=True,
            text=True,
            timeout=30
        )
        
        if result.returncode != 0:
            print(f"Error running blogwatcher: {result.stderr}")
            return []
        
        # Parse JSON output
        articles = json.loads(result.stdout)
        return articles
    except Exception as e:
        print(f"Error getting articles: {e}")
        return []


def parse_blogwatcher_output(text_output):
    """Parse text output from blogwatcher articles command."""
    articles = []
    lines = text_output.split('\n')
    
    current_article = {}
    for line in lines:
        line = line.strip()
        
        # Match article ID and title
        # Format: [ID] [new] Title
        match = re.match(r'\[(\d+)\]\s+\[new\]\s+(.+)', line)
        if match:
            if current_article:
                articles.append(current_article)
            current_article = {
                'id': match.group(1),
                'title': match.group(2),
                'blog': '',
                'url': '',
                'published': ''
            }
        
        # Match blog name
        elif line.startswith('Blog:'):
            current_article['blog'] = line.replace('Blog:', '').strip()
        
        # Match URL
        elif line.startswith('URL:'):
            current_article['url'] = line.replace('URL:', '').strip()
        
        # Match published date
        elif line.startswith('Published:'):
            current_article['published'] = line.replace('Published:', '').strip()
    
    if current_article:
        articles.append(current_article)
    
    return articles


def create_aitable_record(article):
    """Create a record in AITable News_Raw."""
    url = f"{AITABLE_BASE}/datasheets/{DATASHEET_ID}/records"
    
    # Map blog names to source types
    source_type = "Local_Media"
    if any(gov in article['blog'].lower() for gov in ['county', 'government', 'city', 'state']):
        source_type = "Gov"
    elif 'weather' in article['blog'].lower():
        source_type = "Gov"
    
    # Auto-categorize
    category = "Community"
    title_lower = article['title'].lower()
    if any(word in title_lower for word in ['school', 'education', 'student']):
        category = "Schools"
    elif any(word in title_lower for word in ['police', 'sheriff', 'fire', 'emergency', 'crash', 'shooting']):
        category = "Public_Safety"
    elif any(word in title_lower for word in ['commissioner', 'council', 'meeting', 'election', 'vote']):
        category = "Civics"
    elif any(word in title_lower for word in ['weather', 'storm', 'rain', 'snow']):
        category = "Community"
    
    # Parse date
    date_published = datetime.now().isoformat()
    if article.get('published'):
        try:
            dt = datetime.strptime(article['published'], '%Y-%m-%d')
            date_published = dt.isoformat()
        except:
            pass
    
    record = {
        "Title_Original": article['title'],
        "Body_Original": f"Source: {article['blog']}\nPublished: {article.get('published', 'Unknown')}",
        "Source_URL": article['url'],
        "Source_Name": article['blog'],
        "Source_Type": source_type,
        "Date_Original": date_published,
        "Category": category,
        "Status": "New",
        "Summary_Short": article['title'][:120] + "..." if len(article['title']) > 120 else article['title'],
        "Notes": f"Auto-imported via blogwatcher on {datetime.now().strftime('%Y-%m-%d %H:%M')}"
    }
    
    payload = {"records": [{"fields": record}]}
    
    try:
        response = requests.post(url, headers=HEADERS, json=payload, timeout=30)
        if response.status_code == 200:
            return True
        else:
            print(f"  ⚠ AITable error: {response.status_code}")
            return False
    except Exception as e:
        print(f"  ⚠ Request failed: {e}")
        return False


def mark_articles_read(article_ids):
    """Mark articles as read in blogwatcher."""
    for article_id in article_ids:
        try:
            subprocess.run(
                ["blogwatcher", "read", article_id],
                capture_output=True,
                timeout=10
            )
        except Exception as e:
            print(f"  ⚠ Could not mark article {article_id} as read: {e}")


def main():
    print("="*60)
    print(" 📰 Blogwatcher → AITable Sync")
    print(f" {datetime.now().strftime('%Y-%m-%d %H:%M')}")
    print("="*60)
    
    # First, scan for new articles
    print("\n🔍 Scanning blogs for new articles...")
    try:
        result = subprocess.run(
            ["blogwatcher", "scan"],
            capture_output=True,
            text=True,
            timeout=120
        )
        print(result.stdout)
        if result.stderr:
            print(result.stderr)
    except Exception as e:
        print(f"⚠ Scan error: {e}")
    
    # Get articles
    print("\n📥 Fetching articles from blogwatcher...")
    result = subprocess.run(
        ["blogwatcher", "articles"],
        capture_output=True,
        text=True,
        timeout=30
    )
    
    articles = parse_blogwatcher_output(result.stdout)
    
    if not articles:
        print("\n✓ No new articles to process")
        return
    
    print(f"\n📊 Found {len(articles)} articles to import")
    
    # Import to AITable
    print(f"\n💾 Importing to AITable...")
    imported = 0
    article_ids = []
    
    for article in articles:
        print(f"  → {article['title'][:60]}...")
        if create_aitable_record(article):
            imported += 1
            article_ids.append(article['id'])
    
    print(f"\n✅ Imported {imported}/{len(articles)} articles")
    
    # Mark as read
    if article_ids:
        print(f"\n📝 Marking {len(article_ids)} articles as read...")
        mark_articles_read(article_ids)
    
    print("\n" + "="*60)


if __name__ == "__main__":
    main()
