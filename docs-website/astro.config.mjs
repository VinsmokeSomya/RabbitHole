// @ts-check
import { defineConfig } from 'astro/config';
import starlight from '@astrojs/starlight';

import svelte from '@astrojs/svelte';

// https://astro.build/config
export default defineConfig({
	site: 'https://VinsmokeSomya.github.io',
	integrations: [
		starlight({
			title: 'RabbitHole',
			logo: {
				src: './src/assets/logo.png',
			},
			social: [
				{
					icon: 'github',
					label: 'GitHub',
					href: 'https://github.com/VinsmokeSomya/RabbitHole',
				},
			],
			sidebar: [
				{
					label: 'Overview',
					items: [
						{ label: 'Getting Started', slug: 'getting-started' },
						{ label: 'Core Concepts', slug: 'core-concepts' },
					],
				},
				{
					label: 'Guides',
					items: [{ label: 'How-To Guides', slug: 'how-to' }],
				},
				{
					label: 'Reference',
					items: [
						{ label: 'Architecture', slug: 'architecture' },
						{ label: 'Technical Blueprint', slug: 'blueprint' },
						{ label: 'Roadmap', slug: 'roadmap' },
					],
				},
				{
					label: 'API Reference',
					items: [
						{ label: 'Data Models', slug: 'api/data-models' },
						{ label: 'JSON-RPC', slug: 'api/json-rpc' },
					],
				},
			],
		}),
		svelte(),
	],
});