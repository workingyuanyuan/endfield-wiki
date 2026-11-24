"""Write the facts part of every operator record from the cached game data.

Usage: python3 -I pipeline/build_records.py
Reads cache/third/wf/json/<lang>-<slug>.json (made by wf_extract.py) and
cache/official/roster-rows.json; writes records/operators/<slug>.json.
Names and numbers only: the game's description text stays in the cache.
The game's own text of an operator is a separate file, records/gametext/<slug>.json
(pipeline/gametext.py).
"""
import glob
import json
import os

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
WF = os.path.join(ROOT, 'cache', 'third', 'wf', 'json')
LANGS = {'en': 'en', 'tc': 'zh-TW', 'cn': 'zh-CN'}
SLUGS = {'mifu': 'mi-fu'}


def tri(src, pick):
    return {LANGS[l]: pick(src[l]) for l in LANGS}


def main():
    roster = json.load(open(os.path.join(ROOT, 'cache', 'official', 'roster-rows.json'), encoding='utf8'))
    official = {}
    for key, en, tw, cn, rarity, _, _ in roster:
        official.setdefault(en, {'key': key, 'zh-TW': tw, 'zh-CN': cn, 'rarity': int(rarity)})
    os.makedirs(os.path.join(ROOT, 'records', 'operators'), exist_ok=True)
    problems = []
    for path in sorted(glob.glob(os.path.join(WF, 'en-*.json'))):
        wf_slug = os.path.basename(path)[3:-5]
        src = {l: json.load(open(os.path.join(WF, f'{l}-{wf_slug}.json'), encoding='utf8')) for l in LANGS}
        en = src['en']
        slug = SLUGS.get(wf_slug, wf_slug)
        off = official.get(en['name'])
        if not off:
            problems.append(f'{slug}: not in the official list under the name {en["name"]}')
        else:
            for lang, l in (('zh-TW', 'tc'), ('zh-CN', 'cn')):
                if off[lang] != src[l]['name']:
                    problems.append(f'{slug}: {lang} name differs: official {off[lang]}, game data {src[l]["name"]}')
            if off['rarity'] != en['rarity']:
                problems.append(f'{slug}: rarity differs')
        record = {
            'slug': slug,
            'gameId': en['id'],
            'gameDataVersion': en['version'],
            'gameDataPage': f'https://warfarin.wiki/en/operators/{wf_slug}',
            'officialKey': off['key'] if off else None,
            'name': tri(src, lambda d: d['name']),
            'rarity': en['rarity'],
            'class': tri(src, lambda d: d['class']),
            'element': tri(src, lambda d: d['element']),
            'weapon': tri(src, lambda d: d['weapon']),
            'mainAttr': tri(src, lambda d: d['mainAttr']),
            'subAttr': tri(src, lambda d: d['subAttr']),
            'faction': tri(src, lambda d: d['faction']),
            'race': tri(src, lambda d: d['race']),
            'voice': tri(src, lambda d: d['cv']),
            'skills': [],
            'talents': [],
            'potentials': [],
            'stats': en['stats'],
            'promotions': [],
        }
        for i, s in enumerate(en['skills']):
            main = s['parts'][0]
            values, seen = [], set()
            for a, b in zip(s['parts'], src['tc']['skills'][i]['parts']):
                for r, q in zip(a['rows'], b['rows']):
                    key = (r['name'], r['first'], r['last'])
                    if key not in seen:
                        seen.add(key)
                        values.append({'name': {'en': r['name'], 'zh-TW': q['name']}, 'first': r['first'], 'last': r['last']})
            record['skills'].append({
                'kind': s['kind'],
                'name': tri(src, lambda d: d['skills'][i]['name']),
                'cost': main['cost'][0],
                'cooldown': main['cooldown'],
                'levels': main['levels'],
                'values': values,
            })
        for i, t in enumerate(en['talents']):
            record['talents'].append({
                'name': tri(src, lambda d: d['talents'][i]['name']),
                'promotions': [lv['promotion'] for lv in t['levels']],
            })
        for i, p in enumerate(en['potentials']):
            record['potentials'].append({'level': p['level'], 'name': tri(src, lambda d: d['potentials'][i]['name'])})
        for i, p in enumerate(en['promotions']):
            if not p['items'] or not p['id'].startswith('charBreak'):
                continue
            record['promotions'].append({
                'stage': p['stage'],
                'name': tri(src, lambda d: d['promotions'][i]['name']),
                'levelCap': int(''.join(ch for ch in p['desc'] if ch.isdigit())),
                'items': [{'name': tri(src, lambda d: d['promotions'][i]['items'][j]['name']), 'count': it['count']}
                          for j, it in enumerate(p['items'])],
            })
        out = os.path.join(ROOT, 'records', 'operators', f'{slug}.json')
        json.dump(record, open(out, 'w', encoding='utf8'), ensure_ascii=False, indent=1)
    for p in problems:
        print('CHECK', p)
    print(len(glob.glob(os.path.join(ROOT, 'records', 'operators', '*.json'))), 'records')


if __name__ == '__main__':
    main()
