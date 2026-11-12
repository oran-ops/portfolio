/* OASIS -- its own plates (built from docs/fieldguide-six/oasis.md). window.FGDOC.oasis(X, FG, RT) makes one instance; its
   draw(ctx) is called by fg.js after the shared drawing on every draw. ctx = {X, DOC, host, hostUV, FG, STILL, baselineOf,
   ink, line, text, uv, scroller}.
   Nothing here writes, moves or wraps a word. What it adds: classes on existing elements, x/y/anchor
   attributes and a size on the B plate's seven existing <text> nodes (positions, never content), one
   wordless aria-hidden <g> inside the file's own B svg (rebuilt on every draw), drawings in host()/hostUV(),
   and one CSS highlight range over the word 'profitability' in 03 item 3 (no element is added). */
window.FGDOC = window.FGDOC || {};
window.FGDOC.oasis = function (X, FG, RT) {
  "use strict";
  var HOST = RT.H;

  /* THE LAMP'S NAMED CITATIONS beyond the shared list: note 1 'Profitability sits twice' —
     the 02 cell whose whole text is 'Profitability' (a class on the cell), and the word in 03 item 3
     (a highlight range; the row's text stays one text node) */
  var cell = null, word = null;
  [].forEach.call(X.querySelectorAll(".grid2c .dash"), function (d) { if (d.textContent.trim() === "Profitability") { cell = d; d.classList.add("cite", "oas-cw"); } });
  [].forEach.call(X.querySelectorAll(".list .lg"), function (l) {
    [].forEach.call(l.childNodes, function (n) {
      var i = n.nodeType === 3 ? n.nodeValue.indexOf("the profitability-based") : -1;
      if (i < 0 || word) return;
      word = document.createRange(); word.setStart(n, i + 4); word.setEnd(n, i + 4 + 13);
    });
  });
  if (word && window.CSS && CSS.highlights && window.Highlight) CSS.highlights.set("oasis-cite", new Highlight(word));
  /* the highlight cannot transition: it comes on with the citations (420ms after arming), off at once */
  var lit, was = false;
  var mo = new MutationObserver(RT.guard(function () {
    var on = X.classList.contains("uv");
    if (on === was) return;                            /* only the lamp's own change; never react to our class */
    was = on; clearTimeout(lit);
    if (!on) { if (X.classList.contains("oas-lit")) X.classList.remove("oas-lit"); return; }
    if (RT.still()) X.classList.add("oas-lit"); else lit = RT.later(function () { if (X.classList.contains("uv") && !X.classList.contains("oas-lit")) X.classList.add("oas-lit"); }, 420);
  }));

  var INK = "#1a1714", LINE = "#C98A3A", TXT = "#7E5416", UVC = "#9B7BFF";
  /* a label's width as the svg itself sets it (a canvas measures another face than svg text gets) */
  function measure(t, fs, ls) { t.style.fontSize = fs + "px"; t.style.letterSpacing = ls + "em"; return t.getComputedTextLength(); }
  function disc(cx, cy, r) { return "M" + (cx - r) + " " + cy + "a" + r + " " + r + " 0 1 0 " + 2 * r + " 0a" + r + " " + r + " 0 1 0 " + (-2 * r) + " 0Z"; }

  var draw = function (o) {
    var FG = o.FG;                                       /* (the shared draw() installs FG.defs() on every draw) */

    /* 03 · the brush ticks: the shared code now lays them in the TEXT tier (the ✓ is text; 2026-10-16) */

    /* 02 · THE TITLE BLOCK: a rough outer frame (double pass, corners overshooting 3px) and one-pass
       internal rules at the cells' own edges, so the grid follows the cells at every width */
    var g2 = X.querySelector(".grid2c");
    if (g2) {
      var s2 = o.host(g2), P2 = new FG.Pen("oasis-titleblock"), W2 = g2.clientWidth, H2 = g2.clientHeight, xs = {}, ys = {};
      FG.path(s2, P2.rect(0.5, 0.5, W2 - 1, H2 - 1, { overshoot: 3 }), INK, 1.3);
      [].forEach.call(g2.querySelectorAll(".dash"), function (c) { var b = FG.box(c, g2); if (b.x > 2) xs[Math.round(b.x)] = 1; if (b.y > 2) ys[Math.round(b.y)] = 1; });
      Object.keys(xs).forEach(function (x) { FG.path(s2, P2.line(+x, 0, +x, H2, { rough: .5, passes: 1 }), INK, .9, { opacity: ".55" }); });
      Object.keys(ys).forEach(function (y) { FG.path(s2, P2.line(0, +y, W2, +y, { rough: .5, passes: 1 }), INK, .9, { opacity: ".55" }); });
    }

    /* 04 · THE SCHEDULE PLATE's four screws, 13px in (11 on a phone): a domed disc, a rough rim, one slot */
    var pl = X.querySelector(".chips");
    if (pl) {
      var s4 = o.host(pl), pw = pl.clientWidth, ph = pl.clientHeight, ins = HOST.w <= 760 ? 11 : 13;
      var dd = FG.el(s4, "defs", {}), rg = FG.el(dd, "radialGradient", { id: "oas-screw", cx: "35%", cy: "35%", r: "70%" });
      [["0", "#FBEFD6"], [".55", "#E2B873"], ["1", "#A9732C"]].forEach(function (st) { FG.el(rg, "stop", { offset: st[0], "stop-color": st[1] }); });
      [[ins, ins], [pw - ins, ins], [ins, ph - ins], [pw - ins, ph - ins]].forEach(function (c, i) {
        var P = new FG.Pen("oasis-screw-" + i), a = P.R() * Math.PI;
        FG.el(s4, "circle", { cx: c[0], cy: c[1], r: 4.6, fill: "url(#oas-screw)" });
        FG.path(s4, P.ellipse(c[0], c[1], 4.6, 4.6, { wobble: .04, steps: 10 }), TXT, .9);
        FG.path(s4, P.line(c[0] - Math.cos(a) * 3.4, c[1] - Math.sin(a) * 3.4, c[0] + Math.cos(a) * 3.4, c[1] + Math.sin(a) * 3.4, { rough: .2, passes: 1 }), "#4a3210", 1.1);
      });
    }

    setOut(o);
    rings(o);
    tracing(o);
  };

  /* ==========================================================================================
     B · THE SIX-FOLD SETTING-OUT. The file's ring, six spokes, hub and six nodes, redrawn in ink;
     under them the six-petal rosette a compass draws with the ring's own radius: graphite arcs about
     each node (each from node k−1 through the centre to node k+1), the petals hatched brass at 49°.
     Each petal runs from the centre to ONE function, around the spoke the file draws: no relation
     between two functions, no order, no rank. R by the fit rule, from the labels' measured widths. */
  function setOut(o) {
    var FG = o.FG, col = X.querySelector(".hairtop .ringlbl"); col = col && col.parentElement;
    var sv = col && col.querySelector(":scope > svg:not(.fg-svg)"); if (!sv) return;
    var texts = [].slice.call(sv.querySelectorAll("text")); if (texts.length !== 7) return;
    /* the svg's own width: on a phone it runs into the sheet's side padding, wider than its column */
    var ceo = texts[0], labs = texts.slice(1), W = Math.floor(sv.getBoundingClientRect().width) || col.clientWidth;
    var A = [0, 1, 2, 3, 4, 5].map(function (k) { return -Math.PI / 2 + k * Math.PI / 3; });
    var side = [0, 1, 1, 0, -1, -1];                    /* 1: right of the ring, -1: left, 0: on the axis */
    /* configurations in order of preference; the first that keeps R at or above its floor is used */
    /* R2 OA1: the second 'beside' is kept only where it truly fits at R >= 110 (from 503px); below it the CALLOUT
       rosette: the six-fold at the card's full width, the four side labels lifted over and under the ring's
       shoulders, each tied to its own node by a graphite leader (the guide's PL. IV callouts). The 'stack'
       forms stay as the fallback for a card too narrow for the callout (never at 320px and up). */
    var CF = [
      { mode: "beside", fs: 12.5, ls: .18, off: 24, hub: 34, node: 9.5, cfs: 14, cls: .2, rmax: 172, floor: 120 },
      { mode: "beside", fs: 11, ls: .12, off: 14, hub: 24, node: 7, cfs: 12, cls: .2, rmax: 120, floor: 110, edge: 1 },
      { mode: "callout", fs: W < 290 ? 10.5 : 11, ls: W < 290 ? .1 : .12, node: W < 290 ? 7 : 8, cfs: 13, cls: .2, floor: 1 },
      { mode: "stack", fs: 11, ls: .12, hub: 24, node: 7, cfs: 12, cls: .2, rmax: 110, floor: 56 },
      { mode: "stack", fs: 10, ls: .06, hub: 22, node: 7, cfs: 12, cls: .16, rmax: 110, floor: 50 },
      { mode: "stack", fs: 9, ls: .02, hub: 17, node: 6, cfs: 10.5, cls: .12, rmax: 110, floor: 0 }];
    var c, R, Lw;
    for (var ci = 0; ci < CF.length; ci++) {
      c = CF[ci]; Lw = labs.map(function (t) { return measure(t, c.fs, c.ls); });
      R = fit(c, Lw, W);
      if (R >= c.floor) break;
    }
    R = Math.max(30, Math.floor(R));
    var CO = c.mode === "callout";
    var hub = c.mode === "beside" ? c.hub : CO ? Math.max(24, Math.min(.22 * R, 32)) : Math.max(15, Math.min(c.hub, R * .4)), nr = c.node, capH = c.fs * .73;
    /* R2 review fix (OA1 at 320-330): on the narrowest cards (W < 300) the two lower side labels are long enough to
       reach the bottom node, and on the old line they stood level with it (the eye paired 'CUSTOMER SUCCESS' with
       FINANCE's node). There they drop below the node (baseline cy+R+16+capH: their caps 9px under its disc), FINANCE
       below them (baseline cy+R+44, >= 8px under their baseline), the card 10px taller. Nothing else moves. */
    var LOW = CO && W < 300;
    var top = c.mode === "beside" ? (ci === 0 ? 85 : 60) : nr + 9 + capH + 20, H = CO ? 2 * R + 110 + (LOW ? 10 : 0) : Math.round(2 * R + 2 * top);
    var cx = W / 2, cy = CO ? R + 58 : H / 2 + (c.mode === "beside" && ci === 0 ? 4 : 0);
    var N = A.map(function (a) { return [cx + Math.cos(a) * R, cy + Math.sin(a) * R]; });
    sv.setAttribute("viewBox", "0 0 " + W + " " + H);

    /* the drawing: one wordless group, first in the svg (under the seven strings) */
    var old = sv.querySelector(":scope > g.oas-plate"); if (old) old.remove();
    var g = document.createElementNS(FG.NS, "g"); g.setAttribute("class", "oas-plate"); g.setAttribute("aria-hidden", "true");
    sv.insertBefore(g, sv.firstChild);
    function P(d, cls, w, extra) { var a = { "class": cls }; if (w) a["stroke-width"] = w; for (var k in extra) a[k] = extra[k]; return FG.path(g, d, null, 0, a); }
    function petal(k, steps) {                          /* the lens about nodes k−1 and k+1, from the centre to node k */
      var pts = [], c1 = N[(k + 5) % 6], c2 = N[(k + 1) % 6], i, a;
      function span(cn, p, q) { var a0 = Math.atan2(p[1] - cn[1], p[0] - cn[0]), a1 = Math.atan2(q[1] - cn[1], q[0] - cn[0]); if (a1 - a0 > Math.PI) a1 -= 2 * Math.PI; if (a0 - a1 > Math.PI) a1 += 2 * Math.PI; return [a0, a1]; }
      var s1 = span(c1, [cx, cy], N[k]), s2 = span(c2, N[k], [cx, cy]);
      for (i = 0; i <= steps; i++) { a = s1[0] + (s1[1] - s1[0]) * i / steps; pts.push([c1[0] + Math.cos(a) * R, c1[1] + Math.sin(a) * R]); }
      for (i = 1; i < steps; i++) { a = s2[0] + (s2[1] - s2[0]) * i / steps; pts.push([c2[0] + Math.cos(a) * R, c2[1] + Math.sin(a) * R]); }
      return pts;
    }
    var G = new FG.Pen("oasis-rosette"), gap = R < 90 ? 4 : 5;
    /* 1 · the petal hatch, brass, 49°, uniform (emphasis, never data) */
    N.forEach(function (n, k) { P(G.hachure(petal(k, 24), { gap: gap, angle: 49, rough: .25 }).d, "oas-hatch", 1); });
    /* 2 · graphite construction: six arcs of radius R, one about each node, 120° each */
    var gr = FG.el(g, "g", { filter: "url(#fg-graphite)" });
    N.forEach(function (n, k) { FG.path(gr, G.arc(n[0], n[1], R, A[k] + Math.PI * 2 / 3, A[k] + Math.PI * 4 / 3, { passes: 1, wobble: R < 90 ? .2 : .35 }), null, 0, { "class": "oas-gr", "stroke-width": 1 }); });
    /* 3 · the file's ring, ink, double pass */
    var I = new FG.Pen("oasis-ring");
    P(I.arc(cx, cy, R, -Math.PI / 2, Math.PI * 1.5 + .03, { wobble: R < 90 ? .3 : .5 }), "oas-ink", R < 90 ? 1.4 : 1.6);
    /* 4 · the six spokes, from the hub to the node */
    N.forEach(function (n, k) {
      var a = A[k], r0 = hub + 2, r1 = R - nr - 1.5, SP = new FG.Pen("oasis-spoke-" + k);
      P(SP.line(cx + Math.cos(a) * r0, cy + Math.sin(a) * r0, cx + Math.cos(a) * r1, cy + Math.sin(a) * r1, { rough: .6 }), "oas-ink", R < 90 ? 1.1 : 1.25);
    });
    /* 5 · the CEO hub, card-filled, rim double pass */
    P(disc(cx, cy, hub), "oas-hub");
    P(I.ellipse(cx, cy, hub, hub, { wobble: .02, steps: 14 }), "oas-ink", R < 90 ? 1.5 : 1.8);
    /* 6 · the six nodes: brass discs, a rim in the text tier */
    N.forEach(function (n, k) {
      P(disc(n[0], n[1], nr), "oas-node");
      P(new FG.Pen("oasis-node-" + k).ellipse(n[0], n[1], nr, nr, { wobble: .03, steps: 10 }), "oas-rim", R < 90 ? 1.1 : 1.3);
    });

    /* the seven strings: positions only */
    function put(t, x, y, anchor, fs, ls) {
      var sh = anchor === "middle" ? fs * ls / 2 : anchor === "end" ? fs * ls : 0;   /* letter-spacing trails the last glyph */
      t.setAttribute("x", (x + sh).toFixed(1)); t.setAttribute("y", y.toFixed(1)); t.setAttribute("text-anchor", anchor);
      t.style.fontSize = fs + "px"; t.style.letterSpacing = ls + "em";
    }
    put(ceo, cx, cy + c.cfs * .36, "middle", c.cfs, c.cls);
    if (CO) {
      /* R2 OA1 · the callout: OPERATIONS and FINANCE on the axis; TECHNICAL TEAMS / PRODUCTION over the ring's
         shoulders, MARKETING / CUSTOMER SUCCESS under them, each standing over its own node. The leaders:
         graphite, one pass, vertical from 4.5px off the label to 3px off its node, a 1.9px dot at the label
         end; wholly outside the ring; one per side label, none between functions, none to the CEO. */
      var yUp = cy - R - 9, yDn = cy + R + (LOW ? 16 : 9) + capH, lg = FG.el(g, "g", { filter: "url(#fg-graphite)" });
      labs.forEach(function (t, k) {
        var n = N[k], sd = side[k];
        if (!sd) { put(t, cx, k === 0 ? cy - R - 30 : cy + R + (LOW ? 44 : 34), "middle", c.fs, c.ls); return; }
        var up = k === 1 || k === 5, y = up ? yUp : yDn;
        put(t, sd < 0 ? Math.max(12, n[0] - 24) : Math.min(W - 12, n[0] + 24), y, sd < 0 ? "start" : "end", c.fs, c.ls);
        var y0 = up ? y + 4.5 : y - capH - 4.5, y1 = up ? n[1] - nr - 3 : n[1] + nr + 3;
        FG.path(lg, new FG.Pen("oasis-callout-" + k).line(n[0], y0, n[0], y1, { rough: .25, passes: 1 }), null, 0, { "class": "oas-gr oas-lead", "stroke-width": 1.25 });
        FG.path(lg, disc(n[0], y0, 1.9), null, 0, { "class": "oas-gr oas-lead oas-dot" });
      });
      return;
    }
    labs.forEach(function (t, k) {
      var n = N[k], sd = side[k];
      if (c.mode === "beside") {
        if (!sd) put(t, cx, k === 0 ? n[1] - (ci === 0 ? 26 : 19) : n[1] + (ci === 0 ? 36 : 27), "middle", c.fs, c.ls);
        else put(t, n[0] + sd * c.off, n[1] + c.fs * .4, sd > 0 ? "start" : "end", c.fs, c.ls);
      } else {
        if (!sd) put(t, cx, k === 0 ? n[1] - nr - 9 : n[1] + nr + 9 + capH, "middle", c.fs, c.ls);
        else {
          var up = k === 1 || k === 5, d = nr + 6, fx = ringX(R, .5 * R + d), x = cx + sd * (fx + 5);
          put(t, x, up ? n[1] - d : n[1] + d + capH, sd > 0 ? "start" : "end", c.fs, c.ls);
        }
      }
    });
  }
  function ringX(R, dy) { return Math.sqrt(Math.max(0, R * R - dy * dy)); }
  /* the largest R at which every label stays on the card with an 8px margin and clear of the ring */
  function fit(c, Lw, W) {
    if (c.mode === "beside") {
      var Ll = Math.max(Lw[4], Lw[5]), Lr = Math.max(Lw[1], Lw[2]);   /* labs 4,5 sit left of the ring; 1,2 right */
      var R = (W - Ll - Lr - 2 * (c.off + 8)) / 1.732;
      /* R2 OA1 · the second 'beside' must truly fit to be kept: each side's longer label 8px inside the card. (The
         split above shares the space evenly, so the longer side's label ran (Lr - Ll)/2 = 3.7px past its 8px:
         4.3px from the card at 495-519px.) Where it is capped at rmax (from ~520px) nothing changes. */
      if (c.edge) R = Math.min(R, (W / 2 - 8 - c.off - Math.max(Ll, Lr)) / .866);
      /* the axis labels must also fit their own width */
      return Math.min(c.rmax, R, Math.max(Lw[0], Lw[3]) > W - 16 ? 0 : 1e9);
    }
    if (c.mode === "callout") {                         /* R2 OA1: R from the card's width; the two labels on each
                                                           shoulder line must keep 8px apart, the axis labels fit */
      var Rc = Math.min(146, Math.floor((W - 52) / 2)), nx = W / 2 - Rc * Math.cos(Math.PI / 6);
      var xl = Math.max(12, nx - 24), xr = Math.min(W - 12, W - nx + 24);
      if (xl + Math.max(Lw[4], Lw[5]) + 8 > xr - Math.max(Lw[1], Lw[2]) || Math.max(Lw[0], Lw[3]) > W - 16) return 0;
      return Rc;
    }
    for (var R2 = c.rmax; R2 >= 20; R2 -= 1) {
      var d = c.node + 6, fx = ringX(R2, .5 * R2 + d), ok = true;
      [1, 2, 4, 5].forEach(function (k) { if (fx + 5 + Lw[k] > W / 2 - 8) ok = false; });
      if (Math.max(Lw[0], Lw[3]) > W - 16) ok = false;
      if (ok) return R2;
    }
    return 0;
  }

  /* the lamp: a violet hand ring around each 'Profitability' it lights (on with the citations, off at once).
     As XTIX's 'enterprise' ring: narrow and tall (rx w/2+2.5, ry h/2+8), so its ends sit in the word
     spaces, never on the neighbouring letters; the row's ring is painted under the glyphs (CSS). */
  function rings(o) {
    var FG = o.FG;
    /* fitted (R2 D5): today's ellipse (rx w/2+2.5, ry h/2+8), brought in only as far as it must to keep 2px
       off every neighbouring letter (FG.ringFit; same seeds, stroke and glow). ONE NAMED EXEMPTION: the '-'
       immediately after 'profitability' in 03 — the file joins the word to its hyphen ('profitability-based'),
       so the ring around the word must cross it; nothing else is exempt. */
    [[cell, null], [word && word.startContainer.parentElement, word]].forEach(function (pr, i) {
      var hostEl = pr[0]; if (!hostEl) return;
      var rr = pr[1];
      if (!rr) { rr = document.createRange(); rr.selectNodeContents(hostEl); }
      if (!rr.getBoundingClientRect().width) return;
      var ex = [];
      if (pr[1]) { var tn = pr[1].endContainer, at = pr[1].endOffset; if (tn.nodeType === 3 && tn.data.charAt(at) === "-") { var hy = document.createRange(); hy.setStart(tn, at); hy.setEnd(tn, at + 1); ex.push(hy); } }
      var s = o.hostUV(hostEl);
      s.classList.add("uv-ring");
      var fit = FG.ringFit(hostEl, rr, { seed: "oasis-profit-ring-" + i, rx0: 2.5, ry0: 8, wobble: .025, steps: 20, stroke: 1.4, exempt: ex, svg: s });
      FG.path(s, fit.d, UVC, 1.4);
    });
  }

  /* THE LIGHT DRAWING (zone 3, armed only): 'Ten built. Seven installed to run them.' as two louvre
     banks in section — ten blades and seven, hung from one head line at one pitch, in the note's
     order. Appears whole with its zone; no labels, numbers, frame, axis or arrow. */
  function tracing(o) {
    var FG = o.FG, z3 = X.querySelector('.hairtop[data-block="reflection"] .devz'); if (!z3) return;
    var Wz = z3.clientWidth, Hz = z3.clientHeight; if (Wz < 10 || Hz < 10) return;
    var narrow = HOST.w < 1100, pitch = narrow ? 17 : 20, bw = narrow ? 28 : 35, rise = narrow ? 11 : 13, gap = narrow ? 44 : 56;
    var total = bw * 2 + gap, x0, y0;
    if (!narrow) { x0 = 640 + (Wz - 640 - total) / 2; y0 = Hz / 2 - (pitch * 10 + rise) / 2 + rise; }
    else { var pb = parseFloat(getComputedStyle(z3).paddingBottom) || 0; if (pb < 200) return; x0 = (Wz - total) / 2; y0 = Hz - pb + (pb - pitch * 10) / 2 - 4; }
    var s = o.hostUV(z3), TP = new FG.Pen("oasis-tracing");
    s.classList.add("uv-trace");
    [10, 7].forEach(function (cnt, i) {
      var x = x0 + i * (bw + gap);
      FG.path(s, TP.line(x - 4, y0, x + bw + 4, y0, { rough: .3 }), UVC, 1.3);
      for (var n = 1; n <= cnt; n++) { var y = y0 + pitch * n; FG.path(s, TP.line(x, y, x + bw, y - rise, { rough: .25 }), UVC, 1.6); }
    });
  }

  return {
    draw: draw,
    open: function () {
      was = X.classList.contains("uv");
      if (was && !X.classList.contains("oas-lit")) X.classList.add("oas-lit");     /* armed across a close */
      mo.observe(X, { attributes: true, attributeFilter: ["class"] });
    },
    close: function () { mo.disconnect(); clearTimeout(lit); }
  };
};
