# -*- coding: utf-8 -*-
# Corrections round, stage: page 6 / xtix evidence (items 5,11p2,12,13,14,15,16,17,18).
# PDF: edits scoped to the p06 slice. Site: edits scoped to the #xtix slice.
import io, re

LOG = []
def op(name, ok):
    LOG.append((' OK    ' if ok else ' **FAIL** ') + name)
    return ok

DASH3 = ('<div class="dash">Position for enterprise before scaling outbound.</div>'
         '<div class="dash">Build strategic partnerships from day one.</div>'
         '<div class="dash">Use AI as core infrastructure &mdash; not an add-on.</div>')
OLD5 = ('<div class="dash">Differentiate the product earlier against competitors</div>'
        '<div class="dash">Accelerate enterprise positioning</div>'
        '<div class="dash">Invest in strategic partnerships sooner</div>'
        '<div class="dash">Expand the AI platform even earlier</div>'
        '<div class="dash">Build the Israeli operation in parallel with global activity</div>')
SUB_OLD = 'XTIX &middot; FINTECH SAAS &middot; EARLY-STAGE STARTUP'
SUB_NEW = 'XTIX &middot; B2B SAAS &middot; TECH &middot; E-TICKETS PLATFORM'

# ================= PDF =================
c = io.open('casebook.html', encoding='utf-8').read()
i = c.find('<!-- ================= PAGE 06')
j = c.find('<!-- ================= PAGE 07')
assert 0 < i < j
p6 = c[i:j]

def rep(seg, old, new, name, n=1):
    cnt = seg.count(old)
    op('PDF ' + name, cnt == n)
    return seg.replace(old, new, n)

p6 = rep(p6, SUB_OLD, SUB_NEW, '5  subtitle')
meta_line = '<div class="meta">' + SUB_NEW + '</div>'
p6 = rep(p6, meta_line, meta_line + '\n  <div class="plabel">PART 2 OF 2 &mdash; THE EVIDENCE</div>', '11 part label')
p6 = rep(p6, '&euro;3M+ ARR', '$9M+ ARR', '12 $9M+ ARR')
p6 = rep(p6, '<tr><td class="k">QUALIFIED MEETINGS</td><td class="v">~6 per week</td></tr>',
             '<tr><td class="k">TOP-GROWTH MARKETS</td><td class="v vt">Prioritised Global expansion</td></tr>', '13 row A')
p6 = rep(p6, '<tr><td class="k">NEW OPPORTUNITIES</td><td class="v">~20 per week</td></tr>',
             '<tr><td class="k">AI SEGMENTATION</td><td class="v vt">Precision targeting model</td></tr>', '13 row B')
# 14 gauge polish: thinner track, bolder round arc, bigger %
p6 = rep(p6, 'stroke-width="3.4"', 'stroke-width="3"', '14 track x3', 3)
p6 = rep(p6, 'stroke-width="4" stroke-linecap="butt"', 'stroke-width="5" stroke-linecap="round"', '14 arc x3', 3)
p6 = rep(p6, 'y="40.5" text-anchor="middle" font-size="14"', 'y="41" text-anchor="middle" font-size="15"', '14 pct x3', 3)
p6 = rep(p6, OLD5, DASH3, '17 reflection 3 dashes')
p6b, n = re.subn(r'\s*<div data-moved class="lesson">\s*<div class="qx">Commercial growth.*?</div>\s*</div>', '', p6, flags=re.S)
op('PDF 18 closer removed', n == 1); p6 = p6b if n == 1 else p6

c = c[:i] + p6 + c[j:]
# extend the p05 plabel rule to p06
c2 = c.replace('.p05 .plabel{position:absolute', '.p05 .plabel,.p06 .plabel{position:absolute', 1)
op('PDF plabel css extended', c2 != c); c = c2
PDF_CSS = """
/* corrections p06 */
.p06 .tbl .vt{font-size:11px;font-weight:600;letter-spacing:.01em}
.p06 .inner>div:first-child{display:flex;flex-direction:column}
.p06 .gaug{margin:auto 0;padding-top:0;border-top:0}
.p06 .g1 svg{width:82px!important;height:82px!important}
.p06 .g1{width:118px}
.p06 .g1 .gl{font-size:9.5px;margin-top:8px}
.p06 .band{grid-template-columns:1fr;margin-top:12px;padding-top:12px}
.p06 .refl2{grid-template-columns:1fr 1fr 1fr;gap:0 22px}
.p06 .band .dash{font-size:10.8px;margin-bottom:0}
"""
k = c.rfind('</style>')
c = c[:k] + PDF_CSS + '\n' + c[k:]
io.open('casebook.html', 'w', encoding='utf-8', newline='').write(c)
LOG.append('== casebook written')

# ================= SITE =================
s = io.open('site.html', encoding='utf-8').read()
a = s.find('id="xtix"')
b = s.find('id="oasis"')
assert 0 < a < b
x = s[a:b]

def repx(seg, old, new, name, n=1):
    cnt = seg.count(old)
    op('SITE ' + name, cnt == n)
    return seg.replace(old, new, n)

x = repx(x, '<span class="cur">&euro;</span>', '<span class="cur">$</span>', '12 $ symbol')
x = repx(x, 'data-n="3" data-suf="M+"', 'data-n="9" data-suf="M+"', '12 counter 9M+')
x = repx(x, '<div class="rv" style="--i:2"><div class="bignum">~<span class="cnt" data-n="6">0</span></div><div class="biglbl">QUALIFIED MEETINGS / WEEK</div></div>',
            '<div class="rv" style="--i:2"><div class="bigtxt">Prioritised Global expansion</div><div class="biglbl">TOP-GROWTH MARKETS</div></div>', '13 cell 2')
x = repx(x, '<div class="rv" style="--i:3"><div class="bignum">~<span class="cnt" data-n="20">0</span></div><div class="biglbl">NEW OPPORTUNITIES / WEEK</div></div>',
            '<div class="rv" style="--i:3"><div class="bigtxt">Precision targeting model</div><div class="biglbl">AI SEGMENTATION</div></div>', '13 cell 3')
ZRA = '<div class="zr rv"><b>A</b><span class="d2"></span>EVIDENCE &mdash; FROM INFRASTRUCTURE TO EXECUTION</div>'
x = repx(x, ZRA, '<div class="plabel pl2 rv">PART 2 OF 2 &mdash; THE EVIDENCE</div>\n' + ZRA, '11 part label')
x = repx(x, 'stroke-width="4.2" style=', 'stroke-width="5" stroke-linecap="round" style=', '14 arc x3', 3)
x = repx(x, 'font-size="13.5" font-weight="700"', 'font-size="14.5" font-weight="700"', '14 pct x3', 3)
x = repx(x, '<div class="list">' + OLD5, '<div class="list refl3">' + DASH3, '17 reflection 3 dashes')
xb, n = re.subn(r'\s*<div class="lessq rv" style="--i:1">\s*<div class="qx">Commercial growth.*?</div>\s*</div>', '', x, flags=re.S)
op('SITE 18 closer removed', n == 1); x = xb if n == 1 else x
x = repx(x, '<div class="hairtop cols2">', '<div class="hairtop">', '17 D full width')

s = s[:a] + x + s[b:]
SITE_CSS = """
/* corrections p06 (xtix part 2) */
#xtix .pl2{margin:0 0 14px}
#xtix .bigtxt{font-weight:700;font-size:clamp(18px,1.9vw,24px);line-height:1.2;color:var(--ink);letter-spacing:-.01em}
#xtix .refl3{display:grid;grid-template-columns:repeat(3,1fr);gap:12px 30px}
@media (max-width:900px){#xtix .refl3{grid-template-columns:1fr}}
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
ss = io.open('site.html', encoding='utf-8').read()
LOG.append('   casebook: FINTECH=%d euro3M=%d QUALIFIED=%d Differentiate=%d growth-closer=%d PART2=%d 9M=%d' %
    (cc.count('FINTECH SAAS'), cc.count('&euro;3M+'), cc.count('QUALIFIED MEETINGS'),
     cc.count('Differentiate the product'), cc.count("Commercial growth doesn't begin"),
     cc.count('PART 2 OF 2'), cc.count('$9M+')))
LOG.append('   site:     FINTECH=%d euro-cur=%d QUALIFIED=%d Differentiate=%d growth-closer=%d PART2=%d data-n9=%d' %
    (ss.count('FINTECH SAAS'), ss.count('<span class="cur">&euro;</span>'), ss.count('QUALIFIED MEETINGS'),
     ss.count('Differentiate the product'), ss.count("Commercial growth doesn't begin"),
     ss.count('PART 2 OF 2'), ss.count('data-n="9"')))
print('\n'.join(LOG))
