# Architecture — the hub portfolio

This document is the contract. Nothing gets built until it is agreed, and when the two
disagree, this document is wrong and gets fixed first.

**The governing rule, from which every other decision follows:**

> **The shell is 1984. The content is 2026.**

Everything that is *the machine* — the world map, the folder, the desktop, the icons, the
window chrome, the cursor — is old, pixelled, isometric. Everything that is *the work* stays
exactly as it is built today. Page 2's sentence is not a caption on this design; it **is** the
structure.

---

## 1. What exists today, measured

Not estimated. These are counts from `m/index.html` and `build/`.

| | |
|---|---|
| `m/index.html` | 688 KB, one file |
| inlined fonts | 222 KB binary, **299 KB as base64** — a 35% penalty for inlining |
| CSS | 179 KB, 1,529 rules, 4 `<style>` tags |
| JavaScript | 143 KB, 2,960 lines, **23 `<script>` tags**, 105 functions |
| event listeners | 61 `addEventListener`, 132 `querySelector` |
| observers | 21 `IntersectionObserver`, 32 `requestAnimationFrame`, 37 `getBoundingClientRect` |
| responsive | 26 `matchMedia`, 100 `@media` blocks (20 distinct queries) |
| **routing** | **`history.*` × 0, `location.hash` × 0 — there is none** |
| external requests | 1, a LinkedIn profile link. No external assets. |
| build | ~100 one-off Python patch scripts in `build/` |

### 1.1 The problem in one sentence

**The source is the same size as the output.** `site_mobile.html` is 703 KB and is edited in
place by string surgery; `build_mobile.py` adds a `<head>` and copies it. There is no smaller
representation to reason about, so every change is a search-and-replace on a 700 KB file, and
`build/` — `round7`, `round7b`, `round7c`, `round7d`, `page4_fix`, `fix_agent1` … `fix_agent7` —
is an archaeological record rather than a build system.

### 1.2 The finding that makes migration safe

CSS scoping, across all 1,529 rules:

| | rules | share | disposition |
|---|---|---|---|
| scoped to exactly one section | 545 | 36% | **moves with its section** |
| spanning several sections | 21 | 1% | **decided one by one** (§11.3) |
| global / kit | 963 | 63% | **stays in the kit** |

Per section: `final` 174, `hero` 140, `statement` 58, `medcoin` 37, `philosophy` 36, `tech` 36,
`files` 23, `leadership` 18, `xtix` 16, `eventer` 4, `oasis` 3.

The four case files carry almost no styling of their own — 16, 3, 4 and 37 rules — because they
share one `.case` template. **The expensive-looking part of the migration is the cheap part.**

### 1.3 There are two sites, not one

This was missed on the first pass and it changes the scope.

| file | size | built from |
|---|---|---|
| `index.html` | 945 KB | `src_site.html`, 925 KB |
| `m/index.html` | 688 KB | `site_mobile.html`, 703 KB |

Both carry **the same eleven sections in the same order**. They are 78% similar. Neither links
to the other and neither redirects to the other. `build_mobile.py` carries a hard guard that
aborts if it would touch the root file — which is what gets written when two things must never
meet.

So the same eleven sections are maintained **twice, by hand, in two 900 KB files**. Every copy
change is made twice or the two drift apart. **Collapsing them into one source is the largest
single maintenance win available here**, and §9's "one source, two layouts" is only worth
saying if it replaces both. See §14.2.

### 1.4 A quarter of the shared CSS is dead

The 963 rules that are not scoped to a section, classified by where their classes actually
appear in the markup:

| | rules | bytes | disposition |
|---|---|---|---|
| prologue / shell only | 222 | 31.4 KB | the kit |
| shared | 159 | 20.0 KB | the kit |
| element / global | 146 | 12.0 KB | the kit |
| documents only | 229 | 27.3 KB | **ships with its document, not the kit** |
| **matches nothing in the markup** | **207** | **26.3 KB** | **dead — delete** |

**The kit is 61 KB, not 114**, and 26 KB goes in the bin. This is the difference between §13's
budget being achievable and being a wish.

### 1.5 The JavaScript splits too

The 143 KB across 23 script tags is not one program. Counting references to the seven document
ids per tag: tag 7 has 17, tag 5 has 14, tag 1 has 10, tag 10 has 8 — those go with the
documents. Tag 20 is 21.5 KB and belongs entirely to page 2's statement. Tag 19, 6.3 KB, drives
the rotating drawer that §14.1 deletes.

The shell keeps the router, the isometric renderer, the machine and the desktop. It does not
keep the documents' animation code, and the budget in §13 assumes that split.

### 1.6 The two builds have diverged — neither contains the other

§1.3 assumed the two sites were one design in two layouts. They are not. They are two
generations, and copy exists in each that does not exist in the other.

Their visible word counts are 2,256 and 2,250 — six words apart, which is exactly the sort of
coincidence that lets a divergence hide. Comparing block by block instead
(`tools/reconcile_content.py`):

| section | decide | new in m/ | rewrites | artefacts | |
|---|---|---|---|---|---|
| `hero` | 1 | 1 | 0 | 15 | being replaced anyway |
| `statement` | 1 | 0 | 0 | 0 | |
| `philosophy` | 0 | 0 | 0 | 0 | **identical** |
| `files` | 5 | 3 | 1 | 5 | being replaced anyway |
| `xtix` | 4 | 3 | 3 | 6 | |
| `oasis` | 4 | 3 | 2 | 3 | |
| `eventer` | 0 | 4 | 1 | 0 | |
| `medcoin` | 2 | 7 | 2 | 0 | |
| `leadership` | 0 | 0 | 0 | 0 | **identical** |
| `tech` | 0 | 1 | 1 | 0 | |
| `final` | 0 | 2 | 1 | 0 | |
| **total** | **17** | **24** | **11** | **29** | |

**This table replaces an earlier one that said 52, and the correction matters more than the
number.** The first count treated every unmatched block as lost copy. Three kinds of thing are
not lost copy:

- **artefacts** — both pages animate their figures, so one capture freezes at `0M+` and the
  other at `9M+`. Five of xtix's nine raw differences were exactly this.
- **rewrites** — `Prioritised Global expansion` became `Prioritized global expansion`. A diff
  reports one deletion and one addition; it is a spelling fix.
- **improvements** — medcoin's root line *"Every commercial decision affects operations. Every
  operational decision affects profitability"* became three lines in `m/`, the third of which,
  *"Every strategic decision affects survival."*, did not exist before.

**Across the seven documents there are 10 candidates, not 52** — and reading all ten resolved
them to **one**: a single line restored to `oasis`. Every other candidate was already present in
`m/` under better wording. The full record is in `DECISIONS.md` #15-19.

Oasis is the pattern in miniature: of its four candidates, three were already covered by better
wording in `m/` — `Standardized commercial processes` → `Designed the commercial process` — and
one was a real gap. A string-similarity tool cannot tell a reworded claim from a dropped one. It
narrows the field; the reading is still the work.

`m/` is, on this evidence, consistently the better copy. The root is a source to harvest from,
not a version to restore.

Some of what only the root has is real writing, not chrome: *"If you connect to the vision,
you'll always know where you're going."*, `MEMO — FROM THE ARCHIVE`, `FOUNDER CASE STUDY`,
`Recruited an entire sales team`, `Conducted weekly coaching sessions`, `Built onboarding
documentation`, `Standardized outbound methodology`, `Supported international commercial
expansion`, `Raised external investment`.

The full sheet is `docs/CONTENT_RECONCILIATION.md`, regenerated by the tool.

---

## 2. Principles

1. **Wrap, never rewrite.** The seven documents are cut out mechanically and verified by
   pixel diff. Not one of them is re-typed.
2. **New code is born small and separate.** The shell does not inherit the monolith's habits.
3. **One world, not three.** The world map, the folder and the desktop share one isometric
   projection, one tile size, one sprite sheet, one renderer (§7).
4. **One state machine, not 61 listeners.** (§5)
5. **One source, two layouts.** Desktop and mobile differ in stated ways and nowhere else (§9).
6. **Every number in this document is checked by the build.** (§12)
7. **No external requests.** The single LinkedIn link is the only permitted exception.
8. **Nothing is added at the end.** Sound, motion and copy are designed with the thing they
   belong to, because each of them is the first to be cut when it arrives last.

---

## 3. Source tree

```
src/
  kit/                        the 1984 kit — everything shared
    palette.css               colour tokens, unchanged from today
    reset.css                 the existing reset, extracted
    chrome.css                window frame, title bar, buttons, scrollbar, cursor
    type.css                  font faces and the type scale
    iso.js                    the isometric contract (§7): project, sort, blit
    sprites.png               one sheet, all tiles and icons
    sprites.json              atlas: name -> {x, y, w, h, ax, ay}
  shell/
    router.js                 the state machine (§5) and the URL map (§6)
    boot.js                   asset gate, first paint
    page1_map.js              the world map scene
    page2_statement.html      unchanged, lifted whole
    page3_folder.js           the folder scene
    page4_machine.js          camera approach, floating caption, hit test
    desktop.js                the CRT desktop, icon grid, window manager
    docframe.js               fetch, mount, unmount a document
  doc/
    xtix.html    xtix.css     each is markup + its own scoped rules
    oasis.html   oasis.css
    eventer.html eventer.css
    medcoin.html medcoin.css
    leadership.html leadership.css
    tech.html    tech.css
    final.html   final.css
  content/
    copy.json                 every string in the shell, in one place (§10)
    manifest.json             the seven documents: id, title, icon, colour, order
build.py                      the only build step
docs/
  ARCHITECTURE.md             this file
  CONTENT_RECONCILIATION.md   the 52 copy decisions, regenerated by tools/
```

Output:

```
m/
  index.html                  shell only
  app.css  app.js             kit + shell, concatenated
  doc/xtix.html  …            seven fragments, fetched on open
  asset/
    font/*.woff2              five faces, separate and cacheable
    sprites.png
    mach.bin                  desktop machine
    mach-lite.bin             mobile machine
```

---

## 4. The build

`build.py` replaces all ~100 scripts in `build/`. One command, one input tree, one output tree,
deterministic, no in-place editing of anything.

```
read src/content/manifest.json
  -> for each document: read doc/<id>.html and doc/<id>.css
  -> concatenate kit/*.css + shell CSS         -> m/app.css
  -> concatenate kit/*.js  + shell/*.js        -> m/app.js
  -> render index.html from the shell template
  -> copy assets, hashing filenames for cache
  -> run every check in §12; refuse to write if any fails
```

Rules:

- **The build never edits its own input.** `src/` is read-only during a build.
- **The build is idempotent.** Running it twice produces byte-identical output.
- **`index.html` at the repo root is never touched by a build.** The md5 guard in
  `build_mobile.py` is kept permanently and extended to the whole `m/` tree. The root changes
  exactly once, by hand, when it becomes the redirect described in §14.2.
- **`build/` is retired**, not deleted: moved to `build/_legacy/` with a README explaining that
  it is the record of how the monolith was made and is no longer runnable.

---

## 5. The state machine

One object. Every navigation in the product is a transition in this table and nothing else.

### 5.1 States

| state | what the reader sees | scroll | machine | history entry |
|---|---|---|---|---|
| `boot` | the loading gate | locked | not loaded | no |
| `prologue` | pages 1–3, scrolling | page scroll | not loaded | yes |
| `machine` | page 4, the machine, orbitable | **locked**, given to the camera | loaded | yes |
| `desktop` | the CRT desktop, icons | locked | loaded, held at the zoom pose | yes |
| `doc` | one document, full frame | document scroll | held, hidden | yes |

`doc` carries one parameter: `id ∈ {xtix, oasis, eventer, medcoin, leadership, tech, final}`.

### 5.2 Transitions

| from | to | trigger | guard | transition |
|---|---|---|---|---|
| `boot` | `prologue` | shell assets ready | — | fade |
| `prologue` | `machine` | scroll passes the end of page 3 | machine asset loaded | scroll hands off to camera |
| `machine` | `prologue` | scroll up past the handoff | — | camera hands back to scroll |
| `machine` | `desktop` | click/tap the machine | — | **camera flies into the CRT** until the glass fills the frame, then the 2D layer takes over |
| `desktop` | `machine` | Esc, back, or the close box | — | camera flies out |
| `desktop` | `doc` | single click on an icon | fragment fetched | icon zooms, document opens |
| `doc` | `desktop` | close box, Esc, back, or reaching the end | — | document closes, desktop returns |
| `doc` | `doc` | next/previous within a document's footer | fragment fetched | crossfade |

### 5.3 Entry and exit actions — the part that is usually forgotten

Every state declares both. This is where scroll-lock bugs live.

| state | on entry | on exit |
|---|---|---|
| `prologue` | restore page scroll; restore scroll position; start page-1 animation loop | pause the animation loop |
| `machine` | lock page scroll; start the render loop; bind pointer for orbit; show the caption | stop the render loop; unbind pointer; **restore scroll** |
| `desktop` | keep the machine at the zoom pose; render the desktop layer; focus the first icon | release focus |
| `doc` | mount the fragment; **run the reveal pass over it (§11.5)**; reset its scroll to top; set the page title; mark it read | unmount; **release its stylesheet**; remember its scroll position |

### 5.4 Rules

- **One renderer runs at a time.** `machine` and `desktop` share the WebGL loop; `prologue` and
  `doc` do not run it at all.
- **Scroll is owned by exactly one state.** Locking and unlocking happens only in entry/exit.
- **No state is reachable except through this table.** No direct DOM handler may change state.
- **Loading is the one exception, and it is a rule rather than a row.** On load, `boot` goes
  directly to whichever state the URL names, once that state's assets are ready, with no
  animation. `any` is not a state and never appears as a transition target.

---

## 6. URLs and history

Hash routing. GitHub Pages serves static files, and path routing needs a 404 rewrite trick that
would break the moment the repo is renamed.

| URL | state |
|---|---|
| `/portfolio/m/` | `prologue` |
| `/portfolio/m/#/machine` | `machine` |
| `/portfolio/m/#/desktop` | `desktop` |
| `/portfolio/m/#/doc/xtix` | `doc(xtix)` |

The bare URL enters `prologue` at the top of page 1.

- Every transition calls `history.pushState`, except `prologue ⇄ machine`, which is a scroll and
  uses `replaceState` — otherwise scrolling up and down fills the back stack with junk.
- `popstate` drives the machine; the machine never reads the URL except on load.
- An unknown hash falls back to `prologue` rather than erroring.
- **This makes every document shareable**, which is the point: a link straight to XTIX.

---

## 7. The isometric contract

The single biggest simplification available. The world map, the folder scene and the desktop
icons are the same kind of object: an isometric scene made of tiles and sprites. Defined once,
they share one renderer, one sheet and one look; defined three times, they become three worlds
that never quite match and three places to change when the style moves.

| | value | why |
|---|---|---|
| projection | **2:1 isometric** | what SimCity, The Sims and Age of Empires used; the only ratio that is pixel-exact |
| tile | **64 × 32 px** at 1× | comfortable for the detail level in the references |
| scale | integer only: 1×, 2×, 3× | any fractional scale destroys pixel edges |
| world → screen | `sx = (x − y) · 32`, `sy = (x + y) · 16 − z · 16` | |
| sprite anchor | bottom centre of the tile diamond | |
| depth order | painter's, by `x + y`, then `z`, then draw order — **not** `x + y + z`, see below | |
| canvas | `image-rendering: pixelated`, backing store at 1× then scaled | crisp at every zoom |
| colour | **tokens only** (§8.1) | art may not introduce a colour |

Worked, because a projection stated and never evaluated is a projection nobody has checked:

| world | screen | |
|---|---|---|
| `(0,0,0)` | `(0, 0)` | the origin |
| `(1,0,0)` | `(+32, +16)` | one tile east |
| `(0,1,0)` | `(−32, +16)` | one tile south |
| `(1,1,0)` | `(0, +32)` | one tile down the diamond |

One tile therefore spans 64 px across and 32 px down — the 2:1 ratio, exactly.

**One `z` unit lifts 16 px, which is half a tile height.** This is stated because it is the one
number in the contract that cannot be inferred from the others: a cube one tile square and one
tile tall is `z = 2`, not `z = 1`. Half-units exist so a path can sit a step above its ground
without a whole block of lift.

**Why not `x + y + z`.** That was the rule here until a test disagreed with it. Height does not
move a sprite toward the viewer, it lifts it on screen. A tower at `(0,0,9)` and a person at
`(3,3,0)` score 9 and 6 under the old key, so the tower is drawn over a person standing well in
front of it. Under `x + y` they score 0 and 6 and the person is in front, which is where they
are. `z` remains the tiebreaker, and must: two crates on one tile differ in nothing else, and
the upper one is drawn second. Covered by `tools/test_iso.js`.

`iso.js` exposes exactly four functions: `project(x,y,z)`, `sort(list)`, `blit(name,x,y,z)`,
`hit(sx,sy) -> {x,y,z}`. Nothing else. Every scene is a list of placed sprites.

---

## 8. The 1984 kit

### 8.1 Palette — unchanged

Taken verbatim from today's `:root`. **No new colours.**

| token | value | role |
|---|---|---|
| `--bg` | `#191A1F` | ground |
| `--card` | `#202127` | surface |
| `--card2` | `#25262D` | raised surface |
| `--ink` | `#F2F1ED` | text, and MEDCOIN's colour |
| `--mut` | `#B6B7BB` | muted text |
| `--dim` | `#B6B7BB` | muted text, deprecated alias |
| `--lbl` | `#CFD0D4` | labels |
| `--grid` | `#33353C` | rules |
| `--grid2` | `#4B4E55` | edges |
| `--hair` | `rgba(255,255,255,.09)` | hairlines |
| `--emb` | `#2FB380` | XTIX, and leadership/tech/final |
| `--brass` | `#E0A458` | OASIS |
| `--ice` | `#5E8FBF` | EVENTER |

*Note: `--mut` and `--dim` hold the same value today. The kit keeps both names so nothing
breaks, and marks `--dim` deprecated.*

### 8.2 The seven icons

The reader picked seven equal icons in **different shapes** — which is how old desktops said
"these are different kinds of thing" without a word of explanation.

| document | icon | colour | order |
|---|---|---|---|
| XTIX | case file — document with a folded corner | `--emb` | 1 |
| OASIS | case file | `--brass` | 2 |
| EVENTER | case file | `--ice` | 3 |
| MEDCOIN | case file | `--ink` | 4 |
| LEADERSHIP | ruled notepad | `--emb` | 5 |
| TECH | system suitcase | `--emb` | 6 |
| FINAL | sealed letter | `--emb` | 7 |

### 8.3 Window chrome

One frame, used by the desktop window and by every document: title bar with horizontal rules,
a close box at the left, a drag texture, a 1 px border, no rounding, no shadow.

---

## 9. Desktop and mobile

**One source. One breakpoint: `min-width: 900px`.** Everything below is one column.

| | mobile | desktop |
|---|---|---|
| machine geometry | procedural, **23,506 tris, ~50 KB** | CC0 mesh, **61,081 tris, 505 KB** |
| approach to the machine | scroll drives the camera | same, longer travel |
| orbit | one finger drag | drag; wheel zooms |
| hit target | the whole machine | the screen, with a hover halo |
| desktop layer | full frame | a window inside the CRT |
| icon grid | 2 columns | 4 columns |
| documents | full frame | windowed, 960 px max |

The mobile machine is not a compromise made for this plan — **it already exists**, built and
verified, and it is reachable today at `?geo=proc`.

---

## 10. Copy

Every string the shell shows lives in `src/content/copy.json`. Not one string is typed into a
template. This is what makes a copy pass possible without touching code.

Strings needed: the page-1 map legend and the four company stops; page 3's points; the floating
caption over the machine; the desktop window title (`ORAN CARMON`); the seven icon labels; the
close/back affordances; the "read" state; empty and error states.

---

## 11. Migrating the seven documents

Mechanical, one document at a time, verified before moving to the next.

### 11.1 Per document

1. Cut `<section id="…">…</section>` from `m/index.html` into `src/doc/<id>.html`.
2. Move the rules scoped to `#<id>` into `src/doc/<id>.css` — 545 rules across all seven.
3. Build.
4. **Verify by pixel diff** (§11.4). The result must be **identical**, not merely close.
5. **Then, and only then, reconcile the copy** against the root build (§1.6) as a separate,
   visible change — with its own pixel diff, whose differences are all intended.
6. Only then start the next document.

**Steps 4 and 5 are never combined, and the order is not negotiable.** A cut that also edits the
copy produces a diff full of intended changes, and an unintended one hides among them
perfectly. Cutting proves the machinery; reconciling changes the product. One diff must contain
exactly one kind of change or neither diff means anything.

Order: `oasis` (3 rules) → `eventer` (4) → `xtix` (16) → `leadership` (18) → `tech` (36) →
`medcoin` (37) → `final` (174). Strictly easiest first, so the pipeline is proven on a cheap
case before it meets the expensive one.

### 11.2 The prologue sections

| section | fate |
|---|---|
| `hero` | **replaced** by the isometric world map |
| `statement` | **kept exactly**, lifted whole |
| `philosophy` | **redesigned** as a folder, same content |
| `files` | **replaced** by the desktop; three things survive it, listed in §14.1 |

### 11.3 The 21 cross-section rules

Each is decided individually and recorded in a table in the migration log. Only two outcomes
are allowed: **duplicate into each document that needs it**, or **promote to the kit**. A rule
may not stay half in one place and half in another.

### 11.4 Verification by pixel diff

The strongest check available, and the one this project has earned the hard way:

1. Screenshot today's `m/index.html` at 390×844 and 1440×900, full length.
2. Screenshot the rebuilt page at the same sizes.
3. Diff. **Any pixel that moved must be explained**, or the migration is wrong.

This runs per document, not once at the end.

### 11.5 The freeze harness — and the bug it exposes

A pixel diff of this page as it stands would be noise, not evidence: 32 `requestAnimationFrame`
loops and 34 keyframe animations mean no two screenshots of it are ever identical. So the diff
runs against a frozen page — all animation paused, all transitions off, all reveals forced on.

Writing that harness surfaced a defect the specification would otherwise have shipped.

**83 elements start invisible.** `.rv { opacity: 0; transform: translateY(26px) }`, and they are
revealed by an `IntersectionObserver` adding `.on` as the reader scrolls past. That works when
every section is on one long page. It does **not** work for a document mounted on demand: open
`#/doc/xtix` directly and the observer has never run over that markup, so the document mounts
and renders **blank**.

The fix belongs in the entry action, not in a patch later: on mounting a document, the reveal
pass runs over the new fragment — immediately for anything already in view, and by observer for
the rest. The same code serves the harness and the product, which is the only reason to trust
that the thing being tested is the thing being shipped.

---

## 12. What the build checks, every time

The build refuses to write output if any of these fail:

1. Every `id` in `manifest.json` appears exactly once in the output.
2. No CSS rule references a section id that is not in the manifest.
3. No `<a href>` or asset URL points outside the origin, except the LinkedIn whitelist entry.
4. Every URL in `router.js` resolves to a state — **one way only**. A state is not required to
   have a URL: Oran ruled that FINAL has no address, because the reader is meant to reach it by
   working through the file rather than by being handed a link. An earlier version of this check
   demanded both directions and would have refused to build the design he asked for.
5. Every string rendered by the shell exists in `copy.json`; no literal text in templates.
6. Every sprite named in a scene exists in `sprites.json`.
7. Budgets (§13) are met.
8. `index.html` at the repo root has the same md5 before and after.
9. Building twice produces identical bytes.

---

## 13. Budgets

Numbers, not intentions. Check 7 enforces them.

| | budget | today |
|---|---|---|
| first paint (`index.html` + `app.css` + `app.js`) | **≤ 200 KB** | 688 KB |
| fonts, shell face | **0 KB** — the 5×7 face is drawn in code | 0 KB ✓ |
| fonts, document faces | **≤ 300 KB inlined** — see the ruling below | 299.7 KB ✓ |
| sprite sheet | ~30 KB | — |
| machine, mobile | ≤ 60 KB | 23,506 tris — measured, §11 |
| machine, desktop | ≤ 520 KB | 61,081 tris — measured, §11 |
| any one document | ≤ 60 KB | largest is XTIX at 15.8 KB ✓ |
| sound | **0 KB** | 0 KB ✓ — the layer is removed entirely, not merely unsampled |
| time to first meaningful paint, 4G | ≤ 2.0 s | not measured |

**The font budget was rewritten, and the reason is the interesting part.** It used to read
"shell faces only, ~5 KB inlined" against a measured 299 KB, which made the table permanently
red for a reason that was never a defect. That line assumed the shell and the documents would
be typeset in the same faces. They are not: the shell is set in a 5×7 bitmap drawn in code and
costs nothing, and the five web faces belong entirely to the documents, whose typography Oran
ruled untouched. Two budgets, not one.

**And serving those faces as files was considered and refused.** Measured, base64 inflates the
five faces from 224.8 KB to 299.7 KB, so files would save **75 KB** and would cache between
visits. Both true. It was refused because the page already shows a loading screen, so that
weight is spent behind a screen built to absorb it, and because the alternative introduces a
failure this page has never had: six files that must ship in sync, where one missing font
leaves the page working but wrong. A single file cannot half-arrive. The saving is real and
invisible; the risk is small and permanent, so it is not taken.

**Two of these budgets were wrong, and how they were wrong is worth keeping.** An earlier
version of this table asserted ≤ 240 KB for fonts and ≤ 120 KB for the sprite sheet. Neither
figure had a source — they were written because they sounded like reasonable ceilings.
Measurement says they do not bind at all: the two shell faces subset to **3,768 B raw, 5,024 B
inlined**, and a 16-colour 1024 × 1024 isometric sheet comes to **29 KB**. Roughly 49× headroom
on type and 4× on sprites.

It matters because a ceiling nobody established was about to decide a real question: the
typeface recommendation turned partly on which face was cheaper, between options four kilobytes
apart, on a page that already carries seven hundred. **These decisions get spent on fidelity,
not on bytes.** The first-paint budget stays, because it was derived from a measurement (§1.4)
rather than chosen.

**Where the 200 KB goes.** Measured, not hoped: the kit CSS is 61 KB (§1.4), and the shell JS is
what remains of today's 143 KB once the documents take their own (§1.5), plus the router, the
isometric renderer, the machine and the desktop, which do not exist yet. Shipping today's
totals unchanged — 114 KB of CSS and 143 KB of JS — comes to **258 KB and misses the budget**.
Deleting the 26 KB of dead rules and moving the documents' 27 KB out of the kit is what makes
the number reachable, which is why §1.4 is in this document at all.

---

## 14. Decisions

### 14.1 Settled

**No skip.** There is no "jump to the work" affordance anywhere. The prologue is the product;
a reader who wants the machine scrolls to it. A deep link still lands directly, because a link
is someone else's decision about where a reader should start, not the reader's own shortcut.

**Sound is in**, and it is designed with everything else rather than added at the end (§14.3).

**`files` is replaced by the desktop — and it turns out to be the same idea already.** What
page 4 shows today is a rotating archive drawer holding four file cards, dragged to turn and
clicked to open, under the label `ARCHIVE DRAWER C-01` and the hint `DRAG TO TURN · CLICK A
FILE`. That is the desktop's job, done as a drawer instead of as a Macintosh. So the drawer
goes, and three things survive it:

| survives | why |
|---|---|
| the four descriptors — `XTIX — BUILT FROM ZERO`, `OASIS — LEADERSHIP`, `EVENTER — ALIGNMENT`, `MEDCOIN — FOUNDER` | earned copy; they become the icon subtitles |
| the framing `EXECUTIVE PORTFOLIO · 04 DOSSIERS · 2018–2026` | belongs on the desktop window's title bar, with 04 becoming 07 |
| the affordance line pattern | `DRAG TO TURN · CLICK A FILE` is the shape the floating caption over the machine needs |

One structural consequence to be explicit about: **the drawer holds four, the desktop holds
seven.** Today `leadership`, `tech` and `final` are not in the drawer at all — they arrive by
continuing to scroll past the case files. On the desktop they become icons like the rest, which
is a promotion, and §8.2 gives them their own icon shapes so they do not pretend to be cases.

### 14.2 Still to decide — the kit

These are the phase C decisions. Each needs a visual before it is settled, and each is listed
with what is already known, so the choice is made against facts rather than in the abstract.

**Fonts.** Five faces exist today, 222 KB: Inter 47, JetBrains Mono 39, Fraunces 35 and 79,
Special Elite 22. The shell needs a bitmap face for the 1984 chrome that none of the five
provides. To decide: which face; whether it is one weight or two; whether both Fraunces cuts
are still earning their 114 KB; and which of the five the shell itself needs, since a document
can load its own. A pixel face subsets very small — the glyphs are simple — so this probably
costs under 15 KB rather than another 47.

**Colours.** The palette in §8.1 is fixed and closed. What is open is the *working sub-palette*
for the isometric art: those games ran on 16 to 32 colours, and the discipline is what makes
them look like themselves. To decide: how many stops, how the four project colours appear on
the map, and whether the 1984 world keeps the charcoal ground or has a ground of its own.

**Sound.** §14.3.

**Motion.** `--ease: cubic-bezier(.22,.61,.2,1)` already exists and stays. To decide: the
duration of the flight into the CRT, whether icons animate on open, and what
`prefers-reduced-motion` turns off — which must include the camera flight, or the setting is
decorative.

**Cursor.** An old arrow inside the machine, the system cursor outside it, or one throughout.

**Art scale.** Sprites are authored at 1× against the 64 × 32 tile (§7) and displayed at 1× on
mobile and 2× on desktop. To confirm: whether any scene needs 3×, because that decides the
sheet's resolution and it cannot be changed later without redrawing.

**Reading state.** Whether an opened document is marked as read on the desktop, and what that
looks like in an idiom that had no such concept.

**The two sites — settled.** The link is not published anywhere binding, so the choice was made
on the files rather than on the URL.

| | decision | why |
|---|---|---|
| **base** | **`m/index.html`** | newer by 11 days (20 Aug vs 9 Aug); carries the more developed design — the rotating drawer, the hero rotator, the archive stamps; and holds more unique document copy (30 blocks against 22) |
| **published at** | **`/portfolio/m/`** | chosen; the link is not published anywhere binding, and staying put means no URL ever changes hands |
| **the old root build** | **harvested, then reduced to a redirect** | it holds 48 blocks the mobile build does not (§1.6). Every one is decided before its section is frozen, and only then does the file go |

The migration runs **once**, not twice, and ends with one source at one URL.

**The root is not simply left alone.** `/portfolio/` is the shorter address and the one a person
would guess, and today it serves a 945 KB build that is two design generations stale. Leaving it
there recreates the exact drift this section exists to end. So, **in this order**:

1. every block in §1.6 that lives only in the root is decided and harvested into its document;
2. `index.html` is replaced by a redirect to `/m/`, three lines long;
3. `src_site.html` moves to `build/_legacy/` as the record of what it was.

Step 2 does not happen before step 1 is complete, for all eleven sections. Until then the root
stays exactly as it is, and the guard in `build_mobile.py` that refuses to touch it — written to
keep two tracks apart — now protects the archive instead. It stays.

### 14.3 Sound — what is already determined by the medium

Three constraints exist before any taste is applied, and they settle more than they look like
they do.

**Synthesise, do not sample.** These machines made square waves with short envelopes. Web Audio
produces exactly that for **zero bytes**, stays tunable to the last millisecond, and cannot
become a licensing question. Samples would cost 50–200 KB and break the budget in §13 for a
worse result.

**The Macintosh startup chime is Apple's.** We make our own. This is not a grey area and it is
cheap to respect: a different interval, a different envelope.

**A browser will not make a sound before the reader has clicked something.** The prologue is
scroll-only, so no sound is possible in it — and the first click in the whole product is the
one on the machine. That is not an obstacle to work around. **The machine makes the first
sound, because the reader turned it on.** The silence before it is now deliberate.

To decide: which events sound at all (turn-on, disk insert, window open, window close, icon
select, the drive seeking); the mute control's placement in the chrome; and whether sound
starts on or off. The recommendation is **on**, because it can only ever follow a deliberate
click on a machine, with the mute always visible and its state remembered.

---

## 15. Build order

Each phase ends with something that can be looked at and judged.

| phase | deliverable | kind |
|---|---|---|
| **A** | this document, agreed | decision |
| **B** | `src/` tree, `build.py`, root and `m/` collapsed to one source, one section migrated (`oasis`) and pixel-verified, then its copy reconciled | engineering |
| **C** | the 1984 kit — palette, sub-palette, bitmap face, tiles, icons, chrome, cursor, and the sound kit, on one page | **visual + audible** |
| **D** | page 1, the world map — 2–3 directions | **visual** |
| **E** | page 3 as a folder | **visual** |
| **F** | page 4: approach, floating caption, the click | **live prototype** |
| **G** | the desktop inside the CRT | visual, then live |
| **H** | the remaining six documents migrated and reconciled | engineering |
| **H2** | the root harvested to the last block, then reduced to a redirect to `/m/` | engineering |
| **I** | copy pass across `copy.json` | writing |
| **J** | mobile, budgets, the checks in §12 | verification |

**B before C** is deliberate. If the plumbing is not proven on the cheapest document first, we
will discover its problems while also arguing about art direction, and it will be impossible to
tell which of the two is going wrong.
