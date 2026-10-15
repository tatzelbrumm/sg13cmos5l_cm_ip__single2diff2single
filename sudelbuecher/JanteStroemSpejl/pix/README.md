<!--
SPDX-FileCopyrightText: 2026 Christoph Maier
SPDX-License-Identifier: Apache-2.0
-->
# pix/: pictures for [REPORT.md](../REPORT.md)

| File | What it shows | Made by | Proves / doesn't prove |
|---|---|---|---|
| [lecture_p25_current_mirror.png](lecture_p25_current_mirror.png) | Slide 25 of the 2019 UiO test lecture: the current mirror as subtraction of threshold voltages, I₂ ≈ I₁ + g_m δV_T | `pdftoppm -f 25 -singlefile -r 110` from [../ref/2019-03-11_Maier_UiO_test_lecture_analog_IC_design.pdf](../ref/2019-03-11_Maier_UiO_test_lecture_analog_IC_design.pdf) | Shows the reasoning the simulations quantify. Nothing more. |
| [lecture_p46_jante_flag.png](lecture_p46_jante_flag.png) | Slide 46: the 22-transistor mirror layout as the Norwegian flag, one Janteloven rule per output row, the eleventh on the reference row | as above, page 46 | The origin of the netlist. Hand-drawn layout, never DRC-checked or extracted. |
| [lv_mismatch_cace_auto_bins.svg](lv_mismatch_cace_auto_bins.svg) | CACE's own `pooled_mismatch.svg`, LV, iref = 3u / 10u | CACE 2.11.0, cloud run RUN_2026-10-15_18-10-17 | Kept as the bad example: each histogram has its own `bins="auto"`, so both peaks are equally high. Don't compare the heights. |
| [lv_mismatch_shared_bins.svg](lv_mismatch_shared_bins.svg) | LV mismatch, iref = 3u / 10u, 500 runs × 10 outputs each, common bin edges | [../cace/scripts/replot_shared_bins.py](../cace/scripts/replot_shared_bins.py) on the same run | Fair comparison of spread and peak. Typical corner at 27 °C only: the outputs share one reference, so pooled samples are correlated within a run. |
| [lv_rout_shared_bins.svg](lv_rout_shared_bins.svg) | LV, iref = 3u, outputs at V_GS(ref) + dvds, dvds = −0.3 / 0 / +0.3 V | as above, `mirror_rout` | The shift is systematic (r_out); the width is random (mismatch). dvds = −0.3 V is already near the saturation knee. |
| [hv_mismatch_shared_bins.svg](hv_mismatch_shared_bins.svg) | Same as `lv_mismatch_shared_bins.svg` for `sg13_hv_nmos` | cloud run RUN_2026-10-15_18-28-01 | Same geometry and currents, different V_GS (1.27 / 1.82 V). |
| [hv_rout_shared_bins.svg](hv_rout_shared_bins.svg) | Same as `lv_rout_shared_bins.svg` for `sg13_hv_nmos` | as above | |

All simulation figures come from the cloud rebuild of the IIC-OSIC-TOOLS 2026.09 tools
([../../cloud_environment.md](../../cloud_environment.md)). A local CACE run plus
`replot_shared_bins.py` should reproduce them bit for bit (fixed SEED).
PNG and SVG files written through the device bridge may carry a C2PA/JUMBF
provenance stamp, so compare image payloads, not file hashes.
