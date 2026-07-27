# -*- coding: utf-8 -*-
# 11-agent audit: mechanical fixes (contrast, spacing, alignment, sizes, elements).
# Each op independent; logs OK/SKIP. PDF first; shared subset mirrored to site.
import io, re

LOG = []
def op(name, fn):
    global s
    try:
        s2 = fn(s)
        if s2 is None or s2 == s:
            LOG.append(("SKIP", name))
        else:
            s = s2
            LOG.append(("OK", name))
    except Exception as e:
        LOG.append(("ERR", name + " :: " + str(e)[:80]))

def rep1(old, new):
    def f(s):
        return s.replace(old, new, 1) if old in s else None
    return f

def repn(old, new, n=None):
    def f(s):
        if old not in s: return None
        return s.replace(old, new) if n is None else s.replace(old, new, n)
    return f

def css(add):
    def f(s):
        k = s.rfind("</style>")
        return s[:k] + add + "\n" + s[k:]
    return f

# ============================================================ CASEBOOK
s = io.open("casebook.html", encoding="utf-8").read()

# ---- A. CONTRAST ----
op("A1 dim token -> muted", rep1("--dim:#606167", "--dim:#8E8E93"))
for a in [".55)", ".6)", ".62)", ".72)", ".75)"]:
    op("A2 ink alpha %s -> full" % a, repn("rgba(25,26,31,%s" % a.rstrip(")") + ")", "#191A1F"))
op("A2b cover fl2 white .55 -> .8", rep1("color:rgba(242,241,237,.55)", "color:rgba(242,241,237,.8)"))
op("A5 GAP st2 -> lbl", rep1(".p05 .frow .st2{margin-left:auto;font-family:'JetBrains Mono',monospace;font-size:8px;letter-spacing:.12em;color:var(--mut)}",
                             ".p05 .frow .st2{margin-left:auto;font-family:'JetBrains Mono',monospace;font-size:8px;letter-spacing:.12em;color:var(--lbl)}"))
def a6(s):
    i = s.find('CUSTOMER INSIGHT')
    a = s.rfind('<svg', 0, i); b = s.find('</svg>', i)
    svg = s[a:b]
    n = svg.count('fill="#8E8E93"')
    if not n: return None
    svg = svg.replace('fill="#8E8E93"', 'fill="#A6A7AC"')
    return s[:a] + svg + s[b:]
op("A6 p09 dept/caption fills -> lbl", a6)
def a8a(s):  # p08 radial spoke labels
    i = s.find('WORKED CLOSELY WITH')
    a = s.rfind('<svg', 0, i)
    if a < 0: return None
    b = s.find('</svg>', a)
    svg = s[a:b]
    if 'fill="#8E8E93"' not in svg: return None
    svg = svg.replace('fill="#8E8E93"', 'fill="#A6A7AC"')
    return s[:a] + svg + s[b:]
op("A8a p08 spoke labels -> lbl", a8a)
def a8b(s):  # p10 timeline labels
    j = s.find('FOUNDED')
    a = s.rfind('<svg', 0, j); b = s.find('</svg>', j)
    svg = s[a:b]
    if 'fill="#8E8E93"' not in svg: return None
    svg = svg.replace('fill="#8E8E93"', 'fill="#A6A7AC"')
    return s[:a] + svg + s[b:]
op("A8b p10 timeline labels -> lbl", a8b)
op("A7 p10 why body -> lbl", rep1(".p10b .why .wt{font-size:10.6px;line-height:1.5;color:var(--mut)}",
                                   ".p10b .why .wt{font-size:10.6px;line-height:1.5;color:var(--lbl)}"))
op("A4 p13 chips bigger+lbl", css(".p13 .ich span{font-size:9px;padding:5px 10px;color:var(--lbl)}"))

# ---- B/C. TYPE + SPACING ----
op("B1 p10 sizes up + reclaim", css(
 ".p10b .para3{font-size:10.7px;line-height:1.38}\n"
 ".p10b .list .lg{font-size:10.9px}\n"
 ".p10b .lg2 .n2{font-size:7.5px}\n"
 ".p10b .tl2{margin-top:3px;padding-top:3px}\n"
 ".p10b .z{margin-bottom:7px}\n"
 ".p10b .why{margin-top:6px}"))
op("B2+C1 p06 bullets up + band shave (quote in-card)", css(
 ".p06 .band{margin-top:3px;padding-top:3px}\n"
 ".p06 .band .dash{font-size:10.8px}\n"
 ".p06 .band .lesson{margin-top:0}\n"
 ".p06 .lesson .qx{line-height:1.38}\n"
 ".p06 .lesson .who{margin-top:3px}"))
op("B3 p07 quote to family size", rep1(".p07 .insight .qx{font-size:18.5px}", ".p07 .insight .qx{font-size:17.5px}"))
op("B3b p10/p12 boxed quotes to 13.8px + C2 p12 clearance", css(
 ".p10b .lessq2 .qx{font-size:13.8px}\n"
 ".p12b .quote2 .qx{font-size:13.8px;line-height:1.36}\n"
 ".p12b .quote2{margin-top:0}\n"
 ".p12b .bot2{margin-top:3px;padding-top:4px}"))
op("B4 p07 list to 11.8px", css(".p07 .list .lg{font-size:11.8px}"))
op("C3-5 wrap-safe list rows", css(
 ".p10b .list{grid-auto-rows:auto;row-gap:6px}\n"
 ".p10b .list .lg{height:auto;align-items:flex-start}\n"
 ".p11 .tools{grid-auto-rows:auto;align-items:start;gap:8px 18px}\n"
 ".p13 .pgrid{grid-auto-rows:auto;row-gap:13px}"))
op("C9 quote inset unify 18px", css(".p10b .lessq2{padding-left:18px}\n.p12b .quote2{padding-left:18px}"))
op("G3 p03 signature block up", css(".p03 .sig{margin-bottom:14px}"))

# ---- D. ALIGNMENT ----
op("D2 p09 curves 358->361", repn("361 80\"", "361 80\"", 0) if False else repn("358 80\"", "361 80\""))
op("D2b p09 arrow tip 361->364", rep1('<path d="M361 80 l-8 -4.5 v9 z" fill="#5E8FBF"/>', '<path d="M364 80 l-8 -4.5 v9 z" fill="#5E8FBF"/>'))
op("D3 p02 chip to global slot", rep1(".p02b .tok{position:absolute;top:40px;right:64px;", ".p02b .tok{position:absolute;top:49px;right:73px;"))
op("D5 cover tab flush", rep1(".p01b .flip{position:absolute;top:156px;left:63px;", ".p01b .flip{position:absolute;top:156px;left:64px;"))
def d6(s):  # p05 placeholders pitch 44->46 + bar10 ramp
    i = s.find('viewBox="0 0 760 86"')
    if i < 0: return None
    a = s.rfind('<svg', 0, i); b = s.find('</svg>', i)
    svg = s[a:b]; orig = svg
    svg = svg.replace('<rect x="84" y="50"', '<rect x="86" y="50"')
    svg = svg.replace('<rect x="128" y="50"', '<rect x="132" y="50"')
    svg = svg.replace('<text x="99" y="79"', '<text x="101" y="79"')
    svg = svg.replace('<text x="143" y="79"', '<text x="147" y="79"')
    return s[:a] + svg + s[b:] if svg != orig else None
op("D6 p05 placeholder pitch", d6)
op("D8 p06/p10 table label flush", css(".p10b .outs .k{padding-left:0}\n.p06 .mrow td:first-child{padding-left:0}"))

# ---- E/F/G. ELEMENTS ----
def e5(s):  # FOUNDER stamp -> standardized FOUNDED 2018 rstamp
    old = '<div class="stamp">FOUNDER</div>\n          '
    if old not in s:
        old = '<div class="stamp">FOUNDER</div>'
        if old not in s: return None
    s = s.replace(old, "", 1)
    # insert rstamp mirroring p05 slot: right after p10 tabrow close
    i = s.find('id="p10"')
    if i < 0:
        i = s.find('class="page p10b"')
    j = s.find('</div>', s.find('<div class="tabrow"', i))
    if j < 0: return None
    j = s.find('>', j) + 0
    ins = s.find('</div>', s.find('<div class="tabrow"', i)) + len('</div>')
    return s[:ins] + '<div class="rstamp">FOUNDED &middot; 2018</div>' + s[ins:]
op("E5 FOUNDED-2018 stamp standardized", e5)
op("E10 cover holes lane", rep1('.p01b .hole{position:absolute;left:26px;', '.p01b .hole{position:absolute;left:24px;'))
def f2(s):  # cover XTIX tab plain anatomy like siblings
    old = '<div class="itab" style="background:#191A1F;height:26px">'
    if old not in s: return None
    return s.replace(old, '<div class="itab" style="background:#191A1F;height:26px;border-radius:8px 8px 0 0">', 1)
op("F2 cover XTIX tab plain", f2)
def f4(s):  # p10 solid line ends at final node
    old = '<line x1="26" y1="26" x2="912" y2="26" stroke="#F2F1ED" stroke-width="1.3"/>'
    if old not in s: return None
    return s.replace(old, '<line x1="26" y1="26" x2="906" y2="26" stroke="#F2F1ED" stroke-width="1.3"/>', 1)
op("F4 p10 baseline ends at node", f4)
def f5(s):  # p12 feedback arrowhead angle
    old = '<path d="M186.0 56 l-4.5 8.5 h9 z" fill="#8E8E93"/>'
    if old not in s: return None
    return s.replace(old, '<path d="M186.0 56 l-4.5 8.5 h9 z" fill="#8E8E93" transform="rotate(26 186 60.2)"/>', 1)
op("F5 p12 fb arrowhead rotate", f5)

io.open("casebook.html", "w", encoding="utf-8").write(s)
print("== CASEBOOK ==")
for st, nm in LOG: print(" %-4s %s" % (st, nm))

# ============================================================ SITE (shared subset)
LOG = []
s = io.open("site.html", encoding="utf-8").read()
op("S dim token -> muted", rep1("--dim:#606167", "--dim:#8E8E93"))
for a in [".55)", ".6)", ".62)", ".72)", ".75)"]:
    def mk(aa):
        def f(s):
            tgt = "rgba(25,26,31,%s" % aa.rstrip(")") + ")"
            # only color: usages; veil/fills use .55 too on site -> guard: skip .55 fills by replacing only 'color:rgba'
            old = "color:" + tgt
            if old not in s: return None
            return s.replace(old, "color:#191A1F")
        return f
    op("S ink alpha %s (color only)" % a, mk(a))
op("S GAP st2 -> lbl", rep1("font-size:8px;letter-spacing:.12em;color:var(--mut)}", "font-size:8px;letter-spacing:.12em;color:var(--lbl)}"))
def sa6(s):
    i = s.find('CUSTOMER INSIGHT')
    a = s.rfind('<svg', 0, i); b = s.find('</svg>', i)
    svg = s[a:b]
    if 'fill="#8E8E93"' not in svg: return None
    svg = svg.replace('fill="#8E8E93"', 'fill="#A6A7AC"')
    return s[:a] + svg + s[b:]
op("S p09-equiv dept fills -> lbl", sa6)
def sa8(s):
    j = s.find('FOUNDED')
    if j < 0: return None
    a = s.rfind('<svg', 0, j); b = s.find('</svg>', j)
    svg = s[a:b]
    if 'fill="#8E8E93"' not in svg: return None
    svg = svg.replace('fill="#8E8E93"', 'fill="#A6A7AC"')
    return s[:a] + svg + s[b:]
op("S timeline labels -> lbl", sa8)
def sd2(s):
    if '358 80"' not in s: return None
    s = s.replace('358 80"', '361 80"')
    s = s.replace('<path d="M361 80 l-8 -4.5 v9 z" fill="#5E8FBF"/>', '<path d="M364 80 l-8 -4.5 v9 z" fill="#5E8FBF"/>', 1)
    return s
op("S convergence curves+tip", sd2)
def sf4(s):
    old = '<line x1="26" y1="26" x2="912" y2="26" stroke="#F2F1ED" stroke-width="1.3"/>'
    if old not in s: return None
    return s.replace(old, '<line x1="26" y1="26" x2="906" y2="26" stroke="#F2F1ED" stroke-width="1.3"/>', 1)
op("S timeline baseline end", sf4)
def sf5(s):
    m = re.search(r'<path d="M([0-9.]+) 60 l-4\.5 9 h9 z" fill="#8E8E93"/>', s)
    if not m: return None
    x = m.group(1)
    return s.replace(m.group(0), '<path d="M%s 60 l-4.5 9 h9 z" fill="#8E8E93" transform="rotate(26 %s 64.5)"/>' % (x, x), 1)
op("S fb arrowhead rotate", sf5)
op("S industries chips lbl", css("#final .ich span{color:var(--lbl)}\n#final .chips .chip{color:var(--lbl)}"))

io.open("site.html", "w", encoding="utf-8").write(s)
head = ('<!doctype html>\n<html lang="en">\n<head>\n<meta charset="utf-8">\n'
        '<meta name="viewport" content="width=device-width,initial-scale=1">\n'
        '<meta name="color-scheme" content="dark">\n</head>\n<body>\n')
io.open("site_standalone.html", "w", encoding="utf-8").write(head + s + "\n</body>\n</html>")
print("== SITE ==")
for st, nm in LOG: print(" %-4s %s" % (st, nm))
print("DONE")
