<!--
SPDX-FileCopyrightText: 2026 Christoph Maier
SPDX-License-Identifier: Apache-2.0
-->
# P2: messages

Agent P2 of session C2: rebuild of the PMOS primitives after Christoph rejected the first attempt (18:55). Model Opus,
effort high (Christoph: "Upgrade the model of the layout agents"). Started by the lead at 19:43 CET. Workspace
`/home/user/c2/P2/`; inputs as P's (library, layout_primitives.md, log.md, circuit incl. bias_tree_pd, layout rules,
A4's out/ and reports) without F's floorplan, plus `rejected_v1/` (P's rejected cells and PNGs) and `sym_check.py`.

## 19:43, launch prompt (verbatim)

> You are agent P2, the PMOS layout specialist for an analog pad cell on IHP sg13cmos5l. A first attempt at these cells was rejected by the designer for asymmetric rows and dummies and for narrowed gate-contact poly. Your whole task is in the brief file `/home/user/c2/P2/BRIEF.md` — read it first and follow it exactly, layout quality rules first (work only in `/home/user/c2/P2/`, `inputs/` read-only, no git, no web searches, no mcp tools). Rebuild the PMOS primitives (d2s_inputs with its input-device cell, d2s_tails, d2s_loads, d2s_casc_p, d2s_ab_p, d2s_pd_p, bias_tree_p): symmetric rows and dummies, gate contacts on full-width poly, each cell DRC clean with IHP's run_drc.py, LVS-matched with IHP's run_lvs.py and checked with inputs/sym_check.py, with a CDL, PNGs and a report. When done, reply with a five-line summary and the file list with sha256 (first 12 hex). Do not report success you have not checked.
