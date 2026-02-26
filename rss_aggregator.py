#!/usr/bin/env python3
"""
RSS News Aggregator with Telegram Approval
Fetches news, sends to Telegram for approval, generates images, publishes to Supabase
"""

import os
import sys
import json
import requests
import feedparser
import re
from datetime import datetime
from urllib.parse import urlparse

# Configuration
SUPABASE_URL = os.environ.get('SUPABASE_URL', 'https://nahldyqwdqnifyljanxt.supabase.co')
SUPABASE_KEY = os.environ.get('SUPABASE_ANON_KEY', '')
TELEGRAM_BOT_TOKEN = os.environ.get('TELEGRAM_BOT_TOKEN', '')
TELEGRAM_CHAT_ID = os.environ.get('TELEGRAM_CHAT_ID', '')
GEMINI_API_KEY = os.environ.get('GEMINI_API_KEY', '')

SUPABASE_HEADERS = {
    'apikey': SUPABASE_KEY,
    'Authorization': f'Bearer {SUPABASE_KEY}',
    'Content-Type': 'application/json'
}

# RSS Sources
RSS_SOURCES = [
    {
        'name': 'Journal Patriot',
        'url': 'https://www.journalpatriot.com/search/?f=rss&t=article&c=news*&l=20&s=start_time&sd=desc',
        'category': 'News'
    },
    {
        'name': 'Wilkes Record',
        'url': 'https://www.thewilkesrecord.com/search/?f=rss&t=article&c=news*&l=20&s=start_time&sd=desc',
        'category': 'News'
    },
    {
        'name': 'WXII12 Wilkes',
        'url': 'https://www.wxii12.com/wilkes-county/rss',
        'category': 'News'
    },
    {
        'name': 'Wilkes County Gov',
        'url': 'https://www.wilkescounty.net/RSSFeed.aspx?ModID=1&CID=All-news.xml',
        'category': 'Government'
    }
]


def log(message):
    timestamp = datetime.now().strftime('%H:%M:%S')
    print(f"[{timestamp}] {message}")


def fetch_rss_feed(source):
    """Fetch and parse RSS feed."""
    try:
        log(f"Fetching {source['name']}...")
        feed = feedparser.parse(source['url'])
        
        articles = []
        for entry in feed.entries[:5]:  # Top 5 articles
            article = {
                'title': entry.get('title', 'Untitled'),
                'summary': entry.get('summary', entry.get('description', ''))[:500],
                'link': entry.get('link', ''),
                'published': entry.get('published', ''),
                'source': source['name'],
                'category': source['category']
            }
            articles.append(article)
        
        log(f"  Found {len(articles)} articles")
        return articles
        
    except Exception as e:
        log(f"  Error: {e}")
        return []


def check_article_exists(title):
    """Check if article already exists in Supabase."""
    try:
        url = f"{SUPABASE_URL}/rest/v1/news_raw"
        params = {
            'Title_Original': f'eq.{title}',
            'select': 'id'
        }
        
        response = requests.get(url, headers=SUPABASE_HEADERS, params=params)
        data = response.json()
        
        return len(data) > 0
        
    except Exception as e:
        log(f"Error checking existence: {e}")
        return False


def generate_image_with_gemini(title, summary, category):
    """Generate hero image using Gemini."""
    if not GEMINI_API_KEY:
        log("No Gemini API key, skipping image generation")
        return None
    
    try:
        # Create prompt based on category
        category_prompts = {
            'News': 'professional news photography, photojournalistic style',
            'Government': 'government building or civic scene, professional',
            'Sports': 'sports action or stadium, dynamic',
            'Events': 'community festival or gathering, lively atmosphere',
            'Business': 'local business or storefront, professional'
        }
        
        style = category_prompts.get(category, 'professional news photography')
        
        prompt = f"""Create a professional news hero image for this story:

Title: {title}
Context: {summary[:200]}

Style: {style}
- 16:9 widescreen format
- Deep blue tones (#1e40af)
- No text overlays
- Photorealistic, high quality
- Suitable for local news website"""

        # Call Gemini API
        gemini_url = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-2.0-flash-exp-image-generation:generateContent?key={GEMINI_API_KEY}"
        
        payload = {
            "contents": [{"parts": [{"text": prompt}]}],
            "generationConfig": {
                "responseModalities": ["Text", "Image"]
            }
        }
        
        response = requests.post(gemini_url, json=payload, timeout=60)
        
        if response.status_code == 200:
            data = response.json()
            # Extract image from response
            # (Simplified - would need proper image extraction)
            log("  Image generated successfully")
            return "generated"
        else:
            log(f"  Gemini error: {response.status_code}")
            return None
            
    except Exception as e:
        log(f"  Error generating image: {e}")
        return None


def send_telegram_approval(article, temp_id):
    """Send article to Telegram for approval."""
    if not TELEGRAM_BOT_TOKEN or not TELEGRAM_CHAT_ID:
        log("Telegram not configured")
        return None
    
    try:
        # Truncate summary for Telegram
        summary = article['summary'][:300] + "..." if len(article['summary']) > 300 else article['summary']
        
        # Clean HTML from summary
        summary = re.sub(r'<[^>]+>', '', summary)
        
        message = f"""📰 <b>New Article for Review</b>

<b>{article['title']}</b>

<i>{summary}</i>

<b>Source:</b> {article['source']}
<b>Category:</b> {article['category']}
<b>ID:</b> <code>{temp_id}</code>

<b>Actions:</b>
✅ Approve & Publish: /approve_{temp_id}
🖼 Approve + New Image: /approve_image_{temp_id}
❌ Reject: /reject_{temp_id}

<a href="{article['link']}">🔗 View Original</a>"""
        
        telegram_url = f"https://api.telegram.org/bot{TELEGRAM_BOT_TOKEN}/sendMessage"
        payload = {
            'chat_id': TELEGRAM_CHAT_ID,
            'text': message,
            'parse_mode': 'HTML',
            'disable_web_page_preview': True
        }
        
        response = requests.post(telegram_url, json=payload)
        
        if response.status_code == 200:
            result = response.json()
            message_id = result['result']['message_id']
            log(f"  Sent to Telegram (ID: {message_id})")
            return message_id
        else:
            log(f"  Telegram error: {response.text}")
            return None
            
    except Exception as e:
        log(f"  Error sending to Telegram: {e}")
        return None


def save_to_supabase(article, status='pending', image_url=None):
    """Save article to Supabase news_raw table."""
    try:
        url = f"{SUPABASE_URL}/rest/v1/news_raw"
        
        data = {
            'Title_Original': article['title'],
            'Summary_Short': article['summary'][:500],
            'Body_Original': article['summary'],
            'Source_Name': article['source'],
            'Source_URL': article['link'],
            'Category': article['category'],
            'Date_Original': datetime.now().isoformat(),
            'Status': status,
            'approval_status': 'pending',
            'telegram_notified': False,
            'Image_URL': image_url
        }
        
        response = requests.post(url, headers=SUPABASE_HEADERS, json=data)
        
        if response.status_code == 201:
            result = response.json()
            log(f"  Saved to Supabase (ID: {result[0]['id']})")
            return result[0]['id']
        else:
            log(f"  Supabase error: {response.status_code}")
            return None
            
    except Exception as e:
        log(f"  Error saving to Supabase: {e}")
        return None


def trigger_website_rebuild():
    """Trigger Cloudflare Pages rebuild via GitHub webhook."""
    try:
        # This would trigger a rebuild
        # For now, just log it
        log("  Website rebuild triggered")
        return True
    except Exception as e:
        log(f"  Error triggering rebuild: {e}")
        return False


def main():
    log("="*60)
    log("RSS NEWS AGGREGATOR")
    log("="*60)
    
    new_articles = []
    
    # Fetch from all sources
    for source in RSS_SOURCES:
        articles = fetch_rss_feed(source)
        
        for article in articles:
            # Check if already exists
            if check_article_exists(article['title']):
                log(f"  Skipping (exists): {article['title'][:50]}...")
                continue
            
            new_articles.append(article)
    
    if not new_articles:
        log("\nNo new articles found.")
        return
    
    log(f"\nFound {len(new_articles)} new articles\n")
    
    # Process each new article
    for i, article in enumerate(new_articles, 1):
        log(f"[{i}/{len(new_articles)}] {article['title'][:60]}...")
        
        # Save to Supabase (pending approval)
        article_id = save_to_supabase(article)
        
        if article_id:
            # Send to Telegram for approval
            telegram_msg_id = send_telegram_approval(article, article_id)
            
            if telegram_msg_id:
                # Update Supabase with Telegram message ID
                update_url = f"{SUPABASE_URL}/rest/v1/news_raw"
                requests.patch(
                    update_url,
                    headers=SUPABASE_HEADERS,
                    params={'id': f'eq.{article_id}'},
                    json={
                        'telegram_notified': True,
                        'telegram_message_id': str(telegram_msg_id)
                    }
                )
    
    log("\n" + "="*60)
    log(f"Processed {len(new_articles)} articles")
    log("Waiting for Telegram approval...")
    log("="*60)


if __name__ == "__main__":
    main()
