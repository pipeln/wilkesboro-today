#!/usr/bin/env python3
"""
Script to populate Wilkesboro AITable datasheets with collected data.
Uses AITable REST API v1.
"""

import requests
import json
import sys

# Configuration
API_TOKEN = "uskNPM9fPVHOgAGbDepyKER"
BASE_URL = "https://aitable.ai/api/v1"
HEADERS = {
    "Authorization": f"Bearer {API_TOKEN}",
    "Content-Type": "application/json"
}

# Datasheet IDs
DATASHEETS = {
    "News_Raw": "dstjSJ3rvilwBd3Bae",
    "Events": "dstnnbs9qm9DZJkt8L",
    "Resources": "dstRRB7Fi8ZVP7eRcS",
    "Editorial_Tasks": "dstGEMKDzVQ5gBL9J1"
}

# Data to add
NEWS_RAW_DATA = [
    {"Title": "Superintendent Mark Byrd death", "Source": "Journal Patriot", "Date": "2026-02-20", "Category": "Schools", "Status": "New"},
    {"Title": "Murder charge in Brushies shooting", "Source": "Local news", "Date": "2026-02-24", "Category": "Public Safety", "Status": "New"},
    {"Title": "GOP commissioner candidates filing", "Source": "Local news", "Date": "2026-02-24", "Category": "Politics", "Status": "New"},
    {"Title": "Rising student homelessness", "Source": "Local news", "Date": "2026-02-24", "Category": "Schools", "Status": "New"},
    {"Title": "State of Emergency terminated (Winter Storm Fern)", "Source": "County Government", "Date": "2026-02-09", "Category": "Government", "Status": "New"},
    {"Title": "County Commissioner meeting rescheduled to March 5", "Source": "County Government", "Date": "2026-02-24", "Category": "Government", "Status": "New"},
    {"Title": "Public hearing for County Office Building", "Source": "County Government", "Date": "2026-02-24", "Category": "Government", "Status": "New"},
    {"Title": "Wilkes Record school delay notice", "Source": "The Wilkes Record", "Date": "2026-02-24", "Category": "Schools", "Status": "New"},
    {"Title": "Legislative update from Rep. Blair Eddins", "Source": "NC Legislature", "Date": "2026-02-24", "Category": "Politics", "Status": "New"}
]

EVENTS_DATA = [
    {"Event_Name": "Wilkesboro Planning Board Meeting", "Date": "2026-02-24", "Time": "5:15 PM", "Location": "Wilkesboro", "Status": "New"},
    {"Event_Name": "Board of Elections Meeting", "Date": "2026-02-24", "Time": "5:00 PM", "Location": "Wilkesboro", "Status": "New"},
    {"Event_Name": "County Commissioners Meeting (rescheduled)", "Date": "2026-03-05", "Time": "TBD", "Location": "Wilkesboro", "Status": "New"}
]

RESOURCES_DATA = [
    {"Name": "Catherine H. Barber Memorial Shelter", "Phone": "336-838-7120", "Address": "3200 Statesville Rd N, North Wilkesboro", "Type": "Emergency Shelter", "Status": "New"},
    {"Name": "Wilkes County DSS", "Phone": "336-651-7400", "Address": "PO Box 119, Wilkesboro", "Type": "Social Services", "Status": "New"},
    {"Name": "Wilkes Housing Authority", "Phone": "336-667-8979", "Address": "Wilkesboro, NC", "Type": "Housing Assistance", "Status": "New"},
    {"Name": "Care Connection", "Phone": "336-667-2273", "Address": "Wilkes County", "Type": "Community Services", "Status": "New"},
    {"Name": "Samaritan Kitchen of Wilkes", "Phone": "", "Address": "Wilkesboro", "Type": "Food/Meals", "Notes": "Evening meals 5pm", "Status": "New"},
    {"Name": "Meals on Wheels of Wilkes County", "Phone": "", "Address": "Wilkes County", "Type": "Food/Meals", "Notes": "Home delivery for seniors", "Status": "New"},
    {"Name": "NC United Way", "Phone": "211", "Address": "North Carolina", "Type": "Hotline", "Status": "New"}
]

EDITORIAL_TASKS_DATA = [
    {"Task": "Summarize news from Journal Patriot about superintendent", "Priority": "High", "Due_Date": "2026-02-25", "Category": "News Summary", "Status": "New"},
    {"Task": "Create event listings for Feb 24 and March 5 meetings", "Priority": "High", "Due_Date": "2026-02-24", "Category": "Events", "Status": "New"},
    {"Task": "Verify Resources entries", "Priority": "Medium", "Due_Date": "2026-02-26", "Category": "Verification", "Status": "New"},
    {"Task": "Build newsletter digest", "Priority": "High", "Due_Date": "2026-02-25", "Category": "Newsletter", "Status": "New"}
]


def create_records(datasheet_id, records):
    """Create records in a datasheet."""
    url = f"{BASE_URL}/datasheets/{datasheet_id}/records"
    
    # Format records for AITable API
    payload = {
        "records": [{"fields": record} for record in records]
    }
    
    try:
        response = requests.post(url, headers=HEADERS, json=payload)
        response.raise_for_status()
        return response.json()
    except requests.exceptions.RequestException as e:
        print(f"Error creating records: {e}")
        if hasattr(e.response, 'text'):
            print(f"Response: {e.response.text}")
        return None


def main():
    results = {}
    
    # Add News_Raw records
    print("Adding News_Raw records...")
    result = create_records(DATASHEETS["News_Raw"], NEWS_RAW_DATA)
    if result:
        results["News_Raw"] = len(NEWS_RAW_DATA)
        print(f"  ✓ Added {len(NEWS_RAW_DATA)} records")
    else:
        results["News_Raw"] = 0
        print("  ✗ Failed to add records")
    
    # Add Events records
    print("Adding Events records...")
    result = create_records(DATASHEETS["Events"], EVENTS_DATA)
    if result:
        results["Events"] = len(EVENTS_DATA)
        print(f"  ✓ Added {len(EVENTS_DATA)} records")
    else:
        results["Events"] = 0
        print("  ✗ Failed to add records")
    
    # Add Resources records
    print("Adding Resources records...")
    result = create_records(DATASHEETS["Resources"], RESOURCES_DATA)
    if result:
        results["Resources"] = len(RESOURCES_DATA)
        print(f"  ✓ Added {len(RESOURCES_DATA)} records")
    else:
        results["Resources"] = 0
        print("  ✗ Failed to add records")
    
    # Add Editorial_Tasks records
    print("Adding Editorial_Tasks records...")
    result = create_records(DATASHEETS["Editorial_Tasks"], EDITORIAL_TASKS_DATA)
    if result:
        results["Editorial_Tasks"] = len(EDITORIAL_TASKS_DATA)
        print(f"  ✓ Added {len(EDITORIAL_TASKS_DATA)} records")
    else:
        results["Editorial_Tasks"] = 0
        print("  ✗ Failed to add records")
    
    # Print summary
    print("\n" + "="*50)
    print("SUMMARY - Records Added")
    print("="*50)
    total = 0
    for datasheet, count in results.items():
        print(f"  {datasheet}: {count}")
        total += count
    print("-"*50)
    print(f"  TOTAL: {total}")
    print("="*50)
    
    return results


if __name__ == "__main__":
    main()
