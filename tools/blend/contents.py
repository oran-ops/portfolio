# -*- coding: utf-8 -*-
"""What is actually in Mac.blend: the object, its mesh, its modifiers, its materials.

Before deciding whether a file solves anything, find out whether the geometry is real geometry
or a cage waiting for a subdivision modifier - the two look identical in a viewport screenshot
and are completely different things to ship.
"""
import struct
import sys

from blendread import Blend

PATH = sys.argv[1] if len(sys.argv) > 1 else r'C:\Users\Alex\Downloads\Mac.blend'
b = Blend(PATH)
E = b.E


def arr(addr, n, fmt, stride):
    """read n records of `fmt` from the block at old-address addr"""
    blk = b.follow(addr)
    if blk is None:
        return None
    out = []
    for i in range(n):
        out.append(struct.unpack_from(E + fmt, b.d, blk.off + i * stride))
    return out


print('=' * 78)
print('OBJECTS')
print('=' * 78)
for sdna, off in b.of_type('Object'):
    nm = b.name_of(sdna, off)
    typ = b.field(sdna, off, 'type')
    loc = b.field(sdna, off, 'loc')
    size = b.field(sdna, off, 'size')
    rot = b.field(sdna, off, 'rot')
    obmat = b.field(sdna, off, 'obmat')
    data = b.field(sdna, off, 'data')
    totcol = b.field(sdna, off, 'totcol')
    print('%-28s type=%d  totcol=%s' % (nm, typ, totcol))
    print('   loc  %s' % ['%.4f' % v for v in loc])
    print('   size %s' % ['%.4f' % v for v in size])
    print('   rot  %s' % ['%.4f' % v for v in rot])
    print('   obmat rows:')
    for r in range(4):
        print('     %s' % ['%9.5f' % obmat[r * 4 + c] for c in range(4)])
    # modifier stack
    ls, lo = b.sub(sdna, off, 'modifiers')
    first = struct.unpack_from(E + 'Q', b.d, lo)[0]
    node = first
    seen = 0
    while node and seen < 32:
        blk = b.follow(node)
        if blk is None:
            break
        msd = blk.sdna
        mname = b.field(msd, blk.off, 'name')
        mtype = b.field(msd, blk.off, 'type')
        tname = b.types[b.structs[msd][0]]
        extra = ''
        if 'levels' in b.layout(msd):
            extra = '  levels=%s render=%s' % (b.field(msd, blk.off, 'levels'),
                                               b.field(msd, blk.off, 'renderLevels'))
        print('   modifier: %-22s %-24s type=%s%s' % (mname, tname, mtype, extra))
        node = b.field(msd, blk.off, 'next')
        seen += 1
    if not first:
        print('   modifier: (none)')
    OBJ = (sdna, off, data)

print()
print('=' * 78)
print('MESH')
print('=' * 78)
for sdna, off in b.of_type('Mesh'):
    nm = b.name_of(sdna, off)
    tv = b.field(sdna, off, 'totvert')
    te = b.field(sdna, off, 'totedge')
    tp = b.field(sdna, off, 'totpoly')
    tl = b.field(sdna, off, 'totloop')
    print('%-28s verts=%-8d edges=%-8d polys=%-8d loops=%d' % (nm, tv, te, tp, tl))
    mvert = b.field(sdna, off, 'mvert')
    mpoly = b.field(sdna, off, 'mpoly')
    mloop = b.field(sdna, off, 'mloop')
    print('   mvert=%s mpoly=%s mloop=%s' % (hex(mvert), hex(mpoly), hex(mloop)))
    vb = b.follow(mvert)
    if vb:
        vs = b.sizeof(vb.sdna)
        print('   MVert struct = %s (%d bytes), block count=%d'
              % (b.types[b.structs[vb.sdna][0]], vs, vb.count))
        lo = [1e30] * 3
        hi = [-1e30] * 3
        for i in range(vb.count):
            x, y, z = struct.unpack_from(E + '3f', b.d, vb.off + i * vs)
            for k, v in enumerate((x, y, z)):
                if v < lo[k]:
                    lo[k] = v
                if v > hi[k]:
                    hi[k] = v
        print('   bbox min  %s' % ['%9.5f' % v for v in lo])
        print('   bbox max  %s' % ['%9.5f' % v for v in hi])
        print('   size      %s' % ['%9.5f' % (hi[k] - lo[k]) for k in range(3)])
    pb = b.follow(mpoly)
    if pb:
        ps = b.sizeof(pb.sdna)
        from collections import Counter
        cnt = Counter()
        mats = Counter()
        for i in range(pb.count):
            tot = struct.unpack_from(E + 'i', b.d, pb.off + i * ps + 4)[0]
            mat = struct.unpack_from(E + 'h', b.d, pb.off + i * ps + 8)[0]
            cnt[tot] += 1
            mats[mat] += 1
        print('   polygon sides: %s' % dict(sorted(cnt.items())))
        print('   material slots used: %s' % dict(sorted(mats.items())))

print()
print('=' * 78)
print('MATERIALS')
print('=' * 78)
for sdna, off in b.of_type('Material'):
    nm = b.name_of(sdna, off)
    r = b.field(sdna, off, 'r')
    g = b.field(sdna, off, 'g')
    bl = b.field(sdna, off, 'b')
    rough = b.field(sdna, off, 'roughness')
    metal = b.field(sdna, off, 'metallic')
    nt = b.field(sdna, off, 'nodetree')
    print('%-30s rgb=(%.3f,%.3f,%.3f)  rough=%s metal=%s  nodes=%s'
          % (nm, r or 0, g or 0, bl or 0,
             ('%.3f' % rough) if rough is not None else '-',
             ('%.3f' % metal) if metal is not None else '-',
             'yes' if nt else 'no'))

print()
print('=' * 78)
print('IMAGES')
print('=' * 78)
for sdna, off in b.of_type('Image'):
    nm = b.name_of(sdna, off)
    path = b.field(sdna, off, 'name')
    packed = b.field(sdna, off, 'packedfile')
    print('%-30s  packed=%s' % (nm, 'yes' if packed else 'no'))
    if path:
        print('    path: %s' % path)

print()
print('=' * 78)
print('LIBRARIES / LINKED')
print('=' * 78)
n = 0
for sdna, off in b.of_type('Library'):
    print('  %s' % b.name_of(sdna, off))
    n += 1
print('  (none)' if n == 0 else '')
