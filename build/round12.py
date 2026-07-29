# -*- coding: utf-8 -*-
# Round 12 — the dust signs the file. At the very end of the document the drifting
# dust gathers into the name, holds, and disperses. Its own canvas, so the ambient
# dust engine is untouched.
import io

MODULE = r"""
<script>
/* ARCHIVE SIGNATURE — the dust was the evidence all along */
(function(){
"use strict";
try{
  var q=new URLSearchParams(location.search);
  if(matchMedia('(prefers-reduced-motion: reduce)').matches)return;
  if(q.get('static')==='1')return;

  var cv=null,ctx=null,W=0,H=0,DPR=1,P=[],T=null,sampled=false;
  var prog=0,state='idle',t0=0,armed=true,lastY=0;
  var mx=-1e4,my=-1e4,pmx=0,pmy=0,vx=0,vy=0,running=false;

  function make(){
    cv=document.createElement('canvas');
    cv.id='dustsig';
    cv.style.cssText='position:fixed;inset:0;z-index:58;pointer-events:none;opacity:0;transition:opacity .5s linear';
    document.body.appendChild(cv);
    ctx=cv.getContext('2d');
    size();
    addEventListener('resize',function(){clearTimeout(cv.__t);cv.__t=setTimeout(function(){size();sampled=false;seed()},200)},{passive:true});
    document.addEventListener('mousemove',function(e){pmx=mx;pmy=my;mx=e.clientX;my=e.clientY;
      if(pmx>-1e3){vx=mx-pmx;vy=my-pmy}},{passive:true});
  }
  function size(){
    DPR=Math.min(2,window.devicePixelRatio||1);
    W=innerWidth;H=innerHeight;
    cv.width=W*DPR;cv.height=H*DPR;ctx.setTransform(DPR,0,0,DPR,0,0);
  }
  function sample(){
    var off=document.createElement('canvas');off.width=W;off.height=H;
    var o=off.getContext('2d');
    o.fillStyle='#fff';o.textAlign='center';o.textBaseline='middle';
    var big=Math.round(Math.min(W/8.2,96));
    o.font='800 '+big+'px Inter, sans-serif';
    o.fillText('ORAN CARMON',W/2,H*0.47);
    var sm=Math.round(Math.min(W/44,15));
    o.font='700 '+sm+'px "JetBrains Mono", monospace';
    o.fillText('C O M M E R C I A L   S Y S T E M S   B U I L D E R',W/2,H*0.47+big*0.72);
    var d=o.getImageData(0,0,W,H).data,out=[],step=W>900?3:2;
    for(var y=0;y<H;y+=step){for(var x=0;x<W;x+=step){
      if(d[(y*W+x)*4+3]>140)out.push(x,y);
    }}
    /* deterministic shuffle so the sweep order is stable across frames */
    var n=out.length/2;
    for(var i=n-1;i>0;i--){
      var j=(i*9301+49297)%(i+1);
      var ax=out[i*2],ay=out[i*2+1];
      out[i*2]=out[j*2];out[i*2+1]=out[j*2+1];out[j*2]=ax;out[j*2+1]=ay;
    }
    T=out;sampled=true;
  }
  function seed(){
    var n=Math.round(Math.min(1400,Math.max(500,W*H/1500)));
    P=[];
    for(var i=0;i<n;i++){
      P.push({x:Math.random()*W,y:Math.random()*H,
        dx:(Math.random()-.5)*.26,dy:(Math.random()-.5)*.22,
        r:Math.random()*1.2+.7,a:Math.random()*.32+.12,
        s1:Math.random(),s2:Math.random()});
    }
  }
  function ready(cb){
    if(!cv)make();
    if(!P.length)seed();
    if(sampled)return cb();
    if(document.fonts&&document.fonts.ready){document.fonts.ready.then(function(){sample();cb()})}
    else{sample();cb()}
  }

  function begin(){
    if(state!=='idle'||!armed)return;
    armed=false;
    ready(function(){
      state='form';t0=performance.now();
      cv.style.opacity='1';
      if(!running){running=true;requestAnimationFrame(loop)}
      try{if(window.__archLog)window.__archLog('SIGNATURE ON FILE',2600)}catch(e){}
    });
  }
  function loop(now){
    var el=now-t0;
    if(state==='form'){prog=Math.min(1,el/1500);if(prog>=1){state='hold';t0=now}}
    else if(state==='hold'){prog=1;if(el>2400){state='out';t0=now}}
    else if(state==='out'){prog=Math.max(0,1-el/1200);
      if(prog<=0){state='idle';cv.style.opacity='0';running=false;ctx.clearRect(0,0,W,H);return}}
    draw();
    requestAnimationFrame(loop);
  }
  function ease(p){return p<.5?8*p*p*p*p:1-Math.pow(-2*p+2,4)/2}

  function draw(){
    ctx.clearRect(0,0,W,H);
    var n=P.length,tn=T?T.length/2:0,R=54+Math.hypot(vx,vy)*3.4;
    vx*=.88;vy*=.88;
    var e=ease(prog),tt=performance.now()/1000;
    for(var i=0;i<n;i++){
      var p=P[i];
      p.x+=p.dx;p.y+=p.dy;
      if(p.x<0)p.x=W;if(p.x>W)p.x=0;if(p.y<0)p.y=H;if(p.y>H)p.y=0;
      var X=p.x,Y=p.y,s=0;
      if(tn){
        var d=i/n;
        s=Math.min(1,Math.max(0,e*(1+d*.85)-d*.85));
        var k=(i%tn)*2;
        X=p.x+(T[k]-p.x)*s;Y=p.y+(T[k+1]-p.y)*s;
      }
      var ddx=X-mx,ddy=Y-my,dist=Math.sqrt(ddx*ddx+ddy*ddy);
      if(dist<R){
        var f=1-dist/R;
        X+=f*Math.sin(tt*2.6+p.s1*6.28)*(p.s2*9+vx*1.4);
        Y+=f*Math.cos(tt*2.6+p.s1*6.28)*(p.s2*9+vy*1.4);
      }
      ctx.globalAlpha=p.a+s*.62;
      ctx.fillStyle=s>.55?'#2FB380':'#CFD0D4';
      var sz=p.r*(1+s*.5);
      ctx.fillRect(X,Y,sz,sz);
    }
    ctx.globalAlpha=1;
  }

  /* the signature fires once you reach the end of the file, and re-arms
     only after you have travelled back up the document */
  addEventListener('scroll',function(){
    var y=pageYOffset,doc=document.documentElement.scrollHeight;
    if(y+innerHeight>doc-120){begin()}
    else if(doc-(y+innerHeight)>innerHeight*1.2){armed=true}
    lastY=y;
  },{passive:true});
}catch(err){}
})();
</script>
"""

p = 'site.html'
s = io.open(p, encoding='utf-8').read()
k = s.rfind('</script>')
s = s[:k + 9] + '\n' + MODULE.strip() + s[k + 9:]
io.open(p, 'w', encoding='utf-8', newline='').write(s)

head = ('<!doctype html>\n<html lang="en">\n<head>\n<meta charset="utf-8">\n'
        '<meta name="viewport" content="width=device-width,initial-scale=1">\n'
        '<meta name="color-scheme" content="dark">\n</head>\n<body>\n')
io.open('site_standalone.html', 'w', encoding='utf-8', newline='').write(head + s + '\n</body>\n</html>')
print('signature module added:', len(s.encode('utf-8')), 'bytes')
