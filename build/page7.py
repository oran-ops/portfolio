# -*- coding: utf-8 -*-
import io
p="casebook.html"; s=io.open(p,encoding="utf-8").read()

css="""
/* ============ PAGE 07 - OASIS COMMAND ============ */
.p07 .folder{padding:20px 26px 16px}
.p07 .inner{display:grid;grid-template-columns:1fr 1fr;column-gap:30px;position:relative}
.p07 .inner::before{content:"";position:absolute;left:50%;top:2px;bottom:2px;width:1px;background:repeating-linear-gradient(180deg,var(--grid) 0 5px,transparent 5px 11px)}
.p07 .zr{margin-bottom:8px}
.p07 .z{margin-bottom:15px}
.p07 .rgrid{display:grid;grid-template-columns:1fr 1fr;gap:5.5px 16px;margin-top:2px}
.p07 .dash{font-size:11.2px}
.p07 .lg{margin-bottom:5.5px;font-size:11.6px}
.p07 .model{margin-top:4px;padding-top:13px;border-top:1px solid var(--grid)}
.p07 .chips{display:flex;flex-wrap:nowrap;gap:8px;margin-top:10px}
.p07 .chip{flex:1;border:1px solid var(--grid);border-radius:8px;padding:8px 6px;text-align:center;
font-family:'JetBrains Mono',monospace;font-weight:600;font-size:7.8px;letter-spacing:.1em;color:var(--mut);line-height:1.5}
.p07 .chip b{display:block;color:var(--brass);font-size:8.6px;letter-spacing:.16em;margin-bottom:3px}
.p07 .insight{margin-top:15px;text-align:center;position:relative;padding:9px 0 7px}
.p07 .insight .qx{font-family:'Fraunces',serif;font-style:italic;font-weight:500;font-size:17px;color:var(--ink)}
.p07 .insight .qx b{color:var(--brass);font-weight:600}
.p07 .insight .who{margin-top:5px;font-family:'JetBrains Mono',monospace;font-size:7.5px;letter-spacing:.26em;color:var(--dim)}
"""
s=s.replace("</style>",css+"</style>",1)

resp="".join('<div class="dash">%s</div>'%t for t in ["Recruiting &amp; building the sales team",
"Defining commercial strategy","Pricing model development","KPI design","Sales methodology",
"Forecasting","Commercial reviews","Cross-functional leadership","Profitability management"])

built="".join('<div class="lg"><span class="n">LOG.%02d</span><span class="c">&#10003;</span>%s</div>'%(i+1,t) for i,t in enumerate([
"Recruited &amp; onboarded the entire sales team","Built the pricing model from scratch",
"Designed the commercial process","Implemented KPI framework",
"Created sales playbooks &amp; onboarding","Established weekly business reviews",
"Built forecasting methodology","Created cross-functional collaboration"]))

chips="".join('<div class="chip"><b>%s</b>%s</div>'%(k,t) for k,t in [
("WEEKLY","COACHING SESSIONS"),("MONTHLY","1:1 PERFORMANCE REVIEWS"),("QUARTERLY","BUSINESS REVIEWS"),
("LIVE","DEAL REVIEWS"),("ALWAYS","COMMERCIAL COACHING"),("CROSS-FN","COLLABORATION"),("OWNED","CLEAR OWNERSHIP &amp; ACCOUNTABILITY")])

page="""
<!-- ================= PAGE 07 . OASIS COMMAND ================= -->
<section class="page casef p07" style="--fc:var(--brass)">
  <span class="brk tl"></span><span class="brk tr"></span><span class="brk bl"></span><span class="brk br"></span>
  <div class="hd">
    <div class="rub"><span class="d"></span>CASE STUDY 02</div>
    <div class="tok">FILE 02 &middot; COMMAND</div>
  </div>
  <div class="ttl">Building Leaders, Not Just Sales Teams</div>
  <div class="meta">OASIS &middot; CEO &middot; CONSTRUCTION &amp; SMART BUILDING SOLUTIONS</div>
  <div class="folder">
    <div class="flip"><span class="nm">Oasis</span><span class="fl">FILE 02</span></div>
    <div class="inner">
      <div>
        <div class="z">
          <div class="zr"><b>01</b><span class="d2"></span>THE SITUATION</div>
          <div class="para">As CEO, my responsibility extended far beyond sales. The objective wasn't simply to increase revenue &mdash; it was to build a <b>profitable, scalable commercial organization</b> capable of supporting the company's long-term vision.</div>
        </div>
        <div class="z" style="margin-bottom:0">
          <div class="zr"><b>02</b><span class="d2"></span>MY RESPONSIBILITIES</div>
          <div class="rgrid">"""+resp+"""</div>
        </div>
      </div>
      <div>
        <div class="zr"><b>03</b><span class="d2"></span>COMMERCIAL SYSTEM BUILT</div>
        """+built+"""
      </div>
    </div>
    <div class="model">
      <div class="zr"><b>04</b><span class="d2"></span>LEADERSHIP MODEL</div>
      <div class="chips">"""+chips+"""</div>
    </div>
    <div class="insight">
      <div class="qx">High-performing sales teams aren't built by pressure. <b>They're built by clarity.</b></div>
      <div class="who">SIGNATURE INSIGHT &middot; FILE 02 &middot; OASIS</div>
    </div>
  </div>
  <div class="ftr">
    <span>THE COMMERCIAL BUILDER</span>
    <span class="mid"><span class="d"></span>CASE STUDY &mdash; OASIS</span>
    <span><b>P.07</b> &mdash; 13</span>
  </div>
</section>
"""
s=s.replace("</body></html>",page+"\n</body></html>")
io.open(p,"w",encoding="utf-8").write(s)
print("page 7 added")
