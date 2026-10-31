<!--
SPDX-FileCopyrightText: 2026 Christoph Maier
SPDX-License-Identifier: Apache-2.0
-->
# C2 previews

Intermediate pictures shown to Christoph during session C2 (his request, about 17:00: "keep previews for documentation
purposes, out of the mainstream"). Kept here on the notes branch, not in the design branch. Rendered with `../render.py`
(KLayout LayoutView, PDK layer properties, the ring metals M3 / M4 / TM1 and their vias hidden), unless the file name
names an agent's own render.

| file | what |
|---|---|
| `pad_cell_before_C2.png` | the pad cell as committed on `toplevel` 8a72dd8, before C2: y 0–88 drawn, y 88–178 empty |
| `F_floorplan_stage1.png` | F stage 1 (16:58): floorplan variants 1 (recommended) and 2, F's own render |
| `K_cv_candidates.png` | K stage 2: C(V) per µm² of every candidate (hv PMOS, S-Varicap, moscap_p / _n, MOM), K's own plot |
| `K_cv_thick_oxide.png` | K stage 2: the thick-oxide candidates (hv PMOS, S-Varicap) |
| `K_c_along_swing.png` | K stage 3: capacitance of CMA / CMB and of the splits along the pad's DC swing |
| `K_step_response.png` | K stage 4: closed-loop step at 1 kΩ ∥ 100 pF, present caps and variants |
| `N_sinks_6x6_c.png` | N's cell sinks_6x6_c (delivered about 17:37, passed the lead's check 17:45), N's own render |
| `N_d2s_casc_n_c.png` | N's cell d2s_casc_n_c (delivered about 17:37, passed the lead's check 17:45), N's own render |
| `N_d2s_ab_n_c.png` | N's cell d2s_ab_n_c (delivered about 17:37, passed the lead's check 17:45), N's own render |
| `N_d2s_pd_n_c.png` | N's cell d2s_pd_n_c (delivered about 17:37, passed the lead's check 17:45), N's own render |
| `P_d2s_inputs_c.png` | P's cell d2s_inputs_c (delivered about 17:52, passed the lead's check 17:55), P's own render |
| `P_d2s_tails_c.png` | P's cell d2s_tails_c (delivered about 17:52, passed the lead's check 17:55), P's own render |
| `P_d2s_loads_c.png` | P's cell d2s_loads_c (delivered about 17:52, passed the lead's check 17:55), P's own render |
| `P_d2s_casc_p_c.png` | P's cell d2s_casc_p_c (delivered about 17:52, passed the lead's check 17:55), P's own render |
| `P_d2s_ab_p_c.png` | P's cell d2s_ab_p_c (delivered about 17:52, passed the lead's check 17:55), P's own render |
| `P_d2s_pd_p_c.png` | P's cell d2s_pd_p_c (delivered about 17:52, passed the lead's check 17:55), P's own render |
| `F_stage2_bias_tree_pd_cell.png` | F stage 2 (about 17:50), F's own render |
| `F_stage2_d2s_rhigh_cell.png` | F stage 2 (about 17:50), F's own render |
| `F_stage2_floorplan_v1_stage2.png` | F stage 2 (about 17:50), F's own render |
| `F_stage2_pad_stage2_cma_ring_left.png` | F stage 2 (about 17:50), F's own render |
| `F_stage2_pad_stage2_cma_ring_right.png` | F stage 2 (about 17:50), F's own render |
| `F_stage2_pad_stage2_isolator_left.png` | F stage 2 (about 17:50), F's own render |
| `F_stage2_pad_stage2_left_edge_top.png` | F stage 2 (about 17:50), F's own render |
