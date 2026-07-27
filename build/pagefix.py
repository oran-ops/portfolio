# -*- coding: utf-8 -*-
# PDF polish pass: global lip-gap fix, Medcoin -> dark, P09 label, P11 rhythm
import io, re
p="casebook.html"; s=io.open(p,encoding="utf-8").read()

# ---------- 1. GLOBAL: breathing room between meta line and folder tab lip ----------
css="""
/* polish pass */
.casef .ttl{top:82px}
.casef .meta{top:124px}
.casef .folder{top:184px;height:462px}
.p06 .folder{height:472px}
.p09 .folder{height:472px}
.p12 .folder{height:476px}
.p11 .pr{margin-bottom:16px}
.p11 .cols{margin-top:22px}
.p11 .sigq{margin-top:22px}

/* ============ PAGE 10B - MEDCOIN ORIGIN (DARK, WHITE FILE) ============ */
.p10b .folder{padding:22px 28px 16px}
.p10b .inner{display:grid;grid-template-columns:53fr 47fr;column-gap:30px}
.p10b .zr{margin-bottom:7px}
.p10b .z{margin-bottom:12px}
.p10b .para{font-size:11.4px;line-height:1.5}
.p10b .bgrid{display:grid;grid-template-columns:1fr 1fr;gap:5.5px 14px}
.p10b .lg{font-size:10.7px;font-weight:600}
.p10b .lg .c2{flex:none;width:11px;height:11px;background:var(--ink);color:#0C0D10;font-size:9px;font-weight:800;line-height:11px;text-align:center;margin-right:8px}
.p10b .lg2{display:flex;align-items:center;font-size:10.7px;font-weight:600;color:var(--ink)}
.p10b .outs{position:relative;border:1px solid var(--grid);border-radius:0 12px 12px 12px;background:var(--card2);padding:4px 16px 6px}
.p10b .outs table{width:100%;border-collapse:collapse}
.p10b .outs td{border-top:1px solid var(--grid);padding:7px 0;vertical-align:middle}
.p10b .outs tr:first-child td{border-top:none}
.p10b .outs .k{font-family:'JetBrains Mono',monospace;font-size:8px;letter-spacing:.16em;color:var(--dim)}
.p10b .outs .v{text-align:right;font-weight:700;font-size:12px;color:var(--ink)}
.p10b .outs .v.em{color:var(--emb)}
.p10b .stamp{position:absolute;top:-14px;right:14px;transform:rotate(-7deg);border:2px solid var(--emb);border-radius:6px;
padding:5px 12px;font-family:'JetBrains Mono',monospace;font-weight:700;font-size:11px;letter-spacing:.3em;color:var(--emb);background:var(--bg)}
.p10b .tl2{margin-top:11px;padding-top:11px;border-top:1px solid var(--grid)}
.p10b .band2{margin-top:9px;padding-top:11px;border-top:1px solid var(--grid);display:grid;grid-template-columns:56fr 44fr;column-gap:30px}
.p10b .para3{font-size:10.7px;line-height:1.46;color:var(--mut)}
.p10b .para3 b{color:var(--ink);font-weight:600}
.p10b .lessq2{border-left:2px solid var(--ink);padding:2px 0 2px 16px}
.p10b .lessq2 .qx{font-family:'Fraunces',serif;font-style:italic;font-weight:500;font-size:13.6px;line-height:1.42;color:var(--ink)}
.p10b .lessq2 .qx b{color:var(--emb);font-weight:600}
.p10b .lessq2 .who{margin-top:5px;font-family:'JetBrains Mono',monospace;font-size:7.5px;letter-spacing:.24em;color:var(--dim)}
"""
s=s.replace("</style>",css+"</style>",1)

# ---------- 2. remove old paper P10 section ----------
s=re.sub(r'\n<!--[^\n]*PAGE 10 \. MEDCOIN ORIGIN[^\n]*-->\n<section class="page p10">.*?</section>\n','\n',s,flags=re.S)

# ---------- 3. new dark P10 ----------
built="".join('<div class="lg2"><span class="c2">&#10003;</span>%s</div>'%t for t in [
"Founded the company from scratch","Defined the business model","Built the commercial strategy",
"Established strategic partnerships","Raised external investment","Deployed cryptocurrency ATMs across Europe",
"Built operational &amp; regulatory processes","Managed financial-service providers &amp; international vendors",
"Designed the customer journey &amp; user experience"])
outs="".join('<tr><td class="k">%s</td><td class="v%s">%s</td></tr>'%(k," em" if em else "",v) for k,v,em in [
("MARKETS","Europe",False),("BUSINESS MODEL","Crypto ATM network",False),
("INVESTMENT","External investment raised",False),("REVENUE","Hundreds of thousands of &euro;",True),
("INFRASTRUCTURE","Operational ATM network deployed",False),("TEAM","Founder-led operation",False)])
ms=[("FOUNDED",40),("BUSINESS MODEL",255),("PARTNERSHIPS",470),("INVESTMENT RAISED",685),("ATMs ACROSS EUROPE",900)]
nodes=""
for i,(t,x) in enumerate(ms):
    last=(i==4)
    nodes+=('<circle cx="%d" cy="26" r="%s" fill="%s" stroke="#F2F1ED" stroke-width="1.6"/>'
            '<text x="%d" y="52" text-anchor="middle" font-size="7.2" letter-spacing="1.3" fill="#8E8E93">%s</text>'
            )%(x,"6" if last else "4.5","#F4603E" if last else "#0C0D10",x,t)
tline=('<svg viewBox="0 0 1040 58" style="width:100%;height:auto">'
       '<line x1="26" y1="26" x2="912" y2="26" stroke="#F2F1ED" stroke-width="1.3"/>'
       '<line x1="912" y1="26" x2="1014" y2="26" stroke="#F4603E" stroke-width="2" stroke-dasharray="4 4"/>'
       '<path d="M1020 26 l-9 -5 v10 z" fill="#F4603E"/>'
       +nodes+
       '<text x="968" y="14" text-anchor="middle" font-size="7.4" font-weight="700" letter-spacing="1.5" fill="#F4603E">REVENUE</text>'
       '</svg>')

page="""
<!-- ================= PAGE 10 . MEDCOIN ORIGIN ================= -->
<section class="page casef p10b" style="--fc:var(--ink)">
  <span class="brk tl"></span><span class="brk tr"></span><span class="brk bl"></span><span class="brk br"></span>
  <div class="hd">
    <div class="rub"><span class="d"></span>FOUNDER CASE STUDY</div>
    <div class="tok">FILE 04 &middot; ORIGIN</div>
  </div>
  <div class="ttl">Building a Business From Vision</div>
  <div class="meta">MEDCOIN TEKNOLOJI &middot; CRYPTO FINTECH &middot; FOUNDER</div>
  <div class="folder">
    <div class="flip"><span class="nm">Medcoin</span><span class="fl">FILE 04</span></div>
    <div class="inner">
      <div>
        <div class="z">
          <div class="zr"><b>01</b><span class="d2"></span>THE VISION</div>
          <div class="para">Create a <b>compliant, scalable cryptocurrency ATM business</b> serving the European market through secure, accessible digital financial services.</div>
        </div>
        <div class="z">
          <div class="zr"><b>02</b><span class="d2"></span>THE CHALLENGE</div>
          <div class="para">Building a company from zero meant making <b>every strategic decision</b> &mdash; from business model and partnerships to compliance, operations and commercialization.</div>
        </div>
        <div class="z" style="margin-bottom:0">
          <div class="zr"><b>03</b><span class="d2"></span>WHAT WE BUILT</div>
          <div class="bgrid">"""+built+"""</div>
        </div>
      </div>
      <div>
        <div class="zr"><b>04</b><span class="d2"></span>BUSINESS OUTCOMES</div>
        <div class="outs">
          <div class="stamp">FOUNDER</div>
          <table>"""+outs+"""</table>
        </div>
      </div>
    </div>
    <div class="tl2">
      <div class="zr"><b>05</b><span class="d2"></span>THE ORIGIN LINE</div>
      """+tline+"""
    </div>
    <div class="band2">
      <div>
        <div class="zr"><b>06</b><span class="d2"></span>WHAT I LEARNED</div>
        <div class="para3">Being a founder changes how you think. Every commercial decision affects operations. Every operational decision affects profitability. Every strategic decision affects survival. Leading a company taught me that <b>commercial leadership is ultimately business leadership</b>.</div>
      </div>
      <div class="lessq2">
        <div class="qx">Founders don't manage functions. <b>They align the entire business around one vision.</b></div>
        <div class="who">LESSON &middot; FILE 04 &middot; MEDCOIN</div>
      </div>
    </div>
  </div>
  <div class="ftr">
    <span>THE COMMERCIAL BUILDER</span>
    <span class="mid"><span class="d"></span>CASE STUDY &mdash; MEDCOIN</span>
    <span><b>P.10</b> &mdash; 13</span>
  </div>
</section>
"""
# insert where old p10 was: right before PAGE 11 comment
anchor='\n<!-- ================= PAGE 11 . LEADERSHIP ================= -->'
assert anchor in s
s=s.replace(anchor,page+anchor,1)

# ---------- 4. P09: move feedback label above the dashed line ----------
s=s.replace('<text x="300" y="20" text-anchor="middle" font-size="6.6" letter-spacing="1.6" fill="#5A5B60">CUSTOMER INSIGHT &#8594; BUSINESS DECISIONS</text>',
            '<text x="300" y="3.5" text-anchor="middle" font-size="6.6" letter-spacing="1.6" fill="#5A5B60">CUSTOMER INSIGHT &#8594; BUSINESS DECISIONS</text>')

io.open(p,"w",encoding="utf-8").write(s)
print("polish pass applied")
