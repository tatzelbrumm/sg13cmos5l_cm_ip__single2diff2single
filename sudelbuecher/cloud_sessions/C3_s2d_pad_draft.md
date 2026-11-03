<!--
SPDX-FileCopyrightText: 2026 Christoph Maier
SPDX-License-Identifier: Apache-2.0
-->
# C3 (draft): layout of the `sg13cmos5l_IOPadSingle2Diff` pad cell, bottom-up with agents

**Status: draft for Christoph's review, 2026-11-03.** Open points are marked **[decide]**; they are collected at the
end.

Claude Code cloud session, environment `sg13cmos5l` (setup script of `github.com/tatzelbrumm/claude-cloud-config`).
The same method as C2 (`sudelbuecher/cloud_sessions/C2_pad_cram_draft.md`): compact primitives from agents, a
floorplan / assembly agent, and the lead checks every delivery independently. **C2's sections "Rules", "ESD, as far as
IHP has published it" (the parts that apply to an input pad), "Cost rules" and "Session mechanics" apply unchanged**;
this brief only lists what differs.

## What differs from C2

- **No pad cell exists yet.** `macros/sg13cmos5l_IOPadSingle2Diff/layout/klayout/` is empty. The pad cell is built
  from scratch.
- **The protection is IHP's own.** `CP` / `CN` (`Clamp_P20N0D` / `Clamp_N20N0D`, gate-tied), `DN` / `DP`, `SP`
  (`SecondaryProtection`, 587 Ω rppd, `pad` → `padres`) are exactly `sg13cmos5l_IOPadAnalog`
  (`sudelbuecher/sg13cmos5l_IOPadAnalog/sg13cmos5l_IOPadAnalog_real_hierarchy.spi`). Start from IHP's
  `IOPadAnalog` layout (`libs.ref/sg13cmos5l_io/gds/`): keep its protection and rings as they are, and put the s2d
  amplifier in the free core-side area. No output drivers, no CMA / CMB, so no agent K.
- **The amplifier is `s2d_mpdda_pd`** (four signal units, CMFB cross-quad, folded cascode, two 12 × 12 µm hv NMOS load
  capacitors). Its input `padres` drives gates only.
- **Area is the risk.** `layout_primitives.md` §4: `s2d_mpdda_pd` alone ≈ 5500 µm² with spacing against ≈ 6500 µm²
  above the ESD zone, before the bias tree. The levers are listed there, biggest first.

## Read first

`CLAUDE.md`; this brief; C2's brief (the sections named above); C2's `HANDOFF.md`, `decisions.md` and `report.md` §1
in `sudelbuecher/design_considerations/pad_buffer_layout/pad_cell_2026-10-31/`; Christoph's reviews of C2's primitives
(`sudelbuecher/sg13cmos5l_IOPadDiff2Single_build/agents_c2/P2/out/d2s_p2_cells_human_review.txt`,
`…/N2/out/d2s_n2_cells_human_review.txt`) and his symmetry rule in `decisions.md` (about 18:55);
`layout_primitives.md` §1–6; `macros/sg13cmos5l_IOPadSingle2Diff/README.md` and `FILL_IN.md`.

## Phase 0, lead: tools

As C2 phase 0, plus C2's environment fix **before any DRC or LVS run**: the PDK checkout is sparse and leaves IHP's
main DRC deck and 45 LVS decks as dangling links, and `run_drc.py` then prints "Passed" while every table crashes.
`git -C /foss/pdks/IHP-Open-PDK sparse-checkout add /ihp-sg13g2/libs.tech/klayout/tech/`; then no dangling link
under `ihp-sg13cmos5l/libs.tech/klayout`; grep every `run_drc.py` log for "exception".

## Phase 1, lead: frame, partition, budget

1. **Frame from `IOPadAnalog`:** its outline, rings and bands; the free core-side region (x, y ranges); the row
   `Filler1000 | IOPadAnalog | pad cell | Filler200 | IOPadIOVdd | pad cell | Filler1000` with C2's `row_check.py`
   (DRC with latch-up on, one net per rail and band). Use C2's `phase1/` results; measure only what differs.
2. **Partition** of `sg13cmos5l_IOPadSingle2Diff.sch`, as C2's: in the cell `xa` (`s2d_mpdda_pd`), `CP` `CN` `DN` `DP`
   `SP`; `xt` (`bias_tree_noab_pd`) if it fits; out to the slot `xg` (`bias_gen_pd`) and `xc` (`en_ctrl_3v3`).
   **[decide]** whether the load capacitors (`s2d_cload`) stay in the cell (lever 3 of §4).
   The cell's new ports and sheet as proposals; the slot sheet is not changed. The symbol problem of C2's
   `HANDOFF.md` ("Known problem for the backannotation") applies here too: follow what Christoph decides for C2.
3. **Budget** of every block, compacted, against the free region. **Stop condition:** if `xa` doesn't fit even
   compacted, stop after phase 1 and report which levers of §4 would make it fit.
4. `report.md`, commit, push.

## Phase 2, agents P and N (in parallel): compact primitives

Cells (from `pad_buffer_layout/klayout/pad_buffer_cells.{gds,cdl}`):
- **P:** input tubs `tub_p20x1` (12 tubs in s2d), `s2d_tails`, `s2d_loads`, `s2d_casc_p`, `s2d_pd_p`;
- **N:** `s2d_sinks_cmfb`, `s2d_casc_n`, `s2d_pd_n`, `s2d_cload`, `s2d_rhigh`; the fold sinks as N2's
  `sinks_6x6_s2d_c2` (`agents_c2/N2/out/`), checked, not redrawn.

Apply Christoph's review rules of C2 from the start, not after a rejection: symmetric rows along the line between
the rows with symmetric dummies (never dummies on one side only); taps as rings where space allows; no well notches;
the dummy-tie convention **[decide]** (C2 open decision 3). Reuse P2's / N2's code and C2's `sym_check.py`. The
deliverables and the lead's checks as in C2 phase 2.

## Phase 3, agent F: floorplan and assembly

Stage A, placement only, from the drawn cells in the pad context (C2 decision of about 17:55: bottom-up, nothing
forced on P / N); then **Christoph's review of the placement picture**; stage B, routing, after his go. F may change
its copies of P's and N's cells (`<cell>_f`, every change listed). Lead checks as in C2 phase 3.

## Phase 4, lead: integration

As C2 phase 4, for `macros/sg13cmos5l_IOPadSingle2Diff/layout/klayout/sg13cmos5l_IOPadSingle2Diff.klay.gds` (new file,
no backup needed). Backannotation of `s2d_mpdda.sch` / `s2d_mpdda_pd.sch` / the pad sheet and
`netlist/source/*.spice`; DRC / LVS with the macro Makefile targets (`SCRIPTS_DIR=../../scripts`); the row checks on
the final cell; the CACE note (14 groups in `sg13cmos5l_IOPadSingle2Diff.yaml` and `s2d_mpdda_pd_sel.yaml`).

## Models

| role | model, effort | why |
|---|---|---|
| lead | Opus, high | as C2 |
| P, N | Opus, high | C2's first attempt with Sonnet was rejected (2026-10-31 18:55) |
| F | Opus, high | as C2 |

## Parallel with C2

C3 changes none of C2's files and no shared macro (C2 rule 4). Shared cells (`tub_p20x1`, `sinks_6x6`) are copied
under C3 names. **[decide]** start now, in parallel with C2's stage B, or after C2's routing is through, so that F's
lessons from routing reach C3.

## Git, for this task only (Christoph's permission)

- Design branch `claude/c3-s2d-pad-layout` from `toplevel`, for `macros/sg13cmos5l_IOPadSingle2Diff/` only.
- Notes branch `claude/c3-s2d-pad-layout-sudel` from `sudel_buecher`, as worktree `../sudel`.
- Both created by Christoph before the start; the session pushes to them (fast-forward only). Never push `main`,
  `toplevel` or `sudel_buecher`; no tags, no force pushes, no merges.
- Notes: `sudelbuecher/design_considerations/pad_buffer_layout/pad_cell_s2d/` (report, checks, decisions);
  agents `sudelbuecher/sg13cmos5l_IOPadSingle2Diff_build/agents_c3/<role>/` with brief, messages, report, `out/`,
  `work/`; logs `sudelbuecher/logs/claude/c3-s2d-pad-layout/`.

## Open decisions, collected

1. Start now in parallel with C2, or after C2's stage B.
2. `s2d_cload` in the cell or outside.
3. Dummy-tie convention (C2 open decision 3).
4. The pad symbol / ports problem: as decided for C2.
