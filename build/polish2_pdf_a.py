# -*- coding: utf-8 -*-
# Executive polish — PDF steps 1-5 (were lost when run #1 crashed pre-write)
import io, re
p="casebook.html"; s=io.open(p,encoding="utf-8").read()

# 1. CASEBOOK -> PORTFOLIO
s=s.replace("<title>The Commercial Builder - Executive Casebook</title>",
            "<title>The Commercial Builder - Executive Portfolio</title>")
s=s.replace("EXECUTIVE CASEBOOK","EXECUTIVE PORTFOLIO")

# 2. statement breathing
s=s.replace("color:var(--emb);margin-top:10px}","color:var(--emb);margin-top:26px}",1)

# 3. LOG.NN out
n=len(re.findall(r'<span class="n">LOG\.\d{2}</span>',s))
s=re.sub(r'<span class="n">LOG\.\d{2}</span>','',s)
print("LOG prefixes removed:",n)

# 4. XTIX before/after
s=s.replace("COMMERCIAL REALITY &middot; MISSING AT INTAKE","BEFORE &middot; COMMERCIAL REALITY AT INTAKE")
s=s.replace('<div class="zr"><b>04</b><span class="d2"></span>WHAT I BUILT</div>',
            '<div class="zr"><b>04</b><span class="d2"></span>WHAT I BUILT &middot; AFTER</div>')
s=s.replace("INTAKE &middot; &#8709; NOTHING","BEFORE &middot; &#8709; NOTHING")
s=s.replace('<b>10 SYSTEMS</b> &middot; LIVE','AFTER &middot; <b>10 SYSTEMS LIVE</b>')

# 5. P06 tech bullets -> chain diagram
old_tech=('<div class="para">Designed &amp; implemented an internal <b>AI-powered commercial intelligence platform</b> that:</div>'
'\n          <div class="dash">Researched prospects automatically</div>'
'<div class="dash">Imported &amp; enriched leads from commercial databases</div>'
'<div class="dash">Generated personalized outreach per prospect\'s business</div>'
'<div class="dash">Automated commercial sequences</div>'
'<div class="dash">Continuously improved through feedback &amp; knowledge</div>'
'\n          <div class="pur">PURPOSE: IMPROVE COMMERCIAL DECISION-MAKING WHILE INCREASING EXECUTION CAPACITY.</div>')
nodes=["LEAD","RESEARCH","AI BRAIN","KNOWLEDGE BASE","DECISION","OUTREACH"]
ch=""; y=8
for i,nm in enumerate(nodes):
    ch+=('<rect x="6" y="%d" width="150" height="19" rx="6" fill="#121316" stroke="#3A3D43" stroke-width="1.1"/>'
         '<text x="81" y="%d" text-anchor="middle" font-size="7.4" letter-spacing="1.2" fill="#F2F1ED">%s</text>')%(y,y+12.8,nm)
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
assert old_tech in s, "tech block not found"
s=s.replace(old_tech,new_tech,1)

# bonus fix: P12 feedback label clearance
s=s.replace('viewBox="0 0 %d 102"'% (4+104+30+96+30+118+30+120+30+160+30+52), 'viewBox="0 0 %d 112"'%(4+104+30+96+30+118+30+120+30+160+30+52))
s=s.replace('y="92" text-anchor="middle" font-size="7" letter-spacing="1.8" fill="#5A5B60">LEARNING FEEDBACK','y="104" text-anchor="middle" font-size="7" letter-spacing="1.8" fill="#5A5B60">LEARNING FEEDBACK')

io.open(p,"w",encoding="utf-8").write(s)
print("steps 1-5 applied")
