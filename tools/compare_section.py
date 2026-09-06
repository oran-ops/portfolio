# -*- coding: utf-8 -*-
"""Show one section's copy from both builds, aligned in reading order.

A list of "blocks only in root" is not something anyone can decide on: a line of copy means
different things depending on what sits either side of it. So this aligns the two versions the
way a diff does and prints them in the order a reader meets them, marking only where they part.

    python tools/compare_section.py oasis
"""
import difflib
import html
import io
import os
import re
import sys

sys.stdout.reconfigure(encoding='utf-8', errors='replace')
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
WHICH = sys.argv[1] if len(sys.argv) > 1 else 'oasis'


def blocks(path, sid):
    doc = io.open(os.path.join(ROOT, path), encoding='utf-8', errors='replace').read()
    pos = [(m.group(1), m.start()) for m in re.finditer(r'<section[^>]*id="([^"]+)"', doc)]
    for i, (s, a) in enumerate(pos):
        if s != sid:
            continue
        b = pos[i + 1][1] if i + 1 < len(pos) else len(doc)
        chunk = re.sub(r'<(script|style)[^>]*>.*?</\1>', ' ', doc[a:b], flags=re.S)
        chunk = re.sub(r'<[^>]+>', '\n', chunk)
        out = []
        for w in chunk.split('\n'):
            w = re.sub(r'\s+', ' ', html.unescape(w).replace('\xa0', ' ')).strip()
            if w:
                out.append(w)
        return out
    return []


A = blocks('index.html', WHICH)
B = blocks('m/index.html', WHICH)
print('section  %s' % WHICH)
print('root     %d blocks' % len(A))
print('m/       %d blocks' % len(B))
print()

sm = difflib.SequenceMatcher(None, A, B, autojunk=False)
n = 0
for tag, i1, i2, j1, j2 in sm.get_opcodes():
    if tag == 'equal':
        # enough context to place the change, never the whole run
        run = A[i1:i2]
        if len(run) > 4:
            for x in run[:2]:
                print('    =  %s' % x[:104])
            print('    =  ... %d identical blocks ...' % (len(run) - 4))
            for x in run[-2:]:
                print('    =  %s' % x[:104])
        else:
            for x in run:
                print('    =  %s' % x[:104])
        continue
    n += 1
    print()
    print('  --- difference %d -------------------------------------------------' % n)
    for x in A[i1:i2]:
        print('  ROOT >  %s' % x[:104])
    for x in B[j1:j2]:
        print('  m/   >  %s' % x[:104])
    print()

print()
print('%d places where the two part company.' % n)
