# -*- coding: utf-8 -*-
# Round 9 — the closing carries the personal statement, the contact details lead.
import io, re

LOG = []
def op(name, fn, s):
    try:
        out = fn(s)
        if out is None or out == s:
            LOG.append(' SKIP  ' + name); return s
        LOG.append(' OK    ' + name); return out
    except Exception as e:
        LOG.append(' ERR   %s :: %s' % (name, str(e)[:110])); return s

def css_end(add):
    def f(s):
        k = s.rfind('</style>')
        return s[:k] + add + '\n' + s[k:]
    return f

VISION = ('<div class="vq">If you connect to the vision, '
          '<b>you\'ll always know where you\'re going.</b></div>')
STATEMENT = ('<div class="vq">I enjoy building commercial organizations <b>from zero</b>. '
             'I believe <b>systems scale better than heroes</b>. '
             'My goal is to leave every company <b>stronger than I found it</b>.</div>')

def seal_text(s):
    if VISION not in s: return None
    return s.replace(VISION, STATEMENT, 1)

def drop_about(s):
    s2, n = re.subn(r'\s*<div class="fabout"[^>]*>.*?</div>\s*\n', '\n', s, flags=re.S)
    return s2 if n else None

def drop_closeline(s):
    s2, n = re.subn(r'\s*<div class="closeline"[^>]*>.*?</div>\s*\n', '\n', s, flags=re.S)
    return s2 if n else None

CONTACT_SITE = """
/* R9 — the contact details close the file, so they lead */
#final .fcontact{margin-top:44px;gap:16px}
#final .fcontact .cc{padding:22px 24px;gap:10px;border:1px solid var(--grid);background:var(--card2);border-radius:14px}
#final .fcontact .k{font-size:9.5px;letter-spacing:.3em;color:var(--emb)}
#final .fcontact .v{font-size:17px;letter-spacing:.01em;word-break:break-word}
#final .vseal .vq{font-size:clamp(17px,2vw,22px);line-height:1.5}
#final .vseal{margin-bottom:6px}
@media (max-width:680px){
  #final .fcontact .cc{padding:16px 18px}
  #final .fcontact .v{font-size:14px}
  #final .vseal .vq{font-size:15.5px}
}
"""
CONTACT_PDF = """
/* R9 — the contact details close the file, so they lead */
.p13 .fcontact{margin-top:20px;gap:12px}
.p13 .fcontact .cc{padding:13px 16px;gap:7px;border:1px solid var(--grid2)}
.p13 .fcontact .k{font-size:8px;letter-spacing:.28em;color:var(--emb)}
.p13 .fcontact .v{font-size:13px}
.p13 .vseal .vq{font-size:13.6px;line-height:1.48}
.p13 .vseal{margin-top:6px;padding:15px 30px 12px}
.p13 .osmap{padding-bottom:15px}
"""

for path, css in (('site.html', CONTACT_SITE), ('casebook.html', CONTACT_PDF)):
    s = io.open(path, encoding='utf-8').read()
    LOG.append('== ' + path)
    s = op('statement moved into the seal', seal_text, s)
    s = op('standalone about line removed', drop_about, s)
    s = op('sign-off line removed', drop_closeline, s)
    s = op('contact details enlarged', css_end(css), s)
    io.open(path, 'w', encoding='utf-8', newline='').write(s)

head = ('<!doctype html>\n<html lang="en">\n<head>\n<meta charset="utf-8">\n'
        '<meta name="viewport" content="width=device-width,initial-scale=1">\n'
        '<meta name="color-scheme" content="dark">\n</head>\n<body>\n')
site = io.open('site.html', encoding='utf-8').read()
io.open('site_standalone.html', 'w', encoding='utf-8', newline='').write(head + site + '\n</body>\n</html>')
LOG.append('== standalone rebuilt')
print('\n'.join(LOG))
