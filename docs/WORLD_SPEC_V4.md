# WORLD v4 — specification

Supersedes the v3 build described in `WORLD_STATE.md` §2–3. Written before any code, because
the two rejections before this one were both "you built without a plan".

v3's failure was not detail — it had 6,337 instances. It was that the *system* was wrong in
three places at once: the terrain was quantised into tiles so it could only ever be steps, the
colour pipeline forced every model onto four brand ramps so nothing could look real, and props
were placed by proximity rules rather than by what a thing is *for*. v4 replaces all three.

**Library available:** 42 Kenney kits, 4,236 models, all CC0. See `world-build/kits/`.

---

## 0. The eight requirements this must satisfy

| | Requirement | Where it is answered |
|---|---|---|
| R1 | Matte, realistic, varied colour on **everything** | §2 |
| R2 | No steps, no cliffs — smooth valleys, wadis, hills, mountains, real shading | §1 |
| R3 | Each place is its own dense mini-world; click the name to zoom in | §4, §6 |
| R4 | Logic in everything — orientation, grouping, scale, occupancy | §5 |
| R5 | Case label text larger | §6 |
| R6 | Main path stronger and wider; plus secondary roads and tracks | §3 |
| R7 | START and END markers consistent with the case axis | §6 |
| R8 | Many kits, many element types, creative | §4, and the 4,236-model library |

---

## 1. Terrain — one continuous surface

**The rule that kills the steps: there are no tiles.** The ground is a single triangle mesh
sampled from a continuous height function. Nothing is rounded to a level, so nothing can
terrace, and there is no such thing as a cliff block.

- **Extent** 84 × 60 world units, 1 unit = 8 m → about 670 m × 480 m.
- **Resolution** 3 samples per unit → 253 × 181 vertices ≈ 45,800 verts, ≈ 91,000 triangles.
- **Normals** analytic, from central differences of the height field. Smooth by construction.

`H(x, y)` is the sum of, in order:

1. **Trend.** Rises along the route parameter `t`: 0 at XTIX, ~9 units (72 m) at MEDCOIN.
   Elevation carries the career, as before — but now as a gradient, not a staircase.
2. **Fractal value noise**, 5 octaves, lacunarity 2.0, gain 0.5 — the general undulation.
3. **Ridge noise**, weighted up near MEDCOIN, for a mountain spine at the high end.
4. **A wadi** — a dry valley carved along its own curve, deep and steep-sided at the low end,
   shallowing as it climbs. Carved with a smooth distance falloff, never a wall.
5. **A river** — a second carved channel, wider and flatter-bottomed, with a water surface
   drawn at a fixed level inside it.
6. **Pads.** Near each place, `H` is blended toward a locally level value with a smoothstep
   falloff over ~6 units. Levelling ground before building is what actually happens, and the
   blend means the transition is a slope, never a step.

**Slope is a first-class quantity.** `slope(x,y)` from the same derivatives drives colour,
what may be placed, and where roads may run.

## 2. Colour — realistic, matte, varied

v3 forced every model through `onto_ramp()` into one of four brand ramps. That is why the
world was one green and why nothing looked like itself. v4 inverts it.

**Base colour comes from the model's own material** — Kenney's palettes are already coherent
and were designed to sit together. Then one global grade, applied to every model identically:

- desaturate 18 % (matte, no plastic)
- lift the darkest tones slightly so nothing crushes to black (this also fixes W9)
- vegetation only: rotate hue toward the document's green

**The document's green.** The brand token is `#2FB380` — hue 157°, quite teal. Real grass is
90–110°. Vegetation is placed at **hue 138°, saturation 26 %, lightness 30–42 %** — recognisably
the same family as the token, but matte and real. The token itself stays reserved as an accent.

**Per-instance variation, from a hash of position** (never modulo — that produces visible
periodic patterns): hue ±6°, saturation ±8 %, lightness ±10 %. Thirty houses are thirty
houses, not one house thirty times.

**Brand accents are rationed.** Each place spends its ramp colour on a handful of deliberate
objects — a flag, signage, a roof trim, a vehicle — and nowhere else. Terrain never wears a
company colour. That was v3's mistake and it is what made the map look painted rather than lit.

**Terrain colour** is a function of height, slope and distance-to-water:

| Condition | Reads as |
|---|---|
| in channel, below water level | wet gravel, dark |
| within 1.5 u of water | lush dark green, damp earth at the lip |
| low and flat | rich meadow green |
| mid | grass, drying with height |
| slope > 0.45 | earth showing through |
| slope > 0.62 | rock, grey-brown |
| high and flat | dry pale grass, then scree |
| highest | bare stone |

Blended, not switched — every boundary is a ramp over a range, so no bands appear.

## 3. Roads — draped ribbons, not tiles

Tiles cannot follow a smooth surface, and v3's road left gaps because the tile was scaled to
0.85 (`WORLD_STATE.md` §5). v4 generates road **geometry**.

A road is a Catmull–Rom spline. At each sample the tangent gives a perpendicular; the ribbon
edges are offset ±width/2 and dropped onto the terrain at `H + 0.02`. Triangulated as a strip.
Because it is sampled from the same height function, it cannot float and cannot gap.

| Class | Width | Surface | Purpose |
|---|---|---|---|
| **Main route** | 2.2 u (17.6 m) | dark asphalt, pale centre dashes, kerbs | the career path — deliberately the strongest line on the map |
| **Secondary** | 1.2 u | pale gravel | place → outlying feature: quarry, jetty, farm, lookout |
| **Track** | 0.7 u | dirt | forest cabin, field edge, riverbank |
| **Footpath** | 0.4 u | stone/paving | inside the mini-worlds only |

The main route is the widest and highest-contrast object in the world, against a matte green
ground. R6 is a contrast problem, and it is solved with width and value, not with a brighter
colour.

**Roads bind the terrain.** Where a road passes, `H` is smoothed along the ribbon so the
surface does not buck under it — the same trick as the pads, and the reason a road can climb
to MEDCOIN in switchbacks without stepping.

## 4. The four mini-worlds

Each is authored, dense, and built from what the place *means*. Each sits on its pad and fills
roughly 16 × 16 units.

**XTIX — BUILT FROM ZERO.** A town being built, read left to right: raw forest, then cleared
ground with stumps, then an active construction site, then a finished street. The site has a
building part-raised — ground floor walled, upper floor still columns and open frames —
scaffolding on two faces, a tower crane, site hoarding, cones, a portacabin, stacked pallets,
bricks, pipes, sand and gravel heaps, a mixer, tipper trucks, and workers. Newly planted
saplings in rows along the new road: young trees, not mature ones. *Kits: modular-buildings,
retro-urban-kit, factory-kit, brick-kit, racing-kit (barriers), survival-kit, blocky-characters.*

**OASIS — LEADERSHIP.** A working town square. Houses face the square — this is what made
OASIS the one place in v3 that read correctly, and it is kept. Added: a well or fountain at the
centre, a market row with stalls and produce, awnings and parasols, benches, lamp posts,
planters, a cafe, a bus and delivery van at the kerb, and people in groups of two to four.
Pavements, crossings, parked cars aligned to the kerb. *Kits: city-kit-suburban,
fantasy-town-kit, mini-market, food-kit, furniture-kit, holiday-kit, car-kit, mini-characters.*

**EVENTER — ALIGNMENT.** A junction town, where alignment is literal. Two roads actually meet;
signals on all four corners; painted crossings; traffic queued facing the right way on the
right side. A rail line crosses with a level crossing and a small station — timetables are
alignment made physical. Mid-rise offices front the streets, with pavements and street
furniture. *Kits: city-kit-roads, 3d-road-tiles, train-kit, modular-buildings, city-kit-commercial,
car-kit, furniture-kit.*

**MEDCOIN — FOUNDER.** The summit, and what is *missing* is the content: no forest, no crowd,
no street furniture. Bare rock and thin dry grass. One structure with real presence — a tower
with a mast and dishes — a helipad, a few solar panels, and a single road climbing in
switchbacks. One figure standing at the edge, facing back down the valley at the other three
places. *Kits: space-kit, space-station-kit, castle-kit, modular-buildings, nature-kit (rock).*

## 5. Logic — enforced in code, not judged by eye

Each of these is a function, so it holds for every instance rather than for the ones that were
checked:

1. **Buildings face something.** Rotation is computed toward the nearest road centreline or
   square centre — never authored as a guess, never facing a tree.
2. **Vehicles belong to roads.** Placed by arc-length along a ribbon, offset to the correct
   side, rotated to the tangent. A car cannot be in a field.
3. **People belong to places.** Pavements, squares, plots, doorways, vehicles. Never scattered
   in forest. Emitted in groups of 2–4 with small spacing, because people stand together.
4. **Trees grow in groves** with one dominant species per grove; a tree that would land alone
   in open ground is not placed. Kept from v3 — it was the one rule that worked.
5. **Flowers and crops come in patches and rows**, never singly.
6. **Nothing floats and nothing sinks.** Every instance's height is sampled from `H` at its own
   position, after pads and road-binding are applied.
7. **Slope gates placement.** Buildings need slope < 0.12; props < 0.3; trees < 0.5; nothing
   at all above 0.75.
8. **One sun.** A single fixed direction lights terrain, water, roads and every model, with a
   sky-coloured fill from above and a bounce term from the ground.

## 6. Presentation

- **Labels larger**: name 19 px semibold, subtitle 12 px, tracked. The arrow above each place
  stays, tinted to that place's accent.
- **Click a label → fly to the place**: eased camera interpolation over ~900 ms to dist 19,
  pitch 0.46 — close AND low, because the point of flying in is to read detail and a
  near-overhead framing flattens exactly the vertical detail worth reading. Click the background, or a back control, to
  return to the map. This is R3's second half — the density only pays off if it can be seen.
- **START and END.** `XTIX` is marked **START · FILE 01** and `MEDCOIN` **END · FILE 04**,
  matching the document's file order and the order given for the cases.
  **Open question, deliberately not fabricated:** only XTIX has a recorded date range locally
  (2023–2026, from `lab2.html`). The other three are not in any file here. The markers
  therefore carry file numbers, not years. If the four real date ranges are supplied, the
  markers become years and the direction of travel is a single constant to flip.

## 7. Budgets and checks

- Terrain ≈ 91 k triangles; models ≈ 250 k; total under 400 k. v3 drew 267 k comfortably.
- The generator stays deterministic under a fixed seed; the printed instance and triangle
  counts are the ratchet, as in v3.
- Every build renders the five standard views headlessly (`shoot.py all`) so a regression is
  visible rather than assumed.
- Checks that must pass before any build is shown:
  `no instance more than 0.05 u off the terrain`, `no building on slope > 0.12`,
  `no person outside a permitted zone`, `no tree closer than 1.0 u to a road centreline`,
  `every place has ≥ 120 instances`.
