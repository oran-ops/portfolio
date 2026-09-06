# -*- coding: utf-8 -*-
"""The screen well: its opening, its walls and how deep it is.

The previous attempt tested `depth > face + 0.06` and nothing else, so it swallowed every pixel
that sees straight through the opening to the inside of the rear panel ten inches away, and duly
reported a well 9.6 in wide and 9.9 in deep - the whole machine. Bounded at both ends now.

Rather than a bounding box, this reports the opening row by row. The opening is a rounded
rectangle and its per-row width IS the outline, which is what a generator consumes; a box would
throw the corner radius away and I would be back to guessing it.
"""
import sys

import numpy as np

from meshlib import boxes, islands, load, raster

PATH = sys.argv[1] if len(sys.argv) > 1 else r'C:\Users\Alex\Downloads\Mac.blend'
co, tris, tmat, blend = load(PATH)
lab, nisl = islands(co, tris)
bx = boxes(co, tris, tmat, lab, nisl)
bx.sort(key=lambda e: -float(np.prod(e['size'] + 1e-6)))
CASE = bx[0]
keep = lab[tris[:, 0]] == CASE['id']

RAKE_M, RAKE_C = 0.11858, -6.4069            # front face plane, from spec2
fimg, flo, PX = raster(co, tris, keep, 0, 2, 1, -1.0)
depth = -fimg
H, W = depth.shape
zrow = flo[1] + np.arange(H) * PX
face = RAKE_M * zrow + RAKE_C

onface = (~np.isnan(depth)) & (np.abs(depth - face[:, None]) < 0.06)
wall = (~np.isnan(depth)) & (depth > face[:, None] + 0.06) & (depth < face[:, None] + 1.6)
through = np.isnan(depth) | ((~np.isnan(depth)) & (depth > face[:, None] + 1.6))
opening = wall | through

print('front face pixels on the raked plane : %d' % onface.sum())
print('well wall pixels (0.06..1.6 in deep) : %d' % wall.sum())
print('see-through pixels                   : %d' % through.sum())

print()
print('OPENING, ROW BY ROW  (only rows whose opening is wider than 1 in)')
print('%8s | %8s %8s | %7s | %8s' % ('z (in)', 'left x', 'right x', 'width', 'wall dp'))
print('-' * 52)
rows = []
# above z=12.4 the raked face has ended, so 'not on the face' means 'not the face at
# all' and every row reads as a 9.6 in opening. Stop where the face stops.
for z in np.arange(5.6, 12.45, 0.1):
    r = int((z - flo[1]) / PX)
    if r < 0 or r >= H:
        continue
    o = opening[r]
    if not o.any():
        continue
    c = np.where(o)[0]
    # ignore stray fittings: take the widest run
    br = np.split(c, np.where(np.diff(c) > 8)[0] + 1)
    run = max(br, key=len)
    if len(run) * PX < 1.0 or not onface[r, :run[0]].any() or not onface[r, run[-1]:].any():
        continue
    x0 = flo[0] + run[0] * PX
    x1 = flo[0] + run[-1] * PX
    dw = depth[r][wall[r]]
    wd = np.median(dw - face[r]) if dw.size else float('nan')
    rows.append((z, x0, x1, x1 - x0, wd))
    print('%8.2f | %+8.3f %+8.3f | %7.3f | %8.3f' % rows[-1])

if rows:
    A = np.array(rows)
    zmin, zmax = A[0, 0], A[-1, 0]
    wmax = A[:, 3].max()
    flat = A[A[:, 3] > wmax - 0.02]
    print()
    print('opening         %.3f wide x %.3f tall     z %.2f .. %.2f'
          % (wmax, zmax - zmin + 0.1, zmin, zmax))
    print('                x %+.3f .. %+.3f   centre x %+.3f  z %+.3f'
          % (A[:, 1].min(), A[:, 2].max(), (A[:, 1].min() + A[:, 2].max()) / 2,
             (zmin + zmax) / 2))
    print('                case centre x %+.3f  z %+.3f   -> offset %+.3f, %+.3f'
          % (CASE['ctr'][0], CASE['ctr'][2],
             (A[:, 1].min() + A[:, 2].max()) / 2 - CASE['ctr'][0],
             (zmin + zmax) / 2 - CASE['ctr'][2]))
    print('                full width over z %.2f .. %.2f' % (flat[0, 0], flat[-1, 0]))
    d = np.nanmedian(A[:, 4])
    print('                wall depth below the raked face: median %.3f in' % d)

    # corner radius of the opening: fit a circle to the top-right shoulder
    top = A[A[:, 0] > zmax - 1.6]
    if len(top) > 6:
        P = np.c_[top[:, 2], top[:, 0]]
        M = np.c_[2 * P, np.ones(len(P))]
        s = np.linalg.lstsq(M, (P ** 2).sum(1), rcond=None)[0]
        R = np.sqrt(s[2] + s[0] ** 2 + s[1] ** 2)
        res = np.abs(np.hypot(P[:, 0] - s[0], P[:, 1] - s[1]) - R).max()
        print('                opening corner radius %.3f in (%d pts, resid %.4f)'
              % (R, len(P), res))

# the glass, for comparison
scr = [e for e in bx if e['mat'] == 1 and e['size'][0] > 5][0]
print()
print('CRT glass       %.3f x %.3f   centre x %+.3f  z %+.3f   front y %+.3f'
      % (scr['size'][0], scr['size'][2], scr['ctr'][0], scr['ctr'][2], scr['lo'][1]))
print('                glass sits %.3f in inside the opening on each side, %.3f top/bottom'
      % ((wmax - scr['size'][0]) / 2, ((zmax - zmin + 0.1) - scr['size'][2]) / 2))
