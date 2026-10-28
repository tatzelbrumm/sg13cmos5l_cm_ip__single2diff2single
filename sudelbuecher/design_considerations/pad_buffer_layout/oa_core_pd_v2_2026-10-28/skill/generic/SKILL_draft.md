---
name: analog-block-assembly
description: Process-agnostic skill for assembling a compact analog block from finished layout primitives (arrays, small cells) - floorplan as a placement grammar ("score"), one merged well per supply, tie segments only where latch-up needs them, rails and edge pins, two-metal grid routing, DRC / LVS / latch-up checks, and layout-driven backannotation of the schematic. Every process value comes from a process adapter file; this folder holds no process names or numbers.
---

# Analog block assembly from primitives (process-agnostic)

## When to use
- You have primitive cells (device arrays, small device groups) with pins on their edges, a schematic / netlist of
  the block, and must deliver a compact block with supply rails along two edges, signal ports on the block edge,
  and only the two lowest routing metals used (the upper metals stay free for the next level).
- You want the layout to drive the design: finger splits, series splits, dummies follow the layout, and the
  schematic is backannotated from it.
- Not for drawing the primitives themselves (array patterns, rotated devices): that is a different skill; this one
  takes them as given and may only request or make small edits (well to the edge, pin moved, tie removed).

## Files (relative)
- `generator.py`: placement grammar -> placement -> ties / merged wells -> router -> rails / edge pins -> GDS,
  report, latch-up check, `compose_reference()` (LVS reference from the primitives' own netlists), `selftest()`.
- `backannotate.py`: layout fingers -> sheet devices (parallel / series / dummies), edited sheet copy, subckt text,
  device-change list, xschem netlisting of the new sheet.
- `area_audit.py`: where the block's area goes (bands, ties, wells, free area, utilization).
- `render_block.py`: pictures from the GDS (same scale side by side, annotations); `score_picture.py`: placement
  score picture without process layers.
- `adapter_template.py`: every field a process adapter must provide, with where to find it.
- `patterns.md`: the floorplan patterns in score form; `rules.md`: do / don't with pitfalls.
- `pictures/score_v1.png`, `pictures/score_compact.png`: an example before / after as scores; layer-level pictures
  of the same example are process specific: see `../ihp_sg13cmos5l/pictures/`.

## Procedure
1. **Inventory** every primitive: bbox, which edges carry which pins (layer, net), which edges are well / oxide
   edges, where its ties are (or that it has none), its internal net names (unlabelled internal nodes are normal).
   Run `area_audit.py` on the old block if there is one: the bands (bbox minus device core) and the free area are
   the budget you can win.
2. **Group by bulk**: all devices whose bulk is the same supply go into ONE well; the cells must have their well
   drawn to the cell edge and no own ring. One tie-diffusion strip per substrate group, shared by abutting cells.
3. **Write the score** (placement grammar, see `patterns.md`): stack rows so that row widths are nearly equal;
   orient each cell (P / R / I / RI) so that its pins face the cell they connect to and so that no foreign pin lands
   on a rail or a neighbour's supply metal; put the matched array where no foreign net needs to cross it.
   Try two or three scores; they cost seconds to place.
4. **Gaps**: `gap=auto` lets the DRC callback find the smallest clean gap (with the well / oxide merge applied in
   the trial, and a label check for shorts); use a fixed negative gap only for intended sharing (a ring or tie
   under a rail).
5. **Ties**: put tie stripes where the latch-up distance needs them: under the supply rail (free parts only) and
   explicit segments where the array's designer says (in its margins). Check with `Block.latchup()`; never add a tie
   between the rows of an arrayed device block; report the numbers if the array is too large.
6. **Route** on the two lowest metals; ports on one edge if possible; keep-outs over matched arrays (their own nets
   allowed). Read the report: wire length per net, layers drawn.
7. **Check**: DRC of the block and of every changed primitive; LVS against a reference composed from the
   primitives' own netlists (`compose_reference`, cell-internal bulk tied to the supply that the merged well
   carries); latch-up; reproducibility (build twice, same bytes).
8. **Backannotate**: `backannotate.py` maps the extracted fingers to the sheet devices by terminals (topology comes
   from the sheet, sizes from the layout; any topology difference is an error), writes the sheet copy, the subckt
   text and the change list with the ratios that set the circuit; netlist the new sheet and run LVS of the layout
   against it (closing check).
9. **Pictures**: v1 and the new block at the same scale; one annotated picture of the rule behind each saving.

## Pattern notation (short; full form in `patterns.md`)
- `V` = voices stacked top to bottom, `H` = time left to right, `cell <inst> o=<T>`, `rail <net> h= [tap=n|p]`,
  `space`, `FREE` (absolute positions, e.g. two cells that share a tie by exact overlap).
- Transforms: P = R0 (prime), R = M90 (retrograde, x reversed), I = M0 (inversion, y reversed), RI = R180
  (retrograde inversion = point symmetry), plus R90 / R270 (rotation: a row becomes a column).

## Pitfalls (details and fixes in `rules.md`)
- A pin box alone is not the terminal: the router must see the cell's whole metal of that net.
- Gap search by DRC alone does not see shorts: touching metal of two nets merges silently.
- A tie or well added after placement can widen the block beyond the rails.
- Tracks at the minimum pitch cannot be reached by a uniform grid: add the pin centre lines to the grid.
- The heuristic of a grid search must be a true lower bound, or the router takes detours.
- Ports are alternatives (any edge node), not connected terminals.

## Porting to another process
Copy `adapter_template.py` to `<process>.py` and fill every field from the new PDK:
| adapter field | where to find it | how to verify |
|---|---|---|
| `LAYERS` (diff, poly, cont, implants, well, thick oxide, metal 1/2 + pin + text, via) | layer map / tech file of the PDK, DRC deck layer definitions | self-test GDS opens with the right layer names |
| `RULE_KEYS` / `rules()` (metal width / space / wide space / area, via size / space / enclosure, contact, diff, well, implant, thick oxide, latch-up, grid) | DRC deck (rule text and value) | `generator.selftest()` output passes the PDK's DRC |
| `WELL_OUTLINE` (allowed angles) | the deck's angle / off-grid checks | polygonal well passes DRC |
| `TAPS`, `THICK`, `MERGE_LAYERS` (tie construction, oxide merge) | deck rules for ties, wells, thick oxide; the PDK's tie PCells | self-test ties pass DRC and LVS (tie net = rail net) |
| `derive()` (n / p diffusion, device S/D, ties) | the deck's layer derivations (implant logic) | `Block.latchup()` agrees with the deck's latch-up rule on a test cell |
| `LU_STEP`, latch-up distances | latch-up rules and how the deck measures them | a cell with one tie at the limit distance passes, one beyond fails |
| device recognition for LVS | the LVS deck (recognition layers, terminals, bulk) | the PDK's own LVS on the self-test and on one primitive |
| PEX / model facts (which layers carry R / C that matter, characterized W / L / nf ranges) | PEX rules, model cards | stated in the adapter with source; affects score choices (sensitive nets short) |
Then run `generator.selftest(adapter, "selftest.gds", drc=...)` and the PDK's own DRC and LVS on it, and on one
assembled block. Process-specific tools (a Python DRC subset, an extractor) belong to the process folder, e.g. in
IHP sg13cmos5l: `../ihp_sg13cmos5l/tools/` (see `../ihp_sg13cmos5l/SKILL_draft.md`).
