# The statement orb — what vanlent.dev actually does

Every earlier attempt at this element was a guess at the picture. This document is not a guess.
Everything below was read out of vanlent.dev's own JavaScript bundle, and the reading was then
checked against a screenshot of the running site.

## How the parameters were obtained

The site is a Next.js app; the hero orb is drawn by react-three-fiber into a single WebGL2
canvas. Downloading the 34 chunks it references and searching them turned up three things:

| what | where |
| --- | --- |
| nine named presets, as JSON | `chunks/701431d012697037.js` |
| the two GLSL programs, as plain string literals | module 88099 in `chunks/174a6db326ee0789.js` |
| the shape generators and shell layout | `chunks/33572b3640db9e04.js` |
| the camera and the render loop | `chunks/6e7b677a3709fdcf.js` |

The hero morph path is `[HERO_PATH_PRESETS.bubbly, base_prsrv, fillaments]`, so the state the
page opens on — the one worth copying — is the preset named **`bubbly`**.

## The recipe

```
shape            "sphere"        a plain Fibonacci sphere, then shuffled
particleCount    33000
wobble           1               radial displacement, amplitude wobble / 6
wobbleType       0               ORGANIC
curl             0               no curl in this state
lockShell        0
rotationSpeed    0.3             rad/s about Y: rotation.y += delta * speed
animationSpeed   1               uTime is the clock in plain seconds
scale            1
additive         false
softSprites      false           hard square points, not sprites
dark flowColor   0.85 0.88 0.92
camera           position [0, 0, 8], fov 50, dpr [1, 2]
```

`bubbly` also carries a `shells` array. It is dead weight — shells are only read when the shape
is `nestedSpheres2`/`nestedSpheres3`, and this one is `"sphere"`. Reading it as live
configuration would have produced three concentric shells that the real page never draws.

### Geometry

Fibonacci sphere, then a Fisher–Yates shuffle driven by the LCG `e = (9301e + 49297) mod 233280`
seeded at 12345. The shuffle is not cosmetic: points are drawn in buffer order and every point
is opaque, so buffer order decides which of two points landing on one pixel is the one you see.
Ordered points band visibly.

### Deformation

```glsl
float wobbleOrganic(vec3 pos, float time) { return snoise(vec4(pos / 1.5, time)); }
...
uPos += n * uNoise * uNoiseAmount / 6.0;
```

A 4D simplex noise sampled at the point's own position divided by 1.5, with **time as the fourth
axis** — that is what makes the body breathe rather than merely spin. The displacement is
**radial**, so the surface swells and dents instead of shearing, which is why the silhouette
reads as a stone and not as noise.

The amplitude is `wobble / 6`, so ±0.167 on a unit radius.

### Shading

```glsl
vec3 baseGray = vec3(0.85, 0.88, 0.92);        // dark theme
vec3 L = normalize(vec3(-1.0, 0.0, 0.5));
vec3 R = normalize(vec3( 1.0, 0.0, 0.5));
float totalLight = (max(dot(N, L), 0.0) + max(dot(N, R), 0.0)) * 0.9 + 0.1;
finalColor = baseGray * totalLight;
alpha = 1.0;
```

Two lights, hard left and hard right, both tipped slightly toward the viewer. They light a band
around the equator and leave the poles near black, which is what makes the orb read as a body
rather than a cloud.

Two details that are easy to get wrong:

- **The shading normal is the undisplaced direction**, `normalize(scaledPosition)`, not the
  normal of the deformed surface. Using the deformed one makes the lighting crawl with the
  wobble. It does not crawl.
- Because the normal ignores the wobble, the light term is a perfectly symmetric function of
  direction — so all the apparent asymmetry in the real orb is **density**, not shading. Where
  the surface swells, the same points cover more area and the region goes dim; where it dents,
  they bunch up and it goes bright.

### Point size

```glsl
gl_PointSize = 5.0 / (-viewPosition.z);        // x1.6 on the small layout
```

At the centre that is 5/8 = 0.625 px. `ALIASED_POINT_SIZE_RANGE` starts at 1 on every driver
tested, so in practice **every point is one pixel** and the depth term changes nothing. The fine
dotted texture is 33,000 one-pixel dots, and the bright limb is a projection effect: at a
grazing angle you look through far more of the shell per pixel.

### Output transform

The fragment shader ends at `gl_FragColor` with **no** `#include <tonemapping_fragment>` and
**no** `#include <colorspace_fragment>`. three.js only resolves the includes an author writes,
so a raw `ShaderMaterial` gets neither tone mapping nor an sRGB encode. The shader's value goes
to the framebuffer unchanged — which means a hand-rolled WebGL port must **not** add either, or
it will come out visibly too bright.

## The arithmetic that proves the reading

A unit sphere at the origin, seen from `z = 8` through a 50° vertical field, spans

    1 / (8 · tan 25°) = 0.268

of the half-height — so 0.268 of the viewport height, end to end.

- predicted: **0.268 H**
- measured on the running site at 1920×911: **0.277 H**

The wobble pushes the silhouette out by a few percent, which closes the gap. Our port at the
same viewport measures 242 px against a predicted 244 px. The numbers describe the thing on
screen, so the reading is right.

For contrast, the build this replaced used `base = min(W, H) · 0.355`, i.e. a diameter of
0.71·min(W,H) — about **2.6× too large**. That alone made it unrecognisable.

## What "two spheres" means on vanlent.dev — and what it means here

The preset named `2spheres_jittered` has `shape: "nestedSpheres2"`: an outer shell at radius 1
and an inner one at 0.54, **concentric**, counter-rotating. Not two orbs side by side. The page
carries exactly one canvas and one orb, morphing along scroll.

So "one, then two" is our behaviour, not theirs, and that is fine — it is the argument the two
sentences make. What has to be identical is the orb itself.

## Our implementation

`lab/orb.html`, 14.7 KB, self-contained, no external requests, no library.

WebGL is not a preference here. 33,000 points each needing a 4D simplex sample every frame is
roughly three million operations per frame for the noise alone, which is not a canvas-2D
workload. The whole scene is four small matrices and two short programs; three.js would be
357 KB to draw five uniforms.

The 4D simplex noise is Ian McEwan / Ashima Arts, MIT licensed — the same public implementation
vanlent.dev uses — quoted with its notice. The rest is written for this file: it computes the
same mathematics, because the mathematics is what puts the picture on screen.

Measured cost on Intel integrated graphics via ANGLE/D3D11: **0.005 ms per 33,000-point draw**,
against a 16.7 ms budget. Two orbs cost 0.01 ms.

### One measurement trap worth recording

The lab page's own FPS counter read `1 fps`, and a rAF-based timing probe timed out after 45
seconds. Both were false alarms: `document.visibilityState` was `"hidden"`, and Chrome throttles
rAF in a hidden tab. The GPU timing above — which does not depend on rAF cadence — showed the
draw is effectively free. **Before believing a frame-rate number, check that the tab was
visible when it was taken.**

## In page 2 (r73)

Ported into the statement section, reading the same `split` the sentence morph drives: one orb
while "One intelligence built the world." holds, two when "Two will build the next." arrives.
The second is held back until split 0.45 and then arrives quickly, so it reads as another one
appearing rather than as a shape that was always there fading up. Its noise clock runs 11.3s
off the first, because otherwise the pair is one body drawn twice.

Sizing is ours, not copied, and for a reason. The reference orb has a whole viewport: 244px on
a 911px-tall window. Ours has a 530x510 panel beside the sentence. Copying the ratio would put
33,000 points into a 137px orb - four times the reference's density, which turns the lattice
into a lump. So the diameter comes from the panel and **the point count follows the area**,
holding dots-per-pixel at the reference's value. Prefixes of the buffer are valid samples
because the cloud is shuffled, so this costs a draw range and no rebuild.

| | diameter | points | points/px^2 |
| --- | --- | --- | --- |
| reference | 244px | 33,000 | 0.706 |
| desktop panel 530x510 | 212px | 24,900 | 0.705 |
| phone panel 390x380 | 156px | 13,489 | 0.82 |

Measured on the built page: 205px against 212 predicted on desktop, and both orbs sit inside
the panel with margins at 390x380.

One correction along the way: the camera was first sized to the nominal unit radius, which drew
the orb about 8% wide - enough that a pair touched both edges of the panel. The wobble is
snoise in [-1,1] over 6, so the radius runs 0.833 to 1.167 and the silhouette is the maximum
around the visible rim. Sizing to 1.15 instead of 1.0 fixed it.

### The bug this round nearly shipped

The renderer is injected into the SAME closure as the sentence engine. It was first called
`paint` - and so is the sentence's own painter. A second function declaration of that name does
not shadow or warn; it silently replaces the first. The sentence morph was dead, and nothing
looked obviously wrong: the orbs still answered the scroll, the text still sat there, and only
a check of every character's `visibility` showed both sentences stuck on screen at once.

Worse, the collision guard written to catch it reported a clean bill. It found the closure's
end by searching for `})();` - a string the injected code itself contains - so it compared the
sentence engine against a third of the new block and missed the clash entirely. Bounding the
region by the injection marker, which is unique by construction, found it at once.

And then the fixed guard fired on the comment explaining the trap, because that comment
contains the declaration it warns about. The guard now strips block comments before scanning.
That is the third time this session a guard has matched prose rather than code; a guard that
does is a guard against writing documentation.

## Still open

- A true frame-rate reading with the tab visible, on the phone as well as the desktop. Every
  reading taken so far came from a hidden tab, where Chrome throttles rAF to about 1fps.
