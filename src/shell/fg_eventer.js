/* EVENTER -- its own plates (built from docs/fieldguide-six/eventer.md). window.FGDOC.eventer(X, FG, RT) makes one instance; its
   draw(ctx) is called by fg.js after the shared drawing on every draw. ctx = {X, DOC, host, hostUV, FG, STILL, baselineOf,
   ink, line, text, uv, scroller}. */
window.FGDOC = window.FGDOC || {};
window.FGDOC.eventer = function (X0, FG0, RT) {
  "use strict";
  var HOST = RT.H;
  var ICE = "#5E8FBF", ICET = "#406182", INK = "#1a1714", UVC = "#9B7BFF", CARD = "#fffdf8";
  var GS = { done: false, io: null };                       /* the 07 gesture: once per open, never replayed */
  function bez(p1x, p1y, p2x, p2y) {
    function c(t, a, b) { return 3 * a * t * (1 - t) * (1 - t) + 3 * b * t * t * (1 - t) + t * t * t; }
    return function (x) { var t = x; for (var i = 0; i < 8; i++) { var e = c(t, p1x, p2x) - x, d = (c(t + 1e-4, p1x, p2x) - c(t, p1x, p2x)) / 1e-4; if (!d) break; t = Math.max(0, Math.min(1, t - e / d)); } return c(t, p1y, p2y); };
  }
  var easeIn = bez(.3, .6, .3, 1), easeRet = bez(.45, .05, .25, 1);
  function n1(v) { return Math.round(v * 10) / 10; }

  /* ------------------------------------------------------------ no line opens on a dash
     The file keeps '— across' and '— not' together (its own nowrap tags), but the space before each is
     still a break. Where a measure puts the dash at a line's start, the claim's measure narrows (a
     style, never a word) until the dash rides with the word before it. Re-measured on every draw. */
  function noDashStart(ctx) {
    [].forEach.call(ctx.X.querySelectorAll(".folder .para"), function (p) { p.style.maxWidth = ""; });
    [].forEach.call(ctx.X.querySelectorAll(".folder .para .nw"), function (nw) {
      var t = nw.firstChild; if (!t || t.nodeType !== 3 || !/^[—–]/.test(t.data)) return;
      var p = nw.closest(".para"), r = document.createRange(), r2 = document.createRange();
      function opens() {
        r.setStart(t, 0); r.setEnd(t, 1); var a = r.getClientRects()[0];
        r2.setStart(p, 0); r2.setEndBefore(nw); var rs = r2.getClientRects(), b = rs[rs.length - 1];
        return !!(a && b && a.top > b.top + a.height * .5);
      }
      var w = p.getBoundingClientRect().width, n = 0;
      while (opens() && n++ < 60) { w -= 6; p.style.maxWidth = w + "px"; }
    });
  }

  /* ------------------------------------------------------------ E9 · the ✓ is text: its brush tick takes the text tier */
  function ticks(ctx) {
    [].forEach.call(ctx.X.querySelectorAll(".list .lg > svg.fg-svg:not(.uv-layer) path"), function (p) { p.setAttribute("fill", ctx.text); });
  }

  /* ------------------------------------------------------------ E5 · the twin line under 03's <b>, on every line fragment */
  function twin03(ctx) {
    var b = ctx.X.querySelector('.z[data-zone="03"] > .para b'); if (!b) return;
    var para = b.closest(".para"), s = ctx.host(para), P = new ctx.FG.Pen("eventer-03-twin"), hb = para.getBoundingClientRect(), desc = ctx.baselineOf(b).desc;
    var r = document.createRange(); r.selectNodeContents(b);
    var seen = {};
    [].forEach.call(r.getClientRects(), function (rc) {
      var key = Math.round(rc.top) + ":" + Math.round(rc.left);
      if (rc.width < 2 || seen[key]) return; seen[key] = 1;
      var x1 = rc.left - hb.left - 3, x2 = rc.right - hb.left + 3, y = rc.bottom - hb.top - desc + 6;
      ctx.FG.path(s, P.curve([[x1, y + P.j(.4)], [(x1 + x2) / 2, y + 1.3], [x2, y + P.j(.4)]]), ICE, 2.2);
    });
  }

  /* ------------------------------------------------------------ E6 · each count's 28px rule (the guide's insight-card rule) */
  function counts(ctx) {
    [].forEach.call(ctx.X.querySelectorAll(".etr .et"), function (et, i) {
      var s = ctx.host(et), P = new ctx.FG.Pen("eventer-count-rule-" + i);
      ctx.FG.path(s, P.line(0, 1.5, 28, 1, { passes: 1, rough: .5 }), ICE, 2);
    });
  }

  /* ------------------------------------------------------------ E9/E12 · the ring on the word zone 3 quotes ('pricing', the decision in contribution 4)
     The guide's ring (XTIX's): a narrow, tall hand ellipse, its ends inside the word spaces, the room
     added vertically, so it never touches 'percentage-plus-fixed' or 'model:'. */
  function ring(ctx) {
    if (window.CSS && CSS.highlights) CSS.highlights.delete("ev-cite");
    var row = [].filter.call(ctx.X.querySelectorAll(".list .lg"), function (l) { return /pricing model/.test(l.textContent); })[0]; if (!row) return;
    var tn = [].filter.call(row.childNodes, function (n) { return n.nodeType === 3 && /pricing/.test(n.data); })[0]; if (!tn) return;
    var word = "pricing", i = tn.data.indexOf(word);
    var r = document.createRange(); r.setStart(tn, i); r.setEnd(tn, i + word.length);
    if (window.CSS && CSS.highlights && window.Highlight) CSS.highlights.set("ev-cite", new Highlight(r));
    var s = ctx.hostUV(row);
    s.classList.add("uv-ring");
    /* fitted (R2 D5): today's ellipse (rx w/2+1.8, ry h/2+8), brought in only as far as it must to keep
       2px off the wrapped next line and its neighbours (FG.ringFit; same seed, stroke and glow) */
    var fit = ctx.FG.ringFit(row, r, { seed: "eventer-pricing-ring", rx0: 1.8, ry0: 8, wobble: .012, steps: 24, stroke: 1.4, svg: s });
    if (fit.d) ctx.FG.path(s, fit.d, UVC, 1.4);
  }

  /* ------------------------------------------------------------ desktop: each developed zone hangs into the gap
     below its claim (never into the next header), so the row is as tall as the claim: no blank band
     under 01, 03 or 06 with the lamp off, and arming still moves nothing */
  function hang(ctx) {
    [].forEach.call(ctx.X.querySelectorAll(".folder .devz"), function (z) { z.style.marginBottom = ""; });
    if (HOST.w < 1100) return;
    [].forEach.call(ctx.X.querySelectorAll(".folder .devz"), function (z) {
      var box = z.parentElement, para = box.querySelector(":scope > .para"); if (!para) return;
      var over = z.getBoundingClientRect().bottom - para.getBoundingClientRect().bottom; if (over <= 0) return;
      var host = box.classList.contains("z") ? box : box.parentElement, nx = host.nextElementSibling;
      while (nx && !nx.getClientRects().length) nx = nx.nextElementSibling;
      var gap = nx ? nx.getBoundingClientRect().top - box.getBoundingClientRect().bottom : 0;
      var m = Math.max(0, Math.min(over, gap - 28));
      if (m > 0) z.style.marginBottom = -Math.round(m) + "px";
    });
  }

  /* ------------------------------------------------------------ the header rows: a dashed rule shorter than 40px
     reads as a fleck, not a rule; it is left out there (and kept everywhere it has room) */
  function rules(ctx) {
    [].forEach.call(ctx.X.querySelectorAll(".folder .zr"), function (zr) {
      zr.classList.remove("ev-norule");
      var zl = zr.querySelector(".zl"); if (!zl) return;
      var room = zr.getBoundingClientRect().right - zl.getBoundingClientRect().right - (parseFloat(getComputedStyle(zr).columnGap) || 0);
      if (room < 40) zr.classList.add("ev-norule");
    });
  }

  /* ============================================================ E11 · THE CONVERGENCE PLATE
     The file's own diagram drawn as the guide's PL. II: five departments in file order, five hand
     curves arriving tangent (one darker bundle), ONE ice head into THE CUSTOMER, and the file's return
     as a phantom path of motion lettered with its own words. Geometry is recomputed from the panel's
     width, never scaled. */
  var NAMES = ["PRODUCT", "MARKETING", "FINANCE", "R&D", "BUSINESS DEVELOPMENT"];
  function lsPx(t) { return parseFloat(getComputedStyle(t).letterSpacing) || 0; }
  function vis(t) { return t.getComputedTextLength() - lsPx(t); }
  function put(t, x, y) { t.setAttribute("x", n1(x + lsPx(t) / 2)); t.setAttribute("y", n1(y)); t.setAttribute("text-anchor", "middle"); t.removeAttribute("transform"); }
  /* the label face that lets the longest label sit on one line inside its box (no line break: no tag inside SVG text) */
  function fitLabels(T, room, base) {
    var ladder = [[base, .14], [base, .08], [base, .06], [base, .04], [base - .5, .04], [base - 1, .02], [base - 1.5, 0]], k;
    for (k = 0; k < ladder.length; k++) {
      T.dept.forEach(function (t) { t.style.fontSize = ladder[k][0] + "px"; t.style.letterSpacing = ladder[k][1] + "em"; });
      if (vis(T.dept[4]) <= room) break;
    }
  }

  /* the desktop row: boxes in file order on one row, the circle at the right. BUSINESS DEVELOPMENT, the
     last box, keeps a horizontal run of at least 100px before the meeting point, so its curve arrives
     tangent like the other four (never a J-hook into the head). Below the circle, a footer band under
     a hairline carries the caption, as the guide's plates do. */
  function rowForm(W, T) {
    T.dept.forEach(function (t) { t.style.fontSize = ""; t.style.letterSpacing = ""; });
    var ws = T.dept.map(vis), combos = [[100, 22, 14, 32, 30], [96, 18, 12, 32, 30], [88, 14, 10, 28, 28]];
    for (var c = 0; c < combos.length; c++) {
      var r = combos[c][0], pad = combos[c][1], gap = combos[c][2], x0 = combos[c][3], x = x0, boxes = [];
      ws.forEach(function (w) { var bw = Math.max(pad === 22 ? 84 : 76, Math.round(w + 2 * pad)); boxes.push({ x: x, y: 118, w: bw, h: 52 }); x += bw + gap; });
      var end = x - gap, cx = W - combos[c][4] - r, cy = 318, mx = cx - r - 14, bd = boxes[4].x + boxes[4].w / 2;
      if (bd <= mx - 100 && end <= cx - r - 8) return { kind: "row", W: W, H: 530, band: 470, boxes: boxes, r: r, cx: cx, cy: cy, mx: mx, x0: x0, end: end };
    }
    return null;
  }
  /* the vertical form (phone and narrow): boxes stacked in file order, the circle below */
  function colForm(W, T) {
    var g = { kind: "col", W: W, boxes: [] }, i;
    if (W >= 300) {
      var bw = Math.min(200, W - 150);
      for (i = 0; i < 5; i++) g.boxes.push({ x: 22, y: 78 + 54 * i, w: bw, h: 40 });
      g.r = 58; g.cx = W - 88; g.cy = 432; g.H = 560; g.lane = null;
    } else {
      /* below 300 the designer's split label would need a tag inside the SVG text: the boxes widen
         instead, the five lines join one lane at the right, and the circle sits under the stack */
      var bw2 = Math.min(200, W - 88);
      for (i = 0; i < 5; i++) g.boxes.push({ x: 22, y: 78 + 54 * i, w: bw2, h: 40 });
      g.lane = W - 54; g.r = 50; g.cx = Math.round((22 + g.lane) / 2); g.ym = 78 + 54 * 4 + 40 + 22; g.cy = g.ym + 70 + g.r + 14; g.H = g.cy + g.r + 64;
    }
    fitLabels(T, g.boxes[0].w - 16, 11);
    return g;
  }

  function plate(ctx) {
    var X = ctx.X, FG = ctx.FG, wrap = X.querySelector(".convwrap"), sv = wrap && wrap.querySelector("svg.conv"); if (!sv) return;
    var texts = [].slice.call(sv.querySelectorAll("text")), by = function (s) { return texts.filter(function (t) { return t.textContent === s; })[0]; };
    var T = { dept: NAMES.map(by), the: by("THE"), cust: by("CUSTOMER"), cap: by("SHARED RESPONSIBILITY"),
      ret: texts.filter(function (t) { return /^CUSTOMER INSIGHT/.test(t.textContent); })[0] };
    if (T.dept.some(function (t) { return !t; }) || !T.the || !T.cust || !T.cap || !T.ret) return;   /* the file changed: today's diagram stays */
    sv.classList.add("ev-plate"); wrap.classList.add("ev-plate-wrap");
    T.dept.forEach(function (t) { t.classList.add("ev-lbl"); });
    T.dept[4].classList.add("ev-halo");
    T.the.classList.add("ev-cust"); T.cust.classList.add("ev-cust");
    T.ret.classList.add("ev-ret", "ev-halo"); T.cap.classList.add("ev-cap");

    var narrow = innerWidth < 861, swipe = ctx.scroller && narrow;
    wrap.classList.toggle("ev-swipe", swipe);
    wrap.style.maxWidth = "";
    var W = wrap.clientWidth, g = swipe ? rowForm(880, T) : rowForm(W, T);
    if (!g) { var Wc = Math.min(W, 420); if (Wc < W) wrap.style.maxWidth = Wc + "px"; g = colForm(Wc, T); }
    sv.setAttribute("viewBox", "0 0 " + g.W + " " + g.H);
    sv.style.width = g.W + "px"; sv.style.height = g.H + "px"; sv.style.minWidth = "0";
    wrap.setAttribute("data-form", g.kind);

    var s = ctx.host(wrap); s.style.zIndex = "-1";
    s.setAttribute("viewBox", "0 0 " + g.W + " " + g.H); s.style.width = g.W + "px"; s.style.height = g.H + "px";
    var P = new FG.Pen("eventer-07-frame"), W2 = g.W, H = g.H, row = g.kind === "row";
    if (swipe) FG.el(s, "rect", { x: 0, y: 0, width: W2, height: H, fill: CARD });
    FG.path(s, P.rect(row ? 12 : 10, row ? 12 : 10, W2 - (row ? 24 : 20), H - (row ? 24 : 20), { overshoot: 3 }), INK, row ? 1.4 : 1.3);
    /* the footer band's hairline, frame to frame */
    if (row && g.band) FG.path(s, P.line(12, g.band, W2 - 12, g.band, { passes: 1, rough: .25 }), INK, .9);

    /* the return: a phantom path of motion, from THE CUSTOMER back to the start of the row */
    var cx = g.cx, cy = g.cy, r = g.r, retD, headD, tip;
    if (row) {
      var a = -35.5 * Math.PI / 180, sx = cx + r * Math.cos(a), sy = cy + r * Math.sin(a);
      var tx = g.x0 + 6;
      retD = "M" + n1(sx) + " " + n1(sy) + "C" + n1(Math.min(cx + 1.115 * r, W2 - 24)) + " " + n1(sy - 90) + " " + n1(cx + .77 * r) + " 70 " + n1(cx - 40) + " 70L" + (tx + 2) + " 70";
      tip = [tx, 70];
      headD = "M" + n1(tx + 9 * Math.cos(.52)) + " " + n1(70 - 9 * Math.sin(.52)) + "L" + tx + " 70L" + n1(tx + 9 * Math.cos(.52)) + " " + n1(70 + 9 * Math.sin(.52));
    } else {
      var xr = W2 - 22;
      retD = "M" + n1(cx + r) + " " + cy + "C" + xr + " " + cy + " " + xr + " " + (cy - 30) + " " + xr + " " + (cy - 70) + "L" + xr + " 74Q" + xr + " 44 " + (xr - 30) + " 44L29 44";
      tip = [27, 44];
      headD = "M" + n1(27 + 8 * Math.cos(.52)) + " " + n1(44 - 8 * Math.sin(.52)) + "L27 44L" + n1(27 + 8 * Math.cos(.52)) + " " + n1(44 + 8 * Math.sin(.52));
    }
    var ret = FG.path(s, retD, INK, row ? 1.3 : 1.2, { opacity: ".62", "stroke-dasharray": row ? "14 4 2 4 2 4" : "12 4 2 4 2 4", "stroke-linecap": "butt" });
    var retHead = FG.path(s, headD, INK, row ? 1.3 : 1.2, { opacity: ".62" });

    /* the five inflows: one curve per department, each double-passed, all arriving tangent at one point */
    var curves = [], mx, my;
    /* BUSINESS DEVELOPMENT's ice line is laid first, so where the five run as one the bundle reads as ink */
    [4, 0, 1, 2, 3].map(function (i) { return [g.boxes[i], i]; }).forEach(function (bi) {
      var b = bi[0], i = bi[1];
      var CP = new FG.Pen("eventer-07-curve-" + i), hero = i === 4, col = hero ? ICET : INK, w = hero ? 1.7 : 1.3, d1, d2;
      function seg(j) {
        if (row) {
          var bx = b.x + b.w / 2; mx = g.mx; my = cy;
          return "M" + n1(bx + j(.5)) + " " + (b.y + b.h) + "C" + n1(bx + j(1)) + " " + n1(b.y + b.h + 92 + j(2)) + " " + n1(bx + .55 * (mx - bx) + j(2)) + " " + n1(my + j(.4)) + " " + mx + " " + my;
        }
        if (!g.lane) {
          var y = b.y + b.h / 2; mx = W2 - 88; my = 360;
          return "M" + (b.x + b.w) + " " + n1(y + j(.4)) + "C" + n1(W2 - 98 + j(1)) + " " + n1(y + j(.6)) + " " + n1(W2 - 88 + j(.4)) + " " + n1(y + 20 + j(1)) + " " + mx + " " + my;
        }
        var y2 = b.y + b.h / 2, L = g.lane; mx = cx; my = cy - r - 14;
        return "M" + (b.x + b.w) + " " + n1(y2 + j(.4)) + "C" + n1(L + j(.5)) + " " + n1(y2 + j(.5)) + " " + n1(L + j(.3)) + " " + n1(y2 + 20) + " " + L + " " + g.ym +
          "C" + L + " " + (g.ym + 28) + " " + cx + " " + (my - 30) + " " + mx + " " + my;
      }
      d1 = seg(function (m) { return CP.j(m * .4); }); d2 = seg(function (m) { return CP.j(m); });
      curves.push(FG.path(s, d1, col, w, { opacity: ".95" }), FG.path(s, d2, col, w, { opacity: ".5" }));
    });

    /* the boxes: rough double strokes; BUSINESS DEVELOPMENT hatched as the file colours it */
    g.boxes.forEach(function (b, i) {
      var BP = new FG.Pen("eventer-07-box-" + i), hero = i === 4;
      if (hero) FG.path(s, BP.hachureRect(b.x + 1.5, b.y + 1.5, b.w - 3, b.h - 3, { gap: 5, angle: 49, rough: .45 }).d, ICE, 1.1);
      FG.path(s, BP.rect(b.x, b.y, b.w, b.h, { overshoot: row ? 2.5 : 2 }), hero ? ICET : INK, hero ? 1.6 : (row ? 1.3 : 1.2));
    });

    /* THE CUSTOMER: a compass circle, two passes, the join overlapping near 11 o'clock */
    var CP2 = new FG.Pen("eventer-07-customer"), a0 = -123 * Math.PI / 180;
    FG.path(s, CP2.arc(cx, cy, r, a0, a0 + Math.PI * 2 + 6 * Math.PI / 180, { wobble: .6 }), ICET, row ? 2.2 : 2);

    /* ONE head: a short ice shaft from the meeting point to the circle, two open arms */
    var HP = new FG.Pen("eventer-07-head"), hx, hy, ang, arm = row ? 11 : 9, spread = 28 * Math.PI / 180, shaft, arms = [];
    if (row) { hx = cx - r - 1; hy = cy; ang = 0; }
    else { hx = cx; hy = cy - r - 1; ang = Math.PI / 2; }
    shaft = FG.path(s, HP.line(mx, my, hx, hy, { passes: 1, rough: .2 }), ICET, row ? 1.7 : 1.6);
    [-1, 1].forEach(function (sg) {
      arms.push(FG.path(s, HP.line(hx, hy, hx - arm * Math.cos(ang + sg * spread), hy - arm * Math.sin(ang + sg * spread), { passes: 1, rough: .2 }), ICET, row ? 1.7 : 1.6));
    });

    /* the file's words, placed (attributes only) */
    var lblY = row ? 26 + 4.5 : 20 + 4;
    g.boxes.forEach(function (b, i) { put(T.dept[i], b.x + b.w / 2, b.y + lblY); });
    if (row) {
      T.the.style.fontSize = ""; T.cust.style.fontSize = ""; T.cust.style.letterSpacing = "";
      put(T.the, cx, cy - 6); put(T.cust, cx, cy + 18);
      T.ret.style.fontSize = ""; T.ret.style.letterSpacing = "";
      put(T.ret, (g.x0 + g.end) / 2, 58);
      T.cap.style.fontSize = ""; T.cap.style.letterSpacing = "";
    } else {
      T.the.style.fontSize = "12px"; T.cust.style.fontSize = "12px"; T.cust.style.letterSpacing = r < 56 ? ".12em" : ".16em";
      put(T.the, cx, cy - 4); put(T.cust, cx, cy + 14);
      T.cap.style.fontSize = "11px"; T.cap.style.letterSpacing = ".14em";
      if (W2 >= 300 && !g.lane) {
        T.ret.style.fontSize = "10px"; T.ret.style.letterSpacing = ".02em";
        put(T.ret, W2 / 2, 34);
      } else {
        /* reading upward along the return's long side */
        T.ret.style.fontSize = "10.5px"; T.ret.style.letterSpacing = ".1em";
        var xr2 = W2 - 22, midY = (74 + cy - 70) / 2, bx2 = xr2 - 7;
        put(T.ret, bx2, midY);
        T.ret.setAttribute("transform", "rotate(-90 " + n1(bx2) + " " + n1(midY) + ")");
      }
    }
    var capY = row && g.band ? g.band + 26 : cy + r + 34, cw = vis(T.cap), ccx = Math.min(cx, W2 - (row ? 28 : 24) - cw / 2);
    put(T.cap, ccx, capY);
    /* the twin stroke under SHARED RESPONSIBILITY (E5's recipe) */
    var TP = new FG.Pen("eventer-07-twin"), x1 = ccx - cw / 2 - 3, x2 = ccx + cw / 2 + 3, ty = capY + 7;
    FG.path(s, TP.curve([[x1, ty + TP.j(.4)], [(x1 + x2) / 2, ty + (row ? 2.5 : 2)], [x2, ty + TP.j(.4)]]), ICE, row ? 2.2 : 2);

    /* in today's sideways scroller, a label wholly outside the scroller's window is not painted at all
       (it is clipped); it is also set to opacity 0 so no reading of the page counts a word nobody can see
       there. It stays in the DOM, the text and the accessibility tree; it shows as it scrolls in. */
    wrap.__evClip = function () {
      var wb = wrap.getBoundingClientRect(), sw = wrap.classList.contains("ev-swipe");
      texts.forEach(function (t) {
        var tb = t.getBoundingClientRect();
        t.style.opacity = sw && (tb.right <= wb.left + 1 || tb.left >= wb.right - 1) ? "0" : "";
      });
    };
    if (!wrap.__evClipOn) { wrap.__evClipOn = true; wrap.addEventListener("scroll", function () { if (wrap.__evClip) wrap.__evClip(); }, { passive: true }); }
    wrap.__evClip();

    gesture(ctx, s, wrap, curves, shaft, arms, ret, retD, retHead, row);
  }

  /* ------------------------------------------------------------ question 2, behind ?gesture=1: drawn once.
     (a) 0–700ms the five inflows on ONE clock (no department first); (b) 700–780 the head's two arms;
     (c) 800–1700 the return from THE CUSTOMER back to the row's start, through a solid mask (the
     phantom's dashes never crawl). Phone: the return appears whole at 800. Arming the lamp, stillness,
     a redraw or re-entry: complete. */
  function gesture(ctx, s, wrap, curves, shaft, arms, ret, retD, retHead, row) {
    if (GS.io) { GS.io.disconnect(); GS.io = null; }
    if (ctx.STILL || GS.done) { wrap.setAttribute("data-gesture", "done"); return; }
    var FG = ctx.FG, Ls = curves.map(function (p) { return p.getTotalLength(); });
    curves.forEach(function (p, i) { p.style.strokeDasharray = Ls[i] + " " + Ls[i]; p.style.strokeDashoffset = Ls[i]; });
    [shaft].concat(arms).concat([retHead]).forEach(function (p) { p.style.visibility = "hidden"; });
    var defs = FG.el(s, "defs", {}), mk = FG.el(defs, "mask", { id: "ev-ret-mask", maskUnits: "userSpaceOnUse" });
    var mp = FG.el(mk, "path", { d: retD, stroke: "#fff", "stroke-width": 8, fill: "none" }), ML = mp.getTotalLength();
    mp.style.strokeDasharray = ML + " " + ML; mp.style.strokeDashoffset = ML; ret.setAttribute("mask", "url(#ev-ret-mask)");
    wrap.setAttribute("data-gesture", "armed");
    function finish() {
      curves.forEach(function (p) { p.style.strokeDasharray = ""; p.style.strokeDashoffset = ""; });
      [shaft].concat(arms).concat([retHead]).forEach(function (p) { p.style.visibility = ""; });
      mp.style.strokeDashoffset = 0; wrap.setAttribute("data-gesture", "done");
    }
    /* one observer at a time (the previous draw's is disconnected above); it starts at 40% in view, or,
       for a plate taller than the window can show at 40%, once its top has crossed the window's middle */
    var io = GS.io = new IntersectionObserver(RT.guard(function (es) {
      var en = es[es.length - 1], rb = en.boundingClientRect, mid = HOST.top + HOST.h / 2;
      var seen = en.intersectionRatio >= .4 || (en.isIntersecting && rb.top < mid && rb.bottom > mid);
      if (GS.done || !seen) return;
      GS.done = true; io.disconnect(); GS.io = null; wrap.setAttribute("data-gesture", "running");
      var t0 = performance.now();
      (function frame(now) {
        if (!s.isConnected) return;
        if (ctx.X.classList.contains("uv")) return finish();
        var t = now - t0, p = easeIn(Math.min(1, t / 700));
        curves.forEach(function (c, i) { c.style.strokeDashoffset = Ls[i] * (1 - p); });
        if (t >= 700) { shaft.style.visibility = ""; arms[0].style.visibility = ""; }
        if (t >= 740) arms[1].style.visibility = "";
        if (t >= 800) mp.style.strokeDashoffset = row ? ML * (1 - easeRet(Math.min(1, (t - 800) / 900))) : 0;
        if (t >= (row ? 1700 : 800)) return finish();
        RT.raf(frame);
      })(t0);
    }), { root: HOST.root, threshold: [0, .1, .2, .3, .4, .5, .6, .8, 1] });
    io.observe(wrap);
  }

  return {
    draw: function (ctx) {                                    /* (FG.defs() and the analyst's arrow are the shared draw's) */
      noDashStart(ctx); rules(ctx); hang(ctx); ticks(ctx); twin03(ctx); counts(ctx); ring(ctx); plate(ctx);
    },
    open: function () { GS.done = false; },
    close: function () { if (GS.io) { GS.io.disconnect(); GS.io = null; } }
  };
};
