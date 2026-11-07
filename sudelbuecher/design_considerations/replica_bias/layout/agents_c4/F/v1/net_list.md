<!-- SPDX-FileCopyrightText: 2026 Christoph Maier / SPDX-License-Identifier: Apache-2.0 -->
# Net list of pad_ref_rb by cell pins (Claude, agent F, C4; measured by pin_map.py on out/pad_ref_rb.gds)

Placed pin boxes in pad_ref_rb coordinates (um). Fan-out = number of cells joined (+ the port where there is one). Sensitive = a bias or internal analog node of the replica (high impedance or matched).

| net | class | fan-out | cell (orientation): pin layer, box |
|---|---|---:|---|
| bd | sensitive | 2 | rb_mirror (R180): M2 (23.25, 57.33; 23.75, 57.62); rb_tubs (M90): M1 (40.55, 57.56; 41.66, 57.86) |
| bt | sensitive | 2 | rb_tails (R180): M2 (42.52, 53.86; 43.63, 54.16); rb_tubs (M90): M1 (41.89, 57.56; 42.56, 57.86); rb_tubs (M90): M1 (35.79, 57.56; 36.46, 57.86) |
| en_3v3 | input (port, enable) | 1 + port | rb_tree_n (R180): M2 (70.64, 79.67; 71.14, 79.96) |
| en_3v3_b | input (port, enable) | 3 + port | rb_cload (M0): M2 (18.08, 71.77; 18.37, 72.17); rb_tree_n (R180): M2 (37.13, 79.67; 37.63, 79.96); rb_tree_p (R180): M1 (27.01, 55.29; 27.27, 55.59) |
| gh | sensitive | 3 | rb_avg (R0): M1 (61.55, 71.92; 62.55, 72.22); rb_tree_n (R180): M2 (46.42, 74.22; 46.70, 74.62); rb_tubs (M90): M1 (46.21, 69.23; 46.91, 69.53) |
| iref | input (port, 5 uA sourced) | 2 + port | rb_tree_n (R180): M2 (69.12, 74.22; 69.42, 74.62); rb_tree_p (R180): M1 (27.47, 55.29; 27.73, 55.59) |
| m | sensitive | 2 | rb_avg (R0): M1 (57.95, 63.07; 58.25, 63.37); rb_avg (R0): M1 (65.84, 63.07; 66.14, 63.37); rb_tubs (M90): M1 (40.11, 69.23; 40.81, 69.53) |
| ni | sensitive | 2 | rb_tree_n (R180): M2 (37.13, 75.95; 37.63, 76.24); rb_tree_p (R180): M1 (26.54, 55.29; 26.80, 55.59) |
| ts | sensitive | 2 | rb_tails (R180): M2 (47.77, 53.86; 48.88, 54.16); rb_tubs (M90): M1 (47.99, 57.56; 48.66, 57.86) |
| vbnc | sensitive | 2 | rb_casc (M0): M2 (4.00, 36.17; 4.50, 36.46); rb_tree_p (R180): M2 (30.33, 45.22; 31.44, 45.52) |
| vbp | sensitive | 3 | rb_tails (R180): M2 (33.61, 49.54; 34.11, 49.84); rb_tree_n (R180): M2 (61.57, 74.22; 61.86, 74.62); rb_tree_p (R180): M2 (33.11, 49.54; 33.61, 49.84) |
| vcm | output (port) | 4 + port | bypass_rb_f (R0): M2 (17.19, 27.60; 17.69, 27.89); rb_cload (M0): M2 (17.19, 71.77; 17.48, 72.17); rb_mirror (R180): M2 (23.25, 57.83; 23.75, 58.12); rb_tubs (M90): M1 (34.01, 69.23; 34.71, 69.53) |
| vref | output (port) | 4 + port | bypass_rb_f (R0): M2 (43.11, 1.24; 43.61, 1.53); rb_casc (M0): M2 (4.00, 41.44; 4.50, 41.73); rb_cload (M0): M2 (20.09, 71.77; 20.38, 72.17); rb_tree_n (R180): M2 (64.02, 74.22; 64.31, 74.62) |
| xp | sensitive | 3 | rb_avg (R0): M1 (61.55, 57.56; 62.55, 57.77); rb_casc (M0): M2 (75.22, 41.44; 75.72, 41.73); rb_tree_n (R180): M2 (57.12, 74.22; 57.41, 74.62) |
| vddh | supply (pin) | 4 | rb_casc (M0): M2 (4.00, 35.17; 4.50, 35.46); rb_tails (R180): M1 (56.88, 50.53; 57.18, 52.53); rb_tree_p (R180): M1 (32.69, 50.53; 32.99, 52.53); rb_tubs (M90): M2 (54.95, 69.08; 55.45, 69.34) |
| vssh | supply (pin) | 5 | bypass_rb_f (R0): M1 (4.29, 1.29; 4.79, 1.55); rb_casc (M0): M1 (4.29, 41.95; 4.79, 42.21); rb_cload (M0): M1 (4.29, 85.22; 4.79, 85.48); rb_mirror (R180): M1 (22.96, 65.18; 23.46, 65.44); rb_tree_n (R180): M1 (70.35, 83.39; 70.85, 83.64) |
