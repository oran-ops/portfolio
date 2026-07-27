# -*- coding: utf-8 -*-
import io
p="casebook.html"; s=io.open(p,encoding="utf-8").read()

css="""
/* ============ PAGE 13 - FINAL THOUGHTS + CONTACT ============ */
.p13 .folder{padding:26px 30px 20px}
.p13 .inner{display:grid;grid-template-columns:62fr 38fr;column-gap:34px;position:relative;height:100%}
.p13 .inner::before{content:"";position:absolute;left:60.4%;top:2px;bottom:2px;width:1px;background:repeating-linear-gradient(180deg,var(--grid) 0 5px,transparent 5px 11px)}
.p13 .zr{margin-bottom:14px}
.p13 .pgrid{display:grid;grid-template-columns:1fr 1fr;gap:13px 26px}
.p13 .pi{display:flex;gap:11px;align-items:flex-start}
.p13 .pi .n{flex:none;font-family:'JetBrains Mono',monospace;font-weight:700;font-size:10px;color:var(--emb);
border:1.5px solid var(--emb);border-radius:7px;width:26px;height:26px;display:flex;align-items:center;justify-content:center}
.p13 .pi .t{font-size:11.8px;line-height:1.42;color:var(--ink);font-weight:600;padding-top:4px}
.p13 .pi.vision .t{font-family:'Fraunces',serif;font-style:italic;font-weight:500;font-size:12.6px;color:var(--emb)}
.p13 .card{position:relative;border:1px solid var(--grid);border-radius:0 12px 12px 12px;background:var(--card2);margin-top:26px;padding:16px 18px 14px}
.p13 .card .clip{position:absolute;top:-26px;left:-1px;height:26px;background:var(--ink);border-radius:7px 16px 0 0;
display:flex;align-items:center;gap:10px;padding:0 13px}
.p13 .card .clip .nm{font-family:'Fraunces',serif;font-weight:500;font-size:13.5px;color:#0C0D10}
.p13 .card .clip .fl{font-family:'JetBrains Mono',monospace;font-weight:600;font-size:7.5px;letter-spacing:.16em;color:rgba(12,13,16,.6)}
.p13 .crow{display:flex;justify-content:space-between;align-items:center;border-top:1px solid var(--grid);padding:9px 0}
.p13 .crow:first-of-type{border-top:none}
.p13 .crow .k{font-family:'JetBrains Mono',monospace;font-size:8px;letter-spacing:.2em;color:var(--dim)}
.p13 .crow .v{font-family:'JetBrains Mono',monospace;font-weight:600;font-size:10.5px;letter-spacing:.04em;color:var(--ink)}
.p13 .closeline{margin-top:16px;font-family:'Fraunces',serif;font-style:italic;font-weight:500;font-size:14px;line-height:1.5;color:var(--mut);text-align:center}
.p13 .closeline b{color:var(--emb);font-weight:600}
.p13 .endrow{margin-top:16px;display:flex;align-items:center;justify-content:space-between}
.p13 .stamp2{transform:rotate(-6deg);border:2px solid var(--emb);border-radius:6px;padding:6px 14px;
font-family:'JetBrains Mono',monospace;font-weight:700;font-size:11px;letter-spacing:.3em;color:var(--emb)}
.p13 .bc{display:flex;flex-direction:column;align-items:flex-end;gap:3px}
.p13 .bc svg{height:26px}
.p13 .bc .yr{font-family:'JetBrains Mono',monospace;font-size:7.5px;letter-spacing:.3em;color:var(--dim)}
.p13 .minidrawer{display:flex;gap:5px;margin-top:18px}
.p13 .md{flex:1;height:11px;border-radius:3px 7px 0 0;opacity:.92}
.p13 .mdl{border-bottom:1px solid var(--grid2);height:1px;margin-top:0}
"""
s=s.replace("</style>",css+"</style>",1)

pr=["Understand before you build.","Vision creates direction. Execution creates momentum.",
"Commercial growth is a business problem &mdash; not a sales problem.","Build systems before you scale people.",
"Measure decisions &mdash; not assumptions.","Technology should improve thinking &mdash; not replace it.",
"Great leaders create ownership.","Commercial success belongs to every department.",
"Continuous learning is a competitive advantage.","If you connect to the vision, you'll always know where you're going."]
pis=""
for i,t in enumerate(pr):
    cls=' vision' if i==9 else ''
    pis+='<div class="pi%s"><div class="n">%02d</div><div class="t">%s</div></div>'%(cls,i+1,t)

bars=""; x=0
import random
w=[2,1,3,1,2,1,1,3,2,1,2,3,1,2,1,3,1,1,2,3,1,2]
for i,ww in enumerate(w):
    bars+='<rect x="%d" y="0" width="%d" height="26" fill="%s"/>'%(x,ww,"#8E8E93" if i%3 else "#F2F1ED")
    x+=ww+2

page="""
<!-- ================= PAGE 13 . FINAL THOUGHTS ================= -->
<section class="page casef p13" style="--fc:var(--emb)">
  <span class="brk tl"></span><span class="brk tr"></span><span class="brk bl"></span><span class="brk br"></span>
  <div class="hd">
    <div class="rub"><span class="d"></span>FINAL THOUGHTS</div>
    <div class="tok">END OF FILE</div>
  </div>
  <div class="ttl">The Builder's Principles</div>
  <div class="meta">TEN PRINCIPLES &middot; ONE OPERATING SYSTEM</div>
  <div class="folder">
    <div class="flip"><span class="nm">The Builder</span><span class="fl">FINAL THOUGHTS</span></div>
    <div class="inner">
      <div>
        <div class="zr"><b>A</b><span class="d2"></span>THE BUILDER'S PRINCIPLES</div>
        <div class="pgrid">"""+pis+"""</div>
      </div>
      <div>
        <div class="zr"><b>B</b><span class="d2"></span>CONTACT</div>
        <div class="card">
          <div class="clip"><span class="nm">Oran Carmon</span><span class="fl">COMMERCIAL BUILDER</span></div>
          <div class="crow"><span class="k">LINKEDIN</span><span class="v">linkedin.com/in/oran-carmon</span></div>
          <div class="crow"><span class="k">EMAIL</span><span class="v">orancarmon@gmail.com</span></div>
          <div class="crow"><span class="k">PHONE</span><span class="v">+972-54-668-5331</span></div>
        </div>
        <div class="endrow">
          <div class="stamp2">CASE CLOSED</div>
          <div class="bc"><svg viewBox="0 0 %d 26">%s</svg><span class="yr">ARCHIVE 2026</span></div>
        </div>
        <div class="minidrawer">
          <div class="md" style="background:var(--emb)"></div>
          <div class="md" style="background:var(--brass)"></div>
          <div class="md" style="background:var(--ice)"></div>
          <div class="md" style="background:var(--ink)"></div>
        </div>
        <div class="mdl"></div>
        <div class="closeline">Turning vision into <b>measurable growth</b>.</div>
      </div>
    </div>
  </div>
  <div class="ftr">
    <span>THE COMMERCIAL BUILDER</span>
    <span class="mid"><span class="d"></span>FINAL THOUGHTS</span>
    <span><b>P.13</b> &mdash; 13</span>
  </div>
</section>
"""%(x,bars)
s=s.replace("</body></html>",page+"\n</body></html>")
io.open(p,"w",encoding="utf-8").write(s)
print("page 13 added")
