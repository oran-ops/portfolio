# -*- coding: utf-8 -*-
# Round 15 — the space rebuilt properly.
#   birth:    stars are born one by one across the FIRST screen's scroll, so the
#             field is already spread when the statement arrives
#   feel:     an internal eased progress chases the scroll (lerp), so wheel steps
#             can never show — everything glides
#   gather:   fewer, calmer stars; arcs tightened; a landing star condenses into
#             a small hard point instead of a soft blob
#   handover: long overlap (18% of the scene) where the constellation shrinks
#             into the glyph strokes while the real type rises beneath it
#   fixes:    pointer parallax fades out as a star lands (was shifting the
#             constellation off the type), trails capped, twinkle slowed
# Test hooks: ?aipre=0..1 (birth phase) and ?aip=0..1 (scene phase) freeze the
# choreography for deterministic captures.
import io, re

p = 'site.html'
s = io.open(p, encoding='utf-8').read()

s2, n = re.subn(r'<script>\s*/\* SECOND INTELLIGENCE II.*?</script>\n?', '', s, flags=re.S)
print('old module removed:', n)
s = s2
assert 'if(window.__ai2){window.__ai2(p);}else{words(W2,.40,.26);}' in s, 'hook missing'

MODULE = r"""
<script>
/* SECOND INTELLIGENCE III — space is born on the first screen; the sentence condenses out of it */
(function(){
"use strict";
try{
var q=new URLSearchParams(location.search);
if(matchMedia('(prefers-reduced-motion: reduce)').matches)return;
if(q.get('static')==='1')return;
if(innerWidth<861&&q.get('force')!=='1')return;
var L2=document.getElementById('stmt2'),L1=document.getElementById('stmt1');
var stWrap=document.querySelector('#statement .pinh');
if(!L2||!stWrap)return;
var W2i=[].slice.call(L2.querySelectorAll('.w>i'));
var TP=q.get('aip')!==null?parseFloat(q.get('aip')):null;
var TPRE=q.get('aipre')!==null?parseFloat(q.get('aipre')):null;

/* choreography — fractions of the pinned scene */
var CALL0=.20,CALL1=.38,
    G0=.38,G1=.70,K=.75,
    U0=.74,U1=.92,
    FR0=.93,FR1=.985;

var NTXT=1900,FREE=260,TOTAL=NTXT+FREE;
var cv=null,ctx=null,DPR=1,SPR={};
var T=null,N=0,key='';
var ST=null;
var t=0,lastY=-1,kick=0,cleared=true;
var P=-1,PRE=-1;             /* eased progress, chase the scroll */
var stTop=0,geomKey='';
var mx=-1e4,my=-1e4,vx=0,vy=0,pmx=0,pmy=0;
var doneSnd=false;

function rng(i){var x=Math.sin(i*127.1+311.7)*43758.5453;return x-Math.floor(x)}
function q5(v){return v<.5?16*v*v*v*v*v:1-Math.pow(-2*v+2,5)/2}
function sm(v){return v<=0?0:v>=1?1:v*v*(3-2*v)}
function clampU(v){return v<0?0:v>1?1:v}
function band(p,a,b){return clampU((p-a)/(b-a))}

function sprite(mid,core,tight){
  var c=document.createElement('canvas');c.width=c.height=32;
  var g=c.getContext('2d');
  var r=g.createRadialGradient(16,16,0,16,16,16);
  r.addColorStop(0,core);r.addColorStop(tight?.5:.3,mid);r.addColorStop(1,'rgba(25,26,31,0)');
  g.fillStyle=r;g.fillRect(0,0,32,32);
  return c;
}
function ensure(){
  if(cv)return;
  cv=document.createElement('canvas');cv.id='ai2c';
  cv.style.cssText='position:fixed;inset:0;z-index:57;pointer-events:none';
  document.body.appendChild(cv);ctx=cv.getContext('2d');
  SPR.em=sprite('rgba(47,179,128,.9)','rgba(235,255,246,.95)',false);
  SPR.wt=sprite('rgba(207,208,212,.85)','rgba(255,255,255,.92)',false);
  SPR.dm=sprite('rgba(140,142,148,.55)','rgba(200,201,206,.6)',false);
  SPR.core=sprite('rgba(47,179,128,1)','rgba(240,255,248,1)',true);
  size();build();
  addEventListener('resize',function(){if(cv){size();key='';geomKey='';build()}},{passive:true});
}
function size(){DPR=Math.min(2,devicePixelRatio||1);cv.width=innerWidth*DPR;cv.height=innerHeight*DPR;ctx.setTransform(DPR,0,0,DPR,0,0)}

function build(){
  ST=new Array(TOTAL);
  var W=innerWidth,H=innerHeight;
  for(var i=0;i<TOTAL;i++){
    var z=.25+rng(i*3+1)*.75;
    var kind=rng(i*7+5);
    ST[i]={
      fx:rng(i*11+2)*W, fy:rng(i*13+3)*H,
      z:z,
      sz:(3.0+rng(i*17+4)*2.8)*z,
      d:rng(i*19+6)*.45,
      perp:(rng(i*23+7)-.5)*140,
      tw:.8+rng(i*29+8)*1.4,
      ph:rng(i*31+9)*6.28,
      b:rng(i*37+11)*.8,
      spr:z>.75?(kind>.45?'em':'wt'):(z>.45?(kind>.6?'wt':'dm'):'dm'),
      a:(.3+z*.5)*(kind>.85?1.25:1),
      px:0,py:0,has:false
    };
  }
}

function geom(){
  var k=innerWidth+'x'+innerHeight;
  if(k===geomKey)return;
  geomKey=k;
  stTop=stWrap.getBoundingClientRect().top+pageYOffset;
}

function sample(){
  if(document.fonts&&document.fonts.status!=='loaded')return false;
  var r=L2.getBoundingClientRect();
  if(r.width<40)return false;
  var k=Math.round(r.width)+'x'+Math.round(r.height)+'x'+innerWidth;
  if(k===key&&T)return true;
  var cs=getComputedStyle(L2);
  var w=Math.ceil(r.width),h=Math.ceil(r.height*1.4);
  var off=document.createElement('canvas');off.width=w;off.height=h;
  var o=off.getContext('2d');
  o.fillStyle='#fff';o.textBaseline='middle';
  o.font=cs.fontWeight+' '+cs.fontSize+' '+cs.fontFamily;
  try{o.letterSpacing=cs.letterSpacing==='normal'?'0px':cs.letterSpacing}catch(e){}
  var txt=(L2.textContent||'').replace(/\s+/g,' ').trim();
  var tw=o.measureText(txt).width;
  o.fillText(txt,(w-tw)/2,h/2);
  var data=o.getImageData(0,0,w,h).data;
  var step=3,pts;
  do{
    pts=[];
    for(var y=0;y<h;y+=step){for(var x=0;x<w;x+=step){
      if(data[(y*w+x)*4+3]>140){pts.push(x,y-(h-r.height)/2)}
    }}
    step++;
  }while(pts.length/2>NTXT&&step<8);
  T=pts;N=Math.min(NTXT,pts.length/2);key=k;
  return true;
}

function setW2(v,rise){
  for(var i=0;i<W2i.length;i++){
    W2i[i].style.opacity=String(v);
    W2i[i].style.transform=v>=1?'none':'translateY('+((1-v)*(rise?10:0))+'%)';
  }
  if(!W2i.length)L2.style.opacity=String(v);
}

function flx(x,y,tt){return Math.sin(y*.0022+tt*.25)+Math.cos((x+y)*.0013-tt*.17)}
function fly(x,y,tt){return Math.cos(x*.0021-tt*.22)+Math.sin((x-y)*.0011+tt*.13)}

document.addEventListener('mousemove',function(e){pmx=mx;pmy=my;mx=e.clientX;my=e.clientY;
  if(pmx>-1e3){vx=mx-pmx;vy=my-pmy}},{passive:true});

window.__ai2=function(pRaw){
  geom();
  var yNow=pageYOffset,vhh=innerHeight;
  var preRaw=stTop>vhh*.3?clampU((yNow-vhh*.3)/(stTop-vhh*.3)):1;
  if(pRaw>0)preRaw=1;
  if(TP!==null){pRaw=TP;P=TP}
  if(TPRE!==null){preRaw=TPRE;PRE=TPRE}

  /* the eased clocks — wheel steps can never reach the pixels */
  if(P<0)P=pRaw;if(PRE<0)PRE=preRaw;
  P+=(pRaw-P)*.085;
  PRE+=(preRaw-PRE)*.085;

  var u=band(P,U0,U1);u=sm(u);
  var freeOut=1-band(P,FR0,FR1);
  if(PRE<.003||(P>.99&&freeOut<=.02)){
    if(cv&&!cleared){ctx.clearRect(0,0,innerWidth,innerHeight);cleared=true}
    setW2(P>=U1?1:0,false);
    if(P<G0)doneSnd=false;
    return;
  }
  ensure();
  var hasT=sample();
  cleared=false;
  t+=.016;

  if(lastY>=0)kick+=(yNow-lastY)*.02;
  lastY=yNow;kick*=.88;
  vx*=.9;vy*=.9;

  var call=band(P,CALL0,CALL1)*.35;
  var g=band(P,G0,G1);
  var W=innerWidth,H=innerHeight;
  var r=L2.getBoundingClientRect();
  var R=70+Math.hypot(vx,vy)*2.2;

  if(u>=1){setW2(1,false)}else{setW2(u,true)}
  if(u>=.999&&!doneSnd){doneSnd=true;
    try{window.__archAudio&&window.__archAudio.tick&&window.__archAudio.tick()}catch(e){}
    try{window.__archLog&&window.__archLog('SECOND INTELLIGENCE ONLINE',2600)}catch(e){}
  }

  ctx.clearRect(0,0,W,H);
  for(var i=0;i<TOTAL;i++){
    var st=ST[i];
    var birth=sm((PRE-st.b)/.16);
    if(birth<=.01)continue;
    var isTxt=hasT&&i<N;

    var e=0;
    if(isTxt){e=q5(clampU(g*(1+K)-st.d*K))}
    if(e<.55){
      var sp=(1-e)*.4*st.z;
      st.fx+=flx(st.fx,st.fy,t)*sp;
      st.fy+=fly(st.fx,st.fy,t)*sp+kick*st.z*(1-e)*.5;
      if(st.fx<-50)st.fx+=W+100;if(st.fx>W+50)st.fx-=W+100;
      if(st.fy<-50)st.fy+=H+100;if(st.fy>H+50)st.fy-=H+100;
    }
    var tx=0,ty=0;
    if(isTxt){tx=T[i*2]+r.left;ty=T[i*2+1]+r.top;
      if(call>0&&e<.05){st.fx+=(tx-st.fx)*.006*call;st.fy+=(ty-st.fy)*.006*call}
    }
    var X,Y;
    if(isTxt&&e>0){
      var dxx=tx-st.fx,dyy=ty-st.fy,dl=Math.max(60,Math.hypot(dxx,dyy));
      var arc=st.perp*(1-e);
      var cxp=(st.fx+tx)/2-dyy/dl*arc;
      var cyp=(st.fy+ty)/2+dxx/dl*arc;
      var ie=1-e;
      X=ie*ie*st.fx+2*ie*e*cxp+e*e*tx;
      Y=ie*ie*st.fy+2*ie*e*cyp+e*e*ty;
    }else{X=st.fx;Y=st.fy}

    /* depth parallax — released as the star lands, so the constellation
       sits exactly where the type will stand */
    var pf=isTxt?(1-e):1;
    if(mx>-1e3){X+=(mx-W/2)*.012*st.z*pf;Y+=(my-H/2)*.008*st.z*pf}

    if(isTxt&&g>.92&&u<.6){
      var ddx=X-mx,ddy=Y-my,dd=Math.sqrt(ddx*ddx+ddy*ddy);
      if(dd<R){var f=1-dd/R;X+=f*Math.sin(t*2.2+i)*(6+vx*.7);Y+=f*Math.cos(t*2.2+i)*(6+vy*.7)}
    }

    var twk=.78+.22*Math.sin(t*st.tw+st.ph);
    var a=st.a*twk*birth;
    if(isTxt){a*=(.8+.4*e);a*=(1-u)}
    else{a*=freeOut}
    if(a<=.012)continue;

    /* a landing star condenses into a hard point */
    var d2=isTxt?(st.sz*(1-e)+2.6*e)*(1-u*.45):st.sz;
    if(d2<2.2)d2=2.2;
    var spr=isTxt&&e>.7?SPR.core:(isTxt&&e>.45?SPR.em:SPR[st.spr]);
    ctx.globalAlpha=Math.min(1,a);
    if(st.has&&e<.85){
      var mvx=X-st.px,mvy=Y-st.py,mv=mvx*mvx+mvy*mvy;
      if(mv>9&&mv<784){ctx.globalAlpha=Math.min(1,a*.35);ctx.drawImage(spr,st.px-d2,st.py-d2,d2*2,d2*2);ctx.globalAlpha=Math.min(1,a)}
    }
    ctx.drawImage(spr,X-d2,Y-d2,d2*2,d2*2);
    st.px=X;st.py=Y;st.has=true;
  }
  ctx.globalAlpha=1;
};
}catch(err){}
})();
</script>
"""

k = s.rfind('</script>')
s = s[:k + 9] + '\n' + MODULE.strip() + s[k + 9:]
io.open(p, 'w', encoding='utf-8', newline='').write(s)
head = ('<!doctype html>\n<html lang="en">\n<head>\n<meta charset="utf-8">\n'
        '<meta name="viewport" content="width=device-width,initial-scale=1">\n'
        '<meta name="color-scheme" content="dark">\n</head>\n<body>\n')
io.open('site_standalone.html', 'w', encoding='utf-8', newline='').write(head + s + '\n</body>\n</html>')
print('v3 installed, site', len(s.encode('utf-8')), 'bytes')
