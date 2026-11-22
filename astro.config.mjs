// @ts-check
import { defineConfig } from 'astro/config';
import starlight from '@astrojs/starlight';
import sitemap from '@astrojs/sitemap';
import starlightLinksValidator from 'starlight-links-validator';
import { sitemapOptions } from './src/lib/sitemap.mjs';
import { ORIGIN, BASE, TITLE, DESCRIPTION } from './src/lib/site.mjs';
import { satteri } from '@astrojs/markdown-satteri';
import { hastBase } from './src/lib/hast-base.mjs';

export default defineConfig({
	site: ORIGIN,
	base: BASE || undefined,
	trailingSlash: 'always',
	// Content links are written without the sub-path; this adds it in the HTML.
	markdown: { processor: satteri({ hastPlugins: [hastBase] }) },
	integrations: [
		// Added here so that it takes options; Starlight then leaves its own copy out.
		sitemap(sitemapOptions()),
		starlight({
			title: TITLE,
			description: DESCRIPTION,
			defaultLocale: 'root',
			locales: {
				root: { label: 'English', lang: 'en' },
				'zh-tw': { label: '繁體中文', lang: 'zh-TW' },
				'zh-cn': { label: '简体中文', lang: 'zh-CN' },
			},
			sidebar: [
				{
					label: 'Versions',
					translations: { 'zh-TW': '版本', 'zh-CN': '版本' },
					items: [{ autogenerate: { directory: 'versions' } }],
				},
				{
					label: 'Systems',
					translations: { 'zh-TW': '系統', 'zh-CN': '系统' },
					items: [{ slug: 'systems' }, { slug: 'systems/headhunting' }, { slug: 'systems/arsenal' }, { slug: 'systems/combat' }, { slug: 'systems/operator-progression' }, { slug: 'systems/weapons' }, { slug: 'systems/gear' }, { slug: 'systems/enemies' }, { slug: 'systems/dijiang' }, { slug: 'systems/servers-and-time' }, { slug: 'systems/platforms' }, { slug: 'systems/names' }],
				},
				{
					label: 'AIC',
					translations: { 'zh-TW': '集成工業', 'zh-CN': '集成工业' },
					items: [{ slug: 'aic' }, { slug: 'aic/power' }, { slug: 'aic/production' }, { slug: 'aic/recipes' }, { slug: 'aic/regional-development' }],
				},
				{
					label: 'Operators',
					translations: { 'zh-TW': '幹員', 'zh-CN': '干员' },
					collapsed: true,
					items: [{ autogenerate: { directory: 'operators' } }],
				},
			],
			customCss: ['@fontsource-variable/lexend', './src/styles/endfield.css'],
			components: {
				// Three overrides: the site name with its links, the answer above the body with the page notes after it, and the theme buttons.
				SiteTitle: './src/components/SiteTitle.astro',
				MarkdownContent: './src/components/MarkdownContent.astro',
				ThemeSelect: './src/components/ThemeSelect.astro',
			},
			routeMiddleware: './src/routeData.ts',
			credits: false,
			pagination: false,
			expressiveCode: {
				themes: ['night-owl', 'github-light'],
				// `patch` gets diff colours but keeps the literal +/- in the page text.
				// The `diff` language is not used: Expressive Code draws its +/- with CSS,
				// so an agent reading the HTML would not see which lines were added or removed.
				shiki: { langAlias: { patch: 'diff' } },
				styleOverrides: { borderRadius: '0', borderWidth: '1px', frames: { shadowColor: 'transparent' } },
			},
			plugins: [
				starlightLinksValidator({
					exclude: ['/**/*.md', '/*.md', '/llms.txt', '/**/llms.txt', '/index.json', '/**/index.json', '/**/art/**'],
				}),
			],
		}),
	],
});
