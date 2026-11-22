# Following the sources of this site

The pages are written from the official notices of the global service (en-us, with the zh-tw, ja-jp and ko-kr editions for names), the official operator list, the game data tables of `github.com/rmxlinux/EndfieldData` and warfarin.wiki (one data mine), Endfield Talos Wiki and a few player guides. A version brings new operators, banners and data every few weeks, and banners and Arsenal Issues change within a version. `pnpm upstream` compares the sources with what the pages were written from.

```
pnpm upstream            # report. Exit 0: no difference. 1: differences. 2: the check could not be made
pnpm upstream --write    # also record the notices and operator entries seen and the fingerprints of the cited notices in upstream/manifest.json
```

It changes no page and needs no token; where `GITHUB_TOKEN` is set (the workflow sets it), it is sent to the GitHub API only, for its higher rate limit. It reads the English pages only: the other languages carry the same facts and sources.

## What is watched, and where the record is

| Watched | Compared with | Kept in |
| --- | --- | --- |
| The official notice list, every page of the bulletin API (`web-news.gryphline.com/api/bulletin?lang=en-us&...`, 20 a page; it holds sticky notices first, so all of it is read). The reading must give as many notices as the list states | The notices already known: those the pages cite and those read at the last `--write`, with their title and date | The pages (links to `endfield.gryphline.com/en-us/news/<cid>`) and `manifest.json` (`notices`) |
| The text of every cited notice dated on or after the earliest notice that the newest version page cites | A SHA-256 from the last `--write` | `manifest.json` (`cited`) |
| The game data tables that `pipeline/ed_extract.py`, `names_jako.py` and `build_lists.py` read (the table names written in those scripts), at the newest commit of EndfieldData | The blob of each table at the commit the pages cite (their links to `github.com/rmxlinux/EndfieldData/tree/<commit>`, one commit for all pages). `COMMIT` in `ed_extract.py` and `names_jako.py` must be that commit | The pages |
| "Current Version" on the warfarin.wiki home page | "game data X.Y" in the pages' `appliesTo` | The pages |
| The entries of the official operator list (`endfield.gryphline.com/en-us/operator`): key, name, rarity, class and element | The entries read at the last `--write`; an entry has a page here when its name is the title of an operator page | `manifest.json` (`operators`) |

Not watched: Endfield Talos Wiki, Game8 and NGA. Endfield Talos Wiki gave the version numbers, which do not change once paired with a title, and its pages are edited every day; a new version's number is looked up there anyway. warfarin.wiki is read only for its version line: one request, nothing kept, as its `robots.txt` (`use=reference`) allows. It answers 403 to GitHub's hosted runners (tested 2026-11-22), so the weekly run skips it (`UPSTREAM_SKIP_WARFARIN`) and says so in a note; run `pnpm upstream` on a computer to compare its version. The EndfieldData tables, the same data mine, are read by both. The older cited notices are checked through the list (still there, same title and date), not through their text: banners that have closed are rarely corrected, and reading all of them each week would mean some 60 more requests.

## The report

One line for each difference, then the notes, then a count. A line reads `kind: id: detail`, where the id is a notice id (cid), a table or an operator key.

| Line | Meaning | What to do |
| --- | --- | --- |
| `new update notes` | A notice titled "Update Notes": a new version, or a content update within one | A new version: follow "A new version" below. A content update: update what it changes |
| `new headhunting notice` | A notice with "Headhunting" or "Release Celebration" in its title: a new Chartered, Special or RE-Factor banner | Follow "A new banner" below |
| `new arsenal notice` | A notice titled "[… Issue] LTO Details", "Limited-Time Offer Details" or "RE-Factor Issue": a new Arsenal Issue | Follow "A new banner" below |
| `new notice to classify` | A notice in the "notices" tab that matches no known kind (a new kind of banner title, a policy, a rule change) | Read it. If a page rests on it, update the page; if it is a new kind of banner, add its title to `KINDS` in `scripts/upstream.mjs`; if it is a kind that is never needed, add a word to `NOTE_TITLE` |
| `cited notice changed` | A cited notice has another title or date in the list, or (current version) another text than at the last `--write` | Read the notice, update the pages it names in every language |
| `cited notice gone` | A cited notice answers "公告不存在" (code 1500) or 404 | Find where it went and update the pages that cite it in every language |
| `cited notice left the list` | A cited notice is missing from the list but still answers | Read it: it may have been withdrawn. Update the pages if so |
| `not in the manifest` | A cited notice of the current version has no fingerprint yet | Check that the pages it names agree with it, then `--write` |
| `game data changed` | A table that the pipeline reads differs at the newest EndfieldData commit from the commit the pages cite | Look at the compare link. Data for content that is not released yet (the repository carries the next version before its release, as the official wiki shows previews) stays out: wait for the update notes. Otherwise move `COMMIT` in `ed_extract.py` and `names_jako.py` and every page's EndfieldData link to the new commit, fetch its tables into `cache/third/ed/<commit>/`, run the commands after a change to a record (`AGENTS.md`), and read the diff of the generated pages |
| `game data version` | warfarin.wiki shows another version than the pages' "game data X.Y" | New game data: after the release, follow the steps after new game data under Commands in `AGENTS.md` (fetch the pages again, `wf_extract.py`, `build_records.py`, restate what changed) |
| `operator entry changed` / `operator entry gone` | An entry of the official operator list that has an operator page here changed its name, rarity, class or element, or left the list | Update the operator page's record and the lists that name it |
| `note: operator entry changed` / `note: operator entry gone` | The same for an entry without a page here (a second Endministrator entry, a preview) | Nothing is due; `--write` records it |
| `note: new notice` | A new notice in the "news" or "events" tab, or one whose title marks a preview, event, account action or store news (DEV Comm, guide page, pre-download, maintenance preview, …) | Nothing is due; the version that a DEV Comm announces arrives with its update notes. `--write` records it as known |
| `note: new operator entry` | A new entry in the official operator list: usually an operator of the next version, listed before release (Kay and Mimino were) | Nothing is due before the release; the new version adds its page |
| `note: game text changed` | An `I18nTextTable_*` changed or is gone: the game's text tables change with every data update | At the next update of the game data, run `names_jako.py` and `check_jako_names.py` |
| `note: not read: warfarin.wiki` | The run skipped warfarin.wiki (the weekly run always does) | Run `pnpm upstream` on a computer when a new version is out |
| `note: game data commit` | EndfieldData has a newer commit in which tables the pipeline does not read changed (with or without `game data changed` lines) | Nothing for those tables |

`check not made` with exit 2 is not a report: fix the cause it names and run again. It prints the lines it found first. "the notice list gave N notices, not the M it states" means the list changed during two readings or its form changed; "entries read" means the operator list's markup changed; "COMMIT … is not the commit the pages cite" means a script was moved to a new commit and the pages were not rebuilt from it, or the reverse: rebuild the pages, or set the scripts back. "the pages cite N EndfieldData commits" means some pages were rebuilt and others not.

## A new version

1. Read the update notes in English, then the zh-tw, ja-jp and ko-kr editions of the same cid, as the content rules in `AGENTS.md` say for names. Pair the title with its version number on Endfield Talos Wiki.
2. Once the version is out: new game data (`game data version`, `game data changed`) as above, new operators' records and pages, the version page in every language, `records/versions.json`, the banners and Arsenal Issues (below), the home page, the version index and `LLMS_NOTES` in `src/lib/site.mjs`.
3. Run the commands after a change to a record (`AGENTS.md`), then `scripts/to-zh-cn.py`.

## A new banner

A headhunting banner: add it to `records/banners.json` (dates in UTC+8, the 6-star operators of the pool), then `build_pages.py` (operator pages: how to obtain), and add it to the version page and to `systems/headhunting` where it lists banners, in every language. An Arsenal Issue: add it to the version page and to `systems/arsenal`, in every language.

## After updating

1. Set `lastVerified` of each page that was read again, and `effectiveDate` to the date of the newest notice used.
2. `pnpm upstream --write`, then `pnpm upstream` until no line is left (`--write` leaves with 0 whatever differences it reports, and with 2 without writing when the check could not be made), then `pnpm verify`.
3. The owner confirms the content before the push.

`--write` records every notice and operator entry read as known and every cited notice of the current version as it is now. Run it after the pages agree with them, not before: a new update notes notice that is recorded as seen is no longer reported. It cannot hide a game data change or version: those are read from the pages and the pipeline scripts.

`lastVerified` moves only for a page that was read against its sources again. A run without a difference moves nothing.

## Schedule

`.github/workflows/upstream.yml` runs the command once a week (owner, 2026-11-22) and by hand (`gh workflow run upstream.yml`). A difference on the default branch opens one issue with the label `upstream`, assigned to the owner; later runs replace its text, comment when the kind and id of a line other than a note are added or removed (a new detail on the same kind and id does not comment), and close it when there is no difference. A run that could not make the check fails the workflow and leaves the issue as it is.

GitHub stops scheduled workflows in a public repository after 60 days without activity in it; `gh workflow enable upstream.yml` starts them again.
