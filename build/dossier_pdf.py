# -*- coding: utf-8 -*-
# DOSSIER ROLLOUT — PDF: cover=master folder, statement=spine, case pages=tab-row+rail+field-report
import io, re
p="casebook.html"; s=io.open(p,encoding="utf-8").read()

# ================= 1. NEW COVER (P.01) =================
s=re.sub(r'<!-- =+ PAGE 01[^\n]*-->\s*<section class="page p01">.*?</section>','@@P01@@',s,count=1,flags=re.S)
if '@@P01@@' not in s:
    s=re.sub(r'<section class="page p01">.*?</section>','@@P01@@',s,count=1,flags=re.S)
assert '@@P01@@' in s, "p01 not found"

P01="""<section class="page p01b">
  <span class="brk tl"></span><span class="brk tr"></span><span class="brk bl"></span><span class="brk br"></span>
  <div class="idx">
    <span class="k">ARCHIVE N&deg;</span> 2026-04<br>
    <span class="k">CLASSIFICATION:</span> <span class="em">COMMERCIAL</span><br>
    <span class="k">STATUS:</span> <span class="br2">ACTIVE</span>
  </div>
  <div class="crumb">ARCHIVE://COMMERCIAL/2026 <b>&#8250;</b> ORAN_CARMON <b>&#8250;</b> MASTER_FILE</div>
  <div class="barc">
    <svg viewBox="0 0 62 30" style="width:62px;height:30px"><rect x="0" width="2" height="30" fill="#F2F1ED"/><rect x="3" width="1" height="30" fill="#8E8E93"/><rect x="6" width="3" height="30" fill="#8E8E93"/><rect x="11" width="1" height="30" fill="#F2F1ED"/><rect x="14" width="2" height="30" fill="#8E8E93"/><rect x="18" width="1" height="30" fill="#8E8E93"/><rect x="21" width="1" height="30" fill="#F2F1ED"/><rect x="24" width="3" height="30" fill="#8E8E93"/><rect x="29" width="2" height="30" fill="#8E8E93"/><rect x="33" width="1" height="30" fill="#F2F1ED"/><rect x="36" width="2" height="30" fill="#8E8E93"/><rect x="40" width="3" height="30" fill="#8E8E93"/><rect x="45" width="1" height="30" fill="#F2F1ED"/><rect x="48" width="2" height="30" fill="#8E8E93"/><rect x="52" width="1" height="30" fill="#8E8E93"/><rect x="55" width="3" height="30" fill="#F2F1ED"/><rect x="60" width="1" height="30" fill="#8E8E93"/></svg>
    <div class="yr">2026</div>
  </div>
  <div class="folder">
    <div class="flip"><span class="nm">Oran Carmon</span><span class="fl">MASTER FILE &middot; N&deg; 2026-04</span></div>
    <span class="hole" style="top:74px"></span><span class="hole" style="top:120px"></span>
    <div class="stamp">PULL TO OPEN &#8250;</div>
    <div class="kick">E X E C U T I V E &nbsp; P O R T F O L I O</div>
    <h1>THE COMMERCIAL<br>SYSTEMS BUILDER</h1>
    <div class="sub">From Vision to Measurable Growth</div>
    <div class="rule"><span class="ln"></span><span class="d"></span><span class="ln"></span></div>
    <div class="by">BY <b>ORAN CARMON</b> &nbsp;&middot;&nbsp; COMMERCIAL SYSTEMS BUILDER</div>
    <div class="qq">&ldquo;If you connect to the vision, you'll always know where you're going.&rdquo;</div>
    <div class="tagl">A PRACTICAL GUIDE TO BUILDING COMMERCIAL ORGANIZATIONS THAT SCALE</div>
    <div class="inner">
      <div class="itab" style="background:var(--brass);height:30px"><span class="nm2">Oasis</span><span class="fl2">FILE 02</span></div>
      <div class="itab" style="background:var(--ice);height:36px"><span class="nm2">Eventer</span><span class="fl2">FILE 03</span></div>
      <div class="itab" style="background:var(--ink);height:42px"><span class="nm2">Medcoin</span><span class="fl2">FILE 04</span></div>
    </div>
  </div>
</section>"""
s=s.replace('@@P01@@',P01,1)

# ================= 2. NEW STATEMENT (P.02) =================
s=re.sub(r'<!-- =+ PAGE 02[^\n]*-->\s*<section class="page p02">.*?</section>','@@P02@@',s,count=1,flags=re.S)
if '@@P02@@' not in s:
    s=re.sub(r'<section class="page p02">.*?</section>','@@P02@@',s,count=1,flags=re.S)
assert '@@P02@@' in s, "p02 not found"

P02="""<section class="page p02b">
  <span class="brk tr"></span><span class="brk br"></span>
  <div class="spine">
    <div class="sp" style="background:var(--emb)"><span>FILE 01 &mdash; XTIX</span></div>
    <div class="sp" style="background:var(--brass)"><span>FILE 02 &mdash; OASIS</span></div>
    <div class="sp" style="background:var(--ice)"><span>FILE 03 &mdash; EVENTER</span></div>
    <div class="sp" style="background:var(--ink)"><span>FILE 04 &mdash; MEDCOIN</span></div>
  </div>
  <div class="rub"><span class="d"></span>MEMO 001</div>
  <div class="tok">CLASSIFICATION: COMMERCIAL</div>
  <div class="in">
    <div class="memo">MEMO &middot; FROM THE ARCHIVE</div>
    <div class="l1">Most companies don't need better salespeople.</div>
    <div class="l2">They need better commercial decisions.</div>
    <div class="sig">FOR INTERNAL REVIEW &middot; DO NOT DISTRIBUTE</div>
  </div>
  <div class="pn"><b>P.02</b> &mdash; 13</div>
</section>"""
s=s.replace('@@P02@@',P02,1)

# ================= 3. KIT + PAGE CSS =================
CSS="""
/* ============ DOSSIER V2 — COVER ============ */
.p01b .idx{position:absolute;top:44px;left:64px;font-family:'JetBrains Mono',monospace;font-size:10px;letter-spacing:.22em;color:var(--mut);line-height:2.2}
.p01b .idx .k{color:var(--dim)}
.p01b .idx .em{color:var(--emb);font-weight:600}
.p01b .idx .br2{color:var(--brass);font-weight:600}
.p01b .crumb{position:absolute;top:118px;left:64px;font-family:'JetBrains Mono',monospace;font-size:10px;letter-spacing:.16em;color:var(--dim)}
.p01b .crumb b{color:var(--emb);font-weight:600}
.p01b .barc{position:absolute;top:44px;right:64px;text-align:center}
.p01b .barc .yr{margin-top:4px;font-family:'JetBrains Mono',monospace;font-size:8px;letter-spacing:.3em;color:var(--dim)}
.p01b .folder{position:absolute;top:196px;left:64px;right:64px;bottom:52px;background:var(--emb);border-radius:0 26px 22px 22px}
.p01b .flip{position:absolute;top:-40px;left:-1px;height:40px;background:var(--emb);border-radius:11px 24px 0 0;display:flex;align-items:center;gap:15px;padding:0 22px}
.p01b .flip .nm{font-family:'Fraunces',serif;font-weight:600;font-size:19px;color:#0C0D10}
.p01b .flip .fl{font-family:'JetBrains Mono',monospace;font-weight:700;font-size:9px;letter-spacing:.2em;color:rgba(12,13,16,.6)}
.p01b .hole{position:absolute;left:26px;width:15px;height:15px;border:2px solid rgba(12,13,16,.38);border-radius:50%}
.p01b .kick{position:absolute;top:46px;left:0;right:0;text-align:center;font-family:'JetBrains Mono',monospace;font-weight:700;font-size:10.5px;letter-spacing:.5em;color:rgba(12,13,16,.62)}
.p01b h1{position:absolute;top:80px;left:0;right:0;text-align:center;font-weight:800;font-size:64px;line-height:1.04;letter-spacing:-.03em;color:#0C0D10}
.p01b .sub{position:absolute;top:236px;left:0;right:0;text-align:center;font-family:'Fraunces',serif;font-style:italic;font-weight:500;font-size:22px;color:rgba(12,13,16,.82)}
.p01b .rule{position:absolute;top:286px;left:50%;transform:translateX(-50%);display:flex;align-items:center;gap:12px}
.p01b .rule .ln{width:64px;height:1px;background:rgba(12,13,16,.35)}
.p01b .rule .d{width:7px;height:7px;background:#0C0D10;transform:rotate(45deg)}
.p01b .by{position:absolute;top:308px;left:0;right:0;text-align:center;font-family:'JetBrains Mono',monospace;font-weight:600;font-size:10px;letter-spacing:.3em;color:rgba(12,13,16,.72)}
.p01b .by b{color:#0C0D10;font-weight:800}
.p01b .qq{position:absolute;top:338px;left:0;right:0;text-align:center;font-family:'Fraunces',serif;font-style:italic;font-size:13.5px;color:rgba(12,13,16,.62)}
.p01b .stamp{position:absolute;top:30px;right:34px;transform:rotate(6deg);border:2px solid rgba(12,13,16,.75);border-radius:7px;
padding:7px 14px;font-family:'JetBrains Mono',monospace;font-weight:700;font-size:10px;letter-spacing:.26em;color:rgba(12,13,16,.85)}
.p01b .tagl{position:absolute;left:30px;bottom:22px;font-family:'JetBrains Mono',monospace;font-size:8.5px;letter-spacing:.2em;color:rgba(12,13,16,.6)}
.p01b .inner{position:absolute;right:30px;bottom:0;display:flex;gap:10px;align-items:flex-end}
.p01b .itab{height:34px;border-radius:8px 16px 0 0;display:flex;align-items:center;gap:10px;padding:0 14px}
.p01b .itab .nm2{font-family:'Fraunces',serif;font-weight:500;font-size:13.5px;color:#0C0D10}
.p01b .itab .fl2{font-family:'JetBrains Mono',monospace;font-size:7.5px;letter-spacing:.14em;color:rgba(12,13,16,.6)}

/* ============ DOSSIER V2 — STATEMENT ============ */
.p02b .spine{position:absolute;top:0;bottom:0;left:0;width:112px;display:flex;flex-direction:column}
.p02b .sp{flex:1;position:relative}
.p02b .sp span{position:absolute;top:14px;left:50%;transform:translateX(-50%);writing-mode:vertical-rl;
font-family:'JetBrains Mono',monospace;font-weight:700;font-size:9px;letter-spacing:.3em;color:rgba(12,13,16,.72)}
.p02b .rub{position:absolute;top:48px;left:170px;display:flex;align-items:center;gap:11px;font-family:'JetBrains Mono',monospace;font-weight:700;font-size:10.5px;letter-spacing:.26em;color:var(--ink)}
.p02b .rub .d{width:7px;height:7px;background:var(--emb);transform:rotate(45deg)}
.p02b .tok{position:absolute;top:40px;right:64px;font-family:'JetBrains Mono',monospace;font-weight:600;font-size:9.5px;letter-spacing:.16em;
border:1px solid var(--grid);border-radius:7px;padding:6px 12px;color:var(--emb)}
.p02b .in{position:absolute;left:112px;right:0;top:50%;transform:translateY(-52%);text-align:center;padding:0 70px}
.p02b .memo{display:inline-flex;background:var(--emb);color:#0C0D10;border-radius:7px 16px 0 0;
padding:9px 17px;font-family:'JetBrains Mono',monospace;font-weight:700;font-size:9.5px;letter-spacing:.22em;margin-bottom:34px}
.p02b .l1{font-weight:800;font-size:45px;letter-spacing:-.03em;line-height:1.16;color:var(--ink)}
.p02b .l2{font-weight:800;font-size:45px;letter-spacing:-.03em;line-height:1.16;color:var(--emb);margin-top:26px}
.p02b .sig{margin-top:38px;font-family:'JetBrains Mono',monospace;font-size:9px;letter-spacing:.26em;color:var(--dim)}
.p02b .pn{position:absolute;right:64px;bottom:44px;font-family:'JetBrains Mono',monospace;font-size:9.5px;letter-spacing:.18em;color:var(--dim)}
.p02b .pn b{color:var(--mut);font-weight:600}

/* ============ DOSSIER V2 — CASE KIT ============ */
.casef .folder{padding-left:64px}
.casef .tabrow{position:absolute;top:-34px;left:-1px;display:flex;gap:8px;align-items:flex-end;z-index:4}
.casef .tA{height:34px;background:var(--fc);border-radius:9px 20px 0 0;display:flex;align-items:center;gap:12px;padding:0 18px}
.casef .tA .nm{font-family:'Fraunces',serif;font-weight:500;font-size:15px;color:#0C0D10}
.casef .tA .fl{font-family:'JetBrains Mono',monospace;font-weight:700;font-size:8.5px;letter-spacing:.16em;color:rgba(12,13,16,.62)}
.casef .tB{height:27px;border:1.5px dashed var(--grid2);border-bottom:0;border-radius:9px 18px 0 0;display:flex;align-items:center;padding:0 15px;
font-family:'JetBrains Mono',monospace;font-weight:600;font-size:8px;letter-spacing:.18em;color:var(--dim)}
.casef .rail{position:absolute;left:0;top:0;bottom:0;width:46px;border-right:1px dashed var(--grid)}
.casef .rail .hole{position:absolute;left:15px;width:15px;height:15px;border:2px solid var(--grid2);border-radius:50%}
.casef .rail .vlab{position:absolute;top:56%;left:50%;transform:translate(-50%,-50%) rotate(180deg);writing-mode:vertical-rl;
font-family:'JetBrains Mono',monospace;font-size:7.5px;letter-spacing:.28em;color:var(--dim);white-space:nowrap}
.casef .rstamp{position:absolute;top:-13px;right:20px;transform:rotate(-6deg);border:2px solid var(--fc);border-radius:6px;
padding:4px 11px;font-family:'JetBrains Mono',monospace;font-weight:700;font-size:9px;letter-spacing:.22em;color:var(--fc);background:var(--bg);z-index:6}
.p03 .folder{padding-left:64px}

/* field report (p05) */
.p05 .reality{padding:10px 14px 6px}
.p05 .fh{display:flex;justify-content:space-between;font-family:'JetBrains Mono',monospace;font-weight:600;font-size:8px;letter-spacing:.2em;color:var(--dim);margin-bottom:6px}
.p05 .fh b{color:var(--emb)}
.p05 .frow{display:flex;align-items:center;gap:9px;padding:4px 0;border-bottom:1px dotted var(--grid2);font-size:10.8px;color:var(--mut)}
.p05 .frow:last-child{border-bottom:0}
.p05 .frow .o{flex:none;width:12px;height:12px;border:1.5px solid var(--emb);border-radius:50%;position:relative}
.p05 .frow .o::after{content:"";position:absolute;left:2.5px;right:2.5px;top:50%;height:1.5px;margin-top:-1px;background:var(--emb)}
.p05 .frow .st2{margin-left:auto;font-family:'JetBrains Mono',monospace;font-size:7px;letter-spacing:.12em;color:var(--dim)}
.p06 .g1 svg{width:52px!important;height:52px!important}
.p04 .crumb2{position:absolute;top:176px;left:72px;font-family:'JetBrains Mono',monospace;font-size:9px;letter-spacing:.16em;color:var(--dim)}
.p04 .crumb2 b{color:var(--emb)}
"""
s=s.replace("</style>",CSS+"</style>",1)

# ================= 4. TAB-ROWS + RAILS per case page =================
def tabrow(nm,fl,ghost):
    g='<div class="tB">%s</div>'%ghost if ghost else ''
    return ('<div class="tabrow"><div class="tA"><span class="nm">%s</span><span class="fl">%s</span></div>%s</div>')%(nm,fl,g)
def rail(vlab):
    return ('<div class="rail"><span class="hole" style="top:86px"></span><span class="hole" style="top:132px"></span>'
            '<div class="vlab">%s</div></div>')%vlab

FLIPS=[
 # (old flip html, new tabrow, rail label, optional stamp)
 ('<div class="flip"><span class="nm">XTIX</span><span class="fl">FILE 01</span></div>',
  tabrow("XTIX","&#9656; INTAKE","EVIDENCE &#8250;"), "CASE FILE N&deg; 01 &middot; XTIX &middot; OPENED 2026",
  '<div class="rstamp">RECEIVED &middot; 2026</div>'),
 ('<div class="flip"><span class="nm">XTIX</span><span class="fl">FILE 01 &middot; EVIDENCE</span></div>',
  tabrow("XTIX","&#9656; EVIDENCE","&#8249; INTAKE"), "CASE FILE N&deg; 01 &middot; XTIX &middot; EVIDENCE", ""),
 ('<div class="flip"><span class="nm">Oasis</span><span class="fl">FILE 02</span></div>',
  tabrow("Oasis","&#9656; COMMAND","EVIDENCE &#8250;"), "CASE FILE N&deg; 02 &middot; OASIS &middot; OPENED 2026",
  '<div class="rstamp">RECEIVED &middot; 2026</div>'),
 ('<div class="flip"><span class="nm">Oasis</span><span class="fl">FILE 02 &middot; EVIDENCE</span></div>',
  tabrow("Oasis","&#9656; EVIDENCE","&#8249; COMMAND"), "CASE FILE N&deg; 02 &middot; OASIS &middot; EVIDENCE", ""),
 ('<div class="flip"><span class="nm">Eventer</span><span class="fl">FILE 03</span></div>',
  tabrow("Eventer","&#9656; SYNC","NEXT &middot; MEDCOIN &#8250;"), "CASE FILE N&deg; 03 &middot; EVENTER &middot; OPENED 2026",
  '<div class="rstamp">SYNCED &middot; 2026</div>'),
 ('<div class="flip"><span class="nm">Medcoin</span><span class="fl">FILE 04</span></div>',
  tabrow("Medcoin","&#9656; ORIGIN","&#8249; EVENTER"), "CASE FILE N&deg; 04 &middot; MEDCOIN &middot; FOUNDER", ""),
 ('<div class="flip"><span class="nm">Leadership</span><span class="fl">MANAGEMENT FILE</span></div>',
  tabrow("Leadership","&#9656; DOCTRINE","AI SYSTEM &#8250;"), "MANAGEMENT FILE &middot; PRINCIPLES &amp; TOOLKIT", ""),
 ('<div class="flip"><span class="nm">Technology</span><span class="fl">SYSTEM FILE &middot; AI</span></div>',
  tabrow("Technology","&#9656; AI SYSTEM","&#8249; DOCTRINE"), "SYSTEM FILE &middot; COMMERCIAL INTELLIGENCE", ""),
 ('<div class="flip"><span class="nm">The Builder</span><span class="fl">FINAL THOUGHTS</span></div>',
  tabrow("The Builder","&#9656; END OF FILE","&#8249; ARCHIVE"), "FINAL THOUGHTS &middot; THE BUILDER'S PRINCIPLES", ""),
]
cnt=0
for old,new,vlab,stamp in FLIPS:
    if old in s:
        s=s.replace(old,new+'\n    '+rail(vlab)+(('\n    '+stamp) if stamp else ''),1)
        cnt+=1
print("tabrows applied:",cnt,"/9")

# p03 master file flip -> tabrow
old3='<div class="flip"><span class="sq"></span>MASTER FILE &middot; THE 8 PRINCIPLES</div>'
new3=('<div class="tabrow"><div class="tA" style="background:var(--emb)"><span class="fl" style="color:rgba(12,13,16,.62)">&#9670;</span>'
'<span class="fl" style="font-size:9px">MASTER FILE &middot; THE 8 PRINCIPLES</span></div>'
'<div class="tB">THE CASE FILES &#8250;</div></div>\n    '
+rail("MASTER FILE &middot; THE COMMERCIAL OPERATING SYSTEM"))
if old3 in s:
    s=s.replace(old3,new3,1); print("p03 tabrow ok")

# ================= 5. P05 field report =================
old_re=re.search(r'<div class="reality"><span class="subl">BEFORE &middot; COMMERCIAL REALITY AT INTAKE</span>\s*<div class="rgrid">.*?</div>\s*</div>',s,flags=re.S)
assert old_re, "reality block"
gaps=["No CRM","No Business Development function","No sales methodology","No outbound process","No pipeline management","No KPI framework","No reporting structure"]
frows="".join('<div class="frow"><span class="o"></span>%s<span class="st2">GAP.%02d</span></div>'%(g,i+1) for i,g in enumerate(gaps))
newr=('<div class="reality"><div class="fh"><span><b>FIELD REPORT</b> &middot; BEFORE &middot; COMMERCIAL REALITY AT INTAKE</span><span>07 GAPS</span></div>'
+frows+'</div>')
s=s[:old_re.start()]+newr+s[old_re.end():]
print("field report in")

# ================= 6. P04 crumb =================
s=s.replace('<div class="meta">EXECUTIVE PORTFOLIO &middot; 04 DOSSIERS &middot; 2018&ndash;2026</div>',
'<div class="meta">EXECUTIVE PORTFOLIO &middot; 04 DOSSIERS &middot; 2018&ndash;2026</div>\n  <div class="crumb2">ARCHIVE://COMMERCIAL/2026 <b>&#8250;</b> ORAN_CARMON <b>&#8250;</b> CASE_FILES</div>',1)

io.open(p,"w",encoding="utf-8").write(s)
print("dossier rollout done")
