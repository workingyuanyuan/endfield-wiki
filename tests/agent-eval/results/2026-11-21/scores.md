# Agent test, 2026-11-21

Scored by the author of the site against `questions.json` (24 questions). Pass needs the answer and the main point of the qualifier; partial is one of the two, or an inference the reader marked as such; fail is a wrong or missing answer. Fetches are counted from the logs in this folder.

| Question | Page | This site | Original sources |
| --- | --- | --- | --- |
| q01 | operators/laevatain | pass | partial: inferred "probably not", found no statement |
| q02 | versions/1-6 | pass | pass |
| q03 | versions/1-6 | pass | partial: gave an end time from the fan wiki that no official notice states |
| q04 | operators | pass | fail: not found |
| q05 | versions | partial: answer right; the reader used the operator page, which did not say that the number is unofficial or give the Americas / Europe date | fail: not found |
| q06 | operators/laevatain | pass | fail: found potentials, not talents |
| q07 | versions/1-6 | pass | fail: 2026-12-03, the fan wiki's date; the update notes say 2026-12-02 |
| q08 | operators | pass | pass |
| q09 | operators/ember | pass | partial: answer only |
| q10 | operators/purrchena | pass | pass |
| q11 | systems/banner-history | pass | partial: found Tangtang, not Yvonne |
| q12 | operators/typhoeus | pass | partial: did not find that it is her last banner |
| q13 | versions/1-3 | pass | fail: not found |
| q14 | systems/names | pass | pass |
| q15 | systems/headhunting | pass | pass |
| q16 | systems/servers-and-time | pass | fail: not found |
| q17 | systems/platforms | pass | partial: from a headline date only |
| q18 | systems/arsenal | pass | partial: did not find how long an Issue stays |
| q19 | versions/1-0 | pass | pass |
| q20 | aic/power | pass | partial: right recipes, 4 fetches (over the budget), no word on the missing HC battery |
| q21 | aic/power | pass | partial: marked as an inference |
| q22 | systems/operator-progression | pass | partial: answer only |
| q23 | systems/gear | pass | partial: answer only |
| q24 | systems/combat | pass | partial: answer only |

| Run | Pass | Partial | Fail | Fetches (from the log) |
| --- | --- | --- | --- | --- |
| This site, start URL `http://127.0.0.1:4398/endfield-wiki/` | 23 | 1 | 0 | 23 (at most 3 for one question) |
| Original sources, start URLs `endfield.gryphline.com/en-us/news`, `warfarin.wiki/en`, `endfield.wiki.gg` | 6 | 12 | 6 | 47 (one question over the budget of 3) |

What the reader of the original sources ran into: the official news page and the warfarin.wiki pages gave the fetch tool a headline list or an empty shell; 43 of its 47 fetches went to endfield.wiki.gg, whose version and banner lists reached it without operator names; operator pages there were cut at 5,000 characters before the talents.

After the run, two things were changed on the site. Operator pages of rate-up operators now name the version by title and say that the number is unofficial, with both servers' dates (the cause of the partial on q05). The 1.6 page now names the currency Vitrified Indigo, which q07 asked about and the page did not use.

Limits:

- One reader model (Claude Sonnet, as a subagent) and one run per side.
- The questions, the expected answers and the scores are the site author's. The qualifiers are the ones the site was written to carry, which favours the site.
- The site was served locally, built with `SITE_URL=http://127.0.0.1:4398/endfield-wiki`, before the fixes from the last independent review were applied.
- The reader of the original sources could not open pages that need a script to render; a reader with a browser would do better there.
