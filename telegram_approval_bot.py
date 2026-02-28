#!/usr/bin/env python3
"""
Simplified Telegram Approval Bot for Wilkesboro Today
Approve/Reject only → Auto-publishes to website
"""

import os
import sys
import json
import requests
import re
import base64
from datetime import datetime
from urllib.parse import quote

# Configuration
SUPABASE_URL = os.environ.get('SUPABASE_URL', 'https://nahldyqwdqnifyljanxt.supabase.co')
SUPABASE_KEY = os.environ.get('SUPABASE_ANON_KEY', '')
TELEGRAM_BOT_TOKEN = os.environ.get('TELEGRAM_BOT_TOKEN', '')
TELEGRAM_CHAT_ID = os.environ.get('TELEGRAM_CHAT_ID', '')
GEMINI_API_KEY = os.environ.get('GEMINI_API_KEY', '')

# WordPress/Wilkesboro Today API
WP_API_URL = os.environ.get('WP_API_URL', 'https://wilkesborotoday.com/wp-json/wp/v2')
WP_USERNAME = os.environ.get('WP_USERNAME', '')
WP_APP_PASSWORD = os.environ.get('WP_APP_PASSWORD', '')

SUPABASE_HEADERS = {
    'apikey': SUPABASE_KEY,
    'Authorization': f'Bearer {SUPABASE_KEY}',
    'Content-Type': 'application/json'
}

DEFAULT_IMAGE_ID = 0  # WordPress media ID for default image

def log(message):
    timestamp = datetime.now().strftime('%H:%M:%S')
    print(f"[{timestamp}] {message}")


def extract_first_image(url):
    """Extract first good image from article URL."""
    try:
        response = requests.get(url, timeout=10, headers={'User-Agent': 'Mozilla/5.0'})
        if response.status_code == 200:
            # Look for image URLs
            img_pattern = r'https?://[^\s"\'<>]+\.(?:jpg|jpeg|png)'
            found = re.findall(img_pattern, response.text, re.IGNORECASE)
            for img in found:
                # Skip logos, icons, small images
                if any(x in img.lower() for x in ['logo', 'icon', 'avatar', 'button', 'thumb']):
                    continue
                return img
    except Exception as e:
        log(f"Could not extract image: {e}")
    return None


def generate_ai_image(prompt):
    """Generate an AI image using Gemini."""
    if not GEMINI_API_KEY:
        return None
    
    try:
        url = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-2.0-flash-exp-image-generation:generateContent?key={GEMINI_API_KEY}"
        
        payload = {
            "contents": [{
                "parts": [{
                    "text": f"Professional news photo for: {prompt}. Clean, journalistic style."
                }]
            }],
            "generationConfig": {
                "responseModalities": ["Text", "Image"]
            }
        }
        
        response = requests.post(url, json=payload, headers={'Content-Type': 'application/json'})
        if response.status_code == 200:
            data = response.json()
            for part in data.get('candidates', [{}])[0].get('content', {}).get('parts', []):
                if 'inlineData' in part:
                    return part['inlineData']['data']  # Base64
    except Exception as e:
        log(f"Image generation failed: {e}")
    return None


def upload_image_to_wordpress(image_url_or_data, title):
    """Upload image to WordPress and return media ID."""
    if not WP_USERNAME or not WP_APP_PASSWORD:
        log("WordPress credentials not configured")
        return DEFAULT_IMAGE_ID
    
    try:
        auth = base64.b64encode(f"{WP_USERNAME}:{WP_APP_PASSWORD}".encode()).decode()
        headers = {'Authorization': f'Basic {auth}'}
        
        # If it's a URL, download it
        if image_url_or_data.startswith('http'):
            img_response = requests.get(image_url_or_data, timeout=30)
            if img_response.status_code != 200:
                return DEFAULT_IMAGE_ID
            image_data = img_response.content
            filename = f"news-{datetime.now().strftime('%Y%m%d')}.jpg"
        else:
            # Base64 data from AI generation
            image_data = base64.b64decode(image_url_or_data)
            filename = f"ai-generated-{datetime.now().strftime('%Y%m%d')}.jpg"
        
        # Upload to WordPress
        files = {'file': (filename, image_data, 'image/jpeg')}
        response = requests.post(f"{WP_API_URL}/media", headers=headers, files=files)
        
        if response.status_code == 201:
            return response.json().get('id', DEFAULT_IMAGE_ID)
    except Exception as e:
        log(f"Image upload failed: {e}")
    
    return DEFAULT_IMAGE_ID


def publish_to_wordpress(article, image_id=None):
    """Publish article to WordPress site."""
    if not WP_USERNAME or not WP_APP_PASSWORD:
        log("WordPress credentials not configured - article not published")
        return False
    
    try:
        auth = base64.b64encode(f"{WP_USERNAME}:{WP_APP_PASSWORD}".encode()).decode()
        headers = {
            'Authorization': f'Basic {auth}',
            'Content-Type': 'application/json'
        }
        
        # Prepare post content
        post_data = {
            'title': article.get('headline', 'Untitled'),
            'content': f"<p>{article.get('summary', '')}</p><p>Source: <a href='{article.get('source_url', '#')}'>{article.get('source', 'Unknown')}</a></p>",
            'status': 'publish',  # Publish immediately
            'categories': [1],  # Default category ID
            'tags': article.get('tags', []),
            'featured_media': image_id if image_id else DEFAULT_IMAGE_ID
        }
        
        response = requests.post(f"{WP_API_URL}/posts", headers=headers, json=post_data)
        
        if response.status_code == 201:
            post = response.json()
            log(f"✅ Published to website: {post.get('link', '')}")
            return post.get('link', '')
        else:
            log(f"❌ WordPress publish failed: {response.status_code}")
            return False
    except Exception as e:
        log(f"❌ Publish error: {e}")
        return False


def send_telegram_message(text, parse_mode='HTML'):
    """Send message to Telegram."""
    if not TELEGRAM_BOT_TOKEN or not TELEGRAM_CHAT_ID:
        return None
    
    url = f"https://api.telegram.org/bot{TELEGRAM_BOT_TOKEN}/sendMessage"
    payload = {
        'chat_id': TELEGRAM_CHAT_ID,
        'text': text,
        'parse_mode': parse_mode
    }
    
    try:
        response = requests.post(url, json=payload)
        return response.status_code == 200
    except Exception as e:
        log(f"Telegram send failed: {e}")
        return False


def fetch_pending_articles():
    """Fetch articles waiting for approval."""
    url = f"{SUPABASE_URL}/rest/v1/news_items"
    params = {
        'select': '*',
        'order': 'created_at.desc',
        'limit': 10
    }
    
    try:
        response = requests.get(url, headers=SUPABASE_HEADERS, params=params)
        if response.status_code == 200:
            articles = response.json()
            # Filter to only those not yet processed
            return [a for a in articles if a.get('status') not in ['Approved', 'Rejected', 'Published']]
        return []
    except Exception as e:
        log(f"Fetch error: {e}")
        return []


def send_article_for_approval(article):
    """Send article to Telegram with simple approve/reject buttons."""
    if not TELEGRAM_BOT_TOKEN or not TELEGRAM_CHAT_ID:
        log("Telegram not configured")
        return None
    
    title = article.get('headline', 'Untitled')
    summary = article.get('summary', '')[:250]
    source = article.get('source', 'Unknown')
    article_id = article.get('id')
    source_url = article.get('source_url') or 'https://wilkesboro.net'
    
    # Ensure source_url is a valid string
    if not isinstance(source_url, str) or not source_url.startswith('http'):
        source_url = 'https://wilkesboro.net'
    
    message = f"""📰 <b>ARTICLE FOR APPROVAL</b>

<b>{title}</b>

{summary}...

<b>Source:</b> {source}
<b>ID:</b> <code>{article_id}</code>

Reply with:
✅ <b>approve</b> - Publish to website
❌ <b>reject</b> - Discard"""
    
    url = f"https://api.telegram.org/bot{TELEGRAM_BOT_TOKEN}/sendMessage"
    payload = {
        'chat_id': TELEGRAM_CHAT_ID,
        'text': message,
        'parse_mode': 'HTML',
        'reply_markup': {
            'inline_keyboard': [[
                {'text': '✅ APPROVE', 'callback_data': f'approve:{article_id}'},
                {'text': '❌ REJECT', 'callback_data': f'reject:{article_id}'}
            ], [
                {'text': '📖 Read Full Article', 'url': source_url}
            ]]
        }
    }
    
    try:
        response = requests.post(url, json=payload)
        if response.status_code == 200:
            log(f"✅ Sent: {title[:40]}...")
            return response.json()['result']['message_id']
        else:
            log(f"❌ Telegram error: {response.text}")
    except Exception as e:
        log(f"❌ Send error: {e}")
    return None


def update_article_status(article_id, status, extra_data=None):
    """Update article status in Supabase."""
    url = f"{SUPABASE_URL}/rest/v1/news_items"
    params = {'id': f'eq.{article_id}'}
    data = {'status': status}
    if extra_data:
        data.update(extra_data)
    
    try:
        response = requests.patch(url, headers=SUPABASE_HEADERS, params=params, json=data)
        return response.status_code == 200
    except Exception as e:
        log(f"Update error: {e}")
        return False


def approve_and_publish(article_id):
    """Approve article and publish to website."""
    log(f"Approving article {article_id}...")
    
    # Get article details
    url = f"{SUPABASE_URL}/rest/v1/news_items"
    params = {'id': f'eq.{article_id}'}
    
    try:
        response = requests.get(url, headers=SUPABASE_HEADERS, params=params)
        if response.status_code != 200 or not response.json():
            log("❌ Article not found")
            return False
        
        article = response.json()[0]
        title = article.get('headline', 'Untitled')
        
        # Step 1: Get image
        log("Getting image...")
        image_url = extract_first_image(article.get('source_url', ''))
        
        if image_url:
            log(f"Found article image: {image_url[:50]}...")
            image_id = upload_image_to_wordpress(image_url, title)
        else:
            log("No article image found, generating AI image...")
            ai_image = generate_ai_image(title)
            if ai_image:
                image_id = upload_image_to_wordpress(ai_image, title)
            else:
                log("Using default image")
                image_id = DEFAULT_IMAGE_ID
        
        # Step 2: Publish to WordPress
        log("Publishing to website...")
        post_url = publish_to_wordpress(article, image_id)
        
        # Step 3: Update status
        update_data = {
            'status': 'Published',
            'published_at': datetime.now().isoformat(),
            'published_url': post_url if post_url else '',
            'wordpress_post_id': post_url.split('/')[-2] if post_url and '/' in post_url else None
        }
        update_article_status(article_id, 'Published', update_data)
        
        # Step 4: Send confirmation
        if post_url:
            send_telegram_message(
                f"✅ <b>Article Published!</b>\n\n"
                f"<b>{title[:60]}...</b>\n"
                f"🔗 <a href='{post_url}'>View on Website</a>\n\n"
                f"Live in ~2 minutes"
            )
        else:
            send_telegram_message(
                f"✅ <b>Article Approved</b>\n\n"
                f"<b>{title[:60]}...</b>\n\n"
                f"⚠️ Could not auto-publish. Manual publish needed."
            )
        
        return True
        
    except Exception as e:
        log(f"❌ Approval failed: {e}")
        send_telegram_message(f"❌ <b>Failed to publish article {article_id}</b>\nError: {str(e)[:100]}")
        return False


def reject_article(article_id):
    """Reject article."""
    log(f"Rejecting article {article_id}...")
    
    # Get article for confirmation
    url = f"{SUPABASE_URL}/rest/v1/news_items"
    params = {'id': f'eq.{article_id}'}
    
    try:
        response = requests.get(url, headers=SUPABASE_HEADERS, params=params)
        article = response.json()[0] if response.json() else None
        
        update_article_status(article_id, 'Rejected', {'rejected_at': datetime.now().isoformat()})
        
        if article:
            send_telegram_message(
                f"❌ <b>Article Rejected</b>\n\n"
                f"<b>{article.get('headline', 'Untitled')[:60]}...</b>\n"
                f"ID: <code>{article_id}</code>"
            )
        return True
    except Exception as e:
        log(f"❌ Reject error: {e}")
        return False


def main():
    log("="*60)
    log("TELEGRAM APPROVAL BOT")
    log("="*60)
    
    # Check config
    if not all([SUPABASE_KEY, TELEGRAM_BOT_TOKEN, TELEGRAM_CHAT_ID]):
        log("❌ Missing config: SUPABASE_ANON_KEY, TELEGRAM_BOT_TOKEN, TELEGRAM_CHAT_ID")
        return
    
    # Fetch and send pending articles
    articles = fetch_pending_articles()
    
    if not articles:
        log("No pending articles")
        return
    
    log(f"Found {len(articles)} articles to approve")
    
    for article in articles:
        send_article_for_approval(article)
    
    log("="*60)
    log("Done! Check Telegram to approve/reject")


if __name__ == "__main__":
    if len(sys.argv) > 2:
        action = sys.argv[1]
        article_id = sys.argv[2]
        
        if action == 'approve':
            approve_and_publish(article_id)
        elif action == 'reject':
            reject_article(article_id)
        else:
            main()
    else:
        main()
