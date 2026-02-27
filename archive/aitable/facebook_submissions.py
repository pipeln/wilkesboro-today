#!/usr/bin/env python3
"""
Facebook Group Monitoring via Community Submissions
Since Facebook blocks scraping, this uses AITable forms + Telegram bot for community input.
"""

import requests
from datetime import datetime

API_TOKEN = "uskNPM9fPVHOgAGbDepyKER"
BASE_URL = "https://aitable.ai/api/v1"
HEADERS = {
    "Authorization": f"Bearer {API_TOKEN}",
    "Content-Type": "application/json"
}

# Facebook Groups to Monitor (for reference - we'll use manual/community input)
FACEBOOK_GROUPS = [
    {"name": "Wilkes County, NC Community", "id": "wilkescommunity", "type": "community"},
    {"name": "Wilkesboro NC Buy Sell Trade", "id": "wilkesbuy sell", "type": "marketplace"},
    {"name": "North Wilkesboro Community", "id": "northwilkes", "type": "community"},
    {"name": "Wilkes County Events", "id": "wilkesevent s", "type": "events"}
]

# AITable Datasheet IDs
DATASHEETS = {
    "Submissions": "dstXXXX",  # Update with actual ID
    "Events": "dstnnbs9qm9DZJkt8L",
    "News_Raw": "dstjSJ3rvilwBd3Bae"
}


def check_submissions():
    """Check AITable Submissions table for new Facebook-sourced tips."""
    url = f"{BASE_URL}/datasheets/{DATASHEETS['Submissions']}/records"
    
    try:
        response = requests.get(url, headers=HEADERS)
        if response.status_code == 200:
            data = response.json()
            return data.get('records', [])
    except Exception as e:
        print(f"Error checking submissions: {e}")
    
    return []


def process_facebook_submission(submission):
    """Process a Facebook-sourced submission into Events or News."""
    fields = submission.get('fields', {})
    
    # Determine if it's an event or news
    sub_type = fields.get('Submission_Type', 'Other')
    
    if sub_type == 'Event':
        return {
            'datasheet': 'Events',
            'record': {
                'Title': fields.get('Title', ''),
                'Description': fields.get('Body', ''),
                'Date_Start': fields.get('Related_Date', ''),
                'Venue_Name': extract_venue(fields.get('Body', '')),
                'City': extract_city(fields.get('Body', '')),
                'Organizer_Name': fields.get('Submitted_By_Name', ''),
                'Source_URL': fields.get('Related_Resource_ID', ''),  # Could be FB link
                'Submission_Channel': 'Facebook',
                'Status': 'Needs_Review',
                'Notes': f"Submitted via Facebook/community on {datetime.now().strftime('%Y-%m-%d')}"
            }
        }
    else:
        return {
            'datasheet': 'News_Raw',
            'record': {
                'Title_Original': fields.get('Title', ''),
                'Body_Original': fields.get('Body', ''),
                'Source_Name': f"Facebook - {fields.get('Submitted_By_Name', 'Unknown')}",
                'Source_Type': 'Social',
                'Date_Original': datetime.now().isoformat(),
                'Category': 'Community',
                'Status': 'Needs_Review',
                'Notes': f"Community submission from Facebook"
            }
        }


def extract_venue(text):
    """Try to extract venue from event description."""
    # Simple extraction - look for common venue patterns
    import re
    
    # Look for "at [Venue]" or "@ [Venue]"
    patterns = [
        r'at\s+([A-Z][A-Za-z\s]+(?:Hall|Center|Park|Library|School|Church|Building))',
        r'@\s+([A-Z][A-Za-z\s]+)',
        r'Location:\s*([^\n]+)',
        r'Venue:\s*([^\n]+)'
    ]
    
    for pattern in patterns:
        match = re.search(pattern, text, re.IGNORECASE)
        if match:
            return match.group(1).strip()
    
    return ''


def extract_city(text):
    """Extract city from text."""
    cities = ['Wilkesboro', 'North Wilkesboro', 'Ronda', 'Hays']
    for city in cities:
        if city.lower() in text.lower():
            return city
    return 'Wilkes County'


def create_record(datasheet_id, record):
    """Create a single record in AITable."""
    url = f"{BASE_URL}/datasheets/{datasheet_id}/records"
    payload = {"records": [{"fields": record}]}
    
    try:
        response = requests.post(url, headers=HEADERS, json=payload)
        return response.status_code == 200
    except Exception as e:
        print(f"Error creating record: {e}")
        return False


def generate_submission_form_html():
    """Generate HTML for a simple submission form that feeds into AITable."""
    html = '''
<!DOCTYPE html>
<html>
<head>
    <title>Submit Wilkes County News/Event</title>
    <style>
        body { font-family: Arial, sans-serif; max-width: 600px; margin: 50px auto; padding: 20px; }
        label { display: block; margin-top: 15px; font-weight: bold; }
        input, textarea, select { width: 100%; padding: 8px; margin-top: 5px; }
        button { margin-top: 20px; padding: 10px 20px; background: #007cba; color: white; border: none; cursor: pointer; }
        button:hover { background: #005a87; }
    </style>
</head>
<body>
    <h1>Submit News or Event</h1>
    <p>Help keep the community informed! Submit news tips, events, or announcements.</p>
    
    <form action="YOUR_AITABLE_FORM_ENDPOINT" method="POST">
        <label>Type:</label>
        <select name="Submission_Type">
            <option value="Event">Event</option>
            <option value="Announcement">Announcement</option>
            <option value="Story_Idea">Story Idea</option>
            <option value="Other">Other</option>
        </select>
        
        <label>Your Name:</label>
        <input type="text" name="Submitted_By_Name" placeholder="Your name (optional)">
        
        <label>Title:</label>
        <input type="text" name="Title" placeholder="Event or news title" required>
        
        <label>Details:</label>
        <textarea name="Body" rows="6" placeholder="Describe the event or news..." required></textarea>
        
        <label>Date (if applicable):</label>
        <input type="date" name="Related_Date">
        
        <label>Source Link (Facebook post, website, etc.):</label>
        <input type="url" name="Related_Resource_ID" placeholder="https://...">
        
        <button type="submit">Submit</button>
    </form>
    
    <p style="margin-top: 30px; font-size: 0.9em; color: #666;">
        Submissions are reviewed before publishing. Thank you for contributing!
    </p>
</body>
</html>
    '''
    return html


def main():
    print("="*60)
    print(" Facebook/Community Submission Processor")
    print("="*60)
    
    # Check for new submissions
    submissions = check_submissions()
    
    if not submissions:
        print("\nℹ No new submissions to process")
        return
    
    print(f"\n📥 Found {len(submissions)} submissions")
    
    processed = 0
    for sub in submissions:
        result = process_facebook_submission(sub)
        if result:
            datasheet = DATASHEETS[result['datasheet']]
            if create_record(datasheet, result['record']):
                processed += 1
                print(f"  ✓ Processed: {result['record'].get('Title', result['record'].get('Title_Original', 'Unknown'))[:50]}...")
    
    print(f"\n✅ Processed {processed}/{len(submissions)} submissions")
    
    # Save form HTML for reference
    with open('/root/.openclaw/workspace/community_form.html', 'w') as f:
        f.write(generate_submission_form_html())
    
    print("\n📝 Form template saved to: community_form.html")
    print("="*60)


if __name__ == "__main__":
    main()
