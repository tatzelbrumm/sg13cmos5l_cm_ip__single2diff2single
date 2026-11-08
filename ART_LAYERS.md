# ART_LAYERS: proposed metal layer per colour (tughra art in slot_7)

Numbers come from the PDK files (`art/pdk_layers.py` reads `sg13cmos5l.lyp` and `sg13cmos5l_tech_default.json`), the
slot7 GDS (`art/find_free_space.py`, report in `art/free_space.md`) and the source image (`art/segment.py`). Stroke
widths are measured at the scale used (ART_NOTES.md).

The process has **five** metal layers (Metal1..Metal4, TopMetal1; Metal5/TopMetal2 are forbidden by the deck,
`CMOS5L.FORB`). The art uses GatPoly and Metal1..Metal4; TopMetal1 is not used.

## Mapping (revision 4: GatPoly added, TopMetal1 still unused, red and orange on one layer)

Requested: poly as an extra layer, nofill markers, red and orange still on one layer (rev 3). With GatPoly there are **five** art layers
(GatPoly, Metal1..Metal4) for six colours, and red + orange sharing one layer makes exactly five groups, so **no second merge is needed any more** (gold gets its own layer again).

| colour | layer | GDS layer/datatype | PDK min width / min space (um) | reason |
|---|---|---|---|---|
| purple | GatPoly | 5/0 | 0.13 / 0.18 | The smallest element (one word, three pieces, 74 um2) and it touches no other colour, so if poly turns out to be the layer that is hard to see, little is lost. Poly has the finest rules of all five layers. Poly alone on field oxide, with **no Activ underneath**: a test with Activ under the strokes violated Act.a, Act.b, Act.d, Gat.c (0.18 um end cap), Gat.f (no 45/90-degree corners of poly on Activ) and LU.b (Activ counts as N+ and needs a pSD tie within 20 um), while poly alone added no violation and left LVS unchanged. The floating poly is not tied to any gate, so antenna diodes are not needed. |
| red, orange (shared) | Metal1 | 8/0 | 0.16 / 0.18 | As requested. Metal1 has the finest metal rules and this group holds fine detail (orange word, red word). |
| gold | Metal2 | 10/0 | 0.20 / 0.21 | Long thin swoosh and one word; touches no red or orange stroke. |
| blue | Metal3 | 30/0 | 0.20 / 0.21 | Long ribbon plus the large word. Metal3 is the busiest layer of the slot (92 % free) but the chosen spot is free on it. |
| green | Metal4 | 50/0 | 0.20 / 0.21 | Tall stems, the densest cluster; the highest metal that can hold detail, hence the most visible layer, and 98 % of the slot is free on it. |

Stack order seen from above: Metal4 (green) > Metal3 (blue) > Metal2 (gold) > Metal1 (red/orange) > GatPoly (purple). All metal is above poly, so a poly stroke
is seen only where no metal covers it. Because each colour's mask already has a gap where another colour hid it in the source, the stacking order changes
the picture only where a layer was thickened.

**No-fill markers** (new): one rectangle on each of Activ.nofill 1/23, GatPoly.nofill 5/23, Metal1..Metal4.nofill 8/23, 10/23, 30/23, 50/23 and
TopMetal1.nofill 126/23 (the PDK's filler script `macros/sg13cmos5l_filler_*.lym` excludes exactly these datatypes; TopMetal1 filler would otherwise cover
the art from above), covering the art box grown by 3 um and clipped to the free region, so that the harness' filler stays out of the art. Activ and TopMetal1 carry only the marker, no art.
The deck limits a poly no-fill box to 400 x 400 um (GFil.i); the box is about 158 x 90 um.

## The merge: what touches and what is lost

Measured on the segmented image:

- **Red and orange touch directly** at **two small places** on the lower-left edge of the orange word where it meets the red ribbon
  (clusters about 1.35 x 1.15 um and 2.50 x 1.20 um). On Metal1 they **fuse into one polygon** with the red ribbon. Nothing else of the two colours is within the minimum space.
- **Lost:** the colour difference between red and orange (both Metal1); the orange word's separation from the red ribbon at the two contacts.
- Gold, purple, blue, green each have a layer of their own; where they cross others in plan view the upper layer hides the lower one and nothing connects (no vias).

## Revision history

- Rev 1 (first commit): green TopMetal1, red Metal4, blue Metal3, purple Metal2, orange + gold Metal1.
- Rev 2 (tag `art-rev2-topmetal1`, local only; commit `abe3133`): purple TopMetal1, green Metal4, red Metal3, blue Metal2, orange + gold Metal1. Motivation: green on TopMetal1 turned the stems into one blob
  and red's word into mush when tested at 1.64 um (IoU of the result with the source mask: red 0.65, green 0.63, purple 0.61, blue 0.59, gold 0.54, orange 0.43,
  test at 0.0955 um/px). Result: the purple word became a blob (IoU 0.48).
- Rev 3 (tag `art-rev3-m1-m4`, local only): no TopMetal1; red, orange and gold on Metal1; purple Metal2; blue Metal3; green Metal4.
- Rev 4 (this one): GatPoly added for purple; red + orange on Metal1; gold Metal2; blue Metal3; green Metal4; nofill markers.

## Caveats stated up front

- **Metal1-Metal4 get a design minimum of about 0.35 um body and 0.25 um flat** (the PDK minimum is 0.16 / 0.18 on
  Metal1 and 0.20 / 0.21 on Metal2-4), so that the deck's Euclidean width and space checks pass on 50 nm staircases. Strokes thinner than that are thickened to it.
- **Edges are 0 / 90 degrees only** (50 nm staircases): the deck's angle rule allows only 0 / 45 / 90 degrees on metal, and 45-degree chamfers
  were measured to fail the width and space rules at every round stroke end and tight bend.
- **Colour under a microscope is not guaranteed.** The metals are aluminium, so the colours will not look like the source; what differs is height
  and the dielectric stack above each layer. Metal4 is the most visible; poly lies about 1 um under Metal1 beneath transparent oxide, and how well it shows is **not verified**. The mapping makes the *shapes* distinguishable, not the hues.
- **Density:** the art adds a few percent of local metal on each layer, and the deck's density rules are global per chip (35-60 % on Metal1-4) or per 800 x 800 um window with
  fillers, so the art can only help the minimum. The slot has no fill of its own; the harness fills.
- **Slotting:** the metal slit rules concern wide metal; no art stroke is wider than about 2.2 um.
- **Layers slot7 reserves:** the slot7 documents name none. The slot7 GDS has a no-fill marker (datatype 23) on Metal1 and
  Metal2 along the right edge (x 535.15 to 537.15 um) and its supply straps on TopMetal1 at y 130-140 and 232-242 um;
  the chosen region is clear of all of them (see `art/free_space.md`). TopMetal1 is not used by the art.
