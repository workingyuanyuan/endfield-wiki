# The pipeline: scripts, records and their order

Read this before running a script in this folder or changing a record. `../AGENTS.md` holds the rules and the commands every change needs; `../SOURCES.md` the sources and how the game's text is derived; each script's header says what it reads and writes.

## Commands

```
python3 -I pipeline/build_pages.py     # operator pages (en, zh-tw, ja, ko) from records/
python3 -I pipeline/build_lists.py     # names, weapons, dijiang, recipes, enemies from records/
python3 -I pipeline/build_story.py     # operator file pages from records/story/
python3 -I pipeline/gametext.py        # the game's descriptions and official introductions -> records/gametext/, gear-sets.json effects
python3 -I pipeline/names_jako.py      # records/names-jako.json: ja/ko names and terms from the text tables and notices
python3 -I pipeline/check_jako_names.py [page.md ...]       # ja/ko pages: every game name in its ja/ko form
python3 -I pipeline/jako_pages.py sheet|check|aliases ...    # hand-written ja/ko pages: writer's sheet, check against the English page, one set of titles
uv run --with opencc-python-reimplemented pipeline/names_voc.py     # names whose Simplified form is not a plain conversion
python3 -I pipeline/build_records.py   # facts part of records/operators/ from the cached game data
python3 -I pipeline/wf_extract.py cache/third/wf/<lang>-<slug>.html [...]   # a cached game-data page to JSON
python3 -I pipeline/wf_misc.py         # terms, tutorials, facilities, weapons, gear sets from the cache
python3 -I pipeline/ed_extract.py      # recommended weapons, base skills, Essence stats, recipes, enemies from cache/third/ed/<commit>/
python3 -I pipeline/notice_text.py cache/official/art/en-us-<cid>.json   # an official notice from the cache as text
```

After a change to a record: `names_jako.py` (when names changed), `build_pages.py`, `build_lists.py`, `to-zh-cn.py`, `check_jako_names.py`, `pnpm build`, `node scripts/prose-review.mjs run`, then `pnpm verify`. After new game data: fetch the pages again into `cache/third/wf/` (the fetch scripts are kept there), then `wf_extract.py`, `build_records.py`, `names_voc.py`, `ed_extract.py` and `gametext.py`.

## Records and folders

- Records: `records/operators/<slug>.json` (names and numbers, rebuilt by `build_records.py`); `records/gametext/` and `records/story/` (the game's text, written by `gametext.py` and `story_extract.py`); `recommend.json`, `base-skills.json`, `weapon-essence.json`, `recipes.json`, `enemies.json` (written by `ed_extract.py`); `banners.json`, `versions.json`, `obtain.json`, `changes.json`, `weapons.json` are kept by hand from the notices and the game data, with ja and ko prose where they carry prose.
- The game's text: `gametext.py` fills each description template with the values of warfarin.wiki's English text and writes every language; operator pages quote the introduction, skills and talents as block quotes and put potentials and base skills in table cells. Checks 12 and 13 of `check-dist.mjs` fail when a line of a record is not on its page unchanged; `check_prose.py`, `check_jako_names.py` and the prose ledger skip this text. No line on a page says the text is the game's. Details: `SOURCES.md`.

| Path | Role |
| --- | --- |
| `pipeline/` | Scripts that read the cached sources, build the records and write the generated pages |
| `records/` | The site's own data, committed; also `names-voc.json` (name pairs for the Simplified pages) and `pages.txt` (every page, for the link check of `lint_page.py`) |
| `cache/` | Copies of sources, not committed: `official/` (notices, operator list), `third/wf/` (warfarin.wiki), `third/wg/` (Endfield Talos Wiki), `third/ed/<commit>/` (game tables) |

## What the page scripts write

- Operator pages follow one structure: portrait, Profile, How to obtain, Recommended weapons, Skills (with each skill's own SP cost, Ultimate Energy cost and combo cooldown, from the record), Skill values (level 1 and 12), Talents, Potentials, Base skills, Base stats, Promotion materials, Changes since release. Portraits are the card images of the official operator list, as WebP in `public/art/operators/<slug>.webp`.
- Operator file pages (`story/<slug>`) have no sidebar section: each follows its operator in the Operators group and shows only on that operator's pages; the index `story/` follows the operator list, and the operator page links its file page in a Profile row named by the game's term.

## Japanese and Korean

- Japanese is written in だ・である, Korean in -다; numbers, dates, times and links are those of the English page. Game names and terms come from the game's own text (`records/names-jako.json`); a term the tables have is never translated by hand. Players' words (天井, 천장) go beside the game's terms in descriptions and headings. Template sentences are whole sentences per language in the page scripts; Korean particles after a variable go through `josa()`.
- A page that Japanese or Korean lacks is listed in `records/pending.json`, named as plain text in that language and never linked; index and home pages list only pages that exist in that language. Remove the id in the commit that adds the page. `src/routeData.ts` marks Starlight's English fallback at such an address `noindex` and keeps it out of sidebars, hreflang, the sitemap and search.
