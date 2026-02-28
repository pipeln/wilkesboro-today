#!/usr/bin/env python3
"""
Execute SQL schema creation in Supabase using service role
"""

import os
import requests

SUPABASE_URL = os.environ.get('SUPABASE_URL', 'https://nahldyqwdqnifyljanxt.supabase.co')
SUPABASE_KEY = os.environ.get('SUPABASE_ANON_KEY', '')

def execute_sql_via_rest(sql):
    """Execute SQL via Supabase REST API (requires service role)"""
    
    # Try using the pg_execute function if available
    url = f"{SUPABASE_URL}/rest/v1/rpc/exec_sql"
    headers = {
        'apikey': SUPABASE_KEY,
        'Authorization': f'Bearer {SUPABASE_KEY}',
        'Content-Type': 'application/json'
    }
    
    payload = {'query': sql}
    
    try:
        response = requests.post(url, headers=headers, json=payload)
        if response.status_code == 200:
            return True, response.json()
        else:
            return False, f"Status {response.status_code}: {response.text}"
    except Exception as e:
        return False, str(e)


def create_tables_via_api():
    """Create tables using Supabase REST API (table creation via POST)"""
    
    supabase_headers = {
        'apikey': SUPABASE_KEY,
        'Authorization': f'Bearer {SUPABASE_KEY}',
        'Content-Type': 'application/json'
    }
    
    tables_created = []
    errors = []
    
    # Define table schemas
    tables = {
        'news_items': {
            'id': {'type': 'uuid', 'default': 'uuid_generate_v4()'},
            'headline': {'type': 'text', 'not_null': True},
            'source_name': {'type': 'text'},
            'source_url': {'type': 'text'},
            'published_date': {'type': 'date'},
            'summary': {'type': 'text'},
            'full_content': {'type': 'text'},
            'category': {'type': 'text', 'default': "'News'"},
            'subcategory': {'type': 'text'},
            'status': {'type': 'text', 'default': "'New'"},
            'location': {'type': 'text'},
            'community': {'type': 'text'},
            'county': {'type': 'text'},
            'tags': {'type': 'text[]'},
            'image_url': {'type': 'text'},
            'image_source': {'type': 'text'},
            'wordpress_post_id': {'type': 'int'},
            'published_url': {'type': 'text'},
            'sent_to_telegram': {'type': 'bool', 'default': 'false'},
            'telegram_message_id': {'type': 'text'},
            'created_at': {'type': 'timestamptz', 'default': 'now()'},
            'updated_at': {'type': 'timestamptz', 'default': 'now()'},
            'approved_at': {'type': 'timestamptz'},
            'published_at': {'type': 'timestamptz'},
            'approved_by': {'type': 'text'},
            'source_file': {'type': 'text'},
            'migrated_at': {'type': 'timestamptz'}
        },
        'events': {
            'id': {'type': 'uuid', 'default': 'uuid_generate_v4()'},
            'title': {'type': 'text', 'not_null': True},
            'description': {'type': 'text'},
            'date_start': {'type': 'date'},
            'date_end': {'type': 'date'},
            'time_start': {'type': 'text'},
            'time_end': {'type': 'text'},
            'venue_name': {'type': 'text'},
            'venue_address': {'type': 'text'},
            'city': {'type': 'text'},
            'county': {'type': 'text'},
            'organizer_name': {'type': 'text'},
            'organizer_contact': {'type': 'text'},
            'source_url': {'type': 'text'},
            'category': {'type': 'text', 'default': "'Community'"},
            'tags': {'type': 'text[]'},
            'status': {'type': 'text', 'default': "'New'"},
            'image_url': {'type': 'text'},
            'created_at': {'type': 'timestamptz', 'default': 'now()'},
            'updated_at': {'type': 'timestamptz', 'default': 'now()'},
            'source_file': {'type': 'text'},
            'migrated_at': {'type': 'timestamptz'}
        },
        'alerts': {
            'id': {'type': 'uuid', 'default': 'uuid_generate_v4()'},
            'title': {'type': 'text', 'not_null': True},
            'description': {'type': 'text'},
            'alert_type': {'type': 'text'},
            'severity': {'type': 'text'},
            'community': {'type': 'text'},
            'county': {'type': 'text'},
            'source_name': {'type': 'text'},
            'source_url': {'type': 'text'},
            'issued_at': {'type': 'timestamptz'},
            'expires_at': {'type': 'timestamptz'},
            'status': {'type': 'text', 'default': "'Active'"},
            'created_at': {'type': 'timestamptz', 'default': 'now()'},
            'resolved_at': {'type': 'timestamptz'},
            'source_file': {'type': 'text'},
            'migrated_at': {'type': 'timestamptz'}
        },
        'jobs': {
            'id': {'type': 'uuid', 'default': 'uuid_generate_v4()'},
            'title': {'type': 'text', 'not_null': True},
            'employer': {'type': 'text'},
            'employer_type': {'type': 'text'},
            'location': {'type': 'text'},
            'city': {'type': 'text'},
            'county': {'type': 'text'},
            'description': {'type': 'text'},
            'requirements': {'type': 'text'},
            'salary_range': {'type': 'text'},
            'job_type': {'type': 'text'},
            'application_url': {'type': 'text'},
            'posted_date': {'type': 'date'},
            'deadline_date': {'type': 'date'},
            'status': {'type': 'text', 'default': "'Open'"},
            'source_name': {'type': 'text'},
            'source_url': {'type': 'text'},
            'created_at': {'type': 'timestamptz', 'default': 'now()'},
            'updated_at': {'type': 'timestamptz', 'default': 'now()'},
            'source_file': {'type': 'text'},
            'migrated_at': {'type': 'timestamptz'}
        },
        'government_notices': {
            'id': {'type': 'uuid', 'default': 'uuid_generate_v4()'},
            'title': {'type': 'text', 'not_null': True},
            'notice_type': {'type': 'text'},
            'description': {'type': 'text'},
            'government_body': {'type': 'text'},
            'meeting_date': {'type': 'timestamptz'},
            'location': {'type': 'text'},
            'agenda_items': {'type': 'text[]'},
            'source_url': {'type': 'text'},
            'status': {'type': 'text', 'default': "'Upcoming'"},
            'created_at': {'type': 'timestamptz', 'default': 'now()'},
            'updated_at': {'type': 'timestamptz', 'default': 'now()'},
            'source_file': {'type': 'text'},
            'migrated_at': {'type': 'timestamptz'}
        },
        'services': {
            'id': {'type': 'uuid', 'default': 'uuid_generate_v4()'},
            'name': {'type': 'text', 'not_null': True},
            'category': {'type': 'text'},
            'subcategory': {'type': 'text'},
            'description': {'type': 'text'},
            'eligibility': {'type': 'text'},
            'application_process': {'type': 'text'},
            'required_documents': {'type': 'text[]'},
            'contact_phone': {'type': 'text'},
            'contact_email': {'type': 'text'},
            'website': {'type': 'text'},
            'hours': {'type': 'text'},
            'location': {'type': 'text'},
            'city': {'type': 'text'},
            'county': {'type': 'text'},
            'status': {'type': 'text', 'default': "'Active'"},
            'created_at': {'type': 'timestamptz', 'default': 'now()'},
            'updated_at': {'type': 'timestamptz', 'default': 'now()'},
            'source_file': {'type': 'text'},
            'migrated_at': {'type': 'timestamptz'}
        },
        'activity_logs': {
            'id': {'type': 'uuid', 'default': 'uuid_generate_v4()'},
            'activity_date': {'type': 'date', 'not_null': True},
            'activity_type': {'type': 'text'},
            'description': {'type': 'text'},
            'files_modified': {'type': 'text[]'},
            'decisions_made': {'type': 'text[]'},
            'notes': {'type': 'text'},
            'created_at': {'type': 'timestamptz', 'default': 'now()'},
            'source_file': {'type': 'text'},
            'migrated_at': {'type': 'timestamptz'}
        },
        'code_review_reports': {
            'id': {'type': 'uuid', 'default': 'uuid_generate_v4()'},
            'report_date': {'type': 'date', 'not_null': True},
            'total_issues': {'type': 'int', 'default': '0'},
            'security_issues': {'type': 'int', 'default': '0'},
            'performance_issues': {'type': 'int', 'default': '0'},
            'style_issues': {'type': 'int', 'default': '0'},
            'files_scanned': {'type': 'int', 'default': '0'},
            'report_path': {'type': 'text'},
            'created_at': {'type': 'timestamptz', 'default': 'now()'},
            'source_file': {'type': 'text'},
            'migrated_at': {'type': 'timestamptz'}
        },
        'code_issues': {
            'id': {'type': 'uuid', 'default': 'uuid_generate_v4()'},
            'report_id': {'type': 'uuid'},
            'file_path': {'type': 'text'},
            'line_number': {'type': 'int'},
            'issue_type': {'type': 'text'},
            'severity': {'type': 'text'},
            'description': {'type': 'text'},
            'recommendation': {'type': 'text'},
            'status': {'type': 'text', 'default': "'Open'"},
            'created_at': {'type': 'timestamptz', 'default': 'now()'},
            'resolved_at': {'type': 'timestamptz'}
        }
    }
    
    # Try to create each table via direct REST API
    for table_name, columns in tables.items():
        try:
            # Check if table exists by trying to select from it
            check_url = f"{SUPABASE_URL}/rest/v1/{table_name}?limit=1"
            check_response = requests.get(check_url, headers=supabase_headers)
            
            if check_response.status_code == 200:
                print(f"✓ Table '{table_name}' already exists")
                tables_created.append(table_name)
                continue
            
            # Table doesn't exist, we need to create it via SQL
            print(f"✗ Table '{table_name}' does not exist - needs SQL creation")
            
        except Exception as e:
            errors.append(f"{table_name}: {e}")
    
    return tables_created, errors


def main():
    print("="*60)
    print("SUPABASE TABLE CREATION")
    print("="*60)
    
    if not SUPABASE_KEY:
        print("ERROR: SUPABASE_ANON_KEY not set")
        return
    
    print("\nChecking existing tables...")
    tables_created, errors = create_tables_via_api()
    
    print(f"\n✓ Tables found: {len(tables_created)}")
    for t in tables_created:
        print(f"  - {t}")
    
    if errors:
        print(f"\n✗ Errors: {len(errors)}")
        for e in errors:
            print(f"  - {e}")
    
    print("\n" + "="*60)
    print("NOTE: To create missing tables, run migration_schema.sql")
    print("in the Supabase Dashboard SQL Editor.")
    print("="*60)


if __name__ == "__main__":
    main()
