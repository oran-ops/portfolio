# Decisions log

Every settled decision, with the reason. `ARCHITECTURE.md` says what the thing *is*; this says
what was *chosen* and why, so that a choice is never quietly re-litigated six weeks later — and
so that when one is reopened, it is reopened against its original reasoning rather than against
a memory of it.

Newest last.

---

## 2026-08-22 — Structure

| # | decision | reason |
|---|---|---|
| 1 | **The shell is 1984, the content is 2026** | Page 2's sentence made structural rather than decorative. It is also what allows the seven documents to stay untouched. |
| 2 | **No skip.** No "jump to the work" affordance anywhere | The prologue is the product. A deep link still lands directly, because that is someone else's decision about where a reader starts, not the reader's own shortcut. |
| 3 | **Sound is in**, designed alongside everything else | Anything added at the end is the first thing cut. |
| 4 | **Sound is synthesised, never sampled** | These machines made square waves. Web Audio produces them for zero bytes, stays tunable, and cannot become a licensing question. Samples would cost 50–200 KB for a worse result. |
| 5 | **We write our own startup chime** | Apple's is Apple's. Not a grey area, and cheap to respect. |
| 6 | **The machine makes the first sound in the product** | Not a choice so much as a discovery: browsers refuse audio before a user gesture, the prologue is scroll-only, and the first click in the whole product is the one on the machine. The silence before it is now deliberate. |
| 7 | **Seven equal icons in seven different shapes** | Old desktops said "these are different kinds of thing" with shape alone. Four case files, a ruled notepad, a system suitcase, a sealed letter. |
| 8 | **`files` (page 4) is replaced by the desktop** | It already *is* the desktop, built as a rotating drawer. Three things survive it: the four descriptors, the `04 DOSSIERS · 2018–2026` framing, and the `DRAG TO TURN · CLICK A FILE` affordance pattern. |
| 9 | **Hash routing, not path routing** | GitHub Pages serves static files; path routing needs a 404 rewrite that breaks the moment the repo is renamed. |
| 10 | **One isometric contract for all three scenes** | 2:1, 64 × 32, integer scales, painter's sort. Defined once they share a renderer and a look; defined three times they become three worlds and three places to change. Verified by executing the projection, not by reading it. |
| 11 | **Base build: `m/index.html`** | Newer by 11 days, more developed design, and — as the reconciliation showed — consistently the better copy. |
| 12 | **Published at `/portfolio/m/`** | Chosen; the link is not published anywhere binding, so nothing has to change hands. |
| 13 | **The root is harvested, then reduced to a redirect** | `/portfolio/` is the guessable address and serves a build two generations stale. Leaving it recreates the drift. **Order is fixed:** harvest every unique block first, replace second. |
| 14 | **Cut and reconcile are never the same change** | A cut that also edits copy produces a diff full of intended changes, and an unintended one hides among them perfectly. One diff, one kind of change. |

## 2026-08-22 — Copy

| # | decision | reason |
|---|---|---|
| 15 | **`oasis`: take `m/` wholesale, restore one line** | Of four flagged root-only claims, three are already covered by stronger wording in `m/` — `Standardized commercial processes` → `Designed the commercial process`, `Built onboarding documentation` → `Created sales playbooks & onboarding`, `Established KPI-driven management` → `Implemented company-wide KPI framework`. |
| 16 | **Restore `Conducted weekly coaching sessions`** | The one genuine gap. `m/` has `Established weekly business reviews`, which is a meeting about numbers; coaching is developing people. OASIS is the file whose theme is **leadership**, so of the four this is the line most on its own subject. |
| 17 | **`xtix`: no change** | All four flagged root-only lines are already in `m/`, in a checkmark list an earlier probe had missed: `Reporting Dashboards` covers `Built the company's commercial reporting structure`, `Forecasting Structure` covers `Implemented forecasting methodology`, `Outbound Sequences` covers `Standardized outbound methodology`, and `Prioritized global expansion` covers `Supported international commercial expansion`. |
| 18 | **`medcoin`: no change** | `FOUNDER CASE STUDY` became `CASE STUDY 04 · FOUNDER`; the root's two-clause line became three in `m/`, gaining `Every strategic decision affects survival.` |
| 19 | **`eventer`, `leadership`, `tech`, `final`: no change** | Nothing flagged. `leadership` is byte-identical between the two builds. |

## 2026-08-22 — Kit

| # | decision | reason |
|---|---|---|
| 20 | **Painter's order is `x + y`, then `z`, then draw order** | Corrects the contract, which said `x + y + z`. Height lifts a sprite on screen; it does not move it toward the viewer. Under the old key a tower at the back drew over a person in front of it. Found by a test whose expectation was written from the scene rather than from the code. |
| 21 | **Ramps are computed in OKLab, and the token is a stop in its own ramp** | HSL lightness is not perceptual, so its ramps come out uneven. And a ramp whose middle stop has drifted off the token is not derived from the palette, it *is* a new palette — the first version silently turned `#2FB380` into `#22AB79`. |
| 23 | **The 120 KB / 240 KB asset budgets are withdrawn** | They had no source — I wrote them because they sounded like reasonable ceilings. Measured, the two shell faces subset to 5 KB inlined and the sprite sheet to 29 KB: 49× and 4× headroom. A ceiling nobody established was about to decide the typeface, between options four kilobytes apart on a seven-hundred-kilobyte page. |
| 22 | **A token at the end of the range gets an asymmetric ramp** | `#F2F1ED` is paper white and has no highlight above it; a symmetric ramp spent two of its five stops on the same colour. It now sits at position 5 of 5, all its stops below it. |

---

**Final tally: across all seven documents, one line was restored.** The raw block diff said 52,
the filtered tool said 10, and reading them said 1. A string tool narrows the field; it cannot
tell a reworded claim from a dropped one, and the reading is still the work.

---

## Still open — the phase C kit

Fonts · the isometric sub-palette · which events sound · motion durations and what
`prefers-reduced-motion` disables · cursor · art scale · reading state. Each needs a visual
before it is settled. See `ARCHITECTURE.md` §14.2.
