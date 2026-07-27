# -*- coding: utf-8 -*-
# Feedback round: global ink tone + steel blue + $ + graph redesign + 9 visual bugs
import io, re

def swap_common(s):
    # 1. dark ink text -> matte charcoal (matches bg)
    s=s.replace("#0C0D10","#131417")
    s=s.replace("rgba(12,13,16,","rgba(19,20,23,")
    # 3. ice -> matte steel blue
    s=s.replace("#7CC4E8","#5E8FBF")
    s=s.replace("rgba(124,196,232,.12)","rgba(94,143,191,.14)")
    s=s.replace("rgba(124,196,232,.20)","rgba(94,143,191,.22)")
    return s

# ---------- from-zero graph (redesigned, shared geometry) ----------
def fromzero_svg(animated):
    parts=[]
    parts.append('<line x1="24" y1="66" x2="736" y2="66" stroke="#46494F" stroke-width="1.2"/>')
    x=40
    for i in range(3):
        parts.append('<rect x="%d" y="50" width="30" height="16" rx="2" fill="none" stroke="#46494F" stroke-width="1.2" stroke-dasharray="3 3"/>'%x)
        parts.append('<text x="%d" y="79" text-anchor="middle" font-size="6.4" letter-spacing="1" fill="#5A5B60">&#8709;</text>'%(x+15))
        x+=44
    parts.append('<line x1="%d" y1="10" x2="%d" y2="70" stroke="#46494F" stroke-width="1" stroke-dasharray="2 4"/>'%(x+4,x+4))
    x+=22
    heights=[16,21,26,31,36,41,46,51,56,60]
    for i,h in enumerate(heights):
        g_open=('<g class="bar0" style="--i:%d">'%i) if animated else '<g>'
        parts.append(g_open+
            '<rect x="%d" y="%d" width="30" height="%d" rx="1.5" fill="#2FB380"/>'%(x,66-h,h)+
            '<rect x="%d" y="%d" width="30" height="3" rx="1.5" fill="rgba(19,20,23,.4)"/>'%(x,66-h)+
            '</g>')
        parts.append('<text x="%d" y="79" text-anchor="middle" font-size="6.4" letter-spacing="1" fill="#5A5B60">%02d</text>'%(x+15,i+1))
        x+=46
    parts.append('<path d="M%d 66 l9 -5 v10 z" fill="#2FB380" transform="rotate(180 %d 66)"/>'%(742,742))
    return '<svg viewBox="0 0 760 86" preserveAspectRatio="xMidYMid meet" style="width:100%%;height:%s">%s</svg>'%(("auto" if animated else "78px"),"".join(parts))

# ============================================================ PDF
s=io.open("casebook.html",encoding="utf-8").read()
s=swap_common(s)

# bug1 (p03 rail): short vlab + lower start
s=s.replace('<div class="vlab">MASTER FILE &middot; OPERATING SYSTEM</div>','<div class="vlab">MASTER FILE &middot; 2026</div>')

# bug2a (p05 graph): replace old strip svg
m=re.search(r'<svg viewBox="0 0 660 64"[^>]*>.*?</svg>',s,flags=re.S)
assert m, "old fz svg"
s=s[:m.start()]+fromzero_svg(False)+s[m.end():]
# bug2b (strip leaking left past the rail)
s=s.replace(".p05 .fz{position:absolute;left:26px;right:26px;",".p05 .fz{position:absolute;left:64px;right:26px;",1)

# bug3 (p08 currency + gap)
s=s.replace('<div class="num"><b>&#8362;</b>2M</div>','<div class="num"><b>$</b>2M</div>',1)
s=s.replace(".p08 .stat .num b{color:var(--brass);font-weight:800}",".p08 .stat .num b{color:var(--brass);font-weight:800;margin-right:7px}",1)

# bug4 (p09 caption air from dashed arrow)
s=s.replace('<text x="300" y="3.5" text-anchor="middle" font-size="6.6"','<text x="300" y="-0.5" text-anchor="middle" font-size="6.6"',1)

# bug5 (p10 even check rows + paragraph rhythm)
CSS_P10="""
.p10b .bgrid{grid-auto-rows:1fr;align-items:center;gap:4px 14px}
.p10b .para3{font-size:10.5px;line-height:1.5}
"""
# bug6+7 (p11 even toolkit rows + sigq gap)
CSS_P11="""
.p11 .tools{grid-auto-rows:1fr;align-items:center;gap:5px 18px}
.p11 .sigq .who{margin-top:10px}
"""
# bug8 (p12 quote inside frame + arrowhead)
CSS_P12="""
.p12b .quote2{margin-top:5px}
.p12b .quote2 .qx{font-size:13.4px}
"""
# bug9 (p13 contact clip air)
CSS_P13="""
.p13 .card{margin-top:34px}
"""
s=s.replace("</style>",CSS_P10+CSS_P11+CSS_P12+CSS_P13+"</style>",1)

# p12 feedback arrowhead: proper upward triangle at path end
s=re.sub(r'<path d="M([\d.]+) 57 l-4 7 l8 \.5 z" fill="#8E8E93"/>',
         lambda m:'<path d="M%s 56 l-4.5 8.5 h9 z" fill="#8E8E93"/>'%m.group(1), s, count=1)

io.open("casebook.html","w",encoding="utf-8").write(s)
print("PDF round applied")

# ============================================================ SITE
t=io.open("site.html",encoding="utf-8").read()
t=swap_common(t)

# 2. stamp text (site only): not clickable-looking
t=t.replace('<div class="stampP">PULL TO OPEN &#8250;</div>','<div class="stampP">CONFIDENTIAL</div>',1)

# bug1 site (philosophy rail label)
t=t.replace('<div class="vlab">MASTER FILE &middot; OPERATING SYSTEM</div>','<div class="vlab">MASTER FILE &middot; 2026</div>')

# bug2a site graph redesign (animated)
m=re.search(r'<svg viewBox="0 0 740 70"[^>]*>.*?</svg>',t,flags=re.S)
assert m, "site fz svg"
t=t[:m.start()]+fromzero_svg(True)+t[m.end():]

# bug3 site currency
t=t.replace('<div class="bignum"><span class="cur">&#8362;</span><span class="cnt" data-n="2" data-suf="M">0M</span></div>',
'<div class="bignum"><span class="cur" style="margin-right:8px">$</span><span class="cnt" data-n="2" data-suf="M">0M</span></div>',1)

# bug5/6/7/8/9 site mirrors
CSS_SITE="""
#medcoin .list>*{min-height:0}
#leadership .tools{grid-auto-rows:1fr;align-items:center}
#leadership .sigq .who{margin-top:10px}
#tech .lessq{margin-top:14px}
#final .card{margin-top:38px}
"""
t=t.replace("</style>",CSS_SITE+"</style>",1)

# p12-equivalent site arrowhead
t=re.sub(r"<path d=\"M([\d.]+) 61 l-4\.4 7\.6 l8\.6 \.6 z\" fill=\"#8E8E93\"/>",
         lambda m:'<path d="M%s 60 l-4.5 9 h9 z" fill="#8E8E93"/>'%m.group(1), t, count=1)

io.open("site.html","w",encoding="utf-8").write(t)
print("SITE round applied:",len(t),"bytes")

# standalone rebuild
full=("<!doctype html>\n<html lang=\"en\">\n<head>\n<meta charset=\"utf-8\">\n"
"<meta name=\"viewport\" content=\"width=device-width,initial-scale=1\">\n"
"<meta name=\"color-scheme\" content=\"dark\">\n</head>\n<body>\n"+t+"\n</body>\n</html>")
io.open("site_standalone.html","w",encoding="utf-8").write(full)
print("standalone rebuilt")
