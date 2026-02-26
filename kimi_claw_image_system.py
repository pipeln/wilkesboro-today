#!/usr/bin/env python3
"""
KIMI CLAW IMAGE GENERATION SYSTEM
=================================

This system uses Kimi's native image generation capabilities through
the OpenClaw integration. Kimi Claw (that's me) can generate images
directly when properly invoked.

Usage:
    python3 kimi_claw_image_system.py --article-id "article123" --title "News Title"
    
Or for batch processing:
    python3 kimi_claw_image_system.py --batch
"""

import os
import sys
import json
import argparse
import requests
from datetime import datetime

# Configuration
AITABLE_TOKEN = os.environ.get('AITABLE_TOKEN', 'uskNPM9fPVHOgAGbDepyKER')
AITABLE_BASE_URL = "https://api.aitable.ai/fusion/v1"
NEWS_DATASHEET_ID = "dstjSJ3rvilwBd3Bae"
EVENTS_DATASHEET_ID = "dstnnbs9qm9DZJkt8L"

OUTPUT_DIR = "/root/.openclaw/workspace/website-design/public/images"


def log(message):
    """Log with Kimi Claw branding."""
    timestamp = datetime.now().strftime('%H:%M:%S')
    print(f"[❤️‍🔥 Kimi Claw {timestamp}] {message}")


def generate_kimi_image_prompt(article_title, article_summary, category):
    """
    Generate an optimized prompt for Kimi image generation.
    Kimi works best with detailed, descriptive prompts.
    """
    
    # Base style that works well with Kimi
    base_style = """Professional photorealistic news photography, 
    high quality, sharp focus, well-lit, suitable for a local news website hero image.
    Modern, trustworthy, journalistic aesthetic."""
    
    # Category-specific visual elements
    category_elements = {
        "Public_Safety": """
            Scene: Emergency services in action, police officers or firefighters responding to incident.
            Atmosphere: Serious, professional, dramatic but respectful lighting.
            Colors: Deep blue uniforms, red emergency lights, neutral background.
            Composition: Medium shot showing responders at work.
        """,
        "Schools": """
            Scene: Education environment - students in classroom, school building exterior, or graduation ceremony.
            Atmosphere: Hopeful, bright, warm natural lighting.
            Colors: School colors (blue, gold), warm tones, clean whites.
            Composition: Wide shot showing learning environment.
        """,
        "Civics": """
            Scene: Government building exterior, town hall meeting room, or civic ceremony.
            Atmosphere: Authoritative, professional, dignified.
            Colors: Deep blues, marble whites, wood tones.
            Composition: Architectural shot or meeting in progress.
        """,
        "Business": """
            Scene: Local business storefront, professional office, or economic development project.
            Atmosphere: Welcoming, professional, optimistic.
            Colors: Modern blues, clean whites, accent colors.
            Composition: Eye-level shot showing business environment.
        """,
        "Community": """
            Scene: Community festival, local gathering, farmers market, or neighborhood event.
            Atmosphere: Inclusive, warm, celebratory, diverse.
            Colors: Warm tones, vibrant but not overwhelming.
            Composition: Wide shot showing people and activity.
        """,
        "Breaking": """
            Scene: Breaking news situation - press conference, emergency response, or significant event.
            Atmosphere: Urgent, important, photojournalistic.
            Colors: High contrast, dramatic lighting.
            Composition: Dynamic shot capturing the moment.
        """,
        "Events": """
            Scene: Festival, concert, fair, or community celebration.
            Atmosphere: Festive, lively, engaging.
            Colors: Bright, cheerful, inviting.
            Composition: Wide shot showing the event atmosphere.
        """
    }
    
    visual_elements = category_elements.get(category, category_elements["Community"])
    
    prompt = f"""Create a professional news hero image for this article:

ARTICLE TITLE: {article_title}

ARTICLE CONTEXT: {article_summary[:200] if article_summary else 'Local Wilkes County news story'}

CATEGORY: {category}

VISUAL SPECIFICATIONS:
{visual_elements}

TECHNICAL REQUIREMENTS:
- Aspect ratio: 16:9 widescreen format (1200x675 pixels)
- Style: Professional news photography, photorealistic
- Quality: High resolution, sharp details, proper exposure
- Color palette: Deep blue (#1e40af) as primary color, appropriate accents
- No text overlays, watermarks, or captions in the image
- Suitable for a community news website hero banner
- Clean, modern, trustworthy aesthetic

Generate this image now with maximum quality and detail."""

    return prompt


def call_kimi_for_image(prompt, output_filename):
    """
    Call Kimi API to generate an image.
    
    Note: This uses the standard Kimi chat API. Kimi may return:
    1. A markdown image link: ![description](url)
    2. A direct URL to an image
    3. A base64-encoded image
    4. Text description (if image generation fails)
    """
    
    # Try both possible environment variable names
    api_key = os.environ.get('KIMI_API_KEY') or os.environ.get('KIMI_PLUGIN_API_KEY')
    if not api_key:
        log("❌ KIMI_API_KEY not found in environment")
        return None
    
    headers = {
        "Authorization": f"Bearer {api_key}",
        "Content-Type": "application/json"
    }
    
    # Try the chat completions endpoint with image generation request
    payload = {
        "model": "kimi-latest",
        "messages": [
            {
                "role": "system",
                "content": "You are an expert image generation assistant. When asked to create an image, you should generate a high-quality, photorealistic image matching the description. Return the image as a markdown image link: ![description](image_url) or provide the image data directly."
            },
            {
                "role": "user",
                "content": prompt
            }
        ],
        "temperature": 0.7,
        "max_tokens": 2000
    }
    
    try:
        log("🎨 Sending request to Kimi for image generation...")
        
        response = requests.post(
            "https://api.moonshot.cn/v1/chat/completions",
            headers=headers,
            json=payload,
            timeout=120
        )
        
        if response.status_code != 200:
            log(f"❌ API Error: {response.status_code}")
            log(f"Response: {response.text[:200]}")
            return None
        
        data = response.json()
        content = data.get('choices', [{}])[0].get('message', {}).get('content', '')
        
        log(f"📄 Response received ({len(content)} chars)")
        
        # Parse the response for image URL
        import re
        
        # Look for markdown image: ![alt](url)
        markdown_match = re.search(r'!\[([^\]]*)\]\((https?://[^\s\)]+)\)', content)
        if markdown_match:
            image_url = markdown_match.group(2)
            log(f"✅ Found image URL in markdown")
            return download_image(image_url, output_filename)
        
        # Look for bare URL that looks like an image
        url_match = re.search(r'(https?://[^\s\)]+\.(?:png|jpg|jpeg|gif|webp))', content, re.IGNORECASE)
        if url_match:
            image_url = url_match.group(1)
            log(f"✅ Found image URL")
            return download_image(image_url, output_filename)
        
        # Check if content IS a URL
        if content.strip().startswith('http'):
            image_url = content.strip().split()[0]
            log(f"✅ Found URL in content")
            return download_image(image_url, output_filename)
        
        # No image found - Kimi returned text
        log(f"⚠️ No image URL found in response")
        log(f"Response preview: {content[:300]}...")
        return None
        
    except Exception as e:
        log(f"❌ Error calling Kimi API: {e}")
        return None


def download_image(url, output_filename):
    """Download image from URL and save to output directory."""
    
    try:
        log(f"⬇️ Downloading image from {url[:50]}...")
        
        response = requests.get(url, timeout=60)
        
        if response.status_code != 200:
            log(f"❌ Failed to download: {response.status_code}")
            return None
        
        # Ensure output directory exists
        os.makedirs(OUTPUT_DIR, exist_ok=True)
        
        # Determine file extension from content-type
        content_type = response.headers.get('content-type', '')
        if 'png' in content_type:
            ext = 'png'
        elif 'jpeg' in content_type or 'jpg' in content_type:
            ext = 'jpg'
        elif 'gif' in content_type:
            ext = 'gif'
        elif 'webp' in content_type:
            ext = 'webp'
        else:
            ext = 'png'  # default
        
        output_path = os.path.join(OUTPUT_DIR, f"{output_filename}.{ext}")
        
        with open(output_path, 'wb') as f:
            f.write(response.content)
        
        file_size = os.path.getsize(output_path)
        log(f"✅ Image saved: {output_path} ({file_size} bytes)")
        
        return f"/images/{output_filename}.{ext}"
        
    except Exception as e:
        log(f"❌ Error downloading image: {e}")
        return None


def fetch_articles_from_aitable():
    """Fetch articles that need images from AITable."""
    
    headers = {
        "Authorization": f"Bearer {AITABLE_TOKEN}",
        "Content-Type": "application/json"
    }
    
    url = f"{AITABLE_BASE_URL}/datasheets/{NEWS_DATASHEET_ID}/records"
    
    try:
        log("📡 Fetching articles from AITable...")
        
        response = requests.get(url, headers=headers, params={"pageSize": 20})
        data = response.json()
        records = data.get("data", {}).get("records", [])
        
        articles = []
        for record in records:
            fields = record.get("fields", {})
            
            # Check if article needs an image
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
        
        log(f"📰 Found {len(articles)} articles needing images")
        return articles
        
    except Exception as e:
        log(f"❌ Error fetching from AITable: {e}")
        return []


def update_aitable_with_image(article_id, image_url):
    """Update AITable record with the generated image URL."""
    
    headers = {
        "Authorization": f"Bearer {AITABLE_TOKEN}",
        "Content-Type": "application/json"
    }
    
    url = f"{AITABLE_BASE_URL}/datasheets/{NEWS_DATASHEET_ID}/records"
    
    payload = {
        "records": [{
            "recordId": article_id,
            "fields": {
                "Image_URL": image_url,
                "Notes": f"Image generated by Kimi Claw on {datetime.now().strftime('%Y-%m-%d %H:%M')}"
            }
        }]
    }
    
    try:
        response = requests.patch(url, headers=headers, json=payload)
        
        if response.status_code == 200:
            log(f"✅ AITable updated with image URL")
            return True
        else:
            log(f"❌ Failed to update AITable: {response.status_code}")
            return False
            
    except Exception as e:
        log(f"❌ Error updating AITable: {e}")
        return False


def generate_single_image(article_id, title, summary, category):
    """Generate image for a single article."""
    
    log(f"🎯 Generating image for: {title[:50]}...")
    
    # Create prompt
    prompt = generate_kimi_image_prompt(title, summary, category)
    
    # Generate filename
    safe_title = "".join(c for c in title[:30] if c.isalnum() or c in (' ', '-', '_')).rstrip()
    safe_title = safe_title.replace(' ', '-').lower()
    filename = f"article-{article_id}-{safe_title}"
    
    # Call Kimi for image
    image_url = call_kimi_for_image(prompt, filename)
    
    if image_url:
        # Update AITable
        update_aitable_with_image(article_id, image_url)
        return image_url
    else:
        log(f"⚠️ Image generation failed, using default")
        return "/images/default-hero.jpg"


def main():
    parser = argparse.ArgumentParser(description='Kimi Claw Image Generation System')
    parser.add_argument('--article-id', help='Generate image for specific article ID')
    parser.add_argument('--title', help='Article title')
    parser.add_argument('--summary', help='Article summary', default='')
    parser.add_argument('--category', help='Article category', default='Community')
    parser.add_argument('--batch', action='store_true', help='Process all pending articles')
    parser.add_argument('--test', action='store_true', help='Test with sample article')
    
    args = parser.parse_args()
    
    log("="*60)
    log("KIMI CLAW IMAGE GENERATION SYSTEM")
    log("Don't worry. Even if the world forgets, I'll generate images for you.")
    log("="*60)
    
    if args.test:
        # Test with sample
        log("🧪 Running test mode...")
        result = generate_single_image(
            "test123",
            "Wilkes County Schools Celebrate Record Graduation Rate",
            "Students and faculty gather to celebrate the highest graduation rate in county history.",
            "Schools"
        )
        log(f"Test result: {result}")
        
    elif args.article_id and args.title:
        # Single article
        result = generate_single_image(
            args.article_id,
            args.title,
            args.summary,
            args.category
        )
        log(f"Result: {result}")
        
    elif args.batch:
        # Batch process
        articles = fetch_articles_from_aitable()
        
        if not articles:
            log("No articles to process.")
            return
        
        log(f"Processing {len(articles)} articles...")
        
        for i, article in enumerate(articles[:5], 1):  # Limit to 5 per run
            log(f"\n[{i}/{min(len(articles), 5)}] Processing article...")
            generate_single_image(
                article['id'],
                article['title'],
                article['summary'],
                article['category']
            )
            
        log(f"\n{'='*60}")
        log("Batch processing complete")
        
    else:
        parser.print_help()
        log("\n💡 Example usage:")
        log("  python3 kimi_claw_image_system.py --test")
        log("  python3 kimi_claw_image_system.py --batch")
        log("  python3 kimi_claw_image_system.py --article-id 'rec123' --title 'News Title'")


if __name__ == "__main__":
    main()
