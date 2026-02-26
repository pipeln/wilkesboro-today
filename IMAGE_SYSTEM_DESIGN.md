# Real-Time Image Generation System - Design Document

## Current Problems
1. Cron job spawns agents that may not complete reliably
2. No feedback loop - don't know if images actually got created
3. No quality control - images might not match article content
4. No real-time updates - hourly batch is too slow for breaking news

## Proposed Architecture

```
┌─────────────────┐     ┌──────────────────┐     ┌─────────────────┐
│   AITable       │────▶│  Image Queue     │────▶│  Generation     │
│   (New Article) │     │  (Priority)      │     │  Service        │
└─────────────────┘     └──────────────────┘     └─────────────────┘
         │                                               │
         │                                               ▼
         │                                       ┌─────────────────┐
         │                                       │  Quality Check  │
         │                                       │  (AI Review)    │
         │                                       └─────────────────┘
         │                                               │
         ▼                                               ▼
┌─────────────────┐                             ┌─────────────────┐
│   Website       │◀────────────────────────────│  CDN/Storage    │
│   (Live Update) │                             │  (Cloudflare)   │
└─────────────────┘                             └─────────────────┘
```

## Option 1: DALL-E 3 / Midjourney API (Recommended)

**Pros:**
- High quality images
- Fast generation (10-30 seconds)
- Good text understanding
- Reliable API

**Cons:**
- Costs money ($0.04-0.08 per image)
- Rate limits

**Implementation:**
```python
# image_service.py
import openai
import requests

def generate_image(prompt, article_id):
    """Generate image using DALL-E 3"""
    response = openai.images.generate(
        model="dall-e-3",
        prompt=prompt,
        size="1792x1024",  # 16:9 for hero images
        quality="standard",
        n=1
    )
    
    image_url = response.data[0].url
    
    # Download and save to CDN
    download_and_upload(image_url, f"article-{article_id}.jpg")
    
    return image_url
```

## Option 2: Stable Diffusion XL (Self-Hosted)

**Pros:**
- No per-image cost
- Full control
- Can fine-tune on local imagery

**Cons:**
- Requires GPU server ($50-100/month)
- Setup complexity
- Slower generation

**Implementation:**
- Deploy on RunPod / Vast.ai
- API endpoint for generation
- Webhook callback when complete

## Option 3: Cloudflare Workers + AI

**Pros:**
- Runs on Cloudflare's network
- No server management
- Integrated with your hosting

**Cons:**
- Limited to Stable Diffusion (lower quality)
- Newer technology

**Implementation:**
```javascript
// worker.js
export default {
  async fetch(request, env) {
    const { prompt } = await request.json();
    
    const response = await env.AI.run(
      '@cf/stabilityai/stable-diffusion-xl-base-1.0',
      { prompt }
    );
    
    return new Response(response, {
      headers: { 'content-type': 'image/png' }
    });
  }
}
```

## Recommended: Hybrid Approach

### Tier 1: Breaking News (DALL-E 3)
- Immediate generation
- High quality
- Cost: ~$0.08 per image

### Tier 2: Regular News (Stable Diffusion)
- Batch processing
- Lower cost
- Queue-based

### Tier 3: Default Images (Pre-made)
- Use existing default-hero.jpg
- Zero cost
- Instant

## Real-Time WebSocket Updates

Instead of cron jobs, use WebSockets for instant updates:

```javascript
// Browser receives new article with image
const ws = new WebSocket('wss://wilkesboro-today.com/ws');

ws.onmessage = (event) => {
  const { article, imageUrl } = JSON.parse(event.data);
  
  // Fade in new article with image
  addArticleToFeed(article, imageUrl);
};
```

## Quality Control Pipeline

```python
def quality_check(image_path, article_title):
    """AI reviews generated image for relevance"""
    
    # Use GPT-4 Vision to check image
    review = openai.chat.completions.create(
        model="gpt-4-vision-preview",
        messages=[{
            "role": "user",
            "content": [
                {"type": "text", "text": f"Does this image match the article: '{article_title}'? Rate 1-10."},
                {"type": "image_url", "image_url": {"url": image_path}}
            ]
        }]
    )
    
    score = extract_score(review.choices[0].message.content)
    
    if score < 7:
        # Regenerate with better prompt
        return regenerate_image(article_title)
    
    return image_path
```

## Implementation Phases

### Phase 1: Basic DALL-E Integration (This Week)
- Set up OpenAI API key
- Create image generation endpoint
- Update AITable webhook to trigger generation
- Store images in Cloudflare R2 (cheap storage)

### Phase 2: Real-Time Updates (Next Week)
- WebSocket server for live updates
- Browser receives new articles instantly
- Images load as they're generated

### Phase 3: Quality & Optimization (Later)
- AI quality checking
- Prompt engineering improvements
- Caching frequently used images

## Cost Estimate (DALL-E 3)

| Usage | Cost/Month |
|-------|-----------|
| 100 images | $8 |
| 500 images | $40 |
| 1000 images | $80 |
| Storage (R2) | ~$1 |

## Next Steps

1. **Choose approach** - DALL-E 3 for quality vs Stable Diffusion for cost?
2. **Set up API keys** - OpenAI or Replicate
3. **Create image service** - Webhook endpoint
4. **Update AITable** - Add webhook on new articles
5. **Test pipeline** - End-to-end with one article

Which approach feels right to you? Quality (DALL-E) or cost (Stable Diffusion)?
