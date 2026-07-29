# -*- coding: utf-8 -*-
# Round 14 — the statement becomes deep space. Soft round stars in three depth
# layers float in flowing currents from the moment the scene opens; as you scroll
# they are called toward the sentence, arc in on curved orbits, hold as a
# constellation, and dissolve into the real type on a scrubbed crossfade.
# Nothing pops: the stars that become the sentence are the ones you watched float.
import io, re

p = 'site.html'
s = io.open(p, encoding='utf-8').read()

s2, n = re.subn(r'<script>\s*/\* SECOND INTELLIGENCE.*?</script>\n?', '', s, flags=re.S)
print('old module removed:', n)
s = s2
assert 'if(window.__ai2){window.__ai2(p);}else{words(W2,.40,.26);}' in s, 'hook still present'

MODULE = r"""
<script>
/* SECOND INTELLIGENCE II — the sentence condenses out of deep space */
(function(){
"use strict";
try{
var q=new URLSearchParams(location.search);
if(matchMedia('(prefers-reduced-motion: reduce)').matches)return;
if(q.get('static')==='1')return;
if(innerWidth<861&&q.get('force')!=='1')return;
var L2=document.getElementById('stmt2'),L1=document.getElementById('stmt1');
if(!L2)return;
var W2i=[].slice.call(L2.querySelectorAll('.w>i'));

/* choreography (fractions of the pinned scene) */
var FIN0=.004,FIN1=.06,   /* field fades in            */
    CALL0=.24,CALL1=.40,  /* stars lean toward the line */
    G0=.40,G1=.78,K=.8,   /* orbit in and settle        */
    XF0=.815,XF1=.875,    /* constellation -> real type */
    FO0=.90,FO1=.97;      /* residual space fades out   */

var FREE=340,CAP=2400;
var cv=null,ctx=null,DPR=1,SPR={};
var T=null,N=0,key='',ST=null,total=0;
var t=0,lastY=-1,kick=0,cleared=true;
var mx=-1e4,my=-1e4,vx=0,vy=0,pmx=0,pmy=0;
var doneSnd=false;

function rng(i){var x=Math.sin(i*127.1+311.7)*43758.5453;return x-Math.floor(x)}
function q5(v){return v<.5?16*v*v*v*v*v:1-Math.pow(-2*v+2,5)/2}
function clampU(v){return v<0?0:v>1?1:v}
function band(p,a,b){return clampU((p-a)/(b-a))}

function sprite(mid,core){
  var c=document.createElement('canvas');c.width=c.height=32;
  var g=c.getContext('2d');
  var r=g.createRadialGradient(16,16,0,16,16,16);
  r.addColorStop(0,core);r.addColorStop(.3,mid);r.addColorStop(1,'rgba(25,26,31,0)');
  g.fillStyle=r;g.fillRect(0,0,32,32);
  return c;
}
function ensure(){
  if(cv)return;
  cv=document.createElement('canvas');cv.id='ai2c';
  cv.style.cssText='position:fixed;inset:0;z-index:57;pointer-events:none';
  document.body.appendChild(cv);ctx=cv.getContext('2d');
  SPR.em=sprite('rgba(47,179,128,.9)','rgba(235,255,246,.95)');
  SPR.wt=sprite('rgba(207,208,212,.85)','rgba(255,255,255,.92)');
  SPR.dm=sprite('rgba(140,142,148,.55)','rgba(200,201,206,.6)');
  size();
  addEventListener('resize',function(){if(cv){size();key=''}},{passive:true});
}
function size(){DPR=Math.min(2,devicePixelRatio||1);cv.width=innerWidth*DPR;cv.height=innerHeight*DPR;ctx.setTransform(DPR,0,0,DPR,0,0)}

function setW2(v,rise){
  for(var i=0;i<W2i.length;i++){
    W2i[i].style.opacity=String(v);
    W2i[i].style.transform=v>=1?'none':'translateY('+((1-v)*(rise?12:0))+'%)';
  }
  if(!W2i.length)L2.style.opacity=String(v);
}

function sample(){
  if(document.fonts&&document.fonts.status!=='loaded')return false;
  var r=L2.getBoundingClientRect();
  if(r.width<40)return false;
  var k=Math.round(r.width)+'x'+Math.round(r.height)+'x'+innerWidth+'x'+innerHeight;
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
  var step=2,pts;
  do{
    pts=[];
    for(var y=0;y<h;y+=step){for(var x=0;x<w;x+=step){
      if(data[(y*w+x)*4+3]>140){pts.push(x,y-(h-r.height)/2)}
    }}
    step++;
  }while(pts.length/2>CAP&&step<7);
  T=pts;N=pts.length/2;key=k;
  build();
  return true;
}

/* every star exists from the first frame of the scene; the first N of them
   happen to be the ones the sentence will claim */
function build(){
  total=N+FREE;
  ST=new Array(total);
  var W=innerWidth,H=innerHeight;
  for(var i=0;i<total;i++){
    var z=.25+rng(i*3+1)*.75;
    var kind=rng(i*7+5);
    ST[i]={
      fx:rng(i*11+2)*W, fy:rng(i*13+3)*H,
      z:z,
      sz:(3.2+rng(i*17+4)*3.2)*z,
      d:rng(i*19+6)*.55,
      perp:(rng(i*23+7)-.5)*260,
      tw:1.5+rng(i*29+8)*2.5,
      ph:rng(i*31+9)*6.28,
      spr:z>.75?(kind>.45?'em':'wt'):(z>.45?(kind>.6?'wt':'dm'):'dm'),
      a:(.28+z*.5)*(kind>.85?1.25:1),
      px:0,py:0,has:false
    };
  }
}

/* slow space currents */
function flx(x,y,tt){return Math.sin(y*.0022+tt*.25)+Math.cos((x+y)*.0013-tt*.17)}
function fly(x,y,tt){return Math.cos(x*.0021-tt*.22)+Math.sin((x-y)*.0011+tt*.13)}

document.addEventListener('mousemove',function(e){pmx=mx;pmy=my;mx=e.clientX;my=e.clientY;
  if(pmx>-1e3){vx=mx-pmx;vy=my-pmy}},{passive:true});

window.__ai2=function(p){
  var fieldA=Math.min(band(p,FIN0,FIN1),1-band(p,FO0,FO1));
  if(fieldA<=0){
    if(cv&&!cleared){ctx.clearRect(0,0,innerWidth,innerHeight);cleared=true}
    setW2(p>=XF1?1:0,false);
    if(p<G0)doneSnd=false;
    return;
  }
  ensure();
  if(!sample()){setW2(1,false);return}
  cleared=false;
  t+=.016;

  /* the page's scroll speed stirs the field */
  var yNow=pageYOffset;
  if(lastY>=0)kick+=(yNow-lastY)*.028;
  lastY=yNow;kick*=.88;
  vx*=.9;vy*=.9;

  var call=band(p,CALL0,CALL1)*.35;
  var g=band(p,G0,G1);
  var u=band(p,XF0,XF1);           /* scrubbed crossfade into real type */
  var W=innerWidth,H=innerHeight;
  var r=L2.getBoundingClientRect();
  var R=70+Math.hypot(vx,vy)*2.2;

  /* the real line rises inside the crossfade, in place */
  if(u>=1){setW2(1,false)}else{setW2(u,true)}
  if(u>=1&&!doneSnd){doneSnd=true;
    try{window.__archAudio&&window.__archAudio.tick&&window.__archAudio.tick()}catch(e){}
    try{window.__archLog&&window.__archLog('SECOND INTELLIGENCE ONLINE',2600)}catch(e){}
  }

  ctx.clearRect(0,0,W,H);
  for(var i=0;i<total;i++){
    var st=ST[i];
    var isTxt=i<N;

    /* free drift along the currents — always alive */
    var e=0;
    if(isTxt){var sN=clampU(g*(1+K)-st.d*K);e=q5(sN)}
    if(e<.6){
      var sp=(1-e)*.42*st.z;
      st.fx+=(flx(st.fx,st.fy,t))*sp;
      st.fy+=(fly(st.fx,st.fy,t))*sp+kick*st.z*.5;
      if(st.fx<-50)st.fx+=W+100;if(st.fx>W+50)st.fx-=W+100;
      if(st.fy<-50)st.fy+=H+100;if(st.fy>H+50)st.fy-=H+100;
    }
    /* the call: the whole field leans toward the sentence */
    var tx=0,ty=0;
    if(isTxt){tx=T[i*2]+r.left;ty=T[i*2+1]+r.top;
      if(call>0&&e<.1){st.fx+=(tx-st.fx)*.006*call;st.fy+=(ty-st.fy)*.006*call}
    }
    var X,Y;
    if(isTxt&&e>0){
      /* curved orbit in: quadratic bezier with a per-star arc */
      var cxp=(st.fx+tx)/2-((ty-st.fy))/Math.max(60,Math.hypot(tx-st.fx,ty-st.fy))*st.perp*(1-e);
      var cyp=(st.fy+ty)/2+((tx-st.fx))/Math.max(60,Math.hypot(tx-st.fx,ty-st.fy))*st.perp*(1-e);
      var ie=1-e;
      X=ie*ie*st.fx+2*ie*e*cxp+e*e*tx;
      Y=ie*ie*st.fy+2*ie*e*cyp+e*e*ty;
    }else{X=st.fx;Y=st.fy}

    /* depth parallax from the pointer */
    X+=(mx>-1e3?(mx-W/2)*.012*st.z:0);
    Y+=(my>-1e3?(my-H/2)*.008*st.z:0);

    /* settled constellation breathes; pointer stirs it */
    if(isTxt&&g>.92){
      var ddx=X-mx,ddy=Y-my,dd=Math.sqrt(ddx*ddx+ddy*ddy);
      if(dd<R){var f=1-dd/R;X+=f*Math.sin(t*2.6+i)*(7+vx*.8);Y+=f*Math.cos(t*2.6+i)*(7+vy*.8)}
    }

    /* alpha: twinkle in space, brighten as it lands, hand over to the type */
    var twk=.72+.28*Math.sin(t*st.tw+st.ph);
    var a=st.a*twk*fieldA;
    if(isTxt){a*=(0.75+.55*e);a*=(1-u)}
    if(a<=0.01)continue;

    var d2=st.sz*(isTxt?(1-e*.34):1);
    var spr=isTxt&&e>.55?SPR.em:SPR[st.spr];
    ctx.globalAlpha=Math.min(1,a);
    /* motion ghost: a short comet tail when moving fast */
    if(st.has){
      var mvx=X-st.px,mvy=Y-st.py,mv=mvx*mvx+mvy*mvy;
      if(mv>9&&mv<4000){ctx.globalAlpha=Math.min(1,a*.38);ctx.drawImage(spr,st.px-d2,st.py-d2,d2*2,d2*2);ctx.globalAlpha=Math.min(1,a)}
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
print('deep-space module installed, site', len(s.encode('utf-8')), 'bytes')
