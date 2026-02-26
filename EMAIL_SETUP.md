# Email Configuration for wilkesbot@wilkesboro.net

## Account Details
- **Email:** wilkesbot@wilkesboro.net
- **Password:** squitch-unnerved-paly-stapling
- **Incoming:** mail.wilkesboro.net:993 (IMAP/SSL)
- **Outgoing:** mail.wilkesboro.net:465 (SMTP/SSL)

## Python Email Scripts

### 1. Check Submissions (IMAP)

```python
import imaplib
import email
from email.header import decode_header
import re
from datetime import datetime

def check_submission_emails():
    """Check wilkesbot@wilkesboro.net for community submissions."""
    
    IMAP_SERVER = "mail.wilkesboro.net"
    IMAP_PORT = 993
    EMAIL = "wilkesbot@wilkesboro.net"
    PASSWORD = "squitch-unnerved-paly-stapling"
    
    try:
        # Connect to IMAP
        mail = imaplib.IMAP4_SSL(IMAP_SERVER, IMAP_PORT)
        mail.login(EMAIL, PASSWORD)
        mail.select("inbox")
        
        # Search for unread emails
        status, messages = mail.search(None, "UNSEEN")
        
        submissions = []
        
        for msg_num in messages[0].split():
            status, msg_data = mail.fetch(msg_num, "(RFC822)")
            
            for response_part in msg_data:
                if isinstance(response_part, tuple):
                    msg = email.message_from_bytes(response_part[1])
                    
                    # Decode subject
                    subject, encoding = decode_header(msg["Subject"])[0]
                    if isinstance(subject, bytes):
                        subject = subject.decode(encoding or "utf-8")
                    
                    # Get sender
                    from_addr = msg.get("From", "")
                    
                    # Get body
                    body = ""
                    if msg.is_multipart():
                        for part in msg.walk():
                            content_type = part.get_content_type()
                            if content_type == "text/plain":
                                body = part.get_payload(decode=True).decode("utf-8", errors="ignore")
                                break
                    else:
                        body = msg.get_payload(decode=True).decode("utf-8", errors="ignore")
                    
                    submissions.append({
                        "subject": subject,
                        "from": from_addr,
                        "body": body,
                        "date": msg.get("Date"),
                        "raw": msg
                    })
                    
                    # Mark as seen
                    mail.store(msg_num, "+FLAGS", "\\Seen")
        
        mail.logout()
        return submissions
        
    except Exception as e:
        print(f"Email check failed: {e}")
        return []
```

### 2. Send Newsletters (SMTP)

```python
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

def send_newsletter(recipients, subject, html_content, text_content=None):
    """Send newsletter via wilkesbot@wilkesboro.net."""
    
    SMTP_SERVER = "mail.wilkesboro.net"
    SMTP_PORT = 465
    EMAIL = "wilkesbot@wilkesboro.net"
    PASSWORD = "squitch-unnerved-paly-stapling"
    
    try:
        # Create message
        msg = MIMEMultipart("alternative")
        msg["From"] = f"Wilkes County Bot <{EMAIL}>"
        msg["To"] = ", ".join(recipients) if isinstance(recipients, list) else recipients
        msg["Subject"] = subject
        
        # Add plain text version
        if text_content:
            msg.attach(MIMEText(text_content, "plain"))
        
        # Add HTML version
        msg.attach(MIMEText(html_content, "html"))
        
        # Send via SMTP/SSL
        with smtplib.SMTP_SSL(SMTP_SERVER, SMTP_PORT) as server:
            server.login(EMAIL, PASSWORD)
            server.sendmail(EMAIL, recipients, msg.as_string())
        
        print(f"✅ Newsletter sent to {len(recipients) if isinstance(recipients, list) else 1} recipient(s)")
        return True
        
    except Exception as e:
        print(f"❌ Failed to send newsletter: {e}")
        return False
```

### 3. Parse Submission Emails

```python
def parse_submission_email(subject, body, from_addr):
    """Parse incoming email into structured submission."""
    
    # Detect submission type from subject
    subject_lower = subject.lower()
    
    if any(word in subject_lower for word in ["event", "happening", "festival", "concert"]):
        sub_type = "Event"
    elif any(word in subject_lower for word in ["news", "announcement", "update"]):
        sub_type = "Announcement"
    elif any(word in subject_lower for word in ["tip", "story", "idea"]):
        sub_type = "Story_Idea"
    else:
        sub_type = "Other"
    
    # Extract date if present
    import re
    date_match = re.search(r'(\d{1,2}/\d{1,2}(?:/\d{2,4})?|(?:Jan|Feb|Mar|Apr|May|Jun|Jul|Aug|Sep|Oct|Nov|Dec)[a-z]*\.?\s+\d{1,2})', body, re.IGNORECASE)
    event_date = date_match.group(1) if date_match else None
    
    # Extract location
    locations = ['Wilkesboro', 'North Wilkesboro', 'Ronda', 'Hays', 'Millers Creek']
    found_location = None
    for loc in locations:
        if loc.lower() in body.lower():
            found_location = loc
            break
    
    return {
        "Submission_Type": sub_type,
        "Submitted_By_Name": from_addr.split("<")[0].strip() if "<" in from_addr else from_addr,
        "Submitted_By_Email": from_addr.split("<")[1].replace(">", "") if "<" in from_addr else from_addr,
        "Source_Channel": "Email",
        "Title": subject,
        "Body": body[:2000],  # Limit length
        "Related_Date": event_date,
        "Status": "New",
        "Notes": f"Location detected: {found_location}" if found_location else ""
    }
```

## Integration with AITable

```python
def process_email_submissions():
    """Full pipeline: check email → parse → add to AITable."""
    
    from email_checker import check_submission_emails
    from aitable_api import create_record  # Your existing AITable function
    
    # Check for new emails
    emails = check_submission_emails()
    
    for email_data in emails:
        # Parse into submission format
        submission = parse_submission_email(
            email_data["subject"],
            email_data["body"],
            email_data["from"]
        )
        
        # Add to AITable Submissions table
        create_record("Submissions", submission)
        
        print(f"✅ Added submission: {submission['Title'][:50]}...")
```

## Cron Setup

```bash
# Check for email submissions every 15 minutes
*/15 * * * * cd /root/.openclaw/workspace && python3 email_processor.py >> logs/email.log 2>&1

# Send daily newsletter at 8 AM
0 8 * * * cd /root/.openclaw/workspace && python3 send_daily_digest.py >> logs/newsletter.log 2>&1
```

## Email Commands

Users can email with specific subjects for auto-routing:

| Subject Prefix | Action |
|----------------|--------|
| `[EVENT]` or `[Event]` | Routes to Events table |
| `[NEWS]` or `[News]` | Routes to News_Raw table |
| `[TIP]` or `[Tip]` | Routes to Submissions |
| `[RESOURCE]` | Routes to Resources table |

## Newsletter Template

```html
<!DOCTYPE html>
<html>
<head>
    <meta charset="UTF-8">
    <title>Wilkes County Daily Digest</title>
    <style>
        body { font-family: Georgia, serif; max-width: 600px; margin: 0 auto; padding: 20px; }
        h1 { color: #2c5282; border-bottom: 3px solid #2c5282; padding-bottom: 10px; }
        .item { margin: 20px 0; padding: 15px; background: #f7fafc; border-left: 4px solid #2c5282; }
        .category { font-size: 0.8em; color: #718096; text-transform: uppercase; }
        .title { font-size: 1.2em; font-weight: bold; margin: 5px 0; }
        .source { font-size: 0.85em; color: #4a5568; }
        .footer { margin-top: 30px; padding-top: 20px; border-top: 1px solid #e2e8f0; font-size: 0.85em; color: #718096; }
    </style>
</head>
<body>
    <h1>📰 Wilkes County Daily Digest</h1>
    <p>{{date}}</p>
    
    {{content}}
    
    <div class="footer">
        <p>Submit news: <a href="mailto:wilkesbot@wilkesboro.net">wilkesbot@wilkesboro.net</a></p>
        <p>You're receiving this because you subscribed to Wilkes County updates.</p>
    </div>
</body>
</html>
```
