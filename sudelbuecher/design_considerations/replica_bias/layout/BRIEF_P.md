<!--
SPDX-FileCopyrightText: 2026 Christoph Maier
SPDX-License-Identifier: Apache-2.0
-->
# Brief P: the PMOS rows of pad_ref_rb

Read `BRIEF_common.md` first. Your workspace: `P/` (this folder's `P/work`, `P/out`). Start from C3's P
(`.../agents_c3/P/out/build_s2d_p3.py`, `report.md`) and reuse its code.

| cell (deliver as `rb_<name>`) | copies (S2D pad) | devices (netlists; D G S B) |
|---|---|---|
| `rb_tree_p` | `bias_tree_noab_p_c3` as drawn (its own generator call), rewired | PBNC `vbnc vbp vdd vdd` 2/6; BP `vbp vbp vdd vdd` 2/6 diode, in the pad's dummy 2/6 slot (MDBP); MDPBN `vdd vbp vdd vdd` 5/6 dummy in the pad's PBN slot (already in the netlist); TGP `ni en_3v3_b iref vdd` 1/0.45 |
| `rb_tails` | `s2d_tails_hi_f` / `s2d_tails_c3`, cut to two tails with the row's end dummies | TR `ts vbp vdd vdd` 5/6 (the edge detector's copy of a unit tail); BT `bt vbp vdd vdd` 5/6; dummies 5/6 at both ends, one NWell on vdd |
| `rb_tubs` | `tub_p20x1_c3` in a row as in `s2d_inputs_c3`, with the row's dummy tubs at both ends | MR `gh gh ts ts` 20/1 ng=2 (diode; bulk = source ts); BA `bd m bt bt` 20/1 ng=2; BB `vcm vcm bt bt` 20/1 ng=2 (bulk = source bt); each tub its own NWell, identical copies |
| `rb_avg` | new: three small "tubs" after `tub_p20x1_c3`'s construction (own NWell, butted source tie, identical gate-to-well distance on all sides) | SU `m m gh gh` 1/4; SL1 `xp xp m m` 1/4; SL2 `xp xp m m` 1/4 (SL1 / SL2 in parallel, SU in series above them; the 1/4 finger is the pad's `pmosHV_w1_l4` of `s2d_loads_f` / `s2d_casc_p_f`) |

Notes:
- TR and BT replicate the unit tails: same finger, same neighbors as in the pad's tail row; if a symmetric four-wide
  row (dummy, TR, BT, dummy) is not what the pad's row structure gives, say what is closest and why.
- The tubs: MR replicates a unit input device (gate = drain here); BA / BB are the same device in vcm_rb's buffer.
  Reproduce the pad tub exactly; only the nets differ.
- `rb_avg` has no pad counterpart: keep it minimal and symmetric (SL1 / SL2 mirror-symmetric about SU's axis).
