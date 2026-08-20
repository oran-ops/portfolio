# PAGE 4 — THE RING. Owner's spec, 2026-08-19. Build to this, not around it.

## The concept
An old all-in-one computer sits to the RIGHT. Four floppy disks lie scattered to its LEFT,
as if someone pulled them out and tossed them down beside it.

## The computer
- EXACTLY the machine in the reference image, one to one: same cream/beige body colour, same
  shadow, same form, same vents/slots, same panel lines, same proportions, same camera angle
  and position as the photograph.
- Screen: black, the SAME value as the page background.
- On the screen: "Oran Carmon — Master File" plus an old white matte folder icon, drawn the
  way an old computer would draw it.

## The floppy disks — four, one per case file
- EXACTLY the disks in the reference images, one to one.
- Body colour: the SAME cream as the computer, so they stand out against the charcoal ground.
- Each carries a STICKY NOTE, one per project colour: XTIX, OASIS, EVENTER, MEDCOIN.
- Sticky-note behaviour: adhered at the TOP, lifting free at the BOTTOM.
- On each note, the project name in HANDWRITING — a real, legible, modern hand. Not an
  antique bookhand. "As if I wrote it myself."
- Arrangement: lying at angles, genuinely untidy - one disk's corner resting on another,
  overlapping, arbitrary. Not a neat fan, not a grid.

## Ground and light
- Background: matte charcoal, same as the rest of the document, lifted very slightly with
  grey. Everything matte.
- Lighting: general, natural, NO lamp fixture. It should feel like arriving at a naturally
  lit area, with the light handled as a web effect rather than a modelled lamp.

## Placement and reading order
- The computer sits to the RIGHT of the disks. Scrolling into page 4, the reader meets the
  SCATTERED DISKS FIRST and the computer is revealed after, because it is further right.
- Position within the document: keep the existing distances exactly as they are today, so the
  scroll arrival point of page 4 does not move.

## Separate, now DONE
The statement spheres on page 2 were rebuilt from vanlent.dev's own bundle and are live in
`/m/`. See `docs/ORB_SPEC.md`.

---

# TECHNICAL FINDINGS — how the two reference effects are actually built

## vanlent.dev — the point sphere (page 2 reference)
- Three.js, ONE WebGL canvas, and **no model files at all** — no glTF, no .bin, no textures.
  The sphere is generated in code, so it can be reproduced legitimately in full.
- NOT yet extracted: point count, point size, colour, camera distance, rotation speed. A
  `fixed inset-0 z-[9999]` overlay intercepts elementFromPoint and the react-three-fiber store
  was not reachable from the canvas. Next attempt: hook the WebGL context and read the draw
  calls, or find the r3f root from another element.

## pxpush.com — the computer and floppy (page 4 reference)
- Three.js, three WebGL canvases.
- The floppy is a real glTF model:
    /img/home/floppy_disk/scene.gltf
    /img/home/floppy_disk/scene.bin
    /img/home/floppy_disk/textures/material_0_diffuse.png
    /img/home/floppy_disk/textures/material_0_specularGlossiness.png
    /img/home/floppy_disk/textures/material_0_normal.png
- The `material_0_*` / specularGlossiness naming is a Sketchfab export signature, so the model
  is licensed from a third party — not PX Push's own work.
- Also present: /img/crt.png, /img/noise.png, /img/home/pxpush.mp4, /img/cursor.obj

## Why SVG cannot reach this
The floppy's look comes from a NORMAL map (the moulded surface texture) and a
SPECULAR-GLOSSINESS map (the plastic sheen). Neither exists in SVG. Any flat-vector attempt is
drawing a picture of a rendered object and will always miss.

## Models the owner selected (Sketchfab)
- Apple Macintosh 128K:
  https://sketchfab.com/3d-models/apple-macintosh-128k-1dc6a0b8b0b444a4b5b52e9877769664
- Floppy disk:
  https://sketchfab.com/3d-models/floppy-disk-4b6d5a8b45aa4beeb9fed31d45d1d153

## Architectural consequence — DECIDED 2026-08-20: build, do not load

site_mobile.html is ONE self-contained file: zero external requests, everything base64
inlined, no build step. A glTF model plus three textures plus a renderer breaks that premise —
either the site starts making external requests, or the file grows by the asset size plus 33%
for base64. Measured earlier: a hand-rolled WebGL scene with 5 lit objects is ~5KB
unminified; three.js is 357KB minified and is the wrong tool here.

**The models are not used.** Four reasons, in order of weight:

1. Zero external requests is the page's premise, not a preference.
2. glTF + three textures + a loader is north of a megabyte after base64, on a page that is
   686KB in total. three.js alone is 357KB to draw a handful of boxes.
3. A Macintosh 128K is a stepped profile extruded across a width. It is a few hundred lines.
4. Building it raises no licensing question at all.

The owner also offered the Sketchfab **embed**. That is an iframe to sketchfab.com — external
requests on every load plus their branding and attribution on the page — so it cannot ship
either. It is excellent as a *reference*, and orbiting it is where the profile below came from.

If the owner still wants the licensed model, swapping it in is a change of geometry source,
not a rebuild: the renderer, the light and the panel shader all stay.

## What the reference actually looks like — read by orbiting it

The first attempt modelled the machine as a rounded box and it read as a fridge. Orbiting the
reference to a side view shows the silhouette is a **stepped profile**, and that is the whole
character of the object:

- the top runs back on a gentle slope, then breaks into a steeper rear shoulder
- the back stands about **83%** of the front's height
- under the front face the body steps **back** before it reaches the floor, so the face
  overhangs its own base
- the vents are low on the flanks, not high, and there is a second pair on the top rear
  flanking a recessed carry handle

Profile as built, in (z, y), z forward, from the top front corner clockwise:

```
( 0.560,  0.675)   top front
(-0.100,  0.585)   the gentle run back across the top
(-0.560,  0.395)   rear shoulder, steeper
(-0.560, -0.675)   rear bottom
( 0.500, -0.675)   base, front bottom
( 0.500, -0.330)   base front, top of it
( 0.560, -0.250)   the overhang: the face steps out over the base
```

## THE MACHINE, BUILD 3 — the work plan that replaces guessing

Builds 1 and 2 were one extruded profile with the whole front painted into the fragment
shader. That is why it is not one to one and no amount of shader polish would have got it
there: on the reference the front is an ASSEMBLY, and its parting lines, pocket walls and
draft angles are geometry. A line painted where a seam should be reads as a line, not a seam.

The reader will also be able to orbit the finished scene, which removes the last excuse: a
detail that only works from one angle is not allowed anywhere in this model.

### Dimensions — from the product, not from a pixel ruler

Perspective screenshots are a bad ruler; two readings off the same view disagreed by 30% on
the screen's aspect. The Macintosh 128K is a documented product, so the frame is:

```
case            9.7 W x 13.5 H x 11.2 D inches      ->  0.97 x 1.35 x 1.12   (1 unit = 10 in)
CRT active      512 x 342 px at 72 dpi              ->  7.11 x 4.75 in, aspect 1.50
floppy slot     ~3.6 in wide
```

The reference supplies what the spec sheet cannot: the part breakdown, where the parting lines
run, how deep the pockets are, and the finish.

### Parts

| # | part | how it is built |
| --- | --- | --- |
| 1 | case shell | profile extrusion, front plane set back to z = 0.500 to leave room for the bezel |
| 2 | front bezel | rounded-rect FRAME extruded in z, 0.060 thick, with a real opening for the screen |
| 3 | screen well | the frame's inner wall, drafted, plus a back plate |
| 4 | tube surround | dark moulding inside the well |
| 5 | glass | 1.50 aspect, the page's own charcoal |
| 6 | disk pocket | a second, shallower frame on the bezel face, with its own back plate |
| 7 | base plinth | rounded box under the bezel, set back — the overhang becomes real |
| 8 | rear | handle recess, two vent grids, port row |

### The one new primitive

`frameXY(outer, inner, z0, z1, draft)` — a rounded-rectangular frame extruded along z with a
drafted inner wall. Both outlines are sampled by casting a ray from the centre and bisecting on
the rounded-rect distance field, which matches outer and inner sample for sample and needs no
special case at the corners. Everything else is built from the two primitives already written:
the rounded box and the rounded profile extrusion.

### What stays in the shader, and why

The logo, the vent slits and the mould texture. All three are surface markings with no depth
worth modelling — the vents get a normal perturbation so they still catch light as grooves.
Everything with a WALL is geometry now.

## Build order agreed with the owner
1. The machine, alone, until it matches the photograph  — **first pass done, `lab/machine.html`**
2. One floppy, alone — body, texture, sheen
3. The sticky note — adhered at top, lifting at bottom, handwritten name
4. Four floppies scattered, genuinely untidy
5. The screen content — "Oran Carmon — Master File" and a white matte folder icon
6. Light and ground
7. Placement: computer to the RIGHT, disks met first on scroll; existing scroll distances kept

## Still missing
No handwriting typeface is embedded in the document. One must be chosen, licensed and
inlined before the sticky notes can be built.
