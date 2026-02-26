# Advertising Templates for Wilkesboro Today

## Available Ad Sizes

| Size Name | Dimensions | Best For | File |
|-----------|-----------|----------|------|
| **Leaderboard** | 728x90 | Top of page, header | `leaderboard.png` |
| **Medium Rectangle** | 300x250 | Sidebar, content area | `medium-rectangle.png` |
| **Large Rectangle** | 336x280 | Content area, in-article | `large-rectangle.png` |
| **Half Page** | 300x600 | Sidebar, high visibility | `half-page.png` |
| **Skyscraper** | 160x600 | Narrow sidebar | `skyscraper.png` |
| **Billboard** | 970x250 | Large header, premium placement | `billboard.png` |

## Using in Your Website

### Astro Component

```astro
---
import AdBanner from '../components/AdBanner.astro';
---

<!-- Sidebar ad -->
<AdBanner size="medium-rectangle" />

<!-- Header banner -->
<AdBanner size="leaderboard" />

<!-- Tall sidebar -->
<AdBanner size="skyscraper" />
```

### Direct HTML

```html
<!-- Leaderboard -->
<a href="/advertise">
  <img src="/ads/leaderboard.png" alt="Advertise Here" width="728" height="90">
</a>

<!-- Medium Rectangle -->
<a href="/advertise">
  <img src="/ads/medium-rectangle.png" alt="Advertise Here" width="300" height="250">
</a>
```

## Customizing Templates

The SVG source files are editable:
- Open in Illustrator, Figma, or Inkscape
- Modify colors, text, layout
- Export to PNG at specified dimensions

## Ad Placement Guidelines

### Above the Fold (Premium)
- Leaderboard (728x90) - Header
- Billboard (970x250) - Below header

### Sidebar (Standard)
- Skyscraper (160x600) - Narrow sidebar
- Half Page (300x600) - Wide sidebar
- Medium Rectangle (300x250) - Sidebar

### Content Area (Contextual)
- Large Rectangle (336x280) - Between articles
- Medium Rectangle (300x250) - In-article

## Contact for Advertising

Email: advertise@wilkesborotoday.com

## Rates

| Placement | Size | Monthly Rate |
|-----------|------|-------------|
| Header | Leaderboard | $500 |
| Sidebar (top) | Half Page | $400 |
| Sidebar | Skyscraper | $300 |
| In-article | Medium Rectangle | $250 |
| Footer | Leaderboard | $200 |

Contact us for custom packages and long-term rates.
