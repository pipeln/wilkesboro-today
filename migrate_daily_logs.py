#!/usr/bin/env python3
"""
Daily Logs / Activity Markdown Parser
Parses daily log files and migrates to Supabase
"""

import os
import re
import json
from datetime import datetime
from pathlib import Path
from supabase import create_client

SUPABASE_URL = os.environ.get('SUPABASE_URL', 'https://nahldyqwdqnifyljanxt.supabase.co')
SUPABASE_KEY = os.environ.get('SUPABASE_ANON_KEY', '')

def get_supabase():
    if not SUPABASE_KEY:
        raise ValueError("SUPABASE_ANON_KEY not set")
    return create_client(SUPABASE_URL, SUPABASE_KEY)


def parse_daily_log_file(filepath):
    """Parse daily log markdown file."""
    
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()
    
    filename = os.path.basename(filepath)
    
    # Extract date from filename
    date_match = re.search(r'(\d{4}-\d{2}-\d{2})', filename)
    if date_match:
        log_date = date_match.group(1)
    else:
        log_date = datetime.now().strftime('%Y-%m-%d')
    
    data = {
        'activities': [],
        'source_file': filename
    }
    
    # Parse sections
    sections = re.findall(r'##\s*([^\n]+)\s*\n((?:[^#]|\n)+)', content)
    
    for section_name, section_content in sections:
        section_name = section_name.strip()
        section_content = section_content.strip()
        
        activity = {
            'activity_date': log_date,
            'activity_type': categorize_activity(section_name),
            'description': f"{section_name}: {section_content[:500]}",
            'notes': section_content
        }
        
        # Extract files modified
        files_modified = []
        file_pattern = r'`([^`]+\.(?:py|md|sql|json|js|html))`'
        files = re.findall(file_pattern, section_content)
        if files:
            files_modified.extend(files)
        
        # Also look for "created" or "modified" mentions
        created_files = re.findall(r'(?:created|wrote|built)\s+`?([^`\n]+\.(?:py|md|sql))`?', section_content, re.IGNORECASE)
        files_modified.extend(created_files)
        
        if files_modified:
            activity['files_modified'] = list(set(files_modified))[:10]  # Limit to 10
        
        # Extract decisions
        decisions = []
        decision_pattern = r'(?:decided|agreed|chose|will)\s+([^\.\n]+)'
        decision_matches = re.findall(decision_pattern, section_content, re.IGNORECASE)
        if decision_matches:
            decisions = [d.strip() for d in decision_matches[:5]]
            activity['decisions_made'] = decisions
        
        data['activities'].append(activity)
    
    # If no sections found, treat entire content as one activity
    if not data['activities']:
        data['activities'].append({
            'activity_date': log_date,
            'activity_type': 'General',
            'description': content[:500],
            'notes': content
        })
    
    return data


def categorize_activity(section_name):
    """Categorize activity based on section name."""
    name_lower = section_name.lower()
    
    if any(word in name_lower for word in ['research', 'investigation', 'analysis']):
        return 'Research'
    elif any(word in name_lower for word in ['code', 'development', 'build', 'create']):
        return 'Development'
    elif any(word in name_lower for word in ['data', 'migration', 'import', 'export']):
        return 'Data Entry'
    elif any(word in name_lower for word in ['review', 'audit', 'check']):
        return 'Review'
    elif any(word in name_lower for word in ['meeting', 'discussion', 'call']):
        return 'Meeting'
    elif any(word in name_lower for word in ['plan', 'design', 'strategy']):
        return 'Planning'
    else:
        return 'General'


def migrate_to_supabase(data):
    """Migrate parsed activity data to Supabase."""
    
    supabase = get_supabase()
    stats = {'activities': 0, 'errors': 0}
    
    for item in data['activities']:
        try:
            item['source_file'] = data['source_file']
            item['migrated_at'] = datetime.now().isoformat()
            
            supabase.table('activity_logs').insert(item).execute()
            stats['activities'] += 1
        except Exception as e:
            print(f"Error inserting activity: {e}")
            stats['errors'] += 1
    
    return stats


def main():
    print("="*60)
    print("DAILY LOGS MIGRATION TOOL")
    print("="*60)
    
    memory_dir = Path('/root/.openclaw/workspace/memory')
    
    # Find daily log files (YYYY-MM-DD.md format)
    files = [f for f in memory_dir.glob('*.md') if re.match(r'\d{4}-\d{2}-\d{2}\.md', f.name)]
    
    print(f"\nFound {len(files)} daily log files")
    
    total_stats = {'activities': 0, 'errors': 0}
    
    for filepath in files[:1]:  # Test with first file only
        print(f"\nProcessing: {filepath.name}")
        
        try:
            data = parse_daily_log_file(filepath)
            print(f"  Parsed: {len(data['activities'])} activities")
            
            stats = migrate_to_supabase(data)
            
            for key in total_stats:
                total_stats[key] += stats[key]
            
            print(f"  Migrated: Activities: {stats['activities']}, Errors: {stats['errors']}")
            
        except Exception as e:
            print(f"  ERROR: {e}")
            import traceback
            traceback.print_exc()
    
    print("\n" + "="*60)
    print("MIGRATION COMPLETE")
    print("="*60)
    print(f"Total Activities: {total_stats['activities']}")
    print(f"Total Errors: {total_stats['errors']}")


if __name__ == "__main__":
    main()
