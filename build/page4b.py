# -*- coding: utf-8 -*-
import io
p="index.html"; s=io.open(p,encoding="utf-8").read()
EM="—"

reality=["No CRM","No Business Development function","No sales methodology","No outbound process",
"No pipeline management","No KPI framework","No reporting structure"]
reality_html="\n".join('            <div class="zi">%s</div>'%i for i in reality)
approach=["Business &amp; product analysis","Market research","Competitive analysis",
"ICP definition","Customer segmentation","Commercial positioning"]
approach_html="\n".join('            <div class="zb">%s</div>'%i for i in approach)
built=["Commercial Strategy","HubSpot CRM Infrastructure","Business Development Process","Sales Pipeline",
"ICP Framework","Outbound Sequences","KPI Framework","Forecasting Structure","Reporting Dashboards","AI-Powered Outbound Engine"]
built_html="\n".join('            <div class="zck"><span class="k">&#10003;</span> %s</div>'%i for i in built)

new=(
'<!-- ============ 04 - CASE STUDY: XTIX (situation/mission/approach/built) ============ -->\n'
'<section class="page">\n'
'  <span class="brk tl"></span><span class="brk tr"></span><span class="brk bl"></span><span class="brk br"></span>\n'
'  <div class="hd"><div class="l">§04 <span>· Case Study 01 / 03</span></div><div class="r">Oran Carmon '+EM+' Building Revenue Engines</div></div>\n'
'  <div class="wrap col">\n'
'    <div class="cs2-top">\n'
'      <div>\n'
'        <div class="eyebrow">Case Study 01</div>\n'
'        <div class="cs2-title">Building a Commercial Function From Zero</div>\n'
'        <div class="cs2-meta"><b>XTIX</b> &#183; FinTech SaaS &#183; Early-Stage Startup</div>\n'
'      </div>\n'
'      <div class="rolebox">\n'
'        <div class="rl">My Role</div>\n'
'        <div class="ri"><span class="ck">&#10003;</span> Builder</div>\n'
'        <div class="ri"><span class="ck">&#10003;</span> Strategist</div>\n'
'        <div class="ri"><span class="ck">&#10003;</span> Operator</div>\n'
'        <div class="ri"><span class="ck">&#10003;</span> Leader</div>\n'
'        <div class="ri"><span class="ck">&#10003;</span> AI Innovator</div>\n'
'      </div>\n'
'    </div>\n'
'    <div class="zones">\n'
'      <div class="zone">\n'
'        <div class="zhead"><span class="zn">01</span><span class="zt">The Situation</span></div>\n'
'        <div class="zp">When I joined XTIX, the company had a strong vision and product &#8212; but <b>no commercial infrastructure</b> to support scalable growth.</div>\n'
'        <div class="zsub">Commercial Reality</div>\n'
'        <div class="zlist">\n'+reality_html+'\n        </div>\n'
'      </div>\n'
'      <div class="zone">\n'
'        <div class="zhead"><span class="zn">02</span><span class="zt">My Mission</span></div>\n'
'        <div class="zp">Design and build a <b>commercial operating system</b> capable of supporting predictable business growth &#8212; starting with the Israeli market and later expanding globally.</div>\n'
'      </div>\n'
'      <div class="zone">\n'
'        <div class="zhead"><span class="zn">03</span><span class="zt">My Approach</span></div>\n'
'        <div class="zp">Rather than launching outbound immediately, I focused on <b>understanding the business first</b>. The first phase included:</div>\n'
'        <div class="zbul">\n'+approach_html+'\n        </div>\n'
'        <div class="zclose">Only then did execution begin.</div>\n'
'      </div>\n'
'      <div class="zone">\n'
'        <div class="zhead"><span class="zn">04</span><span class="zt">What I Built</span></div>\n'
'        <div class="zchecks">\n'+built_html+'\n        </div>\n'
'      </div>\n'
'    </div>\n'
'    <div class="cs2-sig">\n'
'      <div class="sl">Signature Insight</div>\n'
'      <div class="stx">A commercial function shouldn\'t start with outreach. <span class="g">It should start with understanding.</span></div>\n'
'    </div>\n'
'  </div>\n'
'  <div class="ft"><div class="l">Case Study '+EM+' XTIX</div><div class="r"><b>P.04</b> '+EM+' 11</div></div>\n'
'</section>\n\n'
)
a=s.index("<!-- ============ 04 ")
b=s.index("<!-- ============ 05 ")
s=s[:a]+new+s[b:]

css=(
"\n/* ================= CASE STUDY 4-zone (page 04) ================= */\n"
".cs2-top{display:flex;justify-content:space-between;align-items:flex-start;gap:40px}\n"
".cs2-title{font-family:var(--disp);font-weight:800;font-size:25px;letter-spacing:-.02em;color:var(--ink);margin-top:9px;line-height:1.05;max-width:640px}\n"
".cs2-meta{margin-top:11px;font-family:var(--mono);font-size:10px;letter-spacing:.08em;text-transform:uppercase;color:var(--muted2)}\n"
".cs2-meta b{color:var(--acc);font-weight:400}\n"
".zones{display:grid;grid-template-columns:1fr 1fr;gap:14px;margin-top:15px}\n"
".zone{border:1px solid var(--line2);padding:14px 17px 15px}\n"
".zhead{display:flex;align-items:baseline;gap:10px;margin-bottom:10px}\n"
".zhead .zn{font-family:var(--mono);font-size:11px;color:var(--acc);font-weight:700}\n"
".zhead .zt{font-family:var(--disp);font-weight:700;font-size:13px;letter-spacing:.03em;color:var(--ink);text-transform:uppercase}\n"
".zp{color:var(--muted);font-size:11px;line-height:1.5;font-weight:300}\n"
".zp b{color:var(--ink);font-weight:500}\n"
".zsub{font-family:var(--mono);font-size:8.5px;letter-spacing:.14em;text-transform:uppercase;color:var(--muted2);margin:10px 0 8px}\n"
".zlist{display:flex;flex-direction:column;gap:4px}\n"
".zlist .zi{font-family:var(--mono);font-size:10px;color:var(--muted);display:flex;align-items:center;gap:9px;letter-spacing:.02em}\n"
".zlist .zi::before{content:\"\";width:6px;height:1px;background:var(--acc);flex:none}\n"
".zbul{display:flex;flex-direction:column;gap:4px;margin-top:9px}\n"
".zbul .zb{font-size:11px;color:var(--muted);font-weight:300;position:relative;padding-left:13px;line-height:1.35}\n"
".zbul .zb::before{content:\"\";position:absolute;left:0;top:6px;width:4px;height:4px;background:var(--acc)}\n"
".zclose{margin-top:9px;font-family:var(--serif);font-style:italic;font-size:11.5px;color:var(--acc)}\n"
".zchecks{display:grid;grid-template-columns:1fr 1fr;gap:6px 16px;margin-top:2px}\n"
".zck{display:flex;align-items:center;gap:8px;font-size:10.5px;color:var(--ink);font-weight:400}\n"
".zck .k{color:var(--acc);font-size:10px}\n"
".cs2-sig{margin-top:14px;padding-top:13px;border-top:1px solid var(--line)}\n"
".cs2-sig .sl{font-family:var(--mono);font-size:10px;letter-spacing:.2em;text-transform:uppercase;color:var(--acc);margin-bottom:7px}\n"
".cs2-sig .stx{font-family:var(--serif);font-style:italic;font-weight:500;font-size:15px;color:var(--ink);line-height:1.3}\n"
".cs2-sig .stx .g{color:var(--acc)}\n"
)
s=s.replace("</style>", css+"</style>",1)
io.open(p,"w",encoding="utf-8").write(s)
print("page4 rebuilt as 4 zones")
