#!/usr/bin/env python3
"""
Wilkes County Agenda Center Scraper - Supabase Version
Extracts meetings and agendas from wilkescounty.net/agendacenter
"""

import requests
import re
from datetime import datetime
from bs4 import BeautifulSoup
from supabase_client import create_record

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
        date_pattern = re.compile(r'(Jan|Feb|Mar|Apr|May|Jun|Jul|Aug|Sep|Oct|Nov|Dec)[a-z]*\.?\s+(\d{1,2}),?\s+(\d{4})', re.I)
        
        page_text = soup.get_text()
        lines = page_text.split('\n')
        current_board = None
        
        for line in lines:
            line = line.strip()
            if not line:
                continue
            
            if any(board in line for board in ['County Commissioners', 'Board of Health', 'Planning Board', 'Board of Elections']):
                current_board = line.strip()
                continue
            
            date_match = date_pattern.search(line)
            if date_match and current_board:
                date_str = date_match.group(0)
                if 'agenda' in line.lower() or 'meeting' in line.lower():
                    meetings.append({'board': current_board, 'date_str': date_str, 'raw': line})
        
        return meetings
    except Exception as e:
        print(f"Error fetching agenda center: {e}")
        return []

def parse_meeting_date(date_str):
    """Parse date string to ISO format."""
    formats = ['%b %d, %Y', '%B %d, %Y', '%b. %d, %Y', '%b %d %Y']
    for fmt in formats:
        try:
            dt = datetime.strptime(date_str.strip(), fmt)
            return dt.strftime('%Y-%m-%d')
        except:
            continue
    return None

def main():
    print("="*60)
    print(" Wilkes County Agenda Center Scraper → Supabase")
    print("="*60)
    
    meetings = fetch_agenda_center()
    print(f"Found {len(meetings)} meetings")
    
    for meeting in meetings:
        date_iso = parse_meeting_date(meeting['date_str'])
        record = {
            'title': f"{meeting['board']} Meeting",
            'date_start': date_iso,
            'city': 'Wilkesboro',
            'status': 'New',
            'tags': ['Government']
        }
        try:
            create_record("events", record)
            print(f"  Created: {record['title']}")
        except Exception as e:
            print(f"  Error: {e}")

if __name__ == "__main__":
    main()
