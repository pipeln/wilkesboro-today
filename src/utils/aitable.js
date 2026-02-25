// AITable API Configuration
export const AITABLE_CONFIG = {
  baseUrl: 'https://api.aitable.ai/fusion/v1',
  token: import.meta.env.AITABLE_TOKEN || 'uskNPM9fPVHOgAGbDepyKER',
  datasheets: {
    news: 'dstjSJ3rvilwBd3Bae',
    events: 'dstnnbs9qm9DZJkt8L',
    resources: 'dstRRB7Fi8ZVP7eRcS',
    submissions: 'dstD2x1pp48NxsMCjs'
  }
};

// API Helper Functions
export async function fetchAITableRecords(datasheetId, options = {}) {
  const { maxRecords = 100, view, filterByFormula } = options;
  
  const params = new URLSearchParams();
  if (maxRecords) params.append('pageSize', maxRecords.toString());
  if (view) params.append('viewId', view);
  
  const url = `${AITABLE_CONFIG.baseUrl}/datasheets/${datasheetId}/records?${params}`;
  
  try {
    const response = await fetch(url, {
      headers: {
        'Authorization': `Bearer ${AITABLE_CONFIG.token}`,
        'Content-Type': 'application/json'
      }
    });
    
    if (!response.ok) {
      throw new Error(`AITable API error: ${response.status}`);
    }
    
    const data = await response.json();
    return data.data?.records || [];
  } catch (error) {
    console.error('Error fetching from AITable:', error);
    return [];
  }
}

// Fetch News Articles
export async function getNewsArticles(limit = 10) {
  const records = await fetchAITableRecords(AITABLE_CONFIG.datasheets.news, {
    maxRecords: limit
  });
  
  if (!records || records.length === 0) {
    return [];
  }
  
  return records.map(record => ({
    id: record.recordId,
    title: record.fields.Title_Original || record.fields.Title || 'Untitled',
    summary: record.fields.Summary_Short || (record.fields.Body_Original ? record.fields.Body_Original.substring(0, 200) : ''),
    body: record.fields.Body_Original || '',
    category: record.fields.Category || 'Community',
    source: record.fields.Source_Name || 'Unknown',
    sourceUrl: record.fields.Source_URL,
    date: record.fields.Date_Original || new Date().toISOString(),
    location: record.fields.Location || 'Wilkes County',
    slug: slugify(record.fields.Title_Original || record.fields.Title)
  }));
}

// Fetch Events
export async function getEvents(limit = 10) {
  const records = await fetchAITableRecords(AITABLE_CONFIG.datasheets.events, {
    maxRecords: limit
  });
  
  if (!records || records.length === 0) {
    return [];
  }
  
  return records.map(record => ({
    id: record.recordId,
    title: record.fields.Title || 'Untitled Event',
    description: record.fields.Description || '',
    date: record.fields.Date_Start || new Date().toISOString().split('T')[0],
    time: record.fields.Time_Start || 'TBD',
    venue: record.fields.Venue_Name || 'TBD',
    address: record.fields.Venue_Address || '',
    city: record.fields.City || 'Wilkes County',
    organizer: record.fields.Organizer_Name || '',
    sourceUrl: record.fields.Source_URL || ''
  }));
}

// Fetch Resources
export async function getResources(category = null) {
  const options = {};
  if (category) {
    options.filterByFormula = `{Category} = '${category}'`;
  }
  
  const records = await fetchAITableRecords(AITABLE_CONFIG.datasheets.resources, options);
  
  return records.map(record => ({
    id: record.recordId,
    name: record.fields.Name,
    type: record.fields.Type,
    description: record.fields.Short_Description,
    address: record.fields.Address,
    city: record.fields.City,
    phone: record.fields.Phone,
    email: record.fields.Email,
    website: record.fields.Website,
    hours: record.fields.Hours,
    topics: record.fields.Topics
  }));
}

// Helper: Create URL-friendly slug
function slugify(text) {
  if (!text) return 'untitled';
  return text
    .toString()
    .toLowerCase()
    .trim()
    .replace(/\s+/g, '-')
    .replace(/[^\w\-]+/g, '')
    .replace(/\-\-+/g, '-');
}