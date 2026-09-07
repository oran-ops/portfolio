// GENERATED FROM tools/screen.js -- the pure renderer, shared by the browser and by
// tools/shoot_crt.js, which bakes the CRT texture for Blender. ONE renderer: the pixels
// the camera flies INTO and the pixels it lands ON cannot differ, because they are made
// by the same function.
"use strict";
var K = (typeof window !== "undefined" && window.KIT) || (typeof global !== "undefined" && global.KIT);


/* ------------------------------------------------------------------ the pixel buffer
   Everything is drawn at 1x into a plain byte array and blitted once. Nothing is drawn at a
   fractional coordinate, so nothing can land off-grid however the page is zoomed. */
function Buf(w, h) { this.w = w; this.h = h; this.d = new Uint8ClampedArray(w * h * 4); }
Buf.prototype.set = function (x, y, c) {
  x |= 0; y |= 0;
  if (x < 0 || y < 0 || x >= this.w || y >= this.h) return;
  var i = (y * this.w + x) * 4;
  this.d[i] = c[0]; this.d[i + 1] = c[1]; this.d[i + 2] = c[2]; this.d[i + 3] = 255;
};
Buf.prototype.rect = function (x0, y0, x1, y1, c) {
  for (var y = y0; y <= y1; y++) for (var x = x0; x <= x1; x++) this.set(x, y, c);
};
Buf.prototype.frame = function (x0, y0, x1, y1, c) {
  for (var x = x0; x <= x1; x++) { this.set(x, y0, c); this.set(x, y1, c); }
  for (var y = y0; y <= y1; y++) { this.set(x0, y, c); this.set(x1, y, c); }
};
Buf.prototype.hl = function (y, x0, x1, c) { for (var x = x0; x <= x1; x++) this.set(x, y, c); };
Buf.prototype.vl = function (x, y0, y1, c) { for (var y = y0; y <= y1; y++) this.set(x, y, c); };
Buf.prototype.invert = function (x0, y0, x1, y1) {
  for (var y = Math.max(0, y0); y <= Math.min(this.h - 1, y1); y++)
    for (var x = Math.max(0, x0); x <= Math.min(this.w - 1, x1); x++) {
      var i = (y * this.w + x) * 4;
      this.d[i] = 255 - this.d[i]; this.d[i + 1] = 255 - this.d[i + 1];
      this.d[i + 2] = 255 - this.d[i + 2];
    }
};

var BLACK = [0, 0, 0], WHITE = [255, 255, 255];

/* the 50 per cent checkerboard the Macintosh desktop actually was */
function dither(b, x0, y0, x1, y1) {
  for (var y = y0; y <= y1; y++)
    for (var x = x0; x <= x1; x++) b.set(x, y, ((x + y) & 1) ? WHITE : BLACK);
}

/* ------------------------------------------------------------------ the face */
function gly(ch) { return K.font[ch] || K.font["."]; }
function adv(ch) { return gly(ch)[0].length + 1; }
function tw(s) { var n = 0; for (var i = 0; i < s.length; i++) n += adv(s[i]); return n ? n - 1 : 0; }
function txt(b, s, x, y, c) {
  for (var i = 0; i < s.length; i++) {
    var g = gly(s[i]);
    for (var j = 0; j < g.length; j++)
      for (var k = 0; k < g[j].length; k++) if (g[j][k] === "1") b.set(x + k, y + j, c);
    x += adv(s[i]);
  }
  return x;
}

/* ------------------------------------------------------------------ the icons
   `dim` is the selected state. A 1-bit Finder selected by INVERTING the bitmap; on a colour
   icon that turns emerald into magenta, so System 7 dimmed inside the mask instead and left
   the inversion to the label. Oran chose colour, so the colour rule is the one that applies.
   Either way it happens inside the mask -- the white window behind the icon is untouched. */
function ico(b, name, x, y, dim) {
  var rows = K.icons[name], pal = K.colour[name], k = 1 - (dim || 0);
  for (var j = 0; j < 32; j++)
    for (var i = 0; i < 32; i++) {
      var ch = rows[j][i];
      if (ch === ".") continue;
      var c = pal[ch];
      b.set(x + i, y + j, k === 1 ? c : [c[0] * k, c[1] * k, c[2] * k]);
    }
}

/* ------------------------------------------------------------------ the window chrome
   docs/KIT_OPTIONS.md measures the System 1 title bar exactly: rows 0-18 of the bar read
   1 black / 3 white / 11 striped / 3 white / 1 black, black rules on bar rows 4,6,8,10,12,14.
   One frame is used by the desktop window and by every document (ARCHITECTURE 8.3). */
var BAR = 19;
function titlebar(b, x0, y0, x1, title, active, closebox) {
  b.rect(x0, y0, x1, y0 + BAR - 1, WHITE);
  b.hl(y0, x0, x1, BLACK);
  b.hl(y0 + 18, x0, x1, BLACK);
  if (active) for (var r = 4; r <= 14; r += 2) b.hl(y0 + r, x0 + 1, x1 - 1, BLACK);
  var t = tw(title), cx = ((x0 + x1) >> 1) - (t >> 1);
  b.rect(cx - 6, y0 + 1, cx + t + 5, y0 + 17, WHITE);       /* punched through the stripes */
  txt(b, title, cx, y0 + 6, BLACK);
  if (active && closebox) {
    b.rect(x0 + 5, y0 + 1, x0 + 19, y0 + 17, WHITE);
    b.frame(x0 + 7, y0 + 4, x0 + 17, y0 + 14, BLACK);
    // System 1 drew this square EMPTY and filled it on press. Oran overrode that on
    // purpose: an empty square does not read as an exit to anyone who never used the
    // machine. Clarity beats authenticity here, and it is his call.
    for (var d = 0; d < 7; d++) {
      b.set(x0 + 9 + d, y0 + 6 + d, BLACK);
      b.set(x0 + 15 - d, y0 + 6 + d, BLACK);
    }
    return [x0 + 7, y0 + 4, x0 + 17, y0 + 14];
  }
  return null;
}

/* present, but with nothing to scroll: the track is drawn and left empty, and the arrow boxes
   are drawn without their triangles. In 1-bit there is no greying -- the absence IS the state. */
function scrollbars(b, x0, y0, x1, y1) {
  var S = 15;
  b.rect(x1 - S + 1, y0, x1, y1, WHITE);
  b.rect(x0, y1 - S + 1, x1, y1, WHITE);
  b.vl(x1 - S, y0, y1, BLACK);
  b.hl(y1 - S, x0, x1, BLACK);
  b.hl(y0 + S, x1 - S, x1, BLACK);
  b.hl(y1 - 2 * S, x1 - S, x1, BLACK);
  b.vl(x0 + S, y1 - S, y1, BLACK);
  b.vl(x1 - 2 * S, y1 - S, y1, BLACK);
}

/* ------------------------------------------------------------------ the screen */
var MENU = 20;
var MENUS = ["File", "Edit", "View", "Special"];
/* the 1977 Apple mark is Apple's. This is a lozenge, which is ours. */
function mark(b, x, y) {
  for (var j = 0; j < 9; j++) for (var i = 0; i < 9; i++)
    if (Math.abs(i - 4) + Math.abs(j - 4) <= 4) b.set(x + i, y + j, BLACK);
  b.set(x + 4, y + 4, WHITE); b.set(x + 3, y + 4, WHITE); b.set(x + 5, y + 4, WHITE);
  b.set(x + 4, y + 3, WHITE); b.set(x + 4, y + 5, WHITE);
}

function menubar(b, W) {
  b.rect(0, 0, W - 1, MENU - 1, WHITE);
  b.hl(MENU - 1, 0, W - 1, BLACK);
  mark(b, 11, 5);
  var x = 30;
  for (var i = 0; i < MENUS.length; i++) {
    if (x + tw(MENUS[i]) > W - 6) break;
    x = txt(b, MENUS[i], x, 6, BLACK) + 9;
  }
}

var LAYOUT = { inset: 10, gap: 8, labelGap: 3 };

/* A real Mac truncated rather than overlapped. Pick the longest form that fits, never both. */
function fits(opts, room) {
  for (var i = 0; i < opts.length; i++) if (tw(opts[i]) <= room) return opts[i];
  return opts[opts.length - 1];
}

/* ONE layout function. The 512x342 CRT texture and the phone are the same code with different
   arguments -- two copies of a layout drift, one cannot. Returns the hit boxes. */
function drawScreen(b, W, H, cols, st) {
  var L = LAYOUT, hits = [];
  b.rect(0, 0, W - 1, H - 1, WHITE);
  dither(b, 0, MENU, W - 1, H - 1);
  menubar(b, W);

  if (!st.open) {                                   /* the folder, shut, on the desktop */
    var fx = (W >> 1) - 16, fy = MENU + (((H - MENU) * 38 / 100) | 0);
    ico(b, "folder", fx, fy);
    var lab = K.labels.folder, lw = tw(lab), lx = (W >> 1) - (lw >> 1);
    b.rect(lx - 3, fy + 35, lx + lw + 2, fy + 44, WHITE);
    txt(b, lab, lx, fy + 36, BLACK);
    hits.push({ id: "folder", x0: fx - 4, y0: fy - 2, x1: fx + 35, y1: fy + 45 });
    return hits;
  }

  var x0 = L.inset, x1 = W - 1 - L.inset;
  var y0 = MENU + L.gap, y1 = H - 1 - L.inset;
  b.rect(x0, y0, x1, y1, WHITE);
  b.frame(x0, y0, x1, y1, BLACK);
  var title = fits([K.labels.folder, "Master File"], (x1 - x0) - 52);
  var close = titlebar(b, x0, y0, x1, title, true, true);
  if (close) hits.push({ id: "close", x0: close[0] - 2, y0: close[1] - 2, x1: close[2] + 2, y1: close[3] + 2 });

  /* the status line sits directly UNDER the title bar, as it did on a real Mac */
  var sy = y0 + BAR;
  // BOTH counts come from the icon list, so they cannot disagree with what is drawn.
  // Oran ruled seven: the Finder counted what the window held, and READ ME is a file a
  // reader opens like the rest. His word is "files".
  var N = K.order.length;
  var st1 = N + " files", st2 = st.opened + " of " + N + " opened", st3 = "2018–2026";
  var room = x1 - x0 - 30;
  txt(b, st1, x0 + 8, sy + 3, BLACK);
  if (tw(st1) + tw(st2) + tw(st3) + 34 <= room) {
    txt(b, st2, ((x0 + x1) >> 1) - (tw(st2) >> 1), sy + 3, BLACK);
    txt(b, st3, x1 - 22 - tw(st3), sy + 3, BLACK);
  } else if (tw(st1) + tw(st2) + 18 <= room) {
    txt(b, st2, x1 - 22 - tw(st2), sy + 3, BLACK);
  }
  b.hl(sy + 13, x0, x1, BLACK);

  scrollbars(b, x0, y0 + BAR, x1, y1);

  /* the icon grid, packed to the top of the window as the Finder packed it */
  var cx0 = x0 + 1, cx1 = x1 - 15, cy0 = sy + 14;
  var cw = (cx1 - cx0 + 1) / cols;
  var nrow = Math.ceil(K.order.length / cols);
  var top = cy0 + 16;
  var pitch = Math.max(66, Math.min(120, (((y1 - 15 - top - 52) / (nrow - 1)) | 0)));
  for (var i = 0; i < K.order.length; i++) {
    var id = K.order[i], r = (i / cols) | 0, c = i % cols;
    var ix = (cx0 + cw * (c + 0.5)) | 0, iy = top + r * pitch;
    var on = (st.sel === id);
    ico(b, id, ix - 16, iy, on ? 0.5 : 0);
    var lab2 = K.labels[id], lw2 = tw(lab2), lx2 = ix - (lw2 >> 1);
    b.rect(lx2 - 3, iy + 32 + L.labelGap, lx2 + lw2 + 2, iy + 42 + L.labelGap, WHITE);
    txt(b, lab2, lx2, iy + 33 + L.labelGap, BLACK);
    if (on) b.invert(lx2 - 3, iy + 32 + L.labelGap, lx2 + lw2 + 2, iy + 42 + L.labelGap);
    hits.push({ id: id, x0: ix - 20, y0: iy - 2, x1: ix + 19, y1: iy + 44 });
  }

  if (st.doc) {                                     /* a document, in the SAME frame */
    var dx0 = x0 + ((W < 300) ? 6 : 26), dx1 = x1 - ((W < 300) ? 6 : 26);
    var dy0 = y0 + ((H < 420) ? 60 : 74), dy1 = y1 - ((H < 420) ? 20 : 34);
    b.rect(dx0 + 3, dy0 + 3, dx1 + 3, dy1 + 3, BLACK);   /* the drop shadow System 1 drew */
    b.rect(dx0, dy0, dx1, dy1, WHITE);
    b.frame(dx0, dy0, dx1, dy1, BLACK);
    var dc = titlebar(b, dx0, dy0, dx1, K.labels[st.doc], true, true);
    hits.push({ id: "docclose", x0: dc[0] - 2, y0: dc[1] - 2, x1: dc[2] + 2, y1: dc[3] + 2 });
    ico(b, st.doc, dx0 + 12, dy0 + BAR + 12);
    var ty = dy0 + BAR + 16;
    txt(b, K.labels[st.doc], dx0 + 54, ty, BLACK);
    txt(b, st.opened + " of " + K.order.length + " opened", dx0 + 54, ty + 12, BLACK);
    b.hl(dy0 + BAR + 54, dx0 + 10, dx1 - 10, BLACK);
    var lines = ["The document arrives here, in this",
                 "same frame. One frame is used by the",
                 "folder and by every document."];
    for (var q = 0; q < lines.length; q++) {
      if (tw(lines[q]) > dx1 - dx0 - 24) continue;
      txt(b, lines[q], dx0 + 12, dy0 + BAR + 62 + q * 11, BLACK);
    }
  }
  return hits;
}


/* ------------------------------------------------------------------ the document window
   The folder is a raster: 512 x 342 drawn at 1x and scaled by a whole number. A DOCUMENT
   cannot be, because its content is live HTML at real sizes that has to reflow -- so the
   frame is CSS boxes and the CHROME inside them is drawn by these functions at 1x and scaled
   by the same whole number. The two constructions differ; the pixels do not. */

/* A live vertical scroll bar. `pos` and `vis` are fractions of the content: where the top of
   the view sits, and how much of the content it shows. The folder's bars are drawn empty
   because nothing scrolls; in 1-bit there is no greying, and that absence IS the state. */
function vscroll(b, x0, y0, x1, y1, pos, vis, live) {
  var W = x1 - x0 + 1, S = 15;
  b.rect(x0, y0, x1, y1, WHITE);
  b.frame(x0, y0, x1, y1, BLACK);
  var sizeTop = y1 - S + 1;                    /* the size box, always drawn inactive */
  b.hl(sizeTop, x0, x1, BLACK);
  var upB = y0 + S, dnT = sizeTop - S;
  b.hl(upB, x0, x1, BLACK);
  b.hl(dnT, x0, x1, BLACK);
  var cx = x0 + (W >> 1);
  for (var r = 0; r < 4; r++) {                /* the two arrows: apex out, base in */
    for (var d = -r; d <= r; d++) {
      b.set(cx + d, y0 + 6 + r, BLACK);        /* up:   apex at the top */
      b.set(cx + d, dnT + 9 - r, BLACK);       /* down: apex at the bottom */
    }
  }
  if (!live) return null;
  var tTop = upB + 1, tBot = dnT - 1, tH = tBot - tTop + 1;
  dither(b, x0 + 1, tTop, x1 - 1, tBot);       /* the active track was a 50% grey */
  var th = Math.max(16, Math.round(tH * Math.min(1, vis)));
  var ty = tTop + Math.round((tH - th) * Math.max(0, Math.min(1, pos)));
  b.rect(x0 + 1, ty, x1 - 1, ty + th - 1, WHITE);
  b.frame(x0 + 1, ty, x1 - 1, ty + th - 1, BLACK);
  return { trackTop: tTop, trackBot: tBot, thumbTop: ty, thumbH: th, up: upB, down: dnT };
}

/* A System 1 push button. The default button carries a second border outside the first --
   that doubled outline is how the machine said "this is what Return does". */
function pushbutton(b, x0, y0, x1, y1, label, isDefault) {
  function round(a, c, d, e, col, fill) {
    if (fill) b.rect(a, c, d, e, fill);
    b.hl(c, a + 2, d - 2, col);
    b.hl(e, a + 2, d - 2, col);
    b.vl(a, c + 2, e - 2, col);
    b.vl(d, c + 2, e - 2, col);
    b.set(a + 1, c + 1, col); b.set(d - 1, c + 1, col);
    b.set(a + 1, e - 1, col); b.set(d - 1, e - 1, col);
  }
  if (isDefault) round(x0, y0, x1, y1, BLACK, null);
  var i = isDefault ? 4 : 0;
  round(x0 + i, y0 + i, x1 - i, y1 - i, BLACK, WHITE);
  var w = tw(label);
  txt(b, label, ((x0 + x1) >> 1) - (w >> 1), ((y0 + y1) >> 1) - 3, BLACK);
}

if (typeof module !== "undefined" && module.exports)
  module.exports = { Buf: Buf, drawScreen: drawScreen, dither: dither, ico: ico,
                     txt: txt, tw: tw, BLACK: BLACK, WHITE: WHITE,
                     titlebar: titlebar, menubar: menubar, vscroll: vscroll,
                     pushbutton: pushbutton, BAR: BAR, MENU: MENU };
if (typeof window !== "undefined") {
  window.Buf = Buf; window.drawScreen = drawScreen; window.dither = dither;
  window.ico = ico; window.txt = txt; window.tw = tw;
  window.titlebar = titlebar; window.menubar = menubar; window.vscroll = vscroll;
  window.pushbutton = pushbutton; window.BAR = BAR; window.MENU = MENU;
  window.BLACK = BLACK; window.WHITE = WHITE;
  /* AND THE MACHINE'S SCREEN IS REDRAWN THE MOMENT THIS ENGINE EXISTS.
     machine.js is expanded before this file, so its first paint of the CRT necessarily used a
     fallback -- a blank white panel and an empty menu bar. It cannot know when the real drawing
     functions arrive, and a setTimeout(0) from inside it is a guess about parse order that is
     wrong often enough to matter (it was wrong here: the machine showed the fallback for the
     whole of page 3). This line is not a guess. It is the exact instant the engine is ready. */
  if (typeof window.__crt === "function") { try { window.__crt("title"); } catch (e) { } }
}
