<!-- SPDX-FileCopyrightText: 2026 Christoph Maier / SPDX-License-Identifier: Apache-2.0 -->
# Pin map of the input rows (Claude, agent F, C4; measured by pin_map.py from the delivered GDS)

Cell frame of each delivered cell (R0); edge = the bounding-box edge the pin box touches.

| cell (file) | size um | pin | net | layer | edge | box (x0, y0; x1, y1) |
|---|---|---|---|---|---|---|
| rb_tree_p (rb_p_cells.gds) | 12.94 x 10.37 | en_3v3_b | en_3v3_b | M1 | bottom | (6.340, 0.000; 6.600, 0.300) |
| rb_tree_p (rb_p_cells.gds) | 12.94 x 10.37 | iref | iref | M1 | bottom | (5.875, 0.000; 6.135, 0.300) |
| rb_tree_p (rb_p_cells.gds) | 12.94 x 10.37 | ni | ni | M1 | bottom | (6.805, 0.000; 7.065, 0.300) |
| rb_tree_p (rb_p_cells.gds) | 12.94 x 10.37 | vbnc | vbnc | M2 | top | (2.165, 10.070; 3.275, 10.370) |
| rb_tree_p (rb_p_cells.gds) | 12.94 x 10.37 | vbp | vbp | M2 | left | (0.000, 5.750; 0.500, 6.050) |
| rb_tree_p (rb_p_cells.gds) | 12.94 x 10.37 | vdd | vddh | M1 | inside | (0.620, 3.060; 0.920, 5.060) |
| rb_tails (rb_p_cells.gds) | 24.19 x 9.16 | bt | bt | M2 | bottom | (14.165, 0.000; 15.275, 0.300) |
| rb_tails (rb_p_cells.gds) | 24.19 x 9.16 | ts | ts | M2 | bottom | (8.915, 0.000; 10.025, 0.300) |
| rb_tails (rb_p_cells.gds) | 24.19 x 9.16 | vbp | vbp | M2 | right | (23.690, 4.320; 24.190, 4.620) |
| rb_tails (rb_p_cells.gds) | 24.19 x 9.16 | vdd | vddh | M1 | inside | (0.620, 1.630; 0.920, 3.630) |
| rb_tubs (rb_p_cells.gds) | 28.70 x 11.97 | bd | bd | M1 | bottom | (13.795, 0.000; 14.905, 0.300) |
| rb_tubs (rb_p_cells.gds) | 28.70 x 11.97 | bt | bt | M1 | bottom | (12.890, 0.000; 13.560, 0.300) |
| rb_tubs (rb_p_cells.gds) | 28.70 x 11.97 | bt | bt | M1 | bottom | (18.990, 0.000; 19.660, 0.300) |
| rb_tubs (rb_p_cells.gds) | 28.70 x 11.97 | gh | gh | M1 | top | (8.540, 11.670; 9.240, 11.970) |
| rb_tubs (rb_p_cells.gds) | 28.70 x 11.97 | m | m | M1 | top | (14.640, 11.670; 15.340, 11.970) |
| rb_tubs (rb_p_cells.gds) | 28.70 x 11.97 | ts | ts | M1 | bottom | (6.790, 0.000; 7.460, 0.300) |
| rb_tubs (rb_p_cells.gds) | 28.70 x 11.97 | vcm | vcm | M1 | top | (20.740, 11.670; 21.440, 11.970) |
| rb_tubs (rb_p_cells.gds) | 28.70 x 11.97 | vdd | vddh | M2 | left | (0.000, 11.520; 0.500, 11.780) |
| rb_avg (rb_avg_v3.gds) | 8.19 x 14.66 | gh | gh | M1 | top | (3.595, 14.360; 4.595, 14.660) |
| rb_avg (rb_avg_v3.gds) | 8.19 x 14.66 | m | m | M1 | left | (0.000, 5.510; 0.300, 5.810) |
| rb_avg (rb_avg_v3.gds) | 8.19 x 14.66 | m | m | M1 | right | (7.890, 5.510; 8.190, 5.810) |
| rb_avg (rb_avg_v3.gds) | 8.19 x 14.66 | xp | xp | M1 | bottom | (3.595, 0.000; 4.595, 0.210) |
| rb_tree_n (rb_n_cells.gds) | 34.01 x 9.71 | en_3v3 | en_3v3 | M2 | left | (-3.330, 3.195; -2.830, 3.485) |
| rb_tree_n (rb_n_cells.gds) | 34.01 x 9.71 | en_3v3_b | en_3v3_b | M2 | right | (30.180, 3.195; 30.680, 3.485) |
| rb_tree_n (rb_n_cells.gds) | 34.01 x 9.71 | gh | gh | M2 | top | (21.105, 8.535; 21.395, 8.935) |
| rb_tree_n (rb_n_cells.gds) | 34.01 x 9.71 | iref | iref | M2 | top | (-1.605, 8.535; -1.315, 8.935) |
| rb_tree_n (rb_n_cells.gds) | 34.01 x 9.71 | ni | ni | M2 | right | (30.180, 6.915; 30.680, 7.205) |
| rb_tree_n (rb_n_cells.gds) | 34.01 x 9.71 | vbp | vbp | M2 | top | (5.955, 8.535; 6.245, 8.935) |
| rb_tree_n (rb_n_cells.gds) | 34.01 x 9.71 | vref | vref | M2 | top | (3.505, 8.535; 3.795, 8.935) |
| rb_tree_n (rb_n_cells.gds) | 34.01 x 9.71 | vss | vssh | M1 | inside | (-3.040, -0.490; -2.540, -0.230) |
| rb_tree_n (rb_n_cells.gds) | 34.01 x 9.71 | xp | xp | M2 | top | (10.405, 8.535; 10.695, 8.935) |
| rb_casc (rb_n_cells.gds) | 71.72 x 12.37 | vbnc | vbnc | M2 | left | (-2.010, 4.830; -1.510, 5.120) |
| rb_casc (rb_n_cells.gds) | 71.72 x 12.37 | vdd | vddh | M2 | left | (-2.010, 5.830; -1.510, 6.120) |
| rb_casc (rb_n_cells.gds) | 71.72 x 12.37 | vref | vref | M2 | left | (-2.010, -0.440; -1.510, -0.150) |
| rb_casc (rb_n_cells.gds) | 71.72 x 12.37 | vss | vssh | M1 | inside | (-1.720, -0.920; -1.220, -0.660) |
| rb_casc (rb_n_cells.gds) | 71.72 x 12.37 | xp | xp | M2 | right | (69.210, -0.440; 69.710, -0.150) |
| rb_mirror (rb_n_cells.gds) | 19.75 x 9.17 | bd | bd | M2 | left | (-1.500, 7.330; -1.000, 7.620) |
| rb_mirror (rb_n_cells.gds) | 19.75 x 9.17 | vcm | vcm | M2 | left | (-1.500, 6.830; -1.000, 7.120) |
| rb_mirror (rb_n_cells.gds) | 19.75 x 9.17 | vss | vssh | M1 | inside | (-1.210, -0.490; -0.710, -0.230) |
| rb_cload (rb_n_cells.gds) | 29.56 x 14.24 | en_3v3_b | en_3v3_b | M2 | inside | (13.075, 12.820; 13.365, 13.220) |
| rb_cload (rb_n_cells.gds) | 29.56 x 14.24 | vcm | vcm | M2 | inside | (12.185, 12.820; 12.475, 13.220) |
| rb_cload (rb_n_cells.gds) | 29.56 x 14.24 | vref | vref | M2 | inside | (15.085, 12.820; 15.375, 13.220) |
| rb_cload (rb_n_cells.gds) | 29.56 x 14.24 | vss | vssh | M1 | inside | (-0.710, -0.490; -0.210, -0.230) |
| bypass_rb (rb_n_cells.gds) | 53.30 x 40.02 | vcm | vcm | M2 | inside | (12.185, 38.710; 12.685, 39.000) |
| bypass_rb (rb_n_cells.gds) | 53.30 x 40.02 | vref | vref | M2 | inside | (12.905, -0.540; 13.405, -0.250) |
| bypass_rb (rb_n_cells.gds) | 53.30 x 40.02 | vss | vssh | M1 | inside | (-0.710, -0.490; -0.210, -0.230) |
| capr (rb_caps.gds) | 71.58 x 19.14 | vref | vref | M2 | inside | (34.285, -0.540; 34.785, -0.250) |
| capr (rb_caps.gds) | 71.58 x 19.14 | vss | vssh | M1 | inside | (-0.710, -0.490; -0.210, -0.230) |
| capm (rb_caps.gds) | 19.74 x 5.49 | vcm | vcm | M2 | inside | (8.365, 4.180; 8.865, 4.470) |
| capm (rb_caps.gds) | 19.74 x 5.49 | vss | vssh | M1 | inside | (-0.710, -0.490; -0.210, -0.230) |
| capt (rb_caps.gds) | 5.50 x 14.64 | vcm | vcm | M2 | inside | (3.085, 13.330; 3.375, 13.620) |
| capt (rb_caps.gds) | 5.50 x 14.64 | vss | vssh | M1 | inside | (-0.710, -0.490; -0.210, -0.230) |
| capv (rb_caps.gds) | 41.86 x 14.90 | vcm | vcm | M2 | inside | (19.425, 13.590; 19.925, 13.880) |
| capv (rb_caps.gds) | 41.86 x 14.90 | vss | vssh | M1 | inside | (-0.710, -0.490; -0.210, -0.230) |
