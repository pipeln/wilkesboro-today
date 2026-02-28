# Supabase Data Migration Plan

## Executive Summary

**Goal:** Migrate all data from local markdown files to Supabase database for centralized storage, querying, and real-time access.

**Current State:**
- 26+ memory files (social monitor reports, election research, daily logs)
- 11+ research files (resources, government data, healthcare)
- 3+ code review reports
- Data scattered across markdown files, not queryable

**Target State:**
- All structured data in Supabase tables
- Real-time access via API
- Proper relationships and indexing
- Automated ingestion pipeline

---

## Data Inventory

### 1. Social Monitor Reports
**Files:** `wilkes-social-monitor-*.md`, `2026-*-wilkes-social-monitor.md`

**Data Types:**
- News articles (headline, source, date, summary, URL)
- Events (title, date, location, description)
- Alerts (urgent items, public safety)
- Jobs (title, employer, location, posting date)
- Government notices (meetings, hearings, deadlines)

**Target Tables:**
- `news_items` - All news stories
- `events` - Community events
- `alerts` - Urgent public safety alerts
- `jobs` - Job postings
- `government_notices` - Official notices

### 2. Election Research
**Files:** `2026-*-election-research.md`, `wilkes_county_2026_election_summary.md`

**Data Types:**
- Candidates (name, party, bio, contact info)
- Races (office, seats, term, party)
- Elections (date, type, jurisdiction)
- Issues (policy topics)
- Candidate positions (stances on issues)
- Endorsements

**Target Tables:**
- `candidates` ✓ (already created)
- `races` ✓ (already created)
- `elections` ✓ (already created)
- `issues` ✓ (already created)
- `candidate_positions` ✓ (already created)
- `endorsements`

### 3. Resource Research
**Files:** `research/*resources*.md`, `wilkesboro_deep_research_*.md`

**Data Types:**
- Organizations (name, type, address, phone, website)
- Services (category, description, eligibility)
- Government offices
- Healthcare providers
- Education resources
- Housing assistance

**Target Tables:**
- `resources` ✓ (already created)
- `services`
- `organizations`

### 4. Daily Logs / Session Notes
**Files:** `2026-02-*.md` (daily notes)

**Data Types:**
- Actions taken
- Decisions made
- Tasks completed
- Notes and observations

**Target Tables:**
- `activity_logs`
- `decisions`
- `tasks`

### 5. Code Reviews
**Files:** `code-reviews/*.md`

**Data Types:**
- Issues found (security, performance, style)
- File locations
- Recommendations

**Target Tables:**
- `code_review_reports`
- `code_issues`

---

## Database Schema Design

### New Tables Needed

```sql
-- News Items (expanded from current)
CREATE TABLE news_items (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    headline TEXT NOT NULL,
    source_name TEXT,
    source_url TEXT,
    published_date DATE,
    summary TEXT,
    full_content TEXT,
    category TEXT, -- 'News', 'Event', 'Alert', 'Job', 'Government'
    subcategory TEXT,
    status TEXT DEFAULT 'New', -- 'New', 'Pending', 'Approved', 'Published', 'Rejected'
    location TEXT,
    community TEXT, -- 'Wilkesboro', 'North Wilkesboro', etc.
    county TEXT, -- 'Wilkes', 'Caldwell', etc.
    tags TEXT[],
    image_url TEXT,
    image_source TEXT, -- 'article', 'ai_generated', 'default'
    wordpress_post_id INTEGER,
    published_url TEXT,
    sent_to_telegram BOOLEAN DEFAULT FALSE,
    telegram_message_id TEXT,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    approved_at TIMESTAMP WITH TIME ZONE,
    published_at TIMESTAMP WITH TIME ZONE,
    approved_by TEXT,
    -- For tracking source of data
    source_file TEXT, -- which markdown file this came from
    migrated_at TIMESTAMP WITH TIME ZONE
);

-- Events (dedicated table for community events)
CREATE TABLE events (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    title TEXT NOT NULL,
    description TEXT,
    date_start DATE,
    date_end DATE,
    time_start TEXT,
    time_end TEXT,
    venue_name TEXT,
    venue_address TEXT,
    city TEXT,
    county TEXT,
    organizer_name TEXT,
    organizer_contact TEXT,
    source_url TEXT,
    category TEXT, -- 'Community', 'Government', 'School', 'Sports', etc.
    tags TEXT[],
    status TEXT DEFAULT 'New',
    image_url TEXT,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    source_file TEXT,
    migrated_at TIMESTAMP WITH TIME ZONE
);

-- Alerts (urgent public safety items)
CREATE TABLE alerts (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    title TEXT NOT NULL,
    description TEXT,
    alert_type TEXT, -- 'Weather', 'Public Safety', 'Health', 'Traffic'
    severity TEXT, -- 'Critical', 'High', 'Medium', 'Low'
    community TEXT,
    county TEXT,
    source_name TEXT,
    source_url TEXT,
    issued_at TIMESTAMP WITH TIME ZONE,
    expires_at TIMESTAMP WITH TIME ZONE,
    status TEXT DEFAULT 'Active', -- 'Active', 'Resolved', 'Cancelled'
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    resolved_at TIMESTAMP WITH TIME ZONE,
    source_file TEXT,
    migrated_at TIMESTAMP WITH TIME ZONE
);

-- Jobs
CREATE TABLE jobs (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    title TEXT NOT NULL,
    employer TEXT,
    employer_type TEXT, -- 'Government', 'Business', 'Nonprofit'
    location TEXT,
    city TEXT,
    county TEXT,
    description TEXT,
    requirements TEXT,
    salary_range TEXT,
    job_type TEXT, -- 'Full-time', 'Part-time', 'Contract'
    application_url TEXT,
    posted_date DATE,
    deadline_date DATE,
    status TEXT DEFAULT 'Open', -- 'Open', 'Closed', 'Filled'
    source_name TEXT,
    source_url TEXT,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    source_file TEXT,
    migrated_at TIMESTAMP WITH TIME ZONE
);

-- Government Notices
CREATE TABLE government_notices (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    title TEXT NOT NULL,
    notice_type TEXT, -- 'Meeting', 'Hearing', 'RFP', 'Public Comment'
    description TEXT,
    government_body TEXT, -- 'Wilkes County', 'Town of Wilkesboro', etc.
    meeting_date TIMESTAMP WITH TIME ZONE,
    location TEXT,
    agenda_items TEXT[],
    source_url TEXT,
    status TEXT DEFAULT 'Upcoming', -- 'Upcoming', 'Completed', 'Cancelled'
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    source_file TEXT,
    migrated_at TIMESTAMP WITH TIME ZONE
);

-- Services (from resource research)
CREATE TABLE services (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    name TEXT NOT NULL,
    category TEXT, -- 'Housing', 'Food', 'Healthcare', 'Employment', etc.
    subcategory TEXT,
    description TEXT,
    eligibility TEXT,
    application_process TEXT,
    required_documents TEXT[],
    contact_phone TEXT,
    contact_email TEXT,
    website TEXT,
    hours TEXT,
    location TEXT,
    city TEXT,
    county TEXT,
    status TEXT DEFAULT 'Active',
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    source_file TEXT,
    migrated_at TIMESTAMP WITH TIME ZONE
);

-- Activity Logs (for daily notes)
CREATE TABLE activity_logs (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    activity_date DATE NOT NULL,
    activity_type TEXT, -- 'Research', 'Development', 'Data Entry', 'Review'
    description TEXT,
    files_modified TEXT[],
    decisions_made TEXT[],
    notes TEXT,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    source_file TEXT,
    migrated_at TIMESTAMP WITH TIME ZONE
);

-- Code Review Reports
CREATE TABLE code_review_reports (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    report_date DATE NOT NULL,
    total_issues INTEGER,
    security_issues INTEGER,
    performance_issues INTEGER,
    style_issues INTEGER,
    files_scanned INTEGER,
    report_path TEXT,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    source_file TEXT,
    migrated_at TIMESTAMP WITH TIME ZONE
);

-- Code Issues (detailed issues from reviews)
CREATE TABLE code_issues (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    report_id UUID REFERENCES code_review_reports(id),
    file_path TEXT,
    line_number INTEGER,
    issue_type TEXT, -- 'Security', 'Performance', 'Style'
    severity TEXT, -- 'High', 'Medium', 'Low'
    description TEXT,
    recommendation TEXT,
    status TEXT DEFAULT 'Open', -- 'Open', 'Fixed', 'Ignored'
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    resolved_at TIMESTAMP WITH TIME ZONE
);
```

---

## Migration Strategy

### Phase 1: Schema Setup (Week 1)
1. Create all new tables in Supabase
2. Set up indexes for common queries
3. Set up Row Level Security (RLS) policies
4. Test connection and basic CRUD operations

### Phase 2: Parser Development (Week 1-2)
1. Build markdown parsers for each file type:
   - Social monitor report parser
   - Election research parser
   - Resource research parser
   - Daily log parser
   - Code review parser

2. Each parser should:
   - Extract structured data from markdown tables/lists
   - Handle variations in formatting
   - Map data to appropriate table columns
   - Track source file for traceability

### Phase 3: Data Migration (Week 2)
1. Run parsers on all historical files
2. Insert data into Supabase
3. Validate data integrity
4. Handle duplicates (skip or update)

### Phase 4: Automation Setup (Week 3)
1. Modify cron jobs to write directly to Supabase
2. Update Telegram bot to read from Supabase
3. Set up real-time subscriptions for new data
4. Create dashboard/views for data visualization

### Phase 5: Cleanup (Week 4)
1. Archive old markdown files
2. Update documentation
3. Train users on new workflow
4. Monitor for issues

---

## Implementation Plan

### Immediate Actions (Today)

1. **Create missing tables in Supabase**
   - Run SQL to create news_items, events, alerts, jobs, government_notices, services, activity_logs, code_review_reports, code_issues

2. **Build the social monitor parser**
   - Parse existing social monitor markdown files
   - Extract news items, events, alerts, jobs
   - Insert into appropriate tables

### This Week

1. **Build remaining parsers**
   - Election research parser
   - Resource research parser
   - Daily log parser

2. **Migrate historical data**
   - Run all parsers on existing files
   - Validate data in Supabase

3. **Update cron jobs**
   - Modify social monitor to write directly to Supabase
   - Modify election research to write directly to Supabase

### Next Week

1. **Update applications**
   - Telegram bot reads from Supabase
   - Website pulls from Supabase
   - Approval workflow uses Supabase

2. **Documentation**
   - Document schema
   - Document API usage
   - Create runbooks

---

## Tools & Scripts Needed

1. **Migration Scripts:**
   - `migrate_social_monitor.py` - Parse social monitor markdown files
   - `migrate_election_research.py` - Parse election research files
   - `migrate_resources.py` - Parse resource research files
   - `migrate_daily_logs.py` - Parse daily log files
   - `migrate_code_reviews.py` - Parse code review files

2. **Validation Scripts:**
   - `validate_migration.py` - Check data integrity
   - `count_records.py` - Compare markdown vs database counts

3. **Automation Updates:**
   - Update `telegram_approval_bot.py` to read from Supabase
   - Update cron job scripts to write to Supabase
   - Create real-time sync if needed

---

## Success Metrics

- [ ] All markdown data migrated to Supabase
- [ ] Zero data loss during migration
- [ ] Cron jobs writing directly to Supabase
- [ ] Telegram bot reading from Supabase
- [ ] Query response time < 100ms
- [ ] Documentation complete

---

## Next Steps

1. **Approve this plan**
2. **Create the missing tables** (I can do this now)
3. **Build the first parser** (social monitor)
4. **Test with a few files**
5. **Scale to all files**

Ready to proceed? I can start creating the tables and building the parsers.
