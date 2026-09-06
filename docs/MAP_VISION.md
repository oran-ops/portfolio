# THE MAP — the vision

Oran's brief, written back in full so we can both check I have it right before anything is
designed. This supersedes `MAP_BRIEF.md` as the statement of intent; that file stays as the
record of what was rejected and why.

**Process rule, stated by him and binding on everything below:** plan together, specify
together, approve each mini-world visually one at a time, then build. No designing ahead of
agreement. This is a work plan for THE MAP only — separate from the plan for the whole
portfolio document.

---

## 1. The idea in one paragraph

A green country — vegetation, trees, small hills, flowers, cabins in the forest, off-road
vehicles in the remote parts. **British Columbia.** One road runs through it, and that road
carries the reader to four workplaces. Wherever the road arrives somewhere, the forest suddenly
becomes a **small metropolis**. Manhattan and Central Park in one frame: Central Park is
everything around the road, Manhattan is the four places themselves.

## 2. The look

**Reference images A–F, and F above all — for its sharpness and its modernity.** These
establish *spirit and thinking*, not colours and not a design to copy. That mistake has been
made once already: the earlier links only established "isometric map", nothing more.

- True isometric, sharp, modern, crisp. Award-standard.
- Dense with readable detail: icons, components, small things.
- A thin base plate under the map, as in F.

## 3. Colour

- **Bright, alive, vivid** — colours that make the place feel alive, like the references.
- **But matte in tone.** Vivid and matte together, not glossy.
- **Each workplace is dominated by its own colour.**
- **DECIDED — the palette is free.** No tie to the folder colours at all: *"אני חוזר בי, נבנה
  את הכל עם הצבעים שנבחר ביחד בלי קשר לצבעים של התיקיות — הכל על פי מה שמתאים."* This removes
  the contradiction that the earlier brief carried, where the four document accents were
  simultaneously required and forbidden.
- Realism is explicitly not the goal here: *"אני יודע שזה לא מציאותי, כן, אבל זה מה שאני רוצה."*

**→ Open decision 1: choose four area colours plus the country green, by eye, from options.**

## 4. Topography

- The map is **roughly square** — not exact, but not a rectangle.
- **Mostly flat.** Small hills, small rises, small falls. No cuts, no steps — as agreed.
- One road, carrying cars, joining the four workplaces.
- **START sits immediately before XTIX; the road runs on to END, immediately after MEDCOIN.**

## 5. The four mini-worlds

Each has its own theme, is packed with elements, and is a small world inside the whole map.
Clicking a workplace zooms the map in and reveals it.

### XTIX — built everything from zero
Not Dubai, not New York, not Tokyo. **30 % under construction, 70 % already standing.**
Skyscrapers, luxury restaurants, new cars, people in suits, ordered roads, large private houses
or tall apartment blocks, density, a great deal happening at once. Modern, fast, a moving pace,
building going on all the time. In the construction zones: **tall cranes, contractors at work,
excavations with tools, building skeletons mid-rise**, the plan of a future metropolis.
*The message: raised from nothing, fast — and still it came up tall, luxurious and very
strong.*

### OASIS — a residential neighbourhood with a focused business centre
Existing, but still new. Private houses with yards and fences; low residential blocks with
parking and cars; the private houses are genuinely luxurious, with new cars. Many people in the
street, **children playing, public playgrounds**. A **significant, strong commercial centre —
not tall — taking at least 15 % of the mini city**: clothing, restaurants, services, shopping,
fashion, combined with company offices. Two floors of retail, then two floors of offices.
*The message: something stable, existing, alive and breathing. Construction is finished, and
what it finished as was an outstanding neighbourhood living its quality routine in community.*

### EVENTER — the interchange
Like the famous Los Angeles interchange — **as a reference, not a copy.** A busy junction,
packed with cars, roads, ramps, signs, traffic standing in a jam. **Every customer he had at
Eventer is one of those cars** — there were that many. Old and established, so it reads as a
city already full. The point of the junction is to get through it: ALIGNMENT.
**But not only an interchange.** Buildings, people and businesses around it, so it is the
centre of a city rather than a slip road dropped into the middle of the map.

### MEDCOIN — the business district
Like the Ramat Gan exchange, like the Twin Towers district. Work, industry, companies — little
residential. Office buildings, real skyscrapers if they serve.
- **At the edges:** low industry — factories, tractors, forklifts, material yards, smoke,
  concrete, coal, stone, marble, timber, metal, **people working with their hands**.
- **At the centre:** skyscrapers, offices, **people in suits** — law firms, finance — and the
  restaurants that go with that world.

## 6. Interaction

- Mouse-controlled on every axis, as now.
- **Nowhere to travel beyond the map.** The map is for looking at.
- **Not clickable, except to zoom into a workplace.**
- To go further the reader scrolls, and begins moving inside the document. Guidance of the
  reader comes later — the map first.

## 7. Decisions taken

1. **Palette — free.** Chosen together, by eye, with no tie to the folder colours. *Open: the
   choice itself.*
2. **Build order — OASIS first**, then EVENTER, then MEDCOIN, then XTIX. OASIS is the most
   ordinary, so it sets the vocabulary of houses, streets, people and shops that the other
   three reuse; XTIX is the most demanding and gains from everything learned before it.
3. **Proportion — the whole map is 100.** The four mini cities together are **60 %**, so each
   is **15 %**. The green country is the remaining **40 %**.

### What the proportion means in numbers

Taking the map as a square of side `S`:

| | share | area | side, if square |
|---|---|---|---|
| one mini city | 15 % | 0.15 S² | **0.387 S** |
| four together | 60 % | 0.60 S² | — |
| green country | 40 % | 0.40 S² | — |

Each city is therefore **about two fifths of the map's width** — very large, and a deliberate
choice: these are dense small cities, not villages, and four of them nearly fill the frame. The
green is what runs between and around them, and it has to do its work in the gaps rather than
in open expanse. That is a real constraint on the layout and it is worth seeing early.

## 8. What carries over, and what does not

**Carries over:** the 43-kit / 4,236-model library; the measured per-kit scale table; the
placement rules and the checker that proves them; the headless render pipeline; the four
authored layouts as *content* to be rebuilt against this vision.

**Does not:** the naturalistic colour grade; the fractal terrain; the perspective camera; fog
and aerial perspective; anything that made the map read as a landscape rather than as a
designed object.
