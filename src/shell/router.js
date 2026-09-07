"use strict";
/* THE ROUTER — five screens, and the Back button that walks them.
 *
 *   pages    the three scrolling pages: the statement, the philosophy, the machine
 *   machine  inside the Macintosh, looking at the folder
 *   doc      one of the seven files, open in the window
 *
 * WHAT IS ADDRESSABLE, AND WHAT IS NOT.
 *
 * Six documents carry a hash, so a link to one opens it. FINAL DOES NOT. Oran ruled that the
 * ending has no address — "המטרה שהוא יחפור במסמך על מנת לגלות אותם" — because it is meant to
 * be reached by working through the file, not by being handed a link to the contact details.
 *
 * So opening READ ME pushes a history entry with no change of URL. Back still walks out of it,
 * because history is a stack of states and only some of them happen to have addresses. This is
 * why build check 4 was rewritten one-way: every URL must resolve to a state, but a state is
 * not required to have a URL. The old two-way check would have refused to build this.
 *
 * ONE STATE OBJECT, ONE APPLY. Every path in and out goes through go() and render(), so there
 * is no second place where the shell can be turned on. The bug that costs a day in a router is
 * two code paths that both half-know how to open something.
 */
(function () {
  var DOCS = (window.KIT && window.KIT.order) ? window.KIT.order.slice() : [];
  var SILENT = "final";                     /* the one file with no address */
  var html = document.documentElement;

  var state = { screen: "pages", id: null };
  var applying = false;

  function hashFor(s) {
    if (s.screen === "machine") { return "#machine"; }
    if (s.screen === "doc" && s.id && s.id !== SILENT) { return "#" + s.id; }
    return "";                              /* pages, and the ending, carry no hash */
  }

  function stateFromHash() {
    var h = (location.hash || "").replace(/^#/, "");
    if (h === "machine") { return { screen: "machine", id: null }; }
    if (h && DOCS.indexOf(h) >= 0 && h !== SILENT) { return { screen: "doc", id: h }; }
    return { screen: "pages", id: null };
  }

  /* ---------------------------------------------------------------- rendering a state */
  /* THE CHOREOGRAPHY, IN THE ORDER ORAN SET IT.
   *
   *   "קודם המחשב מתיישר ואז התיקייה נפתחת... רק אחרי שהתיקייה נפתחה מתחיל אפקט הזום אין"
   *
   * The machine straightens. THEN the folder opens. Only then does the zoom begin. He was
   * explicit that the order is the point, so it is three beats and not one movement.
   *
   * The middle beat is a held pause rather than the folder actually opening on the CRT. The
   * screen is a texture baked from the same drawScreen() that renders the folder — that is why
   * the pixels the camera flies into and the pixels it lands on cannot drift — and swapping it
   * mid-flight means re-uploading it, which is a piece of work of its own. The beat is honoured
   * so the sequence reads correctly; what fills it is a smaller thing than it will be.
   */
  /* REST must BE the machine's resting camera and not a copy of an older one: the flight
     starts by snapping to `from`, so a stale REST makes the first frame of the entry a jump.
     These match the defaults in machine.js exactly. */
  var REST = { yaw: -0.52, pitch: 0.26, dist: 7.20 };
  var FLAT = { yaw: 0, pitch: 0.08, dist: 6.40 };
  var IN = { yaw: 0, pitch: 0.02, dist: 1.15 };

  function ease(t) { return t < 0.5 ? 2 * t * t : 1 - Math.pow(-2 * t + 2, 2) / 2; }

  function fly(from, to, ms, then) {
    if (typeof window.__cam !== "function" ||
        matchMedia("(prefers-reduced-motion: reduce)").matches) {
      if (typeof window.__cam === "function") { window.__cam(to.yaw, to.pitch, to.dist, null); }
      then();
      return;
    }
    var t0 = performance.now();
    (function step(now) {
      var t = Math.min(1, (now - t0) / ms), k = ease(t);
      window.__cam(from.yaw + (to.yaw - from.yaw) * k,
                   from.pitch + (to.pitch - from.pitch) * k,
                   from.dist + (to.dist - from.dist) * k, null);
      if (t < 1) { requestAnimationFrame(step); } else { then(); }
    })(t0);
  }

  var flying = false;

  /* THE PAGE'S WHEEL HANDLER MUST STAND DOWN INSIDE THE MACHINE.
   *
   * The scrolling pages run an inertia scroller: a window-level wheel listener, {passive:false},
   * that calls preventDefault() on every notch and drives window.scrollTo itself. Inside the
   * machine there is no window scroll -- html.mw-on is overflow:hidden -- so it went on eating
   * every wheel event and scrolling nothing, and the document window, which is a perfectly
   * ordinary overflow-y:auto box, could not be scrolled at all. Every one of the seven files
   * was frozen at its first screen. Nothing errored; the page simply did not move.
   *
   * The scroller already reads a flag for exactly this, so this is the flag and not a patch. */
  function wheelToPage(on) { window.__wheelOff = !on; }

  function enterShell(animate) {
    if (html.classList.contains("mw-on")) { return; }
    wheelToPage(false);
    if (!animate || flying || typeof window.__cam !== "function") {
      html.classList.add("mw-on");
      if (typeof window.__shellInit === "function") { window.__shellInit(); }
      return;
    }
    flying = true;

    /* AN ANIMATION MUST NEVER BE THE ONLY WAY IN.
     *
     * The flight is driven by requestAnimationFrame, and rAF does not fire in a background tab
     * or a hidden window. Measured: with the pane hidden the camera never moved and the shell
     * never opened — the reader clicks the machine and nothing happens, with no error to say
     * why. So the arrival is on a deadline, and the flight is decoration in front of it. If the
     * frames do not come, the reader still gets where they asked to go, just without the trip.
     */
    var arrived = false;
    function arrive() {
      if (arrived) { return; }
      arrived = true;
      flying = false;
      html.classList.add("mw-on");
      if (typeof window.__shellInit === "function") { window.__shellInit(); }
      /* put the machine back where it was, unseen behind the shell, so leaving it does not land
         the reader on a camera halfway inside a cathode ray tube. Oran: the machine resets its
         angle. */
      if (typeof window.__cam === "function") {
        window.__cam(REST.yaw, REST.pitch, REST.dist, null);
      }
    }
    setTimeout(arrive, 1600);                   /* the flight is 480 + 260 + 620 = 1360 */

    /* FROM WHERE THE CAMERA IS, NOT FROM WHERE IT STARTED.
       This flew from REST, and REST is only where the camera sits if the reader has not
       touched it. Turn the machine round to look at its back -- which the whole orbit exists
       to invite -- then click the screen, and the first frame SNAPPED the view back to the
       resting angle before any of the movement began. Oran: "clicking the screen produces an
       unclear jump". That jump is this line, and it fired for anyone who used the machine as
       a machine before going into it.

       Reading the camera back costs nothing -- __cam with no arguments is already the getter
       the harness uses -- and it makes the first beat what it was always described as: the
       machine STRAIGHTENING, from wherever the reader left it. */
    var now = (typeof window.__cam === "function") ? window.__cam(null, null, null, null) : null;
    var from = now ? { yaw: now[0], pitch: now[1], dist: now[2] } : REST;
    fly(from, FLAT, 480, function () {          /* 1. the machine straightens */
      if (arrived) { return; }
      setTimeout(function () {                  /* 2. the folder opens */
        if (arrived) { return; }
        fly(FLAT, IN, 620, arrive);             /* 3. and only then, the zoom */
      }, 260);
    });
  }

  function leaveShell() {
    if (!html.classList.contains("mw-on")) { return; }
    if (typeof shut === "function") { shut(); }
    html.classList.remove("mw-on");
    wheelToPage(true);
  }

  function render(s) {
    applying = true;
    try {
      if (s.screen === "pages") {
        leaveShell();
      } else {
        /* the flight belongs to the reader clicking the machine. Arriving on a link, or coming
           back with the Back button, should put them where they asked to be at once — a camera
           move they did not ask for reads as the page being slow. */
        enterShell(s.via === "click");
        if (s.screen === "doc" && s.id) {
          if (typeof show === "function") { show(s.id); }
        } else if (typeof shut === "function") {
          shut();
        }
      }
    } finally { applying = false; }
  }

  /* ---------------------------------------------------------------- moving between them */
  function go(screen, id, replace, via) {
    var next = { screen: screen, id: id || null, via: via || null };
    if (next.screen === state.screen && next.id === state.id) { return; }
    state = next;
    var url = location.pathname + location.search + hashFor(next);
    try {
      if (replace) { history.replaceState(next, "", url); }
      else { history.pushState(next, "", url); }
    } catch (e) { /* file:// and other opaque origins refuse pushState; the shell still works */ }
    render(next);
  }

  window.addEventListener("popstate", function (e) {
    var s = (e.state && e.state.screen) ? e.state : stateFromHash();
    state = { screen: s.screen, id: s.id || null };
    render(state);
  });

  /* ---------------------------------------------------------------- the doors */

  /* into the machine — page 3 calls this when the reader clicks the screen */
  window.__enterMachine = function () {
    state.via = "click";
    go("machine", null, false, "click");
  };

  /* CLICKING THE MACHINE GOES IN; DRAGGING IT DOES NOT.
   *
   * The canvas already owns pointerdown for orbiting, so a plain click listener would fire at
   * the end of every drag and throw the reader inside the machine every time they turned it
   * round to look. The distance the pointer travelled separates the two: under six pixels is a
   * click, past it the reader was orbiting and meant nothing by letting go. */
  (function () {
    var cv = document.getElementById("mach-gl");
    if (!cv) { return; }
    var x0 = 0, y0 = 0, down = false;
    cv.addEventListener("pointerdown", function (e) {
      down = true; x0 = e.clientX; y0 = e.clientY;
    }, { passive: true });
    cv.addEventListener("pointerup", function (e) {
      if (!down) { return; }
      down = false;
      var moved = Math.abs(e.clientX - x0) + Math.abs(e.clientY - y0);
      if (moved < 6) { window.__enterMachine(); }
    }, { passive: true });
    cv.addEventListener("pointercancel", function () { down = false; }, { passive: true });
  })();

  /* out of it — the folder's own close box */
  window.__mwExit = function () { go("pages", null); };

  /* a file opens. The folder calls show() directly, so this is how the router hears about it
     rather than being the thing that did it: one state object, updated from wherever the open
     actually happened. */
  window.__mwOpened = function (id) {
    if (applying) { return; }
    go("doc", id);
  };

  /* and closes, back to the folder rather than out of the machine — Oran: "חוזר לתיקייה
     כאשר לוחצים על BACK", and the X replaced BACK. */
  window.__mwClosed = function () {
    if (applying) { return; }
    if (state.screen === "doc") { go("machine", null); }
  };

  /* ---------------------------------------------------------------- arriving with a hash */
  var first = stateFromHash();
  if (first.screen !== "pages") {
    /* replace, not push: the address the reader arrived at is where they are, and Back should
       leave the site rather than walk into a state they never visited. */
    window.addEventListener("load", function () {
      setTimeout(function () { go(first.screen, first.id, true); }, 60);
    });
  } else {
    try { history.replaceState(state, "", location.pathname + location.search); } catch (e) { }
  }
})();
