# ART_LAYERS: proposed metal layer per colour (tughra art in slot_7)

Numbers come from the PDK files (`art/pdk_layers.py` reads `sg13cmos5l.lyp` and `sg13cmos5l_tech_default.json`), the
slot7 GDS (`art/find_free_space.py`, report in `art/free_space.md`) and the source image (`art/segment.py`). Stroke
widths are measured at the scale used (ART_NOTES.md).

The process has **five** metal layers (Metal1..Metal4, TopMetal1; Metal5/TopMetal2 are forbidden by the deck,
`CMOS5L.FORB`). The art uses only Metal1..Metal4, so colours share layers.

## Mapping (revision 3: no TopMetal1, red and orange on one layer)

The requester ruled out TopMetal1 as too coarse (1.64 um minimum width and space) and asked for red and orange on the same layer.
That leaves Metal1..Metal4 for six colours. Red + orange alone would still need five layers, so **one more merge was needed**;
the one chosen is gold, which already shared a layer with orange in revision 1. This is an assumption (see below).

| colour | layer | GDS layer/datatype | PDK min width / min space (um) | reason |
|---|---|---|---|---|
| red, orange **and** gold (shared) | Metal1 | 8/0 | 0.16 / 0.18 | Metal1 has the finest rules, and this group holds the finest detail (orange word, gold swoosh tail 0.4 um, red word). The three colours are mutually far apart except two small contacts between red and orange (below). |
| purple | Metal2 | 10/0 | 0.20 / 0.21 | Smallest element (one word, three pieces); it touches no other colour (0.0 um2 within 0.3 um of red or orange, 0.7 um2 of blue). |
| blue | Metal3 | 30/0 | 0.20 / 0.21 | Long ribbon plus the large word. Metal3 is the busiest layer of the slot (92 % free) but the chosen spot is free on it. |
| green | Metal4 | 50/0 | 0.20 / 0.21 | Tall stems, the densest cluster; the highest metal that can hold detail, hence the most visible layer, and 98 % of the slot is free on it. |

Stack order seen from above: Metal4 (green) > Metal3 (blue) > Metal2 (purple) > Metal1 (red/orange/gold). Because each colour's mask already has a
gap where another colour hid it in the source, the stacking order changes the picture only where a layer was thickened.

## The merge: what touches and what is lost

Measured on the segmented image at the scale used (0.102 um per source pixel):

- **Red and orange touch directly** (distance 0.0). The contact is at **two small places**, both on the lower-left edge of the orange word
  where it meets the red ribbon: a cluster about 1.35 x 1.15 um and one about 2.50 x 1.20 um, roughly 50-52 um from the left edge and
  60-61 um from the top of the art. On Metal1 these strokes **fuse into the red ribbon**, so the orange word stays attached to the red
  ribbon at those two spots. Nothing else of the two colours is within the minimum space.
- **Gold** is 13.5 um from the nearest red stroke and 9.8 um from the nearest orange stroke: it touches nothing and merges with nothing.
- **Lost:** the colour difference between red, orange and gold (all Metal1); the orange word's separation from the red ribbon at the two contacts.
- Other layers cross these in plan view; no vias are drawn, so nothing connects. The upper layer hides the lower one where they overlap.

## Revision history

- Rev 1 (first commit): green TopMetal1, red Metal4, blue Metal3, purple Metal2, orange + gold Metal1.
- Rev 2 (second commit): purple TopMetal1, green Metal4, red Metal3, blue Metal2, orange + gold Metal1. Motivation: green on TopMetal1 turned the stems into one blob
  and red's word into mush when tested at 1.64 um (IoU of the result with the source mask: red 0.65, green 0.63, purple 0.61, blue 0.59, gold 0.54, orange 0.43,
  test at 0.0955 um/px). Result: the purple word became a blob (IoU 0.48).
- Rev 3 (this one): requested change, no TopMetal1; red, orange and gold on Metal1; purple Metal2; blue Metal3; green Metal4.

## Caveats stated up front

- **Metal1-Metal4 get a design minimum of about 0.35 um body and 0.25 um flat** (the PDK minimum is 0.16 / 0.18 on
  Metal1 and 0.20 / 0.21 on Metal2-4), so that the deck's Euclidean width and space checks pass on 50 nm staircases. Strokes thinner than that are thickened to it.
- **Edges are 0 / 90 degrees only** (50 nm staircases): the deck's angle rule allows only 0 / 45 / 90 degrees on metal, and 45-degree chamfers
  were measured to fail the width and space rules at every round stroke end and tight bend.
- **Colour under a microscope is not guaranteed.** All four layers are aluminium, so the six colours will not look like the source; what differs is height
  and the dielectric stack above each layer. Metal4 is the most visible and Metal1 the least. The mapping makes the *shapes* distinguishable, not the hues.
- **Density:** the art adds a few percent of local metal on each layer, and the deck's density rules are global per chip (35-60 % on Metal1-4) or per 800 x 800 um window with
  fillers, so the art can only help the minimum. The slot has no fill of its own; the harness fills.
- **Slotting:** the metal slit rules concern wide metal; no art stroke is wider than about 2.2 um.
- **Layers slot7 reserves:** the slot7 documents name none. The slot7 GDS has a no-fill marker (datatype 23) on Metal1 and
  Metal2 along the right edge (x 535.15 to 537.15 um) and its supply straps on TopMetal1 at y 130-140 and 232-242 um;
  the chosen region is clear of all of them (see `art/free_space.md`). TopMetal1 is not used by the art.
