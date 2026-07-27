# -*- coding: utf-8 -*-
# Mobile excellence layer — everything scoped to <=680px (desktop untouched).
import io
s = io.open("site.html", encoding="utf-8").read()

# fix legacy wrong-class rule (.dtab never existed; tabs are .itab)
OLD = "@media (max-width:760px){#hero .idx{position:static;margin-bottom:26px}#hero .barc{display:none}#hero .drawer{flex-wrap:wrap}#hero .dtab{min-width:46%}}"
NEW = "@media (max-width:760px){#hero .idx{position:static;margin-bottom:26px}#hero .drawer{flex-wrap:wrap}#hero .itab{min-width:44%}}"
assert OLD in s, "legacy 760 rule"
s = s.replace(OLD, NEW, 1)

MOBILE = """
/* ================= MOBILE EXCELLENCE (<=680px) ================= */
@media (max-width:680px){
 html,body{overflow-x:hidden}
 .wrap{padding-left:16px!important;padding-right:16px!important}
 #rail{display:none!important}
 svg{max-width:100%}
 /* --- hero --- */
 #hero .crumb{font-size:7.5px;letter-spacing:.12em;white-space:normal;line-height:2;padding-right:12px}
 #hero .mfold{border-radius:0 14px 12px 12px}
 #hero .center{padding:0 6px}
 #hero h1{font-size:clamp(27px,8.6vw,38px);letter-spacing:-.028em;line-height:1.04}
 #hero .sub{font-size:15.5px}
 #hero .by{font-size:8.5px;letter-spacing:.18em;line-height:1.9}
 #hero .quote{font-size:12px;padding:0 8px}
 #hero .tagl{font-size:7.5px;letter-spacing:.14em}
 #hero .kick{font-size:7.5px;letter-spacing:.3em}
 #hero .stampP{transform:scale(.78) rotate(-6deg);right:6px;top:14px}
 #hero .drawer{flex-wrap:wrap;gap:8px;padding:0 10px 2px;border-bottom:0}
 #hero .itab{min-width:44%;height:34px;justify-content:center;border-radius:8px 12px 8px 8px}
 #hero .idx{display:none}
 /* --- statement --- */
 #statement .spine{width:20px}
 #statement .sp span{display:none}
 #statement .in{padding-left:26px!important;padding-right:6px}
 #statement .l1,#statement .l2{font-size:clamp(19px,5.9vw,24px);line-height:1.26}
 .memo{font-size:8px;letter-spacing:.16em;padding:7px 12px;margin-bottom:22px}
 /* --- section headers --- */
 .sttl{font-size:clamp(20px,6.6vw,26px)!important;letter-spacing:-.02em}
 .smeta{font-size:8px;letter-spacing:.1em}
 .shead{flex-wrap:wrap;gap:8px}
 .shead .tok{font-size:7.5px;padding:5px 9px}
 .secnum{display:none}
 /* --- folders & stamps --- */
 .rstampS{transform:scale(.78) rotate(-6deg)!important;right:4px!important}
 .tabrow .tB{display:none}
 .frail{display:none}
 .folder{border-radius:0 12px 10px 10px}
 /* --- grids collapse --- */
 .grid2c,.cols2,.tools,.bgrid,.pgrid,.stackr,#philosophy .grid{grid-template-columns:1fr!important}
 .chips{gap:7px}
 /* --- evidence & numbers --- */
 .bignum{font-size:clamp(34px,10.5vw,44px)}
 .outs{width:100%}
 /* --- charts pan instead of squeeze --- */
 .archw{overflow-x:auto;-webkit-overflow-scrolling:touch}
 .archw svg{min-width:620px}
 .fz{overflow-x:auto;-webkit-overflow-scrolling:touch}
 .fz svg{min-width:560px}
 /* --- ticker --- */
 .ticker .tk{font-size:8px;letter-spacing:.2em}
 /* --- case index cards --- */
 .hintro .bigt{font-size:clamp(30px,10vw,40px)}
 .hintro .fmeta{font-size:8.5px;letter-spacing:.12em}
 .hfolder{padding:30px 18px 78px}
 .hfolder .hcat{font-size:clamp(24px,8vw,32px)}
 .hfolder .hdoss{font-size:10.5px;line-height:1.7}
 .hfolder .hcta{left:18px;bottom:22px;font-size:9.5px;padding:9px 13px}
 /* --- quotes --- */
 .sigq .qx,.lessq .qx,.lessq2 .qx,.quote2 .qx{font-size:13.5px!important;line-height:1.45}
 /* --- contact & footer --- */
 #final .card{margin-top:26px}
 .crow{gap:8px}
 .crow b,.crow span{font-size:10.5px;letter-spacing:.06em;overflow-wrap:anywhere}
 footer{flex-wrap:wrap;gap:6px;font-size:7.5px;letter-spacing:.14em;padding:14px 16px}
 /* --- boot gate --- */
 #boot .bl,#boot .bl2{font-size:8px;letter-spacing:.2em;padding:0 14px;text-align:center}
 #bootgate{font-size:10.5px;padding:12px 20px;letter-spacing:.22em}
}
"""
s = s.replace("</style>", MOBILE + "</style>", 1)

io.open("site.html", "w", encoding="utf-8").write(s)
head = ('<!doctype html>\n<html lang="en">\n<head>\n<meta charset="utf-8">\n'
        '<meta name="viewport" content="width=device-width,initial-scale=1">\n'
        '<meta name="color-scheme" content="dark">\n</head>\n<body>\n')
io.open("site_standalone.html", "w", encoding="utf-8").write(head + s + "\n</body>\n</html>")
print("mobile layer installed")
