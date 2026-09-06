# -*- coding: utf-8 -*-
"""Renumber the seven files — settled in Stage 3, corrected in Stage 7.

Two numbering systems were running at once and both were stale. `.secnum` read 03–08, which
were positions in the old scrolling page, not file numbers. `.tok` numbered only the first
four; LEADERSHIP and TECH carried no number at all, and FINAL carried "END OF FILE".

FINAL becomes FILE 07, which was Oran's correction to me and the reason is arithmetic: a
reader who opens all six documents and then READ ME must be able to reach `7 of 7`. If FINAL
is not a file, the counter can never complete. He also has it counted as a file in the folder
status line, so anything else would contradict what the shell already says.

FINAL has no `.secnum` at all, so one is inserted, in the position the other six use: directly
before `.wrap`, and aria-hidden, because it is a visual index and not something to read aloud.

    python tools/renumber_files.py           report
    python tools/renumber_files.py --write   apply
"""
import io
import os
import re
import sys

sys.stdout.reconfigure(encoding='utf-8', errors='replace')
HERE = os.path.dirname(os.path.abspath(__file__))
DOC = os.path.join(os.path.dirname(HERE), 'src', 'doc')

# file -> (secnum, tok). The tok descriptors continue the pattern the first four established.
WANT = [
    ('xtix',       '01', 'FILE 01 &middot; INTAKE'),
    ('oasis',      '02', 'FILE 02 &middot; COMMAND'),
    ('eventer',    '03', 'FILE 03 &middot; SYNC'),
    ('medcoin',    '04', 'FILE 04 &middot; ORIGIN'),
    ('leadership', '05', 'FILE 05 &middot; MANAGEMENT'),
    ('tech',       '06', 'FILE 06 &middot; SYSTEM'),
    ('final',      '07', 'FILE 07 &middot; PRINCIPLES'),
]

SECNUM = re.compile(r'(<div class="secnum"[^>]*>)([^<]*)(</div>)')
TOK = re.compile(r'(<div class="tok"[^>]*>)([^<]*)(</div>)')


def main():
    write = '--write' in sys.argv
    changed = 0
    for doc, num, tok in WANT:
        path = os.path.join(DOC, '%s.html' % doc)
        src = io.open(path, encoding='utf-8').read()
        out = src

        if SECNUM.search(out):
            was = SECNUM.search(out).group(2)
            out = SECNUM.sub(lambda m: m.group(1) + num + m.group(3), out, count=1)
        else:
            # FINAL: insert one, in the position the other six use.
            anchor = '<div class="wrap">'
            if out.count(anchor) < 1:
                print('  REFUSED %s: no .wrap to anchor the number to' % doc)
                return 1
            i = out.index(anchor)
            indent = ''
            j = i
            while j > 0 and out[j - 1] in ' \t':
                indent = out[j - 1] + indent
                j -= 1
            out = (out[:j] + indent + '<div class="secnum" aria-hidden="true">' + num
                   + '</div>\n' + indent + out[i:])
            was = '(absent)'

        if not TOK.search(out):
            print('  REFUSED %s: no .tok' % doc)
            return 1
        was_tok = TOK.search(out).group(2)
        out = TOK.sub(lambda m: m.group(1) + tok + m.group(3), out, count=1)

        if out != src:
            changed += 1
            print('  %-11s secnum %-9s -> %-4s   tok %-24s -> %s'
                  % (doc, was, num, was_tok, tok))
            if write:
                io.open(path, 'w', encoding='utf-8', newline='').write(out)

    print()
    print('  %d of %d files changed%s' % (changed, len(WANT), '' if write else '  (dry run)'))
    if write:
        print('  now run:  python build.py')
    return 0


if __name__ == '__main__':
    sys.exit(main())
