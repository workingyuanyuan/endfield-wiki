"""Read the game's recommended weapons and base skills from the client tables
and write records/recommend.json and records/base-skills.json.

Usage: python3 -I pipeline/ed_extract.py
Reads cache/third/ed/<commit>/ (tables of github.com/rmxlinux/EndfieldData at
that commit; the cache is not committed) and records/operators/, weapons.json.
The game's description text is not written to records: base-skill effects are
stored as a kind and a number, and the page scripts word them.
"""
import glob
import json
import os
import re

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
COMMIT = 'd847759f71d4549aba4727b3b0ac1a1ad0e37742'
ED = os.path.join(ROOT, 'cache', 'third', 'ed', COMMIT)
SOURCE = f'https://github.com/rmxlinux/EndfieldData/tree/{COMMIT}/TableCfg'


def table(name):
    return json.load(open(os.path.join(ED, name + '.json'), encoding='utf8'))


TEXT = {'en': table('I18nTextTable_EN'), 'zh-TW': table('I18nTextTable_TC'), 'zh-CN': table('I18nTextTable_CN'),
        'ja': table('I18nTextTable_JP'), 'ko': table('I18nTextTable_KR')}


def text(ref, lang):
    return TEXT[lang].get(str(ref['id']), '')


def names(ref):
    out = {lang: text(ref, lang) for lang in TEXT}
    assert all(out.values()), ref
    return out


def term(en):
    """A term by its English text: of the text ids that carry it, the one with the shortest
    Traditional Chinese text (Wuling is also the start of "Wuling Medal" and "Wuling region")."""
    ids = [k for k, v in TEXT['en'].items() if v == en]
    assert ids, en
    best = min(ids, key=lambda k: (len(TEXT['zh-TW'].get(k, '')), k))
    return {lang: TEXT[lang][best] for lang in TEXT}


OPS = {}
for path in glob.glob(os.path.join(ROOT, 'records', 'operators', '*.json')):
    rec = json.load(open(path, encoding='utf8'))
    OPS[rec['gameId']] = rec
WEAPONS = {w['id'] for w in json.load(open(os.path.join(ROOT, 'records', 'weapons.json'), encoding='utf8'))}
ATTR = {'str': 'str', 'agi': 'agi', 'wisd': 'int', 'will': 'will'}

# Room types: 3 and 5 are both the Reception Room in the text table.
ROOMS = {0: 'control', 1: 'manufacturing', 2: 'growth', 3: 'reception', 5: 'reception'}
ICON_KIND = {
    'facskill_spaceship_physical_power': 'mood-regen-all',
    'facskill_spaceship_manufacture_power_consume': 'mood-drop-room',
    'facskill_spaceship_plant_power_consume': 'mood-drop-room',
    'facskill_spaceship_guestroom_power_consume': 'mood-drop-room',
    'facskill_spaceship_plant_flower': 'grow-plant',
    'facskill_spaceship_plant_fungus': 'grow-fungus',
    'facskill_spaceship_plant_mineral': 'grow-mineral',
    'facskill_spaceship_guestroom_efficiency': 'clue-speed',
}


def kind_of(skill):
    icon, en = skill['icon'], text(skill['desc'], 'en')
    if icon == 'facskill_spaceship_manufacture_efficiency':
        return 'make-operator-exp' if 'operator EXP' in en else 'make-weapon-exp'
    if icon == 'facskill_spaceship_guestroom_clue':
        return 'clue-chance'
    return ICON_KIND[icon]


def main():
    rec_w = table('CharWpnRecommendTable')
    rec_s = table('CharWpnSkillRecommendTable')
    recommend = {'source': SOURCE, 'operators': {}}
    for gid, op in sorted(OPS.items(), key=lambda kv: kv[1]['slug']):
        row = rec_w[gid]
        weapons = row['weaponIds1'] + row['weaponIds2'] + row['weaponIds3']
        missing = [w for w in weapons if w not in WEAPONS]
        assert not missing, (gid, missing)
        attrs = []
        for sid in rec_s[gid]['weaponSkillIds']:
            a = ATTR[re.match(r'wpn_attr_(\w+?)_(low|mid|high)$', sid).group(1)]
            if a not in attrs:
                attrs.append(a)
        recommend['operators'][op['slug']] = {'weapons': weapons, 'attributes': attrs}

    char_skills = table('SpaceshipCharSkillTable')
    skills = table('SpaceshipSkillTable')
    rooms = table('SpaceshipRoomTypeTable')
    base = {'source': SOURCE, 'rooms': {}, 'operators': {}}
    for rtype, room in rooms.items():
        key = ROOMS[int(rtype)]
        base['rooms'].setdefault(key, names(room['name']))
    for gid, op in sorted(OPS.items(), key=lambda kv: kv[1]['slug']):
        if gid not in char_skills:
            continue
        out = []
        for entry in char_skills[gid]['skillList']:
            sk = skills[entry['skillId']]
            hint = text(entry['unlockHint'], 'en')
            m = re.fullmatch(r'Reach E(\d) to (?:unlock|activate)', hint)
            assert m, (gid, hint)
            values = [float(p['valueStringList'][0]) for p in sk['parameters']]
            level = {'mark': sk['skillNamePostfix'], 'promotion': int(m.group(1)), 'value': round(values[0], 4)}
            kind = kind_of(sk)
            if kind == 'clue-chance':
                clue = re.search(r'Clue (\d) Rate-UP: ([^(]+?) \(', text(sk['desc'], 'en'))
                zh = re.search(r'線索\d——(.+?)的機率', text(sk['desc'], 'zh-TW'))
                cn = re.search(r'线索\d——(.+?)的(?:概率|几率|机率)', text(sk['desc'], 'zh-CN'))
                assert clue and zh and cn, (gid, sk['id'])
                level['clue'] = {'number': int(clue.group(1)), 'en': clue.group(2), 'zh-TW': zh.group(1), 'zh-CN': cn.group(1)}
                level['small'] = ' a small ' in text(sk['desc'], 'en')
                del level['value']
            idx = entry['skillIndex']
            if len(out) <= idx:
                out.append({'name': names(sk['talentName']), 'room': ROOMS[sk['roomType']], 'kind': kind, 'levels': []})
            assert out[idx]['kind'] == kind and out[idx]['room'] == ROOMS[sk['roomType']], (gid, sk['id'])
            out[idx]['levels'].append(level)
        base['operators'][op['slug']] = out

    # Essence stats per weapon: each 4- to 6-star weapon has one combination of an
    # attribute stat, a secondary stat and a skill stat (GemTagKeyToWeaponTable).
    gems = table('GemTable')
    kinds = {0: 'attribute', 1: 'secondary', 2: 'skill'}
    essence = {'source': SOURCE, 'stats': {}, 'weapons': {}}
    for g in sorted(gems.values(), key=lambda g: (g['termType'], g['sortOrder'])):
        essence['stats'][g['tagId']] = {'kind': kinds[g['termType']], 'name': names(g['tagName'])}
    for key, row in table('GemTagKeyToWeaponTable').items():
        tags = sorted(key.split('+'), key=lambda t: list(essence['stats']).index(t))
        assert [essence['stats'][t]['kind'] for t in tags] == ['attribute', 'secondary', 'skill'], key
        for wid in row['list']:
            assert wid not in essence['weapons'], wid
            essence['weapons'][wid] = tags

    # Recipes of the AIC production facilities. Recipes whose id or items hold "activity" use items
    # that the game describes as made "during a special period" (event items): left out.
    items_t = table('ItemTable')
    facilities = {f['id'] for f in json.load(open(os.path.join(ROOT, 'records', 'facilities.json'), encoding='utf8'))}
    recipes = {'source': SOURCE, 'items': {}, 'recipes': []}
    for rid, r in sorted(table('FactoryMachineCraftTable').items(), key=lambda kv: (kv[1]['machineId'], kv[1]['sortId'])):
        touched = [x['id'] for g in r['ingredients'] + r['outcomes'] for x in g['group']]
        if 'activity' in rid or any('activity' in i for i in touched):
            continue
        assert r['machineId'] in facilities, (rid, r['machineId'])
        # One ingredient group (all of it is used); one or two outcome groups (a second one is
        # a by-product such as Sewage, on eight recipes).
        assert len(r['ingredients']) == 1 and 1 <= len(r['outcomes']) <= 2, rid
        ins = [{'id': x['id'], 'count': x['count']} for x in r['ingredients'][0]['group']]
        outs = [{'id': x['id'], 'count': x['count']} for g in r['outcomes'] for x in g['group']]
        for x in ins + outs:
            recipes['items'].setdefault(x['id'], names(items_t[x['id']]['name']))
        recipes['recipes'].append({'id': rid, 'machine': r['machineId'], 'inputs': ins, 'outputs': outs, 'seconds': r['progressRound']})

    # Enemies of the in-game encyclopedia (WikiEntryTable entries wiki_<template id>): class,
    # where they are found, and the resistances of the base enemy (enemy id = template id).
    # Stage versions of an enemy (ids with a suffix, such as _hdg025) can have other values.
    wiki = {x[len('wiki_'):] for v in table('WikiEntryTable').values() for x in v['list'] if x.startswith('wiki_eny_')}
    enemy_t, attr_t, dist_t = table('EnemyTable'), table('EnemyAttributeTemplateTable'), table('DistributionInfoTable')
    resist_keys = {'physical': 'physicalResistance', 'heat': 'fireResistance', 'electric': 'pulseResistance',
                   'cryo': 'crystResistance', 'nature': 'naturalResistance'}
    enemies = {'source': SOURCE, 'classes': {k: names(v['name']) for k, v in table('DisplayEnemyTypeTable').items()},
               'areas': {}, 'enemies': []}
    for tid, d in table('EnemyTemplateDisplayInfoTable').items():
        if tid not in wiki:
            continue
        a = attr_t[enemy_t[tid]['attrTemplateId']]
        # No enemy in the encyclopedia has an Aether resistance other than 0 (attribute 99).
        assert all(x['attrValue'] == 0 for x in a['levelIndependentAttributes']['attrs'] if x['attrType'] == 99), tid
        areas = [x for x in d['distributionIds'] if x in dist_t]
        for x in areas:
            enemies['areas'].setdefault(x, names(dist_t[x]['areaName']))
        enemies['enemies'].append({'id': tid, 'name': names(d['name']), 'class': str(d['displayType']),
                                   'resist': {k: int(a[f]) if a[f] == int(a[f]) else a[f] for k, f in resist_keys.items()},
                                   'areas': areas})
    assert len(enemies['enemies']) == len(wiki), (len(enemies['enemies']), len(wiki))
    # The game shows a resistance as a grade: the grade with the smallest damage-taken scalar that
    # is not below 1 - resistance / 100 (checked on the official wiki, 2026-11-22: 0 is D,
    # 20, 30, 35 and 40 are C, 50 and 60 are B).
    enemies['grades'] = sorted(({'grade': v['name'] and names(v['name'])['en'], 'taken': v['damageTakenScalar']}
                                for v in table('EnemyDamageTakenLevelTable').values()), key=lambda g: g['taken'])
    enemies['terms'] = {k: term(en) for k, en in (('physical', 'Physical Resistance'), ('heat', 'Heat Resistance'), ('electric', 'Electric Resistance'),
                                                   ('cryo', 'Cryo Resistance'), ('nature', 'Nature Resistance'), ('map01', 'Valley IV'), ('map02', 'Wuling'))}

    for name, data in (('recommend.json', recommend), ('base-skills.json', base), ('weapon-essence.json', essence), ('recipes.json', recipes), ('enemies.json', enemies)):
        with open(os.path.join(ROOT, 'records', name), 'w', encoding='utf8') as f:
            json.dump(data, f, ensure_ascii=False, indent=1)
            f.write('\n')
    print(len(recommend['operators']), 'operators with recommendations;', len(base['operators']), 'with base skills')


if __name__ == '__main__':
    main()
