# -*- coding: utf-8 -*-
import io
p="casebook.html"; s=io.open(p,encoding="utf-8").read()

css="""
/* ============ PAGE 04 - THE CASE FILES (DIVIDER) ============ */
.p04 .hd{position:absolute;top:50px;left:72px;right:72px;display:flex;justify-content:space-between;align-items:center;z-index:5}
.p04 .rub{display:flex;align-items:center;gap:11px;font-family:'JetBrains Mono',monospace;font-weight:700;font-size:10.5px;letter-spacing:.26em;color:var(--ink)}
.p04 .rub .d{width:7px;height:7px;background:var(--emb);transform:rotate(45deg)}
.p04 .tok{display:inline-flex;align-items:center;gap:8px;font-family:'JetBrains Mono',monospace;font-weight:600;font-size:9.5px;letter-spacing:.16em;
border:1px solid var(--grid);border-radius:7px;padding:6px 12px;color:var(--emb)}
.p04 .title{position:absolute;top:90px;left:72px;font-weight:800;font-size:46px;letter-spacing:-.035em;line-height:1;color:var(--ink)}
.p04 .metaL{position:absolute;top:150px;left:74px;font-family:'JetBrains Mono',monospace;font-size:9.5px;letter-spacing:.24em;color:var(--mut)}
.p04 .rail{position:absolute;top:150px;right:74px;display:flex;align-items:center;gap:10px;font-family:'JetBrains Mono',monospace;font-size:9px;letter-spacing:.2em;color:var(--dim)}
.p04 .rail .ln{width:60px;height:1px;background:repeating-linear-gradient(90deg,var(--grid2) 0 5px,transparent 5px 11px)}

.p04 .drawer{position:absolute;top:198px;left:72px;right:72px}
.p04 .file{margin-bottom:12px}
.p04 .lip{display:inline-flex;align-items:center;gap:13px;height:30px;border-radius:9px 20px 0 0;padding:0 18px;position:relative;top:1px;z-index:2}
.p04 .lip .nm{font-family:'Fraunces',serif;font-weight:500;font-size:16px;color:#0C0D10}
.p04 .lip .fl{font-family:'JetBrains Mono',monospace;font-weight:600;font-size:8.5px;letter-spacing:.18em;color:rgba(12,13,16,.6)}
.p04 .body{position:relative;height:66px;border-radius:0 14px 14px 14px;padding:0 24px;display:flex;align-items:center}
.p04 .body .ttl{font-weight:600;font-size:19px;letter-spacing:-.012em;color:#0C0D10}
.p04 .body .rt{margin-left:auto;display:flex;align-items:center;gap:18px}
.p04 .body .cat{font-family:'JetBrains Mono',monospace;font-weight:700;font-size:9.5px;letter-spacing:.18em;color:rgba(12,13,16,.72)}
.p04 .body .go{display:flex;align-items:center;gap:9px;font-family:'JetBrains Mono',monospace;font-weight:600;font-size:9.5px;letter-spacing:.14em;
color:rgba(12,13,16,.66);border-left:1px solid rgba(12,13,16,.22);padding-left:17px}
.p04 .body .go b{font-size:13px;line-height:1;color:rgba(12,13,16,.85)}
"""
s=s.replace("</style>",css+"</style>",1)

def f(color,name,fl,title,cat,pg,off,dark=False):
    ink="rgba(255,255,255,.9)" if dark else None
    return ('    <div class="file">'
            '<div class="lip" style="background:%s;margin-left:%dpx"><span class="nm">%s</span><span class="fl">%s</span></div>'
            '<div class="body" style="background:%s">'
            '<div class="ttl">%s</div>'
            '<div class="rt"><span class="cat">%s</span>'
            '<span class="go">%s <b>&#8250;</b></span></div>'
            '</div></div>\n')%(color,off,name,fl,color,title,cat,pg)

files=(
 f("var(--emb)","XTIX","FILE 01","Building a Commercial Function From Zero","BUILT FROM ZERO","P.05",0)+
 f("var(--brass)","Oasis","FILE 02","Building Leaders, Not Just Sales Teams","LEADERSHIP","P.07",40)+
 f("var(--ice)","Eventer","FILE 03","Aligning Commercial Execution Across Teams","ALIGNMENT","P.09",80)+
 f("var(--ink)","Medcoin","FILE 04","Building a Business From Vision","FOUNDER","P.10",120)
)

page="""
<!-- ================= PAGE 04 . THE CASE FILES ================= -->
<section class="page p04">
  <span class="brk tl"></span><span class="brk tr"></span><span class="brk bl"></span><span class="brk br"></span>
  <div class="hd">
    <div class="rub"><span class="d"></span>THE ARCHIVE</div>
    <div class="tok">OPEN FILE 01 &#8250;</div>
  </div>
  <div class="title">The Case Files</div>
  <div class="metaL">FOUR COMMERCIAL BUILDS &middot; ONE OPERATING SYSTEM</div>
  <div class="rail"><span>DRAWER A</span><span class="ln"></span><span>04 DOSSIERS</span></div>
  <div class="drawer">
"""+files+"""  </div>
  <div class="ftr">
    <span>THE COMMERCIAL BUILDER</span>
    <span class="mid"><span class="d"></span>THE CASE FILES</span>
    <span><b>P.04</b> &mdash; 13</span>
  </div>
</section>
"""
s=s.replace("</body></html>",page+"\n</body></html>")
io.open(p,"w",encoding="utf-8").write(s)
print("page 4 added")
