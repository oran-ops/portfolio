# -*- coding: utf-8 -*-
"""The case outline as an ordered closed polyline - the thing the generator extrudes.

Per-row min/max was enough to fit straight lines to, but it cannot describe a corner and it
cannot be handed to an extruder. A boundary trace can: it walks the silhouette once and returns
the outline in order, corners and all, so the profile I build from is the profile that was
measured rather than my reconstruction of it from four line equations.

Moore-neighbour tracing, then Douglas-Peucker. The simplification tolerance is stated in inches
so the error it introduces is a number I can quote rather than a setting I chose by feel.
"""
import sys

import numpy as np

from meshlib import boxes, islands, load, raster

PATH = sys.argv[1] if len(sys.argv) > 1 else r'C:\Users\Alex\Downloads\Mac.blend'
PX = 0.005


def trace(mask):
    """Moore-neighbour boundary trace of the largest filled region; returns (row, col) in order"""
    H, W = mask.shape
    start = None
    for r in range(H):
        c = np.where(mask[r])[0]
        if len(c):
            start = (r, c[0])
            break
    if start is None:
        return np.zeros((0, 2), int)
    # 8-neighbourhood, clockwise from west
    N = [(0, -1), (-1, -1), (-1, 0), (-1, 1), (0, 1), (1, 1), (1, 0), (1, -1)]
    out = [start]
    cur = start
    back = 0
    guard = 0
    while guard < 4 * H * W:
        guard += 1
        found = False
        for k in range(8):
            d = N[(back + 1 + k) % 8]
            p = (cur[0] + d[0], cur[1] + d[1])
            if 0 <= p[0] < H and 0 <= p[1] < W and mask[p]:
                # the direction we came from, as an index
                back = (N.index((-d[0], -d[1])) + 4) % 8
                back = N.index((-d[0], -d[1]))
                cur = p
                out.append(p)
                found = True
                break
        if not found:
            break
        if len(out) > 3 and cur == start:
            break
    return np.array(out)


def dp(pts, tol):
    """Douglas-Peucker on an open chain"""
    if len(pts) < 3:
        return pts
    a, b = pts[0], pts[-1]
    ab = b - a
    L = float(np.hypot(*ab))
    if L < 1e-12:
        d = np.hypot(*(pts - a).T)
    else:
        d = np.abs(ab[0] * (pts[:, 1] - a[1]) - ab[1] * (pts[:, 0] - a[0])) / L
    i = int(d.argmax())
    if d[i] > tol:
        return np.vstack([dp(pts[:i + 1], tol)[:-1], dp(pts[i:], tol)])
    return np.vstack([a, b])


co, tris, tmat, blend = load(PATH)
lab, nisl = islands(co, tris)
bx = boxes(co, tris, tmat, lab, nisl)
bx.sort(key=lambda e: -float(np.prod(e['size'] + 1e-6)))
CASE = bx[0]
keep = lab[tris[:, 0]] == CASE['id']
CX, CY, CZ = CASE['ctr']


def outline(au, av, ad, name, tol=0.010):
    img, lo, px = raster(co, tris, keep, au, av, ad, 1.0, px=PX)
    mask = ~np.isnan(img)
    # fill interior holes so the trace follows the silhouette, not the screen opening
    fill = mask.copy()
    for r in range(mask.shape[0]):
        c = np.where(mask[r])[0]
        if len(c):
            fill[r, c[0]:c[-1] + 1] = True
    b = trace(fill)
    if not len(b):
        return None
    P = np.c_[lo[0] + b[:, 1] * px, lo[1] + b[:, 0] * px]
    S = dp(P, tol)
    # worst error the simplification introduced, measured back against the traced boundary
    err = 0.0
    for i in range(len(S) - 1):
        a, bb = S[i], S[i + 1]
        L = np.hypot(*(bb - a))
        if L < 1e-9:
            continue
        seg = P[(np.minimum(a[0], bb[0]) - 1e-6 <= P[:, 0]) & (P[:, 0] <= np.maximum(a[0], bb[0]) + 1e-6)]
        if len(seg):
            d = np.abs((bb[0] - a[0]) * (seg[:, 1] - a[1]) - (bb[1] - a[1]) * (seg[:, 0] - a[0])) / L
            err = max(err, float(d.min() if len(d) else 0))
    print()
    print('%s outline: %d boundary px -> %d points at tol %.3f in' % (name, len(P), len(S), tol))
    print('   bbox  %s %.3f..%.3f   %s %.3f..%.3f'
          % ('uv'[0], P[:, 0].min(), P[:, 0].max(), 'uv'[1], P[:, 1].min(), P[:, 1].max()))
    return P, S


side = outline(1, 2, 0, 'SIDE (Y across, Z up)')
front = outline(0, 2, 1, 'FRONT (X across, Z up)')

P, S = side
print()
print('SIDE PROFILE, relative to the case centre (y%+.3f z%+.3f), in inches:' % (CY, CZ))
print('   [Y, Z]')
for q in S:
    print('   [%+8.4f, %+8.4f],' % (q[0] - CY, q[1] - CZ))

np.save('outline_side.npy', P)
np.save('outline_front.npy', front[0])
np.save('case_centre.npy', CASE['ctr'])
print()
print('saved outline_side.npy (%d pts), outline_front.npy (%d pts)' % (len(P), len(front[0])))
