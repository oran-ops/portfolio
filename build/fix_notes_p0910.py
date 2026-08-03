# -*- coding: utf-8 -*-
# User notes on p09 + p10.
import io, re

LOG = []
def op(name, ok):
    LOG.append((' OK    ' if ok else ' **FAIL** ') + name)

c = io.open('casebook.html', encoding='utf-8').read()

# ================= p09: compact schema, label clear of the circle =================
def chip(x, w, label, hot=False):
    fill = 'rgba(94,143,191,.14)' if hot else '#25262D'
    stroke = '#5E8FBF' if hot else '#4B4E55'
    tfill = '#F2F1ED' if hot else '#CFD0D4'
    cx = x + w / 2.0
    return ('<rect x="%d" y="14" width="%d" height="21" rx="6" fill="%s" stroke="%s" stroke-width="1.3"/>'
            '<text x="%.1f" y="27.8" text-anchor="middle" font-size="9" letter-spacing="1.2" fill="%s">%s</text>'
            % (x, w, fill, stroke, cx, tfill, label)), cx

C1, x1 = chip(10, 130, 'PRODUCT')
C2, x2 = chip(180, 140, 'MARKETING')
C3, x3 = chip(360, 130, 'FINANCE')
C4, x4 = chip(530, 100, 'R&amp;D')
C5, x5 = chip(670, 210, 'BUSINESS DEVELOPMENT', hot=True)
MERGE = 1136
def curve(cx, hot=False):
    col = '#5E8FBF' if hot else '#4B4E55'
    w = '1.7' if hot else '1.3'
    c2x = cx + (MERGE - cx) * 0.55
    return ('<path d="M%.1f 35 C %.1f 55, %.1f 64, %d 64" fill="none" stroke="%s" stroke-width="%s"/>'
            % (cx, cx, c2x, MERGE, col, w))

NEW = ('<svg viewBox="-39 -14 1300 122" style="width:100%;height:auto;display:block" class="conv">'
       + C1 + C2 + C3 + C4 + C5
       + curve(x1) + curve(x2) + curve(x3) + curve(x4) + curve(x5, True)
       + '<path d="M1150 64 l-11 -6 v12 z" fill="#5E8FBF"/>'
       + '<circle cx="1180" cy="64" r="27" fill="#25262D" stroke="#5E8FBF" stroke-width="2.2"/>'
       + '<text x="1180" y="61" text-anchor="middle" font-size="8.6" font-weight="700" letter-spacing="1.3" fill="#F2F1ED">THE</text>'
       + '<text x="1180" y="71.5" text-anchor="middle" font-size="8.6" font-weight="700" letter-spacing="1.3" fill="#F2F1ED">CUSTOMER</text>'
       + '<path d="M1201 45 C 1252 16, 1150 4, 700 4 L 161 4" fill="none" stroke="#B6B7BB" stroke-width="1.1" stroke-dasharray="3 4"/>'
       + '<path d="M153 4 l11 -5.5 v11 z" fill="#CFD0D4"/>'
       + '<text x="620" y="-6" text-anchor="middle" font-size="8.5" letter-spacing="1.6" fill="#CFD0D4">CUSTOMER INSIGHT &#8594; BUSINESS DECISIONS</text>'
       + '<text x="1180" y="104" text-anchor="middle" font-size="8.5" letter-spacing="1.4" fill="#CFD0D4">SHARED RESPONSIBILITY</text>'
       + '</svg>')

i = c.find('<!-- ================= PAGE 09')
j = c.find('<!-- ================= PAGE 10')
p9 = c[i:j]
p9b, n = re.subn(r'<svg viewBox="-39 -15 1300 131".*?</svg>', lambda m: NEW, p9, count=1, flags=re.S)
op('p09 schema compacted (circle r27 @cy64, label y104 -> 13u clearance)', n == 1)
c = c[:i] + (p9b if n else p9) + c[j:]

# ================= p10: shorten zones 01/02 =================
V_OLD = 'A <b>compliant, scalable crypto-ATM network</b> &mdash; accessible digital finance for Europe.'
V_NEW = 'A <b>compliant, scalable crypto-ATM network</b> for Europe.'
C_OLD = 'From zero, <b>every decision was mine</b> &mdash; model, partnerships, compliance, operations, commercialization.'
C_NEW = 'From zero, <b>every decision was mine</b> &mdash; model, partnerships, compliance, operations.'
op('p10 zone 01 shortened', c.count(V_OLD) == 1); c = c.replace(V_OLD, V_NEW, 1)
op('p10 zone 02 shortened', c.count(C_OLD) == 1); c = c.replace(C_OLD, C_NEW, 1)

CSS = """
/* ===== user notes on p09 / p10 ===== */
/* p09-1: breathing room between the evidence tiles and the rule below */
.p09 .etr{margin-bottom:11px}
.p09 .band{padding-top:12px}
/* p10-1: zone 05 heading off the rule above it */
.p10b .tl2{padding-top:11px}
/* p10-2: give zones 03/04 the width they need so list items sit on one line */
.p10b .inner{grid-template-columns:32fr 68fr}
.p10b .inner::before{left:32.5%}
.p10b .bgrid{grid-template-columns:1fr 1.26fr}
"""
k = c.rfind('</style>')
c = c[:k] + CSS + '\n' + c[k:]
io.open('casebook.html', 'w', encoding='utf-8', newline='').write(c)
LOG.append('== casebook written')
print('\n'.join(LOG))
