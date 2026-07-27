# -*- coding: utf-8 -*-
# Fix the visual jump: two-sided flap, case-color frame stays, slower open
import io
s=io.open("site.html",encoding="utf-8").read()

CASES=[
 ("xtix","var(--emb)","#131417","01","XTIX","BUILT FROM ZERO","C-01"),
 ("oasis","var(--brass)","#131417","02","Oasis","LEADERSHIP","C-02"),
 ("eventer","var(--ice)","#131417","03","Eventer","ALIGNMENT","C-03"),
 ("medcoin","var(--ink)","#131417","04","Medcoin","FOUNDER","C-04"),
]
def theater_old(sid,oc,ink,num,nm,cat,code):
    return ('<div class="otx" id="otx-%s" data-sec="%s">\n'
    '  <div class="ots">\n'
    '    <div class="otroom">\n'
    '      <div class="otf" style="--oc:%s;--oink:%s">\n'
    '        <div class="otf-under">\n'
    '          <div class="ou-num">%s</div>\n'
    '          <div class="ou-lines">\n'
    '            <div class="ou-l">CASE FILE %s &mdash; %s</div>\n'
    '            <div class="ou-l">STATUS: <b>DECLASSIFIED</b></div>\n'
    '            <div class="ou-red"></div><div class="ou-red w2"></div>\n'
    '            <div class="ou-l dim">&gt; EVIDENCE ENCLOSED &mdash; CONTINUE</div>\n'
    '          </div>\n'
    '        </div>\n'
    '        <div class="otf-veil"></div>\n'
    '        <div class="otf-cover">\n'
    '          <div class="oc-lip"><b>%s</b><span>FILE %s</span></div>\n'
    '          <div class="oc-eyebrow">CASE FILE &middot; COMMERCIAL ARCHIVE</div>\n'
    '          <div class="oc-cat">%s</div>\n'
    '          <div class="oc-class">&gt; classification: COMMERCIAL<br>&gt; drawer: %s &middot; archive 2026</div>\n'
    '          <div class="oc-barc" aria-hidden="true"><i>%s</i></div>\n'
    '          <div class="oc-conf">CONFIDENTIAL</div>\n'
    '          <span class="oc-hole" style="top:26%%"></span><span class="oc-hole" style="top:44%%"></span>\n'
    '        </div>\n'
    '      </div>\n'
    '      <div class="otdrw">\n'
    '        <div class="od-face">\n'
    '          <span class="od-handle"></span>\n'
    '          <span class="od-lab">ARCHIVE DRAWER %s &middot; COMMERCIAL RECORDS</span>\n'
    '        </div>\n'
    '      </div>\n'
    '      <div class="otstat">PULLING FILE %s &mdash; %s</div>\n'
    '    </div>\n'
    '  </div>\n'
    '</div>')%(sid,sid,oc,ink,num,num,nm.upper(),nm,num,cat,code,code,code,num,nm.upper())

def theater_new(sid,oc,ink,num,nm,cat,code):
    return ('<div class="otx" id="otx-%s" data-sec="%s">\n'
    '  <div class="ots">\n'
    '    <div class="otroom">\n'
    '      <div class="otf" style="--oc:%s;--oink:%s">\n'
    '        <div class="oc-lip"><b>%s</b><span>FILE %s</span></div>\n'
    '        <div class="otf-under">\n'
    '          <div class="ou-num">%s</div>\n'
    '          <div class="ou-lines">\n'
    '            <div class="ou-l">CASE FILE %s &mdash; %s</div>\n'
    '            <div class="ou-l">STATUS: <b>DECLASSIFIED</b></div>\n'
    '            <div class="ou-red"></div><div class="ou-red w2"></div>\n'
    '            <div class="ou-l dim">&gt; EVIDENCE ENCLOSED &mdash; CONTINUE</div>\n'
    '          </div>\n'
    '        </div>\n'
    '        <div class="otf-veil"></div>\n'
    '        <div class="otf-cover">\n'
    '          <div class="oc-face">\n'
    '            <div class="oc-eyebrow">CASE FILE &middot; COMMERCIAL ARCHIVE</div>\n'
    '            <div class="oc-cat">%s</div>\n'
    '            <div class="oc-class">&gt; classification: COMMERCIAL<br>&gt; drawer: %s &middot; archive 2026</div>\n'
    '            <div class="oc-barc" aria-hidden="true"><i>%s</i></div>\n'
    '            <div class="oc-conf">CONFIDENTIAL</div>\n'
    '            <span class="oc-hole" style="top:26%%"></span><span class="oc-hole" style="top:44%%"></span>\n'
    '          </div>\n'
    '          <div class="oc-backf"></div>\n'
    '        </div>\n'
    '      </div>\n'
    '      <div class="otdrw">\n'
    '        <div class="od-face">\n'
    '          <span class="od-handle"></span>\n'
    '          <span class="od-lab">ARCHIVE DRAWER %s &middot; COMMERCIAL RECORDS</span>\n'
    '        </div>\n'
    '      </div>\n'
    '      <div class="otstat">PULLING FILE %s &mdash; %s</div>\n'
    '    </div>\n'
    '  </div>\n'
    '</div>')%(sid,sid,oc,ink,nm,num,num,num,nm.upper(),cat,code,code,code,num,nm.upper())

for c in CASES:
    old=theater_old(*c); new=theater_new(*c)
    assert old in s, "old theater "+c[0]
    s=s.replace(old,new,1)
print("4 theaters restructured")

# ---------- CSS ----------
assert '.otx{height:165vh;position:relative;z-index:5}' in s
s=s.replace('.otx{height:165vh;position:relative;z-index:5}','.otx{height:185vh;position:relative;z-index:5}',1)

OLD_CSS=""".otf{position:absolute;left:50%;top:50%;width:min(680px,74vw);height:min(60vh,470px);
margin:calc(min(60vh,470px)/-2) 0 0 calc(min(680px,74vw)/-2);z-index:1;will-change:transform;transform-style:preserve-3d;
transform:translateY(44vh) scale(.62)}
.otf-cover{position:absolute;inset:0;background:var(--oc);border-radius:0 22px 18px 18px;
transform-origin:50% 0;will-change:transform;backface-visibility:hidden;padding:44px 40px;z-index:3}"""
NEW_CSS=""".otf{position:absolute;left:50%;top:50%;width:min(680px,74vw);height:min(60vh,470px);
margin:calc(min(60vh,470px)/-2) 0 0 calc(min(680px,74vw)/-2);z-index:1;will-change:transform;transform-style:preserve-3d;
transform:translateY(44vh) scale(.62);background:var(--oc);border-radius:0 22px 18px 18px}
.otf-cover{position:absolute;inset:0;border-radius:0 22px 18px 18px;
transform-origin:50% 0;will-change:transform;transform-style:preserve-3d;z-index:3}
.oc-face{position:absolute;inset:0;backface-visibility:hidden;background:var(--oc);border-radius:inherit;padding:44px 40px}
.oc-backf{position:absolute;inset:0;backface-visibility:hidden;transform:rotateX(180deg);border-radius:inherit;
background:var(--oc);background-image:linear-gradient(rgba(19,20,23,.34),rgba(19,20,23,.34))}"""
assert OLD_CSS in s, "otf css"
s=s.replace(OLD_CSS,NEW_CSS,1)

OLD_U=""".otf-under{position:absolute;inset:0;background:var(--card);border:1px solid var(--grid);border-radius:0 22px 18px 18px;
padding:44px 40px;z-index:1;overflow:hidden}"""
NEW_U=""".otf-under{position:absolute;inset:14px 12px 12px;background:var(--card);border-radius:0 16px 12px 12px;
padding:38px 36px;z-index:1;overflow:hidden}
.otf-under .ou-l b{color:var(--oc)}"""
assert OLD_U in s, "under css"
s=s.replace(OLD_U,NEW_U,1)

s=s.replace('.otf-veil{position:absolute;inset:0;background:rgba(19,20,23,.55);border-radius:0 22px 18px 18px;z-index:2;pointer-events:none}',
'.otf-veil{position:absolute;inset:14px 12px 12px;background:rgba(19,20,23,.55);border-radius:0 16px 12px 12px;z-index:2;pointer-events:none}',1)
s=s.replace('.ou-red{margin-top:14px;height:12px;width:62%;background:#0F1013;border-radius:2px}',
'.ou-red{margin-top:14px;height:12px;width:62%;background:#26282D;border-radius:2px}',1)
s=s.replace('.oc-lip{position:absolute;top:-34px;left:0;height:34px;background:var(--oc);border-radius:10px 20px 0 0;',
'.oc-lip{position:absolute;top:-34px;left:0;height:34px;background:var(--oc);border-radius:10px 20px 0 0;z-index:4;',1)

# ---------- JS scrub constants ----------
OLD_JS="""      var pull=eo(clamp(tp/.42));
      th.otf.style.transform='translateY('+((1-pull)*44)+'vh) scale('+(.62+.38*pull)+')';
      var dfade=clamp((tp-.40)/.18);
      th.drw.style.opacity=String(1-dfade);
      th.drw.style.transform='translateX(-50%) translateY('+(eo(dfade)*9)+'vh)';
      var open=eo(clamp((tp-.55)/.30));
      th.cover.style.transform='rotateX('+(-open*112)+'deg)';
      th.veil.style.opacity=String((1-open)*.55);"""
NEW_JS="""      var pull=eo(clamp(tp/.40));
      th.otf.style.transform='translateY('+((1-pull)*44)+'vh) scale('+(.62+.38*pull)+')';
      var dfade=clamp((tp-.38)/.16);
      th.drw.style.opacity=String(1-dfade);
      th.drw.style.transform='translateX(-50%) translateY('+(eo(dfade)*9)+'vh)';
      var open=eo(clamp((tp-.48)/.38));
      th.cover.style.transform='rotateX('+(-open*138)+'deg)';
      th.veil.style.opacity=String((1-open)*.55);"""
assert OLD_JS in s, "scrub js"
s=s.replace(OLD_JS,NEW_JS,1)

OLD_MSG="var msg = tp<.5?('PULLING '+th.lab.replace('PULLING ','')):(tp<.86?'OPENING FILE \\u2026':'FILE OPEN \\u2014 READ \\u2193');"
NEW_MSG="var msg = tp<.48?('PULLING '+th.lab.replace('PULLING ','')):(tp<.84?'OPENING FILE \\u2026':'FILE OPEN \\u2014 READ \\u2193');"
assert OLD_MSG in s, "msg js"
s=s.replace(OLD_MSG,NEW_MSG,1)

io.open("site.html","w",encoding="utf-8").write(s)
full=("<!doctype html>\n<html lang=\"en\">\n<head>\n<meta charset=\"utf-8\">\n"
"<meta name=\"viewport\" content=\"width=device-width,initial-scale=1\">\n"
"<meta name=\"color-scheme\" content=\"dark\">\n</head>\n<body>\n"+s+"\n</body>\n</html>")
io.open("site_standalone.html","w",encoding="utf-8").write(full)
print("two-sided cover + color frame + slower open:",len(s))
