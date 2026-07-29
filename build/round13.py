# -*- coding: utf-8 -*-
# Round 13 — the dust moves to the statement. "One intelligence built the world."
# is set type; "Two will build the next." assembles itself, scrubbed by the scroll
# of the pinned scene. The end state is the real crisp text, never particles.
import io, re

p = 'site.html'
s = io.open(p, encoding='utf-8').read()

# 1. the end-of-document signature is gone
s2, n = re.subn(r'<script>\s*/\* ARCHIVE SIGNATURE.*?</script>\n?', '', s, flags=re.S)
print('old signature module removed:', n)
s = s2

# 2. line 2 of the statement hands its reveal to the assembly module
old = 'words(W2,.40,.26);'
assert old in s, 'statement hook anchor missing'
s = s.replace(old, 'if(window.__ai2){window.__ai2(p);}else{words(W2,.40,.26);}', 1)
print('statement hook installed')

MODULE = r"""
<script>
/* SECOND INTELLIGENCE — the second line assembles itself out of the archive dust */
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
var cv=null,ctx=null,DPR=1,T=null,S=null,N=0,key='';
var doneSnd=false,shown=-1,t=0;
function rng(i){var x=Math.sin(i*127.1+311.7)*43758.5453;return x-Math.floor(x)}
function q5(v){return v<.5?16*v*v*v*v*v:1-Math.pow(-2*v+2,5)/2}
function ensure(){
  if(cv)return;
  cv=document.createElement('canvas');cv.id='ai2c';
  cv.style.cssText='position:fixed;inset:0;z-index:57;pointer-events:none';
  document.body.appendChild(cv);ctx=cv.getContext('2d');size();
  addEventListener('resize',function(){if(cv){size();key=''}},{passive:true});
}
function size(){DPR=Math.min(2,devicePixelRatio||1);cv.width=innerWidth*DPR;cv.height=innerHeight*DPR;ctx.setTransform(DPR,0,0,DPR,0,0)}
function setW2(v){
  for(var i=0;i<W2i.length;i++){
    W2i[i].style.opacity=String(v);
    W2i[i].style.transform=v?'none':'translateY(115%)';
  }
  if(!W2i.length)L2.style.opacity=String(v);
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
  var step=2,pts;
  do{
    pts=[];
    for(var y=0;y<h;y+=step){for(var x=0;x<w;x+=step){
      if(data[(y*w+x)*4+3]>140){pts.push(x,y-(h-r.height)/2)}
    }}
    step++;
  }while(pts.length/2>2600&&step<7);
  T=pts;N=pts.length/2;key=k;
  var r1=L1?L1.getBoundingClientRect():r;
  S=new Float32Array(N*2);
  for(var i=0;i<N;i++){
    var a=rng(i),b=rng(i+9999),c=rng(i+51234);
    if(a<.62){
      S[i*2]=(r1.left-r.left)+b*r1.width+(rng(i+777)-.5)*90;
      S[i*2+1]=(r1.top-r.top)+c*r1.height+(rng(i+888)-.5)*70;
    }else{
      S[i*2]=(b-.5)*innerWidth*.9+r.width/2;
      S[i*2+1]=(c-.9)*innerHeight*.7;
    }
  }
  return true;
}
var mx=-1e4,my=-1e4,vx=0,vy=0,pmx=0,pmy=0;
document.addEventListener('mousemove',function(e){pmx=mx;pmy=my;mx=e.clientX;my=e.clientY;
  if(pmx>-1e3){vx=mx-pmx;vy=my-pmy}},{passive:true});
window.__ai2=function(p){
  t+=.016;
  var prog=Math.max(0,Math.min(1,(p-.38)/.34));
  if(prog<=0){
    if(cv){ctx.clearRect(0,0,innerWidth,innerHeight);cv.style.opacity='0'}
    if(shown!==0){setW2(0);shown=0}
    doneSnd=false;return;
  }
  ensure();
  if(!sample()){if(shown!==1){setW2(1);shown=1}return}
  if(prog>=.995){
    ctx.clearRect(0,0,innerWidth,innerHeight);cv.style.opacity='0';
    if(shown!==1){setW2(1);shown=1;
      if(!doneSnd){doneSnd=true;
        try{window.__archAudio&&window.__archAudio.tick&&window.__archAudio.tick()}catch(e){}
        try{window.__archLog&&window.__archLog('SECOND INTELLIGENCE ONLINE',2600)}catch(e){}
      }
    }
    return;
  }
  cv.style.opacity='1';
  if(shown!==0){setW2(0);shown=0}
  var r=L2.getBoundingClientRect();
  ctx.clearRect(0,0,innerWidth,innerHeight);
  var K=.85,R=64+Math.hypot(vx,vy)*2.4;vx*=.9;vy*=.9;
  for(var i=0;i<N;i++){
    var d=i/N;
    var sN=Math.max(0,Math.min(1,prog*(1+K)-d*K));
    var e=q5(sN);
    var sx=S[i*2],sy=S[i*2+1],tx=T[i*2],ty=T[i*2+1];
    var X=sx+(tx-sx)*e,Y=sy+(ty-sy)*e;
    var sw=(1-e)*16;
    X+=Math.sin(t*2.2+i*.61)*sw*rng(i+3);
    Y+=Math.cos(t*2.4+i*.37)*sw*rng(i+4);
    X+=r.left;Y+=r.top;
    if(prog>.9){
      var ddx=X-mx,ddy=Y-my,dd=Math.sqrt(ddx*ddx+ddy*ddy);
      if(dd<R){var f=1-dd/R;X+=f*Math.sin(t*3+i)*(6+vx);Y+=f*Math.cos(t*3+i)*(6+vy)}
    }
    var a=rng(i+42);
    ctx.globalAlpha=.34+.62*e;
    ctx.fillStyle=e<.55?'#9BE3C6':(a>.82?'#F2F1ED':'#2FB380');
    var z=(2.5+a*1.3)*(1-e*.22);
    ctx.fillRect(X,Y,z,z);
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
print('module installed, site', len(s.encode('utf-8')), 'bytes')
