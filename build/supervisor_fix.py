# -*- coding: utf-8 -*-
# SUPERVISOR MEGA-FIX — applies all confirmed findings from the 8-agent audit
import io, re

# ============================================================ PDF
s=io.open("casebook.html",encoding="utf-8").read()

# --- D1: prune dead CSS blocks (old p01/p02/p10-paper/p12 + patch chunks + .serif) ---
def cut_block(txt, start_marker):
    i=txt.find(start_marker)
    if i<0: return txt,False
    j=txt.find("/* ============",i+10)
    if j<0: return txt,False
    return txt[:i]+txt[j:],True
for mk in ["/* ============ PAGE 01 — COVER ============ */",
           "/* ============ PAGE 02 — STATEMENT ============ */",
           "/* ============ PAGE 10 - MEDCOIN ORIGIN (PAPER) ============ */",
           "/* ============ PAGE 12 - TECHNOLOGY & AI ============ */"]:
    s,ok=cut_block(s,mk); print("prune",mk[18:40],ok)
# stray patch chunks of dead pages
for chunk_start,chunk_end in [
    ("\n.p10 .z{margin-bottom:11px}","\n.p10 .zr2{margin-bottom:6px}\n"),
    ("\n.p12 .lead{font-size:13px}","\n.p12 .phil{margin-top:8px}\n"),
]:
    a=s.find(chunk_start)
    if a>=0:
        b=s.find(chunk_end,a)
        if b>=0: s=s[:a]+s[b+len(chunk_end)-1:]; print("chunk pruned",chunk_start.strip()[:18])
s=s.replace(".serif{font-family:'Fraunces',serif}\n","")

# --- D2: var(--emb) instead of hardcoded in icon classes ---
s=s.replace(".p03 .node svg .f{fill:#2FB380;stroke:none}",".p03 .node svg .f{fill:var(--emb);stroke:none}")
s=s.replace(".p03 .node svg .em{stroke:#2FB380}",".p03 .node svg .em{stroke:var(--emb)}")

# --- S1: rail label shorten + p03 vlab lower ---
s=s.replace("MASTER FILE &middot; THE COMMERCIAL OPERATING SYSTEM","MASTER FILE &middot; OPERATING SYSTEM")
s=s.replace(".p03 .rail .vlab{position:absolute;top:60%;",".p03 .rail .vlab{position:absolute;top:64%;",1)

# --- S5: p9 conv viewBox top extend (fixes clipped caption) ---
s=s.replace('viewBox="0 0 560 168"','viewBox="0 -8 560 176"',1)

# --- S9: p12 arch viewBox height (fixes clipped caption) ---
s=re.sub(r'viewBox="0 0 (\d+) 102"', lambda m:'viewBox="0 0 %s 114"'%m.group(1), s, count=1)

# --- T3: chain loop label size ---
s=s.replace('font-size="6.6" letter-spacing="1.6" fill="#5A5B60" transform="rotate(90 204 97)">LEARNING LOOP',
            'font-size="6.9" letter-spacing="1.6" fill="#5A5B60" transform="rotate(90 204 97)">LEARNING LOOP')

# --- C2: add 4 missing stack chips ---
s=s.replace('<span><b>Clay</b></span><span><b>Apollo</b></span><span><b>Hunter</b></span>',
'<span><b>Clay</b></span><span><b>Apollo</b></span><span><b>Hunter</b></span><span>Custom AI Workflows</span><span>Lead Intelligence</span><span>Lead Enrichment</span><span>Competitive Intelligence</span>',1)

# --- C3: Medcoin LOG numbering ---
cnt=[0]
def addlog(m):
    cnt[0]+=1
    return '<div class="lg2"><span class="n2">LOG.%02d</span><span class="c2">'%cnt[0]
s=re.sub(r'<div class="lg2"><span class="c2">',addlog,s)
print("medcoin LOG added:",cnt[0])

# --- spacing compensations CSS (S2,S3,S4,S6,S7,S8) ---
CSS_PDF="""
/* supervisor fixes */
.p06 .folder{height:462px}
.p06 .tech svg{width:156px!important;margin-top:2px!important}
.p06 .band{margin-top:6px;padding-top:7px}
.p09 .folder{height:462px}
.p09 .conv{margin:0 0 6px}
.p09 .z{margin-bottom:11px}
.p09 .lg{margin-bottom:5px}
.p09 .band{padding-top:10px}
.p09 .inner::before{left:47.2%}
.p10b .stamp{top:-22px}
.p10b .tl2{margin-top:6px;padding-top:6px}
.p10b .band2{margin-top:5px;padding-top:6px}
.p10b .para3{font-size:10px;line-height:1.35}
.p10b .lessq2 .qx{font-size:12.4px}
.p10b .outs td{padding:5.5px 0}
.p10b .lg2 .n2{font-family:'JetBrains Mono',monospace;font-size:7px;letter-spacing:.1em;color:var(--dim);width:34px;flex:none}
.p12b .archw{margin:10px 0 2px}
.p12b .bot2{margin-top:6px;padding-top:10px}
.p12b .quote2{margin-top:6px}
.p12b .phil{margin-top:5px}
.p12b .lead{font-size:12.5px}
"""
s=s.replace("</style>",CSS_PDF+"</style>",1)
io.open("casebook.html","w",encoding="utf-8").write(s)
print("PDF fixes applied")

# ============================================================ SITE
t=io.open("site.html",encoding="utf-8").read()

# --- C1: Oasis chips parity ---
t=t.replace("<b>CROSS-FN</b>COLLABORATION","<b>CROSS-FUNCTIONAL</b>COLLABORATION")
t=t.replace("<b>OWNED</b>OWNERSHIP &amp; ACCOUNTABILITY","<b>OWNED</b>CLEAR OWNERSHIP &amp; ACCOUNTABILITY")

# --- C2: stack chips ---
t=t.replace('<span><b>Clay</b></span><span><b>Apollo</b></span><span><b>Hunter</b></span>',
'<span><b>Clay</b></span><span><b>Apollo</b></span><span><b>Hunter</b></span><span>Custom AI Workflows</span><span>Lead Intelligence</span><span>Lead Enrichment</span><span>Competitive Intelligence</span>',1)

# --- F1: Eventer ice marquee band ---
btxt='FILE 03 &middot; EVENTER &middot; ALIGNMENT &mdash; '
band=('<div class="bigmq" style="--mqc:rgba(124,196,232,.20)" aria-hidden="true"><div class="in2"><span>'+btxt*4+'</span><span>'+btxt*4+'</span></div></div>\n')
t=t.replace('<section class="sec case" id="eventer"',band+'<section class="sec case" id="eventer"',1)

# --- S1 site: philosophy rail label + vlab ---
t=t.replace("MASTER FILE &middot; THE COMMERCIAL OPERATING SYSTEM","MASTER FILE &middot; OPERATING SYSTEM")

# --- S10: xtix right-col misalignment (inline top margin on first z) ---
t=t.replace('<div>\n          <div class="z"><div class="zr"><b>02</b><span class="d2"></span>MISSION OBJECTIVE</div>',
            '<div>\n          <div class="z" style="margin-top:0"><div class="zr"><b>02</b><span class="d2"></span>MISSION OBJECTIVE</div>',1)
t=t.replace('<div class="z" style="margin-top:22px"><div class="zr"><b>02</b><span class="d2"></span>MISSION OBJECTIVE</div>',
            '<div class="z"><div class="zr"><b>02</b><span class="d2"></span>MISSION OBJECTIVE</div>',1)

# --- T1/T2/T4: font sizes + weights ---
t=t.replace('font-size="7.2" letter-spacing="1.2"','font-size="7.8" letter-spacing="1.2"')
t=t.replace('font-size="6.8" letter-spacing="1.6"','font-size="7.4" letter-spacing="1.6"')
t=t.replace('font-size="6.8" letter-spacing="1.4"','font-size="7.4" letter-spacing="1.4"')
t=t.replace('font-size="7" letter-spacing="1.6" fill="#5A5B60" transform="rotate(90 230 110)">LEARNING LOOP',
            'font-size="7.5" letter-spacing="1.6" fill="#5A5B60" transform="rotate(90 230 110)">LEARNING LOOP')
t=t.replace("font-weight:900","font-weight:800")

# --- D2 site icons var ---
t=t.replace("#philosophy .node svg .f{fill:#2FB380;stroke:none}","#philosophy .node svg .f{fill:var(--emb);stroke:none}")
t=t.replace("#philosophy .node svg .em{stroke:#2FB380}","#philosophy .node svg .em{stroke:var(--emb)}")

# --- B7: philosophy title word-split (two plain lines) ---
t=t.replace('Every Business Is Different.<br><span style="color:var(--emb)">The Principles of Growth Are Not.</span>',
            '<span class="ln">Every Business Is Different.</span><br><span class="ln g2">The Principles of Growth Are Not.</span>',1)
old_split="document.querySelectorAll('.sttl,#files .bigt,#hero h1').forEach(function(tt){if(split(tt))tt.classList.add('tw')});"
new_split=("document.querySelectorAll('.sttl,#files .bigt,#hero h1').forEach(function(tt){"
"if(split(tt)){tt.classList.add('tw');return}"
"var any=false;[].forEach.call(tt.querySelectorAll('.ln'),function(l){if(split(l))any=true});"
"if(any)tt.classList.add('tw');});")
if old_split in t: t=t.replace(old_split,new_split,1); print("split deep ok")
else:
    t=t.replace("document.querySelectorAll('.sttl,#files .bigt,#statement .l1,#statement .l2,#hero h1').forEach(function(t){t.classList.add('wipe')});","",1)
    # fallback: find actual split line
    m=re.search(r"document\.querySelectorAll\('\.sttl[^\n]*forEach\(function\((\w+)\)\{if\(split\(\1\)\)\1\.classList\.add\('tw'\)\}\);",t)
    if m:
        v=m.group(1)
        t=t[:m.start()]+("document.querySelectorAll('.sttl,#files .bigt,#hero h1').forEach(function(%s){"
        "if(split(%s)){%s.classList.add('tw');return}"
        "var any=false;[].forEach.call(%s.querySelectorAll('.ln'),function(l){if(split(l))any=true});"
        "if(any)%s.classList.add('tw');});")%(v,v,v,v,v)+t[m.end():]
        print("split deep ok (regex)")

# --- B1: quirks-proof measurements ---
t=t.replace("var h=document.documentElement;DOCH=Math.max(1,h.scrollHeight-h.clientHeight);",
"var se=document.scrollingElement||document.documentElement;DOCH=Math.max(1,se.scrollHeight-window.innerHeight);",1)
t=t.replace("var pb=function(){var h=document.documentElement;pbar.style.width=(window.pageYOffset/Math.max(1,h.scrollHeight-h.clientHeight)*100)+'%'};",
"var pb=function(){var se=document.scrollingElement||document.documentElement;pbar.style.width=(window.pageYOffset/Math.max(1,se.scrollHeight-window.innerHeight)*100)+'%'};",1)
t=t.replace("function maxY(){var h=document.documentElement;return h.scrollHeight-h.clientHeight}",
"function maxY(){var se=document.scrollingElement||document.documentElement;return Math.max(0,se.scrollHeight-window.innerHeight)}",1)

# --- B2: engineOK early + hidden-tab-aware failsafe ---
t=t.replace("function init(){\n  measure();","function init(){\n  window.__engineOK=true;\n  measure();",1)
t=t.replace("setTimeout(function(){\n  try{\n    if(window.__engineOK)return;",
"""setTimeout(function chk(){
  try{
    if(window.__engineOK)return;
    if(document.hidden){
      document.addEventListener('visibilitychange',function once(){
        document.removeEventListener('visibilitychange',once);
        setTimeout(chk,2500);
      });
      return;
    }""",1)

# --- B3: don't arm wheel while boot visible ---
t=t.replace("    try{\n      armed=true;","    try{\n      armed=!document.getElementById('boot');",1)

# --- B4: disarm resets writing; anchors bail when off ---
t=t.replace("function disarm(){try{document.documentElement.style.scrollBehavior=''}catch(e){};armed=false;window.__wheelOff=true}",
"function disarm(){try{document.documentElement.style.scrollBehavior=''}catch(e){};armed=false;writing=false;window.__wheelOff=true}",1)
t=t.replace("    a.addEventListener('click',function(ev){\n      var id=a.getAttribute('href');",
"    a.addEventListener('click',function(ev){\n      if(window.__wheelOff)return;\n      var id=a.getAttribute('href');",1)

# --- B5: rename orphans ---
t=t.replace("'#tech .stacks,#tech .bot'","'#tech .archw,#tech .bot'")
t=t.replace(".list,.grid2c,.tools,.pgrid,.chips,#tech .stacks,#philosophy .grid",".list,.grid2c,.tools,.pgrid,.chips,#tech .stackr,#philosophy .grid")
t=t.replace("'a,.dtab,#files .tab,.crow,.chip,.sc'","'a,#files .tab,.crow,.chip'")
# mobile: hero inner wraps
t=t.replace("@media (max-width:820px){#hero .tagl{display:none}#hero .inner{right:12px}#hero .itab{padding:0 10px}#hero .itab .fl2{display:none}}",
"@media (max-width:820px){#hero .tagl{display:none}#hero .inner{left:8px;right:8px;flex-wrap:wrap;justify-content:flex-end}#hero .itab{padding:0 10px;height:32px}#hero .itab .fl2{display:none}}",1)
# dead hover rule out (magnetic owns it)
t=t.replace("#hero .itab:hover{transform:translateY(-8px)}\n","")

# --- B6/M4: static leaks + static scroll behavior ---
t=t.replace("body.static .tk{animation:none!important}",
"body.static .tk,body.static #heromq .row,body.static .crawlp,body.static #hero .barc svg rect,body.static .blink,body.static #hero .cue .ar::after,body.static #philosophy .node,body.static #final .md{animation:none!important}",1)
t=t.replace("if(isStatic)document.body.classList.add('static');\nvar frozen=isStatic||reduced;",
"if(isStatic){document.body.classList.add('static');document.documentElement.style.scrollBehavior='auto';}\nvar frozen=isStatic||reduced;",1)

# --- M1: folders scrub owns transform (kill css transition fight) ---
t=t.replace("[].forEach.call(document.querySelectorAll('.case .folder,#philosophy .folder,#leadership .folder,#final .folder'),function(f){\n  var flip=f.querySelector('.flip');",
"[].forEach.call(document.querySelectorAll('.case .folder,#philosophy .folder,#leadership .folder,#final .folder'),function(f){\n  f.style.transition='none';\n  var flip=f.querySelector('.flip');\n  if(flip)flip.style.transition='none';",1)

# --- M2: heroFx-driven chrome loses its reveal transition after boot ---
t=t.replace("document.querySelectorAll('#hero .rv').forEach(function(u){u.classList.add('on')});\n    lastY=-1;",
"document.querySelectorAll('#hero .rv').forEach(function(u){u.classList.add('on')});\n    setTimeout(function(){document.querySelectorAll('#hero .idx,#hero .barc').forEach(function(el){el.style.transition='none'})},1800);\n    lastY=-1;",1)

# --- M3: magnetic waits for reveal on files tabs ---
t=t.replace("    t.addEventListener('mousemove',function(e){\n      var r=t.getBoundingClientRect();",
"    t.addEventListener('mousemove',function(e){\n      if(t.closest('#files')&&!t.classList.contains('on'))return;\n      var r=t.getBoundingClientRect();",1)

# --- M5: idle life additions ---
t=t.replace("</style>","""
.sttl .g2{color:var(--emb)}
#philosophy .u.on .node{animation:nfloat 7s ease-in-out infinite;animation-delay:calc(var(--i,0)*.9s)}
@keyframes nfloat{0%,100%{transform:translateY(0)}50%{transform:translateY(-4px)}}
#final .minidrawer .md{animation:bob 6s ease-in-out infinite}
#final .minidrawer .md:nth-child(2){animation-delay:.7s}
#final .minidrawer .md:nth-child(3){animation-delay:1.4s}
#final .minidrawer .md:nth-child(4){animation-delay:2.1s}
@media (prefers-reduced-motion:reduce){#philosophy .u.on .node,#final .minidrawer .md{animation:none!important}}
#philosophy .frail .vlab{top:66%}
</style>""",1)
# mfold joins tilt
t=t.replace("[].forEach.call(document.querySelectorAll('.folder'),function(f){\n    f.addEventListener('mousemove'",
"[].forEach.call(document.querySelectorAll('.folder,#hero .mfold'),function(f){\n    f.addEventListener('mousemove'",1)
# statement spine life (scrub with p)
t=t.replace("var stWrap=document.querySelector('#statement .pinh');\nvar stTop=0,stH=0;",
"var stWrap=document.querySelector('#statement .pinh');\nvar stTop=0,stH=0;\nvar SPS=[].slice.call(document.querySelectorAll('#statement .sp span'));",1)
t=t.replace("  words(W1,.05,.30);","  for(var si=0;si<SPS.length;si++){var sq=eo(clamp((p-.02-si*.05)/.22));SPS[si].style.opacity=String(.2+.8*sq);SPS[si].style.transform='translateX(-50%) translateY('+((1-sq)*44)+'px)';}\n  words(W1,.05,.30);",1)

io.open("site.html","w",encoding="utf-8").write(t)
print("SITE fixes applied:",len(t),"bytes")

# ============================================================ STANDALONE (temp-link safe: real doctype)
full=("<!doctype html>\n<html lang=\"en\">\n<head>\n<meta charset=\"utf-8\">\n"
"<meta name=\"viewport\" content=\"width=device-width,initial-scale=1\">\n"
"<meta name=\"color-scheme\" content=\"dark\">\n</head>\n<body>\n"+t+"\n</body>\n</html>")
io.open("site_standalone.html","w",encoding="utf-8").write(full)
print("standalone built:",len(full),"bytes")
