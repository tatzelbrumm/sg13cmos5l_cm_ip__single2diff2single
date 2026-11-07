<!--
SPDX-FileCopyrightText: 2026 Christoph Maier
SPDX-License-Identifier: Apache-2.0
-->
# Brief P3: rb_avg redone with abutted gate poly (pad_ref_rb, cloud session C4, 2026-11-07)

Read `BRIEF_common.md` (same folder) first; it still applies. Your workspace: `P3/` (`P3/work`, `P3/out`). Report to
`reports/P3_report.md` (same folder; if that write is refused, put the report in your hand-back). Write "Claude" for
yourself in every file, never a model name.

## Why this round

Agent P built rb_avg (the three averaging diodes of vcm_rb) as separate "small tubs", each 1u/4u PMOS in its own NWell
with its own tie, and in round 2 added dummy small tubs on vdd at both ends: `D SL1 SU SL2 D`, 36.80 × 3.23 µm. Its code,
outputs and reports: `P/out/` (`build_rb_p.py`, `rb_p_cells.gds / .cdl`, logs) and `reports/P_report.md`, `P_report_r2.md`.

Christoph (2026-11-07): "rb_avg: why can't you abut by gate poly? there's PLENTY of precedent in the bias generators and
pads, and in the records of the layout agents." The lead's brief over-constrained P ("each in its own NWell"). The
circuit (`R/macros/vcm_rb/netlist/source/vcm_rb.spice`; D G S B):

| device | terminals | note |
|---|---|---|
| SU | `m m gh gh` 1u/4u | diode, bulk = source gh |
| SL1, SL2 | `xp xp m m` 1u/4u | diodes in parallel, bulk = source m: identical terminals |

The averaging works because the three devices are identical (m = average of gh and xp); their mismatch is the cell's
offset. So every active finger must see the same surroundings.

## What to do

1. **Two wells, by bulk net:** well(gh) for SU, well(m) for SL1 + SL2. SL1 / SL2 are fingers of one row with abutted gate
   poly (gate xp), sharing diffusion where the circuit allows (both sources are m, both drains xp).
2. **Dummies by gate-poly abutment, the pads' convention** (C3 decision 3, Christoph 2026-11-03: "Dummy source and drain
   to the rails, gate net by abutment where dummies extend abutted gate poly"): dummy fingers of the same 1u/4u geometry
   at both ends of each row, gate poly abutted to the row's gate (SU's row: gate m; SL row: gate xp), source and drain on
   that well's rail (gh, resp. m), bulk = the well. Then SU sees a dummy on each side, SL1 and SL2 each see a dummy and
   an identical active finger: make the device-layer surroundings of SU, SL1 and SL2 identical (P's `logs/surround.py`
   measures it).
3. **Precedent to study before drawing** (paths in `BRIEF_common.md`): the pad tub `tub_p20x1_c3` (two fingers with
   abutted gate poly in one well, bulk = source; the dummy tubs), the pads' rows with end dummies contacted by abutment
   (C3 `build_s2d_p3.py` / `build_s2d_n3.py`, C2 P2 / N2 in `agents_c2/`), the OA core's layout
   (`S/design_considerations/pad_buffer_layout/oa_core_pd_v2_2026-10-28/`: oa_ms1, oa_svpg, the generic / IHP layout skill),
   and the harness bias generator's Magic layouts if useful (`/home/user/rtimothyedwards/sg13cmos5l_ocd_ip__biasgen/magic/`,
   read as text, never run its scripts). Say which precedent you followed.
4. Revisit the tie: P kept a separate tie because "a butted tie needs ≥ 0.40 µm P+ beyond the gate (pSD.i1) plus
   ≥ 0.30 µm N+ (pSD.f), but the PCell's source is 0.34". With shared diffusion between fingers or a tie at the row end,
   that may no longer bind. Choose the most compact correct option and cite the rules.
5. Use P's library code (import `build_rb_p.py` / `build_s2d_p3.py` from `P/out/`, do not edit P's files) and the
   PDK PCells; deliver `rb_avg` as a cell of its own in `P3/out/rb_avg_v3.gds` (+ `.cdl`, PNG, build script, logs).
   The other three PMOS cells stay as P delivered them.

## Checks and report

DRC (`run_drc.py --no_density`), LVS (`run_lvs.py --disable_tap_extraction`, CDL with all dummies), sym_check, LU,
the surround XOR (SU vs SL1 vs SL2, device layers, within one finger pitch), size against P's 36.80 × 3.23 µm.
Report (≤ 60 lines): layout, the precedent followed, checks, size, and the **dummies for backannotation** (name, size,
d g s b; they replace MDA[1:0] all-on-vdd in vcm_rb), plus pin positions.
