# STAGE 6 SAMPLE: ALL SIX DOCUMENTS INSIDE A MACINTOSH WINDOW.
#
#   python tools/build_doc.py        ->  lab/document.html
#
# READS m/index.html AND NEVER WRITES TO IT. Nothing lands in the live site without Oran's
# word, so this pulls the six sections out, applies the approved deletions, and renders them
# inside the new frame on a lab page of its own.
#
# THE GOVERNING DECISION: the documents' content does not change -- not their layout, not their
# typography, not their colours, not their wording beyond the deletions below. What changes is
# the FRAME AROUND THEM. So the site's whole stylesheet comes across untouched, the sections'
# markup comes across untouched, and the JavaScript that builds the LIVE LAYER is lifted whole
# rather than re-written. Re-writing it is how a frame-only change quietly becomes a content
# change.
#
# EVERY DELETION DECLARES HOW MANY IT EXPECTS TO FIND, per document. The six documents are not
# alike -- TECH has no folder and no punch holes at all, LEADERSHIP has holes but no
# classification band, and only XTIX and OASIS carry the (S) mark -- so a cut that silently
# matches nothing would look identical to a cut that worked. The counts below were measured
# from the file, and the build fails if the file stops matching them.
import io
import os
import re
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
REPO = os.path.dirname(HERE)
sys.path.insert(0, HERE)
import mac_kit as K

SRC = os.path.join(REPO, "m", "index.html")
TPL = os.path.join(HERE, "doc_page.html")
OUT = os.path.join(REPO, "lab", "document.html")

# id, .secnum today -> in document order, .tok rewrite, and the expected count of each cut
DOCS = [
    dict(id="xtix", old="03", new="01", tok=None,
         n=dict(otx=1, clsband=1, clsctl=1, pmark=1, frail=1, srcline=0)),
    dict(id="oasis", old="04", new="02", tok=None,
         n=dict(otx=1, clsband=1, clsctl=1, pmark=1, frail=1, srcline=1)),
    dict(id="eventer", old="05", new="03", tok=None,
         n=dict(otx=1, clsband=1, clsctl=1, pmark=0, frail=1, srcline=0)),
    dict(id="medcoin", old="06", new="04", tok=None,
         n=dict(otx=1, clsband=1, clsctl=1, pmark=0, frail=1, srcline=0)),
    dict(id="leadership", old="07", new="05",
         tok=("MANAGEMENT FILE", "FILE 05 &middot; MANAGEMENT"),
         n=dict(otx=0, clsband=0, clsctl=0, pmark=0, frail=1, srcline=0)),
    dict(id="tech", old="08", new="06",
         tok=("SYSTEM FILE &middot; AI", "FILE 06 &middot; SYSTEM"),
         n=dict(otx=0, clsband=0, clsctl=0, pmark=0, frail=0, srcline=0)),
]

CUTS = [
    ("otx", None, '<div class="otx"'),                    # drawer + folder-cover lift
    ("clsband", r'<div class="clsband">.*?</div>', None),  # the RESTRICTED band
    ("clsctl", r'<div class="clsctl">.*?</div>', None),    # the control number line
    ("pmark", r'<span class="pmark">.*?</span>', None),    # the (S) mark
    ("frail", r'<div class="frail">.*?</div>', None),      # the punch holes and their rail
    ("srcline", r'<div class="srcline">.*?</div>', None),  # "ON RECORD - CASE FILE 02"
]


def read(p):
    return io.open(p, encoding="utf-8").read()


def block(s, start, open_tag="<div", close_tag="</div>"):
    """Span of a tag from `start` to its own matching close -- nesting counted, not guessed."""
    i, depth = start, 0
    while i < len(s):
        a = s.find(open_tag, i)
        b = s.find(close_tag, i)
        if b < 0:
            raise SystemExit("unbalanced block from %d" % start)
        if 0 <= a < b:
            depth += 1
            i = a + len(open_tag)
        else:
            depth -= 1
            i = b + len(close_tag)
            if depth == 0:
                return start, i
    raise SystemExit("unbalanced block from %d" % start)


src = read(SRC)
print("m/index.html  %d bytes  (READ ONLY)" % len(src.encode("utf-8")))

# ---------------------------------------------------------------- the stylesheet, whole
css = []
for m in re.finditer(r"<style>(.*?)</style>", src, re.S):
    if src[max(0, m.start() - 12):m.start()].endswith("<noscript>"):
        continue
    css.append(m.group(1))
css = "\n".join(css)
print("   stylesheet   %d bytes, carried across untouched\n" % len(css.encode("utf-8")))

# ---------------------------------------------------------------- the six documents
print("   %-11s %7s %7s  %s" % ("document", "before", "after", "removed (n)"))
sections = []
totals = {}
for d in DOCS:
    m = re.search(r'<section class="sec[^"]*" id="%s"' % d["id"], src)
    if not m:
        raise SystemExit("no #%s section" % d["id"])
    i, j = block(src, m.start(), "<section", "</section>")
    sec = src[i:j]
    before = len(sec.encode("utf-8"))
    got = []
    for name, pattern, anchor in CUTS:
        want = d["n"][name]
        if anchor is not None:
            found = sec.count(anchor)
            if found != want:
                raise SystemExit("%s: expected %d x %s, found %d" % (d["id"], want, name, found))
            for _ in range(found):
                a, b = block(sec, sec.find(anchor), "<div", "</div>")
                sec = sec[:a] + sec[b:]
        else:
            found = len(re.findall(pattern, sec, re.S))
            if found != want:
                raise SystemExit("%s: expected %d x %s, found %d" % (d["id"], want, name, found))
            sec = re.sub(pattern, "", sec, flags=re.S)
        if found:
            got.append("%s x%d" % (name, found))
        totals[name] = totals.get(name, 0) + found

    # the numbering: today's values are positions on the old scrolling page
    old = '<div class="secnum" aria-hidden="true">%s</div>' % d["old"]
    if old not in sec:
        raise SystemExit("%s: .secnum %s not found" % (d["id"], d["old"]))
    sec = sec.replace(old, '<div class="secnum" aria-hidden="true">%s</div>' % d["new"])

    # the last two documents carry no file number at all today
    if d["tok"]:
        a, b = '<div class="tok">%s</div>' % d["tok"][0], '<div class="tok">%s</div>' % d["tok"][1]
        if a not in sec:
            raise SystemExit("%s: .tok %r not found" % (d["id"], d["tok"][0]))
        sec = sec.replace(a, b)

    after = len(sec.encode("utf-8"))
    print("   %-11s %7d %7d  %s%s" % (d["id"], before, after, ", ".join(got) or "-",
                                      "   tok -> " + d["tok"][1] if d["tok"] else ""))
    sections.append(sec)

print("\n   totals: " + ", ".join("%s %d" % (k, v) for k, v in sorted(totals.items())))

# ---------------------------------------------------------------- what that makes dead in the CSS
DEAD = ("otx", "ots", "otroom", "otf", "oc-", "ou-", "otdrw", "od-", "otstat",
        "clsband", "clsctl", "pmark", "frail", "hole", "srcline")
dead_n = dead_b = 0
for sel, body in re.findall(r"([^{}]+)\{([^{}]*)\}", css):
    names = re.findall(r"\.([A-Za-z][\w-]*)", sel)
    if names and all(any(n == x or n.startswith(x) for x in DEAD) for n in names):
        dead_n += 1
        dead_b += len(("%s{%s}" % (sel.strip(), body)).encode("utf-8"))
print("   CSS these deletions make dead: %d rules, %d bytes" % (dead_n, dead_b))
print("   (measured, not removed -- this script never writes to the live file)")


# ---------------------------------------------------------------- lifting the document's script
def lift(label, anchor=None, at=None, reroot=True):
    """Take one whole balanced block of the site's own script, verbatim."""
    k = at if at is not None else src.find(anchor)
    if k < 0:
        raise SystemExit("MISSING: %s" % label)
    i, depth, started = k, 0, False
    while i < len(src):
        c = src[i]
        if c == "{":
            depth += 1
            started = True
        elif c == "}":
            depth -= 1
            if started and depth == 0:
                out = src[k:src.find(";", i) + 1]
                print("   lifted %-22s %6d bytes" % (label, len(out.encode("utf-8"))))
                return out.replace("document.querySelectorAll", "root.querySelectorAll") \
                    if reroot else out
        i += 1
    raise SystemExit("unbalanced: %s" % label)


def iife_at(needle, label, reroot=False):
    k = src.index(needle)
    return lift(label, at=src.rindex("(function(){", 0, k), reroot=reroot)


# ---------------------------------------------------------------- THE SCROLL ENGINE (block 0)
# The documents rendered but did not MOVE: the ten-column chart never filled, the $9M+ never
# counted, the ring arcs never ran. One line explains all three:
#
#     function top0(el){ var r=el.getBoundingClientRect(); return r.top + window.pageYOffset }
#
# Every scene registers its trigger through top0 and its progress is compared against page
# scroll. Inside a window the document scrolls in a CONTAINER: the rect still moves, but
# window.pageYOffset is 0 and stays 0. So every scene sits frozen at t=0 -- which is also why
# the live layer appeared (it is observer-driven) while the animation did not.
#
# THE ENGINE IS NOT REWRITTEN. Its scene registry, travel and lead values and every easing
# curve are untouched; only its CLOCK is swapped, from the page to whatever is actually
# scrolling. It is emphatically NOT converted to IntersectionObserver: it is progress-driven,
# scenes advance continuously, and an observer only reports crossings.
print("")
lines = src.split("\n")
b0s = next(i for i, l in enumerate(lines) if l.strip() == "<script>" and i > 3200)
b0e = next(i for i in range(b0s, len(lines)) if lines[i].strip() == "</script>")
engine = "\n".join(lines[b0s + 1:b0e])
print("   lifted %-22s %6d bytes  (block 0, lines %d-%d)"
      % ("the scroll engine", len(engine.encode("utf-8")), b0s + 2, b0e))

# Two null guards. Block 0 was written for a page that has a hero and a progress bar, and
# dereferences both without checking. A document sample has neither, and the block died at
# load. Inert stand-ins are less invasive than importing a page's furniture into a document.
GUARDS = [
    ("var hero=document.getElementById('hero');",
     "var hero=document.getElementById('hero')||document.createElement('section');"),
    ("var pbar=document.getElementById('pbar');",
     "var pbar=document.getElementById('pbar')||document.createElement('div');"),
    # heroFx() dereferences hc on every frame without a guard, while every other hero part is
    # guarded. With no #hero in a document sample that threw inside frame(), which then never
    # re-scheduled itself -- so the engine died on its first frame and NOTHING animated. A
    # detached stand-in keeps heroFx harmless instead of fatal.
    ("var hc=hero.querySelector('.hw')||hero.querySelector('.center'),",
     "var hc=hero.querySelector('.hw')||hero.querySelector('.center')"
     "||document.createElement('div'),"),
]
# The clock. Each of these is a scroll SOURCE; the viewport-width reads (MOB, the soft-resize
# guard) are deliberately left alone, because a breakpoint is about the screen, not the box.
CLOCK = [
    ("function top0(el){var r=el.getBoundingClientRect();return r.top+window.pageYOffset}",
     "function top0(el){var r=el.getBoundingClientRect();\n"
     "  return r.top-SC.getBoundingClientRect().top+SC.scrollTop}"),
    ("var vh=window.innerHeight,DOCH=1;", "var vh=SC.clientHeight,DOCH=1;"),
    ("  var y=window.pageYOffset;if(y<0)y=0;", "  var y=SC.scrollTop;if(y<0)y=0;"),
    ("  var gate=y+window.innerHeight*(MOB?1.15:.94);", "  var gate=y+SC.clientHeight*(MOB?1.15:.94);"),
    ("  vh=window.innerHeight;", "  vh=SC.clientHeight;"),
    ("if(mf0)mf0.style.minHeight=Math.round(window.innerHeight*.56)+'px'",
     "if(mf0)mf0.style.minHeight=Math.round(SC.clientHeight*.56)+'px'"),
    ("var se=document.scrollingElement||document.documentElement;"
     "DOCH=Math.max(1,se.scrollHeight-window.innerHeight);",
     "DOCH=Math.max(1,SC.scrollHeight-SC.clientHeight);"),
    ("  var y=window.pageYOffset;\n", "  var y=SC.scrollTop;\n"),
    ("    var pb=function(){var se=document.scrollingElement||document.documentElement;"
     "pbar.style.width=(window.pageYOffset/Math.max(1,se.scrollHeight-window.innerHeight)*100)+'%'};\n"
     "    window.addEventListener('scroll',pb,{passive:true});pb();",
     "    var pb=function(){pbar.style.width="
     "(SC.scrollTop/Math.max(1,SC.scrollHeight-SC.clientHeight)*100)+'%'};\n"
     "    SC.addEventListener('scroll',pb,{passive:true});pb();"),
    ("      var top=Math.max(0,el.getBoundingClientRect().top+window.pageYOffset-8);",
     "      var top=Math.max(0,el.getBoundingClientRect().top-SC.getBoundingClientRect().top"
     "+SC.scrollTop-8);"),
]
# A LOOP THAT RE-SCHEDULES ITSELF AT THE END OF A BODY THAT CAN THROW IS ONE EXCEPTION AWAY
# FROM STOPPING FOR EVER. frame() ends with requestAnimationFrame(frame), so any error above
# that line -- a null the page had and a document sample does not, say -- kills the engine
# after exactly one frame. The symptom is precise and was observed: every scene holds the
# value it was given on that single frame, so the bars sit at scaleY(0), the arcs at their
# full --seg, and nothing ever moves again. Scheduling FIRST makes the next frame independent
# of everything below it. Same number of frames, same order, no other change.
LOOP = [
    ("function frame(){\n  window.__engineOK=true;\n",
     "function frame(){\n  requestAnimationFrame(frame);   /* scheduled FIRST: see build_doc.py "
     "-- an exception below must not be able to stop the loop */\n"
     "  window.__mwFrames=(window.__mwFrames||0)+1;   /* liveness: a dead loop should be "
     "visible, not inferred */\n"
     "  window.__engineOK=true;\n"),
    ("    statement(y);\n  }\n  requestAnimationFrame(frame);\n}",
     "    statement(y);\n  }\n}"),
]
# And the container's own scroll drives it too. On the page the rAF poll was the only clock it
# needed; in a window, binding the scroller means the engine advances on the very event that
# should advance it, whatever happens to the frame loop.
LISTEN = [("setTimeout(init,60);",
           "setTimeout(init,60);\nSC.addEventListener('scroll',frame,{passive:true});")]
for old, new in GUARDS + CLOCK + LOOP + LISTEN:
    if engine.count(old) != 1:
        raise SystemExit("block 0 changed shape (%d matches): %s" % (engine.count(old), old[:70]))
    engine = engine.replace(old, new)
left = engine.count("pageYOffset")
if left:
    raise SystemExit("%d page-scroll reads survived in the engine" % left)
print("   swapped %d scroll sources, %d null guards, loop hardened, container scroll bound"
      % (len(CLOCK), len(GUARDS)))

# Positions are cached at measure() time. This sample hides five of six documents, so they must
# be re-measured whenever the visible one changes -- measure() is the block's own function and
# is simply made reachable. The export goes INSIDE the block's own IIFE, which is where measure
# lives; appended after it, it is out of scope and throws at load.
EXPORT_AT = "  heroB=top0(hero)+hero.offsetHeight;heroFar=false;\n}\n"
if engine.count(EXPORT_AT) != 1:
    raise SystemExit("cannot find the end of measure() to export it from")
engine = engine.replace(EXPORT_AT, EXPORT_AT + "window.__mwMeasure=measure;\n"
                        # The engine advances on requestAnimationFrame. Some environments -- a
                        # background tab, and this project's own preview pane, which reports
                        # visibilityState "visible" and still produces no frames -- never fire
                        # it, and then nothing can be observed moving. This steps the engine
                        # once against the CURRENT scroll position, so the clock can be proved
                        # as a function of container scroll without a compositor. It drives the
                        # block's own frame(); it does not reimplement any of it.
                        + "window.__mwStep=function(){lastY=-1;frame();};\n"
                        # The engine's `units` and `scenes` span the whole page, and a hidden
                        # section measures at the very top of the scroller -- so every unit in
                        # the five documents that are not on screen clears the reveal gate and
                        # is marked done for good. Open any of them afterwards and its entrance
                        # has already been spent: everything arrives at once. The page this was
                        # written for never hides a section, so it never had to say what
                        # "re-entering" means; a window does. This gives one document its
                        # entrance back, and touches nothing outside it.
                        + "window.__mwRearm=function(root){\n"
                        + "  units.forEach(function(u){if(root.contains(u.el)){u.done=false;\n"
                        + "    u.el.classList.remove('on');u.el.classList.remove('done');}});\n"
                        + "  scenes.forEach(function(x){if(root.contains(x.el))x.lp=-1});\n"
                        + "};\n")
engine = "var SC=window.__mwScroller||document.scrollingElement||document.documentElement;\n" + engine

# the swipe-to-reveal on "Zero commercial infrastructure.", which Oran's list KEEPS
redx = lift("redaction handler", "document.querySelectorAll('.redx').forEach(function(r){")

# The .rxs bars lift on SCROLL rather than on a tap, so pointed at the page they never lift
# inside a window. Every document has at least one.
rxs = iife_at("var els=[].slice.call(document.querySelectorAll('.rxs'));", "rxs scroll lift",
              reroot=True)
# Two substitutions, and only two. The block measures each bar as `rect.top + pageYOffset`, the
# page-relative offset. Inside a scroll container the rect is still relative to the BROWSER
# viewport, so that sum is out by wherever the container sits.
for old, new in (("var y=pageYOffset;",
                  "var y=root.scrollTop, rt=root.getBoundingClientRect().top;"),
                 ("st[i].top=st[i].el.getBoundingClientRect().top+y;",
                  "st[i].top=st[i].el.getBoundingClientRect().top-rt+y;")):
    if old not in rxs:
        raise SystemExit("rxs block changed shape -- re-check: %s" % old)
    rxs = rxs.replace(old, new)

# ---------------------------------------------------------------- the LIVE LAYER
# The documents do not end with their markup. Four IIFEs after the last </section> build a
# whole layer at runtime, and rendering the sections alone gets a static skeleton of it:
#
#   1. the EVIDENCE SLIP, injected after each file's headline figure
#   2. the UV LAMP, its developed zones, the film edge and the signature line
#   3. the ANALYST NOTE, struck glyph by glyph with deterministic jitter
#   4. the METHOD SLIP and the sheet-flip tab that turns between the two faces
#
# They query `document` and the sections are in this page, so they are lifted WHOLE and run
# unmodified apart from the edits recorded below. Source order is dependency order: the lamp
# needs the folder, and both the note and the method slip need the evidence slip. Only the four
# CASE files appear in their tables -- LEADERSHIP and TECH never had a live layer, and this
# reproduces that rather than inventing one for them.
print("")
live = "\n".join([
    iife_at("var DEFS=[", "evidence slip"),
    iife_at("var LAMPS={", "uv lamp + zones"),
    iife_at("var NOTES={", "analyst note"),
    iife_at("xtix:{ctrl:'(S)", "method slip + flip"),
])

# ---- the deletion list, extended into the live layer.
# The approved lines were measured on the HTML, so they missed the JS -- which re-injects the
# same control-number prop TWICE, not once: in the METHOD slip (the -A numbers) and again in
# the EVIDENCE slip, where it lands exactly where the deleted (S) mark used to sit beside the
# headline figure. Same prop, same ruling, so both go -- and the <b> that renders it goes with
# them, because an empty bold tag in a header reads as a bug the way an empty band would.
#
# The two are spelled differently in the source: the evidence slip writes its middot and numero
# as literal \u escapes, the method slip writes the characters themselves.
EV_CTRL = re.compile(r"\n\s*ctrl:'\(.\) \\u00B7 CTRL \\u2116 [^']*',")
MS_CTRL = re.compile("ctrl:'\\(.\\) · CTRL № [^']*',")   # sits inline after `xtix:{`
EV_RENDER = "'<div class=\"es-h\"><span>EVIDENCE SLIP</span><b>'+df.ctrl+'</b></div>'"
EV_CLEAN = "'<div class=\"es-h\"><span>EVIDENCE SLIP</span></div>'"
MS_RENDER = ("'<div class=\"es-h\"><span>METHOD SLIP — HOW THE CLAIM WAS BUILT</span><b>'+\n"
             "      M[id].ctrl+'</b></div>'+")
MS_CLEAN = "'<div class=\"es-h\"><span>METHOD SLIP — HOW THE CLAIM WAS BUILT</span></div>'+"

# THE LAMP HANGS OFF A DELETED ELEMENT. Its builder bails on `if(!band)return`, where band is
# `.clsband` -- one of the approved deletions -- and `band` is never read again. So removing
# the RESTRICTED band silently removes the UV lamp, its developed zones, the film edge and the
# signature line from all four case files. The guard is vestigial: the `.folder` check above it
# and the `built` counter below it already do the real work.
LAMP_GUARD = "    var band=sec.querySelector('.clsband');if(!band)return;\n"
LAMP_CLEAN = ("    /* the .clsband guard went with the band itself: it was never read again,\n"
              "       and the .folder check above and the `built` counter below already gate\n"
              "       this. Left in place it would have deleted the lamp along with it. */\n")

edits = [
    ("ctrl prop, evidence slip", EV_CTRL, ""),
    ("ctrl prop, method slip", MS_CTRL, ""),
    ("ctrl render, evidence slip", EV_RENDER, EV_CLEAN),
    ("ctrl render, method slip", MS_RENDER, MS_CLEAN),
    ("the lamp's guard on the deleted .clsband", LAMP_GUARD, LAMP_CLEAN),
]
print("")
for label, old, new in edits:
    if hasattr(old, "sub"):
        n = len(old.findall(live))
        live = old.sub(new, live)
    else:
        n = live.count(old)
        live = live.replace(old, new)
    if not n:
        raise SystemExit("MISSING in live layer: %s" % label)
    print("   live layer: %-40s %d" % (label, n))
if "ctrl" in live:
    raise SystemExit("a ctrl reference survived in the live layer")


# ---------------------------------------------------------------- charset, belt and braces
# The lifted script carries real UTF-8: em dashes, middots, arrows, the numero sign. Served
# without a declared charset the browser guessed windows-1252 and the METHOD SLIP header came
# out as mojibake. The page declares its charset -- and on top of that every non-ASCII
# character in the JS is written as an escape, which is pure ASCII and cannot be mis-decoded
# however a server describes the file. Two independent fixes, because the first depends on a
# <meta> surviving whatever wrapper the page ends up inside.
def ascii_js(t):
    out = []
    for c in t:
        out.append(c if ord(c) < 128 else "\\u%04x" % ord(c))
    return "".join(out)


engine = ascii_js(engine)
redx = ascii_js(redx)
rxs = ascii_js(rxs)
live = ascii_js(live)

# ---------------------------------------------------------------- assemble
kit = os.path.join(REPO, "lab", "_kit.js")
K.emit_js(kit)
parts = {
    "/*KIT*/": read(kit).strip(),
    "/*SCREEN*/": read(os.path.join(HERE, "screen.js")).strip(),
    "/*DOCCSS*/": css,
    "/*ENGINE*/": engine,
    "/*REDX*/": redx,
    "/*RXS*/": rxs,
    "/*LIVE*/": live,
    "<!--DOCHTML-->": "\n".join(sections),
}
html = read(TPL)
for mark, body in parts.items():
    if mark not in html:
        raise SystemExit("template has lost its %s marker" % mark)
    html = html.replace(mark, body)
io.open(OUT, "w", encoding="utf-8").write(html)
print("\nlab/document.html  %d bytes  (%d documents)" % (len(html.encode("utf-8")), len(DOCS)))
