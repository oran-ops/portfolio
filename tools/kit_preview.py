# LOOK AT THE KIT. Renders every icon at 1x and 8x, on white and on the 50% desktop dither,
# plus the face at 1x and 4x and every string the shell actually needs. Written so the art is
# judged by looking at it rather than by trusting the code that drew it.
import os
import sys
from PIL import Image, ImageDraw

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import mac_kit as K

OUT = os.path.dirname(os.path.abspath(__file__))
SCALE = 7
PAD = 14
STRINGS = ["File  Edit  View  Special",
           "Oran Carmon " + chr(0x2014) + " Master File",
           "6 items      0 opened      2018" + chr(0x2013) + "2026",
           "XTIX  OASIS  EVENTER  MEDCOIN  LEADERSHIP  TECH  READ ME"]


def icon_image(name, scale):
    cells = K.rgba(name)
    im = Image.new("RGBA", (32 * scale, 32 * scale), (0, 0, 0, 0))
    d = ImageDraw.Draw(im)
    for y in range(32):
        for x in range(32):
            c = cells[y][x]
            if c:
                d.rectangle([x * scale, y * scale,
                             (x + 1) * scale - 1, (y + 1) * scale - 1], fill=c)
    return im


def dither(w, h):
    im = Image.new("RGB", (w, h), (255, 255, 255))
    d = ImageDraw.Draw(im)
    for y in range(h):
        for x in range(y % 2, w, 2):
            d.point((x, y), (0, 0, 0))
    return im


def text_image(s, scale, fg=(0, 0, 0), bg=(255, 255, 255)):
    w, h = K.text_w(s), 8
    im = Image.new("RGB", (w * scale, h * scale), bg)
    d = ImageDraw.Draw(im)

    def put(x, y):
        d.rectangle([x * scale, y * scale, (x + 1) * scale - 1, (y + 1) * scale - 1], fill=fg)

    K.draw_text(put, s, 0, 0)
    return im


names = K.ORDER + ["folder"]
cell = 32 * SCALE + PAD
W = PAD + len(names) * cell
rows_h = PAD + cell + cell + PAD + 60 + sum((8 * s + 10) for s in (1, 2, 4)) * 1 + 120
sheet = Image.new("RGB", (max(W, 1180), 900), (240, 240, 240))
dr = ImageDraw.Draw(sheet)

# row 1: every icon at 8x on white, as it appears inside the window
dr.rectangle([0, 0, sheet.size[0], PAD + cell], fill=(255, 255, 255))
for i, n in enumerate(names):
    sheet.paste(icon_image(n, SCALE), (PAD + i * cell, PAD), icon_image(n, SCALE))

# row 2: the same icons on the desktop dither, where MEDCOIN's keyline has to survive
y2 = PAD + cell
sheet.paste(dither(sheet.size[0], cell + PAD), (0, y2))
for i, n in enumerate(names):
    sheet.paste(icon_image(n, SCALE), (PAD + i * cell, y2 + PAD // 2), icon_image(n, SCALE))

# row 3: the icons at 1x and 2x -- the sizes they are actually shown at
y3 = y2 + cell + PAD + 10
dr.rectangle([0, y3 - 6, sheet.size[0], y3 + 90], fill=(255, 255, 255))
x = PAD
for n in names:
    sheet.paste(icon_image(n, 1), (x, y3 + 30), icon_image(n, 1))
    sheet.paste(icon_image(n, 2), (x + 40, y3 + 14), icon_image(n, 2))
    x += 130

# row 4: the face
y4 = y3 + 100
for s in (1, 2, 4):
    for st in STRINGS:
        im = text_image(st, s)
        if y4 + im.size[1] > sheet.size[1] - 4:
            break
        sheet.paste(im, (PAD, y4))
        y4 += im.size[1] + 6
    y4 += 8

p = os.path.join(OUT, "_kit_preview.png")
sheet.save(p)
print("wrote %s  %dx%d" % (p, sheet.size[0], sheet.size[1]))
for n in names:
    print("  %-11s %s" % (n, "".join("#" if c else "." for c in K.rgba(n)[16])))
