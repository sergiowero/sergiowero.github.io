// @ts-check
import { defineConfig } from 'astro/config';

// User site (sergiowero.github.io) → served from the domain root, no `base` needed.
export default defineConfig({
  site: 'https://sergiowero.github.io',
  trailingSlash: 'always',
  build: { format: 'directory' },
});
