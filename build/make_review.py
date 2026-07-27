# -*- coding: utf-8 -*-
# AI-review build: swap 700KB base64 fonts for Google Fonts links -> clean readable source
import io
s = io.open("site.html", encoding="utf-8").read()

i0 = s.index("<style>")
i1 = s.index(":root{--bg")
head = s[:i0]
rest = s[i1:]

gf = ('<link rel="preconnect" href="https://fonts.googleapis.com">\n'
      '<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>\n'
      '<link href="https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700;800'
      '&family=Fraunces:ital,wght@0,500;0,600;1,500;1,600'
      '&family=JetBrains+Mono:wght@400;600;700&display=swap" rel="stylesheet">\n'
      '<!-- REVIEW BUILD: production version embeds these three typefaces as base64 @font-face -->\n')

out = head + gf + "<style>\n" + rest
io.open("site_review.html", "w", encoding="utf-8").write(out)
print("review build:", round(len(out)/1024), "KB (was", round(len(s)/1024), "KB)")
