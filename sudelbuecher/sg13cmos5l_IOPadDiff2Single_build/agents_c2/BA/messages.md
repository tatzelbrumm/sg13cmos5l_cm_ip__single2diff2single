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

## about 16:40, BA's reply (summary)

Sheets, symbols, source netlists of the pad match `pad_candidate.cdl` device for device (BA's own compare tool, which also
catches a planted error); users rewired (8 templates, slot, top, tb_pad_dc.spice); tb_pad_dc runs, I_Q +2.2 % (SX / SY ng 6).
Open: XMDBN (bias-tree dummy on ni, internal to bias_tree_pd). Report: `report.md`.

## the lead's integration and check

Files copied into the design branch. make klayout-lvs / magic-lvs first failed on: DCN / DCP as IHP's subckt symbols (drawn
diodes are 67.6 / 65.8 µm long) → replaced by drawn dantenna / dpantenna pairs (lead); no top-level port labels in the
layout → `add_top_labels.py` (texts only, geometry XOR empty). Remaining: the ni dummy, and vss / iovss joined through the
substrate under --disable_tap_extraction (the vss band ptap of the edge contract). Decisions for Christoph.
