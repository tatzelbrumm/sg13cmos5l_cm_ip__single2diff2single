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
