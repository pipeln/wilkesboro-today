-- ============================================================
-- Supabase Migration: New Tables for Complete Data Migration
-- Execute this SQL in Supabase Dashboard SQL Editor
-- ============================================================

-- Enable UUID extension
CREATE EXTENSION IF NOT EXISTS "uuid-ossp";

-- ============================================================
-- NEWS & CONTENT TABLES
-- ============================================================

-- News Items (comprehensive news stories)
CREATE TABLE IF NOT EXISTS news_items (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    headline TEXT NOT NULL,
    source_name TEXT,
    source_url TEXT,
    published_date DATE,
    summary TEXT,
    full_content TEXT,
    category TEXT DEFAULT 'News', -- 'News', 'Event', 'Alert', 'Job', 'Government'
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
    source_file TEXT,
    migrated_at TIMESTAMP WITH TIME ZONE
);

-- Events (community events)
CREATE TABLE IF NOT EXISTS events (
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
    category TEXT DEFAULT 'Community', -- 'Community', 'Government', 'School', 'Sports'
    tags TEXT[],
    status TEXT DEFAULT 'New', -- 'New', 'Approved', 'Published'
    image_url TEXT,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    source_file TEXT,
    migrated_at TIMESTAMP WITH TIME ZONE
);

-- Alerts (urgent public safety items)
CREATE TABLE IF NOT EXISTS alerts (
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

-- Jobs (job postings)
CREATE TABLE IF NOT EXISTS jobs (
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

-- Government Notices (meetings, hearings, RFPs)
CREATE TABLE IF NOT EXISTS government_notices (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    title TEXT NOT NULL,
    notice_type TEXT, -- 'Meeting', 'Hearing', 'RFP', 'Public Comment'
    description TEXT,
    government_body TEXT, -- 'Wilkes County', 'Town of Wilkesboro'
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

-- ============================================================
-- RESOURCE TABLES
-- ============================================================

-- Services (community services)
CREATE TABLE IF NOT EXISTS services (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    name TEXT NOT NULL,
    category TEXT, -- 'Housing', 'Food', 'Healthcare', 'Employment'
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

-- ============================================================
-- ACTIVITY & LOG TABLES
-- ============================================================

-- Activity Logs (daily work logs)
CREATE TABLE IF NOT EXISTS activity_logs (
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

-- ============================================================
-- CODE QUALITY TABLES
-- ============================================================

-- Code Review Reports
CREATE TABLE IF NOT EXISTS code_review_reports (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    report_date DATE NOT NULL,
    total_issues INTEGER DEFAULT 0,
    security_issues INTEGER DEFAULT 0,
    performance_issues INTEGER DEFAULT 0,
    style_issues INTEGER DEFAULT 0,
    files_scanned INTEGER DEFAULT 0,
    report_path TEXT,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    source_file TEXT,
    migrated_at TIMESTAMP WITH TIME ZONE
);

-- Code Issues (detailed findings)
CREATE TABLE IF NOT EXISTS code_issues (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    report_id UUID REFERENCES code_review_reports(id) ON DELETE CASCADE,
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

-- ============================================================
-- INDEXES FOR PERFORMANCE
-- ============================================================

-- News items indexes
CREATE INDEX IF NOT EXISTS idx_news_items_date ON news_items(published_date DESC);
CREATE INDEX IF NOT EXISTS idx_news_items_status ON news_items(status);
CREATE INDEX IF NOT EXISTS idx_news_items_category ON news_items(category);
CREATE INDEX IF NOT EXISTS idx_news_items_county ON news_items(county);
CREATE INDEX IF NOT EXISTS idx_news_items_community ON news_items(community);
CREATE INDEX IF NOT EXISTS idx_news_items_telegram ON news_items(sent_to_telegram);

-- Events indexes
CREATE INDEX IF NOT EXISTS idx_events_date ON events(date_start DESC);
CREATE INDEX IF NOT EXISTS idx_events_status ON events(status);
CREATE INDEX IF NOT EXISTS idx_events_county ON events(county);

-- Alerts indexes
CREATE INDEX IF NOT EXISTS idx_alerts_severity ON alerts(severity);
CREATE INDEX IF NOT EXISTS idx_alerts_status ON alerts(status);
CREATE INDEX IF NOT EXISTS idx_alerts_county ON alerts(county);

-- Jobs indexes
CREATE INDEX IF NOT EXISTS idx_jobs_status ON jobs(status);
CREATE INDEX IF NOT EXISTS idx_jobs_county ON jobs(county);
CREATE INDEX IF NOT EXISTS idx_jobs_posted_date ON jobs(posted_date DESC);

-- Government notices indexes
CREATE INDEX IF NOT EXISTS idx_notices_date ON government_notices(meeting_date DESC);
CREATE INDEX IF NOT EXISTS idx_notices_status ON government_notices(status);

-- Services indexes
CREATE INDEX IF NOT EXISTS idx_services_category ON services(category);
CREATE INDEX IF NOT EXISTS idx_services_county ON services(county);

-- ============================================================
-- ROW LEVEL SECURITY (RLS) POLICIES
-- ============================================================

-- Enable RLS on all tables
ALTER TABLE news_items ENABLE ROW LEVEL SECURITY;
ALTER TABLE events ENABLE ROW LEVEL SECURITY;
ALTER TABLE alerts ENABLE ROW LEVEL SECURITY;
ALTER TABLE jobs ENABLE ROW LEVEL SECURITY;
ALTER TABLE government_notices ENABLE ROW LEVEL SECURITY;
ALTER TABLE services ENABLE ROW LEVEL SECURITY;
ALTER TABLE activity_logs ENABLE ROW LEVEL SECURITY;
ALTER TABLE code_review_reports ENABLE ROW LEVEL SECURITY;
ALTER TABLE code_issues ENABLE ROW LEVEL SECURITY;

-- Create policies (allow all for now - adjust as needed)
CREATE POLICY "Allow all" ON news_items FOR ALL USING (true) WITH CHECK (true);
CREATE POLICY "Allow all" ON events FOR ALL USING (true) WITH CHECK (true);
CREATE POLICY "Allow all" ON alerts FOR ALL USING (true) WITH CHECK (true);
CREATE POLICY "Allow all" ON jobs FOR ALL USING (true) WITH CHECK (true);
CREATE POLICY "Allow all" ON government_notices FOR ALL USING (true) WITH CHECK (true);
CREATE POLICY "Allow all" ON services FOR ALL USING (true) WITH CHECK (true);
CREATE POLICY "Allow all" ON activity_logs FOR ALL USING (true) WITH CHECK (true);
CREATE POLICY "Allow all" ON code_review_reports FOR ALL USING (true) WITH CHECK (true);
CREATE POLICY "Allow all" ON code_issues FOR ALL USING (true) WITH CHECK (true);

-- ============================================================
-- INITIAL DATA (Optional - for testing)
-- ============================================================

-- Add a test record to verify setup
INSERT INTO news_items (headline, source_name, summary, category, county, status, tags)
VALUES (
    'Test: Supabase Migration Complete',
    'System',
    'Database schema successfully created for Wilkesboro Today data migration.',
    'System',
    'Wilkes',
    'New',
    ARRAY['test', 'migration']
);

SELECT 'Supabase Migration Schema Created Successfully!' as status;
