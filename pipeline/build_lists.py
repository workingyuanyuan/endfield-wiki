"""Write the lookup pages that come from records: banner history, names, weapons.

Usage: python3 -I pipeline/build_lists.py
Reads records/ only and writes src/content/docs/systems/{banner-history,names,weapons}.md
in English and Traditional Chinese. Do not edit those pages by hand.
"""
import os
import sys
from collections import Counter

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import build_pages as bp  # noqa: E402
from build_pages import EN, ZH, OPS, ALL, CHARTERED, STANDARD6, TYPE, TODAY, VERSIONS, load, quote  # noqa: E402

CN = 'zh-CN'
WEAPONS = load('weapons.json')
# A record whose id is another weapon's id plus a suffix (wpn_sword_0021_ink) is a second
# model of that weapon: same name, rarity and stats in the game tables (checked 2026-11-22
# against WeaponBasicTable and ItemTable of rmxlinux/EndfieldData). It is one weapon.
_ids = {w['id'] for w in WEAPONS}
WEAPONS = [w for w in WEAPONS if not any(w['id'].startswith(i + '_') for i in _ids)]


def front(lang, title, desc, applies, caveat, effective, aliases, sources):
    limit = 110 if lang == EN else 70
    assert len(desc) <= limit, (title, len(desc), desc)
    fm = ['---', f'title: {quote(title)}', f'description: {quote(desc)}', f'appliesTo: {quote(applies)}', f'caveat: {quote(caveat)}',
          f'lastVerified: {TODAY}', f'effectiveDate: {effective}', 'aliases:'] + [f'  - {quote(a)}' for a in aliases] + ['sources:']
    for t, u in sources:
        fm += [f'  - title: {quote(t)}', f'    url: {u}']
    return fm + ['---', '']


def write(section, slug, lang, lines):
    folder = os.path.join(bp.DOCS, '' if lang == EN else 'zh-tw', section)
    os.makedirs(folder, exist_ok=True)
    open(os.path.join(folder, slug + '.md'), 'w', encoding='utf8').write('\n'.join(lines) + '\n')


def op_link(slug, lang):
    pre = '' if lang == EN else '/zh-tw'
    return f"[{OPS[slug]['name'][lang]}]({pre}/operators/{slug}/)"


def banner_history(lang):
    L = lambda en, zh: en if lang == EN else zh  # noqa: E731
    # The rule the page states, checked on the records: every rate-up operator is in exactly
    # three Chartered pools counted from its own banner, and in none after them.
    for i, b in enumerate(CHARTERED):
        later = [j for j, x in enumerate(CHARTERED) if b['rateUp'] in x['sixStars'] and j >= i]
        assert later == list(range(i, min(i + 3, len(CHARTERED)))), b['id']
    open_now = [b for b in ALL if bp.is_open(b)]
    title = L('Headhunting banner history: every banner, dates and pools', '尋訪歷史：每一期尋訪、時間與名單')
    alias = L('尋訪歷史：每一期尋訪、時間與名單', 'Headhunting banner history: every banner, dates and pools')
    desc = L(f'All {len(ALL)} headhunting banners of Arknights: Endfield from release to Version 1.6, with dates and 6-star pools.',
             f'《明日方舟：終末地》公測至 1.6 版的 {len(ALL)} 期尋訪，含時間與 6 星名單。')
    caveat = L('Times are server time: UTC+8 on the Asia server and UTC-5 on the Americas / Europe server. warfarin.wiki dates the first banner, Scars of the Forge, from 2025-12-09; on the global service it opened with the release on 2026-01-22.',
               '時間為伺服器時間：Asia 伺服器是 UTC+8，Americas / Europe 伺服器是 UTC-5。warfarin.wiki 把第一期尋訪「熔火灼痕」記為 2025-12-09 開始；國際版是隨 2026-01-22 公測開放的。')
    sources = [(L(f"{b['name'][EN]} {TYPE[b['type']][EN]}", f"{bp.bname(b, ZH)}{TYPE[b['type']][ZH]}說明"), f"https://endfield.gryphline.com/en-us/news/{b['notice']}") for b in ALL]
    sources.append((L('warfarin.wiki, Laevatain (banner dates in game data 1.6)', 'warfarin.wiki 萊萬汀頁（遊戲資料 1.6 的尋訪日期）'), 'https://warfarin.wiki/en/operators/laevatain'))
    out = front(lang, title, desc, L('Arknights: Endfield, global service, release (2026-01-22) to Version 1.6', '《明日方舟：終末地》國際版，公測（2026-01-22）至 1.6 版'),
                caveat, max(b['noticeDate'] for b in ALL), [alias, '寻访历史：每一期寻访、时间与名单'], sources)
    n_ch = len(CHARTERED)
    o = open_now[0]
    out += [L(f"From release to {TODAY} the global service has had {len(ALL)} operator headhunting banners: {n_ch} Chartered Headhunting, 2 RE-Factor Headhunting and 1 Special Headhunting. On {TODAY} one is open: {o['name'][EN]}, with {OPS[o['rateUp']]['name'][EN]} as the rate-up operator.",
              f"從公測到 {TODAY}，國際版共有 {len(ALL)} 期幹員尋訪：{n_ch} 期特許尋訪、2 期重構尋訪、1 期特殊尋訪。{TODAY} 開放中的只有{bp.bname(o, ZH)}，機率提升幹員是{OPS[o['rateUp']]['name'][ZH]}。"), '',
            L('## All banners', '## 所有尋訪'), '',
            L('Opening and closing times are server time. A banner that opens with a version update opens when that maintenance ends.', '開放與結束時間為伺服器時間。隨版本更新開放的尋訪，在該次維護結束時開放。'), '',
            L('| Banner | Chinese name | Version | Type | Rate-up | Opens | Ends |', '| 尋訪 | 英文名稱 | 版本 | 類型 | 機率提升 | 開放 | 結束 |'),
            '| --- | --- | --- | --- | --- | --- | --- |']
    for b in ALL:
        up = op_link(b['rateUp'], lang) if b['rateUp'] else L('None', '無')
        other = b['name'][ZH] if lang == EN else b['name'][EN]
        out.append(f"| {b['name'][lang]} | {other} | {b['version']} | {TYPE[b['type']][lang]} | {up} | {bp.point(b['opens'], lang)} | {bp.point(b['closes'], lang)} |")
    out += ['', L('## 6-star operators in each pool', '## 每期尋訪的 6 星名單'), '',
            L('| Banner | 6-star operators that can appear |', '| 尋訪 | 可能出現的 6 星幹員 |'), '| --- | --- |']
    sep = L(', ', '、')
    for b in ALL:
        out.append(f"| {b['name'][lang]} | {sep.join(OPS[s]['name'][lang] for s in b['sixStars'])} |")
    five = bp.list_names(STANDARD6, lang)
    out += ['', L('## How the Chartered pool rotates', '## 特許尋訪名單如何輪替'), '',
            L(f"A rate-up 6-star operator is in the pool of three Chartered Headhunting banners, its own included, then leaves and is not added to Basic Headhunting. All {n_ch} Chartered pools above follow this. Gilberta and Yvonne were also in the pools before their own banners: the three release banners listed the same three operators.",
              f"機率提升的 6 星幹員連同自己的那一期在內，會留在 3 期特許尋訪的名單內，之後移出名單，而且不會加入基礎尋訪。上表 {n_ch} 期特許尋訪的名單都符合這條規則。潔爾佩塔與伊馮在自己的那一期之前就已在名單內：公測的三期尋訪列出的是同樣三名幹員。"), '',
            L(f"Five 6-star operators are in every Chartered pool: {five}.", f"每一期特許尋訪名單都有的 6 星幹員共五名：{five}。"), '',
            L('| Rate-up operator | Own banner | Last Chartered banner in the pool |', '| 機率提升幹員 | 自己的那一期 | 留在名單內的最後一期 |'), '| --- | --- | --- |']
    for i, b in enumerate(CHARTERED):
        last_i = i + 2
        if last_i < len(CHARTERED):
            last = CHARTERED[last_i]['name'][lang]
        else:
            left = last_i - len(CHARTERED) + 1
            last = L(f"{left} more after {CHARTERED[-1]['name'][EN]}", f"{bp.bname(CHARTERED[-1], ZH)}之後還有 {left} 期")
        out.append(f"| {op_link(b['rateUp'], lang)} | {b['name'][lang]} | {last} |")
    out += ['', L('## Reruns and special banners', '## 復刻與特殊尋訪'), '',
            L('RE-Factor Headhunting brings back one earlier rate-up operator. Special Headhunting has had one banner, Fest of Brilliance, with four 6-star operators and a count of its own.',
              '重構尋訪讓一名過去的機率提升幹員再次登場。特殊尋訪至今只有「輝光慶典」一期，名單內有四名 6 星幹員，保底計數與其他尋訪分開。'), '',
            L('| Banner | Type | 6-star operators | Opens | Ends |', '| 尋訪 | 類型 | 6 星幹員 | 開放 | 結束 |'), '| --- | --- | --- | --- | --- |']
    for b in ALL:
        if b['type'] != 'chartered':
            out.append(f"| {b['name'][lang]} | {TYPE[b['type']][lang]} | {sep.join(OPS[s]['name'][lang] for s in b['sixStars'])} | {bp.point(b['opens'], lang)} | {bp.point(b['closes'], lang)} |")
    pre = '' if lang == EN else '/zh-tw'
    out += ['', L(f'Rates, guarantees and what carries over between banners are on [Headhunting]({pre}/systems/headhunting/). Weapon banners are on [Arsenal Exchange and Arsenal Issues]({pre}/systems/arsenal/).',
                  f'機率、保底與各期之間的繼承規則見[尋訪]({pre}/systems/headhunting/)；武器的申領見[武庫申領]({pre}/systems/arsenal/)。')]
    write('systems', 'banner-history', lang, out)


def distinct(rows):
    seen, out = set(), []
    for r in rows:
        if r[EN] not in seen:
            seen.add(r[EN])
            out.append(r)
    return out


def names(lang):
    L = lambda en, zh: en if lang == EN else zh  # noqa: E731
    pre = '' if lang == EN else '/zh-tw'
    title = L('Names in three scripts', '名稱對照')
    alias = L('名稱對照', 'Names in three scripts')
    desc = L('Operators, classes, elements, weapon types, attributes, factions and races of Endfield in three scripts.',
             '《明日方舟：終末地》幹員、職業、屬性、武器類型、陣營與種族的三種文字名稱。')
    caveat = L("Rossi is 洛西 in Traditional Chinese and 洛茜 in Simplified Chinese: a different character, not a conversion between scripts. The Simplified names are those of the game's own Simplified Chinese text.",
               '洛西的簡體中文名是洛茜，用字不同，不只是繁簡轉換。簡體中文名稱出自遊戲本身的簡體中文文字。')
    sources = [(L('Official operator list (Gryphline)', '官方幹員列表 (Gryphline)'), 'https://endfield.gryphline.com/en-us/operator'),
               (L('Official operator list, Simplified Chinese (Hypergryph)', '官方幹員列表，簡體中文 (Hypergryph)'), 'https://endfield.hypergryph.com/operator'),
               (L('warfarin.wiki, Operators (game data 1.6)', 'warfarin.wiki 幹員列表（遊戲資料 1.6）'), 'https://warfarin.wiki/en/operators')]
    out = front(lang, title, desc, L('Arknights: Endfield, global service, Version 1.6; names from game data 1.6 in three languages', '《明日方舟：終末地》國際版，1.6 版；名稱出自三種語言的遊戲資料 1.6'),
                caveat, TODAY, [alias, '名称对照'], sources)
    head = '| English | 繁體中文 | 簡體中文 |'
    out += [L(f'Names of weapons are on [Weapons list]({pre}/systems/weapons/); names of banners are on each [version page]({pre}/versions/), with the version titles.',
              f'武器名稱見[武器列表]({pre}/systems/weapons/)；尋訪名稱與版本標題見各[版本頁]({pre}/versions/)。'), '',
            L('## Operators', '## 幹員'), '', head, '| --- | --- | --- |']
    for slug in sorted(OPS):
        n = OPS[slug]['name']
        out.append(f"| [{n[EN]}]({pre}/operators/{slug}/) | {n[ZH]} | {n[CN]} |")
    ops = list(OPS.values())
    for key, en_h, zh_h in (('class', 'Classes', '職業'), ('element', 'Elements', '屬性'), ('weapon', 'Weapon types', '武器類型'),
                            ('faction', 'Factions', '陣營'), ('race', 'Races', '種族')):
        out += ['', L(f'## {en_h}', f'## {zh_h}'), '', head, '| --- | --- | --- |']
        for r in sorted(distinct([o[key] for o in ops]), key=lambda r: r[EN]):
            out.append(f"| {r[EN]} | {r[ZH]} | {r[CN]} |")
    attrs = distinct([o['mainAttr'] for o in ops] + [o['subAttr'] for o in ops])
    out += ['', L('## Attributes', '## 能力值'), '', head, '| --- | --- | --- |'] + [f"| {r[EN]} | {r[ZH]} | {r[CN]} |" for r in sorted(attrs, key=lambda r: r[EN])]
    promo = distinct([p['name'] for o in ops for p in o['promotions']])
    out += ['', L('## Promotion stages', '## 精英化階段'), '', head, '| --- | --- | --- |'] + [f"| {r[EN]} | {r[ZH]} | {r[CN]} |" for r in promo]
    write('systems', 'names', lang, out)


def weapons(lang):
    L = lambda en, zh: en if lang == EN else zh  # noqa: E731
    pre = '' if lang == EN else '/zh-tw'
    total = len(WEAPONS)
    title = L('Weapons list', '武器列表')
    alias = L('武器列表', 'Weapons list')
    desc = L(f'All {total} Arknights: Endfield weapons in Version 1.6: type, rarity, Essence stats and recommended operators.',
             f'《明日方舟：終末地》1.6 版的 {total} 把武器：類型、稀有度、基質詞條與推薦幹員。')
    fans = {}
    for slug, rec in bp.RECOMMEND['operators'].items():
        for wid in rec['weapons']:
            fans.setdefault(wid, []).append(slug)
    sep = L(', ', '、')
    caveat = L('Operator headhunting gives no weapons. Each pull gives Arsenal Tickets, which are spent on Arsenal Issues; 6-star weapons come from Arsenal Issues and the Arsenal Exchange.',
               '幹員尋訪不會出武器。每次尋訪會給武庫配額，用於武庫申領；6 星武器來自武庫申領與兌換。')
    sources = [(L('warfarin.wiki, Weapons (game data 1.6)', 'warfarin.wiki 武器列表（遊戲資料 1.6）'), 'https://warfarin.wiki/en/weapons'),
               (L('The Hearth Fire Beckons the Starry Flow Chartered Headhunting (Arsenal Tickets)', '「煙火邀星河」特許尋訪說明（武庫配額）'), 'https://endfield.gryphline.com/en-us/news/7012'),
               (bp.GAME_TABLES[1][lang], bp.GAME_TABLES[0])]
    out = front(lang, title, desc, L('Arknights: Endfield, global service, Version 1.6; list from game data 1.6', '《明日方舟：終末地》國際版，1.6 版；列表出自遊戲資料 1.6'),
                caveat, '2026-11-04', [alias], sources)
    types = []
    for w in WEAPONS:
        if w['type'][EN] not in [t[EN] for t in types]:
            types.append(w['type'])
    types.sort(key=lambda t: t[EN])
    count = Counter((w['type'][EN], w['rarity']) for w in WEAPONS)
    rar = sorted({w['rarity'] for w in WEAPONS}, reverse=True)
    out += [L(f'Version 1.6 has {total} weapons. An operator uses one weapon type, shown on the [operator pages]({pre}/operators/). How weapons are obtained, and how Essences raise weapon skills, is on [Arsenal and Essences]({pre}/systems/arsenal/). Each 4- to 6-star weapon has three Essence stats, an attribute, a secondary stat and a skill stat, and an Essence raises the weapon skill of each stat it carries; 3-star weapons have none. Recommended for lists the operators whose in-game recommendations include the weapon.',
              f'1.6 版共有 {total} 把武器。每名幹員只使用一種武器類型，見[各幹員頁]({pre}/operators/)。武器的取得方式與用基質提升武器技能，見[武庫申領與基質]({pre}/systems/arsenal/)。4 到 6 星武器各有三個基質詞條：能力值、副屬性與技能詞條，基質帶有哪個詞條，就提升對應的武器技能；3 星武器沒有基質詞條。「推薦幹員」列出遊戲推薦中包含這把武器的幹員。'), '',
            L('## Counts by type and rarity', '## 各類型與稀有度的數量'), '',
            '| ' + L('Type', '類型') + ' | ' + ' | '.join(L(f'{r}-star', f'{r} 星') for r in rar) + ' | ' + L('Total', '合計') + ' |',
            '| --- |' + ' --- |' * (len(rar) + 1)]
    for t in types:
        row = [count[(t[EN], r)] for r in rar]
        out.append(f"| {t[lang]} | " + ' | '.join(str(x) for x in row) + f' | {sum(row)} |')
    for t in types:
        out += ['', f"## {t[lang]}" if lang == ZH else f"## {t[EN]}", '',
                L(f"{t[EN]} is {t[ZH]} in Traditional Chinese and {t[CN]} in Simplified Chinese.", f"{t[ZH]}的英文是 {t[EN]}。"), '',
                '| English | 繁體中文 | 簡體中文 | ' + L('Rarity | Essence stats | Recommended for', '稀有度 | 基質詞條 | 推薦幹員') + ' |', '| --- | --- | --- | --- | --- | --- |']
        for w in WEAPONS:
            if w['type'][EN] == t[EN]:
                tags = bp.ESSENCE['weapons'].get(w['id'])
                stats = sep.join(bp.ESSENCE['stats'][x]['name'][lang] for x in tags) if tags else L('None', '無')
                assert tags or w['rarity'] == 3, w['id']
                who = sep.join(OPS[o]['name'][lang] for o in fans.get(w['id'], []))
                out.append(f"| {w['name'][EN]} | {w['name'][ZH]} | {w['name'][CN]} | {w['rarity']} | {stats} | {who} |")
    write('systems', 'weapons', lang, out)


def recipes(lang):
    L = lambda en, zh: en if lang == EN else zh  # noqa: E731
    pre = '' if lang == EN else '/zh-tw'
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
    title = L('Recipes by product', '依產品查配方')
    desc = L(f'Which AIC facility makes each of {len(products)} Arknights: Endfield products, from what inputs and how fast.',
             f'《明日方舟：終末地》{len(products)} 種集成工業產品由哪個設施製造、需要什麼原料、多快。')
    caveat = L('Times are per run of one facility. A product with several recipes is listed once per recipe; recipes that use event items are left out.',
               '時間是單一設施做一次的時間。有多個配方的產品，每個配方各列一行；使用活動道具的配方不列入。')
    sources = [(L('Recipe table FactoryMachineCraftTable (game data 1.6)', '配方表 FactoryMachineCraftTable（遊戲資料 1.6）'),
                bp.GAME_TABLES[0].replace('/tree/', '/blob/') + '/FactoryMachineCraftTable.json')]
    out = front(lang, title, desc, L('Arknights: Endfield, global service, Version 1.6; recipes from game data 1.6', '《明日方舟：終末地》國際版，1.6 版；配方出自遊戲資料 1.6'),
                caveat, TODAY, [L('依產品查配方', 'Recipes by product'), '依产品查配方'], sources)
    sep = L(', ', '、')
    either = L(' or ', '或')
    out += [L(f"Every AIC production recipe of Version 1.6 except filling and emptying containers, sorted by the English name of the product: {len(rows)} recipes for {len(products)} products. Search the page for a product to find the facility that makes it, the inputs one run takes, what one run gives and how long it takes. What each facility makes, and its power use, is on [Production and logistics]({pre}/aic/production/).",
              f"1.6 版所有的集成工業生產配方（不含裝填與清空容器），依產品的英文名稱排序：{len(products)} 種產品，共 {len(rows)} 個配方。在頁面中搜尋產品名稱，即可找到製造它的設施、一次所需的原料、一次的產出與所需時間。各設施能做什麼與耗電量，見[生產與物流]({pre}/aic/production/)。"), '',
            L(f"The Filling Unit puts a fluid or gas into an empty bottle or canister ({n_fill} recipes), and the Separating Unit empties it again ({n_sep} recipes); a filled container keeps the container's name. Recipes of the Filling Unit that make something new, such as drinks, Canned Citrome and Buck Capsules, are in the table.",
              f"灌裝機把液體或氣體裝進空瓶或空罐（{n_fill} 個配方），拆解機再把它們清空（{n_sep} 個配方）；裝滿的容器沿用容器本身的名稱。灌裝機做出新東西的配方，例如瓶裝飲料、柑實罐頭與蕎癒膠囊，列在表中。"), '',
            L('## Recipes', '## 配方'), '',
            L('| Product | Made in | Inputs | Output | Time |', '| 產品 | 英文 | 設施 | 原料 | 產出 | 時間 |'),
            '| --- | --- | --- | --- | --- |' if lang == EN else '| --- | --- | --- | --- | --- | --- |']
    for (ins, outs, secs), machines in rows:
        made = either.join(m[lang] for m in machines)
        inp = sep.join(f'{I(i)} ×{c}' for i, c in ins)
        outp = sep.join(f'{I(i)} ×{c}' for i, c in outs)
        main = outs[0][0]
        if lang == EN:
            out.append(f'| {I(main)} | {made} | {inp} | {outp} | {secs} s |')
        else:
            out.append(f'| {I(main)} | {items[main][EN]} | {made} | {inp} | {outp} | {secs} 秒 |')
    write('aic', 'recipes', lang, out)


KIND_LABEL = {
    'mood-regen-all': {EN: 'Mood recovery of all operators', ZH: '所有幹員心情恢復'},
    'mood-drop-room': {EN: 'Slower mood drop in the room', ZH: '艙室內幹員心情消耗降低'},
    'make-operator-exp': {EN: 'Operator EXP materials, faster', ZH: '幹員經驗材料生產效率'},
    'make-weapon-exp': {EN: 'Weapon EXP materials, faster', ZH: '武器經驗材料生產效率'},
    'grow-plant': {EN: 'Vitrified plants, faster', ZH: '晶植材料培養速度'},
    'grow-fungus': {EN: 'Fungal matter, faster', ZH: '菌類材料培養速度'},
    'grow-mineral': {EN: 'Rare minerals, faster', ZH: '礦物材料培養速度'},
    'clue-speed': {EN: 'Clue collection, faster', ZH: '線索收集效率'},
    'clue-chance': {EN: 'Chance of one clue', ZH: '特定線索的機率'},
}
ROOM_ORDER = ['control', 'manufacturing', 'growth', 'reception']


def dijiang(lang):
    L = lambda en, zh: en if lang == EN else zh  # noqa: E731
    pre = '' if lang == EN else '/zh-tw'
    rooms = bp.BASE['rooms']
    R = lambda k: rooms[k][lang]  # noqa: E731
    title = L('Dijiang', '帝江號')
    desc = L("Dijiang, the base ship of Arknights: Endfield: its rooms, operator assignments, mood, and base skills by room.",
             '《明日方舟：終末地》的基地飛船帝江號：艙室、幹員進駐、心情，以及各艙室的後勤技能。')
    caveat = L("An assigned operator loses mood over time; at zero mood they leave to rest in the Central Ring and give no effect until their mood is full again. Base skills unlock at promotions, so an operator below Promotion I has none.",
               '進駐的幹員會隨時間消耗心情；心情耗盡時會前往中央環廳休息，在心情恢復滿之前不提供進駐效果。後勤技能隨精英化解鎖，未精英化的幹員沒有後勤技能。')
    sources = [(L('In-game tutorials on Dijiang, WikiTutorialPageTable (game data 1.6)', '遊戲內教學「帝江號」，WikiTutorialPageTable（遊戲資料 1.6）'), bp.GAME_TABLES[0].replace('/tree/', '/blob/') + '/WikiTutorialPageTable.json'),
               (bp.GAME_TABLES[1][lang], bp.GAME_TABLES[0])]
    out = front(lang, title, desc, L('Arknights: Endfield, global service, Version 1.6; tutorials and base skills from game data 1.6', '《明日方舟：終末地》國際版，1.6 版；教學與後勤技能出自遊戲資料 1.6'),
                caveat, TODAY, [L('帝江號', 'Dijiang'), '帝江号'], sources)
    ops = bp.BASE['operators']
    n_ops = len(ops)
    out += [L(f"Dijiang is the Endministrator's ship and the base of Arknights: Endfield. Operators assigned to its rooms make progression materials, grow plants, fungi and minerals, collect clues and build trust while the player is elsewhere. Each room needs at least one operator to work, and every operator assigned raises its output. {n_ops} of the 34 operators have base skills that add to one room; the Endministrator has none.",
              f"帝江號是管理員的飛船，也是《明日方舟：終末地》的基地。進駐艙室的幹員會在玩家不在時製造培養材料、培養晶植、菌類與礦物、收集線索並累積信賴值。功能艙室至少要進駐 1 名幹員才能運轉，每多進駐一名幹員，艙室的生產效能就提升。34 名幹員中有 {n_ops} 名擁有加成某個艙室的後勤技能；管理員沒有。"), '',
            L('## Rooms', '## 艙室'), '',
            L('| Room | What it does | Base skills that work there |', '| 艙室 | 用途 | 在此生效的後勤技能 |'), '| --- | --- | --- |']
    kinds_in = {}
    for o in ops.values():
        for sk in o:
            kinds_in.setdefault(sk['room'], [])
            if sk['kind'] not in kinds_in[sk['room']]:
                kinds_in[sk['room']].append(sk['kind'])
    what = {
        'control': L("Manages the whole ship and every room's assignments. Its level decides how many rooms can be built and how far they can be upgraded. Operators assigned here gain trust over time, also while the player is away.",
                     '管理整艘飛船與所有艙室的進駐。它的等級決定能建造多少艙室、艙室能升到幾級。進駐這裡的幹員會隨時間累積信賴值，玩家不在帝江號時也會累積。'),
        'manufacturing': L('Makes operator and weapon progression materials over time from a chosen MFG Plan. Each item takes part of the room\'s MFG Load, which caps how many can be queued.',
                           '依選定的製造方案，隨時間製造幹員與武器的培養材料。每個物品占用艙室的一部分製造載荷，載荷決定一次能排多少。'),
        'growth': L('Grows materials for promotions, skill upgrades and weapon tuning. Growing needs seed materials, extracted from existing materials, which uses those up.',
                    '培養幹員突破、技能提升與武器進階用的材料。培養需要基核，基核從原有材料中提取，提取會消耗原有材料。'),
        'reception': L('Operators here collect clues and earn credits over time. A full set of clue types starts a Clue Exchange; clues can be given to and received from friends.',
                       '進駐的幹員隨時間收集線索並獲得信用。集齊所有類型的線索可開展情報交流；線索可以贈予好友，也可以接收。'),
    }
    sep = L('; ', '；')
    for k in ROOM_ORDER:
        out.append(f"| {R(k)} | {what[k]} | {sep.join(KIND_LABEL[x][lang] for x in kinds_in.get(k, []))} |")
    out += ['', L('## Mood, shifts and upgrades', '## 心情、輪班與升級'), '',
            L("- Operators assigned to a working room lose mood over time. At zero mood an operator goes to the Central Ring to rest and gives no assignment effect; at full mood they return to the room by themselves.",
              '- 進駐功能艙室的幹員會隨時間消耗心情。心情耗盡時幹員前往中央環廳休息，期間不提供進駐效果；心情恢復滿後會自動回到艙室。'),
            L('- Each room can hold two shifts of operators, A and B. Shifts can be switched by hand or rotated on a schedule.',
              '- 每個艙室可以設定 A、B 兩個小組，可手動換班，也可依設定的時段自動輪換。'),
            L('- Leveling up the Control Nexus opens more space for new rooms and raises the level cap of some rooms. An upgraded room holds more operators and unlocks more production. Building and upgrading take Aerospace Materials, gathered regularly from Recycling Stations across Talos-II.',
              '- 提升總控中樞等級會開放更多空間建造艙室，並提高部分艙室的等級上限。升級後的艙室可進駐更多幹員，並解鎖更多生產內容。建造與升級需要航太建材，可定期從各地的資源回收站收取。'),
            L("- Credits come from clue collection, Clue Exchange, Production Assists in friends' rooms and delivery jobs for friends.",
              '- 信用來自線索收集、情報交流、對好友艙室的生產助力，以及幫好友完成運送委託。'), '',
            L('## Base skills by room', '## 各艙室的後勤技能'), '',
            L(f"Which operators to assign to each room. Each base skill has two levels, unlocked at promotions; the second replaces the first. A clue skill does not stack with another of the same kind. Each operator's page lists their base skills under Base skills.",
              f"各艙室適合進駐哪些幹員。每個後勤技能有兩級，隨精英化解鎖；第二級取代第一級。提升線索機率的技能，同類不疊加。各幹員頁的「後勤技能」列出該幹員的後勤技能。")]
    def cell(sk, lv):
        stage = L(f"Promotion {bp.ROMAN[lv['promotion']]}", f"精英化{bp.ROMAN[lv['promotion']]}")
        if sk['kind'] == 'clue-chance':
            v = L('small rise' if lv['small'] else 'rise', '小幅提升' if lv['small'] else '提升')
        else:
            v = '+' + bp.percent(lv['value']) if sk['kind'] != 'mood-drop-room' else '−' + bp.percent(lv['value'])
        return f"{v}, {stage}" if lang == EN else f"{v}，{stage}"
    for k in ROOM_ORDER:
        rows = []
        for slug, o in ops.items():
            for sk in o:
                if sk['room'] != k:
                    continue
                label = KIND_LABEL[sk['kind']][lang]
                if sk['kind'] == 'clue-chance':
                    c = sk['levels'][0]['clue']
                    label = L(f"Clue {c['number']}, {c['en']}", f"線索{c['number']}，{c['zh-TW']}")
                    order = (sk['kind'], c['number'], 0, slug)
                else:
                    order = (sk['kind'], '', -sk['levels'][-1]['value'], slug)
                rows.append((order, f"| {label} | {op_link(slug, lang)} | {sk['name'][lang]} | {cell(sk, sk['levels'][0])} | {cell(sk, sk['levels'][1])} |"))
        out += ['', f"### {R(k)}", '',
                L('| Effect | Operator | Skill | First level | Second level |', '| 效果 | 幹員 | 技能 | 第一級 | 第二級 |'), '| --- | --- | --- | --- | --- |']
        out += [r for _, r in sorted(rows)]
    write('systems', 'dijiang', lang, out)


ELEMENTS = ('physical', 'heat', 'electric', 'cryo', 'nature')


def enemies(lang):
    L = lambda en, zh: en if lang == EN else zh  # noqa: E731
    pre = '' if lang == EN else '/zh-tw'
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
    span = lambda g: L(' to ', ' 至 ').join(map(str, (min(seen[g]), max(seen[g])))) if len(seen[g]) > 1 else str(min(seen[g]))  # noqa: E731
    used = [g['grade'] for g in reversed(grades) if g['grade'] in seen]
    unused = [g['grade'] for g in grades if g['grade'] not in seen]
    elem = {k: terms[k][lang].replace(' Resistance', '').replace('抗性', '') for k in ELEMENTS}
    # The region of an area: Valley IV (map01) or Wuling (map02); an Energy Alluvium point by the
    # area it is named after; the Special Protocol Spaces are neither.
    by_name = {v[EN]: k for k, v in areas.items() if 'energy_point' not in k}
    def region(aid):
        if 'energy_point' in aid:
            aid = by_name[areas[aid][EN].split(': ', 1)[1].replace(' EZ', ' Exclusion Zone')]
        return next((m for m in ('map01', 'map02') if m in aid), None)
    def where(e):
        plain = [areas[a][lang] for a in e['areas'] if 'energy_point' not in a]
        alluvium = [areas[a][lang].split(': ', 1)[-1].split('·', 1)[-1] for a in e['areas'] if 'energy_point' in a]
        parts = [L(', ', '、').join(plain)] if plain else []
        if alluvium:
            parts.append(L('Energy Alluvium: ', '能量淤積點：') + L(', ', '、').join(alluvium))
        return L('; ', '；').join(parts) or '—'
    def regions(e):
        rs = sorted({r for r in map(region, e['areas']) if r})
        return L(' and ', '、').join(terms[r][lang] for r in rs) or '—'
    title = L('Enemy resistances', '敵人抗性')
    desc = L(f'Physical, Heat, Electric, Cryo and Nature resistances of all {n} enemies in Arknights: Endfield, by region.',
             f'《明日方舟：終末地》{n} 種敵人的物理、灼熱、電磁、寒冷、自然抗性與分布地區。')
    caveat = L("The values are those of each enemy's base form, met in the open world. Some stage versions of an enemy have other resistances, for example 15 in every element.",
               '表中數值是各敵人基本型態的抗性，即在野外遇到的型態。部分關卡中的同名敵人抗性不同，例如五種屬性皆為 15。')
    sources = [(bp.GAME_TABLES[1][lang], bp.GAME_TABLES[0])]
    out = front(lang, title, desc, L('Arknights: Endfield, global service, game data 1.6', '《明日方舟：終末地》國際版，遊戲資料 1.6'),
                caveat, TODAY, [L('敵人抗性', 'Enemy resistances'), '敌人抗性'], sources)
    top = high[0]
    out += [L(f"Each point of resistance cuts damage of that element by 1% (see [Combat](/systems/combat/)). The game shows each resistance as a grade; among enemies {', '.join(f'{g} is {span(g)}' for g in used)}, and no enemy has {' or '.join(unused)}. Of the {n} enemies in the in-game encyclopedia, {len(none)} have no resistance; most of the others have 20 in two to five elements. The highest is {top[2]['name'][EN]}'s Physical Resistance of {top[0]}. No enemy resists Æther damage.",
              f"每 1 點抗性使該屬性的傷害降低 1%（見[戰鬥](/zh-tw/systems/combat/)）。遊戲內以等級顯示抗性；敵人的抗性中，{'，'.join(f'{g} 為 {span(g)}' for g in used)}，沒有敵人達到 {' 或 '.join(unused)}。遊戲內圖鑑的 {n} 種敵人中，{len(none)} 種沒有任何抗性；其餘大多在二到五種屬性上各有 20 點。最高的是{top[2]['name'][ZH]}的物理抗性 {top[0]}。沒有敵人具有超域抗性。"), '',
            L('## Highest resistances', '## 抗性最高的敵人'), '',
            L('Every resistance of 30 or more:', '抗性 30 以上的全部列出：'), '',
            L('| Enemy | Resistance | Grade | Value |', '| 敵人 | 抗性 | 等級 | 數值 |'), '| --- | --- | --- | --- |']
    out += [f"| {e['name'][lang]} | {terms[k][lang]} | {grade(v)} | {v} |" for v, k, e in high]
    out += ['', L('## All enemies', '## 所有敵人'), '',
            L(f"Sorted by English name. Each resistance is given as grade and value. Class is the game's own: Common, Advanced, Elite, Alpha, Boss.",
              f"依英文名稱排序。抗性寫成等級與數值。類型為遊戲內的分類：{'、'.join(classes[c][ZH] for c in ('0', '3', '1', '4', '2'))}。"), '',
            '| ' + ' | '.join([L('Enemy', '敵人'), L('Class', '類型')] + [elem[k] for k in ELEMENTS] + [L('Region', '地區'), L('Where found', '分布')]) + ' |',
            '| ' + ' | '.join(['---'] * 9) + ' |']
    for e in ens:
        name = e['name'][lang] if lang == EN else f"{e['name'][ZH]}（{e['name'][EN]}）"
        out.append('| ' + ' | '.join([name, classes[e['class']][lang]] + [f"{grade(e['resist'][k])} ({e['resist'][k]})" for k in ELEMENTS] + [regions(e), where(e)]) + ' |')
    write('systems', 'enemies', lang, out)


if __name__ == '__main__':
    for lang in (EN, ZH):
        names(lang)
        weapons(lang)
        dijiang(lang)
        recipes(lang)
        enemies(lang)
    print('names, weapons, dijiang, recipes, enemies written')
