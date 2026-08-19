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

## Separate, still outstanding
The statement spheres on page 2 must match vanlent.dev EXACTLY - same size, motion, density,
colours, shading. Current build is not close enough.

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

## Architectural consequence, decide before building
site_mobile.html is ONE self-contained file: zero external requests, everything base64
inlined, no build step. A glTF model plus three textures plus a renderer breaks that premise —
either the site starts making external requests, or the file grows by the asset size plus 33%
for base64. Measured earlier: a hand-rolled WebGL scene with 5 lit objects is ~5KB
unminified; three.js is 357KB minified and is the wrong tool here.

## Build order agreed with the owner
1. The machine, alone, until it matches the photograph
2. One floppy, alone — body, texture, sheen
3. The sticky note — adhered at top, lifting at bottom, handwritten name
4. Four floppies scattered, genuinely untidy
5. The screen content — "Oran Carmon — Master File" and a white matte folder icon
6. Light and ground
7. Placement: computer to the RIGHT, disks met first on scroll; existing scroll distances kept

## Still missing
No handwriting typeface is embedded in the document. One must be chosen, licensed and
inlined before the sticky notes can be built.
