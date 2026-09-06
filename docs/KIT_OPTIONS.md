# ORAN PORTFOLIO — DECISION SHEET
Six research passes, collapsed into the choices that remain. Verifier corrections are marked `[CORR]` and the corrected value is the one shown. Anything whose licence could not be confirmed is stripped out of the live options and parked in **§UNCONFIRMED** at the bottom.

**Two facts that reframe several decisions before you start:**
1. The 120 KB sprite budget and 240 KB font budget are **not binding**. Measured: two subsetted faces = 3,768 B raw / 5,024 B inlined; a 16-colour 1024×1024 isometric sheet = 29.0 KB. You have ~49× headroom on type and ~4× on sprites. Spend decisions on fidelity, not bytes. `[CORR — the palette research contradicted itself, saying both "the difference between one sheet and cutting content" and "77 KB to spare"; the second is right]`
2. Every "native size" in the font research was a guess. They have now been measured. Four were wrong. See D1/D2.

---

# PART A — TYPE

## D1. The shell face (menu bar, window titles, buttons, dialogs)

| Option | Native grid | Bytes | Licence | Honest downside |
|---|---|---|---|---|
| **Chicago Kare** (Duane King) | **16 px** `[CORR — research assumed 12 px; measured upm 1024, X-coordinate GCD exactly 64, zero off-grid X across all 95 ASCII glyphs → 1024/64 = 16]` | 9,400 B full / **1,884 B subsetted** `[CORR — research said 4–5 KB]` | **MIT** — no attribution, no reserved name | No bold, no italic, no small companion. 215 glyphs, not ~250 `[CORR]`. Reproduction of an Apple design — use the file, keep the word "Chicago" out of visible UI copy. |
| **ChiKareGo2** (Giles Booth) | 16 px em (BitFontMaker2 cell: 12 above baseline, 4 below) `[CORR — the chrome research said "12 px and 24 px only"; the tool's cell makes it a 16 px em, pixel-exact at 16/32/48]` | ~30 KB TTF | CC-BY (stated verbatim on the pentacom gallery page) | Permanent visible credit. Hand-reconstruction, not measurement. **Download is a JS `confirm()` → `?action=dl&id=3780`** — no direct URL, no version tag, no checksum; cannot be wired into a reproducible build. Ships stripe/close-box/Apple-logo extras. |
| **Pixel Operator** (Enaguas) | 16 px design + matched 8 px variant | ~40 KB | **CC0** (from release 2018.10.04-1) | Generic pixel sans. Reads DOS/console, not Apple — using it for window titles quietly kills the conceit. Scattered distribution; verify you have the post-2018 CC0 build. |
| **Spleen** (Cambus) | 5×8, 6×12, 8×16, 12×24, 16×32, 32×64 (six hand-drawn BDFs) | ~45 KB | BSD-2-Clause | Not a doubling ladder `[CORR — three separate chains plus an orphan 5×8; no 10×16, no 24×48]`. Console font: monospace, austere, will read as Unix terminal. Copyright notice must be reproduced. |
| **W95FA** | — | ~30 KB | OFL 1.1 (structured field confirmed; page published **3 Jan 2020**, not 2019 `[CORR]`) | Wrong machine, wrong decade. Listed only so it's ruled out deliberately rather than via a "best retro fonts" listicle. |

**Structural fact:** there is no true bitmap font on the web. WOFF2 wraps outlines; browsers ignore monochrome EBDT/EBLC strikes from webfonts (they *do* render CBDT/CBLC and sbix colour strikes — that's how emoji fonts work) `[CORR — the research's claim was too broad]`. Crispness comes from geometry alignment, never from file format.

**What I would pick and why:** Chicago Kare. It is the only option here that is simultaneously the correct historical face, MIT (no credit line to place inside a 1-bit shell, which is a real design problem for the CC-BY options), reproducibly fetchable from a real repo rather than a JS-gated hobby gallery, and now *measured* rather than assumed — 16 px em, pixel-exact at 16/32/48/64, `ascent-override:75%` / `descent-override:25%` derived from its actual hhea (768/−256 on upm 1024). At 1,884 bytes subsetted it is the cheapest thing in the project. Take ChiKareGo2's stripe and close-box glyphs only if you decide to draw window chrome as text — and if you do, archive both the TTF and the gallery page as your licence evidence before building on it.

---

## D2. The icon-label face (Geneva-class small text)

| Option | Native grid | Bytes | Licence | Honest downside |
|---|---|---|---|---|
| **FindersKeepers** (Booth) — 9 pt Geneva revival | 16 px em, 9 px design inside *(inferred from the BitFontMaker2 cell, not measured)* | ~30 KB TTF | CC-BY | Same JS-gated pentacom download, no versioning. 9 px caps in a 16 px em = a lot of dead vertical space; you will be overriding metrics. At 32 px it looks crude, not charming. Has the single-storey `a` the era used. |
| **Silkscreen** (Kottke) | **8 px** `[CORR — upm 1000, GCD 125, cap 625 = 5 font-px. And Kottke's rule is stated in POINTS: 8pt = 10.667 CSS px, which blurs. State it in px.]` | 8,404 B (Google latin) / 9,048 B (repo's own woff2) | OFL 1.1 — **Regular and Bold only** `[CORR — Expanded and Expanded Bold are not in the OFL distribution; they exist only in Kottke's 2001 freeware release. See §UNCONFIRMED]` | **No lowercase.** "Documents" renders "DOCUMENTS" — reads arcade, not Macintosh. Its lowercase glyphs are cosmetic: `a` and `A` have identical advance (750) and identical bbox (125,0,625,625). |
| **Tiny5** (Schmidt/Gissio) | **8 px** `[CORR — upm 1024, GCD 128, cap 640 = 5 font-px. The research's "at 5 px you're at the floor" objection was computed at a size you'd never set.]` | 9,036 B | OFL 1.1 | Proportional 5 px caps still degrade on fractional-DPR Windows (1.25/1.5). Zero era connection to 1984. Carries Cyrillic/Greek you don't need. |
| **Micro 5** | **11 px** `[CORR — upm 1650, GCD 150, cap 5 font-px. Identical to Departure Mono's grid, which the research called "hostile".]` | 8,932 B; **Charted companion 40,812 B** `[CORR — research said "doubles your payload"; it's 4.6×]` | OFL 1.1 | Designed for knitting charts — spacing optimises for stitches, not pixel legibility. Charted is a 40.8 KB gimmick. |

**The measurement that actually decides this:** advance-sum for the string "Documents" —
- Chicago Kare at its native 16 px = **72.0 px** → overflows a 64 px tile by 12.5% `[CORR — the research used "fits in a 64 px tile" to indict Press Start 2P while its own recommended face fails the same test]`
- Press Start 2P at native 8 px = **72.0 px** (identical; at *equal* font-size it's +100%, not the claimed "40–60% wider")
- Tiny5 at 8 px = **38 px** ✓ · Micro 5 at 11 px = **37 px** ✓

**What I would pick and why:** two different jobs, two answers. For the **Mac desktop icon labels**, FindersKeepers — it is the actual face the 1984 Finder used, the two-font Chicago/Geneva split is the single biggest tell separating a real retro-Mac from a pastiche, and the labels there sit on a 32 px icon with room to breathe. For **world-map tile labels that must fit inside 64 px**, Tiny5 at 8 px — it is the only OFL, measured, proportional face that actually fits, and neither Chicago-class nor Geneva-class type does. Accept two label faces; they never appear in the same scene, so nobody sees the seam.

---

## D3. Font delivery and the crispness contract

**Static vs variable — settled by measurement, and the research had it backwards.** `[CORR]` Pixelify Sans, live HEAD against Google:
- `family=Pixelify+Sans` (static 400) = **7,692 B** · `wght@400` = 7,692 B · static 700 = 7,904 B
- `wght@400..700` (variable, has `fvar`, 4 named instances) = **12,016 B**

Variable is **56% larger**, not smaller. Four statics = 30,768 B, not the claimed ~48 KB (that figure was 4 × the variable's own size). For Regular + one bold it's 12.0 KB variable vs 15.6 KB two statics — a 3.6 KB saving, not 40 KB. **And Pixelify Sans fits no pixel lattice at any pixels-per-em from 4 to 72 (best fit 14.4% of coordinates) — it is crisp nowhere, so "crisp at the four named instances" is also false.** The general rule stands on its own merits: a single-master outline-pixel font at its native size beats a variable one, because any intermediate axis value puts edges off-grid.

**Effects fonts, not UI fonts** (axis *is* the point, none reliably pixel-exact): Handjet **7,668 B** `[CORR from 7,328]`, carries a vendor warning about macOS rendering artifacts — and your audience is hiring managers on Macs. Bitcount Grid Single **3,764 B** `[CORR from 2,972; family is at v3, so it is no longer the smallest file in the survey — Sixtyfour 3,060 and Workbench 3,372 are smaller]`, and it fits no lattice either (best 25%), so "drawn on a strict lattice" is false. Workbench/Sixtyfour's SCAN and BLED axes model CRT scanline height and phosphor bleed — genuinely the most honest tool for "this is a 1984 screen" at 3 KB — but they're Amiga and C64 faces and BLED is the opposite of pixel-crisp by design. VT323 (17,936 B) was deliberately smeared then auto-traced; it antialiases at every setting and must never be UI.

**Subsetting — the real floor:**
```
pyftsubset ChicagoKare-Regular.ttf \
  --unicodes=U+0020-007E,U+00A9,U+2022,U+2192 \
  --layout-features='' --no-hinting --desubroutinize \
  --drop-tables+=DSIG --flavor=woff2 --output-file=shell.woff2
```
→ **1,884 bytes** (98 codepoints). ASCII-only = 1,856 B. A 4-glyph subset = **508 B**, which refutes the claimed "~1 KB fixed container overhead, can't go below 2.5 KB" `[CORR]`. Strip hinting deliberately — DirectWrite grid-fitting shifts stems on a font that is already grid-perfect.

**Inline as data URI.** Base64 = +33% and does not recover under gzip/brotli (the payload is already deflate-compressed). Two faces inlined ≈ **5,024 B**. Zero external requests, no FOUT.

**The CSS, corrected:**
```css
@font-face{
  font-family:"Shell";
  src:url(data:font/woff2;base64,…) format("woff2");
  font-display:block;
  ascent-override:75%; descent-override:25%; line-gap-override:0%;  /* Chicago Kare hhea 768/-256 on upm 1024 */
}
.shell{
  font-family:"Shell",monospace;
  font-size:32px;        /* 16px em × k=2. NOT 24px — see below */
  line-height:32px;      /* px, never unitless */
  letter-spacing:0;      /* fractional tracking = guaranteed blur */
  -webkit-font-smoothing:none;   /* real, but macOS WebKit/Blink only */
  font-synthesis:none; font-kerning:none; font-variant-ligatures:none;
  text-rendering:optimizeSpeed;  /* NOT geometricPrecision — enables subpixel positioning */
}
```
There is **no** switch that disables antialiasing in Chrome or Firefox on Windows or Linux. `-webkit-font-smoothing` and `-moz-osx-font-smoothing` are macOS-only per MDN. Never set `-moz-osx-font-smoothing:grayscale` from a reset — it forces smoothing on.

**DPR arithmetic.** One font-pixel = k CSS px = k × DPR device px, and that must be an integer.
- DPR 1.0 / 2.0 / 3.0 → any k
- DPR 1.5 → k must be **even**. On a 16 px em: 32, 64. **16 px itself blurs.**
- DPR 1.25 / 1.75 → k must be a multiple of 4 → 64 px minimum. Effectively unusable.

`[CORR]` The research's convention #9 recommends "2× (24 px)". On the measured 16 px em that is **k=1.5 and blurs at DPR 1** — the exact failure it warns against. But it also claimed "1.5× is not an integer and is therefore not available to you", which is false: k=1.5 at DPR 2 gives 3 device pixels, so **24 px is pixel-exact on a Retina Mac** and lands at 113.4% of 1984 physical size vs 32 px at 132.1% on a 109 ppi monitor. Physical-size reality: one 72 dpi pixel = 0.353 mm; one CSS px at 109 ppi = 0.233 mm, at 254 ppi ≈ 0.20 mm.

**The zero-risk fallback:** draw the menu bar and the seven icon labels once into a canvas at 1× with `imageSmoothingEnabled=false`, scale by an integer with `image-rendering:pixelated`. Deterministic on every browser, DPR and zoom — and it's the same mechanism the isometric renderer already uses. Price: text stops being selectable and screen-readable, so mirror it in a visually-hidden span.

**What I would pick and why:** two static single-master faces, subsetted to ASCII plus `© • →`, inlined as base64, at **k=2 (32 px shell / 16 px labels)** as the default, with a runtime `devicePixelRatio` read that snaps k to the nearest legal value and re-checks on resize. Total ~5 KB. Skip variable entirely — the one case where it was supposed to win measured backwards, and the font it was supposed to win with isn't pixel-crisp at any size. Canvas-render the menu bar and the seven labels (short fixed strings, highest fidelity stakes, mirrored in aria) and leave everything else as live DOM text so it stays selectable and indexable.

---

# PART B — COLOUR

**Anchors, verified exactly by two independent re-derivations:** `#2FB380` okL 68.4 okC 0.135 · `#E0A458` okL 76.1 okC 0.117 · `#5E8FBF` okL 63.5 okC 0.090 · `#F2F1ED` okL 95.8 · `#191A1F` okL 21.9, okC **0.010**, OKLab hue **276.6** `[CORR — the stated "hue 230" is the HSL hue; the cool-cast argument is directionally right but leans on a near-neutral colour]`.

**The tokens are not equal in weight:** brass is lightest at 76.1, ice darkest at 63.5 — a **12.58** okL spread. If all four ramps use identical offsets, brass reads as the loudest company and ice the quietest, purely from the tokens.

## D4. Ramp geometry for XTIX / OASIS / EVENTER

| Option | Stops | Emerald ramp | Honest downside |
|---|---|---|---|
| **P1 — flat HSL lightening** *(the control, include to reject)* | 5 | `#16523B #22835D #2FB380 #4FD19E #7FDDB9` | Measured chroma across the ramp: 0.073 → 0.107 → 0.135 → **0.137 → 0.104**. The highlight desaturates and reads chalky; the shadow reads as the same green with the lamp turned down. Verified exactly. |
| **P2 — ground-keyed mix** | 4 | `#225A48 #288261 #2FB380 #6AC6A1` | Brass drops from okC 0.117 to **0.054** at its darkest stop and stops being brass — it's khaki. Only 4 stops: no room for both a lit top face and a rim. Least characterful. |
| **P3 — disciplined hue-shift** *(research's lead)* | 5 | `#164D44 #217D63 #2FB380 #55CA8F #92D4AC` | `[CORR]` **Its one auditable rule fails on 6 of 12 non-anchor stops** (emerald 13.4/13.2, brass 12.3, ice 12.3/13.3 — max 13.6 including P4). Cause: hue shifted ±12° in HSL, *then* endpoints pulled 22%/10% toward ground/paper, which rotates hue further. okL steps uneven (38.2, 53.0, 68.4, 75.7, 81.5): 15-pt gaps low, ~6-pt gaps high, so stops 4–5 collapse on small props. Darkest stop only **16.3** okL above the ground. |
| **P4 — "equal okL step"** | 5 | `#1B6055 #24886C #2FB380 #5CCC94 #9ED8B6` | `[CORR — two separate failures]` **(a)** It does not equalise the companies: measured brass-minus-ice is 12.54/12.67/12.58/12.46/12.73 at each stop — the 12.58 token spread is preserved to two decimals. Equal steps *from each token's own anchor* translate the ramp, they can't level differing anchors. **(b)** Steps are 11.9/12.1/8.1/**6.8** — the bottom step is 75% larger than the top, and 6.8 is the same collapse P3 is criticised for. |
| **P5 — high-contrast AoE2 register** | 5 | `#09353B #146D62 #2FB380 #63D18D #AFDBB4` | Breaks family visibly. Brass darkest `#86210E` is red brick; ice `#1C1F6D` is indigo; **emerald `#09353B` measures hue 187.2 — cyan, 30.4° off `[CORR — the research flagged only brass and ice]`**. Bright ends collide with paper (brass `#F3EEDE` okL 94.9 vs `#F2F1ED` 95.8). |
| **P6 — soft 3-stop, Sims register** | 3 | `#238C75 #2FB380 #4CC988` | Darkest stop okL 57.6 — **35.7 above the ground**, so objects float rather than sit. No stop dark enough for a contact shadow, so you need a separate shadow colour anyway and the 12-slot saving partly evaporates. No focal hierarchy. |
| **P7 — token as the LIT TOP FACE** | 5 | `#08262C #135A58 #1F8671 #2FB380 #63C686` | Contact stop `#08262C` is okL **25.0** against the ground's 21.9 — a 3.1 gap, effectively invisible `[CORR — a far more damning number than the ones the research cited]`. Brass `#791F12` is oxblood. Token appears only on the smallest cube face. |
| **P8 — two-stop tier for props <16 px** | 2 | `#287F5F / #2FB380` | Only works if the scenes have a genuine near/far distinction. If everything is the same size it reads as unfinished art beside 5-stop hero objects. |

**What I would pick and why:** P3 as the shape, with the construction order fixed — apply the ground/paper endpoint pull **before** the hue shift so the 12° cap actually holds on the shipped hex, then restate the rule as measured on output ("capped at 12°, verified post-pull") so it survives the audit it invites. P3 is right because the token stays a real, large, front-left face colour rather than an abstraction hidden between stops, and because 5 stops map exactly onto contact shadow / right face / left face / lit top / 1px rim. Reject P4 outright: it is sold on a benefit that is arithmetically the inverse of its construction, and if you actually want the companies equalised you need shared *absolute* okL targets (all three ramps hitting 40/52/64/76/88), which is a different font of ramp nobody has built yet. Add P8 as a second tier for sub-16px props — below 16 px a 5-stop ramp is a lie.

---

## D5. MEDCOIN — the `--ink` company with no hue

| Option | Values | okL | Honest downside |
|---|---|---|---|
| **N1 — existing token greys only** | `#191A1F #25262D #33353C #4B4E55 #B6B7BB #CFD0D4 #F2F1ED` | 21.9 · 27.1 · 33.0 · 42.4 · 78.0 · 85.8 · 95.8 | **A 35.6 okL hole between `#4B4E55` and `#B6B7BB`.** Anything shaded on this set bands hard. Built from the same greys as the grid and cards, so MEDCOIN won't read as a company — it reads as background. |
| **N2 — warm-paper ramp** | `#434137 #6F6B5D #9F9989 #CAC6BA #F2F1ED` | 37.4 · 52.7 · 68.4 · 82.6 · 95.8 (steps 15.3/15.7/14.2/13.2) | Warm greys not in the token list — the option most exposed to a strict "no new colours" reading. Makes MEDCOIN parchment-coloured, which is a character choice (aged document) that may not suit a medical-coin brand. `[CORR — "most even spacing of any ramp here" is beaten by P6-ice, spread 1.5 vs 2.5; qualify it to 5-stop ramps]` |
| **N3 — split-neutral (cool shadow, warm light)** | `#303340 #575D6B #8B9198 #CCCCC2 #F2F1ED` | 32.4 · 47.8 · 65.4 · 84.2 · 95.8 | `[CORR — half right]` `#303340` vs `--grid #33353C` is **dE 1.2** — a real collision, MEDCOIN objects merge with grid lines. But `#575D6B` vs `--grid2 #4B4E55` is **dE 5.6**, visible separation, not a merge. So the objection holds for one stop, not two. |

**What I would pick and why:** N2. The real MEDCOIN problem is that a company whose identity is `#F2F1ED` has no hue to build from, and building it from the *cool* token greys makes it vanish into the UI — which is exactly what N1 does and what N3 does at one stop. Going warm puts it in clean opposition to both the cool `#191A1F` ground and the cool grid, so it reads as a distinct fourth thing without inventing a brand hue. The defensible framing when someone objects: these are shading stops for `#F2F1ED`, the same status as P3's stops for `#2FB380`. If that framing is rejected, the whole ramp system falls with it, so settle that question once for all four companies rather than per-company.

---

## D6. Total palette size

**The cost curve, measured on identical artwork at minimum legal PNG bit depth — and it is not what the research said:** `[CORR]`

| Colours | Bytes | Note |
|---|---|---|
| 16 | **29,661** (29.0 KB) | 4bpp |
| 17 | 43,762 | **the cliff: +13.8 KB, +48%** |
| 18 | 43,828 | |
| 24 | 43,701 | |
| 32 | 43,716 | *smaller than 18* |

Slots 18–32 cost **~15 bytes total**. You pay once at slot 17, never per slot. So "adding dither costs roughly the same as doubling the palette" and T2's "67% increase for 16 extra slots you may not use" are both framed wrongly. **The rule is binary: stay at 16, or take all 32.** That also makes T3 (27 colours) strictly dominated — it pays the 8bpp price while wasting 5 of the 32 slots it bought.

Two further corrections to the headline figures: T1's quoted **25.5 KB was measured on a sheet that never painted 5 of its 16 colours — and they were exactly the neutrals** (`#25262D #33353C #4B4E55 #B6B7BB #F2F1ED`), because the test script's index cycle started at 6. Painting all 16 on identical geometry gives **29.0 KB**. And the "32-colour" measurements were written with a padded **256-entry PLTE** (768 B instead of 96 B), so T2/T3 should read ~41.9 KB, not 42.6.

- **T1 — 16 colours (EGA discipline):** 6 shared neutrals + 3 stops each for emerald/brass/ice + 1 shared deep shadow. **Downside:** 3 stops per company means no rim and no per-company contact shadow — you are choosing P6's flatness whether you meant to or not. MEDCOIN gets no ramp and must borrow the neutrals, which is N1's disappearing problem. Zero headroom: any new scenery colour reopens the whole palette.
- **T2 — 32 colours (Amiga discipline):** 9 neutrals + full P3 5-stop ramps ×3 + a 4-stop MEDCOIN + depth tints + true black `[note: the script's 32nd slot was #0F1013, not the #000000 the spec says]`. **Downside:** more slots means less discipline — limited palettes cohere because reuse is *forced*, and at 32 an artist stops reusing. Expect drift over a long build unless someone polices it.
- **A1 — atmospheric depth tinting** (a second axis on any ramp): emerald at 0/18/36/54% depth = `#2FB380 / #2B976F / #277C5D / #23604C`; brass `#E0A458 / #BC8B4E / #987243 / #755939`; ice `#5E8FBF / #527AA2 / #456585 / #395069`. **Downside:** multiplies the palette by the band count — 3 bands turns 20 chromatic slots into 60, past any discipline. And XTIX at the far end of the map is no longer `#2FB380` in any recognisable sense.

**What I would pick and why:** 32. The research recommended 16 on a byte argument that no longer exists — the real cost is a single +13.8 KB cliff you cross the moment you want a 17th colour, and 41.9 KB against any realistic budget is nothing. Sixteen buys you three stops per company, which silently downgrades D4's P3 to P6 and leaves MEDCOIN homeless; thirty-two buys full 5-stop ramps for all four companies with room for two depth bands on the world map only. Take the discipline the 16-colour constraint would have imposed and impose it by hand instead: write the 32 slots down as a fixed table, assign each ramp a contiguous index run (which D7 needs anyway), and treat adding a colour as a change that requires reopening that table.

---

## D7. Dithering policy

**The QuickDraw pattern bytes, verbatim from `InitGraf`** — these are published facts, free to use: white `0x0000000000000000` · black `0xFFFFFFFFFFFFFFFF` · **gray (50%) `0xAA55AA55AA55AA55`** · ltGray (25%) `0x8822882288228822` · dkGray (75%) `0x77DD77DD77DD77DD`. Each is 8×8 bits = 8 bytes. Where each was used: 50% = desktop, scroll-bar track, dimmed menu text, `DragGrayRgn` outlines. 25% = utility/palette window title bars ("don't use racing stripes in a utility window title bar") and tear-off menu drag regions. 75% = subscriber borders, 3 px wide. **Critically: the desktop pattern is aligned to the global port origin, not to each window** — patterns never shift when a window moves. Anchor your 8×8 tiling to the page, not to the element.

| Option | Measured cost | Honest downside |
|---|---|---|
| **D1 — Bayer 4×4 between adjacent ramp stops** (matrix `[[0,8,2,10],[12,4,14,6],[3,11,1,9],[15,7,13,5]]/16`, 17 levels) | +16.97 KB (correctly implemented) | At 2× integer scale one art pixel is 2 device pixels, so a 4×4 cell becomes an **8×8 device-pixel crosshatch** that does not optically blend at any normal viewing distance. This is the argument that actually kills it. |
| **D2 — 50% checkerboard, confined to the 1984 shell** | **+12.22 KB — 28% cheaper than Bayer 4×4, independently verified** | At 2× it becomes a 2×2 block pattern and stops looking like the crisp Mac original, so it must be authored at *device*-pixel scale — which means it cannot live in the same integer-scaled sprite pipeline as the isometric art and needs its own render path (CSS `repeating-gradient` or a separate 1× layer). Shimmers on non-integer browser zoom, which you don't control. |
| **D3 — Bayer 2×2 on ground seams only** (`[[0,2],[3,1]]/4`, 5 levels) | 38,607 B | `[CORR]` **Bayer 2×2 thresholded at 50% IS D2's checkerboard — byte-identical, 38,607 B each.** These are not two options at the level D3 would be used at. Also: a single dithered seam among flat art reads as a compression artifact to anyone who doesn't know the reference. |
| **D4 — no dither inside the scenes; buy a stop instead** | dither +17.19 KB vs colours +17.12 KB | `[CORR — the claim "strictly dominates" rests on 80 bytes, 0.18% of a 43 KB file, and it REVERSES when the measurement bug is fixed]`. The test script's "dither" was `px = max(1, index-1)` — a palette-index decrement, not a blend between ramp stops — and under the test palette's ordering it blended emerald-dark into **paper white**, brass-dark into emerald-light, ice-dark into brass-light. Varying only the test sheet's cell spacing flips the winner in 6 of 16 configurations, from 9,753 B cheaper to 5,998 B dearer. The conclusion may still be right; the byte argument does not support it. |
| **Tiles ATLAS-3 — Bayer between existing tokens to fake shading** | 0 (patterns compress extremely well) | Directly conflicts with D4. Also doesn't solve the problem it claims: three faces want three distinct values, and dithering gives convincing midtones between *two*, not a ramp. |

**What I would pick and why:** D2 alone — checkerboard in the shell, nothing inside the isometric scenes. Not because of file size (that measurement is noise) but because of D1's optical argument, which is the only one that survives scrutiny: a 4×4 Bayer cell at 2× is an 8×8 device-pixel crosshatch, which is texture, not tone. Confining the checkerboard to the shell also makes "SHELL IS 1984 / CONTENT IS 2026" a mechanical rule rather than a mood — dithering literally marks where the eras divide — and it is the cheapest 28%-cheaper-to-compress thing on the list. This also settles the tiles research's self-declared blocking question ("does *no new colours* mean no new tokens or no new pixel values?"): it means no new **tokens**, the ramps in D4/D5 are shading stops, and ATLAS-3 is not needed as a substitute for them.

---

## D8. Outline / silhouette policy

Forced by the numbers, not optional: P3's darkest emerald `#164D44` is only **16.3** okL above the `#191A1F` ground, and ice's `#293E6F` only **15.4**. Both will have mushy silhouettes.

- **(a) No outline**, use each ramp's stop 0 as the edge. *Downside:* it will look weak — those 15–16 point gaps are the whole problem.
- **(b) Universal 1px outline in `--grid #33353C`** (okL 33.0). *Downside:* easiest to implement and keep consistent, but pushes the look toward sticker-art and away from the soft-3D island reference.
- **(c) Selective:** dark edge on the shadow side, ramp stop 4 as a 1px rim on the lit side, nothing elsewhere. *Downside:* requires deciding a light direction per object and holding it across every asset — exactly the consistency that slips on a long build and is very visible when it does.

**What I would pick and why:** (c), paired with a written light-direction rule fixed on day one and never revisited (which D-bake in the tiles section requires anyway — baked shadows lock your sun angle permanently). It costs no palette slots, reads as directional lighting rather than a cartoon stroke, and it is effectively what AoE2 and HoMM3 both do. Accept (b) as the fallback if the build stretches and consistency starts drifting — a universal outline that is applied uniformly beats a selective one applied inconsistently.

---

## D9. Sprite reuse — the biggest byte saving available

**R1 — one grey master, per-company index remap (AoE2's player-colour technique).** Author every shared object once in a neutral 5-stop master (`#303340 #575D6B #8B9198 #CCCCC2 #F2F1ED`), then map stop-for-stop onto emerald / brass / ice / N2 at runtime. Cuts the sheet by close to 4× on any object appearing in more than one territory — far bigger than any palette-size decision.

**Downside:** needs a runtime recolour path (a canvas pass), and pre-baking the four variants gives back the entire saving. A canvas pass means the art is no longer a plain `<img>` — an extra failure mode and some first-paint cost. It also constrains authoring absolutely: every object must be drawn to exactly 5 stops with no off-ramp accents, or the remap produces wrong results.

`[CORR]` Drop "verify the index run against the actual 50.pal" as an action item — that file lives inside AoE2's DRS archives, is proprietary Microsoft/Ensemble/Forgotten Empires content, and cannot be vendored. The *technique* is a method, not protectable expression, and is unaffected. State the index count as unverifiable, not pending.

**What I would pick and why:** take R1, but only if D6 lands on 32 colours — with contiguous index runs per ramp, which the Deluxe Paint convention already requires and which D7's dither measurement was broken by lacking. The saving is real and it is the largest single lever in the sprite budget, and the authoring constraint it imposes (exactly 5 stops, no off-ramp accents) is a constraint you want anyway for palette discipline. Do the recolour as a one-time canvas pass at load into four cached `ImageBitmap` sets, not per frame — you pay the CPU once and the art is a plain blit thereafter.

---

# PART C — THE ISOMETRIC WORLD

**Fixed contract:** `sx = (x−y)*32`, `sy = (x+y)*16 − z*16`. Tile 64×32. z-unit 16 px.

**2:1 is dimetric, not isometric.** 2:1 puts the ground axes at `atan(1/2)` = **26.565°**. True isometric is 30° (a 1.732:1 ratio). 2:1 won because `tan = exactly 1/2` means every step along a ground axis is 2 px across and 1 px down — a perfectly periodic 2-pixel run, no AA, no jitter, identical at any length. A 30° line has slope 0.577 and produces an aperiodic Bresenham pattern of mixed 1px and 2px runs. Every reference game chose 2:1 and none of them are isometric.

**The heritage numbers:** Civ II terrain diamond **64×32** (exactly your contract; its overlapping diamond is the documented cause of the famous north/south road gaps). OpenTTD `TILE_SIZE=16`, `TILE_PIXELS=32`, `TILE_HEIGHT=8`, `MAX_TILE_HEIGHT=255`, ground sprite 64×31 at base zoom — **note its z step is 8 px = half its 16 px per-row y step; yours is 16 px = the full step, so your elevation is exactly twice as steep as Transport Tycoon's.** AoE2 rhombus **97×49** (= 2·48+1 by 48+1, giving 1px vertex tips and rows 1,3,5…97…5,3,1), blendomatic tile_size 48·49+1 = 2353, 4 blend patterns per terrain pair. Sims 1 SPR2 carries **three** channels — colour, **z-buffer**, alpha — and a DGRP always holds exactly 12 images (3 zooms × 4 rotations). **HoMM3 is not isometric at all** — flat top-down 32×32 squares, all depth painted in.

## D10. The path (career route across the world map)

| Option | Sprites | Size | Honest downside |
|---|---|---|---|
| **PATH-1 — full 16-tile 4-bit bitmask** (N=1, E=2, S=4, W=8; 1 isolated + 4 dead ends + 2 straights + 4 corners + 4 T + 1 cross) | 16 | ~8 KB | 4-connected only, so the route can only step along the four screen diagonals — anything wanting to run screen-horizontally becomes a staircase. A 4-stop route uses maybe 6 of the 16; you ship 10 that never appear. |
| **PATH-2 — symmetry-reduced, 10 drawn + h-flip** (h-flip is `sx → −sx`, which under `sx=(x−y)*32` is exactly the x↔y swap, and `sy=(x+y)*16` is invariant under it; with the vertical flip too the group has order 4 → 7 sprites) | 10 (or 7) | ~5 KB | **Flipping mirrors the light.** Any directional shading gets lit from the wrong side halfway along the route. The vertical flip is far worse (top-lit becomes bottom-lit). Only safe if the path is lit flat. |
| **PATH-3 — spoke/stub compositing** (one half-segment per direction + centre cap; 5 sprites cardinal-only, 9 for full 8-connectivity) | 9 | **~4 KB** | No corner bevelling — two stubs at 90° give a hard mechanical join, and a real bend wants art that knows it's a bend. Overlapping stub edges double-darken on any partial alpha, so the art must be strictly 1-bit alpha. 2–5 `drawImage` per path tile. |
| **PATH-4 — author only the ~6–8 configs the real route uses** | 7–9 | ~4 KB | Brittle to editing. Reroute the path or add a fifth company and you get a mask with no tile behind it — a hole in the road. Needs a fallback console warning and a re-audit every map change. |
| **PATH-5 — polyline in WORLD space, projected** (offset ±half-width **in world space before projecting**, because a ground circle projects to a 2:1 ellipse) | 0 | 0 | Anti-aliased vector on nearest-neighbour pixel art — the exact contrast that makes hybrid pixel scenes look cheap. Quantise it and you've written a custom Bresenham. Also a single flat layer: cannot be occluded per-tile. |
| **PATH-6 — stepping stones** (16×10 px at tile centres, offset −8,−5) | 1–4 | <1 KB | Looks sparse and placeholder-ish unless the stone art carries real weight. A 90° bend has no visual cue that it *is* a bend — the route is inferred from proximity alone, which fails if two branches ever pass near each other. |
| **PATH-7 — dashed trail with animated reveal** (dash lengths quantised to the 2px iso run) | 0 | 0 | Marching-ants reads as UI chrome, not terrain — can make the map feel like a slide deck with an arrow on it. Animated dash reveal is a 2015 scrollytelling idiom and fights "the shell is 1984". |
| **PATH-8 — pre-bake the whole route as one PNG** | 1 | **25–60 KB** | A 900×500 transparent PNG-8 at 4bpp is ~225 KB raw. Completely un-editable — moving a company means redrawing. Single flat layer, cannot be occluded. |
| **PATH-9 — generate the tiles procedurally at load** (row y in 0..15, fill x = 30−2y to 33+2y, mirrored) | 0 | **0** (~1.5 KB JS) | Flat. No hand, no dither texture, no worn edges — reads as a *diagram* of an isometric map. Front-loads a few ms and you must debug a small rasteriser. |
| **PATH-10 — 47-tile blob autotile** (cardinals bits 0,2,4,6 = 1/4/16/64; diagonals 1,3,5,7 = 2/8/32/128; 256→47 by clearing each diagonal unless *both* adjacent cardinals are set) | 47 | ~30 KB | Overwhelmingly the wrong tool for a one-tile-wide route — it exercises maybe 8 of 47. A quarter of the sprite budget on inner-corner tiles that can never appear. |
| **PATH-11 — dual-grid corner Wang** (16 tiles offset by 32,16) | 16 | ~8 KB | The half-tile offset means the visible grid no longer lines up with the data grid, which breaks click targets, landmark anchoring and painter's sort simultaneously. It's a *region* technique — a one-tile-wide line is its worst case. |

**The constraint nobody mentioned in the brief:** `sx=(x−y)*32` means +x is down-right and +y is down-left, so a 4-connected path can only move along the four screen diagonals. **HoMM3's roads look like roads because it is an 8-connected square top-down grid.** Copying that feel inside a 4-connected iso grid is a category error. World diagonals are the free win: `(+1,+1)` is straight **down** the screen by 32 px, `(+1,−1)` is straight **right** by 64 px — both exact integers, both inside the contract.

**Seam geometry, settled:** use the **even 64×32 diamond** with rows stepping 2 px per side (widths 4, 8, 12 … 64, **doubled at the equator**, 4 px tips). It is the only variant arithmetically exact against `sy=(x+y)*16`. The odd-height family (AoE2 97×49, TTD 64×31) buys sharper tips but a 1px seam — precisely the defect Civ II shipped.

**What I would pick and why:** PATH-3 at 9 sprites, 8-connected. It is the only option under 5 KB that solves the actual problem — the staircase — and it does it by adding one sprite per direction rather than a rebuilt lookup table. No bitmask, no 47-tile combinatorics, no special-casing: for each connected neighbour, draw its stub. If the mechanical corner joins bother you once you see them, adding four bevel sprites later is additive rather than a rewrite, which none of the table-driven options give you. Pair it with PATH-7's forward reveal **only if** you can make the dashes read as terrain rather than chrome; if not, drop the animation — the route being a time axis is a nice-to-have, and marching ants in a 1984 shell is a loud wrong note.

---

## D11. Elevation

- **ELEV-1 — none.** Height painted into tile art, z used only for landmarks. *Downside:* flat maps are flat; a level plane with four buildings on it can read as a chessboard, and elevation is the hardest thing to retrofit.
- **ELEV-2 — landmark plinths only** (z=1 or 2 = 16 or 32 px; a 3×3 plinth at z=1 is a 192×96 diamond plus a 16 px skirt = 192×112). *Downside:* a plinth with no other relief anywhere looks like a showroom pedestal, especially at z=2. Introduces the first real sort case — the plinth front face must draw after the ground tile in front but before anything standing on it, so a landmark is now ≥2 sortable pieces.
- **ELEV-3 — full slope set (OpenTTD model).** 4-bit corner mask = 16 combos = 1 flat + 15 slopes, plus 4 steep = 19 ground shapes **per terrain type**, plus sloped path variants. *Downside:* **it breaks the fixed contract.** Painter's sort on x+y+z assumes one z per tile; a per-corner heightmap does not have one. Plus a plausible 3× sprite-sheet increase. Effectively off the table — say so rather than half-implementing.
- **ELEV-4 — cliffs as objects on flat terrain.** *Downside:* a lie that shows. Terrain above and below the cliff is at the same z, so anything near the edge is at the wrong height, shadows disagree, and the path can't cross without a ramp sprite that is itself fiction.

**Footprint arithmetic under your projection:** a W×H footprint has a base diamond **(W+H)·32 wide × (W+H)·16 tall**. 2×2 = 128×64. 3×3 = 192×96. Add 16 px per z unit. A 3×3 landmark standing 5z tall is **192×176 px**. Budget from these, not from guesses.

**What I would pick and why:** ELEV-2 at z=1. It buys the entire visual benefit of elevation — the four stops become important, they sit *on* the world, they get a base shadow and a bigger click target — for four sprites and zero new systems, using machinery the contract already defines. z=2 tips into pedestal territory. ELEV-3 is genuinely off the table because it invalidates the sort key, and that is worth stating flatly to the room rather than leaving as an open possibility that costs a week to discover.

---

## D12. Sort order

- **SORT-1 — sort multi-tile objects by their FRONT tile.** Key = `(x0+W−1) + (y0+H−1) + z`; emit when the painter reaches that tile. Store an explicit per-sprite anchor `(ax,ay)` in atlas metadata and draw at `(sx−ax, sy−ay)`. A plain 64×32 ground tile has anchor `(32,16)`. *Downside:* fixes depth **order**, not overlap — two large landmarks whose boxes intersect can still form a cycle no single key resolves. Does nothing for sprites overhanging their footprint. A wrong anchor is a silent 8px misalignment that's easy to eyeball-fix in the wrong direction.
- **SORT-2 — slice big landmarks into per-tile sprites (Sims 1 DGRP model).** Makes cyclic overlap structurally impossible because every drawable is exactly one tile. *Downside:* 9 atlas entries and 9 gutters for a 3×3; tall sprites get cut through their middle so slice boundaries must be pixel-exact or you get visible seams down the building; overhang must be hand-assigned to a slice.
- **SORT-3 — make the bug impossible by spacing.** Every landmark footprint odd-sized (3×3, so it has a true centre tile for label and click target); no two footprints within 2 tiles of each other or of any prop taller than 1z. Hit test with the diamond, not the box: inside tile (x,y) iff `|dx|/32 + |dy|/16 ≤ 1`. *Downside:* it's a constraint on art direction, not a solution, and constraints get forgotten — cluster two companies later and the bug returns silently.

**Tie-breaking, unavoidable:** `x+y+z` ties constantly for props sharing a cell. Break with a stable secondary key — a per-entity insertion index, or a layer byte (ground=0, decal=1, prop=2, actor=3, overlay=4). Without it the sort is unstable across browsers and props flicker between frames.

**What I would pick and why:** SORT-1 plus SORT-3's spacing rule, with an assertion in the map loader that checks the spacing and console-warns. For a map with four well-separated stops on a 16×16 grid, that combination is *provably* sufficient and costs two integers per sprite plus a validation function — SORT-2 is engineering for a problem this scene does not have. The assertion is the load-bearing part: the failure mode of SORT-3 is that someone clusters two companies for a visual reason six weeks from now and gets a building drawn in front of one it should be behind, which is subtle enough to ship.

---

## D13. Atlas packing and delivery

- **ATLAS-1 — one 512×512 fixed-grid PNG-8, 2px gutters, indexed.** 66×34 cells (64×32 + gutter) = 7 cols × 15 rows = 105 tile slots. Realistic content: 8 ground variants (16,384 px) + 16 path tiles (32,768) + 16 props at 64×48 (49,152) + 4 landmarks at 192×176 (**135,168 — 58% of the pixel budget on their own**) ≈ 233,000 px, inside 512×512 = 262,144. At 4bpp = 131,072 B raw, deflating 3–8× to **15–40 KB**. *Downside:* a fixed grid wastes space on anything not tile-shaped, and if the landmarks grow you repack. 40 KB is the *optimistic* ceiling — richly dithered art could land at 60–70 KB. PNG-8 gives exactly one alpha level: no soft edges anywhere, ever. A soft shadow means PNG-32 and ~3× the size.
- **ATLAS-2 — inline base64 vs same-origin file.** Base64 = 4/3 plus newlines ≈ **+37% in practice**, and it does **not** recover under gzip/brotli because the PNG is already deflate-compressed. A 35 KB PNG becomes ~48 KB of text. A same-origin `/assets/atlas.png` costs one request and zero inflation, plus browser caching. *Downside:* if the requirement really is a single portable HTML file you can hand someone, inlining is mandatory and the 37% is the price — plus re-download on every load with no cache, plus 48 KB of base64 noise in view-source, which for a portfolio a technical reader might inspect is a small real cost.

**Hard caps to design against:** one canvas must stay under **16,777,216 px** (4096×4096 equivalent) or iOS Safari throws. Total canvas memory across a page is capped around **224–384 MB** depending on iOS version, and Safari holds dead canvases longer than you expect. A 430×932 CSS viewport at DPR 3 is 1290×2796 = 3.6M px = 14 MB — safe. **A 64×64 tile map pre-rendered as ONE surface at scale 2 is 16384×8192 = 134M px — eight times over the cap, instant crash.** Chunk at 512×512 or 1024×1024, never one surface. Texture atlas floor: 2048×2048 is universally safe; 4096 is fine on any post-A7 iOS device but isn't worth the risk.

**What I would pick and why:** ATLAS-1 at 512×512, delivered as a **same-origin file, not inlined**. "Zero external requests" almost certainly means no third-party hosts — no CDN, no Google Fonts, no analytics — not literally zero HTTP. A same-origin PNG recovers ~13 KB, gets caching for free, and keeps view-source clean. Settle that reading explicitly at the decision session, because if it turns out the deliverable really is a single portable file you must budget 48 KB not 35 KB, and that is a number people plan around. Fonts stay inlined either way — they're 5 KB and the FOUT risk on a pixel face is worse than the request.

---

# PART D — THE 1984 SHELL

**These metrics are facts and are free to use. The artwork is not.** Chicago, Geneva and Monaco are Apple typefaces; the System 6 icon set is Apple's and Susan Kare's. Do not extract from a ROM or disk image.

## D14. Where the chrome metrics come from

| Source | What it uniquely gives | Honest downside |
|---|---|---|
| **Inside Macintosh: Toolbox Essentials** (woofle.net/impdf/, chapter PDFs 150–600 KB; `pdftotext -layout` + grep "pixel" surfaces nearly everything in a minute) | 20 px menu bar and title-bar offset · scroll bar 16 px wide / 15 px gutter / 48 px minimum · 15×15 size box clip rect · button 20 px tall · 59 px OK/Cancel · 12×12 checkbox · 1px outer + 2px inner modal frame · 13/23 px dialog spacing · ICN# 32×32 / ics# 16×16 · arrow hotspot (1,1) · the pattern names | It documents **System 7 (1992)**, not 1984–88 — some statements describe things that didn't exist (zoom boxes everywhere, colour frames, Application menu). Stops short of WDEF-drawn geometry: no close box size, no stripe positions, no icon grid. WebFetch can't read these; you must download and convert. |
| **Executor** (autc04/executor, `src/wind/*.map`, `src/ctl/*.map` as human-readable ASCII bitmaps) | The six stripe positions · 11×11 close/zoom boxes in 13×13 cells · left+8 and right−21 offsets · two-overlapping-squares grow glyph (7×7 at col2/row3, 9×9 at col4/row5) · 16×16 scroll arrow (triangle rows 3–8 widening 2/4/6/8/10/12, then a 6px stem 4 rows tall) · plain 16×16 thumb · `FrameRoundRect(&r,10,10)` · `rDocProc` curvature table `{4,6,8,10,12,20,24}` · exact `InitGraf` pattern bytes and arrow cursor hex | **GPL.** The geometry facts aren't copyrightable, but do not paste `.map` files or drawing code into the page. It is a reimplementation — assume one pixel of possible error, especially the close box's horizontal offset (8 or 9 depending on how you count). |
| **1992 HIG** (vintageapple.org, 4.2 MB) | The *reasoning*, not just numbers — the whole 1-bit icon design section: 1px outline, minimise black because the Finder selects by **inverting**, substitute 50% gray for mid tones. Source of "racing stripes". Default button "an additional border of three black pixels, separated by a border of one white pixel". | 1992 = System 7 with colour, and it explicitly tells you to prefer "true gray" over the 50% pattern — the opposite of what a 1984 shell wants. You must read it backwards. Text extraction noisy near figures. |
| **Infinite Mac / Mini vMac + System 6.0.8** | The only way to settle what nobody wrote down: **the Finder's icon-grid spacing (Clean Up snap) is not documented anywhere** — most recreations assume a 64-wide cell and that is a guess. Also the I-beam/watch/cross/plus hotspots, only the arrow's (1,1) is published. | You are measuring Apple's shipped artwork — extract **metrics**, never bitmaps. Emulator scaling lies: capture at exactly 1:1 or every number is off by a fraction. Mini vMac needs a Mac Plus ROM, which is Apple's. |
| **system.css** (MIT) | Fastest way to see the whole vocabulary assembled; MIT means you can lift techniques freely. Good cross-check. | **Not pixel-true.** Sizes in rem/em with fractional values (title bar 1.5rem, scrollbar 22 px, arrows 23.38 px), renders the six lines as a CSS gradient rather than six 1px rules at documented positions — it will fight "integer scales only" the moment a viewer changes base font size. **Bundles ChicagoFLF and a "Monaco" whose provenance is unstated** → see §UNCONFIRMED. Read it, don't install it. |
| **98.css** (MIT) | Wrong era, right technique: `border-image` with tiny inline SVG/data-URI slices to get pixel-exact bevels that survive arbitrary box sizes — exactly how you stretch a 6-stripe title bar to any window width without a fractional pixel. | Windows, colour, bevelled — every visual decision is the opposite of 1-bit Mac. Nothing to copy directly, only a method. Irrelevant if the shell is canvas. |

**The one real conflict, resolved:** Executor builds the frame as `SetRect(left−1, top−19, right+1, top)` → **19 rows of bar**. The 1992 HIG says "at least 19 pixels high". Inside Macintosh says "the title bar is 20 pixels high". Both are Apple's own words. **Build it as 19 px of bar + 1 px black rule = 20 px of offset from structure top to content top. Do not build a 20-row striped bar.**

**The six lines, exact:** black 1px rules at content-relative y = top−15, −13, −11, −9, −7, −5. Numbering the bar's rows 0–18 (row 0 = frame top rule): black on 4, 6, 8, 10, 12, 14; white on 5, 7, 9, 11, 13; three white above (1–3), three white below (15–17); row 18 = the black rule under the bar. Striped band **exactly 11 px tall**. Whole bar reads 1 black / 3 white / 11 striped / 3 white / 1 black = 19. Title in Chicago 12, centred, baseline row 14, with **6 px of white padding either side of the string punched through the stripes**. Inactive = stripes erased, close box erased, zoom box erased, size box erased — only the 1px outline and the centred title survive. In 1-bit there is no greying; **that absence of detail IS the inactive state**.

**What I would pick and why:** Inside Macintosh as the authority, Executor as the ruler, and one afternoon in Infinite Mac at exactly 1:1 to settle the four things neither wrote down (icon grid spacing, the three unpublished cursor hotspots, the ±1px close-box offset, and whether the System 6 menu bar had rounded top corners — a claim I found no source for and would not build on). That is thirty minutes of measurement that converts the entire low-confidence list into numbers, and it is exactly the "measure one parameter at a time, never eye-adjust" discipline this project already runs on. Read system.css for structure, strip its fonts, and ship neither its CSS nor Executor's code.

---

## D15. The seven document icons

- **Draw your own 32×32 ICN#-style set.** 1px black outline, as few black pixels inside as possible (the Finder selects by inverting, so a mostly-black icon looks identical selected and unselected), 50% gray where a colour version would use a mid tone, silhouette-first — two icons of different type must differ **at 32×32 in outline alone**. Hand-draw the 16×16 too; the Finder's algorithmic reduction looks bad. Plus an inverted variant for selection. Whole set as indexed PNG: **under 4 KB.** *Downside:* real hand labour, and 32×32 1-bit punishes any shape not resolved at that size. Needs discipline held across seven icons — consistent outline weight, light direction, black budget — exactly the thing that drifts if you draw them on different days.
- **Kenney 1-Bit Pack (CC0).** ~1000 16×16 one-bit tiles, public domain, no attribution. *Downside:* it's a game-asset pack — swords, chests, dungeon tiles. No folder, no system suitcase, no floppy in the Macintosh idiom, and the drawing language is NES-ish (chunkier, outline-heavy, different silhouette logic). 16×16 doesn't scale into a 32×32 slot. Realistically you'd use two or three tiles.
- **Pixelarticons (MIT).** ~480 icons on a 24×24 grid, SVG + webfont, includes file/folder/floppy/trash/window. *Downside:* **24 doesn't divide into 32**, so nothing lines up and nothing scales by an integer. Modern flat-pixel style — thin uniform strokes, no mask, no inversion behaviour — won't sit beside a Kare-derived window frame.
- **Kenney Isometric Tiles City (CC0)** — for the world map, as a *measuring* reference only: read the real anchor offsets, footprint conventions, gutter, and building-height-to-tile-width proportions professionals use, instead of guessing. *Downside:* you cannot ship any of it — full-colour, wrong style, and mostly rendered-3D-to-sprite rather than hand-drawn pixel art, so it's the wrong reference for pixel *craft* specifically.

**Icon labels:** Geneva 9, centred under the icon on a white rectangle. Selected inverts **both** the bitmap (inside its mask) and the label box.

**What I would pick and why:** draw all seven yourself. No free set contains "XTIX growth dossier" or "MEDCOIN", the whole point of the shell is that 1984 renders 2026 content, and at under 4 KB it is the cheapest thing in the project while removing every licence question at once. Draw all seven in one sitting with the black-pixel budget written on the wall — the drift risk is entirely a scheduling problem, so solve it by scheduling. Use Kenney's isometric pack for an hour of *measurement* on the world-map landmarks and then close it.

---

## D16. Cursors

**Hand-author as data-URI PNGs.** The arrow's exact bits are published in Inside Macintosh: Imaging With QuickDraw, Fig 8-2 — data `0000 4000 6000 7000 7800 7C00 7E00 7F00 7F80 7C00 6C00 4600 0600 0300 0300 0000`, mask `C000 E000 F000 F800 FC00 FE00 FF00 FF80 FFC0 FFE0 FE00 EF00 CF00 8780 0780 0380`, hotspot **(1,1)**. Render to 32×32 at 2× nearest-neighbour: `cursor: url(data:image/png;base64,…) 2 2, auto`. **The mask matters as much as the image — that 1px white keyline is the only reason a black arrow stays visible on the 50% grey desktop, and every lazy recreation drops it.** Other standard cursors are `CURS` resources with fixed IDs: iBeam=1, cross=2, plus=3, **watch=4** (the wristwatch is the era's wait cursor; the beachball doesn't exist yet).

**Downside:** browsers cap custom cursors around 32×32 (128×128 hard limit, anything over 32 unreliable) and will not nearest-neighbour a 16×16 up for you, so you must pre-scale and **double the hotspot to (2,2)**. The watch and I-beam bitmaps are **not** published — tracing them from a screenshot copies Apple's artwork, so draw equivalents. A custom cursor over the whole page is a real accessibility cost.

**What I would pick and why:** ship the published arrow, hand-draw a watch and an I-beam in the same idiom, and **scope the custom cursor to the desktop scene only** — it is the one place the fiction needs it, and a page-wide custom cursor on a portfolio a hiring manager is skimming is a net negative. Measure the three unpublished hotspots in Infinite Mac during the D14 session rather than assuming the watch is (8,8).

---

# PART E — SOUND

**Hardware, verified:** 8-bit mono PWM at **22,254.5 Hz** (15.6672 MHz / 704 pixel-times per line). Nyquist **11,127 Hz**, no reconstruction filter worth the name. Sound buffer **740 bytes** in high RAM (= 370 16-bit slots = one frame) plus a 740-byte alternate; the high byte of each slot is the audio sample and the low field is the 400K Sony's motor PWM `[CORR — "low BYTE" softened to "low field"; independent sources describe a 6-bit motor value, and the sole citation (thomasw.dev) returns 403 to automated fetch]`. **8 levels of analog attenuation plus a mute** — a 1984 volume change was a discrete step, so a period-correct slider has 8 detents, not 100. `[CORR — the "3 general-purpose VIA outputs" detail is unsourced; the 8 levels are confirmed]` `[CORR — "370 × 60.15 = the same number" doesn't close: 370 × 60.15 = 22,255.5. The true frame rate is 60.1474 Hz.]` `[CORR — 8-bit SNR is 6.02n + 1.76 = **49.9 dB**, not ~48]`

**The legal fact the whole sound section was built on, and it's wrong:** `[CORR]` Apple's registered sound mark is **US Reg. No. 4,257,783** (serial 85/663,397, filed 27 Jun 2012, registered 11 Dec 2012): *"a synthesizer playing a slightly flat, by approximately 30 cents, G flat/F sharp major chord"* — the Reekes-lineage chime in use since 1999. **Not** the 1987 Mac II C-major chord. So "avoid C major" and "600 Hz is safe because it isn't the C major chord" both defend against a mark that does not exist. What you actually avoid is a slightly-flat Gb/F# major triad with synth timbre. On the correct mark, Chime A (inharmonic, no triad at all) is the safest and Chime B is safer than claimed.

**And the "historically accurate" option isn't:** `[CORR]` folklore.org — the primary source — has Charlie Kellner filling the buffer with a square wave and then making *"successive passes on it, averaging adjacent samples until everything reached the same level,"* producing *"a pleasant, distinctive chiming quality."* Repeated neighbour-averaging is a low-pass; **the machine did not emit a square.** folklore.org states **no frequency at all** — the 600 Hz figure rests on one Wikipedia sentence that also misattributes sound generation to the 6522 VIA. Treat 600 Hz as plausible-unverified.

## D17. Boot chime

| Option | Recipe | Honest downside |
|---|---|---|
| **A — struck bar (inharmonic)** | 4 sines on free-free bar ratios 1 : 2.756 : 5.404 : 8.933 from 392 Hz (G4) → **392, 1080, 2118, 3502 Hz**, gains 1.0/0.55/0.30/0.18, **independent** T60s of 2.2 / 1.4 / 0.9 / 0.55 s, 2 ms attack. Strike: white noise → BP 3.2 kHz Q 1.2, 12 ms, decaying over 25 ms, 0.06. Total 2.4 s. | The differentiated decays are what separate real struck metal from four beeps — but inharmonic bells are the most over-used sound in modern UI since 2014 and it risks reading as a Slack ping. `[CORR — titled "brass plate" but built on BAR ratios; a bell's partials are ~0.5/1/1.2/1.5/2. These numbers are a glockenspiel.]` `[CORR — the four gains sum to 2.03 and all attack over the same 2 ms, so they're phase-coherent at onset: the bus sees ~0.9 plus the strike noise, ≈ −6.9 dBFS, at the edge of clipping, not the stated −12.]` |
| **B — four-tone arpeggio** | One PeriodicWave, odd harmonics 1/3/5/7/9 at 1, 0.33, 0.20, 0.14, 0.11. Voices at **261.6 / 392.0 / 523.3 / 784.0 Hz**, onsets 0 / 90 / 180 / 270 ms. Per note: 3 ms attack, 60 ms decay to 0.35 sustain, 400 ms release, all four left ringing. LP 6 kHz Q 0.7. Tail to silence 1.6 s. | An ascending arpeggio into a sustained stack is structurally the same gesture as both the Apple and Windows startup sounds — listeners recognise *shape* before pitch. 270 ms before the pad lands makes the boot feel slow. `[CORR — "1, 0.33, 0.20, 0.14, 0.11" is exactly 1/n, an ideal square truncated at the 9th, not a "soft" square.]` `[CORR — "exactly what a 256-byte wavetable holds" is wrong; 256 samples supports harmonics to the 128th. The real cap is the 22,254.5 Hz output rate: at 784 Hz that's 28.4 samples/cycle → the 14th harmonic.]` `[CORR — four voices sustaining at 0.35 sum to 1.4, clipped; the stated "peak 0.45" requires an unstated group gain of ~0.32.]` |
| **C — one tone, three octaves** | 220 / 440 / 880 Hz, gains 0.5 / 0.30 / 0.15, all 8 ms attack, 220 ms hold, 900 ms release, shared LP sweeping **6000 → 900 Hz** over 700 ms Q 0.7. Total 1.2 s. | Without pitch motion it can read flat or funereal, and **220 Hz is at or below what most laptop speakers reproduce**, so half the energy vanishes on the machines the audience uses. `[CORR — 0.5+0.30+0.15 = 0.95 on harmonically locked, phase-coherent voices vs a stated peak of 0.45: a factor-of-two error.]` |
| **D — power supply spin-up** | BP centre rising **120 → 900 Hz** over 900 ms, Q 8, gain 0→0.25→0 peaking at 600 ms. Under it: 50 Hz saw at 0.06 with a 4 Hz gain LFO. At 950 ms a 1.4 kHz square blip, 40 ms, gain 0.3. | Read by a large minority as "something is loading badly", and it's the generic web-whoosh cliché this project is avoiding. `[CORR — at 120 Hz with Q 8 the bandpass ENBW ≈ 24 Hz, so noise loses sqrt(24/24000) = 0.032 → **≈ −53 dBFS. The first half is inaudible.** And because ENBW scales with fc at fixed Q, the sweep gains ~9 dB purely from widening — an unintended crescendo on top of the intended envelope.]` `[CORR — breaks the doc's own 200 Hz floor with a 50 Hz saw.]` |
| **E — CRT degauss + flyback whine** | Thunk: 55 Hz sine swept **90 → 48 Hz** over 200 ms, 1 ms attack, 380 ms decay, plus a 6 ms noise burst LP 400 Hz. Whine: sustained sine at gain 0.006. | **`[CORR — FATAL]` The compact Mac's horizontal scan rate is 22,254.5 Hz, not 15.7 kHz — that's the NTSC *television* line rate. Pixel clock / pixels-per-line IS the line rate: 15.6672 MHz / 704 = 22,254.5, which is exactly why there's one audio sample per line.** As specified it is also unbuildable: under Engine A's 22,254.5 Hz render, 15.7 kHz exceeds the 11,127 Hz Nyquist and **folds back to 6,554.5 Hz** — an audible mid-treble whistle. At 44.1 kHz it aliases to 21,845 Hz. And gain 0.006 = −44.4 dBFS, −50.5 after master ≈ **25 dB SPL — at or below threshold**, so "actively painful" is off by ~60 dB. The whole objection paragraph evaluates a tone that will not exist. `[CORR — labelled "55 Hz sine" then specified as swept 90→48; the 55 is meaningless.]` |
| **F — the "historically accurate" 600 Hz beep** | 600 Hz band-limited PeriodicWave (odd harmonics 1–9 at 1/n), 4 ms attack, 120 ms hold, 90 ms release, LP 3.5 kHz Q 0.5, peak 0.4. | `[CORR]` **Its entire pitch is "it is the truth", and it isn't.** The primary source describes an iterated low-pass, not a square; a square with 1/n odd harmonics is not "the actual documented waveform", and 600 Hz is uncorroborated. As a *sound* it's also a thin reward for the biggest interaction in the piece — one bleep after a scrolled prologue and a click on a rendered Macintosh. Only works if the disk sequence gives the boot a second act. |

**What I would pick and why:** Chime A, renamed honestly (struck bar, not bell or plate), with the four partial gains normalised so the coherent onset sum lands at 0.5 rather than 2.03 — that is a one-line fix and it is the difference between −12 dBFS and clipping. A is the right answer for the reason the research half-articulated and then undermined with the wrong trademark: it contains no triad at all, so it cannot collide with the actual registered mark (a slightly-flat Gb/F# major chord), while B and C are built from stacked fifths and octaves that at least *gesture* at one. The "Slack ping" risk is real and is managed by the differentiated decay rates — four partials with T60s of 2.2/1.4/0.9/0.55 s do not sound like a notification. Cut Chime E entirely, or keep only the 48–90 Hz degauss thunk: the flyback whine is at the wrong frequency, is unbuildable at the right one on either sample rate, and is inaudible at the specified gain.

---

## D18. Boot sequence timing

**Proposed:** chime at t=0 → 400 ms silence → insert clunk at 1.4 s → motor spin-up over 700 ms → five seeks at 2.20 / 2.34 / 2.51 / 2.66 / 2.80 s → motor ramps out over 400 ms → soft tick at 3.4 s as the desktop paints. Total 3.5 s, frame-matched to the boot animation.

`[CORR — the timeline does not close for any of the six chimes.]` "Chime at 0 → 400 ms silence → clunk at 1.4 s" implies a chime of **exactly 1.0 s**. None is: A = 2.4 s (the insert lands *inside* it, and 400 ms of silence is impossible), B = 1.6, C = 1.2 (→ insert at 1.6, not 1.4), D = 1.1, E unbounded, F = 0.214 (→ **1.19 s of dead air**, not 400 ms). The research's own recommended pairing was "C or F" — both wrong.

`[CORR]` Motor "ramping in over 700 ms" from t ≈ 1.66 s isn't at full level until **2.36 s, but the first seek fires at 2.20 s** — the drive seeks before it spins up.

`[CORR]` The five seeks are spaced **140/170/150/140 ms**, but DISK SEEK A specifies **12 ms** spacing with ±1.5 ms jitter. These are two different objects sharing one name, and the sequence's own jitter is ±20%, not the stated ±12%.

`[CORR]` Motor duration is capped at three different values in three places: **4 s** (recipe), **2 s** (recommended set), **3 s** (the WCAG rule).

**Honest downside of shipping the sequence at all:** 3.5 s of chained audio needs a stop mechanism and must be skippable, because on the second visit it is an obstacle. Every extra element is another thing that can land 40 ms wrong and break the illusion — a sequence is far harder to tune than a single event.

**What I would pick and why:** rebuild the timeline as offsets from the *end* of the chime rather than from t=0, so it survives changing the chime. Concretely: chime ends → 400 ms → insert (260 ms) → motor ramp-in 700 ms → **first seek at motor-full + 100 ms**, five seeks at 45 ms spacing (see D19 — 12 ms buzzes) → motor ramp-out 400 ms → desktop tick. Pick one motor cap and write it once: 2 s, which keeps the whole sequence comfortably under the 3 s WCAG line even though (see D22) 1.4.2 probably doesn't apply to a user-clicked power switch anyway. Belt and braces on the one number that has legal weight is cheap.

---

## D19. The mechanical family — key click, seek, disk

| Option | Recipe | Honest downside |
|---|---|---|
| **KEY CLICK A — two-layer dome** | L1 contact: white noise 6 ms, HP 1.8 kHz, gain 0.35, decay 8 ms. L2 case: 1-sample impulse → BP 2.6 kHz Q 6, 30 ms, gain 0.2. Randomise ±6% pitch, ±15% gain. 35 ms total. | `[CORR]` **L2 lands at ≈ −45 dBFS** (impulse through BPF peaks at gain × 2π·fc/(Q·fs) = 0.2 × 0.0567 = 0.0113) while L1 peaks at −15 dBFS. **The "case body resonance" — half the design idea — is 30 dB under the tick and will not be heard.** `[CORR]` The stated overlap warning is impossible: 8 keys/s = 125 ms between onsets vs a 35 ms event; overlap needs >28.6/s ≈ **340 WPM**. The prescribed mitigation (drop L2 under 120 ms spacing) fires at 4× the real threshold, and the 3-voice cap governs a case where at most one voice is ever live. |
| **KEY CLICK B — beam-spring clack** | Noise 3 ms HP 3 kHz gain 0.45 decay 6 ms; 90 Hz sine plate, 1 ms attack, 45 ms decay, 0.25; optional BP 1.1 kHz Q 9 ping at 0.12 over 60 ms. | An IBM Model F sound, not a Macintosh one — the 1984 keyboard was comparatively quiet. A period error anyone who owned one will hear immediately, and loud enough to be genuinely annoying. Breaks the 200 Hz floor at 90 Hz. |
| **KEY CLICK C — 1-bit tick** | A 2 ms buffer where exactly one sample is +0.8, rest 0, through LP 5 kHz Q 0.5, gain 0.25. | `[CORR]` ≈ −32 dBFS **for ~64 μs**; against the ear's ~200 ms integration window that's a further ~35 dB loudness penalty. Effectively nothing on laptop and phone drivers — or a digital pop users read as a glitch. Zero variation. |
| **KEY CLICK D — press/release pair** | Keydown as A; keyup same structure at BP 1.6 kHz, gain 0.18 (−6 dB), 18 ms decay. Suppress release if held >400 ms. | Doubles the event rate and every stacking problem. If the text is auto-typed, keyup timing is invented — double the CPU and annoyance for realism nobody can verify. |
| **DISK SEEK A — stepper chatter** | N = 4–9 steps by "distance". Each: 3 ms noise → BP 1.6 kHz Q 4 at 0.3, plus 220 Hz sine ping, 1 ms attack, 25 ms decay, 0.12. **Spaced 12 ms ± 1.5 ms.** | `[CORR — FATAL]` Auditory fusion happens at **20–30 Hz** (inter-onset below ~33–50 ms). 12 ms = 83.3 steps/s is **3× past it** — this will be heard as an 83 Hz tone, not chatter, with certainty rather than as a risk. The ±1.5 ms jitter is 12.5% FM of that tone: a warble, not a mechanism. |
| **DISK SEEK B — slow grind** | 6 steps at **45 ms**. Each: 15 ms noise → BP sweeping 1.1 kHz → 850 Hz, Q 2, gain 0.28, 2 ms attack, 10 ms release. | `[CORR]` **45 ms = 22 Hz, above the fusion threshold — this is the one that reads as discrete steps.** Its real downside is duration: 270 ms held before a UI response, and if the load is instant you're adding latency for atmosphere. `[CORR — "total 270 ms" counts 20 ms of trailing silence; onsets run 0–225, last burst + release ends at 250.]` |
| **DISK MOTOR** | Brown-ish noise `y[n] = y[n−1]·0.98 + w[n]·0.02` → LP 800 Hz Q 0.7, parallel BP **130 Hz Q 12**. Gain 0 → 0.06 over 700 ms, out over 400 ms. AM at 5.5 Hz, depth 12%. | `[CORR]` **5.5 Hz = 330 RPM. The 400K Sony ran 390–600 RPM = 6.5–10 Hz** — the chosen rate is below the drive's slowest zone, and it's the one number derivable from hardware. `[CORR]` The BP 130 Hz Q 12 path (3 dB BW 10.8 Hz, ENBW ≈ 17 Hz → sqrt(17/24000) = 0.027) sits **30–40 dB below** the parallel lowpassed noise — the resonance the recipe calls "what makes it a disk rather than a fan" is the quietest thing in it. `[CORR]` The 0.98 coefficient is a one-pole LP, not an integrator, and its corner is **sample-rate dependent**: 154 Hz at 48 k, 142 Hz at 44.1 k, **71.5 Hz at 22,254.5 Hz** — so the sound changes per device, and under Engine A it sits below the 200 Hz floor. The subsequent LP 800 Hz is redundant (already ~14 dB down there). Plus: sustained loops are the #1 cause of people muting a site. |
| **DISK INSERT** | 0–120 ms: noise → BP 2.2 kHz Q 1.5, gain 0.05 → 0.22 (slide). 130 ms: snap — 4 ms noise, HP 4 kHz, 0.5, decay 8 ms. 150 ms: clunk — 140 Hz sine, 1 ms attack, 90 ms decay, 0.3, plus 60 ms noise LP 300 Hz at 0.15. 260 ms total. | Three layers is three chances to sound like a dropped cardboard box. The gaps are load-bearing to within ~20 ms, so this needs several rounds of ear-tuning. Breaks the 200 Hz floor at 140 Hz. |
| **DISK EJECT** | Motor 0.06 → 0 over 250 ms while its resonance sweeps **130 → 90 Hz**. 260 ms: spring pop — 280 Hz sine, 1 ms attack, 60 ms decay, 0.3, plus 3 ms HP noise at 0.35. 300–390 ms: slide out, BP 2.2 kHz Q 1.5, 0.2 → 0. ~400 ms. | 400 ms on a "go back" action means the reader is often already elsewhere while it's still playing — must be interruptible. If the visual close is 200 ms the sound floats free of the picture and the illusion dies. |

**The 200 Hz floor is the document's own headline rule and six recipes break it:** Chime D (50 Hz), Chime E (48–90), Key Click B (90), Insert (140), Motor (130, and 130→90 on eject), Error B (150 + 75), Error C (110). `[CORR — the recommended default set was precisely the combination that breaks it hardest.]`

**What I would pick and why:** Key Click A with L2's gain raised ~30 dB to actually reach the mix (or dropped entirely — as specified it is paying CPU for silence), Seek **B** at 45 ms as the default rather than the exception, insert/eject kept, and the motor loop **cut**. Seek A is not a tuning risk, it is arithmetically a buzz, and the research recommended it as default and B as the rare case — that is backwards for the ear even though 12 ms is a plausible real track-to-track time. The motor goes because it is the single largest mute-the-site risk, it breaks the 200 Hz floor, its defining resonance is 30–40 dB under its own noise bed, and its brown-noise corner changes with the visitor's sample rate. Insert-snap-clunk into silence into seeks reads as a machine perfectly well without a loop underneath it.

---

## D20. The UI family — window, icon, error, tick

| Option | Recipe | Honest downside |
|---|---|---|
| **WINDOW A — zoom-rect glide** | Open: odd-harmonic 1–5 PeriodicWave, exponential glide **320 → 660 Hz** over 60 ms, 3 ms attack / 25 ms release, peak 0.12, LP 4 kHz, then a 2 ms tick. Close: **660 → 300 Hz** over 50 ms, peak 0.09. | Rising glides are cartoon vocabulary — possibly too playful for a portfolio aimed at commercial leadership roles, and the option most likely to feel dated in two years. `[CORR — 0.09/0.12 = −2.5 dB, not the stated −3; and "the same reversed" would be 660→320, not 300.]` |
| **WINDOW B — two-tick shutter** | Open: two noise ticks 45 ms apart — BP 1.8 kHz Q 3 (3 ms, 0.18) then BP 1.2 kHz Q 3 (3 ms, 0.14). Close: one tick, BP 1.4 kHz, 0.15. No pitched content. | So restrained a meaningful share of readers won't consciously register feedback at all. Open and close get almost the same identity, so the shell loses a little legibility. |
| **WINDOW C — paper handling** | Open: 180 ms noise → BP 3.5 kHz Q 0.8 with a **3-bump randomised** envelope (30–50 ms each, peaks 0.05–0.09). Close: 120 ms, BP 2.4 kHz, 2 bumps, 0.06. | Pulls the shell toward "desk simulator" rather than "machine", and fights the disk vocabulary — a document cannot credibly be both a sheet of paper and a floppy disk in the same 90 seconds. |
| **ICON SELECT** | 1 ms noise HP 2 kHz at 0.18 + 900 Hz sine at 0.06, 18 ms with 15 ms release. Each further selection within 400 ms transposes the sine **+1 semitone (×1.0595)**, capped at +4, resetting after 400 ms. | Charming on the first pass, gimmicky by the tenth, and it implies a musical intent the rest of the shell doesn't have. Only works for keyboard nav — a mouse crossing icons quickly triggers a chromatic run that sounds accidental. |
| **ICON OPEN** | Two ticks 70 ms apart, second **+5 semitones (×1.335, a perfect fourth)** and 2 dB quieter; seek begins 40 ms after. Suppress the plain select on double-click via a 250 ms window so the gesture produces 2 sounds, not 4. | The suppression logic is the most bug-prone thing in the audio layer — a wrong window either double-fires or swallows the select on single clicks. Also 110 ms of sound before the seek even starts. |
| **ERROR A — two-note fall** | **440 Hz** 90 ms, 20 ms gap, **330 Hz** 90 ms. Odd-harmonic square, LP 2.5 kHz Q 0.7, 4 ms attack / 30 ms release, peak 0.22. | `[CORR]` **440→330 is a descending perfect FOURTH (4.98 semitones), not a major third.** A falling fourth reads neutral or bugle-call, not negation — the recognised "uh-oh" figure is the minor/major third. A major third down from 440 is **349.2 Hz**. Fix the frequency or drop the "universally read as no" claim. (The doc names 1.335 correctly as a fourth four entries later.) Also clichéd, and mildly scolding when the only "errors" are dead-end clicks. `[CORR — audible length is 230 ms with releases, not 200.]` |
| **ERROR B — dull thud** | 150 Hz + 75 Hz sines at 0.3 / 0.18, 1 ms attack, 120 ms decay, LP 500 Hz Q 0.7, plus 8 ms noise LP 800 Hz at 0.15. | **All energy below 500 Hz — exactly where laptop and phone speakers have nothing.** On a MacBook Air it degrades to a faint "tk" or actual silence, the worst possible failure for an error sound. Needs a 1.2 kHz click layer as insurance, which dilutes the idea. Breaks the 200 Hz floor twice. |
| **ERROR C — buzzer** | 110 Hz saw → WaveShaper (tanh, drive 4, 4096-point, oversample '2x') → BP 700 Hz Q 3, gated by a 25 Hz square LFO = 5 pulses over 200 ms. Peak 0.25. | Genuinely unpleasant — correct for a real failure, wrong for a portfolio where a curious visitor should never be punished. `[CORR — the 25 Hz square LFO produces 10 instantaneous gain edges, violating the doc's own "never set gain instantaneously" rule; an OscillatorNode into `gain.gain` ADDS and swings −1..+1, so it inverts rather than mutes without an offset; and tanh drive 4 on a 110 Hz saw at '2x' will alias — '4x' is available.]` |
| **ERROR D — single low beep** | 220 Hz odd-harmonic 1–7 square, 260 ms, 5 ms attack, 40 ms release, LP 2 kHz, peak 0.18. | A lone low beep from a web page is what browsers and OSes use for real system alerts — some readers will think something outside the page broke. Least informative: no shape, so no meaning beyond "noise happened". `[CORR — "deliberately 6 dB below the ordinary UI sounds" is actually −1.74 dB vs Error A and −2.85 vs the window trim. 6 dB below 0.22 is 0.11.]` |
| **TICK A — sine pip** | 2000 Hz sine, 1 ms attack, exponential to 0.001 over 22 ms, gain 0.05. | Smartwatch/2020s vocabulary with no relationship to 1984 hardware — an 8-bit PWM machine could not produce a clean 2 kHz sine at −32 dBFS. In a period-fidelity shell it's the sound most likely to break the illusion for someone who knows. |
| **TICK B — filtered impulse** | 1-sample impulse → BP 4 kHz Q 3, 12 ms, peak 0.08, filter freq randomised ±8%. | `[CORR]` **Actual output ≈ −43 dBFS** (0.08 × 2π·4000/(3·48000) = 0.0140, ×0.5 master), against a stated slot of −28 dBFS — **15 dB short, i.e. inaudible on a laptop.** The doc worries it will be piercing; the arithmetic says silent. 4 kHz is also where speech consonants live, so at high volume it can mask screen-reader output — drop to 2.8 kHz if assistive tech matters. |
| **TICK C — hover whisper** | 8 ms white noise, HP 5 kHz, **4 ms attack** (no transient), 4 ms release, peak 0.025. Debounce 60 ms, fire only on hover-target identity change. | On laptop speakers at moderate volume it is likely literally inaudible, so all the effort produces nothing for most of the audience. Without the debounce and change-guard, a mouse crossing seven icons is a hiss storm; with them it may fire so rarely it seems broken. |

**What I would pick and why:** Window B, Icon Select + Icon Open, Error A **at 349.2 Hz** so the interval is actually the falling third the justification depends on, and Tick B at 2.8 kHz **with its gain raised ~15 dB** to reach its stated slot. Window B wins because it is the only one you can trigger twenty times without thinking about it, which is the correct test for the most-repeated sound in the shell — and its "invisible craft" downside is the acceptable one. Error B goes: it fails the 200 Hz period rule and the laptop-speaker reality simultaneously, and an error sound that is silent on the audience's hardware is worse than no error sound. Cut Error C — build it, discover nothing in the shell deserves it, delete it.

---

## D21. Gain architecture — the decision the recipes silently contradict

`[CORR — this is the most consequential arithmetic failure in the sound research, and it invalidates every dBFS annotation in it.]`

**Two incompatible stages are specified.** The recipes' dBFS labels assume `event gain × 0.5 master` and nothing else — and on that reading they check out: Tick A 0.05 × 0.5 = 0.025 = **−32.0 dBFS** ✓, Error A 0.22 × 0.5 = **−19.2** ✓, chime 0.5 × 0.5 = **−12.0** ✓. But MIX then adds per-category trims feeding the master (chime 0.50, insert/eject 0.30, error 0.35, window 0.25, icon 0.22, key click 0.18, tick 0.10). Apply both and everything drops 6–20 dB: chime → **−18** (not −12), key click → **−30** (not −22), Tick A → **0.0025 = −52 dBFS**. Key Click A is wrong under *both* readings (−15 without trims, −30 with; its two layers summing at 0.55 would peak at **−11 dBFS — as loud as the boot chime, during typing**). Seek A's "≈ −20" is **−13.6** by peak.

**And filter loss is never computed anywhere.** Noise through a bandpass loses `sqrt(ENBW / Nyquist)`; a unit impulse through a bandpass peaks at `≈ 2π·fc/(Q·fs)`. Run against the stated numbers at 48 kHz post-master: Tick B → **−43** (target −28) · Key Click A L2 → **−45** (L1 −15) · Motor's 130 Hz resonance → **30–40 dB** under its own bed · Chime D at 120 Hz → **−53**. Net: **every oscillator sound lands near or above target and every noise/impulse sound lands 15–45 dB under.** That is not a mix with a gain ladder — it is loud beeps and silence. It also destroys the "shared sonic material" argument, because the members of that family are exactly the ones that vanish.

- **Fixed gain ladder, no dynamics.** Deterministic, debuggable, zero added latency, zero pumping. *Downside:* no single set of numbers survives every device — laptop speakers apply their own loudness compression that squashes the chime-to-tick ratio, and headphones invert it. There is no fix, only a compromise tuned on the audience's likely machines.
- **DynamicsCompressorNode as a safety limiter** (threshold −10 dB, knee 0, ratio 20, attack 0.003, release 0.25). *Downside:* it breathes — a loud chime audibly ducks a tick landing on top of it, which sounds like a mistake rather than a mix. The 3 ms attack lets exactly the transients you were worried about through anyway, and Chrome's implementation adds lookahead latency to **every** sound in the shell.

**Working targets, unchanged and still right:** chime ≈ **−12 dBFS**, ordinary UI **−18 to −24**, hover/tick **−28 to −34**. `[CORR — "if it is comfortable at 25% system volume it will not injure anyone at 100%" does not follow for the case that matters: headphones, where full scale can exceed 110 dB SPL and a −12 dBFS chime lands near 100 dB. macOS and Windows volume curves also differ by well over 10 dB at the same slider position, so "25%" is not a test.]`

**What I would pick and why:** one stage, not two — delete the recipe-level dBFS annotations, keep the category trims as the single source of truth, and then **re-derive every event's node gain by measuring the actual output** with an `OfflineAudioContext` render and a peak scan. That is the method the research prescribed and is the one thing guaranteed to contradict its own published numbers, which is precisely why it should be run first. No compressor: for material this quiet, a hard gain budget plus a voice cap does the same job with none of the breathing, and the 3 ms attack doesn't catch what you'd want it for. Test on headphones, not at 25% laptop volume.

---

## D22. Engine, grain, and the unlock gate

**ENGINE A — pre-render every event with `OfflineAudioContext` at 22,254.5 Hz.** *Downside:* everything is frozen at render time, so variation beyond `playbackRate` needs pre-rendered variants. `[CORR — the constructor as written passes a non-integer length: 2.4 × 22254.5 = 53410.8, truncated by WebIDL. Round it.]` `[CORR — "real fold-back" does not occur for oscillator sounds: Web Audio band-limits PeriodicWave output, so you get a clean tone with an 11.1 kHz Nyquist. Only the noise buffers and the WaveShaper actually alias. If genuine fold-back is the selling point, write the waveform sample-by-sample into an AudioBuffer.]` `[CORR — the sample-and-hold stair-step, the direct consequence of "no reconstruction filter" and the machine's real signature, is exactly what a resampler removes. AudioBufferSourceNode interpolates; it does not zero-order-hold. You'd need ZOH upsampling or an AudioWorklet.]` `[CORR — playbackRate 0.94–1.06 shifts the effective rate to 20,919–23,590 Hz, moving the fold-back point with every "variation".]` `[CORR — unstated RAM: ~4.5 s of mono Float32 at 22,254.5 Hz = 89 KB/s → ~400 KB resident, more with variants. "Zero impact on the budget" is true for download only.]`

**ENGINE B — live graph per event**, voice cap 8, drop oldest, hover ticks throttled to one per 60 ms. *Downside:* a mouse dragged across a grid can request hundreds of node graphs per second; without the cap that's real jank, and node churn causes GC pauses that show up as dropped frames in the isometric renderer — the one thing this project cannot afford.

**GRAIN — 8-bit quantiser** (`x → round(x·127.5)/127.5`, 4096-point WaveShaper, `oversample:'none'`). *Downside:* quantisation noise is proportionally loudest at low signal levels, so every quiet decay tail hisses. `[CORR — and it is in the wrong place. Step = 1/127.5 = 0.00784, so a 0.025-peak tick spans **3.2 steps — under 3 bits**, a square-ish buzz. Tick C at 0.025 and Tick B at its true −43 dBFS would be annihilated. On the real machine, 8-bit quantisation happened at the DAC's full scale and the 3-bit attenuator reduced level *after* it — quiet sounds were not low-resolution. Put the quantiser inside the per-event render at unity, before any trim.]` `[CORR — the curve reaches 128/127.5 = 1.0039, overshooting unity; and a 4096-point curve is linearly interpolated (16 points per 256-level plateau), so the staircase is approximate.]`

**GATE 1 — lazy context on first gesture.** *Downside:* constructing a context takes real time (ms on desktop, occasionally 100 ms+ on low-end Android). If the gate gesture IS the boot click, the most important sound in the piece is the one that's late.
**GATE 2 — construct early, resume on first gesture.** *Downside:* `[CORR — misattributed. Chrome's guidance actually describes auto-resume: "An AudioContext will be resumed automatically when... the user has interacted with a page [and] the start() method of a source node is called." It does not describe constructing early and pre-rendering while suspended, and "OfflineAudioContext rendering is not gated" carries no citation — verify before building on it.]` `[CORR — the "6 contexts per page" cap was removed in Chrome 66, eight years ago. Use one context anyway, for the right reasons: one clock, one master gain, one suspend/resume path.]`
**GATE 3 — explicit period-correct "Sound" checkbox in the prologue.** *Downside:* puts a decision in front of the reader before they have any reason to care; unchecked-by-default means most never turn it on, so the whole layer is built for a minority.
**GATE 4 — the power switch IS the gate.** *Downside:* if the tab is muted, OS volume is down, or iOS's ring switch is off, the single biggest moment passes in silence and they never learn there was anything to hear. The visible 8-step indicator is mandatory, not optional.

**Browser rules, corrected:** activation-triggering events are `keydown` (excluding Escape and browser-reserved keys), `mousedown`, `pointerdown` (pointerType 'mouse'), `pointerup` (non-mouse), `touchend` — **not** mousemove, wheel, scroll, touchmove, focus or any programmatic dispatch. Chrome's autoplay policy hit Web Audio in **Chrome 71** `[CORR from 70]`; MEI needs >7 s of audible media on the origin. **WebKit 237322 is RESOLVED, not "open for years"** `[CORR]` — on iOS 17+ set `navigator.audioSession.type = 'playback'`; the silent-`<audio>` trick is now the *legacy* fallback for pre-17. The Audio Session API is a **W3C Working Draft (13 Nov 2024)** `[CORR from "editor's draft"]` and its default type is **'auto'**, not 'ambient' `[CORR]`.

**The unlock skeleton has a permanent-failure bug** `[CORR]` — and it was billed as "the only code worth writing down exactly":
```js
// BROKEN: {once:true} + an Escape keydown = silent, permanent audio death.
// Escape does not confer activation, but the once:true listener is consumed anyway
// and never re-registers. Re-arm until ctx.state === 'running':
const unlock = async () => {
  try { await ctx.resume(); } catch {}
  try { await silentAudioEl.play(); } catch {}          // must be a data: URI WAV under zero-external-requests
  if (navigator.audioSession) navigator.audioSession.type = 'playback';
  if (ctx.state === 'running') detachAll();             // only NOW remove the listeners
};
```
Also: `exponentialRampToValueAtTime` cannot **start** from 0 either (RangeError / implementation-defined jump), and every one of the ~25 envelopes begins at zero — use `linearRamp` for attacks. The doc states the target-zero rule and not the source-zero rule. And the `visibilitychange` handler calls `ctx.resume()` unconditionally, which rejects if the user never unlocked.

`[CORR]` Budget: 4–7 KB minified is ~2× optimistic. The recommended set is 13–14 sounds plus a sequencer, voice pool, offline pre-render path, live path, 8-step volume, mute/suspend and localStorage — realistically **10–15 KB minified, 4–5 KB gzipped**. Still free against any budget; just not the stated number.

**What I would pick and why:** Engine A for fixed sounds, Engine B for the pitch-stepping select, quantiser **inside the per-event render at unity** rather than on the master, and Gate 4 with Gate 2's early construct underneath so the chime has no warm-up latency — but write the re-arming unlock, not the `{once:true}` one, because that single flag turns one stray Escape keypress into a dead audio path for the session and it fails silently. Drop the claim that Engine A gives you authentic fold-back; it gives you a clean band-limited tone at a low sample rate, which is a different and less interesting thing, and if the grain is the point it has to come from the quantiser and hand-written buffers.

---

## D23. Audio defaults and accessibility

**There is no `prefers-reduced-sound`.** Media Queries Level 5 ships `prefers-reduced-motion`, `prefers-contrast`, `prefers-color-scheme`, `prefers-reduced-transparency`, `prefers-reduced-data`, `forced-colors`; `prefers-reduced-strobing` is only an open issue (csswg-drafts #8651). `[CORR — "none is under active discussion" is slightly too strong: csswg-drafts #9975 is open on ambient audio and UI sound effects. Operationally nothing changes — a visible persistent control is still the only mechanism.]`

**WCAG 2.x SC 1.4.2 Audio Control (Level A):** if audio plays **automatically** for more than **3 seconds**, a mechanism must exist to pause/stop it or control its volume independently of system volume. `[CORR — this probably does not apply here. Under Gate 4 the entire boot sequence is triggered by the reader clicking a power switch, and user-initiated audio is the standard example of what 1.4.2 does not cover. The research asserted flatly that it does and then built constraints on it — that is the one place it claimed certainty and overclaimed. Build the stop control anyway; it is right on the merits and the loop-surviving-a-route-change failure is a genuine defect.]`

- **Persistent mute in the menu bar, right-aligned** — a real `<button>` with `aria-pressed`, an accessible name that says "Sound on"/"Sound off" not just an icon, in the normal tab order, visible focus ring, localStorage. The right side of the menu bar is where the real Mac put its clock and menu extras **and** where every modern user already looks. *Downside:* a period-correct rendering is the thing that makes it hard to recognise as a mute control — it probably needs a modern speaker glyph inside the 1984 frame, which is a small compromise of the shell rule.
- **Default (a) OFF** with a visible "sound available" hint. *Downside:* most readers never hear a single sound you built.
- **Default (b) ON**, gesture-gated, nothing above −18 dBFS. *Downside:* the open-plan-office disaster; one bad first second can lose a reader entirely.
- **Default (c) inferred from `prefers-reduced-motion`.** *Downside:* **no specification blessing** — motion sensitivity is not sound sensitivity, and a reviewer can fairly call it an assumption about users.
- **Mute must actually mute:** master gain ramped to 0 over 30 ms **and then** `ctx.suspend()`; kill loops on mute, on `visibilitychange` to hidden, and on scene change. *Downside:* suspending means the first sound after unmute pays resume latency again, and an abrupt loop kill clicks unless it too gets a 30 ms ramp — the stop path needs the same envelope care as the start path, which is the bit everyone forgets.

**What I would pick and why:** default **off**, menu-bar-right toggle with a modern speaker glyph inside a period-correct frame, localStorage override, everything killed on hide. Yes, that means most readers never hear it — and that is the correct trade for an audience of hiring managers who may open the tab in an open-plan office, where the downside is not "they miss a nice detail" but "they close the tab". Reject (c) outright: inferring sound preference from motion preference is an assumption dressed as an accommodation, and this is a portfolio being reviewed by people who may notice.

**One scope warning to say out loud:** "sound is the only part of this project that is free" is true for the *sound layer* — synthesis from arithmetic carries no font, palette, library or sample licence. It clears nothing else. Chicago, the Happy Mac and smiling-disk icons, the System 1 trade dress and the "Macintosh" word mark are all Apple's, and synthesising your own beeps does not touch them.

---

# PART F — RUNTIME

## D24. Renderer

| Option | Size | Honest downside |
|---|---|---|
| **A — single Canvas 2D, viewport-culled, painter's order.** One canvas, `imageSmoothingEnabled=false`, one `setTransform` per frame, sort visible list by x+y+z with a stable tiebreak, `drawImage` from one atlas. | **0** | Per-sprite tinting means either pre-baking every colour variant or a slow offscreen composite per sprite. Thousands of moving sprites bottleneck — raw Canvas sits well below Pixi at 10,000 sprites. Particle-scale effects later = a rewrite. |
| **B — A + chunked static pre-render.** Bake the immutable ground into offscreen canvases of 1024×1024 source px, blit the 2–6 chunks intersecting the viewport. | **0** | Memory arithmetic is unforgiving: a 64×64 map baked as ONE surface at scale 2 is 134M px, **8× over Safari's 16,777,216 cap — crashes the tab.** Any animating ground tile must be excluded and drawn per-frame, fragmenting the draw path. |
| **C — Pixi.js v8**, `scaleMode: NEAREST`, batched. | **~150 KB gzipped** | Larger than the entire sprite budget, and must be inlined to satisfy zero-external-requests. WebGL context loss needs explicit handling (Safari drops contexts on tab backgrounding and memory pressure). Shader compile hitch on first paint on low-end Android. **And the killer: NEAREST is necessary but not sufficient — a container transform on a fractional device pixel makes WebGL sample between texels and shimmer.** You inherit all of Canvas 2D's snapping discipline plus 150 KB. |
| **D — LittleJS.** WebGL2 + Canvas2D hybrid, no dependencies, starter builds to a **7 KB** zip with all primary features. MIT. | **7 KB** | Small community, thin docs, opinionated about the game loop and entity model in ways that may fight a three-scenes-one-renderer structure. You'd adopt someone's world-coordinate conventions on top of an isometric contract you've already fixed. Unclear how its camera handles integer-snap. |
| **E — DOM sprites with `translate3d`**, z-index = x+y+z, `image-rendering:pixelated`. | 0 | Falls apart above ~300–500 nodes on mobile. z-index with thousands of values creates stacking contexts browsers handle inconsistently. **Worst option for crispness: you cannot force the compositor to snap a transformed layer to whole device pixels**, so on a DPR-1.5 laptop sprites land half-off-grid with no recourse. |
| **F — hybrid: canvas world, DOM everything else.** Isometric scenes to canvas; all text, labels, chrome, escape hatch and the desktop scene as real DOM. Nine tokens defined once as CSS custom properties, read at startup via `getComputedStyle` into the canvas code. | 0 | **Two coordinate systems that must stay in sync** — a DOM label anchored to a world tile needs the forward projection recomputed on every camera move, and CSS transforms are in CSS px while the canvas thinks in source px × S × P. Getting a DOM label to sit *exactly* on a canvas sprite across all DPRs is genuinely annoying; budget a day. |

**Frame budget:** 60 fps = 16.67 ms, and you don't get all of it — on a mid-range 2021 Android assume ~8 ms for JS/layout and ~6 ms for compositing. A 64×64 map is **4096 ground tiles**; naive per-frame `drawImage` of all of them is 4–9 ms on that phone before a single prop. **Culling to the viewport is the baseline, not an optimisation.** At 16×16 you're at ~256 ground + ~40 path + 4 landmarks + ~20 props ≈ **320 drawImage calls**, which is nothing — and the whole static ground+path layer can pre-bake into one blit.

**Scale sanity:** 16×16 renders to 1024×512 at 1×, 2048×1024 at 2×. A 24×24 map is 1472×736 at 1×, already too wide for any viewport at 2×. **Use 16×16 or 20×20 at 1×, and reserve 2× for a zoomed detail state.**

**What I would pick and why:** F with B underneath — canvas for the two isometric scenes with the ground pre-baked into 1024×1024 chunks, real DOM for the desktop scene and for every piece of text anywhere. The desktop scene is a flat, axis-aligned, rectangular 1984 UI, which is precisely what HTML and CSS are natively good at, and Poolsuite and Windows96 both prove DOM is sufficient there. More importantly: on a job-search portfolio, the case-study copy being real selectable text that Google indexes and a screen reader can read is not a nice-to-have. Pixi's 150 KB buys headroom for sprite counts you will never approach while still requiring every bit of the integer-snap discipline Canvas 2D needs. The one-day cost of syncing DOM labels to canvas sprites is the price and it is worth paying.

---

## D25. Crispness / DPR

**The rule, as code:**
```js
const S = 2;                                   // world scale
const D = devicePixelRatio;
const P = Math.max(1, Math.floor(D));          // integer backing-store multiplier
canvas.width  = Math.round(cssW * P);
canvas.height = Math.round(cssH * P);
canvas.style.width = cssW + 'px';
ctx.setTransform(S*P, 0, 0, S*P,
                 Math.round(camX * S * P),     // the half everyone forgets
                 Math.round(camY * S * P));
ctx.imageSmoothingEnabled = false;
// NEVER ctx.scale(D, D) with fractional D
```
**Integer magnification is the product, not the factor:** one source pixel occupies S × P device pixels. At DPR 3 with S=2 that's 6 device pixels — still integer, still crisp. `S*P` must be whole; `D` need not be.

**Downside of the snap:** it quantises scroll motion. At DPR 3 / S=2 the camera moves in 1/6-source-pixel steps (smooth); at DPR 1 / S=1 it moves in whole source pixels, which on a slow parallax pan reads as visible stepping. That is the right trade here, but it is a real one.

**The fractional-DPR desktop is the norm, not an edge case** — Windows at 125/150/175% scaling, plus browser zoom on top, is roughly half your desktop visitors.
- **(a) `P = round(D)`, let the browser do one final resample**, `image-rendering:auto` so it's a uniform bilinear softening rather than uneven pixel doubling. *Downside:* your pixel art is slightly soft on exactly the machines a hiring manager uses.
- **(b) Constrain canvas CSS width/height so `cssW * D` is a whole number** — at D=1.5, only even CSS widths — quantised in a `ResizeObserver`, remainder letterboxed with `--bg`. *Downside:* the canvas size is no longer the container size, so layout must tolerate a few px of slack on every resize, and letterboxing can look like a bug.
- **`devicePixelContentBox`** solves all of it in one API (`observer.observe(canvas, {box:['device-pixel-content-box']})`, callback fires before paint). *Downside:* **Safari does not support it** — Chrome/Edge 84+, Firefox 108+, and WebKit still hasn't implemented it. Your reader may well be on a Mac, so you write the fallback anyway, which means you've written both. Feature-detect, treat as a bonus.
- **Two-stage upscale** — render everything at scale 1 into an offscreen canvas, blit once at integer scale. *Downside:* one extra full-frame copy per frame (on a 1290×2796 iPhone backing store that's real bandwidth), it caps effective resolution so overlaid DOM text is crisp while the canvas beneath is 1×-upscaled (jarring mismatch), and the offscreen is a second large surface against the iOS canvas memory cap.

**Second-order:** Chrome positions text at subpixel x-offsets, so even with a legal k a glyph origin at x=100.5 blurs. Keep text left-aligned at integer padding; avoid flex-centring that produces .5px offsets; never put a fractional transform on a text element. Browser zoom breaks all of it and there is no fix.

**What I would pick and why:** the integer rule above as the foundation, plus option (b) — quantise the canvas CSS size in a `ResizeObserver` and letterbox the slack with `--bg`. Roughly half the desktop audience is on fractional DPR, and option (a) makes the art soft on precisely those machines, which undercuts the only thing the aesthetic is trading on. Letterboxing a few pixels is a visible-but-explicable compromise; a soft pixel grid is not. Build the debug overlay first — printing `devicePixelRatio`, `canvas.width`, `canvas.style.width`, computed `S*P` and the camera offset in device pixels — and change one parameter at a time.

---

## D26. Hit testing

**The exact inverse of your projection at z=0:** `x = sx/64 + sy/32`, `y = sy/32 − sx/64`, then floor both. (Check: x=1,y=0 → sx=32, sy=16; back out 32/64+16/32 = 1 and 16/32−32/64 = 0. ✓) Subtract any half-tile anchor offset **before** inverting.

**The z-ambiguity is one-parameter, not unsolvable.** Let `u = sx/32` (= x−y, fixed by the click) and `v = sy/16` (= x+y−z, fixed by the click). For any candidate height z: `x = (u+v+z)/2`, `y = (v+z−u)/2`. A screen point is a *line* through the world — walk it.

| Option | Cost | Honest downside |
|---|---|---|
| **1 — inverse projection to ground tile** | O(1), zero memory | **Only correct at z=0.** Any prop drawn taller than its tile reports the tile *behind* it when you click its upper body. Necessary but never sufficient. |
| **2 — height-map ray march** — iterate z from max stack down to 0, compute the candidate tile, return the first that holds geometry. 4–8 iterations. | ~free | Requires an occupancy structure keyed by (x,y,z) kept in sync whenever anything moves. Resolves to **tiles, not sprites** — a decorative prop overhanging its cell is still wrong. |
| **3 — reverse painter walk + 1-bit alpha mask.** Walk the frame's sorted list front-to-back; for each entry whose bbox contains the point, read that pixel's alpha; first non-transparent wins. Mask built **once at load** from a single `getImageData` over the atlas — a 2048×2048 atlas is **512 KB of RAM as a bitmask, zero extra download**. Typical cost: <10 bbox tests + one bit lookup. | ~free after load | The one-time `getImageData` is a **synchronous main-thread stall of 10–30 ms** — do it during the prologue scroll, never on first interaction. The scratch canvas needs `{willReadFrequently:true}` or the readback forces a GPU sync. A cross-origin-tainted canvas throws on `getImageData`, so the atlas must be same-origin or a data URI. |
| **4 — colour-ID picking buffer.** Second offscreen canvas, each entity as a unique flat RGB stencilled through its own alpha (`globalCompositeOperation:'source-in'`), read one pixel. 24-bit = 16.7M IDs. | 0 bytes, real memory | **A second full-size canvas doubles canvas memory** — at DPR 3 that's another 14 MB against iOS's cap. Every `getImageData` is a potential GPU→CPU sync stall; call it on pointermove naively and you drop frames. Invalidates on every camera move, which for a scroll-driven site is constantly. |
| **5 — anchor-and-footprint registry.** Declare each prop's footprint and clickable rect in atlas metadata rather than deriving it. Lets you make a small icon easier to click than its pixels suggest — **the recommended minimum touch target is 44 CSS px and an authentic 32×32 Mac icon at scale 1 is well under that.** | 0 | Every new sprite needs hand-authored metadata that drifts out of sync the moment you re-export the atlas. Declared rects are **rectangles** — they cannot express the diamonds and L-shapes isometric props actually have, so you still get wrong picks at corners. |

**What I would pick and why:** method 3 as the primary, with method 5 layered on top purely as touch-target *expansion*. Method 3 is the only one that directly solves the problem actually named — sprites overlapping the tile they're anchored to — it is pixel-exact so clicking a document icon's transparent corner correctly falls through, and after a one-time 10–30 ms load cost it is essentially free forever. Method 4 is strictly worse here: it doubles canvas memory against the iOS cap and invalidates on every camera move on a scroll-driven page. Keep method 1 as the ground-plane fast path for hover highlights, and build the alpha mask during the prologue scroll where the stall is invisible.

---

## D27. Navigation model — what to take from bruno-simon.com and what to refuse

**What the site actually is today (folio-2025, MIT on GitHub, Blender files included):** Three.js using **TSL** so the same shader source runs on WebGL or WebGPU; **Rapier** physics (Cannon.js in 2019); **Howler.js** with three commissioned **CC0** tracks by Kounine. WASD/arrows + shift-boost, ctrl-brake, space-jump, enter-interact; one finger to drive on mobile, two for camera; gamepad dual-stick. Modular menus, an "I'm Stuck" respawn teleport, an M-key map, a leaderboard circuit, a 30-message community board. README documents a **15-stage numbered game loop (0–999)** and a compression pipeline using KTX-Software and gltf-transform with etc1s encoding.

**Why it feels good — three reasons, only one technical:** the input loop is unusually tight and the physics exaggerated, so it rewards fiddling before reading; nothing punishes you (no fail state, no timer, explicit escape hatch); and **the content is genuinely secondary and the site knows it** — Bruno is a WebGL teacher, the medium *is* the message.

**Take:**
- **Diegetic instructions** — bake "CLICK THE SCREEN" into the floor tiles in the sprite sheet at 1984 bitmap weight, not as an HTML tooltip. *Downside:* can't be localised, can't be read by a screen reader, can't change without re-exporting the atlas, and becomes illegible at 8 px if you ever ship a scale-1 mobile view. Mitigate with a visually-hidden DOM duplicate.
- **The escape hatch** — a persistent, always-visible "return to desktop" plus a keyboard shortcut, in all three scenes. **Highest-value single steal on the list.** *Downside:* a visible admission the metaphor can fail, and making it read as a 1984 element rather than a modern FAB is real design work.
- **Loading as the first scene** — start fetching at page load, let the reader scroll prose, gate on scroll position rather than a spinner. *Downside:* a fast scroller outruns the load and hits an empty Mac. You need a genuine static pixel poster frame and a scroll-lock that engages only if assets are late — fiddly logic, easy to get subtly wrong on slow 3G.
- **Bake everything, light nothing at runtime.** *Downside:* baked shadows lock your sun angle forever. A later day/night pass or an arbitrarily-rotated prop means re-authoring every affected sprite. Decide the light direction once, write it down, never revisit.
- **A numbered, staged loop** — give every system an integer priority, sort once, run in order. *Downside:* architectural overhead that feels absurd for three scenes and can encourage building a general engine when you needed a specific one. Take the discipline (a written, numbered order), not necessarily the machinery.
- **Hidden interactions** — three or four hotspots that acknowledge themselves. *Downside:* implies session state and storage you don't otherwise need, and on a job-search portfolio there's a real tone risk — a hiring manager who gets an achievement toast may read it as unserious. Keep any acknowledgement silent and visual.

**Refuse: free-roam physics.** *Why it doesn't transfer:* isometric 2:1 with integer scales is a **grid** projection. Smooth physics motion at sub-tile positions destroys the pixel grid — a sprite at x=3.47 either lands on a fractional device pixel or judders as you snap it. You'd be paying for a physics engine to fight your own rendering contract.

**Structural precedents:**
- **Jesse Zhou's ramen shop** — a diorama with **anchored camera positions**, not a place you wander; beginner-to-shipped in under six months. *Downside:* its charm depends on modelling and lighting craft a 2:1 baked-sprite projection cannot replicate, and fixed anchors in isometric risk feeling like a slideshow rather than a place. → §UNCONFIRMED (repo licence).
- **Henry Heffernan's portfolio** — 90s Mac in 3D, split across **two repos**: the 3D scene and a **separately-runnable 2D operating system** composited into the CRT. The split is the lesson: build the desktop as its own thing you can develop at full size in a browser tab, then mount it. *Downside:* React + Three.js + a full window manager is nowhere near your byte budget, and mapping a click on a tilted screen mesh to a UI coordinate is genuinely fiddly. → §UNCONFIRMED (repo licence).
- **Robby Leonardi's interactive resume** — scroll as a **scrub head on a fixed animation**; the reader controls *rate*, never *route*. Closest published precedent to a scroll-driven journey through a game world, and it proves the model works for a CV specifically. *Downside:* linear with no branching — gets you through the prologue to the Mac but doesn't help once the reader is on a desktop with seven documents. A decade old; craft standards have moved.
- **Google Maps 8-bit (2012, Square Enix sprites)** — the purest published example of the governing rule, an old genre rendering current data. Look specifically at how they handled **density**: an NES world map has far fewer pixels than a road network needs, and the answer was aggressive symbolic abstraction — exactly your problem compressing four companies into a world map. *Downside:* a gag with a corporate art budget and a punchline, never meant to be used twice.
- **daedalOS (MIT)** — a full browser desktop, 4+ years of work. Use as a **lookup** for window focus order, drag bounds, double-click timing, icon selection rectangles. *Downside:* vastly larger than seven icons needs; importing this scale of abstraction is the definition of over-engineering.
- **Infinite Mac** — real emulated System software. Worth one afternoon to feel real spacing, timing and cursor behaviour. *Downside:* multi-megabyte emulator + ROM + disk image, external asset loading, no content control, no mobile story, severe licensing questions. Research reference only.

**What I would pick and why:** scroll-driven with a fixed camera track plus clickable hotspots — Leonardi's rate-not-route model to reach the Mac, Zhou's anchored-camera model between the three scenes, and Heffernan's two-repo split so the desktop is a standalone thing you can build and test at full size before mounting it into the 3D shell. Refuse free-roam outright, and not only for the pixel-grid reason: the reader is a hiring manager at App Central or Unity with maybe ninety seconds, and Bruno can afford wandering because the drive *is* his portfolio. If yours has to be hunted for, a 90-second skim converts into a 90-second failure. Take the craft — diegetic instructions, the escape hatch, bake-everything, the tight input loop — and leave the navigation.

---

# §UNCONFIRMED — do not ship without checking

Each of these is a live option **except** for its licence. Nothing here goes into a build until someone opens the actual terms.

| Item | Status | What to check |
|---|---|---|
| **04b_03** (Yuji Oshimoto) | Circulates as "freeware" with terms that vary between mirrors and no canonical OFL/CC0 text. Its dafont entry carries **no licence tag at all** (other entries show "100% Free" or "Free for personal use"). Redistribution rights — which is exactly what embedding is — **not confirmed**. | Nothing to check short of contacting the author. Treat as unusable. |
| **m3x6** (Daniel Linssen) | Its itch.io info panel has **no "Asset license" row** — only Status/Category/Rating/Author/Tags/Content. Informal free-use prose only. | Whether the author will state terms. **Note the split: `m5x7` IS formally CC0** — its itch.io metadata table carries "Asset license: Creative Commons Zero v1.0 Universal", so it belongs in the live list, not here. `[CORR — the research bundled both under "do not use"]` |
| **Silkscreen Expanded / Expanded Bold** | The googlefonts/silkscreen OFL repo contains **only Regular and Bold** (fonts/otf, fonts/ttf, fonts/webfonts each hold exactly 2 files; METADATA.pb lists only weights 400 and 700). Expanded exists only in Kottke's 2001 freeware release — a different distribution on an older, unclear footing. | The 2001 release's actual terms, if you want the Expanded cuts. The OFL covers only the two weights. |
| **Terminus TTF ≤ 4.30** | files.ax86.net states: *"From version 4.32 onwards, the font license is the SIL Open Font License, version 1.1"* — earlier versions are GPL v2 or later. | The **version number** of the exact file you ship. A mirrored or distro-packaged 4.30 is GPL, not OFL. Attach the licence to the version, never to the family. |
| **ChicagoFLF and the "Monaco" TTFs in the wild** (bundled by system.css and several retro CSS kits) | Licence unstated or unverifiable, and both are Apple typefaces. "A CSS project on GitHub bundles it" is not a licence grant. | Nothing checkable exists. **Recommendation: do not ship.** If system.css is used, strip its font files and substitute Chicago Kare + FindersKeepers. |
| **Lospec palette geometry** | Independently confirmed: **no licence on the palette-list index, none on individual palette pages**, and the site Terms grant Lospec broad rights over submissions while granting users none. Some individual palettes carry author-set terms (AxulArt's 32-colour is CC BY 4.0). | Per-palette, per-author. Since only step geometry would be borrowed and no hex copied, exposure is probably nil — but D4's P3/P4 already derive their offsets from scratch, so **skip it entirely**. |
| **Henry Heffernan — henryjeff/portfolio-website, henryjeff/portfolio-inner-site** | Licence not verified. | The repo LICENSE files. Read for **structure** (the two-repo split), do not lift code. |
| **Jesse Zhou — enderh3art/Ramen-Shop** | Licence not verified. | The repo LICENSE file. Read for structure, do not lift code. |
| **Executor (autc04/executor)** | Repository code is **GPL**. | Nothing — the geometry facts extracted from `.map` files are not copyrightable and are free to use, but **do not paste the `.map` files or the drawing code** into a proprietary page. |
| **Inside Macintosh PDFs, 1992 HIG, Mac Plus ROM images** | Apple copyright. | Reference only, do not redistribute. The **measurements are facts and are free**. A Mac Plus ROM for Mini vMac is legally murky to obtain even though trivially findable. |
| **AoE2 `50.pal`** | Proprietary Microsoft / Ensemble / Forgotten Empires content inside the game's DRS archives. **Not a licence to check — a hard no.** | Never vendor it. The index-remap technique (D9) is a method, not protectable expression, and is unaffected; state the player-colour index count as **unverifiable**, not pending. |
| **Apple System 6 ICN# resources and Chicago/Geneva/Monaco FONT/NFNT resources** extracted from a disk image | Apple copyright plus Susan Kare's designs. **Hard no.** | Listed only so the boundary is explicit. Measure from an emulator all you like; **embed nothing**. |

---

# UNRESOLVED CROSS-AREA CONFLICTS — settle these in the room

1. **`ChiKareGo2`'s native size.** The chrome research says "12 px and 24 px only"; the fonts measurement says every BitFontMaker2 export has a 16 px em (12 above baseline, 4 below) and is pixel-exact at 16/32/48. **Resolve to 16.** The same 768/−256-on-1024 metric was independently measured in Chicago Kare, which was *not* built in BitFontMaker2 — so `[CORR]` that 12/4 split is **Chicago's own metric, not a tool artifact**, which is why every honest Chicago revival lands on a 16 px em.
2. **Dithering inside the isometric scenes.** Tiles ATLAS-3 proposes Bayer between existing tokens to fake three-face shading; palette D1/D4 argues against it on optical grounds. **Resolve toward the palette** — D4/D5's ramps *are* the shading answer, so ATLAS-3 is not needed as a substitute, and D7 confines dither to the shell.
3. **"No new colours" — tokens or pixel values?** The tiles research calls this "the one blocking question in my area" and it is genuinely blocking, because every isometric convention depends on the three-face split (top 100% / side ~75% / side ~50%). D4 and D5 answer it (ramps are shading stops for existing tokens, not new brand colours), but that answer must be said out loud and accepted once, for all four companies, before any art is drawn.
4. **Zero external requests — literally, or no third parties?** D13 and D3 both hinge on it. Same-origin PNG recovers ~13 KB and adds caching; a truly single portable HTML file costs +37% on the atlas. Decide the reading, not the implementation.
5. **The 120 KB / 240 KB budgets have no source.** They are asserted in two research passes and never established, and the measured numbers say neither binds. Either source them or drop them — the T1-vs-T2 recommendation turned entirely on a constraint the same document's own arithmetic contradicts.
6. **Unverified conventions worth thirty minutes each in an emulator, per the "measure, then build" rule:** the Finder's Clean Up icon-grid spacing (every recreation assumes a 64-wide cell; that is a guess); the I-beam / watch / cross / plus cursor hotspots (only the arrow's (1,1) is published); the close box's offset from the outer frame line (8 or 9 px depending on how you count); whether the System 6 menu bar had rounded top corners (claimed, no source found); Sims 1's exact tile pixel dimensions (128×64 widely repeated, no primary source); SimCity 2000's base diamond and per-altitude step (32×16 family is the common claim, unconfirmed); HoMM3's 32×32 adventure-map tile (consistent with its square-grid movement rules, but the wikis document gameplay, not sprite dimensions).