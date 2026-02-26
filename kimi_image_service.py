#!/usr/bin/env python3
"""
Kimi Image Generation Service
Uses Kimi API to generate images for news articles
"""

import requests
import json
import os
import re
from datetime import datetime

# Configuration
KIMI_API_KEY = os.environ.get('KIMI_API_KEY', '')
KIMI_API_URL = "https://api.moonshot.cn/v1/chat/completions"

AITABLE_TOKEN = os.environ.get('AITABLE_TOKEN', 'uskNPM9fPVHOgAGbDepyKER')
AITABLE_BASE_URL = "https://api.aitable.ai/fusion/v1"
AITABLE_HEADERS = {
    "Authorization": f"Bearer {AITABLE_TOKEN}",
    "Content-Type": "application/json"
}

NEWS_DATASHEET_ID = "dstjSJ3rvilwBd3Bae"


def generate_image_prompt(article_title, article_summary, category):
    """Create an optimized prompt for Kimi image generation."""
    
    # Category-specific visual directions
    category_styles = {
        "Public_Safety": "emergency services scene, police or firefighters in action, dramatic lighting, professional photojournalism",
        "Schools": "education setting, students in classroom, school building exterior, warm natural lighting",
        "Civics": "government building, town hall meeting, civic ceremony, professional architecture photography",
        "Business": "local business storefront, professional office interior, economic development, welcoming atmosphere",
        "Community": "community festival, local gathering, neighborhood event, inclusive diverse crowd",
        "Breaking": "breaking news scene, urgency, professional photojournalism, documentary style"
    }
    
    style = category_styles.get(category, "local news scene, professional photography")
    
    prompt = f"""Generate a professional news hero image for this article:

TITLE: {article_title}
CONTEXT: {article_summary[:300] if article_summary else 'Local news story'}
CATEGORY: {category}

Create a photorealistic image with these specifications:
- Style: {style}
- Aspect ratio: 16:9 widescreen format
- Quality: Professional news photography
- Colors: Deep blue tones (#1e40af) as primary, appropriate accents
- Mood: Trustworthy, professional, community-focused
- No text overlays or watermarks in the image
- Suitable for a local news website hero banner

Generate the image now."""
    
    return prompt


def generate_image_with_kimi(prompt, article_id):
    """Generate image using Kimi API."""
    
    if not KIMI_API_KEY:
        print("Error: KIMI_API_KEY not set")
        return None
    
    headers = {
        "Authorization": f"Bearer {KIMI_API_KEY}",
        "Content-Type": "application/json"
    }
    
    payload = {
        "model": "kimi-latest",  # or specific model with image gen
        "messages": [
            {
                "role": "user",
                "content": prompt
            }
        ],
        "temperature": 0.7,
        "max_tokens": 2000
    }
    
    try:
        response = requests.post(KIMI_API_URL, headers=headers, json=payload, timeout=120)
        
        if response.status_code == 200:
            data = response.json()
            
            # Extract content from response
            content = data.get('choices', [{}])[0].get('message', {}).get('content', '')
            
            # Check if Kimi returned an image URL or markdown image
            # Kimi may return: ![description](image_url) or just a URL
            image_url = None
            
            # Try to extract image URL from markdown
            markdown_match = re.search(r'!\[.*?\]\((https?://[^\s]+)\)', content)
            if markdown_match:
                image_url = markdown_match.group(1)
            else:
                # Try to find any URL that looks like an image
                url_match = re.search(r'(https?://[^\s]+\.(?:png|jpg|jpeg|gif))', content, re.IGNORECASE)
                if url_match:
                    image_url = url_match.group(1)
            
            if image_url:
                print(f"✓ Image URL received: {image_url[:60]}...")
                
                # Download the image
                img_response = requests.get(image_url, timeout=30)
                if img_response.status_code == 200:
                    # Save image
                    output_dir = "/root/.openclaw/workspace/website-design/public/images"
                    os.makedirs(output_dir, exist_ok=True)
                    
                    # Determine extension from content-type or URL
                    content_type = img_response.headers.get('content-type', '')
                    if 'png' in content_type:
                        ext = 'png'
                    elif 'jpeg' in content_type or 'jpg' in content_type:
                        ext = 'jpg'
                    else:
                        ext = 'png'  # default
                    
                    image_path = f"{output_dir}/article-{article_id}.{ext}"
                    with open(image_path, 'wb') as f:
                        f.write(img_response.content)
                    
                    print(f"✓ Image saved: {image_path}")
                    return f"/images/article-{article_id}.{ext}"
                else:
                    print(f"✗ Failed to download image: {img_response.status_code}")
                    return None
            else:
                print(f"⚠ No image URL found in response")
                print(f"Response content: {content[:200]}...")
                return None
        else:
            print(f"API Error: {response.status_code}")
            print(f"Response: {response.text[:200]}")
            return None
            
    except Exception as e:
        print(f"Error generating image: {e}")
        return None


def fetch_articles_needing_images():
    """Fetch approved articles from AITable that need images."""
    url = f"{AITABLE_BASE_URL}/datasheets/{NEWS_DATASHEET_ID}/records"
    
    try:
        response = requests.get(url, headers=AITABLE_HEADERS, params={"pageSize": 10})
        data = response.json()
        records = data.get("data", {}).get("records", [])
        
        articles = []
        for record in records:
            fields = record.get("fields", {})
            # Check if article is approved but has no image
            if (fields.get("Status") == "Approved" and 
                not fields.get("Image_URL") and
                fields.get("Title_Original")):
                
                articles.append({
                    "id": record.get("recordId"),
                    "title": fields.get("Title_Original"),
                    "summary": fields.get("Summary_Short", fields.get("Body_Original", "")),
                    "category": fields.get("Category", "Community"),
                    "date": fields.get("Date_Original")
                })
        
        return articles
    except Exception as e:
        print(f"Error fetching articles: {e}")
        return []


def update_article_image(article_id, image_url):
    """Update AITable record with the generated image URL."""
    url = f"{AITABLE_BASE_URL}/datasheets/{NEWS_DATASHEET_ID}/records"
    
    payload = {
        "records": [{
            "recordId": article_id,
            "fields": {
                "Image_URL": image_url,
                "Notes": f"Image generated by Kimi on {datetime.now().strftime('%Y-%m-%d %H:%M')}"
            }
        }]
    }
    
    try:
        response = requests.patch(url, headers=AITABLE_HEADERS, json=payload)
        return response.status_code == 200
    except Exception as e:
        print(f"Error updating article: {e}")
        return False


def main():
    print("="*60)
    print("KIMI IMAGE GENERATION SERVICE")
    print(f"Started: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print("="*60)
    
    if not KIMI_API_KEY:
        print("\n⚠️  KIMI_API_KEY not set!")
        print("Checking environment...")
        # Try to get from session
        import subprocess
        result = subprocess.run(['echo', '$KIMI_API_KEY'], capture_output=True, text=True)
        print(f"Env check: {result.stdout}")
        return
    
    # Fetch articles needing images
    articles = fetch_articles_needing_images()
    print(f"\nFound {len(articles)} articles needing images")
    
    if not articles:
        print("No articles to process.")
        return
    
    # Process each article
    for article in articles[:2]:  # Limit to 2 per run for testing
        print(f"\n{'='*60}")
        print(f"Processing: {article['title'][:60]}...")
        print(f"Category: {article['category']}")
        
        # Generate prompt
        prompt = generate_image_prompt(
            article['title'],
            article['summary'],
            article['category']
        )
        
        print(f"Prompt length: {len(prompt)} chars")
        
        # Generate image
        image_url = generate_image_with_kimi(prompt, article['id'])
        
        if image_url:
            # Update AITable
            if update_article_image(article['id'], image_url):
                print(f"✓ Updated AITable with image URL")
            else:
                print(f"✗ Failed to update AITable")
        else:
            print(f"✗ Image generation failed")
    
    print(f"\n{'='*60}")
    print("Processing complete")
    print("="*60)


if __name__ == "__main__":
    main()
