# -*- coding: utf-8 -*-
"""Lift the baked Macintosh out of lab/machine.html and into src/machine/machine.js.

    python tools/bake_machine.py                 report what is in the blob
    python tools/bake_machine.py --write         write the selected groups into machine.js

WHY THIS EXISTS. Oran modelled the machine himself -- macintosh.blend -- and the whole point
of the object is that it is HIS. The first build shipped the procedural one instead, on a
weight argument, and he was right to call that a substitution rather than a decision:

    "you used the wrong computer, this isn't the computer I brought, it's what you created"

So the mesh ships. What does not ship is everything on the desk beside it, and the reason is
measurement rather than taste. The blob breaks down like this:

    machine     23,566 verts   25,258 tris   332 KB   <- the Macintosh. This is the object.
    keyboard    14,771 verts   13,516 tris   195 KB
    cable        6,931 verts   13,820 tris   135 KB   <- a CABLE, for 13,820 triangles
    mouse        2,470 verts    3,129 tris    38 KB

The cable costs more than the mouse and nearly as much as the keyboard, for a curve. And
extract_machine.py already recorded that the model's peripherals are its weakest part: its
keyboard is 7% too wide and its mouse 28% too wide against Apple's published dimensions,
which is why the procedural ones were built to the real figures in the first place.

So: HIS machine, and the measured keyboard and mouse. 332 KB instead of 700, the object in
question is the real one, and the two things beside it are the more accurate pair. The page
goes to roughly 690 KB gzipped rather than 951.

The blob's own format is unchanged and decodeMach is untouched -- this only drops groups and
rewrites the group count, so what arrives is byte-for-byte the same geometry Blender baked.
"""
import base64
import io
import os
import re
import struct
import sys

sys.stdout.reconfigure(encoding='utf-8', errors='replace')
HERE = os.path.dirname(os.path.abspath(__file__))
REPO = os.path.dirname(HERE)
LAB = os.path.join(REPO, 'lab', 'machine.html')
DEST = os.path.join(REPO, 'src', 'machine', 'machine.js')

# THE WHOLE SET. Oran: "you took only the computer and not the mouse and the keyboard? Why? What
# is the logic? Take the whole set please - fix this immediately."
#
# I had kept only the case and argued the peripherals from Apple's published dimensions. He has
# ruled, and the ruling is his to make: it is his model, and a desk assembled from two sources is
# not the object he built. All four groups ship.
#
# The price, stated plainly rather than buried: 933 KB of base64 instead of 443, which is about
# 505 KB over the wire instead of 240. The page goes to roughly 950 KB gzipped.
#
# What the arithmetic says about the fit, checked before shipping it: his keyboard lands at
# x -0.728..0.595, z 0.710..1.285 and the procedural one occupied x -0.728..0.595, z 0.707..1.289 --
# the same desk position to three decimals, so the transforms in MESH_XF are right. His mouse
# likewise. The cable intersects both the machine and the keyboard, which is what a cable does.
# All seven floppies clear both.
KEEP = ('machine', 'keyboard', 'cable', 'mouse')


def groups(raw):
    """Walk the blob and return (name, start, end, verts, tris) for every group."""
    assert raw[:4] == b'MACH', 'not a MACH blob'
    o = 4
    ver, = struct.unpack_from('<H', raw, o); o += 2
    assert ver == 2, 'blob version %d, expected 2' % ver
    ng, = struct.unpack_from('<H', raw, o); o += 2
    head = o
    out = []
    for _ in range(ng):
        start = o
        ln = raw[o]; o += 1
        name = raw[o:o + ln].decode('ascii'); o += ln
        nv, = struct.unpack_from('<I', raw, o); o += 4
        wide = raw[o]; o += 1
        o += 24                                   # bbox: two float3
        o += nv * 6                               # positions, quantised to u16
        o += nv * 2                               # normals, octahedral
        np_, = struct.unpack_from('<H', raw, o); o += 2
        tris = 0
        for _k in range(np_):
            o += 1                                # material
            ni, = struct.unpack_from('<I', raw, o); o += 4
            o += ni * (4 if wide else 2)
            tris += ni // 3
        out.append((name, start, o, nv, tris))
    return head, out


def main():
    write = '--write' in sys.argv
    lab = io.open(LAB, encoding='utf-8', errors='replace').read()
    m = re.search(r"decodeMach\('([A-Za-z0-9+/=]+)'", lab)
    if not m:
        print('  REFUSED: no baked blob found in %s' % LAB)
        return 1
    raw = base64.b64decode(m.group(1))
    head, gs = groups(raw)

    print('%-10s %8s %9s %10s' % ('group', 'verts', 'tris', 'bytes'))
    for name, a, b, nv, tris in gs:
        print('%-10s %8s %9s %9.1fK   %s'
              % (name, '{:,}'.format(nv), '{:,}'.format(tris), (b - a) / 1024.0,
                 'KEEP' if name in KEEP else 'built instead'))

    kept = [g for g in gs if g[0] in KEEP]
    missing = [k for k in KEEP if k not in [g[0] for g in gs]]
    if missing:
        print('\n  REFUSED: %s is not in the blob' % ', '.join(missing))
        return 1

    out = bytearray(raw[:head])
    struct.pack_into('<H', out, 6, len(kept))     # the group count, rewritten
    for _name, a, b, _nv, _t in kept:
        out += raw[a:b]
    blob = base64.b64encode(bytes(out)).decode('ascii')

    print('\n  %d of %d groups, %s verts, %s tris'
          % (len(kept), len(gs), '{:,}'.format(sum(g[3] for g in kept)),
             '{:,}'.format(sum(g[4] for g in kept))))
    print('  blob %.1f KB of base64 (was %.1f KB for all four)'
          % (len(blob) / 1024.0, len(m.group(1)) / 1024.0))

    # it must survive its own decoder before it is allowed near the page
    h2, g2 = groups(bytes(out))
    assert [g[0] for g in g2] == list(KEEP), 'the rewritten blob does not read back'
    assert [g[3] for g in g2] == [g[3] for g in kept], 'vertex counts moved'
    print('  re-reads correctly: %s' % ', '.join('%s %d verts' % (g[0], g[3]) for g in g2))

    if not write:
        print('\n  (report only; pass --write to put it in src/machine/machine.js)')
        return 0

    js = io.open(DEST, encoding='utf-8').read()
    n = len(re.findall(r"decodeMach\('[A-Za-z0-9+/=]*'", js))
    if n != 1:
        print('\n  REFUSED: %d decodeMach call sites in machine.js, expected 1' % n)
        return 1
    js = re.sub(r"decodeMach\('[A-Za-z0-9+/=]*'", "decodeMach('" + blob + "'", js)
    io.open(DEST, 'w', encoding='utf-8', newline='').write(js)
    print('\n  written into src/machine/machine.js')
    return 0


if __name__ == '__main__':
    sys.exit(main())
