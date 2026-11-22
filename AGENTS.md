# Rules for agents maintaining this site

This site is an unofficial wiki for the game Arknights: Endfield (明日方舟：終末地; Hypergryph, published outside mainland China by Gryphline). Its first readers are AI agents; humans come second. The rules in `../AGENTS.md` apply; this file holds what is specific to this site.

State on 2026-11-22: the owner approved the look on the sample pages; all pages were written, rewritten after the owner's feedback below, then extended with the game's recommended weapons, base skills, Dijiang and recipes by product (60 pages per language). Published on 2026-11-22 at `https://yuanaruru.com/endfield-wiki/` from `github.com/workingyuanyuan/endfield-wiki` (public; deploy by the workflow, which runs `pnpm verify`). The user site's `SITES` entry and home page rows were requested from the session working on that repository, which had uncommitted changes.

## Decisions by the owner (2026-11-21)

- Languages: English at the root, Traditional Chinese (`/zh-tw/`), Simplified Chinese (`/zh-cn/`, written by script from `zh-tw`).
- Scope of the first release: about 55 to 60 pages per language. Versions 1.0 to 1.6 (7), one page per operator (34 to 37), a names page, 10 to 12 pages on systems and AIC (headhunting and guarantees, combat, weapons, gear sets, AIC power, logistics and production chains, regional development, platforms and servers). No page per weapon, gear piece, facility, item or enemy.
- How pages are produced: a mix. Records from which a script writes the Markdown for operators, index pages, the names page and lookup tables; hand-written Markdown for version pages and system pages. The scripts are `pipeline/build_pages.py` (operator pages) and `pipeline/build_lists.py` (names, weapons); they read `records/` only.
- How the home page reaches every page: it links index pages (`versions/`, `operators/`, `systems/`, `aic/`), and each index page links every page of its section within its first 5,000 extracted characters. `scripts/check-dist.mjs` fails for a page that neither the home page nor an index page links.
- Sources of numbers: the game data that warfarin.wiki publishes (it states "Current Version v1.6") is accepted for in-game text and numbers. Read only the pages needed, do not crawl (its `robots.txt` carries `ai-train=no, use=reference` and it states no licence), restate in our own words and tables, and check samples against the official notices and endfield.wiki.gg.
- Service covered: the global service (Asia and Americas / Europe servers). Mainland China is not covered. This follows `nte-wiki`; the owner was told and did not object.
- Look: taken from the official site (white ground, grey panels, near-black ink, signal yellow `#fffa00`, square corners, small spaced labels, a double slash before section names). No wordmark, image or font of the publisher. Motion (owner's request, 2026-11-22, in place of the earlier "no motion"; the owner approved the motion and the favicon from demo videos the same day): modelled on the official site and the login screen, measured that day: 0.2–0.3 s responses to the pointer, a flicker-in for the title and section headings, a yellow line that draws once under the header and along each section rule, a wipe for the answer and for tables, and a cross-document view transition that keeps the header and sidebar still. Each plays once; nothing loops; images do not move; all of it sits inside `prefers-reduced-motion: no-preference`, and a block waits unseen for its entrance only while the script runs (on screen, not in print). The code is the motion section at the end of `src/styles/endfield.css` and the script in `src/components/SiteTitle.astro`. Favicon (`public/favicon.svg`, 2026-11-22): a yellow inverted triangle with a cut on near-black, drawn for this site; the earlier one was copied from the NTE wiki by mistake.
- Official art is used, by the owner's decision, as on `nte-wiki`. The publisher's Fan Content and Streaming Guidelines (notice 4497, 2026-02-03) prohibit "content that directly copies or uses excerpts of the Company's official materials and lacks clear originality"; the owner chose before that text was read and has been told. Credits go in the `art` frontmatter field. Remove an image when the publisher asks.
- Who lets a change go live: the owner confirms every time.
- Address: `https://yuanaruru.com/endfield-wiki/`.

## Decisions by the owner after reading the preview (2026-11-21)

The owner does not play the game and cannot audit the facts; they judge the pages as a reader and asked for the `nte-wiki` way of working.

- Short titles, without a subtitle after a colon: the sidebar shows them. The question words go in the description and the headings.
- No citation phrases in the prose ("official notices say", "Endfield Talos Wiki lists", "the game data shows"). The page notes name the sources. A sentence names a source only where two sources disagree on something a reader acts on, or where one player test (NGA) is the only source; then once per section.
- No disclaimers: nothing about what is unknown, unannounced, or true "as of" a date. State the positive fact or leave it out.
- Time-limited content stays out: events, limited shops and sales, sign-ins, compensation, pre-downloads, protocol passes, collaborations, the next version, the end of the current one. Headhunting banners and Arsenal Issues stay as a dated history on version and operator pages. Operator pages say nothing that depends on the day they are built. `systems/banner-history` was removed for this reason.
- One clock: dates and times are Asia server time (UTC+8), without a label beside each. The home page caveat, `systems/servers-and-time` and `llms.txt` state once how the Americas / Europe server (UTC-5) relates.
- Player research from the NGA forum (board `fid=846`, mainland players) may serve as a source, as on `nte-wiki`: the combat damage formula comes from the guide 「终末地数据机制导论」 (`tid=46094556`). Player questions from its 提问求助 sub-board went into the question list.
- `pipeline/check_prose.py` checks a page for these four kinds of wording; run it with `lint_page.py` on every hand-written page.

## Expansion and strategy (2026-11-22)

The owner approved the expansion plan (audit the five partial answers, recommended weapons and base skills on operator pages, reverse lookups, a Dijiang page, an enemy table pilot) and asked how the site stands against the publisher's own wiki, `wiki.skport.com/endfield`, which they called the best source and the biggest competitor.

- Measured that day: every URL of the official wiki, `robots.txt`, `sitemap.xml` and `llms.txt` included, returns the same 4 KB JavaScript shell with one title and description; entries load from an API that answers 401 without a token the page fetches for itself; the home page has no links to entries. A fetch-only agent gets nothing from it. One web search (one engine, one run) returned no page of it. It is edited by players with the official team (edit log, contribution rank), updated within the hour, in eight languages without Simplified Chinese, and an operator entry is deeper than ours (stats per level, every skill level, voice lines, gallery).
- Strategy, agreed by Fable, Astra and Neon (`~/.local/state/delegation-log/docs-sites/20261122-strategy.*`): readability for agents is a head start that ends if the official wiki renders on the server; the lasting advantage is answers that span entries (which weapon for which operator and back, which operator for which room, which facility for which product), the qualifier next to the fact, version history, player-tested mechanics and Simplified Chinese. Do not race it on depth per entry. Use it as a second witness for fields the game generates (recommendations, base skills), read in a browser at a human pace, never through its API. Question words go in descriptions and headings; titles stay short. Search competitors are guide sites and community wikis.
- Decided by the owner on 2026-11-22, where the advisors disagreed: no links from operator pages to official wiki entries, and no line in `llms.txt` about the official wiki needing JavaScript. Publish before the enemy table. Our records are not published as JSON (all three advisors: later or not at all).
- Kay and Mimino have entries marked as previews on the official wiki: next-version content, left out.
- Pages added: `systems/dijiang` and `aic/recipes` (generated by `build_lists.py`); operator pages gained Recommended weapons and Base skills; the weapons list gained Essence stats and Recommended for. The enemy table pilot is not built: resistances sit in attribute tables not yet read, and regions come from distribution codes.
- Found while building: 19 AIC recipes use items the game describes as made "during a special period" (event items: Chubby Lung, Xiranite gourds, Proto Xiranite, Proto Xiran-Cuprium); they were in the facility counts of `aic/production` and were removed there.

## Advisors (2026-11-21)

Astra and Neon were asked before building (briefs and answers in `~/.local/state/delegation-log/docs-sites/20261121-205412-*`). Adopted from both: no page per item, authority by kind of fact, two sites that share one data mine count as one source, resolve the 37 against 34 operator count before writing, every page names its version. They disagreed on scope (about 16 pages on AIC problems against about 55 to 60), on production (all records against a mix) and on the home page (direct links against index pages); the owner chose the second in each case.

## Who wrote what, and what was checked (2026-11-21)

Briefs and answers are in `~/.local/state/delegation-log/docs-sites/` (files of 2026-11-21).

| Work | Writer | Check |
| --- | --- | --- |
| Home, index pages, Version 1.6, Laevatain's text, records of banners, versions, changes and how operators are obtained | The main agent, from the notices | `lint_page.py` (every date against the cited notices) |
| Version pages 1.0 to 1.5, English and Traditional Chinese | Three Claude Opus subagents, from the cached notices | `lint_page.py`; an independent reader for all six (Astra for 1.1 and 1.4, a Claude Opus subagent for the rest) |
| Restated text of 33 operators (introduction, skills, talents, potentials), both languages | Neon (`gemini-4-neon-medium`), seven batches, from source sheets of the game text | `check_text.py` on every record; Astra read all 33 against the sheets. It found 21 wrong statements (half of them in the introductions), 16 mismatches between the two languages and 2 wrong terms; all were fixed. It also flagged about 80 short lines as close to the game's wording (stat lines, the basic attack line); those were left |
| Headhunting, Arsenal, servers and time, platforms | Two Claude Opus subagents, from notices and Endfield Talos Wiki | Astra for headhunting and servers and time (4 wrong statements on headhunting, fixed); a Claude Opus subagent for Arsenal and platforms |
| Combat, operator progression, gear, the four AIC pages | Two Claude Opus subagents, from game data, in-game tutorials and Endfield Talos Wiki | A Claude Opus subagent read all seven against the sources |
| Operator pages, banner history, names, weapons | Scripts, from `records/` | The scripts assert the three-banner rule and the description lengths; `pnpm verify` |
| Simplified Chinese | `scripts/to-zh-cn.py` | Names compared with the game's Simplified text by `pipeline/names_voc.py`; parity checks of `pnpm verify` |

| Rewrite after the owner's feedback (titles, citation phrases, disclaimers, time-limited content, one clock): versions; headhunting, Arsenal, servers and time, platforms, operator progression; combat, gear, AIC | Three Claude Opus subagents, from the existing pages; new sections from Endfield Talos Wiki (Essences, Coolant Gel), the NGA guide `tid=46094556` (damage formula) and NGA player threads (headhunting questions) | `check_prose.py` and `lint_page.py` on every page; Astra read the new sections of headhunting, Arsenal and combat against their sources (9, 1 and 9 findings), a Claude Opus subagent applied them |
| Home page, operator page script, `llms.txt` notes | The main agent | `check_prose.py`, `pnpm verify` |
| Expansion of 2026-11-22: qualifiers of q11, q13, q18, q27 moved next to their answers; recommended weapons, base skills, Essence stats, `systems/dijiang`, `aic/recipes`; event recipes out of `aic/production` | The main agent; generated parts by `ed_extract.py` and the page scripts | `check_prose.py`, `lint_page.py`, `pnpm verify`; a script compared 32 fields of 7 operators with the official wiki (all equal) and the 25 rows of the hand-written recipe table on `aic/production` with `aic/recipes` (all equal); the in-game tutorials agree with the combat glossary and give no number for Stagger, so ×1.3 stays an NGA player value |

Astra (Codex) reached its usage limit after four reviews, so the last two reviews went to Claude Opus subagents with the same briefs: a reader of the same model family as the writers, in a fresh context.

Agent test after the expansion (2026-11-22; the five partial questions again and five new ones, q28 to q32; one Claude Sonnet reader, one run, local): 10 pass with 16 fetches, q13 after one more move of its qualifier; `tests/agent-eval/results/2026-11-22-expansion/scores.md`. Agent test after the rewrite (27 questions, five replaced by timeless ones and three from NGA, one Claude Sonnet reader, one run, local): 22 pass, 5 partial, 0 fail with 38 fetches; `tests/agent-eval/results/2026-11-21-rewrite/scores.md`. Agent test of 2026-11-21 (24 questions, one Claude Sonnet reader per side, one run): this site 23 pass, 1 partial, 0 fail with 23 fetches; original sources 6 pass, 12 partial, 6 fail with 47 fetches. Details and limits in `tests/agent-eval/results/2026-11-21/scores.md`.

## Commands

```
pnpm verify      # build, then run the acceptance checks. Run this before you call a change done.
pnpm build       # build
pnpm check       # acceptance checks on an existing dist/
python3 -I pipeline/build_pages.py     # operator pages (en, zh-tw) from records/
python3 -I pipeline/build_lists.py     # names, weapons (en, zh-tw) from records/
uv run --with opencc-python-reimplemented scripts/to-zh-cn.py   # write the zh-cn pages from the zh-tw pages
python3 -I pipeline/lint_page.py <page.md> [...]                # check one page without a build
python3 -I pipeline/check_prose.py <page.md> [...]              # citation phrases, disclaimers, time-limited content, a second server's dates
python3 -I pipeline/check_text.py <sheet.json> records/text/<slug>.json   # check one operator's restated text
pnpm preview     # serve dist/ at http://127.0.0.1:4398/endfield-wiki/ with GitHub Pages style headers
python3 -I pipeline/notice_text.py cache/official/art/en-us-<cid>.json   # an official notice from the cache as text
python3 -I pipeline/extract_official_operators.py <page script .js> cache/official/operators.json
python3 -I pipeline/wf_extract.py cache/third/wf/<lang>-<slug>.html [...]   # a cached game-data page to JSON
python3 -I pipeline/build_records.py   # facts part of records/operators/ from the cached game data
python3 -I pipeline/text_sheet.py <out dir> <slug> [...]   # the sheet a writer restates an operator from
python3 -I pipeline/wf_misc.py         # terms, tutorials, facilities, weapons, gear sets from the cache
python3 -I pipeline/ed_extract.py      # recommended weapons, base skills, Essence stats, recipes from cache/third/ed/<commit>/
uv run --with opencc-python-reimplemented pipeline/names_voc.py   # names whose Simplified form is not a plain conversion
```

After a change to a record: `build_pages.py`, `build_lists.py`, `to-zh-cn.py`, then `pnpm verify`. After new game data: fetch the pages again into `cache/third/wf/` (the fetch scripts are kept there), then `wf_extract.py`, `build_records.py`, `names_voc.py`, and restate what changed in `records/text/`.

## Content rules

- Pages live in `src/content/docs/` (English), `src/content/docs/zh-tw/` and `src/content/docs/zh-cn/`. Addresses use the official English name in lower case with hyphens: `operators/laevatain`, `operators/last-rite`, `versions/1-6`. A section's index page is `<section>/index.md`.
- Do not edit `zh-cn` pages by hand. Run `scripts/to-zh-cn.py` after every change to a `zh-tw` page. When a `zh-tw` page brings in a new name, compare it with the mainland site and add a pair to `VOC` when the two differ beyond the script (one did: 洛西 / 洛茜, Rossi). A table whose header names both 繁體中文 and 簡體中文 keeps its rows as written. A sentence that quotes a Traditional name needs an entry in `FIXES`.
- Every page has `aliases`: the title and aliases together are the same set of strings in every language, and the Simplified title must be among the aliases of the `zh-tw` page.
- Write links and images root-relative and without the site's sub-path: `/operators/laevatain/`, `/art/operators/laevatain.webp`. In `zh-tw` pages, links start with `/zh-tw/`; image paths do not.
- Quote a frontmatter value that contains a colon followed by a space (`"Arknights: Endfield ..."`).
- Times: Asia server time (UTC+8), written without a label. "Server time" in a notice is UTC+8 on the Asia server and UTC-5 on the Americas / Europe server; a maintenance window is the same six hours on both (06:00 to 12:00 UTC+8 is 17:00 to 23:00 UTC-5 the day before). A banner that closes "before version update and maintenance" ends at "End of Version x"; do not infer a date.
- Version numbers are not in official notices; they come from Endfield Talos Wiki (source in the page notes of `versions/`). Pages give the number with the title.
- Names: English from the en-us notices, Traditional Chinese from the zh-tw notices, Simplified Chinese from the mainland site or the game's Simplified text. Chinese pages use the game's own Chinese names for skills, states and terms.
- Skill and talent effects are restated in our own words, short; names stay as in the game. No tier lists, team builds or damage rankings.
- Do not write `//` in page text: the skin draws it before section names and the check script treats it as a leak.
- Operator pages and `systems/names`, `systems/weapons` are written by script. Do not edit them: change the record or the script. `records/operators/<slug>.json` holds names and numbers from the game data (rebuilt by `build_records.py`); `records/text/<slug>.json` holds the restated introduction, skills, talents and potentials in English and Traditional Chinese (written by hand or by a delegate, checked with `check_text.py`); `records/banners.json`, `versions.json`, `obtain.json`, `changes.json`, `weapons.json` are hand-kept from the notices and the game data. `records/recommend.json`, `base-skills.json`, `weapon-essence.json` and `recipes.json` are written by `ed_extract.py` from the game tables; base-skill effects are stored as a kind and a number, and the scripts word them. The game's own description text is never committed: it stays in `cache/`.
- A skill's own SP cost, Ultimate Energy cost and combo cooldown are added to the table by the script from the record; the restated text does not repeat them.
- Pronouns in restated text: the operator's name, or the pronoun the game text or an official notice itself uses for that operator.
- Operator pages follow one structure: portrait, Profile, How to obtain, Recommended weapons, Skills, Skill values (the game's value rows at skill level 1 and 12), Talents, Potentials, Base skills, Base stats, Promotion materials, Changes since release. Portraits are the card images of the official operator list (303 by 386 px), converted to WebP in `public/art/operators/<slug>.webp`.

## Skin rules

- The skin is `src/styles/endfield.css`. Heading font: Lexend (SIL OFL 1.1, from `@fontsource-variable/lexend`); Chinese uses system fonts, with Simplified ones on `zh-CN` pages.
- In the light theme yellow is a ground colour only (highlight under links, selected row, marks); text accents are ink. In the dark theme yellow carries links.
- Text drawn with CSS `content`: the double slash before `h2`. A pattern for it is in check 5 of `scripts/check-dist.mjs`.
- Three Starlight components are overridden: `SiteTitle`, `MarkdownContent`, `ThemeSelect`.
- Screenshots: `preview/endfield-wiki/` one level up. Headless Chromium needs `FONTCONFIG_FILE` pointing at a config that adds `/mnt/c/Windows/Fonts`.

## Where things are

| Path | Role |
| --- | --- |
| `src/lib/site.mjs` | Site URL and sub-path, locales, URL rules, `llms.txt` notes, labels |
| `src/lib/`, `src/pages/` | Markdown twins, `llms.txt`, bundles, `index.json`, `robots.txt`, sitemap options |
| `src/components/`, `src/styles/endfield.css` | The three overrides and the skin |
| `scripts/check-dist.mjs`, `scripts/check-found.mjs` | Acceptance checks |
| `scripts/to-zh-cn.py` | Writes the Simplified Chinese pages from the Traditional Chinese ones |
| `pipeline/` | Scripts that read the cached sources, build the records and write the generated pages |
| `records/` | The site's own data, committed: operators (facts and restated text), banners, versions, how operators are obtained, changes per operator, weapons, name pairs for the Simplified pages, `pages.txt` (every page of the site, used by the link check of `lint_page.py`) |
| `cache/` | Copies of sources, not committed: `official/list-all.json` (all 135 notices, en-us and zh-tw), `official/art/<lang>-<cid>.json` (full text of the 2026 notices), `official/operators.json`, `third/wf/` (warfarin.wiki pages and what was cut from them: operators, terms, tutorials, facilities, weapons, gear sets), `third/wg/` (Endfield Talos Wiki wikitext), `sheets/` (source sheets for restating) |
| `tests/agent-eval/questions.json` | The site's question list, with the expected answer, the qualifier and the page for each |

## Sources checked on 2026-11-21 (plain HTTP fetch unless noted)

| Source | Result | Use |
| --- | --- | --- |
| `web-news.gryphline.com/api/bulletin?lang=<en-us or zh-tw>&code=arknights_endfield_official&page=<n>&pageSize=20` | JSON list of all notices, 135 on this date; `pageSize` above 20 is cut to 20 | Finding notices |
| `web-news.gryphline.com/api/bulletin/<cid>?lang=...&code=arknights_endfield_official` | Full text of a notice as HTML in JSON. The public page is `endfield.gryphline.com/<lang>/news/<cid>`, readable too | Primary: dates, banners, events, names |
| `endfield.gryphline.com/<lang>/operator` | 37 entries with name, rarity (`data-rarity`), class and element (`data-key`) in the HTML. Faction, race, intro and English voice actor of the 26 launch entries are a JSON array in a page script, per language, Simplified Chinese included; later operators have name, intro and voice actor as flat keys there, and their faction and race are not in the scripts | Operator list, profiles, portraits |
| `endfield.hypergryph.com` | Mainland site, Simplified Chinese | Simplified names only |
| `warfarin.wiki/<en, tc or cn>/operators/<slug>` | Server-rendered game data 1.6. The page carries the game's tables as a data stream in a script (`pipeline/wf_decode.py` reads it): profile, attributes per level, talents, potentials, skills with values per level, promotion costs, and a list of 109 terms with the game's explanation. Description templates carry placeholders; the rendered text has the values. Its banner dates are not those of the global service (Scars of the Forge from 2025-12-09) | In-game text and numbers |
| `warfarin.wiki/<lang>/weapons`, `/gear`, `/facilities`, `/tutorials` and their item pages | Same form. Lists: 85 weapon entries (84 weapons: `wpn_sword_0021_ink` is a second model of Grand Vision, same stats; `build_lists.py` drops it), 276 gear pieces in 24 sets, 129 facilities, about 370 in-game tutorials. A facility page has power use and every recipe; a gear page has the set effect; a tutorial page has the in-game tutorial text. Read on 2026-11-21: all 34 operators in three languages, the four lists in three languages, 51 tutorials in two, 45 facilities in English and 18 in Traditional Chinese, one gear piece per set in two | Facility table, recipes, set effects, terms |
| `endfield.wiki.gg/api.php?action=query&prop=revisions&rvprop=content&rvslots=main&titles=A|B|C` | Wikitext of many pages in one request. Operator infoboxes carry `starting`, `headhunting` (standard, chartered, welfare) and `welfare` | How operators are obtained, headhunting rates and guarantees, AIC |
| `github.com/rmxlinux/EndfieldData` at commit `d847759f71d4549aba4727b3b0ac1a1ad0e37742` (read 2026-11-22; tables of 2026-11-05, 1.6) | No licence. 773 client tables, with the game's English, Traditional and Simplified Chinese text. Its English and Traditional Chinese text is the global service's: 85 of 85 weapon names and 315 of 315 facility fields equal the warfarin.wiki records, so the two are one data mine and count as one source. Gacha tables, dates and permanence are not taken from it | Recommended weapons, base skills, Essence stats, recipes, in-game tutorials. Raw tables stay in `cache/third/ed/` |
| `wiki.skport.com/endfield` (official, Gryphline; read 2026-11-22 in headless Chromium) | Plain fetch returns only a JavaScript shell; see Expansion and strategy. Entry URL `/endfield/detail?mainTypeId=1&subTypeId=1&gameEntryId=<catalog item id>`. All rights reserved | Second witness, by sample: 7 operators (Laevatain, Xaihi, Da Pan, Gilberta, Perlica, Akekuri, Alesh) gave 32 fields (recommended weapons, base skill levels with value and promotion), all equal to our records; its two differences were player typos ("Wordly Wisdom", a doubled space) |
| `endfield.wiki.gg/api.php` | MediaWiki API, CC BY-SA 4.0. Version pages carry the version number | Version numbers, cross-check |
| `game8.co/games/Arknights-Endfield/archives/<id>` | Readable after the site navigation | Cross-check |
| `prydwen.gg/arknights-endfield/characters/<slug>` | Guide text readable | Not used yet |
| `wiki.biligame.com/zmd/` | Readable, Simplified Chinese | Not used yet |
| Fandom | 403 | Not readable |

Findings that pages rely on:

- The official notices never state a version number. Titles and numbers were paired from the version infoboxes of endfield.wiki.gg (1.1 to 1.6) and Game8 (1.6).
- 37 official entries against 34 in the game data: Endministrator has two entries, and Kay and Mimino appear in no notice up to 2026-11-21.
- The rate-up 6-star operator of a Chartered Headhunting banner is in the pool for three Chartered banners, its own included, then leaves and is not added to Basic Headhunting (every Chartered notice; confirmed on the pools of Laevatain and Liino).
- Official Traditional Chinese writes the 1.1 title with a comma (新潮起，故淵離); endfield.wiki.gg omits it.
- Official notices list only the 6-star operators of a pool. That an operator is in the standard roster, or is a starting operator, comes from the infoboxes of Endfield Talos Wiki; pages say so.
- Purrchena (5-star, Version 1.5) was given by the event Purry Big Feline! RAWR! and is in no headhunting notice.
- Promotions I to III cost the same for all 34 operators, whatever the rarity; Promotion IV differs in two materials (14 combinations).
- 30 names of skills, talents, potentials and promotion stages differ between the game's Simplified and Traditional Chinese texts beyond the script (for example 精英化I and 精英化·一). `records/names-voc.json` lists them and `scripts/to-zh-cn.py` applies them.
- The names of all 34 operators in the game data match the official operator lists in English, Traditional and Simplified Chinese.
- A skill with two forms (Arcane's Array Arcana: INT and WILL) keeps its text under each form's condition, not in the skill's main description.
- The English and Traditional Chinese texts of one notice can differ: the 1.5 update notes list three wording changes only in English.
