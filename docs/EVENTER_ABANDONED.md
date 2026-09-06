# EVENTER — the abandoned ground (YELLOW). Plan for approval

Oran's brief, in his words:

> *"Under the interchange it should be brown earth — not green like OASIS. An area of
> abandoned businesses, abandoned buildings, abandoned vehicles, barrels, dumped tyres,
> bare fences, and here and there a food business. I mention a homeless area not to create
> that mood, but only to describe the ELEMENTS we will build with. It does not need to be
> as crowded as MEDCOIN, but it does need to be as built-up as OASIS."*

## 1. The ground, measured

| | |
|---|---|
| the earth square, 275–525 × 245–495 | **62,500 m²** |
| piers standing in it | **81**, heights **5.5 – 18.6 m** |
| ground the piers themselves take | 1,274 m² |
| ground kept clear so pier shadows read | 854 m² |
| **buildable** | **60,372 m² (96.6 %)** |

**The shadow rule is derived, not fixed.** The earlier plan said "4.2 m clear south-west of
every pier". The sun was then measured: it sits in the **north-east** at 75°, so shadows
fall **south-west** — the direction was right — but a shadow is `height × cot 75° = 0.268 h`,
which is **1.46 m for the shortest pier and 4.99 m for the tallest**. One fixed number was
three times too big for some piers and too small for others. The keep-out is now each
pier's own shadow plus 1 m.

## 2. What goes in it — every element Oran listed

| element | source | count |
|---|---|---|
| abandoned buildings and businesses | city-kit-industrial, **20 types** | 30 |
| food businesses | lowpoly-city fast-food, food truck, awnings | 5 |
| abandoned vehicles | car-kit, **50 models**, rust-tinted | 34 |
| barrels and drums | food-kit barrel, factory-kit boxes | 50 |
| **dumped tyres and wheels** | car-kit debris-tire + 8 wheel types | 90 |
| car debris — bumpers, doors, panels | car-kit, **14 debris models** | 70 |
| dumpsters and waste containers | retro-urban, lowpoly-city | 24 |
| **bare fences** | construction fence, low fence, conveyor rails | 60 |
| rubble, bricks, beams, blocks | retro-urban-kit | 80 |
| cables and broken barriers | retro-urban, **5 barrier types** | 40 |
| chimneys and tanks | city-kit-industrial | 10 |
| dead scrub and weeds | nature-kit, desaturated | 80 |
| | | **573** |

## 3. Four rules, and each one is a test

**A. Nothing may pass through a deck.** L1 is only 6.5 m up and an industrial building is
8–12 m tall. Every object's height is checked against whatever is above that spot, and a
building that does not fit is swapped for one that does. *Test: 0 objects intersecting a
deck.*

**B. Nothing on a pier, nothing in its shadow.** *Test: 0 objects within a pier's footprint;
0 inside its own measured shadow strip.*

**C. Nothing leaves the earth square.** The planting belt begins at its edge and the two
must not mix. *Test: 0 objects outside 275–525 × 245–495.*

**D. Occupied, not packed.** "As built-up as OASIS, not as crowded as MEDCOIN" is a
density, so it gets a number: **35–55 % of the buildable ground within 4 m of something**.
Below that it reads as empty, above it as a scrapyard.

## 4. Variety — the standing rule

| category | min models | max share |
|---|---|---|
| buildings | 14 | 12 % |
| vehicles | 16 | 10 % |
| debris and tyres | 12 | 14 % |
| props (barrels, dumpsters, rubble) | 14 | 12 % |
| fences | 4 | 35 % |

Plus **rust tinting per instance** — the abandoned vehicles and steelwork get their own
shade through an object-level Hue/Saturation node, the same mechanism that gave the villa
roofs eight colours from one texture atlas.

## 5. How it ties to the blue and red zones

- The **blue belt** already screens this zone from the villas — its tall conifers sit on
  the belt's inner edge, facing this way, exactly so that this is what they hide.
- The **collector ring** is the second separator, as Oran put it: *"the road is a separator
  too."*
- So the yellow zone can be as derelict as the brief asks **without touching the villas**:
  58 m of planting and carriageway sit between them.
- Nothing here uses the villa palette. This zone is brown earth, rust, bare metal and grey
  concrete — it must not read as a continuation of the lawn.

## 6. Order of work

1. props library — import, **measure each file**, rust-tint
2. buildings first, largest-first, each checked against the deck above it
3. vehicles, then fences, then the small debris — same occupancy discipline as the plots
4. verify all four rules and the variety table
5. render, read the picture, fix what the numbers could not see
