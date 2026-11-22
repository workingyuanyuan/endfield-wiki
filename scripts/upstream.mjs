// Compares the sources of this site with what its pages were written from.
// upstream/README.md says what is watched, what each line of the report means and how to
// update the pages.
//
//   pnpm upstream            report. Exit 0: no difference. 1: differences. 2: the check could not be made
//   pnpm upstream --write    also record the notices and operator entries seen and the fingerprints
//                            of the cited notices in upstream/manifest.json (exit 0 whatever it reports)
//
// Four things are watched, read from the English pages, the pipeline scripts and the sources:
//
//   1. The official notice list (the bulletin API of web-news.gryphline.com), every page of it:
//      a new update notes, headhunting or Arsenal notice is a difference, and so is a new notice
//      in the "notices" tab that matches no known kind; any other new notice is a note. A cited
//      notice that leaves the list, or whose title or date changes, is a difference.
//   2. The text of the cited notices of the current version (from the earliest notice that the
//      newest version page cites): a SHA-256 in the manifest.
//   3. The game data tables that the pipeline reads (github.com/rmxlinux/EndfieldData), at the
//      newest commit against the commit the pages cite (COMMIT in pipeline/ed_extract.py).
//   4. The game data version shown by warfarin.wiki, and the entries of the official operator list.
//
// endfield.wiki.gg, Game8 and NGA are not watched (upstream/README.md says why).

import { createHash } from 'node:crypto';
import { readFileSync, writeFileSync, readdirSync, existsSync, mkdirSync } from 'node:fs';
import { dirname, join, relative } from 'node:path';
import { fileURLToPath } from 'node:url';

const ROOT = fileURLToPath(new URL('..', import.meta.url));
const DOCS = join(ROOT, 'src/content/docs');
const MANIFEST = join(ROOT, 'upstream/manifest.json');
const write = process.argv.includes('--write');

const API = 'https://web-news.gryphline.com/api/bulletin';
const QUERY = 'lang=en-us&code=arknights_endfield_official';
const PAGE_SIZE = 20; // the API cuts a larger pageSize to 20
const NOTICE_URL = /https:\/\/endfield\.gryphline\.com\/en-us\/news\/(\d+)/g;
const OPERATORS = 'https://endfield.gryphline.com/en-us/operator';
const WARFARIN = 'https://warfarin.wiki/en';
const REPO = 'rmxlinux/EndfieldData';
// The scripts that read the game data tables, and the one that holds the commit they read.
const TABLE_READERS = ['pipeline/ed_extract.py', 'pipeline/names_jako.py', 'pipeline/build_lists.py'];
const PINNING = ['pipeline/ed_extract.py', 'pipeline/names_jako.py'];
const TABLE_NAME = /\b[A-Z][A-Za-z0-9]*Table(?:_[A-Z]{2})?\b/g;
const TEXT_TABLE = /^I18nTextTable_/;
const GAME_DATA_URL = /https:\/\/github\.com\/rmxlinux\/EndfieldData\/(?:tree|blob)\/([0-9a-f]{40})/g;

// Kinds of notice. The first three are what the pages keep: versions, headhunting banners and
// Arsenal Issues (weapon banners). "Release Celebration [Hues of Passion] Details" was a banner.
const KINDS = [
	['new update notes', /\bupdate notes\b/i],
	['new headhunting notice', /\bheadhunting\b|\brelease celebration\b/i],
	['new arsenal notice', /\bissue\b.*\b(?:LTO|limited-time offer)\b|\bRE-Factor Issue\b/i],
];
// Previews of a version or its maintenance are notes, whatever else the title names.
const PREVIEW_TITLE = /pre-download|maintenance preview|DEV Comm|guide page/i;
// New notices of these kinds are notes: next-version previews, maintenance previews,
// pre-downloads, events, account actions, community and store news.
const NOTE_TITLE =
	/DEV Comm|guide page|pre-download|maintenance preview|suspension|\bevent\b|discord|whatsapp|comic|collaboration|\bFAQ\b|\btest\b|gift|compensation|steam|wishlist|sign-in|tribute|prize|linking|game tools|gallery|social media/i;

const LANGUAGE_DIRS = new Set(['zh-tw', 'zh-cn', 'ja', 'ko']);
// A plain client name, without personal details (see the root AGENTS.md).
const HEADERS = { 'user-agent': 'Mozilla/5.0 (compatible; docs-site-upstream-check)' };

const sha256 = (text) => createHash('sha256').update(text).digest('hex');
const day = (seconds) => new Date((seconds + 8 * 3600) * 1000).toISOString().slice(0, 10); // UTC+8
const pause = (ms) => new Promise((resolve) => setTimeout(resolve, ms));

/** Fetches a URL. Returns null for a 404, throws for any other failure; tries once more after a network error or a 5xx. */
async function request(url, { json = false, headers = {}, tries = 2 } = {}) {
	let res;
	let body;
	try {
		res = await fetch(url, { headers: { ...HEADERS, ...headers }, signal: AbortSignal.timeout(30_000) });
		if (res.ok) body = await res.text();
	} catch (error) {
		if (tries > 1) return retry();
		throw new Error(`${url}: ${error.cause?.code ?? error.name}`);
	}
	if (res.status === 404) return null;
	if ((res.status >= 500 || res.status === 429) && tries > 1) return retry();
	if (!res.ok) throw new Error(`${url}: HTTP ${res.status}`);
	if (!json) return body;
	try {
		return JSON.parse(body);
	} catch {
		throw new Error(`${url}: not JSON`);
	}
	async function retry() {
		await pause(Math.min(Number(res?.headers.get('retry-after')) || 5, 60) * 1_000);
		return request(url, { json, headers, tries: tries - 1 });
	}
}

/** The GitHub API. GITHUB_TOKEN, where set (the workflow sets it), raises the rate limit. */
function github(path) {
	const headers = { accept: 'application/vnd.github+json' };
	if (process.env.GITHUB_TOKEN) headers.authorization = `Bearer ${process.env.GITHUB_TOKEN}`;
	return request(`https://api.github.com/repos/${REPO}/${path}`, { json: true, headers });
}

/** The English pages: id (`operators/laevatain`), frontmatter and the notice ids they cite. */
function englishPages(YAML) {
	const pages = [];
	const walk = (dir) => {
		for (const entry of readdirSync(dir, { withFileTypes: true })) {
			const path = join(dir, entry.name);
			if (entry.isDirectory()) {
				if (dir !== DOCS || !LANGUAGE_DIRS.has(entry.name)) walk(path);
			} else if (entry.name.endsWith('.md')) {
				const text = readFileSync(path, 'utf8');
				const match = text.match(/^---\n([\s\S]*?)\n---/);
				if (!match) throw new Error(`${relative(ROOT, path)}: no frontmatter`);
				const cids = [...new Set([...text.matchAll(NOTICE_URL)].map((m) => m[1]))];
				pages.push({ id: relative(DOCS, path).replace(/\.md$/, ''), data: YAML.parse(match[1]), cids, text });
			}
		}
	};
	walk(DOCS);
	return pages.sort((a, b) => a.id.localeCompare(b.id));
}

/** One page of the notice list. */
async function listPage(n) {
	const res = await request(`${API}?${QUERY}&page=${n}&pageSize=${PAGE_SIZE}`, { json: true });
	if (res?.code !== 0 || !Array.isArray(res.data?.list) || typeof res.data.total !== 'number') {
		throw new Error(`notice list page ${n}: unexpected answer`);
	}
	return res.data;
}

/** Every notice in the list, by cid. The list holds sticky notices first, then the rest by date. */
async function readList() {
	for (let attempt = 1; ; attempt++) {
		const notices = new Map();
		const first = await listPage(1);
		const total = first.total;
		const pages = Math.ceil(total / PAGE_SIZE) + 2;
		let data = first;
		for (let n = 1; n <= pages; n++) {
			if (n > 1) data = await listPage(n);
			for (const item of data.list) {
				notices.set(String(item.cid), { cid: String(item.cid), title: item.title, date: day(item.displayTime), tab: item.tab });
			}
			if (data.list.length === 0 || notices.size >= total) break;
		}
		if (total > 0 && notices.size === total) return notices;
		// A notice published or removed during the reading shifts the pages: read them again once.
		if (attempt === 2) throw new Error(`the notice list gave ${notices.size} notices, not the ${total} it states`);
		await pause(5_000);
	}
}

/** The text of a notice: title and body, tags dropped, cells and blocks kept apart. Null when the notice is gone. */
async function noticeText(cid, JSDOM) {
	const res = await request(`${API}/${cid}?${QUERY}`, { json: true });
	if (res === null || res.code === 1500) return null; // "公告不存在" comes with HTTP 200
	const html = res?.data?.data;
	if (res?.code !== 0 || typeof html !== 'string' || html.trim() === '') throw new Error(`notice ${cid}: unexpected answer`);
	const marked = html.replace(/<\/(td|th)>/gi, ' | </$1>').replace(/<(br|\/p|\/div|\/li|\/tr|\/h\d)\b[^>]*>/gi, '\n$&');
	const body = new JSDOM(`<body>${marked}</body>`).window.document.body.textContent;
	const text = `${res.data.title}\n${body}`
		.split('\n')
		.map((line) => line.replace(/\s+/g, ' ').trim())
		.filter(Boolean)
		.join('\n');
	return text;
}

/** The blob SHA of every file in TableCfg/ at a commit. */
async function tables(commit) {
	const root = await github(`git/trees/${commit}`);
	const dir = root?.tree?.find((entry) => entry.path === 'TableCfg' && entry.type === 'tree');
	if (!dir) throw new Error(`${REPO} ${commit.slice(0, 7)}: no TableCfg folder`);
	const tree = await github(`git/trees/${dir.sha}`);
	if (!tree || tree.truncated) throw new Error(`${REPO} ${commit.slice(0, 7)}: TableCfg listing truncated or missing`);
	return new Map(tree.tree.filter((e) => e.type === 'blob').map((e) => [e.path.replace(/\.json$/, ''), e.sha]));
}

/** The entries of the official operator list. */
function parseOperators(html, JSDOM) {
	const doc = new JSDOM(html).window.document;
	return [...doc.querySelectorAll('[class*="OperatorItem_operatorItem__"]')].map((item) => ({
		key: item.querySelector('[class*="OperatorItem_image__"]')?.getAttribute('data-key') ?? '',
		name: item.querySelector('[class*="OperatorItem_nameText__"]')?.textContent.trim() ?? '',
		rarity: item.querySelector('[data-rarity]')?.getAttribute('data-rarity') ?? '',
		icons: [...item.querySelectorAll('[class*="OperatorItem_icon__"]')].map((icon) => icon.getAttribute('data-key')).join(' '),
	}));
}

async function main() {
	// Imported here, so that a failure to load them is "check not made" (exit 2), not exit 1.
	const YAML = (await import('yaml')).default;
	const { JSDOM } = await import('jsdom');
	if (!write && !existsSync(MANIFEST)) throw new Error('upstream/manifest.json is missing; run --write once the pages agree with the sources');
	const old = existsSync(MANIFEST) ? JSON.parse(readFileSync(MANIFEST, 'utf8')) : { notices: [], cited: {}, operators: [] };
	if (!Array.isArray(old.notices) || !Array.isArray(old.operators) || typeof old.cited !== 'object' || old.cited === null) {
		throw new Error('upstream/manifest.json lacks notices, cited or operators');
	}
	const oldNotices = new Map(old.notices.map((n) => [n.cid, n]));
	const oldCited = old.cited;
	const oldOperators = new Map(old.operators.map((o) => [o.key, o]));

	const pages = englishPages(YAML);
	const differences = [];
	const notes = [];
	const failures = [];
	const counts = {};
	const attempt = async (what) => {
		try {
			await what();
		} catch (error) {
			failures.push(error.message);
		}
	};

	// What the pages cite.
	const citedBy = new Map();
	for (const { id, cids } of pages) for (const cid of cids) citedBy.set(cid, [...(citedBy.get(cid) ?? []), id]);
	const by = (cid) => `cited by ${citedBy.get(cid).join(', ')}`;
	const versionPages = pages
		.filter(({ id }) => /^versions\/\d+-\d+$/.test(id))
		.map((page) => ({ page, v: page.id.slice(9).split('-').map(Number) }))
		.sort((a, b) => b.v[0] - a.v[0] || b.v[1] - a.v[1]);
	if (versionPages.length === 0) throw new Error('no version pages');
	const current = versionPages[0].page;
	if (current.cids.length === 0) throw new Error(`${current.id}: cites no official notice`);

	// 1. The notice list.
	let notices = new Map();
	await attempt(async () => {
		notices = await readList();
		counts.list = notices.size;
		const known = new Set([...oldNotices.keys(), ...citedBy.keys()]);
		for (const n of notices.values()) {
			if (known.has(n.cid)) continue;
			const line = `${n.cid}: ${n.title} (${n.date}, ${n.tab}) https://endfield.gryphline.com/en-us/news/${n.cid}`;
			const kind = PREVIEW_TITLE.test(n.title) ? null : KINDS.find(([, pattern]) => pattern.test(n.title))?.[0];
			if (kind) differences.push(`${kind}: ${line}`);
			else if (n.tab === 'notices' && !NOTE_TITLE.test(n.title)) differences.push(`new notice to classify: ${line}`);
			else notes.push(`note: new notice: ${line}`);
		}
		for (const cid of citedBy.keys()) {
			const now = notices.get(cid);
			const was = oldNotices.get(cid);
			if (!now) {
				// Gone from the list: the notice itself says whether it is gone.
				if ((await noticeText(cid, JSDOM)) === null) differences.push(`cited notice gone: ${cid}: ${by(cid)}`);
				else differences.push(`cited notice left the list: ${cid}: ${by(cid)}`);
			} else if (was && (was.title !== now.title || was.date !== now.date)) {
				differences.push(`cited notice changed: ${cid}: title or date, now "${now.title}" (${now.date}), ${by(cid)}`);
			}
		}
	});

	// 2. The text of the cited notices of the current version: from the earliest notice its page cites.
	const cited = {};
	const since = current.cids.map((cid) => notices.get(cid)?.date).filter(Boolean).sort()[0];
	if (notices.size && !since) failures.push(`${current.id}: none of its notices is in the list`);
	for (const cid of [...citedBy.keys()].sort()) {
		const n = notices.get(cid) ?? oldNotices.get(cid); // a notice that left the list keeps its recorded date
		if (!since || !n || n.date < since) continue;
		await attempt(async () => {
			const text = await noticeText(cid, JSDOM);
			if (text === null) return differences.push(`cited notice gone: ${cid}: ${by(cid)}`);
			cited[cid] = { title: n.title, sha256: sha256(text), characters: text.length };
			if (!oldCited[cid]) differences.push(`not in the manifest: ${cid}: ${n.title}, ${by(cid)}`);
			else if (oldCited[cid].sha256 !== cited[cid].sha256) differences.push(`cited notice changed: ${cid}: text, ${n.title}, ${by(cid)}`);
			await pause(1_000);
		});
	}
	counts.cited = Object.keys(cited).length;

	// 3. The game data tables the pipeline reads, at the newest commit against the pinned one.
	await attempt(async () => {
		// The commit the pages cite is the baseline; the scripts that hold a COMMIT must name the same one.
		const cites = [...new Set(pages.flatMap(({ text }) => [...text.matchAll(GAME_DATA_URL)].map((m) => m[1])))];
		if (cites.length !== 1) throw new Error(`the pages cite ${cites.length} EndfieldData commits (${cites.join(', ')}), not one`);
		const pinned = cites[0];
		for (const file of PINNING) {
			const commit = readFileSync(join(ROOT, file), 'utf8').match(/^COMMIT = '([0-9a-f]{40})'/m)?.[1];
			if (commit !== pinned) throw new Error(`${file}: COMMIT ${commit ?? 'missing'} is not the commit the pages cite, ${pinned.slice(0, 7)}`);
		}
		const names = [...new Set(TABLE_READERS.flatMap((file) => readFileSync(join(ROOT, file), 'utf8').match(TABLE_NAME) ?? []))].sort();
		if (names.length < 15) throw new Error(`only ${names.length} table names found in the pipeline scripts`);
		const head = (await github('commits/HEAD'))?.sha;
		if (!head) throw new Error(`${REPO}: no newest commit`);
		counts.tables = `${names.length} tables at ${head.slice(0, 7)}`;
		if (head === pinned) return;
		const [before, after] = [await tables(pinned), await tables(head)];
		const read = new Set(names);
		for (const name of names) {
			if (!before.has(name)) throw new Error(`${name}: not in TableCfg at ${pinned.slice(0, 7)}`);
			if (before.get(name) === after.get(name)) continue;
			const line = after.has(name)
				? `${name}: ${pinned.slice(0, 7)}..${head.slice(0, 7)} https://github.com/${REPO}/compare/${pinned.slice(0, 7)}...${head.slice(0, 7)}`
				: `${name}: gone at ${head.slice(0, 7)} (pages cite ${pinned.slice(0, 7)})`;
			if (TEXT_TABLE.test(name)) notes.push(`note: game text changed: ${line}`);
			else differences.push(`game data changed: ${line}`);
		}
		const other = [...after].filter(([name, sha]) => !read.has(name) && before.get(name) !== sha).length;
		if (other) notes.push(`note: game data commit: ${head.slice(0, 7)}: ${other} tables changed that the pipeline does not read`);
	});

	// 4a. The game data version that warfarin.wiki shows, against "game data X.Y" in the pages.
	await attempt(async () => {
		const html = await request(WARFARIN);
		const shown = html?.replace(/<!-- -->/g, '').match(/Current Version:\s*<\/span>\s*<span>v([\d.]+)</)?.[1];
		if (!shown) throw new Error(`${WARFARIN}: no "Current Version" found`);
		const cited = [...new Set(pages.flatMap(({ data }) => [...String(data.appliesTo ?? '').matchAll(/game data (\d+\.\d+)/g)].map((m) => m[1])))];
		counts.warfarin = `v${shown}`;
		if (cited.some((v) => v !== shown)) differences.push(`game data version: warfarin.wiki: shows v${shown}, the pages say game data ${cited.join(', ')}`);
	});

	// 4b. The official operator list. An entry with an operator page here that changes or leaves is a
	// difference; a new entry is a note (next-version operators are listed before their release).
	const operators = [];
	await attempt(async () => {
		const html = await request(OPERATORS);
		const entries = html === null ? [] : parseOperators(html, JSDOM);
		if (entries.length < 34 || entries.some((e) => !e.key || !e.name)) throw new Error(`${OPERATORS}: ${entries.length} entries read, or an entry without key or name`);
		operators.push(...entries);
		counts.operators = entries.length;
		const paged = new Set(pages.filter(({ id }) => id.startsWith('operators/') && id !== 'operators/index').map(({ data }) => data.title));
		const now = new Map(entries.map((e) => [e.key, e]));
		const show = (e) => `${e.name}, ${e.rarity}-star, ${e.icons}`;
		for (const e of entries) {
			const was = oldOperators.get(e.key);
			if (!was) { if (existsSync(MANIFEST)) notes.push(`note: new operator entry: ${e.key}: ${show(e)}`); continue; }
			if (show(was) === show(e)) continue;
			const line = `${e.key}: was ${show(was)}, now ${show(e)}`;
			if (paged.has(was.name) || paged.has(e.name)) differences.push(`operator entry changed: ${line}`);
			else notes.push(`note: operator entry changed: ${line}`);
		}
		for (const was of oldOperators.values()) {
			if (now.has(was.key)) continue;
			if (paged.has(was.name)) differences.push(`operator entry gone: ${was.key}: ${show(was)}`);
			else notes.push(`note: operator entry gone: ${was.key}: ${show(was)}`);
		}
	});

	for (const line of [...differences, ...notes]) console.log(line);
	const summary = [
		`${counts.list ?? 0} notices in the list`,
		`${counts.cited} cited notices of ${current.id} read`,
		counts.tables && `${counts.tables}`,
		counts.warfarin && `warfarin.wiki ${counts.warfarin}`,
		`${counts.operators ?? 0} operator entries`,
		`${pages.length} pages`,
	].filter(Boolean);
	console.log(`${summary.join(', ')}; ${differences.length} differences, ${notes.length} notes.`);
	if (failures.length) throw new Error(failures.join('; '));

	if (write) {
		const manifest = {
			api: `${API}?${QUERY}`,
			read: new Date().toISOString().slice(0, 10),
			notices: [...notices.values(), ...[...citedBy.keys()].filter((cid) => !notices.has(cid) && oldNotices.has(cid)).map((cid) => oldNotices.get(cid))].sort((a, b) => b.date.localeCompare(a.date) || b.cid.localeCompare(a.cid)),
			cited,
			operators,
		};
		mkdirSync(dirname(MANIFEST), { recursive: true });
		writeFileSync(MANIFEST, JSON.stringify(manifest, null, '\t') + '\n');
		console.log('manifest updated.');
		return 0;
	}
	return differences.length ? 1 : 0;
}

try {
	process.exitCode = await main();
} catch (error) {
	console.error(`check not made: ${error.message}`);
	process.exitCode = 2;
}
