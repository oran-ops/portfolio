# -*- coding: utf-8 -*-
"""Cut the archive props Oran approved for removal — the nine lines, by name.

These are the empty pieces of 1970s dressing: a classification band that classifies nothing,
control numbers for a registry that does not exist, and a copy count for copies nobody made.
None of them say anything about Oran, and they now sit inside a 1984 Macintosh, which is a
second costume from a second decade.

What is NOT cut, and the distinction that governs it: the live layer stays in full — the
analyst note, the UV lamp, the evidence slip, the sheet flip. Those deliver real content
through a device. These nine deliver nothing. A deletion list without a keep list invites
over-deletion, so the keep list is asserted here too.

    python tools/cut_archive_props.py           report what would change
    python tools/cut_archive_props.py --write   make the cut
"""
import io
import os
import re
import sys

sys.stdout.reconfigure(encoding='utf-8', errors='replace')
HERE = os.path.dirname(os.path.abspath(__file__))
DOC = os.path.join(os.path.dirname(HERE), 'src', 'doc')

# Exactly what Oran read and approved, by document. The counts are asserted: if a file does
# not hold precisely this many, the cut refuses rather than guessing.
CUTS = {
    'xtix':    {'clsband': 1, 'clsctl': 1},
    'oasis':   {'clsband': 1, 'clsctl': 1, 'srcline': 1},
    'eventer': {'clsband': 1, 'clsctl': 1},
    'medcoin': {'clsband': 1, 'clsctl': 1},
}

# Must survive untouched. Checked after the cut, not before, because the failure this guards
# against is a regex that reaches further than its author intended.
KEEP = ['CASE STUDY', 'PART 1 OF 2', 'lampband', 'evslip', 'an-note', 'slipflip']


def element(html, cls):
    """The whole <div class="cls">…</div>, brace-matched, plus the whitespace before it."""
    out = []
    for m in re.finditer(r'<div class="%s"[^>]*>' % cls, html):
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
        out.append((start, end, html[m.start():end]))
    return out


def main():
    write = '--write' in sys.argv
    total = 0
    for doc, wanted in CUTS.items():
        path = os.path.join(DOC, '%s.html' % doc)
        html = io.open(path, encoding='utf-8').read()
        before = len(html)
        spans = []
        for cls, n in wanted.items():
            found = element(html, cls)
            if len(found) != n:
                print('  REFUSED %s: expected %d .%s, found %d' % (doc, n, cls, len(found)))
                return 1
            for s, e, frag in found:
                spans.append((s, e))
                print('  %-8s .%-8s %4d B  %s' % (doc, cls, e - s,
                                                  ' '.join(re.sub(r'<[^>]+>', ' ', frag).split())[:64]))
        for s, e in sorted(spans, reverse=True):
            html = html[:s] + html[e:]
        for k in KEEP:
            if k in io.open(path, encoding='utf-8').read() and k not in html:
                print('  REFUSED %s: the cut removed %r, which must survive' % (doc, k))
                return 1
        total += before - len(html)
        if write:
            io.open(path, 'w', encoding='utf-8', newline='').write(html)
    print()
    print('  %d bytes across %d documents%s' % (total, len(CUTS), '' if write else '  (dry run)'))
    if write:
        print('  now run:  python build.py')
    return 0


if __name__ == '__main__':
    sys.exit(main())
