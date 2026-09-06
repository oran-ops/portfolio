# THE 1984 KIT -- one source for the pixel art, used by BOTH the web shell and the CRT texture.
#
# Everything the Macintosh layer draws comes from this file: a bitmap face, seven document
# icons, one folder, and the window chrome constants. It is authored once here and emitted as
# JS for the browser, so the screen inside the 3D CRT and the screen the reader lands on after
# the camera flight are literally the same pixels. Two copies of pixel art drift; one cannot.
#
# LICENCE, stated because it constrains the design (docs/KIT_OPTIONS.md D15, UNCONFIRMED):
# Chicago, Geneva and the System 6 icons are Apple's. Nothing here is extracted from a ROM, a
# disk image or a font file. The face below is drawn from scratch on a 5x7 cell; the icons are
# drawn from scratch on the ICN#-style rules the doc sets out:
#   * 1 px black keyline
#   * as few black pixels INSIDE as possible -- selection inverts the bitmap, and a mostly
#     black icon looks the same selected as unselected
#   * silhouette first: two icons of different KIND must differ at 32x32 in outline alone
#   * one light direction (upper left) and one outline weight across the whole set
# The four case files share a silhouette on purpose -- they are the same kind of thing, and
# colour is what separates them. MEDCOIN is paper white, which would vanish on a white window,
# so its keyline is doubled. That is the period answer to a light icon, not a new colour.
import json
import os

HERE = os.path.dirname(os.path.abspath(__file__))
REPO = os.path.dirname(HERE)

# ---------------------------------------------------------- the palette, from ARCHITECTURE 8.1
EMB = (0x2F, 0xB3, 0x80)      # XTIX, leadership, tech, the letter
BRASS = (0xE0, 0xA4, 0x58)    # OASIS
ICE = (0x5E, 0x8F, 0xBF)      # EVENTER
INK = (0xF2, 0xF1, 0xED)      # MEDCOIN, and paper


def mix(a, b, t):
    return tuple(int(round(a[i] + (b[i] - a[i]) * t)) for i in range(3))


def light(c):
    return mix(c, (255, 255, 255), 0.45)


def dark(c):
    return mix(c, (0, 0, 0), 0.32)


# ---------------------------------------------------------------------------------- the face
# 5 x 7 caps on an 8-row cell; row 7 carries descenders. Proportional: the advance is measured
# from the glyph, so nothing is hand-spaced and nothing can drift.
F = {}
F["A"] = "01110 10001 10001 11111 10001 10001 10001 00000"
F["B"] = "11110 10001 10001 11110 10001 10001 11110 00000"
F["C"] = "01110 10001 10000 10000 10000 10001 01110 00000"
F["D"] = "11110 10001 10001 10001 10001 10001 11110 00000"
F["E"] = "11111 10000 10000 11110 10000 10000 11111 00000"
F["F"] = "11111 10000 10000 11110 10000 10000 10000 00000"
F["G"] = "01110 10001 10000 10111 10001 10001 01111 00000"
F["H"] = "10001 10001 10001 11111 10001 10001 10001 00000"
F["I"] = "111 010 010 010 010 010 111 000"
F["J"] = "00111 00010 00010 00010 00010 10010 01100 00000"
F["K"] = "10001 10010 10100 11000 10100 10010 10001 00000"
F["L"] = "10000 10000 10000 10000 10000 10000 11111 00000"
F["M"] = "10001 11011 10101 10101 10001 10001 10001 00000"
F["N"] = "10001 11001 10101 10011 10001 10001 10001 00000"
F["O"] = "01110 10001 10001 10001 10001 10001 01110 00000"
F["P"] = "11110 10001 10001 11110 10000 10000 10000 00000"
F["Q"] = "01110 10001 10001 10001 10101 10010 01101 00000"
F["R"] = "11110 10001 10001 11110 10100 10010 10001 00000"
F["S"] = "01111 10000 10000 01110 00001 00001 11110 00000"
F["T"] = "11111 00100 00100 00100 00100 00100 00100 00000"
F["U"] = "10001 10001 10001 10001 10001 10001 01110 00000"
F["V"] = "10001 10001 10001 10001 10001 01010 00100 00000"
F["W"] = "10001 10001 10001 10101 10101 11011 10001 00000"
F["X"] = "10001 10001 01010 00100 01010 10001 10001 00000"
F["Y"] = "10001 10001 01010 00100 00100 00100 00100 00000"
F["Z"] = "11111 00001 00010 00100 01000 10000 11111 00000"
F["0"] = "01110 10011 10011 10101 11001 11001 01110 00000"
F["1"] = "00100 01100 00100 00100 00100 00100 01110 00000"
F["2"] = "01110 10001 00001 00010 00100 01000 11111 00000"
F["3"] = "11111 00010 00100 00010 00001 10001 01110 00000"
F["4"] = "00010 00110 01010 10010 11111 00010 00010 00000"
F["5"] = "11111 10000 11110 00001 00001 10001 01110 00000"
F["6"] = "00110 01000 10000 11110 10001 10001 01110 00000"
F["7"] = "11111 00001 00010 00100 01000 01000 01000 00000"
F["8"] = "01110 10001 10001 01110 10001 10001 01110 00000"
F["9"] = "01110 10001 10001 01111 00001 00010 01100 00000"
F["a"] = "00000 00000 01110 00001 01111 10001 01111 00000"
F["b"] = "10000 10000 11110 10001 10001 10001 11110 00000"
F["c"] = "00000 00000 01110 10001 10000 10001 01110 00000"
F["d"] = "00001 00001 01111 10001 10001 10001 01111 00000"
F["e"] = "00000 00000 01110 10001 11111 10000 01110 00000"
F["f"] = "00110 01001 01000 11110 01000 01000 01000 00000"
F["g"] = "00000 00000 01111 10001 10001 01111 00001 01110"
F["h"] = "10000 10000 11110 10001 10001 10001 10001 00000"
F["i"] = "010 000 110 010 010 010 111 000"
F["j"] = "00010 00000 00110 00010 00010 00010 10010 01100"
F["k"] = "10000 10000 10010 10100 11000 10100 10010 00000"
F["l"] = "110 010 010 010 010 010 111 000"
F["m"] = "00000 00000 11010 10101 10101 10101 10101 00000"
F["n"] = "00000 00000 11110 10001 10001 10001 10001 00000"
F["o"] = "00000 00000 01110 10001 10001 10001 01110 00000"
F["p"] = "00000 00000 11110 10001 10001 11110 10000 10000"
F["q"] = "00000 00000 01111 10001 10001 01111 00001 00001"
F["r"] = "00000 00000 10110 11001 10000 10000 10000 00000"
F["s"] = "00000 00000 01111 10000 01110 00001 11110 00000"
F["t"] = "01000 01000 11110 01000 01000 01001 00110 00000"
F["u"] = "00000 00000 10001 10001 10001 10011 01101 00000"
F["v"] = "00000 00000 10001 10001 10001 01010 00100 00000"
F["w"] = "00000 00000 10001 10001 10101 10101 01010 00000"
F["x"] = "00000 00000 10001 01010 00100 01010 10001 00000"
F["y"] = "00000 00000 10001 10001 10001 01111 00001 01110"
F["z"] = "00000 00000 11111 00010 00100 01000 11111 00000"
F[" "] = "00 00 00 00 00 00 00 00"
F["-"] = "000 000 000 111 000 000 000 000"
F[chr(0x2013)] = "00000 00000 00000 11111 00000 00000 00000 00000"
F[chr(0x2014)] = "0000000 0000000 0000000 1111111 0000000 0000000 0000000 0000000"
F["."] = "0 0 0 0 0 0 1 0"
F[","] = "00 00 00 00 00 00 01 10"
F["/"] = "00001 00001 00010 00100 01000 10000 10000 00000"

FONT = {k: v.split(" ") for k, v in F.items()}


def glyph(ch):
    return FONT.get(ch, FONT["."])


def adv(ch):
    """Advance width: the glyph's own width plus one column of side bearing."""
    return len(glyph(ch)[0]) + 1


def text_w(s):
    return sum(adv(c) for c in s) - (1 if s else 0)


def draw_text(put, s, x, y):
    """Stamp a string with put(x, y). y is the TOP of the 8-row cell."""
    for ch in s:
        g = glyph(ch)
        for j, row in enumerate(g):
            for i, b in enumerate(row):
                if b == "1":
                    put(x + i, y + j)
        x += adv(ch)
    return x


# --------------------------------------------------------------------------------- the icons
# Grid characters: . transparent  K black  C colour  L light  S dark  W white
N = 32


def grid():
    return [["."] * N for _ in range(N)]


def px(g, x, y, c):
    if 0 <= x < N and 0 <= y < N:
        g[y][x] = c


def hl(g, y, x0, x1, c):
    for x in range(x0, x1 + 1):
        px(g, x, y, c)


def vl(g, x, y0, y1, c):
    for y in range(y0, y1 + 1):
        px(g, x, y, c)


def box(g, x0, y0, x1, y1, fill, edge=None):
    for y in range(y0, y1 + 1):
        for x in range(x0, x1 + 1):
            px(g, x, y, fill)
    if edge:
        hl(g, y0, x0, x1, edge)
        hl(g, y1, x0, x1, edge)
        vl(g, x0, y0, y1, edge)
        vl(g, x1, y0, y1, edge)


def thicken(g):
    """Double the OUTER keyline only. Black grows into transparency, so the interior -- and
    every interior black line -- is untouched. This is the period answer to a light icon."""
    add = []
    for y in range(N):
        for x in range(N):
            if g[y][x] == "K":
                for dy in (-1, 0, 1):
                    for dx in (-1, 0, 1):
                        nx, ny = x + dx, y + dy
                        if 0 <= nx < N and 0 <= ny < N and g[ny][nx] == ".":
                            add.append((nx, ny))
    for x, y in add:
        g[y][x] = "K"
    return g


def case_file():
    """A document with the top-right corner turned down. x 7..24, y 3..29."""
    g = grid()
    box(g, 7, 12, 24, 29, "C", "K")
    for y in range(3, 12):
        d = 16 + (y - 3)                  # the cut edge walks right one pixel a row
        px(g, 7, y, "K")
        for x in range(8, 16):
            px(g, x, y, "C")
        for x in range(16, d):
            px(g, x, y, "L")              # the turned-back flap, seen from its back
        px(g, d, y, "K")
    hl(g, 3, 7, 16, "K")
    hl(g, 12, 16, 24, "K")                # the fold's lower edge
    hl(g, 13, 8, 23, "L")                 # lit from the upper left
    vl(g, 8, 13, 27, "L")
    hl(g, 28, 9, 23, "S")
    vl(g, 23, 14, 28, "S")
    for i, y in enumerate((16, 19, 22, 25)):
        hl(g, y, 10, 21 if i < 3 else 17, "S")   # ruled text, ragged last line
    return g


def notepad():
    """A ruled pad on a spiral binding. Silhouette: square, with THREE rings breaking the top
    edge. Five thin ones read as a comb at 32 px -- three fat ones read as a spiral."""
    g = grid()
    box(g, 4, 9, 27, 29, "C", "K")
    box(g, 5, 10, 26, 14, "S", None)      # the binding band, which must stay visible
    hl(g, 15, 4, 27, "K")
    for cx in (9, 16, 23):                # each loop crosses the pad's top edge, 4 up 2 down
        box(g, cx - 1, 5, cx + 2, 11, "W", "K")
    hl(g, 16, 5, 26, "L")
    vl(g, 5, 16, 28, "L")
    hl(g, 28, 6, 26, "S")
    vl(g, 26, 17, 28, "S")
    for i, y in enumerate((19, 22, 25, 28)):
        hl(g, y, 8, 23 if i < 3 else 18, "S")
    return g


def suitcase():
    """The system suitcase. Silhouette: a wide box with a handle standing above it. ONE central
    clasp, not two latches -- two read as a barbell and cost twice the black."""
    g = grid()
    hl(g, 5, 12, 19, "K")
    hl(g, 6, 12, 19, "K")
    vl(g, 12, 7, 10, "K")
    vl(g, 13, 7, 10, "K")
    vl(g, 18, 7, 10, "K")
    vl(g, 19, 7, 10, "K")
    box(g, 3, 10, 28, 27, "C", "K")
    hl(g, 11, 4, 27, "L")
    vl(g, 4, 11, 25, "L")
    hl(g, 26, 5, 27, "S")
    vl(g, 27, 12, 26, "S")
    hl(g, 18, 3, 28, "K")                 # the case opening
    hl(g, 19, 4, 27, "L")                 # and the light catching the lower lip
    box(g, 13, 16, 18, 21, "L", "K")      # the clasp, centred on the opening
    hl(g, 18, 14, 17, "S")
    return g


def letter():
    """A sealed letter. Silhouette: the only landscape icon, and the only one with a disc.
    The flap falls at 2:1, not 45 degrees -- a 45 degree flap on a 26 px envelope reaches
    almost to the floor and leaves the seal nowhere to sit."""
    g = grid()
    box(g, 3, 9, 28, 26, "C", "K")
    for i in range(0, 7):                 # 2 px across for every 1 px down
        for x in range(3 + i * 2, 29 - i * 2):
            px(g, x, 9 + i, "L")
        px(g, 3 + i * 2, 9 + i, "K")
        px(g, 4 + i * 2, 9 + i, "K")
        px(g, 28 - i * 2, 9 + i, "K")
        px(g, 27 - i * 2, 9 + i, "K")
    hl(g, 9, 3, 28, "K")
    hl(g, 10, 4, 27, "L")
    vl(g, 3, 9, 26, "K")
    vl(g, 28, 9, 26, "K")
    hl(g, 26, 3, 28, "K")
    hl(g, 25, 4, 27, "S")
    ring = [(-3, -4), (-2, -4), (-1, -4), (0, -4), (1, -4), (2, -4),
            (-4, -3), (3, -3), (-4, -2), (3, -2), (-4, -1), (3, -1),
            (-4, 0), (3, 0), (-4, 1), (3, 1), (-4, 2), (3, 2),
            (-3, 3), (-2, 3), (-1, 3), (0, 3), (1, 3), (2, 3)]
    for dx in range(-3, 3):
        for dy in range(-3, 3):
            px(g, 16 + dx, 18 + dy, "W")
    for dx, dy in ring:
        px(g, 16 + dx, 18 + dy, "K")
    for dx, dy in ((-1, -1), (0, -1), (-1, 0), (0, 0), (-2, 0), (1, -1)):
        px(g, 16 + dx, 18 + dy, "S")      # the mark pressed into the wax
    return g


def folder():
    """The shut Master File folder. The back leaf's tab steps DOWN into the front leaf -- a tab
    drawn as a separate box on top reads as a box on top."""
    g = grid()
    box(g, 3, 11, 28, 27, "C", "K")
    box(g, 3, 7, 14, 12, "C", None)       # the tab is part of the back leaf, not a lid
    hl(g, 7, 3, 14, "K")
    vl(g, 3, 7, 11, "K")
    for i in range(3):                    # and it steps down to meet the front leaf
        px(g, 15 + i, 8 + i, "K")
        px(g, 15 + i, 9 + i, "K")
        for x in range(15 + i, 28):
            px(g, x, 10 + i, "C")
    hl(g, 8, 4, 14, "L")
    hl(g, 13, 3, 28, "K")                 # the seam where the front leaf begins
    hl(g, 14, 4, 27, "L")                 # the front leaf's top edge catches the light
    vl(g, 4, 14, 25, "L")
    hl(g, 26, 5, 27, "S")
    vl(g, 27, 15, 26, "S")
    return g


ICONS = {
    "xtix": (case_file(), EMB),
    "oasis": (case_file(), BRASS),
    "eventer": (case_file(), ICE),
    "medcoin": (thicken(case_file()), INK),
    "leadership": (notepad(), EMB),
    "tech": (suitcase(), EMB),
    "final": (letter(), EMB),
    "folder": (folder(), EMB),
}

LABELS = {"xtix": "XTIX", "oasis": "OASIS", "eventer": "EVENTER", "medcoin": "MEDCOIN",
          "leadership": "LEADERSHIP", "tech": "TECH", "final": "READ ME",
          "folder": "Oran Carmon " + chr(0x2014) + " Master File"}

ORDER = ["xtix", "oasis", "eventer", "medcoin", "leadership", "tech", "final"]


def palette(base):
    return {"K": (0, 0, 0), "W": (255, 255, 255), "C": base,
            "L": light(base), "S": dark(base)}


def rgba(name):
    """The icon as a 32x32 list of RGBA tuples; None where transparent."""
    g, base = ICONS[name]
    p = palette(base)
    return [[(p[c] + (255,)) if c in p else None for c in row] for row in g]


def black_budget(name):
    g = ICONS[name][0]
    ink = sum(1 for row in g for c in row if c == "K")
    body = sum(1 for row in g for c in row if c != ".")
    return ink, body, (100.0 * ink / body if body else 0)


def emit_js(path):
    data = {
        "font": {k: v for k, v in FONT.items()},
        "icons": {k: ["".join(r) for r in v[0]] for k, v in ICONS.items()},
        "colour": {k: {"C": list(v[1]), "L": list(light(v[1])), "S": list(dark(v[1])),
                       "K": [0, 0, 0], "W": [255, 255, 255]} for k, v in ICONS.items()},
        "labels": LABELS,
        "order": ORDER,
    }
    with open(path, "w", encoding="utf-8") as fh:
        fh.write("// GENERATED by tools/mac_kit.py -- do not edit by hand.\n")
        fh.write("window.KIT=")
        json.dump(data, fh, ensure_ascii=False, separators=(",", ":"))
        fh.write(";\n")
    return os.path.getsize(path)


if __name__ == "__main__":
    n = emit_js(os.path.join(REPO, "lab", "_kit.js"))
    print("lab/_kit.js  %d bytes" % n)
    print("%-12s %6s %6s %7s" % ("icon", "black", "body", "black%"))
    for k in ORDER + ["folder"]:
        ink, body, pc = black_budget(k)
        print("%-12s %6d %6d %6.1f%%" % (k, ink, body, pc))
    print("face: %d glyphs, cap height 7 on an 8-row cell" % len(FONT))
