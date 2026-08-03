# -*- coding: utf-8 -*-
# Agent-7 (cross-document) findings. PDF-only. System-level token normalisation.
import io, re

c = io.open('casebook.html', encoding='utf-8').read()

# --- micro-label floor: the rotated LEARNING LOOP label rendered at 5.5px ---
n = c.count('font-size="7.8" letter-spacing="1.3" fill="#CFD0D4" transform="rotate(90 204 97)"')
print('p06 LEARNING LOOP label found:', n)
c = c.replace('font-size="7.8" letter-spacing="1.3" fill="#CFD0D4" transform="rotate(90 204 97)"',
              'font-size="10" letter-spacing="1.3" fill="#CFD0D4" transform="rotate(90 204 97)"', 1)

CSS = """
/* ===== agent-7 pass: document-wide token normalisation ===== */
/* body-copy drift -> the 11.8px list token (highest-volume role in the deck) */
.p05 .frow{font-size:11.8px}
.p06 .tbl .vt{font-size:11.8px}
.p11 .lg{font-size:11.8px}
/* micro-label floor: one-off sizes collapsed onto the 8.0px step */
.p08 .stat .slip{font-size:8px}
.p08 .ringwrap svg text[font-size="8.5"]{font-size:8px}
/* p10 is the white-paper folder, so it has no colour accent — restore the
   two-tone zone-header device with the label grey instead */
.p10b .zr b{color:var(--lbl)}
/* p09: level the two column heads and put the right column on the 2-col norm */
.p09 .inner>div:last-child{padding-top:0}
.p09 .inner>div:last-child>.zr:first-child{margin-top:0}
/* p04 meta line on the header type token */
.p04 .meta{font-size:9.5px;top:41px}
"""
k = c.rfind('</style>')
c = c[:k] + CSS + '\n' + c[k:]
io.open('casebook.html', 'w', encoding='utf-8', newline='').write(c)
print('applied')
