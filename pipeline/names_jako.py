"""Write records/names-jako.json: the game's Japanese and Korean text for the names in
records/ and for the game terms the page scripts use.

Usage: python3 -I pipeline/names_jako.py
Reads records/ and the cache: the game's text tables (cache/third/ed/<commit>/
I18nTextTable_{EN,TC,JP,KR}.json, {id: text}, one id across languages) and the ja-jp and
ko-kr official notices of the version update notes (cache/official/art/<lang>-<cid>.json).

- names: every {en, zh-TW} pair in records/ that carries no ja and ko of its own (records
  written by ed_extract.py carry them), found by the pair (English text, Traditional Chinese
  text) in the tables. Where the ids of a pair give several Japanese or Korean texts, the
  context rules in SEVERAL decide. Prose in changes.json and obtain.json is not a name: those
  records carry their own ja and ko fields.
- Version titles are not in the tables: they come from the 「」 in the title of the ja-jp and
  ko-kr notice with the same id as the English update notes.
- Faction names in base-skill clue names (UWST, TGCC, HAS) are abbreviations in English
  only; they are found by their Traditional Chinese text alone.
- terms: game terms by their exact English text (as term() in ed_extract.py), optionally
  narrowed by the Traditional Chinese text the zh-tw pages use.
Ruby markup of the Japanese text (<p="reading" padding=0>X</p>) is reduced to X.
"""
import collections
import glob
import json
import os
import re
import sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
COMMIT = '887923b9e56e132f2570a25e8c2cf5e971508736'
ED = os.path.join(ROOT, 'cache', 'third', 'ed', COMMIT)
LANGS = {'en': 'EN', 'zh-TW': 'TC', 'ja': 'JP', 'ko': 'KR'}
RUBY = re.compile(r'<p="[^"]*" padding=0>(.*?)</p>')


def plain(s):
    s = RUBY.sub(r'\1', s or '')
    assert '<' not in s, s
    return s


TEXT = {lang: json.load(open(os.path.join(ED, f'I18nTextTable_{code}.json'), encoding='utf8')) for lang, code in LANGS.items()}
BY_PAIR = collections.defaultdict(list)
BY_EN = collections.defaultdict(list)
BY_ZH = collections.defaultdict(list)
for _id, _en in TEXT['en'].items():
    _zh = RUBY.sub(r'\1', TEXT['zh-TW'].get(_id, ''))
    BY_EN[_en].append(_id)
    BY_PAIR[(_en, _zh)].append(_id)
    BY_ZH[_zh].append(_id)


def variants(ids, lang):
    out = collections.Counter()
    for i in ids:
        try:
            out[plain(TEXT[lang].get(i, ''))] += 1
        except AssertionError:
            continue
    out.pop('', None)
    return out


def pick(ids, lang):
    """The text most ids give; ties go to the shorter text."""
    c = variants(ids, lang)
    if not c:
        return None
    return sorted(c.items(), key=lambda kv: (-kv[1], len(kv[0]), kv[0]))[0][0]


# Pairs whose ids give several Japanese or Korean texts (after ruby is removed), decided by
# the context of the record. Checked 2026-11-22; each reason is the evidence used.
SEVERAL = {
    ('Agility', '敏捷'): ('ja', '敏捷', 'attribute of an operator: two of the three ids give 敏捷, and the Essence stat Agility is 敏捷UP'),
    ('SP Recovery', '技力回復'): ('ja', 'SP回復量', 'skill value name: 36 of the 37 ids, all skill value rows, give SP回復量; the other is SP回復'),
    ('SP Return', '返還技力'): ('ja', 'SP返還量', 'skill value name: 60 of the 63 ids give SP返還量; three give 戦技ポイント（SP）の返還'),
    ('Endfield Industries', '終末地工業'): ('ja', 'エンドフィールド工業', 'faction: 64 of the 71 ids in game data 1.7 give エンドフィールド工業; seven give エンドフィールド'),
    ('Cooldown', '冷卻'): ('ja', 'クールダウン', "Xaihi's basic attack is named Cooldown: one id gives クールダウン, one クールタイム; "
                       'クールタイム is also the UI label for a cooldown time (冷卻時間), so the skill name takes the other form'),
}

# Game terms the page scripts use, by exact English text; the value narrows the ids to those
# whose Traditional Chinese text is the one the zh-tw pages use (None: all ids).
TERMS = {
    'Basic Attack': None, 'Battle Skill': None, 'Combo Skill': None, 'Ultimate': None,
    'SP Cost': None, 'Ultimate Energy Cost': None, 'Cooldown': '冷卻時間',
    'Promotion I': '精英化I', 'Promotion II': None, 'Promotion III': None, 'Promotion IV': None,
    'Strength': '力量', 'Agility': '敏捷', 'Intellect': '智識', 'Will': '意志', 'ATK': '攻擊力', 'HP': '生命值',
    'Main Attribute': '主能力', 'Secondary Attribute': '副能力',
    'Rarity': '稀有度', 'Class': None, 'Element': None, 'Weapon': '武器', 'Faction': '陣營', 'Race': None,
    'Skills': None, 'Talent': '天賦', 'Potential': '潛能', 'Base Skill': None, 'Operators': None,
    'Chartered Headhunting': None, 'Special Headhunting': None, 'RE-Factor Headhunting': None,
    'Basic Headhunting': None, 'Headhunting': '尋訪',
    'Essence': '基質', 'Weapon Skill': None, 'Arsenal Ticket': None, 'Arsenal Issue': '武庫申領', 'Arsenal Exchange': None,
    'Dijiang': '帝江號', 'Central Ring': None, 'MFG Plan': None, 'MFG Load': None, 'Clue Exchange': None,
    'Recycling Station': '資源回收站', 'Mood': None, 'Trust': '信賴值', 'Credits': None,
    'Production Assist': None, 'Control Nexus': None, 'Reception Room': None, 'Shift A': None, 'Shift B': None,
    'Endministrator': None, 'Endfield Industries': None, 'Talos-II': None, 'Rhodes Island': None,
    'Weapon Tuning': '武器突破', 'Rare Mineral': None, 'EXP': None, 'Drinks': None,
    'Physical': None, 'Heat': None, 'Electric': None, 'Cryo': None, 'Nature': None,
    'Energy Alluvium': '能量淤積點', 'Valley IV': None, 'Wuling': '武陵',
    'Filling Unit': None, 'Separating Unit': None, 'Stagger': '失衡值', 'Finisher': None,
    'Gear': None, 'Blueprint': None, 'Combat': '戰鬥',
    'Protocol Automation-Core': None, 'Core AIC Area': None, 'Sub-PAC': None, 'AIC Steward': None,
    'AIC Factory Plan': '工業發展規劃', 'Electric Pylon': None, 'Regional Development': None, 'Regional Transfer': None,
    'Outpost': None, 'Stock Bill': None, 'Depot Node': None, 'Regional Development Level': None, 'Depot': '倉庫',
    'Backpack': '背包', 'TP Point': None, 'Protocol Management': None, 'Thermal Bank': None, 'Depot Bus': None,
    'Protocol Capacity': None, 'Arts Infliction': None, 'Arts Burst': None, 'Physical Status': None, 'Coolant Gel': '冷卻脂',
    'Logistics Units': None, 'Combat & Support': None, 'Ornamental': None, 'Planting': '種植調配', 'Resourcing': '資源開採',
    'Depot Access': None, 'Production I': None, 'Production II': None, 'Power': '電力', 'Miscellaneous': None,
    'Auto-Farmer': '自動農植機', 'Backup Power': None, 'Regional Overview': None, 'Continue Placing': None,
    "Si's Painting": None, 'Wuling City': '武陵城',
    'UP': '機率提升', 'Cabin': None, 'Clues': None, 'Assign': '進駐', 'Unlock': '解鎖', 'Recommended': '推薦',
    'Essence Stats': None, 'Æther Resistance': None, 'AIC': '集成工業', 'Aerospace Material': '航太建材', 'Enemies': None, 'Facility': '設備', 'Weapon Type': None,
}
# Where the ids of a term disagree in a way the Traditional Chinese text cannot settle.
TERM_FIX = {
    ('Rarity', 'ja'): ('レア度', 'the id with 稀有度 gives レア度順 and the id with 按稀有度 gives レア度: the two texts are swapped in JP'),
}


def walk(o, path, out):
    if isinstance(o, dict):
        if isinstance(o.get('en'), str) and isinstance(o.get('zh-TW'), str):
            out.append((path, o))
        for k, v in o.items():
            walk(v, f'{path}/{k}', out)
    elif isinstance(o, list):
        for i, v in enumerate(o):
            walk(v, f'{path}[{i}]', out)


def notice_title(lang, cid):
    path = os.path.join(ROOT, 'cache', 'official', 'art', f'{lang}-{cid}.json')
    title = json.load(open(path, encoding='utf8'))['data']['title']
    m = re.match(r'\s*「([^」]+)」', title)
    assert m, (path, title)
    return m.group(1)


def main():
    found = []
    for f in sorted(glob.glob(os.path.join(ROOT, 'records', '**', '*.json'), recursive=True)):
        rel = os.path.relpath(f, os.path.join(ROOT, 'records'))
        if rel.startswith('text' + os.sep) or rel in ('names-jako.json', 'names-voc.json', 'pending.json'):
            continue
        data = json.load(open(f, encoding='utf8'))
        hits = []
        walk(data, rel, hits)
        found += hits
        # Voice actors: {en: {eng, jap, ...}, zh-TW: {...}} per operator.
        if rel.startswith('operators' + os.sep):
            for key, en in data['voice']['en'].items():
                found.append((f'{rel}/voice/{key}', {'en': en, 'zh-TW': data['voice']['zh-TW'][key]}))
    versions = json.load(open(os.path.join(ROOT, 'records', 'versions.json'), encoding='utf8'))
    titles = {(v['title']['en'], v['title']['zh-TW']): v['notes'] for v in versions if v['title']}

    names, seen, counts, report = [], set(), collections.Counter(), []
    for path, o in found:
        pair = (o['en'], o['zh-TW'])
        if path.startswith(('changes.json', 'obtain.json')) and not path.endswith('/event'):
            if not (o.get('ja') and o.get('ko')):
                sys.exit(f'{path}: prose without ja and ko fields; write them (translated from English, game names from the tables)')
            counts['prose'] += 1
            continue
        if 'ja' in o and 'ko' in o:
            continue
        if pair in seen:
            continue
        seen.add(pair)
        entry = {'en': pair[0], 'zh-TW': pair[1]}
        if pair in titles:
            cid = titles[pair]
            entry.update(ja=notice_title('ja-jp', cid), ko=notice_title('ko-kr', cid), source=f'notice {cid}')
            counts['notice'] += 1
        elif pair in BY_PAIR:
            ids = BY_PAIR[pair]
            for lang in ('ja', 'ko'):
                entry[lang] = pick(ids, lang)
                if len(variants(ids, lang)) > 1:
                    rule = SEVERAL.get(pair)
                    if not rule or rule[0] != lang:
                        sys.exit(f'several {lang} texts for {pair} at {path}: {dict(variants(ids, lang))}; add a rule to SEVERAL')
                    assert rule[1] in variants(ids, lang), (pair, rule)
                    entry[lang] = rule[1]
                    entry['source'] = f'tables, several ({dict(variants(ids, lang))}); {rule[2]}'
                    report.append(f'{pair[0]} ({pair[1]}): {lang} {rule[1]} of {dict(variants(ids, lang))}: {rule[2]}')
            entry.setdefault('source', 'tables')
            counts['several' if 'several' in entry['source'] else 'one'] += 1
        elif pair[1] in BY_ZH and re.fullmatch(r'[A-Z]{2,5}', pair[0]):
            ids = BY_ZH[pair[1]]
            for lang in ('ja', 'ko'):
                assert len(variants(ids, lang)) == 1, (pair, lang, variants(ids, lang))
                entry[lang] = pick(ids, lang)
            entry['source'] = 'tables, by the Traditional Chinese text (English abbreviation)'
            counts['abbreviation'] += 1
        else:
            sys.exit(f'not found: {pair} at {path}')
        names.append(entry)
    names.sort(key=lambda e: (e['en'].lower(), e['zh-TW']))

    terms = {}
    for en, zh in TERMS.items():
        ids = BY_EN[en] if zh is None else BY_PAIR.get((en, zh), [])
        assert ids, (en, zh)
        t = {'zh-TW': pick(ids, 'zh-TW')}
        for lang in ('ja', 'ko'):
            fix = TERM_FIX.get((en, lang))
            t[lang] = fix[0] if fix else pick(ids, lang)
            if fix:
                report.append(f'term {en}: {lang} {fix[0]}: {fix[1]}')
        terms[en] = t

    out = {'source': f'https://github.com/rmxlinux/EndfieldData/tree/{COMMIT}/TableCfg (I18nTextTable_EN, _TC, _JP, _KR); '
                     'version titles from the ja-jp and ko-kr update notes (web-news.gryphline.com, read 2026-11-22)',
           'names': names, 'terms': terms}
    with open(os.path.join(ROOT, 'records', 'names-jako.json'), 'w', encoding='utf8') as f:
        json.dump(out, f, ensure_ascii=False, indent=1)
        f.write('\n')
    for line in report:
        print(line)
    print(f"{len(names)} names ({counts['one']} one to one, {counts['several']} several, {counts['notice']} from notices, "
          f"{counts['abbreviation']} abbreviations); {counts['prose']} prose fields (changes.json, obtain.json) carry their own ja and ko; {len(terms)} terms")


if __name__ == '__main__':
    main()
