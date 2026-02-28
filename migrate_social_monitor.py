#!/usr/bin/env python3
"""
Social Monitor Markdown Parser
Parses social monitor reports and migrates data to Supabase
"""

import os
import re
import json
import requests
from datetime import datetime
from pathlib import Path
from supabase import create_client

# Supabase config
SUPABASE_URL = os.environ.get('SUPABASE_URL', 'https://nahldyqwdqnifyljanxt.supabase.co')
SUPABASE_KEY = os.environ.get('SUPABASE_ANON_KEY', '')

def get_supabase():
    if not SUPABASE_KEY:
        raise ValueError("SUPABASE_ANON_KEY not set")
    return create_client(SUPABASE_URL, SUPABASE_KEY)


def parse_date_from_filename(filename):
    """Extract date from filename like '2026-02-28-wilkes-social-monitor.md'"""
    match = re.search(r'(\d{4}-\d{2}-\d{2})', filename)
    if match:
        return match.group(1)
    return datetime.now().strftime('%Y-%m-%d')


def parse_social_monitor_file(filepath):
    """Parse a social monitor markdown file and extract structured data."""
    
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()
    
    filename = os.path.basename(filepath)
    file_date = parse_date_from_filename(filename)
    
    data = {
        'news_items': [],
        'events': [],
        'alerts': [],
        'jobs': [],
        'government_notices': [],
        'source_file': filename
    }
    
    # Extract date from content if available
    date_match = re.search(r'\*\*Date:\*\*\s*([A-Za-z]+ \d{1,2},? \d{4}|\d{4}-\d{2}-\d{2})', content)
    if date_match:
        report_date = date_match.group(1)
    else:
        report_date = file_date
    
    # Parse news items from tables
    # Look for table rows with news items
    table_pattern = r'\|\s*([^|]+)\s*\|\s*([^|]+)\s*\|\s*([^|]+)\s*\|\s*([^|]+)\s*\|'
    tables = re.findall(table_pattern, content)
    
    for row in tables:
        source, community, category, content_snippet = row
        source = source.strip()
        community = community.strip()
        category = category.strip()
        content_snippet = content_snippet.strip()
        
        # Skip header rows
        if source.lower() in ['source', '---'] or 'journal patriot' in source.lower():
            continue
        
        # Determine type based on category
        cat_lower = category.lower()
        
        if 'alert' in cat_lower or 'urgent' in cat_lower:
            data['alerts'].append({
                'title': content_snippet[:200],
                'alert_type': 'Public Safety',
                'severity': 'High' if 'urgent' in cat_lower else 'Medium',
                'community': community,
                'source_name': source,
                'issued_at': report_date,
                'status': 'Active'
            })
        elif 'job' in cat_lower or 'employment' in cat_lower:
            data['jobs'].append({
                'title': content_snippet[:200],
                'employer': source,
                'city': community,
                'posted_date': report_date,
                'status': 'Open'
            })
        elif 'event' in cat_lower:
            data['events'].append({
                'title': content_snippet[:200],
                'city': community,
                'date_start': report_date,
                'category': 'Community',
                'source_name': source
            })
        elif 'government' in cat_lower:
            data['government_notices'].append({
                'title': content_snippet[:200],
                'government_body': source,
                'notice_type': 'Meeting' if 'meeting' in content_snippet.lower() else 'General',
                'source_url': ''
            })
        else:
            # Default to news item
            data['news_items'].append({
                'headline': content_snippet[:300],
                'source_name': source,
                'published_date': report_date,
                'summary': content_snippet,
                'category': category,
                'community': community,
                'county': 'Wilkes' if 'wilkes' in community.lower() else None,
                'status': 'New'
            })
    
    # Also look for bullet points with news items
    bullet_pattern = r'^\s*[-*]\s*\*\*([^:]+):\*\*\s*(.+)$'
    bullets = re.findall(bullet_pattern, content, re.MULTILINE)
    
    for category, content_text in bullets:
        data['news_items'].append({
            'headline': content_text[:300],
            'source_name': 'Social Monitor',
            'published_date': report_date,
            'summary': content_text,
            'category': category.strip(),
            'status': 'New'
        })
    
    return data


def migrate_to_supabase(data):
    """Migrate parsed data to Supabase."""
    
    supabase = get_supabase()
    stats = {'news_items': 0, 'events': 0, 'alerts': 0, 'jobs': 0, 'government_notices': 0, 'errors': 0}
    
    # Insert news items
    for item in data['news_items']:
        try:
            item['source_file'] = data['source_file']
            item['migrated_at'] = datetime.now().isoformat()
            supabase.table('news_items').insert(item).execute()
            stats['news_items'] += 1
        except Exception as e:
            print(f"Error inserting news item: {e}")
            stats['errors'] += 1
    
    # Insert events
    for item in data['events']:
        try:
            item['source_file'] = data['source_file']
            item['migrated_at'] = datetime.now().isoformat()
            supabase.table('events').insert(item).execute()
            stats['events'] += 1
        except Exception as e:
            print(f"Error inserting event: {e}")
            stats['errors'] += 1
    
    # Insert alerts
    for item in data['alerts']:
        try:
            item['source_file'] = data['source_file']
            item['migrated_at'] = datetime.now().isoformat()
            supabase.table('alerts').insert(item).execute()
            stats['alerts'] += 1
        except Exception as e:
            print(f"Error inserting alert: {e}")
            stats['errors'] += 1
    
    # Insert jobs
    for item in data['jobs']:
        try:
            item['source_file'] = data['source_file']
            item['migrated_at'] = datetime.now().isoformat()
            supabase.table('jobs').insert(item).execute()
            stats['jobs'] += 1
        except Exception as e:
            print(f"Error inserting job: {e}")
            stats['errors'] += 1
    
    # Insert government notices
    for item in data['government_notices']:
        try:
            item['source_file'] = data['source_file']
            item['migrated_at'] = datetime.now().isoformat()
            supabase.table('government_notices').insert(item).execute()
            stats['government_notices'] += 1
        except Exception as e:
            print(f"Error inserting notice: {e}")
            stats['errors'] += 1
    
    return stats


def main():
    print("="*60)
    print("SOCIAL MONITOR MIGRATION TOOL")
    print("="*60)
    
    # Find all social monitor files
    memory_dir = Path('/root/.openclaw/workspace/memory')
    files = list(memory_dir.glob('*social-monitor*.md'))
    
    print(f"\nFound {len(files)} social monitor files")
    
    total_stats = {'news_items': 0, 'events': 0, 'alerts': 0, 'jobs': 0, 'government_notices': 0, 'errors': 0}
    
    for filepath in files:
        print(f"\nProcessing: {filepath.name}")
        
        try:
            data = parse_social_monitor_file(filepath)
            stats = migrate_to_supabase(data)
            
            for key in total_stats:
                total_stats[key] += stats[key]
            
            print(f"  News: {stats['news_items']}, Events: {stats['events']}, Alerts: {stats['alerts']}, Jobs: {stats['jobs']}, Notices: {stats['government_notices']}, Errors: {stats['errors']}")
            
        except Exception as e:
            print(f"  ERROR: {e}")
    
    print("\n" + "="*60)
    print("MIGRATION COMPLETE")
    print("="*60)
    print(f"Total News Items: {total_stats['news_items']}")
    print(f"Total Events: {total_stats['events']}")
    print(f"Total Alerts: {total_stats['alerts']}")
    print(f"Total Jobs: {total_stats['jobs']}")
    print(f"Total Notices: {total_stats['government_notices']}")
    print(f"Total Errors: {total_stats['errors']}")


if __name__ == "__main__":
    main()
