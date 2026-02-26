# Calendar Integration Guide for Wilkesboro Today

## Recommended: Google Calendar (Best Overall)

### Why Google Calendar?
- ✅ Free
- ✅ Embeddable on your website
- ✅ Public sharing
- ✅ iCal/ICS export
- ✅ Mobile apps
- ✅ Easy to manage
- ✅ Works with AITable

---

## Setup Options

### Option 1: Google Calendar (Recommended)

**Step 1: Create Calendar**
1. Go to https://calendar.google.com
2. Click "+" next to "Other calendars"
3. Select "Create new calendar"
4. Name: "Wilkesboro Community Events"
5. Make it **public** (for website embedding)

**Step 2: Get Embed Code**
1. Click the 3 dots next to your calendar
2. Select "Settings and sharing"
3. Scroll to "Integrate calendar"
4. Copy the "Embed code" (iframe)

**Step 3: Add to Website**
```html
<iframe 
  src="https://calendar.google.com/calendar/embed?src=YOUR_CALENDAR_ID&ctz=America/New_York"
  style="border: 0" 
  width="100%" 
  height="600" 
  frameborder="0" 
  scrolling="no"
></iframe>
```

---

### Option 2: Add Events from AITable

**Manual Export (One-time):**
1. In AITable, go to Events datasheet
2. Filter for upcoming events
3. Export as CSV
4. Import to Google Calendar

**Automatic Sync (Better):**
Use Zapier or Make.com:
- Trigger: New record in AITable Events
- Action: Create event in Google Calendar

**Zapier Setup:**
1. https://zapier.com
2. Create Zap: AITable → Google Calendar
3. Trigger: "New Record" in Events table
4. Action: "Create Detailed Event"
5. Map fields:
   - Title → Event Title
   - Date_Start → Start Date
   - Time_Start → Start Time
   - Venue_Name → Location
   - Description → Description

---

### Option 3: Self-Hosted Calendar (Advanced)

**FullCalendar.js** - JavaScript calendar library
- Embeds directly in Astro site
- Pulls from AITable API
- No Google dependency

**Pros:**
- Complete control
- Matches your design
- No external service

**Cons:**
- More complex setup
- Need to build UI

---

## Current Events to Add

From your AITable, here are upcoming events to add:

| Event | Date | Time | Location |
|-------|------|------|----------|
| Board of Commissioners Meeting | Mar 5, 2026 | 5:00 PM | Wilkesboro |
| Food Truck Fridays | Mar 6, 2026 | 5:00 PM | Downtown North Wilkesboro |
| NASCAR Craftsman Truck Series | Jul 18, 2026 | TBD | North Wilkesboro Speedway |
| NASCAR Cup Series | Jul 19, 2026 | TBD | North Wilkesboro Speedway |
| Wilkes County Agricultural Fair | Oct 1-4, 2026 | All day | Fairgrounds |

---

## Quick Implementation

### 1. Create Google Calendar (5 minutes)
- Create account
- Make public calendar
- Copy embed URL

### 2. Add to Astro Site (10 minutes)
Create `src/pages/events.astro`:
```astro
---
import Layout from '../layouts/Layout.astro';
---

<Layout>
  <div class="max-w-6xl mx-auto px-4 py-8">
    <h1 class="text-3xl font-bold mb-6">Community Events</h1>
    
    <div class="bg-white rounded-xl shadow-sm overflow-hidden">
      <iframe 
        src="https://calendar.google.com/calendar/embed?src=YOUR_ID&ctz=America/New_York"
        style="border: 0" 
        width="100%" 
        height="700" 
        frameborder="0" 
        scrolling="no"
        class="w-full"
      ></iframe>
    </div>
    
    <div class="mt-6 text-center">
      <a 
        href="https://calendar.google.com/calendar/ical/YOUR_ID/public/basic.ics"
        class="inline-flex items-center px-4 py-2 bg-primary text-white rounded-lg"
      >
        📅 Subscribe to Calendar
      </a>
    </div>
  </div>
</Layout>
```

### 3. Auto-Sync with Zapier (15 minutes)
- Connect AITable → Google Calendar
- All new events auto-appear

---

## Alternative Calendars

| Calendar | Best For | Cost |
|----------|----------|------|
| **Google Calendar** | General use, embedding | Free |
| **Outlook Calendar** | Microsoft ecosystem | Free |
| **Apple Calendar** | Apple users | Free |
| **Calendly** | Event scheduling | Free tier |
| **Eventbrite** | Ticketed events | Free tier |
| **FullCalendar** | Custom integration | Free (OSS) |

---

## My Recommendation

**Use Google Calendar + Zapier:**
1. Easy to manage
2. Embeds perfectly in Astro
3. Auto-syncs from AITable
4. Free forever
5. Users can subscribe

Want me to:
1. Set up the Google Calendar embed code?
2. Create the events page for your site?
3. Set up the Zapier automation?
4. Show you how to manually import current events?