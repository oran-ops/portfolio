# -*- coding: utf-8 -*-
"""Before cutting a class, find out what depends on it.

Written after cutting `.clsband`, the RESTRICTED strip, which looked like pure ornament and was
in fact the UV lamp module's entry condition:

    var band = sec.querySelector('.clsband'); if (!band) return;

Twelve developed zones, four lamps and eight film edges went with it, silently — a missing
anchor returns rather than throwing, so there was no console error and no failed build. Only
counting the same selectors in the committed page and in the new one showed it.

A keep-list is not enough on its own. The one guarding that cut asserted `lampband` survived,
and passed *vacuously*: `lampband` is never in `src/doc/*.html` at all, because the page builds
it at runtime. A check that looks for a string in a file that never held it always succeeds.

    python tools/depends.py clsband frail hole otx

For each name, this reports every JavaScript reference in the source, split into the ones that
merely mention it and the ones that GATE on it — a querySelector whose result is tested, which
is where a silent death comes from.
"""
import io
import os
import re
import sys

sys.stdout.reconfigure(encoding='utf-8', errors='replace')
HERE = os.path.dirname(os.path.abspath(__file__))
SRC = os.path.join(os.path.dirname(HERE), 'src')


def sources():
    for root, _dirs, files in os.walk(SRC):
        for f in sorted(files):
            if f.endswith(('.html', '.js')):
                p = os.path.join(root, f)
                yield os.path.relpath(p, os.path.dirname(HERE)), io.open(
                    p, encoding='utf-8', errors='replace').read()


def scripts_only(text):
    """Only the parts a browser executes. Markup mentioning a class is not a dependency."""
    out = []
    i = 0
    while True:
        a = text.find('<script', i)
        if a < 0:
            break
        a = text.find('>', a)
        b = text.find('</script>', a)
        if a < 0 or b < 0:
            break
        out.append((a + 1, text[a + 1:b]))
        i = b
    return out


GATE = re.compile(r'(querySelector(?:All)?|closest|getElementsByClassName|matches)\s*\(')


def main():
    names = [a for a in sys.argv[1:] if not a.startswith('-')]
    if not names:
        print(__doc__.strip().splitlines()[0])
        print('\n  usage: python tools/depends.py <class> [<class> ...]')
        return 2

    for name in names:
        print('=' * 78)
        print('.%s' % name)
        print('=' * 78)
        gates, mentions = [], []
        for path, text in sources():
            for base, js in scripts_only(text):
                for m in re.finditer(re.escape(name), js):
                    a = max(0, m.start() - 150)
                    frag = ' '.join(js[a:m.end() + 110].split())
                    # a gate is a lookup whose result decides whether code continues
                    look = GATE.search(js[max(0, m.start() - 60):m.start() + 40])
                    guarded = re.search(r'if\s*\(\s*!\s*\w+\s*\)\s*return', js[m.start():m.start() + 260])
                    (gates if (look and guarded) else mentions).append((path, frag))

        if gates:
            print('  GATES — code that stops if this is missing. Cutting it kills a feature:')
            for path, frag in gates:
                print('     %s' % path)
                print('       …%s…' % frag[-190:])
        else:
            print('  no gates found')
        print()
        print('  other references in script: %d' % len(mentions))
        for path, frag in mentions[:4]:
            print('     %-24s …%s…' % (path, frag[-110:]))
        if len(mentions) > 4:
            print('     … and %d more' % (len(mentions) - 4))
        print()
    return 0


if __name__ == '__main__':
    sys.exit(main())
