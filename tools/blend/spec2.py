# -*- coding: utf-8 -*-
"""The parameter table, this time with the geometry fits taken off rasterised silhouettes.

The first pass sampled vertices inside thin slabs and produced a 22.7 deg rake with a 9.8 in
residual - a fit so bad it announced its own failure. The cause: the flat panels of this mesh
are a few large triangles, so a slab drawn between two rows of corners contains no vertices at
all and the "front edge" it reports is whatever happened to be nearby. Rasterising asks the
surface instead of the vertex buffer, and every residual below is now in thousandths of an inch.
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
CX, CY, CZ = CASE['ctr']
keep = lab[tris[:, 0]] == CASE['id']


def fit(x, y):
    A = np.vstack([x, np.ones_like(x)]).T
    m, c = np.linalg.lstsq(A, y, rcond=None)[0]
    return m, c, float(np.abs(y - (m * x + c)).max())


# ---- side silhouette: Y (depth) across, Z (height) up ----------------------
simg, slo, PX = raster(co, tris, keep, 1, 2, 0, 1.0)
smask = ~np.isnan(simg)


def row_edges(mask, lo, z):
    r = int((z - lo[1]) / PX)
    if r < 0 or r >= mask.shape[0] or not mask[r].any():
        return None
    c = np.where(mask[r])[0]
    return lo[0] + c[0] * PX, lo[0] + c[-1] * PX


def col_top(mask, lo, u):
    c = int((u - lo[0]) / PX)
    if c < 0 or c >= mask.shape[1] or not mask[:, c].any():
        return None
    return lo[1] + np.where(mask[:, c])[0][-1] * PX


print('=' * 86)
print('MACINTOSH - measured (inches, +X right, -Y front, +Z up).  case centre x%+.3f y%+.3f z%+.3f'
      % (CX, CY, CZ))
print('=' * 86)
print('case bbox        %.3f W x %.3f D x %.3f H     x %+.3f..%+.3f  y %+.3f..%+.3f  z %+.3f..%+.3f'
      % (*CASE['size'], CASE['lo'][0], CASE['hi'][0], CASE['lo'][1],
         CASE['hi'][1], CASE['lo'][2], CASE['hi'][2]))

zs = np.arange(3.6, 12.7, 0.1)
fr = np.array([[z, row_edges(smask, slo, z)[0]] for z in zs])
m, c, e = fit(fr[:, 0], fr[:, 1])
print()
print('FRONT FACE RAKE   dY/dZ %+.5f  =  %.2f deg from vertical   max resid %.4f in'
      % (m, np.degrees(np.arctan(m)), e))
print('                  y = %+.4f %+.5f*z      z=3.3 -> y%+.3f    z=12.8 -> y%+.3f'
      % (c, m, m * 3.3 + c, m * 12.8 + c))

ys = np.arange(-4.2, 3.7, 0.1)
rf = np.array([[y, col_top(smask, slo, y)] for y in ys])
m2, c2, e2 = fit(rf[:, 0], rf[:, 1])
print('ROOF SLOPE        dZ/dY %+.5f  =  %.2f deg falling to the rear   max resid %.4f in'
      % (m2, np.degrees(np.arctan(-m2)), e2))
print('                  z = %+.4f %+.5f*y      y=-4.2 -> z%.3f     y=+3.5 -> z%.3f'
      % (c2, m2, m2 * -4.2 + c2, m2 * 3.5 + c2))

print()
print('CHIN AND BROW     (front edge y at each height, 0.1 in steps)')
prev = None
for z in np.arange(0.3, 4.1, 0.1):
    r = row_edges(smask, slo, z)
    if r is None:
        continue
    mark = ''
    if prev is not None and abs(r[0] - prev) > 0.05:
        mark = '   <-- step %+.3f' % (r[0] - prev)
    print('   z=%4.1f  front y %+7.3f   rear y %+7.3f   depth %6.3f%s'
          % (z, r[0], r[1], r[1] - r[0], mark))
    prev = r[0]

print()
print('REAR              rear y is flat at %+.3f up to z=10.8, then:' % row_edges(smask, slo, 5.0)[1])
for z in np.arange(10.8, 13.6, 0.2):
    r = row_edges(smask, slo, z)
    if r:
        print('   z=%5.2f  rear y %+7.3f' % (z, r[1]))

# ---- front silhouette ------------------------------------------------------
fimg, flo, _ = raster(co, tris, keep, 0, 2, 1, -1.0)
fmask = ~np.isnan(fimg)
w = [row_edges(fmask, flo, z) for z in np.arange(1.0, 13.3, 0.1)]
w = [q for q in w if q]
print()
print('FRONT WIDTH       constant %.3f  (min %.3f, max %.3f over z=1.0..13.3)'
      % (np.median([q[1] - q[0] for q in w]), min(q[1] - q[0] for q in w),
         max(q[1] - q[0] for q in w)))
print('                  x %+.3f .. %+.3f' % (np.median([q[0] for q in w]),
                                              np.median([q[1] for q in w])))

# corner radius from the mask boundary, fitted as a circle
rr, cc = np.where(fmask)
X = flo[0] + cc * PX
Z = flo[1] + rr * PX
sel = (X > 3.6) & (Z > 12.4)
if sel.sum() > 50:
    P = np.c_[X[sel], Z[sel]]
    # boundary points only: for each column the highest filled row
    bnd = []
    for x0 in np.unique(np.round(P[:, 0], 2)):
        q = P[np.abs(P[:, 0] - x0) < 0.006]
        if len(q):
            bnd.append([x0, q[:, 1].max()])
    bnd = np.array(bnd)
    A = np.c_[2 * bnd, np.ones(len(bnd))]
    s = np.linalg.lstsq(A, (bnd ** 2).sum(1), rcond=None)[0]
    R = np.sqrt(s[2] + s[0] ** 2 + s[1] ** 2)
    res = np.abs(np.hypot(bnd[:, 0] - s[0], bnd[:, 1] - s[1]) - R).max()
    print('CORNER RADIUS     %.3f in  (top-right of the front outline, %d pts, max resid %.4f)'
          % (R, len(bnd), res))

# ---- the screen well -------------------------------------------------------
depth = -fimg
face = m * (flo[1] + np.arange(depth.shape[0]) * PX) + c      # the raked plane, per row
recess = (~np.isnan(depth)) & (depth > face[:, None] + 0.06)
hole = np.isnan(depth)
well = recess | hole
lab_rows = np.where(well.any(1))[0]
big = well.copy()
big[:int((3.0 - flo[1]) / PX)] = False          # ignore the chin fittings
rr2, cc2 = np.where(big)
if len(rr2):
    # the well is the large connected block in the upper half; bound it by density
    zz = flo[1] + rr2 * PX
    xx = flo[0] + cc2 * PX
    up = zz > 6.0
    print()
    print('SCREEN WELL       x %+.3f..%+.3f (%.3f wide)   z %.3f..%.3f (%.3f tall)'
          % (xx[up].min(), xx[up].max(), xx[up].max() - xx[up].min(),
             zz[up].min(), zz[up].max(), zz[up].max() - zz[up].min()))
    print('                  centre x %+.3f (case %+.3f)   z %+.3f'
          % ((xx[up].min() + xx[up].max()) / 2, CX, (zz[up].min() + zz[up].max()) / 2))
    d = depth[big][~np.isnan(depth[big])]
    fl = face[rr2][~np.isnan(depth[big])] if len(d) == len(rr2) else None
    inner = recess & (np.arange(depth.shape[0])[:, None] * PX + flo[1] > 6.0)
    if inner.any():
        dd = depth[inner] - face[np.where(inner)[0]]
        print('                  wall depth below the face: median %.3f  p90 %.3f  max %.3f in'
              % (np.median(dd), np.percentile(dd, 90), dd.max()))

# ---- keyboard, from its own silhouette -------------------------------------
kb = [e for e in bx if e['size'][0] > 13 and e['ctr'][1] < -9][0]
kkeep = lab[tris[:, 0]] == kb['id']
kimg, klo, _ = raster(co, tris, kkeep, 1, 2, 0, 1.0)
kmask = ~np.isnan(kimg)
ys = np.arange(kb['lo'][1] + 0.3, kb['hi'][1] - 0.3, 0.05)
tops = np.array([[y, col_top(kmask, klo, y)] for y in ys if col_top(kmask, klo, y) is not None])
m3, c3, e3 = fit(tops[:, 0], tops[:, 1])
print()
print('=' * 86)
print('KEYBOARD  %.3f W x %.3f D x %.3f H   centre %+.3f %+.3f %+.3f'
      % (*kb['size'], *kb['ctr']))
print('=' * 86)
print('case top slope    dZ/dY %+.5f  =  %.2f deg rising to the rear   max resid %.4f in'
      % (m3, np.degrees(np.arctan(m3)), e3))
print('                  front y %+.3f (z %.3f)   rear y %+.3f (z %.3f)   height %.3f..%.3f'
      % (kb['lo'][1], m3 * kb['lo'][1] + c3, kb['hi'][1], m3 * kb['hi'][1] + c3,
         kb['lo'][2], kb['hi'][2]))
print('                  sits %.3f in in front of the case, %.3f in off the case centre in X'
      % (CASE['lo'][1] - kb['hi'][1], kb['ctr'][0] - CX))
