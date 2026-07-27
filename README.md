# Oran Carmon — Executive Portfolio

**Live site:** https://oran-ops.github.io/portfolio/

The commercial dossier of Oran Carmon — Commercial Growth Leader. Four case files
(XTIX, Oasis, Eventer, Medcoin), built as a single design system: flat matte
charcoal, emerald folders, no gradients or glows.

## Contents

| Path | What it is |
|---|---|
| `index.html` | **The living site** — animated dossier: desk reveal, folder opening, investigator arc. Self-contained (fonts inlined) |
| `src_site.html` | The same site without the html/head wrapper — the file to edit, then re-wrap into `index.html` |
| `cover.html` | Static cover page — fallback for anywhere motion isn't wanted |
| `dossier.html` | The full 13-section portfolio, readable in the browser |
| `assets/ORAN_CARMON_Portfolio.pdf` | Print edition of the same dossier |
| `assets/linkedin_cover.png` | LinkedIn cover, 3168×792 |
| `assets/linkedin_profile.png` | LinkedIn profile picture with the emerald ring |
| `fonts/fonts_dossier.css` | Self-contained webfonts (Inter, Fraunces, JetBrains Mono) |

## Design tokens

```
bg #191A1F   card #202127   card2 #25262D   grid #33353C   grid2 #4B4E55
ink #F2F1ED  label #A6A7AC  muted #8E8E93
emerald #2FB380 (XTIX)   brass #E0A458 (Oasis)   steel #5E8FBF (Eventer)   ink (Medcoin)
```

Flat matte only. Text on colour is always `#191A1F`.

## Local preview

```bash
python -m http.server 8080
```

Then open http://localhost:8080/

## Contact

oran@xtix.ai

## Build history

`build/` holds every generator and patch script that produced these files, in the
order they ran (`_replay_ops.json` is the recorded sequence). The site was rebuilt
from exactly this chain after its working copy was lost; the casebook rebuilt in the
same run came out byte-identical to the delivered file, which is how the recovery
was verified.
