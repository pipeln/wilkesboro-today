# Quick Start

## Prerequisites
- Node.js 18+ 
- npm or yarn
- Git

## Local Development

```bash
# Clone repository
git clone https://github.com/yourusername/wilkesboro-today.git
cd wilkesboro-today

# Install dependencies
npm install

# Create environment file
cp .env.example .env
# Edit .env and add your AITABLE_TOKEN

# Start dev server
npm run dev

# Build for production
npm run build

# Preview production build
npm run preview
```

## Deploy to Cloudflare Pages

### Option 1: Git Integration (Recommended)
1. Push code to GitHub
2. Go to https://dash.cloudflare.com
3. Click **Pages** → **Create a project**
4. Connect your GitHub repo
5. Build settings:
   - Build command: `npm run build`
   - Output directory: `dist`
6. Add environment variable: `AITABLE_TOKEN`
7. Deploy!

### Option 2: Wrangler CLI
```bash
# Install Wrangler
npm install -g wrangler

# Login to Cloudflare
wrangler login

# Deploy
wrangler pages deploy dist
```

## Project Structure

```
website-design/
├── src/
│   ├── components/      # Reusable components
│   ├── layouts/         # Page layouts
│   ├── pages/           # Route pages
│   ├── styles/          # Global styles
│   └── utils/           # Helper functions
├── public/              # Static assets
├── dist/                # Build output
├── astro.config.mjs     # Astro config
├── tailwind.config.mjs  # Tailwind config
└── package.json         # Dependencies
```

## Available Scripts

| Command | Description |
|---------|-------------|
| `npm run dev` | Start dev server (localhost:4321) |
| `npm run build` | Build for production |
| `npm run preview` | Preview production build |
| `npm run astro` | Astro CLI commands |

## Environment Variables

Create `.env` file:

```
AITABLE_TOKEN=your_token_here
```

## Features

- ⚡ **Astro** - Fast static site generation
- 🎨 **Tailwind CSS** - Utility-first styling
- 📱 **Responsive** - Mobile-first design
- 🔍 **SEO** - Built-in optimization
- 🗺️ **Sitemap** - Auto-generated
- 📰 **RSS** - Feed generation
- 🌐 **AITable** - Headless CMS

## License

MIT
