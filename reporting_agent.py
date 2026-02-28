#!/usr/bin/env python3
"""
Daily Business Report Agent
Provides executive summary updates throughout the day
Like attending a business meeting with status from all departments
"""

import os
import json
import requests
from datetime import datetime, timedelta
from supabase import create_client
from collections import defaultdict

SUPABASE_URL = os.environ.get('SUPABASE_URL', 'https://nahldyqwdqnifyljanxt.supabase.co')
SUPABASE_KEY = os.environ.get('SUPABASE_ANON_KEY', '')
TELEGRAM_BOT_TOKEN = os.environ.get('TELEGRAM_BOT_TOKEN', '')
TELEGRAM_CHAT_ID = os.environ.get('TELEGRAM_CHAT_ID', '')

def get_supabase():
    if not SUPABASE_KEY:
        raise ValueError("SUPABASE_ANON_KEY not set")
    return create_client(SUPABASE_URL, SUPABASE_KEY)


def get_database_health():
    """Check database connection and status."""
    try:
        supabase = get_supabase()
        
        # Check connection
        result = supabase.table('news_items').select('count', count='exact').execute()
        news_count = result.count
        
        # Get table counts
        tables = ['news_items', 'events', 'alerts', 'jobs', 'candidates', 'resources']
        counts = {}
        
        for table in tables:
            try:
                result = supabase.table(table).select('count', count='exact').execute()
                counts[table] = result.count
            except:
                counts[table] = 'Error'
        
        # Get recent activity (last 24 hours)
        yesterday = (datetime.now() - timedelta(days=1)).isoformat()
        
        recent_news = supabase.table('news_items').select('count', count='exact').gte('created_at', yesterday).execute()
        recent_approved = supabase.table('news_items').select('count', count='exact').eq('status', 'Approved').gte('created_at', yesterday).execute()
        
        return {
            'status': '✅ Healthy',
            'connection': 'Connected',
            'total_records': sum(c for c in counts.values() if isinstance(c, int)),
            'table_counts': counts,
            'recent_activity': {
                'new_items_24h': recent_news.count,
                'approved_24h': recent_approved.count
            }
        }
    except Exception as e:
        return {
            'status': '❌ Error',
            'connection': f'Failed: {str(e)[:50]}',
            'total_records': 0,
            'table_counts': {},
            'recent_activity': {}
        }


def get_agent_status():
    """Get status of all agents/cron jobs."""
    
    agents = {
        'wilkes-social-monitor': {
            'name': 'Social Media Monitor',
            'purpose': 'Monitors news sources across Wilkes County and surrounding communities',
            'schedule': 'Every hour',
            'category': 'Data Collection'
        },
        'deep-research-agent': {
            'name': 'Deep Research Agent',
            'purpose': 'Discovers and catalogs community resources, government offices, and services',
            'schedule': 'Every 4 hours',
            'category': 'Data Collection'
        },
        'election-research-agent': {
            'name': 'Election Research Agent',
            'purpose': 'Gathers comprehensive information on candidates and election races',
            'schedule': 'Every 6 hours',
            'category': 'Election Data'
        },
        'wilkes-jobs-monitor': {
            'name': 'Jobs Monitor',
            'purpose': 'Checks job boards for employment opportunities in the region',
            'schedule': 'Daily',
            'category': 'Employment'
        },
        'code-review-agent': {
            'name': 'Code Review Agent',
            'purpose': 'Scans code for security issues, performance problems, and quality concerns',
            'schedule': 'Daily',
            'category': 'Quality Assurance'
        }
    }
    
    # Check log files for recent activity
    log_dir = '/root/.openclaw/workspace/logs'
    
    for agent_id, agent in agents.items():
        # Default status
        agent['status'] = '⏸️ Idle'
        agent['last_run'] = 'Unknown'
        agent['items_processed'] = 0
        
        # Check for recent log activity
        log_file = f"{log_dir}/{agent_id.replace('-', '_')}.log"
        if os.path.exists(log_file):
            try:
                # Get last modified time
                mtime = os.path.getmtime(log_file)
                last_run = datetime.fromtimestamp(mtime)
                
                if datetime.now() - last_run < timedelta(hours=2):
                    agent['status'] = '✅ Active'
                elif datetime.now() - last_run < timedelta(hours=6):
                    agent['status'] = '⚠️ Delayed'
                else:
                    agent['status'] = '❌ Stalled'
                
                agent['last_run'] = last_run.strftime('%H:%M')
                
                # Count items from log (approximate)
                with open(log_file, 'r') as f:
                    content = f.read()
                    if 'Found' in content:
                        import re
                        matches = re.findall(r'Found (\d+)', content)
                        if matches:
                            agent['items_processed'] = sum(int(m) for m in matches[-5:])
            except:
                pass
    
    return agents


def get_pending_approvals():
    """Get items waiting for approval."""
    try:
        supabase = get_supabase()
        
        # New items
        new_items = supabase.table('news_items').select('count', count='exact').eq('status', 'New').execute()
        
        # Pending Telegram
        pending_telegram = supabase.table('news_items').select('count', count='exact').eq('sent_to_telegram', False).execute()
        
        return {
            'new_items': new_items.count,
            'awaiting_telegram': pending_telegram.count
        }
    except:
        return {'new_items': 0, 'awaiting_telegram': 0}


def generate_executive_summary():
    """Generate executive summary report."""
    
    now = datetime.now().strftime('%A, %B %d, %Y at %I:%M %p')
    
    # Get all data
    db_health = get_database_health()
    agents = get_agent_status()
    pending = get_pending_approvals()
    
    # Build report
    report = f"""
📊 **DAILY BUSINESS REPORT**
{now}

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

🏢 **DATABASE STATUS**
Status: {db_health['status']}
Connection: {db_health['connection']}
Total Records: {db_health['total_records']:,}

Recent Activity (24h):
• New Items: {db_health.get('recent_activity', {}).get('new_items_24h', 0)}
• Approved: {db_health.get('recent_activity', {}).get('approved_24h', 0)}

Table Breakdown:
"""
    
    for table, count in db_health.get('table_counts', {}).items():
        report += f"• {table}: {count:,}\n"
    
    report += f"""
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

🤖 **AGENT STATUS REPORT**
"""
    
    # Group agents by category
    by_category = defaultdict(list)
    for agent_id, agent in agents.items():
        by_category[agent['category']].append((agent_id, agent))
    
    for category, agent_list in by_category.items():
        report += f"\n**{category}**\n"
        for agent_id, agent in agent_list:
            report += f"""
{agent['status']} {agent['name']}
├─ Purpose: {agent['purpose'][:60]}...
├─ Schedule: {agent['schedule']}
├─ Last Run: {agent['last_run']}
└─ Items: {agent['items_processed']}
"""
    
    report += f"""
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

📋 **PENDING ACTIONS**
• New items awaiting review: {pending['new_items']}
• Items to send to Telegram: {pending['awaiting_telegram']}

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

💡 **RECOMMENDATIONS**
"""
    
    # Add recommendations based on status
    if pending['new_items'] > 10:
        report += "• High volume of new items - consider reviewing\n"
    
    stalled_agents = [a['name'] for a in agents.values() if 'Stalled' in a['status']]
    if stalled_agents:
        report += f"• Check stalled agents: {', '.join(stalled_agents)}\n"
    
    if db_health['status'] != '✅ Healthy':
        report += "• ⚠️ Database connection issue - investigate immediately\n"
    
    report += "• Review and approve pending items via Telegram\n"
    report += "• Monitor website build status\n"
    
    report += """
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

Reply with:
/report - Full detailed report
/approve - View pending approvals
/status - Quick status check
"""
    
    return report


def send_telegram_report(report_text):
    """Send report via Telegram."""
    if not TELEGRAM_BOT_TOKEN or not TELEGRAM_CHAT_ID:
        print("Telegram not configured")
        return False
    
    url = f"https://api.telegram.org/bot{TELEGRAM_BOT_TOKEN}/sendMessage"
    payload = {
        'chat_id': TELEGRAM_CHAT_ID,
        'text': report_text,
        'parse_mode': 'Markdown'
    }
    
    try:
        response = requests.post(url, json=payload)
        return response.status_code == 200
    except Exception as e:
        print(f"Failed to send Telegram: {e}")
        return False


def main():
    print("="*60)
    print("DAILY BUSINESS REPORT AGENT")
    print("="*60)
    print(f"Generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print()
    
    # Generate report
    report = generate_executive_summary()
    
    # Print to console
    print(report)
    
    # Send to Telegram
    print("\nSending to Telegram...")
    if send_telegram_report(report):
        print("✅ Report sent successfully")
    else:
        print("❌ Failed to send report")
    
    # Save to file
    report_file = f"/root/.openclaw/workspace/logs/daily_report_{datetime.now().strftime('%Y%m%d_%H%M')}.txt"
    with open(report_file, 'w') as f:
        f.write(report)
    print(f"✅ Report saved to: {report_file}")


if __name__ == "__main__":
    main()
