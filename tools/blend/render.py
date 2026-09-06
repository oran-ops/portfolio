# -*- coding: utf-8 -*-
"""Orthographic views of the mesh, with each piece in its own colour and numbered.

Identification has to come before measurement: a table of 341 boxes tells me their sizes and
nothing about which one is the keyboard. This draws the same arrays the table was built from,
so the number on the picture and the row in the table are the same object by construction.
"""
import sys

import numpy as np
from PIL import Image, ImageDraw

from meshlib import boxes, islands, load

PATH = sys.argv[1] if len(sys.argv) > 1 else r'C:\Users\Alex\Downloads\Mac.blend'
W = H = 1000

co, tris, tmat, blend = load(PATH)
lab, nisl = islands(co, tris)
bx = boxes(co, tris, tmat, lab, nisl)
bx.sort(key=lambda e: -float(np.prod(e['size'] + 1e-6)))
rank = {e['id']: i for i, e in enumerate(bx)}
print('%d tris, %d islands' % (len(tris), nisl))


def palette(i):
    h = (i * 0.61803398875) % 1.0
    s, v = 0.62, 1.0
    k = int(h * 6)
    f = h * 6 - k
    p, q, t = v * (1 - s), v * (1 - s * f), v * (1 - s * (1 - f))
    return [(v, t, p), (q, v, p), (p, v, t), (p, q, v), (t, p, v), (v, p, q)][k % 6]


VIEWS = {                       # (right axis, up axis, depth axis, depth sign)
    'front': (0, 2, 1, -1.0),   # camera on -Y: the keyboard side is the front
    'side':  (1, 2, 0, 1.0),    # camera on +X, so -Y (the front) is to the left
    'top':   (0, 1, 2, 1.0),    # camera above
}


def render(view, colour_by):
    ax, ay, az, sgn = VIEWS[view]
    lo, hi = co.min(0), co.max(0)
    ctr = (lo + hi) / 2
    span = max(hi[ax] - lo[ax], hi[ay] - lo[ay]) * 1.06
    sc = W / span

    def proj(p):
        x = (p[:, ax] - ctr[ax]) * sc + W / 2
        y = H / 2 - (p[:, ay] - ctr[ay]) * sc
        return x, y

    px, py = proj(co)
    depth = co[:, az] * sgn

    zbuf = np.full((H, W), -1e30)
    img = np.zeros((H, W, 3), np.float32)

    if colour_by == 'island':
        cols = np.array([palette(rank.get(int(l), 0)) for l in range(nisl)], np.float32)
        tcol = cols[lab[tris[:, 0]]]
    else:
        nm = int(tmat.max()) + 1
        cols = np.array([palette(i * 3 + 1) for i in range(nm)], np.float32)
        tcol = cols[tmat]

    a, b, c = tris[:, 0], tris[:, 1], tris[:, 2]
    v0 = co[b] - co[a]
    v1 = co[c] - co[a]
    nrm = np.cross(v0, v1)
    ln = np.linalg.norm(nrm, axis=1, keepdims=True)
    nrm = nrm / np.maximum(ln, 1e-12)
    L = np.array([0.35, -0.72, 0.60])
    L = L / np.linalg.norm(L)
    lam = np.clip(nrm @ L, 0, 1) * 0.72 + 0.28
    tcol = tcol * lam[:, None]

    x0 = np.minimum(np.minimum(px[a], px[b]), px[c])
    x1 = np.maximum(np.maximum(px[a], px[b]), px[c])
    y0 = np.minimum(np.minimum(py[a], py[b]), py[c])
    y1 = np.maximum(np.maximum(py[a], py[b]), py[c])
    order = np.argsort(-(depth[a] + depth[b] + depth[c]))   # far to near, painter + zbuf

    for t in order:
        ix0 = max(int(np.floor(x0[t])), 0)
        ix1 = min(int(np.ceil(x1[t])) + 1, W)
        iy0 = max(int(np.floor(y0[t])), 0)
        iy1 = min(int(np.ceil(y1[t])) + 1, H)
        if ix1 <= ix0 or iy1 <= iy0:
            continue
        ia, ib, ic = a[t], b[t], c[t]
        ax0, ay0 = px[ia], py[ia]
        bx0, by0 = px[ib], py[ib]
        cx0, cy0 = px[ic], py[ic]
        det = (bx0 - ax0) * (cy0 - ay0) - (cx0 - ax0) * (by0 - ay0)
        if abs(det) < 1e-9:
            continue
        gx, gy = np.meshgrid(np.arange(ix0, ix1) + 0.5, np.arange(iy0, iy1) + 0.5)
        w1 = ((gx - ax0) * (cy0 - ay0) - (cx0 - ax0) * (gy - ay0)) / det
        w2 = ((bx0 - ax0) * (gy - ay0) - (gx - ax0) * (by0 - ay0)) / det
        w0 = 1.0 - w1 - w2
        inside = (w0 >= 0) & (w1 >= 0) & (w2 >= 0)
        if not inside.any():
            continue
        z = w0 * depth[ia] + w1 * depth[ib] + w2 * depth[ic]
        sub = zbuf[iy0:iy1, ix0:ix1]
        win = inside & (z > sub)
        if not win.any():
            continue
        sub[win] = z[win]
        img[iy0:iy1, ix0:ix1][win] = tcol[t]

    out = Image.fromarray((np.clip(img, 0, 1) * 255).astype(np.uint8))
    d = ImageDraw.Draw(out)
    if colour_by == 'island':
        for e in bx[:34]:
            cx = (e['ctr'][ax] - ctr[ax]) * sc + W / 2
            cy = H / 2 - (e['ctr'][ay] - ctr[ay]) * sc
            n = str(rank[e['id']])
            d.rectangle([cx - 8, cy - 7, cx + 8 + 6 * (len(n) - 1), cy + 8], fill=(0, 0, 0))
            d.text((cx - 5, cy - 6), n, fill=(255, 255, 255))
    d.text((8, 8), '%s  (%s)  1 unit = 1 inch' % (view, colour_by), fill=(255, 255, 255))
    name = 'view_%s_%s.png' % (view, colour_by)
    out.save(name)
    print('  %s' % name)


for v in VIEWS:
    for cb in ('island', 'material'):
        render(v, cb)

print()
print('%-4s %-8s %8s %8s %8s | %8s %8s %8s | %6s'
      % ('#', 'mat', 'X(in)', 'Y(in)', 'Z(in)', 'ctrX', 'ctrY', 'ctrZ', 'tris'))
for i, e in enumerate(bx[:34]):
    print('%-4d %-8d %8.3f %8.3f %8.3f | %8.3f %8.3f %8.3f | %6d'
          % (i, e['mat'], e['size'][0], e['size'][1], e['size'][2],
             e['ctr'][0], e['ctr'][1], e['ctr'][2], e['tris']))
