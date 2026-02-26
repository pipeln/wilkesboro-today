# Fixing Cloudflare API Authentication Error

## The Problem
Error 403 - Authentication error. Your API token doesn't have permission to access the Pages project.

## Solution - Create Proper API Token

### Step 1: Go to Cloudflare
1. Visit: https://dash.cloudflare.com
2. Log in

### Step 2: Create API Token
1. Click your **profile** (top right corner)
2. Select **"My Profile"**
3. Click **"API Tokens"** tab
4. Click **"Create Token"**

### Step 3: Use Custom Template
Instead of using a pre-made template, click **"Get started"** under **"Create Custom Token"**

### Step 4: Configure Token

**Token Name:** `GitHub Actions Pages Deploy`

**Permissions:**
| Permission | Setting |
|------------|---------|
| Zone | Read |
| Cloudflare Pages | Edit |
| Account | Read |

**Zone Resources:**
- Include: All zones (or specific zone if you have a domain)

**Account Resources:**
- Include: All accounts

### Step 5: Create Token
1. Click **"Continue to summary"**
2. Click **"Create Token"**
3. **COPY THE TOKEN IMMEDIATELY** - you won't see it again!

### Step 6: Update GitHub Secret

1. Go to: https://github.com/pipeln/wilkesboro-today/settings/secrets/actions
2. Find `CLOUDFLARE_API_TOKEN`
3. Click **Update**
4. Paste your new token
5. Click **Update secret**

### Step 7: Get Account ID

1. In Cloudflare dashboard, look at the right sidebar
2. Copy **Account ID**
3. In GitHub secrets, add/update `CLOUDFLARE_ACCOUNT_ID` with this value

### Step 8: Re-run Deployment

1. Go to: https://github.com/pipeln/wilkesboro-today/actions
2. Find the failed workflow
3. Click **"Re-run jobs"**

## Alternative: Use Global API Key (Less Secure)

If custom token doesn't work:

1. In Cloudflare profile, go to **"API Tokens"**
2. Scroll down to **"Global API Key"**
3. Click **"View"**
4. Copy that key and use it as `CLOUDFLARE_API_TOKEN`

## Verification

After updating, your GitHub secrets should have:
- ✅ `CLOUDFLARE_API_TOKEN` - Your new token
- ✅ `CLOUDFLARE_ACCOUNT_ID` - From Cloudflare sidebar
- ✅ `AITABLE_TOKEN` - `uskNPM9fPVHOgAGbDepyKER`

## Still Not Working?

Check these:
1. Is the Pages project name exactly `wilkesboro-today` in Cloudflare?
2. Is your GitHub repo connected to the right Cloudflare account?
3. Try creating a new Pages project from scratch in Cloudflare

## Quick Check

Run this to test your token:
```bash
curl -X GET "https://api.cloudflare.com/client/v4/accounts" \
  -H "Authorization: Bearer YOUR_API_TOKEN" \
  -H "Content-Type: application/json"
```

Should return your account info if the token works.
