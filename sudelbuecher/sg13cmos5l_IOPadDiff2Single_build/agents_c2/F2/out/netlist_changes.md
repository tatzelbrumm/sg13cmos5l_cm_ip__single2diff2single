<!--
SPDX-FileCopyrightText: 2026 Christoph Maier
SPDX-License-Identifier: Apache-2.0
-->
# F2 stage B: what the pad candidate implies for the sheets and source netlists (backannotation list)

Reference netlists as drawn: `pad_candidate.cdl` (pad level + `d2s_block`), `cells/d2s_block.cdl`, the cells' CDLs in
`cells/`. Each item: sheet / netlist, change, source of the change.

## Pad level (`sg13cmos5l_IOPadDiff2Single.sch` / `.spice`)

1. **CMA / CMB behind identical 2 kOhm stages (v8 polarity, Christoph 2026-11-03).** New nets `pa`, `pb`; new devices
   per stage (IHP's `sg13cmos5l_SecondaryProtection` with a longer resistor):
   ```
   XRA pad pa iovss rppd w=1u l=7.435u          (1991.6 Ohm, PCell value; agent K measured the same)
   XDNA iovss pa dantenna w=0.64u l=3.1u
   XDPA pa iovdd dpantenna w=0.64u l=4.98u
   XRB pad pb iovss rppd w=1u l=7.435u
   XDNB iovss pb dantenna w=0.64u l=3.1u
   XDPB pb iovdd dpantenna w=0.64u l=4.98u
   XCMA pa a pa pa sg13_hv_pmos w=7.96u l=32.16u ng=1     (was: XCMA pad a pad pad ...)
   XCMB b pb b b sg13_hv_pmos w=7.96u l=32.16u ng=1       (was: XCMB b pad b b ...)
   ```
   The "turned" variant sent earlier on 2026-11-03 is withdrawn (lead's message after Christoph's review).
2. **Partition as phase 1 (1.7):** Xd + Xt drawn in the cell (`d2s_block`), Xg / Xc in the slot; ports
   `iovdd iovss vdd vss pad vinp vinn vref iref en_3v3 en_3v3_b`; `vfb` = pad through a Kelvin line from the pad
   junction; Xd's `vdd` / `vddo` = iovdd, `vss` / `vsso` = iovss (vddo and vsso each with its own path to the rail).
   The symbol's port change affects `slot.sch`, the project top and 8 CACE templates (HANDOFF.md, known problem).

## d2s_mpdda_pd (`d2s_mpdda_pd.sch`, `netlist/source/d2s_mpdda_pd.spice`, `units.spice`)

From P2 / N2 (unchanged by F2; their reports):
3. SX / SY `w=36u ng=4` -> 6 x 6/6 each; PL / PR `w=24u ng=4` -> 4 x 6/4 each; PCL / PCR `w=30u ng=2` -> 2 x 15/3 each;
   CX / CY as drawn (2 x 15/3). The input pairs as `tub_p20x1_c2` (2 x 10/1, ng 2, own NWell, bulk = source).
4. The four bias diodes move into d2s_mpdda_pd's cells: BP (tails), BPC (casc_p), BN (sinks), BNC (casc_n); the
   bias_tree_pd sheet without `Xd` (bias_diodes) is what the layout draws.
5. `unit_r2`'s `rl=50.6u` drawn as 4 x rhigh 0.5 / 12.65 in series (internal nodes) + 2 dummy segments (all on vss).
6. Dummies (every one a device): tubs 4 (vdd), tails 3 x 5/6 (D = S = vdd, G = vbp), loads 4 x 1/4 (G = l2),
   casc_p 1 x 1/4 (G = vbpc), ab_p 2 x 6.66/0.6 (all vdd), sinks 4 x 2/6 + twin 6/6 (D = S = G = vbn),
   casc_n 4 x 2/3 (D = S = G = vbnc).
7. SA bulk vddo -> vdd (P2); SB bulk vsso -> vss (N2). Same nets in the pad.

From F2 (new in stage B):
8. **ab_n dummies:** D = S = G = **vss** (2 x 2/1; N2 had vabn). ab_p's convention (vdd). Open decision 3 of the
   handoff (one dummy convention) still open for the other cells.
9. **Switches folded into the class-AB cells:** SA / SABP live in `d2s_ab_p_f2`, SB / SABN in `d2s_ab_n_f2` (same
   devices, same nets). In the sheet: no change; in the hierarchy: `d2s_pd_p` / `d2s_pd_n` are gone.
10. **sinks:** no netlist change (the twin T keeps D = S = G = vbn; tied by a Metal1 strap across its own channel
    instead of the removed center gate columns).

## bias_tree_pd (`bias_tree_pd.sch`, `bias_ref_pd.spice`)

11. TGN / TGP / TDN in one cell `d2s_tgsw_f2` under NI (same devices and nets); TGP's bulk = vdd (the shared iovdd
    well). Dummies: bias_tree_p 1 x 2/6 (D = S = vdd, G = vbp), bias_tree_n 1 x 2.4/6 (D = S = G = ni).

## Not changed

clamp frames (OP / RP1 / RPD, ON / RN1), DCN / DCP, the a / b joins, dabp / dabn: as drawn by A1 / F.
