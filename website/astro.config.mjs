// @ts-check
import { defineConfig } from 'astro/config';
import starlight from '@astrojs/starlight';

// https://astro.build/config
export default defineConfig({
	site: 'https://VinsmokeSomya.github.io',
	base: '/RabbitHole',
	integrations: [
		starlight({
			title: 'RabbitHole',
			logo: {
				src: '~/assets/logo.svg',
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
					label: 'Guides',
					items: [
						{ label: 'Getting Started', slug: 'documentation' },
						{ label: 'How-to & Examples', slug: 'howto' },
					],
				},
				{
					label: 'Design & Vision',
					items: [
						{ label: 'Architecture', slug: 'architecture' },
						{ label: 'Technical Blueprint', slug: 'blueprint' },
						{ label: 'Roadmap', slug: 'roadmap' },
					],
				},
			],
		}),
	],
});
