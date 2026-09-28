# -*- coding: utf-8 -*-
"""NOT ONE WORD, AND NOT ONE POINT OUT OF PLACE -- the check for a lab XTIX page.

Oran's two rules for every redesign: the text does not change in any way, and the structure of the
page and the order of its points do not change. tools/check_lab_words.js proves the first for
lab/xtix-build.html. This proves both, for any lab XTIX page, in the finished state (built, lamp
armed, developed zones open):

  WORDS   every string a reader can see in <main> is VERBATIM in the file's own text:
          src/doc/xtix.html, the XTIX lamp zones in src/shell/frame.js, the plate and its signature.
  ORDER   the page's words, in reading order, equal the LIVE XTIX's words over the same range --
          from "CASE STUDY 01" to "COMMERCIAL OPERATING SYSTEM -- BUILT", lamp armed, as the built
          page renders them. Nothing added, dropped, moved or said twice; the lamp plate's place
          counts. Compared word by word, because the live title is split into one run per word.

Its first run on lab/xtix-build.html: WORDS 90/90, ORDER differs in 10 places -- the window set a
second time in 04, the lamp moved into 04, the tab and both developed zones dropped, the ten names
said twice. On lab/xtix-moment.html: 109/109, and the same 263 words in the same order.

  python -m http.server 8765        (from the repo root, in another terminal)
  python tools/check_lab_order.py lab/xtix-moment.html

Python Playwright driving the INSTALLED Chrome (channel="chrome"); nothing is downloaded.
"""
import io, os, re, sys, json, difflib
from playwright.sync_api import sync_playwright

REPO = os.path.dirname(os.path.dirname(os.path.abspath(__file__))).replace(chr(92), '/') + '/'
PAGE = sys.argv[1]
BASE = 'http://localhost:8765/'

def decode(s):
    for a, b in (('&middot;', '·'), ('&mdash;', '—'), ('&ndash;', '–'), ('&amp;', '&'), ('&#8709;', '∅'),
                 ('&#8594;', '→'), ('&empty;', '∅'), ('&rarr;', '→'), ('&rsquo;', '’'), ('&#9656;', '▸'),
                 ('&#10003;', '✓'), ('&nbsp;', ' ')):
        s = s.replace(a, b)
    s = s.replace(chr(92) + 'u00B7', '·').replace(chr(92) + 'u00b7', '·').replace(chr(92) + 'u2014', '—')
    return s
def norm(s): return ' '.join(re.sub(r'<[^>]+>', '', decode(s)).split())

doc = io.open(REPO + 'src/doc/xtix.html', encoding='utf-8').read()
fj = io.open(REPO + 'src/shell/frame.js', encoding='utf-8').read()
i = fj.index('var LAMPS={'); lamp = fj[i:fj.index('oasis:[', i)]
j = fj.index("var OFF='PRESS TO ARM'"); plate = fj[j:j + 200] + ' ' + re.search(r'class="lampnm">([^<]+)<', fj).group(1)
sig = re.search(r"sig\.textContent='([^']+)'", fj).group(1)
svgtext = re.sub(r'<svg[\s\S]*?</svg>', lambda m: ' '.join(re.findall(r'<text[^>]*>([^<]*)</text>', m.group(0))), doc)
CORPUS = norm(' \n '.join([svgtext, lamp, plate, sig]))

RUNS = r"""(root)=>{
  const out=[]; const w=document.createTreeWalker(root, NodeFilter.SHOW_TEXT);
  let n; while((n=w.nextNode())){
    const t=n.data.replace(/\s+/g,' ').trim(); if(!t) continue;
    let e=n.parentElement, hidden=false;
    while(e && e!==root.parentElement){ if(e.getAttribute && e.getAttribute('aria-hidden')==='true'){hidden=true;break} e=e.parentElement; }
    out.push({t, hidden});
  }
  return out;
}"""

with sync_playwright() as pw:
    b = pw.chromium.launch(channel='chrome', headless=True)
    pg = b.new_page(viewport={'width': 1440, 'height': 900})
    errs = []; pg.on('pageerror', lambda e: errs.append(str(e)))
    pg.goto((PAGE if PAGE.startswith('http') else BASE + PAGE), wait_until='load'); pg.wait_for_timeout(600)
    # the finished state, lamp armed
    if pg.evaluate("!!window.__moment"):
        pg.evaluate("window.__moment.apply(10)")
        pg.click('#lamp'); pg.wait_for_timeout(900)
    elif pg.evaluate("!!window.__build"):
        pg.evaluate("window.__build.apply(10, true)"); pg.wait_for_timeout(300)
        pg.click('#lamp'); pg.wait_for_timeout(600)
    runs = pg.evaluate(RUNS, pg.query_selector('main'))
    plate_runs = [r['t'] for r in pg.evaluate(RUNS, pg.query_selector('#lamp'))]

    # ---------------- the live XTIX, the same state
    lp = b.new_page(viewport={'width': 1440, 'height': 900})
    lp.goto(BASE + 'm/index.html?noboot=1', wait_until='load'); lp.wait_for_timeout(1500)
    lp.evaluate("window.__enterMachine()"); lp.wait_for_timeout(2800)
    lp.evaluate("show('xtix')"); lp.wait_for_timeout(900)
    lp.evaluate("document.querySelector('#xtix .lampband').click()"); lp.wait_for_timeout(900)
    # the live file counts $9M+ up from 0 when it comes into view; read it once it has landed
    for _ in range(40):
        lp.evaluate("()=>{const v=document.getElementById('view'); v.scrollTop += v.clientHeight*0.5}")
        lp.wait_for_timeout(120)
    lp.wait_for_timeout(2500)
    live = lp.evaluate(RUNS, lp.query_selector('#xtix'))
    b.close()

# ---------------- WORDS
vis = [r['t'] for r in runs]
bad = [t for t in vis if t not in CORPUS]
print('WORDS  %d strings in <main>, %d verbatim, %d NOT in the file' % (len(vis), len(vis) - len(bad), len(bad)))
for t in dict.fromkeys(bad): print('        «%s»' % t)

# ---------------- ORDER
# Compared WORD BY WORD: the live file splits its title into one run per word for its kinetic
# type, so runs are not comparable, but the sequence of words a reader meets is.
def words(seq): return ' '.join(seq).split()
def cut(ws, first, last):
    f, l = first.split(), last.split()
    a = next(i for i in range(len(ws)) if ws[i:i + len(f)] == f)
    z = max(i for i in range(len(ws)) if ws[i:i + len(l)] == l) + len(l)
    return ws[a:z]
FIRST, LAST = 'CASE STUDY 01', 'COMMERCIAL OPERATING SYSTEM — BUILT'
page_runs = [r['t'] for r in runs if not r['hidden']]   # the plate's place is part of the structure
live_w = cut(words([r['t'] for r in live if not r['hidden']]), FIRST, LAST)
page_w = cut(words(page_runs), FIRST, LAST)
sm = difflib.SequenceMatcher(a=live_w, b=page_w, autojunk=False)
hunks = [op for op in sm.get_opcodes() if op[0] != 'equal']
print('ORDER  live %d words, page %d words -> %s' % (len(live_w), len(page_w), 'IDENTICAL SEQUENCE' if not hunks else 'DIFFERS in %d places' % len(hunks)))
for tag, a1, a2, b1, b2 in hunks:
    ctx = ' '.join(live_w[max(0, a1 - 4):a1])
    print('        %-7s after "...%s"' % (tag, ctx))
    if a2 > a1: print('           live: %s' % ' '.join(live_w[a1:a2])[:300])
    if b2 > b1: print('           page: %s' % ' '.join(page_w[b1:b2])[:300])
print('PLATE  %s' % ' | '.join(plate_runs))

# ---------------- STATE and LAYOUT
# WORDS and ORDER read the finished state, and only text. A draft of the moment passed both while
# it showed 04 "WHAT I BUILT · (AFTER)" as not built for 200-590px of scroll, and the prototype
# passes WORDS while standing its list and chart side by side. So:
#   STATE   04 must never CHANGE while a reader scrolls. Every element of each of its ten items --
#           the name, the check, the mark, and their ::before/::after -- is fingerprinted (opacity,
#           colour, filter, transform, text-decoration, visibility, background, shadow, clip) at load
#           and again every 16px from top to bottom; any difference fails. That sees an absent state,
#           a strike-through, a greyed or filtered check, and a pairing accent. It runs lamp off, lamp
#           armed (by a real click, so the beam is live) and under reduced motion. The load state must
#           show every name and check at full ink, and the lab's pairing switch must be off at load.
#           (A second ruling proved the first version of STATE -- ink only, lamp off only -- could
#           not fail on pairing-on-by-default, strike-through or greyed checks. This one is built to.)
#   LAYOUT  the points stand one above the other -- each heading below the last -- and the whole of
#           04's list stands above the chart's heading: one column, never side by side.
TEN = ['Commercial Strategy', 'HubSpot CRM Infrastructure', 'Business Development Process', 'Sales Pipeline',
       'ICP Framework', 'Outbound Sequences', 'KPI Framework', 'Forecasting Structure', 'Reporting Dashboards',
       'AI-Powered Outbound Engine']
HEADS = ['THE SITUATION', 'MISSION OBJECTIVE', 'MY APPROACH', 'WHAT I BUILT · (AFTER)',
         'FROM ZERO — INFRASTRUCTURE BUILD-UP', 'PART 2 OF 2 — THE EVIDENCE']
PROBE = r"""([ten, heads])=>{
  const main=document.querySelector('main');
  function holder(t){ let best=null; const w=document.createTreeWalker(main,NodeFilter.SHOW_TEXT);
    let n; while((n=w.nextNode())){ if(n.data.replace(/\s+/g,' ').trim()===t){ best=n.parentElement; break; } } return best; }
  function ink(e){ let a=1,n=e; while(n&&n.nodeType===1){ const s=getComputedStyle(n);
      if(s.visibility==='hidden'||s.display==='none') return 0; a*=parseFloat(s.opacity); n=n.parentElement; }
    const c=(getComputedStyle(e).color.match(/[0-9.]+/g)||[]); return a*(c.length>3?parseFloat(c[3]):1); }
  const P=['opacity','color','filter','transform','textDecorationLine','visibility','backgroundImage','backgroundColor','boxShadow','clipPath','fontStyle','fontWeight'];
  function sig(e){ const out=[]; for(const x of [e,...e.querySelectorAll('*')]){ for(const ps of [null,'::before','::after']){
      const c=getComputedStyle(x,ps); if(ps && (c.content==='none'||c.content==='normal')) continue; out.push(P.map(k=>c[k]).join('|')); } }
    return out.join('~'); }
  /* the item's own row: climb from the name to the child of the element that holds all ten */
  function rowOf(e){ let x=e; while(x.parentElement && x.parentElement!==main){
      const p=x.parentElement; if(ten.filter(u=>p.textContent.includes(u)).length>=10) return x; x=p; } return x; }
  const items=ten.map(t=>{const e=holder(t); if(!e) return {t, a:-1, sig:''}; const row=rowOf(e);
    return {t, a:ink(e), sig:sig(row), r:row.getBoundingClientRect().toJSON()}});
  const checks=[]; const w=document.createTreeWalker(main,NodeFilter.SHOW_TEXT); let n;
  while((n=w.nextNode())){ if(n.data.trim()==='✓') checks.push(ink(n.parentElement)); }
  const hs=heads.map(t=>{const e=holder(t); return e?e.getBoundingClientRect().top+pageYOffset:null});
  return {items, checks, hs, pair:document.documentElement.classList.contains('pair'),
          y:pageYOffset, H:document.documentElement.scrollHeight, vh:innerHeight};
}"""
fails = []
with sync_playwright() as pw:
    b = pw.chromium.launch(channel='chrome', headless=True)
    for dev, mode in (('1440x900', 'lamp off'), ('iPhone 13', 'lamp off'), ('1440x900', 'lamp armed'),
                      ('iPhone 13', 'lamp armed'), ('1440x900', 'reduced motion')):
        opts = {'viewport': {'width': 1440, 'height': 900}} if dev == '1440x900' else dict(pw.devices[dev])
        if mode == 'reduced motion': opts = dict(opts, reduced_motion='reduce')
        ctx = b.new_context(**opts); pg = ctx.new_page()
        pg.goto((PAGE if PAGE.startswith('http') else BASE + PAGE), wait_until='load'); pg.wait_for_timeout(700)
        if mode == 'lamp armed' and pg.query_selector('#lamp'):
            pg.query_selector('#lamp').scroll_into_view_if_needed(); pg.wait_for_timeout(200)
            box = pg.query_selector('#lamp').bounding_box()
            if dev == '1440x900': pg.mouse.click(box['x'] + box['width'] / 2, box['y'] + box['height'] / 2)
            else: pg.touchscreen.tap(box['x'] + box['width'] / 2, box['y'] + box['height'] / 2)
            pg.wait_for_timeout(1500); pg.evaluate('scrollTo(0,0)'); pg.wait_for_timeout(300)
        s0 = pg.evaluate(PROBE, [TEN, HEADS])
        base = [i['sig'] for i in s0['items']]
        problems = []
        if s0['pair']: problems.append('the pairing switch is ON at load')
        # under the lamp the whole folder's ink falls back by design; the bar is lower there
        floor = 0.4 if mode == 'lamp armed' else 0.9
        lowinit = [i['t'] for i in s0['items'] if i['a'] < floor]
        if lowinit: problems.append('at load, %d of the ten names below full ink (%s...)' % (len(lowinit), lowinit[0]))
        if s0['checks'] and min(s0['checks']) < floor: problems.append('at load, check marks at ink %.2f' % min(s0['checks']))
        y, changed = 0, None
        while True:
            s = pg.evaluate(PROBE, [TEN, HEADS])
            diff = [i['t'] for i, b0 in zip(s['items'], base) if i['sig'] != b0]
            if diff and not changed: changed = (s['y'], diff)
            if s['y'] + s['vh'] >= s['H'] - 2: break
            y += 16; pg.evaluate('(y)=>scrollTo(0,y)', y); pg.wait_for_timeout(22)
        if changed: problems.append('at scrollY %d, %d of the ten changed as the reader scrolled (%s...)' % (changed[0], len(changed[1]), changed[1][0]))
        if problems: fails.append('STATE')
        print('STATE  %-9s %-14s %s' % (dev, mode, 'unchanged at every scroll position, full ink at load' if not problems else 'FAILS: ' + '; '.join(problems)))
        if mode == 'lamp off':
            pg.wait_for_timeout(1200)
            s = pg.evaluate(PROBE, [TEN, HEADS])
            tops = [h for h in s['hs'] if h is not None]
            stacked = len(tops) == len(HEADS) and all(b2 > a2 for a2, b2 in zip(tops, tops[1:]))
            rows = [i for i in s['items'] if i['a'] >= 0]
            list_bottom = max(i['r']['bottom'] + s['y'] for i in rows) if rows else None
            chart_head = s['hs'][4]
            below = list_bottom is not None and chart_head is not None and chart_head > list_bottom
            if not (stacked and below): fails.append('LAYOUT')
            print('LAYOUT %-9s %-14s %s' % (dev, '', 'one column: the six headings stacked, 04 wholly above the chart' if (stacked and below) else
                  'FAILS: headings stacked %s, chart heading below the list %s' % (stacked, below)))
        ctx.close()
    b.close()
print('ERRORS %d' % len(errs))
sys.exit(1 if (bad or hunks or fails) else 0)
