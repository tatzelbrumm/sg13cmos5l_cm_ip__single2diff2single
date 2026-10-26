<!--
SPDX-FileCopyrightText: 2026 Christoph Maier
SPDX-License-Identifier: Apache-2.0
-->
# Cell tree of `pad_buffer_cells.gds`

Read from the GDS, 2026-10-26. Primitive -> rows (`_r1`, and `_r2` mirrored about the shared tie) ->
IHP SG13_dev devices, as W/L in um with counts (dummies included). Sizes are bounding boxes.
P-numbers as in `../layout_primitives.md`. The top cell `pad_buffer_cells` only places these side by side.

```
d2s amplifier (sg13cmos5l_IOPadDiff2Single)
|- d2s_inputs  (P1 input devices)  [34.8 x 28.8 um]
|  |- 4 x tub_p20x1_dummy  [4.3 x 13.0 um]  pmosHV 20/1 ng=2, ntap1
|  `- 8 x tub_p20x1  [4.3 x 13.0 um]  pmosHV 20/1 ng=2, ntap1
|- d2s_tails  (P2 tails + BP)  [45.0 x 14.0 um]
|  |- d2s_tails_r1  [44.3 x 8.0 um]  pmosHV 5/6 x6, ntap1
|  `- d2s_tails_r2  [44.3 x 8.0 um]  pmosHV 5/6 x6, ntap1
|- d2s_rhigh  (P3 degeneration R)  [27.7 x 20.0 um]  rhigh 0.5x12.65 x18, ptap1
|- sinks_6x6  (P4 fold sinks + BN (both pads))  [60.4 x 16.4 um]
|  |- sinks_6x6_r1  [58.2 x 8.6 um]  nmosHV 6/6 x8, ptap1
|  `- sinks_6x6_r2  [58.2 x 8.6 um]  nmosHV 6/6 x8, ptap1
|- d2s_loads  (P5 loads)  [53.4 x 9.0 um]  pmosHV 6/4 x10, ntap1
|- d2s_casc_n  (P6 cascodes + BNC)  [26.3 x 17.6 um]  nmosHV 15/3 x4, nmosHV 1/8, ptap1
|- d2s_casc_p  (P6 cascodes + BPC)  [23.0 x 18.0 um]  pmosHV 15/3 x4, pmosHV 1/4, ntap1
|- d2s_ab_p  (P7 class AB, P side)  [10.0 x 9.7 um]  pmosHV 6.66/0.6 x5, ntap1
|- d2s_ab_n  (P7 class AB, N side)  [11.3 x 7.0 um]  nmosHV 4.4/1 x5, ptap1
|- d2s_cma  (P9 Miller cap A)  [17.9 x 19.0 um]  pmosHV 16/16, ntap1
|- d2s_cmb  (P9 Miller cap B)  [17.9 x 19.0 um]  pmosHV 16/16, ntap1
|- d2s_pd_p  (power-down)  [3.2 x 2.2 um]  pmosHV 1/0.45 1 x 2 array, shared vdd, no tap
`- d2s_pd_n  (power-down)  [2.5 x 2.0 um]  nmosHV 1/0.45 1 x 2 array, shared vss, no tap

s2d amplifier (sg13cmos5l_IOPadSingle2Diff); sinks_6x6 shared with d2s
|- s2d_inputs  (P1 input devices)  [47.0 x 28.8 um]
|  |- 4 x tub_p20x1_dummy  [4.3 x 13.0 um]  pmosHV 20/1 ng=2, ntap1
|  `- 12 x tub_p20x1  [4.3 x 13.0 um]  pmosHV 20/1 ng=2, ntap1
|- s2d_tails  (P2 tails + BP)  [59.6 x 14.0 um]
|  |- s2d_tails_r1  [58.9 x 8.0 um]  pmosHV 5/6 x8, ntap1
|  `- s2d_tails_r2  [58.9 x 8.0 um]  pmosHV 5/6 x8, ntap1
|- s2d_rhigh  (P3 degeneration R)  [38.9 x 22.4 um]  rhigh 0.5x12.65 x26, ptap1
|- s2d_sinks_cmfb  (P4 CMFB sinks)  [45.9 x 16.4 um]
|  |- s2d_sinks_cmfb_r1  [43.6 x 8.6 um]  nmosHV 6/6 x6, ptap1
|  `- s2d_sinks_cmfb_r2  [43.6 x 8.6 um]  nmosHV 6/6 x6, ptap1
|- s2d_loads  (P5 loads)  [74.6 x 9.0 um]  pmosHV 6/4 x14, ntap1
|- s2d_casc_n  (P6 cascodes + BNC)  [43.5 x 17.6 um]  nmosHV 15/3 x8, nmosHV 1/8, ptap1
|- s2d_casc_p  (P6 cascodes + BPC)  [31.6 x 18.0 um]  pmosHV 15/3 x6, pmosHV 1/4, ntap1
|- s2d_cload  (P9 load caps)  [26.5 x 14.6 um]  nmosHV 12/12 x2, ptap1
|- s2d_pd_n  (output ties)  [2.5 x 2.0 um]  nmosHV 1/0.45 1 x 2 array, shared vcm, no tap
`- s2d_pd_p  (output ties)  [3.2 x 2.2 um]  pmosHV 1/0.45 1 x 2 array, shared vcm, no tap

bias tree (d2s_bias_in_tree_pd without BP / BN)
|- bias_tree_n  (NMOS mirror (gate ni))  [43.6 x 8.6 um]  nmosHV 6/6 x5, nmosHV 2.4/6, ptap1
|- bias_tree_p  (PMOS mirror (gate vbp))  [37.0 x 8.0 um]  pmosHV 5/6 x4, pmosHV 2/6, ntap1
|- bias_tree_sw  (iref TG + pull-down)  [2.5 x 2.0 um]  nmosHV 1/0.45 1 x 2 array, shared ni, no tap
`- bias_tree_swp  (iref TG)  [2.4 x 4.0 um]  pmosHV 1/0.45, ntap1

Oguey-Aebischer core (oa_core_pd)
|- oa_pmir_a  (PMOS mirror, rows 1-2)  [76.8 x 8.0 um]
|  |- oa_pmir_a_r1  [74.9 x 5.0 um]  pmosHV 2/8 x8, ntap1
|  `- oa_pmir_a_r2  [74.9 x 5.0 um]  pmosHV 2/8 x8, ntap1
|- oa_pmir_b  (PMOS mirror, rows 3-4)  [76.8 x 8.0 um]
|  |- oa_pmir_b_r1  [74.9 x 5.0 um]  pmosHV 2/8 x8, ntap1
|  `- oa_pmir_b_r2  [74.9 x 5.0 um]  pmosHV 2/8 x8, ntap1
|- oa_pcas  (PMOS cascodes)  [30.2 x 5.0 um]  pmosHV 2/2 x7, pmosHV 0.5/2, pmosHV 1/2, ntap1
|- oa_nmir  (M10 / M11)  [34.1 x 24.4 um]
|  |- oa_nmir_r1  [31.9 x 12.6 um]  nmosHV 10/1 x14, ptap1
|  `- oa_nmir_r2  [31.9 x 12.6 um]  nmosHV 10/1 x14, ptap1
|- oa_mcs  (MCS / MCL)  [62.5 x 6.0 um]  nmosHV 3.4/30 x2, ptap1
|- oa_misc_n  (MC10, MS2, MS3, SKS)  [9.5 x 12.6 um]  nmosHV 10/1 x2, nmosHV 0.5/2, nmosHV 1/0.45, ptap1
`- oa_misc_p  (MS1 chain, SVPG)  [58.2 x 5.5 um]
   |- oa_misc_p_r1  [57.1 x 3.5 um]  pmosHV 0.5/12.5 x4, ntap1
   `- oa_misc_p_r2  [57.5 x 4.0 um]  pmosHV 0.5/12.5 x4, pmosHV 1/0.45, ntap1

bandgap core (bg_core_pd)
|- bg_pmir  (PMOS mirror)  [23.1 x 24.0 um]
|  |- bg_pmir_r1  [21.2 x 13.0 um]  pmosHV 10/1 x9, ntap1
|  `- bg_pmir_r2  [21.2 x 13.0 um]  pmosHV 10/1 x9, ntap1
|- bg_pcas  (PMOS cascodes)  [24.9 x 24.0 um]
|  |- bg_pcas_r1  [21.2 x 13.0 um]  pmosHV 10/1 x9, ntap1
|  `- bg_pcas_r2  [21.2 x 13.0 um]  pmosHV 10/1 x9, ntap1
|- bg_nab  (NA / NB)  [31.6 x 12.6 um]  nmosHV 10/4 x6, ptap1
|- bg_misc_n  (MS2, MS3, SKS)  [7.2 x 12.6 um]  nmosHV 10/1, nmosHV 0.5/2, nmosHV 1/0.45, ptap1
|- bg_misc_p  (MS1 chain, SVPG)  [58.2 x 5.5 um]
|  |- bg_misc_p_r1  [57.1 x 3.5 um]  pmosHV 0.5/12.5 x4, ntap1
|  `- bg_misc_p_r2  [57.5 x 4.0 um]  pmosHV 0.5/12.5 x4, pmosHV 1/0.45, ntap1
|- bg_pnp  (Q1 + 8 Q2 (placed only))  [22.2 x 17.8 um]  pnpMPA 2x2, 3 x 3 array, shared collector rings
`- bg_res  (R1A / R1B / R0 (placed only))  [56.9 x 11.2 um]  rhigh 0.5x9.94 x41

fit checks (arrangements of the cells above, no new geometry): fit_bias_tree_oa_bg, fit_s2d_front_caps, fit_s2d_front, fit_d2s_front_caps, fit_d2s_front
```
