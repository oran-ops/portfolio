# -*- coding: utf-8 -*-
# Desk-reveal choreography: lerped progress, slow linear lid to -98deg (stays visible),
# anticipation tilt, page settle, staggered declassify bars.
import io
s=io.open("site.html",encoding="utf-8").read()

OLD_MAP="""var THS=[].slice.call(document.querySelectorAll('.otx')).map(function(x){
  return {x:x,ots:x.querySelector('.ots'),otf:x.querySelector('.otf'),
    cover:x.querySelector('.otf-cover'),veil:x.querySelector('.otf-veil'),
    drw:x.querySelector('.otdrw'),stat:x.querySelector('.otstat'),
    lab:x.querySelector('.otstat').textContent,t:0,h:1,lp:-1,sndA:0,sndB:0};
});"""
NEW_MAP="""var THS=[].slice.call(document.querySelectorAll('.otx')).map(function(x){
  return {x:x,ots:x.querySelector('.ots'),otf:x.querySelector('.otf'),
    cover:x.querySelector('.otf-cover'),veil:x.querySelector('.otf-veil'),
    drw:x.querySelector('.otdrw'),stat:x.querySelector('.otstat'),
    lines:x.querySelector('.ou-lines'),reds:[].slice.call(x.querySelectorAll('.ou-red')),
    lab:x.querySelector('.otstat').textContent,t:0,h:1,lp:-1,disp:0,sndA:0,sndB:0};
});
function band(p,a,b){var t=(p-a)/(b-a);t=t<0?0:t>1?1:t;return t*t*(3-2*t)}"""
assert OLD_MAP in s, "THS map anchor"
s=s.replace(OLD_MAP,NEW_MAP,1)

OLD_LOOP="""    /* theaters */
    for(var j=0;j<THS.length;j++){
      var th=THS[j];
      var tp=clamp((y-th.t)/th.h);
      if(tp===th.lp)continue;
      /* sound triggers on upward crossings */
      var now=performance.now();
      if(th.lp>-1&&th.lp<.04&&tp>=.04&&now-th.sndA>1200){th.sndA=now;paper();}
      if(th.lp>-1&&th.lp<.56&&tp>=.56&&now-th.sndB>1200){th.sndB=now;flip();}
      th.lp=tp;
      var pull=eo(clamp(tp/.40));
      th.otf.style.transform='translateY('+((1-pull)*44)+'vh) scale('+(.62+.38*pull)+')';
      var dfade=clamp((tp-.38)/.16);
      th.drw.style.opacity=String(1-dfade);
      th.drw.style.transform='translateX(-50%) translateY('+(eo(dfade)*9)+'vh)';
      var open=band ? 0 : 0;
      th.cover.style.transform='rotateX('+(-open*138)+'deg)';
      th.veil.style.opacity=String((1-open)*.55);
      var msg = tp<.48?('PULLING '+th.lab.replace('PULLING ','')):(tp<.84?'OPENING FILE \\u2026':'FILE OPEN \\u2014 READ \\u2193');
      if(th.stat.textContent!==msg)th.stat.textContent=msg;
    }"""
# NOTE: the real current text has open=eo(...) — build it exactly:
OLD_LOOP="""    /* theaters */
    for(var j=0;j<THS.length;j++){
      var th=THS[j];
      var tp=clamp((y-th.t)/th.h);
      if(tp===th.lp)continue;
      /* sound triggers on upward crossings */
      var now=performance.now();
      if(th.lp>-1&&th.lp<.04&&tp>=.04&&now-th.sndA>1200){th.sndA=now;paper();}
      if(th.lp>-1&&th.lp<.56&&tp>=.56&&now-th.sndB>1200){th.sndB=now;flip();}
      th.lp=tp;
      var pull=eo(clamp(tp/.40));
      th.otf.style.transform='translateY('+((1-pull)*44)+'vh) scale('+(.62+.38*pull)+')';
      var dfade=clamp((tp-.38)/.16);
      th.drw.style.opacity=String(1-dfade);
      th.drw.style.transform='translateX(-50%) translateY('+(eo(dfade)*9)+'vh)';
      var open=eo(clamp((tp-.48)/.38));
      th.cover.style.transform='rotateX('+(-open*138)+'deg)';
      th.veil.style.opacity=String((1-open)*.55);
      var msg = tp<.48?('PULLING '+th.lab.replace('PULLING ','')):(tp<.84?'OPENING FILE \\u2026':'FILE OPEN \\u2014 READ \\u2193');
      if(th.stat.textContent!==msg)th.stat.textContent=msg;
    }"""
NEW_LOOP="""    /* theaters — desk-reveal choreography (progress is LERPED: cannot jump) */
    for(var j=0;j<THS.length;j++){
      var th=THS[j];
      var tp=clamp((y-th.t)/th.h);
      if(th.lp===-1){th.disp=tp;}
      var dnew=th.disp+(tp-th.disp)*.13;
      if(Math.abs(tp-dnew)<.0012)dnew=tp;
      if(tp===th.lp&&dnew===th.disp)continue;
      th.disp=dnew;
      var now=performance.now();
      if(th.lp>-1&&th.lp<.04&&tp>=.04&&now-th.sndA>1200){th.sndA=now;paper();}
      if(th.lp>-1&&th.lp<.5&&tp>=.5&&now-th.sndB>1200){th.sndB=now;flip();}
      th.lp=tp;
      var p=dnew;
      var pull=eo(clamp(p/.36));
      var tilt=7*band(p,.26,.46)*(1-band(p,.52,.86));
      th.otf.style.transform='translateY('+((1-pull)*44)+'vh) scale('+(.62+.38*pull)+') rotateX('+tilt.toFixed(2)+'deg)';
      var dfade=band(p,.34,.5);
      th.drw.style.opacity=String(1-dfade);
      th.drw.style.transform='translateX(-50%) translateY('+(eo(dfade)*9)+'vh)';
      var open=band(p,.38,.80);
      th.cover.style.transform='rotateX('+(-(open*98)).toFixed(2)+'deg)';
      th.veil.style.opacity=String(.6*(1-band(p,.45,.72)));
      if(th.lines)th.lines.style.transform='translateY('+((1-band(p,.5,.78))*14).toFixed(1)+'px)';
      for(var rj=0;rj<th.reds.length;rj++){
        th.reds[rj].style.transform='scaleX('+(1-band(p,.72+rj*.07,.82+rj*.07)).toFixed(3)+')';
      }
      var msg = p<.36?('PULLING '+th.lab.replace('PULLING ','')):(p<.78?'OPENING COVER \\u2026':'FILE OPEN \\u2014 READ \\u2193');
      if(th.stat.textContent!==msg)th.stat.textContent=msg;
    }"""
assert OLD_LOOP in s, "theater loop anchor"
s=s.replace(OLD_LOOP,NEW_LOOP,1)

OLD_CSS=""".oc-backf{position:absolute;inset:0;backface-visibility:hidden;transform:rotateX(180deg);border-radius:inherit;
background:var(--oc);background-image:linear-gradient(rgba(19,20,23,.34),rgba(19,20,23,.34))}"""
NEW_CSS=""".oc-backf{position:absolute;inset:0;backface-visibility:hidden;transform:rotateX(180deg);border-radius:inherit;
background:var(--oc);background-image:linear-gradient(rgba(19,20,23,.34),rgba(19,20,23,.34))}
.oc-backf:before{content:"";position:absolute;inset:16px;border:1.5px solid rgba(19,20,23,.3);border-radius:12px}
.oc-backf:after{content:"";position:absolute;left:50%;bottom:24px;transform:translateX(-50%);width:130px;height:11px;border-radius:6px;background:rgba(19,20,23,.24)}
.otf:before{content:"";position:absolute;left:8px;right:8px;top:0;height:1px;background:rgba(255,255,255,.09);z-index:5}
.ou-lines{transform:translateY(14px);will-change:transform}
.ou-red{transform-origin:right center;will-change:transform}"""
assert OLD_CSS in s, "backf css anchor"
s=s.replace(OLD_CSS,NEW_CSS,1)

io.open("site.html","w",encoding="utf-8").write(s)
head='<!doctype html>\n<html lang="en">\n<head>\n<meta charset="utf-8">\n<meta name="viewport" content="width=device-width,initial-scale=1">\n<meta name="color-scheme" content="dark">\n</head>\n<body>\n'
io.open("site_standalone.html","w",encoding="utf-8").write(head+s+"\n</body>\n</html>")
print("DESK REVEAL installed")
