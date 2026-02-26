# Gemini Image Generation Setup

## Prerequisites

1. **Google AI Studio Account**
   - Go to https://makersuite.google.com/app/apikey
   - Create an API key
   - Copy the key

2. **Enable API Access**
   - Go to https://console.cloud.google.com/
   - Enable "Generative Language API"
   - Ensure billing is set up (free tier available)

## Setup

### Step 1: Set Environment Variable

```bash
export GEMINI_API_KEY='your-api-key-here'
```

Or add to your shell profile:
```bash
echo 'export GEMINI_API_KEY="your-api-key-here"' >> ~/.bashrc
source ~/.bashrc
```

### Step 2: Test the Service

```bash
cd /root/.openclaw/workspace
python3 gemini_image_service.py
```

### Step 3: Create Webhook Endpoint

For real-time generation, create a webhook that AITable can call:

```python
# webhook_server.py
from flask import Flask, request
import subprocess

app = Flask(__name__)

@app.route('/generate-image', methods=['POST'])
def generate_image():
    article_id = request.json.get('article_id')
    # Trigger image generation
    subprocess.run(['python3', 'gemini_image_service.py'])
    return {'status': 'queued'}

if __name__ == '__main__':
    app.run(port=5000)
```

### Step 4: AITable Webhook Configuration

In AITable, set up a webhook:
1. Go to your News_Raw datasheet
2. Click "Automations" or "Webhooks"
3. Create new webhook
4. Trigger: When record is created and Status = "Approved"
5. Action: POST to your webhook URL
6. Payload: `{ "article_id": "{record_id}" }`

## How It Works

1. **New article approved** in AITable
2. **Webhook triggers** immediately
3. **Gemini generates** image based on:
   - Article title
   - Summary/content
   - Category (custom visual style per category)
4. **Image saved** to `/public/images/article-{id}.png`
5. **AITable updated** with image URL
6. **Website shows** new article with image

## Category-Based Visual Styles

| Category | Visual Style |
|----------|-------------|
| Public_Safety | Emergency services, dramatic lighting |
| Schools | Education, students, warm lighting |
| Civics | Government buildings, professional |
| Business | Storefronts, offices, welcoming |
| Community | Festivals, gatherings, inclusive |
| Breaking | Urgency, photojournalism style |

## Cost

- **Gemini Pro Vision**: Free tier available (60 requests/minute)
- **Paid tier**: $0.0025 per image (very cheap)
- **Much cheaper than DALL-E 3**

## Limitations

- Gemini image generation is newer than DALL-E
- Quality may vary
- Some prompts may be rejected (safety filters)
- Rate limits apply

## Troubleshooting

**"API key not valid"**
- Check key is copied correctly
- Ensure API is enabled in Google Cloud Console

**"No image generated"**
- Gemini may return text instead of image for some prompts
- Try adjusting the prompt

**"Rate limit exceeded"**
- Wait a minute and try again
- Upgrade to paid tier for higher limits

## Next Steps

1. Get your Gemini API key
2. Test the service manually
3. Set up AITable webhook
4. Deploy webhook server (if needed)
5. Monitor generation quality

Want me to help set up any of these steps?
