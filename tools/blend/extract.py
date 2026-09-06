# -*- coding: utf-8 -*-
"""Pull the machine out of the .blend as something a browser can actually draw.

A browser has no .blend loader - the format is Blender's memory image, not an interchange
format - so "embed the file" means converting it. Since both ends of this pipeline are mine,
the target is a small binary blob rather than glTF: glTF would carry a JSON document, a buffer
layout and an accessor table that exist to let unknown readers cope, and there is no unknown
reader here.

Three things this has to get right, and they are the three that were flagged as risks:

  SIZE      positions as 16-bit fixed point over each group's own bounding box, normals as
            octahedral 16-bit. Eight bytes a vertex instead of twenty-four.
  NORMALS   the file's MVert.no is Blender's legacy normal and does not carry split normals,
            so shading straight off it loses every hard edge. Recomputed here with an angle
            threshold, which is what gives a moulded case its crease.
  STAGING   the artist's scene has a desk mat and puts the mouse ten inches out on it. That is
            set dressing, not the product, and it goes.
"""
import json
import struct
import sys

import numpy as np

from meshlib import boxes, islands, load

PATH = sys.argv[1] if len(sys.argv) > 1 else r'C:\Users\Alex\Downloads\Mac.blend'
SMOOTH_DEG = 38.0

co, tris, tmat, blend = load(PATH)
lab, nisl = islands(co, tris)
bx = boxes(co, tris, tmat, lab, nisl)
by_id = {e['id']: e for e in bx}
bx.sort(key=lambda e: -float(np.prod(e['size'] + 1e-6)))
CASE = bx[0]
print('%d tris, %d islands' % (len(tris), nisl))

# ---------------------------------------------------------------- who is what
# The case, the keyboard and the mouse are told apart by where they sit, not by index: island
# numbering is an artefact of the traversal order and would change if the file ever did.
CASE_X = (CASE['lo'][0] - 0.4, CASE['hi'][0] + 0.4)
CASE_Y = (CASE['lo'][1] - 0.4, CASE['hi'][1] + 0.4)


def group_of(e):
    cx, cy, cz = e['ctr']
    sx, sy, sz = e['size']
    if e['id'] == CASE['id']:
        return 'machine'
    # the desk mat: big, flat, lying on the ground away to the right
    if sz < 1.3 and sx > 8 and sy > 8:
        return None
    if CASE_X[0] <= cx <= CASE_X[1] and CASE_Y[0] <= cy <= CASE_Y[1]:
        return 'machine'
    if cy < CASE['lo'][1] and cx < 6.0:
        return 'keyboard'
    if cx > 6.0:
        return 'mouse'
    return 'machine'


groups = {}
for e in bx:
    g = group_of(e)
    if g:
        groups.setdefault(g, []).append(e)
for g in ('machine', 'keyboard', 'mouse'):
    es = groups.get(g, [])
    t = sum(e['tris'] for e in es)
    lo = np.min([e['lo'] for e in es], 0)
    hi = np.max([e['hi'] for e in es], 0)
    print('%-9s %3d islands  %6d tris   %.2f x %.2f x %.2f in  at %s'
          % (g, len(es), t, *(hi - lo), np.round((hi + lo) / 2, 2)))
dropped = [e for e in bx if group_of(e) is None]
print('dropped   %3d islands  %6d tris  (%s)'
      % (len(dropped), sum(e['tris'] for e in dropped),
         ', '.join('%.1fx%.1f' % (e['size'][0], e['size'][1]) for e in dropped[:4])))

print()
print('the five biggest islands kept, so nothing large goes in unidentified:')
for e in bx[:8]:
    g = group_of(e)
    print('   %-8s %6d tris  %6.2f x %6.2f x %6.2f  at %7.2f %7.2f %7.2f  mat %d'
          % (g or 'DROP', e['tris'], *e['size'], *e['ctr'], e['mat']))

# ---------------------------------------------------------------- normals
print()
print('recomputing normals with a %.0f degree crease threshold' % SMOOTH_DEG)
fn = np.cross(co[tris[:, 1]] - co[tris[:, 0]], co[tris[:, 2]] - co[tris[:, 0]])
fa = np.linalg.norm(fn, axis=1, keepdims=True)
fnu = fn / np.maximum(fa, 1e-20)

# weld on position first: the exporter split vertices at every seam, so averaging over the raw
# vertex buffer would average nothing and every face would come out flat.
G = 1e-4
key = np.round(co / G).astype(np.int64)
key -= key.min(0)
mul = key.max(0) + 1
flat = (key[:, 0] * mul[1] + key[:, 1]) * mul[2] + key[:, 2]
uq, inv = np.unique(flat, return_inverse=True)
print('  %d vertices -> %d welded positions' % (len(co), len(uq)))

# accumulate face normals per welded position, then decide per corner whether to use the
# average or the face's own normal
acc = np.zeros((len(uq), 3))
for k in range(3):
    np.add.at(acc, inv[tris[:, k]], fnu * fa)
accn = acc / np.maximum(np.linalg.norm(acc, axis=1, keepdims=True), 1e-20)
cosT = np.cos(np.radians(SMOOTH_DEG))

nrm = np.zeros_like(co)
cnt = np.zeros(len(co))
for k in range(3):
    vi = tris[:, k]
    a = accn[inv[vi]]
    smooth = (a * fnu).sum(1) >= cosT
    use = np.where(smooth[:, None], a, fnu)
    np.add.at(nrm, vi, use)
    np.add.at(cnt, vi, 1)
nrm /= np.maximum(np.linalg.norm(nrm, axis=1, keepdims=True), 1e-20)
hard = int((cnt > 0).sum())
print('  %d of %d vertices carry a normal' % (hard, len(co)))

np.save('ex_normals.npy', nrm)
np.save('ex_groups.npy', np.array([group_of(by_id[i]) or '' for i in range(nisl)], dtype=object),
        allow_pickle=True)
print('saved ex_normals.npy, ex_groups.npy')
