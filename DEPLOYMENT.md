# Cloudflare Pages Deployment Guide

## Free Tier Limits (Very Generous)

| Feature | Free Tier |
|---------|-----------|
| **Builds** | 500 builds/month |
| **Bandwidth** | Unlimited |
| **Requests** | Unlimited |
| **Storage** | Unlimited |
| **Custom domains** | Yes |
| **SSL** | Auto (Let's Encrypt) |
| **Preview deployments** | Yes |

**More than enough for a local news site!**

---

## Setup Instructions

### 1. Create Cloudflare Account
1. Go to https://dash.cloudflare.com/sign-up
2. Sign up (free)
3. Verify email

### 2. Create Pages Project

**Option A: Git Integration (Recommended)**
1. Push code to GitHub
2. In Cloudflare dashboard: **Pages** → **Create a project**
3. Connect GitHub repository
4. Configure build settings:
   - **Build command:** `npm run build`
   - **Build output directory:** `dist`
   - **Root directory:** `/`

**Option B: Direct Upload**
1. Build locally: `npm run build`
2. Cloudflare dashboard: **Pages** → **Upload assets**
3. Drag `dist/` folder

### 3. Environment Variables

Add in Cloudflare dashboard:
- `AITABLE_TOKEN` = your AITable API token

Path: **Pages** → **Your project** → **Settings** → **Environment variables**

### 4. Custom Domain (Optional)

1. Buy domain (Cloudflare, Namecheap, etc.)
2. In Pages: **Custom domains** → **Set up a custom domain**
3. Follow DNS instructions

---

## Build Configuration

### astro.config.mjs (already configured)
```javascript
export default defineConfig({
  output: 'static',  // Required for Cloudflare Pages
  adapter: undefined, // Static output
  build: {
    format: 'directory'
  }
});
```

### wrangler.toml (optional, for advanced config)
```toml
name = "wilkesboro-today"
compatibility_date = "2024-01-01"

[build]
command = "npm run build"
```

---

## Automatic Deployments

### With GitHub (Recommended)
Every push to `main` branch → automatic deployment

### Build Schedule
For daily content updates from AITable:

**Option 1: GitHub Actions Cron**
```yaml
# Add to .github/workflows/deploy.yml
on:
  schedule:
    - cron: '0 */6 * * *'  # Every 6 hours
```

**Option 2: Cloudflare Cron Triggers**
Use Cloudflare Workers to trigger rebuilds

---

## Performance Features (Free)

✅ **Global CDN** - 300+ locations worldwide  
✅ **HTTP/3** - Latest protocol  
✅ **Brotli compression** - Smaller files  
✅ **Edge caching** - Instant load times  
✅ **Analytics** - Basic visitor stats  

---

## Alternative Free Hosts

| Host | Pros | Cons |
|------|------|------|
| **Cloudflare Pages** | Best performance, unlimited bandwidth | None really |
| **Vercel** | Great for Next.js, easy deploy | Bandwidth limits on free |
| **Netlify** | Good features, easy UI | Build minute limits |
| **GitHub Pages** | Simple, integrated | No server-side functions |
| **Surge.sh** | Super simple | Basic features |

**Recommendation: Cloudflare Pages** 🏆

---

## Cost Comparison

| Host | Monthly Cost | Bandwidth | Builds |
|------|-------------|-----------|--------|
| Cloudflare Pages | **$0** | Unlimited | 500 |
| Vercel | $0 | 100GB | 6,000 min |
| Netlify | $0 | 100GB | 300 min |
| GitHub Pages | $0 | 100GB | N/A |

---

## Quick Deploy Checklist

- [ ] Code pushed to GitHub
- [ ] Cloudflare account created
- [ ] Pages project created
- [ ] Build settings configured
- [ ] Environment variables set
- [ ] First deployment successful
- [ ] Custom domain (optional)
- [ ] Analytics enabled

---

## Troubleshooting

**Build fails?**
- Check Node.js version (use 18+)
- Verify `package.json` has build script
- Check environment variables

**Site not updating?**
- Clear Cloudflare cache
- Check build logs in dashboard
- Verify GitHub webhook

**Slow builds?**
- Use `npm ci` instead of `npm install`
- Cache node_modules in CI

---

*Ready to deploy? Just push to GitHub and connect to Cloudflare Pages!*
