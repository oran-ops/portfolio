# -*- coding: utf-8 -*-
"""Pack the machine, with vertices split at creases so hard edges stay hard.

Splitting costs vertices - 30,441 becomes 53,000-odd at a 45 degree crease - so the budget is
won back where it cannot be seen: octahedral normals drop from 16 bits per component to 8,
which is a worst-case angular error under a degree on a matte cream surface lit by three broad
sources. Positions stay at 16 bits, because a position error IS visible: it shows up as a seam
where two parts should meet.

  magic   'MACH'                        4 bytes
  version u16 = 2                       (v1 had 16-bit normals and no crease splitting)
  groups  u16
  per group:
    name        u8 length + ascii
    verts       u32, wide u8
    lo[3],hi[3] f32
    pos         u16[3] per vertex
    nrm         u8[2]  per vertex       octahedral
    parts       u16 count, then per part: u8 material, u32 index count, u16/u32 indices
"""
import base64
import gzip
import struct
import sys

import numpy as np

from meshlib import boxes, islands, load
from normals import split_normals

PATH = sys.argv[1] if len(sys.argv) > 1 else r'C:\Users\Alex\Downloads\Mac.blend'
# per group. A moulded case wants its edges kept; a coiled cable is a smooth tube and splitting
# it at 45 degrees only facets it - it doubled the cable's vertices to make it look worse.
CREASE = {'machine': 45.0, 'keyboard': 45.0, 'mouse': 45.0, 'cable': 80.0}
DROP_CABLE = '--nocable' in sys.argv

co, tris, tmat, blend = load(PATH)
lab, nisl = islands(co, tris)
bx = boxes(co, tris, tmat, lab, nisl)
order = sorted(bx, key=lambda e: -float(np.prod(e['size'] + 1e-6)))
CASE = order[0]


def classify(e):
    cx, cy, cz = e['ctr']
    sx, sy, sz = e['size']
    if e['id'] == CASE['id']:
        return 'machine', 0
    if sz < 1.3 and sx > 8 and sy > 8:
        return None, 0                                    # the desk mat
    if e['mat'] == 1 and sx > 5:
        return 'machine', 2                               # the tube face
    if e['tris'] > 6000 and sz < 2.0 and cz < 1.5:
        return (None if DROP_CABLE else 'cable'), 1       # the coiled keyboard cable
    if cy < CASE['lo'][1] - 0.2 and cx < 6.0:
        if sx < 4.0 and sz < 1.0 and cz > 1.2:
            return 'keyboard', 4                          # a keycap
        return 'keyboard', 0
    if cx > 6.0:
        return 'mouse', (4 if (sx < 2.0 and cz > 0.7) else 0)
    if cz > 12.0 and sy > 6.0:
        # the roof grilles are moulded IN the cream case, not fitted as a black part. Handing
        # them the dark moulding material turned them into two holes in the roof.
        return 'machine', 0
    if sx < 1.2 and sy < 1.2 and sz < 1.2:
        return 'machine', 1                               # small dark fittings
    return 'machine', 0


ASSIGN = {e['id']: classify(e) for e in bx}
tri_group = np.array([(ASSIGN[l][0] or '') for l in lab[tris[:, 0]]], dtype=object)
tri_mat = np.array([ASSIGN[l][1] for l in lab[tris[:, 0]]], dtype=np.uint8)

# split per group, each at its own angle. The groups are separate objects and share no
# vertices, so doing them apart changes nothing except which angle applies.
GP, GN, GT = {}, {}, {}
for g in ['machine', 'keyboard', 'cable', 'mouse']:
    sel = tri_group == g
    if not sel.any():
        continue
    used = np.unique(tris[sel])
    rm = np.full(len(co), -1, np.int64)
    rm[used] = np.arange(len(used))
    p, n, t = split_normals(co[used], rm[tris[sel]], CREASE[g])
    GP[g], GN[g], GT[g] = p, n, t
    print('  %-9s %6d -> %6d verts (x%.2f) at %.0f deg'
          % (g, len(used), len(p), len(p) / len(used), CREASE[g]))


def oct8(n):
    d = np.abs(n).sum(1, keepdims=True)
    p = n[:, :2] / np.maximum(d, 1e-20)
    neg = n[:, 2] < 0
    px = np.where(neg, (1.0 - np.abs(p[:, 1])) * np.where(p[:, 0] >= 0, 1.0, -1.0), p[:, 0])
    py = np.where(neg, (1.0 - np.abs(p[:, 0])) * np.where(p[:, 1] >= 0, 1.0, -1.0), p[:, 1])
    q = np.stack([px, py], 1)
    return np.clip(np.round((q * 0.5 + 0.5) * 255.0), 0, 255).astype('<u1')


def oct8_decode(b):
    q = b.astype(np.float64) / 255.0 * 2.0 - 1.0
    x, y = q[:, 0].copy(), q[:, 1].copy()
    z = 1.0 - np.abs(x) - np.abs(y)
    m = z < 0
    xs, ys = x.copy(), y.copy()
    x[m] = (1.0 - np.abs(ys[m])) * np.where(xs[m] >= 0, 1.0, -1.0)
    y[m] = (1.0 - np.abs(xs[m])) * np.where(ys[m] >= 0, 1.0, -1.0)
    v = np.stack([x, y, z], 1)
    return v / np.maximum(np.linalg.norm(v, axis=1, keepdims=True), 1e-20)


allN = np.vstack([GN[g] for g in GN])
e = np.degrees(np.arccos(np.clip((oct8_decode(oct8(allN)) * allN).sum(1), -1, 1)))
print('8:8 octahedral error: mean %.3f deg, 99th pct %.3f, max %.3f'
      % (e.mean(), np.percentile(e, 99), e.max()))

out = bytearray()
gorder = ['machine', 'keyboard', 'cable', 'mouse']
present = [g for g in gorder if (tri_group == g).any()]
out += b'MACH' + struct.pack('<HH', 2, len(present))
report = []
for g in present:
    sel = tri_group == g
    t = GT[g]
    m = tri_mat[sel]
    used = np.unique(t)
    remap = np.full(len(GP[g]), -1, np.int64)
    remap[used] = np.arange(len(used))
    pp, nn = GP[g][used], oct8(GN[g])[used]
    lo, hi = pp.min(0), pp.max(0)
    span = np.maximum(hi - lo, 1e-6)
    q = np.clip(np.round((pp - lo) / span * 65535.0), 0, 65535).astype('<u2')
    wide = len(used) >= 65536
    name = g.encode()
    out += struct.pack('<B', len(name)) + name
    out += struct.pack('<IB', len(used), 1 if wide else 0)
    out += struct.pack('<6f', *lo, *hi)
    out += q.tobytes() + nn.tobytes()
    mats = sorted(set(int(x) for x in m))
    out += struct.pack('<H', len(mats))
    for mm in mats:
        idx = remap[t[m == mm]].ravel()
        out += struct.pack('<BI', mm, len(idx))
        out += idx.astype('<u4' if wide else '<u2').tobytes()
    report.append((g, len(used), int(sel.sum()), mats))

raw = bytes(out)
b64 = base64.b64encode(raw).decode()
open('mach.bin', 'wb').write(raw)
open('mach.b64', 'w').write(b64)
print()
print('%-9s %8s %8s  %s' % ('group', 'verts', 'tris', 'materials'))
for g, nv, nt, mats in report:
    print('%-9s %8d %8d  %s' % (g, nv, nt, mats))
gz = len(gzip.compress(b64.encode(), 9))
print()
print('binary   %7d bytes (%3.0f KB)   base64 %7d (%3.0f KB)   gzipped %7d (%3.0f KB)'
      % (len(raw), len(raw) / 1024, len(b64), len(b64) / 1024, gz, gz / 1024))
