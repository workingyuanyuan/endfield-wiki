// Shared site facts and URL rules. Plain JS so astro.config.mjs, Astro code and
// the check script all use the same rules.

// The public address, including the sub-path of a GitHub Pages project site, without a
// trailing slash. SITE_URL overrides it for local agent tests (see tests/agent-eval/README.md).
export const SITE = (process.env.SITE_URL ?? 'https://yuanaruru.com/endfield-wiki').replace(/\/+$/, '');
/** Scheme and host of SITE. */
export const ORIGIN = new URL(SITE).origin;
/** Sub-path the site is served under: `/endfield-wiki`, or the empty string at a domain root. */
export const BASE = new URL(SITE).pathname.replace(/\/+$/, '');
export const TITLE = { en: 'Endfield Wiki', 'zh-TW': '終末地 Wiki', 'zh-CN': '终末地 Wiki', ja: 'エンドフィールド Wiki', ko: '엔드필드 Wiki' };
export const DESCRIPTION =
	'Unofficial reference for the game Arknights: Endfield (明日方舟：終末地): versions, operators and systems, read from the official notices.';

/** Root-relative address for an `href` or `src` in HTML: the site path behind BASE. */
export function withBase(path) {
	return BASE + path;
}

/**
 * Locales: `dir` is the content sub-folder and URL prefix ('' = root); `maxDescription` is the
 * length limit of the one-sentence answer, in characters. A language may lack pages for a
 * time: `records/pending.json` lists the English pages it does not have yet.
 */
export const LOCALES = [
	{ dir: '', lang: 'en', label: 'English', maxDescription: 110 },
	{ dir: 'zh-tw', lang: 'zh-TW', label: '繁體中文', maxDescription: 70 },
	{ dir: 'zh-cn', lang: 'zh-CN', label: '简体中文', maxDescription: 70 },
	{ dir: 'ja', lang: 'ja', label: '日本語', maxDescription: 70 },
	{ dir: 'ko', lang: 'ko', label: '한국어', maxDescription: 90 },
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
			'One name has five spellings: English (Laevatain), Traditional Chinese (萊萬汀), Simplified Chinese (莱万汀), Japanese (レーヴァテイン) and Korean (레바테인); the Japanese and Korean ones are taken from the game. A few differ beyond the script: Rossi is 洛西 in Traditional and 洛茜 in Simplified Chinese. Page addresses use the lower-case English name.',
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
			'同一個名稱有五種寫法：英文 (Laevatain)、繁體中文（萊萬汀）、簡體中文（莱万汀）、日文（レーヴァテイン）、韓文（레바테인）；日文與韓文取自遊戲本身。少數名稱不只是字體不同：Rossi 的繁體中文是洛西，簡體中文是洛茜。頁面網址用小寫英文名。',
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
			'同一个名称有五种写法：英文 (Laevatain)、繁体中文（萊萬汀）、简体中文（莱万汀）、日文（レーヴァテイン）、韩文（레바테인）；日文与韩文取自游戏本身。少数名称不只是字体不同：Rossi 的繁体中文是洛西，简体中文是洛茜。页面网址用小写英文名。',
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
	ja: {
		summary: '『アークナイツ：エンドフィールド』(Arknights: Endfield) の非公式資料サイト：バージョン、オペレーター、システムを公式のお知らせから読み取ってまとめています。',
		heading: '回答の前に',
		notes: [
			'どのページの日付と時刻も Asia サーバー時間 (UTC+8) です。Americas / Europe サーバーは UTC-5 です。アップデートのメンテナンスは両サーバーで同じ時刻に行われ（UTC-5 では前日の 17:00 から 23:00）、期間限定コンテンツはそれぞれのサーバー時間の同じ時刻に始まって終わるため、13 時間ずれます。',
			'日付はグローバル版 (endfield.gryphline.com) のものです。中国本土版 (endfield.hypergryph.com) は扱いません。',
			'公式のお知らせはバージョンをタイトルで呼び、番号は使いません。1.6 は「丹青渡」です。番号はファン Wiki によるもので、バージョン索引ページ (/ja/versions/) が各番号とタイトルを対応させています。',
						'特別スカウトのピックアップ対象の★6オペレーターは、特別スカウト3回分の後に特別スカウトの対象から外れ、通常スカウトにも追加されません。各ページはスカウトを日付つきの履歴として載せ、期間限定イベントは扱いません。いま開催中のものは公式のお知らせで確認してください。',
			'1つの名前に5つの表記があります：英語 (Laevatain)、繁体字中国語（萊萬汀）、簡体字中国語（莱万汀）、日本語（レーヴァテイン）、韓国語（레바테인）。日本語と韓国語はゲーム内の表記です。字体の違いだけではないものもあります：Rossi は繁体字中国語で洛西、簡体字中国語で洛茜です。ページのアドレスは小文字の英語名です。',
			'このサイトは非公式です。日付、スカウト、イベント、名前は公式のお知らせと公式サイトから読み取っています。スキルの説明と数値はゲームデータ 1.6 のゲーム内テキスト（warfarin.wiki が公開）で、endfield.wiki.gg と照合しています。ティアリストと編成は載せていません。戦闘のダメージ計算式は NGA フォーラムのプレイヤー検証によるものです。',
			'どのページにも Markdown 版があります：URL 末尾のスラッシュを取り、`.md` を付けてください。',
		],
		pages: 'ページ',
		home: 'ホームページ：各索引ページ。索引ページがすべてのページを載せています',
		full: 'すべてのページを1つのファイルにまとめたもの',
		digest: '各ページの答え、注意点、日付、出典（本文なし）',
		json: 'すべての言語のすべてのページと別名（JSON）',
		otherLanguage: 'この索引の他の言語',
		more: 'その他',
	},
	ko: {
		summary: '「명일방주: 엔드필드」(Arknights: Endfield)의 비공식 자료 사이트: 버전, 오퍼레이터, 시스템을 공식 공지에서 읽어 정리했습니다.',
		heading: '답하기 전에',
		notes: [
			'모든 페이지의 날짜와 시각은 Asia 서버 시간(UTC+8)입니다. Americas / Europe 서버는 UTC-5를 씁니다. 업데이트 점검은 두 서버에서 같은 순간에 진행되고(UTC-5 기준 전날 17:00~23:00), 기간 한정 콘텐츠는 각 서버 시간의 같은 시각에 열리고 끝나므로 13시간 차이가 납니다.',
			'날짜는 글로벌 서비스(endfield.gryphline.com) 기준입니다. 중국 본토 서비스(endfield.hypergryph.com)는 다루지 않습니다.',
			'공식 공지는 버전을 번호가 아닌 제목으로만 부릅니다. 1.6 버전은 「단청도」입니다. 번호는 팬 위키에서 온 것이며, 버전 색인 페이지(/ko/versions/)가 각 번호와 제목을 짝지어 둡니다.',
						'특별 허가 헤드헌팅의 확률 업 6성 오퍼레이터는 특별 허가 헤드헌팅 3회가 지나면 특별 허가 헤드헌팅 대상에서 빠지고, 기초 헤드헌팅에도 추가되지 않습니다. 각 페이지는 헤드헌팅을 날짜가 붙은 기록으로 싣고 기간 한정 이벤트는 다루지 않습니다. 지금 열려 있는 것은 공식 공지에서 확인하세요.',
			'이름 하나에 표기가 다섯 가지 있습니다: 영어(Laevatain), 번체 중국어(萊萬汀), 간체 중국어(莱万汀), 일본어(レーヴァテイン), 한국어(레바테인). 일본어와 한국어는 게임 내 표기입니다. 글자체만 다른 것이 아닌 이름도 있습니다: Rossi는 번체 중국어로 洛西, 간체 중국어로 洛茜입니다. 페이지 주소는 소문자 영어 이름을 씁니다.',
			'이 사이트는 비공식 사이트입니다. 날짜, 헤드헌팅, 이벤트, 이름은 공식 공지와 공식 사이트에서 읽었습니다. 스킬 설명과 수치는 게임 데이터 1.6의 게임 내 텍스트(warfarin.wiki 공개)이며 endfield.wiki.gg와 대조했습니다. 티어 리스트와 덱 구성은 없습니다. 전투 대미지 공식은 NGA 포럼의 플레이어 실측에서 나왔습니다.',
			'모든 페이지에 Markdown 버전이 있습니다. URL 끝의 슬래시를 빼고 `.md`를 붙이세요.',
		],
		pages: '페이지',
		home: '홈페이지: 각 색인 페이지. 색인 페이지가 모든 페이지를 나열합니다',
		full: '모든 페이지를 한 파일로 합친 것',
		digest: '각 페이지의 답, 주의 사항, 날짜, 출처(본문 제외)',
		json: '모든 언어의 모든 페이지와 다른 이름(JSON)',
		otherLanguage: '이 색인의 다른 언어',
		more: '더 보기',
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
	ja: {
		appliesTo: '対象',
		caveat: '注意点',
		effectiveDate: '出典の日付',
		lastVerified: '最終確認',
		aliases: '別表記',
		sources: '出典',
		art: 'アート',
		artBy: 'Hypergryph／Gryphline、公式サイトより',
		markdown: 'Markdown',
		page: 'ページ',
		otherLanguage: '他の言語',
		allPages: 'すべてのページ',
		home: 'ホーム',
		pageList: 'ページ一覧',
		unofficial: '非公式',
		formats: 'このページの他の形式',
	},
	ko: {
		appliesTo: '적용 범위',
		caveat: '주의 사항',
		effectiveDate: '출처 날짜',
		lastVerified: '마지막 확인',
		aliases: '다른 표기',
		sources: '출처',
		art: '아트',
		artBy: 'Hypergryph / Gryphline, 공식 사이트에서',
		markdown: 'Markdown',
		page: '페이지',
		otherLanguage: '다른 언어',
		allPages: '모든 페이지',
		home: '홈',
		pageList: '페이지 목록',
		unofficial: '비공식',
		formats: '이 페이지의 다른 형식',
	},
};

/** Format a Date (or date string) as YYYY-MM-DD. */
export function isoDate(d) {
	return new Date(d).toISOString().slice(0, 10);
}
