# -*- coding: utf-8 -*-
# Fine-tuning round — SITE
import io, re
p="site.html"; s=io.open(p,encoding="utf-8").read()

# 1. name
s=s.replace("THE COMMERCIAL<br>BUILDER","THE COMMERCIAL<br>SYSTEMS BUILDER")
s=s.replace("THE COMMERCIAL BUILDER","THE COMMERCIAL SYSTEMS BUILDER")
s=s.replace("<title>Oran Carmon &mdash; The Commercial Builder</title>",
            "<title>Oran Carmon &mdash; The Commercial Systems Builder</title>")
s=s.replace("COMMERCIAL BUILDER","COMMERCIAL SYSTEMS BUILDER")

# 2. LOG restore
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
print("site LOG restored on",before,"rows")

# 3. mission objective
s=s.replace(">MY MISSION<",">MISSION OBJECTIVE<")

# 4. COS-built under the big counter
s=s.replace('<div class="biglbl">PIPELINE MANAGED</div>',
'<div class="biglbl">PIPELINE MANAGED</div><div class="biglbl" style="color:var(--emb);margin-top:5px">COMMERCIAL OPERATING SYSTEM &mdash; BUILT</div>',1)

# 5. internal-AI chip (tech)
s=s.replace('This is the commercial intelligence platform I designed &amp; implemented:</div>',
'This is the commercial intelligence platform I designed &amp; implemented:</div>\n    <div class="intb rv" style="--i:3">AI BUILT FOR INTERNAL COMMERCIAL OPERATIONS &mdash; NOT A SELLABLE PRODUCT</div>',1)

# 6. key business outcome slip
s=s.replace('<div class="slip">EVIDENCE &middot; KEY DEAL</div>','<div class="slip">KEY BUSINESS OUTCOME</div>',1)

# 7. About Me on final
a="</div>\n        </div>\n        <div>\n          <div class=\"zr\"><b>B</b><span class=\"d2\"></span>INDUSTRIES"
assert a in s, "site final anchor"
about=("</div>\n          <div class=\"zr\" style=\"margin-top:30px\"><b>AM</b><span class=\"d2\"></span>ABOUT ME</div>"
"\n          <div class=\"abt st\" style=\"--i:1\">I enjoy building commercial organizations <b>from zero</b>.<br>"
"I believe <b>systems scale better than heroes</b>.<br>"
"My goal is to leave every company <b>stronger than I found it</b>.</div>"
"\n        </div>\n        <div>\n          <div class=\"zr\"><b>B</b><span class=\"d2\"></span>INDUSTRIES")
s=s.replace(a,about,1)

# CSS
css="""
.intb{display:inline-flex;margin-top:16px;border:1px solid rgba(244,96,62,.45);border-radius:8px;padding:8px 15px;
font-family:'JetBrains Mono',monospace;font-weight:600;font-size:9px;letter-spacing:.18em;color:var(--emb)}
#final .abt{font-family:'Fraunces',serif;font-style:italic;font-size:16px;line-height:1.8;color:var(--mut)}
#final .abt b{color:var(--ink);font-weight:500}
"""
s=s.replace("</style>",css+"</style>",1)

io.open(p,"w",encoding="utf-8").write(s)
print("fine-tuning applied to site:",len(s),"bytes")
