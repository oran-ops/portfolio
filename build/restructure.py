# -*- coding: utf-8 -*-
import io
p="index.html"
s=io.open(p,encoding="utf-8").read()
EM="—"

# 1) remove OS(04) + old XTIX(05): from OS comment up to OASIS comment
a=s.index("<!-- ============ 04 ")
b=s.index("<!-- ============ 06 ")
s=s[:a]+s[b:]

infra=["Commercial Strategy","CRM Architecture (HubSpot)","Business Development Process",
"Pipeline Management","Sales Sequences","ICP Definition","Market Research","Competitor Analysis",
"KPI Framework","Forecasting","Reporting Dashboards","AI-powered Outbound Engine"]
checks="\n".join('          <div class="cs-check"><span class="ck">&#10003;</span> %s</div>'%i for i in infra)

xtix=(
'<!-- ============ 04 - CASE STUDY: XTIX ============ -->\n'
'<section class="page">\n'
'  <span class="brk tl"></span><span class="brk tr"></span><span class="brk bl"></span><span class="brk br"></span>\n'
'  <div class="hd"><div class="l">§04 <span>· Case Study 01 / 03</span></div><div class="r">Oran Carmon '+EM+' Building Revenue Engines</div></div>\n'
'  <div class="wrap col">\n'
'    <div class="cs-top">\n'
'      <div class="cs-topL">\n'
'        <div class="eyebrow">Case Study 01</div>\n'
'        <div class="cs-title">Building a Commercial Function From Zero</div>\n'
'        <div class="cs-co-row">\n'
'          <div class="cs-co">XTIX</div>\n'
'          <div class="cs-meta">\n'
'            <div><b>Industry</b><span class="v">FinTech · SaaS</span></div>\n'
'            <div><b>Stage</b><span class="v">Early-Stage Startup</span></div>\n'
'            <div><b>Commercial Team</b><span class="v">Built from Zero</span></div>\n'
'          </div>\n'
'        </div>\n'
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
'    <div class="cs-cols">\n'
'      <div class="cs-col">\n'
'        <div class="cs-lbl">The Challenge</div>\n'
'        <div class="cs-p">When I joined XTIX, there was <b>no commercial infrastructure</b>.</div>\n'
'        <div class="cs-nolist">\n'
'          <div class="no">No CRM</div>\n'
'          <div class="no">No defined Business Development process</div>\n'
'          <div class="no">No outbound methodology</div>\n'
'          <div class="no">No commercial playbook</div>\n'
'          <div class="no">No pipeline management</div>\n'
'          <div class="no">No reporting structure</div>\n'
'        </div>\n'
'        <div class="cs-p">The company\'s vision was clear. <b>The commercial execution wasn\'t.</b></div>\n'
'        <div class="cs-p">The challenge wasn\'t generating more leads '+EM+' it was building the entire <b>commercial operating system</b> from the ground up.</div>\n'
'      </div>\n'
'      <div class="cs-col">\n'
'        <div class="cs-lbl">My Objective</div>\n'
'        <div class="cs-p">Design a <b>scalable commercial foundation</b> capable of supporting predictable business growth '+EM+' not only for Israel, but eventually for the company\'s global commercial activity.</div>\n'
'        <div class="cs-sec2">\n'
'          <div class="cs-lbl">First Decisions</div>\n'
'          <div class="cs-p">Instead of immediately launching outbound campaigns, I focused on <b>understanding the business</b>. I analyzed:</div>\n'
'          <div class="cs-bul">\n'
'            <div class="b">The product</div>\n'
'            <div class="b">Target markets</div>\n'
'            <div class="b">Customer segments</div>\n'
'            <div class="b">Competitive landscape</div>\n'
'            <div class="b">Commercial positioning</div>\n'
'            <div class="b">International expansion opportunities</div>\n'
'          </div>\n'
'          <div class="cs-p">Only after building that understanding did execution begin.</div>\n'
'        </div>\n'
'      </div>\n'
'      <div class="cs-col">\n'
'        <div class="cs-lbl">Commercial Infrastructure Built</div>\n'
'        <div class="cs-checks">\n'+checks+'\n'
'        </div>\n'
'      </div>\n'
'    </div>\n'
'    <div class="cs-sig">\n'
'      <div class="sl">Signature Insight</div>\n'
'      <div class="stx">A commercial department shouldn\'t begin with outreach. <span class="g">It should begin with understanding.</span></div>\n'
'    </div>\n'
'  </div>\n'
'  <div class="ft"><div class="l">Case Study '+EM+' XTIX</div><div class="r"><b>P.04</b> '+EM+' 10</div></div>\n'
'</section>\n\n'
)

ins=s.index("<!-- ============ 06 ")
s=s[:ins]+xtix+s[ins:]

for old,new in [("§06","§05"),("§07","§06"),("§08","§07"),("§09","§08"),("§10","§09"),("§11","§10")]:
    s=s.replace(old,new)
for old,new in [("P.06","P.05"),("P.07","P.06"),("P.08","P.07"),("P.09","P.08"),("P.10","P.09"),("P.11","P.10")]:
    s=s.replace(old,new)

s=s.replace(EM+" 11", EM+" 10").replace("&mdash; 11","&mdash; 10")

for old,new in [("<!-- ============ 06 ","<!-- ============ 05 "),
("<!-- ============ 07 ","<!-- ============ 06 "),
("<!-- ============ 08 ","<!-- ============ 07 "),
("<!-- ============ 09 ","<!-- ============ 08 "),
("<!-- ============ 10 ","<!-- ============ 09 "),
("<!-- ============ 11 ","<!-- ============ 10 ")]:
    s=s.replace(old,new)

css=(
"\n/* ================= CASE STUDY (page 04) ================= */\n"
".cs-top{display:flex;justify-content:space-between;align-items:flex-start;gap:44px}\n"
".cs-title{font-family:var(--disp);font-weight:800;font-size:26px;letter-spacing:-.02em;color:var(--ink);margin-top:11px;max-width:620px;line-height:1.06}\n"
".cs-co-row{display:flex;align-items:flex-end;gap:24px;margin-top:16px}\n"
".cs-co{font-family:var(--disp);font-weight:900;font-size:38px;letter-spacing:-.03em;color:var(--ink);text-transform:uppercase;line-height:.9}\n"
".cs-meta{display:flex;gap:22px;padding-bottom:4px}\n"
".cs-meta > div{font-family:var(--mono);font-size:9.5px;letter-spacing:.05em;text-transform:uppercase}\n"
".cs-meta b{color:var(--muted2);font-weight:400;display:block;margin-bottom:4px}\n"
".cs-meta .v{color:var(--ink)}\n"
".rolebox{border:1px solid var(--line2);padding:13px 18px 14px;min-width:158px}\n"
".rolebox .rl{font-family:var(--mono);font-size:9.5px;letter-spacing:.20em;text-transform:uppercase;color:var(--acc);margin-bottom:10px}\n"
".rolebox .ri{display:flex;align-items:center;gap:10px;font-family:var(--disp);font-weight:600;font-size:12px;color:var(--ink);padding:3px 0}\n"
".rolebox .ri .ck{color:var(--acc);font-size:11px}\n"
".cs-cols{display:grid;grid-template-columns:1fr 1fr 1fr;margin-top:20px;padding-top:20px;border-top:1px solid var(--line)}\n"
".cs-col{padding:0 28px;border-left:1px solid var(--line)}\n"
".cs-col:first-child{padding-left:0;border-left:none}\n"
".cs-col:last-child{padding-right:0}\n"
".cs-lbl{font-family:var(--mono);font-size:10px;letter-spacing:.18em;text-transform:uppercase;color:var(--acc);margin-bottom:12px;display:flex;align-items:center;gap:9px}\n"
".cs-lbl::before{content:\"\";width:12px;height:1px;background:var(--acc)}\n"
".cs-p{color:var(--muted);font-size:11.5px;line-height:1.55;font-weight:300}\n"
".cs-p b{color:var(--ink);font-weight:500}\n"
".cs-p + .cs-p{margin-top:8px}\n"
".cs-nolist{margin:10px 0;display:flex;flex-direction:column;gap:6px}\n"
".cs-nolist .no{font-family:var(--mono);font-size:10px;color:var(--muted);display:flex;align-items:center;gap:9px;letter-spacing:.02em}\n"
".cs-nolist .no::before{content:\"\";width:6px;height:1px;background:var(--acc);flex:none}\n"
".cs-sec2{margin-top:16px}\n"
".cs-bul{margin:10px 0;display:flex;flex-direction:column;gap:6px}\n"
".cs-bul .b{font-size:11.5px;color:var(--muted);font-weight:300;display:flex;gap:10px;align-items:flex-start}\n"
".cs-bul .b::before{content:\"\";width:4px;height:4px;background:var(--acc);flex:none;margin-top:6px}\n"
".cs-checks{display:flex;flex-direction:column;gap:7px}\n"
".cs-check{display:flex;align-items:center;gap:10px;font-size:11.5px;color:var(--ink);font-weight:400}\n"
".cs-check .ck{color:var(--acc);font-size:11px}\n"
".cs-sig{margin-top:auto;padding-top:15px;border-top:1px solid var(--line)}\n"
".cs-sig .sl{font-family:var(--mono);font-size:10px;letter-spacing:.20em;text-transform:uppercase;color:var(--acc);margin-bottom:8px}\n"
".cs-sig .stx{font-family:var(--serif);font-style:italic;font-weight:500;font-size:16px;color:var(--ink);line-height:1.3}\n"
".cs-sig .stx .g{color:var(--acc)}\n"
)
s=s.replace("</style>", css+"</style>",1)

io.open(p,"w",encoding="utf-8").write(s)
print("done pages:", s.count('<section class="page"'), "P.04:", "P.04" in s, "total10:", (EM+" 10") in s)
