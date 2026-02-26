# Western North Carolina RSS Feeds

Compiled research on free RSS feeds for Western North Carolina and surrounding areas.

---

## ✅ CONFIRMED WORKING FEEDS

### Wilkes County / Local
| Source | RSS URL | Type | Coverage | Notes |
|--------|---------|------|----------|-------|
| Wilkes County Government | `https://www.wilkescounty.net/RSSFeed.aspx?ModID=1&CID=All-news.xml` | Government | Wilkes County | ✅ Reliable, no rate limits |
| Wilkes County Agenda Center | `https://wilkescounty.net/agendacenter` (scrape) | Government | Wilkes County | Direct PDF links |

### Asheville / Buncombe County
| Source | RSS URL | Type | Coverage | Notes |
|--------|---------|------|----------|-------|
| Mountain Xpress | `https://mountainx.com/feed/` | News | Asheville, WNC | Alternative weekly |
| Buncombe County Gov | `https://www.buncombenc.gov/CivicAlerts.aspx?CID=1` | Government | Buncombe County | News flash alerts |
| Black Mountain | `https://www.townofblackmountain.org/CivicAlerts.aspx?CID=1` | Government | Black Mountain | Town news |

### Boone / Watauga County
| Source | RSS URL | Type | Coverage | Notes |
|--------|---------|------|----------|-------|
| Watauga Democrat | `https://www.wataugademocrat.com/rss` | News | Watauga County | May have paywall |
| Appalachian State | Check `news.appstate.edu` | Education | Boone, ASU | University news |

### Statewide / Regional
| Source | RSS URL | Type | Coverage | Notes |
|--------|---------|------|----------|-------|
| NC Department of Insurance | `https://www.ncdoi.gov/ncdoigov-rss-feeds` | Government | NC State | Multiple feeds available |
| NC Legislature | `https://www.ncleg.gov/` (RSS available) | Government | NC State | Bill tracking |
| DigitalNC | `https://www.digitalnc.org/about/news/rss-feeds/` | Archives | NC Historical | Digital heritage |

### Weather / Emergency
| Source | RSS URL | Type | Coverage | Notes |
|--------|---------|------|----------|-------|
| NWS RSS Hub | `https://www.weather.gov/rss/` | Weather | National | Hurricane, severe weather |
| NWS Greenville-Spartanburg | `https://www.weather.gov/gsp/` | Weather | WNC, Upstate SC | Local forecasts |
| NOAA Weather Radio | `https://www.weather.gov/nwr/stations?State=NC` | Emergency | NC | Station listings |

---

## ⚠️ PROBLEMATIC FEEDS (Blocked/Restricted)

| Source | Issue | Alternative |
|--------|-------|-------------|
| Journal Patriot | Rate limited (429) | Email alerts to wilkesbot@wilkesboro.net |
| Wilkes Record | Bot detection (403) | Email forwarding |
| WXII 12 | Geo-blocked (451) | Newsletter subscription |
| Asheville Citizen-Times | Paywall | Limited free articles |
| Winston-Salem Journal | Paywall | Limited free articles |

---

## 🔍 FEEDS TO TEST

These need verification - may work with proper headers/rate limiting:

```
# News
https://www.journalpatriot.com/rss
https://www.thewilkesrecord.com/rss
https://www.citizen-times.com/rss
https://journalnow.com/rss
https://www.wataugademocrat.com/rss

# TV Stations
https://www.wlos.com/rss
https://www.wcnc.com/rss
https://www.wxii12.com/rss

# Universities
https://news.appstate.edu/rss (check if exists)
https://www.unca.edu/news/rss (check if exists)
```

---

## 📋 RECOMMENDED ADDITIONS TO enhanced_populate.py

```python
RSS_SOURCES = [
    # Existing
    {
        "url": "https://www.wilkescounty.net/RSSFeed.aspx?ModID=1&CID=All-news.xml",
        "name": "Wilkes County Government",
        "type": "Gov",
        "delay": 0,
        "enabled": True
    },
    
    # New - Asheville
    {
        "url": "https://mountainx.com/feed/",
        "name": "Mountain Xpress",
        "type": "Local_Media",
        "delay": 5,
        "enabled": True
    },
    
    # New - Buncombe County
    {
        "url": "https://www.buncombenc.gov/CivicAlerts.aspx?CID=1",
        "name": "Buncombe County Government",
        "type": "Gov",
        "delay": 5,
        "enabled": True
    },
    
    # New - Weather
    {
        "url": "https://www.weather.gov/rss/",
        "name": "National Weather Service",
        "type": "Gov",
        "delay": 10,
        "enabled": True
    },
    
    # Disabled - require email fallback
    {
        "url": "https://www.journalpatriot.com/rss",
        "name": "Journal Patriot",
        "type": "Local_Media",
        "delay": 15,
        "enabled": False,
        "fallback_method": "email_submissions",
        "note": "Rate limited - use email alerts"
    },
]
```

---

## 📧 EMAIL ALERT SUBSCRIPTIONS (For Blocked Sources)

Set up email forwarding to `wilkesbot@wilkesboro.net`:

1. **Journal Patriot** - Sign up at journalpatriot.com for daily digest
2. **Wilkes Record** - Newsletter subscription
3. **WXII 12** - Breaking news alerts
4. **Asheville Citizen-Times** - Daily headlines
5. **Winston-Salem Journal** - Morning newsletter

---

## 🔧 NEXT STEPS

1. Test each feed URL with `python3 enhanced_populate.py`
2. Add working feeds to RSS_SOURCES list
3. Set up email forwarding for blocked sources
4. Consider RSS-Bridge for Facebook groups (self-hosted)

---

*Compiled: 2026-02-25*
