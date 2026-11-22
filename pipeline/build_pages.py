"""Write the pages that come from records: one page per operator, in English and
Traditional Chinese.

Usage: python3 -I pipeline/build_pages.py
Reads records/ only (no cache, no network) and writes
src/content/docs/operators/<slug>.md and src/content/docs/zh-tw/operators/<slug>.md.
Run scripts/to-zh-cn.py afterwards for the Simplified Chinese pages.
Do not edit the pages it writes: change the record or this script.
"""
import glob
import json
import os

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DOCS = os.path.join(ROOT, 'src', 'content', 'docs')
TODAY = '2026-11-22'
EN, ZH = 'en', 'zh-TW'
ROMAN = {1: 'I', 2: 'II', 3: 'III', 4: 'IV'}


def load(name):
    return json.load(open(os.path.join(ROOT, 'records', name), encoding='utf8'))


BANNERS = load('banners.json')
VERSIONS = {v['number']: v for v in load('versions.json')}
OBTAIN = load('obtain.json')
CHANGES = load('changes.json')
OPS = {}
for _path in sorted(glob.glob(os.path.join(ROOT, 'records', 'operators', '*.json'))):
    _rec = json.load(open(_path, encoding='utf8'))
    _rec['text'] = json.load(open(os.path.join(ROOT, 'records', 'text', _rec['slug'] + '.json'), encoding='utf8'))
    OPS[_rec['slug']] = _rec

ALL = BANNERS['banners']
CHARTERED = [b for b in ALL if b['type'] == 'chartered']
STANDARD6 = BANNERS['standardSixStars']
TYPE = {
    'chartered': {EN: 'Chartered Headhunting', ZH: '特許尋訪'},
    'special': {EN: 'Special Headhunting', ZH: '特殊尋訪'},
    'refactor': {EN: 'RE-Factor Headhunting #1', ZH: '重構尋訪#1'},
}
WEAPON_EN = {'Sword': 'a sword', 'Greatsword': 'a greatsword', 'Polearm': 'a polearm',
             'Handcannon': 'a handcannon', 'Arts Unit': 'an Arts Unit'}
SLOT = {
    'basic': {EN: 'Basic attack', ZH: '普通攻擊'},
    'battle': {EN: 'Battle skill', ZH: '戰技'},
    'combo': {EN: 'Combo skill', ZH: '連攜技'},
    'ultimate': {EN: 'Ultimate', ZH: '終結技'},
}


RECOMMEND = load('recommend.json')
BASE = load('base-skills.json')
ESSENCE = load('weapon-essence.json')
WEAPON = {w['id']: w for w in load('weapons.json')}
GAME_TABLES = (RECOMMEND['source'], {EN: 'rmxlinux/EndfieldData, game tables (1.6, 2026-11-05)', ZH: 'rmxlinux/EndfieldData 遊戲資料表（1.6，2026-11-05）'})
ATTR_KEY = {'Strength': 'str', 'Agility': 'agi', 'Intellect': 'int', 'Will': 'will'}
BASE_EFFECT = {
    'mood-regen-all': {EN: 'Mood recovery of all operators +{v}', ZH: '所有幹員心情恢復 +{v}'},
    'mood-drop-room': {EN: 'Mood drop of the operators in this room −{v}', ZH: '本艙室幹員心情消耗 −{v}'},
    'make-operator-exp': {EN: 'Operator EXP materials made {v} faster', ZH: '幹員經驗材料生產效率 +{v}'},
    'make-weapon-exp': {EN: 'Weapon EXP materials made {v} faster', ZH: '武器經驗材料生產效率 +{v}'},
    'grow-plant': {EN: 'Vitrified plants grow {v} faster', ZH: '晶植材料培養速度 +{v}'},
    'grow-fungus': {EN: 'Fungal matter grows {v} faster', ZH: '菌類材料培養速度 +{v}'},
    'grow-mineral': {EN: 'Rare minerals grow {v} faster', ZH: '礦物材料培養速度 +{v}'},
    'clue-speed': {EN: 'Clues collected {v} faster', ZH: '線索收集效率 +{v}'},
}


def percent(v):
    return f"{round(v * 100, 2):g}%"


def base_effect(skill, level, lang):
    if skill['kind'] == 'clue-chance':
        c = level['clue']
        if lang == EN:
            more = 'Slightly higher' if level['small'] else 'Higher'
            return f"{more} chance of Clue {c['number']} ({c['en']}); does not stack with another skill of this kind"
        more = '小幅提升' if level['small'] else '提升'
        return f"線索{c['number']}（{c['zh-TW']}）的機率{more}；同類效果不疊加"
    return BASE_EFFECT[skill['kind']][lang].format(v=percent(level['value']))


def recommended(op, lang):
    rec = RECOMMEND['operators'][op['slug']]
    sep = ', ' if lang == EN else '、'
    rows = []
    for wid in rec['weapons']:
        w = WEAPON[wid]
        stats = sep.join(ESSENCE['stats'][t]['name'][lang] for t in ESSENCE['weapons'][wid])
        rows.append(f"| {w['name'][lang]} | {w['rarity']} | {stats} |")
    keys = [ATTR_KEY[op['mainAttr'][EN]], ATTR_KEY[op['subAttr'][EN]]]
    assert keys == rec['attributes'], op['slug']
    return rows


LATEST = max(VERSIONS, key=lambda v: [int(x) for x in v.split('.')])


def name(slug, lang):
    return OPS[slug]['name'][lang]


def bname(b, lang):
    return b['name'][EN] if lang == EN else f"「{b['name'][ZH]}」"


def point(p, lang):
    """A start or end of a banner, as a table cell. Times are server time; the home page says so once."""
    if p['kind'] == 'time':
        return p['at']
    v = LATEST if p['version'] == 'next' else p['version']
    if p['kind'] == 'release':
        if v == '1.0':
            return {EN: 'Release, 2026-01-22', ZH: '公測，2026-01-22'}[lang]
        return {EN: f"Version {v} update, {VERSIONS[v]['asia']}", ZH: f"{v} 版更新，{VERSIONS[v]['asia']}"}[lang]
    if p['version'] == 'next':
        return {EN: f'End of Version {v}', ZH: f'{v} 版結束'}[lang]
    return {EN: f"Version {v} update, {VERSIONS[v]['asia']}", ZH: f"{v} 版更新，{VERSIONS[v]['asia']}"}[lang]


def status(slug):
    """How the operator is obtained. Nothing here depends on the day the page is built."""
    if slug == OBTAIN['playerCharacter']:
        return {'kind': 'player'}
    if slug in OBTAIN['eventReward']:
        return {'kind': 'reward', **OBTAIN['eventReward'][slug]}
    mine = [b for b in ALL if slug in b['sixStars']]
    own = [b for b in CHARTERED if b['rateUp'] == slug]
    if not own:
        kind = 'standard6' if slug in STANDARD6 else 'standard'
        return {'kind': kind, 'starting': slug in OBTAIN['starting'], 'banners': [b for b in mine if b['type'] != 'chartered']}
    rerun = [b for b in ALL if b['type'] == 'refactor' and b['rateUp'] == slug]
    return {'kind': 'chartered', 'own': own[0], 'banners': mine, 'rerun': rerun}


def list_names(slugs, lang):
    names = [name(s, lang) for s in slugs]
    if lang == ZH:
        return '、'.join(names[:-1]) + '與' + names[-1] if len(names) > 1 else names[0]
    return ', '.join(names[:-1]) + ' and ' + names[-1] if len(names) > 1 else names[0]


def describe(op, st, lang):
    n = op['name'][lang]
    r, el, cl, w = op['rarity'], op['element'][lang], op['class'][lang], op['weapon'][lang]
    if st['kind'] == 'player':
        return {EN: f'The Endministrator, the player character, is a {r}-star {el} {cl} with {WEAPON_EN[op['weapon'][EN]]}.',
                ZH: f'{n}是玩家操作的主角，{r} 星{el}{cl}幹員，使用{w}。'}[lang]
    if st['kind'] == 'chartered':
        tail = {EN: f"limited, rate-up in {st['own']['name'][EN]}", ZH: f"限定幹員，於{bname(st['own'], ZH)}機率提升"}[lang]
    else:
        key = 'starting' if st.get('starting') else st['kind']
        tail = {
            'standard6': {EN: 'in the standard headhunting roster', ZH: '在常駐尋訪名單內'},
            'standard': {EN: 'in the standard headhunting roster', ZH: '在常駐尋訪名單內'},
            'starting': {EN: 'every account starts with this operator', ZH: '每個帳號開局就擁有'},
            'reward': {EN: 'given by a Version 1.5 event', ZH: '1.5 版活動贈送的幹員'},
        }[key][lang]
    out = {EN: f'{n} is a {r}-star {el} {cl} with {WEAPON_EN[op['weapon'][EN]]}; {tail}.', ZH: f'{n}是 {r} 星{el}{cl}幹員，使用{w}；{tail}。'}[lang]
    if len(out) > (110 if lang == EN else 70):
        out = {EN: f'{n} is a {r}-star {el} {cl} with {WEAPON_EN[op['weapon'][EN]]}; limited operator.', ZH: f'{n}是 {r} 星{el}{cl}幹員，使用{w}；限定幹員。'}[lang]
    return out


RULE = {EN: "A limited operator stays in the pool of the two Chartered Headhunting banners after its own, without rate-up, then leaves the pool; limited operators are never added to Basic Headhunting.",
        ZH: '限定幹員在自己那一期之後的 2 期特許尋訪仍在名單內，但沒有機率提升，之後移出名單；限定幹員不會加入基礎尋訪。'}


def caveat(op, st, lang):
    n = op['name'][lang]
    k = st['kind']
    if k == 'player':
        return {EN: 'The Endministrator is the player character and is in no headhunting pool. The official operator list shows two Endministrator entries for one operator.',
                ZH: f'{n}是玩家操作的主角，不在任何尋訪名單內。官方幹員列表的兩筆{n}是同一名幹員。'}[lang]
    if k == 'reward':
        return {EN: f"{n} is in no headhunting pool; {n} was given by the Version {st['version']} event {st['event'][EN]}.",
                ZH: f"{n}不在任何尋訪名單內，是 {st['version']} 版活動「{st['event'][ZH]}」贈送的幹員。"}[lang]
    if k == 'standard6':
        return {EN: f'{n} has never been the rate-up operator of a banner. {n} is one of five standard 6-star operators listed in every Chartered Headhunting pool.',
                ZH: f'{n}沒有當過機率提升幹員；{n}是 5 名常駐 6 星幹員之一，每一期特許尋訪的名單都有{n}。'}[lang]
    if k == 'standard':
        if st['starting']:
            return {EN: f'Every account has {n} from the start of the game; {n} is also in the standard headhunting roster.',
                    ZH: f'每個帳號從遊戲開始就擁有{n}；{n}也在常駐尋訪名單內。'}[lang]
        return {EN: f'{n} has no rate-up banner. {n} is in the standard roster that Basic Headhunting and every Chartered Headhunting pool draw from.',
                ZH: f'{n}沒有機率提升尋訪；{n}在常駐名單內，基礎尋訪與每一期特許尋訪都抽得到。'}[lang]
    out = RULE[lang]
    for b in st['rerun']:
        out += {EN: f" {n} returned as the rate-up operator of RE-Factor Headhunting {b['name'][EN]}.",
                ZH: f"{n}曾在重構尋訪{bname(b, ZH)}再次機率提升。"}[lang]
    return out


def banner_table(slug, banners, lang):
    head = {EN: '| Banner | Type | Place | Opens | Ends |', ZH: '| 尋訪 | 類型 | 位置 | 開放 | 結束 |'}[lang]
    rows = [head, '| --- | --- | --- | --- | --- |']
    for b in banners:
        if b['rateUp'] == slug:
            place = {EN: 'Rate-up', ZH: '機率提升'}[lang]
        elif b['type'] == 'special':
            place = {EN: 'One of four 6-star operators', ZH: '四名 6 星幹員之一'}[lang]
        else:
            place = {EN: 'In the pool', ZH: '在名單內'}[lang]
        rows.append(f"| {b['name'][lang]} | {TYPE[b['type']][lang]} | {place} | {point(b['opens'], lang)} | {point(b['closes'], lang)} |")
    return '\n'.join(rows)


def special_notes(slug, banners, lang):
    out = []
    n = name(slug, lang)
    for b in banners:
        if b['type'] == 'special':
            four = list_names(b['sixStars'], lang)
            out.append({EN: f"{b['name'][EN]} held only {four} as 6-star operators. Its guarantee count was separate from every other banner; 120 pulls on it gave a permit to choose one of the four.",
                        ZH: f"{bname(b, ZH)}的 6 星幹員只有{four}。它的保底計數與其他尋訪分開；在這個尋訪累計 120 次，可獲得一張從四人中任選一名的憑證。"}[lang])
        if b['type'] == 'refactor' and b['rateUp'] == slug:
            out.append({EN: f"RE-Factor Headhunting brings back an earlier rate-up operator. {b['name'][EN]} guarantees {n} within the first 120 pulls, once across all banners of that name, and its pull count carries over to the next banner of the same name.",
                        ZH: f"重構尋訪讓過去的機率提升幹員再次登場。{bname(b, ZH)}前 120 次尋訪必定獲得{n}，這項保底在所有同名重構尋訪中只生效 1 次，計數會繼承到下一次同名重構尋訪。"}[lang])
    return out


def obtain(op, st, lang):
    slug, n = op['slug'], op['name'][lang]
    k = st['kind']
    if k == 'player':
        return [{EN: 'The Endministrator is the player character: every account has the Endministrator from the start of the game, and no headhunting pool contains this operator. The official operator list shows two entries for this one operator, one for each appearance.',
                 ZH: f'{n}是玩家操作的主角，每個帳號從遊戲開始就擁有，不在任何尋訪名單內。官方幹員列表有兩筆{n}，是同一名幹員的兩種外觀。'}[lang]]
    if k == 'reward':
        ev, extra = st['event'][lang], st['with'][lang]
        start, end = st['opens']['at'], point(st['closes'], lang)
        return [{EN: f'{n} was given by {ev}, a giveaway event of Version {st["version"]} that ran from {start} to the {end}. Logging in and playing the game modes during the event gave {n}, {extra}.',
                 ZH: f'{n}由 {st["version"]} 版的饋贈活動「{ev}」贈送，活動時間為 {start} 至 {end}。活動期間登入並參與各類玩法，可領取{n}、{extra}。'}[lang]]
    if k in ('standard6', 'standard'):
        out = []
        if st['starting']:
            who = list_names(OBTAIN['starting'], lang)
            out.append({EN: f'Every account has {n} from the start of the game. The four starting operators are {who}.',
                        ZH: f'每個帳號從遊戲開始就擁有{n}。初始幹員共四名：{who}。'}[lang])
        if k == 'standard6':
            five = list_names(STANDARD6, lang)
            out.append({EN: f'{n} has no rate-up banner. Five standard 6-star operators are in the pool of Basic Headhunting and of every Chartered Headhunting banner: {five}.',
                        ZH: f'{n}沒有自己的機率提升尋訪。基礎尋訪與每一期特許尋訪的名單都有這 5 名常駐 6 星幹員：{five}。'}[lang])
        else:
            out.append({EN: f'{n} has no rate-up banner. {n} is in the standard roster, which Basic Headhunting and every Chartered Headhunting pool draw from.',
                        ZH: f'{n}沒有自己的機率提升尋訪。{n}在常駐名單內，基礎尋訪與每一期特許尋訪都抽得到。'}[lang])
        if st['banners']:
            out.append({EN: f'Banners other than Chartered Headhunting that listed {n}:', ZH: f'特許尋訪以外，名單內有{n}的尋訪：'}[lang])
            out.append(banner_table(slug, st['banners'], lang))
            out += special_notes(slug, st['banners'], lang)
        return out
    own = st['own']
    v = own['version']
    pre = '' if lang == EN else '/zh-tw'
    link = f"{pre}/versions/{v.replace('.', '-')}/"
    if v == '1.0':
        where = {EN: f"[Version 1.0]({link})", ZH: f"[1.0 版]({link})"}[lang]
    else:
        ver = VERSIONS[v]
        where = {EN: f"[Version {v}, {ver['title'][EN]}]({link})", ZH: f"[{v} 版「{ver['title'][ZH]}」]({link})"}[lang]
    out = [{EN: f"{n} is the rate-up 6-star operator of {own['name'][EN]}, a Chartered Headhunting banner of {where}. Banners with {n}:",
            ZH: f"{n}是{where}特許尋訪{bname(own, ZH)}的機率提升 6 星幹員。名單內有{n}的尋訪："}[lang],
           banner_table(slug, st['banners'], lang), RULE[lang]]
    return out + special_notes(slug, st['banners'], lang)


def skill_suffix(skill, lang):
    k = skill['kind']
    if k == 'battle' and skill['cost']:
        return {EN: f" Costs {skill['cost']} SP.", ZH: f"消耗 {skill['cost']} 點技力。"}[lang]
    if k == 'ultimate' and skill['cost']:
        return {EN: f" Costs {skill['cost']} Ultimate Energy.", ZH: f"消耗 {skill['cost']} 點終結技能量。"}[lang]
    if k == 'combo' and skill['cooldown'][0]:
        a, b = skill['cooldown']
        if a == b:
            return {EN: f' Cooldown {a} s.', ZH: f'冷卻 {a} 秒。'}[lang]
        return {EN: f' Cooldown {a} s, {b} s at the highest skill level.', ZH: f'冷卻 {a} 秒，技能等級最高時 {b} 秒。'}[lang]
    return ''


def closed_sentence(text, lang):
    text = text.strip()
    end = '。' if lang == ZH else '.'
    return text if text[-1] in '.。！!？?' else text + end


def unlock(promotions, lang):
    def stage(p):
        return {EN: f'Promotion {ROMAN[p]}', ZH: f'精英化{ROMAN[p]}'}[lang]
    first = {EN: 'Default', ZH: '預設'}[lang] if promotions[0] == 0 else stage(promotions[0])
    later = [stage(p) for p in promotions[1:]]
    if not later:
        return first
    if lang == ZH:
        return f"{first}；{'、'.join(later)} 時提升"
    return f"{first}; upgraded at {' and '.join(later)}"


def quote(value):
    return '"' + value.replace('\\', '\\\\').replace('"', '\\"') + '"'


def page(op, lang):
    slug = op['slug']
    st = status(slug)
    n = op['name'][lang]
    text = op['text']
    L = lambda en, zh: en if lang == EN else zh  # noqa: E731
    pre = '' if lang == EN else '/zh-tw'

    desc = describe(op, st, lang)
    limit = 110 if lang == EN else 70
    assert len(desc) <= limit, (slug, lang, len(desc), desc)

    # Sources and the date of the newest notice a page relies on.
    banners = st.get('banners') or []
    cited = list(banners)
    sources = [(L('Official operator list (Gryphline)', '官方幹員列表 (Gryphline)'), 'https://endfield.gryphline.com/en-us/operator')]
    dates = ['2026-01-22']
    for b in cited:
        title = L(f"{b['name'][EN]} {TYPE[b['type']][EN]}", f"{bname(b, ZH)}{TYPE[b['type']][ZH]}說明")
        sources.append((title, f"https://endfield.gryphline.com/en-us/news/{b['notice']}"))
        dates.append(b['noticeDate'])
    versions = {c['version'] for c in CHANGES.get(slug, [])} | ({st['version']} if st['kind'] == 'reward' else set())
    if st['kind'] == 'chartered' and st['own']['version'] != '1.0':
        versions.add(st['own']['version'])
    versions = sorted(versions)
    for v in versions:
        ver = VERSIONS[v]
        sources.append((L(f"{ver['title'][EN]} Version Update Notes", f"「{ver['title'][ZH]}」版本更新說明"),
                        f"https://endfield.gryphline.com/en-us/news/{ver['notes']}"))
        dates.append(ver['notesDate'])
    sources.append((L(f"warfarin.wiki, {op['name'][EN]} (game data {op['gameDataVersion']})", f"warfarin.wiki {n}頁（遊戲資料 {op['gameDataVersion']}）"), op['gameDataPage']))
    sources.append((GAME_TABLES[1][lang], GAME_TABLES[0]))
    sources.append((L(f"Endfield Talos Wiki, {op['name'][EN]}", f"Endfield Talos Wiki 的 {op['name'][EN]} 頁"),
                    'https://endfield.wiki.gg/wiki/' + op['name'][EN].replace(' ', '_')))

    aliases = [op['name'][x] for x in (EN, ZH, 'zh-CN') if op['name'][x] != n]
    aliases = list(dict.fromkeys(aliases))

    fm = ['---', f'title: {quote(n)}', f'description: {quote(desc)}',
          'appliesTo: ' + quote(L(f"Arknights: Endfield, global service, Version 1.6; skill texts and stats from game data {op['gameDataVersion']}",
                                  f"《明日方舟：終末地》國際版，1.6 版；技能文字與數值出自遊戲資料 {op['gameDataVersion']}")),
          f'caveat: {quote(caveat(op, st, lang))}', f'lastVerified: {TODAY}', f'effectiveDate: {max(dates)}', 'aliases:']
    fm += [f'  - {quote(a)}' for a in aliases]
    fm += ['art:', '  - title: ' + L('Operator list', '幹員列表'), '    url: https://endfield.gryphline.com/en-us/operator', 'sources:']
    for title, url in sources:
        fm += [f'  - title: {quote(title)}', f'    url: {url}']
    fm.append('---')

    voice = op['voice'][lang]
    body = ['', L(f'![{n}, official card art](/art/operators/{slug}.webp)', f'![{n}，官方卡面圖](/art/operators/{slug}.webp)'), '',
            L('## Profile', '## 基本資料'), '', L('| Field | Value |', '| 欄位 | 內容 |'), '| --- | --- |']
    rows = [
        (L('Rarity', '稀有度'), L(f"{op['rarity']}-star", f"{op['rarity']} 星")),
        (L('Class', '職業'), op['class'][lang]), (L('Element', '屬性'), op['element'][lang]),
        (L('Weapon', '武器'), op['weapon'][lang]), (L('Main attribute', '主屬性'), op['mainAttr'][lang]),
        (L('Secondary attribute', '副屬性'), op['subAttr'][lang]), (L('Faction', '陣營'), op['faction'][lang]),
        (L('Race', '種族'), op['race'][lang]), (L('Voice, English', '英語配音'), voice.get('eng')),
        (L('Voice, Japanese', '日語配音'), voice.get('jap')), (L('Voice, Chinese', '中文配音'), voice.get('chi')),
        (L('Voice, Korean', '韓語配音'), voice.get('kor')),
    ]
    body += [f'| {k} | {v} |' for k, v in rows if v]
    body += ['', text['intro'][lang], '', L('## How to obtain', '## 取得方式'), '']
    for block in obtain(op, st, lang):
        body += [block, '']

    n_main, n_sub = op['mainAttr'][lang], op['subAttr'][lang]
    body += [L('## Recommended weapons', '## 推薦武器'), '',
             L(f"The weapons the game recommends for {n}, in the game's order. Each weapon has three Essence stats, one per weapon skill; an Essence raises every skill whose stat it carries. The game also recommends, for every operator, weapons that raise the main and secondary attributes, here {n_main} and {n_sub}.",
               f"遊戲為{n}推薦的武器，依遊戲中的順序。每把武器有三個基質詞條，各對應一個武器技能；基質帶有哪個詞條，就提升對應的技能。遊戲也會為每名幹員推薦提升主屬性與副屬性的武器，{n}是{n_main}與{n_sub}。"), '',
             L('| Weapon | Rarity | Essence stats |', '| 武器 | 稀有度 | 基質詞條 |'), '| --- | --- | --- |']
    body += recommended(op, lang)
    body += ['', L(f'Every weapon, with its Essence stats and the operators it is recommended for, is on the [Weapons list]({pre}/systems/weapons/).',
                   f'所有武器的基質詞條與推薦幹員見[武器列表]({pre}/systems/weapons/)。'), '']
    body += [L('## Skills', '## 技能'), '', L('| Slot | Name | What it does |', '| 欄位 | 名稱 | 效果 |'), '| --- | --- | --- |']
    for s in op['skills']:
        effect = closed_sentence(text['skills'][s['kind']][lang], lang) + skill_suffix(s, lang)
        body.append(f"| {SLOT[s['kind']][lang]} | {s['name'][lang]} | {effect} |")
    body += ['', L('## Skill values', '## 技能數值'), '',
             L('The values the game lists for each skill, at skill level 1 and at the highest level, 12. A value that does not change is the same in both columns.',
               '遊戲為每個技能列出的數值，分別是技能等級 1 與最高的等級 12。不隨等級改變的數值，兩欄相同。'), '',
             L('| Skill | Value | Level 1 | Level 12 |', '| 技能 | 數值 | 等級 1 | 等級 12 |'), '| --- | --- | --- | --- |']
    for s in op['skills']:
        assert s['levels'] == 12, (slug, s['kind'])
        for v in s['values']:
            body.append(f"| {s['name'][lang]} | {v['name'][lang]} | {v['first']} | {v['last']} |")
    body += ['', L('## Talents', '## 天賦'), '', L('| Talent | Unlock | Effect |', '| 天賦 | 解鎖 | 效果 |'), '| --- | --- | --- |']
    for t, tx in zip(op['talents'], text['talents']):
        body.append(f"| {t['name'][lang]} | {unlock(t['promotions'], lang)} | {closed_sentence(tx[lang], lang)} |")
    body += ['', L('## Potentials', '## 潛能'), '', L('| No. | Name | Effect |', '| 編號 | 名稱 | 效果 |'), '| --- | --- | --- |']
    for p, tx in zip(op['potentials'], text['potentials']):
        body.append(f"| {p['level']} | {p['name'][lang]} | {tx[lang].strip().rstrip('.。')} |")
    if op['slug'] in BASE['operators']:
        body += ['', L('## Base skills', '## 後勤技能'), '',
                 L(f"Base skills work while {n} is assigned to a room of the Dijiang. Each has two levels; the second replaces the first. See [Dijiang]({pre}/systems/dijiang/).",
                   f"{n}進駐帝江號的艙室時，後勤技能生效。每個技能有兩級，第二級取代第一級。見[帝江號]({pre}/systems/dijiang/)。"), '',
                 L('| Skill | Room | Unlock | Effect |', '| 技能 | 艙室 | 解鎖 | 效果 |'), '| --- | --- | --- | --- |']
        for sk in BASE['operators'][op['slug']]:
            room = BASE['rooms'][sk['room']][lang]
            for lv in sk['levels']:
                stage = L(f"Promotion {ROMAN[lv['promotion']]}", f"精英化{ROMAN[lv['promotion']]}")
                body.append(f"| {sk['name'][lang]} {lv['mark']} | {room} | {stage} | {base_effect(sk, lv, lang)} |")
    body += ['', L('## Base stats', '## 基礎數值'), '',
             L('| Level | Strength | Agility | Intellect | Will | ATK | HP |', '| 等級 | 力量 | 敏捷 | 智識 | 意志 | 攻擊力 | 生命值 |'),
             '| --- | --- | --- | --- | --- | --- | --- |']
    for level in ('1', '90'):
        s = op['stats'][level]
        body.append(f"| {level} | {s['str']} | {s['agi']} | {s['int']} | {s['will']} | {s['atk']} | {s['hp']} |")
    body += ['', L('## Promotion materials', '## 精英化材料'), '',
             L('| Promotion | Level cap | Materials |', '| 精英化 | 等級上限 | 材料 |'), '| --- | --- | --- |']
    for p in op['promotions']:
        sep = L(', ', '、')
        items = sep.join(f"{i['name'][lang]} ×{i['count']}" for i in p['items'])
        body.append(f"| {p['name'][lang]} | {p['levelCap']} | {items} |")
    if CHANGES.get(slug):
        body += ['', L('## Changes since release', '## 上線後的變更'), '', L('| Version | Change |', '| 版本 | 變更 |'), '| --- | --- |']
        for c in CHANGES[slug]:
            body.append(f"| {c['version']} | {c[lang].rstrip('.。')} |")
    return '\n'.join(fm + body) + '\n'


def main():
    for slug, op in OPS.items():
        for lang, folder in ((EN, DOCS), (ZH, os.path.join(DOCS, 'zh-tw'))):
            path = os.path.join(folder, 'operators', f'{slug}.md')
            os.makedirs(os.path.dirname(path), exist_ok=True)
            open(path, 'w', encoding='utf8').write(page(op, lang))
    print(len(OPS), 'operator pages per language')


if __name__ == '__main__':
    main()
