<!--
SPDX-FileCopyrightText: 2026 Christoph Maier
SPDX-License-Identifier: Apache-2.0
-->
# C3: Christoph's decisions (verbatim, Europe/Berlin)

| time | words | consequence |
|---|---|---|
| 2026-11-03 18:34 (brief) | "In parallel, if c2 isn't finished." | C2 was finished when C3 started (its notes branch ends with the C2 chat log, 2d0fb2d). C3 ran on its own, and C2's files stayed untouched. |
| 2026-11-03 18:34 (brief) | "If the load capacitors are within the pad layout, keep them there. If not, export. If it's not clear whether the capacitors will fit, keep them in for now." | Phase 1 shows that `xa` does not fit with them (report §1.3). Under this rule they went out to the slot on IHP's frame. On template version 4 they fit (tentative fit A), so they stay in (decision of about 20:30). |
| 2026-11-03 18:34 (brief) | "Dummy source and drain to the rails, gate net by abutment where dummies extend abutted gate poly." | Written into the phase 2 briefs of P and N (`agents_c3/`). |
| 2026-11-03 18:34 (brief) | "new ports to follow layout." | Report §1.2, the port list as C2's option B. |
| 2026-11-03 about 20:30 | "Go with A. Start having the specialist agents compact the layout primitives and then have the laout builder further compact the entire layout." | Fit variant A: all of `xa`, the load capacitors and `xt` in the cell. Phase 2 started 20:33: agents P (PMOS: tubs / inputs, tails, loads, casc_p, pd_p, bias_tree_noab_p) and N (NMOS / R: sinks_6x6_s2d from N2's cell, sinks_cmfb, casc_n, pd_n, cload, rhigh, bias_tree_noab_n), both Opus, effort high. Briefs `agents_c3/{P,N}/BRIEF.md`, with Christoph's C2 review rules and C3 decision 3 from the start. Then agent F: placement and compaction (stage A), then Christoph's review of the placement before routing (the brief). |
| 2026-11-04 about 13:00 (review of F's stage A) | "1. Great choice to split the tails! 2. I'll go with your choice to omit the isolator ring. 3. I approve." and "Consider abutment of this pad with IHP sg13cmos5l_IOPad standard cells; if you can, leave some space at the long edges of the pads for placing guard/diffusion/well tap structures as they may become necessary." and "go ahead!" | 1: F's `s2d_tails_hi_f` / `s2d_tails_lo_f` stay. 2: no isolator between the ESD zone and the buffer. 3: the NMOS power-down pair stays inside `s2d_cload_c3`. Edge reserve for F (stage B): x 1.8–4.3 and 75.7–78.2 (2.5 µm inside each edge strip, along the long edges) kept free of the buffer's device layers and M1, or as much as fits, reported per y range. Stage B (routing, pad candidate) started; brief addendum `agents_c3/F/BRIEF_stageB.md`. |

Open for Christoph: none at the moment. The levers of report §1.4 are not needed on template version 4 (fit A); he
reviewed F's stage A on 2026-11-04 (row above).
