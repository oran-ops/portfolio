# -*- coding: utf-8 -*-
# QA y-shim: retry scrollTo until it sticks (headless late-layout clamp)
import io
s = io.open("site.html", encoding="utf-8").read()
OLD = """  if(q.get('static')==='1'){document.body.style.marginTop=(-yv)+'px';}
  else{setTimeout(function(){window.scrollTo(0,yv)},700);setTimeout(function(){window.scrollTo(0,yv)},1600);}"""
NEW = """  if(q.get('static')==='1'){document.body.style.marginTop=(-yv)+'px';}
  else{
    var ytry=0,yiv=setInterval(function(){
      ytry++;
      if(Math.abs(window.pageYOffset-yv)>6)window.scrollTo(0,yv);
      if(ytry>16||Math.abs(window.pageYOffset-yv)<=6&&ytry>4)clearInterval(yiv);
    },200);
  }"""
assert OLD in s, "shim anchor"
s = s.replace(OLD, NEW, 1)
# probe later, after shim settles
s = s.replace("},2200);\n  }catch(e){document.title='PROBE3ERR::'+e.message}", "},2200);\n  }catch(e){document.title='PROBE3ERR::'+e.message}", 1)
OLD2 = "      });\n    }catch(e){document.title='PROBE3ERR::'+e.message}\n  },2200);"
NEW2 = "      });\n    }catch(e){document.title='PROBE3ERR::'+e.message}\n  },3600);"
assert OLD2 in s, "probe delay anchor"
s = s.replace(OLD2, NEW2, 1)
io.open("site.html", "w", encoding="utf-8").write(s)
head = ('<!doctype html>\n<html lang="en">\n<head>\n<meta charset="utf-8">\n'
        '<meta name="viewport" content="width=device-width,initial-scale=1">\n'
        '<meta name="color-scheme" content="dark">\n</head>\n<body>\n')
io.open("site_standalone.html", "w", encoding="utf-8").write(head + s + "\n</body>\n</html>")
print("shim retry + probe@3600 done")
