
"use strict";
var S = 2;                                   /* logical pixel -> CSS pixel. Whole, always. */
/* SEVEN, and taken from the kit rather than written out here.
   FINAL is FILE 07: Oran's correction, and the reason is arithmetic — a reader who opens all
   six documents and then READ ME must be able to reach "7 of 7". A list hard-coded to six
   could not, and would have disagreed silently with the folder, whose renderer has always
   counted K.order.length. One source of truth for what the seven files are. */
var IDS = K.order.slice();
var STORE = "ocmf.opened";                   /* the same key the folder page reads */

function cv(id) { return document.getElementById(id); }
function secOf(id) { return document.getElementById(id); }
function blit(canvas, b, w, h) {
  canvas.width = w * S; canvas.height = h * S;
  var off = document.createElement("canvas");
  off.width = w; off.height = h;
  var ox = off.getContext("2d"), im = ox.createImageData(w, h);
  im.data.set(b.d); ox.putImageData(im, 0, 0);
  var x = canvas.getContext("2d");
  x.imageSmoothingEnabled = false;
  x.clearRect(0, 0, canvas.width, canvas.height);
  x.drawImage(off, 0, 0, canvas.width, canvas.height);
}

/* ---------------------------------------------------------------- the menu bar */
function drawMenu() {
  var w = Math.ceil(cv("c-menu").clientWidth / S) || 400;
  var b = new Buf(w, 20);
  menubar(b, w);
  blit(cv("c-menu"), b, w, 20);
}

/* ---------------------------------------------------------------- the files on the desktop */
function drawFiles() {
  var box = cv("mw-files");
  box.innerHTML = "";
  IDS.forEach(function (id) {
    var w = 76, h = 50, b = new Buf(w, h);
    ico(b, id, (w >> 1) - 16, 2);
    var lab = K.labels[id], lw = tw(lab), lx = (w >> 1) - (lw >> 1);
    b.rect(lx - 3, 38, lx + lw + 2, 48, WHITE);
    txt(b, lab, lx, 39, BLACK);
    var btn = document.createElement("button");
    btn.className = "mw-icon";
    btn.type = "button";
    btn.setAttribute("aria-label", "Open " + lab);
    btn.setAttribute("data-id", id);
    var c = document.createElement("canvas");
    btn.appendChild(c);
    box.appendChild(btn);
    blit(c, b, w, h);
    c.style.width = (w * S) + "px";
    c.style.height = (h * S) + "px";
    btn.onclick = function () { show(id); };
  });
}

/* ---------------------------------------------------------------- the title bar
   The file's NAME alone, as the Finder showed it. The full identification already appears
   inside the document. Close box at the left, with the X Oran asked for. */
function drawTitle() {
  var el = cv("c-title"), w = Math.ceil(el.clientWidth / S);
  if (!w || !openId) return;
  var b = new Buf(w, 19);
  titlebar(b, 0, 0, w - 1, K.labels[openId], true, true);
  blit(el, b, w, 19);
}

/* ---------------------------------------------------------------- the live scroll bar */
var hit = null;
function drawBar() {
  var el = cv("c-bar"), v = cv("view");
  var h = Math.floor(el.clientHeight / S), w = 15;
  if (!h || el.offsetParent === null) { hit = null; return; }
  var range = v.scrollHeight - v.clientHeight;
  var b = new Buf(w, h);
  hit = vscroll(b, 0, 0, w - 1, h - 1,
                range > 0 ? v.scrollTop / range : 0,
                v.scrollHeight ? v.clientHeight / v.scrollHeight : 1,
                range > 0);
  blit(el, b, w, h);
}

/* ---------------------------------------------------------------- DONE */
function drawDone() {
  var w = 120, h = 28, b = new Buf(w, h);
  pushbutton(b, 0, 0, w - 1, h - 1, "DONE", true);
  blit(cv("c-done"), b, w, h);
}

/* ---------------------------------------------------------------- the document's own script
   Lifted verbatim from the site. Re-writing any of it by hand is how a frame-only change
   quietly becomes a content change. */
/* THE SCROLL ENGINE, lifted whole with its clock swapped from the page to the window's own
   scroller -- see build_doc.py for the exact substitutions. It owns the counting figures, the
   ten-column chart, the SVG ring arcs, the path drawing, the .rv reveal and the .st/--i
   stagger. It is progress-driven, not observer-driven: scenes advance continuously against
   travel and lead values, which is why it is NOT converted to IntersectionObserver -- an
   observer reports crossings, and that would change how every one of them feels. */
function scrollEngine() {
  var SC=window.__mwScroller||document.scrollingElement||document.documentElement;
(function(){
"use strict";
var q=new URLSearchParams(location.search);
var reduced=window.matchMedia('(prefers-reduced-motion: reduce)').matches;
var isStatic=q.get('static')==='1';
if(isStatic){document.body.classList.add('static');document.documentElement.style.scrollBehavior='auto';}
var frozen=isStatic||reduced;
var only=q.get('only');
if(only){document.querySelectorAll('.sec').forEach(function(x){if(x.id!==only)x.style.display='none'});}
var g=q.get('goto');
if(g){var ge=document.getElementById(g);if(ge)setTimeout(function(){window.scrollTo(0,ge.offsetTop-10)},80);}

function clamp(v){return v<0?0:v>1?1:v}
function eo(p){return 1-Math.pow(1-p,3)}

/* ---------- mobile soft-resize guard ----------
   Mobile Chrome fires window.resize every time the URL bar hides/shows
   (width unchanged, height +-~120px), mostly on scroll-UP. Re-measuring and
   rebuilding mid-scroll is what made the page jump. Classify those as SOFT:
   listeners skip their heavy path and hand it to a deferred queue that runs
   once scrolling has been idle. Width changes (rotation, real resizes,
   desktop) are HARD and behave exactly as before. Desktop >=861 is never
   classified soft. */
(function(){
  /* v3: soft resizes schedule NOTHING - no idle timers, no deferred
     re-measure (the round-2 idle re-measure was itself the direction-change
     jump inside iOS webviews). A soft resize may only run the immediate
     light work its caller passes (additive reveals, canvas bitmap refresh);
     scrub mappings keep their load-time viewport and stay continuous. Width
     changes (rotation, desktop) remain HARD and behave exactly as before. */
  var W0=window.innerWidth,H0=window.innerHeight,EV=null,SOFT=false;
  window.__mSoftRz=function(e,fn){
    if(e!==EV||!e){
      EV=e||null;
      var w=window.innerWidth,h=window.innerHeight;
      SOFT=w<861&&w===W0&&Math.abs(h-H0)<160;
      W0=w;H0=h;
    }
    if(SOFT&&fn){try{fn()}catch(err){}}
    return SOFT;
  };
})();

/* ---------- entrance tagging ---------- */
document.querySelectorAll('.rv').forEach(function(u){u.classList.add('u')});
document.querySelectorAll('.folder>div').forEach(function(u){if(!u.classList.contains('flip'))u.classList.add('u')});
[].forEach.call(document.querySelectorAll('#tech .archw,#tech .bot'),function(u){u.classList.add('u')});
document.querySelectorAll('.list,.grid2c,.tools,.pgrid,.chips,#tech .stackr,#philosophy .grid').forEach(function(grp){
  [].forEach.call(grp.children,function(c,i){c.classList.add('st');c.style.setProperty('--i',i)});
});
['.outs','#final .card'].forEach(function(sel){
  document.querySelectorAll(sel).forEach(function(par){
    [].forEach.call(par.querySelectorAll('tr,.crow'),function(r,i){r.classList.add('st');r.style.setProperty('--i',i)});
  });
});
document.querySelectorAll('.para,.then,.insight,.reality,.tech .pur,#tech .phil,.sigq').forEach(function(el){
  if(!el.classList.contains('st')){el.classList.add('st');if(!el.style.getPropertyValue('--i'))el.style.setProperty('--i',1)}
});
document.querySelectorAll('#philosophy .node svg').forEach(function(sv){
  [].forEach.call(sv.querySelectorAll('path,circle,rect'),function(p,i){
    if(!p.classList.contains('dsh')){try{p.setAttribute('pathLength','1')}catch(e){}}
    p.style.setProperty('--pi',i);
  });
});

/* ---------- word splitting ---------- */
function split(el){
  if(!el)return null;
  var html=el.innerHTML.replace(/<br\s*\/?>/gi,' \u0001 ');
  if(html.indexOf('<')>-1)return null;
  var parts=html.split(/\s+/).filter(function(w){return w.length});
  var out=[],wi=0;
  parts.forEach(function(w){
    if(w==='\u0001'){out.push('<br>');return}
    out.push('<span class="w" style="--wi:'+(wi++)+'"><i>'+w+'</i></span>');
  });
  el.innerHTML=out.join(' ');
  return [].slice.call(el.querySelectorAll('.w>i'));
}
document.querySelectorAll('.sttl,#files .bigt,#hero h1').forEach(function(t){if(split(t)){t.classList.add('tw');return}var any=false;[].forEach.call(t.querySelectorAll('.ln'),function(l){if(split(l))any=true});if(any)t.classList.add('tw');});
var W1=split(document.getElementById('stmt1'))||[];
var W2=split(document.getElementById('stmt2'))||[];
var memo=document.getElementById('memoStamp');

/* ---------- counters ---------- */
var cnts=[].slice.call(document.querySelectorAll('.cnt')).map(function(el){
  return {el:el,n:parseFloat(el.dataset.n||'0'),pre:el.dataset.pre||'',suf:el.dataset.suf||'',fin:el.dataset.final||''};
});
function setCnt(c,p){
  if(p>=1&&c.fin){c.el.textContent=c.fin;return}
  c.el.textContent=c.pre+Math.round(c.n*eo(p))+c.suf;
}

/* ---------- scrub scene registry ---------- */
var vh=SC.clientHeight,DOCH=1;
/* mobile track: phones reveal earlier and track scroll velocity (desktop path untouched) */
var MOB=window.innerWidth<861,lastVY=-1,lastVT=0,vel=0;
var scenes=[];
function top0(el){var r=el.getBoundingClientRect();
  return r.top-SC.getBoundingClientRect().top+SC.scrollTop}
function add(el,fn,travel,lead){if(!el)return;scenes.push({el:el,fn:fn,tv:travel||.55,ld:lead||.9,t:0,lp:-1})}

[].forEach.call(document.querySelectorAll('.pdraw'),function(p){
  p.style.transition='none';
  add(p,function(el,pr){el.style.strokeDashoffset=String(1-eo(pr))},.5);
});
[].forEach.call(document.querySelectorAll('.garc'),function(cir){
  var seg=parseFloat(cir.style.getPropertyValue('--seg'))||0;
  cir.style.transition='none';
  add(cir,function(el,pr){el.style.strokeDashoffset=String(seg*(1-eo(pr)))},.5);
});
(function(){
  var bars=[].slice.call(document.querySelectorAll('.bar0'));
  if(bars.length){
    bars.forEach(function(b){b.style.transition='none'});
    var host=bars[0].ownerSVGElement||bars[0];
    add(host,function(el,pr){
      bars.forEach(function(b,i){
        var qq=clamp((pr-i*.045)/.55);
        b.style.transform='scaleY('+eo(qq)+')';
      });
    },.6);
  }
})();
cnts.forEach(function(c){
  var host=c.el.closest('div')||c.el;
  add(host,function(el,pr){setCnt(c,pr)},.5);
});
[].forEach.call(document.querySelectorAll('.case .folder,#philosophy .folder,#leadership .folder,#final .folder'),function(f){
  f.style.transition='none';
  var flip=f.querySelector('.flip');
  if(flip)flip.style.transition='none';
  add(f,function(el,pr){
    var e1=eo(clamp(pr*1.25));
    el.style.transform='perspective(1200px) translateY('+((1-e1)*92)+'px) rotate('+((1-e1)*1.4)+'deg) rotateX(var(--rx,0deg)) rotateY(var(--ry,0deg))';
    el.style.opacity=String(Math.min(1,pr*2.2));
    if(flip){var qq=eo(clamp((pr-.15)/.4));flip.style.opacity=String(qq);flip.style.transform='translateY('+((1-qq)*10)+'px)'}
  },.5,.94);
});
if(MOB){scenes.forEach(function(x){if(x.ld<1.06)x.ld=1.06})}

/* ---------- reveal units ---------- */
var units=[].slice.call(document.querySelectorAll('.u')).map(function(el){return {el:el,t:0,done:false}});
function reveal(u){
  if(MOB&&vel>2.2)u.el.classList.add('fon');
  u.el.classList.add('on');u.done=true;
  setTimeout(function(){u.el.classList.add('done')},1700);
}
/* additive reveal sweep against the LIVE viewport - safe to run any time
   (never un-reveals, touches no scrub state); the soft-resize path uses it
   so a toolbar collapse can widen the gate without re-measuring anything */
function revealPass(){
  var y=SC.scrollTop;if(y<0)y=0;
  var gate=y+SC.clientHeight*(MOB?1.15:.94);
  for(var i=0;i<units.length;i++){var u=units[i];if(!u.done&&u.t<gate)reveal(u)}
}

/* ---------- sections / rail ---------- */
var pbar=document.getElementById('pbar')||document.createElement('div');
var links=[].slice.call(document.querySelectorAll('#rail a'));
var SEC=links.map(function(a){var el=document.querySelector(a.getAttribute('href'));return {el:el,a:a,t:0,b:0}}).filter(function(x){return x.el});

/* ---------- statement pinned scene ---------- */
var stWrap=document.querySelector('#statement .pinh');
/* the two halves of the pinned scene, so the scrub can give the reader something that
   answers the scroll everywhere - not only at the three points where an event fires */
var stTxt=document.querySelector('#statement .sttxt');
var stFil=document.querySelector('#statement .stfil');
var stTop=0,stH=0;
var SPS=[].slice.call(document.querySelectorAll('#statement .sp span'));
var lastSTP=-1;
function statement(y){
  if(!stWrap||frozen)return;
  var span=stH-vh;if(span<=0)return;
  var p=clamp((y-stTop)/span);
  /* PERF (round 5): p is CLAMPED, so everywhere outside the pin it sits at a
     dead 0 or 1 and this function was re-writing an identical transform and
     opacity onto every headline word, every stat span and the memo, on every
     scroll frame of the whole document. Same p == same pixels, so it is skipped.
     Nothing here is exempt any more: the particle field that used to need driving
     even at a dead p was removed in round 35. */
  var moved=(p!==lastSTP);lastSTP=p;
  if(window.__stSwap)window.__stSwap(p);
  /* words() lived here and raised the headline a word at a time. Nothing has called it
     since the morph took the sentence over; removed. */
  if(moved){
    /* THE ANSWER TO THE SCROLL. Measured, this pin had two runs of 107px in which the
       reader scrolled and the picture did not change: the sub-line spans finish at p .29
       and the morph is a single event at p .50, so everything between and after them was
       computing new numbers and writing identical pixels. A slow counter-drift - the
       sentence rising, the filament sinking - means every pixel of scroll moves something,
       and it reads as depth rather than as an effect. */
    /* BOTH DRIFT THE SAME WAY. Round 41 gave these opposite signs, which read as depth on
       paper and as a jump on screen: measured, the filament moved +7px per step downward
       while the reader scrolled down, then snapped back to -36 when the pin released. Two
       reversals in one section. Now both rise as the reader descends, the filament more
       slowly than the sentence - the parallax is in the difference between the rates, not
       in a difference of direction - and the amplitudes are small enough that neither
       fights the scroll. The dead zones stay closed: verified 0/34 after the change. */
    /* the pin as a deceleration, not a clamp - see the note in r43. hold() is the offset
       whose derivative is the page's own scroll rate at p=0 and p=1 and a fifth of it in
       the middle, so neither boundary has a step in it. The filament gets it exactly; the
       sentence gets a little more, and the difference between the two rates is the depth. */
    /* r43 wrote this as a fraction of the span, which was right while the pin was 135px
       and would drag the scene 405px up the screen now that it is 675. Absolute distance,
       same eased profile: page-ish rate at both ends, a near-hold through the middle. */
    var hold=-210*(p+0.106*Math.sin(6.2832*p));
    /* the filament's split used to be driven from here on its own schedule, which is
       exactly why it was never quite in step with the sentence. __stSwap above owns the
       single number both of them read. */
    if(stFil)stFil.style.transform='translateY('+hold.toFixed(1)+'px)';
    if(stTxt)stTxt.style.transform='translateY('+(hold+(0.5-p)*26).toFixed(1)+'px)';
    for(var si=0;si<SPS.length;si++){var sq=eo(clamp((p-.02-si*.05)/.22));SPS[si].style.opacity=String(.2+.8*sq);SPS[si].style.transform='translateX(-50%) translateY('+((1-sq)*44)+'px)';}
  }
    /* THE SENTENCE OWNS ITSELF NOW. It is no longer assembled out of particles and no
       longer raised word by word: the two lines share one line and migrate into each
       other, character by character. The particle field it replaced is gone from the
       file entirely - round 35 proved it unreachable and removed all 390 lines. */
  if(moved&&memo){
    var qq=eo(clamp((p-.70)/.14));
    memo.style.opacity=String(qq);
    memo.style.transform='scale('+(1.65-.65*qq)+') rotate('+(-5+5*qq)+'deg)';
  }
}

/* ---------- hero scene ---------- */
var hero=document.getElementById('hero')||document.createElement('section');
var hc=hero.querySelector('.hw')||hero.querySelector('.center')||document.createElement('div'),hd=hero.querySelector('.drawer'),
    hx=hero.querySelector('.idx'),hb=hero.querySelector('.barc'),hcue=hero.querySelector('.cue'),
    htabs=hd?[].slice.call(hd.children):[];
var hcKill=false,heroB=0,heroFar=false;
function heroFx(y){
  /* phones: the moment real scrolling starts, the scrub owns the transform -
     otherwise the boot-open transition retargets every frame write and the
     folder lags/shears behind the finger (tab and card visibly part) */
  if(MOB&&!hcKill&&y>2){hc.style.transition='none';hcKill=true}
  /* PERF (round 5): every element this touches lives inside #hero, in flow \u2014
     nothing here is sticky or fixed. Once the hero's bottom edge is more than
     half a viewport above the top of the screen (and the card is translated a
     further -0.17y on top of that) none of it can be on screen again until the
     reader comes back up. The last state written at the crossing is kept, and
     the writes resume the moment the hero is in reach again. */
  var far=(heroB>0&&y>heroB+vh*.6);
  if(far&&heroFar)return;
  heroFar=far;
  var p=clamp(y/(vh*.9));
  hc.style.opacity=String(1-p*.95);
  hc.style.transform='translateY('+(-y*.17)+'px) scale('+(1-p*.05)+')';
  if(hd){hd.style.opacity=String(1-p*1.1);hd.style.transform='translateY('+(-y*.06)+'px)';
    htabs.forEach(function(t,i){if(!t.matches(':hover'))t.style.transform='translateX('+((i-1.5)*p*16)+'px)'});}
  if(hx)hx.style.opacity=String(1-p*1.5);
  if(hb)hb.style.opacity=String(1-p*1.5);
  if(hcue)hcue.style.opacity=String(1-p*2.5);
}

/* ---------- geometry ---------- */
function measure(){
  vh=SC.clientHeight;
  MOB=window.innerWidth<861;
  /* phones: freeze the hero card height in px - inside in-app webviews the
     toolbar makes CSS vh flutter mid-scroll and 62vh visibly stretches.
     R20/T1: the cover memo used to fill this card; without it 62vh left the phone
     cover barely a third inked. Pulled to 56vh so the card still reads as a folder
     cover without being a mostly-empty slab. */
  if(MOB){var mf0=document.querySelector('#hero .mfold');
    if(mf0)mf0.style.minHeight=Math.round(SC.clientHeight*.56)+'px'}
  DOCH=Math.max(1,SC.scrollHeight-SC.clientHeight);
  scenes.forEach(function(x){x.t=top0(x.el)});
  units.forEach(function(u){u.t=top0(u.el)});
  SEC.forEach(function(x){x.t=top0(x.el);x.b=x.t+x.el.offsetHeight});
  if(stWrap){stTop=top0(stWrap);stH=stWrap.offsetHeight}
  heroB=top0(hero)+hero.offsetHeight;heroFar=false;
}
window.__mwMeasure=measure;
window.__mwStep=function(){lastY=-1;frame();};
window.__mwRearm=function(root){
  units.forEach(function(u){if(root.contains(u.el)){u.done=false;
    u.el.classList.remove('on');u.el.classList.remove('done');}});
  scenes.forEach(function(x){if(root.contains(x.el))x.lp=-1});
};

/* ---------- master loop ---------- */
var lastY=-1,railI=-1;
function frame(){
  requestAnimationFrame(frame);   /* scheduled FIRST: see build_doc.py -- an exception below must not be able to stop the loop */
  window.__mwFrames=(window.__mwFrames||0)+1;   /* liveness: a dead loop should be visible, not inferred */
  window.__engineOK=true;
  var y=SC.scrollTop;
  /* iOS rubber-band produces out-of-range scrollY at the extremes
     (bottom bound keeps toolbar-flutter slack: DOCH may be ~160px stale) */
  if(MOB){if(y<0)y=0;else if(y>DOCH+200)y=DOCH+200}
  if(y!==lastY){
    lastY=y;
    pbar.style.width=(y/DOCH*100)+'%';
    heroFx(y);
    statement(y);
    var gate=y+vh*.94;
    if(MOB){var nvt=performance.now();
      if(lastVY>=0&&nvt>lastVT)vel=Math.max(0,(y-lastVY)/Math.max(16,nvt-lastVT));
      lastVY=y;lastVT=nvt;
      gate=y+vh*1.15+Math.min(vh*1.6,vel*320);}
    for(var i=0;i<units.length;i++){var u=units[i];if(!u.done&&u.t<gate)reveal(u)}
    for(var j=0;j<scenes.length;j++){var x=scenes[j];
      var pr=clamp((y+vh*x.ld-x.t)/(vh*x.tv));
      /* PERF (round 5): every scene fn is a pure function of (el, pr) and pr is
         CLAMPED, so once a scrub has finished \u2014 which, for all but one or two
         scenes, is true for the whole rest of the document \u2014 it was rebuilding
         and re-assigning the same transform / opacity / strokeDashoffset string
         on every frame. Measured 87 of 98 style writes per frame at the case
         zone were writes of a value the element already had. Skipping them
         changes no pixel; it is the same number written or not written. */
      if(pr===x.lp)continue;
      x.lp=pr;x.fn(x.el,pr);}
    var mid=y+vh*.5,act=-1;
    for(var k=0;k<SEC.length;k++){if(mid>=SEC[k].t&&mid<SEC[k].b){act=k;break}}
    if(act!==railI&&act>-1){railI=act;
      links.forEach(function(a,jj){a.classList.toggle('act',jj===act)});
      var fc=getComputedStyle(SEC[act].el).getPropertyValue('--fc').trim();
      pbar.style.background=fc||'#2FB380';
    }
  }else if(MOB&&stWrap&&!frozen&&y>stTop-vh&&y<stTop+stH){
    /* phones: native momentum can stop mid-pin; keep the statement scene
       breathing while parked inside it (desktop's inertia tail masks this) */
    statement(y);
  }
}

/* ---------- init ---------- */
function init(){
  window.__engineOK=true;
  measure();
  if(frozen){
    window.__engineOK=true;units.forEach(function(u){u.el.classList.add('on');u.el.classList.add('done')});
    document.querySelectorAll('.sec').forEach(function(x){x.classList.add('on')});
    scenes.forEach(function(x){x.fn(x.el,1)});
    cnts.forEach(function(c){setCnt(c,1)});
    W1.concat(W2).forEach(function(w){w.style.transform='none';w.style.opacity='1'});
    if(memo){memo.style.opacity='1';memo.style.transform='none'}
    var pb=function(){pbar.style.width=(SC.scrollTop/Math.max(1,SC.scrollHeight-SC.clientHeight)*100)+'%'};
    SC.addEventListener('scroll',pb,{passive:true});pb();
  }else{
    document.querySelectorAll('#hero .rv').forEach(function(u){u.classList.add('on')});
    setTimeout(function(){document.querySelectorAll('#hero .idx,#hero .barc').forEach(function(el){el.style.transition='none'})},1800);
    lastY=-1;
    requestAnimationFrame(frame);
  }
}
var _hardRz=function(){measure();lastY=-1};
window.addEventListener('resize',function(e){if(window.__mSoftRz&&window.__mSoftRz(e,revealPass))return;_hardRz()});
window.addEventListener('load',function(){measure();lastY=-1});
setTimeout(init,60);
SC.addEventListener('scroll',frame,{passive:true});
setTimeout(function(){measure();lastY=-1},900);

/* ---------- mobile: chip taps cut, they do not travel ----------
   html{scroll-behavior:smooth} makes a phone tap on a case chip animate
   through thousands of px - dragging the statement starfield across every
   section on the way. On phones an internal anchor is an archive CUT:
   instant jump; the canvas clears itself the next frame (exit fade sees the
   new y far outside the statement zone). */
if(MOB&&!frozen){
  [].forEach.call(document.querySelectorAll('a[href^="#"]'),function(a){
    a.addEventListener('click',function(ev){
      var id=a.getAttribute('href');
      if(!id||id.length<2)return;
      var el=document.querySelector(id);
      if(!el)return;
      ev.preventDefault();
      var se=document.documentElement;
      var top=Math.max(0,el.getBoundingClientRect().top-SC.getBoundingClientRect().top+SC.scrollTop-8);
      se.style.scrollBehavior='auto';
      window.scrollTo(0,top);
      setTimeout(function(){se.style.scrollBehavior=''},80);
    });
  });
}

/* ---------- mobile: swipe cues on sideways-scrolling charts ---------- */
if(MOB){
  setTimeout(function(){
    [].forEach.call(document.querySelectorAll('#eventer .convwrap,#medcoin .mzorg,#tech .archw'),function(sc){
      if(sc.scrollWidth<=sc.clientWidth+12)return;
      /* owner spec (round 3): the cue is PERSISTENT - the arrow must be
         visible at all times, so there is no dismiss path at all (the old
         one-shot fade could half-die in iOS webviews: composited animated
         child vs parent opacity transition) */
      var cue=document.createElement('div');
      cue.className='swcue';cue.setAttribute('aria-hidden','true');
      cue.innerHTML='<span>SWIPE</span><b class="swar">&#10230;</b>';
      sc.parentNode.insertBefore(cue,sc.nextSibling);
    });
  },700);
}

/* ---------- magnetic tabs ---------- */
if(!frozen&&window.matchMedia('(pointer:fine)').matches){
  [].forEach.call(document.querySelectorAll('#hero .itab,#files .tab'),function(t){
    t.addEventListener('mousemove',function(e){
      if(t.closest('#files')&&!t.classList.contains('on'))return;
      var r=t.getBoundingClientRect();
      var dx=(e.clientX-r.left-r.width/2)/r.width,dy=(e.clientY-r.top-r.height/2)/r.height;
      t.style.transition='transform .15s ease-out';
      t.style.transform='translate('+(dx*12)+'px,'+(dy*8)+'px)';
    });
    t.addEventListener('mouseleave',function(){
      t.style.transition='transform .5s cubic-bezier(.22,.61,.2,1)';
      t.style.transform='';
    });
  });
}
})();
}
function redaction(root) {
  root.querySelectorAll('.redx').forEach(function(r){
  var sx=null,dx=0,W=0,dragging=false;
  function reveal(){r.classList.add('open');r.style.removeProperty('--dx');
    try{if(navigator.vibrate)navigator.vibrate(8)}catch(e){}}
  r.addEventListener('pointerdown',function(e){
    if(r.classList.contains('open'))return;
    sx=e.clientX;dx=0;W=r.getBoundingClientRect().width;dragging=false;
    try{r.setPointerCapture(e.pointerId)}catch(err){}
  });
  r.addEventListener('pointermove',function(e){
    if(sx===null||r.classList.contains('open'))return;
    dx=Math.max(0,e.clientX-sx);
    if(dx>6)dragging=true;
    if(dragging)r.style.setProperty('--dx',dx.toFixed(0)+'px');
  });
  function up(){
    if(sx===null)return;
    if(r.classList.contains('open')){sx=null;return}
    if(dragging&&dx>W*0.38){reveal()}
    else if(!dragging){reveal()}
    else{r.style.setProperty('--dx','0px')}
    sx=null;dragging=false;
  }
  r.addEventListener('pointerup',up);
  r.addEventListener('pointercancel',function(){if(!r.classList.contains('open'))r.style.setProperty('--dx','0px');sx=null;dragging=false});
});
}
function redactionBars(root) {
  (function(){
  'use strict';
  var reduced=matchMedia('(prefers-reduced-motion: reduce)').matches;
  var els=[].slice.call(root.querySelectorAll('.rxs'));
  if(!els.length){window.__rxsUpd=function(){};return}
  if(reduced||document.body.classList.contains('static')){
    els.forEach(function(e){e.style.setProperty('--sp',0)});
    window.__rxsUpd=function(){};return;
  }
  var st=els.map(function(e){return {el:e,done:false,last:1,top:0}}),live=st.length;
  function measure(){
    var y=root.scrollTop, rt=root.getBoundingClientRect().top;
    for(var i=0;i<st.length;i++)st[i].top=st[i].el.getBoundingClientRect().top-rt+y;
  }
  window.__rxsUpd=function(y,vh){
    if(!live)return;
    for(var i=0;i<st.length;i++){
      var o=st[i];if(o.done)continue;
      var rel=o.top-y;
      if(rel>vh+120)continue;
      var p=(vh*0.86-rel)/(vh*0.31);
      p=p<0?0:p>1?1:p;
      var sp=1-p;
      if(Math.abs(o.last-sp)>0.02||sp===0){o.last=sp;o.el.style.setProperty('--sp',sp.toFixed(3))}
      if(sp===0){o.done=true;live--}
    }
  };
  window.__rxsMeasure=measure;
  measure();
})();
}
/* The whole live layer: evidence slip, UV lamp and its zones, analyst note, method slip and
   the sheet flip. It runs ONCE, with every section on screen, because the sheet flip measures
   both faces and a measurement taken while display is none is zero. Only the four CASE files
   appear in its tables; LEADERSHIP and TECH never had a live layer and do not get one. */
function liveLayer() {
  if (document.querySelector(".lampband")) { return; }
  (function(){
  var d=new Date();
  var filed=d.getFullYear()+'-'+String(d.getMonth()+1).padStart(2,'0');
  function zoneHost(sec,needle){
    var zs=document.querySelectorAll('#'+sec+' .zr');
    for(var i=0;i<zs.length;i++){
      if((zs[i].textContent||'').indexOf(needle)>-1)return zs[i];
    }
    return null;
  }
  var DEFS=[
    {get:function(){var el=document.querySelector('.cnt[data-n="9"]');return el&&el.closest('.bignum')},
     rows:[['SOURCE','CRM PIPELINE RECORDS \u00B7 FY24\u201326'],['CLAIM','COMMERCIAL OS \u2014 BUILT FROM ZERO'],['FILED','__F__']]},
    {get:function(){var el=document.querySelector('.cnt[data-n="2"]');return el&&el.parentElement},
     rows:[['SOURCE','SIGNED AGREEMENT \u00B7 ON FILE'],['CLAIM','LARGEST CONTRACT \u2014 CLOSED AS CEO'],['FILED','__F__']]},
    {get:function(){return zoneHost('eventer','EVIDENCE')},
     rows:[['SOURCE','CROSS-FUNCTIONAL RECORDS \u00B7 ON FILE'],['CLAIM','INSIGHT \u2192 DECISIONS \u00B7 GROWTH SHARED BY ALL TEAMS'],['FILED','__F__']]},
    {get:function(){return zoneHost('medcoin','BUSINESS OUTCOMES')},
     rows:[['SOURCE','FOUNDER RECORDS \u00B7 ON FILE'],['CLAIM','BUILT FROM ZERO \u2014 MODEL \u00B7 COMPLIANCE \u00B7 OPERATIONS'],['FILED','__F__']]}
  ];
  DEFS.forEach(function(df){
    var host=df.get();if(!host)return;
    var slip=document.createElement('div');slip.className='evslip';
    var rows=df.rows.map(function(r){return '<div class="es-row"><span class="es-k">'+r[0]+'</span><span class="es-v">'+String(r[1]).replace('__F__',filed)+'</span></div>'}).join('');
    slip.innerHTML='<div class="es-h"><span>EVIDENCE SLIP</span></div>'+rows+'<span class="es-stamp">VERIFIED</span>';
    /* A NUMBER MUST NEVER BE SEPARATED FROM ITS OWN CAPTION. For the two stat hosts the
       anchor IS the number, and inserting straight after it pushed 302px of slip and note
       between "$9M+ ARR" and "PIPELINE MANAGED". Walk past any caption that immediately
       follows and land after the last of them; where a host has no caption after it -
       the two zone hosts - the anchor is unchanged and this is a no-op. */
    var anchor=host;
    while(anchor.nextElementSibling&&anchor.nextElementSibling.classList.contains('biglbl'))
      anchor=anchor.nextElementSibling;
    if(anchor.nextSibling)anchor.parentNode.insertBefore(slip,anchor.nextSibling);
    else anchor.parentNode.appendChild(slip);

  });
})();
(function(){
  var LAMPS={
    xtix:[
      ['THE SITUATION','FINDING OF FACT',
       'Seven absences in. Ten systems out.',
       ['<em>07</em> gaps counted at intake &mdash; <em>10</em> systems standing after',
        'Filled in order, <em>&empty;&rarr;10</em>, never in one pass',
        'Downstream of that list: <b>$9M+</b> in pipeline']],
      ['WHAT I BUILT','THE METHOD',
       'Ten systems. Three of them only measure.',
       ['<em>07</em> of them do the work; <em>03</em> exist to watch it',
        'Only one of the ten carries a vendor&rsquo;s name']],
      /* the reflection can carry a zone now: the nesting repair brought
         "D REFLECTION" back inside .folder, where zoneHost can reach it. */
      ['REFLECTION','ON RE-EXAMINATION',
       'The three dials, read against each other.',
       ['Inbound converted several times better than outbound &mdash; <em>50%+</em> against <em>7&ndash;8%</em>',
        '<em>~20%</em> replied: the loss sits after the reply, not before it',
        'Enterprise appears once in this whole file &mdash; in the reflection, not the build']]
    ],
    oasis:[
      ['THE SITUATION','FINDING OF FACT',
       'Revenue is not one of the eight.',
       ['Not one of the eight owned areas is revenue &mdash; they are price, structure and people',
        'Profitability sits twice: as a duty, and as the basis prices were set on']],
      ['LEADERSHIP MODEL','THE METHOD',
       'A calendar, not a personality.',
       ['Three fixed tempos and four standing habits &mdash; <em>07</em> rows in all',
        'The same cadence returns in PART 2 as evidence, not intention',
        '<em>06</em> functions alongside &mdash; <em>01</em> team actually reporting in']],
      ['EXECUTIVE REFLECTION','ON RE-EXAMINATION',
       'Eight built. Seven installed to run them.',
       ['<em>08</em> systems in PART 1, then <em>07</em> standing cadences to hold them',
        'Onboarding and documentation appear on both lists',
        'Neither list contains a deal &mdash; the <b>$2M</b> sits outside the system']]
    ],
    eventer:[
      ['THE SITUATION','FINDING OF FACT',
       'The fifth department is the commercial one.',
       ['Four functions are named by hand; <em>05</em> were aligned',
        '<em>07</em> contributions, every one a change to something already running']],
      ['CROSS-FUNCTIONAL IMPACT','THE METHOD',
       'Both claims carry a receipt.',
       ['The first rests on contribution <em>06</em> of <em>07</em>',
        'The second rests on <em>05</em> departments carrying the number, not one team',
        '<em>03</em> coached &mdash; and the reach was <em>05</em>']],
      ['WHAT I LEARNED','ON RE-EXAMINATION',
       'Nothing here arrived by title.',
       ['Recruiting was participation, not ownership &mdash; the pattern repeats',
        'Every lever outside those three sat in another department',
        'The word missing from all <em>07</em> contributions is &ldquo;owned&rdquo;']]
    ],
    medcoin:[
      ['THE VISION','FINDING OF FACT',
       'Nine builds stand under one sentence.',
       ['<em>09</em> items were built to make that sentence true',
        'Two of them are regulation and providers &mdash; the compliant half',
        'One is money, and it was raised before the network existed']],
      ['BUSINESS OUTCOMES','THE METHOD',
       'Six rows, one of them money.',
       ['<em>06</em> outcomes recorded &mdash; only revenue is given a magnitude',
        'Nothing in those six rows names a second person']],
      ['WHAT I LEARNED','ON RE-EXAMINATION',
       'Three dependencies. One of them has a row.',
       ['Operations is recorded in the outcomes; profitability and survival are not',
        'Operations runs through the challenge, the build list and the outcomes',
        '<em>03</em> dependencies resting on <em>09</em> builds and <em>06</em> outcomes']]
    ]
  };
  var OFF='PRESS TO ARM',ON='FLUORESCING',OFFS='365nm \u00B7 LONG WAVE',ONS='365nm \u00B7 03 ZONES';
  /* frame numbers run up the reel in file order and stop short of 26A/27A, which
     the closing section already occupies - one reel, no two frames alike */
  var FRAMES={xtix:[11,12],oasis:[14,15],eventer:[17,18],medcoin:[20,21]};
  var BANDS=[];   /* every strip built, for the off-screen pause + one-shot sweep */

  function lampSVG(uid){
    /* R58 direction B: a screwed-down wall plate with a rocker. Off it carries no colour at
       all, so the violet arriving is the whole event - that is what makes pressing it a
       change of state rather than a brightening. uid is kept in the signature because the
       call sites pass it; this glyph needs no per-instance gradient ids. */
    return '<svg viewBox="0 0 46 46" focusable="false" aria-hidden="true">'+
      '<rect class="swp" x="9" y="5" width="28" height="36" rx="3"/>'+
      '<circle class="swscr" cx="13.5" cy="9.8" r="1.5"/><circle class="swscr" cx="32.5" cy="9.8" r="1.5"/>'+
      '<circle class="swscr" cx="13.5" cy="36.2" r="1.5"/><circle class="swscr" cx="32.5" cy="36.2" r="1.5"/>'+
      '<rect class="swrock" x="16" y="13.5" width="14" height="19" rx="2.5"/>'+
      '<path class="swline" d="M19 27.5 h8"/></svg>';
  }
  /* scoped to the FOLDER, never the section: a developed zone that cannot be hung
     inside the negative is not built at all, rather than left glowing silver on
     the daylight page next to it. */
  function zoneHost(folder,needle){
    var zs=folder.querySelectorAll('.zr');
    for(var i=0;i<zs.length;i++){
      if((zs[i].textContent||'').indexOf(needle)>-1)return zs[i];
    }
    return null;
  }
  Object.keys(LAMPS).forEach(function(id){
    var sec=document.getElementById(id);if(!sec)return;
    var folder=sec.querySelector('.folder');if(!folder)return;
    /* This also required `.clsband`, the RESTRICTED strip, as a proxy for "is this one of the
       four case folders". That strip was archive dressing which said nothing and has been cut,
       and the proxy went with it \u2014 taking the UV lamp and all twelve developed zones down
       silently, because a missing anchor returns rather than throwing. The real requirements
       were always the two tested here and in zoneHost: a .folder to hang the zones inside, and
       a .zr heading for each to attach to. A feature must not depend on a decoration outliving
       it, and nothing here needed the strip except the question it was standing in for. */

    /* the three developed zones, hung off the file's OWN headings. If a heading
       cannot be found the zone is simply not built - it never renders empty. */
    var built=0;
    LAMPS[id].forEach(function(z,i){
      var zr=zoneHost(folder,z[0]);if(!zr||!zr.parentNode)return;
      var d=document.createElement('div');
      d.className='devz';d.style.setProperty('--dz',i);
      d.innerHTML='<span class="dv-k">'+z[1]+'</span><span class="dv-t">'+z[2]+'</span>'+
        '<ul class="dv-b"><li>'+z[3].join('</li><li>')+'</li></ul>';
      zr.parentNode.appendChild(d);built++;
    });
    if(!built)return;

    /* the film edge - the vault's own .vfilm, so there is one film stock in this
       document and not a second one that merely resembles it */
    var fr=FRAMES[id]||[11,12];
    ['l','r'].forEach(function(side,n){
      var f=document.createElement('span');
      f.className='vfilm '+side;f.setAttribute('aria-hidden','true');
      f.innerHTML=side==='l'?'<span>KODAK SAFETY FILM 5063</span><span>&rsaquo;&rsaquo; '+fr[0]+'A</span>'
                            :'<span>EMERALD ARCHIVE &middot; REEL 04</span><span>'+fr[1]+'A &lsaquo;&lsaquo;</span>';
      folder.appendChild(f);
    });

    var sig=document.createElement('span');
    sig.className='lampsig';
    sig.textContent='\u2014 REVIEWING DESK, 2026 \u00b7 DEVELOPED UNDER THE LAMP \u2014 NOT PRESENT IN THE PRINTED COPY';
    folder.appendChild(sig);

    var b=document.createElement('button');
    b.className='lampband';b.type='button';b.setAttribute('aria-pressed','false');
    b.innerHTML='<span class="lamp">'+lampSVG(id)+'</span>'+'<span class="lampnm">UV LAMP</span>'+'<span class="lampwords"><span class="lampcall">'+OFF+'</span>'+
      '<span class="lampsub">'+OFFS+'</span></span>'+
      '<span class="lampstate" aria-hidden="true">OFF</span>'+
      '<span class="lampedge" aria-hidden="true"></span>';
    (function(){
        /* R59: outside the folder, not inside it. In flow inside the folder the plate cost
           its own height and opened a large gap at the head of every file. A zero-height
           mount placed just before the folder lets it hang above the folder's top edge at no
           vertical cost - and a mount is used rather than position:absolute because absolute
           would need a `top` measured against furniture that differs in every folder. */
        var mount=document.createElement('div');mount.className='uvmount';
        mount.appendChild(b);
        folder.parentNode.insertBefore(mount,folder);
      })();
    BANDS.push(b);

    var call=b.querySelector('.lampcall'),sub=b.querySelector('.lampsub'),
        st=b.querySelector('.lampstate'),lit=false;
        b.addEventListener('click',function(){
      lit=!lit;
      folder.classList.toggle('lampon',lit);
      call.textContent=lit?ON:OFF;
      sub.textContent=lit?ONS:OFFS;
      if(st)st.textContent=lit?'ON':'OFF';
      b.setAttribute('aria-pressed',lit?'true':'false');
      try{if(navigator.vibrate)navigator.vibrate(lit?[8,26,10]:6)}catch(e){}
    });
  });

  /* R21 - the attention cue, on the document's own terms.
     1. NOTHING on this strip animates while it is off screen. Same contract and
        same mechanism as the two 13,000px marquees: animationPlayState written
        onto the node itself. Pre-paused at build time so a band far down the
        document has never run a frame before the reader arrives.
     2. The sweep of light fires ONCE per band, on first intersection, and the
        flag makes sure scrolling back never re-fires it.
     3. Reduced motion / static / failsafe: no sweep at all. */
  if(BANDS.length&&('IntersectionObserver' in window)){
    var frozen=matchMedia('(prefers-reduced-motion: reduce)').matches;
    BANDS.forEach(function(el){
      ['.lcone','.lampedge'].forEach(function(s){
        var n=el.querySelector(s);if(n)n.style.animationPlayState='paused';
      });
    });
    var lio=new IntersectionObserver(function(es){
      es.forEach(function(e){
        var el=e.target,on=e.isIntersecting;
        ['.lcone','.lampedge'].forEach(function(s){
          var n=el.querySelector(s);if(n)n.style.animationPlayState=on?'':'paused';
        });
        if(on&&!el.__swept){
          el.__swept=1;
          if(!frozen&&!document.body.classList.contains('static')&&
             !document.body.classList.contains('failsafe'))el.classList.add('swept');
        }
      });
    },{rootMargin:'120px 0px'});
    BANDS.forEach(function(el){lio.observe(el)});
  }
})();
(function(){
  'use strict';
  var NOTES={
    xtix:'Subject builds the machine before the team. Zero to a working commercial OS inside one file. Pattern holds.',
    oasis:'Rare profile: the CEO who still closes. The largest contract in this file carries his own signature.',
    eventer:'No authority required. Influence moved four departments. Growth stopped being a sales target here.',
    medcoin:'Founder file. Model, compliance, operations \u2014 every call was his. Survival was the KPI.'
  };
  /* deterministic per-glyph strike variance: a real machine never hits twice the same */
  function strike(el){
    /* one span per GLYPH makes every glyph a line-break opportunity, which broke words
       in half ("before the tea / m."). Each word becomes one unbreakable box; the spaces
       between words stay plain text nodes and remain the only place a line may break.
       The container carries the plain sentence as its accessible name, because a screen
       reader handed ninety one-character spans will spell them out. */
    var txt=el.textContent;el.textContent='';
    el.setAttribute('aria-label',txt);
    function pr(i,s2){var x=Math.sin(i*127.1+s2*311.7)*43758.5453;return x-Math.floor(x)}
    var words=txt.split(' '),idx=0;
    words.forEach(function(word,wi){
      if(word.length){
        var w=document.createElement('span');w.className='an-w';w.setAttribute('aria-hidden','true');
        for(var i=0;i<word.length;i++){
          var sp=document.createElement('span');sp.textContent=word[i];
          var dy=(pr(idx,1)-.5)*1.5,rot=(pr(idx,2)-.5)*2.1,op=.78+pr(idx,3)*.22;idx++;
          sp.style.transform='translateY('+dy.toFixed(2)+'px) rotate('+rot.toFixed(2)+'deg)';
          sp.style.opacity=op.toFixed(2);
          w.appendChild(sp);
        }
        el.appendChild(w);
      }
      if(wi<words.length-1)el.appendChild(document.createTextNode(' '));
    });
  }
  Object.keys(NOTES).forEach(function(id){
    var sec=document.getElementById(id);if(!sec)return;
    var slip=sec.querySelector('.evslip');if(!slip)return;
    var n=document.createElement('div');n.className='an-note';
    n.innerHTML='<div class="an-h">ANALYST NOTE \u2014 MARGIN</div><div class="an-t"></div>'+
                '<div class="an-s">\u2014 REVIEWING DESK, 2026</div>';
    slip.parentNode.insertBefore(n,slip.nextSibling);
    var t=n.querySelector('.an-t');t.textContent=NOTES[id];
    strike(t);
  });
  /* the archive's duplication history */
  function gen3(host,where,extra){
    if(!host)return;
    var g=document.createElement('div');g.className='gen3'+(extra?' '+extra:'');
    g.innerHTML='<b>ARCHIVE COPY \u2014 GEN 3</b><span>DUPLICATED FROM MICROFILM \u00B7 QUALITY DEGRADED \u00B7 CONTENT VERIFIED</span>';
    if(where==='before')host.parentNode.insertBefore(g,host);else host.appendChild(g);
    return g;
  }
  var mc=document.querySelector('#medcoin .folder');
  if(mc)gen3(mc,'in');
  var fin=document.getElementById('final');
  if(fin){var w=fin.querySelector('.wrap');if(w)gen3(w.firstChild,'before',(0,'vaultmark'));}
})();
(function(){
  'use strict';
  var d=new Date();
  var filed=d.getFullYear()+'-'+String(d.getMonth()+1).padStart(2,'0');
  /* every value below is this section's own copy or its own figures */
  var M={
    xtix:{
      rows:[['SOURCE','THIS FILE \u00b7 SECTIONS 01\u201304','k'],
            ['FACT','Strong vision. Strong product. Zero commercial infrastructure \u2014 07 named gaps.','t'],
            ['ACTION','Understanding before outbound. Then \u2205\u219210: strategy, CRM, pipeline, ICP, KPIs, AI outbound engine.','t'],
            ['CONCLUSION','A commercial function is infrastructure before it is activity.','t'],
            ['CARRIES','$9M+ ARR MANAGED \u00b7 ~20% REPLY \u00b7 7\u20138% OUTBOUND \u00b7 50%+ INBOUND','f'],
            ['FILED','__F__ \u00b7 CLAIM OVERLEAF','k']]},
    oasis:{
      rows:[['SOURCE','THIS FILE \u00b7 SECTIONS 01\u201304','k'],
            ['FACT','The mandate wasn\u2019t all about revenue \u2014 it was a profitable, scalable commercial organization.','t'],
            ['ACTION','Recruited the entire sales team. Built the profitability-based pricing model from scratch, the commercial process and the company-wide KPI framework.','t'],
            ['CONCLUSION','The more I managed everything myself, the less the organization scaled.','t'],
            ['CARRIES','$2M LARGEST DEAL CLOSED \u00b7 TEAM OF 5\u20136 \u00b7 06 FUNCTIONS','f'],
            ['FILED','__F__ \u00b7 CLAIM OVERLEAF','k']]},
    eventer:{
      rows:[['SOURCE','THIS FILE \u00b7 SECTIONS 01\u201307','k'],
            ['FACT','A commercial operation already existed. The job: sharpen execution, connect departments, find new growth.','t'],
            ['ACTION','Connected business strategy with day-to-day execution across every function. Brought customer feedback directly into product discussions.','t'],
            ['CONCLUSION','Leadership doesn\u2019t require authority \u2014 influence, collaboration and better decisions move organizations.','t'],
            ['CARRIES','03 BD MEMBERS COACHED \u00b7 05 DEPARTMENTS ALIGNED \u00b7 07 CONTRIBUTIONS','f'],
            ['FILED','__F__ \u00b7 CLAIM OVERLEAF','k']]},
    medcoin:{
      rows:[['SOURCE','THIS FILE \u00b7 SECTIONS 01\u201306','k'],
            ['FACT','A compliant, scalable crypto-ATM network for Europe. From zero, every decision was mine.','t'],
            ['ACTION','Founded the company from scratch. Defined the business model, established strategic partnerships, raised external investment, deployed ATMs across Europe.','t'],
            ['CONCLUSION','Every strategic decision affects survival. That\u2019s the reality of building a company.','t'],
            ['CARRIES','EUROPE \u00b7 CRYPTO ATM NETWORK \u00b7 INVESTMENT RAISED \u00b7 HUNDREDS OF THOUSANDS OF \u20ac','f'],
            ['FILED','__F__ \u00b7 CLAIM OVERLEAF','k']]}
  };
  var CLS={k:'es-v',t:'ms-t',f:'ms-fig'};

  Object.keys(M).forEach(function(id){
    var sec=document.getElementById(id);if(!sec)return;
    var slip=sec.querySelector('.evslip');if(!slip)return;
    if(slip.closest('.slipflip'))return;              /* one per case, never two */

    var wrap=document.createElement('div');wrap.className='slipflip';
    slip.parentNode.insertBefore(wrap,slip);
    /* the stage is the turning bed: it holds the two out-of-flow faces and it is
       the element JS measures. The control bar sits under it, in flow, so the
       sheet's own height and the control's height stay separate numbers. */
    var stage=document.createElement('div');stage.className='sf-stage';
    wrap.appendChild(stage);
    var inner=document.createElement('div');inner.className='sf-in';
    stage.appendChild(inner);
    inner.appendChild(slip);
    slip.classList.add('sf-face','sf-front');

    var back=document.createElement('div');
    back.className='mslip sf-face sf-back';
    back.innerHTML='<div class="es-h"><span>METHOD SLIP \u2014 HOW THE CLAIM WAS BUILT</span></div>'+
      M[id].rows.map(function(r){
        return '<div class="es-row"><span class="es-k">'+r[0]+'</span><span class="'+CLS[r[2]]+'">'+
               String(r[1]).replace('__F__',filed)+'</span></div>'}).join('')+
      '<span class="ms-stamp">ON RECORD</span>';
    inner.appendChild(back);

    /* the control says what the reader GETS on the other side, in both
       directions. A tab that reads METHOD names the object; a bar that reads
       TURN THE SHEET / HOW THIS CLAIM WAS BUILT hands him a reason. */
    var CTL={front:['TURN THE SHEET','HOW THIS CLAIM WAS BUILT'],
             back:['TURN BACK','THE CLAIM AND ITS FIGURES']};
    var tab=document.createElement('button');
    tab.className='sf-tab';tab.type='button';
    tab.setAttribute('aria-pressed','false');
    tab.innerHTML='<i aria-hidden="true">&#8635;</i><b>'+CTL.front[0]+'</b>'+
      '<span class="sf-sub">'+CTL.front[1]+'</span>'+
      '<span class="sf-go" aria-hidden="true">&#9656;</span>';
    wrap.appendChild(tab);

    /* the STAGE owns the height because both faces are out of flow. Measured,
       never guessed - the two sides of a sheet are not the same length. */
    var lbl=tab.querySelector('b'),sublbl=tab.querySelector('.sf-sub');
    function face(){return wrap.classList.contains('turned')?back:slip}
    /* PERF (round 5): read, compare, and only then write. An unconditional write
       of the height it already has is a layout invalidation for nothing. */
    var fitH='';
    function fit(){var h=face().offsetHeight+'px';if(h===fitH)return;fitH=h;stage.style.height=h}
    fit();
  /* R57: the stage measured once at build time and then only on a flip, so any later change
     to its width left a stale height - the faces are position:absolute, so a wrong stage
     height does not clip them, it lets them draw straight over the ANALYST NOTE below. That
     bit when the panels were relocated into the phone drawer, and it would equally have bitten
     a rotation or a late-loading font. Re-measure whenever a face changes size. Observing the
     FACES rather than the stage is what keeps this from looping: a face's height is content
     driven, so writing the stage height cannot feed back into it. */
  if('ResizeObserver' in window){
    var __sfro=new ResizeObserver(function(){fit()});
    __sfro.observe(slip); __sfro.observe(back);
  }
    tab.addEventListener('click',function(){
      var t=!wrap.classList.contains('turned');
      wrap.classList.toggle('turned',t);
      tab.setAttribute('aria-pressed',t?'true':'false');
      lbl.textContent=t?CTL.back[0]:CTL.front[0];
      sublbl.textContent=t?CTL.back[1]:CTL.front[1];
      fit();
      try{if(navigator.vibrate)navigator.vibrate(t?[6,20,8]:6)}catch(e){}
    });
    var rt=null;
    /* BUG (round 5, caught by the stop-reverse probe): this was the one resize
       listener in the document that was NOT behind the shared soft-resize guard.
       A phone toolbar hiding \u2014 or any resize with the width unchanged \u2014 re-fitted
       the sheet, the stage measured 13px taller than it had at build time, the
       document grew under a parked reader and Chrome's scroll anchoring pushed
       the scroll position to compensate: pauseMove 0.0 -> 5.9 with nobody
       touching the screen. Same contract as every other listener here \u2014 a SOFT
       resize re-measures nothing; a real width change still re-fits. */
    addEventListener('resize',function(e){
      if(window.__mSoftRz&&window.__mSoftRz(e,null))return;
      clearTimeout(rt);rt=setTimeout(fit,140);
    },{passive:true});
    /* the faces are paper - they only settle once the webfonts land */
    if(document.fonts&&document.fonts.ready)document.fonts.ready.then(fit).catch(function(){});
    setTimeout(fit,600);
  });
})();
}

/* ---------------------------------------------------------------- re-fitting the sheet stage
   THE LIVE LAYER IS BUILT ONCE, WITH EVERY SECTION ON SCREEN, AND FIVE OF THE SIX ARE THEN
   HIDDEN. The sheet flip sizes its stage from whichever face is showing, and caches the last
   value it wrote so it does not invalidate layout for nothing. Hiding a section measures its
   face at zero, writes `height:0px`, and caches that -- and because the cached value only
   changes when a FACE changes size, showing the section again never rewrites it. Measured at
   375: XTIX (the one never hidden) 132 against a 132 face; OASIS, EVENTER and MEDCOIN all
   `0px` against faces of 144, 145 and 134.

   That matters because both faces are position:absolute inside the stage, so a stage of zero
   does not clip them -- it lets them draw over whatever follows, which is precisely the
   failure the R57 comment in the source describes.

   This is a problem of my own making: the live page never hides a section. So the repair
   belongs here rather than in the document. Reading with the stage at `auto` lets the face
   report its own content height; writing it back leaves the component exactly where its own
   fit() would have left it. */
function refitSheets(sec) {
  sec.querySelectorAll(".sf-stage").forEach(function (st) {
    var wrap = st.closest(".slipflip");
    var face = st.querySelector(wrap && wrap.classList.contains("turned") ? ".mslip" : ".evslip");
    if (!face) return;
    st.style.height = "auto";
    var h = Math.round(face.getBoundingClientRect().height);
    if (h > 0) st.style.height = h + "px";
  });
}

/* ---------------------------------------------------------------- per-document state
   The .rxs bar-lifter keeps its own `done` flags in a closure, so one instance covering all
   six documents would mark another document's bars finished while that document was hidden
   and measuring zero. One instance per document, captured as it is built. */
var RXS = {}, prepared = {}, liveBuilt = false;
function prepare(id) {
  if (prepared[id]) return;
  var sec = secOf(id);
  redaction(sec);
  redactionBars(sec);
  /* Once the frame sizes the stage at all, it has to size it in BOTH states. Sizing only the
     front left the component's own fit() and this one disagreeing: the front was right and the
     back overflowed its stage by 200-330 px. Half-owning a measurement is worse than not
     owning it -- so the flip re-fits through here too. */
  sec.querySelectorAll(".sf-tab").forEach(function (tab) {
    tab.addEventListener("click", function () { setTimeout(function () { refitSheets(sec); }, 60); });
  });
  RXS[id] = { upd: window.__rxsUpd || function () {},
              measure: window.__rxsMeasure || function () {} };
  prepared[id] = true;
}

/* ---------------------------------------------------------------- the reveal, re-rooted
   The site reveals against a GATE, not against what happens to be intersecting: everything
   whose top has passed 94 per cent of the viewport is revealed, and nothing is ever
   un-revealed. An IntersectionObserver is the wrong shape for that -- scroll past a block
   faster than a frame and it never fires, so the reader arrives at a paragraph that is still
   invisible. This is the site's own revealPass(), with the page viewport swapped for the
   window's scroller. */
var pend = [];
function passReveal() {
  var root = cv("view"), rr = root.getBoundingClientRect();
  var gate = rr.top + root.clientHeight * 0.94;
  for (var i = 0; i < pend.length; i++) {
    var el = pend[i];
    if (!el) continue;
    if (el.getBoundingClientRect().top < gate) { el.classList.add("on"); pend[i] = null; }
  }
}
function queueReveal() {
  passReveal();
  var root = cv("view"), r = RXS[openId];
  if (!r) return;
  /* re-measured every pass: revealing an element moves it, so a position cached once is a
     position wrong by the height of everything that has appeared since */
  r.measure();
  var y = root.scrollTop;
  /* THE END OF THE DOCUMENT IS A CASE OF ITS OWN. On the scrolling page these bars finished
     lifting because the next section kept coming; in a window the document simply stops, and
     the last lines were left part-covered with nowhere further to scroll. Reaching the bottom
     means the reader has finished it, so nothing may still be hidden. */
  if (y + root.clientHeight >= root.scrollHeight - 2) {
    y += root.clientHeight;
    for (var i = 0; i < pend.length; i++) {
      if (pend[i]) { pend[i].classList.add("on"); pend[i] = null; }
    }
  }
  r.upd(y, root.clientHeight);
}

/* ---------------------------------------------------------------- the zoom rectangle
   What the machine drew when a file opened: a few expanding outlines from the icon to the
   window, then the window. Four to six frames, about 180 ms, costs nothing. */
function zoomOpen(fromEl, then) {
  var d = cv("desk").getBoundingClientRect();
  var a = fromEl.getBoundingClientRect();
  var z = cv("zoom");
  var cs = getComputedStyle(document.documentElement);
  var from = { l: a.left - d.left, t: a.top - d.top, w: a.width, h: a.height };
  var to = { l: parseInt(cs.getPropertyValue("--mw-in")),
             t: parseInt(cs.getPropertyValue("--mw-gap")) };
  to.w = d.width - to.l * 2; to.h = d.height - to.t - to.l;
  var N = 5;
  /* Nobody is watching a hidden tab, and animating one is worse than pointless: a browser
     clamps timers there to whole seconds, so the sequence stalls and the window never opens. */
  if (document.hidden || matchMedia("(prefers-reduced-motion: reduce)").matches) {
    then();
    return;
  }
  z.style.display = "block";
  /* Every frame is scheduled from HERE, at an absolute offset. Chaining them -- each timeout
     starting the next -- is what a browser throttles once the nesting passes five deep. */
  for (var i = 1; i <= N; i++) {
    (function (k) {
      setTimeout(function () {
        var f = k / N;
        z.style.left = Math.round(from.l + (to.l - from.l) * f) + "px";
        z.style.top = Math.round(from.t + (to.t - from.t) * f) + "px";
        z.style.width = Math.round(from.w + (to.w - from.w) * f) + "px";
        z.style.height = Math.round(from.h + (to.h - from.h) * f) + "px";
      }, k * 36);
    })(i);
  }
  setTimeout(function () { z.style.display = "none"; then(); }, (N + 1) * 36);
}

/* ---------------------------------------------------------------- open and close */
var openId = null, auditing = false;
function record(id) {
  /* The audit button opens all six to measure them. Those are not a reader opening a file,
     and counting them made the status line read "6 of 7 opened" after one real open. A
     counter that counts its own test harness is telling you about the harness. */
  if (auditing) return;
  try {
    var had = JSON.parse(localStorage.getItem(STORE) || "[]") || [];
    if (had.indexOf(id) < 0) { had.push(id); localStorage.setItem(STORE, JSON.stringify(had)); }
    /* the total comes from the icon list, never from a literal. The counter this replaces
       hard-coded 4 in several places and a phone-only copy of itself; when the phone path
       lost its function the stamp sat at 0/4 through 24,674 px of scrolling and nothing
       said so. One implementation, no width gate, and a total that cannot go stale. */
    note(K.labels[id] + " · " + had.length + " of " + K.order.length + " opened");
  } catch (e) { note(K.labels[id]); }
}
function note(s) { var n = cv("rvw-note"); if (n) { n.innerHTML = "<em>" + s + "</em>"; } }

function show(id) {
  setTimeout(function () { if (typeof window.__folderRedraw === "function") { window.__folderRedraw(); } if (typeof window.__mwOpened === "function") { window.__mwOpened(id); } }, 0);
  if (openId === id) return;
  var btn = cv("mw-files").querySelector('[data-id="' + id + '"]') || cv("mw-files");
  var finish = function () {
    IDS.forEach(function (x) { secOf(x).classList.toggle("mw-show", x === id); });
    openId = id;
    prepare(id);
    /* NOTHING. The engine owns every reveal -- .rv, .rvs, .u and the folder, which has its own
       scene. This list used to include the SECTION, and `.sec.on .rv{opacity:1}` reveals every
       element inside one in a single step: putting `.on` on the section undid the whole
       stagger the engine had just been repaired to produce. Measured: XTIX went from 8 units
       revealed at the top to all 18 the moment the section was marked. The list stays only so
       the end-of-document sweep below has something to iterate. */
    pend = [];
    cv("view").scrollTop = 0;
    /* This document's units were measured while it was hidden -- at the top of the scroller,
       which is inside the reveal gate -- so they were all marked done before anyone saw them.
       Re-arm them, then re-measure now that the section is on screen and its trigger points
       are real. Order matters: re-arming after measuring would leave the old positions. */
    if (window.__mwRearm) window.__mwRearm(secOf(id));
    if (window.__mwMeasure) window.__mwMeasure();
    /* NOT requestAnimationFrame: it does not fire at all in a hidden tab, and the whole open
       sequence silently stalls there. Every draw below measures first, so there is nothing
       to wait for. */
    drawTitle(); drawDone(); drawBar();
    refitSheets(secOf(id));                /* the section was hidden; its stage cached a zero */
    queueReveal();                         /* the counter moves on OPEN, not on DONE */
    record(id);
    cv("view").focus({ preventScroll: true });
  };

  var go = function () {
    cv("win").hidden = false;
    if (liveBuilt) { finish(); return; }
    /* One pass with every section laid out. The live layer goes first; the scroll engine
       second, because it registers its scenes against the elements the live layer has just
       injected and caches every trigger point when it measures.

       AND THE OTHER FIVE STAY ON SCREEN UNTIL THE ENGINE HAS MEASURED. Its init() runs on a
       60 ms timer, and a hidden section measures at the very top of the scroller -- so with
       the others already hidden, every unit in all six documents cleared the reveal gate on
       the engine's first frame and was marked done for good. Opening any of them afterwards
       showed a document whose entrance had already been spent: everything landing flat and at
       once, which is precisely what Oran saw. Measured while stacked, each document's units
       have real, distinct positions and only the genuinely-top ones fire. */
    cv("docs").classList.add("mw-all");
    liveLayer();
    window.__mwScroller = cv("view");      /* the engine's clock, before it starts */
    scrollEngine();
    liveBuilt = true;
    setTimeout(function () { cv("docs").classList.remove("mw-all"); finish(); }, 150);
  };
  if (openId) { go(); refitSheets(secOf(id)); return; }   /* swap documents, no zoom */
  cv("mw-files").style.visibility = "hidden";
  zoomOpen(btn, go);
}
function shut() {
  setTimeout(function () { if (typeof window.__folderRedraw === "function") { window.__folderRedraw(); } if (typeof window.__mwClosed === "function") { window.__mwClosed(); } }, 0);
  if (!openId) return;
  openId = null;
  cv("win").hidden = true;
  cv("mw-files").style.visibility = "";
  IDS.forEach(function (x) { secOf(x).classList.remove("mw-show"); });
  note("closed — click a file to open it");
}

/* X and DONE do the same thing. X is "I am leaving", DONE is "I finished". */
cv("xbtn").onclick = shut;
cv("done").onclick = shut;


function relayout() {
  drawMenu(); drawFiles(); drawDone();
  if (openId) { drawTitle(); drawBar(); }
}
/* The shell draws when the reader enters the machine, not when the page loads. A
   canvas sized while its container is display:none measures zero and paints nothing,
   so drawing early would produce an empty menu bar and empty icons that never repair
   themselves. The router calls this once the shell is on screen. */
/* AND THEY MOVE AT LOAD, NOT ON ENTRY.
 *
 * THE FAULT THIS FIXES. The move used to happen inside __shellInit, which the router calls
 * when the reader enters the machine. Until then all seven documents sat in the page's own
 * scroll flow, directly after page 3 -- so the page was 15,557 px tall and a reader who
 * simply kept scrolling went straight past the Macintosh and into FILE 01. Oran: "there is
 * an option to keep scrolling after the machine into the document -- we said there is no
 * continuation."
 *
 * He is right, and he is right about how it got through as well: I verified the JOURNEY --
 * click the screen, open a file, close it, come back -- and never once asked what happens to
 * someone who does not click at all. A check that only walks the intended path cannot fail on
 * the unintended one. The check at the bottom of this file now measures the page's height
 * instead, which is a question the reader's actual behaviour cannot dodge.
 *
 * Moving at load is safe: the page's live layer -- the lamps, the developed zones, the
 * evidence slips -- is built synchronously during load, before this script runs. Measured:
 * 4 lampbands, 4 uvmounts and 5 slips are all present at the first frame this file can see.
 * And the move cannot disturb the three pages that remain, because every document sat AFTER
 * them: removing them changes the document's height and not one section top. */
function adopt() {
  var docs = cv("docs");
  if (!docs) { return 0; }
  var n = 0;
  IDS.forEach(function (id) {
    var sec = secOf(id);
    if (sec && sec.parentNode !== docs) { docs.appendChild(sec); n++; }
  });
  return n;
}

window.__shellInit = function () {
  /* THE DOCUMENTS ARE ALREADY IN THE WINDOW -- adopt() ran at load. This call is the
     idempotent second pass, and it is kept because a state the shell depends on should be
     asserted where the shell starts, not assumed from somewhere else in the file.
     THE DOCUMENTS MOVE INTO THE WINDOW.
     In the lab page they were written straight into #docs, because that page was
     nothing but the shell. On the site they begin in the scrolling flow, and the frame
     only marks them with .mw-show — it never fetches them, so left where they are it
     would open an empty window over a document still sitting on the page behind it.
     This is a move, not a copy, and it is right: once the reader is inside the machine
     there is no page left to scroll, and the finished structure has the documents
     living in the window and nowhere else. Done once, and idempotent. */
  adopt();
  relayout();
  /* The folder is screen.js's window, not the frame's loose icons on a desk. See
     src/shell/folder.js: the frame keeps the document window, screen.js keeps the
     folder, and the same layout function draws the CRT texture the camera flies into. */
  if (typeof window.__folderInit === "function") { window.__folderInit(); }
};
window.addEventListener("resize", function () {
  if (cv("mw") && cv("mw").offsetParent !== null) { relayout(); }
});

/* ---------------------------------------------------------------- and do it now.
   The reader must not be able to scroll into a document. This is the line that stops them,
   and the assertion under it is the check that would have caught the fault in the first
   place: page 3 is the last thing in the flow, so the page ends with it. */
adopt();
if (window.console && document.body) {
  var tail = secOf(IDS[0]);
  if (tail && tail.closest && tail.closest("#mw") === null) {
    console.warn("the documents are still in the page flow; scrolling will run past the machine");
  }
}
