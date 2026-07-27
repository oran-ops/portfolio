# -*- coding: utf-8 -*-
# Repair the two error-trap statements that got a literal newline baked into a string.
import io, re
s = io.open("site.html", encoding="utf-8").read()

pat1 = re.compile(r"\}catch\(e3\)\{window\.__acts3ERR=.*?;\}", re.S)
m1 = pat1.search(s)
assert m1, "trap1 not found"
s = s[:m1.start()] + "}catch(e3){window.__acts3ERR=String(e3&&e3.message||e3);}" + s[m1.end():]

pat2 = re.compile(r"window\.__acts3ERR2=err\.message.*?;", re.S)
m2 = pat2.search(s)
assert m2, "trap2 not found"
s = s[:m2.start()] + "window.__acts3ERR2=String(err&&err.message||err);" + s[m2.end():]

io.open("site.html", "w", encoding="utf-8").write(s)
head = ('<!doctype html>\n<html lang="en">\n<head>\n<meta charset="utf-8">\n'
        '<meta name="viewport" content="width=device-width,initial-scale=1">\n'
        '<meta name="color-scheme" content="dark">\n</head>\n<body>\n')
io.open("site_standalone.html", "w", encoding="utf-8").write(head + s + "\n</body>\n</html>")
print("traps repaired")
