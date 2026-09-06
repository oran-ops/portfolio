# -*- coding: utf-8 -*-
"""Generate src/kit/sprites.png and sprites.json — the placeholder atlas.

Not art. This exists so the renderer can be proven end to end before a single decision about
style is made, and so the atlas FORMAT is settled while it is still cheap to change. The tiles
are drawn from the ramps in tools/ramps.py, which also puts those ramps on screen where they
can be judged instead of read as hex.

Geometry, all of it following from ARCHITECTURE.md §7:

  a flat tile   64 x 32, the diamond, anchor at its centre (32, 16)
  a block of H  64 x (32 + 16H); the top face is the diamond, two side faces below it, and the
                anchor is the BASE tile's centre at (32, 16 + 16H) — so a block sits on its
                tile no matter how tall it is

THE PATH SET IS SIXTEEN TILES. A path connects to four neighbours, each either joined or not,
so there are 2^4 = 16 cases: one empty, four dead ends, four straights and corners, four
T-junctions, one crossroads. The tile to draw is chosen by a 4-bit mask — bit 0 for +x, 1 for
-x, 2 for +y, 3 for -y — which is the autotiling trick those games used, and it means a scene
stores where the path goes and never which picture to use.
"""
import io
import json
import math
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from PIL import Image, ImageDraw
from ramps import ramp

sys.stdout.reconfigure(encoding='utf-8', errors='replace')
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
KIT = os.path.join(ROOT, 'src', 'kit')

TW, TH, TZ = 64, 32, 16
STRATEGY = 'C'                      # hue-shifted + chroma arch; see docs/RAMPS.md

GROUND = ramp('#202127', STRATEGY)  # card
PATH = ramp('#E0A458', STRATEGY)    # brass
STOPS = {'xtix': ramp('#2FB380', STRATEGY), 'oasis': ramp('#E0A458', STRATEGY),
         'eventer': ramp('#5E8FBF', STRATEGY), 'medcoin': ramp('#F2F1ED', STRATEGY)}

# the diamond, in sprite coordinates, centred on (32, 16)
DIAMOND = [(32, 0), (64, 16), (32, 32), (0, 16)]
# screen offset from a tile centre to each of its four neighbours
NEIGHBOUR = [(32, 16), (-32, -16), (-32, 16), (32, -16)]     # +x, -x, +y, -y


def flat(col, edge=None):
    im = Image.new('RGBA', (TW, TH), (0, 0, 0, 0))
    d = ImageDraw.Draw(im)
    d.polygon(DIAMOND, fill=col, outline=edge or col)
    return im, (32, 16)


def block(top, left, right, h):
    """h in z units; one z unit is 16 px"""
    H = TH + TZ * h
    im = Image.new('RGBA', (TW, H), (0, 0, 0, 0))
    d = ImageDraw.Draw(im)
    lift = TZ * h
    d.polygon([(0, 16), (32, 32), (32, 32 + lift), (0, 16 + lift)], fill=left)
    d.polygon([(64, 16), (32, 32), (32, 32 + lift), (64, 16 + lift)], fill=right)
    d.polygon(DIAMOND, fill=top)
    return im, (32, 16 + lift)


def path_tile(mask):
    """one of the sixteen; `mask` is a 4-bit set of connected neighbours"""
    im = Image.new('RGBA', (TW, TH), (0, 0, 0, 0))
    d = ImageDraw.Draw(im)
    d.polygon(DIAMOND, fill=GROUND[1])
    cx, cy = 32, 16
    W = 5.0
    for bit, (dx, dy) in enumerate(NEIGHBOUR):
        if not (mask >> bit) & 1:
            continue
        ex, ey = cx + dx / 2.0, cy + dy / 2.0        # the shared edge's midpoint
        L = math.hypot(dx, dy)
        px, py = -dy / L * W, dx / L * W             # perpendicular, in screen space
        d.polygon([(cx + px, cy + py), (cx - px, cy - py),
                   (ex - px, ey - py), (ex + px, ey + py)], fill=PATH[3])
    if mask:
        # The joint, and it has to be a diamond rather than a dot.
        #
        # Two band quads meeting at an angle leave a wedge uncovered on the OUTSIDE of the
        # turn, and every corner of the route showed the notch. A round cap sized to the band's
        # half-width does not reach it either: in a 2:1 projection a tile turn is about 127
        # degrees on screen, not 90, so the wedge is wider than the band. A diamond of the
        # band's own proportions covers it and stays in perspective, which a circle would not.
        j = W * 1.9
        d.polygon([(cx, cy - j / 2), (cx + j, cy), (cx, cy + j / 2), (cx - j, cy)],
                  fill=PATH[3])
    return im, (32, 16)


def main():
    sprites = []
    for i, c in enumerate(GROUND[:4]):
        sprites.append(('ground%d' % i,) + flat(c, GROUND[0]))
    for m in range(16):
        sprites.append(('path%02d' % m,) + path_tile(m))
    for name, r in STOPS.items():
        sprites.append(('stop_%s' % name,) + block(r[3], r[1], r[2], 2))
    sprites.append(('marker',) + block(GROUND[4], GROUND[2], GROUND[3], 1))

    pad = 2
    cols = 8
    cw = max(s[1].width for s in sprites) + pad
    ch = max(s[1].height for s in sprites) + pad
    rows = (len(sprites) + cols - 1) // cols
    sheet = Image.new('RGBA', (cols * cw, rows * ch), (0, 0, 0, 0))
    atlas = {}
    for i, (name, im, anchor) in enumerate(sprites):
        x, y = (i % cols) * cw, (i // cols) * ch
        sheet.paste(im, (x, y))
        atlas[name] = {'x': x, 'y': y, 'w': im.width, 'h': im.height,
                       'ax': anchor[0], 'ay': anchor[1]}

    os.makedirs(KIT, exist_ok=True)
    sheet.save(os.path.join(KIT, 'sprites.png'), optimize=True)
    io.open(os.path.join(KIT, 'sprites.json'), 'w', encoding='utf-8', newline='').write(
        json.dumps(atlas, indent=0, sort_keys=True))

    kb = os.path.getsize(os.path.join(KIT, 'sprites.png')) / 1024.0
    print('%d sprites -> %dx%d sheet, %.1f KB  (budget 120 KB)'
          % (len(sprites), sheet.width, sheet.height, kb))
    print('  %d ground, 16 path (the full 4-bit set), %d stops, 1 marker'
          % (4, len(STOPS)))
    print('atlas: src/kit/sprites.json, %d entries' % len(atlas))


if __name__ == '__main__':
    main()
