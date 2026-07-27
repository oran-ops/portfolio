# -*- coding: utf-8 -*-
# Round 7e — tighten the pinned band and clear the last two collisions.
import io
p = 'casebook.html'
s = io.open(p, encoding='utf-8').read()
ADD = """
/* R7e */
.casef .folder .lesson,.casef .folder .lessq2,.casef .folder .insight,
.casef .folder .sigq,.casef .folder .quote2{bottom:11px;padding-top:7px!important}
.lesson .qx,.lessq2 .qx,.insight .qx,.sigq .qx,.quote2 .qx{font-size:11.8px!important;line-height:1.34}
.p09 .band{padding-top:6px}
.p09 .band .para{font-size:10.6px;line-height:1.42}
.p09 .z{margin-bottom:9px}
.p09 .et{padding:8px 12px}
.p09 .etr{margin-top:12px}
.p10b .band2{margin-top:2px;padding-top:3px}
.p10b .para3{font-size:10.2px;line-height:1.34}
.p10b .why{margin-top:5px;padding:8px 14px}
.p10b .tl2{margin-top:2px;padding-top:2px}
"""
k = s.rfind('</style>')
s = s[:k] + ADD + '\n' + s[k:]
io.open(p, 'w', encoding='utf-8', newline='').write(s)
print('round7e applied,', len(s.encode('utf-8')), 'bytes')
