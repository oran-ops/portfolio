/* LEADERSHIP -- its own plates (built from docs/fieldguide-six/leadership.md). window.FGDOC.leadership(X, FG, RT) makes one
   instance; its draw(ctx) is called by fg.js after the shared drawing on every draw. ctx = {X, DOC, host, hostUV, FG, STILL,
   baselineOf, ink, line, text, uv, scroller}. */
window.FGDOC = window.FGDOC || {};
window.FGDOC.leadership = function (X, FG0, RT) {
  "use strict";
  var HOST = RT.H;

  /* ---------------------------------------------------------- L6 · 05: seat the spacers (once, at parse time)
     05's name is one text node: "Great Managers Solve Today's Problems. Great Leaders Build Tomorrow's System."
     It is split at its own word ends (no character changes) and an EMPTY aria-hidden span is seated at each:
     .ld-gap after a column of the first or second sentence, .ld-brk after the first sentence. */
  var NM = null;
  (function seat() {
    var nm = X.querySelectorAll(".pr .nm2")[4]; if (!nm) return;
    if (nm.querySelector(".ld-brk")) { NM = nm; return; }
    var t = nm.firstChild;
    if (nm.childNodes.length !== 1 || !t || t.nodeType !== 3) return;
    var words = t.data.split(" ");
    if (words.length !== 10 || !/\.$/.test(words[4]) || !/\.$/.test(words[9])) return;   /* not the expected pair: leave it as printed */
    /* after word i: [kind, column]  — 1: c1 line 1, 2: c2, 3: c3, 4: the break, 6/7/8: c1–c3 line 2 */
    var after = { 1: ["ld-gap", 1], 2: ["ld-gap", 2], 3: ["ld-gap", 3], 4: ["ld-brk", 0], 6: ["ld-gap", 1], 7: ["ld-gap", 2], 8: ["ld-gap", 3] };
    var node = t, start = 0, used = 0;                 /* node: the tail run, which begins at `start` in the name */
    for (var i = 0; i < 9; i++) {
      used += words[i].length + (i ? 1 : 0);           /* the end of word i */
      if (!after[i]) continue;
      var rest = node.splitText(used - start); start = used;
      var sp = document.createElement("span");
      sp.className = after[i][0]; sp.setAttribute("aria-hidden", "true");
      if (after[i][1]) sp.setAttribute("data-c", after[i][1]);
      nm.insertBefore(sp, rest);
      node = rest;
    }
    NM = nm;
  })();

  /* draw time: measure each column's pair and pad the narrower one, only where the aligned pair fits */
  function align05() {
    var nm = NM; if (!nm || !nm.isConnected) return;
    var gaps = nm.querySelectorAll(".ld-gap");
    nm.classList.remove("ld-ant");
    [].forEach.call(gaps, function (g) { g.style.width = ""; });
    if (HOST.w < 761) return;
    nm.classList.add("ld-measure");
    var texts = [].filter.call(nm.childNodes, function (n) { return n.nodeType === 3; });   /* 8 runs: 4 per sentence */
    if (texts.length !== 8) { nm.classList.remove("ld-measure"); return; }
    var rg = document.createRange();
    var w = texts.map(function (n) {
      var a = n.data.length - n.data.replace(/^\s+/, "").length, b = n.data.replace(/\s+$/, "").length;
      rg.setStart(n, a); rg.setEnd(n, b); return rg.getBoundingClientRect().width;
    });
    /* the word space, as set (its own advance plus the tracking), from the run that opens on one */
    rg.setStart(texts[1], 0); rg.setEnd(texts[1], texts[1].data.length);
    var sp = rg.getBoundingClientRect().width - w[1];
    nm.classList.remove("ld-measure");
    var em = parseFloat(getComputedStyle(nm).fontSize), extra = .2 * em, cols = [0, 1, 2, 3].map(function (k) { return Math.max(w[k], w[k + 4]); });
    var need = cols[0] + cols[1] + cols[2] + cols[3] + 3 * (sp + extra);
    if (need > nm.clientWidth - 4) return;                                        /* does not fit: two plain sentences */
    [].forEach.call(gaps, function (g, i) {
      var k = +g.getAttribute("data-c") - 1, line = i < 3 ? 0 : 4;
      g.style.width = (cols[k] - w[k + line] + extra).toFixed(2) + "px";
    });
    nm.classList.add("ld-ant");
  }

  /* ---------------------------------------------------------- L1 · the first line's measure: 'Building' and its space, as set */
  function titleLine() {
    var t = X.querySelector(".sttl"), ws = t ? t.querySelectorAll(":scope > .w") : []; if (ws.length < 2) return;
    var sp = ws[0].nextSibling, rg = document.createRange(), px = parseFloat(getComputedStyle(t).fontSize);
    if (!sp || sp.nodeType !== 3 || !px) return;
    rg.selectNodeContents(sp);
    var w = ws[0].getBoundingClientRect().width + rg.getBoundingClientRect().width;
    if (w > 0 && w < px * 6) t.style.setProperty("--ld-bw", ((w + 1) / px).toFixed(4) + "em");
  }

  /* ---------------------------------------------------------- L7 · THE KIT, SEATED
     One cut per piece: the piece's box grown 6px left, top and bottom and 14px right (a finger recess, not a
     gap), corner radii 6 (left) and 18 (right: the finger-scoop). The cuts go through the sheet's paper by its own mask (.folder::before
     already takes var(--sheet-holes)); the wall shadow and the cut edge are drawn under the pieces. */
  var L = 6, T = 6, RX = 14, RL = 6, RR = 18;
  function cutRect(b) { return { x: b.x - L, y: b.y - T, w: b.w + L + RX, h: b.h + 2 * T }; }
  function rr(c, dx, dy) {
    var x = c.x + (dx || 0), y = c.y + (dy || 0), w = c.w, h = c.h, f = function (v) { return v.toFixed(1); };
    return "M" + f(x + RL) + " " + f(y) + "H" + f(x + w - RR) + "A" + RR + " " + RR + " 0 0 1 " + f(x + w) + " " + f(y + RR) +
      "V" + f(y + h - RR) + "A" + RR + " " + RR + " 0 0 1 " + f(x + w - RR) + " " + f(y + h) + "H" + f(x + RL) +
      "A" + RL + " " + RL + " 0 0 1 " + f(x) + " " + f(y + h - RL) + "V" + f(y + RL) + "A" + RL + " " + RL + " 0 0 1 " + f(x + RL) + " " + f(y) + "Z";
  }
  /* ONE FITTED INSERT (review, wf_82eb10ce-2df): the rows the width needs, no more, balanced so no piece is
     left alone where a neighbour could share its row, and every row filled to the tray's measure. Pieces stay
     in file order; each grows by its row's equal share, so widths stay the words' own plus a common margin
     (never a scale). Only flex-basis is written; the rows still come from wrapping. */
  function fit(tools, pieces) {
    pieces.forEach(function (p) { p.style.removeProperty("flex"); });
    tools.classList.add("ld-fit", "ld-fit-measure");
    var cs = getComputedStyle(tools), W = tools.clientWidth - parseFloat(cs.paddingLeft) - parseFloat(cs.paddingRight), g = parseFloat(cs.columnGap) || 0;
    var nat = pieces.map(function (p) { return Math.min(p.getBoundingClientRect().width, W); });
    tools.classList.remove("ld-fit-measure");
    var n = nat.length, rows = 0, run = -1;
    nat.forEach(function (w) { if (run < 0 || run + g + w > W + .01) { rows++; run = w; } else run += g + w; });
    /* best[k][i]: least sum of squared slack setting the first i pieces in k rows */
    var best = [], from = [], k, i, j;
    for (k = 0; k <= rows; k++) { best.push([]); from.push([]); for (i = 0; i <= n; i++) best[k].push(Infinity); }
    best[0][0] = 0;
    for (k = 1; k <= rows; k++) for (i = 1; i <= n; i++) for (j = i - 1; j >= 0; j--) {
      var sum = 0; for (var m = j; m < i; m++) sum += nat[m];
      var slack = W - sum - g * (i - j - 1); if (slack < -.01) break;
      var c = best[k - 1][j] + slack * slack; if (c < best[k][i]) { best[k][i] = c; from[k][i] = j; }
    }
    if (!isFinite(best[rows][n])) { tools.classList.remove("ld-fit"); return; }
    for (k = rows, i = n; k > 0; k--) {
      j = from[k][i]; var tot = 0; for (m = j; m < i; m++) tot += nat[m];
      var share = (W - tot - g * (i - j - 1)) / (i - j) - .3;            /* .3px short per piece: the row closes, the next piece wraps */
      for (m = j; m < i; m++) pieces[m].style.flex = "1 0 " + Math.max(nat[m], nat[m] + share).toFixed(2) + "px";
      i = j;
    }
  }

  var trayHost = null;
  function tray(ctx) {
    var tools = X.querySelector(".tools"), folder = X.querySelector(".folder");
    if (!tools || !folder) return;
    if (trayHost) { trayHost.remove(); trayHost = null; }
    var FG = ctx.FG, pieces = [].slice.call(tools.querySelectorAll(".lg"));
    if (pieces.length) fit(tools, pieces);
    var fb = folder.getBoundingClientRect(), W = fb.width, H = fb.height;
    if (!W || !H || !pieces.length) return;
    /* 1 · the cuts through the sheet's paper: an even-odd path, the sheet minus every slot */
    var d = "M0 0H" + W.toFixed(1) + "V" + H.toFixed(1) + "H0Z";
    pieces.forEach(function (p) { d += rr(cutRect(FG.box(p, folder))); });
    var svg = "<svg xmlns='http://www.w3.org/2000/svg' width='" + W.toFixed(1) + "' height='" + H.toFixed(1) + "' viewBox='0 0 " + W.toFixed(1) + " " + H.toFixed(1) +
      "' preserveAspectRatio='none'><path fill-rule='evenodd' fill='#000' d='" + d + "'/></svg>";
    folder.style.setProperty("--sheet-holes", 'url("data:image/svg+xml,' + encodeURIComponent(svg) + '") 0 0/100% 100% no-repeat');
    tools.classList.add("ld-seated");
    /* 2 · the wall: each slot darkened, minus itself shifted 3.2/3.2 and softened (the sheet's thickness reads at 1x), leaves a crescent on the
       upper-left wall only (the light comes from the top left, as everywhere in the guide) */
    var s = ctx.host(tools); trayHost = s; s.style.zIndex = "-1";
    var tb = tools.getBoundingClientRect(), cuts = pieces.map(function (p) { return cutRect(FG.box(p, tools)); });
    var defs = FG.el(s, "defs", {});
    var fl = FG.el(defs, "filter", { id: "ld-wall-soft", x: "-5%", y: "-5%", width: "110%", height: "110%" });
    FG.el(fl, "feGaussianBlur", { stdDeviation: ".9" });
    var mk = FG.el(defs, "mask", { id: "ld-wall", maskUnits: "userSpaceOnUse", x: -40, y: -40, width: tb.width + 80, height: tb.height + 80 });
    FG.el(mk, "rect", { x: -40, y: -40, width: tb.width + 80, height: tb.height + 80, fill: "#fff" });
    FG.el(mk, "path", { d: cuts.map(function (c) { return rr(c, 3.2, 3.2); }).join(""), fill: "#000", filter: "url(#ld-wall-soft)" });
    FG.el(s, "path", { d: cuts.map(function (c) { return rr(c); }).join(""), fill: "rgba(26,23,20,.40)", mask: "url(#ld-wall)" });
    /* 3 · the cut edge: one hand contour per slot, double-passed, seeded by its place in the file */
    cuts.forEach(function (c, i) {
      var P = new FG.Pen("leadership-cut-" + (i < 9 ? "0" : "") + (i + 1)), o = { rough: .28, bow: .5 }, a = { wobble: .18 }, x = c.x, y = c.y, w = c.w, h = c.h, e = "";
      e += P.line(x + RL, y, x + w - RR, y, o) + P.arc(x + w - RR, y + RR, RR, -Math.PI / 2, 0, a);
      e += P.line(x + w, y + RR, x + w, y + h - RR, o) + P.arc(x + w - RR, y + h - RR, RR, 0, Math.PI / 2, a);
      e += P.line(x + w - RR, y + h, x + RL, y + h, o) + P.arc(x + RL, y + h - RL, RL, Math.PI / 2, Math.PI, a);
      e += P.line(x, y + h - RL, x, y + RL, o) + P.arc(x + RL, y + RL, RL, Math.PI, Math.PI * 1.5, a);
      FG.path(s, e, "rgba(26,23,20,.5)", .8);
    });
  }

  /* a change of the sheet's size without a window resize (a late reflow) re-cuts the tray, never the words */
  var ro = null, lastCtx = null, raf = 0;
  function watch(ctx) {
    lastCtx = ctx;
    var folder = X.querySelector(".folder"), tools = X.querySelector(".tools");
    if (ro || !window.ResizeObserver || !folder || !tools) return;
    ro = new ResizeObserver(RT.guard(function () { cancelAnimationFrame(raf); raf = requestAnimationFrame(RT.guard(function () { if (lastCtx) tray(lastCtx); })); }));
    ro.observe(folder); ro.observe(tools);
  }

  return {
    draw: function (ctx) {
      titleLine();
      align05();
      tray(ctx);
      watch(ctx);
    },
    close: function () { if (ro) { ro.disconnect(); ro = null; } cancelAnimationFrame(raf); lastCtx = null; }
  };
};
