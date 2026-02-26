# North Carolina State News RSS Feeds

Complete list of RSS feeds for NC state news coverage, including local, regional, and statewide sources.

---

## 📍 LOCAL / WILKES COUNTY

| Source | RSS URL | Type | Status |
|--------|---------|------|--------|
| Wilkes County Government | `https://www.wilkescounty.net/RSSFeed.aspx?ModID=1&CID=All-news.xml` | Gov | ✅ Working |
| Journal Patriot | `https://www.journalpatriot.com/search/?f=rss&t=article&c=news/local*&l=10&s=start_time&sd=desc` | News | ⚠️ Rate limited |
| Wilkes Record | `https://www.thewilkesrecord.com/search/?f=rss&t=article&c=news*&l=10&s=start_time&sd=desc` | News | ⚠️ Bot detection |
| WXII 12 News | `https://www.wxii12.com/wilkes-county/rss` | News | ❌ Geo-blocked |

---

## 📍 ASHEVILLE / WESTERN NC

| Source | RSS URL | Type | Status |
|--------|---------|------|--------|
| Mountain Xpress | `https://mountainx.com/feed/` | News | ✅ Working |
| Buncombe County Gov | `https://www.buncombenc.gov/CivicAlerts.aspx?CID=1` | Gov | ✅ Working |
| Asheville Citizen-Times | `https://www.citizen-times.com/rss` | News | ⚠️ Paywall |
| WLOS 13 | `https://www.wlos.com/rss` | News | ⚠️ Rate limited |

---

## 📍 BOONE / WATAUGA

| Source | RSS URL | Type | Status |
|--------|---------|------|--------|
| Watauga Democrat | `https://www.wataugademocrat.com/rss` | News | ✅ Working |
| Appalachian State | Check `news.appstate.edu` | Education | 🔍 To test |

---

## 📍 CHARLOTTE

| Source | RSS URL | Type | Status |
|--------|---------|------|--------|
| WCNC Charlotte | `https://www.wcnc.com/rss` | News | ✅ Working |
| Charlotte Observer | `https://www.charlotteobserver.com/news/local/rss` | News | ⚠️ Paywall |
| WBTV 3 | `https://www.wbtv.com/rss` | News | 🔍 To test |
| WSOC 9 | `https://www.wsoctv.com/rss` | News | 🔍 To test |

---

## 📍 WINSTON-SALEM / GREENSBORO

| Source | RSS URL | Type | Status |
|--------|---------|------|--------|
| Winston-Salem Journal | `https://journalnow.com/rss` | News | ⚠️ Paywall |
| Greensboro News & Record | `https://www.greensboro.com/rss` | News | ⚠️ Paywall |
| WFMY News 2 | `https://www.wfmynews2.com/rss` | News | ✅ Working |
| WXII 12 (Triad) | `https://www.wxii12.com/rss` | News | ❌ Geo-blocked |

---

## 📍 RALEIGH / TRIANGLE

| Source | RSS URL | Type | Status |
|--------|---------|------|--------|
| News & Observer | `https://www.newsobserver.com/news/local/rss` | News | ⚠️ Paywall |
| WRAL | `https://www.wral.com/rss` | News | ✅ Working |
| ABC11 WTVD | `https://abc11.com/rss` | News | ✅ Working |
| CBS 17 | `https://www.cbs17.com/rss` | News | 🔍 To test |
| NC State University | Check `news.ncsu.edu` | Education | 🔍 To test |
| UNC Chapel Hill | Check `unc.edu/news` | Education | 🔍 To test |
| Duke University | Check `today.duke.edu` | Education | 🔍 To test |

---

## 📍 STATEWIDE / NC GOVERNMENT

| Source | RSS URL | Type | Status |
|--------|---------|------|--------|
| NC Legislature | `https://www.ncleg.gov/rss` | Gov | ✅ Working |
| NC Dept of Insurance | `https://www.ncdoi.gov/ncdoigov-rss-feeds` | Gov | ✅ Working |
| NC Governor's Office | Check `governor.nc.gov` | Gov | 🔍 To test |
| NC Department of Health | Check `ncdhhs.gov` | Gov | 🔍 To test |
| NC Board of Elections | `https://www.ncsbe.gov/news/feed` | Gov | ✅ Working |

---

## 🌤️ WEATHER / EMERGENCY

| Source | RSS URL | Type | Status |
|--------|---------|------|--------|
| National Weather Service | `https://www.weather.gov/rss/` | Weather | ✅ Working |
| NWS Greenville-Spartanburg | `https://www.weather.gov/gsp/` | Weather | ✅ WNC coverage |
| NWS Raleigh | `https://www.weather.gov/rah/` | Weather | ✅ Central NC |
| ReadyNC | Check `readync.gov` | Emergency | 🔍 To test |

---

## 📊 SUMMARY BY REGION

| Region | Working | Limited | Blocked | Total |
|--------|---------|---------|---------|-------|
| Wilkes/Local | 1 | 2 | 1 | 4 |
| Asheville/WNC | 2 | 2 | 0 | 4 |
| Boone/Watauga | 1 | 0 | 0 | 1 |
| Charlotte | 1 | 1 | 0 | 2+ |
| Winston/Greensboro | 1 | 2 | 1 | 4 |
| Raleigh/Triangle | 2 | 1 | 0 | 3+ |
| Statewide | 3 | 0 | 0 | 3+ |
| Weather | 3 | 0 | 0 | 3 |

**Total Active Sources: ~15 working feeds**

---

## 🔧 CONFIGURATION

See `enhanced_populate.py` for the full RSS_SOURCES configuration with rate limiting and enable/disable flags.

---

*Last updated: 2026-02-25*
