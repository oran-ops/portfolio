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
import re
import os
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

    left = re.findall(r'<!--DOC:\w+-->|/\*D:\w+:\d+\*/', body)
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

    html = head + body + '\n</body>\n</html>'

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
