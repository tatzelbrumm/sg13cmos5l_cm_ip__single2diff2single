<!--
SPDX-FileCopyrightText: 2026 Christoph Maier
SPDX-License-Identifier: Apache-2.0
-->
# C2 handoff: where the pad-cell layout stands, and what the next lead session does (2026-11-03)

Written by the C2 cloud lead session before handing over to a session on Christoph's regular quota. Everything named
here is on the two branches; nothing lives only in the old cloud container.

## Branches and folders

| what | where |
|---|---|
| design branch (macro changes go here) | `claude/c2-pad-layout` — still identical to `toplevel` 8a72dd8; nothing integrated yet |
| notes branch | `claude/c2-pad-layout-sudel` |
| the task brief | `sudelbuecher/cloud_sessions/C2_pad_cram_draft.md` (final; "(draft)" is part of the name); launch prompt `C2_launch_prompt` |
| lead's report, decisions, scripts | `sudelbuecher/design_considerations/pad_buffer_layout/pad_cell_2026-10-31/` (`report.md`, `decisions.md` = Christoph's words verbatim, `HANDOFF.md` = this, `row_check.py`, `path_widths.py`, `lead_check.py`, `sym_check.py`, `render.py`, `lead_checks/`, `previews/`, `phase1/`) |
| agents | `sudelbuecher/sg13cmos5l_IOPadDiff2Single_build/agents_c2/`: `K/` (capacitors, done), `P2/`, `N2/` (rebuilt primitives, reviewed), `F2/BRIEF.md` (next), `rejected_v1/` (first attempt, archived) |
| logs | `sudelbuecher/logs/claude/c2-pad-layout/` (+ rows in `sudelbuecher/MANIFEST.tsv`) |

Local layout (docs/local-container.md): design worktree `~/EDA/sg13cmos5l_cm_ip__single2diff2single`, notes worktree
`~/EDA/sg13cmos5l_cm_ip__single2diff2single_sudelbuecher`; in the IIC-OSIC-TOOLS container under `/foss/designs/`.
Never switch the design worktree to a notes branch.

## Done

- **Phase 0** (tools) and **phase 1** (abutment, row DRC with latch-up, partition, budget): `report.md` §0–1. The row
  check found the present pad cell lacks the four upper bands; the partition keeps Xd, Xt, Xfp / Xfn, CMA / CMB, DCN /
  DCP in the cell, moves Xg and Xc to the slot; new ports `iovdd iovss vdd vss pad vinp vinn vref iref en_3v3 en_3v3_b`.
- **Agent K** (capacitors, 6 stages, `agents_c2/K/report.md`): keep CMA; CMB options keep / keep behind IHP's secondary
  stage (rppd 587 Ω or 2 kΩ + dantenna + dpantenna; loop unchanged) / turn around; the loop's voltage dependence is the
  driver's (sourcing half near the top rail: PM 39.7° at 300 pF, GM 16.8 dB), not the capacitors'.
- **Primitives:** first attempt rejected (2026-10-31 18:55); rebuilt by P2 / N2 (Opus), lead-checked (XOR vs rebuild,
  IHP DRC + latch-up, IHP LVS, device tables vs circuit, `sym_check.py`), **reviewed by Christoph** (`P2/out/` and
  `N2/out/d2s_[np]2_cells_human_review.txt`).

## Open decisions (Christoph)

1. **CMB:** keep as drawn / keep behind the secondary stage (2 kΩ recommended by the lead on ESD grounds) / turn around
   (its own well and ring; **never** a shared well with CMA). F2 keeps CMB as drawn and reserves room for the stage.
2. **CACE proposal:** add the output offset (vref, vref ± 0.65 V) as a condition of `loop_params` / `loop_load_params`
   in `d2s_mpdda_pd_sel.yaml` (CACE checks only at vref and misses the worst GM and the worst 300 pF PM).
3. **Dummy ties:** N2 tied NMOS dummies D = S = G to the gate net, P2 tied PMOS dummies to vdd. One convention.
4. **BP position:** at a row end with full twins (P2) or in the middle (as N2 did with BN).
5. **F2's model:** Opus, effort high (as F); Fable is the next tier under the brief's rule. Effort never above high.

## Next steps for the lead session

1. **Set up F2's workspace** outside the repos, e.g. `~/EDA/c2_work/F2/{work,out}`, and start F2 as a background
   subagent with `agents_c2/F2/BRIEF.md`, giving it the absolute paths of the two worktrees (`$D`, `$N`) and `$W`.
   F2 does **stage A (placement) only**, then stops.
2. **Check stage A** (DRC / LVS / `sym_check.py` of every changed cell, with `lead_check.py`), copy F2's `out/` and
   `work/` into `agents_c2/F2/`, send Christoph the placement picture, and **wait for his review**.
3. **Stage B** (routing, pad candidate) after his go; check it the same way plus `row_check.py` and `path_widths.py` on
   the whole pad (compare with `phase1/`).
4. **Phase 4** of the brief (`C2_pad_cram_draft.md`): back up the cell to `layout/klayout/backups/`, write the pad
   candidate into the macro, delete the 63/0 TEXT.drawing box; backannotate sheets and source netlists from F2's
   `netlist_changes.md`; DRC / LVS with the macro Makefile targets (`klayout-drc`, `klayout-lvs`, `magic-drc`,
   `magic-lvs-netlist`, `magic-lvs`, `SCRIPTS_DIR=../../scripts`); the row checks on the final cell; the CACE note; the
   open points of 2026-10-28.
   - **Known problem for the backannotation:** the pad's symbol `sg13cmos5l_IOPadDiff2Single.sym` is used by
     `macros/slot/schematic/xschem/slot.sch`, the project top `schematic/xschem/sg13cmos5l_cm_ip__single2diff2single.sch`
     and 8 CACE templates (`verification/cace/templates/*_tb_*.sch`). The partitioned cell has different ports, and the
     slot sheet must not change in this task. Decide with Christoph before editing: e.g. a new cell sheet for the layout
     plus a wrapper that keeps the old symbol (Xc, Xg + the new cell), or the new ports with the templates updated.
5. Keep `report.md` and `decisions.md` current; commit and push the notes branch after every finished step (a crash
   then loses at most the step in progress).

## Environment notes

- In the old cloud container the PDK checkout was sparse and IHP's main DRC / most LVS decks were dangling links;
  `run_drc.py` then printed "Passed" while 30 tables crashed. Locally, check once:
  `ls -la $PDK_ROOT/ihp-sg13cmos5l/libs.tech/klayout/tech/drc/rule_decks/layers_def.drc` must resolve, and grep every
  `run_drc.py` log for "generated an exception".
- `sym_check.py` is the symmetry test (mirror XOR of device layers, necked gate-contact poly). The narrow-poly test is a
  heuristic; Christoph's review is the real check.
- Local sessions: read `docs/local-container.md` and the "Local-only" section of `docs/traps.md` first (CLAUDE.md).
