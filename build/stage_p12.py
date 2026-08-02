# -*- coding: utf-8 -*-
# Corrections round, stage: page 12 / tech (items 35, 36, 37, 38, 39, 40).
import io, re

LOG = []
def op(name, ok):
    LOG.append((' OK    ' if ok else ' **FAIL** ') + name)

LEAD_OLD = ("Technology should never replace commercial thinking &mdash; <b>it should amplify it</b>. "
            "I don't collect tools; I build systems. This is the commercial intelligence platform I designed &amp; implemented:")
LEAD_NEW = "Technology should amplify commercial thinking &mdash; not replace it. The platform I designed &amp; implemented:"
GPT3 = '<span><b>GPT</b></span><span><b>Claude</b></span><span><b>Gemini</b></span>'
LLM1 = '<span><b>LLMs</b></span>'
CAW  = '<span>Custom AI Workflows</span>'
ADD4 = '<span><b>Supabase</b></span><span><b>Twilio</b></span><span><b>Postman</b></span><span><b>Railway</b></span>'
INT3 = '<span>Lead Intelligence</span><span>Lead Enrichment</span><span>Competitive Intelligence</span>'

# ================= PDF =================
c = io.open('casebook.html', encoding='utf-8').read()
i = c.find('<!-- ================= PAGE 12')
j = c.find('<!-- ================= PAGE 13')
assert 0 < i < j
p = c[i:j]

n = p.count(LEAD_OLD); op('PDF 35 lead', n == 1)
p = p.replace(LEAD_OLD, LEAD_NEW, 1)
n = p.count('<path d="M186.0 56 l-4.5 8.5 h9 z" fill="#B6B7BB"/>'); op('PDF 36 arrowhead', n == 1)
p = p.replace('<path d="M186.0 56 l-4.5 8.5 h9 z" fill="#B6B7BB"/>', '', 1)
n = p.count('<text x="482.0" y="104"'); op('PDF 37 label anchor', n == 1)
p = p.replace('<text x="482.0" y="104"', '<text x="482.0" y="72"', 1)
n = p.count('viewBox="0 0 808 114"'); op('PDF 37 viewbox', n == 1)
p = p.replace('viewBox="0 0 808 114"', 'viewBox="0 0 808 92"', 1)
n = p.count(GPT3); op('PDF 38 LLMs', n == 1)
p = p.replace(GPT3, LLM1, 1)
n = p.count(CAW); op('PDF 38 add-4 anchor', n == 1)
p = p.replace(CAW, CAW + ADD4, 1)
n = p.count(INT3); op('PDF 38 intel trio removed', n == 1)
p = p.replace(INT3, '', 1)
p2, n = re.subn(r'\s*<div data-moved class="quote2">\s*<div class="qx">AI doesn\'t replace commercial leaders.*?</div>\s*</div>', '', p, count=1, flags=re.S)
op('PDF 39 closer removed', n == 1); p = p2 if n else p

c = c[:i] + p + c[j:]
PDF_CSS = """
/* corrections p12 — lead + rhythm */
.p12b .lead{font-family:inherit;font-style:normal;font-weight:700;font-size:13px;
  letter-spacing:.01em;color:var(--ink)}
.p12b .folder{display:flex;flex-direction:column}
.p12b .archw{margin-top:auto}
.p12b .bot2{margin-top:auto;padding-bottom:6px}
"""
k = c.rfind('</style>')
c = c[:k] + PDF_CSS + '\n' + c[k:]
io.open('casebook.html', 'w', encoding='utf-8', newline='').write(c)
LOG.append('== casebook written')

# ================= SITE =================
s = io.open('site.html', encoding='utf-8').read()
a = s.find('id="tech"')
b = s.find('id="final"')
assert 0 < a < b
x = s[a:b]

n = x.count(LEAD_OLD); op('SITE 35 lead', n == 1)
x = x.replace(LEAD_OLD, LEAD_NEW, 1)
n = x.count('<path d="M200.0 60 l-4.5 9 h9 z" fill="#B6B7BB"/>'); op('SITE 36 arrowhead', n == 1)
x = x.replace('<path d="M200.0 60 l-4.5 9 h9 z" fill="#B6B7BB"/>', '', 1)
n = x.count('<text x="519.5" y="114"'); op('SITE 37 label anchor', n == 1)
x = x.replace('<text x="519.5" y="114"', '<text x="519.5" y="80"', 1)
n = x.count('viewBox="0 0 872 124"'); op('SITE 37 viewbox', n == 1)
x = x.replace('viewBox="0 0 872 124"', 'viewBox="0 0 872 100"', 1)
n = x.count(GPT3); op('SITE 38 LLMs', n == 1)
x = x.replace(GPT3, LLM1, 1)
n = x.count(CAW); op('SITE 38 add-4 anchor', n == 1)
x = x.replace(CAW, CAW + ADD4, 1)
n = x.count(INT3); op('SITE 38 intel trio removed', n == 1)
x = x.replace(INT3, '', 1)
x2, n = re.subn(r'\s*<div class="lessq"><div class="qx">AI doesn\'t replace commercial leaders.*?</div></div>', '', x, count=1, flags=re.S)
op('SITE 39 closer removed', n == 1); x = x2 if n else x

s = s[:a] + x + s[b:]
SITE_CSS = """
/* corrections p12 (tech) — lead */
#tech .lead{font-family:inherit;font-style:normal;font-weight:700;
  font-size:clamp(14px,1.8vw,17px);letter-spacing:.01em;color:var(--ink)}
"""
k = s.rfind('</style>')
s = s[:k] + SITE_CSS + '\n' + s[k:]
io.open('site.html', 'w', encoding='utf-8', newline='').write(s)
head = ('<!doctype html>\n<html lang="en">\n<head>\n<meta charset="utf-8">\n'
        '<meta name="viewport" content="width=device-width,initial-scale=1">\n'
        '<meta name="color-scheme" content="dark">\n</head>\n<body>\n')
io.open('site_standalone.html', 'w', encoding='utf-8', newline='').write(head + s + '\n</body>\n</html>')
LOG.append('== site written + standalone rebuilt')

for name, t in (('casebook', c), ('site', s)):
    LOG.append('   %s: never-replace=%d GPT=%d Gemini=%d LLMs=%d Supabase=%d LeadIntel=%d AI-closer=%d intb-kept=%d' %
        (name, t.count('should never replace'), t.count('<b>GPT</b>'), t.count('Gemini'),
         t.count('<b>LLMs</b>'), t.count('Supabase'), t.count('Lead Intelligence'),
         t.count("AI doesn't replace commercial leaders"), t.count('AI BUILT FOR INTERNAL')))
print('\n'.join(LOG))
