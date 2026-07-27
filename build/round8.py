# -*- coding: utf-8 -*-
# Round 8 — list alignment, bolder tab heads, the AI section repaired, one more
# contrast notch, and a closing rebuilt as a system schematic.
import io, re

LOG = []
def op(name, fn, s):
    try:
        out = fn(s)
        if out is None or out == s:
            LOG.append(' SKIP  ' + name); return s
        LOG.append(' OK    ' + name); return out
    except Exception as e:
        LOG.append(' ERR   %s :: %s' % (name, str(e)[:110])); return s

def css_end(add):
    def f(s):
        k = s.rfind('</style>')
        return s[:k] + add + '\n' + s[k:]
    return f

def close_of(txt, open_start):
    i = txt.find('>', open_start) + 1
    depth = 1
    for m in re.finditer(r'<(/?)div\b[^>]*>', txt[i:]):
        depth += -1 if m.group(1) else 1
        if depth == 0:
            return i + m.end()
    raise ValueError('unbalanced')

# ---------- 4. one more notch of contrast ----------
def contrast_notch(s):
    if '#A9AAAE' not in s and '#C3C4C8' not in s: return None
    return s.replace('#A9AAAE', '#B6B7BB').replace('#C3C4C8', '#CFD0D4')

# ---------- 1. tab-head text carries more weight ----------
LIP_SITE = """
/* R8 — tab-head text reads as the label it is */
.hfolder .hlip .nm{font-weight:700}
.hfolder .hlip .fl{opacity:.85;font-weight:700}
.tabrow .tA .nm{font-weight:600}
.tabrow .tA .fl{opacity:.9}
.flip .nm{font-weight:700}
.flip .fl{opacity:.9}
#final .card .clip .nm,.case .stat .slip{font-weight:700}
"""
LIP_PDF = """
/* R8 — tab-head text reads as the label it is */
.flip .nm,.tA .nm,.p13 .card .clip .nm{font-weight:700!important}
.flip .fl,.tA .fl,.p13 .card .clip .fl{font-weight:700!important;color:#191A1F!important}
.p08 .stat .slip{font-weight:700}
"""

# ---------- image 1: the approach list hugs the left ----------
def approach_left_site(s):
    old = '<div class="grid2c" style="margin-top:12px">'
    if old not in s: return None
    return s.replace(old, '<div class="grid2c apl" style="margin-top:12px">', 1)

APPR_CSS_SITE = """
/* R8 — the approach list stays attached to its heading */
#xtix .grid2c.apl{grid-template-columns:max-content max-content;justify-content:start;column-gap:46px}
@media (max-width:680px){#xtix .grid2c.apl{grid-template-columns:1fr}}
"""
APPR_CSS_PDF = """
/* R8 — the approach list stays attached to its heading */
.agrid{grid-template-columns:max-content max-content;justify-content:start;column-gap:34px}
"""

# ---------- image 2: the AI section ----------
TECH_CSS_SITE = """
/* R8 — breathing room in the system list, feedback loop reads clearly */
#tech .list{display:grid;gap:11px}
#tech .list .lg{align-items:flex-start;line-height:1.45}
#tech .list .lg .c{margin-top:1px}
#tech .stackr{gap:9px}
#tech .phil{margin-top:22px;padding-top:14px;border-top:1px solid var(--grid);line-height:1.9}
#tech .archw svg{overflow:visible}
"""
TECH_CSS_PDF = """
/* R8 — breathing room in the system list */
.p12 .list{display:grid;gap:6.5px}
.p12 .list .lg{align-items:flex-start;line-height:1.4}
.p12 .phil{margin-top:12px;padding-top:9px;border-top:1px solid var(--grid)}
"""

def loop_arrow(s):
    # the feedback arrowhead was rotated off-axis; point it straight into the node
    s2, n = re.subn(r'\s*transform="rotate\(26 [\d.]+ [\d.]+\)"', '', s)
    return s2 if n else None

def tech_quote_to_bottom(s):
    i = s.find('id="tech"')
    if i < 0: return None
    j = s.find('</section>', i)
    seg = s[i:j]
    m = re.search(r'<div class="lessq" style="margin-top:20px">', seg)
    if not m: return None
    q0 = m.start(); q1 = close_of(seg, q0)
    quote = seg[q0:q1].replace('<div class="lessq" style="margin-top:20px">',
                               '<div class="lessq">', 1)
    seg = seg[:q0] + seg[q1:]
    # last child of .wrap = just before the two closing divs at the end of the section
    k = seg.rfind('</div>')          # closes .wrap
    k2 = seg.rfind('</div>', 0, k)   # closes the last inner block
    seg = seg[:k2 + 6] + '\n    ' + quote + seg[k2 + 6:]
    return s[:i] + seg + s[j:]

# ---------- 5. the closing as a system schematic ----------
P = [("01", "Understand before you build."),
     ("02", "Vision creates direction.<br>Execution creates momentum."),
     ("03", "Commercial growth is a business problem &mdash; not a sales problem."),
     ("04", "Build systems before you scale people."),
     ("05", "Measure decisions &mdash; not assumptions."),
     ("06", "Technology should improve thinking &mdash; not replace it."),
     ("07", "Great leaders create ownership."),
     ("08", "Commercial success belongs to every department."),
     ("09", "Continuous learning is a competitive advantage.")]

def nodes(rv):
    out = []
    for i, (n, t) in enumerate(P):
        side = 'l' if i % 2 == 0 else 'r'
        cls = 'node %s rv' % side if rv else 'node %s' % side
        st = ' style="--i:%d"' % (i % 5) if rv else ''
        out.append('<div class="%s"%s><span class="nn">%s</span><span class="nt">%s</span></div>'
                   % (cls, st, n, t))
    return ''.join(out)

def osmap(rv):
    spine = '<div class="spine rv"></div>' if rv else '<div class="spine"></div>'
    return ('<div class="osmap">%s%s<div class="tipd"></div></div>' % (spine, nodes(rv)))

def seal(rv):
    cls = 'vseal rv' if rv else 'vseal'
    st = ' style="--i:3"' if rv else ''
    return ('<div class="%s"%s>'
            '<span class="vb tl"></span><span class="vb tr"></span>'
            '<span class="vb bl"></span><span class="vb br"></span>'
            '<div class="vmark">&#10022;</div>'
            '<div class="vq">If you connect to the vision, <b>you\'ll always know where you\'re going.</b></div>'
            '<div class="vsig"><span class="vd"></span>ORAN CARMON'
            '<span class="vsep">&middot;</span>COMMERCIAL SYSTEMS BUILDER<span class="vd"></span></div>'
            '</div>') % (cls, st)

ABOUT = ('I enjoy building commercial organizations <b>from zero</b>. '
         'I believe <b>systems scale better than heroes</b>. '
         'My goal is to leave every company <b>stronger than I found it</b>.')

SITE_FINAL = """<section class="sec" id="final" style="--fc:var(--emb)">
  <div class="wrap">
    <div class="shead rv" style="--i:0">
      <div class="rub"><span class="d"></span>FINAL THOUGHTS</div>
      <div class="tok">END OF FILE</div>
    </div>
    <div class="sttl rv" style="--i:1">The Builder's Principles</div>
    <div class="smeta rv" style="--i:1">TEN PRINCIPLES &middot; ONE OPERATING SYSTEM</div>
    <div class="folder rv" style="--i:2;margin-top:48px">
      <div class="tabrow"><div class="tA"><span class="nm">The Builder</span><span class="fl">&#9656; END OF FILE</span></div></div>
      <div class="frail"><span class="hole" style="top:76px"></span><span class="hole" style="top:114px"></span></div>
      __OSMAP__
      __SEAL__
      <div class="fabout rv" style="--i:4">__ABOUT__</div>
      <div class="fcontact rv" style="--i:4">
        <a class="cc" href="https://www.linkedin.com/in/oran-carmon" target="_blank" rel="noopener"><span class="k">LINKEDIN</span><span class="v">linkedin.com/in/oran-carmon</span></a>
        <a class="cc" href="mailto:orancarmon@gmail.com"><span class="k">EMAIL</span><span class="v">orancarmon@gmail.com</span></a>
        <a class="cc" href="tel:+972546685331"><span class="k">PHONE</span><span class="v">+972-54-668-5331</span></a>
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
      __OSMAP__
      __SEAL__
      <div class="fabout">__ABOUT__</div>
      <div class="fcontact">
        <div class="cc"><span class="k">LINKEDIN</span><span class="v">linkedin.com/in/oran-carmon</span></div>
        <div class="cc"><span class="k">EMAIL</span><span class="v">orancarmon@gmail.com</span></div>
        <div class="cc"><span class="k">PHONE</span><span class="v">+972-54-668-5331</span></div>
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

CLOSE_CSS_SITE = """
/* ============ R8 — THE CLOSING: ten principles, one system ============ */
#final .secnum{display:none}
#final .smeta{margin-top:14px;font-family:'JetBrains Mono',monospace;font-weight:600;
  font-size:10px;letter-spacing:.34em;color:var(--lbl)}
#final .osmap{position:relative;display:grid;grid-template-columns:1fr 104px 1fr;margin-top:10px;padding:6px 0 22px}
#final .osmap .spine{position:absolute;left:50%;top:0;bottom:22px;width:2px;margin-left:-1px;
  background:var(--emb);opacity:.55;transform:scaleY(0);transform-origin:top;
  transition:transform 1.15s var(--ease) .1s}
#final .osmap .spine.on{transform:scaleY(1)}
#final .node{position:relative;display:flex;align-items:baseline;gap:13px;padding:15px 0}
#final .node.l{grid-column:1;flex-direction:row-reverse;justify-content:flex-start;text-align:right}
#final .node.r{grid-column:3;justify-content:flex-start;text-align:left}
#final .node .nn{flex:none;font-family:'JetBrains Mono',monospace;font-weight:700;font-size:10px;
  letter-spacing:.16em;color:var(--emb)}
#final .node .nt{font-size:14px;line-height:1.5;font-weight:600;color:var(--ink);max-width:340px}
#final .node::after{content:"";position:absolute;top:calc(50% - .5px);width:52px;height:1px;background:var(--grid2)}
#final .node.l::after{right:-52px}
#final .node.r::after{left:-52px}
#final .node::before{content:"";position:absolute;top:50%;width:9px;height:9px;background:var(--emb);
  transform:translateY(-50%) rotate(45deg);z-index:2}
#final .node.l::before{right:-56.5px}
#final .node.r::before{left:-56.5px}
#final .osmap .tipd{position:absolute;left:50%;bottom:2px;margin-left:-7px;width:0;height:0;
  border-left:7px solid transparent;border-right:7px solid transparent;border-top:11px solid var(--emb)}
#final .vseal{position:relative;margin-top:6px;padding:34px 44px 26px;text-align:center;
  border:1px solid rgba(47,179,128,.34);border-radius:16px;background:rgba(47,179,128,.05)}
#final .vseal .vb{position:absolute;width:15px;height:15px;border:2px solid var(--emb)}
#final .vseal .vb.tl{top:11px;left:11px;border-right:0;border-bottom:0}
#final .vseal .vb.tr{top:11px;right:11px;border-left:0;border-bottom:0}
#final .vseal .vb.bl{bottom:11px;left:11px;border-right:0;border-top:0}
#final .vseal .vb.br{bottom:11px;right:11px;border-left:0;border-top:0}
#final .vseal .vmark{font-size:13px;color:var(--emb);line-height:1;margin-bottom:12px}
#final .vseal .vq{font-family:'Fraunces',serif;font-style:italic;font-weight:500;
  font-size:clamp(19px,2.3vw,25px);line-height:1.4;color:var(--ink);max-width:940px;margin:0 auto}
#final .vseal .vq b{color:var(--emb);font-weight:600}
#final .vseal .vsig{margin-top:18px;display:flex;align-items:center;justify-content:center;gap:11px;
  font-family:'JetBrains Mono',monospace;font-weight:700;font-size:8.5px;letter-spacing:.32em;color:var(--lbl)}
#final .vseal .vd{width:6px;height:6px;background:var(--emb);transform:rotate(45deg)}
#final .vseal .vsep{color:var(--emb)}
#final .fabout{margin-top:34px;text-align:center;font-family:'Fraunces',serif;font-style:italic;
  font-size:16px;line-height:1.85;color:var(--mut);max-width:760px;margin-left:auto;margin-right:auto}
#final .fabout b{color:var(--ink);font-weight:500}
#final .fcontact{display:grid;grid-template-columns:repeat(3,1fr);gap:14px;margin-top:34px}
#final .fcontact .cc{display:flex;flex-direction:column;gap:7px;padding:16px 18px;text-decoration:none;
  border:1px solid var(--hair);border-radius:12px;background:var(--card);transition:border-color .3s var(--ease)}
#final .fcontact .cc:hover{border-color:var(--emb)}
#final .fcontact .k{font-family:'JetBrains Mono',monospace;font-size:9px;letter-spacing:.26em;color:var(--lbl)}
#final .fcontact .v{font-family:'JetBrains Mono',monospace;font-weight:600;font-size:12.5px;
  color:var(--ink);word-break:break-all}
#final .closeline{margin-top:34px;font-size:18px;color:var(--lbl);border-top:1px solid var(--grid);padding-top:22px}
@media (max-width:680px){
  #final .osmap{grid-template-columns:30px 1fr;padding-bottom:26px}
  #final .osmap .spine{left:15px}
  #final .node.l,#final .node.r{grid-column:2;flex-direction:row;justify-content:flex-start;text-align:left;padding:11px 0}
  #final .node.l::after,#final .node.r::after{left:-15px;right:auto;width:15px}
  #final .node.l::before,#final .node.r::before{left:-19.5px;right:auto}
  #final .osmap .tipd{left:15px}
  #final .node .nt{font-size:13px}
  #final .vseal{padding:22px 16px 28px}
  #final .vseal .vsig{flex-wrap:wrap;gap:5px 8px;font-size:7px;margin-top:14px}
  #final .vseal .vb{width:11px;height:11px}
  #final .fcontact{grid-template-columns:1fr}
  #final .fabout{font-size:14px;margin-top:26px}
  #final .closeline{font-size:15px}
}
"""

CLOSE_CSS_PDF = """
/* ============ R8 — THE CLOSING (PDF) ============ */
.p13 .inner13{position:relative;height:100%}
.p13 .osmap{position:relative;display:grid;grid-template-columns:1fr 84px 1fr;margin-top:2px;padding:2px 0 15px}
.p13 .osmap .spine{position:absolute;left:50%;top:0;bottom:15px;width:1.6px;margin-left:-.8px;
  background:var(--emb);opacity:.55}
.p13 .node{position:relative;display:flex;align-items:baseline;gap:10px;padding:8px 0}
.p13 .node.l{grid-column:1;flex-direction:row-reverse;justify-content:flex-start;text-align:right}
.p13 .node.r{grid-column:3;justify-content:flex-start;text-align:left}
.p13 .node .nn{flex:none;font-family:'JetBrains Mono',monospace;font-weight:700;font-size:8.2px;
  letter-spacing:.14em;color:var(--emb)}
.p13 .node .nt{font-size:11px;line-height:1.38;font-weight:600;color:var(--ink);max-width:250px}
.p13 .node::after{content:"";position:absolute;top:calc(50% - .5px);width:42px;height:1px;background:var(--grid2)}
.p13 .node.l::after{right:-42px}
.p13 .node.r::after{left:-42px}
.p13 .node::before{content:"";position:absolute;top:50%;width:7px;height:7px;background:var(--emb);
  transform:translateY(-50%) rotate(45deg);z-index:2}
.p13 .node.l::before{right:-45.5px}
.p13 .node.r::before{left:-45.5px}
.p13 .osmap .tipd{position:absolute;left:50%;bottom:1px;margin-left:-5px;width:0;height:0;
  border-left:5px solid transparent;border-right:5px solid transparent;border-top:8px solid var(--emb)}
.p13 .vseal{position:relative;margin-top:4px;padding:14px 30px 11px;text-align:center;
  border:1px solid rgba(47,179,128,.34);border-radius:12px;background:rgba(47,179,128,.05)}
.p13 .vseal .vb{position:absolute;width:11px;height:11px;border:1.5px solid var(--emb)}
.p13 .vseal .vb.tl{top:7px;left:7px;border-right:0;border-bottom:0}
.p13 .vseal .vb.tr{top:7px;right:7px;border-left:0;border-bottom:0}
.p13 .vseal .vb.bl{bottom:7px;left:7px;border-right:0;border-top:0}
.p13 .vseal .vb.br{bottom:7px;right:7px;border-left:0;border-top:0}
.p13 .vseal .vmark{font-size:9px;color:var(--emb);line-height:1;margin-bottom:6px}
.p13 .vseal .vq{font-family:'Fraunces',serif;font-style:italic;font-weight:500;font-size:15px;
  line-height:1.34;color:var(--ink);max-width:660px;margin:0 auto}
.p13 .vseal .vq b{color:var(--emb);font-weight:600}
.p13 .vseal .vsig{margin-top:8px;display:flex;align-items:center;justify-content:center;gap:9px;
  font-family:'JetBrains Mono',monospace;font-weight:700;font-size:6.8px;letter-spacing:.28em;color:var(--lbl)}
.p13 .vseal .vd{width:5px;height:5px;background:var(--emb);transform:rotate(45deg)}
.p13 .vseal .vsep{color:var(--emb)}
.p13 .fabout{margin:13px auto 0;text-align:center;font-family:'Fraunces',serif;font-style:italic;
  font-size:11.4px;line-height:1.6;color:var(--mut);max-width:620px}
.p13 .fabout b{color:var(--ink);font-weight:500}
.p13 .fcontact{display:grid;grid-template-columns:repeat(3,1fr);gap:10px;margin-top:13px}
.p13 .fcontact .cc{display:flex;flex-direction:column;gap:5px;padding:9px 12px;
  border:1px solid var(--grid);border-radius:10px;background:var(--card2)}
.p13 .fcontact .k{font-family:'JetBrains Mono',monospace;font-size:7.5px;letter-spacing:.24em;color:var(--lbl)}
.p13 .fcontact .v{font-family:'JetBrains Mono',monospace;font-weight:600;font-size:10px;color:var(--ink)}
.p13 .closeline{margin-top:12px;border-top:1px solid var(--grid);padding-top:9px;
  font-size:12.4px;color:var(--lbl);text-align:center}
"""

def replace_section(start_pat, new_html):
    def f(s):
        m = re.search(start_pat, s)
        if not m: return None
        j = s.find('</section>', m.start())
        return s[:m.start()] + new_html + s[j + 10:]
    return f

# ================= run =================
site_final = (SITE_FINAL.replace('__OSMAP__', osmap(True)).replace('__SEAL__', seal(True))
              .replace('__ABOUT__', ABOUT))
pdf_final = (PDF_FINAL.replace('__OSMAP__', osmap(False)).replace('__SEAL__', seal(False))
             .replace('__ABOUT__', ABOUT))

s = io.open('site.html', encoding='utf-8').read()
LOG.append('== site.html')
s = op('4 contrast notch', contrast_notch, s)
s = op('1 tab-head weight', css_end(LIP_SITE), s)
s = op('img1 approach list tagged', approach_left_site, s)
s = op('img1 approach list css', css_end(APPR_CSS_SITE), s)
s = op('img2 tech list + loop css', css_end(TECH_CSS_SITE), s)
s = op('img2 feedback arrowhead', loop_arrow, s)
s = op('img2 tech quote to bottom', tech_quote_to_bottom, s)
s = op('5 closing rebuilt', replace_section(r'<section class="sec" id="final"', site_final), s)
s = op('5 closing css', css_end(CLOSE_CSS_SITE), s)
io.open('site.html', 'w', encoding='utf-8', newline='').write(s)
LOG.append('   site %d bytes' % len(s.encode('utf-8')))

c = io.open('casebook.html', encoding='utf-8').read()
LOG.append('== casebook.html')
c = op('4 contrast notch', contrast_notch, c)
c = op('1 tab-head weight', css_end(LIP_PDF), c)
c = op('img1 approach list css', css_end(APPR_CSS_PDF), c)
c = op('img2 tech list css', css_end(TECH_CSS_PDF), c)
c = op('img2 feedback arrowhead', loop_arrow, c)
c = op('5 closing rebuilt', replace_section(r'<section class="page casef p13"', pdf_final), c)
c = op('5 closing css', css_end(CLOSE_CSS_PDF), c)
io.open('casebook.html', 'w', encoding='utf-8', newline='').write(c)
LOG.append('   casebook %d bytes' % len(c.encode('utf-8')))

head = ('<!doctype html>\n<html lang="en">\n<head>\n<meta charset="utf-8">\n'
        '<meta name="viewport" content="width=device-width,initial-scale=1">\n'
        '<meta name="color-scheme" content="dark">\n</head>\n<body>\n')
io.open('site_standalone.html', 'w', encoding='utf-8', newline='').write(head + s + '\n</body>\n</html>')
LOG.append('== standalone rebuilt')
print('\n'.join(LOG))
