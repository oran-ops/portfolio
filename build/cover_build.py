# -*- coding: utf-8 -*-
# LinkedIn cover 1584x396 — two variants on the EMERALD dossier language.
import io

BASE_CSS = """
:root{--bg:#191A1F;--card:#202127;--card2:#25262D;--ink:#F2F1ED;--mut:#8E8E93;--lbl:#A6A7AC;
--grid:#33353C;--grid2:#4B4E55;--hair:rgba(255,255,255,.09);--emb:#2FB380;--brass:#E0A458;--ice:#5E8FBF}
*{margin:0;padding:0;box-sizing:border-box}
html,body{width:1584px;height:396px;overflow:hidden}
body{background:var(--bg);font-family:Inter,sans-serif;color:var(--ink);position:relative}
.brk{position:absolute;width:26px;height:26px;border:2px solid var(--grid2)}
.brk.tl{top:22px;left:26px;border-right:0;border-bottom:0}
.brk.tr{top:22px;right:26px;border-left:0;border-bottom:0}
.brk.bl{bottom:22px;left:26px;border-right:0;border-top:0}
.brk.br{bottom:22px;right:26px;border-left:0;border-top:0}
.crumb{position:absolute;top:34px;left:70px;font-family:'JetBrains Mono',monospace;font-weight:600;
font-size:11px;letter-spacing:.22em;color:var(--mut)}
.crumb b{color:var(--emb);font-weight:600}
.tag{position:absolute;top:34px;right:70px;display:flex;align-items:center;gap:12px;
font-family:'JetBrains Mono',monospace;font-weight:700;font-size:11px;letter-spacing:.3em;color:var(--lbl)}
.tag i{width:9px;height:9px;background:var(--emb);transform:rotate(45deg)}
.ghost{position:absolute;font-weight:800;letter-spacing:-.03em;color:transparent;
-webkit-text-stroke:1.1px rgba(255,255,255,.05);white-space:nowrap;line-height:1}
"""

A = """<!doctype html><html><head><meta charset="utf-8">
<link rel="stylesheet" href="fonts/fonts_dossier.css">
<style>""" + BASE_CSS + """
.ghost.g1{font-size:300px;top:-60px;left:-40px}
.ghost.g2{font-size:300px;bottom:-78px;right:-60px}
.mid{position:absolute;left:50%;top:47%;transform:translate(-50%,-50%);text-align:center;width:1100px}
.kick{font-family:'JetBrains Mono',monospace;font-weight:700;font-size:12px;letter-spacing:.55em;color:var(--emb);margin-bottom:18px}
h1{font-weight:800;font-size:74px;line-height:1.02;letter-spacing:-.028em;white-space:nowrap}
.sub{margin-top:14px;font-family:'Fraunces',serif;font-style:italic;font-weight:500;font-size:25px;color:var(--emb)}
.tabs{position:absolute;right:96px;bottom:0;display:flex;gap:12px;align-items:flex-end}
.tb{border-radius:9px 14px 0 0;display:flex;align-items:center;gap:9px;padding:0 18px;height:44px}
.tb .nm{font-family:'Fraunces',serif;font-weight:600;font-size:15.5px;color:#191A1F}
.tb .fl{font-family:'JetBrains Mono',monospace;font-weight:700;font-size:8px;letter-spacing:.16em;color:rgba(25,26,31,.8)}
.tb.t1{background:var(--emb);height:58px}
.tb.t2{background:var(--brass);height:50px}
.tb.t3{background:var(--ice);height:44px}
.tb.t4{background:var(--ink);height:38px}
.hairline{position:absolute;left:70px;right:70px;bottom:74px;height:1px;
background:repeating-linear-gradient(90deg,var(--grid) 0 6px,transparent 6px 14px)}
.holes{position:absolute;left:70px;top:50%;transform:translateY(-50%);display:flex;flex-direction:column;gap:22px}
.holes span{width:15px;height:15px;border:2px solid var(--grid2);border-radius:50%}
</style></head><body>
<span class="brk tl"></span><span class="brk tr"></span><span class="brk bl"></span><span class="brk br"></span>
<div class="ghost g1">COMMERCIAL</div>
<div class="ghost g2">SYSTEMS</div>
<div class="crumb">ARCHIVE://COMMERCIAL/2026 <b>&#8250;</b> ORAN_CARMON <b>&#8250;</b> MASTER_FILE</div>
<div class="tag">EXECUTIVE PORTFOLIO &middot; 2026<i></i></div>
<div class="holes"><span></span><span></span></div>
<div class="mid">
  <div class="kick">O R A N &nbsp; C A R M O N</div>
  <h1>THE COMMERCIAL SYSTEMS BUILDER</h1>
  <div class="sub">From Vision to Measurable Growth</div>
</div>
<div class="hairline"></div>
<div class="tabs">
  <div class="tb t1"><span class="nm">XTIX</span><span class="fl">FILE 01</span></div>
  <div class="tb t2"><span class="nm">Oasis</span><span class="fl">FILE 02</span></div>
  <div class="tb t3"><span class="nm">Eventer</span><span class="fl">FILE 03</span></div>
  <div class="tb t4"><span class="nm">Medcoin</span><span class="fl">FILE 04</span></div>
</div>
</body></html>"""

B = """<!doctype html><html><head><meta charset="utf-8">
<link rel="stylesheet" href="fonts/fonts_dossier.css">
<style>""" + BASE_CSS + """
.ghost.g1{font-size:280px;top:-52px;left:-30px;-webkit-text-stroke:1.1px rgba(255,255,255,.045)}
.folder{position:absolute;right:0;top:64px;bottom:0;width:880px;background:var(--emb);border-radius:22px 0 0 0;padding:64px 70px 0 74px}
.flip{position:absolute;top:-42px;left:0;height:42px;background:var(--emb);border-radius:11px 22px 0 0;
display:flex;align-items:center;gap:14px;padding:0 24px}
.flip .nm{font-family:'Fraunces',serif;font-weight:600;font-size:20px;color:#191A1F}
.flip .fl{font-family:'JetBrains Mono',monospace;font-weight:700;font-size:9px;letter-spacing:.2em;color:rgba(25,26,31,.85)}
.folder .kick{font-family:'JetBrains Mono',monospace;font-weight:700;font-size:11px;letter-spacing:.5em;color:rgba(25,26,31,.72);margin-bottom:14px}
.folder h1{font-weight:800;font-size:62px;line-height:1.03;letter-spacing:-.028em;color:#191A1F}
.folder .sub{margin-top:12px;font-family:'Fraunces',serif;font-style:italic;font-weight:500;font-size:23px;color:rgba(25,26,31,.9)}
.folder .hole{position:absolute;left:26px;width:15px;height:15px;border:2px solid rgba(25,26,31,.4);border-radius:50%}
.stmt{position:absolute;left:70px;top:120px;width:520px}
.stmt .l1{font-weight:800;font-size:30px;line-height:1.25;color:var(--ink)}
.stmt .l2{font-weight:800;font-size:30px;line-height:1.25;color:var(--emb);margin-top:6px}
.stmt .who{margin-top:18px;font-family:'JetBrains Mono',monospace;font-weight:700;font-size:10px;letter-spacing:.3em;color:var(--mut)}
</style></head><body>
<span class="brk tl"></span><span class="brk bl"></span>
<div class="ghost g1">BUILDER</div>
<div class="crumb">ARCHIVE://COMMERCIAL/2026 <b>&#8250;</b> ORAN_CARMON</div>
<div class="stmt">
  <div class="l1">One intelligence built the world.</div>
  <div class="l2">Two will build the next.</div>
  <div class="who">ORAN CARMON &middot; EXECUTIVE PORTFOLIO &middot; 2026</div>
</div>
<div class="folder">
  <div class="flip"><span class="nm">Oran Carmon</span><span class="fl">MASTER FILE</span></div>
  <span class="hole" style="top:56px"></span><span class="hole" style="top:96px"></span>
  <div class="kick">E X E C U T I V E &nbsp; P O R T F O L I O</div>
  <h1>THE COMMERCIAL<br>SYSTEMS BUILDER</h1>
  <div class="sub">From Vision to Measurable Growth</div>
</div>
</body></html>"""

io.open("coverA.html", "w", encoding="utf-8").write(A)
io.open("coverB.html", "w", encoding="utf-8").write(B)
print("covers written")
