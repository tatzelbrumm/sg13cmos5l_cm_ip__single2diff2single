<!--
SPDX-FileCopyrightText: 2026 Christoph Maier
SPDX-License-Identifier: Apache-2.0
-->
# P (C4): PMOS rows of pad_ref_rb (2026-11-07, 20:30–20:57 CET)

Claude, agent P. [M] = measured by a tool run, [R] = reasoning. Saved by the lead from the agent's hand-back (the
agent's own write of `out/report.md` was refused); Christoph asked for it to be kept as a file.

**Code.** `build_rb_p.py` imports C3's `build_s2d_p3.py` as a library (copy unchanged, sha256 874063e7aff4 = agents_c3/P/out;
run alone it reproduces C3's gds byte for byte, b456862ae015) [M]. Every row is the pad row's own generator code with
other device lists / nets. Two runs give byte-identical files (gds 3811e8adfc9d) [M]. Pad comparison: `compare_pad.py`
XORs each row against the drawn s2d pad (`sg13cmos5l_IOPadSingle2Diff.klay.gds`), output `logs/compare_pad.txt`.
Checks: `logs/check.sh`; the brief's sym_check path (agents_c3/F/work/B4/inputs) is a dangling link, so
`design_considerations/pad_buffer_layout/pad_cell_2026-10-31/sym_check.py` was used (reproduces C3's logged results for
the tub, 0, and the tree, Cont 0.0384) [M]; LU = C3's `lu.py`.

## Checks [M] (round 1, final: nothing to fix)

| cell | size µm | area µm² / pad counterpart | DRC | LVS | sym_check (X, one row) | LU µm |
|---|---|---|---|---|---|---|
| rb_tree_p | 12.94 × 10.37 | 134.2 / 134.2 (bias_tree_noab_p_c3) = 1.00 | 0 | match | Cont 0.0384 (= the pad's) | 3.55 |
| rb_tails | 24.19 × 9.16 | 221.6 / 413.9 (s2d_tails_hi_f, 8 devices) = 0.54 | 0 | match | 0 | 3.67 |
| rb_tubs | 28.70 × 11.97 | 343.5 / 1258 (s2d_inputs_c3, 16 tubs) = 0.27 | 0 | match | 0 | 10.45 |
| rb_avg | 21.36 × 3.23 | 69.0 / none (README estimate 124) | 0 | match | 0 | 1.45 |

DRC `run_drc.py --no_density --mp=4`: "No DRC violations detected" in every log, no "exception". LVS `run_lvs.py
--disable_tap_extraction`, flat, 0 warnings; extracted devices carry the netlist terminals. Total 768 µm² (README
estimate 879). sym_check residual of the tree = the same box as in the pad cell, (4.40,2.63;8.54,9.17), the 5/6 PCell's
own 5 nm contact flooring (known C3 residual).

## Per cell: identical to the pad / different (all XORs [M])

**rb_tree_p** = `P.bias_tree()` line by line; row `PBNC 2/6 | MDPBN 5/6 (dummy, PBN slot) | BP 2/6 (diode, dummy slot)`,
TGP below. Identical: all device layers (Activ, GatPoly, Cont, pSD, NWell, TGO XOR 0), ring, gate columns, vbp stub, TGP,
every pin except vbn. Different (metal only): PBN's drain pad / M2 / vbn pin removed, MDPBN's drain into the ring strip
like the pad's dummy; the dummy slot's drain-to-ring M1 becomes BP's diode lane into its own gate column (the pad tails'
BP lane, mirrored, −0.29…−0.03, 0.24 below the ring strip). XOR M1 2.14, M2 1.59, Via1 0.11, M2pin 0.33 µm². TGP drawn as
in the pad; the CDL lists it d = ni, s = iref as pad_ref_rb.spice.

**rb_tails** = F's `tails_row()` (it built the pad's s2d_tails_hi_f / _lo_f from P's tails()) with 4 devices `D | TR BT | D`.
Left half (D TR) against _lo_f's left end (D A2b), right half (BT D) against _lo_f's right end (M2a D) and _hi_f's
(M2b D): identical on every layer, metal and pins included, except that the ring's top and bottom strips are 21.0 µm
shorter (22.95 vs 43.95), so their centered contact rows shift (Cont XOR 0.78 µm² per half; 0 without the two strips).
vbp stub at the right end as in both pad rows. The pad has no 4-wide row; D TR BT D reproduces the ends of
s2d_tails_lo_f (dummy at both ends) around two units; TR and BT each have a 5/6 neighbor on both sides, abutted gate
strip, one NWell on vdd, as every pad tail.

**rb_tubs** = five `P.tub()` (= the pad's tub_p20x1_c3 with its labels removed, as in the pad: XOR 0 on every layer) at
s2d_inputs_c3's pitch 6.10, the pad's lower-row orientation: `D | MR BA BB | D`. Device layers XOR 0 against the first
five tubs of the pad's lower row. Metal: the band holds only vdd (dummy gates, the pad's Via1 scheme); the gate tabs
(the pad's, on the right head) go straight up to M1 pins on the top edge; the diodes MR and BB get a 0.44 × 0.40 M1 strap
from the drain stripe end to both gate pads (over the poly bridge); BA's drain tab runs on to the bottom edge, crossing
the tie without contact, as the pad's tab; bt: one M2 link between BA's right and BB's left source plate on the pad's
first under-row track (y −0.95). Order as the README plan: BA, BB adjacent (6.10 apart) halves their gradient term
against BA MR BB; all five are the same tub, so the device layers are mirror-symmetric.

**rb_avg** (new) `SL1 | SU | SL2`, SL1 the M90 image of SL2 about SU's axis. Small tub `rb_tub_p1x4`: the pad's
pmosHV_w1_l4 finger (XOR 0 against `pmosHV_w1_l4$1`), upright, built as the tub: 4.0 × 0.56 gate head with one contact
row, N+ tie 0.43 below the Activ (pSD.i1 0.40 + pSD.d1 0.03) with the source plate over it, NWell and TGO 0.62 beyond
(NW.c1, NW.e1), drain-to-gate-pad M1 strap (diode). Against the brief [R]: not butted (a butted tie needs ≥ 0.40 P+
beyond the gate, pSD.i1, plus ≥ 0.30 N+, pSD.f, but the PCell's source is 0.34; that would mean adding Activ to the
device), so the tub's separate tie; gate-to-well distance as in the tub, not equal on all sides (0.96 left / right, 0.62
top, 1.35 on the tie side), identical in all three; tie contacts along its whole length. Wiring M1 only: m from SU's gate
pad out to both NWell gaps and down them onto SL1's / SL2's ties (their sources); xp: the SL gate pads joined over SU,
0.22 above it (M1.e). No dummies (symmetric without).

## Pins (cell frame, µm)

- rb_tree_p: vbnc M2 (2.165,10.07;3.275,10.37); vbp M2 (0,5.75;0.5,6.05); vdd M1 (0.62,3.06;0.92,5.06); bottom M1: iref
  x 5.875–6.135, en_3v3_b 6.34–6.60, ni 6.805–7.065.
- rb_tails: M2 bottom: ts x 8.915–10.025, bt 14.165–15.275; vbp M2 (23.69,4.32;24.19,4.62); vdd M1 (0.62,1.63;0.92,3.63).
- rb_tubs: top M1 (y 11.67–11.97): gh x 8.54–9.24, m 14.64–15.34, vcm 20.74–21.44; bottom M1: ts x 6.79–7.46, bt
  12.89–13.56 and 18.99–19.66, bd 13.795–14.905; vdd M2 (0,11.52;0.5,11.78), track spans the cell.
- rb_avg: bottom M1: m x 6.69–6.95 and 14.41–14.67, gh 8.41–9.08; xp M1 top (10.18,2.97;11.18,3.23).

## Netlist consequences

No change of W, L, ng, finger split or device order. Dummies to backannotate (d g s b): rb_tails MDT0, MDT3 5u/6u
`vdd vbp vdd vdd`; rb_tubs MDU0, MDU4 20u/1u ng=2 `vdd vdd vdd vdd` (the pad's dummy tubs); rb_tree_p MDPBN already in
bias_tree_rb; rb_avg none.

## Open questions for Christoph

1. rb_avg: dummy small tubs at both ends ("best" under rule 1, about +15 µm width)? Butted tie, or equal gate-to-well
   distance on all four sides (1.35 µm surround: 24.8 instead of 17.6 µm² per small tub)?
2. rb_tubs: keep `D MR BA BB D` (pair adjacent, better against gradients), or `D BA MR BB D` (pair mirror-symmetric
   about MR, twice the distance)?

## Lead's note (2026-11-07, after Christoph's answers)

1. Christoph: "apply dummies; there's plenty of room at slot7 bottom. try to reproduce the dummy structures in the pads
   for matching." -> rb_avg gets dummy small tubs at both ends (round 2); MDT, MDU, MDA backannotated into vcm_rb.
2. Christoph: "I trust your tub order judgment ... at least until I get around to review it ex post facto." -> keep
   `D MR BA BB D`.
