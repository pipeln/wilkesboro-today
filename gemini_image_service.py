#!/usr/bin/env python3
"""
Gemini Image Generation Service - Production Ready
Uses Google Gemini API for reliable, cost-effective image generation
"""

import os
import sys
import json
import base64
import requests
from datetime import datetime
from pathlib import Path

# Configuration - Read directly from .env file
def load_env_file(filepath):
    """Simple .env file loader without external dependencies."""
    env_vars = {}
    try:
        with open(filepath, 'r') as f:
            for line in f:
                line = line.strip()
                if line and not line.startswith('#') and '=' in line:
                    key, value = line.split('=', 1)
                    env_vars[key.strip()] = value.strip()
    except Exception as e:
        print(f"Warning: Could not load .env file: {e}")
    return env_vars

# Load from .env file
env_vars = load_env_file('/root/.openclaw/workspace/.env')
GEMINI_API_KEY = env_vars.get('GEMINI_API_KEY', os.environ.get('GEMINI_API_KEY', ''))
GEMINI_API_URL = "https://generativelanguage.googleapis.com/v1beta/models/gemini-2.0-flash-exp-image-generation:generateContent"

AITABLE_TOKEN = os.environ.get('AITABLE_TOKEN', 'uskNPM9fPVHOgAGbDepyKER')
AITABLE_BASE_URL = "https://api.aitable.ai/fusion/v1"
AITABLE_HEADERS = {
    "Authorization": f"Bearer {AITABLE_TOKEN}",
    "Content-Type": "application/json"
}

NEWS_DATASHEET_ID = "dstjSJ3rvilwBd3Bae"
OUTPUT_DIR = "/root/.openclaw/workspace/website-design/public/images"


def log(message, level="INFO"):
    """Log with timestamp and level."""
    timestamp = datetime.now().strftime('%H:%M:%S')
    emoji = {"INFO": "ℹ️", "SUCCESS": "✅", "ERROR": "❌", "WARNING": "⚠️"}.get(level, "ℹ️")
    print(f"[{emoji} {timestamp}] {message}")


def generate_optimized_prompt(title, summary, category):
    """Create an optimized prompt for Gemini image generation."""
    
    # Category-specific visual directions
    category_prompts = {
        "Public_Safety": """
            Scene: Emergency services in action - police officers, firefighters, or EMS responding.
            Atmosphere: Professional, serious, documentary photography style.
            Lighting: Dramatic but respectful, blue and red emergency lights visible.
            Composition: Medium shot showing responders at work, vehicles in background.
        """,
        "Schools": """
            Scene: Education environment - students in modern classroom, school building exterior, or graduation.
            Atmosphere: Hopeful, bright, inspiring, warm natural lighting.
            Colors: School colors, warm tones, clean academic setting.
            Composition: Wide shot showing learning space, students engaged.
        """,
        "Civics": """
            Scene: Government building exterior, town hall meeting room, civic ceremony, or courthouse.
            Atmosphere: Authoritative, professional, dignified, institutional.
            Colors: Deep blues, marble whites, wood tones, American flags if appropriate.
            Composition: Architectural shot or meeting in progress, formal setting.
        """,
        "Business": """
            Scene: Local business storefront, professional office interior, downtown street, or economic development.
            Atmosphere: Welcoming, professional, optimistic, modern.
            Colors: Contemporary blues, clean whites, professional grays.
            Composition: Eye-level shot showing business environment, storefront or office.
        """,
        "Community": """
            Scene: Community festival, farmers market, local gathering, neighborhood event, or parade.
            Atmosphere: Inclusive, warm, celebratory, diverse crowd, friendly.
            Colors: Warm tones, vibrant but tasteful, inviting.
            Composition: Wide shot showing people and activity, community spirit.
        """,
        "Breaking": """
            Scene: Breaking news situation - press conference, news van, emergency response, significant event.
            Atmosphere: Urgent, important, photojournalistic, documentary style.
            Lighting: High contrast, dramatic, professional news photography.
            Composition: Dynamic shot capturing the moment, action-oriented.
        """,
        "Events": """
            Scene: Festival, concert, fair, sports event, or community celebration.
            Atmosphere: Festive, lively, engaging, energetic.
            Colors: Bright, cheerful, event lighting.
            Composition: Wide shot showing event atmosphere, crowd and activities.
        """
    }
    
    visual_direction = category_prompts.get(category, category_prompts["Community"])
    
    prompt = f"""Create a professional news hero image for this article:

TITLE: {title}
CONTEXT: {summary[:250] if summary else 'Local community news story'}
CATEGORY: {category}

VISUAL DIRECTION:
{visual_direction}

TECHNICAL SPECIFICATIONS:
- Aspect ratio: 16:9 widescreen format
- Style: Professional photojournalism, photorealistic, high quality
- Resolution: Suitable for web hero banner (1200+ pixels wide)
- Color palette: Deep professional blue tones as primary, appropriate secondary colors
- Lighting: Professional, well-lit, clear visibility
- Composition: Balanced, news-worthy, engaging
- NO text overlays, watermarks, or captions in the image
- NO people if it would be inappropriate for the news context
- Suitable for a trusted community news website

Generate a single high-quality image that captures the essence of this news story."""

    return prompt


def generate_image_with_gemini(prompt, article_id):
    """Generate image using Gemini API."""
    
    if not GEMINI_API_KEY:
        log("GEMINI_API_KEY not set. Please add it to .env file", "ERROR")
        return None
    
    url = f"{GEMINI_API_URL}?key={GEMINI_API_KEY}"
    
    payload = {
        "contents": [{
            "parts": [{
                "text": prompt
            }]
        }],
        "generationConfig": {
            "temperature": 0.4,
            "topP": 0.8,
            "topK": 40,
            "maxOutputTokens": 2048,
            "responseModalities": ["Text", "Image"]
        }
    }
    
    try:
        log("Sending request to Gemini API...")
        
        response = requests.post(url, json=payload, timeout=120)
        
        if response.status_code != 200:
            log(f"API Error: {response.status_code}", "ERROR")
            log(f"Response: {response.text[:300]}", "ERROR")
            return None
        
        data = response.json()
        
        # Check for image in response
        candidates = data.get('candidates', [])
        if not candidates:
            log("No candidates in response", "ERROR")
            return None
        
        content = candidates[0].get('content', {})
        parts = content.get('parts', [])
        
        for part in parts:
            # Check for inline image data
            if 'inlineData' in part:
                image_data = part['inlineData']['data']
                mime_type = part['inlineData'].get('mimeType', 'image/png')
                
                # Decode base64
                image_bytes = base64.b64decode(image_data)
                
                # Determine extension
                ext = 'png'
                if 'jpeg' in mime_type or 'jpg' in mime_type:
                    ext = 'jpg'
                elif 'webp' in mime_type:
                    ext = 'webp'
                
                # Save image
                os.makedirs(OUTPUT_DIR, exist_ok=True)
                output_path = os.path.join(OUTPUT_DIR, f"article-{article_id}.{ext}")
                
                with open(output_path, 'wb') as f:
                    f.write(image_bytes)
                
                file_size = len(image_bytes)
                log(f"Image saved: {output_path} ({file_size} bytes)", "SUCCESS")
                
                return f"/images/article-{article_id}.{ext}"
            
            # Check for text response (sometimes Gemini returns description)
            elif 'text' in part:
                text = part['text']
                log(f"Gemini returned text: {text[:100]}...", "WARNING")
                
                # Try to extract URL from text
                import re
                url_match = re.search(r'(https?://[^\s\)]+\.(?:png|jpg|jpeg|gif|webp))', text, re.IGNORECASE)
                if url_match:
                    image_url = url_match.group(1)
                    return download_image(image_url, article_id)
        
        log("No image found in response", "ERROR")
        return None
        
    except Exception as e:
        log(f"Error generating image: {e}", "ERROR")
        return None


def download_image(url, article_id):
    """Download image from URL."""
    try:
        log(f"Downloading image from URL...")
        response = requests.get(url, timeout=60)
        
        if response.status_code == 200:
            os.makedirs(OUTPUT_DIR, exist_ok=True)
            output_path = os.path.join(OUTPUT_DIR, f"article-{article_id}.png")
            
            with open(output_path, 'wb') as f:
                f.write(response.content)
            
            log(f"Image downloaded: {output_path}", "SUCCESS")
            return f"/images/article-{article_id}.png"
        else:
            log(f"Failed to download: {response.status_code}", "ERROR")
            return None
            
    except Exception as e:
        log(f"Error downloading image: {e}", "ERROR")
        return None


def fetch_articles_needing_images():
    """Fetch approved articles from AITable that need images."""
    url = f"{AITABLE_BASE_URL}/datasheets/{NEWS_DATASHEET_ID}/records"
    
    try:
        log("Fetching articles from AITable...")
        
        response = requests.get(url, headers=AITABLE_HEADERS, params={"pageSize": 20})
        data = response.json()
        records = data.get("data", {}).get("records", [])
        
        articles = []
        for record in records:
            fields = record.get("fields", {})
            
            # Check if article is approved but has no image
            if (fields.get("Status") in ["Approved", "Published"] and 
                not fields.get("Image_URL") and
                fields.get("Title_Original")):
                
                articles.append({
                    "id": record.get("recordId"),
                    "title": fields.get("Title_Original"),
                    "summary": fields.get("Summary_Short", fields.get("Body_Original", "")),
                    "category": fields.get("Category", "Community"),
                    "date": fields.get("Date_Original")
                })
        
        log(f"Found {len(articles)} articles needing images")
        return articles
        
    except Exception as e:
        log(f"Error fetching articles: {e}", "ERROR")
        return []


def update_article_image(article_id, image_url):
    """Update AITable record with the generated image URL."""
    url = f"{AITABLE_BASE_URL}/datasheets/{NEWS_DATASHEET_ID}/records"
    
    payload = {
        "records": [{
            "recordId": article_id,
            "fields": {
                "Image_URL": image_url,
                "Notes": f"Image generated by Gemini on {datetime.now().strftime('%Y-%m-%d %H:%M')}"
            }
        }]
    }
    
    try:
        response = requests.patch(url, headers=AITABLE_HEADERS, json=payload)
        
        if response.status_code == 200:
            log("AITable updated successfully", "SUCCESS")
            return True
        else:
            log(f"Failed to update AITable: {response.status_code}", "ERROR")
            return False
            
    except Exception as e:
        log(f"Error updating AITable: {e}", "ERROR")
        return False


def main():
    import argparse
    
    parser = argparse.ArgumentParser(description='Gemini Image Generation Service')
    parser.add_argument('--test', action='store_true', help='Test with sample article')
    parser.add_argument('--batch', action='store_true', help='Process all pending articles')
    parser.add_argument('--article-id', help='Specific article ID')
    parser.add_argument('--title', help='Article title')
    parser.add_argument('--summary', default='', help='Article summary')
    parser.add_argument('--category', default='Community', help='Article category')
    
    args = parser.parse_args()
    
    print("="*70)
    print("GEMINI IMAGE GENERATION SERVICE")
    print("Powered by Google Gemini 2.0 Flash")
    print("="*70)
    
    if not GEMINI_API_KEY:
        print("\n❌ GEMINI_API_KEY not set!")
        print("\nTo get your API key:")
        print("1. Go to https://makersuite.google.com/app/apikey")
        print("2. Create a new API key")
        print("3. Add it to /root/.openclaw/workspace/.env:")
        print("   GEMINI_API_KEY=your_key_here")
        return
    
    if args.test:
        log("Running test mode...")
        
        prompt = generate_optimized_prompt(
            "Wilkes County Schools Celebrate Record Graduation Rate",
            "Students and faculty gather to celebrate the highest graduation rate in county history at 93.2%.",
            "Schools"
        )
        
        image_url = generate_image_with_gemini(prompt, "test")
        
        if image_url:
            log(f"Test successful! Image: {image_url}", "SUCCESS")
        else:
            log("Test failed - check API key and try again", "ERROR")
            
    elif args.batch:
        articles = fetch_articles_needing_images()
        
        if not articles:
            log("No articles to process.")
            return
        
        log(f"Processing {len(articles)} articles...")
        
        for i, article in enumerate(articles[:5], 1):
            log(f"\n[{i}/{min(len(articles), 5)}] {article['title'][:50]}...")
            
            prompt = generate_optimized_prompt(
                article['title'],
                article['summary'],
                article['category']
            )
            
            image_url = generate_image_with_gemini(prompt, article['id'])
            
            if image_url:
                update_article_image(article['id'], image_url)
            else:
                log(f"Skipping article {article['id']} - generation failed", "WARNING")
        
        log("\nBatch processing complete", "SUCCESS")
        
    elif args.article_id and args.title:
        prompt = generate_optimized_prompt(args.title, args.summary, args.category)
        image_url = generate_image_with_gemini(prompt, args.article_id)
        
        if image_url:
            update_article_image(args.article_id, image_url)
            log(f"Image generated: {image_url}", "SUCCESS")
        else:
            log("Generation failed", "ERROR")
    else:
        parser.print_help()
        print("\nExamples:")
        print("  python3 gemini_image_service.py --test")
        print("  python3 gemini_image_service.py --batch")
        print("  python3 gemini_image_service.py --article-id 'rec123' --title 'News Title'")


if __name__ == "__main__":
    main()
