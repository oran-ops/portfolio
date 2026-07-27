# -*- coding: utf-8 -*-
import io
p="casebook.html"; s=io.open(p,encoding="utf-8").read()

css="""
/* ============ PAGE 11 - LEADERSHIP ============ */
.p11 .folder{padding:24px 30px 18px}
.p11 .lead{font-family:'Fraunces',serif;font-style:italic;font-weight:500;font-size:15px;line-height:1.5;color:var(--mut);max-width:1020px}
.p11 .lead b{color:var(--ink);font-weight:500}
.p11 .cols{display:grid;grid-template-columns:59fr 41fr;column-gap:34px;margin-top:18px;position:relative}
.p11 .cols::before{content:"";position:absolute;left:57.2%;top:2px;bottom:2px;width:1px;background:repeating-linear-gradient(180deg,var(--grid) 0 5px,transparent 5px 11px)}
.p11 .zr{margin-bottom:12px}
.p11 .pr{display:flex;gap:14px;margin-bottom:13px}
.p11 .pr .n{flex:none;width:30px;height:30px;border:1.5px solid var(--emb);border-radius:8px;display:flex;align-items:center;justify-content:center;
font-family:'JetBrains Mono',monospace;font-weight:700;font-size:11px;color:var(--emb)}
.p11 .pr .nm2{font-weight:700;font-size:13.2px;color:var(--ink);letter-spacing:-.01em}
.p11 .pr .ds{margin-top:3px;font-size:10.8px;line-height:1.45;color:var(--mut)}
.p11 .tools{display:grid;grid-template-columns:1fr 1fr;gap:7px 14px}
.p11 .lg{font-size:11px}
.p11 .sigq{margin-top:16px;padding-top:14px;border-top:1px solid var(--grid);text-align:center}
.p11 .sigq .qx{font-family:'Fraunces',serif;font-style:italic;font-weight:500;font-size:17.5px;color:var(--ink)}
.p11 .sigq .qx b{color:var(--emb);font-weight:600}
.p11 .sigq .who{margin-top:5px;font-family:'JetBrains Mono',monospace;font-size:7.5px;letter-spacing:.26em;color:var(--dim)}
"""
s=s.replace("</style>",css+"</style>",1)

def pr(n,name,desc):
    return ('<div class="pr"><div class="n">%02d</div><div><div class="nm2">%s</div>'
            '<div class="ds">%s</div></div></div>')%(n,name,desc)

princ=(pr(1,"Build Trust Before Performance","People perform better when expectations are clear and trust is earned.")+
pr(2,"Coach Before You Judge","Every performance issue deserves investigation first &mdash; understand the process, review the data, listen first, coach second, decide last.")+
pr(3,"Create Ownership","People shouldn't execute tasks. They should own outcomes.")+
pr(4,"Decisions Based on Facts","KPIs don't replace leadership &mdash; they improve it. Every coaching session begins with evidence, not assumptions.")+
pr(5,"Great Managers Solve Today's Problems. Great Leaders Build Tomorrow's System.","My objective was never to close one more deal &mdash; it was to build an organization that produces consistent results without depending on one individual."))

tools="".join('<div class="lg"><span class="n">LOG.%02d</span><span class="c">&#10003;</span>%s</div>'%(i+1,t) for i,t in enumerate([
"Hiring &amp; Recruitment","Onboarding Programs","Weekly Team Meetings","Monthly 1:1 Reviews",
"Quarterly Performance Reviews","KPI Design","Coaching","Sales Methodology",
"Performance Improvement Plans","Cross-functional Leadership"]))

page="""
<!-- ================= PAGE 11 . LEADERSHIP ================= -->
<section class="page casef p11" style="--fc:var(--emb)">
  <span class="brk tl"></span><span class="brk tr"></span><span class="brk bl"></span><span class="brk br"></span>
  <div class="hd">
    <div class="rub"><span class="d"></span>LEADERSHIP</div>
    <div class="tok">MANAGEMENT FILE</div>
  </div>
  <div class="ttl">Building People. Building Systems. Building Accountability.</div>
  <div class="meta">HOW I LEAD &middot; PRINCIPLES &amp; TOOLKIT</div>
  <div class="folder">
    <div class="flip"><span class="nm">Leadership</span><span class="fl">MANAGEMENT FILE</span></div>
    <div class="lead">I believe leadership is not measured by how many people report to you &mdash; it is measured by <b>how many people become better because of you</b>. My role is to create clarity, ownership and an environment where people consistently perform at their best.</div>
    <div class="cols">
      <div>
        <div class="zr"><b>A</b><span class="d2"></span>LEADERSHIP PRINCIPLES</div>
        """+princ+"""
      </div>
      <div>
        <div class="zr"><b>B</b><span class="d2"></span>LEADERSHIP TOOLKIT</div>
        <div class="tools">"""+tools+"""</div>
        <div class="sigq">
          <div class="qx">Leadership is not about creating better employees. <b>It's about creating people who no longer depend on you.</b></div>
          <div class="who">SIGNATURE PRINCIPLE &middot; MANAGEMENT FILE</div>
        </div>
      </div>
    </div>
  </div>
  <div class="ftr">
    <span>THE COMMERCIAL BUILDER</span>
    <span class="mid"><span class="d"></span>LEADERSHIP</span>
    <span><b>P.11</b> &mdash; 13</span>
  </div>
</section>
"""
s=s.replace("</body></html>",page+"\n</body></html>")
io.open(p,"w",encoding="utf-8").write(s)
print("page 11 added")
