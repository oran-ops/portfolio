# -*- coding: utf-8 -*-
# LANDO LEAP: boot preloader, inertia smooth-scroll, stronger kinetic type, ghost numerals, folder physics
import io
p="site.html"; s=io.open(p,encoding="utf-8").read()

# ---------- 1. engine tweaks ----------
# heroFx targets .center (now .mfold has class center) — ok. drawer gone; guard exists.
# folder rise boost + settle rotation
s=s.replace("el.style.transform='perspective(1200px) translateY('+((1-e1)*56)+'px) rotateX(var(--rx,0deg)) rotateY(var(--ry,0deg))';",
"el.style.transform='perspective(1200px) translateY('+((1-e1)*92)+'px) rotate('+((1-e1)*1.4)+'deg) rotateX(var(--rx,0deg)) rotateY(var(--ry,0deg))';",1)
# magnetic targets: dtab -> itab
s=s.replace("'#hero .dtab,#files .tab'","'#hero .itab,#files .tab'")
# arch feedback curve clearance (site)
s=s.replace('C %.1f 106'%0 if False else 'C ','C ')  # no-op guard

# ---------- 2. CSS ----------
CSS="""
/* ===== LANDO LAYER ===== */
::selection{background:var(--emb);color:#0C0D10}
::-webkit-scrollbar{width:9px}
::-webkit-scrollbar-track{background:#0C0D10}
::-webkit-scrollbar-thumb{background:#2E3036;border-radius:5px;border:2px solid #0C0D10}
::-webkit-scrollbar-thumb:hover{background:var(--emb)}
#boot{position:fixed;inset:0;z-index:100000;background:#0C0D10;display:flex;flex-direction:column;
align-items:center;justify-content:center;transition:transform .75s cubic-bezier(.7,0,.2,1)}
#boot.done{transform:translateY(-101%)}
#boot .bl{font-family:'JetBrains Mono',monospace;font-size:10px;letter-spacing:.3em;color:var(--dim);margin-bottom:10px}
#boot .bl b{color:var(--emb)}
#boot .cnt2{font-weight:900;font-size:clamp(70px,12vw,140px);letter-spacing:-.03em;color:var(--ink);line-height:1;font-variant-numeric:tabular-nums}
#boot .bbar{width:min(420px,70vw);height:2px;background:#2E3036;margin-top:26px;position:relative;overflow:hidden}
#boot .bbar i{position:absolute;left:0;top:0;bottom:0;width:0;background:var(--emb)}
#boot .bfile{margin-top:18px;font-family:'JetBrains Mono',monospace;font-size:9px;letter-spacing:.24em;color:var(--mut)}
#heromq .row{-webkit-text-stroke:1px rgba(242,241,237,.10)}
#heromq .r1{font-size:190px}
#heromq .r2{font-size:190px}
.bigmq{padding:40px 0;transform:rotate(-1.6deg);margin:20px -40px;width:calc(100% + 80px)}
.bigmq .in2{font-size:106px;animation-duration:38s}
.secnum{position:absolute;top:34px;right:20px;z-index:0;pointer-events:none;font-weight:900;font-size:210px;line-height:1;
letter-spacing:-.04em;color:transparent;-webkit-text-stroke:1px rgba(242,241,237,.055)}
.sec{overflow:visible}
.sec .wrap{position:relative;z-index:1}
@media (max-width:900px){.secnum{font-size:120px;top:16px}}
@media (prefers-reduced-motion:reduce){#boot{display:none}}
body.static #boot{display:none}
"""
s=s.replace("</style>",CSS+"</style>",1)

# ---------- 3. boot HTML ----------
BOOT="""<div id="boot" aria-hidden="true">
  <div class="bl">ARCHIVE://COMMERCIAL/2026 <b>&#8250;</b> LOCATING MASTER FILE</div>
  <div class="cnt2" id="bootpct">0%</div>
  <div class="bbar"><i id="bootbar"></i></div>
  <div class="bfile">ORAN CARMON &middot; THE COMMERCIAL SYSTEMS BUILDER</div>
</div>
"""
s=s.replace('<div id="pbar"></div>',BOOT+'<div id="pbar"></div>',1)

# ---------- 4. ghost numerals ----------
NUMS=[("hero",None),("statement",None),("philosophy","01"),("files","02"),("xtix","03"),("oasis","04"),
("eventer","05"),("medcoin","06"),("leadership","07"),("tech","08"),("final","09")]
for sec,num in NUMS:
    if not num: continue
    s=s.replace('id="%s"'%sec+'', 'id="%s"'%sec, 1)
import re
def addnum(sid,num,txt):
    pat='<section class="sec case" id="%s"'%sid
    if pat not in txt: pat='<section class="sec" id="%s"'%sid
    i=txt.index(pat)
    j=txt.index('>',i)+1
    return txt[:j]+'\n  <div class="secnum" aria-hidden="true">%s</div>'%num+txt[j:]
for sec,num in NUMS:
    if num: s=addnum(sec,num,s)
print("numerals in")

# ---------- 5. LANDO JS: boot + smooth scroll + numeral parallax ----------
JS="""
<script>
(function(){
"use strict";
var q=new URLSearchParams(location.search);
var reduced=window.matchMedia('(prefers-reduced-motion: reduce)').matches;
var isStatic=q.get('static')==='1';
var boot=document.getElementById('boot');
if(reduced||isStatic){if(boot)boot.remove();}
else if(boot){
  var pct=document.getElementById('bootpct'),bar=document.getElementById('bootbar');
  var t0=null,DUR=1450;
  document.documentElement.style.overflow='hidden';
  function step(ts){
    if(!t0)t0=ts;
    var pr=Math.min(1,(ts-t0)/DUR);
    var e=1-Math.pow(1-pr,2.2);
    var v=Math.round(e*100);
    pct.textContent=v+'%';
    bar.style.width=(e*100)+'%';
    if(pr<1)requestAnimationFrame(step);
    else{
      setTimeout(function(){
        boot.classList.add('done');
        document.documentElement.style.overflow='';
        setTimeout(function(){boot.remove()},820);
      },140);
    }
  }
  requestAnimationFrame(step);
}

/* ---- inertia smooth scroll (desktop wheel) ---- */
if(!reduced&&!isStatic&&window.matchMedia('(pointer:fine)').matches){
  var target=window.pageYOffset,cur=target,writing=false,active=false;
  function maxY(){var h=document.documentElement;return h.scrollHeight-h.clientHeight}
  window.addEventListener('wheel',function(e){
    if(e.ctrlKey)return;
    e.preventDefault();
    var d=e.deltaY;if(e.deltaMode===1)d*=16;else if(e.deltaMode===2)d*=window.innerHeight;
    target=Math.max(0,Math.min(maxY(),target+d));
    active=true;
  },{passive:false});
  window.addEventListener('scroll',function(){
    if(writing)return;
    var y=window.pageYOffset;
    if(Math.abs(y-cur)>2){cur=y;target=y;}
  },{passive:true});
  document.querySelectorAll('#rail a, a[href^="#"]').forEach(function(a){
    a.addEventListener('click',function(ev){
      var id=a.getAttribute('href');
      if(!id||id.charAt(0)!=='#')return;
      var el=document.querySelector(id);
      if(!el)return;
      ev.preventDefault();
      target=Math.max(0,Math.min(maxY(),el.getBoundingClientRect().top+window.pageYOffset-8));
      active=true;
    });
  });
  (function loop(){
    if(active){
      cur+=(target-cur)*.11;
      if(Math.abs(target-cur)<.4){cur=target;active=Math.abs(target-cur)>=.4;}
      writing=true;window.scrollTo(0,cur);writing=false;
    }
    requestAnimationFrame(loop);
  })();
}

/* ---- ghost numeral parallax ---- */
if(!reduced&&!isStatic){
  var nums=[].slice.call(document.querySelectorAll('.secnum'));
  (function nloop(){
    for(var i=0;i<nums.length;i++){
      var r=nums[i].parentElement.getBoundingClientRect();
      if(r.bottom>0&&r.top<window.innerHeight){
        nums[i].style.transform='translateY('+((r.top-window.innerHeight*.5)*-.14)+'px)';
      }
    }
    requestAnimationFrame(nloop);
  })();
}
})();
</script>"""
s=s.rstrip()+"\n"+JS
io.open(p,"w",encoding="utf-8").write(s)
print("lando layer done:",len(s),"bytes")
