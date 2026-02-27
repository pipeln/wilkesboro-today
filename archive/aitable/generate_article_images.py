#!/usr/bin/env python3
"""
Article Image Generator - Creates hero images for news articles
Runs via cron to generate images for new articles without images
"""

import requests
import json
import os
from datetime import datetime

API_TOKEN = "uskNPM9fPVHOgAGbDepyKER"
BASE_URL = "https://api.aitable.ai/fusion/v1"
HEADERS = {
    "Authorization": f"Bearer {API_TOKEN}",
    "Content-Type": "application/json"
}

NEWS_DATASHEET_ID = "dstjSJ3rvilwBd3Bae"

def fetch_articles_without_images():
    """Fetch news articles that need images."""
    url = f"{BASE_URL}/datasheets/{NEWS_DATASHEET_ID}/records"
    
    # Filter for articles without images and approved status
    params = {
        "pageSize": 10,
    }
    
    try:
        response = requests.get(url, headers=HEADERS, params=params)
        data = response.json()
        records = data.get("data", {}).get("records", [])
        
        # Filter articles without images
        articles_needing_images = []
        for record in records:
            fields = record.get("fields", {})
            # Check if article has no image field or empty image
            if not fields.get("Image_URL") and fields.get("Status") == "Approved":
                articles_needing_images.append({
                    "id": record.get("recordId"),
                    "title": fields.get("Title_Original", "Untitled"),
                    "summary": fields.get("Summary_Short", fields.get("Body_Original", "")[:100]),
                    "category": fields.get("Category", "Community"),
                    "date": fields.get("Date_Original")
                })
        
        return articles_needing_images
    except Exception as e:
        print(f"Error fetching articles: {e}")
        return []


def generate_image_prompt(article):
    """Generate an image generation prompt based on article content."""
    title = article["title"]
    category = article["category"]
    summary = article["summary"]
    
    # Base style for all images
    base_style = """Professional news photography style, clean composition, 
    suitable for a local news website hero image. Modern, trustworthy aesthetic."""
    
    # Category-specific prompts
    category_prompts = {
        "Public_Safety": f"Emergency services, police or fire department scene related to: {title}. {base_style} Blue and red tones.",
        "Schools": f"Education scene, students or school building related to: {title}. {base_style} Warm, hopeful lighting.",
        "Civics": f"Government building, town hall, or civic scene related to: {title}. {base_style} Professional, authoritative.",
        "Business": f"Local business scene, storefront or office related to: {title}. {base_style} Professional, welcoming.",
        "Community": f"Community gathering, local event, or neighborhood scene related to: {title}. {base_style} Warm, inclusive."
    }
    
    prompt = category_prompts.get(category, f"Local news scene related to: {title}. {base_style}")
    
    # Add title text overlay instruction
    prompt += f""" Include space at bottom for text overlay. 
    Color scheme: Deep blue #1e40af primary, white background elements."""
    
    return prompt


def spawn_image_generation_agent(article):
    """Spawn a subagent to generate the image."""
    prompt = generate_image_prompt(article)
    
    task = f"""Generate a hero image for a news article with the following details:

Title: {article['title']}
Category: {article['category']}
Summary: {article['summary']}

Image Prompt: {prompt}

Requirements:
1. Create a 1200x600 pixel hero image
2. Save as: /root/.openclaw/workspace/website-design/public/images/article-{article['id']}.jpg
3. Also create a 600x400 thumbnail version: /root/.openclaw/workspace/website-design/public/images/article-{article['id']}-thumb.jpg
4. Use the Wilkesboro Today color scheme (deep blue #1e40af, red #dc2626 accents)
5. Include subtle "Wilkesboro Today" watermark or branding
6. Make it professional and news-worthy

If you cannot generate actual image files, create high-quality SVG versions that can be converted.

After creating the images, return the file paths and a brief description of what was created.
"""
    
    # This would spawn a subagent - for now we log the task
    print(f"Would spawn agent for article: {article['title'][:50]}...")
    print(f"Prompt: {prompt[:100]}...")
    
    # In production, this would call the sessions_spawn API
    return {
        "article_id": article["id"],
        "title": article["title"],
        "prompt": prompt,
        "status": "queued"
    }


def update_article_with_image(article_id, image_path):
    """Update AITable record with the generated image URL."""
    url = f"{BASE_URL}/datasheets/{NEWS_DATASHEET_ID}/records"
    
    payload = {
        "records": [{
            "recordId": article_id,
            "fields": {
                "Image_URL": f"/images/{os.path.basename(image_path)}",
                "Notes": f"Image auto-generated on {datetime.now().strftime('%Y-%m-%d %H:%M')}"
            }
        }]
    }
    
    try:
        response = requests.patch(url, headers=HEADERS, json=payload)
        return response.status_code == 200
    except Exception as e:
        print(f"Error updating article: {e}")
        return False


def main():
    print("="*60)
    print("ARTICLE IMAGE GENERATOR")
    print(f"Started: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print("="*60)
    
    # Fetch articles needing images
    articles = fetch_articles_without_images()
    print(f"\nFound {len(articles)} articles needing images")
    
    if not articles:
        print("No articles need images. Exiting.")
        return
    
    # Process each article
    results = []
    for article in articles[:3]:  # Limit to 3 per run to avoid overload
        print(f"\nProcessing: {article['title'][:60]}...")
        result = spawn_image_generation_agent(article)
        results.append(result)
    
    print(f"\n{'='*60}")
    print(f"Queued {len(results)} image generation tasks")
    print("="*60)
    
    # Save queue for processing
    queue_file = "/root/.openclaw/workspace/image_generation_queue.json"
    with open(queue_file, "w") as f:
        json.dump(results, f, indent=2)
    
    print(f"Queue saved to: {queue_file}")


if __name__ == "__main__":
    main()
