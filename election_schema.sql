-- ============================================================
-- Supabase Election Database Schema
-- Execute this SQL in your Supabase Dashboard SQL Editor
-- ============================================================

-- Enable UUID extension
CREATE EXTENSION IF NOT EXISTS "uuid-ossp";

-- Jurisdictions (counties, districts, etc.)
CREATE TABLE IF NOT EXISTS jurisdictions (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    name TEXT NOT NULL,
    state TEXT NOT NULL,
    county TEXT,
    type TEXT NOT NULL, -- 'county', 'city', 'state', 'federal'
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);

-- Elections
CREATE TABLE IF NOT EXISTS elections (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    name TEXT NOT NULL,
    election_date DATE NOT NULL,
    election_type TEXT NOT NULL, -- 'primary', 'general', 'special', 'runoff'
    jurisdiction_id UUID REFERENCES jurisdictions(id),
    status TEXT DEFAULT 'upcoming', -- 'upcoming', 'active', 'completed', 'cancelled'
    early_voting_start DATE,
    early_voting_end DATE,
    registration_deadline DATE,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);

-- Races (specific contests within an election)
CREATE TABLE IF NOT EXISTS races (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    election_id UUID REFERENCES elections(id),
    office TEXT NOT NULL, -- 'Sheriff', 'Commissioner', 'Board of Education'
    district TEXT, -- for district-specific races
    seats_available INTEGER DEFAULT 1,
    term_length TEXT, -- '2 years', '4 years', etc.
    party_affiliation TEXT, -- 'Republican', 'Democrat', 'Non-partisan', etc.
    salary TEXT,
    description TEXT,
    requirements TEXT,
    status TEXT DEFAULT 'active',
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);

-- Candidates
CREATE TABLE IF NOT EXISTS candidates (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    full_name TEXT NOT NULL,
    first_name TEXT,
    last_name TEXT,
    party TEXT,
    incumbent BOOLEAN DEFAULT FALSE,
    email TEXT,
    phone TEXT,
    website TEXT,
    facebook TEXT,
    twitter TEXT,
    linkedin TEXT,
    photo_url TEXT,
    biography TEXT,
    occupation TEXT,
    education TEXT,
    previous_offices TEXT,
    age INTEGER,
    residence TEXT,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);

-- Candidate-Race junction (candidates can run in multiple races over time)
CREATE TABLE IF NOT EXISTS candidacies (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    candidate_id UUID REFERENCES candidates(id),
    race_id UUID REFERENCES races(id),
    election_id UUID REFERENCES elections(id),
    status TEXT DEFAULT 'active', -- 'active', 'withdrawn', 'disqualified', 'won', 'lost'
    votes_received INTEGER,
    vote_percentage DECIMAL(5,2),
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    UNIQUE(candidate_id, race_id, election_id)
);

-- Issues/Policy Areas
CREATE TABLE IF NOT EXISTS issues (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    name TEXT NOT NULL,
    category TEXT, -- 'economy', 'education', 'public safety', etc.
    description TEXT,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);

-- Candidate Positions on Issues
CREATE TABLE IF NOT EXISTS candidate_positions (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    candidate_id UUID REFERENCES candidates(id),
    issue_id UUID REFERENCES issues(id),
    position TEXT NOT NULL, -- 'support', 'oppose', 'neutral', 'mixed', 'unknown'
    statement TEXT, -- candidate's own words or summary
    source_url TEXT,
    source_date DATE,
    confidence TEXT DEFAULT 'medium', -- 'high', 'medium', 'low' - how certain we are
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    UNIQUE(candidate_id, issue_id)
);

-- Endorsements
CREATE TABLE IF NOT EXISTS endorsements (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    candidate_id UUID REFERENCES candidates(id),
    endorser_name TEXT NOT NULL,
    endorser_type TEXT, -- 'individual', 'organization', 'newspaper', 'politician'
    endorser_title TEXT,
    date DATE,
    quote TEXT,
    source_url TEXT,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);

-- News/Articles about candidates or races
CREATE TABLE IF NOT EXISTS news_items (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    candidate_id UUID REFERENCES candidates(id),
    race_id UUID REFERENCES races(id),
    headline TEXT NOT NULL,
    source TEXT,
    source_url TEXT,
    published_date DATE,
    summary TEXT,
    sentiment TEXT, -- 'positive', 'negative', 'neutral'
    tags TEXT[],
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);

-- Create indexes for common queries
CREATE INDEX IF NOT EXISTS idx_elections_date ON elections(election_date);
CREATE INDEX IF NOT EXISTS idx_races_election ON races(election_id);
CREATE INDEX IF NOT EXISTS idx_candidacies_race ON candidacies(race_id);
CREATE INDEX IF NOT EXISTS idx_candidacies_candidate ON candidacies(candidate_id);
CREATE INDEX IF NOT EXISTS idx_positions_candidate ON candidate_positions(candidate_id);
CREATE INDEX IF NOT EXISTS idx_positions_issue ON candidate_positions(issue_id);

-- ============================================================
-- Sample Data: Wilkes County 2026 Elections
-- ============================================================

-- 1. Jurisdiction
INSERT INTO jurisdictions (name, state, county, type) 
VALUES ('Wilkes County', 'NC', 'Wilkes', 'county')
ON CONFLICT DO NOTHING;

-- 2. Elections
INSERT INTO elections (name, election_date, election_type, jurisdiction_id, status, early_voting_start, early_voting_end, registration_deadline)
SELECT 
    'Wilkes County 2026 Primary Election',
    '2026-03-03',
    'primary',
    id,
    'upcoming',
    '2026-02-13',
    '2026-02-28',
    '2026-02-07'
FROM jurisdictions WHERE name = 'Wilkes County'
ON CONFLICT DO NOTHING;

INSERT INTO elections (name, election_date, election_type, jurisdiction_id, status)
SELECT 
    'Wilkes County 2026 General Election',
    '2026-11-03',
    'general',
    id,
    'upcoming'
FROM jurisdictions WHERE name = 'Wilkes County'
ON CONFLICT DO NOTHING;

-- 3. Races
INSERT INTO races (election_id, office, seats_available, party_affiliation, term_length, description)
SELECT 
    e.id, 'Board of Education', 2, 'Non-partisan', '4 years', 'Wilkes County Board of Education - 2 seats available'
FROM elections e WHERE e.name = 'Wilkes County 2026 Primary Election'
ON CONFLICT DO NOTHING;

INSERT INTO races (election_id, office, seats_available, party_affiliation, term_length, description)
SELECT 
    e.id, 'Sheriff', 1, 'Republican', '4 years', 'Wilkes County Sheriff - Republican primary'
FROM elections e WHERE e.name = 'Wilkes County 2026 Primary Election'
ON CONFLICT DO NOTHING;

INSERT INTO races (election_id, office, seats_available, party_affiliation, term_length, description)
SELECT 
    e.id, 'County Commissioner', 2, 'Republican', '4 years', 'Wilkes County Commissioner - Republican primary, 2 seats'
FROM elections e WHERE e.name = 'Wilkes County 2026 Primary Election'
ON CONFLICT DO NOTHING;

-- 4. Issues
INSERT INTO issues (name, category) VALUES
('School Budgets', 'Education'),
('Student Safety', 'Education'),
('Career Preparation', 'Education'),
('Declining Enrollment', 'Education'),
('Rural School Funding', 'Education'),
('Teacher Support', 'Education'),
('Curriculum Reform', 'Education'),
('Family Engagement', 'Education'),
('Faith-Based Education', 'Education'),
('Infrastructure', 'Government'),
('Economic Development', 'Government'),
('Government Transparency', 'Government'),
('Tax Rates', 'Government'),
('Employee Wages', 'Government'),
('Law Enforcement', 'Public Safety'),
('Public Safety', 'Public Safety'),
('Business Recruitment', 'Economy'),
('Agriculture Support', 'Economy'),
('Housing', 'Economy')
ON CONFLICT DO NOTHING;

-- 5. Candidates - Board of Education
INSERT INTO candidates (full_name, occupation, biography, incumbent, party) VALUES
('Rudy Holbrook', 'Businessman', 'Chairman of Wilkes Board of Education. 46+ years in business.', true, 'Non-partisan'),
('Jammie Jolly', 'Educator', '32+ years in education. Former teacher. ASU and ECU graduate.', true, 'Non-partisan'),
('Jose Rivera', 'Pastor, Physician', 'Pastor and physician. Former member of SC Minority Affairs Commission.', false, 'Non-partisan');

-- 6. Candidates - Sheriff
INSERT INTO candidates (full_name, biography, incumbent, party) VALUES
('Chris Shew', 'Incumbent Sheriff', true, 'Republican'),
('Eric Byrd', 'Challenger', false, 'Republican'),
('David Carson', 'Challenger', false, 'Republican'),
('James Dowell', 'Challenger', false, 'Republican'),
('David Gambill Jr.', 'Challenger', false, 'Republican'),
('Sharon Call-Diaz', 'Challenger', false, 'Republican');

-- Update David Carson email
UPDATE candidates SET email = 'wdcarson43@gmail.com' WHERE full_name = 'David Carson';

-- 7. Candidates - County Commissioner
INSERT INTO candidates (full_name, biography, occupation, incumbent, party) VALUES
('Bill Sexton', '3 years as commissioner, 18 years as fire department president', 'Fire Department President', true, 'Republican'),
('Brandon Absher', '37+ years as firefighter and deputy sheriff', 'Firefighter/Deputy Sheriff', false, 'Republican'),
('Howard "H.S." Greene', 'From Deep Gap. ''Common Sense Candidate''', '', false, 'Republican'),
('Mark Mull', '', '', false, 'Republican'),
('Walter Vaughn III', '', '', false, 'Republican'),
('Randy Queen', 'Perennial candidate', '', false, 'Republican'),
('Michael Grant', 'Focus on economic opportunity and jobs', '', false, 'Republican'),
('Keith Elmore', 'Former commissioner (20 years), extensive board experience', 'Former Commissioner', false, 'Republican');

-- 8. Create Candidacies (link candidates to races)
-- Board of Education
INSERT INTO candidacies (candidate_id, race_id, election_id, status)
SELECT c.id, r.id, e.id, 'active'
FROM candidates c, races r, elections e
WHERE c.full_name = 'Rudy Holbrook' AND r.office = 'Board of Education' AND e.name = 'Wilkes County 2026 Primary Election';

INSERT INTO candidacies (candidate_id, race_id, election_id, status)
SELECT c.id, r.id, e.id, 'active'
FROM candidates c, races r, elections e
WHERE c.full_name = 'Jammie Jolly' AND r.office = 'Board of Education' AND e.name = 'Wilkes County 2026 Primary Election';

INSERT INTO candidacies (candidate_id, race_id, election_id, status)
SELECT c.id, r.id, e.id, 'active'
FROM candidates c, races r, elections e
WHERE c.full_name = 'Jose Rivera' AND r.office = 'Board of Education' AND e.name = 'Wilkes County 2026 Primary Election';

-- Sheriff
INSERT INTO candidacies (candidate_id, race_id, election_id, status)
SELECT c.id, r.id, e.id, 'active'
FROM candidates c, races r, elections e
WHERE c.full_name IN ('Chris Shew', 'Eric Byrd', 'David Carson', 'James Dowell', 'David Gambill Jr.', 'Sharon Call-Diaz')
AND r.office = 'Sheriff' AND e.name = 'Wilkes County 2026 Primary Election';

-- County Commissioner
INSERT INTO candidacies (candidate_id, race_id, election_id, status)
SELECT c.id, r.id, e.id, 'active'
FROM candidates c, races r, elections e
WHERE c.full_name IN ('Bill Sexton', 'Brandon Absher', 'Howard "H.S." Greene', 'Mark Mull', 'Walter Vaughn III', 'Randy Queen', 'Michael Grant', 'Keith Elmore')
AND r.office = 'County Commissioner' AND e.name = 'Wilkes County 2026 Primary Election';

-- 9. Add Candidate Positions
-- Rudy Holbrook positions
INSERT INTO candidate_positions (candidate_id, issue_id, position, statement)
SELECT c.id, i.id, 'support', 'Focus on school budgets and fiscal responsibility'
FROM candidates c, issues i WHERE c.full_name = 'Rudy Holbrook' AND i.name = 'School Budgets';

INSERT INTO candidate_positions (candidate_id, issue_id, position, statement)
SELECT c.id, i.id, 'support', 'Prioritizes student safety initiatives'
FROM candidates c, issues i WHERE c.full_name = 'Rudy Holbrook' AND i.name = 'Student Safety';

INSERT INTO candidate_positions (candidate_id, issue_id, position, statement)
SELECT c.id, i.id, 'support', 'Emphasizes career preparation for students'
FROM candidates c, issues i WHERE c.full_name = 'Rudy Holbrook' AND i.name = 'Career Preparation';

-- Jammie Jolly positions
INSERT INTO candidate_positions (candidate_id, issue_id, position, statement)
SELECT c.id, i.id, 'concern', 'Addresses declining enrollment challenges'
FROM candidates c, issues i WHERE c.full_name = 'Jammie Jolly' AND i.name = 'Declining Enrollment';

INSERT INTO candidate_positions (candidate_id, issue_id, position, statement)
SELECT c.id, i.id, 'support', 'Advocates for rural school funding'
FROM candidates c, issues i WHERE c.full_name = 'Jammie Jolly' AND i.name = 'Rural School Funding';

INSERT INTO candidate_positions (candidate_id, issue_id, position, statement)
SELECT c.id, i.id, 'support', 'Supports teachers and staff'
FROM candidates c, issues i WHERE c.full_name = 'Jammie Jolly' AND i.name = 'Teacher Support';

-- Jose Rivera positions
INSERT INTO candidate_positions (candidate_id, issue_id, position, statement)
SELECT c.id, i.id, 'support', 'Advocates for curriculum reform'
FROM candidates c, issues i WHERE c.full_name = 'Jose Rivera' AND i.name = 'Curriculum Reform';

INSERT INTO candidate_positions (candidate_id, issue_id, position, statement)
SELECT c.id, i.id, 'support', 'Emphasizes family engagement in education'
FROM candidates c, issues i WHERE c.full_name = 'Jose Rivera' AND i.name = 'Family Engagement';

INSERT INTO candidate_positions (candidate_id, issue_id, position, statement)
SELECT c.id, i.id, 'support', 'Supports faith-based education approaches'
FROM candidates c, issues i WHERE c.full_name = 'Jose Rivera' AND i.name = 'Faith-Based Education';

-- Bill Sexton positions
INSERT INTO candidate_positions (candidate_id, issue_id, position, statement)
SELECT c.id, i.id, 'support', 'Focus on infrastructure improvements'
FROM candidates c, issues i WHERE c.full_name = 'Bill Sexton' AND i.name = 'Infrastructure';

INSERT INTO candidate_positions (candidate_id, issue_id, position, statement)
SELECT c.id, i.id, 'support', 'Supports economic development initiatives'
FROM candidates c, issues i WHERE c.full_name = 'Bill Sexton' AND i.name = 'Economic Development';

-- Brandon Absher positions
INSERT INTO candidate_positions (candidate_id, issue_id, position, statement)
SELECT c.id, i.id, 'support', 'Advocates for government transparency'
FROM candidates c, issues i WHERE c.full_name = 'Brandon Absher' AND i.name = 'Government Transparency';

INSERT INTO candidate_positions (candidate_id, issue_id, position, statement)
SELECT c.id, i.id, 'concern', 'Focus on tax rate management'
FROM candidates c, issues i WHERE c.full_name = 'Brandon Absher' AND i.name = 'Tax Rates';

INSERT INTO candidate_positions (candidate_id, issue_id, position, statement)
SELECT c.id, i.id, 'support', 'Supports fair employee wages'
FROM candidates c, issues i WHERE c.full_name = 'Brandon Absher' AND i.name = 'Employee Wages';

-- Michael Grant positions
INSERT INTO candidate_positions (candidate_id, issue_id, position, statement)
SELECT c.id, i.id, 'support', 'Focus on economic opportunity and jobs'
FROM candidates c, issues i WHERE c.full_name = 'Michael Grant' AND i.name = 'Economic Development';

-- Keith Elmore positions
INSERT INTO candidate_positions (candidate_id, issue_id, position, statement)
SELECT c.id, i.id, 'support', 'Focus on business recruitment'
FROM candidates c, issues i WHERE c.full_name = 'Keith Elmore' AND i.name = 'Business Recruitment';

INSERT INTO candidate_positions (candidate_id, issue_id, position, statement)
SELECT c.id, i.id, 'support', 'Supports agriculture initiatives'
FROM candidates c, issues i WHERE c.full_name = 'Keith Elmore' AND i.name = 'Agriculture Support';

INSERT INTO candidate_positions (candidate_id, issue_id, position, statement)
SELECT c.id, i.id, 'support', 'Focus on housing issues'
FROM candidates c, issues i WHERE c.full_name = 'Keith Elmore' AND i.name = 'Housing';

-- Sheriff candidates - general positions
INSERT INTO candidate_positions (candidate_id, issue_id, position)
SELECT c.id, i.id, 'support'
FROM candidates c, issues i 
WHERE c.party = 'Republican' AND c.biography LIKE '%Sheriff%'
AND i.name IN ('Law Enforcement', 'Public Safety');

SELECT 'Wilkes County 2026 Election Database Setup Complete!' as status;
