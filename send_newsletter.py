#!/usr/bin/env python3
"""
Newsletter sender for wilkesbot@wilkesboro.net
Sends daily/weekly digests to subscribers
"""

import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from datetime import datetime
import requests

# Email Configuration
SMTP_SERVER = "mail.wilkesboro.net"
SMTP_PORT = 465
EMAIL = "wilkesbot@wilkesboro.net"
PASSWORD = "squitch-unnerved-paly-stapling"

# AITable Configuration
AITABLE_TOKEN = "uskNPM9fPVHOgAGbDepyKER"
AITABLE_BASE = "https://aitable.ai/api/v1"
HEADERS = {
    "Authorization": f"Bearer {AITABLE_TOKEN}",
    "Content-Type": "application/json"
}


def get_approved_news():
    """Fetch approved news from AITable for newsletter."""
    datasheet_id = "dstjSJ3rvilwBd3Bae"
    
    url = f"{AITABLE_BASE}/datasheets/{datasheet_id}/records"
    
    try:
        response = requests.get(url, headers=HEADERS, params={"pageSize": 20})
        if response.status_code == 200:
            data = response.json()
            records = data.get('records', [])
            
            # Filter for approved/published items
            approved = []
            for r in records:
                fields = r.get('fields', {})
                if fields.get('Status') in ['Approved', 'Published']:
                    approved.append({
                        'title': fields.get('Title_Original', 'Untitled'),
                        'summary': fields.get('Summary_Short', fields.get('Body_Original', '')[:150]),
                        'category': fields.get('Category', 'Community'),
                        'source': fields.get('Source_Name', 'Unknown'),
                        'url': fields.get('Source_URL', '')
                    })
            
            return approved[:10]  # Top 10 items
    except Exception as e:
        print(f"Error fetching news: {e}")
    
    return []


def generate_newsletter_html(news_items):
    """Generate HTML newsletter from news items."""
    
    date_str = datetime.now().strftime("%A, %B %d, %Y")
    
    items_html = ""
    for item in news_items:
        category_color = {
            'Schools': '#3182ce',
            'Public_Safety': '#e53e3e',
            'Civics': '#38a169',
            'Business': '#d69e2e',
            'Community': '#805ad5'
        }.get(item['category'], '#4a5568')
        
        items_html += f"""
        <div style="margin: 20px 0; padding: 15px; background: #f7fafc; border-left: 4px solid {category_color};">
            <div style="font-size: 0.75em; color: #718096; text-transform: uppercase; letter-spacing: 0.5px;">
                {item['category']}
            </div>
            <div style="font-size: 1.15em; font-weight: bold; margin: 5px 0; color: #2d3748;">
                {item['title']}
            </div>
            <div style="font-size: 0.95em; color: #4a5568; line-height: 1.5;">
                {item['summary']}
            </div>
            <div style="font-size: 0.8em; color: #718096; margin-top: 8px;">
                Source: {item['source']}
                {f' | <a href="{item["url"]}" style="color: #3182ce;">Read more →</a>' if item['url'] else ''}
            </div>
        </div>
        """
    
    if not items_html:
        items_html = """
        <div style="padding: 30px; text-align: center; color: #718096;">
            <p>No new updates today. Check back tomorrow!</p>
        </div>
        """
    
    html = f"""<!DOCTYPE html>
<html>
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Wilkes County Daily Digest</title>
</head>
<body style="font-family: Georgia, 'Times New Roman', serif; max-width: 600px; margin: 0 auto; padding: 20px; background: #ffffff; color: #2d3748;">
    
    <div style="text-align: center; padding: 20px 0; border-bottom: 3px solid #2c5282;">
        <h1 style="color: #2c5282; margin: 0; font-size: 1.8em;">📰 Wilkes County Daily Digest</h1>
        <p style="color: #718096; margin: 10px 0 0 0;">{date_str}</p>
    </div>
    
    <div style="padding: 10px 0;">
        {items_html}
    </div>
    
    <div style="margin-top: 30px; padding: 20px; background: #edf2f7; border-radius: 8px; font-size: 0.9em; color: #4a5568;">
        <p style="margin: 0 0 10px 0;"><strong>Have news to share?</strong></p>
        <p style="margin: 0;">
            Email us at <a href="mailto:wilkesbot@wilkesboro.net" style="color: #2c5282;">wilkesbot@wilkesboro.net</a><br>
            Subject line tips: [EVENT], [NEWS], [TIP], [RESOURCE]
        </p>
    </div>
    
    <div style="margin-top: 30px; padding-top: 20px; border-top: 1px solid #e2e8f0; font-size: 0.8em; color: #a0aec0; text-align: center;">
        <p>You're receiving this because you subscribed to Wilkes County updates.</p>
        <p>To unsubscribe, reply with "UNSUBSCRIBE"</p>
    </div>
    
</body>
</html>"""
    
    return html


def send_newsletter(recipients, subject=None):
    """Send newsletter to subscriber list."""
    
    if subject is None:
        subject = f"Wilkes County Daily Digest - {datetime.now().strftime('%b %d')}"
    
    # Get news items
    print("📰 Fetching approved news...")
    news_items = get_approved_news()
    print(f"   Found {len(news_items)} items")
    
    # Generate newsletter
    html_content = generate_newsletter_html(news_items)
    
    # Create plain text version
    text_content = f"Wilkes County Daily Digest - {datetime.now().strftime('%A, %B %d, %Y')}\n\n"
    for item in news_items:
        text_content += f"[{item['category']}] {item['title']}\n"
        text_content += f"{item['summary']}\n"
        text_content += f"Source: {item['source']}\n\n"
    
    # Send emails
    print(f"📧 Connecting to {SMTP_SERVER}...")
    
    try:
        with smtplib.SMTP_SSL(SMTP_SERVER, SMTP_PORT) as server:
            server.login(EMAIL, PASSWORD)
            
            sent_count = 0
            for recipient in recipients:
                msg = MIMEMultipart("alternative")
                msg["From"] = f"Wilkes County Bot <wilkesbot@wilkesboro.net>"
                msg["To"] = recipient
                msg["Subject"] = subject
                
                msg.attach(MIMEText(text_content, "plain"))
                msg.attach(MIMEText(html_content, "html"))
                
                server.sendmail(EMAIL, recipient, msg.as_string())
                sent_count += 1
                print(f"   ✅ Sent to {recipient}")
        
        print(f"\n🎉 Newsletter sent to {sent_count} subscriber(s)")
        return True
        
    except Exception as e:
        print(f"❌ Failed to send: {e}")
        return False


def main():
    print("="*60)
    print(" 📧 WilkesBot Newsletter Sender")
    print(f" {datetime.now().strftime('%Y-%m-%d %H:%M')}")
    print("="*60)
    
    # TODO: Load subscriber list from file or AITable
    # For testing, use a single recipient
    subscribers = [
        # Add subscriber emails here
        # "subscriber@example.com",
    ]
    
    if not subscribers:
        print("\n⚠ No subscribers configured")
        print("   Add emails to the subscribers list in this script")
        return
    
    send_newsletter(subscribers)
    
    print("="*60)


if __name__ == "__main__":
    main()
