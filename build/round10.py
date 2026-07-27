# -*- coding: utf-8 -*-
# Round 10 — the living layer goes into the site: volume, hops, parallax, float,
# page-turn, sweep. Motion is site-only; the PDF stays as printed.
import io, re

LOG = []
def op(name, fn, s):
    try:
        out = fn(s)
        if out is None or out == s:
            LOG.append(' SKIP  ' + name); return s
        LOG.append(' OK    ' + name); return out
    except Exception as e:
        LOG.append(' ERR   %s :: %s' % (name, str(e)[:110])); return s

def css_end(add):
    def f(s):
        k = s.rfind('</style>')
        return s[:k] + add + '\n' + s[k:]
    return f

s = io.open('site.html', encoding='utf-8').read()

# ---------------- 1 + 7 : volume and the light sweep ----------------
VOLUME = """
/* ============ R10 — VOLUME: folders behave like physical objects ============ */
@property --sx{syntax:'<length>';inherits:true;initial-value:-320px}
.hfolder,#hero .mfold{filter:drop-shadow(13px 17px 0 rgba(9,10,13,.55))}
/* paper peeking out of the folder, clear of the tab head */
.hfolder::before,#hero .mfold::before{content:"";position:absolute;top:-13px;left:38%;right:7%;height:15px;
  background:#EDECE6;border-top:5px solid #D6D4CC;border-radius:3px 9px 0 0;z-index:0}
/* the thickness of the card itself */
.hfolder::after,#hero .mfold::after{content:"";position:absolute;left:0;right:0;bottom:-7px;height:7px;
  background:rgba(25,26,31,.34);border-radius:0 0 20px 20px;z-index:0}
#hero .mfold::after{bottom:-8px;height:8px;border-radius:0 0 22px 22px}
#hero .mfold::before{left:52%;right:9%}
/* one sweep, one clock: the tab head and the body read the same position */
.hfolder,.hfolder .hlip,#hero .mfold{
  background-image:linear-gradient(104deg,transparent 42%,rgba(255,255,255,.13) 50%,transparent 58%);
  background-repeat:no-repeat;background-size:200px 320%;background-position:var(--sx) center}
.hfolder,#hero .mfold{animation:sweepx 7.5s ease-in-out infinite}
@keyframes sweepx{0%{--sx:-320px}46%{--sx:1500px}100%{--sx:1500px}}
#hero .mfold{animation-delay:1.2s}
.hcard:nth-child(2) .hfolder{animation-delay:.9s}
.hcard:nth-child(3) .hfolder{animation-delay:1.8s}
.hcard:nth-child(4) .hfolder{animation-delay:2.7s}
"""

# ---------------- 5 : the cover breathes ----------------
FLOAT = """
/* ============ R10 — the cover is an object on a desk ============ */
#hero .mfold.on{animation:sweepx 7.5s ease-in-out 1.2s infinite,hfloat 7.5s ease-in-out infinite}
@keyframes hfloat{0%,100%{transform:translateY(0)}50%{transform:translateY(-13px)}}
#hero .itab{animation:hfloat 7.5s ease-in-out infinite}
#hero .itab:nth-child(2){animation-delay:.12s}
#hero .itab:nth-child(3){animation-delay:.24s}
#hero .itab:nth-child(4){animation-delay:.36s}
"""

# ---------------- 6 : the drawer turns like pages ----------------
TURN_CSS = """
/* ============ R10 — a case turns away as it leaves ============ */
.hcard{perspective:1500px}
.hfolder{transform-origin:left center;
  transform:rotateY(var(--ry,0deg)) scale(var(--sc,.94));backface-visibility:hidden}
"""

def turn_js(t):
    old = "hcards[i].style.setProperty('--sc',String(1.02-Math.min(.1,d*.22)));"
    if old not in t: return None
    new = ("hcards[i].style.setProperty('--sc',String(1.02-Math.min(.1,d*.22)));\n"
           "        var sd=(r.left+r.width/2-cx)/window.innerWidth;\n"
           "        var ry=sd<-.12?Math.max(-68,(sd+.12)*190):0;\n"
           "        hcards[i].style.setProperty('--ry',ry.toFixed(1)+'deg');")
    return t.replace(old, new, 1)

# ---------------- 3 : the signal hops the wires ----------------
def hops(t):
    i = t.find('id="tech"')
    if i < 0: return None
    j = t.find('</section>', i)
    seg = t[i:j]
    xs = re.findall(r'<line class="pdraw" pathLength="1" style="--i:\d+" x1="(\d+)" y1="45" x2="(\d+)" y2="45"', seg)
    if len(xs) < 5: return None
    dots = ''.join('<circle class="hop h%d" cx="%s" cy="45" r="3.4" fill="#2FB380"/>' % (n, a)
                   for n, (a, b) in enumerate(xs))
    k = seg.rfind('</svg>')
    seg = seg[:k] + dots + seg[k:]
    return t[:i] + seg + t[j:]

HOPS_CSS = """
/* ============ R10 — the signal hops wire to wire ============ */
#tech .hop{opacity:0}
#tech .h0{animation:hopx 5s cubic-bezier(.5,0,.5,1) infinite}
#tech .h1{animation:hopx 5s cubic-bezier(.5,0,.5,1) .62s infinite}
#tech .h2{animation:hopx 5s cubic-bezier(.5,0,.5,1) 1.24s infinite}
#tech .h3{animation:hopx 5s cubic-bezier(.5,0,.5,1) 1.86s infinite}
#tech .h4{animation:hopx 5s cubic-bezier(.5,0,.5,1) 2.48s infinite}
@keyframes hopx{0%{opacity:0;transform:translateX(0)}
  3%{opacity:1;transform:translateX(0)}
  11%{opacity:1;transform:translateX(22px)}
  13%{opacity:0;transform:translateX(22px)}
  100%{opacity:0;transform:translateX(22px)}}
#tech .archw .pdraw{transition:opacity .3s linear}
"""

# ---------------- 4 : background parallax, eased ----------------
PARALLAX_CSS = """
/* ============ R10 — the background sits behind the page, not on it ============ */
.secnum,#heromq{transform:translate3d(var(--pxx,0px),var(--pyy,0px),0);will-change:transform}
"""

PARALLAX_JS = """
<script>
/* R10 — pointer parallax, eased in a single frame loop (no jitter) */
(function(){
  if(matchMedia('(prefers-reduced-motion:reduce)').matches)return;
  if(document.body.classList.contains('static'))return;
  var layers=[];
  [['#heromq',18],['.secnum',30]].forEach(function(p){
    [].forEach.call(document.querySelectorAll(p[0]),function(el){layers.push({el:el,d:p[1],x:0,y:0})});
  });
  if(!layers.length)return;
  var tx=0,ty=0,run=false;
  addEventListener('pointermove',function(e){
    tx=(e.clientX/innerWidth-.5); ty=(e.clientY/innerHeight-.5);
    if(!run){run=true;requestAnimationFrame(loop)}
  },{passive:true});
  function loop(){
    var moving=false;
    for(var i=0;i<layers.length;i++){
      var L=layers[i], gx=-tx*L.d, gy=-ty*L.d*.42;
      L.x+=(gx-L.x)*.075; L.y+=(gy-L.y)*.075;
      if(Math.abs(gx-L.x)>.06||Math.abs(gy-L.y)>.06)moving=true;
      L.el.style.setProperty('--pxx',L.x.toFixed(2)+'px');
      L.el.style.setProperty('--pyy',L.y.toFixed(2)+'px');
    }
    if(moving){requestAnimationFrame(loop)}else{run=false}
  }
})();
</script>
"""

# ---------------- safety: every new motion respects the kill switches ----------------
KILL = """
/* R10 — kill switches keep working */
body.static .hfolder,body.static #hero .mfold,body.static #hero .mfold.on,body.static #hero .itab,
body.failsafe .hfolder,body.failsafe #hero .mfold,body.failsafe #hero .mfold.on,body.failsafe #hero .itab,
body.static #tech .hop,body.failsafe #tech .hop{animation:none!important}
body.static .hfolder,body.static #hero .mfold{--sx:-320px}
@media (prefers-reduced-motion:reduce){
  .hfolder,#hero .mfold,#hero .mfold.on,#hero .itab,#tech .hop{animation:none!important}
  .secnum,#heromq{transform:none!important}
}
@media (max-width:860px){
  .hfolder,#hero .mfold{filter:none}
  .hfolder::before,#hero .mfold::before{display:none}
  .hcard{perspective:none}
  .hfolder{transform:scale(var(--sc,1))!important}
}
"""

s = op('1+7 volume and sweep', css_end(VOLUME), s)
s = op('5 cover float', css_end(FLOAT), s)
s = op('6 page-turn css', css_end(TURN_CSS), s)
s = op('6 page-turn in the drawer loop', turn_js, s)
s = op('3 hop dots in the chain', hops, s)
s = op('3 hop css', css_end(HOPS_CSS), s)
s = op('4 parallax css', css_end(PARALLAX_CSS), s)
s = op('kill switches', css_end(KILL), s)

def add_js(t):
    k = t.rfind('</script>')
    return t[:k + 9] + '\n' + PARALLAX_JS.strip() + t[k + 9:]
s = op('4 parallax loop', add_js, s)

io.open('site.html', 'w', encoding='utf-8', newline='').write(s)
head = ('<!doctype html>\n<html lang="en">\n<head>\n<meta charset="utf-8">\n'
        '<meta name="viewport" content="width=device-width,initial-scale=1">\n'
        '<meta name="color-scheme" content="dark">\n</head>\n<body>\n')
io.open('site_standalone.html', 'w', encoding='utf-8', newline='').write(head + s + '\n</body>\n</html>')
LOG.append('site %d bytes | standalone rebuilt' % len(s.encode('utf-8')))
print('\n'.join(LOG))
