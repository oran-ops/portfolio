# EVENTER — the plan, revision 2, 2026-08-26

Revised after Oran's review. Changes from revision 1: **a bigger and genuinely more complex
interchange**, the **abandoned ground beneath it**, and a **ring of luxury villas** instead of
generic mid-rise. Written to the same standard as `MEDCOIN_PLAN.md`.

**MEDCOIN is the case study.** It was built fast and almost fault-free because every stage had a
numeric acceptance test that ran before anything was shown. Same method here.

---

## 1. What changed, and why

Oran's review, in his words and what each one forces:

| he said | what it changes |
|---|---|
| "I couldn't really understand the plan" | a simple 2D line drawing, plan and section |
| "4 rings — is that enough? I want something really significant" | **the interchange is upgraded** — see section 3 |
| under the interchange: brown earth, abandoned, barrels, tyres, bare fences | **a whole new zone**, section 6 |
| ring city: luxury villas, pools, tennis courts, basketball courts | **the ring is redesigned**, section 7 |
| variety in the cars matters most — it is a jam | section 8 |
| all cars in a lane the same way, as in MEDCOIN | already fixed in the generator |
| **crash barriers beside every road** | section 5.5 — a new global rule |
| sun at 75°, as the other maps | unchanged: 75°, azimuth 135°, energy 0.8835 |

---

## 2. The square grows to 440 m

The upgrade needs room, and so do the villas. **440 × 440 instead of 372 × 372.**

| | 372 m *(as MEDCOIN)* | **440 m** |
|---|---|---|
| interchange footprint | 210 m | **250 m** |
| ring depth each side | 81 m | **95 m** |
| deepest villa plot that fits | 60 m — nothing over | **60 m plot + 12 m street, with room** |

**Why it is justified:** EVENTER's subject is the largest single structure on the whole map. A
372 m square forces a choice between a significant interchange and villas with tennis courts, and
Oran asked for both. 440 m is 40 % more area and buys both.

**It does break the "each city is 15 % of the map" rule from `MAP_VISION`.** Flagging it rather
than hiding it — say the word and the interchange shrinks back instead.

---

## 3. The interchange upgrade — what was tested and what was chosen

### A full four-level stack does NOT fit. Measured.

In a true stack every left turn gets its own flyover at its own level. The fourth level sits at
26 m, so its ramp must climb from 6.5 to 26 and come back down to 13:

| | at 6.5 % grade | at 7 % grade |
|---|---|---|
| L1 → L3 → L2 flyover | 300 m of ramp | 279 m |
| **a fourth level** | **500 m** | **464 m** |
| available inside the footprint | **250 m** | 250 m |

A fourth level needs twice the room there is. Making the grade steeper to force it in would give a
1-in-8 ramp that reads as a ski jump.

### Chosen: a four-level HYBRID — flyovers and loops together

| level | z | carries |
|---|---|---|
| **L0** | 0.14 | the abandoned ground, the collector ring |
| **L1** | **6.5 m** | east–west through route, 8 lanes, **+ 2 collector-distributor roads** |
| **L2** | **13.0 m** | north–south through route, 8 lanes, **+ 2 collector-distributor roads** |
| **L3** | **19.5 m** | **two direct flyovers** — the E→N and W→S left turns |
| loops | between L1 and L2 | the other two left turns, N→W and S→E |

Clear height at every level: **5.6 m** (6.5 spacing − 0.9 deck), above the 5.0 m standard.

**Why a hybrid beats either pure form.** A pure stack needs a level it cannot have. A pure
cloverleaf is four identical loops — which is exactly the "4 rings" Oran found underwhelming.
Mixing them gives **two sweeping high flyovers crossing above two tight loops**, at four different
heights. That reads as complex from above because the ribbons genuinely are at different heights,
not because there are more of the same thing.

### Collector-distributor roads — the cheapest complexity there is

A C-D road is a parallel side road that collects ramp traffic before merging it into the main
carriageway. Four of them — one each side of each route — add **four more long parallel ribbons**
and the short braided links between them, for about 22 m of extra width per side. Real big
interchanges look dense because of C-D roads more than because of levels.

### The count

| | revision 1 | **revision 2** |
|---|---|---|
| levels | 3 | **4** |
| separate road ribbons | 14 | **18** |
| lane-metres in the interchange | 7,624 | **10,876** |

---

## 4. The 2,000 cars, re-checked against the bigger interchange

| where | lane-metres | density | cars |
|---|---|---|---|
| L1 deck, 440 m × 8 lanes | 3,520 | jam | |
| L2 deck, 440 m × 8 lanes | 3,520 | jam | |
| 2 loops, 198 m each | 396 | jam | |
| 2 flyovers at L3, 280 m each | 560 | jam | |
| 4 collector-distributor roads | 2,000 | jam | |
| 4 right-turn ramps + 4 city ramps | 880 | jam | |
| **interchange subtotal** | **10,876** | **1 per 6.5 m** | **1,673** |
| villa streets, 2,622 m × 2 lanes | 5,244 | 1 per 25 m | 210 |
| parked on driveways | — | — | 120 |
| | | **TOTAL** | **2,003** |

**2,003 against Oran's ~2,000 customers.** The bigger interchange holds more jam, and the quiet
villa ring holds fewer cars, and the two changes cancel almost exactly.

**The jam wins if they ever conflict.** The interchange is already at jam spacing; if it needs to
look fuller the lever is the ring, never the interchange.

---

## 5. Road construction rules — global

### 5.1 Section, every elevated road

| element | width |
|---|---|
| 4 lanes each way at 3.5 m | 28.0 m |
| central reservation | 2.0 m |
| shoulders | 2.0 m |
| **carriageway** | **32.0 m** |
| deck thickness | 0.9 m |

### 5.2 Crash barriers — Oran's rule, applied everywhere

**Every road gets a barrier down both edges, following the exact boundary of its own carriageway.**
Not a decoration and not optional:

| road | barrier |
|---|---|
| elevated deck, outer edge | solid concrete parapet, 0.9 m |
| elevated deck, median | double-sided barrier, 0.8 m |
| ramp and loop, both edges | parapet, 0.9 m — a ramp is the one place a car could leave the map |
| collector ring and villa streets, at grade | steel guardrail, 0.75 m, on posts every 4 m |

**Test:** every metre of every elevated edge carries a barrier — 0 gaps. Sample the edge every
2 m and require a barrier within 0.3 m. A missing 6 m of parapet on a loop is invisible in plan
and obvious the moment the camera drops to street level.

### 5.3 Piers, soffits

- **Piers generated, not placed** — a tapered box every 18 m, height read from the deck above it.
- **Soffits closed** — an isometric camera sees the underside; a single-plane deck reads as paper.
- Piers under L3 are ~18.6 m tall and are the tallest structures in the city.

### 5.4 Driving direction

Right-hand traffic. Loops and ramps are one-way, so their direction is fixed by the movement they
serve. Both MEDCOIN faults are already fixed in the generator and carry over:

1. **The front is at minus the length axis** on all 38 vehicle models.
2. **Parked cars take the heading of the lane beside them.**

`verify_traffic_direction` extends to judge a ramp against its own 3D tangent.

---

## 6. Under the interchange — the abandoned ground

Oran: brown earth, not OASIS green. Abandoned businesses and buildings, abandoned vehicles,
barrels, dumped tyres, bare fences, the occasional food business. He was explicit that he is
naming the **elements**, not asking for a mood.

**Why it must be planned properly:** from above the decks hide most of it — but the moment the
camera drops to street level the whole area is visible. It also gives the deck shadows something
to fall on, which is what sells the height.

### Ground

| surface | where |
|---|---|
| **bare brown earth** `#7A6F60` | the majority — this is the defining colour |
| cracked asphalt, patched | old service roads and yards |
| gravel and rubble | around the pier bases |
| **no green** | not one blade — that belongs to OASIS |

### Elements — all present in the kits, none needs downloading

| element | source | count |
|---|---|---|
| dumped tyres and wheels | 15 `wheel-*`, `debris-tire` | 90 |
| car debris — bumpers, doors, panels, axles | 14 `debris-*` | 120 |
| **abandoned vehicles**, rusted and desaturated | the 38 vehicle models, rust tint | 45 |
| barrels and drums | `food-kit/barrel` | 70 |
| dumpsters, waste containers, bins | `dumpster`, `waste-container-*`, `trashcan` | 40 |
| crates, pallets, cardboard | `crate`, `pallet`, `cardboardBox*` | 85 |
| **bare fencing**, leaning and broken | `construction-fence`, `fence-*` | 75 |
| abandoned buildings and lock-ups | low `building-*` with a grey/rust tint | 22 |
| **food businesses** — the occupied ones | `food-kit` frontages | 6 |
| tents and campfires | 5 `tent*`, 4 `campfire_*` | 18 |
| **TOTAL** | | **~570** |

### Density — the number Oran actually specified

He asked for "not as loaded as MEDCOIN, but as loaded as the OASIS build level."

| | objects per m² of ground |
|---|---|
| OASIS, excluding vegetation | 1 per 130 m² |
| **EVENTER under-deck, target** | **1 per 79 m²** |
| MEDCOIN industry belt | 1 per 21 m² |

**~570 elements over ~45,000 m² of open ground, about 25 % ground fill** — against MEDCOIN's
47 %. Denser than OASIS, half of MEDCOIN, which is where he put it.

**Acceptance:** 0 green pixels; ≥ 25 % ground fill; every element type present in every quadrant;
0 elements standing inside a pier or under a deck with less than 2 m of headroom.

---

## 7. The ring city — luxury villas

> **SUPERSEDED IN PART by section 21.** The third audit found that both elevated routes
> cross this ring, so villas as laid out here would sit under a viaduct. The land is now
> divided into 4 corner blocks (estates), 8 side blocks (villas) and 4 road corridors
> (businesses). The plot mix and the per-plot composition below still stand.

Oran: very large luxury private houses, lawns, pools, tennis courts, basketball courts, all inside
the plots. Rich people's houses. Every plot needs designing.

### The plot mix — checked against the 95 m ring

A tennis court is **36 × 18 m** including runback, so a plot with one needs at least 40 m in one
direction. That single number sizes the whole ring.

| plot type | size | area | count | contents |
|---|---|---|---|---|
| **estate** | 45 × 60 m | 2,700 m² | **15** | main house + guest house + garage, pool, **tennis court**, lawn, mature trees, gated drive |
| **villa** | 32 × 45 m | 1,440 m² | **25** | house + garage, **pool**, lawn, trees, drive |
| **house** | 25 × 38 m | 950 m² | **20** | house, lawn, trees, drive; some with a **basketball half-court** |
| | | **95,500 m²** | **60** | |

Usable ring area after streets and verges (75 % of 131,100) is **98,325 m²** — **it fits**, with
2,800 m² spare.

### What is on a plot, and how it is placed

Not scattered. Every plot is composed, and the composition is the same everywhere so the street
reads as one neighbourhood:

1. **Frontage**: gated drive off the street, `driveway-long`, wall or `fence-*` along the boundary.
2. **The house set back** from the street by 8–14 m, front lawn between.
3. **Behind the house**: the private ground — pool, court, terrace.
4. **Boundary planting**: `tree-large` along the side boundaries, which is what makes a rich
   suburb read as rich from above — mature trees, not saplings.

**Luxury comes from the plot, not the building.** The kit's houses are 10–11 m across — a normal
suburban house. Scaling one to 20 m makes an ugly giant. Instead an estate carries **two or three
buildings** — main house, guest house, garage block — arranged around the ground. That is what a
large property actually looks like from above, and it uses the models at their honest size.

### Assets — all present except one

| need | source |
|---|---|
| houses, 21 types | `city-kit-suburban/building-type-a…u` |
| drives, paths | `driveway-long/short`, `path-long/short`, `path-stones-*` |
| boundary walls and fences, 9 types | `city-kit-suburban/fence-*` |
| **pools** | `lowpoly-city/swimming-pool-1h`, scaled ×1.8 → 9.7 × 7.9 m |
| **basketball** | `lowpoly-city/basketball-net-1h` on a generated painted court |
| trees, planters | `tree-large`, `tree-small`, `planter` |
| **tennis courts — NO MODEL EXISTS** | **generated**: a coloured 36 × 18 m quad, white lines, a low net box, surrounding fence from `fence-*`. The same `Mesh`/`_q` code that draws road markings |

**Green is correct here** and only here: lawns, trees, and the courts. It is the deliberate
contrast with the brown ground under the interchange 95 m away — wealth on the outside, dereliction
underneath. That contrast is the picture of this city.

---

## 8. Car variety — the thing the eye reads most

Oran: it is a jam, the roads and the cars are the point, so **how the cars differ from one another
matters most**.

| axis | how |
|---|---|
| **model** | all 38, and no model twice within 5 cars in the same lane |
| **colour** | per-instance tint, as MEDCOIN's buildings — 15 variants per palette texture |
| **class mix** | saloons, hatchbacks, vans, taxis, police, ambulances, buses, articulated lorries |
| **lane discipline** | lorries and buses weighted to the outer lanes, sports cars to the inner |
| **spacing** | jitter 5.8–7.4 m so the queue is not a comb |
| **stance** | ±2° yaw jitter — a real stopped queue is never perfectly aligned |
| **the abandoned ones** | 45 rusted, desaturated, some without wheels, under the deck |

**Test:** ≥ 30 distinct models used; no model repeated within 5 cars in a lane; distinct hue count
≥ 12 in any 60 m crop of the jam.

---

## 9. Layout

> **SUPERSEDED by section 21** — the ring divides into corners, sides and road corridors.

| zone | size | share |
|---|---|---|
| **INTERCHANGE**, four levels | 250 × 250 centred | 32.3 % |
| **UNDER-DECK GROUND**, abandoned | inside the footprint, at grade | — |
| **RING CITY**, 60 luxury plots | a 95 m band on all four sides | 67.7 % |

---

## 10. Build order

| # | stage | acceptance test |
|---|---|---|
| 0 | ground and palette — brown earth inside, villa green outside | 0 green pixels under the deck; 0 brown in the villa ring |
| 1 | villa street grid + collector ring | 0 streets crossing the collector; every junction plated |
| 2 | L1 and L2 decks + 4 C-D roads | deck width 32.0 ± 0.05; **clear height ≥ 5.0 m everywhere** |
| 3 | 2 loops + 2 L3 flyovers + 8 ramps | every join within **0.05 m and 2°**; grade ≤ 7 %; **0 ramp-to-ramp intersections in 3D** |
| 4 | piers, soffits, **barriers** | every pier top meets its soffit within 0.02 m; **0 gaps in any barrier**; 0 piers standing in a road |
| 5 | LOD vehicle set | 38 models decimated; top-down silhouette within 5 %; ≤ 450 tris |
| 6 | **the jam — 2,000 vehicles** | exactly 2,000; **0 wrong-way; 0 mixed lanes**; 0 cars through a barrier; every car raycast onto its own deck |
| 7 | **60 villa plots** | every plot has drive + house + boundary; 0 overlaps; every estate has a tennis court that fits; pools not inside houses |
| 8 | **under-deck abandoned ground** | ≥ 25 % fill; ~570 elements; every type in every quadrant; 0 elements inside a pier |
| 9 | signage, gantries, lighting | every gantry spans its carriageway; 0 clipping a deck above |
| 10 | people and planting | people on pavements and in gardens only; **0 people on the elevated decks** |
| 11 | dead-space sweep | ≤ 2 empty samples in the whole square |

### The tests that are new here

- **Clear height** — sample both surfaces on a grid, take the minimum gap.
- **3D intersection** — a bounding box is exact only for axis-aligned geometry, and every ramp is
  curved *and* inclined. Triangle-level tests from the start.
- **Cars on a graded deck** — raycast each car onto the deck below it, the method that placed 547
  roof props on MEDCOIN with zero floating. A car placed at a flat z on a 7 % ramp floats or sinks.
- **Barrier continuity** — sample every road edge every 2 m.

---

## 11. Shadows — at the world sun, 75°, azimuth 135°

Light direction measured from the built scene: **(−0.183, −0.183, −0.966)**. Shadows fall
**south-west**, offset **0.2679 × height**.

| object | height | shadow offset |
|---|---|---|
| L1 deck | 6.5 m | 1.74 m |
| L2 deck | 13.0 m | 3.48 m |
| **L3 flyover** | **19.5 m** | **5.22 m** |
| tallest pier | 18.6 m | 4.98 m |

**The decks are 32 m wide and the largest shadow offset is 5.22 m**, so every shadow falls *under*
its own deck. Elevated road reads as **above and attached**, never floating — the same rule that
governed the trees in `MEDCOIN_PLAN` 2e.

**This is why the ground beneath must be built.** Four levels of shadow falling on bare nothing
would waste the strongest depth cue on the map.

---

## 12. Lessons carried in from OASIS and MEDCOIN

1. Measure scale per **file**, not per kit.
2. Apply a plausibility range to every imported model — it caught five wrong ones.
3. **A missing texture renders magenta**, so it looks like a design choice. Audit `bpy.data.images`.
4. Donor models smuggle in green — `nature-kit` uses a material named `grass` on rocks and trees.
5. **Check `input.links` before trusting a socket default.** OASIS's grass is ColorRamp-driven.
6. Vehicles need **two** things measured: the length axis, and which end is the front.
7. Parked cars take the heading of the lane beside them.
8. A junction is as wide as the road, not a point.
9. Pack largest-first, or small items win every contested spot.
10. Test a rule only where it applies — testing prisms for shadow detachment gave 3,093 false fails.
11. Read `matrix_world` only after `view_layer.update()`.
12. Never verify placement from `bound_box + location`.
13. Judge each object from itself, never by zipping two lists.
14. A pixel test as well as a geometry test, every time.
15. A test that cries wolf on a clean build is worse than no test.

---

## 13. Road connections

| city | enters | leaves |
|---|---|---|
| OASIS *(built)* | west | east |
| MEDCOIN *(built)* | south | east |
| **EVENTER** | **west, on L1** | **east, on L1** |

**Recommendation stands: normalise all four cities to enter west and leave east.** One edit to
MEDCOIN's `main_path()`, already done safely twice with `verify_main_clearance` to prove it.

EVENTER's **L1 deck is the through route** — the road arrives from OASIS, climbs onto the
interchange, crosses it, and leaves toward MEDCOIN. The traveller's own road is the one that flies
over everything, which is the right emphasis for the city whose subject is the junction.

---

## 14. Approved by Oran, 2026-08-26

- **The 440 m square** — approved.
- **The rail line** — approved. Specified in section 17.

---

# THE DEEP AUDIT — run 2026-08-26, before any geometry

Oran asked for the same hard self-check that was run before MEDCOIN was built: every ratio
recomputed, every system re-read, and an honest search for what is missing. **Twelve gaps were
found and all twelve are closed below.** The arithmetic was computed, not asserted.

---

## 15. Audit part 1 — the ratios

### 15.1 Does the area budget close to 100 %?

| | m² | share |
|---|---|---|
| INTERCHANGE footprint, 250 × 250 | 62,500 | 32.3 % |
| collector ring road, 22 m wide | 22,000 | 11.4 % |
| villa streets, 12 m wide | 13,056 | 6.7 % |
| plots — villas and businesses | 96,044 | 49.6 % |
| **SUM** | **193,600** | **100.0 %** |

**It closes exactly.** The 95 m ring resolves as **22 m collector + 12 m street + 61 m plot
depth**, so a villa fronts a quiet street and backs onto open country — which is what a
sought-after plot actually does.

### 15.2 Do the plots fit, with businesses added?

| plot type | size | count | area |
|---|---|---|---|
| **estate** — house + guest house + garage, pool, **tennis court** | 45 × 60 | **12** | 32,400 |
| **villa** — house + garage, **pool** | 32 × 45 | **21** | 30,240 |
| **house** — house, lawn, some with a **basketball half-court** | 25 × 38 | **16** | 15,200 |
| villa land used | | **49** | **77,840** |
| villa land available | | | 80,044 — **fits** |
| **businesses**, on the collector frontage | ~571 m² each | **28** | 16,000 |

**77 plots in total.** 49 villas and 28 businesses.

### 15.3 Every ratio, against the two built cities

| | OASIS *(built)* | MEDCOIN *(built)* | **EVENTER** |
|---|---|---|---|
| area m² | 138,384 | 138,384 | **193,600** |
| buildings | 151 | 408 | **168** |
| m² per building | 916 | 339 | **1,155** |
| vehicles | 190 | 522 | **2,000** |
| **m² per vehicle** | 728 | 265 | **97** |
| people | 298 | 1,200 | **320** |
| **m² per person** | 464 | 115 | **605** |
| props and elements | 719 | 2,736 | **890** |
| planting objects | 11,492 | 169 | **481** |
| vehicles per building | 1.3 | 1.3 | **11.9** |
| **people per vehicle** | 1.57 | 2.30 | **0.16** |

**Read the last three rows.** EVENTER has the **fewest people per m²** and the **most vehicles per
m²** of the three, and nearly **twelve vehicles for every building**. That is not an accident of
the numbers — it is the city. A motorway interchange ringed by private estates has almost no
pedestrians and enormous traffic. **It is the exact inverse of MEDCOIN**, where 2.3 people stood
for every car.

---

## 16. Audit part 2 — the six systems of `MAP_ANALYSIS`, re-read

### 1.1 Buildings form BLOCKS, not objects — **PARTIAL, and deliberately**

`MAP_ANALYSIS` warns: *"My build places detached objects along a line with grass between them.
That is a suburb of identical villas, and it is why it reads as elements on a map."*

**Oran has now asked for exactly that** — detached luxury villas with lawns. The tension is real
and must be named rather than ignored. It resolves three ways:

1. **A plot is composed, not scattered.** Gate → wall → drive → house set back 8–14 m → private
   ground behind → boundary planting. Five elements in a fixed relationship. That is a *composition*,
   which is what 1.1 is actually asking for; what it warns against is objects dropped on grass.
2. **The 28 businesses DO form blocks**, with party walls and a continuous frontage on the
   collector ring. The city has both kinds of fabric, in the right places.
3. **The abandoned lock-ups under the deck** form broken terraces — blocks with pieces missing.

### 1.2 The pavement is a real object — **WAS A GAP, now closed**

MEDCOIN's first audit found *"THERE IS NO PAVEMENT — the biggest finding."* The EVENTER plan had
not given a street section at all. **Closed:**

| road | section |
|---|---|
| **collector ring** | 2 lanes each way 14.0 · kerb 0.5 · **pavement 3.0** · both sides → **22.0 m** |
| **villa street** | 2 lanes 7.0 · kerb 0.5 · **pavement 2.0** · both sides → **12.0 m** |
| **service road**, under the deck | 6.0 m, no kerb, no pavement — a yard road, as the MEDCOIN belt |

Everything on a street stands **on the pavement**: people, lamps, signs, bins, trees in pits.

### 1.3 Building types distinguishable at a glance — **WAS A GAP, now closed**

The ring was "luxury villas" — one type. A city needs types that cannot be mistaken. **Closed —
each with the five signatures 1.3 demands:**

| type | footprint | height | roof | façade | surroundings |
|---|---|---|---|---|---|
| **Detached villa** | small, square | 1–2 floors | **pitched, chimney** | few windows, porch, garage door | **lawn, wall, gated drive, pool, court** |
| **Retail podium** *(the 28)* | wide, shallow | 1–2 floors | flat with plant | **continuous glazed shopfront + signage band** | **forecourt, parking, fuel canopy, awnings** |
| **Abandoned lock-up** | wide, low | 1 floor | shallow, damaged | **blind walls, boarded openings, roller doors** | **rubble, bare fence, dumped tyres** |

Three types, three roofs, three surroundings. A villa cannot be mistaken for a lock-up.

### 1.4 The life layer is systematic, not sprinkled — **WAS A GAP, now closed**

No people count, no spacing rules had been given. **Closed, by rule against the street:**

| item | rule | count |
|---|---|---|
| **people** | 1 per 9 m on the collector frontage; 1 per 45 m on villa streets; a few under the deck; **NONE on the elevated decks** | **320** |
| street trees | 1 per 15 m on the collector; boundary planting on every plot | **481 planting objects** |
| lamp posts | 1 per 27 m, alternating sides, on the collector and villa streets | ~130 |
| **motorway lighting masts** | 12 m masts, 1 per 40 m, on the outer shoulder of every elevated deck | ~55 |
| **gantry signs** | over every diverge, 300 m and 100 m in advance | 14 |
| traffic signals + painted crossings | every collector-ring junction | 12 junctions |
| rooftop plant | on every flat roof — the 28 businesses | 28 |

**The 50 m test** from 1.4 — *"pick any 50 m of street; a reference has 8–15 objects on it"*:
collector ring ≈ 12, villa street ≈ 8, under-deck service road ≈ 7.6. **All pass.**

### 1.5 Colour is natural, saturated only in small things — **WAS A GAP, now closed**

Never stated. **Closed. EVENTER's colour source is THE CARS** — as MEDCOIN's was its containers
and OASIS's was its roofs.

| surface | policy |
|---|---|
| villas | natural render, brick, tile, timber — per-instance tone variation, no brand colour |
| businesses | neutral walls; **saturated only in the signage band and the awnings** |
| under-deck | brown earth `#7A6F60`, rust, grey concrete, weathered timber |
| elevated roads | asphalt `#3E3F45`, concrete parapets, white markings |
| **the 2,000 cars** | **the whole colour budget of the city** |

### 1.6 One sun, hard shadows — **OK**

75°, azimuth 135°, energy **0.8835** — identical to both built cities, and now measured rather
than derived.

---

## 17. Audit part 3 — the twelve gaps, and how each is closed

### 17.1 The rail line — approved, now specified

The real Judge Pregerson interchange carries the Metro C Line in the median of the I-105. That is
the detail that makes the reference unmistakable.

| | |
|---|---|
| **where** | in **L1's median**, at z = 6.5 m, running the full 440 m east–west |
| **L1 deck grows** | 4 lanes each way 28.0 + **rail median 9.0** + shoulders 2.0 = **39.0 m** |
| **clearance under L2** | soffit 12.10 − rail 6.50 = **5.60 m** |
| a light-rail car at 4.30 m | **fits, 1.30 m spare** |
| **catenary** | **not modelled** — it would clear by only 0.10 m, and at 5.7 px/m an overhead wire is invisible |
| **station** | a 120 m island platform in the median, at the west end of the interchange, with a pedestrian bridge down to the collector ring |
| **trains** | 3 trains of 4–6 coupled units, from `train-kit` |
| assets | `train-kit`, 103 pieces — track, trams, electric city and subway units |

**Scale calibration required.** `train-electric-city-a` at the city-kit ×8 is **13.5 m tall** — a
train the height of a four-storey building. `train-kit` is not on the ×8 convention. **Calibrate
against the track gauge:** measure the rail spacing in `railroad-straight` and scale so it equals
**1.435 m**. This is the per-file lesson from MEDCOIN, and the plausibility gate (a carriage
between 3.5 and 5.0 m tall) rejects anything that fails it.

**Why the station earns its place:** it gives the people layer a reason to exist in a city that
otherwise has almost no pedestrians, and it ties the rail to the collector ring rather than leaving
it as scenery running through.

### 17.2 The z-stack — a clearance rule, not a level list

MEDCOIN fixed **13 flat levels** in advance. EVENTER cannot: ramps vary continuously in z. The
rule changes shape.

| surface | z |
|---|---|
| bare earth | 0.000 |
| gravel, rubble | 0.030 |
| yard plates, forecourts | 0.050 |
| ground asphalt | 0.140 |
| ground markings | 0.152 |
| ground pavement | 0.190 / kerb 0.200 |
| **L1 deck** | **6.500**, markings 6.512, soffit 5.600 |
| **L2 deck** | **13.000**, markings 13.012, soffit 12.100 |
| **L3 deck** | **19.500**, markings 19.512, soffit 18.600 |
| ramps and loops | **continuous** |

**The rule for anything on a slope:** *no two road surfaces may come within 0.30 m of one another
in z wherever they overlap in plan, and any road passing over another must clear it by ≥ 5.0 m.*
Flat coplanar z-fighting is replaced by a **minimum-gap test on a sampled grid** — the same
failure (THE BLACK STRIP) in a form a flat z-list cannot express.

### 17.3 The remaining ten

| gap | closed by |
|---|---|
| **people** — no count | 320, distributed by the 1.4 rules above |
| **businesses** — the brief demands them; the ring was all villas | 28 retail podiums on the collector frontage, forming blocks |
| **street sections** | given in 1.2 above |
| **motorway lighting** | 12 m masts, 1 per 40 m on every deck — ~55 |
| **square edge** | villa garden walls back onto green country; **no perimeter fence** — MEDCOIN needed one because an industrial site has one, an affluent suburb does not |
| **tree count** | 481 planting objects; boundary planting on all 49 plots |
| **camera** | orthographic, the same 54.7° / 45° isometric as `CAM_MED`, ortho_scale 660 to frame a 440 m square, 3200 × 1930 → **4.85 px/m** |
| **parking** | 28 business forecourts; 49 villa drives; no on-street parking in the villa ring — a rich suburb parks off-street |
| **traveller's reading** | the road arrives from OASIS at the **west**, climbs onto L1, crosses, and leaves **east** toward MEDCOIN |
| **polygon budget** | recomputed below |

### 17.4 Polygon budget, recomputed for the 440 m square with the rail

| | triangles |
|---|---|
| 200 cars at full detail | 580,000 |
| 1,800 LOD cars at ~400 | 720,000 |
| 49 villa plots | 392,000 |
| 28 businesses | 70,000 |
| 570 under-deck elements | 228,000 |
| 320 people | 23,040 |
| interchange ribbons, piers, barriers | 50,000 |
| **rail: track, station, 3 trains** | 36,000 |
| street furniture, gantries, lighting masts | 120,000 |
| ground, streets, collector ring | 80,000 |
| tennis and basketball courts | 10,000 |
| **TOTAL** | **2,309,040** |
| MEDCOIN, as actually built | 3,427,746 |
| **headroom** | **1,118,706 — comfortable** |

---

## 18. The build order, revised for everything above

| # | stage | acceptance test |
|---|---|---|
| 0 | ground and palette | 0 green under the deck; 0 brown in the villa ring; area closes to 100 % |
| 1 | collector ring + villa streets, **with kerbs and pavements** | pavement continuous both sides; 0 streets crossing the collector |
| 2 | L1 (39 m, with rail median) and L2 (32 m) decks + 4 C-D roads | width ± 0.05; **clear height ≥ 5.0 m everywhere** |
| 3 | 2 loops + 2 L3 flyovers + 8 ramps | joins within **0.05 m and 2°**; grade ≤ 7 %; **0 ramp-to-ramp intersections in 3D** |
| 4 | piers, soffits, **barriers on every edge** | pier tops meet soffits within 0.02 m; **0 gaps in any barrier**; 0 piers in a road |
| 5 | **rail: calibrate, track, station, trains** | gauge = 1.435 m ± 0.02; carriage height 3.5–5.0 m; **5.6 m clear under L2** |
| 6 | LOD vehicle set | 38 models decimated; silhouette within 5 %; ≤ 450 tris |
| 7 | **the jam — 2,000 vehicles** | exactly 2,000; **0 wrong-way; 0 mixed lanes**; 0 through a barrier; **every car raycast onto its own deck** |
| 8 | **49 villa plots** | every plot has gate + drive + house + boundary; 0 overlaps; every estate's tennis court fits; 0 pools inside houses |
| 9 | **28 businesses** | continuous frontage, party walls; signage band on every unit; forecourt on every unit |
| 10 | **under-deck abandoned ground** | ≥ 25 % fill; ~570 elements; every type in every quadrant; 0 elements inside a pier |
| 11 | signage, gantries, lighting masts | every gantry spans its carriageway; 0 clipping a deck above |
| 12 | people and planting | 320 people, **0 on the elevated decks**; 481 planting objects |
| 13 | dead-space sweep | ≤ 2 empty samples in the whole square |

---

## 19. Audit result

| | |
|---|---|
| area budget | **closes to 100.0 %** |
| plots | 49 villas + 28 businesses — **fit with 2,204 m² spare** |
| cars | **2,003 against a target of 2,000** |
| polygon budget | **2.31 M against MEDCOIN's 3.43 M** |
| the six systems of `MAP_ANALYSIS` | 1 OK, 1 partial-by-design, **4 gaps found and closed** |
| other gaps found | **12, all closed** |
| lessons carried from OASIS and MEDCOIN | **15, listed in section 12** |
| clearances, grades, shadows, turn topology | **computed, not assumed** |

**The plan is ready to build.**

---

# THE THIRD AUDIT — the deep pass, 2026-08-26

Oran asked for this a third time, deeper than the two before, with **the shadow analysed
specifically against the roads**, and an honest account of what his repeated corrections teach.
This is the most important section in the document.

**It found one fault in the layout that would have wasted a whole build**, and one reversal of a
rule I have been carrying since OASIS.

---

## 20. Part 1 — the shadow, analysed against the roads

### 20.1 A reversal I have been carrying since OASIS

Every shadow decision in OASIS and MEDCOIN followed one rule: **a shadow that stays attached to
its object is correct**, because a detached shadow is what makes a tree look as if it floats. That
rule drove the sun from 30° to 68° to 82° and finally to 75°.

**For an elevated road the rule inverts.** A viaduct *is* off the ground. If its shadow falls
entirely beneath it, the eye has no way to tell it from a road painted on the floor. **Here a
visibly detached shadow is the goal, not the fault.**

Applying it, and the answer is uncomfortable:

| deck | height | width | shadow offset | band visible beyond the edge | as % of its own width |
|---|---|---|---|---|---|
| L1 | 6.5 m | 39.0 m | 1.74 m | 1.74 m | **4.5 %** |
| L2 | 13.0 m | 32.0 m | 3.48 m | 3.48 m | **10.9 %** |
| L3 | 19.5 m | 16.0 m | 5.23 m | 5.23 m | 32.7 % |

**The widest deck shows a shadow band only 4.5 % of its own width.** At 75° the deck's own shadow
is a *weak* height cue. Something else has to carry the height, and the plan had not identified
what.

### 20.2 What actually sells the height: the piers

| | height | shadow length | spacing |
|---|---|---|---|
| pier under L1 | 5.6 m | 1.50 m | every 18 m |
| pier under L2 | 12.1 m | **3.24 m** | every 18 m |
| pier under L3 | 18.6 m | **4.98 m** | every 18 m |

A row of shadows 3.24 m long repeating every 18 m is a **rhythm**, and rhythm reads at any scale.
**This is the strongest height cue in the city** — stronger than the decks, stronger than the
soffits.

> **NEW DESIGN RULE, and it is a build constraint, not a note:**
> **keep a 4.2 m clear radius on the SOUTH-WEST side of every pier base.**
> Pile debris against a pier's SW face and its shadow is swallowed, and with it the single best
> proof that the road is in the air. This directly constrains where the 570 abandoned elements may
> be placed — and nothing in the plan said so until now.

### 20.3 Deck-on-deck shadow — the cue nobody planned for

| | offset |
|---|---|
| L2 onto L1 | 1.74 m |
| L3 onto L2 | 1.74 m |
| L3 onto L1 | 3.48 m |
| L1 / L2 / L3 onto the ground | 1.70 / 3.45 / 5.19 m |

A 32 m dark band lying **across another road**, offset 1.74 m, is unmistakable. Four levels means
shadows falling on shadows — **this is EVENTER's signature image**, and it costs nothing: it
happens automatically once the geometry is right. No other city on this map can produce it.

### 20.4 How dark is it under the deck? Measured, not guessed

From the fit made during the sun calibration: **ambient supplies 59.6 %** of the lit ground value.

| | |
|---|---|
| fully shadowed ground, in linear light | 0.596 × lit |
| **in what the eye sees (sRGB)** | **0.806 × lit** |

**The under-deck area renders at 81 % brightness. It is not a black void** — every one of the 570
elements will be clearly visible.

> **The consequence is a design instruction.** The ground under the interchange is **uniformly**
> lit: every part of it sits in the same shadow, so there is no light gradient anywhere in it. Its
> visual interest therefore **cannot come from lighting**. It must come from **material and shape
> contrast** — rust against grey concrete, white goods against brown earth, tall bare fences
> against flat ground, a lit food kiosk against a dark lock-up. Plan the abandoned zone by
> *contrast*, not by *density*.

### 20.5 Sun against camera — is a shadow even visible from where we look?

Camera sits south-east and looks north-west. Shadows fall south-west. **The angle between them is
exactly 90°** — shadows lie *across* the frame, neither toward nor away from the camera, which is
the orientation in which they read most strongly.

Already optimal. Worth recording that **it was luck rather than design** until this audit, and it
should now be treated as a fixed constraint: if the camera azimuth is ever changed, the sun
azimuth must move with it.

---

## 21. Part 2 — a fault in my own layout, found by following the roads to the square edge

**L1 runs east–west across the full 440 m. L2 runs north–south across the full 440 m.** The
interchange footprint is only the central 250 m.

**So each route passes through 95 m of RING CITY on two opposite sides** — and I had planned 49
luxury villas in that ring.

> **As written, the plan put elevated motorway over luxury villas.**
> Nobody builds an estate with a tennis court under a viaduct. The plan was wrong, and it would
> have been discovered only after the villas were placed.

### The ring actually divides into three kinds of land

| | area | crossed by |
|---|---|---|
| **4 corner blocks**, 95 × 95 m | 36,100 m² | **neither road** — the quietest land in the city |
| **4 road corridors** through the ring | 13,490 m² | a viaduct overhead |
| **8 side blocks** between them | 81,510 m² | neither, but adjacent to a corridor |

### The fix — and it improves the plan rather than patching it

**Put the businesses where the road is, and the villas where it is quiet.**

| land | use | why |
|---|---|---|
| **4 road corridors** | fuel, motels, diners, retail, lorry parking, under and beside the viaducts | these are the businesses that exist *because* of a motorway. Under a viaduct is exactly where they belong — and it satisfies the brief's demand for "buildings, people and businesses" without inventing a reason for them |
| **4 corner blocks** | the largest **estates** — house, guest house, garage, pool, tennis court | farthest from both roads, the only land in the square touched by neither |
| **8 side blocks** | villas and houses | quiet, but with a business corridor for a neighbour |

**Capacity: ~58 residential plots** (up from 49) plus the businesses, which now have a real place
instead of being squeezed into the villa frontage.

This is not a compromise forced by a mistake. **It makes the city more legible:** the traveller
arrives past the fuel and the motels, and the wealth is tucked into the corners behind them. That
is what an interchange town actually looks like.

---

## 22. Part 3 — what Oran's corrections teach, across both cities

### 22.1 Every fault he caught, and its root

| city | what he saw | cause | **the root** |
|---|---|---|---|
| OASIS | 77 of 190 cars broadside | heading written into `rotation.z` | the model's own axis was never measured |
| OASIS | "things look like they float" ×3 | sun at 30°, then a viewport setting | **two variables changed at once** |
| OASIS | "the roads look cut and wrong" ×5 | junction geometry | a junction treated as a point |
| MEDCOIN | "the frame jumped out at the corner" | corridor lying 9.1 m on the city | **clearance sampled at two points I chose** |
| MEDCOIN | "why is there grass in the image" | nothing wrong — the framing | I showed a render without saying what the frame held |
| MEDCOIN | cars facing each other in a lane | front at minus the length axis | **the axis was measured; the end was assumed** |
| MEDCOIN | "the buildings look the same" | one `colormap.png`, base colour white | variety measured by model count, not by what renders |
| EVENTER | "I could not understand the plan" | prose and tables, no drawing | I checked the plan was *complete*, not that it was *legible* |
| EVENTER | "4 rings — is that enough?" | a cloverleaf is four identical loops | "complete" was tested; **"significant" was not** |

### 22.2 The pattern — and it is deeper than the one found before MEDCOIN

Before MEDCOIN I concluded that *"the tests measured rule compliance, never visual outcome"*, and
the answer was pixel tests. That was true, and it helped. **It was also incomplete, because faults
kept arriving after pixel tests existed.**

The three that got through are the instructive ones:

| fault | what the test actually measured |
|---|---|
| corner overlap | clearance **at two points I chose myself** |
| cars reversed | the **axis**, which is merely *correlated* with orientation |
| grass 32 % dark | a **socket value**, which is an *input*, not the output |

None of those is "geometry instead of pixels". Every one is the same thing:

> ### The test measured a PROXY for the property, not the property.

A proxy passes whenever it is correlated with the truth — which is nearly always. **So a proxy
test stays quiet right up until the one case where it matters.** An axis is correlated with
orientation until a model faces the other way. Two edge samples are correlated with clearance
until the corner. A socket value is correlated with colour until something is plugged into it.

### 22.3 The four rules that follow, to be applied to every EVENTER test

| | rule | in practice |
|---|---|---|
| **1** | Measure the **property**, not something correlated with it | not "is the length axis aligned" but "does the front point where the lane goes" |
| **2** | Measure **every instance**, never samples chosen by hand | not "clearance at the two edge midpoints" but "the minimum over all 435 path samples" |
| **3** | Measure the **output**, not the input | not "the Base Color socket" but "the colour of the pixel that renders" |
| **4** | **Prove the test can fail** before trusting that it passed | break one case deliberately, confirm the test catches it, then fix it back |

**Rule 4 is new, and it is the one that would have caught the other three.** Every test in this
build gets a deliberate broken case first. **A test that has never failed is not a test — it is a
hope.**

### 22.4 Two rules about working with Oran, not about geometry

- **"Complete" and "significant" are different tests.** The revision-1 interchange was complete
  and correct and he was right that it was underwhelming. Before showing any design, ask not only
  "is anything missing" but "is this the most significant version of this idea that fits".
- **Show the frame, not just the render.** He asked about grass that was never in the city — the
  render was right and the framing was unexplained. Every image from now on is delivered with what
  the frame contains and where its edges are.

---

## 23. Part 4 — micro-resolution: what resolves at 4.85 px/m

Camera: orthographic, the same 54.7° / 45° isometric as `CAM_MED`, `ortho_scale` 660, 3200 px
wide. The 440 m square projects 622 m across and fits with margin.

| feature | size | px | reads as |
|---|---|---|---|
| L1 deck width | 39.0 m | 189 | dominant |
| tennis court | 36.0 m | 175 | dominant |
| pool | 9.7 m | 47 | dominant |
| a car, long | 4.5 m | 22 | clearly legible |
| lane width | 3.5 m | 17 | clearly legible |
| a car, wide | 1.8 m | 8.7 | reads as a band |
| **rail gauge** | 1.435 m | **7.0** | **both rails read separately** |
| pier width | 1.2 m | 5.8 | reads as a band |
| **parapet** | 0.9 m | **4.4** | **a band — this is why barriers matter** |
| guardrail | 0.75 m | 3.6 | a line |
| a person | 0.6 m | 2.9 | a line |
| sleeper spacing | 0.6 m | 2.9 | a line |
| lane marking | 0.36 m | 1.75 | a line |
| kerb height | 0.20 m | 0.97 | a hint — keep the 10 mm lip, catching light is its job |
| window mullion | 0.10 m | 0.48 | **invisible — do not build** |
| catenary wire | 0.02 m | 0.10 | **invisible — do not build** |

**What falls out:**

- **Build both rails.** At 7 px the gauge separates; a single line would read as a painted stripe.
- **Sleepers as a repeating bar, not 3D timber.** 2.9 px each — the rhythm reads, the object does not.
- **No catenary.** Invisible at 0.10 px *and* it would clear L2 by only 0.10 m. Two independent
  reasons agree, which is the strongest kind of decision.
- **No window detail anywhere.** 0.48 px.
- **Barriers are visible and therefore load-bearing** — 4.4 px is a clear band. Oran's instruction
  to put a barrier beside every road is not a realism note, it is a legibility requirement.

### 23.1 Merge and diverge geometry, to the metre

A ramp that simply touches a carriageway reads as a collision. Real ones taper.

| | length | rate |
|---|---|---|
| diverge (exit) taper | 75 m | 1:25 |
| merge (entry) taper | 90 m | 1:30 |
| lane drop | 60 m | 1:20 |

With 8 diverges and 8 merges that is **1,320 m of taper geometry**, about 4 % of all ribbon
length — and **the single most visible sign that the interchange was designed rather than
assembled.**

### 23.2 Clearance, to the centimetre

| level | deck top | soffit | clear over the level below |
|---|---|---|---|
| ground asphalt | 0.14 | — | — |
| **L1** | 6.50 | 5.60 | **5.46 m** |
| **L2** | 13.00 | 12.10 | **5.60 m** |
| **L3** | 19.50 | 18.60 | **5.60 m** |

**Minimum anywhere: 5.46 m** against a 5.00 m standard — a **0.46 m margin**. That margin is
enough to absorb a deck that sags, a ramp that overshoots its grade, or a surface built 50 mm
proud. **It is the reason to fix 6.5 m spacing now rather than discover it mid-build.**

---

## 24. Third audit — result

| | |
|---|---|
| shadow analysed against the roads | **a rule reversed**: for an elevated deck a detached shadow is the goal |
| the real height cue identified | **the piers**, not the decks — 3.24 m shadows every 18 m |
| new build constraint | **4.2 m clear SW of every pier base**, constraining the 570 elements |
| under-deck brightness | **81 %** of lit — build it by *contrast*, not by density |
| sun against camera | **90° — optimal**, and now a fixed constraint rather than luck |
| **fault found in the layout** | **elevated motorway over luxury villas** — corrected, and the fix improves the city |
| residential plots | 49 → **~58**, and the businesses gained a real place |
| root-cause of every correction | **the test measured a proxy, not the property** |
| new test-design rules | **4**, of which rule 4 — *prove the test can fail* — is the one that catches the rest |
| micro-resolution | 17 features measured; **4 struck off as invisible** |
| clearance margin | **0.46 m**, fixed now rather than found later |

**The plan is ready.**
