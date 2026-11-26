"""Write the story pages: one page per operator with the game's own text of the operator's
files, voice lines and chats, and the story index, in all five languages.

Usage: python3 -I pipeline/build_story.py
Reads records/story/<slug>.json and records/story/terms.json (pipeline/story_extract.py)
and records/operators/, and writes src/content/docs/<lang>/story/. Simplified Chinese is
written here from the game's Simplified Chinese text, not converted from Traditional
Chinese: scripts/to-zh-cn.py leaves story/ alone. Do not edit the pages it writes.

The game's text is shown as the game gives it (owner decision, 2026-11-23); the only
change is Markdown escaping. The sentences around it are ours.
"""
import glob
import json
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import build_pages as bp  # noqa: E402

ROOT = bp.ROOT
DOCS = bp.DOCS
TODAY = '2026-11-26'
EN, ZH, CN, JA, KO = 'en', 'zh-TW', 'zh-CN', 'ja', 'ko'
LANGS = (EN, ZH, CN, JA, KO)
FOLDER = {EN: '', ZH: 'zh-tw', CN: 'zh-cn', JA: 'ja', KO: 'ko'}
PRE = {lang: ('/' + f if f else '') for lang, f in FOLDER.items()}
MAX_DESC = {EN: 110, ZH: 70, CN: 70, JA: 70, KO: 90}
TERMS = json.load(open(os.path.join(ROOT, 'records', 'story', 'terms.json'), encoding='utf8'))
SOURCE_TITLE = {EN: 'rmxlinux/EndfieldData, game tables (1.7, 2026-11-25)', ZH: 'rmxlinux/EndfieldData 遊戲資料表（1.7，2026-11-25）',
                CN: 'rmxlinux/EndfieldData 游戏资料表（1.7，2026-11-25）', JA: 'rmxlinux/EndfieldData、ゲームデータテーブル（1.7、2026-11-25）',
                KO: 'rmxlinux/EndfieldData 게임 데이터 테이블(1.7, 2026-11-25)'}


def L(lang, en, zh, cn, ja, ko):
    return {EN: en, ZH: zh, CN: cn, JA: ja, KO: ko}[lang]


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
    for para in s.split('\n\n'):
        lines = [x for x in esc(para).split('\n')]
        out.append('\n'.join('> ' + x + ('\\' if k < len(lines) - 1 and x else '') for k, x in enumerate(lines)))
    return '\n>\n'.join(out)


def inline(s):
    """Game text on one line (a table cell or a list item): line breaks become spaces."""
    return ' '.join(esc(s).split('\n'))


def unlock_text(u, op, lang):
    if not u:
        return ''
    if u['kind'] == 'trust':
        return TERMS['trust'][lang].replace('%s', str(u['value']))
    return op['promotions'][u['value'] - 1]['name'][lang]


def name(op, lang):
    return op['name'][lang]


def title_of(op, lang):
    n = name(op, lang)
    return L(lang, f"{n}'s file", f'{n}的檔案', f'{n}的档案', f'{n}のプロファイル', f'{n}의 파일')


def speaker(who, op, lang):
    return who[lang] if isinstance(who, dict) else ''


def chat_lines(items, op, lang, depth=0):
    pad = '  ' * depth
    out = []
    for it in items:
        if 'choice' in it:
            for k, branch in enumerate(it['choice'], 1):
                out.append(pad + '- ' + L(lang, f'Reply {k}', f'回覆{k}', f'回复{k}', f'返信{k}', f'답장 {k}'))
                out += chat_lines(branch, op, lang, depth + 1)
        elif it['speaker'] == 'system':
            out.append(f"{pad}- *{inline(it['text'][lang])}*")
        else:
            out.append(f"{pad}- **{speaker(it['speaker'], op, lang)}**{L(lang, ': ', '：', '：', '：', ': ')}{inline(it['text'][lang])}")
    return out


def page(st, op, lang):
    n = name(op, lang)
    title = title_of(op, lang)
    nf, nv, nc = len(st['files']), len(st['voice']), len(st['chats'])
    trust = sorted({f['unlock']['value'] for f in st['files'] if f['unlock'] and f['unlock']['kind'] == 'trust'})
    first_locked = next((f for f in st['files'] if f['unlock']), None)
    if nc:
        desc = L(lang, f"{n}'s {nf} operator files, {nv} voice lines and {nc} chats.",
                 f'{n}的 {nf} 份幹員檔案、{nv} 句語音與 {nc} 段聊天。',
                 f'{n}的 {nf} 份干员档案、{nv} 句语音与 {nc} 段聊天。',
                 f'{n}のプロファイル{nf}件、ボイス{nv}件、チャット{nc}件。',
                 f'{n}의 오퍼레이터 파일 {nf}개, 음성 {nv}개, 채팅 {nc}개.')
    else:
        desc = L(lang, f"{n}'s {nf} operator files and {nv} voice lines.",
                 f'{n}的 {nf} 份幹員檔案與 {nv} 句語音。',
                 f'{n}的 {nf} 份干员档案与 {nv} 句语音。',
                 f'{n}のプロファイル{nf}件、ボイス{nv}件。',
                 f'{n}의 오퍼레이터 파일 {nf}개, 음성 {nv}개.')
    assert len(desc) <= MAX_DESC[lang], (st['slug'], lang, len(desc), desc)
    lock = ''
    if first_locked:
        values = L(lang, ' or ', ' 或 ', ' 或 ', 'または', ' 또는 ').join(str(v) for v in trust)
        ft = first_locked['title'][lang]
        lock = L(lang, f"From “{ft}” on, a file unlocks at trust {values}. ",
                 f'「{ft}」起的檔案，信賴值達到 {values} 才解鎖。',
                 f'「{ft}」起的档案，信赖度达到 {values} 才解锁。',
                 f'「{ft}」以降のプロファイルは信頼度{values}で解放される。',
                 f"'{ft}'부터의 파일은 신뢰도 {values}에 도달해야 해제된다. ")
    caveat = lock + L(lang, "Each language has the game's own text in that language; the editions do not always match line for line.",
                      '各語言是遊戲各自的版本，句子不一定逐句對應。', '各语言是游戏各自的版本，句子不一定逐句对应。',
                      '各言語のテキストはゲームのその言語版であり、文ごとに一致するとは限らない。',
                      '각 언어의 텍스트는 게임의 해당 언어판이며, 문장 단위로 일치하지 않을 수 있다.')
    applies = L(lang, 'Arknights: Endfield, global service; text of game data 1.7 in English',
                '《明日方舟：終末地》國際版；遊戲資料 1.7 的繁體中文文字', '《明日方舟：终末地》；游戏资料 1.7 的简体中文文字',
                '『アークナイツ：エンドフィールド』グローバル版。ゲームデータ1.7の日本語テキスト',
                '《명일방주: 엔드필드》 글로벌 서비스. 게임 데이터 1.7의 한국어 텍스트')
    titles = {x: title_of(op, x) for x in LANGS}
    aliases = bp.aliases_of(titles, title)
    fm = ['---', f'title: {bp.quote(title)}', f'description: {bp.quote(desc)}', f'appliesTo: {bp.quote(applies)}',
          f'caveat: {bp.quote(caveat.strip())}', f'lastVerified: {TODAY}', 'aliases:']
    fm += [f'  - {bp.quote(a)}' for a in aliases]
    fm += ['sources:', f'  - title: {bp.quote(SOURCE_TITLE[lang])}', f"    url: {st['source']}", '---']

    # The body opens with a heading: the answer line is the page's only opening.
    body = ['', '## ' + TERMS['file'][lang], '']
    for f in st['files']:
        body += ['### ' + esc(f['title'][lang]), '']
        u = unlock_text(f['unlock'], op, lang)
        if u:
            body += [f'*{u}*', '']
        body += [quoted(f['text'][lang]), '']
    head = L(lang, '| Title | Line | Unlock |', '| 標題 | 台詞 | 解鎖 |', '| 标题 | 台词 | 解锁 |', '| タイトル | セリフ | 解放 |', '| 제목 | 대사 | 해제 |')
    body += ['## ' + L(lang, 'Voice lines', '語音', '语音', 'ボイス', '음성'), '', head, '| --- | --- | --- |']
    for v in st['voice']:
        body.append(f"| {inline(v['title'][lang])} | {inline(v['text'][lang])} | {unlock_text(v['unlock'], op, lang)} |")
    if st['chats']:
        body += ['', '## ' + L(lang, 'Chats', '聊天', '聊天', 'チャット', '채팅'), '']
        for c in st['chats']:
            body += ['### ' + esc(c['topic'][lang]), '']
            body += chat_lines(c['lines'], op, lang)
            body.append('')
    return '\n'.join(fm + body).rstrip('\n') + '\n'


def index_page(stories, ops, lang):
    # The index sits in the Operators group of the sidebar, under the operator list.
    names = ('Operator files', '幹員檔案', '干员档案', 'プロファイル', '오퍼레이터 파일')
    title = L(lang, *names)
    titles = {x: L(x, *names) for x in LANGS}
    k = len(stories)
    desc = L(lang, f"The files, voice lines and chats of the {k} operators of Arknights: Endfield.",
             f'《明日方舟：終末地》{k} 名幹員的檔案、語音與聊天。',
             f'《明日方舟：终末地》{k} 名干员的档案、语音与聊天。',
             f'『アークナイツ：エンドフィールド』のオペレーター{k}人のプロファイル、ボイス、チャット。',
             f'《명일방주: 엔드필드》 오퍼레이터 {k}명의 파일, 음성, 채팅.')
    assert len(desc) <= MAX_DESC[lang], (lang, len(desc))
    caveat = L(lang, "Each language has the game's own text in that language; the editions do not always match line for line.",
               '各語言是遊戲各自的版本，句子不一定逐句對應。', '各语言是游戏各自的版本，句子不一定逐句对应。',
               '各言語のテキストはゲームのその言語版であり、文ごとに一致するとは限らない。',
               '각 언어의 텍스트는 게임의 해당 언어판이며, 문장 단위로 일치하지 않을 수 있다.')
    applies = L(lang, 'Arknights: Endfield, global service; text of game data 1.7', '《明日方舟：終末地》國際版；遊戲資料 1.7 的文字',
                '《明日方舟：终末地》；游戏资料 1.7 的文字', '『アークナイツ：エンドフィールド』グローバル版。ゲームデータ1.7のテキスト',
                '《명일방주: 엔드필드》 글로벌 서비스. 게임 데이터 1.7의 텍스트')
    fm = ['---', f'title: {bp.quote(title)}', f'description: {bp.quote(desc)}', f'appliesTo: {bp.quote(applies)}',
          f'caveat: {bp.quote(caveat)}', f'lastVerified: {TODAY}', 'aliases:']
    fm += [f'  - {bp.quote(a)}' for a in bp.aliases_of(titles, title)]
    fm += ['sources:', f'  - title: {bp.quote(SOURCE_TITLE[lang])}', f"    url: {stories[0]['source']}", '---']
    body = ['', L(lang, '| Operator | Files | Voice lines | Chats |', '| 幹員 | 檔案 | 語音 | 聊天 |', '| 干员 | 档案 | 语音 | 聊天 |',
              '| オペレーター | プロファイル | ボイス | チャット |', '| 오퍼레이터 | 파일 | 음성 | 채팅 |'), '| --- | --- | --- | --- |']
    for st in sorted(stories, key=lambda s: name(ops[s['slug']], EN)):
        op = ops[st['slug']]
        body.append(f"| [{title_of(op, lang)}]({PRE[lang]}/story/{st['slug']}/) | {len(st['files'])} | {len(st['voice'])} | {len(st['chats'])} |")
    return '\n'.join(fm + body) + '\n'


def main():
    ops = {s: bp.enrich(op) for s, op in bp.OPS.items()}
    stories = []
    for p in sorted(glob.glob(os.path.join(ROOT, 'records', 'story', '*.json'))):
        if os.path.basename(p) == 'terms.json':
            continue
        stories.append(json.load(open(p, encoding='utf8')))
    for lang in LANGS:
        folder = os.path.join(DOCS, FOLDER[lang], 'story')
        os.makedirs(folder, exist_ok=True)
        for old in glob.glob(os.path.join(folder, '*.md')):
            os.remove(old)
        for st in stories:
            open(os.path.join(folder, f"{st['slug']}.md"), 'w', encoding='utf8').write(page(st, ops[st['slug']], lang))
        open(os.path.join(folder, 'index.md'), 'w', encoding='utf8').write(index_page(stories, ops, lang))
    print(len(stories), 'story pages and the index, per language, in', ', '.join(LANGS))


if __name__ == '__main__':
    main()
