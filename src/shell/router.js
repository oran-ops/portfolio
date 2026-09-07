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
  var REST = { yaw: 0, pitch: 0.20, dist: 6.60 };
  var FLAT = { yaw: 0, pitch: 0.09, dist: 5.90 };
  /* IN is worked out at flight time, not written down: it aims at the raster's own centre
     and stands at the distance that fills 86% of the frame height with it, which is what
     makes the last frame of the zoom and the first frame of the folder the same picture.
     1.15 was a distance from the CASE centre, and it left the top half of the screen outside
     the frame. */
  var IN = { yaw: 0, pitch: 0.02, dist: 1.15 };
  function inKeyframe() {
    if (typeof window.__screen !== "function" || typeof window.__camFill !== "function") {
      return IN;
    }
    var s = window.__screen();
    return { yaw: 0, pitch: 0.02, dist: window.__camFill(0.86), aim: [s.x, s.y, s.z] };
  }

  function ease(t) { return t < 0.5 ? 2 * t * t : 1 - Math.pow(-2 * t + 2, 2) / 2; }

  /* THE FRAMING THAT LEAVES NO ROOM SHOWING.
     __camFill's argument is the fraction of the frame's HEIGHT the screen fills, so the 0.86
     the flight lands on leaves a band of the machine's own cream case around the picture.
     Measured at 1440x900 over a 192-point grid: at 0.86, 14.1% of the frame is case; at the
     cover framing, 0.0%. To cover the frame instead of fitting inside it, the height
     fraction has to be the viewport's aspect divided by the screen's own -- read from
     __screen(), not assumed -- and a little over, so no seam survives rounding. Below 1 the
     height is already the limiting axis (a portrait phone), and the clamp says so. */
  function coverFill() {
    var s = (typeof window.__screen === "function") ? window.__screen() : null;
    if (!s || !s.hw || !s.hh) { return window.__camFill(1.22); }
    var need = (window.innerWidth / window.innerHeight) / (s.hw / s.hh);
    return window.__camFill(Math.max(1.02, need * 1.02));
  }

  /* where the camera goes on WITH the shell fading in over it: same aim, same angle, closer. */
  function pushKeyframe() {
    var s = (typeof window.__screen === "function") ? window.__screen() : null;
    var k = { yaw: 0, pitch: 0.02, dist: coverFill() };
    if (s) { k.aim = [s.x, s.y, s.z]; }
    return k;
  }

  /* the aim travels with the camera. A keyframe without one means the case centre, which is
     where the orbit sits when nobody is flying. */
  var HOME = null;
  function aimOf(k) {
    if (k.aim) { return k.aim; }
    if (!HOME && typeof window.__camAim === "function") { HOME = window.__camAim(); }
    return HOME || [0, 0.06, 0];
  }
  function setCam(yaw, pitch, dist, aim) {
    /* THE AIM IS SET FIRST AND QUIETLY, THEN THE CAMERA DRAWS ONCE.
       Both __cam and __camAim end in frame(), so this function was rendering 55,723
       triangles twice per animation frame -- 62 draw calls where 31 will do -- on the one
       beat in the whole page where the frame budget is tightest. Identical pixels either
       way; the second draw only ever overwrote the first. */
    if (aim && typeof window.__camAim === "function") { window.__camAim(aim, true); }
    window.__cam(yaw, pitch, dist, null);
  }

  function fly(from, to, ms, then) {
    var a0 = aimOf(from), a1 = aimOf(to);
    if (typeof window.__cam !== "function" ||
        matchMedia("(prefers-reduced-motion: reduce)").matches) {
      if (typeof window.__cam === "function") { setCam(to.yaw, to.pitch, to.dist, a1); }
      then();
      return;
    }
    var t0 = performance.now();
    (function step(now) {
      var t = Math.min(1, (now - t0) / ms), k = ease(t);
      /* DISTANCE IS INTERPOLATED IN LOG, NOT LINEARLY, AND THIS IS THE ZOOM HE KEEPS
         CALLING UNSMOOTH. The leg falls from 5.90 to about 1.52 -- a 3.88x change -- and
         perceived zoom goes as the RATIO, not the difference. Interpolated linearly, the
         halfway point of the leg delivers only 34% of the perceived movement and the last
         quarter delivers the rest in a rush. In log the halfway point is 50%: the object
         grows at a constant rate, which is what a dolly does and what the eye expects.
         Same endpoints, same duration, same easing -- only the space it is eased in. */
      setCam(from.yaw + (to.yaw - from.yaw) * k,
             from.pitch + (to.pitch - from.pitch) * k,
             Math.exp(Math.log(from.dist) + (Math.log(to.dist) - Math.log(from.dist)) * k),
             [a0[0] + (a1[0] - a0[0]) * k,
              a0[1] + (a1[1] - a0[1]) * k,
              a0[2] + (a1[2] - a0[2]) * k]);
      if (t < 1) { requestAnimationFrame(step); } else { then(); }
    })(t0);
  }

  var flying = false;

  /* BEAT TWO, WHICH USED TO BE A HELD PAUSE WITH NOTHING IN IT.
     The plan has said since stage 4 that the machine straightens, THEN the folder opens, THEN
     the zoom begins -- and the middle beat was 260 ms of nothing, because swapping the CRT's
     texture mid-flight was a piece of work of its own and the note in this file said so.
     It is that piece of work. machine.js draws the screen in three states now; this steps it
     from the title through the Macintosh zoom rectangle into the folder, so what the reader
     watches during the pause is the screen opening. Oran: "make an effect during the zoom, so
     the screen passes into the folder while the reader watches."

     Stepped, not per frame: each step re-uploads a 512x512 texture, and __crt collapses any
     step it has already drawn, so this asks for about eight uploads across the beat.
     Under prefers-reduced-motion, and if rAF is not running, it lands on the end state at
     once rather than not at all. */
  function openOnScreen(ms, then) {
    if (typeof window.__crt !== "function") { then(); return; }
    if (matchMedia("(prefers-reduced-motion: reduce)").matches) {
      window.__crt("folder");
      then();
      return;
    }
    var t0 = performance.now(), done = false;
    var land = function () {
      if (done) { return; }
      done = true;
      window.__crt("folder");
      then();
    };
    setTimeout(land, ms + 120);                 /* the same deadline discipline as the flight */
    (function step(now) {
      if (done) { return; }
      var t = Math.min(1, (now - t0) / ms);
      window.__crt("open", t);
      if (t < 1) { requestAnimationFrame(step); } else { land(); }
    })(t0);
  }

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
    html.classList.add("mw-fly");          /* the cue stands down -- see .machcue in machine.css */

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
      html.classList.remove("mw-fly");
      html.classList.add("mw-on");
      if (typeof window.__shellInit === "function") { window.__shellInit(); }
      /* AND THE CAMERA DOES NOT STOP HERE, which is the whole of the fix.
         The shell fades in over 340ms; for those 340ms the machine is still visible underneath
         it, and it goes on pushing from the 86% framing to one that covers the frame. Two
         things follow. The cream border of the case -- 14.1% of the frame at the landing,
         measured -- is gone before the window is opaque, so the shell arrives over the same
         1-bit picture rather than over a band of beige. And the motion carries across the
         handover, so the two pictures dissolve instead of cutting.
         Matched to the fade, not longer: rendering the machine after the window is opaque is
         work nobody can see. */
      fly(inKeyframe(), pushKeyframe(), 340, function () { });
      /* put the machine back where it was, unseen behind the shell, so leaving it does not land
         the reader on a camera halfway inside a cathode ray tube. Oran: the machine resets its
         angle. */
      /* THE CAMERA IS NOT RESET HERE ANY MORE, AND THAT IS THE JUMP AT THE END OF THE ZOOM.
         This ran in the same frame that added mw-on. The shell fades in over 190 ms, so for
         those 190 ms the reader was watching the machine SNAP from the end of the zoom back
         to its resting angle, through a window that had not finished arriving. Oran: "there
         is a jump at the end of the zoom-in."
         The reset still has to happen -- leaving the machine on a camera parked inside a
         cathode ray tube is the fault it was written for -- so it happens in leaveShell(),
         while the shell is still covering everything. Nobody can see it there, which is the
         whole point. */
    }
    setTimeout(arrive, 1900);                   /* the flight is 480 + 440 + 620 = 1540 */

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
      openOnScreen(440, function () {           /* 2. THE FOLDER OPENS, on the screen itself */
        if (arrived) { return; }
        fly(FLAT, inKeyframe(), 620, arrive);   /* 3. and only then, the zoom */
      });
    });
  }

  function leaveShell() {
    if (!html.classList.contains("mw-on")) { return; }
    if (typeof shut === "function") { shut(); }
    /* put the machine back BEFORE uncovering it: the reset that used to run at the end of the
       flight, moved to the one moment at which it cannot be seen. */
    if (typeof window.__cam === "function") {
      window.__cam(REST.yaw, REST.pitch, REST.dist, null);
      if (typeof window.__camAim === "function") { window.__camAim(null); }
    }
    html.classList.remove("mw-on");
    wheelToPage(true);
    /* the machine goes back to showing its title, so the next reader through -- or the same
       one, coming back -- gets the whole sequence rather than a screen already open. */
    if (typeof window.__crt === "function") { window.__crt("title"); }
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
    /* AND THE SAME DOOR, FOR SOMEBODY WHO IS NOT HOLDING A MOUSE. The canvas carries
       role="button" and a name (see machine/machine.html); a thing that announces itself as a
       button has to answer Enter and Space, or it is a lie told to a screen reader. Space is
       also the page's scroll key, so it is prevented here and only here -- on the one element
       that has said it is a button. */
    cv.addEventListener("keydown", function (e) {
      if (e.key === "Enter" || e.key === " " || e.key === "Spacebar") {
        e.preventDefault();
        window.__enterMachine();
      }
    });
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
