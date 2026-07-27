# -*- coding: utf-8 -*-
import io, math
p="casebook.html"; s=io.open(p,encoding="utf-8").read()

css="""
/* ============ PAGE 12 - TECHNOLOGY & AI ============ */
.p12 .folder{padding:22px 28px 16px}
.p12 .lead{font-family:'Fraunces',serif;font-style:italic;font-weight:500;font-size:13.5px;line-height:1.5;color:var(--mut)}
.p12 .lead b{color:var(--ink);font-weight:500}
.p12 .stacks{display:grid;grid-template-columns:repeat(4,1fr);column-gap:14px;margin-top:16px}
.p12 .sc{position:relative;border:1px solid var(--grid);border-radius:0 10px 10px 10px;background:var(--card2);padding:26px 13px 11px;margin-top:20px}
.p12 .sc .sl{position:absolute;top:-20px;left:-1px;height:20px;background:var(--emb);border-radius:6px 13px 0 0;
display:flex;align-items:center;padding:0 10px;font-family:'JetBrains Mono',monospace;font-weight:700;font-size:7.5px;letter-spacing:.18em;color:#0C0D10}
.p12 .sc .tools{font-weight:700;font-size:12.5px;letter-spacing:-.01em;color:var(--ink);line-height:1.35;margin-bottom:7px}
.p12 .sc .it{display:flex;align-items:center;gap:7px;font-size:10px;color:var(--mut);margin-bottom:4px}
.p12 .sc .it::before{content:"";flex:none;width:7px;height:1.8px;background:var(--emb)}
.p12 .bot{display:grid;grid-template-columns:38fr 62fr;column-gap:30px;margin-top:16px;padding-top:14px;border-top:1px solid var(--grid)}
.p12 .zr{margin-bottom:8px}
.p12 .lg{margin-bottom:6px;font-size:11px}
.p12 .case2{display:grid;grid-template-columns:1fr 1fr;gap:4px 18px}
.p12 .phil{margin-top:10px;font-family:'JetBrains Mono',monospace;font-size:9px;letter-spacing:.14em;color:var(--emb);line-height:1.7}
.p12 .quote2{margin-top:10px;border-left:2px solid var(--emb);padding:2px 0 2px 16px}
.p12 .quote2 .qx{font-family:'Fraunces',serif;font-style:italic;font-weight:500;font-size:14.5px;line-height:1.45;color:var(--ink)}
.p12 .quote2 .qx b{color:var(--emb);font-weight:600}
.p12 .loopwrap{text-align:center}
.p12 .looplbl{margin-top:2px;font-family:'JetBrains Mono',monospace;font-size:8px;letter-spacing:.18em;color:var(--dim)}
"""
s=s.replace("</style>",css+"</style>",1)

# AI engine loop: 6 nodes on a circle, ember direction arrows
cx,cy,R=130,102,64
labels=["RESEARCH","ENRICH","PERSONALIZE","AUTOMATE","LEARN","IMPROVE"]
els='<circle cx="%d" cy="%d" r="%d" fill="none" stroke="#26282C" stroke-width="1.4"/>'%(cx,cy,R)
for i,lab in enumerate(labels):
    a=math.radians(-90+i*60)
    x,y=cx+R*math.cos(a),cy+R*math.sin(a)
    lx,ly=cx+(R+22)*math.cos(a),cy+(R+22)*math.sin(a)
    anchor="middle"
    if lx<cx-32: anchor="end"
    if lx>cx+32: anchor="start"
    els+='<circle cx="%.1f" cy="%.1f" r="6" fill="#16181C" stroke="#F4603E" stroke-width="1.8"/>'%(x,y)
    els+='<text x="%.1f" y="%.1f" text-anchor="%s" font-size="7" letter-spacing="1.2" fill="#8E8E93">%s</text>'%(lx,ly+2.4,anchor,lab)
    # direction arrow at midpoint between this node and next (tangent direction)
    am=math.radians(-90+i*60+30)
    mx,my=cx+R*math.cos(am),cy+R*math.sin(am)
    rot=math.degrees(am)+90
    els+='<path d="M%.1f %.1f l-4.5 -6.5 h9 z" fill="#F4603E" transform="rotate(%.1f %.1f %.1f)"/>'%(mx,my,rot,mx,my)
els+=('<text x="%d" y="%d" text-anchor="middle" font-size="9.5" font-weight="700" letter-spacing="2" fill="#F2F1ED">AI</text>'
      '<text x="%d" y="%d" text-anchor="middle" font-size="9.5" font-weight="700" letter-spacing="2" fill="#F2F1ED">ENGINE</text>')%(cx,cy-2,cx,cy+10)
loop='<svg viewBox="0 0 260 204" style="width:100%%;max-width:270px;height:auto;margin:0 auto;overflow:visible">%s</svg>'%els

def sc(label,tools,items):
    its="".join('<div class="it">%s</div>'%i for i in items)
    return ('<div class="sc"><div class="sl">%s</div><div class="tools">%s</div>%s</div>')%(label,tools,its)

stacks=(sc("CRM","HubSpot",["Commercial Infrastructure","Pipeline Management","Forecasting","Reporting"])+
sc("AUTOMATION","Zapier &middot; Webhooks",["Google Workspace","API Integrations"])+
sc("AI","GPT &middot; Claude &middot; Gemini",["Custom AI Workflows","Knowledge Base","Lead Intelligence","Personalized Outreach","Continuous Learning"])+
sc("COMMERCIAL DATA","Clay &middot; Apollo &middot; Hunter",["Market Research","Lead Enrichment","Competitive Intelligence"]))

case="".join('<div class="lg"><span class="n">LOG.%02d</span><span class="c">&#10003;</span>%s</div>'%(i+1,t) for i,t in enumerate([
"Researching prospects","Enriching leads","Personalizing outreach","Automating commercial workflows",
"Learning from previous interactions","Improving commercial recommendations over time"]))

page="""
<!-- ================= PAGE 12 . TECHNOLOGY & AI ================= -->
<section class="page casef p12" style="--fc:var(--emb)">
  <span class="brk tl"></span><span class="brk tr"></span><span class="brk bl"></span><span class="brk br"></span>
  <div class="hd">
    <div class="rub"><span class="d"></span>COMMERCIAL TECHNOLOGY &amp; AI</div>
    <div class="tok">SYSTEM FILE &middot; AI</div>
  </div>
  <div class="ttl">How I use technology to improve commercial decisions.</div>
  <div class="meta">CRM &middot; AUTOMATION &middot; AI &middot; COMMERCIAL DATA</div>
  <div class="folder">
    <div class="flip"><span class="nm">Technology</span><span class="fl">SYSTEM FILE &middot; AI</span></div>
    <div class="lead">Technology should never replace commercial thinking &mdash; <b>it should amplify it</b>. Throughout my career, I've used technology to remove repetitive work, improve decision-making and increase execution capacity.</div>
    <div class="stacks">"""+stacks+"""</div>
    <div class="bot">
      <div class="loopwrap">
        """+loop+"""
        <div class="looplbl">CONTINUOUS COMMERCIAL LOOP</div>
      </div>
      <div>
        <div class="zr"><b>AI</b><span class="d2"></span>AI CASE &mdash; INTERNAL COMMERCIAL INTELLIGENCE PLATFORM</div>
        <div class="case2">"""+case+"""</div>
        <div class="phil">MY PHILOSOPHY: TECHNOLOGY SHOULD AUTOMATE EXECUTION. PEOPLE SHOULD MAKE DECISIONS.</div>
        <div class="quote2">
          <div class="qx">AI doesn't replace commercial leaders. <b>It lets them think faster, learn faster and execute at scale.</b></div>
        </div>
      </div>
    </div>
  </div>
  <div class="ftr">
    <span>THE COMMERCIAL BUILDER</span>
    <span class="mid"><span class="d"></span>COMMERCIAL TECHNOLOGY &amp; AI</span>
    <span><b>P.12</b> &mdash; 13</span>
  </div>
</section>
"""
s=s.replace("</body></html>",page+"\n</body></html>")
io.open(p,"w",encoding="utf-8").write(s)
print("page 12 added")
