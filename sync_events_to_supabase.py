#!/usr/bin/env python3
"""
Supabase Events Sync - Populate Events table with confirmed Wilkes County events
"""

import json
from datetime import datetime, timedelta
from supabase_client import create_record, fetch_records

# Confirmed Wilkes County Events
CONFIRMED_EVENTS = [
    {"title": "Wilkes County Board of Commissioners Meeting", "description": "Regular meeting - rescheduled from March 3.", "date_start": "2026-03-05", "time_start": "5:00 PM", "venue_name": "Commissioners' Meeting Room", "venue_address": "110 North Street", "city": "Wilkesboro", "organizer_name": "Wilkes County Government", "source_url": "https://www.wilkescounty.net", "status": "Approved", "tags": ["Government"]},
    {"title": "NC Primary Election Day", "description": "Primary Election Day for North Carolina. Polls open 6:30 AM - 7:30 PM.", "date_start": "2026-03-03", "time_start": "6:30 AM", "time_end": "7:30 PM", "venue_name": "Various Polling Locations", "venue_address": "Throughout Wilkes County", "city": "Wilkes County", "organizer_name": "NC State Board of Elections", "source_url": "https://www.ncsbe.gov", "status": "Approved", "tags": ["Government"]},
    {"title": "NASCAR Cup Series Race", "description": "NASCAR Cup Series race at North Wilkesboro Speedway.", "date_start": "2026-07-19", "time_start": "3:30 PM", "venue_name": "North Wilkesboro Speedway", "venue_address": "1801 US-421", "city": "North Wilkesboro", "organizer_name": "NASCAR", "source_url": "https://www.northwilkesborospeedway.com", "status": "Approved", "tags": ["Outdoor", "Family"]},
    {"title": "Brushy Mountain Apple Festival", "description": "One of the largest one-day arts and crafts festivals in the Southeast.", "date_start": "2026-10-03", "time_start": "9:00 AM", "time_end": "5:00 PM", "venue_name": "Downtown North Wilkesboro", "venue_address": "Main Street", "city": "North Wilkesboro", "organizer_name": "Brushy Mountain Ruritan Club", "source_url": "http://www.applefestival.net", "status": "Approved", "tags": ["Family", "Free", "Food", "Outdoor"]},
]

def main():
    print("="*60)
    print("WILKES COUNTY EVENTS → SUPABASE SYNC")
    print("="*60)
    
    print(f"\nAdding {len(CONFIRMED_EVENTS)} events to Supabase...")
    
    success_count = 0
    for event in CONFIRMED_EVENTS:
        print(f"  → {event['title'][:50]}...", end=" ")
        try:
            create_record("events", event)
            print("✓")
            success_count += 1
        except Exception as e:
            print(f"✗ {e}")
    
    print(f"\n✅ Successfully added {success_count}/{len(CONFIRMED_EVENTS)} events")

if __name__ == "__main__":
    main()
