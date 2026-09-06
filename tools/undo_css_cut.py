# -*- coding: utf-8 -*-
"""Put one section's CSS rules back into the monolith.

    python tools/undo_css_cut.py tech

Needed because the rules are stored verbatim: substituting them back restores the monolith
exactly as it was before the cut, including anything the cut should not have taken with it.
That is the property that makes a bad cut recoverable rather than a reconstruction job.
"""
import io
import os
import re
import sys

sys.stdout.reconfigure(encoding='utf-8', errors='replace')
HERE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
MONO = os.path.join(HERE, 'src', '_monolith.html')

sid = sys.argv[1] if len(sys.argv) > 1 else None
path = os.path.join(HERE, 'src', 'doc', '%s.css' % sid)
if not sid or not os.path.exists(path):
    raise SystemExit('usage: undo_css_cut.py <section-id>  (needs src/doc/<id>.css)')

s = io.open(MONO, encoding='utf-8').read()
before = len(re.findall(r'/\*D:\w+:\d+\*/', s))

chunks = re.split(r'/\*--(\d+)--\*/', io.open(path, encoding='utf-8').read())
n = 0
for idx, rule in zip(chunks[1::2], chunks[2::2]):
    mark = '/*D:%s:%s*/' % (sid, idx)
    if mark not in s:
        raise SystemExit('marker %s not in the monolith' % mark)
    s = s.replace(mark, rule, 1)
    n += 1

io.open(MONO, 'w', encoding='utf-8', newline='').write(s)
os.remove(path)
after = len(re.findall(r'/\*D:\w+:\d+\*/', s))
print('restored %d rules for %s; removed src/doc/%s.css' % (n, sid, sid))
print('markers in the monolith: %d -> %d' % (before, after))
