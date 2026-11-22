"""List the names whose Simplified Chinese form is not the plain conversion of the Traditional one.

Usage: uv run --with opencc-python-reimplemented pipeline/names_voc.py
Reads records/ and writes records/names-voc.json, which scripts/to-zh-cn.py applies before
converting. Also adds the Simplified title as an alias to draft pages given as arguments.
"""
import glob
import json
import os
import re
import sys

from opencc import OpenCC

cc = OpenCC('tw2s')
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


def walk(node, out):
    if isinstance(node, dict):
        if 'zh-TW' in node and 'zh-CN' in node and isinstance(node['zh-TW'], str):
            out.add((node['zh-TW'], node['zh-CN']))
        for v in node.values():
            walk(v, out)
    elif isinstance(node, list):
        for v in node:
            walk(v, out)


def main():
    pairs = set()
    for path in glob.glob(os.path.join(ROOT, 'records', '**', '*.json'), recursive=True):
        if path.endswith('names-voc.json'):
            continue
        walk(json.load(open(path, encoding='utf8')), pairs)
    voc = sorted(((tw, cn) for tw, cn in pairs if cc.convert(tw) != cn and tw and cn), key=lambda p: -len(p[0]))
    json.dump(voc, open(os.path.join(ROOT, 'records', 'names-voc.json'), 'w', encoding='utf8'), ensure_ascii=False, indent=1)
    print(len(pairs), 'name pairs,', len(voc), 'differ beyond the script')
    for tw, cn in voc:
        print(' ', tw, '->', cn, '| plain conversion:', cc.convert(tw))
    # Simplified title as an alias on pages given as arguments (zh-tw page first, then its English page).
    for zh, en in zip(sys.argv[1::2], sys.argv[2::2]):
        text = open(zh, encoding='utf8').read()
        title = re.search(r'^title: (.*)$', text, flags=re.M).group(1)
        simp = cc.convert(title)
        if simp == title:
            continue
        for path in (zh, en):
            t = open(path, encoding='utf8').read()
            head = t.split('\n---\n', 1)[0]
            if simp.strip('"') in head:
                continue
            t = re.sub(r'^(aliases:\n(?:  - .*\n)+)', lambda m: m.group(1) + f'  - {simp}\n', t, count=1, flags=re.M)
            open(path, 'w', encoding='utf8').write(t)
            print('alias added:', path, simp)


if __name__ == '__main__':
    main()
