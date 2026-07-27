# -*- coding: utf-8 -*-
import io,re
p="art_body2.html"; s=io.open(p,encoding="utf-8").read()

# 1) ambient SVG hardcoded hex -> CSS vars (so palettes re-theme them)
amb=[('fill="#EFDCCC"','style="fill:var(--terra-soft)"'),
('stroke="#C0724A"','style="stroke:var(--terra)"'),
('fill="#C0724A"','style="fill:var(--terra)"'),
('fill="#A75E38"','style="fill:var(--terra2)"'),
('stroke="#8E9C78"','style="stroke:var(--sage)"'),
('stroke="#D6D0C2"','style="stroke:var(--stone)"'),
('stroke="#8B8378"','style="stroke:var(--muted)"'),
('fill="#8E9C78"','style="fill:var(--sage)"')]
for a,b in amb: s=s.replace(a,b)

# 2) palette switcher UI + logic (before closing script tag block)
ui=(
'<div class="palbar" role="group" aria-label="Palette picker">\n'
'  <div class="pl">Palette</div>\n'
'  <button class="pw sel" data-pal="builder" title="Warm Builder"><span style="background:conic-gradient(#C0724A 0 50%,#33302A 50% 100%)"></span>Warm Builder</button>\n'
'  <button class="pw" data-pal="trust" title="Trust &amp; Growth"><span style="background:conic-gradient(#4E7A5A 0 50%,#24313C 50% 100%)"></span>Trust &amp; Growth</button>\n'
'  <button class="pw" data-pal="premium" title="Revenue Premium"><span style="background:conic-gradient(#A8813C 0 50%,#2B322C 50% 100%)"></span>Revenue Premium</button>\n'
'</div>\n')
css=(
".palbar{position:fixed;left:16px;bottom:16px;z-index:30;background:var(--paper2);border:1px solid var(--line2);"
"border-radius:14px;padding:10px 12px;display:flex;align-items:center;gap:10px;box-shadow:0 8px 30px rgba(40,40,36,.10)}\n"
".palbar .pl{font-weight:600;font-size:10px;letter-spacing:.16em;text-transform:uppercase;color:var(--muted)}\n"
".palbar .pw{display:flex;align-items:center;gap:7px;font-family:var(--sans);font-weight:600;font-size:11px;color:var(--muted);"
"background:none;border:1px solid transparent;border-radius:10px;padding:5px 9px;cursor:pointer;transition:all .25s}\n"
".palbar .pw span{width:18px;height:18px;border-radius:50%;display:block;border:1.5px solid rgba(0,0,0,.08)}\n"
".palbar .pw:hover{border-color:var(--line2)}\n"
".palbar .pw.sel{border-color:var(--terra);color:var(--ink)}\n")
s=s.replace("@media (max-width:820px){", css+"@media (max-width:820px){",1)
s=s.replace('<div class="badge">', ui+'<div class="badge">',1)

js=(
"  var PALS={\n"
"   builder:{paper:'#FAF9F6',paper2:'#FFFFFF',ink:'#33302A',ink2:'#4B4234',muted:'#8B8378',soft:'#B9B1A2',line:'#ECE7DC',line2:'#DFD8C9','terra':'#C0724A','terra2':'#A75E38','terra-soft':'#EFDCCC',sage:'#8E9C78','sage-soft':'#E2E6D6',stone:'#D6D0C2'},\n"
"   trust:{paper:'#F8F9F8',paper2:'#FFFFFF',ink:'#24313C',ink2:'#3A4754',muted:'#76818B',soft:'#A9B2BA',line:'#E5E8E5',line2:'#D4D9D4','terra':'#4E7A5A','terra2':'#3D6348','terra-soft':'#DCE8DE',sage:'#38678F','sage-soft':'#DAE4EC',stone:'#CBD1CB'},\n"
"   premium:{paper:'#FAF8F3',paper2:'#FFFFFF',ink:'#2B322C',ink2:'#41493F',muted:'#7E7F72',soft:'#AEAC9B',line:'#E9E4D6',line2:'#DBD4C1','terra':'#A8813C','terra2':'#8C6A2E','terra-soft':'#EADFC4',sage:'#3E5C4B','sage-soft':'#D8E2DB',stone:'#D2CCBB'}};\n"
"  document.querySelectorAll('.pw').forEach(function(b){b.addEventListener('click',function(){\n"
"    document.querySelectorAll('.pw').forEach(function(x){x.classList.remove('sel')});b.classList.add('sel');\n"
"    var pal=PALS[b.getAttribute('data-pal')];for(var k in pal){document.documentElement.style.setProperty('--'+k,pal[k]);}\n"
"  });});\n")
s=s.replace("})();\n</script>", js+"})();\n</script>")

io.open(p,"w",encoding="utf-8").write(s)

# 3) rebuild artifact.html with fonts
warm=io.open("fonts/fonts_warm.css",encoding="utf-8").read()
heebo="\n".join(b for b in re.findall(r"@font-face\{[^}]*\}",warm) if "Heebo" in b)
fraunces=io.open("fonts/fonts_fraunces.css",encoding="utf-8").read()
out="<title>The Commercial Builder - Oran Carmon</title>\n"+s.replace("/*__FONTS__*/",heebo+"\n"+fraunces)
io.open("artifact.html","w",encoding="utf-8").write(out)
print("palette switcher added; artifact bytes:",len(out))
