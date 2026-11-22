# Agent test after the expansion (2026-11-22)

The five questions that were partial on 2026-11-21 (q11, q13, q18, q22, q27) were asked again after their qualifiers were moved next to the answers, together with five new questions on the new content (q28 to q32: recommended weapons, the weapons reverse lookup, Dijiang base skills, recipes by product, Dijiang mood).

Reader: one Claude Sonnet subagent, one run, local serving at http://127.0.0.1:4398/endfield-wiki/, 3 fetches per question. q13 was asked once more, to a fresh Claude Sonnet subagent, after its qualifier moved again. Fetches counted from `site-fetch.log` and `site-fetch-q13.log`: 16 for the ten questions, 2 for the q13 rerun; no question over the budget.

| Result | Count | Questions |
| --- | --- | --- |
| Pass | 10 | q11, q13 (rerun), q18, q22, q27, q28–q32 |
| Partial | 0 | |
| Fail | 0 | |

- q13 was partial in the first run: the qualifier (Camille stays in the Chartered pool for two more banners) sat under the pool table. It moved to directly under the banner dates on `versions/1-3`, and the rerun gave it.
- q22 passed with an unchanged page: the qualifier was already in the first paragraph and the caveat.
- q28 was answered from the weapons list (reverse lookup) instead of Laevatain's page; the answer and its order match the operator page.

Limits: one reader model, one run per question, local serving, questions written by the author of the site from the game tables. The original sources were not run.
