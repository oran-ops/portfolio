# -*- coding: utf-8 -*-
# Contrast & size-floor fixes per auditor: --lbl token, emerald alpha floor, size bumps
import io, re

LBL_DECL = "--lbl:#A6A7AC;"

# ============================================================ PDF
s=io.open("casebook.html",encoding="utf-8").read()
s=s.replace("--dim:#5A5B60;","--dim:#5A5B60;"+LBL_DECL,1)

# --- Sev1: dim -> lbl on content selectors (targeted rule swaps) ---
PDF_DIM2LBL=[
 (".p06 .tbl .k{font-family:'JetBrains Mono',monospace;font-size:8.5px;letter-spacing:.14em;color:var(--dim)",
  ".p06 .tbl .k{font-family:'JetBrains Mono',monospace;font-size:9.5px;letter-spacing:.14em;color:var(--lbl)"),
 (".p08 .stat .lbl{margin-top:6px;font-family:'JetBrains Mono',monospace;font-size:8px;letter-spacing:.22em;color:var(--dim)}",
  ".p08 .stat .lbl{margin-top:6px;font-family:'JetBrains Mono',monospace;font-size:9px;letter-spacing:.22em;color:var(--lbl)}"),
 (".p06 .g1 .gl{margin-top:4px;font-family:'JetBrains Mono',monospace;font-size:7.5px;letter-spacing:.14em;color:var(--dim);line-height:1.6}",
  ".p06 .g1 .gl{margin-top:4px;font-family:'JetBrains Mono',monospace;font-size:9px;letter-spacing:.14em;color:var(--lbl);line-height:1.6}"),
 (".p09 .et .el{margin-top:5px;font-family:'JetBrains Mono',monospace;font-size:7.2px;letter-spacing:.16em;color:var(--dim);line-height:1.6}",
  ".p09 .et .el{margin-top:5px;font-family:'JetBrains Mono',monospace;font-size:9px;letter-spacing:.16em;color:var(--lbl);line-height:1.6}"),
 (".p10b .outs .k{font-family:'JetBrains Mono',monospace;font-size:8px;letter-spacing:.16em;color:var(--dim)}",
  ".p10b .outs .k{font-family:'JetBrains Mono',monospace;font-size:9px;letter-spacing:.16em;color:var(--lbl)}"),
 (".p13 .crow .k{font-family:'JetBrains Mono',monospace;font-size:8px;letter-spacing:.2em;color:var(--dim)}",
  ".p13 .crow .k{font-family:'JetBrains Mono',monospace;font-size:9px;letter-spacing:.2em;color:var(--lbl)}"),
 (".p10b .why .wl{display:block;font-family:'JetBrains Mono',monospace;font-weight:600;font-size:7.5px;letter-spacing:.24em;color:var(--dim);margin-bottom:5px}",
  ".p10b .why .wl{display:block;font-family:'JetBrains Mono',monospace;font-weight:600;font-size:9px;letter-spacing:.24em;color:var(--lbl);margin-bottom:5px}"),
 (".p08 .ringlbl{margin-top:2px;font-family:'JetBrains Mono',monospace;font-size:8px;letter-spacing:.18em;color:var(--dim)}",
  ".p08 .ringlbl{margin-top:2px;font-family:'JetBrains Mono',monospace;font-size:9px;letter-spacing:.18em;color:var(--lbl)}"),
 (".p05 .fh{display:flex;justify-content:space-between;font-family:'JetBrains Mono',monospace;font-weight:600;font-size:8px;letter-spacing:.2em;color:var(--dim);margin-bottom:6px}",
  ".p05 .fh{display:flex;justify-content:space-between;font-family:'JetBrains Mono',monospace;font-weight:600;font-size:9px;letter-spacing:.2em;color:var(--lbl);margin-bottom:6px}"),
 (".p05 .fz .lab{font-family:'JetBrains Mono',monospace;font-weight:600;font-size:8.5px;letter-spacing:.24em;color:var(--dim);white-space:nowrap}",
  ".p05 .fz .lab{font-family:'JetBrains Mono',monospace;font-weight:600;font-size:9.5px;letter-spacing:.24em;color:var(--lbl);white-space:nowrap}"),
 (".casef .meta{position:absolute;top:124px;left:72px;font-family:'JetBrains Mono',monospace;font-size:9.5px;",
  ".casef .meta{position:absolute;top:124px;left:72px;font-family:'JetBrains Mono',monospace;font-size:10px;"),
]
cnt=0
for a,b in PDF_DIM2LBL:
    if a in s: s=s.replace(a,b,1); cnt+=1
print("PDF dim->lbl rules:",cnt,"/",len(PDF_DIM2LBL))

# SVG annotation fills
s=s.replace('fill="#5A5B60"','fill="#A6A7AC"')

# --- Sev2: emerald-folder alpha floor + solid cat ---
s=s.replace(".p01b .qq{position:absolute;top:338px;left:0;right:0;text-align:center;font-family:'Fraunces',serif;font-style:italic;font-size:13.5px;color:rgba(19,20,23,.62)}",
            ".p01b .qq{position:absolute;top:338px;left:0;right:0;text-align:center;font-family:'Fraunces',serif;font-style:italic;font-size:13.5px;color:rgba(19,20,23,.8)}")
s=s.replace(".p01b .kick{position:absolute;top:46px;left:0;right:0;text-align:center;font-family:'JetBrains Mono',monospace;font-weight:700;font-size:10.5px;letter-spacing:.5em;color:rgba(19,20,23,.62)}",
            ".p01b .kick{position:absolute;top:46px;left:0;right:0;text-align:center;font-family:'JetBrains Mono',monospace;font-weight:700;font-size:10.5px;letter-spacing:.5em;color:rgba(19,20,23,.78)}")
s=s.replace(".p01b .by{position:absolute;top:308px;left:0;right:0;text-align:center;font-family:'JetBrains Mono',monospace;font-weight:600;font-size:10px;letter-spacing:.3em;color:rgba(19,20,23,.72)}",
            ".p01b .by{position:absolute;top:308px;left:0;right:0;text-align:center;font-family:'JetBrains Mono',monospace;font-weight:600;font-size:10px;letter-spacing:.3em;color:rgba(19,20,23,.8)}")
s=s.replace(".p01b .tagl{position:absolute;left:30px;bottom:22px;font-family:'JetBrains Mono',monospace;font-size:8.5px;letter-spacing:.2em;color:rgba(19,20,23,.6)}",
            ".p01b .tagl{position:absolute;left:30px;bottom:22px;font-family:'JetBrains Mono',monospace;font-size:9.5px;letter-spacing:.2em;color:rgba(19,20,23,.8)}")
s=s.replace(".p04 .cat{position:absolute;right:26px;top:50%;transform:translateY(-50%);font-family:'JetBrains Mono',monospace;font-weight:700;font-size:9.5px;letter-spacing:.16em;color:rgba(19,20,23,.72)}",
            ".p04 .cat{position:absolute;right:26px;top:50%;transform:translateY(-50%);font-family:'JetBrains Mono',monospace;font-weight:700;font-size:10px;letter-spacing:.16em;color:#131417}")

# --- Sev3: size floor (PDF) ---
s=s.replace(".p06 .tech svg{width:156px!important;margin-top:2px!important}",".p06 .tech svg{width:176px!important;margin-top:2px!important}")
s=s.replace(".p06 .ops .lg{margin-bottom:4px}",".p06 .ops .lg{margin-bottom:3px}")
# chain node labels bigger
s=re.sub(r'(<rect x="6" y="\d+" width="150"[^/]*/><text[^>]*font-size=")7\.4(")',r'\g<1>10.2\g<2>',s)
# gauges: bigger svg + numbers
s=s.replace(".p06 .g1 svg{width:52px!important;height:52px!important}",".p06 .g1 svg{width:60px!important;height:60px!important}")
s=re.sub(r'(text-anchor="middle" font-size=")12\.5(" font-weight="700" fill="#F2F1ED">(?:~20%|7&ndash;8%|50%\+))',r'\g<1>14\g<2>',s)
# conv/ring/arch/origin label bumps
s=s.replace('font-size="7.2" letter-spacing="1.2"','font-size="8.6" letter-spacing="1.2"')      # conv depts (pdf)
s=s.replace('font-size="8.2" font-weight="700" letter-spacing="1.4" fill="#F2F1ED">THE<','font-size="9" font-weight="700" letter-spacing="1.4" fill="#F2F1ED">THE<')
s=s.replace('font-size="8.2" font-weight="700" letter-spacing="1.4" fill="#F2F1ED">CUSTOMER<','font-size="9" font-weight="700" letter-spacing="1.4" fill="#F2F1ED">CUSTOMER<')
s=s.replace('font-size="6.8" letter-spacing="1" fill="#8E8E93"','font-size="7.6" letter-spacing="1" fill="#8E8E93"')   # ring names
s=s.replace('font-size="7.6" letter-spacing="1.1" fill="#F2F1ED"','font-size="8.4" letter-spacing="1.1" fill="#F2F1ED"') # arch labels
s=s.replace('font-size="7.2" letter-spacing="1.3" fill="#8E8E93"','font-size="8" letter-spacing="1.3" fill="#8E8E93"')   # origin milestones
s=s.replace('font-size="7.4" font-weight="700" letter-spacing="1.5" fill="#2FB380">REVENUE','font-size="8.4" font-weight="700" letter-spacing="1.5" fill="#2FB380">REVENUE')
# emerald microcopy sizes
s=s.replace(".p06 .tech .pur{margin-top:5px;font-size:7.6px}",".p06 .tech .pur{margin-top:5px;font-size:9px}")
s=s.replace(".p06 .cosb{display:flex;align-items:center;gap:8px;margin-top:9px;font-family:'JetBrains Mono',monospace;font-weight:700;font-size:8px;",
            ".p06 .cosb{display:flex;align-items:center;gap:8px;margin-top:9px;font-family:'JetBrains Mono',monospace;font-weight:700;font-size:9px;")
s=s.replace(".p12b .intb{display:inline-flex;margin-top:10px;border:1px solid rgba(47,179,128,.45);border-radius:7px;padding:6px 13px;\nfont-family:'JetBrains Mono',monospace;font-weight:600;font-size:8.5px;",
            ".p12b .intb{display:inline-flex;margin-top:10px;border:1px solid rgba(47,179,128,.45);border-radius:7px;padding:6px 13px;\nfont-family:'JetBrains Mono',monospace;font-weight:600;font-size:9.5px;")
s=s.replace(".p12b .phil{margin-top:5px;font-family:'JetBrains Mono',monospace;font-size:9px;",".p12b .phil{margin-top:5px;font-family:'JetBrains Mono',monospace;font-size:9.5px;")
# chips
s=s.replace(".p13 .ich span{border:1px solid var(--grid);border-radius:7px;padding:4px 10px;font-family:'JetBrains Mono',monospace;font-size:7.6px;",
            ".p13 .ich span{border:1px solid var(--grid);border-radius:7px;padding:4px 10px;font-family:'JetBrains Mono',monospace;font-size:9px;")
s=s.replace(".p12b .stackr span{border:1px solid var(--grid);border-radius:7px;padding:5px 10px;font-family:'JetBrains Mono',monospace;font-size:8px;",
            ".p12b .stackr span{border:1px solid var(--grid);border-radius:7px;padding:5px 10px;font-family:'JetBrains Mono',monospace;font-size:9px;")
s=s.replace(".p07 .chip{padding:12px 6px;font-size:8.2px}",".p07 .chip{padding:12px 6px;font-size:9px}")
s=s.replace(".p07 .chip b{font-size:9px;margin-bottom:4px}",".p07 .chip b{font-size:9.6px;margin-bottom:4px}")

io.open("casebook.html","w",encoding="utf-8").write(s)
print("PDF contrast pass done")

# ============================================================ SITE
t=io.open("site.html",encoding="utf-8").read()
t=t.replace("--dim:#5A5B60;","--dim:#5A5B60;"+LBL_DECL,1)

SITE_SWAPS=[
 (".case .biglbl{margin-top:8px;font-family:'JetBrains Mono',monospace;font-size:8.5px;letter-spacing:.22em;color:var(--dim)}",
  ".case .biglbl{margin-top:8px;font-family:'JetBrains Mono',monospace;font-size:10px;letter-spacing:.22em;color:var(--lbl)}"),
 (".case .g1 .gl{margin-top:6px;font-family:'JetBrains Mono',monospace;font-size:8px;letter-spacing:.14em;color:var(--dim);line-height:1.7}",
  ".case .g1 .gl{margin-top:6px;font-family:'JetBrains Mono',monospace;font-size:10px;letter-spacing:.14em;color:var(--lbl);line-height:1.7}"),
 (".et .el{margin-top:7px;font-family:'JetBrains Mono',monospace;font-size:7.8px;letter-spacing:.16em;color:var(--dim);line-height:1.65}",
  ".et .el{margin-top:7px;font-family:'JetBrains Mono',monospace;font-size:9.5px;letter-spacing:.16em;color:var(--lbl);line-height:1.65}"),
 (".why .wl{display:block;font-family:'JetBrains Mono',monospace;font-weight:600;font-size:8px;letter-spacing:.24em;color:var(--dim);margin-bottom:6px}",
  ".why .wl{display:block;font-family:'JetBrains Mono',monospace;font-weight:600;font-size:9.5px;letter-spacing:.24em;color:var(--lbl);margin-bottom:6px}"),
 (".reality .fh{display:flex;justify-content:space-between;font-family:'JetBrains Mono',monospace;font-weight:600;font-size:9px;letter-spacing:.2em;color:var(--dim);margin-bottom:9px}",
  ".reality .fh{display:flex;justify-content:space-between;font-family:'JetBrains Mono',monospace;font-weight:600;font-size:9.5px;letter-spacing:.2em;color:var(--lbl);margin-bottom:9px}"),
 ("#medcoin .outs .k{font-family:'JetBrains Mono',monospace;font-size:8.5px;letter-spacing:.16em;color:var(--dim)}",
  "#medcoin .outs .k{font-family:'JetBrains Mono',monospace;font-size:10px;letter-spacing:.16em;color:var(--lbl)}"),
 ("#final .crow .k{font-family:'JetBrains Mono',monospace;font-size:8.5px;letter-spacing:.2em;color:var(--dim)}",
  "#final .crow .k{font-family:'JetBrains Mono',monospace;font-size:10px;letter-spacing:.2em;color:var(--lbl)}"),
 ("#final .crow .v{font-family:'JetBrains Mono',monospace;font-weight:600;font-size:11.5px;",
  "#final .crow .v{font-family:'JetBrains Mono',monospace;font-weight:600;font-size:12.5px;"),
 (".ringlbl,.looplbl{margin-top:8px;font-family:'JetBrains Mono',monospace;font-size:8.5px;letter-spacing:.18em;color:var(--dim);text-align:center}",
  ".ringlbl,.looplbl{margin-top:8px;font-family:'JetBrains Mono',monospace;font-size:10px;letter-spacing:.18em;color:var(--lbl);text-align:center}"),
 ("#final .ich span{border:1px solid var(--grid);border-radius:8px;padding:6px 12px;font-family:'JetBrains Mono',monospace;font-size:8.6px;",
  "#final .ich span{border:1px solid var(--grid);border-radius:8px;padding:6px 12px;font-family:'JetBrains Mono',monospace;font-size:10px;"),
 ("#tech .stackr span{border:1px solid var(--grid);border-radius:8px;padding:6px 11px;font-family:'JetBrains Mono',monospace;font-size:8.6px;",
  "#tech .stackr span{border:1px solid var(--grid);border-radius:8px;padding:6px 11px;font-family:'JetBrains Mono',monospace;font-size:10px;"),
 (".case .chip{flex:1;min-width:130px;border:1px solid var(--grid);border-radius:9px;padding:12px 10px;text-align:center;\nfont-family:'JetBrains Mono',monospace;font-weight:600;font-size:8.6px;",
  ".case .chip{flex:1;min-width:130px;border:1px solid var(--grid);border-radius:9px;padding:12px 10px;text-align:center;\nfont-family:'JetBrains Mono',monospace;font-weight:600;font-size:10px;"),
 (".intb{display:inline-flex;margin-top:16px;border:1px solid rgba(47,179,128,.45);border-radius:8px;padding:8px 15px;\nfont-family:'JetBrains Mono',monospace;font-weight:600;font-size:9px;",
  ".intb{display:inline-flex;margin-top:16px;border:1px solid rgba(47,179,128,.45);border-radius:8px;padding:8px 15px;\nfont-family:'JetBrains Mono',monospace;font-weight:600;font-size:10.5px;"),
 ("#tech .phil{margin-top:14px;font-family:'JetBrains Mono',monospace;font-size:9.5px;",
  "#tech .phil{margin-top:14px;font-family:'JetBrains Mono',monospace;font-size:10.5px;"),
 (".smeta{margin-top:10px;font-family:'JetBrains Mono',monospace;font-size:10px;",
  ".smeta{margin-top:10px;font-family:'JetBrains Mono',monospace;font-size:11px;"),
 ("#files .fmeta{font-family:'JetBrains Mono',monospace;font-size:10px;",
  "#files .fmeta{font-family:'JetBrains Mono',monospace;font-size:11px;"),
]
cnt=0
for a,b in SITE_SWAPS:
    if a in t: t=t.replace(a,b,1); cnt+=1
print("site swaps:",cnt,"/",len(SITE_SWAPS))

# svg annotation fills + label bumps
t=t.replace('fill="#5A5B60"','fill="#A6A7AC"')
t=t.replace('font-size="7.8" letter-spacing="1.2"','font-size="9.8" letter-spacing="1.2"')   # conv depts
t=t.replace('font-size="8.6" font-weight="700" letter-spacing="1.4" fill="#F2F1ED">THE<','font-size="10" font-weight="700" letter-spacing="1.4" fill="#F2F1ED">THE<')
t=t.replace('font-size="8.6" font-weight="700" letter-spacing="1.4" fill="#F2F1ED">CUSTOMER<','font-size="10" font-weight="700" letter-spacing="1.4" fill="#F2F1ED">CUSTOMER<')
t=t.replace('font-size="7.4" letter-spacing="1" fill="#8E8E93"','font-size="8.6" letter-spacing="1" fill="#8E8E93"')     # ring
t=t.replace('font-size="8.2" letter-spacing="1.2" fill="#F2F1ED"','font-size="9.4" letter-spacing="1.2" fill="#F2F1ED"') # arch
t=t.replace('font-size="7.6" letter-spacing="1.3" fill="#8E8E93"','font-size="9" letter-spacing="1.3" fill="#8E8E93"')   # origin
t=t.replace('font-size="8" letter-spacing="1.3" fill="#F2F1ED"','font-size="10.5" letter-spacing="1.3" fill="#F2F1ED"')  # chain nodes

# cover alphas (site hero on emerald)
t=t.replace("#hero .mfold .quote{color:rgba(19,20,23,.6)}","#hero .mfold .quote{color:rgba(19,20,23,.8)}")
t=t.replace("#hero .mfold .kick{color:rgba(19,20,23,.62)}","#hero .mfold .kick{color:rgba(19,20,23,.78)}")
t=t.replace("#hero .mfold .by{color:rgba(19,20,23,.72)}","#hero .mfold .by{color:rgba(19,20,23,.8)}")
t=t.replace("#hero .tagl{position:absolute;left:30px;bottom:20px;font-family:'JetBrains Mono',monospace;font-size:8.5px;letter-spacing:.2em;color:rgba(19,20,23,.6)}",
            "#hero .tagl{position:absolute;left:30px;bottom:20px;font-family:'JetBrains Mono',monospace;font-size:10px;letter-spacing:.2em;color:rgba(19,20,23,.8)}")
t=t.replace("#files .cat{position:absolute;right:28px;top:50%;transform:translateY(-50%);font-family:'JetBrains Mono',monospace;font-weight:700;font-size:10px;letter-spacing:.16em;color:rgba(19,20,23,.72)}",
            "#files .cat{position:absolute;right:28px;top:50%;transform:translateY(-50%);font-family:'JetBrains Mono',monospace;font-weight:700;font-size:10.5px;letter-spacing:.16em;color:#131417}")
t=t.replace("#hero .by{margin-top:22px;font-family:'JetBrains Mono',monospace;font-size:11px;","#hero .by{margin-top:22px;font-family:'JetBrains Mono',monospace;font-size:11.5px;")

io.open("site.html","w",encoding="utf-8").write(t)
print("SITE contrast pass done:",len(t),"bytes")

# standalone rebuild
full=("<!doctype html>\n<html lang=\"en\">\n<head>\n<meta charset=\"utf-8\">\n"
"<meta name=\"viewport\" content=\"width=device-width,initial-scale=1\">\n"
"<meta name=\"color-scheme\" content=\"dark\">\n</head>\n<body>\n"+t+"\n</body>\n</html>")
io.open("site_standalone.html","w",encoding="utf-8").write(full)
print("standalone rebuilt")
