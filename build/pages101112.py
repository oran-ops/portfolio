# -*- coding: utf-8 -*-
import io
EM="—"
p="index.html"; s=io.open(p,encoding="utf-8").read()
BR='  <span class="brk tl"></span><span class="brk tr"></span><span class="brk bl"></span><span class="brk br"></span>\n'

# ================= PAGE 10 — LEADERSHIP =================
principles=[
("01","Build Trust Before Performance","People perform better when expectations are clear and trust is earned."),
("02","Coach Before You Judge","Every performance issue deserves investigation first &#8212; understand the process, review the data, listen first, coach second, decide last."),
("03","Create Ownership","People shouldn't execute tasks. They should <b>own outcomes</b>."),
("04","Decisions Based on Facts","KPIs don't replace leadership &#8212; they improve it. Every coaching session begins with <b>evidence, not assumptions</b>."),
("05","Great Managers Solve Today's Problems. Great Leaders Build Tomorrow's System.","My objective was never to close one more deal &#8212; it was to build an organization that produces consistent results <b>without depending on one individual</b>."),
]
prin_html='\n'.join('        <div class="pr2"><div class="p2n">%s</div><div><div class="p2t">%s</div><div class="p2d">%s</div></div></div>'%(n,t,d) for n,t,d in principles)
toolkit=["Hiring &amp; Recruitment","Onboarding Programs","Weekly Team Meetings","Monthly 1:1 Reviews","Quarterly Performance Reviews","KPI Design","Coaching","Sales Methodology","Performance Improvement Plans","Cross-functional Leadership"]
tk_html='\n'.join('        <div class="ci"><span class="k">&#10003;</span> %s</div>'%x for x in toolkit)
page10=(
'<!-- ============ 10 - LEADERSHIP ============ -->\n'
'<section class="page">\n'+BR+
'  <div class="hd"><div class="l">§10 <span>· Leadership</span></div><div class="r">Oran Carmon '+EM+' Building Revenue Engines</div></div>\n'
'  <div class="wrap col">\n'
'    <div class="eyebrow">Leadership</div>\n'
'    <div class="ph-title" style="font-size:26px">Building People. Building Systems. <span class="g">Building Accountability.</span></div>\n'
'    <div class="lead-p">I believe leadership is not measured by how many people report to you &#8212; it is measured by <b>how many people become better because of you</b>. My role is to create clarity, ownership and an environment where people consistently perform at their best.</div>\n'
'    <div class="lead-grid">\n'
'      <div>\n'
'        <div class="cs-lbl">Leadership Principles</div>\n'
'        <div style="margin-top:10px">\n'+prin_html+'\n        </div>\n'
'      </div>\n'
'      <div class="ev-box" style="align-self:start">\n'
'        <div class="bl">Leadership Toolkit</div>\n'+tk_html+'\n'
'      </div>\n'
'    </div>\n'
'    <div class="cs2-sig">\n'
'      <div class="sl">Signature Principle</div>\n'
'      <div class="stx">Leadership is not about creating better employees. <span class="g">It\'s about creating people who no longer depend on you.</span></div>\n'
'    </div>\n'
'  </div>\n'
'  <div class="ft"><div class="l">Leadership</div><div class="r"><b>P.10</b> '+EM+' 12</div></div>\n'
'</section>\n\n'
)

# ================= PAGE 11 — COMMERCIAL TECH & AI =================
def stk(items):
    return '<br>'.join(items)
crm=stk(["<b>HubSpot</b>","Commercial Infrastructure","Pipeline Management","Forecasting","Reporting"])
auto=stk(["<b>Zapier</b>","<b>Webhooks</b>","<b>Google Workspace</b>","<b>API Integrations</b>"])
ai=stk(["<b>GPT</b>","<b>Claude</b>","<b>Gemini</b>","Custom AI Workflows","Knowledge Base","Lead Intelligence","Personalized Outreach","Continuous Learning"])
data=stk(["<b>Clay</b>","<b>Apollo</b>","<b>Hunter</b>","Market Research","Lead Enrichment","Competitive Intelligence"])
aicase=["Researching prospects","Enriching leads","Personalizing outreach","Automating commercial workflows","Learning from previous interactions","Improving commercial recommendations over time"]
aic_html='\n'.join('          <div class="ci"><span class="k">&#10003;</span> %s</div>'%x for x in aicase)
page11=(
'<!-- ============ 11 - COMMERCIAL TECH & AI ============ -->\n'
'<section class="page">\n'+BR+
'  <div class="hd"><div class="l">§11 <span>· Commercial Technology &amp; AI</span></div><div class="r">Oran Carmon '+EM+' Building Revenue Engines</div></div>\n'
'  <div class="wrap col">\n'
'    <div class="eyebrow">Commercial Technology &amp; AI</div>\n'
'    <div class="ph-title" style="font-size:26px">How I use technology to <span class="g">improve commercial decisions.</span></div>\n'
'    <div class="lead-p">Technology should never replace commercial thinking &#8212; it should <b>amplify it</b>. Throughout my career, I\'ve used technology to remove repetitive work, improve decision-making and increase execution capacity.</div>\n'
'    <div class="stack">\n'
'      <div class="stk"><div class="sl2">CRM</div><div class="si2">'+crm+'</div></div>\n'
'      <div class="stk"><div class="sl2">Automation</div><div class="si2">'+auto+'</div></div>\n'
'      <div class="stk"><div class="sl2">AI</div><div class="si2">'+ai+'</div></div>\n'
'      <div class="stk"><div class="sl2">Commercial Data</div><div class="si2">'+data+'</div></div>\n'
'    </div>\n'
'    <div class="x2-bottom">\n'
'      <div class="lookback">\n'
'        <div class="lbl2">AI Case &#8212; Internal Commercial Intelligence Platform</div>\n'
'        <div class="aic-grid">\n'+aic_html+'\n        </div>\n'
'      </div>\n'
'      <div>\n'
'        <div class="myphil"><b>My Philosophy:</b> Technology should automate execution. People should make decisions.</div>\n'
'        <div class="x2-quote" style="margin-top:12px">AI doesn\'t replace commercial leaders. <span class="g">It lets them think faster, learn faster and execute at scale.</span></div>\n'
'      </div>\n'
'    </div>\n'
'  </div>\n'
'  <div class="ft"><div class="l">Commercial Technology &amp; AI</div><div class="r"><b>P.11</b> '+EM+' 12</div></div>\n'
'</section>\n\n'
)

# ================= PAGE 12 — FINAL THOUGHTS + CONTACT =================
fps=[
("1","Understand before you build.",""),
("2","Vision creates direction. Execution creates momentum.",""),
("3","Commercial growth is a business problem &#8212; not a sales problem.",""),
("4","Build systems before you scale people.",""),
("5","Measure decisions &#8212; not assumptions.",""),
("6","Technology should improve thinking &#8212; not replace it.",""),
("7","Great leaders create ownership.",""),
("8","Commercial success belongs to every department.",""),
("9","Continuous learning is a competitive advantage.",""),
("10","If you connect to the vision, you'll always know where you're going.","moto"),
]
fp_html='\n'.join('        <div class="fi"><div class="fn">%s</div><div class="fx %s">%s</div></div>'%(n,c,t) for n,t,c in fps)
page12=(
'<!-- ============ 12 - FINAL THOUGHTS + CONTACT ============ -->\n'
'<section class="page">\n'+BR+
'  <div class="hd"><div class="l">§12 <span>· Final Thoughts</span></div><div class="r">Oran Carmon '+EM+' Building Revenue Engines</div></div>\n'
'  <div class="wrap col">\n'
'    <div class="eyebrow">Final Thoughts</div>\n'
'    <div class="ph-title" style="font-size:28px">The Builder\'s Principles</div>\n'
'    <div class="fp">\n'+fp_html+'\n    </div>\n'
'    <div class="contact-blk">\n'
'      <div style="display:flex;justify-content:space-between;align-items:flex-end">\n'
'        <div><div class="cname">Oran Carmon</div><div class="crole">Commercial Builder</div></div>\n'
'      </div>\n'
'      <div class="crow">\n'
'        <div class="cit"><div class="cl">LinkedIn</div><div class="cv">linkedin.com/in/oran-carmon</div></div>\n'
'        <div class="cit"><div class="cl">Email</div><div class="cv">orancarmon@gmail.com</div></div>\n'
'        <div class="cit"><div class="cl">Phone</div><div class="cv">+972-54-668-5331</div></div>\n'
'      </div>\n'
'    </div>\n'
'  </div>\n'
'  <div class="ft"><div class="l">Turning Vision Into Commercial Growth</div><div class="r"><b>P.12</b> '+EM+' 12</div></div>\n'
'</section>\n\n'
)

i=s.index("</body>")
s=s[:i]+page10+page11+page12+s[i:]
# total 9 -> 12
s=s.replace(EM+" 9", EM+" 12").replace("&mdash; 9","&mdash; 12")

css=(
"\n/* pages 10-12 */\n"
".lead-p{color:var(--muted);font-size:12px;line-height:1.55;font-weight:300;margin-top:12px;max-width:1010px}\n"
".lead-p b{color:var(--ink);font-weight:500}\n"
".lead-grid{display:grid;grid-template-columns:1.55fr 1fr;gap:44px;margin-top:16px}\n"
".pr2{display:grid;grid-template-columns:26px 1fr;gap:12px;padding:8px 0;border-top:1px solid var(--line);align-items:start}\n"
".pr2:first-child{border-top:none;padding-top:0}\n"
".pr2 .p2n{font-family:var(--mono);font-size:11px;color:var(--acc);font-weight:700;padding-top:1px}\n"
".pr2 .p2t{font-family:var(--disp);font-weight:700;font-size:12.5px;color:var(--ink);letter-spacing:-.01em;line-height:1.2}\n"
".pr2 .p2d{margin-top:4px;font-size:10.5px;color:var(--muted);line-height:1.45;font-weight:300}\n"
".pr2 .p2d b{color:var(--ink);font-weight:500}\n"
".stack{display:grid;grid-template-columns:repeat(4,1fr);margin-top:16px;padding-top:14px;border-top:1px solid var(--line2)}\n"
".stk{padding:0 22px;border-left:1px solid var(--line)}\n"
".stk:first-child{padding-left:0;border-left:none}\n"
".stk .sl2{font-family:var(--mono);font-size:10px;letter-spacing:.14em;text-transform:uppercase;color:var(--acc);margin-bottom:11px}\n"
".stk .si2{font-size:11px;color:var(--muted);font-weight:300;line-height:1.85}\n"
".stk .si2 b{color:var(--ink);font-weight:500}\n"
".myphil{font-family:var(--serif);font-style:italic;font-size:12px;color:var(--muted);line-height:1.4}\n"
".myphil b{color:var(--acc);font-style:normal;font-family:var(--mono);font-size:10px;letter-spacing:.12em;text-transform:uppercase;font-weight:700;display:block;margin-bottom:5px}\n"
".aic-grid{display:grid;grid-template-columns:1fr 1fr;gap:4px 16px;margin-top:2px}\n"
".fp{display:grid;grid-template-columns:1fr 1fr;gap:0 50px;margin-top:16px}\n"
".fp .fi{display:grid;grid-template-columns:30px 1fr;gap:12px;padding:9px 0;border-bottom:1px solid var(--line);align-items:baseline}\n"
".fp .fi .fn{font-family:var(--disp);font-weight:800;font-size:14px;color:var(--acc)}\n"
".fp .fi .fx{font-size:12px;color:var(--ink);font-weight:400;line-height:1.35}\n"
".fp .fi .fx.moto{font-family:var(--serif);font-style:italic;color:var(--acc);font-weight:500}\n"
".contact-blk{margin-top:auto;padding-top:16px;border-top:1px solid var(--line2)}\n"
".contact-blk .cname{font-family:var(--disp);font-weight:800;font-size:18px;color:var(--ink);text-transform:uppercase;letter-spacing:-.01em}\n"
".contact-blk .crole{font-family:var(--mono);font-size:10px;letter-spacing:.2em;text-transform:uppercase;color:var(--acc);margin-top:4px}\n"
".contact-blk .crow{margin-top:14px;display:grid;grid-template-columns:repeat(3,1fr);gap:24px}\n"
".contact-blk .cit .cl{font-family:var(--mono);font-size:9px;letter-spacing:.2em;text-transform:uppercase;color:var(--muted2);margin-bottom:6px}\n"
".contact-blk .cit .cv{font-family:var(--disp);font-weight:600;font-size:12.5px;color:var(--ink)}\n"
)
s=s.replace("</style>", css+"</style>",1)
io.open(p,"w",encoding="utf-8").write(s)
print("pages 10,11,12 added; total", s.count('<section class="page"')+1)
