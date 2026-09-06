/* The isometric contract. ARCHITECTURE.md §7.
 *
 *   2:1 projection, 64 x 32 px tiles, integer scales only.
 *   sx = (x - y) * 32
 *   sy = (x + y) * 16 - z * 16
 *   painter's sort on x + y + z
 *   one z unit lifts 16 px, half a tile height
 *
 * Four functions and nothing else. Every scene — the world map, the folder, the desktop — is a
 * list of placed sprites handed to these. If a fifth function ever seems necessary, the scene
 * is doing something the contract does not describe, and the contract is what should change.
 */
(function (root) {
  'use strict';

  var TW = 64, TH = 32, TZ = 16;          /* tile width, tile height, one z unit */

  function project(x, y, z) {
    return { sx: (x - y) * (TW / 2), sy: (x + y) * (TH / 2) - (z || 0) * TZ };
  }

  /* Screen back to tile, on the ground plane z = 0. Inverting the two equations:
   *   x - y = sx / 32      x + y = sy / 16
   * gives x = sx/64 + sy/32 and y = sy/32 - sx/64. Returned unrounded so a caller can decide
   * whether it wants the tile (floor) or the position within it (the fraction). */
  function hit(sx, sy) {
    var x = sx / TW + sy / TH;
    var y = sy / TH - sx / TW;
    return { x: x, y: y, tx: Math.floor(x), ty: Math.floor(y) };
  }

  /* Painter's order: x + y first, then z, then insertion order.
   *
   * NOT x + y + z, which is what the contract said until a test disagreed with it. Height does
   * not move a sprite toward the viewer, it lifts it on screen — so a tower at (0,0,9) and a
   * person at (3,3,0) score 9 and 6 under the old key, and the tower is drawn over the person
   * standing well in front of it. Under x + y they score 0 and 6, and the person is in front,
   * which is where they are.
   *
   * z survives as the tiebreaker, and it has to: two crates on the same tile differ in nothing
   * else, and the upper one must be drawn second.
   *
   * Insertion order breaks the remaining ties, which is what makes a scene reproducible — two
   * sprites on one tile at one height must not swap between frames. Array.sort is stable
   * everywhere that matters now; the index is carried anyway, because a scene that flickers on
   * one browser is not worth the bytes saved. */
  function sort(list) {
    return list.map(function (s, i) { return { s: s, i: i }; })
      .sort(function (a, b) {
        var da = a.s.x + a.s.y, db = b.s.x + b.s.y;
        if (da !== db) return da - db;
        var za = a.s.z || 0, zb = b.s.z || 0;
        return za === zb ? a.i - b.i : za - zb;
      })
      .map(function (w) { return w.s; });
  }

  /* Draw one sprite. The anchor is the bottom centre of the tile diamond, so a sprite taller
   * than its tile grows upward and a sprite wider than its tile grows sideways about that
   * point — which is what lets a building occupy one tile and still overhang its neighbours. */
  function blit(ctx, atlas, sheet, name, x, y, z) {
    var f = atlas[name];
    if (!f) throw new Error('no sprite named ' + name);
    var p = project(x, y, z);
    ctx.drawImage(sheet, f.x, f.y, f.w, f.h,
                  Math.round(p.sx - f.ax), Math.round(p.sy - f.ay), f.w, f.h);
  }

  root.iso = { TW: TW, TH: TH, TZ: TZ,
               project: project, hit: hit, sort: sort, blit: blit };
})(typeof window !== 'undefined' ? window : globalThis);
