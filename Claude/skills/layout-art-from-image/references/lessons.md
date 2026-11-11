# Lessons from the first project (IHP sg13cmos5l, tughra calligraphy in slot_7)

Source: `ART_NOTES.md`, `ART_LAYERS.md`, `art/*` on branch `art/tughra-metal`. Everything marked (measured) was run; "not verified" was not.

## Free space and placement
- Slot 537.15 x 273 um; per-layer free fraction 88-98 %. Largest per-layer rectangles were up to 285 x 263 um, but supply straps on the top metal cross them: art on lower metals under a strap is hidden from above. The placement rectangle was the one free on all art layers and clear of the straps (319 x 90 um). Height set the scale. (measured)
- Margins used: 1 um on poly and Metal1-4 (about 5x minimum spacing, above the widest wide-metal spacing 0.6 um and the filler distance 0.42 um), 3 um on top metal (its filler spacing), 5 um to the slot edge. The handover docs held no keep-out rules.

## Layer choice
- IHP sg13cmos5l has only Metal1-4 and TopMetal1 (Metal5 / TopMetal2 are forbidden by the deck). TopMetal1 needs 1.64 um width and space, 5-8x the others: tested on all six colours, every colour lost detail (IoU with the source 0.43-0.65); green stems fused into a blob, a small word became a blob. User decision: do not use it.
- Poly (min 0.13 / 0.18 um) alone, on field oxide, added no DRC rule and left LVS unchanged. With active under it: Act.a, Act.b, Act.d, Gat.c (end cap 0.18), Gat.f (no 45/90 degree corners on active) and LU.b (active counts as N+ and needs a pSD tie within 20 um) were violated. (measured)
- Final mapping: purple GatPoly, red + orange Metal1 (user request; they touch at two small places and fuse there), gold Metal2, blue Metal3, green Metal4. Shape fidelity (IoU with the source mask) 0.97-0.99.

## Geometry
- Segmentation: references from the legend squares; hue bands; orange and gold share a hue band, so split by position; 5x5 mode filter removes hue-mixed fringes; unmix against the off-white background for soft coverage.
- A first version with 45 degree outlines (marching squares) gave tens of width / space / 45-degree-spacing markers per layer at every round end and tight bend. The deck's Euclidean check measures the distance between non-adjacent edges: two convex 45 degree turns over a short edge count as a narrow width. A disc kernel with a staircase failed at tips for the same reason (rows only 1-2 cells wide).
- What passed: chamfered-square kernel (7 cells = 0.35 um body, 0.25 um flat at 50 nm), 0/90 degree staircases on the 50 nm grid, then a repair loop with KLayout `width_check` / `space_check` at rule + 0.01 um, covering each marker with a snapped box, until empty.
- Writer: polygons above 4000 vertices are split by the GDS writer; the pieces abut and merge.

## Verification
- Compare rule sets and marker counts original vs merged: the bare slot already violated seven global minimum-density rules, so "no violations" would have been the wrong test. XOR of merged-minus-art-cell vs original: 0 polygons over 39 layer/datatypes. LVS deep, tap extraction off: identical extracted netlists.
- Density deltas were small (Metal1 1.64 -> 2.01 %); the rules are chip-level, so only the delta means anything.
- Filler: the PDK filler only fills inside a seal ring (layer 39/0), the bare slot had none, so a synthetic ring was added in scratch copies. Control without markers: 126-661 filler shapes per layer touching the art box (4000-7000 um2 of Activ, poly and Metal1-4 filler inside); with the seven nofill markers: 0 area inside the box. A different harness filler might not honour the markers.

## Process
- Commit the layer proposal on its own before the geometry; it was revised three times, each with a measured reason, the history shows why.
- Do not claim what was not run: poly visibility under a microscope, colour appearance, harness flow, PEX were all untested and are listed as such.
- Branch hygiene: the brief said "default branch"; the user later wanted another base (`toplevel`, unrelated history to `main`). Check `git merge-base` before claiming one branch contains another; it printed nothing for these two. A rebase of a pushed branch needs `--force-with-lease`.
- The remote refused tag pushes in the cloud session (branch pushes worked).
