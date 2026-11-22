"""Decode the data that a warfarin.wiki page carries (Remix turbo-stream) into plain JSON.

Usage: python3 -I pipeline/wf_decode.py <page.html> <out.json>
The page script holds one flat array; objects use keys "_<n>" that point at the
key's string, and values are indices into the same array. Negative values are
constants (undefined, null, and so on).
"""
import json
import re
import sys

sys.setrecursionlimit(100000)


def decode(html: str):
    chunks = re.findall(r'streamController\.enqueue\((".*?")\);?\s*</script>', html, flags=re.S)
    if not chunks:
        raise SystemExit('no stream data in page')
    flat = json.loads(json.loads(chunks[0]).split('\n')[0])
    memo = {}

    def at(i):
        if i < 0:
            return None
        if i in memo:
            return memo[i]
        v = flat[i]
        if isinstance(v, dict):
            out = {}
            memo[i] = out
            for k, x in v.items():
                out[flat[int(k[1:])]] = at(x)
            return out
        if isinstance(v, list):
            if v and isinstance(v[0], str) and len(v) >= 1 and v[0] in ('D', 'P', 'E', 'M', 'S', 'N', 'Z', 'U', 'R', 'Y', 'A', 'B', 'T'):
                memo[i] = v
                return v
            out = []
            memo[i] = out
            out.extend(at(x) for x in v)
            return out
        memo[i] = v
        return v

    return at(0)


if __name__ == '__main__':
    data = decode(open(sys.argv[1], encoding='utf8').read())
    json.dump(data, open(sys.argv[2], 'w', encoding='utf8'), ensure_ascii=False)
