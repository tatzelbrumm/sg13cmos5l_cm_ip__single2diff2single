<!--
SPDX-FileCopyrightText: 2026 Christoph Maier
SPDX-License-Identifier: Apache-2.0
-->
# Brief F: floorplan and compaction of the `sg13cmos5l_IOPadSingle2Diff` buffer in the pad template (C3, 2026-11-03)

You are agent F, the floorplan and assembly agent. You build the s2d buffer block **bottom-up** from the compact
primitives of agents P and N (checked by the lead) and place it in the cleaned-out pad template. Then you compact the
whole arrangement further (Christoph: "have the layout builder further compact the entire layout"). This brief covers
**stage A only**: placement and compaction without routing. Christoph reviews your placement picture before any
routing (stage B).

**Workspace:** yours only, `$WS` (`inputs/` read-only, `work/`, `out/`). Write nowhere else.

## Inputs (`$WS/inputs/`)

- `template/`: the pad template, version 4 (`sg13cmos5l_IOPadSingle2Diff_template.gds`, top cell
  `sg13cmos5l_IOPadSingle2Diff`, its `README.md` and `build_template.py`).
  - Protection at the pad side, y 5.38–41.6: DN | DP, with CN | CP on top.
  - rppd gate ties in the gap between the columns.
  - iovdd bar above CP and two M2 risers (x 42.6–45.2, 75.5–78.4) up to y 72.55.
  - The NWell legs and the edge stubs.
  - The free region and its keep-outs are listed in `fit/fit_s2d.py` (`REGION`, `OBST`).
- `fit/`: the tentative packing Christoph chose ("Go with A"), `fit_A.gds` / `.png`, `fit.md`.
  - It is a bounding-box packer result with the uncompacted library cells, 2 µm apart: **a proof that everything fits,
    not a floorplan.** It ignores signal flow; for example, the input tubs sit far from their tails.
- `P/`, `N/`: the checked primitives (`s2d_p3_cells.gds` / `.cdl`, `s2d_n3_cells.gds` / `.cdl`), the agents' reports
  and PNGs, and the lead's check results.
- `circuit/`: `s2d_mpdda.spice`, `s2d_pd.spice`, `units.spice`, `bias_tree_noab_pd.spice`, `bias_ref_pd.spice`, the
  sheets, and the pad's partitioned port list (below).
- `C2_F2/`: your C2 predecessor's floorplan and assembly of the d2s pad: `report_stageB.md`, `out/src/` (the
  assembly and router code), `out/cells/d2s_block.gds`, placement pictures. **Reuse its code and approach.** Its
  final cell was accepted after Christoph's reviews.
- `C2_decisions.md`, `review/` (Christoph's reviews of C2's primitives), `layout_primitives.md`, `log.md`,
  `sym_check.py`, `row_check.py`, `SG13CMOS5L_os_layout_rules.txt`.

## What goes into the cell (the partition, phase 1 report §1.2)

- `xa` = `s2d_mpdda_pd`: all primitives of P and N, including the load capacitors `s2d_cload` (decision 2: they fit).
- `xt` = `bias_tree_noab_pd`: P's and N's tree cells. Its four bias diodes sit in the tails (BP), the sinks (BN) and
  the cascodes (BPC, BNC).
- Out of the cell, to the slot: `xg` (`bias_gen_pd`) and `xc` (`en_ctrl_3v3`).
- Ports: `iovdd iovss vdd vss pad outp outn vcm vref iref en_3v3 en_3v3_b`.
  - Core-side pins `outp outn vcm vref iref en_3v3 en_3v3_b` go on Metal2 at the top edge (y 180).
  - The buffer input is the template's `pad` pin (M2, x 20.40–21.02, top at y 31.18, just above CN). The secondary
    protection is left out for now.
  - In the pad, the buffer's `vdd` / `vss` are iovdd / iovss.

## Rules (binding)

1. **Bottom-up** (Christoph, C2 17:55): "F should adapt its floorplan to compacted layout primitives (maybe put in
   context), not top down with an unrealistic floorplan cast in stone." Nothing goes back to P / N as a constraint.
2. **"adapt the floorplan for compact connection of the layout primitives, not the other way around"** (C2, 14:25).
   Group by signal flow:
   - each tail under its tub's column (`layout_primitives.md` §2);
   - the R block beside the tubs / tails;
   - sinks and cascodes next to the fold nodes x / y / xc / yc;
   - loads and their cascodes next to the outputs;
   - the bias tree next to the arrays it feeds;
   - short `sa_U` / `sb_U` wires of equal length.
3. **You may change your copies of P's and N's cells** to compact further (`<cell>_f`, each DRC clean and LVS-matched
   on its own; list every change). Symmetry and gate contacts stay as P / N drew them:
   - rows mirror-symmetric about the line dividing them;
   - the same dummy at both ends of every row;
   - no necked gate poly;
   - dummies' source and drain on the rails, gate by abutment (C3 decision 3).
   Check every changed copy with `sym_check.py`.
4. **Christoph's rules** of 2026-10-28 and of his C2 reviews (`review/`, `C2_decisions.md` 14:25, 15:50):
   - no taps between rows of arrayed transistors;
   - one NWell per rail (the input tubs keep their own wells) and no well notches;
   - taps as rings where space allows;
   - switches with the cells they serve;
   - contact gates with poly;
   - American English.
5. **The protection is fixed.** Don't touch the template's cells and wiring (clamps, diodes, rppds, `esd_wiring`,
   edge stubs, legs).
   - Keep your cells ≥ 1.5 µm from the protection's outer rings and out of the risers' x ranges up to y 73.05.
   - Mind the latch-up rules (LU.a / LU.b 20 µm). IOPadAnalog separated its ESD zone with a p+ plate, and the
     template has none: state whether your arrangement needs an isolator between the zone and the buffer, and
     reserve room for it if so.
6. **Routing room.**
   - M3 / M4 / TM1 are the IO ring's rails. M3 is free only at y 119–126 and 134–140.
   - Route in M1 / M2. Reserve wiring channels in the placement, and say how wide and why.
   - Tap the tail source bus and the sink source bus each at one point (§6).
7. **Rule values only from the PDK decks and documents**, cited with file and rule name. Keep code small.
8. **Edge contract:** the template's edge intervals stay as they are; `row_check.py` must still pass (26 / 26 nets,
   edges the same as IOPadAnalog's).

## Stage A deliverables (`out/`), then stop

- `placement_A.gds`: the template plus your placed cells and reworked copies, top cell `sg13cmos5l_IOPadSingle2Diff`.
- `out/previews/placement_A.png` (cells named, the rails, M3 gaps and reserved channels marked) and close-ups of the
  densest regions.
- Every changed cell `<cell>_f` in `out/cells/` (`.gds` + `.cdl`), with its DRC / LVS / sym_check logs.
- Run DRC on `placement_A.gds`: IHP `run_drc.py --no_density` (grep for "exception") and `sg13cmos5l_maximal.drc
  -rd latchUpRules=true`. Run `row_check.py` on it.
- `out/stage_A_note.md` (under ~80 lines):
  - area per block (as delivered, and after your compaction);
  - the bounding box of the whole block, and the free area left;
  - the wiring channels;
  - the isolator question of rule 5;
  - every change to P's / N's cells;
  - what you expect stage B to need.
- Reply with a summary of no more than 15 lines and the `out/` file list with sha256 (first 12 hex), then stop.

## Checks

Run each check once, and again after each fix. Three rounds at most per cell, then report it and leave it.

- **DRC:** `python3 /foss/pdks/ihp-sg13cmos5l/libs.tech/klayout/tech/drc/run_drc.py --path=<gds> --topcell=<cell>
  --no_density --mp=4 --run_dir=<dir>`.
- **LVS:** `.../lvs/run_lvs.py --layout=<gds> --netlist=<cdl> --topcell=<cell> --run_dir=<dir>
  --disable_tap_extraction` (add `--run_mode=deep` for hierarchical cells).
- **Symmetry:** `python3 inputs/sym_check.py <gds> <cell>`.

## Hard rules

- No git, no web, no `mcp__*` tools.
- Say which statements are measured facts and which are reasoning. Times: `TZ=Europe/Berlin date`.
- Keep each background command under 2 h. Kill processes by PID, never with `pkill -f`.
