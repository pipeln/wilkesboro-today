#!/usr/bin/env python3
"""
Kimi Image Generation Service - Using Native Kimi API
"""

import os
import sys
import json
import requests
from datetime import datetime

# Load from .env file
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

# Load environment
env_vars = load_env_file('/root/.openclaw/workspace/.env')
KIMI_API_KEY = env_vars.get('KIMI_API_KEY', '')
KIMI_API_URL = "https://api.moonshot.cn/v1/chat/completions"

OUTPUT_DIR = "/root/.openclaw/workspace/website-design/public/images"


def log(message, level="INFO"):
    timestamp = datetime.now().strftime('%H:%M:%S')
    emoji = {"INFO": "ℹ️", "SUCCESS": "✅", "ERROR": "❌", "WARNING": "⚠️"}.get(level, "ℹ️")
    print(f"[{emoji} {timestamp}] {message}")


def generate_kimi_image(prompt, output_filename):
    """Generate image using Kimi API."""
    
    if not KIMI_API_KEY:
        log("KIMI_API_KEY not set", "ERROR")
        return None
    
    headers = {
        "Authorization": f"Bearer {KIMI_API_KEY}",
        "Content-Type": "application/json"
    }
    
    payload = {
        "model": "kimi-k2-5",
        "messages": [
            {
                "role": "system",
                "content": "You are an expert at creating detailed image descriptions and can generate images. When asked to create an image, provide a detailed description and if possible, generate the actual image."
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
        log("Sending request to Kimi API...")
        
        response = requests.post(
            KIMI_API_URL,
            headers=headers,
            json=payload,
            timeout=120
        )
        
        if response.status_code == 200:
            data = response.json()
            content = data.get('choices', [{}])[0].get('message', {}).get('content', '')
            
            log(f"Response received: {len(content)} chars")
            log(f"Preview: {content[:200]}...")
            
            # Check if Kimi returned an image URL or markdown
            import re
            
            # Look for markdown image
            markdown_match = re.search(r'!\[([^\]]*)\]\((https?://[^\s\)]+)\)', content)
            if markdown_match:
                image_url = markdown_match.group(2)
                log(f"Found image URL in markdown")
                return download_image(image_url, output_filename)
            
            # Look for bare URL
            url_match = re.search(r'(https?://[^\s\)]+\.(?:png|jpg|jpeg|gif|webp))', content, re.IGNORECASE)
            if url_match:
                image_url = url_match.group(1)
                log(f"Found image URL")
                return download_image(image_url, output_filename)
            
            # If no image, Kimi returned a description - we can use this with another service
            log("No direct image URL found - Kimi provided description", "WARNING")
            log("Description can be used with Gemini/DALL-E", "INFO")
            
            # Save description for use with other services
            desc_file = os.path.join(OUTPUT_DIR, f"{output_filename}_description.txt")
            with open(desc_file, 'w') as f:
                f.write(content)
            
            return None
        else:
            log(f"API Error: {response.status_code}", "ERROR")
            log(f"Response: {response.text[:300]}", "ERROR")
            return None
            
    except Exception as e:
        log(f"Error: {e}", "ERROR")
        return None


def download_image(url, filename):
    """Download image from URL."""
    try:
        log(f"Downloading image...")
        response = requests.get(url, timeout=60)
        
        if response.status_code == 200:
            os.makedirs(OUTPUT_DIR, exist_ok=True)
            output_path = os.path.join(OUTPUT_DIR, f"{filename}.png")
            
            with open(output_path, 'wb') as f:
                f.write(response.content)
            
            file_size = len(response.content)
            log(f"Image saved: {output_path} ({file_size} bytes)", "SUCCESS")
            return f"/images/{filename}.png"
        else:
            log(f"Download failed: {response.status_code}", "ERROR")
            return None
            
    except Exception as e:
        log(f"Download error: {e}", "ERROR")
        return None


def main():
    print("="*60)
    print("KIMI IMAGE GENERATION SERVICE")
    print("="*60)
    
    if not KIMI_API_KEY:
        log("KIMI_API_KEY not found in .env file", "ERROR")
        return
    
    # Test prompt
    prompt = """Create a professional news hero image for this article:
    
Title: "Wilkes County Celebrates New Community Center Opening"

Generate a photorealistic image showing:
- A modern community center building with people gathered
- Celebration atmosphere with balloons or ribbon cutting
- Blue sky, sunny day
- Diverse community members
- Professional photography style
- Wide angle, suitable for website hero banner (16:9 ratio)

Return the image as a markdown image link or direct URL."""

    log("Running test...")
    result = generate_kimi_image(prompt, "kimi-test")
    
    if result:
        log(f"Success! Image: {result}", "SUCCESS")
    else:
        log("Image generation failed or returned description only", "WARNING")
        log("Kimi may have provided a description that can be used with Gemini", "INFO")


if __name__ == "__main__":
    main()
