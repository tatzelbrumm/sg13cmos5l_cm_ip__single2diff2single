# ART_NOTES: tughra calligraphy as metal art in slot_7

> **Second location not done.** `git worktree list` in the work repo shows one worktree only (the main checkout). There
> is no worktree called "sudelbuecher". The repo has a tracked *directory* `sudelbuecher/` (logs) and an orphan *branch*
> `sudel_buecher`, which the repo's CLAUDE.md forbids switching to in the main checkout. As instructed for this case, **only the
> first branch, `art/tughra-metal`, was made.** The branch `art/tughra-metal-sudelbuecher` does not exist.

## Result in one paragraph

The calligraphy (legend row excluded) is drawn in floating metal in the empty band of `slot_7` between its two
TopMetal1 supply straps, at **scale 0.102 um per source pixel: 152.05 x 89.4 um, lower-left corner at (88.5, 141.3) um**
in slot coordinates. **TopMetal1 is not used** (too coarse, 1.64 um). Four metal layers carry six colours:
**red + orange + gold on Metal1**, purple Metal2, blue Metal3, green Metal4. The merged GDS adds
**no DRC violation** (all tables, density, antenna), the XOR against the untouched slot7 is **empty**, and LVS
still matches with an **identical extracted netlist**.

This is revision 3. Rev 1 and rev 2 (with TopMetal1) are in the git history and in `ART_LAYERS.md`.

| file | what |
|---|---|
| `art/tughra_art.gds` | art only, cell `tughra_art`, 4 metal layers, dbu 1 nm |
| `art/slot7_with_art.gds` | copy of slot7 `final/gds/slot_7.gds` plus `tughra_art` placed at (88.5, 141.3) |
| `art/build_art.py` | image -> polygons -> both GDS files (deterministic; `python3 art/build_art.py`) |
| `art/segment.py`, `art/pdk_layers.py`, `art/find_free_space.py` | colour segmentation; layer numbers and rules from the PDK; free-space analysis |
| `art/verify_art.py`, `art/verify_report.md/.json`, `art/verify/*.log` | XOR, clearance, DRC, LVS before / after (logs trimmed to the last 120 lines) |
| `art/preview_side_by_side.png`, `preview_art.png`, `preview_layers.png`, `preview_slot_context.png`, `art/layer_colour_map.npz` | previews (the npz tells the preview which colour to draw each Metal1 cell in) |
| `art/free_space.md/.json`, `art/build_stats.json` | analysis numbers |
| `ART_LAYERS.md` | layer proposal (own commit, then revised twice) |

Re-run: `export PDK_ROOT=/foss/pdks; python3 art/find_free_space.py; python3 art/build_art.py; python3 art/preview.py; python3 art/verify_art.py`
(the slot7 GDS and CDL are read from `/home/user/sg13cmos5l_cm_slot7`, override with `SLOT7_GDS` / `SLOT7_CDL`;
`verify_art.py` takes about 3 minutes). Python modules needed: `klayout`, `numpy`, `opencv-python-headless`,
`scikit-image`, `shapely`, `Pillow` (installed with pip in this session). Run `verify_art.py` after the last `build_art.py`; it reads the GDS files on disk.

## Repos and branches

- Reference `tatzelbrumm/claude-cloud-config`: read only (README for the environment: tools under `/foss/tools`, KLayout 0.30.12). Nothing pushed.
- Slot7 repo `tatzelbrumm/sg13cmos5l_cm_slot7`, commit `454da6a`: **read only.** No branch, commit, file edit, push, PR or issue. `git status` there is clean.
  Input file `final/gds/slot_7.gds`, sha256 `5f8fd14a...bd` (the same as its README lists as the source file).
- Work repo: branch `art/tughra-metal` made from `origin/main`, the remote's default branch (`git remote show origin`: HEAD branch main, commit `60f270a`).
  The session's checkout was on `claude/gifted-cray-wapti0` (a copy of `toplevel`), which was left untouched.
  No merge, no PR, default branch untouched.
- The default branch's CLAUDE.md says "no git commands without asking first" (written for a local connected-folder sandbox). This task explicitly
  asks for commits and pushes and git works in this cloud container, so the task's instruction was followed.

## Free space and placement

Free region per layer = slot boundary (prBoundary 189/4, 0..537.15 x 0..273 um) shrunk by 5 um, minus every shape on that layer
(drawing, pin, no-fill, boundary datatypes) grown by a margin. **Margins:** Metal1-Metal4 **1.0 um**; TopMetal1 **3.0 um** (reported, not used by the art); slot edge **5 um**.

- 1.0 um is about 5x the minimum spacing (0.18 / 0.21 um), larger than the widest wide-metal spacing in the deck (0.6 um, rules M1.f / Mn.f)
  and than the harness filler distance (0.42 um, M?Fil.c), so a floating art stroke is never closer to a signal than a rule or the filler would put it.
- 5 um from the slot edge: the neighbouring slot's shapes and the slot's own pins reach to the edge.
- No exclusion or keep-out rule is written in the slot7 documents (README, FOR_TIM.md, PROGRESS.md, slot_7.md); they say only that fill is not done.
  The slot's own markers were still honoured: the no-fill marker (datatype 23) on Metal1/Metal2 at x 535.15-537.15 um and the TopMetal1 straps.

Largest free rectangles (um; full list in `art/free_space.md`):

| layer | free of slot | largest rectangle |
|---|---|---|
| Metal1 | 93.8 % | (39, 5) - (324, 268), 285 x 263 |
| Metal2 | 95.7 % | (39, 5) - (324, 268), 285 x 263 |
| Metal3 | 92.0 % | (5, 114.5) - (324, 268), 319 x 153.5 |
| Metal4 | 98.0 % | (39, 5) - (324, 268), 285 x 263 |
| TopMetal1 | 88.6 % | (10, 5) - (532, 127), 522 x 122; next (5, 143) - (532, 229), 527 x 86 |
| free on Metal1-4 and clear of the TopMetal1 shapes by 1 um | | (39, 5) - (451.75, 77.25), 412.8 x 72.2; **(5, 141) - (324, 231), 319 x 90** |

**Choice: (5, 141) - (324, 231), 319 x 90 um**, art centred in x. Reasons: (1) it is free on all four art layers, so the art sits over
empty silicon and couples to nothing; (2) the larger single-layer rectangles (up to 263 um tall) are crossed by the TopMetal1 supply straps at
y 130-140 and 232-242 um, which would hide lower-metal art when seen from above; (3) the other candidate (412.8 x 72.2) is shorter, and the art's height sets the scale.
The art is height limited (875 source rows, 1488 x 875 source pixels, aspect 1.70, kept).

**Scale 0.102 um/px.** Final art box (88.5, 141.3) - (240.55, 230.7) um; 0.3 um spare at the top. Closest approach to existing shapes (bisection, `verify_report.json`):
same-layer Metal1 and Metal2 more than 60 um, Metal3 36.6 um, Metal4 more than 60 um; the nearest existing metal of any layer is the TopMetal1 strap, 1.3 um from the art
(no overlap: 0.000 um2 with existing metal on every layer); at least 42 um from the slot edge.

## Layers

| colour | layer | GDS | polygons | area (um2) | shape fidelity (IoU with the source mask at this scale) |
|---|---|---|---|---|---|
| red, orange, gold | Metal1 | 8/0 | 25 | 816.5 | 0.987 (red covered 99.9 %, orange 99.7 %, gold 99.9 %) |
| purple | Metal2 | 10/0 | 2 | 74.4 | 0.980 |
| blue | Metal3 | 30/0 | 12 | 484.1 | 0.989 |
| green | Metal4 | 50/0 | 13 | 478.4 | 0.967 |

(The GDS reader counts a few more polygons than written because the writer splits any polygon above 4000 vertices; the pieces abut and merge.)
Reasons and the merge are in `ART_LAYERS.md`.

**What the shared Metal1 layer does (red + orange, plus gold):** red and orange touch in the source at two small places on the lower-left edge of the orange word
(clusters about 1.35 x 1.15 um and 2.50 x 1.20 um). On Metal1 both are in **one polygon with the red ribbon**: `build_stats.json` lists one fused component holding
red and orange, art box (7.35, 22.25) - (64.25, 35.45) um, i.e. slot coordinates (95.85, 163.55) - (152.75, 176.75), 107.9 um2. Gold (13.5 um from red, 9.8 um from orange) fuses with nothing.
**Lost:** the colour difference between red, orange and gold; all curves are 50 nm staircases; thin tapering tips are thickened to the minimum width (about 0.35 um).
Where two layers cross in plan view the upper hides the lower; no vias, nothing connects.

## How the geometry was made

1. `segment.py`: the six reference colours are sampled from the legend squares; class = hue band; orange vs gold share a hue band and are separated
   by position (orange = warm pixels left of x = 795 and above y = 676 in source pixels); a 5x5 mode filter removes hue-mixed edge fringes;
   soft coverage from unmixing against the white background. Legend cut: art ends at source row 896, the legend begins at row 897 (87.6 % of the
   height; the brief said roughly 87 %, a cut at 891 would clip the lowest tip of the gold ornament).
2. Coverage resampled to a 0.05 um grid at the scale and cut at 0.5.
3. Per layer: widths floored along the skeleton, closing (space) and opening (width) with a chamfered-square kernel (7 cells = 0.35 um body, 0.25 um flat) until stable;
   specks under two kernel squares dropped.
4. Polygons: runs of 0.05 um cells merged = staircases, only 0 / 90 degree edges, all vertices multiples of 50 nm (on the 5 nm grid; the deck's
   angle rule allows only 0 / 45 / 90 degrees). A 45-degree outline (marching squares) was tried first and gave tens of Mn.a / Mn.b / Mn.i markers per layer
   (for example 86 on Metal4) at round stroke ends and tight bends, because two convex 45-degree turns over a short edge are measured as narrow width.
   A disk kernel with the staircase failed for the same reason at stroke tips; the chamfered square keeps a flat of at least 0.25 um at every extremity.
5. Repair: the deck's Euclidean width and space checks, at rule + 0.01 um, run on each layer's region; each marker is covered by a box (marker + 75 nm, snapped to 50 nm)
   and merged; repeated until empty (Metal1 needed 8 passes of at most 24 markers, Metal4 4 of at most 28, Metal2 4 of at most 4, Metal3 3 of at most 5).

## Verification (details in `art/verify_report.md`)

- **DRC** (PDK `run_drc.py`, all tables, density and antenna on, deep mode): original slot_7 violates `AFil.g, GFil.g, M1.j, M2.j, M3.j, M4.j, TM1.c`
  (global minimum densities of the bare slot; they are chip-level rules and the slot has no fill). The merged GDS violates **exactly the same rules with
  the same marker counts: no new violation from the art** (min width, min space, 45-degree rules, area, max density, slit rules, antenna: none).
  The deck's slit rules (Slt.e1 for MIM, Slt.i slit density) report nothing.
  Densities (chip = slot here): Metal1 1.64 -> 2.20 %, Metal2 0.76 -> 0.81 %, Metal3 2.14 -> 2.47 %, Metal4 0.65 -> 0.98 %, TopMetal1 unchanged.
  The art only raises minimum density; no maximum rule is near its limit.
- **XOR**: merged with the `tughra_art` cell deleted vs the original, flattened over all 34 layer/datatypes: **0 polygons**; labels and cell list identical.
- **LVS** (PDK `run_lvs.py --run_mode=deep --disable_tap_extraction` against slot7's `netlist/slot_7.cdl`, the recipe in slot7's README): original PASS, merged PASS
  (0 errors, 0 warnings), extracted layout netlists identical. The work repo's own `make` LVS flow is for the template macros, not slot7, so the PDK script was used.
- **Previews**: `preview_side_by_side.png` (source left, art right), `preview_layers.png`, `preview_slot_context.png`.

## Assumptions (all of them)

1. "Default branch" = `origin`'s HEAD, `main`, not the session branch.
2. Legend cut at source row 897 (the first row of legend ink), not at 87 % = row 891.
3. One scale for the whole art; aspect kept (1.70, not exactly 3:2, because the legend row is cut).
4. The art goes into the largest rectangle that is free on the four art metals and clear of the TopMetal1 straps (so nothing is hidden under a strap), not into the
   largest single-layer rectangles.
5. Margins: 1 um (Metal1-4), 5 um from the slot edge.
6. **Rev 3 request: no TopMetal1, and red and orange on one layer.** That alone leaves five groups for four layers, so a second merge was needed:
   **gold joins red and orange on Metal1** (gold already shared a layer with orange in rev 1 and 2, and it touches neither). If a different second merge was meant, change `LAYER_OF` in `build_art.py`.
7. Design minimum width / space are larger than the PDK minimum (0.25 um flats on Metal1-4) so that the deck's Euclidean checks pass on staircases; thin strokes are thickened, never removed.
8. Orange vs gold told apart by position, since their hues overlap.
9. Different layers may cross in plan view; no vias; the art has no labels or pins, so every polygon is a floating, unnamed net.
10. Cell name `tughra_art` as asked; slot7's README says sub-cells of slot_7 carry the prefix `slot7_` (the actual GDS has no prefix; the harness prefixes on import).
    If the harness needs the prefix, change `CELL` in `build_art.py`.
11. The art is placed as a cell reference in the top cell `slot_7` of the merged copy (slot7's own cells are untouched).
12. "Metal density rules" were judged by the deck's global (chip = slot) and 800 x 800 um window rules; the slot sits in a larger chip, so only the added metal, not the absolute density, is meaningful.
13. Real colour under a microscope is not controlled; all four layers are aluminium.

## Not done / risks

- **No no-fill marker is drawn around the art.** If the harness fills the slot (metal, Activ, GatPoly fillers; the bare slot is far below the minimum densities),
  filler shapes would land between and around the art strokes. Whether the harness' fill respects `*.nofill` datatypes (e.g. Metal1.nofill 8/23) is not checked here.
- The harness flow (projects-gds, gds-prefill, net check) was not run; floating unlabelled metal may need a look there.
- No PEX; the art is at least 36 um from existing metal on the same layer and at least 28 um from any other metal layer except the TopMetal1 strap (1.3 um, no overlap), so coupling is not expected to matter but was not extracted.
- Writing back into the slot7 repo is a separate step, not done.
