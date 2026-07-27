# -*- coding: utf-8 -*-
import io
p="casebook.html"; s=io.open(p,encoding="utf-8").read()

css="""
/* ============ PAGE 09 - EVENTER SYNC ============ */
.p09 .folder{padding:26px 30px 20px}
.p09 .inner{display:grid;grid-template-columns:47fr 53fr;column-gap:32px;position:relative}
.p09 .inner::before{content:"";position:absolute;left:44.5%;top:2px;bottom:2px;width:1px;background:repeating-linear-gradient(180deg,var(--grid) 0 5px,transparent 5px 11px)}
.p09 .z{margin-bottom:17px}
.p09 .zr{margin-bottom:9px}
.p09 .para{font-size:11.9px;line-height:1.58}
.p09 .lg{margin-bottom:8px;font-size:11.6px}
.p09 .conv{margin:2px 0 14px}
.p09 .band{margin-top:6px;padding-top:15px;border-top:1px solid var(--grid);display:grid;grid-template-columns:1fr 1fr;column-gap:32px}
.p09 .band .para{font-size:11.6px}
.p09 .insight{border-left:2px solid var(--ice);padding:2px 0 2px 18px}
.p09 .insight .qx{font-family:'Fraunces',serif;font-style:italic;font-weight:500;font-size:15px;line-height:1.45;color:var(--ink)}
.p09 .insight .qx b{color:var(--ice);font-weight:600}
.p09 .insight .who{margin-top:6px;font-family:'JetBrains Mono',monospace;font-size:7.5px;letter-spacing:.24em;color:var(--dim)}
"""
s=s.replace("</style>",css+"</style>",1)

# convergence diagram: 5 dept nodes flow into CUSTOMER; dashed feedback returns to top
depts=["PRODUCT","MARKETING","FINANCE","R&amp;D","BUSINESS DEVELOPMENT"]
rows=""
y=16
for i,d in enumerate(depts):
    em = (i==4)
    col = "#7CC4E8" if em else "#3A3D43"
    tcol= "#F2F1ED" if em else "#8E8E93"
    fill= "rgba(124,196,232,.12)" if em else "#16181C"
    w=148
    rows+=('<rect x="4" y="%d" width="%d" height="22" rx="6" fill="%s" stroke="%s" stroke-width="1.3"/>'
           '<text x="%.1f" y="%.1f" text-anchor="middle" font-size="7.2" letter-spacing="1.2" fill="%s">%s</text>'
           '<path d="M%d %.1f C 230 %.1f, 260 96, 330 96" fill="none" stroke="%s" stroke-width="1.4"/>'
           )%(y,w,fill,col, 4+w/2, y+14.5, tcol, d, 4+w, y+11.0, y+11.0, col)
    y+=34
conv=('<svg class="conv" viewBox="0 0 560 190" style="width:100%;height:auto">'
      +rows+
      '<path d="M336 96 l-7 -4 v8 z" fill="#7CC4E8"/>'
      '<circle cx="392" cy="96" r="34" fill="#16181C" stroke="#7CC4E8" stroke-width="2.2"/>'
      '<text x="392" y="93" text-anchor="middle" font-size="8.5" font-weight="700" letter-spacing="1.4" fill="#F2F1ED">THE</text>'
      '<text x="392" y="104" text-anchor="middle" font-size="8.5" font-weight="700" letter-spacing="1.4" fill="#F2F1ED">CUSTOMER</text>'
      '<path d="M392 62 C 392 16, 250 8, 160 8" fill="none" stroke="#8E8E93" stroke-width="1.1" stroke-dasharray="3 4"/>'
      '<path d="M160 8 l7 -3.6 v7.2 z" fill="#8E8E93" transform="rotate(180 160 8)"/>'
      '<text x="300" y="24" text-anchor="middle" font-size="6.6" letter-spacing="1.6" fill="#5A5B60">CUSTOMER INSIGHT &#8594; BUSINESS DECISIONS</text>'
      '<text x="446" y="150" text-anchor="middle" font-size="6.6" letter-spacing="1.4" fill="#5A5B60">SHARED RESPONSIBILITY</text>'
      '</svg>')

contrib="".join('<div class="lg"><span class="n">LOG.%02d</span><span class="c">&#10003;</span>%s</div>'%(i+1,t) for i,t in enumerate([
"Managed &amp; coached Business Development team members","Participated in recruiting commercial talent",
"Improved commercial processes","Introduced new business initiatives",
"Worked closely with Product, Marketing, Finance &amp; R&amp;D",
"Brought customer feedback directly into product discussions",
"Helped improve commercial alignment across the organization"]))

page="""
<!-- ================= PAGE 09 . EVENTER SYNC ================= -->
<section class="page casef p09" style="--fc:var(--ice)">
  <span class="brk tl"></span><span class="brk tr"></span><span class="brk bl"></span><span class="brk br"></span>
  <div class="hd">
    <div class="rub"><span class="d"></span>CASE STUDY 03</div>
    <div class="tok">FILE 03 &middot; SYNC</div>
  </div>
  <div class="ttl">Aligning Commercial Execution Across Teams</div>
  <div class="meta">EVENTER &middot; SAAS &middot; EVENT MANAGEMENT PLATFORM</div>
  <div class="folder">
    <div class="flip"><span class="nm">Eventer</span><span class="fl">FILE 03</span></div>
    <div class="inner">
      <div>
        <div class="z">
          <div class="zr"><b>01</b><span class="d2"></span>THE SITUATION</div>
          <div class="para">Eventer already had an <b>existing commercial operation</b>. Unlike previous roles, the objective wasn't to build a department from scratch &mdash; it was to improve execution, strengthen collaboration between departments and identify new commercial growth opportunities.</div>
        </div>
        <div class="z">
          <div class="zr"><b>02</b><span class="d2"></span>MY ROLE</div>
          <div class="para">I worked across multiple business functions to improve commercial performance by <b>connecting business strategy with day-to-day execution</b>.</div>
        </div>
        <div class="z" style="margin-bottom:0">
          <div class="zr"><b>03</b><span class="d2"></span>CROSS-FUNCTIONAL IMPACT</div>
          <div class="para">Rather than focusing only on Business Development, I worked closely with multiple departments to ensure customer insights translated into business decisions. Commercial growth became a <b>shared organizational responsibility</b> &mdash; not just a sales target.</div>
        </div>
      </div>
      <div>
        <div class="zr"><b>04</b><span class="d2"></span>ORGANIZATIONAL CONVERGENCE</div>
        """+conv+"""
        <div class="zr" style="margin-top:4px"><b>05</b><span class="d2"></span>KEY CONTRIBUTIONS</div>
        """+contrib+"""
      </div>
    </div>
    <div class="band">
      <div>
        <div class="zr"><b>06</b><span class="d2"></span>WHAT I LEARNED</div>
        <div class="para">Leadership doesn't always require authority. Some of the biggest organizational changes happen through <b>influence, collaboration and better decision-making</b>.</div>
      </div>
      <div class="insight">
        <div class="qx">Commercial growth accelerates when every department understands the customer &mdash; <b>not only Sales.</b></div>
        <div class="who">SIGNATURE INSIGHT &middot; FILE 03 &middot; EVENTER</div>
      </div>
    </div>
  </div>
  <div class="ftr">
    <span>THE COMMERCIAL BUILDER</span>
    <span class="mid"><span class="d"></span>CASE STUDY &mdash; EVENTER</span>
    <span><b>P.09</b> &mdash; 13</span>
  </div>
</section>
"""
s=s.replace("</body></html>",page+"\n</body></html>")
io.open(p,"w",encoding="utf-8").write(s)
print("page 9 added")
