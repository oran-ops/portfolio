# -*- coding: utf-8 -*-
# p10 PDF pass (rerun after restore): balanced zone-03 capture anchored on its tail text.
import io, re

LOG = []
def op(name, ok):
    LOG.append((' OK    ' if ok else ' **FAIL** ') + name)
    return ok

c = io.open('casebook.html', encoding='utf-8').read()
i = c.find('<!-- ================= PAGE 10')
j = c.find('<!-- ================= PAGE 11')
assert 0 < i < j
p = c[i:j]

# zone 03: capture through the z-div close, anchored on the final lg2 text
m = re.search(r'<div class="z" style="margin-bottom:0">\s*<div class="zr"><b>03</b>.*?user experience</div></div>\s*</div>', p, re.S)
op('PDF 32 zone-03 located (balanced)', bool(m))
assert m
z3 = m.group(0)
assert z3.count('<div') == z3.count('</div>'), 'unbalanced capture: %d vs %d' % (z3.count('<div'), z3.count('</div>'))
op('PDF 32 capture balanced (%d divs)' % z3.count('<div'), True)
p = p.replace(z3, '', 1)
z3_clean = z3.replace('<div class="z" style="margin-bottom:0">', '<div class="z">', 1)
anchor = '<div class="zr"><b>04</b><span class="d2"></span>BUSINESS OUTCOMES</div>'
n = p.count(anchor); op('PDF 32 zone-04 anchor', n == 1)
assert n == 1
p = p.replace(anchor, z3_clean + '\n        ' + anchor, 1)

p2, n = re.subn(r'\s*<div class="why"><span class="wl">WHY IT ENDED</span>.*?</div></div>', '', p, count=1, flags=re.S)
op('PDF 33 WHY removed', n == 1); p = p2 if n else p
p2, n = re.subn(r'\s*<div data-moved class="lessq2">\s*<div class="qx">Founders don\'t manage functions.*?</div>\s*</div>', '', p, count=1, flags=re.S)
op('PDF 30 closer removed', n == 1); p = p2 if n else p
n = p.count('<line x1="26" y1="26" x2="906"'); op('PDF 29 line anchor', n == 1)
p = p.replace('<line x1="26" y1="26" x2="906"', '<line x1="40" y1="26" x2="906"', 1)

c = c[:i] + p + c[j:]
PDF_CSS = """
/* corrections p10 — order + rhythm */
.p10b .inner{grid-template-columns:44fr 56fr}
.p10b .inner>div:first-child{display:flex;flex-direction:column;justify-content:space-evenly;padding-bottom:6px}
.p10b .inner>div:first-child .z{margin-bottom:0}
.p10b .folder{display:flex;flex-direction:column}
.p10b .tl2{margin-top:auto}
.p10b .band2{grid-template-columns:1fr;margin-top:10px;padding-top:12px;padding-bottom:6px}
"""
k = c.rfind('</style>')
c = c[:k] + PDF_CSS + '\n' + c[k:]
io.open('casebook.html', 'w', encoding='utf-8', newline='').write(c)

seg = c[c.find('PAGE 10'):c.find('PAGE 11')]
i02 = seg.find('<b>02</b>'); i03 = seg.find('<b>03</b>'); i04 = seg.find('<b>04</b>')
LOG.append('   order: 02@%d < 03@%d < 04@%d -> %s' % (i02, i03, i04, 'OK' if 0 < i02 < i03 < i04 else 'FAIL'))
LOG.append('   residue: WHY=%d Turkey=%d closer=%d' % (seg.count('WHY IT ENDED'), seg.count('Turkey'), seg.count("Founders don't")))
print('\n'.join(LOG))
