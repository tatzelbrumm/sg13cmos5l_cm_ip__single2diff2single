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

## about 20:20, N2's reply (summary)

Seven cells in `d2s_n2_cells.gds` (dfe0d001eda6): sinks_6x6_c2 51.68 × 16.51 (+ s2d variant R90), d2s_casc_n_c2 40.70 × 12.41,
d2s_ab_n_c2 20.68 × 4.02, d2s_pd_n_c2 4.73 × 2.95, bias_tree_n_c2 30.26 × 8.59, d2s_rhigh_c2 13.80 × 17.29; unmodified
nmosHV PCells, the same narrow dummy at both ends of every row; BN / BNC / NI / RN2 in the middle of their maps, BN with a
twin; gate contacts in columns on poly as tall as the gate; DRC 0, LVS match, sym_check residuals only on Cont of the
centre PCell. Dummies tied D = S = G to the gate net (not vss).

## the lead's check

`lead_check.py`: XOR against a rebuild empty, own DRC clean (no exceptions), own LVS match, device tables equal to the
circuit (resistors: series-reduced by LVS, 4 × 0.5/50.6 + 2 dummies). `sym_check.py`: casc_n, pd_n, rhigh 0; sinks
0.0768 µm², ab_n 0.0256, bias_tree_n 0.0384 µm², all on Cont of the centre device. Waiting for Christoph's review.
