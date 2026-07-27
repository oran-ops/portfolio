# -*- coding: utf-8 -*-
# Round 7b — make the new bottom bands fit the fixed-height PDF cards.
import io, re

p = 'casebook.html'
s = io.open(p, encoding='utf-8').read()
LOG = []

def op(name, fn):
    global s
    try:
        out = fn(s)
        if out is None or out == s:
            LOG.append(' SKIP  ' + name)
        else:
            s = out; LOG.append(' OK    ' + name)
    except Exception as e:
        LOG.append(' ERR   %s :: %s' % (name, str(e)[:90]))

def css_end(add):
    def f(t):
        k = t.rfind('</style>')
        return t[:k] + add + '\n' + t[k:]
    return f

# p13: the sign-off moves under ABOUT ME so the card closes cleanly
def p13_closeline(t):
    line = '<div class="closeline">Turning vision into <b>commercial growth</b>.</div>'
    i = t.find('class="page casef p13"')
    if i < 0: return None
    j = t.find('</section>', i)
    seg = t[i:j]
    if line not in seg: return None
    seg2 = seg.replace('\n      ' + line, '')
    anchor = 'My goal is to leave every company <b>stronger than I found it</b>.</div>'
    if anchor not in seg2: return None
    seg2 = seg2.replace(anchor, anchor + '\n          ' + line, 1)
    return t[:i] + seg2 + t[j:]

FIT = """
/* R7b — bottom bands fit inside the fixed-height cards */
.p06 .band .lesson{margin-top:7px!important;padding-top:6px!important}
.p06 .lesson .qx{font-size:10.9px!important;line-height:1.4}
.p06 .tbl td{padding:4px 2px}
.p06 .gaug{margin-top:5px;padding-top:5px}
.p06 .g1 svg{width:54px!important;height:54px!important}
.p06 .ops .lg{margin-bottom:2px}
.p06 .tech{margin-top:8px;padding:8px 13px}
.p06 .refl2{gap:2px 18px}
.p06 .band .dash{font-size:10.3px}
.p13 .pi{padding:5px 0 4px}
.p13 .pi .t{font-size:11px;line-height:1.35}
.p13 .vseal{margin-top:12px;padding:13px 26px 11px}
.p13 .vseal .vq{font-size:15.5px;line-height:1.34}
.p13 .vseal .vsig{margin-top:8px}
.p13 .fbot{margin-top:13px;gap:26px}
.p13 .abt{font-size:11.6px;line-height:1.55}
.p13 .card{margin-top:24px}
.p13 .crow{padding:7px 0}
.p13 .closeline{margin-top:12px;padding-top:9px;font-size:12.4px;text-align:left}
"""

op('p13 sign-off moved under ABOUT ME', p13_closeline)
op('fit adjustments', css_end(FIT))
io.open(p, 'w', encoding='utf-8', newline='').write(s)
print('\n'.join(LOG))
print('casebook now', len(s.encode('utf-8')), 'bytes')
