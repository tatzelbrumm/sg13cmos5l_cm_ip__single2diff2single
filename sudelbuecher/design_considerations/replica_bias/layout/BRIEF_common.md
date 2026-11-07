<!--
SPDX-FileCopyrightText: 2026 Christoph Maier
SPDX-License-Identifier: Apache-2.0
-->
# Layout of pad_ref_rb: common brief for the row specialists P and N (cloud session C4, 2026-11-07)

You are a layout specialist for the replica bias cell `pad_ref_rb` of the custom pads (Chipalooza 2026, PDK
ihp-sg13cmos5l). Two specialists work in parallel: **P** (PMOS rows) and **N** (NMOS rows and capacitors). An assembly
agent **F** places and routes your cells afterwards; Christoph Maier reviews. This brief plus `BRIEF_P.md` /
`BRIEF_N.md` (in this folder) are your instructions.

## The one principle

Christoph, 2026-11-07: **"the replica bias must match their layout structures."** pad_ref_rb copies devices of the two
pads (`sg13cmos5l_IOPadSingle2Diff` = S2D, `sg13cmos5l_IOPadDiff2Single` = D2S) so that its voltages track theirs.
Each replica device must therefore look like the pad device it copies: the same PCell finger, orientation, row
neighbors, dummies, well and tie arrangement, gate bar and contact pattern. Where the pad has a row, build yours **with
the code that built the pad's row** (session C3's `build_s2d_p3.py` / `build_s2d_n3.py`), changing only the device
list and nets, not the geometry rules. The drawn S2D pad cell is the binding reference; the D2S pad is the reference
for devices both pads share (unit tails, input tubs).

## Sources of truth (read; do not edit)

Repo `R = /home/user/sg13cmos5l_cm_ip__single2diff2single` (branch `claude/c4-replica-bias`), notes worktree
`S = /home/user/sg13cmos5l_cm_ip__single2diff2single_sudelbuecher/sudelbuecher`.

- **Netlists** (the circuit; every device, net and size): `R/macros/pad_ref_rb/netlist/source/pad_ref_rb.spice`
  (`bias_tree_rb`, `bypass_rb` with parameters `ncm`, `ncr`, `pad_ref_rb`), `R/macros/vcm_rb/netlist/source/vcm_rb.spice`,
  `R/macros/vref_s2d_rb/netlist/source/vref_s2d_rb.spice`. Sheets and renders next to them (`schematic/`).
- **Layout plan and primitives:** `R/macros/pad_ref_rb/layout/primitives/` (`README.md`: which pad row each replica
  copies, the row plan, area estimate; `mapping.tsv`: device → pad structure; `pad_ref_rb_primitives.gds`: unchanged
  `rbsrc_*` copies of the S2D pad's rows and devices, XOR-identical).
- **The pad layouts (references, read only):** `R/macros/sg13cmos5l_IOPadSingle2Diff/layout/klayout/sg13cmos5l_IOPadSingle2Diff.klay.gds`,
  `R/macros/sg13cmos5l_IOPadDiff2Single/layout/klayout/sg13cmos5l_IOPadDiff2Single.klay.gds`; S2D layout report
  `S/design_considerations/pad_buffer_layout/pad_cell_s2d/report.md`.
- **The agents that built the S2D pad's rows (session C3):** `S/sg13cmos5l_IOPadSingle2Diff_build/agents_c3/P/` and `.../N/`
  (`BRIEF.md` with Christoph's binding rules, `report.md`, `out/build_s2d_p3.py` / `out/build_s2d_n3.py`, cells, CDLs, logs),
  and `.../F/` (assembly; `out/src/`). Their predecessors for the D2S pad: `S/sg13cmos5l_IOPadDiff2Single_build/agents_c2/`.
- **Earlier layout knowledge:** `S/design_considerations/pad_buffer_layout/layout_primitives.md`,
  `S/design_considerations/pad_buffer_layout/klayout/` (`pad_buffer_cells.py`, `README.md`),
  `S/design_considerations/pad_buffer_layout/oa_core_pd_v2_2026-10-28/skill/` (layout skill: generic + ihp_sg13cmos5l).
- **Check helpers:** `S/sg13cmos5l_IOPadSingle2Diff_build/agents_c3/F/work/B4/inputs/sym_check.py`, `.../SG13CMOS5L_os_layout_rules.txt`.

## Christoph's layout rules (binding; read the full text in the C3 P / N briefs)

1. Symmetry: rows mirror-symmetric about the line dividing them; the same dummy at both ends of every row; "dummies on
   only one (mismatching) side of each row" is unacceptable.
2. Gate contacts on full-width poly, no necked poly; contact gates with poly; where dummies extend abutted gate poly,
   the gate is contacted by abutment.
3. Dummies: source and drain to the rail, gate net by abutment. PMOS rail vdd, NMOS rail vss.
4. Unmodified PDK PCell transistors; do not shorten contacts or break up an array.
5. No well taps between rows of arrayed transistors (periphery only, LU.a 20 µm); one NWell per rail, no notches;
   taps as rings where space allows; a pair of switches shares its well and tap. Exception: a device with bulk =
   source (the input tubs, the averaging diodes) keeps its own NWell, identical in every copy.
6. Metal stubs no longer than needed; M1 inside a primitive, M2 only where the cell needs it; American English.
7. No floorplan constraints from F: draw each cell compact and symmetric, pins on its edges where they serve its nets.

## Netlist consequences you must report

- **Dummies:** every dummy you draw becomes a netlist device (`XMD<name>`, D = S = B on the rail, gate as drawn) when the
  lead backannotates. List each with its cell, size, terminals.
- **Any change of W, L, ng, finger split or device order** needs a reason and goes in the report.
- **LVS strategy (lead's default, Christoph may revise):** each of your cells must be LVS-clean against its own CDL
  (which you write, from the netlists, plus its dummies). The assembled pad_ref_rb will be compared flat, because your
  rows mix devices of bias_tree_rb, vcm_rb and vref_s2d_rb.

## Checks (each cell)

- DRC: `python3 /foss/pdks/ihp-sg13cmos5l/libs.tech/klayout/tech/drc/run_drc.py --path=<gds> --topcell=<cell> --no_density --mp=4 --run_dir=<dir>`
  (grep the log for "exception"); 0 violations.
- LVS: `python3 /foss/pdks/ihp-sg13cmos5l/libs.tech/klayout/tech/lvs/run_lvs.py --layout=<gds> --netlist=<cdl> --topcell=<cell> --run_dir=<dir> --disable_tap_extraction`.
- Symmetry: `python3 <sym_check.py> <gds> <cell>`.
- A comparison against the pad: for each copied row, a measured statement of what is identical to the pad's row
  (XOR of the shared part, or same generator call) and what differs.
Run each check once and again after each fix; three rounds at most per cell, then report it and leave it.

## Environment and hard rules

- `export PDK_ROOT=/foss/pdks; source /home/user/sg13cmos5l_cm_ip__single2diff2single/.designinit` before any tool.
- Write only in your workspace (`P/` or `N/` next to this file: `work/`, `out/`). Do not edit the repo or the notes
  worktree. No git, no web, no `mcp__*` tools.
- Rule values only from the PDK decks and documents; cite file and rule. Say what is measured and what is reasoning.
- Keep code small. Background commands under 2 h; kill processes by PID, never `pkill -f`.

## Deliverables (in `out/`), then stop

- `<prefix>_cells.gds` (all your cells, one top cell showing them), `<prefix>_cells.cdl`, the build script(s), PNG per
  cell, DRC / LVS / sym_check logs.
- `report.md` (≤ 80 lines): per cell size, area against the pad's counterpart, what is identical to the pad and what
  differs (with reasons), the dummies (for backannotation), open questions for Christoph.
- Reply with a summary of no more than 15 lines and the `out/` file list.
