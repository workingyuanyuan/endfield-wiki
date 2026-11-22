# Agent test

Checks whether an agent with only a fetch tool answers questions about the game better from this site than from the official site and guide sites.

## Files

| File | Role |
| --- | --- |
| `questions.json` | The questions with the expected answer, the qualifier that is easy to miss, and the page that holds them. Written by the author of the site from the official notices and the game data |
| `fetch.mjs` | The fetch tool given to the agent. Modelled on the MCP reference Fetch server: main-article extraction, Markdown output, 5,000 characters per call, `start_index` to continue. Every call is logged to `runs/<run>.log` |
| `results/<date>/` | Answers and fetch logs of each recorded run |

## How to run

1. Build the site with a local address and serve it:

```
SITE_URL=http://127.0.0.1:4398/endfield-wiki pnpm build
pnpm preview
```

2. Give a fresh agent the questions (without the expected answers), the fetch command below as its only source, a start URL, and a budget of 3 fetches per question.

```
node tests/agent-eval/fetch.mjs --run <run-name> --q <question-id> <url> [start_index]
```

Start URL for this site: `http://127.0.0.1:4398/endfield-wiki/`. Start URLs for the baseline: `https://endfield.gryphline.com/en-us/news`, `https://warfarin.wiki/en` and `https://endfield.wiki.gg/`.

3. Score each answer against `questions.json`: pass needs the answer and the qualifier; partial is one of the two or an unverified inference; fail is a wrong or missing answer.

4. Run `pnpm verify` afterwards so that `dist/` carries the public address again.

## Search test

Checks whether an agent that starts from a question, with no URL, finds this site. It runs on the live site once its pages are indexed. It is a record, not a gate for publishing.

1. Give a fresh agent the questions from `questions.json` (without the expected answers, and without this site's name or address), a web search tool, and the fetch command above as its only way to read a page. No start URL.
2. Record the search tool, the queries the agent made and its answers. The fetch log holds the URLs it read.
3. Score each question: pass needs a page of this site among the pages read, and the answer with its qualifier. Record "not found" when no page of this site was read.
4. For each miss, find the cause: the page is not indexed (sitemap, links, `robots.txt`); it is indexed but not chosen (the question's words are not in its title or headings, it has nothing the source lacks, nothing links to the site); or it was read and the qualifier was lost.

## Results

### 2026-11-21, after the rewrite

27 questions (q01, q03, q07, q11, q12 replaced by questions that do not depend on the day; q25 to q27 from NGA player questions). This site: 22 pass, 5 partial, 0 fail, 38 fetches from the log. Each partial answer gave the main fact and missed a second qualifier lower on the same page. One Claude Sonnet reader, one run, local serving; the original sources were not run again. Details in `results/2026-11-21-rewrite/scores.md`.

### 2026-11-21

24 questions. Answers, fetch logs and the score of every question are in `results/2026-11-21/`.

| Run | Pass | Partial | Fail | Fetches (from the log) |
| --- | --- | --- | --- | --- |
| This site, start URL `http://127.0.0.1:4398/endfield-wiki/` | 23 | 1 | 0 | 23 |
| Original sources (official news, warfarin.wiki, endfield.wiki.gg) | 6 | 12 | 6 | 47; one question went over the budget |

Limits of this result:

- One reader model (Claude Sonnet, as a subagent) and one run per side.
- The questions, the expected answers and the scores were written by the author of the site.
- The site was served locally.
- The reader of the original sources had only the test's fetch tool, which cannot run page scripts: the official news page and warfarin.wiki gave it almost nothing.
