# -*- coding: utf-8 -*-
"""Harvest the HERO copy into the bottom of page 1.

Oran: *"אל תמחק לנו לחלוטין את HERO, תסיר אותו ושמור אותו בצד"* — do not delete it, take it out
and keep it aside. And the plan: page 1 is today's statement, the neural-net canvas and its
sentence, with the harvested HERO copy beneath it.

WHAT MOVES, AND WHY IT IS NESTED RATHER THAN COPIED OUT.

Fifty-nine CSS rules style this card and every one of them is written `#hero .something`. Lifting
the markup into #statement would have left the card unstyled — the title at browser-default
size, the serif line gone, the folder shape gone. So the element keeps its id and moves whole:
it becomes a <div id="hero"> nested inside #statement, and every descendant selector still
matches, because a descendant selector does not care where its ancestor lives.

WHERE. #statement is a pinned sequence — .pinh is 175vh tall and .pin sticks to the top through
it while the canvas runs. The bottom of page 1 is therefore after .pinh, not inside it, which is
where this puts the card.

TWO LINES COME OUT, both named by Oran:
    E X E C U T I V E   P O R T F O L I O
    FOUR COMPANIES — 2018–2026

Everything else HERO carried — the marquee, ARCHIVE N°, STATUS: ACTIVE, the drawer lip, SCROLL
TO OPEN — is furniture for a screen that no longer exists. It is written to src/harvest/hero.html
whole, which is the "keep it aside" he asked for, rather than living only in a commit.

    python tools/harvest_hero.py           report
    python tools/harvest_hero.py --write   do it
"""
import io
import os
import re
import sys

sys.stdout.reconfigure(encoding='utf-8', errors='replace')
HERE = os.path.dirname(os.path.abspath(__file__))
REPO = os.path.dirname(HERE)
MONO = os.path.join(REPO, 'src', '_monolith.html')
KEEP = os.path.join(REPO, 'src', 'harvest')

# named by Oran, and asserted so a rewording upstream stops this rather than silently missing
DROP = [
    ('<div class="kick">E X E C U T I V E &nbsp; P O R T F O L I O</div>', 'EXECUTIVE PORTFOLIO'),
    ('<span class="idy">FOUR COMPANIES &mdash; 2018&ndash;2026</span>', 'FOUR COMPANIES'),
]
# must survive the move, or the card has lost the thing it exists to say
SURVIVE = ['THE COMMERCIAL<br>SYSTEMS BUILDER', 'From Vision to Measurable Growth',
           'BY <b>ORAN CARMON</b>', 'COMMERCIAL GROWTH', 'CROSS-FUNCTIONAL EXECUTION']


def section(html, sid):
    i = html.index('id="%s"' % sid)
    i = html.rindex('<section', 0, i)
    j = html.index('</section>', i) + len('</section>')
    return i, j


def main():
    write = '--write' in sys.argv
    s = io.open(MONO, encoding='utf-8').read()

    h0, h1 = section(s, 'hero')
    hero = s[h0:h1]
    for frag, label in DROP:
        if hero.count(frag) != 1:
            print('  REFUSED: %s appears %d times, expected 1' % (label, hero.count(frag)))
            return 1
    for k in SURVIVE:
        if k not in hero:
            print('  REFUSED: %r is not in HERO; the copy has changed' % k[:40])
            return 1

    # the card, as it will live inside page 1
    card = hero
    for frag, _ in DROP:
        card = card.replace(frag, '')
    card = card.replace('<section class="sec" id="hero">', '<div id="hero" class="harvested">', 1)
    card = re.sub(r'</section>\s*$', '</div>', card)
    card = re.sub(r'\n[ \t]*\n', '\n', card)

    for k in SURVIVE:
        if k not in card:
            print('  REFUSED: the card lost %r' % k[:40])
            return 1
    for _, label in DROP:
        if label.split()[0] in re.sub(r'<[^>]+>', ' ', card):
            print('  REFUSED: %s survived the cut' % label)
            return 1

    out = s[:h0] + s[h1:]                       # HERO leaves the flow

    # and lands at the bottom of page 1, after the pinned sequence
    st0, st1 = section(out, 'statement')
    stmt = out[st0:st1]
    anchor = '</section>'
    if not stmt.endswith(anchor):
        print('  REFUSED: #statement does not end where expected')
        return 1
    stmt_new = stmt[:-len(anchor)] + '\n' + card + '\n' + anchor
    out = out[:st0] + stmt_new + out[st1:]

    print('  HERO             %5d B  removed from the flow' % (h1 - h0))
    print('  the card         %5d B  nested into #statement, after the pinned sequence' % len(card))
    print('  dropped          %s' % ', '.join(l for _, l in DROP))
    print('  kept aside       src/harvest/hero.html')
    print('  sections         %d -> %d' % (s.count('<section'), out.count('<section')))

    if write:
        if not os.path.isdir(KEEP):
            os.makedirs(KEEP)
        io.open(os.path.join(KEEP, 'hero.html'), 'w', encoding='utf-8', newline='').write(hero)
        io.open(MONO, 'w', encoding='utf-8', newline='').write(out)
        print('  now run:  python build.py')
    else:
        print('  (dry run)')
    return 0


if __name__ == '__main__':
    sys.exit(main())
