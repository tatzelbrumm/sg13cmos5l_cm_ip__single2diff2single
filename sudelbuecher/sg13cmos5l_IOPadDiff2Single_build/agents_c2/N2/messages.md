<!--
SPDX-FileCopyrightText: 2026 Christoph Maier
SPDX-License-Identifier: Apache-2.0
-->
# N2: messages

Agent N2 of session C2: rebuild of the NMOS primitives after Christoph rejected the first attempt (18:55). Model Opus,
effort high (Christoph: "Upgrade the model of the layout agents"). Started by the lead at 19:43 CET. Workspace
`/home/user/c2/N2/`; inputs as N's (library, layout_primitives.md, log.md, circuit incl. bias_tree_pd, layout rules,
A3's out/ and reports) without F's floorplan, plus `rejected_v1/` (N's rejected cells, F's rejected d2s_rhigh, PNGs), bg_res_c and `sym_check.py`.

## 19:43, launch prompt (verbatim)

> You are agent N2, the NMOS layout specialist for an analog pad cell on IHP sg13cmos5l. A first attempt at these cells was rejected by the designer for asymmetric rows and dummies and for narrowed gate-contact poly. Your whole task is in the brief file `/home/user/c2/N2/BRIEF.md` — read it first and follow it exactly, layout quality rules first (work only in `/home/user/c2/N2/`, `inputs/` read-only, no git, no web searches, no mcp tools). Rebuild the NMOS primitives (sinks_6x6 with an s2d variant, d2s_casc_n, d2s_ab_n, d2s_pd_n, bias_tree_n) and the resistor block d2s_rhigh: symmetric rows and dummies, gate contacts on full-width poly, each cell DRC clean with IHP's run_drc.py, LVS-matched with IHP's run_lvs.py and checked with inputs/sym_check.py, with a CDL, PNGs and a report. When done, reply with a five-line summary and the file list with sha256 (first 12 hex). Do not report success you have not checked.
