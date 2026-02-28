#!/usr/bin/env python3
"""
Database Cleanup Script
Removes test data and standardizes records
"""

import os
from datetime import datetime
from supabase import create_client

SUPABASE_URL = os.environ.get('SUPABASE_URL', 'https://nahldyqwdqnifyljanxt.supabase.co')
SUPABASE_KEY = os.environ.get('SUPABASE_ANON_KEY', '')

def get_supabase():
    if not SUPABASE_KEY:
        raise ValueError("SUPABASE_ANON_KEY not set")
    return create_client(SUPABASE_URL, SUPABASE_KEY)


def cleanup_news_items():
    """Clean up news_items table."""
    supabase = get_supabase()
    
    print("="*60)
    print("DATABASE CLEANUP")
    print("="*60)
    
    # Get initial count
    result = supabase.table('news_items').select('count', count='exact').execute()
    initial_count = result.count
    print(f"\nInitial news_items count: {initial_count}")
    
    # Delete test records
    print("\n1. Removing test records...")
    
    # Delete items with 'test' in headline (case insensitive)
    result = supabase.table('news_items').delete().ilike('headline', '%test%').execute()
    print(f"   Removed test headlines")
    
    # Delete items with system/generic headlines
    generic_patterns = [
        'Date:', 'Source:', 'Classification:', '---',
        'Coverage Area:', 'Community:', 'Headline:',
        'Executive Summary', 'Items Found:', 'Urgent Alerts'
    ]
    
    for pattern in generic_patterns:
        try:
            result = supabase.table('news_items').delete().ilike('headline', f'{pattern}%').execute()
        except:
            pass
    print(f"   Removed generic/system headers")
    
    # Delete items with very short headlines (less than 20 chars)
    # This requires fetching and deleting individually
    result = supabase.table('news_items').select('id, headline').execute()
    short_ids = [r['id'] for r in result.data if len(r.get('headline', '')) < 20]
    
    for item_id in short_ids:
        try:
            supabase.table('news_items').delete().eq('id', item_id).execute()
        except:
            pass
    print(f"   Removed {len(short_ids)} short headlines")
    
    # Delete items with no meaningful source
    result = supabase.table('news_items').delete().eq('source', 'System').execute()
    print(f"   Removed system-generated items")
    
    # Standardize categories
    print("\n2. Standardizing data...")
    
    # Set default category
    result = supabase.table('news_items').update({'category': 'News'}).is_('category', 'null').execute()
    print(f"   Set default categories")
    
    # Set county based on community
    communities_wilkes = ['Wilkesboro', 'North Wilkesboro', 'Wilkes County', 'Hays', 'Millers Creek']
    for community in communities_wilkes:
        result = supabase.table('news_items').update({'county': 'Wilkes'}).ilike('community', f'%{community}%').execute()
    print(f"   Standardized counties")
    
    # Set status for items without one
    result = supabase.table('news_items').update({'status': 'New'}).is_('status', 'null').execute()
    print(f"   Set default status")
    
    # Get final count
    result = supabase.table('news_items').select('count', count='exact').execute()
    final_count = result.count
    
    print(f"\n" + "="*60)
    print("CLEANUP COMPLETE")
    print("="*60)
    print(f"Removed: {initial_count - final_count} records")
    print(f"Remaining: {final_count} records")
    
    return initial_count - final_count, final_count


def show_sample_data():
    """Show sample of remaining data."""
    supabase = get_supabase()
    
    print("\n" + "="*60)
    print("SAMPLE REMAINING RECORDS")
    print("="*60)
    
    result = supabase.table('news_items').select('headline, source, category, county').limit(10).execute()
    
    for i, item in enumerate(result.data, 1):
        print(f"\n{i}. {item['headline'][:60]}...")
        print(f"   Source: {item.get('source', 'N/A')}")
        print(f"   Category: {item.get('category', 'N/A')}")
        print(f"   County: {item.get('county', 'N/A')}")


def main():
    print("\n⚠️  This will clean test and invalid data from the database.")
    print("Press Ctrl+C to cancel, or wait 3 seconds to proceed...")
    
    try:
        import time
        time.sleep(3)
    except KeyboardInterrupt:
        print("\nCancelled.")
        return
    
    removed, remaining = cleanup_news_items()
    show_sample_data()
    
    print(f"\n✅ Cleanup complete! Removed {removed} records, {remaining} remain.")


if __name__ == "__main__":
    main()
