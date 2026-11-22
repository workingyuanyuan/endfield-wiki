"""Cut cached warfarin.wiki pages (game data) down to what the system pages are written from.

Usage: python3 -I pipeline/wf_misc.py
Writes, under cache/third/wf/:
  terms-<lang>.json            combat and item terms with the game's own explanation
  tut/text/<lang>-<id>.md      in-game tutorial pages as text
  facilities.json              AIC facilities: names in three scripts, group, power use, footprint, recipes
  weapons.json, gear-sets.json lists for the lookup tables
"""
import glob
import json
import os
import re
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from wf_decode import decode  # noqa: E402
from wf_extract import plain  # noqa: E402

WF = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), 'cache', 'third', 'wf')
LANGS = {'en': 'en', 'tc': 'zh-TW', 'cn': 'zh-CN'}


def route(path, key):
    return decode(open(path, encoding='utf8').read())['loaderData'][key]


def terms():
    for lang in LANGS:
        r = route(os.path.join(WF, f'{lang}-laevatain.html'), 'routes/$lang.operators.$slug')
        tips = r['config']['tooltips']
        out = {k: {'name': v['name'], 'desc': plain(v['desc'])} for k, v in sorted(tips.items())}
        json.dump(out, open(os.path.join(WF, f'terms-{lang}.json'), 'w', encoding='utf8'), ensure_ascii=False, indent=1)


def tutorials():
    os.makedirs(os.path.join(WF, 'tut', 'text'), exist_ok=True)
    for path in sorted(glob.glob(os.path.join(WF, 'tut', '??-wiki_tut_*.html'))):
        base = os.path.basename(path)[:-5]
        data = route(path, 'routes/$lang.tutorials.$slug')['response']
        pages = data['data']['wikiTutorialPageTable']
        lines = [f"# {data['meta']['name']}", f"(in-game tutorial {data['meta']['id']}, game data {data['meta']['version']}, https://warfarin.wiki/{data['meta']['lang']}/tutorials/{data['meta']['id']})", '']
        for p in sorted(pages.values(), key=lambda x: x['order']):
            lines += [f"## {p['title']}", plain(p['content']), '']
        open(os.path.join(WF, 'tut', 'text', base + '.md'), 'w', encoding='utf8').write('\n'.join(lines))


def facilities():
    names, groups = {}, {}
    for lang in LANGS:
        for g in route(os.path.join(WF, f'list-facilities-{lang}.html'), 'routes/$lang.facilities._index')['response']['data']:
            for e in g['entries']:
                names.setdefault(e['id'], {})[LANGS[lang]] = e['name']
                if lang == 'en':
                    groups[e['id']] = g['groupName']
    out = []
    for path in sorted(glob.glob(os.path.join(WF, 'tut', 'fac-en-*.html'))):
        r = route(path, 'routes/$lang.facilities.$slug')
        d = r['response']['data']
        b = d['factoryBuildingTable']
        item_names = {i['id']: i['name'] for i in (r.get('itemsResponse') or {}).get('data') or []}
        recipes = []
        for c in d.get('factoryMachineCraftTable') or []:
            def side(key):
                got = []
                for grp in c.get(key) or []:
                    for it in grp.get('group') or []:
                        got.append({'item': item_names.get(it['id'], it['id']), 'count': it['count']})
                return got
            recipes.append({'in': side('ingredients'), 'out': side('outcomes'), 'seconds': c.get('progressRound'), 'mode': c.get('formulaGroupId')})
        out.append({'id': b['id'], 'name': names.get(b['id'], {'en': b['name']}), 'group': groups.get(b['id']),
                    'power': b['powerConsume'], 'needsPower': b['needPower'], 'bandwidth': b['bandwidth'],
                    'width': b['range']['width'], 'depth': b['range']['depth'], 'desc': b['desc'], 'recipes': recipes,
                    'page': f"https://warfarin.wiki/en/facilities/{b['id']}"})
    json.dump(out, open(os.path.join(WF, 'facilities.json'), 'w', encoding='utf8'), ensure_ascii=False, indent=1)


def gear_sets():
    from wf_extract import from_page, page_text
    sets = json.load(open(os.path.join(WF, 'gear-sets.json'), encoding='utf8'))
    for s in sets:
        s['effect'] = {}
        for lang in ('en', 'tc'):
            path = os.path.join(WF, 'gear', f"{lang}-{s['first']}.html")
            if not os.path.exists(path):
                continue
            html = open(path, encoding='utf8').read()
            d = decode(html)['loaderData']['routes/$lang.gear.$slug']['response']['data']
            blob = json.dumps(d['skillPatchTable'], ensure_ascii=False)
            texts = [x for x in re.findall(r'"description": "((?:[^"\\]|\\.)+)"', blob)]
            texts = [json.loads('"' + t + '"') for t in texts]
            if texts:
                s['effect'][LANGS[lang]] = from_page(plain(texts[0]), page_text(html))
    json.dump(sets, open(os.path.join(WF, 'gear-sets.json'), 'w', encoding='utf8'), ensure_ascii=False, indent=1)


def recipes_tc():
    """Item names of recipes in Traditional Chinese, matched to the English ones by position."""
    path = os.path.join(WF, 'facilities.json')
    fac = json.load(open(path, encoding='utf8'))
    for f in fac:
        tc = os.path.join(WF, 'tut', f"fac-tc-{f['id']}.html")
        if not os.path.exists(tc) or not f['recipes']:
            continue
        r = route(tc, 'routes/$lang.facilities.$slug')
        names = {i['id']: i['name'] for i in (r.get('itemsResponse') or {}).get('data') or []}
        en = route(os.path.join(WF, 'tut', f"fac-en-{f['id']}.html"), 'routes/$lang.facilities.$slug')
        en_names = {i['id']: i['name'] for i in (en.get('itemsResponse') or {}).get('data') or []}
        f['itemNames'] = {en_names[i]: names[i] for i in en_names if i in names}
        f['desc_zh-TW'] = r['response']['data']['factoryBuildingTable']['desc']
    json.dump(fac, open(path, 'w', encoding='utf8'), ensure_ascii=False, indent=1)


def weapons():
    rows = {}
    for lang in LANGS:
        r = route(os.path.join(WF, f'list-weapons-{lang}.html'), 'routes/$lang.weapons._index')['response']
        types = r['refs']['weaponTypes']
        for w in r['data']:
            row = rows.setdefault(w['id'], {'id': w['id'], 'slug': w['slug'], 'rarity': w['rarity'], 'name': {}, 'type': {}})
            row['name'][LANGS[lang]] = w['name']
            row['type'][LANGS[lang]] = types[str(w['weaponType'])]
    json.dump(sorted(rows.values(), key=lambda x: (-x['rarity'], x['type']['en'], x['name']['en'])),
              open(os.path.join(WF, 'weapons.json'), 'w', encoding='utf8'), ensure_ascii=False, indent=1)


if __name__ == '__main__':
    terms()
    weapons()
    tutorials()
    facilities()
    recipes_tc()
    gear_sets()
