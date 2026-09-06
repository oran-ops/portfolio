# -*- coding: utf-8 -*-
"""Slice the mesh with a plane and hand back the outline as a polyline.

The side view showed the case is raked at the front, stepped at the chin and sloped across the
roof - none of which a straight extrusion can produce, so no amount of tuning my existing
parameters was ever going to close the gap. A cross-section turns that shape into the one thing
my generator can actually consume: an ordered list of points.

Chaining is done on welded endpoints. Floating point makes two segments that share a corner
disagree in the last bit, and a loop that breaks there silently becomes two open chains.
"""
import sys

import numpy as np

from meshlib import islands, load


def section(co, tris, axis, value, keep=None):
    """intersect with the plane axis=value; returns a list of closed/open polylines in the
    other two axes, as (u, v) with u,v the axes in cyclic order after `axis`"""
    u, v = [k for k in (0, 1, 2) if k != axis]
    if keep is not None:
        tris = tris[keep]
    d = co[:, axis] - value
    dt = d[tris]                                   # (n,3) signed distance per corner
    hit = ~((dt > 0).all(1) | (dt < 0).all(1))
    t = tris[hit]
    if len(t) == 0:
        return []
    segs = []
    for tri in t:
        pts = []
        for a, b in ((0, 1), (1, 2), (2, 0)):
            da, db = d[tri[a]], d[tri[b]]
            if (da > 0) == (db > 0):
                continue
            if da == db:
                continue
            w = da / (da - db)
            p = co[tri[a]] + (co[tri[b]] - co[tri[a]]) * w
            pts.append((p[u], p[v]))
        if len(pts) >= 2:
            segs.append((pts[0], pts[1]))
    if not segs:
        return []

    # weld endpoints onto a grid so shared corners really are shared
    G = 1e-5
    node = {}
    idx = []
    P = []
    for s in segs:
        pair = []
        for p in s:
            k = (round(p[0] / G), round(p[1] / G))
            j = node.get(k)
            if j is None:
                j = len(P)
                node[k] = j
                P.append(p)
            pair.append(j)
        if pair[0] != pair[1]:
            idx.append(tuple(pair))

    adj = {}
    for a, b in idx:
        adj.setdefault(a, []).append(b)
        adj.setdefault(b, []).append(a)

    used = set()
    loops = []
    for a, bs in adj.items():
        if len(bs) == 1 and a not in used:          # open chain: start at a loose end
            loops.append(_walk(a, adj, used, idx))
    for a in adj:
        if a not in used:
            loops.append(_walk(a, adj, used, idx))
    return [np.array([P[i] for i in L]) for L in loops if len(L) > 2]


def _walk(start, adj, used, idx):
    chain = [start]
    used.add(start)
    cur = start
    while True:
        nxt = None
        for c in adj.get(cur, ()):
            if c not in used:
                nxt = c
                break
        if nxt is None:
            break
        chain.append(nxt)
        used.add(nxt)
        cur = nxt
    return chain


def simplify(pts, tol):
    """Douglas-Peucker, so the printed profile is something a human can read and a generator
    can use, instead of one point per triangle edge"""
    if len(pts) < 3:
        return pts
    a, b = pts[0], pts[-1]
    ab = b - a
    L = np.hypot(*ab)
    if L < 1e-12:
        dist = np.hypot(*(pts - a).T)
    else:
        dist = np.abs(np.cross(np.tile(ab, (len(pts), 1)), pts - a)) / L
    i = int(dist.argmax())
    if dist[i] > tol:
        return np.vstack([simplify(pts[:i + 1], tol)[:-1], simplify(pts[i:], tol)])
    return np.vstack([a, b])


if __name__ == '__main__':
    PATH = sys.argv[1] if len(sys.argv) > 1 else r'C:\Users\Alex\Downloads\Mac.blend'
    co, tris, tmat, blend = load(PATH)
    lab, nisl = islands(co, tris)

    # island 0 is the case shell: 9.539 x 10.845 x 13.341 in, the only piece that size
    counts = np.bincount(lab[tris[:, 0]], minlength=nisl)
    sizes = []
    for i in np.argsort(-counts)[:40]:
        p = co[np.unique(tris[lab[tris[:, 0]] == i])]
        sizes.append((i, p.max(0) - p.min(0), p.min(0), p.max(0)))
    case = max(sizes, key=lambda e: float(np.prod(e[1])))[0]
    keep = lab[tris[:, 0]] == case
    p = co[np.unique(tris[keep])]
    print('case island %d   bbox %s .. %s   size %s'
          % (case, np.round(p.min(0), 3), np.round(p.max(0), 3), np.round(p.max(0) - p.min(0), 3)))

    print()
    print('--- SIDE PROFILE  (plane x = 0, axes Y=depth, Z=height, inches) ---')
    for L in section(co, tris, 0, 0.0, keep):
        s = simplify(L, 0.012)
        print('  loop, %d pts -> %d after simplify' % (len(L), len(s)))
        for q in s:
            print('     Y %8.3f   Z %8.3f' % (q[0], q[1]))

    print()
    print('--- PLAN SECTIONS  (horizontal, width x depth at a given height) ---')
    for z in (0.5, 1.5, 3.0, 5.0, 7.0, 9.0, 11.0, 12.5, 13.2):
        Ls = section(co, tris, 2, z, keep)
        if not Ls:
            continue
        allp = np.vstack(Ls)
        print('  z=%5.2f in :  width %7.3f  depth %7.3f   (x %7.3f..%7.3f, y %7.3f..%7.3f)'
              % (z, allp[:, 0].ptp(), allp[:, 1].ptp(),
                 allp[:, 0].min(), allp[:, 0].max(), allp[:, 1].min(), allp[:, 1].max()))

    print()
    print('--- FRONT-FACE SECTIONS  (vertical, at a given depth y) ---')
    for y in (-6.05, -6.0, -5.8, -5.5, -5.0, -4.5):
        Ls = section(co, tris, 1, y, keep)
        if not Ls:
            continue
        allp = np.vstack(Ls)
        print('  y=%6.2f in :  width %7.3f  height %7.3f  (z %7.3f..%7.3f)'
              % (y, allp[:, 0].ptp(), allp[:, 1].ptp(), allp[:, 1].min(), allp[:, 1].max()))
