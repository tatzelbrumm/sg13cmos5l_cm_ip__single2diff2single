<!--
SPDX-FileCopyrightText: 2026 Christoph Maier
SPDX-License-Identifier: Apache-2.0
-->
# C1: verification changes and omissions, for review

Cloud session C1, 2026-10-30, branch `claude/c1-core-pex-verif` (commits 0ee4cc0 … 8a72dd8). Report:
`C1_core_pex_bias_verification_report.md`. Paths below are relative to `macros/bias_sel_pd/` unless they start with
`macros/` or `scripts/`. "Undo" assumes the rest stays.

## Changes

1. **`verification/cace/templates/bias_sel_pd_tb_dc.sch`, `_tb_tran.sch`: replica loads `XRp1 XRp2 XRn1 XRn2` renamed
   `XRabp1 XRabp2 XRabn1 XRabn2`.** SPICE names are case-insensitive, so they were the fixtures `XRP1 XRP2 XRN1 XRN2`
   (added 2026-10-27/28) a second time, and ngspice-47 stops: "device already exists, bail out". These templates had not
   run since. Undo: rename back (ngspice-47 then stops again). `_tb_tran.sch` also sets `option reltol=1e-4` at run time
   just before `tran` (see 4; a no-op for the other views). Undo: delete that line with 4.
2. **Same two templates: `.include CACE{templates}/cores/CACE{cores=schematic}.spice` before the DUT include** (+2
   comment lines). A core view file may define `oa_core_pd` / `bg_core_pd`; ngspice keeps the first definition of a
   subckt and ignores the DUT netlist's ("redefinition ... ignored" in the log). `cores/schematic.spice` is comments only:
   a control run (HEAD templates + only change 1) gave identical `sel_params`. Undo: delete the three lines.
3. **`_tb_dc.sch`: `.option SEED=CACE[CACE{seed=12345} + CACE{iterations=0}]`**, as in `bias_oa_pd_tb_dc.sch`, for the
   mismatch groups. Outside them nothing is drawn; same control run. Undo: delete with the mismatch groups (6).
4. **`verification/cace/templates/cores/` (new): the core views.** `schematic.spice`, `magic_pex_2.spice`,
   `magic_pex_3.spice`, `magic_pex_2_mm_ok.spice`, and four generated netlists (`make cores-pex-sim`):
   `bg_core_pd_magic_pex_{2,3}_tied.spice` tie bg's 41 capacitor-only nodes (one per rhigh segment) to vss through 1 TΩ.
   Without that the op is singular and lands on a wrong point (sel 1: vbp +18 %); with it PEX 2 reproduces the
   schematic's dc currents. `{oa,bg}_core_pd_magic_pex_2_mm_ok.spice` also carry `mm_ok=1` on every MOS and rhigh.
   oa's netlists are included as committed (no such nodes). `magic_pex_3.spice` sets `.option itl1=5000` and, in a
   `.control` block of its own, `option reltol=1e-3` for the operating points (the template's later `.options
   reltol=1e-4` would win otherwise): with the full-RC bg netlist 7 dc runs fell back to a transient op and landed on
   wrong points (sel 2, tt: I vdd −21 %; sel 1, ff, −40 °C: vbp +33 %); itl1 fixed 4, reltol the other 3, and the dc
   currents then agree with the schematic to 0.02 %. The tran and start-up templates set reltol back to 1e-4 right
   before their transient (at 1e-3, 2 tran runs stopped and settling to 1 % wasn't resolved). `magic_pex_2_mm_ok.spice`
   has the same two settings (2 of 600 `mm_params` runs fell back to a transient op without them). Undo: delete the
   folder (with 2).
5. **`verification/cace/bias_sel_pd.yaml`: default condition `cores` (typical `schematic`).** Undo: delete it.
6. **`bias_sel_pd.yaml`: mismatch groups `mm_params` (tt, typ, typ, 27 °C), `mm_lo_params` (ss, rhigh wcs, pnpMPA bcs,
   −40 °C), `mm_hi_params` (ff, bcs, wcs, 125 °C)**, each sel 1 / 2 / 3 × vdd 3.0 / 3.6 V × 100 iterations, limits `any`
   (sel 3 doubles every current; `make mc-table` compares sel 1 / 2 with the limits of `supply_params` and
   `pvt_params`). The worst-case corners are the extremes of the `pvt`, `supply` and `rpnp` results, the same for both
   cores. Not in the default `CACE_GROUPS` (3 × 600 runs: 15 min on the schematic, 1.7 h in the `mm_ok` view): `make sim-cace-mm`. Undo: delete the three groups,
   `CACE_GROUPS_MM`, `sim-cace-mm`, `mc-table`, `scripts/cace/mc_stats.py`.
7. **`bias_sel_pd.yaml` + new `templates/bias_sel_pd_tb_psrr.sch`, `_tb_startup.sch`: groups `psrr_params` (sel 0 / 1 / 2 ×
   ss / tt / ff × −40 / 27 / 125 °C, report only) and `startup_params` (sel 1 / 2 from a supply ramp, limits of
   `bias_oa_pd`), in the default `CACE_GROUPS`.** The measurements of the flat copies' psrr / startup groups. Besides
   `tran_params` they are the only groups where the cores' parasitic C can show. The PSRR template has the DUT's vss on
   node VSS (GND in the DC one) so that it can carry ripple, and reltol 1e-4 as the DC template (with the flat one's
   1e-6 the op of sel 0, ss, −40 °C fell back to a transient op); the start-up one needs `itl4=1000` (sel 2, ff,
   −40 °C, 3.6 V stopped at "timestep too small" in pnpMPA) and `option reltol=1e-4` before its transient (see 4). The
   bandgap's pnpMPA at −40 °C on the 1 µs ramp is fragile: `vntol=1e-4` rescued one PEX 3 run but lost two PEX 2 runs,
   so it is not used. Undo: delete the groups, the templates and the two names in `CACE_GROUPS`.
8. **`Makefile`: `CORES` (default `schematic`).** Another view runs a copy of the yaml (`_bias_sel_pd_cores.yaml`,
   deleted afterwards) whose `cores` defaults to it, and writes `results/bias_sel_pd_cores_<view>/`; a missing view
   file fails (`exit ${status:-1}`). `sim-cace` warns per group about runs whose op fell back to a transient op or
   stopped at "timestep too small" (the run folders are deleted, so this went unseen). New targets `sim-cace-mm`,
   `mc-table`, `cores-pex-sim`; `spec-table` takes `CORES`. Undo: `git checkout <base> -- Makefile` (then 2-7 can't be
   selected).
9. **`scripts/cace/pex_for_sim.py`, `mc_stats.py`, `compare_views.py` (new).** Simulation copies of PEX netlists
   (`--mm-ok`, `--tie`), Monte Carlo statistics against limits, view-against-view tables. Undo: delete.
10. **`verification/cace/results/bias_sel_pd/` rewritten by `make sim-cace`.** sel 0 is bit-identical to the committed
    CSV; sel 1 / 2 / 3 differ (vbp −0.15 / −1.0 / −0.6 % at tt, 27 °C) because the cores' schematics were redrawn for
    their layouts on 2026-10-28, after these results (0d12e00). Plus `psrr_params`, `startup_params` and the mismatch
    CSVs, and the CACE plots (one PNG per yaml `plot:` entry, over all runs of the group; the other bias_* results
    have none). Undo: `git checkout <base> -- verification/cace/results/bias_sel_pd`.
11. **New results folders** `results/bias_sel_pd_cores_magic_pex_2/` (all groups + the plain-PEX mismatch groups),
    `_magic_pex_3/` (all default groups), `_magic_pex_2_mm_ok/` (mismatch groups). Undo: delete.
12. **`macros/bg_core_pd/`: generated outputs** (as C0's list for oa_core_pd): schematic and layout LVS netlists, magic
    PEX 1 / 2 / 3, KLayout-PEX 2, `bg_core_pd_pex.sym`, DRC and LVS reports. Undo: delete.

## Omissions

1. **`bias_oa_pd`, `bias_bg_pd` (flat copies) not dropped or slimmed.** They characterize the cores as they were before
   2026-10-28, and their psrr templates have the same `XRP1` / `XRp1` collision (1), so `psrr_params` can't be rerun
   there as is. `bias_sel_pd` now covers dc, PVT, mismatch, psrr, start-up and power-down for the current cores with
   sel 1 / 2, with every core view. Suggestion: drop their CACE once nothing else needs them (`bias_oa_pd` is in the pad
   testbench `tb_pd_startup_oa`).
2. **The same collision in `bias_in_pd` / `bias_out_pd` `_tb_psrr.sch` not fixed** (not core-related). Fix: rename the
   replicas as in 1.
3. **`bias_sel_pd/README.md` not updated** (not a testbench or verification file): its 2026-10-20 results are stale for
   sel 1 / 2 / 3; the report has the new numbers.
4. **No KLayout-PEX view.** Only magic views, as the brief asked; `cores/klayout_pex_2.spice` would be the same 15 lines
   (bg's KLayout netlist has the same 41 capacitor-only nodes).
5. **`<core>_pex.sym` (type primitive) not used.** The views redefine the subckt instead, so neither the DUT sheet nor
   the templates' drawing changes.
6. **Core Makefiles' `SCRIPTS_DIR := scripts` not fixed**; the PEX targets need `SCRIPTS_DIR=../../scripts` (C0 finding).
7. **`scripts/cace/cace_to_csv.py` column labels not fixed:** its SI map lacks `us`, so `t_settle[us]` (already in the
   committed CSV) and the new `t_su90[us]` hold seconds; `%/V` columns hold fractions per volt. `spec_table.py` and the
   new scripts scale by the yaml unit, so only the label is wrong. Fix: add `'us': 's'` to the map.
8. **One PEX 3 run not chased further:** in `psrr_params` the op of sel 2, ff, −40 °C still falls back to a transient
   op (its values are ~10 % off a converged reference with gmin 1e-12; it sets none of the maxima). All other PEX 3
   groups run complete without fallback.
9. **Pad-level CACE** (`sg13cmos5l_IOPadDiff2Single`, `…Single2Diff`): out of scope; the report says what it would need.
