# -*- coding: utf-8 -*-
# User-approved declutter + finale redesign. Independent ops, logged.
import io, re

def run(path, ops, standalone=False):
    s = io.open(path, encoding="utf-8").read()
    print("==", path)
    for name, fn in ops:
        try:
            s2 = fn(s)
            if s2 is None or s2 == s:
                print(" SKIP", name)
            else:
                s = s2
                print(" OK  ", name)
        except Exception as e:
            print(" ERR ", name, str(e)[:90])
    io.open(path, "w", encoding="utf-8").write(s)
    if standalone:
        head = ('<!doctype html>\n<html lang="en">\n<head>\n<meta charset="utf-8">\n'
                '<meta name="viewport" content="width=device-width,initial-scale=1">\n'
                '<meta name="color-scheme" content="dark">\n</head>\n<body>\n')
        io.open("site_standalone.html", "w", encoding="utf-8").write(head + s + "\n</body>\n</html>")
    return s

def sub(pat, rep, desc_count=None, flags=0):
    def f(s):
        s2, n = re.subn(pat, rep, s, flags=flags)
        return s2 if n else None
    return f

def css_end(add):
    def f(s):
        k = s.rfind("</style>")
        return s[:k] + add + "\n" + s[k:]
    return f

# ---------------- shared ops ----------------
def logn_gone(s):
    s2, n1 = re.subn(r'<span class="n">LOG\.\d\d</span>', '', s)
    s3, n2 = re.subn(r'<span class="n2">LOG\.\d\d</span>', '', s2)
    return s3 if (n1 + n2) else None

def gap_gone(s):
    s2, n = re.subn(r'<span class="st2">GAP\.\d\d</span>', '', s)
    return s2 if n else None

def tb_gone(s):
    s2, n = re.subn(r'<div class="tB">[^<]*</div>', '', s)
    return s2 if n else None

def vlab_gone(s):
    s2, n = re.subn(r'<div class="vlab">[^<]*</div>', '', s)
    return s2 if n else None

def who_gone(s):
    s2, n = re.subn(r'<div class="who">(?:LESSON|SIGNATURE)[^<]*</div>', '', s)
    return s2 if n else None

def disclaimer_trim(s):
    old = "FOR INTERNAL REVIEW &middot; DO NOT DISTRIBUTE"
    return s.replace(old, "FOR INTERNAL REVIEW", 1) if old in s else None

def dup_rows_gone(s):
    n = 0
    for row in [
        r'<tr><td class="k">OUTBOUND REPLY RATE</td><td class="v">~20%</td></tr>',
        r'<tr><td class="k">OUTBOUND CONVERSION</td><td class="v">7&ndash;8%</td></tr>',
        r'<tr><td class="k">INBOUND CONVERSION</td><td class="v">50%\+</td></tr>',
    ]:
        s2, k = re.subn(row, '', s)
        s = s2; n += k
    return s if n else None

def tools_checks_gone(s):
    # remove check glyphs only inside the leadership toolkit list
    i = s.find('LEADERSHIP TOOLKIT')
    if i < 0: return None
    j = s.find('</div>\n', s.find('<div class="tools">', i))
    a = s.find('<div class="tools">', i)
    b = s.find('SIGNATURE') if s.find('SIGNATURE', a) > -1 else a + 3000
    seg_end = min(x for x in [s.find('sigq', a), s.find('</section>', a), a + 4000] if x > -1)
    seg = s[a:seg_end]
    seg2, n = re.subn(r'<span class="c">&#10003;</span>', '', seg)
    if not n: return None
    return s[:a] + seg2 + s[seg_end:]

# ---------------- CASEBOOK ----------------
def p04_manifests(s):
    old_x = '<div class="dossier">&gt; commercial function: none &rarr; operating system<br>&gt; pipeline: &euro;0 &rarr; &euro;3M+ ARR &middot; 7 enterprise closed</div>'
    if old_x not in s: return None
    s = s.replace(old_x, '<div class="dossier">&gt; Built the commercial function from zero</div>', 1)
    reps = [
        ('<div class="body" style="background:var(--brass);border-radius:0 12px 0 0"><div class="cat">LEADERSHIP &#8250;</div></div>',
         '<div class="body" style="background:var(--brass);border-radius:0 12px 0 0"><div class="cat">LEADERSHIP &#8250;</div><div class="dossier">&gt; CEO &mdash; built a profitable, scalable commercial organization</div></div>'),
        ('<div class="body" style="background:var(--ice);border-radius:0 12px 0 0"><div class="cat">ALIGNMENT &#8250;</div></div>',
         '<div class="body" style="background:var(--ice);border-radius:0 12px 0 0"><div class="cat">ALIGNMENT &#8250;</div><div class="dossier">&gt; Aligned commercial execution across teams</div></div>'),
    ]
    for a, b in reps:
        if a in s: s = s.replace(a, b, 1)
    m = re.search(r'(<div class="body" style="background:var\(--ink\)[^"]*">\s*<div class="cat">FOUNDER &#8250;</div>)(</div>)', s)
    if m:
        s = s[:m.end(1)] + '<div class="dossier">&gt; Founder &mdash; built the business from vision</div>' + s[m.end(1):]
    return s

def p13_ladder_css(s):
    add = """
/* FINALE LADDER — distinct closing geometry */
.p13 .pgrid{display:block}
.p13 .pi{display:flex;align-items:baseline;gap:16px;border-top:1px solid var(--grid);padding:7px 0 6px;position:relative}
.p13 .pgrid .pi:first-child{border-top:none;padding-top:0}
.p13 .pi .n{border:none;border-radius:0;width:36px;height:auto;justify-content:flex-start;
font-family:Inter,sans-serif;font-weight:800;font-size:20px;letter-spacing:-.02em;
color:transparent;-webkit-text-stroke:1.1px var(--emb);background:transparent}
.p13 .pi .t{padding-top:0;font-size:11.4px;line-height:1.35}
.p13 .pi.vision{border-top:1.5px solid var(--emb);margin-top:5px;padding-top:9px}
.p13 .pi.vision .n{-webkit-text-stroke:1.1px var(--emb)}
.p13 .pi.vision .t{font-size:13.2px}
"""
    k = s.rfind("</style>")
    return s[:k] + add + s[k:]

def ftr_left_gone_pdf(s):
    old = '<span>THE COMMERCIAL SYSTEMS BUILDER</span>'
    if old not in s: return None
    return s.replace(old, '<span></span>')

CASE_OPS = [
    ("LOG.NN prefixes gone", logn_gone),
    ("GAP.NN tags gone", gap_gone),
    ("ghost tabs gone", tb_gone),
    ("rail vlab text gone", vlab_gone),
    ("quote attributions gone", who_gone),
    ("footer-left wordmark gone", ftr_left_gone_pdf),
    ("disclaimer trimmed", disclaimer_trim),
    ("p06 dup metric rows gone", dup_rows_gone),
    ("p11 toolkit checks gone", tools_checks_gone),
    ("p04 one-line manifests", p04_manifests),
    ("p13 finale ladder css", p13_ladder_css),
]

# ---------------- SITE ----------------
def site_ftr_left(s):
    m = re.search(r'<span>ORAN CARMON[^<]*THE COMMERCIAL SYSTEMS BUILDER</span>', s)
    if not m: return None
    return s[:m.start()] + '<span>ORAN CARMON</span>' + s[m.end():]

def site_hdoss(s):
    reps = [
        ('&gt; commercial function: none &rarr; operating system<br>&gt; pipeline: &euro;0 &rarr; &euro;3M+ ARR &middot; 7 enterprise closed',
         '&gt; Built the commercial function from zero'),
        ('&gt; classification: COMMAND FILE &middot; GROWTH<br>&gt; contents: evidence &middot; exhibits &middot; testimony',
         '&gt; CEO &mdash; built a profitable, scalable commercial organization'),
        ('&gt; classification: B2B2C &middot; MARKETING&ndash;PRODUCT<br>&gt; contents: evidence &middot; exhibits &middot; log',
         '&gt; Aligned commercial execution across teams'),
        ('&gt; classification: ORIGIN FILE &middot; 2018<br>&gt; contents: origin &middot; evidence &middot; verdict',
         '&gt; Founder &mdash; built the business from vision'),
    ]
    hit = 0
    for a, b in reps:
        if a in s:
            s = s.replace(a, b, 1); hit += 1
    return s if hit else None

def site_dup_rows(s):
    n = 0
    for lab in ["OUTBOUND REPLY RATE", "OUTBOUND CONVERSION", "INBOUND CONVERSION"]:
        s2, k = re.subn(r'<tr><td class="k">' + lab + r'</td><td class="v[^"]*">[^<]*</td></tr>', '', s)
        s = s2; n += k
    return s if n else None

def site_ladder_css(s):
    add = """
/* FINALE LADDER (site) */
#final .pgrid{display:block}
#final .pi{display:flex;align-items:baseline;gap:16px;border-top:1px solid var(--grid);padding:9px 0 8px}
#final .pgrid .pi:first-child{border-top:none;padding-top:0}
#final .pi .n{border:none;border-radius:0;width:44px;height:auto;justify-content:flex-start;
font-family:Inter,sans-serif;font-weight:800;font-size:24px;letter-spacing:-.02em;
color:transparent;-webkit-text-stroke:1.2px var(--emb);background:transparent}
#final .pi .t{padding-top:0}
#final .pi.vision{border-top:1.5px solid var(--emb);margin-top:6px;padding-top:12px}
"""
    k = s.rfind("</style>")
    return s[:k] + add + s[k:]

SITE_OPS = [
    ("LOG.NN prefixes gone", logn_gone),
    ("GAP.NN tags gone", gap_gone),
    ("ghost tabs gone", tb_gone),
    ("rail vlab text gone", vlab_gone),
    ("quote attributions gone", who_gone),
    ("footer-left suffix gone", site_ftr_left),
    ("disclaimer trimmed", disclaimer_trim),
    ("dup metric rows gone", site_dup_rows),
    ("leadership toolkit checks gone", tools_checks_gone),
    ("index-card one-line manifests", site_hdoss),
    ("finale ladder css", site_ladder_css),
]

run("casebook.html", CASE_OPS)
run("site.html", SITE_OPS, standalone=True)
print("DECLUTTER ROUND DONE")
