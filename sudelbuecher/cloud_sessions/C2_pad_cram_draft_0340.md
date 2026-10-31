<!--
SPDX-FileCopyrightText: 2026 Christoph Maier
SPDX-License-Identifier: Apache-2.0
-->
# C2 (draft): what of the class-AB buffer fits into the pad cell, and does the cell line up with IHP's pads

Claude Code cloud session, environment `sg13cmos5l` with the setup script of
`github.com/tatzelbrumm/claude-cloud-config`, as C1. A **cheap feasibility pass**: measuring, packing and
abutment checks with existing cells. No new device geometry, no routing, no PEX, no CACE, no simulation (the
OSDI models are not needed). It runs in parallel with C1 and touches none of C1's files (`oa_core_pd`,
`bg_core_pd`, `bias_sel_pd`).

Read first, and nothing else unless a step below names it: `CLAUDE.md`; this brief;
`sudelbuecher/design_considerations/pad_buffer_layout/layout_primitives.md` §4 (floorplan of the 80 × 180 µm
cell); `sudelbuecher/design_considerations/pad_buffer_layout/klayout/README.md` sections "Cells" and "Fit in the pad cell".

**Cost rules:**
- One session, no background agents, no web searches.
- At most 3 floorplan variants, no parameter sweeps. Each check runs once, plus at most once more after a fix. A step
  that fails twice is recorded and left; go on with the next one.
- Reuse before writing: the `fit_*` shelf packing in `pad_buffer_cells.py`; `agents/A2_oa_core_pd_layout/work/render.py`;
  `agents/A3_oa_nmos_primitives/work/verify.py` (latch-up distances); `agents/A4_oa_pmos_primitives/work/lu_ctx.py`
  (latch-up contexts); the DRC invocation of the macro Makefile's `klayout-drc` target. Scripts of your own are short,
  one per purpose, and stay in the task folder.
- Write `report.md` after each phase, then commit and push, so a time limit loses nothing.

**Git, for this task only (Christoph's permission):** `git fetch origin sudel_buecher && git worktree add -b
claude/c2-pad-cram-sudel ../sudel origin/sudel_buecher`; commits on `claude/c2-pad-cram-sudel` and pushing that
branch. Nothing under `macros/` changes. Never push `main`, `toplevel` or `sudel_buecher`, no tags, no force pushes,
no merges. Outputs: `../sudel/sudelbuecher/design_considerations/pad_buffer_layout/pad_cram_2026-10-31/`; command logs
as in C0, under `../sudel/sudelbuecher/logs/claude/c2-pad-cram/`.

## 0. Tools

`/foss/setup.log` needs `APT_OK`, `PIP_OK`, `PDK_OK` and `SETUP_DONE`, and no `KLAYOUT_DEB_FAILED`.
`TOOLS_OK` and `OSDI_OK` are not needed here; the Makefile's DRC target may want `TOOLS_OK`. Record
`klayout -b -v`, `git -C /foss/pdks/IHP-Open-PDK rev-parse HEAD` and the path of `sg13cmos5l_io.gds` under
`/foss/pdks/ihp-sg13cmos5l/libs.ref/sg13cmos5l_io/`.

## 1. Does the pad cell line up with IHP's pads and fillers?

Cell: `macros/sg13cmos5l_IOPadDiff2Single/layout/klayout/sg13cmos5l_IOPadDiff2Single.klay.gds` as it is
(clamps, diodes and replicas in y 0–84; y 84–178 still empty). This phase does not depend on phase 2.

1. **Outline:** the boundary layer IHP's pad cells use, and the width × height and origin of `sg13cmos5l_IOPadAnalog`,
   `IOPadIOVdd`, `IOPadIOVss` and each `Filler*`. Compare with the pad cell.
2. **Edge profile:** for every layer, the y intervals of the merged shapes that touch the left and the right cell edge
   (within 0.005 µm). Run it on IOPadAnalog, one filler and the pad cell, and print a table of the differences.
   Expected from IHP's cells (measured 2026-10-27): the ring rails on Metal3 / Metal4 / TopMetal1 across the whole
   width, and these silicon bands from edge to edge:
   - NWell with n+, iovdd: y 6–61;
   - p+ ring, iovss: 65–84.4;
   - the p+ plate with Substrate (40/0), iovss: 84.5–140;
   - n+ strip in NWell, iovdd: 148.35–148.65;
   - p+ strip, vss: 156.85–157.15;
   - n+ strip in NWell, vdd: 166.85–167.15.

   A filler gets these potentials only by abutment, so every band must reach both edges of the pad cell and be tied
   there to its rail.
3. **Row:** abut `Filler1000 | IOPadAnalog | pad cell | Filler200 | IOPadIOVdd | pad cell | Filler1000` in one GDS.
   Run IHP's KLayout DRC on it once, with latch-up rules on (`sg13cmos5l_maximal.drc` sets `$latchUpRules` when it
   isn't given). Report violations within 5 µm of an abutment line separately from the rest.
4. **Nets across the row:** extract Metal1 … TopMetal1 with the vias (klayout.db `LayoutToNetlist`). Each ring rail
   and each band must be one net through all seven cells.

## 2. What fits into y 84–178 (94 µm × 80 µm)

The packing so far, of the drawn but not yet compacted cells in `pad_buffer_cells.gds` (2 µm gaps):
- the d2s front end packs to 94.2 µm;
- with CMA / CMB, 98.8 µm;
- the bias tree with the two reference cores, 131.1 µm.

The cores go to slot 7 and are not part of this task.

1. **Compacted size per cell, estimated without drawing.** Apply the rules that compacted oa_core_pd from 3856 to
   2355 µm²: `agents/A3_oa_nmos_primitives/out/skill/generic/rules.md` and `.../ihp_sg13cmos5l/rules.md`; read these
   two, not the rest of `skill/`. Christoph's rules from 2026-10-28:
   - no substrate taps between rows of arrayed transistors;
   - one NWell per rail, not separate wells;
   - a tap ring is optional and needn't be rectangular;
   - NWell polygonal where the rules allow;
   - narrow dummies;
   - the layout drives the design (note any backannotation it would imply).

   Give each estimate with the rule it uses.
2. **Fill in priority order:**
   1. the d2s front end with the class-AB groups and power-down (must);
   2. CMA / CMB;
   3. a bias-tree leg (`bias_tree_n`, `bias_tree_p`, `bias_tree_sw`);
   4. the enable / level shifting the pad needs (area from the existing cell, or from the schematic's device list
      if no cell exists).

   Respect the constraints of `layout_primitives.md` §4:
   - M1 / M2 routing under the ring rails, M3 only in the gaps at y 119–126 and 134–140;
   - double guard rings between the output devices and the circuitry (§7.2.1 of the layout rules);
   - LU.a, 20 µm.

   Leave interconnect channels and state their width.
3. **Floorplan GDS:** the existing cells as instances where they fit at their present size, compacted estimates as
   boxes on a marker layer, on top of the pad cell; one PNG.
4. **Table:** each block marked fits as drawn / fits only compacted / goes to slot 7, with µm², height, and which zone
   it sits in.

## 3. Not in this task

Drawing the compacted cells, routing, LVS of the full pad, PEX, CACE. That is a later task, using the generators
of A2–A4 (`agents/*/out*/`, `agents/*/work*/`), after Christoph has seen this report.
