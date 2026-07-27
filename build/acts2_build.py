# -*- coding: utf-8 -*-
# ARCHIVE ALIVE II — drawer-pull theaters, buttery scroll, velocity shear,
# zoom-through, live LOG, decrypt labels, archive audio. Max edition.
import io, re
p="site.html"; s=io.open(p,encoding="utf-8").read()

# ---------- 1. remove seccovers (replaced by theaters) ----------
s,n=re.subn(r'\s*<div class="seccover"[^>]*><span class="sct">[^<]*</span></div>','',s)
assert n==4, "seccover removal %d"%n

# ---------- 2. theaters ----------
CASES=[
 ("xtix","var(--emb)","#131417","01","XTIX","BUILT FROM ZERO","C-01"),
 ("oasis","var(--brass)","#131417","02","Oasis","LEADERSHIP","C-02"),
 ("eventer","var(--ice)","#131417","03","Eventer","ALIGNMENT","C-03"),
 ("medcoin","var(--ink)","#131417","04","Medcoin","FOUNDER","C-04"),
]
def theater(sid,oc,ink,num,nm,cat,code):
    return ('<div class="otx" id="otx-%s" data-sec="%s">\n'
    '  <div class="ots">\n'
    '    <div class="otroom">\n'
    '      <div class="otf" style="--oc:%s;--oink:%s">\n'
    '        <div class="otf-under">\n'
    '          <div class="ou-num">%s</div>\n'
    '          <div class="ou-lines">\n'
    '            <div class="ou-l">CASE FILE %s &mdash; %s</div>\n'
    '            <div class="ou-l">STATUS: <b>DECLASSIFIED</b></div>\n'
    '            <div class="ou-red"></div><div class="ou-red w2"></div>\n'
    '            <div class="ou-l dim">&gt; EVIDENCE ENCLOSED &mdash; CONTINUE</div>\n'
    '          </div>\n'
    '        </div>\n'
    '        <div class="otf-veil"></div>\n'
    '        <div class="otf-cover">\n'
    '          <div class="oc-lip"><b>%s</b><span>FILE %s</span></div>\n'
    '          <div class="oc-eyebrow">CASE FILE &middot; COMMERCIAL ARCHIVE</div>\n'
    '          <div class="oc-cat">%s</div>\n'
    '          <div class="oc-class">&gt; classification: COMMERCIAL<br>&gt; drawer: %s &middot; archive 2026</div>\n'
    '          <div class="oc-barc" aria-hidden="true"><i>%s</i></div>\n'
    '          <div class="oc-conf">CONFIDENTIAL</div>\n'
    '          <span class="oc-hole" style="top:26%%"></span><span class="oc-hole" style="top:44%%"></span>\n'
    '        </div>\n'
    '      </div>\n'
    '      <div class="otdrw">\n'
    '        <div class="od-face">\n'
    '          <span class="od-handle"></span>\n'
    '          <span class="od-lab">ARCHIVE DRAWER %s &middot; COMMERCIAL RECORDS</span>\n'
    '        </div>\n'
    '      </div>\n'
    '      <div class="otstat">PULLING FILE %s &mdash; %s</div>\n'
    '    </div>\n'
    '  </div>\n'
    '</div>')%(sid,sid,oc,ink,num,num,nm.upper(),nm,num,cat,code,code,code,num,nm.upper())

for sid,oc,ink,num,nm,cat,code in CASES:
    pat=r'(<section class="sec case" id="%s"[^>]*>)'%sid
    s,n=re.subn(pat,lambda m:m.group(1)+'\n  '+theater(sid,oc,ink,num,nm,cat,code),s,count=1)
    assert n==1, "theater "+sid

# ---------- 3. tune existing engines ----------
# smoother inertia glide
assert 'cur+=(target-cur)*.11;' in s
s=s.replace('cur+=(target-cur)*.11;','cur+=(target-cur)*.085;',1)
assert 'target=Math.max(0,Math.min(maxY(),target+d));' in s
s=s.replace('target=Math.max(0,Math.min(maxY(),target+d));','target=Math.max(0,Math.min(maxY(),target+d*.92));',1)
# shorter horizontal pin (faster flow)
assert '.hwrap{height:380vh}' in s
s=s.replace('.hwrap{height:380vh}','.hwrap{height:330vh}',1)
# htrack transform carries velocity shear too
assert "htrack.style.transform='translateX('+(-X)+'px)';" in s
s=s.replace("htrack.style.transform='translateX('+(-X)+'px)';",
            "htrack.style.transform='translateX('+(-X)+'px) skewY(var(--vsk,0deg))';",1)

# ---------- 4. CSS ----------
CSS="""
/* ============== ARCHIVE ALIVE II ============== */
/* velocity shear */
.sec>.wrap{transform:skewY(var(--vsk,0deg))}
/* drawer-pull theaters */
.otx{height:165vh;position:relative;z-index:5}
.ots{position:sticky;top:0;height:100svh;overflow:hidden;pointer-events:none}
.otroom{position:absolute;inset:0;perspective:1500px}
.otf{position:absolute;left:50%;top:50%;width:min(680px,74vw);height:min(60vh,470px);
margin:calc(min(60vh,470px)/-2) 0 0 calc(min(680px,74vw)/-2);z-index:1;will-change:transform;transform-style:preserve-3d;
transform:translateY(44vh) scale(.62)}
.otf-cover{position:absolute;inset:0;background:var(--oc);border-radius:0 22px 18px 18px;
transform-origin:50% 0;will-change:transform;backface-visibility:hidden;padding:44px 40px;z-index:3}
.oc-lip{position:absolute;top:-34px;left:0;height:34px;background:var(--oc);border-radius:10px 20px 0 0;
display:flex;align-items:center;gap:12px;padding:0 18px}
.oc-lip b{font-family:'Fraunces',serif;font-weight:600;font-size:17px;color:var(--oink)}
.oc-lip span{font-family:'JetBrains Mono',monospace;font-weight:700;font-size:9px;letter-spacing:.18em;color:var(--oink);opacity:.62}
.oc-eyebrow{font-family:'JetBrains Mono',monospace;font-weight:700;font-size:9.5px;letter-spacing:.3em;color:var(--oink);opacity:.6}
.oc-cat{margin-top:12px;font-weight:800;font-size:clamp(34px,4.4vw,60px);line-height:1;letter-spacing:-.02em;color:var(--oink)}
.oc-class{margin-top:18px;font-family:'JetBrains Mono',monospace;font-size:12px;line-height:1.9;color:var(--oink);opacity:.85}
.oc-barc{position:absolute;right:38px;top:40px;width:96px;height:34px;
background:repeating-linear-gradient(90deg,var(--oink) 0 2px,transparent 2px 5px,var(--oink) 5px 8px,transparent 8px 10px)}
.oc-barc i{position:absolute;left:0;right:0;top:100%;margin-top:4px;font-style:normal;text-align:center;
font-family:'JetBrains Mono',monospace;font-size:8px;letter-spacing:.34em;color:var(--oink);opacity:.7}
.oc-conf{position:absolute;right:34px;bottom:34px;transform:rotate(-6deg);border:2px solid var(--oink);border-radius:4px;
padding:6px 12px;font-family:'JetBrains Mono',monospace;font-weight:700;font-size:10px;letter-spacing:.3em;color:var(--oink);opacity:.8}
.oc-hole{position:absolute;left:20px;width:14px;height:14px;border:2px solid var(--oink);opacity:.35;border-radius:50%}
.otf-under{position:absolute;inset:0;background:var(--card);border:1px solid var(--grid);border-radius:0 22px 18px 18px;
padding:44px 40px;z-index:1;overflow:hidden}
.ou-num{position:absolute;right:18px;bottom:-24px;font-weight:800;font-size:200px;line-height:1;color:transparent;
-webkit-text-stroke:1.5px var(--grid2);letter-spacing:-.04em}
.ou-lines{position:relative;z-index:1}
.ou-l{font-family:'JetBrains Mono',monospace;font-size:12.5px;letter-spacing:.14em;color:var(--lbl);margin-top:10px}
.ou-l b{color:var(--emb);font-weight:700}
.ou-l.dim{margin-top:22px;color:var(--mut)}
.ou-red{margin-top:14px;height:12px;width:62%;background:#0F1013;border-radius:2px}
.ou-red.w2{width:44%;margin-top:8px}
.otf-veil{position:absolute;inset:0;background:rgba(19,20,23,.55);border-radius:0 22px 18px 18px;z-index:2;pointer-events:none}
.otdrw{position:absolute;left:50%;bottom:0;width:min(900px,86vw);transform:translateX(-50%);z-index:4;will-change:transform,opacity}
.od-face{position:relative;height:17vh;min-height:110px;background:#101114;border:1px solid var(--grid);border-bottom:0;border-radius:14px 14px 0 0}
.od-face:before{content:"";position:absolute;left:0;right:0;top:0;height:10px;background:#0B0C0E;border-radius:14px 14px 0 0}
.od-handle{position:absolute;left:50%;top:34px;transform:translateX(-50%);width:120px;height:10px;border-radius:6px;
background:#26282D;border:1px solid var(--grid2)}
.od-lab{position:absolute;left:50%;bottom:22px;transform:translateX(-50%);white-space:nowrap;
font-family:'JetBrains Mono',monospace;font-weight:700;font-size:9.5px;letter-spacing:.3em;color:var(--dim)}
.otstat{position:absolute;left:50%;bottom:26px;transform:translateX(-50%);z-index:5;white-space:nowrap;
font-family:'JetBrains Mono',monospace;font-weight:700;font-size:10px;letter-spacing:.32em;color:var(--lbl)}
/* zoom-through slab */
.zoomer{position:fixed;z-index:9998;display:flex;align-items:center;justify-content:center;
border-radius:20px;will-change:left,top,width,height;transition:left .52s cubic-bezier(.7,0,.2,1),top .52s cubic-bezier(.7,0,.2,1),
width .52s cubic-bezier(.7,0,.2,1),height .52s cubic-bezier(.7,0,.2,1),border-radius .52s cubic-bezier(.7,0,.2,1),opacity .4s ease}
.zoomer span{font-weight:800;font-size:clamp(30px,5vw,64px);letter-spacing:-.02em;color:#131417}
/* live log */
#loglin{position:fixed;left:18px;bottom:16px;z-index:60;font-family:'JetBrains Mono',monospace;
font-weight:700;font-size:9.5px;letter-spacing:.22em;color:var(--lbl);pointer-events:none}
#loglin:after{content:"_";animation:logc 1.1s steps(1) infinite;color:var(--emb)}
@keyframes logc{50%{opacity:0}}
/* rec led */
#recled{position:fixed;right:18px;top:14px;z-index:60;font-family:'JetBrains Mono',monospace;font-weight:700;
font-size:9px;letter-spacing:.28em;color:var(--lbl);pointer-events:none;display:flex;align-items:center;gap:7px}
#recled i{width:7px;height:7px;border-radius:50%;background:var(--emb);animation:recb 2.4s ease-in-out infinite}
@keyframes recb{0%,100%{opacity:1}50%{opacity:.2}}
/* sound toggle */
#sndtg{position:fixed;right:18px;bottom:16px;z-index:70;background:transparent;border:1px solid var(--grid2);border-radius:6px;
color:var(--lbl);font-family:'JetBrains Mono',monospace;font-weight:700;font-size:9px;letter-spacing:.26em;
padding:7px 12px;cursor:pointer}
#sndtg.off{color:var(--dim);border-color:var(--grid)}
#sndtg:hover{border-color:var(--emb);color:var(--emb)}
/* graph bar hover */
.bar0:hover rect:first-child{fill:#3DD598}
/* kill-switches */
@media (max-width:860px){.otx,#loglin,#recled,#sndtg{display:none!important}.sec>.wrap{transform:none}}
@media (prefers-reduced-motion:reduce){.otx,#loglin,#recled,#sndtg{display:none!important}.sec>.wrap{transform:none!important}}
body.static .otx,body.static #loglin,body.static #recled,body.static #sndtg{display:none!important}
body.static .sec>.wrap{transform:none!important}
body.failsafe .otx,body.failsafe #loglin,body.failsafe #recled,body.failsafe #sndtg{display:none!important}
body.failsafe .sec>.wrap{transform:none!important}
"""
s=s.replace("</style>",CSS+"</style>",1)

# ---------- 5. acts2 JS ----------
JS="""
<script>
(function(){
"use strict";
try{
var q=new URLSearchParams(location.search);
var reduced=window.matchMedia('(prefers-reduced-motion: reduce)').matches;
var frozen=reduced||q.get('static')==='1'||window.innerWidth<861;
function clamp(v){return v<0?0:v>1?1:v}
function eo(p){return 1-Math.pow(1-p,3)}

/* ================= archive audio ================= */
var AC=null,master=null;
var sndOn=true;
try{sndOn=(localStorage.getItem('arch_snd')||'1')==='1'}catch(e){}
function ac(){
  if(!AC){
    var C=window.AudioContext||window.webkitAudioContext;if(!C)return null;
    AC=new C();master=AC.createGain();master.gain.value=.13;master.connect(AC.destination);
  }
  if(AC.state==='suspended')AC.resume();
  return AC;
}
function nz(dur,f0,f1,g){
  if(!sndOn||frozen)return;
  try{var c=ac();if(!c)return;
    var b=c.createBuffer(1,Math.max(1,Math.floor(c.sampleRate*dur)),c.sampleRate),d=b.getChannelData(0);
    for(var i=0;i<d.length;i++)d[i]=(Math.random()*2-1)*(1-i/d.length);
    var src=c.createBufferSource();src.buffer=b;
    var f=c.createBiquadFilter();f.type='lowpass';
    f.frequency.setValueAtTime(f0,c.currentTime);
    f.frequency.exponentialRampToValueAtTime(Math.max(40,f1),c.currentTime+dur);
    var gg=c.createGain();gg.gain.setValueAtTime(g,c.currentTime);
    gg.gain.exponentialRampToValueAtTime(.001,c.currentTime+dur);
    src.connect(f);f.connect(gg);gg.connect(master);src.start();
  }catch(e){}
}
function tn(fr,dur,g,type){
  if(!sndOn||frozen)return;
  try{var c=ac();if(!c)return;
    var o=c.createOscillator();o.type=type||'sine';o.frequency.value=fr;
    var gg=c.createGain();gg.gain.setValueAtTime(g,c.currentTime);
    gg.gain.exponentialRampToValueAtTime(.001,c.currentTime+dur);
    o.connect(gg);gg.connect(master);o.start();o.stop(c.currentTime+dur);
  }catch(e){}
}
var paper=function(){nz(.30,900,220,.5)};
var flip=function(){nz(.13,1500,480,.34);tn(520,.06,.10,'triangle')};
var thunk=function(){tn(72,.15,.5,'sine');nz(.05,420,160,.35)};
var tick=function(){tn(1500,.02,.07,'square')};
if(!frozen){
  var tg=document.createElement('button');tg.id='sndtg';tg.type='button';
  tg.textContent=sndOn?'SND ON':'SND OFF';tg.classList.toggle('off',!sndOn);
  document.body.appendChild(tg);
  tg.addEventListener('click',function(){
    sndOn=!sndOn;
    try{localStorage.setItem('arch_snd',sndOn?'1':'0')}catch(e){}
    tg.textContent=sndOn?'SND ON':'SND OFF';tg.classList.toggle('off',!sndOn);
    if(sndOn){ac();tick();}
  });
  var oldOpen=window.__bootOpen;
  if(oldOpen){window.__bootOpen=function(){ac();paper();oldOpen()}}
  document.addEventListener('click',function first(){document.removeEventListener('click',first);ac();paper();},{once:true});
}

/* ================= theaters ================= */
var THS=[].slice.call(document.querySelectorAll('.otx')).map(function(x){
  return {x:x,ots:x.querySelector('.ots'),otf:x.querySelector('.otf'),
    cover:x.querySelector('.otf-cover'),veil:x.querySelector('.otf-veil'),
    drw:x.querySelector('.otdrw'),stat:x.querySelector('.otstat'),
    lab:x.querySelector('.otstat').textContent,t:0,h:1,lp:-1,sndA:0,sndB:0};
});
if(frozen)THS=[];

/* ================= live log + decrypt ================= */
var GLY='#@%&$/\\\\<>=+*'.split('');
function scrambleTo(el,txt,ms){
  var t0=performance.now(),n=txt.length;
  (function fr(now){
    var p=clamp((now-t0)/ms);
    var k=Math.floor(p*n),out='';
    for(var i=0;i<n;i++){
      var ch=txt.charAt(i);
      out+= i<k?ch:(ch===' '?' ':GLY[(i*7+Math.floor(now/46))%GLY.length]);
    }
    el.textContent=out;
    if(p<1)requestAnimationFrame(fr);
  })(t0);
}
var LOGMAP=[['hero','MASTER FILE \\u2014 ORAN CARMON'],['statement','MEMO \\u2014 FROM THE ARCHIVE'],
 ['philosophy','OPERATING SYSTEM \\u2014 05 LAYERS'],['files','CASE INDEX \\u2014 04 FILES'],
 ['xtix','READING FILE 01 \\u2014 XTIX'],['oasis','READING FILE 02 \\u2014 OASIS'],
 ['eventer','READING FILE 03 \\u2014 EVENTER'],['medcoin','READING FILE 04 \\u2014 MEDCOIN'],
 ['leadership','LEADERSHIP FILE \\u2014 TESTIMONY'],['tech','SYSTEM FILE \\u2014 COMMERCIAL AI'],
 ['final','CASE CLOSED \\u2014 CONTACT']];
var logEl=null,logSecs=[],logCur=-1;
if(!frozen){
  logEl=document.createElement('div');logEl.id='loglin';logEl.textContent='> ARCHIVE://2026';
  document.body.appendChild(logEl);
  var led=document.createElement('div');led.id='recled';led.innerHTML='<i></i>ARCHIVE LIVE';
  document.body.appendChild(led);
  logSecs=LOGMAP.map(function(a){var el=document.getElementById(a[0]);return el?{el:el,txt:a[1],t:0,b:0}:null}).filter(Boolean);
}
/* decrypt-on-reveal for plain mono labels */
if(!frozen&&'IntersectionObserver' in window){
  var dio=new IntersectionObserver(function(es){
    es.forEach(function(en){
      if(!en.isIntersecting)return;
      var el=en.target;dio.unobserve(el);
      var txt=el.dataset.dorig;if(!txt)return;
      scrambleTo(el,txt,460);
    });
  },{threshold:.4});
  [].forEach.call(document.querySelectorAll('.tok,.smeta,.hcat,.vlab'),function(el){
    if(el.children.length)return;
    el.dataset.dorig=el.textContent;
    dio.observe(el);
  });
}

/* ================= zoom-through open ================= */
if(!frozen){
  [].forEach.call(document.querySelectorAll('.hcta'),function(a){
    a.addEventListener('click',function(ev){
      ev.preventDefault();ev.stopPropagation();
      var id=a.getAttribute('href'),sec=document.querySelector(id);
      if(!sec)return;
      var card=a.closest('.hfolder'),r=card.getBoundingClientRect();
      var cl=document.createElement('div');cl.className='zoomer';
      cl.style.left=r.left+'px';cl.style.top=r.top+'px';
      cl.style.width=r.width+'px';cl.style.height=r.height+'px';
      cl.style.background=getComputedStyle(card).backgroundColor;
      var nmEl=card.querySelector('.hcat');
      cl.innerHTML='<span>'+(nmEl?nmEl.textContent:'FILE')+'</span>';
      document.body.appendChild(cl);
      paper();
      requestAnimationFrame(function(){requestAnimationFrame(function(){
        cl.style.left='0px';cl.style.top='0px';cl.style.width='100vw';cl.style.height='100vh';cl.style.borderRadius='0';
      })});
      setTimeout(function(){
        var otx=document.getElementById('otx-'+id.slice(1));
        var Y=sec.getBoundingClientRect().top+window.pageYOffset;
        if(otx){
          var oR=otx.getBoundingClientRect();
          Y=(oR.top+window.pageYOffset)+(otx.offsetHeight-innerHeight)*.88;
        }
        window.scrollTo({top:Y,left:0,behavior:'instant'});
        flip();
        cl.style.opacity='0';
        setTimeout(function(){try{cl.remove()}catch(e){}},430);
      },560);
    },true);
  });
}

/* ================= marquee velocity coupling ================= */
var tkAnims=[];
if(!frozen){
  setTimeout(function(){
    try{
      [].forEach.call(document.querySelectorAll('.ticker .tk'),function(tk){
        if(tk.getAnimations){tk.getAnimations().forEach(function(a){tkAnims.push(a)})}
      });
    }catch(e){}
  },1500);
}

/* ================= master loop: velocity + shear + theaters + log ================= */
var vh=window.innerHeight;
function measure(){
  vh=window.innerHeight;
  THS.forEach(function(th){
    var r=th.x.getBoundingClientRect();
    th.t=r.top+window.pageYOffset;
    th.h=Math.max(1,th.x.offsetHeight-vh);
  });
  logSecs.forEach(function(l){
    var r=l.el.getBoundingClientRect();
    l.t=r.top+window.pageYOffset;l.b=l.t+l.el.offsetHeight;
  });
}
window.addEventListener('resize',measure);
window.addEventListener('load',function(){setTimeout(measure,90)});
setTimeout(measure,140);setTimeout(measure,1400);

var pv=window.pageYOffset,vs=0;
function loop(){
  var y=window.pageYOffset;
  var v=y-pv;pv=y;
  vs+=(v-vs)*.12;
  if(!frozen){
    /* velocity shear */
    var sk=Math.max(-1.4,Math.min(1.4,vs*.016));
    if(Math.abs(sk)<.02)sk=0;
    document.documentElement.style.setProperty('--vsk',sk.toFixed(3)+'deg');
    /* marquee coupling */
    if(tkAnims.length){
      var pr=1+Math.min(2.6,Math.abs(vs)*.055);
      if(vs<-1)pr=-pr;
      for(var i=0;i<tkAnims.length;i++){try{tkAnims[i].playbackRate=pr}catch(e){}}
    }
    /* theaters */
    for(var j=0;j<THS.length;j++){
      var th=THS[j];
      var tp=clamp((y-th.t)/th.h);
      if(tp===th.lp)continue;
      /* sound triggers on upward crossings */
      var now=performance.now();
      if(th.lp>-1&&th.lp<.04&&tp>=.04&&now-th.sndA>1200){th.sndA=now;paper();}
      if(th.lp>-1&&th.lp<.56&&tp>=.56&&now-th.sndB>1200){th.sndB=now;flip();}
      th.lp=tp;
      if(tp>=1){
        th.ots.style.visibility='hidden';
        continue;
      }
      th.ots.style.visibility='';
      var pull=eo(clamp(tp/.42));
      th.otf.style.transform='translateY('+((1-pull)*44)+'vh) scale('+(.62+.38*pull)+')';
      var dfade=clamp((tp-.40)/.18);
      th.drw.style.opacity=String(1-dfade);
      th.drw.style.transform='translateX(-50%) translateY('+(eo(dfade)*9)+'vh)';
      var open=eo(clamp((tp-.55)/.30));
      th.cover.style.transform='rotateX('+(-open*112)+'deg)';
      th.veil.style.opacity=String((1-open)*.55);
      var exit=eo(clamp((tp-.88)/.12));
      th.ots.style.opacity=String(1-exit);
      th.ots.style.transform='translateY('+(-exit*7)+'vh)';
      var msg = tp<.5?('PULLING '+th.lab.replace('PULLING ','')):(tp<.86?'OPENING FILE \\u2026':'FILE OPEN \\u2014 READ \\u2193');
      if(th.stat.textContent!==msg)th.stat.textContent=msg;
    }
    /* live log */
    if(logEl){
      var mid=y+vh*.5,act=-1;
      for(var k=0;k<logSecs.length;k++){if(mid>=logSecs[k].t&&mid<logSecs[k].b){act=k;break}}
      if(act>-1&&act!==logCur){
        logCur=act;
        scrambleTo(logEl,'> '+logSecs[act].txt,420);
        tick();
      }
    }
  }
  requestAnimationFrame(loop);
}
requestAnimationFrame(loop);

/* stamp thunk when final CASE CLOSED reveals */
if(!frozen&&'IntersectionObserver' in window){
  var fin=document.querySelector('#final .folder');
  if(fin){
    var fio=new IntersectionObserver(function(es){
      es.forEach(function(en){if(en.isIntersecting){thunk();fio.disconnect();}});
    },{threshold:.5});
    fio.observe(fin);
  }
}
window.__acts2OK=true;
}catch(err){
  try{
    [].forEach.call(document.querySelectorAll('.otx'),function(x){x.style.display='none'});
    document.documentElement.style.setProperty('--vsk','0deg');
  }catch(e){}
}
})();
</script>"""
s=s.rstrip()+"\n"+JS

io.open(p,"w",encoding="utf-8").write(s)
print("ARCHIVE ALIVE II built:",len(s),"bytes")

full=("<!doctype html>\n<html lang=\"en\">\n<head>\n<meta charset=\"utf-8\">\n"
"<meta name=\"viewport\" content=\"width=device-width,initial-scale=1\">\n"
"<meta name=\"color-scheme\" content=\"dark\">\n</head>\n<body>\n"+s+"\n</body>\n</html>")
io.open("site_standalone.html","w",encoding="utf-8").write(full)
print("standalone rebuilt")
