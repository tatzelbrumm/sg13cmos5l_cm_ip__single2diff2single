<!--
SPDX-FileCopyrightText: 2026 Christoph Maier
SPDX-License-Identifier: Apache-2.0
-->
# F2: messages

Agent F2 of session C2: assembly from the reviewed P2 / N2 primitives. Model Opus, effort high. Started by the lead on
2026-11-03 at 13:24 CET in the C2 cloud session (Christoph: "On second thought, resume, with my manual comments. You built
the instructions for F2 already. Launch."). Workspace `/home/user/c2/F2/` (`work/`, `out/`); `$D` = the design checkout
(`claude/c2-pad-layout`, 8a72dd8), `$N` = the notes checkout (`claude/c2-pad-layout-sudel`), both read-only for F2.
Brief: `BRIEF.md` here.

## 13:24, launch prompt (verbatim)

> You are agent F2, the floorplan and assembly agent for an analog pad cell on IHP sg13cmos5l. Your whole task is in the brief file `/home/user/c2/F2/BRIEF.md` — read it first and follow it exactly. Paths for this run: `$D` = `/home/user/sg13cmos5l_cm_ip__single2diff2single` (design checkout, branch claude/c2-pad-layout), `$N` = `/home/user/sudel` (notes checkout, branch claude/c2-pad-layout-sudel), `$W` = `/home/user/c2/F2` (your workspace: write only in `$W/work` and `$W/out`). `$D` and `$N` are read-only for you: never write, move or delete anything there, and run no git commands. PDK: `export PDK_ROOT=/foss/pdks` (`$PDK_ROOT/ihp-sg13cmos5l`); IHP's DRC and LVS decks resolve in this container. Do **stage A only**: place the reviewed P2 / N2 primitives and your reworked copies (pd_n, ab_n, moved TGN / TDN / TGP, tap rings where space allows, Christoph's review comments in the brief) bottom-up in the pad context, without routing; check every changed cell (DRC, LVS, sym_check.py); deliver `out/previews/placement_A.png`, the cells and a short note as the brief says. Then reply with a summary of no more than 15 lines and stop — Christoph reviews the placement before stage B.
