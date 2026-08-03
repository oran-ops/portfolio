# -*- coding: utf-8 -*-
# p09 convergence band: compact vertical layout that fits the card, centred, even gaps.
import io, re

def chip(x, w, label, hot=False):
    fill = 'rgba(94,143,191,.14)' if hot else '#25262D'
    stroke = '#5E8FBF' if hot else '#4B4E55'
    tfill = '#F2F1ED' if hot else '#CFD0D4'
    cx = x + w / 2.0
    return ('<rect x="%d" y="18" width="%d" height="22" rx="6" fill="%s" stroke="%s" stroke-width="1.3"/>'
            '<text x="%.1f" y="32.5" text-anchor="middle" font-size="9" letter-spacing="1.2" fill="%s">%s</text>'
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
    return ('<path d="M%.1f 40 C %.1f 64, %.1f 74, %d 74" fill="none" stroke="%s" stroke-width="%s"/>'
            % (cx, cx, c2x, MERGE, col, w))

NEW = ('<svg viewBox="-39 -15 1300 136" style="width:100%;height:auto;display:block" class="conv">'
       + C1 + C2 + C3 + C4 + C5
       + curve(x1) + curve(x2) + curve(x3) + curve(x4) + curve(x5, True)
       + '<path d="M1148 74 l-11 -6 v12 z" fill="#5E8FBF"/>'
       + '<circle cx="1180" cy="74" r="32" fill="#25262D" stroke="#5E8FBF" stroke-width="2.2"/>'
       + '<text x="1180" y="70.5" text-anchor="middle" font-size="9" font-weight="700" letter-spacing="1.4" fill="#F2F1ED">THE</text>'
       + '<text x="1180" y="82" text-anchor="middle" font-size="9" font-weight="700" letter-spacing="1.4" fill="#F2F1ED">CUSTOMER</text>'
       + '<path d="M1204 52 C 1258 18, 1150 5, 700 5 L 161 5" fill="none" stroke="#B6B7BB" stroke-width="1.1" stroke-dasharray="3 4"/>'
       + '<path d="M153 5 l11 -5.5 v11 z" fill="#CFD0D4"/>'
       + '<text x="620" y="-6" text-anchor="middle" font-size="8.5" letter-spacing="1.6" fill="#CFD0D4">CUSTOMER INSIGHT &#8594; BUSINESS DECISIONS</text>'
       + '<text x="1180" y="116" text-anchor="middle" font-size="8.5" letter-spacing="1.4" fill="#CFD0D4">SHARED RESPONSIBILITY</text>'
       + '</svg>')

c = io.open('casebook.html', encoding='utf-8').read()
i = c.find('<!-- ================= PAGE 09')
j = c.find('<!-- ================= PAGE 10')
p9 = c[i:j]
p9b, n = re.subn(r'<svg viewBox="-37 -10 1300 152".*?</svg>', lambda m: NEW, p9, count=1, flags=re.S)
print('schema replaced:', n)
assert n == 1
c = c[:i] + p9b + c[j:]

# right column back to natural flow (space-between was pushing the band off the card)
old = '.p09 .inner>div:last-child{justify-content:space-between;padding-bottom:2px}'
assert c.count(old) == 1
c = c.replace(old, '.p09 .inner>div:last-child{justify-content:flex-start}', 1)
io.open('casebook.html', 'w', encoding='utf-8', newline='').write(c)
print('done')
