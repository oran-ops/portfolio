# -*- coding: utf-8 -*-
# Round 7c — pull p06's closing band fully inside the card; let p13 breathe again.
import io
p = 'casebook.html'
s = io.open(p, encoding='utf-8').read()
ADD = """
/* R7c */
.p06 .tech svg{width:158px!important;margin-top:2px!important}
.p06 .tech{padding:7px 12px}
.p06 .g1 svg{width:50px!important;height:50px!important}
.p06 .g1 .gl{line-height:1.5}
.p06 .band{margin-top:2px;padding-top:2px}
.p06 .band .lesson{margin-top:4px!important;padding-top:6px!important}
.p13 .pi{padding:6px 0 5px}
.p13 .vseal{margin-top:15px;padding:15px 26px 12px}
.p13 .fbot{margin-top:15px}
.p13 .card{margin-top:28px}
.p13 .closeline{margin-top:15px;padding-top:11px}
"""
k = s.rfind('</style>')
s = s[:k] + ADD + '\n' + s[k:]
io.open(p, 'w', encoding='utf-8', newline='').write(s)
print('round7c applied,', len(s.encode('utf-8')), 'bytes')
