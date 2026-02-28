#!/usr/bin/env python3
"""
Fast Database Cleanup - Essential only
"""

import os
from supabase import create_client

SUPABASE_URL = os.environ.get('SUPABASE_URL', 'https://nahldyqwdqnifyljanxt.supabase.co')
SUPABASE_KEY = os.environ.get('SUPABASE_ANON_KEY', '')

def get_supabase():
    return create_client(SUPABASE_URL, SUPABASE_KEY)

def main():
    print("="*60)
    print("FAST DATABASE CLEANUP")
    print("="*60)
    
    supabase = get_supabase()
    
    # Get count
    result = supabase.table('news_items').select('count', count='exact').execute()
    print(f"Total records: {result.count}")
    
    # Just standardize - don't delete (faster)
    print("\nStandardizing data...")
    
    # Update null categories
    try:
        supabase.table('news_items').update({'category': 'News'}).is_('category', 'null').execute()
        print("✓ Categories set")
    except Exception as e:
        print(f"Note: {e}")
    
    # Update null status
    try:
        supabase.table('news_items').update({'status': 'New'}).is_('status', 'null').execute()
        print("✓ Status set")
    except Exception as e:
        print(f"Note: {e}")
    
    print("\n✅ Cleanup complete!")

if __name__ == "__main__":
    main()
