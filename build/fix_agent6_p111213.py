# -*- coding: utf-8 -*-
# Agent-6 findings, p11 / p12 / p13. PDF-only.
import io

c = io.open('casebook.html', encoding='utf-8').read()

CSS = """
/* ===== agent-6 pass: closing trio p11 / p12 / p13 ===== */
/* p11-1 signature band starts on the content band, not in the left gutter */
.p11 .sigq{margin-left:38px}
/* p11-2 dotted divider on the true gutter centre of the 59/41 split */
.p11 .cols::before{left:calc(59% - 3px)}
/* p11-3 principle descriptions on the document body token */
.p11 .pr .ds{font-size:11.8px;line-height:1.4}
/* p11-4 the closing signature sentence matches the p13 seal sentence
   (it was being shrunk by an !important rule written for the case-page
   closers, all of which were removed earlier in this round) */
.p11 .sigq .qx{font-size:13.6px!important;line-height:1.4}
/* p12-1 the green info chip hugs its text again (it was stretched by the
   flex-column card added in the page-12 stage) */
.p12b .intb{align-self:flex-start}
/* p12-2 checklist on the document body token */
.p12b .lg{font-size:11.8px}
/* p12-3 + p13-1 full-width elements reach the document ink edge */
.p12b .folder,.p13 .folder{padding-right:26px}
/* p13-2 numerals share one axis with their connector stub and diamond */
.p13 .node{align-items:center}
/* p13-3 spine lines on the document body token */
.p13 .node .nt{font-size:11.8px;line-height:1.36}
"""
k = c.rfind('</style>')
c = c[:k] + CSS + '\n' + c[k:]
io.open('casebook.html', 'w', encoding='utf-8', newline='').write(c)
print('applied')
