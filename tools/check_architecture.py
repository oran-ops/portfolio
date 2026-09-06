# -*- coding: utf-8 -*-
"""Check docs/ARCHITECTURE.md against the code and against itself.

Three passes, and each one is an instrument rather than a reading:

  FACTS       every number in the document is re-measured from m/index.html and compared.
              A specification that quotes a figure the code does not have is worse than one
              that quotes none, because it will be trusted.

  CLOSURE     the state machine is checked for the properties that make it a machine: every
              transition names declared states, every state has an entry AND an exit, every
              state is reachable from boot, and states and URLs are a bijection. The exit
              half is the one that is always missing, and missing exits are where scroll-lock
              bugs live.

  CONSISTENCY the same list of seven documents appears in four places in the document and the
              four must agree; the per-section rule counts appear in two and must agree.

Run from the repo root. Exit code 1 if anything fails.
"""
import io
import os
import re
import sys
import collections

sys.stdout.reconfigure(encoding='utf-8', errors='replace')
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DOC = io.open(os.path.join(ROOT, 'docs', 'ARCHITECTURE.md'), encoding='utf-8').read()
PAGE = io.open(os.path.join(ROOT, 'm', 'index.html'), encoding='utf-8').read()

FAIL = []
OK = []


def check(name, got, want, tol=0):
    same = (abs(got - want) <= tol) if isinstance(want, (int, float)) else (got == want)
    (OK if same else FAIL).append((name, got, want))
    print('  %-46s %-16s %s' % (name, got, 'ok' if same else 'EXPECTED ' + str(want)))


def section(n):
    """the text of one numbered section of the document"""
    m = re.search(r'\n## %s\..*?(?=\n## |\Z)' % n, DOC, re.S)
    return m.group(0) if m else ''


def sub(n):
    """one numbered SUBsection, e.g. 5.2.

    The first version of this checker pointed s51, s52 and s53 all at section(5), so counting
    the rows of "the transitions table" silently counted the states table and the entry/exit
    table too and reported 17 rows for a table with 8. A checker that cannot address the thing
    it is checking will report on something else, and sound exactly as confident doing it.
    """
    m = re.search(r'\n### ' + re.escape(n) + r' .*?(?=\n### |\n## |\Z)', DOC, re.S)
    return m.group(0) if m else ''


# ============================================================ PASS 1 - FACTS
print('=' * 78)
print('PASS 1  FACTS - every figure re-measured from the code')
print('=' * 78)

css = '\n'.join(re.findall(r'<style[^>]*>(.*?)</style>', PAGE, re.S))
js = '\n'.join(re.findall(r'<script[^>]*>(.*?)</script>', PAGE, re.S))
b64 = re.findall(r'base64,([A-Za-z0-9+/=]+)', css)
css_nofont = re.sub(r'base64,[A-Za-z0-9+/=]+', 'base64,X', css)
rules = re.findall(r'([^{}]+)\{[^{}]*\}', css_nofont)

check('page size, KB', len(PAGE.encode()) // 1024, 688, 1)
check('fonts, binary KB', sum(len(x) * 3 // 4 for x in b64) // 1024, 222, 2)
check('fonts, base64 KB', sum(len(x) for x in b64) // 1024, 299, 2)
check('css without fonts, KB', len(css_nofont.encode()) // 1024, 179, 2)
check('css rules', len(rules), 1529, 2)
check('style tags', len(re.findall(r'<style', PAGE)), 4)
check('js KB', len(js.encode()) // 1024, 143, 2)
check('js lines', js.count('\n'), 2960, 5)
check('script tags', len(re.findall(r'<script', PAGE)), 23)
check('functions', len(re.findall(r'function\s+\w+|=>\s*\{', js)), 105, 2)
check('addEventListener', js.count('addEventListener'), 61)
check('querySelector', len(re.findall(r'querySelector', js)), 132)
check('IntersectionObserver', js.count('IntersectionObserver'), 21)
check('requestAnimationFrame', js.count('requestAnimationFrame'), 32)
check('getBoundingClientRect', js.count('getBoundingClientRect'), 37)
check('matchMedia', js.count('matchMedia'), 26)
check('@media blocks', len(re.findall(r'@media', css_nofont)), 100)
check('@media distinct', len(set(m.strip() for m in re.findall(r'@media[^{]*', css_nofont))), 20)
check('history.* calls', len(re.findall(r'history\.', js)), 0)
check('location.hash', js.count('location.hash'), 0)
check('external URLs', len(set(re.findall(r'(?:src|href)\s*[=:]\s*["\']?(https?://[^"\')\s]+)', PAGE))), 1)

SEC = ['hero', 'statement', 'philosophy', 'files', 'xtix', 'oasis',
       'eventer', 'medcoin', 'leadership', 'tech', 'final']
own = collections.Counter()
shared = glob = 0
for r in rules:
    hits = [x for x in SEC if '#' + x in r]
    if len(hits) == 1:
        own[hits[0]] += 1
    elif len(hits) > 1:
        shared += 1
    else:
        glob += 1
check('rules scoped to one section', sum(own.values()), 545)
check('rules spanning several', shared, 21)
check('rules global / kit', glob, 963)

DOC_COUNTS = {'final': 174, 'hero': 140, 'statement': 58, 'medcoin': 37, 'philosophy': 36,
              'tech': 36, 'files': 23, 'leadership': 18, 'xtix': 16, 'eventer': 4, 'oasis': 3}
for k, v in DOC_COUNTS.items():
    check('  rules scoped to #%s' % k, own[k], v)

order = [m.group(1) for m in re.finditer(r'<section[^>]*id="([^"]+)"', PAGE)]
check('section order matches', order, SEC)

TOKENS = {'--bg': '#191A1F', '--card': '#202127', '--card2': '#25262D', '--ink': '#F2F1ED',
          '--mut': '#B6B7BB', '--dim': '#B6B7BB', '--lbl': '#CFD0D4', '--grid': '#33353C',
          '--grid2': '#4B4E55', '--emb': '#2FB380', '--brass': '#E0A458', '--ice': '#5E8FBF'}
root = re.search(r':root\s*\{([^}]*)\}', css_nofont)
have = dict(re.findall(r'(--[\w-]+)\s*:\s*([^;]+)', root.group(1))) if root else {}
bad = [k for k, v in TOKENS.items() if have.get(k, '').strip() != v]
check('colour tokens match :root', 'all %d match' % len(TOKENS) if not bad else 'MISMATCH %s' % bad,
      'all %d match' % len(TOKENS))

for tok, val in TOKENS.items():
    if ('| `%s` | `%s` |' % (tok, val)) not in DOC and tok not in ('--mut', '--dim'):
        FAIL.append(('token %s in doc' % tok, 'absent or wrong', val))

# ---- the claims added after the deep pass -------------------------------
root = io.open(os.path.join(ROOT, 'index.html'), encoding='utf-8', errors='replace').read()
check('two sites exist: root KB', len(root.encode()) // 1024, 945, 1)
check('two sites exist: m/ KB', len(PAGE.encode()) // 1024, 688, 1)
check('neither site redirects to the other',
      ('location.replace' in root) or ('http-equiv="refresh"' in root), False)
check('.rv elements that start invisible',
      sum(1 for m in re.finditer(r'class="([^"]*)"', PAGE)
          if re.search(r'(?:^|\s)rv(?:\s|$)', m.group(1))), 83)
check('.rv is revealed by adding .on', '.rv.on' in css_nofont, True)
check('doc entry action runs the reveal pass',
      'run the reveal pass over it' in DOC, True)
check('the two-sites finding is in the document', '§1.3' in DOC or '1.3 There are two sites' in DOC, True)
check('dead-CSS finding is in the document', '26.3 KB' in DOC, True)
check('kit is stated as 61 KB, not 114', 'kit is 61 KB, not 114' in DOC, True)

# ---- the divergence finding -----------------------------------------
def vis(doc):
    # script and style stripped first, or the count is mostly JavaScript
    d = re.sub(r'<(script|style)[^>]*>.*?</' + chr(92) + '1>', ' ', doc, flags=re.S)
    return len(re.sub(r'<[^>]+>', ' ', d).split())


check('root and m/ word counts are within 10', abs(vis(root) - vis(PAGE)) <= 10, True)
for probe in ['connect to the vision', 'Recruited an entire sales team', 'FOUNDER CASE STUDY']:
    check('  "%s" is in root only' % probe[:28], (probe in root) and (probe not in PAGE), True)
check('the divergence finding is in the document', '1.6 The two builds have diverged' in DOC, True)
check('the 52 figure was corrected, not quietly dropped',
      'replaces an earlier one that said 52' in DOC, True)
check('the corrected total is stated', '10 candidates, not 52' in DOC, True)
check('the reconciliation sheet exists',
      os.path.exists(os.path.join(ROOT, 'docs', 'CONTENT_RECONCILIATION.md')), True)
check('cut and reconcile are kept apart',
      'never combined' in DOC and 'exactly one kind of change' in DOC, True)
check('base build is settled as m/', '**`m/index.html`**' in DOC, True)
check('published url is settled as /m/', '**`/portfolio/m/`**' in DOC, True)
check('root is harvested before it is replaced',
      'does not happen before step 1 is complete' in DOC, True)
check('every url in the map is under /m/',
      all(u.startswith('/portfolio/m/') for u in
          re.findall(r'^\| `(/[^`]+)` \|', section(6), re.M)), True)

# ============================================================ PASS 2 - CLOSURE
print()
print('=' * 78)
print('PASS 2  CLOSURE - is the state machine actually a machine')
print('=' * 78)

s51, s52, s53, s6 = sub('5.1'), sub('5.2'), sub('5.3'), section(6)
states = set(re.findall(r'^\| `(\w+)` \|', s51, re.M))
trans = re.findall(r'^\| `?(\w+)`? \| `?(\w+)`? \| ([^|]+) \| ([^|]+) \|', s52, re.M)
trans = [t for t in trans if t[0] in states and t[1] in states]
entry = set(re.findall(r'^\| `(\w+)` \| ([^|]+) \| ([^|]+) \|$', s53, re.M) and
            [m[0] for m in re.findall(r'^\| `(\w+)` \| ([^|]+) \| ([^|]+) \|$', s53, re.M)])
urls = dict(re.findall(r'^\| `([^`]+)` \| `?([\w()]+)`? *\|', s6, re.M))

print('  states declared      :', ', '.join(sorted(states)))
print('  transitions parsed   :', len(trans))
print('  entry/exit declared  :', ', '.join(sorted(entry)))
print('  urls declared        :', len(urls))

check('states declared', len(states), 5)
rows = len(re.findall(r'^\| `\w+` \|', s52, re.M))
check('every row of the 5.2 table parsed as a transition', len(trans), rows)
check('5.2 has the transitions 5.1 needs', rows >= 8, True)

for a, b, trig, guard in trans:
    if a not in states:
        FAIL.append(('transition source is a declared state', a, 'one of %s' % states))
    if b not in states:
        FAIL.append(('transition target is a declared state', b, 'one of %s' % states))

for st in states - {'boot'}:
    if st not in entry:
        FAIL.append(('state %s declares entry AND exit' % st, 'missing', 'present'))
check('every non-boot state has entry+exit',
      len((states - {'boot'}) - entry) == 0, True)

reach = {'boot'}
changed = True
while changed:
    changed = False
    for a, b, _, _ in trans:
        if (a in reach or a == 'any') and b not in reach:
            reach.add(b)
            changed = True
check('every state reachable from boot', sorted(reach), sorted(states))

url_states = set()
for u, st in urls.items():
    url_states.add(st.split('(')[0])
check('states <-> urls, both directions', sorted(url_states), sorted(states - {'boot'}))

# ============================================================ PASS 3 - CONSISTENCY
print()
print('=' * 78)
print('PASS 3  CONSISTENCY - the document against itself')
print('=' * 78)

DOCS = ['xtix', 'oasis', 'eventer', 'medcoin', 'leadership', 'tech', 'final']

m = re.search(r'`id ∈ \{([^}]+)\}`', DOC)
from_51 = [x.strip() for x in m.group(1).split(',')] if m else []
check('§5.1 document ids', from_51, DOCS)

icons = re.findall(r'^\| ([A-Z]+) \| [^|]+ \| `(--\w+)` \| (\d) \|', section(8), re.M)
check('§8.2 icon table ids', [i[0].lower() for i in icons], DOCS)
check('§8.2 orders are 1..7', [int(i[2]) for i in icons], list(range(1, 8)))

mig = re.findall(r'`(\w+)` \((\d+) rules?\)|`(\w+)` \((\d+)\)', section(11))
mig_ids = [(a or c) for a, b, c, d in mig]
mig_cnt = [int(b or d) for a, b, c, d in mig]
check('§11.1 migration order ids', sorted(mig_ids), sorted(DOCS))
check('§11.1 order is easiest first', mig_cnt, sorted(mig_cnt))
for i, n in zip(mig_ids, mig_cnt):
    check('  §11.1 count for %s matches §1.2' % i, n, DOC_COUNTS[i])

case_colours = {i[0].lower(): i[1] for i in icons}
live = dict(re.findall(r'<section[^>]*id="(\w+)"[^>]*--fc:var\((--\w+)\)', PAGE))
for d in ['xtix', 'oasis', 'eventer', 'medcoin']:
    check('  §8.2 colour for %s matches the code' % d, case_colours.get(d), live.get(d))

tree = section(3)
for f in ['router.js', 'iso.js', 'build.py', 'manifest.json', 'copy.json', 'sprites.json']:
    if f not in tree:
        FAIL.append(('§3 tree declares %s' % f, 'absent', 'present'))
    if DOC.count(f) < 2:
        FAIL.append(('%s is referenced outside the tree' % f, DOC.count(f), '>= 2'))

fp = re.search(r'first paint[^|]*\| \*\*≤ (\d+) KB\*\* \| (\d+) KB', section(13))
if fp:
    check('§13 first-paint budget is below today', int(fp.group(1)) < int(fp.group(2)), True)
    check('§13 quotes today as the measured page size', int(fp.group(2)), len(PAGE.encode()) // 1024, 1)

check('§9 mobile tri count', '23,506' in section(9), True)
check('§9 desktop tri count', '61,081' in section(9), True)

phases = re.findall(r'^\| \*\*([A-J])\*\* \|', section(15), re.M)
check('§15 phases A..J complete', phases, list('ABCDEFGHIJ'))

print()
print('=' * 78)
print('%d checks passed, %d failed' % (len(OK), len(FAIL)))
if FAIL:
    print()
    for n, g, w in FAIL:
        print('  FAIL  %-46s got %-20s want %s' % (n, g, w))
print('=' * 78)
sys.exit(1 if FAIL else 0)
