# -*- coding: utf-8 -*-
"""The build. One input tree, one output tree, and a ratchet that will not let it drift.

    python build.py            build and check
    python build.py --accept   build, and adopt the result as the new baseline

The migration works by emptying `src/_monolith.html`. Everything starts inside it; sections move
out into `src/doc/` one at a time; when the file is gone the migration is done. That is the whole
process, and it is legible from the file listing alone.

**The ratchet.** `src/.baseline` holds the md5 of `m/index.html` as it stood before any of this
began. Every build compares against it:

  MATCH     the output is byte-for-byte what it always was. A cut that reports MATCH is proven
            clean — no rendering, no screenshot, no judgement involved.
  DIFFERS   the output changed. Legitimate when a change of copy or structure was intended, and
            then `--accept` records the new baseline with a note. Never legitimate silently.

Byte-identity is a far stronger instrument than a pixel diff and it is free, so it is used for
every step where it is achievable — which is every step that only moves code. The pixel diff in
ARCHITECTURE.md §11.4 is for the steps where the output is *supposed* to change.
"""
import hashlib
import io
import json
import re
import os
import subprocess
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
SRC = os.path.join(HERE, 'src')
OUT = os.path.join(HERE, 'm', 'index.html')
ROOT_INDEX = os.path.join(HERE, 'index.html')
BASELINE = os.path.join(SRC, '.baseline')


def read(*parts):
    return io.open(os.path.join(SRC, *parts), encoding='utf-8').read()


def md5(b):
    return hashlib.md5(b if isinstance(b, bytes) else b.encode('utf-8')).hexdigest()


def main():
    accept = '--accept' in sys.argv

    # the root build is an archive until §14.2 step 1 is complete for all eleven sections.
    # This guard is inherited from build_mobile.py, where it kept two tracks apart; it now
    # protects the thing being harvested, and it outlives the reason it was written.
    root_before = md5(io.open(ROOT_INDEX, 'rb').read())

    head = read('head.html')
    body = read('_monolith.html')

    # Expand every <!--DOC:id--> back into place. Verbatim in, verbatim out — which is exactly
    # what lets a correct cut leave the built page byte-for-byte unchanged.
    docdir = os.path.join(SRC, 'doc')
    for name in sorted(os.listdir(docdir)):
        if not name.endswith('.html'):
            continue
        mark = '<!--DOC:%s-->' % name[:-5]
        if mark not in body:
            raise SystemExit('src/doc/%s exists but its marker is not in the monolith' % name)
        body = body.replace(mark, read('doc', name), 1)

    # and every /*D:id:n*/ back into the stylesheet it was taken from
    for name in sorted(os.listdir(docdir)):
        if not name.endswith('.css'):
            continue
        sid = name[:-4]
        # split on the marker only; whatever follows it is the rule, byte for byte. Nothing is
        # stripped here, because stripping is how two newlines went missing the first time.
        chunks = re.split(r'/\*--(\d+)--\*/', read('doc', name))
        for n, rule in zip(chunks[1::2], chunks[2::2]):
            mark = '/*D:%s:%s*/' % (sid, n)
            if mark not in body:
                raise SystemExit('rule marker %s is missing from the monolith' % mark)
            body = body.replace(mark, rule, 1)

    # and the Macintosh shell, lifted out of the lab template by tools/extract_shell.py.
    #
    # It ships INERT: the entry gate at the end of frame.css keeps .mw out of the document
    # until <html> carries mw-on. Without that the shell is a white sheet over the whole page,
    # because in the lab it WAS the whole page.
    #
    # Order matters and is asserted by the marker names: the kit defines what the seven files
    # are, the folder renderer counts them, and the frame reads K.order on its first line.
    # and the Macintosh itself — page 3. Procedural, 117 KB; the 933 KB baked mesh stays in
    # the lab, where it does not have to fit a 520 KB budget. See tools/extract_machine.py.
    machdir = os.path.join(SRC, 'machine')
    for mark, name in (('/*MACHINE:css*/', 'machine.css'),
                       ('<!--MACHINE:html-->', 'machine.html'),
                       ('/*MACHINE:js*/', 'machine.js')):
        if body.count(mark) != 1:
            raise SystemExit('machine marker %s appears %d times, expected 1'
                             % (mark, body.count(mark)))
        path = os.path.join(machdir, name)
        if not os.path.exists(path):
            raise SystemExit('%s is missing; run tools/extract_machine.py --write' % path)
        body = body.replace(mark, io.open(path, encoding='utf-8').read(), 1)

    shelldir = os.path.join(SRC, 'shell')
    for mark, name in (('/*SHELL:css*/', 'frame.css'),
                       ('<!--SHELL:html-->', 'frame.html'),
                       ('/*SHELL:kit*/', 'kit.js'),
                       ('/*SHELL:screen*/', 'screen.js'),
                       ('/*SHELL:js*/', 'frame.js'),
                       ('/*SHELL:folder*/', 'folder.js'),
                       ('/*SHELL:router*/', 'router.js'),
                       ('/*SHELL:cursor*/', 'cursor.css')):
        if body.count(mark) != 1:
            raise SystemExit('shell marker %s appears %d times, expected 1'
                             % (mark, body.count(mark)))
        path = os.path.join(shelldir, name)
        if not os.path.exists(path):
            raise SystemExit('%s is missing; run tools/extract_shell.py --write' % path)
        body = body.replace(mark, io.open(path, encoding='utf-8').read(), 1)

    left = re.findall(r'<!--DOC:\w+-->|/\*D:\w+:\d+\*/|/\*SHELL:\w+\*/|<!--SHELL:\w+-->' + r'|/\*MACHINE:\w+\*/|<!--MACHINE:\w+-->', body)
    if left:
        raise SystemExit('unexpanded markers remain: %s' % left)

    # CHECK 10: no selector list may end in a comma.
    #
    # Removing #sndtg from four grouped rules left `.otx,#loglin,#recled,{...}`. A trailing
    # comma makes the whole selector list invalid, and a browser discards the entire rule
    # rather than the bad part of it — so four kill-switches died at once and nothing said so.
    # The serious one was prefers-reduced-motion: a reader who had asked for stillness was
    # getting a scrambling log line and a pulsing red LED instead.
    #
    # Only <style> contents are examined. A blanket search would hit 34 legitimate JavaScript
    # call sites like addEventListener('scroll', pb, {passive:true}) — the first repair written
    # for this bug did exactly that, and would have corrupted every one of them.
    for m in re.finditer(r'<style[^>]*>(.*?)</style>', head + body, re.S):
        for bad in re.finditer(r'([^{}]{0,120}),\s*\{', m.group(1)):
            raise SystemExit('selector list ends in a comma, so the browser will discard the '
                             'whole rule:\n    %s' % ' '.join(bad.group(0).split())[-110:])

    # CHECK 11: no id may appear twice in the output.
    #
    # The frame's icon box was called #files, and page 3 is a section that has always been called
    # #files too. getElementById answers with the first match, so drawFiles() ran innerHTML="" on
    # PAGE 3 and erased it, and the Macintosh inside it, the moment the reader entered the shell.
    # Nothing errored. The damage was only visible after coming back out to an empty page.
    #
    # Two documents cannot share a name, and the build is the right place to say so — it is the
    # only point that sees every fragment assembled together.
    # Markup only. The stylesheet carries SVG filters inside data: URIs — mask-image with a
    # <filter id="r"> in it, twice — and each data URI is its own document, so those are not a
    # collision. The first version of this check reported them, which is the same mistake check
    # 10 was written to avoid: look where the thing actually lives.
    markup_only = re.sub(r'<style[^>]*>.*?</style>', '', body, flags=re.S)
    counts = {}
    for m in re.finditer(r'\sid="([^"]+)"', markup_only):
        counts[m.group(1)] = counts.get(m.group(1), 0) + 1
    dupes = ['%s x%d' % (k, n) for k, n in sorted(counts.items()) if n > 1]
    if dupes:
        raise SystemExit('the same id appears more than once, so getElementById will answer with '
                         'whichever came first:\n    ' + ', '.join(dupes))

    html = head + body + '\n</body>\n</html>'

    # CHECK 12: every <script> block in the output must parse as JavaScript.
    #
    # The machine's fragment shader is a single-quoted JS string a couple of thousand
    # characters long, and the GLSL comments inside it escape their apostrophes because they
    # have to. I wrote a comment in that said "the monitor's footprint"; the apostrophe closed
    # the literal, and the whole machine stopped existing -- no parts, no camera, nothing on
    # the page where the Macintosh had been. The build still succeeded. Every other check
    # still passed. It shipped 1.9 MB with a hole in it.
    #
    # A syntax error is the cheapest thing in the world to detect and one of the most
    # expensive to ship, so the build asks a parser now instead of trusting the author. Each
    # block is wrapped in a function body -- which is what a <script> effectively is -- so a
    # top-level return is legal and declarations in one block cannot collide with another.
    #
    # If node is not installed the check says it was skipped rather than passing quietly. It
    # does not fail the build for a missing tool, but a check that can silently not run is
    # not a check.
    blocks = [m.group(1) for m in re.finditer(
        r'<script(?![^>]*\bsrc=)[^>]*>(.*?)</script>', html, re.S) if m.group(1).strip()]
    probe = os.path.join(HERE, '.syntax_probe.js')
    try:
        io.open(probe, 'w', encoding='utf-8', newline='').write(
            'const b=' + json.dumps(blocks) + ';\n'
            'for(let i=0;i<b.length;i++){\n'
            '  try{ new Function(b[i]) }catch(e){\n'
            '    console.log("FAIL block "+i+": "+e.message);\n'
            '    console.log("   it begins: "+b[i].replace(/\\s+/g," ").slice(0,110));\n'
            '    process.exit(3); } }\n'
            'console.log("OK "+b.length);\n')
        r = subprocess.run(['node', probe], capture_output=True, text=True)
        out = (r.stdout or '').strip()
        if r.returncode == 3:
            raise SystemExit('a <script> block in the output is not valid JavaScript:\n    '
                             + out.replace('\n', '\n    '))
        if r.returncode != 0:
            print('  note: the JavaScript syntax check could not run')
        else:
            print('  %s script blocks parse' % out.split()[-1])
    except FileNotFoundError:
        print('  note: node is not installed, so the JavaScript syntax check was skipped')
    finally:
        try:
            os.remove(probe)
        except OSError:
            pass

    # CHECK 13: nothing may CALL a function the page never defines.
    #
    # CHECK 12 proves each block parses. Parsing is not resolving. Sound was removed from this
    # page and its functions went with it -- paper(), flip(), thunk() -- while the CALLS
    # stayed, along with tick(), whose definition left with the HUD. Five of them. Every one
    # parses perfectly and throws ReferenceError the moment it runs, and two were inside
    # loop(), the page's main requestAnimationFrame body, which re-arms itself on its own last
    # line: the first folder-pull past 4% of its travel killed the scroll loop for the rest of
    # the visit. It shipped, and every check we had called the build clean.
    #
    # This models no scope, deliberately. A name declared anywhere in the page counts as
    # declared, so the check under-reports and can never cry wolf. What it does catch is the
    # exact shape of the fault above: code deleted, call sites left behind.
    JS_GLOBALS = set('''
        window document console Math JSON Date Object Array String Number Boolean RegExp Error
        TypeError RangeError SyntaxError Promise Set Map WeakMap WeakSet Symbol Function
        parseInt parseFloat isNaN isFinite encodeURIComponent decodeURIComponent encodeURI
        decodeURI setTimeout setInterval clearTimeout clearInterval requestAnimationFrame
        cancelAnimationFrame matchMedia getComputedStyle fetch Image Audio Uint8Array
        Uint8ClampedArray Uint16Array Uint32Array Int8Array Int16Array Int32Array Float32Array
        Float64Array ArrayBuffer DataView atob btoa IntersectionObserver ResizeObserver
        MutationObserver PerformanceObserver performance navigator location history screen
        localStorage sessionStorage CustomEvent Event KeyboardEvent PointerEvent MouseEvent
        URL URLSearchParams Blob FileReader TextDecoder TextEncoder Intl Proxy Reflect
        structuredClone queueMicrotask AbortController DOMParser XMLHttpRequest WebSocket
        addEventListener removeEventListener dispatchEvent scrollTo scrollBy getSelection
        if for while switch return typeof new delete void in of instanceof do else try catch
        finally throw break continue case default class extends super this function var let
        const yield await async static get set eval arguments
    '''.split())
    # ONE left-to-right pass over strings and comments together, so a quote inside another
    # kind of quote cannot open a string of its own -- which it did on my first attempt, and
    # the machine's GLSL leaked out of a single-quoted literal and reported nine of its own
    # functions as missing.
    NOISE = re.compile(r'"(?:[^"\\]|\\.)*"' r"|'(?:[^'\\]|\\.)*'" r'|`(?:[^`\\]|\\.)*`'
                       r'|/\*.*?\*/|//[^\n]*', re.S)
    js = NOISE.sub(' ', '\n;\n'.join(blocks))
    declared = set()
    for pat in (r'\bfunction\s+([A-Za-z_$][\w$]*)',
                r'\b(?:var|let|const)\s+([A-Za-z_$][\w$]*)',
                r'([A-Za-z_$][\w$]*)\s*=\s*function',
                r'window\.([A-Za-z_$][\w$]*)\s*=',
                r'\bcatch\s*\(\s*([A-Za-z_$][\w$]*)',
                r'\bfunction\b[^(]*\(([^)]*)\)'):
        for m in re.finditer(pat, js):
            for part in re.split(r'[,\s]+', m.group(1)):
                if re.match(r'^[A-Za-z_$][\w$]*$', part or ''):
                    declared.add(part)
    for m in re.finditer(r'\b(?:var|let|const)\s+([^;\n{]{0,400})', js):
        for part in re.findall(r'([A-Za-z_$][\w$]*)\s*(?==|,|$)', m.group(1)):
            declared.add(part)
    ghosts = {}
    for m in re.finditer(r'(?<![.\w$])([A-Za-z_$][\w$]*)\s*\(', js):
        name = m.group(1)
        if name not in JS_GLOBALS and name not in declared:
            ghosts[name] = ghosts.get(name, 0) + 1
    if ghosts:
        raise SystemExit('the page calls a function it never defines, so this parses and then '
                         'throws ReferenceError when it runs:\n    '
                         + '\n    '.join('%s()  called %d time(s)' % (k, ghosts[k])
                                         for k in sorted(ghosts)))
    print('  no calls to undefined functions')

    io.open(OUT, 'w', encoding='utf-8', newline='').write(html)
    got = md5(html)
    want = read('.baseline').strip()

    root_after = md5(io.open(ROOT_INDEX, 'rb').read())
    assert root_before == root_after, 'SAFETY: index.html at the repo root changed'

    print('m/index.html   %d bytes   md5 %s' % (len(html.encode()), got))
    print('baseline                    md5 %s' % want)
    print()
    if got == want:
        print('  MATCH — byte-for-byte identical to the current baseline.')
        return 0
    if accept:
        # A baseline that can move without leaving a reason is not a ratchet, it is a habit.
        why = ' '.join(a for a in sys.argv[1:] if not a.startswith('--'))
        if not why:
            print('  --accept needs a reason. Example:')
            print('    python build.py --accept "oasis: restored the coaching line, DECISIONS #16"')
            return 1
        io.open(BASELINE, 'w', encoding='utf-8', newline='').write(got)
        with io.open(os.path.join(SRC, '.baseline.log'), 'a', encoding='utf-8', newline='') as f:
            f.write('%s  %s  %s\n' % (got, want, why))
        print('  DIFFERS, and --accept was given.')
        print('  new baseline %s' % got)
        print('  reason       %s' % why)
        return 0
    print('  DIFFERS — and no --accept was given.')
    print()
    print('  If this was intended, look at the change first, then re-run with --accept.')
    print('  If it was not, the last edit moved more than it meant to.')
    return 1


if __name__ == '__main__':
    sys.exit(main())
