# -*- coding: utf-8 -*-
# Agent-5 findings, p09 (Eventer) + p10 (Medcoin). PDF-only.
import io, re

LOG = []
def op(name, ok):
    LOG.append((' OK    ' if ok else ' **FAIL** ') + name)

c = io.open('casebook.html', encoding='utf-8').read()

# ---- p09 schema: even chip gaps (40u) + centre the diagram in the band ----
def chip(x, w, label, hot=False):
    fill = 'rgba(94,143,191,.14)' if hot else '#25262D'
    stroke = '#5E8FBF' if hot else '#4B4E55'
    tfill = '#F2F1ED' if hot else '#CFD0D4'
    cx = x + w / 2.0
    return ('<rect x="%d" y="20" width="%d" height="22" rx="6" fill="%s" stroke="%s" stroke-width="1.3"/>'
            '<text x="%.1f" y="34.5" text-anchor="middle" font-size="9.5" letter-spacing="1.2" fill="%s">%s</text>'
            % (x, w, fill, stroke, cx, tfill, label)), cx

C1, x1 = chip(10, 130, 'PRODUCT')
C2, x2 = chip(180, 140, 'MARKETING')
C3, x3 = chip(360, 130, 'FINANCE')
C4, x4 = chip(530, 100, 'R&amp;D')
C5, x5 = chip(670, 210, 'BUSINESS DEVELOPMENT', hot=True)
MERGE = 1132
def curve(cx, hot=False):
    col = '#5E8FBF' if hot else '#4B4E55'
    w = '1.7' if hot else '1.3'
    c2x = cx + (MERGE - cx) * 0.55
    return ('<path d="M%.1f 42 C %.1f 72, %.1f 85, %d 85" fill="none" stroke="%s" stroke-width="%s"/>'
            % (cx, cx, c2x, MERGE, col, w))

NEW = ('<svg viewBox="-37 -10 1300 152" style="width:100%;height:auto;display:block" class="conv">'
       + C1 + C2 + C3 + C4 + C5
       + curve(x1) + curve(x2) + curve(x3) + curve(x4) + curve(x5, True)
       + '<path d="M1144 85 l-11 -6 v12 z" fill="#5E8FBF"/>'
       + '<circle cx="1180" cy="85" r="36" fill="#25262D" stroke="#5E8FBF" stroke-width="2.2"/>'
       + '<text x="1180" y="81" text-anchor="middle" font-size="9.5" font-weight="700" letter-spacing="1.4" fill="#F2F1ED">THE</text>'
       + '<text x="1180" y="93" text-anchor="middle" font-size="9.5" font-weight="700" letter-spacing="1.4" fill="#F2F1ED">CUSTOMER</text>'
       + '<path d="M1206 60 C 1262 20, 1150 2, 700 2 L 158 2" fill="none" stroke="#B6B7BB" stroke-width="1.1" stroke-dasharray="3 4"/>'
       + '<path d="M150 2 l11 -5.5 v11 z" fill="#CFD0D4"/>'
       + '<text x="620" y="-5" text-anchor="middle" font-size="9" letter-spacing="1.6" fill="#CFD0D4">CUSTOMER INSIGHT &#8594; BUSINESS DECISIONS</text>'
       + '<text x="1180" y="136" text-anchor="middle" font-size="9" letter-spacing="1.4" fill="#CFD0D4">SHARED RESPONSIBILITY</text>'
       + '</svg>')

i = c.find('<!-- ================= PAGE 09')
j = c.find('<!-- ================= PAGE 10')
p9 = c[i:j]
p9b, n = re.subn(r'<svg viewBox="0 -10 1300 160".*?</svg>', lambda m: NEW, p9, count=1, flags=re.S)
op('p09 schema rebuilt (even gaps, centred, micro-type lifted)', n == 1)
c = c[:i] + (p9b if n else p9) + c[j:]

CSS = """
/* ===== agent-5 pass: p09 (Eventer) + p10 (Medcoin) ===== */
/* grid symmetry + dotted gutter divider, matching p05/p06/p07 */
.p09 .inner{grid-template-columns:1fr 1fr;column-gap:30px}
.p09 .inner::before{left:50%}
.p10b .inner{grid-template-columns:1fr 1fr;column-gap:30px;position:relative}
.p10b .inner::before{content:"";position:absolute;left:50%;top:4px;bottom:4px;width:1px;
  background:repeating-linear-gradient(180deg,var(--grid) 0 5px,transparent 5px 11px)}
/* body scale back to the document tokens (compression residue) */
.p09 .para{font-size:12px;line-height:1.55}
.p09 .lg{font-size:11.8px;margin-bottom:6px}
.p10b .para{font-size:12px;line-height:1.55}
.p10b .lg2{font-size:11.8px}
.p10b .para3{font-size:12px;line-height:1.5}
/* one zone-separation token on both pages */
.p09 .z{margin-bottom:15px}
.p10b .z{margin-bottom:15px}
.p10b .inner>div:last-child>.zr{margin-top:15px}
.p10b .inner>div:last-child>.zr:first-child{margin-top:0}
/* p09: level the two column heads + rebalance the short right column */
.p09 .inner>div{display:flex;flex-direction:column}
.p09 .inner>div:last-child{justify-content:space-between;padding-bottom:2px}
/* full-width rules reach the document ink edge */
.p09 .band,.p10b .tl2,.p10b .band2{margin-right:0}
"""
k = c.rfind('</style>')
c = c[:k] + CSS + '\n' + c[k:]
io.open('casebook.html', 'w', encoding='utf-8', newline='').write(c)
LOG.append('== casebook written')
print('\n'.join(LOG))
