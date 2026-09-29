/* THE XTIX MOMENT -- ported from lab/xtix-moment.html, approved by Oran on 2026-09-29:
     1. the pairing is right: bar k of the ∅→10 chart IS item k of 04's list, built in the list's order;
     2. the look (Instrument Serif / Geist / Geist Mono; "From Zero" in italic; "Only then did
        execution begin." at display size);
     3. put it on the live site -- XTIX only; the other six documents are untouched.
   Everything here is scoped to #xtix and does nothing if XTIX is not on the page. No word is
   written: this script only adds and removes classes and custom properties.

   THE BUILD. "Filled in order, ∅→10, never in one pass" -- the file's own words, in the lamp
   zone under THE SITUATION. The ten bars rise one at a time, in place, as the reader brings the
   chart up the window, ONE WAY (a bar once risen stays risen), and item k of 04's list takes the
   bar's accent while bar k rises. 04's ten are printed as the file prints them -- each under its
   check, at full ink -- before, during and after: the accent adds, it never withholds.
   Frozen states (reduced motion, ?static=1, failsafe) and the armed lamp get the chart whole. */
(function () {
  "use strict";
  var sec = document.getElementById("xtix");
  if (!sec) return;
  var body = document.body;
  var reduced = matchMedia("(prefers-reduced-motion: reduce)").matches;
  var fine = matchMedia("(pointer: fine)").matches;
  function stillNow() {
    return reduced || body.classList.contains("static") || body.classList.contains("failsafe");
  }
  /* the window's scroller when the machine is up; the page itself otherwise */
  function scroller() { return document.getElementById("view"); }
  function port() {
    var v = scroller();
    if (v && v.clientHeight) {
      var r = v.getBoundingClientRect();
      return { top: r.top, bottom: r.top + v.clientHeight, h: v.clientHeight,
               end: v.scrollTop + v.clientHeight >= v.scrollHeight - 2 };
    }
    var de = document.documentElement;
    return { top: 0, bottom: innerHeight, h: innerHeight,
             end: innerHeight + pageYOffset >= de.scrollHeight - 2 };
  }
  function shown() { return sec.classList.contains("mw-show") || !scroller(); }

  sec.classList.add("x-js");

  var bars = sec.querySelector(".xbars");
  var COLS = bars ? [].slice.call(bars.querySelectorAll(".xb")) : [];
  var list = null, ITEMS = [];
  [].forEach.call(sec.querySelectorAll(".grid2c:not(.apl)"), function (g) {
    var lg = g.querySelectorAll(".lg");
    if (lg.length === 10) { list = g; ITEMS = [].slice.call(lg); }
  });
  var folder = sec.querySelector(".folder");
  if (COLS.length !== 10 || !list || !folder) return;

  /* ---------------------------------------------------------------- the title's two words */
  function emphasise() {
    [].forEach.call(sec.querySelectorAll(".sttl .w"), function (w) {
      var t = w.textContent.replace(/\s+/g, "");
      if (t === "From" || t === "Zero") w.classList.add("x-em");
    });
  }

  /* ---------------------------------------------------------------- the build */
  var built = 0, target = 0, stepper = 0, nowTimer = 0;
  function paint(n) {
    built = n;
    for (var i = 0; i < 10; i++) {
      var now = i === n - 1;
      COLS[i].classList.toggle("on", i < n);
      COLS[i].classList.toggle("x-now", now);
      ITEMS[i].classList.toggle("x-now", now);
    }
    /* the tenth arrives with the same accent as the nine before it, and then settles */
    clearTimeout(nowTimer);
    if (n === 10) nowTimer = setTimeout(settle, 1300);
  }
  function settle() {
    clearTimeout(nowTimer);
    for (var i = 0; i < 10; i++) { COLS[i].classList.remove("x-now"); ITEMS[i].classList.remove("x-now"); }
  }
  /* NEVER IN ONE PASS, even when the reader flings past or a tall window opens with the chart
     already in view: the bars owed are paid one at a time, 90ms apart -- and a frame apart (16ms)
     while more than one is owed. At 90ms throughout, a reader scrolling faster than ~700px/s
     carried the chart off the top of the window before bar 10 rose. At 30ms, ten owed bars took
     270ms -- nearly all of the ~300ms a phone on its side keeps the chart on screen at 700px/s,
     leaving no room for a single slow frame (measured, 2026-09-29). At reading speed bars never
     queue, so this path is only ever the fast one. */
  function toward(n) {
    if (n > target) target = n;
    if (stepper || built >= target) return;
    (function step() {
      stepper = 0;
      if (built >= target) return;
      paint(built + 1);
      if (built < target) stepper = setTimeout(step, target - built > 1 ? 16 : 90);
    })();
  }
  function finish() {
    clearTimeout(stepper); stepper = 0; target = 10;
    if (built < 10) { for (var i = 0; i < 10; i++) COLS[i].classList.add("on"); built = 10; }
    settle();
  }

  /* WHEN. The build starts the moment the chart is wholly in the window and ends while its top
     is still below the upper fifth, so every bar rises in view. It also keeps item k in the
     window when bar k rises, where the geometry allows it -- where it does not (a phone on its
     side), it falls back to the chart alone: an item that is always printed built can go
     unaccented, but it can never be shown unbuilt. */
  var LEAD = 6, EDGE = 12;
  function schedule(P) {
    var vh = P.h, C = bars.getBoundingClientRect();
    /* 12px a bar at the least: a phone on its side has ~200px of chart travel, and at 18 the
       build used 164px of it, leaving no room for a quick flick (measured, 2026-09-29) */
    var d = Math.min(48, Math.max(12, (vh * 0.80 - C.height - LEAD) / 9));
    var L = list.getBoundingClientRect(), room = vh - (C.bottom - L.top) - LEAD - EDGE;
    if (room >= 0) {
      /* and a margin inside the edge: half the spare room, up to 48px. One wheel notch moves the
         page ~100px between two frames, and item k has to still be on screen when bar k rises
         after it. At 1440x900 a 12px margin let item 10 slip out under a 24px step. */
      var slack = room - Math.min(48, room / 2), di = 56;
      for (var k = 2; k <= 10; k++) di = Math.min(di, (slack + ITEMS[k - 1].getBoundingClientRect().top - L.top) / (k - 1));
      d = Math.min(d, Math.max(18, di));
    }
    return { t: P.bottom - C.bottom, d: d };
  }
  var raf = 0;
  function frame() {
    raf = 0;
    if (!sec.classList.contains("x-armed") || !shown()) return;
    var P = port(), s = schedule(P);
    var step = s.t < LEAD ? 0 : Math.min(10, 1 + Math.floor((s.t - LEAD) / s.d));
    /* the end of the document is a case of its own */
    if (step > 0 && P.end) step = 10;
    if (step > target) toward(step);
  }
  function onScroll() { if (!raf) raf = requestAnimationFrame(frame); kick(); }
  /* the bars start down only if the moment can run; otherwise the chart is printed whole */
  function arm() {
    clearTimeout(stepper); stepper = 0;
    if (stillNow() || lampLit()) { sec.classList.remove("x-armed"); finish(); return; }
    target = 0; paint(0); sec.classList.add("x-armed"); frame();
  }

  /* ---------------------------------------------------------------- $9M+ lands whole, once per opening */
  var big = sec.querySelector(".bignum"), io = null;
  function heroWatch() {
    if (!big) return;
    if (stillNow() || !("IntersectionObserver" in window)) { big.classList.add("x-in"); return; }
    if (!io) io = new IntersectionObserver(function (es) {
      es.forEach(function (e) { if (e.isIntersecting) big.classList.add("x-in"); });
    }, { threshold: 0.5 });
    io.unobserve(big); io.observe(big);          /* re-observing makes it report where it is now */
  }

  /* ---------------------------------------------------------------- THE LAMP, HELD
     The switch and the zones are the live layer's (src/_monolith.html, __em2); it still owns the
     .lampon state and the plate's words. This adds the beam. The pool is held in the WINDOW,
     like a lamp in the hand: with a mouse it follows the pointer; on a phone it stays where the
     reader last touched -- a little ABOVE the finger, so the finger does not cover what it
     finds -- while the paper scrolls under it. It has weight: 18% of the way to its aim each
     frame, and it sleeps once it has arrived. Arming it shows the finished file, since the lamp
     examines the file rather than watching it being built. A keyboard press, reduced motion,
     ?static=1 and failsafe get every developed zone plain and whole: a beam needs a pointer. */
  var clip = document.createElement("span");
  clip.className = "x-beamclip"; clip.setAttribute("aria-hidden", "true");
  clip.innerHTML = '<span class="x-beam"></span>';
  folder.appendChild(clip);
  function lampLit() { return folder.classList.contains("lampon"); }
  function zones() { return [].slice.call(folder.querySelectorAll(".devz, .lampsig")); }
  var beamOn = false, loop = 0, ax = 0, ay = 0, bx = null, by = null, sig = null;
  function aimInside() {
    var f = folder.getBoundingClientRect(), P = port();
    ax = f.left + f.width * 0.42;
    ay = Math.min(Math.max(P.top + P.h * 0.42, f.top + 150), Math.max(f.top + 150, f.bottom - 80));
  }
  function aimAtZone() {                         /* once the zones have opened: the first in view */
    if (!beamOn) return;
    var Z = zones(), P = port();
    for (var i = 0; i < Z.length; i++) {
      if (Z[i].classList.contains("lampsig")) continue;
      var z = Z[i].getBoundingClientRect();
      if (z.height && z.bottom > P.top + 60 && z.top < P.bottom - 60) {
        ax = z.left + z.width * 0.34; ay = z.top + z.height * 0.5; kick(); return;
      }
    }
  }
  function tick() {
    loop = 0;
    if (!beamOn) return;
    if (bx === null) { bx = ax; by = ay; }
    bx += (ax - bx) * 0.18; by += (ay - by) * 0.18;
    var f = folder.getBoundingClientRect(), Z = zones(), s = f.left + "," + f.top;
    folder.style.setProperty("--bx", (bx - f.left).toFixed(1) + "px");
    folder.style.setProperty("--by", (by - f.top).toFixed(1) + "px");
    for (var i = 0; i < Z.length; i++) {
      var z = Z[i].getBoundingClientRect();
      s += "," + z.left + "," + z.top;
      Z[i].style.setProperty("--mx", (bx - z.left).toFixed(1) + "px");
      Z[i].style.setProperty("--my", (by - z.top).toFixed(1) + "px");
    }
    /* asleep only when the aim is reached AND nothing under it has moved -- the zones grow
       open for 600ms after arming, and the paper scrolls */
    var rest = Math.abs(ax - bx) < 0.3 && Math.abs(ay - by) < 0.3 && s === sig;
    sig = s;
    if (!rest) loop = requestAnimationFrame(tick);
  }
  function kick() { if (beamOn && !loop) loop = requestAnimationFrame(tick); }
  function setBeam(on, plain) {
    beamOn = on && !plain;
    folder.classList.toggle("x-beamon", beamOn);
    folder.classList.toggle("x-plain", on && plain);
    cancelAnimationFrame(loop); loop = 0; sig = null;
    if (on) { sec.classList.remove("x-armed"); finish(); }
    if (!beamOn) return;
    aimInside(); bx = null;
    folder.classList.remove("x-flick"); void folder.offsetWidth; folder.classList.add("x-flick");
    setTimeout(function () { folder.classList.remove("x-flick"); }, 700);
    setTimeout(aimAtZone, 650);
    kick();
  }
  /* on the section, so it runs AFTER the plate's own listener has turned .lampon over */
  sec.addEventListener("click", function (e) {
    var b = e.target && e.target.closest ? e.target.closest(".lampband") : null;
    if (!b || !sec.contains(b)) return;
    var on = lampLit();
    setBeam(on, stillNow() || e.detail === 0);    /* detail === 0 is a keyboard press */
    if (!on) arm();
  });
  if (fine) addEventListener("pointermove", function (e) {
    if (beamOn) { ax = e.clientX; ay = e.clientY; kick(); }
  }, { passive: true });
  folder.addEventListener("pointerdown", function (e) {
    if (!beamOn) return;
    ax = e.clientX; ay = e.clientY - (e.pointerType === "touch" ? 120 : 0); kick();
  });

  /* ---------------------------------------------------------------- each opening */
  function opened() {
    emphasise();
    if (lampLit()) setBeam(true, stillNow() || folder.classList.contains("x-plain"));
    arm();
    if (big) big.classList.remove("x-in");
    heroWatch();
  }
  var was = sec.classList.contains("mw-show");
  new MutationObserver(function () {
    var now = sec.classList.contains("mw-show");
    if (now && !was) opened();
    if (!now && was) { clearTimeout(stepper); stepper = 0; cancelAnimationFrame(loop); loop = 0; }
    was = now;
  }).observe(sec, { attributes: true, attributeFilter: ["class"] });

  var hooked = null;
  function hook() {                              /* #view exists before this runs; hook it once */
    var v = scroller();
    if (v && v !== hooked) { v.addEventListener("scroll", onScroll, { passive: true }); hooked = v; }
  }
  hook();
  addEventListener("scroll", onScroll, { passive: true });
  addEventListener("resize", onScroll);
  emphasise();
  if (!scroller() || was) opened(); else { finish(); }

  /* the faces are embedded, but a face is only decoded when first used -- so they are asked
     for now, and the engines re-measure once they have arrived: a serif title and a new
     reading face move every trigger point below them */
  if (document.fonts && document.fonts.load) {
    Promise.all(["400 20px 'Instrument Serif'", "italic 400 20px 'Instrument Serif'",
                 "400 16px 'Geist'", "500 16px 'Geist'", "500 12px 'Geist Mono'"].map(function (f) {
      return document.fonts.load(f).catch(function () {});
    })).then(function () {
      if (shown() && window.__mwMeasure) window.__mwMeasure();
      onScroll();
    });
  }

  window.__xtix = { built: function () { return built; }, armed: function () { return sec.classList.contains("x-armed"); },
                    beam: function () { return beamOn; } };
})();
