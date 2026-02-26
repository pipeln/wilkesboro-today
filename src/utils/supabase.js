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

// Fetch articles from Supabase
export async function getArticles(limit = 10, category = null) {
  try {
    let query = supabase
      .from('articles')
      .select('*')
      .eq('status', 'published')
      .order('published_at', { ascending: false })
      .limit(limit);
    
    if (category && category !== 'All') {
      query = query.eq('category', category);
    }
    
    const { data, error } = await query;
    
    if (error) {
      console.error('Supabase error:', error);
      return getDemoArticles(limit);
    }
    
    return data?.map(article => ({
      id: article.id,
      title: article.title,
      summary: article.summary,
      body: article.body,
      category: article.category,
      source: article.source_name,
      sourceUrl: article.source_url,
      image: article.image_url || '/images/default-thumbnail.jpg',
      date: article.published_at || article.created_at,
      slug: article.id
    })) || getDemoArticles(limit);
    
  } catch (e) {
    console.error('Error fetching articles:', e);
    return getDemoArticles(limit);
  }
}

// Fetch single article
export async function getArticle(id) {
  try {
    const { data, error } = await supabase
      .from('articles')
      .select('*')
      .eq('id', id)
      .single();
    
    if (error || !data) {
      console.error('Supabase error:', error);
      return getDemoArticle(id);
    }
    
    return {
      id: data.id,
      title: data.title,
      summary: data.summary,
      body: data.body,
      category: data.category,
      source: data.source_name,
      sourceUrl: data.source_url,
      author: data.source_name || 'Staff',
      image: data.image_url || '/images/default-hero.jpg',
      date: data.published_at || data.created_at
    };
    
  } catch (e) {
    console.error('Error fetching article:', e);
    return getDemoArticle(id);
  }
}

// Fetch events from Supabase
export async function getEvents(limit = 10) {
  try {
    const { data, error } = await supabase
      .from('events')
      .select('*')
      .eq('status', 'approved')
      .order('date_start', { ascending: true })
      .limit(limit);
    
    if (error) {
      console.error('Supabase error:', error);
      return getDemoEvents(limit);
    }
    
    return data?.map(event => ({
      id: event.id,
      title: event.title,
      description: event.description,
      date: event.date_start,
      time: event.time_start,
      venue: event.venue_name,
      address: event.venue_address,
      city: event.city,
      organizer: event.organizer_name,
      sourceUrl: event.source_url
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
      id: 'superintendent-byrd-passes-away',
      title: 'Wilkes County Schools Superintendent Mark Byrd Passes Away',
      summary: 'Superintendent Mark Byrd, 54, was found dead at his residence on February 20. The NCSBI is investigating. Dr. Westley Wood has been appointed interim superintendent.',
      category: 'Breaking',
      source: 'Journal Patriot',
      sourceUrl: 'https://www.journalpatriot.com/news/superintendent-byrd-found-dead-from-apparent-gunshot/article_4367622b-bb8a-55ed-b4ed-2b5a5517f1d1.html',
      date: '2026-02-20',
      image: '/images/default-hero.jpg',
      slug: 'superintendent-byrd-passes-away'
    },
    {
      id: 'commissioners-meeting-march-5',
      title: 'County Commissioners Meeting Rescheduled to March 5',
      summary: 'The Wilkes County Board of Commissioners meeting has been moved from March 3 to Thursday, March 5, 2026 at 5:00 PM.',
      category: 'Government',
      source: 'Wilkes County Gov',
      sourceUrl: 'https://www.wilkescounty.net',
      date: '2026-02-26',
      image: '/images/default-thumbnail.jpg',
      slug: 'commissioners-meeting-march-5'
    },
    {
      id: 'wilkesboro-comic-con-feb-28',
      title: 'Wilkesboro Comic Con Returns February 28',
      summary: 'The annual Wilkesboro Comic Con is back this Saturday with vendors, cosplay, and family-friendly activities.',
      category: 'Events',
      source: 'wilkescomiccon.com',
      sourceUrl: 'https://wilkescomiccon.com',
      date: '2026-02-26',
      image: '/images/default-thumbnail.jpg',
      slug: 'wilkesboro-comic-con-feb-28'
    }
  ];
  return articles.slice(0, limit);
}

function getDemoArticle(id) {
  const articles = {
    'superintendent-byrd-passes-away': {
      id: 'superintendent-byrd-passes-away',
      title: 'Wilkes County Schools Superintendent Mark Byrd Passes Away',
      summary: 'Superintendent Mark Byrd, 54, was found dead at his residence on February 20.',
      body: 'Wilkes County School Superintendent Mark Byrd, 54, was found dead Friday at his residence on Oak Ridge Church Road in Hays from an apparent self-inflicted gunshot wound, according to the Wilkes County Sheriff\'s Office.',
      category: 'Breaking',
      source: 'Journal Patriot',
      sourceUrl: 'https://www.journalpatriot.com/news/superintendent-byrd-found-dead-from-apparent-gunshot/article_4367622b-bb8a-55ed-b4ed-2b5a5517f1d1.html',
      author: 'Journal Patriot Staff',
      image: '/images/default-hero.jpg',
      date: '2026-02-20'
    }
  };
  return articles[id] || articles['superintendent-byrd-passes-away'];
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
