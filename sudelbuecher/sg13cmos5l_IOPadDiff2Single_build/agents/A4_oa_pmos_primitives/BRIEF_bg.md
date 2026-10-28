# Brief P2: the bandgap's PMOS primitives, compact (IHP sg13cmos5l), 2026-10-28 04:45

Same workspace, hard rules and check tools as your `BRIEF.md`. New read-only inputs: `inputs_bg/`, which holds
`bg_core_pd.sch`, its xschem netlist `bg_core_pd_xschem.spice`, the READMEs, and the standalone GDS of the bg
primitives. The library cells are in `inputs/pad_buffer_cells.gds`.

## The user (04:25 and 04:28, verbatim)

"There should be lessons learned from Oguey Aebischer for first modifying layout primitives for the bandgap reference,
then compacting the overall bandgap core." — "It might make sense for Agent 2 to recruit help from Agents 3 and 4."

So, as for oa_core_pd:
- you do the PMOS primitives, A3 the NMOS ones;
- A2 (the assembler) does the pnp and resistor arrays and then compacts `bg_core_pd` from all the cells;
- A2 may modify your cells (as copies) if the assembly gets smaller.

All of the user's layout rules from your first brief still hold, and so does your own OA experience (your `out/skill/`).

## Your cells

The PMOS devices of `bg_core_pd`, all `sg13_hv_pmos`, bulk = vdd (from the sheet's netlist):

```
XPB  vpg vpg vdd vdd  W=40u L=1u ng=4   (mirror diode)        XPBC vpc vpc vpg vdd W=40u L=1u ng=4  (its cascode, diode)
XPA  ca  vpg vdd vdd  W=40u L=1u ng=4                          XPAC g   vpc ca  vdd W=40u L=1u ng=4
XPO  co  vpg vdd vdd  W=80u L=1u ng=8   (output, 2x)           XPOC iout vpc co vdd W=80u L=1u ng=8
XMS1 ks  en_3v3_b vdd vdd W=0.5u L=100u                       XSVPG vpg en_3v3 vdd vdd W=1u L=0.45u
```

Library: `bg_pmir_pcas` (PB, PBC, PA, PAC, PO, POC, 38.59 × 27.60 µm) and `bg_misc_p` (MS1 chain and SVPG,
12.04 × 17.14 µm).

1. **`bg_pmir_pcas` compact** (e.g. `bg_pmir_pcas_c`):
   - 32 fingers of 10/1: PB 4, PA 4, PO 8 for the mirror, the same counts for the cascodes;
   - rotated rows;
   - the mirror (PB : PA : PO = 1 : 1 : 2) common-centroid / point-symmetric, XOR-checked against its image as for
     oa_pmir_c; the cascodes in their own rows, matched the same way;
   - narrow dummies;
   - tap-less, NWell (= ThickGateOx) to the cell edge so it merges with the block's vdd well;
   - LU checked against the parent taps you assume.
2. **`bg_misc_p` successor**: MS1 (0.5/100) as a series chain like `oa_ms1` (8 × 0.5/12.5 or what packs best), and
   SVPG on its own like `oa_svpg`. Tap-less, NWell to the edge.
3. Pins: Metal1 / Metal2, on the edge(s) where the assembler can reach them:
   - vpg / vpc / ca / co face the NMOS side;
   - iout faces the port edge.
   State your assumption of where those sides are.
4. Checks: DRC 0 apart from the intended LU.a of tap-less cells, LVS match, and a render.

## Deliverables (`out_bg/`)

- `bg_p_cells.gds` / `.cdl`, `build_bg_p.py`, and the logs.
- Before / after pictures.
- A report under ~80 lines covering:
  - sizes before / after;
  - the device map and the symmetry XOR;
  - the LU assumption;
  - the backannotation list;
  - pins with coordinates;
  - lessons for the skill.
- Your `out/skill/` extended (generic / IHP, tagged), not replaced.
- Reply with a five-line summary and the file list with sha256 (first 12 hex).
