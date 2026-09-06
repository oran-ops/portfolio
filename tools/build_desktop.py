# Assemble lab/desktop.html: the template, with the kit inlined.
#
# Inlined rather than linked because the page has to stand alone -- it is published for review,
# and a page that fetches a sibling file is a page that shows nothing when it is moved.
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
REPO = os.path.dirname(HERE)
sys.path.insert(0, HERE)
import mac_kit as K

TPL = os.path.join(HERE, "desktop_page.html")
OUT = os.path.join(REPO, "lab", "desktop.html")

kit = os.path.join(REPO, "lab", "_kit.js")
K.emit_js(kit)


def read(p):
    with open(p, encoding="utf-8") as fh:
        return fh.read()


parts = {"/*KIT*/": read(kit).strip(),
         "/*SCREEN*/": read(os.path.join(HERE, "screen.js")).strip()}
html = read(TPL)
for mark, body in parts.items():
    if mark not in html:
        raise SystemExit("template has lost its %s marker" % mark)
    html = html.replace(mark, body)

with open(OUT, "w", encoding="utf-8") as fh:
    fh.write(html)

print("lab/desktop.html  %d bytes" % len(html.encode("utf-8")))
for mark, body in sorted(parts.items()):
    print("   %-10s %6d bytes inlined" % (mark.strip("/*"), len(body.encode("utf-8"))))
