# -*- coding: utf-8 -*-
# Agent-4 findings, Oasis pair (p07/p08). PDF-only.
import io, re

LOG = []
def op(name, ok):
    LOG.append((' OK    ' if ok else ' **FAIL** ') + name)

c = io.open('casebook.html', encoding='utf-8').read()

# F6: zone C heading must sit on the column-left line like A and B
old = '<div class="zr" style="justify-content:center"><b>C</b><span class="d2"></span>CROSS-FUNCTIONAL LEADERSHIP</div>'
op('F6 C heading inline centring removed', c.count(old) == 1)
c = c.replace(old, '<div class="zr"><b>C</b><span class="d2"></span>CROSS-FUNCTIONAL LEADERSHIP</div>', 1)

# F7: ring diagram must not overhang the column's right ink edge
old = '<svg viewBox="0 0 240 196" style="width:100%;max-width:250px;height:auto;margin:0 auto;overflow:visible">'
op('F7 ring svg max-width', c.count(old) == 1)
c = c.replace(old, '<svg viewBox="0 0 240 196" style="width:100%;max-width:228px;height:auto;margin:0 auto;overflow:visible">', 1)

CSS = """
/* ===== agent-4 pass: Oasis pair symmetry (p07/p08) ===== */
/* F5 card padding parity with the corrected p05/p06 norm */
.p07 .folder,.p08 .folder{padding-top:22px;padding-right:26px}
/* F2 one shared checklist size + rhythm across the pair (kit base 11.8px) */
.p07 .lg,.p08 .lg{font-size:11.8px;margin-bottom:9.5px}
/* F3 zone paragraphs back to the kit base */
.p07 .para{font-size:12px;line-height:1.55}
/* F4 chip labels optically centred inside the stretched chip box */
.p07 .chip{display:flex;flex-direction:column;justify-content:center}
/* F1 LEADERSHIP MODEL band anchored at the card bottom, zones spread above it */
.p07 .folder{display:flex;flex-direction:column}
.p07 .inner{flex:1}
.p07 .inner>div{display:flex;flex-direction:column}
.p07 .inner>div>.z:last-child{margin-bottom:0}
.p07 .model{margin-top:auto}
"""
k = c.rfind('</style>')
c = c[:k] + CSS + '\n' + c[k:]
io.open('casebook.html', 'w', encoding='utf-8', newline='').write(c)
LOG.append('== casebook written')
print('\n'.join(LOG))
