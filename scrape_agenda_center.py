#!/usr/bin/env python3
"""
Wilkes County Agenda Center Scraper
Extracts meetings and agendas from wilkescounty.net/agendacenter
"""

import requests
import re
from datetime import datetime
from bs4 import BeautifulSoup

# AITable Configuration
AITABLE_TOKEN = "uskNPM9fPVHOgAGbDepyKER"
AITABLE_BASE = "https://aitable.ai/api/v1"
HEADERS = {
    "Authorization": f"Bearer {AITABLE_TOKEN}",
    "Content-Type": "application/json"
}

DATASHEETS = {
    "Events": "dstnnbs9qm9DZJkt8L",
    "News_Raw": "dstjSJ3rvilwBd3Bae"
}


def fetch_agenda_center():
    """Fetch and parse the agenda center page."""
    url = "https://wilkescounty.net/agendacenter"
    
    try:
        resp = requests.get(url, headers={
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
        }, timeout=20)
        resp.raise_for_status()
        
        soup = BeautifulSoup(resp.content, 'html.parser')
        
        meetings = []
        
        # Find all board/commission sections
        sections = soup.find_all(['h2', 'h3', 'div'], class_=re.compile('agenda|board|commission', re.I))
        
        # Also look for the specific structure we saw
        # The page has sections like "County Commissioners", "Board of Health"
        board_sections = soup.find_all(text=re.compile(r'County Commissioners|Board of Health|Planning Board|Board of Elections'))
        
        # Find meeting entries - they typically have dates and agenda links
        # Look for date patterns and associated links
        date_pattern = re.compile(r'(Jan|Feb|Mar|Apr|May|Jun|Jul|Aug|Sep|Oct|Nov|Dec)[a-z]*\.?\s+(\d{1,2}),?\s+(\d{4})', re.I)
        
        # Get all text and parse for meetings
        page_text = soup.get_text()
        
        # Find meeting entries by looking for date + "Agenda" patterns
        lines = page_text.split('\n')
        current_board = None
        
        for line in lines:
            line = line.strip()
            if not line:
                continue
            
            # Check if this is a board/commission header
            if any(board in line for board in ['County Commissioners', 'Board of Health', 'Planning Board', 'Board of Elections']):
                current_board = line.strip()
                continue
            
            # Look for date patterns
            date_match = date_pattern.search(line)
            if date_match and current_board:
                date_str = date_match.group(0)
                
                # Check if there's an agenda link nearby
                if 'agenda' in line.lower() or 'meeting' in line.lower():
                    meetings.append({
                        'board': current_board,
                        'date_str': date_str,
                        'title': line,
                        'raw': line
                    })
        
        # Alternative: Parse the HTML structure more directly
        # Look for rows with dates and agenda links
        meeting_rows = soup.find_all(['tr', 'div', 'li'], class_=re.compile('meeting|agenda|row', re.I))
        
        for row in meeting_rows:
            text = row.get_text()
            date_match = date_pattern.search(text)
            
            if date_match:
                # Find the board/commission context
                board = None
                for prev in row.find_all_previous(['h2', 'h3', 'h4']):
                    board_text = prev.get_text().strip()
                    if any(keyword in board_text for keyword in ['Commissioners', 'Health', 'Planning', 'Elections']):
                        board = board_text
                        break
                
                # Find agenda link
                agenda_link = None
                for link in row.find_all('a', href=True):
                    if 'agenda' in link.get_text().lower() or 'viewfile' in link['href'].lower():
                        agenda_link = link['href']
                        if not agenda_link.startswith('http'):
                            agenda_link = 'https://wilkescounty.net' + agenda_link
                        break
                
                meetings.append({
                    'board': board or 'Wilkes County Board',
                    'date_str': date_match.group(0),
                    'title': text[:100],
                    'agenda_url': agenda_link,
                    'raw': text[:200]
                })
        
        return meetings
        
    except Exception as e:
        print(f"Error fetching agenda center: {e}")
        return []


def parse_meeting_date(date_str):
    """Parse date string to ISO format."""
    formats = [
        '%b %d, %Y',
        '%B %d, %Y',
        '%b. %d, %Y',
        '%b %d %Y'
    ]
    
    for fmt in formats:
        try:
            dt = datetime.strptime(date_str.strip(), fmt)
            return dt.strftime('%Y-%m-%d')
        except:
            continue
    
    return None


def extract_meeting_details(text):
    """Extract meeting details from text."""
    details = {
        'time': None,
        'location': 'Wilkes County Office Building, 110 North St, Wilkesboro, NC'
    }
    
    # Look for time patterns
    time_match = re.search(r'(\d{1,2}:\d{2}\s*(?:AM|PM|am|pm))', text, re.I)
    if time_match:
        details['time'] = time_match.group(1)
    
    # Default times for known boards
    if 'commissioners' in text.lower():
        details['time'] = details['time'] or '5:00 PM'
    elif 'health' in text.lower():
        details['time'] = details['time'] or '6:00 PM'
    
    return details


def create_event_record(meeting):
    """Create an event record for AITable."""
    date_iso = parse_meeting_date(meeting['date_str'])
    details = extract_meeting_details(meeting.get('raw', ''))
    
    # Determine event title
    board_name = meeting.get('board', 'Wilkes County Board')
    title = f"{board_name} Meeting"
    
    # Create description
    description = f"Regular scheduled meeting of the {board_name}."
    if meeting.get('agenda_url'):
        description += f"\n\nAgenda: {meeting['agenda_url']}"
    
    return {
        'Title': title,
        'Description': description,
        'Date_Start': date_iso,
        'Time_Start': details['time'] or 'TBD',
        'Venue_Name': 'Wilkes County Office Building',
        'Venue_Address': details['location'],
        'City': 'Wilkesboro',
        'Organizer_Name': board_name,
        'Source_URL': meeting.get('agenda_url', 'https://wilkescounty.net/agendacenter'),
        'Status': 'New',
        'Tags': ['Government'],
        'Notes': f"Auto-imported from Agenda Center on {datetime.now().strftime('%Y-%m-%d')}"
    }


def create_news_record(meeting):
    """Create a news record for agenda posting."""
    date_iso = parse_meeting_date(meeting['date_str'])
    board_name = meeting.get('board', 'Wilkes County Board')
    
    return {
        'Title_Original': f"Agenda Posted: {board_name} - {meeting['date_str']}",
        'Body_Original': f"Agenda posted for {board_name} meeting scheduled for {meeting['date_str']}.\n\nView agenda: {meeting.get('agenda_url', 'https://wilkescounty.net/agendacenter')}",
        'Source_URL': meeting.get('agenda_url', 'https://wilkescounty.net/agendacenter'),
        'Source_Name': 'Wilkes County Agenda Center',
        'Source_Type': 'Gov',
        'Date_Original': datetime.now().isoformat(),
        'Category': 'Civics',
        'Status': 'New',
        'Location': 'Wilkesboro',
        'Summary_Short': f"Agenda posted for {board_name} meeting on {meeting['date_str']}",
        'Notes': f"Meeting date: {meeting['date_str']}"
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
            print(f"  ⚠ AITable error: {response.status_code}")
            return False
    except Exception as e:
        print(f"  ⚠ Request failed: {e}")
        return False


def main():
    print("="*60)
    print(" 📋 Wilkes County Agenda Center Scraper")
    print(f" {datetime.now().strftime('%Y-%m-%d %H:%M')}")
    print("="*60)
    
    # Fetch meetings
    print("\n🔍 Fetching agenda center...")
    meetings = fetch_agenda_center()
    
    print(f"\n📊 Found {len(meetings)} meetings")
    
    if not meetings:
        print("\n⚠ No meetings found - page structure may have changed")
        return
    
    # Display found meetings
    for m in meetings[:10]:  # Show first 10
        print(f"\n📅 {m.get('board', 'Unknown')}")
        print(f"   Date: {m.get('date_str', 'Unknown')}")
        print(f"   Agenda: {m.get('agenda_url', 'N/A')}")
    
    # Create records
    print(f"\n💾 Creating AITable records...")
    
    events_created = 0
    news_created = 0
    
    for meeting in meetings:
        # Create event record
        event_record = create_event_record(meeting)
        if create_aitable_record(DATASHEETS["Events"], event_record):
            events_created += 1
            print(f"  ✓ Event: {event_record['Title'][:50]}...")
        
        # Create news record for agenda posting
        news_record = create_news_record(meeting)
        if create_aitable_record(DATASHEETS["News_Raw"], news_record):
            news_created += 1
            print(f"  ✓ News: {news_record['Title_Original'][:50]}...")
    
    print(f"\n{'='*60}")
    print(f" ✅ Created {events_created} events, {news_created} news items")
    print(f"{'='*60}")


if __name__ == "__main__":
    main()
