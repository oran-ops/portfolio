# MOBILE TRACK — BUG LEDGER (site_mobile.html)

Perimeter: edits limited to `site_mobile.html` + harness files (`build_harness.py` regenerates
`m_test.html` + `harness.html`). Every fix is mobile-gated: CSS in `@media (max-width:880px)`
(or narrower), JS behind `window.innerWidth<861` (`MOB`). Desktop path byte-identical above 861.

## Harness / methodology

- Harness v2 (build_harness.py): 390x844 real iframe, rAF->setTimeout shim, clicks the boot
  gate like a human (`W.__bootOpen()`), drives a paced scroll (`?step=&tick=`), samples per tick.
- **Spec rule**: an element is a defect ("invis") only when its top is deeper than 25% into the
  viewport (r.top < 633) while computed opacity < .55. The bottom-25% band is a grace zone
  ("edge", informational). Kids = `.st`/`.rvs` stagger children measured the same way.
- Extra probes: statement words lit (stmt1/stmt2), memo opacity, `#ai2c` canvas non-zero pixel
  count, pin progress; holes geometry (hole x vs card text x); end-audit (pdraw/garc/cnt/bar
  completion, boot removed, ticker animation alive, overflow-x max, failsafe flag).
- Shot mode `?shot=<y>` + `--screenshot` for visual review.
- **Caveat**: baseline + run1 numbers were collected under harness v1-spec (any in-view invisible
  counted, no grace zone, no gate click); run2+ numbers are v2-spec (stricter methodology, boot
  gate clicked). Directionally comparable, not numerically.
- **Ops caveat**: one flaky regression (run2_420: 18/48) was CPU starvation from zombie headless
  Chrome instances left by a timed-out 300s-budget run; identical build re-ran 0/0 (run3_420).
  Rule since: one Chrome at a time, explicit timeout, 25s virtual budget, unique --user-data-dir.

## Ledger

| # | page/section | symptom | root cause | fix | verified-run |
|---|---|---|---|---|---|
| 1 | ALL sections (hero, files ticker, xtix, oasis, eventer, medcoin, leadership, tech, final) | Scrolling outruns entrances: whole section heads, plabels, evidence rows, principle rows sit fully in view at opacity 0 (baseline_420: totInvis 94, totKids 78; e.g. `xtix:shead.rv` on-screen invisible at y=6720) | Reveal gate `u.t < y+vh*.94` fires only when an element's top crosses 94% of the viewport, then .8s transitions + 80ms/65ms stagger delays (up to ~1.3s total) play while a phone flick moves 1.5 viewports; scenes lead .9/.94 too late for one-column mobile flow | (a) engine: mobile gate `y+vh*1.15 + min(vh*1.6, vel*320)` velocity lookahead (site_mobile.html ~2136-2140), `MOB` flag ~2014, refreshed in measure() ~2117; (b) scene leads bumped to >=1.06 on mobile only (~2056); (c) CSS M3 block (~1822-1889): all entrance transitions .26-.55s, stagger steps 26-45ms, travel distances shrunk (36px->18px etc.); (d) `.fon` fast-flick mode: units revealed while vel>2.2px/ms get zero-delay ~.3s entrances (engine ~2061 + M3-fast CSS) — slow scrolls keep the staged choreography | run1_420 (0/0), run1_260 (0/0), run3_420 (0/0), run3_700 (0/0) |

| 2 | statement (page 2) | No star/particle canvas on phones: approach to the pinned statement is a black screen, sentence never "assembles" (owner bug #3); harness: `#ai2c` absent, nz=-1 | SECOND INTELLIGENCE V script hard-returns at `innerWidth<861` (was ~3352) | Mobile perf profile instead of the kill-switch: `MOBP` flag; text stars 1900->950, free 260->120, DPR cap 2->1.75 on phones, still off <360px and for reduced-motion/static; `__ai2` no-ops (words forced visible) under body.failsafe on phones. Desktop >=861 byte-identical | runP_420 (cvMax 47), runS_420 (cvMax 84, cvEnd 0) |
| 3 | hero folder card + drawer case cards | Punch-holes printed over the first characters of every text line at 390px (owner bug #4): mfold holes x25..39 vs text x13; hfolder holes x21..35 vs text x17 | M1 padding flatten removed the wide rail band the holes were centered in (desktop pads 40/42px, mobile 14/18px) while holes kept desktop offsets | M4 block (~1891-1907): rebuilt an honest narrow rail — `.hfolder` padding-left 34px + holes 13px at x10 (<=860); `#hero .mfold` padding 26px + holes 12px at x7 (<=680) — holes centered in the band, content clears it | runH_420 probe: mfold holes [7,11] vs txL 25; hfolder [9,12] vs txL 32; visual check in sweep |
| 4 | statement (page 2) | (a) Second sentence stalls/never lights on phones after a flick; (b) parked mid-pin, the starfield freezes mid-flight dead | (a) physics P/PRE smoothing (.085/update) is updated only when scrollY changes; a phone flick crosses the 1122px pin in ~15 frames so P never reaches the U0=.74 word band until far past release; (b) `statement()`/`__ai2` are only called inside frame()'s `y!==lastY` branch — desktop's JS inertia tail keeps y micro-changing, native mobile momentum stops dead | (a) `SMF=MOBP?.14:.085` smoothing on phones (~3363/3512); (b) engine idle branch: while parked inside the statement zone on mobile, keep calling `statement(y)` every frame (~2155-2159). Desktop paths untouched | runS_420 (stmt2 5/5 by +300px after release, cvEnd 0), runS_hold (parked at p=.49: canvas keeps breathing, nz oscillates 42-63) |

| 5 | statement (page 2) — THE core of owner bug #2 | On phones the pinned statement never pins: the scene scrolls past like a static block (text gone in the first 40% of the section), then ~1.3 viewports of empty void before philosophy. Harness shot 01 proved it (pin bottom edge exiting at exactly pinh-top + 844 - y) | At <=680 the MOBILE EXCELLENCE block sets `html,body{overflow-x:hidden}`. With html non-visible, body's overflow no longer propagates to the viewport, so body keeps its own overflow-x:hidden, computes overflow-y:auto, and becomes the sticky containment scroller — which never scrolls. Every `position:sticky` descendant silently dies at <=680 only (desktop: html stays visible, body's hidden propagates to the viewport, body ends up visible — sticky fine) | `html{overflow-x:hidden}` + `body{overflow-x:clip}` (~1358-1365): clip cannot create a scroll container; ancient browsers fall back to today's behavior. Sideways clipping preserved (audit ofxMax stayed 0) | fix_01/fix_02 shots: pin holds fullscreen, sentence assembles from stars mid-pin; runV_420 clean |
| 6 | hero (page 1) | "EXECUTIVE PORTFOLIO" kick line rides up under the "Oran Carmon" name tab — top half of EXECUTIVE hidden behind the tab; card content starts at the folder's top edge | Legacy `#hero .center{padding:0 6px}` (<=680) hits the master folder card too (it carries `.mfold.center`), and being later in source than the base `#hero .mfold{padding:46px 40px 64px}` it zeroes the card's vertical padding | M5 (<=680): `#hero .mfold{padding-top:46px;padding-bottom:64px}` restores the designed air (~1911-1915) | fix_00_hero shot |
| 7 | medcoin — origin line | THE ORIGIN LINE svg timeline scaled to ~330px renders its station labels at ~2.8px — unreadable | 1060-unit-wide svg at width:100% with 9px design-size labels | Inert `mzorg` class on the svg's wrap + M5 (<=680): swipe like the site's other wide charts (overflow-x auto, min-width 760px, svg text 12.5px, edge-fade mask) | fix_15 shot: labels readable, fade + scrollbar hint |

## Visual sweep (task D) — screenshots mshots/00-22 + fix_*

Reviewed all 12 pages at 390x844: hero, statement (mid+end), philosophy (head+grid), files
(head+folder cards), xtix (head+mid+charts), oasis (head+mid), eventer (head+diagram), medcoin
(head+outcomes+origin), leadership (head+toolkit), tech (head+stack), final (ladder+seal+contact),
footer. Defects found: #5 (statement pin), #6 (hero kick), #7 (origin line) — fixed above. Clean:
folder punch-holes in their bands (hero + all four drawer cards), swipeable wide diagrams with
edge fades (eventer convergence, tech architecture), counters/bars/arcs complete, principles
ladder, vseal, contact cards, live footer clock, background marquees.

## Harness fidelity note (v2.1)

The driver now sub-steps every tick into 5 per-frame scrolls (real momentum updates y every
frame, not once per flick) and gained `?hold=<y>&dwell=<ms>` park-and-watch mode plus shot-mode
section-top reporting. Without sub-stepping, scroll-position physics (P smoothing) was starved
in a way no real phone would be.

## Run history

| run | spec | step/tick | totInvis | totKids | notes |
|---|---|---|---|---|---|
| baseline_420 | v2 harness, pre-fix source | 420/80 | 94 | 78 | worst: xtix/oasis/leadership/tech heads, files ticker, medcoin lists |
| run1_420 | after M3+gate (no .fon yet) | 420/80 | 0 | 0 | audit clean |
| run1_260 | same build | 260/120 | 0 | 0 | |
| run1_700 | same build | 700/80 | 52 | 44 | fast flick outran staged delays -> built .fon |
| run2_420 | after .fon | 420/80 | 18 | 48 | FLAKE — zombie-Chrome CPU starvation (see ops caveat) |
| run3_420 | same build, clean CPU | 420/80 | 0 | 0 | audit clean |
| run3_700 | same build | 700/80 | 0 | 0 | audit clean, ofxMax 0, counters/bars/pdraw complete |

Statement probe status after #1: stmt1 5/5 words lit by p=.36, stmt2 5/5 by p=.74 (fallback
word-rise), memo 1.0 by p=1; canvas `#ai2c` absent on mobile (nz=-1) — particles fix pending (#2).
Holes probe status: mfold holes x=25..39 vs text x=13 (padL 14) — overlapping content; hfolder
holes x=21..35 vs text x=17 (padL 18) — overlapping. Fix pending (#3).

---

# ROUND 2 (owner re-test, 9 items)

| # | page/section | symptom | root cause | fix | verified-run |
|---|---|---|---|---|---|
| R2-1 | statement | Text too small on phones (owner: significantly bigger) | Mobile override clamp(17px,5.4vw,22px) ≈21px at 390 | clamp(22px,7.2vw,28px), line-height 1.22 (+33%). Cap chosen so stmt2 stays ONE LINE >=360px — the particle scene rasters stmt2 as a single line, wrap would desync stars vs DOM; <360px physics is already off so wrap there is safe | pending shots + l2lines audit |
| R2-2 | statement gather | Sentence-2 dots "appear from thin air", field feels static, exit "just vanishes" | (a) pre-gather text stars dimmed to .8 alpha; (b) free-field fade compressed into a 62px band (FR .93-.985) driven by smoothed P — fires abruptly after release; (c) resize-storm rebuild teleported all stars (see R2-3) | MOBP profile: pre/flight alpha .95+.3ev; FR widened .90-.99; spatial exit `relOut` = fade over .55vh tied to page position past pin release, with clear when 0; sampling densified (step 2, NTXT 1200) for the larger glyphs | pending storm + shots |
| R2-3 | WHOLE DOCUMENT (owner's serious bug) | Scroll-up jump + broken scrolling everywhere | Mobile Chrome fires window.resize on URL-bar hide/show (width same, height ±~120). SIX resize listeners re-measured/rebuilt mid-scroll: engine (measure+lastY=-1 → full re-scrub snap), acts covers/lights, audio theaters, investigator, dust, star canvas (size+key reset+build → teleport) | `window.__mSoftRz(e,fn)` shared guard: width<861 + width-unchanged + |dH|<160 → SOFT: skip heavy path, queue the re-measure for scroll-idle (260ms window). 5 listeners guarded; canvas soft path runs size() only (paint area correct, no teleport); dust left as-was (no layout impact, blink only). Desktop: never classified soft, byte-identical | pending storm probe |
| R2-4 | medcoin zone 03 | Sideways jump + self-correct while scrolling up/down | Prime suspect = R2-3 resize storm (mzorg overflow-x container + re-measure interplay) | R2-3 guard; dedicated harness probe: #medcoin .wrap left + scrollLeft sampled every tick, both drive directions + storm | pending |
| R2-5 | eventer 07 / medcoin 05 / tech A | Nobody understands these scroll sideways | No affordance | Shared `.swcue` chip: mono "SWIPE" + emerald arrow, right-aligned above each chart, nudge keyframes (reduced-motion off), one-shot fade after first real swipe; engine injects on phones only when the container actually overflows | pending shots |
| R2-6 | medcoin zone 04 outcomes | Stacked rows read awkwardly (key left / value right mixed alignment) | Base `.outs .v{text-align:right}` outranked the round-1 td override | M6: td.v left-aligned 15px under a 9px letterspaced key, calmer row padding | pending shot |
| R2-7 | oasis part 2 zone C | Hub-spoke labels escape the zone frame | Labels spill ±41-47 units past the 260-unit viewBox by design (overflow:visible); desktop columns absorb ~48px spill, a 390px column cannot | M6 (<=680): cap rendered svg at max-width:225px so the spill stays inside the column | pending before/after shot |
| R2-8 | hero chips / any anchor | Tapping a case chip drags the statement particles across every section | `html{scroll-behavior:smooth}` + native anchor = long animated transit through the statement zone (desktop uses its own JS inertia path, pointer:fine only) | Phones: anchors preventDefault + instant scrollTo (archive cut), temporarily forcing scrollBehavior:auto; canvas self-clears next frame via relOut | pending |

## Round-2 iteration notes

- Oasis (R2-7): first fix (`#oasis .cols2 svg[...]{max-width:225px}`) failed — the svg carries an
  INLINE `max-width:280px`; needed `!important` + un-scoped selector, final 215px. Verified by shot.
- Swipe cue (R2-5): first placement (before the container) broke for `.mzorg`/`.archw` whose zone
  label lives INSIDE the scroll container — the cue visually attached to the previous zone. Final:
  cue inserted AFTER the container on all three — a bottom-right caption under the scrollbar.
- Reverse harness drive teleports to document-bottom (impossible for a human); first reverse-storm
  run flagged 9 grace-period entrances (class state healthy: on+fon, 80ms into .3s transitions).
  REV mode now lands like a deep link (500ms settle) before driving — matches real deep-link UX.

## Round-2 verification status

All R2 items verified: R2-1 (l2 single line, 28px, audit l2lines=1), R2-2 (shots: star-sentence
clearly legible pre-handoff; spatial exit clears canvas by pin+.55vh — was lingering 1.6
viewports), R2-3 (guard [1,1] unit probe + storm/storm-rev drives clean), R2-4 (mw [14,14,0]
lateral zero-drift through resize storms both directions), R2-5 (3 cues injected, 1 dismissed by
the programmatic swipe probe, shots at all three), R2-6/R2-7 (shots), R2-8 (instant-cut handler;
canvas self-clears via relOut — no transit for particles to smear across).

## ROUND-2 FINAL BATTERY (all with particles active, swipe cues live)

| run | mode | inv/kids | errors | cvMax/cvEnd | mw lateral | guard | cues/off | l2 lines/px | scenes bad | ofx | failsafe |
|---|---|---|---|---|---|---|---|---|---|---|---|
| f1_420 | 420/80 | 0/0 | [] | 98/0 | [14,14,0] | [1,1] | 3/1 | 1/28 | 0 | 0 | no |
| f2_260 | 260/120 | 0/0 | [] | 97/0 | [14,14,0] | [1,1] | 3/1 | 1/28 | 0 | 0 | no |
| f3_700 | 700/80 | 0/0 | [] | 116/0 | [14,14,0] | [1,1] | 3/1 | 1/28 | 0 | 0 | no |
| f4_storm | 420 + resize every 3rd tick | 0/0 | [] | 98/0 | [14,14,0] | [1,1] | — | — | 0 | 0 | no |
| f5_stormrev | 420 reverse + storm | 0/0 | [] | 112/42* | [14,14,0] | [1,1] | — | — | 0 | 0 | no |

*f5 cvEnd 42 = ambient field legitimately alive near the hero where the reverse run ends.

## Round-2 files touched

- `site_mobile.html` — `__mSoftRz` guard + 5 guarded listeners (engine/acts/audio/investigator/
  canvas-soft-size); mobile instant-anchor handler; swipe-cue injector; statement font override;
  physics: FR band, NTXT 1200, step 2 sampling, gather alphas, relOut spatial exit, stH cache;
  M6 CSS block (cue styling, oasis cap, outcomes rhythm). All mobile-gated; desktop >=861
  byte-identical (guard classifies nothing soft at >=861; relOut stays 1; cues never injected).
- `build_harness.py` (v2.2): storm + rev modes, guard unit probe, medcoin lateral probe,
  l2lines/l2px audit, swipe-dismiss probe, deep-link landing settle for REV.
- `BUGLOG.md`, `mshots2/*.png`, `r2*/f*.json`.
- Perimeter re-verified after the battery: site.html / site_standalone.html / casebook.html /
  Oran_Personal_Brand untouched; zero headless Chrome left; profile dirs removed.

---

# ROUND 3 (owner re-test in Telegram's iOS in-app webview)

Environment note: WKWebView inside Telegram — its own toolbar collapse/expand (resize storms +
CSS-vh flutter), Safari engine, rubber-band overscroll.

| # | section | symptom | root cause | fix | verified-run |
|---|---|---|---|---|---|
| R3-4 | whole document (serious) | scroll down, stop, reverse up -> jump, snap-back, then normal | ROUND-2'S OWN deferred idle re-measure: direction change -> webview toolbar resize (soft) -> 260ms idle timer armed -> fired `measure()+lastY=-1` right as the user resumed -> full re-scrub snap with changed vh | v3 guard: soft resizes schedule NOTHING (no timers, no deferred re-measure — machinery deleted). Soft path = additive `revealPass()` against live innerHeight (never un-reveals, touches no scrub state) + canvas `size()` only. Scrub mappings keep their load-time viewport (tolerate ±13%, corrected by any hard resize). Plus: engine y clamped for iOS rubber-band (top hard, bottom +200px slack over possibly-stale DOCH), physics yNow clamped >=0; no visualViewport listeners exist; wheel-inertia confirmed pointer:fine-gated | pending stop-reverse profile x3 |
| R3-1 | hero (early scroll) | tab and folder ride apart "as if not connected"; folder stretches downward as scrolling starts | (a) `#hero .mfold{min-height:62vh}` — CSS vh flutters in in-app webviews as the toolbar collapses -> the card literally stretches mid-scroll; (b) boot-open pose transition (1.15s, perspective+rotateX) still mid-flight when the user scrolls -> every heroFx inline write RETARGETS the transition -> the folder lags/shears behind the finger, tab vs card projecting differently under the 3D pose | (a) engine freezes the card height in px at measure-time on phones (recomputed only on hard resizes); (b) <=680 the open transition is .45s and heroFx kills it at first real scroll (y>2) so the scrub owns the transform instantly | pending hero glue probe + scrub shots |
| R3-2 | statement assembly | when the sentence is complete, dots still appear/hover around it — "must be precise on the timing" | text-star fade used the same u-ramp as the word rise (they crossfaded AROUND each other, stragglers still in flight); ambient green 'em' stars sit near the text band post-handoff | phones: (1) urgency — approach spring x(1+5*band(P,.66,.76)) while flight noise dies; (2) hard landing guarantee — any star still in flight when the word ramp passes u=.2 lands with a flare, so arrival completes BEFORE the swap; (3) text stars extinguish INTO the glyphs by P=.86 (words solidify at .92) — no dot outlives the letters; (4) ambient stars within ~1.7 line-heights of the sentence dim by 85% post-handoff. Reverse is symmetric (mode-3 re-scatter + alpha band reverses) | pending green-band metric + shots |
| R3-3 | swipe cues | after swiping, the arrow vanished while SWIPE stayed; new spec: arrow visible AT ALL TIMES | one-shot dismiss faded the container; in iOS webviews the composited animated child (arrow) can die ahead of the parent's opacity transition -> partial state | dismiss path deleted entirely — the cue (label + nudging arrow) is persistent; reduced-motion keeps a static arrow | pending persistence probe (swipe then check) |

## Round-3 discovery (hero probe)

The deep probe caught the true tab/card detach: `#hero .mfold.on` runs `hfloat` — a ±13px
levitation animation on the CARD while the name tab never floats (line ~1655; desktop has this
too, where it is ambience in a wide layout). At 390px the card fills the screen and the pair
reads as broken. Phones now keep the `sweepx` sheen, drop the float (<=680). Probe before:
gapDev 4.5px with a live matrix on the card; after: gapDev 0.0 at every step, storm included,
minHeight frozen 523px. This float was also the residual 0.2-0.5px "pauseMove" in early
stop-reverse runs — final runs show 0.0 flat.

## ROUND-3 FINAL BATTERY (final source)

| run | mode | inv/kids | errors | cvMax/cvEnd | mw | cues/off | l2 | scenes bad | fs |
|---|---|---|---|---|---|---|---|---|---|
| g1_420 | 420/80 | 0/0 | [] | 98/0 | [14,14,0] | 3/0 | 1 line @28px | 0 | no |
| g2_260 | 260/120 | 0/0 | [] | 98/0 | [14,14,0] | 3/0 | 1/28 | 0 | no |
| g3_700 | 700/80 | 0/0 | [] | 116/0 | [14,14,0] | 3/0 | 1/28 | 0 | no |
| g4_storm | 420+resize/3 ticks | 0/0 | [] | 98/0 | [14,14,0] | 3/0 | — | 0 | no |
| g5_stormrev | reverse+storm | 0/0 | [] | 79/33* | [14,14,0] | 3/0 | — | 0 | no |
| g6-g8 stoprev | pause@600/1400/12000 + soft resizes while parked | pauseMove 0.0, drift 0.0 at all three | | | | | | | |
| h4/h5 hero | glue probe, plain+storm | gapDev 0.0, dxDev 0.0, minH 523px frozen | | | | | | | |

*ambient field legitimately alive near hero at reverse-run end.

R3-2 precision metric (st=[w1,lit1,w2,lit2,memo,nz,nearG,farG]): at EVERY sample where the
sentence is solid (lit2=5), nearG=0 across all paces — zero green pixels within the sentence
band +-60px after solidify; mid-crossfade samples show only the designed dots-becoming-letters
state. Shots: mshots3/st_solid.png (solid sentences, clean field), hero200/400/600 (rigid card
through the scrub), cue_swiped.png (chart swiped, SWIPE + arrow still fully visible).

## Round-3 files touched

- `site_mobile.html`: v3 soft-resize guard (timer-free, ~2020-2040); revealPass (~2075-2085);
  engine rubber-band clamp (~2160) + physics yNow clamp; mfold px min-height freeze in measure();
  heroFx transition kill at first scroll + hcKill; physics precision (urgency, force-land at
  u>.2, extinguish by P=.86, near-band ambient dim); persistent swipe cue (dismiss deleted);
  M6 additions (fast boot-open <=680, no-float mfold <=680). All mobile-gated.
- `build_harness.py` v3: hero glue profile (`?profile=hero`), stop-reverse profile
  (`?profile=stoprev&pause=`), canvas green-band scan (nearG/farG in stmt samples), shot
  `&swipe=1`, persistence assertions.
- Perimeter re-verified; zero headless Chrome; profiles removed.

## EXIT — three consecutive fully-clean runs (final source, particles active)

| run | step/tick | totInvis | totKids | errors | cvMax/cvEnd | ofxMax | scenes (pdraw/garc/cnt/bar) | boot/ticker/failsafe |
|---|---|---|---|---|---|---|---|---|
| exit1_420 | 420/80 | 0 | 0 | [] | 90 / 0 | 0 | 0/0/0/0 bad | removed / alive / no |
| exit2_260 | 260/120 | 0 | 0 | [] | 63 / 0 | 0 | 0/0/0/0 bad | removed / alive / no |
| exit3_700 | 700/80 | 0 | 0 | [] | 102 / 0 | 0 | 0/0/0/0 bad | removed / alive / no |

Statement across the three: pin sticks (pt=0 through the scene), stmt1 5/5 in-pin, memo 1.0
in-pin; stmt2 5/5 at release at the leisurely pace (260: lit at p=1.11, 116px past release) and
during the ~1s physics settle after violent flicks (420/700) — canvas dissolves to 0 after.
Hold-mode: parked mid-pin, the starfield keeps breathing (nz oscillates), pt stays 0.

## Open design decisions (recommendations)

1. stmt2 on violent flicks completes ~0.5-1.5s after pin release (physics settle; already 2x
   snappier on phones via SMF .14 vs desktop .085). Could force-complete words at release
   (`setW2(1)` when p>=1) — recommend KEEP the settle: it is the designed constellation feel and
   matches desktop behavior under equally fast wheel scrolling.
2. Investigator arc + archive audio stay OFF under 861px (deliberate per owner instruction —
   heavy). Recommend keep off.
3. Free-star ambience is visible over hero/philosophy during approach/dissolve (fixed z-1
   canvas — same as desktop). Recommend keep.
4. `.fon` fast-flick threshold vel>2.2px/ms: the 260-pace keeps the full staged choreography,
   faster gets condensed zero-delay entrances. Recommend keep threshold.
5. `body{overflow-x:clip}` fallback: pre-2022 browsers without `clip` fall back to the previous
   (broken-pin) behavior. Recommend accept — the belt on `html` still prevents sideways scroll.
6. 681-860 tablet band inherits the new hfolder rail (M4 <=860); mfold hole fix is <=680 only
   (681-880 keeps the desktop-padded card where original offsets are correct). Recommend as-is.

## Files touched (perimeter respected)

- `site_mobile.html` — all changes mobile-gated (`@media (max-width:880px/860/680)` CSS,
  `window.innerWidth<861` JS): overflow fix ~1358-1365; M3 pacing ~1829-1875; M3-fast .fon
  ~1876-1896; M4 holes ~1899-1912; M5 sweep ~1915-1930; engine MOB/vel/gate/.fon/idle-statement
  ~2021, ~2063, ~2068, ~2124, ~2143-2147, ~2162-2166; physics MOBP/SMF/counts/DPR/failsafe-guard
  ~3364-3369, ~3383, ~3418, ~3430, ~3510-3511, ~3502.
- `build_harness.py` (+ its outputs `m_test.html`, `harness.html`) — harness v2.1.
- `BUGLOG.md`, `mshots/*.png`, `baseline_*/run*/exit*.json` — evidence.
- NOT touched: `site.html`, `site_standalone.html`, `casebook.html`, anything under
  `Desktop\Oran_Personal_Brand` (timestamps verified pre-session). No git, no deploy.

---

# ROUND 4 (owner iPhone/Telegram: assembly precision STILL off — frame-rate-dependence hunt)

Owner: "dots visibly late/hovering around the sentence as it completes" while harness showed
nearG=0 twice. Working hypothesis to PROVE first: the harness shim runs a deterministic 16ms
frame; the device drops to ~30-40fps (1320 stars, DPR 1.75, WKWebView). Every per-frame
multiplicative constant converges per FRAME while the finger moves per SECOND — at 30fps the
physics gets HALF the convergence per px of scroll. Stragglers at solidify, invisible at 16ms.

## Pre-work audit of per-frame constants in the scene (site_mobile.html ~3513-3823)

frame-rate-DEPENDENT (converge per frame, not per ms):
- P+=(pRaw-P)*SMF, PRE likewise (SMF .14 phone) — line ~3671
- t+=.016 fixed tick (noise/twinkle clock) ~3690
- kick*=.88 decay; vx,vy*=.9 mouse decay ~3693
- call attraction st.fx+=(tx-st.fx)*.005*call ~3728
- field drift st.fx+=flx()*sp, sp=.4*st.z px/frame ~3719
- flight spring st.vx+=dxx*st.k*urg+noise; st.vx*=dmp (.84|st.dp .90-.925); x+=vx ~3748-3754
- velocity clamp vv>18 px/frame; landing test vv<1.1 px/frame ~3753-3755
- mode-3 return spring, damping .9, clamp 15 ~3768-3773
- flare=9|6, flare-- per frame ~3755-3756, 3804
frame-rate-INDEPENDENT (audited clean):
- engine vel = (dy)/(performance.now dt) px/ms -> .fon threshold unaffected ~2260
- all reveal/scene/counter ramps pure functions of y; CSS transitions wall-clock
- discrete transitions are LEVEL-triggered (mode flips, u>.2 force-land re-checked every
  frame) — a P-leap cannot skip them; no band-equality edges found. Flare is the only
  frame-COUNT ramp.
- harness ran DPR=1 (headless devicePixelRatio=1, cap min()) — device runs 1.75: bitmap
  4x px count never exercised. Also green-band scan compared device-px rows vs CSS band —
  correct at DPR1 only; fix scan to normalize.

## Round-4 harness upgrades (build_harness.py v4)

- ?fps=60|30|20 -> inner shim setTimeout 16|33|50ms (m_test.html reads its own query; outer
  passes it through a dynamic iframe src). performance.now() spacing under virtual time gives
  the scene a REAL slow dt to measure.
- ?profile=mom momentum flick: land above statement, approach to P~=.5, then v0=2400px/s
  decaying x.94 per 16.667ms, y stepped every 16ms wall — scroll moves per SECOND while the
  scene frames at fps. Samples every ~33ms + 2.5s settle tail.
- aitele=1 always on inner: scene __tele = [fr,scx,scy,tcx,tcy,nfly,nland] per frame ->
  harness reads nfly (in-flight text stars) + mean position error (scx-tcx) at every sample.
- solid metric: lit2s = words with opacity>=.97 (strict, u~1) alongside legacy lit2 (>.6).
- canvasNZ band scan normalized by cv.width/390 so it stays correct at any DPR.
- ?dpr=N attempts Object.defineProperty(devicePixelRatio) on the inner window (env knob).
- ?profile=stmt: short statement-zone fixed-pace drive (fast battery at 3 fps values).

STATUS: harness upgrade in progress.

## R4 RED — REPRODUCED (harness v4, momentum flick v0=2400px/s decay .94/frame, start P=.5)

Strict-solid = all 5 stmt2 words at opacity>=.97. err = swarm-centroid distance from glyph
targets (px). maxDrop = largest one-sample fall in nfly (the mass-snap size).

| fps | crossMs (words-lit->solid) | maxFlyCross | meanErrFly | maxErrCross | flyAtSolid | maxDrop | solidT after flick |
|---|---|---|---|---|---|---|---|
| 60 | 160 | 723 | 3.4px | 6.7px | 0 | 721 (from <=7px - invisible) | 448ms |
| 30 | 192 | 728 | 15.7px | 31.3px | 0 | 728 (from ~30-40px - VISIBLE pop) | 608ms |
| 20 | 320 | 728 | 30.8px | 46.2px | 0 | 728 (from ~46-78px - gross pop) | 800ms |

The owner's symptom decoded: during the crossfade (P .74-.86) the words visibly rise while the
ENTIRE swarm (728 dots) still hovers 31-46px+ off-glyph at 30/20fps (fps60: 3-7px = reads as
dots-on-letters). Then the u>.2 force-land teleports all 728 in ONE frame - a pop. Choreography
also lands 160-350ms later in wall time (P smoothing halves per frame, not per ms).
Fixed 420/80 sustained drive twin: err at pin release 7px@60 vs 18px@30; post-release settle
solidified words at 60fps but not at 30 inside +1.2vh of scroll.
WHY ROUND-3 WAS GREEN-BLIND: nearG was asserted at lit2=5 samples only; the force-snap +
extinguish (P .783/.86) complete BEFORE strict solid (P~.906) at EVERY fps - the metric could
not see the crossfade. New discriminators: meanErrFly / maxErrCross / maxDrop / crossMs.
Evidence: r4_mom60.json / r4_mom30.json / r4_mom20.json / r4_stmt30.json / r4_stmt60.json.

FIX TARGET: dt-normalize (clamp [8,50]ms) so 30/20fps matches the 60fps numbers (err<=8px
through cross, snap from <=8px, crossMs ~160, solidT ~450); budget NTXT 900 (Bresenham thin,
not grid step-3 which would collapse to ~470), FREE 100, DPR cap 1.5 + one-way governor at
emaDt>26ms; flare frames -> dt units; soft-resize size() repaints same frame via re-entrant
__ai2(lastPRaw); all MOBP-gated, desktop dtN identically 1 via ternaries picking original ops.

## R4 FIX (site_mobile.html, all MOBP-gated; desktop dtN===1 picks original arithmetic)

Constants changed (before -> after), scene ~3524-3860:
- NEW dt clock: dtN=clamp(measured rdt,8..50)/16.667 per frame; desktop stays exactly 1.
- P/PRE smoothing: *SMF -> *smf where smf=1-(1-SMF)^dtN                      [.14/frame -> per-wall-ms]
- noise clock: t+=.016 -> t+=.016*dtN
- kick decay .88 -> .88^dtN; mouse vx,vy .9 -> .9^dtN
- call attraction .005*call -> .005*call*dtN
- field drift sp=.4*z -> .4*z*dtN; kick term *.5 -> *.5*dtN
- flight spring: accel terms *dtN; damping (.84|st.dp) -> ^dtN; x+=v -> x+=v*dtN
  (numerically simulated dtN=1/2/3 pre-ship: converges in identical wall time, no divergence)
- return spring (mode 3): same treatment, damping .9 -> .9^dtN (shared d90)
- flare frame-count -> dt units: st.flare-- -> st.flare-=dtN
- budget: NTXT 1200->900, FREE 120->100 (TOTAL 1320->1000, -24% sprites/frame); DPR cap
  1.75->1.5; density compensation sz*1.1, ssz*1.16, alpha*1.12 (phones only)
- glyph sampler: never coarsens to step 3 on phones (would collapse to ~470 pts);
  keeps step 2 and thins EVENLY (Bresenham) to NTXT. Measured: 390px sentence yields
  728 step-2 points -> N=728 unchanged by the budget cut (thinning is a no-op today).
- one-way governor: emaDt(.06)>26ms && fr>24 -> DPRCAP 1.25 once + same-frame size()+repaint
- soft-resize: size() now repainted in the SAME frame via re-entrant __ai2(lastPRaw) with
  dtN=0 (pure redraw: smf=0, c^0=1, x+=v*0) - no blank frame in Telegram toolbar storms
- ambient near-band dim: 1.7 line-heights/85% -> 2.4/92% (guarantees green-scan zero across
  the whole +-60px metric band: worst-case ambient alpha .09 < scan threshold .157)
- threshold audit vs P-leaps: all discrete transitions LEVEL-triggered + latched in st.mode,
  re-checked every frame (launch front>st.d / force-land u>.2 / re-scatter front<st.d-.05);
  extinguish/solidify/urgency continuous in P; reverse symmetric by the same conditions.
- harness/instrumentation only: __tele pushes every frame under ?aitele=1 (was: stale after
  extinguish), __aiN/__aiGov/__aiDbg exports (TELE/gov-gated, production-inert).

## R4 GREEN — momentum flick, post-fix (same drive as RED)

| fps | crossMs | meanErrFly | maxErrCross | flyAtSolid | maxFlyAfterSolid | nearG@solid rows | tail | solidT |
|---|---|---|---|---|---|---|---|---|
| 60 | 160 | 6.7 | 6.7 | 0 | 0 | all 0 | 0ms | 448 |
| 30 | 160 | 4.2 | 6.3 | 0 | 0 | all 0 | 0ms | 448 |
| 20 | 128 | 2.2 | 6.7 | 0 | 0 | all 0 | 0ms | 416 |

30/20fps now match the 60fps reference within sample quantization: swarm within ~7px of
glyphs through the whole crossfade at every frame rate; force-land fires from <=7px
(invisible); wall-clock timing identical (solidT 448 vs RED's 608/800). Governor: fired at
fps30; fps20 initially missed it (fr>40 warmup > frames in one crossing) -> gate lowered to
fr>24, emaDt inertia (~6 frames) is the real filter. Evidence r4_g_mom*.json.
STATUS: running statement battery (3 fps x 260|420|700 + mom) then full regression battery.

## R4 GREEN — statement battery, FINAL SOURCE (fps 60/30/20 x 260|420|700 + momentum)

All 12 runs: errors [], totInvis 0, cvEnd 0; every strict-solid sample maxNearG=0 maxFly=0
maxErr=0; stmt2 reaches l2s=5/5 at every pace INCLUDING the 700 conveyor (the round-3 flake -
exit3_700 lit vs g3_700 dark - was a pre-existing race: exit branch gated words on smoothed P
frozen wherever the engine stopped calling the scene; now phones use max(P,pRaw) - the page
being past the ramp is the truth; desktop expression untouched).
Momentum (final): fps60 crossMs160/meanErr2.9/maxErr5.8; fps30 160/3.4/6.7; fps20 128/2.2/6.7;
flyAtSolid=0, maxFlyAfterSolid=0, nearG=0 at every solid row, tail 0ms - at all three rates.
Evidence: r4_final_stmt_*.json, r4_final_mom*.json.
STATUS: full regression battery (fps60+fps30 x 420|260|700|storm|storm-rev|stoprev x3) next.

## ROUND-4 FULL REGRESSION BATTERY (final source, fps=60 AND fps=30)

| run | inv/kids | errors | solid n/nearG/fly | cvMax/cvEnd | ofx | mw | guard | cues | scenes bad | boot/ticker/fs | l2 |
|---|---|---|---|---|---|---|---|---|---|---|---|
| 420/80 @60 | 0/0 | [] | 3/0/0 | 101/0 | 0 | [14,14,0] | [1,1] | 3/0 | 0/0/0/0 | ok/alive/no | 1@28 |
| 420/80 @30 | 0/0 | [] | 3/0/0 | 99/0 | 0 | [14,14,0] | [1,1] | 3/0 | 0/0/0/0 | ok/alive/no | 1@28 |
| 260/120 @60 | 0/0 | [] | 5/0/0 | 87/0 | 0 | [14,14,0] | [1,1] | 3/0 | 0/0/0/0 | ok/alive/no | 1@28 |
| 260/120 @30 | 0/0 | [] | 5/0/0 | 100/0 | 0 | [14,14,0] | [1,1] | 3/0 | 0/0/0/0 | ok/alive/no | 1@28 |
| 700/80 @60 | 0/0 | [] | 2/0/0 | 99/0 | 0 | [14,14,0] | [1,1] | 3/0 | 0/0/0/0 | ok/alive/no | 1@28 |
| 700/80 @30 | 0/0 | [] | 2/0/0 | 112/0 | 0 | [14,14,0] | [1,1] | 3/0 | 0/0/0/0 | ok/alive/no | 1@28 |
| storm @60 | 0/0 | [] | 3/0/0 | 102/0 | 0 | [14,14,0] | [1,1] | — | 0/0/0/0 | ok/alive/no | — |
| storm @30 | 0/0 | [] | 3/0/0 | 103/0 | 0 | [14,14,0] | [1,1] | — | 0/0/0/0 | ok/alive/no | — |
| storm-rev @60 | 0/0 | [] | 4/0/0 | 73/34* | 0 | [14,14,0] | [1,1] | — | 17/3/5/10** | ok/alive/no | — |
| storm-rev @30 | 0/0 | [] | 4/0/0 | 71/34* | 0 | [14,14,0] | [1,1] | — | 17/3/5/10** | ok/alive/no | — |
| stoprev 600 @60/@30 | pauseMove 0.0 / drift 0.0 both | | | | | | | | | | |
| stoprev 1400 @60/@30 | pauseMove 0.0 / drift 0.0 both | | | | | | | | | | |
| stoprev 12000 @60/@30 | pauseMove 0.0 / drift 0.0 both | | | | | | | | | | |

*ambient legitimately alive near hero at reverse-end (round-2 f5: 42, round-3 g5: 33 - same).
**identical to f5/g5 baselines (17/3/5/10): scenes scrubbed back to pr=0 at page top by the
reverse drive - designed, not a regression (verified against archived g5/f5 JSONs).
.fon fast-flick check at low fps: engine vel is px/REAL-ms (divides by performance.now dt,
~2136) - fps-independent by construction; 700/80@30 totInvis 0 confirms in practice.
Governor fired opportunistically (260@30, mom@30) - one-way, DPR notch, no metric changed.

Shots (mshots4/): st_solid_fps30.png - solid sentence, zero stray dots anywhere near the
band; st_mid_fps30.png - mid-assembly parked at p~=.62, sentence drawn IN dots exactly on
glyph geometry (the designed constellation), stmt1 lit above, ambient field healthy.

## Round-4 files touched (perimeter respected)

- site_mobile.html - scene only (~3513-3860), all MOBP-gated or dtN===1-inert on desktop:
  dt clock + governor + budget + sampler thinning + density comp + soft-resize same-frame
  repaint + ambient dim widen + exit-branch pRaw truth + TELE instrumentation.
- build_harness.py v4 (+ regenerated m_test.html, harness.html): fps shim knob, momentum
  profile, stmt profile, tele/lit2strict probes, DPR-normalized green scan, solid-agg
  verdict, teleLast stale-ghost guard, dpr override knob.
- BUGLOG.md, r4_*.json evidence, mshots4/*.png, raw dumps (mom*/gmom*/sb_*/sc_*/mc*/F*/SR*).
- NOT touched: site.html, site_standalone.html, casebook.html (timestamps Aug 3/4),
  Desktop\Oran_Personal_Brand (verified). No git, no deploy. Zero stray chromes; all 49
  chrome_prof_r4* dirs removed.

## Round-4 open design calls (recommendations)

1. Momentum profile defaults (v0 2400px/s, decay .94/frame, flick from P=.5) are our model of
   the owner's flick; his Telegram webview may differ (iOS decay ~.998/ms). The dt-normalized
   physics is pace-invariant across 260-700 and momentum, so this should generalize -
   recommend owner re-test on device as the true GREEN gate.
2. Free-star ambience now ~272 visible drifters (TOTAL 1000 - N 728) vs ~592 before; alpha
   +12%/size +10-16% compensation applied. Field reads slightly sparser but brighter at DPR
   1.5. Recommend accept (it bought the frame budget); owner eyeball on device decides.
3. Governor threshold emaDt>26ms & fr>24, one-way to DPR 1.25: deliberately conservative,
   never reverses within a session (avoids oscillation). Recommend keep one-way.
4. Sustained-conveyor exit (700 pace) now guarantees a lit sentence via the pRaw-truth exit
   branch; the star assembly itself still dissolves via relOut when the page is past the pin
   (designed spatial exit). Recommend keep.
5. dt clamp ceiling 50ms means a device below ~15fps runs physics at .75x wall speed
   (graceful, teleport-proof). Recommend keep.

## ROUND 4 EXIT SUMMARY

RED (fps-dependence) proven: at 30/20fps the swarm hovered 31-46px+ off-glyph through the
crossfade with a single-frame 728-star teleport pop, and the whole scene ran 160-350ms late.
GREEN: after dt-normalization the 30/20fps numbers equal the 60fps reference (err<=6.7px,
flyAtSolid 0, nearG 0 at every strict-solid sample, tail 0ms) across momentum + 3 fixed paces,
and the full 16-run regression battery at fps 60/30 is clean with no desktop-side edits.

## BIG BUILD — feature 1: THE VAULT (done)
Final section + footer rendered as a silver-halide microfilm negative, always on.
- #final: bed #0A0B0D, inset vignette 150px, faint centre bloom; padding 74px for the film edges.
- .vfilm left/right rebates injected by JS: black stock, sprocket-hole dot columns
  (radial-gradient repeat-y), vertical mono captions KODAK SAFETY FILM 5063 / EMERALD ARCHIVE REEL 04
  + frame numbers 26A/27A. Film continues THROUGH the footer via footer::before/::after so there is
  no seam at the section boundary (found by pixel sampling: the vignette made plain #0A0B0D look lighter).
- Negative palette: silver #EDEFF6 text with scan-bloom text-shadows, emerald retired inside the vault
  (deliberate: different medium). .vseal .vq b needed the two-class selector to beat the base rule.
- Mobile: rebates 40px/30px at 860/560 breakpoints.
Verified: harness 420 clean (0/0, no errors); end-of-document screenshot shows continuous film frame.

## BIG BUILD — feature 2: TYPE VOICES (done)
Special Elite latin subset (53KB woff2 -> 71KB base64) inlined. Four analyst margin notes,
one per case, inserted after each .evslip: case-colored left rule, -0.55deg tilt,
"ANALYST NOTE — MARGIN" header, "— REVIEWING DESK, 2026" sign-off. Per-glyph strike variance
(deterministic sin-hash: translateY ±0.75px, rotate ±1.05deg, opacity .78-1) so no two glyphs
land alike. Two gen-3 marks: inside the Medcoin folder and above the vault (light variant).
Bug caught in probe: the note div was created empty (text never assigned) — glyph count 0
exposed it; wired NOTES[id] before strike(). Verified: 90/84/85/74 glyphs, font resolves to
Special Elite, both gen3 marks in place.

## BIG BUILD — feature 3: KINETIC TITLES (done)
Fraunces variable (wght 100..900, latin, 36KB woff2 -> 49KB base64) inlined as 'FrauncesVar'.
All eight .sttl chapter titles moved from Inter 800 to the variable serif; weight scrubbed per
word 140->880 with tracking .05em->0 as the title climbs the viewport. Reuses the site's existing
.tw word split (.w>i) — the reveal keeps opacity/transform, the scrub only touches weight/tracking,
so no fight and no new .u elements for the harness. Writes only on >=8-unit deltas, only for titles
within 200px of the viewport. Verified: all 8 resolve to FrauncesVar; line counts unchanged
(1/1/1/1/2/2/2/1); scrub 554,451,347,244,140,140 early -> all 880 late; harness 420 clean;
mom30 statement unaffected (errCross 5.8, flyAtSolid 0).

## BIG BUILD — feature 4: SCROLL-REDACTION (done)
Eight quiet unlabeled bars — one to three per section across all four cases plus leadership and
tech — that lift as the page scrolls past (open by the time the line reaches ~55% viewport),
one-way latched so they never re-cover. Visually the light matte of the SEALED bars but thinner
and mute: no label, no sheen, no pointer. Listener self-removes once all eight are done.
Verified: 8 bars in 8 sections; --sp 1 -> 0.000 across the window; still 0.000 after scrolling
back to top (latch holds); mid-wipe screenshot shows the three XTIX reflection lines emerging.

## BIG BUILD — feature 5: DRAWER LOUPE (done)
Press-and-hold (340ms touch / 400ms mouse dwell) on any of the four drawer file cards raises a
196px glass: dark sphere, case-colored ring and glow, showing the spine ticket — FILE NN, name in
Fraunces, industry/scope/date lines, ON RECORD. Moves with the pointer, hides on release/leave/scroll,
cancels if the pointer travels >8px (so a swipe through the drawer never triggers it), and a capture-
phase click guard means a hold can never also open the file. Verified: 4 cards; hold shows Oasis /
FILE 02 / brass #E0A458; release hides; screenshot shows the glass over the XTIX card.

## BIG BUILD — battery (features 1-5)
420/260/700 all 0-0, errors [], ofx 0, counters/pdraw 0, canvas alive (cvMax 94-102).
mom30 errCross 5.8 / mom20 errCross 0 — flyAtSolid 0, nearG 0, solidT 448 at both.
storm + storm-reverse 0-0 (one storm-rev sample showed 10 transient invisibles; immediate
rerun of the identical profile returned 0 — harness sampling race at the reverse start, not
a site defect). stoprev@1400 pauseMove 0.0 drift 0.0. Mobile 390: no horizontal overflow.
Weight added this round: Special Elite 71KB + Fraunces variable 49KB (base64) -> file 968KB -> 1104KB.

## BIG BUILD — feature 6: STATEMENT MORPH (deferred to its own round)
Not implemented. Reason: it requires reviving the star population AFTER the extinguish/solidify
handoff and re-targeting it inside the round-4-verified physics loop, plus lengthening the pin and
remapping P (the smoothing accumulator must be split from the assembly progress, and the scene's
exit clause re-gated). That is a rewrite of the most delicate system in the document and belongs in
a dedicated round with a full canvas prototype in the lab first, per the standing lab-first covenant.
Design already specified: PACC accumulator + assembly remap P=min(1,PACC/MS), morph progress
PM=(PACC-MS)/(1-MS), pin 230vh -> ~296vh so assembly keeps its absolute scroll pacing, DOM stmt2
fades back to stars over the first 18% of PM, index-mapped target swap to a signature raster
("ORAN CARMON"), reverse symmetric, exit clause gated on PM>=1.

## BIG BUILD — feature 5b: drawer becomes a display case (owner note)
OPEN FILE removed from all four drawer cards (the diamond rail already jumps to any case, and the
drawer is meant to be walked through) — which also removes the click/lens conflict. The glass now
comes up on a resting mouse (90ms dwell on pointerenter, follows the pointer, hides on leave) and on
a short 130ms touch hold with move-cancel so vertical scrolling never flashes it. A standing
"⌕ INSPECT" hint sits where the button was, fading out while the glass is up. Lens key line
brightened 1.45x. Verified: 0 hcta, 4 hints, hover raises the correct card's glass (Eventer / ice),
leave hides; harness 420 + 700 clean.

## PERF ROUND — "everything must be a rocket" (owner)
Measured first, then cut. Profile showed 812KB of the 1104KB file was base64 fonts: fifteen
static faces (5x Inter, 3x JetBrains Mono, 5x Fraunces, Special Elite, FrauncesVar).
1. FONT PAYLOAD 812KB -> ~306KB. Five variable/subset faces replace all fifteen: Inter var
   (100..900), JetBrains Mono var, Fraunces var roman + italic (FrauncesVar retired — the kinetic
   titles ride the real Fraunces axis now, font-optical-sizing:none to keep display proportions),
   Special Elite subset via the Google text= API (53KB -> 23KB, only the glyphs the four analyst
   notes use). FILE 1104KB -> 582KB (-47%). Visual delta 31k px of 1.34M (variable vs static
   rasterization) — verified by screenshot, typography intact.
2. GRAIN: was a fixed full-viewport mix-blend-mode:overlay layer, i.e. a full-screen blend pass on
   every scroll frame. Now a plain .22 alpha layer — same texture, no blend.
3. SCROLL WORK: my kinetic-title and sealed-line loops each called getBoundingClientRect for every
   word/line every frame (forced layout). Both now read CACHED document positions, re-measured only
   on hard resize and font-ready, and both run in ONE shared rAF pass. Site engine untouched.
4. LENS: 90ms dwell removed — show() is now synchronous on pointerenter; transition .2s/.28s ->
   .11s/.16s. Probe: lens visible in the same tick, fully on within 50ms (was "a few seconds"
   on the owner's machine under the old main-thread load).
5. will-change:font-variation-settings dropped from the title words (layer hints cost more than
   they saved with a variable font).
6. The two 13,035px hero/section marquees pause via IntersectionObserver when off screen.
   FIRST ATTEMPT WAS WRONG: pausing every descendant of #hwrap/.minidrawer/.tk killed two drawer
   card reveals at the 700 pace (caught by the battery: inv 1-2 at y=4900). Narrowed to the two
   marquee elements only — 700 and 420 back to 0/0.
Battery after: 420/260/700 0-0, mom30 unchanged (errCross 5.8, flyAtSolid 0, solidT 448).

## DEEP PERF ROUND (owner: "everything must be a rocket") + loupe leak fix
Method: instrument first, cut second. Probes counted, per scroll frame and per zone:
DOM nodes, composited layers, canvas ops attributed PER CANVAS, layout reads attributed by
CALLER stack, style writes, and rAF schedulers.

FINDINGS
1. THE BIG ONE — the statement particle field was painting over the whole document.
   Its progress P is smoothed at 8.5% per call and only advances while the page moves, so after a
   fast scroll THROUGH the statement, P lagged far behind reality for dozens of frames and the
   scene kept drawing ~3,000 sprites/frame across sections nowhere near it — worst exactly during
   fast scrolling. Measured: xtix zone 3,083 drawImage/frame; files zone 986.
   FIX: viewport truth overrides the smoothed clock — if the pinned scene is off screen
   (below stTop+stH+0.4vh or above stTop-1.3vh) clear and return, whatever P believes.
2. Ten always-on rAF loops. The ghost-numeral loop read a rect per section every frame forever;
   moved onto the shared scroll pass with cached document positions and change-thresholded writes.
3. The dust canvas repainted a full-viewport bitmap every frame. Now half resolution
   (a quarter of the fill area, CSS-upscaled — soft points, no visible difference), with pointer
   coordinates and burst impulses converted to canvas space.
4. 49 forced compositing layers; released the 8 largest (the ghost numerals) now that they only
   write on real change.
5. ixhcv rope canvas was already viewport-gated — left alone.

RESULT (same probe, before -> after)
   canvas ops / frame        2,412 -> 274      (-89%)
   xtix zone canvas ops      3,311 -> 228      (-93%)
   layout reads / frame         76 -> 42       (-45%)
   file size (earlier round) 1,104KB -> 582KB  (-47%)
NO REGRESSIONS: 420/260/700 all 0/0, errors [], counters/pdraw/garc/bars 0, ticker alive,
canvas alive (cvMax 99-104) and cvEnd 0; mom30 errCross 0 / mom60 5.7, flyAtSolid 0, nearG 0,
solidT 448 — identical to the pre-round baseline; storm clean; stoprev pauseMove 0.0 drift 0.0.
Visual: statement, xtix and vault screenshots unchanged.

## BUG — the glass "flowed down the page" (owner screenshot: Medcoin lens over XTIX)
Root cause: the drawer is a horizontally-driven track. While the page scrolls, the cards slide
sideways UNDER a stationary pointer and each one fires pointerenter — so the lens was re-opened
every frame right after the scroll handler hid it, and since the pointer never moved it stayed
frozen at its last position, appearing to drift down the document.
FIX: the glass answers a deliberate pointer only — it opens if the pointer itself moved within
170ms AND no scroll happened in the last 280ms; any scroll hides it.
Verified against the exact scenario: deliberate move+enter shows; then 14 scroll steps while
every card fires pointerenter with a stationary pointer -> stays hidden.

## AUDIT ROUND — three verified defects fixed
Three independent agents audited the build (design/placement, content/reveal choices, gap analysis).
Three findings were CODE defects, each confirmed by me in the source before fixing:
1. The ritual bought nothing: `if(sc&&y+vh*.55>sc.b)markReviewed(...)` credited a file as REVIEWED
   just for scrolling past it, so the meter hit 4/4 with every stamp box still empty. Removed —
   reviewed now means stamped. Probe: a full-document scroll with no stamping leaves 0/4 (was 4/4).
2. `ceremony()` at 4/4 targeted `#ccstamp`, which had 0 occurrences in markup (2 JS references,
   4 orphan CSS rules) — it was dropped when the vault was built, so nothing ever happened at 4/4.
   Added `.vcommit` in the vault: ARCHIVE DISPOSITION / a dashed IN REVIEW · 0/4 stamp that ignites
   solid-white with scan bloom at 4/4 / "FOUR FILES REVIEWED — THE RECORD CLOSES".
3. Medcoin carried light-paper CSS on a dark card: analyst note #3A362E on #202127 = 1.33:1
   (WCAG floor 4.5:1), plus a near-black redaction bar and a dark gen3 mark. All five overrides
   re-toned for the dark card. Probe: note now rgb(221,217,206).

## ROUND 22 — XTIX markup repair, lamp de-duplication, and DEEP PERF 2
Two agents worked the same file concurrently with anchored-replacement discipline.

CONTENT/STRUCTURE
- One stray </div> in #xtix's STARTING POINT block closed the intake column early; the whole tail
  shifted one level and the chart, all of PART 2 and D REFLECTION rendered OUTSIDE .folder. Removed;
  #xtix now has the same child shape as its three siblings, document div balance 0. The evidence
  blocks correctly sit on the card now (inset 92/38px) instead of full-bleed — a real visual delta,
  deliberately not masked because the lamp repaints the card and any mask would break when lit.
  Three components were re-tuned for the new 988px host inside a min-width:901px block (phone untouched).
- All 12 lamp zones rewritten so the developed layer duplicates nothing visible in daylight. Proof:
  a rendered-DOM checker (verbatim + any shared 3-significant-word shingle, stopwords/figures excluded)
  reports 0 overlaps across 34 lines. Two zones use 2 bullets rather than pad.

PERFORMANCE — the real cause was style recalculation, not script (script was 0.65ms/frame)
- `--vsk` (the velocity shear) was written to :root every scroll frame. A custom property is INHERITED,
  so each write invalidated computed style for ~6,000 nodes; only two rules ever read it. Now written as
  an inline transform on the .sec>.wrap elements within one viewport. Vault style recalc 1.251s -> 0.128s
  per 119-frame burst.
- Scene scrubs, statement(), setW2, acts frame(), heroFx, the drawer loop and the rope/signature polls
  all now skip unchanged values or gate on cached geometry; the drawer loop was split read-phase/
  write-phase (it was forcing six synchronous layouts per frame). Cursor loops self-suspend.
- Bug found by probe: fit() on the flippable slips was the only resize listener outside the soft-resize
  guard — a resize regrew the document under a parked reader and Chrome's scroll anchoring moved the
  page. stoprev pauseMove was 5.9 with nobody touching the screen; now 0.0.
RESULTS (119-frame bursts, CDP metrics): long tasks during scroll 23 -> 0 across five zones; vault worst
frame 114.5ms -> 23.1ms, main-thread busy 2.511s -> 0.722s; files 98.8 -> 20.0ms; layout reads/frame at a
case 8.6 -> 0; style writes/frame 98 -> 6.4 (87 of the 98 were writing a value the element already had).
Visual proof: pixel-diff against a build with all 41 edits mechanically reverted — 0.04-0.09% on case and
vault views, inside the run-to-run control band.
Combined verification (both agents' work, final file): 420 and 700 both 0/0, errors [], ofx 0, all audits 0.



================================================================================
ROUND 23 — DOCUMENT-SCALE RESEARCH (two agents) + three lab mockups
================================================================================
BRIEF: owner asked to zoom out from component polish to whole-document ideas —
"effects only seen on award-winning sites", "something people won't forget".
Two agents in parallel: a world sweep (Awwwards/FWA/Codrops teardowns, jury
language, post-mortems) and a concept generator that read this file, the BUGLOG
and lab.html and priced seven concepts against this project's own metrics.

CONVERGENCE (independent, from opposite directions):
 1. THE ARTIFACT AT THE END. World sweep: not one career-scale site in the set
    hands the reader an object; the Wrapped literature says design the shareable
    artifact FIRST. Concept agent arrived at the same thing as "the examination
    record" and noted it is the only device that looks different for every reader.
 2. ONE MATERIAL IDEA, NO EXCEPTIONS beats twelve clever sections (PX PUSH's
    permanent CRT is the evidence). Here that material is film, and the document
    already speaks it in two isolated places.
 3. The lamp should not stay a per-folder secret — BUT the code-reading agent
    killed the global version the world sweep implied: a body class cannot reach
    the hard-coded fills in the four inline-SVG charts, the audit round already
    produced a real 1.33:1 failure from re-toning ONE card, and a class on <body>
    is exactly the whole-tree invalidation R22 deleted. Take the travelling lamp
    (develops only the current section), drop the global.

VERIFIED MYSELF BEFORE ACCEPTING (did not take the agents at face value):
 * site_mobile.html:3862-3863 — acts3 computes `frozen` from innerWidth<861 and
   returns at 3863, BEFORE markReviewed/ceremony/__markReviewed are defined at
   3923-3940. The four .stampbox elements call window.__markReviewed at 4798
   inside a try/catch, so on a phone they silently call nothing.
 * The markup default at line 2650 is literally `IN REVIEW &middot; 0/4`, and
   line 3922 (the only code that ever rewrites it) is inside the returned block.
   => After 24,674px of scrolling, the last thing a phone reader sees in the
   vault is a permanent 0/4. It reads as a failure state. REAL DEFECT, must be
   fixed regardless of which concept is chosen.
 * FRAMES={xtix:[11,12],oasis:[14,15],eventer:[17,18],medcoin:[20,21]} at 4942
   plus 26A/27A at 4990 — the document is already numbered as a 27-frame reel
   and never tells the reader. Mapping the 11 sections onto 27 frames lands all
   six canonical numbers exactly on the right content. The metaphor is not being
   imposed; it is being revealed.

BUILT (lab only — site untouched, per the lab-first covenant):
 29 THE REEL — machine edge + gate + live FRAME nn A / 27A counter. Motion is
    backgroundPositionY on a composited layer; counter writes only in the
    act!==railI branch that already fires once per section. +0 layout reads.
 30 THE CONTACT SHEET — 27 frames, real content harvested from the live DOM,
    every tile carries a FACT not a section name, per-case colour, EXPOSED ticks.
    Does not execute during scroll at all, so 98->6.4 and 23->0 cannot regress.
 31 THE EXAMINATION RECORD — four states (full / partial / untouched / return),
    silver on black inside the film rebate, LOCAL RECORD - NOT TRANSMITTED, and
    the empty state written as generously as the full one.

REJECTED IN THE LAB WRITE-UP (impressive but wrong here):
 * global second exposure (see 3 above) · animated file-closes — the static
   closed cover keeps ~90% of the payoff without putting contact details behind
   a transform at peak reader intent · restructuring the four cases onto a time
   axis — the subject is capability, not duration · scroll-as-camera push-in —
   scaling live text is blurry composited or a relayout per frame off it.

VERIFICATION: lab probe 0 errors, 27 frames, 0 empty facts, no horizontal
overflow, docH 18,516. Deployed to /lab/ (live 185,976 bytes, contains ex29-31).
index.html md5 13b3a8c3197ed6ec948f83c820e4588b and m/index.html md5
73f76891414f00ef0993b5062817e913 asserted unchanged locally AND re-fetched live
after the push. Backup: lab_backup_r23.html.



================================================================================
ROUND 32 — phone stamp repair shipped; reconnaissance for the ring/statement port
================================================================================
SHIPPED: the phone stamp defect found in R23. acts3 computes `frozen` from
innerWidth<861 and returns BEFORE markReviewed / ceremony / __markReviewed are
defined, so the four .stampbox elements called nothing on a phone and #ccstamp
kept its markup default. The last thing a phone reader saw after 24,674px was a
permanent "IN REVIEW - 0/4". A self-contained counter now lives inside the frozen
branch: same contract, dedupes by id, fires the seal + ceremony at 4/4, zero
scroll work. Verified at 390: 1/4 -> 2/4 -> 3/4 -> dup ignored -> CASE CLOSED,
.vcommit.sealed true. Verified at 1440: identical pre-existing behaviour, no
regression (desktop holds at 3/4 until the vault ceremony fires, as before).

RECONNAISSANCE recorded so the next round does not have to rediscover it:

* THE STATEMENT. The sentence is real DOM: #stmt1 (.l1) "One intelligence built
  the world." and #stmt2 (.l2) "Two will build the next.", inside .in > .pin >
  .pinh (a 230vh pin). A split() call turns both into per-word spans carrying
  .tw, and the particle assembly flies to those spans. The particle field is
  #dust, a fixed full-viewport canvas created in JS (there is no <canvas> in the
  markup at all - five are created at runtime: dust, ixhcv, a 32px sprite, ai2c,
  and an offscreen text-raster). To port exhibit 36: keep #stmt1/#stmt2, stop the
  assembly targeting .tw, re-lay the block left-aligned with the filament canvas
  beside it, and drive the morph off the same pin progress the scene already has.

* THE RING. Better news than expected. The lab component establishes its OWN
  perspective at .rg-stage and its own preserve-3d at .rg-ring, so an ancestor
  transform cannot flatten it - and the only risky ancestor property found on the
  chain is the `transform` on .sec>.wrap (the R22 velocity shear), which is
  harmless for this reason. What WOULD break it is a filter or opacity<1 landing
  ON .rg-stage or .rg-ring themselves, so neither may ever be given one. #files
  and .minidrawer carry no overflow/filter/contain that would interfere.

STILL TO DO, IN ORDER: (1) statement port, (2) ring replaces the horizontal
drawer, (3) the 25 .lampon rules converted to UV + .vfilm hidden inside folders +
the DEVELOPED/365nm wording. All three approved by the owner.


--------------------------------------------------------------------------------
STATEMENT PORT — the exact seam, located. Execution deferred, deliberately.
--------------------------------------------------------------------------------
The whole swap comes down to THREE call sites inside the statement pin scrub, all
within ~80 chars of each other around offset 531000:

    words(W1,.05,.30);                       <- line 1 revealed over pin .05-.35
    if(window.__ai2){window.__ai2(p);}       <- the particle assembly drives line 2
    else if(moved){words(W2,.40,.26);}       <- the no-particle fallback for line 2

plus one failsafe at ~536371 that force-settles everything:

    W1.concat(W2).forEach(function(w){w.style.transform='none';w.style.opacity='1'});

W1/W2 come from split(), which rewrites each line into
<span class="w" style="--wi:N"><i>WORD</i></span>. That is GOOD NEWS for the port:
the words are already individually addressable and already unbreakable spans, so
the exhibit-22 morph can be built on top of the existing structure instead of
replacing it. Per-character can be had by splitting inside each .w>i, which leaves
every other consumer of .w>i intact.

WHY I DID NOT EXECUTE IT IN THE SAME PASS. __ai2 is created elsewhere and owns the
#ai2c canvas; it is scrub-driven rather than self-running, so not calling it stops
it painting, but the canvas retains its last frame and must be cleared or removed,
and the assembly's audio hook has to be unpicked with it. On top of that the block
has to be re-laid left-aligned with a filament canvas beside it INSIDE a 230vh pin
- and this is the one section that consumed four mobile bug rounds (statement text
size, particles arriving before their sentence, the up-scroll jump, the
direction-change jump, and frame-rate-independent assembly timing). The swap is
maybe 40 minutes; the regression battery it demands - harness at 420 and 700 pace,
fps 60/30/20, ofx, totInvis, flyAtSolid/solidT against the 448ms baseline - is the
larger half, and shipping the swap without it would put the most fragile scene in
the document into the live file unverified.

Everything needed to execute is now written down. Next session starts at the three
call sites above.


--------------------------------------------------------------------------------
UV CONVERSION — applied to the work copy, NOT deployed. One element unresolved.
--------------------------------------------------------------------------------
DONE AND PROVEN: the 25 .lampon rules converted to a 365nm palette; ground #0E0A18
with a violet cone; ordinary ink receded (--fc/--emb/--brass/--ice -> #7F87CE);
charts drained violet; .vfilm retired inside folders; .frail kept faint (paper
fluoresces); lamp SVG violet; developed copy fluorescing #A6FFE0 / #57F5C4 with
bloom; wording now SWITCH ON THE UV LAMP / 365nm - FLUORESCING - 03 ZONES.

VAULT PROVEN UNTOUCHED: #final block md5 6ed90cc9eb9f5d3863bb4548aa69677a before
AND after; zero selectors join `lampon` and `#final`; `lampon` is applied only to
`folder`. 0 JS errors, no horizontal overflow.

UNRESOLVED, AND WHY IT IS NOT DEPLOYED: three elements reach the case accent
directly and stay emerald rgb(47,179,128) under the lamp - .tabrow .tA and
.clsband (the arrow rule .lamparrow s WAS fixed and is now violet). Escalation
tried, in order, all verified by re-render:
  1. `.case .folder.lampon .clsband{background:...}`            - lost
  2. the same with !important                                    - lost
  3. appended last in source order with !important               - lost
  4. `#xtix,#oasis,#eventer,#medcoin` prefix + !important        - lost
Nothing in an author stylesheet loses to all four unless the value is an INLINE
style. Next session: confirm with getPropertyValue on the element's style
attribute, then set it at toggle time in the existing lamp click handler with
el.style.setProperty('background','#241C48','important') - which beats inline -
or find and remove the inline source. One move either way.

Backup of the pre-UV work copy: site_backup_pre_uv.html.


--------------------------------------------------------------------------------
UV SOLVED — and the diagnosis is worth more than the fix
--------------------------------------------------------------------------------
Six escalations failed (plain rule, !important, last-in-source, ID-prefixed
!important, inline setProperty important, an independent listener) because I was
guessing instead of measuring. One measurement ended it. Two findings:

1. `.clsband` and `.tabrow .tA` NEVER DECLARE A COLOUR. They read
   `background:var(--fc,var(--emb))`. No override on the consuming rule can win at
   any specificity, with or without !important, because the value arrives through
   the variable. The variable has to be rewritten ON those elements.

2. Even after rewriting it - measured: --fc resolved to #241C48 on the element,
   the rule matched, no inline style - the computed background stayed
   rgb(47,178,127), ONE UNIT off the original emerald. That is a
   `transition:background-color .85s` sitting at ~0%: the scrub loop touches these
   nodes every frame and restarts the transition before it can ever arrive. The
   colour was correct the whole time and simply frozen on the way there.

FIX: rewrite --fc/--emb/--brass/--ice on the two elements AND `transition:none`
while lit. Verified: zero bright elements under the lamp.

OVERFLOW CHECKED PROPERLY: ofx is true in the PRE-UV backup in BOTH lamp states
too - the culprit is `.row r1` at 18,501px, the first-page marquee, pre-existing
and intentional. Not a regression; the new build is actually cleaner (no overflow
with the lamp off).

VAULT: #final md5 6ed90cc9eb9f5d3863bb4548aa69677a before AND after. All dead
enforcement code from the six failed attempts removed before shipping.


--------------------------------------------------------------------------------
THE RING — installed in the document, one framing tune left. NOT deployed.
--------------------------------------------------------------------------------
APPROACH: keep #hwrap's 330vh, #hpin's sticky, #htrack and its scroll driver,
measure()'s maxX contract, every kill-switch and the <=860px vertical fallback -
touch NONE of it. Replace only the four .hcard.hfolder cards with one room panel.
Because #htrack is already translated sideways by scroll, the pan from the intro
card into the room is the document's own machinery; no second mechanism.

VERIFIED AT 1440 AND 390: 4 cards, 4 armillary rings, 4 threads, 0 old folders,
perspective 1500px/1100px ESTABLISHED, stage filter none, stage opacity 1,
transform-style preserve-3d, 0 JS errors, no horizontal overflow, and document
height 26,482 - byte-for-byte the same geometry as before the swap.

THREE TRAPS HIT AND FIXED, each named by measurement not guesswork:
 1. `height:100%` on the room collapsed to zero - #hpin centres its children
    rather than stretching them, so a percentage resolved against an auto-height
    track. Fixed with an explicit 100svh + align-self:stretch.
 2. The room carried `rv`, so the reveal loop held it at low opacity - which both
    dimmed it and put an opacity on an ancestor of the perspective element. The
    room is a place, not a reveal unit; the class is gone.
 3. The "dark box over the card" was NOT a box. elementsFromPoint named it:
    SPAN.w inside .bigt inside .hcard.hintro - the intro card butting straight
    against the room, i.e. exactly the seam the owner rejected in the lab. Fixed
    with the same left-edge mask the lab used.

REMAINING, AND THE ONLY THING BETWEEN THIS AND SHIPPING: maxX =
htrack.scrollWidth - hpin.clientWidth measures 1411px, so the track keeps
travelling after the room has arrived and drags the ring off to the left. The pan
must END with the room filling the pin. Options, in order of preference:
  a. give .hcard.hroom the pin's width rather than 100vw, so the room's arrival
     and the end of the travel coincide;
  b. move .hcard.hend out of #htrack so maxX = intro width + gaps;
  c. clamp x in the scrub so it never exceeds (roomLeft - pinLeft).
Option (a) is one line and changes no JS.

Backup before the swap: site_backup_pre_ring.html.


RING - PAN FRAMING CLOSED. One artefact still open; NOT deployed.
FIXED: the end card lifted out of #htrack, so maxX no longer over-travels and the
pan ends exactly as the room fills the pin. Verified at 1440: room + stage + 4
cards + 4 rings + 4 threads, perspective 1500px, filter none, opacity 1,
preserve-3d, 0 errors, no overflow, docH 26,599 (+117 for the end card now in
normal flow). The armillary was also moved off CSS animation onto the existing
rAF loop, since an animation on transform gives an element its own stacking
context inside preserve-3d.

STILL OPEN: a dark rectangle sits over the upper right of the FRONT folder,
roughly 135x125, and it MOVES WITH THE ROOM (at one scroll position it measured
90x140 at a different offset). Ruled out by direct test: it is not the intro card
(that was a separate, real seam, fixed with the left-edge mask); not the CSS
animation (removing it changed nothing); not the armillary's Z position (seating
the core 46px behind the axis moved the rings but not the box). Next session:
elementsFromPoint at the box centre WITH the boot gate properly dismissed - the
one probe that named the intro-card seam in a single shot - then fix and ship.

Deliberately not deployed. A visible artefact on the front folder of the case
index is worse than waiting; /m/ currently carries the UV conversion only, which
is verified. Backup before the ring: site_backup_pre_ring.html.


================================================================================
THE STATEMENT — ported. Particles retired; the sentence migrates.
================================================================================
CHARACTERISED FIRST: statement(y) drives SPS (four file spines, p .02-.24),
words(W1,.05,.30) for line 1, window.__ai2(p) which hands line 2 to the particle
field via setW2, and memo at p .70-.84. Layout was text-align:center inside a
centred flex .pin.

CHANGED: SPS and memo untouched and still working. Line 1 became the morph host;
line 2 hidden, because the two sentences now share one line and take turns in it.
__ai2 is simply no longer called - it is scrub-driven, never self-running - and
#ai2c is never even created as a result. .in became a two-column frame: filament
left, text right, left-aligned, the pair centred.

MECHANIC: exhibit 22 exactly - every character blurs out upward on a 9ms stagger
and the next sentence arrives from below on the same stagger, 430ms cross, 5.0s
cycle, IntersectionObserver-gated. Words wrapped so a break can only fall between
them (splitting on characters alone lets the browser break inside a word - the
defect found when porting exhibit 22 into the lab).

TYPE: Fraunces' own axes, no new font file - WONK 1 for the splayed alternates,
SOFT 42 for the terminals, opsz 144 for display contrast. 52px desktop, 28px phone.

VERIFIED 1440 AND 390: 29 characters in 5 wrapped words, text correct, axes
correct, align left, line 2 display:none, #ai2c absent, filament drawing
(10,724 / 3,567 lit pixels), memo present, 4 spines present, 0 JS errors, docH
26,599 unchanged. Horizontal overflow measured against the pre-port backup:
IDENTICAL (sw 1473 / cw 1431, culprit .row r1 at 18,501px - the first-page
marquee, pre-existing and intentional).

Backup: site_backup_pre_stmt.html.


================================================================================
ROUND 33 — the owner's full note set: ring seam/drag/render, statement x5, cases
================================================================================
RING 1 (the visible frame): the room was a hard-edged panel. Now a soft radial field
meeting the page charcoal, with the mask feathering ALL FOUR edges (was left only).
Entry and exit verified by screenshot: no cut either way.
RING 2 (drag hijacking scroll): the cause was TEXT SELECTION - a mouse-down allowed
to start a selection lets the browser auto-scroll the page while dragging. Fixed with
user-select:none + preventDefault on mouse pointerdown + dragstart guard. The wheel
deliberately keeps native document scroll: there is no wheel handler.
RING 3 (folder render v2): laid-grain stock lit from the upper left, double shadow
(10px tight + 36px soft), crisper tab with a darkened foot, bigger ghost numeral at
opsz 144, tighter contact shadow.
STMT 1 (stuck scroll): the 230vh pin was 130vh of dead hold. Now 135vh (hold 35vh).
docH 26,599 -> 25,744.
STMT 2 (the missing face): the AXES were set but the FAMILY was not - Fraunces axes
on Inter do nothing. font-family:'Fraunces' added. THE actual bug.
STMT 3 (swap speed/exposure): desktop swap is now SCROLL-DRIVEN - __stSwap(p) called
from the statement scrub, A below p .32, B above p .5, hysteresis between - so a
scrolling reader always meets both sentences in order. Phones (scrub frozen <861)
keep a 3.0s in-view cycle. Migration faster: 270ms cross, 7ms stagger, 290ms hand-off.
STMT 4: MEMO - FROM THE ARCHIVE removed.
STMT 5 (two voices): .sA small matte grey-charcoal 34px/1.26, .sB large bone ink
60px/1.08, 500ms voice transition. Charcoal family only - no emerald in the line.
CASES (the ring's language): ghost numeral 01-04 and a blind conic seal in each
case's own colour via --cn + color-mix, tab brought to the ring tab finish
(gradient + darkened foot + top light). z-index:-1 children sit above the folder
ground because the scrub's transform makes every folder a stacking context. Under
.lampon both recede to dim violet - the UV invariant holds.

HARNESS LESSON RE-LEARNED, RECORDED: CSS transitions do not advance under
--virtual-time-budget. The "stuck at 49.96px" and the "swap did not fire" readings
were BOTH this - with --force-prefers-reduced-motion the same probes read sA=34px,
sB=60px, and both texts swap cleanly in both directions. The mechanism was proven
by direct __stSwap() call; production scroll drives the same path as every other
scrub scene in the file.

VERIFIED: 1440 + 390 zero JS errors; Fraunces family live; memo gone; user-select
none; ghost "01" rendered; vault md5 6ed90cc9eb9f5d3863bb4548aa69677a unchanged.
Backup: site_backup_pre_r33.html.


================================================================================
ROUND 34 — acting on the code review and the visual audit
================================================================================
TWO "BLOCKERS" DISMISSED WITH PROOF. Both reviewers audited the un-wrapped WORK COPY.
build_mobile.py supplies <!doctype>, lang="en", <meta charset=utf-8> and the viewport
meta. Measured on the LIVE file: UTF-8 decodes cleanly, 0 mojibake, 0 replacement
characters, Content-Type carries charset=utf-8, samples ("365nm ·", "— XTIX") correct.
LESSON: brief future auditors on the BUILT artefact, not on site_mobile.html.

VAULT BASELINE CHANGED, DELIBERATELY: 6ed90cc9... -> 1d64d003.... Diffed to prove it is
exactly one character, same byte length - the straight apostrophe in "The Builder's
Principles" became curly (audit item H16). Nothing structural.

FIXED, each verified by measurement:
* THE DRAG (the owner's own note, only half-fixed in R33). user-select stopped SELECTION
  auto-scroll, but the gesture still bubbled to #hpin's drag-inertia handler and threw the
  room ~166px sideways (measured: #htrack -926 -> -1092 over an 8-step drag).
  e.stopPropagation() on the stage. NOW trackMovedByDrag false at 1440/720/390 while
  ringSpin reaches 60.48deg - the ring turns, the room does not.
* TABLET CLIPPING was the ROOM, not the radius: width:100% resolved to 396px against an
  auto-width track, so 2 of 4 cards sat outside it at 720. Room is 100vw at every width
  now, with three radius bands (320 / 228 / 142). 0 clipped cards at 390, 480, 620, 720,
  860, 900, 1440.
* REDUCED MOTION - three defects, one cause: end states revealed without retiring the
  prompts that asked for them. "REVIEWED" printed over "PRESS & HOLD TO STAMP"; the lamp
  invited you to switch on something already on (needed !important - it lost on
  specificity first try); the statement showed its setup and never its payoff (now renders
  "Two will build the next." at 60px). The ring and filament ignored every kill switch
  because the CSS cancelled `animation` on .rg-ar, a property R33 removed when the
  armillary moved onto the rAF loop. Both gate in JS now; ringSpin measured 0.00deg.
* ANALYST NOTES broke mid-word - the same one-span-per-glyph defect as the statement.
  Words are unbreakable boxes (63 .an-w measured); the container carries the plain
  sentence as aria-label, because a screen reader given 90 one-character spans spells them.
* OASIS .stat was 759px inside a 287px column at 390. min-width:0 on the grid item.
* THE RING HINT rendered 13-190px past the right edge at 1440 (.rg-stage is 100vw inside a
  narrower pin). Moved left, lifted to AA.
* KEYBOARD: #files had 0 tabbable elements and #rail is display:none below 1150px. Cards
  are role=button, tabindex=0, labelled; Enter/Space opens, arrows turn.
* MEDCOIN: .clsband was 1.01:1 against its own folder; .clsctl 2.86:1 against 8.01:1 for
  the other three. Both corrected to the case's own paper accent / inherited --dim.
* Evidence-slip keys 2.97:1 -> #67624F. Copy: Prioritized global, curly apostrophe, Title
  Case on the tech title, phone CTA no longer claims the files "stand below".
* --ry collision renamed --hry (it is inherited and .rg-ar reads it).
* Desktop #ccstamp could hold at 3/4 forever; now writes 4/4.
* z-index writes inside preserve-3d REMOVED (measured "(none)") - the strongest lead on
  the iOS-only dark rectangle.

VERIFIED: 0 JS errors, no horizontal overflow, at 390/480/620/720/860/900/1440.
Backup: site_backup_pre_r34.html.
STILL OPEN from the audits: the ~55KB dead-code sweep, H5 statrow alignment, H9-H12 case
consistency, remaining M/L contrast and copy items, and the performance audit (running).

================================================================================
ROUND 35 - THE DEAD-CODE SWEEP AND THE PERFORMANCE AUDIT (-19,708 bytes)
================================================================================

TWO CORRECTIONS TO THE PROJECT'S OWN MEASUREMENT PRACTICE, both from the perf audit
and both accepted:

 1. EVERY TIMING NUMBER THIS PROJECT HAS EVER PRODUCED UNDER --virtual-time-budget WAS
    MEASURED AGAINST A STOPPED CLOCK. Proof: eight identical CPU burns inside rAF - the
    first reported 217.7ms, every later one 0.0ms; the long-task observer caught 1 of 8.
    The "0 long tasks / worst frame 23.1ms" baseline was an artifact. Real-time CDP only
    from here (perf/drive.js, perf/shot.js).
 2. site_mobile.html IS A BODY FRAGMENT. Loaded bare it renders in QUIRKS MODE at a
    1022px layout viewport, where innerWidth<861 is false and the ENTIRE mobile path -
    frozen-B, the reveal tuning, the desktop kill switches - silently never runs. Only
    the wrapped build may be measured. This invalidated a full batch and it will catch
    the next person too.

DEAD CODE REMOVED (all four proven dead by instrumentation, not by reading):
* THE PARTICLE FIELD, ~390 lines. Wrapping createElement and getContext proved it: the
  only runtime-created canvas is #dust (plus #ixhcv on desktop). #ai2c is never built, no
  context is ever taken, the 1,000-object array never allocated. A closed circle kept it
  unreachable - ensure() is called only from window.__ai2, and __ai2 only from a resize
  listener that ensure() itself registers. Its session-long document.mousemove listener
  went with it.
* .seccover - four CSS rules, ZERO elements. The scroll loop iterated an empty NodeList
  every frame and measure() walked it twice. One of the dead rules carried a will-change.
* THE DRAWER LOUPE - it queried `#files .hfolder`; the ring replaced every folder in that
  track, so it returned on its second line. Module, stylesheet and INSPECT hint gone.
* THE INDEX-BOARD ROPES - THE ONLY DEAD CODE THAT STILL COST FRAMES. Every forced reflow
  in the document (210, all desktop) came from this one block writing ixhcv.width and
  then reading two rects in the same frame. It had drawn nothing since the ring landed:
  the ropes anchor to `.hfolder .hlip` and there are zero of those in the markup.
* @keyframes rgArm and its three cancel rules - R33 moved the arms to rAF; nothing has
  declared `animation` on .rg-ar since.

THE FOUR MEASURED FIXES:
* THE FILAMENT, 5.4x FASTER. It issued one strokeStyle assignment and one beginPath+
  stroke PER LINK - ~2,470 path submissions a frame, each preceded by a freshly built
  rgba() string the engine then re-parsed. Alpha is now quantised into 24 buckets whose
  colour strings are built ONCE; links are counting-sorted and each bucket is one path,
  one stroke. Same for the node dots. MEASURED, isolated rAF callback, parked at 390:
  2.233ms -> 0.416ms per frame, worst frame 10.4ms -> 1.0ms, canvas ops 10,141 -> 4,547
  per frame. Quantisation step is .0217 on a filament whose brightest strand is .26.
* THE RING: THIS WAS THE --vsk BUG REPRODUCED ONE LEVEL DOWN, and I wrote the rule that
  should have caught it. --spin was written to #rgRing every frame; it is read by exactly
  one selector, #rgRing's own transform - but a custom property is INHERITED, so every
  write invalidated computed style for 108 descendants. transform is not inherited. The
  CSS composes exactly that transform, so the output is pixel-identical - PROVEN: parked
  in oasis where the loop is stopped, all four arm matrices and the ring matrix are
  BYTE-IDENTICAL between builds. --d stays a custom property (22 descendants read it) but
  is now gated on the value changing. MEASURED: 17 -> 7.5 style writes/frame.
  THE BROADER RULE: never write an inherited custom property, on any element with a large
  subtree, in a per-frame loop.
* THE DUST had NO stop condition of any kind - the rAF was re-armed OUTSIDE the
  !document.hidden guard, there was no cancelAnimationFrame anywhere, and an
  IntersectionObserver could not help because the canvas is fixed and full-viewport by
  construction. It now stops on a hidden tab and fades out after ~7s of no scroll and no
  pointer. MEASURED over an 11s dwell: 42,900 -> 24,180 canvas ops, 65 -> 36.7 ops/frame.
  Its resize listener was also the only one in the file bypassing __mSoftRz.
* POINTER PARALLAX ran on every touch scroll - found only under a REAL compositor gesture,
  invisible to scrollTo. A finger emits pointermove, so the loop stayed awake for the whole
  scroll writing 18 inherited custom properties a frame across 2,281 of 2,287 frames:
  style writes 4,443 -> 41,040, nine times everything else combined. Now pointer:fine only.
* will-change on .folder promoted seven large subtrees from load; now scoped to .wcv,
  toggled by an IO with 300px of margin so it is always set before the element can be seen.

A MEASUREMENT TRAP WORTH RECORDING: the first files-zone A/B showed r35 at 56.3fps against
r34's 59.1 and I nearly went hunting. Repeating with the order reversed showed 59.7/60.0
for both. The machine hosts the owner's real Chrome (74 processes); absolute fps on this
box is noise. Paired, same-run deltas are the only trustworthy figures - and per-loop
callback time, which is what the 5.4x above rests on.

OPEN, MEASURED, NOT FIXED - THE RING'S DEPTH SORT:
The far card's back face intermittently paints IN FRONT of the near card's front face,
cutting "FILE 01" and slicing XTIX in half. CAUGHT ON CAMERA: title band 44.0% dark in the
suspect frame against 4.0% at spin 0. It is PRE-EXISTING - r34 and r35 captured at the same
moment are identical - and it is angle-dependent, not reproducible on demand (frozen at 0,
-14 and +14 degrees all render correctly; 6 live captures clean). Note that elementsFromPoint
named .f-back as the top hit at every probe point, which is a FALSE LEAD: hit-testing ignores
backface-visibility. Not fixed here, deliberately: an unverified structural change to 3D
sorting does not belong in the same round as a verified performance sweep.

================================================================================
ROUNDS 36-37 - THE CASE-FILE CONSISTENCY AND CONTRAST ITEMS
================================================================================

FOUR OF THE REPORTED FINDINGS WERE NOT DEFECTS. Checking each against the document
before editing is the whole point of this round:

* ".plabel appears in only 2 of 4 cases" -> CORRECT AS IS. Only XTIX and Oasis are
  two-part cases; the label literally reads "PART 1 OF 2". Adding it to the single-part
  files would be the error.
* "three different rubric numbering systems" -> there are TWO, and the pair IS a system:
  single-part cases run 01..0N straight through, two-part cases restart with letters for
  part two. XTIX and Oasis are identical to each other. Not drift.
* "Eventer skips zones 04 and 05" -> MY OWN MEASUREMENT ERROR, and I shipped it into the
  work copy before catching it. My survey regex required a `.d2` span inside `.zr`, and
  Eventer's zones 04 and 05 do not use it, so they were invisible to the scan. I renumbered
  06->04 and 07->05 and the live DOM then read 01,02,03,04,05,04,05 - two duplicate pairs
  where there had been a complete sequence. Reverted before deploy. THE LESSON IS THE SAME
  ONE AS THE BOOT GATE: a static scan of the source is not the document. Read the DOM.
* twelve of seventeen contrast "failures" -> a walker that looks for backgroundColor cannot
  see a surface painted by background-image. Every "dark text on charcoal" hit inside a case
  folder is dark text on CREAM PAPER at ~12:1. And .secnum and the marquee report 1.00
  because their colour genuinely is transparent - they are gradient-clipped display
  numerals, aria-hidden, carrying no information.

WHAT WAS REAL AND IS FIXED:

* H5, AND IT WAS NOT A SPACING PROBLEM. MEASURED at 1440 and 390: the gap between the
  "$9M+ ARR" headline and its own caption was 330px and 340px, against 8px for the two
  stats beside it. Cause: the evidence slip anchors to the element holding the counter,
  which for the two stat hosts IS THE NUMBER, and inserted immediately after it - so the
  slip and then the analyst note landed BETWEEN the number and the label that names it.
  The block read as five unrelated objects. The anchor now walks past any caption that
  immediately follows before inserting; where a host has no caption after it (the two zone
  hosts) it is a no-op. Verified: children are now bignum, biglbl, biglbl, slipflip,
  an-note, and the gap is 8px at both widths.
* The fourth case was headed FOUNDER CASE STUDY while the other three were CASE STUDY
  01/02/03, so the series stopped at three. Now CASE STUDY 04 · FOUNDER - the index is
  restored without losing the distinction.
* CONTRAST, five items, all on solid backgrounds at full opacity, all measured before and
  after: .es-h 2.97 -> 4.94 (now the same #67624F as the slip keys corrected in r34);
  .rt-date and .rt-end i 3.21 -> 6.40 (the last literal #6B6E76 outside the vault);
  .rt-lbl 4.46 -> 6.62; .es-stamp 3.91 -> 6.40 (the .85 opacity was doing the damage -
  composited over paper it LIGHTENS the green; full opacity, slightly deeper green, the
  stamped look intact); .gen3 span 3.60 -> clear. On that last one the blur stays: it is a
  third-generation microfilm copy and should look like one. But the line it degrades reads
  CONTENT VERIFIED, and the reader has to be able to read it.
  FINAL SWEEP: 0 failures on solid backgrounds, down from 5. 0 JS errors, 0 horizontal
  overflow at 390.

DELIBERATELY NOT TOUCHED:
* #final .vc-s still uses literal #6B6E76. It is inside the vault, which has a tracked
  hash, and the owner's standing instruction is to leave the last page alone. Flagged, not
  changed.
* Medcoin's zone 03 is headed WHAT WE BUILT where XTIX has WHAT I BUILT. That is a claim
  about who did the work, not a formatting inconsistency, and it is the owner's account of
  his own career. Raised as a question, not edited.

================================================================================
ROUND 38 - THE OWNER'S TWO NOTES: THE ROOM AS A SURPRISE, THE SECOND SENTENCE
================================================================================

1. THE ROOM WAS NEVER HIDDEN, AND A LINEAR PAN COULD NOT HIDE IT.
   MEASURED at 1440 before touching anything, stepping through the whole pin: at hp=0 the
   room's left edge sat at 758px, so 682px of it - 47% of the screen - was already on show
   before the reader had scrolled a pixel. Two independent causes:
   (a) GEOMETRY. The track lays out [12vw pad][34vw intro][5vw gap][100vw room]. The room
       begins at 51vw. It was never off screen.
   (b) THE PAN WAS LINEAR, and linear cannot give a reveal at this scale. A 100vw room
       crossing a 100vw viewport spends ~90% of the available travel merely ENTERING, so
       however far right it starts its leading edge appears almost at once and then creeps
       for the rest of the section. Pushing it right alone would have moved the leak, not
       closed it - which is why the margin is only half the fix.
   58vw of lead, the trailing 12vw of track padding dropped (nothing follows the room since
   r34 moved the closing card out to .hendflow, and that padding was what made the pan
   overshoot and leave the room 197px off-left at the end), and the pan now runs
   HOLD -> SWEEP -> SETTLE on a smoothstep over hp 0.20..0.75.
   VERIFIED at 1440 and 1100, eleven steps through the pin:
     hp 0.0-0.3  room visible = 0px          (the intro card alone; the room is absent)
     hp 0.4-0.6  333 -> 1169px               (the sweep)
     hp 0.7-1.0  1416px, left frozen at -24  (settled, 98.3% of frame, no further travel)
   Phone is untouched and must be: the <=860 rule sets margin:14px 0 which resets the lead,
   and the whole branch is behind !mob.matches. MEASURED on the phone build:
   marginLeft 0px, 0 JS errors, 0 horizontal overflow.
   MEASUREMENT NOTE: the first pass at this returned identical numbers at every one of the
   eleven steps. The pan is rAF-driven, so a synchronous scrollTo loop reads a stale
   transform every time - no frame runs between the steps. shot.js now supports an async
   probe (awaitPromise) marked with an /*ASYNC*/ tag.

2. THE TWO SENTENCES REALLY WERE THE SAME COLOUR, and the cause was a dead argument:
   render(txt,em) is called with em=false at ALL THREE call sites, so .em2 never applied to
   anything and the only difference between the lines was #8E939C against #F2F1ED - grey
   against off-white, which on charcoal reads as the same colour twice. The rule had been
   sitting there unreachable.
   The second line now carries a PER-CHARACTER RAMP rather than a flat swatch: it holds the
   document's ink through "Two will" and then commits, glyph by glyph, into the emerald the
   dossier is named for, so the sentence about what comes next turns into it as it lands.
   It rides the existing stagger, so the colour arrives WITH each character.
   VERIFIED: first six glyphs rgb(242,241,237), last glyph rgb(47,179,128) exactly, worst
   contrast anywhere on the line 6.52:1.
   FASTER, as asked: stagger 7ms -> 5ms per glyph (end to end 133ms -> 95ms), hand-off
   290ms -> 235ms, glyph transition .27s -> .23s. The section is not pinned and does not
   pause - the swap is simply quick enough to be seen.
   .em2 removed; it was unreachable.

================================================================================
ROUNDS 39-40 - THE RING'S DEPTH SORT. R39 WAS WRONG; R40 IS THE FIX.
================================================================================

THE DEFECT: at many ring angles the far card's BACK face painted over the near card's
FRONT face, cutting through "FILE 01" and slicing the file name in half.

THREE DETECTORS, TWO OF THEM WRONG. Recording the failures because each looked convincing:
 1. elementsFromPoint named .f-back as the topmost element at every probe point. FALSE:
    hit-testing ignores backface-visibility, so it reports geometry that is never painted.
 2. "count dark pixels inside the front card's bounding box" gave 10 failing angles peaking
    at 36-48deg. FALSE: a card rotated 45deg leaves large empty corners inside its own
    axis-aligned box and other cards legitimately show through them. The metric peaked at
    exactly the angles of maximum rotation, which should have been the tell.
 3. WORKS: paint every front face one test colour and every back face another; capture each
    state TWICE - once normally, once with all other cards hidden - and count pixels that
    are front-face colour in the second and back-face colour in the first. No bounding
    boxes, no heuristics.

AND A FOURTH TRAP, WHICH IS THE REAL LESSON OF THIS ROUND. I built a harness that PINS the
ring to exact angles for determinism. It is deterministic and it is not the document: the
ring in the file never stops moving. R39 (backface-visibility:hidden on the threads) scored
0 of 90 pinned angles and I reported it as fixed. Driving the ring LIVE, it scored 35,122
leaked pixels against a 33,998 baseline - NO IMPROVEMENT AT ALL. The pinned harness could
not see it because the guilty thread at those moments FACES the viewer, so declining to
draw its back changes nothing. R39 is reverted, not stacked on.
Same trap, same round: the pinned sweep said desktop was never affected (0/30 at 1440).
Live at 1440, the baseline leaks in 8 of 10 frames, worst 10,377px. It was never phone-only.

WHAT IT ACTUALLY IS: each .rg-thread is a 216x3px plane laid radially and turned 90deg from
its own card - so the FRONT card's thread lies EDGE-ON to the viewer, its plane containing
the view axis, and it cuts through every card plane in the ring. Intersecting polygons force
the engine to split geometry into a BSP tree, and a bad split is how a face 284px further
away comes out in front. Measured live, hiding each thread in turn: thread 0 alone takes the
leak from 7,606 to 57; the other three change nothing.

ELIMINATION LOG, every candidate measured, not reasoned about:
  z-index on the cards, quantised          no effect  - the 3D sort outranks it
  painter's order, deepest sibling first   no effect  - likewise
  push the back face 40px deeper           WORSE, 9/30 and up to 16.5% of the face
  hide the side faces / the tab box        no effect
  thread opacity forced to 1               no effect  - so NOT the flattening rule
  thread shortened                         no effect  - so not its reach either
  retire the far card's back face          works, but costs 94,295px of picture
  THREADS OUT OF THE 3D CONTEXT            THE FIX

THE FIX IS STRUCTURAL: the four threads move into a wrapper carrying transform-style:flat.
That ends the 3D rendering context at the wrapper, so they composite as ONE plane and can
slice nothing, while still sorting against the cards by depth - which is what a connector at
the ring's centre should do anyway. The wrapper is 0x0 at the ring's own origin, exactly
like .rg-ring, so every thread's left/top:50% resolves identically and no layout moves.

MEASURED LIVE, 20 frames, the same angle sequence for each build:
  r38 baseline   14/20 frames leaking   worst 6,682   total 33,998
  r39 backface   15/20                  worst 6,719   total 35,122   (no help)
  r40 wrapper     6/20                  worst    68   total    449   (76x better)
The residual 40-68px hits are the bounding-box metric's own false-positive floor.
At 1440: 39,852 -> 194. Threads and their pips still render; 0 JS errors; 0 overflow.

================================================================================
ROUND 41 - THE SCROLL STICKS, AND 789px OF SIDEWAYS SCROLL NOBODY HAD SEEN
================================================================================

HOW "IT STICKS" WAS MEASURED. Not frame rate - the document already holds 60fps and had
done for several rounds, which is exactly why the owner's report and my numbers disagreed.
A pinned section that sticks is one where the reader keeps scrolling AND THE PICTURE STOPS
CHANGING. So: step through the section in even scroll increments, capture each step, diff
consecutive frames, and look for runs of near-zero difference.

ONE CORRECTION WAS NEEDED BEFORE THE NUMBERS MEANT ANYTHING, and it is the same trap as the
stopped clock and the pinned ring: the dust, the marquees, the armillary AND THE FILAMENT
all animate on their own, so they register as "change" at every step even where scrolling
contributes nothing. The first statement run, with the filament still running, reported 0
dead steps - it was measuring the filament, not the document. With everything self-animating
suppressed, what is left is the document's actual answer to the reader's finger.

WHAT IT FOUND at 1440x900:
* #files: 4 dead steps in a row = 341px of scrolling that changed 93-450 pixels against a
  247,930 maximum. THIS ONE WAS MINE. Round 38 held the pan at zero for the first fifth of
  the pin to keep the room a surprise - and during that hold the room is off screen and the
  intro card is stationary, so nothing whatsoever moves.
* #statement: 6 dead steps in two runs of 107px, at 41-47% and 56-62% of the section. Across
  the whole pinned travel the only scroll-driven events are the sub-line spans (p .02-.29)
  and the single morph at p .50. Between and after them the scrub computed new numbers every
  frame and wrote identical pixels.
* Phones were never the problem and are untouched: below 861px both pins are frozen and the
  sections scroll normally. 0 dead steps at 390 before and after.

THE FIXES
* #files: the hold becomes a slow start. The room's absence is the job of the 58vw of lead,
  not of a dead pan - so the mapping keeps a real slope at zero (the intro card slides from
  the first pixel of scroll), eases through the middle, and completes at 80% so the last
  fifth is still a settle with the room square in the frame. VERIFIED the surprise survives:
  0px of room visible at hp 0.0 and 0.1, entering at 0.2, filled from 0.8.
* #statement: the pin shortened 135vh -> 115vh so the scroll budget matches what happens in
  it, plus a slow counter-drift - the sentence rising 84px, the filament sinking 48px across
  the pin - so every pixel of scroll moves something. Two transform writes on two elements,
  neither inherited. The dead words() helper went with it; nothing had called it since the
  morph took the sentence over.
MEASURED AFTER: #statement 6/34 dead -> 0/34. #files 4/40 -> 0/40. Mobile 0/30 both.

THE HORIZONTAL SCROLL, found by the full re-audit and PRE-EXISTING:
window.pageXOffset reaches 789 at 1440 from Oasis onward - the page really does scroll
sideways. Identical in the round-34 build, so no recent round caused it. Elimination:
disabling every ::before/::after fixes it, and so does clipping .folder - the source is a
pseudo-element inside the case folders that is meant to bleed past them.
NOT fixed at the viewport: html{overflow-x:clip} kills the sideways scroll AND BREAKS EVERY
STICKY PIN - measured, pinTop went from a constant 0 to -2070. body{overflow-x:clip} is
worse still, because it replaces the `hidden` that was propagating to the viewport.
.folder{overflow-x:clip} leaves every pin at 0 and takes 789px -> 42px.
STILL OPEN: the residual 42px is .bigmq, the tilted marquee bands - 1525px wide by design,
direct children of body, so nothing above them clips. Fixing it needs a wrapper per band.

================================================================================
ROUNDS 42-43 - THE FILAMENT JUMP (mine) AND THE ROOM'S DARK HALO
================================================================================

1. THE JUMP WAS MINE, FROM ROUND 41. Tracing the filament's screen position step by step:
   it tracks the scroll at -36px per step, then inside the pin it moves +7px per step -
   DOWNWARD, while the reader is scrolling down - for four steps, then snaps back to -36.
   The counter-drift added in r41 to close the dead zones ran the filament AGAINST the
   scroll. Two direction reversals in one section is exactly what reads as a jump.
   r42 pointed both halves the same way (up, at different rates - parallax is in the
   difference between the rates, not a difference of direction): 4 wrong-way steps -> 0.

   r43 THEN REMOVED THE PIN'S EDGES TOO. Two rate changes were left, at entry and exit -
   the scene going from -36 to -10 per step the instant sticky took over. A rigid pin
   cannot do anything else. So the hold was given a speed profile instead of an edge:
   writing the element's offset as T(p), its apparent speed is T'(p)/span, so choose
       f(p) = 0.2 + 0.8*cos^2(pi*p)     f(0)=f(1)=1, f(0.5)=0.2
   and integrate once:
       T(p) = -span * (0.6*p + 0.0637*sin(2*pi*p))
   One sine per frame. At both boundaries the scene moves exactly as fast as the page, so
   there is nothing to step over; through the middle it slows to a near-hold.
   MEASURED at real scroll granularity (5px steps across the 135px pin): -5,-5,-5 ... easing
   to -1.0 at the centre and back to -5, WORST RATE CHANGE BETWEEN CONSECUTIVE STEPS 0.5px,
   0 wrong-way steps. Dead zones still 0/34.
   NOTE ON MEASUREMENT: at 36px sampling this still reported "2 discontinuities". The pin is
   only ~4 samples wide at that resolution. The 5px scan is what showed the truth - sampling
   coarser than the feature being measured invents steps that are not there.

2. THE ROOM NEVER MET THE PAGE. Sampling rendered pixels down the room's interior: the page
   is rgb(25,26,31) and the room's radial gradient ended at rgb(11,12,16) - fourteen levels
   darker. The edge mask then cross-faded that dark edge over the page, so every edge the
   reader entered or left through carried a dark halo (measured rgb(17,18,24) at the floor
   against rgb(25,26,31) at the seam). The room was landing on black where it should have
   been landing on the document.
   Outer stop is now the document's own charcoal, the centre stays lifted, and the mask
   ramps start sooner and run longer.
   MEASURED, deviation from the page colour through the room: before -8 to +8 (a dark band
   top and bottom); after 0 to +16 - it never goes darker than the page, and reaches it
   exactly at every seam.

================================================================================
ROUND 44 - THE RING ADOPTS THE DOCUMENT'S FOLDER (the owner's inversion)
================================================================================

The plan had the four case sections learning to look like the invented cream card. The
owner turned it around: the RING carries the actual case folder instead. It is the better
call - the object the reader turns is now the object he is about to read at full size, so
the ring stops making a promise the document then has to keep.

KEPT, because it is what makes the ring an object rather than a picture: the six-face box
and its 11px thickness, the tab welded to the body, the depth fog on --d, the cast shadow,
the armillary, and the threads' flat plane from r40.

THE SURFACE IS NOW THE CASE FOLDER, built from its real furniture in its real order:
the tab moved to the LEFT (the case folder's tab is top-left; the ring's was mirrored right
for nothing but symmetry) and now reads "> FILE 0N"; the classification band; the control
row carrying the file's OWN control number and copy count, read out of the document
(X-26-0101 03/12, O-26-0102 05/12, E-26-0103 07/12, M-26-0104 09/12); the punch rail; the
name; the category; and the opening zone heading with its first lines - Medcoin's correctly
reads THE VISION where the other three read THE SITUATION.
REMOVED: the guilloche, the wax seal and the ghost numeral. They were invented for the cream
card and the case folder has none of them; keeping them would be the same mismatch in the
other direction.

VERIFICATION, and one scare worth recording. The bounding-box detector first reported the
depth sort had regressed (worst leak 68 -> 497). It had not: that run sampled 12 frames
against the baseline's 20, so it was comparing different ring angles. Run properly, 20
frames each on the same angle sequence:
    r43 (before)  6/20 frames leaking, worst 284, total 917
    r44 (after)   6/20 frames leaking, worst 189, total 644
The card redesign is slightly BETTER, not worse. Dead zones identical (1/40 both, the one
step being variance around the 2%-of-max threshold rather than a real hold). 0 JS errors,
0 horizontal overflow at 390 and 1440.

ALSO RECORDED: the PINNED sweep says 9/30 for r40, r41, r43 AND r44 alike, while the live
harness says r40 improved things 76x. The two harnesses have disagreed since r40 and the
live one is authoritative - the ring in the document never stops moving. The pinned rig
freezes the armillary at an attitude the animation only passes through.

================================================================================
ROUND 45 - THE RING CARRIES THE THEATRE FOLDER (r44's face replaced)
================================================================================

I had read "bring the document's folders into the ring" as the CASE folder - the charcoal
panel inside each section. The owner meant the COLOURED folder from the scene that plays
before each case, and sent the reference. Both live in the document, so both readings were
literal; his is the one that counts, and r44's charcoal face is replaced here.

His instructions, each taken exactly: the reference's design (solid case colour, dark ink,
tab top-left); NO copy but the name and the number; the name LARGE; NO VOLUME; LANDSCAPE
(268x186 against 214x288); and the threads gone with the armillary rings kept.

THE CONSEQUENCE WORTH NAMING: removing the volume and the threads deletes every plane that
crossed another inside the ring's 3D context. The depth-sort defect that took rounds 39 and
40 to chase is now structurally impossible - MEASURED, exact detector, 0 of 30 angles and a
worst leak of 0px, against 13 of 90 before r40 and a residual after it.

FOUR DEFECTS I MADE AND CAUGHT, each of a kind worth remembering:
* A DANGLING HALF-RULE SWALLOWED THE WHOLE CARD. My thread removal cut to the end of the
  LINE holding `.rg-thread:before{`, but that rule spans two lines, so its second half was
  left at top level. CSS error recovery then treated `background:...;box-shadow:...}` as a
  selector hunting for its `{` - and it found `.rg-card`'s, consuming the entire card rule.
  Symptom: --W read as "", transform read as "none", every folder 0x0 and invisible. Brace
  and comment counts were both balanced, which is why neither check caught it.
* FILE 0N WAS INVISIBLE because I hung it on `.t-front:after`, and `.tb:after` already owns
  that pseudo for the depth fog - whose opacity is calc(--d * .72), i.e. ZERO at the front
  of the ring. The number was being rendered at opacity 0 exactly where it must be read.
  It has its own element now and the fog keeps its pseudo.
* A SINGLE PLANE LEFT THREE OF THE FOUR CARDS INVISIBLE - edge-on at 90 degrees, turned
  away at 180. backface-visibility on the CHILDREN does not fix it (they are not in a 3D
  context of their own): the names simply appeared mirrored. The folder now has a real
  reverse - a second plane 1px behind, plain colour, nothing printed. Two parallel planes,
  so nothing can cross and nothing z-fights.
* THE BOUNDING-BOX DETECTOR reported 6/14 frames leaking after the change. False: a
  LANDSCAPE card has a wide axis-aligned box that legitimately contains its neighbours. The
  exact silhouette detector, which is immune to that, reports 0/30.

VERIFIED: 0 JS errors and 0 clipped folders at 390/620/860/1440 (the one 12px sliver at 390
is an edge-on card inside the room's own edge fade). Horizontal overflow unchanged at 42px,
the pre-existing .bigmq tilt.

================================================================================
ROUND 46 - THE FOLDER OPENS SIDEWAYS
================================================================================

It was hinged along its TOP edge and rotated away from the reader - rotateX(98deg), origin
50% 0. That is a laptop lid. A folder is hinged at its spine.
  origin  50% 0 -> 0 50%     the left edge
  axis    rotateX -> rotateY, and NEGATIVE so the free edge comes toward the reader before
                              it travels left, the way a cover is actually lifted
  angle   98 -> 104deg       past vertical, so the cover rests open instead of being held
  easing  linear -> eased    a cover has weight and should not track the finger one to one

THREE THINGS HAD TO BE MEASURED RATHER THAN GUESSED.

1. THE FIRST ATTEMPT PUT A GREEN WEDGE ACROSS A THIRD OF THE FRAME. At 116 degrees off a
   left hinge the cover's free edge ends up ~610px TOWARD THE CAMERA, and .otroom's 1500px
   perspective magnifies that by 1.7 - so the cover stopped reading as a cover and became a
   shape. Fixed by deepening the stage to 2600px, moving the perspective origin to 42%, and
   stopping at 104 rather than 116.

2. .ots CLIPS AT THE VIEWPORT, and a 680px cover swinging off a left hinge reaches about
   300px past the folder's own left edge - off screen at anything under ~1200px wide. So the
   FOLDER TRAVELS RIGHT as the cover opens, by 19% of its width (13% on narrow screens), and
   the angle eases back there too. That is also what happens in life: opening a folder moves
   its centre of mass and the spread re-centres.

3. THE WHOLE OPENING WAS HAPPENING IN A THIRD OF A SCREEN. Measuring the cover's actual
   angle against scroll showed 0 -> -104deg between .22 and .38 of the section, then nothing
   for the remaining 60%. The band ran .38-.80 of the DRIVER's p, but the driver's p is
   measured against the sticky travel (85vh) while the section is 185vh, so it saturates at
   about 0.4 of the section. Widened to .34-.94, and the gesture now takes ~2.5x the scroll.

WHAT MAKES IT READ AS AN OBJECT RATHER THAN A ROTATION: a crease at the spine so the hinge
is a place and not an axis; the cast shadow RETREATS toward the spine as the cover lifts
instead of fading where it stands (the veil became a directional gradient that slides); a
sheen across the cover that the perspective turns into a moving highlight for free; and the
inside of the cover darkening toward the fold, where less light reaches.

VERIFIED: all four theatres open sideways and stay inside the frame (folder left 441-458 at
1440, right edge in frame); 0 JS errors; dead zones 1/40, the same variance-level reading as
the other sections. MOBILE IS UNTOUCHED - .otx is display:none below 861px by existing
design, so this is a desktop-only scene and always was.

================================================================================
ROUND 47 - THE IMPROVEMENT PASS: statement, ring room, opening
================================================================================

Each of the three was CAPTURED AT FOUR POINTS AND LOOKED AT before anything was changed.
Both of the big findings were things no metric had reported, because nothing was broken -
they were simply not good enough.

--- THE STATEMENT -------------------------------------------------------------
FOUND: the whole scene is over in the first eighth of the section and the rest is an empty
black screen. The cause is arithmetic: .pinh was 115vh against a .pin of min-height:100svh,
so the ENTIRE scrub range was 15vh - 135px at a 900px viewport - inside a 1035px section.
The sentence had finished morphing by 13% of the section, and a reader scrolling at any
normal speed could miss the first sentence completely. (r41 shortened this pin to kill dead
scroll. The right fix for dead scroll is content that answers the scroll, not less scroll.)

 1. THE PIN GETS DURATION: 115vh -> 175vh, so the scrub owns 675px instead of 135.
 2. THE FILAMENT NOW ARGUES THE SENTENCE. "One intelligence built the world. Two will build
    the next." The filament was a decorative network beside those words; it is now a single
    strand through the first line that SEPARATES INTO TWO as the words migrate, on the same
    scroll. Each node's parameter lerps from its place on one spine to its place on one of
    two half spines, the halves push apart in x, and the spine link across the halfway node
    is dropped once the split begins - without that the two strands stay tied by one long
    line. Two precomputed taper tables keep it table-driven rather than putting 176 sines
    back into the frame.
 3. THE DRIFT WAS WRITTEN AS A FRACTION OF THE SPAN in r43, which was right at 135px and
    would have dragged the scene 405px up the screen at 675. Absolute distance now, same
    eased profile.
 4. The filament had a frame nearly three times its own size and now has to hold two
    strands: 38% -> 45% of the row, and the drawing scale 0.56 -> 0.62.
MEASURED AFTER: 0 of 40 dead steps with the pin 4.6x longer.

--- THE RING ROOM -------------------------------------------------------------
FOUND: a very large dark room with a small cluster in the middle of it. The folders held
about a fifth of the frame's width at 1440, the armillary was a coin behind them, and
NOTHING IN THE SCENE WAS LIT BY ANYTHING - the floor grid simply existed. It read as a
diagram of a room rather than a room.
 1. SCALE: folders 268x186 -> 336x234, ring radius 330 -> 415, every breakpoint following.
 2. THE ARMILLARY becomes the size of the idea it carries: 96/77/58/39 -> 150/121/92/63.
 3. A LIGHT SOURCE: a pool on the floor where the ring stands, and a soft volume of air
    behind it, so the objects sit IN something instead of on top of a void.
 4. THE REVERSE OF A LIGHT FOLDER WAS GLARING. color-mix at 84% of the tint is right for
    emerald and wrong for Medcoin's paper, whose back came out near-white and read as
    cardboard. 52% now - the reverse of a folder is the same folder in shadow, whatever
    colour it is.
MEASURED AFTER: depth sort 0/30 worst 0px, 0 clipped folders at 620 and 860, 0 dead steps.

--- THE OPENING ---------------------------------------------------------------
FOUND: the hinge is right, but once the cover is open the reader looks at the INSIDE of it
for the rest of the scene - and the inside was an empty coloured wedge with a hairline box.
The inside cover is the one surface in a real file that is always pre-printed. It now
carries a routing form (identical on every file, because that is what a pre-printed form
is), and the fold has a contact shadow that never leaves.

ALL THREE: 0 JS errors at 390 and 1440, horizontal overflow unchanged at the pre-existing
42px, index.html untouched.

================================================================================
ROUND 48 - THE MOBILE ROUND, and the UV lamp on both platforms
================================================================================
Every section captured at 390x664 - an iPhone 14 with Safari's chrome taking the height,
which is the viewport the owner actually has, not the 390x844 the device reports.

--- THE RING FELL OFF THE RIGHT OF THE PHONE, and the cause was not the ring ------------
MEASURED: the room spanned x 32..422 on a 390px screen and the folders reached 441 - 51px
past the edge. Below 861 the horizontal track is not a track at all: it is a plain vertical
stack with 18px of padding, so #hpin is 362px wide inside a 390px screen. The room was still
declaring width:100vw, so it was 390 wide inside a 362 column and started at x=32 - and
EVERYTHING IN THE RING INHERITED THAT SHIFT, because the ring is centred on the room. The
room is a column item on the phone and is now sized like one.
Radius trimmed 190 -> 168 and the card 178 -> 166 for margin.
MEASURED AFTER, worst case across the whole pan: cards 2..382 inside 390. Zero overflow on
either side, at every point.

--- THE STATEMENT'S FILAMENT WAS A SCRIBBLE ---------------------------------------------
clamp(180px,26svh,240px) - about a quarter of the phone's screen for the one object the
section is built around, and it now has to hold TWO strands since r47. -> clamp(300px,44svh,
420px), with the sentence's own min-height reduced to pay for it.

--- THE UV LAMP, on BOTH platforms ------------------------------------------------------
* THE ARROW WAS A STRAY DASH: a 46px rule and a small triangle sitting between the lamp and
  the words, pointing at a glyph already in view. On desktop it read as a typo. On a 390px
  phone it ate ~35px of a 268px content box - WHICH IS WHY "SWITCH ON THE UV LAMP" BROKE
  WITH THE WORD LAMP ALONE ON THE SECOND LINE. Removed entirely, markup and rules.
* THE LAMP WAS A BLOB: 30px desktop, 26px phone. At that size the tube, the head and the
  cone are one smudge. 40px and 34px now, with a heavier stroke, using the room the arrow
  freed.
* NOTHING SAID IT WAS A SWITCH ON THE PHONE: .lampstate - the OFF/ON pill that makes the
  strip legible as a control - was display:none below 860. It is back, as a compact pill.
* THE WORDS: shortened so they cannot wrap at any width, and nowrap on both lines.
  "SWITCH ON THE UV LAMP" -> "TURN ON THE UV LAMP"
  "365nm - THIS FILE HOLDS MORE THAN THE PRINT" -> "365nm - MORE HERE THAN THE PRINT SHOWS"

--- FULL SWEEP, all eleven sections at 390x664 ------------------------------------------
0 JS errors and 0 horizontal document overflow on every one. The only elements crossing the
viewport edge are the four .bigmq marquee bands, which are 1525px wide by design and bleed
deliberately; body's overflow-x contains them and the page does not scroll sideways.
DESKTOP UNHARMED: every change above is either inside a max-width media query or is the
lamp, which was verified at 1440 after the change - band 988x52, title on one line, no arrow,
state pill present, 0 errors.

---

## ROUND 50 — the filament, the ring room, and a deep mobile pass

### The measurement that changed the round

I captured the ring, looked at a large slab of green, and was ready to desaturate it —
it read as neon plastic against the document's restrained palette. Sampled, the front
folder is **(48,178,128)**, which is `#2FB380`: the document's own emerald, exactly, and
the same value the document folder renders. Nothing was wrong with the colour.

What was wrong is that a large **unmodulated** plane against a near-black room has no
boundary of its own, so it reads as a swatch rather than an object. That is a *border*
problem, and the owner had struck volume out of these folders — so the answer is a
hairline, not a gradient. **A colour that looks wrong in situ is not necessarily a wrong
colour.** Sample before you reach for the palette.

### The filament (page 2)

Flat `rgba(242,241,237)` composited source-over, depth expressed only as alpha, structure
a chain of i→i+1..i+30. Legible, airless.

| change | why |
| --- | --- |
| `globalCompositeOperation='lighter'` | crossings ADD instead of covering. One line; the difference between a wireframe and something lit. Base alphas came down to compensate. |
| depth-graded whites | the bucket index is already a depth proxy (`a = 0.26·f²·kk²`, and kk *is* depth), so a ramp across the buckets is free at boot: cool blue-white far → neutral → warm bright near |
| bloom | each node drawn twice — wide+dim under small+sharp. 24 extra fills. |
| long-range chords | one per node, i→i+46..68, formed only where the strand has folded close in space. Connections that *could not be predicted from the ordering* are what make a network read as a network and not a rope. |
| hubs | every 13th node larger — hierarchy instead of 176 identical dots |
| travelling pulses | they used to blink between a fixed adjacent pair and reset to another. Now each walks a run of consecutive nodes with a comet trail: signal, not flicker. |
| radius cap | k reaches ~1.5 at the near edge, so `0.5+k²·2.1` grew a front node to a 5px disc |

Measured on the pinned statement, 259 frames: **mean 16.92→16.67ms, frames over 20ms 3→0,
max 50.1→16.8.** The added work is free.

### The split and the sentence disagreed on phones

Caught by capturing a phone rather than reasoning about it: at 390px the filament had
separated while the line still read *"One intelligence built the world."*

Below 861 the pin is frozen, so `__stSwap` never fires and the sentence runs on a
3-second interval — but the split was still being driven by scroll position, which keeps
advancing. **Two clocks.** `__stnfSplit` now refuses input below 861 and the phone's cycle
calls `__stnfSplitTo` in the same callback as `migrate`. Verified by wrapping the entry
point: four calls, alternating 1/0, each carrying the sentence of that moment.

### The room

* **The armillary was buried.** It is the centre of the composition and the front folder
  covered all but its top arc. It sat at `translateY(-27px)` with R=150 while the card's
  top edge with its tab is at −150. Raised to −88; every breakpoint follows.
* **The far card's reverse was a hard blue rectangle cutting the rings** — (28,40,48)
  against a room of (30,32,39). Two failed attempts before the right one:
  1. mixed the reverse harder toward the room **and** raised the fog. Measured: the side
     folders lost a third of their brightness (brass 88→61, paper 86→63). The mix is flat
     and hits everything; the fog is proportional to depth and hits only what is far. **I
     had changed two things at once and only one of them was aimed at the problem.** Mix
     reverted, fog kept.
  2. fogged toward `#0C0E13`, which is darker than the room — so the panel became a hard
     black hole instead of a bright one. **A thing that recedes must converge on the colour
     of the space it recedes into.** Fogging toward `#191A1F` at .94 gives **(29,32,40)
     against a room of (30,32,39)** — it dissolves.
* **A thread of background between the tab and the folder.** Scanned the join: nine clean
  rows of (48,178,128), then y=460 at (37,119,92). The two planes met exactly at 0 from
  different depths and the projection left a hairline. The tab now overlaps by 1.5px at
  the same depth. Also: my own new hairline had put a rim on the tab's *bottom*, which is
  not an edge — it is where the tab meets the folder. Three sides.
* **The horizon was a seam.** The floor's mask was `#000` at 0%, and 0% is the far edge, so
  the grid appeared out of nothing along a hard line at exactly `top:70%`.

### The document folder

Still carried r46's sheen at `.16` — which is the volume the owner struck out of the ring
folders, still sitting on the document ones, so the two did not read as the same object.
Cut to a third: a highlight still travels as the cover swings, a shut folder is one flat
colour. Same hairline edge as the ring.

### Deep mobile audit — 280/320/360/375/390/430/540

`mobaudit.js` walks every section reporting JS errors, document overflow, elements crossing
the viewport that nothing clips, self-overflow, ellipsis truncation, small tap targets and
contrast on solid backgrounds.

**Result at every width: 0 JS errors, 0 horizontal document overflow, 0 offscreen elements,
0 contrast failures.** Four defects found and closed:

1. `.es-k` at 4.22:1 — r49 darkened `.es-k` and the audit *still* reported 4.22. It was
   right and I was wrong about which element: there are **two** rules. `.mslip .es-k`
   overrides the colour to `#6E685C` *and* sits on different paper (`#E4E1D6`). `#625C50`
   on that paper is 5.07:1.
2. Ring folder names shaved — 108px of room for a name needing 112. Fixed below 400, and
   then **found still open between 401 and 620**, because I had fixed the band I measured
   rather than the rule. 120px of room, "Medcoin" at 28px needs 123.
3. `.hintro` carried `min-width:300px` into a 284px stacked column at 320.
4. The hero kicker's min-content was 269px in a 224px box — the string is *already*
   hand-spaced ("E X E C U T I V E") and then carried another `.3em` on top.

False positives worth recording so the next audit does not chase them: `.hcard.hroom`
"overflows" by ~950px at every width — that is `.rg-floor`, a 3484px ground plane which is
*supposed* to be larger than the room and is clipped by design. Same for the marquee tracks
and the horizontal scrollers.

Dead-zone sweep after all of it: **statement 0/45, files 0/45**, minimum change per step
380 and 327 pixels.

### And one bad instrument

To check the split/sentence coupling I first counted "lit runs" along horizontal scan lines
of the canvas — it reported 1, 2 and 3 strands in an order that tracked nothing. A
horizontal scan through a tangled 3D shape crosses it an arbitrary number of times. Same
family as the stopped clock and the bounding-box depth detector: **the instrument was
wrong, not the feature.** Wrapping the actual entry point answered it in one run.

---

## ROUND 51 — the statement, rebuilt around one number

### The diagnosis, which was structural and not a timing constant

The sentence and the filament were never going to be in step, because they were different
KINDS of thing. The split is a **continuous function of scroll**. The sentence was a
**discrete event**: cross p=0.5 and a 235ms hand-off fires; cross p=0.32 and it fires back.
A reader scrubbing slowly saw the strand pull apart smoothly while the words snapped. No
constant was going to fix that.

So: one number, `q` in [0,1], and everything is a function of it — every character's
position, blur, opacity and scale; the separation; the rotation of the whole sculpture. On
desktop `q` is the pin's own scroll. On a phone, where the pin is frozen, `q` gets its own
eased cycle with holds at both ends. **Same mechanism, two sources.** The sentence is now
scrubbable: scroll back and it re-assembles letter by letter.

The schedule is arranged so the two ripples overlap — A leaves on a stagger, B begins
arriving while A is still going — so the line reads as one sentence *turning into* the
other rather than two sentences swapping places.

### Two voices in one typeface

Fraunces is variable and its exotic axes were sitting at one fixed setting.

| | opsz | SOFT | WONK | wght |
| --- | --- | --- | --- | --- |
| *One intelligence built the world.* | 144 | 100 | 0 | 300 |
| **Two will build the next.** | 9 | 0 | 1 | 900 |

Wide, soft and light for what already happened; sharp, spiky and heavy for what comes
next. Same font file, nothing new downloaded.

And light travels through the words: one colour keyframe per character with a negative
`animation-delay` staggered by index, so a bright wave runs along the line for ever — cool
grey to cool white on the first sentence, emerald to pale mint on the second. Pure CSS.

### The helix — four passes, and only the last one was reasoning

The strands used to be pushed apart in a straight line. Separating in a line is a split;
winding around a shared axis is a dance, and it is the right image for the sentence.

1. **Radius quadratic in q** so it would "grow out of nothing" — which put the helix at a
   quarter of its radius when the sentence was already half morphed. *I reintroduced the
   exact desynchronisation the whole round exists to fix, inside that round.* Made linear
   and normalised so separation completes on the same number as the last character: q=0.86.
2. **Widened it** — still a tangle.
3. **The chords were gluing it shut.** Round 50 added one long-range link per node,
   i to i+46..68, and with HN=88 that offset crosses the halfway boundary for most of the
   strand. Every frame drew a mesh of arbitrary lines through the gap the helix had just
   opened. Chords crossing the boundary are now dropped the moment the strands part —
   crossings are the **rungs'** job, and they do it deliberately and sparsely.
4. **Then I stopped and did the arithmetic.** The strand is 1.06 tall. I had given the
   helix a radius of 0.46 — a *diameter of 0.92*. A coil 1.06 tall and 0.92 wide is not a
   strand, it is a squat spring seen end-on, and no amount of removing lines was going to
   make it read as two things winding around each other. Height must be a multiple of
   diameter. Stretch to 1.31, radius to 0.30, sheath tightened by a third → about 2.2:1.
   It read immediately.

Then measured the drawn extent against the canvas: top 0.043, bottom 0.965. Not clipped,
but 4% is not a margin when the scene also breathes 3% and tilts on its own clock. The
camera now steps back 11% as the strands part → 0.09 / 0.914.

### The regression I caused, and why desktop hid it

Both sentences are `position:absolute` now, so `.l1` has **no in-flow content**. On desktop
`.sttxt` is `flex:1 1 auto` in a row and `flex-grow` hands it the free space without ever
consulting content — full width, looked perfect. On a phone `.in` becomes a column with
`align-items:center`, where the cross size **is** the content size, and a box whose only
children are absolute measures zero. The line collapsed to a sliver and "Two will build the
next." wrapped onto five lines.

**Making children absolute removes them from their parent's intrinsic size**, and any
layout that sizes to content — a centred column, a fit-content box, an auto grid track —
loses its width silently. Fixed with an explicit `width:100%`.

### And one I caused in round 50 and only found by reading

Round 50 added `function ramp(tr)` to the filament. The morph **already had**
`function ramp(u)` in the same scope. Declarations hoist and the last one wins, so since
round 50 the morph's per-character emerald ramp had been calling the filament's, which
returns a bare `"214,216,214"` with no `rgb()` — invalid, silently ignored. The second
sentence lost its colour ramp and nothing reported it. Renamed to `tone()`.

### Verification

* Frame pacing, **three paired runs**, because the first single comparison looked like a
  regression: r53 gave 3, 0, **19** long frames; r61 gave 8, 0, 0. p50 is 16.7ms in every
  run and the previous build owned the worst run of the six. The spread is the host
  machine, not the build. *One measurement was not enough to tell a regression from noise.*
* Dead zone on the statement: **0/45**, minimum change per step 382px.
* Mobile audit at 280 / 320 / 390 / 430: **0 JS errors, 0 horizontal overflow, 0 offscreen,
  0 truncation, 0 contrast failures.**
* Helix fit on the phone, watched across a full cycle: worst extent 0.113–0.88 in a
  336x300 canvas.

---

## Round 52 — the PDF that had been wrong on the live site for three weeks

The task was "update the PDF with the site's numbers". **No number needed updating.** The
source file `dossier.html` already carried every current figure. What had happened is
simpler and worse: the corrections were made on 4 August, rendered to
`ORAN_CARMON_Portfolio_WIP_corrections.pdf`, and **never deployed**. The file at
`assets/ORAN_CARMON_Portfolio.pdf` was still EMERALD_v8 from 27 July, so every download
since then served `€3M+ ARR` where the truth is `$9M+ ARR` — wrong currency, and a third
of the magnitude, on the single most important figure in the portfolio. Three of the four
case files also carried the wrong sector.

### Two instrument failures, both caught before they became claims

**The PDF's letter-spacing turns every letter into a word.** Extracted text arrives as
`X T I X  ·  B 2 B  S A A S` — letters separated by one space, words by two. A raw word
count gave the PDF 3,766 words against the site's 2,137, and I was one step from reporting
that the PDF held nearly twice the content. Normalising — split on the double space, then
join any group whose tokens are all single characters — gives 1,694. The comparison had to
be built before it could be trusted:

```python
def unspace(line):
    groups = re.split(r'\s{2,}', line.strip())
    out = []
    for g in groups:
        toks = g.split(' ')
        out.append(''.join(toks) if (len(toks) > 1 and all(len(t) <= 1 for t in toks)) else g)
    return ' '.join(x for x in out if x)
```

**`inventory.py` skips `<svg>`, and the site has seventeen.** The figure sweep reported the
entire thirteen-tool technology stack as missing from the site. All of it is present, drawn
as SVG. A parser's blind spot reads exactly like an absence in the document.

A third, smaller: nine figures appeared on one side only. Every one was an artifact —
site-only furniture (the `26-010x` control numbers, the ring's file count) or a regex that
cannot see split markup, since on the site `$9M+` is a currency span plus a counter span
whose literal text is `0M+`. **Zero real disagreements.**

### The pipeline was proven before anything was overwritten

Rather than trust that `dossier.html` was the source, it was rendered and compared to the
known-good output:

```
chrome --headless=new --disable-gpu --user-data-dir="$UDD" --no-pdf-header-footer
  --virtual-time-budget=20000 --print-to-pdf="$OUT/_roundtrip.pdf" "file:///…/dossier.html"
```

13 pages, text identical on 13/13, 1,186,098 bytes — matching the WIP exactly. Only then
did the output replace the served file. `--virtual-time-budget` is legitimate here: it
freezes the clock, which is wrong for timing measurement and right for print.

### One near-miss on a blind replace

`>OPERATIONS<` occurs twice in `dossier.html`. The first is XTIX's zone B, which the copy
cleanup removed. **The second is a label inside Oasis's cross-functional SVG diagram.** A
global replace would have corrupted a diagram in a different case file. The cleanup was not
applied to the PDF in this round for a separate reason — print pages are fixed-height and
removing a zone reflows thirteen of them — but the trap was there either way.

### Verification

* Live URL polled until it served the new bytes: `9b0b33d4…`, 1,186,098 bytes, 13 pages.
* All six corrections confirmed **in the bytes downloaded from the live URL**, not in the
  local file: `$9M+ ARR` present, `€3M` absent, three sectors corrected, `2026-Present`,
  `NINE PRINCIPLES`.
* One residual `FINTECH` investigated rather than assumed stale — it is Medcoin's own
  `CRYPTO FINTECH · FOUNDER`, identical on both sides. Correct.
* `index.html` md5 `13b3a8c3197ed6ec948f83c820e4588b` asserted before the commit.

---

## Round 53 — the cleanup, carried into print

Same four items as the site. What makes the print file a different problem: `.page` is a
fixed 1280x720 box with `overflow:hidden`, so **nothing reflows between pages, and anything
that outgrows its box is silently clipped and never reported.** A removal cannot cascade; an
addition can vanish.

### Three traps, each found by checking instead of assuming

**`OPERATIONS` occurs three times.** Only the first is XTIX's zone B. The second is a
`<text>` label inside Oasis's cross-functional org-chart SVG. The third is page 12's
`AI BUILT FOR INTERNAL COMMERCIAL OPERATIONS — NOT A SELLABLE PRODUCT`. A global replace
corrupts two pages in two other case files. Every edit is anchored to one verified offset
inside one page's byte range, and the script asserts both bystanders survive.

**`Led a team of 5–6 sales professionals` appears exactly once in the document** — inside the
zone being deleted, and it is the only statement of the team's size anywhere in the PDF.
Delete first, carry second, and the fact is gone. The script refuses to run if that row is
not present in the block it is about to cut.

**Oasis zone B was a grid child, not a block in a column.** `.p08 .inner` is
`grid-template-columns:1fr 1fr 1fr` with children A / B / C(`.ringwrap`). Removing the child
without narrowing the template leaves an empty third track — a hole, not a two-column page.
Narrowed in the same commit. The org-chart SVG carries `max-width:228px`, so the wider track
*cannot* make it taller: the "widening made it taller" failure from the site work does not
reach here. That was worth checking rather than fearing.

### The instrument lied first, again

The first fit probe measured the lowest descendant bottom per page and reported **26px of
slack on all thirteen pages**. That number is `span.brk`, the decorative corner bracket
pinned 26px off every page foot by design. It would have read *identically on a page whose
text was cut in half.* The replacement measures the two ways content actually disappears
here: `scrollHeight > clientHeight` on every element whose computed overflow clips
(internal), and any box crossing the 720px fold (page).

`.zr` chip enumeration also under-reported: XTIX looked like `A → B → D` with no C, because
the C chip carries `style="margin-bottom:7px"` and my regex demanded `class="zr">`. **A page
does not skip a letter; a regex skips an attribute.** Live DOM read settled it.

### Verification

* Fit, all 13 pages, before and after: **0 clipped, 0 crossing the fold.** Oasis zone 03
  absorbed its 9th row, 447 → 459px. p08 now two 508px tracks, no empty column.
* Text diff page by page: **41 changed lines, every one an approved item.** 13 pages both
  sides.
* **Then I looked** — pages 6, 7, 8, 10 rasterised from the render and read as a reader meets
  them. My first reaction to p08 was "40% empty"; the before render has the identical blank
  lower band and ink coverage went *up*, 10.4% → 11.1%, because the stat card widened. The
  real change is that losing the middle column leaves the `$2M` card and the org chart as two
  islands with a gap. Design round, not patched here.
* Live URL polled to the new bytes; ten content probes read from the downloaded file.
* One probe expectation was wrong, not the file: `WHAT I BUILT` counts 2, because XTIX p05
  has `04 WHAT I BUILT · (AFTER)`. Both correct.

---

## Round 54 — the cover says who this is

A reader's note: from the start it is not clear what the document is or who wrote it. Read
the live `/m/` as a new reader on a phone before accepting or rejecting the note. It is
correct, and the reason is specific: the gate says `100% GROWING... OPEN CASE FILE`, the
cover offers a coined identity (`THE COMMERCIAL SYSTEMS BUILDER`) and a promise (`From
Vision to Measurable Growth`), and the next two screens are the filament and a couplet.
**No recognisable role, no scope, no company and no number for roughly 2,400px.** Research
already in this project says 6–8 seconds and layer-cake scanning. So one line of hard fact
went on the cover, and three pieces of furniture came off it.

### `.mflip` is not a label, it is the folder's tab

It reads like a name plate. The CSS is
`background:var(--emb);border-radius:11px 24px 0 0;height:44px;width:max-content` — **it is
the tab head**, the thing that makes the cover read as a folder instead of a card. The
instruction was to delete the text on the tab, so the text went and the element stayed.
Emptied, `width:max-content` collapsed it to its own 44px of padding, so it needed an
explicit width to keep reading as a tab and not a stub.

The bottom-right status row is desktop-only: `#loglin` is built inside `if(!frozen)` and
`frozen` is true below 861px, so that line never existed on a phone.

### Three typography defects no measurement reported

Found by looking at the render, not by any probe:

1. `CROSS-FUNCTIONAL EXECUTION` split mid-word at the hyphen → `CROSS-` / `FUNCTIONAL`.
2. Desktop wrapped when it had no reason to — **my own `max-width:37em` is 351px at 9.5px
   type inside a 1100px card.** I briefly blamed the string for a break my cap had caused.
3. The wrap could put the separator at the start of a line → `· CEO · FOUNDER`.

Each role is now its own `white-space:nowrap` unit carrying its trailing separator, so the
only break opportunities are between roles and a separator can never lead a line. Mobile
tracking .14em → .12em (the file already uses .12em for `#hero .crumb`) because the first
two roles measured 331px against ~330px of card and fell to three lines *by one pixel*.

The block deliberately carries no `rv` class. Its siblings `.sub` and `.by` have none either.
A line whose whole job is to orient a reader in six seconds must not be able to fail to
appear, so it survives `body.static`, `body.failsafe` and a scene that never fires.

### "Pushed" is not "deployed"

The commit went up and the site kept serving the old build. I polled the CDN for about
fifteen minutes assuming propagation lag, and even reported it as "Pages build is lagging".
It was not lagging — **the `pages-build-deployment` run for `a652e7a` had FAILED.** One call
to `/deployments?environment=github-pages` answered in seconds what fifteen minutes of
polling could not.

The tell was there and I read it wrong at first: `Age: 0` on a fresh request means the CDN
*did* go back to origin and origin handed back the old file. That is the opposite of a cache
problem. Cache-busting query strings are useless here — Pages ignores them for cache keys,
and the age kept climbing across `?cb=` values.

The job breakdown matters: `build` **succeeded** (Jekyll was fine — there is no `{{` or `{%`
in the file and no `.nojekyll` is needed), and `deploy` failed with an empty description.
Nothing was wrong with the content; `raw.githubusercontent` served the correct 672KB build
the whole time. The deploy step is not independently re-runnable without auth, but any push
to main starts a fresh run, so an empty commit recovered it.

**Check the deployment state, not the served bytes, when a push does not appear.**

### Verification

* Live, 1440×900 and 390×844: roles on 1 and 2 lines, 9.5px (above the file's 8.5px phone
  floor), ident inside the card, card 223/243px clear of the fold, **0 JS errors**, 0
  horizontal overflow on the phone. The 42px desktop overflow is the known `.bigmq` item.
* Breadcrumb absent, tab name absent, tab still 128px/92px wide.
* Served markup uses `&middot;`/`&mdash;`/`&ndash;` under `charset=utf-8`, no mojibake — the
  `Â·` I saw first was my own console decoding the pipe, not the page.

---

## Round 55 — wave 1 of the five folder changes

### A removal that owned something three sections away

`.ritual` looked like decoration at the foot of each folder. Its press-and-hold stamp was the
**only** caller of `window.__markReviewed`, and that drives `#casemeter` on the desktop and
`#ccstamp` **inside the vault**, which turns `IN REVIEW · 0/4` into `CASE CLOSED` directly
beneath the line *"FOUR FILES REVIEWED — THE RECORD CLOSES"*. Deleting the block silently
would have left the document's ending making a promise nothing could keep — and the vault is
under a standing do-not-touch rule, so the ending was not available as a place to fix it.

The furniture went; the ceremony stayed. A file reports itself read when the reader reaches
its foot — a 1px sentinel where the ritual used to sit, observed with a −12% bottom
rootMargin so it only fires at the genuine end of the file.

**It is strictly better on a phone.** The whole reviewed system was desktop-only: below 861px
the four stamps called nothing, so the vault could never close and the last thing a phone
reader met was a counter frozen at 0/4. Now verified at 390×844: `CASE CLOSED`. The open
phone-stamp defect is closed by deleting the thing that was broken.

### The selector filter was the wrong instrument

First attempt removed the ritual's CSS by testing each rule's selector. Half those rules live
inside `@media` blocks, where a flat rule-by-rule regex both misses them and **cannot separate
`.redx` rules that must stay from `.sb-imp` rules that must go when they share a block.** The
run finished with the stamp CSS still in place; the guard `assert 'stampbox' not in s` caught
it before anything was written.

The CSS is one contiguous 3,607-char run. Cut it by its real boundaries, verify first that it
contains nothing foreign — the only non-ritual selectors inside were `0%,100%` and `50%`,
which are its own keyframe steps — and remove the three stragglers by exact text.

### Where change 2 was stopped on purpose

The covering layers are two devices, not one. `.rxs::after` and `.redx::after` are **stickers**
and became `#D8C24A`. `.redct` is a black **redaction** bar; redaction is its own language in
this file and a censored line is not a sticky note, so it was left and raised with the owner
rather than swept in. `#medcoin .rxs::after` existed only because cream vanished on Medcoin's
paper folder — yellow does not, so the override went.

### Verification

* `.ritual` / `.stampbox` / `.rt-sig` / `.rt-end` → **0 of each**; 4 sentinels present.
* Counters after a full read: `0/4 → 4/4` desktop; `IN REVIEW → CASE CLOSED` on **both**.
* Sticker fill `rgb(216,194,74)` in all four folders.
* `SEALED · TAP TO REVEAL` contrast on the new yellow: **5.18:1**, still AA (was ~7:1 on
  cream). Checked rather than assumed — a legible swatch says nothing about text printed on it.
* Folder foot trailing gap **−1px**: no orphaned space where the block used to be.
* 0 JS errors, no new horizontal overflow. Document 5,087 chars lighter.

---

## Round 56 — wave 2, the evidence rail (desktop)

### The grid that would have looked right and stuck 29px

The obvious shape for a sticky sidebar is a two-column grid on `.wrap` with the rail spanning
every row: `grid-column:1; grid-row:1 / -1`. **It silently does not work here.** With only
`grid-template-columns` declared, every row is implicit, and `-1` resolves against the
*explicit* grid — which has no rows — so the rail spans exactly one row. Its containing block
becomes the 29px-tall `.shead` row, and it sticks inside that.

A flex row instead: the rail's containing block is the row, whose height is the folder's
height, which is exactly the distance the rail should travel.

### The folder barely paid for it

`.wrap` was `max-width:1120px` with **160px of unused margin either side at 1440**. Taking the
rail out of the folder's own width would have cost the folder 27%. Widening `.wrap` into
margin it was already wasting costs the folder 1165 → 994 at 1440, and nothing at 1600+.

### Gate the move, not the styling

The move only happens above 1180px. If the panels were relocated and the rail then merely
hidden below that, the panels would **vanish from every narrow layout** — present in the DOM,
invisible to the reader, silent in every test that only counts elements. Verified at 1100px:
no rail, panels still inside the folder, document unchanged.

### The reveal trap

`.slipflip` lived inside a `.rv.u` container whose classes drive the scroll reveal. Lifted out
of it, the panels can sit permanently at `opacity:0` — invisible in every screenshot and
reported by no error, because nothing is broken, they simply never get told to appear. The
rail states their rest state explicitly. Specificity alone was enough; no `!important`.

### Moved, and proven moved

`appendChild` relocates a node with its listeners intact — but "should still work" is not
evidence, since a rebuilt panel looks identical and does nothing. Clicking `.sf-tab` after the
move takes `.slipflip` → `slipflip turned` and its height 154 → 388, at 1440 and 1280.

### The measurement that nearly passed as a failure

The first stick test sampled five points across the whole **section** and reported `0/5` held.
The rail can only stick across its containing block — the `.caserow`, which is the folder's
height, not the section's — and two of five samples landing on the same number proves nothing
either way. A dense walk across the row's actual span: **13 of 17 samples at a constant
position**, then release at the folder's end. The rail was working the whole time; the
instrument was pointed at the wrong span.

### Open

Rail pins 75px from the top while its computed `top` is 92px. It sticks reliably and
consistently at that offset. The 17px difference is unexplained — recorded rather than guessed
at, since a plausible-sounding cause I have not tested is worth nothing.

---

## Round 57 — wave 3, the phone drawer

### The bug the move exposed was not the move's bug

The turn control disappeared from the phone drawer. It had not disappeared: `.sf-stage`
measured **0** while the `.evslip` inside it measured **113**.

The stage owns the height because both faces are `position:absolute`, and it is measured by a
closure-local `fit()` that runs **once at build time** and thereafter only on a flip.
Relocating the panel changed its width, so the stored height went stale. And because the faces
are out of flow, **a wrong stage height does not clip them — it lets them draw straight over
the ANALYST NOTE below.** The design comment in that very block promises the control "can
never overlap the ANALYST NOTE". It could, and it did.

This was never specific to the drawer. A phone rotation or a late-loading font leaves exactly
the same stale height. So the fix is not to re-measure after my move — it is to make the
component re-measure whenever a face changes size:

```js
if('ResizeObserver' in window){
  var __sfro=new ResizeObserver(function(){fit()});
  __sfro.observe(slip); __sfro.observe(back);
}
```

Observing the **faces**, not the stage, is what keeps it from looping: a face's height is
content-driven, so writing the stage height cannot feed back into it.

    before   .sf-stage 0     .slipflip 57    strip drawn over the note
    after    .sf-stage 113   .slipflip 170   strip in flow beneath it

### The gesture cannot take the page, by construction

Both touch listeners are `{passive:true}`, so `preventDefault` is not available to them at all
— they read the gesture and can never cancel a scroll. That is a property of registration, not
a threshold that might be tuned wrong. Verified rather than argued: a touch dispatched on the
closed tab, then a scroll — the page still moved.

### Fixed, not sticky

The drawer hangs off `<body>`. Sticky depends on every ancestor's overflow and on transforms
this file applies to sections, several of which the phone build freezes. A body-level fixed
element depends on nothing above it. One drawer per file rather than one shared drawer whose
contents move in and out — repeatedly moving the same nodes is how listeners get lost.

### Two guards of mine that were wrong, and what they teach

`assert s.count("className='evdrawer'") == 0 and s.count("d.className='evdrawer'") == 1` — the
second string contains the first, so the assertion could never pass. And
`assert 'preventDefault' not in JS` tripped on the word inside my own comment explaining why
there is no `preventDefault`. **A guard that matches prose instead of code is a guard against
writing documentation.** Both now test for a call site, not a word.

### Verification

* Phone 390×844: 4 drawers, one per file; both panels in each, none left in a folder; live
  only inside its own file; closed tab at x=0..27, 132px tall; open body at x=0, 328 wide,
  fully inside the viewport; opens and closes; 0 overflow, 0 JS errors.
* Desktop 1440×900: rail unaffected; turn tab y=209 above the note y=281.

---

## Round 58 — the switch, the rail off the folder's width, matte violet

### A negative margin on a flex item is a gift to its siblings

To stop the rail costing the folder any width, the rail became `flex:0 0 0` and was pulled
into the page margin with `margin-left: calc(-1 * (railw + gap))`. That made things **worse**:
a negative margin on a flex **item** hands the recovered space back to the line, so the folder
absorbed all 284px, grew to **1442px** and started at **x=−13** — further from its original
geometry than the wave-2 version it was meant to fix.

The offset belongs to the rail's **children**. They are not flex items of `.caserow`, so
shifting them leaves the rail's own box at zero width and the flex line never learns about it.

    before fix   folder x=-13  w=1442
    after  fix   folder x=271  w=1158   (identical to no-rail geometry)

### The rail can only exist where the margin can hold it

Margin is `(100vw − 1120)/2`. The panels stop being readable under about 196px, so the rail
needs **1580px** of viewport. Below that the drawer takes over — its gate moved 1180 → 1580 so
every width still gets exactly one of the two, and none gets both.

1440 now gets the drawer. That is the honest answer rather than a compromise: at 1440 there is
no room for a rail that does not squeeze the folder, and squeezing the folder is precisely
what was rejected.

### The switch stayed in flow on purpose

An absolutely positioned plate in the folder's top-right corner would land on the
`CTRL № / CASE FILE / COPY 3 OF 12` row already there, and `.folder` clips on X so any overhang
would be cut. `margin-left:auto` puts it top-right with neither risk, at the cost of the
vertical space it occupies — which is the right trade for a control nobody was pressing.

The toggle wiring queries `.lampcall`, `.lampsub`, `.lampstate` by class. Keeping all three
names meant the glyph, copy and styling could all change without touching one line of logic.

### Colour

`#D8C24A` → `#9483C6`. The seal ink moved with it, `#4A473F` → `#211C2F`: the old ink was a
warm grey chosen for a cream sticker and would have read as dirt on violet. **Measured, not
eyeballed: 4.97:1, AA.**

### Verification

* 1700 / 1920: folder geometry identical to no-rail; rail content 256px / 320px in the margin,
  28px clear of the folder.
* 1440: no rail, 4 drawers, folder x=141 w=1158.
* 390 / 360: switch 119×89 inside the folder, tap target over 44px, arms and disarms,
  0 horizontal overflow, 0 JS errors.
