# -*- coding: utf-8 -*-
# Corrections round, stage: page 5 (items 5,6,7,8,9,11-part1).
# PDF edits are scoped to the p05 slice so p06's twin strings stay for its own stage.
import io, re

LOG = []
def op(name, ok):
    LOG.append((' OK    ' if ok else ' SKIP  ') + name)

SUB_OLD = 'XTIX &middot; FINTECH SAAS &middot; EARLY-STAGE STARTUP'
SUB_NEW = 'XTIX &middot; B2B SAAS &middot; TECH &middot; E-TICKETS PLATFORM'
FH_OLD  = '<span><b>FIELD REPORT</b> &middot; BEFORE &middot; COMMERCIAL REALITY AT INTAKE</span><span>07 GAPS</span>'
FH_NEW  = '<span><b>STARTING POINT</b></span><span>07 GAPS</span>'
ISR_OLD = 'Israel first, then global.'
ISR_NEW = 'Domestic &amp; International.'
AFT_OLD = 'WHAT I BUILT &middot; AFTER'
AFT_NEW = 'WHAT I BUILT &middot; (AFTER)'

# ---------------- PDF ----------------
c = io.open('casebook.html', encoding='utf-8').read()
i = c.find('<!-- ================= PAGE 05')
j = c.find('<!-- ================= PAGE 06')
assert 0 < i < j, 'p05 slice not found'
p5 = c[i:j]

n0 = p5.count(SUB_OLD); p5 = p5.replace(SUB_OLD, SUB_NEW, 1); op('P5 subtitle', n0 >= 1)
n1 = p5.count(FH_OLD);  p5 = p5.replace(FH_OLD, FH_NEW, 1);  op('P5 starting point header', n1 == 1)
n2 = p5.count(ISR_OLD); p5 = p5.replace(ISR_OLD, ISR_NEW, 1); op('P5 domestic & international', n2 == 1)
n3 = p5.count(AFT_OLD); p5 = p5.replace(AFT_OLD, AFT_NEW, 1); op('P5 (AFTER)', n3 == 1)
meta_line = '<div class="meta">' + SUB_NEW + '</div>'
assert meta_line in p5
p5 = p5.replace(meta_line, meta_line + '\n  <div class="plabel">PART 1 OF 2 &mdash; THE BUILD</div>', 1)
op('P5 part label', True)

c = c[:i] + p5 + c[j:]
PDF_CSS = """
/* corrections p05 */
.p05 .plabel{margin-top:7px;font-family:'JetBrains Mono',monospace;font-weight:700;
  font-size:8.5px;letter-spacing:.24em;color:var(--emb)}
.p05 .then{font-size:13.5px;font-weight:600}
"""
k = c.rfind('</style>')
c = c[:k] + PDF_CSS + '\n' + c[k:]
io.open('casebook.html', 'w', encoding='utf-8', newline='').write(c)
LOG.append('== casebook written')

# ---------------- SITE ----------------
s = io.open('site.html', encoding='utf-8').read()
def rep1(txt, old, new, name):
    n = txt.count(old)
    op(name, n == 1)
    return txt.replace(old, new, 1) if n == 1 else txt

s = rep1(s, SUB_OLD, SUB_NEW, 'SITE subtitle')
s = rep1(s, FH_OLD, FH_NEW, 'SITE starting point header')
s = rep1(s, ISR_OLD, ISR_NEW, 'SITE domestic & international')
s = rep1(s, AFT_OLD, AFT_NEW, 'SITE (AFTER)')
smeta = '<div class="smeta rv" style="--i:2">' + SUB_NEW + '</div>'
assert smeta in s
s = s.replace(smeta, smeta + '\n    <div class="plabel rv" style="--i:2">PART 1 OF 2 &mdash; THE BUILD</div>', 1)
op('SITE part label', True)

SITE_CSS = """
/* corrections p05 (xtix part 1) */
#xtix .plabel{margin-top:10px;font-family:'JetBrains Mono',monospace;font-weight:700;
  font-size:9.5px;letter-spacing:.26em;color:var(--emb)}
#xtix .then{font-size:16px;font-weight:600}
"""
k = s.rfind('</style>')
s = s[:k] + SITE_CSS + '\n' + s[k:]
io.open('site.html', 'w', encoding='utf-8', newline='').write(s)
head = ('<!doctype html>\n<html lang="en">\n<head>\n<meta charset="utf-8">\n'
        '<meta name="viewport" content="width=device-width,initial-scale=1">\n'
        '<meta name="color-scheme" content="dark">\n</head>\n<body>\n')
io.open('site_standalone.html', 'w', encoding='utf-8', newline='').write(head + s + '\n</body>\n</html>')
LOG.append('== site written + standalone rebuilt')

# residue
cc = io.open('casebook.html', encoding='utf-8').read()
LOG.append('   casebook: FINTECH left=%d (p06 keeps its own) | STARTING POINT=%d | Israel=%d | (AFTER)=%d | PART 1=%d'
           % (cc.count('FINTECH SAAS'), cc.count('STARTING POINT'), cc.count('Israel first'),
              cc.count('(AFTER)'), cc.count('PART 1 OF 2')))
ss = io.open('site.html', encoding='utf-8').read()
LOG.append('   site: FINTECH left=%d | STARTING POINT=%d | Israel=%d | (AFTER)=%d | PART 1=%d'
           % (ss.count('FINTECH SAAS'), ss.count('STARTING POINT'), ss.count('Israel first'),
              ss.count('(AFTER)'), ss.count('PART 1 OF 2')))
print('\n'.join(x if isinstance(x, str) else x for x in LOG))
