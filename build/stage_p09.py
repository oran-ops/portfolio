# -*- coding: utf-8 -*-
# Corrections round, stage: page 9 / eventer (items 25, 26, 27, 28).
# New reading order: 01-04 left col, 05-06 right col, 07 = convergence band of honor.
import io, re

LOG = []
def op(name, ok):
    LOG.append((' OK    ' if ok else ' **FAIL** ') + name)

SUB_OLD = 'EVENTER &middot; SAAS &middot; EVENT MANAGEMENT PLATFORM'
SUB_NEW = 'EVENTER &middot; SAAS &middot; EVENT-TECH PLATFORM'

def chip(x, w, label, hot=False):
    fill = 'rgba(94,143,191,.14)' if hot else '#25262D'
    stroke = '#5E8FBF' if hot else '#4B4E55'
    tfill = '#F2F1ED' if hot else '#CFD0D4'
    cx = x + w / 2.0
    return ('<rect x="%d" y="20" width="%d" height="22" rx="6" fill="%s" stroke="%s" stroke-width="1.3"/>'
            '<text x="%.1f" y="34.5" text-anchor="middle" font-size="8.5" letter-spacing="1.2" fill="%s">%s</text>'
            % (x, w, fill, stroke, cx, tfill, label)), cx

C1, x1 = chip(10, 130, 'PRODUCT')
C2, x2 = chip(190, 140, 'MARKETING')
C3, x3 = chip(370, 130, 'FINANCE')
C4, x4 = chip(540, 100, 'R&amp;D')
C5, x5 = chip(680, 210, 'BUSINESS DEVELOPMENT', hot=True)
def curve(cx, hot=False):
    col = '#5E8FBF' if hot else '#4B4E55'
    w = '1.7' if hot else '1.3'
    return '<path d="M%.1f 42 C %.1f 78, 960 85, 1092 85" fill="none" stroke="%s" stroke-width="%s"/>' % (cx, cx, col, w)

NEWSVG = ('<svg viewBox="0 -10 1300 160" style="width:100%;height:auto;display:block" class="conv">'
          + C1 + C2 + C3 + C4 + C5
          + curve(x1) + curve(x2) + curve(x3) + curve(x4) + curve(x5, True)
          + '<path d="M1104 85 l-10 -5.5 v11 z" fill="#5E8FBF"/>'
          + '<circle cx="1180" cy="85" r="36" fill="#25262D" stroke="#5E8FBF" stroke-width="2.2"/>'
          + '<text x="1180" y="81" text-anchor="middle" font-size="9.5" font-weight="700" letter-spacing="1.4" fill="#F2F1ED">THE</text>'
          + '<text x="1180" y="93" text-anchor="middle" font-size="9.5" font-weight="700" letter-spacing="1.4" fill="#F2F1ED">CUSTOMER</text>'
          + '<path d="M1206 60 C 1262 20, 1150 4, 700 4 L 118 4" fill="none" stroke="#B6B7BB" stroke-width="1.1" stroke-dasharray="3 4"/>'
          + '<path d="M110 4 l11 -5.5 v11 z" fill="#CFD0D4"/>'
          + '<text x="650" y="-3" text-anchor="middle" font-size="8" letter-spacing="1.6" fill="#CFD0D4">CUSTOMER INSIGHT &#8594; BUSINESS DECISIONS</text>'
          + '<text x="1180" y="140" text-anchor="middle" font-size="8" letter-spacing="1.4" fill="#CFD0D4">SHARED RESPONSIBILITY</text>'
          + '</svg>')

LEARN_ZONE = ('<div class="zr" style="margin-top:14px"><b>06</b><span class="d2"></span>WHAT I LEARNED</div>\n'
              '        <div class="para">Leadership doesn\'t require authority &mdash; <b>influence, collaboration and better decisions</b> move organizations.</div>')

# ================= PDF =================
c = io.open('casebook.html', encoding='utf-8').read()
i = c.find('<!-- ================= PAGE 09')
j = c.find('<!-- ================= PAGE 10')
assert 0 < i < j
p9 = c[i:j]

n = p9.count(SUB_OLD); op('PDF 25 subtitle', n == 1)
p9 = p9.replace(SUB_OLD, SUB_NEW, 1)
n = p9.count('<b>EV</b>'); op('PDF 27 EV->04', n == 1)
p9 = p9.replace('<b>EV</b>', '<b>04</b>', 1)
p9b, n = re.subn(r'<div class="zr"><b>04</b><span class="d2"></span>ORGANIZATIONAL CONVERGENCE</div>\s*<svg class="conv".*?</svg>\s*', '', p9, count=1, flags=re.S)
op('PDF 27 old convergence zone cut', n == 1); p9 = p9b if n else p9
# band: 06 -> 07 + new svg (do BEFORE re-inserting 06 in the right column)
OLD_BAND_INNER = ('<div class="zr"><b>06</b><span class="d2"></span>WHAT I LEARNED</div>\n        '
                  '<div class="para">Leadership doesn\'t require authority &mdash; <b>influence, collaboration and better decisions</b> move organizations.</div>')
n = p9.count(OLD_BAND_INNER); op('PDF 27 band anchor', n == 1)
p9 = p9.replace(OLD_BAND_INNER,
                '<div class="zr"><b>07</b><span class="d2"></span>ORGANIZATIONAL CONVERGENCE</div>\n        ' + NEWSVG, 1)
LAST_LG = 'Helped improve commercial alignment across the organization</div>'
n = p9.count(LAST_LG); op('PDF 27 right-col tail anchor', n == 1)
p9 = p9.replace(LAST_LG, LAST_LG + '\n        ' + LEARN_ZONE, 1)
p9b, n = re.subn(r'\s*<div data-moved class="insight">\s*<div class="qx">Commercial growth accelerates.*?</div>\s*</div>', '', p9, count=1, flags=re.S)
op('PDF 26 closer removed', n == 1); p9 = p9b if n else p9

c = c[:i] + p9 + c[j:]
PDF_CSS = """
/* corrections p09 — convergence band of honor */
.p09 .folder{display:flex;flex-direction:column}
.p09 .band{grid-template-columns:1fr;margin-top:auto;padding-top:12px;padding-bottom:2px}
.p09 .conv{margin:4px 0 0}
"""
k = c.rfind('</style>')
c = c[:k] + PDF_CSS + '\n' + c[k:]
io.open('casebook.html', 'w', encoding='utf-8', newline='').write(c)
LOG.append('== casebook written')

# ================= SITE =================
s = io.open('site.html', encoding='utf-8').read()
a = s.find('id="eventer"')
b = s.find('id="medcoin"')
assert 0 < a < b
x = s[a:b]

n = x.count(SUB_OLD); op('SITE 25 subtitle', n == 1)
x = x.replace(SUB_OLD, SUB_NEW, 1)
n = x.count('<b>EV</b>'); op('SITE 27 EV->04', n == 1)
x = x.replace('<b>EV</b>', '<b>04</b>', 1)
xb, n = re.subn(r'<div class="zr[^"]*"[^>]*><b>04</b><span class="d2"></span>ORGANIZATIONAL CONVERGENCE</div>\s*<svg.*?</svg>\s*', '', x, count=1, flags=re.S)
op('SITE 27 old convergence cut', n == 1); x = xb if n else x
# closer slot becomes the schema finale
NEW_FINALE = ('<div class="hairtop"><div class="zr rv"><b>07</b><span class="d2"></span>ORGANIZATIONAL CONVERGENCE</div>'
              '<div class="convwrap rv" style="--i:1">' + NEWSVG + '</div></div>')
xb, n = re.subn(r'<div class="lessq rv"[^>]*>\s*<div class="qx">Commercial growth accelerates.*?</div>\s*</div>', NEW_FINALE, x, count=1, flags=re.S)
op('SITE 26+27 closer -> finale', n == 1); x = xb if n else x

s = s[:a] + x + s[b:]
SITE_CSS = """
/* corrections p09 (eventer) */
#eventer .convwrap{width:100%;margin-top:6px}
@media (max-width:860px){#eventer .convwrap{overflow-x:auto;-webkit-overflow-scrolling:touch}
#eventer .convwrap svg{min-width:820px}}
"""
k = s.rfind('</style>')
s = s[:k] + SITE_CSS + '\n' + s[k:]
io.open('site.html', 'w', encoding='utf-8', newline='').write(s)
head = ('<!doctype html>\n<html lang="en">\n<head>\n<meta charset="utf-8">\n'
        '<meta name="viewport" content="width=device-width,initial-scale=1">\n'
        '<meta name="color-scheme" content="dark">\n</head>\n<body>\n')
io.open('site_standalone.html', 'w', encoding='utf-8', newline='').write(head + s + '\n</body>\n</html>')
LOG.append('== site written + standalone rebuilt')

cc = io.open('casebook.html', encoding='utf-8').read()
ss = io.open('site.html', encoding='utf-8').read()
LOG.append('   casebook: EVENT MGMT=%d | EVENT-TECH=%d | accelerates=%d | b07=%d | EV=%d' %
    (cc.count('EVENT MANAGEMENT'), cc.count('EVENT-TECH'), cc.count('accelerates'),
     cc.count('<b>07</b><span class="d2"></span>ORGANIZATIONAL'), cc.count('<b>EV</b>')))
LOG.append('   site:     EVENT MGMT=%d | EVENT-TECH=%d | accelerates=%d | b07=%d | EV=%d' %
    (ss.count('EVENT MANAGEMENT'), ss.count('EVENT-TECH'), ss.count('accelerates'),
     ss.count('<b>07</b><span class="d2"></span>ORGANIZATIONAL'), ss.count('<b>EV</b>')))
print('\n'.join(LOG))
