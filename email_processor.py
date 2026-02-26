#!/usr/bin/env python3
"""
Email processor for wilkesbot@wilkesboro.net
Checks inbox, parses submissions, adds to AITable
"""

import imaplib
import email
from email.header import decode_header
import re
import requests
from datetime import datetime

# Email Configuration
IMAP_SERVER = "mail.wilkesboro.net"
IMAP_PORT = 993
EMAIL = "wilkesbot@wilkesboro.net"
PASSWORD = "squitch-unnerved-paly-stapling"

# AITable Configuration
AITABLE_TOKEN = "uskNPM9fPVHOgAGbDepyKER"
AITABLE_BASE = "https://aitable.ai/api/v1"
HEADERS = {
    "Authorization": f"Bearer {AITABLE_TOKEN}",
    "Content-Type": "application/json"
}

# Datasheet IDs
DATASHEETS = {
    "Submissions": "dstD2x1pp48NxsMCjs",
    "Events": "dstnnbs9qm9DZJkt8L",
    "News_Raw": "dstjSJ3rvilwBd3Bae"
}


def check_emails():
    """Check inbox for new submission emails."""
    submissions = []
    
    try:
        print(f"📧 Connecting to {IMAP_SERVER}...")
        mail = imaplib.IMAP4_SSL(IMAP_SERVER, IMAP_PORT)
        mail.login(EMAIL, PASSWORD)
        mail.select("inbox")
        
        # Search for unread emails
        status, messages = mail.search(None, "UNSEEN")
        
        if not messages[0]:
            print("📭 No new emails")
            mail.logout()
            return []
        
        print(f"📬 Found {len(messages[0].split())} new email(s)")
        
        for msg_num in messages[0].split():
            status, msg_data = mail.fetch(msg_num, "(RFC822)")
            
            for response_part in msg_data:
                if isinstance(response_part, tuple):
                    msg = email.message_from_bytes(response_part[1])
                    
                    # Decode subject
                    subject = decode_header_str(msg["Subject"])
                    from_addr = msg.get("From", "")
                    date_str = msg.get("Date", "")
                    
                    # Get body
                    body = extract_body(msg)
                    
                    submissions.append({
                        "subject": subject,
                        "from": from_addr,
                        "body": body,
                        "date": date_str
                    })
                    
                    # Mark as seen
                    mail.store(msg_num, "+FLAGS", "\\Seen")
        
        mail.logout()
        
    except Exception as e:
        print(f"❌ Email error: {e}")
    
    return submissions


def decode_header_str(header_value):
    """Safely decode email header."""
    if not header_value:
        return ""
    
    decoded = decode_header(header_value)
    result = ""
    
    for part, charset in decoded:
        if isinstance(part, bytes):
            result += part.decode(charset or "utf-8", errors="ignore")
        else:
            result += part
    
    return result


def extract_body(msg):
    """Extract text body from email message."""
    body = ""
    
    if msg.is_multipart():
        for part in msg.walk():
            content_type = part.get_content_type()
            content_disposition = str(part.get("Content-Disposition", ""))
            
            # Skip attachments
            if "attachment" in content_disposition:
                continue
            
            if content_type == "text/plain":
                try:
                    body = part.get_payload(decode=True).decode("utf-8", errors="ignore")
                    break
                except:
                    pass
            elif content_type == "text/html" and not body:
                try:
                    html = part.get_payload(decode=True).decode("utf-8", errors="ignore")
                    # Simple HTML to text
                    import html
                    body = html.unescape(re.sub(r'<[^>]+>', ' ', html))
                except:
                    pass
    else:
        try:
            body = msg.get_payload(decode=True).decode("utf-8", errors="ignore")
        except:
            pass
    
    return body.strip()


def parse_submission(subject, body, from_addr):
    """Parse email into structured submission."""
    subject_lower = subject.lower()
    
    # Detect type from subject prefixes
    if any(p in subject_lower for p in ["[event]", "event:", "happening:"]):
        sub_type = "Event"
    elif any(p in subject_lower for p in ["[news]", "news:", "announcement:"]):
        sub_type = "Announcement"
    elif any(p in subject_lower for p in ["[tip]", "tip:", "story:"]):
        sub_type = "Story_Idea"
    elif any(p in subject_lower for p in ["[resource]", "resource:"]):
        sub_type = "Resource"
    else:
        # Auto-detect from content
        if any(word in subject_lower for word in ["event", "festival", "concert", "meeting"]):
            sub_type = "Event"
        else:
            sub_type = "Other"
    
    # Extract sender info
    sender_name = from_addr.split("<")[0].strip().strip('"')
    sender_email = ""
    if "<" in from_addr:
        sender_email = from_addr.split("<")[1].replace(">", "").strip()
    else:
        sender_email = from_addr
    
    # Extract date from body
    date_match = re.search(
        r'(\d{1,2}/\d{1,2}(?:/\d{2,4})?|(?:Jan|Feb|Mar|Apr|May|Jun|Jul|Aug|Sep|Oct|Nov|Dec)[a-z]*\.?\s+\d{1,2}(?:,\s+\d{4})?)',
        body, re.IGNORECASE
    )
    event_date = date_match.group(1) if date_match else None
    
    # Extract location
    locations = ['Wilkesboro', 'North Wilkesboro', 'Ronda', 'Hays', 'Millers Creek', 'Purlear']
    found_location = None
    for loc in locations:
        if loc.lower() in body.lower():
            found_location = loc
            break
    
    return {
        "Submission_Type": sub_type,
        "Submitted_By_Name": sender_name or "Anonymous",
        "Submitted_By_Email": sender_email,
        "Source_Channel": "Email",
        "Title": subject[:200],
        "Body": body[:2000],
        "Related_Date": event_date,
        "Status": "New",
        "Notes": f"Location: {found_location}" if found_location else ""
    }


def create_aitable_record(datasheet_id, fields):
    """Create record in AITable."""
    url = f"{AITABLE_BASE}/datasheets/{datasheet_id}/records"
    payload = {"records": [{"fields": fields}]}
    
    try:
        response = requests.post(url, headers=HEADERS, json=payload)
        if response.status_code == 200:
            return True
        else:
            print(f"  ⚠ AITable error: {response.status_code} - {response.text[:200]}")
            return False
    except Exception as e:
        print(f"  ⚠ Request failed: {e}")
        return False


def main():
    print("="*60)
    print(" 📧 WilkesBot Email Processor")
    print(f" {datetime.now().strftime('%Y-%m-%d %H:%M')}")
    print("="*60)
    
    # Check for emails
    emails = check_emails()
    
    if not emails:
        print("\n✓ Nothing to process")
        return
    
    # Process each email
    processed = 0
    for email_data in emails:
        print(f"\n📨 Processing: {email_data['subject'][:50]}...")
        print(f"   From: {email_data['from']}")
        
        # Parse into submission
        submission = parse_submission(
            email_data['subject'],
            email_data['body'],
            email_data['from']
        )
        
        print(f"   Type: {submission['Submission_Type']}")
        
        # Add to AITable
        # TODO: Update DATASHEETS["Submissions"] with actual ID
        # For now, just print what would be created
        print(f"   📝 Would create: {submission['Title'][:40]}...")
        print(f"   📋 Submission data:")
        for key, val in submission.items():
            if val:
                print(f"      {key}: {str(val)[:60]}{'...' if len(str(val)) > 60 else ''}")
        
        # Add to AITable
        if create_aitable_record(DATASHEETS["Submissions"], submission):
            processed += 1
            print("   ✅ Added to AITable")
    
    print(f"\n{'='*60}")
    print(f" ✅ Processed {processed} email(s)")
    print(f"{'='*60}")


if __name__ == "__main__":
    main()
