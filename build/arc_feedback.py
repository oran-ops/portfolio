# -*- coding: utf-8 -*-
# Arc feedback round: remove interlude+UV+hero-barcode, visible clearance chip,
# stable evidence tag (hysteresis+fixed slot), long teaser w/ approach fill,
# in-view ceremony w/ slam, visible idle cue, stronger magnetic/whoosh.
import io, re
s = io.open("site.html", encoding="utf-8").read()

# ---------- 1. REMOVALS ----------
# interlude section
i = s.find('<section class="sec" id="interlude">')
assert i > -1
j = s.find('</section>', i) + len('</section>')
# include trailing newline
if s[j:j+1] == '\n': j += 1
s = s[:i] + s[j:]
# LOGMAP + LIGHTS entries
a = "['interlude','CROSS-REFERENCING FILES 01 + 02'],"
assert a in s; s = s.replace(a, "", 1)
a = "['interlude','#131417'],"
assert a in s; s = s.replace(a, "", 1)
# uv layers
s, n = re.subn(r'<div class="uvlayer" aria-hidden="true">.*?</div>', '', s, flags=re.S)
assert n == 5, "uv removal %d" % n
# hero barcode (engine null-safe on .barc)
m = re.search(r'<div class="barc rv"[^>]*>.*?</svg>\s*<div class="yr">[^<]*</div>\s*</div>\s*', s, flags=re.S)
if not m: m = re.search(r'<div class="barc rv"[^>]*>.*?</div>\s*</div>\s*', s, flags=re.S)
assert m, "hero barc"
s = s[:m.start()] + s[m.end():]
print("removed: interlude, uv x5, hero barcode")

# ---------- 2. CSS additions ----------
CSS = """
/* clearance chip (role moment) */
#clearance{position:fixed;left:50%;top:16%;transform:translate(-50%,-8px);z-index:99990;opacity:0;
background:#1A1B1F;border:2px solid var(--emb);border-radius:8px;padding:13px 26px;pointer-events:none;
font-family:'JetBrains Mono',monospace;font-weight:700;font-size:11px;letter-spacing:.28em;color:var(--emb);
transition:opacity .5s var(--ease),transform .6s cubic-bezier(.3,1.2,.4,1);white-space:nowrap}
#clearance.on{opacity:1;transform:translate(-50%,0)}
/* evidence tag text morph */
#evtag b{display:inline-block}
#evtag.sw b{animation:tagsw .45s var(--ease)}
@keyframes tagsw{0%{transform:translateY(-9px);opacity:0}100%{transform:translateY(0);opacity:1}}
/* teaser approach fill */
#teaser .tz{position:relative;overflow:hidden}
#teaser .tz i{position:absolute;left:0;top:0;bottom:0;width:0;background:rgba(19,20,23,.16);font-style:normal}
#teaser .tz b{position:relative;font-weight:700}
/* ceremony */
#ccstamp.ceremony{animation:ccslam .75s cubic-bezier(.3,1.3,.45,1) both!important}
@keyframes ccslam{0%{opacity:0;transform:scale(2.1) rotate(-14deg)}62%{opacity:1;transform:scale(.94) rotate(-4deg)}100%{opacity:1;transform:scale(1) rotate(-6deg)}}
.minidrawer>*{transition:none}
.minidrawer.closed>*{animation:stripin .5s var(--ease) both}
.minidrawer.closed>*:nth-child(2){animation-delay:.14s}
.minidrawer.closed>*:nth-child(3){animation-delay:.28s}
.minidrawer.closed>*:nth-child(4){animation-delay:.42s}
@keyframes stripin{0%{transform:translateY(-24px);opacity:0}100%{transform:translateY(0);opacity:1}}
/* idle cue */
#idlecue{position:fixed;left:50%;bottom:56px;transform:translateX(-50%) translateY(18px);z-index:59;opacity:0;
background:transparent;border:1px solid var(--grid2);border-radius:8px;padding:9px 18px;pointer-events:none;
font-family:'JetBrains Mono',monospace;font-weight:700;font-size:9.5px;letter-spacing:.28em;color:var(--lbl);
transition:opacity .6s var(--ease),transform .6s var(--ease)}
#idlecue.on{opacity:1;transform:translateX(-50%) translateY(0);animation:idlebob 2.2s ease-in-out .6s infinite}
@keyframes idlebob{0%,100%{transform:translateX(-50%) translateY(0)}50%{transform:translateX(-50%) translateY(6px)}}
body.static #clearance,body.static #idlecue,body.failsafe #clearance,body.failsafe #idlecue{display:none!important}
@media (max-width:860px){#clearance,#idlecue{display:none!important}}
"""
s = s.replace("</style>", CSS + "</style>", 1)

# ---------- 3. acts3 JS surgery ----------
# 3a. role hook -> also show clearance chip; QA &role=1
OLD = """(function(){
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
})();"""
NEW = """var clearanceEl=document.createElement('div');
clearanceEl.id='clearance';
clearanceEl.textContent='\\u25C6 REVIEWER ACCESS GRANTED \\u2014 CLEARANCE: COMMERCIAL';
document.body.appendChild(clearanceEl);
function showClearance(){
  clearanceEl.classList.add('on');
  if(window.__archLog)window.__archLog('REVIEWER ACCESS GRANTED · CLEARANCE: COMMERCIAL',3400);
  setTimeout(function(){clearanceEl.classList.remove('on')},3000);
}
(function(){
  var hadBoot=!!document.getElementById('boot');
  if(q.get('role')==='1')setTimeout(showClearance,1200);
  var iv=setInterval(function(){
    if(document.getElementById('boot'))return;
    clearInterval(iv);
    if(hadBoot){
      try{if(window.__dustBurst)window.__dustBurst(innerWidth/2,innerHeight*.62)}catch(e){}
      setTimeout(showClearance,700);
    }
  },250);
})();"""
assert OLD in s; s = s.replace(OLD, NEW, 1)

# 3b. tag: fixed slot + hysteresis, no per-frame dock chasing
OLD = """var tx=innerWidth-160,ty=-60,tr=0,evMode='';
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
}"""
NEW = """var tx=innerWidth-176,ty=-60,tr=0,evMode='',evZone='',evZoneAt=0;
function calcZone(y){
  var mid=y+vh*.5;
  if(secs.hero&&mid<secs.hero.b-180)return 'hero';
  if(secs.final&&mid>=secs.final.t+120)return 'final';
  for(var i=0;i<CASES.length;i++){var sc=secs[CASES[i]];
    if(sc&&mid>=sc.t+120&&mid<sc.b-120)return CASES[i];}
  return 'slot';
}
function tagTarget(y,now){
  var z=calcZone(y);
  if(z!==evZone){
    if(!evZoneAt)evZoneAt=now;
    if(now-evZoneAt>380){evZone=z;evZoneAt=0;}
  } else evZoneAt=0;
  var Z=evZone||z;
  if(Z==='hero'){
    var hw=document.querySelector('#hero .hw');
    if(hw){var r=hw.getBoundingClientRect();
      if(r.bottom>120)return {x:r.left+36,y:Math.max(14,r.top+88),m:'hero',t:'CASE 2026-04',c:'#2FB380'};}
  }
  if(Z==='final'&&ccstamp){
    var r3=ccstamp.getBoundingClientRect();
    if(r3.top>60&&r3.top<vh-40)return {x:r3.left,y:r3.top-46,m:'final',t:'REVIEW · '+reviewedN+'/4',c:'#2FB380'};
    return {x:innerWidth-176,y:76,m:'final',t:'REVIEW · '+reviewedN+'/4',c:'#2FB380'};
  }
  for(var i2=0;i2<CASES.length;i2++){
    if(Z===CASES[i2])return {x:innerWidth-176,y:76,m:Z,t:'FILE 0'+(i2+1)+' · OPEN',c:CCOL[Z]};
  }
  return {x:innerWidth-176,y:76,m:'slot',t:'CASE 2026-04',c:'#2FB380'};
}"""
assert OLD in s; s = s.replace(OLD, NEW, 1)

# tag apply: pass now + morph animation on text change
OLD = """  /* evidence tag */
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
  }"""
NEW = """  /* evidence tag */
  var tt=tagTarget(y,now);
  tx+=(tt.x-tx)*.11;ty+=(tt.y-ty)*.11;
  tr+=((Math.max(-8,Math.min(8,vs*.3)))-tr)*.1;
  tag.style.transform='translate('+tx.toFixed(1)+'px,'+ty.toFixed(1)+'px) rotate('+tr.toFixed(2)+'deg)';
  if(evMode!==tt.m){evMode=tt.m;
    document.getElementById('evtxt').textContent=tt.t;
    tag.style.background=tt.c;
    tag.classList.remove('sw');void tag.offsetWidth;tag.classList.add('sw');
  } else {
    var evt=document.getElementById('evtxt');
    if(tt.m==='final'&&evt.textContent!==tt.t)evt.textContent=tt.t;
  }"""
assert OLD in s; s = s.replace(OLD, NEW, 1)

# 3c. teaser: long window + approach fill
OLD = """teaser.innerHTML='<div class="tz" id="tzin"></div>';"""
NEW = """teaser.innerHTML='<div class="tz" id="tzw"><i id="tzf"></i><b id="tzin"></b></div>';"""
assert OLD in s; s = s.replace(OLD, NEW, 1)
OLD = """var tzin=document.getElementById('tzin'),tzTxt='';"""
NEW = """var tzin=document.getElementById('tzin'),tzw=document.getElementById('tzw'),tzf=document.getElementById('tzf'),tzTxt='';"""
assert OLD in s; s = s.replace(OLD, NEW, 1)
OLD = """  /* teasers */
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
  if(!shown)teaser.style.transform='translate(-50%,102%)';"""
NEW = """  /* teasers — long accompany window + approach fill */
  var shown=false;
  for(var g=0;g<TEAS.length;g++){
    var th=theaters[TEAS[g].target];if(!th)continue;
    var T=th.t;
    var pr=bnd(y,T-3.1*vh,T-2.5*vh)*(1-bnd(y,T-1.04*vh,T-.9*vh));
    if(pr>.01){
      shown=true;
      if(tzTxt!==TEAS[g].txt){tzTxt=TEAS[g].txt;tzin.textContent=tzTxt;tzw.style.background=TEAS[g].c;}
      var fill=bnd(y,T-3.1*vh,T-1.06*vh);
      tzf.style.width=(fill*100).toFixed(1)+'%';
      teaser.style.transform='translate(-50%,'+((1-pr)*102)+'%)';
      break;
    }
  }
  if(!shown)teaser.style.transform='translate(-50%,102%)';"""
assert OLD in s; s = s.replace(OLD, NEW, 1)

# 3d. ceremony: trigger only when stamp visible
OLD = """  /* ceremony */
  if(reviewedN===4&&secs.final&&y+vh*.6>secs.final.t)ceremony();"""
NEW = """  /* ceremony — only when the stamp is actually in view */
  if(reviewedN===4&&!ceremonyDone&&ccstamp){
    var ccr=ccstamp.getBoundingClientRect();
    if(ccr.top<vh*.82&&ccr.bottom>40)ceremony();
  }"""
assert OLD in s; s = s.replace(OLD, NEW, 1)

# 3e. idle: visible cue chip + 8s threshold
OLD = """var whooshAt=0,idleAt=performance.now(),idleOn=false;"""
NEW = """var whooshAt=0,idleAt=performance.now(),idleOn=false;
var idlecue=document.createElement('div');idlecue.id='idlecue';
idlecue.textContent='\\u25BE CONTINUE REVIEW';document.body.appendChild(idlecue);"""
assert OLD in s; s = s.replace(OLD, NEW, 1)
OLD = """    idleAt=performance.now();
    if(idleOn){idleOn=false;try{if(window.__dustIdle)window.__dustIdle(false)}catch(e){};if(window.__archLogReset)window.__archLogReset();}"""
NEW = """    idleAt=performance.now();
    if(idleOn){idleOn=false;idlecue.classList.remove('on');
      try{if(window.__dustIdle)window.__dustIdle(false)}catch(e){};if(window.__archLogReset)window.__archLogReset();}"""
assert OLD in s; s = s.replace(OLD, NEW, 1)
OLD = """  if(!idleOn&&now-idleAt>6000){
    idleOn=true;
    try{if(window.__dustIdle)window.__dustIdle(true)}catch(e){}
    if(window.__archLog)window.__archLog('ARCHIVE IDLE — FILES AWAITING REVIEW',2600);
  }"""
NEW = """  if(!idleOn&&now-idleAt>8000){
    idleOn=true;
    idlecue.classList.add('on');
    try{if(window.__dustIdle)window.__dustIdle(true)}catch(e){}
    if(window.__archLog)window.__archLog('ARCHIVE IDLE — FILES AWAITING REVIEW',2600);
  }"""
assert OLD in s; s = s.replace(OLD, NEW, 1)

# 3f. magnetic stronger + whoosh more present
OLD = "se.scrollTop=se.scrollTop+((thm.t+thm.h)-y)*.06;"
assert OLD in s; s = s.replace(OLD, "se.scrollTop=se.scrollTop+((thm.t+thm.h)-y)*.13;", 1)
OLD = "if(Math.abs(vs)>17&&now-whooshAt>300){whooshAt=now;"
assert OLD in s; s = s.replace(OLD, "if(Math.abs(vs)>12&&now-whooshAt>280){whooshAt=now;", 1)
OLD = "AU().nz(.2,Math.min(1300,420+Math.abs(vs)*6),170,.05)"
assert OLD in s; s = s.replace(OLD, "AU().nz(.22,Math.min(1300,420+Math.abs(vs)*6),170,.09)", 1)

io.open("site.html", "w", encoding="utf-8").write(s)
head = ('<!doctype html>\n<html lang="en">\n<head>\n<meta charset="utf-8">\n'
        '<meta name="viewport" content="width=device-width,initial-scale=1">\n'
        '<meta name="color-scheme" content="dark">\n</head>\n<body>\n')
io.open("site_standalone.html", "w", encoding="utf-8").write(head + s + "\n</body>\n</html>")
print("ARC FEEDBACK ROUND APPLIED:", len(s))
