# -*- coding: utf-8 -*-
"""Cut the filing-cabinet drawer — the `.otx` intro block, in the four case documents.

Oran's ruling: *"המגירה יורדת."* In the new structure a document is opened by clicking an icon
in a Macintosh folder, and the drawer put a second opening immediately after the first — an
archive drawer sliding out and a folder cover lifting, inside a machine that had just opened
the same file. Two openings, from two different decades, back to back. What replaces it is the
zoom rectangle: the gesture the real machine used, about 180 ms, and then the document.

The wording that leaves with it, per document: the folder lip, the big number, `CASE FILE 0N`,
`STATUS: DECLASSIFIED`, `> EVIDENCE ENCLOSED — CONTINUE`, `CASE FILE · COMMERCIAL ARCHIVE`, the
cover category, `> classification: COMMERCIAL`, `> drawer: C-0N · archive 2026`, `ARCHIVE
DRAWER C-0N · COMMERCIAL RECORDS`, and `PULLING FILE 0N`.

CHECKED FIRST, this time. `python tools/depends.py otx` reports no gates: the eight script
references are a map over `querySelectorAll('.otx')`, which is fine when empty, and lookups
already wrapped in `if(otx){...}`. That check exists because cutting `.clsband` without it took
the UV lamp down silently.

    python tools/cut_drawer.py           report
    python tools/cut_drawer.py --write   make the cut
"""
import io
import os
import re
import sys

sys.stdout.reconfigure(encoding='utf-8', errors='replace')
HERE = os.path.dirname(os.path.abspath(__file__))
DOC = os.path.join(os.path.dirname(HERE), 'src', 'doc')

CASES = ['xtix', 'oasis', 'eventer', 'medcoin']
# The three that never had one. Asserted, so a future .otx appearing here is noticed.
NONE = ['leadership', 'tech', 'final']

# Must survive in the file the cut touches. Unlike the keep-list that failed on `.clsband`,
# every name here genuinely exists in these files, so the assertion cannot pass vacuously.
KEEP = ['class="secnum"', 'class="wrap"', 'class="shead', 'class="sttl',
        'class="folder', 'class="tabrow', 'class="cols2', 'class="zr"']


def block(html, cls):
    """The whole <div class="cls">…</div>, brace-matched over div tags."""
    m = re.search(r'<div class="%s"' % cls, html)
    if not m:
        return None
    depth, end = 0, m.start()
    for t in re.finditer(r'</?div\b', html[m.start():]):
        depth += -1 if t.group(0).startswith('</') else 1
        if depth == 0:
            end = m.start() + t.end() + 1
            break
    start = m.start()
    while start > 0 and html[start - 1] in ' \t':
        start -= 1
    if start > 0 and html[start - 1] == '\n':
        start -= 1
    return start, end


def main():
    write = '--write' in sys.argv
    total = 0

    for doc in NONE:
        s = io.open(os.path.join(DOC, '%s.html' % doc), encoding='utf-8').read()
        if 'class="otx"' in s:
            print('  REFUSED %s: expected no drawer, found one' % doc)
            return 1

    for doc in CASES:
        path = os.path.join(DOC, '%s.html' % doc)
        src = io.open(path, encoding='utf-8').read()
        span = block(src, 'otx')
        if not span:
            print('  REFUSED %s: no .otx to cut' % doc)
            return 1
        s, e = span
        out = src[:s] + src[e:]

        if 'class="otx"' in out:
            print('  REFUSED %s: a second .otx remains' % doc)
            return 1
        for k in KEEP:
            if k not in src:
                print('  REFUSED %s: keep-list entry %r is not in this file, so asserting it '
                      'would prove nothing' % (doc, k))
                return 1
            if k not in out:
                print('  REFUSED %s: the cut removed %r' % (doc, k))
                return 1
        if out.count('<div') != out.count('</div>'):
            print('  REFUSED %s: div tags no longer balance (%d open, %d close)'
                  % (doc, out.count('<div'), out.count('</div>')))
            return 1

        gone = len(src) - len(out)
        total += gone
        print('  %-9s %5d B removed, %5d left   (%.0f%% of the file)'
              % (doc, gone, len(out), 100.0 * gone / len(src)))
        if write:
            io.open(path, 'w', encoding='utf-8', newline='').write(out)

    print()
    print('  %d bytes across %d documents%s' % (total, len(CASES), '' if write else '  (dry run)'))
    if write:
        print('  now run:  python build.py')
    return 0


if __name__ == '__main__':
    sys.exit(main())
