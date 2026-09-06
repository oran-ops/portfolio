# The junction, designed once — final

Three attempts. The first two were both me trying to simulate how traffic merges instead
of drawing a road. Oran, plainly:

> *"The loop is a fairly narrow two-way road; when it reaches the motorway it just has to
> connect at its own width — an ordinary connection, no widening, no trying to invent a
> special junction. Connect them the way we did in MEDCOIN. The logic does not have to be
> how vehicles merge in reality; it only has to look like an interchange."*

## What the first two attempts got wrong

| attempt | what it did | why it was wrong |
|---|---|---|
| **1. the gore** | closed the ramp's outer edge **at** the tangent point | two lanes of traffic arrived through a 0.30 m needle — a funnel |
| **2. the auxiliary lane** | carried the ramp 45 m past the nose at full width, then closed it | it **widened the motorway** for 45 m to swallow the ramp. Also not a road connecting to a road |
| **3. the mouth** | the ramp turns in and its asphalt runs into the motorway's asphalt | ✅ |

Both earlier attempts also shared a routing fault: the ramps ran **edge to edge** with the
motorway for their whole parallel approach, so there was nowhere to put a barrier between
them. That is why a road-by-road barrier audit came back with L1 only 71 % covered.

## The mouth — the whole thing is three numbers

**1. THE GAP.** Every road running parallel to another is **1.0 m clear** of it. Both then
carry a barrier, and they read as two roads instead of one wide one.

**2. THE TURN.** A ramp's centreline sits `lat` metres outboard of the motorway's edge. An
arc of radius `r` turning through `θ` moves it `r(1 − cos θ)` sideways, so `r = lat / (1 − cos θ)`.

| road | lateral to close | angle | radius | arc | mouth |
|---|---|---|---|---|---|
| loop, flyover | 5.5 m | 30° | 41.0 m | 21.5 m | 18.0 m |
| collector road | 5.5 m | 30° | 41.0 m | 21.5 m | 18.0 m |

**All sixteen turn at the same angle**, which was not the plan. A collector road sits
15.5 m outboard and looked like it would need 40° to close that in the length available —
but it has already eased laterally into the ramp corridor before it reaches the junction,
so by the time it turns in it has the same 5.5 m to close as a loop does. A harder turn
was designed for a problem that the routing had already solved.

**3. THE MOUTH.** A 9 m strip crossing a line at 30° cuts `9 / sin 30° = 18 m` out of it.
So the ramp is carried `half / sin θ` **past** the edge, and everything that ends up inside
the motorway is clipped away — the motorway's own asphalt is already there. What is left is
a full-width ramp opening into an 18 m mouth, and **not one metre of it is a taper**.

## Barriers — one rule

- **Every edge of every road carries a barrier.**
- It stops only across a **mouth** — the span another road's asphalt actually opens — plus
  2 m either side.

That replaced "no barrier wherever another edge is within 1.30 m", which had been deleting
barriers between roads that merely run a metre apart.

## Signs

One per junction, driven by `world-build/tools/eventer_junctions.json`. Placed in the
signage stage with the gantries, as agreed.

## Measured, on all sixteen junctions

| | |
|---|---|
| width at the mouth vs nominal | **9.00 m / 9.00 m** — no junction loses any |
| approach angle | 27–31°, all sixteen |
| ramp asphalt sitting on a motorway deck | **0 corners** |
| roads that end in nothing | **0** |
| barrier coverage, measured on the built mesh | **100 %, 0 gaps** |
| clearance conflicts / worst headroom | **0** / **5.60 m** vs a 5.00 m standard |
| holes visible from the camera | 13 of 11,600 rays, all at plate edges |
| piers standing in a road | **0** |
| steepest grade | **6.80 %** |

## Four times a build and its test read different data

Worth its own heading, because it happened four times in one city and cost more than any
geometry did.

1. `piers()` skipped clashing piers; `verify_piers()` recounted them and disagreed.
2. Windows measured the distance to an edge's **nearest sample** instead of to the edge
   **line** — and 2.5 m resampling made coincident edges read as 1.0 m apart. Every
   junction on L2 was silently skipped.
3. The clearance test compared deck **surface to surface** when the property is surface to
   **soffit** — 0.90 m too generous, and it nearly signed off 4.24 m of headroom.
4. Barriers were built on the **clipped** edge and tested on the **unclipped** one, so
   132 m of barrier that exists was reported missing.

Every one of them was fixed the same way: **one function, every caller.** `pier_sites`
decides where a pier goes. `edge_pt` decides where an edge is. `barrier_windows` decides
where a barrier stops. Build and test both call them.
