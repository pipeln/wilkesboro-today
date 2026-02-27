#!/usr/bin/env python3
"""
Telegram Approval Bot for Wilkesboro Today
Sends pending articles to Telegram for manual approval with image handling
"""

import os
import sys
import json
import requests
import re
from datetime import datetime
from urllib.parse import quote

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

DEFAULT_IMAGE_URL = "https://wilkesborotoday.com/wp-content/uploads/2026/02/default-news.jpg"

def log(message):
    timestamp = datetime.now().strftime('%H:%M:%S')
    print(f"[{timestamp}] {message}")


def extract_images_from_url(url):
    """Try to extract images from article URL."""
    images = []
    try:
        response = requests.get(url, timeout=10, headers={'User-Agent': 'Mozilla/5.0'})
        if response.status_code == 200:
            # Look for image URLs in the HTML
            img_pattern = r'https?://[^\s"\'<>]+\.(?:jpg|jpeg|png|gif|webp)'
            found = re.findall(img_pattern, response.text, re.IGNORECASE)
            # Filter for likely article images (not logos/icons)
            for img in found[:5]:  # Limit to first 5
                if any(x in img.lower() for x in ['logo', 'icon', 'avatar', 'button']):
                    continue
                if img not in images:
                    images.append(img)
    except Exception as e:
        log(f"Could not extract images: {e}")
    return images[:3]  # Return max 3 images


def generate_ai_image(prompt, article_id):
    """Generate an AI image using Gemini."""
    if not GEMINI_API_KEY:
        log("No Gemini API key configured")
        return None
    
    try:
        url = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-2.0-flash-exp-image-generation:generateContent?key={GEMINI_API_KEY}"
        
        payload = {
            "contents": [{
                "parts": [{
                    "text": f"Create a professional news illustration for: {prompt}. Style: Clean, professional news photography style."
                }]
            }],
            "generationConfig": {
                "responseModalities": ["Text", "Image"]
            }
        }
        
        response = requests.post(url, json=payload, headers={'Content-Type': 'application/json'})
        if response.status_code == 200:
            data = response.json()
            # Extract image from response
            for part in data.get('candidates', [{}])[0].get('content', {}).get('parts', []):
                if 'inlineData' in part:
                    return part['inlineData']['data']  # Base64 image data
        log(f"Image generation response: {response.text[:200]}")
    except Exception as e:
        log(f"Image generation error: {e}")
    return None


def send_confirmation_message(article, action):
    """Send confirmation message after approval/rejection."""
    if not TELEGRAM_BOT_TOKEN or not TELEGRAM_CHAT_ID:
        return
    
    title = article.get('headline', 'Untitled')[:50]
    article_id = article.get('id', '')[:8]
    
    if action == 'approved':
        message = f"""✅ <b>Article Approved & Published!</b>

<b>{title}...</b>
ID: <code>{article_id}</code>

The article is now live on the website.
Image: {article.get('image_url', 'Default image used')}
"""
    else:
        message = f"""❌ <b>Article Rejected</b>

<b>{title}...</b>
ID: <code>{article_id}</code>

The article has been removed from the queue.
"""
    
    telegram_url = f"https://api.telegram.org/bot{TELEGRAM_BOT_TOKEN}/sendMessage"
    payload = {
        'chat_id': TELEGRAM_CHAT_ID,
        'text': message,
        'parse_mode': 'HTML'
    }
    
    try:
        requests.post(telegram_url, json=payload)
    except Exception as e:
        log(f"Failed to send confirmation: {e}")


def fetch_pending_articles():
    """Fetch articles waiting for approval."""
    url = f"{SUPABASE_URL}/rest/v1/news_items"
    params = {
        'select': '*',
        'order': 'created_at.desc',
        'limit': 5
    }
    
    try:
        response = requests.get(url, headers=SUPABASE_HEADERS, params=params)
        if response.status_code == 200:
            articles = response.json()
            return [a for a in articles if not a.get('sent_to_telegram')]
        else:
            log(f"Error fetching articles: {response.status_code}")
            return []
    except Exception as e:
        log(f"Exception: {e}")
        return []


def send_telegram_notification(article):
    """Send article to Telegram for approval with image options."""
    
    if not TELEGRAM_BOT_TOKEN or not TELEGRAM_CHAT_ID:
        log("Telegram credentials not configured")
        return None
    
    title = article.get('headline', 'Untitled')
    summary = article.get('summary', '')[:300]
    source = article.get('source', 'Unknown')
    article_id = article.get('id')
    source_url = article.get('source_url', '#')
    
    # Extract images from article
    existing_images = extract_images_from_url(source_url) if source_url != '#' else []
    
    # Build message
    message = f"""📰 <b>New Article for Review</b>

<b>{title}</b>

<i>{summary}...</i>

<b>Source:</b> {source}
<b>ID:</b> <code>{article_id}</code>

<b>Image Options:</b>
{"🖼 Found " + str(len(existing_images)) + " images from article" if existing_images else "⚠️ No images found in article"}
"""
    
    # First, send any existing images found
    if existing_images:
        telegram_url = f"https://api.telegram.org/bot{TELEGRAM_BOT_TOKEN}/sendMediaGroup"
        media = []
        for i, img_url in enumerate(existing_images[:3]):
            media.append({
                'type': 'photo',
                'media': img_url,
                'caption': f'Image {i+1} from article' if i == 0 else ''
            })
        
        try:
            requests.post(telegram_url, json={
                'chat_id': TELEGRAM_CHAT_ID,
                'media': media
            })
        except Exception as e:
            log(f"Could not send images: {e}")
    
    # Send approval message with buttons
    telegram_url = f"https://api.telegram.org/bot{TELEGRAM_BOT_TOKEN}/sendMessage"
    
    # Build keyboard with image options
    keyboard = [
        [
            {'text': '✅ Approve', 'callback_data': f'approve:{article_id}'},
            {'text': '❌ Reject', 'callback_data': f'reject:{article_id}'}
        ]
    ]
    
    # Add image option buttons
    if existing_images:
        keyboard.append([
            {'text': '🖼 Use Article Image', 'callback_data': f'img_existing:{article_id}'}
        ])
    
    keyboard.extend([
        [
            {'text': '🎨 Generate AI Image', 'callback_data': f'img_generate:{article_id}'},
            {'text': '📄 Use Default Image', 'callback_data': f'img_default:{article_id}'}
        ],
        [
            {'text': '📝 View Source', 'url': source_url}
        ]
    ])
    
    payload = {
        'chat_id': TELEGRAM_CHAT_ID,
        'text': message,
        'parse_mode': 'HTML',
        'reply_markup': {
            'inline_keyboard': keyboard
        }
    }
    
    try:
        response = requests.post(telegram_url, json=payload)
        if response.status_code == 200:
            result = response.json()
            message_id = result['result']['message_id']
            log(f"✅ Sent to Telegram: {title[:50]}...")
            return message_id
        else:
            log(f"❌ Telegram error: {response.text}")
            return None
    except Exception as e:
        log(f"❌ Exception: {e}")
        return None


def mark_as_notified(article_id, message_id):
    """Mark article as notified in Supabase."""
    url = f"{SUPABASE_URL}/rest/v1/news_items"
    params = {'id': f'eq.{article_id}'}
    data = {'sent_to_telegram': True}
    
    try:
        response = requests.patch(url, headers=SUPABASE_HEADERS, params=params, json=data)
        return response.status_code == 200
    except Exception as e:
        log(f"Error marking as notified: {e}")
        return False


def update_article_image(article_id, image_url, image_source='default'):
    """Update article with selected image."""
    url = f"{SUPABASE_URL}/rest/v1/news_items"
    params = {'id': f'eq.{article_id}'}
    data = {
        'image_url': image_url,
        'image_source': image_source
    }
    
    try:
        response = requests.patch(url, headers=SUPABASE_HEADERS, params=params, json=data)
        return response.status_code == 200
    except Exception as e:
        log(f"Error updating image: {e}")
        return False


def approve_article(article_id, image_choice='default'):
    """Approve an article for publishing."""
    # First get article details
    url = f"{SUPABASE_URL}/rest/v1/news_items"
    params = {'id': f'eq.{article_id}'}
    
    try:
        # Get article
        response = requests.get(url, headers=SUPABASE_HEADERS, params=params)
        article = response.json()[0] if response.status_code == 200 else None
        
        # Handle image based on choice
        if image_choice == 'generate' and article:
            log("Generating AI image...")
            image_data = generate_ai_image(article.get('headline', ''), article_id)
            if image_data:
                # Would need to upload to storage and get URL
                update_article_image(article_id, 'ai_generated', 'ai')
            else:
                update_article_image(article_id, DEFAULT_IMAGE_URL, 'default')
        elif image_choice == 'default':
            update_article_image(article_id, DEFAULT_IMAGE_URL, 'default')
        
        # Update status
        data = {'status': 'Approved', 'approved_at': datetime.now().isoformat()}
        response = requests.patch(url, headers=SUPABASE_HEADERS, params=params, json=data)
        
        if response.status_code == 200:
            log(f"✅ Article {article_id} approved")
            if article:
                send_confirmation_message(article, 'approved')
            return True
        else:
            log(f"❌ Failed to approve: {response.status_code}")
            return False
    except Exception as e:
        log(f"❌ Exception: {e}")
        return False


def reject_article(article_id, reason=''):
    """Reject an article."""
    url = f"{SUPABASE_URL}/rest/v1/news_items"
    params = {'id': f'eq.{article_id}'}
    
    try:
        # Get article for confirmation
        response = requests.get(url, headers=SUPABASE_HEADERS, params=params)
        article = response.json()[0] if response.status_code == 200 else None
        
        data = {'status': 'Rejected', 'rejected_at': datetime.now().isoformat()}
        response = requests.patch(url, headers=SUPABASE_HEADERS, params=params, json=data)
        
        if response.status_code == 200:
            log(f"❌ Article {article_id} rejected")
            if article:
                send_confirmation_message(article, 'rejected')
            return True
        else:
            log(f"❌ Failed to reject: {response.status_code}")
            return False
    except Exception as e:
        log(f"❌ Exception: {e}")
        return False


def main():
    log("="*60)
    log("TELEGRAM APPROVAL BOT")
    log("="*60)
    
    if not all([SUPABASE_KEY, TELEGRAM_BOT_TOKEN, TELEGRAM_CHAT_ID]):
        log("❌ Missing configuration. Check environment variables.")
        return
    
    log("Fetching pending articles...")
    articles = fetch_pending_articles()
    
    if not articles:
        log("No pending articles to notify.")
        return
    
    log(f"Found {len(articles)} pending articles")
    
    for article in articles:
        message_id = send_telegram_notification(article)
        if message_id:
            mark_as_notified(article['id'], message_id)
    
    log("="*60)
    log("Done!")


if __name__ == "__main__":
    if len(sys.argv) > 1:
        action = sys.argv[1]
        article_id = sys.argv[2] if len(sys.argv) > 2 else None
        image_choice = sys.argv[3] if len(sys.argv) > 3 else 'default'
        
        if action == 'approve' and article_id:
            approve_article(article_id, image_choice)
        elif action == 'reject' and article_id:
            reason = sys.argv[3] if len(sys.argv) > 3 else ''
            reject_article(article_id, reason)
        else:
            main()
    else:
        main()
