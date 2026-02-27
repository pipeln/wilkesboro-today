#!/usr/bin/env python3
"""
Supabase client utility for Wilkes County projects.
Replaces Aitable with Supabase.
"""

import os
from supabase import create_client, Client

# Supabase configuration from environment
SUPABASE_URL = os.environ.get("SUPABASE_URL", "https://nahldyqwdqnifyljanxt.supabase.co")
SUPABASE_KEY = os.environ.get("SUPABASE_KEY", "")

# Table names (matching the Aitable datasheets)
TABLES = {
    "Events": "events",
    "News_Raw": "news_items",
    "Submissions": "submissions",
    "Resources": "resources",
    "Candidates": "candidates",
    "Races": "races",
    "Elections": "elections",
    "Issues": "issues",
    "Positions": "candidate_positions",
}

_supabase_client = None

def get_supabase() -> Client:
    """Get or create Supabase client singleton."""
    global _supabase_client
    if _supabase_client is None:
        if not SUPABASE_KEY:
            raise ValueError("SUPABASE_KEY environment variable not set")
        _supabase_client = create_client(SUPABASE_URL, SUPABASE_KEY)
    return _supabase_client

def get_table_name(aitable_name: str) -> str:
    """Map Aitable datasheet name to Supabase table name."""
    return TABLES.get(aitable_name, aitable_name.lower().replace(" ", "_"))

def fetch_records(table_name: str, filters: dict = None, limit: int = None):
    """Fetch records from Supabase table."""
    supabase = get_supabase()
    query = supabase.table(table_name).select("*")
    
    if filters:
        for key, value in filters.items():
            query = query.eq(key, value)
    
    if limit:
        query = query.limit(limit)
    
    result = query.execute()
    return result.data

def create_record(table_name: str, fields: dict):
    """Create a new record in Supabase table."""
    supabase = get_supabase()
    result = supabase.table(table_name).insert(fields).execute()
    return result.data[0] if result.data else None

def update_record(table_name: str, record_id: str, fields: dict):
    """Update an existing record."""
    supabase = get_supabase()
    result = supabase.table(table_name).update(fields).eq("id", record_id).execute()
    return result.data[0] if result.data else None

def delete_record(table_name: str, record_id: str):
    """Delete a record."""
    supabase = get_supabase()
    result = supabase.table(table_name).delete().eq("id", record_id).execute()
    return result.data
