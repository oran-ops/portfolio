# -*- coding: utf-8 -*-
# INVESTIGATOR ARC — role, 0/4 meter, signature moments, teasers, interlude,
# evidence tag, UV notes, red strings, burst, whoosh, magnetic, idle, ceremony.
import io, re
p="site.html"; s=io.open(p,encoding="utf-8").read()

# ============================================================ A. HTML INJECTIONS
# --- A1. interlude section between oasis and eventer ---
INTERLUDE=('<section class="sec" id="interlude">\n'
'  <div class="wrap">\n'
'    <div class="ix-log rv" style="--i:0">&gt; CROSS-REFERENCING FILES 01 + 02 &hellip;</div>\n'
'    <div class="ix-board rv" style="--i:1">\n'
'      <canvas class="ix-canvas" aria-hidden="true"></canvas>\n'
'      <div class="ix-tab ix-a"><b>XTIX</b><span>FILE 01 &middot; REVIEWED &#10003;</span></div>\n'
'      <div class="ix-tab ix-b"><b>Oasis</b><span>FILE 02 &middot; REVIEWED &#10003;</span></div>\n'
'      <div class="ix-chip c1">&ldquo;commercial operating system&rdquo;</div>\n'
'      <div class="ix-chip c2">&ldquo;built by clarity&rdquo;</div>\n'
'      <div class="ix-verdict">PATTERN ON FILE &middot; CONTINUE &darr;</div>\n'
'    </div>\n'
'  </div>\n'
'</section>\n')
anch='<section class="sec case" id="eventer"'
assert anch in s
s=s.replace(anch,INTERLUDE+anch,1)

# --- A2. UV hidden-note layers inside folders ---
def uv(notes):
    inner="".join('<span class="uvn" style="%s">%s</span>'%(st,tx) for st,tx in notes)
    return '<div class="uvlayer" aria-hidden="true">%s</div>'%inner
UVS=[
 ('#hero',   'class="hw"', [("top:20%;left:6%;transform:rotate(-2.4deg)","ARCHIVE COPY — DO NOT REMOVE"),
                            ("bottom:26%;right:8%;transform:rotate(1.8deg)","reviewed: 2026 ✓")]),
 ('#xtix',   None, [("top:14%;right:6%;transform:rotate(-2deg)","cross-ref: FILE 02 →"),
                    ("bottom:18%;left:8%;transform:rotate(1.6deg)","evidence B verified ✓")]),
 ('#oasis',  None, [("top:12%;right:7%;transform:rotate(2deg)","compare: FILE 01 · systems"),
                    ("bottom:16%;left:6%;transform:rotate(-1.8deg)","margin note: clarity ✓")]),
 ('#eventer',None, [("top:16%;left:6%;transform:rotate(-2.2deg)","shared responsibility — noted"),
                    ("bottom:14%;right:7%;transform:rotate(1.5deg)","cross-ref: FILE 04 →")]),
 ('#medcoin',None, [("top:14%;right:6%;transform:rotate(-1.6deg)","origin file — sealed 2018"),
                    ("bottom:16%;left:7%;transform:rotate(2.2deg)","verdict: builder ✓")]),
]
# hero: inject into .hw ; cases: into first .folder of the section
for sid,heroCls,notes in UVS:
    if heroCls:
        i=s.find('<div class="hw"')
        j=s.find('>',i)+1
        s=s[:j]+uv(notes)+s[j:]
    else:
        si=s.find('id="%s"'%sid[1:])
        fi=s.find('<div class="folder rv"',si)
        fj=s.find('>',fi)+1
        s=s[:fj]+uv(notes)+s[fj:]
print("uv layers injected")

# --- A3. tag CASE CLOSED stamp in #final with an id ---
fi=s.find('id="final"')
seg=s[fi:fi+9000]
m=re.search(r'<div class="([a-z0-9 ]+)">CASE CLOSED</div>',seg)
assert m, "case closed stamp"
seg2=seg.replace(m.group(0),'<div class="%s" id="ccstamp">CASE CLOSED</div>'%m.group(1),1)
s=s[:fi]+seg2+s[fi+9000:]
print("ccstamp tagged")

# ============================================================ B. ENGINE PATCHES
# --- B1. acts2: expose velocity ---
a="vs+=(v-vs)*.12;"
assert a in s
s=s.replace(a,"vs+=(v-vs)*.12;window.__vs=vs;",1)

# --- B2. acts2: expose audio ---
a="var tick=function(){tn(1500,.02,.07,'square')};"
assert a in s
s=s.replace(a,a+"\nwindow.__archAudio={paper:paper,flip:flip,thunk:thunk,tick:tick,nz:nz};",1)

# --- B3. acts2: log API + hold ---
a="var logEl=null,logSecs=[],logCur=-1;"
assert a in s
s=s.replace(a,"var logEl=null,logSecs=[],logCur=-1,logHold=0;",1)
a="""  var led=document.createElement('div');led.id='recled';led.innerHTML='<i></i>ARCHIVE LIVE';
  document.body.appendChild(led);"""
assert a in s
s=s.replace(a,a+"""
  window.__archLog=function(txt,hold){if(!logEl)return;scrambleTo(logEl,'> '+txt,460);logHold=performance.now()+(hold||0);};
  window.__archLogReset=function(){logCur=-1;logHold=0;};""",1)
a="if(act>-1&&act!==logCur){"
assert a in s
s=s.replace(a,"if(act>-1&&act!==logCur&&performance.now()>logHold){",1)

# --- B4. acts2: LOGMAP interlude entry ---
a="['oasis','READING FILE 02 \\u2014 OASIS'],"
assert a in s
s=s.replace(a,a+"['interlude','CROSS-REFERENCING FILES 01 + 02'],",1)

# --- B5. acts5: LIGHTS interlude + dust hooks ---
a="['oasis','#1B1815'],"
assert a in s
s=s.replace(a,a+"['interlude','#131417'],",1)
a="var mx=-999,my=-999;"
assert a in s
s=s.replace(a,"""var idleF=1;
  window.__dustBurst=function(bx,by){try{for(var q=0;q<pts.length;q++){var dxx=pts[q].x-bx,dyy=pts[q].y-by;var dd=Math.max(60,Math.hypot(dxx,dyy));pts[q].vx+=dxx/dd*(2.6+Math.random()*3.2);pts[q].vy+=dyy/dd*(2.6+Math.random()*3.2);}}catch(e){}};
  window.__dustIdle=function(on){idleF=on?1.6:1};
  var mx=-999,my=-999;""",1)
a="pt.x+=pt.vx;pt.y+=pt.vy;"
assert a in s
s=s.replace(a,"""pt.x+=pt.vx*idleF;pt.y+=pt.vy*idleF;
        if(Math.abs(pt.vx)>.25)pt.vx*=.955;
        if(Math.abs(pt.vy)>.2)pt.vy*=.955;""",1)

# ============================================================ C. CSS
CSS="""
/* ============ INVESTIGATOR ARC ============ */
/* case meter */
#casemeter{position:fixed;right:18px;top:40px;z-index:60;text-align:right;pointer-events:none}
#casemeter .cml{font-family:'JetBrains Mono',monospace;font-weight:700;font-size:9px;letter-spacing:.26em;color:var(--lbl)}
#casemeter .cmb{margin-top:7px;display:flex;gap:6px;justify-content:flex-end}
#casemeter .sq{width:13px;height:13px;border-radius:3px;opacity:.22;position:relative;transition:opacity .4s var(--ease)}
#casemeter .sq.done{opacity:1}
#casemeter .sq.done:after{content:"\\2713";position:absolute;inset:0;display:flex;align-items:center;justify-content:center;
font-family:'JetBrains Mono',monospace;font-weight:700;font-size:9px;color:#131417;animation:sqpop .5s cubic-bezier(.3,1.4,.5,1)}
@keyframes sqpop{0%{transform:scale(0)}100%{transform:scale(1)}}
/* teaser */
#teaser{position:fixed;left:50%;bottom:0;z-index:58;transform:translate(-50%,102%);will-change:transform;pointer-events:none}
#teaser .tz{background:var(--tzc,#2FB380);color:#131417;border-radius:10px 14px 0 0;padding:10px 22px 12px;
font-family:'JetBrains Mono',monospace;font-weight:700;font-size:10px;letter-spacing:.24em;white-space:nowrap}
/* evidence tag */
#evtag{position:fixed;left:0;top:0;z-index:56;pointer-events:none;will-change:transform;display:flex;align-items:center;gap:8px;
background:var(--evc,#2FB380);color:#131417;border-radius:6px;padding:7px 12px;
font-family:'JetBrains Mono',monospace;font-weight:700;font-size:9px;letter-spacing:.2em}
#evtag i{width:7px;height:7px;border-radius:50%;border:2px solid rgba(19,20,23,.55);font-style:normal}
/* uv layer */
.uvlayer{position:absolute;inset:0;opacity:0;pointer-events:none;z-index:6;clip-path:circle(0px at 50% 50%)}
.uvn{position:absolute;font-family:'JetBrains Mono',monospace;font-weight:700;font-size:10.5px;letter-spacing:.16em;
color:var(--fc,#2FB380);white-space:nowrap}
#hero .uvn{color:#131417}
/* detective circle */
.dcwrap{position:relative}
.dcsvg{position:absolute;inset:-14px -20px;width:calc(100% + 40px);height:calc(100% + 28px);pointer-events:none;overflow:visible}
.dcsvg ellipse{fill:none;stroke-width:2.6;stroke-linecap:round;stroke-dasharray:1;stroke-dashoffset:1}
.dcsvg.draw ellipse{transition:stroke-dashoffset 1.1s cubic-bezier(.5,0,.3,1)}
.dcsvg.draw ellipse:nth-child(2){transition-delay:.22s}
.dcsvg.draw ellipse{stroke-dashoffset:0}
/* locked stamp */
#ccstamp.lk{color:var(--mut)!important;border-color:var(--grid2)!important;border-style:dashed!important;opacity:1!important;animation:none!important}
#ccstamp.ceremony{animation:stampdrop .85s cubic-bezier(.3,1.35,.45,1) both}
/* minidrawer close */
.minidrawer{position:relative}
.minidrawer.closed:before{content:"";position:absolute;left:-4px;right:-4px;top:-7px;height:5px;border-radius:3px;
background:#46494F;animation:lidin .7s var(--ease) both}
@keyframes lidin{0%{transform:translateY(-14px);opacity:0}100%{transform:translateY(0);opacity:1}}
/* interlude */
#interlude .wrap{max-width:1150px;margin:0 auto;padding:16vh 28px 14vh}
.ix-log{font-family:'JetBrains Mono',monospace;font-weight:700;font-size:12px;letter-spacing:.26em;color:var(--emb)}
.ix-board{position:relative;margin-top:46px;height:46vh;min-height:300px;border:1px solid var(--grid);border-radius:16px;background:var(--card)}
.ix-canvas{position:absolute;inset:0;width:100%;height:100%;pointer-events:none}
.ix-tab{position:absolute;display:flex;align-items:center;gap:10px;padding:11px 18px;border-radius:8px 16px 8px 8px;color:#131417}
.ix-tab b{font-family:'Fraunces',serif;font-weight:600;font-size:16px}
.ix-tab span{font-family:'JetBrains Mono',monospace;font-weight:700;font-size:8.5px;letter-spacing:.18em;opacity:.72}
.ix-a{left:7%;top:18%;background:var(--emb)}
.ix-b{right:7%;bottom:20%;background:var(--brass)}
.ix-chip{position:absolute;font-family:'Fraunces',serif;font-style:italic;font-size:14.5px;color:var(--ink);
border:1px solid var(--grid2);border-radius:9px;padding:9px 16px;background:var(--card2)}
.ix-chip.c1{left:12%;bottom:24%}
.ix-chip.c2{right:13%;top:22%}
.ix-verdict{position:absolute;left:50%;bottom:-13px;transform:translateX(-50%);background:var(--bg);padding:4px 14px;
font-family:'JetBrains Mono',monospace;font-weight:700;font-size:9px;letter-spacing:.3em;color:var(--lbl)}
/* index-board string canvas */
#ixhcv{position:absolute;inset:0;pointer-events:none;z-index:0}
/* kill-switches */
@media (max-width:860px){#casemeter,#teaser,#evtag,.uvlayer,.ix-canvas,#ixhcv,.dcsvg{display:none!important}
 .ix-board{height:auto;min-height:0;padding:26px 18px 34px}
 .ix-tab,.ix-chip{position:static;display:inline-flex;margin:8px 8px 0 0}
 .ix-verdict{position:static;transform:none;display:block;margin-top:18px;text-align:center}}
@media (prefers-reduced-motion:reduce){#casemeter,#teaser,#evtag,.uvlayer,#ixhcv{display:none!important}
 .dcsvg ellipse{stroke-dashoffset:0!important}}
body.static #casemeter,body.static #teaser,body.static #evtag,body.static .uvlayer,body.static #ixhcv,body.static .ix-canvas{display:none!important}
body.static .dcsvg ellipse{stroke-dashoffset:0!important;transition:none!important}
body.failsafe #casemeter,body.failsafe #teaser,body.failsafe #evtag,body.failsafe .uvlayer,body.failsafe #ixhcv,body.failsafe .ix-canvas{display:none!important}
body.failsafe .dcsvg ellipse{stroke-dashoffset:0!important}
"""
s=s.replace("</style>",CSS+"</style>",1)

# ============================================================ D. ACTS3 SCRIPT
JS=r"""
<script>
(function(){
"use strict";
try{
var q=new URLSearchParams(location.search);
var reduced=window.matchMedia('(prefers-reduced-motion: reduce)').matches;
var frozen=reduced||q.get('static')==='1'||window.innerWidth<861;
if(frozen){window.__acts3OK=true;return;}
function clamp(v){return v<0?0:v>1?1:v}
function bnd(v,a,b){var t=(v-a)/(b-a);t=t<0?0:t>1?1:t;return t*t*(3-2*t)}
var AU=function(){return window.__archAudio||{}};
var CASES=['xtix','oasis','eventer','medcoin'];
var CCOL={xtix:'#2FB380',oasis:'#E0A458',eventer:'#5E8FBF',medcoin:'#F2F1ED'};

/* ---------- geometry ---------- */
var vh=innerHeight,secs={},theaters={},lastWheel=0;
function measure(){
  vh=innerHeight;
  ['hero','statement','philosophy','files','interlude','leadership','tech','final'].concat(CASES).forEach(function(id){
    var el=document.getElementById(id);if(!el)return;
    var r=el.getBoundingClientRect();
    secs[id]={t:r.top+pageYOffset,b:r.top+pageYOffset+el.offsetHeight,el:el};
  });
  CASES.forEach(function(id){
    var o=document.getElementById('otx-'+id);if(!o)return;
    var r=o.getBoundingClientRect();
    theaters[id]={t:r.top+pageYOffset,h:Math.max(1,o.offsetHeight-vh)};
  });
}
addEventListener('resize',measure);
addEventListener('load',function(){setTimeout(measure,120)});
setTimeout(measure,200);setTimeout(measure,1600);
addEventListener('wheel',function(){lastWheel=performance.now()},{passive:true});

/* ---------- 1. role line + gate burst ---------- */
(function(){
  var hadBoot=!!document.getElementById('boot');
  var iv=setInterval(function(){
    if(document.getElementById('boot'))return;
    clearInterval(iv);
    if(hadBoot){
      try{if(window.__dustBurst)window.__dustBurst(innerWidth/2,innerHeight*.62)}catch(e){}
      setTimeout(function(){
        if(window.__archLog)window.__archLog('REVIEWER ACCESS GRANTED · CLEARANCE: COMMERCIAL',3200);
      },800);
    }
  },250);
})();

/* ---------- 2. case meter + reviewed set ---------- */
var meter=document.createElement('div');meter.id='casemeter';
meter.innerHTML='<div class="cml">FILES REVIEWED · <b id="cmn">0/4</b></div><div class="cmb">'+
  CASES.map(function(id){return '<span class="sq" data-c="'+id+'" style="background:'+CCOL[id]+'"></span>'}).join('')+'</div>';
document.body.appendChild(meter);
var reviewed={},reviewedN=0;
var ccstamp=document.getElementById('ccstamp'),ceremonyDone=false;
if(ccstamp){ccstamp.classList.add('lk');ccstamp.textContent='IN REVIEW · 0/4';}
function markReviewed(id){
  if(reviewed[id])return;
  reviewed[id]=true;reviewedN++;
  var el=document.getElementById('cmn');if(el)el.textContent=reviewedN+'/4';
  var sq=meter.querySelector('.sq[data-c="'+id+'"]');if(sq)sq.classList.add('done');
  try{AU().tick&&AU().tick()}catch(e){}
  if(ccstamp&&!ceremonyDone&&reviewedN<4)ccstamp.textContent='IN REVIEW · '+reviewedN+'/4';
}
function ceremony(){
  if(ceremonyDone||!ccstamp)return;
  ceremonyDone=true;
  ccstamp.classList.remove('lk');
  ccstamp.textContent='CASE CLOSED';
  void ccstamp.offsetWidth;
  ccstamp.classList.add('ceremony');
  var md=document.querySelector('.minidrawer');if(md)md.classList.add('closed');
  try{AU().thunk&&AU().thunk()}catch(e){}
  if(window.__archLog)window.__archLog('REVIEW COMPLETE · 4/4 FILES',4200);
}

/* ---------- 3. evidence tag ---------- */
var tag=document.createElement('div');tag.id='evtag';
tag.innerHTML='<i></i><b id="evtxt">CASE 2026-04</b>';
document.body.appendChild(tag);
var tx=innerWidth-160,ty=-60,tr=0,evMode='';
function tagTarget(y){
  var mid=y+vh*.5;
  if(secs.hero&&mid<secs.hero.b){
    var hw=document.querySelector('#hero .hw');
    if(hw){var r=hw.getBoundingClientRect();return {x:r.left+40,y:r.top+96,m:'hero',t:'CASE 2026-04',c:'#2FB380'};}
  }
  for(var i=0;i<CASES.length;i++){
    var id=CASES[i],sc=secs[id];
    if(sc&&mid>=sc.t&&mid<sc.b){
      var tA=sc.el.querySelector('.tabrow .tA');
      if(tA){var r2=tA.getBoundingClientRect();
        if(r2.top>-60&&r2.top<vh)return {x:r2.right+14,y:r2.top+4,m:id,t:'FILE 0'+(i+1)+' · OPEN',c:CCOL[id]};
      }
      return {x:innerWidth-166,y:vh*.4,m:id,t:'FILE 0'+(i+1)+' · OPEN',c:CCOL[id]};
    }
  }
  if(secs.final&&mid>=secs.final.t){
    if(ccstamp){var r3=ccstamp.getBoundingClientRect();
      if(r3.top>0&&r3.top<vh)return {x:r3.left,y:r3.top-46,m:'final',t:'REVIEW · '+reviewedN+'/4',c:'#2FB380'};}
    return {x:innerWidth-166,y:vh*.4,m:'final',t:'REVIEW · '+reviewedN+'/4',c:'#2FB380'};
  }
  return {x:innerWidth-166,y:vh*.42,m:'float',t:'CASE 2026-04',c:'#2FB380'};
}

/* ---------- 4. teasers ---------- */
var teaser=document.createElement('div');teaser.id='teaser';
teaser.innerHTML='<div class="tz" id="tzin"></div>';
document.body.appendChild(teaser);
var TEAS=[
 {target:'oasis', txt:'NEXT → FILE 02 · OASIS — LEADERSHIP', c:'#E0A458'},
 {target:'eventer', txt:'NEXT → FILE 03 · EVENTER — ALIGNMENT', c:'#5E8FBF'},
 {target:'medcoin', txt:'NEXT → FILE 04 · MEDCOIN — FOUNDER', c:'#F2F1ED'}
];
var tzin=document.getElementById('tzin'),tzTxt='';

/* ---------- 5. verlet strings ---------- */
var RED='#B0524E';
function mkRope(n){
  var pts=[];for(var i=0;i<n;i++)pts.push({x:0,y:0,px:0,py:0});
  return pts;
}
function ropeStep(pts,ax,ay,bx,by,imp,mxx,myy){
  var n=pts.length;
  for(var i=1;i<n-1;i++){
    var p=pts[i];
    var vx=(p.x-p.px)*.975, vy=(p.y-p.py)*.975+.5;
    p.px=p.x;p.py=p.y;p.x+=vx;p.y+=vy+imp;
    if(mxx>-9990){var dx=p.x-mxx,dy=p.y-myy,dd=dx*dx+dy*dy;
      if(dd<3600&&dd>1){var f=(3600-dd)/3600;p.x+=dx/Math.sqrt(dd)*f*7;p.y+=dy/Math.sqrt(dd)*f*7;}}
  }
  pts[0].x=ax;pts[0].y=ay;pts[n-1].x=bx;pts[n-1].y=by;
  var rest=Math.hypot(bx-ax,by-ay)*1.08/(n-1);
  for(var k=0;k<3;k++){
    for(var i2=0;i2<n-1;i2++){
      var a=pts[i2],b=pts[i2+1];
      var ddx=b.x-a.x,ddy=b.y-a.y,dl=Math.hypot(ddx,ddy)||.001;
      var diff=(dl-rest)/dl*.5;
      if(i2>0){a.x+=ddx*diff;a.y+=ddy*diff;}
      if(i2+1<n-1){b.x-=ddx*diff;b.y-=ddy*diff;}
    }
    pts[0].x=ax;pts[0].y=ay;pts[n-1].x=bx;pts[n-1].y=by;
  }
}
function ropeDraw(ctx,pts,color){
  ctx.strokeStyle=color;ctx.lineWidth=2;ctx.lineJoin='round';ctx.lineCap='round';
  ctx.beginPath();ctx.moveTo(pts[0].x,pts[0].y);
  for(var i=1;i<pts.length;i++)ctx.lineTo(pts[i].x,pts[i].y);
  ctx.stroke();
  ctx.fillStyle=color;
  ctx.beginPath();ctx.arc(pts[0].x,pts[0].y,3.4,0,7);ctx.fill();
  ctx.beginPath();ctx.arc(pts[pts.length-1].x,pts[pts.length-1].y,3.4,0,7);ctx.fill();
}
var mxG=-9999,myG=-9999;
document.addEventListener('mousemove',function(e){mxG=e.clientX;myG=e.clientY},{passive:true});

/* index-board strings */
var hpin=document.getElementById('hpin'),ixhcv=null,ixhctx=null,hRopes=null,hIntro=null,hLips=null;
if(hpin){
  ixhcv=document.createElement('canvas');ixhcv.id='ixhcv';
  hpin.insertBefore(ixhcv,hpin.firstChild);
  ixhctx=ixhcv.getContext('2d');
  hIntro=hpin.querySelector('.hintro');
  hLips=[].slice.call(hpin.querySelectorAll('.hfolder .hlip'));
  hRopes=hLips.map(function(){return mkRope(12)});
}
/* interlude string */
var ixc=document.querySelector('#interlude .ix-canvas'),ixctx=ixc?ixc.getContext('2d'):null;
var ixRope=mkRope(16);
var ixA=document.querySelector('#interlude .ix-a'),ixB=document.querySelector('#interlude .ix-b');

/* ---------- 6. UV lamp ---------- */
if(matchMedia('(pointer:fine)').matches){
  [].slice.call(document.querySelectorAll('.uvlayer')).forEach(function(layer){
    var host=layer.parentElement,raf=null;
    host.addEventListener('mousemove',function(e){
      if(raf)return;
      raf=requestAnimationFrame(function(){
        raf=null;
        var r=layer.getBoundingClientRect();
        layer.style.opacity='1';
        layer.style.clipPath='circle(120px at '+(e.clientX-r.left)+'px '+(e.clientY-r.top)+'px)';
      });
    },{passive:true});
    host.addEventListener('mouseleave',function(){layer.style.opacity='0'});
  });
}

/* ---------- 7. detective circles ---------- */
function circleStat(el,color){
  if(!el)return;
  var w=el.closest('div');if(!w)return;
  w.classList.add('dcwrap');
  var svgNS='http://www.w3.org/2000/svg';
  var svg=document.createElementNS(svgNS,'svg');svg.setAttribute('class','dcsvg');
  svg.setAttribute('viewBox','0 0 100 60');svg.setAttribute('preserveAspectRatio','none');
  for(var i=0;i<2;i++){
    var el2=document.createElementNS(svgNS,'ellipse');
    el2.setAttribute('cx',50+(i?2.5:0));el2.setAttribute('cy',30+(i?1.5:0));
    el2.setAttribute('rx',46-(i?2:0));el2.setAttribute('ry',24-(i?1.5:0));
    el2.setAttribute('pathLength','1');
    el2.setAttribute('stroke',color);
    el2.setAttribute('transform','rotate('+(i?-3:2)+' 50 30)');
    svg.appendChild(el2);
  }
  w.appendChild(svg);
  var io=new IntersectionObserver(function(es){
    es.forEach(function(en){if(en.isIntersecting){setTimeout(function(){svg.classList.add('draw')},350);io.disconnect();}});
  },{threshold:.7});
  io.observe(w);
}
(function(){
  var x3=null;
  [].slice.call(document.querySelectorAll('#xtix .bignum')).some(function(b){
    if(b.textContent.indexOf('3')>-1){x3=b;return true}return false;});
  circleStat(x3,'#2FB380');
  var o2=null;
  [].slice.call(document.querySelectorAll('#oasis .bignum,#oasis .num')).some(function(b){
    if(b.textContent.indexOf('2M')>-1){o2=b;return true}return false;});
  circleStat(o2,'#E0A458');
})();

/* ---------- 8. eventer convergence self-draw ---------- */
var evPrepped=false,evPlayed=false,evSvg=null;
(function(){
  var i=-1,svgs=[].slice.call(document.querySelectorAll('#eventer svg'));
  svgs.some(function(sv){if(sv.textContent.indexOf('CUSTOMER INSIGHT')>-1){evSvg=sv;return true}return false;});
  if(!evSvg)return;
  var paths=[].slice.call(evSvg.querySelectorAll('path')).filter(function(pp){return pp.getAttribute('fill')==='none'||!pp.getAttribute('fill')});
  var rings=[].slice.call(evSvg.querySelectorAll('circle'));
  var boxes=[].slice.call(evSvg.querySelectorAll('rect,text'));
  var tris=[].slice.call(evSvg.querySelectorAll('path')).filter(function(pp){var f=pp.getAttribute('fill');return f&&f!=='none'});
  evSvg.__parts={paths:paths,rings:rings,boxes:boxes,tris:tris};
  evPrepped=true;
  paths.forEach(function(pp){pp.setAttribute('pathLength','1');pp.style.strokeDasharray='1';pp.style.strokeDashoffset='1';pp.style.transition='none';});
  rings.forEach(function(rr){rr.setAttribute('pathLength','1');rr.style.strokeDasharray='1';rr.style.strokeDashoffset='1';rr.style.transition='none';});
  boxes.forEach(function(bb){bb.style.opacity='0';bb.style.transition='none';});
  tris.forEach(function(tt){tt.style.opacity='0';tt.style.transition='none';});
})();
function evPlay(){
  if(evPlayed||!evPrepped)return;evPlayed=true;
  var P=evSvg.__parts;
  P.boxes.forEach(function(bb,i){bb.style.transition='opacity .45s ease';setTimeout(function(){bb.style.opacity='1'},i*70);});
  P.paths.forEach(function(pp,i){pp.style.transition='stroke-dashoffset .9s cubic-bezier(.5,0,.3,1) '+(0.35+i*0.14)+'s';pp.style.strokeDashoffset='0';});
  P.rings.forEach(function(rr,i){rr.style.transition='stroke-dashoffset 1s cubic-bezier(.5,0,.3,1) '+(1.1+i*.2)+'s';rr.style.strokeDashoffset='0';});
  P.tris.forEach(function(tt,i){tt.style.transition='opacity .4s ease '+(1.5+i*.2)+'s';tt.style.opacity='1';});
  try{AU().tick&&AU().tick()}catch(e){}
}

/* ---------- 9. medcoin timeline tape ---------- */
var mdPrepped=false,mdPlayed=false,mdSvg=null;
(function(){
  var svgs=[].slice.call(document.querySelectorAll('#medcoin svg'));
  svgs.some(function(sv){if(sv.textContent.indexOf('FOUNDED')>-1){mdSvg=sv;return true}return false;});
  if(!mdSvg)return;
  var lines=[].slice.call(mdSvg.querySelectorAll('line'));
  var dashp=[].slice.call(mdSvg.querySelectorAll('path')).filter(function(pp){return (pp.getAttribute('stroke-dasharray')||pp.style.strokeDasharray)});
  var nodes=[].slice.call(mdSvg.querySelectorAll('circle'));
  var texts=[].slice.call(mdSvg.querySelectorAll('text'));
  var tris=[].slice.call(mdSvg.querySelectorAll('path')).filter(function(pp){var f=pp.getAttribute('fill');return f&&f!=='none'});
  mdSvg.__parts={lines:lines,dashp:dashp,nodes:nodes,texts:texts,tris:tris};
  mdPrepped=true;
  lines.forEach(function(l){l.setAttribute('pathLength','1');l.style.strokeDasharray='1';l.style.strokeDashoffset='1';l.style.transition='none';});
  nodes.forEach(function(nd){nd.style.opacity='0';nd.style.transition='none';});
  texts.forEach(function(tx){tx.style.opacity='0';tx.style.transition='none';});
  tris.forEach(function(tt){tt.style.opacity='0';tt.style.transition='none';});
  dashp.forEach(function(dp){dp.style.opacity='0';dp.style.transition='none';});
})();
function mdPlay(){
  if(mdPlayed||!mdPrepped)return;mdPlayed=true;
  var P=mdSvg.__parts;
  P.lines.forEach(function(l){l.style.transition='stroke-dashoffset 1.2s cubic-bezier(.5,0,.3,1) .15s';l.style.strokeDashoffset='0';});
  P.nodes.forEach(function(nd,i){nd.style.transition='opacity .35s ease '+(0.25+i*.22)+'s';nd.style.opacity='1';});
  P.texts.forEach(function(tx,i){tx.style.transition='opacity .4s ease '+(0.35+i*.2)+'s';tx.style.opacity='1';});
  P.dashp.forEach(function(dp){dp.style.transition='opacity .5s ease 1.6s';dp.style.opacity='1';});
  P.tris.forEach(function(tt){tt.style.transition='opacity .4s ease 1.85s';tt.style.opacity='1';});
  try{AU().tick&&AU().tick()}catch(e){}
}

/* ---------- master loop ---------- */
var whooshAt=0,idleAt=performance.now(),idleOn=false;
['scroll','mousemove','keydown','wheel','pointerdown'].forEach(function(ev){
  addEventListener(ev,function(){
    idleAt=performance.now();
    if(idleOn){idleOn=false;try{if(window.__dustIdle)window.__dustIdle(false)}catch(e){};if(window.__archLogReset)window.__archLogReset();}
  },{passive:true});
});
var magRest={};
function loop(){
  var y=pageYOffset,now=performance.now();
  var vs=window.__vs||0;
  /* reviewed detection */
  for(var i=0;i<CASES.length;i++){
    var sc=secs[CASES[i]];
    if(sc&&y+vh*.55>sc.b)markReviewed(CASES[i]);
  }
  /* ceremony */
  if(reviewedN===4&&secs.final&&y+vh*.6>secs.final.t)ceremony();
  /* evidence tag */
  var tt=tagTarget(y);
  tx+=(tt.x-tx)*.09;ty+=(tt.y-ty)*.09;
  tr+=((Math.max(-10,Math.min(10,vs*.35)))-tr)*.1;
  tag.style.transform='translate('+tx.toFixed(1)+'px,'+ty.toFixed(1)+'px) rotate('+tr.toFixed(2)+'deg)';
  if(evMode!==tt.m){evMode=tt.m;
    document.getElementById('evtxt').textContent=tt.t;
    tag.style.setProperty('--evc',tt.c);tag.style.background=tt.c;
  } else {
    var evt=document.getElementById('evtxt');
    if(tt.m==='final'&&evt.textContent!==tt.t)evt.textContent=tt.t;
  }
  /* teasers */
  var shown=false;
  for(var g=0;g<TEAS.length;g++){
    var th=theaters[TEAS[g].target];if(!th)continue;
    var T=th.t;
    var pr=bnd(y,T-1.75*vh,T-1.05*vh)*(1-bnd(y,T-1.02*vh,T-.88*vh));
    if(pr>.01){
      shown=true;
      if(tzTxt!==TEAS[g].txt){tzTxt=TEAS[g].txt;tzin.textContent=tzTxt;tzin.style.setProperty('--tzc',TEAS[g].c);tzin.style.background=TEAS[g].c;}
      teaser.style.transform='translate(-50%,'+((1-pr)*102)+'%)';
      break;
    }
  }
  if(!shown)teaser.style.transform='translate(-50%,102%)';
  /* index-board strings */
  if(ixhcv&&hIntro){
    var hr=hpin.getBoundingClientRect();
    if(hr.bottom>0&&hr.top<vh&&hr.height>10){
      if(ixhcv.width!==hpin.clientWidth){ixhcv.width=hpin.clientWidth;ixhcv.height=hpin.clientHeight;}
      ixhctx.clearRect(0,0,ixhcv.width,ixhcv.height);
      var ir=hIntro.getBoundingClientRect();
      var ax=ir.right-hr.left-30,ay=ir.top-hr.top+ir.height*.35;
      for(var hI=0;hI<hLips.length;hI++){
        var lr=hLips[hI].getBoundingClientRect();
        if(lr.right<hr.left-120||lr.left>hr.right+120)continue;
        var bx=lr.left-hr.left+10,by=lr.top-hr.top+lr.height*.85;
        var rope=hRopes[hI];
        if(rope[0].x===0&&rope[0].y===0){for(var rp=0;rp<rope.length;rp++){rope[rp].x=rope[rp].px=ax+(bx-ax)*rp/(rope.length-1);rope[rp].y=rope[rp].py=ay+(by-ay)*rp/(rope.length-1);}}
        ropeStep(rope,ax,ay,bx,by,Math.max(-3,Math.min(3,vs*.06)),mxG-hr.left,myG-hr.top);
        ropeDraw(ixhctx,rope,RED);
      }
    }
  }
  /* interlude string */
  if(ixc&&ixA&&ixB){
    var br=ixc.getBoundingClientRect();
    if(br.bottom>0&&br.top<vh){
      if(ixc.width!==ixc.clientWidth){ixc.width=ixc.clientWidth;ixc.height=ixc.clientHeight;}
      ixctx.clearRect(0,0,ixc.width,ixc.height);
      var ra=ixA.getBoundingClientRect(),rb=ixB.getBoundingClientRect();
      var ax2=ra.right-br.left-8,ay2=ra.bottom-br.top-6;
      var bx2=rb.left-br.left+8,by2=rb.top-br.top+6;
      if(ixRope[0].x===0){for(var rp2=0;rp2<ixRope.length;rp2++){ixRope[rp2].x=ixRope[rp2].px=ax2+(bx2-ax2)*rp2/(ixRope.length-1);ixRope[rp2].y=ixRope[rp2].py=ay2+(by2-ay2)*rp2/(ixRope.length-1);}}
      ropeStep(ixRope,ax2,ay2,bx2,by2,Math.max(-3,Math.min(3,vs*.06)),mxG-br.left,myG-br.top);
      ropeDraw(ixctx,ixRope,RED);
    }
  }
  /* signature draws */
  if(evPrepped&&!evPlayed&&evSvg){var er=evSvg.getBoundingClientRect();if(er.top<vh*.78&&er.bottom>0)evPlay();}
  if(mdPrepped&&!mdPlayed&&mdSvg){var mr=mdSvg.getBoundingClientRect();if(mr.top<vh*.8&&mr.bottom>0)mdPlay();}
  /* whoosh */
  if(Math.abs(vs)>17&&now-whooshAt>300){whooshAt=now;
    try{if(AU().nz)AU().nz(.2,Math.min(1300,420+Math.abs(vs)*6),170,.05)}catch(e){}
  }
  /* magnetic completion */
  for(var mg=0;mg<CASES.length;mg++){
    var thm=theaters[CASES[mg]];if(!thm)continue;
    var tpm=(y-thm.t)/thm.h;
    if(tpm>.84&&tpm<.985&&Math.abs(vs)<.5&&now-lastWheel>420){
      if(!magRest[CASES[mg]])magRest[CASES[mg]]=now;
      else if(now-magRest[CASES[mg]]>460){
        var se=document.scrollingElement;
        se.scrollTop=se.scrollTop+((thm.t+thm.h)-y)*.06;
      }
    } else magRest[CASES[mg]]=0;
  }
  /* idle life */
  if(!idleOn&&now-idleAt>6000){
    idleOn=true;
    try{if(window.__dustIdle)window.__dustIdle(true)}catch(e){}
    if(window.__archLog)window.__archLog('ARCHIVE IDLE — FILES AWAITING REVIEW',2600);
  }
  requestAnimationFrame(loop);
}
requestAnimationFrame(loop);
window.__acts3OK=true;
}catch(err){
  try{
    ['casemeter','teaser','evtag','ixhcv'].forEach(function(id){var el=document.getElementById(id);if(el)el.remove()});
    [].slice.call(document.querySelectorAll('svg')).forEach(function(sv){
      [].slice.call(sv.querySelectorAll('*')).forEach(function(el){
        if(el.style){el.style.opacity='';el.style.strokeDashoffset='';el.style.strokeDasharray='';}
      });
    });
  }catch(e){}
}
})();
</script>"""
s=s.rstrip()+"\n"+JS

io.open(p,"w",encoding="utf-8").write(s)
head='<!doctype html>\n<html lang="en">\n<head>\n<meta charset="utf-8">\n<meta name="viewport" content="width=device-width,initial-scale=1">\n<meta name="color-scheme" content="dark">\n</head>\n<body>\n'
io.open("site_standalone.html","w",encoding="utf-8").write(head+s+"\n</body>\n</html>")
print("INVESTIGATOR ARC built:",len(s),"bytes")
