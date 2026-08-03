# -*- coding: utf-8 -*-
# Agent-3 findings, XTIX pair (p05/p06). PDF-only (site has its own flowing layout).
import io, re

LOG = []
def op(name, ok):
    LOG.append((' OK    ' if ok else ' **FAIL** ') + name)

c = io.open('casebook.html', encoding='utf-8').read()

# --- F1: p06 grid symmetry (46fr/54fr -> 1fr 1fr, gap 30px like p05 .cols) ---
old = '.p06 .inner{display:grid;grid-template-columns:46fr 54fr;column-gap:28px}'
op('F1 grid 1fr 1fr', c.count(old) == 1)
c = c.replace(old, '.p06 .inner{display:grid;grid-template-columns:1fr 1fr;column-gap:30px;position:relative}', 1)

# --- F11: chart placeholders sit on the bar baseline (y 50 h 16 -> bottom 66) ---
n = c.count('<rect x="40" y="50" width="30" height="16"')
op('F11 placeholder rects (3)', n == 1 and c.count('y="50" width="30" height="16"') == 3)
for x in ('40', '86', '132'):
    c = c.replace('<rect x="%s" y="50" width="30" height="16"' % x,
                  '<rect x="%s" y="51.5" width="30" height="16"' % x, 1)

# --- CSS block: everything else ---
CSS = """
/* ===== agent-3 pass: XTIX pair symmetry (p05/p06) ===== */
/* F2 dotted column divider — parity with p05/p07/p09/p11/p13 */
.p06 .inner::before{content:"";position:absolute;left:50%;top:4px;bottom:4px;width:1px;
  background:repeating-linear-gradient(180deg,var(--grid) 0 5px,transparent 5px 11px)}
/* F3 body scale back to family default (compression residue from earlier rounds) */
.p06 .ops .lg{font-size:11.8px;margin-bottom:5.7px}
.p06 .tech .para{font-size:12px;line-height:1.55}
.p06 .band .dash{font-size:11.8px}
/* F4 card top padding parity with p05 */
.p06 .folder{padding-top:22px}
/* F5 columns start level: kill the table's first-row top padding */
.p06 .tbl tr:first-child td{padding-top:0}
/* F6 marker parity: square -> diamond like every other zone marker */
.p06 .cosb .sq2{transform:rotate(45deg)}
/* F7 STARTING POINT box: last row gets the same air as the others */
.p05 .reality{padding-bottom:2px}
/* F8 right-aligned tracked mono hangs flush to the edge */
.p05 .plabel,.p06 .plabel,.p07 .plabel,.p08 .plabel{margin-right:-0.24em}
.ftr span:last-child{margin-right:-0.14em}
"""
k = c.rfind('</style>')
c = c[:k] + CSS + '\n' + c[k:]
io.open('casebook.html', 'w', encoding='utf-8', newline='').write(c)
LOG.append('== casebook written')
print('\n'.join(LOG))
