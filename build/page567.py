# -*- coding: utf-8 -*-
import io
EM="—"
p="index.html"; s=io.open(p,encoding="utf-8").read()
BR='  <span class="brk tl"></span><span class="brk tr"></span><span class="brk bl"></span><span class="brk br"></span>\n'

def li(items, cls="x2-list", tag="li"):
    return '\n'.join('          <div class="%s">%s</div>'%(tag,x) for x in items)
def chk(items):
    return '\n'.join('          <div class="ci"><span class="k">&#10003;</span> %s</div>'%x for x in items)

# ---------- PAGE 5: XTIX EVIDENCE ----------
perf=[("Pipeline Managed",'<span class="m">€3M+</span> ARR'),
("Qualified Meetings",'<span class="m">~6</span> per week'),
("New Opportunities",'<span class="m">~20</span> per week'),
("Outbound Reply Rate",'<span class="m">~20%</span>'),
("Outbound Conversion",'<span class="m">7&#8211;8%</span>'),
("Inbound Conversion",'<span class="m">50%+</span>')]
perf_html='\n'.join('          <div class="er"><div class="ea">%s</div><div class="eo">%s</div></div>'%(a,o) for a,o in perf)
ops=["Built the company's commercial reporting structure","Implemented forecasting methodology","Designed KPI framework","Established pipeline management","Standardized outbound methodology","Supported international commercial expansion"]
tech=["Researched prospects automatically","Imported &amp; enriched leads from commercial databases","Generated personalized outreach per prospect's business","Automated commercial sequences","Continuously improved through feedback &amp; knowledge"]
refl5=["Differentiate the product earlier against competitors","Accelerate enterprise positioning","Invest in strategic partnerships sooner","Expand the AI platform even earlier","Build the Israeli operation in parallel with global activity"]
refl_html='\n'.join('          <div class="ri2">%s</div>'%x for x in refl5)

page5=(
'<!-- ============ 05 - XTIX EVIDENCE ============ -->\n'
'<section class="page">\n'+BR+
'  <div class="hd"><div class="l">§05 <span>· Case Study 01 &#183; Evidence</span></div><div class="r">Oran Carmon '+EM+' Building Revenue Engines</div></div>\n'
'  <div class="wrap col">\n'
'    <div class="eyebrow">Case Study 01 &#183; XTIX</div>\n'
'    <div class="x2-title">Evidence <span class="tsub">'+EM+' From Infrastructure to Execution</span></div>\n'
'    <div class="x2-cols">\n'
'      <div class="x2-col">\n'
'        <div class="cs-lbl">Performance</div>\n'
'        <div class="evt">\n'+perf_html+'\n        </div>\n'
'      </div>\n'
'      <div class="x2-col">\n'
'        <div class="cs-lbl">Operations</div>\n'
'        <div class="chk">\n'+chk(ops)+'\n        </div>\n'
'      </div>\n'
'      <div class="x2-col">\n'
'        <div class="cs-lbl">Technology</div>\n'
'        <div class="x2-p">Designed &amp; implemented an internal <b>AI-powered commercial intelligence platform</b> that:</div>\n'
'        <div class="x2-list">\n'+li(tech)+'\n        </div>\n'
'        <div class="tech-purpose"><b>Purpose:</b> Improve commercial decision-making while increasing execution capacity.</div>\n'
'      </div>\n'
'    </div>\n'
'    <div class="x2-bottom">\n'
'      <div class="lookback">\n'
'        <div class="lbl2">Reflection '+EM+' If I were rebuilding XTIX today</div>\n'
'        <div class="refl-grid">\n'+refl_html+'\n        </div>\n'
'      </div>\n'
'      <div class="x2-quote">Commercial growth doesn\'t begin when the first campaign is launched. <span class="g">It begins when the commercial system becomes repeatable.</span></div>\n'
'    </div>\n'
'  </div>\n'
'  <div class="ft"><div class="l">Case Study '+EM+' XTIX</div><div class="r"><b>P.05</b> '+EM+' 7</div></div>\n'
'</section>\n\n'
)

# ---------- PAGE 6: OASIS PART 1 ----------
resp=["Recruiting &amp; building the sales team","Defining commercial strategy","Pricing model development","KPI design","Sales methodology","Forecasting","Commercial reviews","Cross-functional leadership","Profitability management"]
built=["Recruited &amp; onboarded the entire sales team","Built the pricing model from scratch","Designed the commercial process","Implemented KPI framework","Created sales playbooks &amp; onboarding","Established weekly business reviews","Built forecasting methodology","Created cross-functional collaboration"]
lead=["Weekly coaching sessions","Monthly 1:1 performance reviews","Quarterly business reviews","Live deal reviews","Commercial coaching","Cross-functional collaboration","Clear ownership &amp; accountability"]
page6=(
'<!-- ============ 06 - OASIS PART 1 ============ -->\n'
'<section class="page">\n'+BR+
'  <div class="hd"><div class="l">§06 <span>· Case Study 02</span></div><div class="r">Oran Carmon '+EM+' Building Revenue Engines</div></div>\n'
'  <div class="wrap col">\n'
'    <div class="cs2-top"><div>\n'
'      <div class="eyebrow">Case Study 02</div>\n'
'      <div class="cs2-title">Building Leaders, Not Just Sales Teams</div>\n'
'      <div class="cs2-meta"><b>Oasis</b> &#183; CEO &#183; Construction &amp; Smart Building Solutions</div>\n'
'    </div></div>\n'
'    <div class="zones">\n'
'      <div class="zone">\n'
'        <div class="zhead"><span class="zn">01</span><span class="zt">The Situation</span></div>\n'
'        <div class="zp">As CEO, my responsibility extended far beyond sales. The objective wasn\'t simply to increase revenue &#8212; it was to build a <b>profitable, scalable commercial organization</b> capable of supporting the company\'s long-term vision.</div>\n'
'      </div>\n'
'      <div class="zone">\n'
'        <div class="zhead"><span class="zn">02</span><span class="zt">My Responsibilities</span></div>\n'
'        <div class="zbul">\n'+li(resp, cls="zb", tag="zb")+'\n        </div>\n'
'      </div>\n'
'      <div class="zone">\n'
'        <div class="zhead"><span class="zn">03</span><span class="zt">Commercial System Built</span></div>\n'
'        <div class="zchecks">\n'+'\n'.join('          <div class="zck"><span class="k">&#10003;</span> %s</div>'%x for x in built)+'\n        </div>\n'
'      </div>\n'
'      <div class="zone">\n'
'        <div class="zhead"><span class="zn">04</span><span class="zt">Leadership Model</span></div>\n'
'        <div class="zbul">\n'+li(lead, cls="zb", tag="zb")+'\n        </div>\n'
'      </div>\n'
'    </div>\n'
'    <div class="cs2-sig">\n'
'      <div class="sl">Signature Insight</div>\n'
'      <div class="stx">High-performing sales teams aren\'t built by pressure. <span class="g">They\'re built by clarity.</span></div>\n'
'    </div>\n'
'  </div>\n'
'  <div class="ft"><div class="l">Case Study '+EM+' Oasis</div><div class="r"><b>P.06</b> '+EM+' 7</div></div>\n'
'</section>\n\n'
)

# ---------- PAGE 7: OASIS EVIDENCE ----------
cl=["Recruited an entire sales team","Led a team of 5&#8211;6 sales professionals","Conducted weekly coaching sessions","Established KPI-driven management","Built onboarding documentation","Standardized commercial processes"]
bp=['Largest deal closed: <span class="m">₪2M</span>',"Built pricing strategy from zero","Introduced profitability-based pricing","Defined company-wide commercial KPIs","Improved cross-department collaboration","Created structured commercial reporting"]
xf=["Operations","Production","Customer Success","Finance","Marketing","Technical Teams"]
page7=(
'<!-- ============ 07 - OASIS EVIDENCE ============ -->\n'
'<section class="page">\n'+BR+
'  <div class="hd"><div class="l">§07 <span>· Case Study 02 &#183; Evidence</span></div><div class="r">Oran Carmon '+EM+' Building Revenue Engines</div></div>\n'
'  <div class="wrap col">\n'
'    <div class="eyebrow">Case Study 02 &#183; Oasis</div>\n'
'    <div class="x2-title">Evidence <span class="tsub">'+EM+' Commercial Results</span></div>\n'
'    <div class="x2-cols">\n'
'      <div class="x2-col">\n'
'        <div class="cs-lbl">Commercial Leadership</div>\n'
'        <div class="x2-list">\n'+li(cl)+'\n        </div>\n'
'      </div>\n'
'      <div class="x2-col">\n'
'        <div class="cs-lbl">Business Performance</div>\n'
'        <div class="x2-list">\n'+li(bp)+'\n        </div>\n'
'      </div>\n'
'      <div class="x2-col">\n'
'        <div class="cs-lbl">Cross-Functional Leadership</div>\n'
'        <div class="x2-p">Worked closely with:</div>\n'
'        <div class="chk">\n'+chk(xf)+'\n        </div>\n'
'      </div>\n'
'    </div>\n'
'    <div class="x2-bottom">\n'
'      <div class="lookback">\n'
'        <div class="lbl2">Reflection '+EM+' Looking Back</div>\n'
'        <p>The biggest lesson I learned as CEO wasn\'t about selling &#8212; it was about <b>leadership</b>. The more I tried to manage every function myself, the less scalable the organization became. Real leadership begins when leaders <b>build systems that let others succeed</b> without depending on them.</p>\n'
'      </div>\n'
'      <div class="x2-quote">Organizations don\'t scale because leaders work harder. <span class="g">They scale because leaders create clarity, ownership and trust.</span></div>\n'
'    </div>\n'
'  </div>\n'
'  <div class="ft"><div class="l">Case Study '+EM+' Oasis</div><div class="r"><b>P.07</b> '+EM+' 7</div></div>\n'
'</section>\n\n'
)

# splice: keep up to page5 comment, replace 5/6/7, drop 8-11
i5=s.index("<!-- ============ 05 ")
tail=s[s.index("</body>"):]
s=s[:i5]+page5+page6+page7+tail

# renumber totals to 7
s=s.replace(EM+" 11", EM+" 7").replace("&mdash; 11","&mdash; 7")
# fix stale "/ 03" case labels on page 4 header
s=s.replace("§04 <span>· Case Study 01 / 03</span>","§04 <span>· Case Study 01</span>")

# add CSS
css=(
"\n/* evidence-page extras */\n"
".x2-title .tsub{color:var(--muted2);font-weight:600;font-size:16px;letter-spacing:-.01em}\n"
".chk{display:flex;flex-direction:column;gap:5px;margin-top:9px}\n"
".chk .ci{display:flex;align-items:flex-start;gap:8px;font-size:10.5px;color:var(--ink);font-weight:400;line-height:1.35}\n"
".chk .ci .k{color:var(--acc);font-size:10px;margin-top:1px;flex:none}\n"
".tech-purpose{margin-top:9px;font-size:10px;color:var(--muted);font-weight:300;line-height:1.4}\n"
".tech-purpose b{color:var(--acc);font-weight:600}\n"
".refl-grid{display:grid;grid-template-columns:1fr 1fr;gap:4px 16px;margin-top:8px}\n"
".refl-grid .ri2{font-size:9.5px;color:var(--muted);font-weight:300;position:relative;padding-left:11px;line-height:1.35}\n"
".refl-grid .ri2::before{content:\"\";position:absolute;left:0;top:5px;width:5px;height:1px;background:var(--acc)}\n"
".lookback p{font-size:10px;color:var(--muted);line-height:1.5;font-weight:300}\n"
".lookback p b{color:var(--ink);font-weight:500}\n"
)
s=s.replace("</style>", css+"</style>",1)

io.open(p,"w",encoding="utf-8").write(s)
print("pages 5,6,7 built; 8-11 removed;", s.count('<section class="page"')+1, "sections")
