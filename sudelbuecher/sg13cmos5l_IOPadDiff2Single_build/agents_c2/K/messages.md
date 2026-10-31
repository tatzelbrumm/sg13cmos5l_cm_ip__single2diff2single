<!--
SPDX-FileCopyrightText: 2026 Christoph Maier
SPDX-License-Identifier: Apache-2.0
-->
# K: messages

Agent K of session C2 (capacitors for CMA / CMB, with ngspice). Model Opus, effort medium (brief C2, table "Models").
Started by the lead on 2026-10-31 at about 16:22 CET, in the cloud session's container. Workspace `/home/user/c2/K/`
(`inputs/` read-only: a `git archive` of `toplevel` 8a72dd8 as `inputs/repo/`, and `inputs/notes/` with A5's brief,
A5's `inputs.md`, the two PDK PDFs as text from A5's `work/txt/`, `layout_primitives.md`, the ESD notes, C1's report).

## about 16:22, launch prompt (verbatim)

> You are agent K, an investigative agent for an analog IC designer working on the IHP sg13cmos5l process. Your whole task is in the brief file `/home/user/c2/K/BRIEF.md` — read it first and follow it exactly, including its rules (work only in `/home/user/c2/K/`, `inputs/` read-only, no git, no web searches, no mcp tools). The question is whether the Miller capacitors CMA and CMB of the output pad (two hv PMOS MOS capacitors, 256 µm² gate area each) can be replaced by, or split between, other capacitor types of the PDK so that capacitance remains over the whole output swing, with ngspice C(V), a DC swing of the pad, and the loop's phase margin for the best splits. Write results in four stages into `/home/user/c2/K/out/report.md` and announce each stage in `out/announcements.md` as the brief says. When done, reply with a summary of no more than 15 lines: the short answers, the recommended option with its area and phase margin, and the open points.
