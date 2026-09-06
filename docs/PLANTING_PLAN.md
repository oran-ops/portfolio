# PLANTING PLAN — the green country around OASIS
Written 2026-08-23, after the plan was built. Everything outside the city is planted;
everything inside the city waits for the buildings, by Oran's instruction. The park is the
one in-city exception and is planted now.

## The palette
All foliage is regraded from the kit's teal (hue 169–181°) into the map's own green family,
measured from TARGET_iconscout.png (#88A04C). Three tint bands, so depth reads as colour:

| band | hue | value | used for |
|---|---|---|---|
| FOREST | ~94° | dark | perimeter belt, dense stands |
| MID | ~86° | mid | grove archipelago, approach trees, park rows |
| MEADOW | ~78° | light-warm | flower glades, park beds, lawns |

Trunks stay brown. `tree_default_fall` (cream crown) is untouched and rationed (~15 on the
map) as a blossom accent. No palms — this is British Columbia, not a resort.

## The rhythms, from the outside in
1. **Perimeter forest** (map edge → ~70 m in): jittered 6.4 m lattice at 88 % occupancy —
   tall pines and broadleaf canopy, 40/30/22/8 tall/crown/bush/grass mix, undergrowth carpet
   on an 8 m lattice at 42 %. Reads as a closed wild belt with no bald patches.
2. **Grove archipelago** (belt → city buffer): the same lattice at ~50–60 %, MID band —
   forest that begins to breathe, with sightlines through it.
3. **Glades**: 9 deliberate clearings (r 16–26 m) kept at ~5 % planting; 6 of them carry
   wildflower drifts — two colour families per glade (red/purple/yellow, A/B variants),
   grass tufts between, a few bushes on the rim. Clustered, never confetti.
4. **City approach** (within ~28 m of the zone): open ground with scattered single feature
   trees and low bushes at ~12 % — the town does not sit in a hole in the forest; the forest
   stands back from it.
5. **Road verges**: every instance keeps ≥3–4 m clear of any kerb (checked per instance
   against the main's true path and every street's segment).

## The park (in-city strip, west of the main road)
- **Allee**: a formal row of `tree_detailed` every 9 m along the road side — the park's edge
  reads from the air.
- Feature groups: 3 oaks (N), 5 pines (S), 3 broadleaf (centre-W).
- 4 round flower beds (r 3.5 m, 8–12 flowers each, mixed families) ringed by low bushes.
- Informal lawn singles and drifts; the central lawn stays OPEN — the playground and paths
  belong to the buildings phase.

## Inside the city — deferred, agreed
Street trees in pits along pavements, garden planting per private plot, plaza planters and
the commercial centre's frontage greenery — all planned to be placed together with the
buildings so nothing needs uprooting.

## Numbers as built
~9,000 vegetation instances: ~2,600 tall, ~2,700 crown/medium, ~120 small, ~3,100 bushes,
~180 grass tufts, ~290 flowers, 15 blossom accents. Deterministic seeds: 20260824–26.
