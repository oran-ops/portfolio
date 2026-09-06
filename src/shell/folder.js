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
  var STORE = "ocmf.opened";
  var S = 2;                         /* logical pixel -> CSS pixel. Whole, always. */
  var canvas = null, hits = [], W = 0, H = 0;

  function loadOpened() {
    try { return JSON.parse(localStorage.getItem(STORE) || "[]") || []; }
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

  function at(e) {
    var r = canvas.getBoundingClientRect();
    var x = (e.clientX - r.left) * (W / r.width);
    var y = (e.clientY - r.top) * (H / r.height);
    for (var i = 0; i < hits.length; i++) {
      var h = hits[i];
      if (x >= h.x0 && x <= h.x1 && y >= h.y0 && y <= h.y1) { return h.id; }
    }
    return null;
  }

  /* ONE CLICK opens a document, never two. A phone cannot do two. */
  function act(id) {
    if (!id) { return; }
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
    /* the frame owns opening: it moves the section into the window, runs the reveal, starts
       the engine on the container, and records the open. */
    if (typeof show === "function") { show(id); }
  }

  window.__folderInit = function () {
    var desk = document.getElementById("desk");
    if (!desk) { return; }
    /* the frame's loose icons step aside for the folder */
    var files = document.getElementById("files");
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
