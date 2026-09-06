# -*- coding: utf-8 -*-
"""Split vertices at creases, so a hard edge is actually hard.

The file carries no duplicate vertices - 30,441 in, 30,441 welded - which means its hard edges
were never expressed as split geometry. They lived in Blender's custom split-normal layer, and
a naive recompute throws them away: every corner of a crease shares one vertex, one vertex can
carry one normal, and averaging across the crease is what produced the diagonal smear under
the drive slot.

The fix is smoothing groups, not a lower angle threshold. For each vertex the incident faces
are clustered by direction; each cluster becomes its own output vertex with its own averaged
normal. A face that sits alone in its cluster keeps its own normal and the edge stays sharp; a
face on a rounded corner still averages with its neighbours and the corner stays round. A
threshold alone cannot do both, which is why lowering it only trades one artefact for another.

Clusters are seeded largest-area-first so a big flat panel defines the cluster and a sliver
joins it, rather than a sliver seeding a cluster the panel then fails to match.
"""
import numpy as np


def split_normals(co, tris, crease_deg=38.0):
    """returns (positions, normals, new_tris) with vertices duplicated at creases"""
    fn = np.cross(co[tris[:, 1]] - co[tris[:, 0]], co[tris[:, 2]] - co[tris[:, 0]])
    area = np.linalg.norm(fn, axis=1)
    fnu = fn / np.maximum(area[:, None], 1e-20)
    cosT = float(np.cos(np.radians(crease_deg)))
    nv, nt = len(co), len(tris)

    corner_v = tris.ravel()
    corner_f = np.repeat(np.arange(nt), 3)
    order = np.argsort(corner_v, kind='stable')
    cv, cf = corner_v[order], corner_f[order]
    lo = np.searchsorted(cv, np.arange(nv), side='left')
    hi = np.searchsorted(cv, np.arange(nv), side='right')

    out_pos, out_nrm = [], []
    face_slot = np.full((nt, 3), -1, np.int64)      # corner -> output vertex
    # which corner (0,1,2) each entry of cf is, so the mapping can be written back
    corner_k = np.tile(np.arange(3), nt)[order]

    for v in range(nv):
        a, b = lo[v], hi[v]
        if a == b:
            continue
        faces = cf[a:b]
        ks = corner_k[a:b]
        idx = np.argsort(-area[faces])              # largest first
        sums = []                                   # running area-weighted vector per cluster
        assign = np.empty(len(faces), np.int64)
        for j in idx:
            f = faces[j]
            n = fnu[f]
            best = -1
            for ci in range(len(sums)):
                s = sums[ci]
                L = np.sqrt(s @ s)
                if L > 1e-20 and (s @ n) / L >= cosT:
                    best = ci
                    break
            if best < 0:
                sums.append(area[f] * n.copy())
                best = len(sums) - 1
            else:
                sums[best] += area[f] * n
            assign[j] = best
        base = len(out_pos)
        for s in sums:
            L = np.sqrt(s @ s)
            out_pos.append(co[v])
            out_nrm.append(s / L if L > 1e-20 else np.array([0.0, 1.0, 0.0]))
        for j in range(len(faces)):
            face_slot[faces[j], ks[j]] = base + assign[j]

    P = np.asarray(out_pos, np.float64)
    N = np.asarray(out_nrm, np.float64)
    return P, N, face_slot


if __name__ == '__main__':
    import sys
    from meshlib import load
    co, tris, tmat, b = load(sys.argv[1] if len(sys.argv) > 1
                             else r'C:\Users\Alex\Downloads\Mac.blend')
    for deg in (25.0, 38.0, 50.0):
        P, N, T = split_normals(co, tris, deg)
        print('crease %4.0f deg : %6d verts -> %6d  (x%.2f)  faces %d'
              % (deg, len(co), len(P), len(P) / len(co), len(T)))
