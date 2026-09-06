# XTIX — the build. Every decision taken alone, and every fault found on the way

Oran left the machine and gave standing authority to build the city to the plan, taking any
decision myself and reporting all of them at the end. This is that report.

**The build ran to `XTIX_PLAN.md` section 9, in order, with a verification pass after each
stage rather than one at the end.** Nothing here was invented: the builder
(`world-build/tools/xtix_gen.py`) reads `xtix_plan.py`, the same structures the drawing
renders from and the audit measures.

---

## 1. What got built

| stage | what | result |
|---|---|---|
| 1 | ground, verge, 16 road corridors, kerbs, pavements, markings | 1 object |
| 2 | 174 plots pegged: yard, or hoarded earth dug to its stage | 51 hoardings, 19 courtyards |
| 3b | podiums holding the street wall | **114** |
| 3+4 | **172 buildings** — 20 shape families × 12 facades × 11 tints | 172 objects |
| 4b | site elements, **different at every stage** | **1,226** |
| 5+6 | tower cranes, derived from stage — and the landmark's | **41** |
| 8 | traffic: 520 moving + 240 parked | **760** |
| 8b | people: 1,600 on pavements + 255 crew | **1,855** |
| 8c | 328 street trees + 196 verge trees | **524** |
| 8d | street furniture, 14 models | **396** |
| 9 | plaza, park and 19 service courts | **352** |

**5,421 objects · 4,833,534 triangles** — against EVENTER's 5.89 M, with **1.06 M of
headroom**. The plan estimated 3.78 M; the towers and the public space came in heavier than
budgeted, which is stated here rather than smoothed over.

---

## 2. Decisions I took alone

### 2.1 A tower is scaled to its plot in X and Y, and its height is left exact

The twenty archetypes have fixed plan dimensions; the plots do not. Something had to give.
**The height is the property the plan actually specifies**, so it is kept exact and the
footprint is scaled to the plot. The cost is the shape's aspect ratio, which no test
measures and no eye reads at 4.44 px/m.

### 2.2 Crowns are a proportion of their building, not a fixed size

The first city came out as **a field of spikes**. Every crown was 17–30 m tall whatever it
stood on — nothing on a 200 m tower, and doubling the height of a 45 m one. **Now 11.5 % of
the shaft, capped at 30 m**, with the parapet and sky-garden crowns capped lower still
because a parapet is a parapet whatever it sits on.

### 2.3 The shape decks are weighted toward the forms that do not taper

Six of residential's nine shapes tapered to a point, and residential is 70 of the 172
buildings — so **half the city ended in a spike**. Real apartment towers are slabs, point
blocks and stepped terraces. The decks now repeat `slab`, `setback`, `terrace` and `twist`,
and the sculptural forms are the minority they should be. `a_cone`'s taper was also eased
from 0.36 to 0.55: at 0.36 it was a cone, and a cone is a shape, not a building.

### 2.4 The tint bands were widened, and the audit rule with them

The first city read **monochrome**. The neutral band started at 120 m and the tall towers
are most of what you see, so the colour was all hiding at ground level where nothing is
visible. Measured on the palette: the cool tints are not the saturated ones — gold and amber
sit near 0.47, azure at 0.50 but at far higher value. **Cool now runs to 165 m**, and the
audit rule was re-scoped to the genuinely warm end, which is what MAP_ANALYSIS 1.5 is
actually about.

### 2.5 Three archetypes and one facade were built and never used

`lean`, `torus` and the `ribbon` facade appeared in no use-class list, so 18 of 20 families
reached the city and two were built for nothing. **A vocabulary is only a vocabulary if
every word is used.** All 20 shapes, all 12 facades and all 11 tints are now in the city.

### 2.6 Five of seven street-furniture filenames were wrong

`light-curved`, `traffic-lights`, `sign-post`, `detail-bench` and `detail-bin` do not exist.
**A guessed name loads nothing and fails silently** — EVENTER recorded exactly this against
`hatchback`. Checked against the folder, the bank went from **2 models to 14**.

---

## 3. Faults found during the build, and fixed

### 3.1 The ground covered every road in the city

The city-wide ground slab was laid at z = 0.10 and the carriageways at 0.00, so **only the
painted markings showed through**. Ground is the bottom of the stack, not a layer in the
middle of it. The z-order is now stated explicitly in the file: ground 0.00 < asphalt 0.05 <
markings 0.062 < kerb and pavement 0.21 < plots 0.23.

### 3.2 Six archetypes are not centred on their own origin

A bundle sits on a 2 × 2 grid; a bridge is two towers 32 m apart. Placing the object origin
at the plot centre therefore put the building off-centre by however far its shafts are
pushed out — **10 buildings outside their plot and 4 interpenetrating.** The fix is to
centre the **bounding box**, not the origin.

### 3.3 THE HEADLINE: the builder and the verifier had different cities

The verifier reported ten buildings up to 54.8 m short. Chasing it down, the objects' own
stored values disagreed with the plan — one carried `H = 31.1` where the plan said 38.7, one
carried `prog = 0.142` where the plan said 0.882.

**`plots()` was not a pure function.** `landmark_block()` read the module-level
`MATURITY_CUT`, and `summary()` overwrites it. So calling `plots()` before or after
`summary()` moved the landmark, which changed that block's tier, which changed the plot
count, which shifted the entire random stream downstream. **The builder built one city and
the verifier checked another.**

This is the sixth time across four cities that a build and its test read different data, and
it is the most dangerous instance of it yet — because everything *looked* right. The fix is
the fix it has always been: **pass the argument, do not read the global.** `plots(seed, cut)`
is now proved deterministic across a `summary()` call in both directions.

### 3.4 Three of my own checks were measuring the wrong thing

| check | what it did | what it should do |
|---|---|---|
| carriageway / pavement bands | a band is infinite along its own axis, so a car 60 m outside the city was "on a road" and **181 people correctly on a pavement were flagged for standing in traffic** at junctions | bound the band to the city, and count someone as in the road only if they are in a carriageway **and not on any pavement** |
| dead space | marked the cell an object's **origin** landed in, so a 62 m building filled 1 cell of the 9 it covers — the city read as **10.2 % empty** when it is 0 % | mark the object's **extent** |
| dead textures | counted image nodes with no data, and so reported **75 faults after all 75 had been fixed** | count only dead images still **linked into the shader** — measure the output, not the input |

### 3.5 And EVENTER's lesson 11, arriving for the second time

`b_height` was the one check in the file that did not call `view_layer.update()` before
reading `matrix_world`. It duly reported ten buildings short that were not short at all — it
was reading matrices from before the scale was applied.

> *Read `matrix_world` only after `view_layer.update()`.* Written down after OASIS. Broken
> again here.

---

## 4. The verification — 11 checks on the BUILT scene

Not the plan; the geometry that exists. Every one fed a deliberate break first: **7 of 7
rule-4 proofs caught their break**, and one of them (`vehicle on road`) *failed* to catch it
first time, which is how fault 3.4 was found.

| | check | result |
|---|---|---|
| ✓ | vehicles facing the wrong way | **0** of 760 |
| ✓ | vehicles not on a carriageway | **0** |
| ✓ | vehicles outside the city square | **0** |
| ✓ | people standing on a carriageway | **0** of 1,855 |
| ✓ | buildings outside their plot | **0** of 172 |
| ✓ | buildings shorter than planned | **0** |
| ✓ | intersecting buildings | **0** |
| ✓ | crane jibs fouling a taller building | **0** of 41 |
| ✓ | dead images still feeding a shader | **0** |
| ✓ | dead 20 m cells in the built city | **0** of 729 |
| ✓ | built counts vs the plan | worst error **0.7 %** |

**Buildings 172/172 · cranes 41/41 · vehicles 760 of 765 · people 1,855 of 1,858.**

And the plan audit still passes all 21 checks after every change made during the build.

---

## 5. The finish pass — "faded, grey, not modern"

Oran, on the built city: *"the colours are very faded and do not read as future or modern,
the colours read very grey. The buildings need to be glossy, like new buildings."*

He is right, and the numbers said so before the render did. **Two causes, both mine.**

### 5.1 There was nothing to reflect

The world was flat 0.8 grey in every direction. **A glossy surface in a featureless world is
a matte surface** — a mirror would have rendered grey, and no amount of lowering roughness
could have shown. What makes a real glass tower read as glass is the **vertical gradient of
the sky running down its face.**

The existing world already split camera rays from the rest, so the fix cost nothing
elsewhere: **camera rays still see the identical flat 0.8 backdrop**, which keeps XTIX's
background matching OASIS, MEDCOIN and EVENTER exactly. Only reflection and diffuse rays see
a sky — warm ground bounce below the horizon, a grey horizon band, a cool zenith — and only
the buildings care.

Materials went from roughness **0.22 with no coat** to **0.05–0.13 with a clear coat and a
real IOR of 1.46**. That is what glass is.

### 5.2 My own rule was draining the colour

Measured before touching anything:

| tint | saturation |
|---|---|
| glass_pearl | **3.3 %** |
| glass_pale | 6.9 % |
| glass_smoke | 11.6 % |
| glass_ice | 21.8 % |

Those four are `TINT_NEUTRAL`, and `tint_for()` gave **only those** to every building over
165 m. The skyline — most of the image — was painted at a mean **10.9 % saturation**. That
is the grey, and it came from a rule I wrote to satisfy MAP_ANALYSIS 1.5.

**Oran has overruled that rule for this city, and it is recorded as his call rather than
smuggled through.** What survives of 1.5 is the part still true: gold and amber, the two
genuinely hot tints, stay off buildings over 150 m — a 200 m mass of hot orange is too much.
Everything else is available at every height.

| | before | after |
|---|---|---|
| palette saturation, mean | 33 % | **46 %** |
| palette value, mean | 0.74 | **0.84** |
| glass roughness | 0.22 | **0.05 – 0.13** |
| clear coat | none | **0.55** |

### 5.3 And a grey grid was laid over every colour in the city

One shared spandrel at value 0.43 and one shared near-white mullion, across all 172
buildings. On a facade the bands and mullions are a large fraction of what the eye actually
meets, so a single grey pair greyed **every** building regardless of its glass.

**The slab band and the mullions now derive from each tower's own glass** — a darker,
slightly desaturated version, which is what a real curtain wall is: the same glass,
back-painted, in a frame that belongs to the building. **The roofs too**, because at this
camera angle a great deal of what you see is roof, and one grey across 172 of them is the
same fault one plane up.

### 5.4 A fault the fix caused, and how it was caught

Purging the material cache to force the new colours left **41 cranes with empty material
slots** — they rendered white instead of yellow. The material cache is keyed by name, so
deleting a material silently empties the slot of every object that was using it and was not
rebuilt.

A check now runs after every material purge: **objects with an empty material slot must be
zero.** It found the 41; it now reports 0.

**All 11 build checks and all 21 plan checks still pass after every change above.**

---

## 6. The second finish pass — investigated, then improved

Oran: *"looks better, but run another significant improvement. Investigate, improve, update,
make everything better. Run analyses and check whether we have anything to add, replace or
improve."*

**So the first thing was to measure where the remaining weakness actually was, not guess.**

### 6.1 The measurement that set the priority

Projected area in the frame at the isometric camera — a horizontal surface projects by
sin(54.7°), a vertical one by cos(54.7°) — over all 172 buildings:

| | m² projected | share |
|---|---|---|
| **roof and podium deck** | 131,571 | **21.5 %** |
| facade | 481,422 | 78.5 % |

**And facades occlude one another in a dense grid while roofs never do**, so the roof share
of what is actually *seen* is higher than 21.5 %. **Sixty-four of the 172 buildings are
roof-dominant.** Every one of those roofs was a flat grey cap.

That is the largest untouched surface in the city, and it decided the order of work.

### 6.2 The roofscape

What stands on a roof is decided by **what the building is** — so a roof is one more thing
that tells an office from an apartment block *from above*, which is where this map looks
from:

| use | on the roof |
|---|---|
| **office** | plant rooms, a run of chillers, aerial masts |
| **residential** | water tanks, a roof garden, small plant |
| **landmark** | a **helipad**, and three masts |

**The count scales with the roof.** A fixed number left a 60 m deck with the same two
aerials as a 20 m one — the largest roofs, which fill the most frame, were the emptiest.

### 6.3 The facade was one flat colour over 78.5 % of the frame

Two glass variants — the same tint a shade lighter and a shade darker — now pick per floor
from a **deterministic hash of the floor index**, so a facade has the quiet unevenness a
real one has (panels catching the sky at different angles, blinds down on some floors)
without any randomness that could differ between a build and a rebuild.

And **a cap and a base**: on any tower over 14 floors the top three and bottom two take the
frame material. That is what makes a tower read as *designed* rather than extruded.

### 6.4 The podium had no shopfront

Oran's brief asks for luxury restaurants and shops at the base of the towers, and a podium
that is one flat band of glass from pavement to parapet has neither. The ground floor is now
**taller and darker — a glazed shopfront — with a bright fascia band over it.** That fascia
is the one place in this city where a saturated colour is genuinely a *small* thing, so it
still obeys MAP_ANALYSIS 1.5 while the rest of the palette no longer does.

### 6.5 A fault this pass introduced, and caught

Deriving the roof colour from each tower's tint at 60 % brightness gave a **near-black plate**
on the darker tints — value 0.23 on the blue towers — which read as a hole punched in the top
of the building. A roof deck in daylight is gravel, membrane or pavers: a **light** surface.
Mixed mostly toward a light grey with only a hint of the building, it lands at 0.70–0.75.

The shaft's own top cap was also `dark`, and showed past several crown types. It is a roof
now, because it is one.

| | |
|---|---|
| triangles | **4,785,798** — 1.10 M under EVENTER |
| build verification | **11 of 11 pass** |
| plan audit | **21 of 21 pass** |
| objects with an empty material slot | **0** |

---

## 7. Third pass — the fault under all of it

Oran, on the built city:

> *"On the roads there are no cars, or there are grey unclear elements — I don't understand
> what they are. I also don't see people. Work on it with traffic signs too, and work
> properly on the execution."*

Every one of those objects was in the scene. The verification said so, and the verification
was right: 760 vehicles on a carriageway, facing the correct way; 1,855 people on a pavement,
none in the road. All eleven checks passed.

**They were lying down.**

### 7.1 The root cause

`bpy.ops.wm.obj_import` *does* convert Y-up to Z-up — but it leaves the mesh in the file's own
coordinates and puts a `+90°` X rotation on the **object**. Proven by importing one character
three ways:

| import | mesh extent | object rotation | world extent |
|---|---|---|---|
| as coded | 1.60, 2.70, 0.80 | (1.571, 0, 0) | 1.60, 0.80, **2.70** |
| defaults | 1.60, 2.70, 0.80 | (1.571, 0, 0) | 1.60, 0.80, **2.70** |
| up_axis=Z | 1.60, 2.70, 0.80 | (0, 0, −3.142) | 1.60, **2.70**, 0.80 |

`load_model()` then called `transform_apply(rotation=True)` to bake that in. It is an
**operator**: it needs the object active and selected in the view layer, and these prototypes
are linked into a hidden library collection, so it silently did nothing. The placement code
then wrote `rotation_euler = (0, 0, yaw)` and the conversion was gone for good.

Measured after the fact: `sedan.obj` is **(1.50, 1.30, 2.55)** on disk, and the placed sedans
measured **(1.47, 1.28, 2.51)** in the world. Identical — which can only happen if no
conversion survived. 760 cars stood on their tails, 1,855 people lay on their backs, and every
sign, light, tree and scaffold board lay flat on the ground.

The fix is one line on the **data** API, which takes no context and cannot no-op:

```python
ob.data.transform(Matrix.Rotation(math.pi / 2.0, 4, "X"))
```

Every transform in that loader is a data call now, for the same reason.

| | before | after |
|---|---|---|
| people, median height | **0.52 m** | **1.75 m** |
| cars standing on end | **760 of 760** | **0 of 760** |
| cars, median length | 1.47 m | **4.91 m** |

### 7.2 Why the verification missed it

Because it measured **position and facing** — never **uprightness**. That is EVENTER rule 1
for the fourth time on this map: *measure the property, not a proxy.* A car can be in its
lane, pointed down its lane, and vertical.

The check that now exists reads the world-space Z extent of **every** instance and, per rule 4,
is fed the pre-fix numbers to confirm it rejects them.

It caught one of my own faults immediately: it flagged 112 objects as "not upright" that were
**road crossings**, which are painted on the carriageway and *supposed* to be flat. The band
was the proxy, not the geometry. Crossings are now tested for flatness and everything else for
uprightness.

### 7.3 The grey was mine too

Every vehicle material was `colormap.NNN` at base colour **(0.439, 0.417, 0.366)** — one flat
beige-grey across 2,615 objects. That was `fix_missing_textures()`, which unlinked any image
node whose image reported `has_data == False` and painted the socket a flat colour.

**The textures were never missing.** 95 of them sit on disk across 37 kits, and every `.mtl`
references them correctly. `has_data` is simply *lazy*: Blender does not load an image buffer
until something samples it, so a perfectly good 512×512 PNG reads `False`. The fallback fired
on every healthy texture in the city.

Two fixes:

- **Resolve, don't paint over.** Match each image through **the kit that owns the model using
  it** — never by filename. Eleven kits ship a file called `colormap.png`, and a naive
  basename match sent all 760 cars to *brick-kit*'s atlas. A kit texture only means anything
  against the UVs of its own kit.
- **`size`, not `has_data`.** `size` is read from the file header the moment the path resolves
  and stays `(0, 0)` only when the file genuinely is absent — which is the thing being tested.

Result: 26 images resolved to the correct kit, 2 genuinely missing (`bars.png`, `metal.png` —
that kit ships without them), and the fallback now touches **6 materials instead of 82**.

### 7.4 Traffic signs

XT_FURN already held 53 traffic lights and 60 highway signs. They were invisible for two
reasons, both real: they were grey, and `build_furniture()` gives every item
`rnd.rng(0, 2π)` — a **random yaw**. A traffic light pointing diagonally across a pavement is
not a traffic light, it is a grey post.

Signage is the one class of street object whose orientation *is* its meaning, so none of it is
placed at random:

| | count | placement |
|---|---|---|
| signals | **184** | four per avenue junction, two per quiet crossroads, facing back across it |
| signs | **444** | on the kerb, facing the carriageway they speak to |
| lamps | **205** | behind the sign line |
| crossings | **112** | on each approach to every avenue junction |

Only complete, post-mounted models are used. Kenney's `-object-` variants are the sign *panel*
alone, meant to be parented onto a post: placed as street furniture they measured
**(0.66, 3.00, 0.94)** — a three-metre board hovering at knee height. Measured, then cut.

A related trap found while measuring: `load_model()` caches by **name** and ignores the target
size on any later call, so `sign-highway`, already loaded by `build_furniture` at 1.4 m,
silently ignored this stage's request for 3.0 m. **Model size depends on which stage asks
first.**

### 7.5 Construction that reads as construction

The other half of "grey elements I don't understand". The leanest towers carry **288 faces**
against 33,011 for a finished one. That is not a bug — a site at `prog 0.09` legitimately has
two slabs and a core — but two grey slabs seen from 900 m up are a grey plate, and 51
buildings looked like that.

What tells you a site is a site, from the air, is not the frame:

- **Hoarding** — 51 painted rectangles drawn hard on the plot line, in four liveries. This is
  the single clearest aerial signal of a building site.
- **Digs** — 8 early sites are a hole, not a plate.
- **Rebar** — **990 starter bars** standing out of the last pour across 42 frames. A tower
  going up ends in a flat grey slab, and from 900 m a flat grey slab is indistinguishable
  from a finished roof — which is precisely what made those buildings unreadable. Bars
  waiting for the next lift are the cheapest true signal on a site and the only one visible
  from *directly above*, which is where this camera is.
- **Formwork** — 42 stacks of panels on the slabs: flat, bright, and unmistakably *material*
  rather than building.
- **Sheeting** — 26 coloured bands on the top floors, the only saturated colour on a real site.

The first cut of this computed the top of the pour *inside* the sheeting branch, so a site too
short to wrap got no rebar and no formwork either — and the short ones are exactly the stumps
that read worst. The top is found once now, and decorated after.

The first sheeting attempt was **13 m tall and cut to the plot's design width**, and it read as
a solid coloured box wrapped round the building — another unexplained element, not a fix for
one. It is now **5.5 m** and sized off **the tower's own mesh at that height** (median width
20.7 m against 46.7 m before), because a tower that sets back or tapers is narrower up there
and a band cut to the plan's width stands off it in mid-air.

### 7.6 Two more things worth having

**Podium roofscape.** A podium roof is the biggest flat surface in the city: it fills the plot,
it is low, and nothing occludes it from a camera 55° up. 114 of them were capped in pale glass
and read as 114 blank plates. Towers have had a roofscape since the first finish pass; the
podiums, far more visible from above, never did.

**Crane livery.** 41 cranes in one saturated yellow is a yellow forest. Real fleets are hired
from several firms and painted accordingly — six liveries now. The **count is unchanged**:
crane density is the XTIX story and Oran never asked me to thin it.

### 7.7 A build script, at last

There wasn't one. The city was built by calling each stage by hand across a long session,
which is exactly why a fault in `load_model()` survived a full verification pass: every stage
was checked, the **order** never was. `xtix_build.py` now runs all thirteen stages, logs each,
and drops stale `XL_*` prototypes first — because `load_model()` returns any existing
prototype, so the axis fix would otherwise never have reached the city.

| | |
|---|---|
| full rebuild | **2.3 minutes**, 6,360 renderable objects |
| people upright | **1,855 of 1,855** |
| vehicles flat on their wheels | **760 of 760** |
| signage added | **945** |
| construction elements added | **127** — 51 hoardings, 26 sheeting bands, 42 formwork stacks, 8 digs |
| rebar bars | **990** across 42 frames |
| build verification | **11 of 11 pass** |

---

## 8. Fourth pass — vehicles, people, cranes, landscape, buildings

Oran asked for a significant round on all five, worked slowly and self-checked, with deep
analysis behind every change. So this pass began by **measuring the built scene**, not by
editing it — and the first thing the measurements caught was me.

### 8.1 Two faults that were mine, not the city's

The first vehicle analysis reported a **median heading error of exactly 90°** on 734 of 760
cars, and **226 cars more than 0.6 m off a lane centreline**. Both were wrong:

- **90° is the convention.** After the Y-up conversion a model's front is its local **−Y**,
  so yaw 0 faces −Y, not +X. I had compared raw yaw against `atan2(dy, dx)`. The shipped
  verifier already does this honestly — it rotates `(0,−1,0)` by `matrix_world` and compares
  against the `head` tag written at placement — and it passes 760 of 760.
- **The 226 were the parked cars**, which belong at the kerb and not in a lane at all.

Measured against a proxy, a correct city looks broken. Both checks were rewritten before
anything was changed.

### 8.2 Vehicles — 157 real intersections

With the measurement honest, one fault survived: **157 intersecting pairs**. The worst was a
moving garbage truck and a *parked* sports car with centres **0.92 m apart**, both around 5–6 m
long. Two causes, both structural:

```python
t = rnd.rng(2.0, l["len"] - 2.0)        # uniform random position, no spacing check
off = 1.55 * (1.0 if rnd.f() < 0.5 else -1.0)   # parking offset, direction by coin toss
```

A lane is 3.5 m and these models are 1.9–2.95 m wide, so a car parked 1.55 m off a lane centre
sits **half inside the neighbouring live lane** — and the coin toss put half of them leaning
into moving traffic. On a 7 m street there is simply no room to park at all.

Rewritten so overlap is impossible by construction:

- **Parking is a lane, not an offset.** An avenue is 14 m and carries four lanes: the outer
  one each side becomes kerbside parking, two stay running. A 7 m street carries two lanes,
  one each way, and gets **no parking** — which is also how a dense core actually works.
  Lane centres are 3.5 m apart and the widest model is 2.95 m, so adjacent lanes cannot touch.
- **Positions are walked, not drawn.** A headway of 3.5–22 m for moving traffic, 0.9–4.5 m for
  parked. Walking also gives traffic the platoon-and-gap look a random scatter never has.
- **Junction boxes are kept clear**, which removes the crossing case entirely.

| | before | after |
|---|---|---|
| intersecting pairs | **157** | **0** |
| moving cars off lane centre | up to 1.55 m | **0.00 m**, max |
| heading error | — | **0.00°**, max |
| vehicles | 760 | **1,050** |

### 8.3 People — 1,855 to 3,920, and in groups

The old placement drew a uniform `t` along each pavement strip. That measured **31 % of the
city's 20 m cells completely empty** while others held fourteen: the signature of a Poisson
scatter, and why the streets read as sprinkled rather than busy.

Real pavements are the opposite — mostly small groups, with hard concentrations where people
are made to stop. So the builder now places **events, not individuals**: a lone walker, or a
knot of two to five; then deliberate crowds at the **junction corners** where a city queues to
cross, and in the **plaza and park** — two zones the plan has always listed and the builder
had never filled.

Nothing may intersect anything else; a 1 m spatial hash makes that exact rather than
approximate, and cheap enough to run on all 3,920.

| | before | after |
|---|---|---|
| people | 1,855 | **3,920** |
| median per 20 m cell | 3 | **7** |
| at crossings / in open space | 0 / 0 | **543 / 328** |
| intersecting pairs | — | **0** |

The density constant lives in `xtix_plan.PAVE_M_PER_PERSON` (9.3 → **4.4 m per person**), not
in the builder. An earlier cut raised the count with `max(plan, 760)` inside `build_traffic`,
which is exactly the fault this map keeps re-learning: the builder and the verifier then read
different numbers and the count check fails for the right reason.

### 8.4 Cranes — the crown and the core were never counted

All 41 measured **perfectly vertical, all on the ground**. But against each crane's **own**
building rather than its nearest, three were wrong:

| | clearance | |
|---|---|---|
| `XC_2_0_0` | **−0.6 m** | mast ended *below* a 241.4 m tower |
| `XC_3_5_0` | **+1.6 m** | no room to lift anything |
| `XC_4_1_3` | **+69.8 m** | towering over what it was building |

The first two came from sizing off `built_h`, which is the **structure only**. What actually
stands on a plot is taller:

- a finished tower carries a **crown** — 11.5 % of the shaft, capped at 30 m;
- one under way carries the **slip-formed core**, `CORE_LEAD = 4` floors of 3.7 m = **14.8 m**
  above the top slab.

Sizing off the slab alone left sixteen cranes between 3.2 and 7.9 m clear — 14.8 m short,
which is exactly the core lead. The third came from the loop that raises a mast until its jib
clears the tallest neighbour it can reach: with no cap, one tall neighbour drags a crane into
the sky. It now shortens the **jib** instead, so the neighbour falls out of slew — and when the
jib is already at its 24 m floor and the obstacle is 19.8 m away, the cap yields, because a jib
through a building is a fault and a tall crane is only a preference.

One more of the same family: `build_cranes` chose a plot corner from **its own RNG** while the
plan measured reach from the plot **centre**, 27 m away — so a crane could reach a neighbour
the plan had ruled out of range, and the verifier duly caught it. The plan chooses the position
now, and the builder is told where to stand.

| | before | after |
|---|---|---|
| clearance over own building | **−0.6 → 69.8 m** | **18.8 → 81.1 m** |
| under 8 m clearance | 2 (and 16 after the first fix) | **0** |
| jibs fouling a building | 0 → 1 (introduced) | **0** |
| tilt / off the ground | 0 / 0 | **0 / 0** |

### 8.5 The landscape — "it looks just thrown"

He was right, and the code said so before the render did:

```python
step = (4.0 * CITY) / per                       # 196 trees over 2,160 m
inst.location = (x + rnd.rng(-2.5, 2.5), y + rnd.rng(-2.5, 2.5), 0.0)
```

A `while` loop walking the perimeter at a fixed step, dropping **one tree per step**. Measured
on the built scene: nearest neighbour **6.3 / 9.4 / 13.2 m**, every tree between 4.9 and 9.8 m
tall, **no understory whatever**. A line of equally spaced dots is the one arrangement that
cannot read as landscape.

**The kit was never the limit.** `nature-kit` holds ~54 tree variants (18 were in use), six
bushes, nine flowers, four grasses, about forty rocks, seven stumps, logs and pots; there are
hedges in `fantasy-town-kit` and planters in `city-kit-suburban`. None of the understory had
ever been loaded.

What replaced it — `xtix_land.py`, which now owns everything outside the city square:

- **Groves.** 728 clumps, rejection-sampled so they are dense against the kerb and thin
  outward (`exp(−d/62 m)`), each a mix of canopy, mid-storey, conifer and autumn, **sized per
  tree** — a stand where every tree is the same height is a hedge.
- **Understory.** Shrubs massed at the skirt of each grove, ground cover between, rocks and
  fallen logs occasionally.
- **Meadow** in the gaps, so they are not bare lawn.
- Every plant tested against a spatial hash, so nothing grows through anything else.

| | before | after |
|---|---|---|
| plants outside the city | **196** | **11,299** |
| species | 18 | **91** |
| groves | 0 | **728** |
| shrubs / ground cover | 0 / 0 | **≈4,900 / ≈2,900** |

### 8.6 The colour of leaves, and two broken models

Measured, and the single reason the woodland still read as one thing: **nature-kit does not
texture its plants at all.** Every model carries flat named materials, and the whole kit has
exactly three foliage colours — `leafsGreen` (0.161, 0.788, 0.671), `leafsDark`, and
`leafsFall` — shared by all ~54 trees, six bushes and four grasses. So 91 species of different
**shape** were painted the same two greens: shape variety with no colour variety still reads as
uniform, which is the fault the tower palette had before the gloss pass.

Eight tints now spread the canopy across the range a real one covers — new growth, shade,
olive, deep forest — while keeping the kit's teal as the most common, so the family still
reads. Assigned per **object**, so one mesh wears several colours across the map. 11,652 slots.

Two kit models are **broken**, and a scan by surface area found them:

- `tree_default_fall` and `tree_blocks_fall` are **100 % `woodBirch`** (1.00, 0.95, 0.87) —
  canopy included. Their `.mtl` assigns the trunk material to every face, so they render as
  cream-white lollipops standing in the woodland. Not a colour to fix; a model to not use.
- 380 stray `_defaultMat` slots — two faces per tree the kit never assigns, pure white.
  White is the one colour a tree cannot be.

The same scan flagged the hedges as pure white, and that one was **my proxy again**: their
`.mtl` is `Kd 1 1 1` plus `map_Kd`, which is simply how a textured material looks. The texture
resolves and links; the hedges are green.

### 8.7 Buildings — connecting them

Oran asked to be creative here, and earlier set the direction: not Dubai, not New York, not
Tokyo — *more futuristic, more innovative, very sophisticated*.

**Sky bridges.** A skyline of separate towers is every skyline. What reads as a *planned*
future city, instantly and at any distance, is towers that are **connected**. It is the one
move that changes the silhouette rather than the surface, and this camera looks at the
silhouette. **14 bridges**, spans 7.1–23.0 m, at heights 42–95 m.

They are kept rare deliberately — a bridge on every pair would be a lattice and would read as
a mistake; a dozen reads as a decision. One per tower, finished towers only (you do not connect
to a building still going up), and the span is measured off both towers' **actual cross-sections
at the bridge height**, never the plan's nominal width, because a tower that sets back is not
that width by the time it is up there. A first cut put one bridge **through a third tower**;
they now refuse any span that crosses a building they do not connect.

**Roof gardens.** These hit a real geometric limit, and the measurement is worth recording: a
62 × 31 plot carrying a 56 × 25 tower leaves a **2.2 m ring**, and across all 114 podiums the
median best margin is **−2.5 m**. The tower fills its own podium. Only 23 can hold anything,
and 16 got one. A walkway is not a terrace, so the effort moved to where the ground actually
is: **19 courtyards, the plaza and the park**, now hedged and planted — 747 plants. MEDCOIN's
audit said it first: a courtyard with nothing in it is dead ground wearing a nicer name.

### 8.8 State

| | |
|---|---|
| renderable objects | **21,146** |
| vehicles · clashes | 1,050 · **0** |
| people · intersections | 3,920 · **0** |
| cranes · under-clearance · tilt | 41 · **0** · **0** |
| plants (landscape · gardens · roofs · street) | 11,299 · 747 · 470 · 328 |
| sky bridges | 14 |
| build verification | **11 of 11 pass** |
| full rebuild | 8.8 min |

One performance fault found and fixed along the way: `drop_prototypes()` removed 20,351
objects **one at a time** and took six minutes, because each call re-resolves every user of the
datablock. `bpy.data.batch_remove()` does the set in one pass.
