/** @type {import('tailwindcss').Config} */
export default {
  content: ['./src/**/*.{astro,html,js,jsx,md,mdx,svelte,ts,tsx,vue}'],
  theme: {
    extend: {
      colors: {
        primary: {
          DEFAULT: '#1e40af',
          dark: '#1e3a8a',
          light: '#3b82f6',
        },
        secondary: '#dc2626',
        accent: '#f59e0b',
      },
      fontFamily: {
        sans: ['Inter', 'system-ui', 'sans-serif'],
        serif: ['Source Serif Pro', 'Georgia', 'serif'],
      },
    },
  },
  plugins: [],
}