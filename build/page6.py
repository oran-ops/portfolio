# -*- coding: utf-8 -*-
import io, math
p="casebook.html"; s=io.open(p,encoding="utf-8").read()

css="""
/* ============ PAGE 06 - XTIX EVIDENCE ============ */
.p06 .folder{padding:20px 26px 16px}
.p06 .inner{display:grid;grid-template-columns:46fr 54fr;column-gap:28px}
.p06 .zr{margin-bottom:9px}
.p06 .tbl{width:100%;border-collapse:collapse}
.p06 .tbl td{border-top:1px solid var(--grid);padding:6.5px 2px;vertical-align:middle}
.p06 .tbl tr:first-child td{border-top:none}
.p06 .tbl .k{font-family:'JetBrains Mono',monospace;font-size:8.5px;letter-spacing:.14em;color:var(--dim);line-height:1.5}
.p06 .tbl .v{text-align:right;font-weight:700;font-size:14.5px;color:var(--ink);white-space:nowrap}
.p06 .tbl .v.em{color:var(--emb)}
.p06 .gaug{display:flex;justify-content:space-between;margin-top:14px;padding-top:12px;border-top:1px solid var(--grid)}
.p06 .g1{text-align:center;width:88px}
.p06 .g1 .gl{margin-top:4px;font-family:'JetBrains Mono',monospace;font-size:7.5px;letter-spacing:.14em;color:var(--dim);line-height:1.6}
.p06 .ops .lg{margin-bottom:6px;font-size:11.4px}
.p06 .tech{margin-top:12px;border:1px solid var(--grid);border-radius:10px;background:var(--card2);padding:12px 14px}
.p06 .tech .para{font-size:11.3px;line-height:1.5}
.p06 .tech .dash{font-size:11px;margin-top:5px}
.p06 .tech .pur{margin-top:8px;font-family:'JetBrains Mono',monospace;font-size:8.5px;letter-spacing:.1em;color:var(--emb);line-height:1.6}
.p06 .band{margin-top:14px;padding-top:14px;border-top:1px solid var(--grid);display:grid;grid-template-columns:56fr 44fr;column-gap:28px}
.p06 .band .dash{font-size:11px;margin-bottom:5px}
.p06 .lesson{border-left:2px solid var(--emb);padding:2px 0 2px 18px}
.p06 .lesson .qx{font-family:'Fraunces',serif;font-style:italic;font-weight:500;font-size:15.5px;line-height:1.45;color:var(--ink)}
.p06 .lesson .qx b{color:var(--emb);font-weight:600}
.p06 .lesson .who{margin-top:6px;font-family:'JetBrains Mono',monospace;font-size:7.5px;letter-spacing:.24em;color:var(--dim)}
"""
s=s.replace("</style>",css+"</style>",1)

def gauge(pct_display, pct, label):
    r=27; c=2*math.pi*r; seg=c*pct
    return ('<div class="g1"><svg viewBox="0 0 72 72" style="width:64px;height:64px;margin:0 auto">'
            '<circle cx="36" cy="36" r="%d" fill="none" stroke="#26282C" stroke-width="3.4"/>'
            '<circle cx="36" cy="36" r="%d" fill="none" stroke="#F4603E" stroke-width="4" stroke-linecap="butt" '
            'stroke-dasharray="%.1f %.1f" transform="rotate(-90 36 36)"/>'
            '<text x="36" y="40.5" text-anchor="middle" font-size="12.5" font-weight="700" fill="#F2F1ED">%s</text>'
            '</svg><div class="gl">%s</div></div>')%(r,r,seg,c-seg,pct_display,label)

rows=[("PIPELINE MANAGED","&euro;3M+ ARR",True),
("QUALIFIED MEETINGS","~6 per week",False),
("NEW OPPORTUNITIES","~20 per week",False),
("OUTBOUND REPLY RATE","~20%",False),
("OUTBOUND CONVERSION","7&ndash;8%",False),
("INBOUND CONVERSION","50%+",False)]
tbl="".join('<tr><td class="k">%s</td><td class="v%s">%s</td></tr>'%(k," em" if em else "",v) for k,v,em in rows)

ops="".join('<div class="lg"><span class="n">LOG.%02d</span><span class="c">&#10003;</span>%s</div>'%(i+1,t) for i,t in enumerate([
"Built the company's commercial reporting structure","Implemented forecasting methodology",
"Designed KPI framework","Established pipeline management",
"Standardized outbound methodology","Supported international commercial expansion"]))

tech="".join('<div class="dash">%s</div>'%t for t in [
"Researched prospects automatically","Imported &amp; enriched leads from commercial databases",
"Generated personalized outreach per prospect's business","Automated commercial sequences",
"Continuously improved through feedback &amp; knowledge"])

refl="".join('<div class="dash">%s</div>'%t for t in [
"Differentiate the product earlier against competitors","Accelerate enterprise positioning",
"Invest in strategic partnerships sooner","Expand the AI platform even earlier",
"Build the Israeli operation in parallel with global activity"])

page="""
<!-- ================= PAGE 06 . XTIX EVIDENCE ================= -->
<section class="page casef p06" style="--fc:var(--emb)">
  <span class="brk tl"></span><span class="brk tr"></span><span class="brk bl"></span><span class="brk br"></span>
  <div class="hd">
    <div class="rub"><span class="d"></span>CASE STUDY 01 &middot; XTIX</div>
    <div class="tok">&#10003; EVIDENCE LOGGED</div>
  </div>
  <div class="ttl">Evidence &mdash; From Infrastructure to Execution</div>
  <div class="meta">XTIX &middot; FINTECH SAAS &middot; EARLY-STAGE STARTUP</div>
  <div class="folder">
    <div class="flip"><span class="nm">XTIX</span><span class="fl">FILE 01 &middot; EVIDENCE</span></div>
    <div class="inner">
      <div>
        <div class="zr"><b>A</b><span class="d2"></span>PERFORMANCE</div>
        <table class="tbl">"""+tbl+"""</table>
        <div class="gaug">
"""+gauge("~20%",0.20,"OUTBOUND<br>REPLY RATE")+gauge("7&ndash;8%",0.075,"OUTBOUND<br>CONVERSION")+gauge("50%+",0.50,"INBOUND<br>CONVERSION")+"""
        </div>
      </div>
      <div>
        <div class="zr"><b>B</b><span class="d2"></span>OPERATIONS</div>
        <div class="ops">"""+ops+"""</div>
        <div class="tech">
          <div class="zr" style="margin-bottom:7px"><b>C</b><span class="d2"></span>TECHNOLOGY</div>
          <div class="para">Designed &amp; implemented an internal <b>AI-powered commercial intelligence platform</b> that:</div>
          """+tech+"""
          <div class="pur">PURPOSE: IMPROVE COMMERCIAL DECISION-MAKING WHILE INCREASING EXECUTION CAPACITY.</div>
        </div>
      </div>
    </div>
    <div class="band">
      <div>
        <div class="zr"><b>D</b><span class="d2"></span>REFLECTION &mdash; IF I WERE REBUILDING XTIX TODAY</div>
        """+refl+"""
      </div>
      <div class="lesson">
        <div class="qx">Commercial growth doesn't begin when the first campaign is launched. <b>It begins when the commercial system becomes repeatable.</b></div>
        <div class="who">LESSON &middot; FILE 01 &middot; XTIX</div>
      </div>
    </div>
  </div>
  <div class="ftr">
    <span>THE COMMERCIAL BUILDER</span>
    <span class="mid"><span class="d"></span>CASE STUDY &mdash; XTIX</span>
    <span><b>P.06</b> &mdash; 13</span>
  </div>
</section>
"""
s=s.replace("</body></html>",page+"\n</body></html>")
io.open(p,"w",encoding="utf-8").write(s)
print("page 6 added")
