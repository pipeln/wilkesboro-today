import { defineConfig } from 'astro/config';
import tailwind from '@astrojs/tailwind';
import sitemap from '@astrojs/sitemap';
import rss from '@astrojs/rss';

// https://astro.build/config
export default defineConfig({
  site: 'https://wilkesborotoday.com',
  integrations: [
    tailwind(),
    sitemap(),
  ],
  output: 'static',
  adapter: undefined, // Use static output for Cloudflare Pages
  build: {
    format: 'directory'
  }
});