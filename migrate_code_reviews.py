#!/usr/bin/env python3
"""
Code Review Markdown Parser
Parses code review reports and migrates to Supabase
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


def parse_code_review_file(filepath):
    """Parse code review markdown file."""
    
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()
    
    filename = os.path.basename(filepath)
    
    # Extract date from filename
    date_match = re.search(r'(\d{4}-\d{2}-\d{2})', filename)
    if date_match:
        report_date = date_match.group(1)
    else:
        report_date = datetime.now().strftime('%Y-%m-%d')
    
    data = {
        'report': {},
        'issues': [],
        'source_file': filename
    }
    
    # Parse summary stats
    total_match = re.search(r'\*\*Total Issues:\*\*\s*(\d+)', content)
    security_match = re.search(r'Security Issues:\*\*\s*(\d+)', content)
    perf_match = re.search(r'Performance Issues:\*\*\s*(\d+)', content)
    style_match = re.search(r'(Style|Code Quality) Issues:\*\*\s*(\d+)', content)
    files_match = re.search(r'Files Scanned:\*\*\s*(\d+)', content)
    
    data['report'] = {
        'report_date': report_date,
        'total_issues': int(total_match.group(1)) if total_match else 0,
        'security_issues': int(security_match.group(1)) if security_match else 0,
        'performance_issues': int(perf_match.group(1)) if perf_match else 0,
        'style_issues': int(style_match.group(2)) if style_match else 0,
        'files_scanned': int(files_match.group(1)) if files_match else 0,
        'report_path': str(filepath)
    }
    
    # Parse security issues
    security_section = re.search(
        r'###\s*(?:🔒\s*)?Security Issues.*?\n((?:\|[^\n]+\|\n?)+)',
        content,
        re.DOTALL | re.IGNORECASE
    )
    if security_section:
        rows = re.findall(r'\|\s*([^|]+)\s*\|\s*([^|]+)\s*\|', security_section.group(1))
        for file_path, issue in rows:
            if file_path.strip() and file_path.strip() != 'File':
                data['issues'].append({
                    'file_path': file_path.strip(),
                    'issue_type': 'Security',
                    'severity': 'High',
                    'description': issue.strip(),
                    'status': 'Open'
                })
    
    # Parse performance issues
    perf_section = re.search(
        r'###\s*(?:⚡\s*)?Performance Issues.*?\n((?:\|[^\n]+\|\n?)+)',
        content,
        re.DOTALL | re.IGNORECASE
    )
    if perf_section:
        rows = re.findall(r'\|\s*([^|]+)\s*\|\s*([^|]+)\s*\|', perf_section.group(1))
        for file_path, issue in rows:
            if file_path.strip() and file_path.strip() != 'File':
                data['issues'].append({
                    'file_path': file_path.strip(),
                    'issue_type': 'Performance',
                    'severity': 'Medium',
                    'description': issue.strip(),
                    'status': 'Open'
                })
    
    # Parse code quality issues
    quality_section = re.search(
        r'###\s*(?:📝\s*)?(?:Code Quality|Style).*?\n((?:\|[^\n]+\|\n?)+)',
        content,
        re.DOTALL | re.IGNORECASE
    )
    if quality_section:
        rows = re.findall(r'\|\s*([^|]+)\s*\|\s*([^|]+)\s*\|', quality_section.group(1))
        for file_path, issue in rows:
            if file_path.strip() and file_path.strip() != 'File':
                data['issues'].append({
                    'file_path': file_path.strip(),
                    'issue_type': 'Style',
                    'severity': 'Low',
                    'description': issue.strip(),
                    'status': 'Open'
                })
    
    # Also look for bullet point issues
    bullet_issues = re.findall(r'^\s*[-*]\s*([^\n]+)', content, re.MULTILINE)
    for issue in bullet_issues:
        if any(keyword in issue.lower() for keyword in ['bare except', 'line too long', 'todo', 'fixme']):
            # Extract file path if mentioned
            file_match = re.search(r'`?([^`\s]+\.py)`?', issue)
            file_path = file_match.group(1) if file_match else 'Unknown'
            
            # Determine type
            if 'bare except' in issue.lower():
                issue_type = 'Style'
                severity = 'Medium'
            elif 'line too long' in issue.lower():
                issue_type = 'Style'
                severity = 'Low'
            elif 'todo' in issue.lower() or 'fixme' in issue.lower():
                issue_type = 'Maintenance'
                severity = 'Low'
            else:
                issue_type = 'Style'
                severity = 'Low'
            
            data['issues'].append({
                'file_path': file_path,
                'issue_type': issue_type,
                'severity': severity,
                'description': issue.strip(),
                'status': 'Open'
            })
    
    return data


def migrate_to_supabase(data):
    """Migrate parsed code review data to Supabase."""
    
    supabase = get_supabase()
    stats = {'reports': 0, 'issues': 0, 'errors': 0}
    
    # Insert report
    try:
        report_data = data['report'].copy()
        report_data['source_file'] = data['source_file']
        report_data['migrated_at'] = datetime.now().isoformat()
        
        result = supabase.table('code_review_reports').insert(report_data).execute()
        report_id = result.data[0]['id']
        stats['reports'] += 1
        
        # Insert issues
        for issue in data['issues']:
            try:
                issue['report_id'] = report_id
                issue['created_at'] = datetime.now().isoformat()
                
                supabase.table('code_issues').insert(issue).execute()
                stats['issues'] += 1
            except Exception as e:
                print(f"Error inserting issue: {e}")
                stats['errors'] += 1
                
    except Exception as e:
        print(f"Error inserting report: {e}")
        stats['errors'] += 1
    
    return stats


def main():
    print("="*60)
    print("CODE REVIEW MIGRATION TOOL")
    print("="*60)
    
    code_review_dir = Path('/root/.openclaw/workspace/code-reviews')
    files = list(code_review_dir.glob('*.md'))
    
    print(f"\nFound {len(files)} code review files")
    
    total_stats = {'reports': 0, 'issues': 0, 'errors': 0}
    
    for filepath in files[:1]:  # Test with first file only
        print(f"\nProcessing: {filepath.name}")
        
        try:
            data = parse_code_review_file(filepath)
            print(f"  Parsed: Report with {len(data['issues'])} issues")
            
            stats = migrate_to_supabase(data)
            
            for key in total_stats:
                total_stats[key] += stats[key]
            
            print(f"  Migrated: Reports: {stats['reports']}, Issues: {stats['issues']}, Errors: {stats['errors']}")
            
        except Exception as e:
            print(f"  ERROR: {e}")
            import traceback
            traceback.print_exc()
    
    print("\n" + "="*60)
    print("MIGRATION COMPLETE")
    print("="*60)
    print(f"Total Reports: {total_stats['reports']}")
    print(f"Total Issues: {total_stats['issues']}")
    print(f"Total Errors: {total_stats['errors']}")


if __name__ == "__main__":
    main()
