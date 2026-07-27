# -*- coding: utf-8 -*-
import io
p="index.html"; s=io.open(p,encoding="utf-8").read()
EM="—"
a=s.index("<!-- ============ 04 ")
b=s.index("<!-- ============ 05 ")
seg=s[a:b]

# 1) remove header-right brand on page 4
seg=seg.replace('<div class="r">Oran Carmon '+EM+' Building Revenue Engines</div>','<div class="r"></div>')

# 2) remove rolebox block
rolebox=(
'      <div class="rolebox">\n'
'        <div class="rl">My Role</div>\n'
'        <div class="ri"><span class="ck">&#10003;</span> Builder</div>\n'
'        <div class="ri"><span class="ck">&#10003;</span> Strategist</div>\n'
'        <div class="ri"><span class="ck">&#10003;</span> Operator</div>\n'
'        <div class="ri"><span class="ck">&#10003;</span> Leader</div>\n'
'        <div class="ri"><span class="ck">&#10003;</span> AI Innovator</div>\n'
'      </div>\n'
)
assert rolebox in seg, "rolebox not found"
seg=seg.replace(rolebox,"")

# 3) remove signature block
sig=(
'    <div class="cs2-sig">\n'
'      <div class="sl">Signature Insight</div>\n'
'      <div class="stx">A commercial function shouldn\'t start with outreach. <span class="g">It should start with understanding.</span></div>\n'
'    </div>\n'
)
assert sig in seg, "sig not found"
seg=seg.replace(sig,"")

s=s[:a]+seg+s[b:]
io.open(p,"w",encoding="utf-8").write(s)
print("removed 3 elements from page 4")
