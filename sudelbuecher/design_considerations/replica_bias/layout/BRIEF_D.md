<!--
SPDX-FileCopyrightText: 2026 Christoph Maier
SPDX-License-Identifier: Apache-2.0
-->
# Brief D: layout of `bias_dist_pd` (4 inputs, 4 outputs) for the shared bias option (cloud session C4, 2026-11-07)

You are agent D. You lay out `bias_dist_pd`, the switchable 1 : 1 distribution mirror that hands one shared set of
reference currents to every block that needs bias. Christoph chose the shared option: "ok lay out for the shared option,
there's plenty of space to duplicate the layout if the mood hits me". Model: Opus, effort high.

**Workspace:** `$WS` = `layout_rb/D` (`work/`, `out/`); report to `layout_rb/reports/D_report.md`, progress lines to
`layout_rb/reports/D_progress.md`. Write nowhere else. The repository is read-only for you.

## Circuit (source of truth, read only)

- `/home/user/sg13cmos5l_cm_ip__single2diff2single/macros/bias_dist_pd/netlist/source/bias_dist_pd.spice` (4 inputs
  since today), its `README.md` (truth table, the two possible analog / digital cuts, the TG reuse notes),
  `testbenches/spice/tb_truth.out`. The gates: `macros/hv_logic/netlist/source/hv_logic.spice` (`nand2_hv`, `inv_hv`,
  1u / 0.45u hv devices; no layout exists yet).
- Devices: input slices 4 × (nand2_hv + inv_hv + TG TIN / TIP 1u/0.45u); output slices 4 × (nand2_hv + inv_hv + PMOS
  output PO 5u/6u + TG TON / TOP); core NI, NM 6u/6u (NMOS), PD 5u/6u (PMOS diode), TDN, SVPD 1u/0.45u.
- Inputs (sourced currents): iin0 = oa_core_pd, iin1 = bg_core_pd, iin2 / iin3 = harness ibias0 / ibias1. Outputs
  (sourced, 1 : 1): iout0..3 = S2D iref, D2S iref, pad_ref_rb iref, spare. Static enables en_in<k>, en_out<j>,
  en_3v3, en_3v3_b.

## Rules (binding)

- `inputs/BRIEF_common.md`, section "Binding rules, verbatim from the briefs of the pads' layout agents": every rule
  there binds you (symmetry and matched dummies at row ends, dummies on the rail with gate by abutment, bias diode at a
  row end needs its twin or goes to the middle, taps as rings and never between rows, no center gate contacts, gates
  contacted with poly, minimal metal stubs, compactness against the pad / library counterpart).
- **Matching:** NI / NM and PD / PO0..3 are the matched devices: put each group in one row with its diode in the
  middle or twinned, as the pads' tree and tail rows do (`inputs/N/rb_n_cells.gds` rb_tree_n, `inputs/P/rb_p_cells.gds`
  rb_tails are the closest precedents; reuse their generators `build_rb_n.py`, `build_rb_p.py`, `build_s2d_p3.py`).
- **Switches and logic:** the TG is the project's standard 1u / 0.45u pair; the d2s pad has a laid-out one
  (`d2s_tgsw_f2` in `/home/user/sg13cmos5l_cm_ip__single2diff2single/macros/sg13cmos5l_IOPadDiff2Single/layout/klayout/sg13cmos5l_IOPadDiff2Single.klay.gds`).
  Draw `inv_hv` and `nand2_hv` as compact cells (DRC / LVS clean on their own) and reuse them. Choose the cut
  between analog and digital yourself (the README's option A strict, or B by slice); say why.
- **Metal M1 / M2 only** (Christoph: "Pad structures are only routed M1/M2. Let's keep it that way for consistency").
- **Floorplan context** (Christoph): the bias block sits at slot7's right side near the top, with "reference cores
  ... best stacked vertically", pad_ref_rb toward the right edge. So: the inputs iin0 / iin1 face the cores (left),
  iin2 / iin3 come from the harness on the slot's left edge (left), the outputs face right and up (S2D iref at the
  slot's right edge y 159.5, D2S iref y 260.6, pad_ref_rb's iref on its left edge, a spare). Enables on one edge
  (static configuration bits). Pins `vddh` / `vssh` for the supplies, as pad_ref_rb.
- **Compact:** "the layout should be MUCH more compact" (Christoph on the first pad_ref_rb). Report area against the
  sum of the device rows.
- Rule values only from the PDK decks / documents; keep code small; say which statements are measured [M] and which
  are reasoning [R].

## Deliverables (`out/`), then stop

- `bias_dist_pd.gds` (top cell `bias_dist_pd`) and the gate / row cells; `.cdl` (flat, every device, dummies
  included, built by script from the source netlist plus your dummies); `pin_map.md`.
- Checks: `run_drc.py --no_density` (and grep "exception"), `sg13cmos5l_maximal.drc -rd latchUpRules=true`, LVS
  `run_lvs.py --disable_tap_extraction` against your CDL, `sym_check.py` on the matched rows, a negative LVS test.
- `previews/` (whole cell with nets, close-ups), `note.md` (under 80 lines: structure, area, dummies added with
  d g s b and W / L for backannotation, open points), the report, then a reply of no more than 15 lines.

Tools: `export PDK_ROOT=/foss/pdks; cd /home/user/sg13cmos5l_cm_ip__single2diff2single && source .designinit`; DRC
`python3 /foss/pdks/ihp-sg13cmos5l/libs.tech/klayout/tech/drc/run_drc.py --path=<gds> --topcell=<cell> --no_density
--mp=4 --run_dir=<dir>`; LVS `.../lvs/run_lvs.py --layout --netlist --topcell --run_dir --disable_tap_extraction`.
Hard rules: no git, no web, no `mcp__*` tools; "Claude, agent D" in files, never a model name; kill by PID only; if
an action is refused or blocked, stop that step and report it.
