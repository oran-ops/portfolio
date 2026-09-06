// BAKE THE CRT TEXTURE for the Blender scene, from the SAME renderer the web page uses.
//
// The camera flies into the Macintosh's glass and hands over to the 2D layer. If the texture on
// the glass and the screen the reader lands on were drawn by two different pieces of code, the
// hand-over would jump -- and the two would drift apart the first time either was edited. So
// there is one drawScreen(), in tools/screen.js, and this runs it outside a browser.
//
//   node tools/shoot_crt.js [outdir]
//
// Writes mac_screen_closed.png and mac_screen_open.png at 512 x 342, the Macintosh 128K's own
// framebuffer, with the black surround a real 128K had around its raster.
"use strict";
const fs = require("fs");
const path = require("path");
const zlib = require("zlib");

const HERE = __dirname;
const REPO = path.dirname(HERE);
const OUT = process.argv[2] || "C:/Users/Alex/Desktop/Blender";

// the kit assigns to window.KIT; screen.js reads it from there
global.window = {};
new Function(fs.readFileSync(path.join(REPO, "lab", "_kit.js"), "utf8"))();
global.KIT = global.window.KIT;
const S = require("./screen.js");

const W = 512, H = 342;
// Measured on the model: the near-flat part of the tube carries 93 per cent of the image in
// 73 per cent of its height, so a picture mapped edge to edge is crushed into the curved rim.
// A 128K showed its raster inside a black surround. Putting that back is the fix and the
// more faithful thing at once.
const BX = 26, BY = 30;

function png(w, h, rgba) {
  const raw = Buffer.alloc((w * 4 + 1) * h);
  for (let y = 0; y < h; y++) {
    raw[y * (w * 4 + 1)] = 0;                       // filter: none
    rgba.copy ? 0 : 0;
    for (let x = 0; x < w * 4; x++) raw[y * (w * 4 + 1) + 1 + x] = rgba[y * w * 4 + x];
  }
  const crcTable = [];
  for (let n = 0; n < 256; n++) {
    let c = n;
    for (let k = 0; k < 8; k++) c = c & 1 ? 0xEDB88320 ^ (c >>> 1) : c >>> 1;
    crcTable[n] = c >>> 0;
  }
  const crc = b => {
    let c = 0xFFFFFFFF;
    for (const v of b) c = crcTable[(c ^ v) & 0xFF] ^ (c >>> 8);
    return (c ^ 0xFFFFFFFF) >>> 0;
  };
  const chunk = (type, data) => {
    const len = Buffer.alloc(4); len.writeUInt32BE(data.length, 0);
    const body = Buffer.concat([Buffer.from(type, "ascii"), data]);
    const c = Buffer.alloc(4); c.writeUInt32BE(crc(body), 0);
    return Buffer.concat([len, body, c]);
  };
  const ihdr = Buffer.alloc(13);
  ihdr.writeUInt32BE(w, 0); ihdr.writeUInt32BE(h, 4);
  ihdr[8] = 8; ihdr[9] = 6; ihdr[10] = 0; ihdr[11] = 0; ihdr[12] = 0;
  return Buffer.concat([
    Buffer.from([0x89, 0x50, 0x4E, 0x47, 0x0D, 0x0A, 0x1A, 0x0A]),
    chunk("IHDR", ihdr),
    chunk("IDAT", zlib.deflateSync(raw, { level: 9 })),
    chunk("IEND", Buffer.alloc(0)),
  ]);
}

function shoot(open, file) {
  const b = new S.Buf(W, H);
  S.drawScreen(b, W, H, 4, { open: open, sel: null, doc: null, opened: 0 });
  const OW = W + 2 * BX, OH = H + 2 * BY;
  const out = Buffer.alloc(OW * OH * 4);
  for (let i = 0; i < OW * OH; i++) out[i * 4 + 3] = 255;      // the surround is opaque black
  for (let y = 0; y < H; y++)
    for (let x = 0; x < W; x++)
      for (let k = 0; k < 4; k++)
        out[(((y + BY) * OW) + (x + BX)) * 4 + k] = b.d[(y * W + x) * 4 + k];
  const p = path.join(OUT, file);
  fs.writeFileSync(p, png(OW, OH, out));
  return [p, OW, OH];
}

for (const [open, file] of [[false, "mac_screen_closed.png"], [true, "mac_screen_open.png"]]) {
  const [p, w, h] = shoot(open, file);
  console.log("wrote %s  %dx%d  (%dx%d picture in a %d/%d black surround)",
              p, w, h, W, H, BX, BY);
}
