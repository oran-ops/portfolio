# -*- coding: utf-8 -*-
import io, re
p="casebook.html"; s=io.open(p,encoding="utf-8").read()

# ---- 1. remove OLD p04 CSS block (marker -> </style>) ----
MK="/* ============ PAGE 04 - THE CASE FILES (DIVIDER) ============ */"
before, rest = s.split(MK, 1)
_junk, after_style = rest.split("</style>", 1)
s = before.rstrip()+"\n</style>"+after_style

# ---- 2. remove OLD p04 <section> ----
s = re.sub(r'\n<!--[^\n]*PAGE 04[^\n]*-->\n<section class="page p04">.*?</section>\n',
           '\n', s, flags=re.S)

# ---- 3. new p04 CSS (faithful port of the case-files hero) ----
css="""
/* ============ PAGE 04 - THE CASE FILES (DIVIDER) ============ */
.p04 .title{position:absolute;top:58px;left:72px;font-weight:800;font-size:54px;line-height:1;letter-spacing:-.03em;text-transform:uppercase;color:var(--ink)}
.p04 .meta{position:absolute;top:76px;right:74px;font-family:'JetBrains Mono',monospace;font-size:10px;letter-spacing:.2em;color:var(--mut)}
.p04 .stack{position:absolute;top:214px;left:72px;right:72px}
.p04 .tab{position:relative}
.p04 .lip{height:34px;border-radius:9px 22px 0 0;display:flex;align-items:center;padding:0 18px;position:relative;top:1px;z-index:2}
.p04 .lip .nm{font-family:'Fraunces',serif;font-weight:500;font-size:17px;color:#0C0D10}
.p04 .lip .meta2{margin-left:auto;font-family:'JetBrains Mono',monospace;font-weight:600;font-size:9px;letter-spacing:.16em;color:rgba(12,13,16,.6)}
.p04 .body{position:relative;height:54px}
.p04 .cat{position:absolute;right:26px;top:50%;transform:translateY(-50%);font-family:'JetBrains Mono',monospace;font-weight:700;font-size:9.5px;letter-spacing:.16em;color:rgba(12,13,16,.72)}
.p04 .tab.open .body{height:102px;border-radius:0 14px 14px 14px;padding:16px 22px}
.p04 .tab.open .cat{top:18px;transform:none}
.p04 .dossier{font-family:'JetBrains Mono',monospace;font-size:12.5px;line-height:1.8;color:rgba(12,13,16,.85)}
"""
s=s.replace("</style>",css+"</style>",1)

# ---- 4. new p04 section ----
def closed(color,name,fno,cat,width,off,last=False):
    br = "0 12px 12px 12px" if last else "0 12px 0 0"
    return ('    <div class="tab"><div class="lip" style="background:%s;width:%dpx;margin-left:%dpx">'
            '<span class="nm">%s</span><span class="meta2">%s</span></div>'
            '<div class="body" style="background:%s;border-radius:%s"><div class="cat">%s</div></div></div>\n'
            )%(color,width,off,name,fno,color,br,cat)

xtix=('    <div class="tab open"><div class="lip" style="background:var(--emb);width:250px;margin-left:0px">'
      '<span class="nm">XTIX</span><span class="meta2">FILE 01</span></div>'
      '<div class="body" style="background:var(--emb)"><div class="cat">BUILT FROM ZERO &#8250;</div>'
      '<div class="dossier">&gt; commercial function: none &rarr; operating system<br>'
      '&gt; pipeline: &euro;0 &rarr; &euro;3M+ ARR &middot; 7 enterprise closed</div></div></div>\n')

stack=(xtix+
 closed("var(--brass)","Oasis","FILE 02","LEADERSHIP &#8250;",300,46)+
 closed("var(--ice)","Eventer","FILE 03","ALIGNMENT &#8250;",350,92)+
 closed("var(--ink)","Medcoin","FILE 04","FOUNDER &#8250;",400,138,last=True))

page="""
<!-- ================= PAGE 04 . THE CASE FILES ================= -->
<section class="page p04">
  <span class="brk tl"></span><span class="brk tr"></span><span class="brk bl"></span><span class="brk br"></span>
  <div class="title">THE CASE<br>FILES</div>
  <div class="meta">EXECUTIVE CASEBOOK &middot; 04 DOSSIERS &middot; 2018&ndash;2026</div>
  <div class="stack">
"""+stack+"""  </div>
  <div class="ftr">
    <span>THE COMMERCIAL BUILDER</span>
    <span class="mid"><span class="d"></span>THE CASE FILES</span>
    <span><b>P.04</b> &mdash; 13</span>
  </div>
</section>
"""
s=s.replace("</body></html>",page+"\n</body></html>")
io.open(p,"w",encoding="utf-8").write(s)
print("page 4 rebuilt (faithful port)")
