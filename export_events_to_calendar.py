#!/usr/bin/env python3
"""
Export Supabase events to Google Calendar
Run this to bulk import your current events
"""

from datetime import datetime
import json
import os

# Import Supabase client
from supabase_client import fetch_records

def fetch_events():
    """Fetch events from Supabase."""
    try:
        records = fetch_records("events", limit=1000)
        print(f"📊 Found {len(records)} records")
        
        # Debug: print first record fields
        if records:
            print(f"\n🔍 Sample record fields: {list(records[0].keys())}")
            print(f"   Sample data: {records[0]}")
        
        return records
    except Exception as e:
        print(f"❌ Error fetching events: {e}")
        return []

def export_to_csv(records, filename="events_export.csv"):
    """Export events to CSV format for Google Calendar import."""
    
    valid_events = []
    
    with open(filename, 'w', encoding='utf-8') as f:
        # Header
        f.write("Subject,Start Date,Start Time,End Date,End Time,All Day Event,Description,Location\n")
        
        for record in records:
            # Try different field name variations
            title = record.get('title') or record.get('Title') or record.get('event_name') or ''
            title = str(title).replace(',', ' ').replace('"', '')
            
            date_start = record.get('date_start') or record.get('Date_Start') or record.get('date') or ''
            time_start = record.get('time_start') or record.get('Time_Start') or record.get('time') or ''
            
            venue = record.get('venue_name') or record.get('Venue_Name') or record.get('venue') or ''
            address = record.get('venue_address') or record.get('Venue_Address') or record.get('address') or ''
            city = record.get('city') or record.get('City') or ''
            
            description = record.get('description') or record.get('Description') or record.get('body') or ''
            description = str(description).replace(',', ' ').replace('"', '').replace('\n', ' ')
            
            organizer = record.get('organizer_name') or record.get('Organizer_Name') or record.get('organizer') or ''
            
            # Skip if no title
            if not title:
                print(f"⚠️ Skipping record with no title: {record.get('id')}")
                continue
            
            valid_events.append(record)
            
            # Parse date
            start_date = ''
            start_time = ''
            end_time = ''
            all_day = 'True'
            
            if date_start:
                try:
                    # Handle ISO format
                    if 'T' in str(date_start):
                        dt = datetime.fromisoformat(str(date_start).replace('Z', '+00:00'))
                        start_date = dt.strftime('%m/%d/%Y')
                        
                        # Parse time
                        if time_start and str(time_start) not in ['TBD', '', 'None']:
                            start_time = str(time_start)
                            all_day = 'False'
                        else:
                            start_time = ''
                            all_day = 'True'
                    else:
                        # Assume MM/DD/YYYY or YYYY-MM-DD
                        start_date = str(date_start)
                except Exception as e:
                    print(f"⚠️ Date parse error for '{title}': {e}")
                    start_date = str(date_start)
            
            # Build location
            location_parts = [p for p in [venue, address, city] if p]
            location = ', '.join(location_parts)
            
            # Build description
            full_description = description
            if organizer:
                full_description += f" Organized by: {organizer}."
            
            # Write CSV row
            f.write(f'"{title}","{start_date}","{start_time}","{start_date}","{end_time}",{all_day},"{full_description}","{location}"\n')
    
    print(f"✅ Exported {len(valid_events)} valid events to {filename}")
    return valid_events

def create_import_instructions():
    """Create instructions for importing to Google Calendar."""
    instructions = """
╔══════════════════════════════════════════════════════════════╗
║           IMPORT EVENTS TO GOOGLE CALENDAR                   ║
╚══════════════════════════════════════════════════════════════╝

1. Go to https://calendar.google.com

2. In the left sidebar, find your calendar "Wilkesboro Community Events"

3. Click the three dots (⋮) next to the calendar name

4. Select "Settings and sharing"

5. Scroll down to "Import & Export"

6. Click "Import"

7. Select the file: events_export.csv

8. Choose your "Wilkesboro Community Events" calendar

9. Click "Import"

✅ All events will appear in your calendar!

═══════════════════════════════════════════════════════════════

TIPS:
- Events with dates will show on the correct day
- Events without specific times are marked as "All day"
- You can edit any event after importing
- The calendar is public and embeddable on your website

═══════════════════════════════════════════════════════════════
"""
    print(instructions)
    
    with open('IMPORT_INSTRUCTIONS.txt', 'w') as f:
        f.write(instructions)
    print("📄 Instructions saved to IMPORT_INSTRUCTIONS.txt")

def main():
    print("="*60)
    print(" Supabase Events → Google Calendar Export")
    print("="*60)
    
    print("\n📥 Fetching events from Supabase...")
    records = fetch_events()
    
    if not records:
        print("❌ No events found")
        return
    
    print(f"\n💾 Exporting to CSV...")
    valid_events = export_to_csv(records)
    
    if valid_events:
        print(f"\n✅ Successfully prepared {len(valid_events)} events for import")
        create_import_instructions()
        
        print("\n" + "="*60)
        print(" NEXT STEPS:")
        print("="*60)
        print("1. Open: https://calendar.google.com")
        print("2. Find your 'Wilkesboro Community Events' calendar")
        print("3. Go to Settings → Import & Export")
        print("4. Upload: events_export.csv")
        print("5. Done! Events will appear in your calendar")
        print("\n📄 See IMPORT_INSTRUCTIONS.txt for detailed steps")
    else:
        print("\n⚠️ No valid events found to export")
        print("Check that your Supabase events table has data in the title and date fields")

if __name__ == "__main__":
    main()
