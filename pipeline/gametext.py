"""The game's own text of operators and gear sets, and how pages show it.

Usage: python3 -I pipeline/gametext.py
Reads cache/third/ed/<commit>/ (tables of github.com/rmxlinux/EndfieldData at that commit:
CharGrowthTable, PotentialTalentEffectTable, CharacterPotentialTable, SkillPatchTable,
EquipSuitTable and the five text tables), cache/official/operators.json (the operator
introductions of the official site, in its five editions) and cache/third/wf/ (the
rendered game text of warfarin.wiki, English, Traditional and Simplified Chinese).
Writes records/gametext/<slug>.json and the `effect` field of records/gear-sets.json.

The text is shown as the game gives it, in each language's edition, never reworded
(owner decision, 2026-11-23, for story text; 2026-11-24 for every text of the game's own
expression). Only the game's markup is removed: style tags, term links and Japanese ruby
(its base text is kept). A description template carries placeholders such as
`{atk_scale:0%}`. Their values are read by matching the English template against the
English text warfarin.wiki renders from the same game data; the values then fill the
template of every language, and the Traditional and Simplified Chinese results must equal
warfarin.wiki's text in those languages, or the script stops. The lines of a skill that
show the operator's current attributes (`/* ... */`, filled at run time) are left out.

The functions esc, quoted and inline turn game text into Markdown; build_pages.py,
scripts/to-zh-cn.py and the checks use them, so the text is written one way everywhere.
"""
import glob
import json
import os
import re

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
COMMIT = 'd847759f71d4549aba4727b3b0ac1a1ad0e37742'
ED = os.path.join(ROOT, 'cache', 'third', 'ed', COMMIT)
WF = os.path.join(ROOT, 'cache', 'third', 'wf')
OUT = os.path.join(ROOT, 'records', 'gametext')
LANGS = {'en': 'EN', 'zh-TW': 'TC', 'zh-CN': 'CN', 'ja': 'JP', 'ko': 'KR'}
WF_LANG = {'en': 'en', 'zh-TW': 'tc', 'zh-CN': 'cn'}
SOURCE = f'https://github.com/rmxlinux/EndfieldData/tree/{COMMIT}/TableCfg'
DIFFER = []  # texts whose Chinese differs from warfarin.wiki's; printed, for a reader to check
KINDS = {0: 'basic', 1: 'battle', 2: 'ultimate', 3: 'combo'}

RUBY = re.compile(r'<p="[^"]*" padding=0>(.*?)</p>')
TAG = re.compile(r'</?(?:color|size|b|i|u)(?:=[^>]*)?>|<[@#][\w.]+>|</>')
STATE = re.compile(r'/\*.*?\*/', re.S)
HOLE = re.compile(r'\{[^{}]*\}')


def clean(s):
    """Game text without its markup; line breaks kept, spaces at line ends dropped."""
    s = RUBY.sub(r'\1', s)
    s = TAG.sub('', s)
    s = s.replace('\r\n', '\n')
    return '\n'.join(line.rstrip() for line in s.split('\n')).strip()


def esc(s):
    """Markdown escaping of game text: the characters Markdown would read as markup."""
    for ch in '\\`*_[]<>|':
        s = s.replace(ch, '\\' + ch)
    out = []
    for line in s.split('\n'):
        if line[:1] in '#+-=' or (line[:1].isdigit() and line.lstrip('0123456789')[:1] in '.)'):
            line = '\\' + line
        out.append(line)
    return '\n'.join(out)


def quoted(s):
    """Game text as a block quote, its line breaks kept."""
    out = []
    for para in re.split(r'\n\s*\n', s):
        lines = esc(para).split('\n')
        out.append('\n'.join('> ' + x + ('\\' if k < len(lines) - 1 and x else '') for k, x in enumerate(lines)))
    return '\n>\n'.join(out)


def inline(s):
    """Game text on one line (a table cell): line breaks become spaces."""
    return ' '.join(x for x in esc(s).split('\n') if x)


def lines_of(s):
    """The lines of a game text, as a check looks for them in a page."""
    return [x for x in (y.strip() for y in s.split('\n')) if x]


def page_texts(rel):
    """The game texts a page shows, as (texts by language, 'quoted' or 'inline'): what
    build_pages.py writes, what scripts/to-zh-cn.py swaps for the game's Simplified
    Chinese, and what the checks look for. rel is the page path below the language
    folder, such as operators/arcane.md or systems/gear.md."""
    out = []
    m = re.fullmatch(r'operators/([a-z-]+)\.md', rel)
    if m and m.group(1) != 'index':
        g = json.load(open(os.path.join(OUT, m.group(1) + '.json'), encoding='utf8'))
        out.append((g['intro'], 'quoted'))
        for s in g['skills']:
            out += [(t, 'quoted') for t in [s['text']] + [c['text'] for c in s['conditions']] if t]
        out += [(lv['text'], 'quoted') for t in g['talents'] for lv in t['levels']]
        out += [(p['text'], 'inline') for p in g['potentials']]
        base = json.load(open(os.path.join(ROOT, 'records', 'base-skills.json'), encoding='utf8'))
        out += [(lv['text'], 'inline') for sk in base['operators'].get(m.group(1), []) for lv in sk['levels']]
    if rel == 'systems/gear.md':
        out += [(s['effect'], 'inline') for s in json.load(open(os.path.join(ROOT, 'records', 'gear-sets.json'), encoding='utf8'))]
    return out


def table(name):
    return json.load(open(os.path.join(ED, name + '.json'), encoding='utf8'))


def norm(s):
    """Text compared with warfarin.wiki: markup gone, all runs of white space one space."""
    return re.sub(r'\s+', ' ', clean(s)).strip()


class Filler:
    """Placeholder values of one text, read from the matching text that warfarin.wiki
    renders: the same skill, talent level or potential, in English, Traditional and
    Simplified Chinese."""

    def __init__(self, rendered):
        self.rendered = rendered  # {lang: normalised rendered text}
        self.values = {}

    def learn(self, template_en, where):
        self.values = {}
        t = norm(STATE.sub('', template_en))
        holes = HOLE.findall(t)
        if not holes:
            return
        parts = HOLE.split(t)
        pattern = '(.+?)'.join(re.escape(p) for p in parts).replace(r'\ ', r'\s*')
        text = self.rendered['en']
        # The whole text (a talent, a potential), or a run of whole lines inside it (a part
        # of a skill, which warfarin.wiki joins into one text).
        m = re.fullmatch(pattern, text) or re.search(r'(?:^|(?<=\s))' + pattern + r'(?=\s|$)', text)
        assert m, f'{where}: the rendered English text does not match {t!r}'
        for h, v in zip(holes, m.groups()):
            old = self.values.setdefault(h, v.strip())
            assert old == v.strip(), (where, h, old, v)

    def fill(self, template, where):
        s = clean(STATE.sub('', template))

        def one(m):
            assert m.group(0) in self.values, (where, m.group(0))
            return self.values[m.group(0)]
        return HOLE.sub(one, s).strip()


def unit(T, ref, filler, where, required=True):
    """One text of the game in every language, placeholders filled."""
    if not ref or not ref.get('id'):
        return None
    raw = {lang: T[lang].get(str(ref['id']), '') for lang in LANGS}
    if not any(raw.values()):
        assert not required, where
        return None
    missing = [lang for lang, v in raw.items() if not v]
    assert not missing, (where, missing)
    if filler:
        filler.learn(raw['en'], where)
        out = {lang: filler.fill(v, where) for lang, v in raw.items()}
        for lang in ('zh-TW', 'zh-CN'):
            if lang not in filler.rendered:
                continue
            got = norm(out[lang])
            if got not in filler.rendered[lang]:
                DIFFER.append((where, lang, got))
    else:
        out = {lang: clean(v) for lang, v in raw.items()}
    for lang, v in out.items():
        assert '{' not in v and '/*' not in v and '<' not in v, (where, lang, v)
    return out


def intro_of(official, key):
    out = {}
    for lang, edition in (('en', 'en'), ('zh-TW', 'zh-TW'), ('zh-CN', 'zh-CN'), ('ja', 'ja'), ('ko', 'ko')):
        o = official[edition]
        t = o['text'].get(f'operator.content.{key}.intro', '')
        if not t:
            t = next((r.get('intro', '') for r in o['roster'] or [] if r.get('key') == key), '')
        assert t, (key, lang)
        out[lang] = '\n'.join(line.strip() for line in t.replace('\r\n', '\n').split('\n')).strip()
    return out


def rendered_of(slug):
    """warfarin.wiki's rendered text of an operator: {lang: {'skills': {kind: text},
    'talents': [[text per level]], 'potentials': [text]}}, normalised."""
    wf = {'mi-fu': 'mifu'}.get(slug, slug)
    out = {}
    for lang, code in WF_LANG.items():
        d = json.load(open(os.path.join(WF, 'json', f'{code}-{wf}.json'), encoding='utf8'))
        out[lang] = {'skills': {s['kind']: norm(s['desc']) for s in d['skills']},
                     'talents': [[norm(lv['desc']) for lv in t['levels']] for t in d['talents']],
                     'potentials': [norm(p['desc']) for p in d['potentials']]}
    return out


def pick(rendered, *path):
    out = {}
    for lang, r in rendered.items():
        for k in path:
            r = r[k]
        out[lang] = r
    return Filler(out)


def operator(gid, slug, key, T, growth, effects, potentials, official):
    # The two Endministrator characters (chr_0002, chr_0003) carry stub skills and talents
    # with empty values; the ones the game shows, and that the potentials refer to, are the
    # shared entry chr_9000_endmin.
    g = growth['chr_9000_endmin' if re.match(r'chr_000[23]_endmin', gid) else gid]
    rendered = rendered_of(slug)
    out = {'slug': slug, 'gameId': gid, 'source': SOURCE, 'intro': intro_of(official, key), 'skills': [], 'talents': [], 'potentials': []}
    for sg in sorted(g['skillGroupMap'].values(), key=lambda s: [0, 1, 3, 2].index(s['skillGroupType']) if s['skillGroupType'] < 4 else 9):
        if sg['skillGroupType'] not in KINDS:
            continue
        where = f"{slug} {sg['skillGroupId']}"
        filler = pick(rendered, 'skills', KINDS[sg['skillGroupType']])
        conditions = []
        for i in (1, 2):
            name = unit(T, sg[f'conditionName{i}'], None, where, required=False)
            text = unit(T, sg[f'conditionPostDesc{i}'], filler, where, required=False)
            if text:
                conditions.append({'name': name, 'text': text})
        out['skills'].append({'kind': KINDS[sg['skillGroupType']], 'name': unit(T, sg['name'], None, where),
                              'text': unit(T, sg['desc'], filler, where, required=False), 'conditions': conditions})
    nodes = sorted((n['passiveSkillNodeInfo'] for n in g['talentNodeMap'].values() if n['nodeType'] == 4), key=lambda p: (p['index'], p['level']))
    for p in nodes:
        where = f"{slug} {p['talentEffectId']}"
        if p['level'] == 1:
            out['talents'].append({'name': unit(T, p['name'], None, where), 'levels': []})
        filler = pick(rendered, 'talents', p['index'], p['level'] - 1)
        out['talents'][p['index']]['levels'].append({'promotion': p['breakStage'], 'text': unit(T, effects[p['talentEffectId']]['desc'], filler, where)})
    for b in potentials[gid]['potentialUnlockBundle']:
        where = f"{slug} {b['potentialEffectId']}"
        filler = pick(rendered, 'potentials', b['level'] - 1)
        out['potentials'].append({'level': b['level'], 'name': unit(T, b['name'], None, where),
                                  'text': unit(T, effects[b['potentialEffectId']]['desc'], filler, where)})
    return out


def gear_sets(T):
    """The 3-piece effect of each gear set (the description of its skill), its values read
    from warfarin.wiki's English text and checked against its Traditional Chinese."""
    path = os.path.join(ROOT, 'records', 'gear-sets.json')
    sets = json.load(open(path, encoding='utf8'))
    suits = table('EquipSuitTable')
    patches = table('SkillPatchTable')
    wf = {s['id']: s for s in json.load(open(os.path.join(WF, 'gear-sets.json'), encoding='utf8'))}
    for s in sets:
        (entry,) = suits[s['id']]['list']
        (patch,) = patches[entry['skillID']]['SkillPatchDataBundle']
        filler = Filler({lang: norm(v) for lang, v in wf[s['id']]['effect'].items()})
        s['effect'] = unit(T, patch['description'], filler, s['id'])
    open(path, 'w', encoding='utf8').write(json.dumps(sets, ensure_ascii=False, indent=1) + '\n')
    return len(sets)


def main():
    T = {lang: table('I18nTextTable_' + code) for lang, code in LANGS.items()}
    growth, effects, potentials = table('CharGrowthTable'), table('PotentialTalentEffectTable'), table('CharacterPotentialTable')
    official = json.load(open(os.path.join(ROOT, 'cache', 'official', 'operators.json'), encoding='utf8'))
    os.makedirs(OUT, exist_ok=True)
    n = 0
    for path in sorted(glob.glob(os.path.join(ROOT, 'records', 'operators', '*.json'))):
        op = json.load(open(path, encoding='utf8'))
        rec = operator(op['gameId'], op['slug'], op['officialKey'], T, growth, effects, potentials, official)
        open(os.path.join(OUT, op['slug'] + '.json'), 'w', encoding='utf8').write(json.dumps(rec, ensure_ascii=False, indent=1) + '\n')
        n += 1
    print(n, 'operators;', gear_sets(T), 'gear sets')
    for d in DIFFER:
        print('differs from warfarin.wiki:', *d)


if __name__ == '__main__':
    main()
