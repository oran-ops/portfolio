/* TECH -- its own plates. window.FGDOC.tech(X, FG, RT) makes one instance; its draw(ctx) is called by fg.js after the shared
   drawing on every draw. ctx = {X, DOC, host, hostUV, FG, STILL, baselineOf, ink, line, text, uv, scroller}.
   Nothing here writes a word: what it writes goes on the file's own elements: classes, the screen's viewBox and height, and
   its seven texts' x / y (and, in the vertical form, the feedback text's rotation). */
window.FGDOC = window.FGDOC || {};
window.FGDOC.tech = function (X0, FG0, RT) {
  "use strict";
  var HOST = RT.H, NS = "http://www.w3.org/2000/svg", HEADLESS = false;      /* Q2: the head; G30 decides at S8 (D9) */
  var PH = "#7FE3B8", FLASH = "#e6fff4", INK = "#1a1714";
  var written = false;          /* the light pen writes once per open of the file; re-entry and redraws show it complete */
  var io = null;                /* the one observer that waits for the board: disconnected and replaced on every draw */
  var finishNow = null;         /* the current overlay's end state, reachable without the observer (print, no IO) */
  function beforePrint() { if (finishNow) finishNow(); }

  /* the phosphor bloom (and its doubled write-through form), installed once in one hidden, wordless svg */
  function bloomDefs() {
    if (document.getElementById("tech-defs")) return;
    var s = document.createElementNS(NS, "svg");
    s.setAttribute("id", "tech-defs"); s.setAttribute("aria-hidden", "true"); s.setAttribute("width", "0"); s.setAttribute("height", "0");
    s.style.position = "absolute"; s.style.left = "0"; s.style.top = "0";
    function f(id, s1, o1, s2, o2) {
      return '<filter id="' + id + '" filterUnits="userSpaceOnUse" x="-400" y="-400" width="4000" height="4000" color-interpolation-filters="sRGB">' +
        '<feGaussianBlur in="SourceAlpha" stdDeviation="' + s1 + '" result="a1"/><feFlood flood-color="#7FE3B8" flood-opacity="' + o1 + '"/><feComposite in2="a1" operator="in" result="g1"/>' +
        '<feGaussianBlur in="SourceAlpha" stdDeviation="' + s2 + '" result="a2"/><feFlood flood-color="#2FB380" flood-opacity="' + o2 + '"/><feComposite in2="a2" operator="in" result="g2"/>' +
        '<feMerge><feMergeNode in="g2"/><feMergeNode in="g1"/><feMergeNode in="SourceGraphic"/></feMerge></filter>';
    }
    /* drop-shadow(0 0 1.2px rgba(127,227,184,.75)) drop-shadow(0 0 7px rgba(47,179,128,.42)); hot = doubled */
    s.innerHTML = "<defs>" + f("tech-bloom", .6, .75, 3.5, .42) + f("tech-bloom-hot", 1.2, .95, 7, .8) + "</defs>";
    document.body.appendChild(s);
  }

  /* the visible lines of an element's text: each non-space character's box, grouped by line */
  function lineBoxes(el) {
    var rg = document.createRange(), hb = el.getBoundingClientRect(), out = [];
    var w = document.createTreeWalker(el, NodeFilter.SHOW_TEXT), n;
    while ((n = w.nextNode())) {
      if (n.parentElement.closest("svg")) continue;
      for (var i = 0; i < n.data.length; i++) {
        if (/\s/.test(n.data[i])) continue;
        rg.setStart(n, i); rg.setEnd(n, i + 1);
        var r = rg.getClientRects()[0]; if (!r || !r.width) continue;
        var cy = (r.top + r.bottom) / 2, hit = null;
        for (var k = 0; k < out.length; k++) if (Math.abs(out[k].cy - cy) < r.height * .5) { hit = out[k]; break; }
        if (hit) { hit.l = Math.min(hit.l, r.left); hit.r = Math.max(hit.r, r.right); hit.t = Math.min(hit.t, r.top); hit.b = Math.max(hit.b, r.bottom); }
        else out.push({ l: r.left, r: r.right, t: r.top, b: r.bottom, cy: cy, el: n.parentElement });
      }
    }
    return out.map(function (o) { return { x: o.l - hb.left, r: o.r - hb.left, y: o.t - hb.top, b: o.b - hb.top, el: o.el }; });
  }

  /* ---------------------------------------------------------------- T1 the cover's hand rule, in TECH's own seed */
  function coverRule(c) {
    var r = c.X.querySelector(".dt-rule"); if (!r) return;
    [].forEach.call(r.querySelectorAll("svg.fg-svg"), function (s) { s.style.display = "none"; });
    var s = c.host(r), P = new c.FG.Pen("tech-cover-rule");
    c.FG.path(s, P.line(1, 4.5, 51, 3.6, { passes: 1, rough: .7, bow: 1.4 }), c.line, 2.6);
  }

  /* ---------------------------------------------------------------- T3 the tape: one strip per line when it wraps */
  function tape(c) {
    var t = c.X.querySelector(".intb"); if (!t) return;
    t.classList.remove("tape-strips");
    if (lineBoxes(t).length < 2) return;            /* one line: the block itself is the strip */
    t.classList.add("tape-strips");
    var L = lineBoxes(t), cs = getComputedStyle(t), px = parseFloat(cs.paddingLeft), py = parseFloat(cs.fontSize) < 13 ? 6 : 7;
    var a = cs.getPropertyValue("--tape-a").trim() || "#1c6a4c", b = cs.getPropertyValue("--tape-b").trim() || "#145338";
    var s = c.host(t); s.style.zIndex = "-1";
    var d = c.FG.el(s, "defs", {});
    var g1 = c.FG.el(d, "linearGradient", { id: "tech-tape-fill", x1: 0, y1: 0, x2: 0, y2: 1 });
    c.FG.el(g1, "stop", { offset: 0, "stop-color": a }); c.FG.el(g1, "stop", { offset: 1, "stop-color": b });
    var g2 = c.FG.el(d, "linearGradient", { id: "tech-tape-gloss", x1: 0, y1: 0, x2: 0, y2: 1 });
    [[0, "#fff", .08], [.34, "#fff", .08], [.35, "#000", 0], [1, "#000", .08]].forEach(function (st) { c.FG.el(g2, "stop", { offset: st[0], "stop-color": st[1], "stop-opacity": st[2] }); });
    var fl = c.FG.el(d, "filter", { id: "tech-tape-sh", x: "-5%", y: "-30%", width: "110%", height: "180%" });
    c.FG.el(fl, "feDropShadow", { dx: 0, dy: 1, stdDeviation: .75, "flood-color": INK, "flood-opacity": .35 });
    L.forEach(function (l) {
      var x = l.x - px, y = l.y - py, w = (l.r - l.x) + 2 * px, h = (l.b - l.y) + 2 * py;
      c.FG.el(s, "rect", { x: x, y: y, width: w, height: h, rx: 3, fill: "url(#tech-tape-fill)", stroke: "rgba(0,0,0,.25)", "stroke-width": 1, filter: "url(#tech-tape-sh)" });
      c.FG.el(s, "rect", { x: x, y: y, width: w, height: h, rx: 3, fill: "url(#tech-tape-gloss)" });
    });
  }

  /* ---------------------------------------------------------------- T4 a wrapped zone label: its rule follows the last line,
     on the label's midline (the shared rule's: .32em above the baseline) */
  function zoneRules(c) {
    [].forEach.call(c.X.querySelectorAll(".zr"), function (z) {
      var zl = z.querySelector(".zl"); if (!zl) return;
      z.classList.remove("zr-wrapped");
      if (lineBoxes(zl).length < 2) return;
      z.classList.add("zr-wrapped");
      var L = lineBoxes(zl), last = L[L.length - 1], zb = c.FG.box(zl, z), W = z.clientWidth - (parseFloat(getComputedStyle(z).paddingRight) || 0);
      var fs = parseFloat(getComputedStyle(zl).fontSize) || 13;
      var x1 = zb.x + last.r + 18, y = Math.round(zb.y + last.b - c.baselineOf(zl).desc - .32 * fs) + .5;
      if (W - x1 < 40) return;
      var s = c.host(z);
      c.FG.path(s, "M" + x1 + " " + y + "H" + W, INK, 1, { "stroke-dasharray": "3 2", "stroke-linecap": "butt", opacity: ".18" });
    });
  }

  /* ---------------------------------------------------------------- a sketched outline's crossings
     Every crossing of a drawn path (its M/C/L strokes, every pass) with the line coord[ax] = v, as the
     other coordinate. A head lands on the OUTERMOST stroke of its station's drawn outline, not on the
     nominal box: the hand's strokes wander ±1px, and an exact arrow touches the line that is drawn. */
  function crossings(d, ax, v) {
    var tk = d.match(/[A-Za-z]|-?(?:\d+\.?\d*|\.\d+)(?:e[-+]?\d+)?/g) || [], segs = [], cur = [0, 0], cmd = "", i = 0, out = [];
    while (i < tk.length) {
      if (/^[A-Za-z]$/.test(tk[i])) { cmd = tk[i++]; continue; }
      if (cmd === "M") { cur = [+tk[i], +tk[i + 1]]; i += 2; cmd = "L"; }
      else if (cmd === "L") { var e = [+tk[i], +tk[i + 1]]; segs.push([cur, cur, e, e]); cur = e; i += 2; }
      else if (cmd === "C") { var s = [cur, [+tk[i], +tk[i + 1]], [+tk[i + 2], +tk[i + 3]], [+tk[i + 4], +tk[i + 5]]]; segs.push(s); cur = s[3]; i += 6; }
      else i++;
    }
    function at(s, t, k) { var u = 1 - t; return u * u * u * s[0][k] + 3 * u * u * t * s[1][k] + 3 * u * t * t * s[2][k] + t * t * t * s[3][k]; }
    segs.forEach(function (s) {
      var N = 48, f0 = at(s, 0, ax) - v;
      for (var n = 1; n <= N; n++) {
        var t0 = (n - 1) / N, t1 = n / N, f1 = at(s, t1, ax) - v;
        if (f0 === 0) out.push(at(s, t0, 1 - ax));
        if (f0 * f1 < 0) { var a = t0, b = t1, fa = f0; for (var k = 0; k < 40; k++) { var m = (a + b) / 2, fm = at(s, m, ax) - v; if (fa * fm <= 0) b = m; else { a = m; fa = fm; } } out.push(at(s, (a + b) / 2, 1 - ax)); }
        f0 = f1;
      }
      if (f0 === 0) out.push(at(s, 1, 1 - ax));
    });
    return out;
  }
  /* where a head's tip lands: TOUCH px short of the outermost drawn stroke along its axis (centre to centre;
     1.3px strokes, so the two inks just meet), measured by tools/arrow.py at every width */
  var TOUCH = 1;
  function landing(d, ax, v, keep, pick, fallback) {
    var c = crossings(d, ax, v).filter(keep);
    return c.length ? pick.apply(null, c) : fallback;
  }

  /* ---------------------------------------------------------------- T5 THE LIGHT PEN: the board and its screen */
  function board(c) {
    if (io) { io.disconnect(); io = null; }          /* a redraw never leaves an observer on a detached overlay */
    finishNow = null;
    var FG = c.FG, aw = c.X.querySelector(".archw"), sv = aw && aw.querySelector("svg:not(.fg-svg)"); if (!sv) return;
    var tx = [].slice.call(sv.querySelectorAll("text")); if (tx.length < 7) return;
    var names = tx.slice(0, 6), fb = tx[6], col = PH;
    fb.classList.add("tech-fb");
    /* the form: one row (the file's) while five arrows still have room — at full type (gaps ≥ 26), then at
       compact type (gaps ≥ 18); else the vertical form */
    aw.classList.remove("tech-v", "tech-c", "tech-xs"); sv.style.height = ""; fb.removeAttribute("transform");
    aw.classList.toggle("tech-s", !!c.scroller); aw.scrollLeft = 0;   /* below FG.bound.tech: the board scrolls sideways, as R10 */
    var W = sv.getBoundingClientRect().width, len = function (t) { return t.getComputedTextLength(); };
    function fit(padX, m) {
      var ws = names.map(function (t) { return len(t) + padX; }), sum = ws.reduce(function (a, b) { return a + b; }, 0);
      return { ws: ws, m: m, gap: (W - 2 * m - sum) / 5 };
    }
    var F = fit(24, 40);
    if (F.gap < 26) F = fit(24, 24);
    if (F.gap < 26) { aw.classList.add("tech-c"); F = fit(16, 24); }
    var vert = F.gap < 18, B = [], H, i, x0, bw, bh2, xg;
    if (!vert) {
      H = 300; var cy = 95, bh = 46, x = F.m;            /* the row and the return centred on the glass */
      F.ws.forEach(function (w) { B.push({ x: x, y: cy - bh / 2, w: w, h: bh }); x += w + F.gap; });
    } else {
      aw.classList.remove("tech-c"); aw.classList.add("tech-v");
      W = sv.getBoundingClientRect().width;            /* the portrait glass (CSS caps it at 380) */
      var Wv = Math.min(W, 338), off = Math.max(0, (W - Wv) / 2), top = 44;
      x0 = Wv < 300 ? 16 : 22; bh2 = 42;
      /* right of the stations: the return's stub (≥22, so the head meets its line), its chamfer, and the gutter
         that carries the rotated feedback text (30 from the glass edge) */
      bw = Math.min(232, Wv - x0 - 70);
      var longest = Math.max.apply(null, names.map(len));
      if (longest + 16 > bw) { aw.classList.add("tech-xs"); }
      var fl = len(fb), g = Math.max(48, Math.ceil((fl + 8) / 4 - bh2)), y = top;
      for (i = 0; i < 6; i++) { B.push({ x: off + x0, y: y, w: bw, h: bh2 }); y += bh2 + g; }
      H = y - g + 40; xg = off + Wv - 30;
    }
    sv.style.height = H + "px";
    sv.setAttribute("viewBox", "0 0 " + W + " " + H);
    names.forEach(function (t, k) { var b = B[k]; t.setAttribute("x", (b.x + b.w / 2).toFixed(1)); t.setAttribute("y", (b.y + b.h / 2 + .5).toFixed(1)); });

    /* the board's top edge, under the zone's header row (its padding is the gap) */
    var sb = FG.box(sv, aw), pad = parseFloat(getComputedStyle(sv).marginTop) || 22, bt = sb.y - pad;
    aw.style.setProperty("--bt", bt + "px");
    /* the sketch frame: one calm pass, with card between it and the glass (5 of 14 on phone, 10 of 22) */
    var s = c.host(aw), BP = new FG.Pen("tech-board"), inset = pad < 20 ? 5 : 10;
    FG.path(s, BP.rect(inset, bt + inset, (c.scroller ? aw.scrollWidth : aw.clientWidth) - 2 * inset, aw.clientHeight - bt - 2 * inset, { overshoot: 3, passes: 1 }), INK, 1.1);

    /* the marks, in the screen's own coordinates */
    var g0 = FG.el(s, "g", { transform: "translate(" + sb.x + " " + sb.y + ")" });
    g0.setAttribute("filter", "url(#tech-bloom)");
    var outl = B.map(function (b, k) {
      var NP = new FG.Pen("tech-node-" + k), od = NP.rect(b.x, b.y, b.w, b.h, { overshoot: 2.2, rough: .55 });
      FG.path(g0, od, col, 1.3);
      return od;
    });
    var P = new FG.Pen("tech-arch");
    function head(x, y, a) { return P.line(x, y, x - 8 * Math.cos(a - .5), y - 8 * Math.sin(a - .5), { passes: 1, rough: .25 }) + P.line(x, y, x - 8 * Math.cos(a + .5), y - 8 * Math.sin(a + .5), { passes: 1, rough: .25 }); }
    var shafts = [], heads = [];
    /* each head lands on its station's drawn outline (TOUCH short of its outermost stroke), on the shaft's line */
    for (i = 0; i < 5; i++) {
      var A0 = B[i], A1 = B[i + 1], d, h, tp;
      if (!vert) {
        var yy = A0.y + A0.h / 2;
        tp = landing(outl[i + 1], 1, yy, function (x) { return x < A1.x + A1.w / 2; }, Math.min, A1.x) - TOUCH;
        d = P.line(A0.x + A0.w + 4, yy, tp, yy, { passes: 1, rough: .4 }); h = head(tp, yy, 0);
      } else {
        var xx = A0.x + A0.w / 2;
        tp = landing(outl[i + 1], 0, xx, function (y) { return y < A1.y + A1.h / 2; }, Math.min, A1.y) - TOUCH;
        d = P.line(xx, A0.y + A0.h + 4, xx, tp, { passes: 1, rough: .4 }); h = head(xx, tp, Math.PI / 2);
      }
      shafts.push(FG.path(g0, d, col, 1.3)); heads.push(FG.path(g0, h, col, 1.3));
    }
    /* THE RETURN — the file's feedback path, CRM → AI RESEARCH: orthogonal, 45° chamfers, phantom. It ends
       exactly where its head's tip is: on AI RESEARCH's drawn outline, along the last run's own line, so
       the head's axis is the path's final tangent by construction (tools/arrow.py measures all of it). */
    var AR = B[1], CR = B[5], ch = 14, rq, rh, op = ".7";
    if (!vert) {
      var xa = AR.x + AR.w / 2, xc = CR.x + CR.w / 2, yb = 229;
      var ta = landing(outl[1], 0, xa, function (y) { return y > AR.y + AR.h / 2; }, Math.max, AR.y + AR.h) + TOUCH;
      rq = [[xc, CR.y + CR.h + 4], [xc, yb - ch], [xc - ch, yb], [xa + ch, yb], [xa, yb - ch], [xa, ta]];
      rh = head(xa, ta, -Math.PI / 2);
      fb.setAttribute("x", ((xa + xc) / 2).toFixed(1)); fb.setAttribute("y", (yb - 16).toFixed(1));
    } else {
      var ya = AR.y + AR.h / 2, yc = CR.y + CR.h / 2;
      var xr = landing(outl[1], 1, ya, function (x) { return x > AR.x + AR.w / 2; }, Math.max, AR.x + AR.w) + TOUCH;
      rq = [[CR.x + CR.w + 4, yc], [xg - ch, yc], [xg, yc - ch], [xg, ya + ch], [xg - ch, ya], [xr, ya]];
      rh = head(xr, ya, Math.PI);
      fb.setAttribute("x", "0"); fb.setAttribute("y", "0");
      fb.setAttribute("transform", "translate(" + (xg + 14).toFixed(1) + " " + ((ya + yc) / 2).toFixed(1) + ") rotate(90)");
    }
    var rp = "M" + rq.map(function (q) { return q[0] + " " + q[1]; }).join("L");
    /* the phantom pattern (14 4 2 4 2 4) fitted to the run: a whole number of cycles plus one long dash, so
       the line leaves CRM on a long dash and arrives under the head on one (never a gap at the tip); the
       scale moves at most a few per cent from the drawn pattern */
    var RL = 0; for (i = 1; i < rq.length; i++) RL += Math.hypot(rq[i][0] - rq[i - 1][0], rq[i][1] - rq[i - 1][1]);
    var nc = Math.max(1, Math.round((RL - 14) / 30)), ks = RL / (30 * nc + 14);
    var ret = FG.path(g0, rp, col, 1.3, { opacity: op, "stroke-dasharray": [14, 4, 2, 4, 2, 4].map(function (v) { return +(v * ks).toFixed(4); }).join(" "), "stroke-linecap": "butt" });
    var rhp = HEADLESS ? null : FG.path(g0, rh, col, 1.3, { opacity: op });

    if (c.STILL || written || !("IntersectionObserver" in window)) return;   /* printed complete */
    /* TIER 1 (Oran, 2026-10-15: yes): once the board is in view, the light pen writes once — the five shafts in
       the file's order, each head as its shaft lands, then the return through a solid mask (its phantom dashes
       never crawl), closing with the head at AI RESEARCH. Each new vector shows the storage tube's write-through:
       bright, settling to phosphor over 420ms (colour only). Text never moves. */
    var mid = "tech-loop-mask", dd = FG.el(s, "defs", {}), mk = FG.el(dd, "mask", { id: mid, maskUnits: "userSpaceOnUse" });
    var mp = FG.el(mk, "path", { d: rp, stroke: "#fff", "stroke-width": 8, fill: "none" });      /* in the return's own user space */
    var ML = mp.getTotalLength();
    ret.setAttribute("mask", "url(#" + mid + ")");
    mp.style.strokeDasharray = ML + " " + ML; mp.style.strokeDashoffset = ML;
    var later = shafts.concat(heads).concat(rhp ? [rhp] : []);
    later.forEach(function (p) { p.style.visibility = "hidden"; });
    /* the end state, without motion: every mark shown, the return unmasked (print; a stale or missing observer) */
    finishNow = function () {
      written = true; if (io) { io.disconnect(); io = null; }
      later.forEach(function (p) { p.style.visibility = ""; p.style.strokeDasharray = ""; p.style.strokeDashoffset = ""; });
      mp.style.transition = "none"; mp.style.strokeDashoffset = 0;
    };
    function flash(p) {
      p.style.stroke = FLASH; p.setAttribute("filter", "url(#tech-bloom-hot)"); p.getBoundingClientRect();
      p.style.transition = (p.style.transition ? p.style.transition + "," : "") + "stroke 420ms ease-out";
      p.style.stroke = col;
      RT.later(function () { p.removeAttribute("filter"); }, 430);
    }
    function play() {
      written = true; if (io) { io.disconnect(); io = null; }
      var t = 0;
      shafts.forEach(function (p, n) {
        RT.later(function () {
          var L = p.getTotalLength();
          p.style.strokeDasharray = L + " " + L; p.style.strokeDashoffset = L; p.style.visibility = "";
          p.style.transition = "stroke-dashoffset 150ms cubic-bezier(.45,.05,.25,1)"; flash(p);
          p.getBoundingClientRect(); p.style.strokeDashoffset = 0;
          RT.later(function () { p.style.strokeDasharray = ""; p.style.strokeDashoffset = ""; heads[n].style.visibility = ""; flash(heads[n]); }, 160);
        }, t);
        t += 170;
      });
      RT.later(function () {
        flash(ret);
        if (vert) { mp.style.strokeDashoffset = 0; if (rhp) { rhp.style.visibility = ""; flash(rhp); } return; }   /* phone: the return appears whole */
        mp.style.transition = "stroke-dashoffset 900ms cubic-bezier(.45,.05,.25,1)"; mp.getBoundingClientRect(); mp.style.strokeDashoffset = 0;
        RT.later(function () { if (rhp) { rhp.style.visibility = ""; flash(rhp); } }, 920);
      }, t + 40);
    }
    /* the trigger is relative to the viewport, so a board taller than the window still plays: 40% of the board
       in view, or half the window's height filled by it, or its top past the window's middle — whichever comes
       first. NEVER SEEN: a board the reader has already passed (a fling the observer did not sample, an anchor
       jump, a restored scroll) is printed complete, so coming back up never meets a half-drawn plate. */
    var TH = []; for (i = 0; i <= 20; i++) TH.push(i / 20);
    io = new IntersectionObserver(RT.guard(function (es) {
      var e = es[es.length - 1], r = e.boundingClientRect;
      if (written || !s.isConnected) return;
      if (!e.isIntersecting) { if (r.top < HOST.top) finishNow(); return; }
      var vh = e.rootBounds ? e.rootBounds.height : HOST.h;
      if (e.intersectionRect.height >= Math.min(.4 * r.height, .5 * vh) - .5 || r.top <= HOST.top + .5 * vh) play();
    }), { root: HOST.root, threshold: TH });
    io.observe(aw);
  }

  /* ---------------------------------------------------------------- T7 / T9 by hand: the philosophy's stroke, the close's hairline
     R2 TE1: the philosophy no longer sits under an 18%-ink hairline; it opens under the cover rule's own stroke —
     56px of emerald (the fill tier, 2.6px) at its top-left, as the file's title card does. The .bot hairline stays. */
  function hairlines(c) {
    var ph = c.X.querySelector(".phil"), bt = c.X.querySelector(".bot"), s, P;
    if (ph) { s = c.host(ph); P = new c.FG.Pen("tech-phil-rule"); c.FG.path(s, P.line(1, 4.5, 55, 3.6, { passes: 1, rough: .7, bow: 1.4 }), c.line, 2.6); }
    if (bt) { s = c.host(bt); P = new c.FG.Pen("tech-bot-rule"); c.FG.path(s, P.line(0, -32, bt.clientWidth, -32, { passes: 1, rough: .35 }), INK, .9, { opacity: ".18" }); }
  }

  return {
    draw: function (c) {
      bloomDefs();
      coverRule(c); tape(c); zoneRules(c); board(c); hairlines(c);
    },
    open: function () { written = false; finishNow = null; addEventListener("beforeprint", beforePrint); },
    close: function () { removeEventListener("beforeprint", beforePrint); if (io) { io.disconnect(); io = null; } finishNow = null; }
  };
};
