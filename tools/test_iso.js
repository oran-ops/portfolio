/* Tests for src/kit/iso.js.   node tools/test_iso.js
 *
 * The expectations here were written from what the scene should look like, not from what the
 * code does — which is the only reason they are worth running. The painter's-order case
 * disagreed with the contract on its first run, and the contract was the thing that was wrong:
 * it sorted on x + y + z, so a tower at the back drew over a person in front of it.
 */
const fs = require('fs');
const g = globalThis;
eval(fs.readFileSync(__dirname + '/../src/kit/iso.js', 'utf8'));
const iso = g.iso;

let fail = 0;
function eq(a, b, m) {
  if (Math.abs(a - b) > 1e-9) { console.log('  FAIL ' + m + ': ' + a + ' != ' + b); fail++; }
}
function is(got, want, m) {
  if (got !== want) { console.log('  FAIL ' + m + ': ' + got + ' != ' + want); fail++; }
  else { console.log('  ' + m + ': ' + got); }
}

console.log('projection, against the table in ARCHITECTURE.md §7:');
for (const [x, y, z, sx, sy] of
     [[0,0,0, 0,0], [1,0,0, 32,16], [0,1,0, -32,16], [1,1,0, 0,32],
      [0,0,1, 0,-16], [0,0,2, 0,-32]]) {
  const p = iso.project(x, y, z);
  eq(p.sx, sx, `(${x},${y},${z}).sx`);
  eq(p.sy, sy, `(${x},${y},${z}).sy`);
}
console.log('  six points exact');

console.log('one tile spans 64 x 32, the 2:1 ratio:');
eq(iso.project(1, 0, 0).sx - iso.project(0, 1, 0).sx, 64, 'width');
eq(iso.project(1, 1, 0).sy - iso.project(0, 0, 0).sy, 32, 'height');
console.log('  64 x 32');

console.log('one z unit lifts half a tile height:');
eq(iso.project(0, 0, 0).sy - iso.project(0, 0, 1).sy, 16, 'lift');
console.log('  16 px');

console.log('round trip, project then hit, over 1600 tiles:');
let worst = 0;
for (let x = -20; x < 20; x++) for (let y = -20; y < 20; y++) {
  const p = iso.project(x, y, 0), h = iso.hit(p.sx, p.sy);
  worst = Math.max(worst, Math.abs(h.x - x), Math.abs(h.y - y));
}
eq(worst, 0, 'worst error');
console.log('  worst error ' + worst);

console.log('painter order:');
is(iso.sort([{ n: 'far', x: 0, y: 0, z: 0 }, { n: 'near', x: 3, y: 3, z: 0 },
             { n: 'mid', x: 1, y: 1, z: 0 }, { n: 'high', x: 0, y: 0, z: 9 }])
      .map(s => s.n).join(' '),
   'far high mid near', 'x+y first, z only to break a tie');

is(iso.sort([{ n: 'top', x: 2, y: 2, z: 2 }, { n: 'bottom', x: 2, y: 2, z: 0 },
             { n: 'middle', x: 2, y: 2, z: 1 }]).map(s => s.n).join(' '),
   'bottom middle top', 'crates stacked on one tile sort by height');

is(iso.sort([{ n: 'tower', x: 0, y: 0, z: 9 }, { n: 'person', x: 3, y: 3, z: 0 }])
      .map(s => s.n).join(' '),
   'tower person', 'a tall tower behind does not cover a person in front');

is(iso.sort([{ n: 'a', x: 1, y: 0, z: 0 }, { n: 'b', x: 0, y: 1, z: 0 },
             { n: 'c', x: 2, y: -1, z: 0 }]).map(s => s.n).join(''),
   'abc', 'equal depth keeps insertion order');

console.log('');
console.log(fail ? fail + ' FAILURES' : 'iso.js — every assertion passed');
process.exit(fail ? 1 : 0);
