# -*- coding: utf-8 -*-
import io
f="BUILD_SPEC.md"; s=io.open(f,encoding="utf-8").read()

# 1) case-study titles + order, added after the ending-structure global rule
anchor="- **Case-study ending structure (global):** every Case Study ends with the same flow — **Evidence → Reflection → Lesson**. Apply to Oasis (p6) and Medcoin (p7) too.\n"
titles=('- **Case study titles (fixed):** XTIX = "Building a Commercial Function From Zero" · OASIS = "Building Leaders, Not Just Sales Teams" · '
        'EVENTER = "Creating Commercial Alignment Across Departments" · MEDCOIN = "Building a Business From Vision".\n'
        '- **Case studies = XTIX → Oasis → Eventer → Medcoin. Each spans 2 pages (Part 1 + Evidence).**\n')
s=s.replace(anchor, anchor+titles, 1)

# 2) total pages line
s=s.replace("- Total pages: **11**. Footer total reads `— 11`.",
            "- Total pages: **TBD** (grew to ~15 — 4 case studies × 2 pages + front/back matter). Assign §NN / P.NN / footer total at FINAL build.")

# 3) PAGE ORDER block
old_order=("## PAGE ORDER (11)\n"
"1. Cover · 2. Statement · 3. My Commercial Philosophy · 4. XTIX (part 1) · 5. XTIX (part 2) · 6. Oasis · 7. Medcoin · 8. AI Growth Engine · 9. Leadership Principles · 10. Results · 11. Let's Build Together.\n")
new_order=("## PAGE ORDER (grew — final numbers assigned at build)\n"
"Provisional: 1 Cover · 2 Statement · 3 Philosophy · 4-5 XTIX · 6-7 Oasis · 8-9 Eventer (pending) · 10-11 Medcoin (pending) · 12 AI Growth Engine · 13 Leadership Principles · 14 Results · 15 Let's Build Together.\n")
s=s.replace(old_order,new_order)

# 4) replace pages 6-11 block
a=s.index("## PAGE 6 — OASIS  (STATUS: AWAITING CONTENT)")
b=s.index("---\n\n## OPEN ITEMS")
block=(
"## PAGE 6 — OASIS (PART 1): Building Leaders, Not Just Sales Teams  (STATUS: content received) — Case Study 02\n"
"- Meta: Oasis | CEO | Construction & Smart Building Solutions\n"
"- **The Situation:** \"As CEO, my responsibility extended far beyond sales. The objective wasn't simply to increase revenue. It was to build a profitable, scalable commercial organization capable of supporting the company's long-term vision.\"\n"
"- **My Responsibilities** (\"I led the company's commercial operation end-to-end, including:\"): Recruiting & building the sales team · Defining commercial strategy · Pricing model development · KPI design · Sales methodology · Forecasting · Commercial reviews · Cross-functional leadership · Profitability management\n"
"- **Commercial System Built** (✓): Recruited & onboarded the entire sales team · Built the pricing model from scratch · Designed the commercial process · Implemented KPI framework · Created sales playbooks & onboarding · Established weekly business reviews · Built forecasting methodology · Created cross-functional commercial collaboration\n"
"- **Leadership Model** (\"building independent, accountable professionals — that meant:\"): Weekly coaching sessions · Monthly 1:1 performance reviews · Quarterly business reviews · Live deal reviews · Commercial coaching · Cross-functional collaboration · Clear ownership & accountability\n"
"- **Signature Insight:** \"High-performing sales teams aren't built by pressure. They're built by clarity.\"  [!] p4 had its Signature Insight REMOVED — reconcile whether part-1 pages keep signatures.\n\n"
"## PAGE 7 — OASIS (PART 2): Evidence  (STATUS: content received) — Case Study 02 — Evidence → Reflection → Lesson\n"
"- Page name: Evidence · Section: Commercial Results\n"
"- **Commercial Leadership:** Recruited an entire sales team · Led a team of 5–6 sales professionals · Conducted weekly coaching sessions · Established KPI-driven management · Built onboarding documentation · Standardized commercial processes\n"
"- **Business Performance:** Largest deal closed: ₪2M · Built pricing strategy from zero · Introduced profitability-based pricing · Defined company-wide commercial KPIs · Improved cross-department collaboration · Created structured commercial reporting\n"
"- **Cross-Functional Leadership** (\"Worked closely with:\" ✓): Operations · Production · Customer Success · Finance · Marketing · Technical Teams\n"
"- **Reflection (Looking Back):** \"The biggest lesson I learned as CEO wasn't about selling. It was about leadership. The more I tried to manage every function myself, the less scalable the organization became. Real leadership begins when leaders build systems that allow others to succeed without depending on them.\"\n"
"- **Lesson (Biggest Lesson):** \"Organizations don't scale because leaders work harder. They scale because leaders create clarity, ownership and trust.\"\n\n"
"## EVENTER (Part 1 + Evidence)  (STATUS: AWAITING CONTENT) — Case Study 03 — Title: \"Creating Commercial Alignment Across Departments\"\n\n"
"## MEDCOIN (Part 1 + Evidence)  (STATUS: AWAITING CONTENT) — Case Study 04 — Title: \"Building a Business From Vision\"\n\n"
"## AI GROWTH ENGINE  (STATUS: placeholder in file; awaiting final content)\n"
"## LEADERSHIP PRINCIPLES  (STATUS: placeholder; awaiting final content)\n"
"## RESULTS  (STATUS: placeholder; awaiting final content)\n"
"## LET'S BUILD TOGETHER  (STATUS: placeholder; awaiting final content)\n\n"
)
s=s[:a]+block+s[b:]

# 5) open items additions
oi="## OPEN ITEMS / DECISIONS PENDING\n"
adds=(oi+
"- **NUMBERING/TOTAL:** doc grew (Eventer added; each case study = 2 pages). Final §NN, P.NN and footer total assigned at build.\n"
"- **Signature Insight consistency:** p4 (XTIX pt1) has NONE; p6 (Oasis pt1) HAS one. Decide at build whether all part-1 pages carry a Signature Insight.\n"
"- **Eventer content** still needed (Case Study 03).\n")
s=s.replace(oi, adds, 1)

io.open(f,"w",encoding="utf-8").write(s)
print("spec updated for pages 6-7 + Eventer + titles")
