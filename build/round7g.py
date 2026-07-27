# -*- coding: utf-8 -*-
# Round 7g — make every closing quote a direct child of its card, so the pin to the
# card's bottom edge resolves against the card on every page (p11 was resolving
# against an inner grid and vanished).
import io, re

p = 'casebook.html'
s = io.open(p, encoding='utf-8').read()
TAG = re.compile(r'<div class="(lesson|lessq2|insight|sigq|quote2)\b[^"]*"[^>]*>')

def close_of(txt, open_start):
    """index just past the </div> that closes the div opening at open_start"""
    i = txt.find('>', open_start) + 1
    depth = 1
    for m in re.finditer(r'<(/?)div\b[^>]*>', txt[i:]):
        depth += -1 if m.group(1) else 1
        if depth == 0:
            return i + m.end()
    raise ValueError('unbalanced')

moved = 0
while True:
    m = TAG.search(s)
    hit = None
    for m in TAG.finditer(s):
        if 'data-moved' in s[m.start():m.end()]:
            continue
        hit = m
        break
    if not hit:
        break
    q0 = hit.start()
    q1 = close_of(s, q0)
    quote = s[q0:q1]
    # enclosing folder
    fold = None
    for fm in re.finditer(r'<div class="folder"[^>]*>', s[:q0]):
        fold = fm
    if not fold:
        print('no folder for', hit.group(1)); break
    fclose = close_of(s, fold.start())
    # tag it so the loop moves on, then relocate to just before the folder closes
    quote_tagged = quote.replace('<div class="', '<div data-moved class="', 1)
    s = s[:q0] + s[q1:]                      # remove from the column
    fclose -= (q1 - q0)                      # folder close shifts left
    ins = fclose - len('</div>')
    s = s[:ins] + quote_tagged + s[ins:]     # append as the card's last child
    moved += 1

io.open(p, 'w', encoding='utf-8', newline='').write(s)
print('quotes relocated to card level:', moved)
