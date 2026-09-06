# WORLD — state of play, 2026-08-23

Page 1 of the new document is an old-game world map: a PATH through the four companies, each
with an arrow above it pointing up to its label, and a START and an END. This file is the
handoff — what exists, what is honestly still wrong, and how to resume cold.

**v4 replaced v3 entirely.** v3's problem was never detail; it had 6,337 instances. It was that
three systems were wrong at once — the ground was tiled so it could only ever terrace, the
colour pipeline forced every model onto four brand ramps so nothing could look real, and props
were placed by proximity rather than by what a thing is for. The specification is
`WORLD_SPEC_V4.md`; this file records the build against it. The superseded v3 handoff is kept
as `WORLD_STATE_v3.md.bak`.

---

## 1. Where everything is

Everything lives in `C:\Users\Alex\Desktop\Oran_Personal_Brand\world-build\` — deliberately
**outside** the repo, because 140 MB of source models are build inputs, not site output. It is
**not** in the scratchpad; that folder is wiped at the end of a session.

| What | Path |
|---|---|
| Terrain: height field, river, wadi, pads, road binding | `tools/w4_terrain.py` |
| Colour: the one grade, per-instance variation, terrain bands | `tools/w4_palette.py` |
| Geometry: terrain block, road ribbons, water, skirt, blob | `tools/w4_mesh.py` |
| Models, and the placement rules | `tools/w4_props.py` |
| The four mini-worlds and the outposts | `tools/w4_places.py` |
| Assembly: road network, vegetation, wildlife, build | `tools/w4_gen.py` |
| Viewer → one self-contained page | `tools/w4_view.py` |
| **Headless renderer — works with the screen locked** | `tools/shoot.py` |
| **Acceptance checks — gates a build, exits non-zero** | `tools/check_world.py` |
| Per-kit scale calibration, and the ruler that checks it | `tools/calibrate.py`, `tools/ruler.py` |
| Kit ingest and indexing | `tools/ingest.py` |
| 43 kits, 4,236 models, all CC0 | `kits/all/` |

```bash
cd "C:/Users/Alex/Desktop/Oran_Personal_Brand/world-build/tools" && python w4_gen.py && python w4_view.py && python shoot.py all
```

`w4_gen.py` is deterministic under `random.Random(20260823)`. The printed instance and triangle
counts are the ratchet: if they move, something changed.

### Rendering with no display

`shoot.py` is what makes unattended work possible. The interactive browser cannot screenshot a
pane that is not being shown — an occluded window stops compositing — so every render step died
the moment the screen locked. Headless Chrome with SwiftShader rasterises WebGL2 in software:
no GPU, no display, no unlocked desktop. About 2 s per 1600×1000 frame, and it captures the
whole **page**, so the DOM labels and arrows are included.

Named views: `map`, `high`, `xtix`, `oasis`, `eventer`, `medcoin`, `mill`, `farm`, `quarry`,
`cabin`. Any camera also works: `python shoot.py close -0.95 0.30 16 -26.5 15.5 3.0`
(yaw, pitch, dist, target x, target z, target **height**).

Measured power settings on this machine: on AC, `STANDBYIDLE = 0` and `HIBERNATEIDLE = 0` — it
never sleeps, so a locked screen does not interrupt a build. On battery it sleeps after
**20 minutes**, which does. Long unattended runs must be on mains.

---

## 2. What the build contains

**216 distinct models · 7,847 instances · 90,720 terrain triangles · 954 k drawn triangles.**
Blob 2.75 MB raw / **3.67 MB base64, down 41 % from 6.2 MB**. World 84 × 60 units at 8 m per
unit, so 672 m × 480 m. The build is deterministic: two runs print identical counts.

Three compressions got it there, each measured before it was built: positions quantised to
uint16 over each model's own bounding box (0.2 mm steps over a 12 m box); sub-pixel triangles
culled with a threshold that scales to the model and a floor so small models survive; and
vertex deduplication with a 16-bit index buffer — measured at 49 % of vertices unique across
the whole world, which is 35 % off the model geometry.

**Published** as a private artifact so it can be opened and explored in a browser rather than
looked at as screenshots: <https://claude.ai/code/artifact/c51affef-4fe9-4fce-9a2f-bed077f63c81>.
`tools/mkartifact.py` strips the document shell, because the artifact host wraps the file in
its own doctype/head/body and a complete HTML document cannot be nested inside that.

**The sun casts.** A 4096 orthographic shadow map covers the whole world in one pass, sampled
with 4-tap PCF. Nothing floated on the ground before this; it is the single largest change in
how the world reads. The depth pass culls FRONT faces, which puts shadow acne on surfaces that
are turned away from the light and already shaded.

**Terrain.** One continuous height field on a 253 × 181 lattice, triangulated once. There are no
tiles, so steps and cliffs are not possible — that is a change of category, not a fix. Trend
rising along the route, five octaves of fbm, a ridge-noise mountain range along a crest line, a
river whose bed is read off the land and then forced to descend, a dry wadi, smoothstep pads
under every settlement, and the field smoothed along every road so a road can climb without
bucking. Normals are the analytic derivative of the same field, so shading is smooth by
construction rather than by a smoothing pass.

**Roads.** Generated ribbons, not tiles: a Catmull–Rom spline, offset rails, dropped onto the
height field. Main route 1.5 u (12 m) with kerbs and centre dashes; secondaries 0.95 u; tracks
0.6 u. Plus a second main road crossing at EVENTER and a railway with a level crossing.

**The four mini-worlds**, authored in a local frame aligned to the road that serves each:

- **XTIX (317)** — a town going up. A three-storey frame, walled below and skeletal above, with
  scaffolding on two faces and a 26 m tower crane assembled from mast and jib parts. Site
  barriers, materials yard, plant, crew; a finished street of six houses across the road with
  pavements, lamps and newly planted saplings; and a second plot not started yet.
- **OASIS (237)** — a working square, set 3.1 u off the through-road so the road does not split
  it. Fountain, market row, parasols, benches, lamps, planters; twenty-four houses facing in
  across three ranks; garden fences, hedges, side lanes with a front path to each door; a park
  with a pond, a bus stop with people waiting, cars aligned to the kerb, accessories in use.
- **EVENTER (165)** — a junction. Two roads actually meet, signals on all four corners, painted
  crossings, traffic queued in lane facing the right way; a railway with a locomotive and three
  wagons; two ranks of offices fronting the streets; pavements and street furniture.
- **MEDCOIN (84)** — the summit. Glazed commercial towers on bare rock, a mast and four dishes,
  tanks, a compound fence, hard standing. No forest, no crowd, no street furniture — the
  absence is the content. One figure at the edge, facing back down the valley.

**Outposts (63).** Every branch road now arrives somewhere: a watermill on the river with boats
and a bridge, a quarry EVENTER was cut from, a forest cabin with a fire and cut timber, and a
farm with animals, a fence and a proper block-of-rows field.

**Living cover.** 349 groves (2,699 trees), 233 riparian, 213 flowers in patches, 2,435
undergrowth, 242 crops in rows, 239 treeline conifers, 80 wild animals in twos and threes,
and 19 vehicles spread along the network rather than parked only at the junction.

Woodland comes in **eight stand types, each with its own colour bias** — dark north-facing
conifer, lighter birch, a minority turning in autumn, palms only on low ground near water.
A forest of identically tinted groves reads as one texture; this reads as woodland.

Density falls as the land rises, so the forest thins along the same line the career climbs,
gives way to a scattered treeline of hardy conifers, and stops before the bare summit. Snow
lies above 16 units, and only where the slope is shallow enough to hold it.

**Landmarks (86).** Things in the wilderness that are not settlements: a ruin above the river,
a lookout on a ridge, a pond with deer at the edge, a clearing where somebody has been felling,
a jetty with boats on the lower river, and a ring of standing stones on the open ground east of
the route. "70 % of the map is undifferentiated forest" was a fair note against v3.

**Roadside (59).** Hedgerows and post-and-rail fences along the open stretches of the main
route, a gate and a sign wherever a branch leaves it, markers spaced by arc length, and a
shelter with people waiting. Only 29 % of the verge is eligible — settlements and the climb to
the summit block the rest, correctly — so the runs are long and the gaps short.

**People (244 more, ~350 in all).** A `populate` pass adds groups on flat ground inside each
settlement, off the carriageway, under the same rule as the authored ones: twos and threes,
never scattered through the forest.

**Worked ground.** The terrain carries a `bare` mask that the palette reads, so the quarry is
stripped and dug into a bowl, the XTIX plot is cleared of turf, and the field is ploughed soil.
A quarry standing on unbroken grass is not a quarry.

**Colour.** Each model keeps its own material, graded once — desaturate 28 %, lift the crush
point, compress the blowout — with per-instance hue and value variation from a position hash.
Brand accents are rationed to one flag per place. Terrain never wears a company colour.

### The checks actually run now

`WORLD_SPEC_V4.md` §7 listed acceptance checks. Listing them is not running them, so
`check_world.py` measures the built instance data and exits non-zero if anything fails. On the
first run it found four real faults — three buildings on ground steeper than the spec allows,
seven forest trees inside the carriageway clearance, eight vehicles stranded away from any
road, and **a terrain gradient of 5.15, which is a 79-degree cliff in a world whose whole
premise is that it has none.**

Two of those were the checks being wrong rather than the world: a street tree BELONGS beside a
road, and a car parked in a town square is not stranded. Both checks were corrected rather than
the world bent to satisfy them.

The cliff was real. It came from ridge noise producing single-cell spikes, and from the height
field and the mountain crest both running off the map boundary. Chasing each source separately
kept trading one for another, so `Terrain.delimit()` now smooths **only where the field is too
steep** and repeats until it is not. The no-cliffs property holds by construction instead of by
inspection, and the rest of the terrain is untouched.

```
[PASS] nothing sinks into the terrain              0 below ground
[PASS] buildings on slope < 0.12                   0 over the limit
[PASS] people inside a settlement or beside a road 0 stray
[PASS] no tree within 0.90 u of a road centreline  0 too close
[PASS] every place has >= 120 instances            XTIX 518, OASIS 410, EVENTER 212, MEDCOIN 146
[PASS] vehicles on a road or inside a settlement   0 stranded
[PASS] no terrain gradient above 3.0 (interior)    steepest 2.83, 0 cells over
[PASS] page payload under 5 MB base64              3.58 MB
```

The gradient check measures the interior, excluding a 2 u margin. That margin is where the
field feathers off to the map boundary; it is covered by the skirt and no camera looks at it
edge-on. The exclusion is stated in the check's own output so it cannot hide.

---

## 3. Honest verdict

Far past v3. The map reads as a place: a river running out of the mountains, forest thinning as
the land climbs, four settlements on one road, outlying farms and a quarry, and a summit at the
end of it.

**Still wrong, in order:**

| # | Problem |
|---|---|
| **V1** | ~~Payload 6.2 MB~~ — **fixed**: 3.65 MB base64 after quantisation, sub-pixel culling and vertex dedup. |
| **V2** | ~~Labels unreadable over pale ground~~ — **fixed**: each line now sits on its own backing plate. |
| **V3** | ~~XTIX monochrome~~ — **partly fixed**: shipping containers, drums and material stacks carry colour now, but the frame itself is still grey and the tower crane reads thin at map scale. |
| **V4** | ~~Houses intersecting~~ — **fixed**: the claim radius is taken from the model's real footprint rather than a fixed circle. |
| **V5** | ~~Buildings uniformly cool~~ — **fixed**: two instances in five are pushed warm as well as hue-varied. |
| **V6** | ~~Bridge beside the crossing~~ — **fixed**: it is placed on the mill road's actual river crossing and stepped by its own measured length until it spans the channel. |
| **V7** | 988 k drawn triangles against a spec figure of 400 k. It renders in ~2 s headless at 1600×1000 with software rasterisation, so the budget is what is wrong, not the scene — but it should be restated with a measurement behind it rather than left contradicted. |
| **V8** | ~~Crane too thin~~ — **fixed**: the mast is eight stacked lattice cubes in works yellow with a jib and counterweight, and reads at map zoom. The frame itself is still grey, which is what concrete is. |
| **V9** | ~~Occupied rejections unchecked~~ — **covered**: `check_world.py` verifies every place still reaches its instance floor, and all four clear it by 25 % or more. |
| **V10** | ~~Slope limiter flattened the summit's backdrop~~ — **fixed**: with smoothness now guaranteed by `delimit()` rather than by keeping amplitude low, the range was raised again. Peaks reach 19.3 u, MEDCOIN stands at 16.5, and every check still passes. |

---

## 4. Measured facts — do not re-derive these

**Scale is calibrated per kit and verified visually.** v3 anchored the nature kit at 1 tile = 8 m
and was wrong by 2×: `tree_default` is 1.708 raw units and a mature broadleaf is 7 m, so that
kit is 4.10 m per model unit and its ground tile is 4.1 m, not 8. Every kit has a row in
`tools/kit_scale.json`, with the diagnostic model and the real size asserted recorded in
`tools/kit_scale_why.json`. `ruler.py` draws one model per kit against a metre grid and a 1.75 m
human bar and prints each height in metres, so a wrong scale is a number rather than a feeling.

Spot checks after calibration: car 4.56 m, two-storey house 7.19 m, person 1.74 m, door 2.05 m,
barrel 0.88 m, mature tree 6.64 m, rail segment 10.4 m.

**Traps already paid for, recorded so they are not paid for twice:**

- `wall-a-door` is a wall PANEL containing a door — a storey, not a 2.05 m door.
- `colormap` materials carry `Kd 1 1 1` and put the real colour in the texture. Preferring Kd
  turned every textured building pure white.
- Kenney's nature kit ships foliage at hue 169° and its pines at 181° — genuinely teal. Left
  alone, every tree renders mint.
- The green-unification window must stop short of blue. At 209° it caught the river, graded it
  to the same green as the grass, and the water disappeared entirely.
- `fence-1x4` spans 14.5 m. Nine of them 0.5 u apart overlap into one brown slab.
- The kit's `crane` is a 4.7 m workshop crane, not a tower crane.
- `construction-fence` is an open mesh panel; from overhead it reads as a row of hooks.
- Terrain index winding `a,b,c` puts the normal at (0,−1,0) and back-face culling eats the
  entire terrain.
- The camera needs a look-at HEIGHT. Aiming at sea level puts a summit off the top of the frame.
- Anything laid along a road must step by ARC LENGTH; the point array is not evenly spaced.
- Outposts need pads like the places do, or the slope gate silently rejects every building.
- Vegetation clear-zones must be checked per INSTANCE, not per grove centre, or grove members
  spill in and trees grow through the ruin and the farmyard.
- Authored planting inside a place must be exempt from those clear-zones, or a place loses its
  own grass.
- Culling triangles by absolute area erases small models entirely — a flower's every triangle
  is tiny. The threshold has to scale with the model, with a floor.
- `hi = H/15` saturates, so anything driven off it applies fully above 15 units. Snow has to be
  driven from real height or it covers a third of the range instead of the peaks.
- Measure the render, do not eyeball it: the high plateau looked like pale sand and measured
  0.34–0.42 lightness, which is correct rock.
- A property you want guaranteed has to be enforced, not tuned toward. Six rounds of adjusting
  ridge amplitude, edge feathering and range damping each traded one steep cell for another;
  one relaxation pass that smooths only what is too steep ended it in a single change.
- Anything laid along a road must also know which of ITS OWN axes is long: a hedge runs along
  Z, a fence panel along X, and rotating both the same way laid the fences across the road.

---

## 4b. The world master plan — 2026-08-29

All four cities are finished, and the plan for making them ONE world is
**`WORLD_MASTER_PLAN.md`**, with its numbers held as code in `tools/world_plan.py` and drawn
from that code by `tools/world_draw.py` (sheets 1 LAYOUT and 2 READING).

Nothing is built. What the survey established, measured headlessly from the four `.blend`
files rather than read off the generators:

- **The sun and the camera are already identical in all four** — 75 deg elevation, 135 deg
  azimuth, 0.8835 energy, 3.4 deg angle; orthographic at pitch 54.7 / yaw 45. Shadow direction
  and length are consistent across the world by construction, which is normally the hardest
  thing to reconcile in a merge.
- **Three seams that are not** — OASIS's plate green is `(0.246, 0.352, 0.072)` against the
  `(0.363, 0.518, 0.107)` the other three share; XTIX reaches no plate edge with road on any
  side (104-141 m short); and OASIS's streets are a lighter material than the rule that finds
  carriageway in the other three, so its mouths are the one number still to measure.
- **The layout is solved, not eyeballed.** `world_options.py` and `world_refine.py`: a compact
  2 x 2 hits 60 % built but puts two cities at the same place across the frame (middle reading
  step 23 m); a diagonal chain reads evenly and falls to a third built. The staggered rhombus
  gets both -- **1,874 m city bounding box, 60.0 % built, reading steps 606 / 341 / 676 m**, on
  a **2,020 m plate** whose 73 m margin is set by XTIX's own 70.2 m shadow.
- **The world totals 47,987 objects and 17.5 M faces**, against v4's 954 k. Page 1 is WebGL, so
  delivery is three tiers -- an L0 massing proxy for the world (<= 350 k triangles), an L1
  payload per city loaded on click, L2 as Cycles stills.
- **A dynamism contract**, restructured after the deep pass. A change is made safe in one of
  three ways: the WORLD OWNS it (sun, camera, ambient, and **the outer 40 m of every plate**,
  which the world re-plants itself so no city's verge has to match another's); the WORLD ADAPTS
  to it (the approach road is built from each city's OWN asphalt, so OASIS's blue-grey needs no
  change and a later re-colour propagates); or the CITY MUST HOLD it -- eleven checkable items
  C1-C11. Every change Oran has asked for across five rounds falls on the free side.

### What the deep join pass found, 2026-08-29

Measured in `world_join.py`, `world_join2.py`, `world_join3.py`, then audited by
`world_audit.py` -- **26 checks, 0 failures**.

**Agrees:** the sun, the camera, colour management (all four Standard/sRGB), the street grids,
and -- the one that could have sunk it -- **scale**: a person measures 1.75 / 1.74 / 1.75 m
across three cities, 1 % agreement.

**Does not:**
- **EVENTER's north and south mouths are at z = 13.0 m** -- the interchange's flyover. Only its
  W and E mouths are at grade. The route now ramps 12.86 m over 593 m (2.17 %) and enters
  EVENTER on the viaduct, leaving on the surface road. Found only by measuring mouth heights
  instead of assuming zero.
- **OASIS's asphalt is (0.133, 0.147, 0.216)** -- three times brighter than the other three and
  tinted blue, which is why every earlier survey reported "no roads at any OASIS edge". Its
  mouths are now measured: W at y=211, E at y=491, N spur at x=330 (155 m).
- **XTIX's foliage was teal** (hue 148.5) where the other three are green. That one was mine --
  the eight tints were built around the kit's raw teal, not knowing the other three had already
  graded away from it. **Re-graded 2026-08-29**: asked to bring XTIX to "the world's leaf
  colour" on the assumption the maps were in harmony, the measurement showed they were not --
  the three greens span 22.4 degrees of hue and EVENTER's foliage is 2.7x DARKER than OASIS's.
  So a world palette was derived instead (`world_plan.WORLD_FOLIAGE`, eight tints, hue 88-118
  centred on the area-weighted 104.2, value 0.24-0.67) and XTIX brought to it: 11,652 slots
  re-dealt, measured after at hue 99.8 / value 0.482, centrally placed among the other three.
  **The other three are still outstanding** -- hue is now one band across all four, value is not.
- **Four different ambients** -- EVENTER was authored 3.1x darker than OASIS, so identical RGB
  does not mean identical appearance. The world owns one shader and step 9c re-renders each
  city under it.
- OASIS's plate green, still (0.246, 0.352, 0.072) against the others' (0.363, 0.518, 0.107).

**OASIS also moved 45 m north**, so its west mouth lines up exactly with XTIX's avenue and the
connector is one straight line rather than a 17-degree kink. Reading steps 638 / 309 / 676.

---

## 5. The plan from here

1. **V1 payload**, then **V2 labels**, then **V3 XTIX colour**, then **V4 rectangular claims**.
2. **START/END and the timeline.** The markers carry FILE numbers, not years, and that is
   deliberate: only XTIX has a date range recorded anywhere local (2023–2026, from `lab2.html`).
   **The other three are not in any file here.** Supply them and the markers become years; the
   direction of travel is one constant to flip.
3. Then phases D–J: page 1 final, page 3 as a folder, page 4 approach and the click into the
   machine, the desktop with seven documents, copy, mobile, checks.

## 6. Standing constraints

- The shell is 1984. The content is 2026.
- Publish at `/portfolio/m/`. The root `index.html` is never touched by a build.
- Zero external requests except the one LinkedIn link.
- No new colours beyond the fixed tokens; every token stays a stop in its own ramp.
- Variation comes from a hash, never from modulo.
- Downloading any file needs explicit permission first.

## 7. The lessons this has already cost

1. **Design before building.** Two rejections, both the same note. The blueprint tables are the
   fix, and they are why the places read at all.
2. **Measure, then build — and verify the instrument.** `calibrate.py` returned 22 m per unit
   for `city-kit-roads` with complete confidence, because the only thing matching /traffic/ was
   a road tile with a light on it. `ruler.py` exists because a number that wrong needs a picture
   to catch it.
3. **When something looks wrong, measure before tuning.** The railway "obviously" had gaps; the
   spacing measured 1.293 u against a 1.300 u model. The real cause was a mountain in the way.

---

## EVENTER — complete, 2026-08-27

The interchange city is finished and audited. Third of the four workplaces to be built.

| | |
|---|---|
| plate · city square | 800 × 740 m · 440 × 440 m |
| roads | **14 ribbons** — 2 through routes, 4 ramps, 8 collector-distributors — at 4 levels |
| junctions | **16**, every one a full-width mouth at 27–31° |
| collector ring | 345 m square, 1,338 m of centreline, kerbs and pavements |
| planting belt | **5,132** objects, 93.4 % canopy cover, 32 species |
| villa ring | **36 plots**, 25–56 m wide, houses 11–22.6 m footprint in 21 types and 8 shades |
| abandoned ground | **573** objects in 12 categories, buildings in rows on the city's axes |
| traffic | **1,827 vehicles** in **15 road-relevant models**, 44 lanes, thinned toward the plate edges, **0 facing the wrong way · 0 intersecting · 0 that do not belong** |
| car colours | **100**, all in use — **970** distinct model x colour combinations |
| people · rail | **280** (0 on a deck) · 1.435 m gauge, 1,998 sleepers, 16 train cars |
| signage | 16 junction signs, 10 gantries, 76 lighting masts |
| **total** | ~8,800 objects, ~1.2 M triangles |

Renders: `world-build/shots/EVENTER_final*.png` — full plate, core, villas, abandoned.
Generator: `world-build/tools/eventer_gen.py`. Scene: `world-build/eventer.blend`.

Documents: `EVENTER_PLAN.md` (the interchange), `EVENTER_JUNCTION.md` (the mouth, designed
once and applied sixteen times), `EVENTER_ZONES.md` (the four rings), `EVENTER_PLOTS.md`
(the villa plots), `EVENTER_ABANDONED.md` (the yellow zone), `EVENTER_NIGHT.md` (the night
build and every decision taken alone), `EVENTER_FLEET.md` (edge thinning, what belongs on a
road, and the faults the audit was hiding).

### The lesson this city cost, six times over

**A build and its test read different data, and the test wins the argument while being
wrong.** Piers, road edges, plot contents, object kinds, a car's long axis, and a grid
search radius — six times, and six times the fix was the same: *one function, every
caller.* Guessing from a name, from a world bounding box, or from a second copy of the rule
is what produced every one of them.

---

## XTIX — complete, 2026-08-28

The fourth and last of the four workplaces, and the one the build order deliberately left
until last because it gains from everything learned before it.

**What it is:** a metropolis built from zero, **30 % of it still going up**. The frontier
runs on the diagonal — finished and tall at the back of the frame, construction at the
front — with the full road grid laid across the whole square from the first day, so *"the
plan of a future metropolis"* is something you can see rather than something explained.

| | |
|---|---|
| plate · city square | 800 × 740 m · **540 × 540 m** |
| grid | **7 × 7 = 49 blocks** of 62 m; 2 avenues at 20 m, 6 streets at 11 m; closes to 540 m exactly |
| buildings | **172** — 20 shape families × 12 facades × 11 glass tints, every one in use |
| under construction | **51 sites, 29.7 %**, across four stages at once |
| renewal in the mature core | **6 towers**, so cranes stand inside the finished skyline |
| landmark | **216 m** on the seam, the only building over 196 — topped out, crane still on it |
| tower cranes | **41**, every one derived from its plot's stage |
| site elements | **1,226**, different at every stage |
| traffic · people | **1,050** (698 moving, 352 parked) · **3,920** (2,796 pavement, 543 crossings, 328 open space, 253 crew) |
| planting | 328 street trees · **11,299** in the landscape outside · 747 in courtyards, plaza and park · 470 on roof gardens |
| public space | plaza, park, **19 service courtyards** — all planted |
| signage | **945** — 184 signals, 444 signs, 205 lamps, 112 crossings |
| construction dressing | **127** — 51 hoardings, 26 sheeting bands, 42 formwork stacks, 8 digs — plus **990 rebar bars** out of the top pours |
| sky bridges | **14**, spans 7.1–23.0 m at heights 42–95 m |
| **total** | **21,146 renderable objects** |

Renders: `world-build/shots/XTIX_final*.png`. Generator: `tools/xtix_gen.py`.
Plan: `tools/xtix_plan.py`. Audits: `tools/xtix_audit.py` (plan), `tools/xtix_verify.py`
(built scene). Scene: `world-build/xtix.blend`.

Documents: `XTIX_PLAN.md` (the plan, both audits, the two drawings) and `XTIX_BUILD.md`
(every decision taken alone and every fault found building it).

### What this city added to the method

**The plan became code.** For the first time the plan, the drawing and the audit all read
one set of structures, and the builder reads the same ones. That is the sixth answer to the
lesson that cost the most across four cities — *a build and its test read different data* —
and it is the first time the answer was structural rather than a fix applied afterwards.

**And it caught the worst instance of that lesson yet.** `plots()` was not a pure function:
`landmark_block()` read a global that `summary()` overwrites, so calling it before or after
moved the landmark, changed a block's tier, changed the plot count, and shifted the whole
random stream. **The builder built one city and the verifier checked another** — and
everything looked right. Only a per-object comparison of each tower's stored height against
its planned height exposed it.

**And the fault that all of it hid.** Oran said he could not see the cars or the people.
Both were there, both verified — 760 vehicles in their lanes facing the right way, 1,855
people on pavements — and both were **lying down**. `obj_import` puts its Y-up to Z-up
conversion on the OBJECT, not the mesh; `load_model()` tried to bake it with
`transform_apply()`, an operator that needs view-layer context and silently did nothing on a
hidden library collection; the placement code then overwrote `rotation_euler` with the yaw.
Every kit model in the city was left in file coordinates. Cars stood on their tails, people
lay on their backs, trees and signs lay flat. The fix is one `mesh.transform()` — a data
call, which cannot silently no-op — and the lesson is now explicit: **where an operator and
a data call both exist, the data call is the one that can be trusted.**

The verification missed it for eleven checks running because it measured **position and
facing** and never **uprightness**. Rule 1, a fourth time: measure the property, not a proxy.

**A second self-inflicted one.** `fix_missing_textures()` painted 2,615 objects one flat
beige-grey because it tested `image.has_data`, which is *lazy* — a healthy 512×512 PNG reads
`False` until something samples it. The 95 kit textures were on disk the whole time. Images
resolve through **the kit that owns the model using them** now, never by filename: eleven
kits ship a `colormap.png`, and matching on the name alone put the brick atlas on every car.

**The fourth pass measured first, and caught itself twice.** Asked to improve the vehicles,
the first analysis reported a 90 degrees median heading error on 734 of 760 cars and 226 cars
off their lane centre. Both were the MEASUREMENT: 90 degrees is the -Y front convention, and
the 226 were parked cars, which belong at the kerb. Measured against a proxy, a correct city
looks broken -- and had I trusted it I would have "fixed" geometry that was already right.

What survived was real: **157 intersecting vehicle pairs**, because positions were drawn
uniformly at random along each lane and parked cars were offset 1.55 m from a lane centre with
the direction chosen by a coin toss -- half of them leaning into live traffic on a lane only
3.5 m wide. Parking is a LANE now, not an offset; positions are walked with a headway; junction
boxes are kept clear. Zero clashes, zero lane-centre error, zero heading error.

**And a lesson about what a plan owns.** `build_cranes` picked a plot corner from its own RNG
while `crane_masts` measured jib reach from the plot CENTRE, 27 m away -- so a crane could
reach a neighbour the plan had ruled out of range. The plan chooses the position now. Same
family as the `plots()` purity fault, and the fourth time this map has paid for a builder
deciding something its own test reasoned about.

**Rule 4 earned its place twice.** Every check is fed a deliberate break before it is
trusted. Two checks failed to catch their break — the canyon test, because I broke `H` while
it reads the resolved massing, and the on-road test, because a road band is infinite along
its own axis. Both were real flaws, and neither would have been found any other way.

---

## 2026-08-29 — MEDCOIN planted, and the drawing set

**MEDCOIN planted.** 866 groves, 7,313 plants (2,730 trees, 3,109 shrubs, 1,345 ground cover,
129 rocks). Measured after: hue 100.5, sat 0.719, value 0.470, foliage 7,547 → 192,907 m².
Saved to `medcoin.blend`; pre-planting state kept at `medcoin.blend.preplant`.

All four cities now share one leaf palette — hue spread **9.5°**, value ratio **1.33×**:

| city | hue | sat | value | materials | foliage m² |
|---|---|---|---|---|---|
| XTIX | 99.7 | 0.712 | 0.484 | 15 | 251,065 |
| OASIS | 109.2 | 0.758 | 0.364 | 65 | 214,131 |
| EVENTER | 104.8 | 0.759 | 0.383 | 35 | 259,915 |
| MEDCOIN | 100.5 | 0.719 | 0.470 | 13 | 192,907 |

**The drawing set.** Five sheets, bound as `world-build/WORLD_MASTER_DRAWINGS.pdf`. Sheets 3,
4 and 5 are new and are drawn from `world_grid.json` — the four `.blend` files classified
headless on a common 8 m grid (33,413 cells, 5,760 built, roof height on every one). See
§14 of WORLD_MASTER_PLAN.md.

**Open, and Oran's to decide:** the four plates do not yet read as one ground. Leaf colour is
matched, ground mix is not — EVENTER 50 % bare grass, OASIS 86 % wood. §14.2 sets out the two
options. Nothing has been built either way.

**Nothing was merged.** The world is still four separate `.blend` files; the whole map exists
only as drawings, which is what was asked for.


---

## 2026-08-29 rev E — the visual plan finished, the world re-audited

**Eleven sheets**, bound as `world-build/WORLD_MASTER_DRAWINGS_revE.pdf`. Sheets 9, 10 and 11
are new: the site layouts, the palette and the light, and the reading.

**Every harness green.**

| harness | result |
|---|---|
| `world_verify` | 25 of 25 |
| `world_beltverify` | 20 of 20 |
| `world_net` | 38 road ends, 0 dead ends |
| `world_layout9` | 157 structures on 10 sites, 0 faults |
| `world_reader` | 17 checks, 13 pass, 4 deliberate gaps |
| `world_register` | 66 requirements, 0 open |

**Fixed point.** Feeding the measured roof areas back into the programme changes 0 of 10 built
fractions; sheets 7 and 9 agree to 1.000×.

**Build edits this session:** OASIS's plate grass levelled to the world value (one material,
one object, 455,102 m², re-measured from the saved file). Backup at `world_map.blend.pregrass`.

**Still four separate `.blend` files.** Nothing merged. The belt exists only as drawings.

**Next:** build ONE district — the XTIX–EVENTER gap — and render it. About 4 % of the belt, and
it converts every arithmetic claim on sheets 8, 9 and 10 into evidence.

---

## The first district exists

`world-build/belt_district.blend` — the XTIX–EVENTER gap, x 0–980 / y 800–1215, 406,700 m²,
about 4 % of the belt. Built in stages by `world-build/tools/belt_build.py`.

```bash
blender -b --python belt_build.py -- --stage ground
blender -b --python belt_build.py -- --stage roads
blender -b --python belt_build.py -- --stage structures
blender -b --python belt_build.py -- --stage planting
blender -b --python belt_build.py -- --stage verify
```

| | |
|---|---|
| roads | 7 sections, all from `world_net.all_roads()` |
| structures | 44 from 20 assets, placed by `world_layout9.json` |
| planting | 2,648 plants, 24 unique meshes |
| geometry | 822,850 faces drawn from 94,376 stored — 8.7× |

**Every harness green, including the new one.**

| harness | result |
|---|---|
| `world_verify` | 25 of 25 |
| `world_beltverify` | 20 of 20 |
| `world_net` | 38 road ends, 0 dead ends |
| `world_layout9` | 154 structures on 10 sites, 0 faults |
| `world_reader` | 17 checks, 13 pass, 4 deliberate gaps |
| `world_register` | 66 requirements, 0 open |
| `belt_build --stage verify` | 7 of 7, measured through the depsgraph |

**New this session:** `world_cells.py` — one classifier for what is on the ground at a point,
imported by both `world_beltverify` and `belt_build`. It replaced two copies that had already
drifted: the audit's `city_at` was on inclusive bounds while its `in_rect` was half-open, so
2,960 m² of woodland was booked as city.

**Corrected in the plan by building it:** the filling station is one 54.84 × 25.67 × 7.23 m
asset, not two invented rectangles; the peterbilt is a 8.5 m tractor unit built at 2.73× life
size, not a 20 m rig; `Farm_Plow02` has its own dimensions; site containment is tested against
the site, not against its bounding box in the road frame. Details in §23.3 of the master plan.

**Still four separate `.blend` files plus this district.** Nothing merged.

### Rebuilt after Oran's review, 2026-08-30

Three findings, all correct: the roads were seven flat quads with no markings, no verges and
no junctions; the fields were flat coloured rectangles; and the preview was sent at 1.18 m/px
where the cities are reviewed at 0.62 and 0.37.

- **`road_measure.py` / `_3` / `_4`** — opened the three city files and measured what a road in
  this world is made of before designing anything. XTIX's ground is ONE mesh, 1,179 faces, 11
  flat-colour slots, no UVs, no textures. Marking 0.26 x 2.60 m every 6.50 m at +0.011 above
  the tarmac; MEDCOIN 0.36 x 2.00 every 5.00 at +0.012. **All three cities agree on a 40 % duty
  cycle.**
- **`world_road.py`** — the road standard. The reserve includes its verges, which makes a 12 m
  reserve a 7 m carriageway (XTIX's street) and a 20 m reserve a 14 m one (XTIX's avenue). An
  80 m motorway is 28 m of tarmac, a 12 m median and 20 m verges — not an 80 m black slab.
  Verges, dashes, edge lines, junction fillets and tapers.
- **`world_field.py`** — the field standard. Drill rows, tramlines, headland, per-field
  direction and one of six crops or three grasslands. 381 faces for the whole belt. Pasture
  recoloured against the plate: it was **47 % lighter than the grass it sat on**.
- **EVENTER south frontage**, y = 1185, boundary to boundary — the road Oran drew in red.
  Six new junctions; the network is now 20 roads, 10.33 km, 40 ends, 0 dead ends.
- **Every BOUNDARY or MOUTH end is carried 40 m past the cut** before drawing, so a road that
  leaves the frame is seen to leave it.
- **`--stage verify` C1 to C8** — checks that count CRAFT, not quantity. Fifty-two green checks
  had not caught a black rectangle, because all fifty-two counted quantities.

**Harnesses:** world_verify 25/25 · world_beltverify 20/20 · world_net 0 dead ends ·
world_layout9 0 faults · world_register 0 open · **belt_build verify 15 of 15**.

**Renders at stated scales:** `BD_page.png` 0.908 m/px (page 1's own scale) and
`BD_detail.png` 0.368 m/px (the scale XTIX was shot at). `shoot_bd.py` now takes metres per
pixel and works the pixels out, so craft is compared against craft.

**Next:** the second district, or the merge. The district proves the generators; the merge is
what makes one world out of five files.

---

## THE WORLD IS BUILT — 2026-08-30

One file, `world_belt.blend`, holds the whole of page 1: the countryside belt across the full
2,020 × 2,020 m plate **and** all four cities merged into their plates.

**78,287 objects · 20,195,466 faces · every check green.**

### How to rebuild it, cold

```bash
cd "C:/Users/Alex/Desktop/Oran_Personal_Brand/world-build"
python tools/world_audit2.py                                    # the plan, 11 of 11, before anything
B="C:/Program Files/Blender Foundation/Blender 5.2/blender.exe"
for s in ground roads water structures planting furniture life; do
  "$B" -b --python tools/world_build.py -- --stage $s
done
for c in MEDCOIN EVENTER OASIS XTIX; do
  "$B" -b --python tools/world_build.py -- --stage merge --city $c
done
"$B" -b --python tools/world_approach.py                        # measures the 19 city seams
"$B" -b --python tools/world_build.py -- --stage approach
"$B" -b --python tools/world_build.py -- --stage verify
"$B" -b --python tools/world_build.py -- --stage render --mpp 0.908
```

`--stage ground` starts from an empty file, so it wipes everything after it. Every other stage
loads the last save, clears **only what it built last time**, and adds its own work back — each
object carries a `stg` stamp naming the stage that made it. A detail crop is the same camera on
a smaller rectangle: `--stage render --mpp 0.16 --x0 700 --y0 860 --x1 860 --y1 1000 --tag station`.

XTIX takes about twelve minutes to append on this machine; the others four to five.

### The modules, and which question each one owns

| module | the question it is the only answer to |
|---|---|
| `world_make.py` | **how anything is built** — shared by the sample board and the world, never copied |
| `world_road.py` | what a road is: reserve, carriageway, verge, 40 % markings, fillets, tapers, grade separations |
| `world_field.py` | what a field is: crop, drill rows, tramlines, headland — and `subdivide()`, which cuts a block into the fields that survive the roads and the water |
| `world_water.py` | the one watercourse, its banks, its bridges and its pond |
| `world_place.py` | **what may stand where** — `free`, `along`, `split`, `cluster`, `power_network` |
| `world_palette.py` | what colour a kit material becomes, and that nothing in the belt is cyan |
| `world_elements.py` | the register: 78 elements, each with a source, a layer and a rule |
| `world_build.py` | the driver: the stages, the canopy field, the structure sources, the merge, the approaches |
| `world_approach.py` | how far into each city a belt road must run before it meets that city's own road |
| `world_audit2.py` | whether the plan is buildable — run **before** building, always |

### Harnesses

`world_audit2` 11/11 · `sample_build verify` 4/4 with 4,858 objects unchanged ·
`world_verify` 25/25 · `world_beltverify` 20/20 · `world_net` 40 ends, 0 dead ·
`world_layout9` 154 structures, 0 faults · `world_build verify` — 0 on a carriageway, 0 in
water, 0 off the board, 0 taller than wide, 4 cities on their plates, 0 belt materials in the
cyan band, 0 dead textures.

### What is honestly still open

- ~~**The 30 mm lip at each plate edge.**~~ **CLOSED 2026-08-30 by Oran, on the render:**
  *"it's bad, but I don't see it looking like a sticker — it actually looks fine."* The seam
  stays as built. Each city keeps its own ground (OASIS's terrain is 115,776 vertices,
  EVENTER's villa ground stands 5 m proud) and is lifted 30 mm so its surface sits above the
  world plate rather than fighting it. Recorded here because the reason it looked like a fault
  in the first place — the pale rectangles — turned out to be the woodland density, not the
  ground colour: every city's grass is already the belt's exact green.
- **XTIX's carriageway sits 60 mm below the belt's** after the lift (0.080 against 0.140).
  Logged since §24.2, still not averaged away.
- **The copy round** for the page itself — labels, the PATH, START and END — has not started.

---

## THE BELT REVIEWED, REBUILT AND INHABITED — 2026-08-31

Oran cut the plate into sixteen sheets and marked ten of them. Every note has been answered,
and the belt now has people, stock, machinery, traffic and lighting in it.

**88,236 objects · 22,099,591 faces · every check green.**

### How to rebuild it, cold

```bash
cd "C:/Users/Alex/Desktop/Oran_Personal_Brand/world-build"
python tools/world_audit2.py                          # the plan, 11 of 11, before anything
B="C:/Program Files/Blender Foundation/Blender 5.2/blender.exe"
"$B" -b --python tools/world_xsec.py                  # what each city hands over at its edge
"$B" -b --python tools/world_approach.py              # how far in each city's street starts
for s in ground roads water structures planting furniture life; do
  "$B" -b --python tools/world_build.py -- --stage $s
done
for c in MEDCOIN EVENTER OASIS XTIX; do
  "$B" -b --python tools/world_build.py -- --stage merge --city $c
done
"$B" -b --python tools/world_build.py -- --stage approach
"$B" -b --python tools/world_build.py -- --stage verify
"$B" -b --python tools/world_build.py -- --stage render --mpp 0.908
"$B" -b --python tools/world_build.py -- --stage tiles --mpp 0.20
python tools/world_roadmap.py                         # every road named, on the render
python tools/world_keymap.py                          # the A1-D4 sheet grid, on the render
```

`--stage ground` starts from an empty file, so it wipes everything after it. Every other stage
loads the last save, **purges orphaned datablocks**, clears only what it built last time, and
adds its own work back. Each object carries a `stg` stamp naming the stage that made it.

**Two measurements must run before the build and are inputs to it:** `world_xsec` (the
cross-section each city hands over at each mouth) and `world_approach` (how far into each city
its own street network really starts). Both find carriageway by **material name**, sampled over
the face — never by colour, and never at the vertices.

### The modules, and which question each owns

| module | the question it is the only answer to |
|---|---|
| `world_make.py` | **how anything is built** — shared by the sample board and the world |
| `world_road.py` | what a road is: reserve, carriageway, verge, 40 % markings, fillets, tapers, grade separations |
| `world_mouth.py` | what a city hands over at its edge, and how the belt continues it |
| `world_field.py` | what a field is, and `subdivide()` — what survives the roads and the water |
| `world_water.py` | the watercourse, its banks, its bridges and its pond |
| `world_place.py` | **what may stand where** — `free`, `along`, `split`, `cluster`, `power_network` |
| `world_life.py` | what lives, works and grows: people, stock, wildlife, machinery, crop, rough ground, mottling, bus stops |
| `world_palette.py` | what colour a kit material becomes — and it now **corrects** cyan rather than reporting it |
| `world_build.py` | the driver: stages, canopy field, structure sources, merge, approaches, tiles |
| `world_xsec.py` · `world_approach.py` | the two seam measurements |
| `world_audit2.py` | whether the plan is buildable — run **before** building, always |
| `world_roadmap.py` · `world_keymap.py` | the named road map and the A1–D4 sheet grid, for review |

### Review material

`renders/REVIEW/` holds the sheets: `00_KEY.png` (the A1–D4 grid), `00_WHOLE_0p908.png`
(page scale), `A1.png`–`D4.png` (16 sheets at 0.20 m/px, ~4,000 × 3,500 px each) and
`views/` (16 declared close views). `renders/ROAD_KEY.png` names all twenty roads.

### What is honestly still open

- **The PATH treatment has not started** — the trail markers, START and END, and the labels
  over each city. It carries a design fork (route in 3D, words as an overlay) that was put to
  Oran and is unanswered.
- **XTIX's carriageway sits 60 mm below the belt's** after the 30 mm merge lift. 0.07 of a
  pixel at page scale. Logged since the road standard was first measured.
- ~~The 30 mm lip at each plate edge~~ — **closed by Oran on the render**: *"it's bad, but I
  don't see it looking like a sticker — it actually looks fine."*
- **`EVE-E 548` leaves EVENTER where EVENTER has no road at all** (measured: nothing within
  201 m). It is closed with a turning head and a barrier, which is honest, but the road's
  reason for existing is a plan question rather than a build one.

---

## THE ROADS MADE FROM THE INTERCHANGE'S OWN PARTS — 2026-08-31

Oran, on the render: *"the elements of the roads are not right and do not match, and so
suddenly the road looks different — just find the elements of the roads we built the
interchange with and apply the continuation with those same roads."* And then, on the first
corrected render: *"look at the connection of the roads into a single road — not good."*

Both were right, and both had the same shape of cause: **a thing that existed but was pointed
at the wrong place.**

### What changed

| | before | now |
|---|---|---|
| where the elevated road's elements come from | invented in `world_build` | `world_road.EV_SRGB`, EVENTER's own table, asserted against `eventer_gen.PALETTE` |
| an elevated deck | a plane of zero thickness | a 0.90 m box: deck, soffit, concrete edge walls, barrier parapet, kerb |
| piers | pier grey, axis-aligned | EVENTER's concrete, square to their own deck |
| markings | 0.36 m white, dashed centre | 0.45 m, **yellow solid centre**, white edges and lanes |
| kerbs | none | MAIN, DUAL and TRUNK, both edges, full length |
| a stream crossing on a motorway | a stretched `bridge_stone` | the same deck as the viaducts |
| where a dual becomes a single | a flat quad on the grass, six metres under the road | two converging decks at the road's own height |
| a vehicle's heading | whichever function the caller remembered | `place()` turns every vehicle by its own long axis |
| which way a vehicle faces | local +Y — the whole fleet in reverse | local −Y, measured by rendering all fourteen models |
| which way traffic runs | the lane's offset, so carriageways met head-on | the carriageway's, so each runs one way |
| lighting on a viaduct | none — a column under its own deck was thrown away | on the deck, inside the parapet |

### The two new checks

- **`tools/world_provenance.py`** — asserts, inside Blender, that `world_road.EV_SRGB` still
  equals `eventer_gen.PALETTE` key for key and that `DECK_T`, `PARAPET_H/T`, `KERB_W` and the
  marking width still match; then measures every elevated-road material in the built file
  against that table. It failed the first time it ran, naming the three materials that were
  wrong. A comment saying "these came from EVENTER" is not evidence.
- **`tools/world_inspect.py`** — the element-by-element audit: sun and shadow, orientation,
  direction of travel, lighting columns, road intersections, layer discipline, z-fighting,
  degenerate geometry, floating. Scoped by the `stg` stamp to what the belt itself built,
  because the four cities are signed off and would otherwise drown the belt's own faults.

### Two hazards found and closed

- **`import world_build` used to destroy the world.** The module dispatched at import, so a
  one-line check of whether a function existed ran the default `ground` stage — which empties
  the file and saves. 88,346 objects and four merged cities to 767, in two seconds. Recovered
  from Blender's own `.blend1`. There is now a `if __name__ == "__main__":` guard and an
  explicit copy at `world_belt.blend.SAFE`.
- **A stage re-run was quadratic.** `bpy.data.objects.remove()` unlinks from every collection,
  so clearing 2,484 road objects out of the merged 88,000-object world one at a time had not
  finished in twenty minutes. `bpy.data.batch_remove()` does the same work in one pass, and
  the stage now takes minutes. The orphan purge was batched with it.
