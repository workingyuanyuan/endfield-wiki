# Rules for agents maintaining this site

An unofficial wiki for the game Arknights: Endfield (明日方舟：終末地; Hypergryph, published outside mainland China by Gryphline), at `https://yuanaruru.com/endfield-wiki/` from the public repository `workingyuanyuan/endfield-wiki`; the deploy workflow runs `pnpm verify`. The rules in `../AGENTS.md` apply; this file holds what is specific to this site.

Read before the work: `SOURCES.md` before fetching a source, reading game data or writing from one (what each allows, how to read it, the findings pages rely on); `pipeline/README.md` before running a pipeline script, changing a record or writing a Japanese or Korean page (commands, their order, what each record file is); `upstream/README.md` when `pnpm upstream` reports a difference or a version lands; `../COMMUNITY.md` when a version lands. Who wrote and checked what goes in `reviews/work-log.md`; questions and test results in `tests/agent-eval/`.

## Decisions

By the owner unless marked.

- Languages (2026-11-21, 2026-11-22): English at the root, Traditional Chinese (`/zh-tw/`), Simplified Chinese (`/zh-cn/`, written by script from `zh-tw`), Japanese (`/ja/`) and Korean (`/ko/`). No human review of the Japanese and Korean text: the checks are scripts and a reader of another model family than the writer. For their hand-written pages, first look for third-party Japanese or Korean sources and write from them; where they add no fact, translate from the English page.
- Service: the global service (Asia and Americas / Europe servers). Mainland China is not covered.
- Scope: versions, one page per operator with its file page, a names page, systems and AIC pages. No page per weapon, gear piece, facility, item or enemy; those are lookup tables.
- How pages are produced: records from which a script writes the Markdown for operators, operator files, index pages, the names page and lookup tables; hand-written Markdown for version pages and system pages.
- The home page links index pages (`versions/`, `operators/`, `systems/`, `aic/`); each links every page of its section within its first 5,000 extracted characters.
- Numbers (2026-11-21): the game data that warfarin.wiki publishes is accepted for in-game numbers (recipes, stats, skill multipliers, the numbers inside the game's descriptions). Read only the pages needed, do not crawl, and check samples against the official notices and endfield.wiki.gg.
- The game's own text (2026-11-23, 2026-11-24) is shown as the game gives it, in each language's edition from the game's text tables, never restated: operator files, voice lines and chats, the skill, talent, potential and base-skill descriptions and gear set effects, and the operator introductions, which come from the official site's operator list in its five editions. Facts in our own sentences and tables (dates, banners, changes from the update notes, numbers, names) stay ours. Remove a text when the publisher asks.
- Official art is used, with notice 4497 in view (Fan Content and Streaming Guidelines, which prohibit "content that directly copies or uses excerpts of the Company's official materials and lacks clear originality"). Remove an image when the publisher asks.
- Time-limited content stays out (2026-11-21): events, limited shops and sales, sign-ins, compensation, pre-downloads, protocol passes, collaborations, the next version, the end of the current one. Headhunting banners and Arsenal Issues stay as a dated history on version and operator pages. Operator pages say nothing that depends on the day they are built.
- One clock (2026-11-21): dates and times are Asia server time (UTC+8), without a label beside each. The home page caveat, `systems/servers-and-time` and `llms.txt` state once how the Americas / Europe server (UTC-5) relates.
- A sentence names a source only where two sources disagree on something a reader acts on, or where one player test is the only source; then once per section. Player research from the NGA board `fid=846` may serve as a source.
- The publisher's own wiki, `wiki.skport.com/endfield` (2026-11-22): no links from operator pages to its entries, no line in `llms.txt` about it needing JavaScript, and our records are not published as JSON.
- Strategy (agent, 2026-11-22): the publisher's wiki is a second witness for fields the game generates (recommendations, base skills), read in a browser at a human pace, never through its API. Do not race it on depth per entry. What lasts is answers that span entries (weapon to operator and back, operator to room, facility to product), the qualifier beside the fact, version history, player-tested mechanics and Simplified Chinese.
- Look (2026-11-21): taken from the official site: white ground, grey panels, near-black ink, signal yellow `#fffa00`, square corners, small spaced labels, a double slash before section names, a yellow block before the site name.
- Motion (2026-11-22, approved from demo videos): modelled on the official site and the login screen: 0.2–0.3 s pointer responses, a flicker-in for the title and section headings, a yellow line drawn once under the header and along each section rule, a wipe for the answer and tables, a cross-document view transition that keeps header and sidebar still. Each plays once, nothing loops; a block waits unseen for its entrance only while the script runs (motion section of `src/styles/endfield.css`, script in `SiteTitle.astro`). Favicon: a yellow inverted triangle with a cut on near-black.
- Home page key visual: the launch key visual of the official site (`kv-obt-pc`, the whole cast, no lettering). The picture at the top of the official site changes with each version and is not used.
- The owner confirms every change before it goes live. `pnpm upstream` runs every day in a workflow that keeps one issue (2026-11-25).

## Commands

```
pnpm verify      # prose check, build, acceptance checks. Run it before you call a change done.
pnpm upstream    # compare the sources with what the pages were written from (upstream/README.md)
pnpm build; pnpm check     # build; acceptance checks on an existing dist/
pnpm preview     # serve dist/ at http://127.0.0.1:4398/endfield-wiki/ with GitHub Pages style headers
node scripts/prose-review.mjs run      # after a build: read the prose not yet read (`status` instead of `run`: count it)
python3 -I pipeline/lint_page.py <page.md> [...]     # check one page without a build
python3 -I pipeline/check_prose.py [page.md ...]     # citation phrases, disclaimers, time-limited content, a second server's dates, sentences about the site
uv run --with opencc-python-reimplemented scripts/to-zh-cn.py       # write the zh-cn pages from the zh-tw pages
```

After a change to a record or new game data, run the scripts in the order `pipeline/README.md` gives, then `pnpm verify`.

## Content rules

- Pages live in `src/content/docs/` and its language folders. Addresses use the official English name in lower case with hyphens: `operators/laevatain`, `versions/1-6`. A section's index page is `<section>/index.md`.
- Written by script, never by hand: operator pages, `story/`, `systems/names`, `systems/weapons`, `systems/dijiang`, `systems/enemies`, `aic/recipes`, and every `zh-cn` page. Change the record or the script.
- Run `scripts/to-zh-cn.py` after every change to a `zh-tw` page. When a `zh-tw` page brings in a new name, compare it with the mainland site and add a pair to `VOC` when the two differ beyond the script. A table whose header names both 繁體中文 and 簡體中文 keeps its rows as written; a sentence that quotes a Traditional name needs an entry in `FIXES`.
- Every page has `aliases`: title and aliases together are the same set of strings in every language in which the page exists, and the Simplified title is among the aliases of the `zh-tw` page. After a change of a title or an alias run `jako_pages.py aliases <page id>` and `to-zh-cn.py`.
- Links and images are root-relative and without the site's sub-path: `/operators/laevatain/`, `/art/operators/laevatain.webp`. Links in `zh-tw`, `ja` and `ko` pages start with `/zh-tw/`, `/ja/`, `/ko/`; image paths do not.
- Japanese and Korean pages: read `pipeline/README.md` (Japanese and Korean) before writing or translating one: register, where names come from, and `records/pending.json` for a page a language lacks, which is named as plain text and never linked.
- Description limits: English 110, Chinese 70, Japanese 70, Korean 90 characters (`maxDescription` in `LOCALES`).
- Quote a frontmatter value that contains a colon followed by a space (`"Arknights: Endfield ..."`).
- Times: "server time" in a notice is UTC+8 on the Asia server and UTC-5 on the Americas / Europe server; a maintenance window is the same six hours on both. A banner that closes "before version update and maintenance" ends at "End of Version x"; do not infer a date.
- Version numbers are not in official notices; they come from Endfield Talos Wiki. Pages give the number with the title.
- Names: English from the en-us notices, Traditional Chinese from the zh-tw notices, Simplified Chinese from the mainland site or the game's Simplified text, Japanese and Korean from the game's text tables and the ja-jp and ko-kr notices. Chinese pages use the game's own Chinese names for skills, states and terms.
- No tier lists, team builds or damage rankings on fact pages; players' ratings belong to the community section (`../COMMUNITY.md`). Next-version content (entries the official wiki marks as previews) stays out.
- Do not write `//` in page text: the skin draws it before section names and the check script treats it as a leak.
- The game's text is written into the pages by `gametext.py` (`pipeline/README.md`); `check_prose.py`, `check_jako_names.py` and the prose ledger skip it, and checks 12 and 13 of `check-dist.mjs` fail when a line of a record is not on its page unchanged. No line on a page says the text is the game's.
- Operator pages and operator file pages are written whole by `build_pages.py` and `build_story.py`; their structure, the portraits and where file pages show in the sidebar are in `pipeline/README.md`. Change the script, not a page.
- Run `check_prose.py` and `lint_page.py` on every hand-written page; `lint_page.py` compares every date with the cited notices. Screenshots go in `../preview/endfield-wiki/`.

## Skin rules

- The skin is `src/styles/endfield.css`. Heading font: Lexend (SIL OFL 1.1); Chinese, Japanese and Korean use system fonts per language, so kanji never take Chinese glyph forms; Japanese breaks lines with `line-break: strict`, Korean by word.
- In the light theme yellow is a ground colour only (highlight under links, selected row, marks); text accents are ink. In the dark theme yellow carries links.
- Text drawn with CSS `content`: the double slash before `h2` (pattern in check 5 of `scripts/check-dist.mjs`).
- Overrides: `SiteTitle`, `MarkdownContent`, `ThemeSelect`. The header links the four sections in the sidebar's order (versions, operators, systems, AIC); the sidebar keeps the operators group collapsed. Check 11 of `check-dist.mjs` covers the header and the page notes.
