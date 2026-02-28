#!/usr/bin/env python3
"""
Election Research Markdown Parser
Parses election research reports and migrates to Supabase
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


def parse_election_research_file(filepath):
    """Parse election research markdown file."""
    
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()
    
    filename = os.path.basename(filepath)
    
    data = {
        'candidates': [],
        'races': [],
        'elections': [],
        'issues': [],
        'positions': [],
        'source_file': filename
    }
    
    # Extract election date
    election_match = re.search(r'\*\*Election Date:\*\*\s*([A-Za-z]+ \d{1,2},? \d{4})', content)
    election_date = None
    if election_match:
        date_str = election_match.group(1)
        try:
            election_date = datetime.strptime(date_str, '%B %d, %Y').strftime('%Y-%m-%d')
        except:
            pass
    
    # Parse candidates from tables or sections
    # Look for candidate sections
    candidate_sections = re.findall(
        r'\*\*([^*]+)\*\*\s*\(([^)]+)\)\s*-\s*([^\n]+)(?:\n|\r\n?)((?:\s*-\s*[^\n]+\n?)+)',
        content
    )
    
    for name, role, summary, details in candidate_sections:
        candidate = {
            'full_name': name.strip(),
            'occupation': role.strip(),
            'biography': summary.strip(),
            'party': 'Unknown',
            'incumbent': 'incumbent' in content.lower() and name.lower() in content.lower()
        }
        
        # Parse details
        for line in details.strip().split('\n'):
            line = line.strip().lstrip('-').strip()
            if 'education' in line.lower():
                candidate['education'] = line.split(':', 1)[1].strip() if ':' in line else line
            elif 'background' in line.lower():
                candidate['biography'] += ' ' + (line.split(':', 1)[1].strip() if ':' in line else line)
            elif 'email' in line.lower():
                candidate['email'] = line.split(':', 1)[1].strip() if ':' in line else ''
        
        data['candidates'].append(candidate)
    
    # Parse races
    race_patterns = [
        r'\*\*([^*]+)\*\*\s*\(([^)]+)\)\s*-\s*(\d+)\s*seats?',
        r'\*\*([^*]+)\*\*.*?\(([^)]+)\s+Primary\)'
    ]
    
    for pattern in race_patterns:
        races = re.findall(pattern, content, re.IGNORECASE)
        for race_name, party, seats in races:
            data['races'].append({
                'office': race_name.strip(),
                'party_affiliation': party.strip(),
                'seats_available': int(seats) if seats.isdigit() else 1,
                'term_length': '4 years'
            })
    
    # Parse issues
    issue_section = re.search(r'##\s*Issues?\s*\n((?:\s*-\s*[^\n]+\n?)+)', content, re.IGNORECASE)
    if issue_section:
        for line in issue_section.group(1).strip().split('\n'):
            line = line.strip().lstrip('-').strip()
            if line:
                data['issues'].append({
                    'name': line,
                    'category': 'General'
                })
    
    return data


def migrate_to_supabase(data):
    """Migrate parsed election data to Supabase."""
    
    supabase = get_supabase()
    stats = {'candidates': 0, 'races': 0, 'elections': 0, 'issues': 0, 'errors': 0}
    
    # Get or create jurisdiction
    try:
        result = supabase.table('jurisdictions').select('id').eq('name', 'Wilkes County').execute()
        if result.data:
            jurisdiction_id = result.data[0]['id']
        else:
            result = supabase.table('jurisdictions').insert({
                'name': 'Wilkes County',
                'state': 'NC',
                'county': 'Wilkes',
                'type': 'county'
            }).execute()
            jurisdiction_id = result.data[0]['id']
    except Exception as e:
        print(f"Error with jurisdiction: {e}")
        jurisdiction_id = None
    
    # Insert candidates
    for item in data['candidates']:
        try:
            item['source_file'] = data['source_file']
            item['migrated_at'] = datetime.now().isoformat()
            supabase.table('candidates').insert(item).execute()
            stats['candidates'] += 1
        except Exception as e:
            print(f"Error inserting candidate: {e}")
            stats['errors'] += 1
    
    # Insert races
    for item in data['races']:
        try:
            item['source_file'] = data['source_file']
            item['migrated_at'] = datetime.now().isoformat()
            supabase.table('races').insert(item).execute()
            stats['races'] += 1
        except Exception as e:
            print(f"Error inserting race: {e}")
            stats['errors'] += 1
    
    # Insert issues
    for item in data['issues']:
        try:
            item['source_file'] = data['source_file']
            item['migrated_at'] = datetime.now().isoformat()
            supabase.table('issues').insert(item).execute()
            stats['issues'] += 1
        except Exception as e:
            print(f"Error inserting issue: {e}")
            stats['errors'] += 1
    
    return stats


def main():
    print("="*60)
    print("ELECTION RESEARCH MIGRATION TOOL")
    print("="*60)
    
    memory_dir = Path('/root/.openclaw/workspace/memory')
    files = list(memory_dir.glob('*election-research*.md'))
    
    # Also check root level files
    root_dir = Path('/root/.openclaw/workspace')
    root_files = list(root_dir.glob('*election*.md'))
    files.extend(root_files)
    
    print(f"\nFound {len(files)} election research files")
    
    total_stats = {'candidates': 0, 'races': 0, 'elections': 0, 'issues': 0, 'errors': 0}
    
    for filepath in files[:1]:  # Test with first file only
        print(f"\nProcessing: {filepath.name}")
        
        try:
            data = parse_election_research_file(filepath)
            print(f"  Parsed: {len(data['candidates'])} candidates, {len(data['races'])} races, {len(data['issues'])} issues")
            
            stats = migrate_to_supabase(data)
            
            for key in total_stats:
                total_stats[key] += stats[key]
            
            print(f"  Migrated: Candidates: {stats['candidates']}, Races: {stats['races']}, Issues: {stats['issues']}, Errors: {stats['errors']}")
            
        except Exception as e:
            print(f"  ERROR: {e}")
            import traceback
            traceback.print_exc()
    
    print("\n" + "="*60)
    print("MIGRATION COMPLETE")
    print("="*60)
    print(f"Total Candidates: {total_stats['candidates']}")
    print(f"Total Races: {total_stats['races']}")
    print(f"Total Issues: {total_stats['issues']}")
    print(f"Total Errors: {total_stats['errors']}")


if __name__ == "__main__":
    main()
