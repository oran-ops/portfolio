# -*- coding: utf-8 -*-
"""Lift the Macintosh out of lab/machine.html and into src/machine/, procedurally.

    python tools/extract_machine.py           report
    python tools/extract_machine.py --write   write src/machine/

THE MESH DOES NOT COME. lab/machine.html is 1,050 KB and 933 of them are one baked geometry
blob — 61,081 triangles, decoded at load. The same file builds the machine from code instead
when it is asked to: `var USE_MESH = !/[?&]geo=proc/.test(location.search)`, and that path
produces 25 parts and 23,506 triangles, measured.

So the procedural machine ships and the mesh stays in the lab. The reasons are budgets Oran
and I wrote down before either of us knew this would come up: ARCHITECTURE.md §13 allows
520 KB for the desktop machine and 60 KB for the phone. The mesh misses the desktop budget by
about 2x and the phone one by fifteen. The procedural machine fits both, and it is the same
object — a 128K, an M0110 keyboard and an M0100 mouse, measured to 246 x 344 x 276 mm.

It also settles an open question rather than dodging it. The one thing left unanswered in the
plan was whether the machine should be real-time or a pre-rendered turntable. Real-time was the
recommendation; procedural real-time is that answer at a tenth of the weight.

WHAT IS KEPT: the Caveat face, 49.6 KB, which writes the four floppy labels by hand. Losing it
would leave them in a system font, and a handwritten label is the whole point of them.

The code is already inside its own IIFE, so its 197 names cannot reach the shell's.
"""
import io
import os
import re
import sys

sys.stdout.reconfigure(encoding='utf-8', errors='replace')
HERE = os.path.dirname(os.path.abspath(__file__))
REPO = os.path.dirname(HERE)
SRC = os.path.join(REPO, 'lab', 'machine.html')
OUT = os.path.join(REPO, 'src', 'machine')

# a single-letter id is fine on a page with four elements and a poor neighbour on a page with
# two thousand, so the canvas is renamed on the way in.
CANVAS_OLD, CANVAS_NEW = 'c', 'mach-gl'


def main():
    write = '--write' in sys.argv
    s = io.open(SRC, encoding='utf-8', errors='replace').read()
    before = len(s)

    # ---- CSS: THE @font-face ONLY, and rules written here for a canvas that lives in a page.
    #
    # The lab page's stylesheet is for a page that is nothing but the machine, and it says so:
    #   html,body{margin:0;height:100%;background:var(--charcoal)}
    #   canvas{position:fixed;inset:0}
    # Shipping either would have taken the site's body and covered the whole viewport with the
    # machine. #lbl, #read and #hint are the lab's own readouts and go with them.
    raw = '\n'.join(m.group(1) for m in re.finditer(r'<style[^>]*>(.*?)</style>', s, re.S))
    face = re.findall(r'@font-face\s*\{[^}]*\}', raw, re.S)
    if len(face) != 1 or 'Caveat' not in face[0]:
        print('  REFUSED: expected exactly one @font-face for Caveat, found %d' % len(face))
        return 1
    css = (face[0] + '\n\n'
           '/* The machine sits in page 3, not over it. The lab page styled this canvas\n'
           '   position:fixed;inset:0 because there it WAS the page. */\n'
           '#mach-wrap{position:relative;width:100%;height:100%;min-height:52svh;\n'
           '  background:#191A1F;overflow:hidden}\n'
           '#mach-gl{display:block;width:100%;height:100%;cursor:grab;touch-action:none}\n'
           '#mach-gl:active{cursor:grabbing}\n'
           '.machcue{position:absolute;left:0;right:0;bottom:18px;text-align:center;\n'
           "  font-family:'JetBrains Mono',ui-monospace,monospace;font-size:10px;\n"
           '  letter-spacing:.24em;text-transform:uppercase;color:var(--emb);\n'
           '  pointer-events:none;opacity:.9}\n')

    # ---- the script: one IIFE
    i = s.index('<script')
    js = s[s.index('>', i) + 1: s.index('</script>', i)]
    if not js.lstrip().startswith('(function()'):
        print('  REFUSED: the machine is no longer a single IIFE; its 197 names would leak')
        return 1

    # ---- the mesh goes
    blobs = [m for m in re.finditer(r'[A-Za-z0-9+/]{2000,}', js)]
    if len(blobs) != 1:
        print('  REFUSED: expected exactly one geometry blob in the script, found %d' % len(blobs))
        return 1
    mesh = len(blobs[0].group(0))
    js = js[:blobs[0].start()] + js[blobs[0].end():]

    # and the flag that would have looked for it
    flag = "var USE_MESH = !/[?&]geo=proc/.test(location.search);"
    if js.count(flag) != 1:
        print('  REFUSED: the USE_MESH flag did not match')
        return 1
    js = js.replace(flag,
        "/* The mesh is not shipped — see tools/extract_machine.py. 933 KB of baked geometry\n"
        "     against a 520 KB budget, for the same object the code builds in 68 KB. This was a\n"
        "     query flag; it is now a fact, so nothing can turn it back on and find no data. */\n"
        "  var USE_MESH = false;", 1)

    # ---- the lab's readout is not shipped, so writing to it must not throw.
    #
    # Four places set read.textContent, one of them once per frame, and the FIRST of them is
    # the no-WebGL message — so on the exact machine that cannot render, the page would have
    # thrown instead of saying so. A plain object takes the assignment and discards it.
    rd = "var read=document.getElementById('read');"
    if js.count(rd) != 1:
        print('  REFUSED: the readout lookup did not match')
        return 1
    js = js.replace(rd,
        "/* the lab's on-screen readout is not shipped; the assignments are kept because one of\n"
        "     them is the no-WebGL message, and a page that cannot render should say so rather\n"
        "     than throw on the way to saying so. */\n"
        "  var read=document.getElementById('read')||{};", 1)

    # ---- the canvas gets a name that can live among two thousand elements
    if js.count("getElementById('%s')" % CANVAS_OLD) != 1:
        print('  REFUSED: the canvas lookup did not match')
        return 1
    js = js.replace("getElementById('%s')" % CANVAS_OLD,
                    "getElementById('%s')" % CANVAS_NEW, 1)
    css = re.sub(r'(^|[^-\w])#%s\b' % CANVAS_OLD, r'\1#%s' % CANVAS_NEW, css)

    # The cue is Oran's own wording, from the stage where the choreography was settled:
    # "קודם המחשב מתיישר ואז התיקייה נפתחת" — and the words on screen, "Click on the Screen".
    markup = ('<div id="mach-wrap">\n'
              '  <canvas id="%s"></canvas>\n'
              '  <div class="machcue">Click on the Screen</div>\n'
              '</div>' % CANVAS_NEW)

    print('  source            %8.1f KB' % (before / 1024.0))
    print('  mesh blob removed %8.1f KB' % (mesh / 1024.0))
    print('  ---')
    print('  CSS + Caveat      %8.1f KB' % (len(css) / 1024.0))
    print('  JS  (procedural)  %8.1f KB' % (len(js) / 1024.0))
    print('  markup            %8.1f KB' % (len(markup) / 1024.0))
    print('  total shipped     %8.1f KB   (was %.1f)' %
          ((len(css) + len(js) + len(markup)) / 1024.0, before / 1024.0))

    if write:
        if not os.path.isdir(OUT):
            os.makedirs(OUT)
        for name, body in (('machine.css', css), ('machine.html', markup), ('machine.js', js)):
            io.open(os.path.join(OUT, name), 'w', encoding='utf-8', newline='').write(body)
            print('  wrote src/machine/%s' % name)
    else:
        print('  (dry run)')
    return 0


if __name__ == '__main__':
    sys.exit(main())
