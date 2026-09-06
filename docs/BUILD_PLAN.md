# Build plan

> **STATUS: BUILT.** Steps A through H are done and on the live site. What follows was written
> before any of it and is left as it was written, because a plan edited to match what happened
> stops being a record of what was decided. Where the build departed from it, the departure is
> in the commit that made it and in the closing summary at the foot of this file.


The restructure, as settled with Oran across nine planning stages. Nothing here was invented
by me: every decision below is one he made, and where I recommended something he overruled,
his ruling is what is written.

The governing rule from `ARCHITECTURE.md` still holds and is what everything below serves:

> **The shell is 1984. The content is 2026.**

And one rule of his own, which is why this document exists before any code does:

> אנחנו רק מתכננים כרגע — nothing is modified, updated, edited or built without his approval.

---

## 1. The five screens

| | screen | reached by |
|---|---|---|
| 1 | the loading page | first load — **unchanged, not in scope** |
| 2 | three scrolling pages | click through the loading page |
| 3 | the folder | clicking the Macintosh screen on page 3 |
| 4 | a document | one click on an icon in the folder |
| 5 | FINAL | the READ ME icon in the folder |

The three scrolling pages are: **p1** today's `statement` — the neural-net canvas and its
sentence — with the harvested HERO copy beneath it; **p2** today's `philosophy`, unchanged;
**p3** the Macintosh, floating.

FINAL is separate and has **no URL**. Oran: *"המטרה שהוא יחפור במסמך על מנת לגלות אותם."*

---

## 2. What already exists

Built and verified in a real browser, desktop and mobile:

| | where | state |
|---|---|---|
| the 1984 kit | `tools/mac_kit.py` → `lab/_kit.js` | 5×7 face, 69 glyphs, seven icons, colours |
| the folder | `lab/desktop.html` | seven icons, menu bar, window, counter |
| the six documents | `lab/document.html` | in the window frame, animations running |
| the machine | `lab/machine.html` | 61,081 tris; `?geo=proc` gives 23,506 |

Not built: **FINAL in the window**, **the three scrolling pages restructured**, **the router**,
**the sound removal**, **the cursors**, and the integration of all of it into `m/index.html`.

---

## 3. Order of work

Each step names what it depends on. Steps A and B are already largely done in `lab/`.

### A · The subtractions

Independent of everything else, and they shrink the surface the rest has to work against.

- The `.otx` intro block — the filing-cabinet drawer *and* the folder-cover lift — out of all
  four case documents.
- Nine lines of archive wording: the `R E S T R I C T E D · EMERALD ARCHIVE` band ×4, the
  `CTRL № … · CASE FILE … · COPY N OF 12` row ×4, and OASIS's `ON RECORD · CASE FILE 02` source
  line. Oran approved these individually, by reading them.
- Both control-number systems in JavaScript — `(S) · CTRL № X-26-0101-A` in the claim map and
  `(C) · CTRL № M-26-0104` in the evidence slip. These were missed by the first audit because
  it measured HTML only; the page composes them at runtime.
- The `(S)` mark beside `$9M+ ARR` and `$2M`. Neither of us could establish what it meant.
- Punch holes and their rail, from every document.
- **The whole sound layer** — 16.2 KB: the synth, the five voices, the `#sndtg` toggle, its CSS,
  ten call sites, the `arch_snd` key. Oran: *"אפשר להוריד — אני לא רוצה להתעסק בזה יותר מדי."*
- The review ceremony and its gate: `ARCHIVE DISPOSITION` / `IN REVIEW · 0/4` /
  `FOUR FILES REVIEWED — THE RECORD CLOSES`, the `CASE CLOSED` stamp, the closing mini-drawer,
  the sound, the vibration, and the `REVIEW COMPLETE · 4/4 FILES` log line. It gated the ending
  on reading four files, which contradicts a decision he had already made.
- Numbering: `.secnum` becomes 01–06, and the two documents that carried no number get one —
  LEADERSHIP `FILE 05 · MANAGEMENT`, TECH `FILE 06 · SYSTEM`.

**What is kept, and must not be swept up with the above:** `CASE STUDY 01`, `FILE 01 · INTAKE`,
`PART 1 OF 2 — THE BUILD`, MEDCOIN's `FOUNDER` stamp, the red rule under *Zero commercial
infrastructure*, and the entire live layer — the analyst note, the UV lamp, the evidence slip,
the sheet flip, the dev zones. Those carry content. The deleted lines carried none.

### B · FINAL — depends on A

The only document not yet in the window. It becomes **`FILE 07`**, `.tok` = `FILE 07 · PRINCIPLES`,
window title `READ ME`.

Oran overruled me here and was right: I had decided FINAL should carry no number. His reason is
arithmetic — a reader who opens all six documents and then READ ME must be able to see
`7 of 7`. If FINAL is not a file, the counter can never complete.

The nine principles, the signed closing statement and the three contact rows are untouched.
The gate is replaced by a line that reports and does not block: `5 of 7 files read`, in **one
implementation** for desktop and phone, not the two that drifted apart last time.

### C · The window frame — depends on A

A Macintosh document window around content that does not change. Oran:
*"רק הכלליות משתנה."*

    ┌──────────────────────────────────────────────┐
    │ ◆  File  Edit  View  Special                 │  menu bar, stays
    ├──────────────────────────────────────────────┤
    │ ░┌────────────────────────────────────────┐░ │  dithered desktop
    │ ░│⊠══════════  XTIX  ══════════════════│░ │  stripes, X at LEFT
    │ ░├──────────────────────────────────┬───┤░ │
    │ ░│   the document, dark, unchanged  │▲█▼│░ │  live scroll bar
    │ ░└────────────────────────────────────────┘░ │
    └──────────────────────────────────────────────┘

A white 1-bit 1984 frame around a dark 2026 document. The boundary is meant to be visible.

- Title: the file's name alone — `XTIX`, not `CASE FILE 01 — XTIX`.
- Close box: a square **with an X through it**, at the left. Oran overrode the historical empty
  square deliberately, so that it reads as an exit control to someone who never used System 1.
- Scroll bar: live on desktop; **absent on mobile**, where 15 px of 1-bit chrome is neither
  usable nor authentic to anything.
- `DONE` at the end of the content, a System 1 push button. It and the X do the same thing.
- Opening: the **zoom rectangle** — expanding outline rectangles from the icon to the window
  bounds, four to six frames, ~180 ms. This is what the real machine did, and it is what Oran
  asked for: an effect of a document opening, and then the document.
- The counter increments **on open**, not on DONE.

### D · The shell, wired — depends on B and C

Machine → folder → document → FINAL, as one path. All three parts exist; this is assembly.

Folder status line: `7 files · 3 of 7 opened · 2018–2026`. Seven, not six — a Finder counted
what the window held, and READ ME is openable like the rest.

### E · The router — depends on D

**The largest genuinely new piece.** A state machine across the five screens, with browser Back
following the stages. Build check 4 is now one-way: every URL resolves to a state, but a state
need not have a URL, because FINAL has none.

### F · The scrolling pages — depends on E

p1 = `statement` + the harvested HERO copy. p2 = `philosophy`, unchanged. p3 = the machine.

Scroll locks at the machine inside a bounded control region. The machine resets its angle when
returned to. The choreography on entry is fixed and ordered: **the machine straightens first,
then the folder opens, and only then the zoom-in begins.**

### G · The cursors — depends on F

| where | cursor |
|---|---|
| loading page, the three scrolling pages | the circle and dot, **improved** |
| inside the machine — folder, documents, FINAL | **a Macintosh arrow** |
| touch, and `prefers-reduced-motion` | the system cursor, untouched |

The circle-and-dot is *"כבד קצת בזרימה"*, and measurement says exactly why. The dot itself is
eased at `0.40`, so it trails the physical pointer by roughly two frames — and a trailing *dot*
reads as lag, where a trailing *ring* reads as an effect. Separately, the hover test runs
`e.target.closest()` against five selectors on **every** pointer event.

Four changes: the dot becomes exact (`cx = mx`); the ring keeps its 0.16 trail; the hover test
moves into the frame loop; `will-change: transform` keeps both on the compositor.

### H · Integration and the checks

Into `m/index.html`, then every check in §12 of `ARCHITECTURE.md`.

`index.html` at the repo root is never written — check 8 already enforces this.

---

## 4. How to verify, and how not to

Written from three false failure reports I filed during Stage 6, all from the same cause.

**Let the page settle before measuring anything.** Element boxes and opacities keep moving for a
second or more after a document opens. A check that runs immediately reports the start state and
calls it a failure. Put a settle wait and a double `requestAnimationFrame` in front of every
measurement.

**Drive scrolling with a real gesture.** Assigning `element.scrollTop` moves the element but
dispatches no scroll event in an automation context, so a scroll-driven engine never runs and
every value sampled is the initial one. That produced a confident, entirely wrong report that
the animation engine was broken.

**Compare against `clientWidth`, not `innerWidth`,** when testing for horizontal overflow.
`innerWidth` includes the scrollbar and invents an overflow that is not there.

**Emulate mobile by loading the page in a 375 px iframe.** Device emulation in some harnesses
applies the user agent and touch points but not the viewport size, so media queries silently
evaluate as desktop and the test proves nothing.

**A keep-list must be checked where the thing actually lives.** The first cut carried a guard
asserting that `lampband`, `evslip` and `an-note` survived it — and the guard passed while the
cut silently killed the UV lamp and all twelve developed zones. It passed *vacuously*: those
names never appear in `src/doc/*.html`, because the page composes them at runtime from the
monolith's JavaScript. A guard that looks for a string in a file that never contained it always
succeeds and proves nothing.

**And decoration can be load-bearing.** The lamp module required `.clsband` — the RESTRICTED
strip — as a proxy for "is this one of the four case folders". Removing an element that appears
to be pure ornament took a feature down with it, and took it down *silently*, because a missing
anchor returns rather than throwing: no console error, no failed build, just an absence. Before
cutting anything, grep the JavaScript for its class name. The nine props were checked this way
after the fact; every future cut is checked before.

**Compare against the committed page, not against expectation.** What settled this was building
`git show HEAD:m/index.html`, serving both, and counting the same selectors in each: 12 zones
and 4 lamps before, 0 and 0 after. Expectation would have said nothing was wrong.

The three numbers that establish the scene engine is alive, all under real scrolling:

    .cnt    passes through intermediate values, rather than sitting on its final text
    .bar0   leaves matrix(1,0,0,0,0,0) — that matrix is scaleY(0), an invisible bar
    .garc   strokeDashoffset reaches 0

---

## 5. Decisions recorded, so they are not relitigated

- **Sound is removed, not muted.** Including on mobile, where it never played anyway.
- **The document's content, layout and typography do not change.** Five web faces stay,
  inlined, in one file. Serving them as separate files would save a measured 75 KB and was
  refused: the loading screen already absorbs that weight, and one file cannot half-arrive.
- **The live layer stays in full** — it delivers real content through a device, which is not
  the same thing as the empty props that were removed.
- **Selection dims inside the icon mask and inverts only the label.** Inverting emerald produces
  magenta; that is arithmetic, not taste. `KIT_OPTIONS.md` D15 says "inverts both", which was
  the 1-bit rule and stopped applying when Oran chose colour icons.
- **Nothing licensed ships.** No Chicago, no Geneva, no Apple mark, no system icons. The menu
  bar carries a lozenge. D15 argues for drawing everything from scratch to remove every licence
  question and then specifies Geneva 9 for labels; the hand-drawn face settles it in practice,
  and the doc should be corrected so nobody reaches for Geneva later.
- **The isometric world map is parked**, by his decision, with its own handover in
  `HANDOVER_BLENDER.md`. Nothing here depends on it.

---

## 6. What was built, and where it departed from the plan

Written after the fact. Every departure below was a decision taken while Oran was away, under
his instruction to decide rather than wait, and each is here so he can overturn any of them.

### Decisions taken without him

**The procedural machine ships, not the mesh.** `lab/machine.html` is 1,050 KB and 933 of them
are one baked geometry blob. The same file builds the machine from code — 25 parts, 23,506
triangles — and that is what ships, at 117 KB. The mesh misses this document's own desktop
budget by about 2× and the phone one by fifteen. It also settles the one question the plan left
open, whether the machine should be real-time or a pre-rendered turntable: real-time was the
recommendation, and procedural real-time is that answer at a tenth of the weight.

**The folder is screen.js's, not the frame's.** The frame arrived from the lab drawing seven
icons loose on a dithered desk. The folder Oran approved is a window with a striped title bar,
a close box at the left and a three-column status line, and `screen.js` already drew exactly
that — in one layout function that also bakes the CRT texture, so the pixels the camera flies
into cannot drift from the ones it lands on. Two renderers now: the folder is screen.js's, the
document window is the frame's.

**The rail lost eight of its eleven entries.** COVER pointed at a section that no longer exists,
and the seven documents are not scroll destinations any more — their hashes belong to the
router, so a rail link would have opened a document directly. That is the one thing Oran ruled
out explicitly: every file is reached through the folder, only through there.

**Page 3's subtitle was rewritten.** It read `EXECUTIVE PORTFOLIO · 04 DOSSIERS · 2018–2026` —
a phrase Oran had removed from the hero, and a count of four when there are seven. It reads
`SEVEN FILES · ONE MACHINE · 2018–2026`.

**The middle beat of the entry is a held pause.** Oran's order is: the machine straightens, then
the folder opens, then the zoom begins. The first and third are camera moves and are built. The
second would mean re-uploading the CRT texture mid-flight, which is a piece of work of its own;
the beat is honoured so the sequence reads correctly, and what fills it is smaller than it will
be. This is the one place the build is thinner than the plan.

**A Macintosh arrow was drawn.** The plan said the pointer inside the machine is the machine's
own but never said where it came from. Apple's is Apple's, like Chicago and the Apple mark, so
it is drawn on a 16×16 grid in `tools/make_cursor.py`, with an I-beam over running text.

### Left alone, deliberately

The marquee, `ARCHIVE N°` and `STATUS: ACTIVE` came with the harvested hero card. They are its
furniture rather than its copy, and whether they belong at the bottom of page 1 is a judgement
Oran has not made.

`EMERALD ARCHIVE · REEL 04` on the film-strip edge, and the orphaned review-counter JavaScript
with its hard-coded 4. Neither was on any approved list.

### Faults found and fixed while building

Each of these was found by measuring, and none of them announced itself:

- Cutting `.clsband` took the UV lamp and twelve developed zones down **silently**, because the
  lamp module used that strip as its entry condition. Found by counting the same selectors in
  the published page and the new one. `tools/depends.py` exists so it cannot recur.
- Removing `#sndtg` from four grouped selectors left them ending in a comma, which made every
  one of those rules invalid — so the archive HUD stopped hiding under `prefers-reduced-motion`.
  Build check 10 refuses it now.
- The shell shipped at `z-index:auto` and drew underneath the hero card.
- The live layer built twice: 24 developed zones for 12, 8 lamps for 4.
- The machine's lab stylesheet would have taken the site's `body` and covered the viewport.
- Its no-WebGL message wrote to an element that is not shipped, so the one machine that cannot
  render would have thrown on its way to saying so.
- The entry flight is driven by `requestAnimationFrame`, which does not fire in a hidden tab —
  so the reader clicked the machine and nothing happened. The arrival is on a deadline now.
  **An animation must never be the only way into a state.**
