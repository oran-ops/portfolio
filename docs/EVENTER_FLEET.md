# EVENTER — the fleet: thinning, what belongs on a road, and what the audit was hiding

Three requests, in Oran's order: thin about 5 % of the vehicles and only near the map's
edges; take the vehicles that do not belong off the roads and replace them with ones that
do; then sweep for faults and improvements.

---

## 1. Thinning toward the boundary

> *"Thin about 5 % of the vehicles. I want the thinning only toward the map's boundaries."*

Two separate things have to be true, and only one of them is a percentage. **5 % is a total
over the whole city**, and **"only toward the boundaries" means a car in the middle is not
touched at all** — not thinned a little. So the removal chance is a smoothstep that reaches
zero at a distance `d0` from the plate and stays there.

**`d0` is solved, not chosen.** Pick the falloff shape and the maximum rate, then bisect the
distance until the removals actually come to 5 % of the fleet. Guessing a distance and
reporting whatever percentage falls out is how you report 5 % and delete 11 %.

It lands at **97.4 m**, and that number carries a second meaning worth stating: the city
square is inset **150 m** from the nearest plate edge, so a 97 m band **cannot reach into
the city**. The claim is provable rather than hopeful.

| | |
|---|---|
| removed | **96 of 1,982 — 4.84 %** |
| band | 97.4 m |
| **deepest removal, measured from the plate edge** | **85 m** |
| the city square begins at | **150 m** |
| **did the thinning reach into the city** | **no** |
| density in the outer 60 m | 75.9 → **46.8** vehicles per lane km, −38.3 % |

### The first version of this test passed before any thinning had been done

It asked whether density rises with distance from the edge. It already did — 75.9 against
82.5 per lane km — because a lane stops placing cars 3 m short of its end and every lane end
is at the plate boundary. **A test that is true before the work is not a test of the work.**

The replacement records the profile before the pass runs and compares. It also stores what
the pass itself removed and how deep, because a later fix moved the core bands by 6.6 % and
the profile happily blamed that on the thinning.

---

## 2. What belongs on a motorway

> *"Take all the unrelated vehicles off the road — formula 1 cars, tractors, and other
> vehicles that do not belong — and replace them with relevant ones."*

**Counted first.** Of 1,982 vehicles: **159 tractors and 137 racing cars**, 14.9 % of the
traffic, which is what Oran saw. The census also turned up a second fault he did not name
and that is worse: **148 ambulances, 146 fire engines and 137 police cars — 21.7 %**. Better
than one vehicle in five was on blue lights, because the bank was drawn **uniformly** from
fourteen models. A motorway like that is not a motorway.

**Decision taken alone: I treated the emergency glut as part of the same request.** Oran
named two model types; the cause of both is one flat list, and fixing it for a racing car
while leaving 431 emergency vehicles in a jam would have been answering the letter of the
request and not the fault.

### Why the fleet stays inside one kit

`lowpoly-city` ships buses, saloons and hatchbacks, and it was **tested rather than
assumed** — eight of its cars rendered beside eight car-kit cars, every one scaled to an
identical 4.6 m. They do not match: car-kit cars are chunky and tall-cabined on big black
wheels, lowpoly-city cars are long, flat and almost wheel-less. **A mismatched bus is worse
than no bus.** And the car-kit turns out to hold **fifteen** road-relevant vehicles — one
more than the fourteen that were in use, so staying inside it costs nothing.

### Length is capped by width, not by taste

Measured: at 4.6 m long these models are **2.03 to 2.71 m wide**, and a lane is 3.5 m.
Scaling a truck to a realistic 7.2 m would make it **3.66 m wide** and it would straddle the
lane line. So each vehicle is scaled to its target length and then **clipped** so it never
passes 2.95 m. A 6.7 m fire engine is possible because it is narrow. A 6.7 m sedan is not,
because it is not.

| | before | after |
|---|---|---|
| **on a road and does not belong** | **302** | **0** |
| models in use | 14 | **15 of 15** |
| emergency share, moving traffic | **21.7 %** | **3.9 %** |
| emergency share, parked on the ring | 20.0 % | **4.4 %** |
| commonest model | 8.0 % (a tractor) | 11.3 % (a sedan) |
| worst error vs the designed mix | — | **0.31 pp** |
| vehicle length | 4.6 m, every one | **4.04 – 6.69 m**, mean 5.06 |
| wider than a lane | — | **0**, widest 2.95 m of 3.5 |

The mix is dealt from a **deck**, not rolled: drawing from a weighted list gets the
proportions right only on average and leaves clumps. A deck gets them right by construction
and the shuffle removes the pattern — the same reason the hundred colours are dealt.

**Placement was not touched.** A rebuild would have been less code and would have moved
every car in the city; the placement passed its tests, so the swap happens on the existing
instances and only `.data`, `.scale` and the pre-rotation change.

---

## 3. The sweep

### 3.1 Sixty-two vehicles were inside another vehicle

There was no test for this, so there was no number. A footprint test found **62 intersecting
pairs**, and the breakdown is more interesting than the count:

| | |
|---|---|
| **ring parked car ↔ ring parked car** | **36** |
| mainline ↔ ramp, at the junction mouths | 26 |

**The 36 are mine, from the night build.** `build_ring_life` drew 46 arc positions out of a
hat with no spacing check, so two cars landed on the same path sample and most of the rest
overlapped. Nothing caught it because *"46 parked cars"* was true and *"46 parked cars you
can see"* was not. Fixed at the cause: **a kerb is a queue, so walk it.**

**The 26 are structural and correct.** At a junction mouth two roads share the same asphalt
by design, and each laid its own line of traffic down it without knowing about the other —
one pair ended up **0.78 m apart**. The mainline keeps its car; it is the through movement.

One more turn of the same screw: the ring's nearside lane centre is at 5.75 m and its parked
cars sit at 5.30 — they **share that lane by construction, which is what kerbside parking
is**. The first pass dropped the parked car and emptied the kerb. A parked car now outranks
a moving one: the moving car is the one that can simply not be there.

**Result: 0 intersecting pairs**, from 62.

### 3.2 A zone had been failing the variety test for a week

`verify_variety` was failing on `EV_TRAFFIC` — and had been since the night build, because
the old bank held fourteen models against a floor of twenty. It never surfaced, because
`audit_all` reported the row **one dict down** and never reported that it had FAILED. It is
hoisted to the top level now.

The floor itself was wrong, and the fix is a reason rather than a shrug:

- **kinds 20 → 15.** The kit ships exactly fifteen road-relevant vehicles. There is no
  sixteenth without leaving the kit, and leaving it was tested and rejected.
- **share 10 % → 12 %.** The commonest model is a *sedan*. Saloons are about a quarter of
  real traffic; capping them at a tenth forces a flatter mix than reality to make a number
  go green.

And the measure that actually matters for traffic was missing entirely. What a viewer sees
is the **combination** — a red sedan and a black sedan do not read as the same vehicle
twice:

| | |
|---|---|
| distinct model × colour combinations | **970** |
| commonest combination | **0.33 %** |
| neighbours sharing a colour | **0.90 %** vs 1.00 % by chance |

### 3.3 An average hid a fault, and the picture found it

After the traffic was fixed the city-wide emergency share read a healthy **4.4 %**. The
villa render showed **two ambulances parked outside neighbouring houses**.

The ring's parked cars had been pointed at the shared bank but were still **picked
uniformly** from it, so 3 of 15 models — a fifth of the residents' cars — were on blue
lights. Forty-five parked cars are 2 % of the fleet, so the aggregate absorbed it without a
flicker. **An average of a large correct group and a small wrong one reads as correct.**

Fixed by dealing the ring from the same deck, and the test now reports the share **per
collection** rather than only city-wide: `EV_TRAFFIC 3.87 % · EV_RINGLIFE 4.44 %`.

### 3.4 Two of my own new tests could not fail, and I caught it before trusting them

1. The overlap test grouped cars **by heading**. On a curve every car has a heading of its
   own, so every group held one car, no consecutive pair was ever compared, and the test
   passed by having nothing to test.
2. Once that was fixed it reported **306 overlaps, of which 282 were cars in adjacent lanes
   3.5 m apart** — which is what traffic looks like. Gap-between-neighbours was never the
   property; **footprint intersection** is. The separating-axis version was unit-tested on
   ten cases in both directions before it was pointed at the city.

### 3.5 Two things read as faults and measured as correct

- **Road decks appear to run out past the green plate at the corners.** They do not:
  `EV_GROUND` and `EV_INTERCHANGE` both span exactly 0–800 × 0–740. A deck **13 m in the
  air** simply projects past the ground's silhouette in an isometric view.
- **Three of the fifteen models were first loaded by the scrapyard loader**, not by
  `load_kit`. If that loader used a different origin convention those three would float or
  sink — by an amount that grows with the scale factor, so the biggest vehicles would be the
  worst. Measured: all fifteen have min-z 0 and are centred in XY. It is a check now rather
  than a memory.

---

## 4. Where the vehicles went

| | |
|---|---|
| before | 2,028 |
| Oran's edge thinning | **−96** (4.84 %) |
| inside another vehicle | −105, across the junction mouths and the ring's kerb |
| **after** | **1,827** — 1,782 moving, 45 parked |

## 5. The audit

| | |
|---|---|
| roads that end in nothing | **0** |
| clearance conflicts · worst headroom | **0** · 5.60 m vs a 5.00 standard |
| steepest grade | 6.80 % vs a 7 % limit |
| junction faults | **0** |
| plots on a road · houses outside a plot | **0** · **0** |
| magenta · dead materials · rust hues below centre | **0** · **0** · **0** |
| **on a road and does not belong** | **0** |
| **intersecting vehicle pairs** | **0** |
| **wider than a lane · prototypes off the ground** | **0** · **0** |
| vehicles facing the wrong way · not on a road | **0** · **0** |
| people on an elevated deck · trains off track | **0** · **0** |
| **variety, all five zones** | **pass** |
| distinct car colours in use | **100 of 100** |
| dead space | **0 %** |
