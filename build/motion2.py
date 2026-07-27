# -*- coding: utf-8 -*-
# MOTION V2 — full choreography pass on site.html
import io, re
s=io.open("site.html",encoding="utf-8").read()

# ============ 1. CSS ============
CSS="""
/* ===================== MOTION V2 ===================== */
.rv.on{opacity:1;transform:none}
.wipe{clip-path:inset(-6% 101% -10% -1%)}
.rv.wipe{transition:opacity .85s var(--ease),transform .85s var(--ease),clip-path 1.05s var(--ease);transition-delay:calc(var(--i,0)*80ms)}
.wipe.on{clip-path:inset(-6% -1% -10% -1%)}
.st{opacity:0;transform:translateY(16px)}
.u.on .st{opacity:1;transform:none;transition:opacity .55s var(--ease) calc(var(--i,0)*65ms),transform .55s var(--ease) calc(var(--i,0)*65ms)}
.st .c{transform:scale(0) rotate(-45deg)}
.u.on .st .c{transform:scale(1) rotate(0deg);transition:transform .4s var(--ease) calc(var(--i,0)*65ms + .26s)}
.st .o{transform:scale(0)}
.u.on .st .o{transform:scale(1);transition:transform .4s var(--ease) calc(var(--i,0)*65ms + .22s)}
.dash.st::before{transform:scaleX(0);transform-origin:left}
.u.on .dash.st::before{transform:scaleX(1);transition:transform .45s var(--ease) calc(var(--i,0)*65ms + .18s)}
.u .zr{opacity:0;transform:translateX(-16px)}
.u.on .zr{opacity:1;transform:none;transition:opacity .6s var(--ease),transform .6s var(--ease)}
.u .zr .d2{transform:rotate(225deg) scale(0)}
.u.on .zr .d2{transform:rotate(45deg) scale(1);transition:transform .55s var(--ease) .15s}
.u.on .rvs{opacity:1;transform:none}
.case .hairtop{border-top:0}
.case .hairtop::before{content:"";position:absolute;top:0;left:0;right:0;height:1px;background:var(--grid);transform:scaleX(0);transform-origin:left}
.case .hairtop{position:relative}
.case .hairtop.on::before{transform:scaleX(1);transition:transform 1.1s var(--ease)}
.lessq{border-left:0;position:relative}
.lessq::before{content:"";position:absolute;left:0;top:2px;bottom:2px;width:2px;background:var(--fc,var(--emb));transform:scaleY(0);transform-origin:top}
.lessq.on::before,.u.on .lessq::before{transform:scaleY(1);transition:transform .8s var(--ease) .25s}
.sigp::before,.sigp::after{width:0;height:0;opacity:0}
.sigp.on::before,.sigp.on::after{width:17px;height:17px;opacity:1;transition:width .5s var(--ease) .55s,height .5s var(--ease) .55s,opacity .3s var(--ease) .55s}
.folder .flip{opacity:0;transform:translateY(9px)}
.folder.on .flip{opacity:1;transform:none;transition:opacity .55s var(--ease) .08s,transform .55s var(--ease) .08s}
.u.on .garc{stroke-dashoffset:0}
.u.on .pdraw{stroke-dashoffset:0}
.u.on .ndot{opacity:1;transform:scale(1)}
.u.on .bar0{transform:scaleY(1)}
#philosophy .node svg *{stroke-dasharray:1;stroke-dashoffset:1}
#philosophy .u.on .node svg *{stroke-dashoffset:0;transition:stroke-dashoffset .75s var(--ease) calc(var(--i,0)*85ms + var(--pi,0)*70ms + .2s)}
.crawlp{animation:crawlp 8s linear infinite}
@keyframes crawlp{to{stroke-dashoffset:-56}}
.bignum{opacity:0;transform:translateY(12px) scale(.97)}
.u.on .bignum{opacity:1;transform:none;transition:opacity .7s var(--ease),transform .7s var(--ease)}
.ticker{overflow:hidden;border-top:1px solid var(--hair);border-bottom:1px solid var(--hair);margin-top:64px}
.tk{display:flex;white-space:nowrap;width:max-content;animation:tick 32s linear infinite;
font-family:'JetBrains Mono',monospace;font-size:9px;letter-spacing:.26em;color:var(--dim);padding:13px 0}
.tk b{color:var(--mut);font-weight:600}
.tk em{font-style:normal;color:var(--emb)}
.tk>span{padding-right:0}
@keyframes tick{to{transform:translateX(-50%)}}
#hero .center,#hero .drawer{will-change:transform,opacity}
#rail a.act .dt{transform:rotate(45deg) scale(1.25);transition:all .3s var(--ease)}

/* reduced-motion + static: everything visible, nothing moves */
@media (prefers-reduced-motion:reduce){
 .st,.u .zr,.bignum,.rv,.rvs,.folder .flip{opacity:1!important;transform:none!important}
 .wipe{clip-path:none!important}
 .pdraw,.garc,#philosophy .node svg *{stroke-dashoffset:0!important}
 #philosophy .node svg *{stroke-dasharray:none!important}
 .sigp::before,.sigp::after{width:17px!important;height:17px!important;opacity:1!important}
 .case .hairtop::before,.lessq::before{transform:none!important}
 .st .c,.st .o{transform:none!important}
 .u .zr .d2{transform:rotate(45deg)!important}
 .tk,.crawlp{animation:none!important}
}
body.static .st,body.static .zr,body.static .bignum,body.static .rv,body.static .rvs,body.static .folder .flip{opacity:1!important;transform:none!important}
body.static .wipe{clip-path:none!important}
body.static .pdraw,body.static #philosophy .node svg *{stroke-dashoffset:0!important}
body.static #philosophy .node svg *{stroke-dasharray:none!important}
body.static .sigp::before,body.static .sigp::after{width:17px!important;height:17px!important;opacity:1!important}
body.static .case .hairtop::before,body.static .lessq::before{transform:none!important}
body.static .st .c,body.static .st .o{transform:none!important}
body.static .zr .d2{transform:rotate(45deg)!important}
body.static .tk{animation:none!important}
"""
s=s.replace("</style>",CSS+"</style>",1)

# ============ 2. HTML surgical tweaks ============
# 2a. gauge numbers -> live counters
s=s.replace('<text x="40" y="45" text-anchor="middle" font-size="13.5" font-weight="700" fill="#F2F1ED">~20%</text>',
            '<text x="40" y="45" text-anchor="middle" font-size="13.5" font-weight="700" fill="#F2F1ED" class="cnt" data-n="20" data-pre="~" data-suf="%">~0%</text>')
s=s.replace('<text x="40" y="45" text-anchor="middle" font-size="13.5" font-weight="700" fill="#F2F1ED">7&ndash;8%</text>',
            '<text x="40" y="45" text-anchor="middle" font-size="13.5" font-weight="700" fill="#F2F1ED" class="cnt" data-n="8" data-suf="%" data-final="7–8%">0%</text>')
s=s.replace('<text x="40" y="45" text-anchor="middle" font-size="13.5" font-weight="700" fill="#F2F1ED">50%+</text>',
            '<text x="40" y="45" text-anchor="middle" font-size="13.5" font-weight="700" fill="#F2F1ED" class="cnt" data-n="50" data-suf="%+">0%+</text>')

# 2b. Oasis ring spokes -> line draw
a=s.index('CROSS-FUNCTIONAL LEADERSHIP'); b=s.index('</svg>',a)
seg=s[a:b]; cnt=[0]
def spoke(m):
    cnt[0]+=1
    return '<line class="pdraw" pathLength="1" style="--i:%d" '%(cnt[0]+2)+m.group(0)[6:]
seg=re.sub(r'<line x1="[\d.]+" y1="[\d.]+" x2="[\d.]+" y2="[\d.]+" stroke="#3A3D43" stroke-width="1"/>',
           lambda m:'<line class="pdraw" pathLength="1" style="--i:%d" %s'%(cnt.__setitem__(0,cnt[0]+1) or cnt[0]+2, m.group(0)[6:]), seg)
s=s[:a]+seg+s[b:]

# 2c. Eventer feedback loop -> living crawl (was broken pdraw+dasharray combo)
s=s.replace('<path class="pdraw" style="--i:5" pathLength="1" d="M444 70 C 496 34, 436 6, 260 6 L 176 6" fill="none" stroke="#8E8E93" stroke-width="1.1" stroke-dasharray="3 4"/>',
            '<path class="crawlp" d="M444 70 C 496 34, 436 6, 260 6 L 176 6" fill="none" stroke="#8E8E93" stroke-width="1.1" stroke-dasharray="3 4"/>')

# 2d. Medcoin revenue dash -> living crawl
s=s.replace('<line x1="930" y1="26" x2="1032" y2="26" stroke="#F4603E" stroke-width="2" stroke-dasharray="4 4"/>',
            '<line class="crawlp" x1="930" y1="26" x2="1032" y2="26" stroke="#F4603E" stroke-width="2" stroke-dasharray="4 4"/>')

# 2e. AI loop arrows pop in sequence
a=s.index('id="tech"'); b=s.index('CONTINUOUS COMMERCIAL LOOP',a)
seg=s[a:b]; k=[0]
def arr(m):
    k[0]+=1
    return '<path class="ndot" style="--i:%d" '%(k[0]+5)+m.group(0)[6:]
seg=re.sub(r'<path d="M[\d.]+ [\d.]+ l-4\.5 -6\.5 h9 z" fill="#F4603E"',
           lambda m:'<path class="ndot" style="--i:%d" %s'%(k.__setitem__(0,k[0]+1) or k[0]+5, m.group(0)[6:]), seg)
s=s[:a]+seg+s[b:]

# 2f. archive ticker after the case-files drawer
tick_txt=('FILE 01 <b>XTIX</b> — BUILT FROM ZERO <em>&#9670;</em> '
          'FILE 02 <b>OASIS</b> — LEADERSHIP <em>&#9670;</em> '
          'FILE 03 <b>EVENTER</b> — ALIGNMENT <em>&#9670;</em> '
          'FILE 04 <b>MEDCOIN</b> — FOUNDER <em>&#9670;</em> '
          'EXECUTIVE CASEBOOK &middot; 04 DOSSIERS &middot; 2018–2026 <em>&#9670;</em> ')
ticker='<div class="ticker rv" style="--i:5"><div class="tk"><span>'+tick_txt+'</span><span>'+tick_txt+'</span></div></div>'
old='</a>\n    </div>\n  </div>\n</section>\n\n<section class="sec case" id="xtix"'
assert old in s
s=s.replace(old,'</a>\n    </div>\n    '+ticker+'\n  </div>\n</section>\n\n<section class="sec case" id="xtix"',1)

# ============ 3. replace the whole script with the V2 engine ============
i0=s.index("<script>"); i1=s.index("</script>")+len("</script>")
JS="""<script>
(function(){
  var q=new URLSearchParams(location.search);
  var reduced=window.matchMedia('(prefers-reduced-motion: reduce)').matches;
  var isStatic=q.get('static')==='1';
  if(isStatic)document.body.classList.add('static');
  var only=q.get('only');
  if(only){document.querySelectorAll('.sec').forEach(function(x){if(x.id!==only)x.style.display='none'});}
  var g=q.get('goto');
  if(g){var ge=document.getElementById(g);if(ge){setTimeout(function(){window.scrollTo(0,ge.offsetTop-10)},60);}}

  /* ---------- choreography tagging ---------- */
  var units=[].slice.call(document.querySelectorAll('.rv,.folder>div:not(.flip),#tech .stacks,#tech .bot'));
  units.forEach(function(u){u.classList.add('u')});
  document.querySelectorAll('.sttl,#files .bigt,#statement .l1,#statement .l2,#hero h1').forEach(function(t){t.classList.add('wipe')});
  document.querySelectorAll('.list,.grid2c,.tools,.pgrid,.chips,#tech .stacks,#philosophy .grid').forEach(function(grp){
    [].forEach.call(grp.children,function(c,i){c.classList.add('st');c.style.setProperty('--i',i);});
  });
  ['.outs','#final .card'].forEach(function(sel){
    document.querySelectorAll(sel).forEach(function(par){
      var rs=par.querySelectorAll('tr,.crow');
      [].forEach.call(rs,function(r,i){r.classList.add('st');r.style.setProperty('--i',i);});
    });
  });
  document.querySelectorAll('.para,.then,.insight,.reality,.tech .pur,#tech .phil,.sigq').forEach(function(el){
    if(!el.classList.contains('st')){el.classList.add('st');if(!el.style.getPropertyValue('--i'))el.style.setProperty('--i',1);}
  });
  document.querySelectorAll('#philosophy .node svg').forEach(function(sv){
    [].forEach.call(sv.querySelectorAll('path,circle,rect'),function(p,i){
      try{p.setAttribute('pathLength','1')}catch(e){}
      p.style.setProperty('--pi',i);
    });
  });

  /* ---------- counters ---------- */
  function runCnt(el){
    if(el.dataset.done)return;el.dataset.done=1;
    var n=parseFloat(el.dataset.n||'0'),pre=el.dataset.pre||'',suf=el.dataset.suf||'',fin=el.dataset.final||'';
    function set(v){el.textContent=pre+v+suf}
    if(reduced||isStatic){if(fin){el.textContent=fin}else{set(n)}return}
    var t0=null,dur=1500;
    function step(ts){
      if(!t0)t0=ts;var p=Math.min(1,(ts-t0)/dur);p=1-Math.pow(1-p,3);
      set(Math.round(n*p));
      if(p<1){requestAnimationFrame(step)}else if(fin){el.textContent=fin}
    }
    requestAnimationFrame(step);
  }

  /* ---------- reveal engine ---------- */
  if(isStatic){
    units.forEach(function(u){u.classList.add('on')});
    document.querySelectorAll('.sec').forEach(function(x){x.classList.add('on')});
    document.querySelectorAll('.cnt').forEach(runCnt);
  }else{
    var io=new IntersectionObserver(function(es){
      es.forEach(function(e){
        if(e.isIntersecting){
          e.target.classList.add('on');
          e.target.querySelectorAll('.cnt').forEach(runCnt);
          io.unobserve(e.target);
        }
      });
    },{threshold:.2,rootMargin:'0px 0px -8% 0px'});
    units.forEach(function(u){io.observe(u)});
    document.querySelectorAll('#hero .rv').forEach(function(u){u.classList.add('on');u.querySelectorAll('.cnt').forEach(runCnt);});
  }

  /* ---------- rail + section state + progress color ---------- */
  var pbar=document.getElementById('pbar');
  var links=[].slice.call(document.querySelectorAll('#rail a'));
  var secs=links.map(function(a){return document.querySelector(a.getAttribute('href'))});
  var io2=new IntersectionObserver(function(es){
    es.forEach(function(e){
      if(e.isIntersecting){
        e.target.classList.add('on');
        var i=secs.indexOf(e.target);
        if(i>-1){
          links.forEach(function(a,j){a.classList.toggle('act',j===i)});
          var fc=getComputedStyle(e.target).getPropertyValue('--fc').trim();
          pbar.style.background=fc||'#F4603E';
        }
      }
    });
  },{threshold:.22});
  secs.forEach(function(x){if(x)io2.observe(x)});

  /* ---------- scroll: progress + hero parallax fade ---------- */
  var hero=document.getElementById('hero');
  var hc=hero.querySelector('.center'),hd=hero.querySelector('.drawer'),hcue=hero.querySelector('.cue');
  var tick=false;
  function onScroll(){
    if(tick)return;tick=true;
    requestAnimationFrame(function(){
      tick=false;
      var h=document.documentElement,y=h.scrollTop;
      pbar.style.width=(y/(h.scrollHeight-h.clientHeight)*100)+'%';
      if(!reduced&&!isStatic){
        var vh=window.innerHeight,p=Math.min(1,y/(vh*.85));
        hc.style.opacity=1-p*.92;
        hc.style.transform='translateY('+(-y*.16)+'px)';
        if(hd){hd.style.opacity=1-p;hd.style.transform='translateY('+(-y*.07)+'px)';}
        if(hcue){hcue.style.opacity=1-p*2;}
      }
    });
  }
  window.addEventListener('scroll',onScroll,{passive:true});
  onScroll();
})();
</script>"""
s=s[:i0]+JS+s[i1:]

io.open("site.html","w",encoding="utf-8").write(s)
print("MOTION V2 applied:",len(s),"bytes")
