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

## Bandgap core bg_core_pd (2026-10-28): rules with values (I32 on; G-numbers in ../generic/rules.md)
| # | rule | value (source) |
|---|---|---|
| I32 (G27, G28) | pnpMPA as drawn in the library: emitter Activ 2 x 2 um (AE 4 um2, PE 8 um), base N+ ring in its own NWell, collector P+ ring; bg_pnp = 3 x 3 AREF at 7.15 x 5.67 um sharing the collector rings; collector ring = P+ outside NWell = substrate tie | measured on `pnpMPA` / `bg_pnp` in pad_buffer_cells.gds; base NWell 1.25 um inside the array box -> NW.b1 1.80 [NW_b1] (base on vss, vdd well) gives >= 0.55 um array box to the vdd well; NW.f 0.24 [NW_f] collector ring to an NWell |
| I33 (G29) | rhigh segment `rhigh$1`: body on PolyRes 128/0 (GatPoly only at the heads), 0.5 x 9.94 um, contact bars 0.36 x 0.16 um, pitch 0.68 = 0.50 + Gat.b 0.18 [Gat_b] | measured on `bg_res`; the deck has no NWell rule for rhigh (Rhi.a-f in sg13cmos5l_maximal.drc): the array abuts the vdd well at 0 um, DRC 0 |
| I34 (G34) | rhigh value: xschem symbol (`sg13cmos5l_pr/rhigh.sym`, value=) R = (1.6e-4 / w + 1360 ((b + 1) l + (1.081 w + 0.18e-6) b) / (w - 0.04e-6)) / m; one segment 0.5 x 9.94 um = 29.708 kOhm (= the library cell's label r=29707.826) | a chain of n segments has n head terms: R0 18 x = 534.7 kOhm vs one 0.5 / 179.5 um device 531.0 (+0.70 %); R1A 11 x vs 0.5 / 109.3 +1.03 %; R1B 10 x vs 0.5 / 99.36 +1.02 %; R1A / R0 and R1B / R0 +0.32 % (expression evaluated, not simulated) |
| I35 | ContBar: rhigh head contacts are bars, not squares | CntB.h1 0.05 [CntB_h1] Metal1 enclosure, CntB.b1 0.36 [CntB_b1] space for runs > 5.0 [CntB_b1_l]; Cnt.a 0.16 [Cnt_a] applies to the square contacts only (tools/drc.py) |
| I36 (G32) | bg_ms1 hanging under bg_pmir_pcas_c: n tie segment in pmir's bottom margin, Activ y -0.51 ... -0.21 (cell coordinates), 13.1 um over ms1's width | Act.b 0.21 [Act_b] to the bottom row; NW.e1 0.62 [NW_e1] -> NWell 0.51 um below pmir's edge, inside ms1's merged well; LU.a 20 [LU_a]: without it LU.a flagged ms1's lower P+ (10 shapes; ms1 starts 16.15 um below the rail tie and is 6.99 um tall) |
| I37 | wide vdd rail over bg_pmir_pcas_c: 0.22 um gap | its side lines (vpg co ca / vpc g iout) run to the top edge; M1.e 0.22 [M1_e] next to Metal1 wider than 0.30 [M1_e_w] |

## Pitfalls specific to IHP (bandgap)
| # | symptom | cause | fix |
|---|---|---|---|
| I38 | LVS: rhigh not extracted | the resistor body is PolyRes 128/0, not GatPoly | resistor layer = PolyRes, terminals = GatPoly outside PolyRes (heads); R in squares (L / W) |
| I39 | LVS: the BJT extractor needs a collector layer; "terminal B isn't connected" | pnpMPA's collector is the substrate | DeviceExtractorBJT3Transistor with an empty C layer and its substrate terminal tC on the global net of the substrate tie; connect the emitter / base terminal layers |
| I40 | xschem writes "?" for the pnpMPA lines (inputs_bg/bg_core_pd_xschem.spice) | the symbol's format calls Tcl ev7 / ev, which the PDK copy's xschemrc does not define | two procs in the rc (`out_bg/xs/xschemrc`); the netlist then has `pnpMPA a=4e-12 p=8e-06 m=8` |
| I41 | Cnt.a errors on every rhigh head | the 0.36 x 0.16 contact bars checked as square contacts | ContBar class (I35) |

## The bg_core_pd numbers
| item | library primitives (no block existed) | compact block |
|---|---|---|
| area | 6 primitives, sum of boxes 2673.0 um2 | 47.55 x 50.05 = 2379.9 um2 (-11.0 %); revised primitives 2044.1 um2 (-23.5 %) |
| bands inside primitives (bbox - device core) | 880.3 um2 | 314.8 um2 |
| tie diffusion inside primitives | 303.8 um2 (rings) | 8.0 um2 (bg_n4) + 17.8 um2 top level (rail tie, ms1 segment) |
| vdd wells | 2 (bg_pmir_pcas, bg_misc_p) | 1 (plus the 9 pnp base wells on vss, part of the device) |
| free area (no primitive, no rail) | (no block) | 249.9 um2 = 10.5 %, mostly the strip beside bg_pnp_c (routing channel) |
| ea / eb / e2 wiring | (unwired) | ea 3.50 M1 + 14.55 M2, 1 via (incl. the branch to Q1); eb 4.59 M2; e2 4.32 M2, 1 via |
