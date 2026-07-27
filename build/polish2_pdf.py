# -*- coding: utf-8 -*-
# Executive polish pass — PDF (casebook.html)
import io, re
p="casebook.html"; s=io.open(p,encoding="utf-8").read()

# ---------- 1. CASEBOOK -> PORTFOLIO ----------
s=s.replace("<title>The Commercial Builder - Executive Casebook</title>",
            "<title>The Commercial Builder - Executive Portfolio</title>")
s=s.replace("EXECUTIVE CASEBOOK","EXECUTIVE PORTFOLIO")

# ---------- 2. statement breathing ----------
s=s.replace(".p02 .l2{font-weight:800;font-size:47px;letter-spacing:-.03em;line-height:1.18;color:var(--emb);margin-top:10px}",
            ".p02 .l2{font-weight:800;font-size:47px;letter-spacing:-.03em;line-height:1.18;color:var(--emb);margin-top:26px}")

# ---------- 3. declutter: LOG.NN prefixes out ----------
s=re.sub(r'<span class="n">LOG\.\d{2}</span>','',s)

# ---------- 4. XTIX before/after ----------
s=s.replace("COMMERCIAL REALITY &middot; MISSING AT INTAKE","BEFORE &middot; COMMERCIAL REALITY AT INTAKE")
s=s.replace('<div class="zr"><b>04</b><span class="d2"></span>WHAT I BUILT</div>',
            '<div class="zr"><b>04</b><span class="d2"></span>WHAT I BUILT &middot; AFTER</div>')
s=s.replace("INTAKE &middot; &#8709; NOTHING","BEFORE &middot; &#8709; NOTHING")
s=s.replace('<b>10 SYSTEMS</b> &middot; LIVE','AFTER &middot; <b>10 SYSTEMS LIVE</b>')

# ---------- 5. P06: AI bullets -> mini chain diagram ----------
old_tech=('<div class="para">Designed &amp; implemented an internal <b>AI-powered commercial intelligence platform</b> that:</div>'
'\n          <div class="dash">Researched prospects automatically</div>'
'<div class="dash">Imported &amp; enriched leads from commercial databases</div>'
'<div class="dash">Generated personalized outreach per prospect\'s business</div>'
'<div class="dash">Automated commercial sequences</div>'
'<div class="dash">Continuously improved through feedback &amp; knowledge</div>'
'\n          <div class="pur">PURPOSE: IMPROVE COMMERCIAL DECISION-MAKING WHILE INCREASING EXECUTION CAPACITY.</div>')
nodes=["LEAD","RESEARCH","AI BRAIN","KNOWLEDGE BASE","DECISION","OUTREACH"]
ch=""; y=8
for i,n in enumerate(nodes):
    ch+=('<rect x="6" y="%d" width="150" height="19" rx="6" fill="#121316" stroke="#3A3D43" stroke-width="1.1"/>'
         '<text x="81" y="%d" text-anchor="middle" font-size="7.4" letter-spacing="1.2" fill="#F2F1ED">%s</text>')%(y,y+12.8,n)
    if i<5:
        ch+='<line x1="81" y1="%d" x2="81" y2="%d" stroke="#F4603E" stroke-width="1.4"/><path d="M81 %d l-3.6 -5 h7.2 z" fill="#F4603E"/>'%(y+19,y+29,y+30)
    y+=30
ch+=('<path d="M162 165 C 208 150, 208 40, 162 22" fill="none" stroke="#8E8E93" stroke-width="1.1" stroke-dasharray="3 4"/>'
     '<path d="M160 20 l8.5 -1 l-3.4 7.6 z" fill="#8E8E93"/>'
     '<text x="204" y="97" text-anchor="middle" font-size="6.6" letter-spacing="1.6" fill="#5A5B60" transform="rotate(90 204 97)">LEARNING LOOP</text>')
chain='<svg viewBox="0 0 224 188" style="width:214px;height:auto;margin:6px auto 0;display:block">'+ch+'</svg>'
new_tech=('<div class="para">Designed &amp; implemented an internal <b>AI-powered commercial intelligence platform</b>:</div>'
+chain+
'\n          <div class="pur" style="text-align:center">PURPOSE: BETTER COMMERCIAL DECISIONS &middot; GREATER EXECUTION CAPACITY.</div>')
assert old_tech in s
s=s.replace(old_tech,new_tech,1)

# ---------- 6. P07: CEO Responsibilities ----------
old_resp=('<div class="zr"><b>02</b><span class="d2"></span>MY RESPONSIBILITIES</div>\n            <div class="rgrid">'
'<div class="dash">Recruiting &amp; building the sales team</div><div class="dash">Defining commercial strategy</div>'
'<div class="dash">Pricing model development</div><div class="dash">KPI design</div><div class="dash">Sales methodology</div>'
'<div class="dash">Forecasting</div><div class="dash">Commercial reviews</div><div class="dash">Cross-functional leadership</div>'
'<div class="dash">Profitability management</div></div>')
ceo=["P&amp;L","Pricing Strategy","Hiring","Commercial Operations","Profitability","Cross-Functional Leadership","Strategic Planning","Forecasting &amp; KPIs"]
new_resp=('<div class="zr"><b>02</b><span class="d2"></span>CEO RESPONSIBILITIES</div>\n            <div class="rgrid">'
+"".join('<div class="dash">%s</div>'%t for t in ceo)+'</div>')
assert old_resp in s
s=s.replace(old_resp,new_resp,1)

# ---------- 7. P08: Executive Reflection ----------
s=s.replace("REFLECTION &mdash; LOOKING BACK","EXECUTIVE REFLECTION")

# ---------- 8. P09: evidence tiles ----------
css_add="""
.p09 .etr{display:flex;gap:10px;margin-top:16px}
.p09 .et{flex:1;border:1px solid var(--grid);border-radius:10px;padding:10px 12px;background:var(--card2)}
.p09 .et .en{font-family:'JetBrains Mono',monospace;font-weight:700;font-size:19px;color:var(--ice);line-height:1}
.p09 .et .el{margin-top:5px;font-family:'JetBrains Mono',monospace;font-size:7.2px;letter-spacing:.16em;color:var(--dim);line-height:1.6}
.p10b .why{margin-top:12px;border:1px solid var(--grid);border-radius:10px;padding:10px 14px;background:var(--card2)}
.p10b .why .wl{display:block;font-family:'JetBrains Mono',monospace;font-weight:600;font-size:7.5px;letter-spacing:.24em;color:var(--dim);margin-bottom:5px}
.p10b .why .wt{font-size:10.6px;line-height:1.5;color:var(--mut)}
.p13 .ich{display:flex;flex-wrap:wrap;gap:7px;margin-bottom:18px}
.p13 .ich span{border:1px solid var(--grid);border-radius:7px;padding:5px 11px;font-family:'JetBrains Mono',monospace;font-size:8px;letter-spacing:.12em;color:var(--mut)}
"""
s=s.replace("</style>",css_add+"</style>",1)

anchor='shared organizational responsibility</b> &mdash; not just a sales target.</div>\n        </div>'
tiles=('\n          <div class="zr" style="margin-top:16px"><b>EV</b><span class="d2"></span>EVIDENCE</div>'
'<div class="etr">'
'<div class="et"><div class="en">03</div><div class="el">BD TEAM MEMBERS<br>MANAGED &amp; COACHED</div></div>'
'<div class="et"><div class="en">05</div><div class="el">DEPARTMENTS<br>ALIGNED</div></div>'
'<div class="et"><div class="en">07</div><div class="el">KEY CONTRIBUTIONS<br>DELIVERED</div></div>'
'</div>')
assert anchor in s
s=s.replace(anchor,anchor+tiles,1)

# ---------- 9. P10: why it ended ----------
a10='</table>\n        </div>\n      </div>\n    </div>\n    <div class="tl2">'
why=('</table>\n        </div>'
'\n        <div class="why"><span class="wl">WHY IT ENDED</span>'
'<div class="wt">Operations concluded following geopolitical changes affecting business activity in Turkey.</div></div>'
'\n      </div>\n    </div>\n    <div class="tl2">')
assert a10 in s
s=s.replace(a10,why,1)

# ---------- 10. P11: lead swap ----------
s=s.replace('I believe leadership is not measured by how many people report to you &mdash; it is measured by <b>how many people become better because of you</b>. My role is to create clarity, ownership and an environment where people consistently perform at their best.',
            'Great leaders build people who <b>no longer depend on them</b>.')

# ---------- 11. P12: full rebuild -> system architecture ----------
s=re.sub(r'\n<!--[^\n]*PAGE 12 \. TECHNOLOGY & AI[^\n]*-->\n<section class="page casef p12".*?</section>\n','\n',s,flags=re.S)

css12="""
/* ============ PAGE 12B - COMMERCIAL INTELLIGENCE PLATFORM ============ */
.p12b .folder{padding:24px 30px 18px}
.p12b .lead{font-family:'Fraunces',serif;font-style:italic;font-weight:500;font-size:13.5px;line-height:1.5;color:var(--mut)}
.p12b .lead b{color:var(--ink);font-weight:500}
.p12b .archw{margin:18px 0 6px}
.p12b .bot2{display:grid;grid-template-columns:46fr 54fr;column-gap:32px;margin-top:14px;padding-top:16px;border-top:1px solid var(--grid)}
.p12b .zr{margin-bottom:10px}
.p12b .lg{margin-bottom:7px;font-size:11.4px}
.p12b .stackr{display:flex;flex-wrap:wrap;gap:7px}
.p12b .stackr span{border:1px solid var(--grid);border-radius:7px;padding:5px 10px;font-family:'JetBrains Mono',monospace;font-size:8px;letter-spacing:.12em;color:var(--mut)}
.p12b .stackr span b{color:var(--ink);font-weight:600}
.p12b .phil{margin-top:12px;font-family:'JetBrains Mono',monospace;font-size:9px;letter-spacing:.14em;color:var(--emb);line-height:1.7}
.p12b .quote2{margin-top:11px;border-left:2px solid var(--emb);padding:2px 0 2px 16px}
.p12b .quote2 .qx{font-family:'Fraunces',serif;font-style:italic;font-weight:500;font-size:14px;line-height:1.45;color:var(--ink)}
.p12b .quote2 .qx b{color:var(--emb);font-weight:600}
"""
s=s.replace("</style>",css12+"</style>",1)

# architecture svg
arch_nodes=[("LEAD SOURCES",104),("AI RESEARCH",96),("KNOWLEDGE BASE",118),("DECISION ENGINE",120),("PERSONALIZED OUTREACH",160),("CRM",52)]
gap=30; x=4; parts=""; centers=[]
for name,w in arch_nodes:
    parts+=('<rect x="%d" y="30" width="%d" height="26" rx="8" fill="#16181C" stroke="#F4603E" stroke-width="1.5"/>'
            '<text x="%.1f" y="46.5" text-anchor="middle" font-size="7.6" letter-spacing="1.1" fill="#F2F1ED">%s</text>')%(x,w,x+w/2,name)
    centers.append((x,w))
    x+=w+gap
total=x-gap+4
for i in range(len(arch_nodes)-1):
    x0=centers[i][0]+centers[i][1]; x1=centers[i+1][0]
    parts+=('<line x1="%d" y1="43" x2="%d" y2="43" stroke="#F4603E" stroke-width="1.5"/>'
            '<path d="M%d 43 l-6 -3.4 v6.8 z" fill="#F4603E"/>')%(x0+2,x1-7,x1-1)
fb_x0=centers[5][0]+centers[5][1]/2; fb_x1=centers[1][0]+centers[1][1]/2
parts+=('<path d="M%.1f 56 C %.1f 96, %.1f 96, %.1f 58" fill="none" stroke="#8E8E93" stroke-width="1.2" stroke-dasharray="3 4"/>'
        '<path d="M%.1f 57 l-4 7 l8 .5 z" fill="#8E8E93"/>'
        '<text x="%.1f" y="92" text-anchor="middle" font-size="7" letter-spacing="1.8" fill="#5A5B60">LEARNING FEEDBACK &mdash; EVERY INTERACTION IMPROVES THE SYSTEM</text>'
        )%(fb_x0,fb_x0,fb_x1,fb_x1,fb_x1,(fb_x0+fb_x1)/2)
arch='<svg viewBox="0 0 %d 102" style="width:100%%;height:auto">%s</svg>'%(total,parts)

case_checks="".join('<div class="lg"><span class="c">&#10003;</span>%s</div>'%t for t in [
"Researching prospects","Enriching leads","Personalizing outreach",
"Automating commercial workflows","Learning from previous interactions",
"Improving commercial recommendations over time"])
stack="".join('<span>%s</span>'%t for t in ["<b>HubSpot</b> CRM","<b>Zapier</b> &middot; Webhooks","Google Workspace","API Integrations",
"<b>GPT</b>","<b>Claude</b>","<b>Gemini</b>","<b>Clay</b>","<b>Apollo</b>","<b>Hunter</b>"])

page12="""
<!-- ================= PAGE 12 . COMMERCIAL INTELLIGENCE PLATFORM ================= -->
<section class="page casef p12b" style="--fc:var(--emb)">
  <span class="brk tl"></span><span class="brk tr"></span><span class="brk bl"></span><span class="brk br"></span>
  <div class="hd">
    <div class="rub"><span class="d"></span>COMMERCIAL TECHNOLOGY &amp; AI</div>
    <div class="tok">SYSTEM FILE &middot; AI</div>
  </div>
  <div class="ttl">How I use technology to improve commercial decisions.</div>
  <div class="meta">COMMERCIAL INTELLIGENCE PLATFORM &middot; SYSTEM ARCHITECTURE</div>
  <div class="folder">
    <div class="flip"><span class="nm">Technology</span><span class="fl">SYSTEM FILE &middot; AI</span></div>
    <div class="lead">Technology should never replace commercial thinking &mdash; <b>it should amplify it</b>. I don't collect tools; I build systems. This is the commercial intelligence platform I designed &amp; implemented:</div>
    <div class="archw">
      <div class="zr"><b>A</b><span class="d2"></span>COMMERCIAL INTELLIGENCE PLATFORM &mdash; SYSTEM ARCHITECTURE</div>
      """+arch+"""
    </div>
    <div class="bot2">
      <div>
        <div class="zr"><b>B</b><span class="d2"></span>WHAT THE SYSTEM DOES</div>
        """+case_checks+"""
      </div>
      <div>
        <div class="zr"><b>C</b><span class="d2"></span>UNDERLYING STACK</div>
        <div class="stackr">"""+stack+"""</div>
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
a13='\n<!-- ================= PAGE 13 . FINAL THOUGHTS ================= -->'
assert a13 in s
s=s.replace(a13,page12+a13,1)

# ---------- 12. P13: industries in, barcode out ----------
s=s.replace('<div class="zr"><b>B</b><span class="d2"></span>CONTACT</div>',
'<div class="zr"><b>B</b><span class="d2"></span>INDUSTRIES &amp; FOCUS</div>\n        <div class="ich">'
+"".join('<span>%s</span>'%t for t in ["SaaS","FinTech","Construction","Events","B2B","AI","Commercial Strategy","Business Development","Revenue Operations"])
+'</div>\n        <div class="zr"><b>C</b><span class="d2"></span>CONTACT</div>',1)
s=re.sub(r'<div class="bc"><svg viewBox="0 0 \d+ 26">.*?</svg><span class="yr">ARCHIVE 2026</span></div>',
         '<span class="yr" style="font-family:\'JetBrains Mono\',monospace;font-size:8px;letter-spacing:.3em;color:var(--dim)">ARCHIVE &middot; 2026</span>',s,count=1,flags=re.S)

io.open(p,"w",encoding="utf-8").write(s)
print("executive polish applied to PDF")
