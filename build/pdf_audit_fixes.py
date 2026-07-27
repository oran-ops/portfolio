# -*- coding: utf-8 -*-
# 10 fixes from the PDF visual audit
import io,re
s=io.open("casebook.html",encoding="utf-8").read()

# ---- 1+2: p10/p12 bottom overflow (append overrides = last wins) ----
CSS="""
.p10b .band2{margin-top:5px;padding-top:6px}
.p10b .tl2{margin-top:7px;padding-top:6px}
.p10b .para3{font-size:10.2px;line-height:1.42}
.p10b .lessq2 .qx{font-size:12.6px}
.p10b .lessq2 .who{margin-top:4px}
.p12b .bot2{margin-top:4px;padding-top:7px}
.p12b .quote2{margin-top:3px}
.p12b .quote2 .qx{font-size:13px;line-height:1.4}
.p06 .band{margin-top:10px;padding-top:10px}
.p06 .band .dash{font-size:10.4px}
"""
s=s.replace("</style>",CSS+"</style>",1)

# ---- 3(p06 handled in CSS) ----

# ---- 4+5+8: convergence svg (p09) ----
i=s.find('CUSTOMER INSIGHT'); a=s.rfind('<svg',0,i); b=s.find('</svg>',i)+6
svg=s[a:b]; orig=svg
assert svg.count('font-size="7"')==5
svg=svg.replace('font-size="7"','font-size="8.5"')
assert svg.count('font-size="6.6"')==2
svg=svg.replace('font-size="6.6"','font-size="8"')
svg=svg.replace('viewBox="0 -8 560 176"','viewBox="0 -11 560 179"',1)
assert svg.count('336 80"')==5
svg=svg.replace('336 80"','358 80"')
assert '<path d="M340 80 l-8 -4.5 v9 z" fill="#5E8FBF"/>' in svg
svg=svg.replace('<path d="M340 80 l-8 -4.5 v9 z" fill="#5E8FBF"/>','<path d="M361 80 l-8 -4.5 v9 z" fill="#5E8FBF"/>',1)
s=s[:a]+svg+s[b:]
print("p09 svg fixed")

# ---- 5: p05 from-zero ticks ----
i=s.find('viewBox="0 0 760 86"')
assert i>-1
a=s.rfind('<svg',0,i+10); b=s.find('</svg>',i)+6
fz=s[a:b]
n1=fz.count('font-size="6.4"')
fz=fz.replace('font-size="6.4"','font-size="8"')
n2=fz.count('fill="#5A5B60"')
fz=fz.replace('fill="#5A5B60"','fill="#8E8E93"')
s=s[:a]+fz+s[b:]
print("p05 ticks bumped:",n1,"labels,",n2,"fills")

# ---- 5b: GAP index labels ----
OLD=".p05 .frow .st2{margin-left:auto;font-family:'JetBrains Mono',monospace;font-size:7px;letter-spacing:.12em;color:var(--dim)}"
NEW=".p05 .frow .st2{margin-left:auto;font-family:'JetBrains Mono',monospace;font-size:8px;letter-spacing:.12em;color:var(--mut)}"
assert OLD in s; s=s.replace(OLD,NEW,1)

# ---- 5c: LEARNING LOOP rotated caption ----
OLD='<text x="204" y="97" text-anchor="middle" font-size="6.9" letter-spacing="1.6" fill="#A6A7AC" transform="rotate(90 204 97)">LEARNING LOOP</text>'
NEW='<text x="204" y="97" text-anchor="middle" font-size="8.6" letter-spacing="1.6" fill="#A6A7AC" transform="rotate(90 204 97)">LEARNING LOOP</text>'
assert OLD in s; s=s.replace(OLD,NEW,1)

# ---- 6: p11 widow ----
OLD="depend on you.</b>"
assert OLD in s; s=s.replace(OLD,"depend on&nbsp;you.</b>",1)

# ---- 7: p12 runt ----
OLD="PEOPLE SHOULD MAKE DECISIONS."
assert OLD in s; s=s.replace(OLD,"PEOPLE SHOULD MAKE&nbsp;DECISIONS.",1)

# ---- 9: cover hole spacing (first folder holes on p01) ----
OLD='<span class="hole" style="top:74px"></span><span class="hole" style="top:120px"></span>'
assert OLD in s; s=s.replace(OLD,'<span class="hole" style="top:74px"></span><span class="hole" style="top:108px"></span>',1)

# ---- 10: FOUNDER stamp angle ----
OLD='.p10b .stamp{position:absolute;top:-14px;right:14px;transform:rotate(-7deg);'
assert OLD in s; s=s.replace(OLD,'.p10b .stamp{position:absolute;top:-14px;right:14px;transform:rotate(-6deg);',1)

io.open("casebook.html","w",encoding="utf-8").write(s)
print("ALL 10 PDF FIXES APPLIED")
