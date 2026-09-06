# The machine, measured from a mesh

Every number in this file was read off a 3D mesh of a compact Macintosh, not off a photograph.
That distinction is the whole point. A photograph gives you a projection and you recover shape
by fitting a homography and hoping; a mesh gives you the coordinates.

**Units.** The file is modelled at **1 Blender unit = 1 inch**. That was not stated anywhere in
the file — it was established by measuring the case and comparing against the real machine:

| | measured | Macintosh 128K, published | error |
|---|---|---|---|
| height | 13.341 in (case top 13.562) | 13.5 in | −1.2 % |
| width | 9.530 in | 9.7 in | −1.8 % |
| depth | 10.830 in (at the brow) | 10.9 in | −0.6 % |

Three independent dimensions agreeing to within 2 % of a machine the file knew nothing about
is what makes the unit scale a finding rather than an assumption.

**Axes.** +X to the viewer's right, **−Y is the front**, +Z up. The origin is the file's, not
the case's; the case centre sits at x +0.042, y −0.634, z +6.891.

---

## 1. The case

The shape that three hand-tuned builds never found. It is not a box.

```
front face      raked   y = −6.4069 + 0.11858·z        6.76° from vertical
roof            sloped  z = 13.0580 − 0.11217·y        6.40° falling to the rear
```

Both are straight to **five thousandths of an inch** over their whole run (max residual
0.0051 in and 0.0058 in respectively), so they are genuinely planes, not curves.

| feature | value |
|---|---|
| width | 9.530 in, constant from z = 1.0 to 13.3 — no taper |
| height | z 0.221 … 13.562 |
| chin, front face | y = −4.736, from z = 0.22 to 2.10 |
| brow | sweeps forward from z 2.10 to 3.00, reaching the front-most point y = −6.056 |
| raked face | z 3.00 … 12.80 |
| rear wall | y = +4.774, from z = 0.22 to 10.80 |
| rear chamfer | (y +4.774, z 10.80) → (y +3.894, z 12.60), 26.1° from vertical |
| depth at the chin | 9.510 in |
| depth at the brow | 10.830 in — the deepest section |
| front outline, top corner radius | 0.215 in (max deviation 0.0035 in) |
| front outline, bottom corner radius | 0.168 in (deviation 0.0034 in) |

The brow is the detail that gives the machine its face: between z = 2.1 and z = 3.0 the front
surface pushes forward 1.32 in, then leans back again for the remaining ten inches. A flat
front cannot produce that, and no adjustment of a flat front gets closer to it.

## 2. The screen

The visible screen is the **opening**, not the glass — the glass is larger than the hole and
the bezel crops it.

| feature | value |
|---|---|
| opening | 7.610 W × 5.800 H in |
| opening, x | −3.768 … +3.842 |
| opening, z | 6.42 … 12.22 |
| opening centre | x +0.037, z +9.350 |
| **relative to the case centre** | **x −0.004 in, z +2.459 in** |
| opening edge chamfer | 0.154 in deep |
| opening corner radius | 0.258 in at the bottom; the top corners are a longer, gentler sweep |
| CRT glass | 7.698 × 6.049 in, centre x +0.071, z +9.290 |
| glass bulge (sag) | 1.027 in, implying a face radius of ≈ 12.2 in |
| glass pole | y = −5.641, which is **0.336 in proud** of the surrounding face plane |

The screen is **centred**: 0.004 in off the case's centreline. Earlier work had it 0.53 in to
the right, which came from a homography fitted to a single photograph.

## 3. Fittings on the front face

| feature | size | centre (x, z) | relative to case centre |
|---|---|---|---|
| floppy slot assembly | 4.320 × 0.990 in | +1.732, +4.286 | +1.690, −2.605 |
| Apple logo recess | 0.600 × 0.600 in | −3.598, +3.761 | −3.640, −3.130 |

## 4. Fittings elsewhere

| feature | size (X × Y × Z) | centre |
|---|---|---|
| carry handle recess | 4.111 × 1.291 × 0.641 | +0.069, +0.296, +12.526 |
| roof vent grilles (pair) | 1.741 × 7.748 × 0.914 each | x ±3.31, z 13.058 |
| upper rear vents (pair) | 2.054 × 0.605 × 1.185 each | x ±3.23, y +4.298, z 11.776 |

## 5. Keyboard

| feature | value |
|---|---|
| case | 14.139 W × 5.870 D × 1.996 H in |
| centre | x −0.619, y −10.660, z +1.021 |
| position | 1.668 in in front of the case, 0.661 in left of its centreline |
| top slope | 9.72° rising to the rear (case silhouette, residual 0.138 in) |
| keycap-top plane | 11.62° (residual 0.046 in) |
| 1u keycap | 0.763 W × 0.760 D × 0.714 H |
| key pitch | 0.783 – 0.788 in |
| rows, front to back | 4, 12, 13, 14, 14 keys |

The two slope figures differ because the case silhouette includes the raised rear lip while the
keycap fit does not. The keycap plane is the better one to build to: its residual is a third of
the other's.

## 6. Mouse

| feature | value |
|---|---|
| body | 2.875 W × 3.865 D × 1.248 H in |
| button | 1.392 × 1.395 × 0.709 in |

## 7. Where the mesh disagrees with the real machine

The case is faithful to within 2 %. The peripherals are not, and this matters because the brief
was to match a real Apple Macintosh of the same model:

| | mesh | real | difference |
|---|---|---|---|
| keyboard width | 14.139 in | 13.2 in (M0110) | **+7.1 %** |
| mouse width | 2.875 in | 2.24 in (M0100) | **+28 %** |
| mouse height | 1.248 in | 1.38 in | −9.6 % |

So: **build the case to the mesh, and the keyboard and mouse to the real dimensions.** The mesh
is the better authority on the case's shape, which no catalogue records; the catalogue is the
better authority on the peripherals' size, which the artist evidently approximated.

## 8. What this corrected

The model as it stood before this measurement, in the same units:

| parameter | was | measured | error |
|---|---|---|---|
| front face | flat | raked 6.76° | structural |
| roof | flat | sloped 6.40° | structural |
| chin / brow | absent | 1.32 in forward step | structural |
| case width | 9.70 | 9.530 | +1.8 % |
| case height | 12.875 | 13.341 | −3.5 % |
| case depth | 10.10 | 10.830 | −6.7 % |
| visible screen | 7.11 × 4.75 | 7.610 × 5.800 | −6.6 %, **−18.1 %** |
| screen offset in x | +0.531 in | −0.004 in | it is centred |
| well opening | 8.47 × 6.40 | 7.610 × 5.800 | +11.3 %, +10.3 % |
| corner radius | 0.32 | 0.215 top, 0.168 bottom | — |
| logo position | −4.007, −3.654 | −3.640, −3.130 | 0.37 in, 0.52 in |
| keyboard tilt | 7.37° | 11.62° | −37 % |

The three structural rows are why the earlier builds read as wrong at a glance while every
individual dimension looked defensible. The silhouette was a flat-fronted, flat-topped box; the
machine is a raked, sloped, brow-fronted one.

---

## Provenance and licence

The mesh is a **CC0 / public-domain** asset by `richardsmid` on CGTrader, confirmed on its
download page. CC0 places no restriction on redistribution or embedding, so the geometry is
shipped in the page rather than only measured from.

An earlier draft of this file said the opposite. That was written from CGTrader's general
Royalty Free terms, which do require that a model in a software product be kept out of the end
user's reach - correct for their default licence and wrong for this model, which carries a
different one. Price and licence are separate facts and so are default terms and actual terms.

What ships is not the file. A `.blend` is Blender's memory image and no browser can read one,
so the mesh is converted to a small binary blob:

| | |
|---|---|
| triangles | 55,725 of the file's 56,895 (the desk mat is dropped) |
| vertices | 30,441 in the file, 47,738 after splitting at creases |
| positions | 16-bit fixed point over each group's own box - 0.00015 in per step |
| normals | octahedral, 8 bits per component - 0.29 deg mean error, 0.93 worst |
| binary | 700 KB |
| base64 | 933 KB |
| **over the wire** | **505 KB gzipped** |

The two textures the file references are absent from it - its paths point at the author's own
downloads folder - so nothing was lost by not having them. The screen carries our own content
and the front badge is drawn in the shader, the mesh having only a recess for it.

Sizes are corrected **per object**, because one factor fits none of the three:

| | mesh | published | applied |
|---|---|---|---|
| case | 9.53 x 13.34 x 10.85 in | 246 x 344 x 276 mm | +1.7% / +1.5% / +0.2% |
| keyboard | 14.14 in wide | 336 mm (M0110) | -6.4% |
| mouse | 2.88 x 1.25 in | 62 x 37 mm (M0100) | -15.3% / +16.8% |

The keyboard and mouse keep their measured HEIGHT. Apple's 65 mm for the M0110 is a
max-rear-height on a wedge case and single-sourced; forcing it would stretch the keycaps by a
quarter to satisfy a figure the object itself contradicts.

The procedural build remains at `?geo=proc` - 23,506 triangles against the mesh's 61,081 - and
is the automatic fallback if the blob ever fails to decode. A page that renders a good
approximation beats a page that renders an empty room.

## The tools

In `tools/blend/`. They read a `.blend` directly — no Blender installation involved — because
the format carries its own struct definitions in its `DNA1` block.

| file | what it does |
|---|---|
| `blendread.py` | the `.blend` parser: header, blocks, DNA, field access by name |
| `meshlib.py` | mesh extraction, connected-island splitting, and the rasteriser |
| `render.py` | labelled orthographic views, coloured by island or by material |
| `profile.py` | silhouettes and the front-facing depth map |
| `spec2.py` | the parameter table: rake, slope, chin, widths |
| `well.py` | the screen opening, row by row |
| `corners.py` | corner radii |

### Three instrument failures worth remembering

1. **Sampling vertices in a thin slab.** The flat panels of this mesh are a few large
   triangles, so a slab drawn between two rows of corners contains no vertices and reports a
   face that is not there. It produced a 22.74° rake with a **9.8 in residual** — a fit bad
   enough to announce its own failure — and a chin table claiming the case was 0.309 in wide.
   Rasterise the triangles; ask the surface, not the vertex buffer.
2. **A test bounded at one end.** `depth > face + 0.06` also catches every pixel that sees
   straight through the screen opening to the inside of the rear panel ten inches away, so the
   screen well came back 9.63 in wide and 9.94 in deep — the whole machine. The same
   one-sided-test bug had already cost two shader debugging sessions on this project.
3. **A circle fitted through a straight line.** Both corner radii were first fitted over
   windows that were mostly straight edge, returning 1.293 in and 1.779 in with fat residuals.
   Isolate the corner — the part that departs from both straight edges — then fit. The real
   answers are 0.215 in and 0.258 in, with deviations of three thousandths.

Each was caught by the residual, not by looking at the output. A fit that does not report how
badly it fits is not a measurement.
