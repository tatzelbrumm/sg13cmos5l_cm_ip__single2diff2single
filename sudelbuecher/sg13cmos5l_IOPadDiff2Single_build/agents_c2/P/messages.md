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
