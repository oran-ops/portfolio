# -*- coding: utf-8 -*-
# User doc round: 12 changes from the annotated Word document (site only).
import io, re
s = io.open("site.html", encoding="utf-8").read()

def kill(pattern, desc, count=1, flags=0):
    global s
    s2, n = re.subn(pattern, "", s, count=count, flags=flags)
    assert n == count, "%s: expected %d got %d" % (desc, count, n)
    s = s2
    print("removed:", desc, "x%d" % n)

# 1. PROCESSING -> GROWING (boot line)
OLD = 'PROCESSING<span class="dots">'
assert OLD in s
s = s.replace(OLD, 'GROWING<span class="dots">', 1)
print("boot: GROWING")

# 2. clearance popup deleted (LOG line stays)
OLD = """function showClearance(){
  clearanceEl.classList.add('on');
  if(window.__archLog)window.__archLog('REVIEWER ACCESS GRANTED · CLEARANCE: COMMERCIAL',3400);
  setTimeout(function(){clearanceEl.classList.remove('on')},3000);
}"""
NEW = """function showClearance(){
  if(window.__archLog)window.__archLog('REVIEWER ACCESS GRANTED · CLEARANCE: COMMERCIAL',3400);
}"""
assert OLD in s
s = s.replace(OLD, NEW, 1)
print("clearance popup removed (log kept)")

# 3. hero mid divider (— ◆ —)
i = s.find('id="hero"')
seg_end = s.find('</section>', i)
m = re.search(r'<div class="rule"[^>]*>.*?</div>\s*', s[i:seg_end], flags=re.S)
assert m, "hero rule"
s = s[:i+m.start()] + s[i+m.end():]
print("hero divider removed")

# 4a. lip meta "MASTER FILE · N° 2026-04"
m = re.search(r'<span[^>]*>MASTER FILE &middot; N&deg; 2026-04</span>', s)
assert m, "lip meta"
s = s[:m.start()] + s[m.end():]
print("lip meta removed")

# 4b. "· COMMERCIAL SYSTEMS BUILDER" after BY ORAN CARMON (keep the BY part)
OLDB = 'BY <b>ORAN CARMON</b> &nbsp;&middot;&nbsp; COMMERCIAL SYSTEMS BUILDER'
assert OLDB in s, "by line"
s = s.replace(OLDB, 'BY <b>ORAN CARMON</b>', 1)
print("BY-line suffix removed")

# 4c. kick line
kill(r'<div class="tagl">A PRACTICAL GUIDE[^<]*</div>\s*', "tagl line", flags=re.S)

# 5. hero CONFIDENTIAL stamp
kill(r'<div class="stampP">CONFIDENTIAL</div>\s*', "hero CONFIDENTIAL")

# 6. statement copy — AI x human
OLD = "Most companies don't need better salespeople."
assert OLD in s
s = s.replace(OLD, "Most companies don't need more AI tools.", 1)
OLD = "They need better commercial decisions."
assert OLD in s
s = s.replace(OLD, "They need leaders who turn AI into growth.", 1)
print("statement rewritten")

# 7. theaters: remove barcode + CONFIDENTIAL on all 4 covers
kill(r'<div class="oc-barc" aria-hidden="true"><i>C-0\d</i></div>\s*', "oc-barc x4", count=4, flags=re.S)
kill(r'<div class="oc-conf">CONFIDENTIAL</div>\s*', "oc-conf x4", count=4)

# 8. field-report gap before 03 MY APPROACH
s = s.replace("</style>", "#xtix .reality{margin-bottom:18px}\n</style>", 1)
print("field-report gap added")

# 9. remove detective circle on EUR 3M+ (keep $2M)
OLD = """  var x3=null;
  [].slice.call(document.querySelectorAll('#xtix .bignum')).some(function(b){
    if(b.textContent.indexOf('3')>-1){x3=b;return true}return false;});
  circleStat(x3,'#2FB380');
"""
assert OLD in s
s = s.replace(OLD, "", 1)
print("EUR3M circle removed")

# 10. eventer dashed loop: draw once with the others, then static (kill crawl)
i = s.find('CUSTOMER INSIGHT')
a = s.rfind('<svg', 0, i); b = s.find('</svg>', i)
svg = s[a:b]
assert 'class="crawlp"' in svg
svg = svg.replace('<path class="crawlp"', '<path', 1)
s = s[:a] + svg + s[b:]
print("eventer loop: crawl removed (draws once)")

# 11. medcoin solid line fully static (no scrub-draw, no play)
j = s.find('FOUNDED')
a2 = s.rfind('<svg', 0, j); b2 = s.find('</svg>', j)
svg2 = s[a2:b2]
assert 'class="pdraw"' in svg2
svg2 = svg2.replace('<line class="pdraw" pathLength="1"', '<line', 1)
s = s[:a2] + svg2 + s[b2:]
OLD = """  lines.forEach(function(l){l.setAttribute('pathLength','1');l.style.strokeDasharray='1';l.style.strokeDashoffset='1';l.style.transition='none';});
"""
assert OLD in s
s = s.replace(OLD, "", 1)
OLD = """  P.lines.forEach(function(l){l.style.transition='stroke-dashoffset 1.2s cubic-bezier(.5,0,.3,1) .15s';l.style.strokeDashoffset='0';});
"""
assert OLD in s
s = s.replace(OLD, "", 1)
print("medcoin solid line static")

# 12. CASE CLOSED stamp removed (lock/ceremony are null-safe)
m = re.search(r'<div class="[a-z0-9 ]+" id="ccstamp">CASE CLOSED</div>\s*', s)
assert m, "ccstamp"
s = s[:m.start()] + s[m.end():]
print("CASE CLOSED removed")

io.open("site.html", "w", encoding="utf-8").write(s)
head = ('<!doctype html>\n<html lang="en">\n<head>\n<meta charset="utf-8">\n'
        '<meta name="viewport" content="width=device-width,initial-scale=1">\n'
        '<meta name="color-scheme" content="dark">\n</head>\n<body>\n')
io.open("site_standalone.html", "w", encoding="utf-8").write(head + s + "\n</body>\n</html>")
print("DOC ROUND DONE:", len(s))
