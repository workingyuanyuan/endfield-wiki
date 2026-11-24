"""Write the pages that come from records: one page per operator, in English, Traditional
Chinese, Japanese and Korean.

Usage: python3 -I pipeline/build_pages.py
Reads records/ only (no cache, no network) and writes src/content/docs/operators/<slug>.md
and the same path under zh-tw/, ja/ and ko/. Run scripts/to-zh-cn.py afterwards for the
Simplified Chinese pages. Do not edit the pages it writes: change the record or this script.

Japanese and Korean names come from records/names-jako.json (pipeline/names_jako.py). The
game's own text (the official introduction, skill, talent, potential and base-skill
descriptions) comes from records/gametext/<slug>.json and records/base-skills.json, in each
language's edition, and is shown as given (pipeline/gametext.py writes it the same way for
every script).
"""
import glob
import json
import os
import re
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from gametext import inline, quoted  # noqa: E402

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DOCS = os.path.join(ROOT, 'src', 'content', 'docs')
TODAY = '2026-11-22'
EN, ZH, JA, KO = 'en', 'zh-TW', 'ja', 'ko'
LANGS = (EN, ZH, JA, KO)
FOLDER = {EN: '', ZH: 'zh-tw', JA: 'ja', KO: 'ko'}
PRE = {lang: ('/' + f if f else '') for lang, f in FOLDER.items()}
MAX_DESC = {EN: 110, ZH: 70, JA: 70, KO: 90}
ROMAN = {1: 'I', 2: 'II', 3: 'III', 4: 'IV'}
RUBY = re.compile(r'<p="[^"]*" padding=0>(.*?)</p>')

_JAKO = json.load(open(os.path.join(ROOT, 'records', 'names-jako.json'), encoding='utf8'))
NAMES = {(e['en'], e['zh-TW']): e for e in _JAKO['names']}
TERMS = _JAKO['terms']
PENDING = {lang: set(v) for lang, v in json.load(open(os.path.join(ROOT, 'records', 'pending.json'), encoding='utf8')).items()}


def J(en):
    """A game term in Japanese, by its exact English text (records/names-jako.json)."""
    return TERMS[en][JA]


def K(en):
    """A game term in Korean."""
    return TERMS[en][KO]


def enrich(o):
    """Give every {en, zh-TW} name in a record its Japanese and Korean text."""
    if isinstance(o, dict):
        if isinstance(o.get('en'), str) and isinstance(o.get('zh-TW'), str):
            if JA in o:
                for lang in (JA, KO):
                    o[lang] = RUBY.sub(r'\1', o[lang])
            elif (o['en'], o['zh-TW']) in NAMES:
                e = NAMES[(o['en'], o['zh-TW'])]
                o[JA], o[KO] = e[JA], e[KO]
        for v in o.values():
            enrich(v)
    elif isinstance(o, list):
        for v in o:
            enrich(v)
    return o


def load(name):
    return enrich(json.load(open(os.path.join(ROOT, 'records', name), encoding='utf8')))


def link(lang, text, page):
    """A link to a page, or the text alone where the page does not exist in that language yet."""
    if page in PENDING.get(lang, ()):
        return text
    return f"[{text}]({PRE[lang]}/{page}/)"


# Korean particles depend on whether the word before them ends in a final consonant.
_DIGIT_FINAL = {'0': True, '1': True, '2': False, '3': True, '4': False, '5': False, '6': True, '7': True, '8': True, '9': False}


def josa(word, pair):
    """word + the Korean particle of pair (with final consonant, without): ('은', '는'), ('이', '가'),
    ('을', '를'), ('과', '와'), ('으로', '로'). Digits and Latin letters are read aloud."""
    with_final, without = pair
    last = word.rstrip(')）」 ')[-1]
    code = ord(last) - 0xAC00
    if 0 <= code < 11172:
        final = code % 28
        if pair == ('으로', '로') and final == 8:  # ㄹ takes 로
            return word + without
        return word + (with_final if final else without)
    if last in _DIGIT_FINAL:
        return word + (with_final if _DIGIT_FINAL[last] else without)
    return word + (with_final if last.lower() in 'lmn' else without)


TOPIC, SUBJ, OBJ, AND, TO = ('은', '는'), ('이', '가'), ('을', '를'), ('과', '와'), ('으로', '로')


BANNERS = load('banners.json')
VERSIONS = {v['number']: v for v in load('versions.json')}
OBTAIN = load('obtain.json')
CHANGES = load('changes.json')
OPS = {}
for _path in sorted(glob.glob(os.path.join(ROOT, 'records', 'operators', '*.json'))):
    _rec = enrich(json.load(open(_path, encoding='utf8')))
    for _lang in (JA, KO):
        _rec['voice'][_lang] = {k: NAMES[(v, _rec['voice'][ZH][k])][_lang] for k, v in _rec['voice'][EN].items()}
    _rec['game'] = json.load(open(os.path.join(ROOT, 'records', 'gametext', _rec['slug'] + '.json'), encoding='utf8'))
    OPS[_rec['slug']] = _rec

ALL = BANNERS['banners']
CHARTERED = [b for b in ALL if b['type'] == 'chartered']
STANDARD6 = BANNERS['standardSixStars']
TYPE = {
    'chartered': {EN: 'Chartered Headhunting', ZH: '特許尋訪', JA: J('Chartered Headhunting'), KO: K('Chartered Headhunting')},
    'special': {EN: 'Special Headhunting', ZH: '特殊尋訪', JA: J('Special Headhunting'), KO: K('Special Headhunting')},
    'refactor': {EN: 'RE-Factor Headhunting #1', ZH: '重構尋訪#1', JA: J('RE-Factor Headhunting') + '#1', KO: K('RE-Factor Headhunting') + '#1'},
}
WEAPON_EN = {'Sword': 'a sword', 'Greatsword': 'a greatsword', 'Polearm': 'a polearm',
             'Handcannon': 'a handcannon', 'Arts Unit': 'an Arts Unit'}
SLOT = {
    'basic': {EN: 'Basic attack', ZH: '普通攻擊', JA: J('Basic Attack'), KO: K('Basic Attack')},
    'battle': {EN: 'Battle skill', ZH: '戰技', JA: J('Battle Skill'), KO: K('Battle Skill')},
    'combo': {EN: 'Combo skill', ZH: '連攜技', JA: J('Combo Skill'), KO: K('Combo Skill')},
    'ultimate': {EN: 'Ultimate', ZH: '終結技', JA: J('Ultimate'), KO: K('Ultimate')},
}


RECOMMEND = load('recommend.json')
BASE = load('base-skills.json')
ESSENCE = load('weapon-essence.json')
WEAPON = {w['id']: w for w in load('weapons.json')}
GAME_TABLES = (RECOMMEND['source'], {EN: 'rmxlinux/EndfieldData, game tables (1.6, 2026-11-05)', ZH: 'rmxlinux/EndfieldData 遊戲資料表（1.6，2026-11-05）',
                                     JA: 'rmxlinux/EndfieldData、ゲームデータテーブル（1.6、2026-11-05）', KO: 'rmxlinux/EndfieldData, 게임 데이터 테이블(1.6, 2026-11-05)'})
ATTR_KEY = {'Strength': 'str', 'Agility': 'agi', 'Intellect': 'int', 'Will': 'will'}
def percent(v):
    return f"{round(v * 100, 2):g}%"


def sep_of(lang):
    return {EN: ', ', ZH: '、', JA: '、', KO: ', '}[lang]


def recommended(op, lang):
    rec = RECOMMEND['operators'][op['slug']]
    sep = sep_of(lang)
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
    return b['name'][EN] if lang == EN else f"「{b['name'][lang]}」"


def point(p, lang):
    """A start or end of a banner, as a table cell. Times are server time; the home page says so once."""
    if p['kind'] == 'time':
        return p['at']
    v = LATEST if p['version'] == 'next' else p['version']
    if p['kind'] == 'release' and v == '1.0':
        return {EN: 'Release, 2026-01-22', ZH: '公測，2026-01-22', JA: '正式リリース（2026-01-22）', KO: '정식 출시(2026-01-22)'}[lang]
    if p['kind'] != 'release' and p['version'] == 'next':
        return {EN: f'End of Version {v}', ZH: f'{v} 版結束', JA: f'バージョン{v}終了', KO: f'{v} 버전 종료'}[lang]
    d = VERSIONS[v]['asia']
    return {EN: f"Version {v} update, {d}", ZH: f"{v} 版更新，{d}", JA: f"バージョン{v}アップデート（{d}）", KO: f"{v} 버전 업데이트({d})"}[lang]


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


def join_names(names, lang):
    if len(names) == 1:
        return names[0]
    if lang == ZH:
        return '、'.join(names[:-1]) + '與' + names[-1]
    if lang == JA:
        return '、'.join(names[:-1]) + 'と' + names[-1]
    if lang == KO:
        return ', '.join(names[:-2] + [josa(names[-2], AND)]) + ' ' + names[-1]
    return ', '.join(names[:-1]) + ' and ' + names[-1]


def list_names(slugs, lang):
    return join_names([name(s, lang) for s in slugs], lang)


def describe(op, st, lang):
    n = op['name'][lang]
    r, el, cl, w = op['rarity'], op['element'][lang], op['class'][lang], op['weapon'][lang]
    we = WEAPON_EN[op['weapon'][EN]]
    ja_who = f"{w}を使う星{r}・{el}属性の{cl}オペレーター"
    ko_who = f"{josa(w, OBJ)} 사용하는 {r}성 {el} 속성 {cl} 오퍼레이터"
    if st['kind'] == 'player':
        return {EN: f'The Endministrator, the player character, is a {r}-star {el} {cl} with {we}.',
                ZH: f'{n}是玩家操作的主角，{r} 星{el}{cl}幹員，使用{w}。',
                JA: f'{n}はプレイヤーが操作する主人公で、{ja_who}である。',
                KO: f'{josa(n, TOPIC)} 플레이어가 조작하는 주인공으로, {ko_who}이다.'}[lang]
    if st['kind'] == 'chartered':
        own = st['own']['name']
        tail = {EN: f"limited, rate-up in {own[EN]}", ZH: f"限定幹員，於{bname(st['own'], ZH)}機率提升",
                JA: f"「{own[JA]}」で{J('UP')}対象となった限定オペレーターである", KO: f"「{own[KO]}」에서 {K('UP')} 대상이었던 한정 오퍼레이터이다"}[lang]
    else:
        key = 'starting' if st.get('starting') else st['kind']
        tail = {
            'standard6': {EN: 'in the standard headhunting roster', ZH: '在常駐尋訪名單內', JA: f"恒常の{J('Headhunting')}対象である", KO: f"상시 {K('Headhunting')} 명단에 있다"},
            'standard': {EN: 'in the standard headhunting roster', ZH: '在常駐尋訪名單內', JA: f"恒常の{J('Headhunting')}対象である", KO: f"상시 {K('Headhunting')} 명단에 있다"},
            'starting': {EN: 'every account starts with this operator', ZH: '每個帳號開局就擁有', JA: 'どのアカウントも最初から所持している', KO: '모든 계정이 처음부터 보유한다'},
            'reward': {EN: 'given by a Version 1.5 event', ZH: '1.5 版活動贈送的幹員', JA: 'バージョン1.5のイベントで配布された', KO: '1.5 버전 이벤트에서 지급되었다'},
        }[key][lang]
    out = {EN: f'{n} is a {r}-star {el} {cl} with {we}; {tail}.', ZH: f'{n}是 {r} 星{el}{cl}幹員，使用{w}；{tail}。',
           JA: f'{n}は{ja_who}で、{tail}。', KO: f'{josa(n, TOPIC)} {ko_who}로, {tail}.'}[lang]
    if len(out) > MAX_DESC[lang]:
        out = {EN: f'{n} is a {r}-star {el} {cl} with {we}; limited operator.', ZH: f'{n}是 {r} 星{el}{cl}幹員，使用{w}；限定幹員。',
               JA: f'{n}は{ja_who}で、限定オペレーターである。', KO: f'{josa(n, TOPIC)} {ko_who}로, 한정 오퍼레이터이다.'}[lang]
    return out


RULE = {EN: "A limited operator stays in the pool of the two Chartered Headhunting banners after its own, without rate-up, then leaves the pool; limited operators are never added to Basic Headhunting.",
        ZH: '限定幹員在自己那一期之後的 2 期特許尋訪仍在名單內，但沒有機率提升，之後移出名單；限定幹員不會加入基礎尋訪。',
        JA: f"限定オペレーターは自身の{J('Headhunting')}の後、続く2回の{J('Chartered Headhunting')}にも{J('UP')}なしで含まれ、その後は対象から外れる。限定オペレーターが{J('Basic Headhunting')}に追加されることはない。",
        KO: f"한정 오퍼레이터는 자신의 {K('Headhunting')} 이후 다음 2회의 {K('Chartered Headhunting')}에도 {K('UP')} 없이 포함되고, 그 뒤 명단에서 빠진다. 한정 오퍼레이터는 {K('Basic Headhunting')}에 추가되지 않는다."}


def caveat(op, st, lang):
    n = op['name'][lang]
    nt = josa(n, TOPIC) if lang == KO else n
    k = st['kind']
    if k == 'player':
        return {EN: 'The Endministrator is the player character and is in no headhunting pool. The official operator list shows two Endministrator entries for one operator.',
                ZH: f'{n}是玩家操作的主角，不在任何尋訪名單內。官方幹員列表的兩筆{n}是同一名幹員。',
                JA: f"{n}はプレイヤーが操作する主人公で、どの{J('Headhunting')}の対象にも含まれない。公式オペレーター一覧にある2件の{n}は同じオペレーターである。",
                KO: f"{nt} 플레이어가 조작하는 주인공으로, 어떤 {K('Headhunting')}에도 포함되지 않는다. 공식 오퍼레이터 목록의 {n} 2개는 같은 오퍼레이터이다."}[lang]
    if k == 'reward':
        return {EN: f"{n} is in no headhunting pool; {n} was given by the Version {st['version']} event {st['event'][EN]}.",
                ZH: f"{n}不在任何尋訪名單內，是 {st['version']} 版活動「{st['event'][ZH]}」贈送的幹員。",
                JA: f"{n}はどの{J('Headhunting')}の対象にも含まれず、バージョン{st['version']}のイベント「{st['event'][JA]}」で配布された。",
                KO: f"{nt} 어떤 {K('Headhunting')}에도 포함되지 않으며, {st['version']} 버전 이벤트 「{st['event'][KO]}」에서 지급되었다."}[lang]
    if k == 'standard6':
        return {EN: f'{n} has never been the rate-up operator of a banner. {n} is one of five standard 6-star operators listed in every Chartered Headhunting pool.',
                ZH: f'{n}沒有當過機率提升幹員；{n}是 5 名常駐 6 星幹員之一，每一期特許尋訪的名單都有{n}。',
                JA: f"{n}が{J('UP')}対象になったことはない。{n}はすべての{J('Chartered Headhunting')}の対象に含まれる恒常の星6オペレーター5人の1人である。",
                KO: f"{nt} {K('UP')} 대상이었던 적이 없다. {nt} 모든 {K('Chartered Headhunting')} 명단에 포함되는 상시 6성 오퍼레이터 5명 중 1명이다."}[lang]
    if k == 'standard':
        if st['starting']:
            return {EN: f'Every account has {n} from the start of the game; {n} is also in the standard headhunting roster.',
                    ZH: f'每個帳號從遊戲開始就擁有{n}；{n}也在常駐尋訪名單內。',
                    JA: f"どのアカウントもゲーム開始時から{n}を所持している。{n}は恒常の{J('Headhunting')}対象でもある。",
                    KO: f"모든 계정이 게임 시작부터 {josa(n, OBJ)} 보유한다. {nt} 상시 {K('Headhunting')} 명단에도 있다."}[lang]
        return {EN: f'{n} has no rate-up banner. {n} is in the standard roster that Basic Headhunting and every Chartered Headhunting pool draw from.',
                ZH: f'{n}沒有機率提升尋訪；{n}在常駐名單內，基礎尋訪與每一期特許尋訪都抽得到。',
                JA: f"{n}には{J('UP')}対象となる{J('Headhunting')}がない。{n}は恒常の排出対象で、{J('Basic Headhunting')}とすべての{J('Chartered Headhunting')}で出現する。",
                KO: f"{nt} {K('UP')} 대상이었던 {K('Headhunting')}이 없다. {nt} 상시 명단에 있어 {K('Basic Headhunting')}과 모든 {K('Chartered Headhunting')}에서 나온다."}[lang]
    out = RULE[lang]
    for b in st['rerun']:
        out += {EN: f" {n} returned as the rate-up operator of RE-Factor Headhunting {b['name'][EN]}.",
                ZH: f"{n}曾在重構尋訪{bname(b, ZH)}再次機率提升。",
                JA: f"{n}は{J('RE-Factor Headhunting')}{bname(b, JA)}で再び{J('UP')}対象になった。",
                KO: f" {nt} {K('RE-Factor Headhunting')} {bname(b, KO)}에서 다시 {K('UP')} 대상이 되었다."}[lang]
    return out


def banner_table(slug, banners, lang):
    head = {EN: '| Banner | Type | Place | Opens | Ends |', ZH: '| 尋訪 | 類型 | 位置 | 開放 | 結束 |',
            JA: f"| {J('Headhunting')} | 種類 | 位置づけ | 開始 | 終了 |", KO: f"| {K('Headhunting')} | 유형 | 위치 | 시작 | 종료 |"}[lang]
    rows = [head, '| --- | --- | --- | --- | --- |']
    for b in banners:
        if b['rateUp'] == slug:
            place = {EN: 'Rate-up', ZH: '機率提升', JA: J('UP'), KO: K('UP')}[lang]
        elif b['type'] == 'special':
            place = {EN: 'One of four 6-star operators', ZH: '四名 6 星幹員之一', JA: '星6オペレーター4人のうちの1人', KO: '6성 오퍼레이터 4명 중 1명'}[lang]
        else:
            place = {EN: 'In the pool', ZH: '在名單內', JA: '対象に含まれる', KO: '명단에 포함'}[lang]
        rows.append(f"| {b['name'][lang]} | {TYPE[b['type']][lang]} | {place} | {point(b['opens'], lang)} | {point(b['closes'], lang)} |")
    return '\n'.join(rows)


def special_notes(slug, banners, lang):
    out = []
    n = name(slug, lang)
    for b in banners:
        if b['type'] == 'special':
            four = list_names(b['sixStars'], lang)
            out.append({EN: f"{b['name'][EN]} held only {four} as 6-star operators. Its guarantee count was separate from every other banner; 120 pulls on it gave a permit to choose one of the four.",
                        ZH: f"{bname(b, ZH)}的 6 星幹員只有{four}。它的保底計數與其他尋訪分開；在這個尋訪累計 120 次，可獲得一張從四人中任選一名的憑證。",
                        JA: f"{bname(b, JA)}の星6オペレーターは{four}のみだった。天井のカウントは他のすべての{J('Headhunting')}と別で、この{J('Headhunting')}で120回引くと4人から1人を選べる選択券がもらえた。",
                        KO: f"{bname(b, KO)}의 6성 오퍼레이터는 {four}뿐이었다. 천장 카운트는 다른 모든 {K('Headhunting')}과 별도였고, 이 {K('Headhunting')}에서 120회 뽑으면 4명 중 1명을 고를 수 있는 선택권을 받았다."}[lang])
        if b['type'] == 'refactor' and b['rateUp'] == slug:
            out.append({EN: f"RE-Factor Headhunting brings back an earlier rate-up operator. {b['name'][EN]} guarantees {n} within the first 120 pulls, once across all banners of that name, and its pull count carries over to the next banner of the same name.",
                        ZH: f"重構尋訪讓過去的機率提升幹員再次登場。{bname(b, ZH)}前 120 次尋訪必定獲得{n}，這項保底在所有同名重構尋訪中只生效 1 次，計數會繼承到下一次同名重構尋訪。",
                        JA: f"{J('RE-Factor Headhunting')}は過去の{J('UP')}対象を再び登場させる。{bname(b, JA)}では最初の120回以内に{n}が必ず出る。この確定は同名の{J('RE-Factor Headhunting')}全体で1回だけで、回数は次の同名の{J('RE-Factor Headhunting')}に引き継がれる。",
                        KO: f"{K('RE-Factor Headhunting')}은 과거의 {K('UP')} 대상을 다시 등장시킨다. {bname(b, KO)}에서는 처음 120회 안에 {josa(n, OBJ)} 반드시 얻는다. 이 확정은 같은 이름의 {K('RE-Factor Headhunting')} 전체에서 한 번만 적용되며, 횟수는 다음 같은 이름의 {K('RE-Factor Headhunting')}으로 이어진다."}[lang])
    return out


def obtain(op, st, lang):
    slug, n = op['slug'], op['name'][lang]
    nt = josa(n, TOPIC) if lang == KO else n
    ns = josa(n, SUBJ) if lang == KO else n
    k = st['kind']
    if k == 'player':
        return [{EN: 'The Endministrator is the player character: every account has the Endministrator from the start of the game, and no headhunting pool contains this operator. The official operator list shows two entries for this one operator, one for each appearance.',
                 ZH: f'{n}是玩家操作的主角，每個帳號從遊戲開始就擁有，不在任何尋訪名單內。官方幹員列表有兩筆{n}，是同一名幹員的兩種外觀。',
                 JA: f"{n}はプレイヤーが操作する主人公で、どのアカウントもゲーム開始時から所持している。どの{J('Headhunting')}の対象にも含まれない。公式オペレーター一覧には{n}が2件あるが、外見の違う同じオペレーターである。",
                 KO: f"{nt} 플레이어가 조작하는 주인공으로, 모든 계정이 게임 시작부터 보유한다. 어떤 {K('Headhunting')}에도 포함되지 않는다. 공식 오퍼레이터 목록에는 {ns} 2개 있지만, 외형만 다른 같은 오퍼레이터이다."}[lang]]
    if k == 'reward':
        ev, extra = st['event'][lang], st['with'][lang]
        start, end = st['opens']['at'], point(st['closes'], lang)
        v = st['version']
        return [{EN: f'{n} was given by {ev}, a giveaway event of Version {v} that ran from {start} to the {end}. Logging in and playing the game modes during the event gave {n}, {extra}.',
                 ZH: f'{n}由 {v} 版的饋贈活動「{ev}」贈送，活動時間為 {start} 至 {end}。活動期間登入並參與各類玩法，可領取{n}、{extra}。',
                 JA: f'{n}はバージョン{v}の配布イベント「{ev}」でもらえた。開催期間は{start}から{end}までだった。期間中にログインして各モードを遊ぶと、{n}、{extra}が手に入った。',
                 KO: f'{nt} {v} 버전의 배포 이벤트 「{ev}」에서 지급되었다. 이벤트 기간은 {start}부터 {end}까지였다. 기간 중 접속해 각 콘텐츠를 플레이하면 {n}, {josa(extra, OBJ)} 받을 수 있었다.'}[lang]]
    if k in ('standard6', 'standard'):
        out = []
        if st['starting']:
            who = list_names(OBTAIN['starting'], lang)
            out.append({EN: f'The four starting operators are {who}.',
                        ZH: f'初始幹員共四名：{who}。',
                        JA: f'初期オペレーターは{who}の4人である。',
                        KO: f'초기 오퍼레이터는 {who} 4명이다.'}[lang])
        if k == 'standard6':
            five = list_names(STANDARD6, lang)
            out.append({EN: f'{n} has no rate-up banner. Five standard 6-star operators are in the pool of Basic Headhunting and of every Chartered Headhunting banner: {five}.',
                        ZH: f'{n}沒有自己的機率提升尋訪。基礎尋訪與每一期特許尋訪的名單都有這 5 名常駐 6 星幹員：{five}。',
                        JA: f"{n}には自身が{J('UP')}対象となる{J('Headhunting')}がない。恒常の星6オペレーターは{five}の5人で、{J('Basic Headhunting')}とすべての{J('Chartered Headhunting')}の対象に含まれる。",
                        KO: f"{nt} 자신이 {K('UP')} 대상인 {K('Headhunting')}이 없다. 상시 6성 오퍼레이터 5명({five})은 {K('Basic Headhunting')}과 모든 {K('Chartered Headhunting')}에 포함된다."}[lang])
        else:
            out.append({EN: f'{n} has no rate-up banner. {n} is in the standard roster, which Basic Headhunting and every Chartered Headhunting pool draw from.',
                        ZH: f'{n}沒有自己的機率提升尋訪。{n}在常駐名單內，基礎尋訪與每一期特許尋訪都抽得到。',
                        JA: f"{n}には自身が{J('UP')}対象となる{J('Headhunting')}がない。{n}は恒常の排出対象で、{J('Basic Headhunting')}とすべての{J('Chartered Headhunting')}で出現する。",
                        KO: f"{nt} 자신이 {K('UP')} 대상인 {K('Headhunting')}이 없다. {nt} 상시 명단에 있어 {K('Basic Headhunting')}과 모든 {K('Chartered Headhunting')}에서 나온다."}[lang])
        if st['banners']:
            out.append({EN: f'Banners other than Chartered Headhunting that listed {n}:', ZH: f'特許尋訪以外，名單內有{n}的尋訪：',
                        JA: f"{J('Chartered Headhunting')}以外で{n}が対象に含まれた{J('Headhunting')}：",
                        KO: f"{K('Chartered Headhunting')} 외에 {ns} 포함된 {K('Headhunting')}:"}[lang])
            out.append(banner_table(slug, st['banners'], lang))
            out += special_notes(slug, st['banners'], lang)
        return out
    own = st['own']
    v = own['version']
    page_id = f"versions/{v.replace('.', '-')}"
    if v == '1.0':
        where = {EN: link(EN, 'Version 1.0', page_id), ZH: link(ZH, '1.0 版', page_id), JA: link(JA, 'バージョン1.0', page_id), KO: link(KO, '1.0 버전', page_id)}[lang]
    else:
        t = VERSIONS[v]['title']
        where = {EN: link(EN, f"Version {v}, {t[EN]}", page_id), ZH: link(ZH, f"{v} 版「{t[ZH]}」", page_id),
                 JA: link(JA, f"バージョン{v}「{t[JA]}」", page_id), KO: link(KO, f"{v} 버전 「{t[KO]}」", page_id)}[lang]
    out = [{EN: f"{n} is the rate-up 6-star operator of {own['name'][EN]}, a Chartered Headhunting banner of {where}. Banners with {n}:",
            ZH: f"{n}是{where}特許尋訪{bname(own, ZH)}的機率提升 6 星幹員。名單內有{n}的尋訪：",
            JA: f"{n}は{where}の{J('Chartered Headhunting')}{bname(own, JA)}で{J('UP')}対象となった星6オペレーターである。{n}が対象に含まれた{J('Headhunting')}：",
            KO: f"{nt} {where}의 {K('Chartered Headhunting')} {bname(own, KO)}에서 {K('UP')} 대상이었던 6성 오퍼레이터이다. {ns} 포함된 {K('Headhunting')}:"}[lang],
           banner_table(slug, st['banners'], lang), RULE[lang]]
    return out + special_notes(slug, st['banners'], lang)


def skill_cost(skill, lang):
    """The cost or cooldown of a skill, from the record."""
    k = skill['kind']
    if k == 'battle' and skill['cost']:
        c = skill['cost']
        return {EN: f"{c} SP", ZH: f"{c} 點技力", JA: f"{J('SP Cost')} {c}", KO: f"{K('SP Cost')} {c}"}[lang]
    if k == 'ultimate' and skill['cost']:
        c = skill['cost']
        return {EN: f"{c} Ultimate Energy", ZH: f"{c} 點終結技能量", JA: f"{J('Ultimate Energy Cost')} {c}", KO: f"{K('Ultimate Energy Cost')} {c}"}[lang]
    if k == 'combo' and skill['cooldown'][0]:
        a, b = skill['cooldown']
        if a == b:
            return {EN: f'Cooldown {a} s', ZH: f'冷卻 {a} 秒', JA: f"{J('Cooldown')} {a}秒", KO: f"{K('Cooldown')} {a}초"}[lang]
        return {EN: f'Cooldown {a} s, {b} s at level 12', ZH: f'冷卻 {a} 秒，等級 12 時 {b} 秒',
                JA: f"{J('Cooldown')} {a}秒（レベル12で{b}秒）", KO: f"{K('Cooldown')} {a}초(레벨 12에서 {b}초)"}[lang]
    return '—'


def stage_name(p, lang):
    return {EN: f'Promotion {ROMAN[p]}', ZH: f'精英化{ROMAN[p]}', JA: J(f'Promotion {ROMAN[p]}'), KO: K(f'Promotion {ROMAN[p]}')}[lang]


def unlock(promotions, lang):
    first = {EN: 'Default', ZH: '預設', JA: '初期', KO: '기본'}[lang] if promotions[0] == 0 else stage_name(promotions[0], lang)
    later = [stage_name(p, lang) for p in promotions[1:]]
    if not later:
        return first
    if lang == ZH:
        return f"{first}；{'、'.join(later)} 時提升"
    if lang == JA:
        return f"{first}（{'、'.join(later)}で強化）"
    if lang == KO:
        return f"{first}({', '.join(later)}에서 강화)"
    return f"{first}; upgraded at {' and '.join(later)}"


def quote(value):
    return '"' + value.replace('\\', '\\\\').replace('"', '\\"') + '"'


def aliases_of(titles, title):
    """Every other name of a page, the same set in every language: titles maps en, zh-TW,
    zh-CN, ja and ko to the page's title in each."""
    return list(dict.fromkeys(t for t in (titles[x] for x in (EN, ZH, 'zh-CN', JA, KO)) if t != title))


def page(op, lang):
    slug = op['slug']
    st = status(slug)
    n = op['name'][lang]
    game = op['game']
    L = lambda en, zh, ja, ko: {EN: en, ZH: zh, JA: ja, KO: ko}[lang]  # noqa: E731

    desc = describe(op, st, lang)
    assert len(desc) <= MAX_DESC[lang], (slug, lang, len(desc), desc)

    # Sources and the date of the newest notice a page relies on.
    banners = st.get('banners') or []
    sources = [(L('Official operator list (Gryphline)', '官方幹員列表 (Gryphline)', '公式オペレーター一覧（Gryphline）', '공식 오퍼레이터 목록(Gryphline)'),
                'https://endfield.gryphline.com/en-us/operator')]
    dates = ['2026-01-22']
    for b in banners:
        t = TYPE[b['type']]
        title = L(f"{b['name'][EN]} {t[EN]}", f"{bname(b, ZH)}{t[ZH]}說明", f"{bname(b, JA)}{t[JA]}のお知らせ", f"{bname(b, KO)} {t[KO]} 안내")
        sources.append((title, f"https://endfield.gryphline.com/en-us/news/{b['notice']}"))
        dates.append(b['noticeDate'])
    versions = {c['version'] for c in CHANGES.get(slug, [])} | ({st['version']} if st['kind'] == 'reward' else set())
    if st['kind'] == 'chartered' and st['own']['version'] != '1.0':
        versions.add(st['own']['version'])
    for v in sorted(versions):
        ver = VERSIONS[v]
        t = ver['title']
        sources.append((L(f"{t[EN]} Version Update Notes", f"「{t[ZH]}」版本更新說明", f"「{t[JA]}」バージョンアップデートの説明", f"「{t[KO]}」 버전 업데이트 설명"),
                        f"https://endfield.gryphline.com/en-us/news/{ver['notes']}"))
        dates.append(ver['notesDate'])
    gv = op['gameDataVersion']
    sources.append((L(f"warfarin.wiki, {op['name'][EN]} (game data {gv})", f"warfarin.wiki {n}頁（遊戲資料 {gv}）",
                      f"warfarin.wiki、{n}（ゲームデータ {gv}）", f"warfarin.wiki, {n}(게임 데이터 {gv})"), op['gameDataPage']))
    sources.append((GAME_TABLES[1][lang], GAME_TABLES[0]))
    sources.append((L(f"Endfield Talos Wiki, {op['name'][EN]}", f"Endfield Talos Wiki 的 {op['name'][EN]} 頁",
                      f"Endfield Talos Wiki、{op['name'][EN]}", f"Endfield Talos Wiki, {op['name'][EN]}"),
                    'https://endfield.wiki.gg/wiki/' + op['name'][EN].replace(' ', '_')))

    aliases = aliases_of(op['name'], n)

    fm = ['---', f'title: {quote(n)}', f'description: {quote(desc)}',
          'appliesTo: ' + quote(L(f"Arknights: Endfield, global service, Version 1.6; skill texts and stats from game data {gv}",
                                  f"《明日方舟：終末地》國際版，1.6 版；技能文字與數值出自遊戲資料 {gv}",
                                  f"『アークナイツ：エンドフィールド』グローバル版、バージョン1.6。スキル説明と数値はゲームデータ {gv} による",
                                  f"《명일방주: 엔드필드》 글로벌 서비스, 1.6 버전. 스킬 설명과 수치는 게임 데이터 {gv} 기준")),
          f'caveat: {quote(caveat(op, st, lang))}', f'lastVerified: {TODAY}', f'effectiveDate: {max(dates)}', 'aliases:']
    fm += [f'  - {quote(a)}' for a in aliases]
    fm += ['art:', '  - title: ' + L('Operator list', '幹員列表', 'オペレーター一覧', '오퍼레이터 목록'), '    url: https://endfield.gryphline.com/en-us/operator', 'sources:']
    for title, url in sources:
        fm += [f'  - title: {quote(title)}', f'    url: {url}']
    fm.append('---')

    voice = op['voice'][lang]
    body = ['', L(f'![{n}, official card art](/art/operators/{slug}.webp)', f'![{n}，官方卡面圖](/art/operators/{slug}.webp)',
                  f'![{n}、公式カードイラスト](/art/operators/{slug}.webp)', f'![{n}, 공식 카드 일러스트](/art/operators/{slug}.webp)'), '',
            L('## Profile', '## 基本資料', '## プロフィール', '## 프로필'), '', L('| Field | Value |', '| 項目 | 內容 |', '| 項目 | 内容 |', '| 항목 | 내용 |'), '| --- | --- |']
    rows = [
        (L('Rarity', '稀有度', J('Rarity'), K('Rarity')), L(f"{op['rarity']}-star", f"{op['rarity']} 星", f"星{op['rarity']}", f"{op['rarity']}성")),
        (L('Class', '職業', J('Class'), K('Class')), op['class'][lang]), (L('Element', '屬性', J('Element'), K('Element')), op['element'][lang]),
        (L('Weapon', '武器', J('Weapon'), K('Weapon')), op['weapon'][lang]),
        (L('Main attribute', '主屬性', J('Main Attribute'), K('Main Attribute')), op['mainAttr'][lang]),
        (L('Secondary attribute', '副屬性', J('Secondary Attribute'), K('Secondary Attribute')), op['subAttr'][lang]),
        (L('Faction', '陣營', J('Faction'), K('Faction')), op['faction'][lang]),
        (L('Race', '種族', J('Race'), K('Race')), op['race'][lang]), (L('Voice, English', '英語配音', '英語ボイス', '영어 음성'), voice.get('eng')),
        (L('Voice, Japanese', '日語配音', '日本語ボイス', '일본어 음성'), voice.get('jap')), (L('Voice, Chinese', '中文配音', '中国語ボイス', '중국어 음성'), voice.get('chi')),
        (L('Voice, Korean', '韓語配音', '韓国語ボイス', '한국어 음성'), voice.get('kor')),
    ]
    if os.path.exists(os.path.join(ROOT, 'records', 'story', f'{slug}.json')):
        # The operator's files, voice lines and chats are on the story page; the row is named by
        # the game's own term for the files.
        file_term = json.load(open(os.path.join(ROOT, 'records', 'story', 'terms.json'), encoding='utf8'))['file']
        story = link(lang, L(f"{n}'s file", f'{n}的檔案', f'{n}のプロファイル', f'{n}의 파일'), f'story/{slug}')
        rows.append((L(file_term['en'], file_term['zh-TW'], file_term['ja'], file_term['ko']), story))
    body += [f'| {k} | {v} |' for k, v in rows if v]
    body += ['', quoted(game['intro'][lang]), '']
    body += [L('## How to obtain', '## 取得方式', '## 入手方法', '## 획득 방법'), '']
    for block in obtain(op, st, lang):
        body += [block, '']

    n_main, n_sub = op['mainAttr'][lang], op['subAttr'][lang]
    body += [L('## Recommended weapons', '## 推薦武器', f"## {J('Recommended')}{J('Weapon')}", f"## {K('Recommended')} {K('Weapon')}"), '',
             L(f"Each weapon has three Essence stats, one per weapon skill; an Essence raises every skill whose stat it carries. The game also recommends, for every operator, weapons that raise the main and secondary attributes, here {n_main} and {n_sub}.",
               f"每把武器有三個基質詞條，各對應一個武器技能；基質帶有哪個詞條，就提升對應的技能。遊戲也會為每名幹員推薦提升主屬性與副屬性的武器，{n}是{n_main}與{n_sub}。",
               f"各武器には{J('Essence Stats')}が3つあり、それぞれ{J('Weapon Skill')}1つに対応する。{J('Essence')}は、持っている{J('Essence Stats')}に対応するスキルをすべて強化する。ゲームはどのオペレーターにも、{J('Main Attribute')}と{J('Secondary Attribute')}を上げる武器も{J('Recommended')}する。{n}の場合は{n_main}と{n_sub}である。",
               f"각 무기에는 {josa(K('Essence Stats'), SUBJ)} 3개 있으며, 각각 {K('Weapon Skill')} 하나에 대응한다. {josa(K('Essence'), TOPIC)} 지닌 {K('Essence Stats')}에 대응하는 스킬을 모두 강화한다. 게임은 모든 오퍼레이터에게 {josa(K('Main Attribute'), AND)} {josa(K('Secondary Attribute'), OBJ)} 올리는 무기도 {K('Recommended')}하며, {n}에게는 {n_main}·{n_sub} 무기이다."), '',
             L('| Weapon | Rarity | Essence stats |', '| 武器 | 稀有度 | 基質詞條 |', f"| {J('Weapon')} | {J('Rarity')} | {J('Essence Stats')} |", f"| {K('Weapon')} | {K('Rarity')} | {K('Essence Stats')} |"), '| --- | --- | --- |']
    body += recommended(op, lang)
    body += ['']
    body += [L('## Skills', '## 技能', f"## {J('Skills')}", f"## {K('Skills')}"), '',
             L('| Slot | Name | Cost or cooldown |', '| 類型 | 名稱 | 消耗或冷卻 |', f"| 枠 | 名称 | コスト・{J('Cooldown')} |", f"| 구분 | 이름 | 소모·{K('Cooldown')} |"), '| --- | --- | --- |']
    for s in op['skills']:
        body.append(f"| {SLOT[s['kind']][lang]} | {s['name'][lang]} | {skill_cost(s, lang)} |")
    texts = {g['kind']: g for g in game['skills']}
    assert sorted(texts) == sorted(s['kind'] for s in op['skills']), slug
    for s in op['skills']:
        g = texts[s['kind']]
        body += ['', f"### {s['name'][lang]}", '']
        if g['text']:
            body += [quoted(g['text'][lang]), '']
        for c in g['conditions']:
            # The condition's name, as the game's tab shows it, unless its text begins with it.
            if not c['text'][lang].startswith(c['name'][lang]):
                body += [f"**{c['name'][lang]}**", '']
            body += [quoted(c['text'][lang]), '']
        body.pop()
    body += ['', L('## Skill values', '## 技能數值', f"## {J('Skills')}数値", f"## {K('Skills')} 수치"), '',
             L('| Skill | Value | Level 1 | Level 12 (highest) |', '| 技能 | 數值 | 等級 1 | 等級 12（最高） |', '| スキル | 数値 | レベル1 | レベル12（最高） |', '| 스킬 | 수치 | 레벨 1 | 레벨 12(최고) |'), '| --- | --- | --- | --- |']
    for s in op['skills']:
        assert s['levels'] == 12, (slug, s['kind'])
        for v in s['values']:
            body.append(f"| {s['name'][lang]} | {v['name'][lang]} | {v['first']} | {v['last']} |")
    body += ['', L('## Talents', '## 天賦', f"## {J('Talent')}", f"## {K('Talent')}")]
    assert len(op['talents']) == len(game['talents']), slug
    for t, g in zip(op['talents'], game['talents']):
        assert [lv['promotion'] for lv in g['levels']] == t['promotions'], (slug, t['promotions'])
        body += ['', f"### {t['name'][lang]}"]
        for lv in g['levels']:
            stage = L('Default', '預設', '初期', '기본') if lv['promotion'] == 0 else stage_name(lv['promotion'], lang)
            body += ['', f"**{stage}**", '', quoted(lv['text'][lang])]
    body += ['', L('## Potentials', '## 潛能', f"## {J('Potential')}", f"## {K('Potential')}"), '',
             L('| No. | Name | Effect |', '| 編號 | 名稱 | 效果 |', '| 番号 | 名称 | 効果 |', '| 번호 | 이름 | 효과 |'), '| --- | --- | --- |']
    assert [p['level'] for p in op['potentials']] == [p['level'] for p in game['potentials']], slug
    for p, g in zip(op['potentials'], game['potentials']):
        body.append(f"| {p['level']} | {p['name'][lang]} | {inline(g['text'][lang])} |")
    if op['slug'] in BASE['operators']:
        dj = {EN: link(EN, 'Dijiang', 'systems/dijiang'), ZH: link(ZH, '帝江號', 'systems/dijiang'),
              JA: link(JA, J('Dijiang'), 'systems/dijiang'), KO: link(KO, K('Dijiang'), 'systems/dijiang')}[lang]
        body += ['', L('## Base skills', '## 後勤技能', f"## {J('Base Skill')}", f"## {K('Base Skill')}"), '',
                 L(f"Base skills work while {n} is assigned to a room of the {dj}. Each has two levels; the second replaces the first.",
                   f"{n}進駐{dj}的艙室時，後勤技能生效。每個技能有兩級，第二級取代第一級。",
                   f"{J('Base Skill')}は、{n}が{dj}の{J('Cabin')}に{J('Assign')}されている間に効果を発揮する。各スキルには2段階あり、2段階目が1段階目に置き換わる。",
                   f"{josa(K('Base Skill'), TOPIC)} {josa(n, SUBJ)} {dj}의 {K('Cabin')}에 {K('Assign')}되어 있는 동안 효과가 있다. 각 스킬은 2단계이며, 2단계가 1단계를 대체한다."), '',
                 L('| Skill | Room | Unlock | Effect |', '| 技能 | 艙室 | 解鎖 | 效果 |', f"| スキル | {J('Cabin')} | {J('Unlock')} | 効果 |", f"| 스킬 | {K('Cabin')} | {K('Unlock')} | 효과 |"),
                 '| --- | --- | --- | --- |']
        for sk in BASE['operators'][op['slug']]:
            room = BASE['rooms'][sk['room']][lang]
            for lv in sk['levels']:
                body.append(f"| {sk['name'][lang]} {lv['mark']} | {room} | {stage_name(lv['promotion'], lang)} | {inline(lv['text'][lang])} |")
    stat_names = [L(en, zh, J(en), K(en)) for en, zh in (('Strength', '力量'), ('Agility', '敏捷'), ('Intellect', '智識'), ('Will', '意志'), ('ATK', '攻擊力'), ('HP', '生命值'))]
    body += ['', L('## Base stats', '## 基礎數值', '## 基礎ステータス', '## 기초 능력치'), '',
             '| ' + ' | '.join([L('Level', '等級', 'レベル', '레벨')] + stat_names) + ' |',
             '| --- | --- | --- | --- | --- | --- | --- |']
    for level in ('1', '90'):
        s = op['stats'][level]
        body.append(f"| {level} | {s['str']} | {s['agi']} | {s['int']} | {s['will']} | {s['atk']} | {s['hp']} |")
    body += ['', L('## Promotion materials', '## 精英化材料', '## 昇進素材', '## 정예화 재료'), '',
             L('| Promotion | Level cap | Materials |', '| 精英化 | 等級上限 | 材料 |', '| 昇進 | レベル上限 | 素材 |', '| 정예화 | 레벨 상한 | 재료 |'), '| --- | --- | --- |']
    for p in op['promotions']:
        items = sep_of(lang).join(f"{i['name'][lang]} ×{i['count']}" for i in p['items'])
        body.append(f"| {p['name'][lang]} | {p['levelCap']} | {items} |")
    if CHANGES.get(slug):
        body += ['', L('## Changes since release', '## 上線後的變更', '## リリース後の変更', '## 출시 후 변경 사항'), '',
                 L('| Version | Change |', '| 版本 | 變更 |', '| バージョン | 変更 |', '| 버전 | 변경 |'), '| --- | --- |']
        for c in CHANGES[slug]:
            body.append(f"| {c['version']} | {c[lang].rstrip('.。')} |")
    return '\n'.join(fm + body) + '\n'


def write_pages(lang):
    for slug, op in OPS.items():
        path = os.path.join(DOCS, FOLDER[lang], 'operators', f'{slug}.md')
        os.makedirs(os.path.dirname(path), exist_ok=True)
        open(path, 'w', encoding='utf8').write(page(op, lang))


def main():
    for lang in LANGS:
        write_pages(lang)
    print(len(OPS), 'operator pages per language:', ', '.join(LANGS))


if __name__ == '__main__':
    main()
