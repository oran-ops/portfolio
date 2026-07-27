# -*- coding: utf-8 -*-
# SITE BUILDER PART 1: head + css + hero + statement + philosophy
import io

fonts = io.open("fonts/fonts_dossier.css", encoding="utf-8").read()

CSS = """
:root{--bg:#0C0D10;--card:#121316;--card2:#16181C;--ink:#F2F1ED;--mut:#8E8E93;--dim:#5A5B60;--grid:#26282C;--grid2:#3A3D43;
--hair:rgba(255,255,255,.07);--emb:#F4603E;--emb-dim:rgba(244,96,62,.10);--brass:#E0A458;--ice:#7CC4E8;--ice-dim:rgba(124,196,232,.12);
--ease:cubic-bezier(.22,.61,.2,1)}
*{margin:0;padding:0;box-sizing:border-box}
html{scroll-behavior:smooth}
body{background:var(--bg);color:var(--ink);font-family:'Inter',system-ui,sans-serif;-webkit-font-smoothing:antialiased;overflow-x:hidden}
.mono{font-family:'JetBrains Mono',monospace}
a{color:inherit;text-decoration:none}
svg{display:block}
svg text{font-family:'JetBrains Mono',monospace}

/* reveal system */
.rv{opacity:0;transform:translateY(26px);transition:opacity .8s var(--ease),transform .8s var(--ease);transition-delay:calc(var(--i,0)*80ms)}
.sec.on .rv{opacity:1;transform:none}
.rvs{opacity:0;transform:translateY(14px) scale(.985);transition:opacity .7s var(--ease),transform .7s var(--ease);transition-delay:calc(var(--i,0)*80ms)}
.sec.on .rvs{opacity:1;transform:none}
@media (prefers-reduced-motion:reduce){
  html{scroll-behavior:auto}
  .rv,.rvs{opacity:1!important;transform:none!important;transition:none!important}
  *{animation:none!important;transition:none!important}
}
body.static .rv,body.static .rvs{opacity:1;transform:none;transition:none}

/* chrome */
#pbar{position:fixed;top:0;left:0;height:2px;background:var(--emb);width:0;z-index:99}
#rail{position:fixed;right:26px;top:50%;transform:translateY(-50%);z-index:90;display:flex;flex-direction:column;gap:14px}
#rail a{display:flex;align-items:center;gap:9px;justify-content:flex-end}
#rail .lb{font-family:'JetBrains Mono',monospace;font-size:8px;letter-spacing:.18em;color:var(--dim);opacity:0;transform:translateX(6px);transition:all .3s var(--ease)}
#rail a:hover .lb,#rail a.act .lb{opacity:1;transform:none}
#rail .dt{width:8px;height:8px;border:1.5px solid var(--dim);transform:rotate(45deg);transition:all .3s var(--ease)}
#rail a.act .dt{background:var(--fc,var(--emb));border-color:var(--fc,var(--emb))}
#rail a:hover .dt{border-color:var(--ink)}
@media (max-width:1150px){#rail{display:none}}
.brkbox{position:relative}
.brkbox .bk{position:absolute;width:18px;height:18px;border:0 solid rgba(242,241,237,.35);z-index:5}
.brkbox .bk.tl{top:0;left:0;border-top-width:1.5px;border-left-width:1.5px}
.brkbox .bk.tr{top:0;right:0;border-top-width:1.5px;border-right-width:1.5px}
.brkbox .bk.bl{bottom:0;left:0;border-bottom-width:1.5px;border-left-width:1.5px}
.brkbox .bk.br{bottom:0;right:0;border-bottom-width:1.5px;border-right-width:1.5px}

.sec{position:relative;padding:110px 24px}
.wrap{max-width:1120px;margin:0 auto}
.rub{display:flex;align-items:center;gap:11px;font-family:'JetBrains Mono',monospace;font-weight:700;font-size:11px;letter-spacing:.26em;color:var(--ink)}
.rub .d{width:7px;height:7px;background:var(--fc,var(--emb));transform:rotate(45deg)}
.tok{display:inline-flex;align-items:center;gap:8px;font-family:'JetBrains Mono',monospace;font-weight:600;font-size:10px;letter-spacing:.16em;
border:1px solid var(--grid);border-radius:7px;padding:7px 13px;color:var(--fc,var(--emb))}
.shead{display:flex;justify-content:space-between;align-items:center;margin-bottom:26px}
.sttl{font-weight:800;font-size:clamp(26px,3.6vw,40px);letter-spacing:-.028em;line-height:1.08}
.smeta{margin-top:10px;font-family:'JetBrains Mono',monospace;font-size:10px;letter-spacing:.22em;color:var(--mut)}

/* folder */
.folder{position:relative;background:var(--card);border:1px solid var(--hair);border-radius:0 18px 18px 18px;padding:34px 38px}
.flip{position:absolute;top:-34px;left:-1px;height:34px;background:var(--fc,var(--emb));border-radius:9px 20px 0 0;
display:flex;align-items:center;gap:13px;padding:0 18px}
.flip .nm{font-family:'Fraunces',serif;font-weight:500;font-size:17px;color:#0C0D10}
.flip .fl{font-family:'JetBrains Mono',monospace;font-weight:600;font-size:9px;letter-spacing:.16em;color:rgba(12,13,16,.62)}
.zr{display:flex;align-items:center;gap:10px;font-family:'JetBrains Mono',monospace;font-weight:700;font-size:11px;letter-spacing:.22em;color:var(--ink);margin-bottom:12px}
.zr b{color:var(--fc,var(--emb))}
.zr .d2{width:5px;height:5px;background:var(--fc,var(--emb));transform:rotate(45deg)}
.para{font-size:14.5px;line-height:1.66;color:var(--mut)}
.para b{color:var(--ink);font-weight:600}
.dash{display:flex;align-items:center;gap:10px;font-size:13.5px;color:var(--mut)}
.dash::before{content:"";flex:none;width:10px;height:2px;background:var(--fc,var(--emb))}
.lg{display:flex;align-items:center;gap:10px;font-size:13.5px;font-weight:600;color:var(--ink)}
.lg .n{font-family:'JetBrains Mono',monospace;font-size:8.5px;letter-spacing:.1em;color:var(--dim);width:40px;flex:none}
.lg .c{flex:none;width:13px;height:13px;background:var(--fc,var(--emb));color:#0C0D10;font-size:10px;font-weight:800;line-height:13px;text-align:center}
.mi{display:flex;align-items:center;gap:10px;font-size:13px;color:var(--mut)}
.mi .o{flex:none;width:15px;height:15px;border:1.5px solid var(--fc,var(--emb));border-radius:50%;position:relative}
.mi .o::after{content:"";position:absolute;left:3px;right:3px;top:50%;height:1.5px;margin-top:-1px;background:var(--fc,var(--emb))}
.lessq{border-left:2px solid var(--fc,var(--emb));padding:4px 0 4px 22px}
.lessq .qx{font-family:'Fraunces',serif;font-style:italic;font-weight:500;font-size:19px;line-height:1.5;color:var(--ink)}
.lessq .qx b{color:var(--fc,var(--emb));font-weight:600}
.lessq .who{margin-top:8px;font-family:'JetBrains Mono',monospace;font-size:8px;letter-spacing:.24em;color:var(--dim)}

/* ============ HERO ============ */
#hero{min-height:100svh;display:flex;flex-direction:column;justify-content:center;padding:90px 24px 0}
#hero .idx{position:absolute;top:44px;left:44px;font-family:'JetBrains Mono',monospace;font-size:10px;letter-spacing:.22em;color:var(--mut);line-height:2.3}
#hero .idx .k{color:var(--dim)}
#hero .idx .em{color:var(--emb);font-weight:600}
#hero .idx .br2{color:var(--brass);font-weight:600}
#hero .barc{position:absolute;top:44px;right:44px;text-align:center}
#hero .barc .yr{margin-top:4px;font-family:'JetBrains Mono',monospace;font-size:8px;letter-spacing:.3em;color:var(--dim)}
#hero .center{text-align:center;max-width:1200px;margin:0 auto}
#hero .kick{font-family:'JetBrains Mono',monospace;font-weight:600;font-size:clamp(9px,1.2vw,12px);letter-spacing:.5em;color:var(--mut)}
#hero h1{margin-top:22px;font-weight:800;font-size:clamp(44px,9vw,110px);line-height:1;letter-spacing:-.035em}
#hero .sub{margin-top:26px;font-family:'Fraunces',serif;font-style:italic;font-weight:500;font-size:clamp(18px,2.6vw,30px);color:var(--emb)}
#hero .rule{margin:34px auto 0;display:flex;align-items:center;gap:12px;width:max-content}
#hero .rule .ln{width:76px;height:1px;background:var(--grid2)}
#hero .rule .d{width:8px;height:8px;background:var(--emb);transform:rotate(45deg)}
#hero .by{margin-top:22px;font-family:'JetBrains Mono',monospace;font-size:11px;letter-spacing:.34em;color:var(--mut)}
#hero .by b{color:var(--ink);font-weight:700}
#hero .quote{margin-top:16px;font-family:'Fraunces',serif;font-style:italic;font-size:15px;color:var(--dim)}
#hero .drawer{max-width:1120px;margin:64px auto 0;width:100%;display:flex;gap:10px;border-bottom:1px solid var(--grid2);padding:0 6px}
#hero .dtab{flex:1;height:44px;border-radius:9px 20px 0 0;display:flex;align-items:center;padding:0 16px;cursor:pointer;
transform-origin:bottom;transition:transform .45s var(--ease)}
#hero .dtab:hover{transform:translateY(-7px)}
#hero .dtab .nm{font-family:'Fraunces',serif;font-weight:500;font-size:16px;color:#0C0D10}
#hero .dtab .meta{margin-left:auto;font-family:'JetBrains Mono',monospace;font-size:8px;letter-spacing:.14em;color:rgba(12,13,16,.65)}
#hero .tag{max-width:1120px;margin:14px auto 0;width:100%;display:flex;justify-content:space-between;
font-family:'JetBrains Mono',monospace;font-size:9px;letter-spacing:.2em;color:var(--dim)}
#hero .cue{position:absolute;bottom:26px;left:50%;transform:translateX(-50%);display:flex;flex-direction:column;align-items:center;gap:7px;
font-family:'JetBrains Mono',monospace;font-size:8px;letter-spacing:.3em;color:var(--dim)}
#hero .cue .ar{width:1px;height:26px;background:var(--grid2);position:relative;overflow:hidden}
#hero .cue .ar::after{content:"";position:absolute;top:-10px;left:0;width:1px;height:10px;background:var(--emb);animation:cuefall 1.8s ease-in-out infinite}
@keyframes cuefall{0%{top:-10px}70%{top:26px}100%{top:26px}}
@media (max-width:760px){#hero .idx{position:static;margin-bottom:26px}#hero .barc{display:none}#hero .drawer{flex-wrap:wrap}#hero .dtab{min-width:46%}}

/* ============ STATEMENT ============ */
#statement{padding:150px 24px}
#statement .in{text-align:center;max-width:1050px;margin:0 auto}
#statement .memo{display:inline-flex;background:var(--emb);color:#0C0D10;border-radius:7px 16px 0 0;
padding:9px 17px;font-family:'JetBrains Mono',monospace;font-weight:700;font-size:9.5px;letter-spacing:.22em;margin-bottom:34px}
#statement .l1{font-weight:800;font-size:clamp(26px,4.6vw,50px);letter-spacing:-.03em;line-height:1.18}
#statement .l2{font-weight:800;font-size:clamp(26px,4.6vw,50px);letter-spacing:-.03em;line-height:1.18;color:var(--emb);margin-top:12px}

/* ============ PHILOSOPHY ============ */
#philosophy .folder{margin-top:34px}
#philosophy .grid{display:grid;grid-template-columns:repeat(4,1fr);gap:38px 30px}
@media (max-width:960px){#philosophy .grid{grid-template-columns:repeat(2,1fr)}}
@media (max-width:540px){#philosophy .grid{grid-template-columns:1fr}}
#philosophy .node{width:58px;height:58px;border-radius:50%;background:var(--card2);border:1.5px solid var(--grid2);display:flex;align-items:center;justify-content:center}
#philosophy .node svg{width:34px;height:34px;fill:none;stroke:#F2F1ED;stroke-width:1.5;stroke-linecap:round;stroke-linejoin:round}
#philosophy .node svg .f{fill:#F4603E;stroke:none}
#philosophy .node svg .dsh{stroke-dasharray:2.2 2.8;stroke:#8E8E93}
#philosophy .node svg .em{stroke:#F4603E}
#philosophy .snum{margin-top:13px;font-family:'JetBrains Mono',monospace;font-size:9px;letter-spacing:.2em;color:var(--dim)}
#philosophy .sname{margin-top:5px;font-weight:700;font-size:16px;letter-spacing:-.01em}
#philosophy .sdesc{margin-top:6px;font-size:12.5px;line-height:1.5;color:var(--mut)}
#philosophy .sigp{margin-top:44px;text-align:center;position:relative;padding:16px 28px;width:max-content;max-width:100%;margin-left:auto;margin-right:auto}
#philosophy .sigp::before,#philosophy .sigp::after{content:"";position:absolute;width:17px;height:17px;border:0 solid var(--emb)}
#philosophy .sigp::before{top:0;left:0;border-top-width:2px;border-left-width:2px}
#philosophy .sigp::after{bottom:0;right:0;border-bottom-width:2px;border-right-width:2px}
#philosophy .sigp .qx{font-family:'Fraunces',serif;font-style:italic;font-weight:500;font-size:clamp(16px,2.2vw,21px)}
#philosophy .sigp .qx b{color:var(--emb);font-weight:600}
#philosophy .sigp .who{margin-top:7px;font-family:'JetBrains Mono',monospace;font-size:8px;letter-spacing:.26em;color:var(--dim)}
"""

ICONS = {
'vision':'<svg viewBox="0 0 48 48"><path d="M6 40h36"/><path d="M6 40c6-1.5 9-5 10-9"/><circle cx="14.5" cy="15.5" r="3.4"/><path d="M14.5 18.9v7.6"/><path d="M14.5 21.5l4.4-2.2"/><path d="M14.5 21.5l-4 3"/><path d="M14.5 26.5l3.2 5.5"/><path d="M14.5 26.5l-2.6 6"/><path class="dsh" d="M21.5 14.5h14"/><circle class="f" cx="40" cy="14.5" r="2.6"/></svg>',
'biz':'<svg viewBox="0 0 48 48"><path d="M10 22l14-8 14 8"/><path d="M13 20.5V34c0 1.4 4.9 4 11 4s11-2.6 11-4V20.5"/><path d="M13 27c0 1.4 4.9 4 11 4s11-2.6 11-4"/><circle class="f" cx="24" cy="22.5" r="2"/><path class="dsh" d="M24 14V7"/></svg>',
'market':'<svg viewBox="0 0 48 48"><circle cx="24" cy="24" r="17"/><circle class="dsh" cx="24" cy="24" r="9.5"/><path d="M24 24L35.5 12.5"/><circle class="f" cx="17" cy="28.5" r="2"/><circle class="f" cx="30" cy="31" r="2"/><circle class="f" cx="19" cy="15.5" r="2"/></svg>',
'arch':'<svg viewBox="0 0 48 48"><path d="M8 40h32"/><rect x="11" y="30" width="9" height="10"/><rect x="21.5" y="24" width="9" height="16"/><path d="M37 40V12h-13"/><path d="M26 12l2.5 3.4"/><path class="dsh" d="M28.5 12v6"/><rect class="em" x="25.8" y="18" width="5.4" height="5"/></svg>',
'people':'<svg viewBox="0 0 48 48"><path d="M8 39.5h32"/><circle cx="13" cy="19" r="3.2"/><path d="M8.6 32c0-4 2-6.6 4.4-6.6s4.4 2.6 4.4 6.6"/><circle class="em" cx="24" cy="13.5" r="3.6"/><path class="em" d="M19 28c0-4.6 2.2-7.4 5-7.4s5 2.8 5 7.4"/><circle cx="35" cy="19" r="3.2"/><path d="M30.6 32c0-4 2-6.6 4.4-6.6s4.4 2.6 4.4 6.6"/><path class="dsh" d="M18.5 34.5h11"/></svg>',
'exec':'<svg viewBox="0 0 48 48"><path class="dsh" d="M7 32c4 2 9 .8 9.8-2.4.6-2.6-3.4-3.4-4-.8-.7 3 4.6 4.6 9.2 2.8"/><path d="M24 30L42 11l-6.2 21-4.6-6.4-7.2 4.4z"/><path class="em" d="M31.2 25.6L42 11"/></svg>',
'measure':'<svg viewBox="0 0 48 48"><path d="M9 39V9"/><path d="M9 39h30"/><path d="M9 31h3M9 23h3M9 15h3"/><path d="M14 33l7-6 6 3.6 10-11"/><circle class="f" cx="37" cy="19.6" r="2.4"/><path class="dsh" d="M37 17V9.5"/></svg>',
'improve':'<svg viewBox="0 0 48 48"><path d="M37 27a13 13 0 1 1-4.6-9.9"/><path class="em" d="M31 9.5L39.5 9l.5 8.5"/><path class="em" d="M39.5 9L31.8 16.8"/><circle class="f" cx="24" cy="27" r="1.8"/></svg>'}

steps=[("01","Vision","Define where the business is going.",'vision'),
("02","Business Understanding","Understand the business before improving it.",'biz'),
("03","Market Understanding","Understand the customer before creating the message.",'market'),
("04","Commercial Architecture","Build the commercial engine before scaling it.",'arch'),
("05","People &amp; Leadership","Create ownership, not dependency.",'people'),
("06","Execution","Turn strategy into consistent execution.",'exec'),
("07","Measurement","Measure decisions, not assumptions.",'measure'),
("08","Continuous Improvement","Learn faster than the market evolves.",'improve')]
grid=""
for i,(n,nm,ds,ic) in enumerate(steps):
    grid+=('<div class="rvs" style="--i:%d"><div class="node">%s</div>'
           '<div class="snum">STEP %s</div><div class="sname">%s</div><div class="sdesc">%s</div></div>')%(i,ICONS[ic],n,nm,ds)

barcode='<svg viewBox="0 0 62 30" style="width:62px;height:30px">'
x=0
for i,w in enumerate([2,1,3,1,2,1,1,3,2,1,2,3,1,2,1,3,1,1,2]):
    barcode+='<rect x="%d" y="0" width="%d" height="30" fill="%s"/>'%(x,w,"#8E8E93" if i%3 else "#F2F1ED")
    x+=w+1
barcode+='</svg>'

HTML = """<title>Oran Carmon &mdash; The Commercial Builder</title>
<style>
"""+fonts+CSS+"""
</style>
<div id="pbar"></div>
<nav id="rail">
  <a href="#hero" style="--fc:var(--emb)"><span class="lb">COVER</span><span class="dt"></span></a>
  <a href="#statement" style="--fc:var(--emb)"><span class="lb">STATEMENT</span><span class="dt"></span></a>
  <a href="#philosophy" style="--fc:var(--emb)"><span class="lb">PHILOSOPHY</span><span class="dt"></span></a>
  <a href="#files" style="--fc:var(--emb)"><span class="lb">THE CASE FILES</span><span class="dt"></span></a>
  <a href="#xtix" style="--fc:var(--emb)"><span class="lb">XTIX</span><span class="dt"></span></a>
  <a href="#oasis" style="--fc:var(--brass)"><span class="lb">OASIS</span><span class="dt"></span></a>
  <a href="#eventer" style="--fc:var(--ice)"><span class="lb">EVENTER</span><span class="dt"></span></a>
  <a href="#medcoin" style="--fc:var(--ink)"><span class="lb">MEDCOIN</span><span class="dt"></span></a>
  <a href="#leadership" style="--fc:var(--emb)"><span class="lb">LEADERSHIP</span><span class="dt"></span></a>
  <a href="#tech" style="--fc:var(--emb)"><span class="lb">TECH &amp; AI</span><span class="dt"></span></a>
  <a href="#final" style="--fc:var(--emb)"><span class="lb">CONTACT</span><span class="dt"></span></a>
</nav>

<section class="sec" id="hero">
  <div class="idx rv" style="--i:0">
    <span class="k">ARCHIVE N&deg;</span> 2026-04<br>
    <span class="k">CLASSIFICATION:</span> <span class="em">COMMERCIAL</span><br>
    <span class="k">STATUS:</span> <span class="br2">ACTIVE</span>
  </div>
  <div class="barc rv" style="--i:1">"""+barcode+"""<div class="yr">2026</div></div>
  <div class="center">
    <div class="kick rv" style="--i:1">E X E C U T I V E &nbsp; C A S E B O O K</div>
    <h1 class="rv" style="--i:2">THE COMMERCIAL<br>BUILDER</h1>
    <div class="sub rv" style="--i:3">From vision to measurable growth</div>
    <div class="rule rv" style="--i:4"><span class="ln"></span><span class="d"></span><span class="ln"></span></div>
    <div class="by rv" style="--i:5">BY <b>ORAN CARMON</b> &nbsp;&middot;&nbsp; COMMERCIAL BUILDER</div>
    <div class="quote rv" style="--i:6">&ldquo;If you connect to the vision, you'll always know where you're going.&rdquo;</div>
  </div>
  <div class="drawer rv" style="--i:7">
    <a class="dtab" href="#xtix" style="background:var(--emb)"><span class="nm">XTIX</span><span class="meta">FILE 01</span></a>
    <a class="dtab" href="#oasis" style="background:var(--brass)"><span class="nm">Oasis</span><span class="meta">FILE 02</span></a>
    <a class="dtab" href="#eventer" style="background:var(--ice)"><span class="nm">Eventer</span><span class="meta">FILE 03</span></a>
    <a class="dtab" href="#medcoin" style="background:var(--ink)"><span class="nm">Medcoin</span><span class="meta">FILE 04</span></a>
  </div>
  <div class="tag rv" style="--i:8"><span>A PRACTICAL GUIDE TO BUILDING COMMERCIAL ORGANIZATIONS THAT SCALE</span><span>13 SECTIONS &mdash; 04 CASE FILES</span></div>
  <div class="cue"><span class="ar"></span>SCROLL TO OPEN</div>
</section>

<section class="sec" id="statement">
  <div class="in">
    <div class="memo rv" style="--i:0">MEMO &middot; FROM THE ARCHIVE</div>
    <div class="l1 rv" style="--i:1">Most companies don't need better salespeople.</div>
    <div class="l2 rv" style="--i:2">They need better commercial decisions.</div>
  </div>
</section>

<section class="sec" id="philosophy">
  <div class="wrap">
    <div class="shead rv" style="--i:0">
      <div class="rub"><span class="d"></span>MY COMMERCIAL PHILOSOPHY</div>
      <div class="tok">THE OPERATING SYSTEM &#8250;</div>
    </div>
    <div class="sttl rv" style="--i:1">Every business is different.<br><span style="color:var(--emb)">The principles of growth are not.</span></div>
    <div class="folder rv" style="--i:2;margin-top:56px">
      <div class="flip"><span class="sq" style="width:6px;height:6px;background:#0C0D10;transform:rotate(45deg)"></span><span class="fl" style="color:#0C0D10;font-weight:700">MASTER FILE &middot; THE 8 PRINCIPLES</span></div>
      <div class="grid">"""+grid+"""</div>
    </div>
    <div class="sigp rv" style="--i:3">
      <div class="qx">First build a system that works. <b>Then build a business that scales.</b></div>
      <div class="who">SIGNATURE PRINCIPLE</div>
    </div>
  </div>
</section>
<!--MORE-->
"""

io.open("site.html","w",encoding="utf-8").write(HTML)
print("site part 1 written:",len(HTML),"bytes")
