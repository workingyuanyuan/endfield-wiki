"""Write the source sheet a writer restates an operator from.

Usage: python3 -I pipeline/text_sheet.py <out dir> <slug> [...]
The sheet holds the game's own text in English and Traditional Chinese (from the
cache) and the official introduction. It is working material and is not committed.
"""
import json
import os
import sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
WF = os.path.join(ROOT, 'cache', 'third', 'wf', 'json')
SLUGS = {'mi-fu': 'mifu'}


def sheet(slug):
    wf = SLUGS.get(slug, slug)
    en = json.load(open(os.path.join(WF, f'en-{wf}.json'), encoding='utf8'))
    tc = json.load(open(os.path.join(WF, f'tc-{wf}.json'), encoding='utf8'))
    record = json.load(open(os.path.join(ROOT, 'records', 'operators', f'{slug}.json'), encoding='utf8'))
    official = json.load(open(os.path.join(ROOT, 'cache', 'official', 'operators.json'), encoding='utf8'))
    key = record['officialKey']
    intro = {}
    for lang, name in (('en', 'en'), ('zh-TW', 'zh-TW')):
        text = (official.get(lang) or {}).get('text') or {}
        intro[name] = text.get(f'operator.content.{key}.intro', '')
        if not intro[name]:
            for row in (official.get(lang) or {}).get('roster') or []:
                if row.get('key') == key:
                    intro[name] = row.get('intro', '')
    out = {
        'slug': slug,
        'name': {'en': en['name'], 'zh-TW': tc['name']},
        'profile': {'en': f"{en['rarity']}-star {en['element']} {en['class']}, {en['weapon']}", 'zh-TW': f"{tc['rarity']} 星 {tc['element']} {tc['class']}，{tc['weapon']}"},
        'gameSummary': {'en': en['desc'], 'zh-TW': tc['desc']},
        'officialIntro': intro,
        'skills': {},
        'talents': [],
        'potentials': [],
    }
    for a, b in zip(en['skills'], tc['skills']):
        out['skills'][a['kind']] = {
            'name': {'en': a['name'], 'zh-TW': b['name']},
            'gameText': {'en': a['desc'], 'zh-TW': b['desc']},
            'values': [{'en': r['name'], 'zh-TW': q['name'], 'level1': r['first'], 'level12': r['last']}
                       for p, pb in zip(a['parts'], b['parts']) for r, q in zip(p['rows'], pb['rows'])],
        }
    for a, b in zip(en['talents'], tc['talents']):
        out['talents'].append({
            'name': {'en': a['name'], 'zh-TW': b['name']},
            'levels': [{'unlockedAtPromotion': x['promotion'], 'gameText': {'en': x['desc'], 'zh-TW': y['desc']}}
                       for x, y in zip(a['levels'], b['levels'])],
        })
    for a, b in zip(en['potentials'], tc['potentials']):
        out['potentials'].append({'name': {'en': a['name'], 'zh-TW': b['name']},
                                  'gameText': {'en': a['desc'], 'zh-TW': b['desc']}})
    return out


if __name__ == '__main__':
    out_dir = sys.argv[1]
    os.makedirs(out_dir, exist_ok=True)
    for slug in sys.argv[2:]:
        json.dump(sheet(slug), open(os.path.join(out_dir, f'{slug}.json'), 'w', encoding='utf8'), ensure_ascii=False, indent=1)
