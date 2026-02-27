#!/usr/bin/env python3
"""
Test Supabase connection and operations
"""

import os
from supabase_client import get_supabase, fetch_records, create_record

def test_connection():
    """Test Supabase connection."""
    print("Testing Supabase connection...")
    try:
        supabase = get_supabase()
        print("✓ Connected to Supabase")
        return True
    except Exception as e:
        print(f"✗ Connection failed: {e}")
        return False

def test_fetch():
    """Test fetching records."""
    print("\nTesting fetch operations...")
    try:
        # Test fetching from elections table
        records = fetch_records("elections", limit=5)
        print(f"✓ Fetched {len(records)} elections")
        
        # Test fetching from candidates table
        records = fetch_records("candidates", limit=5)
        print(f"✓ Fetched {len(records)} candidates")
        
        return True
    except Exception as e:
        print(f"✗ Fetch failed: {e}")
        return False

def main():
    print("="*60)
    print("SUPABASE CONNECTION TEST")
    print("="*60)
    
    if not test_connection():
        print("\n✗ Connection test failed. Check your SUPABASE_KEY environment variable.")
        return
    
    test_fetch()
    
    print("\n" + "="*60)
    print("Test complete!")
    print("="*60)

if __name__ == "__main__":
    main()
