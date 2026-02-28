#!/usr/bin/env python3
"""
Resource Research Markdown Parser
Parses resource research files and migrates to Supabase
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


def parse_resource_file(filepath):
    """Parse resource research markdown file."""
    
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()
    
    filename = os.path.basename(filepath)
    
    data = {
        'resources': [],
        'services': [],
        'source_file': filename
    }
    
    # Parse resources from various formats
    # Format 1: Table rows
    table_pattern = r'\|\s*([^|]+)\s*\|\s*([^|]+)\s*\|\s*([^|]+)\s*\|\s*([^|]+)\s*\|'
    tables = re.findall(table_pattern, content)
    
    for row in tables:
        name, type_, contact, notes = row
        name = name.strip()
        type_ = type_.strip()
        contact = contact.strip()
        notes = notes.strip()
        
        # Skip header rows
        if name.lower() in ['name', 'resource', '---']:
            continue
        
        resource = {
            'name': name,
            'type': type_,
            'description': notes
        }
        
        # Parse contact info
        if 'http' in contact:
            resource['website'] = contact
        elif re.match(r'\d{3}-\d{3}-\d{4}', contact):
            resource['phone'] = contact
        elif '@' in contact:
            resource['email'] = contact
        
        data['resources'].append(resource)
    
    # Format 2: Bullet points with resource info
    bullet_pattern = r'^\s*[-*]\s*\*\*([^:]+):\*\*\s*(.+)$'
    bullets = re.findall(bullet_pattern, content, re.MULTILINE)
    
    for name, details in bullets:
        resource = {
            'name': name.strip(),
            'description': details.strip()
        }
        
        # Try to extract phone numbers
        phone_match = re.search(r'(\d{3}-\d{3}-\d{4})', details)
        if phone_match:
            resource['phone'] = phone_match.group(1)
        
        # Try to extract URLs
        url_match = re.search(r'(https?://[^\s\)]+)', details)
        if url_match:
            resource['website'] = url_match.group(1)
        
        # Try to extract address
        address_match = re.search(r'(\d+[^,]+(?:,[^,]+)?)', details)
        if address_match:
            resource['location'] = address_match.group(1)
        
        data['resources'].append(resource)
    
    # Format 3: Section headers with resources
    section_pattern = r'##\s*([^\n]+)\s*\n((?:\s*[-*]\s*[^\n]+\n?)+)'
    sections = re.findall(section_pattern, content)
    
    for section_name, section_content in sections:
        category = section_name.strip()
        
        for line in section_content.strip().split('\n'):
            line = line.strip().lstrip('-').strip()
            if line and len(line) > 5:
                # Check if it's a resource entry
                if any(keyword in line.lower() for keyword in ['center', 'office', 'department', 'agency', 'services', 'program']):
                    resource = {
                        'name': line.split('-')[0].strip() if '-' in line else line[:100],
                        'category': category,
                        'description': line
                    }
                    
                    # Extract phone
                    phone_match = re.search(r'(\d{3}-\d{3}-\d{4})', line)
                    if phone_match:
                        resource['phone'] = phone_match.group(1)
                    
                    data['resources'].append(resource)
    
    return data


def migrate_to_supabase(data):
    """Migrate parsed resource data to Supabase."""
    
    supabase = get_supabase()
    stats = {'resources': 0, 'services': 0, 'errors': 0}
    
    # Insert resources
    for item in data['resources']:
        try:
            item['source_file'] = data['source_file']
            item['migrated_at'] = datetime.now().isoformat()
            item['status'] = 'Active'
            item['audience'] = 'All'
            
            supabase.table('resources').insert(item).execute()
            stats['resources'] += 1
        except Exception as e:
            print(f"Error inserting resource: {e}")
            stats['errors'] += 1
    
    return stats


def main():
    print("="*60)
    print("RESOURCE RESEARCH MIGRATION TOOL")
    print("="*60)
    
    research_dir = Path('/root/.openclaw/workspace/research')
    files = list(research_dir.glob('*.md'))
    
    # Also check memory folder
    memory_dir = Path('/root/.openclaw/workspace/memory')
    memory_files = list(memory_dir.glob('*resource*.md'))
    files.extend(memory_files)
    
    print(f"\nFound {len(files)} resource files")
    
    total_stats = {'resources': 0, 'services': 0, 'errors': 0}
    
    for filepath in files[:1]:  # Test with first file only
        print(f"\nProcessing: {filepath.name}")
        
        try:
            data = parse_resource_file(filepath)
            print(f"  Parsed: {len(data['resources'])} resources")
            
            stats = migrate_to_supabase(data)
            
            for key in total_stats:
                total_stats[key] += stats[key]
            
            print(f"  Migrated: Resources: {stats['resources']}, Errors: {stats['errors']}")
            
        except Exception as e:
            print(f"  ERROR: {e}")
            import traceback
            traceback.print_exc()
    
    print("\n" + "="*60)
    print("MIGRATION COMPLETE")
    print("="*60)
    print(f"Total Resources: {total_stats['resources']}")
    print(f"Total Errors: {total_stats['errors']}")


if __name__ == "__main__":
    main()
