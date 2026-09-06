# NIGHT BUILD — buildings phase, 2026-08-23/24
Oran's directive: build the buildings overnight, slowly, building-by-building, checked.
Diversity of styles per district, positioned logically against the streets, honouring the
approved OASIS plan. This file is the running state so a summarized session stays on rails.

## Ground truth
- Scene: `world-build/world_map.blend`. Roads/cars/veg DONE (flat terrain, ribbon roads).
- Zone frame: OASIS 372 m at map (164,139)..(536,511). city-units: u = 8 m, origin (164,139).
- Street data + main path live in scene prop "ROAD_MEAS" (json).
- Typology (measured): `tools/typology.json` — house/terrace/midrise/retail/tower/shed.
- Scales: `tools/kit_scale.json` values are OLD-WORLD UNITS — multiply by 8 for metres.
- index.json maps model name → kit. lowpoly-city has playground/basketball/pool/fence props.
- Oran's House_20_Pack: `Desktop/BLENDER/LowPoly_House_20_Pack.blend` — candidate lux houses.

## Districts (city-units; zones from the approved plan)
| district | rect (x0,y0,x1,y1) | content |
|---|---|---|
| HOUSES | 11.8, 2.0, 43.4, 17.2 | detached houses on hA/hB/hC; east of x=33 = the luxurious side (bigger parcels, best models). Some terraces on the hC row for variety. |
| CENTRE | 11.8, 19.6, 31.4, 30.6 | retail podium blocks (2 retail + 2 office look), continuous shopfronts toward the PLAZA on cA; inner paved court (car park). |
| TOWERS | 32.6, 18.4, 43.6, 31.0 | NE = the height cluster (towers w/ forecourts); S = FASHION+SERVICES low retail block. |
| BLOCKS | 11.8, 32.6, 43.4, 44.2 | 4-storey mid-rise rows on bA/bB with parking courts. |
| PARK | west strip | planted. Playground (kid-playground-1) comes with the buildings-props pass. |

## Method (the lessons, applied)
- Parcels along frontages; each building FACES its street (rotation from street side).
- Setbacks: house 5 m · terrace 2 m · midrise 6 m · retail 3 m · tower 8 m (forecourt).
- Claim = real footprint rect (axis-aligned; grid city) + no-overlap test per placement.
- Clearance vs street centrelines ≥ half-road + setback; zone containment per building.
- Audit after every district: overlaps=0, road-clear=0, in-zone=100%, facing correct.
- Deterministic seeds. Closeup render per district, eyeballed before the next district.
- Scale VERIFIED per model against door/storey heights before mass placement.

## Status checklist
- [x] Inventory sheet of building models rendered + measured (BLDG_SHEET.png, 62 models)
- [x] Houses district: 29 kit houses in 4 street-facing rows + 2 kit manors restored on the
      lux side + 2 pack villas (house_5, house_6) + 2 pools. Lux east = large lots, correct.
- [x] Blocks district: 13 mid-rise slabs in 3 rows + 2 marked parking courts + 8 parked cars
- [x] Centre: shop rows on boulN/cA (canopy models culled, swapped for real shops incl. the
      mint ice-cream kiosks — Oran to judge), office row on boulS, 2 plaza plates + planters
- [x] Towers + fashion: 5 glass towers + low retail row + eastD offices
- [x] In-city vegetation v1: 54 boulevard trees, 11 yard trees, 16 plaza planters, park
      extras; park playground + basketball court
- [x] Final audit: 0 real overlaps, 0 on-road, 0 outside-zone (77 building/prop objects)
- [x] Renders NIGHT_map / NIGHT_houses / NIGHT_centre / NIGHT_towers / NIGHT_blocks

## Verdict + open refinements for Oran's morning review
Buildings phase v1 stands: every district populated per the approved plan, everything
street-facing, audited clean. Honest gaps to refine WITH Oran:
1. The commercial centre lacks its single big anchor (the 160×96 retail podium as one mass —
   the plan's "2 retail + 2 office" box). Current centre = perimeter shops, no anchor.
2. Oran's House_20_Pack: house_2/20 are diorama scenes (baked terrain base, textures not
   packed → magenta) — removed; house_5/6 fitted after solid-recolor. Discuss whether to
   deep-import more of the pack (separating houses from bases).
3. Density: rows could take an infill pass (targeted gap-filling, not the naive one).
4. Street furniture (lamps, signs, people) and driveways/fences — next detail pass.
5. bY street feeds via bB (no direct mouth on the main) — deliberate.
