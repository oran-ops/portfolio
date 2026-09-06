# THE MAP — the brief, in Oran's words

Every note given so far, in one place, so nothing is lost between rounds and so we can plan
against it instead of against my memory of it. Nothing here is my opinion; §6 is.

---

## 1. What the map is

Page 1 of the portfolio document. An old-game world map with a **PATH through four companies**,
each with an arrow above it pointing up to its label (`XTIX — BUILT FROM ZERO`), and a START
and an END. Clicking a name zooms into that place to see it in full detail.

**The path order is the portfolio's scroll order** — verified against `m/index.html`:
`FILE 01 XTIX → FILE 02 OASIS → FILE 03 EVENTER → FILE 04 MEDCOIN`.

## 2. The rejections, and what each one was really about

| Round | Verdict | The real note |
|---|---|---|
| Pixel-tile demo | "לא הכיוון" | No creativity; a path that isn't a path, just a coloured line; no coherence between the old design and the new |
| First Kenney world | "ביצוע חלש מאוד" | **"לא תכננת, לא חשבת, לא אפיינת, סתם זרקת אלמנטים"** — trees random, buildings unrelated, steps that meant nothing, a green that looked like vomit |
| v4 (naturalistic) | "הכיוון שלנו פה לא נכון" | **Built like Heroes of Might & Magic.** Forgot the other pages. No coherence between modern and old, in colour and in the whole vision. And the map is inverted. |

## 3. Standing requirements

- **Colours** matte and realistic, varied per element type — buildings, people, vegetation,
  paths, rivers, tools, traffic lights, pavements, equipment, structures. Everything designed.
- **Terrain** no steps, no cliffs. Slopes, wadis, valleys, hills, mountains. Real shading, real
  topography.
- **Each place is its own mini-world**, built from that case file's own information, dense and
  detailed; click the name to zoom in and read the smallest detail.
- **Logic in everything** — buildings face the square or the road, never a tree; trees grow in
  groves; flowers in fields; people in groups, in cars, on pavements, in shops; cars on roads;
  correct size ratios; sun and shadow consistent.
- **Case labels** slightly larger.
- **The path** more prominent, wider, stronger — plus secondary roads and tracks linking places
  to a forest, a cabin, wherever.
- **START and END** markers, consistent with the case axis.
- **Many Kenney kits**, many element types, creative.
- The level must match the references from the start: *"אם תיתן לי פחות מההתחלה אני כל הזמן
  אחזור ואבקש לשדרג."*

## 4. What was wrong with v4 — his words

1. **The wrong genre.** It went to a game world (Heroes-like), not to what this document is.
2. **It forgot the rest of the pages.** The map has to belong to the same object as page 2
   (the dissonance), page 3 (the folder), page 4 (the machine) and the 1984 desktop behind it.
3. **No coherence between the modern and the old** — in colour, and in the whole vision.
4. **The map is inverted.**

## 5. The references he gave

| Reference | What it establishes |
|---|---|
| **icograms.com** | **2:1 true isometric projection.** Flat vector, consistent icon styling, 5,572 icons, SVG/PNG export. A *designed diagram*, not a simulated landscape. No API — it is a manual tool, so it is a style reference, not a pipeline. |
| **things.inc/rooms** | True 2:1 isometric diorama cells that tessellate. Chunky voxel craft, crisp edges, **each cell its own deliberate flat palette**, dense readable micro-detail. No fog, no atmospheric perspective, no naturalistic light. |
| dribbble `3d-isometric-map` | The genre at large |
| behance `isometric map` | The genre at large |
| lapa.ninja third-dimension-studio | Presentation craft |

## 6. What I read from this — for confirmation, not assumption

The references share four things that v4 does not have:

1. **True isometric, not perspective.** icograms is explicit: 2:1. Rooms is the same. v4 uses a
   perspective camera, which is why it reads as a landscape you fly over rather than a map you
   look at.
2. **Flat, deliberate colour** — chosen per area, not sampled from a photograph of nature. v4
   grades every model toward realistic greens and browns, which is exactly the "Heroes" read.
3. **No atmosphere.** No fog, no aerial perspective, no soft shadows dissolving detail. Crisp.
4. **Density of readable micro-detail** rather than density of naturalistic scatter.

And the constraint that outranks all of them, from the document's own contract:
**the shell is 1984, the content is 2026.** The map is content — so it should be modern and
crisp — but it has to sit inside a 1984 Macintosh without either half looking borrowed.

## 7. What is worth keeping from v4

Not to save effort — because these are answers to notes in §3 that still stand:

- The **placement rules** (buildings face something, people in groups, trees in groves,
  vehicles on roads, nothing floating) and the **acceptance checker** that proves they hold.
- The **measured per-kit scale table** — 43 kits calibrated against known real sizes.
- The **43-kit, 4,236-model library**, already downloaded and indexed.
- The **headless render pipeline**, which is what makes iterating possible at all.
- The four **authored mini-world layouts** — the content, not the treatment.

What goes: the perspective camera, the naturalistic colour grade, the fog, the soft shadows,
the fractal terrain, and the general ambition to look like a place rather than like a document.
