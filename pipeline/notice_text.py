"""Print an official notice from the cache as plain text.

Usage: python3 -I pipeline/notice_text.py <cache/official/art/<lang>-<cid>.json> [start] [end]
"""
import html
import json
import re
import sys


def text_of(path):
    d = json.load(open(path, encoding="utf-8"))["data"]
    s = d["data"]
    s = re.sub(r"<img[^>]*>", " [image] ", s)
    s = re.sub(r"</t[dh]>", " | ", s)
    s = re.sub(r"<br\s*/?>|</p>|</div>|</li>|</tr>|</h\d>", "\n", s)
    s = html.unescape(re.sub(r"<[^>]+>", "", s)).replace("\xa0", " ")
    s = re.sub(r"[ \t]+", " ", s)
    s = re.sub(r"\n\s*\n+", "\n", s).strip()
    return d["title"], d["displayTime"], s


if __name__ == "__main__":
    title, ts, s = text_of(sys.argv[1])
    a = int(sys.argv[2]) if len(sys.argv) > 2 else 0
    b = int(sys.argv[3]) if len(sys.argv) > 3 else len(s)
    print(f"# {title} (displayTime {ts}, {len(s)} chars)\n")
    print(s[a:b])
