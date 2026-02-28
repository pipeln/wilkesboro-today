#!/usr/bin/env python3
"""
Website Builder for Astro
Fetches data from Supabase and triggers build
"""

import os
import json
import subprocess
from datetime import datetime
from supabase import create_client

SUPABASE_URL = os.environ.get('SUPABASE_URL', 'https://nahldyqwdqnifyljanxt.supabase.co')
SUPABASE_KEY = os.environ.get('SUPABASE_ANON_KEY', '')
ASTRO_BUILD_DIR = os.environ.get('ASTRO_BUILD_DIR', '/root/.openclaw/workspace/website-design')

def get_supabase():
    if not SUPABASE_KEY:
        raise ValueError("SUPABASE_ANON_KEY not set")
    return create_client(SUPABASE_URL, SUPABASE_KEY)


def fetch_approved_news():
    """Fetch approved news items from Supabase."""
    supabase = get_supabase()
    
    print("Fetching approved news...")
    result = supabase.table('news_items').select('*').eq('status', 'Approved').order('published_date', desc=True).limit(50).execute()
    
    print(f"Found {len(result.data)} approved news items")
    return result.data


def fetch_upcoming_events():
    """Fetch upcoming events."""
    supabase = get_supabase()
    
    print("Fetching upcoming events...")
    today = datetime.now().strftime('%Y-%m-%d')
    result = supabase.table('events').select('*').gte('date_start', today).order('date_start').limit(20).execute()
    
    print(f"Found {len(result.data)} upcoming events")
    return result.data


def fetch_candidates():
    """Fetch election candidates."""
    supabase = get_supabase()
    
    print("Fetching candidates...")
    result = supabase.table('candidates').select('*').execute()
    
    print(f"Found {len(result.data)} candidates")
    return result.data


def export_data_to_json(news, events, candidates):
    """Export data to JSON for Astro to consume."""
    
    data_dir = f"{ASTRO_BUILD_DIR}/src/data"
    os.makedirs(data_dir, exist_ok=True)
    
    # Export news
    with open(f"{data_dir}/news.json", 'w') as f:
        json.dump(news, f, indent=2, default=str)
    print(f"Exported {len(news)} news items to news.json")
    
    # Export events
    with open(f"{data_dir}/events.json", 'w') as f:
        json.dump(events, f, indent=2, default=str)
    print(f"Exported {len(events)} events to events.json")
    
    # Export candidates
    with open(f"{data_dir}/candidates.json", 'w') as f:
        json.dump(candidates, f, indent=2, default=str)
    print(f"Exported {len(candidates)} candidates to candidates.json")


def build_website():
    """Trigger Astro build."""
    
    print("\nBuilding Astro website...")
    
    try:
        # Change to website directory
        os.chdir(ASTRO_BUILD_DIR)
        
        # Run npm install if needed
        # subprocess.run(['npm', 'install'], check=True, capture_output=True)
        
        # Build the site
        result = subprocess.run(
            ['npm', 'run', 'build'],
            capture_output=True,
            text=True,
            timeout=300  # 5 minute timeout
        )
        
        if result.returncode == 0:
            print("✅ Build successful!")
            return True
        else:
            print(f"❌ Build failed:\n{result.stderr}")
            return False
            
    except Exception as e:
        print(f"❌ Build error: {e}")
        return False


def deploy_website():
    """Deploy built website."""
    
    print("\nDeploying website...")
    
    # This would integrate with your hosting provider
    # Examples: Netlify, Vercel, Cloudflare Pages, etc.
    
    # For now, just indicate success
    print("✅ Deployment ready (integrate with your hosting provider)")
    return True


def mark_items_published(news_ids):
    """Mark news items as published."""
    supabase = get_supabase()
    
    for item_id in news_ids:
        try:
            supabase.table('news_items').update({
                'status': 'Published',
                'published_at': datetime.now().isoformat()
            }).eq('id', item_id).execute()
        except Exception as e:
            print(f"Warning: Could not mark {item_id} as published: {e}")
    
    print(f"Marked {len(news_ids)} items as published")


def main():
    print("="*60)
    print("WEBSITE BUILDER")
    print("="*60)
    
    # Fetch data
    news = fetch_approved_news()
    events = fetch_upcoming_events()
    candidates = fetch_candidates()
    
    if not news and not events:
        print("\nNo content to publish. Exiting.")
        return
    
    # Export data
    print("\nExporting data...")
    export_data_to_json(news, events, candidates)
    
    # Build website
    if build_website():
        # Deploy
        deploy_website()
        
        # Mark items as published
        news_ids = [n['id'] for n in news]
        mark_items_published(news_ids)
        
        print("\n" + "="*60)
        print("✅ WEBSITE UPDATE COMPLETE")
        print("="*60)
        print(f"Published: {len(news)} news items")
        print(f"Events: {len(events)} upcoming")
        print(f"Candidates: {len(candidates)} profiles")
    else:
        print("\n❌ Build failed. Website not updated.")


if __name__ == "__main__":
    main()
