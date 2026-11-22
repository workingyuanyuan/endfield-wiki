"""Read the operator profiles that the official site ships in its page script.

Usage: python3 -I pipeline/extract_official_operators.py <script.js> <out.json>

For each language the script holds a `JSON.parse('[{"key":...}]')` array (the launch
roster) followed by a `JSON.parse('{...}')` object of interface text, in which later
operators are flat keys: `operator.content.<key>.<field>`. A language is recognised by
one interface string. Output: {lang: {"roster": [...], "text": {operator.* keys}}}.
"""
import json
import re
import sys

MARK = {
    "en": '"aic.items.0.title":"Automated Production"',
    "zh-TW": '"aic.items.0.title":"自動化生產"',
    "zh-CN": '"aic.items.0.title":"自动化生产"',
}


def js_string(src, start):
    """Decode the single-quoted JS string literal that starts at src[start] == "'"."""
    out, i = [], start + 1
    while src[i] != "'":
        c = src[i]
        if c == "\\":
            n = src[i + 1]
            if n == "x":
                out.append(chr(int(src[i + 2 : i + 4], 16)))
                i += 4
            elif n == "u":
                out.append(chr(int(src[i + 2 : i + 6], 16)))
                i += 6
            else:
                out.append({"n": "\n", "t": "\t", "r": "\r"}.get(n, n))
                i += 2
        else:
            out.append(c)
            i += 1
    return "".join(out)


def main(path, out_path):
    src = open(path, encoding="utf-8", errors="replace").read()
    result, roster = {}, None
    for m in re.finditer(r"JSON\.parse\('([\[{])", src):
        value = json.loads(js_string(src, m.start() + len("JSON.parse(")))
        if m.group(1) == "[":
            roster = value if value and isinstance(value[0], dict) and "key" in value[0] else None
            continue
        raw = json.dumps(value, ensure_ascii=False, separators=(",", ":"))
        for lang, mark in MARK.items():
            if mark in raw and lang not in result:
                text = {k: v for k, v in value.items() if k.startswith("operator.")}
                result[lang] = {"roster": roster, "text": text}
        roster = None
    missing = [lang for lang in MARK if lang not in result]
    if missing:
        sys.exit(f"no data found for: {missing}")
    json.dump(result, open(out_path, "w", encoding="utf-8"), ensure_ascii=False, indent=1)
    print({lang: (len(v["roster"] or []), len(v["text"])) for lang, v in result.items()})


if __name__ == "__main__":
    main(sys.argv[1], sys.argv[2])
