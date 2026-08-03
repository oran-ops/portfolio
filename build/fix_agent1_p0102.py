# -*- coding: utf-8 -*-
# Agent-1 findings, cover + statement pages (p01/p02). PDF-only.
import io

c = io.open('casebook.html', encoding='utf-8').read()

CSS = """
/* ===== agent-1 pass: opening pair p01 / p02 ===== */
/* p02-1 page number on the document's right-flush line (was overhanging the margin) */
.p02b .pn{right:72px;margin-right:-0.14em}
/* p01-1 cover on the document's 72px frame (status block, breadcrumb, card) */
.p01b .idx{left:72px;font-size:10.5px}
.p01b .crumb{left:72px}
.p01b .folder{left:72px;right:72px}
/* p01-2 case-file tab row flush to the card's right edge, mirroring the name tab on the left */
.p01b .inner{right:0}
/* p01-3 cover tabs on the document's folder-tab token (15px wordmark / 8.5px label) */
.p01b .itab{gap:12px}
.p01b .itab .nm2{font-size:15px}
.p01b .itab .fl2{font-size:8.5px}
/* p01-4 tracked centred lines optically centred (trailing letter-space trimmed) */
.p01b .kick{margin-right:-0.5em}
.p01b .by{margin-right:-0.16em}
/* p02-2 spine labels centred inside their bars instead of top-inset */
.p02b .sp span{top:50%;transform:translate(-50%,-50%)}
"""
k = c.rfind('</style>')
c = c[:k] + CSS + '\n' + c[k:]
io.open('casebook.html', 'w', encoding='utf-8', newline='').write(c)
print('applied')
