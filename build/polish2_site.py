# -*- coding: utf-8 -*-
# Executive polish — SITE mirror
import io, re
p="site.html"; s=io.open(p,encoding="utf-8").read()

# 1. PORTFOLIO rename
s=s.replace('E X E C U T I V E &nbsp; C A S E B O O K','E X E C U T I V E &nbsp; P O R T F O L I O')
s=s.replace('EXECUTIVE CASEBOOK','EXECUTIVE PORTFOLIO')

# 2. statement breathing
s=s.replace('margin-top:12px}','margin-top:26px}',1)  # first hit is #statement .l2

# 3. LOG.NN out
n=len(re.findall(r'<span class="n">LOG\.\d{2}</span>',s))
s=re.sub(r'<span class="n">LOG\.\d{2}</span>','',s)
print("site LOG removed:",n)

# 4. XTIX before/after
s=s.replace("COMMERCIAL REALITY &middot; MISSING AT INTAKE","BEFORE &middot; COMMERCIAL REALITY AT INTAKE")
s=s.replace('<div class="zr"><b>04</b><span class="d2"></span>WHAT I BUILT</div>',
            '<div class="zr"><b>04</b><span class="d2"></span>WHAT I BUILT &middot; AFTER</div>')

# 5. XTIX tech card -> chain
old_tech=('<div class="para">Designed &amp; implemented an internal <b>AI-powered commercial intelligence platform</b> that:</div>'
'\n              <div class="list" style="margin-top:10px">'
'<div class="dash">Researched prospects automatically</div>'
'<div class="dash">Imported &amp; enriched leads from commercial databases</div>'
'<div class="dash">Generated personalized outreach per prospect\'s business</div>'
'<div class="dash">Automated commercial sequences</div>'
'<div class="dash">Continuously improved through feedback &amp; knowledge</div>'
'</div>\n              <div class="pur">PURPOSE: IMPROVE COMMERCIAL DECISION-MAKING WHILE INCREASING EXECUTION CAPACITY.</div>')
nodes=["LEAD","RESEARCH","AI BRAIN","KNOWLEDGE BASE","DECISION","OUTREACH"]
ch=""; y=8
for i,nm in enumerate(nodes):
    ch+=('<rect class="ndot" style="--i:%d" x="6" y="%d" width="170" height="22" rx="7" fill="#121316" stroke="#3A3D43" stroke-width="1.2"/>'
         '<text x="91" y="%d" text-anchor="middle" font-size="8" letter-spacing="1.3" fill="#F2F1ED">%s</text>')%(i,y,y+14.6,nm)
    if i<5:
        ch+=('<line class="pdraw" pathLength="1" style="--i:%d" x1="91" y1="%d" x2="91" y2="%d" stroke="#F4603E" stroke-width="1.5"/>'
             '<path d="M91 %d l-4 -5.6 h8 z" fill="#F4603E"/>')%(i,y+22,y+33,y+34)
    y+=34
ch+=('<path class="crawlp" d="M184 190 C 234 172, 234 44, 184 24" fill="none" stroke="#8E8E93" stroke-width="1.1" stroke-dasharray="3 4"/>'
     '<path d="M182 22 l9 -1 l-3.6 8 z" fill="#8E8E93"/>'
     '<text x="230" y="110" text-anchor="middle" font-size="7" letter-spacing="1.6" fill="#5A5B60" transform="rotate(90 230 110)">LEARNING LOOP</text>')
chain='<svg viewBox="0 0 252 214" style="width:236px;height:auto;margin:12px auto 0;display:block">'+ch+'</svg>'
new_tech=('<div class="para">Designed &amp; implemented an internal <b>AI-powered commercial intelligence platform</b>:</div>'
+chain+
'\n              <div class="pur" style="text-align:center">PURPOSE: BETTER COMMERCIAL DECISIONS &middot; GREATER EXECUTION CAPACITY.</div>')
assert old_tech in s, "site tech block"
s=s.replace(old_tech,new_tech,1)

# 6. Oasis CEO responsibilities
s=s.replace('<span class="d2"></span>MY RESPONSIBILITIES</div>','<span class="d2"></span>CEO RESPONSIBILITIES</div>',1)
old9=('<div class="dash">Recruiting &amp; building the sales team</div><div class="dash">Defining commercial strategy</div>'
'<div class="dash">Pricing model development</div><div class="dash">KPI design</div><div class="dash">Sales methodology</div>'
'<div class="dash">Forecasting</div><div class="dash">Commercial reviews</div><div class="dash">Cross-functional leadership</div>'
'<div class="dash">Profitability management</div>')
ceo=["P&amp;L","Pricing Strategy","Hiring","Commercial Operations","Profitability","Cross-Functional Leadership","Strategic Planning","Forecasting &amp; KPIs"]
assert old9 in s, "site resp"
s=s.replace(old9,"".join('<div class="dash">%s</div>'%t for t in ceo),1)

# 7. Executive Reflection
s=s.replace("REFLECTION &mdash; LOOKING BACK","EXECUTIVE REFLECTION")

# 8. Eventer evidence tiles
anchor='shared organizational responsibility</b> &mdash; not just a sales target.</div></div>'
tiles=('\n          <div class="zr" style="margin-top:22px"><b>EV</b><span class="d2"></span>EVIDENCE</div>'
'<div class="etr">'
'<div class="et st" style="--i:0"><div class="en">03</div><div class="el">BD TEAM MEMBERS<br>MANAGED &amp; COACHED</div></div>'
'<div class="et st" style="--i:1"><div class="en">05</div><div class="el">DEPARTMENTS<br>ALIGNED</div></div>'
'<div class="et st" style="--i:2"><div class="en">07</div><div class="el">KEY CONTRIBUTIONS<br>DELIVERED</div></div>'
'</div>')
assert anchor in s, "site eventer anchor"
s=s.replace(anchor,anchor+tiles,1)

# 9. Medcoin why ended
a10='</table>\n          </div>'
assert a10 in s, "site outs anchor"
why=(a10+'\n          <div class="why st" style="--i:2"><span class="wl">WHY IT ENDED</span>'
'<div class="wt">Operations concluded following geopolitical changes affecting business activity in Turkey.</div></div>')
s=s.replace(a10,why,1)

# 10. Leadership lead swap
s=s.replace('I believe leadership is not measured by how many people report to you &mdash; it is measured by <b>how many people become better because of you</b>. My role is to create clarity, ownership and an environment where people consistently perform at their best.',
            'Great leaders build people who <b>no longer depend on them</b>.')

# 11. Tech section rebuild
arch_nodes=[("LEAD SOURCES",112),("AI RESEARCH",104),("KNOWLEDGE BASE",128),("DECISION ENGINE",130),("PERSONALIZED OUTREACH",172),("CRM",58)]
gap=32; x=4; parts=""; centers=[]
for i,(name,w) in enumerate(arch_nodes):
    parts+=('<rect class="ndot" style="--i:%d" x="%d" y="30" width="%d" height="30" rx="9" fill="#16181C" stroke="#F4603E" stroke-width="1.6"/>'
            '<text x="%.1f" y="49" text-anchor="middle" font-size="8.2" letter-spacing="1.2" fill="#F2F1ED">%s</text>')%(i,x,w,x+w/2.0,name)
    centers.append((x,w)); x+=w+gap
total=x-gap+4
for i in range(len(arch_nodes)-1):
    x0=centers[i][0]+centers[i][1]; x1=centers[i+1][0]
    parts+=('<line class="pdraw" pathLength="1" style="--i:%d" x1="%d" y1="45" x2="%d" y2="45" stroke="#F4603E" stroke-width="1.6"/>'
            '<path d="M%d 45 l-6.5 -3.8 v7.6 z" fill="#F4603E"/>')%(i,x0+2,x1-8,x1-1)
fb_x0=centers[5][0]+centers[5][1]/2.0; fb_x1=centers[1][0]+centers[1][1]/2.0
parts+=('<path class="crawlp" d="M%.1f 60 C %.1f 106, %.1f 106, %.1f 62" fill="none" stroke="#8E8E93" stroke-width="1.2" stroke-dasharray="3 4"/>'
        '<path d="M%.1f 61 l-4.4 7.6 l8.6 .6 z" fill="#8E8E93"/>'
        '<text x="%.1f" y="114" text-anchor="middle" font-size="7.6" letter-spacing="2" fill="#5A5B60">LEARNING FEEDBACK &mdash; EVERY INTERACTION IMPROVES THE SYSTEM</text>'
        )%(fb_x0,fb_x0,fb_x1,fb_x1,fb_x1,(fb_x0+fb_x1)/2.0)
arch='<svg viewBox="0 0 %d 124" style="width:100%%;height:auto">%s</svg>'%(total,parts)

case_checks="".join('<div class="lg"><span class="c">&#10003;</span>%s</div>'%t for t in [
"Researching prospects","Enriching leads","Personalizing outreach",
"Automating commercial workflows","Learning from previous interactions",
"Improving commercial recommendations over time"])
stack="".join('<span>%s</span>'%t for t in ["<b>HubSpot</b> CRM","<b>Zapier</b> &middot; Webhooks","Google Workspace","API Integrations",
"<b>GPT</b>","<b>Claude</b>","<b>Gemini</b>","<b>Clay</b>","<b>Apollo</b>","<b>Hunter</b>"])

i0=s.index('<div class="stacks">')
endm='</section>\n\n<section class="sec" id="final"'
i1=s.index(endm)
newtech=('<div class="archw u" style="margin-top:40px">'
'<div class="zr"><b>A</b><span class="d2"></span>COMMERCIAL INTELLIGENCE PLATFORM &mdash; SYSTEM ARCHITECTURE</div>'
+arch+'</div>'
'\n    <div class="bot">'
'\n      <div class="rv"><div class="zr"><b>B</b><span class="d2"></span>WHAT THE SYSTEM DOES</div><div class="list">'+case_checks+'</div>'
'<div class="phil">MY PHILOSOPHY: TECHNOLOGY SHOULD AUTOMATE EXECUTION. PEOPLE SHOULD MAKE DECISIONS.</div></div>'
'\n      <div class="rv" style="--i:1"><div class="zr"><b>C</b><span class="d2"></span>UNDERLYING STACK</div>'
'<div class="stackr">'+stack+'</div>'
'<div class="lessq" style="margin-top:20px"><div class="qx">AI doesn\'t replace commercial leaders. <b>It lets them think faster, learn faster and execute at scale.</b></div></div></div>'
'\n    </div>\n  </div>\n')
s=s[:i0]+newtech+s[i1:]

# meta line under tech title
s=s.replace('<div class="lead rv" style="--i:2;margin-top:22px">Technology should never replace commercial thinking &mdash; <b>it should amplify it</b>. Throughout my career, I\'ve used technology to remove repetitive work, improve decision-making and increase execution capacity.</div>',
'<div class="lead rv" style="--i:2;margin-top:22px">Technology should never replace commercial thinking &mdash; <b>it should amplify it</b>. I don\'t collect tools; I build systems. This is the commercial intelligence platform I designed &amp; implemented:</div>')

# 12. Final: industries + barcode out
s=s.replace('<div class="zr"><b>B</b><span class="d2"></span>CONTACT</div>',
'<div class="zr"><b>B</b><span class="d2"></span>INDUSTRIES &amp; FOCUS</div>\n          <div class="chips ich">'
+"".join('<span>%s</span>'%t for t in ["SaaS","FinTech","Construction","Events","B2B","AI","Commercial Strategy","Business Development","Revenue Operations"])
+'</div>\n          <div class="zr" style="margin-top:20px"><b>C</b><span class="d2"></span>CONTACT</div>',1)
s=re.sub(r'<div class="bc">.*?ARCHIVE 2026</span></div>',
         '<span style="font-family:\'JetBrains Mono\',monospace;font-size:8.5px;letter-spacing:.3em;color:var(--dim)">ARCHIVE &middot; 2026</span>',s,count=1,flags=re.S)

# 13. CSS
css="""
/* executive polish */
.etr{display:flex;gap:12px;margin-top:14px}
.et{flex:1;border:1px solid var(--grid);border-radius:11px;padding:13px 15px;background:var(--card2)}
.et .en{font-family:'JetBrains Mono',monospace;font-weight:700;font-size:24px;color:var(--fc,var(--ice));line-height:1}
.et .el{margin-top:7px;font-family:'JetBrains Mono',monospace;font-size:7.8px;letter-spacing:.16em;color:var(--dim);line-height:1.65}
.why{margin-top:14px;border:1px solid var(--grid);border-radius:11px;padding:13px 16px;background:var(--card2)}
.why .wl{display:block;font-family:'JetBrains Mono',monospace;font-weight:600;font-size:8px;letter-spacing:.24em;color:var(--dim);margin-bottom:6px}
.why .wt{font-size:12px;line-height:1.55;color:var(--mut)}
#medcoin .why .wt{color:var(--mut)}
#tech .archw{margin-top:40px}
#tech .stackr{display:flex;flex-wrap:wrap;gap:8px}
#tech .stackr span{border:1px solid var(--grid);border-radius:8px;padding:6px 11px;font-family:'JetBrains Mono',monospace;font-size:8.6px;letter-spacing:.12em;color:var(--mut)}
#tech .stackr span b{color:var(--ink);font-weight:600}
#final .ich{margin-bottom:0}
#final .ich span{border:1px solid var(--grid);border-radius:8px;padding:6px 12px;font-family:'JetBrains Mono',monospace;font-size:8.6px;letter-spacing:.12em;color:var(--mut)}
"""
s=s.replace("</style>",css+"</style>",1)

io.open(p,"w",encoding="utf-8").write(s)
print("site executive polish applied:",len(s),"bytes")
