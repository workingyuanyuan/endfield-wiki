"""Read the story text of operators from the client tables and write records/story/<slug>.json.

Usage: python3 -I pipeline/story_extract.py [slug ...]
Reads cache/third/ed/<commit>/ (tables of github.com/rmxlinux/EndfieldData at that commit;
the cache is not committed): CharacterTable (files and voice lines), SNSChatTable,
SNSDialogTable, SNSDialogTopicTable and SNSDialogOptionTable (chats), and the five text
tables. Without slugs it reads every operator in records/operators/. It also writes
records/story/terms.json, the game's words the page script needs.

The text is the game's own, in each language's edition (owner decision, 2026-11-23): it is
stored as the text table gives it, with only the game's markup removed (Japanese ruby keeps
its base text, as on the other pages). Nothing is reworded.

A chat is stored as the game plays it: lines in order, and where the Endministrator picks a
reply, every branch until the branches meet again. Chat entries other than text (stickers,
images, links to records) and lines that are only a sticker are left out and counted in
`skipped`.
"""
import glob
import json
import os
import re
import sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
COMMIT = 'd847759f71d4549aba4727b3b0ac1a1ad0e37742'
ED = os.path.join(ROOT, 'cache', 'third', 'ed', COMMIT)
OUT = os.path.join(ROOT, 'records', 'story')
LANGS = {'en': 'EN', 'zh-TW': 'TC', 'zh-CN': 'CN', 'ja': 'JP', 'ko': 'KR'}
RUBY = re.compile(r'<p="[^"]*" padding=0>(.*?)</p>')
# Markup of the game's rich text: <color=…>, </color>, <@style>, </>, <i>, <b>.
TAG = re.compile(r'</?(?:color|size|b|i|u)(?:=[^>]*)?>|<@[\w.]+>|</>')
# A sticker inside a chat line; a line that is only a sticker is left out.
IMAGE = re.compile(r'<image="[^"]*">')


def table(name):
    return json.load(open(os.path.join(ED, name + '.json'), encoding='utf8'))


TEXT = {lang: table('I18nTextTable_' + code) for lang, code in LANGS.items()}


def clean(s):
    s = RUBY.sub(r'\1', s)
    s = TAG.sub('', s)
    s = IMAGE.sub('', s)
    return s.replace('\r\n', '\n').strip()


def text(ref, required=True):
    out = {lang: clean(TEXT[lang].get(str(ref['id']), '')) for lang in LANGS}
    if required:
        missing = [lang for lang, v in out.items() if not v]
        assert not missing, (ref, missing)
    return out


def pair(en, zh):
    """A game term by its English and Traditional Chinese text, in every language."""
    ids = sorted(k for k, v in TEXT['en'].items() if v == en and TEXT['zh-TW'].get(k) == zh)
    assert ids, (en, zh)
    return {lang: clean(TEXT[lang][ids[0]]) for lang in LANGS}


# The game's words the page script needs: the speaker name of the player character, the
# unlock condition by trust and the name of the operator file.
TERMS = {'endmin': pair('Endministrator', '管理員'), 'trust': pair('Reach trust: %s', '信賴值達到%s可解鎖'),
         'file': pair('Operator File', '幹員檔案')}


def unlock(entry):
    """Unlock condition as the game stores it: 0 always, 2 a promotion stage, 4 a trust value."""
    kind, value = entry['unlockType'], entry['unlockValue']
    assert kind in (0, 2, 4), entry
    return None if kind == 0 else {'kind': {2: 'promotion', 4: 'trust'}[kind], 'value': value}


def chat(dialog, speakers, options, skipped):
    """The lines of one chat dialog, with reply branches."""
    nodes = {int(k): v for k, v in dialog['dialogContentData'].items()}

    def nexts(n):
        """Nodes that follow node n: its options' targets, or its next node."""
        if n['dialogOptionIds']:
            return [options[o]['optionNextContentId'] for o in n['dialogOptionIds']]
        return [n['nextContentId']] if n['nextContentId'] else []

    def path(start, stop=None):
        """Node ids from start along the first branch, to the end or to stop."""
        out, cur, seen = [], start, set()
        while cur in nodes and cur != stop and cur not in seen and cur > 0:
            seen.add(cur)
            out.append(cur)
            nx = nexts(nodes[cur])
            cur = nx[0] if nx else None
        return out

    def walk(start, stop=None):
        items, cur = [], start
        while cur in nodes and cur != stop and cur > 0:
            n = nodes[cur]
            if n['contentType'] == 1:
                line = text(n['content'], required=False)
                if not any(line.values()):
                    # A node that only offers replies has no text; a line that was only a sticker does.
                    skipped[0] += n['content']['id'] != 0
                else:
                    assert all(line.values()), (dialog['dialogId'], cur)
                    who = speakers.get(n['speaker'])
                    assert who is not None, (dialog['dialogId'], n['speaker'])
                    items.append({'speaker': who, 'text': line})
            elif n['contentType'] == 7:
                items.append({'speaker': 'system', 'text': text(n['content'])})
            else:
                skipped[0] += 1
            targets = [t for t in nexts(n) if t > 0]
            if len(set(targets)) > 1:
                # A choice: follow each branch to the first node every branch reaches.
                paths = [path(t) for t in targets]
                merge = next((x for x in paths[0] if all(x in p for p in paths[1:])), None)
                items.append({'choice': [walk(t, merge) for t in targets]})
                cur = merge
            else:
                cur = targets[0] if targets else None
        return items

    return walk(min(k for k in nodes if k > 0))


def main():
    ops = {}
    for p in sorted(glob.glob(os.path.join(ROOT, 'records', 'operators', '*.json'))):
        rec = json.load(open(p, encoding='utf8'))
        ops[rec['slug']] = rec
    slugs = sys.argv[1:] or list(ops)
    chars = table('CharacterTable')
    chats = table('SNSChatTable')
    dialogs = table('SNSDialogTable')
    topics = table('SNSDialogTopicTable')
    options = table('SNSDialogOptionTable')
    endmin = TERMS['endmin']
    os.makedirs(OUT, exist_ok=True)
    json.dump(TERMS, open(os.path.join(OUT, 'terms.json'), 'w', encoding='utf8'), ensure_ascii=False, indent=1)
    for slug in slugs:
        op = ops[slug]
        ch = chars[op['gameId']]
        rec = {'slug': slug, 'gameId': op['gameId'], 'source': f'https://github.com/rmxlinux/EndfieldData/tree/{COMMIT}/TableCfg',
               'files': [], 'voice': [], 'chats': [], 'skipped': 0}
        for r in sorted(ch['profileRecord'], key=lambda r: r['recordIndex']):
            rec['files'].append({'id': r['recordID'], 'title': text(r['recordTitle']), 'text': text(r['recordDesc']), 'unlock': unlock(r)})
        for v in sorted(ch['profileVoice'], key=lambda v: v['voiceIndex']):
            rec['voice'].append({'id': v['voId'], 'title': text(v['voiceTitle']), 'text': text(v['voiceDesc']), 'unlock': unlock(v)})
        channel = 'sns_' + op['gameId']
        if channel in chats:
            own = text(chats[channel]['name'])
            speakers = {'endmin': endmin, channel: own, '': None}
            skipped = [0]
            # The chats with a topic, in the order the game lists them; chats tied to a
            # mission or a test entry are not topics.
            mine = [d for d in dialogs.values() if d['chatId'] == channel and d['topicId'] in topics]
            mine.sort(key=lambda d: (topics[d['topicId']]['sortId'], d['topicId']))
            for d in mine:
                rec['chats'].append({'id': d['dialogId'], 'topic': text(topics[d['topicId']]['topicName']),
                                     'lines': chat(d, speakers, options, skipped)})
            rec['skipped'] = skipped[0]
        path = os.path.join(OUT, f'{slug}.json')
        json.dump(rec, open(path, 'w', encoding='utf8'), ensure_ascii=False, indent=1)
        print(f"{slug}: {len(rec['files'])} files, {len(rec['voice'])} voice lines, {len(rec['chats'])} chats, {rec['skipped']} non-text chat entries left out")


if __name__ == '__main__':
    main()
