<!--
SPDX-FileCopyrightText: 2026 Christoph Maier
SPDX-License-Identifier: Apache-2.0
-->
# Report of Claude, agent R (survey of fill / decap / endcap / tap and 3.3 V logic / TG / switch cells), 2026-11-08

Full survey: `R/out/survey.md` (tables, rule citations, options A-G). Previews (25 PNG): `R/out/previews/`. Scripts and clones: `R/work/`.
Read only; no design file changed; nothing pushed; no external script run. Fork branches fetched (`git fetch --depth 1`) as listed in the brief.

Key findings:
1. No endcap or tap cell exists in the PDK. [D] `libs.tech/librelane/sg13cmos5l_stdcell/config.tcl` says so; `FP_TAPCELL_DIST 0`. [M] All 84 lv cells have full-width p+ (bottom) and n+/NWell (top) tie rails inside the cell; the harness `housekeeping_top` closes its 33 rows with `decap_8` at the start and fill / decap at the end.
2. lv fill (0.48-3.84 x 3.78 um) and decap_4/8 (1.92 / 3.36 x 3.78 um) are 1.2 V; decaps are lv MOS caps and cannot sit on 3.3 V rails. Fill cells have no gate, only well + ties.
3. A 3.3 V std-cell library `sg13cmos5l_stdcell_hv` (84 cells incl. `hv_fill_1/2/4/8`, `hv_decap_4/8`, `hv_antennanp`, `hv_tiehi/lo`, 7.14 um rows, no endcap, no TG, no level shifter) is in the PDK clone's `dev` ref (`3bccbc7b`, 2026-11-04) but not in the checked-out tree (`df4c5054`) and its blobs are not local (partial clone). Not read: needs a read-only fetch, your decision. Commit messages state DRC clean and LVS 84/84, wells with 0.62 um lateral overhang so a row's outermost cell is clean without a neighbor. Four of these cells are measurable in `rcyaon/bidir-level-shifter` `gds/slot_1.gds` (previews `bidir_sg13g2_hv_*`).
4. The DRC deck has DigiBnd rules (NW.c1/d1/e1/f1 .dig, Cnt.c.Digi) and latch-up rules LU.a-d1; the layout rules say DigiBnd "must be used" with IHP's digital libraries; guard rings are asked for only at pad output buffers (7.2.1).
5. TG / switch / level-shifter layouts that exist: harness `xgate`, `hv_inv_1`, `level_shift` (biasgen, GDS in voltgen_v2 / biasgen2), `analog_switch_small/med`, `analog_pswitch_small`, `sw_lvl_shift`; PDK IO `LevelUp`, `LevelDown`; `bidir-level-shifter` `muxhv` (2 TGs, hv), `level_shifter_up`. No hv transmission-gate standard cell was found anywhere.
6. Closing options (survey section 4): PDK `guard_ring` PCell (nwell / psub), hand-drawn end strips, lv fill (grid 3.78 vs our row 5.99), hv fill / decap (unread), re-draw on the hv std rows (7.14 um), harness switches.

Not done: blobs of the hv library; the other 14 slot repositories; the two template repositories (outside the brief).
