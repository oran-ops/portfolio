# PAPER UNDER GLASS — the redesign of the seven documents

**Status: a plan and a set of built pictures. Nothing in `src/` has been changed.**

Oran, 2026-09-23: *"The documents today speak the visual language of the previous portfolio — very
modern. I want a new, detailed plan with a visual example of how the new page will look when it is
in keeping with the Mac's design… in colour, keeping each folder's own colour, done as an art that
characterises the old Macintosh, with its elements… a new plan for all the icons, all the elements,
all the additions, all the visuals — everything. One very important rule: the text does not change
in any way. The structure of the page in terms of its points stays in the same flow. The matte /
charcoal colours stay. The UV lamp effect stays. Take the old Macintosh and reinvent it inside my
portfolio."*

---

## HOW THIS WAS MADE

Five design directions were developed independently, each anchored in a different part of the
machine's world, and each one built its own component strip in real HTML and rendered it:

| | direction | anchor |
|---|---|---|
| A | THE FILE IS A WINDOW | System 1's own furniture: the striped bar, the close box, the status line, the scroll strip, and the one thing a window has that a card has not — a STATE |
| B | THE FILE IS A MACPAINT DOCUMENT | the pattern palette, FatBits, the marching ants |
| C | THE FILE IS THE MANUAL THAT CAME IN THE BOX | 1984 print: the margin, the hanging numeral, the leader tick, the figure caption |
| D | THE FILE IS A STACK | HyperCard: the card, the background, the roundrect, the shadowed edge |
| E | THE FILE IS A RESOURCE | ResEdit: the 32×32 icon map, the colour table, the bench |

Three judges then scored all five through three different lenses — *is it the Macintosh reinvented
or a costume*, *does it serve a CEO's case file*, *will it survive the build*. All three ranked **A
first, independently**. The system below is A's spine with C's apparatus, E's colour engine, D's
taxonomy and B's texture layer grafted on; `SYSTEM.md` §0.2 records exactly what was taken from each
and what was dropped.

## THE ONE IDEA

> **Every block is either a LEAF or a WINDOW.**
> A leaf is printed: no frame, no bar, its numeral and leader tick hanging in the margin beside it.
> A window is glass: a keyline, a title bar, plaques, and a state.
> **The document is printed. The archive that holds it is a machine. The reader sees both at once.**

That split is what makes the hierarchy work without moving a single word: two or three windows per
document wear a striped bar in the folder's colour and everything else is quiet, so the eye lands
where the evidence is.

## WHAT IS BUILT AND WHAT IS NOT

**Built, rendered and checked** (`docs/redesign/`): XTIX whole, at 1200 and 390, lamp off and lamp
armed; OASIS (brass) and MEDCOIN (bone) whole, both states; the kit sheet — patterns, the object
rule, the icons at 32×32 with their grids, the paper and the stamps, the lamp; and the family sheet
— the same three components in all four folder colours.

**Not built yet:** EVENTER, LEADERSHIP, TECH and READ ME were never drawn. TECH is the one the plan
itself calls the hard case (§14.1), so it should be built first, before a line of production code.

**Known holes, named by the completeness critic:**
- **Focus, disabled and press states do not exist in the plan.** The repo carries eleven
  `:focus-visible` rules today; the redesign retires the document CSS and replaces none of them.
  This is an accessibility regression, not a preference, and needs a drawn answer first.
- **LEADERSHIP's ten tools** need ten 16×16 icons the set does not have, and two of the five
  existing marks do not survive 16px.
- **Hover is dropped without an inventory:** 23 `:hover` rules exist today; three live links would
  lose all desktop feedback.

## WHAT I DECIDED, SO THE PLAN CAN BE EXECUTED

1. **The documents are measured against the window, not the page.** They are read inside the
   machine; `frame.css` already hides the ghost numeral there. The 1120px `.wrap` and the 860
   breakpoint are aimed at a reader who no longer exists.
2. **The archive face is chrome only** — title bars, plaques, stamps, status lines — and never
   larger than scale 3 in the body flow. Two of the builds broke this and the drawings shouted.
3. **`∅` is not redrawn.** The chart's axis and the `∅→10` heading are set in mono, so one of
   Oran's own characters is never redrawn to fit a face.
4. **VERIFIED and ON RECORD stay green in all four folders**, as a stated exemption: they are ink
   on paper, not the machine's colour.
5. **The file standing on the desk carries the Finder's own label**, because it is the Finder's own
   icon; both strings already exist in `src/`, so no new word enters the page.
6. **The focus ring is the machine's marquee** — a 2px dotted black-and-white outline, the one the
   Finder used for selection — on every control the redesign introduces.

## ORAN'S DECISIONS — 2026-09-24

1. **The lamp stands at the HEAD of the file**, where it stood before. Settled.
2. **Its violet reaches the FOLDER ONLY, never the whole room.** The ground stays `#191A1F` at all
   times; `§9.3`'s licence to drop the bed to `#0A0B0D` applies inside the folder and nowhere else.
3. **LEADERSHIP, TECH and READ ME need nothing to close them.** They are not case folders, they
   have no lamp, and — Oran: *"they have the document itself when the reader enters them."* No new
   closing device is to be invented for those three.
4. **The numbering rule is his own text's rule.** Verified across all seven files: a NUMERAL marks
   a point in the first part of a file, a LETTER marks a point in its evidence part. XTIX and OASIS
   run 01–04 and then A · B · C; EVENTER and MEDCOIN are numerals only; TECH and LEADERSHIP are
   letters only. Nothing is renumbered, and no marker is invented for a file that has none.

   | file | first part | evidence part |
   |---|---|---|
   | XTIX | 01 02 03 04 | A B C |
   | OASIS | 01 02 03 04 | A B C |
   | EVENTER | 01 02 03 06 07 | — |
   | MEDCOIN | 01 … 06 | — |
   | TECH | — | A B C |
   | LEADERSHIP | — | A B |
   | READ ME | — | — |

### Still open, and being measured now

- **XTIX in one column or two.** Oran: *"one column is possible — it depends on the length it
  creates. It has to be checked and decided."* Being measured: the height of the whole file in both
  variants, in screens of the document window, at 1200 and at 390 (where two columns collapse to one
  anyway), with both rendered side by side.
- **LEADERSHIP's ten tools.** Oran: *"I need to see the new icons and/or the rack in order to
  decide."* Both are being drawn: ten new 16×16 icons proved distinguishable at 1×, and the rack of
  named windows, each rendered in emerald at 1200 and 390.
- **The chart legend.** Oran prefers numerals, with the caveat that they must not compete with the
  document's own numbering. XTIX's density ramp currently carries numeral ranges inside a file whose
  zones are already 01–04; three candidates are being rendered, including one with no legend words
  at all, since the chart's own axis already says `∅→10`.

## THE FILES

- `SYSTEM.md` — the whole plan, 60 KB, written so a builder can execute it without asking a
  question: tokens with values, type with sizes, the grid, all 110 component classes from the
  inventory answered by name, the icon system, the charts, the slips, the lamp, motion, the phone,
  and a section per document.
- `redesign/tokens.css` — the custom properties, ready to paste.
- `redesign/*.png` — the pictures listed above.

The sources that produced the pictures (HTML, CSS, the Python that draws the archive face and the
icons from `src/shell/kit.js`, and the string verifier that proves not one word was invented) are
kept outside the repo, in this session's scratchpad, and can be moved in when the build starts.
