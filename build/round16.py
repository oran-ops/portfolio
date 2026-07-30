# -*- coding: utf-8 -*-
# Round 16 — the gather is re-driven. Scroll only DISPATCHES stars; each flight
# then runs on its own clock (0.9–1.5s, quintic), launched tangent to the star's
# current drift on a cubic curve, so float becomes flight with no visible seam,
# and a pause in scrolling can never freeze a star mid-air. Reversal returns a
# star to the living field on its own clock too. Landing gets a small flare.
import io, re

p = 'site.html'
s = io.open(p, encoding='utf-8').read()

s2, n = re.subn(r'<script>\s*/\* SECOND INTELLIGENCE III.*?</script>\n?', '', s, flags=re.S)
print('v3 removed:', n)
s = s2
assert 'if(window.__ai2){window.__ai2(p);}else{words(W2,.40,.26);}' in s, 'hook missing'

MODULE = r"""
<script>
/* SECOND INTELLIGENCE IV — scroll dispatches, time flies */
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

var CALL0=.20,CALL1=.36,
    G0=.36,G1=.66,          /* the launch window                  */
    U0=.74,U1=.92,          /* constellation -> real type          */
    FR0=.93,FR1=.985;

var NTXT=1900,FREE=260,TOTAL=NTXT+FREE;
var cv=null,ctx=null,DPR=1,SPR={};
var T=null,N=0,key='';
var ST=null;
var t=0,lastY=-1,kick=0,cleared=true;
var P=-1,PRE=-1;
var stTop=0,geomKey='';
var mx=-1e4,my=-1e4,vx=0,vy=0,pmx=0,pmy=0;
var doneSnd=false;

function rng(i){var x=Math.sin(i*127.1+311.7)*43758.5453;return x-Math.floor(x)}
function q5(v){return v<=0?0:v>=1?1:(v<.5?16*v*v*v*v*v:1-Math.pow(-2*v+2,5)/2)}
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
  cv.style.cssText='position:fixed;inset:0;z-index:1;pointer-events:none';
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
      d:rng(i*19+6)*.85,
      tw:.8+rng(i*29+8)*1.4,
      ph:rng(i*31+9)*6.28,
      b:rng(i*37+11)*.8,
      spr:z>.75?(kind>.45?'em':'wt'):(z>.45?(kind>.6?'wt':'dm'):'dm'),
      a:(.3+z*.5)*(kind>.85?1.25:1),
      ssz:2.2+rng(i*41+13)*.9,
      mode:0,fe:0,fdur:55+rng(i*43+15)*35,rdur:34+rng(i*47+17)*16,
      lx:0,ly:0,c1x:0,c1y:0,c2dx:0,c2dy:0,r0x:0,r0y:0,flare:0,
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
      if(data[(y*w+x)*4+3]>140){var jj=pts.length;
        pts.push(x+(rng(jj*13+29)-.5)*2.6,y-(h-r.height)/2+(rng(jj*17+31)-.5)*2.6)}
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

/* the flight leaves along the star's own current, on a cubic curve */
function dispatch(st,i,tx,ty){
  st.lx=st.fx;st.ly=st.fy;
  var tvx=flx(st.fx,st.fy,t),tvy=fly(st.fx,st.fy,t);
  var tl=Math.max(.35,Math.hypot(tvx,tvy));
  var reach=60+rng(i*53+19)*50;
  st.c1x=st.lx+tvx/tl*reach;
  st.c1y=st.ly+tvy/tl*reach;
  var dx=tx-st.lx,dy=ty-st.ly,dl=Math.max(60,Math.hypot(dx,dy));
  var back=70+rng(i*59+21)*60;
  var side=(rng(i*61+23)-.5)*70;
  st.c2dx=-dx/dl*back-dy/dl*side;
  st.c2dy=-dy/dl*back+dx/dl*side;
  st.mode=1;st.fe=0;
}
function beginReturn(st){
  st.r0x=st.px;st.r0y=st.py;
  st.mode=3;st.fe=0;
}

document.addEventListener('mousemove',function(e){pmx=mx;pmy=my;mx=e.clientX;my=e.clientY;
  if(pmx>-1e3){vx=mx-pmx;vy=my-pmy}},{passive:true});

window.__ai2=function(pRaw){
  geom();
  var yNow=pageYOffset,vhh=innerHeight;
  var preRaw=stTop>vhh*.3?clampU((yNow-vhh*.3)/(stTop-vhh*.3)):1;
  if(pRaw>0)preRaw=1;
  if(TP!==null){pRaw=TP;P=TP}
  if(TPRE!==null){preRaw=TPRE;PRE=TPRE}

  if(P<0)P=pRaw;if(PRE<0)PRE=preRaw;
  P+=(pRaw-P)*.085;
  PRE+=(preRaw-PRE)*.085;

  var u=sm(band(P,U0,U1));
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

  var call=band(P,CALL0,CALL1)*.3;
  var front=band(P,G0,G1);
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

    /* the home position keeps living in the currents, whatever the mode */
    var sp=.4*st.z*(st.mode===0?1:.5);
    st.fx+=flx(st.fx,st.fy,t)*sp;
    st.fy+=fly(st.fx,st.fy,t)*sp+kick*st.z*(st.mode===0?.5:.15);
    if(st.fx<-50)st.fx+=W+100;if(st.fx>W+50)st.fx-=W+100;
    if(st.fy<-50)st.fy+=H+100;if(st.fy>H+50)st.fy-=H+100;

    var tx=0,ty=0;
    if(isTxt){
      tx=T[i*2]+r.left;ty=T[i*2+1]+r.top;
      if(call>0&&st.mode===0){st.fx+=(tx-st.fx)*.005*call;st.fy+=(ty-st.fy)*.005*call}
      /* scroll dispatches; time flies */
      if(st.mode===0&&front>st.d+.001){dispatch(st,i,tx,ty)}
      else if((st.mode===1||st.mode===2)&&front<st.d-.05){beginReturn(st)}
    }

    var X,Y,e=0;
    if(isTxt&&st.mode===1){
      st.fe+=1/st.fdur;
      var s1=q5(st.fe);e=s1;
      if(st.fe>=1){st.mode=2;st.flare=9;e=1;X=tx;Y=ty}
      else{
        var ie=1-s1;
        var c2x=tx+st.c2dx,c2y=ty+st.c2dy;
        X=ie*ie*ie*st.lx+3*ie*ie*s1*st.c1x+3*ie*s1*s1*c2x+s1*s1*s1*tx;
        Y=ie*ie*ie*st.ly+3*ie*ie*s1*st.c1y+3*ie*s1*s1*c2y+s1*s1*s1*ty;
      }
    }else if(isTxt&&st.mode===2){
      X=tx;Y=ty;e=1;
    }else if(isTxt&&st.mode===3){
      st.fe+=1/st.rdur;
      var s2=q5(st.fe);e=1-s2;
      X=st.r0x+(st.fx-st.r0x)*s2;
      Y=st.r0y+(st.fy-st.r0y)*s2;
      if(st.fe>=1){st.mode=0;e=0}
    }else{X=st.fx;Y=st.fy}

    var pf=isTxt?(1-e):1;
    if(mx>-1e3){X+=(mx-W/2)*.012*st.z*pf;Y+=(my-H/2)*.008*st.z*pf}

    if(isTxt&&st.mode===2&&u<.6){
      var ddx=X-mx,ddy=Y-my,dd=Math.sqrt(ddx*ddx+ddy*ddy);
      if(dd<R){var f=1-dd/R;X+=f*Math.sin(t*2.2+i)*(6+vx*.7);Y+=f*Math.cos(t*2.2+i)*(6+vy*.7)}
    }

    var twk=.78+.22*Math.sin(t*st.tw+st.ph);
    var a=st.a*twk*birth;
    if(isTxt){a*=(.8+.4*e);a*=(1-u)}
    else{a*=freeOut}
    if(a<=.012)continue;

    var d2=isTxt?(st.sz*(1-e)+st.ssz*e)*(1-u*.45):st.sz;
    if(st.flare>0){d2*=1+.05*st.flare;st.flare--}
    if(d2<2.2)d2=2.2;
    var spr=isTxt&&e>.7?SPR.core:(isTxt&&e>.45?SPR.em:SPR[st.spr]);
    ctx.globalAlpha=Math.min(1,a);
    if(st.has&&e<.9){
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
io.open('_cap.html', 'w', encoding='utf-8', newline='').write(
    io.open('site_standalone.html', encoding='utf-8').read().replace('words(W1,.05,.30);', 'words(W1,-1,.30);'))
print('v4 installed, site', len(s.encode('utf-8')), 'bytes')
