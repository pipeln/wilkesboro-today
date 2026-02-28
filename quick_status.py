#!/usr/bin/env python3
"""
Quick Status Check - For manual /status command
"""

import os
from datetime import datetime
from supabase import create_client

SUPABASE_URL = os.environ.get('SUPABASE_URL', 'https://nahldyqwdqnifyljanxt.supabase.co')
SUPABASE_KEY = os.environ.get('SUPABASE_ANON_KEY', '')

def get_supabase():
    return create_client(SUPABASE_URL, SUPABASE_KEY)

def main():
    supabase = get_supabase()
    
    # Quick stats
    news = supabase.table('news_items').select('count', count='exact').execute()
    pending = supabase.table('news_items').select('count', count='exact').eq('status', 'New').execute()
    approved = supabase.table('news_items').select('count', count='exact').eq('status', 'Approved').execute()
    
    print(f"""
⚡ QUICK STATUS
Time: {datetime.now().strftime('%H:%M')}

📊 Database:
• Total news: {news.count}
• Pending: {pending.count}
• Approved: {approved.count}

💡 Next: Run reporting_agent.py for full report
""")

if __name__ == "__main__":
    main()
