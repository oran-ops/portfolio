# -*- coding: utf-8 -*-
# Corrections round, stage: pages 1-4 (mapping items 1,2,3,4).
#   1 [BOTH]     ARCHIVE N° 2026-04  -> 2026-Present
#   2 [PDF-only] remove the p02 "FOR INTERNAL REVIEW" sig
#   3 [PDF-only] remove the p02 "MEMO 001" rub
#   4 [PDF-only] remove the p04 breadcrumb (crumb2)
import io, re

LOG = []
def op(name, fn, s):
    try:
        out = fn(s)
        if out is None or out == s:
            LOG.append(' SKIP  ' + name); return s
        LOG.append(' OK    ' + name); return out
    except Exception as e:
        LOG.append(' ERR   %s :: %s' % (name, str(e)[:100])); return s

def archive_no(s):
    old = '<span class="k">ARCHIVE N&deg;</span> 2026-04<br>'
    if old not in s: return None
    return s.replace(old, '<span class="k">ARCHIVE N&deg;</span> 2026-Present<br>', 1)

def memo001(s):
    s2, n = re.subn(r'\s*<div class="rub"><span class="d"></span>MEMO 001</div>', '', s)
    return s2 if n == 1 else None

def internal_review(s):
    s2, n = re.subn(r'\s*<div class="sig">FOR INTERNAL REVIEW</div>', '', s)
    return s2 if n == 1 else None

def breadcrumb(s):
    s2, n = re.subn(r'\s*<div class="crumb2">ARCHIVE://COMMERCIAL/2026 <b>&#8250;</b> ORAN_CARMON <b>&#8250;</b> CASE_FILES</div>', '', s)
    return s2 if n == 1 else None

# ---- PDF ----
c = io.open('casebook.html', encoding='utf-8').read()
LOG.append('== casebook.html')
c = op('1 archive number', archive_no, c)
c = op('3 MEMO 001 removed', memo001, c)
c = op('2 FOR INTERNAL REVIEW removed', internal_review, c)
c = op('4 breadcrumb removed', breadcrumb, c)
io.open('casebook.html', 'w', encoding='utf-8', newline='').write(c)

# ---- SITE (item 1 only) ----
s = io.open('site.html', encoding='utf-8').read()
LOG.append('== site.html')
s = op('1 archive number', archive_no, s)
io.open('site.html', 'w', encoding='utf-8', newline='').write(s)

head = ('<!doctype html>\n<html lang="en">\n<head>\n<meta charset="utf-8">\n'
        '<meta name="viewport" content="width=device-width,initial-scale=1">\n'
        '<meta name="color-scheme" content="dark">\n</head>\n<body>\n')
io.open('site_standalone.html', 'w', encoding='utf-8', newline='').write(head + s + '\n</body>\n</html>')
LOG.append('== standalone rebuilt')

# residue check
for name, txt in (('casebook', c), ('site', s)):
    LOG.append('   %s: 2026-04 left=%d | MEMO 001=%d | FOR INTERNAL REVIEW=%d | CASE_FILES=%d | 2026-Present=%d'
               % (name, txt.count('2026-04'), txt.count('MEMO 001'),
                  txt.count('FOR INTERNAL REVIEW'), txt.count('CASE_FILES'), txt.count('2026-Present')))
print('\n'.join(LOG))
