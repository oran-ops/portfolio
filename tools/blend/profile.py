# -*- coding: utf-8 -*-
"""The numbers, in inches, that the generator needs.

Slicing at x=0 was the wrong instrument: the plane runs straight through the drive bay and the
shell's inner wall, so it returns the machine's guts along with its outline. What I actually
want is the outline, which is a silhouette question.

Two instruments here, both rasterised at 0.01 in per pixel so that a pixel is never the thing
that limits the answer:

  * SILHOUETTE - fill the case triangles into a mask, then read the boundary per row and per
    column. The side outline is single-valued in that form (one front edge and one back edge at
    every height), so no contour chasing and nothing to mis-chain.

  * DEPTH MAP - fill the case again from the front, keeping the nearest surface at each pixel,
    in inches. The front face and the screen recess then differ by their actual depth, so the
    well's outline and its depth fall out of one image instead of being guessed from a photo.
"""
import sys

import numpy as np

from meshlib import boxes, islands, load

PATH = sys.argv[1] if len(sys.argv) > 1 else r'C:\Users\Alex\Downloads\Mac.blend'
PX = 0.01                                   # inches per pixel

co, tris, tmat, blend = load(PATH)
lab, nisl = islands(co, tris)
bx = boxes(co, tris, tmat, lab, nisl)
bx.sort(key=lambda e: -float(np.prod(e['size'] + 1e-6)))
CASE = bx[0]
keep = lab[tris[:, 0]] == CASE['id']
print('case island: %.3f x %.3f x %.3f in   at %s'
      % tuple(list(CASE['size']) + [np.round(CASE['ctr'], 3)]))
print('           x %.3f..%.3f   y %.3f..%.3f   z %.3f..%.3f'
      % (CASE['lo'][0], CASE['hi'][0], CASE['lo'][1], CASE['hi'][1],
         CASE['lo'][2], CASE['hi'][2]))


def raster(tsel, au, av, ad, sgn, lo=None, hi=None, pad=0.05):
    """fill triangles into (u,v); keep the extreme along ad. returns depth image + origin"""
    t = tris[tsel]
    p = co[np.unique(t)]
    if lo is None:
        lo = np.array([p[:, au].min(), p[:, av].min()]) - pad
        hi = np.array([p[:, au].max(), p[:, av].max()]) + pad
    W = int((hi[0] - lo[0]) / PX) + 1
    H = int((hi[1] - lo[1]) / PX) + 1
    img = np.full((H, W), np.nan)
    U = (co[:, au] - lo[0]) / PX
    V = (co[:, av] - lo[1]) / PX
    D = co[:, ad] * sgn
    a, b, c = t[:, 0], t[:, 1], t[:, 2]
    for i in range(len(t)):
        ia, ib, ic = a[i], b[i], c[i]
        ux, uy, uz = U[ia], U[ib], U[ic]
        vx, vy, vz = V[ia], V[ib], V[ic]
        x0 = max(int(min(ux, uy, uz)), 0)
        x1 = min(int(max(ux, uy, uz)) + 2, W)
        y0 = max(int(min(vx, vy, vz)), 0)
        y1 = min(int(max(vx, vy, vz)) + 2, H)
        if x1 <= x0 or y1 <= y0:
            continue
        det = (uy - ux) * (vz - vx) - (uz - ux) * (vy - vx)
        if abs(det) < 1e-9:
            continue
        gx, gy = np.meshgrid(np.arange(x0, x1) + 0.5, np.arange(y0, y1) + 0.5)
        w1 = ((gx - ux) * (vz - vx) - (uz - ux) * (gy - vx)) / det
        w2 = ((uy - ux) * (gy - vx) - (gx - ux) * (vy - vx)) / det
        w0 = 1 - w1 - w2
        ins = (w0 >= -1e-9) & (w1 >= -1e-9) & (w2 >= -1e-9)
        if not ins.any():
            continue
        z = w0 * D[ia] + w1 * D[ib] + w2 * D[ic]
        sub = img[y0:y1, x0:x1]
        win = ins & (np.isnan(sub) | (z > np.nan_to_num(sub, nan=-1e30)))
        sub[win] = z[win]
    return img, lo, hi


def edges(mask, lo, axis):
    """first and last filled index along `axis`, in inches"""
    any_ = mask.any(axis=axis)
    idx = np.arange(mask.shape[1 - axis])
    first = np.where(any_, mask.argmax(axis=axis), -1)
    last = np.where(any_, mask.shape[axis] - 1 - mask[::-1].argmax(axis=axis)
                    if axis == 0 else mask.shape[axis] - 1 - mask[:, ::-1].argmax(axis=axis), -1)
    return any_, first, last, idx


# ---------------------------------------------------------------- side outline
print()
print('=' * 78)
print('SIDE OUTLINE  (looking along -X; Y is depth, -Y is the front; Z is height)')
print('=' * 78)
simg, slo, shi = raster(keep, 1, 2, 0, 1.0)
smask = ~np.isnan(simg)
H, W = smask.shape
rows = np.where(smask.any(1))[0]
print('%8s | %9s %9s | %8s' % ('Z (in)', 'front Y', 'rear Y', 'depth'))
print('-' * 46)
for z_in in np.arange(0.3, 13.6, 0.5):
    r = int((z_in - slo[1]) / PX)
    if r < 0 or r >= H or not smask[r].any():
        continue
    cols = np.where(smask[r])[0]
    y0 = slo[0] + cols[0] * PX
    y1 = slo[0] + cols[-1] * PX
    print('%8.2f | %9.3f %9.3f | %8.3f' % (z_in, y0, y1, y1 - y0))

print()
print('roof line (max Z at each depth Y):')
print('%8s | %8s' % ('Y (in)', 'top Z'))
print('-' * 20)
for y_in in np.arange(-6.0, 4.9, 0.5):
    c = int((y_in - slo[0]) / PX)
    if c < 0 or c >= W or not smask[:, c].any():
        continue
    r = np.where(smask[:, c])[0]
    print('%8.2f | %8.3f' % (y_in, slo[1] + r[-1] * PX))

# ---------------------------------------------------------------- front outline
print()
print('=' * 78)
print('FRONT OUTLINE  (width at each height)')
print('=' * 78)
fimg, flo, fhi = raster(keep, 0, 2, 1, -1.0)
fmask = ~np.isnan(fimg)
Hf, Wf = fmask.shape
print('%8s | %9s %9s | %8s' % ('Z (in)', 'left X', 'right X', 'width'))
print('-' * 46)
for z_in in np.arange(0.3, 13.6, 0.5):
    r = int((z_in - flo[1]) / PX)
    if r < 0 or r >= Hf or not fmask[r].any():
        continue
    cols = np.where(fmask[r])[0]
    x0 = flo[0] + cols[0] * PX
    x1 = flo[0] + cols[-1] * PX
    print('%8.2f | %9.3f %9.3f | %8.3f' % (z_in, x0, x1, x1 - x0))

# ---------------------------------------------------------------- the recess
print()
print('=' * 78)
print('FRONT DEPTH MAP  (how far back each point of the face sits)')
print('=' * 78)
depth = -fimg                                   # back to real Y, nearest surface
val = depth[~np.isnan(depth)]
hist, ed = np.histogram(val, bins=120)
face_y = ed[hist.argmax()]
print('nearest-surface Y histogram peak (the face plane): y = %.3f in' % face_y)
top = np.argsort(-hist)[:6]
print('six busiest depths:')
for i in sorted(top):
    print('   y %7.3f .. %7.3f   %6d px  (%.1f%% of the face)'
          % (ed[i], ed[i + 1], hist[i], 100.0 * hist[i] / len(val)))

recess = (depth > face_y + 0.04) & (depth < face_y + 1.2)
if recess.any():
    rr, cc = np.where(recess)
    x0 = flo[0] + cc.min() * PX
    x1 = flo[0] + cc.max() * PX
    z0 = flo[1] + rr.min() * PX
    z1 = flo[1] + rr.max() * PX
    d = depth[recess]
    print()
    print('recessed region: x %.3f..%.3f (%.3f wide)   z %.3f..%.3f (%.3f tall)'
          % (x0, x1, x1 - x0, z0, z1, z1 - z0))
    print('   centre  x %+.3f   z %+.3f     (case centre x %+.3f)'
          % ((x0 + x1) / 2, (z0 + z1) / 2, CASE['ctr'][0]))
    print('   depth below the face: median %.3f in, 90th pct %.3f in'
          % (np.median(d) - face_y, np.percentile(d, 90) - face_y))

np.save('front_depth.npy', depth)
np.save('front_origin.npy', np.array([flo[0], flo[1], PX]))

# ---------------------------------------------------------------- the fittings
print()
print('=' * 78)
print('FITTINGS  (every island over 0.4 in in its largest dimension)')
print('=' * 78)
print('%-4s %-5s %8s %8s %8s | %8s %8s %8s | %6s'
      % ('#', 'mat', 'X', 'Y', 'Z', 'ctrX', 'ctrY', 'ctrZ', 'tris'))
for i, e in enumerate(bx[:30]):
    print('%-4d %-5d %8.3f %8.3f %8.3f | %8.3f %8.3f %8.3f | %6d'
          % (i, e['mat'], e['size'][0], e['size'][1], e['size'][2],
             e['ctr'][0], e['ctr'][1], e['ctr'][2], e['tris']))
