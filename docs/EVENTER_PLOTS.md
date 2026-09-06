# EVENTER — the villa plots, revision 2. Plan for approval

Ten notes from Oran on the first villa pass. Measured before planning: **8 houses overlap
another element** (up to 55.9 m² each) and **9 plants sit inside a court** — including an
oak in the middle of a tennis court, exactly the one he spotted.

## 0. One root cause behind six of the ten notes

Every element is drawn at a **hard-coded offset** in the plot: drive at u 2.5–7.5, pool at
w−15, court centred, house at 0.34w. Nothing knows about anything else. So a wide house
lands on the tennis court, the drive runs under the house, and a scattered tree is placed
in a rectangle nobody told it about.

**The fix is one mechanism, not six patches: an occupancy map per plot.** Elements are
placed in priority order, each reserves its own footprint plus a clearance, and nothing is
placed where something already is — the same largest-first discipline that fixed MEDCOIN's
belt packing.

```
house  →  drive (derived from the house)  →  court  →  pool
       →  furniture  →  parked cars  →  people  →  planting  →  balls
```

That alone settles notes 3, 6 and 9, and is what makes 7 and 8 possible at all.

---

## 1. Taller walls where a plot faces a motorway

Today: eight 3.0 m segments, only at the four corridor crossings.

**Change:** every plot side that faces a motorway corridor gets a **5.0 m** wall — a noise
wall, tall enough to read as protecting the house behind it. The collector ring keeps no
wall: it is a quiet residential street and a barrier there would look like a motorway
shoulder dropped into a suburb.

*Test:* every plot within 25 m of a motorway corridor carries a ≥5 m wall on the facing
side. 0 gaps.

## 2. Pool variety — size, shape and shade

| | range |
|---|---|
| size | 5×3 m to 14×7 m, **scaled to the plot's free rear area** |
| shape | rectangle · L-shape · octagon · long lap pool |
| water | **5 shades of blue**, from pale turquoise to deep pool blue |

Generated rather than taken from the kit, because the kit has one pool at one size and
Oran asked for exactly the three things a single model cannot give.

*Test:* ≥4 shapes used, ≥5 shades, largest area ≥2.5× the smallest, no shade over 30 %.

## 3 & 4. House size, colour, placement and orientation

Real variety needs the house to change on **four** axes, not one:

| axis | today | **revision 2** |
|---|---|---|
| footprint | 15–19 m, one band | **11–30 m, four size classes** |
| rotation | all parallel to the road | **±20° jitter, and one in five turned 90°** |
| setback | fixed 9 m | **6–14 m** |
| position along the frontage | fixed 0.34 w | **varies with the plot's free space** |
| colour | 8 shades | 8 shades, **no two neighbours alike** |

**The size class is constrained by what else is on the plot, and this was measured.** A
37 m deep plot cannot hold a 30 m house *and* a tennis court: the house is ~18 m deep, and
11 m of court plus margins does not fit in the 11 m left.

| plot | house footprint | why |
|---|---|---|
| estate, tennis court | ≤ 19 m | the court needs 14 m of the rear |
| villa, basketball | ≤ 24 m | a half-court needs 10 m |
| villa, pool only | ≤ **30 m** | nothing else competes for the rear |

*Test:* largest footprint ≥ 2× the smallest; ≥ 6 distinct rotations; no two adjacent plots
share a house type or a shade.

## 5. Basketball courts sized to the plot

| court | size | goes on |
|---|---|---|
| full | 28 × 15 m | only the widest plots |
| half | 15 × 14 m | a normal villa |
| practice pad | 10 × 8 m | a plot whose rear is already busy |

Chosen from the **free rear area after the house and pool are placed** — which is what
"built according to the size of the villa" has to mean.

*Test:* ≥ 3 distinct court sizes present.

## 6. The drives

Today a drive is a fixed rectangle at u 2.5–7.5, and the house is placed independently —
so most of them run under the house or miss it.

**Change:** the drive is **derived from the house after the house is placed**. It runs from
a real gate in the front fence to the house's front face, and its width follows the plot.

*Test:* every drive touches the frontage at one end and the house at the other; 0 drives
crossing any other element.

## 7 & 8. Populating the plots

**≥ 80 % of plots populated, each at a random 60–100 % of its own capacity** — capacity
being how many objects its free area can hold at a sensible spacing.

| element | kit | count |
|---|---|---|
| garden trees, bushes, planters | nature-kit, lowpoly-city | ~9 per plot |
| parked cars | car-kit, **50 models** | 1–3 per plot |
| people | blocky + mini characters, **44 models** | 1–4 per plot |
| garden furniture, loungers, tables | furniture-kit, lowpoly-city | 2–5 per plot |
| balls | generated spheres | 0–3 per plot |

Roughly **500–650 objects across the 28 plots**, and every one placed through the occupancy
map, so none of them can land on a court, a pool, a drive or a house.

*Test:* ≥ 80 % of plots populated; fill fractions actually spread across 60–100 %; per
category ≥ 8 distinct models and no model over 15 % of its category.

## 9. Nothing inside a court but players and a ball

*Test:* for every court rectangle, the only objects inside it are characters or balls.
**0 exceptions** — this is the one Oran caught by eye and it should never have needed to be.

## 10. Re-verifying the five faults from the last pass

| fault | re-check |
|---|---|
| pool coping covering the water | count visible water faces per pool > 0 |
| 4 of 21 house types used | distinct house types = 21 |
| magenta roofs (Hue centred at 0.0 not 0.5) | every tint hue within 0.34–0.58 |
| houses left with no material | 0 houses with an empty material slot |
| workbench MATERIAL mode read as a texture fault | all judging renders in Cycles or TEXTURE mode |

---

## The one thing worth Oran's decision

Object count. Populating the plots properly adds **~600 objects**, on top of the 5,132 in
the planting belt. That is comfortable now, but the abandoned ground (~570), the 2,000
vehicles and the 320 people are still to come. Total heads toward **~9,000 objects and
~1.2 M triangles** — still fine for Cycles at this plate size, but worth saying out loud
before it is built rather than after.
