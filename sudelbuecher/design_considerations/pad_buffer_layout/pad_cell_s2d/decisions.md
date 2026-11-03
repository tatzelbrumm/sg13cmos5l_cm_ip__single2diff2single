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

Open for Christoph: none at the moment. The levers of report §1.4 are not needed on template version 4 (fit A); his
review of F's placement comes after phase 3 stage A.
