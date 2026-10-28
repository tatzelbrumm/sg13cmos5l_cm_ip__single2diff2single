# Block assembly in IHP sg13cmos5l: rules with values, pitfalls (all [IHP])

Values from `sg13cmos5l_tech_default.json` ("drc_rules", key in brackets); rule texts from
`sg13cmos5l_maximal.drc` / the feol, beol, geometry files of the uploaded deck. Generic forms: `../generic/rules.md`.

## Rules with values (I-number = the generic G-number they instantiate)
| # | rule | value (source) |
|---|---|---|
| I1 (G1) | one vdd NWell for all PMOS; gaps below NW.b closed | NW.b 0.62 [NW_b] same net; NW.b1 1.80 [NW_b1] different nets; NW.c1 0.62 [NW_c1] P+Activ in TGO |
| I2 (G2) | NWell / tie outline follows the cells | geometry/3_2_angle.drc: nwell only acute-corner check, ACUTE_LIMIT_DEG 87.0; grid 0.005 [grid] |
| I3 (G3) | no tie between array rows; latch-up at the periphery | LU.a 20.00 [LU_a] (maximal.drc, grown in 0.5 um steps inside the well); LU_b 20.0 [LU_b] (json only) |
| I4 (G4) | n tie in the vdd rail inside ThickGateOx | NW.e1 0.62 [NW_e1], TGO.a 0.27 [TGO_a]; outside TGO: NW.e 0.24 [NW_e], TGO.b 0.27 [TGO_b]; Activ 0.30 = Cnt.a 0.16 [Cnt_a] + 2 Cnt.c 0.07 [Cnt_c]; Cnt.b 0.18 [Cnt_b] |
| I5 (G5) | shared p+ tie of oa_n10 / oa_mcs_c | farthest N+ 18.90 um of 20 (A3's measurement); p tie pSD enclosure pSD.c 0.18 [pSD_c] (conservative), pSD.b 0.31 [pSD_b], pSD.d 0.18 [pSD_d] |
| I10 (G10) | router wire 0.29 = V1.a 0.19 [V1_a] + 2 V1.c1 0.05 [V1_c1]; pitch 0.27 (>= (0.29 + Mn.e 0.24) / 2 = 0.265) | M1.a 0.16 [M1_a], M1.b 0.18 [M1_b], M2.a 0.20 [Mn_a], M2.b 0.21 [Mn_b], V1.b 0.22 [V1_b], M1.d 0.09 [M1_d], M2.d 0.144 [Mn_d] |
| I11 (G11) | wide-metal space next to the wide parts | M1.e 0.22 [M1_e] for M1 > 0.30 [M1_e_w], M2.e 0.24 [Mn_e] for M2 > 0.39 [Mn_e_w], parallel run > 1.0 [M1_e_cr, Mn_e_cr] |
| I12 | thick oxide merged between cells | TGO.e 0.86 [TGO_e] (space), TGO.f 0.86 [TGO_f] (width) |
| I13 | PMOS well next to NMOS: the gap search found 0.35 um for oa_pcas_c | NW.d1 0.62 [NW_d1] N+Activ in TGO; oa_misc_n's N+ 0.27 inside its edge |

## Pitfalls specific to IHP
| # | symptom | cause | fix |
|---|---|---|---|
| I20 | Python DRC instead of IHP's deck | no Ruby KLayout; deck include files missing in the upload | `tools/drc.py` (rules from the json, semantics from the deck files that exist), self-tested on injected errors |
| I21 | standalone LVS of a tap-less PMOS cell fails | bulk vdd in the CDL, floating NWell in the layout | bulk = internal net `nw` |
| I22 | svpg's en_3v3 pin unreachable at the block corner | 0.70 um wide cell M1 / 0.97 um M2 pad next to it -> wide spacing 0.22 / 0.24; grid margin 0.12 from the edge | oa_svpg turned M90 |
| I23 | oa_pmir_c's c8 unreachable with a keep-out | pins are 0.20 M2 tracks at 0.41: no pad, no via (0.19 + 2 x V1.c 0.01 > 0.20) | keep-out allows the array's own nets (access inside the cell) |
| I24 | p tie pSD 0.04 from a cell's pSD | tie implant box not checked against other pSD | blockage pSD.b 0.31 + enclosure |
| I25 | the drc.py antenna step crashed on a cell with no nets | circuit lookup returned None | guarded |

## The oa_core_pd numbers (lessons for bg_core_pd)
| item | v1 (library primitives) | v2 (compact) |
|---|---|---|
| block | 76.00 x 50.74 = 3856 um2 | 40.51 x 58.135 = 2355 um2 (-39 %), aspect 1.44 |
| bands inside primitives (bbox - device core: rings, enclosures, track bands) | 884 um2 (22.9 %) | 316 um2 (13.4 %) |
| PMOS ring bands (three separate vdd wells) | 572 um2 (14.8 %) | 185 um2, one well |
| tie diffusion | 268 um2 | 36 um2 (rail tie 11.4, two pmir segments 4.9, NMOS shared tie 19.7) |
| free area (no primitive, no rail) | 710 um2 (18.4 %) | 232 um2 (9.9 %) |
| inner p+ tap row between array rows | 31.3 x 0.78 um (oa_nmir) | none |
| gate area / block; device diffusion / block | 31.8 % / 39.0 % | 48.8 % / 61.0 % |
| largest empty bays | 209 + 190 + 124 um2 (islands around a tall mirror) | 46 um2 left of oa_mcs_c, 2.8 um routing column right of the NMOS |
For bg_core_pd: bg_pmir_pcas without its ring in the vdd well with bg_misc_p's cells; bg_nab rows interdigitated
without bands (A3's estimate 16 x 20 um); bg_res / bg_pnp as voices of equal length; ties in the rails.
