# -*- coding: utf-8 -*-
import io
p="casebook.html"; s=io.open(p,encoding="utf-8").read()

css="""
/* ============ PAGE 03 — PHILOSOPHY ============ */
.p03 .hd{position:absolute;top:50px;left:72px;right:72px;display:flex;justify-content:space-between;align-items:center;z-index:5}
.p03 .rub{display:flex;align-items:center;gap:11px;font-family:'JetBrains Mono',monospace;font-weight:700;font-size:10.5px;letter-spacing:.26em;color:var(--ink)}
.p03 .rub .d{width:7px;height:7px;background:var(--emb);transform:rotate(45deg)}
.p03 .tok{display:inline-flex;align-items:center;gap:8px;font-family:'JetBrains Mono',monospace;font-weight:600;font-size:9.5px;letter-spacing:.16em;
border:1px solid var(--grid);border-radius:7px;padding:6px 12px;color:var(--emb)}
.p03 .title{position:absolute;top:96px;left:72px;font-weight:800;font-size:37px;letter-spacing:-.03em;line-height:1.12}
.p03 .title .g{color:var(--emb)}
.p03 .grid{position:absolute;top:236px;left:72px;right:72px;display:grid;grid-template-columns:repeat(4,1fr);column-gap:30px;row-gap:34px}
.p03 .cellrow{position:relative}
.p03 .rowline{position:absolute;left:100px;right:20px;top:28px;height:1px;background:repeating-linear-gradient(90deg,var(--grid2) 0 5px,transparent 5px 11px);z-index:1}
.p03 .step{position:relative;z-index:2}
.p03 .node{width:57px;height:57px;border-radius:50%;background:var(--card);border:1.5px solid var(--grid2);display:flex;align-items:center;justify-content:center}
.p03 .node svg{width:34px;height:34px;fill:none;stroke:#F2F1ED;stroke-width:1.5;stroke-linecap:round;stroke-linejoin:round}
.p03 .node svg .f{fill:#F4603E;stroke:none}
.p03 .node svg .dsh{stroke-dasharray:2.2 2.8;stroke:#8E8E93}
.p03 .node svg .em{stroke:#F4603E}
.p03 .snum{margin-top:12px;font-family:'JetBrains Mono',monospace;font-size:9px;letter-spacing:.2em;color:var(--dim)}
.p03 .snum b{color:var(--emb);font-weight:700}
.p03 .sname{margin-top:4px;font-weight:700;font-size:15.5px;letter-spacing:-.01em;color:var(--ink)}
.p03 .sdesc{margin-top:5px;font-weight:400;font-size:11.5px;line-height:1.45;color:var(--mut);max-width:230px}
.p03 .qt{position:absolute;left:50%;transform:translateX(-50%);bottom:76px;padding:14px 26px;text-align:center}
.p03 .qt::before,.p03 .qt::after{content:"";position:absolute;width:17px;height:17px;border:0 solid var(--emb)}
.p03 .qt::before{top:0;left:0;border-top-width:2px;border-left-width:2px}
.p03 .qt::after{bottom:0;right:0;border-bottom-width:2px;border-right-width:2px}
.p03 .qt .qx{font-family:'Fraunces',serif;font-style:italic;font-weight:500;font-size:19px;color:var(--ink)}
.p03 .qt .qx b{color:var(--emb);font-weight:600}
.p03 .qt .who{margin-top:7px;font-family:'JetBrains Mono',monospace;font-size:8px;letter-spacing:.24em;color:var(--dim)}
"""
s=s.replace("</style>",css+"</style>",1)

def step(num,name,desc,icon,emnum=False):
    nb='<b>%s</b>'%num if emnum else num
    return ('      <div class="step"><div class="node">%s</div>'
            '<div class="snum">STEP %s</div><div class="sname">%s</div><div class="sdesc">%s</div></div>\n')%(icon,nb,name,desc)

I={}
I['vision']='<svg viewBox="0 0 48 48"><path d="M6 40h36"/><path d="M6 40c6-1.5 9-5 10-9"/><circle cx="14.5" cy="15.5" r="3.4"/><path d="M14.5 18.9v7.6"/><path d="M14.5 21.5l4.4-2.2"/><path d="M14.5 21.5l-4 3"/><path d="M14.5 26.5l3.2 5.5"/><path d="M14.5 26.5l-2.6 6"/><path class="dsh" d="M21.5 14.5h14"/><circle class="f" cx="40" cy="14.5" r="2.6"/></svg>'
I['biz']='<svg viewBox="0 0 48 48"><path d="M10 22l14-8 14 8"/><path d="M13 20.5V34c0 1.4 4.9 4 11 4s11-2.6 11-4V20.5"/><path d="M13 27c0 1.4 4.9 4 11 4s11-2.6 11-4"/><circle class="f" cx="24" cy="22.5" r="2"/><path class="dsh" d="M24 14V7"/></svg>'
I['market']='<svg viewBox="0 0 48 48"><circle cx="24" cy="24" r="17"/><circle class="dsh" cx="24" cy="24" r="9.5"/><path d="M24 24L35.5 12.5"/><circle class="f" cx="17" cy="28.5" r="2"/><circle class="f" cx="30" cy="31" r="2"/><circle class="f" cx="19" cy="15.5" r="2"/></svg>'
I['arch']='<svg viewBox="0 0 48 48"><path d="M8 40h32"/><rect x="11" y="30" width="9" height="10"/><rect x="21.5" y="24" width="9" height="16"/><path d="M37 40V12h-13"/><path d="M26 12l2.5 3.4"/><path class="dsh" d="M28.5 12v6"/><rect class="em" x="25.8" y="18" width="5.4" height="5"/></svg>'
I['people']='<svg viewBox="0 0 48 48"><path d="M8 39.5h32"/><circle cx="13" cy="19" r="3.2"/><path d="M8.6 32c0-4 2-6.6 4.4-6.6s4.4 2.6 4.4 6.6"/><circle class="em" cx="24" cy="13.5" r="3.6"/><path class="em" d="M19 28c0-4.6 2.2-7.4 5-7.4s5 2.8 5 7.4"/><circle cx="35" cy="19" r="3.2"/><path d="M30.6 32c0-4 2-6.6 4.4-6.6s4.4 2.6 4.4 6.6"/><path class="dsh" d="M18.5 34.5h11"/></svg>'
I['exec']='<svg viewBox="0 0 48 48"><path class="dsh" d="M7 32c4 2 9 .8 9.8-2.4.6-2.6-3.4-3.4-4-.8-.7 3 4.6 4.6 9.2 2.8"/><path d="M24 30L42 11l-6.2 21-4.6-6.4-7.2 4.4z"/><path class="em" d="M31.2 25.6L42 11"/></svg>'
I['measure']='<svg viewBox="0 0 48 48"><path d="M9 39V9"/><path d="M9 39h30"/><path d="M9 31h3M9 23h3M9 15h3"/><path d="M14 33l7-6 6 3.6 10-11"/><circle class="f" cx="37" cy="19.6" r="2.4"/><path class="dsh" d="M37 17V9.5"/></svg>'
I['improve']='<svg viewBox="0 0 48 48"><path d="M37 27a13 13 0 1 1-4.6-9.9"/><path class="em" d="M31 9.5L39.5 9l.5 8.5"/><path class="em" d="M39.5 9L31.8 16.8"/><circle class="f" cx="24" cy="27" r="1.8"/></svg>'

row1=(step("01","Vision","Define where the business is going.",I['vision'])+
step("02","Business Understanding","Understand the business before improving it.",I['biz'])+
step("03","Market Understanding","Understand the customer before creating the message.",I['market'])+
step("04","Commercial Architecture","Build the commercial engine before scaling it.",I['arch']))
row2=(step("05","People &amp; Leadership","Create ownership, not dependency.",I['people'])+
step("06","Execution","Turn strategy into consistent execution.",I['exec'])+
step("07","Measurement","Measure decisions, not assumptions.",I['measure'])+
step("08","Continuous Improvement","Learn faster than the market evolves.",I['improve']))

page="""
<!-- ================= PAGE 03 · PHILOSOPHY ================= -->
<section class="page p03">
  <span class="brk tl"></span><span class="brk tr"></span><span class="brk bl"></span><span class="brk br"></span>
  <div class="hd">
    <div class="rub"><span class="d"></span>MY COMMERCIAL PHILOSOPHY</div>
    <div class="tok">THE OPERATING SYSTEM &#8250;</div>
  </div>
  <div class="title">Every business is different.<br><span class="g">The principles of growth are not.</span></div>
  <div class="grid">
"""+row1+row2+"""  </div>
  <div class="qt">
    <div class="qx">First build a system that works. <b>Then build a business that scales.</b></div>
    <div class="who">SIGNATURE PRINCIPLE</div>
  </div>
  <div class="ftr">
    <span>THE COMMERCIAL BUILDER</span>
    <span><b>P.03</b> &mdash; 13</span>
  </div>
</section>
"""
s=s.replace("</body></html>",page+"\n</body></html>")
io.open(p,"w",encoding="utf-8").write(s)
print("page 3 added")
