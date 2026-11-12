/* MEDCOIN -- its own plates (built from docs/fieldguide-six/medcoin.md). window.FGDOC.medcoin(X, FG, RT) makes one instance; its
   draw(ctx) is called by fg.js after the shared drawing on every draw. ctx = {X, DOC, host, hostUV, FG, STILL, baselineOf,
   ink, line, text, uv, scroller}. The tags below are written once, when the instance is made: existing nodes moved into
   spans, never a character written. */
window.FGDOC = window.FGDOC || {};
window.FGDOC.medcoin = function (X, FG0, RT) {
  "use strict";
  var HOST = RT.H;

  /* ---------------------------------------------------------------- TAGS (once; idempotent) */
  function wrap(node, at, len, cls) {
    if (!node || node.nodeType !== 3 || at < 0 || at + len > node.data.length) return null;
    var r = document.createRange(); r.setStart(node, at); r.setEnd(node, at + len);
    var s = document.createElement("span"); s.className = cls; r.surroundContents(s); return s;
  }
  function textWith(el, word, last) {          /* the text node holding a whole word, and where */
    var w = document.createTreeWalker(el, NodeFilter.SHOW_TEXT), n, hit = null;
    while ((n = w.nextNode())) {
      var re = new RegExp("(^|[^A-Za-z])(" + word + ")(?![A-Za-z])", "g"), m;
      while ((m = re.exec(n.data))) { hit = { node: n, at: m.index + m[1].length }; if (!last) return hit; }
    }
    return hit;
  }
  function cite(el, word, last) {
    if (!el || el.querySelector(".cite-word[data-w='" + word + "']")) return;
    var h = textWith(el, word, last); if (!h) return;
    var s = wrap(h.node, h.at, word.length, "cite-word cite"); if (s) s.setAttribute("data-w", word);
  }
  /* 01 'compliant' (note 1: 'the compliant half') and 02 'operations' (note 3: 'Operations runs through the challenge') */
  cite(X.querySelector('.z[data-zone="01"] > .para b'), "compliant");
  cite(X.querySelector('.z[data-zone="02"] > .para'), "operations", true);
  /* TYPESETTING (tag-only: existing nodes moved into a span, never a character written) */
  function keep(el, word, cls) {                /* a whole string kept on one line */
    if (!el || el.querySelector("." + (cls || "nw"))) return;
    var h = textWith(el, word, true); if (h) wrap(h.node, h.at, word.length, cls || "nw");
  }
  /* 01: 'crypto-ATM' never splits at its hyphen */
  keep(X.querySelector('.z[data-zone="01"] > .para b'), "crypto-ATM");
  /* 02: '— model,' never opens a line. The <b> and the span.nw after it move into one nowrap wrapper,
     so their common ancestor no longer offers a break at the boundary; the <b> still wraps inside. */
  (function () {
    var p = X.querySelector('.z[data-zone="02"] > .para'); if (!p || p.querySelector(".mc-nwb")) return;
    var b = p.querySelector(":scope > b"), n = b && b.nextSibling;
    if (!n || n.nodeType !== 1 || !n.classList.contains("nw")) return;
    var r = document.createRange(), s = document.createElement("span"); s.className = "mc-nwb";
    r.setStartBefore(b); r.setEndAfter(n); r.surroundContents(s);
  })();
  /* (the ticket's control numbers are held whole by the skeleton since R2 D4 — 'CTRL № M-26-0104' in one
     span.nw, both faces, tag-only — so the runtime wrap that stood here is retired: one less to port) */
  /* the back's CARRIES: 'OF €' kept together in its last figure (it may break before it at ≤350px) */
  [].forEach.call(X.querySelectorAll(".sf-back .ms-fig .seg"), function (sg) {
    if (sg.querySelector(".nw") || !/ OF €$/.test(sg.textContent)) return;
    var t = sg.lastChild; if (t && t.nodeType === 3) wrap(t, t.data.lastIndexOf("OF €"), 4, "nw");
  });
  /* the archive stamp: each '·' bound to the words before it — 'DUPLICATED FROM MICROFILM ·',
     'QUALITY DEGRADED ·', 'CONTENT VERIFIED' — so a line breaks after a dot, never before one */
  (function () {
    var sp = X.querySelector(".gen3 > span"); if (!sp || sp.querySelector(".nw")) return;
    var dots = [].slice.call(sp.querySelectorAll(":scope > .dot")); if (!dots.length) return;
    var start = sp.firstChild;
    dots.concat([null]).forEach(function (d) {
      if (!start) return;
      if (start.nodeType === 3) { var lead = /^\s+/.exec(start.data); if (lead) { if (lead[0].length === start.data.length) return; start = start.splitText(lead[0].length); } }
      var r = document.createRange(), s = document.createElement("span"); s.className = "nw";
      r.setStartBefore(start); if (d) r.setEndAfter(d); else r.setEndAfter(sp.lastChild);
      r.surroundContents(s); start = s.nextSibling;
    });
  })();
  /* the receipt: 'of €' kept together; the key REVENUE (note 2: 'only revenue is given a magnitude') */
  var em = X.querySelector(".outs td.v.em");
  if (em && !em.querySelector(".nw")) { var et = em.lastChild; if (et && et.nodeType === 3) wrap(et, et.data.lastIndexOf("of €"), 4, "nw"); }
  [].forEach.call(X.querySelectorAll(".outs td.k"), function (td) { if (td.textContent.trim() === "REVENUE") td.classList.add("cite"); });
  /* 05 'INVESTMENT RAISED' is NOT lit (R2 D1): the origin board is a permanent dark object and never
     changes state (Oran's answer 3 outranks M11's citation list); developed note 1 keeps its words. */
  /* 06: the three sentences as rows of their own words — Every | adjective | decision affects | object. */
  (function matrix() {
    var para = X.querySelector(".hairtop.cols2 .para"); if (!para || para.querySelector(".dep-row")) return;
    var t = para.firstChild;
    if (!t || t.nodeType !== 3 || !/^Every \S+ decision affects \S+\. Every \S+ decision affects \S+\. Every \S+ decision affects \S+\. ?$/.test(t.data)) return;
    var cur = t;
    function take(n) { var rest = cur.splitText(n), piece = cur; cur = rest; return piece; }
    function span(cls, kids) { var s = document.createElement("span"); s.className = cls; kids.forEach(function (k) { s.appendChild(k); }); return s; }
    for (var k = 0; k < 3; k++) {
      if (k) take(1);                                       /* the one space between sentences stays where it is */
      var m = new RegExp("^Every (\\S+) decision affects (\\S+)\\.").exec(cur.data);
      var row = document.createElement("span"); row.className = "dep-row"; para.insertBefore(row, cur);
      var a = take(5), s1 = take(1), adj = take(m[1].length), s2 = take(1), con = take(16), s3 = take(1), obj = take(m[2].length), dot = take(1);
      var cw = span("cite-word cite", [obj]); cw.setAttribute("data-w", m[2]);
      [span("c", [a]), s1, span("v", [adj]), s2, span("c", [con]), span("mc-sp", [s3]), span("v", [cw, dot])].forEach(function (n) { row.appendChild(n); });
    }
  })();

  /* ================================================================ THE DRAWING (every draw) */
  var originDone = false, originIO = null;

  /* M07 · THE RECEIPT: one die-cut (zigzag tear top and bottom, straight sides) shared by the hard ink
     plate (8/8), the paper and its outline. Three layers, back to front, all behind the rows. */
  function receipt(c) {
    var FG = c.FG, outs = X.querySelector(".outs"); if (!outs) return;
    var W = outs.offsetWidth, H = outs.offsetHeight; if (W < 60 || H < 60) return;
    var P = new FG.Pen("medcoin-receipt"), pitch = HOST.w <= 760 ? 8 : 9, depth = 4.5;
    var k = Math.max(2, Math.round(W / (pitch / 2))); if (k % 2) k++;
    var st = W / k, pts = [], i;
    for (i = 0; i <= k; i++) pts.push([i * st, i % 2 ? depth + P.j(.7) : 0]);
    for (i = k; i >= 0; i--) pts.push([i * st, i % 2 ? H - depth - P.j(.7) : H]);
    var d = "M" + pts.map(function (p) { return p[0].toFixed(1) + " " + p[1].toFixed(1); }).join("L") + "Z";
    var plate = c.host(outs);
    FG.path(plate, d, null, 0, { fill: "#1a1714", transform: "translate(8 8)", class: "mc-plate" });
    var paper = c.hostUV(outs), defs = FG.el(paper, "defs", {}), g = FG.el(defs, "linearGradient", { id: "mc-curl", x1: "0", x2: "1", y1: "0", y2: "0" });
    [["0", .045], [".12", 0], [".88", 0], ["1", .045]].forEach(function (s) { FG.el(g, "stop", { offset: s[0], "stop-color": "#1a1714", "stop-opacity": s[1] }); });
    FG.path(paper, d, null, 0, { fill: "#fffdf8", class: "mc-paper" });
    FG.path(paper, d, null, 0, { fill: "url(#mc-curl)", class: "mc-curl" });
    FG.path(c.host(outs), d, "#1a1714", 1.1, { class: "mc-edge" });
  }

  /* M08 · THE ORIGIN BOARD: the file's own SVG becomes the board; its six <text> labels stay (same
     element, same order) and are laid out by attribute; the marks are drawn in a wordless layer. Wide:
     the file's own coordinates, scaled. Narrow (where the labels would collide): the vertical form. */
  function board(c) {
    var FG = c.FG, mz = X.querySelector(".mzorg"), sv = mz && mz.querySelector("svg:not(.fg-svg)"); if (!sv) return;
    var T = [].slice.call(sv.querySelectorAll("text")); if (T.length !== 6) return;
    sv.classList.add("mc-board");
    T.forEach(function (t, i) { t.classList.add(i < 5 ? "mc-lab" : "mc-rev"); });
    mz.classList.toggle("mc-s", !!c.scroller); mz.scrollLeft = 0;   /* below FG.bound.medcoin: the board scrolls sideways, as R10 */
    var W = c.scroller ? 940 : Math.floor(mz.clientWidth); if (W < 120) return;
    function size(H) { sv.setAttribute("viewBox", "0 0 " + W + " " + H); sv.setAttribute("width", W); sv.setAttribute("height", H); }
    function at(t, x, y, anchor) { t.setAttribute("x", x.toFixed(1)); t.setAttribute("y", y.toFixed(1)); t.setAttribute("text-anchor", anchor); }
    var G, vert = false;
    /* the horizontal form: x' = 56 + (x − 44)·(W − 112)/996 */
    sv.classList.remove("mc-v", "mc-tight");
    (function () {
      var H = 184, y = 88, m = 56, sc = (W - 2 * m) / 996, fx = function (x) { return m + (x - 44) * sc; };
      var xs = [44, 262, 480, 698, 916].map(fx);
      size(H);
      xs.forEach(function (x, i) { at(T[i], x, 124, "middle"); });
      at(T[5], fx(986), 66, "middle");
      var bb = T.map(function (t) { return t.getBBox(); }), ok = bb[0].x >= 18 && bb[4].x + bb[4].width <= W - 18 && bb[5].x + bb[5].width <= W - 18;
      for (var i = 0; i < 4; i++) if (bb[i].x + bb[i].width + 16 > bb[i + 1].x) ok = false;
      G = { H: H, ok: ok, pts: xs.map(function (x) { return [x, y]; }), tip: [fx(1040), y], dir: [1, 0] };
    })();
    if (!G.ok) {
      vert = true; sv.classList.add("mc-v"); W = Math.min(W, 420);      /* the vertical form never grows wider than its column of labels needs */
      var x0 = 36, y0 = 44, p = 64, hero = y0 + 4 * p, tip = hero + Math.round(p * 124 / 218), H = tip + 44;
      size(H);
      for (var i = 0; i < 5; i++) at(T[i], 62, y0 + i * p + 4, "start");
      at(T[5], 62, tip + 4, "start");
      var wmax = function () { return Math.max.apply(null, T.map(function (t) { var b = t.getBBox(); return b.x + b.width; })); };
      if (wmax() > W - 18) sv.classList.add("mc-tight");
      G = { H: H, ok: true, pts: [0, 1, 2, 3, 4].map(function (i) { return [x0, y0 + i * p]; }), tip: [x0, tip], dir: [0, 1] };
    }
    /* the marks, in the board's own coordinates */
    var s = c.hostUV(mz), b = FG.box(sv, mz), ox = b.x, oy = b.y, P = new FG.Pen("medcoin-origin-" + (vert ? "v" : "h"));
    s.classList.add("mc-org");
    function q(pt) { return [ox + pt[0], oy + pt[1]]; }
    FG.path(s, P.rect(ox + 12, oy + 12, W - 24, G.H - 24, { overshoot: 3, rough: .6 }), "#F2F1ED", 1.1, { class: "mc-frame mc-w" });
    var a = q(G.pts[0]), e = q(G.pts[4]), D = G.dir;
    /* the line: FOUNDED's centre to ATMs ACROSS EUROPE's centre, two passes (one per path, so a pen can draw them together) */
    var line = [0, 1].map(function () { return FG.path(s, P.line(a[0], a[1], e[0], e[1], { passes: 1, rough: .45, bow: .35 }), "#F2F1ED", 1.6, { class: "mc-w mc-line" }); });
    /* stations 1–4: hollow rings (the file's hollow dots) */
    G.pts.slice(0, 4).forEach(function (pt, i) {
      var c0 = q(pt), RP = new FG.Pen("medcoin-origin-ring-" + i);
      FG.el(s, "circle", { cx: c0[0], cy: c0[1], r: 6.5, fill: "#191A1F", class: "mc-gr" });
      FG.path(s, RP.ellipse(c0[0], c0[1], 6.5, 6.5, { wobble: .03, steps: 10 }), "#F2F1ED", 1.6, { class: "mc-w mc-line" });
    });
    /* station 5: the file's larger filled dot, in MEDCOIN's own white */
    var HP = new FG.Pen("medcoin-origin-hero"), hp = [];
    for (var n = 0; n < 16; n++) { var an = n / 16 * Math.PI * 2, rr = 9.5 * (1 + HP.j(.04)); hp.push([e[0] + Math.cos(an) * rr, e[1] + Math.sin(an) * rr]); }
    hp.push(hp[0]);
    FG.path(s, HP.curve(hp) + "Z", null, 0, { fill: "#F2F1ED", class: "mc-wf mc-hero" });
    /* the run to REVENUE: the PHANTOM line (path of motion), from the disc's edge to the tip, an open head */
    var r0 = [e[0] + D[0] * 12.5, e[1] + D[1] * 12.5], tp = q(G.tip), r1 = [tp[0] - D[0], tp[1] - D[1]], dash = "14 4 2 4 2 4";
    if (!vert) { var f0 = ox + 56 + (930 - 44) * (W - 112) / 996; if (f0 > r0[0]) r0 = [f0, r0[1]]; }
    else {
      /* the short vertical run (0.57 of a pitch, as in the file): it ends at the head's base, so the open
         head is drawn alone, and its pattern is scaled to the run — one whole long–short–short cycle */
      r1 = [tp[0] - D[0] * 9, tp[1] - D[1] * 9];
      var RL = Math.hypot(r1[0] - r0[0], r1[1] - r0[1]);
      dash = [.40, .16, .09, .16, .09, 1].map(function (f) { return (f * RL).toFixed(2); }).join(" ");
    }
    var rd = "M" + r0[0].toFixed(1) + " " + r0[1].toFixed(1) + "L" + r1[0].toFixed(1) + " " + r1[1].toFixed(1);
    var run = FG.path(s, rd, "#F2F1ED", 1.6, { class: "mc-w mc-line", "stroke-dasharray": dash, "stroke-linecap": "butt" });
    var ang = Math.atan2(D[1], D[0]), A = Math.PI / 6, hd = "";
    [-A, A].forEach(function (o) { hd += P.line(tp[0], tp[1], tp[0] - 9 * Math.cos(ang + o), tp[1] - 9 * Math.sin(ang + o), { passes: 1, rough: .2 }); });
    var head = FG.path(s, hd, "#F2F1ED", 1.6, { class: "mc-w mc-line" });

    /* TIER 1 (default ON; ?gesture=0 prints it complete): once per opening, when the board is 40% in view
       — or, failsafe, once its top has crossed the viewport's middle (a board taller than the window can
       never reach 40%) — the pen draws the line in the file's order (1.6px/ms), then the run is revealed
       through a solid mask (its pattern never moves), then the head. Rings, disc and labels are printed
       throughout. Stillness: complete. One observer at a time: every redraw disconnects the last. */
    if (originIO) { originIO.disconnect(); originIO = null; }
    if (c.STILL || originDone) return;
    var mid = "mc-run-mask", mk = FG.el(FG.el(s, "defs", {}), "mask", { id: mid, maskUnits: "userSpaceOnUse" });
    var mp = FG.el(mk, "path", { d: rd, stroke: "#fff", "stroke-width": 8, fill: "none" }), ML = mp.getTotalLength();
    run.setAttribute("mask", "url(#" + mid + ")"); mp.style.strokeDasharray = ML + " " + ML; mp.style.strokeDashoffset = ML;
    line.concat([head]).forEach(function (pth) { pth.style.visibility = "hidden"; });
    originIO = new IntersectionObserver(RT.guard(function (es) {
      var en = es[es.length - 1], vh = (en.rootBounds && en.rootBounds.height) || HOST.h;
      if (originDone || !en.isIntersecting) return;
      if (en.intersectionRatio < .4 && en.boundingClientRect.top > HOST.top + vh / 2) return;
      originDone = true; originIO.disconnect(); originIO = null;
      var L = line[0].getTotalLength(), dur = Math.max(160, Math.min(900, L / 1.6));
      line.forEach(function (pth) { pth.style.visibility = ""; });
      Promise.all(line.map(function (pth) { return FG.drawOn(pth, dur, 0, "linear"); })).then(function () {
        mp.style.transition = "stroke-dashoffset 160ms linear"; mp.getBoundingClientRect(); mp.style.strokeDashoffset = 0;
        RT.later(function () { head.style.visibility = ""; FG.drawOn(head, 80, 0, "linear"); }, 170);
      });
    }), { root: HOST.root, threshold: [0, .05, .1, .15, .2, .25, .3, .35, .4, .5, .6, .7, .8, .9, 1] });
    originIO.observe(sv);
  }

  /* MC1 (R2) · WHERE THE MATRIX WRAPS, IT BECOMES A LITANY. Below 1100 the three rows run as text; where any
     of them takes more than one line (distinct line-box tops of its spans, 4px tolerance), every row breaks
     at the same two joints of its own syntax — 'Every commercial / decision affects / operations.' — by CSS
     on the plate's existing spans (plates/medcoin.css, .mc-litany). Read at every draw with the class OFF,
     so the decision never depends on itself, and before the ring, which is then fitted at the word's new
     place. The class is the only thing written: no text, no wrap. ≥1100 the grid matrix, unchanged. */
  function litany() {
    var para = X.querySelector(".hairtop.cols2 .para"); if (!para) return;
    para.classList.remove("mc-litany");
    if (HOST.w >= 1100) return;
    var wraps = [].some.call(para.querySelectorAll(".dep-row"), function (row) {
      var tops = [];
      [].forEach.call(row.children, function (e) {
        [].forEach.call(e.getClientRects(), function (r) {
          if (r.width > .5 && r.height > .5 && !tops.some(function (t) { return Math.abs(t - r.top) <= 4; })) tops.push(r.top);
        });
      });
      return tops.length > 1;
    });
    if (wraps) para.classList.add("mc-litany");
  }

  /* M09 · the one hand ring under the lamp: around 06 'operations' (note 3: 'One of them has a row') */
  /* The ring is a narrow, tall ellipse around the whole token 'operations.' (its period inside). It is
     FITTED, not guessed: the token's own ink (rendered once into a canvas at its computed font, scaled to
     its measured width) must lie inside the ellipse's inner edge with 3px to spare at the sides, 2px above and below, and the ellipse's
     outer edge must stay inside the word space before it (the matrix's half-em column gap on desktop),
     inside the column on the right, and clear of the ink of the lines above and below. Of the ellipses
     that fit, the tightest is drawn (the right end grows only as far as it must). */
  function ring(c) {
    var FG = c.FG, para = X.querySelector(".hairtop.cols2 .para"), cw = para && para.querySelector(".cite-word"); if (!cw) return;
    var v = cw.parentElement, rg = document.createRange(); rg.setStartBefore(cw); rg.setEndAfter(v.lastChild);
    var tr = rg.getBoundingClientRect(), pb = para.getBoundingClientRect(), cs = getComputedStyle(cw), fs = parseFloat(cs.fontSize) || 40;
    if (tr.width < 4) return;
    var font = cs.fontStyle + " " + cs.fontWeight + " " + cs.fontSize + " " + cs.fontFamily, tok = rg.toString();
    var mc = document.createElement("canvas").getContext("2d"); mc.font = font;
    var mt = mc.measureText(tok), fa = mt.fontBoundingBoxAscent || fs * .95, fd = mt.fontBoundingBoxDescent || fs * .25;
    var ascInk = mc.measureText("bdfhklt").actualBoundingBoxAscent || fs * .74, descInk = mc.measureText("gjpqy").actualBoundingBoxDescent || fs * .24;
    function baseOf(r) { return r.top + (r.height - (fa + fd)) / 2 + fa; }
    var base = baseOf(tr);
    /* the token's ink, relative to (token left, baseline), one sample per CSS px */
    var K = 2, pad = Math.ceil(fs * .5), cvs = document.createElement("canvas"), CW = Math.ceil(mt.width + 2 * pad), CH = Math.ceil(fs * 2);
    cvs.width = CW * K; cvs.height = CH * K;
    var cx2 = cvs.getContext("2d"); cx2.scale(K, K); cx2.font = font; cx2.textBaseline = "alphabetic"; cx2.fillStyle = "#000";
    var B0 = Math.round(fs * 1.25); cx2.fillText(tok, pad, B0);
    var px = cx2.getImageData(0, 0, cvs.width, cvs.height).data, sx = tr.width / (mt.width || tr.width), ink = [], inkL = 1e9, inkR = -1e9;
    for (var xx = 0; xx < cvs.width; xx++) {                                       /* per column, its top and bottom ink (an ellipse is convex) */
      var t0 = -1, t1 = -1;
      for (var yy = 0; yy < cvs.height; yy++) if (px[(yy * cvs.width + xx) * 4 + 3] >= 50) { if (t0 < 0) t0 = yy; t1 = yy; }
      if (t0 < 0) continue;
      var ix = (xx / K - pad) * sx; ink.push([ix, t0 / K - B0], [ix, (t1 + 1) / K - B0]); inkL = Math.min(inkL, ix); inkR = Math.max(inkR, ix + sx / K);
    }
    if (!ink.length) return;
    var fb = X.querySelector(".folder").getBoundingClientRect();                  /* the sheet: the ring never leaves its paper */
    var topLim = -1e9, botLim = 1e9, leftLim = fb.left + 10, rightLim = fb.right - 10;
    /* the neighbours: every other letter of the para within the ring's reach, by its own baseline and its OWN
       ink (canvas metrics of that letter in its computed font): a line above is cleared by its letters' real
       descent, a line below by their real ascent, 1.5px to spare. (MC1: over the litany's 'operations.' stands
       'decision affects', which has no descender; a generic one cost the ring its 3px/2px fit on phones.) */
    var nc = document.createElement("canvas").getContext("2d"), fm = {}, tw = document.createTreeWalker(para, NodeFilter.SHOW_TEXT), tn;
    while ((tn = tw.nextNode())) {
      if (cw.contains(tn) || tn === v.lastChild) continue;                       /* the token itself */
      var ec = getComputedStyle(tn.parentElement), ef = ec.fontStyle + " " + ec.fontWeight + " " + ec.fontSize + " " + ec.fontFamily;
      if (!fm[ef]) { nc.font = ef; var m0 = nc.measureText("Hxg"); fm[ef] = { a: m0.fontBoundingBoxAscent || fa, d: m0.fontBoundingBoxDescent || fd, g: {} }; }
      var F = fm[ef];
      for (var ci = 0; ci < tn.data.length; ci++) {
        var ch = tn.data.charAt(ci); if (!ch.trim()) continue;
        var cr = document.createRange(); cr.setStart(tn, ci); cr.setEnd(tn, ci + 1);
        var q = cr.getClientRects()[0]; if (!q || q.width < .01 || q.right <= tr.left - 2 || q.left >= tr.right + 40) continue;
        if (!F.g[ch]) { nc.font = ef; var mg = nc.measureText(ch); F.g[ch] = [mg.actualBoundingBoxAscent, Math.max(0, mg.actualBoundingBoxDescent)]; }
        var bl = q.top + (q.height - (F.a + F.d)) / 2 + F.a;
        if (bl < base - 4) topLim = Math.max(topLim, bl + F.g[ch][1] + 1.5);      /* a line above: clear its descenders */
        else if (bl > base + 4) botLim = Math.min(botLim, bl - F.g[ch][0] - 1.5); /* a line below: clear its ascenders */
      }
    }
    var zr = para.parentElement && para.parentElement.querySelector(".zr");
    if (zr && zr.getBoundingClientRect().bottom < tr.top) topLim = Math.max(topLim, zr.getBoundingClientRect().bottom + 3);
    var cs2 = v.parentElement.querySelectorAll(":scope > .c"), prev = cs2[cs2.length - 1];   /* 'decision affects' — same line only */
    if (prev) [].forEach.call(prev.getClientRects(), function (r) { if (Math.abs(baseOf(r) - base) < 4) leftLim = Math.max(leftLim, r.right + 1.5); });
    var WOB = .008, HALF = .7, CLRX = 3, CLRY = 2;              /* clearance: 3px at the sides, 2px above and below, */
    var LEVELS = [[3, 2], [2.2, 1.5], [1.6, 1.2]];                                /* relaxed only where one word space is all there is */
    var L0 = tr.left + inkL, R0 = tr.left + inkR;                                 /* the token's ink, left and right, in the viewport */
    var cy0 = base - (ascInk - descInk) / 2, best = null;
    function fit(eL, eR) {                                                        /* the tightest ry for these ends, or null */
      var cxv = (eL + eR) / 2, rx = ((eR - eL) / 2 - HALF) / (1 + WOB), rxI = rx * (1 - WOB) - CLRX, out = null;
      if (rxI <= 0) return null;
      for (var dyc = 0; dyc <= 14 && !out; dyc++) for (var sg = 1; sg >= -1 && !out; sg -= 2) {
        if (!dyc && sg < 0) continue;
        var cyv = cy0 + sg * dyc, need = 0, ok = true;
        for (var i = 0; i < ink.length; i++) {
          var dx = (tr.left + ink[i][0] - cxv) / rxI; if (Math.abs(dx) >= .995) { ok = false; break; }
          need = Math.max(need, Math.abs(base + ink[i][1] - cyv) / Math.sqrt(1 - dx * dx));
        }
        if (!ok) return null;
        var ry = (need + CLRY) / (1 - WOB), ryO = ry * (1 + WOB) + HALF;
        if (cyv - ryO >= topLim && cyv + ryO <= botLim) out = { cx: cxv, cy: cyv, rx: rx, ry: ry, cost: (eR - eL) + 2 * dyc };
      }
      return out;
    }
    for (var lv = 0; lv < LEVELS.length && !best; lv++) {
      CLRX = LEVELS[lv][0]; CLRY = LEVELS[lv][1];
      for (var lo = 3; lo <= 22; lo++) {                                          /* left end: 3–22px out, never past the neighbour */
        var eL = L0 - lo; if (eL < leftLim) break;
        for (var ro = 3; ro <= 70; ro += 2) {
          var eR = R0 + ro; if (eR > rightLim) break;
          var f = fit(eL, eR); if (f && (!best || f.cost < best.cost)) best = f;
          if (f) break;                                                          /* a wider right end only costs more */
        }
      }
      if (best) best.level = lv;
    }
    if (!best) {                                                                  /* nothing fits: the ring keeps the neighbours clear */
      var eL2 = Math.max(leftLim, L0 - 6), eR2 = Math.min(rightLim, R0 + 6), t2 = Math.max(topLim, tr.top - 8), b2 = Math.min(botLim, tr.bottom + 8);
      best = { cx: (eL2 + eR2) / 2, cy: (t2 + b2) / 2, rx: ((eR2 - eL2) / 2 - HALF) / (1 + WOB), ry: Math.max(fs * .4, (b2 - t2) / 2 - HALF) };
    }
    X.setAttribute("data-mc-ring", best.cost ? "fit-" + best.level : "fallback");               /* lab readout: was the ring fitted? */
    var s = c.hostUV(para), RP = new FG.Pen("medcoin-operations-ring");
    s.classList.add("uv-ring");
    FG.path(s, RP.ellipse(best.cx - pb.left, best.cy - pb.top, best.rx, best.ry, { wobble: WOB, steps: 18 }), c.uv, 1.4);
  }

  /* THE ARCHIVE STAMP's two frames (FINAL's recipe, plates/final.js): a hand rounded rectangle, two
     passes through jittered points, the pen overrunning its start; in currentColor, so the frames follow
     the stamp's own tier in both lamp states (ink on paper; MEDCOIN's light tier under the lamp) */
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
      pts.push([x + r + P.j(jit), y + P.j(jit)], [x + r + 14 + P.j(jit), y + P.j(jit)]);
      d += P.curve(pts);
    }
    return d;
  }
  function archive(c) {
    var g = X.querySelector(".gen3"); if (!g) return;
    var w = g.clientWidth, h = g.clientHeight; if (w < 40 || h < 20) return;
    var s = c.hostUV(g), P = new c.FG.Pen("medcoin-archive-stamp");
    c.FG.path(s, rrect(P, -1.1, -1.1, w + 2.2, h + 2.2, 10, .6), "currentColor", 2.2);
    c.FG.path(s, rrect(P, 5.3, 5.3, w - 10.6, h - 10.6, 4.5, .6), "currentColor", 1);
  }

  return {
    draw: function (ctx) {
      ctx.FG.defs();                     /* the shared stamp, felt and graphite filters (one hidden svg in <body>, once) */
      litany(); receipt(ctx); board(ctx); ring(ctx); archive(ctx);
    },
    open: function () { originDone = false; },
    close: function () { if (originIO) { originIO.disconnect(); originIO = null; } }
  };
};
