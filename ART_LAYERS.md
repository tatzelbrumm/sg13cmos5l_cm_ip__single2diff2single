# ART_LAYERS: proposed metal layer per colour (tughra art in slot_7)

Numbers come from the PDK files (`art/pdk_layers.py` reads `sg13cmos5l.lyp` and `sg13cmos5l_tech_default.json`), the
slot7 GDS (`art/find_free_space.py`, report in `art/free_space.md`) and the source image (`art/segment.py`). Stroke
widths are measured at the scale used, 0.0975 um per source pixel (ART_NOTES.md).

The process has **five** metal layers (Metal1..Metal4, TopMetal1; Metal5/TopMetal2 are forbidden by the deck,
`CMOS5L.FORB`). Six colours do not fit one-to-one, so two colours share a layer.

## Mapping (revised after the first geometry run, see "Revision" below)

| colour | layer | GDS layer/datatype | PDK min width / min space (um) | reason |
|---|---|---|---|---|
| purple | TopMetal1 | 126/0 | 1.64 / 1.64 | TopMetal1 cannot draw fine calligraphy: its 1.64 um minimum width and space are 5-8x the other layers'. It gets the smallest, simplest element (one word, 64 um2, 3 pieces) so that the damage is smallest. It is the topmost, thickest metal, so this element is the most visible one under a microscope. |
| green | Metal4 | 50/0 | 0.20 / 0.21 | Tall stems and a word; the stems converge into a dense cluster (on TopMetal1 that cluster merged into one blob in the test). Metal4 is the highest layer that can hold detail and the second most visible. 98 % of the slot is free on Metal4. In the source green lies over red and blue where they cross, and Metal4 is above Metal3 and Metal2. |
| red | Metal3 | 30/0 | 0.20 / 0.21 | Long ribbon plus one word, strokes 0.4-2 um. Lies over blue in the source and Metal3 is above Metal2. Metal3 is the busiest layer of the slot (92 % free) but the chosen spot is free on it. |
| blue | Metal2 | 10/0 | 0.20 / 0.21 | Second long ribbon plus the large word, thin tail 0.4 um. Lowest of the three ribbon colours, as in the source. |
| orange **and** gold (shared) | Metal1 | 8/0 | 0.16 / 0.18 | Finest detail: orange is the smallest, densest calligraphy and gold has the 0.4 um swoosh tail; Metal1 has the smallest minimum width and space of the stack. These two colours are neighbours in hue, so merging them loses the least. |

Stack order seen from above: TopMetal1 (purple) > Metal4 (green) > Metal3 (red) > Metal2 (blue) > Metal1 (orange/gold).

## The merge: what touches and what is lost

- Orange and gold are the pair merged. Measured on the segmented image: **the closest orange stroke and gold stroke
  are 9.4 um apart** (96 px at 0.098 um/px). No stroke of the two colours touches, comes within the layer's minimum
  space, or merges. Nothing is shorted and no polygon is joined by the merge.
- **Lost:** the colour distinction orange vs gold (both words are Metal1 and look the same under a microscope).
  The words stay separate shapes.
- Different layers cross in plan view. No vias are drawn, so nothing connects. The upper layer hides the lower one
  where they overlap when seen from above.

## Revision (why the first proposal changed)

The first proposal put green on TopMetal1, red on Metal4, blue on Metal3, purple on Metal2. Before writing any
polygon I measured how each colour survives TopMetal1's 1.64 / 1.64 rule (strokes widened to 1.7 um, gaps under 1.7 um
closed, one test run at 0.0955 um/px, intersection-over-union of the result with the source mask):

| colour | source area (um2) | area on TopMetal1 | IoU |
|---|---|---|---|
| red | 370 | 567 (x1.53) | 0.65 |
| green | 403 | 641 (x1.59) | 0.63 |
| purple | 64 | 105 (x1.65) | 0.61 |
| blue | 422 | 715 (x1.69) | 0.59 |
| gold | 234 | 435 (x1.86) | 0.54 |
| orange | 103 | 243 (x2.35) | 0.43 |

The IoU values are close, but the pictures are not: green on TopMetal1 turned its converging stems into one blob;
red on TopMetal1 kept the long ribbons but its word became unreadable. Whichever colour gets TopMetal1 loses its
detail, so the **smallest colour (purple) takes it** and the four finer layers keep all other colours at nearly
full detail. Cost: the purple word becomes a blob (its letter shapes are lost) and TopMetal1 shows only that.

## Caveats stated up front

- **TopMetal1 minimum width 1.64 um is larger than most of a purple stroke.** Purple strokes are widened to 1.7 um
  and gaps under 1.7 um are filled, so the word becomes a solid shape.
- **Metal1-Metal4 get a design minimum of 0.30 um width and 0.30 um space** (the PDK minimum is 0.16 / 0.18 on
  Metal1 and 0.20 / 0.21 on Metal2-4), so that the 45-degree and wide-line spacing rules (0.22 / 0.24 um) and the
  grid snapping have margin. Strokes thinner than 0.30 um are widened to it.
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
