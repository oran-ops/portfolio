# -*- coding: utf-8 -*-
# DOSSIER ROLLOUT — SITE: folder hero, spine statement, tab-rows/rails/stamps on case folders, field report
import io, re
p="site.html"; s=io.open(p,encoding="utf-8").read()

# ---------- 1. HERO -> master folder ----------
i0=s.index('<div class="center">')
i1=s.index('<div class="cue">')
hero_new="""<div class="crumb rv" style="--i:1">ARCHIVE://COMMERCIAL/2026 <b>&#8250;</b> ORAN_CARMON <b>&#8250;</b> MASTER_FILE</div>
  <div class="mflip rv" style="--i:2"><span class="nm">Oran Carmon</span><span class="fl">MASTER FILE &middot; N&deg; 2026-04</span></div>
  <div class="mfold center rv" style="--i:2">
    <span class="hole" style="top:60px"></span><span class="hole" style="top:104px"></span>
    <div class="stampP">PULL TO OPEN &#8250;</div>
    <div class="kick">E X E C U T I V E &nbsp; P O R T F O L I O</div>
    <h1>THE COMMERCIAL<br>SYSTEMS BUILDER</h1>
    <div class="sub">From Vision to Measurable Growth</div>
    <div class="rule"><span class="ln"></span><span class="d"></span><span class="ln"></span></div>
    <div class="by">BY <b>ORAN CARMON</b> &nbsp;&middot;&nbsp; COMMERCIAL SYSTEMS BUILDER</div>
    <div class="quote">&ldquo;If you connect to the vision, you'll always know where you're going.&rdquo;</div>
    <div class="tagl">A PRACTICAL GUIDE TO BUILDING COMMERCIAL ORGANIZATIONS THAT SCALE</div>
    <div class="innerw"><div class="inner">
      <a class="itab" href="#xtix" style="background:#0C0D10"><span class="nm2" style="color:var(--emb)">XTIX</span><span class="fl2" style="color:rgba(242,241,237,.55)">FILE 01</span></a>
      <a class="itab" href="#oasis" style="background:var(--brass)"><span class="nm2">Oasis</span><span class="fl2">FILE 02</span></a>
      <a class="itab" href="#eventer" style="background:var(--ice)"><span class="nm2">Eventer</span><span class="fl2">FILE 03</span></a>
      <a class="itab" href="#medcoin" style="background:var(--ink)"><span class="nm2">Medcoin</span><span class="fl2">FILE 04</span></a>
    </div></div>
  </div>
  """
s=s[:i0]+hero_new+s[i1:]

CSS_HERO="""
/* ===== HERO = MASTER FOLDER ===== */
#hero{padding:84px 24px 40px;display:block}
#hero .crumb{max-width:1180px;margin:64px auto 14px;font-family:'JetBrains Mono',monospace;font-size:10px;letter-spacing:.16em;color:var(--dim);position:relative;z-index:2}
#hero .crumb b{color:var(--emb)}
#hero .mflip{max-width:1180px;margin:0 auto;position:relative;z-index:3;display:flex;align-items:center;gap:15px;
background:var(--emb);border-radius:11px 24px 0 0;height:44px;padding:0 22px;width:max-content}
#hero .mflip .nm{font-family:'Fraunces',serif;font-weight:600;font-size:19px;color:#0C0D10}
#hero .mflip .fl{font-family:'JetBrains Mono',monospace;font-weight:700;font-size:9px;letter-spacing:.2em;color:rgba(12,13,16,.6)}
#hero .mfold{position:relative;z-index:2;max-width:1180px;margin:0 auto;background:var(--emb);
border-radius:0 26px 22px 22px;min-height:62vh;padding:46px 40px 64px;overflow:hidden;text-align:center}
#hero .mfold .hole{position:absolute;left:26px;width:15px;height:15px;border:2px solid rgba(12,13,16,.38);border-radius:50%}
#hero .stampP{position:absolute;top:26px;right:30px;transform:rotate(6deg);border:2px solid rgba(12,13,16,.75);border-radius:7px;
padding:7px 14px;font-family:'JetBrains Mono',monospace;font-weight:700;font-size:10px;letter-spacing:.26em;color:rgba(12,13,16,.85)}
#hero .mfold .kick{color:rgba(12,13,16,.62)}
#hero .mfold h1{color:#0C0D10;margin-top:18px;font-size:clamp(40px,7.6vw,96px)}
#hero .mfold .sub{color:rgba(12,13,16,.82)}
#hero .mfold .rule .ln{background:rgba(12,13,16,.35)}
#hero .mfold .rule .d{background:#0C0D10}
#hero .mfold .by{color:rgba(12,13,16,.72)}
#hero .mfold .by b{color:#0C0D10}
#hero .mfold .quote{color:rgba(12,13,16,.6)}
#hero .tagl{position:absolute;left:30px;bottom:20px;font-family:'JetBrains Mono',monospace;font-size:8.5px;letter-spacing:.2em;color:rgba(12,13,16,.6)}
#hero .innerw{position:absolute;inset:0;border-radius:0 26px 22px 22px;overflow:hidden;pointer-events:none}
#hero .inner{position:absolute;right:28px;bottom:0;display:flex;gap:10px;align-items:flex-end;pointer-events:auto}
#hero .itab{height:40px;border-radius:8px 16px 0 0;display:flex;align-items:center;gap:10px;padding:0 16px;
transform-origin:bottom;transition:transform .4s var(--ease)}
#hero .itab:hover{transform:translateY(-8px)}
#hero .itab .nm2{font-family:'Fraunces',serif;font-weight:500;font-size:14.5px;color:#0C0D10}
#hero .itab .fl2{font-family:'JetBrains Mono',monospace;font-size:7.5px;letter-spacing:.14em;color:rgba(12,13,16,.6)}
@media (max-width:820px){#hero .tagl{display:none}#hero .inner{right:12px}#hero .itab{padding:0 10px}#hero .itab .fl2{display:none}}
#hero .mfold .w>i{color:#0C0D10}
"""
s=s.replace("</style>",CSS_HERO+"</style>",1)

# ---------- 2. STATEMENT spine ----------
s=s.replace('<div class="pinh"><div class="pin"><div class="in">',
'<div class="pinh"><div class="pin"><div class="spine" aria-hidden="true">'
'<div class="sp" style="background:var(--emb)"><span>FILE 01 &mdash; XTIX</span></div>'
'<div class="sp" style="background:var(--brass)"><span>FILE 02 &mdash; OASIS</span></div>'
'<div class="sp" style="background:var(--ice)"><span>FILE 03 &mdash; EVENTER</span></div>'
'<div class="sp" style="background:var(--ink)"><span>FILE 04 &mdash; MEDCOIN</span></div>'
'</div><div class="in">',1)
CSS_SP="""
#statement .spine{position:absolute;top:0;bottom:0;left:0;width:96px;display:flex;flex-direction:column}
#statement .sp{flex:1;position:relative}
#statement .sp span{position:absolute;top:16px;left:50%;transform:translateX(-50%);writing-mode:vertical-rl;
font-family:'JetBrains Mono',monospace;font-weight:700;font-size:9px;letter-spacing:.3em;color:rgba(12,13,16,.72)}
#statement .pin{position:sticky}
#statement .in{padding-left:96px}
@media (max-width:760px){#statement .spine{width:34px}#statement .sp span{display:none}#statement .in{padding-left:34px}}
"""
s=s.replace("</style>",CSS_SP+"</style>",1)

# ---------- 3. case folders: tabrow + rail + stamps ----------
CSS_KIT="""
.case .folder,#philosophy .folder,#leadership .folder,#final .folder{padding-left:92px}
.tabrow{position:absolute;top:-38px;left:-1px;display:flex;gap:9px;align-items:flex-end;z-index:4}
.tabrow .tA{height:38px;background:var(--fc,var(--emb));border-radius:9px 20px 0 0;display:flex;align-items:center;gap:13px;padding:0 18px}
.tabrow .tA .nm{font-family:'Fraunces',serif;font-weight:500;font-size:17px;color:#0C0D10}
.tabrow .tA .fl{font-family:'JetBrains Mono',monospace;font-weight:700;font-size:9px;letter-spacing:.16em;color:rgba(12,13,16,.62)}
.tabrow .tB{height:30px;border:1.5px dashed var(--grid2);border-bottom:0;border-radius:9px 18px 0 0;display:flex;align-items:center;padding:0 16px;
font-family:'JetBrains Mono',monospace;font-weight:600;font-size:8.5px;letter-spacing:.18em;color:var(--dim)}
.frail{position:absolute;left:0;top:0;bottom:0;width:56px;border-right:1px dashed var(--grid)}
.frail .hole{position:absolute;left:19px;width:16px;height:16px;border:2px solid var(--grid2);border-radius:50%}
.frail .vlab{position:absolute;top:54%;left:50%;transform:translate(-50%,-50%) rotate(180deg);writing-mode:vertical-rl;
font-family:'JetBrains Mono',monospace;font-size:8px;letter-spacing:.28em;color:var(--dim);white-space:nowrap}
.rstampS{position:absolute;top:-15px;right:24px;transform:rotate(-6deg);border:2px solid var(--fc,var(--emb));border-radius:6px;
padding:5px 13px;font-family:'JetBrains Mono',monospace;font-weight:700;font-size:10px;letter-spacing:.22em;color:var(--fc,var(--emb));background:var(--bg);z-index:6}
@media (max-width:860px){.case .folder,#philosophy .folder,#leadership .folder,#final .folder{padding-left:38px}.frail{width:24px}.frail .vlab,.frail .hole{display:none}.tabrow .tB{display:none}}
/* field report rows */
.reality .fh{display:flex;justify-content:space-between;font-family:'JetBrains Mono',monospace;font-weight:600;font-size:9px;letter-spacing:.2em;color:var(--dim);margin-bottom:9px}
.reality .fh b{color:var(--emb)}
.reality .frow{display:flex;align-items:center;gap:10px;padding:6px 0;border-bottom:1px dotted var(--grid2);font-size:13px;color:var(--mut)}
.reality .frow:last-child{border-bottom:0}
.reality .frow .o{flex:none;width:14px;height:14px;border:1.5px solid var(--emb);border-radius:50%;position:relative}
.reality .frow .o::after{content:"";position:absolute;left:3px;right:3px;top:50%;height:1.5px;margin-top:-1px;background:var(--emb)}
.reality .frow .st2{margin-left:auto;font-family:'JetBrains Mono',monospace;font-size:8px;letter-spacing:.12em;color:var(--dim)}
"""
s=s.replace("</style>",CSS_KIT+"</style>",1)

def tabrow(nm,fl,ghost):
    g='<div class="tB">%s</div>'%ghost if ghost else ''
    return '<div class="tabrow"><div class="tA"><span class="nm">%s</span><span class="fl">%s</span></div>%s</div>'%(nm,fl,g)
def frail(vlab):
    return ('<div class="frail"><span class="hole" style="top:96px"></span><span class="hole" style="top:146px"></span>'
            '<div class="vlab">%s</div></div>')%vlab

REPL=[
 ('<div class="flip"><span class="nm">XTIX</span><span class="fl">FILE 01</span></div>',
  tabrow("XTIX","&#9656; FILE 01","INTAKE + EVIDENCE"), "CASE FILE N&deg; 01 &middot; XTIX &middot; OPENED 2026",
  '<div class="rstampS">RECEIVED &middot; 2026</div>'),
 ('<div class="flip"><span class="nm">Oasis</span><span class="fl">FILE 02</span></div>',
  tabrow("Oasis","&#9656; FILE 02","COMMAND + EVIDENCE"), "CASE FILE N&deg; 02 &middot; OASIS &middot; CEO",
  '<div class="rstampS">RECEIVED &middot; 2026</div>'),
 ('<div class="flip"><span class="nm">Eventer</span><span class="fl">FILE 03</span></div>',
  tabrow("Eventer","&#9656; FILE 03","ALIGNMENT"), "CASE FILE N&deg; 03 &middot; EVENTER &middot; SYNC",
  '<div class="rstampS">SYNCED &middot; 2026</div>'),
 ('<div class="flip"><span class="nm">Medcoin</span><span class="fl">FILE 04</span></div>',
  tabrow("Medcoin","&#9656; FILE 04","FOUNDER"), "CASE FILE N&deg; 04 &middot; MEDCOIN &middot; ORIGIN",""),
 ('<div class="flip"><span class="nm">Leadership</span><span class="fl">MANAGEMENT FILE</span></div>',
  tabrow("Leadership","&#9656; DOCTRINE","AI SYSTEM &#8250;"), "MANAGEMENT FILE &middot; PRINCIPLES &amp; TOOLKIT",""),
 ('<div class="flip"><span class="nm">The Builder</span><span class="fl">FINAL THOUGHTS</span></div>',
  tabrow("The Builder","&#9656; END OF FILE","&#8249; ARCHIVE"), "FINAL THOUGHTS &middot; THE BUILDER'S PRINCIPLES",""),
]
cnt=0
for old,new,vlab,stamp in REPL:
    if old in s:
        s=s.replace(old,new+'\n      '+frail(vlab)+(('\n      '+stamp) if stamp else ''),1)
        cnt+=1
print("site tabrows:",cnt,"/6")

# philosophy master-file flip
old3=re.search(r'<div class="flip"><span class="sq"[^<]*</span><span class="fl"[^>]*>MASTER FILE &middot; THE 8 PRINCIPLES</span></div>',s)
if old3:
    s=s[:old3.start()]+tabrow("Playbook","&#9656; MASTER FILE","THE CASE FILES &#8250;")+'\n      '+frail("MASTER FILE &middot; THE COMMERCIAL OPERATING SYSTEM")+s[old3.end():]
    print("site p03 tabrow ok")

# ---------- 4. XTIX field report ----------
m=re.search(r'<div class="reality rv" style="--i:2"><span class="subl">BEFORE &middot; COMMERCIAL REALITY AT INTAKE</span>\s*<div class="grid2c">.*?</div></div>',s,flags=re.S)
assert m, "site reality"
gaps=["No CRM","No Business Development function","No sales methodology","No outbound process","No pipeline management","No KPI framework","No reporting structure"]
frows="".join('<div class="frow st" style="--i:%d"><span class="o"></span>%s<span class="st2">GAP.%02d</span></div>'%(i,g,i+1) for i,g in enumerate(gaps))
newr=('<div class="reality rv" style="--i:2"><div class="fh"><span><b>FIELD REPORT</b> &middot; BEFORE &middot; COMMERCIAL REALITY AT INTAKE</span><span>07 GAPS</span></div>'+frows+'</div>')
s=s[:m.start()]+newr+s[m.end():]
print("site field report in")

io.open(p,"w",encoding="utf-8").write(s)
print("dossier site rollout done:",len(s),"bytes")
