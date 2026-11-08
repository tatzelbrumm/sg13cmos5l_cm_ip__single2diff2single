<!-- SPDX-FileCopyrightText: 2026 Christoph Maier / SPDX-License-Identifier: Apache-2.0 -->
# bias_dist_pd: pin map (Claude, agent D, C4 2026-11-07)

Cell `bias_dist_pd` in `bias_dist_pd.gds`, bbox (-0.35, -0.47; 60.14, 15.77) um = 60.49 x 16.24 um. Coordinates are
pin boxes in the cell frame, read back from the GDS [M]. Port order of the CDL = the source subckt, with vdd / vss
renamed to vddh / vssh: `vddh vssh en_3v3 en_3v3_b iin0 iin1 iin2 iin3 en_in0 en_in1 en_in2 en_in3 iout0 iout1
iout2 iout3 en_out0 en_out1 en_out2 en_out3`.

| edge | pin | layer | box (um) | note |
|---|---|---|---|---|
| left | iin0 | Metal1 | (-0.35, 6.05; 0.15, 6.26) | oa_core_pd, track T1 |
| left | iin1 | Metal1 | (-0.35, 5.66; 0.15, 5.87) | bg_core_pd, T2 |
| left | iin2 | Metal1 | (-0.35, 5.27; 0.15, 5.48) | harness ibias0, T3 |
| left | iin3 | Metal1 | (-0.35, 4.88; 0.15, 5.09) | harness ibias1, T4 |
| right | iout0 | Metal1 | (59.64, 6.05; 60.14, 6.26) | S2D iref (PO0), T1 |
| right | iout1 | Metal1 | (59.64, 5.66; 60.14, 5.87) | D2S iref (PO1), T2 |
| right | iout2 | Metal1 | (59.64, 5.27; 60.14, 5.48) | pad_ref_rb iref (PO2), T3 |
| right | iout3 | Metal1 | (59.64, 4.88; 60.14, 5.09) | spare (PO3), T4 |
| bottom | en_3v3 | Metal1 | (0.27, -0.47; 0.77, -0.18) | end of the en_3v3 line under the switch row |
| bottom | en_in0..3 | Metal2 | x 2.525 / 6.905 / 11.285 / 15.665, 0.29 wide, y -0.47..-0.17 | |
| bottom | en_3v3_b | Metal2 | (19.235, -0.47; 19.525, -0.17) | TDN gate |
| bottom | en_out0..3 | Metal2 | x 28.000 / 33.250 / 43.750 / 49.000, 0.29 wide, y -0.47..-0.17 | |
| top | vssh | Metal1 | (1.27, 15.22; 3.27, 15.48) | top leg of the NI / NM ring; row vss strip joined by an M2 strap |
| top | vddh | Metal1 | (56.52, 14.49; 58.52, 14.79) | top leg of the PD / PO ring; row vdd strip joined by an M2 strap |

All enables are static configuration bits (bottom edge). iin / iout tracks run in Metal1 to the edges; a Metal2
landing at the edge is one Via1 if the top-level router wants Metal2 pins (F's pad_ref_rb uses Metal2 at its edge).
