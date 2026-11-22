"""Write the lookup pages that come from records: names, weapons, Dijiang, recipes, enemies.

Usage: python3 -I pipeline/build_lists.py
Reads records/ only and writes src/content/docs/systems/{names,weapons,dijiang,enemies}.md
and aic/recipes.md in English, Traditional Chinese, Japanese and Korean (zh-tw/, ja/, ko/).
Run scripts/to-zh-cn.py afterwards. Do not edit those pages by hand.
"""
import os
import re
import sys
from collections import Counter

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import build_pages as bp  # noqa: E402
from build_pages import EN, ZH, JA, KO, LANGS, FOLDER, MAX_DESC, OPS, TODAY, J, K, josa, link, load, quote  # noqa: E402
from build_pages import TOPIC, SUBJ, OBJ, AND, TO  # noqa: E402

CN = 'zh-CN'
COP = ('이다', '다')
WEAPONS = load('weapons.json')
# A record whose id is another weapon's id plus a suffix (wpn_sword_0021_ink) is a second
# model of that weapon: same name, rarity and stats in the game tables (checked 2026-11-22
# against WeaponBasicTable and ItemTable of rmxlinux/EndfieldData). It is one weapon.
_ids = {w['id'] for w in WEAPONS}
WEAPONS = [w for w in WEAPONS if not any(w['id'].startswith(i + '_') for i in _ids)]
GAME = {EN: 'Arknights: Endfield', ZH: '《明日方舟：終末地》', JA: '『アークナイツ：エンドフィールド』', KO: '《명일방주: 엔드필드》'}


def chooser(lang):
    return lambda en, zh, ja, ko: {EN: en, ZH: zh, JA: ja, KO: ko}[lang]


def front(lang, titles, desc, applies, caveat, effective, sources):
    """Frontmatter. titles maps en, zh-TW, zh-CN, ja and ko to the page's title in each."""
    title = titles[lang]
    assert len(desc) <= MAX_DESC[lang], (title, len(desc), desc)
    aliases = bp.aliases_of(titles, title)
    fm = ['---', f'title: {quote(title)}', f'description: {quote(desc)}', f'appliesTo: {quote(applies)}', f'caveat: {quote(caveat)}',
          f'lastVerified: {TODAY}', f'effectiveDate: {effective}', 'aliases:'] + [f'  - {quote(a)}' for a in aliases] + ['sources:']
    for t, u in sources:
        fm += [f'  - title: {quote(t)}', f'    url: {u}']
    return fm + ['---', '']


def write(section, slug, lang, lines):
    folder = os.path.join(bp.DOCS, FOLDER[lang], section)
    os.makedirs(folder, exist_ok=True)
    open(os.path.join(folder, slug + '.md'), 'w', encoding='utf8').write('\n'.join(lines) + '\n')


def op_link(slug, lang):
    return link(lang, OPS[slug]['name'][lang], f'operators/{slug}')


def distinct(rows):
    seen, out = set(), []
    for r in rows:
        if r[EN] not in seen:
            seen.add(r[EN])
            out.append(r)
    return out


def names(lang):
    L = chooser(lang)
    titles = {EN: 'Names in three scripts', ZH: '名稱對照', CN: '名称对照', JA: '名称対照', KO: '명칭 대조'}
    desc = L('Operators, classes, elements, weapon types, attributes, factions and races of Endfield in three scripts.',
             '《明日方舟：終末地》幹員、職業、屬性、武器類型、陣營與種族的三種文字名稱。',
             f"{GAME[JA]}のオペレーター、職業、属性、武器の種類、能力値、陣営、種族の日本語・英語・中国語名。",
             f"{GAME[KO]} 오퍼레이터, 직업, 속성, 무기 유형, 능력치, 진영, 종족의 한국어·영어·중국어 이름.")
    caveat = L("Rossi is 洛西 in Traditional Chinese and 洛茜 in Simplified Chinese: a different character, not a conversion between scripts. The Simplified names are those of the game's own Simplified Chinese text.",
               '洛西的簡體中文名是洛茜，用字不同，不只是繁簡轉換。簡體中文名稱出自遊戲本身的簡體中文文字。',
               f"{OPS['rossi']['name'][JA]}の中国語名は繁体字で洛西、簡体字で洛茜と字が異なり、字体の変換ではない。日本語名と簡体字名はゲーム自身の日本語・簡体字中国語テキストによる。",
               f"{OPS['rossi']['name'][KO]}의 중국어 이름(번체 洛西, 간체 洛茜)은 번체·간체 변환이 아니라 서로 다른 글자이다. 한국어 이름과 간체 이름은 게임 자체의 한국어·간체 중국어 텍스트를 따른다.")
    sources = [(L('Official operator list (Gryphline)', '官方幹員列表 (Gryphline)', '公式オペレーター一覧（Gryphline）', '공식 오퍼레이터 목록(Gryphline)'), 'https://endfield.gryphline.com/en-us/operator'),
               (L('Official operator list, Simplified Chinese (Hypergryph)', '官方幹員列表，簡體中文 (Hypergryph)', '公式オペレーター一覧、簡体字中国語（Hypergryph）', '공식 오퍼레이터 목록, 간체 중국어(Hypergryph)'), 'https://endfield.hypergryph.com/operator'),
               (L('warfarin.wiki, Operators (game data 1.6)', 'warfarin.wiki 幹員列表（遊戲資料 1.6）', 'warfarin.wiki、オペレーター一覧（ゲームデータ 1.6）', 'warfarin.wiki, 오퍼레이터 목록(게임 데이터 1.6)'), 'https://warfarin.wiki/en/operators')]
    out = front(lang, titles, desc, L('Arknights: Endfield, global service, Version 1.6; names from game data 1.6 in three languages', '《明日方舟：終末地》國際版，1.6 版；名稱出自三種語言的遊戲資料 1.6',
                                      f"{GAME[JA]}グローバル版、バージョン1.6。名称は各言語のゲームデータ 1.6 による", f"{GAME[KO]} 글로벌 서비스, 1.6 버전. 이름은 각 언어의 게임 데이터 1.6 기준"),
                caveat, TODAY, sources)
    head = L('| English | 繁體中文 | 簡體中文 |', '| English | 繁體中文 | 簡體中文 |', '| 日本語 | 英語 | 繁体字中国語 | 簡体字中国語 |', '| 한국어 | 영어 | 중국어 번체 | 중국어 간체 |')
    rule = '| --- | --- | --- |' if lang in (EN, ZH) else '| --- | --- | --- | --- |'

    def row(r, first=None):
        first = first or r[lang if lang in (JA, KO) else EN]
        return f"| {first} | {r[ZH]} | {r[CN]} |" if lang in (EN, ZH) else f"| {first} | {r[EN]} | {r[ZH]} | {r[CN]} |"
    weapons_link = L(link(EN, 'Weapons list', 'systems/weapons'), link(ZH, '武器列表', 'systems/weapons'), link(JA, '武器一覧', 'systems/weapons'), link(KO, '무기 목록', 'systems/weapons'))
    version_link = L(link(EN, 'version page', 'versions'), link(ZH, '版本頁', 'versions'), link(JA, 'バージョンページ', 'versions'), link(KO, '버전 페이지', 'versions'))
    out += [L(f'Names of weapons are on {weapons_link}; names of banners are on each {version_link}, with the version titles.',
              f'武器名稱見{weapons_link}；尋訪名稱與版本標題見各{version_link}。',
              f"武器の名称は{weapons_link}に、{J('Headhunting')}の名称とバージョン名は各{version_link}にある。",
              f"무기 이름은 {weapons_link}에, {K('Headhunting')} 이름과 버전 제목은 각 {version_link}에 있다."), '',
            L('## Operators', '## 幹員', f"## {J('Operators')}", f"## {K('Operators')}"), '', head, rule]
    for slug in sorted(OPS):
        n = OPS[slug]['name']
        out.append(row(n, link(lang, n[EN if lang in (EN, ZH) else lang], f'operators/{slug}')))
    ops = list(OPS.values())
    for key, en_h, zh_h, term in (('class', 'Classes', '職業', 'Class'), ('element', 'Elements', '屬性', 'Element'), ('weapon', 'Weapon types', '武器類型', 'Weapon Type'),
                                  ('faction', 'Factions', '陣營', 'Faction'), ('race', 'Races', '種族', 'Race')):
        out += ['', L(f'## {en_h}', f'## {zh_h}', f'## {J(term)}', f'## {K(term)}'), '', head, rule]
        for r in sorted(distinct([o[key] for o in ops]), key=lambda r: r[EN]):
            out.append(row(r))
    attrs = distinct([o['mainAttr'] for o in ops] + [o['subAttr'] for o in ops])
    out += ['', L('## Attributes', '## 能力值', '## 能力値', '## 능력치'), '', head, rule] + [row(r) for r in sorted(attrs, key=lambda r: r[EN])]
    promo = distinct([p['name'] for o in ops for p in o['promotions']])
    out += ['', L('## Promotion stages', '## 精英化階段', '## 昇進段階', '## 정예화 단계'), '', head, rule] + [row(r) for r in promo]
    write('systems', 'names', lang, out)


def weapons(lang):
    L = chooser(lang)
    total = len(WEAPONS)
    titles = {EN: 'Weapons list', ZH: '武器列表', CN: '武器列表', JA: '武器一覧', KO: '무기 목록'}
    desc = L(f'All {total} Arknights: Endfield weapons in Version 1.6: type, rarity, Essence stats and recommended operators.',
             f'《明日方舟：終末地》1.6 版的 {total} 把武器：類型、稀有度、基質詞條與推薦幹員。',
             f"{GAME[JA]}バージョン1.6の武器{total}種：種類、{J('Rarity')}、{J('Essence Stats')}、{J('Recommended')}オペレーター。",
             f"{GAME[KO]} 1.6 버전의 무기 {total}종: 유형, {K('Rarity')}, {K('Essence Stats')}, {K('Recommended')} 오퍼레이터.")
    fans = {}
    for slug, rec in bp.RECOMMEND['operators'].items():
        for wid in rec['weapons']:
            fans.setdefault(wid, []).append(slug)
    sep = bp.sep_of(lang)
    caveat = L('Operator headhunting gives no weapons. Each pull gives Arsenal Tickets, which are spent on Arsenal Issues; 6-star weapons come from Arsenal Issues and the Arsenal Exchange.',
               '幹員尋訪不會出武器。每次尋訪會給武庫配額，用於武庫申領；6 星武器來自武庫申領與兌換。',
               f"オペレーターの{J('Headhunting')}では武器は出ない。1回引くごとに{J('Arsenal Ticket')}がもらえ、{J('Arsenal Issue')}に使う。星6武器は{J('Arsenal Issue')}と{J('Arsenal Exchange')}で手に入る。",
               f"오퍼레이터 {K('Headhunting')}에서는 무기가 나오지 않는다. 1회 뽑을 때마다 {josa(K('Arsenal Ticket'), OBJ)} 받으며, {K('Arsenal Issue')}에 사용한다. 6성 무기는 {josa(K('Arsenal Issue'), AND)} {K('Arsenal Exchange')}에서 얻는다.")
    b7012 = next(b for b in bp.ALL if b['notice'] == '7012')['name']
    sources = [(L('warfarin.wiki, Weapons (game data 1.6)', 'warfarin.wiki 武器列表（遊戲資料 1.6）', 'warfarin.wiki、武器一覧（ゲームデータ 1.6）', 'warfarin.wiki, 무기 목록(게임 데이터 1.6)'), 'https://warfarin.wiki/en/weapons'),
               (L('The Hearth Fire Beckons the Starry Flow Chartered Headhunting (Arsenal Tickets)', '「煙火邀星河」特許尋訪說明（武庫配額）',
                  f"「{b7012[JA]}」{J('Chartered Headhunting')}のお知らせ（{J('Arsenal Ticket')}）", f"「{b7012[KO]}」 {K('Chartered Headhunting')} 안내({K('Arsenal Ticket')})"), 'https://endfield.gryphline.com/en-us/news/7012'),
               (bp.GAME_TABLES[1][lang], bp.GAME_TABLES[0])]
    out = front(lang, titles, desc, L('Arknights: Endfield, global service, Version 1.6; list from game data 1.6', '《明日方舟：終末地》國際版，1.6 版；列表出自遊戲資料 1.6',
                                      f"{GAME[JA]}グローバル版、バージョン1.6。一覧はゲームデータ 1.6 による", f"{GAME[KO]} 글로벌 서비스, 1.6 버전. 목록은 게임 데이터 1.6 기준"),
                caveat, '2026-11-04', sources)
    types = []
    for w in WEAPONS:
        if w['type'][EN] not in [t[EN] for t in types]:
            types.append(w['type'])
    types.sort(key=lambda t: t[EN])
    count = Counter((w['type'][EN], w['rarity']) for w in WEAPONS)
    rar = sorted({w['rarity'] for w in WEAPONS}, reverse=True)
    ops_link = L(link(EN, 'operator pages', 'operators'), link(ZH, '各幹員頁', 'operators'), link(JA, '各オペレーターのページ', 'operators'), link(KO, '각 오퍼레이터 페이지', 'operators'))
    arsenal = L(link(EN, 'Arsenal and Essences', 'systems/arsenal'), link(ZH, '武庫申領與基質', 'systems/arsenal'),
                link(JA, f"武庫と{J('Essence')}", 'systems/arsenal'), link(KO, f"무기고와 {K('Essence')}", 'systems/arsenal'))
    es_j, es_k = J('Essence Stats'), K('Essence Stats')
    out += [L(f'Version 1.6 has {total} weapons. An operator uses one weapon type, shown on the {ops_link}. How weapons are obtained, and how Essences raise weapon skills, is on {arsenal}. Each 4- to 6-star weapon has three Essence stats, an attribute, a secondary stat and a skill stat, and an Essence raises the weapon skill of each stat it carries; 3-star weapons have none. Recommended for lists the operators whose in-game recommendations include the weapon.',
              f'1.6 版共有 {total} 把武器。每名幹員只使用一種武器類型，見{ops_link}。武器的取得方式與用基質提升武器技能，見{arsenal}。4 到 6 星武器各有三個基質詞條：能力值、副屬性與技能詞條，基質帶有哪個詞條，就提升對應的武器技能；3 星武器沒有基質詞條。「推薦幹員」列出遊戲推薦中包含這把武器的幹員。',
              f"バージョン1.6の武器は{total}種ある。オペレーターが使う{J('Weapon Type')}は1つで、{ops_link}に載っている。武器の入手方法と、{J('Essence')}で{J('Weapon Skill')}を強化する方法は{arsenal}にある。星4〜6の武器には{es_j}が3つ（能力値、サブ、スキルが1つずつ）あり、{J('Essence')}は持っている{es_j}ごとに対応する{J('Weapon Skill')}を強化する。星3の武器には{es_j}がない。「{J('Recommended')}オペレーター」の列には、ゲーム内の{J('Recommended')}にその武器が含まれるオペレーターを挙げた。",
              f"1.6 버전의 무기는 {total}종이다. 오퍼레이터가 사용하는 {K('Weapon Type')}은 하나이며, {ops_link}에 나와 있다. 무기 획득 방법과 {K('Essence')}로 {josa(K('Weapon Skill'), OBJ)} 강화하는 방법은 {arsenal}에 있다. 4~6성 무기에는 {josa(es_k, SUBJ)} 3개(능력치, 보조, 스킬 각 1개) 있으며, {josa(K('Essence'), TOPIC)} 지닌 {es_k}마다 대응하는 {josa(K('Weapon Skill'), OBJ)} 강화한다. 3성 무기에는 {josa(es_k, SUBJ)} 없다. ‘{K('Recommended')} 오퍼레이터’ 열에는 게임 내 {K('Recommended')}에 그 무기가 포함된 오퍼레이터를 적었다."), '',
            L('## Counts by type and rarity', '## 各類型與稀有度的數量', f"## 種類と{J('Rarity')}ごとの数", f"## 유형과 {K('Rarity')}별 수"), '',
            '| ' + L('Type', '類型', '種類', '유형') + ' | ' + ' | '.join(L(f'{r}-star', f'{r} 星', f'星{r}', f'{r}성') for r in rar) + ' | ' + L('Total', '合計', '合計', '합계') + ' |',
            '| --- |' + ' --- |' * (len(rar) + 1)]
    for t in types:
        row = [count[(t[EN], r)] for r in rar]
        out.append(f"| {t[lang]} | " + ' | '.join(str(x) for x in row) + f' | {sum(row)} |')
    for t in types:
        out += ['', f"## {t[lang]}", '',
                L(f"{t[EN]} is {t[ZH]} in Traditional Chinese and {t[CN]} in Simplified Chinese.", f"{t[ZH]}的英文是 {t[EN]}。",
                  f"{t[JA]}の英語名は {t[EN]} である。", f"{t[KO]}의 영어 이름은 ‘{t[EN]}’이다."), '',
                L('| English | 繁體中文 | 簡體中文 | Rarity | Essence stats | Recommended for |', '| English | 繁體中文 | 簡體中文 | 稀有度 | 基質詞條 | 推薦幹員 |',
                  f"| 日本語 | 英語 | {J('Rarity')} | {es_j} | {J('Recommended')}オペレーター |", f"| 한국어 | 영어 | {K('Rarity')} | {es_k} | {K('Recommended')} 오퍼레이터 |"),
                '| --- | --- | --- | --- | --- | --- |' if lang in (EN, ZH) else '| --- | --- | --- | --- | --- |']
        for w in WEAPONS:
            if w['type'][EN] == t[EN]:
                tags = bp.ESSENCE['weapons'].get(w['id'])
                stats = sep.join(bp.ESSENCE['stats'][x]['name'][lang] for x in tags) if tags else L('None', '無', 'なし', '없음')
                assert tags or w['rarity'] == 3, w['id']
                who = sep.join(OPS[o]['name'][lang] for o in fans.get(w['id'], []))
                if lang in (EN, ZH):
                    out.append(f"| {w['name'][EN]} | {w['name'][ZH]} | {w['name'][CN]} | {w['rarity']} | {stats} | {who} |")
                else:
                    out.append(f"| {w['name'][lang]} | {w['name'][EN]} | {w['rarity']} | {stats} | {who} |")
    write('systems', 'weapons', lang, out)


def recipes(lang):
    L = chooser(lang)
    data = load('recipes.json')
    items = data['items']
    fac = {f['id']: f['name'] for f in load('facilities.json')}
    fill = [k for k, v in fac.items() if v[EN] == 'Filling Unit']
    sep_unit = [k for k, v in fac.items() if v[EN] == 'Separating Unit']
    I = lambda i: items[i][lang]  # noqa: E731
    # Merge recipes that differ only in the facility (Reactor and Expanded Crucible).
    merged = {}
    n_fill = n_sep = 0
    for r in data['recipes']:
        if r['machine'] in sep_unit:
            n_sep += 1
            continue
        if r['machine'] in fill and items[r['outputs'][0]['id']][EN] in [items[x['id']][EN] for x in r['inputs']]:
            n_fill += 1  # a container filled with a fluid or gas: same name as the empty one
            continue
        key = (tuple((x['id'], x['count']) for x in r['inputs']), tuple((x['id'], x['count']) for x in r['outputs']), r['seconds'])
        merged.setdefault(key, [])
        if fac[r['machine']] not in merged[key]:
            merged[key].append(fac[r['machine']])
    rows = sorted(merged.items(), key=lambda kv: (items[kv[0][1][0][0]][EN].lower(), kv[0][2]))
    products = {k[1][0][0] for k, _ in rows}
    np_, nr = len(products), len(rows)
    titles = {EN: 'Recipes by product', ZH: '依產品查配方', CN: '依产品查配方', JA: '製品別レシピ', KO: '제품별 제작법'}
    desc = L(f'Which AIC facility makes each of {np_} Arknights: Endfield products, from what inputs and how fast.',
             f'《明日方舟：終末地》{np_} 種集成工業產品由哪個設施製造、需要什麼原料、多快。',
             f"{GAME[JA]}の{J('AIC')}製品{np_}種を、作る{J('Facility')}・原料・所要時間で引ける。",
             f"{GAME[KO]} {K('AIC')} 제품 {np_}종을 만드는 {K('Facility')}, 재료, 소요 시간.")
    caveat = L('Times are per run of one facility. A product with several recipes is listed once per recipe; recipes that use event items are left out.',
               '時間是單一設施做一次的時間。有多個配方的產品，每個配方各列一行；使用活動道具的配方不列入。',
               f"時間は{J('Facility')}1台が1回生産する時間である。レシピが複数ある製品は、レシピごとに1行ずつ載せた。イベントアイテムを使うレシピは載せていない。",
               f"시간은 {K('Facility')} 1대가 한 번 생산하는 시간이다. 제작법이 여러 개인 제품은 제작법마다 한 줄씩 실었다. 이벤트 아이템을 쓰는 제작법은 싣지 않았다.")
    sources = [(L('Recipe table FactoryMachineCraftTable (game data 1.6)', '配方表 FactoryMachineCraftTable（遊戲資料 1.6）',
                  'レシピ表 FactoryMachineCraftTable（ゲームデータ 1.6）', '제작법 표 FactoryMachineCraftTable(게임 데이터 1.6)'),
                bp.GAME_TABLES[0].replace('/tree/', '/blob/') + '/FactoryMachineCraftTable.json')]
    out = front(lang, titles, desc, L('Arknights: Endfield, global service, Version 1.6; recipes from game data 1.6', '《明日方舟：終末地》國際版，1.6 版；配方出自遊戲資料 1.6',
                                      f"{GAME[JA]}グローバル版、バージョン1.6。レシピはゲームデータ 1.6 による", f"{GAME[KO]} 글로벌 서비스, 1.6 버전. 제작법은 게임 데이터 1.6 기준"),
                caveat, TODAY, sources)
    sep = bp.sep_of(lang)
    either = L(' or ', '或', 'または', ' 또는 ')
    prod = L(link(EN, 'Production and logistics', 'aic/production'), link(ZH, '生產與物流', 'aic/production'),
             link(JA, '生産と物流', 'aic/production'), link(KO, '생산과 물류', 'aic/production'))
    citrome = {lang2: items['item_bottled_food_1'][lang2].rstrip('Ⅰ') for lang2 in (JA, KO)}
    buck = {lang2: items['item_bottled_rec_hp_1'][lang2].rstrip('Ⅰ') for lang2 in (JA, KO)}
    fj, fk, sj, sk = J('Filling Unit'), K('Filling Unit'), J('Separating Unit'), K('Separating Unit')
    out += [L(f"Every AIC production recipe of Version 1.6 except filling and emptying containers, sorted by the English name of the product: {nr} recipes for {np_} products. Search the page for a product to find the facility that makes it, the inputs one run takes, what one run gives and how long it takes. What each facility makes, and its power use, is on {prod}.",
              f"1.6 版所有的集成工業生產配方（不含裝填與清空容器），依產品的英文名稱排序：{np_} 種產品，共 {nr} 個配方。在頁面中搜尋產品名稱，即可找到製造它的設施、一次所需的原料、一次的產出與所需時間。各設施能做什麼與耗電量，見{prod}。",
              f"バージョン1.6の{J('AIC')}の生産レシピのうち、容器への充填と取り出しを除くすべてを、製品の英語名順に並べた。製品{np_}種、レシピ{nr}件である。ページ内で製品名を検索すると、作る{J('Facility')}、1回に使う原料、1回の産出、所要時間がわかる。各{J('Facility')}で作れるものと消費電力は{prod}にある。",
              f"1.6 버전 {K('AIC')} 생산 제작법 중 용기 충전과 비우기를 제외한 전부를 제품의 영어 이름순으로 정리했다. 제품 {np_}종, 제작법 {nr}개이다. 페이지에서 제품 이름을 검색하면 만드는 {K('Facility')}, 1회에 드는 재료, 1회 산출량, 소요 시간을 알 수 있다. 각 {K('Facility')}에서 만들 수 있는 것과 소비 전력은 {prod}에 있다."), '',
            L(f"The Filling Unit puts a fluid or gas into an empty bottle or canister ({n_fill} recipes), and the Separating Unit empties it again ({n_sep} recipes); a filled container keeps the container's name. Recipes of the Filling Unit that make something new, such as drinks, Canned Citrome and Buck Capsules, are in the table.",
              f"灌裝機把液體或氣體裝進空瓶或空罐（{n_fill} 個配方），拆解機再把它們清空（{n_sep} 個配方）；裝滿的容器沿用容器本身的名稱。灌裝機做出新東西的配方，例如瓶裝飲料、柑實罐頭與蕎癒膠囊，列在表中。",
              f"{fj}は液体や気体を空のボトルや缶に詰め（レシピ{n_fill}件）、{sj}はそれを再び空にする（レシピ{n_sep}件）。中身の入った容器は容器と同じ名前のままである。{fj}のレシピのうち、{J('Drinks')}、{citrome[JA]}、{buck[JA]}など新しいものを作るレシピは表に載せた。",
              f"{josa(fk, TOPIC)} 액체나 기체를 빈 병이나 캔에 채우고(제작법 {n_fill}개), {josa(sk, TOPIC)} 이를 다시 비운다(제작법 {n_sep}개). 내용물이 든 용기는 용기와 같은 이름을 쓴다. {fk} 제작법 중 {K('Drinks')}, {citrome[KO]}, {buck[KO]}처럼 새로운 것을 만드는 제작법은 표에 실었다."), '',
            L('## Recipes', '## 配方', '## レシピ', '## 제작법'), '',
            L('| Product | Made in | Inputs | Output | Time |', '| 產品 | 英文 | 設施 | 原料 | 產出 | 時間 |', f"| 製品 | 英語 | {J('Facility')} | 原料 | 産出 | 時間 |", f"| 제품 | 영어 | {K('Facility')} | 재료 | 산출 | 시간 |"),
            '| --- | --- | --- | --- | --- |' if lang == EN else '| --- | --- | --- | --- | --- | --- |']
    unit = L(' s', ' 秒', '秒', '초')
    for (ins, outs, secs), machines in rows:
        made = either.join(m[lang] for m in machines)
        inp = sep.join(f'{I(i)} ×{c}' for i, c in ins)
        outp = sep.join(f'{I(i)} ×{c}' for i, c in outs)
        main = outs[0][0]
        if lang == EN:
            out.append(f'| {I(main)} | {made} | {inp} | {outp} | {secs}{unit} |')
        else:
            out.append(f'| {I(main)} | {items[main][EN]} | {made} | {inp} | {outp} | {secs}{unit} |')
    write('aic', 'recipes', lang, out)


KIND_LABEL = {
    'mood-regen-all': {EN: 'Mood recovery of all operators', ZH: '所有幹員心情恢復', JA: f"全{J('Operators')}の{J('Mood')}回復", KO: f"모든 {K('Operators')}의 {K('Mood')} 회복"},
    'mood-drop-room': {EN: 'Slower mood drop in the room', ZH: '艙室內幹員心情消耗降低', JA: f"{J('Cabin')}内の{J('Mood')}消耗の軽減", KO: f"{K('Cabin')} 내 {K('Mood')} 소모 감소"},
    'make-operator-exp': {EN: 'Operator EXP materials, faster', ZH: '幹員經驗材料生產效率', JA: f"{J('Operators')}経験値素材の製造効率", KO: f"{K('Operators')} 경험치 재료 생산 효율"},
    'make-weapon-exp': {EN: 'Weapon EXP materials, faster', ZH: '武器經驗材料生產效率', JA: f"{J('Weapon')}経験値素材の製造効率", KO: f"{K('Weapon')} 경험치 재료 생산 효율"},
    'grow-plant': {EN: 'Vitrified plants, faster', ZH: '晶植材料培養速度', JA: '晶植素材の培養速度', KO: '결정화 식물 재료 육성 속도'},
    'grow-fungus': {EN: 'Fungal matter, faster', ZH: '菌類材料培養速度', JA: '菌類素材の培養速度', KO: '버섯 재료 육성 속도'},
    'grow-mineral': {EN: 'Rare minerals, faster', ZH: '礦物材料培養速度', JA: '鉱物素材の培養速度', KO: '광물 재료 육성 속도'},
    'clue-speed': {EN: 'Clue collection, faster', ZH: '線索收集效率', JA: f"{J('Clues')}の捜索速度", KO: f"{K('Clues')} 수집 효율"},
    'clue-chance': {EN: 'Chance of one clue', ZH: '特定線索的機率', JA: f"特定の{J('Clues')}の入手確率", KO: f"특정 {K('Clues')} 획득 확률"},
}
ROOM_ORDER = ['control', 'manufacturing', 'growth', 'reception']


def dijiang(lang):
    L = chooser(lang)
    rooms = bp.BASE['rooms']
    R = lambda k: rooms[k][lang]  # noqa: E731
    titles = {EN: 'Dijiang', ZH: '帝江號', CN: '帝江号', JA: J('Dijiang'), KO: K('Dijiang')}
    dj, dk = J('Dijiang'), K('Dijiang')
    cab_j, cab_k, mood_j, mood_k = J('Cabin'), K('Cabin'), J('Mood'), K('Mood')
    asg_j, asg_k, bs_j, bs_k = J('Assign'), K('Assign'), J('Base Skill'), K('Base Skill')
    clue_j, clue_k = J('Clues'), K('Clues')
    desc = L("Dijiang, the base ship of Arknights: Endfield: its rooms, operator assignments, mood, and base skills by room.",
             '《明日方舟：終末地》的基地飛船帝江號：艙室、幹員進駐、心情，以及各艙室的後勤技能。',
             f"{GAME[JA]}の拠点となる船、{dj}の{cab_j}、オペレーターの{asg_j}、{mood_j}、{cab_j}ごとの{bs_j}。",
             f"{GAME[KO]}의 기지 함선 {dk}: {cab_k}, 오퍼레이터 {asg_k}, {mood_k}, {cab_k}별 {bs_k}.")
    caveat = L("An assigned operator loses mood over time; at zero mood they leave to rest in the Central Ring and give no effect until their mood is full again. Base skills unlock at promotions, so an operator below Promotion I has none.",
               '進駐的幹員會隨時間消耗心情；心情耗盡時會前往中央環廳休息，在心情恢復滿之前不提供進駐效果。後勤技能隨精英化解鎖，未精英化的幹員沒有後勤技能。',
               f"{asg_j}されたオペレーターは時間とともに{mood_j}を消耗する。{mood_j}が0になると{J('Central Ring')}で休み、{mood_j}が満タンに戻るまで効果を出さない。{bs_j}は昇進で解放されるため、{J('Promotion I')}未満のオペレーターには{bs_j}がない。",
               f"{asg_k}된 오퍼레이터는 시간이 지나면 {josa(mood_k, OBJ)} 소모한다. {josa(mood_k, SUBJ)} 0이 되면 {K('Central Ring')}에서 쉬며, {josa(mood_k, SUBJ)} 가득 찰 때까지 효과를 주지 않는다. {josa(bs_k, TOPIC)} 정예화로 잠금 해제되므로, {K('Promotion I')} 미만인 오퍼레이터에게는 {josa(bs_k, SUBJ)} 없다.")
    sources = [(L('In-game tutorials on Dijiang, WikiTutorialPageTable (game data 1.6)', '遊戲內教學「帝江號」，WikiTutorialPageTable（遊戲資料 1.6）',
                  f"ゲーム内チュートリアル「{dj}」、WikiTutorialPageTable（ゲームデータ 1.6）", f"게임 내 튜토리얼 「{dk}」, WikiTutorialPageTable(게임 데이터 1.6)"),
                bp.GAME_TABLES[0].replace('/tree/', '/blob/') + '/WikiTutorialPageTable.json'),
               (bp.GAME_TABLES[1][lang], bp.GAME_TABLES[0])]
    out = front(lang, titles, desc, L('Arknights: Endfield, global service, Version 1.6; tutorials and base skills from game data 1.6', '《明日方舟：終末地》國際版，1.6 版；教學與後勤技能出自遊戲資料 1.6',
                                      f"{GAME[JA]}グローバル版、バージョン1.6。チュートリアルと{bs_j}はゲームデータ 1.6 による", f"{GAME[KO]} 글로벌 서비스, 1.6 버전. 튜토리얼과 {bs_k}은 게임 데이터 1.6 기준"),
                caveat, TODAY, sources)
    ops = bp.BASE['operators']
    n_ops = len(ops)
    em_j, em_k = J('Endministrator'), K('Endministrator')
    out += [L(f"Dijiang is the Endministrator's ship and the base of Arknights: Endfield. Operators assigned to its rooms make progression materials, grow plants, fungi and minerals, collect clues and build trust while the player is elsewhere. Each room needs at least one operator to work, and every operator assigned raises its output. {n_ops} of the 34 operators have base skills that add to one room; the Endministrator has none.",
              f"帝江號是管理員的飛船，也是《明日方舟：終末地》的基地。進駐艙室的幹員會在玩家不在時製造培養材料、培養晶植、菌類與礦物、收集線索並累積信賴值。功能艙室至少要進駐 1 名幹員才能運轉，每多進駐一名幹員，艙室的生產效能就提升。34 名幹員中有 {n_ops} 名擁有加成某個艙室的後勤技能；管理員沒有。",
              f"{dj}は{em_j}の船で、{GAME[JA]}の拠点である。{cab_j}に{asg_j}されたオペレーターは、プレイヤーが他の場所にいる間も育成素材を作り、植物・菌類・鉱物を培養し、{clue_j}を集め、{J('Trust')}を積み上げる。各{cab_j}が稼働するには1人以上の{asg_j}が必要で、{asg_j}する人数が増えるほど生産量が上がる。34人のオペレーターのうち{n_ops}人は、いずれかの{cab_j}を強化する{bs_j}を持つ。{em_j}は持たない。",
              f"{josa(dk, TOPIC)} {em_k}의 함선이자 {GAME[KO]}의 기지이다. {cab_k}에 {asg_k}된 오퍼레이터는 플레이어가 다른 곳에 있는 동안에도 육성 재료를 만들고, 식물·버섯·광물을 육성하며, {josa(clue_k, OBJ)} 모으고 {josa(K('Trust'), OBJ)} 쌓는다. 각 {josa(cab_k, TOPIC)} 1명 이상 {asg_k}되어야 가동되며, {asg_k}된 인원이 늘수록 생산량이 오른다. 오퍼레이터 34명 중 {n_ops}명은 특정 {josa(cab_k, OBJ)} 강화하는 {josa(bs_k, OBJ)} 가지고 있다. {josa(em_k, TOPIC)} 없다."), '',
            L('## Rooms', '## 艙室', f'## {cab_j}', f'## {cab_k}'), '',
            L('| Room | What it does | Base skills that work there |', '| 艙室 | 用途 | 在此生效的後勤技能 |', f"| {cab_j} | 役割 | ここで効果を発揮する{bs_j} |", f"| {cab_k} | 역할 | 여기서 효과가 있는 {bs_k} |"), '| --- | --- | --- |']
    kinds_in = {}
    for o in ops.values():
        for sk in o:
            kinds_in.setdefault(sk['room'], [])
            if sk['kind'] not in kinds_in[sk['room']]:
                kinds_in[sk['room']].append(sk['kind'])
    trust_j, trust_k = J('Trust'), K('Trust')
    what = {
        'control': L("Manages the whole ship and every room's assignments. Its level decides how many rooms can be built and how far they can be upgraded. Operators assigned here gain trust over time, also while the player is away.",
                     '管理整艘飛船與所有艙室的進駐。它的等級決定能建造多少艙室、艙室能升到幾級。進駐這裡的幹員會隨時間累積信賴值，玩家不在帝江號時也會累積。',
                     f"船全体とすべての{cab_j}の{asg_j}を管理する。そのレベルで、建てられる{cab_j}の数と、{cab_j}を上げられるレベルが決まる。ここに{asg_j}されたオペレーターは、プレイヤーがいない間も時間とともに{trust_j}が上がる。",
                     f"함선 전체와 모든 {cab_k}의 {josa(asg_k, OBJ)} 관리한다. 레벨에 따라 지을 수 있는 {cab_k} 수와 {cab_k}의 최대 레벨이 정해진다. 여기에 {asg_k}된 오퍼레이터는 플레이어가 없는 동안에도 시간이 지나면 {josa(trust_k, SUBJ)} 오른다."),
        'manufacturing': L('Makes operator and weapon progression materials over time from a chosen MFG Plan. Each item takes part of the room\'s MFG Load, which caps how many can be queued.',
                           '依選定的製造方案，隨時間製造幹員與武器的培養材料。每個物品占用艙室的一部分製造載荷，載荷決定一次能排多少。',
                           f"選んだ{J('MFG Plan')}に従い、オペレーターと武器の育成素材を時間とともに製造する。各アイテムは{cab_j}の{J('MFG Load')}の一部を使い、{J('MFG Load')}が予約できる数の上限になる。",
                           f"선택한 {K('MFG Plan')}에 따라 오퍼레이터와 무기의 육성 재료를 시간에 걸쳐 제작한다. 각 아이템은 {cab_k}의 {K('MFG Load')} 일부를 차지하며, {josa(K('MFG Load'), SUBJ)} 한 번에 예약할 수 있는 수의 상한이다."),
        'growth': L('Grows materials for promotions, skill upgrades and weapon tuning. Growing needs seed materials, extracted from existing materials, which uses those up.',
                    '培養幹員突破、技能提升與武器進階用的材料。培養需要基核，基核從原有材料中提取，提取會消耗原有材料。',
                    f"昇進、スキル強化、{J('Weapon Tuning')}に使う素材を培養する。培養には元の素材から抽出する基核が必要で、抽出すると元の素材は消費される。",
                    f"정예화, 스킬 강화, {K('Weapon Tuning')}에 쓰는 재료를 육성한다. 육성에는 기존 재료에서 추출하는 재배 코어가 필요하며, 추출하면 기존 재료가 소모된다."),
        'reception': L('Operators here collect clues and earn credits over time. A full set of clue types starts a Clue Exchange; clues can be given to and received from friends.',
                       '進駐的幹員隨時間收集線索並獲得信用。集齊所有類型的線索可開展情報交流；線索可以贈予好友，也可以接收。',
                       f"ここのオペレーターは時間とともに{clue_j}を集め、{J('Credits')}を得る。{clue_j}の種類がすべてそろうと{J('Clue Exchange')}を始められる。{clue_j}はフレンドに贈ることも、受け取ることもできる。",
                       f"이곳의 오퍼레이터는 시간이 지나면 {josa(clue_k, OBJ)} 모으고 {josa(K('Credits'), OBJ)} 얻는다. {clue_k} 종류를 모두 모으면 {josa(K('Clue Exchange'), OBJ)} 시작할 수 있다. {josa(clue_k, TOPIC)} 친구에게 줄 수도, 받을 수도 있다."),
    }
    sep = L('; ', '；', '、', ', ')
    for k in ROOM_ORDER:
        out.append(f"| {R(k)} | {what[k]} | {sep.join(KIND_LABEL[x][lang] for x in kinds_in.get(k, []))} |")
    sa_j, sb_j, sa_k, sb_k = J('Shift A'), J('Shift B'), K('Shift A'), K('Shift B')
    out += ['', L('## Mood, shifts and upgrades', '## 心情、輪班與升級', f'## {mood_j}、シフト、アップグレード', f'## {mood_k}, 근무조, 업그레이드'), '',
            L("- Operators assigned to a working room lose mood over time. At zero mood an operator goes to the Central Ring to rest and gives no assignment effect; at full mood they return to the room by themselves.",
              '- 進駐功能艙室的幹員會隨時間消耗心情。心情耗盡時幹員前往中央環廳休息，期間不提供進駐效果；心情恢復滿後會自動回到艙室。',
              f"- 稼働中の{cab_j}に{asg_j}されたオペレーターは、時間とともに{mood_j}を消耗する。{mood_j}が0になると{J('Central Ring')}へ休みに行き、その間は{asg_j}の効果がない。{mood_j}が満タンになると自分で{cab_j}に戻る。",
              f"- 가동 중인 {cab_k}에 {asg_k}된 오퍼레이터는 시간이 지나면 {josa(mood_k, OBJ)} 소모한다. {josa(mood_k, SUBJ)} 0이 되면 {josa(K('Central Ring'), TO)} 쉬러 가며, 그동안은 {asg_k} 효과가 없다. {josa(mood_k, SUBJ)} 가득 차면 스스로 {josa(cab_k, TO)} 돌아온다."),
            L('- Each room can hold two shifts of operators, A and B. Shifts can be switched by hand or rotated on a schedule.',
              '- 每個艙室可以設定 A、B 兩個小組，可手動換班，也可依設定的時段自動輪換。',
              f"- 各{cab_j}には{sa_j}と{sb_j}の2組を設定できる。シフトは手動で切り替えるか、設定した時間帯で自動的に交代させられる。",
              f"- 각 {cab_k}에는 {josa(sa_k, AND)} {sb_k} 두 조를 설정할 수 있다. 근무조는 직접 바꾸거나, 정한 시간대에 따라 자동으로 교대할 수 있다."),
            L('- Leveling up the Control Nexus opens more space for new rooms and raises the level cap of some rooms. An upgraded room holds more operators and unlocks more production. Building and upgrading take Aerospace Materials, gathered regularly from Recycling Stations across Talos-II.',
              '- 提升總控中樞等級會開放更多空間建造艙室，並提高部分艙室的等級上限。升級後的艙室可進駐更多幹員，並解鎖更多生產內容。建造與升級需要航太建材，可定期從各地的資源回收站收取。',
              f"- {J('Control Nexus')}のレベルを上げると、新しい{cab_j}を建てる場所が増え、一部の{cab_j}のレベル上限が上がる。強化した{cab_j}にはより多くのオペレーターを{asg_j}でき、生産できるものも増える。建設と強化には{J('Aerospace Material')}が必要で、{J('Talos-II')}各地の{J('Recycling Station')}から定期的に受け取れる。",
              f"- {K('Control Nexus')}의 레벨을 올리면 새 {josa(cab_k, OBJ)} 지을 공간이 늘고, 일부 {cab_k}의 레벨 상한이 오른다. 강화한 {cab_k}에는 더 많은 오퍼레이터를 {asg_k}할 수 있고, 생산할 수 있는 것도 늘어난다. 건설과 강화에는 {josa(K('Aerospace Material'), SUBJ)} 필요하며, {K('Talos-II')} 각지의 {K('Recycling Station')}에서 정기적으로 받을 수 있다."),
            L("- Credits come from clue collection, Clue Exchange, Production Assists in friends' rooms and delivery jobs for friends.",
              '- 信用來自線索收集、情報交流、對好友艙室的生產助力，以及幫好友完成運送委託。',
              f"- {J('Credits')}は、{clue_j}の収集、{J('Clue Exchange')}、フレンドの{cab_j}での{J('Production Assist')}、フレンドのための配送依頼で得られる。",
              f"- {josa(K('Credits'), TOPIC)} {clue_k} 수집, {K('Clue Exchange')}, 친구 {cab_k}에서의 {K('Production Assist')}, 친구를 위한 운송 의뢰로 얻는다."), '',
            L('## Base skills by room', '## 各艙室的後勤技能', f'## {cab_j}ごとの{bs_j}', f'## {cab_k}별 {bs_k}'), '',
            L("Which operators to assign to each room. Each base skill has two levels, unlocked at promotions; the second replaces the first. A clue skill does not stack with another of the same kind. Each operator's page lists their base skills under Base skills.",
              "各艙室適合進駐哪些幹員。每個後勤技能有兩級，隨精英化解鎖；第二級取代第一級。提升線索機率的技能，同類不疊加。各幹員頁的「後勤技能」列出該幹員的後勤技能。",
              f"各{cab_j}にどのオペレーターを{asg_j}するかの目安である。{bs_j}にはそれぞれ2段階あり、昇進で解放され、2段階目が1段階目に置き換わる。{clue_j}のスキルは同じ種類のものとは重複しない。各オペレーターのページの「{bs_j}」に、そのオペレーターの{bs_j}が載っている。",
              f"각 {cab_k}에 어떤 오퍼레이터를 {asg_k}할지 정리했다. {josa(bs_k, TOPIC)} 각각 2단계이고 정예화로 잠금 해제되며, 2단계가 1단계를 대체한다. {clue_k} 스킬은 같은 종류끼리 중첩되지 않는다. 각 오퍼레이터 페이지의 ‘{bs_k}’에 해당 오퍼레이터의 {josa(bs_k, SUBJ)} 나와 있다.")]

    def cell(sk, lv):
        stage = bp.stage_name(lv['promotion'], lang)
        if sk['kind'] == 'clue-chance':
            v = L('small rise' if lv['small'] else 'rise', '小幅提升' if lv['small'] else '提升', 'わずかに上昇' if lv['small'] else '上昇', '약간 증가' if lv['small'] else '증가')
        else:
            v = '+' + bp.percent(lv['value']) if sk['kind'] != 'mood-drop-room' else '−' + bp.percent(lv['value'])
        return L(f"{v}, {stage}", f"{v}，{stage}", f"{v}、{stage}", f"{v}, {stage}")
    for k in ROOM_ORDER:
        rows = []
        for slug, o in ops.items():
            for sk in o:
                if sk['room'] != k:
                    continue
                label = KIND_LABEL[sk['kind']][lang]
                if sk['kind'] == 'clue-chance':
                    c = sk['levels'][0]['clue']
                    label = L(f"Clue {c['number']}, {c['en']}", f"線索{c['number']}，{c['zh-TW']}", f"{clue_j}{c['number']}、{c[JA]}", f"{clue_k} {c['number']}, {c[KO]}")
                    order = (sk['kind'], c['number'], 0, slug)
                else:
                    order = (sk['kind'], '', -sk['levels'][-1]['value'], slug)
                rows.append((order, f"| {label} | {op_link(slug, lang)} | {sk['name'][lang]} | {cell(sk, sk['levels'][0])} | {cell(sk, sk['levels'][1])} |"))
        out += ['', f"### {R(k)}", '',
                L('| Effect | Operator | Skill | First level | Second level |', '| 效果 | 幹員 | 技能 | 第一級 | 第二級 |', '| 効果 | オペレーター | スキル | 1段階目 | 2段階目 |', '| 효과 | 오퍼레이터 | 스킬 | 1단계 | 2단계 |'),
                '| --- | --- | --- | --- | --- |']
        out += [r for _, r in sorted(rows)]
    write('systems', 'dijiang', lang, out)


ELEMENTS = ('physical', 'heat', 'electric', 'cryo', 'nature')


def enemies(lang):
    L = chooser(lang)
    rec = load('enemies.json')
    terms, areas, classes = rec['terms'], rec['areas'], rec['classes']
    # One row per name: the two forms of Marble Aggelomoirai share name and values.
    rows = {}
    for e in rec['enemies']:
        key = e['name'][EN]
        if key in rows:
            assert (rows[key]['resist'], rows[key]['class']) == (e['resist'], e['class']), key
            rows[key]['areas'] += [a for a in e['areas'] if a not in rows[key]['areas']]
        else:
            rows[key] = dict(e, areas=list(e['areas']))
    ens = sorted(rows.values(), key=lambda e: e['name'][EN].lower())
    n = len(ens)
    none = [e for e in ens if not any(e['resist'].values())]
    high = sorted([(v, k, e) for e in ens for k, v in e['resist'].items() if v >= 30], key=lambda x: (-x[0], ELEMENTS.index(x[1]), x[2]['name'][EN]))
    grades = rec['grades']

    def grade(v):
        return min((g for g in grades if g['taken'] >= 1 - v / 100 - 1e-9), key=lambda g: g['taken'])['grade']
    seen = {}
    for e in ens:
        for v in e['resist'].values():
            seen.setdefault(grade(v), set()).add(v)
    span = lambda g: L(' to ', ' 至 ', '〜', '~').join(map(str, (min(seen[g]), max(seen[g])))) if len(seen[g]) > 1 else str(min(seen[g]))  # noqa: E731
    used = [g['grade'] for g in reversed(grades) if g['grade'] in seen]
    unused = [g['grade'] for g in grades if g['grade'] not in seen]
    strip = {EN: ' Resistance', ZH: '抗性', JA: '耐性', KO: ' 저항'}[lang]
    elem = {k: terms[k][lang].replace(strip, '') for k in ELEMENTS}
    # The region of an area: Valley IV (map01) or Wuling (map02); an Energy Alluvium point by the
    # area it is named after; the Special Protocol Spaces are neither.
    by_name = {v[EN]: k for k, v in areas.items() if 'energy_point' not in k}

    def region(aid):
        if 'energy_point' in aid:
            aid = by_name[areas[aid][EN].split(': ', 1)[1].replace(' EZ', ' Exclusion Zone')]
        return next((m for m in ('map01', 'map02') if m in aid), None)

    def where(e):
        plain = [areas[a][lang] for a in e['areas'] if 'energy_point' not in a]
        alluvium = [re.split(r'\s*[·・]\s*', areas[a][lang].split(': ', 1)[-1], maxsplit=1)[-1] for a in e['areas'] if 'energy_point' in a]
        sep = bp.sep_of(lang)
        parts = [sep.join(plain)] if plain else []
        if alluvium:
            parts.append(L('Energy Alluvium: ', '能量淤積點：', f"{J('Energy Alluvium')}：", f"{K('Energy Alluvium')}: ") + sep.join(alluvium))
        return L('; ', '；', '／', '; ').join(parts) or '—'

    def regions(e):
        rs = sorted({r for r in map(region, e['areas']) if r})
        return L(' and ', '、', '、', ', ').join(terms[r][lang] for r in rs) or '—'
    titles = {EN: 'Enemy resistances', ZH: '敵人抗性', CN: '敌人抗性', JA: '敵の耐性', KO: '적 저항'}
    desc = L(f'Physical, Heat, Electric, Cryo and Nature resistances of all {n} enemies in Arknights: Endfield, by region.',
             f'《明日方舟：終末地》{n} 種敵人的物理、灼熱、電磁、寒冷、自然抗性與分布地區。',
             f"{GAME[JA]}の敵{n}種の{'・'.join(elem[k] for k in ELEMENTS)}耐性と分布地域。",
             f"{GAME[KO]} 적 {n}종의 {'·'.join(elem[k] for k in ELEMENTS)} 저항과 분포 지역.")
    caveat = L("The values are those of each enemy's base form, met in the open world. Some stage versions of an enemy have other resistances, for example 15 in every element.",
               '表中數值是各敵人基本型態的抗性，即在野外遇到的型態。部分關卡中的同名敵人抗性不同，例如五種屬性皆為 15。',
               '表の数値は各敵の基本形態、つまりフィールドで出会う形態の耐性である。ステージに出る同名の敵には、全属性15など別の耐性を持つものがある。',
               '표의 수치는 각 적의 기본 형태, 즉 필드에서 만나는 형태의 저항이다. 스테이지에 나오는 같은 이름의 적 중에는 모든 속성 15처럼 저항이 다른 경우가 있다.')
    sources = [(bp.GAME_TABLES[1][lang], bp.GAME_TABLES[0])]
    out = front(lang, titles, desc, L('Arknights: Endfield, global service, game data 1.6', '《明日方舟：終末地》國際版，遊戲資料 1.6',
                                      f"{GAME[JA]}グローバル版、ゲームデータ 1.6", f"{GAME[KO]} 글로벌 서비스, 게임 데이터 1.6"),
                caveat, TODAY, sources)
    top = high[0]
    combat = L(link(EN, 'Combat', 'systems/combat'), link(ZH, '戰鬥', 'systems/combat'), link(JA, J('Combat'), 'systems/combat'), link(KO, K('Combat'), 'systems/combat'))
    out += [L(f"Each point of resistance cuts damage of that element by 1% (see {combat}). The game shows each resistance as a grade; among enemies {', '.join(f'{g} is {span(g)}' for g in used)}, and no enemy has {' or '.join(unused)}. Of the {n} enemies in the in-game encyclopedia, {len(none)} have no resistance; most of the others have 20 in two to five elements. The highest is {top[2]['name'][EN]}'s Physical Resistance of {top[0]}. No enemy resists Æther damage.",
              f"每 1 點抗性使該屬性的傷害降低 1%（見{combat}）。遊戲內以等級顯示抗性；敵人的抗性中，{'，'.join(f'{g} 為 {span(g)}' for g in used)}，沒有敵人達到 {' 或 '.join(unused)}。遊戲內圖鑑的 {n} 種敵人中，{len(none)} 種沒有任何抗性；其餘大多在二到五種屬性上各有 20 點。最高的是{top[2]['name'][ZH]}的物理抗性 {top[0]}。沒有敵人具有超域抗性。",
              f"耐性1ポイントごとに、その属性のダメージが1%減る（{combat}を参照）。ゲーム内では耐性を等級で表示する。敵の耐性では{'、'.join(f'{g}が{span(g)}' for g in used)}で、{'と'.join(unused)}の敵はいない。ゲーム内図鑑の敵{n}種のうち{len(none)}種は耐性を持たず、残りの多くは2〜5属性に20ずつ持つ。最も高いのは{top[2]['name'][JA]}の{terms[top[1]][JA]}{top[0]}である。{J('Æther Resistance')}を持つ敵はいない。",
              f"저항 1포인트마다 해당 속성 피해가 1% 줄어든다({combat} 참조). 게임에서는 저항을 등급으로 표시한다. 적의 저항 중 {', '.join(f'{josa(g, TOPIC)} {span(g)}' for g in used)}이며, {' 또는 '.join(unused)} 등급인 적은 없다. 게임 내 도감의 적 {n}종 중 {len(none)}종은 저항이 없고, 나머지는 대부분 2~5개 속성에 20씩 있다. 가장 높은 것은 {top[2]['name'][KO]}의 {terms[top[1]][KO]} {josa(str(top[0]), COP)}. {josa(K('Æther Resistance'), SUBJ)} 있는 적은 없다."), '',
            L('## Highest resistances', '## 抗性最高的敵人', '## 耐性が最も高い敵', '## 저항이 가장 높은 적'), '',
            L('Every enemy with a resistance of 30 or more, with all five of its resistances (grade and value):', '有任一抗性達 30 以上的敵人，列出其全部五種抗性（等級與數值）：',
              '耐性が30以上の敵を、5つの耐性すべて（等級と数値）とともに挙げる：', '저항이 30 이상인 적을 다섯 가지 저항 모두(등급과 수치)와 함께 실었다:'), '',
            '| ' + ' | '.join([L('Enemy', '敵人', J('Enemies'), K('Enemies'))] + [elem[k] for k in ELEMENTS]) + ' |', '| ' + ' | '.join(['---'] * 6) + ' |']
    seen_hi = []
    for v, k, e in high:
        if e['name'][EN] not in seen_hi:
            seen_hi.append(e['name'][EN])
            out.append('| ' + ' | '.join([e['name'][lang]] + [f"{grade(e['resist'][x])} ({e['resist'][x]})" for x in ELEMENTS]) + ' |')
    order = [classes[c][lang] for c in ('0', '3', '1', '4', '2')]
    out += ['', L('## All enemies', '## 所有敵人', f"## すべての{J('Enemies')}", f"## 모든 {K('Enemies')}"), '',
            L("Sorted by English name. Each resistance is given as grade and value. Class is the game's own: Common, Advanced, Elite, Alpha, Boss.",
              f"依英文名稱排序。抗性寫成等級與數值。類型為遊戲內的分類：{'、'.join(order)}。",
              f"英語名順に並べた。耐性は等級と数値で示す。クラスはゲーム内の分類で、{'、'.join(order)}がある。",
              f"영어 이름순으로 정리했다. 저항은 등급과 수치로 표시한다. 분류는 게임 내 분류로, {', '.join(order[:-1] + [josa(order[-1], SUBJ)])} 있다."), '',
            ]
    # One table per region (Valley IV, Wuling, both, neither), so that no single block outweighs
    # the answer for a readability-style extractor, and a reader finds a region at once.
    def rkey(e):
        rs = sorted({r for r in map(region, e['areas']) if r})
        return (len(rs) == 0, len(rs), rs)
    groups = {}
    for e in ens:
        groups.setdefault(tuple(map(str, rkey(e))), []).append(e)
    for key in sorted(groups, key=lambda k: (k[0] == 'True', int(k[1]), k[2])):
        rows = groups[key]
        label = regions(rows[0]) if key[0] == 'False' else L('Other areas', '其他地點', 'その他の場所', '기타 장소')
        out += [f"### {label}", '',
                '| ' + ' | '.join([L('Enemy', '敵人', J('Enemies'), K('Enemies')), L('Class', '類型', 'クラス', '분류')] + [elem[k] for k in ELEMENTS] + [L('Where found', '分布', '分布', '분포')]) + ' |',
                '| ' + ' | '.join(['---'] * 8) + ' |']
        for e in rows:
            nm = L(e['name'][EN], f"{e['name'][ZH]}（{e['name'][EN]}）", f"{e['name'][JA]}（{e['name'][EN]}）", f"{e['name'][KO]}({e['name'][EN]})")
            out.append('| ' + ' | '.join([nm, classes[e['class']][lang]] + [f"{grade(e['resist'][k])} ({e['resist'][k]})" for k in ELEMENTS] + [where(e)]) + ' |')
        out.append('')
    out.pop()
    write('systems', 'enemies', lang, out)


if __name__ == '__main__':
    for lang in LANGS:
        names(lang)
        weapons(lang)
        dijiang(lang)
        recipes(lang)
        enemies(lang)
    print('names, weapons, dijiang, recipes, enemies written in', ', '.join(LANGS))
