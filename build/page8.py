# -*- coding: utf-8 -*-
import io, math
p="casebook.html"; s=io.open(p,encoding="utf-8").read()

css="""
/* ============ PAGE 08 - OASIS EVIDENCE ============ */
.p08 .folder{padding:22px 28px 16px}
.p08 .inner{display:grid;grid-template-columns:31fr 34fr 35fr;column-gap:26px}
.p08 .zr{margin-bottom:10px}
.p08 .stat{border:1px solid var(--grid);border-radius:0 12px 12px 12px;background:var(--card2);position:relative;margin-top:30px;padding:16px 18px 14px}
.p08 .stat .slip{position:absolute;top:-24px;left:-1px;height:24px;background:var(--brass);border-radius:7px 15px 0 0;
display:flex;align-items:center;padding:0 12px;font-family:'JetBrains Mono',monospace;font-weight:700;font-size:7.5px;letter-spacing:.2em;color:#0C0D10}
.p08 .stat .num{font-weight:800;font-size:46px;letter-spacing:-.02em;color:var(--ink);line-height:1}
.p08 .stat .num b{color:var(--brass);font-weight:800}
.p08 .stat .lbl{margin-top:6px;font-family:'JetBrains Mono',monospace;font-size:8px;letter-spacing:.22em;color:var(--dim)}
.p08 .perf{margin-top:14px}
.p08 .dash{font-size:11.2px;margin-bottom:7px}
.p08 .lg{margin-bottom:8.5px;font-size:11.6px}
.p08 .ringwrap{text-align:center}
.p08 .ringlbl{margin-top:2px;font-family:'JetBrains Mono',monospace;font-size:8px;letter-spacing:.18em;color:var(--dim)}
.p08 .band{margin-top:12px;padding-top:14px;border-top:1px solid var(--grid);display:grid;grid-template-columns:58fr 42fr;column-gap:28px}
.p08 .band .para{font-size:11.4px;line-height:1.55}
.p08 .lesson{border-left:2px solid var(--brass);padding:2px 0 2px 18px}
.p08 .lesson .qx{font-family:'Fraunces',serif;font-style:italic;font-weight:500;font-size:14.5px;line-height:1.45;color:var(--ink)}
.p08 .lesson .qx b{color:var(--brass);font-weight:600}
.p08 .lesson .who{margin-top:6px;font-family:'JetBrains Mono',monospace;font-size:7.5px;letter-spacing:.24em;color:var(--dim)}
"""
s=s.replace("</style>",css+"</style>",1)

# leadership ring: CEO center + 6 functions
cx,cy,R=120,98,58
fns=["OPERATIONS","PRODUCTION","CUSTOMER SUCCESS","FINANCE","MARKETING","TECHNICAL TEAMS"]
nodes=""
for i,f in enumerate(fns):
    a=math.radians(-90+i*60)
    x,y=cx+R*math.cos(a), cy+R*math.sin(a)
    lx,ly=cx+(R+24)*math.cos(a), cy+(R+24)*math.sin(a)
    anchor="middle"
    if lx<cx-30: anchor="end"
    if lx>cx+30: anchor="start"
    nodes+='<line x1="%.1f" y1="%.1f" x2="%.1f" y2="%.1f" stroke="#3A3D43" stroke-width="1"/>'%(cx+18*math.cos(a),cy+18*math.sin(a),x-7*math.cos(a),y-7*math.sin(a))
    nodes+='<circle cx="%.1f" cy="%.1f" r="5.5" fill="#121316" stroke="#E0A458" stroke-width="1.6"/>'%(x,y)
    nodes+='<text x="%.1f" y="%.1f" text-anchor="%s" font-size="6.8" letter-spacing="1" fill="#8E8E93">%s</text>'%(lx,ly+2.4,anchor,f)
ring=('<svg viewBox="0 0 240 196" style="width:100%%;max-width:250px;height:auto;margin:0 auto;overflow:visible">'
      '<circle cx="%d" cy="%d" r="%d" fill="none" stroke="#26282C" stroke-width="1.2" stroke-dasharray="3 4"/>'
      '<circle cx="%d" cy="%d" r="18" fill="#16181C" stroke="#E0A458" stroke-width="2"/>'
      '<text x="%d" y="%d" text-anchor="middle" font-size="8.5" font-weight="700" letter-spacing="1.5" fill="#F2F1ED">CEO</text>'
      '%s</svg>')%(cx,cy,R,cx,cy,cx,cy+3,nodes)

lead="".join('<div class="lg"><span class="n">LOG.%02d</span><span class="c">&#10003;</span>%s</div>'%(i+1,t) for i,t in enumerate([
"Recruited an entire sales team","Led a team of 5&ndash;6 sales professionals",
"Conducted weekly coaching sessions","Established KPI-driven management",
"Built onboarding documentation","Standardized commercial processes"]))

perf="".join('<div class="dash">%s</div>'%t for t in ["Built pricing strategy from zero",
"Introduced profitability-based pricing","Defined company-wide commercial KPIs",
"Improved cross-department collaboration","Created structured commercial reporting"])

page="""
<!-- ================= PAGE 08 . OASIS EVIDENCE ================= -->
<section class="page casef p08" style="--fc:var(--brass)">
  <span class="brk tl"></span><span class="brk tr"></span><span class="brk bl"></span><span class="brk br"></span>
  <div class="hd">
    <div class="rub"><span class="d"></span>CASE STUDY 02 &middot; OASIS</div>
    <div class="tok">MISSION DEBRIEF</div>
  </div>
  <div class="ttl">Evidence &mdash; Commercial Results</div>
  <div class="meta">OASIS &middot; CEO &middot; CONSTRUCTION &amp; SMART BUILDING SOLUTIONS</div>
  <div class="folder">
    <div class="flip"><span class="nm">Oasis</span><span class="fl">FILE 02 &middot; EVIDENCE</span></div>
    <div class="inner">
      <div>
        <div class="zr"><b>A</b><span class="d2"></span>BUSINESS PERFORMANCE</div>
        <div class="stat">
          <div class="slip">EVIDENCE &middot; KEY DEAL</div>
          <div class="num"><b>&#8362;</b>2M</div>
          <div class="lbl">LARGEST DEAL CLOSED</div>
        </div>
        <div class="perf">"""+perf+"""</div>
      </div>
      <div>
        <div class="zr"><b>B</b><span class="d2"></span>COMMERCIAL LEADERSHIP</div>
        """+lead+"""
      </div>
      <div class="ringwrap">
        <div class="zr" style="justify-content:center"><b>C</b><span class="d2"></span>CROSS-FUNCTIONAL LEADERSHIP</div>
        """+ring+"""
        <div class="ringlbl">WORKED CLOSELY WITH &middot; 06 FUNCTIONS</div>
      </div>
    </div>
    <div class="band">
      <div>
        <div class="zr"><b>D</b><span class="d2"></span>REFLECTION &mdash; LOOKING BACK</div>
        <div class="para">The biggest lesson I learned as CEO wasn't about selling &mdash; it was about <b>leadership</b>. The more I tried to manage every function myself, the less scalable the organization became. Real leadership begins when leaders build systems that let others succeed <b>without depending on them</b>.</div>
      </div>
      <div class="lesson">
        <div class="qx">Organizations don't scale because leaders work harder. <b>They scale because leaders create clarity, ownership and trust.</b></div>
        <div class="who">LESSON &middot; FILE 02 &middot; OASIS</div>
      </div>
    </div>
  </div>
  <div class="ftr">
    <span>THE COMMERCIAL BUILDER</span>
    <span class="mid"><span class="d"></span>CASE STUDY &mdash; OASIS</span>
    <span><b>P.08</b> &mdash; 13</span>
  </div>
</section>
"""
s=s.replace("</body></html>",page+"\n</body></html>")
io.open(p,"w",encoding="utf-8").write(s)
print("page 8 added")
