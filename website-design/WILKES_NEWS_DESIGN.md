# Wilkes County News Hub - Design Document

## Overview
A modern, fast-loading local news aggregation website for Wilkes County and surrounding areas. Built with Astro for maximum performance.

---

## 🎨 Design System

### Brand Identity
- **Name:** Wilkes County News Hub / Wilkesboro Today
- **Tagline:** "Your community, your news"
- **Tone:** Trustworthy, local, accessible

### Color Palette
```css
:root {
  /* Primary */
  --primary: #1e40af;        /* Deep blue - trust */
  --primary-dark: #1e3a8a;
  --primary-light: #3b82f6;
  
  /* Secondary */
  --secondary: #dc2626;      /* Red - breaking news */
  --accent: #f59e0b;         /* Amber - highlights */
  
  /* Neutral */
  --background: #ffffff;
  --surface: #f8fafc;
  --text-primary: #0f172a;
  --text-secondary: #64748b;
  --border: #e2e8f0;
  
  /* Semantic */
  --success: #10b981;
  --warning: #f59e0b;
  --error: #ef4444;
}
```

### Typography
- **Headings:** Inter (Google Fonts)
- **Body:** Source Serif Pro (readable for news)
- **UI Elements:** Inter

### Layout Grid
- Max width: 1280px
- Columns: 12-column grid
- Gutters: 24px (desktop), 16px (mobile)
- Breakpoints:
  - Mobile: < 640px
  - Tablet: 640px - 1024px
  - Desktop: > 1024px

---

## 📄 Page Structure

### 1. Homepage

```
┌─────────────────────────────────────────┐
│  🔴 BREAKING NEWS BAR (marquee)         │
├─────────────────────────────────────────┤
│  LOGO          NAV    SEARCH  WEATHER  │
├─────────────────────────────────────────┤
│  ┌─────────────────┐  ┌──────────────┐ │
│  │                 │  │              │ │
│  │   HERO STORY    │  │   TOP 5      │ │
│  │   (featured)    │  │   NEWS       │ │
│  │                 │  │              │ │
│  └─────────────────┘  └──────────────┘ │
├─────────────────────────────────────────┤
│  LATEST NEWS          EVENTS           │
│  ┌────┐┌────┐┌────┐  ┌──────────────┐ │
│  │    ││    ││    │  │ • Event 1    │ │
│  │    ││    ││    │  │ • Event 2    │ │
│  └────┘└────┘└────┘  │ • Event 3    │ │
│  ┌────┐┌────┐┌────┐  └──────────────┘ │
│  │    ││    ││    │                   │
│  └────┘└────┘└────┘  WEATHER WIDGET   │
├─────────────────────────────────────────┤
│  RESOURCES          NEWSLETTER         │
│  • Housing          [Email________][Go]│
│  • Food/Shelter                        │
│  • Jobs                                │
├─────────────────────────────────────────┤
│  FOOTER                                │
│  About | Contact | Advertise | Terms   │
└─────────────────────────────────────────┘
```

### 2. Article Page

```
┌─────────────────────────────────────────┐
│  BREAKING NEWS BAR                     │
├─────────────────────────────────────────┤
│  NAVIGATION                            │
├─────────────────────────────────────────┤
│  Breadcrumb: Home > News > Local       │
├─────────────────────────────────────────┤
│  ┌──────────────────────────────────┐  │
│  │  ARTICLE TITLE                   │  │
│  │  By Author | Date | Category     │  │
│  │                                  │  │
│  │  [Featured Image]                │  │
│  │                                  │  │
│  │  Article content...              │  │
│  │                                  │  │
│  │  Source: Journal Patriot         │  │
│  └──────────────────────────────────┘  │
├─────────────────────────────────────────┤
│  💬 COMMENTS SECTION                   │
│  [Login to comment] or [Comment form]  │
├─────────────────────────────────────────┤
│  RELATED ARTICLES                      │
│  ┌────┐┌────┐┌────┐                   │
│  └────┘└────┘└────┘                   │
├─────────────────────────────────────────┤
│  FOOTER                                │
└─────────────────────────────────────────┘
```

### 3. Events Page

```
┌─────────────────────────────────────────┐
│  NAVIGATION                            │
├─────────────────────────────────────────┤
│  COMMUNITY EVENTS CALENDAR             │
│  [Month View] [List View] [Submit]     │
├─────────────────────────────────────────┤
│  ┌──────────────────────────────────┐  │
│  │  Calendar Grid or List           │  │
│  │  • Mar 5 - Commissioners Meeting │  │
│  │  • Mar 6 - Food Truck Friday     │  │
│  └──────────────────────────────────┘  │
│  [Load More]                           │
└─────────────────────────────────────────┘
```

### 4. Resources Directory

```
┌─────────────────────────────────────────┐
│  NAVIGATION                            │
├─────────────────────────────────────────┤
│  COMMUNITY RESOURCES                   │
│  [Filter: All | Housing | Food | Jobs] │
├─────────────────────────────────────────┤
│  ┌────────────┐┌────────────┐          │
│  │ 🏠 Housing ││ 🍽️ Food    │          │
│  │ • Shelter  ││ • Kitchen  │          │
│  │ • DSS      ││ • Meals    │          │
│  └────────────┘└────────────┘          │
│  ┌────────────┐┌────────────┐          │
│  │ 💼 Jobs    ││ 🏥 Health  │          │
│  │ • NCWorks  ││ • Clinic   │          │
│  └────────────┘└────────────┘          │
└─────────────────────────────────────────┘
```

---

## 🧩 Components

### 1. Breaking News Bar
- Fixed position, top of page
- Red background, white text
- Auto-rotating marquee
- Click to view full story

### 2. Weather Widget
- Current temp + conditions
- 3-day forecast
- Location: Wilkesboro, NC
- Data from NWS API

### 3. News Card
```
┌─────────────────┐
│ [Image]         │
│ Category        │
│ Headline...     │
│ Date | Source   │
└─────────────────┘
```

### 4. Event Card
```
┌─────────────────┐
│ MAR 5           │
│ 5:00 PM         │
│ Event Title     │
│ Location        │
│ [Add to Cal]    │
└─────────────────┘
```

### 5. Newsletter Signup
```
┌─────────────────────────┐
│ 📧 Get Daily Updates    │
│ [email@example.com    ] │
│ [Subscribe]             │
│ We respect your privacy │
└─────────────────────────┘
```

### 6. Comment System
- Disqus integration (easiest)
- Or: Custom with AITable backend
- Requires user accounts or anonymous

---

## 🔧 Technical Features

### Subscriber System
- Email newsletter via Buttondown or Mailchimp
- Free tier: 1,000-2,500 subscribers
- Daily digest of top stories
- AITable integration for subscriber list

### Advertising
- Google AdSense (easiest)
- Local ad slots (managed in AITable)
- Ad positions:
  - Sidebar (desktop)
  - Between articles (mobile)
  - Footer banner

### Forms
- **News submission:** AITable form embed
- **Event submission:** AITable form embed
- **Contact:** Formspree (free tier)
- **Newsletter:** Buttondown embed

### Comments
- **Option 1:** Disqus (easiest, free)
- **Option 2:** Custom with AITable
- **Option 3:** Giscus (GitHub-based, free)

### Weather
- NWS API (free)
- OpenWeatherMap (free tier)
- Auto-update every hour

---

## 📱 Responsive Behavior

### Mobile (< 640px)
- Single column layout
- Hamburger menu
- Stacked news cards
- Full-width ads

### Tablet (640px - 1024px)
- 2-column news grid
- Sidebar collapses
- Larger touch targets

### Desktop (> 1024px)
- 3-column news grid
- Persistent sidebar
- Weather widget visible
- Ad sidebar

---

## 🚀 Implementation Phases

### Phase 1: Core (Week 1)
- [ ] Astro project setup
- [ ] AITable API integration
- [ ] Homepage layout
- [ ] News article pages
- [ ] Basic styling

### Phase 2: Features (Week 2)
- [ ] Events calendar
- [ ] Resources directory
- [ ] Weather widget
- [ ] Newsletter signup
- [ ] Search functionality

### Phase 3: Engagement (Week 3)
- [ ] Comment system
- [ ] Subscriber management
- [ ] Advertising slots
- [ ] Social sharing
- [ ] Analytics

### Phase 4: Polish (Week 4)
- [ ] Performance optimization
- [ ] SEO improvements
- [ ] Accessibility audit
- [ ] Mobile refinements
- [ ] Launch

---

## 💰 Cost Breakdown

| Item | Cost/Month |
|------|-----------|
| Cloudflare Pages hosting | Free |
| AITable (current plan) | $0 |
| Buttondown (1,000 subs) | Free |
| Disqus comments | Free |
| Weather API (NWS) | Free |
| Formspree (50 subs) | Free |
| **Total** | **$0** |

Optional upgrades:
- Custom domain: $12/year
- Cloudflare Pro: $20/month (optional)
- More subscribers: $9-29/month

---

## 🎨 Design References

**Inspiration sites:**
- Axios (clean, card-based)
- The Local (European local news)
- Patch (hyperlocal news)
- Semafor (modern news layout)

**Key principles:**
- Content first
- Fast loading
- Easy scanning
- Local focus
- Mobile priority

---

*Document version: 1.0*
*Created: 2026-02-25*
