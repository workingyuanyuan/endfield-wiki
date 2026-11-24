"""Flag wording the owner asked to keep out of the visible text (2026-11-21).

Usage: python3 -I pipeline/check_prose.py <page.md> [...]
Pages in English, Traditional Chinese (zh-tw/), Japanese (ja/) and Korean (ko/).
Checks the body only (the frontmatter may name sources). Exit code 1 when a page has a hit.
Each hit is one of:
  SOURCE   the prose names a source; the page notes name it. Allowed only where two sources
           disagree on something a reader acts on, or one player test stands alone (NGA).
  HEDGE    a disclaimer: what is unknown, unannounced, not stated, or true "as of" a date.
  TIMED    time-limited content: events, sales, sign-ins, compensation, pre-downloads.
  SERVER   a second server's date or a region label beside a date; dates are UTC+8 server
           time, stated once on the home page and on systems/servers-and-time.
  SELF     a sentence about the site or the page instead of the game: who runs the site, what
           it covers, how many pages a section has. The header's "unofficial" label and
           llms.txt say it is unofficial; the description says what the page is about.
With no argument (as in `pnpm verify`), checks every page except zh-cn/, which a script writes
from zh-tw/. The game's own text on operator pages and the gear page (block quotes and the
table cells that hold it) is skipped, as on story pages.
A line that must keep a hit carries the marker <!-- keep --> nowhere: rewrite it instead, or
add the page to ALLOW below with the reason.
"""
import os
import pathlib
import re
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from gametext import inline, page_texts  # noqa: E402

PATTERNS = {
    'SOURCE': [r'Talos Wiki', r'Endfield Wiki', r'warfarin', r'wiki\.gg', r'官方公告', r'公告(稱|只|中|寫|列|提到|未)', r'official notices?',
               r'notices? (say|says|name|names|list|lists|use|uses|call|calls)', r'the game data (list|lists|show|shows|give|gives)',
               r'遊戲資料(列|顯示|中|寫)', r'according to', r'根據', r'記載'],
    'HEDGE': [r'截至', r'目前', r'尚未', r'未公布', r'沒有公告', r'未說明', r'未提及', r'不明', r'未知',
              r'\bas of\b', r'up to 20\d\d', r'not (yet )?(announced|stated|confirmed|known)', r'\bunknown\b',
              r'no (official )?notice', r'unverified', r'(?<!版)本頁', r'this page'],
    'TIMED': [r'補償', r'預先下載', r'預下載', r'簽到', r'限時', r'登入活動', r'compensation', r'pre-?download',
              r'limited-time', r'sign-in', r'log-in event', r'過期', r'expire'],
    'SERVER': [r'Americas', r'（Asia', r'\(Asia', r'Asia 伺服器', r'Asia server', r'UTC-5'],
    'SELF': [r'本站', r'this site', r'not run by', r'(並非|不是|非).{0,12}(經營|營運|官方網站)',
             r'(?<![第前後0-9])([2-9]|[1-9][0-9]+|[二三四五六七八九十兩][一二三四五六七八九十]*) ?頁', r'\b(two|three|four|five|six|seven|eight|nine|ten|eleven|twelve|[0-9]+) pages\b'],
}
# Added for Japanese (ja/) and Korean (ko/) pages, which are also checked with PATTERNS.
# 未公開 is not here: it is the game's own value for an undisclosed race.
PATTERNS_JAKO = {
    'SOURCE': [r'によると', r'によれば', r'公式(お知らせ|告知|発表|の発表)', r'お知らせ(では|に(よ|記|書))', r'ゲームデータ(によ|に記|が示)',
               r'に記載', r'에 따르면', r'에 의하면', r'공식 (공지|발표)', r'공지(에서는|에 (따르|의하|적))', r'게임 데이터(에 (따르|의하|적)|가 보여)'],
    'HEDGE': [r'未確認', r'未発表', r'未定', r'現時点', r'時点で', r'現在', r'まだ', r'明らかになっていない', r'分かっていない',
              r'わかっていない', r'記載(が|は)ない', r'言及(が|は)ない', r'このページ', r'本ページ',
              r'확인되지 않', r'확인된 바', r'알 수 없', r'알려지지 않', r'불명', r'미정', r'아직', r'현재', r'시점(에서|으로|까지)',
              r'발표되지 않', r'공개되지 않', r'언급(이|은) 없', r'이 페이지', r'본 페이지'],
    'TIMED': [r'補填', r'お詫び', r'事前ダウンロード', r'ログインボーナス', r'ログイン(イベント|キャンペーン)', r'期間限定', r'有効期限', r'期限切れ',
              r'점검 보상', r'보상 지급', r'사전 다운로드', r'출석', r'기간 한정', r'로그인 이벤트', r'만료'],
    'SERVER': [r'Asia ?サーバー', r'アジアサーバー', r'アメリカ', r'Asia 서버', r'아시아 서버', r'아메리카'],
    'SELF': [r'このサイト', r'当サイト', r'本サイト', r'運営(する|して|では)', r'(?<![0-9])([2-9]|[1-9][0-9]+) ?ページ', r'이 사이트', r'본 사이트', r'운영하지', r'(?<![0-9])([2-9]|[1-9][0-9]+) ?개 페이지'],
}
# Pages that explain a pattern on purpose.
ALLOW = {
    'systems/servers-and-time.md': {'SERVER'},
    'systems/platforms.md': {'SERVER'},
    'index.md': {'SERVER'},
}


ALL_PAGES = False


def body_of(text):
    m = re.match(r'---\n.*?\n---\n', text, flags=re.S)
    return text[m.end():] if m else text


def check(path):
    norm = path.replace(os.sep, '/')
    rel = re.sub(r'^.*?src/content/docs/(zh-tw/|ja/|ko/)?', '', norm)
    allowed = ALLOW.get(rel, set())
    jako = re.search(r'src/content/docs/(ja|ko)/', norm) is not None
    # Story pages show the game's own text (quotes, table rows, chat lines, file titles and
    # unlock conditions); only the sentences around it are ours.
    game_text = re.compile(r'^\s*(>|\||- |\*|### )') if re.match(r'story/(?!index)', rel) else None
    # Operator pages and the gear page show the game's descriptions and the official
    # introduction as given: block quotes, and table cells holding one of those texts.
    quotes = page_texts(rel)
    cells = [inline(t[lang]) for t, form in quotes if form == 'inline' for lang in t]
    hits = []
    for n, line in enumerate(body_of(open(path, encoding='utf8').read()).split('\n'), 1):
        if game_text and game_text.match(line):
            continue
        if quotes and (line.startswith('>') or any(c in line for c in cells)):
            continue
        for kind, pats in PATTERNS.items():
            if kind in allowed:
                continue
            for p in pats + (PATTERNS_JAKO[kind] if jako else []):
                m = re.search(p, line, flags=re.I)
                if m:
                    hits.append(f'{kind:6} {path}:{n}: "{m.group(0)}" in: {line.strip()[:90]}')
                    break
    return hits


if __name__ == '__main__':
    bad = False
    ALL_PAGES = not sys.argv[1:]
    paths = sys.argv[1:] or sorted(str(f) for f in pathlib.Path('src/content/docs').rglob('*.md') if 'zh-cn' not in f.parts)
    for path in paths:
        hits = check(path)
        for h in hits:
            print(h)
        if not hits and sys.argv[1:]:
            print(f'ok     {path}')
        bad = bad or bool(hits)
    sys.exit(1 if bad else 0)
