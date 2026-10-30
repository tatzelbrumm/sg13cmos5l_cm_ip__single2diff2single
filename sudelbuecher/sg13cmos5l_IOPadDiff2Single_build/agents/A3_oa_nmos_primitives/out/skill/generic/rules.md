<!--
SPDX-FileCopyrightText: 2026 Christoph Maier
SPDX-License-Identifier: Apache-2.0
-->
# Rules followed, process-agnostic form [generic]

2026-10-28, Claude (Opus 5.5). Each rule names the adapter values (semantic names, `adapter_template.py`) that
force it. The values for IHP sg13cmos5l, with deck citations: `../ihp_sg13cmos5l/rules.md` (same numbering).

## Do

1. **[generic] Rotate fingers so the gate runs along the row** (W along the row, L across it) and place them at
   `finger_gap`: the poly endcaps merge into one gate strip per row, and gate contacts are needed only at the row
   ends. Runs of the same device become one array instance.
2. **[generic] Interdigitate by rows; keep every row pure in (S, D).** Then each stripe line carries one net, a
   single Metal2 track runs directly over it, and rows stack at `active_space`: row pitch = active height +
   `active_space`, no band between rows. Check once: facing tracks of adjacent rows are
   `active_space + 2 * stripe_inset - track_w` apart, which must be >= `m2_space`.
3. **[generic] Track and pad from the via:** track width = `via1 + 2 m2_via1_endcap`; M1 pad across a stripe =
   `via1 + 2 via1_m1_enc` high, `n via1 + (n-1) via1_space + 2 via1_m1_endcap` long; up to three vias per finger.
4. **[generic] No tie between rows. Tie segments only at the periphery, only where the latch-up distance needs
   them, following the outline (no closed ring).** One contact row: height = `cont + 2 cont_in_active`. Measure
   the farthest N+ active from the tie and compare with `lu_ptie`; report the number per segment.
5. **[generic] Narrow end dummies (same L), D = S tied by one vertical M1 strap over the dummy column through all
   rows;** the strap doubles as the vertical of that net (vias from its tracks land on it). Dummy gates stay on the
   row's gate strip (uniform spacing at the row ends).
6. **[generic] Vertical structures, from the array outwards: strap, gate bar, joiner(s).** Gate contact at
   `max(m1_space, polycont_to_active)` from the active end (the end finger's stripes end there); bar width >=
   `via1 + 2 via1_m1_enc`; poly tab `cont_in_poly` beyond the contact; joiner `m1_space` outside the bar. A strap
   wider than `m1_wide_w` keeps `m1_wide_space` from parallel neighbours.
7. **[generic] A tie next to the W-end of an unrotated device** (the gate reaches the active edge there) sits at
   `max(active_space, impl_to_ngate_hv + tie_impl_enc, poly_endcap + poly_to_active)`; next to the S/D side of a
   rotated row `active_space` suffices.
8. **[generic] Coda:** fill a short row's free end with the small devices that share its nets; their terminals
   reach the row's lines with short M1 tabs.
9. **[generic] Shareable ties:** tie contacts on a global grid anchored at a common edge; neighbours of the same
   tie type overlap their tie segments; risers of shared nets at the same offset from that edge.
10. **[generic] Pins:** one per net, on the cell edge, pin box + label at its centre, Metal1 or Metal2 only.
11. **[generic] Outlines (implant, thick oxide, well) are polygons following the devices:** union of each source
   layer grown by its enclosure, closed below the merge distance; edges as the deck's angle rules allow.

## Don't

12. **[generic] No well around an NMOS array.** If an isolation well ring is ever needed (say which rule), it is one
    shared structure for the whole NMOS group, merged with the PMOS group's well on the same rail. Separate wells on
    one rail cost `well_space_same` (or must merge) and a ring in its own well costs
    `well_to_nact_hv + 2 well_over_ntie_hv + tie height` per side, against `active_space + tie height` for a
    substrate tie.
13. **[generic] No metal over the channels except dummy straps;** no tracks in a band that a pure row does not need.
14. **[generic] Don't derive a missing device variant by hand.** Combine two exported variants only if the cell is
    separable (x depends on L only, y on W only) and the check in `generator.derive_mos` passes.

## Pitfalls hit

15. **[generic] Narrow M1 under a via near its end:** with `via1_m1_enc` on both long sides and the via at the
    end, three sides fall below `via1_m1_endcap`. Make such tabs `via1 + 2 via1_m1_endcap` wide.
16. **[generic] Byte-reproducible output:** GDS writers stamp the time; switch it off, then two builds give the
    same checksum.
17. **[generic] Labelling a merged L-shaped track by its bounding box** puts the label off the metal (net name
    "?"); decompose into rectangles and label the widest.
18. **[generic] Small devices next to a row:** their poly endcap must keep `poly_to_active` from the next row's
    active, which sets their baseline (not the row baseline).

## Added 2026-10-28 from the matched-pair block (pattern P4)

19. **[generic] Latch-up stack limit:** with one tie segment the farthest N+ active is the far edge of the last
    row: `sum(active height + active_space) + active_space <= lu_ptie`. If the stack is taller, add a second tie
    segment on the far side; never between rows. Report the distance per segment.
20. **[generic] Flip the mirror half:** in an `A B B A` stack, give the retrograde half the inverted current
    direction (S on the top line). Each device then has one finger of each direction, and the two middle rows
    face each other with the same net.
21. **[generic] A row whose source is the tie net** faces the far tie with that line and joins it with one M1
    plate (no track, no via).
22. **[generic] Matched sources into an external network** leave on opposite sides (one joiner each) and come back
    on one lane, meeting at the array's centre line: mirror-image paths, two pins side by side. Put the pins on
    the array's centre line, which differs from the outline's centre when the outline is asymmetric; say so.
23. **[generic] Same active-edge environment for every matched finger:** tie, neighbour rows and the extra row all
    at `active_space` above and below, end dummies at `finger_gap` left and right.
24. **[generic] The one accepted metal-over-channel case besides dummy straps:** a small device's gate contact
    joined to its own gate net's track by a Metal2 stub over its own gate.
25. **[generic] Pitfall: M1 pad around a single via on a single contact** violates the minimum M1 area at
    `track_w` x `track_w`; make it `track_w` x `max(track_w, m1_area / track_w)`.
26. **[generic] A full-width top row leaves no free end:** the coda then widens the outline by its own width;
    budget it when the width is constrained.

## Added 2026-10-28: dummy bias (bg_n4, option 1)

28. **[generic] Dummy at Vgs = 0 when its poly must stay continuous with the row's gate:** strap the dummy's D and
    S to the row's gate net instead of the bulk. With Vgs = 0 the channel is not inverted, so the gate net loses
    the dummy's inverted gate capacitance; only overlap and junction capacitance remain. The dummy keeps its job
    as the edge environment of the matched fingers. Consequence: the dummy straps no longer carry the supply.
    If they were the only metal path between two tie segments (or from a tie to other source terminals), plan a
    separate supply path first. Typically that means freeing a corner by sending the lowest signal tracks down
    risers on the other metal, so the outline does not grow.
