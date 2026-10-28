# Brief N2: the bandgap's NMOS primitives, compact (IHP sg13cmos5l), 2026-10-28 04:45

Same workspace, hard rules and check tools as your `BRIEF.md`. New read-only inputs: `inputs_bg/`, which holds
`bg_core_pd.sch`, its xschem netlist `bg_core_pd_xschem.spice`, the READMEs, and the standalone GDS of the bg
primitives. The library cells are in `inputs/pad_buffer_cells.gds`.

## The user (04:25 and 04:28, verbatim)

"There should be lessons learned from Oguey Aebischer for first modifying layout primitives for the bandgap reference,
then compacting the overall bandgap core." — "It might make sense for Agent 2 to recruit help from Agents 3 and 4."

So, as for oa_core_pd:
- you do the NMOS primitives, A4 the PMOS ones;
- A2 (the assembler) does the pnp and resistor arrays and then compacts `bg_core_pd` from all the cells;
- A2 may modify your cells (as copies) if the assembly gets smaller.

All of the user's layout rules from your first brief still hold, and so does your own OA experience (your `out/skill/`).

## Your cells

The NMOS devices of `bg_core_pd`, all `sg13_hv_nmos`, bulk = vss (from the sheet's netlist):

```
XNA  g   g  ea  vss  W=20u L=4u ng=1      (diode; matched to NB)
XNB  vpc g  eb  vss  W=20u L=4u ng=1      (matched pair NA / NB, sources ea / eb into the pnp / resistor network)
XMS2 ks  g  vss vss  W=10u L=1u
XMS3 vpc ks vss vss  W=0.5u L=2u
XSKS ks  en_3v3_b vss vss W=1u L=0.45u
```

Library: `bg_nab` (NA / NB, 48.87 × 8.21 µm) and `bg_misc_n` (MS2, MS3, SKS, 7.23 × 12.61 µm).

1. **One compact NMOS block** (e.g. `bg_n4`), built like your `oa_n10`:
   - rotated rows;
   - NA / NB interdigitated or common-centroid, matched; the sources ea / eb are separate nets, so say how you keep
     their routing symmetric;
   - MS2, MS3 and SKS at the ends or wherever they cost least;
   - narrow end dummies;
   - one periphery p+ tie, no ring, no NWell, no tap between rows.

   Re-splitting is allowed (e.g. NA / NB as 2 × 10/4 or 4 × 5/4 each) if it packs better. Total W and L stay;
   report the backannotation.
2. Pins: Metal1 / Metal2, on the edge(s) where the assembler can reach them. ea / eb face the pnp / resistor side; g
   and vpc face the PMOS side. State your assumption of where those sides are.
3. Checks: DRC 0 with `inputs/tools/oa_core_pd_drc.py`, LVS match, a render, and LU checked with the periphery tie.

## Deliverables (`out_bg/`)

- `bg_n_cells.gds` / `.cdl`, `build_bg_n.py`, and the logs.
- Before / after pictures.
- A report under ~80 lines covering:
  - sizes before / after;
  - the finger map;
  - tie and LU numbers;
  - the backannotation list;
  - pins with coordinates;
  - lessons for the skill.
- Your `out/skill/` extended (generic / IHP, tagged), not replaced.
- Reply with a five-line summary and the file list with sha256 (first 12 hex).
