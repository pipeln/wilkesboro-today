import { createClient } from '@supabase/supabase-js';

const supabaseUrl = import.meta.env.SUPABASE_URL || process.env.SUPABASE_URL;
const supabaseKey = import.meta.env.SUPABASE_ANON_KEY || process.env.SUPABASE_ANON_KEY;

if (!supabaseUrl || !supabaseKey) {
  console.warn('Supabase credentials not found. Using demo data.');
}

export const supabase = createClient(
  supabaseUrl || 'https://placeholder.supabase.co',
  supabaseKey || 'placeholder-key'
);

// Fetch articles from Supabase (using news_published table)
export async function getArticles(limit = 10, category = null) {
  try {
    let query = supabase
      .from('news_published')
      .select('*')
      .order('Published_At', { ascending: false })
      .limit(limit);
    
    if (category && category !== 'All') {
      query = query.eq('Category', category);
    }
    
    const { data, error } = await query;
    
    if (error) {
      console.error('Supabase error:', error);
      return getDemoArticles(limit);
    }
    
    return data?.map(article => ({
      id: article.id,
      title: article.Title,
      summary: article.Summary,
      category: article.Category,
      source: 'Wilkesboro Today',
      sourceUrl: article.Source_URL || article.WordPress_URL,
      image: '/images/default-thumbnail.jpg',
      date: article.Published_At,
      slug: article.id
    })) || getDemoArticles(limit);
    
  } catch (e) {
    console.error('Error fetching articles:', e);
    return getDemoArticles(limit);
  }
}

// Fetch single article (from news_raw for full content)
export async function getArticle(id) {
  try {
    const { data, error } = await supabase
      .from('news_raw')
      .select('*')
      .eq('id', id)
      .single();
    
    if (error || !data) {
      console.error('Supabase error:', error);
      return getDemoArticle(id);
    }
    
    return {
      id: data.id,
      title: data.Title_Original,
      summary: data.Summary_Short || data.Body_Original?.substring(0, 200),
      body: data.Body_Original,
      category: data.Category,
      source: data.Source_Name,
      sourceUrl: data.Source_URL,
      author: data.Source_Name || 'Staff',
      image: '/images/default-hero.jpg',
      date: data.Date_Original
    };
    
  } catch (e) {
    console.error('Error fetching article:', e);
    return getDemoArticle(id);
  }
}

// Fetch events from Supabase (using events_full table)
export async function getEvents(limit = 10) {
  try {
    const { data, error } = await supabase
      .from('events_full')
      .select('*')
      .eq('Status', 'Approved')
      .order('Date_Start', { ascending: true })
      .limit(limit);
    
    if (error) {
      console.error('Supabase error:', error);
      return getDemoEvents(limit);
    }
    
    return data?.map(event => ({
      id: event.id,
      title: event.Title,
      description: event.Description,
      date: event.Date_Start,
      time: event.Time_Start,
      venue: event.Venue_Name,
      address: event.Venue_Address,
      city: event.City,
      organizer: event.Organizer_Name,
      sourceUrl: event.Source_URL
    })) || getDemoEvents(limit);
    
  } catch (e) {
    console.error('Error fetching events:', e);
    return getDemoEvents(limit);
  }
}

// Demo data fallback
function getDemoArticles(limit) {
  const articles = [
    {
      id: '1',
      title: 'Wilkes County Schools Superintendent Mark Byrd Passes Away',
      summary: 'Superintendent Mark Byrd, 54, was found dead at his residence on February 20. The NCSBI is investigating. Dr. Westley Wood has been appointed interim superintendent.',
      category: 'Breaking',
      source: 'Journal Patriot',
      sourceUrl: 'https://www.journalpatriot.com',
      date: '2026-02-20',
      image: '/images/default-hero.jpg',
      slug: '1'
    },
    {
      id: '2',
      title: 'County Commissioners Meeting Rescheduled to March 5',
      summary: 'The Wilkes County Board of Commissioners meeting has been moved from March 3 to Thursday, March 5, 2026 at 5:00 PM.',
      category: 'Government',
      source: 'Wilkes County Gov',
      sourceUrl: 'https://www.wilkescounty.net',
      date: '2026-02-26',
      image: '/images/default-thumbnail.jpg',
      slug: '2'
    }
  ];
  return articles.slice(0, limit);
}

function getDemoArticle(id) {
  return {
    id: id,
    title: 'Article Not Found',
    summary: 'This article could not be loaded.',
    body: 'Please try again later.',
    category: 'News',
    source: 'Wilkesboro Today',
    sourceUrl: '/',
    author: 'Staff',
    image: '/images/default-hero.jpg',
    date: new Date().toISOString()
  };
}

function getDemoEvents(limit) {
  const events = [
    {
      id: '1',
      title: 'Wilkes County Board of Commissioners Meeting',
      date: '2026-03-05',
      time: '5:00 PM',
      venue: '110 North Street, Wilkesboro',
      city: 'Wilkesboro'
    },
    {
      id: '2',
      title: 'NC Primary Election Day',
      date: '2026-03-03',
      time: '6:30 AM - 7:30 PM',
      venue: 'Various polling locations',
      city: 'Wilkes County'
    }
  ];
  return events.slice(0, limit);
}
