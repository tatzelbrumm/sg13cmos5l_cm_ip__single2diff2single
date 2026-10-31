<!--
SPDX-FileCopyrightText: 2026 Christoph Maier
SPDX-License-Identifier: Apache-2.0
-->
# N: messages

Agent N of session C2 (compact NMOS primitives of d2s_mpdda_pd). Model Sonnet, effort medium. Started by the lead on
2026-10-31 at 17:00 CET. Workspace `/home/user/c2/N/`; inputs: the library `pad_buffer_klayout/` (generator, GDS, CDL,
README, cell tree, Q&A, verification), `layout_primitives.md`, `log.md`, the circuit (`circuit/`: pad netlists,
`d2s_mpdda_pd.sch`, `unit_r2.sch`), the layout rules as text, the project CLAUDE.md, A3's briefs / reports / `out/`,
F's floorplan (`F_floorplan_stage1.png` / `.md`). Brief: `BRIEF.md` here (F's requests of 16:58 inserted verbatim).

## 17:00, launch prompt (verbatim)

> You are agent N, the NMOS layout specialist for an analog pad cell on IHP sg13cmos5l. Your whole task is in the brief file `/home/user/c2/N/BRIEF.md` — read it first and follow it exactly, including its rules (work only in `/home/user/c2/N/`, `inputs/` read-only, no git, no web searches, no mcp tools). Draw the compact NMOS cells of d2s_mpdda_pd (sinks_6x6 upright, d2s_casc_n, d2s_ab_n, d2s_pd_n) to the outlines, orientations and pins that the assembly agent F requested (in the brief), each DRC clean with IHP's run_drc.py and LVS-matched with IHP's run_lvs.py, with a CDL, a PNG per cell and a report. When done, reply with a five-line summary and the file list with sha256 (first 12 hex). Do not report success you have not checked.

## about 17:37, N's final reply (summary)

Five cells in `d2s_n_cells.gds` (8f040ee1249a): `sinks_6x6_c` 15.525 × 46.79 upright, `sinks_6x6_s2d_c` (R90), `d2s_casc_n_c`
9.73 × 33.12, `d2s_ab_n_c` 6.86 × 5.44, `d2s_pd_n_c` 3.52 × 2.04; DRC 0 and LVS match each; netlist changes in `report.md`.
Question: SB's bulk is vsso in `d2s_mpdda_pd`, but the layout has one substrate (vss).

## 17:45, the lead's check and decision

`lead_check.py` (notes: `pad_cell_2026-10-31/lead_checks/N/`): XOR against a rebuild with `build_d2s_n.py` empty, own
run_drc.py clean (no exceptions), own run_lvs.py match, device tables equal to the circuit. Passed to F (`/home/user/c2/F/inputs_N/`).
Decision: SB's bulk = vss in the cell; the backannotation changes XSB's bulk in `d2s_mpdda_pd` to vss (vsso = vss = iovss at
the pad level, so the flat pad LVS is unaffected).
