# Supabase Migration Guide

## Step 1: Create Supabase Account

1. Go to https://supabase.com
2. Click "Start your project"
3. Sign up with GitHub or email
4. Create a new organization
5. Create a new project
   - Name: `wilkesboro-today`
   - Database password: (save this!)
   - Region: US East (N. Virginia) or closest to you

## Step 2: Get API Keys

After project is created (takes 2-3 minutes):

1. Go to Project Settings (gear icon)
2. Click **API** in left sidebar
3. Copy these values:
   - **URL** (Project URL)
   - **anon public** (anon key)

## Step 3: Add to Your Code

Create `.env` file in website-design folder:

```
SUPABASE_URL=https://your-project.supabase.co
SUPABASE_ANON_KEY=your-anon-key
```

## Step 4: Install Supabase Client

```bash
cd /root/.openclaw/workspace/website-design
npm install @supabase/supabase-js
```

## Step 5: Create Database Tables

In Supabase dashboard:

1. Click **Table Editor** (left sidebar)
2. Click **New Table**
3. Create `articles` table:

```sql
create table articles (
  id uuid default uuid_generate_v4() primary key,
  title text not null,
  summary text,
  body text,
  category text,
  source_name text,
  source_url text,
  image_url text,
  status text default 'draft',
  created_at timestamp with time zone default timezone('utc'::text, now()),
  published_at timestamp with time zone
);
```

4. Create `events` table:

```sql
create table events (
  id uuid default uuid_generate_v4() primary key,
  title text not null,
  description text,
  date_start date,
  date_end date,
  time_start text,
  time_end text,
  venue_name text,
  venue_address text,
  city text,
  organizer_name text,
  source_url text,
  image_url text,
  status text default 'draft',
  created_at timestamp with time zone default timezone('utc'::text, now())
);
```

## Step 6: Import Data from AITable

### Option A: Manual CSV Export
1. In AITable: Export each table to CSV
2. In Supabase: Table Editor → Import Data → Upload CSV

### Option B: Migration Script

Create `migrate_to_supabase.py`:

```python
import requests
from supabase import create_client

# Your keys
SUPABASE_URL = "your-url"
SUPABASE_KEY = "your-anon-key"
AITABLE_TOKEN = "uskNPM9fPVHOgAGbDepyKER"

# Connect to Supabase
supabase = create_client(SUPABASE_URL, SUPABASE_KEY)

# Fetch from AITable
url = "https://api.aitable.ai/fusion/v1/datasheets/dstjSJ3rvilwBd3Bae/records"
headers = {"Authorization": f"Bearer {AITABLE_TOKEN}"}
response = requests.get(url, headers=headers)
data = response.json()

# Transform and insert
for record in data['data']['records']:
    fields = record['fields']
    article = {
        'title': fields.get('Title_Original'),
        'summary': fields.get('Summary_Short'),
        'body': fields.get('Body_Original'),
        'category': fields.get('Category'),
        'source_name': fields.get('Source_Name'),
        'source_url': fields.get('Source_URL'),
        'status': fields.get('Status', 'draft').lower()
    }
    
    # Insert to Supabase
    supabase.table('articles').insert(article).execute()
    print(f"Migrated: {article['title'][:50]}...")

print("Migration complete!")
```

## Step 7: Update Your Website Code

Create `src/utils/supabase.js`:

```javascript
import { createClient } from '@supabase/supabase-js'

const supabaseUrl = import.meta.env.SUPABASE_URL
const supabaseKey = import.meta.env.SUPABASE_ANON_KEY

export const supabase = createClient(supabaseUrl, supabaseKey)

// Fetch articles
export async function getArticles(limit = 10) {
  const { data, error } = await supabase
    .from('articles')
    .select('*')
    .eq('status', 'published')
    .order('published_at', { ascending: false })
    .limit(limit)
  
  if (error) throw error
  return data
}

// Fetch single article
export async function getArticle(id) {
  const { data, error } = await supabase
    .from('articles')
    .select('*')
    .eq('id', id)
    .single()
  
  if (error) throw error
  return data
}

// Fetch events
export async function getEvents(limit = 10) {
  const { data, error } = await supabase
    .from('events')
    .select('*')
    .eq('status', 'approved')
    .order('date_start', { ascending: true })
    .limit(limit)
  
  if (error) throw error
  return data
}
```

## Step 8: Update Astro Files

In your `.astro` files, replace AITable calls:

```javascript
// OLD (AITable)
import { getNewsArticles } from '../utils/aitable'
const articles = await getNewsArticles(6)

// NEW (Supabase)
import { getArticles } from '../utils/supabase'
const articles = await getArticles(6)
```

## Step 9: Set Environment Variables in Cloudflare

1. Go to Cloudflare dashboard
2. Pages → wilkesboro-today → Settings → Environment variables
3. Add:
   - `SUPABASE_URL`
   - `SUPABASE_ANON_KEY`

## Step 10: Deploy

```bash
git add .
git commit -m "Migrate from AITable to Supabase"
git push
```

## Need Help?

Supabase docs: https://supabase.com/docs
Community Discord: https://discord.supabase.com
