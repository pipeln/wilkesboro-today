#!/usr/bin/env python3
"""
Telegram Approval Bot for Wilkesboro Today
Sends pending articles to Telegram for manual approval
"""

import os
import sys
import json
import requests
from datetime import datetime
from urllib.parse import quote

# Configuration
SUPABASE_URL = os.environ.get('SUPABASE_URL', 'https://nahldyqwdqnifyljanxt.supabase.co')
SUPABASE_KEY = os.environ.get('SUPABASE_ANON_KEY', '')
TELEGRAM_BOT_TOKEN = os.environ.get('TELEGRAM_BOT_TOKEN', '')
TELEGRAM_CHAT_ID = os.environ.get('TELEGRAM_CHAT_ID', '')  # Your personal chat ID

SUPABASE_HEADERS = {
    'apikey': SUPABASE_KEY,
    'Authorization': f'Bearer {SUPABASE_KEY}',
    'Content-Type': 'application/json'
}


def log(message):
    timestamp = datetime.now().strftime('%H:%M:%S')
    print(f"[{timestamp}] {message}")


def fetch_pending_articles():
    """Fetch articles waiting for approval."""
    url = f"{SUPABASE_URL}/rest/v1/news_raw"
    params = {
        'approval_status': 'eq.pending',
        'telegram_notified': 'eq.false',
        'select': '*',
        'order': 'created_at.desc',
        'limit': 5
    }
    
    try:
        response = requests.get(url, headers=SUPABASE_HEADERS, params=params)
        if response.status_code == 200:
            return response.json()
        else:
            log(f"Error fetching articles: {response.status_code}")
            return []
    except Exception as e:
        log(f"Exception: {e}")
        return []


def send_telegram_notification(article):
    """Send article to Telegram for approval."""
    
    if not TELEGRAM_BOT_TOKEN or not TELEGRAM_CHAT_ID:
        log("Telegram credentials not configured")
        return None
    
    # Build message
    title = article.get('Title_Original', 'Untitled')
    summary = article.get('Summary_Short', article.get('Body_Original', '')[:200])
    category = article.get('Category', 'News')
    source = article.get('Source_Name', 'Unknown')
    article_id = article.get('id')
    
    message = f"""📰 <b>New Article for Review</b>

<b>{title}</b>

<i>{summary[:300]}...</i>

<b>Category:</b> {category}
<b>Source:</b> {source}
<b>ID:</b> <code>{article_id}</code>

<b>Actions:</b>
✅ Approve: /approve_{article_id}
❌ Reject: /reject_{article_id}
📝 Edit: /edit_{article_id}
    """
    
    # Send to Telegram
    telegram_url = f"https://api.telegram.org/bot{TELEGRAM_BOT_TOKEN}/sendMessage"
    payload = {
        'chat_id': TELEGRAM_CHAT_ID,
        'text': message,
        'parse_mode': 'HTML',
        'reply_markup': {
            'inline_keyboard': [
                [
                    {'text': '✅ Approve', 'callback_data': f'approve:{article_id}'},
                    {'text': '❌ Reject', 'callback_data': f'reject:{article_id}'}
                ],
                [
                    {'text': '📝 View Source', 'url': article.get('Source_URL', '#')}
                ]
            ]
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
    url = f"{SUPABASE_URL}/rest/v1/news_raw"
    params = {'id': f'eq.{article_id}'}
    data = {
        'telegram_notified': True,
        'telegram_message_id': str(message_id)
    }
    
    try:
        response = requests.patch(url, headers=SUPABASE_HEADERS, params=params, json=data)
        return response.status_code == 200
    except Exception as e:
        log(f"Error marking as notified: {e}")
        return False


def approve_article(article_id):
    """Approve an article for publishing."""
    url = f"{SUPABASE_URL}/rest/v1/news_raw"
    params = {'id': f'eq.{article_id}'}
    data = {
        'approval_status': 'approved',
        'reviewed_at': datetime.now().isoformat(),
        'Status': 'Approved'
    }
    
    try:
        response = requests.patch(url, headers=SUPABASE_HEADERS, params=params, json=data)
        if response.status_code == 200:
            log(f"✅ Article {article_id} approved")
            return True
        else:
            log(f"❌ Failed to approve: {response.status_code}")
            return False
    except Exception as e:
        log(f"❌ Exception: {e}")
        return False


def reject_article(article_id, reason=''):
    """Reject an article."""
    url = f"{SUPABASE_URL}/rest/v1/news_raw"
    params = {'id': f'eq.{article_id}'}
    data = {
        'approval_status': 'rejected',
        'reviewed_at': datetime.now().isoformat(),
        'reviewer_notes': reason,
        'Status': 'Rejected'
    }
    
    try:
        response = requests.patch(url, headers=SUPABASE_HEADERS, params=params, json=data)
        if response.status_code == 200:
            log(f"❌ Article {article_id} rejected")
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
    
    # Check configuration
    if not all([SUPABASE_KEY, TELEGRAM_BOT_TOKEN, TELEGRAM_CHAT_ID]):
        log("❌ Missing configuration. Check environment variables.")
        log("Required: SUPABASE_ANON_KEY, TELEGRAM_BOT_TOKEN, TELEGRAM_CHAT_ID")
        return
    
    # Fetch pending articles
    log("Fetching pending articles...")
    articles = fetch_pending_articles()
    
    if not articles:
        log("No pending articles to notify.")
        return
    
    log(f"Found {len(articles)} pending articles")
    
    # Send notifications
    for article in articles:
        message_id = send_telegram_notification(article)
        if message_id:
            mark_as_notified(article['id'], message_id)
    
    log("="*60)
    log("Done!")


if __name__ == "__main__":
    # Check for command line arguments (for manual approve/reject)
    if len(sys.argv) > 1:
        action = sys.argv[1]
        article_id = sys.argv[2] if len(sys.argv) > 2 else None
        
        if action == 'approve' and article_id:
            approve_article(article_id)
        elif action == 'reject' and article_id:
            reason = sys.argv[3] if len(sys.argv) > 3 else ''
            reject_article(article_id, reason)
        else:
            main()
    else:
        main()
