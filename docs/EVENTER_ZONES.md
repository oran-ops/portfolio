# EVENTER — the four rings. Plan for approval, 2026-08-26

Oran marked three zones on the plan view and asked for this to be planned properly before
any of it is built. This is that plan. Nothing below is built yet.

> **red** — the villas · **yellow** — everything we planned for under the interchange ·
> **blue** — a heavy planting belt separating the under-interchange zone from the villas
> ("the road is a separator too")

## 1. What changes from the previous plan

| | before | **now** |
|---|---|---|
| villas | both strips, inside **and** outside the collector ring | **outside only** |
| the inner strip (37 m) | villa plots | **planting belt** |
| separation between the abandoned ground and the villas | the ring road alone | **planting belt + ring road**, 58 m of it |
| plot count | ~49 | **29** |
| average plot | ~1,000 m² | **1,370 m²** |

**The cost is stated plainly: halving the buildable land halves the plot count.** Twenty-nine
instead of forty-nine. What is bought with it is exactly what Oran asked for — every plot is
bigger, and there is a real, deep green buffer instead of villas sitting under a viaduct.

## 2. The four rings, measured

Everything here is a square centred on (400, 370). Depths are per side.

| ring | from | to | depth | area |
|---|---|---|---|---|
| **YELLOW** abandoned ground | 0 | 125 m | 125 m | 62,500 m² |
| **BLUE** planting belt | 125 m | 162 m | **37.0 m** | 42,476 m² |
| *(road)* collector ring | 162 m | 183 m | 21.0 m | 28,980 m² |
| **RED** villas | 183 m | 220 m | **37.0 m** | 59,644 m² |
| | | | | **193,600 m²** = the 440 m square |

Cross-section, from the middle of the map outward:

```
 interchange           planting          road            villas         country
|<--- 125 m --->|<--- 37 m --->|<-- 21 m -->|<--- 37 m --->|
|   brown earth |  dense trees | carriageway|  plots       |   grass
|   abandoned   |  + undergrowth  + kerbs   |  + hedges    |
|   ------------|--------------|------------|--------------|-----------
                 ^ tall at this edge, low at the other      ^ city boundary
```

## 3. RED — the villas

**Plots front the collector ring** and run the full 37 m back to the city boundary.

Frontage available: the ring's outer perimeter is 1,464 m, less 380 m where the L1 and L2
corridors cross it (their width plus a 10 m margin either side) = **1,084 m**.

| plot type | n | frontage | plot | what is on it |
|---|---|---|---|---|
| **estate** | 8 | 48 m | 1,776 m² | house, pool, **tennis court**, lawn, drive |
| **villa** | 10 | 36 m | 1,332 m² | house, pool, **basketball half-court**, lawn, drive |
| **villa** | 11 | 30 m | 1,110 m² | house, pool, lawn, drive |
| **total** | **29** | | **1,074 m** of 1,084 | |

**The tennis court fits, and it was checked rather than assumed.** With the long axis along
the frontage: 18.3 m of court and run-off + 12.0 m of house + 6.0 m of margins = 36.3 m in a
37 m strip. Turned the other way it does not fit, so every court is laid parallel to the road.

The strip is cut into **12 blocks** by the two motorway corridors — four corners and eight
half-sides. Plots are laid out per block, so no plot is ever crossed by a road.

There are no pool, tennis or basketball assets in any of the forty kits. They are **generated**
— a basin, a coloured court, painted lines — the same way the lane markings were.

## 4. BLUE — the planting belt

37 m deep, 42,476 m² gross, **~31,000 m² plantable** once the ground under the elevated decks
is excluded.

| | density | count |
|---|---|---|
| canopy trees | 1 per 30 m² | **1,030** |
| understorey bushes | 1 per 15 m² | **2,060** |
| flower and grass clumps | 1 per 25 m² | **1,240** |
| | | **4,330 objects** |

At 1 tree per 30 m² with a 6 m canopy, coverage is ~94 % — it reads as **solid woodland from
above**, which is what "really full" has to mean at 4 px/m.

**It is layered, not uniform.** Tall trees on the inner edge, where the job is to screen the
abandoned ground; low planting on the outer edge, so the villas look onto a garden rather
than a wall. Six tree species from the nature kit, three colour variants each, so the mass
does not repeat visibly.

## 5. The wall

With the planting belt doing the separating, the wall has one job left: **bounding each villa
block where it meets a motorway corridor.** Hedge on the plot side, wall on the road side,
2.2 m. No plot is left open to a viaduct.

## 6. YELLOW — unchanged

The abandoned ground under the interchange, as planned: ~570 elements — derelict buildings,
abandoned vehicles, barrels, dumped tyres, bare fencing, the occasional food stall — at ≥25 %
fill, with **4.2 m clear south-west of every pier** so the pier shadows stay readable.

## 7. Acceptance tests

| stage | test |
|---|---|
| planting belt | 0 objects on a road or in the villa strip; canopy coverage ≥ 90 %; ≥ 6 species |
| villa plots | 0 plots crossed by a road; every court and pool inside its own plot; 29 plots |
| wall | every villa block boundary facing a corridor is walled — 0 gaps |
| all | the whole 440 m square accounted for: no unclaimed ground |

## 8. One choice worth putting back to Oran

The ring sits in the middle of the band, which splits it 37/37. Moving the ring **outward**
to a centreline of 240 would give:

| | villas | planting |
|---|---|---|
| as planned | 37.0 m | 37.0 m |
| ring moved out | **49.5 m** | 24.5 m |

Deeper plots — a tennis court would fit comfortably rather than by 0.7 m — at the cost of a
third of the planting belt. **Default is 37/37 unless Oran says otherwise.**
