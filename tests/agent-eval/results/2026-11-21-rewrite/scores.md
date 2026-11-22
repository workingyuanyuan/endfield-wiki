# Agent test after the rewrite (2026-11-21)

The site was rewritten after the owner's feedback: short titles, no citation phrases or disclaimers, no time-limited content, one clock. Five questions that depended on "today" were replaced by timeless ones (q01, q03, q07, q11, q12) and three NGA player questions were added (q25 to q27). Expected answers of q05, q09, q10 and q13 were restated without the second server's dates and without naming sources, as the pages now are; the facts did not change.

Reader: one Claude Sonnet subagent, one run, local serving at http://127.0.0.1:4398/endfield-wiki/, 3 fetches per question. Fetches counted from `site-fetch.log`: 38 (no question over the budget; one 404 from a guessed address under q16).

| Result | Count | Questions |
| --- | --- | --- |
| Pass | 22 | q01–q10, q12, q14–q17, q19–q21, q23–q26 |
| Partial | 5 | q11 (no RE-Factor guarantee rule), q13 (no stay in the pool after the banner), q18 (several Issues open at once not said), q22 (Promotion IV differs not said), q27 (Stagger ×1.3 not said) |
| Fail | 0 | |

Causes: each partial answer gave the main fact and left out a second qualifier that sits lower on the same page; no page was missed. The original sources were not run again.
