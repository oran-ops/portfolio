# -*- coding: utf-8 -*-
"""Corner radii, read off the outline instead of fitted over a window that is mostly straight.

Both earlier circle fits included long straight runs of edge, and a circle fitted through a
straight line comes back enormous with a fat residual - 1.293 in for a corner and 1.779 in for
the screen opening, neither of them real. A corner is where the outline leaves its own straight
edges, so find the straight edges first, then fit only the points that depart from both.
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
fimg, flo, PX = raster(co, tris, keep, 0, 2, 1, -1.0)
fmask = ~np.isnan(fimg)
H, W = fmask.shape


def right_edge(mask, z):
    r = int((z - flo[1]) / PX)
    if r < 0 or r >= H or not mask[r].any():
        return None
    return flo[0] + np.where(mask[r])[0][-1] * PX


def corner_fit(pts, tol=0.004):
    """fit a circle to pts; report radius and worst deviation"""
    P = np.asarray(pts, float)
    M = np.c_[2 * P, np.ones(len(P))]
    s = np.linalg.lstsq(M, (P ** 2).sum(1), rcond=None)[0]
    R = np.sqrt(max(s[2] + s[0] ** 2 + s[1] ** 2, 0))
    res = np.abs(np.hypot(P[:, 0] - s[0], P[:, 1] - s[1]) - R).max()
    return R, res, s[0], s[1]


print('FRONT OUTLINE, top-right corner  (right edge x at each height)')
print('%8s | %9s' % ('z', 'right x'))
rows = []
for z in np.arange(12.8, 13.60, 0.02):
    x = right_edge(fmask, z)
    if x is None:
        continue
    rows.append((z, x))
    print('%8.2f | %+9.3f' % (z, x))

A = np.array(rows)
straight = A[A[:, 1] > A[:, 1].max() - 0.004]
zbreak = straight[:, 0].max()
ztop = A[:, 0].max()
print()
print('side edge is straight (x=%+.3f) up to z=%.2f;  outline ends at z=%.2f'
      % (A[:, 1].max(), zbreak, ztop))
cor = A[A[:, 0] > zbreak]
if len(cor) >= 4:
    R, res, cx, cz = corner_fit(np.c_[cor[:, 1], cor[:, 0]])
    print('top-right corner radius  %.3f in   (%d pts, max deviation %.4f in, centre %+.2f %.2f)'
          % (R, len(cor), res, cx, cz))
print('corner runs over %.3f in of height and %.3f in of width'
      % (ztop - zbreak, A[:, 1].max() - cor[:, 1].min() if len(cor) else 0))

print()
print('FRONT OUTLINE, bottom-right corner')
rows = []
for z in np.arange(0.22, 1.10, 0.02):
    x = right_edge(fmask, z)
    if x is not None:
        rows.append((z, x))
B = np.array(rows)
print('   x at z=0.24 %+.3f   z=0.40 %+.3f   z=0.80 %+.3f   z=1.00 %+.3f'
      % (B[1, 1], B[np.abs(B[:, 0] - .40).argmin(), 1],
         B[np.abs(B[:, 0] - .80).argmin(), 1], B[np.abs(B[:, 0] - 1.0).argmin(), 1]))
lowc = B[B[:, 1] < B[:, 1].max() - 0.004]
if len(lowc) >= 4:
    R, res, cx, cz = corner_fit(np.c_[lowc[:, 1], lowc[:, 0]])
    print('bottom-right corner radius %.3f in  (%d pts, dev %.4f)' % (R, len(lowc), res))
else:
    print('bottom corner: square to within %.3f in' % PX)

# ---- the screen opening's top-right corner --------------------------------
RAKE_M, RAKE_C = 0.11858, -6.4069
depth = -fimg
zrow = flo[1] + np.arange(H) * PX
face = RAKE_M * zrow + RAKE_C
onface = (~np.isnan(depth)) & (np.abs(depth - face[:, None]) < 0.06)
opening = ~onface & (np.arange(W)[None, :] > -1)
print()
print('SCREEN OPENING, top-right and bottom-right corners')
rows = []
for z in np.arange(6.0, 12.45, 0.02):
    r = int((z - flo[1]) / PX)
    o = opening[r]
    c = np.where(o)[0]
    if not len(c):
        continue
    br = np.split(c, np.where(np.diff(c) > 8)[0] + 1)
    run = max(br, key=len)
    if len(run) * PX < 1.0 or not onface[r, :run[0]].any() or not onface[r, run[-1]:].any():
        continue
    rows.append((z, flo[0] + run[0] * PX, flo[0] + run[-1] * PX))
O = np.array(rows)
xmax = O[:, 2].max()
print('   opening right edge straight at x=%+.3f' % xmax)
for tag, sel in (('top', O[:, 0] > O[:, 0].max() - 1.2), ('bottom', O[:, 0] < O[:, 0].min() + 1.2)):
    q = O[sel]
    q = q[q[:, 2] < xmax - 0.004]
    if len(q) >= 4:
        R, res, cx, cz = corner_fit(np.c_[q[:, 2], q[:, 0]])
        print('   %-6s corner radius %.3f in  (%d pts, dev %.4f)' % (tag, R, len(q), res))
    else:
        print('   %-6s corner: less than %d pts depart the straight edge' % (tag, 4))
print('   opening z %.2f .. %.2f   x %+.3f .. %+.3f' % (O[:, 0].min(), O[:, 0].max(),
                                                        O[:, 1].min(), O[:, 2].max()))
