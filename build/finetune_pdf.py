# -*- coding: utf-8 -*-
# Fine-tuning round — PDF
import io, re
p="casebook.html"; s=io.open(p,encoding="utf-8").read()

# ---------- 1. THE COMMERCIAL SYSTEMS BUILDER ----------
s=s.replace("THE COMMERCIAL<br>BUILDER","THE COMMERCIAL<br>SYSTEMS BUILDER")
s=s.replace("THE COMMERCIAL BUILDER","THE COMMERCIAL SYSTEMS BUILDER")
s=s.replace(">COMMERCIAL BUILDER<",">COMMERCIAL SYSTEMS BUILDER<")
s=s.replace("<title>The Commercial Builder - Executive Portfolio</title>",
            "<title>The Commercial Systems Builder &mdash; Executive Portfolio</title>")

# ---------- 2. restore LOG.NN (user loves the intelligence feel) ----------
def restore_log(txt):
    out=[]; last=0; counter=0
    pat=re.compile(r'<div class="zr"|<div class="lg"><span class="c">')
    for m in pat.finditer(txt):
        out.append(txt[last:m.start()])
        tok=m.group(0)
        if tok.startswith('<div class="zr"'):
            counter=0; out.append(tok)
        else:
            counter+=1
            out.append('<div class="lg"><span class="n">LOG.%02d</span><span class="c">'%counter)
        last=m.end()
    out.append(txt[last:])
    return ''.join(out)
before=s.count('<div class="lg"><span class="c">')
s=restore_log(s)
print("LOG restored on",before,"rows")

# ---------- 3. MY MISSION -> MISSION OBJECTIVE ----------
s=s.replace(">MY MISSION<",">MISSION OBJECTIVE<")

# ---------- 4. COS-built under the performance numbers (P.06) ----------
s=s.replace('</table>\n        <div class="gaug">',
'</table>\n        <div class="cosb"><span class="sq2"></span>COMMERCIAL OPERATING SYSTEM &mdash; BUILT</div>\n        <div class="gaug">',1)

# ---------- 5. internal-AI box (P.12) ----------
s=s.replace('This is the commercial intelligence platform I designed &amp; implemented:</div>',
'This is the commercial intelligence platform I designed &amp; implemented:</div>\n    <div class="intb">AI BUILT FOR INTERNAL COMMERCIAL OPERATIONS &mdash; NOT A SELLABLE PRODUCT</div>',1)

# ---------- 6. Oasis evidence: KEY BUSINESS OUTCOME ----------
s=s.replace('<span class="d2"></span>BUSINESS PERFORMANCE</div>','<span class="d2"></span>KEY BUSINESS OUTCOME</div>',1)
s=s.replace('<div class="slip">EVIDENCE &middot; KEY DEAL</div>','<div class="slip">KEY BUSINESS OUTCOME</div>',1)

# ---------- 7. About Me (P.13, left col under principles) ----------
a='</div>\n      </div>\n      <div>\n        <div class="zr"><b>B</b><span class="d2"></span>INDUSTRIES'
assert a in s, "p13 anchor"
about=('</div>\n        <div class="zr" style="margin-top:20px"><b>AM</b><span class="d2"></span>ABOUT ME</div>'
'\n        <div class="abt">I enjoy building commercial organizations <b>from zero</b>.<br>'
'I believe <b>systems scale better than heroes</b>.<br>'
'My goal is to leave every company <b>stronger than I found it</b>.</div>'
'\n      </div>\n      <div>\n        <div class="zr"><b>B</b><span class="d2"></span>INDUSTRIES')
s=s.replace(a,about,1)

# ---------- CSS ----------
css="""
.p06 .cosb{display:flex;align-items:center;gap:8px;margin-top:9px;font-family:'JetBrains Mono',monospace;font-weight:700;font-size:8px;letter-spacing:.22em;color:var(--emb)}
.p06 .cosb .sq2{width:6px;height:6px;background:var(--emb)}
.p12b .intb{display:inline-flex;margin-top:10px;border:1px solid rgba(244,96,62,.45);border-radius:7px;padding:6px 13px;
font-family:'JetBrains Mono',monospace;font-weight:600;font-size:8.5px;letter-spacing:.18em;color:var(--emb)}
.p13 .abt{font-family:'Fraunces',serif;font-style:italic;font-size:13px;line-height:1.7;color:var(--mut)}
.p13 .abt b{color:var(--ink);font-weight:500}
.p13 .pgrid{gap:20px 28px}
.p06 .gaug{margin-top:7px;padding-top:7px}
"""
s=s.replace("</style>",css+"</style>",1)

io.open(p,"w",encoding="utf-8").write(s)
print("fine-tuning applied to PDF")
