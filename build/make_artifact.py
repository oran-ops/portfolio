# -*- coding: utf-8 -*-
import io, re

raw = io.open("casebook.html", encoding="utf-8").read()
head, rest = raw.split("</style></head><body>")
css = head.split("<style>", 1)[1]
body = rest.split("</body></html>")[0]
fonts = io.open("fonts/fonts_dossier.css", encoding="utf-8").read()

secs = re.findall(r'<section class="page.*?</section>', body, re.S)
names = ["COVER", "STATEMENT", "PHILOSOPHY", "CASE FILES", "XTIX", "XTIX",
         "OASIS", "OASIS", "EVENTER", "MEDCOIN", "LEADERSHIP", "AI ENGINE", "CONTACT"]

TOTAL = 13
rows = []
nav = []
for i, sec in enumerate(secs):
    n = i + 1
    nm = names[i] if i < len(names) else "PAGE"
    nav.append('<a href="#p%d">%02d</a>' % (n, n))
    rows.append(
        '<section class="row" id="p%d">'
        '<div class="cap"><span class="tab">P.%02d</span>'
        '<span class="nm">%s</span><span class="st">FOR REVIEW</span></div>'
        '<div class="frame">%s</div></section>' % (n, n, nm, sec)
    )

viewer_css = """
/* ===== live-preview shell (quiet dark archive table) ===== */
html,body{background:#08090A}
body{font-family:'JetBrains Mono',monospace;min-height:100vh;padding-bottom:80px}
.bar{position:sticky;top:0;z-index:50;display:flex;align-items:center;gap:20px;
padding:14px 26px;background:rgba(8,9,10,.86);backdrop-filter:blur(10px);
border-bottom:1px solid var(--hair)}
.bar .dot{width:8px;height:8px;border-radius:50%;background:var(--emb);
box-shadow:none;flex:none}
.bar .brand{font-weight:700;font-size:11px;letter-spacing:.2em;color:var(--ink)}
.bar .nav{display:flex;gap:4px;margin-left:auto}
.bar .nav a{font-size:10px;letter-spacing:.12em;color:var(--dim);text-decoration:none;
padding:5px 9px;border:1px solid var(--grid);border-radius:6px}
.bar .nav a:hover{color:var(--ink);border-color:var(--grid2)}
.bar .count{font-size:10px;letter-spacing:.16em;color:var(--mut);margin-left:8px}
.stage{width:min(1280px,94vw);margin:0 auto;padding-top:30px}
.row{margin-bottom:34px;scroll-margin-top:74px}
.cap{display:flex;align-items:center;gap:12px;margin-bottom:11px;padding-left:2px}
.cap .tab{font-weight:700;font-size:10px;letter-spacing:.14em;color:#0C0D10;
background:var(--emb);border-radius:5px 12px 0 0;padding:4px 12px 5px}
.cap .nm{font-weight:700;font-size:10px;letter-spacing:.24em;color:var(--ink)}
.cap .st{margin-left:auto;font-size:9px;letter-spacing:.2em;color:var(--dim);
border:1px solid var(--grid);border-radius:5px;padding:3px 9px}
.frame{position:relative;width:100%;overflow:hidden;background:#000;
border:1px solid var(--hair);border-radius:14px}
.frame>.page{transform-origin:top left}
.foot{text-align:center;margin-top:40px;font-size:9.5px;letter-spacing:.22em;color:var(--dim)}
@media (max-width:640px){.bar .brand{font-size:9px}.bar .nav{display:none}}
"""

viewer_js = """
(function(){
  function fit(){
    var fs=document.querySelectorAll('.frame');
    for(var i=0;i<fs.length;i++){
      var f=fs[i], s=f.clientWidth/1280, pg=f.firstElementChild;
      pg.style.transform='scale('+s+')';
      f.style.height=(720*s)+'px';
    }
  }
  window.addEventListener('resize',fit);
  window.addEventListener('load',fit);
  fit();
})();
"""

count = "LIVE PREVIEW &middot; " + str(len(secs)) + " / " + str(TOTAL)
out = (
    "<title>Oran Carmon &mdash; Executive Portfolio</title>\n"
    "<style>\n" + fonts + "\n" + css + "\n" + viewer_css + "</style>\n"
    '<header class="bar">'
    '<span class="dot"></span>'
    '<span class="brand">ORAN CARMON &mdash; EXECUTIVE PORTFOLIO</span>'
    '<nav class="nav">' + "".join(nav) + "</nav>"
    '<span class="count">' + count + "</span>"
    "</header>\n"
    '<main class="stage">\n' + "\n".join(rows) + "\n"
    '<div class="foot">DOSSIER ARCHIVE &middot; ORAN CARMON &middot; UPDATES AS EACH PAGE IS BUILT</div>\n'
    "</main>\n"
    "<script>" + viewer_js + "</script>"
)

io.open("casebook_preview.html", "w", encoding="utf-8").write(out)
print("artifact written:", len(secs), "pages,", len(out), "bytes")
