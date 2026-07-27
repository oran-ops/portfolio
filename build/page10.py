# -*- coding: utf-8 -*-
import io
p="casebook.html"; s=io.open(p,encoding="utf-8").read()

css="""
/* ============ PAGE 10 - MEDCOIN ORIGIN (PAPER) ============ */
.p10{background:#F2F1ED;color:#0C0D10}
.p10 .brk{border-color:rgba(12,13,16,.4)}
.p10 .hd{position:absolute;top:48px;left:72px;right:72px;display:flex;justify-content:space-between;align-items:center;z-index:5}
.p10 .rub{display:flex;align-items:center;gap:11px;font-family:'JetBrains Mono',monospace;font-weight:700;font-size:10.5px;letter-spacing:.26em;color:#0C0D10}
.p10 .rub .d{width:7px;height:7px;background:#F4603E;transform:rotate(45deg)}
.p10 .tok{display:inline-flex;align-items:center;gap:8px;font-family:'JetBrains Mono',monospace;font-weight:600;font-size:9.5px;letter-spacing:.16em;
border:1px solid rgba(12,13,16,.22);border-radius:7px;padding:6px 12px;color:#0C0D10}
.p10 .ttl2{position:absolute;top:88px;left:72px;font-weight:800;font-size:30px;letter-spacing:-.025em;color:#0C0D10}
.p10 .meta2{position:absolute;top:132px;left:72px;font-family:'JetBrains Mono',monospace;font-size:9.5px;letter-spacing:.22em;color:rgba(12,13,16,.55)}
.p10 .folder2{position:absolute;top:172px;left:72px;right:72px;height:474px;background:rgba(12,13,16,.04);border:1px solid rgba(12,13,16,.16);
border-radius:0 16px 16px 16px;padding:22px 28px 16px}
.p10 .flip2{position:absolute;top:-30px;left:-1px;height:30px;background:#0C0D10;border-radius:8px 18px 0 0;
display:flex;align-items:center;gap:12px;padding:0 16px}
.p10 .flip2 .nm{font-family:'Fraunces',serif;font-weight:500;font-size:15px;color:#F2F1ED}
.p10 .flip2 .fl{font-family:'JetBrains Mono',monospace;font-weight:600;font-size:8.5px;letter-spacing:.16em;color:rgba(242,241,237,.6)}
.p10 .inner{display:grid;grid-template-columns:53fr 47fr;column-gap:30px}
.p10 .zr2{display:flex;align-items:center;gap:9px;font-family:'JetBrains Mono',monospace;font-weight:700;font-size:10px;letter-spacing:.22em;color:#0C0D10;margin-bottom:8px}
.p10 .zr2 b{color:#F4603E;font-weight:700}
.p10 .zr2 .d2{width:5px;height:5px;background:#F4603E;transform:rotate(45deg)}
.p10 .para2{font-size:11.6px;line-height:1.52;color:rgba(12,13,16,.68)}
.p10 .para2 b{color:#0C0D10;font-weight:600}
.p10 .z{margin-bottom:14px}
.p10 .bgrid{display:grid;grid-template-columns:1fr 1fr;gap:6px 14px}
.p10 .lg2{display:flex;align-items:center;gap:8px;font-size:10.9px;font-weight:600;color:#0C0D10}
.p10 .lg2 .c{flex:none;width:11px;height:11px;background:#F4603E;color:#F2F1ED;font-size:9px;font-weight:800;line-height:11px;text-align:center}
.p10 .outs{position:relative;border:1px solid rgba(12,13,16,.16);border-radius:10px;background:#F2F1ED;padding:4px 16px 6px}
.p10 .outs table{width:100%;border-collapse:collapse}
.p10 .outs td{border-top:1px solid rgba(12,13,16,.12);padding:6.5px 0;vertical-align:middle}
.p10 .outs tr:first-child td{border-top:none}
.p10 .outs .k{font-family:'JetBrains Mono',monospace;font-size:8px;letter-spacing:.16em;color:rgba(12,13,16,.5)}
.p10 .outs .v{text-align:right;font-weight:700;font-size:12px;color:#0C0D10}
.p10 .outs .v.em{color:#F4603E}
.p10 .stamp{position:absolute;top:-14px;right:14px;transform:rotate(-7deg);border:2px solid #F4603E;border-radius:6px;
padding:5px 12px;font-family:'JetBrains Mono',monospace;font-weight:700;font-size:11px;letter-spacing:.3em;color:#F4603E;background:#F2F1ED}
.p10 .tl{margin-top:12px;padding-top:12px;border-top:1px solid rgba(12,13,16,.14)}
.p10 .band2{margin-top:10px;padding-top:12px;border-top:1px solid rgba(12,13,16,.14);display:grid;grid-template-columns:56fr 44fr;column-gap:30px}
.p10 .para3{font-size:10.9px;line-height:1.5;color:rgba(12,13,16,.68)}
.p10 .para3 b{color:#0C0D10;font-weight:600}
.p10 .lesson2{border-left:2px solid #F4603E;padding:2px 0 2px 16px}
.p10 .lesson2 .qx{font-family:'Fraunces',serif;font-style:italic;font-weight:500;font-size:14px;line-height:1.42;color:#0C0D10}
.p10 .lesson2 .qx b{color:#F4603E;font-weight:600}
.p10 .lesson2 .who{margin-top:5px;font-family:'JetBrains Mono',monospace;font-size:7.5px;letter-spacing:.24em;color:rgba(12,13,16,.5)}
.p10 .ftr2{position:absolute;left:72px;right:72px;bottom:44px;z-index:9;display:flex;align-items:center;justify-content:space-between;
font-family:'JetBrains Mono',monospace;font-size:9.5px;letter-spacing:.18em;color:rgba(12,13,16,.5)}
.p10 .ftr2 .mid2{display:flex;align-items:center;gap:14px;position:absolute;left:50%;transform:translateX(-50%)}
.p10 .ftr2 .d{width:7px;height:7px;background:#F4603E;transform:rotate(45deg)}
.p10 .ftr2 b{color:rgba(12,13,16,.75);font-weight:600}
"""
s=s.replace("</style>",css+"</style>",1)

built="".join('<div class="lg2"><span class="c">&#10003;</span>%s</div>'%t for t in [
"Founded the company from scratch","Defined the business model","Built the commercial strategy",
"Established strategic partnerships","Raised external investment","Deployed cryptocurrency ATMs across Europe",
"Built operational &amp; regulatory processes","Managed financial-service providers &amp; international vendors",
"Designed the customer journey &amp; user experience"])

outs="".join('<tr><td class="k">%s</td><td class="v%s">%s</td></tr>'%(k," em" if em else "",v) for k,v,em in [
("MARKETS","Europe",False),("BUSINESS MODEL","Crypto ATM network",False),
("INVESTMENT","External investment raised",False),("REVENUE","Hundreds of thousands of &euro;",True),
("INFRASTRUCTURE","Operational ATM network deployed",False),("TEAM","Founder-led operation",False)])

# founder timeline: 5 milestones, dark strokes on paper, ember terminal
ms=[("FOUNDED",40),("BUSINESS MODEL",255),("PARTNERSHIPS",470),("INVESTMENT RAISED",685),("ATMs ACROSS EUROPE",900)]
nodes=""
for i,(t,x) in enumerate(ms):
    last=(i==4)
    nodes+=('<circle cx="%d" cy="26" r="%s" fill="%s" stroke="#0C0D10" stroke-width="1.6"/>'
            '<text x="%d" y="52" text-anchor="middle" font-size="7.2" letter-spacing="1.3" fill="rgba(12,13,16,.6)">%s</text>'
            )%(x,"6" if last else "4.5","#F4603E" if last else "#F2F1ED",x,t)
tline=('<svg viewBox="0 0 1040 58" style="width:100%;height:auto">'
       '<line x1="26" y1="26" x2="912" y2="26" stroke="#0C0D10" stroke-width="1.4"/>'
       '<line x1="912" y1="26" x2="1014" y2="26" stroke="#F4603E" stroke-width="2" stroke-dasharray="4 4"/>'
       '<path d="M1020 26 l-9 -5 v10 z" fill="#F4603E"/>'
       +nodes+
       '<text x="968" y="14" text-anchor="middle" font-size="7.4" font-weight="700" letter-spacing="1.5" fill="#F4603E">REVENUE</text>'
       '</svg>')

page="""
<!-- ================= PAGE 10 . MEDCOIN ORIGIN ================= -->
<section class="page p10">
  <span class="brk tl"></span><span class="brk tr"></span><span class="brk bl"></span><span class="brk br"></span>
  <div class="hd">
    <div class="rub"><span class="d"></span>FOUNDER CASE STUDY</div>
    <div class="tok">FILE 04 &middot; ORIGIN</div>
  </div>
  <div class="ttl2">Building a Business From Vision</div>
  <div class="meta2">MEDCOIN TEKNOLOJI &middot; CRYPTO FINTECH &middot; FOUNDER</div>
  <div class="folder2">
    <div class="flip2"><span class="nm">Medcoin</span><span class="fl">FILE 04</span></div>
    <div class="inner">
      <div>
        <div class="z">
          <div class="zr2"><b>01</b><span class="d2"></span>THE VISION</div>
          <div class="para2">Create a <b>compliant, scalable cryptocurrency ATM business</b> serving the European market through secure, accessible digital financial services.</div>
        </div>
        <div class="z">
          <div class="zr2"><b>02</b><span class="d2"></span>THE CHALLENGE</div>
          <div class="para2">Building a company from zero meant making <b>every strategic decision</b> &mdash; from business model and partnerships to compliance, operations and commercialization.</div>
        </div>
        <div class="z" style="margin-bottom:0">
          <div class="zr2"><b>03</b><span class="d2"></span>WHAT WE BUILT</div>
          <div class="bgrid">"""+built+"""</div>
        </div>
      </div>
      <div>
        <div class="zr2"><b>04</b><span class="d2"></span>BUSINESS OUTCOMES</div>
        <div class="outs">
          <div class="stamp">FOUNDER</div>
          <table>"""+outs+"""</table>
        </div>
      </div>
    </div>
    <div class="tl">
      <div class="zr2"><b>05</b><span class="d2"></span>THE ORIGIN LINE</div>
      """+tline+"""
    </div>
    <div class="band2">
      <div>
        <div class="zr2"><b>06</b><span class="d2"></span>WHAT I LEARNED</div>
        <div class="para3">Being a founder changes how you think. Every commercial decision affects operations. Every operational decision affects profitability. Every strategic decision affects survival. Leading a company taught me that <b>commercial leadership is ultimately business leadership</b>.</div>
      </div>
      <div class="lesson2">
        <div class="qx">Founders don't manage functions. <b>They align the entire business around one vision.</b></div>
        <div class="who">LESSON &middot; FILE 04 &middot; MEDCOIN</div>
      </div>
    </div>
  </div>
  <div class="ftr2">
    <span>THE COMMERCIAL BUILDER</span>
    <span class="mid2"><span class="d"></span>CASE STUDY &mdash; MEDCOIN</span>
    <span><b>P.10</b> &mdash; 13</span>
  </div>
</section>
"""
s=s.replace("</body></html>",page+"\n</body></html>")
io.open(p,"w",encoding="utf-8").write(s)
print("page 10 added")
