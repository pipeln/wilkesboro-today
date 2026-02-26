import { defineConfig } from 'astro/config';
import tailwind from '@astrojs/tailwind';
import sitemap from '@astrojs/sitemap';

// https://astro.build/config
export default defineConfig({
  site: 'https://wilkesboro-today.pages.dev',
  integrations: [
    tailwind(),
    sitemap({
      filter: (page) => !page.includes('/admin'),
      customPages: [
        'https://wilkesboro-today.pages.dev/',
        'https://wilkesboro-today.pages.dev/events/',
      ],
    }),
  ],
  output: 'static',
  build: {
    format: 'directory'
  }
});