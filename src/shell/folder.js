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
  var canvas = null, hits = [], W = 0, H = 0;

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
    W = Math.max(320, Math.floor(r.width / S));
    H = Math.max(200, Math.floor(r.height / S));
    return true;
  }

  function draw() {
    if (!canvas || !size()) { return; }
    /* four columns on a wide screen, two on a narrow one. The break is not decoration: it puts
       the four case files on the first row and the notepad, the suitcase and the sealed letter
       on the second, which is the distinction between a company and everything else. */
    var cols = W < 380 ? 2 : 4;
    canvas.width = W * S;
    canvas.height = H * S;
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
  }

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
      desk.insertBefore(canvas, desk.firstChild);
      canvas.addEventListener("click", function (e) { act(at(e)); });
      canvas.addEventListener("mousemove", function (e) {
        canvas.style.cursor = at(e) ? "pointer" : "default";
      });
    }
    state.opened = loadOpened().length;
    draw();
  };

  /* after a document is opened or shut the count has moved, so the folder is redrawn from
     storage rather than from anything this file was told. */
  window.__folderRedraw = function () {
    state.opened = loadOpened().length;
    draw();
  };

  window.addEventListener("resize", function () {
    var mw = document.getElementById("mw");
    if (mw && mw.offsetParent !== null) { draw(); }
  });
})();
