<!--
SPDX-FileCopyrightText: 2026 Christoph Maier
SPDX-License-Identifier: Apache-2.0
-->
# P: messages

Agent P of session C2 (compact PMOS primitives of d2s_mpdda_pd). Model Sonnet, effort medium. Started by the lead on
2026-10-31 at 17:00 CET. Workspace `/home/user/c2/P/`; inputs: the library `pad_buffer_klayout/` (generator, GDS, CDL,
README, cell tree, Q&A, verification), `layout_primitives.md`, `log.md`, the circuit (`circuit/`: pad netlists,
`d2s_mpdda_pd.sch`, `unit_r2.sch`), the layout rules as text, the project CLAUDE.md, A4's briefs / reports / `out/`,
F's floorplan (`F_floorplan_stage1.png` / `.md`). Brief: `BRIEF.md` here (F's requests of 16:58 inserted verbatim).

## 17:00, launch prompt (verbatim)

> You are agent P, the PMOS layout specialist for an analog pad cell on IHP sg13cmos5l. Your whole task is in the brief file `/home/user/c2/P/BRIEF.md` — read it first and follow it exactly, including its rules (work only in `/home/user/c2/P/`, `inputs/` read-only, no git, no web searches, no mcp tools). Draw the compact PMOS cells of d2s_mpdda_pd (d2s_inputs with its tubs, d2s_tails, d2s_loads, d2s_casc_p, d2s_ab_p, d2s_pd_p) to the outlines, orientations and pins that the assembly agent F requested (in the brief), each DRC clean with IHP's run_drc.py and LVS-matched with IHP's run_lvs.py, with a CDL, a PNG per cell and a report. When done, reply with a five-line summary and the file list with sha256 (first 12 hex). Do not report success you have not checked.

## about 17:52, P's final reply (summary)

Six cells in `d2s_p_cells.gds` (d5e68567941f), each DRC 0 and LVS match: inputs 32.05 × 26.71, tails 32.27 × 14.81, loads
11.32 × 30.02, casc_p 11.32 × 33.64, ab_p 6.01 × 7.90, pd_p 3.71 × 2.97. Netlist changes: SA's bulk vdd; tail dummies
2 × 0.3/6 + 1 × 5/6, BP at the right end of row 2; dummy tubs 10/1 ng=1; casc_p stacked columns. Notes for F: tails +2.47 µm
x shift, loads pins ≈ 1 µm off casc_p's, inputs `y` pin 0.5 µm above F's limit.

## 17:55, the lead's check

`lead_check.py` (notes: `pad_cell_2026-10-31/lead_checks/P/`): XOR against a rebuild with `build_d2s_p.py` empty, own
run_drc.py clean (no exceptions), own run_lvs.py match, device tables equal to the circuit. Passed to F (`/home/user/c2/F/inputs_P/`).
