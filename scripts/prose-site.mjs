// Site settings for scripts/prose-review.mjs (the prose ledger).
//
// - derived: locales a script writes from another (Simplified Chinese from Traditional);
//   their prose is the source locale's, converted, and is read there.
// - skip(path, lang): text the page shows as the game gives it (pipeline/gametext.py,
//   records/story/): descriptions, names and story lines are the game's, not the site's prose.

import { readFileSync, existsSync } from 'node:fs';

const json = (rel) => JSON.parse(readFileSync(new URL(`../${rel}`, import.meta.url), 'utf8'));
const lines = (texts, lang) => texts.flatMap((t) => (t?.[lang] || '').split('\n')).filter(Boolean);

export default {
	derived: ['zh-cn'],
	skip(path, lang) {
		const bare = path.replace(/^(zh-tw|zh-cn|ja|ko)\//, '');
		const op = /^operators\/([a-z-]+)\/$/.exec(bare);
		if (op && existsSync(new URL(`../records/gametext/${op[1]}.json`, import.meta.url))) {
			const g = json(`records/gametext/${op[1]}.json`);
			const texts = [g.intro];
			for (const s of g.skills) texts.push(s.name, s.text, ...s.conditions.flatMap((c) => [c.name, c.text]));
			for (const t of g.talents) texts.push(t.name, ...t.levels.map((l) => l.text));
			for (const p of g.potentials) texts.push(p.name, p.text);
			for (const sk of json('records/base-skills.json').operators[op[1]] || []) texts.push(sk.name, ...sk.levels.map((l) => l.text));
			return lines(texts, lang);
		}
		if (bare === 'systems/gear/') return lines(json('records/gear-sets.json').flatMap((s) => [s.name, s.effect]), lang);
		const story = /^story\/([a-z-]+)\/$/.exec(bare);
		if (story && existsSync(new URL(`../records/story/${story[1]}.json`, import.meta.url))) {
			const rec = json(`records/story/${story[1]}.json`);
			const texts = [];
			const walk = (items) => items.forEach((it) => (it.choice ? it.choice.forEach(walk) : texts.push(it.text)));
			for (const f of rec.files) texts.push(f.title, f.text);
			for (const v of rec.voice) texts.push(v.title, v.text);
			for (const c of rec.chats) {
				texts.push(c.topic);
				walk(c.lines);
			}
			return lines(texts, lang);
		}
		return [];
	},
};
