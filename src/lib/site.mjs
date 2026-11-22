// Shared site facts and URL rules. Plain JS so astro.config.mjs, Astro code and
// the check script all use the same rules.

// The public address, including the sub-path of a GitHub Pages project site, without a
// trailing slash. SITE_URL overrides it for local agent tests (see tests/agent-eval/README.md).
export const SITE = (process.env.SITE_URL ?? 'https://yuanaruru.com/endfield-wiki').replace(/\/+$/, '');
/** Scheme and host of SITE. */
export const ORIGIN = new URL(SITE).origin;
/** Sub-path the site is served under: `/endfield-wiki`, or the empty string at a domain root. */
export const BASE = new URL(SITE).pathname.replace(/\/+$/, '');
export const TITLE = { en: 'Endfield Wiki', 'zh-TW': '終末地 Wiki', 'zh-CN': '终末地 Wiki' };
export const DESCRIPTION =
	'Unofficial reference for the game Arknights: Endfield (明日方舟：終末地): versions, operators and systems, read from the official notices.';

/** Root-relative address for an `href` or `src` in HTML: the site path behind BASE. */
export function withBase(path) {
	return BASE + path;
}

/** Locales: `dir` is the content sub-folder and URL prefix ('' = root). */
export const LOCALES = [
	{ dir: '', lang: 'en', label: 'English' },
	{ dir: 'zh-tw', lang: 'zh-TW', label: '繁體中文' },
	{ dir: 'zh-cn', lang: 'zh-CN', label: '简体中文' },
];

/** Starlight's route data gives the home page an empty id; the collection calls it `index`. */
export function pageId(id) {
	return id === '' ? 'index' : id;
}

/** Locale of a content entry id such as `operators/laevatain`, `zh-tw/operators/laevatain`, `index`, `zh-tw`. */
export function localeOf(id) {
	return (
		LOCALES.find((l) => l.dir && (id === l.dir || id.startsWith(l.dir + '/'))) ?? LOCALES[0]
	);
}

/** Entry id without its locale prefix. The home page is `index` in every locale. */
export function bareId(id) {
	const { dir } = localeOf(id);
	if (!dir) return id;
	return id === dir ? 'index' : id.slice(dir.length + 1);
}

/** Entry id of the same page in another locale. */
export function idInLocale(id, locale) {
	const bare = bareId(id);
	if (!locale.dir) return bare;
	return bare === 'index' ? locale.dir : `${locale.dir}/${bare}`;
}

/** Site path of the HTML page for an entry id. */
export function htmlPath(id) {
	return id === 'index' ? '/' : `/${id}/`;
}

/** Site path of the Markdown twin: drop the trailing slash, append `.md`; home is `/index.md`. */
export function mdPath(id) {
	return `/${id}.md`;
}

/** Markdown twin of an internal HTML path such as `/operators/laevatain/` or `/`. */
export function mdPathFromHtmlPath(path) {
	const trimmed = path.replace(/^\/+|\/+$/g, '');
	return mdPath(trimmed === '' ? 'index' : trimmed);
}

/** Site path of a language's page index: `/llms.txt`, `/zh-tw/llms.txt`. */
export function llmsPath(locale) {
	return `${locale.dir ? '/' + locale.dir : ''}/llms.txt`;
}

/**
 * The opening of each language's llms.txt: what a reader gets wrong without being told.
 * Site-specific. Keep it short: it shares the first 5,000 characters with the page list.
 */
export const LLMS_NOTES = {
	en: {
		summary: DESCRIPTION,
		heading: 'Before you answer',
		notes: [
			'Dates and times on every page are Asia server time (UTC+8). The Americas / Europe server runs on UTC-5: update maintenance happens at the same moment there (17:00 to 23:00 UTC-5, the day before), while timed content opens and ends at the same clock time in each server\'s own time, 13 hours apart.',
			'Dates are those of the global service (endfield.gryphline.com). The mainland China service (endfield.hypergryph.com) is not covered.',
			'Official notices name a version by its title, never by a number. Version 1.6 is "Sanctuary of Ink"; the numbers come from the fan wikis, and the versions index pairs every number with its title.',
			'The rate-up 6-star operator of a Chartered Headhunting banner leaves the Chartered pool after three Chartered banners and is not added to Basic Headhunting. Pages list banners as dated history and leave out limited-time events; check the official news for what is open today.',
			'One name has three spellings: English (Laevatain), Traditional Chinese (萊萬汀) and Simplified Chinese (莱万汀). A few differ beyond the script: Rossi is 洛西 in Traditional and 洛茜 in Simplified Chinese. Page addresses use the lower-case English name.',
			'This is an unofficial site. Dates, banners, events and names are read from official notices and the official site. Skill texts and stats are in-game texts of game data 1.6 as published by warfarin.wiki, checked against endfield.wiki.gg. Tier lists and team builds are absent. The combat damage formula comes from player tests on the NGA forum.',
			'Every page has a Markdown twin: drop the trailing slash and append `.md`.',
		],
		pages: 'Pages',
		home: 'Home page: the index pages, which list every page',
		full: 'All pages in one file',
		digest: 'Answer, caveat, dates and sources of every page, without the body',
		json: 'All pages in every language, with alternative names, as JSON',
		otherLanguage: 'This index in',
		more: 'More',
	},
	'zh-TW': {
		summary: '《明日方舟：終末地》(Arknights: Endfield) 的非官方資料站：版本、幹員與系統，內容讀自官方公告。',
		heading: '回答之前',
		notes: [
			'各頁的日期與時間都是 Asia 伺服器時間 (UTC+8)。Americas / Europe 伺服器使用 UTC-5：版本更新維護在兩邊是同一時刻（當地前一天 17:00 至 23:00），限時內容則在各伺服器自己時間的同一時刻開放與結束，相差 13 小時。',
			'日期以國際版 (endfield.gryphline.com) 為準。中國大陸版 (endfield.hypergryph.com) 未收錄。',
			'官方公告只用標題稱呼版本，從不用版本號。1.6 版是「丹青渡」；版本號出自玩家 wiki，「版本」索引頁列出每個版本號對應的標題。',
			'特許尋訪的機率提升 6 星幹員，在三期特許尋訪之後會移出特許尋訪名單，也不會加入基礎尋訪。各頁把尋訪列為附日期的歷史紀錄，不收錄限時活動；現在開放什麼，請查官方公告。',
			'同一個名稱有三種寫法：英文 (Laevatain)、繁體中文（萊萬汀）、簡體中文（莱万汀）。少數名稱不只是字體不同：Rossi 的繁體中文是洛西，簡體中文是洛茜。頁面網址用小寫英文名。',
			'本站並非官方網站。日期、尋訪、活動與名稱讀自官方公告與官方網站；技能文字與數值為遊戲資料 1.6 的遊戲內文字（由 warfarin.wiki 公開），並與 endfield.wiki.gg 核對。強度榜與配隊不收錄。戰鬥傷害公式出自 NGA 論壇的玩家實測。',
			'每一頁都有 Markdown 版本：去掉網址結尾的斜線，加上 `.md`。',
		],
		pages: '頁面',
		home: '首頁：各索引頁，索引頁列出所有頁面',
		full: '所有頁面合併成一個檔案',
		digest: '每一頁的答案、注意事項、日期與出處，不含內文',
		json: '所有語言的所有頁面與別名，JSON 格式',
		otherLanguage: '本索引的其他語言',
		more: '更多',
	},
	'zh-CN': {
		summary: '《明日方舟：终末地》(Arknights: Endfield) 的非官方资料站：版本、干员与系统，内容读自官方公告。',
		heading: '回答之前',
		notes: [
			'各页的日期与时间都是 Asia 服务器时间 (UTC+8)。Americas / Europe 服务器使用 UTC-5：版本更新维护在两边是同一时刻（当地前一天 17:00 至 23:00），限时内容则在各服务器自己时间的同一时刻开放与结束，相差 13 小时。',
			'日期以国际版 (endfield.gryphline.com) 为准。中国大陆版 (endfield.hypergryph.com) 未收录。',
			'官方公告只用标题称呼版本，从不用版本号。1.6 版是「丹青渡」；版本号出自玩家 wiki，「版本」索引页列出每个版本号对应的标题。',
			'特许寻访的概率提升 6 星干员，在三期特许寻访之后会移出特许寻访名单，也不会加入基础寻访。各页把寻访列为附日期的历史纪录，不收录限时活动；现在开放什么，请查官方公告。',
			'同一个名称有三种写法：英文 (Laevatain)、繁体中文（萊萬汀）、简体中文（莱万汀）。少数名称不只是字体不同：Rossi 的繁体中文是洛西，简体中文是洛茜。页面网址用小写英文名。',
			'本站并非官方网站。日期、寻访、活动与名称读自官方公告与官方网站；技能文字与数值为游戏数据 1.6 的游戏内文字（由 warfarin.wiki 公开），并与 endfield.wiki.gg 核对。强度榜与配队不收录。战斗伤害公式出自 NGA 论坛的玩家实测。',
			'每一页都有 Markdown 版本：去掉网址结尾的斜线，加上 `.md`。',
		],
		pages: '页面',
		home: '首页：各索引页，索引页列出所有页面',
		full: '所有页面合并成一个文件',
		digest: '每一页的答案、注意事项、日期与出处，不含正文',
		json: '所有语言的所有页面与别名，JSON 格式',
		otherLanguage: '本索引的其他语言',
		more: '更多',
	},
};

/** UI labels for the facts shown on every page, in both outputs. */
export const LABELS = {
	en: {
		appliesTo: 'Applies to',
		caveat: 'Caveat',
		effectiveDate: 'Source dated',
		lastVerified: 'Last verified',
		aliases: 'Also written',
		sources: 'Sources',
		art: 'Art',
		artBy: 'Hypergryph / Gryphline, from the official site',
		markdown: 'Markdown',
		page: 'Page',
		otherLanguage: 'Other language',
		allPages: 'All pages',
		home: 'Home',
		pageList: 'list of all pages',
		unofficial: 'unofficial',
		formats: 'Other formats of this page',
	},
	'zh-TW': {
		appliesTo: '適用範圍',
		caveat: '注意事項',
		effectiveDate: '來源日期',
		lastVerified: '最後查證',
		aliases: '其他寫法',
		sources: '出處',
		art: '美術',
		artBy: '鷹角網路／Gryphline，取自官方網站',
		markdown: 'Markdown',
		page: '頁面',
		otherLanguage: '其他語言',
		allPages: '所有頁面',
		home: '首頁',
		pageList: '所有頁面清單',
		unofficial: '非官方',
		formats: '本頁的其他格式',
	},
	'zh-CN': {
		appliesTo: '适用范围',
		caveat: '注意事项',
		effectiveDate: '来源日期',
		lastVerified: '最后查证',
		aliases: '其他写法',
		sources: '出处',
		art: '美术',
		artBy: '鹰角网络／Gryphline，取自官方网站',
		markdown: 'Markdown',
		page: '页面',
		otherLanguage: '其他语言',
		allPages: '所有页面',
		home: '首页',
		pageList: '所有页面清单',
		unofficial: '非官方',
		formats: '本页的其他格式',
	},
};

/** Format a Date (or date string) as YYYY-MM-DD. */
export function isoDate(d) {
	return new Date(d).toISOString().slice(0, 10);
}
