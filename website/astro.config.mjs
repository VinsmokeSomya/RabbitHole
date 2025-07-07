// @ts-check
import { defineConfig } from 'astro/config';

import svelte from '@astrojs/svelte';

// https://astro.build/config
export default defineConfig({
  // TODO: Replace `<YOUR-GITHUB-USERNAME>` with your actual GitHub username.
  site: 'https://<YOUR-GITHUB-USERNAME>.github.io',
  base: '/RabbitHole',
  integrations: [svelte()]
});