# Endfield Wiki

Live site: https://yuanaruru.com/endfield-wiki/ (繁體中文 https://yuanaruru.com/endfield-wiki/zh-tw/, 简体中文 https://yuanaruru.com/endfield-wiki/zh-cn/)

An unofficial reference for the game Arknights: Endfield (明日方舟：終末地), global service. It is written first for AI agents that read with a fetch tool, and for people second: every page has a Markdown twin, the answer and its qualifier come first, and each fact is tied to a dated source.

This site is not run by Hypergryph or Gryphline.

## What is in it

| Section | Pages |
| --- | --- |
| Versions | One page per version, 1.0 to 1.6: update date, new content, banners, system changes |
| Operators | One page per operator (34): profile, how to obtain, skills, talents, potentials, stats, promotion materials |
| Systems | Headhunting rates and pity, Arsenal and Essences, servers and time, platforms, combat mechanics and the damage formula, operator progression, weapons, gear sets, names in three scripts |
| AIC | Automated Industry Complex: power, production and logistics, regional development |

Languages: English at the root, Traditional Chinese under `/zh-tw/`, Simplified Chinese under `/zh-cn/` (written by script from the Traditional Chinese pages).

## Sources

Official notices of the global service are the primary source for dates, banners, events and names. Skill, talent, potential, base-skill and gear set texts are the game's own text from its text tables (game data 1.6, rmxlinux/EndfieldData), in each language's edition; numbers are the game data of Version 1.6 as published by warfarin.wiki. Operator introductions are the official site's own text. Endfield Talos Wiki (endfield.wiki.gg, CC BY-SA 4.0) is used for version numbers and for headhunting rules that no notice states; the damage formula comes from player tests on the NGA forum. Operator portraits are the card images of the official operator list; credits are in each page's notes.

## How pages are made

- Version, system and AIC pages are hand-written Markdown in `src/content/docs/`.
- Operator pages and the lookup pages (names, weapons) are written by scripts from `records/`. Change the record, not the page.

```
python3 -I pipeline/build_pages.py     # operator pages from records/
python3 -I pipeline/build_lists.py     # names, weapons
uv run --with opencc-python-reimplemented scripts/to-zh-cn.py   # Simplified Chinese pages
pnpm verify                            # build, then the acceptance checks
pnpm preview                           # serve dist/ at http://127.0.0.1:4398/endfield-wiki/
```

`AGENTS.md` holds the rules for maintaining the site: the owner's decisions, content rules, sources and what each allows.
