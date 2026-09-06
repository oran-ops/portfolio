# -*- coding: utf-8 -*-
"""Remove the sound layer. Oran: *"אפשר להוריד — אני לא רוצה להתעסק בזה יותר מדי."*

Five synthesised voices — paper, flip, thunk, tick and a noise burst — built live in an
AudioContext, so nothing was ever downloaded. A visible SND ON / SND OFF toggle, remembered in
localStorage. None of it played on a phone.

It comes out cleanly, and safely, for a reason worth stating: the accessor is already written
as `AU = function(){ return window.__archAudio || {} }`, and every call site is
`try{ AU().tick && AU().tick() }catch(e){}`. Absence was handled from the first day. Removing
the source leaves the call sites harmless — they are removed anyway, but nothing depended on
their surviving.

`python tools/depends.py sndtg __archAudio` reports no gates, which is the check that was
missing when `.clsband` was cut.

FIVE CSS RULES NAME #sndtg ALONGSIDE #loglin AND #recled. Those two are the floating archive
HUD, which Oran ruled stays on the three scrolling pages and disappears inside the machine. So
those rules lose a selector; they are not deleted.

    python tools/cut_sound.py           report
    python tools/cut_sound.py --write   make the cut
"""
import io
import os
import re
import sys

sys.stdout.reconfigure(encoding='utf-8', errors='replace')
HERE = os.path.dirname(os.path.abspath(__file__))
MONO = os.path.join(os.path.dirname(HERE), 'src', '_monolith.html')

OPEN = '/* ================= archive audio'
CALLS = [r'\s*try\{AU\(\)\.\w+&&AU\(\)\.\w+\(\)\}catch\(e\)\{\}',
         r'\s*try\{if\(AU\(\)\.nz\)AU\(\)\.nz\([^;]*?\)\}catch\(e\)\{\}']
ACCESSOR = r'\s*var AU=function\(\)\{return window\.__archAudio\|\|\{\}\};'
PURE_CSS = [r'\s*/\* sound toggle \*/\s*#sndtg\{[^{}]*\}',
            r'\s*#sndtg\.off\{[^{}]*\}',
            r'\s*#sndtg:hover\{[^{}]*\}']
# selectors to drop from grouped rules, leaving the rest of the rule intact
SHARED = [r'(?<=,)html\.jscur #sndtg(?=,)', r'(?<=,)#sndtg(?=\{)',
          r'(?<=,)body\.static #sndtg(?=\{)', r'(?<=,)body\.failsafe #sndtg(?=\{)']

# Present in the file, so asserting them proves something. #loglin and #recled are the HUD
# Oran keeps; __archLog and the theatre share the audio's script block and must not move.
KEEP = ['#loglin', '#recled', '__archLog', 'LOGMAP', 'scrambleTo', 'THS=', '__bootOpen']


def main():
    write = '--write' in sys.argv
    src = io.open(MONO, encoding='utf-8').read()
    for k in KEEP:
        if k not in src:
            print('  REFUSED: keep-list entry %r is not in the file; asserting it proves nothing' % k)
            return 1

    out = src
    report = []

    a = out.find(OPEN)
    if a < 0:
        print('  REFUSED: the archive-audio banner is not there')
        return 1
    b = out.find('/* =================', a + 20)
    if b < 0:
        print('  REFUSED: no banner closes the audio section')
        return 1
    report.append(('the synth, the five voices and the toggle', b - a))
    out = out[:a] + out[b:]

    for pat, label in ((ACCESSOR, 'the AU accessor'),):
        n = len(re.findall(pat, out))
        report.append((label, sum(len(m.group(0)) for m in re.finditer(pat, out))))
        out = re.sub(pat, '', out)
        if n == 0:
            print('  REFUSED: %s not found' % label)
            return 1

    calls = 0
    for pat in CALLS:
        for m in re.finditer(pat, out):
            calls += len(m.group(0))
        out = re.sub(pat, '', out)
    report.append(('the call sites', calls))

    css = 0
    for pat in PURE_CSS:
        for m in re.finditer(pat, out):
            css += len(m.group(0))
        out = re.sub(pat, '', out)
    report.append(('#sndtg CSS rules', css))

    shared = 0
    for pat in SHARED:
        for m in re.finditer(pat, out):
            shared += len(m.group(0)) + 1
        out = re.sub(pat + r',?', '', out)
    report.append(('#sndtg dropped from shared selectors', shared))

    for k in KEEP:
        if k not in out:
            print('  REFUSED: the cut removed %r, which must survive' % k)
            return 1
    for bad in ('__archAudio', 'sndtg', 'arch_snd', 'AudioContext'):
        if bad in out:
            print('  REFUSED: %r still present after the cut' % bad)
            return 1

    for label, n in report:
        print('  %-40s %6d B' % (label, n))
    print('  %-40s %6d B%s' % ('TOTAL', len(src) - len(out), '' if write else '   (dry run)'))
    if write:
        io.open(MONO, 'w', encoding='utf-8', newline='').write(out)
        print('  now run:  python build.py')
    return 0


if __name__ == '__main__':
    sys.exit(main())
