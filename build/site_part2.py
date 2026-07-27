# -*- coding: utf-8 -*-
# SITE BUILDER PART 2: case files divider + XTIX + OASIS + EVENTER + MEDCOIN
import io, math

CSS = """
/* ============ CASE FILES DIVIDER ============ */
#files .fhead{display:flex;justify-content:space-between;align-items:baseline;flex-wrap:wrap;gap:14px}
#files .bigt{font-weight:800;font-size:clamp(34px,5.4vw,58px);letter-spacing:-.03em;line-height:1;text-transform:uppercase}
#files .fmeta{font-family:'JetBrains Mono',monospace;font-size:10px;letter-spacing:.2em;color:var(--mut)}
#files .stack{margin-top:44px}
#files .tab{position:relative;display:block}
#files .lip{height:38px;border-radius:9px 22px 0 0;display:inline-flex;align-items:center;gap:14px;padding:0 18px;position:relative;top:1px;min-width:230px}
#files .lip .nm{font-family:'Fraunces',serif;font-weight:500;font-size:18px;color:#0C0D10}
#files .lip .fl{margin-left:auto;font-family:'JetBrains Mono',monospace;font-weight:600;font-size:9px;letter-spacing:.16em;color:rgba(12,13,16,.6)}
#files .bod{position:relative;height:58px;border-radius:0 14px 0 0;transition:transform .4s var(--ease)}
#files .tab:last-child .bod{border-radius:0 14px 14px 14px}
#files .cat{position:absolute;right:28px;top:50%;transform:translateY(-50%);font-family:'JetBrains Mono',monospace;font-weight:700;font-size:10px;letter-spacing:.16em;color:rgba(12,13,16,.72)}
#files .tab.open .bod{height:auto;padding:18px 24px 20px}
#files .tab.open .cat{top:20px;transform:none}
#files .dossier{font-family:'JetBrains Mono',monospace;font-size:13px;line-height:1.85;color:rgba(12,13,16,.85)}
#files .tab:hover .bod{transform:translateX(6px)}
@media (max-width:700px){#files .cat{display:none}}

/* ============ CASE SECTIONS SHARED ============ */
.case .folder{margin-top:56px}
.case .cols2{display:grid;grid-template-columns:1fr 1fr;gap:34px}
@media (max-width:900px){.case .cols2{grid-template-columns:1fr}}
.case .z{margin-bottom:22px}
.case .list>*{margin-bottom:9px}
.case .grid2c{display:grid;grid-template-columns:1fr 1fr;gap:9px 22px}
@media (max-width:640px){.case .grid2c{grid-template-columns:1fr}}
.case .hairtop{margin-top:26px;padding-top:24px;border-top:1px solid var(--grid)}
.case .reality{border:1px solid var(--grid);border-radius:12px;padding:16px 18px;background:var(--card2)}
.case .subl{display:block;font-family:'JetBrains Mono',monospace;font-weight:600;font-size:9px;letter-spacing:.24em;color:var(--dim);margin-bottom:12px}
.case .then{margin-top:12px;font-family:'Fraunces',serif;font-style:italic;font-size:15px;color:var(--fc)}
.case .statrow{display:flex;gap:40px;flex-wrap:wrap;align-items:flex-end}
.case .bignum{font-weight:800;letter-spacing:-.02em;line-height:1;font-size:clamp(38px,5.5vw,62px)}
.case .bignum .cur{color:var(--fc)}
.case .biglbl{margin-top:8px;font-family:'JetBrains Mono',monospace;font-size:8.5px;letter-spacing:.22em;color:var(--dim)}
.case .gaug{display:flex;gap:34px;flex-wrap:wrap}
.case .g1{text-align:center}
.case .g1 .gl{margin-top:6px;font-family:'JetBrains Mono',monospace;font-size:8px;letter-spacing:.14em;color:var(--dim);line-height:1.7}
.garc{stroke-dasharray:var(--seg) var(--gap);stroke-dashoffset:var(--seg);transition:stroke-dashoffset 1.6s var(--ease) .25s}
.sec.on .garc,body.static .garc{stroke-dashoffset:0}
.bar0{transform:scaleY(0);transform-box:fill-box;transform-origin:bottom;transition:transform .8s var(--ease);transition-delay:calc(var(--i,0)*60ms)}
.sec.on .bar0,body.static .bar0{transform:scaleY(1)}
.pdraw{stroke-dasharray:1;stroke-dashoffset:1;transition:stroke-dashoffset 1.5s var(--ease);transition-delay:calc(var(--i,0)*180ms)}
.sec.on .pdraw,body.static .pdraw{stroke-dashoffset:0}
.ndot{opacity:0;transform:scale(.4);transform-box:fill-box;transform-origin:center;transition:all .55s var(--ease);transition-delay:calc(var(--i,0)*140ms)}
.sec.on .ndot,body.static .ndot{opacity:1;transform:scale(1)}
.case .tech{border:1px solid var(--grid);border-radius:12px;background:var(--card2);padding:18px 20px}
.case .pur{margin-top:12px;font-family:'JetBrains Mono',monospace;font-size:9px;letter-spacing:.12em;color:var(--fc);line-height:1.7}
.case .chips{display:flex;flex-wrap:wrap;gap:10px}
.case .chip{flex:1;min-width:130px;border:1px solid var(--grid);border-radius:9px;padding:12px 10px;text-align:center;
font-family:'JetBrains Mono',monospace;font-weight:600;font-size:8.6px;letter-spacing:.1em;color:var(--mut);line-height:1.6}
.case .chip b{display:block;color:var(--fc);font-size:9.6px;letter-spacing:.16em;margin-bottom:4px}
.case .insight{text-align:center;margin-top:34px}
.case .insight .qx{font-family:'Fraunces',serif;font-style:italic;font-weight:500;font-size:clamp(17px,2.4vw,22px)}
.case .insight .qx b{color:var(--fc)}
.case .insight .who{margin-top:7px;font-family:'JetBrains Mono',monospace;font-size:8px;letter-spacing:.26em;color:var(--dim)}
.case .stat{border:1px solid var(--grid);border-radius:0 14px 14px 14px;background:var(--card2);position:relative;margin-top:26px;padding:22px 24px;width:max-content;max-width:100%}
.case .stat .slip{position:absolute;top:-26px;left:-1px;height:26px;background:var(--fc);border-radius:7px 15px 0 0;
display:flex;align-items:center;padding:0 13px;font-family:'JetBrains Mono',monospace;font-weight:700;font-size:8px;letter-spacing:.2em;color:#0C0D10}
.ringlbl,.looplbl{margin-top:8px;font-family:'JetBrains Mono',monospace;font-size:8.5px;letter-spacing:.18em;color:var(--dim);text-align:center}

/* ============ MEDCOIN PAPER ============ */
#medcoin{background:#F2F1ED}
#medcoin .rub,#medcoin .sttl{color:#0C0D10}
#medcoin .smeta{color:rgba(12,13,16,.55)}
#medcoin .tok{border-color:rgba(12,13,16,.22);color:#0C0D10}
#medcoin .folder{background:rgba(12,13,16,.045);border-color:rgba(12,13,16,.16)}
#medcoin .flip{background:#0C0D10}
#medcoin .flip .nm{color:#F2F1ED}
#medcoin .flip .fl{color:rgba(242,241,237,.6)}
#medcoin .zr{color:#0C0D10}
#medcoin .para{color:rgba(12,13,16,.68)}
#medcoin .para b{color:#0C0D10}
#medcoin .lg{color:#0C0D10}
#medcoin .lg .c{color:#F2F1ED}
#medcoin .hairtop{border-color:rgba(12,13,16,.14)}
#medcoin .outs{position:relative;border:1px solid rgba(12,13,16,.16);border-radius:12px;background:#F2F1ED;padding:6px 20px 8px}
#medcoin .outs table{width:100%;border-collapse:collapse}
#medcoin .outs td{border-top:1px solid rgba(12,13,16,.12);padding:10px 0;vertical-align:middle}
#medcoin .outs tr:first-child td{border-top:none}
#medcoin .outs .k{font-family:'JetBrains Mono',monospace;font-size:8.5px;letter-spacing:.16em;color:rgba(12,13,16,.5)}
#medcoin .outs .v{text-align:right;font-weight:700;font-size:13.5px;color:#0C0D10}
#medcoin .outs .v.em{color:#F4603E}
#medcoin .stamp{position:absolute;top:-16px;right:16px;transform:rotate(-7deg);border:2px solid #F4603E;border-radius:6px;
padding:6px 13px;font-family:'JetBrains Mono',monospace;font-weight:700;font-size:12px;letter-spacing:.3em;color:#F4603E;background:#F2F1ED}
#medcoin .lessq{border-color:#F4603E}
#medcoin .lessq .qx{color:#0C0D10}
#medcoin .lessq .who{color:rgba(12,13,16,.5)}
#medcoin .insight .who{color:rgba(12,13,16,.5)}
"""

def gauge(disp,pct,label,color="#F4603E"):
    r=30; c=2*math.pi*r; seg=c*pct
    return ('<div class="g1"><svg viewBox="0 0 80 80" style="width:76px;height:76px;margin:0 auto">'
            '<circle cx="40" cy="40" r="%d" fill="none" stroke="#26282C" stroke-width="3.6"/>'
            '<circle class="garc" cx="40" cy="40" r="%d" fill="none" stroke="%s" stroke-width="4.2" '
            'style="--seg:%.1f;--gap:%.1f" transform="rotate(-90 40 40)"/>'
            '<text x="40" y="45" text-anchor="middle" font-size="13.5" font-weight="700" fill="#F2F1ED">%s</text>'
            '</svg><div class="gl">%s</div></div>')%(r,r,color,seg,c-seg,disp,label)

def lg(n,t): return '<div class="lg"><span class="n">LOG.%02d</span><span class="c">&#10003;</span>%s</div>'%(n,t)
def dash(t): return '<div class="dash">%s</div>'%t
def mi(t): return '<div class="mi"><span class="o"></span>%s</div>'%t

# ---------- from-zero bars ----------
bars=""; x=8
for i in range(3):
    bars+='<rect x="%d" y="50" width="30" height="13" fill="none" stroke="#3A3D43" stroke-width="1.3" stroke-dasharray="3 3"/>'%x
    x+=44
bars+='<line x1="%d" y1="8" x2="%d" y2="63" stroke="#3A3D43" stroke-width="1" stroke-dasharray="2 4"/>'%(x+2,x+2)
x+=18
for i,hh in enumerate([15,20,25,30,35,40,45,50,55,60]):
    bars+='<rect class="bar0" style="--i:%d" x="%d" y="%d" width="30" height="%d" fill="#F4603E"/>'%(i,x,63-hh,hh)
    x+=44
fromzero=('<svg viewBox="0 0 740 70" preserveAspectRatio="none" style="width:100%%;height:74px">'
          '<line x1="0" y1="63" x2="740" y2="63" stroke="#26282C" stroke-width="1.3"/>%s</svg>')%bars

# ---------- XTIX ----------
reality="".join(mi(t) for t in ["No CRM","No Business Development function","No sales methodology","No outbound process","No pipeline management","No KPI framework","No reporting structure"])
approach="".join(dash(t) for t in ["Business &amp; product analysis","Market research","Competitive analysis","ICP definition","Customer segmentation","Commercial positioning"])
xbuilt="".join(lg(i+1,t) for i,t in enumerate(["Commercial Strategy","HubSpot CRM Infrastructure","Business Development Process","Sales Pipeline","ICP Framework","Outbound Sequences","KPI Framework","Forecasting Structure","Reporting Dashboards","AI-Powered Outbound Engine"]))
ops="".join(lg(i+1,t) for i,t in enumerate(["Built the company's commercial reporting structure","Implemented forecasting methodology","Designed KPI framework","Established pipeline management","Standardized outbound methodology","Supported international commercial expansion"]))
tech="".join(dash(t) for t in ["Researched prospects automatically","Imported &amp; enriched leads from commercial databases","Generated personalized outreach per prospect's business","Automated commercial sequences","Continuously improved through feedback &amp; knowledge"])
refl="".join(dash(t) for t in ["Differentiate the product earlier against competitors","Accelerate enterprise positioning","Invest in strategic partnerships sooner","Expand the AI platform even earlier","Build the Israeli operation in parallel with global activity"])

XTIX = """
<section class="sec case" id="xtix" style="--fc:var(--emb)">
  <div class="wrap">
    <div class="shead rv" style="--i:0">
      <div class="rub"><span class="d"></span>CASE STUDY 01</div>
      <div class="tok">FILE 01 &middot; INTAKE</div>
    </div>
    <div class="sttl rv" style="--i:1">Building a Commercial Function From Zero</div>
    <div class="smeta rv" style="--i:2">XTIX &middot; FINTECH SAAS &middot; EARLY-STAGE STARTUP</div>
    <div class="folder rv" style="--i:3">
      <div class="flip"><span class="nm">XTIX</span><span class="fl">FILE 01</span></div>
      <div class="cols2">
        <div>
          <div class="z"><div class="zr"><b>01</b><span class="d2"></span>THE SITUATION</div>
            <div class="para">When I joined XTIX, the company had a <b>strong vision and product</b> &mdash; but no commercial infrastructure to support scalable growth.</div></div>
          <div class="reality rv" style="--i:2"><span class="subl">COMMERCIAL REALITY &middot; MISSING AT INTAKE</span>
            <div class="grid2c">"""+reality+"""</div></div>
          <div class="z" style="margin-top:22px"><div class="zr"><b>02</b><span class="d2"></span>MY MISSION</div>
            <div class="para">Design and build a <b>commercial operating system</b> capable of supporting predictable business growth &mdash; starting with the Israeli market and later expanding globally.</div></div>
        </div>
        <div>
          <div class="z"><div class="zr"><b>03</b><span class="d2"></span>MY APPROACH</div>
            <div class="para">Rather than launching outbound immediately, I focused on <b>understanding the business first</b>. The first phase included:</div>
            <div class="grid2c" style="margin-top:12px">"""+approach+"""</div>
            <div class="then">Only then did execution begin.</div></div>
          <div class="z" style="margin-bottom:0"><div class="zr"><b>04</b><span class="d2"></span>WHAT I BUILT</div>
            <div class="grid2c">"""+xbuilt+"""</div></div>
        </div>
      </div>
      <div class="hairtop rv">
        <div class="zr"><b>&#8709;&#8594;10</b><span class="d2"></span>FROM ZERO &mdash; INFRASTRUCTURE BUILD-UP</div>
        """+fromzero+"""
      </div>
      <div class="hairtop">
        <div class="zr rv"><b>A</b><span class="d2"></span>EVIDENCE &mdash; FROM INFRASTRUCTURE TO EXECUTION</div>
        <div class="statrow" style="margin-top:18px">
          <div class="rv" style="--i:1"><div class="bignum"><span class="cur">&euro;</span><span class="cnt" data-n="3" data-suf="M+">0M+</span> <span style="font-size:.45em;color:var(--mut);font-weight:700">ARR</span></div><div class="biglbl">PIPELINE MANAGED</div></div>
          <div class="rv" style="--i:2"><div class="bignum">~<span class="cnt" data-n="6">0</span></div><div class="biglbl">QUALIFIED MEETINGS / WEEK</div></div>
          <div class="rv" style="--i:3"><div class="bignum">~<span class="cnt" data-n="20">0</span></div><div class="biglbl">NEW OPPORTUNITIES / WEEK</div></div>
        </div>
        <div class="cols2" style="margin-top:30px">
          <div class="rv" style="--i:4">
            <div class="gaug">
"""+gauge("~20%",0.20,"OUTBOUND<br>REPLY RATE")+gauge("7&ndash;8%",0.075,"OUTBOUND<br>CONVERSION")+gauge("50%+",0.50,"INBOUND<br>CONVERSION")+"""
            </div>
            <div class="z" style="margin-top:26px"><div class="zr"><b>B</b><span class="d2"></span>OPERATIONS</div>
              <div class="list">"""+ops+"""</div></div>
          </div>
          <div class="rv" style="--i:5">
            <div class="tech">
              <div class="zr"><b>C</b><span class="d2"></span>TECHNOLOGY</div>
              <div class="para">Designed &amp; implemented an internal <b>AI-powered commercial intelligence platform</b> that:</div>
              <div class="list" style="margin-top:10px">"""+tech+"""</div>
              <div class="pur">PURPOSE: IMPROVE COMMERCIAL DECISION-MAKING WHILE INCREASING EXECUTION CAPACITY.</div>
            </div>
          </div>
        </div>
      </div>
      <div class="hairtop cols2">
        <div class="rv"><div class="zr"><b>D</b><span class="d2"></span>REFLECTION &mdash; IF I WERE REBUILDING XTIX TODAY</div>
          <div class="list">"""+refl+"""</div></div>
        <div class="lessq rv" style="--i:1">
          <div class="qx">Commercial growth doesn't begin when the first campaign is launched. <b>It begins when the commercial system becomes repeatable.</b></div>
          <div class="who">LESSON &middot; FILE 01 &middot; XTIX</div>
        </div>
      </div>
    </div>
  </div>
</section>
"""

# ---------- OASIS ----------
resp="".join(dash(t) for t in ["Recruiting &amp; building the sales team","Defining commercial strategy","Pricing model development","KPI design","Sales methodology","Forecasting","Commercial reviews","Cross-functional leadership","Profitability management"])
obuilt="".join(lg(i+1,t) for i,t in enumerate(["Recruited &amp; onboarded the entire sales team","Built the pricing model from scratch","Designed the commercial process","Implemented KPI framework","Created sales playbooks &amp; onboarding","Established weekly business reviews","Built forecasting methodology","Created cross-functional collaboration"]))
chips="".join('<div class="chip"><b>%s</b>%s</div>'%(k,t) for k,t in [("WEEKLY","COACHING SESSIONS"),("MONTHLY","1:1 PERFORMANCE REVIEWS"),("QUARTERLY","BUSINESS REVIEWS"),("LIVE","DEAL REVIEWS"),("ALWAYS","COMMERCIAL COACHING"),("CROSS-FN","COLLABORATION"),("OWNED","OWNERSHIP &amp; ACCOUNTABILITY")])
olead="".join(lg(i+1,t) for i,t in enumerate(["Recruited an entire sales team","Led a team of 5&ndash;6 sales professionals","Conducted weekly coaching sessions","Established KPI-driven management","Built onboarding documentation","Standardized commercial processes"]))
operf="".join(dash(t) for t in ["Built pricing strategy from zero","Introduced profitability-based pricing","Defined company-wide commercial KPIs","Improved cross-department collaboration","Created structured commercial reporting"])

cx,cy,R=130,104,64
fns=["OPERATIONS","PRODUCTION","CUSTOMER SUCCESS","FINANCE","MARKETING","TECHNICAL TEAMS"]
nodes=""
for i,f in enumerate(fns):
    a=math.radians(-90+i*60)
    xx,yy=cx+R*math.cos(a),cy+R*math.sin(a)
    lx,ly=cx+(R+26)*math.cos(a),cy+(R+26)*math.sin(a)
    anchor="middle"
    if lx<cx-32: anchor="end"
    if lx>cx+32: anchor="start"
    nodes+='<line x1="%.1f" y1="%.1f" x2="%.1f" y2="%.1f" stroke="#3A3D43" stroke-width="1"/>'%(cx+20*math.cos(a),cy+20*math.sin(a),xx-8*math.cos(a),yy-8*math.sin(a))
    nodes+='<circle class="ndot" style="--i:%d" cx="%.1f" cy="%.1f" r="6" fill="#121316" stroke="#E0A458" stroke-width="1.7"/>'%(i,xx,yy)
    nodes+='<text x="%.1f" y="%.1f" text-anchor="%s" font-size="7.4" letter-spacing="1" fill="#8E8E93">%s</text>'%(lx,ly+2.6,anchor,f)
ring=('<svg viewBox="0 0 260 210" style="width:100%%;max-width:280px;height:auto;margin:0 auto;overflow:visible">'
      '<circle class="pdraw" pathLength="1" cx="%d" cy="%d" r="%d" fill="none" stroke="#26282C" stroke-width="1.3"/>'
      '<circle cx="%d" cy="%d" r="20" fill="#16181C" stroke="#E0A458" stroke-width="2"/>'
      '<text x="%d" y="%d" text-anchor="middle" font-size="9" font-weight="700" letter-spacing="1.5" fill="#F2F1ED">CEO</text>%s</svg>')%(cx,cy,R,cx,cy,cx,cy+3,nodes)

OASIS = """
<section class="sec case" id="oasis" style="--fc:var(--brass)">
  <div class="wrap">
    <div class="shead rv" style="--i:0">
      <div class="rub"><span class="d"></span>CASE STUDY 02</div>
      <div class="tok">FILE 02 &middot; COMMAND</div>
    </div>
    <div class="sttl rv" style="--i:1">Building Leaders, Not Just Sales Teams</div>
    <div class="smeta rv" style="--i:2">OASIS &middot; CEO &middot; CONSTRUCTION &amp; SMART BUILDING SOLUTIONS</div>
    <div class="folder rv" style="--i:3">
      <div class="flip"><span class="nm">Oasis</span><span class="fl">FILE 02</span></div>
      <div class="cols2">
        <div>
          <div class="z"><div class="zr"><b>01</b><span class="d2"></span>THE SITUATION</div>
            <div class="para">As CEO, my responsibility extended far beyond sales. The objective wasn't simply to increase revenue &mdash; it was to build a <b>profitable, scalable commercial organization</b> capable of supporting the company's long-term vision.</div></div>
          <div class="z" style="margin-bottom:0"><div class="zr"><b>02</b><span class="d2"></span>MY RESPONSIBILITIES</div>
            <div class="grid2c">"""+resp+"""</div></div>
        </div>
        <div>
          <div class="zr"><b>03</b><span class="d2"></span>COMMERCIAL SYSTEM BUILT</div>
          <div class="list">"""+obuilt+"""</div>
        </div>
      </div>
      <div class="hairtop rv">
        <div class="zr"><b>04</b><span class="d2"></span>LEADERSHIP MODEL</div>
        <div class="chips">"""+chips+"""</div>
        <div class="insight"><div class="qx">High-performing sales teams aren't built by pressure. <b>They're built by clarity.</b></div>
        <div class="who">SIGNATURE INSIGHT &middot; FILE 02 &middot; OASIS</div></div>
      </div>
      <div class="hairtop">
        <div class="zr rv"><b>A</b><span class="d2"></span>EVIDENCE &mdash; COMMERCIAL RESULTS</div>
        <div class="cols2" style="margin-top:6px">
          <div>
            <div class="stat rv" style="--i:1">
              <div class="slip">EVIDENCE &middot; KEY DEAL</div>
              <div class="bignum"><span class="cur">&#8362;</span><span class="cnt" data-n="2" data-suf="M">0M</span></div>
              <div class="biglbl">LARGEST DEAL CLOSED</div>
            </div>
            <div class="list" style="margin-top:20px">"""+operf+"""</div>
            <div class="z" style="margin-top:22px"><div class="zr"><b>B</b><span class="d2"></span>COMMERCIAL LEADERSHIP</div>
              <div class="list">"""+olead+"""</div></div>
          </div>
          <div class="rv" style="--i:2;text-align:center">
            <div class="zr" style="justify-content:center"><b>C</b><span class="d2"></span>CROSS-FUNCTIONAL LEADERSHIP</div>
            """+ring+"""
            <div class="ringlbl">WORKED CLOSELY WITH &middot; 06 FUNCTIONS</div>
          </div>
        </div>
      </div>
      <div class="hairtop cols2">
        <div class="rv"><div class="zr"><b>D</b><span class="d2"></span>REFLECTION &mdash; LOOKING BACK</div>
          <div class="para">The biggest lesson I learned as CEO wasn't about selling &mdash; it was about <b>leadership</b>. The more I tried to manage every function myself, the less scalable the organization became. Real leadership begins when leaders build systems that let others succeed <b>without depending on them</b>.</div></div>
        <div class="lessq rv" style="--i:1">
          <div class="qx">Organizations don't scale because leaders work harder. <b>They scale because leaders create clarity, ownership and trust.</b></div>
          <div class="who">LESSON &middot; FILE 02 &middot; OASIS</div>
        </div>
      </div>
    </div>
  </div>
</section>
"""

# ---------- EVENTER ----------
contrib="".join(lg(i+1,t) for i,t in enumerate(["Managed &amp; coached Business Development team members","Participated in recruiting commercial talent","Improved commercial processes","Introduced new business initiatives","Worked closely with Product, Marketing, Finance &amp; R&amp;D","Brought customer feedback directly into product discussions","Helped improve commercial alignment across the organization"]))
depts=["PRODUCT","MARKETING","FINANCE","R&amp;D","BUSINESS DEVELOPMENT"]
rows=""; y=14
for i,d in enumerate(depts):
    em=(i==4)
    col="#7CC4E8" if em else "#3A3D43"
    tcol="#F2F1ED" if em else "#8E8E93"
    fill="rgba(124,196,232,.12)" if em else "#16181C"
    w=150
    rows+=('<rect x="4" y="%d" width="%d" height="22" rx="6" fill="%s" stroke="%s" stroke-width="1.3"/>'
           '<text x="%.1f" y="%.1f" text-anchor="middle" font-size="7.2" letter-spacing="1.2" fill="%s">%s</text>'
           '<path class="pdraw" style="--i:%d" pathLength="1" d="M%d %.1f C 240 %.1f, 270 86, 344 86" fill="none" stroke="%s" stroke-width="1.5"/>'
           )%(y,w,fill,col,4+w/2,y+14.4,tcol,d,i,4+w,y+11.0,y+11.0,col)
    y+=32
conv=('<svg viewBox="0 0 580 178" style="width:100%;height:auto">'
      +rows+
      '<path d="M348 86 l-8 -4.5 v9 z" fill="#7CC4E8"/>'
      '<circle cx="410" cy="86" r="34" fill="#16181C" stroke="#7CC4E8" stroke-width="2.2"/>'
      '<text x="410" y="83" text-anchor="middle" font-size="8.6" font-weight="700" letter-spacing="1.4" fill="#F2F1ED">THE</text>'
      '<text x="410" y="95" text-anchor="middle" font-size="8.6" font-weight="700" letter-spacing="1.4" fill="#F2F1ED">CUSTOMER</text>'
      '<path class="pdraw" style="--i:5" pathLength="1" d="M444 70 C 496 34, 436 6, 260 6 L 176 6" fill="none" stroke="#8E8E93" stroke-width="1.1" stroke-dasharray="3 4"/>'
      '<path d="M168 6 l9 -4.5 v9 z" fill="#8E8E93"/>'
      '<text x="308" y="22" text-anchor="middle" font-size="6.8" letter-spacing="1.6" fill="#5A5B60">CUSTOMER INSIGHT &#8594; BUSINESS DECISIONS</text>'
      '<text x="410" y="140" text-anchor="middle" font-size="6.8" letter-spacing="1.4" fill="#5A5B60">SHARED RESPONSIBILITY</text>'
      '</svg>')

EVENTER = """
<section class="sec case" id="eventer" style="--fc:var(--ice)">
  <div class="wrap">
    <div class="shead rv" style="--i:0">
      <div class="rub"><span class="d"></span>CASE STUDY 03</div>
      <div class="tok">FILE 03 &middot; SYNC</div>
    </div>
    <div class="sttl rv" style="--i:1">Aligning Commercial Execution Across Teams</div>
    <div class="smeta rv" style="--i:2">EVENTER &middot; SAAS &middot; EVENT MANAGEMENT PLATFORM</div>
    <div class="folder rv" style="--i:3">
      <div class="flip"><span class="nm">Eventer</span><span class="fl">FILE 03</span></div>
      <div class="cols2">
        <div>
          <div class="z"><div class="zr"><b>01</b><span class="d2"></span>THE SITUATION</div>
            <div class="para">Eventer already had an <b>existing commercial operation</b>. Unlike previous roles, the objective wasn't to build a department from scratch &mdash; it was to improve execution, strengthen collaboration between departments and identify new commercial growth opportunities.</div></div>
          <div class="z"><div class="zr"><b>02</b><span class="d2"></span>MY ROLE</div>
            <div class="para">I worked across multiple business functions to improve commercial performance by <b>connecting business strategy with day-to-day execution</b>.</div></div>
          <div class="z" style="margin-bottom:0"><div class="zr"><b>03</b><span class="d2"></span>CROSS-FUNCTIONAL IMPACT</div>
            <div class="para">Rather than focusing only on Business Development, I worked closely with multiple departments to ensure customer insights translated into business decisions. Commercial growth became a <b>shared organizational responsibility</b> &mdash; not just a sales target.</div></div>
        </div>
        <div>
          <div class="zr rv"><b>04</b><span class="d2"></span>ORGANIZATIONAL CONVERGENCE</div>
          <div class="rv" style="--i:1">"""+conv+"""</div>
          <div class="zr" style="margin-top:16px"><b>05</b><span class="d2"></span>KEY CONTRIBUTIONS</div>
          <div class="list">"""+contrib+"""</div>
        </div>
      </div>
      <div class="hairtop cols2">
        <div class="rv"><div class="zr"><b>06</b><span class="d2"></span>WHAT I LEARNED</div>
          <div class="para">Leadership doesn't always require authority. Some of the biggest organizational changes happen through <b>influence, collaboration and better decision-making</b>.</div></div>
        <div class="lessq rv" style="--i:1">
          <div class="qx">Commercial growth accelerates when every department understands the customer &mdash; <b>not only Sales.</b></div>
          <div class="who">SIGNATURE INSIGHT &middot; FILE 03 &middot; EVENTER</div>
        </div>
      </div>
    </div>
  </div>
</section>
"""

# ---------- MEDCOIN ----------
mbuilt="".join('<div class="lg"><span class="c">&#10003;</span>%s</div>'%t for t in ["Founded the company from scratch","Defined the business model","Built the commercial strategy","Established strategic partnerships","Raised external investment","Deployed cryptocurrency ATMs across Europe","Built operational &amp; regulatory processes","Managed financial-service providers &amp; international vendors","Designed the customer journey &amp; user experience"])
outs="".join('<tr><td class="k">%s</td><td class="v%s">%s</td></tr>'%(k," em" if em else "",v) for k,v,em in [
("MARKETS","Europe",False),("BUSINESS MODEL","Crypto ATM network",False),("INVESTMENT","External investment raised",False),
("REVENUE","Hundreds of thousands of &euro;",True),("INFRASTRUCTURE","Operational ATM network deployed",False),("TEAM","Founder-led operation",False)])
ms=[("FOUNDED",44),("BUSINESS MODEL",262),("PARTNERSHIPS",480),("INVESTMENT RAISED",698),("ATMs ACROSS EUROPE",916)]
nodes2=""
for i,(t,xx) in enumerate(ms):
    last=(i==4)
    nodes2+=('<circle class="ndot" style="--i:%d" cx="%d" cy="26" r="%s" fill="%s" stroke="#0C0D10" stroke-width="1.6"/>'
             '<text x="%d" y="54" text-anchor="middle" font-size="7.6" letter-spacing="1.3" fill="rgba(12,13,16,.6)">%s</text>')%(i,xx,"7" if last else "5","#F4603E" if last else "#F2F1ED",xx,t)
tline=('<svg viewBox="0 0 1060 60" style="width:100%;height:auto">'
       '<line class="pdraw" pathLength="1" x1="30" y1="26" x2="930" y2="26" stroke="#0C0D10" stroke-width="1.5"/>'
       '<line x1="930" y1="26" x2="1032" y2="26" stroke="#F4603E" stroke-width="2" stroke-dasharray="4 4"/>'
       '<path d="M1040 26 l-9 -5 v10 z" fill="#F4603E"/>'
       +nodes2+
       '<text x="986" y="12" text-anchor="middle" font-size="7.8" font-weight="700" letter-spacing="1.5" fill="#F4603E">REVENUE</text>'
       '</svg>')

MEDCOIN = """
<section class="sec case" id="medcoin" style="--fc:#F4603E">
  <div class="wrap">
    <div class="shead rv" style="--i:0">
      <div class="rub"><span class="d"></span>FOUNDER CASE STUDY</div>
      <div class="tok">FILE 04 &middot; ORIGIN</div>
    </div>
    <div class="sttl rv" style="--i:1">Building a Business From Vision</div>
    <div class="smeta rv" style="--i:2">MEDCOIN TEKNOLOJI &middot; CRYPTO FINTECH &middot; FOUNDER</div>
    <div class="folder rv" style="--i:3">
      <div class="flip"><span class="nm">Medcoin</span><span class="fl">FILE 04</span></div>
      <div class="cols2">
        <div>
          <div class="z"><div class="zr"><b>01</b><span class="d2"></span>THE VISION</div>
            <div class="para">Create a <b>compliant, scalable cryptocurrency ATM business</b> serving the European market through secure, accessible digital financial services.</div></div>
          <div class="z"><div class="zr"><b>02</b><span class="d2"></span>THE CHALLENGE</div>
            <div class="para">Building a company from zero meant making <b>every strategic decision</b> &mdash; from business model and partnerships to compliance, operations and commercialization.</div></div>
          <div class="z" style="margin-bottom:0"><div class="zr"><b>03</b><span class="d2"></span>WHAT WE BUILT</div>
            <div class="list">"""+mbuilt+"""</div></div>
        </div>
        <div>
          <div class="zr rv"><b>04</b><span class="d2"></span>BUSINESS OUTCOMES</div>
          <div class="outs rv" style="--i:1">
            <div class="stamp">FOUNDER</div>
            <table>"""+outs+"""</table>
          </div>
        </div>
      </div>
      <div class="hairtop rv">
        <div class="zr"><b>05</b><span class="d2"></span>THE ORIGIN LINE</div>
        """+tline+"""
      </div>
      <div class="hairtop cols2">
        <div class="rv"><div class="zr"><b>06</b><span class="d2"></span>WHAT I LEARNED</div>
          <div class="para">Being a founder changes how you think. Every commercial decision affects operations. Every operational decision affects profitability. Every strategic decision affects survival. Leading a company taught me that <b>commercial leadership is ultimately business leadership</b>.</div></div>
        <div class="lessq rv" style="--i:1">
          <div class="qx">Founders don't manage functions. <b>They align the entire business around one vision.</b></div>
          <div class="who">LESSON &middot; FILE 04 &middot; MEDCOIN</div>
        </div>
      </div>
    </div>
  </div>
</section>
"""

FILES = """
<section class="sec" id="files">
  <div class="wrap">
    <div class="fhead rv" style="--i:0">
      <div class="bigt">The Case<br>Files</div>
      <div class="fmeta">EXECUTIVE CASEBOOK &middot; 04 DOSSIERS &middot; 2018&ndash;2026</div>
    </div>
    <div class="stack">
      <a class="tab open rv" style="--i:1" href="#xtix">
        <div class="lip" style="background:var(--emb);width:270px"><span class="nm">XTIX</span><span class="fl">FILE 01</span></div>
        <div class="bod" style="background:var(--emb)"><div class="cat">BUILT FROM ZERO &#8250;</div>
          <div class="dossier">&gt; commercial function: none &rarr; operating system<br>&gt; pipeline: &euro;0 &rarr; &euro;3M+ ARR &middot; 7 enterprise closed</div></div>
      </a>
      <a class="tab rv" style="--i:2" href="#oasis">
        <div class="lip" style="background:var(--brass);width:320px;margin-left:46px"><span class="nm">Oasis</span><span class="fl">FILE 02</span></div>
        <div class="bod" style="background:var(--brass)"><div class="cat">LEADERSHIP &#8250;</div></div>
      </a>
      <a class="tab rv" style="--i:3" href="#eventer">
        <div class="lip" style="background:var(--ice);width:370px;margin-left:92px"><span class="nm">Eventer</span><span class="fl">FILE 03</span></div>
        <div class="bod" style="background:var(--ice)"><div class="cat">ALIGNMENT &#8250;</div></div>
      </a>
      <a class="tab rv" style="--i:4" href="#medcoin">
        <div class="lip" style="background:var(--ink);width:420px;margin-left:138px"><span class="nm">Medcoin</span><span class="fl">FILE 04</span></div>
        <div class="bod" style="background:var(--ink)"><div class="cat">FOUNDER &#8250;</div></div>
      </a>
    </div>
  </div>
</section>
"""

s = io.open("site.html", encoding="utf-8").read()
block = "<style>"+CSS+"</style>\n"+FILES+XTIX+OASIS+EVENTER+MEDCOIN+"\n<!--MORE-->"
s = s.replace("<!--MORE-->", block, 1)
io.open("site.html","w",encoding="utf-8").write(s)
print("site part 2 appended:", len(block), "bytes")
