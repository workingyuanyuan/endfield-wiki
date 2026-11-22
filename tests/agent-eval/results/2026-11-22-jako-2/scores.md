# Agent test, Japanese and Korean, phase 2 (2026-11-22)

Ten questions per language on the hand-written pages added in phase 2: the Japanese and Korean forms of q02, q13, q15, q16, q17, q18, q21, q22, q24 and q26 (versions, headhunting, servers and time, platforms, Arsenal, AIC power, operator progression, combat). Questions in `questions-only.txt`, written by the author of the site with the game's Japanese and Korean terms and the players' words (天井, 引き継ぎ; 천장, 이월); expected answers and qualifiers are those of `questions.json`.

Reader: one Claude Sonnet subagent per language, one run, local serving, start URLs `http://127.0.0.1:4398/endfield-wiki/ja/` and `/ko/`, 3 fetches per question. Fetches counted from the logs (`site-fetch-ja.log`, `site-fetch-ko.log`).

| Language | Pass | Partial | Fail | Fetches |
| --- | --- | --- | --- | --- |
| Japanese | 10 (q17 after a rerun) | 0 | 0 | 10, and 1 for the q17 rerun |
| Korean | 8 | 2 | 0 | 10 |

- ja-q17 was partial in the first run: the reader answered from the home page, which said save data is shared across platforms without "on the same server". The home page now says so in every language; a fresh reader gave the full answer (`site-fetch-ja-q17.log`).
- ko-q13: partial. The reader gave the banner and its dates but not that Camille stayed in the Chartered pool for the next two banners, which the page states under the banner table, within the first 5,000 characters. A reading miss.
- ko-q26: partial. The reader gave "cannot be disassembled" and the limit of 2,000, but not where Essences claimed at the limit go (the lost-and-found cache) nor that the other kinds disassemble for Stock Bills.
- ja-q15, ko-q15: the expected qualifier names Endfield Talos Wiki as the only source of the 80-pull carry-over; by the owner's rule the pages do not name sources in the prose, so this part is not scored. Both readers gave which counts carry over and which do not.

Limits: one reader model, one run per language, local serving, questions written by the author of the site, not by Japanese or Korean players; the original sources were not run.
