#!/usr/bin/env python3
"""
Script to add Wilkes County resources to AITable Resources datasheet.
Uses AITable REST API (fusion/v1).
"""

import requests
import json

# Configuration
API_TOKEN = "uskNPM9fPVHOgAGbDepyKER"
BASE_URL = "https://api.aitable.ai/fusion/v1"
HEADERS = {
    "Authorization": f"Bearer {API_TOKEN}",
    "Content-Type": "application/json"
}

# Datasheet ID
RESOURCES_DATASHEET_ID = "dstRRB7Fi8ZVP7eRcS"

# Resources to add - with proper field mapping for AITable
RESOURCES_DATA = [
    # Local Government
    {"Name": "Town of Wilkesboro", "Website": "https://townofwilkesboro.com", "Type": "Gov_Office", "Status": "Active", "Audience": ["All"], "County": "Wilkes", "City": "Wilkesboro"},
    {"Name": "Wilkes County Government", "Website": "https://wilkescounty.net", "Type": "Gov_Office", "Status": "Active", "Audience": ["All"], "County": "Wilkes", "City": "Wilkesboro"},
    {"Name": "North Wilkesboro", "Website": "https://northwilkesboro.org", "Type": "Gov_Office", "Status": "Active", "Audience": ["All"], "County": "Wilkes", "City": "North Wilkesboro"},
    {"Name": "Wilkes County Sheriff", "Website": "https://wilkescounty.net/151/Sheriff", "Type": "Gov_Office", "Status": "Active", "Audience": ["All"], "County": "Wilkes", "City": "Wilkesboro", "Topics": ["Emergency"]},
    {"Name": "Wilkes County Jail", "Phone": "336-903-7623", "Type": "Gov_Office", "Status": "Active", "Audience": ["All"], "County": "Wilkes", "City": "Wilkesboro"},
    {"Name": "VINE Inmate System", "Phone": "1-877-627-2826", "Type": "Gov_Office", "Status": "Active", "Audience": ["All"], "County": "Wilkes", "Topics": ["Legal"]},
    
    # Local News
    {"Name": "Journal Patriot", "Website": "https://journalpatriot.com", "Type": "Business", "Status": "Active", "Audience": ["All"], "County": "Wilkes"},
    {"Name": "The Wilkes Record", "Website": "https://thewilkesrecord.com", "Type": "Business", "Status": "Active", "Audience": ["All"], "County": "Wilkes"},
    
    # Elections
    {"Name": "Wilkes County Board of Elections", "Website": "https://wilkescounty.net/185/Candidates", "Type": "Gov_Office", "Status": "Active", "Audience": ["All"], "County": "Wilkes", "City": "Wilkesboro"},
    {"Name": "NC State Board of Elections", "Website": "https://ncsbe.gov", "Type": "Gov_Office", "Status": "Active", "Audience": ["All"], "County": "Wilkes"},
    
    # Jobs & Employment
    {"Name": "NCWorks Career Center Wilkes", "Address": "Wilkesboro location", "Type": "Gov_Office", "Status": "Active", "Audience": ["All"], "County": "Wilkes", "City": "Wilkesboro", "Topics": ["Jobs"]},
    {"Name": "Goodwill Career Connections", "Address": "1821 US Hwy 421, Wilkesboro", "Type": "Nonprofit", "Status": "Active", "Audience": ["All"], "County": "Wilkes", "City": "Wilkesboro", "Topics": ["Jobs"]},
    {"Name": "Wilkes County Jobs", "Website": "https://wilkescounty.net/Jobs.aspx", "Type": "Gov_Office", "Status": "Active", "Audience": ["All"], "County": "Wilkes", "City": "Wilkesboro", "Topics": ["Jobs"]},
    {"Name": "Wilkes EDC", "Website": "https://wilkesedc.com", "Type": "Gov_Office", "Status": "Active", "Audience": ["All"], "County": "Wilkes", "Topics": ["Jobs"]},
    
    # Homeless & Housing
    {"Name": "Catherine H. Barber Memorial Shelter", "Phone": "336-838-7120", "Address": "3200 Statesville Rd N", "Type": "Nonprofit", "Status": "Active", "Audience": ["All"], "County": "Wilkes", "City": "North Wilkesboro", "Topics": ["Housing"]},
    {"Name": "Wilkes County DSS", "Phone": "336-651-7400", "Address": "PO Box 119", "Type": "Gov_Office", "Status": "Active", "Audience": ["All"], "County": "Wilkes", "City": "Wilkesboro", "Topics": ["Housing"]},
    {"Name": "Wilkes Housing Authority", "Phone": "336-667-8979", "Type": "Gov_Office", "Status": "Active", "Audience": ["All"], "County": "Wilkes", "City": "Wilkesboro", "Topics": ["Housing"]},
    {"Name": "Wilkes Housing and Outreach Center", "Website": "https://highcountrywdb.com", "Type": "Nonprofit", "Status": "Active", "Audience": ["All"], "County": "Wilkes", "Topics": ["Housing"]},
    {"Name": "Care Connection", "Phone": "336-667-2273", "Type": "Health", "Status": "Active", "Audience": ["All"], "County": "Wilkes", "Topics": ["Health"]},
    
    # Food & Meals
    {"Name": "Samaritan Kitchen of Wilkes", "Website": "https://skwilkes.org", "Type": "Nonprofit", "Status": "Active", "Audience": ["All"], "County": "Wilkes", "City": "Wilkesboro", "Topics": ["Food"], "Hours": "Evening meals 5pm"},
    {"Name": "Meals on Wheels of Wilkes County", "Type": "Nonprofit", "Status": "Active", "Audience": ["Seniors"], "County": "Wilkes", "Topics": ["Food"]},
    {"Name": "Wilkes FaithHealth Crisis Assistance", "Short_Description": "Emergency food/rent/utilities", "Type": "Nonprofit", "Status": "Active", "Audience": ["All"], "County": "Wilkes", "Topics": ["Food", "Housing"]},
    {"Name": "Blessing Boxes/Pantries", "Website": "https://wilcoresources.org", "Type": "Nonprofit", "Status": "Active", "Audience": ["All"], "County": "Wilkes", "Topics": ["Food"]},
    
    # Community
    {"Name": "Wilkes Chamber of Commerce", "Website": "https://wilkeschamber.org", "Type": "Business", "Status": "Active", "Audience": ["All"], "County": "Wilkes"},
    {"Name": "Wilkes County Schools", "Website": "https://wcps.org", "Type": "School", "Status": "Active", "Audience": ["Families", "Students"], "County": "Wilkes", "Topics": ["Education"]},
    
    # 24/7 Hotlines
    {"Name": "NC United Way", "Phone": "211", "Type": "Nonprofit", "Status": "Active", "Audience": ["All"], "County": "Wilkes", "Topics": ["Emergency"]},
    {"Name": "VINE (Victim Info)", "Phone": "1-877-627-2826", "Type": "Gov_Office", "Status": "Active", "Audience": ["All"], "County": "Wilkes", "Topics": ["Legal"]},
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
        if hasattr(e, 'response') and e.response:
            print(f"Response: {e.response.text}")
        return None


def main():
    print("Adding Wilkes County resources to Resources datasheet...")
    print(f"Total resources to add: {len(RESOURCES_DATA)}")
    print()
    
    # Add records in batches of 10 (API limit)
    batch_size = 10
    total_added = 0
    failed_batches = []
    
    for i in range(0, len(RESOURCES_DATA), batch_size):
        batch = RESOURCES_DATA[i:i+batch_size]
        batch_num = i // batch_size + 1
        
        print(f"Adding batch {batch_num} ({len(batch)} records)...")
        result = create_records(RESOURCES_DATASHEET_ID, batch)
        
        if result and result.get("success"):
            added = len(result.get("data", {}).get("records", []))
            total_added += added
            print(f"  ✓ Added {added} records")
        else:
            print(f"  ✗ Failed to add batch {batch_num}")
            if result:
                print(f"    Error: {result.get('message', 'Unknown error')}")
            failed_batches.append(batch_num)
    
    print()
    print("="*50)
    print("SUMMARY")
    print("="*50)
    print(f"Total resources to add: {len(RESOURCES_DATA)}")
    print(f"Successfully added: {total_added}")
    print(f"Failed batches: {failed_batches if failed_batches else 'None'}")
    print("="*50)
    
    return total_added


if __name__ == "__main__":
    main()
