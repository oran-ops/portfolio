# -*- coding: utf-8 -*-
# MISSION B — the living layer: custom cursor, kinetic marquee typography, idle life, folder tilt
import io
p="site.html"; s=io.open(p,encoding="utf-8").read()

CSS="""
/* ===================== ALIVE LAYER ===================== */
@media (pointer:fine){html.jscur,html.jscur body,html.jscur a{cursor:none}}
#cur{position:fixed;top:0;left:0;width:9px;height:9px;background:var(--emb);transform:translate(-100px,-100px) rotate(45deg);
pointer-events:none;z-index:9999}
#curR{position:fixed;top:0;left:0;width:36px;height:36px;border:1px solid rgba(242,241,237,.35);border-radius:50%;
transform:translate(-120px,-120px);pointer-events:none;z-index:9998;transition:width .25s var(--ease),height .25s var(--ease),border-color .25s var(--ease)}
#curR.hot{width:56px;height:56px;border-color:var(--emb)}

#heromq{position:absolute;inset:0;overflow:hidden;z-index:0;pointer-events:none}
#heromq .row{position:absolute;white-space:nowrap;width:max-content;font-weight:900;letter-spacing:-.02em;
color:transparent;-webkit-text-stroke:1px rgba(242,241,237,.06)}
#heromq .r1{top:4%;font-size:170px;animation:mqd 80s linear infinite}
#heromq .r2{bottom:3%;font-size:170px;animation:mqr 95s linear infinite}
#hero .center,#hero .idx,#hero .barc,#hero .drawer,#hero .tag,#hero .cue{position:relative;z-index:2}
#hero .idx,#hero .barc{position:absolute}

.bigmq{overflow:hidden;padding:30px 0;border-top:1px solid var(--hair);border-bottom:1px solid var(--hair)}
.bigmq .in2{display:flex;white-space:nowrap;width:max-content;animation:mqd 46s linear infinite;
font-weight:900;font-size:88px;letter-spacing:-.02em;line-height:1;color:transparent;
-webkit-text-stroke:1.2px var(--mqc,rgba(242,241,237,.14))}
.bigmq .in2 span{padding-right:70px}
@keyframes mqd{to{transform:translateX(-50%)}}
@keyframes mqr{from{transform:translateX(-50%)}to{transform:translateX(0)}}

#files .lip{animation:bob 6s ease-in-out infinite}
#files .tab:nth-child(1) .lip{animation-delay:0s}
#files .tab:nth-child(2) .lip{animation-delay:.7s}
#files .tab:nth-child(3) .lip{animation-delay:1.4s}
#files .tab:nth-child(4) .lip{animation-delay:2.1s}
@keyframes bob{0%,100%{transform:translateY(0)}50%{transform:translateY(-4px)}}
.rub .d{animation:dpulse 4.5s ease-in-out infinite}
@keyframes dpulse{0%,100%{transform:rotate(45deg) scale(1)}50%{transform:rotate(45deg) scale(1.22)}}
#hero .barc svg rect:nth-child(7){animation:barbl 4.2s steps(1) infinite}
#hero .barc svg rect:nth-child(13){animation:barbl 6.4s steps(1) infinite reverse}
@keyframes barbl{0%,88%{opacity:1}89%,100%{opacity:.2}}
.folder{will-change:transform}

@media (prefers-reduced-motion:reduce){
 #cur,#curR,#heromq{display:none!important}
 .bigmq .in2,#files .lip,.rub .d,#hero .barc svg rect{animation:none!important}
}
body.static #cur,body.static #curR{display:none}
body.static .bigmq .in2,body.static #files .lip,body.static .rub .d{animation:none!important}
"""
s=s.replace("</style>",CSS+"</style>",1)

# ---------- hero marquee ----------
mq_txt="COMMERCIAL SYSTEMS BUILDER &mdash; ORAN CARMON &mdash; ARCHIVE 2026 &mdash; "
hero_mq=('<div id="heromq" aria-hidden="true">'
'<div class="row r1"><span>'+mq_txt*3+'</span><span>'+mq_txt*3+'</span></div>'
'<div class="row r2"><span>'+mq_txt*3+'</span><span>'+mq_txt*3+'</span></div>'
'</div>')
s=s.replace('<section class="sec" id="hero">','<section class="sec" id="hero">\n  '+hero_mq,1)

# ---------- chapter marquee bands ----------
def band(txt,color):
    inner='<span>'+ (txt+' &mdash; ')*4 +'</span>'
    return ('<div class="bigmq" style="--mqc:%s" aria-hidden="true"><div class="in2">%s%s</div></div>'%(color,inner,inner))
s=s.replace('<section class="sec case" id="oasis"',
            band("FILE 02 &middot; OASIS &middot; LEADERSHIP","rgba(224,164,88,.20)")+'\n<section class="sec case" id="oasis"',1)
s=s.replace('<section class="sec case" id="medcoin"',
            band("FILE 04 &middot; MEDCOIN &middot; FOUNDER","rgba(242,241,237,.15)")+'\n<section class="sec case" id="medcoin"',1)
s=s.replace('<section class="sec" id="tech"',
            band("SYSTEM FILE &middot; AI &middot; COMMERCIAL INTELLIGENCE","rgba(244,96,62,.20)")+'\n<section class="sec" id="tech"',1)

# ---------- folder tilt hook in scrub writer ----------
s=s.replace("el.style.transform='translateY('+((1-e1)*56)+'px)';",
            "el.style.transform='perspective(1200px) translateY('+((1-e1)*56)+'px) rotateX(var(--rx,0deg)) rotateY(var(--ry,0deg))';",1)

# ---------- alive JS ----------
ALIVE="""
<script>
(function(){
"use strict";
var q=new URLSearchParams(location.search);
var reduced=window.matchMedia('(prefers-reduced-motion: reduce)').matches;
var isStatic=q.get('static')==='1';
if(reduced||isStatic)return;
var fine=window.matchMedia('(pointer:fine)').matches;
if(fine){
  document.documentElement.classList.add('jscur');
  var cur=document.createElement('div');cur.id='cur';document.body.appendChild(cur);
  var ring=document.createElement('div');ring.id='curR';document.body.appendChild(ring);
  var mx=-100,my=-100,cx=-100,cy=-100,rx=-120,ry=-120;
  document.addEventListener('mousemove',function(e){mx=e.clientX;my=e.clientY;
    var hot=e.target.closest&&e.target.closest('a,.dtab,#files .tab,.crow,.chip,.sc');
    ring.classList.toggle('hot',!!hot);
  },{passive:true});
  (function loop(){
    cx+=(mx-cx)*.4;cy+=(my-cy)*.4;rx+=(mx-rx)*.16;ry+=(my-ry)*.16;
    cur.style.transform='translate('+(cx-4.5)+'px,'+(cy-4.5)+'px) rotate(45deg)';
    ring.style.transform='translate('+(rx-18)+'px,'+(ry-18)+'px)';
    requestAnimationFrame(loop);
  })();
  [].forEach.call(document.querySelectorAll('.folder'),function(f){
    f.addEventListener('mousemove',function(e){
      var r=f.getBoundingClientRect();
      var dx=(e.clientX-r.left)/r.width-.5, dy=(e.clientY-r.top)/r.height-.5;
      f.style.setProperty('--ry',(dx*1.1)+'deg');
      f.style.setProperty('--rx',(-dy*.9)+'deg');
    },{passive:true});
    f.addEventListener('mouseleave',function(){
      f.style.setProperty('--ry','0deg');f.style.setProperty('--rx','0deg');
    });
  });
}
})();
</script>"""
s=s.rstrip()
if s.endswith("</script>"):
    s=s+"\n"+ALIVE
io.open(p,"w",encoding="utf-8").write(s)
print("alive layer applied:",len(s),"bytes")
