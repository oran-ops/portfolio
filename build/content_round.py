# -*- coding: utf-8 -*-
# Approved copy round: condensed case prose in BOTH files.
import io

PAIRS = [
 # A. XTIX situation
 ("When I joined XTIX, the company had a <b>strong vision and product</b> &mdash; but no commercial infrastructure to support scalable growth.",
  "Strong vision. Strong product. <b>Zero commercial infrastructure.</b>"),
 # B. XTIX mission
 ("Design and build a <b>commercial operating system</b> capable of supporting predictable business growth &mdash; starting with the Israeli market and later expanding globally.",
  "Build a <b>commercial operating system</b> for predictable growth &mdash; Israel first, then global."),
 # C. XTIX approach
 ("Rather than launching outbound immediately, I focused on <b>understanding the business first</b>. The first phase included:",
  "<b>Understanding before outbound:</b>"),
 # D. XTIX technology (his phrasing)
 ("Designed &amp; implemented an internal <b>AI-powered commercial intelligence platform</b>:",
  "Built an in-house <b>AI commercial intelligence platform</b>."),
 ("Designed & implemented an internal <b>AI-powered commercial intelligence platform</b>:",
  "Built an in-house <b>AI commercial intelligence platform</b>."),
 # E. Oasis situation
 ("As CEO, my responsibility extended far beyond sales. The objective wasn't simply to increase revenue &mdash; it was to build a <b>profitable, scalable commercial organization</b> capable of supporting the company's long-term vision.",
  "The mandate as CEO wasn't more revenue &mdash; it was a <b>profitable, scalable commercial organization</b>."),
 # F. Oasis log merges
 ("Built the pricing model from scratch",
  "Built the profitability-based pricing model from scratch"),
 ("Implemented KPI framework",
  "Implemented company-wide KPI framework"),
 ("Built forecasting methodology",
  "Built forecasting &amp; commercial reporting"),
 # F4. Oasis duplicate 5-dash list
 ('<div class="dash">Built pricing strategy from zero</div><div class="dash">Introduced profitability-based pricing</div><div class="dash">Defined company-wide commercial KPIs</div><div class="dash">Improved cross-department collaboration</div><div class="dash">Created structured commercial reporting</div>',
  ""),
 # G. Oasis reflection (his middle version)
 ("The biggest lesson I learned as CEO wasn't about selling &mdash; it was about <b>leadership</b>. The more I tried to manage every function myself, the less scalable the organization became. Real leadership begins when leaders build systems that let others succeed <b>without depending on them</b>.",
  "The biggest lesson wasn't selling &mdash; it was <b>leadership</b>. The more I managed everything myself, the less the organization scaled."),
 # H. Eventer situation
 ("Eventer already had an <b>existing commercial operation</b>. Unlike previous roles, the objective wasn't to build a department from scratch &mdash; it was to improve execution, strengthen collaboration between departments and identify new commercial growth opportunities.",
  "Here, a commercial operation <b>already existed</b>. The job: sharpen execution, connect departments, find new growth."),
 # I. Eventer role
 ("I worked across multiple business functions to improve commercial performance by <b>connecting business strategy with day-to-day execution</b>.",
  "<b>Connecting business strategy with day-to-day execution</b> &mdash; across every function."),
 # J. Eventer impact
 ("Rather than focusing only on Business Development, I worked closely with multiple departments to ensure customer insights translated into business decisions. Commercial growth became a <b>shared organizational responsibility</b> &mdash; not just a sales target.",
  "Customer insights became business decisions. Growth became a <b>shared responsibility</b> &mdash; not a sales target."),
 # K. Eventer learned
 ("Leadership doesn't always require authority. Some of the biggest organizational changes happen through <b>influence, collaboration and better decision-making</b>.",
  "Leadership doesn't require authority &mdash; <b>influence, collaboration and better decisions</b> move organizations."),
 # L. Medcoin vision
 ("Create a <b>compliant, scalable cryptocurrency ATM business</b> serving the European market through secure, accessible digital financial services.",
  "A <b>compliant, scalable crypto-ATM network</b> &mdash; accessible digital finance for Europe."),
 # M. Medcoin challenge
 ("Building a company from zero meant making <b>every strategic decision</b> &mdash; from business model and partnerships to compliance, operations and commercialization.",
  "From zero, <b>every decision was mine</b> &mdash; model, partnerships, compliance, operations, commercialization."),
 # N. Medcoin learned (his closer pick)
 ("Being a founder changes how you think. Every commercial decision affects operations. Every operational decision affects profitability. Every strategic decision affects survival. Leading a company taught me that <b>commercial leadership is ultimately business leadership</b>.",
  "Every commercial decision affects operations. Every operational decision affects profitability. Every strategic decision affects survival. <b>That's the reality of building a company.</b>"),
]

def apply(path):
    s = io.open(path, encoding="utf-8").read()
    hits = 0
    misses = []
    for old, new in PAIRS:
        if old in s:
            s = s.replace(old, new, 1)
            hits += 1
        else:
            alt = old.replace("&mdash;", "—")
            if alt in s:
                s = s.replace(alt, new.replace("&mdash;", "—"), 1)
                hits += 1
            else:
                misses.append(old[:60])
    io.open(path, "w", encoding="utf-8").write(s)
    print(path, "applied:", hits, "of", len(PAIRS))
    for mm in misses:
        print("   MISS:", mm)
    return s

apply("casebook.html")
t = apply("site.html")
head = ('<!doctype html>\n<html lang="en">\n<head>\n<meta charset="utf-8">\n'
        '<meta name="viewport" content="width=device-width,initial-scale=1">\n'
        '<meta name="color-scheme" content="dark">\n</head>\n<body>\n')
io.open("site_standalone.html", "w", encoding="utf-8").write(head + t + "\n</body>\n</html>")
print("standalone rebuilt")
