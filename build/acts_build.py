# -*- coding: utf-8 -*-
# ARCHIVE ALIVE — all 10 acts, maximum edition
import io, re
p="site.html"; s=io.open(p,encoding="utf-8").read()

# ============================================================ ACT 1 — boot gate theater
s=s.replace('<div class="bbar"><i id="bootbar"></i></div>',
'<div class="bbar"><i id="bootbar"></i></div>\n  <div class="bl2">PROCESSING<span class="dots"><i>.</i><i>.</i><i>.</i></span></div>',1)

old_boot="""    if(pr<1)requestAnimationFrame(step);
    else{
      setTimeout(function(){
        boot.classList.add('done');
        document.documentElement.style.overflow='';
        document.querySelectorAll('#hero .rv.on').forEach(function(el){
          el.classList.remove('on');void el.offsetWidth;el.classList.add('on');
        });
        setTimeout(function(){boot.remove()},820);
      },140);
    }"""
new_boot="""    if(pr<1)requestAnimationFrame(step);
    else{
      boot.dataset.gate='1';
      var g=document.createElement('button');
      g.id='bootgate';g.type='button';
      g.innerHTML='OPEN CASE FILE <b>&#8250;</b>';
      boot.appendChild(g);
      requestAnimationFrame(function(){g.classList.add('in')});
      var opened=false;
      var doOpen=function(){
        if(opened)return;opened=true;
        boot.classList.add('done');
        document.documentElement.style.overflow='';
        document.querySelectorAll('#hero .rv.on').forEach(function(el){
          el.classList.remove('on');void el.offsetWidth;el.classList.add('on');
        });
        if(window.__actOpen)window.__actOpen();
        setTimeout(function(){try{boot.remove()}catch(e){}},860);
      };
      window.__bootOpen=doOpen;
      boot.addEventListener('click',doOpen);
      window.addEventListener('keydown',function k(){window.removeEventListener('keydown',k);doOpen();});
    }"""
assert old_boot in s, "boot completion anchor"
s=s.replace(old_boot,new_boot,1)

old_wd="""  setTimeout(function(){
    var b=document.getElementById('boot');
    if(b){try{b.remove()}catch(e){}}
    document.documentElement.style.overflow='';
  },4200);"""
new_wd="""  setTimeout(function(){
    var b=document.getElementById('boot');
    if(b&&b.dataset.gate!=='1'){
      try{b.remove()}catch(e){}
      document.documentElement.style.overflow='';
      if(window.__actOpen)window.__actOpen();
    }
  },5200);"""
assert old_wd in s, "watchdog anchor"
s=s.replace(old_wd,new_wd,1)

# ============================================================ ACT 2 — drawer-pull hero
s=s.replace('</div>\n  <div class="cue">',
'<div id="drawerlip" aria-hidden="true"><span class="dlh"></span></div></div>\n  <div class="cue">',1)

# ============================================================ ACT 3 — horizontal case index (rebuild #files)
mfiles=re.search(r'<section class="sec" id="files">.*?</section>',s,flags=re.S)
assert mfiles, "files section"
old_files=mfiles.group(0)
mt=re.search(r'<div class="ticker.*?</span></div></div>',old_files,flags=re.S)
ticker=mt.group(0) if mt else ''

def hfolder(color,ink,nm,fl,cat,doss,href):
    d=('<div class="hdoss">%s</div>'%doss) if doss else ''
    return ('<div class="hcard hfolder" style="--hc:%s;--hink:%s">'
    '<div class="hlip"><span class="nm">%s</span><span class="fl">%s</span></div>'
    '<div class="hcat">%s</div>'+d+
    '<a class="hcta" href="%s">OPEN FILE <b>&#8250;</b></a>'
    '<span class="hole2" style="top:70px"></span><span class="hole2" style="top:112px"></span>'
    '</div>')%(color,ink,nm,fl,cat,href)

NEW_FILES=('<section class="sec" id="files">\n'
'  <div class="secnum" aria-hidden="true">02</div>\n'
'  <div class="hwrap" id="hwrap">\n'
'    <div class="hpin" id="hpin">\n'
'      <div class="htrack" id="htrack">\n'
'        <div class="hcard hintro">\n'
'          <div class="bigt">THE CASE<br>FILES</div>\n'
'          <div class="fmeta">EXECUTIVE PORTFOLIO &middot; 04 DOSSIERS &middot; 2018&ndash;2026</div>\n'
'          <div class="hhint">SCROLL &mdash; THE DRAWER SLIDES &#8250;</div>\n'
'        </div>\n'
+hfolder("var(--emb)","#131417","XTIX","FILE 01","BUILT FROM ZERO",
 "&gt; commercial function: none &rarr; operating system<br>&gt; pipeline: &euro;0 &rarr; &euro;3M+ ARR &middot; 7 enterprise closed","#xtix")
+hfolder("var(--brass)","#131417","Oasis","FILE 02","LEADERSHIP","","#oasis")
+hfolder("var(--ice)","#131417","Eventer","FILE 03","ALIGNMENT","","#eventer")
+hfolder("var(--ink)","#131417","Medcoin","FILE 04","FOUNDER","","#medcoin")
+'        <div class="hcard hend">\n'
'          <div class="hendt">04 FILES &middot; ONE SYSTEM</div>\n'
'          <div class="hhint">CONTINUE &darr;</div>\n'
'        </div>\n'
'      </div>\n'
'    </div>\n'
'  </div>\n'
'  <div class="wrap">'+ticker+'</div>\n'
'</section>')
s=s.replace(old_files,NEW_FILES,1)

# ============================================================ ACT 8 — section covers
COVERS=[("xtix","#16241D","FILE 01 &middot; UNSEALING"),
        ("oasis","#201B13","FILE 02 &middot; UNSEALING"),
        ("eventer","#151B22","FILE 03 &middot; UNSEALING"),
        ("medcoin","#1B1C1E","FILE 04 &middot; UNSEALING")]
for sid,tint,lab in COVERS:
    s=re.sub(r'(<section class="sec case" id="%s"[^>]*>)'%sid,
             r'\1\n  <div class="seccover" style="background:%s" aria-hidden="true"><span class="sct">%s</span></div>'%(tint,lab),
             s,count=1)

# ============================================================ ACT 9 — live clock in footer
s=s.replace('<span>EXECUTIVE PORTFOLIO &middot; DOSSIER ARCHIVE &middot; 2026</span>',
'<span>EXECUTIVE PORTFOLIO &middot; DOSSIER ARCHIVE &middot; <b id="archclock">--:--:--</b></span>',1)

# ============================================================ CSS — all acts
CSS="""
/* ===================== ARCHIVE ALIVE ===================== */
#boot .bl2{margin-top:14px;font-family:'JetBrains Mono',monospace;font-size:9px;letter-spacing:.3em;color:var(--lbl)}
#boot .dots i{display:inline-block;font-style:normal;animation:dotb 1.2s infinite}
#boot .dots i:nth-child(2){animation-delay:.2s}
#boot .dots i:nth-child(3){animation-delay:.4s}
@keyframes dotb{0%,60%,100%{opacity:.15}30%{opacity:1}}
#bootgate{margin-top:30px;background:transparent;border:2px solid var(--emb);border-radius:8px;color:var(--emb);
font-family:'JetBrains Mono',monospace;font-weight:700;font-size:12px;letter-spacing:.3em;padding:13px 26px;cursor:pointer;
opacity:0;transform:translateY(14px) rotate(-2deg);transition:opacity .5s var(--ease),transform .5s cubic-bezier(.34,1.35,.4,1)}
#bootgate.in{opacity:1;transform:translateY(0) rotate(-2deg)}
#bootgate:hover{background:var(--emb);color:#131417}
#bootgate b{font-weight:700}

html.preopen #hero .hw{transform:perspective(1400px) translateY(11vh) rotateX(7deg) scale(.965);opacity:.4}
#hero .hw{transition:transform 1.15s cubic-bezier(.16,1,.3,1),opacity .9s var(--ease)}
#drawerlip{position:relative;height:22px;margin:-6px 12px 0;background:#101114;border:1px solid var(--grid);border-top:0;border-radius:0 0 14px 14px}
#drawerlip .dlh{position:absolute;left:50%;top:8px;transform:translateX(-50%);width:74px;height:5px;border-radius:3px;background:var(--grid2)}
html.preopen #drawerlip{transform:translateY(-14px)}
#drawerlip{transition:transform 1.15s cubic-bezier(.16,1,.3,1)}

/* horizontal case index */
.hwrap{height:380vh}
.hpin{position:sticky;top:0;height:100svh;overflow:hidden;display:flex;align-items:center;cursor:grab}
.hpin.drag{cursor:grabbing}
.htrack{display:flex;align-items:center;gap:5vw;padding:0 12vw;width:max-content;will-change:transform}
.hcard{flex:0 0 auto}
.hintro{width:34vw;min-width:300px}
.hintro .bigt{font-weight:800;font-size:clamp(40px,5.6vw,72px);line-height:1;letter-spacing:-.03em;text-transform:uppercase}
.hintro .fmeta{margin-top:16px;font-family:'JetBrains Mono',monospace;font-size:11px;letter-spacing:.2em;color:var(--mut)}
.hhint{margin-top:26px;font-family:'JetBrains Mono',monospace;font-size:9.5px;letter-spacing:.26em;color:var(--lbl)}
.hfolder{position:relative;width:56vw;max-width:720px;height:min(58vh,480px);background:var(--hc);
border-radius:0 24px 20px 20px;padding:46px 42px;transform:scale(var(--sc,.94));will-change:transform}
.hfolder .hlip{position:absolute;top:-36px;left:-1px;height:36px;background:var(--hc);border-radius:10px 22px 0 0;
display:flex;align-items:center;gap:13px;padding:0 20px}
.hfolder .hlip .nm{font-family:'Fraunces',serif;font-weight:600;font-size:18px;color:var(--hink)}
.hfolder .hlip .fl{font-family:'JetBrains Mono',monospace;font-weight:700;font-size:9px;letter-spacing:.18em;color:var(--hink);opacity:.62}
.hfolder .hcat{font-weight:800;font-size:clamp(30px,3.6vw,52px);letter-spacing:-.02em;color:var(--hink);line-height:1.02}
.hfolder .hdoss{margin-top:20px;font-family:'JetBrains Mono',monospace;font-size:12.5px;line-height:1.85;color:var(--hink);opacity:.85}
.hfolder .hcta{position:absolute;left:42px;bottom:36px;display:inline-flex;align-items:center;gap:10px;
font-family:'JetBrains Mono',monospace;font-weight:700;font-size:11px;letter-spacing:.22em;color:var(--hink);
border:2px solid var(--hink);border-radius:8px;padding:11px 18px;transition:transform .3s var(--ease)}
.hfolder .hcta:hover{transform:translateX(6px)}
.hfolder .hole2{position:absolute;left:22px;width:15px;height:15px;border:2px solid var(--hink);opacity:.35;border-radius:50%}
.hend{width:26vw;min-width:220px;text-align:center}
.hendt{font-family:'JetBrains Mono',monospace;font-weight:700;font-size:12px;letter-spacing:.3em;color:var(--mut)}
#files .wrap{padding-top:0}
@media (max-width:860px){
 .hwrap{height:auto}
 .hpin{position:static;height:auto;overflow:visible;cursor:default}
 .htrack{flex-direction:column;width:auto;padding:0 18px;gap:56px;transform:none!important}
 .hintro,.hfolder,.hend{width:100%;max-width:none}
 .hfolder{height:auto;min-height:300px;padding:38px 24px 84px}
}

/* section covers */
.sec.case{position:relative}
.seccover{position:absolute;inset:0;z-index:6;display:flex;align-items:center;justify-content:center;
pointer-events:none;will-change:transform}
.seccover .sct{font-family:'JetBrains Mono',monospace;font-weight:700;font-size:11px;letter-spacing:.4em;color:var(--lbl)}

/* declassify field report */
.reality .frow{position:relative}
.reality .frow .redct{position:absolute;top:3px;bottom:3px;left:28px;right:52px;background:#0F1013;transform-origin:right;z-index:2}
.u.on .reality .frow .redct{transform:scaleX(0);transition:transform .6s var(--ease) calc(var(--i,0)*140ms + .45s)}
.reality .frow:hover .st2{color:var(--emb)}
.reality .frow{transition:transform .3s var(--ease)}
.u.done .reality .frow:hover{transform:translateX(5px)}

/* edge arrivals */
.frail{opacity:0;transform:translateX(-26px)}
.folder.on .frail,.u.on .frail{opacity:1;transform:none;transition:opacity .7s var(--ease) .15s,transform .7s var(--ease) .15s}
.tabrow .tB{opacity:0;transform:translateX(22px)}
.folder.on .tabrow .tB{opacity:1;transform:none;transition:opacity .6s var(--ease) .4s,transform .6s var(--ease) .4s}
.rstampS{opacity:0}
.folder.on .rstampS{animation:stampdrop .85s cubic-bezier(.3,1.35,.45,1) .5s both}
@keyframes stampdrop{0%{opacity:0;transform:rotate(-14deg) translateY(-56px) scale(1.15)}70%{opacity:1;transform:rotate(-5deg) translateY(3px) scale(1)}100%{opacity:1;transform:rotate(-6deg) translateY(0) scale(1)}}

/* breathing charts */
.breathe{animation:bob2 7s ease-in-out infinite}
@keyframes bob2{0%,100%{transform:translateY(0)}50%{transform:translateY(-3px)}}

/* cursor label */
#curlbl{position:fixed;top:0;left:0;pointer-events:none;z-index:9999;font-family:'JetBrains Mono',monospace;
font-weight:700;font-size:8.5px;letter-spacing:.22em;color:var(--emb);opacity:0;transform:translate(-120px,-120px);transition:opacity .2s}
#curlbl.show{opacity:1}

/* archive clock */
#archclock{color:var(--mut);font-weight:600}

/* kill-switches */
body.static .seccover,body.failsafe .seccover{display:none!important}
body.static .redct{transform:scaleX(0)!important}
body.static .frail,body.static .tabrow .tB{opacity:1!important;transform:none!important}
body.static .rstampS{opacity:1!important;animation:none!important}
body.static .breathe,body.static #boot .dots i{animation:none!important}
html.preopen body.static #hero .hw{transform:none;opacity:1}
@media (prefers-reduced-motion:reduce){
 .seccover{display:none!important}
 .redct{transform:scaleX(0)!important}
 .frail,.tabrow .tB{opacity:1!important;transform:none!important}
 .rstampS{opacity:1!important;animation:none!important}
 .breathe,#boot .dots i{animation:none!important}
 html.preopen #hero .hw,html.preopen #drawerlip{transform:none;opacity:1}
 .hwrap{height:auto}.hpin{position:static;height:auto}.htrack{transform:none!important;flex-wrap:wrap;width:auto}
}
body.failsafe .redct{display:none}
body.failsafe .frail,body.failsafe .tabrow .tB,body.failsafe .rstampS{opacity:1!important;transform:none!important;animation:none!important}
"""
s=s.replace("</style>",CSS+"</style>",1)

# ============================================================ ACTS JS (script block 5)
JS="""
<script>
(function(){
"use strict";
try{
var q=new URLSearchParams(location.search);
var reduced=window.matchMedia('(prefers-reduced-motion: reduce)').matches;
var isStatic=q.get('static')==='1';
var frozen=reduced||isStatic;
function clamp(v){return v<0?0:v>1?1:v}

/* ---- ACT 2: preopen state until boot gate ---- */
var bootEl=document.getElementById('boot');
if(bootEl&&!frozen){document.documentElement.classList.add('preopen');}
window.__actOpen=function(){
  document.documentElement.classList.remove('preopen');
};
setTimeout(function(){document.documentElement.classList.remove('preopen')},9000);

/* ---- declassify bars ---- */
document.querySelectorAll('.reality .frow').forEach(function(r){
  var b=document.createElement('span');b.className='redct';r.appendChild(b);
});

/* ---- breathing charts ---- */
var BR=['#xtix .tech svg','#xtix .gaug','#oasis .cols2 svg','#eventer .cols2 svg','#medcoin .hairtop svg','#tech .archw svg'];
var bi=0;
BR.forEach(function(sel){
  var el=document.querySelector(sel);
  if(el&&!frozen){el.classList.add('breathe');el.style.animationDelay=(bi*0.9)+'s';bi++;}
});

/* ---- ACT 9: live archive clock ---- */
var ck=document.getElementById('archclock');
if(ck){
  var tick=function(){
    var d=new Date();
    var pad=function(n){return (n<10?'0':'')+n};
    ck.textContent=pad(d.getHours())+':'+pad(d.getMinutes())+':'+pad(d.getSeconds());
  };
  tick();setInterval(tick,1000);
}

/* ---- ACT 9: cursor label ---- */
if(!frozen&&window.matchMedia('(pointer:fine)').matches){
  var lbl=document.createElement('div');lbl.id='curlbl';document.body.appendChild(lbl);
  var lx=-120,ly=-120,tx=-120,ty=-120;
  document.addEventListener('mousemove',function(e){
    tx=e.clientX;ty=e.clientY;
    var t=e.target;
    var txt='';
    if(t.closest&&t.closest('.hfolder'))txt='OPEN FILE';
    else if(t.closest&&t.closest('.hpin'))txt='DRAG / SCROLL';
    else if(t.closest&&t.closest('.reality .frow'))txt='DECLASSIFIED';
    else if(t.closest&&t.closest('#hero .itab, #files a'))txt='OPEN';
    else if(t.closest&&t.closest('#final .crow'))txt='CONTACT';
    lbl.textContent=txt;
    lbl.classList.toggle('show',!!txt);
  },{passive:true});
  (function ll(){
    lx+=(tx-lx)*.2;ly+=(ty-ly)*.2;
    lbl.style.transform='translate('+(lx+22)+'px,'+(ly+24)+'px)';
    requestAnimationFrame(ll);
  })();
}

/* ---- ACT 3+8+4+10: scroll-driven systems ---- */
var hwrap=document.getElementById('hwrap'),hpin=document.getElementById('hpin'),htrack=document.getElementById('htrack');
var hcards=htrack?[].slice.call(htrack.querySelectorAll('.hcard')):[];
var covers=[].slice.call(document.querySelectorAll('.seccover')).map(function(c){return {el:c,sec:c.parentElement,t:0,h:0}});
var LIGHTS=[['hero','#131417'],['statement','#131417'],['philosophy','#131417'],['files','#131417'],
 ['xtix','#14201B'],['oasis','#1B1815'],['eventer','#141920'],['medcoin','#17181B'],
 ['leadership','#131417'],['tech','#14201B'],['final','#131417']];
var lights=LIGHTS.map(function(a){var el=document.getElementById(a[0]);return el?{el:el,c:a[1],t:0,b:0}:null}).filter(Boolean);
function hx(c){return [parseInt(c.substr(1,2),16),parseInt(c.substr(3,2),16),parseInt(c.substr(5,2),16)]}
var curL=hx('#131417'),tgtL=hx('#131417');

var hwTop=0,hwH=0,vh=window.innerHeight,maxX=0;
var dragOff=0,dragV=0,dragging=false,lastPX=0;
function measure(){
  vh=window.innerHeight;
  if(hwrap&&hpin&&htrack){
    hwTop=hwrap.getBoundingClientRect().top+window.pageYOffset;
    hwH=hwrap.offsetHeight;
    maxX=Math.max(0,htrack.scrollWidth-hpin.clientWidth);
  }
  covers.forEach(function(c){
    c.t=c.sec.getBoundingClientRect().top+window.pageYOffset;
    c.h=c.sec.offsetHeight;
  });
  lights.forEach(function(l){
    l.t=l.el.getBoundingClientRect().top+window.pageYOffset;
    l.b=l.t+l.el.offsetHeight;
  });
}
window.addEventListener('resize',measure);
window.addEventListener('load',function(){setTimeout(measure,80)});
setTimeout(measure,120);setTimeout(measure,1200);

/* drag inertia on the horizontal pin */
if(hpin&&!frozen&&window.matchMedia('(pointer:fine)').matches){
  hpin.addEventListener('pointerdown',function(e){
    if(window.innerWidth<860)return;
    dragging=true;lastPX=e.clientX;dragV=0;hpin.classList.add('drag');
  });
  window.addEventListener('pointermove',function(e){
    if(!dragging)return;
    var dx=e.clientX-lastPX;lastPX=e.clientX;
    dragOff-=dx*1.15;dragV=-dx*1.15;
  },{passive:true});
  window.addEventListener('pointerup',function(){dragging=false;hpin.classList.remove('drag');});
}

var mob=window.matchMedia('(max-width:860px)');
function frame(){
  var y=window.pageYOffset;
  if(!frozen){
    /* horizontal drawer */
    if(htrack&&!mob.matches){
      var span=hwH-vh;
      var hp=span>0?clamp((y-hwTop)/span):0;
      if(!dragging){dragOff+=dragV;dragV*=.94;dragOff*=.90;if(Math.abs(dragOff)<.4)dragOff=0;}
      var X=hp*maxX+dragOff;
      htrack.style.transform='translateX('+(-X)+'px)';
      var cx=window.innerWidth/2;
      for(var i=0;i<hcards.length;i++){
        var r=hcards[i].getBoundingClientRect();
        var d=Math.abs(r.left+r.width/2-cx)/window.innerWidth;
        hcards[i].style.setProperty('--sc',String(1.02-Math.min(.1,d*.22)));
      }
    }
    /* section covers */
    for(var j=0;j<covers.length;j++){
      var c=covers[j];
      var pr=clamp((y+vh-c.t)/(vh*.85));
      c.el.style.transform='translateY('+(-pr*103)+'%)';
    }
    /* room relight */
    var mid=y+vh*.5;
    for(var k=0;k<lights.length;k++){
      if(mid>=lights[k].t&&mid<lights[k].b){tgtL=hx(lights[k].c);break;}
    }
    curL[0]+=(tgtL[0]-curL[0])*.06;curL[1]+=(tgtL[1]-curL[1])*.06;curL[2]+=(tgtL[2]-curL[2])*.06;
    document.body.style.backgroundColor='rgb('+Math.round(curL[0])+','+Math.round(curL[1])+','+Math.round(curL[2])+')';
  }
  requestAnimationFrame(frame);
}
if(!frozen)requestAnimationFrame(frame);

/* ---- ACT 9: dust canvas ---- */
if(!frozen){
  var dc=document.createElement('canvas');dc.id='dust';
  dc.style.cssText='position:fixed;inset:0;z-index:1;pointer-events:none;opacity:.5';
  document.body.insertBefore(dc,document.body.firstChild);
  var ctx=dc.getContext('2d');
  var W=0,H=0,pts=[];
  function dsize(){
    W=dc.width=window.innerWidth;H=dc.height=window.innerHeight;
  }
  dsize();window.addEventListener('resize',dsize);
  for(var n=0;n<64;n++){
    pts.push({x:Math.random()*1600,y:Math.random()*900,r:Math.random()*1.4+.4,
      vx:(Math.random()-.5)*.16,vy:(Math.random()-.5)*.12,o:Math.random()*.35+.1});
  }
  var mx=-999,my=-999;
  document.addEventListener('mousemove',function(e){mx=e.clientX;my=e.clientY},{passive:true});
  (function dl(){
    if(!document.hidden){
      ctx.clearRect(0,0,W,H);
      ctx.fillStyle='#8E8E93';
      for(var i2=0;i2<pts.length;i2++){
        var pt=pts[i2];
        pt.x+=pt.vx;pt.y+=pt.vy;
        var ddx=pt.x-mx,ddy=pt.y-my,dd=ddx*ddx+ddy*ddy;
        if(dd<12000){var f=(12000-dd)/12000;pt.x+=ddx*f*.045;pt.y+=ddy*f*.045;}
        if(pt.x<-8)pt.x=W+8;if(pt.x>W+8)pt.x=-8;
        if(pt.y<-8)pt.y=H+8;if(pt.y>H+8)pt.y=-8;
        ctx.globalAlpha=pt.o;
        ctx.fillRect(pt.x,pt.y,pt.r,pt.r);
      }
      ctx.globalAlpha=1;
    }
    requestAnimationFrame(dl);
  })();
}
window.__actsOK=true;
}catch(err){
  try{document.documentElement.classList.remove('preopen')}catch(e){}
  try{var b2=document.getElementById('boot');if(b2)b2.remove();document.documentElement.style.overflow='';}catch(e){}
}
})();
</script>"""
s=s.rstrip()+"\n"+JS

io.open(p,"w",encoding="utf-8").write(s)
print("ARCHIVE ALIVE built:",len(s),"bytes")

# standalone rebuild
full=("<!doctype html>\n<html lang=\"en\">\n<head>\n<meta charset=\"utf-8\">\n"
"<meta name=\"viewport\" content=\"width=device-width,initial-scale=1\">\n"
"<meta name=\"color-scheme\" content=\"dark\">\n</head>\n<body>\n"+s+"\n</body>\n</html>")
io.open("site_standalone.html","w",encoding="utf-8").write(full)
print("standalone rebuilt")
