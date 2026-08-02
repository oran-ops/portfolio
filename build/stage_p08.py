# -*- coding: utf-8 -*-
# Corrections round, stage: page 8 / oasis part 2 (items 22, 23, 24, 11-oasis-p2).
import io, re

LOG = []
def op(name, ok):
    LOG.append((' OK    ' if ok else ' **FAIL** ') + name)

SUB_OLD = 'OASIS &middot; CEO &middot; CONSTRUCTION &amp; SMART BUILDING SOLUTIONS'
SUB_NEW = 'OASIS &middot; CEO &middot; SMART SHADING TECHNOLOGIES'

# ================= PDF =================
c = io.open('casebook.html', encoding='utf-8').read()
i = c.find('<!-- ================= PAGE 08')
j = c.find('<!-- ================= PAGE 09')
assert 0 < i < j
p8 = c[i:j]

n = p8.count(SUB_OLD); op('PDF 22 subtitle', n == 1)
p8 = p8.replace(SUB_OLD, SUB_NEW, 1)
meta_line = '<div class="meta">' + SUB_NEW + '</div>'
assert meta_line in p8
p8 = p8.replace(meta_line, meta_line + '\n  <div class="plabel">PART 2 OF 2 &mdash; THE EVIDENCE</div>', 1)
op('PDF 11 part label', True)
n = p8.count('<div class="perf"></div>'); op('PDF 23 dead perf removed', n == 1)
p8 = p8.replace('<div class="perf"></div>', '', 1)
p8b, n = re.subn(r'\s*<div data-moved class="lesson">\s*<div class="qx">Organizations don\'t scale.*?</div>\s*</div>', '', p8, flags=re.S)
op('PDF 24 closer removed', n == 1); p8 = p8b if n == 1 else p8

c = c[:i] + p8 + c[j:]
c2 = c.replace('.p05 .plabel,.p06 .plabel,.p07 .plabel{position:absolute',
               '.p05 .plabel,.p06 .plabel,.p07 .plabel,.p08 .plabel{position:absolute', 1)
op('PDF plabel css extended to p08', c2 != c); c = c2
PDF_CSS = """
/* corrections p08 — rhythm */
.p08 .inner>div:first-child{display:flex;flex-direction:column}
.p08 .stat{margin-top:auto;margin-bottom:auto}
.p08 .band{grid-template-columns:1fr;margin-top:16px;padding-top:16px}
"""
k = c.rfind('</style>')
c = c[:k] + PDF_CSS + '\n' + c[k:]
io.open('casebook.html', 'w', encoding='utf-8', newline='').write(c)
LOG.append('== casebook written')

# ================= SITE =================
s = io.open('site.html', encoding='utf-8').read()
a = s.find('id="oasis"')
b = s.find('id="eventer"')
assert 0 < a < b
x = s[a:b]

ZRA = '<div class="zr rv"><b>A</b><span class="d2"></span>EVIDENCE &mdash; COMMERCIAL RESULTS</div>'
n = x.count(ZRA); op('SITE 11 anchor', n == 1)
x = x.replace(ZRA, '<div class="plabel pl2 rv">PART 2 OF 2 &mdash; THE EVIDENCE</div>\n' + ZRA, 1)
xb, n = re.subn(r'\s*<div class="lessq rv"[^>]*>\s*<div class="qx">Organizations don\'t scale.*?</div>\s*</div>', '', x, flags=re.S)
op('SITE 24 closer removed', n == 1); x = xb if n == 1 else x

s = s[:a] + x + s[b:]
s2 = s.replace('#xtix .pl2{margin:0 0 14px}', '#xtix .pl2,#oasis .pl2{margin:0 0 14px}', 1)
op('SITE pl2 css extended', s2 != s); s = s2
io.open('site.html', 'w', encoding='utf-8', newline='').write(s)
head = ('<!doctype html>\n<html lang="en">\n<head>\n<meta charset="utf-8">\n'
        '<meta name="viewport" content="width=device-width,initial-scale=1">\n'
        '<meta name="color-scheme" content="dark">\n</head>\n<body>\n')
io.open('site_standalone.html', 'w', encoding='utf-8', newline='').write(head + s + '\n</body>\n</html>')
LOG.append('== site written + standalone rebuilt')

cc = io.open('casebook.html', encoding='utf-8').read()
ss = io.open('site.html', encoding='utf-8').read()
LOG.append('   casebook: CONSTRUCTION=%d | Organizations-dont-scale=%d | THE EVIDENCE labels=%d | perf=%d' %
    (cc.count('CONSTRUCTION'), cc.count("Organizations don't scale"), cc.count('PART 2 OF 2 &mdash; THE EVIDENCE'), cc.count('class="perf"')))
LOG.append('   site:     CONSTRUCTION=%d | Organizations-dont-scale=%d | THE EVIDENCE labels=%d' %
    (ss.count('CONSTRUCTION'), ss.count("Organizations don't scale"), ss.count('PART 2 OF 2 &mdash; THE EVIDENCE')))
print('\n'.join(LOG))
