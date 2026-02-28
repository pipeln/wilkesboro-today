#!/usr/bin/env python3
"""
Cloudflare Pages Deployment Script
Exports data from Supabase and triggers Cloudflare deployment
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
    return create_client(SUPABASE_URL, SUPABASE_KEY)


def fetch_approved_content():
    """Fetch all approved content from Supabase."""
    supabase = get_supabase()
    
    print("Fetching approved content...")
    
    # Approved news
    news = supabase.table('news_items').select('*').eq('status', 'Approved').order('published_date', desc=True).limit(50).execute()
    print(f"  ✓ {len(news.data)} news articles")
    
    # Upcoming events
    today = datetime.now().strftime('%Y-%m-%d')
    events = supabase.table('events').select('*').gte('date_start', today).order('date_start').limit(20).execute()
    print(f"  ✓ {len(events.data)} upcoming events")
    
    # Candidates
    candidates = supabase.table('candidates').select('*').execute()
    print(f"  ✓ {len(candidates.data)} candidates")
    
    # Jobs
    jobs = supabase.table('jobs').select('*').eq('status', 'active').order('posted_date', desc=True).limit(20).execute()
    print(f"  ✓ {len(jobs.data)} jobs")
    
    # Resources
    resources = supabase.table('resources').select('*').execute()
    print(f"  ✓ {len(resources.data)} resources")
    
    return {
        'news': news.data,
        'events': events.data,
        'candidates': candidates.data,
        'jobs': jobs.data,
        'resources': resources.data,
        'last_updated': datetime.now().isoformat()
    }


def export_to_json(data):
    """Export data to JSON files for Astro."""
    
    data_dir = f"{ASTRO_BUILD_DIR}/src/data"
    os.makedirs(data_dir, exist_ok=True)
    
    # Export each data type
    for key, value in data.items():
        if key != 'last_updated':
            filepath = f"{data_dir}/{key}.json"
            with open(filepath, 'w') as f:
                json.dump(value, f, indent=2, default=str)
            print(f"  ✓ Exported {key}.json ({len(value)} items)")
    
    # Export metadata
    metadata = {
        'last_updated': data['last_updated'],
        'counts': {k: len(v) for k, v in data.items() if k != 'last_updated'}
    }
    with open(f"{data_dir}/metadata.json", 'w') as f:
        json.dump(metadata, f, indent=2)
    print(f"  ✓ Exported metadata.json")


def build_and_deploy():
    """Build Astro site and deploy to Cloudflare."""
    
    print("\nBuilding Astro site...")
    
    try:
        os.chdir(ASTRO_BUILD_DIR)
        
        # Build the site
        result = subprocess.run(
            ['npm', 'run', 'build'],
            capture_output=True,
            text=True,
            timeout=300
        )
        
        if result.returncode != 0:
            print(f"❌ Build failed:\n{result.stderr}")
            return False
        
        print("✅ Build successful!")
        
        # Cloudflare Pages automatically deploys from git
        # We need to commit and push the new data files
        print("\nCommitting data files to git...")
        
        subprocess.run(['git', 'add', 'src/data/'], check=True, capture_output=True)
        
        commit_result = subprocess.run(
            ['git', 'commit', '-m', f'Update content: {datetime.now().strftime("%Y-%m-%d %H:%M")}'],
            capture_output=True,
            text=True
        )
        
        if commit_result.returncode == 0:
            print("✅ Changes committed")
            
            # Push to trigger Cloudflare deployment
            push_result = subprocess.run(
                ['git', 'push', 'origin', 'main'],
                capture_output=True,
                text=True
            )
            
            if push_result.returncode == 0:
                print("✅ Pushed to origin - Cloudflare deployment triggered!")
                return True
            else:
                print(f"⚠️ Push failed: {push_result.stderr}")
                return False
        else:
            print("ℹ️ No changes to commit")
            return True
            
    except Exception as e:
        print(f"❌ Error: {e}")
        return False


def mark_items_published(news_ids):
    """Mark news items as published."""
    supabase = get_supabase()
    
    for item_id in news_ids:
        try:
            supabase.table('news_items').update({
                'status': 'Published',
                'published_at': datetime.now().isoformat()
            }).eq('id', item_id).execute()
        except:
            pass
    
    print(f"\n✅ Marked {len(news_ids)} items as published")


def main():
    print("="*60)
    print("CLOUDFLARE PAGES DEPLOYMENT")
    print("="*60)
    print(f"Time: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print(f"Site: https://3e7b83d8.wilkesboro-today.pages.dev/")
    print()
    
    # Fetch data
    data = fetch_approved_content()
    
    if not data['news'] and not data['events']:
        print("\nNo approved content to publish.")
        return
    
    # Export data
    print("\nExporting data...")
    export_to_json(data)
    
    # Build and deploy
    if build_and_deploy():
        # Mark items as published
        news_ids = [n['id'] for n in data['news']]
        mark_items_published(news_ids)
        
        print("\n" + "="*60)
        print("✅ DEPLOYMENT COMPLETE")
        print("="*60)
        print(f"Published: {len(data['news'])} news items")
        print(f"Events: {len(data['events'])} upcoming")
        print(f"Jobs: {len(data['jobs'])} active")
        print(f"\nLive at: https://3e7b83d8.wilkesboro-today.pages.dev/")
    else:
        print("\n❌ Deployment failed.")


if __name__ == "__main__":
    main()
