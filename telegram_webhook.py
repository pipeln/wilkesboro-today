#!/usr/bin/env python3
"""
Telegram Webhook Handler
Processes approval/rejection callbacks from Telegram
"""

import os
import json
import requests
from http.server import HTTPServer, BaseHTTPRequestHandler
from urllib.parse import parse_qs

SUPABASE_URL = os.environ.get('SUPABASE_URL', 'https://nahldyqwdqnifyljanxt.supabase.co')
SUPABASE_KEY = os.environ.get('SUPABASE_ANON_KEY', '')
TELEGRAM_BOT_TOKEN = os.environ.get('TELEGRAM_BOT_TOKEN', '')

SUPABASE_HEADERS = {
    'apikey': SUPABASE_KEY,
    'Authorization': f'Bearer {SUPABASE_KEY}',
    'Content-Type': 'application/json'
}


def update_article_status(article_id, status, notes=''):
    """Update article approval status in Supabase."""
    url = f"{SUPABASE_URL}/rest/v1/news_raw"
    params = {'id': f'eq.{article_id}'}
    data = {
        'approval_status': status,
        'Status': 'Approved' if status == 'approved' else 'Rejected',
        'reviewer_notes': notes
    }
    
    try:
        response = requests.patch(url, headers=SUPABASE_HEADERS, params=params, json=data)
        return response.status_code == 200
    except Exception as e:
        print(f"Error updating article: {e}")
        return False


def send_telegram_response(chat_id, message_id, text):
    """Send response to Telegram."""
    url = f"https://api.telegram.org/bot{TELEGRAM_BOT_TOKEN}/editMessageText"
    payload = {
        'chat_id': chat_id,
        'message_id': message_id,
        'text': text,
        'parse_mode': 'HTML'
    }
    
    try:
        requests.post(url, json=payload)
    except Exception as e:
        print(f"Error sending Telegram response: {e}")


class WebhookHandler(BaseHTTPRequestHandler):
    def do_POST(self):
        content_length = int(self.headers['Content-Length'])
        post_data = self.rfile.read(content_length)
        
        try:
            data = json.loads(post_data)
            print(f"Received: {json.dumps(data, indent=2)}")
            
            # Handle callback queries (button clicks)
            if 'callback_query' in data:
                callback = data['callback_query']
                callback_data = callback.get('data', '')
                message = callback.get('message', {})
                chat_id = message.get('chat', {}).get('id')
                message_id = message.get('message_id')
                
                # Parse callback data (format: "action:article_id")
                if ':' in callback_data:
                    action, article_id = callback_data.split(':', 1)
                    
                    if action == 'approve':
                        if update_article_status(article_id, 'approved'):
                            send_telegram_response(
                                chat_id, 
                                message_id, 
                                f"✅ <b>APPROVED</b>\n\nArticle ID: {article_id}\nStatus: Published to news_published"
                            )
                            print(f"Approved article {article_id}")
                        else:
                            send_telegram_response(
                                chat_id,
                                message_id,
                                f"❌ Error approving article {article_id}"
                            )
                    
                    elif action == 'reject':
                        if update_article_status(article_id, 'rejected'):
                            send_telegram_response(
                                chat_id,
                                message_id,
                                f"❌ <b>REJECTED</b>\n\nArticle ID: {article_id}\nStatus: Rejected"
                            )
                            print(f"Rejected article {article_id}")
                        else:
                            send_telegram_response(
                                chat_id,
                                message_id,
                                f"❌ Error rejecting article {article_id}"
                            )
            
            # Handle commands (e.g., /approve_123)
            elif 'message' in data:
                message = data['message']
                text = message.get('text', '')
                chat_id = message.get('chat', {}).get('id')
                
                if text.startswith('/approve_'):
                    article_id = text.replace('/approve_', '')
                    if update_article_status(article_id, 'approved'):
                        print(f"Approved article {article_id} via command")
                
                elif text.startswith('/reject_'):
                    article_id = text.replace('/reject_', '')
                    if update_article_status(article_id, 'rejected'):
                        print(f"Rejected article {article_id} via command")
            
            # Send success response
            self.send_response(200)
            self.end_headers()
            self.wfile.write(b'OK')
            
        except Exception as e:
            print(f"Error processing webhook: {e}")
            self.send_response(500)
            self.end_headers()
    
    def log_message(self, format, *args):
        # Suppress default logging
        pass


def main():
    port = int(os.environ.get('PORT', 8080))
    server = HTTPServer(('0.0.0.0', port), WebhookHandler)
    print(f"Webhook server running on port {port}")
    server.serve_forever()


if __name__ == "__main__":
    main()
