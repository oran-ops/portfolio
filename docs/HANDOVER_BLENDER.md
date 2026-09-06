# Handover — building the world map in Blender

Everything a fresh session needs to take over the map. Read this first, in full, before
touching anything. It exists because the previous attempt burned a very large number of rounds
on mistakes that are all written down below, and repeating any of them is avoidable.

---

## 1. What is being built

Page 1 of Oran Carmon's executive portfolio at **https://oran-ops.github.io/portfolio/m/** is
an isometric world map. One road runs through a green country — **British Columbia** — and
wherever it arrives the forest becomes a small metropolis. There are four of them, in the
portfolio's own scroll order:

| | place | what it is |
|---|---|---|
| START → | **XTIX** | 30 % under construction, 70 % standing. Skyscrapers, luxury restaurants, new cars, people in suits, ordered roads, tall cranes, contractors, excavations, building skeletons. *"Raised from nothing, fast — and still it came up tall, luxurious and very strong."* Not Dubai, not NY, not Tokyo. |
| | **OASIS** | A finished, lived-in residential neighbourhood. Private houses with yards, fences and new cars; low blocks with parking; children playing; public playgrounds; and a commercial centre ≥15 % of the mini-city — two floors of retail under two of office, never tall. |
| | **EVENTER** | The LA-style interchange (a reference, not a copy). A traffic jam packed with cars — **every car is a customer he had**. But not only an interchange: buildings, people and businesses around it so it is the centre of a city. |
| → END | **MEDCOIN** | A business district like the Ramat Gan exchange / Twin Towers. Edges: low industry, factories, tractors, forklifts, material yards, smoke, concrete, coal, stone, marble, timber, metal, manual workers. Centre: skyscrapers, offices, **people in suits**, law and finance, matching restaurants. |

**Proportions (approved):** whole map = 100. The four mini-cities together = 60 % (15 % each).
Green country = 40 %. The cities are arranged as a **cluster**, not on one axis.

**Interaction:** the mouse controls the map on all axes; there is nowhere to travel beyond it;
it is not clickable except to zoom into a workplace, and from there the reader scrolls on into
the document.

**Topography:** roughly square, mostly flat, small hills, rises and falls — **no cuts or
steps**. START sits immediately before XTIX; the road runs on to END immediately after MEDCOIN.

The full brief is `docs/MAP_VISION.md`. The analysis of what an isometric city is actually made
of is `docs/MAP_ANALYSIS.md`. Read both.

---

## 2. The decision that has been taken

**Path B — pre-rendered, not real-time.**

The scene is built in Blender at whatever quality it needs, rendered **offline**, and the web
page serves images with clickable regions and zoom levels. Fixed camera angles replace free
orbit — which Oran has accepted, and which the existing page already half-does with its
VIEW 1–4 buttons.

Why, in one measurement: the real-time build reached **1,430,232 triangles**, which is the
ceiling a browser can carry. The reference images Oran keeps sending are *renders*. Matching a
render with a real-time engine is the mismatch that cost most of the previous rounds.

**This makes the embed simpler, not harder.** Today the page carries a 6 MB base64 geometry
blob, shaders and a WebGL viewer. Path B carries a handful of WebP images and a small hotspot
layer. Fewer moving parts, smaller page, and the same zero-external-request guarantee.

---

## 3. Hard constraints — these are not negotiable

- **`portfolio-repo/index.html` must never be touched by a build.** It is the live site root.
- The map publishes at **`/portfolio/m/`**.
- **Zero external requests** from the published page, except one LinkedIn link. No CDNs, no
  fonts, no analytics. Everything inlined.
- **The repo is not committed or pushed** without Oran saying so — pushing publishes to the
  live site.
- Downloading anything needs his explicit permission each time.
- **Ask which file type he wants before building a deliverable.** Finished documents are PDFs.
- Deliverables live in `Desktop\Oran_Personal_Brand`, never loose on the Desktop.

---

## 4. Where everything is

```
C:\Users\Alex\Desktop\Oran_Personal_Brand\
├─ portfolio-repo\               the site. index.html at root = LIVE, do not touch
│  ├─ m\index.html               where the map publishes
│  └─ docs\                      MAP_VISION.md, MAP_ANALYSIS.md, DECISIONS.md, BUGLOG.md,
│                                WORLD_STATE.md, and this file
└─ world-build\
   ├─ kits\all\                  4,356 objects across 43 kits, flat, with index.json
   │                             (Kenney kits + the imported lowpoly-city pack)
   ├─ packs\low_poly_city\       the Sketchfab glTF pack, CC-BY-4.0, credit required
   ├─ refs\                      67 images — every reference Oran has ever sent, recovered
   │                             from the session transcript. TARGET_iconscout.png is THE
   │                             target he chose. _vision_msg.txt is the brief in his words.
   ├─ shots\                     every render made. JUDGE.png is the side-by-side panel.
   └─ tools\                     34 Python modules (see below)
```

### The tools that still matter

| file | what it does |
|---|---|
| `refcard.py` | measures a render against the target image: colour, saturation, lightness, and the mix of grass / road / building. Targets are re-measured from the image every run, never hard-coded. |
| `gap.py` | the harder measurements — detail density, hard edges, local contrast, colour count, structure-vs-noise — **and the control panel** that runs the same code over every professional reference. |
| `audit.py` | 14 rules applied to every placed instance: in a road, in water, in a wall, off the tile, floating, sunk, intersecting, facing away from its street, foreign object, scale outlier, empty cell. |
| `roadmap.py` | draws the road network in plan and proves it is a network: every crossing has a junction, nothing is orphaned, nothing dead-ends in a field. |
| `street.py` | the street cross-section. Lane, bay, kerb, walk, furniture, building line — all named, all derived from one definition. |
| `import_gltf.py` | turns a glTF/GLB scene into a usable kit: scale calibrated by measurement, yaw axis-aligned, textures flattened to per-face colour. |
| `sheet.py` | renders a contact sheet of any model list, so a pool is chosen by sight. |
| `decode.py` | turns a reference image into numbers — palette by role, surface mix, widths. |
| `oasis_build.py` | the OASIS generator. 1,104 lines. **Read its comments — every one records a real bug.** |

---

## 5. What is already true, measured

The last real-time build of OASIS:

| | |
|---|---|
| elements placed | 3,756 |
| placement faults | **14 — 0.4 %** |
| road network | **72 of 72 crossings junctioned, 0 seams, 0 dead ends, 1 connected network** |
| colour / surface mix vs target | **7 of 7 inside range** |
| detail density vs professional references | **0.546 against a mean of 0.408 — above them** |

**Read that last row carefully.** On every dimension anyone has managed to measure, the build
is inside or above the professional range — and Oran still judges it short. The remaining gap
is compositional and aesthetic, and no instrument here detects it. **Do not invent a fourth
theory about why.** Oran leads the design decisions from here; implement what he directs and
verify with the tools above before reporting anything as done.

---

## 6. Mistakes already made — do not repeat these

Each of these cost real time. They are in `docs/BUGLOG.md` in more detail.

**Measurement**
- An instrument that compares a picture on a dark page with a picture on a white page reports
  the page, not the picture. This happened **twice** (`refcard`, then `gap`).
- Measuring density over a padded square instead of over the tile itself made the build look
  3× less detailed than it is, and nearly sent the whole project chasing detail it already has.
- Two instruments using different saturation definitions (HSV vs HSL) disagreed by six points
  about the same image.
- Hard-coded targets go stale the moment the definition behind them changes. Re-measure.
- **Always run a control.** Measuring the build against the target proves nothing until the
  same code is run over references whose quality is already agreed.

**Geometry**
- `s = cross(f, up)` was written negated, which rolled the camera 180°. Every render for days
  was upside down, and two later "fixes" were compensations for it.
- Reading global extents (`T.W`, `T.NX`) inside a routine that draws a *cell* put its roads 42
  units off and its junction plates clean off the tile. Pass the extent in.
- `face(dx, dz)` is `atan2(-dx, dz)`. Hand-rolled `atan2(dx, dz)` mirrors the rotation — it laid
  a roller-coaster crosswise over its own circuit.
- A rigid structure has ONE absolute height. Draping coaster track on the terrain gave a heap
  of disconnected ramps.
- Modular kit pieces carry their own internal rise; a "hill" enters at 0 and leaves 5.6 m up.
  Laid end to end on flat ground they do not connect.

**Placement**
- Check the rule at placement time AND sweep once at the end. A prop laid down before the
  building that later covers it passes when placed and is wrong afterwards.
- Claim radius must be the half-*width*, not 0.82 of the half-*diagonal* — the latter bulges
  past the corners and made 1,198 buildings refuse each other on streets they fitted on.
- Street spacing is arithmetic, not taste: `half_road + pavement + setback + half_building`,
  doubled. Guessing it put 449 buildings inside carriageways.
- A model's kit name means nothing. `hedge` ships in a fantasy kit, `satelliteDish` in a space
  kit. Judge by the model, or better, by measurement.
- Four "trees" were untextured grey slabs because a fallback dropped the `veg` flag. Look at
  what you are placing — `sheet.py` exists for this.

**Colour**
- The shader multiplies flat ground by ~1.47 before it reaches the screen, and that carries
  HSL lightness past 0.5 where the saturation denominator flips. Author in screen space and
  divide back through the measured gain (`calibrate.py`).
- **78 % of the colour in the target is roof, not traffic.** Walls are neutral — saturation
  0.01–0.03. Colour lives on roofs, cars and signs.

---

## 7. Assets

- 43 kits, 4,356 objects, already flat and indexed at `world-build/kits/all/index.json`.
- The `lowpoly-city` pack is **CC-BY-4.0** — golukumar, via Sketchfab. Credit is required
  wherever the work is published, and Oran has approved a credit line.
- `gaps.py` lists what the three unbuilt worlds still need. Missing entirely: excavator,
  hi-vis contractors, luxury restaurant, people in suits, flyover, crash barrier, silo,
  forklift. Thin: tower crane, building skeleton, scaffolding, motorway ramp, factory.
- Blender's connector brings **Poly Haven** with it — free, professional, no purchase.
- Nothing has been bought. Meshy, Synty, Spline, KitBash3D and IconScout were all researched;
  see the session for the reasoning. Meshy has an official MCP server if per-object generation
  is ever wanted.

---

## 8. First steps in the new session

1. Confirm the Blender connector is live — Blender running, MCP addon enabled, server started
   on port 9876. `execute_blender_code` returning `bpy.app.version_string` is the check.
2. Read `docs/MAP_VISION.md` and `docs/MAP_ANALYSIS.md`.
3. Look at `world-build/refs/TARGET_iconscout.png` — the agreed target — and `shots/JUDGE.png`,
   which puts it beside the professional references and the last real-time build.
4. **Wait for Oran to direct.** He is leading the design step by step, by his own decision and
   for good reason. Build what he asks, measure it, show him, and do not run ahead.

---

## MEDCOIN — built and verified, 2026-08-26

`world-build/medcoin.blend`. **4,673 objects, ~3.4 M triangles.** Every stage is generated
by `world-build/tools/medcoin_gen.py`; nothing was placed by hand.

### To rebuild the whole city from scratch

```python
import bpy, io
P = "C:/Users/Alex/Desktop/Oran_Personal_Brand/world-build/tools/medcoin_gen.py"
g = {"__name__": "medgen", "__file__": P}
exec(compile(io.open(P, encoding="utf-8").read(), P, "exec"), g)
g["fix_missing_textures"](); g["degreen"](); g["fix_foliage"]()
R = g["build_all"]()          # stages 0-9, deterministic
T = g["verify_all"](R)        # every acceptance test
```

`build_all()` clears and regenerates everything from seeds in `medcoin_gen.SEEDS`, so the
same seeds always give the same city. It needs the prototype collections to exist already —
`LIB`, `LIBPROP`, `LIBVEH`, `LIBLIFE`, `LIBROOF`. Those are imported once from the JSON
libraries beside the script and then live in the .blend.

### The libraries

| file | contents |
|---|---|
| `tools/lib_buildings.json` | 83 building models, bucketed CORE / OFFICE / CIVIC / BELT |
| `tools/lib_props.json` | 52 industrial props in 15 categories |
| `tools/lib_vehicles.json` | 38 vehicles |
| `tools/lib_life.json` | 30 people + 7 furniture categories |
| `tools/lib_roof.json` | 10 rooftop items |

Each row carries a **per-file scale** and every model was checked against a real-world size
range before being admitted. Do not add a model without doing the same — see BUGLOG.

### Three things that will bite a fresh session

1. **A kit's scale is not uniform.** `building-148` is authored in metres among Kenney
   models authored in 1u = 8 m. `retro-urban-kit` pallets need 1.2 while its lamps need 4.0.
   Measure the bbox and check it against a known real size; never infer from the kit.
2. **A missing texture renders magenta**, so it looks like a colour choice, not a broken
   file. Run `fix_missing_textures()` after any import and check `bpy.data.images`.
3. **Donor models carry green.** `nature-kit` rocks and trees use a material named `grass`;
   several lowpoly-city buildings have green facades. `degreen()` repaints them; MEDCOIN's
   rule is zero green inside the square.

### Still open

**The world merge — deliberately not run.** `tools/world_merge.py` is the mechanism and it
is ready, but two things must be true first and neither is:

1. **All four cities must exist.** The road is one continuous route through
   XTIX -> OASIS -> EVENTER -> MEDCOIN. Measured: OASIS's main road runs **west to east**
   across its plate (x 0 to 700); MEDCOIN's enters from the **south** and leaves east. They
   do not chain. Whichever way MEDCOIN's approach is turned, it is fixed against a layout
   that changes the moment EVENTER is placed between them -- so laying it now means laying
   it twice.
2. **Memory.** OASIS is 12,631 objects, MEDCOIN 5,111. At the time of writing the machine
   had **1.29 GB available**, which is the condition that previously took Blender to
   unresponsive. Check available memory (not 'free') before attempting it.

Both cities are also authored at the **same coordinates** -- square 372 x 372 at (164, 139)
on a 700 x 650 plate -- so a merge is a layout operation, not a copy. `world_merge.py`
handles the offsetting, skips prototype collections, and drops each city's own camera, sun
and terrain in favour of the world's.

**One conflict to settle first:** OASIS is lit at 82 degrees and MEDCOIN at 75. One world,
one sun. See MEDCOIN_PLAN section 8.

Everything else on the old list is now done: bus stops, benches and planters are placed
(8 / 46 / 54), and office signage is built (170 signs, plan 2c fault 4).
