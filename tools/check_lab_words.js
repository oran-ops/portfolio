// NOT ONE WORD CHANGES -- the check, for lab/xtix-build.html.
//
// Oran's rule for every redesign of the documents: the text does not change in any way. This reads
// every string a reader can see in the prototype's <main> -- text nodes and pseudo-element content,
// in the finished state with the lamp armed -- and requires each one to appear VERBATIM in the
// file's own text: src/doc/xtix.html, the XTIX lamp zones in src/shell/frame.js, the lamp plate and
// its signature. A string that is not found is printed, and the run exits 1.
//
// Its first run found five: two strings joined with a dot, a "/10" beside the counter, a "FIG. 01"
// numeral from the previous plan, and "0.0M", the first frame of a count-up. All five were removed.
//
//   python -m http.server 8765        (from the repo root)
//   node tools/check_lab_words.js
const { chromium } = require(process.env.PLAYWRIGHT || 'playwright');
const fs = require('fs');
const decode = s => s.replace(/&middot;/g, '·').replace(/&mdash;/g, '—').replace(/&ndash;/g, '–').replace(/&amp;/g, '&')
  .replace(/&#8709;/g, '∅').replace(/&#8594;/g, '→').replace(/&empty;/g, '∅').replace(/&rarr;/g, '→').replace(/&rsquo;/g, '’')
  .replace(/&#9656;/g, '▸').replace(/&#10003;/g, '✓').replace(/&nbsp;/g, ' ').replace(/\\u00B7|\\u00b7/g, '·').replace(/\\u2014/g, '—');
const norm = s => decode(s).replace(/<[^>]+>/g, '').replace(/\s+/g, ' ').trim();
const doc = fs.readFileSync(require('path').join(__dirname, '..', 'src/doc/xtix.html'), 'utf8');
const fj = fs.readFileSync(require('path').join(__dirname, '..', 'src/shell/frame.js'), 'utf8');
const lamp = fj.slice(fj.indexOf('var LAMPS={'), fj.indexOf('oasis:[', fj.indexOf('var LAMPS={')));
const plate = fj.slice(fj.indexOf("var OFF='PRESS TO ARM'"), fj.indexOf("var OFF='PRESS TO ARM'") + 200) + ' ' + (fj.match(/class="lampnm">([^<]+)</) || [])[1];
const sig = (fj.match(/sig\.textContent='([^']+)'/) || [])[1] || '';
const corpus = norm([doc.replace(/<svg[\s\S]*?<\/svg>/g, m => m.replace(/<text[^>]*>([^<]*)<\/text>/g, ' $1 ')), lamp, plate, sig].join(' \n '));
(async () => {
  const b = await chromium.launch();
  const p = await b.newPage({ viewport: { width: 1440, height: 900 } });
  await p.goto('http://localhost:8765/lab/xtix-build.html', { waitUntil: 'load' });
  // the finished state, lamp armed, every developed note laid out
  await p.evaluate(() => { window.__build.apply(10, true); });
  await p.waitForTimeout(300);
  await p.click('#lamp'); await p.waitForTimeout(300);
  const runs = await p.evaluate(() => {
    const out = []; const w = document.createTreeWalker(document.querySelector('main'), NodeFilter.SHOW_TEXT);
    let n; while ((n = w.nextNode())) { const t = n.data.replace(/\s+/g, ' ').trim(); if (t) out.push(t); }
    // pseudo-element text too (bar numerals, the ∅ slots)
    document.querySelectorAll('main *').forEach(e => ['::before', '::after'].forEach(ps => { const c = getComputedStyle(e, ps).content; if (c && c !== 'none' && c !== 'normal' && c !== '""') { const v = c.startsWith('attr(') ? '' : c.replace(/^"|"$/g, ''); const a = c === 'attr(data-n)' ? e.dataset.n : v; if (a && a.trim()) out.push('[pseudo] ' + a); } }));
    return out;
  });
  const bad = [], ok = [];
  for (const r of runs) {
    const t = r.replace(/^\[pseudo\] /, '');
    (corpus.includes(t) ? ok : bad).push(r);
  }
  console.log('strings checked:', runs.length, ' found verbatim:', ok.length);
  console.log('NOT found verbatim:'); [...new Set(bad)].forEach(x => console.log('   «' + x + '»'));
  process.exitCode = bad.length ? 1 : 0;
  await b.close();
})();
