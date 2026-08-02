# -*- coding: utf-8 -*-
# p10 site pass (rerun after restore): move 03 right, drop WHY + closer, line-start fix.
import io, re

LOG = []
def op(name, ok):
    LOG.append((' OK    ' if ok else ' **FAIL** ') + name)
    return ok

s = io.open('site.html', encoding='utf-8').read()
a = s.find('id="medcoin"')
b = s.find('id="leadership"')
assert 0 < a < b
x = s[a:b]

m = re.search(r'<div class="z"[^>]*>\s*<div class="zr"><b>03</b>.*?experience</div></div></div>', x, re.S)
op('SITE 32 zone-03 located', bool(m))
assert m
z3 = m.group(0)
anchor = '<div class="zr rv"><b>04</b><span class="d2"></span>BUSINESS OUTCOMES</div>'
n = x.count(anchor)
op('SITE 32 zone-04 anchor', n == 1)
assert n == 1
x = x.replace(z3, '', 1)
x = x.replace(anchor, z3 + '\n          ' + anchor, 1)

x2, n = re.subn(r'\s*<div class="why st"[^>]*><span class="wl">WHY IT ENDED</span>.*?</div></div>', '', x, count=1, flags=re.S)
op('SITE 33 WHY removed', n == 1); x = x2 if n else x
x2, n = re.subn(r'\s*<div class="lessq rv"[^>]*>\s*<div class="qx">Founders don\'t manage functions.*?</div>\s*</div>', '', x, count=1, flags=re.S)
op('SITE 30 closer removed', n == 1); x = x2 if n else x
m2 = re.search(r'<line x1="(\d+)" y1="26" x2="\d+" y2="26" stroke="#F2F1ED"', x)
op('SITE 29 line found (x1=%s)' % (m2.group(1) if m2 else '?'), bool(m2))
if m2:
    x = x.replace(m2.group(0), m2.group(0).replace('x1="%s"' % m2.group(1), 'x1="44"'), 1)

s = s[:a] + x + s[b:]
io.open('site.html', 'w', encoding='utf-8', newline='').write(s)
head = ('<!doctype html>\n<html lang="en">\n<head>\n<meta charset="utf-8">\n'
        '<meta name="viewport" content="width=device-width,initial-scale=1">\n'
        '<meta name="color-scheme" content="dark">\n</head>\n<body>\n')
io.open('site_standalone.html', 'w', encoding='utf-8', newline='').write(head + s + '\n</body>\n</html>')

seg = s[s.find('id="medcoin"'):s.find('id="leadership"')]
LOG.append('   medcoin: WHAT WE BUILT=%d | WHY=%d | Turkey=%d | closer=%d | zr count=%d' %
    (seg.count('WHAT WE BUILT'), seg.count('WHY IT ENDED'), seg.count('Turkey'),
     seg.count("Founders don't manage"), len(re.findall(r'<div class="zr', seg))))
# order sanity: 03 must appear AFTER 02-zone close and BEFORE 04 in the right cell
i02 = seg.find('<b>02</b>'); i03 = seg.find('<b>03</b>'); i04 = seg.find('<b>04</b>')
LOG.append('   order: 02@%d < 03@%d < 04@%d -> %s' % (i02, i03, i04, 'OK' if i02 < i03 < i04 else 'FAIL'))
print('\n'.join(LOG))
