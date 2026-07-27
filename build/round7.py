# -*- coding: utf-8 -*-
# Round 7 — seven notes from Oran, applied identically to site and PDF.
import io, re

def load(p):
    return io.open(p, encoding='utf-8').read()

def save(p, s):
    io.open(p, 'w', encoding='utf-8', newline='').write(s)

LOG = []
def op(name, fn, s):
    try:
        out = fn(s)
        if out is None or out == s:
            LOG.append(' SKIP  ' + name); return s
        LOG.append(' OK    ' + name); return out
    except Exception as e:
        LOG.append(' ERR   %s :: %s' % (name, str(e)[:100])); return s

def css_end(add):
    def f(s):
        k = s.rfind('</style>')
        return s[:k] + add + '\n' + s[k:]
    return f

# ---------- 4. brighter muted text, everywhere ----------
def contrast_lift(s):
    n = s.count('#8E8E93') + s.count('#A6A7AC')
    if not n: return None
    s = s.replace('#8E8E93', '#A9AAAE').replace('#A6A7AC', '#C3C4C8')
    return s

# ---------- 1. tab head flush with the folder body ----------
def lip_joint(s):
    def fix(m):
        top = int(m.group(1))
        return 'top:-%dpx;left:0' % (top - 1)
    s2, n = re.subn(r'top:-(\d+)px;left:-1px', fix, s)
    return s2 if n else None

# ---------- 3. closing quote → full-width band at the very bottom ----------
QUOTE_CSS_SITE = """
/* R7 — the closing line of every section sits at the very bottom, full width */
#xtix .lessq,#oasis .insight,#oasis .lessq,#eventer .lessq,#medcoin .lessq,
#leadership .sigq,#tech .lessq,.lessq,.insight,.sigq{
  grid-column:1/-1!important;order:9;width:100%;
  border-left:none!important;border-right:none!important;
  border-top:1px solid var(--fc,var(--emb))!important;
  margin-top:30px!important;padding:16px 0 0!important;text-align:center}
.lessq .qx,.insight .qx,.sigq .qx{font-size:19px!important;line-height:1.5;color:var(--ink)}
@media (max-width:680px){.lessq .qx,.insight .qx,.sigq .qx{font-size:15px!important}}
"""
QUOTE_CSS_PDF = """
/* R7 — the closing line of every page sits at the very bottom, full width */
.lesson,.lessq2,.insight,.sigq,.quote2{
  grid-column:1/-1!important;order:9;width:100%;
  border-left:none!important;border-top:1px solid var(--fc,var(--emb))!important;
  margin-top:14px!important;padding:9px 0 0!important;text-align:center}
.lesson .qx,.lessq2 .qx,.insight .qx,.sigq .qx,.quote2 .qx{
  font-size:12.4px!important;line-height:1.45;color:var(--ink)}
"""

# ---------- 2. keep-scrolling cue on the drawer ----------
def drawer_cue(s):
    old = '<div class="hhint">SCROLL &mdash; THE DRAWER SLIDES &#8250;</div>'
    if old not in s: return None
    new = ('<div class="hhint"><span class="hk">KEEP SCROLLING</span>'
           '<span class="har">&#8595;</span>'
           '<span class="hs">THE DRAWER SLIDES SIDEWAYS</span></div>')
    return s.replace(old, new, 1)

CUE_CSS = """
/* R7 — make it unmistakable that the page keeps going down */
.hhint{margin-top:26px;display:inline-flex;align-items:center;gap:11px;
  border:1px solid rgba(47,179,128,.45);border-radius:9px;padding:9px 15px;
  font-family:'JetBrains Mono',monospace;font-size:10px;letter-spacing:.2em;color:var(--lbl)}
.hhint .hk{font-weight:700;color:var(--emb)}
.hhint .har{color:var(--emb);font-size:13px;line-height:1;animation:hbob 1.6s ease-in-out infinite}
.hhint .hs{color:var(--lbl)}
@keyframes hbob{0%,100%{transform:translateY(-2px)}50%{transform:translateY(3px)}}
body.static .hhint .har,body.failsafe .hhint .har{animation:none!important}
@media (prefers-reduced-motion:reduce){.hhint .har{animation:none!important}}
@media (max-width:680px){.hhint{font-size:9px;padding:8px 12px;gap:8px}}
/* R7 — floating case ticker removed */
#evtag{display:none!important}
"""

# ---------- 5 + 6. the closing ----------
PRINCIPLES = [
    ("01", "Understand before you build."),
    ("02", "Vision creates direction. Execution creates momentum."),
    ("03", "Commercial growth is a business problem &mdash; not a sales problem."),
    ("04", "Build systems before you scale people."),
    ("05", "Measure decisions &mdash; not assumptions."),
    ("06", "Technology should improve thinking &mdash; not replace it."),
    ("07", "Great leaders create ownership."),
    ("08", "Commercial success belongs to every department."),
    ("09", "Continuous learning is a competitive advantage."),
]
VISION = "If you connect to the vision, <b>you'll always know where you're going.</b>"

def pgrid(rv=False):
    out = []
    for i, (n, t) in enumerate(PRINCIPLES):
        cls = 'pi rv' if rv else 'pi'
        st = ' style="--i:%d"' % (i % 5) if rv else ''
        out.append('<div class="%s"%s><div class="n">%s</div><div class="t">%s</div></div>' % (cls, st, n, t))
    return ''.join(out)

def seal(rv=False):
    cls = 'vseal rv' if rv else 'vseal'
    st = ' style="--i:3"' if rv else ''
    return ('<div class="%s"%s>'
            '<span class="vb tl"></span><span class="vb tr"></span>'
            '<span class="vb bl"></span><span class="vb br"></span>'
            '<div class="vmark">&#10022;</div>'
            '<div class="vq">%s</div>'
            '<div class="vsig"><span class="vd"></span>ORAN CARMON'
            '<span class="vsep">&middot;</span>COMMERCIAL SYSTEMS BUILDER<span class="vd"></span></div>'
            '</div>') % (cls, st, VISION)

SITE_FINAL = """<section class="sec" id="final" style="--fc:var(--emb)">
  <div class="wrap">
    <div class="shead rv" style="--i:0">
      <div class="rub"><span class="d"></span>FINAL THOUGHTS</div>
      <div class="tok">END OF FILE</div>
    </div>
    <div class="sttl rv" style="--i:1">The Builder's Principles</div>
    <div class="folder rv" style="--i:2;margin-top:52px">
      <div class="tabrow"><div class="tA"><span class="nm">The Builder</span><span class="fl">&#9656; END OF FILE</span></div></div>
      <div class="frail"><span class="hole" style="top:76px"></span><span class="hole" style="top:114px"></span></div>
      <div class="zr"><b>A</b><span class="d2"></span>THE BUILDER'S PRINCIPLES</div>
      <div class="pgrid">__PGRID__</div>
      __SEAL__
      <div class="fbot">
        <div>
          <div class="zr"><b>AM</b><span class="d2"></span>ABOUT ME</div>
          <div class="abt st" style="--i:1">I enjoy building commercial organizations <b>from zero</b>.<br>I believe <b>systems scale better than heroes</b>.<br>My goal is to leave every company <b>stronger than I found it</b>.</div>
        </div>
        <div>
          <div class="zr"><b>C</b><span class="d2"></span>CONTACT</div>
          <div class="card rv" style="--i:1">
            <div class="clip"><span class="nm">Oran Carmon</span><span class="fl">COMMERCIAL SYSTEMS BUILDER</span></div>
            <a class="crow" href="https://www.linkedin.com/in/oran-carmon" target="_blank" rel="noopener"><span class="k">LINKEDIN</span><span class="v">linkedin.com/in/oran-carmon</span></a>
            <a class="crow" href="mailto:orancarmon@gmail.com"><span class="k">EMAIL</span><span class="v">orancarmon@gmail.com</span></a>
            <a class="crow" href="tel:+972546685331"><span class="k">PHONE</span><span class="v">+972-54-668-5331</span></a>
          </div>
        </div>
      </div>
      <div class="closeline rv" style="--i:4">Turning vision into <b>commercial growth</b>.</div>
    </div>
  </div>
</section>"""

PDF_FINAL = """<section class="page casef p13" style="--fc:var(--emb)">
  <span class="brk tl"></span><span class="brk tr"></span><span class="brk bl"></span><span class="brk br"></span>
  <div class="hd">
    <div class="rub"><span class="d"></span>FINAL THOUGHTS</div>
    <div class="tok">END OF FILE</div>
  </div>
  <div class="ttl">The Builder's Principles</div>
  <div class="meta">TEN PRINCIPLES &middot; ONE OPERATING SYSTEM</div>
  <div class="folder">
    <div class="tabrow"><div class="tA"><span class="nm">The Builder</span><span class="fl">&#9656; END OF FILE</span></div></div>
    <div class="rail"><span class="hole" style="top:70px"></span><span class="hole" style="top:104px"></span></div>
    <div class="inner13">
      <div class="zr"><b>A</b><span class="d2"></span>THE BUILDER'S PRINCIPLES</div>
      <div class="pgrid">__PGRID__</div>
      __SEAL__
      <div class="fbot">
        <div>
          <div class="zr"><b>AM</b><span class="d2"></span>ABOUT ME</div>
          <div class="abt">I enjoy building commercial organizations <b>from zero</b>.<br>I believe <b>systems scale better than heroes</b>.<br>My goal is to leave every company <b>stronger than I found it</b>.</div>
        </div>
        <div>
          <div class="zr"><b>C</b><span class="d2"></span>CONTACT</div>
          <div class="card">
            <div class="clip"><span class="nm">Oran Carmon</span><span class="fl">COMMERCIAL SYSTEMS BUILDER</span></div>
            <div class="crow"><span class="k">LINKEDIN</span><span class="v">linkedin.com/in/oran-carmon</span></div>
            <div class="crow"><span class="k">EMAIL</span><span class="v">orancarmon@gmail.com</span></div>
            <div class="crow"><span class="k">PHONE</span><span class="v">+972-54-668-5331</span></div>
          </div>
        </div>
      </div>
      <div class="closeline">Turning vision into <b>commercial growth</b>.</div>
    </div>
  </div>
  <div class="ftr">
    <span></span>
    <span class="mid"><span class="d"></span>FINAL THOUGHTS</span>
    <span><b>P.13</b> &mdash; 13</span>
  </div>
</section>"""

FINAL_CSS_SITE = """
/* ============ R7 — THE CLOSING ============ */
#final .secnum{display:none}
#final .pgrid{display:grid;grid-template-columns:1fr 1fr;gap:0 44px;margin-top:4px}
#final .pi{display:flex;align-items:baseline;gap:14px;border-top:1px solid var(--grid);padding:11px 0 10px}
#final .pgrid .pi:first-child,#final .pgrid .pi:nth-child(2){border-top:none}
#final .pi .n{flex:none;width:auto;height:auto;border:none!important;border-radius:0;background:none;
  font-family:'JetBrains Mono',monospace;font-weight:700;font-size:9.5px;letter-spacing:.14em;
  color:var(--emb)!important;-webkit-text-stroke:0!important;justify-content:flex-start;padding-top:0}
#final .pi .t{font-size:13.6px;line-height:1.5;font-weight:600;color:var(--ink);padding-top:0}
#final .vseal{position:relative;margin-top:34px;padding:34px 44px 26px;text-align:center;
  border:1px solid rgba(47,179,128,.34);border-radius:16px;background:rgba(47,179,128,.05)}
#final .vseal .vb{position:absolute;width:15px;height:15px;border:2px solid var(--emb)}
#final .vseal .vb.tl{top:11px;left:11px;border-right:0;border-bottom:0}
#final .vseal .vb.tr{top:11px;right:11px;border-left:0;border-bottom:0}
#final .vseal .vb.bl{bottom:11px;left:11px;border-right:0;border-top:0}
#final .vseal .vb.br{bottom:11px;right:11px;border-left:0;border-top:0}
#final .vseal .vmark{font-size:13px;color:var(--emb);line-height:1;margin-bottom:12px}
#final .vseal .vq{font-family:'Fraunces',serif;font-style:italic;font-weight:500;
  font-size:clamp(19px,2.5vw,27px);line-height:1.4;color:var(--ink);max-width:820px;margin:0 auto}
#final .vseal .vq b{color:var(--emb);font-weight:600}
#final .vseal .vsig{margin-top:18px;display:flex;align-items:center;justify-content:center;gap:11px;
  font-family:'JetBrains Mono',monospace;font-weight:700;font-size:8.5px;letter-spacing:.32em;color:var(--lbl)}
#final .vseal .vd{width:6px;height:6px;background:var(--emb);transform:rotate(45deg)}
#final .vseal .vsep{color:var(--emb)}
#final .fbot{display:grid;grid-template-columns:1fr 1fr;gap:44px;margin-top:34px}
#final .abt{font-size:15px;line-height:1.75}
#final .card{margin-top:30px}
#final .closeline{margin-top:34px;font-size:18px;color:var(--lbl);
  border-top:1px solid var(--grid);padding-top:22px}
@media (max-width:680px){
  #final .pgrid,#final .fbot{grid-template-columns:1fr;gap:0}
  #final .pgrid .pi:nth-child(2){border-top:1px solid var(--grid)}
  #final .fbot>div+div{margin-top:26px}
  #final .vseal{padding:24px 18px 20px;margin-top:26px}
  #final .vseal .vsig{font-size:7.5px;letter-spacing:.22em;gap:8px}
  #final .closeline{font-size:15px}
}
"""

FINAL_CSS_PDF = """
/* ============ R7 — THE CLOSING (PDF) ============ */
.p13 .inner13{position:relative;height:100%}
.p13 .pgrid{display:grid;grid-template-columns:1fr 1fr;gap:0 30px;margin-top:2px}
.p13 .pi{display:flex;align-items:baseline;gap:11px;border-top:1px solid var(--grid);padding:6.5px 0 5.5px}
.p13 .pgrid .pi:first-child,.p13 .pgrid .pi:nth-child(2){border-top:none;padding-top:0}
.p13 .pi .n{flex:none;width:auto;height:auto;border:none!important;border-radius:0;background:none;
  font-family:'JetBrains Mono',monospace;font-weight:700;font-size:8.2px;letter-spacing:.12em;
  color:var(--emb)!important;-webkit-text-stroke:0!important;justify-content:flex-start;padding-top:0}
.p13 .pi .t{font-size:11.2px;line-height:1.38;font-weight:600;color:var(--ink);padding-top:0}
.p13 .vseal{position:relative;margin-top:16px;padding:16px 30px 13px;text-align:center;
  border:1px solid rgba(47,179,128,.34);border-radius:12px;background:rgba(47,179,128,.05)}
.p13 .vseal .vb{position:absolute;width:11px;height:11px;border:1.5px solid var(--emb)}
.p13 .vseal .vb.tl{top:7px;left:7px;border-right:0;border-bottom:0}
.p13 .vseal .vb.tr{top:7px;right:7px;border-left:0;border-bottom:0}
.p13 .vseal .vb.bl{bottom:7px;left:7px;border-right:0;border-top:0}
.p13 .vseal .vb.br{bottom:7px;right:7px;border-left:0;border-top:0}
.p13 .vseal .vmark{font-size:10px;color:var(--emb);line-height:1;margin-bottom:7px}
.p13 .vseal .vq{font-family:'Fraunces',serif;font-style:italic;font-weight:500;font-size:16.5px;
  line-height:1.38;color:var(--ink);max-width:700px;margin:0 auto}
.p13 .vseal .vq b{color:var(--emb);font-weight:600}
.p13 .vseal .vsig{margin-top:10px;display:flex;align-items:center;justify-content:center;gap:9px;
  font-family:'JetBrains Mono',monospace;font-weight:700;font-size:7px;letter-spacing:.28em;color:var(--lbl)}
.p13 .vseal .vd{width:5px;height:5px;background:var(--emb);transform:rotate(45deg)}
.p13 .vseal .vsep{color:var(--emb)}
.p13 .fbot{display:grid;grid-template-columns:1fr 1fr;gap:30px;margin-top:16px}
.p13 .abt{font-family:'Fraunces',serif;font-style:italic;font-size:12px;line-height:1.65;color:var(--mut)}
.p13 .abt b{color:var(--ink);font-weight:500}
.p13 .card{margin-top:26px}
.p13 .closeline{margin-top:14px;border-top:1px solid var(--grid);padding-top:11px;
  font-size:13px;color:var(--lbl);text-align:center}
"""

def replace_block(start_pat, new_html):
    def f(s):
        m = re.search(start_pat, s)
        if not m: return None
        j = s.find('</section>', m.start())
        if j < 0: return None
        return s[:m.start()] + new_html + s[j + 10:]
    return f

# ================= run =================
for path, is_site in (('site.html', True), ('casebook.html', False)):
    s = load(path)
    LOG.append('== ' + path)
    s = op('4 muted text brightened', contrast_lift, s)
    s = op('1 tab head flush with body', lip_joint, s)
    if is_site:
        s = op('2 keep-scrolling cue', drawer_cue, s)
        s = op('2/7 cue css + ticker off', css_end(CUE_CSS), s)
        s = op('3 closing quotes to the bottom', css_end(QUOTE_CSS_SITE), s)
        s = op('5+6 closing rebuilt', replace_block(r'<section class="sec" id="final"',
               SITE_FINAL.replace('__PGRID__', pgrid(True)).replace('__SEAL__', seal(True))), s)
        s = op('5+6 closing css', css_end(FINAL_CSS_SITE), s)
    else:
        s = op('3 closing quotes to the bottom', css_end(QUOTE_CSS_PDF), s)
        s = op('5+6 closing rebuilt', replace_block(r'<section class="page casef p13"',
               PDF_FINAL.replace('__PGRID__', pgrid(False)).replace('__SEAL__', seal(False))), s)
        s = op('5+6 closing css', css_end(FINAL_CSS_PDF), s)
    save(path, s)
    LOG.append('   %s now %d bytes' % (path, len(s.encode('utf-8'))))

# standalone rebuild
head = ('<!doctype html>\n<html lang="en">\n<head>\n<meta charset="utf-8">\n'
        '<meta name="viewport" content="width=device-width,initial-scale=1">\n'
        '<meta name="color-scheme" content="dark">\n</head>\n<body>\n')
save('site_standalone.html', head + load('site.html') + '\n</body>\n</html>')
LOG.append('== standalone rebuilt')
print('\n'.join(LOG))
