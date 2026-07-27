# -*- coding: utf-8 -*-
import io
p="casebook.html"; s=io.open(p,encoding="utf-8").read()

# --- fidelity fix: cover footer-left = old-PDF tagline ---
s=s.replace("<span>SAAS &middot; FINTECH &middot; ENTERPRISE SALES &middot; COMMERCIAL LEADERSHIP &middot; AI-POWERED GROWTH</span>",
            "<span>A PRACTICAL GUIDE TO BUILDING COMMERCIAL ORGANIZATIONS THAT SCALE</span>",1)

css="""
/* ============ SHARED CASE-FILE KIT ============ */
.casef .hd{position:absolute;top:48px;left:72px;right:72px;display:flex;justify-content:space-between;align-items:center;z-index:5}
.casef .rub{display:flex;align-items:center;gap:11px;font-family:'JetBrains Mono',monospace;font-weight:700;font-size:10.5px;letter-spacing:.26em;color:var(--ink)}
.casef .rub .d{width:7px;height:7px;background:var(--fc);transform:rotate(45deg)}
.casef .tok{display:inline-flex;align-items:center;gap:8px;font-family:'JetBrains Mono',monospace;font-weight:600;font-size:9.5px;letter-spacing:.16em;
border:1px solid var(--grid);border-radius:7px;padding:6px 12px;color:var(--fc)}
.casef .ttl{position:absolute;top:88px;left:72px;font-weight:800;font-size:30px;letter-spacing:-.025em;color:var(--ink)}
.casef .meta{position:absolute;top:132px;left:72px;font-family:'JetBrains Mono',monospace;font-size:9.5px;letter-spacing:.22em;color:var(--mut)}
.casef .folder{position:absolute;top:172px;left:72px;right:72px;height:474px;background:var(--card);border:1px solid var(--hair);
border-radius:0 16px 16px 16px;padding:22px 26px}
.casef .flip{position:absolute;top:-30px;left:-1px;height:30px;background:var(--fc);border-radius:8px 18px 0 0;
display:flex;align-items:center;gap:12px;padding:0 16px}
.casef .flip .nm{font-family:'Fraunces',serif;font-weight:500;font-size:15px;color:#0C0D10}
.casef .flip .fl{font-family:'JetBrains Mono',monospace;font-weight:600;font-size:8.5px;letter-spacing:.16em;color:rgba(12,13,16,.62)}
.casef .zr{display:flex;align-items:center;gap:9px;font-family:'JetBrains Mono',monospace;font-weight:700;font-size:10px;letter-spacing:.22em;color:var(--ink)}
.casef .zr b{color:var(--fc);font-weight:700}
.casef .zr .d2{width:5px;height:5px;background:var(--fc);transform:rotate(45deg)}
.casef .para{font-size:12px;line-height:1.55;color:var(--mut)}
.casef .para b{color:var(--ink);font-weight:600}
.casef .subl{font-family:'JetBrains Mono',monospace;font-weight:600;font-size:8.5px;letter-spacing:.24em;color:var(--dim)}
.casef .mi{display:flex;align-items:center;gap:9px;font-size:11.5px;color:var(--mut)}
.casef .mi .o{flex:none;width:13px;height:13px;border:1.5px solid var(--fc);border-radius:50%;position:relative}
.casef .mi .o::after{content:"";position:absolute;left:2.5px;right:2.5px;top:50%;height:1.5px;margin-top:-1px;background:var(--fc)}
.casef .lg{display:flex;align-items:center;gap:8px;font-size:11.8px;font-weight:600;color:var(--ink)}
.casef .lg .n{font-family:'JetBrains Mono',monospace;font-size:7.5px;letter-spacing:.1em;color:var(--dim);width:34px;flex:none}
.casef .lg .c{flex:none;width:11px;height:11px;background:var(--fc);color:#0C0D10;font-size:9px;font-weight:800;line-height:11px;text-align:center}
.casef .dash{display:flex;align-items:center;gap:9px;font-size:11.8px;color:var(--mut)}
.casef .dash::before{content:"";flex:none;width:9px;height:2px;background:var(--fc)}
.casef .sig{position:absolute;left:50%;transform:translateX(-50%);bottom:54px;padding:10px 24px;text-align:center;white-space:nowrap}
.casef .sig::before,.casef .sig::after{content:"";position:absolute;width:15px;height:15px;border:0 solid var(--fc)}
.casef .sig::before{top:0;left:0;border-top-width:2px;border-left-width:2px}
.casef .sig::after{bottom:0;right:0;border-bottom-width:2px;border-right-width:2px}
.casef .sig .qx{font-family:'Fraunces',serif;font-style:italic;font-weight:500;font-size:16.5px;color:var(--ink)}
.casef .sig .qx b{color:var(--fc);font-weight:600}
.casef .sig .who{margin-top:5px;font-family:'JetBrains Mono',monospace;font-size:7.5px;letter-spacing:.26em;color:var(--dim)}

/* ============ PAGE 05 - XTIX INTAKE ============ */
.p05 .cols{display:grid;grid-template-columns:1fr 1fr;column-gap:30px;height:100%;position:relative}
.p05 .cols::before{content:"";position:absolute;left:50%;top:4px;bottom:4px;width:1px;background:repeating-linear-gradient(180deg,var(--grid) 0 5px,transparent 5px 11px)}
.p05 .z{margin-bottom:16px}
.p05 .z .zr{margin-bottom:8px}
.p05 .reality{margin-top:10px;border:1px solid var(--grid);border-radius:10px;padding:11px 14px;background:var(--card2)}
.p05 .reality .subl{display:block;margin-bottom:8px}
.p05 .rgrid{display:grid;grid-template-columns:1fr 1fr;gap:6px 14px}
.p05 .agrid{display:grid;grid-template-columns:1fr 1fr;gap:6px 14px;margin-top:8px}
.p05 .then{margin-top:9px;font-family:'Fraunces',serif;font-style:italic;font-size:12.5px;color:var(--fc)}
.p05 .bgrid{display:grid;grid-template-columns:1fr 1fr;gap:7px 16px;margin-top:8px}
"""
s=s.replace("</style>",css+"</style>",1)

def mi(t): return '<div class="mi"><span class="o"></span>%s</div>'%t
def lg(n,t): return '<div class="lg"><span class="n">LOG.%02d</span><span class="c">&#10003;</span>%s</div>'%(n,t)
def dash(t): return '<div class="dash">%s</div>'%t

reality="".join(mi(t) for t in ["No CRM","No Business Development function","No sales methodology",
"No outbound process","No pipeline management","No KPI framework","No reporting structure"])
approach="".join(dash(t) for t in ["Business &amp; product analysis","Market research","Competitive analysis",
"ICP definition","Customer segmentation","Commercial positioning"])
built="".join(lg(i+1,t) for i,t in enumerate(["Commercial Strategy","HubSpot CRM Infrastructure",
"Business Development Process","Sales Pipeline","ICP Framework","Outbound Sequences",
"KPI Framework","Forecasting Structure","Reporting Dashboards","AI-Powered Outbound Engine"]))

page="""
<!-- ================= PAGE 05 . XTIX INTAKE ================= -->
<section class="page casef p05" style="--fc:var(--emb)">
  <span class="brk tl"></span><span class="brk tr"></span><span class="brk bl"></span><span class="brk br"></span>
  <div class="hd">
    <div class="rub"><span class="d"></span>CASE STUDY 01</div>
    <div class="tok">FILE 01 &middot; INTAKE</div>
  </div>
  <div class="ttl">Building a Commercial Function From Zero</div>
  <div class="meta">XTIX &middot; FINTECH SAAS &middot; EARLY-STAGE STARTUP</div>
  <div class="folder">
    <div class="flip"><span class="nm">XTIX</span><span class="fl">FILE 01</span></div>
    <div class="cols">
      <div>
        <div class="z">
          <div class="zr"><b>01</b><span class="d2"></span>THE SITUATION</div>
          <div class="para">When I joined XTIX, the company had a <b>strong vision and product</b> &mdash; but no commercial infrastructure to support scalable growth.</div>
          <div class="reality"><span class="subl">COMMERCIAL REALITY &middot; MISSING AT INTAKE</span>
            <div class="rgrid">"""+reality+"""</div>
          </div>
        </div>
        <div class="z">
          <div class="zr"><b>02</b><span class="d2"></span>MY MISSION</div>
          <div class="para">Design and build a <b>commercial operating system</b> capable of supporting predictable business growth &mdash; starting with the Israeli market and later expanding globally.</div>
        </div>
      </div>
      <div>
        <div class="z">
          <div class="zr"><b>03</b><span class="d2"></span>MY APPROACH</div>
          <div class="para">Rather than launching outbound immediately, I focused on <b>understanding the business first</b>. The first phase included:</div>
          <div class="agrid">"""+approach+"""</div>
          <div class="then">Only then did execution begin.</div>
        </div>
        <div class="z">
          <div class="zr"><b>04</b><span class="d2"></span>WHAT I BUILT</div>
          <div class="bgrid">"""+built+"""</div>
        </div>
      </div>
    </div>
  </div>
  <div class="ftr">
    <span>THE COMMERCIAL BUILDER</span>
    <span class="mid"><span class="d"></span>CASE STUDY &mdash; XTIX</span>
    <span><b>P.05</b> &mdash; 13</span>
  </div>
</section>
"""
s=s.replace("</body></html>",page+"\n</body></html>")
io.open(p,"w",encoding="utf-8").write(s)
print("page 5 added")
