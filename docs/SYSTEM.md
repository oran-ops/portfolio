# PAPER UNDER GLASS
### The redesign of all seven documents. One system, built to be executed without asking a question.

---

## 0. WHAT THIS IS, AND WHAT IT IS MADE OF

Five directions were designed and three judges scored them. This is not their average. It is
**direction A's window grammar as the spine**, with **C's margin apparatus grafted on to fix A's
one real weakness**, **E's colour engine underneath it**, **D's card taxonomy deciding which form
a block takes**, and **B's texture layer as the only thing colour does that colour could not do
before**. Everything else was dropped, and §0.2 says what and why.

### 0.1 THE ONE IDEA

A Macintosh document window has a **state** — active or inactive — and that is the one thing a
window can be that a card can never be. A printed manual has a **margin** — a gutter where the
numerals, the figure numbers and the leader ticks live, outside the text, costing the reading
measure nothing. The merge is that **both are true at once**:

> **Every block in every document is either a LEAF or a WINDOW.**
> A **leaf** is printed: it has no frame and no bar, and its apparatus — its numeral, its leader
> tick — hangs in the margin to the left of it. A **window** is glass: it has a keyline, a title
> bar, plaques, and a state. **The document is printed. The archive that holds it is a machine.
> The reader sees both at once, on one dark bench, and that is the design.**

This is what the name means. It is also what solves the problem each single direction had:

| Direction's problem | What the merge does |
|---|---|
| A: eleven title bars per document is a barcode | Most blocks are **leaves** and wear no bar at all. Two or three per document are windows. |
| C: a printed manual inside a 1984 screen is a category slip, and at overview scale it reads as dark editorial | The leaves live **inside** a document window, on a desk, and the blocks that carry weight are **windows** with the machine's own chrome. |
| D: the closed/open card idea had no chrome vocabulary to express itself in | **Closed card = window. Open card = leaf.** The documents already number at two levels (01 02 03 / A B C) and the design finally shows it, for free and without a new word. |
| E: colour applied as eleven identical loud bars | The **CLUT** supplies base/light/shade; the state system decides where the base is allowed to appear. |
| B: a pattern palette that was 90% decoration | Six patterns, each with one job, published as a legend only under the chart that uses them. |

### 0.2 WHAT WAS TAKEN, AND WHAT WAS DROPPED

**FROM A — THE SPINE.** The window grammar; ACTIVE/INACTIVE as the hierarchy device; the
INACTIVE DISCOUNT (colour is lowered, never removed); `--u:2px` as the one logical pixel, which is
frame.css's own number; `--kl #0B0C0F`, the keyline re-pointed one step under the desk so Kare's
grammar survives a dark room; the 32×32 icon pipeline (one 32-row map, re-palettised per folder);
**the figure is a dialog** with System 1's doubled keyline; the one overlap per document; the file
standing on the desk above its own window; the desk dither between blocks; the slip as a window
printed on paper; the lamp plate as a push button whose ring *arrives*; the whole-scale law and
the mono-twin contract.
*Dropped from A:* making every block a window (that was its failure mode); replacing
`redactionBars()` with `box-decoration-break:clone` — a transform on a clone-background span moves
the text with the cover, so the claim does not hold and the repo's measured per-line mechanism is
kept; a live scroll thumb on every block; `.secnum` at scale 24 inside the machine, where
`frame.css:233` hides it outright.

**FROM C — THE APPARATUS.** The margin column (`--marg:104px`), the hanging numeral and its leader
tick; two list idioms that must not look alike plus their struck counterpart; the numbered figure
plate **whose caption is the zone's own heading re-set**; the dot leader; the rubber die; the one
button idiom; **figures scroll, they never shrink**; MEDCOIN as the file with no second press run;
the hand/machine geometry exemption; Fraunces rationed to the title and the quotes.
*Dropped from C:* the manual as the governing metaphor (these documents live inside a screen);
the smooth stroked gauge arcs, which are the one place C breaks its own logic; the seven-jobs list
as the *only* colour rule (it survives as the cap, §6.2); the **defined-term underline** — see the
ruling in §3.4, where E's selection wash won and only one of the two may ship.

**FROM E — THE COLOUR ENGINE.** The **CLUT**: colour is not kept, it is *sourced* from
`window.KIT.colour`, which really does hold base/light/shade per file, so the emerald in an XTIX
chart is provably the emerald the Finder draws the XTIX icon with; the archive contents plate,
used once; the **fatbits lattice** over the big figure; the **selection wash** as the only inline
emphasis; the orthogonal law for every diagram; the three-cell title bar on a phone; the method
slip as a template view; the thumbless scroll strip (once, on the absence panel); a throwing
emitter in the build.
*Dropped from E:* **every word of invented apparatus** — PICT, ID 128, STR#, vers, hidn 3, TMPL,
"31 BYTES · MACROMAN", CASE/DOCT/SYST/PRIN. None of them exists anywhere in the repo, and a
forensic idiom that fabricates one datum has destroyed its own case. The forms are kept; the
vocabulary is not. Also dropped: the MacRoman hex dump, which chops the claim into eight-byte
fragments inside the one object whose whole job is to persuade; the product name in a title
plaque; the 3px chamfer (`pushbutton()` cuts a **one**-pixel corner step and that is what we use).

**FROM D — THE TAXONOMY AND THE VOCABULARY.** Closed card / open card, mapped onto window / leaf;
the **density ramp** on `.bar0`; the **shadow ladder** as a countable vocabulary; the press
feedback (invert, shadow to zero, translate into it); the origin line; the coloured `DONE` ring —
`pushbutton(...,ring)` at `frame.js:194` already takes one and is handed `WHITE`; the
custom-property derivation trap, which is a real bug the merge would otherwise inherit; the
nine-character rule for pixel node labels.
*Dropped from D:* **"CARD n OF N"** — invented copy on every block header; pixel lettering on
`.bignum` and inside dial rings, which in D's own render is the least legible object on the page;
the 9px "pressable" radius inside a zero-radius system; the 22 thin outline icons, which collapse
into indistinguishable rings at their working size; the tear-off palette lamp.

**FROM B — THE TEXTURE LAYER, AND ONLY THAT.** Density as a **second data channel** with the
published legend that makes it readable; *an estimate wears grain*; the **violet spray stipple**
as the lamp's light, which is what lets a lamp glow without a single blur entering the archive;
the marching-ants marquee on the developed zone (once on arrival, then static — §11.3); the
chart's own 1-bit horizontal strip on a phone; the two-tier **furniture vs content** rule with its
MEDCOIN exception.
*Dropped from B:* the twenty-cell tool rail and the permanent pattern tray — 76px of every window
and a full row of every phone, saying nothing about the file, and the clearest costume in the
five; the bright white chrome; **FatBits on `$9M+`**; the outline chip; cutting Fraunces from
`.sttl`; and six of the twelve patterns, because a pattern without a job is decoration.

### 0.3 THE CONSTRAINTS, RESTATED AS RULES THIS SYSTEM OBEYS

1. **Not one word changes.** Every string in `src/doc/*.html` stays exactly as it is, in the same
   order. New *apparatus* may add a numeral (`FIG. 01`) or **re-set a string the document already
   carries**; it may never add a word. This is the operational form of the rule and it is C's
   best contribution: a figure's caption is its own zone heading, re-set.
2. **The flow stays.** Same points, same sequence, every document. A block may be re-dressed,
   split, or given furniture; the reader's path through it does not move.
3. **The ground stays matte charcoal.** `--bg #191A1F`, `--card #202127`, `--card2 #25262D`,
   untouched. This is a dark room with a Macintosh in it.
4. **Every folder keeps its colour** — and gains two more tones of it, from the machine's own table.
5. **The UV lamp stays**: the plate, the violet covers over sealed lines, the developed zones, the
   signature. Re-dressed, never removed, and the existing `redactionBars()` mechanism is kept.
6. **No network, no new fonts.** Four embedded faces plus one that is **drawn** from `kit.js`.
7. **It survives a phone.** Nothing depends on hover. 44px tap targets. Verified at 390.
8. **It is a CEO's case file.** The Macintosh here is an archive machine, not a nostalgia sticker.

---

## 1. THE REFUSALS

These are absolute and they apply to all seven documents at once. There is no halfway version of
any of them that does not look like an accident.

- **No radius.** Every `border-radius` goes to 0, including `.folder`'s `0 18px 18px 18px`,
  `.tabrow .tA`'s `9px 20px 0 0`, `.chip`, `.ndot`'s `rx="7"`, `.bar0`'s `rx="1.5"`, `.vseal`'s
  16px. The only non-square corner in the system is the **one-pixel step** `pushbutton()` cuts,
  which is *drawn*, not rounded.
- **No blur.** Every shadow is a hard offset in pure black. The current build's
  `0 24px 60px rgba(0,0,0,.7)` is the most 2024 thing in these files and it is the first to die.
  The only surviving blur in the archive is `.gen3`'s `blur(.45px)`, which is a *photographic*
  effect on a bitmap and reads as generation loss.
- **No gradient.** Half a tone is a **dither**. Six patterns exist (§6.3) and there is no seventh.
- **No bezier in a drawing, no round line cap, no arbitrary angle.** Every connector is
  horizontal, vertical or exactly 45°. Every arrowhead is a stepped pixel triangle.
- **No easing on machine furniture.** `steps()` only. The reader's own scroll keeps its curve.
- **No fractional scaling of anything drawn in pixels.** Whole scales only.
- **No body copy in the bitmap face, and none of Oran's figures in it either.**
- **No hover-only information.**
- **No truncation.** A real Mac shortened a title that would not fit. This archive may not shorten
  one word of Oran's: the scale steps down, then the mono twin takes over, then the bar **grows**.
- **No second menu bar inside a document, and no third use of the stripe motif.** Stripes belong
  to the document window's bar, to an active zone window's bar, and to the armed lamp. Nowhere
  else. The moment a fourth object wears them the first three stop meaning anything.
- **No invented machine vocabulary printed on the page.** See §0.2.
- **No Apple marks or product names.** The forms are quoted; `screen.js` already draws *our*
  lozenge instead of the 1977 mark and says so in a comment. Keep that discipline.

---

## 2. TOKENS

The full file is `tokens.css`, ready to paste. The values that matter:

```
GROUND   --bg #191A1F   --card #202127   --card2 #25262D          (unchanged)
DESK     --dk #141519   --dl #1E2027     4px conic checkerboard    (new)
INK      --ink #F2F1ED  --lbl #CFD0D4    --mut #B6B7BB  --dim #8A8D95
RULES    --grid #33353C --grid2 #4B4E55                            (unchanged)
KEYLINE  --kl #0B0C0F                                              (new — the one re-point)
EDGES    --we #E7E6E1 (document)  --we2 #9DA0A8 (active zone)  --we3 #4B4E55 (inactive)
UNIT     --u 2px = ONE LOGICAL PIXEL
CHROME   --bar 38px (19 logical)  --barz 26px  --status 26px  --strip 30px (15 logical)
GRID     --marg 104px (8×13)   --base 13px   --measure 64ch
SHADOW   --shd #000;  3 button / 4 slip / 6 window / 10 document.  Always `Npx Npx 0 0`.
LAMP     --uvv #9E7BFF  --uvc #7C4A8A  --uvbg #1B1726  --uvi #D8C9FF  --uvg #57F5C4
```

**`--u:2px` is not a taste.** `frame.css` line 9 fixes the machine at *1 logical pixel = 2 CSS
pixels*. The documents adopt the same number, so a keyline in a document and a keyline in the
Finder behind it are the same thickness. Every rule, stripe, gap, plaque inset and bar height is a
whole multiple of `--u`. **Nothing is ever 1px, 1.5px or 3px.** (One exception, stated once: a
*hairline inside a block* — a table row rule, a list row rule, a dot leader — is 1px `--grid`,
because it is printed on the paper and not drawn by the machine. That distinction is the whole
system in one declaration.)

**`--kl #0B0C0F` is the single most important new value.** Kare's icons assume a white page and
close every silhouette in black. On `#191A1F` a black keyline disappears. One step *under* the
desk and it reads as a dark edge instead of a hole. It is the only place we depart from
`kit.js`'s own numbers, and it is what makes a 1984 icon work in a dark room.

### 2.1 THE COLOUR TABLE, AND THE TRAP THAT WILL BITE YOU

`window.KIT.colour` in `src/shell/kit.js` genuinely holds, per file, five entries:

| | keyline `--c0` | base `--c1` | light `--c2` | shade `--c3` | white `--cw` |
|---|---|---|---|---|---|
| **emb** (XTIX, LEADERSHIP, TECH, READ ME) | #000000 | **#2FB380** | #8DD5B9 | #207A57 | #FFFFFF |
| **brass** (OASIS) | #000000 | **#E0A458** | #EECDA3 | #98703C | #FFFFFF |
| **ice** (EVENTER) | #000000 | **#5E8FBF** | #A6C1DC | #406182 | #FFFFFF |
| **ink** (MEDCOIN) | #000000 | **#F2F1ED** | #F8F7F5 | #A5A4A1 | #FFFFFF |

Light comes from the top left and **never moves**: a bar's top face is `--c2`, its right face is
`--c3`, its body `--c1`, its keyline `--kl`. One accent cannot do that; a table can. Nothing in
any document hand-picks a colour again.

> **THE TRAP.** A custom property is substituted **where it is declared, not where it is used**.
> Declaring `--fc-wash: color-mix(--c3 …)` on `:root` and then re-pointing `--c1` on a `.sec`
> leaves the derived tone holding emerald — OASIS renders brass chips on emerald keylines. Every
> derived tone is re-declared on **`.sec`**, the element that already carries the inline `--fc`.
> Do not lift that block into `:root`. It was rendered wrong once, on purpose, to prove it.

---

## 3. TYPE

Five faces. Four are embedded; the fifth is **drawn, not downloaded**.

### 3.1 THE ARCHIVE FACE (drawn from `kit.js`)

`window.KIT.font` is the Finder's 5×7 bitmap, as **data**, so it cannot be a `font-family` — it is
emitted as inline SVG, **one `<rect>` per horizontal run of ink**, integer coordinates,
`shape-rendering:crispEdges`. A 20-character line at scale 3 is about 90 nodes, not 700.

**It has 70 glyphs**: A–Z a–z 0–9 space `- – — . · , /`. I dumped it and checked what the seven
documents actually need: **✓ appears 41 times, ▸ 6, ∅ 4, → 2**, plus `$ % + : ~ ( ) ' ’ & #`.
**None of them exists.** So thirty glyphs are **drawn on the same 5×7 body, with the same advance
rule (width + 1)**, and shipped back into `kit.js` so there is one face and not two. They are:
`$ % + ~ & : ; ' ’ ( ) ! ? ∅ ↻ → ← ▸ ▾ ▴ € ✓ ✗ ° " “ ” = # @`. The extended face is 100 glyphs.

**Three laws.** Never rotated. Never scaled by a fraction. **Never drawn below scale 2** — the
emitter throws rather than substituting, so this cannot rot silently.

**One sizing rule — THE FIT CONTRACT.** A drawn string takes the **largest whole scale that stands
inside the box it is given**, measured, not guessed. This is exactly what `fits()` in `screen.js`
already does for the machine's own window title. Each body carries its computed width as a data
attribute and one pass picks the widest that fits:

```
room = titleCell.clientWidth − 26
pick the first body whose data-w ≤ room; otherwise the mono twin
```

> **BUILD NOTE, and it cost me a render.** The pass must **compute** widths, never measure them in
> the DOM, and the page must render the **narrowest** body before the pass runs. My first version
> measured the bodies and started from the widest: the box's min-content width was therefore set
> by the very string it was supposed to shrink, the container grew to fit it, and nothing ever
> stepped down — a 1120px document window appeared inside a 390px phone. `screen.js`'s own
> `fits()` never measures the DOM; it uses `tw()`. Neither should this.
>
> Every grid and flex item that can contain a drawn string needs `min-width:0`, or a long title
> silently widens the whole document.

**One contract.** Every drawn string carries an identical **JetBrains Mono twin**. The SVG is
`aria-hidden`; the twin is what a screen reader reads and what find-in-page finds. **The string is
never altered, only re-bodied.** Text a reader cannot reach has changed, and the rule says the
text does not change.

**Where the archive face is used — CHROME AND ONLY CHROME.** Window and bar titles; every plaque
(zone numerals, part labels, chip words, state badges, stamps, the selected file label); button
labels; icon captions; the status line; the title card's file name; the microfilm imprint.

**Where it is never used.** Prose. Any figure of Oran's. Any dial figure. Any node label longer
than nine characters. Body copy of any kind.

### 3.2 THE OTHER FOUR

| Face | Job | Sizes |
|---|---|---|
| **Inter** | the argument, and every number | `.para` 14.5/1.7; `.lg .dash .ds .nt .bigtxt` 13.5/600; `.bignum` 800 tabular `clamp(44px,6vw,68px)`; every margin numeral 800/26px tabular |
| **JetBrains Mono** | every label, key, token, meta line, caption, value, and the twin | 7.5–11px, tracking .14–.30em, weights 600/700/800; **8.5px floor on a coarse pointer**, as `#docs` already enforces |
| **Fraunces** | Oran's voice, and **narrower than today** | `.sttl` `clamp(26px,3.4vw,40px)`/700; `.lead .then .qx .vq` italic 17–25px. **Nothing else.** |
| **Special Elite** | the reviewing desk, **untouched** | `.an-t .an-s .ms-t .dv-t`, including `frame.js`'s per-glyph strike variance, which is the truest thing in the archive |

**Why Fraunces keeps `.sttl`.** B and D both moved the document title to Inter 800 or to a pixel
face. A serif italic headline against a striped bitmap bar is the collision that makes this
*authored* rather than pastiche, and it stops working the moment the serif becomes furniture. A, C
and E all keep it and all three are right.

### 3.3 THE ONE INLINE EMPHASIS

`<b>` inside `.para` becomes **the Finder's selection**: `--ink` at 600 on a wash of the folder's
shade at 40%, 1px 3px padding, radius 0, and `box-decoration-break:clone` so it survives a line
break as two clean blocks.

### 3.4 THE RULING: SELECTION, NOT UNDERLINE

C proposed a 2px folder-colour underline under the defined term; E proposed the selection wash.
Both put the folder's colour into every paragraph without colouring a word, and **shipping both
would give the archive two ways to say the same thing.** The wash wins: it is the Macintosh's own
way of saying *this one*, it is the same gesture the sealed cover and the developed plaque make,
and the printed register already has its own devices (the rules, the leaders, the margin). The
underline is dropped.

---

## 4. THE GRID, AND THE THREE REGISTERS

`.wrap` stays 1120px. Inside a document the body is a two-track grid:

```
.blk { display:grid; grid-template-columns: var(--marg) 1fr }    /* 104px | rest */
```

A **1px `--grid` rule runs down the whole file at `x = --marg`.** That is the chapter rule, and it
is the visual spine of every document. The margin track carries apparatus only: the zone numeral,
its leader tick, a figure number. It never carries a word of Oran's.

### THE THREE REGISTERS — this is the hierarchy, and it replaces size and weight entirely

**1 — THE LEAF.** No frame, no bar. The numeral hangs in the margin in **Inter 800 / 26px /
tabular / `--c1`**, right-aligned, its cap on the heading's first baseline, joined to its heading
by a **14×1px `--c1` leader tick crossing the margin rule**. The heading sits in the text column
in JetBrains Mono 10.5/.24em on a 1px `--grid` rule across the measure. This is the owner's-guide
step, and it buys hierarchy at **zero cost to the reading measure**.
*Used for:* most numbered zones, and every lettered zone (A, B, C).

**2 — THE WINDOW, INACTIVE.** `--u` keyline in `--we3`, `--card` field, a **blank** bar carrying
only its name (and a count plaque at the right where the block has one, e.g. `07 GAPS`), hard 6px
black shadow. No stripes, no close box. In System 1 there was no greying: **the absence IS the
state.**
*Used for:* lists that are objects rather than prose — the absence panel, racks, tables, the
thirteen-vendor grid, the performance rows.

**3 — THE WINDOW, ACTIVE.** Stripes on rows 4·6·8·10·12·14 of a 19-row bar, a close box at the
left, an inverted numeral plaque after it, the name **punched through the stripes** in a box of
the bar's own field. **Two or three per document, authored, never more.**
*Used for:* the block the document wants you to land on.

> **STRIPE TONE — a two-level chrome hierarchy for the price of one table entry.** The **document
> window's** bar wears the **base** `--c1`: it is the loudest object in the file and there is
> exactly one of it. An **active zone window's** bar wears the **shade** `--c3`: it is one of two
> or three. Rendered both ways; the base-everywhere version reads as a barcode and the split does
> not.

**THE INACTIVE DISCOUNT.** An inactive window **keeps its colour and spends it one tone down** —
its numeral plaque goes to `--fc-quiet` with light lettering instead of `--c1` with charcoal.
**Colour is never removed to make something quieter; it is lowered.** This is what lets four
colours and eleven blocks coexist on one charcoal page.

**THE TAXONOMY (D's rule, mapped on).** The documents already number at two levels. A **numbered**
point is a *closed card* → it may be a window. A **lettered** point is an *open card* → it is
always a leaf. Nothing else in the five directions shows a structure these files have always had.

**FULL-BLEED, and this list is exhaustive:** the part divider `.plabel/.pl2`, the break band
`.hairtop`, a figure plate wider than the text column, and the archive contents plate. Everything
else respects the margin rule.

---

## 5. EVERY COMPONENT FAMILY, BY NAME

### 5.1 The head — `.sec .case .wrap .shead .rub .d .tok .sttl .smeta .plabel .pl2 .secnum`

The whole head becomes **the document window**, standing on a **desk bed**: 22px of the charcoal
checkerboard with a 1px `--grid` edge, so the window's hard black offset reads as a shadow and not
as a cropped page. (Rendered without it first; it read as a cut edge.)

- `.rub` "CASE STUDY 01" → the **title bar's centre plaque**, punched white-out of the stripes,
  archive face scale 3.
- `.rub .d` → the **close box** at the bar's left: `titlebar()`'s own 11×11 frame with its two
  7-pixel diagonals at its own coordinates. `aria-hidden`, inert. (See §14 risk 3.)
- `.tok` "FILE 01 · INTAKE" → **the status line**: the 26px row directly under the bar with a
  `--u` rule beneath, which is exactly where a real Mac put "7 files". The folder's own name sits
  at its right end, in mono, because that string already exists on the tab.
- `.sttl` → first line of the content area. Fraunces 700, unchanged position.
- `.smeta` → mono 10/.2em beneath it, unchanged.
- `.plabel` / `.pl2` → **the part divider**: a full-bleed 30px band of the desk, ruled `--u`
  `--grid` top and bottom, with the label in an **inverted plaque** let into its left end. `.pl2`
  is the same object; the parts are distinguished by their own strings, not by a second treatment.
- `.secnum` → **`frame.css:233` is `.mw-view .secnum{display:none}`: the ghost numeral does not
  render inside the machine at all.** It is authored for the scrolling page only, where it becomes
  a giant archive-face numeral at scale 24 filled with a 50% checkerboard of the folder colour,
  rising from behind the window's top-right corner onto bare ground. Cheap, and not wasted — but
  **do not spend an hour on it**, because the machine is where the documents are read.

### 5.2 Folder and tab — `.folder .tabrow .tA .nm .fl .tB`

`.folder` **is** the window: `--u` `--we` keyline, `--card` field, hard 10px black shadow, **all
four corners square**. `padding:34px 38px`; the `!important` `padding-left:75px / padding-right:55px`
at `_monolith.html:413` must be **retired deliberately**, not overridden — the margin track
replaces it.

The rounded coloured tab is gone, because the Macintosh had no tabs. It becomes **the file
standing on the desk above its own window**: the 32×32 file icon at ×2, `.nm` under it in a
**selected label** (folder field, charcoal archive face) because the file you have open is the
file that is selected, and `.fl` "▸ FILE 01" in mono 8.5 below. That is `drawScreen()`'s own
icon-and-label construction moved one level in. `.tB` (the dashed ghost tab) becomes the same
label in outline only.

### 5.3 Zones — `.z .zr .zr b .d2 .para .lead .then`

`.zr b` (01, A, ∅→10) **leaves the text column** and hangs in the margin (leaf) or becomes the
bar's inverted numeral plaque (window). `.d2`, the rotated diamond, **dies as a shape and is
reborn as the leader tick** — a rotated square anti-aliases; a 14×1 rule does not. Where a lozenge
is genuinely wanted (`.rub .d`, `.vd`, `.node::before`, `.vmark`), it is `screen.js`'s own
`mark()` — the 9×9 plotted lozenge with its plus-shaped hole, which the repo notes is **ours, not
Apple's**. `.para` Inter 14.5/1.7 capped at `--measure`. `.lead` and `.then` Fraunces italic.

### 5.4 Separators — `.hairtop .cols2 .grid2c`

`.hairtop` → a **break band**: 26px of the desk dither with a 1px `--grid` rule above it, keeping
its existing `scaleX` draw-on (1040ms — a printed rule, so it eases). `.cols2` / `.grid2c` keep
their geometry; the gutter shows the desk. Windows **overlap exactly once per document** (§5.9).

### 5.5 Lists — `.list .lg .c .n .dash .apl .tools .mi .o .reality .fh .frow .st .refl3 .stackr`

**Three idioms that must not look alike, and the first two are a matched pair:**

- **BUILT** (`.lg`, `.lg .c`) — a ruled row, `border-top:1px var(--grid)`, min-height 36 (44 on a
  phone), with a **16×16 solid box** mark: `--c1` fill, `--kl` keyline, light top-left face, shade
  bottom-right, and the tick **knocked out** of it. Label Inter 13.5/600 `--ink`.
- **ABSENT** (`.mi .o`, `.frow .o`) — **the same box, dashed and struck**. `--c3` dashed frame,
  empty, one 2px `--c1` diagonal. Solid + ticked means present; dashed + struck means absent. The
  pair is the entire icon grammar in two marks and **neither may be redrawn without the other**.
- **ENUMERATED** (`.dash`) — a leader row: an 11×2 `--c1` bar, the label, then a **dot leader**
  (a 4px/1px repeating gradient) running to the column's right edge and closing on a 1×7 tick.

`.reality` / `.fh` → an **inactive window with two plaques in its bar**, "STARTING POINT" left and
"07 GAPS" right: the Finder's status line exactly. It is the **one block in the whole archive**
that carries a **thumbless scroll strip** — track and both arrow boxes drawn, no thumb — because
`screen.js` states the rule in its own comment and this is the block whose subject *is* absence.
Nowhere else: 30px of reading width is too expensive to spend on an in-joke twice.

`.tools` (LEADERSHIP's toolkit) and `.stackr` (TECH's thirteen vendors) → racks of small inactive
windows, the `<b>` name in each bar. `.apl` and `.refl3` inherit the enumerated idiom.

### 5.6 Figures — `.statrow .stat .slip .bignum .cur .cnt .biglbl .bigtxt .perfrows .prow .etr .et .en .el .ringlbl`

**A number is a DIALOG.** No title bar — a dialog has none. System 1's **doubled keyline**:
`--u` frame, `--u` clear, `--u` frame, in `--we`.

- `.bignum` — **Inter 800 tabular, `clamp(44px,6vw,68px)`, in `--ink`**, laid on E's **fatbits
  lattice**: an 8px grid of 1px hairlines at 7.5% drawn *over* the figure, so it reads as
  something the archive plotted rather than something a brochure set. **This is the ruling on the
  loudest fact in the file:** D set it in 5×7 at ×9 and B in FatBits with a dithered shadow, and
  in both directions' own renders `$9M+` is the least legible object on the page. The lattice
  gives the 1984 reading at no cost to legibility. The digits stay in Inter.
- `.cur` — the `$` in `--c1` at .42em, because it belongs to the figure and a figure must be read.
- `.cnt` — counts up in `steps(12)`, keeping its real text node for copy/paste and screen readers.
- `.biglbl` — archive face scale 2 under a `--u` `--grid2` rule, as the dialog's own status line.
  The **second** `.biglbl` becomes an **inverted plaque**.
- `.slip` (OASIS's "KEY BUSINESS OUTCOME") — an inverted plaque hanging off the dialog's top-left.
- `.perfrows` / `.prow`, and EVENTER's `.etr/.et/.en/.el` — **racks** of small inactive windows,
  caption in the bar, value in the body. `.en` (03/05/07) is Inter 800/32px in `--c1`, not pixels.

### 5.7 Chips — `.chips .chip`

Each is **a window the size of a stamp**: `--u` `--we3` keyline, a 22px **flat `--c1` bar**
carrying the `<b>` word in charcoal archive face, the caption in mono 10/.11em beneath, hard 3px
shadow, on `repeat(auto-fill,minmax(198px,1fr))` with the desk in the gutters. In brass this is
the handsomest colour object in the archive, and the four-colour proof confirms it holds in all
four tables.

### 5.8 Principles and maps — `.pr .n .nm2 .ds` / `.osmap .spine .node .nn .nt .l .r .tipd`

`.pr` → five leaves, `.n` an inverted numeral plaque in the margin, `.nm2` Inter 700, `.ds` Inter
13.5. `.osmap`'s spine → a `--u` `--c1` column drawing down in `steps(9)`; `.node::before` → the
plotted lozenge, unrotated; `.node::after` → a `--u` orthogonal connector; `.nn` archive face
scale 2; `.nt` Inter 14/600; `.tipd` → the scroll strip's own down triangle at the spine's foot.

### 5.9 The one overlap

Exactly **one per document**: the evidence slip laid across the corner of the figure window it
belongs to, with System 1's hard black offset. **It must land on clear ground and may never cross
a word** — the window under it reserves 58px of clearance for it. My first render had the slip
covering "PIPELINE MANAGED", which is the one thing this move may not do; the clearance is not
optional, and below 860 the offset narrows to 12px.

### 5.10 Quotes, seal and contact — `.sigq .qx .lessq .who .vseal .vmark .vq .vsig .vd .vsep .fcontact .cc .k .v`

`.vseal` is the archive's last **dialog**: doubled keyline, no bar. `.vmark` → the plotted lozenge
at scale 4. `.vq` stays Fraunces italic. `.vd` → a 3×3 pixel square. `.lessq`'s border → a `--u`
`--c1` rule. `.fcontact` → three **push buttons** sharing the one button idiom: `--u` keyline,
0 radius, drawn 3px offset, 44px minimum, `.k` in the archive face in `--c1`, `.v` in mono 15,
inverting on press. The first carries the **default ring**.

### 5.11 `.rv`, and everything the live layer builds

`.rv` keeps its stagger, but a **window** arrives with the machine's **zoom rectangle**: a `--u`
keyline rect snapping 40%→100% in `steps(4)` over 140ms, then its content. A **leaf** keeps the
existing translate-and-fade, because a leaf is printed.

---

## 6. THE ICON SYSTEM

### 6.1 The grammar

**GRID.** 32×32 for objects, 16×16 for marks. Rendered at **whole scale only**: ×1 inline in a
list, ×2 in a window's furniture, ×3–4 on a title card. One `<rect>` per horizontal run,
`shape-rendering:crispEdges`.

**KEYLINE.** One pixel, **closed all the way round the silhouette**, in `--kl`. No icon in this
set is a silhouette. That rule is what lets a Kare icon read at any size on any ground.

**THE TONAL RULE.** Exactly `kit.js`'s five letters and nothing else may appear:
`K` keyline · `C` the folder's base (the body) · `L` light (**the top and left faces, always**) ·
`S` shade (the bottom and right faces and any recessed plane) · `W` specular (**at most three
pixels**, and most icons have none). Where a plane needs half a tone it is a **one-pixel
checkerboard of C and S**, never a third colour. That is Kare's shading and it is what makes an
icon read as an *object* rather than a sticker.

**THE STANDARD OBJECT.** Every rectangular thing comes out of one primitive: fill `C`, frame `K`,
inset top and left `L`, inset bottom and right `S`. A folder, a chip, a bar, a plate and a page
all come out of those four lines, which is why the set looks like a set.

**ONE MAP, FOUR COLOURS.** Every icon is authored once as a 32-row character map and emitted per
folder from `K.colour`. **EVENTER's file icon IS XTIX's file icon in ice.** Nothing is redrawn per
colour, and arming the lamp re-points the table so every icon goes violet in one move.

### 6.2 The set — eleven objects and five marks

| | | |
|---|---|---|
| **FILE** a page with a turned corner and a ruled body | the document, the desk label, `.doctitle` | 32 |
| **FOLDER** the 1984 tab silhouette | the master file, the archive plate | 32 |
| **SLIP** a torn-foot sheet with a seal block | `.evslip`, `.mslip`, the sheet-turn control | 32 |
| **STAMP** a doubled frame with a struck check | VERIFIED, ON RECORD, FOUNDER | 32 |
| **LAMP** the wall plate and its rocker, from `lampSVG()`'s own geometry | `.lampband` | 32 |
| **CHART** five rising bars on a rule | `.bar0`, any evidence block | 32 |
| **GAUGE** a dial, a graduated face and a needle | `.gaug`, KPI, forecasting | 32 |
| **PEOPLE** three figures behind a table | hiring, coaching, `.pr` | 32 |
| **REEL** a film reel with sprockets | `.gen3`, the vault, `.vfilm` | 32 |
| **CHIP** a DIP package with legs out four ways and a dithered core | TECH, the outbound engine | 32 |
| **LENS** a magnifier | the reviewing desk, `.an-note` | 32 |
| **BUILT** a solid box with the tick knocked out | `.lg .c` | 16 |
| **ABSENT** the same box, dashed and struck | `.mi .o`, `.frow .o` | 16 |
| **RULE** a 10×2 bar | `.dash::before` | 16 |
| **GO** a stepped triangle | `.fl`'s ▸, `.sf-go`, every arrowhead | 16 |
| **MARK** `screen.js`'s own 9×9 lozenge | `.rub .d`, `.vd`, `.vmark`, `.node::before` | 16 |

All sixteen are generated by a small Python DSL built on `screen.js`'s own primitives
(`rect/frame/hl/vl/dither/ring/disc/line`), so the tonal rule is obeyed **by construction** rather
than by hand. `BUILT` and `ABSENT` were redrawn together after the first render, where the check
was a bare tick and the gap was a dark disc: they did not read as a pair, and the pair is the
point.

### 6.3 The patterns — six, each with one job

| | density | job |
|---|---|---|
| **VOID** | 0% (keyline only) | absent. The ∅ slot, the unbuilt. |
| **GRAIN** | 25% | an estimate, a range, anything approximate. |
| **HALF** | 50% | the machine's own checkerboard: the desk, a cover, a masked region. |
| **DENSE** | 75% | nearly. |
| **SOLID** | 100% | built, on record, selected. |
| **SPRAY** | stipple | **the light, and only the light.** The lamp. Never in a chart. |

Cells are **4px = 2 logical px**, so a pattern is the machine's own dither at the machine's own
scale and does not resample on a 3× screen. A chart that uses the ramp **publishes the five-cell
legend under it**; a chart that does not, does not.

> **BUILD NOTE.** The SVG `<pattern>` and the CSS `background-image` version of the same pattern
> must be the **same density**. I shipped a 6% SVG grain against a 25% CSS grain and the legend
> printed one word under two different textures — which is precisely the failure that turns a
> published legend into a lie. Both are 25% now. Check this whenever a pattern is added.

---

## 7. CHARTS AND INLINE SVG DIAGRAMS

### 7.1 One law for every drawing

No curve, no bezier, no round cap, no arbitrary angle. Every connector is horizontal, vertical or
45°. Every arrowhead is a **stepped pixel triangle**. Every bar, node and plate follows the **icon
grammar**: `--kl` keyline, `--c1` body, a 4px `--c2` top face, a 4px `--c3` right face. Every
coordinate is an integer and every drawing carries `shape-rendering:crispEdges`.

### 7.2 `.bar0` — XTIX's ∅→10, the flagship

**The number twice: in HEIGHT and in INK DENSITY.** Thirteen slots on one pitch. The three ∅ slots
are **VOID** — a dashed keyline box with nothing in it, **at the height of a first bar**, because
in 1-bit an absence is drawn and never greyed. Bars 01–10 climb the ramp: 01–03 GRAIN, 04–06 HALF,
07–08 DENSE, 09–10 SOLID. The baseline is a 2px `--chrome` rule closing on a five-step pixel
arrowhead. Axis labels are **JetBrains Mono 9px inside the SVG at the exact bar centres** — they
are values, and values are mono. Bars grow in `steps(5)`. The legend sits beneath.

*Never use pattern as the only encoding.* Density is not linear perceptually; it works here
because the height already carries the count and the legend names each step.

### 7.3 `.gaug .g1 .garc .gl` — the dials

A Macintosh cannot draw a smooth arc, so **the dial counts**: **twenty-four whole-pixel beads over
270°** at integer coordinates, on a 9px pitch. Filled beads are `--c1` with a 2px `--c2` top edge;
unfilled are `--grid`. The figure at the centre is **Inter 700, never pixels** — it is one of
Oran's numbers.

**AN ESTIMATE FADES OUT AT ITS END:** `~20%` and `7–8%` draw their **last two beads in `--c3`**,
so the value visibly stops being exact exactly where its own string already says it does. (B's
idea; B's execution was a grain wash over the whole disc, which read as a dirty lens and fought
the figure. Thirty beads at a 7px pitch also closed into a continuous grey band — twenty-four at
nine is the number that reads.)

### 7.4 Node diagrams — `.ndot .pdraw .hop .crawlp .conv .convwrap .mzorg .archw .intb .stackr .phil .pur .u .h0–h4 .tech .bot`

A node is a **box with a flat 6px `--c1` left tab**, a `--c2` line under its top edge and a `--c3`
line above its bottom, on `--card2` with a `--kl` keyline. **Labels of nine characters or fewer
are drawn in the archive face; anything longer stays in mono** — a pixel face you have to squash
is not a pixel face, and the rule is stated so nobody has to guess per string. Connectors are 2px
`--c1` orthogonal runs with stepped arrowheads.

`.crawlp`'s learning loop stops being a bezier: it exits the last node, runs **orthogonally with
square corners**, and re-enters the first, dashed 6/5 in `--mut`, its label rotated 90°. `.hop`
becomes a 2×2 travelling pixel in `steps()`. OASIS's radial ring and EVENTER's convergence hub use
**the same midpoint-circle routine as the dials** — one circle routine in the whole archive.
MEDCOIN's `.mzorg` becomes a ruled track with ticks every 12px, five square knobs with the last
filled, and the unfinished segment a hard dash running into a stepped arrow.

**Converting these is real geometry work, and it is all-or-none.** If only some diagrams are
converted the archive will look like two draughtsmen, which is worse than either alone.

### 7.5 The figure plate

Every drawing sits in a **numbered plate**: a `--u` `--we3` edge on `--card`, the drawing, and a
caption row — `FIG. nn` in `--c1` followed by **the zone's own heading string, re-set**. The
figure number is apparatus; **not one word is added**.

**FIGURES NEVER SHRINK.** A plate wider than its column scrolls sideways inside its own edge:
`overflow-x:auto` on the art, a natural `width` on the SVG, and **`min-width:0` on the plate, its
grid cell and every ancestor**. Shrinking a chart to fit is how a chart ends up with 5px labels.
On a phone the scroller carries its own 1-bit horizontal strip so the affordance is discoverable.

---

## 8. THE PAPER

### 8.1 Evidence slip — `.evslip .es-h .es-row .es-k .es-v .es-stamp`

**A window printed on paper.** It keeps `#E9E7DF` — the one genuinely warm surface in the archive
— and gains the same striped bar in `#22201C`, the same close box, the same punched plaque, and
System 1's hard 6px black offset in place of the soft one. `.es-k` archive face scale 2 in
`#6B6553`; `.es-v` Special Elite 12.5 in `#22201C`; rows on 1px `rgba(34,32,28,.17)`.

The **sheet's rotation goes** (a Macintosh does not rotate a bitmap). The **VERIFIED stamp keeps
its tilt**, because a hand pressed it — see §8.5. It becomes a proper **rubber die**: a 2px border
plus a 1px outline offset 2px, the classic doubled rule, in `#1C6F4E`, which holds on cream.

At its bottom-right, a **peeled corner**: an 18px wedge with a hard fold edge, pointing at the
TURN THE SHEET control. The physical promise the control keeps.

### 8.2 Method slip and the sheet — `.mslip .ms-t .ms-fig .ms-stamp .slipflip .sf-stage .sf-in .sf-tab .sf-sub .sf-go`

The same sheet one shade cooler (`#F7F5EE`), as a **template view**: six labelled fields each in
its own 1px-ruled box, keys in mono .18em, prose in Special Elite, figures in mono 700 — the best
back face of the five, and immune to string length. `ON RECORD` in the same die.

`.slipflip` / `.sf-stage` / `.sf-in` are **untouched mechanism**. `.sf-tab` becomes the archive's
**one button idiom**: `--u` keyline on `--card2`, 0 radius, a **drawn** 3px offset (never a blur),
min-height 44, the SLIP icon at 24px on the left, "TURN THE SHEET" in the archive face at scale 3,
"HOW THIS CLAIM WAS BUILT" in mono beneath, and a stepped triangle at the right. Pressed, it
inverts, its shadow collapses to zero and it translates 3px into its own shadow, in `steps(2)`.

### 8.3 Analyst note — `.an-note .an-h .an-t .an-s .an-w`

Keeps Special Elite, its signature and its **−0.55°**, because a human laid it down. Its ground
becomes **a scrap of the desk itself** — the charcoal checkerboard inside a `--u` `--we3` keyline
— and `.an-h` becomes an **inverted plaque hanging half off the top edge**, like a tab. The
per-glyph strike variance `frame.js` computes stays exactly as it is.

### 8.4 Microfilm stamp — `.gen3 .vaultmark`

A desk note: `--u` `--we3` keyline, the REEL icon at 32px, "ARCHIVE COPY — GEN 3" in the archive
face at scale 2 **blurred .55px** — a bitmap photographed three times, which says generation loss
better than a blurred typeface ever could — and the long sub-line in mono 8. This is the only
blur left in the archive and it is photographic, not decorative.

### 8.5 THE HAND/MACHINE EXEMPTION

**Everything the machine draws is on-grid and orthogonal. Everything a hand left may sit off-grid:**
`.es-stamp`, `.ms-stamp`, `.stamp`, `.an-note`, the tape. Two hands, two geometries — legible
rather than accidental, and it is what licenses us to flatten the slip while keeping the stamp's
tilt.

---

## 9. THE UV LAMP AND THE SEALED COVERS

**The mechanism does not change.** One plate per case folder, three developed zones, a class
toggle, `aria-pressed`, the same strings: `UV LAMP` / `PRESS TO ARM` → `FLUORESCING` /
`365nm · LONG WAVE` → `365nm · 03 ZONES` / `OFF` → `ON`, and
`— REVIEWING DESK, 2026 · DEVELOPED UNDER THE LAMP — NOT PRESENT IN THE PRINTED COPY`.

### 9.1 The plate — `.lampband .uvmount .lamp .lampnm .lampcall .lampsub .lampstate .lampedge`

**It is a System 1 push button, and it always was — finally dressed as one.**

**OFF:** a `--u` `--we3` keyline on `--card2`, min-height 86, and **no ring at all and no colour at
all**. The 32×32 LAMP icon in the folder's table, `UV LAMP` in the archive face at scale 3,
`PRESS TO ARM` in mono 800/13 in `--c1`, `365nm · LONG WAVE` in mono 8.5, and `OFF` as an
**outlined plaque** at the top right.

**ARMED:** the plate becomes **the default button** — the doubled ring arrives in `--uvv`, three
logical pixels thick and one clear, exactly as `pushbutton()` draws it. Its field goes `#221E33`
and takes the **SPRAY stipple in violet at 50%**, which is what lets a lamp glow *without a single
blur entering the archive*. The bar's stripes, where the plate carries them, go violet too — E's
best single lamp idea: the plate becomes the **active window**, which is the machine's own way of
saying "this is the thing you are now operating". The icon takes the violet table. `FLUORESCING`
in `--uvi`; `ON` as an **inverted violet plaque**.

**PRESSED:** the whole plate inverts, instantly. That is the entire feedback, it works under a
finger, and it is what the machine did.

> **Why OFF carries no ring.** Off, the plate carries no colour at all, so **the violet arriving
> IS the event**. A bright ring on a switched-off lamp makes it the loudest object on the page —
> the exact opposite of what it should be.

### 9.2 The developed zone — `.devz .dv-k .dv-t .dv-b .lampsig`

What the lamp did was **SELECT a region of the canvas and show you what is in it**, so the zone
arrives inside a **marching-ants marquee** in `--uvg` — and **the marquee IS its edge**. There is
no second border under it; drawing both gave the block three edges and read as noise.

Inside: a violet-striped bar carrying `.dv-k` (FINDING OF FACT / THE METHOD / ON RE-EXAMINATION)
as its punched plaque in the archive face; `.dv-t` in **Special Elite 15.5 in `#E9E1FF`** with its
bloom removed — it sits on a violet field instead, which is how a 1-bit machine highlighted a
line; `.dv-b` items in Inter 13.5 with a 10×2 violet tick, `em` in mono 700, `b` in `#F3EEFF`.
`.lampsig` in mono 7.5 under a 1px dashed violet rule. The zone opens with `max-height` in
`steps(6)`.

### 9.3 The lit folder

`--c1` is re-pointed inside `.folder.lampon`, so the file's whole accent — stripes, plaques,
numerals, rules, icons, charts — goes violet in **one move**, exactly as the current build goes
silver in one move. The bed drops to `#0A0B0D`; `.vfilm` still swings in.

### 9.4 Sealed covers and stickers — `.rxs .rxb .redx .rxk .rxkhost`

**A Macintosh masked a region by filling it HALF**, so the cover is a **50% dither of `#673A75`
and `#9159A4`** with a `--u` `#A972BD` keyline — never a gradient, never a sheen. Minimum 20px.

> **KEEP `redactionBars()` EXACTLY AS IT IS.** Direction A proposed deleting its measured
> per-line DOM in favour of `box-decoration-break:clone`. I read the mechanism: `.rxb` are
> absolutely positioned `<i>` elements, measured per line box by `lineBoxes()`, re-measured on
> reflow, and revealed by a `--rxp` scaleX written onto the host (`frame.js:765–865`). **A
> transform on a clone-background span moves the text with the cover**, so "the reveal stays a
> transform on the same span" is false as written, and `__rxsUpd` would have to be rewritten — on
> a mechanism whose measurement pass exists because of a scroll fault Oran already reported once.
> Re-dress the bar; keep the machinery. If a wipe is wanted, use `clip-path` in `steps(6)` on the
> existing `.rxb`.

`.redx` / `.rxk` → an **inverted plaque**: violet field, `#F2E9F6` archive face, `--u` `--kl`
keyline and System 1's raised bevel (2px light inset top-left, 2px dark inset bottom-right). The
CSS sheen sweep goes. `SEALED · TAP TO REVEAL ▸` unchanged, now set in the machine's own face,
inside a **44px invisible hit pad** so a thumb cannot miss between two 26px line covers.

---

## 10. THE TITLE CARD — `.doctitle .dt-no .dt-art .dt-rule .dt-cue .swcue` — and `.mw-done`

The card each file opens on becomes **the machine's zoom rectangle, arrived**: a `--u` `--c1`
frame on the desk, `.dt-no` "FILE 03" as an **inverted plaque**, `.dt-art` — which is already
pixel art on canvas — **re-pointed from arcade lettering to the archive face at scale 8**, a
smaller change than it sounds, `.dt-rule` a 4px `--c1` bar, and `.dt-cue` "scroll to read the
file" in the archive face at scale 2 with a four-step blinking down arrow drawn from the scroll
strip's own triangle. `.swcue` takes the same triangle rotated 90° **as a drawing** (it is not
lettering, so the no-rotation law does not bind it).

**`.mw-done` is UNCHANGED** — it is already drawn 1-bit in canvas by `pushbutton()` with its
default ring, and it is already right. **One argument changes:** `frame.js:194` is
`pushbutton(b, 0, 0, w-1, h-1, "DONE", true, WHITE)` and the signature already takes a ring
colour, so XTIX's DONE gets an emerald ring, OASIS brass, EVENTER ice, MEDCOIN white ink. The one
piece of real 1984 already inside the content area becomes the model for every button in the
documents, and that is the proof this system is native rather than applied.

---

## 11. MOTION

**THE LAW: the machine steps, the paper eases.** Anything drawn in pixels changes state in
`steps()`; anything printed, and anything the reader's own hand drives, keeps a curve.

| | |
|---|---|
| a window arriving | the zoom rectangle: a `--u` keyline rect 40%→100% in `steps(4)`, 140ms, then content |
| a leaf arriving | the existing translate-and-fade, unchanged — it is printed |
| `.hairtop` rule | `scaleX` 1040ms `--ease` — a printed rule draws left to right |
| `.bar0` | bars grow in `steps(5)` |
| dial | beads fill in `steps(24)` |
| `.cnt` | `steps(12)`, real text node kept |
| `.pdraw .crawlp .hop` | `stroke-dasharray` in `steps(n)` — a line ARRIVES in pixels |
| `.devz` | `max-height` in `steps(6)` |
| any button | invert + shadow to 0 + translate 3px into it, `steps(2)`, 90ms |
| the lamp rocker | `steps(2)`, 120ms, so it clacks |
| `.rxb` | the existing reveal, kept |

**11.3 THE MARQUEE RUNS ONCE.** The marching ants travel for one 0.7s pass on arrival and then
**stop**, leaving a static dashed marquee. The documents are live DOM inside `.mw-view`, a real
overflow scroller sitting over the machine; **a permanent repaint loop is the one thing in this
system that would actually cost frames.** The same rule kills any infinite keyline blink.

`prefers-reduced-motion` and the repo's `body.static` leave every rule at full width, every figure
drawn, every marquee dashed and every state settled.

---

## 12. THE PHONE

Breakpoint **860**, the repo's own. Every decision below has a precedent in `frame.css`.

- **The margin track collapses to zero.** The gutter becomes a **2px `--c1` rule at 16px inset**,
  and the numeral leaves the margin to become a **hanging numeral on the heading's own line**
  (Inter 800/20px). The leader tick is dropped — at that distance it is noise.
- **Windows keep their keyline and their bar**, because the state lives in the bar and the whole
  hierarchy therefore survives at any width. This is the main reason the system is phone-safe.
- **The bar grows rather than truncate.** Both `.wbar` and `.wbar.z` must be named in the media
  rule: `.wbar.z` outranks a single-class `.wbar` rule, and that is exactly how a zone bar stayed
  24px and spilled its title over the window body on the first render.
- **The scroll strip stands down entirely**, as `frame.css` drops the machine's own below 860.
- **Pixel lettering steps down by whole scales**, then hands the identical string to its mono
  twin, which wraps. Three bodies of the same words, chosen by computed width.
- **Figures scroll, they never shrink**, under their own 1-bit horizontal strip.
- `.cols2`, `.grid2c`, `.statrow`, `.chips`, `.fcontact`, `.osmap` all collapse to one column **in
  the same order**, so the reader's path is identical on both.
- **The shadow ladder halves** (10→6, 7→4, 4→3, 3→2). The document's own shadow is the last to go.
- **44px minimum** on the lamp plate, the sheet-turn bar, every contact row, every chip, and the
  sealed sticker's hit pad. Mono floor 8.5px on `(pointer:coarse)`.
- **Nothing depends on hover.** Active/inactive is authored; armed, sealed and pressed are all tap.

**Verified at 390: `document.documentElement.scrollWidth === 390`, no horizontal page scroll.**

> **MEASURE BEFORE YOU SCREENSHOT.** A full-page Playwright screenshot resizes the viewport, which
> re-runs the fit pass and can leave the page reporting a width it does not have. Reading
> `scrollWidth` *after* the shot reported 390 on a page that was really 525 wide — a check that
> could not fail. Read the width first, then shoot.

---

## 13. THE SEVEN DOCUMENTS — what each one's colour and material do

The system is one system. What keeps the seven distinct is **which table they draw with, which
material they are made of, and which register dominates.**

### XTIX — emerald `#2FB380` · *the machine being built*
The founding file and the only one with the full apparatus: a bar chart, three dials, a node
diagram, a big figure, an absence panel and two parts. Its material is **the density ramp** —
XTIX is the only document whose data is drawn twice, in height and in ink, because it is the only
one whose subject is a thing being *built up from nothing*. Its ∅ slots are the archive's purest
image of absence. **Register: windows and leaves in even alternation**, the absence panel inactive
and "WHAT I BUILT · (AFTER)" active — the only file where an absence and its answer face each
other as two windows. It carries the one overlap and the one thumbless scroll strip.

### OASIS — brass `#E0A458` · *the cadence*
The warmest table in the archive, and the file with the most **solid caption bars**: seven chip
plates plus the outcome bar, each a flat brass field with charcoal bitmap. That is its material —
OASIS is the file you recognise by the *number of small bright plaques on it*, which is right for
a document about rhythm and cadence. Its radial org ring uses the midpoint circle. **Register:
leaf-dominant** with the chip rack as its one active window, because a cadence is a list of habits
and not a machine.

### EVENTER — ice `#5E8FBF` · *the funnel*
The darkest and coolest table. Ice is the one colour that would fail AA if it ever set prose, and
the system forbids that outright: ice touches structure, data and plaques, never a sentence, and
`#191A1F` on ice at plaque weight clears comfortably. Its material is **the rack** — `.etr/.et/.en/.el`
as three small inactive windows in a row, reading as a trail, plus the convergence hub. **Register:
a leaf spine with one rack**, the quietest of the four case files by design.

### MEDCOIN — bone `#F2F1ED` · *the founder file*
**The file with no second press run.** Its base *is* the ink, so its hierarchy is **structural,
never chromatic**: `--chrome` drops to `--lbl` so content still reads brighter than furniture; its
dividing rules are 2px where the others are 1px; its tint block is bone at 5%; and its caption bars
are white with black machine lettering — **FOUNDER on white is the handsomest object in the
archive**. Its document bar carries white stripes, which makes it the loudest bar anywhere, and
that is correct: MEDCOIN is the file where every decision was his. Its material is **the origin
line** — a ruled track, five square knobs, the last filled, the unfinished segment a hard dash
into a stepped arrow. Severe, and severe on purpose. If it ever reads as unfinished rather than
severe, **push the structure further and do not give it a colour it does not have.**

### LEADERSHIP — emerald · *the hand*
Emerald, but it must not read as XTIX. Its material is **the rack of tools**: ten small inactive
windows, each with a 16×16 icon and its label — the document says "toolkit" and the design stops
paraphrasing it. It is the file with **five principle leaves** and the PEOPLE icon, and it is the
only case file whose dominant object is a human one. **Register: almost entirely leaves**, one
rack, no chart. Fraunces appears twice: the title and `.qx`.

### TECH — emerald · *the diagram*
One wide architecture and thirteen vendors, so it is the file that is **mostly one figure plate**.
Its material is **the orthogonal diagram at full width**, scrolling inside its own edge rather
than shrinking, with `.intb` and `.phil` as full-width inverted plaques and `.stackr` as a rack of
thirteen stamp-sized windows. **Prototype this document first.** It has the fewest blocks and the
most drawing, so it is where the geometry work either holds together or reveals that the
orthogonal law is more expensive than it looks.

### READ ME — emerald on the page, **silver `#E6EAF6` inside the vault**
The closing file. `#final` keeps its `#0A0B0D`, its vignette, its film rebates — the one genuinely
photographic object in the archive — and the silver is delivered by the **same one-line `--c1`
re-point the lamp performs**, so "this file has gone to silver" is one mechanism and not two. Its
material is **the ladder**: nine principle leaves alternating either side of a 1px silver spine,
each tied by a leader to a plotted lozenge. It ends on the archive's last **dialog** — the seal,
doubled keyline, no bar — and then on `DONE`.

---

## 14. BUILD ORDER, TRAPS, AND WHAT IS NOT YET PROVEN

### 14.1 Build order

1. **`tokens.css`** at the head of the document CSS. Retire the `!important` stack
   (`.case .plabel`, `.case .folder` padding at `_monolith.html:413`, `.lampband`) **deliberately**,
   not by overriding it, or you will have two descriptions of every block again.
2. **The emitter**: port `archive_kit.py` to JS, or bake its SVG output into the repo. It reads
   `kit.js`, keeps the 70-glyph face exactly, adds the 30 drawn glyphs, and emits the icons.
   It must **throw** on a glyph outside the face.
3. **The fit pass**: fifteen lines, computed widths, one run at load and one debounced on resize.
4. **TECH first** — fewest blocks, most drawing.
5. Then XTIX (the full apparatus), then OASIS, EVENTER, MEDCOIN, LEADERSHIP, READ ME.

### 14.2 The traps, in the order they will bite

1. **The derived-token trap.** Re-declare on `.sec`, never `:root`. §2.1.
2. **The fit pass must compute, not measure**, and must render the narrowest body first. §3.1.
3. **`min-width:0`** on every grid and flex item that can hold a drawn string or a wide figure.
4. **`.wbar.z` outranks `.wbar`** — name both in the phone rule. §12.
5. **SVG and CSS versions of a pattern must be the same density.** §6.3.
6. **Do not touch `redactionBars()`.** §9.4.
7. **`frame.css:233` hides `.secnum` inside the machine.** Do not spend time there. §5.1.
8. **Measure the page width before the screenshot, not after.** §12.

### 14.3 What the specimen proves, and what it does not

`specimen.html` / `specimen.png` (1200×5207) / `specimen_phone.png` (390×8777) render **on XTIX's
own strings**, with every string lifted verbatim from `src/doc/xtix.html` or `src/shell/frame.js`.
They demonstrate: the document window and its desk bed; the file on the desk; the three registers
side by side; both list idioms and the struck counterpart; the figure dialog with its lattice; the
density-ramp chart with its published legend; the counting dials; the orthogonal diagram; the chip
row in brass; the slip overlapping its figure with the peel and the die; the sheet-turn button;
the analyst note; the microfilm stamp; the lamp OFF and ARMED; the developed zone inside its
marquee; a sealed line covered and revealed; the sixteen icons and marks; and the four folders in
one row.

**They do not prove:** seven whole documents. The per-document authoring pass — which block is a
leaf, which is a window, which window is active — is real judgement work and it is where this
system will either hold together or reveal that some file does not want the form it was given.
The discipline that keeps it honest is one sentence: **two or three active windows per document,
no more.** If that discipline slips, the direction fails loudly rather than quietly.

**What is still weak, honestly.** The ABSENT mark is quieter than BUILT — deliberately, since
absence should not shout — but at 32px in an icon wall it nearly disappears, and it only really
earns its keep at 16px in a row next to its partner. The desk dither is about four steps of
lightness and vanishes entirely in a downscaled screenshot; in the real build it probably wants
one more step of contrast. The drawn `%` and `~` are the weakest of the thirty added glyphs and
are only legible in context. And a specimen flatters any system more than a real document will:
these plates are isolated, and a live file is 8,000px of continuous reading.
