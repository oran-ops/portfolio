# -*- coding: utf-8 -*-
"""Lift the Macintosh shell out of the lab template and into src/, where the real build ships it.

    python tools/extract_shell.py           report
    python tools/extract_shell.py --write   write src/shell/

tools/doc_page.html was written as a LAB PAGE: a whole document whose only job was to show
Oran the frame. It carries three things the site must not ship — a review bar with Close /
Check reveal / Check all six / Forget buttons, an engine pulse counter, and an entry point that
draws the moment the file loads. Everything else is the frame itself and comes across whole.

WHY A TOOL AND NOT AN EDIT. The frame is 32 KB of CSS and JavaScript that someone else wrote,
verified, and may revise. Hand-copying it once would fork it silently: the lab page and the
site would drift, and the first sign would be a bug in one that cannot be reproduced in the
other. This re-runs, and it asserts what it expects to find, so a template that changes shape
stops the extraction rather than producing a quiet half-copy.

WHAT CHANGES, and only this:
  - the review bar's markup, CSS and event bindings are dropped
  - note() becomes null-safe, because its target is part of the review bar
  - the entry point stops running on load and becomes window.__shellInit, so the shell draws
    when the reader enters the machine and not before. A canvas sized while its container is
    display:none measures zero and paints nothing.
"""
import io
import os
import re
import shutil
import sys

sys.stdout.reconfigure(encoding='utf-8', errors='replace')
HERE = os.path.dirname(os.path.abspath(__file__))
REPO = os.path.dirname(HERE)
# THE SOURCE IS THE BUILT LAB PAGE, NOT THE TEMPLATE.
#
# tools/doc_page.html carries four empty placeholders — /*ENGINE*/, /*REDX*/, /*RXS*/ and
# /*LIVE*/ — which build_doc.py fills by lifting the scroll engine, the redaction handler, the
# rxs lift and the whole live layer out of the page and swapping the engine's clock from the
# window to the container. Extracting the template would have produced a frame whose functions
# were all empty: the window would open, the chrome would draw, and the document inside it would
# be blank. It did exactly that on the first attempt.
#
# Lifting the same code again here would mean two implementations of a delicate substitution,
# and they would drift. So build_doc.py stays the only thing that lifts, this stays the only
# thing that strips, and the handover between them is a built file that has been verified in a
# browser.
TPL = os.path.join(REPO, 'lab', 'document.html')
OUT = os.path.join(REPO, 'src', 'shell')

# ids the frame itself provides; the shell is useless without them
FRAME_IDS = ['mw', 'c-menu', 'desk', 'files', 'win', 'c-title', 'xbtn', 'view', 'docs',
             'done', 'c-done', 'c-bar', 'zoom']
# ids that belong to the lab's review bar and must not reach the site
LAB_IDS = ['rvw-note', 'b-close', 'b-check', 'b-all', 'b-forget', 'rvw-engine']


def styles(html):
    return [(m.start(1), m.group(1))
            for m in re.finditer(r'<style[^>]*>(.*?)</style>', html, re.S)]


def main():
    write = '--write' in sys.argv
    s = io.open(TPL, encoding='utf-8').read()

    # ---- CSS: the frame's own blocks. In the built page the site's entire stylesheet sits
    # between them, ~480 KB of it, and re-including that would ship the whole thing twice.
    # Size is the discriminator because it is unambiguous: the frame's blocks are single-digit
    # kilobytes and the site's is three orders larger.
    css = []
    for _, block in styles(s):
        if len(block) > 50000:
            continue
        css.append(block)
    if len(css) < 2:
        print('  REFUSED: expected at least two frame style blocks, found %d' % len(css))
        return 1
    css = '\n'.join(css)
    before_css = len(css)
    # the review bar's own rules go
    css = re.sub(r'[^{}]*\.rvw[^{}]*\{[^{}]*\}', '', css)
    css = re.sub(r'\n{3,}', '\n\n', css)

    # THE SHELL IS NOT ON SCREEN UNTIL THE READER ENTERS THE MACHINE.
    #
    # In the lab page .mw was the whole document, so it is styled `position:fixed; inset:0;
    # background:#fff` — a white sheet over the entire viewport. Shipped as written it would
    # cover the site from the first paint. This appends after that rule, so the same
    # specificity resolves in favour of the later one, and a class on <html> lifts it.
    #
    # It is done here rather than in the monolith so that it is part of the shell's own
    # contract and comes back on every extraction, instead of being a patch someone has to
    # remember to reapply.
    if '.mw{position:fixed' not in css.replace(' ', ''):
        print('  REFUSED: .mw is not the full-viewport sheet this gate assumes')
        return 1
    css += ('\n\n/* ---- the entry gate --------------------------------------------------\n'
            '   .mw is a fixed sheet over the whole viewport. It stays out of the document\n'
            '   until the router puts the reader inside the machine. */\n'
            '.mw{display:none}\n'
            'html.mw-on .mw{display:flex}\n'
            'html.mw-on{overflow:hidden}\n'
            '\n'
            '/* Above everything the page floats. The site carries a HUD at z-index 56-99 and a\n'
            '   custom cursor at 100001-2; .mw shipped with z-index:auto and lost to all of it,\n'
            '   so the first activation drew the shell underneath the hero card. */\n'
            '.mw{z-index:100050}\n'
            '\n'
            '/* ---- and the world outside the machine closes -------------------------\n'
            '   Oran\'s ruling: the floating archive HUD lives on the three scrolling pages and\n'
            '   DISAPPEARS once the reader is inside the machine. It is the same archive fiction\n'
            '   that was cut from inside the documents, and a red ARCHIVE LIVE lamp floating over\n'
            '   a Macintosh window is the one thing that would break the illusion outright.\n'
            '\n'
            '   The circle-and-dot cursor goes with them, because inside the machine the pointer\n'
            '   is the machine\'s own. Hiding it here restores the system cursor; the Macintosh\n'
            '   arrow replaces it in its own step. */\n'
            'html.mw-on #rail,html.mw-on #pbar,html.mw-on #loglin,html.mw-on #recled,\n'
            'html.mw-on #casemeter,html.mw-on #evtag,html.mw-on #clearance,html.mw-on #idlecue,\n'
            'html.mw-on #teaser,html.mw-on #curlbl,html.mw-on #cur,html.mw-on #curR,\n'
            'html.mw-on .evdrawer,html.mw-on #dust,html.mw-on #heromq\n'
            '{display:none!important}\n'
            '\n'
            '/* the page behind is not merely covered, it is taken out of the reading order */\n'
            'html.mw-on body>.sec,html.mw-on body>#hero{visibility:hidden}\n'
            'html.mw-on .mw,html.mw-on .mw *{visibility:visible}\n'
            '\n'
            '/* ---- the folder screen ------------------------------------------------\n'
            '   screen.js draws the whole folder — menu bar, dithered ground, the window with\n'
            '   its striped title bar and the status line — into one canvas that fills the desk.\n'
            '   The frame\'s own menu bar sits above it and is hidden, because two menu bars in\n'
            '   one machine is one too many. */\n'
            '.mw-folder{position:absolute;inset:0;width:100%;height:100%;display:block;\n'
            '  image-rendering:pixelated}\n'
            'html.mw-on .mw-menu{display:none}\n'
            '\n'
            '/* The document window clears the folder\'s menu bar. --mw-gap was 16px, measured\n'
            '   from a desk that began below the frame\'s own menu element; with that element\n'
            '   hidden the desk starts at the top and the folder paints its menu bar into the\n'
            '   first 40 CSS pixels of the canvas, so the window covered 24 of them and File,\n'
            '   Edit, View and Special were cut in half. */\n'
            'html.mw-on{--mw-gap:calc(var(--mw-menu) + 16px)}\n')

    # ---- markup: the frame only, never the review bar
    a = s.index('<div class="mw"')
    b = s.index('<div class="rvw">')
    markup = s[a:b].rstrip()

    # #docs must ship EMPTY. In the built lab page it holds all seven document sections — that
    # page had nowhere else to put them. On the site the documents already exist in the page and
    # the shell adopts them into #docs on entry, so shipping them here would mean two copies of
    # every document: one adopted, one inert, both matching #xtix by id. getElementById would
    # then answer with whichever came first and the shell would drive the wrong one.
    d0 = markup.index('<div id="docs">')
    d1 = markup.index('</div>', markup.index('<!--', d0) if '<!--' in markup[d0:d0 + 200]
                      else d0 + 15)
    inner = markup[d0 + len('<div id="docs">'):d1]
    if '<section' in inner:
        depth, e = 0, d0
        for t in re.finditer(r'</?div\b', markup[d0:]):
            depth += -1 if t.group(0).startswith('</') else 1
            if depth == 0:
                e = d0 + t.end() + 1
                break
        markup = markup[:d0] + '<div id="docs"></div>' + markup[e:]
    if '<section' in markup:
        print('  REFUSED: a document section survived in the frame markup')
        return 1
    for i in FRAME_IDS:
        if 'id="%s"' % i not in markup:
            print('  REFUSED: the frame markup has no #%s' % i)
            return 1
    for i in LAB_IDS:
        if 'id="%s"' % i in markup:
            print('  REFUSED: review-bar id #%s is inside the frame markup' % i)
            return 1

    # ---- JS: the last script block
    i = s.rfind('<script>')
    js = s[i + 8: s.find('</script>', i)]
    before_js = len(js)

    # the review bar's bindings run from the Close handler to the engine pulse, inclusive
    lab_a = js.index('cv("b-close").onclick')
    lab_b = js.index('}, 500);', lab_a) + len('}, 500);')
    js = js[:lab_a] + js[lab_b:]
    # rvw-note is allowed to survive in exactly one place — inside note(), which stays and is
    # made null-safe below, because a dozen call sites report through it. Every other review-bar
    # id must be gone.
    for i_ in LAB_IDS:
        allowed = 1 if i_ == 'rvw-note' else 0
        if js.count(i_) != allowed:
            print('  REFUSED: %r appears %d times after the review-bar removal, expected %d'
                  % (i_, js.count(i_), allowed))
            return 1

    # THE LIVE LAYER IS BUILT ONCE, BY WHOEVER GETS THERE FIRST.
    #
    # In the lab the shell was the only thing on the page, so it built the layer itself. On the
    # site the page has already built it by the time the reader enters the machine, and the shell
    # adopts those very nodes — lamp, slip, note and flip already attached. Building again on top
    # produced exactly double: 24 developed zones for 12, 8 lamps for 4, 8 of everything.
    #
    # Measured, not reasoned: devz 24, evslip 8, lampband 8, an-note 8, slipflip 8.
    #
    # The page's copy is the one that ships today and is the one Oran has reviewed, so it wins;
    # the shell defers. When the documents leave the scrolling flow for good, the page will stop
    # building it and the shell's copy takes over, with no change needed here.
    lv = 'function liveLayer() {'
    if js.count(lv) != 1:
        print('  REFUSED: liveLayer() did not match')
        return 1
    js = js.replace(lv, lv + '\n  if (document.querySelector(".lampband")) { return; }', 1)

    # THE FOLDER REDRAWS AFTER EVERY OPEN AND CLOSE, because its status line carries the count
    # and the count has just moved. Both the frame and the folder read "ocmf.opened" from
    # storage, so nothing is passed between them — the folder simply re-reads.
    #
    # AND THE ROUTER HEARS ABOUT IT. The folder calls show() directly rather than going through
    # the router, which is right — the folder is the thing that opened the file. So the router
    # is told after the fact and keeps one state object, instead of there being two code paths
    # that both half-know how to open a document.
    for fn, sig, tell in (
            ('show', 'function show(id) {', 'window.__mwOpened(id)'),
            ('shut', 'function shut() {', 'window.__mwClosed()')):
        if js.count(sig) != 1:
            print('  REFUSED: %s() did not match' % fn)
            return 1
        js = js.replace(sig, sig +
                        '\n  setTimeout(function () {'
                        ' if (typeof window.__folderRedraw === "function")'
                        ' { window.__folderRedraw(); }'
                        ' if (typeof %s === "function") { %s; } }, 0);'
                        % (tell.split('(')[0], tell), 1)

    # note() targets the review bar, and is called from a dozen places
    js = js.replace('function note(s) { cv("rvw-note").innerHTML = "<em>" + s + "</em>"; }',
                    'function note(s) { var n = cv("rvw-note"); '
                    'if (n) { n.innerHTML = "<em>" + s + "</em>"; } }')
    if 'var n = cv("rvw-note")' not in js:
        print('  REFUSED: note() did not match; it must be made null-safe by hand')
        return 1

    # the entry point: drawn on demand, not on load
    tail = 'window.addEventListener("resize", relayout);\nrelayout();'
    if js.count(tail) != 1:
        print('  REFUSED: the entry point did not match')
        return 1
    js = js.replace(tail,
        '/* The shell draws when the reader enters the machine, not when the page loads. A\n'
        '   canvas sized while its container is display:none measures zero and paints nothing,\n'
        '   so drawing early would produce an empty menu bar and empty icons that never repair\n'
        '   themselves. The router calls this once the shell is on screen. */\n'
        'window.__shellInit = function () {\n'
        '  /* THE DOCUMENTS MOVE INTO THE WINDOW.\n'
        '     In the lab page they were written straight into #docs, because that page was\n'
        '     nothing but the shell. On the site they begin in the scrolling flow, and the frame\n'
        '     only marks them with .mw-show — it never fetches them, so left where they are it\n'
        '     would open an empty window over a document still sitting on the page behind it.\n'
        '     This is a move, not a copy, and it is right: once the reader is inside the machine\n'
        '     there is no page left to scroll, and the finished structure has the documents\n'
        '     living in the window and nowhere else. Done once, and idempotent. */\n'
        '  var docs = cv("docs");\n'
        '  if (docs) {\n'
        '    IDS.forEach(function (id) {\n'
        '      var sec = secOf(id);\n'
        '      if (sec && sec.parentNode !== docs) { docs.appendChild(sec); }\n'
        '    });\n'
        '  }\n'
        '  relayout();\n'
        '  /* The folder is screen.js\'s window, not the frame\'s loose icons on a desk. See\n'
        '     src/shell/folder.js: the frame keeps the document window, screen.js keeps the\n'
        '     folder, and the same layout function draws the CRT texture the camera flies into. */\n'
        '  if (typeof window.__folderInit === "function") { window.__folderInit(); }\n'
        '};\n'
        'window.addEventListener("resize", function () {\n'
        '  if (cv("mw") && cv("mw").offsetParent !== null) { relayout(); }\n'
        '});')

    print('  CSS      %6d -> %6d B   (review-bar rules removed)' % (before_css, len(css)))
    print('  markup   %6d B          (#%s)' % (len(markup), ', #'.join(FRAME_IDS[:5]) + ' …'))
    print('  JS       %6d -> %6d B   (review bar out, entry gated)' % (before_js, len(js)))

    if '/*ENGINE*/' in js or '/*LIVE*/' in js:
        print('  REFUSED: the lifted code is still a placeholder — run tools/build_doc.py first')
        return 1
    kit = io.open(os.path.join(REPO, 'lab', '_kit.js'), encoding='utf-8').read()
    screen = io.open(os.path.join(HERE, 'screen.js'), encoding='utf-8').read()
    print('  kit      %6d B          generated by mac_kit.py' % len(kit))
    print('  screen   %6d B          the folder renderer' % len(screen))
    print()
    print('  total    %6.1f KB' % ((len(css) + len(markup) + len(js) + len(kit) + len(screen)) / 1024.0))

    if write:
        if not os.path.isdir(OUT):
            os.makedirs(OUT)
        for name, body in (('frame.css', css), ('frame.html', markup), ('frame.js', js),
                           ('kit.js', kit), ('screen.js', screen)):
            io.open(os.path.join(OUT, name), 'w', encoding='utf-8', newline='').write(body)
            print('  wrote src/shell/%s' % name)
    else:
        print('  (dry run)')
    return 0


if __name__ == '__main__':
    sys.exit(main())
