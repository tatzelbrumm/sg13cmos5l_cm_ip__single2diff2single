<!-- SPDX-FileCopyrightText: 2026 Christoph Maier / SPDX-License-Identifier: Apache-2.0 -->
# bias_dist_pd layout: note (Claude, agent D, C4 2026-11-07)

[M] = measured by a tool run (logs/summary.txt), [R] = reasoning. Rebuild: `python3 build_bdp.py .` (byte-identical
gds, sha256 5927e632941b [M]); checks: `sh run_checks.sh <run dir>`.

## Structure (previews/bias_dist_pd.png)
- **bdp_mirror_n** `D | NI NM | D` (6u/6u, end dummies 2u/6u), top left: N's `sink_block()` from build_rb_n.py
  executed unchanged, the rb_mirror call with gate ni and band tracks vpd / ni. All-layer XOR against N's rb_mirror 0
  [M]. Placed mirrored, band facing the switches.
- **bdp_mirror_p** `D | PO0 PO1 PD PO2 PO3 | D` (5u/6u), top right: build_rb_p.tails() (F's tails_row, C3's P helpers
  imported unchanged) with seven devices, PD (diode) in the middle. Rows XOR 0 against P's rb_tails on Activ, GatPoly,
  Cont, pSD, NWell, TGO, M1 at the left row end [M]; the ring strips are longer (Cont XOR 1.18 um2 from the centered
  contact rows). Changed: gate net vpd, edge stub on the left, PD's drain -> M1 lane 0.22 under the ring -> M2 riser
  -> the stub (no contact in the middle of the gate bar).
- **Switch row** (one standard-cell row, M1 tie strips vss bottom / vdd top, one NWell): under the N mirror four
  input slices and TDN; under the P mirror an output slice below each PO's drain pad, SVPD below PD's.
- **Channel** between mirrors and row: M1 tracks T0 (ni left, vpd lane right), T1..T4 (iin0..3 to the left edge,
  iout0..3 to the right edge); M2 only vertical (slice risers, po lines into the PO pads, SVPD into PD's pad, the ni
  drop from the N band, two supply straps). Metal1 / Metal2 only.

## Cells and the cut (README option B, by slice)
- `nand2_hv` PMOS ng=2 (vdd a y b vdd) over NMOS ng=2 (y a n1 b vss); `inv_hv` ng=1 pair; `tg_hv` TGP over TGN,
  1u/0.45u, one well and tie. Gates contacted on poly (pads 0.45 wide, bars >= 0.39 [M]). Each is DRC / maximal+LU /
  LVS clean alone [M]; in the row nand2_hv and inv_hv share the vdd / vss stripe (Activ overlap 0.30).
- `bdp_slice` = nand2_hv | inv_hv | tg_hv, 4.38 um pitch x 5.79 um: e_b reaches TGP's gate by a poly bridge, e
  reaches TGN's gate by a poly bar; only en (M2 down), en_3v3 (line) and io_a / io_b (M2 up) leave it.
- Why B [R]: the 16 logic-to-switch nets stay inside their slice (< 3 um, in poly / M1), one cell serves all eight
  legs, the switches share the logic's well and ties (rule 6), and the matched devices stay in their two rows.
  Option A would route those 16 control nets across the cell.

## Area [M]
982.4 um2 (60.49 x 16.24). Device rows: N mirror 181.1, P mirror 365.9, switch cells 218.6 (8 slices + TDN + SVPD
at their pitch x 5.79): sum 765.6 -> 1.28. With the row's fillers (59.25 x 5.79 = 343.1): 890.1 -> 1.10. The row
length is set by the P mirror; 6.4 and 7.5 um of it are filler (ties only).

## Dummies (backannotation, d g s b)
- bdp_mirror_n: MDN0, MDN3 hv nmos 2u/6u `vss ni vss vss` (rb_mirror's MDM0 / MDM3).
- bdp_mirror_p: MDP0, MDP6 hv pmos 5u/6u `vdd vpd vdd vdd` (rb_tails' MDT0 / MDT3).
- No dummies in the switch row. No W, L, ng or finger split changed; 73 circuit devices + 4 dummies in the CDL.

## Checks [M]
run_drc.py --no_density 0 (no "exception"), maximal + latchUpRules 0, flat LVS match (bias_dist_pd and each of the
8 cells alone); negative LVS (TIP0 gate ei0_b -> ei0) does not match; supply metal (tie Activ, Cont, M1, Via1, M2,
no well / substrate) gives exactly 2 nets, vddh and vssh; sym_check bdp_mirror_n 0, bdp_mirror_p Cont 0.0384 um2 in
PD (the middle 5/6 PCell's own 5 nm contact flooring, the residual P reported for rb_tree_p).

## Open points
1. Output order: PO0 (S2D) / PO3 (spare) are the outer pair, PO1 (D2S) / PO2 (pad_ref_rb) the inner pair next to
   PD. Which two loads should share the inner pair? Any permutation is a change of the drain lines only [R].
2. sym_check's narrow-poly heuristic flags the split TG gates (tg_hv 2, slice 1): the 1.24 um gap (NW_c1 + NW_d1)
   leaves 0.14 um of each 0.45-wide pad beyond its endcap zone. The contacted poly is >= 0.39 wide [M]; a 0.04 um
   taller row would clear the heuristic.
3. The switch row has tie strips at its top and bottom, not a closed ring (the mirrors keep their closed rings).
4. Pins: iin / iout on Metal1 at the edges, en_3v3 on Metal1, the other enables on Metal2 (pin_map.md).
5. N's band tracks keep their left pin stubs (about 1.5 um of M2 beyond the ring), unchanged generator code.
6. No PEX; placement in slot7 is left to the assembly (inputs left, outputs right, enables bottom, supplies top).
