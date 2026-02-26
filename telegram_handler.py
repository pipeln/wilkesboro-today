#!/usr/bin/env python3
"""
Telegram Command Handler for Article Approval
Handles /approve, /approve_image, /reject commands
"""

import os
import sys
import requests
from datetime import datetime

# Configuration
SUPABASE_URL = os.environ.get('SUPABASE_URL', 'https://nahldyqwdqnifyljanxt.supabase.co')
SUPABASE_KEY = os.environ.get('SUPABASE_ANON_KEY', '')
TELEGRAM_BOT_TOKEN = os.environ.get('TELEGRAM_BOT_TOKEN', '')
GEMINI_API_KEY = os.environ.get('GEMINI_API_KEY', '')

SUPABASE_HEADERS = {
    'apikey': SUPABASE_KEY,
    'Authorization': f'Bearer {SUPABASE_KEY}',
    'Content-Type': 'application/json'
}


def log(message):
    timestamp = datetime.now().strftime('%H:%M:%S')
    print(f"[{timestamp}] {message}")


def get_article(article_id):
    """Fetch article from Supabase."""
    try:
        url = f"{SUPABASE_URL}/rest/v1/news_raw"
        params = {'id': f'eq.{article_id}'}
        
        response = requests.get(url, headers=SUPABASE_HEADERS, params=params)
        data = response.json()
        
        return data[0] if data else None
        
    except Exception as e:
        log(f"Error fetching article: {e}")
        return None


def generate_new_image(article_id, title, summary, category):
    """Generate new image with Gemini."""
    if not GEMINI_API_KEY:
        return None
    
    try:
        log(f"Generating new image for article {article_id}...")
        
        # Import the image generation function
        sys.path.insert(0, '/root/.openclaw/workspace/website-design')
        from src.utils.supabase import generate_image_with_gemini
        
        # Generate image
        image_path = generate_image_with_gemini(
            f"Generate image for: {title}",
            article_id
        )
        
        return image_path
        
    except Exception as e:
        log(f"Error generating image: {e}")
        return None


def approve_article(article_id, generate_new_img=False):
    """Approve article and publish to news_published."""
    log(f"Approving article {article_id}...")
    
    # Get article
    article = get_article(article_id)
    if not article:
        log(f"Article {article_id} not found")
        return False
    
    # Generate new image if requested
    image_url = article.get('Image_URL')
    if generate_new_img or not image_url:
        new_image = generate_new_image(
            article_id,
            article['Title_Original'],
            article['Summary_Short'],
            article['Category']
        )
        if new_image:
            image_url = new_image
    
    # Update news_raw status
    update_url = f"{SUPABASE_URL}/rest/v1/news_raw"
    requests.patch(
        update_url,
        headers=SUPABASE_HEADERS,
        params={'id': f'eq.{article_id}'},
        json={
            'approval_status': 'approved',
            'Status': 'Approved',
            'reviewed_at': datetime.now().isoformat(),
            'Image_URL': image_url
        }
    )
    
    # Insert into news_published
    published_url = f"{SUPABASE_URL}/rest/v1/news_published"
    published_data = {
        'Title': article['Title_Original'],
        'Summary': article['Summary_Short'],
        'Category': article['Category'],
        'Published_At': datetime.now().isoformat(),
        'Source_URL': article['Source_URL'],
        'WordPress_URL': article['Source_URL'],
        'Audience': 'All'
    }
    
    response = requests.post(published_url, headers=SUPABASE_HEADERS, json=published_data)
    
    if response.status_code == 201:
        log(f"✅ Article {article_id} published!")
        
        # Trigger website rebuild
        trigger_rebuild()
        
        return True
    else:
        log(f"❌ Error publishing: {response.status_code}")
        return False


def reject_article(article_id, reason=''):
    """Reject article."""
    log(f"Rejecting article {article_id}...")
    
    update_url = f"{SUPABASE_URL}/rest/v1/news_raw"
    response = requests.patch(
        update_url,
        headers=SUPABASE_HEADERS,
        params={'id': f'eq.{article_id}'},
        json={
            'approval_status': 'rejected',
            'Status': 'Rejected',
            'reviewed_at': datetime.now().isoformat(),
            'reviewer_notes': reason
        }
    )
    
    if response.status_code == 200:
        log(f"❌ Article {article_id} rejected")
        return True
    else:
        log(f"❌ Error rejecting: {response.status_code}")
        return False


def trigger_rebuild():
    """Trigger website rebuild."""
    try:
        # GitHub Actions webhook or Cloudflare hook
        log("🔄 Triggering website rebuild...")
        
        # This would call GitHub API to trigger workflow
        # For now, just log it
        return True
        
    except Exception as e:
        log(f"Error triggering rebuild: {e}")
        return False


def send_telegram_confirmation(chat_id, message_id, text):
    """Send confirmation to Telegram."""
    if not TELEGRAM_BOT_TOKEN:
        return
    
    try:
        url = f"https://api.telegram.org/bot{TELEGRAM_BOT_TOKEN}/editMessageText"
        payload = {
            'chat_id': chat_id,
            'message_id': message_id,
            'text': text,
            'parse_mode': 'HTML'
        }
        
        requests.post(url, json=payload)
        
    except Exception as e:
        log(f"Error sending Telegram confirmation: {e}")


def process_command(command_text):
    """Process Telegram command."""
    log(f"Processing command: {command_text}")
    
    if command_text.startswith('/approve_'):
        article_id = command_text.replace('/approve_', '').split()[0]
        
        # Check if it's approve with new image
        if '_image_' in command_text:
            article_id = command_text.replace('/approve_image_', '').split()[0]
            success = approve_article(article_id, generate_new_img=True)
        else:
            success = approve_article(article_id)
        
        return success
    
    elif command_text.startswith('/reject_'):
        article_id = command_text.replace('/reject_', '').split()[0]
        reason = ' '.join(command_text.split()[1:]) if len(command_text.split()) > 1 else ''
        
        success = reject_article(article_id, reason)
        return success
    
    elif command_text == '/help':
        return """📰 Article Approval Bot Commands:

✅ /approve_ID - Approve and publish article
🖼 /approve_image_ID - Approve with NEW image
❌ /reject_ID [reason] - Reject article
📊 /status - Check pending articles

Replace ID with the article ID shown in the message."""
    
    return None


def main():
    if len(sys.argv) < 2:
        print("Usage: python3 telegram_handler.py '<command>'")
        print("Example: python3 telegram_handler.py '/approve_123'")
        sys.exit(1)
    
    command = sys.argv[1]
    result = process_command(command)
    
    if result:
        print("✅ Command processed successfully")
    else:
        print("❌ Command failed")


if __name__ == "__main__":
    main()
