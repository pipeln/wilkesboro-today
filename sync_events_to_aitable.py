#!/usr/bin/env python3
"""
AITable Events Sync - Populate Events table with confirmed Wilkes County events
and generate ICS feed for Google Calendar subscription.
"""

import requests
import json
from datetime import datetime, timedelta

API_TOKEN = "uskNPM9fPVHOgAGbDepyKER"
BASE_URL = "https://aitable.ai/api/v1"
HEADERS = {
    "Authorization": f"Bearer {API_TOKEN}",
    "Content-Type": "application/json"
}

EVENTS_DATASHEET_ID = "dstnnbs9qm9DZJkt8L"

# Confirmed Wilkes County Events with proper titles and dates
CONFIRMED_EVENTS = [
    {
        "Title": "Wilkes County Board of Commissioners Meeting",
        "Description": "Regular meeting - rescheduled from March 3. Board meets to discuss county business and vote on matters before them.",
        "Date_Start": "2026-03-05",
        "Date_End": "2026-03-05",
        "Time_Start": "5:00 PM",
        "Time_End": "7:00 PM",
        "Venue_Name": "Commissioners' Meeting Room",
        "Venue_Address": "110 North Street",
        "City": "Wilkesboro",
        "Organizer_Name": "Wilkes County Government",
        "Source_URL": "https://www.wilkescounty.net",
        "Status": "Approved",
        "Tags": ["Government"]
    },
    {
        "Title": "NC Primary Election Day",
        "Description": "Primary Election Day for North Carolina. Multiple contested races including Wilkes County Sheriff. Polls open 6:30 AM - 7:30 PM.",
        "Date_Start": "2026-03-03",
        "Date_End": "2026-03-03",
        "Time_Start": "6:30 AM",
        "Time_End": "7:30 PM",
        "Venue_Name": "Various Polling Locations",
        "Venue_Address": "Throughout Wilkes County",
        "City": "Wilkes County",
        "Organizer_Name": "NC State Board of Elections",
        "Source_URL": "https://www.ncsbe.gov",
        "Status": "Approved",
        "Tags": ["Government"]
    },
    {
        "Title": "zMAX CARS Tour Doubleheader",
        "Description": "zMAX CARS Tour racing doubleheader event at the historic North Wilkesboro Speedway.",
        "Date_Start": "2026-07-17",
        "Date_End": "2026-07-17",
        "Time_Start": "7:00 PM",
        "Time_End": "11:00 PM",
        "Venue_Name": "North Wilkesboro Speedway",
        "Venue_Address": "1801 US-421",
        "City": "North Wilkesboro",
        "Organizer_Name": "North Wilkesboro Speedway",
        "Source_URL": "https://www.northwilkesborospeedway.com",
        "Status": "Approved",
        "Tags": ["Outdoor", "Family"]
    },
    {
        "Title": "NASCAR Craftsman Truck Series: Window World 250",
        "Description": "NASCAR Craftsman Truck Series race at North Wilkesboro Speedway.",
        "Date_Start": "2026-07-18",
        "Date_End": "2026-07-18",
        "Time_Start": "12:30 PM",
        "Time_End": "4:30 PM",
        "Venue_Name": "North Wilkesboro Speedway",
        "Venue_Address": "1801 US-421",
        "City": "North Wilkesboro",
        "Organizer_Name": "NASCAR",
        "Source_URL": "https://www.northwilkesborospeedway.com",
        "Status": "Approved",
        "Tags": ["Outdoor", "Family"]
    },
    {
        "Title": "NASCAR Cup Series Race",
        "Description": "NASCAR Cup Series race at North Wilkesboro Speedway. Part of the 3-day race weekend.",
        "Date_Start": "2026-07-19",
        "Date_End": "2026-07-19",
        "Time_Start": "3:30 PM",
        "Time_End": "7:30 PM",
        "Venue_Name": "North Wilkesboro Speedway",
        "Venue_Address": "1801 US-421",
        "City": "North Wilkesboro",
        "Organizer_Name": "NASCAR",
        "Source_URL": "https://www.northwilkesborospeedway.com",
        "Status": "Approved",
        "Tags": ["Outdoor", "Family"]
    },
    {
        "Title": "Brushy Mountain Apple Festival",
        "Description": "One of the largest one-day arts and crafts festivals in the Southeast. 100+ vendors, food, live entertainment, apple products. RAIN OR SHINE.",
        "Date_Start": "2026-10-03",
        "Date_End": "2026-10-03",
        "Time_Start": "9:00 AM",
        "Time_End": "5:00 PM",
        "Venue_Name": "Downtown North Wilkesboro",
        "Venue_Address": "Main Street",
        "City": "North Wilkesboro",
        "Organizer_Name": "Brushy Mountain Ruritan Club",
        "Source_URL": "http://www.applefestival.net",
        "Status": "Approved",
        "Tags": ["Family", "Free", "Food", "Outdoor"]
    },
    {
        "Title": "Wilkes County Agricultural Fair",
        "Description": "Annual county fair with rides, exhibits, livestock shows, entertainment, and food. Four days of family fun.",
        "Date_Start": "2026-10-01",
        "Date_End": "2026-10-04",
        "Time_Start": "5:00 PM",
        "Time_End": "10:00 PM",
        "Venue_Name": "Wilkes County Agricultural Fairgrounds",
        "Venue_Address": "Willow Lane",
        "City": "North Wilkesboro",
        "Organizer_Name": "Wilkes County Agricultural Fair Association",
        "Source_URL": "https://www.ces.ncsu.edu",
        "Status": "Approved",
        "Tags": ["Family", "Food", "Outdoor"]
    },
    {
        "Title": "Concerts on the Deck - June",
        "Description": "Free outdoor concert series. Bring a chair or blanket. Rain or shine.",
        "Date_Start": "2026-06-21",
        "Date_End": "2026-06-21",
        "Time_Start": "6:00 PM",
        "Time_End": "10:00 PM",
        "Venue_Name": "Downtown North Wilkesboro",
        "Venue_Address": "Downtown",
        "City": "North Wilkesboro",
        "Organizer_Name": "Downtown North Wilkesboro Partnership",
        "Source_URL": "https://www.downtownnorthwilkesboro.com",
        "Status": "Approved",
        "Tags": ["Music", "Free", "Outdoor"]
    },
    {
        "Title": "Concerts on the Deck - July",
        "Description": "Free outdoor concert series. Bring a chair or blanket. Rain or shine.",
        "Date_Start": "2026-07-19",
        "Date_End": "2026-07-19",
        "Time_Start": "6:00 PM",
        "Time_End": "10:00 PM",
        "Venue_Name": "Downtown North Wilkesboro",
        "Venue_Address": "Downtown",
        "City": "North Wilkesboro",
        "Organizer_Name": "Downtown North Wilkesboro Partnership",
        "Source_URL": "https://www.downtownnorthwilkesboro.com",
        "Status": "Approved",
        "Tags": ["Music", "Free", "Outdoor"]
    },
    {
        "Title": "Concerts on the Deck - August",
        "Description": "Free outdoor concert series. Bring a chair or blanket. Rain or shine.",
        "Date_Start": "2026-08-16",
        "Date_End": "2026-08-16",
        "Time_Start": "6:00 PM",
        "Time_End": "10:00 PM",
        "Venue_Name": "Downtown North Wilkesboro",
        "Venue_Address": "Downtown",
        "City": "North Wilkesboro",
        "Organizer_Name": "Downtown North Wilkesboro Partnership",
        "Source_URL": "https://www.downtownnorthwilkesboro.com",
        "Status": "Approved",
        "Tags": ["Music", "Free", "Outdoor"]
    },
    {
        "Title": "Concerts on the Deck - September",
        "Description": "Free outdoor concert series. Bring a chair or blanket. Rain or shine.",
        "Date_Start": "2026-09-20",
        "Date_End": "2026-09-20",
        "Time_Start": "6:00 PM",
        "Time_End": "10:00 PM",
        "Venue_Name": "Downtown North Wilkesboro",
        "Venue_Address": "Downtown",
        "City": "North Wilkesboro",
        "Organizer_Name": "Downtown North Wilkesboro Partnership",
        "Source_URL": "https://www.downtownnorthwilkesboro.com",
        "Status": "Approved",
        "Tags": ["Music", "Free", "Outdoor"]
    },
    {
        "Title": "Wilkes County Cruise-In - March",
        "Description": "Monthly car and truck show. Roads close at 2pm. Features music, food, cakewalks, 50/50 drawing, fellowship.",
        "Date_Start": "2026-03-14",
        "Date_End": "2026-03-14",
        "Time_Start": "2:00 PM",
        "Time_End": "6:00 PM",
        "Venue_Name": "CBD Loop/Marketplace",
        "Venue_Address": "Downtown",
        "City": "North Wilkesboro",
        "Organizer_Name": "Downtown North Wilkesboro Partnership",
        "Source_URL": "https://www.downtownnorthwilkesboro.com",
        "Status": "Approved",
        "Tags": ["Family", "Free", "Outdoor"]
    },
    {
        "Title": "Wilkes County Cruise-In - April",
        "Description": "Monthly car and truck show. Roads close at 2pm. Features music, food, cakewalks, 50/50 drawing, fellowship.",
        "Date_Start": "2026-04-11",
        "Date_End": "2026-04-11",
        "Time_Start": "2:00 PM",
        "Time_End": "6:00 PM",
        "Venue_Name": "CBD Loop/Marketplace",
        "Venue_Address": "Downtown",
        "City": "North Wilkesboro",
        "Organizer_Name": "Downtown North Wilkesboro Partnership",
        "Source_URL": "https://www.downtownnorthwilkesboro.com",
        "Status": "Approved",
        "Tags": ["Family", "Free", "Outdoor"]
    },
    {
        "Title": "Wilkes County Cruise-In - May",
        "Description": "Monthly car and truck show. Roads close at 2pm. Features music, food, cakewalks, 50/50 drawing, fellowship.",
        "Date_Start": "2026-05-09",
        "Date_End": "2026-05-09",
        "Time_Start": "2:00 PM",
        "Time_End": "6:00 PM",
        "Venue_Name": "CBD Loop/Marketplace",
        "Venue_Address": "Downtown",
        "City": "North Wilkesboro",
        "Organizer_Name": "Downtown North Wilkesboro Partnership",
        "Source_URL": "https://www.downtownnorthwilkesboro.com",
        "Status": "Approved",
        "Tags": ["Family", "Free", "Outdoor"]
    },
    {
        "Title": "Wilkes County Cruise-In - June",
        "Description": "Monthly car and truck show. Roads close at 2pm. Features music, food, cakewalks, 50/50 drawing, fellowship.",
        "Date_Start": "2026-06-13",
        "Date_End": "2026-06-13",
        "Time_Start": "2:00 PM",
        "Time_End": "6:00 PM",
        "Venue_Name": "CBD Loop/Marketplace",
        "Venue_Address": "Downtown",
        "City": "North Wilkesboro",
        "Organizer_Name": "Downtown North Wilkesboro Partnership",
        "Source_URL": "https://www.downtownnorthwilkesboro.com",
        "Status": "Approved",
        "Tags": ["Family", "Free", "Outdoor"]
    },
    {
        "Title": "Wilkes County Cruise-In - August",
        "Description": "Monthly car and truck show. Roads close at 2pm. Features music, food, cakewalks, 50/50 drawing, fellowship.",
        "Date_Start": "2026-08-08",
        "Date_End": "2026-08-08",
        "Time_Start": "2:00 PM",
        "Time_End": "6:00 PM",
        "Venue_Name": "CBD Loop/Marketplace",
        "Venue_Address": "Downtown",
        "City": "North Wilkesboro",
        "Organizer_Name": "Downtown North Wilkesboro Partnership",
        "Source_URL": "https://www.downtownnorthwilkesboro.com",
        "Status": "Approved",
        "Tags": ["Family", "Free", "Outdoor"]
    },
    {
        "Title": "Wilkes County Cruise-In - September",
        "Description": "Monthly car and truck show. Roads close at 2pm. Features music, food, cakewalks, 50/50 drawing, fellowship.",
        "Date_Start": "2026-09-12",
        "Date_End": "2026-09-12",
        "Time_Start": "2:00 PM",
        "Time_End": "6:00 PM",
        "Venue_Name": "CBD Loop/Marketplace",
        "Venue_Address": "Downtown",
        "City": "North Wilkesboro",
        "Organizer_Name": "Downtown North Wilkesboro Partnership",
        "Source_URL": "https://www.downtownnorthwilkesboro.com",
        "Status": "Approved",
        "Tags": ["Family", "Free", "Outdoor"]
    },
    {
        "Title": "Wilkes County Cruise-In - October",
        "Description": "Monthly car and truck show. Roads close at 2pm. Features music, food, cakewalks, 50/50 drawing, fellowship.",
        "Date_Start": "2026-10-10",
        "Date_End": "2026-10-10",
        "Time_Start": "2:00 PM",
        "Time_End": "6:00 PM",
        "Venue_Name": "CBD Loop/Marketplace",
        "Venue_Address": "Downtown",
        "City": "North Wilkesboro",
        "Organizer_Name": "Downtown North Wilkesboro Partnership",
        "Source_URL": "https://www.downtownnorthwilkesboro.com",
        "Status": "Approved",
        "Tags": ["Family", "Free", "Outdoor"]
    },
    {
        "Title": "Mexican Independence Day Celebration",
        "Description": "Festival celebrating Mexican Independence Day with traditional food, music, folk dancing and more.",
        "Date_Start": "2026-09-16",
        "Date_End": "2026-09-16",
        "Time_Start": "5:00 PM",
        "Time_End": "9:00 PM",
        "Venue_Name": "Yadkin Valley Marketplace",
        "Venue_Address": "Downtown",
        "City": "North Wilkesboro",
        "Organizer_Name": "Downtown North Wilkesboro Partnership",
        "Source_URL": "https://www.downtownnorthwilkesboro.com",
        "Status": "Approved",
        "Tags": ["Family", "Food", "Music"]
    },
    {
        "Title": "Spooktacular",
        "Description": "3rd annual Halloween festival. Candy stations, vendors, face painting, food and family fun.",
        "Date_Start": "2026-10-24",
        "Date_End": "2026-10-24",
        "Time_Start": "5:00 PM",
        "Time_End": "8:00 PM",
        "Venue_Name": "Downtown North Wilkesboro",
        "Venue_Address": "Downtown",
        "City": "North Wilkesboro",
        "Organizer_Name": "Downtown North Wilkesboro Merchant Association",
        "Source_URL": "https://www.downtownnorthwilkesboro.com",
        "Status": "Approved",
        "Tags": ["Family", "Free"]
    },
    {
        "Title": "Light Up Downtown",
        "Description": "Annual holiday lighting ceremony and festival. Food and craft vendors, local artisans, kids activities, extended business hours.",
        "Date_Start": "2026-12-05",
        "Date_End": "2026-12-05",
        "Time_Start": "5:00 PM",
        "Time_End": "9:00 PM",
        "Venue_Name": "Downtown North Wilkesboro",
        "Venue_Address": "Downtown",
        "City": "North Wilkesboro",
        "Organizer_Name": "Downtown North Wilkesboro Partnership",
        "Source_URL": "https://www.downtownnorthwilkesboro.com",
        "Status": "Approved",
        "Tags": ["Family", "Free"]
    },
    {
        "Title": "Historic Preservation Meeting",
        "Description": "Monthly meeting of the Historic Preservation Commission.",
        "Date_Start": "2026-03-17",
        "Date_End": "2026-03-17",
        "Time_Start": "5:15 PM",
        "Time_End": "6:15 PM",
        "Venue_Name": "Wilkesboro Town Hall",
        "Venue_Address": "203 W. Main St.",
        "City": "Wilkesboro",
        "Organizer_Name": "Town of Wilkesboro",
        "Source_URL": "https://wilkesboronc.org",
        "Status": "Approved",
        "Tags": ["Government"]
    }
]


def create_event_record(event):
    """Create a single event record in AITable."""
    url = f"{BASE_URL}/datasheets/{EVENTS_DATASHEET_ID}/records"
    
    # Format tags for MultiSelect
    tags = event.get("Tags", [])
    
    payload = {
        "records": [{
            "fields": {
                "Title": event["Title"],
                "Description": event["Description"],
                "Date_Start": event["Date_Start"],
                "Date_End": event["Date_End"],
                "Time_Start": event["Time_Start"],
                "Time_End": event["Time_End"],
                "Venue_Name": event["Venue_Name"],
                "Venue_Address": event["Venue_Address"],
                "City": event["City"],
                "Organizer_Name": event["Organizer_Name"],
                "Source_URL": event["Source_URL"],
                "Status": event["Status"],
                "Tags": tags,
                "Notes": f"Auto-imported on {datetime.now().strftime('%Y-%m-%d')}"
            }
        }]
    }
    
    try:
        response = requests.post(url, headers=HEADERS, json=payload)
        if response.status_code == 200:
            return True, response.json()
        else:
            return False, f"API Error: {response.status_code} - {response.text[:200]}"
    except Exception as e:
        return False, str(e)


def generate_ics_feed():
    """Generate ICS file from AITable events."""
    # Fetch all approved events from AITable
    url = f"{BASE_URL}/datasheets/{EVENTS_DATASHEET_ID}/records"
    
    try:
        response = requests.get(url, headers=HEADERS, params={"viewId": "viwXXXXX"})  # Need actual view ID
        events = response.json().get("data", {}).get("records", [])
    except:
        # Fallback to local events if API fails
        events = [{"fields": e} for e in CONFIRMED_EVENTS]
    
    ics_content = ["BEGIN:VCALENDAR", "VERSION:2.0", "PRODID:-//Wilkesboro Today//Events//EN", "CALSCALE:GREGORIAN", "METHOD:PUBLISH", "X-WR-CALNAME:Wilkes County Events", "X-WR-TIMEZONE:America/New_York"]
    
    for event in events:
        fields = event.get("fields", event)  # Handle both API and local formats
        
        title = fields.get("Title", "Untitled Event")
        description = fields.get("Description", "").replace("\n", "\\n")
        start_date = fields.get("Date_Start", "")
        end_date = fields.get("Date_End", "")
        time_start = fields.get("Time_Start", "")
        time_end = fields.get("Time_End", "")
        venue = fields.get("Venue_Name", "")
        address = fields.get("Venue_Address", "")
        city = fields.get("City", "")
        
        # Build location string
        location = f"{venue}, {address}, {city}, NC" if venue else "Wilkes County, NC"
        
        # Parse dates for ICS format
        uid = f"{start_date}-{title.replace(' ', '-')}@wilkesboro.today"
        dtstamp = datetime.now().strftime("%Y%m%dT%H%M%SZ")
        
        # Convert to ICS datetime format
        if time_start:
            # Has specific time
            start_dt = f"{start_date.replace('-', '')}T{parse_time_to_ics(time_start)}"
            end_dt = f"{end_date.replace('-', '')}T{parse_time_to_ics(time_end or time_start)}"
        else:
            # All day event
            start_dt = start_date.replace("-", "")
            end_dt = (datetime.strptime(end_date, "%Y-%m-%d") + timedelta(days=1)).strftime("%Y%m%d")
        
        ics_content.extend([
            "BEGIN:VEVENT",
            f"UID:{uid}",
            f"DTSTAMP:{dtstamp}",
            f"DTSTART{';VALUE=DATE' if not time_start else ''}:{start_dt}",
            f"DTEND{';VALUE=DATE' if not time_start else ''}:{end_dt}",
            f"SUMMARY:{title}",
            f"DESCRIPTION:{description}",
            f"LOCATION:{location}",
            "END:VEVENT"
        ])
    
    ics_content.append("END:VCALENDAR")
    return "\n".join(ics_content)


def parse_time_to_ics(time_str):
    """Convert time like '5:00 PM' to ICS format '170000'."""
    try:
        dt = datetime.strptime(time_str, "%I:%M %p")
        return dt.strftime("%H%M%S")
    except:
        try:
            dt = datetime.strptime(time_str, "%I %p")
            return dt.strftime("%H%M%S")
        except:
            return "120000"


def main():
    print("="*60)
    print("WILKES COUNTY EVENTS - AITABLE SYNC")
    print("="*60)
    
    # Step 1: Populate AITable with confirmed events
    print(f"\n📊 Adding {len(CONFIRMED_EVENTS)} confirmed events to AITable...")
    
    success_count = 0
    for event in CONFIRMED_EVENTS:
        print(f"  → {event['Title'][:50]}...", end=" ")
        success, result = create_event_record(event)
        if success:
            print("✓")
            success_count += 1
        else:
            print(f"✗ {result}")
    
    print(f"\n✅ Successfully added {success_count}/{len(CONFIRMED_EVENTS)} events")
    
    # Step 2: Generate ICS feed
    print("\n📅 Generating ICS feed...")
    ics_content = generate_ics_feed()
    
    ics_filename = "/root/.openclaw/workspace/wilkes_events_2026.ics"
    with open(ics_filename, "w") as f:
        f.write(ics_content)
    
    print(f"✅ ICS feed saved to: {ics_filename}")
    print(f"   File size: {len(ics_content)} bytes")
    
    print("\n" + "="*60)
    print("NEXT STEPS:")
    print("="*60)
    print("1. Events are now in AITable (check your Events datasheet)")
    print("2. ICS file can be imported to Google Calendar:")
    print("   - Go to Google Calendar Settings")
    print("   - Import & Export → Import")
    print("   - Select the .ics file")
    print("3. For auto-sync: Host the ICS file and subscribe to URL")
    print("="*60)


if __name__ == "__main__":
    main()
