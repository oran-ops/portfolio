# -*- coding: utf-8 -*-
"""Derive pixel-art colour ramps from the page's fixed tokens, four different ways.

The palette is closed — no new hues — but a pixel scene cannot be drawn in four flat colours.
It needs ramps: three to five stops per hue that read as light, surface and shadow. What is
open is *how* those stops are derived, and the four strategies below give visibly different
results from the same input, so there is something to actually choose between.

Everything is computed in **OKLab**, not HSL. HSL's lightness is not perceptual: sliding L on a
yellow and on a blue moves them by very different visible amounts, so an HSL ramp comes out
uneven and the mid-tones drift. OKLab was built so that equal steps look equal, which is the
entire job here.

    A  LIGHTNESS ONLY   the control. Included because it is what everyone does first and it is
                        why hand-made ramps look chalky: real light is coloured, and a highlight
                        that is only brighter reads as washed rather than lit.
    B  HUE-SHIFTED      warm toward the highlight, cool toward the shadow. The convention pixel
                        artists actually use, borrowed from painting.
    C  CHROMA-ARCHED    as B, but chroma peaks in the mid-tones and falls at both ends — light
                        washes colour out, shadow swallows it.
    D  ERA-CONSTRAINED  as C, then snapped to a 5-bit-per-channel grid, which is what the Amiga
                        and VGA-era hardware forced. Costs a little accuracy and buys a family
                        resemblance across every ramp, which is a large part of why art of that
                        period looks coherent.
"""
import io
import math
import os
import sys

sys.stdout.reconfigure(encoding='utf-8', errors='replace')

TOKENS = [
    ('emb   XTIX', '#2FB380'),
    ('brass OASIS', '#E0A458'),
    ('ice   EVENTER', '#5E8FBF'),
    ('ink   MEDCOIN', '#F2F1ED'),
    ('bg    ground', '#191A1F'),
    ('card  surface', '#202127'),
    ('grid2 edge', '#4B4E55'),
]


def hex_rgb(h):
    h = h.lstrip('#')
    return tuple(int(h[i:i + 2], 16) / 255.0 for i in (0, 2, 4))


def rgb_hex(c):
    return '#%02X%02X%02X' % tuple(max(0, min(255, round(x * 255))) for x in c)


def to_lin(c):
    return c / 12.92 if c <= 0.04045 else ((c + 0.055) / 1.055) ** 2.4


def to_srgb(c):
    return c * 12.92 if c <= 0.0031308 else 1.055 * (c ** (1 / 2.4)) - 0.055


def oklab(rgb):
    r, g, b = (to_lin(x) for x in rgb)
    l = 0.4122214708 * r + 0.5363325363 * g + 0.0514459929 * b
    m = 0.2119034982 * r + 0.6806995451 * g + 0.1073969566 * b
    s = 0.0883024619 * r + 0.2817188376 * g + 0.6299787005 * b
    l, m, s = (math.copysign(abs(v) ** (1 / 3), v) for v in (l, m, s))
    return (0.2104542553 * l + 0.7936177850 * m - 0.0040720468 * s,
            1.9779984951 * l - 2.4285922050 * m + 0.4505937099 * s,
            0.0259040371 * l + 0.7827717662 * m - 0.8086757660 * s)


def unoklab(lab):
    L, A, B = lab
    l = (L + 0.3963377774 * A + 0.2158037573 * B) ** 3
    m = (L - 0.1055613458 * A - 0.0638541728 * B) ** 3
    s = (L - 0.0894841775 * A - 1.2914855480 * B) ** 3
    r = +4.0767416621 * l - 3.3077115913 * m + 0.2309699292 * s
    g = -1.2684380046 * l + 2.6097574011 * m - 0.3413193965 * s
    b = -0.0041960863 * l - 0.7034186147 * m + 1.7076147010 * s
    return tuple(to_srgb(max(0.0, min(1.0, x))) for x in (r, g, b))


def lch(lab):
    L, a, b = lab
    return L, math.hypot(a, b), math.atan2(b, a)


def unlch(L, C, h):
    return L, C * math.cos(h), C * math.sin(h)


WARM = math.radians(55.0)      # the hue light is shifted toward: a warm orange


def ramp(base_hex, mode, n=5, spread=0.30, lo=0.10, hi=0.96):
    """n stops, darkest first.

    The range SLIDES to stay inside [lo, hi] rather than clipping against it. A symmetric ramp
    centred on a token that already sits near an end produces duplicates — the first version
    gave `#000000  #000000` for the ground and `#FDFCF8  #FDFCF8` for the ink, which is two
    wasted stops out of five on the two tokens that most need their range.
    """
    L0, C0, h0 = lch(oklab(hex_rgb(base_hex)))
    room_dn, room_up = L0 - lo, hi - L0

    # Where the token sits in its own ramp depends on where it sits in the range. A paper white
    # has no highlight and a near-black ground has no shadow; giving either a symmetric ramp
    # spends stops on colours that cannot exist. #F2F1ED came out with two identical light
    # stops before this — a fifth of the ramp, on the token that most needs its darks.
    if room_up < 0.06:
        mid = n - 1                                    # token is the lightest stop
    elif room_dn < 0.06:
        mid = 0                                        # token is the darkest stop
    else:
        mid = (n - 1) // 2

    span = 2.0 * spread
    down = min(span * (mid / float(n - 1)) if mid else 0.0, room_dn)
    up = min(span * ((n - 1 - mid) / float(n - 1)) if mid < n - 1 else 0.0, room_up)

    out = []
    for i in range(n):
        t = ((i - mid) / float(mid)) if i < mid else \
            ((i - mid) / float(n - 1 - mid) if i > mid else 0.0)
        if i == mid:
            # The token itself, untouched. Slide the range and the middle stop drifts off it —
            # the first version turned #2FB380 into #22AB79, which is not a ramp derived from
            # the palette, it is a different palette.
            out.append(rgb_hex(hex_rgb(base_hex)))
            continue
        L = L0 + (t * up if t > 0 else t * down)
        C, h = C0, h0
        if mode in ('B', 'C', 'D'):
            # rotate toward warm in the light and away from it in the shadow, along the
            # shorter arc. 12 degrees reads clearly and is far short of becoming another hue.
            d = (WARM - h0 + math.pi) % (2 * math.pi) - math.pi
            h = h0 + math.copysign(math.radians(12.0), d) * t
        if mode in ('C', 'D'):
            C = C0 * (1.0 - 0.55 * t * t)              # chroma arch: full in the mids
        c = unoklab(unlch(L, C, h))
        if mode == 'D':
            c = tuple(round(x * 31) / 31 for x in c)   # 5 bits per channel
        out.append(rgb_hex(c))
    return out


if __name__ == '__main__':
    modes = [('A', 'lightness only (the control)'),
             ('B', 'hue-shifted, warm light / cool shadow'),
             ('C', 'hue-shifted + chroma arch'),
             ('D', 'as C, snapped to 5 bits per channel')]
    lines = ['# Colour ramps — four strategies from the same fixed tokens', '',
             'Generated by `tools/ramps.py`. Computed in OKLab so equal steps look equal;',
             'in HSL they do not, and the mid-tones drift.', '']
    for code, label in modes:
        print()
        print('=' * 78)
        print('STRATEGY %s — %s' % (code, label))
        print('=' * 78)
        lines += ['## Strategy %s — %s' % (code, label), '',
                  '| token | shadow | | base | | light |', '|---|---|---|---|---|---|']
        for name, hx in TOKENS:
            r = ramp(hx, code)
            print('  %-16s %s' % (name, '  '.join(r)))
            lines.append('| `%s` | %s |' % (name.strip(), ' | '.join('`%s`' % x for x in r)))
        lines.append('')
    out = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))),
                       'docs', 'RAMPS.md')
    io.open(out, 'w', encoding='utf-8', newline='').write('\n'.join(lines))
    print()
    print('wrote docs/RAMPS.md')
