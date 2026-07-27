# -*- coding: utf-8 -*-
# SITE BUILDER PART 3: leadership + tech&AI + final + JS
import io, math

CSS = """
/* ============ LEADERSHIP ============ */
#leadership .lead{font-family:'Fraunces',serif;font-style:italic;font-weight:500;font-size:clamp(15px,2vw,19px);line-height:1.6;color:var(--mut);max-width:960px}
#leadership .lead b{color:var(--ink);font-weight:500}
#leadership .cols2{display:grid;grid-template-columns:58fr 42fr;gap:40px;margin-top:34px}
@media (max-width:900px){#leadership .cols2{grid-template-columns:1fr}}
#leadership .pr{display:flex;gap:16px;margin-bottom:20px}
#leadership .pr .n{flex:none;width:34px;height:34px;border:1.5px solid var(--emb);border-radius:9px;display:flex;align-items:center;justify-content:center;
font-family:'JetBrains Mono',monospace;font-weight:700;font-size:12px;color:var(--emb)}
#leadership .pr .nm2{font-weight:700;font-size:15.5px;letter-spacing:-.01em}
#leadership .pr .ds{margin-top:4px;font-size:12.5px;line-height:1.55;color:var(--mut)}
#leadership .tools{display:grid;grid-template-columns:1fr 1fr;gap:10px 18px}
@media (max-width:560px){#leadership .tools{grid-template-columns:1fr}}
#leadership .sigq{margin-top:30px;padding-top:24px;border-top:1px solid var(--grid);text-align:center}
#leadership .sigq .qx{font-family:'Fraunces',serif;font-style:italic;font-weight:500;font-size:clamp(16px,2.2vw,20px)}
#leadership .sigq .qx b{color:var(--emb);font-weight:600}
#leadership .sigq .who{margin-top:6px;font-family:'JetBrains Mono',monospace;font-size:8px;letter-spacing:.26em;color:var(--dim)}

/* ============ TECH & AI ============ */
#tech .lead{font-family:'Fraunces',serif;font-style:italic;font-weight:500;font-size:clamp(14px,1.9vw,17px);line-height:1.6;color:var(--mut)}
#tech .lead b{color:var(--ink);font-weight:500}
#tech .stacks{display:grid;grid-template-columns:repeat(4,1fr);gap:18px;margin-top:40px}
@media (max-width:1000px){#tech .stacks{grid-template-columns:repeat(2,1fr)}}
@media (max-width:560px){#tech .stacks{grid-template-columns:1fr}}
#tech .sc{position:relative;border:1px solid var(--grid);border-radius:0 12px 12px 12px;background:var(--card2);padding:30px 16px 14px;margin-top:24px}
#tech .sc .sl{position:absolute;top:-24px;left:-1px;height:24px;background:var(--emb);border-radius:7px 15px 0 0;
display:flex;align-items:center;padding:0 12px;font-family:'JetBrains Mono',monospace;font-weight:700;font-size:8px;letter-spacing:.18em;color:#0C0D10}
#tech .sc .tools{font-weight:700;font-size:14.5px;letter-spacing:-.01em;margin-bottom:10px}
#tech .sc .it{display:flex;align-items:center;gap:8px;font-size:11.5px;color:var(--mut);margin-bottom:6px}
#tech .sc .it::before{content:"";flex:none;width:8px;height:2px;background:var(--emb)}
#tech .bot{display:grid;grid-template-columns:36fr 64fr;gap:40px;margin-top:40px;padding-top:30px;border-top:1px solid var(--grid)}
@media (max-width:900px){#tech .bot{grid-template-columns:1fr}}
#tech .phil{margin-top:14px;font-family:'JetBrains Mono',monospace;font-size:9.5px;letter-spacing:.14em;color:var(--emb);line-height:1.8}
#tech .loopc{animation:crawl 9s linear infinite}
@keyframes crawl{to{stroke-dashoffset:-44}}
@media (prefers-reduced-motion:reduce){#tech .loopc{animation:none}}
#tech .grid2c{display:grid;grid-template-columns:1fr 1fr;gap:9px 22px}
@media (max-width:640px){#tech .grid2c{grid-template-columns:1fr}}

/* ============ FINAL ============ */
#final{padding-bottom:60px}
#final .pgrid{display:grid;grid-template-columns:1fr 1fr;gap:22px 30px;margin-top:8px}
@media (max-width:760px){#final .pgrid{grid-template-columns:1fr}}
#final .pi{display:flex;gap:13px;align-items:flex-start}
#final .pi .n{flex:none;width:30px;height:30px;border:1.5px solid var(--emb);border-radius:8px;display:flex;align-items:center;justify-content:center;
font-family:'JetBrains Mono',monospace;font-weight:700;font-size:10.5px;color:var(--emb)}
#final .pi .t{font-size:13.8px;line-height:1.5;font-weight:600;padding-top:4px}
#final .pi.vision .t{font-family:'Fraunces',serif;font-style:italic;font-weight:500;font-size:15px;color:var(--emb)}
#final .cols2{display:grid;grid-template-columns:62fr 38fr;gap:44px}
@media (max-width:900px){#final .cols2{grid-template-columns:1fr}}
#final .card{position:relative;border:1px solid var(--grid);border-radius:0 14px 14px 14px;background:var(--card2);margin-top:30px;padding:20px 22px 16px}
#final .card .clip{position:absolute;top:-28px;left:-1px;height:28px;background:var(--ink);border-radius:7px 16px 0 0;
display:flex;align-items:center;gap:11px;padding:0 14px}
#final .card .clip .nm{font-family:'Fraunces',serif;font-weight:500;font-size:14.5px;color:#0C0D10}
#final .card .clip .fl{font-family:'JetBrains Mono',monospace;font-weight:600;font-size:8px;letter-spacing:.16em;color:rgba(12,13,16,.6)}
#final .crow{display:flex;justify-content:space-between;align-items:center;border-top:1px solid var(--grid);padding:12px 0;gap:14px}
#final .crow:first-of-type{border-top:none}
#final .crow .k{font-family:'JetBrains Mono',monospace;font-size:8.5px;letter-spacing:.2em;color:var(--dim)}
#final .crow .v{font-family:'JetBrains Mono',monospace;font-weight:600;font-size:11.5px;letter-spacing:.04em;color:var(--ink);word-break:break-all;text-align:right}
#final .crow .v:hover{color:var(--emb)}
#final .endrow{margin-top:26px;display:flex;align-items:center;justify-content:space-between}
#final .stamp2{transform:rotate(-6deg);border:2px solid var(--emb);border-radius:6px;padding:7px 15px;
font-family:'JetBrains Mono',monospace;font-weight:700;font-size:12px;letter-spacing:.3em;color:var(--emb)}
#final .bc{display:flex;flex-direction:column;align-items:flex-end;gap:4px}
#final .bc .yr{font-family:'JetBrains Mono',monospace;font-size:8px;letter-spacing:.3em;color:var(--dim)}
#final .minidrawer{display:flex;gap:6px;margin-top:26px;border-bottom:1px solid var(--grid2);padding:0 4px}
#final .md{flex:1;height:13px;border-radius:4px 8px 0 0}
#final .closeline{margin-top:22px;font-family:'Fraunces',serif;font-style:italic;font-weight:500;font-size:16px;color:var(--mut);text-align:center}
#final .closeline b{color:var(--emb);font-weight:600}
footer{border-top:1px solid var(--hair);margin-top:80px;padding:26px 24px;display:flex;justify-content:space-between;flex-wrap:wrap;gap:10px;
font-family:'JetBrains Mono',monospace;font-size:9px;letter-spacing:.2em;color:var(--dim)}
footer b{color:var(--mut);font-weight:600}
"""

# AI loop
cx,cy,R=130,106,66
labels=["RESEARCH","ENRICH","PERSONALIZE","AUTOMATE","LEARN","IMPROVE"]
els='<circle class="loopc" cx="%d" cy="%d" r="%d" fill="none" stroke="#26282C" stroke-width="1.4" stroke-dasharray="7 4"/>'%(cx,cy,R)
for i,lab in enumerate(labels):
    a=math.radians(-90+i*60)
    x,y=cx+R*math.cos(a),cy+R*math.sin(a)
    lx,ly=cx+(R+23)*math.cos(a),cy+(R+23)*math.sin(a)
    anchor="middle"
    if lx<cx-32: anchor="end"
    if lx>cx+32: anchor="start"
    els+='<circle class="ndot" style="--i:%d" cx="%.1f" cy="%.1f" r="6.5" fill="#16181C" stroke="#F4603E" stroke-width="1.8"/>'%(i,x,y)
    els+='<text x="%.1f" y="%.1f" text-anchor="%s" font-size="7.4" letter-spacing="1.2" fill="#8E8E93">%s</text>'%(lx,ly+2.6,anchor,lab)
    am=math.radians(-90+i*60+30)
    mx,my=cx+R*math.cos(am),cy+R*math.sin(am)
    rot=math.degrees(am)+90
    els+='<path d="M%.1f %.1f l-4.5 -6.5 h9 z" fill="#F4603E" transform="rotate(%.1f %.1f %.1f)"/>'%(mx,my,rot,mx,my)
els+=('<text x="%d" y="%d" text-anchor="middle" font-size="10" font-weight="700" letter-spacing="2" fill="#F2F1ED">AI</text>'
      '<text x="%d" y="%d" text-anchor="middle" font-size="10" font-weight="700" letter-spacing="2" fill="#F2F1ED">ENGINE</text>')%(cx,cy-3,cx,cy+11)
loop='<svg viewBox="0 0 260 212" style="width:100%%;max-width:280px;height:auto;margin:0 auto;overflow:visible">%s</svg>'%els

def lg(n,t): return '<div class="lg"><span class="n">LOG.%02d</span><span class="c">&#10003;</span>%s</div>'%(n,t)

def pr(n,name,desc):
    return ('<div class="pr rv" style="--i:%d"><div class="n">%02d</div><div><div class="nm2">%s</div>'
            '<div class="ds">%s</div></div></div>')%(n,n,name,desc)
princ=(pr(1,"Build Trust Before Performance","People perform better when expectations are clear and trust is earned.")+
pr(2,"Coach Before You Judge","Every performance issue deserves investigation first &mdash; understand the process, review the data, listen first, coach second, decide last.")+
pr(3,"Create Ownership","People shouldn't execute tasks. They should own outcomes.")+
pr(4,"Decisions Based on Facts","KPIs don't replace leadership &mdash; they improve it. Every coaching session begins with evidence, not assumptions.")+
pr(5,"Great Managers Solve Today's Problems. Great Leaders Build Tomorrow's System.","My objective was never to close one more deal &mdash; it was to build an organization that produces consistent results without depending on one individual."))

tools="".join(lg(i+1,t) for i,t in enumerate(["Hiring &amp; Recruitment","Onboarding Programs","Weekly Team Meetings","Monthly 1:1 Reviews","Quarterly Performance Reviews","KPI Design","Coaching","Sales Methodology","Performance Improvement Plans","Cross-functional Leadership"]))

def sc(label,toolsline,items,i):
    its="".join('<div class="it">%s</div>'%t for t in items)
    return ('<div class="sc rvs" style="--i:%d"><div class="sl">%s</div><div class="tools">%s</div>%s</div>')%(i,label,toolsline,its)
stacks=(sc("CRM","HubSpot",["Commercial Infrastructure","Pipeline Management","Forecasting","Reporting"],0)+
sc("AUTOMATION","Zapier &middot; Webhooks",["Google Workspace","API Integrations"],1)+
sc("AI","GPT &middot; Claude &middot; Gemini",["Custom AI Workflows","Knowledge Base","Lead Intelligence","Personalized Outreach","Continuous Learning"],2)+
sc("COMMERCIAL DATA","Clay &middot; Apollo &middot; Hunter",["Market Research","Lead Enrichment","Competitive Intelligence"],3))

case="".join(lg(i+1,t) for i,t in enumerate(["Researching prospects","Enriching leads","Personalizing outreach","Automating commercial workflows","Learning from previous interactions","Improving commercial recommendations over time"]))

principles=["Understand before you build.","Vision creates direction. Execution creates momentum.",
"Commercial growth is a business problem &mdash; not a sales problem.","Build systems before you scale people.",
"Measure decisions &mdash; not assumptions.","Technology should improve thinking &mdash; not replace it.",
"Great leaders create ownership.","Commercial success belongs to every department.",
"Continuous learning is a competitive advantage.","If you connect to the vision, you'll always know where you're going."]
pis=""
for i,t in enumerate(principles):
    cls=' vision' if i==9 else ''
    pis+='<div class="pi%s rv" style="--i:%d"><div class="n">%02d</div><div class="t">%s</div></div>'%(cls,i%5,i+1,t)

barcode='<svg viewBox="0 0 62 26" style="width:62px;height:26px">'
x=0
for i,w in enumerate([2,1,3,1,2,1,1,3,2,1,2,3,1,2,1,3,1,1,2]):
    barcode+='<rect x="%d" y="0" width="%d" height="26" fill="%s"/>'%(x,w,"#8E8E93" if i%3 else "#F2F1ED")
    x+=w+1
barcode+='</svg>'

HTML = """<style>"""+CSS+"""</style>
<section class="sec" id="leadership" style="--fc:var(--emb)">
  <div class="wrap">
    <div class="shead rv" style="--i:0">
      <div class="rub"><span class="d"></span>LEADERSHIP</div>
      <div class="tok">MANAGEMENT FILE</div>
    </div>
    <div class="sttl rv" style="--i:1">Building People. Building Systems.<br>Building Accountability.</div>
    <div class="folder rv" style="--i:2;margin-top:52px">
      <div class="flip"><span class="nm">Leadership</span><span class="fl">MANAGEMENT FILE</span></div>
      <div class="lead">I believe leadership is not measured by how many people report to you &mdash; it is measured by <b>how many people become better because of you</b>. My role is to create clarity, ownership and an environment where people consistently perform at their best.</div>
      <div class="cols2">
        <div>
          <div class="zr"><b>A</b><span class="d2"></span>LEADERSHIP PRINCIPLES</div>
          """+princ+"""
        </div>
        <div>
          <div class="zr"><b>B</b><span class="d2"></span>LEADERSHIP TOOLKIT</div>
          <div class="tools">"""+tools+"""</div>
          <div class="sigq rv">
            <div class="qx">Leadership is not about creating better employees. <b>It's about creating people who no longer depend on you.</b></div>
            <div class="who">SIGNATURE PRINCIPLE &middot; MANAGEMENT FILE</div>
          </div>
        </div>
      </div>
    </div>
  </div>
</section>

<section class="sec" id="tech" style="--fc:var(--emb)">
  <div class="wrap">
    <div class="shead rv" style="--i:0">
      <div class="rub"><span class="d"></span>COMMERCIAL TECHNOLOGY &amp; AI</div>
      <div class="tok">SYSTEM FILE &middot; AI</div>
    </div>
    <div class="sttl rv" style="--i:1">How I use technology to improve<br>commercial decisions.</div>
    <div class="lead rv" style="--i:2;margin-top:22px">Technology should never replace commercial thinking &mdash; <b>it should amplify it</b>. Throughout my career, I've used technology to remove repetitive work, improve decision-making and increase execution capacity.</div>
    <div class="stacks">"""+stacks+"""</div>
    <div class="bot">
      <div class="rv" style="text-align:center">
        """+loop+"""
        <div class="looplbl">CONTINUOUS COMMERCIAL LOOP</div>
      </div>
      <div class="rv" style="--i:1">
        <div class="zr"><b>AI</b><span class="d2"></span>AI CASE &mdash; INTERNAL COMMERCIAL INTELLIGENCE PLATFORM</div>
        <div class="grid2c">"""+case+"""</div>
        <div class="phil">MY PHILOSOPHY: TECHNOLOGY SHOULD AUTOMATE EXECUTION. PEOPLE SHOULD MAKE DECISIONS.</div>
        <div class="lessq" style="margin-top:16px">
          <div class="qx">AI doesn't replace commercial leaders. <b>It lets them think faster, learn faster and execute at scale.</b></div>
        </div>
      </div>
    </div>
  </div>
</section>

<section class="sec" id="final" style="--fc:var(--emb)">
  <div class="wrap">
    <div class="shead rv" style="--i:0">
      <div class="rub"><span class="d"></span>FINAL THOUGHTS</div>
      <div class="tok">END OF FILE</div>
    </div>
    <div class="sttl rv" style="--i:1">The Builder's Principles</div>
    <div class="folder rv" style="--i:2;margin-top:52px">
      <div class="flip"><span class="nm">The Builder</span><span class="fl">FINAL THOUGHTS</span></div>
      <div class="cols2">
        <div>
          <div class="zr"><b>A</b><span class="d2"></span>THE BUILDER'S PRINCIPLES</div>
          <div class="pgrid">"""+pis+"""</div>
        </div>
        <div>
          <div class="zr"><b>B</b><span class="d2"></span>CONTACT</div>
          <div class="card rv" style="--i:1">
            <div class="clip"><span class="nm">Oran Carmon</span><span class="fl">COMMERCIAL BUILDER</span></div>
            <a class="crow" href="https://www.linkedin.com/in/oran-carmon" target="_blank" rel="noopener"><span class="k">LINKEDIN</span><span class="v">linkedin.com/in/oran-carmon</span></a>
            <a class="crow" href="mailto:orancarmon@gmail.com"><span class="k">EMAIL</span><span class="v">orancarmon@gmail.com</span></a>
            <a class="crow" href="tel:+972546685331"><span class="k">PHONE</span><span class="v">+972-54-668-5331</span></a>
          </div>
          <div class="endrow rv" style="--i:2">
            <div class="stamp2">CASE CLOSED</div>
            <div class="bc">"""+barcode+"""<span class="yr">ARCHIVE 2026</span></div>
          </div>
          <div class="minidrawer rv" style="--i:3">
            <div class="md" style="background:var(--emb)"></div>
            <div class="md" style="background:var(--brass)"></div>
            <div class="md" style="background:var(--ice)"></div>
            <div class="md" style="background:var(--ink)"></div>
          </div>
          <div class="closeline rv" style="--i:4">Turning vision into <b>commercial growth</b>.</div>
        </div>
      </div>
    </div>
  </div>
</section>

<footer>
  <span><b>ORAN CARMON</b> &mdash; THE COMMERCIAL BUILDER</span>
  <span>EXECUTIVE CASEBOOK &middot; DOSSIER ARCHIVE &middot; 2026</span>
</footer>

<script>
(function(){
  var q=new URLSearchParams(location.search);
  if(q.get('static')==='1'){document.body.classList.add('static');
    document.querySelectorAll('.sec').forEach(function(s){s.classList.add('on')});}
  var reduced=window.matchMedia('(prefers-reduced-motion: reduce)').matches;

  // progress bar
  var pbar=document.getElementById('pbar');
  function prog(){var h=document.documentElement;
    pbar.style.width=(h.scrollTop/(h.scrollHeight-h.clientHeight)*100)+'%';}
  addEventListener('scroll',prog,{passive:true});prog();

  // counters
  function runCnt(el){
    if(el.dataset.done)return;el.dataset.done=1;
    var n=parseFloat(el.dataset.n||'0'),suf=el.dataset.suf||'',t0=null,dur=1400;
    function step(ts){if(!t0)t0=ts;var p=Math.min(1,(ts-t0)/dur);
      p=1-Math.pow(1-p,3);
      el.textContent=Math.round(n*p)+suf;
      if(p<1)requestAnimationFrame(step);}
    if(reduced||document.body.classList.contains('static')){el.textContent=n+suf;return;}
    requestAnimationFrame(step);
  }

  // reveal observer
  var io=new IntersectionObserver(function(es){
    es.forEach(function(e){
      if(e.isIntersecting){
        e.target.classList.add('on');
        e.target.querySelectorAll('.cnt').forEach(runCnt);
        io.unobserve(e.target);
      }
    });
  },{threshold:.16,rootMargin:'0px 0px -8% 0px'});
  document.querySelectorAll('.sec').forEach(function(s){io.observe(s)});
  // hero reveals immediately
  document.getElementById('hero').classList.add('on');
  document.querySelectorAll('#hero .cnt').forEach(runCnt);

  // rail active state
  var links=[].slice.call(document.querySelectorAll('#rail a'));
  var secs=links.map(function(a){return document.querySelector(a.getAttribute('href'))});
  var io2=new IntersectionObserver(function(es){
    es.forEach(function(e){
      if(e.isIntersecting){
        var i=secs.indexOf(e.target);
        links.forEach(function(a,j){a.classList.toggle('act',j===i)});
      }
    });
  },{threshold:.4});
  secs.forEach(function(s){if(s)io2.observe(s)});
})();
</script>
"""

s = io.open("site.html", encoding="utf-8").read()
s = s.replace("<!--MORE-->", HTML, 1)
io.open("site.html","w",encoding="utf-8").write(s)
print("site part 3 appended. total:", len(s), "bytes")
