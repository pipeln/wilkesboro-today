#!/usr/bin/env python3
"""
Hybrid Image Generation Service
Kimi generates optimized prompts, Gemini generates images
Best of both worlds: Kimi's understanding + Gemini's reliability
"""

import os
import sys
import json
import base64
import requests
from datetime import datetime

# Load environment
def load_env_file(filepath):
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

env_vars = load_env_file('/root/.openclaw/workspace/.env')

# API Keys
KIMI_API_KEY = env_vars.get('KIMI_API_KEY', '')
GEMINI_API_KEY = env_vars.get('GEMINI_API_KEY', '')

# API URLs
KIMI_API_URL = "https://api.moonshot.cn/v1/chat/completions"
GEMINI_API_URL = "https://generativelanguage.googleapis.com/v1beta/models/gemini-2.0-flash-exp-image-generation:generateContent"

# AITable Config
AITABLE_TOKEN = env_vars.get('AITABLE_TOKEN', 'uskNPM9fPVHOgAGbDepyKER')
AITABLE_BASE_URL = "https://api.aitable.ai/fusion/v1"
NEWS_DATASHEET_ID = "dstjSJ3rvilwBd3Bae"

OUTPUT_DIR = "/root/.openclaw/workspace/website-design/public/images"


def log(message, level="INFO"):
    timestamp = datetime.now().strftime('%H:%M:%S')
    emoji = {"INFO": "ℹ️", "SUCCESS": "✅", "ERROR": "❌", "WARNING": "⚠️", "KIMI": "🌙", "GEMINI": "♊"}.get(level, "ℹ️")
    print(f"[{emoji} {timestamp}] {message}")


def kimi_generate_prompt(article_title, article_summary, category):
    """
    Step 1: Kimi generates an optimized, detailed image prompt
    """
    if not KIMI_API_KEY:
        log("KIMI_API_KEY not set, using fallback prompt", "WARNING")
        return generate_fallback_prompt(article_title, article_summary, category)
    
    headers = {
        "Authorization": f"Bearer {KIMI_API_KEY}",
        "Content-Type": "application/json"
    }
    
    system_prompt = """You are an expert prompt engineer for AI image generation.
Your task is to create detailed, optimized prompts for generating news article hero images.

Create prompts that are:
- Highly detailed and specific
- Optimized for photorealistic output
- Appropriate for a local news website
- Free of text, watermarks, or logos
- Professional and trustworthy in tone

Return ONLY the image generation prompt. No explanations, no markdown, just the prompt text."""

    user_prompt = f"""Create an optimized image generation prompt for this news article:

TITLE: {article_title}
CATEGORY: {category}
SUMMARY: {article_summary[:300] if article_summary else 'Local news story'}

Requirements:
- Professional photojournalism style
- 16:9 widescreen format (1200x675 pixels)
- Deep blue color scheme (#1e40af) as appropriate
- No text overlays or watermarks
- Suitable for community news website hero banner
- Photorealistic, high quality

Generate a detailed prompt that will create the perfect hero image for this article."""

    payload = {
        "model": "kimi-k2-5",
        "messages": [
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": user_prompt}
        ],
        "temperature": 0.7,
        "max_tokens": 1000
    }
    
    try:
        log("Asking Kimi to generate optimized prompt...", "KIMI")
        
        response = requests.post(KIMI_API_URL, headers=headers, json=payload, timeout=60)
        
        if response.status_code == 200:
            data = response.json()
            generated_prompt = data.get('choices', [{}])[0].get('message', {}).get('content', '')
            
            # Clean up the prompt
            generated_prompt = generated_prompt.strip()
            
            log(f"Kimi generated prompt ({len(generated_prompt)} chars)", "KIMI")
            log(f"Preview: {generated_prompt[:100]}...", "KIMI")
            
            return generated_prompt
        else:
            log(f"Kimi API error: {response.status_code}", "ERROR")
            return generate_fallback_prompt(article_title, article_summary, category)
            
    except Exception as e:
        log(f"Kimi error: {e}", "ERROR")
        return generate_fallback_prompt(article_title, article_summary, category)


def generate_fallback_prompt(title, summary, category):
    """Fallback prompt if Kimi fails"""
    
    category_styles = {
        "Public_Safety": "emergency services scene with police or firefighters, dramatic lighting, professional photojournalism",
        "Schools": "education environment with students or school building, warm natural lighting, inspiring atmosphere",
        "Civics": "government building or town hall, professional architecture, dignified atmosphere",
        "Business": "local business storefront or professional office, modern and welcoming",
        "Community": "community festival or gathering, diverse crowd, warm and inclusive",
        "Breaking": "breaking news scene, urgent photojournalism, documentary style",
        "Events": "festival or celebration, lively atmosphere, community event"
    }
    
    style = category_styles.get(category, "local news scene, professional photography")
    
    prompt = f"""Professional news hero image for: {title}

Scene description: {style}
Context: {summary[:200] if summary else 'Local community news'}

Technical specifications:
- 16:9 widescreen format, 1200x675 pixels
- Photorealistic, high quality, sharp focus
- Professional photojournalism style
- Deep blue tones (#1e40af) where appropriate
- Well-lit, clear composition
- No text overlays, watermarks, or captions
- Suitable for trusted community news website

Create a compelling hero image that captures the essence of this news story."""

    log("Using fallback prompt", "WARNING")
    return prompt


def gemini_generate_image(prompt, article_id):
    """
    Step 2: Gemini generates the actual image from Kimi's prompt
    """
    if not GEMINI_API_KEY:
        log("GEMINI_API_KEY not set", "ERROR")
        return None
    
    url = f"{GEMINI_API_URL}?key={GEMINI_API_KEY}"
    
    # Enhance the prompt for Gemini
    enhanced_prompt = f"""{prompt}

Additional requirements:
- Generate as a single high-quality image
- No text, logos, or watermarks in the image
- Professional news photography aesthetic
- Ready for web use as hero banner"""

    payload = {
        "contents": [{
            "parts": [{"text": enhanced_prompt}]
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
        log("Sending prompt to Gemini for image generation...", "GEMINI")
        
        response = requests.post(url, json=payload, timeout=120)
        
        if response.status_code != 200:
            log(f"Gemini API error: {response.status_code}", "ERROR")
            if response.status_code == 429:
                log("Rate limit exceeded - waiting for quota reset", "WARNING")
            return None
        
        data = response.json()
        candidates = data.get('candidates', [])
        
        if not candidates:
            log("No candidates in response", "ERROR")
            return None
        
        content = candidates[0].get('content', {})
        parts = content.get('parts', [])
        
        for part in parts:
            if 'inlineData' in part:
                # Extract image
                image_data = part['inlineData']['data']
                mime_type = part['inlineData'].get('mimeType', 'image/png')
                
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
            
            elif 'text' in part:
                text = part['text']
                log(f"Gemini returned text: {text[:100]}...", "WARNING")
        
        log("No image found in Gemini response", "ERROR")
        return None
        
    except Exception as e:
        log(f"Gemini error: {e}", "ERROR")
        return None


def hybrid_generate_image(article_title, article_summary, category, article_id):
    """
    Full hybrid pipeline:
    1. Kimi generates optimized prompt
    2. Gemini generates image from prompt
    """
    log(f"Starting hybrid generation for: {article_title[:50]}...")
    
    # Step 1: Kimi creates the prompt
    optimized_prompt = kimi_generate_prompt(article_title, article_summary, category)
    
    # Step 2: Gemini creates the image
    image_url = gemini_generate_image(optimized_prompt, article_id)
    
    return image_url


def fetch_articles_from_aitable():
    """Fetch articles needing images from AITable"""
    headers = {
        "Authorization": f"Bearer {AITABLE_TOKEN}",
        "Content-Type": "application/json"
    }
    
    url = f"{AITABLE_BASE_URL}/datasheets/{NEWS_DATASHEET_ID}/records"
    
    try:
        log("Fetching articles from AITable...")
        
        response = requests.get(url, headers=headers, params={"pageSize": 20})
        data = response.json()
        records = data.get("data", {}).get("records", [])
        
        articles = []
        for record in records:
            fields = record.get("fields", {})
            
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


def update_aitable_image(article_id, image_url):
    """Update AITable with generated image URL"""
    url = f"{AITABLE_BASE_URL}/datasheets/{NEWS_DATASHEET_ID}/records"
    
    headers = {
        "Authorization": f"Bearer {AITABLE_TOKEN}",
        "Content-Type": "application/json"
    }
    
    payload = {
        "records": [{
            "recordId": article_id,
            "fields": {
                "Image_URL": image_url,
                "Notes": f"Hybrid Kimi+Gemini image generated on {datetime.now().strftime('%Y-%m-%d %H:%M')}"
            }
        }]
    }
    
    try:
        response = requests.patch(url, headers=headers, json=payload)
        return response.status_code == 200
    except Exception as e:
        log(f"Error updating AITable: {e}", "ERROR")
        return False


def main():
    import argparse
    
    parser = argparse.ArgumentParser(description='Hybrid Image Generation (Kimi + Gemini)')
    parser.add_argument('--test', action='store_true', help='Test with sample article')
    parser.add_argument('--batch', action='store_true', help='Process all pending articles')
    parser.add_argument('--article-id', help='Specific article ID')
    parser.add_argument('--title', help='Article title')
    parser.add_argument('--summary', default='', help='Article summary')
    parser.add_argument('--category', default='Community', help='Article category')
    
    args = parser.parse_args()
    
    print("="*70)
    print("HYBRID IMAGE GENERATION SERVICE")
    print("Kimi generates prompts → Gemini generates images")
    print("="*70)
    
    if not GEMINI_API_KEY:
        log("GEMINI_API_KEY not set! Add to .env file", "ERROR")
        return
    
    if args.test:
        log("Running test mode...")
        
        image_url = hybrid_generate_image(
            "Wilkes County Schools Celebrate Record Graduation Rate",
            "Students and faculty gather to celebrate the highest graduation rate in county history at 93.2%. The achievement reflects years of hard work.",
            "Schools",
            "hybrid-test"
        )
        
        if image_url:
            log(f"Test successful! Image: {image_url}", "SUCCESS")
        else:
            log("Test failed", "ERROR")
            
    elif args.batch:
        articles = fetch_articles_from_aitable()
        
        if not articles:
            log("No articles to process")
            return
        
        log(f"Processing {len(articles)} articles...")
        
        for i, article in enumerate(articles[:3], 1):  # Limit to 3
            log(f"\n[{i}/{min(len(articles), 3)}] {article['title'][:50]}...")
            
            image_url = hybrid_generate_image(
                article['title'],
                article['summary'],
                article['category'],
                article['id']
            )
            
            if image_url:
                update_aitable_image(article['id'], image_url)
            else:
                log(f"Failed to generate for article {article['id']}", "WARNING")
        
        log("\nBatch processing complete", "SUCCESS")
        
    elif args.article_id and args.title:
        image_url = hybrid_generate_image(
            args.title,
            args.summary,
            args.category,
            args.article_id
        )
        
        if image_url:
            update_aitable_image(args.article_id, image_url)
            log(f"Success! Image: {image_url}", "SUCCESS")
        else:
            log("Generation failed", "ERROR")
    else:
        parser.print_help()
        print("\nExamples:")
        print("  python3 hybrid_image_service.py --test")
        print("  python3 hybrid_image_service.py --batch")
        print("  python3 hybrid_image_service.py --article-id 'rec123' --title 'News Title'")


if __name__ == "__main__":
    main()
