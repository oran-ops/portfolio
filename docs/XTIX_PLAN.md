# XTIX — the plan, 2026-08-27

> *"I want to go back to the drawing board. I want to see the drawing, to be sure everything
> is well planned, that we have quantities, that we have the shadow, that we have a
> placement plan, roads, ways, elements and everything. We do not start building anything
> before there is an orderly plan built on all the earlier work."*

Nothing here is asserted. **The plan is `world-build/tools/xtix_plan.py`**, every number below
is computed by it, and **the two drawings are rendered from the same structures the builder
will read** — because a drawing produced alongside a plan is a picture of an intention, and
the lesson of three cities is that two descriptions of one thing drift apart and the wrong
one wins the argument.

Sheets: `XTIX_PLAN_sheet.png` (layout) · `XTIX_PLAN_massing.png` (heights).

---

## 1. What XTIX is, in Oran's words

> **Built everything from zero.** 30 % under construction, 70 % already standing.
> Skyscrapers, luxury restaurants, new cars, people in suits, ordered roads, tall
> residential, density, a great deal happening at once. In the construction zones: tall
> cranes, contractors at work, excavations with tools, building skeletons mid-rise — the
> plan of a future metropolis.
> *Raised from nothing, fast — and still it came up tall, luxurious and very strong.*

And on style: **"Dubai combined with New York"**, with the earlier *"not Dubai, not New
York, not Tokyo"* clarified as *"it should be MORE futuristic and MORE innovative, something
very sophisticated."* The two cities are the recognisable floor. They are not the target.

### The risk this plan exists to avoid

**XTIX and MEDCOIN could read as the same city.** MEDCOIN is a grid with a ring road and a
tower cluster; XTIX's brief also says skyscrapers, density and ordered roads. Three things
separate them, and all three are structural rather than decorative:

| | MEDCOIN | XTIX |
|---|---|---|
| what it is | a city people **work** in — "little residential" | a city people **live** in — apartments, restaurants |
| the skyline | a flat-topped cluster, no direction | a **ramp** — you can see which way it grew |
| time | finished | **30 % of it is still going up** |

---

## 2. The frame and the grid

| | |
|---|---|
| plate | 800 × 740 m — as EVENTER, OASIS and MEDCOIN |
| city square | **540 × 540 m** at origin (130, 100) — larger than EVENTER's 440, approved |
| blocks | **7 × 7 = 49**, each **62 × 62 m** |
| corridors per axis | **8** — 2 avenues at 20 m, 6 streets at 11 m |
| avenue section | 14 m carriageway + 3 m pavement each side |
| street section | 7 m carriageway + 2 m pavement each side |

**The arithmetic has to close exactly, or the last block is a different size from the other
six and the master plan stops looking planned:**

```
7 blocks × 62 m                       = 434 m
2 avenues × 20 m + 6 streets × 11 m   = 106 m
                                 total  540 m   ✓ checksum passes
```

The two avenues sit at corridors 2 and 5, which groups the blocks **2 – 3 – 2**. An even
spread would have given a chessboard; this gives the grid a rhythm you can read.

**The grid is laid across the whole square from the first day** — including the ground that
has nothing on it yet. That is what makes *"the plan of a future metropolis"* something you
can see rather than something I have to explain.

| roads | metres |
|---|---|
| avenue centreline | 2,160 |
| street centreline | 6,480 |
| **total** | **8,640** |
| pavement, both sides | **17,280** |

---

## 3. The frontier — how 30/70 lands on the ground

Approved shape: **finished and tall at the back of the frame, construction at the front,
full grid throughout.** The camera looks from the south-east, so "back" is the north-west
corner and the growth axis is the **diagonal** — also the longest run available, so the
gradient has the most room to read.

**Maturity** runs 1 at the north-west corner to 0 at the south-east, plus ±0.10 of noise so
the frontier is a band and not a drawn line.

### The threshold is solved, not chosen — twice over

The first attempt solved it against **area**: over a square the sum of two distances is
triangularly distributed, so a naive cut at 0.30 gives 18 % rather than 30 %, and the
corrected area cut is 0.3875. **That was still wrong**, and running the file said so: it
produced **46.6 % of the buildings** under construction, because the frontier is where the
small-plot tiers live and a block there carries nine buildings while a block at the back
carries one.

**Oran counted buildings, not hectares.** The cut is now bisected against the realised
building count. It lands at **0.2605**.

> A third fault surfaced fixing that: the bisection would not converge, stalling at 32.3 %,
> because the stage random number was drawn *inside* the else branch, so the random stream
> forked on the threshold and the count stopped being monotonic in it. Drawn
> unconditionally, it converges.

### The stage ladder

Progress is **dealt from a designed mix**, not read straight off the maturity field. Read
off the field, 50 of 55 sites carried a crane — a crane forest with nothing else to look at.

| stage | prog | share | crane | count |
|---|---|---|---|---|
| 1 · excavation | 0.06 – 0.15 | 16 % | — | **10** |
| 2 · foundations and podium | 0.15 – 0.29 | 17 % | — | **8** |
| 3 · frame rising | 0.30 – 0.69 | 38 % | **yes** | **18** |
| 4 · topping out | 0.70 – 0.95 | 29 % | **yes** | **17** |
| 5 · finished | 1.00 | — | — | **119** |

**Under construction: 53 of 172 = 30.8 %.**

---

## 4. Placement — what stands where

Tier comes from maturity; **height comes from frontage**. That second rule is the one the
massing model forced:

> Tying tier to maturity alone made the whole frontier **low as well as unfinished**,
> because the low tiers and the low progress landed on the same ground and doubled up. A
> growth frontier does not look like that — Dubai's newest towers are its tallest, and a
> developer builds the anchor tower on the main road first.

| tier | maturity | plots/block | height range |
|---|---|---|---|
| tall | ≥ 0.70 | 1 | 105 – 178 m |
| mid | ≥ 0.46 | 2 | 62 – 118 m |
| low | ≥ 0.22 | 6 — street wall | 26 – 64 m |
| edge | ≥ 0.00 | 9 — street wall | 14 – 38 m |

**Avenue frontage multiplies height** — ×2.1 at the edge tier down to ×1.10 at the tall
tier, so the boost is largest where the buildings are smallest (a slim tower on a narrow
avenue plot is the most New York thing in the set) and everything is **capped at 196 m**.

Two corrections were needed to get there, both caught by the numbers:

- **The lift first promoted the tier**, which collapsed the plot count from 177 to 104: a
  block that would have carried six street-wall units became one tower, and that happened
  to 82 % of the city. An avenue frontage does not have *fewer* buildings than a side
  street — it has **taller ones on the same plots**.
- **Frontage was tested on the block**, which made 142 of 172 buildings avenue-fronting.
  At that share it is not a rule, it is a general height rise. Tested on the **plot's own
  edges** it is **81 of 172 — 47 %**, and a unit on the far side of a block correctly does
  not count.

### The street wall

The low tiers are not four detached boxes to a block. They are a **perimeter of party-wall
units** — which is what puts the luxury restaurants and shops at the base of the towers, and
what MEDCOIN's 70 m² core footprints already proved reads as a city rather than a diagram.

> The plan drawing caught a bug here at a glance that no number would have: `per_side`
> rounded to 2 and the corner-skip then excluded **both** indices, so every street-wall
> block came out as a north row, a south row and a hole where the east and west sides
> should be. This is the entire reason for drawing a plan before building it.

### The landmark

**Block (2, 1), maturity 0.424 — on the seam** between the finished city and the frontier.
**218 m, the single tallest thing on the plate**, topped out, **and its crane is still
standing.** That is XTIX in one object: it reached the top, and the crane has not come down.

> It is *assigned*, not qualified for. Leaving "landmark" in the tier table gave **eight**
> landmarks once the avenue rule pushed seven other blocks over the threshold.

### Public space

Two blocks are not built on: a **civic plaza** where the avenues cross on the finished side,
and a **green square** out in the frontier where the ground is still waiting. A metropolis
with no public space is a diagram of one — and a square is where "luxury restaurants" and "a
great deal happening at once" actually happen.

---

## 5. Quantities

| | count |
|---|---|
| **buildings** | **172** |
| of which towers ≥ 60 m | **88** |
| tall (≥ 105 m) · mid (60–105) · low | 50 · 79 · 43 |
| **under construction** | **53 — 30.8 %** |
| **tower cranes** | **36** |
| excavations · foundations | 10 · 8 |
| site hoarding | **~4,100 m** |
| site elements (cones, barriers, spoil, stacks, skips, huts, plant, crew) | **~1,350** |
| **vehicles** | **846** |
| **people** | **1,858** |
| street trees | 166 |
| street furniture | 205 |
| public spaces | 2 |

**The two life densities are carried from MEDCOIN as measured, not re-invented:** 1,200
people on 11,200 m of pavement is one per 9.3 m, and 550 vehicles on 5,600 m of street is
0.098 per metre. Applied to XTIX's 17,280 m and 8,640 m they give the figures above.

### Does the square close to 100 %?

Both earlier plans had to show this and both found faults doing it.

| | m² | share |
|---|---|---|
| roads and pavements | 103,244 | **35.4 %** |
| building footprint | 118,192 | **40.5 %** |
| yards, plazas, forecourts, car parks, sites | 70,164 | **24.1 %** |
| **total** | **291,600** | **100.0 %** ✓ |

**Footprint 40.5 % against MEDCOIN's measured 37.0 %** — XTIX is as dense as the financial
district, which is the answer to "density, a great deal happening at once". It gets there
with 172 large buildings instead of 550 small ones, and the *coverage* is what the eye reads.

---

## 6. The shadow

The world sun has not moved since it was measured on EVENTER: **elevation 75°, azimuth 135°,
direction (−0.183, −0.183, −0.966)**. Shadows fall **south-west** at **0.2679 × height**.

| | height | shadow |
|---|---|---|
| **the landmark** | **218 m** | **58.4 m** |
| tall tower | 175 m | 46.9 m |
| mid tower | 120 m | 32.1 m |
| street wall | 30 m | 8.0 m |

**The number that matters: block + street = 73 m, and the longest shadow on the plate is
58.4 m.** So the tallest tower's shadow crosses its street and reaches 47 m into the
neighbouring block — **but never crosses it.** No building on this plan is ever fully in
another building's shadow, and the street grid stays lit.

This is the first of the four cities where shadow is a **planning constraint rather than a
depth cue**. On EVENTER every shadow fell under its own deck. Here they fall on other
people's plots, and the 73 m pitch is what keeps that survivable.

---

## 7. What it costs to render

EVENTER shipped at **5.89 M triangles** and rendered 3200 × 1930 in 13 minutes. That is the
ceiling, measured rather than assumed.

| | n | each | triangles |
|---|---|---|---|
| towers ≥ 105 m | 50 | 12,000 | 600,000 |
| towers 60 – 105 m | 79 | 7,000 | 553,000 |
| low-rise and street wall | 43 | 2,400 | 103,200 |
| cranes | 36 | 600 | 21,600 |
| site elements | 1,350 | 320 | 432,000 |
| **vehicles** | 846 | 2,266 | **1,917,036** |
| people | 1,858 | 72 | 133,776 |
| street trees | 166 | 900 | 149,400 |
| street furniture | 205 | 260 | 53,300 |
| ground, roads, pavements | | | 90,000 |
| **TOTAL** | | | **3,799,712** |
| **headroom under EVENTER** | | | **2,090,288** |

Vehicles are 50 % of the budget, exactly as they were on EVENTER. If anything needs to give
later, it is there and nowhere else.

---

## 8. Elements — every one checked against what we hold

| what | source | status |
|---|---|---|
| **towers, all 172** | `xtix_towers.py` — 20 shape families × 12 facades × 10 glass tints | **built** |
| **construction state** | the same shafts at `prog < 1` — cladding trails the frame, core runs ahead | **built** |
| **tower cranes** | built procedurally, 270–582 faces each | **built** |
| low and mid-rise fabric | `city-kit-commercial`, `lowpoly-city`, `Buildings+sprite` at their **own** size | ready |
| heavy plant — mobile crane, dozer, mixer, dump truck, forklift | `Construction+1.1.blend` | ready, needs the texture fix |
| harbour / crawler crane | `Crane.blend` — ground plant, not a tower crane | ready |
| site hoarding, cones, barriers, lights | `city-kit-roads`, `Trafiic+cone.blend` | ready |
| scaffolding | `retro-urban-kit` | ready |
| vehicles | EVENTER's fleet — 15 road models, 100 colours, verified | **carried over** |
| people | EVENTER's 30 models | **carried over** |
| helicopters | 3, from the new folder | ready |
| street trees, planting | `nature-kit`, retinted as in EVENTER | **carried over** |

**Two things are known not to work and are not in the plan.** Kit skyscrapers cannot be
stretched to tower height — measured at 100 m their windows become 10–25 m tall. And `1.max`
cannot be opened; Blender has no 3ds Max importer.

**One open decision for Oran:** the sci-fi buildings in the new folder (`High building`,
`hospital_building`, `Downtown Center City`) are genuinely more futuristic than anything
here, but they are a **different style family** — emissive cyan, much finer detail — and
they are wide low masses, not towers. Whether they join XTIX changes how the whole map
reads, so it is his call and not mine.

---

## 9. Build order

1. **Ground, grid, kerbs, pavements** — the whole 540 m square, nothing else
2. **Plots pegged out** — every one of the 172, drawn as hoarding or kerb
3. **The finished 119** — towers, facades, crowns, podiums
4. **The 53 sites** — by stage: excavations, foundations, frames, topping out
5. **36 cranes** — derived from stage, never placed by hand
6. **The landmark**, and its crane
7. **Street wall, shops, restaurants** at the base
8. **Life** — 846 vehicles, 1,858 people, trees, furniture
9. **Plaza and park**
10. **Audit, then render**

## 10. The tests that must exist before stage 3

Every one of these is a property that has already been got wrong once on another city:

- the grid checksum closes to 540 m exactly
- no building outside its plot, no plot on a road *(EVENTER)*
- **under-construction share is 30 % ± 1 building**, measured on buildings
- exactly **one** building over 196 m
- every crane derives from a stage-3 or stage-4 plot, and no other plot has one
- no crane jib intersects a building
- no two buildings intersect *(EVENTER's footprint test, carried over)*
- the square closes to 100 % of area
- **no vehicle facing the wrong way, none off-road** *(EVENTER, carried over)*
- variety: shape families, facades and glass tints all in use, none over its cap
- the lighting state is asserted before every render *(the third-party blends silently
  replaced the world, the sun and the view transform)*

---

## 11. Audit status

**Both audits have now been run.** See below.

---

# THE SECOND AUDIT — the plan against itself, 2026-08-27

Run as **code**, not prose: `world-build/tools/xtix_audit.py`. Twenty-one checks over every
plot, every corridor, every crane and every pair.

Every check obeys the four rules EVENTER cost us, and **rule 4 is enforced literally**:
each check is first fed a deliberately broken plan and must catch it. The file refuses to
report on the real plan if any self-test passes when it should have failed.

> *A test that has never failed is not a test — it is a hope.*

**Self-tests: 12 of 12 caught their break.** One of them caught it only after I fixed the
break itself — I had tampered with `H` while the check reads the plan's *resolved* massing,
so the break never reached it. **The proxy problem, inside the proof of the proxy problem.**

## The five failures, and which were mine

### Two were the TEST, not the plan — and MEDCOIN proves it

| my test | what MEDCOIN scores | verdict |
|---|---|---|
| "the street floor must be visible" | needs **49.6 m** of width for its 70 m towers; it has **22** | the test fails a city Oran approved |
| "8–15 objects per 50 m" | **20.1 with vehicles**, 15.2 without | I counted traffic |

The first asked whether the whole street floor clears the whole building at 54.7°. **Visible
floor was never the property.** MEDCOIN's streets read perfectly well as slots between
masses. Re-scoped: it now measures what the camera actually meets at the kerb — the
**podium** — and reports avenues and side streets separately, because the avenues are what
"ordered roads" has to mean.

The second: **vehicles are not the life layer.** MAP_ANALYSIS 1.4 is about what stands on a
footway. Counting cars scored MEDCOIN outside the band it was approved at.

> This is rule 1 again — *measure the property, not something correlated with it* — and it
> is worth recording that after writing that rule down, I broke it twice in one sitting.

### Three were the plan

**1 · THE STREET CANYON — the biggest finding.** The plan put **171 m towers on 11 m side
streets**: a height-to-width ratio of **15.6**, against Wall Street's 4–6 and MEDCOIN's own
worst case of 6.5. That is not a street, it is a slot, and no city has ever been built that
way.

Fixed with the rule Manhattan wrote into law in 1916, and it costs nothing here because the
tower engine already has setbacks as a first-class idea: **a building over 45 m stands on a
podium that fills its plot and holds the street wall — the shops and restaurants Oran asked
for — and the shaft is set back behind it.** If a plot is too small to buy the setback its
height needs, the setback gives way first and then the **height** does; the building is
lowered until it complies.

| | before | after |
|---|---|---|
| worst tower canyon | **15.6** | **5.01** |
| towers over the 6.5 limit | 24 | **0** |
| worst at the pavement | — | **4.04** — a Paris street wall |
| median tower canyon | — | 4.10 |

**2 · SEVEN CRANE JIBS PASSED THROUGH A TALLER BUILDING.** A jib is up to 62 m and a block
is 62 m, so every crane reaches into the next block. Real jibs do slew over their
neighbours — but **above** them. The mast height is now derived from the tallest thing the
jib can reach, not from its own building alone. **7 → 0.**

**3 · EIGHT DEAD 20 m CELLS**, and every one was the **middle of a perimeter block**. Not
dead ground: MEDCOIN settled this and counted yards and service courts as 36 % of its city.
So they are now **19 courtyards**, each carrying 14 elements — parked cars, bins, delivery
bays, plant, trees. **266 objects that the plan previously had nowhere to put.**

---

# THE THIRD AUDIT — the deep pass

## 13.1 The six systems of `MAP_ANALYSIS`, re-read for XTIX

**1.1 Buildings form BLOCKS, not objects** — **yes, structurally.** The low tiers are a
**perimeter of party-wall units**, six to nine to a block, with a service courtyard behind.
The towers are not detached objects either: each is podium + shaft, and the podium holds the
block edge. Nothing in XTIX is a box sitting on grass.

**1.2 The pavement is a real object** — **closed.**

| road | section |
|---|---|
| **avenue** | 14.0 m carriageway · **3.0 m pavement each side** · 20.0 m corridor |
| **street** | 7.0 m carriageway · **2.0 m pavement each side** · 11.0 m corridor |

17,280 m of pavement. Everything on a street stands on it.

**1.3 Building types distinguishable at a glance** — **closed.** Four types plus two site
states, each with its own footprint, height, crown, facade and surroundings:

| type | share | footprint | height | crown | facade | around it |
|---|---|---|---|---|---|---|
| **landmark** | 0.6 % | set back, whole block | **216 m** | spire **+ its crane** | mullion | plaza, podium |
| **office tower** | 26.2 % | whole block, set back | 60–196 | flat · mast · diagrid | grid · banded · xbrace | podium with retail |
| **residential tower** | 40.7 % | set back | 45–170 | garden · fins | **balcony · stagger · terrace** | podium, courtyard |
| **street wall** | 32.6 % | narrow, party wall | 14–45 | flat parapet | punched · loggia | continuous shopfront |
| *site: excavation* | — | a pit | 2–8 | none | hoarding | spoil, plant, fence |
| *site: frame* | — | slab + columns | rising | bare | none | **crane**, hoarding, materials |

A residential tower cannot be mistaken for an office one: **balconies**.

**1.4 The life layer is systematic** — **closed, by rule against the street.**

| | rule | count |
|---|---|---|
| people on pavements | 1 per 9.3 m — MEDCOIN's measured density | **1,593** |
| site crew | 5 per site, inside the hoarding | **265** |
| street trees | 1 per 13 m of avenue | 166 |
| verge trees | 1 per 11 m of perimeter | 196 |
| street furniture | 1 per 42 m | 205 |
| courtyard elements | 14 per courtyard | 266 |

**The 50 m test: 12.9 objects.** In band (8–15); MEDCOIN scores 15.2 by the same measure.

**1.5 Colour natural, saturated only in small things** — **closed, and it needed a rule.**
Ten glass tints across 172 buildings breaks 1.5 outright if a 196 m tower wears the most
saturated one — that is an enormous saturated area. So **the tint is chosen by height**:
above 120 m only the near-neutral end (pearl, ice, smoke, pale), and the colour lives on the
short buildings and the street wall, where it is a small thing.

> **XTIX's colour source is the STREET WALL and the site yellow of the cranes** — as
> EVENTER's was its cars, MEDCOIN's its containers and OASIS's its roofs.

Measured: **0 saturated tints above 120 m · 11 of 11 tints in use.**

**1.6 One sun, hard shadows** — **unchanged since OASIS.** 75°, azimuth 135°, energy 0.8835.

## 13.2 Micro-resolution — what resolves at 4.44 px/m

| feature | metres | pixels | verdict |
|---|---|---|---|
| podium | 15.0 | 67 | geometry |
| tower setback | 12.0 | 53 | geometry |
| floor line | 3.7 | 16 | geometry |
| crane mast | 2.0 | 8.9 | geometry |
| site hoarding | 2.0 | 8.9 | geometry |
| a person | 1.75 | 7.8 | geometry |
| balcony projection | 1.5 | 6.7 | geometry |
| crane jib chord | 0.85 | 3.8 | geometry |
| facade mullion | 0.5 | 2.2 | **borderline — cut deep or not at all** |
| hand tools | 0.3 | 1.3 | **texture only — do not model** |

## 13.3 The boundary — MEDCOIN's Gap 6, answered

The grid stops dead at 540 m, so without a designed edge the city ends on a kerb in the
middle of a field. The answer a master plan gives: **the outermost corridor is the perimeter
road, and outside it a 24 m planted verge takes the city down to the country** — 54,144 m²
of verge, **196 trees**, then 246,256 m² of country beyond.

## 13.4 Traffic and people — MEDCOIN's Gap 4, answered

Never stated on any city until MEDCOIN asked for it, and never stated here until now:

| | count |
|---|---|
| moving on the carriageway | **524** |
| parked at the kerb | **238** |
| standing inside a site hoarding | **84** |
| **total vehicles** | **846** |

**People stand on a pavement, in the plaza or park, or inside a hoarding as crew. Never on a
carriageway, never on a podium roof, never on an unfinished floor.**

## 13.5 Every lesson from the three cities, and where it lands here

| lesson | from | applied |
|---|---|---|
| measure scale per **file**, not per kit | OASIS | kit fabric measured at import |
| plausibility gate on every imported model | OASIS | the 100 m kit test already rejected the kit skyscrapers |
| **a missing texture renders magenta** | MEDCOIN | the new folder's crane and plant need the fix before use |
| check `input.links` before trusting a socket | OASIS | — |
| vehicles need **two** things measured: axis and front | MEDCOIN | EVENTER's fleet carried over intact |
| parked cars take the heading of the lane beside them | MEDCOIN | carried |
| pack largest-first | OASIS | towers placed before street furniture |
| test a rule only where it applies | OASIS | podium checks skip buildings under 45 m |
| **read `matrix_world` only after `view_layer.update()`** | OASIS | — |
| never verify placement from `bound_box + location` | OASIS | — |
| a pixel test as well as a geometry test | MEDCOIN | the two plan sheets are the pixel test of the plan |
| **a test that cries wolf on a clean build is worse than no test** | EVENTER | two of my own tests were re-scoped for exactly this |
| **one function, every caller** | EVENTER ×6 | the drawing renders from the plan's own structures |
| the four test-design rules | EVENTER | every check here, rule 4 enforced by the file |
| **"complete" and "significant" are different tests** | EVENTER | see below |
| **show the frame, not just the render** | EVENTER | stated with every sheet |

## 13.6 "Complete" and "significant" — asked, measured, answered

The revision-1 interchange was complete, correct, and Oran was right that it was
underwhelming. So: **is this the most significant version of this idea that fits?**

I raised one doubt — that a **second frontier** in another corner would tell *"raised from
nothing, fast"* harder — and Oran said he would consider it, but **only if I was certain**.

**So I measured it instead of arguing it.** Mean maturity along the growth axis, nine bands:

| | |
|---|---|
| **one frontier** | 0.88 · 0.79 · 0.71 · 0.60 · 0.50 · 0.40 · 0.29 · 0.21 · 0.12 |
| **two frontiers** | **0.50 · 0.50 · 0.50** · 0.45 · 0.38 · 0.34 · 0.29 · 0.21 · 0.12 |

**Two frontiers flatten the first third of the map.** The whole mature half collapses to one
middling level: no peak, no direction, no ramp. And *"a flat-topped cluster with no
direction"* is precisely what §1 of this plan says separates XTIX from MEDCOIN — so a second
frontier would have made XTIX **more** like MEDCOIN, not less.

**Answer: no.** With the numbers behind it.

### But the instinct was right, and the mechanism was wrong

A boom city does not grow from two corners. It builds at the edge **and replaces towers in
the middle** — Dubai does exactly this. That keeps the ramp whole, still puts construction in
two places, and buys the strongest single image available: **a crane standing in the middle
of the finished skyline.**

**Six renewal sites**, in mature avenue-fronting ground, kept 95 m apart so they read as
separate redevelopments rather than as the frontier having moved:

| | height | maturity | built |
|---|---|---|---|
| 1 | 180 m | 0.86 | 59 % |
| 2 | 183 m | 0.64 | 79 % |
| 3 | 137 m | 0.61 | 76 % |
| 4 | 126 m | 0.80 | 74 % |
| 5 | 157 m | 0.70 | 69 % |
| 6 | 154 m | 0.68 | 55 % |

**45 sites at the frontier + 6 in the core = 51, still 29.7 % of the buildings.** Every one of
the six is stage 3 or 4, so every one carries a crane.

## 13.7 The cyberpunk buildings — dropped

Oran: *"if we have no other designs connected to it, and the skyscrapers are not cyberpunk in
their design, I do not see the need to put the low cyberpunk buildings into the map — it
would look strange, a small part futuristic and most of the map not."*

**His reasoning is sharper than mine was.** I read it as a style clash between kits; he read
it as an **internal inconsistency** in the city — which is the better reason, and the one
that would have shown in the render. Dropped.

---

# THE CHECK LIST — 21 checks, all passing

| | check | result |
|---|---|---|
| ✓ | grid checksum | **540.0 m exactly** |
| ✓ | plots overlapping a road corridor | 0 |
| ✓ | overlapping plots | 0 |
| ✓ | plots outside the city square | 0 |
| ✓ | dead 20 m cells | **0** |
| ✓ | worst tower canyon | **5.01** (limit 6.5) |
| ✓ | street floor past the podium | **avenues 43.7 %**, side streets 2.4 % |
| ✓ | longest shadow vs block pitch | 58.0 m < 73 m |
| ✓ | buildings that fit their plot | all 172 |
| ✓ | height spread, commonest band | 30.8 % · **no empty band 25–150 m** |
| ✓ | buildings over 196 m | **exactly 1** |
| ✓ | use mix, commonest | 40.7 % residential |
| ✓ | saturated glass above 120 m | **0** · 11 of 11 tints used |
| ✓ | stage mix vs design | worst error 7.3 pp |
| ✓ | cranes not derived from stage | **0** |
| ✓ | crane jibs fouling a neighbour | **0** |
| ✓ | life-layer objects per 50 m | 12.9 |
| ✓ | city area closes | **100.0 %** |
| ✓ | triangles vs EVENTER | **3,775,712** — 2.11 M of headroom |

**Final quantities: 172 buildings · 30.8 % under construction · 83 towers over 60 m ·
39 cranes · 19 courtyards · 846 vehicles · 1,858 people · 362 trees.**

## Awaiting Oran

1. **The cyberpunk buildings** from the new folder — genuinely more futuristic, but a
   different style family. Changes how the whole map reads.
2. **A second frontier** — §13.6. More significant, but a change to an approved layout.
