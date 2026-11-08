# ART_LAYERS: proposed metal layer per colour (tughra art in slot_7)

Proposal, written before the geometry. Numbers come from the PDK files (`art/pdk_layers.py` reads
`sg13cmos5l.lyp` and `sg13cmos5l_tech_default.json`), the slot7 GDS (`art/find_free_space.py`, report in
`art/free_space.md`) and the source image (`art/segment.py`). Stroke widths are measured at the planned scale of
0.098 um per source pixel (see ART_NOTES.md for the final scale).

The process has **five** metal layers (Metal1..Metal4, TopMetal1; Metal5/TopMetal2 are forbidden by the deck,
`CMOS5L.FORB`). Six colours do not fit one-to-one, so two colours share a layer.

| colour | layer | GDS layer/datatype | min width / min space (um) | reason |
|---|---|---|---|---|
| green | TopMetal1 | 126/0 | 1.64 / 1.64 | Widest strokes (median 1.57 um, thickest 2.2 um; the three tall stems are 1.9-2.2 um). Only TopMetal1's 1.64 um minimum can be met by the stems without losing them, and the three stems are 5+ um apart, so the 1.64 um spacing costs little. TopMetal1 is also the topmost, thickest metal, so the biggest element is the most visible one, and in the source the green stems lie over the ribbons, as they do here. |
| red | Metal4 | 50/0 | 0.20 / 0.21 | Long, medium-width ribbon (median 1.4 um). Metal4 is the highest layer under TopMetal1, so it is the second most visible. Free on the whole slot except a few straps (98 % free). In the source the red ribbon lies over the blue one where they cross, which Metal4 over Metal3 reproduces. |
| blue | Metal3 | 30/0 | 0.20 / 0.21 | Second long ribbon (median 1.25 um, thin tail 0.4 um). Metal3 is the busiest layer of the slot (92 % free) but the chosen spot is free on it. Lies under red, as in the source. |
| purple | Metal2 | 10/0 | 0.20 / 0.21 | Smallest element (67 um2, three pieces, one word). Lowest visibility is acceptable for the smallest colour; it hardly crosses any other colour (0.7 um2 within 0.3 um of blue). |
| orange **and** gold (shared) | Metal1 | 8/0 | 0.16 / 0.18 | Finest detail: orange is the smallest, densest calligraphy (strokes 0.4 um at the thinnest) and gold has the 0.4 um swoosh tail; Metal1 has the smallest minimum width and space of the stack. These two colours are the neighbours in hue, so merging them loses the least. |

## The merge: what touches and what is lost

- Orange and gold are the pair chosen. Measured on the segmented image: **the closest orange stroke and gold stroke are
  9.4 um apart** (96 px at 0.098 um/px). No stroke of the two colours touches, comes within the layer's minimum
  space, or merges. Nothing is shorted and no polygon is joined by the merge.
- **Lost:** the colour distinction orange vs gold (both words are Metal1 and look the same under a microscope).
  The words stay separate shapes.
- Other pairs with zero contact exist (blue-orange, orange-purple, purple-red, gold-red) but they differ more in hue
  or use different thickness classes; orange-gold was preferred for the hue reason.
- Different layers cross in plan view (for example green over red). No vias are drawn, so nothing connects.
  The upper layer hides the lower one where they overlap when seen from above; the order TopMetal1 > Metal4 >
  Metal3 > Metal2 > Metal1 is green > red > blue > purple > orange/gold.

## Caveats stated up front

- **TopMetal1 minimum width 1.64 um is larger than most of the green stroke.** At the planned scale 53 % of the
  green skeleton is already below 1.64 um. The green strokes will be thickened and the thin tapering tips and
  the thin cross strokes (where they are thinner than the minimum) will be thickened or dropped; green strokes closer
  than 1.64 um will merge. The shape loss is measured and reported in ART_NOTES.md.
- **Metal1-Metal4 get a design minimum of 0.30 um width and 0.30 um space** (the PDK minimum is 0.16 / 0.18 on
  Metal1 and 0.20 / 0.21 on Metal2-4), so that the 45-degree and wide-line spacing rules (0.22 / 0.24 um) and the
  grid snapping have margin.
- **Edges are 0 / 45 / 90 degrees only**: the deck's angle rule (`3_2_angle.drc`) allows only those on metal. Curves are
  therefore octilinear stair-steps, not smooth curves.
- **Colour under a microscope is not guaranteed.** All five layers are aluminium, so the six colours will not look
  like the source; what differs is height and the dielectric stack above each layer. TopMetal1 and Metal4 are the most
  visible; Metal1 and Metal2 are the least. The layer mapping makes the *shapes* distinguishable, not the hues.
- **Density:** the art adds under 5 % local metal on each layer and the deck's density rules are global per chip
  (35-60 % on Metal1-4, 25-70 % on TopMetal1) or per 800 x 800 um window with fillers, so the art can only help the
  minimum. The slot has no fill of its own; the harness fills.
- **Slotting:** the metal slit rules concern wide metal; no art stroke is wider than about 2.2 um.
- **Layers slot7 reserves:** the slot7 documents name none. The slot7 GDS has a no-fill marker (datatype 23) on Metal1 and
  Metal2 along the right edge (x 535.15 to 537.15 um) and its supply straps on TopMetal1 at y 130-140 and 232-242 um;
  the chosen region is clear of all of them (see `art/free_space.md`).
