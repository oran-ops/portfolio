# -*- coding: utf-8 -*-
"""Cut the binder rail and the (S) marks — the second batch Oran approved.

THE BINDER RAIL. `.frail` and its two `.hole` children, in all six documents that carry it
plus FINAL. Punch holes are a third decade's furniture: the shell is 1984 and the content is
2026, and a ring binder is neither. Oran chose to remove them rather than leave a rail with
nothing on it.

THE (S) MARK. A superscript beside "$9M+ ARR" and "$2M". Neither of us could establish what it
denoted — there is no legend anywhere on the page — and it sits against Oran's own figures,
which is the last place to leave a mark whose meaning nobody can state. He said: remove it.

Not to be confused with `.oc-hole`, which is the folder cover's own perforation inside `.otx`
and leaves with the drawer in a separate cut.

    python tools/cut_binder_and_marks.py           report
    python tools/cut_binder_and_marks.py --write   make the cut
"""
import io
import os
import re
import sys

sys.stdout.reconfigure(encoding='utf-8', errors='replace')
HERE = os.path.dirname(os.path.abspath(__file__))
DOC = os.path.join(os.path.dirname(HERE), 'src', 'doc')

# file -> (.frail rails, .pmark marks). Asserted exactly; the cut refuses on any mismatch.
EXPECT = {
    'xtix':       (1, 1),
    'oasis':      (1, 1),
    'eventer':    (1, 0),
    'medcoin':    (1, 0),
    'leadership': (1, 0),
    'final':      (1, 0),
    'tech':       (0, 0),
}

# Must survive. The rail sits inside .folder, and an over-eager brace match would take the
# folder with it — which is exactly the failure this list exists to catch.
KEEP = ['folder', 'tabrow', 'cols2', 'lampband' ]

RAIL = re.compile(r'\s*<div class="frail">\s*(?:<span class="hole"[^>]*></span>\s*)+</div>')
MARK = re.compile(r'<span class="pmark">\(S\)</span>\s*')


def main():
    write = '--write' in sys.argv
    total = 0
    for doc, (n_rail, n_mark) in EXPECT.items():
        path = os.path.join(DOC, '%s.html' % doc)
        src = io.open(path, encoding='utf-8').read()
        rails, marks = RAIL.findall(src), MARK.findall(src)
        if len(rails) != n_rail or len(marks) != n_mark:
            print('  REFUSED %s: expected %d rail / %d mark, found %d / %d'
                  % (doc, n_rail, n_mark, len(rails), len(marks)))
            return 1
        out = MARK.sub('', RAIL.sub('', src))
        for k in KEEP:
            if src.count(k) != out.count(k):
                print('  REFUSED %s: the cut disturbed %r (%d -> %d)'
                      % (doc, k, src.count(k), out.count(k)))
                return 1
        gone = len(src) - len(out)
        total += gone
        if gone:
            print('  %-11s %4d B   %d rail%s, %d mark%s'
                  % (doc, gone, n_rail, '' if n_rail == 1 else 's',
                     n_mark, '' if n_mark == 1 else 's'))
        if write and gone:
            io.open(path, 'w', encoding='utf-8', newline='').write(out)
    print()
    print('  %d bytes%s' % (total, '' if write else '  (dry run)'))
    if write:
        print('  now run:  python build.py')
    return 0


if __name__ == '__main__':
    sys.exit(main())
