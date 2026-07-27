# -*- coding: utf-8 -*-
import io
p="casebook.html"; s=io.open(p,encoding="utf-8").read()

# ---------- CSS additions ----------
css="""
/* folder DNA on pages 1-3 */
.p01 .quote{bottom:178px}
.p01 .drawer{position:absolute;left:72px;right:72px;bottom:78px;display:flex;gap:10px;border-bottom:1px solid var(--grid2);padding:0 6px}
.p01 .dtab{flex:1;height:38px;border-radius:9px 20px 0 0;display:flex;align-items:center;padding:0 16px}
.p01 .dtab .nm{font-family:'Fraunces',serif;font-weight:500;font-size:15px;color:#0C0D10}
.p01 .dtab .meta{margin-left:auto;font-family:'JetBrains Mono',monospace;font-size:8px;letter-spacing:.14em;color:rgba(12,13,16,.65)}
.p01 .dlabel{position:absolute;left:78px;bottom:124px;font-family:'JetBrains Mono',monospace;font-size:8.5px;letter-spacing:.24em;color:var(--dim)}

.p02 .memo{display:inline-flex;align-items:center;gap:9px;background:var(--emb);color:#0C0D10;border-radius:7px 16px 0 0;
padding:8px 16px;font-family:'JetBrains Mono',monospace;font-weight:700;font-size:9px;letter-spacing:.22em;margin-bottom:30px}

.p03 .title{top:92px}
.p03 .folder{position:absolute;top:238px;left:72px;right:72px;background:var(--card);border:1px solid var(--hair);
border-radius:0 16px 16px 16px;padding:24px 28px 20px}
.p03 .flip{position:absolute;top:-30px;left:-1px;height:30px;background:var(--emb);border-radius:8px 18px 0 0;
display:flex;align-items:center;gap:10px;padding:0 16px;font-family:'JetBrains Mono',monospace;font-weight:700;font-size:9px;letter-spacing:.22em;color:#0C0D10}
.p03 .flip .sq{width:6px;height:6px;background:#0C0D10;transform:rotate(45deg)}
.p03 .grid2{display:grid;grid-template-columns:repeat(4,1fr);column-gap:28px;row-gap:26px}
.p03 .node{width:54px;height:54px}
.p03 .node svg{width:32px;height:32px}
.p03 .snum{margin-top:10px}
.p03 .sname{font-size:15px}
.p03 .sdesc{font-size:11px;line-height:1.4}
.p03 .qt{bottom:58px;padding:12px 24px}
.p03 .qt .qx{font-size:17.5px}
"""
s=s.replace("</style>",css+"</style>",1)

# ---------- P01: add drawer ----------
drawer="""  <div class="dlabel">INSIDE &middot; 04 CASE FILES &#8250;</div>
  <div class="drawer">
    <div class="dtab" style="background:var(--emb)"><span class="nm">XTIX</span><span class="meta">FILE 01</span></div>
    <div class="dtab" style="background:var(--brass)"><span class="nm">Oasis</span><span class="meta">FILE 02</span></div>
    <div class="dtab" style="background:var(--ice)"><span class="nm">Eventer</span><span class="meta">FILE 03</span></div>
    <div class="dtab" style="background:var(--ink)"><span class="nm">Medcoin</span><span class="meta">FILE 04</span></div>
  </div>
  <div class="ftr">"""
s=s.replace('  <div class="ftr">\n    <span>SAAS',drawer+'\n    <span>SAAS',1)

# ---------- P02: memo tab ----------
s=s.replace('  <div class="stmt">\n    <div class="l1">',
'  <div class="stmt">\n    <div class="memo"><span>MEMO &middot; FROM THE ARCHIVE</span></div><br>\n    <div class="l1">',1)

# ---------- P03: wrap grid in folder ----------
old_open='  <div class="grid">\n'
new_open='  <div class="folder">\n    <div class="flip"><span class="sq"></span>MASTER FILE &middot; THE 8 PRINCIPLES</div>\n    <div class="grid2">\n'
assert old_open in s
s=s.replace(old_open,new_open,1)
# close: the grid ends with "  </div>\n  <div class=\"qt\">" inside p03
old_close='  </div>\n  <div class="qt">'
new_close='    </div>\n  </div>\n  <div class="qt">'
assert old_close in s
s=s.replace(old_close,new_close,1)
# remove old absolute .grid css usage (grid class no longer used on p03) — leave CSS harmless

io.open(p,"w",encoding="utf-8").write(s)
print("folder DNA applied to pages 1-3")
