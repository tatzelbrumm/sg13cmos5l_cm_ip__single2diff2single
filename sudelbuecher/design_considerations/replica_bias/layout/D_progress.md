<!--
SPDX-FileCopyrightText: 2026 Christoph Maier
SPDX-License-Identifier: Apache-2.0
-->
23:32 CET D: briefs, circuit, generators (build_rb_p / build_s2d_p3 / build_rb_n) read. Plan: option B slices (nand2_hv + inv_hv + tg_hv), N row D NI NM D (rb_mirror code), P row D PO0 PO1 PD PO2 PO3 D (tails code), slice row under both, channel between.
23:47 CET D: first full build bias_dist_pd 60.49 x 16.24 um (982 um2): run_drc 0, maximal+LU 0, flat LVS match (73 devices + 4 dummies). Gate cells, slice, TDN, SVPD, both mirrors clean alone. Next: sym_check, negative LVS, metal connectivity, previews, docs.
23:58 CET D: done. out/ written (gds, cdl, cells, previews, logs, pin_map.md, note.md); all checks clean, report in reports/D_report.md.
