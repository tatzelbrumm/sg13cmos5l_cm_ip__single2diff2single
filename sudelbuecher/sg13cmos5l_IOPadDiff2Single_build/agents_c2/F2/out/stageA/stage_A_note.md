<!--
SPDX-FileCopyrightText: 2026 Christoph Maier
SPDX-License-Identifier: Apache-2.0
-->
# F2 stage A: placement of the d2s / bias-tree block and the 2 kΩ stages in the pad top (C2, 2026-11-03, 13:24–14:05 CET)

Agent F2 (Claude Opus 5.5). [M] = measured by a tool run, [R] = reasoning. Picture: `previews/placement_A.png`.
Everything rebuilds with `sh src/run_A.sh <dir>`; two rebuilds give the same bytes, equal to the checked files [M].

## Summary

- 15 placements, unrouted: 5 cells as drawn by P2 (inputs, tails, loads, casc_p, pd_p), 8 reworked copies `*_f2`, and the
  new 2 kΩ stage `d2s_sp2k_f2` twice (CMA's at the left edge, CMB's mirrored at the right edge, lead's message of today).
  Every changed / new cell: IHP DRC clean (main + maximal incl. latch-up; the stage also with antenna), 0 exceptions,
  IHP LVS match, sym_check as below [M]. Whole placement (pad + F's reused pad-top cells + block), DRC incl. latch-up and
  antenna: clean [M] (`logs/placement_A_drc.log`).
- Bottom row on the a / b joins: CMA stage | loads | ab_p (+pd_p) | ab_n | pd_n | CMB stage. Column A (PMOS): casc_p,
  tails, inputs, bias_tree_p. Column B (NMOS / R): casc_n (R90) | sinks (R90), rhigh, bias_tree_n (TGN / TDN facing TGP).
- Cells 4931 µm² of 6789 µm² (envelope x 2.5–77.85, y 88.3–178.4), free 1858 µm² (27 %) [M]. The bias tree is placed
  first; the stages took the old CMB reserve and a column at the left edge (column A moved right by 9.7 µm at the bottom).

## Reworked cells (`cells/d2s_f2_n_cells.*`, `cells/d2s_f2_p_cells.*`)

| cell | was (µm) | now (µm) | changes |
|---|---|---|---|
| d2s_pd_n_f2 | 4.73 × 2.95 | 3.04 × 2.56 | redone as the NMOS twin of pd_p: upright SB / SABN, mirror images, drains inside, one M1 gate bar on full-width heads; tie only as long as the row; b / vabn = M1 + 2 Via1 + M2 pad on the drain itself (no stubs); vsso on M1 to the left edge (no M2) |
| d2s_ab_n_f2 | 20.68 × 4.02 | 9.78 × 6.74 | redone as the NMOS twin of ab_p: upright D FNL RN2 ABN D (4.4/1), same stripe order as ab_p (l2 l1, vabn dabn, a b), pins on M1 at the bottom edge at ab_p's pin height; vabn bar over all head contacts, M2 out over the tie; **dummies D = S = G = vss** (were vabn; ab_p's convention, open decision 3) |
| bias_tree_n_f2 | 30.26 × 8.59 | 28.27 × 8.84 | row unchanged (device-layer XOR vs N2 in the row window 0 [M]); TGN / TDN moved together to the left end (TDN on the tie, TGN above, shared ni bridged to the gate column; iref on M2 out across the tie edge) |
| bias_tree_p_f2 | 18.19 × 9.32 | 19.53 × 8.14 | row unchanged (XOR 0 [M]); TGP moved from under the row centre to the right end outside the tie, gate head down |
| d2s_ab_p_f2 | 8.48 × 9.00 | 9.50 × 9.00 | well tap: the top strip became a U (strip + legs beside the end dummies down to the pin edge); devices unchanged (XOR 0 [M]) |
| d2s_rhigh_f2 | 13.80 × 17.29 | 13.80 × 18.11 | closed p+ ring: top / bottom legs beyond the link levels |
| d2s_casc_n_f2 | 40.70 × 12.41 | 40.70 × 12.41 | closed p+ ring: Activ ties under N2's M1 joiners |
| sinks_6x6_f2 | 51.68 × 16.51 | 52.28 × 16.51 | ring enclosing the whole array: legs one tie width outside the tie ends (+ TGO over them) |

Ring cells: additions only (no shape of N2's removed [M]). Netlists as N2 / P2 except the ab_n dummies.

## New: d2s_sp2k_f2, the 2 kΩ secondary stage (`cells/d2s_f2_sp_cells.*`, 7.86 × 14.71 µm)

IHP's `sg13cmos5l_SecondaryProtection` (io library) redrawn from SG13_dev PCells with IHP's distances, stretched by
5.435 µm along the resistor: rppd w 1 / l 7.435 (PCell reports 1991.6 Ω, as K) in its own p+ ring, pad head at the
bottom (M2 pad pin at the bottom edge), core head at the top; dantenna 0.64 × 3.1 beside it in its own p+ ring (iovss);
dpantenna 0.64 × 4.98 above in an NWell with an n+ ring (iovdd), NWell 0.62 beyond it; core on M2 to both diodes.
DRC clean incl. latch-up and antenna (round 3; rounds 1–2: off-grid diode position and via / contact rounding, then M1.c1
inside the diode PCells, fixed by IHP's longer diode Metal1), LVS match: `R pad core iovss rppd`, `D iovss core dantenna`,
`D core iovdd dpantenna` [M] (`logs/sp2k/`). Placed at x 2.5 (CMA) and mirrored at x 69.99 (CMB), y 88.3: pad pins at
x 4.14–4.98 and 75.37–76.21, straight above the pad combs, between F's isolator taps; each stage keeps its own NWell and
guard rings 1.8 µm (NW_b1) from the circuit's wells.

## Checks of the reworked cells (round 2 = final; `logs/checks_round2.txt`, per cell `logs/r2/<cell>/`)

| cell | DRC | LVS | sym_check |
|---|---|---|---|
| pd_n, ab_n, ab_p, rhigh, casc_n | clean | match | 0, 0 necks (ab_n / pd_n / ab_p --no-y) |
| sinks_6x6_f2 | clean | match | X Cont 0.0768 (BN + twin on the axis, the 6/6 PCell's own, as N2), 0 necks |
| bias_tree_n_f2 / _p_f2 | clean | match | residual only in the moved switch block (`sym_rowaxis.txt`); rows XOR 0 against N2 / P2 (`logs/unchanged_parts_xor.txt`) |

Round 1 found and fixed: ab_n vabn bar not covering the outer contacts of the 1 µm heads (M1.c / c1, Cnt.h); ab_p leg
contacts 0.14 from the strip's (Cnt.b); sinks legs 0.07 (Gat_d) from the end gate-column fill, flagged 4× by sym_check's
neck test (legs moved out). Placement: NW.b1, TGO.e, M2.b → abutment, TGO_e spacing, one NWell bridge (the inputs'
lower-left dummy well to the left edge stub's iovdd well), pd_p's vabp pad on ab_p's vabp pin.

## Placement (`placement_A.gds`, `placement_A.tsv`)

| block | cells (µm²) | area µm² |
|---|---|---|
| PMOS | loads 419.5, ab_p 85.5, pd_p 11.0, casc_p 487.5, tails 513.8, inputs 1081.9, bias_tree_p 159.0 | 2758 |
| NMOS / R | ab_n 65.9, pd_n 7.8, casc_n 505.1, rhigh 249.9, sinks 863.1, bias_tree_n 250.0 | 1942 |
| 2 kΩ stages | 2 × 115.7 | 231 |
| d2s_mpdda_pd / bias_tree_pd | | 4291 / 409 (phase-1 estimate 3430 / 380) |

Why this order [R]: a / b / l1 / l2 / dabp / dabn meet in the bottom row on the joins; casc_p over loads (pl / pr / l2);
tails (M0) under the inputs so sb_B, sa_C1, sa_C2, sb_A face each other, rhigh (M0, terminals down) beside that gap;
x / y: inputs' right edge, casc_n and sinks side by side; bias trees at the top next to iref / en pins, drains down;
the stages at the two pad edges, mirror images, each over its capacitor's half of the pad.
Free (largest [M]): top left 21.4 × 13.4 (core-pin lines), above sinks 16.5 × 13.8, above rhigh 13.8 × 8.8, between
casc_p / tails and casc_n 7.9 × 20; column-A gaps 2.5–4.8 high (routing channels).

## CMA / CMB, turned, behind the stages (lead's messages of today; wiring is stage B)

Sheet change for the backannotation (pad level, `sg13cmos5l_IOPadDiff2Single.spice`), new nets pcma / pcmb:
```
XCMA a pcma a a sg13_hv_pmos w=7.96u l=32.16u ng=1      (was: XCMA pad a pad pad ...)  gate on the stage node
XCMB pcmb b pcmb pcmb sg13_hv_pmos w=7.96u l=32.16u ng=1 (was: XCMB b pad b b ...)       S / D / well on the stage node
XRA pad pcma iovss rppd w=1u l=7.435u   XDNA iovss pcma dantenna w=0.64u l=3.1u   XDPA pcma iovdd dpantenna w=0.64u l=4.98u
XRB pad pcmb iovss rppd w=1u l=7.435u   XDNB iovss pcmb dantenna w=0.64u l=3.1u   XDPB pcmb iovdd dpantenna w=0.64u l=4.98u
```
Plan for stage B [R]: CMA: S / D / NWell from the pad junction onto `a` (the a join is 36 µm above it), gate head
(y 50.46–50.82) onto pcma from the left stage (≈ 48 µm line, left edge channel, shared with guard_tie / vfb: to be
untangled). CMB: gate head off the pad comb (F's single-via cut point at 72.26 / 72.67, 50.64) onto `b`; S / D / NWell
onto pcmb from the right stage via the right edge channel x 78.0–78.3 (≈ 45 µm); CMB's well, now pad-driven through
2 kΩ, gets its own guard ring (F's cm_rings share one leg between CMA and CMB: to be split, own rings). CMA's ring stays.

## Christoph's question: Metal1 poly contacts in the centre of sinks_6x6

Why [M, from N2's code]: the two centre columns (0.85 µm gaps beside BN in row 1 and its twin T in row 2) are the M1
path for BN's diode connection (drain bridged to the left centre column) and for T's D = S = G = vbn ties, plus Via1
onto the vbn track. The gate itself does not need them (fed from both ends; vbn is a DC bias) [R].
Can they go, keeping rule 2 [R]: yes. Close both gaps to 0.25 (Gat_b1; rows stay mirror images, same end dummies);
BN's band-side drain gets a 3-Via1 tab onto the vbn track like SX / SY onto x / y; T's band-side stripe the same; T's
outer stripe has no M1 path past the neighbours' source plates, so it needs Via1 + an M2 strap across T's own (dummy)
channel to the vbn track. Tying it to the tie instead would make T a second BN diode (ratio change): no.
Gain 1.2 µm of row, no M1 in the array centre. Not done in stage A; your call for stage B.

## Notes for stage B

- One iovdd well: column-A wells merge where cells abut (loads | ab_p | pd_p); casc_p, tails, the inputs' dummy tubs
  and bias_tree_p need NWell bridges across the 2.5–4.8 µm gaps (NW_b1 keeps them off the active tub wells).
- The 4 sa / sb nets that don't face directly (tails' bottom ↔ inputs' top ↔ rhigh): M1 down the inputs' 1.8 µm well
  gaps or the 2.58 µm channel x 43.42–46.0; M3 is free at y 134–140. rhigh's terminals sit at y ≈ 143, 5 µm above the
  tails / inputs gap (moved up with casc_n for the stage row).
- dabp / dabn: ab_p / ab_n pins at x 48.0 / 58.7, F's stubs at x 38.15–39.55: a ≈ 10–20 µm M1 run along y 88.
- pd_p unchanged so far (adapted when routed); its vabp pad on ab_p's vabp pin is the only connection made in stage A.
  The 63/0 TEXT box is deleted in `placement_A.gds`.
- Reused pad-top cells (d2s_cma / d2s_cmb, cm_rings, guard_tie, nw_isolator, edge_stubs): F's `build_pad.py`
  (`src/src_F/`, only the input path changed), covered by the placement DRC [M]; reworked for the turned capacitors and
  re-checked (LVS, probes, row check) in stage B.
