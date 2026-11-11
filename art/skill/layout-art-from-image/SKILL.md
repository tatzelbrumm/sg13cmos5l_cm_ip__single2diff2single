---
name: layout-art-from-image
description: Turn a raster image (logo, calligraphy, drawing, photo outline) into DRC-clean floating layout art in a chip's GDS, on metal and poly layers of an open PDK (IHP SG13, SKY130, GF180MCU). Covers finding empty space, choosing one layer per colour, tracing to grid-snapped polygons, nofill markers, and verifying with DRC, XOR, LVS and a filler test. Use when asked for die art, layout art, a logo or picture on a chip, or "image to GDS".
---

# Layout art from an image (GDS, open PDKs)

Reference implementation: IHP **sg13cmos5l** (branch `art/tughra-metal` of `tatzelbrumm/sg13cmos5l_cm_ip__single2diff2single`, `ART_NOTES.md`,
`ART_LAYERS.md`). The scripts in `scripts/` are copies of that work. They read layer numbers and rules from the PDK files, but the
rule names, the DRC / LVS commands and the no-fill convention are IHP-specific: for another PDK follow `references/pdk_checklist.md` and adapt
`pdk_layers.py` and the verify step. Do not assume the scripts run unchanged on SKY130 or GF180.

## Before starting
1. Read `references/lessons.md` (what failed, what worked) and `references/pdk_checklist.md`.
2. If the brief says "work unattended": decide, record every decision in `ART_NOTES.md`, carry on. Otherwise ask only what changes the plan (which layers are allowed, which region, which PDK).
3. Treat the host layout repo (the "handover" repo) as **read only**: copy its GDS, write only in your own work repo. Never edit the original GDS.

## Workflow
1. **Free space.** For each metal (and poly) layer: free = layout boundary shrunk by an edge margin minus every shape on that layer (all datatypes) grown by a margin
   (>= the largest spacing rule that can apply, and >= the filler distance). Report the largest free rectangles per layer. Choose the placement region that is free on **all** art layers **and clear
   of top-metal straps** (a top-metal strap hides lower art from above). Read the host docs for keep-outs. (`find_free_space.py`)
2. **Layers.** One layer per colour if the process has enough; otherwise merge the colours that touch least (measure contact, say exactly what fuses). Put fine detail on the layer with the finest rules,
   put the smallest or least important colour on the layer that is coarse or hard to see. Measure how each colour survives each layer's minimum width before deciding. Write `ART_LAYERS.md` and commit it **before** the geometry.
3. **Segment.** Sample the colour references from the legend, class = hue band, position tie-breaks for overlapping hues, mode filter against fringes, soft coverage. Cut the legend row out. (`segment.py`)
4. **Geometry.** Resample to a grid (50 nm worked), widen strokes along their skeleton to the design minimum, close (space) and open (width) with a **chamfered-square** kernel, write **0/90 degree
   staircase polygons** on the manufacturing grid, then run the deck's own Euclidean width/space check on each layer and patch the markers until it is empty. (`build_art.py`)
5. **GDS.** Art in its own cell, written by a re-runnable script; a merged copy of the host GDS with the art placed; **nofill markers** on every art layer (and the layers the filler would use) around the art. Never touch the original file.
6. **Verify** (all, with results in `ART_NOTES.md`): full DRC on original and merged (compare rule sets and marker counts, not just "pass"), XOR merged-minus-art cell vs original (must be empty), LVS before and after (extracted netlists identical),
   clearance to existing shapes, density deltas, previews (side by side with the source), and a **filler test** with a control. (`verify_art.py`, `fill_test.py`, `preview.py`)
7. **Deliver.** Small commits: layer proposal, scripts, then outputs; push each branch; no PR unless asked; list every assumption.

## Hard rules learned (details in references/lessons.md)
- No 45 degree chamfers or disc-rounded ends: the deck's Euclidean width / space checks flag short edges between two convex 45 degree turns; a staircase with flat extremities of at least the minimum width passes.
- Floor widths along the centreline instead of deleting thin strokes; accept that thin tips get thicker.
- Poly **without** active underneath. Poly over active triggers end-cap, angle and latch-up rules and can create devices. A floating poly is tied to no gate, so no antenna diodes or taps are needed.
- The coarsest layer (top metal) takes the smallest colour or none; check how each colour survives before assigning.
- Each colour mask has gaps where another colour hid it in the source, so the stacking order changes little.
- Without nofill markers the PDK filler puts hundreds of shapes into the art; some fillers only run inside a seal ring, so test with a synthetic ring.
- Judge density rules as chip-level; the art can only help a minimum density.
- Not verified, say so: how visible poly or any lower layer is under a microscope; colour is not controlled.

## Starting the next project
`START_NEXT_ART_PROJECT.md` is a short prompt to paste into a new chat or Cowork session together with the image.
