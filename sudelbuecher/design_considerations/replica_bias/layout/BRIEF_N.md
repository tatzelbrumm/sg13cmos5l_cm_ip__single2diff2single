<!--
SPDX-FileCopyrightText: 2026 Christoph Maier
SPDX-License-Identifier: Apache-2.0
-->
# Brief N: the NMOS rows and the capacitors of pad_ref_rb

Read `BRIEF_common.md` first. Your workspace: `N/` (this folder's `N/work`, `N/out`). Start from C3's N
(`.../agents_c3/N/out/build_s2d_n3.py`, `report.md`) and reuse its code.

| cell (deliver as `rb_<name>`) | copies (S2D pad) | devices (netlists; D G S B) |
|---|---|---|
| `rb_tree_n` | `bias_tree_noab_n_c3` as drawn, rewired, extended by slots on the same gate bar | TGN `iref en_3v3 ni vss` 1/0.45; TDN `ni en_3v3_b vss vss` 1/0.45; NI `ni ni vss vss` 6/6; SY `xp ni vss vss` 6/6 (in the pad's NBP 6/6 slot; replicates the fold sink SY, 5 uA); NBP `vbp ni vss vss` 2.4/6 (the pad's NBPC slot); SH1 `gh ni vss vss` 2.4/6 (the pad's dummy 2.4/6 slot); SH2 `gh ni vss vss` 2.4/6 (new slot); SF `vref ni vss vss` 2/6 (every device gated by ni together; or the mirror row, your call with reasons) |
| `rb_casc` | `s2d_casc_n_f` / `s2d_casc_n_c3`, cut | CY `vdd vbnc xp vss` 15/3 and F1..F4 `vdd vbnc vref vss` 15/3 (all five copy the fold cascode CX / CY: gate vbnc, drain vdd); BNC `vbnc vbnc vss vss` 1/8 diode in the middle as in the pad; the row's 2/3 end dummies |
| `rb_mirror` | `sinks_6x6_s2d_c3_core` (6/6 fingers), cut | BD `bd bd vss vss` 6/6 diode; BM `vcm bd vss vss` 6/6; the row's end dummies (2/6) |
| `rb_cload` | `s2d_cload_c3` | CB `vss vcm vss vss` 12/12 (vcm_rb's own capacitor) and the two pull-downs in its TPN / TNN slots: SPD of vcm_rb `vcm en_3v3_b vss vss` 1/0.45, SPD of vref_s2d_rb `vref en_3v3_b vss vss` 1/0.45 |
| `bypass_rb` | the capacitor of `s2d_cload_c3` (12/12 hv NMOS, gate up to the node), arrayed | a **parametric** generator: `ncm` capacitors on vcm, `ncr` on vref (defaults 4 and 8, as in the netlist), S / D / B on vss; the cell's pins vss, vcm, vref; write the CDL with the same parameters. Make the array shape a parameter too (rows × columns), and choose a default that suits a compact block |

Notes:
- The tree row is the pad's own row: keep its geometry, gate bar and tie; added slots extend the row symmetrically
  (a new device in the middle, or a matching pair / dummies at both ends).
- CY and F1..F4 replicate the pad's 15/3 cascode fingers, BNC sits next to them as in the pad: keep the pad's
  orientation and spacing; five fingers in the pad's two-level arrangement or one level, your call with the area.
- The capacitors need no matching; the pull-downs are switches (share well and tap with their neighbors).
