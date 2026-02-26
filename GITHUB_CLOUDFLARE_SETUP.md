# GitHub + Cloudflare Pages Setup Guide

## Current Status
✅ Website code is ready in `/root/.openclaw/workspace/website-design/`
✅ Git repository initialized with initial commit
✅ GitHub Actions workflow configured for Cloudflare Pages deployment
❌ Not yet connected to GitHub
❌ Not yet connected to Cloudflare Pages

---

## Step 1: Create GitHub Repository

### Option A: Using GitHub Web Interface
1. Go to https://github.com/new
2. Repository name: `wilkesboro-today`
3. Make it **Public** (for free GitHub Actions)
4. **DO NOT** initialize with README (we already have one)
5. Click **Create repository**

### Option B: Using GitHub CLI (if installed)
```bash
gh auth login
gh repo create wilkesboro-today --public --source=. --push
```

---

## Step 2: Push Code to GitHub

After creating the repo, run these commands in the website-design folder:

```bash
cd /root/.openclaw/workspace/website-design

# Add the GitHub remote (replace YOUR_USERNAME with your GitHub username)
git remote add origin https://github.com/YOUR_USERNAME/wilkesboro-today.git

# Rename branch to main
git branch -M main

# Push to GitHub
git push -u origin main
```

---

## Step 3: Set Up Cloudflare Pages

1. Go to https://dash.cloudflare.com
2. Sign in (or create free account)
3. Click **Pages** in the left sidebar
4. Click **Create a project**
5. Select **Connect to Git**
6. Connect your GitHub account
7. Select the `wilkesboro-today` repository
8. Configure build settings:
   - **Project name:** `wilkesboro-today`
   - **Production branch:** `main`
   - **Build command:** `npm run build`
   - **Build output directory:** `dist`
9. Click **Save and Deploy**

---

## Step 4: Add Environment Variables

In Cloudflare Pages dashboard:
1. Go to your project
2. Click **Settings** → **Environment variables**
3. Add:
   - `AITABLE_TOKEN` = `uskNPM9fPVHOgAGbDepyKER`
4. Click **Save**

---

## Step 5: Add Cloudflare Secrets to GitHub

In GitHub repository:
1. Go to **Settings** → **Secrets and variables** → **Actions**
2. Add these repository secrets:
   - `CLOUDFLARE_API_TOKEN` - Get from Cloudflare (see below)
   - `CLOUDFLARE_ACCOUNT_ID` - Get from Cloudflare sidebar
   - `AITABLE_TOKEN` - `uskNPM9fPVHOgAGbDepyKER`

### Get Cloudflare API Token:
1. In Cloudflare dashboard, click **My Profile** (top right)
2. Go to **API Tokens**
3. Click **Create Token**
4. Use template: **Edit Cloudflare Workers**
5. Or create custom token with:
   - Zone:Read
   - Page Rules:Edit
   - Cloudflare Pages:Edit
6. Copy the token

---

## Step 6: Deploy!

1. Make any small change and push to GitHub:
```bash
echo "# Wilkesboro Today" >> README.md
git add .
git commit -m "Trigger deployment"
git push
```

2. Watch the magic happen:
   - GitHub Actions will run automatically
   - Build will complete
   - Cloudflare Pages will deploy
   - Site will be live!

---

## Your Site Will Be Live At:

- **Default URL:** `https://wilkesboro-today.pages.dev`
- **Custom Domain:** (You can add later)

---

## What Gets Deployed

The site includes:
- ✅ Homepage with news feed
- ✅ Events page (from AITable)
- ✅ Jobs board
- ✅ Resources directory
- ✅ Weather widget
- ✅ RSS feeds
- ✅ Responsive design

---

## Auto-Deployment

Every push to `main` branch will:
1. Trigger GitHub Actions
2. Build the site with latest AITable data
3. Deploy to Cloudflare Pages
4. Update global CDN (instant worldwide)

---

## Need Help?

If you get stuck on any step, I can help troubleshoot. Just share:
- Error messages
- Which step you're on
- What you've tried

---

## Quick Commands Reference

```bash
# Navigate to project
cd /root/.openclaw/workspace/website-design

# Check git status
git status

# View commit history
git log --oneline

# Push changes
git add .
git commit -m "Your message"
git push

# Force push (if needed)
git push -f origin main
```
