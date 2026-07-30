# -*- coding: utf-8 -*-
# Round 17 — flights become physics. v4's bezier control points shared the flow
# field's tangent, and the flow has a coherent global direction at any moment, so
# all 1900 arcs bowed the same way: the swarm visibly converged above-left, then
# the sentence materialised elsewhere. No path can be trusted to point at its end.
#
# v5: each dispatched star is a body. Every frame it accelerates toward ITS OWN
# target (spring + damping), stirred by per-star decorrelated noise that fades
# with proximity. The perceived convergence point is therefore the sentence
# itself at every instant. Size/colour derive from distance-to-target, so the
# text condenses exactly where the dots arrive. Telemetry (?aitele=1) records the
# swarm centroid every frame so the claim is measurable, not felt.
import io, re

p = 'site.html'
s = io.open(p, encoding='utf-8').read()

s2, n = re.subn(r'<script>\s*/\* SECOND INTELLIGENCE IV.*?</script>\n?', '', s, flags=re.S)
print('v4 removed:', n)
s = s2
assert 'if(window.__ai2){window.__ai2(p);}else{words(W2,.40,.26);}' in s, 'hook missing'

MODULE = r"""
<script>
/* SECOND INTELLIGENCE V — every star steers at its own point of the sentence */
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
var TELE=q.get('aitele')==='1';
if(TELE)window.__tele=[];

var CALL0=.20,CALL1=.36,
    G0=.36,G1=.66,
    U0=.74,U1=.92,
    FR0=.93,FR1=.985;

var NTXT=1900,FREE=260,TOTAL=NTXT+FREE;
var cv=null,ctx=null,DPR=1,SPR={};
var T=null,N=0,key='';
var ST=null;
var t=0,fr=0,lastY=-1,kick=0,cleared=true;
var P=-1,PRE=-1;
var stTop=0,geomKey='';
var mx=-1e4,my=-1e4,vx=0,vy=0,pmx=0,pmy=0;
var doneSnd=false;

function rng(i){var x=Math.sin(i*127.1+311.7)*43758.5453;return x-Math.floor(x)}
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
      x:0,y:0,vx:0,vy:0,
      z:z,
      sz:(3.0+rng(i*17+4)*2.8)*z,
      d:rng(i*19+6)*.85,
      k:.011+rng(i*23+7)*.007,
      dp:.90+rng(i*43+15)*.025,
      nw:.9+rng(i*29+8)*1.6,
      ph:rng(i*31+9)*6.28,
      ph2:rng(i*47+17)*6.28,
      tw:.8+rng(i*53+19)*1.4,
      b:rng(i*37+11)*.8,
      spr:z>.75?(kind>.45?'em':'wt'):(z>.45?(kind>.6?'wt':'dm'):'dm'),
      a:(.3+z*.5)*(kind>.85?1.25:1),
      ssz:2.2+rng(i*41+13)*.9,
      mode:0,flare:0,
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
  t+=.016;fr++;

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
  var tcx=0,tcy=0,scx=0,scy=0,sn=0,nfly=0,nland=0;
  for(var i=0;i<TOTAL;i++){
    var st=ST[i];
    var birth=sm((PRE-st.b)/.16);
    if(birth<=.01)continue;
    var isTxt=hasT&&i<N;

    /* the field home keeps drifting in the shared currents */
    if(st.mode===0){
      var sp=.4*st.z;
      st.fx+=flx(st.fx,st.fy,t)*sp;
      st.fy+=fly(st.fx,st.fy,t)*sp+kick*st.z*.5;
      if(st.fx<-50)st.fx+=W+100;if(st.fx>W+50)st.fx-=W+100;
      if(st.fy<-50)st.fy+=H+100;if(st.fy>H+50)st.fy-=H+100;
    }

    var tx=0,ty=0;
    if(isTxt){
      tx=T[i*2]+r.left;ty=T[i*2+1]+r.top;
      if(call>0&&st.mode===0){st.fx+=(tx-st.fx)*.005*call;st.fy+=(ty-st.fy)*.005*call}
      if(st.mode===0&&front>st.d+.001){
        st.x=st.fx;st.y=st.fy;
        st.vx=flx(st.fx,st.fy,t)*.4*st.z;st.vy=fly(st.fx,st.fy,t)*.4*st.z;
        st.mode=1;
      }else if((st.mode===1||st.mode===2)&&front<st.d-.05){
        st.mode=3;
      }
    }

    var X,Y,ev=0;
    if(isTxt&&st.mode===1){
      /* the body steers at its own point of the sentence, always */
      var dxx=tx-st.x,dyy=ty-st.y;
      var dist=Math.sqrt(dxx*dxx+dyy*dyy);
      var namp=2.1*clampU(dist/260);
      st.vx+=dxx*st.k+Math.sin(t*st.nw+st.ph)*namp;
      st.vy+=dyy*st.k+Math.cos(t*st.nw*.93+st.ph2)*namp;
      var dmp=dist<40?.84:st.dp;
      st.vx*=dmp;st.vy*=dmp;
      var vv=Math.sqrt(st.vx*st.vx+st.vy*st.vy);
      if(vv>15){st.vx*=15/vv;st.vy*=15/vv}
      st.x+=st.vx;st.y+=st.vy;
      if(dist<2.2&&vv<1.1){st.x=tx;st.y=ty;st.mode=2;st.flare=9}
      X=st.x;Y=st.y;
      ev=1-clampU(dist/240);
      nfly++;
    }else if(isTxt&&st.mode===2){
      X=tx;Y=ty;ev=1;nland++;
    }else if(isTxt&&st.mode===3){
      /* going home: same physics, the target is the living field home */
      var hx=st.fx,hy=st.fy;
      var dxx2=hx-st.x,dyy2=hy-st.y;
      var dist2=Math.sqrt(dxx2*dxx2+dyy2*dyy2);
      st.vx+=dxx2*st.k*.8+Math.sin(t*st.nw+st.ph)*1.4;
      st.vy+=dyy2*st.k*.8+Math.cos(t*st.nw*.93+st.ph2)*1.4;
      st.vx*=.9;st.vy*=.9;
      var vv2=Math.sqrt(st.vx*st.vx+st.vy*st.vy);
      if(vv2>15){st.vx*=15/vv2;st.vy*=15/vv2}
      st.x+=st.vx;st.y+=st.vy;
      if(dist2<8){st.mode=0}
      X=st.x;Y=st.y;
      ev=clampU(1-dist2/240)*.4;
    }else{X=st.fx;Y=st.fy}

    var pf=isTxt?(1-ev):1;
    if(mx>-1e3){X+=(mx-W/2)*.012*st.z*pf;Y+=(my-H/2)*.008*st.z*pf}

    if(isTxt&&st.mode===2&&u<.6){
      var ddx=X-mx,ddy=Y-my,dd=Math.sqrt(ddx*ddx+ddy*ddy);
      if(dd<R){var f=1-dd/R;X+=f*Math.sin(t*2.2+i)*(6+vx*.7);Y+=f*Math.cos(t*2.2+i)*(6+vy*.7)}
    }

    var twk=.78+.22*Math.sin(t*st.tw+st.ph);
    var a=st.a*twk*birth;
    if(isTxt){a*=(.8+.4*ev);a*=(1-u)}
    else{a*=freeOut}
    if(a<=.012)continue;

    var d2=isTxt?(st.sz*(1-ev)+st.ssz*ev)*(1-u*.45):st.sz;
    if(st.flare>0){d2*=1+.05*st.flare;st.flare--}
    if(d2<2.2)d2=2.2;
    var spr=isTxt&&ev>.7?SPR.core:(isTxt&&ev>.45?SPR.em:SPR[st.spr]);
    ctx.globalAlpha=Math.min(1,a);
    if(st.has&&ev<.9){
      var mvx=X-st.px,mvy=Y-st.py,mv=mvx*mvx+mvy*mvy;
      if(mv>9&&mv<784){ctx.globalAlpha=Math.min(1,a*.35);ctx.drawImage(spr,st.px-d2,st.py-d2,d2*2,d2*2);ctx.globalAlpha=Math.min(1,a)}
    }
    ctx.drawImage(spr,X-d2,Y-d2,d2*2,d2*2);
    st.px=X;st.py=Y;st.has=true;
    if(TELE&&isTxt&&(st.mode===1||st.mode===2)){scx+=X;scy+=Y;sn++;tcx+=tx;tcy+=ty}
  }
  ctx.globalAlpha=1;
  if(TELE&&sn>0){
    window.__tele.push([fr,Math.round(scx/sn),Math.round(scy/sn),
      Math.round(tcx/sn),Math.round(tcy/sn),nfly,nland]);
  }
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
print('v5 installed, site', len(s.encode('utf-8')), 'bytes')
