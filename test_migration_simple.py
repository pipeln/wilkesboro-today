#!/usr/bin/env python3
"""
Simple test migration - processes just ONE file
"""

import os
import re
from datetime import datetime
from pathlib import Path
from supabase import create_client

SUPABASE_URL = os.environ.get('SUPABASE_URL', 'https://nahldyqwdqnifyljanxt.supabase.co')
SUPABASE_KEY = os.environ.get('SUPABASE_ANON_KEY', '')

def get_supabase():
    if not SUPABASE_KEY:
        raise ValueError("SUPABASE_ANON_KEY not set")
    return create_client(SUPABASE_URL, SUPABASE_KEY)


def main():
    print("="*60)
    print("TEST MIGRATION - SINGLE FILE")
    print("="*60)
    
    # Find just one file
    memory_dir = Path('/root/.openclaw/workspace/memory')
    files = list(memory_dir.glob('*social-monitor*.md'))
    
    if not files:
        print("No files found")
        return
    
    # Take the first file
    filepath = files[0]
    print(f"\nProcessing: {filepath.name}")
    
    # Read file
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()
    
    print(f"File size: {len(content)} characters")
    
    # Simple extraction - just get headlines
    headlines = re.findall(r'\*\*([^*]+)\*\*', content)
    print(f"Found {len(headlines)} headlines")
    
    # Connect to Supabase
    supabase = get_supabase()
    
    # Insert test records (max 5)
    inserted = 0
    for i, headline in enumerate(headlines[:5]):
        try:
            data = {
                'headline': headline.strip()[:200],
                'source': 'Social Monitor Test',
                'published_date': datetime.now().strftime('%Y-%m-%d'),
                'summary': f'Test migration item {i+1}',
                'status': 'New'
            }
            supabase.table('news_items').insert(data).execute()
            inserted += 1
            print(f"  ✓ Inserted: {headline[:50]}...")
        except Exception as e:
            print(f"  ✗ Error: {e}")
    
    print(f"\n{'='*60}")
    print(f"Test complete! Inserted {inserted} records")
    print(f"{'='*60}")


if __name__ == "__main__":
    main()
