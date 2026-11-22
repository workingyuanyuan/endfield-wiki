"""Check the game names on Japanese and Korean pages.

Usage: python3 -I pipeline/check_jako_names.py [page.md ...]
Without arguments, checks every page under src/content/docs/ja/ and ko/. Exit code 1 on a miss.

1. MISSING  A name that the English page with the same id shows in a table cell (alone, or in a
            list joined by ", ", "; ", " or ", " and ") has a Japanese or Korean form in
            records/names-jako.json or in the records written by ed_extract.py, and that form is
            not on the page.
2. CHINESE  A Traditional Chinese name of the records (one with a CJK ideograph, two characters or
            more, and not also the page language's form of some name) is on the page outside a
            Chinese name column (a header with 中文, 中国語, 중국어, 繁体, 簡体, 번체 or 간체) and
            outside a sentence that names the script (繁体字, 簡体字, 번체, 간체).
The body is checked; the frontmatter is not (aliases hold every language's title on purpose).
"""
import glob
import os
import re
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import build_pages as bp  # noqa: E402

DOCS = bp.DOCS
EN, ZH = bp.EN, bp.ZH
CJK = re.compile(r'[㐀-鿿]')
CHINESE_HEAD = re.compile(r'中文|中国語|중국어|繁体|簡体|繁體|簡體|번체|간체')
SCRIPT_SENTENCE = re.compile(r'繁体字|簡体字|번체|간체')


def entries():
    """Every name with en, zh-TW, ja and ko: records (enriched from names-jako.json) and voices.
    Prose (changes.json, the 'with' field of obtain.json) is not a name."""
    out = []

    def walk(o, path):
        if isinstance(o, dict):
            if all(isinstance(o.get(k), str) for k in (EN, ZH, 'ja', 'ko')) and not path.endswith('/with'):
                out.append(o)
            for k, v in o.items():
                walk(v, f'{path}/{k}')
        elif isinstance(o, list):
            for v in o:
                walk(v, path)
    for f in sorted(glob.glob(os.path.join(bp.ROOT, 'records', '*.json'))):
        name = os.path.basename(f)
        if name in ('names-jako.json', 'names-voc.json', 'pending.json', 'changes.json', 'pages.txt'):
            continue
        walk(bp.load(name), name)
    for op in bp.OPS.values():
        walk({k: v for k, v in op.items() if k not in ('text', 'voice')}, 'operators')
        for key, en in op['voice'][EN].items():
            out.append({EN: en, ZH: op['voice'][ZH][key], 'ja': op['voice']['ja'][key], 'ko': op['voice']['ko'][key]})
    return out


def body_of(text):
    m = re.match(r'---\n.*?\n---\n', text, flags=re.S)
    return text[m.end():] if m else text


def cell_tokens(body):
    """Names shown in table cells (header rows excluded): whole cells and the parts of list-like cells."""
    out = set()
    prev = ''
    for line in body.split('\n'):
        header = not prev.startswith('|')
        prev = line
        if not line.startswith('|') or set(line) <= set('|- ') or header:
            continue
        for cell in line.strip().strip('|').split('|'):
            cell = re.sub(r'\[([^\]]*)\]\([^)]*\)', r'\1', cell.strip())
            for part in re.split(r', |; | or | and |: ', cell):
                part = re.sub(r' ×\d+$', '', part.strip())
                part = re.sub(r' [αβγ]$', '', part)
                if part:
                    out.add(part)
    return out


def outside_chinese(body):
    """The body without Chinese name columns and without sentences that name a Chinese script."""
    keep, drop = [], set()
    for line in body.split('\n'):
        if line.startswith('|'):
            cells = line.strip().strip('|').split('|')
            if not drop and not set(line) <= set('|- '):
                header = cells
                drop = {i for i, c in enumerate(header) if CHINESE_HEAD.search(c)}
                keep.append('|'.join(c for i, c in enumerate(cells) if i not in drop))
                continue
            keep.append('|'.join(c for i, c in enumerate(cells) if i not in drop))
        else:
            drop = set()
            keep.append(' '.join(s for s in re.split(r'(?<=[。！？])|(?<=[.!?])\s+', line) if s and not SCRIPT_SENTENCE.search(s)))
    return '\n'.join(keep)


def check(path, names, by_en):
    rel = os.path.relpath(path, DOCS).replace(os.sep, '/')
    lang, page_id = rel.split('/', 1)
    body = body_of(open(path, encoding='utf8').read())
    hits = []
    en_path = os.path.join(DOCS, page_id)
    if os.path.exists(en_path):
        en_body = body_of(open(en_path, encoding='utf8').read())
        for token in sorted(cell_tokens(en_body)):
            forms = {e[lang] for e in by_en.get(token, [])}
            if forms and not any(f in body for f in forms):
                hits.append(f'MISSING {path}: "{token}" has no {" / ".join(sorted(forms))} on the page')
    own = {e[lang] for e in names}
    text = outside_chinese(body)
    for form in sorted(own, key=len, reverse=True):
        if CJK.search(form):
            text = text.replace(form, '\u0000')
    for zh in sorted({e[ZH] for e in names}, key=len, reverse=True):
        if len(zh) >= 2 and CJK.search(zh) and zh not in own and zh in text:
            line = next(x for x in text.split('\n') if zh in x)
            hits.append(f'CHINESE {path}: "{zh}" in: {line.strip()[:90]}')
    return hits


def main():
    paths = sys.argv[1:] or sorted(glob.glob(os.path.join(DOCS, 'ja', '**', '*.md'), recursive=True) +
                                   glob.glob(os.path.join(DOCS, 'ko', '**', '*.md'), recursive=True))
    names = entries()
    by_en = {}
    for e in names:
        by_en.setdefault(e[EN], []).append(e)
    bad = 0
    for path in paths:
        hits = check(os.path.abspath(path), names, by_en)
        for h in hits:
            print(h)
        bad += bool(hits)
    print(f'{len(paths)} pages, {len(names)} names; {bad} pages with a miss')
    sys.exit(1 if bad else 0)


if __name__ == '__main__':
    main()
