"""Check the restated text of one operator against its source sheet.

Usage: python3 -I pipeline/check_text.py <sheet.json> <text.json>
Exit code 1 when anything is wrong. Runs on one operator, without a build.
"""
import json
import re
import sys

KINDS = ['basic', 'battle', 'combo', 'ultimate']
LIMIT = {'en': 400, 'zh-TW': 200}


def numbers(text):
    return set(re.findall(r'\d+(?:\.\d+)?', text))


def cjk(text):
    return len(re.findall(r'[一-鿿]', text))


def longest_run_words(a, b):
    wa, wb = re.findall(r"[A-Za-z0-9'%.]+", a.lower()), re.findall(r"[A-Za-z0-9'%.]+", b.lower())
    grams = {tuple(wb[i:i + 13]) for i in range(len(wb) - 12)}
    return any(tuple(wa[i:i + 13]) in grams for i in range(len(wa) - 12))


def longest_run_chars(a, b, n=26):
    a, b = re.sub(r'\s', '', a), re.sub(r'\s', '', b)
    grams = {b[i:i + n] for i in range(len(b) - n + 1)}
    return any(a[i:i + n] in grams for i in range(len(a) - n + 1))


def check_item(where, item, source_text, errors, combo=False):
    if not isinstance(item, dict) or set(item) != {'en', 'zh-TW'}:
        errors.append(f'{where}: must be an object with exactly the keys "en" and "zh-TW"')
        return
    for lang in ('en', 'zh-TW'):
        text = item[lang]
        if not isinstance(text, str) or not text.strip():
            errors.append(f'{where}.{lang}: empty')
            continue
        # A skill with two forms (the game text carries a bracketed form name) may run longer.
        limit = LIMIT[lang] * (1.7 if '\n\n[' in source_text['en'] else 1)
        if len(text) > limit:
            errors.append(f'{where}.{lang}: {len(text)} characters, limit {LIMIT[lang]}')
        if re.search(r'[|\n\[\]*`<>]|//', text):
            errors.append(f'{where}.{lang}: contains a pipe, line break, bracket, Markdown or "//"')
        if lang == 'en' and cjk(text):
            errors.append(f'{where}.en: contains Chinese characters')
        if lang == 'zh-TW' and cjk(text) < 4:
            errors.append(f'{where}.zh-TW: is not Chinese')
        extra = numbers(text) - numbers(source_text['en'] + ' ' + source_text['zh-TW'])
        if extra:
            errors.append(f'{where}.{lang}: numbers not in the game text or its values: {sorted(extra)}')
        if lang == 'en' and longest_run_words(text, source_text['en']):
            errors.append(f'{where}.en: thirteen or more consecutive words are the same as the game text; restate it')
        if lang == 'zh-TW' and longest_run_chars(text, source_text['zh-TW']):
            errors.append(f'{where}.zh-TW: twenty-six or more consecutive characters are the same as the game text; restate it')
    if combo:
        if not item['en'].startswith('Trigger: '):
            errors.append(f'{where}.en: a combo skill starts with "Trigger: "')
        if not item['zh-TW'].startswith('觸發條件：'):
            errors.append(f'{where}.zh-TW: a combo skill starts with "觸發條件："')
    if numbers(item['en']) != numbers(item['zh-TW']):
        errors.append(f'{where}: the two languages state different numbers: en {sorted(numbers(item["en"]))}, zh-TW {sorted(numbers(item["zh-TW"]))}')


def main(sheet_path, text_path):
    sheet = json.load(open(sheet_path, encoding='utf8'))
    errors = []
    try:
        text = json.load(open(text_path, encoding='utf8'))
    except Exception as e:  # noqa: BLE001
        print(f'ERROR {text_path}: not valid JSON: {e}')
        return 1
    if set(text) != {'slug', 'intro', 'skills', 'talents', 'potentials'}:
        errors.append('top-level keys must be exactly: slug, intro, skills, talents, potentials')
    if text.get('slug') != sheet['slug']:
        errors.append('slug differs from the sheet')
    intro_src = {l: sheet['officialIntro'][l] + ' ' + sheet['gameSummary'][l] + ' ' + sheet['profile'][l] for l in ('en', 'zh-TW')}
    check_item('intro', text.get('intro'), intro_src, errors)
    skills = text.get('skills') or {}
    if list(skills) != KINDS:
        errors.append(f'skills must have the keys {KINDS} in this order')
    for kind in KINDS:
        if kind not in skills or kind not in sheet['skills']:
            continue
        s = sheet['skills'][kind]
        src = {l: s['gameText'][l] + ' ' + ' '.join(f"{v[l]} {v['level1']} {v['level12']}" for v in s['values']) for l in ('en', 'zh-TW')}
        check_item(f'skills.{kind}', skills[kind], src, errors, combo=(kind == 'combo'))
    for name, key in (('talents', 'levels'), ('potentials', None)):
        got, want = text.get(name) or [], sheet[name]
        if len(got) != len(want):
            errors.append(f'{name}: {len(got)} entries, the sheet has {len(want)}')
            continue
        for i, (g, w) in enumerate(zip(got, want)):
            if key:
                src = {l: ' '.join(x['gameText'][l] for x in w[key]) for l in ('en', 'zh-TW')}
            else:
                src = w['gameText']
            check_item(f'{name}[{i}]', g, src, errors)
    for e in errors:
        print(f'ERROR {text_path}: {e}')
    if not errors:
        print(f'ok    {text_path}')
    return 1 if errors else 0


if __name__ == '__main__':
    sys.exit(main(sys.argv[1], sys.argv[2]))
