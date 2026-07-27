# -*- coding: utf-8 -*-
# PDF parity with the doc-round site changes + remove $2M circle from site.
import io, re

# ================= PDF =================
s = io.open("casebook.html", encoding="utf-8").read()

def kill(pattern, desc, count=1, flags=0):
    global s
    s2, n = re.subn(pattern, "", s, count=count, flags=flags)
    assert n == count, "%s: %d/%d" % (desc, n, count)
    s = s2
    print("pdf removed:", desc)

# 1. cover barcode block
kill(r'<div class="barc">\s*<svg viewBox="0 0 62 30".*?</svg>\s*<div class="yr">2026</div>\s*</div>\s*', "cover barcode", flags=re.S)

# 2. lip meta (keep Oran Carmon)
OLD = '<span class="fl">MASTER FILE &middot; N&deg; 2026-04</span>'
assert OLD in s
s = s.replace(OLD, "", 1)
print("pdf removed: lip meta")

# 3. PULL TO OPEN stamp
kill(r'<div class="stamp">PULL TO OPEN &#8250;</div>\s*', "PULL TO OPEN stamp")

# 4. divider rule
kill(r'<div class="rule"><span class="ln"></span><span class="d"></span><span class="ln"></span></div>\s*', "cover divider")

# 5. BY suffix
OLD = 'BY <b>ORAN CARMON</b> &nbsp;&middot;&nbsp; COMMERCIAL SYSTEMS BUILDER'
assert OLD in s
s = s.replace(OLD, 'BY <b>ORAN CARMON</b>', 1)
print("pdf removed: BY suffix")

# 6. tagl practical-guide line
kill(r'<div class="tagl">A PRACTICAL GUIDE[^<]*</div>\s*', "tagl", flags=re.S)

# 7. statement copy
OLD = "Most companies don't need better salespeople."
assert OLD in s
s = s.replace(OLD, "Most companies don't need more AI tools.", 1)
OLD = "They need better commercial decisions."
assert OLD in s
s = s.replace(OLD, "They need leaders who turn AI into growth.", 1)
print("pdf: statement rewritten")

# 8. p13 CASE CLOSED stamp
kill(r'<div class="stamp2">CASE CLOSED</div>\s*', "p13 CASE CLOSED")

io.open("casebook.html", "w", encoding="utf-8").write(s)
print("PDF PARITY DONE")

# ================= SITE =================
t = io.open("site.html", encoding="utf-8").read()
OLD = """(function(){
  var o2=null;
  [].slice.call(document.querySelectorAll('#oasis .bignum,#oasis .num')).some(function(b){
    if(b.textContent.indexOf('2M')>-1){o2=b;return true}return false;});
  circleStat(o2,'#E0A458');
})();"""
assert OLD in t, "o2 circle block"
t = t.replace(OLD, "", 1)
print("site: $2M circle removed")
io.open("site.html", "w", encoding="utf-8").write(t)
head = ('<!doctype html>\n<html lang="en">\n<head>\n<meta charset="utf-8">\n'
        '<meta name="viewport" content="width=device-width,initial-scale=1">\n'
        '<meta name="color-scheme" content="dark">\n</head>\n<body>\n')
io.open("site_standalone.html", "w", encoding="utf-8").write(head + t + "\n</body>\n</html>")
print("ALL DONE")
