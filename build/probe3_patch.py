# -*- coding: utf-8 -*-
# QA probe: &probe3=1 writes arc state into document.title after 2.2s
import io
s = io.open("site.html", encoding="utf-8").read()
ANCH = "requestAnimationFrame(loop);\nwindow.__acts3OK=true;"
ADD = """requestAnimationFrame(loop);
if(q.get('probe3')==='1'){
  setTimeout(function(){
    try{
      document.title='PROBE3::'+JSON.stringify({
        meter:(document.getElementById('cmn')||{}).textContent,
        cc:(document.getElementById('ccstamp')||{}).textContent,
        tag:(document.getElementById('evtxt')||{}).textContent,
        tagTf:document.getElementById('evtag').style.transform.slice(0,40),
        teaser:document.getElementById('teaser').style.transform.slice(0,40),
        it:secs.interlude?Math.round(secs.interlude.t):null,
        oth:theaters.oasis?Math.round(theaters.oasis.t):null,
        eth:theaters.eventer?Math.round(theaters.eventer.t):null,
        mth:theaters.medcoin?Math.round(theaters.medcoin.t):null,
        fin:secs.final?Math.round(secs.final.t):null,
        evPlayed:evPlayed,mdPlayed:mdPlayed
      });
    }catch(e){document.title='PROBE3ERR::'+e.message}
  },2200);
}
window.__acts3OK=true;"""
assert ANCH in s, "probe anchor"
s = s.replace(ANCH, ADD, 1)
io.open("site.html", "w", encoding="utf-8").write(s)
head = ('<!doctype html>\n<html lang="en">\n<head>\n<meta charset="utf-8">\n'
        '<meta name="viewport" content="width=device-width,initial-scale=1">\n'
        '<meta name="color-scheme" content="dark">\n</head>\n<body>\n')
io.open("site_standalone.html", "w", encoding="utf-8").write(head + s + "\n</body>\n</html>")

WRAP = ('<!doctype html><html><head><meta charset="utf-8"><title>waiting</title></head>\n'
        '<body style="margin:0;background:#131417">\n'
        '<iframe id="f" style="width:1280px;height:720px;border:0"></iframe>\n'
        '<script>\n'
        'var qs=new URLSearchParams(location.search);\n'
        'var y=qs.get("y")||"0";\n'
        'document.getElementById("f").src="site_standalone.html?noboot=1&force=1&probe3=1&y="+y;\n'
        'var iv=setInterval(function(){\n'
        '  try{var t=document.getElementById("f").contentDocument.title;\n'
        '    if(t&&t.indexOf("PROBE3")===0){document.title=t;clearInterval(iv);}\n'
        '  }catch(e){document.title="ERR::"+e.message;clearInterval(iv);}\n'
        '},250);\n'
        '</script></body></html>')
io.open("wrap1280.html", "w", encoding="utf-8").write(WRAP)
print("probe3 + wrap1280 ready")
