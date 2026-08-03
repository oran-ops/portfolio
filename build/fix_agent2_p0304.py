# -*- coding: utf-8 -*-
# Agent-2 findings, chapter pages p03 / p04. PDF-only.
import io

c = io.open('casebook.html', encoding='utf-8').read()

CSS = """
/* ===== agent-2 pass: chapter pages p03 / p04 ===== */
/* p04-1 the XTIX card was 102px tall against 54px for the other three */
.p04 .tab.open .body{height:54px;padding:0}
.p04 .tab.open .dossier{left:26px;top:50%;transform:translateY(-50%)}
.p04 .tab.open .cat{top:50%;transform:translateY(-50%)}
/* p04-2 stack re-centred after the card equalisation */
.p04 .stack{top:250px}
/* p04-3 tabs on the document folder-tab token (15px wordmark / 8.5px label) */
.p04 .lip .nm{font-size:15px}
.p04 .lip .meta2{font-size:8.5px}
/* p04-4 card lines on the body token */
.p04 .dossier{font-size:12px}
/* p04-5 top-right meta on the document's right-flush line */
.p04 .meta{right:71px;margin-right:-0.2em}

/* p03-1 the card now fills the page instead of leaving a dead band above the accent */
.p03 .grid2{row-gap:46px}
.p03 .folder{padding-bottom:34px}
/* p03-2 step titles + descriptions on the same tokens as the p11 principle grid */
.p03 .sname{font-size:13.2px}
.p03 .sdesc{font-size:11.8px;line-height:1.4;min-height:33px}
/* p03-3 header row on the document line */
.p03 .hd{top:48px}
/* p03-4 tab label on the folder-tab token */
.p03 .tabrow .fl{font-size:8.5px}
/* p03-5 closing accent on the document's Fraunces closing-sentence token (p11/p13 = 13.6px) */
.p03 .qt .qx{font-size:13.6px}
"""
k = c.rfind('</style>')
c = c[:k] + CSS + '\n' + c[k:]
io.open('casebook.html', 'w', encoding='utf-8', newline='').write(c)
print('applied')
