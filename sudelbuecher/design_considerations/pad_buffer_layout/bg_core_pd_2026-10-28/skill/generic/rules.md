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

## Blocks with a bipolar core and a resistor array (bg_core_pd, 2026-10-28; all [generic])
Same numbering continued (G25 on, P19 on, so the numbers stay unique next to A3's / A4's primitive skills, which use
G15-G24). The IHP values are in `../ihp_sg13cmos5l/rules.md` (I32 on).

| # | rule | forced by (rule type) |
|---|---|---|
| G25 | Primitives first, block second: revise every primitive (no ring, well to the edge, pins on the edge facing the partner, ties only where latch-up needs them), then floorplan. The bandgap block's first placement was 2413 um2 for 2044 um2 of primitives (85 %), all nets routed, because the primitives were already compact. | (order of work) |
| G26 | "Placed only" in a cell list means: devices present, no wiring, no pins. Find out by extraction (floating terminals) before planning; the wiring is then yours, and so are its pin edges. | (LVS) |
| G27 | Bipolar array with base = collector (diode-connected to one supply): fill the lower metal between each base ring and its collector ring; the array becomes one supply plane, its collector rings are the substrate ties. Nothing added around the device's own guard structure. | latch-up / substrate tie rules (the collector ring is the tie) |
| G28 | Common-centroid bipolar array (unit in the centre, n units around it): the outer emitters on a frame of the upper metal (top row, bottom row, one side column, the other side column only up to the middle row); the centre emitter leaves through the gap. One exit per net, both on the same edge; the frame's rows are extra landing points for the neighbour. | (matching practice; one metal for two nets) |
| G29 | Resistor array of identical segments: each resistor is a chain of its segments (left to right), linked alternately at the two head rows; links on the lower metal along levels, short upper-metal stubs from the heads; links share a level where they do not overlap (interval colouring). The segments, pitch and interleave stay as the designer drew them. | metal space; (matching practice) |
| G30 | Chain parity sets the pin edge: an even number of segments puts both ends on the same head row, an odd number on opposite rows. Choose each chain's starting row (and direction) so the terminals that go to the same neighbour come out at the same end of the array (here the two NMOS-side nets at one end, the bipolar-side net and the supply at the other). Free inside the array. | (floorplan) |
| G31 | Floorplan of a bipolar core: the tallest column is the stack resistor array over bipolar array; the MOS column next to it holds the NMOS block and, hanging from the PMOS row's well, the small PMOS cell (startup chain); the PMOS mirror row over both sets the width. Compare the two columns' heights before routing (here 31.86 vs 30.14 um: the slack became a routing channel). | (floorplan) |
| G32 | A PMOS cell hanging below the PMOS row (wells merged by the closing) is farther than the latch-up distance from the rail tie: give it a tie segment in the upper cell's bottom margin over its own width, not a ring. | latch-up distance; tie well enclosure |
| G33 | The sensitive nets of the core (here the two emitter nodes and the scaled emitter node) use the strip left beside the narrower of the stacked arrays; enables and the output go elsewhere (top rail band, the channel between MOS cells). Whole-cell keep-outs that allow the cell's own nets let those nets land on the cell's internal lanes, which gave the shortest connections. | (coupling practice) |
| G34 | Backannotate resistor chains as chains (each segment its own device: in the models each segment has its own head / contact resistance) and bipolar counts as m; dummy segments (both ends on one net) as a separate group. | (models) |

| # | symptom | cause | fix |
|---|---|---|---|
| P19 | LVS: two resistors merged into one across a labelled net | series combination ran before the circuit pins existed | combine devices only after the pins are made (labelled nets are pins) |
| P20 | LVS mismatch on resistors with equal geometry | float resistance values compared exactly | parameter tolerance (relative 1e-6) for R, and AE / NE for bipolars |
| P21 | all bipolar wiring on one row, wells too close, two emitter nets shorted | the array's step vectors taken in the wrong order (a = y step, b = x step in that cell) | derive the x / y steps from the vectors, not from their order |
| P22 | metal width violation 0.035 um at a landing | a wire end stopped 0.075 um short of a pad corner; the same-net closing filled the gap only over the 0.035 um overlap | neck repair after the closing: widen every new neck to the width rule (box centred on it) where the other nets' spacing allows |
| P23 | metal area violation at an edge port | the port pin was boxed in between a wire and the block edge, so it could not grow along its long side | minimum-area fix tries the short side too |
| P24 | an enable could not reach its port | the two analog nets it had to cross took every node of the edge range first | route the crossing net first (explicit order) and give its port an edge range in a channel; the analog nets hop under it |
| P25 | area audit: absurd "core" numbers for resistor / bipolar cells | core = bbox of MOS gates only; an empty region's bbox | adapter hook `device_core()`: resistor bodies and bipolar devices count as device core |
