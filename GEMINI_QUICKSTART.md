# Gemini Image Generation - Quick Setup

## Step 1: Get Your API Key

1. Go to https://makersuite.google.com/app/apikey
2. Sign in with your Google account
3. Click "Create API Key"
4. Copy the key

## Step 2: Add Key to Environment

Edit the `.env` file:
```bash
nano /root/.openclaw/workspace/.env
```

Replace `your_api_key_here` with your actual key:
```
GEMINI_API_KEY=AIzaSy...your_actual_key...
```

Save and exit (Ctrl+X, Y, Enter)

## Step 3: Install Dependencies

```bash
pip3 install python-dotenv
```

## Step 4: Test

```bash
cd /root/.openclaw/workspace
python3 gemini_image_service.py --test
```

If successful, you'll see:
- ✅ Image saved message
- File created at `/website-design/public/images/article-test.png`

## Step 5: Run Batch Generation

```bash
python3 gemini_image_service.py --batch
```

This will:
1. Fetch approved articles from AITable
2. Generate images for each
3. Update AITable with image URLs

## API Limits

- **Free tier**: 60 requests/minute, 1,500 requests/day
- **Paid tier**: Higher limits, still very cheap

## Troubleshooting

**"GEMINI_API_KEY not set"**
- Check `.env` file exists and has correct key
- Run `source /root/.openclaw/workspace/.env` to reload

**"API Error: 400"**
- Invalid API key format
- Key may need to be regenerated

**"No image found in response"**
- Gemini sometimes returns text instead of image
- Try running again with slightly different prompt

## Next Steps

Once working:
1. Set up cron job for automatic generation
2. Add webhook for real-time generation
3. Integrate with website build process
