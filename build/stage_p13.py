# -*- coding: utf-8 -*-
# Corrections round, final stage: page 13 (items 41, 42).
import io

LOG = []
def op(name, ok):
    LOG.append((' OK    ' if ok else ' **FAIL** ') + name)

SEAL_OLD = 'building commercial organizations <b>from zero</b>. '
SEAL_NEW = 'building commercial organizations. '
VB4 = '<span class="vb tl"></span><span class="vb tr"></span><span class="vb bl"></span><span class="vb br"></span>'
PDF_CSS_LINES = [
    '.p13 .vseal .vb{position:absolute;width:11px;height:11px;border:1.5px solid var(--emb)}',
    '.p13 .vseal .vb.tl{top:7px;left:7px;border-right:0;border-bottom:0}',
    '.p13 .vseal .vb.tr{top:7px;right:7px;border-left:0;border-bottom:0}',
    '.p13 .vseal .vb.bl{bottom:7px;left:7px;border-right:0;border-top:0}',
    '.p13 .vseal .vb.br{bottom:7px;right:7px;border-left:0;border-top:0}',
]
SITE_CSS_LINES = [
    '#final .vseal .vb{position:absolute;width:15px;height:15px;border:2px solid var(--emb)}',
    '#final .vseal .vb.tl{top:11px;left:11px;border-right:0;border-bottom:0}',
    '#final .vseal .vb.tr{top:11px;right:11px;border-left:0;border-bottom:0}',
    '#final .vseal .vb.bl{bottom:11px;left:11px;border-right:0;border-top:0}',
    '#final .vseal .vb.br{bottom:11px;right:11px;border-left:0;border-top:0}',
    '#final .vseal .vb{width:11px;height:11px}',
]

# ---- PDF ----
c = io.open('casebook.html', encoding='utf-8').read()
n = c.count(SEAL_OLD); op('PDF 41 seal sentence (n=%d)' % n, n == 1)
c = c.replace(SEAL_OLD, SEAL_NEW, 1)
n = c.count(VB4); op('PDF 42 corner spans (n=%d)' % n, n == 1)
c = c.replace(VB4, '', 1)
removed = 0
for line in PDF_CSS_LINES:
    removed += c.count(line)
    c = c.replace(line + '\n', '').replace(line, '')
op('PDF 42 corner css removed (%d lines)' % removed, removed >= 5)
io.open('casebook.html', 'w', encoding='utf-8', newline='').write(c)

# ---- SITE ----
s = io.open('site.html', encoding='utf-8').read()
n = s.count(SEAL_OLD); op('SITE 41 seal sentence (n=%d)' % n, n == 1)
s = s.replace(SEAL_OLD, SEAL_NEW, 1)
n = s.count(VB4); op('SITE 42 corner spans (n=%d)' % n, n == 1)
s = s.replace(VB4, '', 1)
removed = 0
for line in SITE_CSS_LINES:
    removed += s.count(line)
    s = s.replace(line + '\n', '').replace(line, '')
op('SITE 42 corner css removed (%d lines)' % removed, removed >= 6)
io.open('site.html', 'w', encoding='utf-8', newline='').write(s)
head = ('<!doctype html>\n<html lang="en">\n<head>\n<meta charset="utf-8">\n'
        '<meta name="viewport" content="width=device-width,initial-scale=1">\n'
        '<meta name="color-scheme" content="dark">\n</head>\n<body>\n')
io.open('site_standalone.html', 'w', encoding='utf-8', newline='').write(head + s + '\n</body>\n</html>')

for name, t in (('casebook', c), ('site', s)):
    LOG.append('   %s: seal-from-zero=%d | xtix-from-zero-kept=%d | vb-left=%d' %
        (name, t.count('organizations <b>from zero</b>'),
         t.count('commercial function from zero'), t.count('class="vb')))
print('\n'.join(LOG))
