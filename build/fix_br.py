# -*- coding: utf-8 -*-
import io
s = io.open("site.html", encoding="utf-8").read()
# the JS source contains the escape sequence  literally (backslash-u-0001)
old = "el.innerHTML.replace(/<br\\s*\\/?>/gi,'\\u0001')"
new = "el.innerHTML.replace(/<br\\s*\\/?>/gi,' \\u0001 ')"
assert old in s, "pattern not found"
s = s.replace(old, new, 1)
io.open("site.html", "w", encoding="utf-8").write(s)
print("br tokenization fixed")
