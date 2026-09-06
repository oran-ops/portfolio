# -*- coding: utf-8 -*-
"""Read a .blend without Blender.

A .blend is a memory dump plus a description of its own layout: the DNA1 block lists every
struct the writing build knew, field by field. Parse that and every other block becomes
readable by name, which is the only reason this is a sane thing to do rather than a guess at
byte offsets.

  header  : "BLENDER" + pointer size (underscore=4, dash=8) + endianness (v=LE, V=BE) + version
  block   : 4-char code, int32 size, old-address (pointer-sized), int32 SDNA index, int32 count
  DNA1    : SDNA / NAME n names / TYPE n types / TLEN shorts / STRC n structs
"""
import gzip
import struct
import sys

sys.stdout.reconfigure(encoding='utf-8', errors='replace')

SCALAR = {'char': 'b', 'uchar': 'B', 'short': 'h', 'ushort': 'H', 'int': 'i',
          'uint': 'I', 'float': 'f', 'double': 'd', 'int64_t': 'q',
          'uint64_t': 'Q', 'int8_t': 'b', 'ulong': 'Q', 'long': 'q'}


class Block(object):
    __slots__ = ('code', 'size', 'old', 'sdna', 'count', 'off')

    def __init__(self, code, size, old, sdna, count, off):
        self.code, self.size, self.old = code, size, old
        self.sdna, self.count, self.off = sdna, count, off

    def __repr__(self):
        return '<%s size=%d count=%d sdna=%d>' % (self.code, self.size, self.count, self.sdna)


class Blend(object):
    def __init__(self, path):
        d = open(path, 'rb').read()
        if d[:2] == b'\x1f\x8b':
            d = gzip.decompress(d)
        if d[:7] != b'BLENDER':
            raise SystemExit('not a .blend (and not gzip-wrapped): %r' % d[:8])
        self.d = d
        self.ptr = 8 if d[7:8] == b'-' else 4
        self.E = '<' if d[8:9] == b'v' else '>'
        self.version = d[9:12].decode()
        self.blocks = []
        self.by_old = {}
        self._scan()
        self._dna()

    # ---- blocks -------------------------------------------------------------
    def _scan(self):
        d, E, P = self.d, self.E, self.ptr
        o = 12
        hdr = 16 + P
        pcode = 'Q' if P == 8 else 'I'
        while o + hdr <= len(d):
            code = d[o:o + 4].rstrip(b'\x00').decode('ascii', 'replace')
            size = struct.unpack_from(E + 'i', d, o + 4)[0]
            old = struct.unpack_from(E + pcode, d, o + 8)[0]
            sdna, cnt = struct.unpack_from(E + 'ii', d, o + 8 + P)
            b = Block(code, size, old, sdna, cnt, o + hdr)
            self.blocks.append(b)
            if old:
                self.by_old[old] = b
            if code == 'ENDB':
                break
            o += hdr + size

    # ---- DNA ----------------------------------------------------------------
    def _dna(self):
        blk = [b for b in self.blocks if b.code == 'DNA1'][0]
        d, E = self.d, self.E
        o = blk.off
        assert d[o:o + 4] == b'SDNA'
        o += 4
        state = {'o': o}

        def strings(tag):
            o = state['o']
            assert d[o:o + 4] == tag, (tag, d[o:o + 4])
            o += 4
            n = struct.unpack_from(E + 'i', d, o)[0]
            o += 4
            out = []
            for _ in range(n):
                e = d.index(b'\x00', o)
                out.append(d[o:e].decode('ascii', 'replace'))
                o = e + 1
            state['o'] = (o + 3) & ~3
            return out

        self.names = strings(b'NAME')
        self.types = strings(b'TYPE')
        o = state['o']
        assert d[o:o + 4] == b'TLEN'
        o += 4
        self.tlen = list(struct.unpack_from(E + '%dh' % len(self.types), d, o))
        o += 2 * len(self.types)
        o = (o + 3) & ~3
        assert d[o:o + 4] == b'STRC'
        o += 4
        ns = struct.unpack_from(E + 'i', d, o)[0]
        o += 4
        self.structs = []          # [(type_idx, [(type_idx, name_idx), ...]), ...]
        for _ in range(ns):
            ti, nf = struct.unpack_from(E + 'hh', d, o)
            o += 4
            fs = list(struct.unpack_from(E + '%dh' % (2 * nf), d, o))
            o += 4 * nf
            self.structs.append((ti, list(zip(fs[0::2], fs[1::2]))))
        self.sname = {}
        for i, (t, _) in enumerate(self.structs):
            self.sname[self.types[t]] = i
        self._lay = {}

    def fsize(self, ti, name):
        base = self.ptr if (name.startswith('*') or name.startswith('(*')) else self.tlen[ti]
        n, i = 1, 0
        while '[' in name[i:]:
            a = name.index('[', i)
            b = name.index(']', a)
            n *= int(name[a + 1:b])
            i = b + 1
        return base * n

    def layout(self, sdna):
        """{plain field name: (offset, type name, raw name)}"""
        if sdna in self._lay:
            return self._lay[sdna]
        out, off = {}, 0
        for ti, ni in self.structs[sdna][1]:
            raw = self.names[ni]
            bare = raw.lstrip('*').split('[')[0].replace('(', '').replace(')', '')
            out[bare] = (off, self.types[ti], raw)
            off += self.fsize(ti, raw)
        self._lay[sdna] = out
        return out

    def sizeof(self, sdna):
        return self.tlen[self.structs[sdna][0]]

    # ---- reading ------------------------------------------------------------
    def field(self, sdna, base, name):
        lay = self.layout(sdna)
        if name not in lay:
            return None
        off, tname, raw = lay[name]
        o = base + off
        d, E, P = self.d, self.E, self.ptr
        if raw.startswith('*') or raw.startswith('(*'):
            return struct.unpack_from(E + ('Q' if P == 8 else 'I'), d, o)[0]
        n, i = 1, 0
        while '[' in raw[i:]:
            a = raw.index('[', i)
            b = raw.index(']', a)
            n *= int(raw[a + 1:b])
            i = b + 1
        code = SCALAR.get(tname)
        if code is None:
            return ('struct', tname, o)
        v = struct.unpack_from(E + '%d%s' % (n, code), d, o)
        if tname == 'char' and n > 1:
            return bytes(x & 0xff for x in v).split(b'\x00')[0].decode('utf-8', 'replace')
        return v[0] if n == 1 else list(v)

    def sub(self, sdna, base, name):
        """(sdna, offset) of a nested struct field"""
        off, tname, raw = self.layout(sdna)[name]
        return self.sname[tname], base + off

    def items(self, blk):
        sz = self.sizeof(blk.sdna)
        for i in range(blk.count):
            yield blk.sdna, blk.off + i * sz

    def follow(self, addr):
        return self.by_old.get(addr)

    def name_of(self, sdna, base):
        lay = self.layout(sdna)
        if 'id' in lay and lay['id'][1] == 'ID':
            s, o = self.sub(sdna, base, 'id')
            return self.field(s, o, 'name')
        if 'name' in lay:
            return self.field(sdna, base, 'name')
        return None

    def of_type(self, tname):
        """every (sdna, offset) whose struct is tname"""
        want = self.sname.get(tname)
        if want is None:
            return
        for b in self.blocks:
            if b.sdna == want and b.code not in ('DNA1', 'ENDB'):
                for it in self.items(b):
                    yield it


if __name__ == '__main__':
    b = Blend(sys.argv[1])
    print('blender %s   pointer %d   %s-endian'
          % (b.version, b.ptr, 'little' if b.E == '<' else 'big'))
    print('%d blocks, %d structs, %d types' % (len(b.blocks), len(b.structs), len(b.types)))
    from collections import Counter
    c = Counter(x.code for x in b.blocks)
    print('block codes:', ', '.join('%s=%d' % kv for kv in c.most_common(30)))
