<!--
SPDX-FileCopyrightText: 2026 Christoph Maier
SPDX-License-Identifier: Apache-2.0
-->
# Brief BA: backannotation of the drawn `sg13cmos5l_IOPadSingle2Diff` pad cell (C3, 2026-11-04)

Workspace (yours only): `/tmp/claude-0/-home-user-sg13cmos5l-cm-ip--single2diff2single/9625f5bb-27cd-530e-a9cf-d1aa15a8223d/scratchpad/agents/BA/`
(below: `BA/`).
- `work/` is a full copy of the design repository (branch `claude/c3-s2d-pad-layout`, fast-forwarded to `toplevel`, so
  it holds C2's finished d2s pad). The new layout is already in
  `macros/sg13cmos5l_IOPadSingle2Diff/layout/klayout/sg13cmos5l_IOPadSingle2Diff.klay.gds`. You edit `work/`.
- `inputs/` is read-only. `out/` holds your notes, checks and renders.
- The lead copies your changed files into the real repository after checking them. No git commands.
- American English in everything you write.

## Goal

The xschem sheets, the symbol and the source netlists of `sg13cmos5l_IOPadSingle2Diff` describe exactly the drawn
cell: every drawn device, dummies included, and its ports. Everything that instantiates the pad is updated so that
it keeps working with the old function.

This is the same job C2's agent BA did for the d2s pad. Its brief is `inputs/C2_BA_BRIEF.md`, its report
`inputs/C2_BA/report.md`, and its tools are in `inputs/C2_BA/out/tools/` (`cdl_compare.py`, `sheet_vs_source.py`,
`intended_equiv.py`, `users_ba.py`, `render.sh`, ...). Reuse them, and adapt them where the s2d cell needs it. C2's
finished files in `work/macros/sg13cmos5l_IOPadDiff2Single/` are the model to follow for layout and style:
- the pad sheet and symbol;
- `d2s_mpdda_pd.sch` with its `[DM]` dummy block;
- `units.spice` / `unit_r2.sch`;
- the 8 CACE templates and the yaml;
- `macros/slot/schematic/xschem/slot.sch` (`xd2s`, `xd2s_c`, `xd2s_g`), and the top sheet (`xoutbuf`, `xoutbuf_c`,
  `xoutbuf_g`).

## The truth to match

`inputs/pad_candidate.cdl` (subckt `sg13cmos5l_IOPadSingle2Diff`) is the reference netlist the layout passed IHP LVS
against, device for device. It follows the hierarchy of the layout cells, not of the sheets.
- The lead verified that it equals the circuit (the current source netlists plus `s2d_pad_esd.sch`) except for the
  added dummies and the drawn finger splits: `inputs/circuit_check.py` and `inputs/pad_cdl_check.py`.
- `inputs/netlist_changes.md` (agent F) lists what changes and why. Read it first: it is your change list.
- `inputs/report_stageB*.md` are F's reports, and `inputs/decisions.md` holds Christoph's decisions.

## Changes

1. **Pad cell `macros/sg13cmos5l_IOPadSingle2Diff/schematic/xschem/sg13cmos5l_IOPadSingle2Diff.sch` / `.sym`:**
   - Ports, in this order: `iovdd iovss vdd vss pad outp outn vcm vref iref en_3v3 en_3v3_b`. The old `ibias en_1v2
     sel0_1v2 sel1_1v2 vdd1v2_sense vdd3v3_sense` go, and `iref en_3v3 en_3v3_b` come in.
   - Remove `xc` (`en_ctrl_3v3`) and `xg` (`bias_gen_pd`). Keep `xt` (`bias_tree_noab_pd`) and `xa`
     (`s2d_mpdda_pd`).
   - **Secondary protection: none.** The `sg13cmos5l_SecondaryProtection` instance goes, and `padres` becomes `pad`:
     the buffer's vin is the pad.
   - **Primary protection as drawn:** replace IHP's library clamp / diode instances with the devices of
     `s2d_pad_esd.sch` (in this macro; the CDL's RRP / MMCP / RRN / MMCN / DDP1 / DDP2 / DDN1 / DDN2). Either
     instantiate `s2d_pad_esd.sym` or draw the devices on the pad sheet; say which and why.
     - Diodes as scalar instances, never as vectors: C2 found that vector diode names break the PDK's diode_drc tcl.
     - The rppd bodies are on iovss.
   - **vss / iovss**, as C2's decision 2(a): `Rsub` 1 Ohm vss – iovss with `lvs_ignore=open`, documented as the
     shared p-substrate (see C2's pad sheet and its commit 2abcca1: the LVS netlists keep the two ports separate).
   - Keep the drawing readable: the xschem-analog-schematic skill's style if you know it, no overlapping wires, and
     labels instead of long wires.
2. **`s2d_mpdda_pd.sch` / `s2d_mpdda.sch` and `netlist/source/s2d_pd.spice` / `s2d_mpdda.spice`** (as C2's change 2):
   - finger counts and `ng` as drawn (netlist_changes §1 table);
   - every dummy of the s2d cells as a device, in a `[DM]` block as C2 drew it, with names and nets from the CDL;
   - the two dummy rhigh strips `vss vss vss rhigh w=0.5u l=12.65u`.

   `s2d_mpdda.sch` is Christoph's sheet (2026-10-23). Edit only what the drawn fingers require, and put the dummies
   on `s2d_mpdda_pd.sch` where their nets are reachable (they are all on rails or on bias / vcmfb lines; check). Say
   where each went.
   - The four bias diodes BP / BN / BPC / BNC **stay in `bias_diodes`** (inside `bias_tree_noab_pd`), as C2 left them
     in `bias_tree_pd`. Flat LVS is the same either way; netlist_changes' "move" is not done.
   - `unit_r2` is shared with the d2s macro (`../sg13cmos5l_IOPadDiff2Single/`). C2 already redrew it as 4 rhigh
     segments. Check that it equals the drawn `s2d_rhigh_c3` units; do not edit it unless it differs.
3. **`macros/bias_tree_noab_pd/` (sheet and `netlist/source/bias_tree_noab_pd.spice`):** add the two tree dummies of
   the layout (netlist_changes §2). Use C2's names and style for its `MDBP` / `MDBN` in
   `macros/bias_tree_pd/schematic/xschem/bias_tree_pd.sch` (C2 decision 1(a): the NMOS dummy's gate is the tree's
   internal net `ni`, which the pad sheet cannot reach). Nothing else in that macro changes.
4. **Source netlists** in `macros/sg13cmos5l_IOPadSingle2Diff/netlist/source/*.spice`: the same changes, so that the
   sources and the sheets agree. Update their header comments.
5. **Users of the pad symbol** (keep the old function by placing what left the cell next to it):
   - The 7 CACE templates `verification/cace/templates/sg13cmos5l_IOPadSingle2Diff_tb_*.sch`: add `en_ctrl_3v3`
     and `bias_gen_pd` instances wired as the old pad sheet wired them, as C2 did. Update the yaml's `pins:` section
     to the new ports, and keep the template sources that drove the old pins (they now drive the added instances).
     Also fix any probe of a net that left the cell (C2: `v(x1.en_3v3)` → `v(en_3v3)`) and any reference to
     `padres`.
   - The loop fixture (`s2d_mpdda_pd_sel.sch`, `s2d_mpdda_pd_sel.yaml`, `s2d_mpdda_pd_sel_tb_loop.sch`) uses
     `s2d_mpdda_pd`. It changes only through change 2; check that it still netlists.
   - `macros/slot/schematic/xschem/slot.sch` (`xs2d`) and the top sheet
     `schematic/xschem/sg13cmos5l_cm_ip__single2diff2single.sch` (`xinbuf`): the same, with minimal edits, named
     as C2 named its instances (`xs2d_c` / `xs2d_g`, `xinbuf_c` / `xinbuf_g`).
   - `testbenches/spice/tb_pad_dc.spice` and any other deck in the macro that instantiates the pad with the old
     ports.
6. **`README.md` / `FILL_IN.md`** of the macro: only correct statements that the change makes false (ports,
   protection, xc / xg). The lead writes the verification status.

## Checks (all measured, logs in `out/logs/`)

- **Netlisting:** xschem netlists every changed sheet without errors (PDK xschemrc plus the repo's; run
  `export PDK_ROOT=/foss/pdks; source .designinit` in `work/`).
- **Pad sheet vs layout reference:** netlist the pad sheet as an LVS CDL (`make -C
  macros/sg13cmos5l_IOPadSingle2Diff klayout-lvs-netlist SCRIPTS_DIR=../../scripts`, or what the Makefile needs),
  then compare it with `inputs/pad_candidate.cdl`, flattened, with C2's `cdl_compare.py` adapted. They must agree
  device for device, dummies included: W per (model, L, D/S, G, B), diodes, resistors series-reduced. Also run a
  sanity test: a mutated copy must fail.
- **Sources vs CDL:** the same comparison for the source netlists.
- **Sheets vs source netlists:** each changed sheet's netlist against its source subckt (topology, w / l / ng, port
  order).
- **Users, before vs after:** with C2's `intended_equiv.py` (adapted): the new flat netlist minus exactly the
  intended changes equals the old one. The intended changes are dummies, finger splits, the protection as drawn, no
  secondary protection, `padres` → `pad`, xc / xg moved out, and Rsub. Cover slot.sch, the top sheet, the 7
  templates and the loop fixture. Make the untouched reference with `cp -a` of `work/{macros,schematic,testbenches}`
  **before** you edit (`out/old_root/`).
- **tb_pad_dc** (ngspice), old vs new: it runs. Report I_Q and the bias lines per selection, and the disabled current.
  The secondary protection's removal should not change DC.
- **Boundary:** `make check-boundary` in `work/` passes.
- **Renders:** PNGs of every changed sheet and symbol in `out/renders/`, before and after.
- **Originals:** a copy of every file you replace, as it was, in `out/macro_before/` (same relative paths).

## Deliverables

- `out/changed_files.txt`: every file you changed or added, relative to the repo root.
- The checks above.
- `out/ba_note.md`: under about 100 lines, in the layout of C2's `report.md`. The harness may refuse files named
  `report*`; if it refuses this one too, put its text in your reply.

Reply with a summary of no more than 12 lines, and do not report success you have not checked.

## Hard rules

- Write only in `BA/`. No git and no web searches.
- Background commands run for under 2 h. Kill them by PID, never with `pkill -f`.
- Do not touch the GDS: the lead handles the layout in parallel (port texts, the iovdd rail tie cell; no device or
  net change).
