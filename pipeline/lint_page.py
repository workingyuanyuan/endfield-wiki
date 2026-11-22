"""Check one page without a build.

Usage: python3 -I pipeline/lint_page.py <page.md> [...]
A page under a zh-tw/ folder is checked as Traditional Chinese, any other as English.
Exit code 1 when a page has an error. Lines marked CHECK are facts the script could not
find in the cited notices: resolve each one (fix it, or cite the notice that has it).
"""
# Dates on which the pages were checked against their sources.
VERIFIED = ('2026-11-21', '2026-11-22')
import datetime
import json
import os
import re
import sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, os.path.join(ROOT, 'pipeline'))
from notice_text import text_of  # noqa: E402

REQUIRED = ['title', 'description', 'appliesTo', 'caveat', 'lastVerified', 'sources', 'aliases']
PAGES = set(open(os.path.join(ROOT, 'records', 'pages.txt'), encoding='utf8').read().split())


def frontmatter(text):
    m = re.match(r'---\n(.*?)\n---\n', text, flags=re.S)
    if not m:
        return None, text
    data, key = {}, None
    for line in m.group(1).split('\n'):
        if re.match(r'^[A-Za-z]+:', line):
            key, _, value = line.partition(':')
            value = value.strip()
            data[key] = value if value else []
        elif line.startswith('  - ') and isinstance(data.get(key), list):
            item = line[4:]
            if re.match(r'(title|url): ', item):
                k, _, v = item.partition(': ')
                data[key].append({k: v})
            else:
                data[key].append(item)
        elif line.startswith('    ') and isinstance(data.get(key), list) and data[key] and isinstance(data[key][-1], dict):
            k, _, v = line.strip().partition(': ')
            data[key][-1][k] = v
        else:
            data.setdefault('_bad', []).append(line)
    return data, text[m.end():]


def known_dates(cids):
    dates = set()
    for v in json.load(open(os.path.join(ROOT, 'records', 'versions.json'), encoding='utf8')):
        dates.update([v['asia'], v['americasEurope']])
    texts = []
    for cid in cids:
        path = os.path.join(ROOT, 'cache', 'official', 'art', f'zh-tw-{cid}.json')
        if not os.path.exists(path):
            continue
        _, shown, body = text_of(path)
        texts.append(body)
        tz = datetime.timezone(datetime.timedelta(hours=8))
        dates.add(datetime.datetime.fromtimestamp(int(shown), tz).strftime('%Y-%m-%d'))
        for y, mo, d in re.findall(r'(20\d\d)[/年](\d{1,2})[/月](\d{1,2})', body):
            dates.add(f'{y}-{int(mo):02d}-{int(d):02d}')
    for d in list(dates):
        day = datetime.date.fromisoformat(d)
        dates.add((day - datetime.timedelta(days=1)).isoformat())
    return dates, '\n'.join(texts)


def lint(path):
    errors, checks = [], []
    text = open(path, encoding='utf8').read()
    zh = '/zh-tw/' in path.replace(os.sep, '/')
    fm, body = frontmatter(text)
    if fm is None:
        return ['no frontmatter'], []
    for key in REQUIRED:
        if not fm.get(key):
            errors.append(f'frontmatter: {key} is missing or empty')
    for line in fm.get('_bad', []):
        errors.append(f'frontmatter: cannot read line: {line}')
    for key in ('title', 'description', 'appliesTo', 'caveat'):
        value = fm.get(key) or ''
        if isinstance(value, str):
            bare = value.strip('"')
            if ': ' in bare and not value.startswith('"'):
                errors.append(f'frontmatter: {key} contains ": " and must be in double quotes')
            if re.search(r'[*`\[\]]|\]\(', bare):
                errors.append(f'frontmatter: {key} contains Markdown')
    desc = (fm.get('description') or '').strip('"') if isinstance(fm.get('description'), str) else ''
    limit = 70 if zh else 110
    if len(desc) > limit:
        errors.append(f'description is {len(desc)} characters, limit {limit}')
    if fm.get('lastVerified') not in VERIFIED:
        errors.append(f'lastVerified must be one of {VERIFIED}')
    cids = []
    for s in fm.get('sources') or []:
        if not isinstance(s, dict) or not s.get('title') or not s.get('url'):
            errors.append(f'sources: each entry needs title and url: {s}')
            continue
        m = re.search(r'endfield\.gryphline\.com/([a-z-]+)/news/(\d+)', s['url'])
        if m:
            if m.group(1) != 'en-us':
                errors.append(f'sources: use the en-us notice URL in every language: {s["url"]}')
            cids.append(m.group(2))

    if re.search(r'(?<!:)//', re.sub(r'https?://\S+', '', body)):
        errors.append('body contains "//" (the skin draws it; write the section name without it)')
    if re.search(r'^#\s', body, flags=re.M):
        errors.append('body has a level-1 heading; the title comes from the frontmatter')
    if re.search(r'^\s*\$ ', body, flags=re.M):
        errors.append('a command carries a "$" prompt')
    if ':::' in body or re.search(r'<[A-Za-z][^>]*>', body):
        errors.append('body contains a directive or HTML; pages are plain Markdown')
    header = None
    for line in body.split('\n'):
        if line.startswith('|'):
            cells = len(re.findall(r'(?<!\\)\|', line)) - 1
            if header is None:
                header = cells
            elif cells != header:
                errors.append(f'table row has {cells} cells, header has {header}: {line[:60]}')
        else:
            header = None
    for target in re.findall(r'\]\((/[^)\s]*)\)', body):
        if target.startswith('/art/'):
            continue
        t = target.split('#')[0]
        if not t.endswith('/'):
            errors.append(f'link must end with a slash: {target}')
        if zh and not t.startswith('/zh-tw/'):
            errors.append(f'link in a zh-tw page must start with /zh-tw/: {target}')
        if not zh and re.match(r'/zh-(tw|cn)/', t):
            errors.append(f'link in an English page must not carry a language prefix: {target}')
        page = re.sub(r'^/zh-tw/', '/', t).strip('/')
        if (page or 'index') not in PAGES and (page + '/index') not in PAGES:
            errors.append(f'link to a page that is not planned: {target}')
    if re.search(r'\]\((?!/|https?://)', body):
        errors.append('a link is neither root-relative nor absolute')

    dates, notices = known_dates(cids)
    for d in sorted(set(re.findall(r'20\d\d-\d\d-\d\d', text))):
        if d not in dates and d not in VERIFIED:
            checks.append(f'date {d} is not in the cited notices')
    if zh:
        titles = json.dumps(json.load(open(os.path.join(ROOT, 'records', 'versions.json'), encoding='utf8')), ensure_ascii=False)
        for name in sorted(set(re.findall(r'「([^」]{2,30})」', body))):
            if name not in notices and name not in titles:
                checks.append(f'name 「{name}」 is not in the cited zh-tw notices')
    return errors, checks


if __name__ == '__main__':
    bad = False
    for path in sys.argv[1:]:
        errors, checks = lint(path)
        for e in errors:
            print(f'ERROR {path}: {e}')
        for c in checks:
            print(f'CHECK {path}: {c}')
        if not errors and not checks:
            print(f'ok    {path}')
        bad = bad or bool(errors)
    sys.exit(1 if bad else 0)
