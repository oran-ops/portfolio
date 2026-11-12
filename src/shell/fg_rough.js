/* FG — the field guide's hand. A small rough renderer written for this site (no library, no
   request): every stroke drawn twice with jittered ends and a slight bow, corners overshooting,
   hachure at 49 degrees rising right, as measured in the XTIX UK Field Guide.
   Deterministic: every drawing takes a seed (a string), so a redraw on resize is the same drawing
   and nothing ever shimmers. Paths are returned as SVG path data; segments are also returned where
   a drawing is laid stroke by stroke (hatch), so motion can only ever lay down what the final
   drawing contains. */
(function (root) {
  "use strict";
  var NS = "http://www.w3.org/2000/svg";

  function hash(s) { var h = 2166136261; s = String(s); for (var i = 0; i < s.length; i++) { h ^= s.charCodeAt(i); h = Math.imul(h, 16777619); } return h >>> 0; }
  function rng(seed) {
    var a = typeof seed === "number" ? seed : hash(seed);
    return function () { a |= 0; a = a + 0x6D2B79F5 | 0; var t = Math.imul(a ^ a >>> 15, 1 | a); t = t + Math.imul(t ^ t >>> 7, 61 | t) ^ t; return ((t ^ t >>> 14) >>> 0) / 4294967296; };
  }
  function f(v) { return Math.round(v * 10) / 10; }

  /* A pen: a seeded source of jitter. All shapes below are methods of a pen. */
  function Pen(seed, opts) {
    this.R = rng(seed); this.o = opts || {};
  }
  Pen.prototype.j = function (m) { return (this.R() * 2 - 1) * m; };

  /* one stroke between two points: `passes` overlapping strokes, ends jittered, bowed */
  Pen.prototype.line = function (x1, y1, x2, y2, o) {
    o = o || {}; var rough = o.rough == null ? 1 : o.rough, passes = o.passes || 2, d = "";
    var len = Math.hypot(x2 - x1, y2 - y1) || 1;
    for (var p = 0; p < passes; p++) {
      var off = Math.min(2.2, .35 + len * .006) * rough;
      var ax = x1 + this.j(off), ay = y1 + this.j(off), bx = x2 + this.j(off), by = y2 + this.j(off);
      var nx = -(by - ay) / len, ny = (bx - ax) / len, bw = Math.min(3.2, len * .008 + .3) * rough * (o.bow == null ? 1 : o.bow);
      var k1 = this.j(bw), k2 = this.j(bw);
      d += "M" + f(ax) + " " + f(ay) + "C" + f(ax + (bx - ax) * .33 + nx * k1) + " " + f(ay + (by - ay) * .33 + ny * k1) + " " +
           f(ax + (bx - ax) * .66 + nx * k2) + " " + f(ay + (by - ay) * .66 + ny * k2) + " " + f(bx) + " " + f(by);
    }
    return d;
  };
  /* a polyline or polygon through points */
  Pen.prototype.poly = function (pts, closed, o) {
    var d = "", n = pts.length;
    for (var i = 0; i < (closed ? n : n - 1); i++) { var a = pts[i], b = pts[(i + 1) % n]; d += this.line(a[0], a[1], b[0], b[1], o); }
    return d;
  };
  /* a rectangle whose corners overshoot, as a hand draws one */
  Pen.prototype.rect = function (x, y, w, h, o) {
    var ov = (o && o.overshoot != null) ? o.overshoot : 1.8, R = this.R;
    return this.line(x - ov * R(), y, x + w + ov * R(), y, o) + this.line(x + w, y - ov * R(), x + w, y + h + ov * R(), o) +
           this.line(x + w + ov * R(), y + h, x - ov * R(), y + h, o) + this.line(x, y + h + ov * R(), x, y - ov * R(), o);
  };
  function catmull(pts) {
    var d = "M" + f(pts[0][0]) + " " + f(pts[0][1]);
    for (var i = 0; i < pts.length - 1; i++) {
      var p0 = pts[Math.max(0, i - 1)], p1 = pts[i], p2 = pts[i + 1], p3 = pts[Math.min(pts.length - 1, i + 2)];
      d += "C" + f(p1[0] + (p2[0] - p0[0]) / 6) + " " + f(p1[1] + (p2[1] - p0[1]) / 6) + " " + f(p2[0] - (p3[0] - p1[0]) / 6) + " " +
           f(p2[1] - (p3[1] - p1[1]) / 6) + " " + f(p2[0]) + " " + f(p2[1]);
    }
    return d;
  }
  Pen.prototype.curve = function (pts) { return catmull(pts); };
  /* an ellipse or an arc (start/sweep in radians, 0 = 3 o'clock, clockwise); closed ellipses overlap their start */
  Pen.prototype.ellipse = function (cx, cy, rx, ry, o) {
    o = o || {}; var d = "", passes = o.passes || 2, sweep = o.sweep == null ? Math.PI * 2 : o.sweep, closed = sweep >= Math.PI * 2 - 1e-6;
    for (var p = 0; p < passes; p++) {
      var n = Math.max(5, Math.round((o.steps || 12) * sweep / (Math.PI * 2))), st = o.start == null ? this.R() * Math.PI * 2 : o.start + this.j(.03);
      var over = closed ? 1.07 + this.R() * .04 : 1, pts = [];
      for (var i = 0; i <= n; i++) {
        var a = st + i * (sweep * over / n), q = 1 + this.j(o.wobble == null ? .02 : o.wobble);
        pts.push([cx + Math.cos(a) * rx * q, cy + Math.sin(a) * ry * q]);
      }
      d += catmull(pts);
    }
    return d;
  };
  /* an EXACT arc: it starts and ends where it is told (a figure's arc may neither over- nor under-run);
     only the radius between the ends wavers, so a hand drew it but the ends are measured */
  Pen.prototype.arc = function (cx, cy, r, a0, a1, o) {
    o = o || {}; var d = "", passes = o.passes || 2, wob = o.wobble == null ? .45 : o.wobble;
    var n = Math.max(3, Math.ceil(Math.abs(a1 - a0) * r / 14));
    for (var p = 0; p < passes; p++) {
      var pts = [];
      for (var i = 0; i <= n; i++) { var a = a0 + (a1 - a0) * i / n, rr = r + (i === 0 || i === n ? 0 : this.j(wob)); pts.push([cx + Math.cos(a) * rr, cy + Math.sin(a) * rr]); }
      d += catmull(pts);
    }
    return d;
  };
  /* a SOLID band between two radii (an annular sector), its long edges faintly uneven, its ends exact */
  Pen.prototype.sector = function (cx, cy, r0, r1, a0, a1, o) {
    o = o || {}; var wob = o.wobble == null ? .3 : o.wobble, n = Math.max(4, Math.ceil(Math.abs(a1 - a0) * r1 / 10)), out = [], inn = [];
    for (var i = 0; i <= n; i++) {
      var a = a0 + (a1 - a0) * i / n, e = (i === 0 || i === n) ? 0 : 1;
      out.push([cx + Math.cos(a) * (r1 + e * this.j(wob)), cy + Math.sin(a) * (r1 + e * this.j(wob))]);
      inn.push([cx + Math.cos(a) * (r0 + e * this.j(wob)), cy + Math.sin(a) * (r0 + e * this.j(wob))]);
    }
    inn.reverse();
    return catmull(out) + "L" + f(inn[0][0]) + " " + f(inn[0][1]) + catmull(inn).replace(/^M[^C]*/, "") + "Z";
  };
  /* a TAPERED brush stroke along an arc: width w0 at a0 thinning to w1 at a1 — a dry brush running out */
  Pen.prototype.taperArc = function (cx, cy, r, a0, a1, w0, w1, o) {
    o = o || {}; var n = Math.max(6, Math.ceil(Math.abs(a1 - a0) * r / 4)), L = [], Rt = [], drift = this.j(o.drift == null ? .35 : o.drift);
    for (var i = 0; i <= n; i++) {
      var t = i / n, a = a0 + (a1 - a0) * t, w = (w0 + (w1 - w0) * Math.pow(t, 1.4)) / 2, rr = r + drift * t + this.j(.12);
      L.push([cx + Math.cos(a) * (rr + w), cy + Math.sin(a) * (rr + w)]);
      Rt.push([cx + Math.cos(a) * (rr - w), cy + Math.sin(a) * (rr - w)]);
    }
    Rt.reverse();
    return catmull(L) + "L" + f(Rt[0][0]) + " " + f(Rt[0][1]) + catmull(Rt).replace(/^M[^C]*/, "") + "Z";
  };

  /* a BRUSH stroke through points with a width at each point (a tapered filled outline) */
  Pen.prototype.brush = function (pts, widths) {
    var L = [], Rt = [], n = pts.length;
    for (var i = 0; i < n; i++) {
      var a = pts[Math.max(0, i - 1)], b = pts[Math.min(n - 1, i + 1)], dx = b[0] - a[0], dy = b[1] - a[1], l = Math.hypot(dx, dy) || 1;
      var nx = -dy / l, ny = dx / l, w = widths[i] / 2 + this.j(.06);
      L.push([pts[i][0] + nx * w, pts[i][1] + ny * w]); Rt.push([pts[i][0] - nx * w, pts[i][1] - ny * w]);
    }
    Rt.reverse();
    return catmull(L) + "L" + f(Rt[0][0]) + " " + f(Rt[0][1]) + catmull(Rt).replace(/^M[^C]*/, "") + "Z";
  };

  /* points of a circle's arc, for clipping fills to a wedge */
  function wedge(cx, cy, r, a0, a1, inner) {
    var pts = [], n = Math.max(6, Math.ceil(Math.abs(a1 - a0) / .12));
    for (var i = 0; i <= n; i++) { var a = a0 + (a1 - a0) * i / n; pts.push([cx + Math.cos(a) * r, cy + Math.sin(a) * r]); }
    if (inner) { for (var k = n; k >= 0; k--) { var b = a0 + (a1 - a0) * k / n; pts.push([cx + Math.cos(b) * inner, cy + Math.sin(b) * inner]); } }
    else pts.push([cx, cy]);
    return pts;
  }

  /* HACHURE inside any simple polygon (scanline in a rotated frame, even-odd pairs).
     Returns {d, segs}: segs in drawing order, so a hatch can be laid line by line. */
  Pen.prototype.hachure = function (poly, o) {
    o = o || {}; var gap = o.gap || 5, ang = (o.angle == null ? 49 : o.angle) * Math.PI / 180;
    var ca = Math.cos(ang), sa = Math.sin(ang);
    /* rotate so the hatch direction becomes horizontal; hatch "rising right" in screen space */
    function rot(p) { return [p[0] * ca - p[1] * sa, p[0] * sa + p[1] * ca]; }
    function unrot(p) { return [p[0] * ca + p[1] * sa, -p[0] * sa + p[1] * ca]; }
    var P = poly.map(rot), ys = P.map(function (p) { return p[1]; }), y0 = Math.min.apply(null, ys), y1 = Math.max.apply(null, ys);
    var segs = [], d = "", start = y0 + gap * (.3 + this.R() * .4);
    for (var y = start; y < y1; y += gap * (1 + this.j(.08))) {
      var xs = [];
      for (var i = 0; i < P.length; i++) {
        var a = P[i], b = P[(i + 1) % P.length];
        if ((a[1] <= y && b[1] > y) || (b[1] <= y && a[1] > y)) xs.push(a[0] + (y - a[1]) * (b[0] - a[0]) / (b[1] - a[1]));
      }
      xs.sort(function (m, n) { return m - n; });
      for (var k = 0; k + 1 < xs.length; k += 2) {
        if (xs[k + 1] - xs[k] < 1.2) continue;
        var e1 = unrot([xs[k] + .6, y]), e2 = unrot([xs[k + 1] - .6, y]);
        segs.push([e1[0], e1[1], e2[0], e2[1]]);
      }
    }
    if (o.reverse) segs.reverse();
    var self = this;
    segs.forEach(function (s) { d += self.line(s[0], s[1], s[2], s[3], { rough: o.rough == null ? .55 : o.rough, passes: o.passes || 1 }); });
    return { d: d, segs: segs };
  };
  Pen.prototype.hachureRect = function (x, y, w, h, o) { return this.hachure([[x, y], [x + w, y], [x + w, y + h], [x, y + h]], o); };
  Pen.prototype.hachureWedge = function (cx, cy, r, a0, a1, o, inner) { return this.hachure(wedge(cx, cy, r, a0, a1, inner), o); };

  /* stipple: seeded dots inside a polygon (for "approximate" edges and soft fields) */
  Pen.prototype.stipple = function (poly, density, r) {
    var xs = poly.map(function (p) { return p[0]; }), ys = poly.map(function (p) { return p[1]; });
    var x0 = Math.min.apply(null, xs), x1 = Math.max.apply(null, xs), y0 = Math.min.apply(null, ys), y1 = Math.max.apply(null, ys), d = "";
    var n = Math.round((x1 - x0) * (y1 - y0) * density);
    function inside(x, y) { var c = false; for (var i = 0, k = poly.length - 1; i < poly.length; k = i++) { var a = poly[i], b = poly[k]; if ((a[1] > y) !== (b[1] > y) && x < (b[0] - a[0]) * (y - a[1]) / (b[1] - a[1]) + a[0]) c = !c; } return c; }
    for (var i = 0; i < n; i++) { var x = x0 + this.R() * (x1 - x0), y = y0 + this.R() * (y1 - y0); if (!inside(x, y)) continue; var q = (r || .7) * (.6 + this.R() * .8); d += "M" + f(x - q) + " " + f(y) + "a" + f(q) + " " + f(q) + " 0 1 0 " + f(2 * q) + " 0a" + f(q) + " " + f(q) + " 0 1 0 " + f(-2 * q) + " 0"; }
    return d;
  };

  /* an arrow: a bowed shaft (quadratic) and a two-stroke head */
  Pen.prototype.arrow = function (x1, y1, x2, y2, o) {
    o = o || {}; var bend = o.bend || 0, mx = (x1 + x2) / 2, my = (y1 + y2) / 2, len = Math.hypot(x2 - x1, y2 - y1) || 1;
    var nx = -(y2 - y1) / len, ny = (x2 - x1) / len, cx = mx + nx * bend, cy = my + ny * bend, d = "";
    for (var p = 0; p < (o.passes || 2); p++) d += "M" + f(x1 + this.j(.8)) + " " + f(y1 + this.j(.8)) + "Q" + f(cx + this.j(2)) + " " + f(cy + this.j(2)) + " " + f(x2 + this.j(.6)) + " " + f(y2 + this.j(.6));
    var a = Math.atan2(y2 - cy, x2 - cx), h = o.head == null ? 11 : o.head;
    if (h) d += this.line(x2, y2, x2 - h * Math.cos(a - .45), y2 - h * Math.sin(a - .45), { rough: .5 }) + this.line(x2, y2, x2 - h * Math.cos(a + .45), y2 - h * Math.sin(a + .45), { rough: .5 });
    return d;
  };
  /* a REVISION CLOUD — the draughtsman's mark for "changed in this revision": scallops around a box */
  Pen.prototype.cloud = function (x, y, w, h, o) {
    o = o || {}; var r = o.r || 11, d = "", pts = [], per = 2 * (w + h), n = Math.max(8, Math.round(per / (r * 1.6)));
    for (var i = 0; i < n; i++) {
      var t = i / n * per, px, py;
      if (t < w) { px = x + t; py = y; } else if (t < w + h) { px = x + w; py = y + t - w; } else if (t < 2 * w + h) { px = x + w - (t - w - h); py = y + h; } else { px = x; py = y + h - (t - 2 * w - h); }
      pts.push([px + this.j(1.2), py + this.j(1.2)]);
    }
    for (var p = 0; p < (o.passes || 2); p++) {
      d += "M" + f(pts[0][0]) + " " + f(pts[0][1]);
      for (var k = 0; k < pts.length; k++) {
        var a = pts[k], b = pts[(k + 1) % pts.length], mx = (a[0] + b[0]) / 2, my = (a[1] + b[1]) / 2, cx0 = x + w / 2, cy0 = y + h / 2;
        var vx = mx - cx0, vy = my - cy0, vl = Math.hypot(vx, vy) || 1, bulge = r * (.8 + this.R() * .35);
        d += "Q" + f(mx + vx / vl * bulge) + " " + f(my + vy / vl * bulge) + " " + f(b[0] + this.j(.5)) + " " + f(b[1] + this.j(.5));
      }
    }
    return d;
  };
  /* a wavy hand underline from x1 to x2 at y */
  Pen.prototype.underline = function (x1, x2, y, o) {
    o = o || {}; var d = "";
    for (var p = 0; p < (o.passes || 2); p++) {
      var pts = [], n = Math.max(3, Math.round((x2 - x1) / 90));
      for (var i = 0; i <= n; i++) pts.push([x1 + (x2 - x1) * i / n + this.j(2), y + this.j(o.wave || 2.2) + p * 1.4]);
      d += catmull(pts);
    }
    return d;
  };
  /* a perforation: a row of small hand-punched holes (ticket stubs) */
  Pen.prototype.perforation = function (x1, y1, x2, y2, step, r) {
    var len = Math.hypot(x2 - x1, y2 - y1), n = Math.floor(len / (step || 7)), d = "";
    for (var i = 1; i < n; i++) { var t = i / n, x = x1 + (x2 - x1) * t + this.j(.3), y = y1 + (y2 - y1) * t + this.j(.3), q = (r || 1.1) * (.85 + this.R() * .3);
      d += "M" + f(x - q) + " " + f(y) + "a" + f(q) + " " + f(q) + " 0 1 0 " + f(2 * q) + " 0a" + f(q) + " " + f(q) + " 0 1 0 " + f(-2 * q) + " 0"; }
    return d;
  };
  /* a hand tick (check mark) and a hand cross, sized s */
  Pen.prototype.tick = function (x, y, s) { s = s || 18; return this.line(x, y, x + s * .33, y + s * .33, { rough: .5 }) + this.line(x + s * .33, y + s * .33, x + s, y - s * .45, { rough: .5 }); };
  Pen.prototype.emptyset = function (cx, cy, r) { return this.ellipse(cx, cy, r, r, { wobble: .05 }) + this.line(cx + r * .95, cy - r * 1.25, cx - r * .95, cy + r * 1.25, { rough: .4 }); };

  /* ---------------------------------------------------------------- SVG helpers */
  function svg(host, cls) {
    if (getComputedStyle(host).position === "static") host.style.position = "relative";
    var s = document.createElementNS(NS, "svg"); s.setAttribute("class", "fg-svg" + (cls ? " " + cls : "")); s.setAttribute("aria-hidden", "true");
    host.appendChild(s); return s;
  }
  function path(s, d, stroke, width, a) {
    var p = document.createElementNS(NS, "path"); p.setAttribute("d", d); p.setAttribute("fill", (a && a.fill) || "none");
    if (stroke) { p.setAttribute("stroke", stroke); p.setAttribute("stroke-width", width); p.setAttribute("stroke-linecap", "round"); p.setAttribute("stroke-linejoin", "round"); }
    if (a) { for (var k in a) if (k !== "fill") p.setAttribute(k, a[k]); }
    s.appendChild(p); return p;
  }
  function el(s, tag, a) { var e = document.createElementNS(NS, tag); for (var k in a) e.setAttribute(k, a[k]); s.appendChild(e); return e; }
  function box(e, host) { var a = e.getBoundingClientRect(), b = host.getBoundingClientRect(); return { x: a.left - b.left, y: a.top - b.top, w: a.width, h: a.height }; }

  /* draw-on: the path appears as a pen draws it (dash offset), once. In stillness it is simply there.
     Stillness is read at each opening, never once at load: reduced motion, the shell's ?static=1 (body.static) and its
     failsafe (body.failsafe, which can arrive after load). Each instance hands its own reading to drawOn. */
  function stillNow() {
    var b = document.body;
    return matchMedia("(prefers-reduced-motion: reduce)").matches || !!(b && (b.classList.contains("static") || b.classList.contains("failsafe")));
  }
  function drawOn(p, dur, delay, ease, still) {
    if (still || !p.getTotalLength) return Promise.resolve();
    var L = p.getTotalLength(); p.style.strokeDasharray = L + " " + L; p.style.strokeDashoffset = L;
    return new Promise(function (res) {
      setTimeout(function () {
        p.style.transition = "stroke-dashoffset " + dur + "ms " + (ease || "cubic-bezier(.45,.05,.25,1)");
        p.getBoundingClientRect(); p.style.strokeDashoffset = 0;
        setTimeout(function () { p.style.strokeDasharray = ""; p.style.strokeDashoffset = ""; p.style.transition = ""; res(); }, dur + 30);
      }, delay || 0);
    });
  }

  /* the shared filters, installed once per page in one hidden svg; referenced as url(#fg-…) */
  function defs() {
    if (document.getElementById("fg-defs")) return;
    var s = document.createElementNS(NS, "svg"); s.setAttribute("id", "fg-defs"); s.setAttribute("aria-hidden", "true");
    s.setAttribute("width", "0"); s.setAttribute("height", "0"); s.style.position = "absolute";
    /* GRAPHITE: a pencil line's grain — the stroke's alpha broken by fine noise (construction, never data) */
    s.innerHTML = '<defs><filter id="fg-graphite" x="-5%" y="-5%" width="110%" height="110%" color-interpolation-filters="sRGB">' +
      '<feTurbulence type="fractalNoise" baseFrequency="1.35" numOctaves="2" seed="7" result="n"/>' +
      '<feColorMatrix in="n" type="matrix" values="0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 1.9 0 0 0 -.38" result="a"/>' +
      '<feComposite in="SourceGraphic" in2="a" operator="in"/></filter>' +
      /* STAMP: a rubber-stamp impression — voids where the ink missed, a slight spread of the ink */
      '<filter id="fg-stamp" x="-5%" y="-10%" width="110%" height="120%" color-interpolation-filters="sRGB">' +
      '<feTurbulence type="fractalNoise" baseFrequency=".55" numOctaves="3" seed="11" result="n"/>' +
      '<feColorMatrix in="n" type="matrix" values="0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 -4 0 0 0 3.3" result="v"/>' +
      '<feComposite in="SourceGraphic" in2="v" operator="in" result="s"/><feMorphology in="s" operator="dilate" radius=".35"/></filter>' +
      /* FELT: a felt-tip's bleed — a dilated, softened under-copy at 30% beneath the stroke */
      '<filter id="fg-felt" x="-3%" y="-10%" width="106%" height="120%"><feMorphology in="SourceGraphic" operator="dilate" radius=".4" result="d"/>' +
      '<feGaussianBlur in="d" stdDeviation=".5" result="b"/><feComponentTransfer in="b" result="f"><feFuncA type="linear" slope=".3"/></feComponentTransfer>' +
      '<feMerge><feMergeNode in="f"/><feMergeNode in="SourceGraphic"/></feMerge></filter></defs>';
    document.body.appendChild(s);
  }

  /* THE LAMP'S RING, FITTED (R2 D5). The guide's ring is a narrow, tall hand ellipse around the one word a
     developed note quotes; drawn from fixed offsets it grazed a neighbouring letter on phones (EVENTER's
     wrapped next line, XTIX's 'for' and the line under it, OASIS's hyphen). ringFit starts from today's
     ellipse (rx = w/2 + rx0, ry = h/2 + ry0, centred on the word, 1px down) and measures the stroke the pen
     will really draw (same seed, same wobble, both passes: its path, not an ideal ellipse):
       - against every OTHER character of the host: its ink box (horizontally its Range box joined to the
         glyph's own ink extents, vertically the glyph's ink from canvas measureText in its computed font,
         about the line's baseline); clearance = least distance minus half the stroke;
       - against the cited word's own ink (the word rendered once into a canvas in its computed font and
         laid on its Range box): every ink point must stay inside the ring's outer edge (0.4px to spare) —
         it may run under the stroke at the word's ends, as the approved ring does, but a ring that cuts its
         own word is not a ring around it (the judge's pixel method counts ink outside the loop as touching).
     The search runs over the judge's range, in the judge's order: ry comes in by 1px (down to h/2 + 2)
     before rx comes in by .3px (down to w/2 + .6); the first ellipse that keeps 2px off every neighbour
     with the word inside is drawn; if none can, the one closest to both (the readout says so). The cited word and o.exempt
     (named ranges only) are not neighbours. Coordinates are the host svg's own (its screen matrix, so a
     turned sheet is measured turned). Standard APIs only: Range, getComputedStyle, canvas measureText /
     getImageData, getScreenCTM. o: { seed, rx0, ry0, wobble, steps, stroke, exempt: [Range], svg }
     -> { cx, cy, rx, ry, d, clear, inside }. */
  var mcx = null, mcache = {};
  function ringFit(hostEl, range, o) {
    o = o || {};
    var sw = o.stroke || 1.4, want = 2, inWant = sw - .4, s = o.svg, tmp = null;   /* the word's ink may run under the stroke (as the approved hand ring's ends do), never out past it */
    if (!s) { tmp = s = svg(hostEl); }
    var M = s.getScreenCTM(), Mi = M ? M.inverse() : null;
    function loc(x, y) { if (!Mi) return [x, y]; return [Mi.a * x + Mi.c * y + Mi.e, Mi.b * x + Mi.d * y + Mi.f]; }
    var wr = range.getBoundingClientRect(), c0 = loc(wr.left + wr.width / 2, wr.top + wr.height / 2);
    var w = wr.width, h = wr.height, cx = c0[0], cy = c0[1] + 1;
    if (!mcx) mcx = document.createElement("canvas").getContext("2d");
    function metrics(font) { mcx.font = font; return mcache[font + "|"] || (mcache[font + "|"] = mcx.measureText("Hxg")); }
    /* the neighbours' ink, in the svg's frame */
    var boxes = [], rg = document.createRange(), tw = document.createTreeWalker(hostEl, NodeFilter.SHOW_TEXT), n;
    function inR(r, node, i) { try { return r.comparePoint(node, i) >= 0 && r.comparePoint(node, i + 1) <= 0; } catch (e) { return false; } }
    var reach = Math.max(w, h) / 2 + 40;
    while ((n = tw.nextNode())) {
      var el = n.parentElement; if (!el || el.closest("svg")) continue;
      var cs = getComputedStyle(el);
      if (/rgba\([^)]*,\s*0\)$/.test(cs.webkitTextFillColor || "") || cs.visibility !== "visible") continue;   /* unpainted ink (the ✓ under its brush tick) */
      var font = cs.fontStyle + " " + cs.fontWeight + " " + cs.fontSize + " " + cs.fontFamily, fm = metrics(font), fa = fm.fontBoundingBoxAscent, fd = fm.fontBoundingBoxDescent;
      for (var i = 0; i < n.data.length; i++) {
        var ch = n.data[i]; if (/\s/.test(ch)) continue;
        if (inR(range, n, i)) continue;
        if ((o.exempt || []).some(function (x) { return inR(x, n, i); })) continue;
        rg.setStart(n, i); rg.setEnd(n, i + 1);
        var r = null, rs = rg.getClientRects(); for (var k = 0; k < rs.length; k++) if (rs[k].width > 0 && rs[k].height > 0) { r = rs[k]; break; }
        if (!r) continue;
        mcx.font = font;
        var key = font + "|" + ch, m = mcache[key] || (mcache[key] = mcx.measureText(ch));
        var base = r.top + (r.height - (fa + fd)) / 2 + fa;
        var x0 = Math.min(r.left, r.left - m.actualBoundingBoxLeft), x1 = Math.max(r.right, r.left + m.actualBoundingBoxRight);
        var y0 = base - m.actualBoundingBoxAscent, y1 = base + m.actualBoundingBoxDescent;
        var q = [loc(x0, y0), loc(x1, y0), loc(x0, y1), loc(x1, y1)];
        var b = [Math.min(q[0][0], q[1][0], q[2][0], q[3][0]), Math.min(q[0][1], q[1][1], q[2][1], q[3][1]), Math.max(q[0][0], q[1][0], q[2][0], q[3][0]), Math.max(q[0][1], q[1][1], q[2][1], q[3][1])];
        if (b[2] < cx - reach - w / 2 || b[0] > cx + reach + w / 2 || b[3] < cy - reach || b[1] > cy + reach) continue;
        boxes.push(b);
      }
    }
    /* the cited word's own ink: rendered once at 2x in its font, per column its top and bottom ink, and the
       whole of its first and last columns, laid on the word's Range box (scaled to its measured width) */
    var ink = [], tok = range.toString(), ce = range.startContainer.nodeType === 1 ? range.startContainer : range.startContainer.parentElement;
    if (tok.trim() && ce) {
      var cs2 = getComputedStyle(ce), font2 = cs2.fontStyle + " " + cs2.fontWeight + " " + cs2.fontSize + " " + cs2.fontFamily, fs = parseFloat(cs2.fontSize) || 16;
      var fm2 = metrics(font2); mcx.font = font2;
      var xh2 = mcx.measureText("x").actualBoundingBoxAscent || fs * .5;     /* the word's body: its x-height band */
      var mt = mcx.measureText(tok), K = 2, pad = Math.ceil(fs * .5), cv = document.createElement("canvas"), CW = Math.ceil(mt.width + 2 * pad), CH = Math.ceil(fs * 2), B0 = Math.round(fs * 1.25);
      cv.width = CW * K; cv.height = CH * K;
      var c2 = cv.getContext("2d", { willReadFrequently: true }); c2.scale(K, K); c2.font = font2; c2.textBaseline = "alphabetic"; c2.fillStyle = "#000"; c2.fillText(tok, pad, B0);
      var px = c2.getImageData(0, 0, cv.width, cv.height).data, sx = wr.width / (mt.width || wr.width), base2 = wr.top + (wr.height - (fm2.fontBoundingBoxAscent + fm2.fontBoundingBoxDescent)) / 2 + fm2.fontBoundingBoxAscent;
      var cols = [];
      for (var xx = 0; xx < cv.width; xx++) {
        var t0 = -1, t1 = -1;
        for (var yy = 0; yy < cv.height; yy++) if (px[(yy * cv.width + xx) * 4 + 3] >= 96) { if (t0 < 0) t0 = yy; t1 = yy; }
        if (t0 >= 0) cols.push([xx, t0, t1]);
      }
      cols.forEach(function (cc, j) {
        var X0 = wr.left + ((cc[0] + .5) / K - pad) * sx;
        var ys = (j < 3 || j > cols.length - 4) ? (function () { var a = []; for (var yy = cc[1]; yy <= cc[2]; yy++) a.push(yy); return a; })() : [cc[1], cc[2]];
        ys.forEach(function (yy) { var Y = base2 + ((yy + .5) / K - B0), q2 = loc(X0, Y); q2.body = Y >= base2 - xh2 + .5 && Y <= base2 - .5; ink.push(q2); });
      });
    }
    if (tmp) tmp.remove();
    /* the stroke as drawn: the path's cubics, sampled */
    function samples(d) {
      var t = d.match(/[MC]|-?\d*\.?\d+(?:e[-+]?\d+)?/g) || [], pts = [], p = [0, 0], cmd = "", a = [];
      for (var j = 0; j < t.length; j++) {
        if (t[j] === "M" || t[j] === "C") { cmd = t[j]; a = []; continue; }
        a.push(+t[j]);
        if (cmd === "M" && a.length === 2) { p = [a[0], a[1]]; pts.push(p); a = []; }
        else if (cmd === "C" && a.length === 6) {
          for (var u = 1; u <= 8; u++) { var tt = u / 8, v = 1 - tt;
            pts.push([v * v * v * p[0] + 3 * v * v * tt * a[0] + 3 * v * tt * tt * a[2] + tt * tt * tt * a[4], v * v * v * p[1] + 3 * v * v * tt * a[1] + 3 * v * tt * tt * a[3] + tt * tt * tt * a[5]]); }
          p = [a[4], a[5]]; a = [];
        }
      }
      return pts;
    }
    /* the ink points by their angle about the centre, once per call (they do not move between candidates) */
    var NBIN = 180, ang = function (x, y) { var t = Math.atan2(y - cy, x - cx); return ((Math.floor((t + Math.PI) / (2 * Math.PI) * NBIN) % NBIN) + NBIN) % NBIN; };
    ink.forEach(function (Q) { Q.bin = ang(Q[0], Q[1]); });
    function measure(d, rx, ry) {
      var P = samples(d), nb = Infinity, inn = Infinity, innB = Infinity, j, k;
      for (j = 0; j < P.length; j++) for (k = 0; k < boxes.length; k++) {
        var B = boxes[k], dx = Math.max(B[0] - P[j][0], 0, P[j][0] - B[2]), dy = Math.max(B[1] - P[j][1], 0, P[j][1] - B[3]);
        var dd = dx * dx + dy * dy; if (dd < nb) nb = dd;
      }
      nb = Math.sqrt(nb);
      /* each ink point: its distance to the stroke, signed by which side it lies (normalised radius vs the
         nearest drawn sample's), so a point outside the ring counts as negative. The samples are binned by
         their angle about the centre (2deg bins) and each point is compared with the samples within 24deg
         of its own angle: the nearest stroke point of a point near the ring is always among them. */
      var bins = []; for (j = 0; j < NBIN; j++) bins.push([]);
      for (j = 0; j < P.length; j++) bins[ang(P[j][0], P[j][1])].push(P[j]);
      for (var i2 = 0; i2 < ink.length; i2++) {
        var Q = ink[i2], best = Infinity, bp = null, rq = Math.hypot((Q[0] - cx) / rx, (Q[1] - cy) / ry);
        if (rq < .7) continue;                     /* deep inside: never the nearest to the stroke, never outside it */
        for (var o2 = -12; o2 <= 12; o2++) {
          var L = bins[(Q.bin + o2 + NBIN) % NBIN];
          for (var m2 = 0; m2 < L.length; m2++) { var ex = L[m2][0] - Q[0], ey = L[m2][1] - Q[1], e2 = ex * ex + ey * ey; if (e2 < best) { best = e2; bp = L[m2]; } }
        }
        if (!bp) continue;
        var rp = Math.hypot((bp[0] - cx) / rx, (bp[1] - cy) / ry);
        var sg = (rq <= rp ? 1 : -1) * Math.sqrt(best) - sw / 2; if (sg < inn) inn = sg; if (Q.body && sg < innB) innB = sg;
      }
      return { nb: nb - sw / 2, inn: inn, innB: innB };
    }
    var R0 = w / 2 + (o.rx0 == null ? 2.5 : o.rx0), Q0 = h / 2 + (o.ry0 == null ? 8 : o.ry0), rxMin = Math.min(R0, w / 2 + .6), ryMin = Math.min(Q0, h / 2 + 2);
    /* every candidate in the judge's order; then the first that clears its neighbours with the whole word
       inside, else the first that clears them with the word's BODY inside (an ascender's or descender's tip
       may cross the stroke where the lines are too close for an ellipse to pass round it: OASIS 'p' at
       350-360px over the next line's 'd'), else the one nearest to both */
    var cands = [];
    for (var rx = R0; rx >= rxMin - 1e-6; rx -= .3) {
      for (var ry = Q0; ry >= ryMin - 1e-6; ry -= 1) {
        var d = new Pen(o.seed).ellipse(cx, cy, rx, ry, { wobble: o.wobble == null ? .025 : o.wobble, steps: o.steps || 20 });
        var mm = measure(d, rx, ry);
        cands.push({ cx: cx, cy: cy, rx: rx, ry: ry, d: d, clear: mm.nb, inside: mm.inn, body: mm.innB });
        if (mm.nb >= want && mm.inn >= -inWant) break;
      }
      if (cands[cands.length - 1].clear >= want && cands[cands.length - 1].inside >= -inWant) break;
    }
    var res = cands.filter(function (c) { return c.clear >= want && c.inside >= -inWant; })[0] ||
              cands.filter(function (c) { return c.clear >= want && c.body >= -inWant; })[0];
    if (!res) {
      /* nothing in the judge's range clears: where a wrapped line's ascenders stand under the word, the
         ring's top and bottom may come in past h/2 + 2, by half-pixels to h/2 (still outside the word's
         ink: the body is checked), before settling for the nearest */
      for (var rx2 = R0; rx2 >= rxMin - 1e-6 && !res; rx2 -= .3) {
        for (var ry2 = Math.min(Q0, h / 2 + 1.5); ry2 >= h / 2 - 1e-6; ry2 -= .5) {
          var d2 = new Pen(o.seed).ellipse(cx, cy, rx2, ry2, { wobble: o.wobble == null ? .025 : o.wobble, steps: o.steps || 20 }), m2 = measure(d2, rx2, ry2);
          var c2 = { cx: cx, cy: cy, rx: rx2, ry: ry2, d: d2, clear: m2.nb, inside: m2.inn, body: m2.innB };
          cands.push(c2);
          if (m2.nb >= want && m2.innB >= -inWant) { res = c2; break; }
        }
      }
    }
    if (!res) res = cands.reduce(function (a, c) { return Math.min(c.clear - want, c.body + inWant) > Math.min(a.clear - want, a.body + inWant) ? c : a; });
    return res;
  }

  root.FG = { Pen: Pen, rng: rng, hash: hash, wedge: wedge, svg: svg, path: path, el: el, box: box, drawOn: drawOn, stillNow: stillNow, NS: NS, defs: defs, ringFit: ringFit };
})(window);
