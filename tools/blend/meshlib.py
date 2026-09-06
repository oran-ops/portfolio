# -*- coding: utf-8 -*-
"""Mesh out of a .blend, split into the pieces the modeller actually built.

Kept apart from the measuring and the drawing so that both run over the same arrays. A number
computed one way and a picture drawn another way is not a check of anything.
"""
import struct

import numpy as np

from blendread import Blend


def load(path):
    b = Blend(path)
    E = b.E
    msd, moff = next(b.of_type('Mesh'))
    nv = b.field(msd, moff, 'totvert')
    npo = b.field(msd, moff, 'totpoly')
    nl = b.field(msd, moff, 'totloop')
    vb = b.follow(b.field(msd, moff, 'mvert'))
    pb = b.follow(b.field(msd, moff, 'mpoly'))
    lb = b.follow(b.field(msd, moff, 'mloop'))
    vs, ps, ls = b.sizeof(vb.sdna), b.sizeof(pb.sdna), b.sizeof(lb.sdna)

    raw = np.frombuffer(b.d, dtype=np.uint8)
    co = np.zeros((nv, 3), np.float64)
    v = np.frombuffer(b.d, dtype=np.dtype([('co', '<3f4'), ('rest', 'V8')]),
                      count=nv, offset=vb.off)
    co[:] = v['co']

    lp = np.frombuffer(b.d, dtype=np.dtype([('v', '<u4'), ('e', '<u4')]), count=nl, offset=lb.off)
    lv = lp['v'].astype(np.int64)

    pl = np.frombuffer(b.d, dtype=np.dtype([('start', '<i4'), ('tot', '<i4'),
                                            ('mat', '<i2'), ('pad', 'V2')]),
                       count=npo, offset=pb.off)
    start = pl['start'].astype(np.int64)
    tot = pl['tot'].astype(np.int64)
    mat = pl['mat'].astype(np.int32)

    # every polygon in this file is already a triangle; fan-triangulate anyway so the loader
    # does not quietly depend on that
    tris = []
    tmat = []
    if np.all(tot == 3):
        tris = np.stack([lv[start], lv[start + 1], lv[start + 2]], 1)
        tmat = mat.copy()
    else:
        for i in range(npo):
            s, t = start[i], tot[i]
            for k in range(1, t - 1):
                tris.append((lv[s], lv[s + k], lv[s + k + 1]))
                tmat.append(mat[i])
        tris = np.array(tris, np.int64)
        tmat = np.array(tmat, np.int32)
    return co, tris, tmat, b


def islands(co, tris, grid=1e-4):
    """label each vertex with its connected piece, welding coincident positions first.

    The exporter split vertices at hard edges and UV seams; without the weld every smooth patch
    reads as its own object and the report becomes noise.
    """
    n = len(co)
    key = np.round(co / grid).astype(np.int64)
    key = key - key.min(0)
    mul = key.max(0) + 1
    flat = (key[:, 0] * mul[1] + key[:, 1]) * mul[2] + key[:, 2]
    order = np.argsort(flat, kind='stable')
    rep = np.empty(n, np.int64)
    s = flat[order]
    first = np.r_[True, s[1:] != s[:-1]]
    grp = np.cumsum(first) - 1
    leader = order[first][grp]
    rep[order] = leader

    par = np.arange(n, dtype=np.int64)

    def find(a):
        while par[a] != a:
            par[a] = par[par[a]]
            a = par[a]
        return a

    def uni(a, b):
        ra, rb = find(a), find(b)
        if ra != rb:
            par[rb] = ra

    for i in range(n):
        if rep[i] != i:
            uni(int(rep[i]), i)
    for a, bb, c in tris:
        uni(int(a), int(bb))
        uni(int(a), int(c))
    lab = np.array([find(i) for i in range(n)], np.int64)
    uq, lab = np.unique(lab, return_inverse=True)
    return lab, len(uq)


def boxes(co, tris, tmat, lab, nisl):
    """per-island bounding box, triangle count and dominant material"""
    tl = lab[tris[:, 0]]
    out = []
    for i in range(nisl):
        m = tl == i
        t = tris[m]
        if len(t) == 0:
            continue
        p = co[np.unique(t)]
        mats = np.bincount(tmat[m])
        out.append(dict(id=i, lo=p.min(0), hi=p.max(0), size=p.max(0) - p.min(0),
                        ctr=(p.max(0) + p.min(0)) / 2, tris=int(m.sum()),
                        mat=int(mats.argmax()), nvert=len(p)))
    return out


def raster(co, tris, tsel, au, av, ad, sgn, px=0.01, pad=0.05):
    """Fill triangles into the (au, av) plane, keeping the extreme along ad.

    Sampling vertices in a thin slab is the wrong instrument for this mesh: the flat panels are
    a handful of large triangles, so a slab between two corner rows finds nothing and reports a
    face that is not there. Rasterising asks the surface, not the vertex buffer.
    """
    import numpy as np
    t = tris[tsel]
    p = co[np.unique(t)]
    lo = np.array([p[:, au].min(), p[:, av].min()]) - pad
    hi = np.array([p[:, au].max(), p[:, av].max()]) + pad
    W = int((hi[0] - lo[0]) / px) + 1
    H = int((hi[1] - lo[1]) / px) + 1
    img = np.full((H, W), np.nan)
    U = (co[:, au] - lo[0]) / px
    V = (co[:, av] - lo[1]) / px
    D = co[:, ad] * sgn
    for tri in t:
        ia, ib, ic = tri
        ux, uy, uz = U[ia], U[ib], U[ic]
        vx, vy, vz = V[ia], V[ib], V[ic]
        x0 = max(int(min(ux, uy, uz)), 0); x1 = min(int(max(ux, uy, uz)) + 2, W)
        y0 = max(int(min(vx, vy, vz)), 0); y1 = min(int(max(vx, vy, vz)) + 2, H)
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
    return img, lo, px
