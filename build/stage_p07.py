# -*- coding: utf-8 -*-
# Corrections round, stage: page 7 / oasis part 1 (items 19, 20, 21, 11-oasis).
import io, re

LOG = []
def op(name, ok):
    LOG.append((' OK    ' if ok else ' **FAIL** ') + name)

SUB_OLD = 'OASIS &middot; CEO &middot; CONSTRUCTION &amp; SMART BUILDING SOLUTIONS'
SUB_NEW = 'OASIS &middot; CEO &middot; SMART SHADING TECHNOLOGIES'
MAN_OLD = "The mandate as CEO wasn't more revenue &mdash;"
MAN_NEW = "The mandate as CEO wasn't all about revenue &mdash;"

# ================= PDF =================
c = io.open('casebook.html', encoding='utf-8').read()
i = c.find('<!-- ================= PAGE 07')
j = c.find('<!-- ================= PAGE 08')
assert 0 < i < j
p7 = c[i:j]

n = p7.count(SUB_OLD); op('PDF 21 subtitle', n == 1)
p7 = p7.replace(SUB_OLD, SUB_NEW, 1)
meta_line = '<div class="meta">' + SUB_NEW + '</div>'
assert meta_line in p7
p7 = p7.replace(meta_line, meta_line + '\n  <div class="plabel">PART 1 OF 2 &mdash; THE MANDATE</div>', 1)
op('PDF 11 part label', True)
n = p7.count(MAN_OLD); op('PDF 19 mandate', n == 1)
p7 = p7.replace(MAN_OLD, MAN_NEW, 1)
p7b, n = re.subn(r'\s*<div data-moved class="insight">\s*<div class="qx">High-performing sales teams.*?</div>\s*</div>', '', p7, flags=re.S)
op('PDF 20 closer removed', n == 1); p7 = p7b if n == 1 else p7

c = c[:i] + p7 + c[j:]
c2 = c.replace('.p05 .plabel,.p06 .plabel{position:absolute', '.p05 .plabel,.p06 .plabel,.p07 .plabel{position:absolute', 1)
op('PDF plabel css extended to p07', c2 != c); c = c2
io.open('casebook.html', 'w', encoding='utf-8', newline='').write(c)
LOG.append('== casebook written')

# ================= SITE =================
s = io.open('site.html', encoding='utf-8').read()
a = s.find('id="oasis"')
b = s.find('id="eventer"')
assert 0 < a < b
x = s[a:b]

n = x.count(SUB_OLD); op('SITE 21 subtitle', n == 1)
x = x.replace(SUB_OLD, SUB_NEW, 1)
smeta = '<div class="smeta rv" style="--i:2">' + SUB_NEW + '</div>'
assert smeta in x
x = x.replace(smeta, smeta + '\n    <div class="plabel rv" style="--i:2">PART 1 OF 2 &mdash; THE MANDATE</div>', 1)
op('SITE 11 part label', True)
n = x.count(MAN_OLD); op('SITE 19 mandate', n == 1)
x = x.replace(MAN_OLD, MAN_NEW, 1)
xb, n = re.subn(r'\s*<div class="insight"><div class="qx">High-performing sales teams.*?</div>\s*</div>', '', x, flags=re.S)
op('SITE 20 closer removed', n == 1); x = xb if n == 1 else x

s = s[:a] + x + s[b:]
s2 = s.replace('#xtix .plabel{margin-top:10px', '#xtix .plabel,#oasis .plabel{margin-top:10px', 1)
op('SITE plabel css extended to oasis', s2 != s); s = s2
io.open('site.html', 'w', encoding='utf-8', newline='').write(s)
head = ('<!doctype html>\n<html lang="en">\n<head>\n<meta charset="utf-8">\n'
        '<meta name="viewport" content="width=device-width,initial-scale=1">\n'
        '<meta name="color-scheme" content="dark">\n</head>\n<body>\n')
io.open('site_standalone.html', 'w', encoding='utf-8', newline='').write(head + s + '\n</body>\n</html>')
LOG.append('== site written + standalone rebuilt')

cc = io.open('casebook.html', encoding='utf-8').read()
ss = io.open('site.html', encoding='utf-8').read()
LOG.append('   casebook: CONSTRUCTION=%d (p08 keeps 1) | more-revenue=%d | High-performing=%d | THE MANDATE=%d' %
    (cc.count('CONSTRUCTION'), cc.count("wasn't more revenue"), cc.count('High-performing'), cc.count('THE MANDATE')))
LOG.append('   site:     CONSTRUCTION=%d | more-revenue=%d | High-performing=%d | THE MANDATE=%d' %
    (ss.count('CONSTRUCTION'), ss.count("wasn't more revenue"), ss.count('High-performing'), ss.count('THE MANDATE')))
print('\n'.join(LOG))
