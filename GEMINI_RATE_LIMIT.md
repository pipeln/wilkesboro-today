# Gemini Rate Limit - What Happened

## Error 429 - Quota Exceeded

Your API key is **valid**, but you've hit the rate limit.

## Why This Happened

1. **Free tier limits:**
   - 60 requests per minute
   - 1,500 requests per day
   - May have been exceeded in testing

2. **Possible causes:**
   - Previous test attempts counted against quota
   - Multiple rapid requests
   - Daily limit already reached

## Solutions

### Option 1: Wait (Easiest)
- Rate limits reset automatically
- Try again in 10-15 minutes
- Or try again tomorrow for daily reset

### Option 2: Check Quota Status
Go to: https://ai.dev/rate-limit
See your current usage and when it resets

### Option 3: Upgrade Plan
Go to: https://makersuite.google.com/app/billing
- Pay-as-you-go pricing
- Higher limits
- Still very affordable

### Option 4: Use Different Google Account
- Create new API key with different account
- Fresh quota

## Test Again

Once quota resets:
```bash
cd /root/.openclaw/workspace
python3 gemini_image_service.py --test
```

## Alternative: Use Replicate (No Rate Limits)

If Gemini keeps hitting limits, we can use Replicate API:
- Stable Diffusion XL
- ~$0.01 per image
- No strict rate limits
- Requires credit card (but cheap)

Want me to set up Replicate as backup?
