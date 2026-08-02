# -*- coding: utf-8 -*-
# eventer tail: 06 learned full-width row, 07 convergence finale full-width sibling.
import io, re

s = io.open('site.html', encoding='utf-8').read()
a = s.find('id="eventer"')
b = s.find('id="medcoin"')
x = s[a:b]

pat = (r'<div class="hairtop cols2">\s*'
       r'(<div class="rv"><div class="zr"><b>06</b>.*?move organizations\.</div></div>)\s*'
       r'(<div class="hairtop"><div class="zr rv"><b>07</b>.*?</svg></div></div>)\s*'
       r'</div>')
xb, n = re.subn(pat, lambda m: '<div class="hairtop">\n' + m.group(1) + '\n</div>\n' + m.group(2), x, count=1, flags=re.S)
print('restructured:', n)
assert n == 1
s = s[:a] + xb + s[b:]
io.open('site.html', 'w', encoding='utf-8', newline='').write(s)
head = ('<!doctype html>\n<html lang="en">\n<head>\n<meta charset="utf-8">\n'
        '<meta name="viewport" content="width=device-width,initial-scale=1">\n'
        '<meta name="color-scheme" content="dark">\n</head>\n<body>\n')
io.open('site_standalone.html', 'w', encoding='utf-8', newline='').write(head + s + '\n</body>\n</html>')
seg = s[s.find('id="eventer"'):s.find('id="medcoin"')]
print('hairtop cols2 left in eventer:', seg.count('hairtop cols2'))
print('done')
