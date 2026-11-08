<!-- SPDX-FileCopyrightText: 2026 Christoph Maier / SPDX-License-Identifier: Apache-2.0 -->
# Net list of pad_ref_rb by cell pins (Claude, agent F, C4; measured by pin_map.py on out/pad_ref_rb.gds)

Placed pin boxes in pad_ref_rb coordinates (um). Fan-out = number of cells joined (+ the port where there is one). Sensitive = a bias or internal analog node of the replica (high impedance or matched).

| net | class | fan-out | cell (orientation): pin layer, box |
|---|---|---:|---|
| bd | sensitive | 2 | rb_mirror (M90): M2 (20.15, 53.66; 20.65, 53.95); rb_tubs (R0): M1 (51.91, 45.55; 53.02, 45.85) |
| bt | sensitive | 2 | rb_tails (M0): M2 (49.94, 42.02; 51.05, 42.32); rb_tubs (R0): M1 (51.01, 45.55; 51.68, 45.85); rb_tubs (R0): M1 (57.11, 45.55; 57.78, 45.85) |
| en_3v3 | input (port, enable) | 1 + port | rb_tree_n (R0): M2 (0.90, 37.13; 1.40, 37.42) |
| en_3v3_b | input (port, enable) | 3 + port | rb_cload (M0): M2 (57.72, 60.43; 58.01, 60.83); rb_tree_n (R0): M2 (34.41, 37.13; 34.91, 37.42); rb_tree_p (M0): M1 (66.30, 43.45; 66.56, 43.75) |
| gh | sensitive | 3 | rb_avg (R0): M1 (31.02, 59.91; 32.02, 60.21); rb_tree_n (R0): M2 (25.34, 42.47; 25.62, 42.88); rb_tubs (R0): M1 (46.66, 57.22; 47.36, 57.52) |
| iref | input (port, 5 uA sourced) | 2 + port | rb_tree_n (R0): M2 (2.63, 42.47; 2.92, 42.88); rb_tree_p (M0): M1 (65.84, 43.45; 66.09, 43.75) |
| m | sensitive | 2 | rb_avg (R0): M1 (27.43, 51.06; 27.73, 51.36); rb_avg (R0): M1 (35.31, 51.06; 35.62, 51.36); rb_tubs (R0): M1 (52.76, 57.22; 53.45, 57.52) |
| ni | sensitive | 2 | rb_tree_n (R0): M2 (34.41, 40.85; 34.91, 41.14); rb_tree_p (M0): M1 (66.77, 43.45; 67.03, 43.75) |
| ts | sensitive | 2 | rb_tails (M0): M2 (44.69, 42.02; 45.80, 42.32); rb_tubs (R0): M1 (44.91, 45.55; 45.58, 45.85) |
| vbnc | sensitive | 2 | rb_casc (R180): M2 (72.12, 25.33; 72.62, 25.62); rb_tree_p (M0): M2 (62.12, 33.38; 63.23, 33.68) |
| vbp | sensitive | 3 | rb_tails (M0): M2 (59.46, 37.70; 59.96, 38.00); rb_tree_n (R0): M2 (10.19, 42.47; 10.48, 42.88); rb_tree_p (M0): M2 (59.96, 37.70; 60.46, 38.00) |
| vcm | output (port) | 6 + port | capm (R0): M2 (10.27, 59.68; 10.77, 59.97); capt (R0): M2 (71.80, 59.66; 72.09, 59.95); capv (R0): M2 (21.32, 75.58; 21.82, 75.87); rb_cload (M0): M2 (56.83, 60.43; 57.12, 60.83); rb_mirror (M90): M2 (20.15, 53.16; 20.65, 53.45); rb_tubs (R0): M1 (58.86, 57.22; 59.56, 57.52) |
| vref | output (port) | 4 + port | capr (R0): M2 (36.19, 0.39; 36.69, 0.68); rb_casc (R180): M2 (72.12, 30.60; 72.62, 30.89); rb_cload (M0): M2 (59.73, 60.43; 60.02, 60.83); rb_tree_n (R0): M2 (7.74, 42.47; 8.03, 42.88) |
| xp | sensitive | 3 | rb_avg (R0): M1 (31.02, 45.55; 32.02, 45.76); rb_casc (R180): M2 (0.90, 30.60; 1.40, 30.89); rb_tree_n (R0): M2 (14.63, 42.47; 14.93, 42.88) |
| vddh | supply (pin) | 4 | rb_casc (R180): M2 (72.12, 24.33; 72.62, 24.62); rb_tails (M0): M1 (36.39, 38.69; 36.69, 40.69); rb_tree_p (M0): M1 (60.58, 38.69; 60.88, 40.69); rb_tubs (R0): M2 (38.12, 57.07; 38.62, 57.33) |
| vssh | supply (pin) | 8 | capm (R0): M1 (1.19, 55.01; 1.69, 55.27); capr (R0): M1 (1.19, 0.44; 1.69, 0.70); capt (R0): M1 (68.01, 45.84; 68.51, 46.10); capv (R0): M1 (1.19, 61.50; 1.69, 61.76); rb_casc (R180): M1 (71.83, 31.11; 72.33, 31.37); rb_cload (M0): M1 (43.93, 73.88; 44.43, 74.14); rb_mirror (M90): M1 (19.86, 45.84; 20.36, 46.10); rb_tree_n (R0): M1 (1.19, 33.45; 1.69, 33.71) |
