# Block assembly: rules followed and pitfalls hit (all [generic])

Each rule names the deck rule *type* that forces it; the values of one process are in its folder, e.g. in IHP
sg13cmos5l: `../ihp_sg13cmos5l/rules.md` (same numbering, prefix I).

## Do / don't
| # | rule | forced by (rule type) |
|---|---|---|
| G1 | One well per supply net: cells with the same bulk abut / overlap their wells; gaps below the well space are closed. Never a second well on the same net next to the first. | well space, same net; well enclosure of the device diffusion |
| G2 | No ring by default. Ties as stripes or segments where the latch-up distance needs them; their outline follows the cells (rectilinear, or whatever angles the deck allows for the well). | latch-up distance (diffusion to tie); well angle rules |
| G3 | Never a tie between the rows of one arrayed device block; ties at the array's periphery only. If the array is too large for the latch-up distance, report the number instead. | latch-up distance |
| G4 | Ties under the supply rail cost no area: diffusion + one contact row in the rail band, the rail metal covers the contacts. Inside thick oxide the tie needs the thick-oxide well enclosure; outside it, the thick-oxide-to-diffusion space. | tie well enclosure (thin / thick oxide), thick oxide space to diffusion |
| G5 | One substrate tie strip shared by two abutting NMOS cells (exact overlap, same contact grid). | latch-up distance; diffusion / implant rules of the tie |
| G6 | Voices of equal length: stack rows whose widths are within a few percent; the block is the widest voice. | (floorplan) |
| G7 | Orient for the edges: pin edge toward the partner cell, supply edge toward the rail; check that no foreign pin touches a rail or a neighbour's supply metal (gap trial with a label check). | metal space; (shorts) |
| G8 | The matched array gets a keep-out on the routing metals for foreign nets; its own nets may cross it to reach its pins. | (matching practice) |
| G9 | Ports on one block edge, next to their drivers; rails full width, two edges. | (convention for abutment) |
| G10 | Two routing metals only; the upper metals stay free for the next level. Router wire = via pad (via + end enclosure on both sides); pitch = (wire + widest space) / 2, so that merged same-net wires keep the wide-metal space. | metal width / space / wide space; via size / enclosure |
| G11 | Spacing next to cell metal: the wide-metal value only next to the wide parts (as the deck checks it), the normal value elsewhere. | wide-metal space (width threshold, parallel run) |
| G12 | Backannotate from the layout: sizes from the layout, topology from the sheet; a topology difference is an error in the layout, not a sheet edit. | (LVS) |
| G13 | LVS reference for the block = the primitives' own netlists composed with the block's connections (independent of the block's extraction); then also LVS against the backannotated sheet. | (LVS) |
| G14 | Builds are reproducible: no timestamps in the GDS, fixed router parameters in the config; check by building twice. | (review) |

## Pitfalls hit, in the order they appeared (what failed first, and why)
| # | symptom | cause | fix |
|---|---|---|---|
| P1 | router: "no free access node" on most pins | terminal = pin box only; same-net metal reached through the cell's vias counted as obstacle | terminal = the cell's whole net metal (flat connectivity extraction per cell) |
| P2 | false "short" between two pins of one cell | hierarchical extraction: net probe returned sub-circuit nets with colliding cluster ids | extract a flattened copy of the cell |
| P3 | pins on minimum-pitch tracks unreachable | uniform grid never on the track centre; a pad off-centre violates the space to the neighbour track | non-uniform grid: regular lines + every pin's centre lines; geometric (not index) blocking |
| P4 | every continuation off a track end blocked | a "sliver band" rule blocked nodes near own metal | drop it; fill same-net gaps below the space rule after routing (closing) |
| P5 | 20 um detours for 2 um connections | heuristic from sampled targets overestimates | exact L1 distance transform from all targets (admissible) |
| P6 | a port net routed first blocks the short nets | its length estimate ignored the way to the edge | add the distance to the port edge; route nets with scarce access first |
| P7 | short between a port net and the supply rail | via-landing nodes kept in one global set: another net's rail counted as a landing | per-net landing sets |
| P8 | open on a port net | the whole edge (alternatives) joined the tree; the next branch started elsewhere | for a port, only the reached node joins the tree |
| P9 | metal width violations at landings | a wire square overlapping cell metal by a sliver leaves a diagonal neck | landing patch (bbox of square + touched metal) if it keeps the wide space; close notches AFTER the patches |
| P10 | via-to-via space violation | two branches landing on one narrow pin with vias 0.025 apart | merge same-net vias closer than via + space, bridge the pads |
| P11 | tie contacts at 0.175 instead of the contact space | each contact snapped to the grid separately | snap the start once, step by the (on-grid) pitch |
| P12 | a tie stripe over the whole rail although a cell blocks it | bbox of an L-shaped free region | opening across the stripe, then decomposition into boxes |
| P13 | shorts that DRC does not flag | touching metal of two nets merges silently in the gap search | label check (two net names on one merged polygon) per trial and on the full placement |
| P14 | block wider than its rails | tie wells added after placement stick out of the block | stretch the rails to the final width (better: budget the tie in the placement) |
| P15 | metal area violation at an edge port | the edge node reached by a via: the piece is one pad | grow pieces below the minimum area along their long side where the space allows |
| P16 | keep-out over the array made its own pins unreachable | keep-out applied to all nets | keep-out with an allow list (the array's own nets) |
| P17 | backannotation: "sheet device not found" | an internal node of a primitive has no label in the layout | map unlabelled layout nets to the sheet nets no label carries (all assignments tried, only an error-free one accepted) |
| P18 | auto gap = 0 everywhere looked suspicious | (it was right for cells with rings at their edges) | test the gap search on a pair that must need a gap (PMOS well next to NMOS: well-to-n-diffusion space) |

## Lessons for the next block (generic form; the IHP instance with numbers is in ../ihp_sg13cmos5l/rules.md)
- The area went: per-cell rings and the bands they enclose (largest), empty bays between islands, inner tie rows,
  full-size dummies, separate wells of one supply. Fix them in the primitives first, then the floorplan.
- Ask the primitive designers for: well to the cell edge, no ring, pins on the edge facing the partner, the tie
  segments latch-up needs (positions), and the pin pitch (minimum-pitch tracks need on-line access).
- Assembly-driven edits worth making: a well-merging copy of a ringed cell (ring removed, well to the edge); turn
  a small cell so its narrow pin faces open space.
