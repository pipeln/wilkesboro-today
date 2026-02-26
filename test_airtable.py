#!/usr/bin/env python3
import requests
import json

BASE_ID = "dstRRB7Fi8ZVP7eRcS"
TABLE_NAME = "Resources"
TOKEN = "uskNPM9fPVHOgAGbDepyKER"

resources = [
    {"Name": "Town of Wilkesboro", "Type": "Gov_Office", "Website": "townofwilkesboro.com", "Status": "Active", "Audience": "All"},
    {"Name": "Wilkes County Government", "Type": "Gov_Office", "Website": "wilkescounty.net", "Status": "Active", "Audience": "All"},
    {"Name": "North Wilkesboro", "Type": "Gov_Office", "Website": "northwilkesboro.org", "Status": "Active", "Audience": "All"},
    {"Name": "Wilkes County Sheriff", "Type": "Gov_Office", "Website": "wilkescounty.net/151/Sheriff", "Phone": "336-903-7623", "Status": "Active", "Audience": "All"},
    {"Name": "Wilkes County Jail", "Type": "Gov_Office", "Phone": "336-903-7623", "Status": "Active", "Audience": "All"},
    {"Name": "VINE Inmate System", "Type": "Gov_Office", "Phone": "1-877-627-2826", "Status": "Active", "Audience": "All"},
    {"Name": "Journal Patriot", "Type": "Business", "Website": "journalpatriot.com", "Status": "Active", "Audience": "All"},
    {"Name": "The Wilkes Record", "Type": "Business", "Website": "thewilkesrecord.com", "Status": "Active", "Audience": "All"},
    {"Name": "Wilkes County Board of Elections", "Type": "Gov_Office", "Website": "wilkescounty.net/185/Candidates", "Status": "Active", "Audience": "All"},
    {"Name": "NC State Board of Elections", "Type": "Gov_Office", "Website": "ncsbe.gov", "Status": "Active", "Audience": "All"},
    {"Name": "NCWorks Career Center Wilkes", "Type": "Gov_Office", "Status": "Active", "Audience": "All"},
    {"Name": "Goodwill Career Connections", "Type": "Nonprofit", "Address": "1821 US Hwy 421, Wilkesboro", "Status": "Active", "Audience": "All"},
    {"Name": "Wilkes County Jobs", "Type": "Gov_Office", "Website": "wilkescounty.net/Jobs.aspx", "Status": "Active", "Audience": "All"},
    {"Name": "Wilkes EDC", "Type": "Gov_Office", "Website": "wilkesedc.com", "Status": "Active", "Audience": "All"},
    {"Name": "Catherine H. Barber Memorial Shelter", "Type": "Nonprofit", "Phone": "336-838-7120", "Address": "3200 Statesville Rd N", "Status": "Active", "Audience": "All"},
    {"Name": "Wilkes County DSS", "Type": "Gov_Office", "Phone": "336-651-7400", "Status": "Active", "Audience": "All"},
    {"Name": "Wilkes Housing Authority", "Type": "Gov_Office", "Phone": "336-667-8979", "Status": "Active", "Audience": "All"},
    {"Name": "Samaritan Kitchen of Wilkes", "Type": "Nonprofit", "Website": "skwilkes.org", "Status": "Active", "Audience": "All"},
    {"Name": "Wilkes Chamber of Commerce", "Type": "Business", "Website": "wilkeschamber.org", "Status": "Active", "Audience": "All"},
    {"Name": "Wilkes County Schools", "Type": "School", "Website": "wcps.org", "Status": "Active", "Audience": "All"},
]

headers = {
    "Authorization": f"Bearer {TOKEN}",
    "Content-Type": "application/json"
}

# First, try to get the table schema to verify field names
print("Checking base metadata...")
resp = requests.get(f"https://api.airtable.com/v0/meta/bases", headers=headers)
print(f"Bases response: {resp.status_code}")
print(resp.text[:500])

# Try to list tables in the base
print("\nChecking tables in base...")
resp = requests.get(f"https://api.airtable.com/v0/meta/bases/{BASE_ID}/tables", headers=headers)
print(f"Tables response: {resp.status_code}")
print(resp.text[:1000])
