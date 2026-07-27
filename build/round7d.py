# -*- coding: utf-8 -*-
# Round 7d — pin every closing line to the very bottom edge of its card, identically.
import io
p = 'casebook.html'
s = io.open(p, encoding='utf-8').read()
ADD = """
/* R7d — closing line pinned to the bottom of the card on every page */
.casef .folder{position:relative}
.casef .folder>.lesson,.casef .folder .lesson,.casef .folder .lessq2,
.casef .folder .insight,.casef .folder .sigq,.casef .folder .quote2{
  position:absolute!important;left:26px;right:26px;bottom:13px;width:auto!important;
  margin:0!important;padding:9px 0 0!important;text-align:center;
  border:none!important;border-top:1px solid var(--fc,var(--emb))!important}
/* keep content clear of the pinned strip */
.p09 .inner,.p10b .inner,.p06 .band{padding-bottom:6px}
"""
k = s.rfind('</style>')
s = s[:k] + ADD + '\n' + s[k:]
io.open(p, 'w', encoding='utf-8', newline='').write(s)
print('round7d applied,', len(s.encode('utf-8')), 'bytes')
