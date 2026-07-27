# -*- coding: utf-8 -*-
import io
f="BUILD_SPEC.md"; s=io.open(f,encoding="utf-8").read()

# 1) replace PAGE 5 block
a=s.index("## PAGE 5 —")
b=s.index("## PAGE 6 —")
new5=(
"## PAGE 5 — XTIX (PART 2): EVIDENCE  (STATUS: REVISED — build at end) — sections: Evidence / Performance / Operations / Technology / Reflection / Lesson\n"
"- Eyebrow: Case Study 01 · Page name: **Evidence** · Subtitle: From Infrastructure to Execution\n"
"- **Performance** (table Metric → Result): Pipeline Managed → €3M+ ARR · Qualified Meetings → ~6 per week · New Opportunities → ~20 per week · Outbound Reply Rate → ~20% · Outbound Conversion → 7–8% · Inbound Conversion → 50%+\n"
"- **Operations** (✓): Built the company's commercial reporting structure · Implemented forecasting methodology · Designed KPI framework · Established pipeline management · Standardized outbound methodology · Supported international commercial expansion\n"
"- **Technology:** \"Designed and implemented an internal AI-powered commercial intelligence platform that:\" → Researched prospects automatically · Imported & enriched leads from commercial databases · Generated personalized outreach based on each prospect's business · Automated commercial sequences · Continuously improved through feedback & knowledge accumulation. **Purpose:** Improve commercial decision-making while increasing execution capacity.\n"
"- **Reflection** (\"If I were rebuilding XTIX today, I would:\"): Differentiate the product earlier against competitors · Accelerate enterprise positioning · Invest in strategic partnerships sooner · Expand the AI platform even earlier · Build the Israeli commercial operation in parallel with the global activity\n"
"- **Lesson** (Biggest Lesson): \"Commercial growth doesn't begin when the first campaign is launched. It begins when the commercial system becomes repeatable.\"\n"
"- NOTE: This REPLACES the earlier p5 draft (dropped: Key Initiatives, What Made the Difference, Lessons-5, the \"Technology scales execution\" quote).\n\n"
)
s=s[:a]+new5+s[b:]

# 2) add global rule about case-study ending structure
anchor="- **My Role box: REMOVED — do not use.**\n"
addition=anchor+"- **Case-study ending structure (global):** every Case Study ends with the same flow — **Evidence → Reflection → Lesson**. Apply to Oasis (p6) and Medcoin (p7) too.\n"
s=s.replace(anchor,addition,1)

# 3) update open item about overlap
s=s.replace(
"- **p4 ↔ p5 overlap:** Page 4 \"What I Built\" (10) overlaps heavily with Page 5 \"Key Initiatives\" (7). Oran hinted \"don't repeat.\" → PROPOSED: trim/remove Key Initiatives on p5. AWAITING his OK.",
"- **p4 ↔ p5 overlap:** RESOLVED by the p5 revision (Key Initiatives removed). p5 \"Operations\" still lists KPI/forecasting/reporting which lightly echo p4 \"What I Built\" — acceptable (different framing: built vs operated). Monitor at final build.")

io.open(f,"w",encoding="utf-8").write(s)
print("spec updated; page5 revised, global rule added")
