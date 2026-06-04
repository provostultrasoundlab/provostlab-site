// @ts-check
import { defineConfig } from 'astro/config';

// Live at the polymtl custom domain (CNAME → provostultrasoundlab.github.io).
export default defineConfig({
  site: 'https://provostlab.polymtl.ca',
  base: '/',
});
