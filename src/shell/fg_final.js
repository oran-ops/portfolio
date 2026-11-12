/* FINAL -- its own plates (built from docs/fieldguide-six/final.md). window.FGDOC.final(X, FG, RT) makes one instance; its
   draw(ctx) is called by fg.js after the shared drawing on every draw. ctx = {X, DOC, host, hostUV, FG, STILL, baselineOf,
   ink, line, text, uv, scroller}. */
window.FGDOC = window.FGDOC || {};
window.FGDOC.final = function (X0, FG0, RT) {
  "use strict";
  var HOST = RT.H;
  var INK = "#1a1714", FILL = "#2FB380", TXT = "#1C6E4E", LIGHT = "#7FE3B8", CARD = "#fffdf8";
  /* the drawn-once gesture's state, across redraws (FI2 adds the paced path's: paid, pacing, its listener and frame) */
  var G = { done: false, cur: null, io: null, paid: 0, pacing: false, onScroll: null, raf: 0 };

  function r1(v) { return Math.round(v * 10) / 10; }

  /* the baseline of a one-line box, from its own font's metrics */
  function baseline(el, b) {
    var cs = getComputedStyle(el), cx = document.createElement("canvas").getContext("2d");
    cx.font = cs.fontStyle + " " + cs.fontWeight + " " + cs.fontSize + " " + cs.fontFamily;
    var m = cx.measureText("0123456789"), fs = parseFloat(cs.fontSize);
    var asc = m.fontBoundingBoxAscent || fs * .95, desc = m.fontBoundingBoxDescent || fs * .25;
    return { y: b.y + (b.h - (asc + desc)) / 2 + asc, fs: fs };
  }

  /* a rounded rectangle by hand: two passes through jittered points, corners as short arcs */
  function rrect(P, x, y, w, h, r, jit) {
    var d = "";
    for (var pass = 0; pass < 2; pass++) {
      var pts = [];
      var edge = function (ax, ay, bx, by) {
        var n = Math.max(1, Math.round(Math.hypot(bx - ax, by - ay) / 36));
        for (var i = 0; i < n; i++) pts.push([ax + (bx - ax) * i / n + P.j(jit), ay + (by - ay) * i / n + P.j(jit)]);
      };
      var arc = function (cx, cy, a0) {
        for (var k = 0; k < 3; k++) { var a = a0 + k * Math.PI / 4; pts.push([cx + Math.cos(a) * r + P.j(jit * .5), cy + Math.sin(a) * r + P.j(jit * .5)]); }
      };
      edge(x + r, y, x + w - r, y); arc(x + w - r, y + r, -Math.PI / 2);
      edge(x + w, y + r, x + w, y + h - r); arc(x + w - r, y + h - r, 0);
      edge(x + w - r, y + h, x + r, y + h); arc(x + r, y + h - r, Math.PI / 2);
      edge(x, y + h - r, x, y + r); arc(x + r, y + r, Math.PI);
      pts.push([x + r + P.j(jit), y + P.j(jit)], [x + r + 14 + P.j(jit), y + P.j(jit)]);   /* the pen overruns its start */
      d += P.curve(pts);
    }
    return d;
  }

  var draw = function (ctx) {
    var X = ctx.X, FG = ctx.FG, host = ctx.host;
    FILL = ctx.line || FILL; TXT = ctx.text || TXT;
    FG.defs();                                            /* the shared #fg-stamp filter */
    X.classList.add("fin-card");                         /* FI1: the card's CSS is keyed on it (no script: today's footer) */

    /* the film edge is printed on the sheet: its top follows the sheet's head (x is the shared 18px) */
    var fo = X.querySelector(".folder");
    if (fo) X.style.setProperty("--fin-film-top", Math.round(fo.getBoundingClientRect().top - X.getBoundingClientRect().top + 150) + "px");
    rule(X, FG, host);
    stamp(X, FG, host);
    plumb(X, FG, host, ctx.STILL);
    plate(X, FG, host);
  };

  /* ---------------------------------------------------------- the cover's hand rule, FINAL's own seed */
  function rule(X, FG, host) {
    var r = X.querySelector(".dt-rule"); if (!r) return;
    [].forEach.call(r.querySelectorAll(".fg-svg"), function (s) { s.style.display = "none"; });   /* the shared stroke (redrawn, and removed, on every draw) */
    var s = host(r), P = new FG.Pen("final-dt-rule"), w = r.clientWidth || 52;
    FG.path(s, P.line(1, 4.4, w - 1, 3.8, { passes: 1, rough: .6, bow: 1.2 }), FILL, 2.6);
  }

  /* ---------------------------------------------------------- F2 · the archive stamp's two frames */
  function stamp(X, FG, host) {
    var g = X.querySelector(".gen3"); if (!g) return;
    var s = host(g), P = new FG.Pen("final-stamp"), w = g.clientWidth, h = g.clientHeight;
    if (w < 40 || h < 20) return;
    FG.path(s, rrect(P, -1.1, -1.1, w + 2.2, h + 2.2, 10, .6), TXT, 2.2);
    FG.path(s, rrect(P, 5.3, 5.3, w - 10.6, h - 10.6, 4.5, .6), TXT, 1);
  }

  /* ---------------------------------------------------------- F5 + F6 · THE PLUMB LINE and its bob */
  function plumb(X, FG, host, STILL) {
    var os = X.querySelector(".osmap"); if (!os) return;
    var nodes = [].slice.call(os.querySelectorAll(".node")); if (!nodes.length) return;
    var stag = getComputedStyle(os).gridTemplateColumns.split(" ").length >= 3;
    var cx = stag ? os.clientWidth / 2 : parseFloat(getComputedStyle(os).paddingLeft) - 30;
    cx = Math.round(cx) + .5;
    var pinY = 40, sc = stag ? 1.25 : 1;
    var knots = nodes.map(function (n) {
      var nn = n.querySelector(".nn"), b = FG.box(nn, os), bl = baseline(nn, b);
      return { y: r1(bl.y - .3 * bl.fs), dir: stag && n.classList.contains("l") ? -1 : 1 };
    });
    var last = knots[knots.length - 1].y, bobTop = last + 84, cordEnd = bobTop - 6.4 * sc;
    var s = host(os); s.classList.add("fin-plumb");

    /* the cord: ONE pass, perfectly straight (the guide's one named exemption from the double pass),
       and its shadow, offset to the lower right from the top-left light */
    var sh = FG.el(s, "line", { x1: cx + 3, y1: pinY + 3, x2: cx + 3, y2: cordEnd + 3, stroke: "rgba(26,23,20,.13)", "stroke-width": 1.2 });
    var cord = FG.el(s, "line", { x1: cx, y1: pinY, x2: cx, y2: cordEnd, stroke: INK, "stroke-width": 1.1 });

    /* the drawing pin */
    /* the drawing pin: a domed head lit from the top left, its needle's short shadow to the lower right */
    var pin = FG.el(s, "g", {}), PP = new FG.Pen("final-pin"), pr = stag ? 6 : 5;
    FG.path(pin, "M" + r1(cx + pr * .4) + " " + r1(pinY + pr * .5) + "L" + r1(cx + pr * 1.5) + " " + r1(pinY + pr * 1.7), "rgba(26,23,20,.22)", 1.4);
    FG.el(pin, "circle", { cx: cx + 1.2, cy: pinY + 1.5, r: pr + .5, fill: "rgba(26,23,20,.18)" });
    FG.el(pin, "circle", { cx: cx, cy: pinY, r: pr, fill: CARD });
    FG.path(pin, PP.arc(cx, pinY, pr - 1.4, Math.PI * .1, Math.PI * .9, { passes: 1, wobble: .05 }), "rgba(26,23,20,.28)", 1.2);
    FG.path(pin, PP.ellipse(cx, pinY, pr, pr, { passes: 2, wobble: .03, steps: 10 }), INK, 1.3);
    FG.el(pin, "ellipse", { cx: r1(cx - pr * .38), cy: r1(pinY - pr * .4), rx: r1(pr * .32), ry: r1(pr * .2), fill: "#ffffff", transform: "rotate(-35 " + r1(cx - pr * .38) + " " + r1(pinY - pr * .4) + ")" });

    /* the knots and their ties (today's connector and diamond, redrawn), each principle its own */
    var kg = knots.map(function (k, i) {
      var g = FG.el(s, "g", { class: "fin-knot" }), TP = new FG.Pen("final-tie-0" + (i + 1)), x2 = cx + k.dir * 24;
      FG.path(g, "M" + cx + " " + k.y + "Q" + r1(cx + k.dir * 12) + " " + r1(k.y + 1.6) + " " + x2 + " " + k.y, INK, .9);
      FG.path(g, "M" + cx + " " + r1(k.y + .5 + TP.j(.3)) + "Q" + r1(cx + k.dir * 12 + TP.j(.6)) + " " + r1(k.y + 1.9 + TP.j(.3)) + " " + r1(x2 + k.dir * TP.j(.6)) + " " + r1(k.y + TP.j(.4)), INK, .9, { opacity: ".55" });
      /* the knot: two overlapping turns wrapped round the cord, the second pass rougher and fainter */
      var KP = new FG.Pen("final-knot-0" + (i + 1));
      FG.path(g, KP.arc(cx, r1(k.y - 1.2), 3.2, Math.PI * .95, Math.PI * 2.15, { passes: 1, wobble: .25 }), INK, 1.3);
      FG.path(g, KP.arc(cx, r1(k.y + 1.3), 3.4, -Math.PI * .1, Math.PI * 1.15, { passes: 1, wobble: .3 }), INK, 1.3);
      FG.path(g, KP.arc(cx + KP.j(.3), r1(k.y + .1), 3.6, Math.PI * 1.05, Math.PI * 2.05, { passes: 1, wobble: .35 }), INK, .8, { opacity: ".55" });
      return { g: g, y: k.y };
    });

    /* the bob: today's emerald ▼, as a plumb bob hanging at the cord's end */
    var BP = new FG.Pen("final-bob"), bob = FG.el(s, "g", { transform: "translate(" + cx + " " + r1(bobTop) + ") scale(" + sc + ")" });
    FG.el(bob, "ellipse", { cx: 5.6, cy: 57.6, rx: 7.2, ry: 1.9, fill: "rgba(26,23,20,.12)" });
    FG.el(bob, "circle", { cx: 0, cy: -3.2, r: 3.2, fill: "none", stroke: INK, "stroke-width": 1.2 / sc });
    FG.el(bob, "rect", { x: -6, y: 0, width: 12, height: 7, fill: CARD, stroke: INK, "stroke-width": 1.3 / sc });
    var body = "M-13 7 L13 7 L13 14 C13 26 4 40 0 54 C-4 40 -13 26 -13 14 Z";
    FG.path(bob, body, null, 0, { fill: FILL });
    for (var p = 0; p < 2; p++) {
      var j = function (m) { return r1(BP.j(m)); };
      var dp = "M" + (-13 + j(.4)) + " " + (7 + j(.3)) + " L" + (13 + j(.4)) + " " + (7 + j(.3)) + " L" + (13 + j(.3)) + " " + (14 + j(.3)) +
        " C" + (13 + j(.4)) + " " + (26 + j(.4)) + " " + (4 + j(.4)) + " " + (40 + j(.4)) + " " + j(.25) + " " + (54 + j(.25)) +
        " C" + (-4 + j(.4)) + " " + (40 + j(.4)) + " " + (-13 + j(.4)) + " " + (26 + j(.4)) + " " + (-13 + j(.3)) + " " + (14 + j(.3)) + " Z";
      FG.path(bob, dp, INK, 1.5 / sc, { opacity: p ? ".6" : "1" });
    }
    FG.path(bob, "M-13 14 L13 14", INK, .9 / sc);
    FG.path(bob, "M-9 17 C-9 26 -5 36 -1.5 46", CARD, 1.1 / sc, { opacity: ".6" });

    /* the file's .tipd keeps its box, under the bob, unpainted */
    var tip = os.querySelector(".tipd");
    if (tip) { tip.style.left = r1(cx - 13 * sc) + "px"; tip.style.top = r1(bobTop) + "px"; tip.style.width = r1(26 * sc) + "px"; tip.style.height = r1(54 * sc) + "px"; }

    /* ---- the drawn-once gesture: ON by default (Oran, 2026-10-15); ?gesture=0, stillness, ?static=1 and re-entry
       show it complete. ONE observer for the page, re-aimed (never duplicated) on every redraw. */
    var cur = { cord: cord, sh: sh, knots: kg, bob: bob, pinY: pinY, L: cordEnd - pinY, os: os, cx: cx, sc: sc, bobT: bob.getAttribute("transform") };
    if (G.running) { G.running = false; G.done = true; }      /* a redraw mid-gesture: print it complete */
    G.cur = cur;
    /* FI2 (NEW MOTION, ON by default — Oran 2026-10-24; ?pace=0 off): only on phones, only where the plate is taller than 0.9 of the window,
       with the gesture on and not still; anywhere else today's drop. A redraw that leaves that range mid-way prints the
       cord complete (as a redraw mid-drop does); one that leaves it before anything was let down falls back to the drop. */
    var paced = HOST.w <= 760 && os.offsetHeight > .9 * HOST.h;
    if (G.pacing && !paced) { unpace(); if (G.paid > 0) G.done = true; }
    if (STILL || G.done) return;
    hide(cur);
    if (!("IntersectionObserver" in window)) { unpace(); G.done = true; show(cur); return; }
    if (paced) { if (G.io) G.io.disconnect(); pace(); return; }
    if (!G.io) {
      var th = []; for (var t = 0; t <= 20; t++) th.push(t / 20);
      /* half the plate in view — or, for a plate taller than the window, half the WINDOW filled by it, or its
         top past the window's middle (the failsafe: it can always be reached) */
      G.io = new IntersectionObserver(RT.guard(function (es) {
        es.forEach(function (e) {
          if (G.done || G.running || !e.isIntersecting) return;
          var b = e.boundingClientRect;
          if (e.intersectionRect.height >= Math.min(b.height, HOST.h) * .5 || b.top <= HOST.top + HOST.h / 2) { G.io.disconnect(); letDown(); }
        });
      }), { root: HOST.root, threshold: th });
    }
    G.io.disconnect(); G.io.observe(os);
  }
  function hide(c) {
    [c.cord, c.sh].forEach(function (l) { l.style.strokeDasharray = c.L + " " + c.L; l.style.strokeDashoffset = c.L; });
    c.knots.forEach(function (k) { k.g.style.opacity = "0"; k.g.style.transition = "opacity 80ms linear"; });
    c.bob.style.opacity = "0"; c.bob.style.transition = "opacity 120ms linear";
  }
  function show(c) {
    [c.cord, c.sh].forEach(function (l) { l.style.strokeDasharray = ""; l.style.strokeDashoffset = ""; });
    c.knots.forEach(function (k) { k.g.style.opacity = "1"; });
    c.bob.style.opacity = "1";
    if (c.bobT) c.bob.setAttribute("transform", c.bobT);       /* FI2: the bob back where the print hangs it */
  }

  /* FI2 · the cord let down at the reader's pace (phones, ?pace=1). The approved gesture's own frames, paced: the
     cord pays out to the reader's line (62% down the reading window) — paid = max(paid, host top + host height × .62
     − plate top − pin), clamped to [0, L] — and never retracts; the bob hangs at the cord's end all the way (cord end
     + 6.4·sc, as the print hangs it); each knot and its tie appear whole as the cord passes them, 01→09. At paid = L
     the listener is removed and the plate is printed complete. ONE passive, rAF-throttled scroll listener for the
     page; a redraw keeps paid (G) and re-aims at the new drawing. Text never moves; nothing is written but the
     drawing's own styles.
     PORT: the listener goes on the section's scroller (#view); viewHost() becomes FG.host, which gives the scroller's
     TOP as well as its height (live: #view.getBoundingClientRect().top and #view.clientHeight; lab: 0 and
     innerHeight). Rects are viewport-relative, so the line is host.top + host.h × .62: with the height alone the
     cord would pay out to a line #view's top offset higher (at 390×844, #view starts at y 90: half-way down the
     window instead of 62%). The listener is removed when done or when the document closes, and G is reset once per
     opening (mw-show). */
  function viewHost() { return { top: HOST.top, h: HOST.h }; }
  function pace() {
    var c = G.cur; if (!c) return;
    G.pacing = true;
    if (!G.onScroll) {
      G.onScroll = function () { if (!G.raf) G.raf = requestAnimationFrame(RT.guard(function () { G.raf = 0; pace(); })); };
      HOST.scroller().addEventListener("scroll", G.onScroll, { passive: true });
    }
    var H = viewHost(), line = H.top + H.h * .62 - c.os.getBoundingClientRect().top - c.pinY;
    G.paid = Math.max(0, Math.min(c.L, Math.max(G.paid, line)));
    var p = G.paid;
    [c.cord, c.sh].forEach(function (l) { l.style.strokeDasharray = c.L + " " + c.L; l.style.strokeDashoffset = c.L - p; });
    c.knots.forEach(function (k) { if (k.y <= c.pinY + p + .5) k.g.style.opacity = "1"; });
    c.bob.style.transition = ""; c.bob.style.opacity = "1";
    c.bob.setAttribute("transform", "translate(" + c.cx + " " + r1(c.pinY + p + 6.4 * c.sc) + ") scale(" + c.sc + ")");
    if (p >= c.L) { unpace(); G.done = true; show(c); }
  }
  function unpace() {
    if (G.onScroll) HOST.scroller().removeEventListener("scroll", G.onScroll, { passive: true });
    if (G.raf) cancelAnimationFrame(G.raf);
    G.onScroll = null; G.raf = 0; G.pacing = false;
  }
  /* the cord is let down from the pin at the system pen tempo (1.6px/ms, ≤900ms); each knot and its tie
     appear whole as the pen passes them, 01→09; the bob when the pen reaches it. Text never moves. */
  function letDown() {
    var c = G.cur; if (!c) return;
    G.running = true;
    var dur = Math.min(900, c.L / 1.6), t0 = performance.now();
    (function frame(now) {
      if (G.cur !== c || !G.running) return;                 /* redrawn meanwhile: the new drawing is printed complete */
      var f = Math.max(0, Math.min(1, (now - t0) / dur)), y = c.pinY + f * c.L;
      [c.cord, c.sh].forEach(function (l) { l.style.strokeDashoffset = c.L * (1 - f); });
      c.knots.forEach(function (k) { if (k.y <= y + .5) k.g.style.opacity = "1"; });
      if (f >= 1) { G.running = false; G.done = true; show(c); return; }
      RT.raf(frame);
    })(t0);
  }

  /* ---------------------------------------------------------- F7 + F8 · THE CLOSING PLATE */
  function plate(X, FG, host) {
    var vs = X.querySelector(".vseal"), fc = X.querySelector(".fcontact");
    /* the board's ground in board coordinates, so the glow and the plate rules cross the join */
    if (vs && fc) {
      var top = vs.offsetTop, bh = fc.offsetTop + fc.offsetHeight - top;
      vs.style.setProperty("--fin-bh", bh + "px"); vs.style.setProperty("--fin-by", "0px");
      fc.style.setProperty("--fin-bh", bh + "px"); fc.style.setProperty("--fin-by", (top - fc.offsetTop) + "px");
      /* the plate rules (every 96px) are phased so the foot's hairline falls midway between two of them */
      var hair = fc.offsetTop - top + parseFloat(getComputedStyle(fc).paddingTop) - 1, rp = (((hair + 48 - 95) % 96) + 96) % 96;
      vs.style.setProperty("--fin-rp", rp + "px"); fc.style.setProperty("--fin-rp", rp + "px");
    }
    if (vs) {
      /* hi11's hand underline under each of the file's two <b>, following every wrapped line */
      var vq = vs.querySelector(".vq");
      if (vq) {
        var s = host(vq), hb = vq.getBoundingClientRect(), below = parseFloat(getComputedStyle(vq).fontSize) * .075;   /* 3px at 40px; less at 26px, clear of the next line's ascenders */
        [].forEach.call(vq.querySelectorAll("b"), function (b, i) {
          var P = new FG.Pen("final-b" + (i + 1));
          [].forEach.call(b.getClientRects(), function (r) {
            if (r.width < 4) return;
            var x0 = r.left - hb.left - 2, x1 = r.right - hb.left + 4, y = r.bottom - hb.top + below, m = (x0 + x1) / 2;
            FG.path(s, P.curve([[x0, y + P.j(.4)], [m, y + 1.2 + P.j(.2)], [x1, y + P.j(.4)]]), FILL, 2.4);
            FG.path(s, P.curve([[x0 + 3, y + .6 + P.j(.4)], [m, y + 1.6 + P.j(.2)], [x1 - 2, y + .4 + P.j(.4)]]), FILL, 1.2, { opacity: ".55" });
          });
        });
      }
      /* the signing line: the first .vd, a 56px hand stroke */
      var vd = vs.querySelector(".vsig .vd");
      if (vd) { var ss = host(vd), SP = new FG.Pen("final-sig"); FG.path(ss, SP.line(1, 2.4, 55, 1.8, { passes: 1, rough: .6, bow: 1.3 }), FILL, 2.2); }
    }
    if (vs && fc) card(X, FG, host, vs, fc);
    /* the links' focus ring: a hand rectangle in the light tier (the text tier on card paper, and on the calling card), 6px out */
    if (fc) [].forEach.call(fc.querySelectorAll(".cc"), function (a, i) {
      var fs = host(a), FP = new FG.Pen("final-focus-" + i), u = null;
      fs.classList.add("fin-focus");
      var ab = a.getBoundingClientRect();
      [].forEach.call(a.querySelectorAll(".k,.v"), function (e) {
        var rg = document.createRange(); rg.selectNodeContents(e);            /* the words' own extent, not the block's */
        var q = rg.getBoundingClientRect(); if (!q.width) return;
        var b = { x: q.left - ab.left, y: q.top - ab.top, w: q.width, h: q.height };
        u = u ? { x0: Math.min(u.x0, b.x), y0: Math.min(u.y0, b.y), x1: Math.max(u.x1, b.x + b.w), y1: Math.max(u.y1, b.y + b.h) }
              : { x0: b.x, y0: b.y, x1: b.x + b.w, y1: b.y + b.h };
      });
      if (!u) u = { x0: 0, y0: 0, x1: a.clientWidth, y1: a.clientHeight };
      FG.path(fs, FP.rect(r1(u.x0 - 10), r1(u.y0 - 8), r1(u.x1 - u.x0 + 20), r1(u.y1 - u.y0 + 16), { overshoot: 3, rough: .6 }), TXT, 1.6);
    });
  }

  /* ---------------------------------------------------------- FI1 · THE CALLING CARD
     Measured from the file's own boxes: from the name line's top − --cc-pt to the last link's bottom + --cc-pb, as wide
     as the name line + 1px each side (final.css sets the name line and the links to the card's width less its 1px
     inner edge). Three aria-hidden, wordless svgs in .vseal (z-index 2, under the words at 3): the shadow (the card's
     shape, 2px/3px, black .6, CSS blur 2.4); the card (CSS: stock, tooth, the top-left cut's shade; clipped to its
     shape by a CSS path(); here: its inner edge and the 1px rule --cc-rule under the name line); the two slits, cut
     through the board 10px past the card (less where the board's edge is nearer: the narrow form, ≤384). The card's
     shape: a rectangle, radius 2, minus two right triangles (legs --cc-leg) at its top-left and bottom-right, where
     the corners go under the board. No document id, no text. Port: from the same boxes, in the section's own scope. */
  function card(X, FG, host, vs, fc) {
    var sig = vs.querySelector(".vsig"), ccs = fc.querySelectorAll(".cc"); if (!sig || !ccs.length) return;
    var cs = getComputedStyle(X), tok = function (k, d) { var v = parseFloat(cs.getPropertyValue(k)); return isFinite(v) ? v : d; };
    var pt = tok("--cc-pt", 48), pb = tok("--cc-pb", 46), px = tok("--cc-px", 46), leg = tok("--cc-leg", 34), rl = tok("--cc-rule", 34);
    var a = FG.box(sig, vs), z = FG.box(ccs[ccs.length - 1], vs);
    var x = a.x - 1, y = a.y - pt, w = a.w + 2, h = z.y + z.h + pb - y;         /* final.css insets the words' boxes 1px: the inner edge */
    if (w < 120 || h < 80) return;
    /* the tooth of the name line and of each row continues the card's own (its tile set from the card's corner) */
    [sig].concat([].slice.call(ccs)).forEach(function (e) {
      var b = FG.box(e, vs);
      e.style.setProperty("--fin-tx", Math.round(x - b.x) + "px"); e.style.setProperty("--fin-ty", Math.round(y - b.y) + "px");   /* whole pixels by construction (final.css) */
    });
    var R = 2, f = function (v) { return Math.round(v * 100) / 100; };
    var shape = function (ox, oy) {
      return "M" + f(ox + leg) + " " + f(oy) + "H" + f(ox + w - R) + "Q" + f(ox + w) + " " + f(oy) + " " + f(ox + w) + " " + f(oy + R) +
        "V" + f(oy + h - leg) + "L" + f(ox + w - leg) + " " + f(oy + h) + "H" + f(ox + R) + "Q" + f(ox) + " " + f(oy + h) + " " + f(ox) + " " + f(oy + h - R) +
        "V" + f(oy + leg) + "Z";
    };
    var place = function (s, cls, m) {
      s.classList.add(cls);
      /* unrounded: the card's corner lies exactly 1px left of the name line and --cc-pt above it (the tooth registers) */
      s.style.cssText = "inset:auto;left:" + (x - m) + "px;top:" + (y - m) + "px;width:" + (w + 2 * m) + "px;height:" + (h + 2 * m) + "px";
      return s;
    };
    /* the shadow: lies flush on the board, the guide's one light at the top left */
    var sh = place(host(vs), "fin-card-sh", 14);
    FG.path(sh, shape(14 + 2, 14 + 3), null, 0, { fill: "rgba(0,0,0,.6)" });
    /* the card */
    var cd = place(host(vs), "fin-card-p", 0), d = shape(0, 0);
    cd.style.clipPath = "path('" + d + "')";
    FG.path(cd, d, "rgba(0,0,0,.12)", 2);          /* the inner edge: half of a 2px stroke inside the clip */
    var vt = vs.getBoundingClientRect().top, ry = Math.round(vt + a.y + a.h + rl) - vt - y + .5;   /* the rule on a whole pixel */
    FG.path(cd, "M" + f(px) + " " + f(ry) + "H" + f(w - px), "rgba(26,23,20,.16)", 1, { "stroke-linecap": "butt" });
    /* the slits, through the board: 10px past the card, never nearer than 4px to the board's own edge */
    var o = Math.max(2, Math.min(10, x - 4, vs.clientWidth - (x + w) - 4)), m = 16;
    var sl = place(host(vs), "fin-card-s", m);
    var seg = function (x1, y1, x2, y2, col, sw, op) {
      FG.path(sl, "M" + f(m + x1) + " " + f(m + y1) + "L" + f(m + x2) + " " + f(m + y2), col, sw, op ? { "stroke-opacity": op } : null);
    };
    seg(-o, leg + o, leg + o, -o, "#05060a", 2.2);                                  /* top left: away from the light */
    seg(-o + .6, leg + o - 1.4, leg + o - 1.4, -o + .6, "#3b4148", .9);
    seg(w + o, h - leg - o, w - leg - o, h + o, "#05060a", 2);                      /* bottom right: facing it, a pale core */
    seg(w + o - .8, h - leg - o + 1.6, w - leg - o + 1.6, h + o - .8, "#a39b88", 1, ".85");
  }

  return {
    draw: draw,
    open: function () { unpace(); G = { done: false, cur: null, io: null, paid: 0, pacing: false, onScroll: null, raf: 0 }; },
    close: function () { if (G.io) { G.io.disconnect(); G.io = null; } unpace(); G.running = false; }
  };
};
