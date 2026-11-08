<!-- SPDX-FileCopyrightText: 2026 Christoph Maier / SPDX-License-Identifier: Apache-2.0 -->
# D report (C4): layout of bias_dist_pd, shared bias option (Claude, agent D, 2026-11-07, 23:32-23:58 CET)

[M] = tool result (`layout_rb/D/out/logs/summary.txt`), [R] = reasoning. Everything is in `layout_rb/D/out/`; the
full note follows below. No action was refused or blocked except one `rm -rf` of the (already empty) out/ folder,
which the safety check stopped; it was not needed and not repeated.

## Summary
- `bias_dist_pd.gds` (top cell bias_dist_pd), 60.49 x 16.24 um = 982.4 um2, Metal1 / Metal2 only [M].
- run_drc.py --no_density 0 (no "exception"), maximal + latchUpRules 0, flat LVS match against `bias_dist_pd.cdl`
  (composed by script from bias_dist_pd.spice + hv_logic.spice: 73 devices + 4 dummies); negative LVS fails as it
  should; the same three checks pass on each of the 8 cells alone [M].
- Matched rows from the precedent generators: `D NI NM D` = N's rb_mirror code (all-layer XOR 0 [M]);
  `D PO0 PO1 PD PO2 PO3 D` = the tail-row code with the diode in the middle (row layers XOR 0 against rb_tails' end [M]).
- Cut: option B (one slice nand2_hv | inv_hv | tg_hv per leg), all slices in one standard-cell row under the mirrors.
- Dummies to backannotate: MDN0 / MDN3 nmos 2u/6u `vss ni vss vss`; MDP0 / MDP6 pmos 5u/6u `vdd vpd vdd vdd`.

## Files (out/, sha256 first 12)
- 5927e632941b bias_dist_pd.gds, fe9f7d25d4d9 bias_dist_pd.cdl, f109b5349acd build_bdp.py, 9927dfe21dc5 bdp_cells.py,
  f27c98affec1 run_checks.sh, e3ab80fcb184 check.sh, cd3e79e89807 extra.py; build_stdout.txt
- cells/: nand2_hv, inv_hv, tg_hv, bdp_slice, bdp_tdn, bdp_svpd, bdp_mirror_n, bdp_mirror_p (.gds + .cdl, labeled
  standalone copies; inside bias_dist_pd.gds their labels are removed, as the pad's tub copy)
- logs/: run_drc / maximal_lu / lvs log per cell, bias_dist_pd_lvs_negative.log, summary.txt
- previews/: bias_dist_pd.png (inner nets annotated), closeup_input_slice, closeup_pd_svpd, closeup_left_edge,
  closeup_n_p_junction, one PNG per cell
- pin_map.md, note.md

---
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

## Round 2 (2026-11-08): gate pads away from the channels (Christoph: "we're not short of area, so move the pads away from the channels so the check passes")
- **Change:** the switch-row gap is 1.44 instead of 1.24 um (PMOS Activ 3.17..4.17, vdd strip 4.60..4.90,
  NWell 2.55..5.52). TGN / TDN pads and the e bar now span 1.80..2.30 with contacts at 2.04; TGP / SVPD pads and the
  e_b bridge span 2.55..3.10 with contacts at 2.66. Every contacted piece reaches 0.32 (lower) / 0.37 (upper) beyond
  the 0.25 endcap zone. The full-width 0.45 gate pads are kept (no necks). The channel tracks, the mirrors and every
  pin above the bottom edge moved up 0.20 um.
- **Unchanged:** both mirrors are byte-identical to v1 (cells/bdp_mirror_n.gds, bdp_mirror_p.gds). The pin edges and
  the netlist are also unchanged. Round 1 is kept in out/v1/.
- **Size [M]:** 60.49 x 16.44 um = 994.5 um2 (+12.1). The switch cells are 5.99 um tall (slice 4.38 pitch). The
  device rows sum to 547.0 + 226.2 = 773.2 um2 (ratio 1.29), or 900.5 um2 with the fillers (ratio 1.10).
- **N check [M]** (sym_check.py --no-y): 0 narrow-poly hits on nand2_hv, inv_hv, tg_hv, bdp_slice, bdp_tdn,
  bdp_svpd, bdp_mirror_n, bdp_mirror_p and the flattened bias_dist_pd. Every contacted poly piece outside Activ is
  >= 0.45 um wide.
- **Other checks [M]** (logs/summary.txt):
  - run_drc.py --no_density: 0 violations, no "exception".
  - Maximal deck with latchUpRules: 0.
  - Flat LVS: matches for bias_dist_pd and for each of the 8 cells.
  - Negative LVS: does not match, as intended.
  - Mirror sym_check: bdp_mirror_n 0; bdp_mirror_p Cont 0.0384, the same residual as round 1.
  - Metal-only supply check: 2 nets, vddh and vssh.
  - Rebuilds are byte-identical (gds c0b3d4af3145). Previews are redrawn.
- **Netlist:** the source now carries the dummies (XMDN[0..1], XMDP[0..1], backannotated by the lead). The CDL takes
  them from there instead of adding its own: 73 devices + 4 dummies, unchanged in substance (CDL 80211713f27c).
  Output roles follow the source (iout0 = pad_ref_rb, iout1 = S2D, iout2 = D2S, iout3 = spare), so open point 1 is
  settled: both pads sit on the inner pair. Open point 2 is resolved.
