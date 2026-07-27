# -*- coding: utf-8 -*-
# Round 7h — site: the per-section quote rules are id-scoped, so the closing band
# needs id-scoped rules of its own to win; plus the leftover reveal rule and two
# spacing fixes in the closing.
import io
p = 'site.html'
s = io.open(p, encoding='utf-8').read()
ADD = """
/* R7h — closing band typography (id-scoped to beat the per-section rules) */
#xtix .lessq .qx,#oasis .lessq .qx,#oasis .insight .qx,#eventer .lessq .qx,
#medcoin .lessq .qx,#leadership .sigq .qx,#tech .lessq .qx{
  font-size:19px!important;line-height:1.5!important;color:var(--ink)}
#xtix .lessq,#oasis .lessq,#oasis .insight,#eventer .lessq,
#medcoin .lessq,#leadership .sigq,#tech .lessq{padding:16px 0 0!important;margin-top:30px!important}
.lessq::before,.insight::before,.sigq::before{display:none!important}
@media (max-width:680px){
  #xtix .lessq .qx,#oasis .lessq .qx,#oasis .insight .qx,#eventer .lessq .qx,
  #medcoin .lessq .qx,#leadership .sigq .qx,#tech .lessq .qx{font-size:15px!important}
}
/* R7h — closing: first row aligned, contact lip clear of its label, seal on one line */
#final .pgrid .pi:first-child,#final .pgrid .pi:nth-child(2){padding-top:0}
#final .card{margin-top:42px}
#final .vseal .vq{max-width:940px;font-size:clamp(19px,2.3vw,25px)}
"""
k = s.rfind('</style>')
s = s[:k] + ADD + '\n' + s[k:]
io.open(p, 'w', encoding='utf-8', newline='').write(s)

head = ('<!doctype html>\n<html lang="en">\n<head>\n<meta charset="utf-8">\n'
        '<meta name="viewport" content="width=device-width,initial-scale=1">\n'
        '<meta name="color-scheme" content="dark">\n</head>\n<body>\n')
io.open('site_standalone.html', 'w', encoding='utf-8', newline='').write(head + s + '\n</body>\n</html>')
print('round7h applied,', len(s.encode('utf-8')), 'bytes')
