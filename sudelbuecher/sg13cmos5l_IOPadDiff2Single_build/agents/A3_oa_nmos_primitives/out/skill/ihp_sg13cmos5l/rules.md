<!--
SPDX-FileCopyrightText: 2026 Christoph Maier
SPDX-License-Identifier: Apache-2.0
-->
# Rules followed, IHP sg13cmos5l instances [IHP]

2026-10-28, Claude (Opus 5.5). Numbering as in `../generic/rules.md`. J = `sg13cmos5l_tech_default.json`
("drc_rules"), MAX = `sg13cmos5l_maximal.drc`, ANG = `geometry/3_2_angle.drc`, NWD = `feol/5_1_nwell.drc`.

1. **[IHP]** finger gap = Gat_b1 0.25 (J; MAX Gat.b1 "unrelated 3.3 V GatPoly over Activ"). 10/1 fingers at
   10.25 pitch, 2/1 dummies at 2.25. The earlier worker measured that gaps of 0.36 ... 0.54 fail Gat.b (endcaps
   0.18 + 0.18 leave a sliver) (log 2026-10-26 23:45; not re-measured here).
2. **[IHP]** row pitch = 1.68 (L 1.0 + 2 x 0.34 S/D of the SG13_dev PCell) + Act_b 0.21 (J) = 1.89. Facing
   tracks: 0.21 + 2 x 0.15 (stripe centre inside the Activ) - 0.29 = 0.22 >= Mn_b 0.21 (J).
3. **[IHP]** track 0.29 = V1_a 0.19 + 2 x 0.05 (M2.c1, MAX output text; no json key); pad 0.21 = 0.19 + 2 x V1_c
   0.01; 3-via pad 1.11 = 3 x 0.19 + 2 x V1_b 0.22 + 2 x V1_c1 0.05 (J).
4. **[IHP]** tie: Activ 0.30 = Cnt_a 0.16 + 2 x Cnt_c 0.07; contacts at 0.34 = Cnt_a + Cnt_b 0.18; pSD 0.03
   beyond (pSD_c1, as the ptap1 PCell); M1 0.26 = 0.16 + 2 x M1_c1 0.05; Act_b 0.21 below row X0 (pSD_d 0.18
   + 0.03 and pSD_j1 0.40 are then met, the gate being 0.34 inside). LU_b 20 (J only: `7_2_latchup.drc` is
   included by `ihp-sg13cmos5l.drc` line 463 but absent from this PDK copy); LU_d 6 (J; MAX LU.d1).
   oa_n10: one segment (0.00, -0.51; 35.00, -0.21), farthest N+Activ 18.90 um (row Y top). oa_mcs_c: one segment
   (0.00, 7.48; 30.68, 7.78), farthest 7.48 um.
5. **[IHP]** dummies W 2 / L as the row (the 2026-10-27 convention); strap 1.11 wide over the 2 um dummy.
6. **[IHP]** gate contact 0.18 from the Activ end (M1_b 0.18 > Cnt_e 0.14), bar 0.21, poly tab to 0.41
   (Cnt_d 0.07), three contacts on a 1 um gate (span 0.84 <= 1 - 2 x 0.07); joiner 0.18 outside the bar;
   strap-to-bar 0.625 >= M1_e 0.22 (wide M1, J M1_e_w 0.3, M1_e_cr 1.0).
7. **[IHP]** oa_mcs_c tie 0.43 above MCL = max(Act_b 0.21, pSD_j1 0.40 + pSD_c1 0.03, Gat_c 0.18 + Gat_d 0.07).
8. **[IHP]** MS3 / SKS (R0) in row Y's free end: x from row Y's last Activ + max(Act_b 0.21, Gat_c 0.18 +
   Gat_d 0.07); baseline 0.25 above row X8 (Gat_c + Gat_d); S / D tabs 0.29 wide (rule 15).
9. **[IHP]** tie contact grid anchored at the right Activ edge of oa_n10 (x = 34.77 - k 0.34); oa_mcs_c placed at
   (4.91, -7.99) relative to oa_n10 has the same grid, the same tie y and the vres riser at the same x
   (35.295 ... 35.585): the pair is DRC clean (logs/drc_oa_n_pair.txt).
10. **[IHP]** pins: `Metal1.pin` 8/2 + `Metal1.text` 8/25, `Metal2.pin` 10/2 + `Metal2.text` 10/25, text at the
    box centre; device names on `TEXT` 63/0 (ignored by DRC / LVS). Nothing on Via2 / Metal3 or above.
11. **[IHP]** TGO outline = Activ + TGO_a 0.27 united with the PCells' own TGO, closed at TGO_e 0.86 (oa_n10: one
    14-vertex polygon). ANG: Cont / Via1 orthogonal only; Activ, GatPoly, Metal1-4 0/45/90 deg; NWell, pSD,
    ThickGateOx only "no acute angle below 87 deg": non-rectangular, even non-45 outlines are legal.
12. **[IHP]** no NWell drawn. An n+ ring in its own NWell next to HV NMOS would cost NW_d1 0.62 + NW_e1 0.62 +
    0.30 + NW_e1 0.62 = 2.16 um per side, against Act_b 0.21 + 0.30 = 0.51 um for the p+ segment; wells of one
    rail merge below NW_b 0.62 (NWD NW.b); wells on different nets need NW_b1 1.80 (NWD NW.b1).
14. **[IHP]** the library has no 2/1 HV NMOS; `nmosHV_w2_l1` = x-geometry of nmosHV$7 (10/1) with the
    y-geometry of nmosHV$11 (2/4); derive_mos checked every layer's intervals against both.
15. **[IHP]** tabs with a Via1 at their end: 0.29 wide (0.19 + 2 x V1_c1 0.05).
16. **[IHP]** `SaveLayoutOptions.gds2_write_timestamps = False`: two builds, same sha256.

## IHP pitfalls and workarounds

- **[IHP]** The KLayout DRC deck cannot run here: KLayout 0.28.16 (needs >= 0.29.11), klayout.db has no Ruby, and
  the PDK copy lacks `layers_def.drc`, `5_5_activ`, `5_7_thickgateox`, `5_8_gatpoly`, `5_10_psd`, `5_16_metal1`,
  `7_2_latchup` and others. Workaround: `tools/oa_core_pd_drc.py` (Python subset on klayout.db, values from J,
  semantics from the deck files; "json only" where the file is missing). Checked here by injection: a deleted tie
  gives LU.b, MS3 moved 0.1 um left gives Act.b / Gat.b1 / Cnt.f, a row moved 0.03 um down gives Act.b / Cnt.f.
- **[IHP]** No LVS deck in the PDK copy: `tools/oa_core_pd_lvs.py` extracts HV MOS by the DRC derivations
  (N+ = Activ not under pSD; HV = under ThickGateOx). Checked by injection: one missing Via1 and one M2 short both
  give MISMATCH.
- **[IHP]** The ptap1 PCell carries Substrate 40/0 and a Metal1.pin; with 40/0, IHP's `run_lvs.py` extracts a tap
  resistor unless `--disable_tap_extraction`. The tie segments here are plain p+ Activ without 40/0.
- **[IHP]** The PCell's S / D stripes carry Metal1.pin 8/2 boxes and the gate GatPoly.pin 5/2; they stay in the
  copied device cells (Pin.e is met: the pin boxes lie on Metal1).

## Added 2026-10-28 from bg_n4 (numbering as in ../generic/rules.md)

19. **[IHP]** bg_n4: four rows L = 4 (4 x 4.68 + 3 x 0.21 = 19.35) + row Y (0.21 + 1.68) end 21.24 above R0's
    bottom; with the bottom tie at Act_b 0.21 that is 21.45 um > LU_b 20, so a second segment sits over row Y
    (Activ (0, 21.45; 12.25, 21.75)). With both: farthest N+ 10.33 um (bottom), 7.67 um (top). With one tie, at
    most four rows of L = 4 um (19.56 um) or ten rows of L = 1 um (18.90 um, oa_n10).
20. **[IHP]** flip = the same R270 instance; the wiring alone puts S on the top stripe.
22. **[IHP]** a 2 x 2 cross-quad needs two 10/4 fingers per row: Activ 24.75 + sides 2 x 1.33 = 27.4 um against
    A2's 15-22 um. The library has no 5/4 HV NMOS, and `derive_mos` cannot make one (no exported W = 5 variant
    to take the contact positions from), so the rows hold one finger each.
25. **[IHP]** M1_d 0.09 um2 (J; MAX M1.d): the first DRC run of bg_n4 flagged the 0.29 x 0.29 pad on MS3's gate
    contact (0.084 um2); now 0.29 x 0.315.
26. **[IHP]** the top tie is joined to vss in metal: version 1 through MS2's source plate and the left dummy strap,
    option 1 (item 28) through MS2's source plate, the vss bridge and the right outer column. A tie reached only
    through the substrate is not a vss connection for LVS-clean intent.
27. **[IHP]** top edge towards the PMOS NWell: bg_n4's top tie Activ lies 0.27 um below its top edge, its N+ Activ
    at least 0.78 um below; NW_f1 0.62 and NW_d1 0.62 (J) then leave the assembler >= 0.35 um from the top edge to
    the NWell.

## Added 2026-10-28: bg_n4 option 1 (user 05:43)

28. **[IHP]** bg_n4: all nine dummies (8 x 2/4 in the NA / NB rows, the 2/1 `e` beside MS2) now
    D = S = G = g, B = vss. The two dummy straps are g; each g track (R0-T, R3-B) lands 3 Via1 on each strap.
    Gate area on g that is no longer inverted: 8 x 2 x 4 + 2 x 1 = 66 um2. Cost: no area. The outline stays
    18.12 x 22.80 um and every pin stays where it was. Changed:
    - the left strap had been the only vss path from the bottom tie to the top group (top tie, MS2 / MS3 / SKS
      sources); the new path is M1 along the bottom tie and up a right outer column (x 15.54-15.83, y -0.49 to
      19.60) into SKS's source tab;
    - to free the tie's corner, the lowest ea / eb tracks (R0-B, R1-B) run on to M2 risers (x -1.33..-1.04 and
      15.54..15.83) down to the bottom lanes, and the ea / eb joiners now stop at those tracks;
    - ea / eb stay mirror images in length (vertical runs per device 20.62 um each, lanes 8.475 um each), but the
      M1 / M2 split differs: ea 0.785 um M2 riser + 19.05 um M1 joiner, eb 5.675 um M2 + 9.27 um M1. M1 and M2
      sheet resistances are not in this PDK copy; at 2.5 uA per branch the difference is a few squares of metal
      (reasoning).
    Checks: DRC 0, LVS match (dummies g g g vss), metal-only extraction puts the bottom tie, the top tie and the MS2
    / MS3 / SKS sources on one vss net.
