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

## about 20:30, P2's reply (summary)

Eight cells in `d2s_p2_cells.gds` (f79e87d1d221): tub_p20x1_c2 5.32 × 11.24, d2s_inputs_c2 40.92 × 26.44 (12 tubs, deep-mode
LVS), d2s_tails_c2 34.69 × 14.81, d2s_loads_c2 30.69 × 13.67 (folded `L R R L` / `R L L R`), d2s_casc_p_c2 35.66 × 13.67,
d2s_ab_p_c2 8.48 × 9.00, d2s_pd_p_c2 3.71 × 2.97, bias_tree_p_c2 18.19 × 9.32; mirror symmetry built in (M90 halves, M0
rows), dummies in pairs, BP with a full twin, BPC on the axis with a twin; gate contacts on poly tabs as long as the gate
or on full-width heads; DRC 0, LVS match, sym_check 0. The harness refused `report.md`; its text is in `report.md` here.

## the lead's check

`lead_check.py`: XOR against a rebuild empty, own DRC clean (no exceptions), own LVS match (inputs in deep mode), device
tables equal to the circuit (inputs checked on the hierarchical extraction: A y←vinp / x←vref, B y←vref / x←vinn, C1 / C2
y←vref / x←vfb, tub 20/1 bulk = source). `sym_check.py`: 0 on every cell. Waiting for Christoph's review.
