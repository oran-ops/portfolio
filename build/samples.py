# -*- coding: utf-8 -*-
# Mission A — 3 dossier-direction sample pages (NOT applied to the doc)
import io

HTML="""<!doctype html><html lang="en"><head><meta charset="utf-8">
<title>DOSSIER DIRECTION — SAMPLES</title>
<link rel="stylesheet" href="fonts/fonts_dossier.css">
<style>
:root{--bg:#131417;--card:#1A1B1F;--card2:#1F2126;--ink:#F2F1ED;--mut:#8E8E93;--dim:#5A5B60;--grid:#2E3036;--grid2:#46494F;
--hair:rgba(255,255,255,.09);--emb:#F4603E;--brass:#E0A458;--ice:#7CC4E8;--dk:#0C0D10}
*{margin:0;padding:0;box-sizing:border-box}
@page{size:1280px 720px;margin:0}
html,body{background:#000}
.page{position:relative;width:1280px;height:720px;overflow:hidden;background:var(--bg);color:var(--ink);
font-family:'Inter',system-ui,sans-serif;-webkit-font-smoothing:antialiased;page-break-after:always}
.page:last-child{page-break-after:auto}
.mono{font-family:'JetBrains Mono',monospace}
.brk{position:absolute;width:20px;height:20px;z-index:9;border:0 solid rgba(242,241,237,.38)}
.brk.tl{top:26px;left:26px;border-top-width:1.5px;border-left-width:1.5px}
.brk.tr{top:26px;right:26px;border-top-width:1.5px;border-right-width:1.5px}
.brk.bl{bottom:26px;left:26px;border-bottom-width:1.5px;border-left-width:1.5px}
.brk.br{bottom:26px;right:26px;border-bottom-width:1.5px;border-right-width:1.5px}
.ftr{position:absolute;left:72px;right:72px;bottom:44px;z-index:9;display:flex;align-items:center;justify-content:space-between;
font-family:'JetBrains Mono',monospace;font-size:9.5px;letter-spacing:.18em;color:var(--dim)}
.ftr b{color:var(--mut);font-weight:600}

/* ============ SAMPLE 1 — COVER = THE MASTER FOLDER ============ */
.s1 .idx{position:absolute;top:44px;left:64px;font-family:'JetBrains Mono',monospace;font-size:10px;letter-spacing:.22em;color:var(--mut);line-height:2.2}
.s1 .idx .k{color:var(--dim)}
.s1 .idx .em{color:var(--emb);font-weight:600}
.s1 .idx .br2{color:var(--brass);font-weight:600}
.s1 .crumb{position:absolute;top:118px;left:64px;font-family:'JetBrains Mono',monospace;font-size:10px;letter-spacing:.16em;color:var(--dim)}
.s1 .crumb b{color:var(--emb);font-weight:600}
.s1 .barc{position:absolute;top:44px;right:64px;text-align:center}
.s1 .barc .yr{margin-top:4px;font-family:'JetBrains Mono',monospace;font-size:8px;letter-spacing:.3em;color:var(--dim)}
.s1 .folder{position:absolute;top:196px;left:64px;right:64px;bottom:52px;background:var(--emb);border-radius:0 26px 22px 22px}
.s1 .flip{position:absolute;top:-40px;left:-1px;height:40px;background:var(--emb);border-radius:11px 24px 0 0;
display:flex;align-items:center;gap:15px;padding:0 22px}
.s1 .flip .nm{font-family:'Fraunces',serif;font-weight:600;font-size:19px;color:var(--dk)}
.s1 .flip .fl{font-family:'JetBrains Mono',monospace;font-weight:700;font-size:9px;letter-spacing:.2em;color:rgba(12,13,16,.6)}
.s1 .hole{position:absolute;left:26px;width:15px;height:15px;border:2px solid rgba(12,13,16,.38);border-radius:50%}
.s1 .kick{position:absolute;top:52px;left:0;right:0;text-align:center;font-family:'JetBrains Mono',monospace;font-weight:700;font-size:10.5px;letter-spacing:.5em;color:rgba(12,13,16,.62)}
.s1 h1{position:absolute;top:86px;left:0;right:0;text-align:center;font-weight:800;font-size:64px;line-height:1.04;letter-spacing:-.03em;color:var(--dk)}
.s1 .sub{position:absolute;top:242px;left:0;right:0;text-align:center;font-family:'Fraunces',serif;font-style:italic;font-weight:500;font-size:22px;color:rgba(12,13,16,.82)}
.s1 .rule{position:absolute;top:292px;left:50%;transform:translateX(-50%);display:flex;align-items:center;gap:12px}
.s1 .rule .ln{width:64px;height:1px;background:rgba(12,13,16,.35)}
.s1 .rule .d{width:7px;height:7px;background:var(--dk);transform:rotate(45deg)}
.s1 .by{position:absolute;top:314px;left:0;right:0;text-align:center;font-family:'JetBrains Mono',monospace;font-weight:600;font-size:10px;letter-spacing:.3em;color:rgba(12,13,16,.72)}
.s1 .by b{color:var(--dk);font-weight:800}
.s1 .stamp{position:absolute;top:30px;right:34px;transform:rotate(6deg);border:2px solid rgba(12,13,16,.75);border-radius:7px;
padding:7px 14px;font-family:'JetBrains Mono',monospace;font-weight:700;font-size:10px;letter-spacing:.26em;color:rgba(12,13,16,.85)}
.s1 .tagl{position:absolute;left:30px;bottom:22px;font-family:'JetBrains Mono',monospace;font-size:8.5px;letter-spacing:.2em;color:rgba(12,13,16,.6)}
.s1 .inner{position:absolute;right:30px;bottom:0;display:flex;gap:10px;align-items:flex-end}
.s1 .itab{height:34px;border-radius:8px 16px 0 0;display:flex;align-items:center;gap:10px;padding:0 14px}
.s1 .itab .nm2{font-family:'Fraunces',serif;font-weight:500;font-size:13.5px;color:var(--dk)}
.s1 .itab .fl2{font-family:'JetBrains Mono',monospace;font-size:7.5px;letter-spacing:.14em;color:rgba(12,13,16,.6)}

/* ============ SAMPLE 2 — STATEMENT = SPINE + MEMO ============ */
.s2 .spine{position:absolute;top:0;bottom:0;left:0;width:112px;display:flex;flex-direction:column}
.s2 .sp{flex:1;position:relative}
.s2 .sp span{position:absolute;top:14px;left:50%;transform:translateX(-50%);writing-mode:vertical-rl;
font-family:'JetBrains Mono',monospace;font-weight:700;font-size:9px;letter-spacing:.3em;color:rgba(12,13,16,.72)}
.s2 .rub{position:absolute;top:48px;left:170px;display:flex;align-items:center;gap:11px;font-family:'JetBrains Mono',monospace;font-weight:700;font-size:10.5px;letter-spacing:.26em;color:var(--ink)}
.s2 .rub .d{width:7px;height:7px;background:var(--emb);transform:rotate(45deg)}
.s2 .tok{position:absolute;top:40px;right:64px;font-family:'JetBrains Mono',monospace;font-weight:600;font-size:9.5px;letter-spacing:.16em;
border:1px solid var(--grid);border-radius:7px;padding:6px 12px;color:var(--emb)}
.s2 .in{position:absolute;left:112px;right:0;top:50%;transform:translateY(-52%);text-align:center;padding:0 70px}
.s2 .memo{display:inline-flex;background:var(--emb);color:var(--dk);border-radius:7px 16px 0 0;
padding:9px 17px;font-family:'JetBrains Mono',monospace;font-weight:700;font-size:9.5px;letter-spacing:.22em;margin-bottom:34px}
.s2 .l1{font-weight:800;font-size:45px;letter-spacing:-.03em;line-height:1.16;color:var(--ink)}
.s2 .l2{font-weight:800;font-size:45px;letter-spacing:-.03em;line-height:1.16;color:var(--emb);margin-top:26px}
.s2 .sig{margin-top:38px;font-family:'JetBrains Mono',monospace;font-size:9px;letter-spacing:.26em;color:var(--dim)}
.s2 .pn{position:absolute;right:64px;bottom:44px;font-family:'JetBrains Mono',monospace;font-size:9.5px;letter-spacing:.18em;color:var(--dim)}
.s2 .pn b{color:var(--mut);font-weight:600}

/* ============ SAMPLE 3 — CASE PAGE = TAB ROW + FIELD FORM ============ */
.s3 .hd{position:absolute;top:48px;left:72px;right:72px;display:flex;justify-content:space-between;align-items:center}
.s3 .rub{display:flex;align-items:center;gap:11px;font-family:'JetBrains Mono',monospace;font-weight:700;font-size:10.5px;letter-spacing:.26em;color:var(--ink)}
.s3 .rub .d{width:7px;height:7px;background:var(--emb);transform:rotate(45deg)}
.s3 .tok{font-family:'JetBrains Mono',monospace;font-weight:600;font-size:9.5px;letter-spacing:.16em;border:1px solid var(--grid);border-radius:7px;padding:6px 12px;color:var(--emb)}
.s3 .ttl{position:absolute;top:82px;left:72px;font-weight:800;font-size:30px;letter-spacing:-.025em}
.s3 .meta{position:absolute;top:124px;left:72px;font-family:'JetBrains Mono',monospace;font-size:9.5px;letter-spacing:.22em;color:var(--mut)}
.s3 .tabs{position:absolute;top:156px;left:72px;display:flex;gap:8px;align-items:flex-end}
.s3 .tA{height:34px;background:var(--emb);border-radius:9px 20px 0 0;display:flex;align-items:center;gap:11px;padding:0 18px;position:relative;top:1px;z-index:3}
.s3 .tA .nm{font-family:'Fraunces',serif;font-weight:500;font-size:15px;color:var(--dk)}
.s3 .tA .fl{font-family:'JetBrains Mono',monospace;font-weight:700;font-size:8.5px;letter-spacing:.18em;color:rgba(12,13,16,.62)}
.s3 .tB{height:28px;border:1.5px dashed var(--grid2);border-bottom:0;border-radius:9px 18px 0 0;display:flex;align-items:center;padding:0 16px;position:relative;top:1px;
font-family:'JetBrains Mono',monospace;font-weight:600;font-size:8.5px;letter-spacing:.18em;color:var(--dim)}
.s3 .folder{position:absolute;top:190px;left:72px;right:72px;height:456px;background:var(--card);border:1px solid var(--hair);
border-radius:0 16px 16px 16px;padding:24px 30px 18px 76px}
.s3 .rail{position:absolute;left:0;top:0;bottom:0;width:52px;border-right:1px dashed var(--grid)}
.s3 .rail .hole{position:absolute;left:17px;width:16px;height:16px;border:2px solid var(--grid2);border-radius:50%}
.s3 .rail .vlab{position:absolute;top:50%;left:50%;transform:translate(-50%,-50%) rotate(180deg);writing-mode:vertical-rl;
font-family:'JetBrains Mono',monospace;font-size:8px;letter-spacing:.3em;color:var(--dim);white-space:nowrap}
.s3 .stamp{position:absolute;top:-14px;right:22px;transform:rotate(-6deg);border:2px solid var(--emb);border-radius:6px;
padding:5px 12px;font-family:'JetBrains Mono',monospace;font-weight:700;font-size:9.5px;letter-spacing:.24em;color:var(--emb);background:var(--bg);z-index:5}
.s3 .cols{display:grid;grid-template-columns:1fr 1fr;column-gap:34px}
.s3 .zr{display:flex;align-items:center;gap:9px;font-family:'JetBrains Mono',monospace;font-weight:700;font-size:10px;letter-spacing:.22em;color:var(--ink);margin-bottom:9px}
.s3 .zr b{color:var(--emb)}
.s3 .zr .d2{width:5px;height:5px;background:var(--emb);transform:rotate(45deg)}
.s3 .para{font-size:12px;line-height:1.55;color:var(--mut)}
.s3 .para b{color:var(--ink);font-weight:600}
.s3 .z{margin-bottom:15px}
.s3 .form{border:1px solid var(--grid);border-radius:12px;background:var(--card2);padding:13px 16px 9px;margin-top:10px}
.s3 .form .fh{display:flex;justify-content:space-between;font-family:'JetBrains Mono',monospace;font-weight:600;font-size:8.5px;letter-spacing:.22em;color:var(--dim);margin-bottom:9px}
.s3 .form .fh b{color:var(--emb)}
.s3 .frow{display:flex;align-items:center;gap:10px;padding:5.5px 0;border-bottom:1px dotted var(--grid2);font-size:11.5px;color:var(--mut)}
.s3 .frow:last-child{border-bottom:0}
.s3 .frow .o{flex:none;width:13px;height:13px;border:1.5px solid var(--emb);border-radius:50%;position:relative}
.s3 .frow .o::after{content:"";position:absolute;left:2.5px;right:2.5px;top:50%;height:1.5px;margin-top:-1px;background:var(--emb)}
.s3 .frow .st2{margin-left:auto;font-family:'JetBrains Mono',monospace;font-size:7.5px;letter-spacing:.14em;color:var(--dim)}
.s3 .dash{display:flex;align-items:center;gap:9px;font-size:11.8px;color:var(--mut);margin-bottom:6px}
.s3 .dash::before{content:"";flex:none;width:9px;height:2px;background:var(--emb)}
.s3 .then{margin-top:8px;font-family:'Fraunces',serif;font-style:italic;font-size:13px;color:var(--emb)}
.s3 .lg{display:flex;align-items:center;gap:9px;font-size:11.6px;font-weight:600;color:var(--ink);margin-bottom:6.5px}
.s3 .lg .n{font-family:'JetBrains Mono',monospace;font-size:7.5px;letter-spacing:.1em;color:var(--dim);width:38px;flex:none}
.s3 .lg .c{flex:none;width:11px;height:11px;background:var(--emb);color:var(--dk);font-size:9px;font-weight:800;line-height:11px;text-align:center}
</style></head><body>

<!-- ============ SAMPLE 1 ============ -->
<section class="page s1">
  <span class="brk tl"></span><span class="brk tr"></span><span class="brk bl"></span><span class="brk br"></span>
  <div class="idx">
    <span class="k">ARCHIVE N&deg;</span> 2026-04<br>
    <span class="k">CLASSIFICATION:</span> <span class="em">COMMERCIAL</span><br>
    <span class="k">STATUS:</span> <span class="br2">ACTIVE</span>
  </div>
  <div class="crumb">ARCHIVE://COMMERCIAL/2026 <b>&#8250;</b> ORAN_CARMON <b>&#8250;</b> MASTER_FILE</div>
  <div class="barc">
    <svg viewBox="0 0 62 30" style="width:62px;height:30px"><rect x="0" y="0" width="2" height="30" fill="#F2F1ED"/><rect x="3" y="0" width="1" height="30" fill="#8E8E93"/><rect x="6" y="0" width="3" height="30" fill="#8E8E93"/><rect x="11" y="0" width="1" height="30" fill="#F2F1ED"/><rect x="14" y="0" width="2" height="30" fill="#8E8E93"/><rect x="18" y="0" width="1" height="30" fill="#8E8E93"/><rect x="21" y="0" width="1" height="30" fill="#F2F1ED"/><rect x="24" y="0" width="3" height="30" fill="#8E8E93"/><rect x="29" y="0" width="2" height="30" fill="#8E8E93"/><rect x="33" y="0" width="1" height="30" fill="#F2F1ED"/><rect x="36" y="0" width="2" height="30" fill="#8E8E93"/><rect x="40" y="0" width="3" height="30" fill="#8E8E93"/><rect x="45" y="0" width="1" height="30" fill="#F2F1ED"/><rect x="48" y="0" width="2" height="30" fill="#8E8E93"/><rect x="52" y="0" width="1" height="30" fill="#8E8E93"/><rect x="55" y="0" width="3" height="30" fill="#F2F1ED"/><rect x="60" y="0" width="1" height="30" fill="#8E8E93"/></svg>
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
    <div class="tagl">A PRACTICAL GUIDE TO BUILDING COMMERCIAL ORGANIZATIONS THAT SCALE</div>
    <div class="inner">
      <div class="itab" style="background:var(--brass);height:30px"><span class="nm2">Oasis</span><span class="fl2">FILE 02</span></div>
      <div class="itab" style="background:var(--ice);height:36px"><span class="nm2">Eventer</span><span class="fl2">FILE 03</span></div>
      <div class="itab" style="background:var(--ink);height:42px"><span class="nm2">Medcoin</span><span class="fl2">FILE 04</span></div>
    </div>
  </div>
</section>

<!-- ============ SAMPLE 2 ============ -->
<section class="page s2">
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
</section>

<!-- ============ SAMPLE 3 ============ -->
<section class="page s3">
  <span class="brk tl"></span><span class="brk tr"></span><span class="brk bl"></span><span class="brk br"></span>
  <div class="hd">
    <div class="rub"><span class="d"></span>CASE STUDY 01</div>
    <div class="tok">FILE 01 &middot; INTAKE</div>
  </div>
  <div class="ttl">Building a Commercial Function From Zero</div>
  <div class="meta">XTIX &middot; FINTECH SAAS &middot; EARLY-STAGE STARTUP</div>
  <div class="tabs">
    <div class="tA"><span class="nm">XTIX</span><span class="fl">&#9656; INTAKE</span></div>
    <div class="tB">EVIDENCE &#8250;</div>
  </div>
  <div class="folder">
    <div class="rail">
      <span class="hole" style="top:96px"></span><span class="hole" style="top:150px"></span>
      <div class="vlab">CASE FILE N&deg; 01 &middot; XTIX &middot; OPENED 2026</div>
    </div>
    <div class="stamp">RECEIVED &middot; ARCHIVE 2026</div>
    <div class="cols">
      <div>
        <div class="z">
          <div class="zr"><b>01</b><span class="d2"></span>THE SITUATION</div>
          <div class="para">When I joined XTIX, the company had a <b>strong vision and product</b> &mdash; but no commercial infrastructure to support scalable growth.</div>
        </div>
        <div class="form">
          <div class="fh"><span><b>FIELD REPORT</b> &middot; BEFORE &middot; COMMERCIAL REALITY AT INTAKE</span><span>07 GAPS</span></div>
          <div class="frow"><span class="o"></span>No CRM<span class="st2">GAP.01</span></div>
          <div class="frow"><span class="o"></span>No Business Development function<span class="st2">GAP.02</span></div>
          <div class="frow"><span class="o"></span>No sales methodology<span class="st2">GAP.03</span></div>
          <div class="frow"><span class="o"></span>No outbound process<span class="st2">GAP.04</span></div>
          <div class="frow"><span class="o"></span>No pipeline management<span class="st2">GAP.05</span></div>
          <div class="frow"><span class="o"></span>No KPI framework<span class="st2">GAP.06</span></div>
          <div class="frow"><span class="o"></span>No reporting structure<span class="st2">GAP.07</span></div>
        </div>
        <div class="z" style="margin-top:14px;margin-bottom:0">
          <div class="zr"><b>02</b><span class="d2"></span>MISSION OBJECTIVE</div>
          <div class="para">Design and build a <b>commercial operating system</b> capable of supporting predictable business growth &mdash; starting with the Israeli market and later expanding globally.</div>
        </div>
      </div>
      <div>
        <div class="z">
          <div class="zr"><b>03</b><span class="d2"></span>MY APPROACH</div>
          <div class="para">Rather than launching outbound immediately, I focused on <b>understanding the business first</b>:</div>
          <div style="display:grid;grid-template-columns:1fr 1fr;gap:5px 14px;margin-top:9px">
            <div class="dash">Business &amp; product analysis</div><div class="dash">Market research</div>
            <div class="dash">Competitive analysis</div><div class="dash">ICP definition</div>
            <div class="dash">Customer segmentation</div><div class="dash">Commercial positioning</div>
          </div>
          <div class="then">Only then did execution begin.</div>
        </div>
        <div class="z" style="margin-bottom:0">
          <div class="zr"><b>04</b><span class="d2"></span>WHAT I BUILT &middot; AFTER</div>
          <div style="display:grid;grid-template-columns:1fr 1fr;gap:5px 14px">
            <div class="lg"><span class="n">LOG.01</span><span class="c">&#10003;</span>Commercial Strategy</div>
            <div class="lg"><span class="n">LOG.02</span><span class="c">&#10003;</span>HubSpot CRM Infrastructure</div>
            <div class="lg"><span class="n">LOG.03</span><span class="c">&#10003;</span>Business Development Process</div>
            <div class="lg"><span class="n">LOG.04</span><span class="c">&#10003;</span>Sales Pipeline</div>
            <div class="lg"><span class="n">LOG.05</span><span class="c">&#10003;</span>ICP Framework</div>
            <div class="lg"><span class="n">LOG.06</span><span class="c">&#10003;</span>Outbound Sequences</div>
            <div class="lg"><span class="n">LOG.07</span><span class="c">&#10003;</span>KPI Framework</div>
            <div class="lg"><span class="n">LOG.08</span><span class="c">&#10003;</span>Forecasting Structure</div>
            <div class="lg"><span class="n">LOG.09</span><span class="c">&#10003;</span>Reporting Dashboards</div>
            <div class="lg"><span class="n">LOG.10</span><span class="c">&#10003;</span>AI-Powered Outbound Engine</div>
          </div>
        </div>
      </div>
    </div>
  </div>
  <div class="ftr">
    <span>THE COMMERCIAL SYSTEMS BUILDER</span>
    <span><b>P.05</b> &mdash; 13 &middot; SAMPLE</span>
  </div>
</section>
</body></html>"""

io.open("samples.html","w",encoding="utf-8").write(HTML)
print("samples.html written")
