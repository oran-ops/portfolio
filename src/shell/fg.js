/* fg.js -- the field guide's runtime: the lab's xtix.js restructured as FG.mount(section) -> {open, close, resize}.
   One instance per section, made once and kept: what was module state is instance state; observers, the scroller's
   listener, rAF and timers live only between open and close; stillness is read at each opening; lamp and turn survive a
   close; the once-per-opening gestures re-arm. A runtime that throws prints the file. No lab switch and no test hook ships.
   Everything drawn here is aria-hidden SVG laid over today's DOM; no text node is written except
   the lamp's three whole-string swaps, exactly as the shell makes them today. Seeds are by element,
   so a redraw on resize is the same drawing. */
(function (root) {
  "use strict";
  root.FGDOC = root.FGDOC || {};
  var FG = root.FG, FG0 = FG, INST = {}, FAILED = {}, TOLD = {}, LOADS = {}, CUR = null, OPENING = 0, INK = "#1a1714";
  function $(id) { return document.getElementById(id); }

  /* FG.host: everything the runtime reads of its window. Live: composition widths from #docs, heights and the scroller
     from #view. Lab: the window's values, so the same code runs in both. Rects are viewport-relative: a reading line
     written from a height is HOST.top + HOST.h * k, never the height alone (at 390x844 #view starts at y 90). */
  var HOST = FG.host = {
    get live() { return !!$("docs"); },
    get w() { var d = $("docs"); return d ? d.clientWidth : innerWidth; },
    get h() { var v = $("view"); return v ? v.clientHeight : innerHeight; },
    get top() { var v = $("view"); return v ? v.getBoundingClientRect().top : 0; },
    get root() { return $("view"); },
    scroller: function () { return $("view") || root; },
    scrollBy: function (x, y) { ($("view") || root).scrollBy(x, y); }
  };
  /* where FIT is proven: a document's lowest fitted V (PORT_PLAN 1.3 #4), from its frozen key; below it the plate takes
     the scroller form, a function of V alone, never of the lamp or the turn. Filled at each document's stage. */
  FG.bound = { tech: 325, eventer: 320, medcoin: 313 };

  /* the document's faces, started once per document before anything is measured: fonts.ready resolves while the other
     six sections are display:none, so it says nothing about this one. Live, the shell's go() starts this before the
     window unhides. The text decides which unicode ranges load. */
  function facesOf(sec) {
    var d = sec.getAttribute("data-file"), f = document.fonts, all = [];
    if (LOADS[d]) return LOADS[d];
    if (!f || !f.load) return (LOADS[d] = Promise.resolve());
    var txt = sec.textContent;
    (HOST.live ? ["FG Fraunces", "FG Caveat", "FG Symbols", "Geist", "JetBrains Mono"] : ["Fraunces", "Caveat", "Geist", "JetBrains Mono"]).forEach(function (n) {
      ["normal", "italic"].forEach(function (st) { all.push(f.load(st + ' 400 16px "' + n + '"', txt).catch(function () {})); });
    });
    return (LOADS[d] = Promise.all(all));
  }
  function tell(d, e) {          /* the error, reported once per document */
    if (TOLD[d]) return; TOLD[d] = true;
    if (root.console && console.error) console.error("FG " + d + ": the file is printed still: " + (e && e.message || e));
  }

  /* ---------------------------------------------------------- THE WORDMARK (the title card's art)
     The title card's label, XTIX, as the brand sets it: heavy, italic, tight. Canvas, as today:
     the heading's name reaches a screen reader through its aria-label, unchanged. */
  function wordmark(X) {
    var cv = X.querySelector(".dt-art"); if (!cv) return;
    var phone = HOST.w <= 760, px = phone ? 46 : 64, dpr = Math.max(1, devicePixelRatio || 1);
    var cx = cv.getContext("2d"), font = "italic 800 " + px + "px Geist, system-ui, sans-serif";
    var NAME = (X.querySelector(".doctitle") || {}).getAttribute ? X.querySelector(".doctitle").getAttribute("aria-label") : "";
    cx.font = font; var w = Math.ceil(cx.measureText(NAME).width + px * .5), h = Math.ceil(px * 1.08);
    cv.width = w * dpr; cv.height = h * dpr; cv.style.width = w + "px"; cv.style.height = h + "px";
    cx = cv.getContext("2d"); cx.scale(dpr, dpr); cx.font = font; cx.fillStyle = INK; cx.textBaseline = "alphabetic";
    if ("letterSpacing" in cx) cx.letterSpacing = (-.04 * px) + "px";
    cx.fillText(NAME, 2, px * .86);
  }

  /* A RUNTIME THAT THROWS PRINTS THE FILE. plain(): the stylesheet's own final state, without the .js class (the mount
     itself failed, or the still drawing did too): every word painted, nothing hidden until drawn; the title, a canvas,
     is the one word only a script can print. */
  function plain(X, e) {
    var d = X.getAttribute("data-file");
    FAILED[d] = true; tell(d, e);
    X.classList.remove("js"); X.classList.add("still");
    try { wordmark(X); } catch (e2) { tell(d, e2); }
  }
  function fail(X, e) { var m = INST[X.getAttribute("data-file")]; if (m) m.printed(e); else plain(X, e); }

  function build(X) {
  var DOC = X.getAttribute("data-file"), STILL = false, dead = false, shown = false, timers = [], frames = [], rz = 0, plotIO = null, thenIO = null, engIO = null;
  /* the hand this instance draws with: the page's FG, with this opening's stillness in drawOn */
  var FG = Object.create(FG0);
  FG.drawOn = function (p, dur, delay, ease) { return FG0.drawOn(p, dur, delay, ease, STILL); };
  function guard(f) { return function () { try { return f.apply(this, arguments); } catch (e) { printed(e); } }; }
  function later(f, ms) { var t = setTimeout(function () { timers.splice(timers.indexOf(t), 1); guard(f)(); }, ms); timers.push(t); return t; }
  function raf(f) { var r = requestAnimationFrame(function (now) { frames.splice(frames.indexOf(r), 1); guard(f)(now); }); frames.push(r); return r; }
  /* the plate of this document: made here, so nothing of it runs for a section that is not ported */
  var RT = { H: HOST, still: function () { return STILL; }, later: later, raf: raf, guard: guard };
  var PL = root.FGDOC[DOC] ? root.FGDOC[DOC](X, FG, RT) : null;
  X.classList.add("js");      /* without this class the stylesheet prints the plain final state (failsafe) */
  var FILL = "#2FB380", TXT = "#1C6E4E", UV = "#9B7BFF", UVR = "#7a5be0";
  var drawn = [];
  function host(el) { var s = FG.svg(el); drawn.push(s); return s; }
  function grad(s, id, stops, r) {
    var d = FG.el(s, "defs", {}), g = FG.el(d, "radialGradient", { id: id, cx: "50%", cy: "50%", r: r || "50%" });
    stops.forEach(function (st) { FG.el(g, "stop", { offset: st[0], "stop-color": st[1], "stop-opacity": st[2] }); });
  }

  /* ---------------------------------------------------------- the title card's rule: one hand stroke */
  function rule() {
    var r = X.querySelector(".dt-rule"); if (!r) return;
    var s = host(r), P = new FG.Pen("xtix-dt-rule");
    FG.path(s, P.line(1, 4.5, 51, 3.6, { passes: 1, rough: .7, bow: 1.4 }), FILL, 2.6);
  }

  /* ---------------------------------------------------------- THE DOOR LAMP, drawn on its board */
  function lamp() {
    var b = X.querySelector(".lampband"); if (!b) return;
    var s = host(b), P = new FG.Pen("xtix-lamp-board"), W = b.clientWidth, H = b.clientHeight;
    grad(s, DOC + "-lampHalo", [["0%", UV, .55], ["100%", UV, 0]]);
    grad(s, DOC + "-lampWarm", [["0%", UV, 1], ["100%", UV, 0]]);
    grad(s, DOC + "-bulbHi", [["0%", "#fff", .35], ["100%", "#fff", 0]], "60%");
    /* the inner sketch frame, 12px in, corners overshooting */
    FG.path(s, P.rect(12, 12, W - 24, H - 24, { overshoot: 3 }), INK, 1.3);
    /* the header strip's rule */
    FG.path(s, P.line(12, 56, W - 12, 56, { passes: 1, rough: .4 }), INK, .9, { opacity: ".55" });
    /* the lens assembly, centred in the board's middle row */
    var L = FG.box(b.querySelector(".lamp"), b), cx = L.x + L.w / 2, cy = L.y + L.h / 2;
    var k = Math.min(1, (L.h - 16) / 252), R = 104 * k;
    FG.el(s, "circle", { cx: cx, cy: cy, r: 70 * k, fill: "url(#" + DOC + "-lampHalo)", class: "halo" });
    FG.el(s, "circle", { cx: cx, cy: cy, r: 44 * k, fill: "url(#" + DOC + "-lampWarm)", class: "warm" });
    FG.path(s, P.ellipse(cx, cy, R, R, { wobble: .006, steps: 40 }), INK, 1.8);
    [0, 1, 2, 3].forEach(function (q) {
      var a = q * Math.PI / 2 - Math.PI / 2, c = Math.cos(a), sn = Math.sin(a);
      FG.path(s, P.line(cx + c * (R - 11), cy + sn * (R - 11), cx + c * (R + 11), cy + sn * (R + 11), { rough: .3 }), INK, 1.3);
    });
    /* the reflector: exactly three rings, dashed until the lamp reads 03 ZONES */
    [86, 66, 46].forEach(function (r) {
      FG.path(s, P.ellipse(cx, cy, r * k, r * k, { passes: 1, wobble: .01, steps: 16 }), UV, 1.2, { class: "refl", opacity: ".55" });
    });
    /* the bulb, an irregular disc, its rim and its highlight */
    var bp = [], n = 14;
    for (var i = 0; i < n; i++) { var a = i / n * Math.PI * 2, rr = 20 * k * (1 + P.j(.07)); bp.push([cx + Math.cos(a) * rr, cy + Math.sin(a) * rr]); }
    bp.push(bp[0]);
    var bd = P.curve(bp) + "Z";
    FG.path(s, bd, UVR, 1.2, { fill: UV });
    FG.el(s, "circle", { cx: cx - 6 * k, cy: cy - 6 * k, r: 12 * k, fill: "url(#" + DOC + "-bulbHi)" });
    /* the Fresnel lens over the bulb: six hairlines, r = 32·√(n/6) */
    for (var m = 1; m <= 6; m++) {
      var fr = 32 * k * Math.sqrt(m / 6), st = P.R() * Math.PI * 2;
      FG.path(s, P.arc(cx, cy, fr, st, st + Math.PI * 2 + .07, { passes: 1, wobble: .15 }), INK, .6, { opacity: ".5", class: "fres" + (m < 6 ? " inner" : "") });
    }
    /* the paper key: a rough outline that moves with the key, its second pass the hover's */
    var key = b.querySelector(".lampcall"), ks = host(key), KP = new FG.Pen("xtix-lamp-key");
    var kw = key.clientWidth, kh = key.clientHeight;
    FG.path(ks, KP.rect(0, 0, kw, kh, { overshoot: 2, passes: 1 }), INK, 1.4);
    FG.path(ks, KP.rect(0, 0, kw, kh, { overshoot: 2, passes: 1 }), INK, 1.4, { class: "key2" });
  }

  /* ---------------------------------------------------------- the lamp: three whole-string swaps */
  var lb = X.querySelector(".lampband");
  if (lb) lb.addEventListener("click", guard(function () {
    var on = lb.getAttribute("aria-pressed") !== "true";
    lb.setAttribute("aria-pressed", on ? "true" : "false");
    lb.querySelector(".lampcall").firstChild.nodeValue = on ? "FLUORESCING" : "PRESS TO ARM";
    var sub = lb.querySelector(".lampsub"), last = sub.lastChild;
    last.nodeValue = on ? " 03 ZONES" : " LONG WAVE";
    lb.querySelector(".lampstate").textContent = on ? "ON" : "OFF";
    X.classList.toggle("uv", on);
    if (arrowSvg) analystArrow();       /* the head re-lands on the edge now printed (the plate goes with the lamp) */
  }));

  /* ==========================================================================================
     04 · CAP FIRST, SAME CLOTH (judge E5). The one sequence in the file.
     Each bar's first ink is its cap at its TRUE height (from the file's --h); the walls hang from
     it to the ground; the hatch is laid whole line by line from the top-left. Item k in the list is
     laid in the same hatch on the same progress value, so the two can never disagree about k.
     One way, paced to the window (p = how far the chart has come up the viewport), one bar at a
     time, never skipped, never stopped mid-stroke, paused while the chart is off-screen. A built
     bar stays built. Stillness (reduced motion, the shell's still modes) prints all ten, no accent. */
  var M = { built: 0, cur: 0, pmax: 0, running: false, visible: true, accent: 0 };
  var BARS = {}, SWT = {};
  var panel = X.querySelector('.hairtop[data-block="chart"]'), plot = panel && panel.querySelector(".xbars");
  var list = X.querySelector('.z[data-zone="04"] .grid2c'), rows = list ? [].slice.call(list.querySelectorAll(".lg")) : [];

  function plotH() { return parseFloat(getComputedStyle(panel.querySelector(".xchart")).getPropertyValue("--plot")) || 440; }

  function ticks() {          /* the ten brush ticks over the ten ✓, and each row's swatch, laid down hidden */
    rows.forEach(function (row, i) {
      var k = i + 1, s = host(row), P = new FG.Pen("xtix-04-row-" + k), W = row.clientWidth, H = row.clientHeight;
      s.style.zIndex = "-1";
      /* the swatch: the bar's own hatch, behind the row, with a 2px left rule */
      var g = FG.el(s, "g", { class: "sw" }), lines = []; g.style.opacity = "0";
      var hs = P.hachure([[-8, 2], [W - 4, 2], [W - 4, H - 2], [-8, H - 2]], { gap: 5, angle: 49, rough: .4 }).segs;
      hs.sort(function (a, b) { return (a[0] + a[1] + a[2] + a[3]) - (b[0] + b[1] + b[2] + b[3]); });
      hs.forEach(function (sg) { lines.push(FG.path(g, P.line(sg[0], sg[1], sg[2], sg[3], { passes: 1, rough: .4 }), FILL, 1, { opacity: ".35", visibility: "hidden" })); });
      FG.path(g, P.line(-8, 3, -8, H - 3, { passes: 1, rough: .2 }), FILL, 2);
      SWT[k] = { g: g, lines: lines };
      /* the brush tick over the transparent ✓: 18px, 0.7 → 3.4 → 0.6 */
      var c = FG.box(row.querySelector(".c"), row), x = c.x + 1, y = c.y + c.h / 2 - 1, pts = [], ws = [];
      var V = [[x, y], [x + 5.2, y + 5.6], [x + 18, y - 8.4]];
      for (var t = 0; t <= 1.0001; t += .2) { pts.push([V[0][0] + (V[1][0] - V[0][0]) * t, V[0][1] + (V[1][1] - V[0][1]) * t]); ws.push(.7 + (3.4 - .7) * t); }
      for (t = .1; t <= 1.0001; t += .1) { pts.push([V[1][0] + (V[2][0] - V[1][0]) * t + P.j(.15), V[1][1] + (V[2][1] - V[1][1]) * t]); ws.push(3.4 + (.6 - 3.4) * Math.pow(t, .8)); }
      /* the tick stands for the ✓ (text): the document's text tier, on its own layer outside the lamp's
         recede filter, so it reads in both states (the row's --c-text is the armed tier under the lamp) */
      var tl = FG.svg(row, "uv-layer"); drawn.push(tl); tl.style.zIndex = "-1";
      FG.path(tl, P.brush(pts, ws), null, 0, { fill: getComputedStyle(row).getPropertyValue("--c-text").trim() || TXT });
    });
  }

  function chart() {
    if (!plot) return;
    var s = host(plot), P = new FG.Pen("xtix-elevation"), Hp = plotH(), gy = Hp;
    var cols = [].slice.call(plot.querySelectorAll(".xcol"));
    var slots = cols.map(function (c) { var b = FG.box(c, plot), bw = Math.round(b.w * .72); return { x: b.x + (b.w - bw) / 2, w: bw, el: c, bar: c.querySelector(".xbar") }; });
    var x0 = FG.box(cols[0], plot).x - 4, last = FG.box(cols[cols.length - 1], plot), x1 = last.x + last.w + 4;
    /* the ground: solid, except a dashed stretch where each ∅ stands — zero has no height */
    var zs = slots.filter(function (sl) { return !sl.bar; }), cx = x0, solid = "";
    zs.forEach(function (z) {
      solid += P.line(cx, gy, z.x, gy, { rough: .35 });
      FG.path(s, P.line(z.x, gy, z.x + z.w, gy, { passes: 1, rough: .2 }), INK, 1.4, { opacity: ".45", "stroke-dasharray": "3 2", "stroke-linecap": "butt" });
      cx = z.x + z.w;
    });
    solid += P.line(cx, gy, x1, gy, { rough: .35 });
    FG.path(s, solid, INK, 1.4);
    var et = "";
    for (var ex = x0 + 6; ex < x1 - 2; ex += 11) et += P.line(ex, gy + 2.5, ex - 5, gy + 7.5, { passes: 1, rough: .2 });
    FG.path(s, et, INK, .8, { opacity: ".35" });
    /* the ten bars, each in its own group, every stroke its own path so it can be laid in order */
    var k = 0;
    slots.forEach(function (sl) {
      if (!sl.bar) return; k++;
      var hv = parseFloat(sl.bar.style.getPropertyValue("--h")) || 0, h = Hp * hv / 100, x = sl.x, w = sl.w, top = gy - h;
      var BP = new FG.Pen("xtix-bar-" + k), g = FG.el(s, "g", { class: "bar", "data-k": k });
      var dot = FG.el(g, "circle", { cx: x, cy: top, r: .9, fill: TXT });
      var cap = FG.path(g, BP.line(x - 1.5, top, x + w + 1.5, top, { rough: .45 }), TXT, 1.5, { class: "ol" });
      var wl = FG.path(g, BP.line(x, top, x, gy, { rough: .35 }), TXT, 1.5, { class: "ol" });
      var wr = FG.path(g, BP.line(x + w, top, x + w, gy, { rough: .35 }), TXT, 1.5, { class: "ol" });
      var hs = BP.hachure([[x + .8, top + .8], [x + w - .8, top + .8], [x + w - .8, gy - .6], [x + .8, gy - .6]], { gap: 5, angle: 49, rough: .45 }).segs;
      hs.sort(function (a, b) { return (a[0] + a[1] + a[2] + a[3]) - (b[0] + b[1] + b[2] + b[3]); });
      var hatch = hs.map(function (sg) { return FG.path(g, BP.line(sg[0], sg[1], sg[2], sg[3], { passes: 1, rough: .45 }), FILL, 1.1); });
      [cap, wl, wr].forEach(function (p) { p._L = p.getTotalLength(); });
      BARS[k] = { g: g, dot: dot, cap: cap, walls: [wl, wr], hatch: hatch, col: sl.el, top: top, x: x, w: w };
      g.addEventListener("mouseenter", function () { pair(+g.getAttribute("data-k"), true); });
      g.addEventListener("mouseleave", function () { pair(+g.getAttribute("data-k"), false); });
    });
    for (var b = 1; b <= 10; b++) paint(b, b <= M.built ? 1 : (b === M.cur ? M.f || 0 : -1));
  }

  /* lay bar k at time f of its own 520ms timeline (-1: not yet; 1: built) */
  function paint(k, f) {
    var B = BARS[k]; if (!B) return;
    if (f < 0) { B.g.style.display = "none"; return; }
    B.g.style.display = "";
    var t = f * 520, c = Math.min(1, t / 110), w = Math.max(0, Math.min(1, (t - 110) / 160)), hh = Math.max(0, Math.min(1, (t - 270) / 250));
    B.dot.style.opacity = f >= 1 ? 0 : 1;
    dash(B.cap, c); B.walls.forEach(function (p) { dash(p, w); });
    var n = Math.round(hh * B.hatch.length);
    B.hatch.forEach(function (p, i) { p.style.visibility = i < n ? "visible" : "hidden"; });
    var S = SWT[k];
    if (S && M.accent === k) { var m = Math.round(hh * S.lines.length); S.lines.forEach(function (p, i) { p.style.visibility = i < m ? "visible" : "hidden"; }); }
  }
  function dash(p, f) {
    if (f >= 1) { p.style.strokeDasharray = ""; p.style.strokeDashoffset = ""; p.style.visibility = "visible"; return; }
    if (f <= 0) { p.style.visibility = "hidden"; return; }
    p.style.visibility = "visible"; p.style.strokeDasharray = p._L + " " + p._L; p.style.strokeDashoffset = p._L * (1 - f);
  }
  function accent(k) {
    if (M.accent && SWT[M.accent]) { SWT[M.accent].g.style.transition = "opacity .2s"; SWT[M.accent].g.style.opacity = "0"; rows[M.accent - 1].classList.remove("on-accent"); }
    M.accent = k;
    if (list) list.setAttribute("data-accent", k);
    if (k && SWT[k]) { SWT[k].lines.forEach(function (p) { p.style.visibility = "hidden"; }); SWT[k].g.style.transition = "none"; SWT[k].g.style.opacity = "1"; rows[k - 1].classList.add("on-accent"); }
  }

  function queued() { return Math.min(10, Math.floor(M.pmax * 10 + 1e-6)); }
  function next() {
    if (M.running || M.built >= 10 || !M.visible) return;
    if (queued() <= M.built) return;
    var k = M.built + 1, waiting = queued() - k, dur = 520 * (waiting >= 4 ? .35 : waiting >= 2 ? .6 : 1);
    dur = Math.max(220, dur);
    M.running = true; M.cur = k; M.f = 0;
    accent(k);
    var lab = BARS[k] && BARS[k].col; if (lab) lab.classList.add("drawing");
    var t0 = performance.now();
    (function frame(now) {
      var f = Math.min(1, (now - t0) / dur); M.f = f;
      paint(k, f);
      if (f < 1) return raf(frame);
      M.built = k; M.cur = 0; M.running = false;
      var lb2 = BARS[k] && BARS[k].col; if (lb2) lb2.classList.remove("drawing");
      if (k === 10) later(function () { accent(0); }, 600);
      next();
    })(t0);
  }
  function progress() {
    if (!plot || M.built >= 10) return;
    /* paced by the GROUND LINE, not the panel's top: the build starts only when the ground (and so
       every bar's full height above it) is on screen, and runs over the next half-window of scroll.
       (Measured: paced by the panel's top, bar 01 was laid 247px below a 1000px window.) */
    var r = plot.getBoundingClientRect(), vh = HOST.h, ground = r.top + plotH();
    var p = Math.max(0, Math.min(1, (HOST.top + 0.92 * vh - ground) / (0.45 * vh)));
    if (p > M.pmax) { M.pmax = p; next(); }
  }
  /* after the build: item k and bar k answer each other under the pointer (colour and weight only) */
  function pair(k, on) {
    if (M.built < 10 || !BARS[k]) return;
    BARS[k].g.classList.toggle("hl", on); rows[k - 1].classList.toggle("hl", on);
    var S = SWT[k]; if (!S) return;
    S.lines.forEach(function (p) { p.style.visibility = "visible"; });
    S.g.style.transition = "opacity .12s"; S.g.style.opacity = on ? ".57" : "0";     /* .35 lines × .57 ≈ 20% */
  }
  rows.forEach(function (row, i) {
    row.addEventListener("mouseenter", function () { pair(i + 1, true); });
    row.addEventListener("mouseleave", function () { pair(i + 1, false); });
  });
  if (list) list.setAttribute("data-accent", 0);

  /* ==========================================================================================
     PUNCHED THROUGH (judge E2): seven holes, d=14, at the seven empty .o marks — through the card,
     its shadow plate (offset 2.4px: a crescent, the card's thickness) and the sheet. A rough 0.8px
     cut edge rings each hole on the card. */
  function holes() {
    var card = X.querySelector(".reality"), folder = X.querySelector(".folder"); if (!card || !folder) return;
    var os = [].slice.call(card.querySelectorAll(".frow .o")), R = 7;
    function list(host, dx, dy) {
      return os.map(function (o) { var b = FG.box(o, host); return "radial-gradient(circle at " + (b.x + b.w / 2 + dx).toFixed(1) + "px " + (b.y + b.h / 2 + dy).toFixed(1) + "px, transparent " + R + "px, #000 " + (R + .6) + "px)"; }).join(",");
    }
    card.style.setProperty("--holes", list(card, 0, 0));
    /* the plate is translated 8/8; in its own frame the hole sits at centre − 8 + 2.4 */
    card.style.setProperty("--holes-sh", list(card, -8 + 2.4, -8 + 2.4));
    SHEET = list(folder, 0, 0);                  /* the sheet's own holes; pageTurn() writes the list with S2's cut */
    folder.style.setProperty("--sheet-holes", SHEET);
    /* THE HOLE'S WALL UNDER THE LAMP (R2 D3). Armed, the ink plate goes (it would read as a light card
       on the dark sheet), and with it the crescent that made each die-cut a hole. So the crescent is
       drawn: exactly the part of the plate seen through the hole with the lamp off — the hole's disc about
       c outside the plate's own hole about c' = c + (2.4, 2.4), the card's thickness on the upper-left wall,
       never a filled bullet. Radii as the two cuts print (each mask runs clear to 7px, solid from 7.6px):
       the wall reaches the card's solid edge (7.6 about c) and stops at the plate cut's middle (7.3 about
       c'), so armed it matches the lamp-off crescent (measured at 4x: within 0.5px). Two arcs between the
       circles' meeting points: the long arc of c round the upper left, back along the short arc of c'.
       Shown only armed (xtix.css), under the cut-edge rings as the plate is. */
    var hs = FG.svg(card, "fg-hole-sh"); drawn.push(hs);
    os.forEach(function (o) {
      var b = FG.box(o, card), cx = +(b.x + b.w / 2).toFixed(1), cy = +(b.y + b.h / 2).toFixed(1), Ra = 7.6, Rb = 7.3;
      var dd = Math.hypot(2.4, 2.4), ux = 2.4 / dd, uy = 2.4 / dd, a = (dd * dd + Ra * Ra - Rb * Rb) / (2 * dd), hh = Math.sqrt(Ra * Ra - a * a);
      var mx = cx + a * ux, my = cy + a * uy, p1 = [mx + hh * uy, my - hh * ux], p2 = [mx - hh * uy, my + hh * ux];   /* upper right, lower left */
      FG.el(hs, "path", { fill: "#060608", d: "M" + p1[0].toFixed(2) + " " + p1[1].toFixed(2) + "A" + Ra + " " + Ra + " 0 1 0 " + p2[0].toFixed(2) + " " + p2[1].toFixed(2) +
        "A" + Rb + " " + Rb + " 0 0 1 " + p1[0].toFixed(2) + " " + p1[1].toFixed(2) + "Z" });
    });
    var s = host(card), P = new FG.Pen("xtix-07-holes");
    os.forEach(function (o) { var b = FG.box(o, card); FG.path(s, P.ellipse(b.x + b.w / 2, b.y + b.h / 2, R, R, { passes: 1, wobble: .03, steps: 10 }), INK, .8, { opacity: ".55" }); });
  }

  /* ==========================================================================================
     THE PAGE-TURN (R2 S2). PART 2 OF 2 begins a second sheet. The paper is cut across between the acts:
     sheet 1 ends a foot (--fg-foot) below its last piece, a band of drafting table (--fg-gap) shows
     between the two sheets, and sheet 2 begins a head (--fg-padt) above its first header row, as sheet 1
     does. The PART 2 label lies on the table in that band, at the sheets' edge, as PART 1's lies above the
     first sheet (xtix.css). The cut is one more layer on the sheet's own mask list (--sheet-holes): the
     paper, the armed plate and the lamp's threads all read that list, so the band is lit table in both
     lamp states and nothing violet crosses it. E = the hairtop holding the PART 2 label (XTIX's evidence,
     OASIS's PART 2 block); a file without one gets only its holes. Read from E's own box at every draw
     (resize, fonts, lamp: on phones the developed zones open in the flow and move E). No text, no id. */
  var SHEET = "", TURN = null;
  function pageTurn() {
    var folder = X.querySelector(".folder"); if (!folder) return;
    var E = null, layers = SHEET ? [SHEET] : [];
    [].forEach.call(folder.children, function (c) { if (!E && c.classList.contains("hairtop") && c.querySelector(":scope>.plabel.pl2")) E = c; });
    TURN = null;
    if (E) {
      var cs = getComputedStyle(X), padt = parseFloat(cs.getPropertyValue("--fg-padt")) || 56, gap = parseFloat(cs.getPropertyValue("--fg-gap")) || 112;
      var et = FG.box(E, folder).y, A = et - padt - gap, B = et - padt;
      TURN = { E: E, top: et, A: A, B: B };
      /* the foot shadow and the edge (E::before, E::after) take the SHEET's width, not E's (R2 review fix: XTIX's
         evidence block outgrows the content box at 1100-1199, and an E-sized band hung past the paper) */
      E.style.setProperty("--fg-sheetw", folder.clientWidth + "px");
      layers.push("linear-gradient(#000 0 " + A.toFixed(2) + "px,transparent " + A.toFixed(2) + "px " + B.toFixed(2) + "px,#000 " + B.toFixed(2) + "px)");
    }
    if (layers.length) folder.style.setProperty("--sheet-holes", layers.join(",")); else folder.style.removeProperty("--sheet-holes");
  }

  /* ==========================================================================================
     THE PROMISE LINE and its TWIN (judge E3 + E6). Under exactly the words 'commercial operating
     system' in 02 (the file's <b>), a DASHED emerald hand line: in this file dashed means "not yet".
     Under exactly 'COMMERCIAL OPERATING SYSTEM' in the caption '… — BUILT', the same stroke SOLID.
     No connector runs between them; the rhyme is the only link, and the file states both lines.
     Each follows its words' own line boxes (a Range), so a wrap cannot strand it. */
  function baselineOf(el) {
    var cs = getComputedStyle(el), cx = document.createElement("canvas").getContext("2d");
    cx.font = cs.fontStyle + " " + cs.fontWeight + " " + cs.fontSize + " " + cs.fontFamily;
    var m = cx.measureText("Hxg");
    return { desc: m.fontBoundingBoxDescent || parseFloat(cs.fontSize) * .25 };
  }
  function underWords(hostEl, range, seed, o) {
    var s = host(hostEl), P = new FG.Pen(seed), hb = hostEl.getBoundingClientRect(), bl = baselineOf(range.startContainer.parentElement);
    [].forEach.call(range.getClientRects(), function (r) {
      if (r.width < 2) return;
      var x1 = r.left - hb.left - 3, x2 = r.right - hb.left + 3, y = r.bottom - hb.top - bl.desc + o.below, d = "";
      if (o.dash) {
        for (var x = x1; x < x2 - 2; x += o.dash[0] + o.dash[1]) {
          var e = Math.min(x2, x + o.dash[0]), bow = Math.sin((x - x1) / (x2 - x1) * Math.PI) * 1.2;
          d += P.line(x, y + bow + P.j(.3), e, y + bow + P.j(.3), { passes: 1, rough: .35 });
        }
      } else {
        d = P.curve([[x1, y + P.j(.4)], [(x1 + x2) / 2, y + 1.3], [x2, y + P.j(.4)]]);
      }
      FG.path(s, d, FILL, o.w, { class: o.cls || "" });
    });
  }
  function promise() {
    var b = X.querySelector('.z[data-zone="02"] > .para b');
    if (b) { var r = document.createRange(); r.selectNodeContents(b); underWords(b.closest(".para"), r, "xtix-02-promise", { dash: [9, 6], below: 6, w: 2.2 }); }
    var cap = X.querySelectorAll(".statrow .biglbl")[1];
    if (cap) {
      /* the dash may sit inside a tag ('SYSTEM —' is held in span.nw): search every text node */
      var tw = document.createTreeWalker(cap, NodeFilter.SHOW_TEXT), tn, end = null;
      while ((tn = tw.nextNode())) { var k2 = tn.nodeValue.indexOf(" —"); if (k2 >= 0) { end = [tn, k2]; break; } }
      if (end) { var r2 = document.createRange(); r2.setStart(cap.firstChild, 0); r2.setEnd(end[0], end[1]); underWords(cap, r2, "xtix-A-built", { below: 5, w: 2.2 }); }
    }
    /* the facts' short emerald rules: the two perf rows, then the three figures (document order keeps the perf rows at
       i = 0 and 1, so their seeds and hands are unchanged; the figures take xtix-fact-2, -3, -4) */
    [].forEach.call(X.querySelectorAll(".statrow .prow, .gaug .g1"), function (p, i) {
      var s = host(p), P = new FG.Pen("xtix-fact-" + i);
      FG.path(s, P.line(0, 1.5, 28, 1, { passes: 1, rough: .5 }), FILL, 2);
    });
  }

  /* ==========================================================================================
     HUNG FROM THE COLON (judge E4). Graphite (one pass, grain) for construction; ink only where the
     file says execution began. The underline is drawn ONCE, after the six, when the line is in view
     (Oran said yes, 2026-10-15); in stillness it is simply there. */
  var thenDone = false;
  function approach() {
    FG.defs();
    var lead = X.querySelector('.z[data-zone="03"] > .para b'), apl = X.querySelector('.z[data-zone="03"] > .apl'), then = X.querySelector('.z[data-zone="03"] > .then');
    if (!lead || !apl) return;
    var HB = "#6f6658", s = host(apl), P = new FG.Pen("xtix-03-string"), ab = apl.getBoundingClientRect();
    var tags = [].slice.call(apl.querySelectorAll(".dash")), phone = HOST.w < 1100;
    /* the colon's lower dot */
    var tn = lead.lastChild, k = tn.nodeValue.lastIndexOf(":"), r = document.createRange(); r.setStart(tn, k); r.setEnd(tn, k + 1);
    var cr = r.getBoundingClientRect(), bl = baselineOf(lead), cx = cr.left + cr.width * .42 - ab.left, cy = cr.bottom - bl.desc - 2 - ab.top;
    var G = { opacity: ".85", filter: "url(#fg-graphite)" };
    function pencil(d, w) { return FG.path(s, d, HB, w || 1.1, G); }
    if (!phone) {
      var sy = 0, pts = [], att = [cx].concat(tags.map(function (t) { var b = FG.box(t, apl); return b.x + b.w / 2; })).sort(function (a, b) { return a - b; });
      pencil(P.line(cx, cy, cx + P.j(.6), sy, { passes: 1, rough: .4 }));            /* the drop from the colon */
      var xs = [0].concat(att).concat([apl.clientWidth]), d = "M0 " + sy;
      for (var i = 1; i < xs.length; i++) { var m = (xs[i - 1] + xs[i]) / 2; d += "Q" + m.toFixed(1) + " " + (sy + 8).toFixed(1) + " " + xs[i].toFixed(1) + " " + sy; }   /* sags 4px between supports */
      pencil(d);
      tags.forEach(function (t, n) {
        var b = FG.box(t, apl), x = b.x + b.w / 2, TP = new FG.Pen("xtix-03-tag-" + n);
        pencil(TP.line(x, sy, x + TP.j(.5), b.y, { passes: 1, rough: .3 }));
        FG.el(s, "circle", { cx: x, cy: sy + .4, r: 1.6, fill: HB });
        pencil(TP.rect(b.x, b.y, b.w, b.h, { overshoot: 6 + TP.R() * 3, passes: 1, rough: .5 }), 1.5);
      });
    } else {
      /* phone: the string runs down the left edge; each tag hangs sideways on a short thread */
      var lx = 12, top = cy, last = FG.box(tags[tags.length - 1], apl);
      var dy = Math.max(cy + 14, -6);
      pencil(P.line(cx, cy, cx + P.j(.4), dy, { passes: 1, rough: .3 }));            /* the drop from the colon */
      pencil(P.line(cx, dy, lx, dy + 2, { passes: 1, rough: .4 }));
      pencil(P.line(lx, dy + 2, lx + P.j(.6), last.y + last.h / 2, { passes: 1, rough: .4 }));
      tags.forEach(function (t, n) {
        var b = FG.box(t, apl), y = b.y + b.h / 2, TP = new FG.Pen("xtix-03-tag-" + n);
        pencil(TP.line(lx, y, b.x, y + TP.j(.4), { passes: 1, rough: .3 }));
        FG.el(s, "circle", { cx: lx, cy: y, r: 1.6, fill: HB });
        pencil(TP.rect(b.x, b.y, b.w, b.h, { overshoot: 5 + TP.R() * 3, passes: 1, rough: .5 }), 1.5);
      });
    }
    /* the zone's only ink: one confident stroke under the closing line, ~110% of its width, a 4px bow, the pen's pool where it touched down */
    if (then) {
      var ts = host(then), UP = new FG.Pen("xtix-03-then"), w = then.clientWidth, h = then.clientHeight, ext = w * .05;
      var y = h - 2, path = FG.path(ts, UP.curve([[-ext, y + UP.j(.5)], [w * .5, y + 4], [w + ext, y - 1]]), FILL, 2.6);
      var pool = FG.el(ts, "circle", { cx: -ext, cy: y, r: 1.6, fill: FILL });
      if (thenIO) { thenIO.disconnect(); thenIO = null; }       /* the previous draw's: one observer at a time */
      if (!thenDone) {
        path.style.visibility = "hidden"; pool.style.visibility = "hidden";
        var io = thenIO = new IntersectionObserver(guard(function (es) {
          if (!es[0].isIntersecting || es[0].intersectionRatio < .6 || thenDone) return;
          thenDone = true; io.disconnect(); thenIO = null;
          path.style.visibility = ""; pool.style.visibility = "";
          var L = path.getTotalLength(); FG.drawOn(path, Math.max(160, Math.min(900, L / 1.6)), 120);
        }), { root: HOST.root, threshold: [0, .6, 1] });
        io.observe(then);
      }
    }
  }

  /* ==========================================================================================
     THE STAMPED TICKET (judge E10). Die-cut by mask (half-moon notches r=9 top and bottom, a
     perforation of r=1.4 holes every 7px, at the stub's edge; mirrored on the back), the outline
     drawn along the cut, one height for both faces, a shadow plate that shares the cut and lifts
     with |cos θ| as the ticket turns. The faces keep today's words and accessibility exactly. */
  var SF = { turned: false, busy: false };
  /* the die: notches and perforation at sx; `also` repeats the ticket's own cut on the shadow plate
     (offset back by the plate's 8/8), so through every hole and notch one sees the sheet, not ink */
  function cutURI(W, H, sx, also) {
    var c = "", cuts = [[sx, 0]];          /* [x of the cut, vertical offset] */
    if (also) cuts.push(also);
    cuts.forEach(function (o) {
      var x = o[0], dy = o[1];
      c += "<circle cx='" + x + "' cy='" + dy + "' r='9' fill='black'/><circle cx='" + x + "' cy='" + (H + dy) + "' r='9' fill='black'/>";
      for (var y = 16; y < H - 14; y += 7) c += "<circle cx='" + x + "' cy='" + (y + dy) + "' r='1.4' fill='black'/>";
    });
    var svg = "<svg xmlns='http://www.w3.org/2000/svg' width='" + W + "' height='" + H + "'><defs><mask id='m'><rect width='" + W + "' height='" + H + "' fill='white'/>" + c +
      "</mask></defs><rect width='" + W + "' height='" + H + "' fill='black' mask='url(#m)'/></svg>";
    return 'url("data:image/svg+xml,' + encodeURIComponent(svg) + '")';
  }
  function cutOutline(W, H, sx) {
    return "M0.6 0.6H" + (sx - 9) + "A9 9 0 0 0 " + (sx + 9) + " 0.6H" + (W - .6) + "V" + (H - .6) + "H" + (sx + 9) + "A9 9 0 0 0 " + (sx - 9) + " " + (H - .6) + "H0.6Z";
  }
  /* THE PORTRAIT TICKET (R2 S5) was not taken up (Oran, 2026-10-24): por stays false, the ticket keeps its landscape form. */
  function bandURI(W, H, band, also) {
    var c = "", cuts = [[0, 0]];          /* [x offset, y offset]: the face's own cut; `also` repeats the ticket's on the plate */
    if (also) cuts.push(also);
    cuts.forEach(function (o) {
      var dx = o[0], y = band + o[1];
      c += "<circle cx='" + dx + "' cy='" + y + "' r='9' fill='black'/><circle cx='" + (W + dx) + "' cy='" + y + "' r='9' fill='black'/>";
      for (var x = 16; x < W - 14; x += 7) c += "<circle cx='" + (x + dx) + "' cy='" + y + "' r='1.4' fill='black'/>";
    });
    var svg = "<svg xmlns='http://www.w3.org/2000/svg' width='" + W + "' height='" + H + "'><defs><mask id='m'><rect width='" + W + "' height='" + H + "' fill='white'/>" + c +
      "</mask></defs><rect width='" + W + "' height='" + H + "' fill='black' mask='url(#m)'/></svg>";
    return 'url("data:image/svg+xml,' + encodeURIComponent(svg) + '")';
  }
  function bandOutline(W, H, band) {
    return "M0.6 0.6H" + (W - .6) + "V" + (band - 9) + "A9 9 0 0 0 " + (W - .6) + " " + (band + 9) + "V" + (H - .6) + "H0.6V" + (band + 9) + "A9 9 0 0 0 0.6 " + (band - 9) + "Z";
  }
  function ticket() {
    var sf = X.querySelector(".slipflip"); if (!sf) return;
    var stage = sf.querySelector(".sf-stage"), front = sf.querySelector(".sf-front"), back = sf.querySelector(".sf-back");
    var por = false;
    sf.classList.toggle("fg-portrait", por);
    ["--th", "--thf", "--thb", "--ths", "--thp"].forEach(function (p) { sf.style.removeProperty(p); });
    var W = front.offsetWidth, ST = parseFloat(getComputedStyle(sf).getPropertyValue("--stub")) || 72, th, band = 0, hf, hb;
    if (por) {
      /* each face measured alone (xtix.css lets each take its own height), then held to it */
      band = parseFloat(getComputedStyle(sf).getPropertyValue("--band")) || 46;
      hf = Math.ceil(front.offsetHeight); hb = Math.ceil(back.offsetHeight); th = SF.turned ? hb : hf;
      SF.hf = hf; SF.hb = hb;
      sf.style.setProperty("--thf", hf + "px"); sf.style.setProperty("--thb", hb + "px");
      sf.style.setProperty("--ths", th + "px"); sf.style.setProperty("--thp", th + "px");
      sf.style.setProperty("--cut-front", bandURI(W, hf, band)); sf.style.setProperty("--cut-back", bandURI(W, hb, band));
      sf.style.setProperty("--cut-plate-front", bandURI(W, hf, band, [-8, -8]));
      sf.style.setProperty("--cut-plate-back", bandURI(W, hb, band, [-8, -8]));
    } else {
    th = Math.ceil(Math.max(front.offsetHeight, back.offsetHeight));
    sf.style.setProperty("--th", th + "px");
    var cf = cutURI(W, th, ST), cb = cutURI(W, th, W - ST);
    sf.style.setProperty("--cut-front", cf); sf.style.setProperty("--cut-back", cb);
    sf.style.setProperty("--cut-plate-front", cutURI(W, th, ST, [ST - 8, -8]));
    sf.style.setProperty("--cut-plate-back", cutURI(W, th, W - ST, [W - ST - 8, -8]));
    }
    var plate = stage.querySelector(".sf-plate");
    if (!plate) { plate = document.createElement("div"); plate.className = "sf-plate"; plate.setAttribute("aria-hidden", "true"); stage.insertBefore(plate, stage.firstChild); }
    if (SF.turned) { plate.style.webkitMask = plate.style.mask = "var(--cut-plate-back) 0 0/100% 100% no-repeat"; }
    if (!sf.querySelector(".sf-ear")) { var ear = document.createElement("i"); ear.className = "sf-ear"; ear.setAttribute("aria-hidden", "true"); stage.appendChild(ear); }
    if (!back.querySelector(".sf-ghost")) { var gh = document.createElement("i"); gh.className = "sf-ghost"; gh.setAttribute("aria-hidden", "true"); back.appendChild(gh); }
    /* the outline along the cut, on each face (portrait: each at its own height, the notches in the side edges) */
    [[front, ST, hf], [back, W - ST, hb]].forEach(function (fs) {
      var s = host(fs[0]); FG.path(s, por ? bandOutline(W, fs[2], band) : cutOutline(W, th, fs[1]), INK, 1.3);
    });
    /* the control: a rough paper-key outline */
    var tab = sf.querySelector(".sf-tab"), ks = host(tab), KP = new FG.Pen("xtix-turn-key");
    FG.path(ks, KP.rect(0, 0, tab.offsetWidth, tab.offsetHeight, { overshoot: 2, passes: 1 }), INK, 1.3);
    arrowSvg = null; analystArrow();
  }
  /* THE ANALYST'S ARROW. Drawn with the ticket; when the lamp arms or disarms, the ticket's shadow plate
     is taken away or given back at once, and the head re-lands on the edge that is then printed (same
     svg, same stroke, no motion of its own). */
  var arrowSvg = null;
  function analystArrow() {
    if (arrowSvg && arrowSvg.isConnected) while (arrowSvg.firstChild) arrowSvg.removeChild(arrowSvg.firstChild);
    /* the analyst's arrow (Oran's answer 9, 2026-10-16): one tapered rust stroke from beside the note's
       first line, rising past the note's header and swinging up to the ticket's lower edge LEFT of the
       turn key, its open head ON that edge and pointing into the ticket. It is laid out in page
       coordinates and mapped into the note's own (turned) frame, so the head lands exactly: on the
       paper's edge, or, where the ink shadow plate lies under the ticket, on the plate's (+8px), which the lamp takes away. It
       bows left only as far as the sheet allows, never over the die-cut notches, never across the key
       or any word. On phones the key keeps a 44px lane at its left (xtix.css), so the arrow is drawn
       at every width, the same way. If a lane were ever missing it is not drawn at all. */
    var note = X.querySelector(".an-note"), nt = note && note.querySelector(".an-t"), nh = note && note.querySelector(".an-h");
    var sf = X.querySelector(".slipflip"), stage = sf && sf.querySelector(".sf-stage"), tab = sf && sf.querySelector(".sf-tab");
    if (note && nt && nh && stage && tab) {
      var ST = parseFloat(getComputedStyle(sf).getPropertyValue("--stub")) || 72, lit = X.classList.contains("uv");
      var nb = note.getBoundingClientRect(), hb = nh.getBoundingClientRect(), lb2 = nt.getBoundingClientRect(), tb = stage.getBoundingClientRect();
      var kb = tab.getBoundingClientRect(), fb = X.querySelector(".folder").getBoundingClientRect();
      var xmin = fb.left + 9, n1 = tb.left + ST, n2 = n1 + 8;
      var A0 = [Math.max(fb.left + 14, lb2.left - 6), lb2.top + 16];                      /* beside the first line */
      var th2 = 50 * Math.PI / 180, bow = Math.max(0, Math.min(46, A0[0] - xmin));
      /* where the sheet lets it bow left first, it reaches 150px (the desktop's sweep); where it cannot
         (a phone's 20px margin), it reaches only as far as one clean bend allows (the chord steeper than
         the landing), which on every phone lands it on the stub */
      var reach = bow >= 20 ? 1e9 : (A0[1] - tb.bottom - 8) / Math.tan(th2 + 8 * Math.PI / 180);
      var tx = Math.min(nb.left + 150, A0[0] + reach, kb.left - 29);                       /* left of the key (and its 3px shadow) */
      if (!sf.classList.contains("fg-portrait") && tx > n1 - 22 && tx < n2 + 22) tx = n1 - 22;   /* clear of the notches: onto the stub (S5's portrait ticket has none on its lower edge) */
      tx = Math.max(tb.left + 16, tx);
      var A3 = [tx, tx >= tb.left + 8 && !lit ? tb.bottom + 8 : tb.bottom];   /* under the lamp the plate is gone: the paper's edge */
      /* it lands at 50deg, or 10deg under its chord where the sweep is long, so the stroke bends one way
         only (the desktop's C), never shallower than 28deg: the head always points up into the ticket */
      var chord = Math.atan2(A0[1] - A3[1], A3[0] - A0[0]) * 180 / Math.PI;
      th2 = Math.max(28, Math.min(50, chord - 10)) * Math.PI / 180;
      var rise = A0[1] - A3[1], hl = Math.min(110, .55 * Math.hypot(A3[0] - A0[0], rise), (nb.top - 12 - A3[1]) / Math.sin(th2));   /* the landing begins above the note */
      var A2 = [Math.max(xmin, A3[0] - hl * Math.cos(th2)), A3[1] + hl * Math.sin(th2)], A1 = null, raw = [];
      var at = function (P0, P1, P2, P3, t) { var u = 1 - t; return [u * u * u * P0[0] + 3 * u * u * t * P1[0] + 3 * u * t * t * P2[0] + t * t * t * P3[0], u * u * u * P0[1] + 3 * u * u * t * P1[1] + 3 * u * t * t * P2[1] + t * t * t * P3[1]]; };
      for (var k = 8; k <= rise * 2; k += 4) {              /* lengthen the rise until it clears the note's header and first line by 4px */
        var C1 = [A0[0] - bow, A0[1] - k], ok = true;     /* (and never climbs past the edge it lands on) */
        for (var q = 0; q <= 60 && ok; q++) { var P = at(A0, C1, A2, A3, q / 60); if ((P[1] > nb.top - 4 && P[0] > hb.left - 4) || P[1] < A3[1] - .5) ok = false; }
        if (ok) { A1 = C1; break; }
      }
      if (A1) for (var t = 0; t <= 60; t++) {
        var P2 = at(A0, A1, A2, A3, t / 60); raw.push(P2);
        if (P2[0] > kb.left - 12 && P2[1] > kb.top - 8 && P2[1] < kb.bottom + 8) { raw = []; break; }   /* never across the key */
      }
      if (raw.length) {
        if (!arrowSvg || !arrowSvg.isConnected) arrowSvg = host(note);
        var s2 = arrowSvg, AP = new FG.Pen("xtix-analyst-arrow"), toNote = frameOf(note), pts = [], ws = [];
        raw.forEach(function (p, i) { if (i % 3 === 0 || i === raw.length - 1) { pts.push(toNote(p[0], p[1])); ws.push(3 - 2.2 * i / (raw.length - 1)); } });
        FG.path(s2, AP.brush(pts, ws), null, 0, { fill: "#b4532f" });
        var a = Math.atan2(A3[1] - A2[1], A3[0] - A2[0]), e = toNote(A3[0], A3[1]);                    /* the head along the stroke's own end tangent */
        var h1 = toNote(A3[0] - 9 * Math.cos(a - .5), A3[1] - 9 * Math.sin(a - .5)), h2 = toNote(A3[0] - 9 * Math.cos(a + .5), A3[1] - 9 * Math.sin(a + .5));
        FG.path(s2, AP.line(e[0], e[1], h1[0], h1[1], { passes: 1, rough: .3 }) + AP.line(e[0], e[1], h2[0], h2[1], { passes: 1, rough: .3 }), "#b4532f", 1.6);
      }
    }
  }
  /* an element's own frame under its CSS transform (the analyst note is turned about a degree):
     page point -> the element's local px, where its svg draws */
  function frameOf(el) {
    var cs = getComputedStyle(el), M = new DOMMatrix(cs.transform === "none" ? undefined : cs.transform), o = cs.transformOrigin.split(" ").map(parseFloat);
    var w = el.offsetWidth, h = el.offsetHeight, xs = [], ys = [];
    [[0, 0], [w, 0], [0, h], [w, h]].forEach(function (c) { var p = M.transformPoint(new DOMPoint(c[0] - o[0], c[1] - o[1])); xs.push(p.x + o[0]); ys.push(p.y + o[1]); });
    var b = el.getBoundingClientRect(), L = [b.left - Math.min.apply(null, xs), b.top - Math.min.apply(null, ys)], Mi = M.inverse();
    return function (x, y) { var p = Mi.transformPoint(new DOMPoint(x - L[0] - o[0], y - L[1] - o[1])); return [p.x + o[0], p.y + o[1]]; };
  }
  function bez(p1x, p1y, p2x, p2y) {
    function cx(t, a, b) { return 3 * a * t * (1 - t) * (1 - t) + 3 * b * t * t * (1 - t) + t * t * t; }
    return function (x) { var t = x; for (var i = 0; i < 8; i++) { var e = cx(t, p1x, p2x) - x, d = (cx(t + 1e-4, p1x, p2x) - cx(t, p1x, p2x)) / 1e-4; if (!d) break; t -= e / d; t = Math.max(0, Math.min(1, t)); } return cx(t, p1y, p2y); };
  }
  var ease = bez(.45, 0, .2, 1);
  var tabEl = X.querySelector(".sf-tab");
  if (tabEl) tabEl.addEventListener("click", guard(function () {
    if (SF.busy) return;
    var sf = X.querySelector(".slipflip"), inn = sf.querySelector(".sf-in"), plate = sf.querySelector(".sf-plate"), to = !SF.turned;
    function labels() {
      tabEl.setAttribute("aria-pressed", to ? "true" : "false");
      tabEl.querySelector("b").textContent = to ? "TURN BACK" : "TURN THE SHEET";
      tabEl.querySelector(".sf-sub").textContent = to ? "THE CLAIM AND ITS FIGURES" : "HOW THIS CLAIM WAS BUILT";
      sf.classList.toggle("turned", to); SF.turned = to;
    }
    var por = sf.classList.contains("fg-portrait");
    function pose(deg) {
      inn.style.transform = "rotateY(" + deg + "deg)";
      var c = Math.abs(Math.cos(deg * Math.PI / 180));
      plate.style.transform = "translate(" + (8 * c).toFixed(2) + "px," + (8 * c).toFixed(2) + "px) scaleX(" + c.toFixed(3) + ")";
      var m = (deg > 90 ? "var(--cut-plate-back)" : "var(--cut-plate-front)") + " 0 0/100% 100% no-repeat";
      plate.style.webkitMask = m; plate.style.mask = m;
      if (por) sf.style.setProperty("--thp", (deg > 90 ? SF.hb : SF.hf) + "px");    /* S5: the plate is the height of the face that shows */
    }
    /* S5 (portrait): the faces differ in height, so the stage's height eases on the turn's own clock (e = the turn's
       eased progress, 90deg at .5), anchored at the top, and the content below glides. It moves while the SHORTER face
       is the one showing (growing before the turn passes 90deg, shrinking after it), so the turning ticket never lies
       over the key or the note below it; smoothstep within that half. Monotonic; exact at the end. */
    function stageH(e) {
      if (!por) return;
      var h0 = to ? SF.hf : SF.hb, h1 = to ? SF.hb : SF.hf, k = h1 > h0 ? Math.min(1, e / .5) : Math.max(0, (e - .5) / .5);
      k = k * k * (3 - 2 * k);
      sf.style.setProperty("--ths", (h0 + (h1 - h0) * k).toFixed(2) + "px");
    }
    /* ...and the lamp's strings that the glide would carry past their words are held back until the ticket settles,
       then every string is drawn again (with the analyst's arrow and S2's cut) where the turn has left things */
    function settled() {
      if (!por) return;
      if (thrSvg) [].forEach.call(thrSvg.children, function (g) { g.style.visibility = ""; });
      analystArrow(); pageTurn(); threads();
    }
    var a0 = to ? 0 : 180, a1 = to ? 180 : 0;
    if (STILL) { pose(a1); stageH(1); labels(); settled(); return; }
    if (por && thrSvg) {
      var ft = X.querySelector(".folder").getBoundingClientRect().top, st = sf.querySelector(".sf-stage").getBoundingClientRect().top - ft;
      [].forEach.call(thrSvg.children, function (g) { var bb = g.getBBox(); if (bb.y + bb.height > st) g.style.visibility = "hidden"; });
    }
    SF.busy = true; sf.classList.add("busy"); var t0 = performance.now();
    SF.land = function (cut) {            /* the end of the turn; a close in flight lands it at once */
      SF.land = null;
      if (cut) { pose(a1); stageH(1); }
      labels(); settled(); SF.busy = false; sf.classList.remove("busy");
    };
    (function frame(now) {
      var f = Math.min(1, (now - t0) / 600), e = ease(f); pose(a0 + (a1 - a0) * e); stageH(e);
      if (f < 1) return raf(frame);
      SF.land();
    })(t0);
  }));

  /* ==========================================================================================
     THE PEN COMES HOME (judge E8). One ink line: the file's five arrows in file order, then the
     file's return arc from OUTREACH back to LEAD as a phantom line (14 4 2 4 2 4). Tier 1 (Oran's
     yes, 2026-10-15): when the panel is 40% in view, the pen draws it ONCE in that order — the five
     shafts, then the return (revealed through a solid mask, so the phantom's dashes never crawl),
     closing at LEAD. Stillness and re-entry show it complete. On phone the return appears whole. */
  var engDone = false;
  function engine() {
    var tech = X.querySelector(".tech"), eng = tech && tech.querySelector(".eng"); if (!eng) return;
    var nodes = [].slice.call(eng.querySelectorAll(".eng-n")), loop = eng.querySelector(".eng-loop"), phone = HOST.w < 1100;
    var s = host(eng), P = new FG.Pen("xtix-engine"), B = nodes.map(function (n) { return FG.box(n, eng); });
    /* the panel's sketch frame and the footer hairline, drawn on the whole .tech panel area */
    var ts = host(tech), pr = FG.box(eng, tech), pu = FG.box(tech.querySelector(".pur"), tech), FP = new FG.Pen("xtix-engine-frame");
    FG.path(ts, FP.rect(pr.x + 12, pr.y + 12, pr.w - 24, (pu.y + pu.h) - pr.y - 24, { overshoot: 3 }), INK, 1.4);
    /* the stations */
    B.forEach(function (b, i) {
      var NP = new FG.Pen("xtix-engine-node-" + i), hero = i === 2;
      if (hero) FG.path(s, NP.hachureRect(b.x + 1, b.y + 1, b.w - 2, b.h - 2, { gap: 5, angle: 49, rough: .45 }).d, FILL, 1.1);
      FG.path(s, NP.rect(b.x, b.y, b.w, b.h, { overshoot: 2.5 }), hero ? TXT : INK, hero ? 1.6 : 1.3);
    });
    function head(x, y, a) { return P.line(x, y, x - 8 * Math.cos(a - .5), y - 8 * Math.sin(a - .5), { passes: 1, rough: .25 }) + P.line(x, y, x - 8 * Math.cos(a + .5), y - 8 * Math.sin(a + .5), { passes: 1, rough: .25 }); }
    var shafts = [], heads = [], i;
    for (i = 0; i < B.length - 1; i++) {
      var a = B[i], b = B[i + 1], d, h;
      if (!phone) { var y = a.y + a.h / 2; d = P.line(a.x + a.w + 3, y, b.x - 2, y, { passes: 1, rough: .4 }); h = head(b.x - 2, y, 0); }
      else { var x = a.x + a.w / 2; d = P.line(x, a.y + a.h + 3, x, b.y - 2, { passes: 1, rough: .4 }); h = head(x, b.y - 2, Math.PI / 2); }
      shafts.push(FG.path(s, d, INK, 1.3)); heads.push(FG.path(s, h, INK, 1.3));
    }
    /* the return: OUTREACH → LEAD, a phantom line; its lowest point carries the file's own label */
    var L0 = B[0], L5 = B[B.length - 1], rp, low;
    if (!phone) {
      var rb = L0.y + L0.h + 3, x5 = L5.x + L5.w / 2, x0 = L0.x + L0.w / 2, k = 110 / .75;
      rp = "M" + x5 + " " + rb + "C" + x5 + " " + (rb + k) + " " + x0 + " " + (rb + k) + " " + x0 + " " + (rb + 1);
      low = [(x0 + x5) / 2, rb + 110];
    } else {
      var xr = L0.x + L0.w + 3, yb = L5.y + L5.h / 2, yt = L0.y + L0.h / 2;
      rp = "M" + xr + " " + yb + "C" + (xr + 56) + " " + yb + " " + (xr + 56) + " " + yt + " " + (xr + 2) + " " + yt;
      low = [xr + 42, (yb + yt) / 2];
    }
    var ret = FG.path(s, rp, INK, 1.3, { opacity: ".6", "stroke-dasharray": "14 4 2 4 2 4", "stroke-linecap": "butt" });
    var rh = FG.path(s, phone ? head(L0.x + L0.w + 5, L0.y + L0.h / 2, Math.PI) : head(L0.x + L0.w / 2, L0.y + L0.h + 4, -Math.PI / 2), INK, 1.3, { opacity: ".6" });
    if (loop) {
      if (!phone) { loop.style.left = low[0] + "px"; loop.style.top = (low[1] + 10) + "px"; loop.style.transform = "translate(-50%,0)"; }
      else { loop.style.left = (low[0] + 18) + "px"; loop.style.top = low[1] + "px"; loop.style.transform = "translate(-50%,-50%) rotate(90deg)"; }
    }
    if (engIO) { engIO.disconnect(); engIO = null; }           /* the previous draw's: one observer at a time */
    if (engDone) return;
    /* Tier 1: hidden until the panel is 40% in view, then drawn once in the file's order */
    var mid = "xtix-loop-mask", defs = FG.el(s, "defs", {}), mk = FG.el(defs, "mask", { id: mid, maskUnits: "userSpaceOnUse" });
    var mp = FG.el(mk, "path", { d: rp, stroke: "#fff", "stroke-width": 8, fill: "none" }), ML = mp.getTotalLength();
    ret.setAttribute("mask", "url(#" + mid + ")");
    mp.style.strokeDasharray = ML + " " + ML; mp.style.strokeDashoffset = ML;
    shafts.concat(heads).concat([rh]).forEach(function (p) { p.style.visibility = "hidden"; });
    var io = engIO = new IntersectionObserver(guard(function (es) {
      if (engDone || es[0].intersectionRatio < .4) return;
      engDone = true; io.disconnect(); engIO = null;
      var t = 0;
      shafts.forEach(function (p, n) {
        later(function () { p.style.visibility = ""; FG.drawOn(p, 150, 0).then(function () { heads[n].style.visibility = ""; }); }, t); t += 170;
      });
      later(function () {
        if (phone) { mp.style.strokeDashoffset = 0; rh.style.visibility = ""; return; }
        mp.style.transition = "stroke-dashoffset 900ms cubic-bezier(.45,.05,.25,1)"; mp.getBoundingClientRect(); mp.style.strokeDashoffset = 0;
        later(function () { rh.style.visibility = ""; }, 920);
      }, t + 40);
    }), { root: HOST.root, threshold: [0, .4, 1] });
    io.observe(tech);
  }

  /* THE OVERLAY (judge E9): the vellum's fibre (a wordless layer) and each row's one emerald stroke */
  function vellum() {
    var v = X.querySelector(".refl3"); if (!v) return;
    if (!v.querySelector(".fibre")) { var f = document.createElement("i"); f.className = "fibre"; f.setAttribute("aria-hidden", "true"); v.insertBefore(f, v.firstChild); }
    [].forEach.call(v.querySelectorAll(".dash"), function (d, i) {
      var s = host(d), P = new FG.Pen("xtix-refl-" + i), y = Math.max(2, (d.clientHeight - 30) / 2);
      FG.path(s, P.line(1.5, y, 1.5 + P.j(.4), y + 30, { passes: 1, rough: .3 }), FILL, 3);
    });
  }

  /* ==========================================================================================
     THE LAMP SHOWS ITS SOURCES (judge E11). What lights is a NAMED list — the strings the three
     developed notes quote verbatim — never a pattern (a regex for '07' would also catch bar 07):
       note 1: '07 GAPS' (card), '∅→10' (chart header), '13x' (figure);
       note 3: '~25%', '~40%', '~15%' (the three figures, printed 25% 40% 15% under APPROX. FIGURES) and the
       word 'enterprise' (ringed). */
  var UVC = "#9B7BFF";
  function hostUV(el) { var s = FG.svg(el, "uv-layer"); drawn.push(s); return s; }
  var CITES = { xtix: [".reality .fh>span:last-child", '.hairtop[data-block="chart"] .zr b', ".bignum .cnt", ".gaug .fig", ".cite-word"],
    oasis: [".bignum .cur", ".bignum .cnt", ".cite-word"],          /* note 3: '$2M'; note 2: '06 functions' */
    eventer: [".et .en"],                                           /* notes 1–2: '05', '07', '20' */
    medcoin: [] };                                                  /* its notes quote no printed figure verbatim */
  function cites() {
    (CITES[DOC] || []).forEach(function (q) {
      [].forEach.call(X.querySelectorAll(q), function (e) { e.classList.add("cite"); });
    });
  }

  /* ==========================================================================================
     THE LAMP'S THREADS (R2 S1). The reviewing desk's own links, drawn as violet strings under the lamp.
     Each thread is ONE printed line of a developed note and joins exactly the two things that line names:
     a bracket on each (a 2px spine with its feet toward the words, a knot at its middle) and one dashed
     string between them, laid in the sheet's margin — no arrowheads, no order marks (a link, not a
     sequence). Nothing is drawn with the lamp off (xtix.css keeps the layer hidden; the threads belong to
     the lamp, so daylight shows none either); ?threads=0 draws none. One aria-hidden svg on the sheet,
     clipped to it and masked by the sheet's own list (the holes and S2's gap), so no violet ever reaches
     the table: XTIX's thread is cut where it crosses the act break. Anchors are named (never a pattern)
     and resolved at every draw from the file's own boxes and Ranges.
       xtix    note 1  'Downstream of that list: 13x growth'            the ten systems of 04 (one bracket) -> 13x
       oasis   note 2  'Profitability sits twice'                       02 'Profitability' -> 03 'profitability-based ...'
       eventer note 3  'The first rests on contribution 06 of 07'       'Customer insights became business decisions.' -> 05's 6th of 7
       eventer note 3  'The second rests on 05 departments'             'Growth became ... one team's target.' -> the 05 figure
       medcoin note 1  'Two of them are regulation and providers — the compliant half'
                                                                         the line holding 'compliant' -> 03's 6th and 7th (one bracket) */
  function rectsOf(els) { return [].map.call(els || [], function (e) { return e.getBoundingClientRect(); }).filter(function (q) { return q.height > .5; }); }
  function textRects(el) {           /* an element's own text lines (a ✓, its own absolute mark, left out) */
    if (!el) return null;
    var out = [], w = document.createTreeWalker(el, NodeFilter.SHOW_TEXT), n, r = document.createRange();
    while ((n = w.nextNode())) {
      var c = n.parentElement.closest(".c"); if (!n.data.trim() || (c && el.contains(c))) continue;
      r.selectNodeContents(n); [].push.apply(out, [].slice.call(r.getClientRects()));
    }
    return out.filter(function (q) { return q.width > .5 && q.height > .5; });
  }
  function textAt(root, s) { var w = document.createTreeWalker(root, NodeFilter.SHOW_TEXT), n, i; while ((n = w.nextNode())) if ((i = n.data.indexOf(s)) >= 0) return [n, i]; return null; }
  /* an anchor is its TEXT: the line boxes of the text nodes a Range covers, never the boxes of elements inside it (R2
     review fix: EVENTER's second claim runs to the end of its paragraph, where the lab hangs the claim's own drawing
     layer, an svg as tall as the whole paragraph; a Range's rects included that box, so the second bracket was laid
     from the paragraph's top and only the 4px guard held it below the first) */
  function textLines(p, r) {
    var out = [], w = document.createTreeWalker(p, NodeFilter.SHOW_TEXT), n, q = document.createRange();
    while ((n = w.nextNode())) {
      if (!n.data.trim() || n.parentElement.closest("svg") || (r && !r.intersectsNode(n))) continue;
      q.selectNodeContents(n);
      if (r && n === r.startContainer) q.setStart(n, r.startOffset);
      if (r && n === r.endContainer) q.setEnd(n, r.endOffset);
      [].push.apply(out, [].slice.call(q.getClientRects()));
    }
    return out.filter(function (x) { return x.width > .5 && x.height > .5; });
  }
  function sentence(p, from, to) {   /* the text of p from `from` (or its start) to the end of `to` (or its end) */
    if (!p) return null; var r = document.createRange(), a = from && textAt(p, from), b = to && textAt(p, to);
    if (from) { if (!a) return null; r.setStart(a[0], a[1]); } else r.setStart(p, 0);
    if (to) { if (!b) return null; r.setEnd(b[0], b[1] + to.length); } else r.setEnd(p, p.childNodes.length);
    return textLines(p, r);
  }
  function lineOf(p, word) {         /* the line of p that holds `word`: every text rect of p centred within the word's line */
    var a = p && textAt(p, word); if (!a) return null;
    var wr = document.createRange(); wr.setStart(a[0], a[1]); wr.setEnd(a[0], a[1] + word.length);
    var c = wr.getBoundingClientRect(), q4 = c.height / 4;
    return textLines(p, null).filter(function (q) { var m = (q.top + q.bottom) / 2; return m > c.top + q4 && m < c.bottom - q4; });
  }
  function pick(sel, test) { return [].filter.call(X.querySelectorAll(sel), test)[0] || null; }
  function withList(r, el) { if (r) r.list = el && el.closest(".list"); return r; }
  var THREADS = {
    xtix: [{ lane: "A",
      a: function () { return rectsOf(X.querySelectorAll('.z[data-zone="04"] .grid2c .lg')); },
      b: function () { return textRects(X.querySelector(".statrow .bignum")); } }],
    oasis: [{ lane: "A",
      a: function () { return textRects(pick(".grid2c .dash", function (e) { return e.textContent.trim() === "Profitability"; })); },
      b: function () { return textRects(pick(".list .lg", function (e) { return e.textContent.indexOf("profitability-based") >= 0; })); } }],
    eventer: [{ lane: "B",
      a: function () { return sentence(X.querySelector('.z[data-zone="03"] > .para'), "", "decisions."); },
      b: function () { var l = pick(".list", function (e) { return e.querySelectorAll(":scope>.lg").length === 7; }); var r6 = l && l.querySelectorAll(":scope>.lg")[5]; return r6 ? withList(rectsOf([r6]), r6) : null; } },
      { lane: "A",
      a: function () { return sentence(X.querySelector('.z[data-zone="03"] > .para'), "Growth", ""); },
      b: function () { return rectsOf(X.querySelectorAll(".etr .et:nth-child(2) .en")); } }],
    medcoin: [{ lane: "A",
      a: function () { return lineOf(X.querySelector('.z[data-zone="01"] > .para'), "compliant"); },
      b: function () { var l = X.querySelectorAll('.z[data-zone="03"] .list > .lg'); return l.length >= 7 ? withList(rectsOf([l[5], l[6]]), l[5]) : null; } }]
  };
  var thrSvg = null;
  function n1(v) { return Math.round(v * 10) / 10; }
  /* ONE GLYPH'S INK (the threads' clearance): the letter rastered once in its own computed font (canvas fillText,
     getImageData, as FG.ringFit does), at 4 or more pixels per CSS pixel; its boundary pixels (alpha >= 10%, as
     the eye and the pixel instrument count ink) returned as points in CSS px about its origin: x from its advance
     box's left, y from its baseline (found as FG.ringFit finds it). A face set at an explicit optical size ('opsz'
     in its font-variation-settings: the serif's claims at opsz 72) is rastered at that size and scaled down, since
     the canvas takes its optical size from the font size (the 30px claim measured as the 30px cut is 1-1.5px wider
     than the ink it prints). The text-transform is applied to the character. Cached across draws, per face, optical
     size, PRINTED SIZE and character: the points are in CSS px at the printed size, and a claim set at opsz 72 prints
     at another size on a phone than on a desktop (a cache keyed without the printed size kept the first size's ink
     after a resize: EVENTER at 522, reached from 1237, read the 30px 's' at its desktop size and left both threads
     out; a fresh load at 522 drew them). */
  var INKC = {}, inkCv = null, inkCx = null;
  function glyphInk(ch, cs) {
    if (cs.textTransform === "uppercase") ch = ch.toUpperCase(); else if (cs.textTransform === "lowercase") ch = ch.toLowerCase();
    var fs = parseFloat(cs.fontSize), om = /opsz\D+([\d.]+)/.exec(cs.fontVariationSettings || ""), o = om ? parseFloat(om[1]) : fs, sc = fs / o;
    var font = cs.fontStyle + " " + (cs.fontVariantCaps === "small-caps" ? "small-caps " : "") + cs.fontWeight + " " + o + "px " + cs.fontFamily, key = font + "|" + fs + "|" + ch;
    if (INKC[key]) return INKC[key];
    if (!inkCv) { inkCv = document.createElement("canvas"); inkCx = inkCv.getContext("2d", { willReadFrequently: true }); }
    var c = inkCx; c.setTransform(1, 0, 0, 1, 0, 0); c.font = font;
    var mt = c.measureText(ch), fm = c.measureText("Hxg"), K = Math.max(1, Math.ceil(4 * sc)), pad = Math.ceil(o * .6), B0 = Math.round(o * 1.4);
    inkCv.width = Math.ceil(mt.width + 2 * pad) * K; inkCv.height = Math.ceil(o * 2.2) * K;      /* (a resize clears the context) */
    c.setTransform(K, 0, 0, K, 0, 0); c.font = font; c.textBaseline = "alphabetic"; c.fillStyle = "#000"; c.fillText(ch, pad, B0);
    var W = inkCv.width, H = inkCv.height, px = c.getImageData(0, 0, W, H).data, pts = [], b = [1e9, 1e9, -1e9, -1e9];
    function on(x, y) { return x >= 0 && y >= 0 && x < W && y < H && px[(y * W + x) * 4 + 3] >= 26; }
    for (var y = 0; y < H; y++) for (var x = 0; x < W; x++) {
      if (!on(x, y) || (on(x - 1, y) && on(x + 1, y) && on(x, y - 1) && on(x, y + 1))) continue;
      var X = ((x + .5) / K - pad) * sc, Y = ((y + .5) / K - B0) * sc; pts.push([X, Y]);
      b[0] = Math.min(b[0], X); b[1] = Math.min(b[1], Y); b[2] = Math.max(b[2], X); b[3] = Math.max(b[3], Y);
    }
    return (INKC[key] = { p: pts, b: b, fa: fm.fontBoundingBoxAscent * sc, fd: fm.fontBoundingBoxDescent * sc });
  }
  function threads() {
    var list = THREADS[DOC], folder = X.querySelector(".folder");
    if (!list || !folder) return;
    /* the layer persists across redraws (only its drawing is replaced), so arming the lamp fades it in */
    if (!thrSvg || !thrSvg.isConnected) thrSvg = FG.svg(folder, "uv-layer fg-threads");
    else while (thrSvg.firstChild) thrSvg.removeChild(thrSvg.firstChild);
    /* lamp off (daylight and stillness included): the layer stays, EMPTY, and xtix.css takes it out of rendering
       (display:none); with no drawing in it and no box, nothing of the threads exists to paint, at any width (R2 S1
       close-out). The lamp's own redraw (its capture handler) fills it the frame after arming, inside the fade's
       1s delay. */
    if (!X.classList.contains("uv")) return;
    var fb = folder.getBoundingClientRect(), fcs = getComputedStyle(folder), W = folder.clientWidth;
    var cL = parseFloat(fcs.paddingLeft) || 0, cR = W - (parseFloat(fcs.paddingRight) || 0);
    /* the width-mode from the section's own layout: the phone sheet has 20px margins; the wide sheet sits
       under a two-column cover. Wide: the LEFT margin; below it the analyst's arrow owns the left margin,
       so the threads take the RIGHT one. */
    var phone = cL < 40, wide = getComputedStyle(X).gridTemplateColumns.trim().split(/\s+/).length > 1, s = wide ? -1 : 1, edge = wide ? cL : cR;
    var BX = edge + s * (phone ? 5 : 9), FL = phone ? 3 : 4, LANE = { A: edge + s * (phone ? 10 : 16), B: edge + s * (phone ? 15 : 26) };
    var films = [].map.call(folder.querySelectorAll(":scope>.vfilm"), function (v) { return getComputedStyle(v).display === "none" ? null : v.getBoundingClientRect(); }).filter(Boolean);
    var placed = [];
    /* what of the page reaches into the threads' margin: text runs (kept 4px clear) and boxes (3px). A string is
       never drawn across them: where one would be (XTIX's hero line, as measured on the old figure, ran 15px into a 320px phone's margin, where
       its bracket must stand), that thread is not drawn at that width. */
    var into = function (q) {        /* (what lies in S2's gap is on the table, where the sheet's mask cuts the string: the PART 2 label) */
      if (TURN && q.top - fb.top >= TURN.A - .5 && q.bottom - fb.top <= TURN.B + .5) return false;
      return wide ? q.left - fb.left < cL - .5 : q.right - fb.left > cR + .5; }, intr = [], runs = [];
    (function () {
      var tw = document.createTreeWalker(folder, NodeFilter.SHOW_TEXT), tn, rg = document.createRange();
      while ((tn = tw.nextNode())) {
        if (!tn.data.trim() || tn.parentElement.closest("svg,.tabrow")) continue;
        rg.selectNodeContents(tn);
        var qs = [].filter.call(rg.getClientRects(), function (q) { return q.width > .5; });
        qs.forEach(function (q) { if (into(q)) intr.push([q, 4]); });
        if (qs.length) runs.push([tn, qs]);              /* every text run's lines, for the glyph-ink test below */
      }
      [].forEach.call(folder.querySelectorAll("*"), function (e) {
        /* (the ticket's ink shadow plate is not counted by name: the lamp takes it away, xtix.css #xtix.uv .sf-plate) */
        if (e.closest("svg,.tabrow,.fg-dark") || e.classList.contains("fg-svg") || e.classList.contains("sf-plate")) return;
        var q = e.getBoundingClientRect(); if (q.width && q.height && into(q)) intr.push([q, 3]);
      });
    })();
    function clearOf(segs, knots) {   /* every run of a thread (its brackets' feet and spines, its string) clear of what reaches in */
      return !intr.some(function (it) {
        var q = it[0], x0 = q.left - fb.left - it[1], x1 = q.right - fb.left + it[1], y0 = q.top - fb.top - it[1], y1 = q.bottom - fb.top + it[1];
        if (segs.some(function (sg) { return Math.max(sg[0], sg[2]) > x0 && Math.min(sg[0], sg[2]) < x1 && Math.max(sg[1], sg[3]) > y0 && Math.min(sg[1], sg[3]) < y1; })) return true;
        /* and each knot (a disc r 2.8 at its spine's middle, reaching 2.8px past the spine toward the words; R2 S1
           close-out: at EVENTER 403 a knot stood 3.5px from the 'e' ending its line while the strokes were clear).
           A disc's ink edge is its circle, so it is held to the spec's own 4px (3px from a box), as a distance from
           the glyph's ink box, which holds the ink (the strokes keep their 4.5px square margin about the centre line) */
        var bx0 = q.left - fb.left, bx1 = q.right - fb.left, by0 = q.top - fb.top, by1 = q.bottom - fb.top, kc = Math.min(it[1], 4);
        return knots.some(function (k) { return Math.hypot(Math.max(bx0 - k[0], 0, k[0] - bx1), Math.max(by0 - k[1], 0, k[1] - by1)) - 2.8 < kc; });
      });
    }
    /* THE GLYPHS' INK (R2 S1 close-out). Every point of a thread AS DRAWN (its brackets, its string with the hand's
       bow, each knot's disc) is kept CLR = 4.5px off every letter's INK: the spec's 4px, and half a pixel for the
       measure. The ink is the letter itself, rastered (glyphInk), not its box: a box is the letter's envelope, and
       measured by boxes the threads were left out where the ink stood well clear (EVENTER 470: the bracket's foot
       3.6px from the box of the period ending 'sales target.', 4.7px from its round ink; 388: a 'y' tail's box
       2.5px from the knot, its ink 6.3px). Letters are taken near the thread's own runs (12.5px: the bow, an
       italic's overhang and the clearance), wherever the thread goes (the margin, or a right-column target's
       route across the sheet). The string's points inside S2's gap are not painted (the sheet's mask cuts them). */
    var CLR = 4.5;
    function samples(d) {            /* the points of a drawn path (M, L, C, Q; absolute), every quarter pixel */
      var t = d.match(/[MLCQ]|-?\d*\.?\d+(?:e[-+]?\d+)?/g) || [], out = [], cur = [0, 0], i = 0, c = "", n, s, a, e;
      function take(k) { var r = []; for (var q = 0; q < k; q++) r.push(+t[i++]); return r; }
      while (i < t.length) {
        if (/^[MLCQ]$/.test(t[i])) c = t[i++];
        if (c === "M") { cur = take(2); out.push(cur); }
        else if (c === "L") {
          e = take(2); n = Math.max(1, Math.ceil(Math.hypot(e[0] - cur[0], e[1] - cur[1]) / .25));
          for (s = 1; s <= n; s++) out.push([cur[0] + (e[0] - cur[0]) * s / n, cur[1] + (e[1] - cur[1]) * s / n]);
          cur = e;
        } else if (c === "C") {
          a = take(6); n = Math.max(1, Math.ceil((Math.hypot(a[0] - cur[0], a[1] - cur[1]) + Math.hypot(a[2] - a[0], a[3] - a[1]) + Math.hypot(a[4] - a[2], a[5] - a[3])) / .25));
          for (s = 1; s <= n; s++) { var u = s / n, v = 1 - u;
            out.push([v * v * v * cur[0] + 3 * v * v * u * a[0] + 3 * v * u * u * a[2] + u * u * u * a[4], v * v * v * cur[1] + 3 * v * v * u * a[1] + 3 * v * u * u * a[3] + u * u * u * a[5]]); }
          cur = [a[4], a[5]];
        } else if (c === "Q") {
          a = take(4); n = Math.max(1, Math.ceil((Math.hypot(a[0] - cur[0], a[1] - cur[1]) + Math.hypot(a[2] - a[0], a[3] - a[1])) / .25));
          for (s = 1; s <= n; s++) { var w = s / n, z = 1 - w; out.push([z * z * cur[0] + 2 * z * w * a[0] + w * w * a[2], z * z * cur[1] + 2 * z * w * a[1] + w * w * a[3]]); }
          cur = [a[2], a[3]];
        } else i++;
      }
      return out;
    }
    function inkClear(ds, knots, segs) {
      var S = [];
      ds.forEach(function (d) { [].push.apply(S, samples(d)); });
      if (TURN) S = S.filter(function (p) { return p[1] < TURN.A || p[1] > TURN.B; });
      var R = CLR + 8, bb = segs.map(function (sg) { return [Math.min(sg[0], sg[2]) - R, Math.min(sg[1], sg[3]) - R, Math.max(sg[0], sg[2]) + R, Math.max(sg[1], sg[3]) + R]; });
      function nearQ(l, t, r, b) { return bb.some(function (q) { return r > q[0] && l < q[2] && b > q[1] && t < q[3]; }); }
      var cr = document.createRange(), C2 = CLR * CLR, K = CLR + 2.8;
      for (var i = 0; i < runs.length; i++) {
        var tn = runs[i][0];
        if (!runs[i][1].some(function (q) { return nearQ(q.left - fb.left, q.top - fb.top, q.right - fb.left, q.bottom - fb.top); })) continue;
        var cs = getComputedStyle(tn.parentElement); if (cs.visibility !== "visible") continue;
        for (var j = 0; j < tn.data.length; j++) {
          var ch = tn.data.charAt(j); if (!ch.trim()) continue;
          cr.setStart(tn, j); cr.setEnd(tn, j + 1); var g = cr.getBoundingClientRect();
          if (!g.width || !nearQ(g.left - fb.left, g.top - fb.top, g.right - fb.left, g.bottom - fb.top)) continue;
          var gi = glyphInk(ch, cs); if (!gi.p.length) continue;
          var ox = g.left - fb.left, oy = g.top + (g.height - (gi.fa + gi.fd)) / 2 + gi.fa - fb.top;
          var x0 = ox + gi.b[0], y0 = oy + gi.b[1], x1 = ox + gi.b[2], y1 = oy + gi.b[3];
          var cand = S.filter(function (p) { return p[0] > x0 - CLR && p[0] < x1 + CLR && p[1] > y0 - CLR && p[1] < y1 + CLR; });
          var kn = knots.filter(function (k) { return k[0] > x0 - K && k[0] < x1 + K && k[1] > y0 - K && k[1] < y1 + K; });
          if (!cand.length && !kn.length) continue;
          for (var m = 0; m < gi.p.length; m++) {
            var X = ox + gi.p[m][0], Y = oy + gi.p[m][1];
            for (var q = 0; q < cand.length; q++) { var dx = cand[q][0] - X, dy = cand[q][1] - Y; if (dx * dx + dy * dy < C2) return false; }
            for (q = 0; q < kn.length; q++) if (Math.hypot(kn[q][0] - X, kn[q][1] - Y) - 2.8 < CLR) return false;
          }
        }
      }
      return true;
    }
    function bracket(rects, x, dir) {
      var top = Math.min.apply(null, rects.map(function (q) { return q.top; })) - fb.top, bot = Math.max.apply(null, rects.map(function (q) { return q.bottom; })) - fb.top;
      var y0 = top + 5, y1 = bot - 5;
      if (y1 - y0 < 10) { var m = (y0 + y1) / 2; y0 = m - 5; y1 = m + 5; }
      /* two brackets on one spine that would meet: the later one starts 4px below the earlier's end. (A guard only since
         the review fix: a line two anchors share is now under neither bracket, see ONE LINE, ONE CLAIM below.) */
      placed.forEach(function (p) {
        if (Math.abs(p.x - x) > .5 || y0 >= p.y1 + 4 || y1 <= p.y0 - 4) return;
        if (p.y0 <= y0) { y0 = p.y1 + 4; y1 = Math.max(y1, y0 + 10); } else y1 = Math.min(y1, p.y0 - 4);
      });
      var b = { x: x, dir: dir, y0: y0, y1: y1, k: (y0 + y1) / 2 }; placed.push(b); return b;
    }
    function seg(P, a, b) {          /* a straight run, a hand's slight bow, its ends exact (the string stays one line) */
      var len = Math.hypot(b[0] - a[0], b[1] - a[1]); if (len < 2) return "L" + n1(b[0]) + " " + n1(b[1]);
      var nx = -(b[1] - a[1]) / len, ny = (b[0] - a[0]) / len, bw = Math.min(3.2, len * .008 + .3) * .3, k1 = P.j(bw), k2 = P.j(bw);
      return "C" + n1(a[0] + (b[0] - a[0]) * .33 + nx * k1) + " " + n1(a[1] + (b[1] - a[1]) * .33 + ny * k1) + " " + n1(a[0] + (b[0] - a[0]) * .66 + nx * k2) + " " +
        n1(a[1] + (b[1] - a[1]) * .66 + ny * k2) + " " + n1(b[0]) + " " + n1(b[1]);
    }
    function route(P, pts) {         /* the string: orthogonal runs, corners rounded r 6 (less where a run is short) */
      pts = pts.filter(function (p, i) { return !i || Math.hypot(p[0] - pts[i - 1][0], p[1] - pts[i - 1][1]) > .5; });
      var d = "M" + n1(pts[0][0]) + " " + n1(pts[0][1]), cur = pts[0], last = pts.length - 1;
      for (var i = 1; i < last; i++) {
        var p = pts[i], q = pts[i + 1], li = Math.hypot(p[0] - cur[0], p[1] - cur[1]), lo = Math.hypot(q[0] - p[0], q[1] - p[1]);
        var r = Math.min(6, li / (i === 1 ? 1 : 2), lo / (i + 1 === last ? 1 : 2));
        var a = [p[0] - (p[0] - cur[0]) / li * r, p[1] - (p[1] - cur[1]) / li * r], b = [p[0] + (q[0] - p[0]) / lo * r, p[1] + (q[1] - p[1]) / lo * r];
        d += seg(P, cur, a) + "Q" + n1(p[0]) + " " + n1(p[1]) + " " + n1(b[0]) + " " + n1(b[1]); cur = b;
      }
      return d + seg(P, cur, pts[last]);
    }
    /* ONE LINE, ONE CLAIM (R2 review fix, S1). A bracket covers only the lines that hold text of its own anchor
       alone. Where two anchors' text shares a line (EVENTER 03 '…decisions. Growth…' at 54 widths of 164: the
       first claim's end and the second's start), that line belongs to NEITHER bracket; an anchor left with no
       line of its own at a width has no thread there (a named absence, as the margin's). Two rects are on one
       line when their centres lie within a quarter of the smaller height; another anchor's text counts on the
       side a bracket faces (a right-column target's bracket faces its own column). The rule holds for every
       pair of anchors of the file, either thread, either end. */
    var spec = list.map(function (t) {
      var ra = t.a(), rb = t.b(); if (!ra || !ra.length || !rb || !rb.length) return null;
      var tl = Math.min.apply(null, rb.map(function (q) { return q.left; })) - fb.left, rc = wide && tl > cL + .4 * (cR - cL);
      return { rc: rc, list: rb.list, ends: [{ r: ra, x: BX, d: -s }, { r: rb, x: rc ? tl - 9 : BX, d: rc ? 1 : -s }] };   /* (a right-column target: wide only) */
    });
    var anc = []; spec.forEach(function (o) { if (o) anc.push(o.ends[0], o.ends[1]); });
    function oneLine(p, q) { return Math.abs((p.top + p.bottom) / 2 - (q.top + q.bottom) / 2) < Math.min(p.height, q.height) / 4; }
    anc.forEach(function (e) {
      e.own = e.r.filter(function (p) {
        return !anc.some(function (o) { return o !== e && o.r.some(function (q) { return (e.d > 0 ? q.right - fb.left > e.x : q.left - fb.left < e.x) && oneLine(p, q); }); });
      });
    });
    list.forEach(function (t, k) {
      var o = spec[k]; if (!o || !o.ends[0].own.length || !o.ends[1].own.length) return;
      var ra = o.ends[0].own, rb = o.ends[1].own; rb.list = o.list;
      var A = bracket(ra, BX, -s), B, rc = o.rc;
      if (rc) B = bracket(rb, o.ends[1].x, 1);
      else B = bracket(rb, BX, -s);
      var lx = LANE[t.lane], ylo = Math.min(A.k, B.k), yhi = Math.max(A.k, B.k);
      films.forEach(function (f) {    /* guard: a lane that would run within 4px of the film edge's print moves outside it */
        var x0 = f.left - fb.left, x1 = f.right - fb.left;
        if (lx > x0 - 4 && lx < x1 + 4 && yhi > f.top - fb.top && ylo < f.bottom - fb.top) lx = x1 + 6;
      });
      var pts = [[A.x, A.k], [lx, A.k]];
      if (!rc) pts.push([lx, B.k], [B.x, B.k]);
      else {                          /* leave the lane in the clear band between the target's header row and its list */
        var L = rb.list, zr = L && L.previousElementSibling; while (zr && !zr.classList.contains("zr")) zr = zr.previousElementSibling;
        if (!zr && L) zr = L.closest(".z") && L.closest(".z").querySelector(".zr");
        var yb = zr ? ((zr.getBoundingClientRect().bottom + L.getBoundingClientRect().top) / 2 - fb.top) : B.k;
        pts.push([lx, yb], [B.x - 3, yb], [B.x - 3, B.k], [B.x, B.k]);
      }
      var segs = [];
      [A, B].forEach(function (b) { var fx = b.x + b.dir * FL; segs.push([fx, b.y0, b.x, b.y0], [b.x, b.y0, b.x, b.y1], [fx, b.y1, b.x, b.y1]); });
      pts.forEach(function (p, i) { if (i) segs.push([pts[i - 1][0], pts[i - 1][1], p[0], p[1]]); });
      var kns = [[A.x, A.k], [B.x, B.k]], un = function () { placed.splice(placed.indexOf(A), 1); placed.splice(placed.indexOf(B), 1); };
      if (!clearOf(segs, kns)) { un(); return; }
      /* the drawing, built first (the pen in the same order as it draws: bracket A, bracket B, the string), then held
         to the glyphs' ink as drawn; a thread that would come nearer than CLR to a letter is not drawn at this width */
      var P = new FG.Pen(DOC + "-thread-" + k);
      var dBr = [A, B].map(function (b) { var fx = n1(b.x + b.dir * FL); return "M" + fx + " " + n1(b.y0) + "L" + n1(b.x) + " " + n1(b.y0) + seg(P, [b.x, b.y0], [b.x, b.y1]) + "L" + fx + " " + n1(b.y1); });
      var dT = route(P, pts);
      if (!inkClear([dBr[0], dBr[1], dT], kns, segs)) { un(); return; }
      var g = FG.el(thrSvg, "g", { "data-k": k });
      [A, B].forEach(function (b, i) { FG.path(g, dBr[i], UVC, 2, { "stroke-linecap": "butt", "data-p": i ? "b" : "a" }); });
      FG.path(g, dT, UVC, 1.8, { "stroke-dasharray": "7 4", "stroke-linecap": "butt", "data-p": "t" });
      [A, B].forEach(function (b, i) { FG.el(g, "circle", { cx: n1(b.x), cy: n1(b.k), r: 2.8, fill: UVC, "data-p": i ? "kb" : "ka" }); });
    });
  }
  function developed() {
    /* each developed zone's frame: a dashed violet hand line, double-stroked */
    [].forEach.call(X.querySelectorAll(".devz"), function (z, i) {
      var s = hostUV(z), P = new FG.Pen("xtix-devz-" + i), w = z.clientWidth, h = z.clientHeight;
      if (w < 10 || h < 10) return;
      FG.path(s, P.rect(1, 1, w - 2, h - 2, { overshoot: 3 }), UVC, 1.4, { "stroke-dasharray": "6 4", "stroke-linecap": "butt" });
    });
    /* the ring around 'enterprise' */
    var cw = DOC === "xtix" && X.querySelector(".cite-word");      /* the ring is XTIX's (note 3 names a word); other files light theirs */
    if (cw) {
      /* fitted (R2 D5): today's ellipse, brought in only as far as it must to keep 2px off 'for' and the
         lines above and below (FG.ringFit; same seed, stroke and glow) */
      var d = cw.closest(".dash"), s = hostUV(d), wr = document.createRange(); wr.selectNodeContents(cw);
      s.classList.add("uv-ring");
      var fit = FG.ringFit(d, wr, { seed: "xtix-enterprise-ring", rx0: 2.5, ry0: 8, wobble: .025, steps: 20, stroke: 1.4, svg: s });
      FG.path(s, fit.d, UVC, 1.4);
    }
  }
  cites();
  /* phone: the developed zones open in the flow; keep the lamp key where the reader's finger is */
  if (lb) lb.addEventListener("click", function () {
    var before = lb.getBoundingClientRect().top;
    raf(function () {
      if (HOST.w < 1100) { var after = lb.getBoundingClientRect().top; if (Math.abs(after - before) > .5) HOST.scrollBy(0, after - before); }
      draw();
    });
  }, true);

  /* every other document: a brush tick over each ✓ (the character stays, its glyph transparent) */
  function genericTicks() {
    [].forEach.call(X.querySelectorAll(".lg .c"), function (c, i) {
      var row = c.parentElement, s = FG.svg(row, "uv-layer"), P = new FG.Pen(DOC + "-tick-" + i), b = FG.box(c, row), x = b.x + 1, y = b.y + b.h / 2 - 1, pts = [], ws = [];
      s.style.zIndex = "-1";
      var V = [[x, y], [x + 5.2, y + 5.6], [x + 18, y - 8.4]];
      for (var t = 0; t <= 1.0001; t += .2) { pts.push([V[0][0] + (V[1][0] - V[0][0]) * t, V[0][1] + (V[1][1] - V[0][1]) * t]); ws.push(.7 + 2.7 * t); }
      for (t = .1; t <= 1.0001; t += .1) { pts.push([V[1][0] + (V[2][0] - V[1][0]) * t + P.j(.15), V[1][1] + (V[2][1] - V[1][1]) * t]); ws.push(3.4 - 2.8 * Math.pow(t, .8)); }
      drawn.push(s);
      FG.path(s, P.brush(pts, ws), null, 0, { fill: getComputedStyle(row).getPropertyValue("--c-text").trim() || TXT });   /* the ✓ is text: text tier, both states */
    });
  }

  /* each document's own colour tiers, read from its variables at every draw: the line tier for thin
     marks (falls back to the fill tier), the text tier for outlines that are read as type */
  function tokens() {
    var cs = getComputedStyle(X);
    FILL = (cs.getPropertyValue("--c-line") || cs.getPropertyValue("--c-fill")).trim() || "#2FB380";
    TXT = cs.getPropertyValue("--c-text").trim() || "#1C6E4E";
  }

  function draw() {
    tokens(); FG.defs();
    drawn.forEach(function (s) { s.remove(); }); drawn = [];
    var fd = X.querySelector(".folder");
    if (fd && !fd.querySelector(".fg-dark")) { var dk = document.createElement("i"); dk.className = "fg-dark"; dk.setAttribute("aria-hidden", "true"); fd.insertBefore(dk, fd.firstChild); }
    wordmark(X); rule(); lamp();
    SHEET = "";
    if (DOC === "xtix") holes();
    pageTurn();                                   /* S2: right after the holes (its cut joins their list) */
    if (DOC === "xtix") { promise(); approach(); ticks(); chart(); engine(); vellum(); }
    else genericTicks();
    ticket(); developed();
    if (PL) PL.draw({ X: X, DOC: DOC, host: host, hostUV: hostUV, FG: FG, STILL: STILL, baselineOf: baselineOf, ink: INK, line: FILL, text: TXT, uv: UV, scroller: scroller() });   /* the document's own plates */
    if (TURN && Math.abs(FG.box(TURN.E, X.querySelector(".folder")).y - TURN.top) > .25) pageTurn();   /* a plate moved E: cut again */
    threads();                                    /* S1: after the plates and the page-turn */
    if (M.accent && SWT[M.accent]) { SWT[M.accent].g.style.opacity = "1"; paint(M.cur || M.accent, M.cur ? M.f : 1); }
    progress();
  }
  /* ==========================================================================================
     THE THREE VERBS. open(): stillness read now, the once-per-opening gestures re-armed, the observers and the
     scroller's listener made, drawn, fitted, the shell told (the cue is decided only on a fitted section). close(): every
     observer disconnected, the listener gone, rAF and timers cancelled, a turn in flight landed; lamp and turn stay, as
     in R10. resize(): the same drawing at the new width, 150 ms after the last change. */
  function scroller() { var b = FG0.bound[DOC]; return b != null && innerWidth < b; }
  function fit() {
    draw();
    X.setAttribute("data-fitted", "");
    if (root.__mwSwipeCues) root.__mwSwipeCues();
  }
  function open() {
    if (shown) close();
    shown = true;
    STILL = dead || FG0.stillNow();
    X.classList.toggle("still", STILL);
    M = { built: STILL ? 10 : 0, cur: 0, pmax: 0, running: false, visible: true, accent: 0 };
    BARS = {}; SWT = {}; thenDone = STILL; engDone = STILL;
    if (PL && PL.open) PL.open();
    if (panel && !STILL) {
      HOST.scroller().addEventListener("scroll", progress, { passive: true });
      /* the queue waits while less than half the plot is on screen: a bar is never laid unseen */
      if ("IntersectionObserver" in window) { plotIO = new IntersectionObserver(guard(function (es) { M.visible = es[0].intersectionRatio >= .5; if (M.visible) next(); }), { root: HOST.root, threshold: [0, .5, 1] }); plotIO.observe(plot); }
    }
    guard(fit)();
  }
  function close() {
    shown = false;
    X.removeAttribute("data-fitted");
    clearTimeout(rz);
    HOST.scroller().removeEventListener("scroll", progress, { passive: true });
    [plotIO, thenIO, engIO].forEach(function (o) { if (o) o.disconnect(); });
    plotIO = thenIO = engIO = null;
    if (SF.land) SF.land(true);
    timers.splice(0).forEach(function (t) { clearTimeout(t); });
    frames.splice(0).forEach(function (r) { cancelAnimationFrame(r); });
    if (M.cur && BARS[M.cur] && BARS[M.cur].col) BARS[M.cur].col.classList.remove("drawing");
    if (M.accent) accent(0);
    M.running = false;
    if (PL && PL.close) PL.close();
  }
  function resize() { clearTimeout(rz); rz = setTimeout(guard(fit), 150); }
  /* a throw anywhere after the mount: every gesture stopped, the file drawn again as for reduced motion (every mark
     complete); if that throws too, the drawing goes and the stylesheet prints the file */
  function printed(e) {
    tell(DOC, e);
    function bare(e2) { drawn.forEach(function (s) { s.remove(); }); drawn = []; plain(X, e2); }
    if (dead) return bare(e);
    var was = shown;
    dead = true;
    try { close(); } catch (x) { tell(DOC, x); }
    shown = was; STILL = true;
    X.classList.add("still");
    M = { built: 10, cur: 0, pmax: 0, running: false, visible: true, accent: 0 };
    BARS = {}; SWT = {}; thenDone = true; engDone = true;
    try { if (PL && PL.open) PL.open(); draw(); } catch (x2) { bare(x2); }
  }
  return { open: open, close: close, resize: resize, printed: printed };
  }

  /* one instance per section; a second call returns it (the opening calls it again, right before the drawing) */
  FG.mount = function (section) {
    var d = section.getAttribute("data-file");
    return INST[d] || (INST[d] = build(section));
  };
  /* every ported section, once, at load */
  FG.mountAll = function () {
    [].forEach.call(document.querySelectorAll("[data-file]"), function (s) { try { FG.mount(s); } catch (e) { fail(s, e); } });
  };
  root.__fgFaces = facesOf;
  /* the shell's hooks. Open: the faces, then the instance, then the drawing in one task. */
  root.__fgOpen = function (sec) {
    var d = sec.getAttribute("data-file"), n = ++OPENING;
    CUR = sec;
    return facesOf(sec).then(function () {
      if (n !== OPENING) return;
      if (FAILED[d]) { try { wordmark(sec); } catch (e) { tell(d, e); } return; }
      try { FG.mount(sec).open(); } catch (e) { fail(sec, e); }
    });
  };
  root.__fgClose = function (sec) {
    var m = INST[sec.getAttribute("data-file")];
    OPENING++;
    if (CUR === sec) CUR = null;
    if (m) { try { m.close(); } catch (e) { tell(sec.getAttribute("data-file"), e); } }
  };
  root.__fgResize = function () {
    var m = CUR && INST[CUR.getAttribute("data-file")];
    if (m) m.resize();
  };
})(window);
