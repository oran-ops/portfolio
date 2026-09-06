# -*- coding: utf-8 -*-
"""Build lab/iso.html — the renderer, proven end to end.

Deliberately plain. Its whole job is to answer four questions that cannot be answered by
reading code:

  does the projection actually tile, with no seam and no overlap
  does the painter's order hold when a tall block stands behind a short one
  does hit-testing invert the projection under a real pointer
  do integer scales stay pixel-crisp on a high-DPI screen, and does a fractional one not

Everything is inlined, so the page makes no request — the same rule the portfolio lives under.
"""
import base64
import io
import json
import os
import sys

sys.stdout.reconfigure(encoding='utf-8', errors='replace')
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
KIT = os.path.join(ROOT, 'src', 'kit')
OUT = os.path.join(ROOT, 'lab', 'iso.html')

sheet = base64.b64encode(io.open(os.path.join(KIT, 'sprites.png'), 'rb').read()).decode()
atlas = io.open(os.path.join(KIT, 'sprites.json'), encoding='utf-8').read()
isojs = io.open(os.path.join(KIT, 'iso.js'), encoding='utf-8').read()

HTML = """<!doctype html>
<html lang="en"><head><meta charset="utf-8">
<meta name="viewport" content="width=device-width,initial-scale=1">
<title>iso lab</title>
<style>
 html,body{margin:0;background:#191A1F;color:#B6B7BB;
   font:13px/1.5 ui-monospace,Menlo,Consolas,monospace}
 .bar{padding:8px 12px;border-bottom:1px solid #33353C;display:flex;gap:14px;flex-wrap:wrap;
   align-items:center}
 button{background:#25262D;color:#F2F1ED;border:1px solid #4B4E55;padding:3px 9px;
   font:inherit;cursor:pointer}
 button[aria-pressed="true"]{background:#2FB380;color:#191A1F;border-color:#2FB380}
 canvas{display:block;image-rendering:pixelated;cursor:crosshair}
 #out{padding:8px 12px;border-top:1px solid #33353C;white-space:pre}
 b{color:#F2F1ED;font-weight:400}
</style></head><body>
<div class="bar">
  <span>scale</span>
  <button data-s="1">1x</button><button data-s="2">2x</button><button data-s="3">3x</button>
  <button data-s="1.5">1.5x</button>
  <span style="color:#4B4E55">|</span>
  <button id="grid" aria-pressed="false">tile grid</button>
  <button id="sortoff" aria-pressed="false">break the sort</button>
</div>
<canvas id="c"></canvas>
<div id="out">click a tile</div>
<script>__ISO__</script>
<script>
(function(){
'use strict';
var ATLAS = __ATLAS__;
var sheet = new Image();
var SCALE = 2, GRID = false, SORTOFF = false, hover = null;
var cv = document.getElementById('c'), ctx = cv.getContext('2d');
var out = document.getElementById('out');

/* the route between the four stops. Only the coordinates are stored — which of the sixteen
   path tiles to draw is derived, which is the whole point of a bitmask set. */
var ROUTE = [[1,7],[2,7],[3,7],[3,6],[3,5],[4,5],[5,5],[5,4],[5,3],[6,3],[7,3],[7,2],
             [8,2],[9,2],[9,3],[9,4],[10,4],[11,4],[11,5],[11,6],[12,6]];
var STOPS = [[1,7,'xtix'],[5,3,'oasis'],[9,2,'eventer'],[12,6,'medcoin']];
var inRoute = {};
ROUTE.forEach(function(p){ inRoute[p[0]+','+p[1]] = true; });

function mask(x,y){
  /* bit 0 +x, 1 -x, 2 +y, 3 -y — the same order the generator drew them in */
  return (inRoute[(x+1)+','+y]?1:0) | (inRoute[(x-1)+','+y]?2:0)
       | (inRoute[x+','+(y+1)]?4:0) | (inRoute[x+','+(y-1)]?8:0);
}

function scene(){
  var list = [];
  for(var y=0;y<10;y++) for(var x=0;x<14;x++){
    list.push({x:x, y:y, z:0, n: inRoute[x+','+y] ? 'path'+('0'+mask(x,y)).slice(-2)
                                                  : 'ground'+((x*7+y*3)%4)});
  }
  STOPS.forEach(function(s){ list.push({x:s[0], y:s[1], z:0, n:'stop_'+s[2]}); });
  /* two blocks placed to expose a wrong sort: a tall one behind a short one in front */
  list.push({x:3, y:1, z:0, n:'marker'});
  list.push({x:6, y:8, z:0, n:'marker'});
  return list;
}

function draw(){
  var dpr = Math.max(1, Math.floor(window.devicePixelRatio||1));
  var W = Math.min(980, window.innerWidth), H = 460;
  cv.style.width = W+'px'; cv.style.height = H+'px';
  cv.width = W*dpr; cv.height = H*dpr;
  ctx.setTransform(dpr,0,0,dpr,0,0);
  ctx.imageSmoothingEnabled = false;
  ctx.fillStyle = '#191A1F'; ctx.fillRect(0,0,W,H);

  var ox = W/2, oy = 70;
  ctx.save(); ctx.translate(ox,oy); ctx.scale(SCALE,SCALE);

  var list = scene();
  if(!SORTOFF) list = iso.sort(list);
  list.forEach(function(s){ iso.blit(ctx, ATLAS, sheet, s.n, s.x, s.y, s.z); });

  if(GRID){
    ctx.strokeStyle = 'rgba(47,179,128,.45)'; ctx.lineWidth = 1/SCALE;
    for(var y=0;y<10;y++) for(var x=0;x<14;x++){
      var p = iso.project(x,y,0);
      ctx.beginPath();
      ctx.moveTo(p.sx, p.sy-16); ctx.lineTo(p.sx+32, p.sy);
      ctx.lineTo(p.sx, p.sy+16); ctx.lineTo(p.sx-32, p.sy);
      ctx.closePath(); ctx.stroke();
    }
  }
  if(hover){
    var q = iso.project(hover.tx, hover.ty, 0);
    ctx.fillStyle = 'rgba(242,241,237,.30)';
    ctx.beginPath();
    ctx.moveTo(q.sx, q.sy-16); ctx.lineTo(q.sx+32, q.sy);
    ctx.lineTo(q.sx, q.sy+16); ctx.lineTo(q.sx-32, q.sy);
    ctx.closePath(); ctx.fill();
  }
  ctx.restore();

  out.innerHTML = 'scale <b>'+SCALE+'x</b>   dpr <b>'+dpr+'</b>   backing store <b>'
    + cv.width+'x'+cv.height+'</b>   sprites <b>'+list.length+'</b>'
    + (SCALE % 1 ? '   <b style="color:#E0A458">fractional scale - look at the tile edges</b>' : '')
    + (SORTOFF ? '   <b style="color:#E0A458">sort off - the far blocks now cover the near ones</b>' : '')
    + (hover ? '\\n\\nclicked tile <b>'+hover.tx+','+hover.ty+'</b>'
             + '   path mask <b>'+(inRoute[hover.tx+','+hover.ty]?mask(hover.tx,hover.ty):'-')+'</b>'
      : '\\n\\nclick a tile');
}

cv.addEventListener('click', function(e){
  var r = cv.getBoundingClientRect();
  var W = Math.min(980, window.innerWidth);
  hover = iso.hit((e.clientX-r.left-W/2)/SCALE, (e.clientY-r.top-70)/SCALE);
  draw();
});
document.querySelectorAll('[data-s]').forEach(function(b){
  b.addEventListener('click', function(){
    SCALE = parseFloat(b.dataset.s);
    document.querySelectorAll('[data-s]').forEach(function(o){
      o.setAttribute('aria-pressed', o===b ? 'true' : 'false'); });
    draw();
  });
});
document.getElementById('grid').addEventListener('click', function(){
  GRID=!GRID; this.setAttribute('aria-pressed',GRID); draw(); });
document.getElementById('sortoff').addEventListener('click', function(){
  SORTOFF=!SORTOFF; this.setAttribute('aria-pressed',SORTOFF); draw(); });
window.addEventListener('resize', draw);

sheet.onload = function(){
  document.querySelector('[data-s="2"]').setAttribute('aria-pressed','true');
  draw();
};
sheet.src = 'data:image/png;base64,__SHEET__';
})();
</script></body></html>
"""

html = (HTML.replace('__ISO__', isojs)
            .replace('__ATLAS__', atlas)
            .replace('__SHEET__', sheet))
os.makedirs(os.path.dirname(OUT), exist_ok=True)
io.open(OUT, 'w', encoding='utf-8', newline='').write(html)
print('wrote lab/iso.html  (%d KB, no external requests)' % (len(html.encode()) // 1024))
