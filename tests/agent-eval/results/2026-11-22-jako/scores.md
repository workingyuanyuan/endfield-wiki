# Agent test, Japanese and Korean, phase 1 (2026-11-22)

Ten questions per language, the Japanese and Korean forms of q01, q06, q09, q10, q12, q28, q29, q30, q31 and q33: every page they need exists in both languages in phase 1 (operator pages, weapons, Dijiang, recipes, enemies). The questions were written by the author of the site with the game's own Japanese and Korean names; expected answers and qualifiers are those of `questions.json`.

Reader: one Claude Sonnet subagent per language, one run, local serving, start URLs `http://127.0.0.1:4398/endfield-wiki/ja/` and `/ko/`, 3 fetches per question. Fetches counted from the logs.

| Language | Pass | Partial | Fail | Fetches |
| --- | --- | --- | --- | --- |
| Japanese | 10 (q33 after a rerun) | 0 | 0 | 16, and 3 for the q33 rerun |
| Korean | 10 | 0 | 0 | 20, two of them 404s for guessed addresses |

- ja-q33 was partial in the first run: the reader read only the table of highest resistances, which listed the Electric 35 of the YSTF Captain Blightshade but not its Physical 20; the full row was beyond the first 5,000 characters. That table now gives all five resistances of each enemy in it, in every language, and a fresh reader gave the full answer.
- ko-q01: the reader called Fest of Brilliance a Version 1.3 banner (it ended with the 1.3 update; the page gives its dates). Answer and qualifier were given.
- ko-q30: the question said 균류 소재, the page uses the game's word 버섯 재료; the reader found it.
- ko-q10, ko-q12: the reader guessed Korean addresses (404), then took the right ones from `/ko/llms.txt`.

Limits: one reader model, one run per language, local serving, questions written by the author of the site, not by Japanese or Korean players; the original sources were not run.
