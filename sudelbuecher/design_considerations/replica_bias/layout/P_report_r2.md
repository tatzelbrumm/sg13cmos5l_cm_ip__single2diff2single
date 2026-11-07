<!-- SPDX-FileCopyrightText: 2026 Christoph Maier / SPDX-License-Identifier: Apache-2.0 -->
# P (C4) round 2: dummy small tubs in rb_avg (2026-11-07, 21:00–21:08 CET)

Claude (Opus 5.5), agent P. [M] = measured, [R] = reasoning. This report adds to `P_report.md` (round 1).

Christoph: "apply dummies ... try to reproduce the dummy structures in the pads for matching". Tub order D MR BA BB D: unchanged.

## What changed

**rb_avg** is now `D | SL1 | SU | SL2 | D`, 36.80 × 3.23 µm (69.0 → 118.9 µm²).
- **The dummies:** the same small-tub cell `rb_tub_p1x4`, at the same pitch (5.92 + NW.b1 1.80), each in its neighbor's
  orientation: the right one R0 like SL2, the left one M90 like SL1. The row stays mirror-symmetric about SU's axis.
- **Built as the pad's dummy tubs** (`P.inputs()` builds them relative to `tub_p20x1_c3` with the same scheme):
  - one M1 box from the Activ top to the vdd track + 0.145, inset 0.07 from the Activ ends, over the gate pad and both
    stripe ends, so g = d = s;
  - a Via1 row 0.43 inside the box ends;
  - an M2 vdd track crossing the row at the gate-pad height (y 1.30 in the tub frame, as the pad's band track sits at
    the pad's gate pads);
  - the source plate over the tie gives bulk = vdd.
- **Unchanged:** the separate tie (pSD.i1 / pSD.f) and the tub's gate-to-well distances (0.96 / 0.62 / 1.35).
- **New pin:** vdd M2 (0,2.52;0.5,2.78), with the track spanning the cell. Other pins moved by +7.72 in x:
  - m M1 x 14.41–14.67 and 22.13–22.39 (bottom);
  - gh M1 x 16.13–16.80 (bottom);
  - xp M1 (17.90,2.97;18.90,3.23).
- **Port order:** `rb_avg gh m vdd xp`.

## Checks [M]

| check | result |
|---|---|
| rb_avg DRC (run_drc.py --no_density) | 0 violations, no "exception" |
| rb_avg LVS (--disable_tap_extraction, CDL with MDA0 / MDA1) | match, 0 warnings. Extracted: the two dummies all on vdd (merged, W = 2), SL1 ‖ SL2 xp xp m m, SU m m gh gh |
| sym_check rb_avg (axis x = 18.40 = SU's center) | max mirror XOR 0, 0 narrow-poly hits |
| LU | 1.45 µm (LU.a 20) |
| surroundings (`logs/surround.py`): device layers within ± one pitch of SL1 and of SL2, against SU's | XOR 0 (round 1: 58.05 µm², the missing neighbor) |
| rb_tree_p, rb_tails, rb_tubs, rb_tub_p20x1, rb_tub_p1x4 against round 1 | all-layer XOR 0, CDL identical; the round-1 DRC / LVS / sym / LU results stand |
| pad comparison (`compare_pad.py`) | output identical to round 1. rb_avg has no pad row, and its finger is still XOR 0 against the pad's `pmosHV_w1_l4$1` |
| reproducibility | two builds byte-identical (gds bf7c0f57ab8f) |

## Netlist (your backannotation)

- **MDA matches as stated:** hv PMOS 1u/4u ng=1, D = G = S = B = vdd.
  - My CDL calls them MDA0 (left, next to SL1) and MDA1 (right, next to SL2). Any mapping to MDA[0] / MDA[1] works for
    LVS.
- **MDT and MDU:** unchanged from round 1. MDT0 / MDT3 = 5u/6u, vdd vbp vdd vdd; MDU0 / MDU4 = 20u/1u ng=2, all vdd.

## Files (P/out, sha256 first 12)

- bf7c0f57ab8f rb_p_cells.gds
- 4cea9a38170e rb_p_cells.cdl
- bf16530537f7 build_rb_p.py
- 874063e7aff4 build_s2d_p3.py (unchanged C3)
- f9f49d7555bd compare_pad.py
- PNGs:
  - fc749f93488e rb_avg.png
  - f50303fd30f3 rb_avg_su_sl2_dummy.png (it replaces rb_avg_su_sl2.png)
  - the others are unchanged.
- logs/:
  - check_summary.txt (rounds 1 and 2);
  - drc_rb_avg.log, lvs_rb_avg.log, sym_rb_avg.txt, lu.txt;
  - surround.py, surround_rb_avg.txt;
  - compare_pad.txt.
