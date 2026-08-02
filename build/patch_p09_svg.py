# -*- coding: utf-8 -*-
# p09 schema refine: non-crossing fan-in curves, arrow tip at circle edge, bottom air.
import io, re

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
MERGE = 1132

def curve(cx, hot=False):
    col = '#5E8FBF' if hot else '#4B4E55'
    w = '1.7' if hot else '1.3'
    c2x = cx + (MERGE - cx) * 0.55
    return ('<path d="M%.1f 42 C %.1f 72, %.1f 85, %d 85" fill="none" stroke="%s" stroke-width="%s"/>'
            % (cx, cx, c2x, MERGE, col, w))

NEW = ('<svg viewBox="0 -10 1300 160" style="width:100%;height:auto;display:block" class="conv">'
       + C1 + C2 + C3 + C4 + C5
       + curve(x1) + curve(x2) + curve(x3) + curve(x4) + curve(x5, True)
       + '<path d="M1144 85 l-11 -6 v12 z" fill="#5E8FBF"/>'
       + '<circle cx="1180" cy="85" r="36" fill="#25262D" stroke="#5E8FBF" stroke-width="2.2"/>'
       + '<text x="1180" y="81" text-anchor="middle" font-size="9.5" font-weight="700" letter-spacing="1.4" fill="#F2F1ED">THE</text>'
       + '<text x="1180" y="93" text-anchor="middle" font-size="9.5" font-weight="700" letter-spacing="1.4" fill="#F2F1ED">CUSTOMER</text>'
       + '<path d="M1206 60 C 1262 20, 1150 4, 700 4 L 118 4" fill="none" stroke="#B6B7BB" stroke-width="1.1" stroke-dasharray="3 4"/>'
       + '<path d="M110 4 l11 -5.5 v11 z" fill="#CFD0D4"/>'
       + '<text x="650" y="-3" text-anchor="middle" font-size="8" letter-spacing="1.6" fill="#CFD0D4">CUSTOMER INSIGHT &#8594; BUSINESS DECISIONS</text>'
       + '<text x="1180" y="140" text-anchor="middle" font-size="8" letter-spacing="1.4" fill="#CFD0D4">SHARED RESPONSIBILITY</text>'
       + '</svg>')

for f in ('casebook.html', 'site.html'):
    t = io.open(f, encoding='utf-8').read()
    t2, n = re.subn(r'<svg viewBox="0 -10 1300 160".*?</svg>', lambda m: NEW, t, flags=re.S)
    print(f, 'svg replaced:', n)
    assert n == 1
    io.open(f, 'w', encoding='utf-8', newline='').write(t2)

c = io.open('casebook.html', encoding='utf-8').read()
c = c.replace('.p09 .band{grid-template-columns:1fr;margin-top:auto;padding-top:12px;padding-bottom:2px}',
              '.p09 .band{grid-template-columns:1fr;margin-top:auto;padding-top:12px;padding-bottom:7px}', 1)
io.open('casebook.html', 'w', encoding='utf-8', newline='').write(c)

s = io.open('site.html', encoding='utf-8').read()
head = ('<!doctype html>\n<html lang="en">\n<head>\n<meta charset="utf-8">\n'
        '<meta name="viewport" content="width=device-width,initial-scale=1">\n'
        '<meta name="color-scheme" content="dark">\n</head>\n<body>\n')
io.open('site_standalone.html', 'w', encoding='utf-8', newline='').write(head + s + '\n</body>\n</html>')
print('done')
