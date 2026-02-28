#!/bin/bash
# Production Setup Script
# Run this to set up the complete workflow

echo "=========================================="
echo "WILKESBORO TODAY - PRODUCTION SETUP"
echo "=========================================="
echo ""

# Check environment
echo "1. Checking environment..."

if [ -z "$SUPABASE_ANON_KEY" ]; then
    echo "   ❌ SUPABASE_ANON_KEY not set"
    echo "   Add to .env: SUPABASE_ANON_KEY=your_key"
    exit 1
fi

echo "   ✓ SUPABASE_ANON_KEY set"

# Check Python dependencies
echo ""
echo "2. Checking Python dependencies..."

python3 -c "import supabase" 2>/dev/null
if [ $? -ne 0 ]; then
    echo "   Installing supabase-py..."
    pip install supabase --quiet
fi
echo "   ✓ Dependencies ready"

# Clean existing test data
echo ""
echo "3. Cleaning test data..."
cd /root/.openclaw/workspace
python3 cleanup_data.py

# Set up cron jobs
echo ""
echo "4. Setting up cron jobs..."

CRON_FILE="/tmp/wilkesboro_cron"

# Write cron jobs
cat > $CRON_FILE << 'EOF'
# Wilkesboro Today - Production Cron Jobs

# Data collection every 4 hours
0 */4 * * * cd /root/.openclaw/workspace && python3 collect_news.py >> logs/cron_news.log 2>&1

# Send pending items to Telegram for approval
5 */4 * * * cd /root/.openclaw/workspace && python3 telegram_approval_bot.py >> logs/cron_telegram.log 2>&1

# Build and deploy website
10 */4 * * * cd /root/.openclaw/workspace && python3 build_website.py >> logs/cron_build.log 2>&1

# Daily cleanup at 3 AM
0 3 * * * cd /root/.openclaw/workspace && python3 cleanup_data.py >> logs/cron_cleanup.log 2>&1

# Business reports - 8 AM, 12 PM, 4 PM, 8 PM
0 8,12,16,20 * * * cd /root/.openclaw/workspace && python3 reporting_agent.py >> logs/cron_report.log 2>&1

# Weekly report on Sundays at 8 AM
0 8 * * 0 cd /root/.openclaw/workspace && python3 reporting_agent.py >> logs/cron_report.log 2>&1
EOF

# Install cron jobs
crontab $CRON_FILE
rm $CRON_FILE

echo "   ✓ Cron jobs installed"
echo ""
echo "   Schedule:"
echo "   - Every 4 hours: Data collection → Telegram approval → Website build"
echo "   - Daily 3 AM: Data cleanup"
echo "   - 4x Daily: Business reports (8AM, 12PM, 4PM, 8PM)"
echo "   - Weekly Sunday 8 AM: Full analytics report"

# Create log directory
echo ""
echo "5. Creating log directory..."
mkdir -p /root/.openclaw/workspace/logs
echo "   ✓ Logs directory ready"

# Summary
echo ""
echo "=========================================="
echo "SETUP COMPLETE!"
echo "=========================================="
echo ""
echo "Next steps:"
echo "1. Review PRODUCTION_WORKFLOW.md for details"
echo "2. Test Telegram bot: python3 telegram_approval_bot.py"
echo "3. Check cron jobs: crontab -l"
echo "4. Monitor logs: tail -f logs/*.log"
echo ""
echo "Your workflow:"
echo "- News is collected automatically every 4 hours"
echo "- You approve via Telegram"
echo "- Website builds and deploys automatically"
echo "- Everything is backed up in Supabase"
echo ""
