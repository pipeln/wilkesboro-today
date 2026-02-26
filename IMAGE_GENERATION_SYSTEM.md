# Article Image Generation System

## Overview
Automatically generates hero images for news articles that don't have images.

## How It Works

1. **Check AITable** every hour for approved articles without images
2. **Generate prompts** based on article title, category, and summary
3. **Spawn graphics agents** to create images
4. **Save images** to `/public/images/article-{id}.jpg`
5. **Update AITable** with the image URL

## Cron Job

**Job ID:** `faed285b-e2b4-440f-8f39-cfc4b7b39a20e`
**Schedule:** Every hour
**Script:** `generate_article_images.py`

## Image Specifications

| Type | Size | Format | Location |
|------|------|--------|----------|
| Hero | 1200x600 | JPG | `/images/article-{id}.jpg` |
| Thumbnail | 600x400 | JPG | `/images/article-{id}-thumb.jpg` |

## Category-Based Prompts

| Category | Visual Style |
|----------|-------------|
| Public_Safety | Emergency services, police/fire scenes |
| Schools | Education, students, school buildings |
| Civics | Government buildings, town halls |
| Business | Local businesses, storefronts |
| Community | Gatherings, events, neighborhoods |

## Color Scheme
- Primary: Deep blue `#1e40af`
- Accent: Red `#dc2626`
- Style: Professional news photography

## Manual Trigger

```bash
python3 /root/.openclaw/workspace/generate_article_images.py
```

## View Cron Status

```bash
openclaw cron list
```
