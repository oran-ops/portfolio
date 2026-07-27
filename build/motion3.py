# -*- coding: utf-8 -*-
# MOTION V3 — scroll-scrubbed cinematic engine (replaces V2 reveal system)
import io, re
s=io.open("site.html",encoding="utf-8").read()

# ============ 1. STATEMENT -> pinned scene ============
new_stmt="""<section class="sec" id="statement">
  <div class="pinh"><div class="pin"><div class="in">
    <div class="memo" id="memoStamp">MEMO &middot; FROM THE ARCHIVE</div>
    <div class="l1" id="stmt1">Most companies don't need better salespeople.</div>
    <div class="l2" id="stmt2">They need better commercial decisions.</div>
  </div></div></div>
</section>"""
s=re.sub(r'<section class="sec" id="statement">.*?</section>', new_stmt, s, count=1, flags=re.S)

# blink on STATUS ACTIVE
s=s.replace('<span class="br2">ACTIVE</span>','<span class="br2 blink">ACTIVE</span>',1)

# ============ 2. CSS V3 ============
CSS="""
/* ===================== MOTION V3 ===================== */
.w{display:inline-block;overflow:hidden;vertical-align:top;padding-bottom:.1em;margin-bottom:-.1em}
.w>i{display:inline-block;font-style:inherit;transform:translateY(118%)}
.tw .w>i{transition:transform .85s var(--ease)}
.tw.on .w>i{transform:none;transition-delay:calc(var(--wi,0)*50ms + var(--i,0)*60ms)}
#statement{padding:0}
#statement .pinh{height:230vh}
#statement .pin{position:sticky;top:0;min-height:100svh;display:flex;align-items:center;justify-content:center;padding:0 24px}
#statement .in{width:100%}
#statement .w>i{transition:none;opacity:0}
#statement .memo{opacity:0}
.rv{transform:translateY(36px)}
.st{transform:translateY(26px)}
.u .zr{transform:translateX(-26px)}
.u.done .st{transition-delay:0s;transition-duration:.35s}
.u.done .st.lg:hover,.u.done .st.dash:hover,.u.done .st.mi:hover{transform:translateX(6px)}
.u.done .st.chip:hover{transform:translateY(-3px);border-color:var(--fc,var(--emb))}
.u.done .st.sc:hover{transform:translateY(-4px);border-color:var(--grid2)}
#final .crow{transition:transform .3s var(--ease)}
#final .card.u.done .crow:hover{transform:translateX(-4px)}
.case .folder,#philosophy .folder,#leadership .folder,#final .folder{opacity:0}
#hero .center,#hero .drawer,#statement .pin{will-change:transform,opacity}
.blink{animation:blnk 2.6s steps(1) infinite}
@keyframes blnk{0%,86%{opacity:1}87%,100%{opacity:.28}}
.tk{font-size:10px;animation-duration:26s}
.tk b{color:var(--ink)}
body.static .w>i,body.static .tw .w>i{transform:none!important;opacity:1!important}
body.static #statement .memo{opacity:1!important;transform:none!important}
body.static #statement .pinh{height:auto}
body.static #statement .pin{position:static;padding:150px 24px}
body.static .case .folder,body.static #philosophy .folder,body.static #leadership .folder,body.static #final .folder{opacity:1!important;transform:none!important}
body.static .folder .flip{opacity:1!important;transform:none!important}
@media (prefers-reduced-motion:reduce){
 .w>i{transform:none!important;opacity:1!important}
 #statement .memo{opacity:1!important;transform:none!important}
 #statement .pinh{height:auto}
 #statement .pin{position:static;padding:150px 24px}
 .case .folder,#philosophy .folder,#leadership .folder,#final .folder{opacity:1!important;transform:none!important}
 .folder .flip{opacity:1!important;transform:none!important}
 .blink{animation:none}
}
"""
s=s.replace("</style>",CSS+"</style>",1)

# ============ 3. ENGINE ============
i0=s.index("<script>"); i1=s.index("</script>")+len("</script>")
JS="""<script>
(function(){
"use strict";
var q=new URLSearchParams(location.search);
var reduced=window.matchMedia('(prefers-reduced-motion: reduce)').matches;
var isStatic=q.get('static')==='1';
if(isStatic)document.body.classList.add('static');
var frozen=isStatic||reduced;
var only=q.get('only');
if(only){document.querySelectorAll('.sec').forEach(function(x){if(x.id!==only)x.style.display='none'});}
var g=q.get('goto');
if(g){var ge=document.getElementById(g);if(ge)setTimeout(function(){window.scrollTo(0,ge.offsetTop-10)},80);}

function clamp(v){return v<0?0:v>1?1:v}
function eo(p){return 1-Math.pow(1-p,3)}

/* ---------- entrance tagging ---------- */
document.querySelectorAll('.rv').forEach(function(u){u.classList.add('u')});
document.querySelectorAll('.folder>div').forEach(function(u){if(!u.classList.contains('flip'))u.classList.add('u')});
[].forEach.call(document.querySelectorAll('#tech .stacks,#tech .bot'),function(u){u.classList.add('u')});
document.querySelectorAll('.list,.grid2c,.tools,.pgrid,.chips,#tech .stacks,#philosophy .grid').forEach(function(grp){
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
  var html=el.innerHTML.replace(/<br\\s*\\/?>/gi,'\\u0001');
  if(html.indexOf('<')>-1)return null;
  var parts=html.split(/\\s+/).filter(function(w){return w.length});
  var out=[],wi=0;
  parts.forEach(function(w){
    if(w==='\\u0001'){out.push('<br>');return}
    out.push('<span class="w" style="--wi:'+(wi++)+'"><i>'+w+'</i></span>');
  });
  el.innerHTML=out.join(' ');
  return [].slice.call(el.querySelectorAll('.w>i'));
}
document.querySelectorAll('.sttl,#files .bigt,#hero h1').forEach(function(t){if(split(t))t.classList.add('tw')});
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
var vh=window.innerHeight,DOCH=1;
var scenes=[];
function top0(el){var r=el.getBoundingClientRect();return r.top+window.pageYOffset}
function add(el,fn,travel,lead){if(!el)return;scenes.push({el:el,fn:fn,tv:travel||.55,ld:lead||.9,t:0})}

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
  var flip=f.querySelector('.flip');
  add(f,function(el,pr){
    var e1=eo(clamp(pr*1.25));
    el.style.transform='translateY('+((1-e1)*56)+'px)';
    el.style.opacity=String(Math.min(1,pr*2.2));
    if(flip){var qq=eo(clamp((pr-.15)/.4));flip.style.opacity=String(qq);flip.style.transform='translateY('+((1-qq)*10)+'px)'}
  },.5,.94);
});

/* ---------- reveal units ---------- */
var units=[].slice.call(document.querySelectorAll('.u')).map(function(el){return {el:el,t:0,done:false}});
function reveal(u){
  u.el.classList.add('on');u.done=true;
  setTimeout(function(){u.el.classList.add('done')},1700);
}

/* ---------- sections / rail ---------- */
var pbar=document.getElementById('pbar');
var links=[].slice.call(document.querySelectorAll('#rail a'));
var SEC=links.map(function(a){var el=document.querySelector(a.getAttribute('href'));return {el:el,a:a,t:0,b:0}}).filter(function(x){return x.el});

/* ---------- statement pinned scene ---------- */
var stWrap=document.querySelector('#statement .pinh');
var stTop=0,stH=0;
function statement(y){
  if(!stWrap||frozen)return;
  var span=stH-vh;if(span<=0)return;
  var p=clamp((y-stTop)/span);
  function words(list,start,dur){
    var n=list.length;if(!n)return;
    for(var i=0;i<n;i++){
      var st=start+(i/n)*dur*.8;
      var qq=eo(clamp((p-st)/(dur*.35)));
      list[i].style.transform='translateY('+((1-qq)*115)+'%)';
      list[i].style.opacity=String(qq);
    }
  }
  words(W1,.05,.30);
  words(W2,.40,.26);
  if(memo){
    var qq=eo(clamp((p-.70)/.14));
    memo.style.opacity=String(qq);
    memo.style.transform='scale('+(1.65-.65*qq)+') rotate('+(-5+5*qq)+'deg)';
  }
}

/* ---------- hero scene ---------- */
var hero=document.getElementById('hero');
var hc=hero.querySelector('.center'),hd=hero.querySelector('.drawer'),
    hx=hero.querySelector('.idx'),hb=hero.querySelector('.barc'),hcue=hero.querySelector('.cue'),
    htabs=hd?[].slice.call(hd.children):[];
function heroFx(y){
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
  vh=window.innerHeight;
  var h=document.documentElement;DOCH=Math.max(1,h.scrollHeight-h.clientHeight);
  scenes.forEach(function(x){x.t=top0(x.el)});
  units.forEach(function(u){u.t=top0(u.el)});
  SEC.forEach(function(x){x.t=top0(x.el);x.b=x.t+x.el.offsetHeight});
  if(stWrap){stTop=top0(stWrap);stH=stWrap.offsetHeight}
}

/* ---------- master loop ---------- */
var lastY=-1,railI=-1;
function frame(){
  var y=window.pageYOffset;
  if(y!==lastY){
    lastY=y;
    pbar.style.width=(y/DOCH*100)+'%';
    heroFx(y);
    statement(y);
    var gate=y+vh*.94;
    for(var i=0;i<units.length;i++){var u=units[i];if(!u.done&&u.t<gate)reveal(u)}
    for(var j=0;j<scenes.length;j++){var x=scenes[j];
      var pr=clamp((y+vh*x.ld-x.t)/(vh*x.tv));x.fn(x.el,pr);}
    var mid=y+vh*.5,act=-1;
    for(var k=0;k<SEC.length;k++){if(mid>=SEC[k].t&&mid<SEC[k].b){act=k;break}}
    if(act!==railI&&act>-1){railI=act;
      links.forEach(function(a,jj){a.classList.toggle('act',jj===act)});
      var fc=getComputedStyle(SEC[act].el).getPropertyValue('--fc').trim();
      pbar.style.background=fc||'#F4603E';
    }
  }
  requestAnimationFrame(frame);
}

/* ---------- init ---------- */
function init(){
  measure();
  if(frozen){
    units.forEach(function(u){u.el.classList.add('on');u.el.classList.add('done')});
    document.querySelectorAll('.sec').forEach(function(x){x.classList.add('on')});
    scenes.forEach(function(x){x.fn(x.el,1)});
    cnts.forEach(function(c){setCnt(c,1)});
    W1.concat(W2).forEach(function(w){w.style.transform='none';w.style.opacity='1'});
    if(memo){memo.style.opacity='1';memo.style.transform='none'}
    var pb=function(){var h=document.documentElement;pbar.style.width=(window.pageYOffset/Math.max(1,h.scrollHeight-h.clientHeight)*100)+'%'};
    window.addEventListener('scroll',pb,{passive:true});pb();
  }else{
    document.querySelectorAll('#hero .rv').forEach(function(u){u.classList.add('on')});
    lastY=-1;
    requestAnimationFrame(frame);
  }
}
window.addEventListener('resize',function(){measure();lastY=-1});
window.addEventListener('load',function(){measure();lastY=-1});
setTimeout(init,60);
setTimeout(function(){measure();lastY=-1},900);

/* ---------- magnetic tabs ---------- */
if(!frozen&&window.matchMedia('(pointer:fine)').matches){
  [].forEach.call(document.querySelectorAll('#hero .dtab,#files .tab'),function(t){
    t.addEventListener('mousemove',function(e){
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
</script>"""
s=s[:i0]+JS+s[i1:]

io.open("site.html","w",encoding="utf-8").write(s)
print("MOTION V3 applied:",len(s),"bytes")
