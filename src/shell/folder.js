"use strict";
/* THE FOLDER SCREEN — what the reader lands on inside the machine.
 *
 * The frame arrived from the lab drawing its seven icons loose on the dithered desk, which was
 * all that page needed in order to open a document and measure it. The folder Oran approved is
 * not that: it is a window, with a striped title bar reading "Oran Carmon — Master File", a
 * close box at the left, and a status line across the top in three columns —
 *
 *     7 files            2 of 7 opened            2018–2026
 *
 * That rendering already exists and is already approved: screen.js draws it, in one layout
 * function that serves both the 512x342 CRT texture and the screen the reader stands in front
 * of, so the pixels the camera flies into and the pixels it lands on cannot drift apart.
 *
 * So this replaces the frame's loose icons with screen.js's folder, and keeps the frame for
 * what the frame is good at: the document window. Two renderers, one each for the two things
 * the shell actually shows.
 *
 * THE COUNTER IS ALREADY SHARED. Both write "ocmf.opened" in localStorage, so the folder does
 * not need telling what was opened — it re-reads after every open and redraws.
 */
(function () {
  /* sessionStorage, NOT localStorage. The counter is not stuck -- it is REMEMBERED, and that
     is worse. Both writers kept the opened set in localStorage, which survives every visit, so
     a reader who has been through the file once arrives to a folder that already says
     "7 of 7 opened" and can never move again. Simulated a returning visitor and got exactly
     that. Oran has been testing this for days; his browser has had all seven since round two.
     A line that reads "N of 7 opened" is a progress cue for THIS read. sessionStorage is per
     tab and per visit, which is what that sentence means. */
  var STORE = "ocmf.opened";
  var MEM = (function(){
    try { window.sessionStorage.setItem("ocmf.t","1"); window.sessionStorage.removeItem("ocmf.t");
          return window.sessionStorage; }
    catch (e) { return null; }          /* private windows can refuse it; then nothing is kept */
  })();
  var S = 2;                         /* logical pixel -> CSS pixel. Whole, always. */
  var canvas = null, scroller = null, hits = [], W = 0, H = 0, cols = 4;

  function loadOpened() {
    try { return MEM ? (JSON.parse(MEM.getItem(STORE) || "[]") || []) : []; }
    catch (e) { return []; }
  }

  /* screen.js reads `opened` off this object; everything else it needs it works out itself. */
  var state = { open: true, sel: null, doc: null, opened: loadOpened().length };

  function size() {
    var desk = document.getElementById("desk");
    if (!desk) { return false; }
    var r = desk.getBoundingClientRect();
    if (r.width < 8 || r.height < 8) { return false; }
    /* SQUARE PIXELS. This was max(320, width/2) with the canvas stretched to 100% of the desk,
       so under 640 CSS px the Finder was drawn 1.17 px across and 2 px down -- every icon and
       every bitmap letter squeezed sideways. The raster is the desk halved, and draw() sizes the
       canvas to exactly W*2 x H*2, so one logical pixel is two screen pixels on both axes. */
    W = Math.max(150, Math.floor(r.width / S));
    H = Math.max(150, Math.floor(r.height / S));
    return true;
  }

  function draw() {
    if (!canvas || !size()) { return; }
    /* four columns on a wide screen, two on a narrow one. The break is not decoration: it puts
       the four case files on the first row and the notepad, the suitcase and the sealed letter
       on the second, which is the distinction between a company and everything else. */
    cols = (typeof folderCols === "function") ? folderCols(W, H) : (W < 380 ? 2 : 4);
    /* a desk too short for the grid gets the folder at the height the grid needs, and scrolls */
    if (typeof folderNeedH === "function") { H = folderNeedH(H, cols); }
    canvas.width = W * S;
    canvas.height = H * S;
    canvas.style.width = (W * S) + "px";
    canvas.style.height = (H * S) + "px";
    var b = new Buf(W, H);
    hits = drawScreen(b, W, H, cols, state);
    var off = document.createElement("canvas");
    off.width = W; off.height = H;
    var ox = off.getContext("2d");
    var im = ox.createImageData(W, H);
    im.data.set(b.d);
    ox.putImageData(im, 0, 0);
    var x = canvas.getContext("2d");
    x.imageSmoothingEnabled = false;
    x.clearRect(0, 0, canvas.width, canvas.height);
    x.drawImage(off, 0, 0, canvas.width, canvas.height);
    place();
  }

  /* ---------------------------------------------------------------- the keys
     THE MACHINE WORKS FROM A KEYBOARD. The canvas above is the only thing on the desk and it is
     aria-hidden -- rightly, it is a PICTURE of controls -- while the frame's own buttons in
     #mw-files are display:none (see __folderInit). So on this screen the whole document had
     zero focusable elements: a reader who pressed Enter on the machine arrived and could not
     open a file, could not Tab to anything, and could not Tab back out.

     One transparent button per drawn file, plus the close box, laid over the picture from the
     same hit rectangles the pointer already uses. Built once, repositioned on every draw, never
     rebuilt -- a redraw must not take focus off the button the reader is on. */
  var keys = null, btns = {}, order = [];

  function hitOf(id) {
    for (var i = 0; i < hits.length; i++) { if (hits[i].id === id) { return hits[i]; } }
    return id;
  }

  function onFocus() {
    var id = this.getAttribute("data-id");
    if (!K.labels[id]) { return; }
    /* a Macintosh showed which icon the keys were on by inverting it. Keyboard focus only: a
       programmatic focus after a mouse entry is not :focus-visible, and a folder that arrives
       with XTIX already selected is not what the reader did. */
    var kb = false;
    try { kb = this.matches(":focus-visible"); } catch (e) { }
    if (kb && state.sel !== id) { state.sel = id; draw(); }
  }

  function onKey(e) {
    /* Enter and Space open, on keydown, the way this page's other button-like controls already
       answer (the machine canvas in router.js, the ring cards on page 3). A native <button>
       does activate on its own -- but Chromium does it on the KEYPRESS, and an input path that
       delivers keydown and keyup without one (measured: exactly what an automation harness
       sends) never gets there. preventDefault stops the native activation doubling it; act()
       is guarded against re-entry regardless. */
    if (e.key === "Enter" || e.key === " " || e.key === "Spacebar") {
      e.preventDefault();
      act(hitOf(this.getAttribute("data-id")));
      return;
    }
    var step = { ArrowLeft: -1, ArrowRight: 1, ArrowUp: -cols, ArrowDown: cols }[e.key];
    if (!step || !order.length) { return; }
    e.preventDefault();
    var i = order.indexOf(this.getAttribute("data-id"));
    var j = i < 0 ? 0 : Math.max(0, Math.min(order.length - 1, i + step));
    var t = btns[order[j]];
    if (t) { t.focus(); }
  }

  function place() {
    var desk = document.getElementById("desk");
    if (!desk || !canvas) { return; }
    if (!keys) {
      keys = document.createElement("div");
      keys.className = "mw-keys";
      keys.id = "mw-keys";
      keys.setAttribute("role", "group");
      keys.setAttribute("aria-label", "Oran Carmon \u2014 Master File");
      canvas.parentNode.insertBefore(keys, canvas.nextSibling);
    }
    var r = canvas.getBoundingClientRect();
    if (!r.width || !r.height) { return; }
    /* the canvas's OWN scale. W is max(320, floor(width / 2)), so a constant 2 drifts. */
    var kx = r.width / W, ky = r.height / H;
    var seen = {};
    order = [];
    for (var i = 0; i < hits.length; i++) {
      var h = hits[i], file = !!K.labels[h.id];
      if (!file && h.id !== "close") { continue; }
      var b = btns[h.id];
      if (!b) {
        b = document.createElement("button");
        b.type = "button";
        b.className = "mw-key";
        b.setAttribute("data-id", h.id);
        b.setAttribute("aria-label", file ? "Open " + K.labels[h.id] : "Close the folder");
        b.addEventListener("click", function () { act(hitOf(this.getAttribute("data-id"))); });
        b.addEventListener("focus", onFocus);
        b.addEventListener("keydown", onKey);
        btns[h.id] = b;
        keys.appendChild(b);
      }
      seen[h.id] = true;
      var bl = h.x0 * kx, bt = h.y0 * ky, bw = (h.x1 - h.x0) * kx, bh = (h.y1 - h.y0) * ky;
      /* the close box is drawn 14 logical px square -- 28 CSS px, under a finger's 44. Its
         key grows about its centre to 44; the icons around it are well clear. */
      if (!file) {
        var gx = Math.max(0, 44 - bw) / 2, gy = Math.max(0, 44 - bh) / 2;
        bl = Math.max(0, bl - gx); bt = Math.max(0, bt - gy);
        bw = Math.max(bw, 44); bh = Math.max(bh, 44);
      }
      b.style.left = Math.round(bl) + "px";
      b.style.top = Math.round(bt) + "px";
      b.style.width = Math.round(bw) + "px";
      b.style.height = Math.round(bh) + "px";
      if (file) { order.push(h.id); }
    }
    for (var k in btns) {
      if (btns.hasOwnProperty(k) && !seen[k]) { btns[k].parentNode.removeChild(btns[k]); delete btns[k]; }
    }
  }

  /* focus is never dropped on the floor: the frame calls this when a document closes, so the
     reader is back on the file they had open rather than on <body>. */
  window.__folderFocus = function (id) {
    var b = (id && btns[id]) || btns[order[0]];
    if (!b) { return; }
    try { b.focus({ preventScroll: true }); } catch (e) { b.focus(); }
  };

  /* THE WHOLE HIT, not just its id. The rectangle screen.js returns is the only record of
     where the icon the reader clicked actually is -- the frame's own #mw-files buttons are
     display:none from __folderInit below, so they measure 0 x 0 -- and the zoom needs it to
     grow out of the right place. Callers that only want the name read .id. */
  function at(e) {
    var r = canvas.getBoundingClientRect();
    var x = (e.clientX - r.left) * (W / r.width);
    var y = (e.clientY - r.top) * (H / r.height);
    for (var i = 0; i < hits.length; i++) {
      var h = hits[i];
      if (x >= h.x0 && x <= h.x1 && y >= h.y0 && y <= h.y1) { return h; }
    }
    return null;
  }

  /* the hit box in DESK-LOCAL CSS pixels, through the canvas's own measured scale rather than
     an assumed device ratio, so it stays right if the folder is ever drawn at another size. */
  function zoomFrom(h) {
    var desk = document.getElementById("desk");
    if (!desk || !canvas || !h) { return null; }
    var r = canvas.getBoundingClientRect(), d = desk.getBoundingClientRect();
    if (!r.width || !r.height) { return null; }
    var kx = r.width / W, ky = r.height / H;
    return { l: (r.left - d.left) + h.x0 * kx,
             t: (r.top - d.top) + h.y0 * ky,
             w: (h.x1 - h.x0) * kx,
             h: (h.y1 - h.y0) * ky };
  }

  /* ONE CLICK opens a document, never two. A phone cannot do two. */
  function act(h) {
    if (!h) { return; }
    var id = h.id || h;                 /* a hit from at(), or a bare id from anywhere else */
    if (id === "close") {
      /* the folder's own close box leaves the machine entirely. The router owns what that
         means; until it exists this is simply inert rather than wrong. */
      if (typeof window.__mwExit === "function") { window.__mwExit(); }
      return;
    }
    if (id === "folder") { state.open = true; draw(); return; }
    if (id === "docclose") { if (typeof shut === "function") { shut(); } return; }
    if (!K.labels[id]) { return; }
    state.sel = id;
    /* AND THE ICON IS LIT BEFORE THE WINDOW COVERS IT. This used to set state.sel and call
       show() with no draw() between them, so the 50% dim and the inverted label that
       screen.js:201-206 already draw were not painted until __folderRedraw() ran from the
       frame's finish() -- about 216ms later, behind the window that by then covers the grid.
       The reader clicked a file and the Finder never acknowledged which one. */
    draw();
    /* and the zoom grows out of THIS icon. show() takes its start element from #mw-files,
       which __folderInit sets to display:none, so it measures 0 x 0 at the desk's corner. */
    window.__mwZoomFrom = zoomFrom(h.id ? h : null);
    /* the frame owns opening: it moves the section into the window, runs the reveal, starts
       the engine on the container, and records the open. */
    if (typeof show === "function") { show(id); }
  }

  window.__folderInit = function () {
    var desk = document.getElementById("desk");
    if (!desk) { return; }
    /* The frame's loose icons step aside for the folder.
       #mw-files, not #files: the page's own page 3 is a section called #files, and this line
       was hiding THAT — which is half of why the machine vanished on entry. */
    var files = document.getElementById("mw-files");
    if (files) { files.style.display = "none"; }
    if (!canvas) {
      canvas = document.createElement("canvas");
      canvas.className = "mw-folder";
      canvas.id = "c-folder";
      canvas.setAttribute("aria-hidden", "true");
      /* the folder and its keys live in a scroller of their own, so a folder drawn taller
         than a short desk scrolls, while the document window and the zoom -- which stay on
         the desk -- do not move with it. */
      scroller = document.createElement("div");
      scroller.className = "mw-fscroll";
      scroller.id = "mw-fscroll";
      desk.insertBefore(scroller, desk.firstChild);
      scroller.appendChild(canvas);
      canvas.addEventListener("click", function (e) { act(at(e)); });
      canvas.addEventListener("mousemove", function (e) {
        canvas.style.cursor = at(e) ? "pointer" : "default";
      });
    }
    state.opened = loadOpened().length;
    draw();
    /* and the reader lands on the first file, not on <body>. */
    window.__folderFocus(null);
  };

  /* WHAT THE FOLDER LOOKS LIKE RIGHT NOW, for the CRT the camera flies into.
     machine.js crtFolder() drew the folder on the screen with a literal `opened:0` and
     `sel:null`, while the folder the reader lands on reads the session store and keeps the file
     they last opened selected. So a reader who opened three files, stepped out and clicked back
     in watched the screen say "0 of 7 opened" for the whole zoom, then dissolve into a folder
     saying "3 of 7" with an icon suddenly inverted -- across the one handover this file's own
     header says cannot drift apart. One source now, read fresh at the moment of the click.
     (The column count is deliberately NOT shared: the CRT is cropped to its middle third on a
     phone, and two columns there would put both icons outside the visible band.) */
  window.__folderState = function () {
    return { open: true, sel: state.sel, doc: null, opened: loadOpened().length };
  };

  /* after a document is opened or shut the count has moved, so the folder is redrawn from
     storage rather than from anything this file was told. */
  window.__folderRedraw = function () {
    state.opened = loadOpened().length;
    draw();
  };

  /* THE FOLDER REDRAWS WHEN THE SCREEN CHANGES SIZE -- which it never did.
     The guard here was `mw.offsetParent !== null`, and #mw is position:fixed, whose offsetParent
     is null by specification whether or not it is on screen. frame.js found and fixed exactly
     this in its own resize handler (see the note there); this copy kept the broken test. So a
     reader who rotated a phone or resized the window on the folder screen got the old raster
     stretched over the new size -- measured at 375x812 after starting at 1440x900: a
     1440x900 canvas squeezed into 375 CSS pixels -- and, now that the folder carries keyboard
     buttons laid over its icons, those buttons would sit where the icons used to be.
     mw-on is the right question: is the shell up. A ResizeObserver on the desk covers the size
     changes no resize event reports, such as a phone's toolbar collapsing. */
  function resized() {
    if (document.documentElement.classList.contains("mw-on")) { draw(); }
  }
  window.addEventListener("resize", resized);
  if (typeof ResizeObserver === "function") {
    var deskEl = document.getElementById("desk");
    if (deskEl) { new ResizeObserver(resized).observe(deskEl); }
  }
})();
