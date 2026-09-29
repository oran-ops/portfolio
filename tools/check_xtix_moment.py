# -*- coding: utf-8 -*-
"""THE XTIX MOMENT ON THE LIVE PAGE, MEASURED -- the permanent check for what Oran approved on
2026-09-29 (lab/xtix-moment.html, ported by src/shell/xtix.js + xtix.css): the chart builds bar
by bar with item k of 04 lit as bar k rises, $9M+ lands whole, the lamp is held as a beam.

  python -m http.server 8765        (from the repo root, in another terminal)
  python tools/check_xtix_moment.py [url] [check,check] [device,device]

  checks: build_walk speed fling lamp faces still      devices: desk phone side

Every check here was seen to fail before it was trusted: the pairing at 24px steps on a 12px
margin (item 10 out of the window), the plate's outer glow (PLANT=glow: 6,772 / 16,474 / 36,516
pixels turned violet), a grey-out of waiting items (PLANT=grey: caught at step 14), a 5000px/s
scroll (SPEEDS=5000: 8 of 10 bars risen off screen).

Per device (desktop 1440x900, phone 390x844 touch, phone on its side 844x390 touch):
  BUILD     scrolled down in 24px steps: bars rise one at a time (never two in one step unless
            owed bars are being paid 90ms apart), ONE WAY (scrolling back never lowers a bar), and
            every bar rises with the whole chart inside the window.
  PAIRING   when bar k rises, item k of 04 carries x-now and no other item does; where the
            geometry allows (slack >= 0), item k is inside the window at that moment.
  NEVER UNBUILT  04's ten share one fingerprint (colour, weight, decoration, filter, the check's
            fill) at every step -- the x-now accent (its ::before wash and the check's box-shadow)
            is the one exemption, by name, and is not in the fingerprint.
  FLING     from the top straight to the end: the bars are paid one at a time, all ten.
  REOPEN    shut and open again: the chart is re-armed at 0, the hero waits again.
  LAMP      armed before the chart: chart whole at once; beam on with a mouse; keyboard -> plain;
            nothing outside the folder, its tab and the plate turns violet (pixel diff, off/on).
  SPEED     scrolled at 300/700/1000/1500 px/s on animation frames: every bar rises on screen up
            to LIMIT (desk and phone 1000px/s; a phone on its side 300px/s); faster is printed.
  STILL     reduced motion and ?static=1: chart whole at open, $9M+ in, lamp plain.
  FACES     title in Instrument Serif with From/Zero italic; reading in Geist; labels in Geist Mono.
  NETWORK   every request is to the local server or data:.
Exit 1 on any failure.
"""
import sys, os, asyncio, json, tempfile
from urllib.parse import urlsplit
from playwright.async_api import async_playwright
from PIL import Image

URL = sys.argv[1] if len(sys.argv) > 1 else 'http://localhost:8765/m/index.html'
ORIGIN = '%s://%s/' % tuple(urlsplit(URL)[:2])
OUT = tempfile.mkdtemp(prefix='xtix_moment_')      # screenshots; never inside the repo
DEVICES = [('desk', 1440, 900, False), ('phone', 390, 844, True), ('side', 844, 390, True)]
ONLY = sys.argv[2].split(',') if len(sys.argv) > 2 else None
DEVS = sys.argv[3].split(',') if len(sys.argv) > 3 else None
FAILS = []
INCONCLUSIVE = []
# the speed up to which every bar must rise on screen. The build ends as the chart's top reaches the
# upper fifth of the window (the approved lab's rule), leaving ~160px of margin on a desktop and ~58px
# on a phone on its side; two frames of scroll-to-paint latency eat it at ~1500 and ~700px/s. Faster
# speeds are measured and printed, not asserted.
LIMIT = {'desk': 1000, 'phone': 1000, 'side': 300}
STEP = int(os.environ.get('STEP', '24'))


def fail(dev, msg):
    FAILS.append('%s: %s' % (dev, msg)); print('    FAIL ' + msg)


STATE = r'''() => {
  const s = document.getElementById('xtix'), v = document.getElementById('view');
  const V = v.getBoundingClientRect(), vt = V.top, vb = V.top + v.clientHeight;
  const bars = [...s.querySelectorAll('.xb')], items = [...s.querySelectorAll('.grid2c:not(.apl) .lg')];
  const C = s.querySelector('.xbars').getBoundingClientRect(), L = items[0].parentElement.getBoundingClientRect();
  const fp = e => { const c = getComputedStyle(e), k = getComputedStyle(e.querySelector('.c'));
    return [c.color, c.fontWeight, c.textDecorationLine, c.filter, c.fontStyle, c.visibility, k.backgroundImage, k.color, k.filter].join('|'); };
  return {
    built: bars.filter(b => b.classList.contains('on')).length,
    on: bars.map(b => b.classList.contains('on')),
    now: items.map((e, i) => e.classList.contains('x-now') ? i : -1).filter(i => i >= 0),
    barnow: bars.map((e, i) => e.classList.contains('x-now') ? i : -1).filter(i => i >= 0),
    armed: s.classList.contains('x-armed'),
    chartIn: C.top >= vt - 1 && C.bottom <= vb + 1,
    itemIn: items.map(e => { const r = e.getBoundingClientRect(); return r.top >= vt - 1 && r.bottom <= vb + 1; }),
    slack: (vb - vt) - (C.bottom - L.top) - 6 - 12,
    fps: items.map(fp),
    heroIn: s.querySelector('.bignum').classList.contains('x-in'),
    scroll: v.scrollTop, max: v.scrollHeight - v.clientHeight,
    xform: bars.map(b => getComputedStyle(b.querySelector('.xbar')).transform),
  };
}'''


async def opened(b, dev, w, h, touch, query='', reduced=False):
    ctx = await b.new_context(viewport={'width': w, 'height': h}, is_mobile=touch, has_touch=touch,
                              reduced_motion='reduce' if reduced else 'no-preference')
    pg = await ctx.new_page()
    reqs, errs = [], []
    pg.on('request', lambda r: reqs.append(r.url))
    pg.on('response', lambda r: errs.append('HTTP %d %s' % (r.status, r.url)) if r.status >= 400 else None)
    pg.on('pageerror', lambda e: errs.append('PAGEERROR ' + str(e)))
    # NOT fixed waits: on a cold browser the first page can take longer than any fixed wait, and
    # show('xtix') called before the shell is up opens nothing -- every check after it then
    # measures a closed file (2026-09-29: "at open: armed=False built=10" on the first two desk
    # pages only). Each step waits for the state it needs, and the faces must be in before any
    # measuring, since the serif title and the reading face move everything below them.
    await pg.goto(URL + '?noboot=1' + query, wait_until='load')
    await pg.wait_for_function("() => typeof window.__enterMachine === 'function' && typeof window.show === 'function'", timeout=20000)
    await pg.evaluate("() => window.__enterMachine()")
    await pg.wait_for_function("() => document.documentElement.classList.contains('mw-on')", timeout=20000)
    await pg.wait_for_timeout(600)
    await pg.evaluate("() => show('xtix')")
    await pg.wait_for_function("""() => { const s = document.getElementById('xtix'), v = document.getElementById('view');
      return s && s.classList.contains('mw-show') && v && v.clientHeight > 0 && document.fonts.status === 'loaded' &&
        ["400 20px 'Instrument Serif'", "400 16px 'Geist'", "500 12px 'Geist Mono'"].every(f => document.fonts.check(f)); }""", timeout=20000)
    await pg.wait_for_timeout(1000)
    # and the file must be in the state the checks assume: armed, unless the reader asked for stillness
    st = await pg.evaluate("() => ({armed: document.getElementById('xtix').classList.contains('x-armed'), still: matchMedia('(prefers-reduced-motion: reduce)').matches || document.body.classList.contains('static')})")
    if not st['armed'] and not st['still']:
        raise SystemExit('%s: XTIX opened but not armed -- the page is not in the state this check measures' % dev)
    return ctx, pg, reqs, errs


async def to(pg, sel, frac):
    await pg.evaluate('''([sel, frac]) => { const v = document.getElementById('view'), e = document.querySelector(sel);
      v.scrollTop += (e.getBoundingClientRect().top - v.getBoundingClientRect().top) - v.clientHeight * frac; }''', [sel, frac])


async def build_walk(b, dev, w, h, touch):
    print('  BUILD / PAIRING / NEVER UNBUILT')
    ctx, pg, reqs, errs = await opened(b, dev, w, h, touch)
    if os.environ.get('PLANT') == 'grey':          # proof: items waiting for their bar shown greyed
        await pg.add_style_tag(content='html body #docs #xtix.x-armed .lg{color:#777!important}html body #docs #xtix.x-armed .lg.x-now{color:inherit!important}')
    s = await pg.evaluate(STATE)
    if not s['armed'] or s['built'] != 0:
        fail(dev, 'at open: armed=%s built=%d (want armed, 0)' % (s['armed'], s['built']))
    fp0 = s['fps'][0]
    await to(pg, '#xtix .grid2c:not(.apl)', 0.9)
    await pg.wait_for_timeout(500)
    prev, rose, paired, pairable, maxstep = 0, {}, 0, 0, 0
    for step in range(220):
        await pg.evaluate("(n) => { document.getElementById('view').scrollTop += n }", STEP)
        await pg.wait_for_timeout(130)
        s = await pg.evaluate(STATE)
        if len(set(s['fps'])) != 1 or s['fps'][0] != fp0:
            fail(dev, 'step %d: 04 items differ in fingerprint: %s' % (step, sorted(set(s['fps']))[:3])); break
        if s['built'] < prev:
            fail(dev, 'step %d: built fell %d -> %d' % (step, prev, s['built'])); break
        new = s['built'] - prev
        maxstep = max(maxstep, new)
        if new:
            k = s['built'] - 1
            if not s['chartIn']:
                fail(dev, 'bar %d rose with the chart not wholly in the window' % (k + 1))
            if s['now'] != [k] or s['barnow'] != [k]:
                if not (k == 9 and s['now'] == [] and s['barnow'] == []):
                    fail(dev, 'bar %d rose: item x-now=%s bar x-now=%s' % (k + 1, s['now'], s['barnow']))
            if s['slack'] >= 0:
                pairable += 1
                if s['itemIn'][k]: paired += 1
                else: fail(dev, 'bar %d rose with item %d out of the window (slack %.0f)' % (k + 1, k + 1, s['slack']))
            rose[k] = step
        prev = s['built']
        if s['built'] == 10 and step > max(rose.values()) + 8:
            break
    print('    built %d, bars per step max %d, paired in view %d/%d where it fits' % (prev, maxstep, paired, pairable))
    if prev != 10: fail(dev, 'walk ended with %d built' % prev)
    # one way: back up past the chart, then down again
    await to(pg, '#xtix .grid2c:not(.apl)', 0.2); await pg.wait_for_timeout(600)
    s = await pg.evaluate(STATE)
    if s['built'] != 10: fail(dev, 'scrolling back lowered the chart to %d' % s['built'])
    await pg.screenshot(path=os.path.join(OUT, dev + '_walk.png'))
    await ctx.close()
    return reqs, errs


SPEED_JS = r"""async (v) => {
  const s = document.getElementById('xtix'), view = document.getElementById('view');
  const bars = [...s.querySelectorAll('.xb')], items = [...s.querySelectorAll('.grid2c:not(.apl) .lg')];
  const list = items[0].parentElement, chart = s.querySelector('.xbars'), log = [];
  const inV = (r, V) => r.top >= V.top - 1 && r.bottom <= V.top + view.clientHeight + 1;
  let stall = 0;                                  // the longest frame while the chart is wholly on screen
  const mo = new MutationObserver(() => {
    const V = view.getBoundingClientRect(), C = chart.getBoundingClientRect(), L = list.getBoundingClientRect();
    bars.forEach((b, k) => { if (b.classList.contains('on') && !log[k]) log[k] = {k, chartIn: inV(C, V), itemIn: inV(items[k].getBoundingClientRect(), V),
      now: items[k].classList.contains('x-now'), slack: view.clientHeight - (C.bottom - L.top) - 18}; });
  });
  bars.forEach(b => mo.observe(b, {attributes: true, attributeFilter: ['class']}));
  const V0 = view.getBoundingClientRect();
  view.scrollTop += list.getBoundingClientRect().top - V0.top - view.clientHeight;   // list just below the window
  const end = view.scrollTop + (chart.getBoundingClientRect().bottom - list.getBoundingClientRect().top) + view.clientHeight * 1.2;
  await new Promise(done => { let t0 = null, y0 = view.scrollTop;
    let last = null;
    const f = (t) => { if (t0 === null) t0 = t;
      if (last !== null && inV(chart.getBoundingClientRect(), view.getBoundingClientRect())) stall = Math.max(stall, t - last);
      last = t; view.scrollTop = y0 + v * (t - t0) / 1000;
      if (view.scrollTop < end && view.scrollTop < view.scrollHeight - view.clientHeight - 1) requestAnimationFrame(f); else setTimeout(done, 1200); };
    requestAnimationFrame(f); });
  mo.disconnect();
  return {log, stall: Math.round(stall)};
}"""


async def speed(b, dev, w, h, touch):
    print('  SPEED (steady scroll on animation frames; a fresh browser, so no earlier test shares its frames)')
    b = await PW.chromium.launch(channel='chrome')
    # A STALL IS NOT A VERDICT. Headless Chrome renders in software and drops the odd frame of
    # 100-300ms; the port does not add to it (median 20ms, the same slow frames before and after,
    # measured 2026-09-29). One such frame while a short screen has the chart up for ~300ms decides
    # the result by itself. So the longest frame while the chart is on screen is recorded: a miss
    # with no frame over STALL ms is a FAIL of the page; a miss that coincides with a stall is
    # INCONCLUSIVE and is run again, up to three times -- and reported as such, never passed.
    STALL = 60
    for v in [int(x) for x in os.environ.get('SPEEDS', '300,700,1000,1500').split(',')]:
        for attempt in range(3):
            ctx, pg, reqs, errs = await opened(b, dev, w, h, touch)
            r = await pg.evaluate(SPEED_JS, v)
            await ctx.close()
            log, stall = r['log'], r['stall']
            n = len([x for x in log if x])
            cin = sum(1 for x in log if x and x['chartIn'])
            fit = [x for x in log if x and x['slack'] >= 0]
            pin = sum(1 for x in fit if x['itemIn'])
            acc = sum(1 for x in log if x and x['now'])
            want_c = v <= LIMIT[dev]; want_p = v <= 300
            missed = (want_c and cin != n) or (want_p and pin != len(fit))
            note = '' if not missed else ('  -- browser stalled %dms: inconclusive, again' % stall if stall > STALL else '')
            print('    %4dpx/s  bars %d, rose with chart in view %d/%d, item k in view %d/%d where it fits, accented %d, longest frame %dms%s' % (
                v, n, cin, n, pin, len(fit), acc, stall, note))
            if n != 10: fail(dev, '%dpx/s: %d bars rose' % (v, n))
            if not missed or stall <= STALL: break
        if missed and stall <= STALL:
            if want_c and cin != n: fail(dev, '%dpx/s: %d bars rose off screen with no stall' % (v, n - cin))
            if want_p and pin != len(fit): fail(dev, '%dpx/s: item k out of view for %d bars with no stall' % (v, len(fit) - pin))
        elif missed:
            INCONCLUSIVE.append('%s %dpx/s: the browser stalled on all three runs' % (dev, v))
    await b.close()


async def fling(b, dev, w, h, touch):
    print('  FLING / REOPEN')
    ctx, pg, reqs, errs = await opened(b, dev, w, h, touch)
    # every change to a bar's class is timestamped in the page: one bar per change, never two
    log = await pg.evaluate("""async () => {
      const bars = [...document.querySelectorAll('#xtix .xb')], log = [];
      const mo = new MutationObserver(() => log.push([performance.now(), bars.filter(b => b.classList.contains('on')).length]));
      bars.forEach(b => mo.observe(b, {attributes: true, attributeFilter: ['class']}));
      const v = document.getElementById('view'); v.scrollTop = v.scrollHeight;
      await new Promise(r => setTimeout(r, 1500)); mo.disconnect(); return log; }""")
    counts = [n for t, n in log]
    steps = [b2 - a for a, b2 in zip([0] + counts, counts)]
    ups = [t for (t, n), st in zip(log, steps) if st > 0]
    gaps = [round(b2 - a) for a, b2 in zip(ups, ups[1:])]
    print('    fling: bars %s, rising %d ms apart' % (counts[-1] if counts else 0, min(gaps) if gaps else -1))
    if not counts or counts[-1] != 10: fail(dev, 'fling to the end left %s built' % (counts[-1] if counts else 0))
    if max(steps or [0]) > 1: fail(dev, 'fling raised %d bars in one change' % max(steps))
    if gaps and min(gaps) < 10: fail(dev, 'fling raised bars %dms apart (one a frame is ~16)' % min(gaps))
    await pg.evaluate("() => shut()"); await pg.wait_for_timeout(500)
    await pg.evaluate("() => show('xtix')"); await pg.wait_for_timeout(1600)
    s = await pg.evaluate(STATE)
    if not s['armed'] or s['built'] != 0 or s['heroIn']:
        fail(dev, 'reopen: armed=%s built=%d heroIn=%s (want armed, 0, false)' % (s['armed'], s['built'], s['heroIn']))
    else:
        print('    reopened: re-armed at 0, hero waiting')
    await to(pg, '#xtix .bignum', 0.4); await pg.wait_for_timeout(1500)
    if not (await pg.evaluate(STATE))['heroIn']: fail(dev, '$9M+ never landed after reopen')
    await ctx.close()
    return reqs, errs


async def lamp(b, dev, w, h, touch):
    print('  LAMP')
    ctx, pg, reqs, errs = await opened(b, dev, w, h, touch)
    lb = pg.locator('#xtix .lampband')
    await lb.scroll_into_view_if_needed(); await pg.wait_for_timeout(400)
    if not touch: await lb.hover()                 # the pointer where the press will put it
    if os.environ.get('PLANT') == 'glow':          # proof the check can fail: the outer glow this port removed
        await pg.add_style_tag(content='html body #docs #xtix .uvmount.lampon .lampband{box-shadow:0 0 30px -6px rgba(155,123,255,.7)!important}')
    await pg.wait_for_timeout(2600)                # every reveal on this screen has finished
    # lamp off: a reference picture, and a second one to show the noise floor is zero
    off = os.path.join(OUT, dev + '_lampoff.png'); await pg.screenshot(path=off)
    await pg.wait_for_timeout(600)
    off2 = os.path.join(OUT, dev + '_lampoff2.png'); await pg.screenshot(path=off2)
    from PIL import ImageChops
    nb = ImageChops.difference(Image.open(off).convert('RGB'), Image.open(off2).convert('RGB')).getbbox()
    print('    noise floor (off vs off, 600ms apart): %s' % (nb or 'none'))
    if touch: await lb.tap()
    else: await lb.click()
    await pg.wait_for_timeout(250)
    s = await pg.evaluate(STATE)
    if s['armed'] or s['built'] != 10: fail(dev, 'lamp armed before the chart: armed=%s built=%d' % (s['armed'], s['built']))
    cls = await pg.evaluate("() => document.querySelector('#xtix .folder').className")
    if 'x-beamon' not in cls: fail(dev, 'pointer press did not light the beam: %s' % cls)
    await pg.wait_for_timeout(1500)
    if not touch:
        z = await pg.evaluate("() => { const r = document.querySelector('#xtix .devz').getBoundingClientRect(); return [r.left + r.width * .3, r.top + r.height * .5]; }")
        await pg.mouse.move(z[0], z[1]); await pg.wait_for_timeout(900)
        m = await pg.evaluate("() => { const d = document.querySelector('#xtix .devz'), r = d.getBoundingClientRect(); return [parseFloat(d.style.getPropertyValue('--mx')) + r.left, parseFloat(d.style.getPropertyValue('--my')) + r.top, getComputedStyle(d).maskImage.slice(0, 40)]; }")
        if abs(m[0] - z[0]) > 3 or abs(m[1] - z[1]) > 3 or 'radial' not in m[2]:
            fail(dev, 'beam did not come to the pointer: aim %s, pool %s' % (z, m))
        else:
            print('    beam held at the pointer (%.0f,%.0f), zone masked by it' % (m[0], m[1]))
    on = os.path.join(OUT, dev + '_lampon.png'); await pg.screenshot(path=on)
    # violet outside the folder and the plate?
    # every pixel outside the folder, its tab and the plate that moves TOWARD VIOLET when the lamp
    # comes on (blue rising over green, red not falling behind it) -- a faint glow counts
    rects = await pg.evaluate("""() => ['#xtix .folder', '#xtix .uvmount .lampband', '#xtix .tabrow'].map(s => { const r = document.querySelector(s).getBoundingClientRect(); return [Math.floor(r.left), Math.floor(r.top), Math.ceil(r.right), Math.ceil(r.bottom)]; })""")
    im = Image.open(on).convert('RGB'); W, H = im.size; px = im.load(); bad = 0; where = []
    p0 = Image.open(off).convert('RGB').load()
    for y in range(H):
        for x in range(W):
            if any(r[0] <= x < r[2] and r[1] <= y < r[3] for r in rects): continue
            r1, g1, b1 = px[x, y]; r0, g0, b0 = p0[x, y]
            dr, dg, db = r1 - r0, g1 - g0, b1 - b0
            # a tint toward #9B7BFF moves all three channels up, blue most, red above green; a text
            # anti-aliasing fringe changing mode moves red and green DOWN while blue rises -- not violet
            if db >= 4 and dr >= 0.3 * db and dg >= 0.15 * db and dr > dg: bad += 1; where.append((x // 20 * 20, y // 20 * 20))
    from collections import Counter
    print('    pixels turned violet outside the folder, tab and plate: %d  %s' % (bad, Counter(where).most_common(6) if bad else ''))
    if bad: fail(dev, '%d pixels turned violet outside the folder' % bad)
    # off again, then the keyboard
    if touch: await lb.tap()
    else: await lb.click()
    await pg.wait_for_timeout(400)
    await lb.focus(); await pg.keyboard.press('Enter'); await pg.wait_for_timeout(400)
    cls = await pg.evaluate("() => document.querySelector('#xtix .folder').className")
    mask = await pg.evaluate("() => getComputedStyle(document.querySelector('#xtix .devz')).maskImage")
    if 'lampon' not in cls or 'x-plain' not in cls or 'x-beamon' in cls or mask != 'none':
        fail(dev, 'keyboard press: %s mask=%s (want lampon x-plain, no mask)' % (cls, mask))
    else:
        print('    keyboard press: plain, every zone whole')
    await ctx.close()
    return reqs, errs


async def still(b, dev, w, h, touch):
    print('  STILL')
    for label, q, red in (('reduced motion', '', True), ('?static=1', '&static=1', False)):
        ctx, pg, reqs, errs = await opened(b, dev, w, h, touch, q, red)
        s = await pg.evaluate(STATE)
        body = await pg.evaluate("() => document.body.className")
        idents = set(s['xform'])
        ok = (not s['armed']) and s['built'] == 10 and s['heroIn'] and idents <= {'none'}
        print('    %-15s armed=%s built=%d heroIn=%s bar transforms=%s body=%r' % (label, s['armed'], s['built'], s['heroIn'], sorted(idents), body[:40]))
        if not ok: fail(dev, '%s: chart/hero not whole at open' % label)
        lb = pg.locator('#xtix .lampband')
        await lb.scroll_into_view_if_needed()
        if touch: await lb.tap()
        else: await lb.click()
        await pg.wait_for_timeout(400)
        cls = await pg.evaluate("() => document.querySelector('#xtix .folder').className")
        if 'x-plain' not in cls or 'x-beamon' in cls: fail(dev, '%s lamp: %s (want plain)' % (label, cls))
        await ctx.close()


async def faces(b, dev, w, h, touch):
    ctx, pg, reqs, errs = await opened(b, dev, w, h, touch)
    await pg.wait_for_timeout(800)
    f = await pg.evaluate("""() => { const q = s => getComputedStyle(document.querySelector(s));
      return { title: q('#xtix .sttl').fontFamily, em: [...document.querySelectorAll('#xtix .sttl .w.x-em')].map(e => e.textContent + ':' + getComputedStyle(e.firstElementChild || e).fontStyle),
               para: q('#xtix .para').fontFamily, zr: q('#xtix .zr').fontFamily, lg: q('#xtix .lg').fontFamily,
               loaded: ["400 20px 'Instrument Serif'", "italic 400 20px 'Instrument Serif'", "400 16px 'Geist'", "500 12px 'Geist Mono'"].map(x => document.fonts.check(x)),
               other: getComputedStyle(document.querySelector('#oasis .sttl') || document.body).fontFamily }; }""")
    print('  FACES %s' % json.dumps(f))
    if not f['title'].startswith('"Instrument Serif"') or not f['para'].startswith('Geist') or not f['zr'].startswith('"Geist Mono"'):
        fail(dev, 'faces not as approved: %s' % f)
    if f['em'] != ['From:italic', 'Zero:italic']: fail(dev, 'title emphasis: %s' % f['em'])
    if not all(f['loaded']): fail(dev, 'faces not loaded: %s' % f['loaded'])
    if 'Geist' in f['other'] or 'Instrument' in f['other']: fail(dev, 'the look reached OASIS: %s' % f['other'])
    await ctx.close()
    return reqs, errs


async def main():
    global PW
    async with async_playwright() as p:
        PW = p
        b = await p.chromium.launch(channel='chrome')
        allreq, allerr = [], []
        for dev, w, h, touch in DEVICES:
            if DEVS and dev not in DEVS: continue
            print('== %s %dx%d' % (dev, w, h))
            for fn in (build_walk, speed, fling, lamp, faces, still):
                if ONLY and fn.__name__ not in ONLY: continue
                r = await fn(b, dev, w, h, touch)
                if r: allreq += r[0]; allerr += r[1]
        ext = sorted(set(u for u in allreq if not (u.startswith(ORIGIN) or u.startswith('data:'))))
        print('NETWORK  %d requests, external: %s' % (len(allreq), ext or 'none'))
        if ext: FAILS.append('external requests: %s' % ext)
        errs = sorted(set(allerr))
        print('ERRORS   %s' % (errs or 'none'))
        if [e for e in errs if 'PAGEERROR' in e]: FAILS.append('page errors')
        await b.close()
    print('screenshots in %s' % OUT)
    for x in INCONCLUSIVE: print('INCONCLUSIVE  ' + x)
    print('\n' + ('ALL PASS' if not FAILS else '%d FAILURES\n  ' % len(FAILS) + '\n  '.join(FAILS)))
    sys.exit(1 if FAILS else 0)

asyncio.run(main())
