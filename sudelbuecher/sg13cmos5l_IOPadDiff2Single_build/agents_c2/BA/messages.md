<!--
SPDX-FileCopyrightText: 2026 Christoph Maier
SPDX-License-Identifier: Apache-2.0
-->
# BA: messages

Agent BA of session C2: backannotation of the drawn pad cell into the sheets, symbols, source netlists and CACE
harnesses. Model Opus, effort high. Started by the lead on 2026-11-03 at about 16:15 CET. Workspace `/home/user/c2/BA/`
(`work/` = a copy of the design branch with the new layout integrated; `inputs/`: F2's `pad_candidate.cdl`,
`netlist_changes.md`, `report_stageB.md`, `decisions.md`, `circuit_vs_cdl.py`, bg_core_pd's `bg_sheet_ba.py`).

## about 16:15, launch prompt (verbatim)

> You are agent BA, backannotating xschem schematics, symbols, source netlists and CACE harnesses of an analog pad cell (IHP sg13cmos5l) to its drawn layout. Your whole task is in `/home/user/c2/BA/BRIEF.md` — read it first and follow it exactly (edit only the repository copy in `/home/user/c2/BA/work/`, `inputs/` read-only, notes and checks in `out/`, no git, no web searches). The device-level truth is `/home/user/c2/BA/inputs/pad_candidate.cdl`. When done, reply with a summary of no more than 12 lines and the list of changed files; do not report success you have not checked.
