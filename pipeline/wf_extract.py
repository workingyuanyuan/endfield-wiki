"""Cut a cached warfarin.wiki operator page down to the fields the records use.

Usage: python3 -I pipeline/wf_extract.py <lang>-<slug>.html [...]    (files in cache/third/wf/)
Writes cache/third/wf/json/<lang>-<slug>.json next to the cache.
The page carries the game's own tables (version in meta.version). Text keeps the
game's wording; rich-text tags are removed and {key:format} placeholders are
filled from the effect's own values.
"""
import json
import math
import os
import re
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from wf_decode import decode  # noqa: E402

GROUPS = {'NormalAttack': 'basic', 'NormalSkill': 'battle', 'ComboSkill': 'combo', 'UltimateSkill': 'ultimate'}
STAT_TYPES = {39: 'str', 40: 'agi', 41: 'int', 42: 'will', 2: 'atk', 1: 'hp'}


def plain(text):
    text = re.sub(r'<[@#][^>]*>', '', text or '')
    text = text.replace('</>', '')
    return re.sub(r'[ \t]*\n[ \t]*', '\n', text).strip()


def fmt(value, spec):
    if spec.endswith('%'):
        digits = len(spec.split('.')[1]) - 1 if '.' in spec else 0
        return f'{value * 100:.{digits}f}%'
    digits = len(spec.split('.')[1]) if '.' in spec else 0
    return f'{value:.{digits}f}'


def boards(effect):
    out = {}
    for item in effect.get('dataList') or []:
        for part in ('attachBuff', 'attachSkill'):
            for bb in (item.get(part) or {}).get('blackboard') or []:
                out.setdefault(bb['key'], bb['value'])
        mod = item.get('skillBbModifier') or {}
        if mod.get('bbKey'):
            out.setdefault(mod['bbKey'], mod.get('floatValue'))
    return out


def fill(text, values):
    def one(m):
        key, _, spec = m.group(1).partition(':')
        neg = key.startswith('-')
        key = key.lstrip('-')
        if key not in values or values[key] is None:
            return m.group(0)
        v = values[key]
        return fmt(-v if neg else v, spec or '0')
    return re.sub(r'\{([^{}]+)\}', one, text)


def page_text(html):
    html = re.sub(r'<script.*?</script>|<style.*?</style>', ' ', html, flags=re.S)
    text = re.sub(r'<[^>]+>', ' ', html)
    for a, b in (('&amp;', '&'), ('&lt;', '<'), ('&gt;', '>'), ('&quot;', '"'), ('&#x27;', "'"), ('&#39;', "'"), ('&nbsp;', ' ')):
        text = text.replace(a, b)
    return re.sub(r'\s+', ' ', text)


def from_page(text, page, nth=0):
    """Fill what is still a placeholder with the string the rendered page shows in its place."""
    if '{' not in text:
        return text
    lines = []
    for line in text.split('\n'):
        if '{' not in line:
            lines.append(line)
            continue
        parts = re.split(r'(\{[^{}]+\})', line)
        rx = r'\s*'.join(r'([-+]?\d[\d,]*(?:\.\d+)?%?)' if p.startswith('{') else r'\s*'.join(re.escape(ch) for ch in p if not ch.isspace())
                          for p in parts if p)
        found = list(re.finditer(rx, page))
        m = found[nth] if nth < len(found) else (found[-1] if found else None)
        if not m:
            lines.append(line)
            continue
        vals = iter(m.groups())
        lines.append(''.join(next(vals).strip() if p.startswith('{') else p for p in parts))
    return '\n'.join(lines)


def attr_name(refs, t):
    return refs['attributeShowConfigTable'][str(t)]['list'][0]['name']


def extract(path):
    html = open(path, encoding='utf8').read()
    page = page_text(html)
    root = decode(html)
    route = root['loaderData']['routes/$lang.operators.$slug']
    resp = route['response']
    D, refs = resp['data'], resp['refs']
    c, g, tags = D['characterTable'], D['charGrowthTable'], D['charTagTable']
    effects = D['potentialTalentEffectTable']
    items = {i['id']: i['name'] for i in route['itemsResponse']['data']}
    wtypes = route['weaponsResponse']['refs']['weaponTypes']

    def tag(tid):
        return (refs['tagDataTable'].get(tid) or {}).get('tagName', '')

    def stats(entry):
        a = {x['attrType']: x['attrValue'] for x in entry['Attribute']['attrs']}
        return {name: math.floor(a[t] + 1e-9) for t, name in STAT_TYPES.items()}

    level90 = [a for a in c['attributes'] if round(a['Attribute']['attrs'][0]['attrValue']) == 90][-1]

    skills = []
    for gid, grp in g['skillGroupMap'].items():
        kind = GROUPS[gid.rsplit('_', 1)[1]]
        parts = []
        for sid in grp['skillIdList']:
            bundle = (D['skillPatchTable'].get(sid) or {}).get('SkillPatchDataBundle') or []
            if not bundle:
                continue
            first, last = bundle[0], bundle[-1]
            parts.append({
                'id': sid,
                'levels': len(bundle),
                'costType': first['costType'],
                'cost': [first['costValue'], last['costValue']],
                'cooldown': [first['coolDown'], last['coolDown']],
                'rows': [{'name': a['name'], 'first': a['desc'], 'last': b['desc']}
                         for a, b in zip(first['subDescDataList'], last['subDescDataList'])],
            })
        desc = grp['desc']
        for n in ('1', '2'):
            # A skill with two forms keeps its text under each form's condition.
            if grp.get('conditionPostDesc' + n):
                cond = re.sub(r'\{[^{}]*\}|/\*|\*/|\(\s*\)|（\s*）', '', plain(grp.get('conditionDesc' + n, '')))
                desc += f"\n\n[{grp.get('conditionName' + n, '')}] {cond.strip()}\n{grp['conditionPostDesc' + n]}"
        skills.append({'kind': kind, 'name': grp['name'], 'desc': from_page(plain(desc), page), 'parts': parts})
    skills.sort(key=lambda s: list(GROUPS.values()).index(s['kind']))

    talents = {}
    for node in g['talentNodeMap'].values():
        p = node['passiveSkillNodeInfo']
        if node['nodeType'] != 4:
            continue
        eff = effects.get(p['talentEffectId']) or {}
        talents.setdefault(p['index'], {'name': p['name'], 'levels': []})['levels'].append({
            'level': p['level'], 'promotion': p['breakStage'], 'raw': plain(eff.get('desc', '')), 'boards': boards(eff),
        })
    talents = [talents[k] for k in sorted(talents)]
    for t in talents:
        t['levels'].sort(key=lambda x: x['level'])
        # The page prints the levels of a talent one after another, so level n is the nth match.
        for n, lv in enumerate(t['levels']):
            bare = lambda x: re.sub(r'\{[^{}]+\}', '{}', x['raw'])  # noqa: E731
            same = [x for x in t['levels'] if bare(x) == bare(lv)]
            lv['desc'] = fill(from_page(lv['raw'], page, same.index(lv)), lv['boards'])
        for lv in t['levels']:
            del lv['raw'], lv['boards']

    potentials = []
    for p in D['characterPotentialTable']['potentialUnlockBundle']:
        eff = effects.get(p['potentialEffectId']) or {}
        potentials.append({'level': p['level'], 'name': p['name'],
                           'desc': fill(from_page(plain(eff.get('desc', '')), page), boards(eff))})

    promotions = []
    for node in sorted(g['charBreakCostMap'].values(), key=lambda n: n['breakStage']):
        promotions.append({'id': node['nodeId'], 'stage': node['breakStage'], 'name': node['name'], 'desc': node['description'],
                           'items': [{'id': i['id'], 'name': items.get(i['id'], i['id']), 'count': i['count']}
                                     for i in node['requiredItem']]})

    return {
        'id': c['charId'], 'slug': resp['meta']['slug'], 'lang': resp['meta']['lang'],
        'version': resp['meta']['version'], 'name': c['name'], 'rarity': c['rarity'],
        'element': refs['charTypeTable'][c['charTypeId']]['name'], 'elementId': c['charTypeId'],
        'class': refs['charProfessionTable'][str(c['profession'])]['name'], 'classId': c['profession'],
        'weapon': wtypes.get(str(c['weaponType']), ''), 'weaponId': c['weaponType'],
        'mainAttr': attr_name(refs, c['mainAttrType']), 'subAttr': attr_name(refs, c['subAttrType']),
        'faction': tag(tags.get('blocTagId')), 'factionId': tags.get('blocTagId'),
        'race': tag(tags.get('raceTagId')), 'raceId': tags.get('raceTagId'),
        'cv': {k[:3].lower(): v for k, v in c['cvName'].items() if k.endswith('CVName')},
        'desc': D['itemTable']['desc'],
        'skills': skills, 'talents': talents, 'potentials': potentials,
        'stats': {'1': stats(c['attributes'][0]), '90': stats(level90)},
        'promotions': promotions,
        'banners': route.get('banners') or [],
    }


if __name__ == '__main__':
    for path in sys.argv[1:]:
        out_dir = os.path.join(os.path.dirname(path), 'json')
        os.makedirs(out_dir, exist_ok=True)
        data = extract(path)
        out = os.path.join(out_dir, os.path.basename(path).replace('.html', '.json'))
        json.dump(data, open(out, 'w', encoding='utf8'), ensure_ascii=False, indent=1)
