# -*- coding: utf-8 -*-
# Tone lift: charcoal ladder up 1-2 steps (toward matte charcoal-gray),
# matching dark-ink text lifted the same way. Applies to BOTH files.
import io

SWAPS = [
    # neutral ladder
    ("#131417", "#191A1F"),                # bg + dark ink-on-tab
    ("rgba(19,20,23,", "rgba(25,26,31,"),  # dark-ink alphas
    ("#1A1B1F", "#202127"),                # card
    ("#1F2126", "#25262D"),                # card2
    ("#2E3036", "#33353C"),                # grid
    ("#46494F", "#4B4E55"),                # grid2
    ("#101114", "#16171C"),                # drawer face / lip bar
    ("#0B0C0E", "#111217"),                # drawer inner shadow strip
    ("#0F1013", "#15161B"),                # redact bars (dark)
    ("#26282D", "#2C2D33"),                # handle / light redacts
    ("#5A5B60", "#606167"),                # dim text nudged up for contrast
]
# site relight tints (acts5 LIGHTS) — same delta (+6,+6,+8)
TINTS = [
    ("'#14201B'", "'#1A2621'"),
    ("'#1B1815'", "'#211E1D'"),
    ("'#141920'", "'#1A1F28'"),
    ("'#17181B'", "'#1D1E23'"),
]

def apply(path, tints):
    s = io.open(path, encoding="utf-8").read()
    total = 0
    for a, b in SWAPS:
        n = s.count(a)
        s = s.replace(a, b)
        total += n
        print("  %-22s -> %-12s x%d" % (a, b, n))
    if tints:
        for a, b in TINTS:
            n = s.count(a)
            s = s.replace(a, b)
            print("  %-22s -> %-12s x%d" % (a, b, n))
    io.open(path, "w", encoding="utf-8").write(s)
    print(path, "total neutral swaps:", total)
    return s

print("== casebook.html ==")
apply("casebook.html", tints=False)
print("== site.html ==")
s = apply("site.html", tints=True)
head = ('<!doctype html>\n<html lang="en">\n<head>\n<meta charset="utf-8">\n'
        '<meta name="viewport" content="width=device-width,initial-scale=1">\n'
        '<meta name="color-scheme" content="dark">\n</head>\n<body>\n')
io.open("site_standalone.html", "w", encoding="utf-8").write(head + s + "\n</body>\n</html>")
print("standalone rebuilt")
