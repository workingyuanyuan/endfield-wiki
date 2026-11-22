"""Flag wording the owner asked to keep out of the visible text (2026-11-21).

Usage: python3 -I pipeline/check_prose.py <page.md> [...]
Checks the body only (the frontmatter may name sources). Exit code 1 when a page has a hit.
Each hit is one of:
  SOURCE   the prose names a source; the page notes name it. Allowed only where two sources
           disagree on something a reader acts on, or one player test stands alone (NGA).
  HEDGE    a disclaimer: what is unknown, unannounced, not stated, or true "as of" a date.
  TIMED    time-limited content: events, sales, sign-ins, compensation, pre-downloads.
  SERVER   a second server's date or a region label beside a date; dates are UTC+8 server
           time, stated once on the home page and on systems/servers-and-time.
A line that must keep a hit carries the marker <!-- keep --> nowhere: rewrite it instead, or
add the page to ALLOW below with the reason.
"""
import os
import re
import sys

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
}
# Pages that explain a pattern on purpose.
ALLOW = {
    'systems/servers-and-time.md': {'SERVER'},
    'systems/platforms.md': {'SERVER'},
    'index.md': {'SERVER'},
}


def body_of(text):
    m = re.match(r'---\n.*?\n---\n', text, flags=re.S)
    return text[m.end():] if m else text


def check(path):
    rel = re.sub(r'^.*?src/content/docs/(zh-tw/)?', '', path.replace(os.sep, '/'))
    allowed = ALLOW.get(rel, set())
    hits = []
    for n, line in enumerate(body_of(open(path, encoding='utf8').read()).split('\n'), 1):
        for kind, pats in PATTERNS.items():
            if kind in allowed:
                continue
            for p in pats:
                m = re.search(p, line, flags=re.I)
                if m:
                    hits.append(f'{kind:6} {path}:{n}: "{m.group(0)}" in: {line.strip()[:90]}')
                    break
    return hits


if __name__ == '__main__':
    bad = False
    for path in sys.argv[1:]:
        hits = check(path)
        for h in hits:
            print(h)
        if not hits:
            print(f'ok     {path}')
        bad = bad or bool(hits)
    sys.exit(1 if bad else 0)
