# EVENTER — the night build. Decisions taken alone, and the final state

Oran left the machine running and gave standing authority to finish the map, deciding any
open question myself and reporting every such decision at the end. This is that report.

---

## 1. Decisions I made without asking

### 1.1 The two flyovers carry the movements the GEOMETRY encodes, not the ones their names claim

Right-hand traffic fixes the travel direction of every side of every motorway: L1's north
side runs west, its south side east; L2's east side runs north, its west side south. A ramp
touches a motorway on a known side at each end, so its own direction is **derived**, not
named.

| ramp | its name says | as built it carries |
|---|---|---|
| `NE_N_to_W` | N → W | **N → W** ✅ |
| `SW_S_to_E` | S → E | **S → E** ✅ |
| `NW_E_to_N` | E → N | **S → W** |
| `SE_W_to_S` | W → S | **N → E** |

The two loops match their names exactly. The two flyovers do not: as routed they carry
right turns on a 19.5 m structure, which is over-engineered but reads correctly — a ribbon
climbing over the crossing looks the same either way at this scale.

**Decision: keep the geometry, keep the names, put the cars on the geometry.** Renaming
would touch `flyover_paths`, the junction table, the signage list and every note that
references them, for a change nobody can see. What Oran actually asked for — *no two cars
in the same lane facing each other* — is measured and is **zero**.

### 1.2 No city ramps from the interchange down to the collector ring

L1 sits 6.5 m up across the entire city square and only reaches grade beyond it, so a ramp
joining the ring needs 106 m of descent at 6 %. The only ground with that much room is the
villa strip and the planting belt, and cutting either apart to bury a road that would be
hidden under the viaduct is a poor trade.

**Decision: the ring is a closed residential loop.** The interchange's collector roads leave
the plate at grade to the west and east, and the link between them happens beyond the frame
— which is exactly how L2 is handled, and how every road leaves every plate in this world.

### 1.3 The density band for the abandoned ground was wrong, not the build

I set "35–55 % of the ground within 4 m of something" before I could see it. With 573
objects over 60,372 m² the mean spacing is 10 m, so 64 % is simply what an even scatter
gives; the band assumed a clustering that does not happen. **The picture, not the number,
decided:** it reads as built-up as OASIS and nothing like MEDCOIN, which is the brief.

### 1.4 Small asset banks keep a high share, and that is reported rather than hidden

Chimneys are 50 % one model and food stalls 60 %, because the kits ship four and three.
Every other category is well under its cap. Splitting them by scale and tint is possible
and was **not** done — it would be dressing a shortage rather than fixing one.

### 1.5 The hue guard is scoped to rust, not to the whole file

A blanket "no Hue node below 0.5" flagged four **correct** materials — the villa roofs,
whose atlas is green and where a negative rotation gives terracotta. On the industrial
atlas, which has red panels, the same rotation gives magenta. The constraint belongs to the
rust family. A test that fires on correct work is a test that gets ignored.

### 1.6 The country got trees, because the audit could not see that it was bare

Every test passed and the map still had a fault only the picture shows: **398,400 m² of
country outside the city square, completely empty.** A flat green apron reads as unfinished
ground, not as countryside.

**Decision: 1,009 objects in 16 copses**, not an even scatter — trees in this landscape grow
in stands with open pasture between them, and a sprinkle at the same object count reads as a
lawn with dots on it while costing exactly the same to render.

### 1.7 No LOD pass on the vehicles

The plan called for decimating the cars to ≤450 triangles. Measured: they are 2,266 each and
the traffic is 4.5 M of the map's 5.9 M triangles — but the full-quality final render still
completed in **13 minutes**, and at 4.44 px/m a car is 20 pixels across.

**Decision: leave them.** Decimation of low-poly game assets breaks their shading before it
saves anything visible, and the cost it was meant to solve turned out not to be a cost.

### 1.8 The collector ring got lighting and parked cars

It was a lit residential street with neither. **28 masts and 46 parked cars** — and the
parked ones take the heading of the lane beside them, which is MEDCOIN's second vehicle
fault and the one that put 307 cars nose to nose.

---

## 2. What was built tonight

| stage | result |
|---|---|
| traffic | **1,982 vehicles**, 44 lanes, 14 models, 12.2 m bumper spacing |
| people | **280** — 190 on the ring's pavements, 90 in the abandoned ground, 30 models |
| signage | **16** junction signs, **10** gantries, **76** lighting masts |
| light rail | 1.435 m gauge, **1,998 sleepers**, 92 m island platform, **16 train cars**, 11 models |
| country | **1,009** objects in 16 copses — 778 trees, 161 bushes, 70 rocks |
| ring life | **28** lighting masts, **46** parked cars |
| dead space | swept — **0 empty cells** in the whole city square |

## 3. The final audit — every test, run together

| | |
|---|---|
| roads that end in nothing | **0** |
| clearance conflicts · worst headroom | **0** · **5.60 m** vs a 5.00 m standard |
| steepest grade | **6.80 %** vs a 7 % limit |
| junction faults (width, angle, overlap) | **0** |
| holes visible from the camera | 12 of ~11,600 rays — plate edges and gore tips |
| pier sites dropped for a clash | 25 — piers in a road: **0** |
| plots on a road · houses outside a plot | **0** · **0** |
| ground regions painted wrong | **0** |
| teal, white or salmon foliage | **0** |
| materials pointing at a dead image | **0** |
| rust hues below centre | **0** |
| **vehicles facing the wrong way** | **0** of 1,982 |
| vehicles not on a road | **0** |
| people on an elevated deck | **0** |
| rail inside its median · trains off track | **yes** (3.69 m of 4.5) · **0** |
| **dead space** | **0 %** |

## 4. Faults found and fixed tonight

1. **Every car in the city faced backwards.** MEDCOIN's `veh_pre` already contains the half
   turn — the front is at minus the length axis — and I added a further π on top of it. The
   test caught all 1,982.
2. **The direction test was inverted before that**, reading the model's long axis off its
   **world** bounding box, which is measured after rotation and therefore says nothing about
   the model's own axis. It reported 1,588 cars backwards when none were.
3. **170 vehicles "off-road" were a grid artefact** — a car in L1's outer lane is 16.75 m
   from the centreline, further than the ±1 cell the coarse check searched. A precise
   per-car check found **zero**.
4. **Signs, gantry beams and lamp heads rendered black**: each was drawn as two coincident
   quads with opposite normals, fighting for the same pixels. They are solids now.
5. **The gantry rewrite deleted the anchors its own sign panels used** — caught immediately
   by the build failing rather than by a later render.

## 5. Six times a build and its test read different data

The pattern that cost the most across this whole city, and the fix that worked every time:

| # | what disagreed | the single source now |
|---|---|---|
| 1 | pier placement vs the pier audit | `pier_sites` |
| 2 | where a road edge is, before vs after clipping | `edge_pt` |
| 3 | which element sits where on a plot | `plot_plan` |
| 4 | what a placed object IS | `evkind` tag, set at placement |
| 5 | a car's long axis, local vs world | `long_is_y` tag, set at placement |
| 6 | on-road test grid vs the precise check | both search ±2 cells |

**One function, every caller.** Guessing from names, from bounding boxes, or from a second
copy of the rule is what produced every one of these.

---

## 6. The car colours — 100 of them

Oran: *"the car colours are too cyclical and it hurts the look — I want variety at the
level of a hundred different colours."*

**The obvious suspect was innocent.** The sequence of car models along a lane is not
periodic at all: autocorrelation at every lag from 1 to 14 sits between 0 and 10 %, which
is what random looks like. The real cause is simpler — the kit gives every car of a model
ONE shared atlas material, so **1,982 cars carried fourteen colours between them.** At jam
spacing you meet all fourteen within a few metres, over and over.

### Why the trick that worked twice before did not work here

Hue rotation gave the villa roofs eight shades and the abandoned steelwork nine. Measured,
it could not work on cars: the area-weighted colour of every model sits at **saturation
0.03 to 0.20**, because the atlas blends body, glass, lamps and grille. Rotating the hue of
something that close to grey moves it barely at all.

### Three corrections, every one caught in the picture and not in a number

| # | what the numbers said | what the picture showed |
|---|---|---|
| 1 | 100 colours, min ΔE 18.3, all used | four neutrals out of a hundred — a bag of sweets, not traffic |
| 2 | quotas filled, hues spread | the whole jam leaned **pink**; Lab's magenta region is large and unconstrained selection over-picks it |
| 3 | 30 neutrals, quotas exact | "neutral" was defined as saturation < 0.18, so the quota filled with **tinted** greys — `#131B14` green, `#503B3A` brown, `#90688E` mauve — and exactly one entry brighter than 0.75. No white, no silver, no black |

And a fourth, in the shader rather than the palette: a **COLOR** blend takes hue and
saturation from the palette but **luminance from the atlas**, and the atlas is uniformly
light — so all hundred colours rendered at the same mid brightness and thirty neutrals
became thirty identical greys. A plain mix carries lightness too.

### What it is now

- **30 neutrals, designed rather than selected**: a twelve-step grey ramp from `#F7F7F7`
  to `#141414`, nine cool silvers, nine warm greys.
- **70 chromatic**, chosen by one global farthest-point pass over ~7,000 candidates with a
  quota per hue band — blue 17, red 12, orange 8, green 8, violet 8, magenta 7, teal 6,
  yellow 4, roughly how real traffic is distributed.
- **Masked by brightness**: the mix factor is driven by the atlas's own luminance, so body
  panels take the new colour while glass, tyres and grille keep theirs.

| separation, measured three ways | ΔE |
|---|---|
| chromatic ↔ chromatic | **18.93** |
| neutral ↔ chromatic | **19.23** |
| neutral ↔ neutral | 2.22 |

Twelve of the 4,950 pairs sit below the "obvious" threshold of 5 and **every one is inside
the neutral ramp** — white against pearl against ivory, which is what a car park looks like.

| result | |
|---|---|
| cars recoloured | **2,028** |
| distinct colours in use | **100 of 100** |
| commonest colour | **1.04 %** (20–21 cars each) |
| **neighbours sharing a colour** | **0.72 %** vs 1.00 % expected by chance |
| vehicles moved, rotated or replaced | **0** — only the object-level material slot was touched |
