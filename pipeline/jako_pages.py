"""Japanese and Korean versions of the hand-written pages.

Usage:
  python3 -I pipeline/jako_pages.py sheet <out dir> <page id> [...]   # what a writer needs for one page
  python3 -I pipeline/jako_pages.py check <ja or ko page.md> [...]      # compare a page with its English page
  python3 -I pipeline/jako_pages.py aliases <page id> [...]             # one set of titles in en, zh-tw, ja, ko

A page id is the path under src/content/docs/ without .md (versions/index, systems/combat).

sheet writes <out>/<id with / as __>.json: the English and Traditional Chinese page paths, the game's
Japanese and Korean forms of every name and term the English page uses, and the Japanese and Korean
text of every official notice the page cites (the same notice ids), for names and phrasing.

check fails (exit 1) when the page differs from the English page in: frontmatter fields that must be
equal (lastVerified, effectiveDate, source URLs), number and levels of headings, the shape of each
table (rows and columns), link targets (with the language prefix), images, code blocks, the
description limit, or a number of the English body that the page lacks (numbers inside glossary
names are not compared). A number the page has beyond the English is a NOTE, as is a glossary name of
the English page whose game form is not on the page.

aliases rewrites the aliases of the page in en, zh-tw, ja and ko so that title plus aliases name the
same set in all four (run scripts/to-zh-cn.py afterwards).
"""
import collections
import json
import os
import re
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import jako_text  # noqa: E402
from lint_page import frontmatter  # noqa: E402

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DOCS = os.path.join(ROOT, 'src', 'content', 'docs')
ART = os.path.join(ROOT, 'cache', 'official', 'art')
LIMIT = {'ja': 70, 'ko': 90}
# English words that are also record names but mostly mean something else in page prose.
COMMON = {'Area', 'From', 'Side', 'Flow', 'Paint', 'Main', 'Basic', 'Normal', 'Level', 'Total', 'Type', 'Time',
          'Start', 'End', 'Note', 'Other', 'None', 'Free', 'Daily', 'Weekly', 'Event', 'Shop', 'Reward', 'Rewards'}


def path_of(lang, pid):
    return os.path.join(DOCS, *([lang] if lang != 'en' else []), pid + '.md')


def read(p):
    return open(p, encoding='utf8').read()


def body_of(text):
    m = re.match(r'---\n.*?\n---\n', text, flags=re.S)
    return text[m.end():] if m else text


def all_names():
    """Every record and notice name with en, zh-TW, ja and ko, and the game terms."""
    import check_jako_names
    names = [e for e in check_jako_names.entries() if e['en'] and e['ja'] and e['ko']]
    jako = json.load(open(os.path.join(ROOT, 'records', 'names-jako.json'), encoding='utf8'))
    names += [e for e in jako['names'] if e.get('ja') and e.get('ko')]
    names += [{'en': en, 'zh-TW': v['zh-TW'], 'ja': v['ja'], 'ko': v['ko']} for en, v in jako['terms'].items()]
    return names


def has(text, en):
    return re.search(r'(?<![A-Za-z])' + re.escape(en) + r'(?![A-Za-z])', text) is not None


def glossary(en_text, names):
    gloss = {}
    for e in sorted(names, key=lambda e: -len(e['en'])):
        en = e['en'].strip()
        if len(en) < 3 or en in gloss or en in COMMON or re.fullmatch(r'[\d.%+ ]+', en) or not has(en_text, en):
            continue
        gloss[en] = {'en': en, 'zh-TW': e.get('zh-TW', ''), 'ja': e['ja'], 'ko': e['ko']}
    # Capitalised phrases the records lack, looked up in the game's text tables (one rendering only).
    _, by_en = jako_text.index()
    for phrase in set(re.findall(r'\b[A-Z][A-Za-z\'-]+(?: (?:of |the )?[A-Z][A-Za-z\'-]+){0,4}\b', en_text)):
        if phrase in gloss or ' ' not in phrase:
            continue
        hits = by_en.get(phrase, set())
        if len(hits) == 1:
            tc, ja, ko = next(iter(hits))
            gloss[phrase] = {'en': phrase, 'zh-TW': tc, 'ja': ja, 'ko': ko}
    return sorted(gloss.values(), key=lambda g: g['en'])


def notice(lang, cid):
    p = os.path.join(ART, f'{lang}-{cid}.json')
    if not os.path.exists(p):
        return None
    d = json.load(open(p, encoding='utf8'))['data']
    text = re.sub(r'<br\s*/?>|</p>|</li>|</h\d>', '\n', d.get('data') or d.get('content') or '')
    text = re.sub(r'<[^>]+>', '', text)
    text = re.sub(r'&nbsp;', ' ', text)
    text = re.sub(r'\n\s*\n+', '\n', text).strip()
    return {'title': d.get('title', ''), 'text': text}


def sheet(out, pids):
    os.makedirs(out, exist_ok=True)
    names = all_names()
    for pid in pids:
        en = read(path_of('en', pid))
        cids = list(dict.fromkeys(re.findall(r'gryphline\.com/en-us/news/(\d+)', en)))
        notices = []
        for cid in cids:
            n = {'id': cid, 'en-us title': (notice('en-us', cid) or {}).get('title', '')}
            for lang in ('ja-jp', 'ko-kr'):
                got = notice(lang, cid)
                if got:
                    n[lang] = got
            notices.append(n)
        doc = {'page': pid,
               'english': os.path.relpath(path_of('en', pid), ROOT),
               'traditional_chinese': os.path.relpath(path_of('zh-tw', pid), ROOT),
               'write': {lang: os.path.relpath(path_of(lang, pid), ROOT) for lang in ('ja', 'ko')},
               'glossary': glossary(en, names),
               'notices': notices}
        p = os.path.join(out, pid.replace('/', '__') + '.json')
        with open(p, 'w', encoding='utf8') as f:
            json.dump(doc, f, ensure_ascii=False, indent=1)
        print(pid, len(doc['glossary']), 'glossary entries,', len(notices), 'notices')


def headings(body):
    return [len(m.group(1)) for m in re.finditer(r'^(#{2,6}) ', body, flags=re.M)]


NAMES_HEAD = re.compile(r'繁體中文|繁体字|번체')


def tables(body, names_col=False):
    """(rows, columns) of each table. With names_col, a table whose header names Traditional Chinese
    counts one column less: the Japanese or Korean page adds a column for its own game names there."""
    shapes, rows, cols = [], 0, None
    for line in body.split('\n') + ['']:
        if line.startswith('|'):
            rows += 1
            if cols is None:
                cols = len(re.findall(r'(?<!\\)\|', line)) - 1
                if names_col and NAMES_HEAD.search(line):
                    cols -= 1
        elif rows:
            shapes.append((rows, cols))
            rows, cols = 0, None
    return shapes


def links(body, lang):
    out = []
    for t in re.findall(r'\]\(([^)\s]+)\)', body):
        if lang != 'en' and t.startswith(f'/{lang}/'):
            t = t[len(lang) + 1:]
        out.append(t)
    return sorted(out)


def code(body):
    return re.findall(r'```.*?```|`[^`\n]+`', body, flags=re.S)


def numbers(s):
    s = re.sub(r'\]\([^)]*\)', ']', s)  # link targets
    return collections.Counter(re.findall(r'\d+(?:[.,]\d+)*', s.replace(',', '')))


def check(paths):
    names = all_names()
    bad = 0
    for path in paths:
        norm = os.path.abspath(path).replace(os.sep, '/')
        m = re.search(r'/src/content/docs/(ja|ko)/(.+)\.md$', norm)
        if not m:
            print(f'FAIL {path}: not a ja or ko page'); bad += 1; continue
        lang, pid = m.groups()
        fails, notes = [], []
        text, en_text = read(path), read(path_of('en', pid))
        fm, body = frontmatter(text)
        efm, ebody = frontmatter(en_text)
        if fm is None:
            print(f'FAIL {lang}/{pid}: no frontmatter'); bad += 1; continue
        for key in ('lastVerified', 'effectiveDate'):
            if fm.get(key) != efm.get(key):
                fails.append(f'{key} {fm.get(key)} differs from English {efm.get(key)}')
        urls = lambda d: [s.get('url') for s in d.get('sources') or [] if isinstance(s, dict)]
        if urls(fm) != urls(efm):
            fails.append('source URLs differ from English (same URLs, same order)')
        for key in ('title', 'description', 'appliesTo', 'caveat'):
            if not (fm.get(key) or '').strip('"'):
                fails.append(f'{key} is empty')
        desc = (fm.get('description') or '').strip('"')
        if len(desc) > LIMIT[lang]:
            fails.append(f'description is {len(desc)} characters, limit {LIMIT[lang]}')
        if headings(body) != headings(ebody):
            fails.append(f'heading levels {headings(body)} differ from English {headings(ebody)}')
        if tables(body, names_col=True) != tables(ebody) and tables(body) != tables(ebody):
            fails.append(f'table shapes (rows, columns) {tables(body)} differ from English {tables(ebody)}')
        if links(body, lang) != links(ebody, 'en'):
            a, b = links(body, lang), links(ebody, 'en')
            fails.append(f'link targets differ: only here {[x for x in a if x not in b]}; only in English {[x for x in b if x not in a]}')
        if code(body) != code(ebody):
            fails.append('code spans or blocks differ from English')
        gloss = glossary(ebody, names)
        a_, b_ = ebody, body
        for g in sorted(gloss, key=lambda g: -len(g['en'])):
            a_, b_ = a_.replace(g['en'], ' '), b_.replace(g[lang], ' ')
        na, nb = numbers(a_), numbers(b_)
        missing = na - nb
        extra = nb - na
        if missing:
            fails.append(f'numbers of the English body missing here: {dict(missing)}')
        if extra:
            notes.append(f'numbers here beyond the English body: {dict(extra)}')
        for g in gloss:
            if g[lang] not in body and len(g['en']) > 3:
                notes.append(f'glossary {g["en"]} -> {g[lang]} not on the page')
        if lang == 'ko' and re.search(r'[㐀-鿿]', body):
            notes.append('Han characters in Korean: ' + ' '.join(sorted(set(re.findall(r'[㐀-鿿]+', body)))[:10]))
        if lang == 'ja' and re.search(r'です。|ます。', body):
            notes.append('polite form (です・ます) in a だ・である page')
        if lang == 'ko' and re.search(r'습니다\.|해요\.|에요\.|이에요\.', body):
            notes.append('polite form in a -다 page')
        for f_ in fails:
            print(f'FAIL {lang}/{pid}: {f_}')
        for n in notes:
            print(f'NOTE {lang}/{pid}: {n}')
        bad += bool(fails)
    print('FAIL' if bad else 'ok', len(paths), 'pages,', bad, 'with failures')
    return 1 if bad else 0


def yaml_str(n):
    """A YAML scalar, quoted only where plain text would be read otherwise (scripts/to-zh-cn.py
    compares aliases as written)."""
    if ': ' in n or ' #' in n or n[:1] in '[]{}&*!|>\'"%@`,?:-#' or n != n.strip():
        return '"' + n.replace('"', '\\"') + '"'
    return n


def aliases(pids):
    for pid in pids:
        texts = {lang: read(path_of(lang, pid)) for lang in ('en', 'zh-tw', 'ja', 'ko')}
        names = []
        for lang, t in texts.items():
            fm, _ = frontmatter(t)
            for n in [fm.get('title', '')] + list(fm.get('aliases') or []):
                n = n.strip().strip('"')
                if n and n not in names:
                    names.append(n)
        for lang, t in texts.items():
            fm, _ = frontmatter(t)
            title = fm.get('title', '').strip().strip('"')
            rest = [n for n in names if n != title]
            block = 'aliases:\n' + ''.join(f'  - {yaml_str(n)}\n' for n in rest)
            new = re.sub(r'^aliases:\n(?:  - .*\n)*', block, t, count=1, flags=re.M)
            if new == t and 'aliases:' not in t.split('\n---\n')[0]:
                new = re.sub(r'^sources:', block + 'sources:', t, count=1, flags=re.M)
            if new != t:
                open(path_of(lang, pid), 'w', encoding='utf8').write(new)
                print('aliases', lang, pid, len(rest))


if __name__ == '__main__':
    cmd, args = sys.argv[1], sys.argv[2:]
    if cmd == 'sheet':
        sheet(args[0], args[1:])
    elif cmd == 'check':
        sys.exit(check(args))
    elif cmd == 'aliases':
        aliases(args)
