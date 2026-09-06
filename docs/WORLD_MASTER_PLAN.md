# THE WORLD — master plan

**Status: a plan. Nothing here has been built.**

Four cities exist and are finished. This is the plan for making them one world: where each sits,
how the road joins them, how the ground meets, what the viewer sees and in what order — and,
above all, **the contract that lets any of them be changed later without breaking the whole.**

It is the most exacting plan on this project so far, because the joins *are* the deliverable.
A city that is 5 % better and a seam that is visible is a worse map than four cities left alone.

Every number below is **measured from the built scenes**, not read off a generator's constants.
That distinction has already earned its keep three times in this document.

---

## 1. What exists — measured

`tools/world_survey.py`, `world_reach.py`, `world_mouths.py`, `world_seam.py`, run headless
against the four `.blend` files.

| | plate (m) | objects | faces | tallest | file |
|---|---|---|---|---|---|
| **XTIX** | 809.3 × 746.8 | 21,146 | 6.44 M | 261.9 m | `xtix.blend` 30.6 MB |
| **OASIS** | 700 × 650 | 12,557 | 2.24 M | 47.2 m | `world_map.blend` 9.6 MB |
| **EVENTER** | 800.3 × 740.2 | 9,414 | 5.38 M | 30.1 m | `eventer.blend` 7.4 MB |
| **MEDCOIN** | 700 × 650 | 4,870 | 3.43 M | 72.2 m | `medcoin.blend` 8.6 MB |
| | | **47,987** | **17.5 M** | | 56.2 MB |

Plate sizes are carried in the plan **rounded up** — XTIX 810 × 747, OASIS 700 × 650, EVENTER
**801 × 741**, MEDCOIN 700 × 650. The audit caught EVENTER planned at 800 × 740 against a
measured 800.3 × 740.2: the plan was reserving 0.3 m *less* than the plate occupies. Harmless
at a 157 m corridor, and wrong in principle — a footprint in a contract has to bound the thing
it describes.

### 1.1 What is already reconciled — and it is the hard half

**All four cities carry an identical sun and an identical camera.**

| | value | all four |
|---|---|---|
| sun elevation | **75°** | identical |
| sun azimuth | **135°** | identical |
| sun energy | **0.8835** | identical |
| sun angular size | **3.4°** | identical |
| camera | **orthographic** | identical |
| camera pitch · yaw | **54.7° · 45°** | identical |

This was not planned; it fell out of each city inheriting MEDCOIN's setup. It means **shadow
direction and length are already consistent across the world**, which is normally the single
hardest thing to reconcile when merging independently authored scenes. Shadows fall
**south-west**, `0.2679 m per metre of height` — `cot(75°)`.

### 1.2 What is NOT reconciled — three seams, all found by measuring

**Seam 1 — the greens differ.** The plate green, by surface area:

| | base colour | area |
|---|---|---|
| XTIX | `(0.3629, 0.5183, 0.1065)` | 592,000 m² |
| EVENTER | `(0.3629, 0.5183, 0.1065)` | 398,400 m² |
| MEDCOIN | `(0.3630, 0.5184, 0.1065)` | 455,000 m² |
| **OASIS** | **`(0.2462, 0.3516, 0.0723)`** | 455,102 m² |

Three match to four decimal places. **OASIS is a different, darker green — about 68 % of the
others' brightness.** Dropped into the world as-is it would read as a dark rectangle in the
grass. This is precisely the class of fault that only appears at the join.

**Seam 2 — only two cities can be reached by road.** Asphalt distance to the nearest plate edge:

| | W | E | S | N |
|---|---|---|---|---|
| **XTIX** | 139.6 | 140.8 | 103.6 | 108.7 |
| **OASIS** | 14.9 | 12.4 | 125.2 | 145.3 |
| **EVENTER** | 0.1 | 0.1 | 0.2 | **0.0** |
| **MEDCOIN** | 133.0 | **0.8** | **0.8** | 100.8 |

EVENTER reaches all four edges (it is the interchange). MEDCOIN reaches **E** and **S** — exactly
as `world_merge.py` always said: *"enters from the SOUTH and leaves east."* **XTIX reaches
nothing on any edge.** OASIS reaches within ~13 m but the carriageway itself does not arrive:
its only edge asphalt is two **1.4 m fragments**, at y=224 (W) and y=504 (E) — different
positions, so not the two ends of one road.

**Seam 3 — OASIS's roads are a different material.** A rule that finds long carriageway runs in
the other three (`XTIX` avenues at y=256 and y=484; `EVENTER` through routes at x≈400, y≈370;
`MEDCOIN` at x≈289/411, y≈280/370) finds **nothing** in OASIS. Its residential streets are
lighter than the asphalt threshold. Its mouths must be located with a rule calibrated to OASIS's
own road material — **this is the one number in the plan still to be measured.**

### 1.3 A correction I made to myself, twice

The first mouth survey reported **no road at any OASIS edge**, which would have meant OASIS
could not be connected without re-cutting it. A second pass showed asphalt reaching within
14.9 m. The disagreement was mine: pass 1 required a contiguous run of ≥3 m inside an 18 m
band, and the few narrow faces near the edge never made that span.

The third pass settled it — those faces are real but they are 1.4 m fragments, not a mouth.
**The conclusion survived, the reasoning did not.** Three passes to be sure of one fact is the
right price for a number the whole layout hangs on.

---

## 2. The reading — who sees what, in what order

### 2.1 The screen decides the layout

At yaw 45° and pitch 54.7° the camera sits south-east and looks north-west. In the rendered
frame:

| world direction | on screen |
|---|---|
| **+X +Y** (north-east) | **right** |
| **−X +Y** (north-west) | **up / away** |
| **+X −Y** (south-east) | **down / toward the viewer** |
| −X −Y (south-west) | left |

So a city's position **across the frame** is `(x + y) / √2`, and its height up the frame is
`(y − x) / √2 · cos 54.7°`. A path that reads left to right must run **south-west to
north-east**. That single fact drives everything in §3.

### 2.2 The journey

`START → XTIX → OASIS → EVENTER → MEDCOIN → END` — the portfolio's own scroll order
(`FILE 01…04`), so the map and the document agree.

| zoom | what the viewer sees | what is loaded |
|---|---|---|
| **L0 · the world** | the whole country, four cities, one road, START and END, labels on arrows | massing proxies, ~300 k triangles |
| **L1 · one city** | that city's streets, buildings, traffic, people | that city only, ~1–2.5 MB |
| **L2 · detail** | the smallest detail — a crew on a slab, a shopfront | streamed, or a Cycles still |

Rules from the brief, unchanged: **mouse on every axis; nowhere to travel beyond the map; not
clickable except to zoom into a workplace; scrolling leaves the map and enters the document.**

### 2.3 What comes before what

The eye enters at the **left**, where START sits, and is carried right. Nothing else in the
frame may out-shout that: the four labels are the only text, the road is the only strong line,
and the green is quiet. The order the reader meets things is:

1. **START**, far left, low — the entry.
2. **XTIX**, left at mid-height — tallest in the world, so it also reads as the anchor.
3. **OASIS**, dipping to the **front** of the frame — nearest the viewer, most legible.
4. **EVENTER**, rising to the **back** — the interchange read from above, which is how an
   interchange wants to be read.
5. **MEDCOIN**, right at mid-height — the last city.
6. **END**, far right.

The path therefore traces a gentle **S** across the frame rather than a straight line, and each
city occupies a different band of the frame's height. That is the composition, and it is a
consequence of the layout in §3, not a wish laid on top of it.

---

## 3. The layout — solved, not eyeballed

### 3.1 The trade-off, stated honestly

`tools/world_options.py` measured three families:

| | map | aspect | built | min gap | reading steps across the frame |
|---|---|---|---|---|---|
| **A** compact 2×2 | 1882 × 1859 | 1.012 | **60.2 %** | 372 m | 763, **23**, 769 |
| **B** diagonal chain | 2363 × 2703 | 1.144 | 33.0 % | **−63 m** ✗ overlaps | 803, 943, 809 |
| **C** staggered rhombus | 2040 × 1830 | 1.115 | 56.4 % | 193 m | 535, 357, 590 |

**The conflict is geometric, not a matter of tuning.** In a compact 2×2 the SE and NW cells have
almost the same `x + y`, so two of the four cities land at the same place across the frame and
stack vertically instead of advancing — option A's middle step is **23 m**. Spread the cities
along the diagonal instead and the reading is even, but both off-diagonal corners become pure
green and the built fraction collapses to a third.

Option C gets both. `tools/world_refine.py` then optimised it.

### 3.2 The layout

**City bounding box 1,874 × 1,874 m — aspect 1.000, cities 60.0 % of it, minimum gap 151 m.**

| city | plate origin (x, y) | extent | centre | across frame | up frame |
|---|---|---|---|---|---|
| **XTIX** | **(0, 0)** | 810 × 747 | (405, 373) | 550 | −13 |
| **OASIS** | **(960, 45)** | 700 × 650 | (1310, 370) | 1291 | −384 |
| **EVENTER** | **(216, 1130)** | 800 × 740 | (616, 1500) | 1496 | +361 |
| **MEDCOIN** | **(1174, 1224)** | 700 × 650 | (1524, 1549) | 2172 | +10 |

Reading steps: **638, 309, 676** — every city separates across the frame.

**OASIS moved 45 m north after its mouths were measured.** Its west mouth is at local y = 211
and XTIX's avenue at world y = 329; `329 − 73 − 211 = 45`. With that shift the two roads are
**one straight line** across the corridor instead of a 17° kink in open country. It costs 32 m
off the middle reading step (341 → 309) and is worth it: a road that bends for no visible
reason is the sort of thing that reads as a mistake.

Gaps between plates: XTIX–OASIS **150**, EVENTER–MEDCOIN **158**, XTIX–EVENTER **383**,
OASIS–EVENTER **480**, OASIS–MEDCOIN **574**, XTIX–MEDCOIN **600**.

### 3.3 The plate, and why it is bigger than the cities

Shadows fall **south-west**. XTIX's tallest point is 261.9 m — and it is a **crane**, not a
building, which matters for the contract in §9. It sits at the south-west corner, so it throws
shadow toward the map edge. If the plate stops at the city bounding box, that shadow is cut off
at the boundary — and a shadow clipped by a straight edge is the most obvious tell that a map
is a composite.

**The audit corrected the arithmetic here.** A shadow's horizontal displacement is
`0.2679 m per metre of height` **along the south-west diagonal**. Resolved onto x and y it is
`0.2679 / √2 = 0.1895` **per axis** — and a rectangular plate margin is sized by the per-axis
figure, not the diagonal one. XTIX's 261.9 m therefore needs **49.6 m** of margin per axis, not
70.2 m. The first draft used the diagonal, which was conservative but wrong in principle, and
it made the height ceiling in §9 too low by 113 m.

**The plate extends 73 m beyond the cities on every side: 2,020 × 2,020 m, cities inset at
(73, 73).** That is comfortably over the 49.6 m XTIX needs, and it gives START and END somewhere
to stand and the approach roads somewhere to run.

**The cost, stated plainly.** The vision set the cities at 60 % of the map and the green at
40 %. That holds against the *city bounding box* (60.0 %) but not against the *visible plate*,
where it is **51.6 %**. The 60 % was written before the four cities were built and measured;
the four plates are now fixed sizes and cannot be squeezed. Reaching 60 % of the visible plate
would mean no margin at all — clipped shadows and markers standing on the boundary.

**This is Oran's call, not mine, and it is Q1 in §11.** My recommendation is the 2,020 m plate:
the *spirit* of the 60/40 rule — cities dominant, green working in the gaps rather than lying
around as expanse — is intact at 51.6 %, and the corridors between cities (150–574 m) are what
that rule was really protecting.

### 3.4 The world camera

The audit found this missing: the plan specified every city's framing and never its own.
Derived in `world_plan.world_camera()` from the plate corners plus the tallest thing standing
on it, so it cannot drift from the layout.

| | |
|---|---|
| type | **orthographic**, matching all four cities |
| pitch · yaw | **54.7° · 45°** — the same as every city, so a zoom from L0 into L1 does not change the projection |
| frame | **2,857 m across · 1,651 m up**, aspect **1.73** |
| ortho_scale | **3,028** (6 % padding on the extreme corners) |
| location | (2317.5, −297.5, 2611.6), looking at the plate centre |

The frame's aspect of 1.73 sits comfortably inside 16:9 (1.78). The top of the frame is set by
**XTIX's crane**, not by a plate corner — a 261.9 m object lifts the frame `261.9 × sin 54.7° =
214 m`, which is why the camera is derived from heights and not just from the footprint.

---

## 4. The route — every join, exactly

The world road is one continuous route. Legs, with the mouth each end attaches to. Coordinates
are **city-bounding-box** coordinates; add (73, 73) for plate coordinates.

| leg | from | to | length | status |
|---|---|---|---|---|
Plate coordinates (city-box coordinates plus the 73 m margin). **Every leg begins and ends on
an approach point 30 m outside its mouth, along the edge normal**, so no road meets a city
boundary at an angle — the audit caught leg 2 arriving at EVENTER **37° off normal** before
this rule existed.

| leg | from | to | note |
|---|---|---|---|
| **0** | START (0, 329) | XTIX west (73, 329) | **XTIX gains a west approach, 136 m**, on its avenue at local y = 256 |
| **1** | XTIX east (883, 329) | OASIS west (1033, 329) | **one straight line** — the 45 m shift aligns them exactly |
| **2** | OASIS north (1363, 768) | EVENTER south (993, 1203) | **ramps 12.9 m over 593 m — 2.17 %** — to EVENTER's *elevated* mouth |
| **3** | EVENTER east (1090, 1543) | MEDCOIN south (1389, 1297) | leaves on the surface road, swings south around MEDCOIN's corner |
| **4** | MEDCOIN east (1947, 1837) | END (2020, 1837) | **no change** — MEDCOIN's existing east mouth |

### 4.0 The mouths, all measured

| city | side | local position | width | **z** | status |
|---|---|---|---|---|---|
| XTIX | W · E | y = 256 (its avenue) | 20 m | 0.052 | **to add** — 136 m / 135 m in its own margin |
| OASIS | W | **y = 211** | 8 m | 0.14 | **measured** — extend ~15 m to the edge |
| OASIS | E | **y = 491** | 8 m | 0.14 | **measured** — a secondary branch, not on the main route |
| OASIS | N | **x = 330** | 8 m | 0.14 | **to add** — 155 m spur |
| EVENTER | S | x = 704 | 20 m | **13.0** | as built — **the flyover** |
| EVENTER | E · W | y = 340 | 20 m | 0.14 | as built — at grade |
| MEDCOIN | S | x = 142 | 16 m | 0.14 | as built |
| MEDCOIN | E | y = 540 | 16 m | 0.14 | as built |

**OASIS's through road runs west→east but climbs 280 m across the plate** — in at y = 211, out
at y = 491. Its north spur goes at local **x = 330**, which is the column where its road comes
closest to the north edge: **155 m**, measured in 20 m columns across the whole plate rather
than taken from the road's northernmost point anywhere.

### 4.0b EVENTER is entered on the viaduct

**EVENTER's north and south mouths are at z = 13.0 m.** They are the interchange's flyover;
only its west and east mouths are at grade. This was found by measuring the mouth heights
instead of assuming they were zero, and it changes the route: the connector from OASIS **ramps
12.86 m over 593 m — a 2.17 % gradient** — the route arrives on the viaduct, crosses the
interchange, and leaves on the surface road at the east mouth.

That is exactly what an interchange is for, and it is a far better piece of storytelling than a
flat road would have been. It is also a hazard that would have surfaced only at build time.

### 4.1 Why MEDCOIN is entered from the south

MEDCOIN's only mouths are **S** (local x = 142) and **E** (local y = 540), and it will not be
re-cut. Entering south and leaving east places END at `(1874, 1764)` — reading position
**2,572**, the furthest right point in the frame. The reverse — enter east, leave south — puts
END at reading position 1,796, which is *to the left of MEDCOIN's own centre*. The journey would
appear to end by going backwards. **The direction is forced by the reading order, and it happens
to use both of MEDCOIN's mouths exactly as built.**

### 4.2 Leg 3 in detail

The direct line from EVENTER's east mouth to MEDCOIN's south mouth passes through MEDCOIN's
plate on its west side, where there is no mouth. The route therefore: east into the 158 m
corridor between the two cities → south down that corridor to y ≈ 1,170 → east along the open
green south of MEDCOIN → north into the south mouth at x = 1,316.

That reads as a road swinging around the edge of an industrial district before entering it,
which is what such approaches actually do.

**It costs one thing, and the audit measured it: the route runs 212 m backwards across the
frame** — 7.4 % of the 2,857 m frame width — during the southward part of the swing. Every
alternative was enumerated and is worse:

| alternative | why not |
|---|---|
| enter MEDCOIN by EAST, leave by SOUTH | END lands at reading 1,899, **left of MEDCOIN's own centre** at 2,276 — the journey would end by going backwards |
| leave EVENTER by its east mouth at y=1573 / 1613 / 1752 | all sit 276–455 m *above* MEDCOIN's south mouth — the dip only grows |
| leave EVENTER by a **south** mouth | no dip, but the route then enters and leaves EVENTER on the same edge and **never crosses the interchange** — against the brief's *"the point of the junction is to get through it: ALIGNMENT"* |

MEDCOIN's south mouth is at y = 1,297 and EVENTER's lowest east mouth at y = 1,543; MEDCOIN
cannot be moved north far enough to close that (it would leave the 1,874 m bounding box). So
the 212 m excursion is **structural, bounded, and accepted** — and on screen it is a road
bending toward the viewer around a near corner, which is what roads do.

### 4.3 What the four cities must gain

Only two cities are touched, and only in their **unbuilt plate margins** — no existing road is
re-aligned:

- **XTIX** — a west approach (130 m) and an east approach (140 m), both on the avenue at
  y = 256, running out through the planted verge to the plate edge.
- **OASIS** — a west mouth, an east mouth (both ~15 m of extension to reach the edge) and a
  north spur (~145 m).
- **EVENTER** — nothing.
- **MEDCOIN** — nothing.

---

## 5. Sun and shadow

**One sun, owned by the world. Every city's own SUN object is deleted on import** —
`world_merge.py` already does this (`SKIP_OBJECT = ("CAM_", "SUN", "TERRAIN_Base")`).

| | |
|---|---|
| elevation · azimuth | **75° · 135°** |
| energy · angular size | **0.8835 · 3.4°** |
| shadow direction | **south-west** |
| shadow length, along the diagonal | **0.2679 × height** |
| shadow displacement, **per axis** | **0.1895 × height** — the figure that sizes a margin |

Clearances, measured against the layout:

| city | tallest | reach per axis | falls onto | clear? |
|---|---|---|---|---|
| XTIX | 261.9 m (a crane) | **49.6 m** | the plate margin (73 m) | ✅ by 23.4 m |
| MEDCOIN | 72.2 m | 13.7 m | its own plate | ✅ |
| OASIS | 47.2 m | 8.9 m | its own plate | ✅ |
| EVENTER | 30.1 m | 5.7 m | its own plate | ✅ |

**No city casts a shadow onto another** — checked pairwise, sweeping each city's footprint
73 m south-west and testing it against all three others. The 73 m plate margin buys a height
ceiling of `73 / 0.1895 = 385 m`, which is contract item F7.

---

## 6. The ground — one continuous country

The four plates must stop being four plates.

1. **One world ground.** A single slab, plate top at **z = 0**, skirt to **z = −7** (matching
   OASIS, EVENTER and MEDCOIN; XTIX's skirt is −3 and will be extended). Every city's contents
   already sit on z = 0, so nothing moves vertically.
2. **Each city's own plate is kept, not deleted** — for XTIX and EVENTER the plate object also
   carries the roads and the city slab, so deleting it would delete the streets. Instead the
   plate is made **invisible as a boundary** by matching its green to the world's exactly.
3. **The world green is `(0.3629, 0.5183, 0.1065)`** — the value three of the four already
   share. **OASIS is re-graded to it.** This is a material change to OASIS and nothing else.
4. **The verge.** Each city already ends in a planted edge (XTIX's is 24 m). The world's
   planting continues across the join at the same density, so the eye finds no line.

---

## 7. The green country — what fills the other half

The green is not filler; it is the thing that makes four cities read as one country. It carries:

- **The route**, with its verges, hedgerows, markers and gates where branches leave it.
- **Branch roads that arrive somewhere.** v4's lesson, and it stands: every branch ends at a
  thing — a mill, a quarry, a cabin, a farm. Four cities and four outposts, one per corridor.
- **Woodland in stands, not scatter** — the eight-stand-type rule from v4, and the grove
  machinery now proven on XTIX (728 groves, 11,299 plants, 91 species, understory and meadow).
- **Density that falls away from the road**, so the corridors read as travelled and the corners
  as remote.

The corridors have different jobs and should not be planted the same:

| corridor | width | job |
|---|---|---|
| XTIX–OASIS | 150 m | the first leg — close, cultivated, hedgerows and gates |
| EVENTER–MEDCOIN | 158 m | the last leg — the road swings through it; scrub and worked ground |
| XTIX–EVENTER | 383 m | deep woodland, one outpost |
| OASIS–EVENTER | 480 m | the widest crossing; the road climbs through open country |
| OASIS–MEDCOIN | 574 m | the remotest ground; forest and a landmark |

---

## 8. Delivery — how the viewer scans and digs

**The constraint.** Page 1 is interactive WebGL (`canvas`, `drawArrays`, `createShader` in
`m/index.html`). v4 shipped **954 k drawn triangles as 3.58 MB base64**.

### 8.1 A correction the audit forced

The first draft of this section said the four cities are 17.5 M triangles, "about 65 MB at that
ratio", and that no compression closes an 18× gap. **That was wrong, and wrong in an important
direction.** It applied a payload rate to the *drawn* triangle count and ignored instancing —
which is where nearly all of the geometry goes.

`tools/world_payload.py` measures what actually has to ship: geometry that appears **once**
(procedural, unique) plus each **prototype** once, plus one transform per instance.

| | drawn faces | unique | prototypes | **shipped** | instances | ratio |
|---|---|---|---|---|---|---|
| **XTIX** | 6,444,242 | 818,317 | 59,974 | **878,291** | 20,733 | 7.3× |
| **OASIS** | 2,238,866 | 269,886 | 120,497 | **390,383** | 12,451 | 5.7× |
| **EVENTER** | 5,384,604 | 63,733 | 105,343 | **169,076** | 9,394 | **31.8×** |
| **MEDCOIN** | 3,425,094 | 40,627 | 255,228 | **295,855** | 4,854 | 11.6× |
| **total** | **17,492,806** | | | **1,733,605** | 47,432 | **10.1×** |

**17.5 M collapses to 1.73 M.** EVENTER draws 5.4 M faces and ships 169 k — it is almost
entirely instanced. XTIX is the heavy one, and for a specific reason: its **172 towers are
procedural and every one is different**, so 818 k of its 878 k is geometry that exists once.

### 8.2 What that means

Three tiers, still — but for a different reason than the first draft gave, and with real
numbers behind the split:

| tier | contents | measured |
|---|---|---|
| **L0 world** | four cities as **massing only** — tower volumes, podiums, roads, tree clumps; no facade detail, no people, no furniture | target **≤ 350 k triangles**, inside the proven v4 envelope |
| **L1 city** | one city, full detail, instanced | **XTIX 878 k · OASIS 390 k · EVENTER 169 k · MEDCOIN 296 k** shipped faces |
| **L2 detail** | Cycles stills at fixed angles | images, not geometry |

**On the byte figures, I am deliberately not giving a number I have not measured.** Converting
shipped triangles to base64 megabytes needs the real encoder — v4's own ratio cannot simply be
scaled, because its 954 k was a *drawn* count against a payload that was already instanced and
deduplicated. What is solid is the **shipped face count**, and that XTIX is 5.2× heavier than
EVENTER. The exporter must be run once against XTIX, the heaviest, before the L1 budget in the
contract (F8) is fixed. **That is step 9a in §10.**

**L0 is generated by the city's own generator with an `lod` flag**, not by decimating the built
mesh. Decimation would destroy the crisp low-poly silhouette the whole look depends on;
re-emitting the massing from the same parametric source keeps the proxy honest and guarantees
it still matches after any change inside the city.

## 9. The dynamism contract — the critical one

> *"Any change I want to make in the maps afterwards must be possible without harming the
> overall map — not a change to the road alignment, but a visual change that designs the map
> better."*

The first draft answered this with a flat list of eight frozen values. That was too blunt: it
froze things that did not need freezing, and it missed things that did — the mouth **heights**,
for one, which is how a 13 m flyover nearly went unnoticed.

**A change is made safe in one of three ways, and only the third is a real constraint.**

### 9.1 What the WORLD OWNS — change it freely, it has no effect

The city's version is discarded on import. `world_merge.py` already does this for the camera
and the sun (`SKIP_OBJECT = ("CAM_", "SUN", "TERRAIN_Base")`).

| | |
|---|---|
| the sun | one world sun: 75° / 135° / 0.8835 / 3.4° |
| the camera | one world camera: ortho, 54.7° / 45°, scale 3,028 |
| the world shader | one ambient — XTIX's 0.8 × 0.82, which was itself built to match the others |
| render settings | samples, resolution, output |
| **the boundary belt** | **the outer 40 m of every plate**, re-surfaced and re-planted by the world |

**The boundary belt is the most important line in this document.** The four verges are not
alike and never will be — XTIX has 11,299 plants in groves with understory, EVENTER a 93.4 %
canopy belt, OASIS garden planting, MEDCOIN nothing at all by design. Requiring them to match
would freeze precisely what Oran most wants to keep changing. Instead the world lays its own
ground and its own planting over the last 40 m of every plate, at one density and one palette.
**A city's edge treatment can then change completely and the join cannot show.**

### 9.2 What the WORLD ADAPTS TO — change it freely, the world follows

The world reads the value out of the city and matches it, so a change propagates instead of
breaking.

| | how |
|---|---|
| carriageway **colour** at each mouth | the approach road is built from **that city's own road material**. OASIS's blue-grey asphalt needs no change, and a later re-colour carries automatically |
| carriageway **height** at each mouth | the approach meets whatever z the mouth is at, ramping if it must — already proven by EVENTER's 13 m flyover at 2.17 % |
| the city's **internal** road layout | irrelevant to the world, as long as the mouths hold |

### 9.3 What the CITY MUST HOLD — the actual contract

Eleven items, each checkable. `tools/world_contract.py` — **to be written** — opens a city
`.blend`, checks all eleven, and exits non-zero on any breach. It runs before a changed city is
allowed back into the world, so the world is never rebuilt to find out whether a change broke it.

| # | must hold | value |
|---|---|---|
| **C1** | plate footprint, **including every overhang** — a crane jib counts | XTIX 810 × 747 · OASIS 700 × 650 · EVENTER 801 × 741 · MEDCOIN 700 × 650 |
| **C2** | plate origin in the world | XTIX (0,0) · OASIS (960,**45**) · EVENTER (216,1130) · MEDCOIN (1174,1224) |
| **C3** | ground plane | top **z = 0**, skirt to z = −7 |
| **C4** | every mouth's position, width **and z** | the table in §4.0 |
| **C5** | height ceiling | **385 m** — covers cranes, not just buildings |
| **C6** | colour management | Standard · look None · exposure 0 · gamma 1.0 · sRGB |
| **C7** | model scale | a person **1.70–1.80 m**; the world's tightest measured agreement |
| **C8** | no emissive materials | the world owns the light |
| **C9** | collection prefixes | the merge skips by prefix; renaming them breaks it silently |
| **C10** | L0 proxy | ≤ 90 k triangles |
| **C11** | L1 payload | set at step 9a, once the exporter has run against XTIX |

### 9.4 What is free — everything else

Buildings, shapes, heights under C5, facades, colours, materials, glass tints, crowns,
roofscapes, sky bridges, podiums, construction stage, cranes and their livery, hoarding,
sheeting, rebar, vehicles, people, signage, street furniture, planting of every kind,
courtyards, plaza, park, **and the whole verge**, because the world covers its last 40 m.

**Checked against the record: every change Oran has asked for across five rounds is free.**
The gloss pass, the texture repair, the axis fix, the signage, the landscape, the sky bridges,
the roof gardens, the crane livery — not one touches C1–C11.

### 9.5 The one thing that is not free

**Road alignment**, and specifically the mouths (C4). Oran has already said he will not ask for
it. If a mouth ever must move, the world route is re-planned — that is a world change, not a
city change, and it is the only case that forces one.

### 9.6 A caution the contract cannot cover

**Coherence is not the same as correctness.** XTIX's foliage is being re-graded from teal to
the world's green family (§13.2 ④) as a one-time fix, and afterwards tree colour is *free*. If
a future change pushes one city's palette a long way from the other three, every check here
will still pass and the world will still look wrong. That is a judgement, and it stays with
Oran — which is the right place for it.

---

## 10. Build order, and the gate at each step

Nothing proceeds until the step before it passes.

| # | step | gate |
|---|---|---|
| 1 | ~~measure OASIS's mouths~~ — **done**: W at y=211, E at y=491, N spur at x=330 | closed |
| 2 | write `world_contract.py`; run it against all four as they stand | four reports; F1–F8 known for each |
| 3 | re-grade OASIS's plate green, and XTIX's foliage to the world family | measured equal to the other three |
| 4 | add the XTIX and OASIS approaches (§4.3) | mouths measured at the plate edge, matching F4 |
| 5 | build the world ground, 2,020 × 2,020, and place the four plates | no overlap; gaps match §3.2 to ±1 m |
| 6 | lay the route, legs 0–4 | continuous; meets every mouth; no gradient break |
| 7 | plant the corridors and place the outposts | §7 densities; nothing within the road clear-zone |
| 8 | START, END, arrows and labels | legible at L0; reading order left to right |
| 9a | run the real exporter against **XTIX** — the heaviest, 878 k shipped faces | the L1 byte budget in F8 becomes a measured number instead of an estimate |
| 9b | L0 proxies from each generator's `lod` flag | ≤ 350 k triangles total |
| 9c | **re-render each city under the WORLD ambient** | EVENTER was authored 3.1x darker than OASIS; each city must still read once the world lights it |
| 10 | the world render, and the acceptance checks | one sun, no clipped shadow, no visible seam, no teal woodland |

**Memory.** `world_merge.py` records that appending OASIS (12.6 k objects) into a session
holding MEDCOIN (5.1 k) previously took Blender to unresponsive. The world is now **48 k
objects**. Step 5 must therefore be run **headless, one city at a time, saving between each** —
never in the interactive session.

---

## 11. Open questions

Four, and only the first needs an answer before work starts.

**Q1 · The 60/40 split.** The cities are 60.0 % of their own bounding box but **51.6 %** of the
2,020 m plate, and the plate needs its 73 m margin so XTIX's shadow is not clipped. Accept
51.6 % of the visible map, or tighten the corridors to buy it back? *My recommendation: accept
it. The corridors are what the rule was protecting.*

**Q2 · Which city sits at the front.** The layout puts **OASIS** nearest the viewer, at the
bottom of the frame, and EVENTER at the back. The alternative is to swap them — EVENTER read
close, OASIS from above. *My recommendation: leave it. An interchange is a plan-view object and
gains from being read from above; a neighbourhood gains from being close.*

**Q3 · Do the four cities keep their own colour identity?** The vision says each workplace is
dominated by its own colour. As built they are not — all four use natural materials with
saturated colour rationed to small things. That is MAP_ANALYSIS §1.5, and it is why they look
real. *My recommendation: keep the natural palettes and let each city's identity come from its
TYPE MIX — towers and cranes, houses and gardens, ramps and traffic, sheds and suits — which is
already true and is what MAP_ANALYSIS §3 argued for.*

**Q4 · START and END markers.** WORLD_STATE records that only XTIX has a date range on file
(2023–2026). If the other three have years, the markers can carry them; otherwise they carry
FILE numbers.
---

## 12. The audit — every parameter, re-checked

Oran asked for the plan to be gone over again and verified. Re-reading my own prose is how an
error survives, so `tools/world_audit.py` checks the **numbers** instead: every geometric claim
recomputed from `world_plan.py` and from the raw measurements, independently of the reasoning
that produced it. Rule 4 throughout — each check carries a deliberate break it is known to
catch.

**First run: 17 checks, 5 failed.** All five were real.

### 12.1 The one that mattered — the shadow arithmetic

A shadow's horizontal displacement is `0.2679 m per metre of height` **along the south-west
diagonal**. Resolved onto x and y it is `0.2679 / √2 = 0.1895` **per axis**, and a *rectangular*
plate margin is sized by the per-axis figure.

I had sized the margin from the diagonal. The consequence was not the margin — 73 m is
comfortably over the 49.6 m XTIX actually needs — but the **contract's height ceiling**, which
I had derived as `73 / 0.2679 = 272 m`. The correct value is `73 / 0.1895 = **385 m**`. I had
understated the ceiling by 113 m, which would have refused a perfectly safe building.

### 12.2 The delivery section was wrong, and in an important direction

I wrote that the four cities are 17.5 M triangles, "about 65 MB", and that no compression closes
the gap. That applied a payload rate to the **drawn** triangle count and ignored instancing.

`tools/world_payload.py` measures what actually ships — unique geometry, plus each prototype
once, plus one transform per instance. **17.5 M collapses to 1.73 M, a 10.1× reduction.**
EVENTER draws 5.4 M faces and ships **169 k** (31.8×); XTIX ships 878 k, because its 172 towers
are procedural and every one is different. Section 8 is rewritten around the measured figures,
and it no longer quotes a byte budget I have not measured — the exporter runs against XTIX at
step 9a and F8 is set from the result.

### 12.3 The other three

| | found | fixed |
|---|---|---|
| **plate rounding** | EVENTER planned at 800 × 740 against a measured **800.3 × 740.2** — the plan reserved 0.3 m *less* than the plate occupies | all four rounded **up**: EVENTER is 801 × 741 |
| **the route doubles back** | leg 3 runs **212 m backwards** across the frame | kept, and justified: every alternative enumerated in §4.2 and each is worse |
| **the world camera** | never specified — the plan gave every city's framing and not its own | derived in `world_camera()`, §3.4 |

### 12.4 Two faults in the audit itself

Worth recording, because a check that is wrong is more dangerous than no check:

- The shadow-decomposition test compared against a hard-coded `0.1894` and failed on a rounding
  digit — the true value is `0.18947`. It now checks the **relationship** (`per-axis × √2 =
  diagonal`), which cannot drift with a decimal.
- The doubling-back test simply reported a failure. It now **enumerates the alternatives** and
  passes only if none of them is clean — so the deviation is accepted on evidence rather than
  on my say-so.

### 12.5 And one drift it caught immediately

Rounding EVENTER's plate up by 1 m moved its centre half a metre, which moved the reading steps
from `606, 340, 677` to `606, 341, 676`. The document still quoted the old figures. A check now
verifies that **every headline number in this document is traceable to `world_plan.py`** — the
plan is code, the prose quotes it, and nothing else stops the two drifting apart.

**Second run: 18 checks, 0 failed.**

```
PASS  screen projection matches a first-principles camera basis
PASS  planned plate sizes are not smaller than measured
PASS  every plate sits inside the city bounding box, at MEASURED size
PASS  no two plates overlap, and the tightest corridor is >= 130 m
PASS  shadow decomposes as diagonal / sqrt2, and world_plan uses the per-axis figure
PASS  XTIX's shadow lands on the plate, not past its edge
PASS  the contract's height ceiling is derived from the PER-AXIS reach
PASS  no city casts a shadow onto another city
PASS  the four cities advance across the frame, in path order
PASS  START is left of XTIX and END is right of MEDCOIN
PASS  no route leg has a zero-length segment
PASS  no leg crosses a city it does not connect to
PASS  the route's one backward excursion is bounded and unavoidable
PASS  built fraction of the city bounding box is 60 %
PASS  built fraction of the visible plate is stated honestly as ~51.6 %
PASS  object and face totals match the survey
PASS  the world camera is specified, and frames the whole plate
PASS  every headline figure in the document is traceable to world_plan.py
```

### 12.6 What the audit does NOT cover

Stated so it is not mistaken for completeness:

- **OASIS's road mouths.** Still the one unmeasured number in the plan (§1.2, seam 3). Its
  streets are a lighter material than the rule that finds carriageway in the other three, so
  the west and north mouths in `world_plan.MOUTHS` are marked `None` and the route uses a
  provisional y = 256. **Step 1 of §10 closes this, and it must close before anything is laid.**
- **The L1 byte budget**, until the exporter is run (step 9a).
- **Anything that only appears when built** — how the join actually reads, whether the corridors
  feel like country, whether the labels collide at L0. A plan cannot check those; the acceptance
  gates in §10 are where they get caught.
---

## 13. The joins, measured to the bottom

Oran asked for this as deep as it goes: the colours, the angles, the roads, the trees,
everything. A join fails on **any** property that differs across it, so every one was measured
in all four cities and compared — `tools/world_join.py`, `world_join2.py`, `world_join3.py`.

### 13.1 What agrees

| property | finding |
|---|---|
| **sun** | identical in all four — 75° / 135° / 0.8835 / 3.4° |
| **camera** | identical — orthographic, pitch 54.7°, yaw 45° |
| **colour management** | identical — **Standard**, look None, exposure 0, gamma 1.0, sRGB. So an RGB value means the same thing in all four files |
| **scale** | a person measures **1.75 / 1.74 / 1.75 m** across three cities — **1 % agreement**. Cars 4.56–5.60 m and trees 7.1–10.2 m, both inside a real fleet's and a real wood's variation |
| **street grid** | all four axis-aligned; every road mouth is square to its plate edge |
| **carriageway colour, three of four** | XTIX, EVENTER and MEDCOIN all use (0.048, 0.050, 0.060) to four decimals |
| **plate green, three of four** | XTIX, EVENTER, MEDCOIN all (0.3629, 0.5183, 0.1065) |

Scale was the one that could have sunk the whole idea, and it is clean. A join survives a
colour mismatch; it does not survive a 4.5 m car meeting a 6 m one.

### 13.2 What does not agree — six findings

**① OASIS's plate green is a different green.** `(0.2462, 0.3516, 0.0723)` against the
`(0.3629, 0.5183, 0.1065)` the other three share — about 68 % of their brightness. Both
OASIS and MEDCOIN name it `MAT_country_grass`, which means the *same material* was graded in
one file and not the other.

**② OASIS's carriageway is a different asphalt.** `(0.133, 0.147, 0.216)` against
`(0.048, 0.050, 0.060)` — **three times brighter and tinted blue**. This is why every earlier
survey reported "no roads at any OASIS edge": the detector was calibrated to the other three.

**③ EVENTER's north and south mouths are 13 metres in the air.** They are the interchange's
flyover; only its west and east mouths are at grade. Every other mouth in the world is at
z = 0.14, and XTIX's carriageway at 0.052. **This changed the route** — see §4.0b.

**④ XTIX's foliage was teal where the other three are green — now re-graded.**

Oran asked for XTIX to be brought to "the world's leaf colour", **on the assumption that all
the maps are the same and in harmony**. Measured area-weighted in HSV, that assumption did not
hold:

| | hue | sat | value | foliage area |
|---|---|---|---|---|
| **XTIX** (as built) | **148.5°** | 0.699 | 0.685 | 266,073 m² |
| OASIS | 86.7° | 0.667 | **0.586** | 9,915 m² |
| EVENTER | 104.8° | 0.830 | **0.218** | 245,792 m² |
| MEDCOIN | 109.1° | 0.550 | 0.400 | 7,547 m² |

The three "green" cities are **not in harmony with each other**: their hues span 22.4°, and
**EVENTER's foliage is 2.7× darker than OASIS's** — a wider gap in value than XTIX's was in
hue. There was no world green to copy.

**So one was derived.** `world_plan.WORLD_FOLIAGE` — eight tints, hue **88–118°** centred on
the area-weighted mean of the three (**104.2°**, and EVENTER dominates it because it holds 96 %
of their foliage between them), value **0.24–0.67**, deliberately set to *contain* what the
three already do so a city coming to it shifts hue without losing its own light and shade. The
deck is weighted 1·2·1·3·3·2·2·1, because a real wood is mostly mid-tone with a few extremes.

**XTIX is done** — 11,652 material slots re-dealt, measured after: **hue 99.8°, sat 0.713,
value 0.482**, which places it centrally among the other three rather than 44° outside them.

**What is still outstanding, and the plan does not pretend otherwise:** the other three have
*not* been brought to the palette. Hue is now inside one band for all four, but **value is not**
— OASIS 0.586, XTIX 0.482, MEDCOIN 0.400, EVENTER 0.218. The audit carries a check that passes
while this work is outstanding and must be inverted once it is done.

Two faults in my own tooling surfaced doing it, both of the same kind — a cache mistaken for a
definition:

- `_tinted()` returned an existing material untouched, so every `XT_leaf_*` already in the file
  would have been handed back with its old teal and the re-grade would have silently done
  nothing.
- `foliage_variety()` only re-assigned slots holding a *kit* material name. After the first run
  every slot held `XT_leaf_N`, so a palette change re-coloured the materials but never re-dealt
  them — and with a 15-entry deck against 8 existing materials, only the **dark half** stayed
  in use. Measured value came out **0.389** against the deck's 0.480 until that was fixed.

**⑤ The four cities were authored under four different ambients.**

| | background | strength | effective |
|---|---|---|---|
| XTIX | 0.8 grey | 0.82 | **0.656** |
| OASIS | white | 1.00 | **1.000** |
| EVENTER | 0.8 grey | **0.40** | **0.320** |
| MEDCOIN | white | 1.00 | **1.000** |

**EVENTER's ambient is 3.1× darker than OASIS's.** Identical RGB does not mean identical
appearance: a material tuned under 0.32 lifts when the world lights it at 0.656. The world owns
one shader — XTIX's, which was itself designed to match the others — and **§10 gains a gate:
re-render each city under the world ambient and confirm it still reads.** This cannot be
resolved on paper.

**⑥ Object density varies 3.3×.** XTIX 350 objects/ha, OASIS 276, EVENTER 159, MEDCOIN 107.
MEDCOIN is deliberately sparse — *"no forest, no crowd, no street furniture — the absence is
the content"* — but next to XTIX it will read as empty. Not a fault; a composition note for
when the world is first rendered.

### 13.3 The angles

All four street grids are axis-aligned, and every mouth is square to its plate edge, so the
world reads as one survey rather than four things dropped at angles. Three deliberate
exceptions, all internal: EVENTER's ramps at 27–31°, OASIS's houses at varied yaws (it is a
suburb), and XTIX's `twist` and `lean` towers.

**The route now meets every mouth at 0.0° off normal.** Before the approach rule, leg 2
arrived at EVENTER 37° off — the sort of thing that looks wrong to someone who cannot say why.

### 13.4 The trees, at the join specifically

Beyond colour, the four verges differ in kind: XTIX has a 24 m planted verge with groves,
understory and meadow (11,299 plants); EVENTER a 5,132-object planting belt at 93.4 % canopy;
OASIS garden planting; MEDCOIN 866 groves of 7,313 plants, added 2026-08-29. Requiring four verges to match would
freeze exactly the thing Oran most wants to keep changing.

**So the world plants the last 40 m itself** — see §9.2. The belt is world geometry, laid over
whatever the city has there, at one density and one palette. A city's planting can then change
completely and the join cannot show.


---

## 14. The drawing set

Five sheets. Sheets 1 and 2 are drawn **from the plan** — they show intention. Sheets 3, 4
and 5 are drawn **from the built scenes** — they show fact. That distinction is the point of
the set: if the two halves ever disagree, the plan is wrong, and the disagreement is visible
rather than argued about.

| sheet | file | what it is | source |
|---|---|---|---|
| 1 | `world_draw.py` → `WORLD_PLAN_1_layout.png` | layout: plate, plates, corridors, route, mouths | `world_plan.py` |
| 2 | `world_draw.py` → `WORLD_PLAN_2_reading.png` | the same as the CAMERA sees it, in reading order | `world_plan.py` |
| 3 | `world_draw3.py` → `WORLD_PLAN_3_whole.png` | **THE WHOLE MAP** — every city's real ground, in plan | `world_grid.json` |
| 4 | `world_draw4.py` → `WORLD_PLAN_4_height.png` | height, light, massing and the harmony check | `world_grid.json` |
| 5 | `world_draw5.py` → `WORLD_PLAN_5_iso.png` | **THE ISOMETRIC KEY** — the same grid extruded and projected | `world_grid.json` |

Bound as `world-build/WORLD_MASTER_DRAWINGS.pdf`.

### 14.1 The measured grid

`world_grid.py` opens each of the four `.blend` files headless and classifies the ground on a
common **8 m** grid: `free` / `planted` / `paved` / `built`, plus the **roof elevation** of
every built cell. 33,413 cells over the four cities, 5,760 of them built. Sheets 3, 4 and 5
are all drawn from that one file, so they cannot disagree with each other.

Two faults were found and fixed while building it, both of the same family — *a proxy was
measured instead of the property*:

- **Colour decided before height.** XTIX's jade and teal curtain walling sits at hue 146 and
  176 with the saturation and value of foliage, so the first classifier called its towers
  vegetation and reported **328** built cells against MEDCOIN's 1,352. Nothing growing in
  these kits reaches 15 m; height now decides first, and XTIX reports **3,157**.
- **Roof levels quantised to 2 m** over 93 printable characters caps at 180 m, which would
  have silently flattened every tower in XTIX below its real 261.9 m. The step is 4 m, which
  reaches 372 m — above the tallest roof and below the 385.3 m ceiling of contract F7.

### 14.2 What sheet 4 found

Panel C asks the question §9 keeps raising in words: *do the four plates read as one world?*
It answers it in numbers, and the answer is **not yet**.

| plate | planted | free grass | paved | built |
|---|---|---|---|---|
| XTIX | 51 % | 13 % | 4 % | 33 % |
| OASIS | **86 %** | 0 % | 4 % | 10 % |
| EVENTER | 27 % | **50 %** | 18 % | 6 % |
| MEDCOIN | 53 % | 19 % | 9 % | 19 % |

The leaf **colour** is harmonised — hue spread 9.5°, value ratio 1.33× (§12). But EVENTER's
plate is **half bare mown grass** and OASIS's is **seven-eighths wood**, and at full zoom-out
that is a light square next to a dark one whatever the leaves are doing. The ground mix, not
the leaf palette, is what the eye reads at 2,020 m.

This is a composition decision, not a defect, and it belongs to Oran:

- **level the two ends** — thin OASIS toward ~65 % and plant EVENTER's verge up toward ~45 %,
  giving a band of roughly 45–65 % across all four; or
- **keep the contrast and make it deliberate** — an interchange in open country next to a
  town in a forest is a legible story, provided the *transition* between the two plates is
  planted rather than abrupt.

Either way the fix lives inside a plate or in the world belt of §9.2, so it does not touch
the roads, the mouths or any other city — the dynamism contract holds.

### 14.3 Massing

| city | tallest | mean roof | built cells | plan share |
|---|---|---|---|---|
| XTIX | 261.9 m | 112.7 m | 3,157 | 33 % |
| OASIS | 47.2 m | 11.4 m | 706 | 10 % |
| EVENTER | 23.7 m | 13.6 m | 545 | 6 % |
| MEDCOIN | 72.2 m | 23.0 m | 1,352 | 19 % |

XTIX carries the world's height by an order of magnitude and this is correct — it is the
first city the visitor meets and the one the portfolio is about. The headroom under the
385.3 m ceiling is **123.4 m**, so XTIX can grow by nearly half again before its shadow
would reach the edge of the plate.

The PATH is **3,983 m** from START to END, and the tallest thing standing within 200 m of it
is 260 m — XTIX's crown, met in the first quarter of the journey.


---

## 15. Rev B — the plan verified across five trades

Oran asked for the document itself to be checked as architecture, structure, engineering,
contracting and development, and separately gave one instruction: *a road that runs to the
edge of its own city and stops there must be carried on to the edge of the world plate.*

`world_verify.py` runs 22 checks. **15 pass, 7 fail.** The transcript is
`renders/WORLD_VERIFY.txt`. Every check names its source, because a check that quotes the plan
back at itself proves nothing:

| tag | source |
|---|---|
| `[grid]` | `world_grid.json` — the four `.blend` files rasterised at 8 m |
| `[blend]` | `world_mouthcheck.json` — road geometry read straight out of the `.blend` files |
| `[edge]` | `world_edges.json` — road corridors measured at each plate edge |
| `[plan]` | `world_plan.py` — only ever the thing being **tested** |

### 15.1 The serious one: five declared mouths have no road behind them

The plan declares 11 mouths. `world_mouthcheck.py` opens each city and asks how close road
geometry — found by the carriageway **colour** each city was measured to have, not by object
name — actually gets to the declared point.

| mouth | nearest road | verdict | on the PATH |
|---|---|---|---|
| XTI-W | 130.2 m | **no road** | yes |
| XTI-E | 140.2 m | **no road** | yes |
| OAS-N | 147.2 m | **no road** | yes |
| EVE-S | stops 83.4 m short | elevated road, short | yes |
| EVE-N | stops 82.9 m short | elevated road, short | no |
| OAS-W, OAS-E, EVE-E, EVE-W, MED-S, MED-E | ≤ 12 m | real | |

**Four of the PATH's eight joins land on road that is not there.** XTIX's street grid stops
128 m inside its own plate on the west and 138 m on the east — the verge there is not the 24 m
the plan assumes, it is over 130 m.

**Correction to the first version of this section.** It said the plan "declared these mouths
as built and they were not built". That is wrong for three of the five. XTI-W, XTI-E and OAS-N
were recorded **TO ADD** with estimates of 136, 135 and 155 m, and measurement returned 130.2,
140.2 and 147.2 — the plan's own estimates held to within 8 m. Declaring work is not a fault.
**Only EVE-S and EVE-N were recorded "as built" and are not**, each stopping 83 m inside the
plate. Those two are the overstatement, and they are the only one the audit found.

584 m of road is needed to make the eleven declarations true. It is drawn on sheets 3, 4 and 5
as **PROPOSED**, dashed — a plan shows proposed work, it does not pretend the work is done.
Every metre of it is inside a city plate, so §9's dynamism contract covers it.

### 15.2 Oran's rule, applied

`world_edges.py` walks the perimeter of each city's classified grid and collects the runs of
paved cells that touch it, merging runs less than 24 m apart because a dual carriageway with a
median reads as two runs and an interchange's slip roads read as five.

**14 road corridors reach a plate edge.** Four carry the PATH into the next city. The other
ten now run on to the world boundary — **2.92 km of stub**, drawn at each corridor's measured
width from `world_stubs.band()`, which sheets 3 and 5 both call so they cannot disagree.

| city | side | at | width | carriageways | continuation |
|---|---|---|---|---|---|
| OASIS | W | 208 | 16 m | 1 | the PATH |
| OASIS | E | 488 | 16 m | 1 | **287 m to the world boundary** |
| EVENTER | W | 80 | 16 m | 1 | 289 m to the world boundary |
| EVENTER | W | 372 | 88 m | 4 | 289 m to the world boundary |
| EVENTER | W | 672 | 32 m | 2 | 289 m to the world boundary |
| EVENTER | E | 380 | 104 m | 5 | the PATH |
| EVENTER | E | 548 | 24 m | 2 | 157 m — **BLOCKED by MEDCOIN** |
| EVENTER | S | 76 | 8 m | 1 | 383 m — **BLOCKED by XTIX** |
| EVENTER | S | 212 | 8 m | 1 | 383 m — **BLOCKED by XTIX** |
| EVENTER | S | 400 | 80 m | 4 | 383 m — **BLOCKED by XTIX** |
| EVENTER | S | 488 | 16 m | 1 | 383 m — **BLOCKED by XTIX** |
| EVENTER | N | 404 | 88 m | 4 | 76 m to the world boundary |
| MEDCOIN | E | 540 | 24 m | 2 | the PATH |
| MEDCOIN | S | 140 | 24 m | 1 | the PATH |

The OASIS-E line is the one Oran marked in yellow. It is drawn.

### 15.3 Five conflicts that need a decision

A stub drawn straight through a city it was never routed around would be worse than admitting
there is a junction to design, so blocked stubs stop at the conflict and carry a red bar.

**EVENTER's four south carriageways all run at XTIX.** EVENTER sits directly north of XTIX and
its south corridors land on XTIX's north verge, which has no mouth. The 80 m four-carriageway
corridor at local x=400 is the main north–south motorway of the interchange.

Recommendation, in order of preference:

1. **Give XTIX a north mouth and let the 80 m corridor become a real road into the city.** A
   motorway running south out of the interchange into the tower city is the most legible thing
   on the sheet, and it explains why the interchange exists. It is a road-alignment change, so
   it is a deliberate plan revision, not a free visual edit.
2. **Fan the three minor corridors (8, 8, 16 m) east into the 150 m XTIX–OASIS corridor** and
   run them south from there. No city is touched.
3. **Terminate them inside EVENTER** so they never reach the edge. Cheapest, and it throws away
   the interchange's whole reason for being.

**EVE-E(548) runs at MEDCOIN** — 157 m, then MEDCOIN's west edge, which has no mouth. Same
three options; option 1 here means a MEDCOIN west mouth.

### 15.4 The other four failures

| ref | check | the number | what it means |
|---|---|---|---|
| **A1** | the four plates read as one ground | planted share spans **59 points** — OASIS 86 %, EVENTER 27 % | §14.2. A design decision, Oran's |
| **A2** | no plate reads as unfinished | EVENTER is **50 % bare mown grass** | the same decision, from the other side |
| **C4** | each join has a width transition | EVE-E **104 m** meets MED-S **24 m**, 4.3× | a motorway meeting a city street needs a taper and a slip; the plan details neither |
| **C5** | levels agree at each join | XTI-E to OAS-W is an **88 mm** step | a bump, not a ramp. Needs a 10 m taper |
| **C7** | one carriageway colour | OASIS luminance **0.149** against **0.050** — 3.0× lighter, blue-cast | two different-coloured roads meet at every OASIS join. Either re-grade OASIS's asphalt to the world value or accept it as a town-versus-motorway distinction and grade the *connector* to match at the join |

### 15.5 What passed

All three structural checks (B1–B3): the tallest roof is 261.9 m against a 385.3 m ceiling,
123.4 m of headroom, and its shadow reaches 49.6 m per axis into a 73 m margin. All four
contracting checks (D1–D4): 47,987 objects, 17.5 M faces drawn against 1.73 M shipped, the 8 m
grid overruns no plate by more than one cell, and the proposed work is quantified at 584 m plus
2.92 km. All four development checks (E1–E4): the scroll order is the career order, the reading
steps are 638 / 309 / 676 m, the world fits the camera frame, and the PATH is 3,983 m.

### 15.6 What has NOT been done

Nothing has been built. The four cities are still four separate `.blend` files; the 584 m of
proposed road, the 2.92 km of stub and every conflict resolution exist only as drawings. That
is what was asked for.


---

## 16. Rev C — XTIX takes EVENTER's motorway

Approved by Oran 2026-08-29: EVENTER's interchange sends a road south into XTIX, and XTIX
gains a north mouth to receive it. **21 of 25 checks now pass**, against 15 of 22 at rev B.

### 16.1 Why the mouth is not where the motorway points

The corridor leaves EVENTER **80 m wide, four carriageways**, at world x = 689. Carried
straight south it lands at **XTIX local x = 616**, and `xtix_north.py` reports what is there:

```
what is at local x=616, from y=636 down to y=440:  T########.########PT#####
   -> BUILDINGS
```

A building block. XTIX has only four real north–south avenues, and the choice between them is
a measured trade, not a preference:

| avenue, XTIX local x | width | paving through the north band | shift needed | deflection |
|---|---|---|---|---|
| **508** | 8 m | 12/25 | **108 m** | **15.7°** |
| 440 | 16 m | 16/25 | 176 m | 24.7° |
| 368 | 16 m | 16/25 | 248 m | 32.9° |
| 148 | 8 m | 17/25 | 468 m | 50.7° |

**x = 508.** The 108 m of lateral shift is taken in the 383 m belt between the plates, where it
costs nothing and bends no city's grid.

### 16.2 The gateway

An 80 m four-carriageway motorway does not meet an 8 m street. It ends at a **gateway junction
in the belt**, and a 20 m boulevard goes on into the city:

| segment | length | width | bearing |
|---|---|---|---|
| trunk, out of EVENTER | 140.0 m | 80 m | 180.0° |
| gateway junction | — | 80 → 20 m | — |
| boulevard, into XTIX | 265.9 m | 20 m | 204.0° |
| **total** | **405.9 m** | | **24.0° deflection** |

Then 107 m more inside XTIX's north verge to the head of the avenue at local y = 632 —
**PROPOSED**, dashed on every sheet.

The gateway is also where the width transition lives, which is the C4 fault answered. It is
recorded in `world_plan.LINKS`, and `links()` and `link_geometry()` derive everything from the
measured corridor station — no number on the drawing is typed twice.

**LINKS are not the PATH.** The PATH is the portfolio's scroll order and nothing else belongs
on it. A LINK is a road that joins two cities without being narrated. It is drawn solid with a
thin pale centreline; the PATH keeps its yellow dashes.

### 16.3 Two checks that were wrong, and are now right

Rev B reported seven failures. Two of them were faults in the audit, not in the plan.

**C4 compared things that do not meet.** It held EVE-E's **104 m corridor** — five parallel
carriageways of the interchange, only one of which the PATH uses — against MEDCOIN's 24 m road
and called it a 4.3× mismatch. The join is between the **declared mouths**, and the length
available to change between them is the connector's:

| join | width change | over | taper |
|---|---|---|---|
| XTI-E → OAS-W | 20 → 8 m | 150 m | 1:12 |
| OAS-N → EVE-S | 8 → 20 m | 593 m | 1:49 |
| EVE-E → MED-S | 20 → 16 m | 605 m | 1:151 |
| LINK | 80 → 20 m | at a junction | — |

**C5 called 88 mm a step.** There are 150 m of connector between XTI-E and OAS-W to take it
up — 0.059 %. Nothing meets at a point:

| join | level change | over | gradient |
|---|---|---|---|
| XTI-E → OAS-W | 0.088 m | 150 m | 0.059 % |
| OAS-N → EVE-S | 12.860 m | 593 m | 2.168 % |
| EVE-E → MED-S | 0.000 m | 605 m | 0.000 % |
| LINK | 0.088 m | 406 m | 0.022 % |

C2 was also replaced. It had been hard-coded to pass — the exact fault this harness exists to
catch — and now tests whether each clear stub's endpoint lands on the world boundary. It does,
to 0.00 m.

### 16.4 What is left, and it is all Oran's

| ref | what | the number |
|---|---|---|
| **C3** | 4 minor corridors with no destination | EVE-S 8 m, 8 m, 16 m at XTIX; EVE-E 24 m at MEDCOIN |
| **A1** | the four plates do not read as one ground | planted share spans **59 points** |
| **A2** | one plate reads as unfinished | EVENTER **50 % bare mown grass** |
| **C7** | the carriageways are not one colour | OASIS luminance **0.149** vs **0.050**, 3.0× |

**C3 is deliberately open.** A road needs a **destination**, and the world boundary is only one
kind of destination — a farm, an industrial estate, a service area or a junction is another.
Setting the destinations of these four is the first job of the belt plan, §17, and inventing
2 km of road before that plan exists would be building backwards.


---

## 17. The belt

Oran, 2026-08-29: the green between the cities is large, it must not be plain green, and the
engineering has to be settled before anything visual is decided. Three decisions he made:
the belt **grades between** the cities rather than the plates being levelled; **~35 % worked,
~3 % built**; and OASIS's carriageways **levelled to the world value**.

### 17.1 The technical layer — the canopy target field

`world_belt.py` measures what every city presents in the outermost 40 m inside each of its
sixteen edges. That is the boundary condition: whatever the belt does against an edge, it has
to continue *that*, or the seam shows.

| city | edges | planted | the belt must meet it with |
|---|---|---|---|
| OASIS | W E S N | 98–100 % | closed wood |
| XTIX | W E S N | 69–82 % | wood |
| MEDCOIN | W E S N | 60–79 % | wood, scrub on E |
| **EVENTER** | W E S N | **19–33 %** | **open field**, scrub on E |

So the belt is not painted to a boundary drawn by hand. `world_draw6.py` computes a continuous
**canopy target field** over every 8 m cell:

```
target(p) = Σ wₑ · plantedₑ / Σ wₑ        wₑ = 1 / (dist(p, e) + 40 m)²
```

over all sixteen edges. It runs **20.0 % to 99.3 %, mean 66.0 %**. Plant to this field and no
seam can show, because the field *is* the cities' own edges extended into the belt.

**This is the answer to A1 and A2.** The four plates are not levelled to match. XTIX is a city
in forest and EVENTER an interchange in open farmland, and the belt makes that read as
**geography** rather than as inconsistency. The hardest transition, XTIX 82 % to EVENTER 19 %,
has 383 m of belt to do it in, and the field grades it automatically.

The belt is **1,920,576 m² = 47.1 % of the plate, in one connected region** — it wraps all four
cities rather than sitting between them in pieces. Roads reserve 12.3 % of it. 29.1 % lies more
than 150 m from any city.

### 17.2 The four roads that went nowhere

C3 is discharged. **A road needs a destination, and the world boundary is only one kind.**

| corridor | width | destination | result |
|---|---|---|---|
| EVE-S 76 | 8 m | North Field farm | 257 m of road removed |
| EVE-S 212 | 8 m | Mid Field farm | 257 m removed |
| EVE-S 488 | 16 m | Crossroads services | 161 m removed |
| EVE-W 672 | 32 m | Eventer West works | 260 m removed |
| EVE-E 548 | 24 m | joins the PATH at its bend | a junction is a destination |

**935 m of road came out of the plan**, because a lane that ends at a farm gate does not also
run on to a city it never reaches. EVE-E 548 got no site: the EVENTER–MEDCOIN corridor is 157 m
wide and already carries the PATH through x = 1169, so there is no room for an estate in it.

### 17.3 The programme

Ten sites, declared and then verified — never searched for, never quietly moved.

| | site m² | built m² |
|---|---|---|
| Eventer West works | 37,380 | 16,821 |
| 4 farms | 112,136 | 10,092 |
| 3 service stops | 33,856 | 6,093 |
| 2 hamlets | 57,652 | 15,898 |
| 8 field structures | — | 5,916 |

| | area | share | target |
|---|---|---|---|
| worked land | 663,676 m² | **34.6 %** | 35 % |
| settled | 128,888 m² | 6.7 % | — |
| built footprint | 54,822 m² | **2.85 %** | 3 % |
| woodland | 1,128,011 m² | 58.7 % | the rest |

Industry sits **west of EVENTER** because that is the only open flat ground in the world —
every other edge presents 60–100 % canopy, and clearing wood for sheds would fight the belt's
own character.

### 17.4 Three faults in the checking, not in the plan

Each was found by the checks failing, and each was a fault in *how* the check was written:

1. **The clearance test used the site's centre.** A 110 × 100 m site whose middle is 14 m from
   a carriageway has a corner on it. Now the whole rectangle's perimeter is tested.
2. **Site clearance and building setback were conflated.** A farm must have its gate on the
   lane and a filling station its forecourt on the road — a **site** is supposed to touch the
   carriageway. What may not sit in the verge is a **building**. Now: site 4 m, building 12 m.
3. **A field with a road through it was rejected.** That is a normal field. Worked areas are
   now **net**: the carriageway is deducted, not the field.

A fourth was found in the plan itself: two lanes "served" a site the lane never reached, so
the truncation removed 0 m and the lane still ran past its own destination into empty grass.
Both sites were moved onto their lanes.

Seven sites were auto-fitted to the nearest position passing every check — largest move 108 m,
every one reported. **Every site now passes every check.**

### 17.5 OASIS's carriageways

C7 discharged. `oasis_road.py` surveyed before painting anything, because the last time a
material was changed across a whole city by a colour test, 2,615 objects were painted flat
beige. The survey found exactly **one** material — `MAT_ribbon_asphalt`, 47,788 m², on
`OASIS_MAIN`, `OASIS_STREETS` and `OASIS_CULDESAC`, and nothing else. It was levelled from
luminance 0.1490 to the world's 0.0501, and re-measured from the saved file.

**22 of 25 checks now pass.** The three that remain — A1, A2 and C3 — are all discharged by
this section rather than by the cities, and the audit will report them closed once §17 is built.


---

## 18. The belt re-audited, and the visual plan

### 18.1 The re-audit — 19 of 19, and four faults it found

Oran asked for the belt to be verified again to the smallest points. `world_beltverify.py`
does not add rectangles. **It rasterises**: every 4 m cell of the 2,020 m plate is classified
exactly once, in priority order — city, road, site, worked, woodland — so the areas are counts
and an overlap becomes a measurable quantity instead of an accounting risk.

It found four things the rectangle-adding version could not:

| | what | size |
|---|---|---|
| 1 | **North Field farm overlapped Mid Field farm** | 12,185 m² |
| 2 | **Six worked blocks overlapped sites** | 83,456 m² |
| 3 | **Two field structures stood inside a site** | — |
| 4 | **The area balance double-counted the roads** — "woodland = the rest" charged the same ground as both carriageway and wood | — |

And the root cause of (1) was a fault in the fitter, not in the placement: **`site_ok` tested
canopy, carriageways, city distance and the plate, and said nothing about other sites.** So the
auto-fit, trying to get Mid Field farm off the LINK boulevard, slid it 28 m west straight into
North Field farm and reported success. A fitter that does not know what is already placed will
always do this.

Three more were faults in the checking itself:

- **The clearance test used the site's centre.** A 110 × 100 m site whose middle is 14 m from a
  carriageway has a corner on it.
- **Site clearance and building setback were conflated.** A farm must have its gate on the lane
  and a filling station its forecourt on the road — a *site* is supposed to touch the
  carriageway; a *building* is not. Worse, a site that **serves** a lane must contain it, and
  the clearance test then measured the site against that same lane and failed it. A site is now
  measured against every road **except the one it serves**.
- **`in_rect` used inclusive bounds.** Clipped rectangles share edges by construction, so a cell
  centre landing exactly on a shared edge belonged to both, and the counter reported 12,240 m²
  of double-claimed ground that did not exist.

Fields are now **clipped** around the sites rather than moved — a field beside a farm stops at
the farm's fence — and clipped against each other in order. Field structures are **generated
from the fields** instead of typed in, so none can land on a road.

**Final:**

| class | m² | of belt |
|---|---|---|
| orchard | 261,440 | 13.3 % |
| crop | 166,208 | 8.5 % |
| farmyard | 96,240 | 4.9 % |
| pasture | 90,048 | 4.6 % |
| **worked** | **613,936** | **35.3 %** (dial 35 %) |
| hamlet | 57,952 | 2.9 % |
| works | 36,240 | 1.8 % |
| services | 34,128 | 1.7 % |
| road | 101,344 | 5.2 % |
| woodland | 1,043,952 | 53.1 % |

Built footprint **2.6 %** against a 3 % dial, against EVENTER's 6 % and XTIX's 33 %.

### 18.2 The visual plan — sheet 8

Four rules decide everything, and the fourth was written after the first run drew 36 M faces.

1. **Density follows the canopy field.** At a point whose target canopy is *c*, the planting
   rate is *c*/100 of 160 per hectare. That is what grades EVENTER's open field into OASIS's
   closed wood with no boundary anywhere: **11,965 trees over 1,113,024 m²**.
2. **The belt is low.** The tallest element is 15.4 m against EVENTER's 23.7 m. The moment a
   belt building competes with the smallest city, the world stops reading as
   cities-in-countryside.
3. **Everything is axis-aligned**, like every building in all four cities. At yaw 45° a box on
   the world axes shows two faces and a roof; a box at any other angle shows three and reads as
   a mistake. Farmyards are the only exception — their buildings face the yard.
4. **Face budget follows pixel size: at most 40 faces per pixel of apparent height.**

Rule 4 exists because of a real error. The first pass chose Detailed_Farm's `Tree01` for the
orchard — **4,370 faces on a tree that is three pixels tall**, 1,240 faces per pixel. 7,065 of
them came to **30.9 M faces, more than the four cities put together**. The asset is not wrong;
using it at that size is. Swapped for shapespark's `Tree-01-4` at 191 faces, the orchard costs
1.35 M and at 6 px nobody can tell.

| | before | after |
|---|---|---|
| belt faces drawn | 36.0 M | **4.27 M** |
| against the cities' 17.5 M | 206 % | **24 %** |
| shipped | (miscomputed as 34.9 M) | **0.076 M** |

The shipped figure was also wrong: it multiplied an average by a count. Shipped is the sum of
the **unique** meshes, once each — 87 of them.

**Still over budget, and honestly reported:** `Solid_65.001` (4,840 faces, 412/px, 87 k total)
and the Peterbilt (7,887 faces, 1,747/px, 71 k total). Both are worth decimating and neither is
expensive enough to block anything.

### 18.3 Sun, bearing and the seam

Sun at 75° / 135°, shadows SW at 0.1895 × h per axis. A 12 m barn throws 2.3 m; a 15.6 m
conifer throws 3.0 m. **Shelter belts go north-west of every yard** — on the shadow side, so the
yard itself stays lit.

The seam is not detailed anywhere, because there is nothing to detail: the canopy field runs
continuously from each city's own measured edge value out into the belt. XTI-W leaves at 69 %
and stays near it; OAS-S leaves at 100 % and falls to 68 % over 300 m; EVE-W leaves at 24 % and
rises to 40 %. Nothing meets at a line.

### 18.4 The asset folder

21 files in `Desktop/BLENDER/NEW`. **19 opened and were measured; none failed.** Three RAR
archives could not be extracted — valid headers, not corrupt, but every entry inside is
compressed and no extraction tool is installed on this machine. Full report in
`renders/NEW_ASSET_SCAN.txt`. Seven files ship without their textures, eight are at the wrong
scale (one is 90 km across), `k+700+Kirovets.obj` has an exact duplicate, and
`peterbilt_model.blend1` is a Blender backup rather than the file the author shipped.

None of the scale problems is a fault: every model is normalised on import to a declared real
size, so that list is a list of numbers to declare, not things to fix.


---

## 19. Rev D — the road network, and the rule that no road may end

Oran, 2026-08-29, two notes that turn out to be one problem:

> every one of these new areas needs tracks or roads — there has to be sensible access to the
> farms, the fields, the filling stations, the houses

> no road may be cut off in the middle of the map. Every road must branch or continue
> somewhere. The only place a road may be cut is where it reaches the boundary of the whole
> map, or where it joins another road.

**The second breaks §17.** It cut four lanes short "at their gate" and called a farm a
destination. Under this rule a gate is not a termination — the lane still stops in the middle
of the world.

And the answer to both notes is the same piece of geometry:

> **A lane runs THROUGH the site it serves and carries on.**

That gives the farm its access and gives the road somewhere to go, with one road instead of a
road plus a spur.

### 19.1 The rule, as `world_net.py` enforces it

Every road segment end must be one of:

| verdict | meaning |
|---|---|
| **BOUNDARY** | on the edge of the 2,020 m plate |
| **MOUTH** | on a city's plate edge, where that city's own network continues it |
| **JUNCTION** | within 12 m of another road's centreline |

Anything else is a **DEAD END** and is reported as a failure. The check is a search over the
whole network, not an assertion: a probe lane stopping at (400, 1100), 255 m short of anything,
is graded DEAD END.

### 19.2 The belt network

Two new roads carry everything:

| road | from | to | width |
|---|---|---|---|
| **belt collector** | west boundary (0, 845) | crossroads with the corridor road | 12 m |
| **corridor road** | that crossroads | southern boundary (958, 0), crossing the PATH at y=329 | 12 m |

The collector threads the **42 m** between XTIX's north edge at y=820 and the first farmyard at
y=862 — 15 m clear of the city, 13 m clear of the farm. The corridor road runs down the centre
of the 150 m XTIX–OASIS gap.

EVENTER's three south lanes now run from its plate edge **through** their farm or service area
and on to the collector. EVE-W 672 runs through the works and on to the west boundary.
EVE-E 548 turns south in the corridor and joins the PATH at its bend.

**Result: 36 road ends across 18 roads — 9 on the world boundary, 19 at a city mouth, 8 at a
junction, and 0 stopping in a field. 6.29 km of road, of which 2.88 km is new belt network.**

### 19.3 Every site re-sited onto a road

Six sites moved so that a through-road crosses them:

| site | now on |
|---|---|
| Corridor services (was Gateway services) | the crossroads of the collector and the corridor road |
| East Oasis hamlet | the OAS-E road, moved to straddle y=606 |
| West Eventer farm | the EVE-W 80 lane, moved to straddle y=1283 |
| North Eventer farm | the EVE-N 404 lane, moved to straddle x=693 |
| Oasis road stop | leg 2 of the PATH, where the traveller is furthest from anywhere |
| South crossing (was South Xtix crossing) | where the corridor road meets the southern boundary |

### 19.4 A contradiction in the checks, generalised

§18 found that a site serving a lane must **contain** it, and that the clearance test then
measured the site against that same lane and failed it — fixed by excluding "the lane it
serves". Rev D makes every site have a through-road, so the same fault reappeared on six sites
at once. The rule is now general:

> **A site is measured against every road EXCEPT the ones that cross it.** A site is entitled
> to have its own access road inside it; what it may not do is sit on somebody else's
> carriageway.

`world_belt2`, `world_beltverify` and both drawings now take their roads from **one** list,
`world_net.all_roads()`. Two lists would drift, and then "this site has access" is an opinion.

### 19.5 Where it leaves the belt

| class | m² | of belt |
|---|---|---|
| worked land | 676,384 | 34.4 % |
| settled | 115,744 | 5.9 % |
| **road** | **138,640** | **7.1 %** |
| woodland | 1,034,496 | 52.6 % |
| built footprint | 47,489 | 2.42 % |

**20 of 20 belt checks pass**, including the two new ones: V11 every site has a road running
through it, V20 no road ends anywhere but a boundary, a mouth or a junction. V12 was replaced —
it asked whether a corridor had a *destination*, which was the right question before this rule
and is superseded by it; it now asks whether every corridor measured at a plate edge is
actually carried by the network. All 14 are.


---

## 20. Rev E — the visual plan finished, and the world re-audited from the start

Oran, 2026-08-29: finish the visual plan in full, take every decision yourself and report them;
then take every message from the beginning of the whole-map build, analyse all of it, and go
over everything again. Then zoom out and look for what was missed, then zoom in, then look at
it again from the reader's point of view. State your confidence at the end.

### 20.1 The register

`world_register.py` lists **66 requirements**, in the order Oran gave them, each traced to
where it is met and how it is verified. **48 are met on a measurement, 15 in this session,
3 on an attestation, 0 partial, 0 open.**

The three attestations are the weakest links and all three are design judgements Oran signed
off himself: R02 the buildings' finishes, R03 futuristic rather than literal, R10 improve the
buildings significantly. Nothing measures "glossy".

Writing the register surfaced the gap that produced sheets 9, 10 and 11: **R14 and R15 —
"which user sees it, and how the user scans the world and digs into it" — were asked in the
very first message about the master plan and had never been answered.** Ten sheets described
the world and none of them described its reader.

### 20.2 Sheets 9, 10 and 11

| sheet | what it settles |
|---|---|
| **9  THE SITE LAYOUTS** | every one of 157 structures placed in the frame of the road that serves it, and checked |
| **10  THE PALETTE AND THE LIGHT** | every surface colour read out of the four `.blend` files by area; the sun; the shadow |
| **11  THE READING** | who looks, what they get in 3 seconds, what rewards 3 minutes, and what may still change |

**Sheet 9 found that the farm buildings were doll's-house sized.** `Detailed_Farm_Scene` is a
20.6 × 20.4 m diorama: its machinery is at true size — `Tractor01` is 3.49 m, a real compact
tractor — but `House01` measures 3.29 × 4.63 m, which is a garden shed. The first layout gave
four farms **85 m² of roof between them**. The buildings are now scaled to real sizes, the
props are left alone, and every factor is written down rather than applied silently on import.

**Sheet 10 found a second world-level colour fault.** OASIS's plate grass was
(0.2462, 0.3516, 0.0723), luminance 0.309 against 0.456 for the other three, under the **same
material name** `MAT_country_grass` that MEDCOIN carries at the world value — 32 % darker over
455,102 m², which is most of a plate. Levelled, one material, one object, re-measured from the
saved file.

It also cleared a false alarm: 404 MEDCOIN materials sit at Blender's default 0.8 grey and the
first check called them untextured. It was walking one branch of the node tree. Walking every
branch finds **all 404 correctly textured and 0 m² of bare grey.**

### 20.3 The three passes

`world_reader.py` runs them as checks, not as prose, because a pass written as prose finds
whatever the writer already believed. **17 checks, 13 pass, 4 gaps.**

**ZOOM OUT**

- **Z1 the career order is the left-to-right order on screen.** Screen centres 654, 1291,
  1600, 2276 — strictly increasing. The reader meets the four employers in the order they
  happened without being told to.
- **Z2 no city hides another.** Tested as projected silhouettes by separating axis. The first
  version used axis-aligned boxes and reported three false positives — a box round a projected
  diamond overlaps its neighbour's by construction.
- **Z3 the world has no water.** None: no river, no pond, no lake, in 4.08 M m². The largest
  single thing the world does not have. **Not added in rev E**, because a river crossing the
  belt re-opens the road audit — every road it meets needs a bridge and the no-dead-end rule
  must be re-proved against a barrier. First candidate for rev F, with its cost stated now
  rather than discovered later.
- **Z4 the plates disagree about thickness.** Three cities sit on a 7 m plate with a brown
  skirt; XTIX sits on a 0.25 m sheet. Merge contract M1.
- **Z5 the ambient disagrees 3.1×.** Merge contract M2. The **sun agrees exactly** in all
  four: energy 0.88, angular size 3.40°, altitude 75.0°, Z-rotation 135°, CYCLES / Standard /
  look None / exposure 0.

**ZOOM IN**

- **I2 every field structure is within reach of a road.** Found one at 208 m, then one at
  171 m. Both were metric mismatches between the placer and the checker — edge against
  centreline, then centre against corner. One metric now: centreline, from the structure's
  centre, 160 m.
- **I3 the gateway junction fits**: a 60 m roundabout at (689, 1063), nearest plate edge
  140 m.
- **I4 every structure is square to its road** — 75 roofed structures on three bearings.
- **I5 and I6** record two things no geometric check can see: which way a building **faces**,
  and that the 11,965 belt trees are generated by the grove algorithm against the canopy field
  rather than listed. Listing 11,965 coordinates in a plan would be false precision.

**THE READER**

- **U1 the eye lands on the current employer first.** XTIX is 261.9 m against 72.2 m — 3.6× —
  and also the leftmost city and 33 % built. Three separate signals, one place.
- **U2 the countryside never competes**: 2.71 % built against the least-built city's 6 %;
  tallest belt thing 15.4 m against the lowest city's 23.7 m.
- **U5 the reader is not told what they are looking at.** The world carries no label. A hiring
  manager cannot know the blue towers are XTIX, or that the order is chronological, unless the
  **page** says so. That is a page-design requirement, not a world-geometry one, and it is the
  one thing on that sheet the model cannot supply.

### 20.4 What changed in the plan as a result

| | change |
|---|---|
| roads | a **north frontage road**, boundary to boundary at y = 1990, so North Eventer farm fronts a lane and not the 88 m EVE-N motorway, and EVE-N meets something before the edge. 19 roads, 8.31 km, **38 ends, 0 dead ends** |
| sites | four moved or re-shaped: North Eventer farm to a **steading** with no dwelling; South crossing turned 90 × 190 so its long axis is along its road; Corridor services moved off the crossroads into a quadrant; Mid Field farm 4 m |
| structures | **157**, up from 138, after the works went from 8 warehouse units to 20 — 8.9 % roof on a 37,380 m² site is not an industrial estate |
| colour | OASIS's plate grass levelled; `GROUND_RGB`, `PLATE_SIDE_RGB` and `MERGE_CONTRACT` recorded in `world_plan` |
| checks | `world_verify` **25 of 25** (A1, A2 and C3 rewritten to test the requirement as it now stands); `world_beltverify` **20 of 20**; `world_net` **0 dead ends**; `world_layout9` **0 faults** |

**The system is a fixed point.** Running the whole chain and feeding the measured roof areas
back into the programme changes **0 of 10** built fractions. Sheet 7 and sheet 9 agree to
**1.000×**.


---

## 21. The decisions taken without asking

Oran gave standing authority for this session and asked for the decisions to be reported. There
are twenty-three. Each is stated with why, so any of them can be reversed on its own.

### 21.1 About the reader — the ones that shaped everything else

| # | decision | why |
|---|---|---|
| 1 | **The audience is a hiring manager or recruiter at a games or technology company: 30–90 seconds, on a laptop, looking for whether this person can run commercial growth.** | It was never written down, and every judgement about "how much detail" was being made without it. It is the operative fact, not a guess about taste. |
| 2 | **A static isometric image. The page scrolls along the PATH, four sections in career order. One optional city zoom at 0.56 m/px. No free camera, no street level.** | A hiring manager with sixty seconds will not learn a camera. At 0.125 m/px the low-poly geometry stops being a style and starts being a limitation. |
| 3 | **Detail must reward a second look and never be required for the first.** | The test the countryside has to pass. At world zoom a farm barn is 5 px and a person 1.5 px: the belt is texture at the distance the page is read from. |

### 21.2 About the assets

| # | decision | why |
|---|---|---|
| 4 | **Scale `Detailed_Farm_Scene`'s buildings, leave its props alone.** House01 ×2, Barn01 ×2, Greenhouse ×2, Wind_Mill ×2.5, Reservoir ×2.5. | It is a 20 m diorama with true-size machinery and doll's-house buildings. Four farms had 85 m² of roof between them. |
| 5 | **`American_House_00` is the farmhouse as well as the hamlet's front row.** | Nothing in the folder is a farmhouse, and it is an American farmhouse. Decimate to ~6,000 faces: 39,283 on a 14 px house is 2,900 per pixel. |
| 6 | **`4002336.FBX` replaces `gasstation.FBX`, and is placed as PARTS.** Canopy 42.1 × 17.4 m on the forecourt, shop behind it. | The whole 54.8 × 57.9 m block fits none of the service sites. A layout places parts, not files. Its 91 m apron and its 104 m photographic sky cylinder are dropped on import. |
| 7 | **`plant.blend`'s fan palm and `LOW_POLY_set`'s eight palms and three bananas are not used.** | Tropical. This is a temperate American countryside and there is no warm-climate district. |
| 8 | **Face budget: 40 faces per pixel of apparent height.** | The orchard tree went from 4,370 faces to 191 and the belt from 36.0 M faces to 4.27 M. At 6 px nobody can tell. |

### 21.3 About the roads and the sites

| # | decision | why |
|---|---|---|
| 9 | **A lane runs THROUGH the site it serves and carries on.** | Answers Oran's two notes — access, and no road ending mid-map — with one piece of geometry instead of two. |
| 10 | **A site fronts the NARROWEST road that crosses it.** | You front a service road, not a four-carriageway motorway. |
| 11 | **A site is measured against every road EXCEPT the ones crossing it.** | A site is entitled to its own access inside it; what it may not do is sit on somebody else's carriageway. |
| 12 | **Setback by kind: roof and tall 12 m, forecourt 5 m, yard prop none.** | A farmyard IS the verge. A filling station's canopy fronting the road is its whole purpose. |
| 13 | **A north frontage road, boundary to boundary at y = 1990.** | A farm cannot front an 88 m motorway, and EVE-N 404 had nothing to meet before the edge. |
| 14 | **North Eventer farm becomes a STEADING — farm buildings, no dwelling.** | 44 m of strip between EVENTER's 30 m clearance and the plate rim leaves 10 m of buildable depth. A 20 m farmhouse does not fit in that, and pretending otherwise is how a plan acquires a lie. |
| 15 | **South crossing turned from 210 × 62 to 90 × 190.** | A ribbon settlement wants its length along its road. |
| 16 | **Corridor services moved one field south of the crossroads.** | A service area occupies a quadrant of a junction, never the crossing itself. |
| 17 | **The gateway is a 60 m roundabout.** | It is where 80 m becomes 20 m, and that transition has to be a junction. It fits: nearest plate edge 140 m. |
| 18 | **The works go from 8 warehouse units to 20.** | 8.9 % roof on 37,380 m² is not an industrial estate; a real one runs 25–40 %. It also brings the belt's built footprint onto Oran's 3 % dial. |
| 19 | **Field structures within 160 m of a road, and no track of their own.** | A field barn is reached across its own field. 208 m across a field is not a barn anybody uses. |

### 21.4 About colour, light and the merge

| # | decision | why |
|---|---|---|
| 20 | **OASIS's plate grass levelled to the world value.** | Same material name as MEDCOIN's, 32 % darker, 455,102 m². The same argument as the carriageway in rev C. |
| 21 | **Level the CONTINUOUS surfaces, report the LOCAL ones.** Plate grass, carriageway and plate side run from plate to plate and a seam can show; a yard in XTIX is 150 m of countryside from a yard in MEDCOIN and they never meet. | Otherwise the world gets levelled into sameness for no gain. |
| 22 | **A belt surface may only take a colour that already exists in a city, or one interpolated between two that do.** | It is what stops the belt becoming a fifth palette sitting between four that agree. The canopy field does this for planting; this does it for the ground. |
| 23 | **No water in rev E; the ambient and the plate thickness recorded as merge contract, not levelled now.** | A river re-opens the road audit. Levelling four files for a value the merge overwrites is work that would be thrown away. |


---

## 22. Confidence

Oran asked for a confidence figure. A single number would hide where the risk actually sits, so
here it is by area, with what would move each one.

| area | confidence | what it rests on | what would move it |
|---|---|---|---|
| **geometry and measurement** | **very high** | every figure derives from a measurement or from `world_plan`; no number is typed twice. Four harnesses, 25 + 20 + 17 + 66 checks, each with a proof it can fail. The chain is a fixed point: re-running it changes 0 of 10 built fractions | nothing. This is as verified as a plan can be without being built |
| **the road network** | **very high** | 38 ends across 19 roads: 9 on the boundary, 19 at a city mouth, 8 at a junction, 0 in a field. A probe lane stopping 255 m short is graded DEAD END, so the test is a search and not an assertion | nothing |
| **areas and programme** | **very high** | rasterised at 4 m, every cell classified exactly once. Sheet 7 and sheet 9 agree to 1.000× because the built fraction is back-computed from the roof actually placed | nothing |
| **colour and light** | **high** | read out of the four `.blend` files by area, not chosen. Two faults found and levelled; the sun verified identical in all four | it is measured on BASE COLOUR. A textured surface can read differently from its base colour under light, and that is not checked |
| **the assets** | **medium-high** | 20 of 21 files open and are measured. Every size on sheet 9 comes from the model, not from a catalogue | seven files ship without textures; several need decimating and re-scaling. All are listed, none is done |
| **how it will LOOK** | **medium** | the plan says a farm barn is 5 px and a hamlet 215 px. That is arithmetic, not a picture | **this is the real risk.** Nothing has been rendered. The belt could read sparse, or busy, in a way no number here predicts |
| **the merge** | **medium** | M1–M4 specify what the four files must be made to agree about | none of it has been executed. Merging four files of 47,987 objects is the step most likely to surprise |

### 22.1 The honest summary

**The plan is right to the limit of what measurement can establish, and that limit is real.**
Everything about position, area, access, scale, colour value, shadow length and payload is
verified and reproducible. Nothing about how it will *look* is, because it has not been built.

The single most useful next action is not more checking. It is to **build one district** —
the XTIX–EVENTER gap: the belt collector, the three lanes, two farms, the works, and the
planting between them — and render it at world zoom and at city zoom. That is roughly 4 % of
the belt and it converts every arithmetic claim on sheets 8, 9 and 10 into evidence. If the
belt reads correctly there, it reads everywhere, because the same field and the same rules
generate the rest.

### 22.2 What is still open, and it is deliberate

| | |
|---|---|
| **water** | none in 4.08 M m². Costed, not cheap: every road it crosses needs a bridge and the no-dead-end rule must be re-proved. Rev F |
| **the merge** | M1 one plate, M2 one ambient, M4 one terrain resolution. Specified, not executed |
| **labels** | the world carries none. Four names and a date range per city belong in the PAGE, not the render |
| **three attestations** | R02, R03, R10 — the buildings' finishes. Judgements, signed off, and nothing measures "glossy" |

---

## 23. THE FIRST DISTRICT, BUILT

Section 22 closed the plan. This section is the first part of the belt that exists as
geometry rather than as arithmetic: **x 0–980, y 800–1215 — the XTIX–EVENTER gap.** 406,700 m²,
about 4 % of the belt. It holds the belt collector, all three EVENTER south lanes, the LINK
trunk and its gateway, North Field farm, Mid Field farm, Crossroads services, nine blocks of
worked land and the wood between them, and 20 m of XTIX's own plate so the seam is in frame.

Built by `world-build/tools/belt_build.py` in four stages, each rendered and looked at before
the next was written: **ground → roads → structures → planting**, then a fifth stage,
`verify`, that opens the finished file and measures it.

### 23.1 What it contains

| | |
|---|---|
| ground | 980 × 415 m plate, 7 m skirt, 9 worked blocks, 3 site yards |
| roads | 7 carriageway sections, every one from `world_net.all_roads()` |
| structures | 44, from 20 assets, placed by `world_layout9.json` |
| planting | 2,648 plants, 24 unique meshes |
| geometry | 822,850 faces drawn from 94,376 stored — 8.7× |

The district by ground, from `world_cells.classify`: woodland 34.1 %, crop 19.4 %, pasture
14.4 %, farm 13.1 %, road 10.1 %, XTIX's plate 6.0 %, services 2.9 %.

### 23.2 The build's own harness — `belt_build.py --stage verify`

Seven checks, measured **through the depsgraph**, so what they read is what the camera sees.
None of them reads a variable the builder set.

| | | |
|---|---|---|
| B1 | every structure stands at the height the layout gives it | worst 0.0 % over 25 |
| B2 | every structure sits on the ground | 44, all based at 0.070 m |
| B3 | no plant stands on a carriageway or a city plate | 2,648 placed, 0 |
| B4 | every plant is rooted inside the district | 0 outside |
| B5 | woodland is planted at the sheet's own rate | 97/ha against 160/ha of *closed* wood |
| B6 | nothing exceeds the shadow ceiling | 12.4 m against 385.3 m |
| B7 | one copy of each asset, not one per placement | 8.7× |

**7 of 7.**

### 23.3 What the build found that the plan had wrong

Building is a test the drawings could not run. Nine things came back:

1. **`4002336` is a filling station, not two rectangles.** Dropping its 104 m sky cylinder,
   its 91 × 82 m apron and everything whose top is below 0.5 m leaves **54.84 × 25.67 ×
   7.23 m and 10,068 faces** — a canopy at 42.08 × 17.38, a shop behind it at **24.0 × 8.9**,
   a price pylon and three light masts. The layout had been placing a 42 × 17 canopy and an
   invented **18 × 12** shop 3 m apart; the real shop is a different shape and stands 12.3 m
   away. It is now placed whole, and it states its own roofed area (945 m²) because a
   canopy's bounding box is not roof.
2. **The peterbilt is a tractor unit, not a 20 m rig.** 8.21 × 23.18 × 11.22 m over 7,453
   vertices with no stray geometry — the model is simply built at **2.73× life size**. Scaled
   uniformly to a real 4.1 m cab it is 3.0 m wide and 8.5 m long. The old figure would have
   stretched the mesh 2.7× along and squeezed it to 2.6 m across.
3. **A size tuple is in the source's axis order.** Writing the truck's length first — which
   reads more naturally — asked the placer to scale it 1.03 / 0.13 / 0.37.
4. **Containment was tested against a bounding box, not the site.** `frame_extent` is the
   AABB of the site's corners *projected into the road frame*, and the AABB of a rectangle
   crossed diagonally is bigger than the rectangle. Four structures on the two diagonal sites
   sat up to 2.1 m outside their own land and the check said nothing. Containment is now the
   item's four world corners against the site, which reduces exactly to a clamp: a box of
   half-extents *a*, *c* on frame axes reaches `a·|d.x| + c·|p.x|` in world x, so all four
   corners are inside an axis-aligned site **iff** its world AABB is.
5. **A clamp is a repair, not a solution.** Three lorries at Oasis road stop needed dragging
   9, 13 and 17 m and arrived as a diagonal staircase. Past **3 m** a site now loses the
   structure and says so.
6. **`Farm_Plow02` is not `Farm_Plow01`** — 2.86 × 1.61 against 3.05 × 1.27. Both were placed
   with the first one's dimensions.
7. **Deleting a parent empty does not bake its transform.** Removing the FBX's transform
   empties made a 54.84 × 25.67 m station **20,009 × 42,078 m**: measured before the delete,
   wrong after it. Empties are kept; only roots are moved.
8. **Three assets ship without their textures** — `American_House_00` (6 of 14 materials),
   `Shed` (1 of 1), `4002336` (8 of 18) — and Blender renders a missing image magenta. Most
   of them carry the modeller's own diffuse colour underneath, so cutting the dead link
   restores the asset's real palette; only the handful left on the importer's grey are given
   a colour, from the material's own name.
9. **`city_at` was on inclusive bounds while `in_rect` was half-open.** A city plate claimed
   one cell past its own edge on two sides: **2,960 m² of woodland was booked as city.** The
   classifier now lives once, in `world_cells.py`, and both `world_beltverify` and
   `belt_build` import it — so "this is woodland" means one thing in both.

### 23.4 Three things the build's own tests caught in themselves

- **A test that proves the code ran is not a test.** The conifer repair looked for "a material
  whose green channel is above 0.15" — which `(0.8, 0.8, 0.8)` satisfies — so it picked the
  white material and painted white over white, then reported one material fixed. The render
  still had white trees. It now requires green to *be* green (`g > 2·max(r, b)`) and measures
  the result afterwards.
- **Measure where the thing lands, not where you aimed.** Trees were tested at the cell centre
  and then scattered up to 4 m, so conifers stood in the middle of the belt collector.
- **A threshold you chose is not a property of the file.** B7 asserted "fewer than 300 mesh
  datablocks". It now measures that drawn geometry exceeds stored geometry, which is what
  instancing actually means.

### 23.5 Two visual decisions, made in the build

- **The yard is the built part, not the holding.** Farmyard tan over the whole 180 × 196 m
  site made each farm read as an enormous beige rectangle with a thin line of sheds in it. The
  yard is now cut from the structures with a working margin — 45 %, 82 % and 60 % of the three
  holdings in this district — and the rest of a farm is pasture.
- **Two farms 150 m apart may not be the same farm drawn twice.** The layout is unchanged; the
  *frame* varies. A site may be laid out mirrored along its lane and may take the near side of
  the lane instead of the roomier one — four arrangements from one plan, assigned round-robin
  in site order, because a hash of the name gave North Field and Mid Field the same two bits.
- **Every road in the world is the same asphalt.** Width alone distinguishes a motorway from a
  farm lane. The unsealed-track colour vanished against the crop; a 12 m road that cannot be
  seen is not a road.

### 23.6 Where this leaves the belt

The district is evidence for the rest by construction: the same `world_net` roads, the same
`world_layout9` placements, the same `world_cells` ground and the same canopy field generate
every other district. What has been shown is that they generate something that reads.

**Renders:** `renders/BD_final_world.png` (1,180 m across the frame — the world zoom) and
`renders/BD_final_city.png` (420 m — the city zoom). **File:** `belt_district.blend`.

---

## 24. THE ROADS AND THE FIELDS, REBUILT

Oran, on the first district's render — three notes and one worry:

> *"The roads look terrible ... no markings ... it is just surfaces in the colour of a road ...
> there are no proper connections between roads, it is all cuts at right angles like unrelated
> lines ... in short these are not roads."*
>
> *"There are areas on the map that are simply rectangles in a colour with no relevance
> whatsoever ... after all the hard work we did, to just throw rectangles that are supposed to
> represent a crop — that is not understandable and it is not the right way to do it."*
>
> *"How, after everything we did and all the knowledge we built here, do we arrive at a map
> built in such a broken way?"*

He was right on all three. This section is the answer to the fourth.

### 24.1 Why fifty-two green checks did not catch it

`world_verify` 25, `world_beltverify` 20, `belt_build --stage verify` 7. **Every one of them
counts a QUANTITY** — is it 12 m wide, does it go somewhere, is it the right colour, is the
area balanced, is the setback met. A road that is a black rectangle answers *yes* to all of
them. Nothing asked whether the thing looks like what it claims to be.

And the belt had no asset pack. The cities got their road craft free: `XTIX_final_street.png`
shows lane markings, kerbs, crossings and traffic because the pack shipped them. The belt's
roads were generated here, as `band()` quads, and craft that is not specified is not built.

### 24.2 What the cities actually contain, measured

Before designing anything, `road_measure.py` / `_3` / `_4` opened the three city files and
measured what a road in this world is made of.

| | XTIX | MEDCOIN | EVENTER |
|---|---|---|---|
| how it is built | **one mesh, 1,179 faces, 11 flat-colour slots, no UVs, no textures** | 17,126 faces | 26,709 faces |
| carriageway | 7.00 m and 14.00 m at z **0.050** | z **0.140** | z **0.140** |
| marking | 0.26 × 2.60 m every 6.50 m, z 0.063 | 0.36 × 2.00 m every 5.00 m, z 0.152 | 0.45 m wide |
| duty cycle | **40 %** | **40 %** | ~33 % |
| paint above road | **+0.011** | **+0.012** | — |
| kerb / pavement | 2.0 and 3.0 m, top z 0.210 — a 0.16 m kerb | kerb 0.170–0.200, pavement 0.190 | barriers, soffits, concrete, yellow |

The three cities **agree** that a marking is a 40 % duty cycle sitting about 12 mm above the
tarmac. They **disagree** about the carriageway's height — XTIX 0.050, the other two 0.140 —
and that disagreement is logged as a merge-contract item, not averaged away.

### 24.3 The road standard — `world_road.py`

Nothing in it is a taste; every number came out of the measurement above.

**The reserve includes its verges.** That one rule makes every width the plan already declares
come out as a real road, and two of the widths XTIX itself uses fall out unasked:

| reserve | class | carriageway | central | verge | paved |
|---|---|---|---|---|---|
| 8 m | LANE | 1 × 4.0 m | — | 2.0 m | 50 % |
| 12 m | ROAD | 1 × **7.0 m** ← XTIX's street | — | 2.5 m | 58 % |
| 16 m | ROAD | 1 × 11.0 m | — | 2.5 m | 69 % |
| 20 m | MAIN | 1 × **14.0 m** ← XTIX's avenue | — | 3.0 m | 70 % |
| 32 m | DUAL | 2 × 9.0 m | 6.0 m | 4.0 m | 56 % |
| 80 m | TRUNK | 2 × 14.0 m | 12.0 m | 20.0 m | **35 %** |

That last line is the black trapezoid, answered: **80 m is a motorway's reserve, not its
tarmac.** 28 m of carriageway, a 12 m green median and 20 m green verges reads as a motorway
from above; 80 m of unbroken black does not.

Built per road: a **verge** ribbon over the whole reserve in XTIX's own darker green
(0.2831, 0.4287, 0.0844) at z 0.100 · **carriageways** at z 0.140 · **centre dashes**
0.36 × 2.60 m every 6.50 m and **solid edge lines** 0.32 m wide, both at z 0.152 · **junction
fillets** at z 0.140 · a **taper** where a wide road becomes a narrow one.

Three departures from the cities, each stated rather than hidden:

1. **Junction corners are filleted.** XTIX's 16 carriageway faces simply overlap where they
   meet — invisible at 7 m wide between towers, glaring at 8 to 80 m in open country.
2. **Markings stop short of a junction.** The cities run theirs straight through.
3. **The fillet is built on the CARRIAGEWAY, not the reserve**, and the acute quadrant of a
   skew crossing gets no fillet at all — past twice the right-angle corner distance the
   construction runs away into a long spike, and real practice puts a nose island there.

### 24.4 The field standard — `world_field.py`

The plan gave a crop field 6,376 m of headland planting and a pasture 4,520 m of hedgerow —
**both of them edge treatments** — and said nothing about the inside of a field. The build laid
the edges correctly and left 250,000 m² of flat colour between them.

A field, from 400 m up: **drill rows** at the 6 m working width, light and dark · **tramlines**,
the sprayer's wheelings, a bare pair every boom width and the most recognisable mark on arable
land · a **headland** round the inside where the tractor turns · its **own direction**, along
its own longest axis, with one field in four worked across it and one in eight on the diagonal ·
and **a crop**: wheat, barley, stubble, ploughed, young cereal or rape, not one "crop yellow".

Grass is not flat either: mower stripes at a 20 m pitch and rough patches where nothing was cut.

All of it flat-coloured geometry, because that is how the cities are built. **381 faces of field
texture for the entire belt.**

**And the colour was measured against the plate.** The world's ground is (0.3630, 0.5184,
0.1065), luminance 0.456, in all four cities. The first pasture colours came out at luminance
0.67 to 0.73 — **forty-seven per cent lighter than the grass they sat on** — which is why every
pasture read as a pale rectangle with a hard edge. They are now +8 %, +15 % and +29 %. Ripe
cereal stays at +51 % to +69 %, because ripe cereal really is that much brighter than grass.

### 24.5 The road Oran drew

> *"There is no shape to a road that ends ... add one road as marked and it will go to the
> boundary of the whole map on the western side."*

**EVENTER south frontage**, y = 1185, boundary to boundary. It clears EVENTER's plate at 1203
by 12 m, crosses no site anywhere along its 2,020 m, and creates six new junctions — the three
south lanes, the interchange throat, the PATH and the corridor. It is also right on its own
terms: EVENTER's southern edge is 801 m long and carries three lane mouths and a motorway, and
nothing collected them; the three lanes ran 358 m south to the collector as a comb with no
spine. The network is now **20 roads, 10.33 km, 40 ends, 0 dead ends, 13 junctions and 1 bend.**

*Known simplification, stated:* at x = 689 it crosses the interchange throat **at grade**. Real
practice puts the local road over or under and connects them with slip roads in each quadrant.
This world builds no bridges yet — the same missing machinery as the water item in §22.2.

**And a road that leaves the frame is now seen to leave it.** Every end the network grades
BOUNDARY or MOUTH is carried 40 m further along its own direction before anything is drawn,
then clipped to the district like everything else. The three lanes ended at y = 1203 — EVENTER's
plate edge, a legal mouth — and in a district render, where EVENTER is out of frame, they
stopped in open grass with a rounded end. That is the cut Oran drew a line through.

### 24.6 The checks that count craft, not quantity — `--stage verify`, C1 to C8

| | | measured |
|---|---|---|
| C1 | every carriageway has a made-up verge either side | 9 carriageways, 0 without |
| C2 | every road that should be marked is marked, at the cities' 40 % duty | 6 of 6; duty 39–45 % |
| C3 | paint stops short of every junction | 10 junctions, 0 intrusions |
| C4 | every junction is built as a junction, with corner fillets | 9 junctions, 40 pads, 0 without |
| C5 | no worked field is a flat rectangle of colour | 8 blocks, 0 bare |
| C6 | no grassland is a pale rectangle dropped on the plate | 21 materials against luminance 0.456 |
| C7 | every layer sits at the height measured out of the cities | 0.140 / 0.152 / 0.100 |
| C8 | no road stops in open ground inside the frame | 16 drawn ends |

**15 of 15**, with B1–B7. And each is shown to be able to fail: C6's proof measures **the colour
this build started with** and reports +47 %, past its own 40 % limit.

### 24.7 Three faults the checks found in themselves

Written down because each is the same mistake in a different coat — measuring the wrong thing
and believing the answer:

- **C2 divided by the whole road's length** when only part of it is in the picture, and
  reported 2 % and 18 % duty on two roads that are painted correctly. It now walks the
  centreline a metre at a time and counts only the metres that are both inside the district and
  outside a junction's gap. It had also counted a dual carriageway's two lines against one
  length, and reported 178 % duty on the motorway.
- **C4 demanded fillets for a junction 13 m outside the district**, whose pads clip to nothing.
- **C8 tested the plan's endpoint instead of the drawn one**, and flagged the three lanes that
  are drawn running off the cut — the exact opposite of the fault it exists to find.

### 24.8 Where it stands

`world_verify` 25/25 · `world_beltverify` 20/20 · `world_net` 40 ends, 0 dead ends ·
`world_layout9` 154 structures, 0 faults · `world_register` 66 requirements, 0 open ·
`belt_build --stage verify` **15 of 15**.

**Renders:** `renders/BD_page.png` at 0.908 m/px — the scale page 1 will actually use — and
`renders/BD_detail.png` at 0.368 m/px, the scale XTIX was shot at, so craft can be compared
against craft rather than across three different scales. **Drawings:**
`WORLD_MASTER_DRAWINGS_revG.pdf`.

---

## 25. THE WORLD, BUILT

Oran: *"go for it / but again — work slowly and apply everything, everything we have talked
about the whole time."*

Everything means the belt across the whole plate **and** the four cities merged into it, built
by the code the sample board proved, with the plan audited before a single face was drawn.

### 25.1 One builder, not a copy of one

The sample board and the world are now built by **`world_make.py`**. It was extracted out of
`sample_build.py` and then out of its own `build_board()`, which had grown into a 210-line
monolith holding rules the world needed:

| function | what it owns |
|---|---|
| `build_ground` / `build_field` / `build_roads` / `build_water` | the plate, the crops, the carriageways and markings, the channel and its bridges |
| `build_hedges` | a field boundary, CUT at every road and at the water |
| `build_gate` / `gate_at` | where a field's boundary comes closest to the road that serves it |
| `build_banks` | reeds on both banks, willows along the water |
| `build_woods` / `build_margins` | copses, and the scrub that ends them |
| `build_power` | poles at a pitch, joined at junctions, with cable between them |
| `build_livestock` / `build_traffic` / `build_signs` | herds, tractors, vehicles in lane, warning signs on approach |
| `build_furniture` | passing places, fences on the field side only, marker posts, boulders, verge flowers |
| `kit` / `place` / `place_xyz` / `fit_xyz` | the kit loader and the three ways to size a thing |
| `verify` / `shoot` / `report` | measured where things actually are; one camera; one report |

The extraction was **proved, not assumed**: the sample rebuilt to 4,858 placed objects, 5,634
objects and 346,490 faces — identical to before. The first attempt came out one object short,
because the extracted `build_livestock` put the tractors after all three herds instead of after
the first. `rnd()` is one stream: change the order of the draws and everything downstream moves.
The function was rewritten to the original sequence and the count came back exactly.

### 25.2 The plan, audited before anything was built

`world_audit2.py` puts the real plan — `world_net`'s 20 roads, `world_belt_prog`'s 10 sites and
22 worked blocks, `world_water`'s stream — through the eight layout rules the sample earned,
plus three of its own. **11 of 11, 0 failures.**

W2 and W4 test the **fields**, not the blocks. A block is a budget; a field is what is left of
it once the roads, the water and the yards are taken out. `world_field.subdivide()` rasterises
each block, marks the clean cells, and extracts the largest clean rectangles: **22 blocks into 41
fields, 529,076 of 629,849 m2 (84 %)**, and the one block that yields nothing (*Xtix north
pasture*) is named rather than hidden.

### 25.3 Stages, and why a stage owns what it builds

    ground -> roads -> water -> structures -> planting -> furniture -> life -> merge -> verify -> render

Running a stage twice must not build it twice. The first time `--stage structures` ran again it
stacked a second set of 418 objects on the first, because the stages **share collections** — the
gate writes tarmac into `ROADS`, the furniture writes flowers into `PLANT` — so "empty the
collection" cannot say who owns what. Every object is now stamped with the stage that made it,
and a stage clears its own stamp before it starts. Proved: the second run cleared 418 and
rebuilt to exactly the same total.

### 25.4 What the belt contains

| | |
|---|---|
| plate | 2,020 x 2,020 m; four city plates held clear, 2,108,611 m2 |
| roads | **10.33 km** — 20 verges, 24 carriageways, 1,500 dashes, 38 edge lines, 44 fillets, 1 taper, 11 junctions |
| grade separations | 2 — *EVENTER south frontage* over *LINK 0* on a 94 m deck; *north frontage* over *EVE-N 404* on 102 m — each with two 90 m ramps and abutments |
| water | 1,907 m of channel 9 m wide with 4 m banks, 1 pond, **6 bridges**, each span measured ALONG its road |
| fields | 41 fields, 529,076 m2 — barley x4, grazed x3, hay x5, meadow x4, orchard x9, ploughed x2, rape x3, stubble x4, wheat x4, young cereal x3 |
| sites | 10 yards, 154 aprons — each yard cut to what stands on it |
| structures | 84 buildings, 3 filling stations, 24 machines, 27 props, 264 yard props |
| planting | 5,721 hedge units over 121 boundary runs; 816 reeds, 56 willows; **9,832 trees and 1,189 scrub** — 3,081 conifer, 2,837 oak, 2,159 light and 1,755 dark broadleaf |
| furniture | 4 passing places, 1,540 fence panels, 34 marker posts, 56 boulders, 234 verge flowers, 35 field gates, 33 junction signs |
| power | **141 poles on 19 roads, 131 spans of cable**, 9 of them joining two roads at a junction |
| life | 84 cattle in 12 pastures, 6 tractors at work, 45 vehicles in lane |
| **total** | **23,247 objects, 2,173,164 faces — CLEAN** |

### 25.5 The woodland is a field, not a scatter

Oran, on the first samples: *"vegetation and trees are thrown on the map."* Two things were
wrong and both are fixed.

**Where.** Each city's own countryside continues into the belt. Its planted fraction was
already measured at every plate edge — OASIS 97–100 %, XTIX 68–82 %, MEDCOIN 59–79 %, EVENTER
19–33 % — so `canopy(x, y)` is those sixteen figures weighted by distance. The belt is dense
wood in the OASIS quarter and open farmland in the EVENTER quarter, **graded between**.

**How.** Testing each cell against that fraction independently gives an even speckle of trees
over everything, which is the same fault in a new coat. Three octaves of value noise on a
lattice make the *same* fraction come out as **woods with glades between them**, and a cell
whose neighbours fall the other side of the threshold gets scrub instead of a trunk — so a wood
has a margin rather than a hard edge.

**How much.** The first build planted 11,021 things where the measured targets asked for about
8,550 — 29 % over — and the reason is worth writing down, because it is a mistake that hides
inside code that looks right. `noise()` is a weighted **sum** of three uniform fields, so its
own distribution is bell-shaped and piles up near the middle: `noise < 0.70` does not plant
70 % of the ground, it plants far more. It made every city plate read as a pale rectangle
against a belt darker than it should have been — and the first guess at the cause was a colour
mismatch, until measuring showed every city's grass is already the belt's exact green,
`(0.363, 0.518, 0.107)`. The threshold is now the field's **percentile**, sampled once, and the
achieved cover is measured per quarter against what that quarter's own city asked for:

| quarter | open cells | asked | planted |
|---|---|---|---|
| EVENTER | 3,376 | 41.4 % | **39.2 %** |
| XTIX | 2,672 | 70.9 % | **67.8 %** |
| MEDCOIN | 3,353 | 67.7 % | **73.2 %** |
| OASIS | 4,484 | 89.8 % | **94.2 %** |

8,172 trees and 1,646 scrub. The residual is under six points and it is **reported**, not
assumed — the check that used to say "planted at 156 stems/ha" counted the input.

### 25.6 Faults found by building, and what each cost

- **A dead texture renders magenta.** `retro-urban-kit` is the one kit of 46 whose texture
  files are all missing (3,445 references resolve everywhere else). `world_palette.apply()`
  skipped any material whose Base Color was linked — right for a loaded atlas, wrong for an
  empty texture node. It now cuts the dead link and recolours by name, and `dead_textures()`
  reports any that survive. The pallet was also moved to a kit whose textures load.
- **A fifty-metre white plane over a filling station.** The layout's 54.8 x 25.7 m is the
  **forecourt**, not the canopy. A canopy is 20 x 11 m on four columns over two pumps, and it
  now has a way in, painted bays, tankage and lorries. The first fix put the red fascia *over*
  the deck, which simply covered it — the fascia goes underneath.
- **Silos lying on their side.** Every round object in 46 kits is a navy factory hopper. A grain
  silo is a cream cylinder with a cone on top, so it is **built**, not borrowed.
- **Buildings placed across their plots.** The layout gives *along the road* and *across*;
  mapping those straight onto a model's own x and y builds a barn 19.5 m deep and 5.9 m wide
  whenever the model happens to be longer in y. `fit_xyz()` turns the model to suit the plot.
- **Twenty identical sheds.** The layout named them all the same because the pack it was
  written against had one model; the kit has twenty. Variants are chosen from **where a thing
  stands**, so the choice is stable across rebuilds — and the first hash, a linear combination
  of coordinates, gave two farms 160 m apart the same house, so the bits are properly mixed now.
- **A yard the size of its site** is a coloured rectangle with no relevance — Oran's words about
  the first district. A yard is now the **union of an apron round each thing on the site**, which
  comes out as an L or a T or a yard with a corner missing, and the rest stays grass.
- **The proportion check flagged the silos** as taller than they are wide. That is the check
  working: a silo is declared tall on purpose, alongside the columns, the chimneys and the poles.

### 25.7 The merge

Measured first, decided second:

| | meshes | faces (instanced) | extent | plate |
|---|---|---|---|---|
| XTIX | 21,315 | 6.50 M | −4.5…805.3 x −4.5…743.2 | 810 x 747 at (73, 73) |
| OASIS | 12,561 | 2.24 M | −10.1…700.0 x −4.9…650.0 | 700 x 650 at (1033, 118) |
| EVENTER | 9,621 | 5.54 M | −12.9…800.1 x −12.8…740.0 | 801 x 741 at (289, 1203) |
| MEDCOIN | 12,480 | 4.32 M | −48.7…700.0 x −20.7…650.0 | 700 x 650 at (1247, 1297) |

Every city is authored from its own (0, 0), so **the offset is the plate origin**.

Each city keeps its **own ground**. OASIS's terrain is 115,776 vertices and EVENTER's villa
ground stands 5 m proud; throwing those away to stand the cities on the belt's grass would lose
the thing each city was signed off on. They are lifted **30 mm** so their surface sits above the
world plate instead of fighting it, and their 7 m skirts hang underneath, hidden by the plate.

Dropped: each city's own **sun and cameras** — M2 says the world owns one of each — and the
**prototype collections**, hidden model sources that would otherwise arrive as a heap of
duplicates at the origin.

What actually landed:

| | collections | objects rooted | unique faces | suns/cameras dropped | prototypes skipped |
|---|---|---|---|---|---|
| MEDCOIN | 10 | 12,184 | 303,093 | 3 | 7 |
| EVENTER | 15 | 9,414 | 169,076 | 2 | 5 |
| OASIS | 7 | 11,494 | 390,383 | 3 | 2 |
| XTIX | 17 | 21,146 | 878,291 | 0 (its sun and camera live in the scene collection, so they never came) | 1 |

**78,547 objects.** The instanced face counts above are what the renderer draws; the unique
mesh data behind them is 1.74 M faces, because the cities are heavily instanced.

One thing was found by testing rather than by reading: the inherited merge set
`matrix_parent_inverse` from `root.matrix_world`, which is still identity because the depsgraph
has not run since `root.location` was set. It happened to give the right answer. A result that
depends on when Blender next evaluates is not a rule, so it is now written down as
`Matrix.Identity(4)`, with the reason.

### 25.8 Every road arrives at something

Oran, twice: *"a road cannot suddenly end, cut off in the middle of the map — every road has to
branch or carry on somewhere"*, and *"make sure the roads reach the edges of the boundaries."*

`world_net` reports 40 road ends and **0 dead ends**, and it is right about the plan. But the
plan says a road enters a city at a mouth; it does not say the *city* has a road behind that
mouth. With the cities physically in the world, `world_approach.py` asked the four city files
directly — finding carriageway by **material**, against each city's measured `ROAD_RGB`, because
four generators named their roads four different ways:

| | belt mouths | arrive within 14 m | need an approach |
|---|---|---|---|
| XTIX | 3 | 0 | 3 — 123, 130 and 140 m |
| OASIS | 3 | 2 | 1 — 147 m |
| EVENTER | 11 | 4 | 7 — 14 to 88 m |
| MEDCOIN | 2 | 2 | 0 |
| **all** | **19** | **8** | **11** |

XTIX's own carriageway stops **130 m short of its west edge** on every side: that band is
parkland, which a render of the seam confirms. So the approach is a road through a park to
reach the street grid — not a hole in the plan.

**The first measurement was wrong and had to be redone.** It walked the mouth's exact
centreline and asked for a road vertex within 9 m, which reported *222 m of missing road* into
OASIS where `world_mouthcheck` had already measured nought — OASIS's west road is at the edge,
but its centreline sits about 16 m off the declared mouth. Distance-to-a-line is a proxy; the
property wanted is **how far in the road starts**. Projecting the band onto the road's own
direction and taking the nearest depth gives that, and it agrees with the older harness on
every mouth the two share.

`--stage approach` then draws **11 links, 995 m of carriageway** — the only place the belt draws
inside a city plate, and it draws only what joins the two: the same carriageway, the same 40 %
markings, running straight in along the road's own direction until it overlaps the city's road
head. **441 city objects standing in the new carriageways were cleared** — every one of them a
bush or a small plant (`XL_plant_bushSmall` ×29, `XL_plant_bushLarge` ×24, …). Nothing wider
than 30 m and nothing named ground or terrain is ever removed by it, so no plate and no
building can be.

### 25.9 Where it stands

    ground -> roads -> water -> structures -> planting -> furniture -> life
          -> merge x4 -> approach -> verify -> render

| check | result |
|---|---|
| `world_audit2` — the plan, before building | **11 of 11**, 0 failures |
| `sample_build` — the shared builder, unchanged | 4,858 placed / 5,634 objects / 346,490 faces, identical |
| placed objects measured where they actually are | 20,449 — **0** on a carriageway, **0** in water, **0** off the board, **0** taller than wide |
| the four cities | **all four ON THEIR PLATES**, measured from their own bounding boxes |
| belt materials | 684, **0** in the cyan band, **0** driven by a dead texture |
| city materials | 2,110, of which 166 sit in that hue band **by their own design** — XTIX's towers are teal, and a check written for imported kit assets does not get to repaint a signed-off city |
| **the world** | **78,287 objects, 20,195,466 faces — CLEAN** |

**One thing deliberately not changed.** XTIX's carriageway is at z 0.050 and the other two
cities' at 0.140; the merge lifts each city 30 mm, so XTIX's roads sit at 0.080 against the
belt's 0.140. That is a 60 mm step at three seams, which is 0.07 of a pixel at page-1 scale.
It is logged, not averaged away — the same treatment §24.2 gave it when the disagreement was
first measured.

---

## 26. THE ROADS, REVIEWED AND REBUILT

Oran cut the whole plate into sixteen sheets, marked ten of them, and sent the notes back.
Every note was matched to a **named road** and checked against the network data before any
design was drawn — `world_roadmap.py` puts all twenty roads on the render with their name,
class and reserve, so a note and the code mean the same road.

Eight of the ten sheets carried a fault. **Four of them were the same fault**, and two more
came from one broken measurement, so the job was smaller than ten sheets of notes suggests —
provided it was done in the right order.

### 26.1 The cross-section a city hands over

> *"The interchange connects to 2 roads. What is this form of connection — completely broken
> … you can keep the 2-road configuration, but make it logical with the SAME roads, the same
> road elements, the same design, the same component."* — A4, B4, C4, B3
>
> *"The interchange coming from EVENTER has 2 main wide carriageways and 2 narrower ones at
> the sides. Those narrow ones are cut off in C4, as if they just disappeared."* — C4

He was right, and the reason is one line of thinking that was never questioned: **the belt
drew the cross-section its own class table says, and never looked at what the city brings to
the edge.**

`world_xsec.py` measures it. For every mouth it walks the city's carriageway geometry — found
by **material name**, sampled over the face — and reports, across the road, where there is
tarmac and where there is not:

| mouth | what the city hands over | what the belt used to draw |
|---|---|---|
| `EVE-W 372` | 6 m service · **36 m main** · 6 m service | 2 × 14 m with a 12 m median |
| `EVE-N 404` | **30 m main** · 6 m service | 2 × 14 m with a 12 m median |
| `LINK 0` | **30 m main** · 8 m service | 2 × 14 m with a 12 m median |
| `PATH 1` (OASIS) | **20 m** single | 1 × 14 m |
| `OAS-E 488` | **22 m** single | 1 × 11 m |
| `PATH 3` · `PATH 4` (MEDCOIN) | 10 m + 8 m — a dual with a 4 m median | 1 × 14 m |

Nothing lined up because nothing was ever meant to. `world_mouth.py` now continues the
measured cross-section instead:

- **A stub** — a road whose whole job is to carry one city's exit to the world boundary —
  wears that city's cross-section for its **whole length** and leaves the map with it.
- **A path** — a road between two cities that do not agree — wears each city's cross-section
  for 50 m, then the **service roads merge into the main carriageway over 90 m**, which is
  what a slip road does when it runs out of frontage to serve, and the main tapers to the
  road's own class over the 50 m after that.
- Both carry the markings, so the handed-over tarmac is a road and not a slab. Blocking the
  belt's own paint over the mouth had left 36 m of bare asphalt coming out of a fully-marked
  city — the same fault in a new place, caught in the render before it shipped.

**And a rule that stopped one of these being a lie.** `PATH 3`'s EVENTER end measures 36 m of
carriageway centred **30 m off** that mouth: what the probe found is EVENTER's frontage
running *along* its edge, not a road coming out to meet this one. Carrying it over drew a slab
30 m to one side swinging back over 100 m. A mouth is now only continued when the city's main
band is **within 12 m of the mouth's own centreline**; otherwise it has nothing aligned behind
it and goes to the terminus rules instead.

### 26.2 Two roads that were one road, and four corners with no radius

> *"Two roads that serve the ground-level buildings — merge them into one road with two lanes
> each direction."* — A4

`EVE-W 672` was classed **DUAL at a 32 m reserve**, which builds two separate 9 m carriageways
with a 6 m median. It read as two roads because it *was* two roads. At a 24 m reserve it is
one 18 m carriageway — four lanes, two each way — from the existing standard, not a special
case.

> *"These two sharp 90-degree turns — do them properly, so there is logic."* — C3, C4

Measured: **four corners in the whole network turn exactly 90° with no radius at all**, three
on `PATH 3` and one on `EVE-E 548`. Each is now a quadratic Bézier tangent to both legs, with
the tangent length clamped to 45 % of the shorter leg so a curve can never eat its own road —
`PATH 3`'s first leg is only 79 m. **No bend over 60° is left in the network.**

### 26.3 Roads that ended nowhere — and the measurement that put them there

> *"A road that just ends and is cut … it does not go to a field, it does not go anywhere.
> Either add a field and finish it with a gate, or finish it a little earlier at the road it
> touches."* — A3, B3

The network harness said 40 ends, **0 dead ends**, and it was right about the plan. The stubs
Oran could see were **my own approach links**, sized by a measurement that counted *any dark
surface* as road: XTIX has 363,808 vertices within 0.055 of its road colour and the two that
decided `PATH 0`'s length belonged to something else.

Searching by material name instead — and **sampling over the face, not at its corners**, because
XTIX's ground is one mesh whose 75,600 m² of tarmac has only 64 corners — gives an answer that
can be trusted. Of 16 mouths, **8 arrive within 14 m** and 8 do not:

| | |
|---|---|
| link built — the city's street is within 160 m, behind a green edge | `PATH 0` 144 m, `PATH 1` 158 m, `LINK 1` 130 m into XTIX's parkland; `PATH 2` 165 m into OASIS |
| terminus built — the city has nothing within 200 m | `EVE-W 80` (364 m), `EVE-W 672` (380 m), `EVE-E 548` (201 m), `PATH 2` into EVENTER (330 m) |

A terminus is a **turning head and a barrier**, not a cut: the carriageway widens so a lorry
can come back out, and the road is closed. Carving 380 m through a signed-off city to reach a
street is not a fix.

And on Oran's instruction, `EVE-S 488` and `EVE-S 76` now **end at their junction with the
EVENTER south frontage** rather than running past it into open ground. `EVE-S 212` is not in
his note but is the identical case; leaving it would have made three lanes inconsistent.

### 26.4 What the checks caught in my own work

Five faults, none of them spotted by eye:

| found | why it happened |
|---|---|
| 412 hedges standing **on** `PATH 3` | the corners were rounded, the road moved, and the planting was still on the old line |
| 62 median barriers **off the plate** | the check measured an object's *origin*; a mesh built from world coordinates has its origin at (0, 0). **The check was wrong, not the barriers** — it measures geometry now |
| lorries **in the stream** | they were on the bridge. The exempt list named three models and `build_fleet` uses eight |
| 2 lighting columns **in the water** | the pitch walked over the bridge without asking what was under it |
| a 9 m column **under a 5.4 m deck** | `blocks_for` stops the road that goes *over* a grade separation. Nothing stopped the road that goes *under* |

The last two are the same lesson: furniture ran along a road without asking what was there.
Both now stop at a junction, at a deck and at the water.

---

## 27. THE BELT, INHABITED

> *"Complete all the cars, the trees, the power poles, the means of transport, the farm
> vehicles, PEOPLE in the rural areas, and everything that is needed. Then make significant
> improvements after you finish the build and the checks. You have plenty of time. Take
> independent decisions and give me feedback at the end."*
> — Oran, 2026-08-31, before leaving the machine

The belt had 85 cattle, 7 tractors, 45 vehicles and **not one person in it**. A countryside
with nobody in it is a diagram of a countryside.

`world_life.py` is the answer, and it obeys the same rule as everything else in the belt:
**nothing is placed at a coordinate somebody typed.** Every figure, animal, implement and tuft
is offered to `world_place.Ground` — the one module that knows what may stand where — and goes
down only where the ground allows it. A farmhand on a carriageway is the same fault as a tree
on one.

### 27.1 What was asked for

| | before | now |
|---|---|---|
| people in the rural areas | **0** | **140** — in the yards where the work is, and walking the lanes |
| livestock | 85 cattle | **136** cattle, pigs and hogs, in herds rather than scatters |
| farm machinery | 7 tractors | **28** implements, bales and machines at the field headlands |
| vehicles, inter-city | 45 in the whole belt | **429 at 14.4 % lane occupancy** (15 % asked), from the cities' own fleet |
| vehicles, country roads | — | **91** tractors, pickups and work vehicles at 3.7 % |
| public transport | — | **12 bus stops**, each with people waiting, served by **4 buses** |
| lighting | none | **77 columns at 40 m** on all 13 inter-city roads; double-headed in the median of a dual |
| power | 134 poles | reaches **all four city plates at 0.0 m** — measured, not assumed |
| trees | 8,182 + scrub | unchanged; the canopy is already measured against each city's own edges |

### 27.2 What was added on judgement

Four things Oran did not ask for by name, each because the render showed the belt needed it:

- **Standing crop, 3,812 objects.** Not over the whole field — 529,000 m² at any useful
  density is tens of thousands of objects for something that reads as texture. A field shows
  its crop at its **edges**, which is where the eye goes, so that is where it is planted.
- **The wood floor, 1,635 stumps, logs, rocks and fungi.** A wood is not only its trunks.
- **Rough grazing, 1,183 tussocks and troughs in the pastures and 2,491 over the open grass.**
- **255 patches of mottled ground.** This one replaced an idea that did not work, and the
  correction is the interesting part — see below.

And nineteen deer, foxes and rabbits, in closed canopy only.

### 27.3 The improvement that was wrong, and what replaced it

The first attempt at the empty green between the fields was **more objects**: 2,491 grass
tufts over 400,000 m² of open grass. The render showed almost no change, and measuring why
was the useful part: at 0.18 m/px a 1.2 m tuft is **six pixels**, and six pixels every eleven
metres does not alter what the eye sees. The ground still read as one flat colour.

What breaks flat ground is variation **in the ground itself** — rougher grazing, a damper
corner, a different cut. That is 255 polygons rather than thousands of objects, and it works
at every zoom. They sit at z 0.002, under everything: fields at 0.040, water at 0.048, roads
at 0.100 and up, so nothing there can cover a road.

The tufts were kept — they earn their place at detail zoom — but they are not what fixed it.

### 27.4 Faults the checks found in this work

| found | why |
|---|---|
| **16 people** in the whole countryside on the first run | `Ground.free()` refuses a yard, which is right for a tree and exactly wrong for a farmhand. Every farm, works and services stop rejected them. `free()` and `cluster()` now take `allow_yard` |
| **6 buses on a carriageway** | which is where a bus goes. The exempt list knew eight car models and not the bus |
| **4 materials in the cyan band** | orphans — `lowpoly-city` names its materials `c0`, `c2`, `c8`, `c9`, and the four flagged had **zero users**, left behind by an earlier re-run. **98 orphaned datablocks** had accumulated; a stage now purges what nothing uses before it starts |
| green patches **hanging off the plate** into the sky | the mottle had no idea where the world ended. Now clipped — and a **new check** measures the *extent* of everything drawn, because the old one measures a thing's centre and a 58 m patch centred 20 m inside the edge passes it |

The cyan rule also changed from a complaint into a correction. It used to report an
unrecognised cyan material and leave it there; a check that can only complain about a kit
nobody anticipated fails on the next kit. Anything unmapped that lands in the cyan band is now
turned to the world's own green, keeping its own saturation and value, so a green bus stays a
green bus.

### 27.5 Where it stands

**88,236 objects · 22,099,591 faces · every check green.**

    0 standing on a carriageway   0 in the water   0 off the board
    0 taller than it is wide      0 hanging off the plate
    0 belt materials in the cyan band            0 driven by a dead texture
    4 cities, all measured ON THEIR PLATES

**One more, after the sheets were re-cut and I looked at them myself.** Oran had called the
deck over the northern road *"a very nice idea &mdash; but implement it properly."* It was a
flat slab at 5.4 m with two abutments, and from above that reads as a dark rectangle. What
says bridge is the edge you cannot drive off and the piers holding it up: both grade
separations now carry a parapet along each deck edge and piers beneath, set clear of the
carriageway they cross.

**Still not started, and deliberately:** the PATH treatment — the trail markers, START and END,
and the labels over each city. That is page 1's own subject, and it carries a design fork
(the route in 3D, the words as an overlay) that was put to Oran and is unanswered. Building it
on a guess would be the one thing this project has learned not to do.

---

## 28. THE SAME ROAD ON BOTH SIDES OF THE JOIN

> *"Fix all the roads. You added roads on columns that reach the edge of the map, but the
> connection is not right and not consistent, and the elements of the roads are not right and
> do not match, so suddenly the road looks different — just find the elements of the roads we
> built the interchange with and apply the continuation with those same roads. Cars — you
> fixed some, but not all. Many are still perpendicular, and some now drive against the
> direction, as if there were four lanes one way or cars heading at each other. I do not want
> to keep marking things for you by hand like some kind of inspector. Go back over everything
> you built since yesterday, element by element, one by one."*
> — Oran, 2026-08-31

### 28.1 The elements were never the same, and the asphalt hid it

`tools/eventer_gen.py` contains `ribbon()` — the function EVENTER's interchange was actually
laid with. The belt's roads did not use it. Measured against it, the running surface matched
to four decimal places and **nothing structural did**:

| element | EVENTER's interchange | the belt's continuation |
|---|---|---|
| asphalt | 0.0482, 0.0497, 0.0595 | **identical** |
| deck | 0.90 m box with a soffit | a plane of zero thickness |
| soffit | 0.1620, 0.1590, 0.1499 | **absent** |
| edge walls | conc 0.3325, 0.3231, 0.3005 | absent |
| parapet | barrier 0.6240, 0.6105, 0.5520, 0.90 × 0.35 | pier grey, 1.10 × 0.60 |
| kerb | 0.5395, 0.5520, 0.6171 (cool) | 0.4969, 0.4852, 0.4508 (warm) |
| white | 0.8276, 0.8194, 0.7678 | 0.7453, 0.7453, 0.7156 |
| marking width | 0.45 m | 0.36 m |

That is why it read as a different kit while every colour probe said the roads agreed: the
**tarmac** agreed and the **structure** did not.

The whole table now lives in `world_road.EV_SRGB`, converted the way EVENTER converts it, and
`world_provenance.py` asserts — inside Blender, against `eventer_gen.PALETTE` — that it still
matches, then measures every elevated-road material in the built file against it. It failed
the first time it was run, naming the exact three materials that were wrong.

### 28.2 What the belt's roads were missing at ground level

Putting the two renders side by side at full resolution — EVENTER's carriageways and the
belt's, forty metres apart on the same sheet — named the rest of it:

- **No kerb.** Every EVENTER road is bounded by a pale kerb strip down both edges. The belt's
  were bare asphalt meeting grass. A kerb is a *continuous* line, so it draws the road's shape
  at any zoom, which a dashed lane line cannot.
- **No yellow.** `eventer_gen.mark_spec()` puts white on the edges and lanes and **yellow down
  the middle**, because yellow is what says *do not cross*. The belt drew a white dash there.
- **A stone footbridge under a motorway.** `nature-kit/bridge_stone` stretched to a 26 m span
  reads as a grey slab dropped across the water.

MAIN, DUAL and TRUNK now carry kerbs, a doubled yellow centre line, and cross the stream on
the same deck the viaducts are built from. LANE and ROAD keep their white dashes and their
stone or timber bridges — those are the *"small narrow roads unrelated to the four big maps"*
that were exempted from having to match.

### 28.3 The cars were consistently backwards

Two faults, and the second was hiding behind the first.

**Across the road.** The first pass added `place_facing()` and converted the callers that draw
traffic. It missed seven others — the tractors in a farmyard, the lorry at the pumps, the
parked cars at a services stop — because converting call sites one at a time fixes the ones you
remembered. The rule now lives in `place()` itself: **a car-kit model handed a heading is
always turned so its long axis lies along it.** Every caller that exists and every caller
written later gets it, and there is no way left to place a vehicle sideways by forgetting which
function to call.

**Against the direction.** A bounding box gives an axis, not a direction. All fourteen fleet
models were rendered at heading 0 from straight above, and every cab — delivery, truck-flat,
truck, delivery-flat, the bus, both tractors — pointed **west** where heading 0 means east. The
nose of a car-kit model is its local **−Y**, not +Y, so the whole fleet was driving in reverse.
Consistently, which is why it survived the first pass: nothing collided, everything simply
reversed. One sign.

**Head-on inside one carriageway.** `build_fleet` decided which way a car faced from its
**lane's** offset instead of its **carriageway's**, so on a DUAL or a TRUNK — offsets ±13, four
lanes each — every carriageway got traffic in both directions meeting head-on. That is Oran's
*"four lanes one way, or cars heading at each other"* exactly. A single carriageway still takes
its direction from the lane, because that is what a centre line means.

### 28.4 A viaduct is still a road, and still needs lighting

LINK 0 and EVE-N 404 had not one lighting column between them. Both are short — 140 m and
76 m — and both descend from the interchange, so `ramp_runs()` carries a viaduct along their
**whole length**. A column at ground level under its own deck is nonsense, and the code could
only say no, so every one was thrown away.

They now stand **on** the deck, at its own height, inside the parapet — computed from
`ramp_span()`, the same function `build_ramp` lays the deck from, so the deck and the columns
standing on it cannot disagree.

### 28.5 The audit that Oran asked for, and the five checks that were wrong

`tools/world_inspect.py` asks nine questions of the built file: sun and shadow, orientation,
direction of travel, lighting columns, road intersections, layer discipline, z-fighting,
degenerate geometry, and floating.

The first run failed six sections. **Five of the six were the check, not the world.** It looked
for lighting columns called `LAMP*` when they are called `light-square`; for a sun in a file
whose sun is built at render time; for road surfaces called `CARRIAGE` when they are called
`C_*`; it called 2,691 of EVENTER's own lorries standing on EVENTER's own viaducts "floating";
and it called 614 degenerate triangles inside Kenney's kit meshes a fault of this project's.

A check that names the wrong thing reports a clean world as broken, which is worse than
useless — it teaches you to ignore it. Each was corrected to measure the property it claims to:
the sun against the four cities' merge contract; the columns by their real names; "floating"
and "degenerate" scoped to what the belt itself built, by the `stg` stamp; and z-fighting to
require that two close layers actually **overlap in plan**, because a field's headland at
0.041 and its rows at 0.042 are 1 mm apart by design and never cover the same ground.

### 28.6 Two faults found by this pass that nobody had reported

- **The camera clipped 1 m to 9,000 m.** An orthographic depth buffer is linear, so that is
  0.54 mm of resolution — and the layer stack separates a field's worked surface from its
  headland by exactly 1 mm, under two depth units. It had held, but holding by two units is
  luck, not margin. `shoot()` now clips to the eight corners of what is actually in shot.
  The first attempt at it **rendered a picture of nothing but sky**: it read the camera's
  `matrix_world` one line after setting `rotation_euler`, and a matrix is only recomputed when
  the dependency graph is evaluated -- so "forward" came out as straight down and the clip
  range was computed for a camera pointing somewhere the camera was not. The same trap as
  `bpy.ops`: it does not fail, it quietly answers a question about a state that has not
  happened yet. The direction now comes from the Euler itself, defined once and used both to
  aim the camera and to work out what it can see.
- **`import world_build` destroys the world.** The module dispatched at import, so a one-line
  check that only asked whether a function existed ran the default `ground` stage — which
  empties the file and saves — taking 88,346 objects and four merged cities down to 767 in
  about two seconds. Blender's own `.blend1` had the previous save. There is now an explicit
  `if __name__ == "__main__":` guard and a copy at `world_belt.blend.SAFE`, because a backup
  that exists only because the tool happens to keep one is not a backup.

### 28.7 The taper was not missing. It was on the floor.

Oran, on the first render of the corrected interchange: *"look at the connection of the roads
into a single road — not good."* He was right, and the measurement is worth writing down.

**LINK 0** is a TRUNK: two 14 m carriageways with a 12 m median, 40 m of paved spread.
**LINK 1** is a MAIN: one 14 m carriageway. They meet end to end at (689, 1063), and that
point is **six metres in the air**, half way down the viaduct.

The heights were already right — both sides hand over at exactly 6.00 m, no step. What was
wrong was lateral: two decks funnelled into one with nothing in between.

And `RD.taper()` had been drawing the trapezoid that joins them since the network was first
built. Its own docstring names this pair — *"an 80 m motorway simply stopped and a 20 m road
started somewhere near it"*. It was laid as a **flat quad at 0.14 m**, on the grass, six metres
below the two roads it was supposed to join. The taper was not missing. It was on the floor.

Three things fixed it:

- `deck_patch()` builds a four-cornered piece of road as a **solid** — deck, soffit, edge
  walls, parapets — each corner at its own height, so a taper on a viaduct is on the viaduct.
- Each ramp now gives up 50 m at whichever end the taper occupies, so the taper fills exactly
  that gap and nothing overlaps.
- `taper_quads()` replaced the single trapezoid with **one per carriageway**. A single
  trapezoid turns the 12 m median to tarmac in one step; a real merge converges. Measured:
  carriageway 0 runs from offset −13 half 7 to offset −3.5 half 3.5, and carriageway 1 from
  +13 half 7 to +3.5 half 3.5 — so the wide end spans −20…−6 and +6…+20, exactly LINK 0's two
  carriageways, and the narrow end spans −7…0 and 0…+7, exactly LINK 1's single one. The
  median closes as the two come together, which is what a motorway merge looks like.
