<!--
SPDX-FileCopyrightText: 2026 Christoph Maier
SPDX-License-Identifier: Apache-2.0
-->
# Kickoff: carry the hand-drawn bias sheet style over to the Oguey–Aebischer sheet

2026-10-22. Written at the end of the session in which the Banba bandgap was discussed and
`bg_core_pd.sch` was cleaned up.

Task: Christoph re-drew the bandgap bias sheet `d2s_bias_bg_pd` by hand. Give the other bias sheets
the same arrangement, first and foremost the Oguey–Aebischer variant `d2s_bias_oa_pd`, which was
never hand-edited. Change only placement, wiring, block frames and texts. Devices, sizes, nets and
ports stay as they are.

## Where things are

Main repo: `~/EDA/sg13cmos5l_cm_ip__single2diff2single`, branch `toplevel`. Notes worktree:
`~/EDA/sg13cmos5l_cm_ip__single2diff2single_sudelbuecher`, branch `sudel_buecher`. Read `CLAUDE.md`
first (worktree rules, chat-log rule).

- **The model (hand-edited):**
  - `macros/d2s_bias_bg_pd/schematic/xschem/d2s_bias_bg_pd.sch`. This is a copy of
    `power_down/xschem/d2s_bias_bg_pd.sch` as hand-edited on 2026-10-09 00:12, plus three wiring
    repairs (`macros/d2s_bias_bg_pd/README.md`, section Schematic).
  - `macros/d2s_bias_sel_pd/schematic/xschem/bg_core_pd.sch`, the core cut from it. Its leftover
    en_3v3_b stubs and empty [E] frames were removed on 2026-10-22, and its netlist is unchanged.
- **What the hand edit changed.** Run git in the main repo: the worktree's git link does not
  resolve from the linked VM.

  ```
  git diff 8bdbbb0 685c2bc -- sudelbuecher/design_considerations/class_ab_pad_driver/power_down/xschem/
  ```

  - 8bdbbb0 (2026-10-08) is Claude's drawing; 685c2bc (2026-10-14) is Christoph's "hand drawing
    schematics work in progress".
  - The diff covers bg, in and out. Each sheet has the same set of instances before and after, so
    the edits are placement, wiring, frames and texts only.
  - bg is the most complete; in (2026-10-09 00:44) and out (2026-10-08 18:30) show the same hand at
    work.
- **The target:** `macros/d2s_bias_oa_pd/schematic/xschem/d2s_bias_oa_pd.sch`.
  - It is an unchanged copy of the agent-drawn `power_down/xschem/d2s_bias_oa_pd.sch`
    (2026-10-06 18:45), 71 instances.
  - Afterwards, re-cut `macros/d2s_bias_sel_pd/schematic/xschem/oa_core_pd.sch` from the new sheet,
    the same way `bg_core_pd` was cut from `d2s_bias_bg_pd`.
- **Connectivity reference:** `macros/sg13cmos5l_IOPadDiff2Single/netlist/source/d2s_bias_ref_pd.spice`,
  subckt `d2s_bias_oa_pd`. Design background: `improvements/bias.md` (variant 3) and
  `power_down/log.md` in the notes worktree.

## Scope (defaults; confirm with Christoph at the start)

- **In:** `d2s_bias_oa_pd`, then `oa_core_pd`.
- **Report only:** `d2s_bias_in_pd` and `d2s_bias_out_pd` are Christoph's own hand edits. List where
  they depart from the bg conventions; don't change them unless he says so.
- **Out:** `macros/OgueyAebischerBias`, the old 1:1 sky130 port, which is a separate macro.
- Edit the `macros/` copies. Leave the originals in `power_down/xschem/` unchanged; the macro READMEs
  refer to them as they are.

## Method

1. **Write down the conventions before drawing.** Read them off the diff and the bg sheet, put them
   in this folder's `log.md`, and show them to Christoph. Cover at least:
   - the column order of the blocks ([E] enable, [S] start-up, [C] core, [R] output / I_ref,
     [8] mirror tree and diodes);
   - the rows of the rails vdd / vss / vddo / vsso;
   - the routes of en_3v3 and en_3v3_b;
   - the rhythm of the device grid, the frame sizes and the label positions;
   - where the title and legend texts sit.
2. **Map OA onto that frame.** The OA sheet has the same [E] / [S] / [R] / [8] blocks as bg; only [C]
   differs. Keep every instance name. Move the instances and redraw their wires.
3. Keep the lab_wire names that `oa_core_pd` and `d2s_bias_sel_pd` use.

## Verification (all of it, before handing back)

1. **Netlist identity.**
   - Netlist the new sheet with xschem. Compare it device by device with subckt `d2s_bias_oa_pd`:
     model, w / l / ng / m, the terminal nets (internal nets matched by name), and the port order.
   - Also netlist the old and the new sheet. Apart from the header they must be identical.
   - If they are, no simulation is needed. If they aren't, fix the drawing; don't touch the netlist.
2. **No dangling wire ends.**
   - Get every instance pin from xschem's Tcl (`xschem instance_pins <inst>` and
     `xschem instance_pin_coord <inst> name <pin>`).
   - List the `N` segment ends that touch neither another wire nor a pin.
   - Pin-on-pin joins are legal (e.g. `iout` sits on POC's drain).
   - Each hand edit of bg / in / out introduced wiring errors (3 / 1 / 1; see the macro READMEs), so
     don't skip this check.
3. **Figure.** Export with
   `improvements/xschem/scripts/export_figures.py --xschem <dir> --out <dir> <sheet>`, look at it,
   and send the PNG to Christoph.

## Environment

- Recipe: `sudelbuecher/cloud_environment.md`. For netlisting and figures, xschem and the PDK's
  xschem libraries are enough:
  - `apt-get install flex bison` on top of the recipe's list. Without them, `configure` aborts on
    "parsgen/flex".
  - xschem at `ddc734480d5326fb787993dad24f4062e5d28434`.
  - IHP-Open-PDK (iic-jku fork) at `c271a7e97a7bab201c1d0a399215969d2ee19573`, with a sparse
    checkout of only `ihp-sg13cmos5l/libs.tech/xschem/` and `ihp-sg13g2/libs.tech/xschem/`.
  - `pip install cairosvg pillow`, plus `fonts-liberation`.
  - `PDK_ROOT=<checkout> PDK=ihp-sg13cmos5l`, and the macros' `xschemrc` as shipped.
- Linked computer:
  - Read and edit with device_bash.
  - Stage files into the container for xschem.
  - Write results back with device_commit_files from `/mnt/user-data/outputs/`, with
    `expectedMtimeMs`.
- No git commits; Christoph commits.

## Deliverables

- The new `d2s_bias_oa_pd.sch` and `oa_core_pd.sch`.
- The Schematic sections of `macros/d2s_bias_oa_pd/README.md` and `macros/d2s_bias_sel_pd/README.md`,
  updated: what was redrawn, from which model, and how it was checked.
- `log.md` in this folder: the conventions, the deviations found in in / out, and the check results.
- Figures (PNG, SVG) of both sheets.
