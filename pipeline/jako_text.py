"""Japanese and Korean restated operator text: sheets for the writer, a check, and the merge.

Usage:
  python3 -I pipeline/jako_text.py sheet <out dir> [slug ...]    # one sheet per operator
  python3 -I pipeline/jako_text.py check <file.json> [...]        # a writer's output, without a build
  python3 -I pipeline/jako_text.py merge <file.json> [...]        # add ja/ko to records/text/<slug>.json

A sheet holds the operator's restated English and Traditional Chinese text (records/text) and a
glossary: the game's own Japanese and Korean form of every game name on the operator's record and
of every game term whose English form occurs in the English text, read from the game's text
tables by the pair (English text, Traditional Chinese text). The writer translates the restated
English text, using the glossary forms, into a file of the form
  {"slug": ..., "ja": <same shape as the English text>, "ko": <same shape>}
where the shape is intro (string), skills {basic, battle, combo, ultimate} (strings), talents and
potentials (lists of strings, same length as in English).
"""
import collections
import json
import os
import re
import sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
ED = os.path.join(ROOT, 'cache', 'third', 'ed', 'd847759f71d4549aba4727b3b0ac1a1ad0e37742')
LIMIT = {'ja': 220, 'ko': 300}
KINDS = ['basic', 'battle', 'combo', 'ultimate']
# Terms the restated text uses that are not in the game's term list.
BASICS = ['Basic Attack', 'Battle Skill', 'Combo Skill', 'Ultimate', 'Final Strike', 'Finisher', 'Dive Attack',
          'Ultimate Energy', 'SP', 'Stagger', 'Staggered', 'Promotion I', 'Promotion II', 'Promotion III', 'Promotion IV',
          'Max HP', 'HP', 'ATK', 'DEF', 'Strength', 'Agility', 'Intellect', 'Will', 'Critical Rate', 'Critical DMG',
          'Protection', 'Shield', 'Vulnerable', 'Lift', 'Knock Down', 'Crush', 'Breach', 'Arts Infliction', 'Arts Burst',
          'Heat Infliction', 'Electric Infliction', 'Cryo Infliction', 'Nature Infliction', 'Combustion', 'Electrification',
          'Solidification', 'Corrosion', 'Physical DMG', 'Heat DMG', 'Electric DMG', 'Cryo DMG', 'Nature DMG', 'Arts DMG',
          'Heat Resistance', 'Electric Resistance', 'Cryo Resistance', 'Nature Resistance', 'Physical Resistance',
          'Treatment', 'Healing', 'Link', 'Slow', 'Immobilization', 'Stun', 'Freeze', 'Controlled Operator', 'Physical Status',
          'Arts Reaction', 'Æther DMG', 'Originium Crystals', 'Weaken', 'Susceptibility', 'Amp']


def load(path):
    return json.load(open(path, encoding='utf8'))


RAW = {}


def strip(s):
    return re.sub(r'<[^>]*>|\{[^}]*\}', '', s or '').strip()


def index():
    T = {k: load(os.path.join(ED, f'I18nTextTable_{k}.json')) for k in ('EN', 'TC', 'JP', 'KR')}
    RAW.update(T)
    by_pair, by_en = collections.defaultdict(set), collections.defaultdict(set)
    for i, en in T['EN'].items():
        tc, ja, ko = T['TC'].get(i), T['JP'].get(i), T['KR'].get(i)
        if tc and ja and ko:
            by_pair[(en.strip(), tc.strip())].add((ja.strip(), ko.strip()))
            by_en[en.strip()].add((tc.strip(), ja.strip(), ko.strip()))
    for i, en in T['EN'].items():
        m = re.fullmatch(r'Arts Reaction: (\w+)', strip(en))
        if m and T['JP'].get(i) and T['KR'].get(i):
            parts = [re.split(r'\s*[-:：－]\s*|・', strip(T[k][i]))[-1] for k in ('TC', 'JP', 'KR')]
            by_en[m.group(1)].add(tuple(parts))
    return by_pair, by_en


def names_of(x):
    if isinstance(x, dict):
        if isinstance(x.get('en'), str) and isinstance(x.get('zh-TW'), str):
            yield x['en'], x['zh-TW']
            return
        for v in x.values():
            yield from names_of(v)
    elif isinstance(x, list):
        for v in x:
            yield from names_of(v)


def strings(text, lang):
    yield text['intro'][lang]
    for k in KINDS:
        yield text['skills'][k][lang]
    for t in text['talents'] + text['potentials']:
        yield t[lang]


def sheet(out, slugs):
    by_pair, by_en = index()
    terms = [v['name'] for v in load(os.path.join(ROOT, 'cache', 'third', 'wf', 'terms-en.json')).values()]
    os.makedirs(out, exist_ok=True)
    for slug in slugs:
        text = load(os.path.join(ROOT, 'records', 'text', slug + '.json'))
        rec = load(os.path.join(ROOT, 'records', 'operators', slug + '.json'))
        en_all = ' '.join(strings(text, 'en'))
        gloss = {}
        for en, tc in names_of(rec):
            hits = by_pair.get((en.strip(), tc.strip()), set())
            if len(hits) == 1 and en not in gloss and not re.fullmatch(r'[\d.%+ ]+', en):
                ja, ko = next(iter(hits))
                gloss[en] = {'en': en, 'zh-TW': tc, 'ja': ja, 'ko': ko}
        for en in sorted(set(terms + BASICS), key=len, reverse=True):
            if en in gloss or not re.search(r'(?<![A-Za-z])' + re.escape(en) + r'(?![A-Za-z])', en_all, re.I):
                continue
            hits = by_en.get(en, set())
            if not hits:
                continue
            # The most common rendering when one English term has several texts.
            tc, ja, ko = collections.Counter(hits).most_common(1)[0][0] if len(hits) == 1 else sorted(hits, key=lambda h: (len(h[1]), h))[0]
            gloss[en] = {'en': en, 'zh-TW': tc, 'ja': ja, 'ko': ko}
        # The game's own text that names the operator's skills, talents or potentials, in four
        # languages: for terms only (statuses, effects), never to copy from.
        own = [x['name']['en'] for x in rec['skills'] + rec['talents'] + rec['potentials'] if len(x['name']['en']) > 4]
        refs = []
        for i, en in RAW['EN'].items():
            plain = strip(en)
            if 40 <= len(plain) <= 700 and any(n in plain for n in own) and all(RAW[k].get(i) for k in ('JP', 'KR')):
                item = {'en': plain, 'ja': strip(RAW['JP'][i]), 'ko': strip(RAW['KR'][i])}
                if item not in refs:
                    refs.append(item)
        doc = {'slug': slug, 'reference': refs[:30], 'name': gloss.get(rec['name']['en'], rec['name']),
               'text': {'intro': text['intro'], 'skills': text['skills'], 'talents': text['talents'], 'potentials': text['potentials']},
               'glossary': sorted(gloss.values(), key=lambda g: g['en'])}
        with open(os.path.join(out, slug + '.json'), 'w', encoding='utf8') as f:
            json.dump(doc, f, ensure_ascii=False, indent=1)
        print(slug, len(gloss), 'glossary entries')


def numbers(s):
    return collections.Counter(re.findall(r'\d+(?:\.\d+)?', s))


def check(paths):
    bad = 0
    for path in paths:
        out = load(path)
        slug = out['slug']
        text = load(os.path.join(ROOT, 'records', 'text', slug + '.json'))
        sheet_path = os.path.join(os.path.dirname(path), '..', 'sheets', slug + '.json')
        gloss = load(sheet_path)['glossary'] if os.path.exists(sheet_path) else []
        en = list(strings(text, 'en'))
        for lang in ('ja', 'ko'):
            t = out.get(lang)
            if not t:
                print(f'FAIL {slug} {lang}: missing'); bad += 1; continue
            if len(t.get('talents', [])) != len(text['talents']) or len(t.get('potentials', [])) != len(text['potentials']):
                print(f'FAIL {slug} {lang}: talents or potentials count differs'); bad += 1; continue
            got = list(strings({'intro': {lang: t['intro']}, 'skills': {k: {lang: t['skills'][k]} for k in KINDS},
                                'talents': [{lang: x} for x in t['talents']], 'potentials': [{lang: x} for x in t['potentials']]}, lang))
            for i, (a, b) in enumerate(zip(en, got)):
                where = f'{slug} {lang} #{i}'
                if not b.strip():
                    print(f'FAIL {where}: empty'); bad += 1
                # Numbers inside game names (Yinglung Stance IV is 응룡 4식 in Korean) are not facts to compare.
                a_, b_ = a, b
                for g in sorted(gloss, key=lambda g: -len(g['en'])):
                    a_, b_ = a_.replace(g['en'], ' '), b_.replace(g[lang], ' ')
                if numbers(a_) != numbers(b_):
                    print(f'FAIL {where}: numbers {dict(numbers(a))} vs {dict(numbers(b))}'); bad += 1
                if len(b) > LIMIT[lang]:
                    print(f'FAIL {where}: {len(b)} characters, limit {LIMIT[lang]}'); bad += 1
                if re.search(r'[㐀-鿿]', b) and lang == 'ko':
                    print(f'NOTE {where}: Han characters in Korean: {b[:60]}')
                for g in gloss:
                    if re.search(r'(?<![A-Za-z])' + re.escape(g['en']) + r'(?![A-Za-z])', a) and g[lang] not in b:
                        print(f'NOTE {where}: glossary {g["en"]} -> {g[lang]} not found')
    print('FAIL' if bad else 'ok', len(paths), 'files,', bad, 'failures')
    return 1 if bad else 0


def merge(paths):
    for path in paths:
        out = load(path)
        p = os.path.join(ROOT, 'records', 'text', out['slug'] + '.json')
        text = load(p)
        for lang in ('ja', 'ko'):
            t = out[lang]
            text['intro'][lang] = t['intro']
            for k in KINDS:
                text['skills'][k][lang] = t['skills'][k]
            for x, v in zip(text['talents'], t['talents']):
                x[lang] = v
            for x, v in zip(text['potentials'], t['potentials']):
                x[lang] = v
        with open(p, 'w', encoding='utf8') as f:
            json.dump(text, f, ensure_ascii=False, indent=1)
            f.write('\n')
        print('merged', out['slug'])


if __name__ == '__main__':
    cmd, args = sys.argv[1], sys.argv[2:]
    if cmd == 'sheet':
        slugs = args[1:] or sorted(f[:-5] for f in os.listdir(os.path.join(ROOT, 'records', 'text')) if f.endswith('.json'))
        sheet(args[0], slugs)
    elif cmd == 'check':
        sys.exit(check(args))
    elif cmd == 'merge':
        merge(args)
