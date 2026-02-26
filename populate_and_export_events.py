#!/usr/bin/env python3
"""
Populate AITable Events with real data from scraped sources
Then export to Google Calendar
"""

import requests
from datetime import datetime

# AITable Config
AITABLE_TOKEN = "uskNPM9fPVHOgAGbDepyKER"
AITABLE_BASE = "https://api.aitable.ai/fusion/v1"
EVENTS_DATASHEET = "dstnnbs9qm9DZJkt8L"

def create_event_record(event_data):
    """Create a record in AITable Events."""
    url = f"{AITABLE_BASE}/datasheets/{EVENTS_DATASHEET}/records"
    
    headers = {
        "Authorization": f"Bearer {AITABLE_TOKEN}",
        "Content-Type": "application/json"
    }
    
    payload = {
        "records": [{"fields": event_data}]
    }
    
    try:
        response = requests.post(url, headers=headers, json=payload)
        if response.status_code == 200:
            return True
        else:
            print(f"  ⚠ Error: {response.status_code} - {response.text[:200]}")
            return False
    except Exception as e:
        print(f"  ⚠ Request failed: {e}")
        return False

def populate_real_events():
    """Add real events to AITable."""
    
    events = [
        {
            "Title": "Board of Commissioners Meeting",
            "Description": "Regular meeting of the Wilkes County Board of Commissioners. Public welcome.",
            "Date_Start": "2026-03-05",
            "Time_Start": "5:00 PM",
            "Venue_Name": "Wilkes County Office Building",
            "Venue_Address": "110 North St",
            "City": "Wilkesboro",
            "Organizer_Name": "Wilkes County Government",
            "Status": "Approved",
            "Tags": ["Government", "Meeting"]
        },
        {
            "Title": "Food Truck Fridays - Opening Night",
            "Description": "First Food Truck Friday of the season! Multiple food trucks, live music, family friendly.",
            "Date_Start": "2026-03-06",
            "Time_Start": "5:00 PM",
            "Venue_Name": "Downtown North Wilkesboro",
            "Venue_Address": "Main Street",
            "City": "North Wilkesboro",
            "Organizer_Name": "Town of North Wilkesboro",
            "Status": "Approved",
            "Tags": ["Food", "Music", "Family"]
        },
        {
            "Title": "NASCAR Craftsman Truck Series",
            "Description": "NASCAR Craftsman Truck Series race at North Wilkesboro Speedway.",
            "Date_Start": "2026-07-18",
            "Time_Start": "7:30 PM",
            "Venue_Name": "North Wilkesboro Speedway",
            "Venue_Address": "1800 Speedway Rd",
            "City": "North Wilkesboro",
            "Organizer_Name": "NASCAR",
            "Status": "Approved",
            "Tags": ["Sports", "NASCAR"]
        },
        {
            "Title": "NASCAR Cup Series - Window World 450",
            "Description": "NASCAR Cup Series race at historic North Wilkesboro Speedway.",
            "Date_Start": "2026-07-19",
            "Time_Start": "3:00 PM",
            "Venue_Name": "North Wilkesboro Speedway",
            "Venue_Address": "1800 Speedway Rd",
            "City": "North Wilkesboro",
            "Organizer_Name": "NASCAR",
            "Status": "Approved",
            "Tags": ["Sports", "NASCAR"]
        },
        {
            "Title": "Wilkes County Agricultural Fair",
            "Description": "Annual county fair with rides, livestock, food, and entertainment.",
            "Date_Start": "2026-10-01",
            "Time_Start": "All Day",
            "Venue_Name": "Wilkes County Fairgrounds",
            "City": "North Wilkesboro",
            "Organizer_Name": "Wilkes County Fair Association",
            "Status": "Approved",
            "Tags": ["Fair", "Family", "Agriculture"]
        },
        {
            "Title": "Wilkes County Agricultural Fair - Day 2",
            "Description": "Annual county fair continues.",
            "Date_Start": "2026-10-02",
            "Time_Start": "All Day",
            "Venue_Name": "Wilkes County Fairgrounds",
            "City": "North Wilkesboro",
            "Organizer_Name": "Wilkes County Fair Association",
            "Status": "Approved",
            "Tags": ["Fair", "Family", "Agriculture"]
        },
        {
            "Title": "Wilkes County Agricultural Fair - Day 3",
            "Description": "Annual county fair continues.",
            "Date_Start": "2026-10-03",
            "Time_Start": "All Day",
            "Venue_Name": "Wilkes County Fairgrounds",
            "City": "North Wilkesboro",
            "Organizer_Name": "Wilkes County Fair Association",
            "Status": "Approved",
            "Tags": ["Fair", "Family", "Agriculture"]
        },
        {
            "Title": "Wilkes County Agricultural Fair - Final Day",
            "Description": "Last day of the annual county fair.",
            "Date_Start": "2026-10-04",
            "Time_Start": "All Day",
            "Venue_Name": "Wilkes County Fairgrounds",
            "City": "North Wilkesboro",
            "Organizer_Name": "Wilkes County Fair Association",
            "Status": "Approved",
            "Tags": ["Fair", "Family", "Agriculture"]
        },
        {
            "Title": "Veterans Coffee Call",
            "Description": "Monthly gathering for veterans. Coffee and conversation.",
            "Date_Start": "2026-03-15",
            "Time_Start": "9:00 AM",
            "Venue_Name": "VFW Post 1142",
            "Venue_Address": "Veterans Drive",
            "City": "North Wilkesboro",
            "Organizer_Name": "VFW Post 1142",
            "Status": "Approved",
            "Tags": ["Veterans", "Community"]
        },
        {
            "Title": "Wilkes Genealogical Society Swap Meet",
            "Description": "History Fair and genealogy resource exchange.",
            "Date_Start": "2026-10-11",
            "Time_Start": "10:00 AM",
            "Venue_Name": "Wilkes Public Library",
            "City": "North Wilkesboro",
            "Organizer_Name": "Wilkes Genealogical Society",
            "Status": "Approved",
            "Tags": ["History", "Genealogy"]
        },
        {
            "Title": "Wilkes Senior Resources Masquerade Dance",
            "Description": "Fundraiser dance for senior resources. Costumes encouraged.",
            "Date_Start": "2026-10-24",
            "Time_Start": "6:00 PM",
            "Venue_Name": "The Walker Center",
            "City": "Wilkesboro",
            "Organizer_Name": "Wilkes Senior Resources",
            "Status": "Approved",
            "Tags": ["Seniors", "Dance", "Fundraiser"]
        },
        {
            "Title": "Public Hearing - DSS Building Use",
            "Description": "Public hearing on potential change of County Office Building to Wilkes DSS use.",
            "Date_Start": "2026-02-18",
            "Time_Start": "5:00 PM",
            "Venue_Name": "Wilkes County Office Building",
            "Venue_Address": "110 North St",
            "City": "Wilkesboro",
            "Organizer_Name": "Wilkes County Commissioners",
            "Status": "Approved",
            "Tags": ["Government", "Public Hearing"]
        }
    ]
    
    print(f"📝 Adding {len(events)} events to AITable...\n")
    
    added = 0
    for event in events:
        print(f"  → {event['Title'][:40]}...")
        if create_event_record(event):
            added += 1
            print(f"    ✅ Added")
        else:
            print(f"    ❌ Failed")
    
    print(f"\n✅ Successfully added {added}/{len(events)} events")
    return added

def export_to_google_calendar():
    """Export all events to CSV for Google Calendar."""
    print("\n" + "="*60)
    print(" Exporting to Google Calendar format...")
    print("="*60)
    
    # Re-run the export script
    import subprocess
    result = subprocess.run(['python3', 'export_events_to_calendar.py'], 
                          capture_output=True, text=True)
    print(result.stdout)
    if result.stderr:
        print(result.stderr)

def main():
    print("="*60)
    print(" Populate AITable Events + Export to Google Calendar")
    print("="*60)
    
    # Step 1: Add real events to AITable
    print("\n📥 Step 1: Adding real events to AITable...")
    populate_real_events()
    
    # Step 2: Export to Google Calendar format
    print("\n📤 Step 2: Exporting to Google Calendar format...")
    export_to_google_calendar()
    
    print("\n" + "="*60)
    print(" DONE!")
    print("="*60)
    print("\nNext steps:")
    print("1. Go to https://calendar.google.com")
    print("2. Find your 'Wilkesboro Community Events' calendar")
    print("3. Settings → Import & Export → Import")
    print("4. Upload: events_export.csv")
    print("5. Events will appear in your calendar!")

if __name__ == "__main__":
    main()
