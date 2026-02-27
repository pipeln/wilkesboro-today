#!/usr/bin/env python3
"""
Telegram Webhook Handler for Approval Bot
Processes approve/reject button clicks from Telegram
"""

import os
import json
import requests
from http.server import HTTPServer, BaseHTTPRequestHandler
from urllib.parse import parse_qs

# Import functions from main bot
from telegram_approval_bot import approve_and_publish, reject_article, log

TELEGRAM_BOT_TOKEN = os.environ.get('TELEGRAM_BOT_TOKEN', '')

def send_telegram_response(chat_id, text):
    """Send response to Telegram chat."""
    url = f"https://api.telegram.org/bot{TELEGRAM_BOT_TOKEN}/sendMessage"
    payload = {
        'chat_id': chat_id,
        'text': text,
        'parse_mode': 'HTML'
    }
    try:
        requests.post(url, json=payload)
    except Exception as e:
        log(f"Response error: {e}")


class WebhookHandler(BaseHTTPRequestHandler):
    def do_POST(self):
        content_length = int(self.headers['Content-Length'])
        post_data = self.rfile.read(content_length)
        
        try:
            data = json.loads(post_data)
            
            # Handle callback queries (button clicks)
            if 'callback_query' in data:
                callback = data['callback_query']
                chat_id = callback['message']['chat']['id']
                callback_data = callback['data']
                
                # Parse action and article ID
                if ':' in callback_data:
                    action, article_id = callback_data.split(':', 1)
                    
                    if action == 'approve':
                        send_telegram_response(chat_id, "⏳ Publishing article...")
                        success = approve_and_publish(article_id)
                        # Answer callback to remove loading state
                        requests.post(f"https://api.telegram.org/bot{TELEGRAM_BOT_TOKEN}/answerCallbackQuery",
                                    json={'callback_query_id': callback['id']})
                    
                    elif action == 'reject':
                        success = reject_article(article_id)
                        requests.post(f"https://api.telegram.org/bot{TELEGRAM_BOT_TOKEN}/answerCallbackQuery",
                                    json={'callback_query_id': callback['id']})
            
            # Handle text commands
            elif 'message' in data and 'text' in data['message']:
                text = data['message']['text'].lower().strip()
                chat_id = data['message']['chat']['id']
                
                if text.startswith('approve '):
                    article_id = text.split(' ')[1]
                    approve_and_publish(article_id)
                elif text.startswith('reject '):
                    article_id = text.split(' ')[1]
                    reject_article(article_id)
            
            self.send_response(200)
            self.end_headers()
            
        except Exception as e:
            log(f"Webhook error: {e}")
            self.send_response(500)
            self.end_headers()
    
    def log_message(self, format, *args):
        pass  # Suppress default logging


def main():
    port = int(os.environ.get('PORT', 8080))
    server = HTTPServer(('0.0.0.0', port), WebhookHandler)
    log(f"Webhook server running on port {port}")
    server.serve_forever()


if __name__ == "__main__":
    main()
