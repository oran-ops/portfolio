# -*- coding: utf-8 -*-
"""Move one section out of src/_monolith.html into src/doc/<id>.html.

    python tools/cut_section.py oasis
    python tools/cut_section.py oasis --css      also move its exclusively-scoped rules

The section is replaced by a marker, `<!--DOC:oasis-->`, which `build.py` expands again. Because
the text is stored verbatim and substituted verbatim, a correct cut leaves the built page
**byte-for-byte unchanged** — so `build.py` reporting MATCH is the proof, and no screenshot,
render or judgement is involved.

Markup and CSS are separate invocations on purpose. One change at a time is not a style
preference here: it is the only reason a MATCH means anything.

**CSS is moved only when the section is its sole owner.** A rule reading
`#xtix .lessq, #oasis .lessq, #eventer .lessq` belongs to three documents at once, and moving it
with the first one to leave would silently unstyle the other two. Those are counted, reported,
and left where they are until ARCHITECTURE.md §11.3 decides each of them.
"""
import io
import os
import re
import sys

sys.stdout.reconfigure(encoding='utf-8', errors='replace')
HERE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
MONO = os.path.join(HERE, 'src', '_monolith.html')
DOCDIR = os.path.join(HERE, 'src', 'doc')

SECTIONS = ['hero', 'statement', 'philosophy', 'files', 'xtix', 'oasis',
            'eventer', 'medcoin', 'leadership', 'tech', 'final']


def find_section(s, sid):
    """(start, end) of <section id="sid"> … </section>, counting nesting properly"""
    m = re.search(r'<section[^>]*\bid="%s"' % re.escape(sid), s)
    if not m:
        return None
    a = s.rindex('<section', 0, m.end())
    depth, i = 0, a
    while True:
        o, c = s.find('<section', i + 1), s.find('</section>', i + 1)
        if c == -1:
            raise SystemExit('unbalanced <section> after %s' % sid)
        if o != -1 and o < c:
            depth += 1
            i = o
        else:
            if depth == 0:
                return a, c + len('</section>')
            depth -= 1
            i = c


def style_spans(s):
    return [(m.start(), m.end()) for m in re.finditer(r'<style[^>]*>.*?</style>', s, re.S)]


def main():
    sid = sys.argv[1] if len(sys.argv) > 1 else None
    if sid not in SECTIONS:
        raise SystemExit('usage: cut_section.py <%s> [--css]' % '|'.join(SECTIONS))
    do_css = '--css' in sys.argv

    s = io.open(MONO, encoding='utf-8').read()
    marker = '<!--DOC:%s-->' % sid

    if do_css:
        if marker not in s:
            raise SystemExit('cut the markup first: python tools/cut_section.py %s' % sid)
        spans = style_spans(s)
        mine, shared = [], []
        for m in re.finditer(r'([^{}<>]*#%s[^{}<>]*)\{([^{}]*)\}' % sid, s):
            if not any(a <= m.start() < b for a, b in spans):
                continue
            a, b = m.start(), m.end()
            # Do not swallow a marker left by an earlier cut. `/*D:leadership:0*/` contains no
            # brace and no angle bracket, so the greedy run in front of the selector will
            # happily absorb it — and then that section's rules have no home to return to. The
            # build caught this on `tech`; the rule is: a match starts after any marker inside
            # its own selector text.
            for mk in re.finditer(r'/\*D:\w+:\d+\*/', m.group(1)):
                a = max(a, m.start() + mk.end())
            others = [x for x in SECTIONS if x != sid and '#' + x in m.group(1)]
            (shared if others else mine).append((a, b, s[a:b], others))
        print('rules mentioning #%s inside <style>: %d' % (sid, len(mine) + len(shared)))
        print('  exclusively this section : %d  -> moving' % len(mine))
        print('  shared with others       : %d  -> left in place (ARCHITECTURE §11.3)' % len(shared))
        for _, _, _, others in shared:
            print('     shared with %s' % ', '.join(others))
        if not mine:
            print('nothing exclusive to move.')
            return 0
        # Stored verbatim, with no separator of our own between marker and rule.
        #
        # The first version wrote '/*--0--*/\n' + rule and joined the parts with '\n', so the
        # reader had to guess which newlines were the format's and which were the rule's. It
        # guessed wrong: two of these rules begin with a newline of their own, the reader
        # stripped them, and the page came out two bytes short. The ratchet caught it, but the
        # right answer is a format with nothing to guess about.
        out, parts = [], []
        last = 0
        for n, (a, b, text, _) in enumerate(sorted(mine)):
            out.append(s[last:a])
            out.append('/*D:%s:%d*/' % (sid, n))
            parts.append('/*--%d--*/%s' % (n, text))
            last = b
        out.append(s[last:])
        io.open(os.path.join(DOCDIR, sid + '.css'), 'w', encoding='utf-8',
                newline='').write(''.join(parts))
        result = ''.join(out)
        # every marker that was there must still be there, plus the ones just added
        was = len(re.findall(r'/\*D:\w+:\d+\*/', s))
        now = len(re.findall(r'/\*D:\w+:\d+\*/', result))
        if now != was + len(mine):
            raise SystemExit('marker count went %d -> %d, expected %d: a cut took something '
                             'it should not have' % (was, now, was + len(mine)))
        io.open(MONO, 'w', encoding='utf-8', newline='').write(result)
        print()
        print('wrote src/doc/%s.css  (%d rules, markers %d -> %d)' % (sid, len(mine), was, now))
        print('now run: python build.py     (expect MATCH)')
        return 0

    if marker in s:
        raise SystemExit('%s has already been cut.' % sid)
    span = find_section(s, sid)
    if not span:
        raise SystemExit('no <section id="%s"> in the monolith' % sid)
    a, b = span
    body = s[a:b]
    os.makedirs(DOCDIR, exist_ok=True)
    io.open(os.path.join(DOCDIR, sid + '.html'), 'w', encoding='utf-8', newline='').write(body)
    io.open(MONO, 'w', encoding='utf-8', newline='').write(s[:a] + marker + s[b:])
    print('cut  <section id="%s">  %d bytes  ->  src/doc/%s.html' % (sid, len(body.encode()), sid))
    print('     monolith %d -> %d KB' % (len(s.encode()) // 1024,
                                         (len(s.encode()) - len(body.encode())) // 1024))
    print()
    print('now run: python build.py     (expect MATCH)')
    return 0


if __name__ == '__main__':
    sys.exit(main())
