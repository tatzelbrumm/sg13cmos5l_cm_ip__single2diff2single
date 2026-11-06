# TASK FILE for a cloud agent: replica bias for the reference and common-mode inputs of the custom pads

Read this whole file before doing anything. Written 2026-11-06 on the user's request. It lives on branch `harness-test`
of `tatzelbrumm/sg13cmos5l_cm_ip__single2diff2single` (the design repository). A second task runs in parallel
(`docs/launch/slot7_testplatform_TASK.md`); the branch and directory rules below keep the two apart.

## Goal

The two custom pads need reference and common-mode voltages at their gate-only inputs:
`sg13cmos5l_IOPadSingle2Diff` (S2D): `vref` (input reference) and `vcm` (output common mode);
`sg13cmos5l_IOPadDiff2Single` (D2S): `vref` (output reference; check in its netlist what else depends on the input
common mode). Today they come from outside (CACE fixtures: ideal sources). A resistive divider from the 3.3 V rail
would cost several uA per tap and a lot of rhigh area. Build **replica bias blocks**: small circuits that generate
each voltage from the existing reference currents (about 5 uA from `oa_core_pd` / `bg_core_pd` / harness `ibias`,
distributed by the bias trees) with replicas of the devices whose operating window sets the optimum, so that the
voltage tracks process, temperature and iovdd the same way the window does, at a current well below a divider's.

Use only primitives that already exist in this repository: the device instances and units of the pads' schematics
(`s2d_mpdda`, `d2s_mpdda_pd`, `unit_r2`, the hv MOS sizes used there), `bg_core_pd`, `oa_core_pd`, `bias_tree_pd`,
`bias_tree_noab_pd`, `bias_dist_pd`, and their layouts where layouts exist. No new device types.

## Hard rules

1. Design repository: the user has created two branches for this task. Work and push only on them:
   **`claude/c4-replica-bias`** (from `toplevel`) for the design, and **`claude/c4-replica-bias-sudel`** (from the
   orphan branch `sudel_buecher`) for notes, logs and the chat log, checked out in a separate worktree
   (`git worktree add ../sg13cmos5l_cm_ip__single2diff2single_sudelbuecher claude/c4-replica-bias-sudel`; never switch
   the main checkout to it: an orphan branch empties the working tree). If either branch is missing, stop and tell the
   user. Never push to `main`, `toplevel`, `sudel_buecher`, `harness-test` or any other branch.
2. Do not touch `tatzelbrumm/sg13cmos5l_cm_slot7` or `tatzelbrumm/sg13cmos5l_ocd_chipalooza`. Migration of the result
   into the delivery repository is a later task: only write down what would move there.
3. Do not change the pad cells' layouts or their existing macros; new work goes into NEW macros under `macros/`
   (one per block, named e.g. `vref_s2d_rb`, `vcm_rb`, `vref_d2s_rb`; your choice, written down). Reusing a
   schematic of an existing macro as a symbol instance is fine.
4. Environment: `export PDK_ROOT=/foss/pdks; source .designinit` in the repo root before any `make` (see `CLAUDE.md`).
   Avoid `make all`. Traps listed in `CLAUDE.md` and `docs/traps.md` apply (CACE `-s` explicitly; PEX element counts,
   not diffs; mismatch MC on `-s schematic` only).
5. No spreadsheets, no Microsoft formats. Every command, assumption and number goes into the run log. Do not ask the
   user questions during the run: take the most reasonable reading, write it down, continue. Commit and push after
   each phase.

## Phase 1: survey (read only; no new simulation runs)

Find out, from what already exists, where the bias voltages should sit, and what the existing evidence covers:
- Where `vref` / `vcm` (S2D) and `vref` (D2S; and whatever else depends on its input common mode) should sit, and
  with what tolerance, according to the existing simulation and characterization runs. Starting points:
  `macros/sg13cmos5l_IOPadSingle2Diff/README.md` (input window: unit gates <= about iovdd - 1.3 V; vref and vcm default
  1.2 V; with vref = 0.5 V the pad range is 0 ... 1 V), `macros/sg13cmos5l_IOPadDiff2Single/README.md` (suite at
  vref = vicm = 1.65 V; headroom limits at iovdd = 3.0 V; the proposal vcm = 1.2 V for both buffers), every CACE yaml
  and result under `macros/*/verification/cace/` that involves the pads or their drivers, the testbench decks and
  results under `macros/*/testbenches/` and `macros/*/verification/`, and the design notes they cite on `sudel_buecher`
  (`sudelbuecher/design_considerations/`, read through the worktree).
- What these runs cover, as a table per run (file, date / commit, schematic or extracted, what is swept: vref / vcm
  values, iovdd, corners, temperature, load, mismatch MC; which quantities: range, linearity / INL, gain, loop
  stability, settling, current, power-down), and which results are stale (taken before a later design change that
  the READMEs mention, e.g. capacitor sizes, enable complement, output-stage move).
- Which device's operating window sets each optimum (the candidate replica), and what the runs say about how that
  window moves with process, temperature and iovdd.
- The gaps: target values or ranges that no run covers, conditions missing (corners, temperatures, iovdd 3.0 / 3.6 V,
  extracted views), stale results that matter, and contradictions between sources (e.g. 1.2 V versus 1.65 V).

Write it into `docs/replica_bias/SURVEY.md` on `claude/c4-replica-bias` (with the run table and the gap list), commit and push.

**Then STOP and ask the user.** Present the proposed targets with their evidence, the gap list and, for each gap, the
simulation or characterization run you would do to close it (what, which bench, rough run time). Run nothing new
until the user has answered; take the user's answer as the scope of the next steps. (This overrides hard rule 5 for
this one point: here you do ask.)

## Phase 2: design and simulate (after the user's answer to Phase 1)

For each needed voltage (at most three blocks; share one where targets coincide):
- Schematic (xschem `.sch`/`.sym`) with power-down (`en_3v3` / `en_3v3_b`, as in `oa_core_pd`): disabled, no current,
  output pulled to a defined level that keeps the pad's own power-down state (check what the pads expect).
- Testbenches: DC over corners / temperature / iovdd (target band met?), supply current (compare with a divider giving
  the same output at the same output impedance), output impedance and settling into the pad's gate load, start-up,
  enable / disable; mismatch MC on `-s schematic`. Prefer a CACE yaml per macro like the existing ones.
- Closed-loop check: pad + its replica bias together (the pad's CACE suite with the ideal vref / vcm source replaced),
  range and linearity no worse than with the ideal source at the chosen value.

## Phase 3: layout (as far as time allows; say where you stopped)

KLayout (or magic) layout per block from the existing device layouts, DRC (`make klayout-drc`, `make magic-drc`) and
LVS (`make magic-lvs`, `make klayout-lvs`) clean, `make build-top`-style views. If layout is not reached, deliver
schematic + simulation and a floorplan sketch (where each block sits: in the pad cell or in the slot).

## Records

- On `claude/c4-replica-bias`: each macro's `README.md` (purpose, ports, results tables, limitations) in the style of
  `macros/oa_core_pd/README.md`; `docs/replica_bias/RUNLOG.md` (one entry per step: UTC time, exact command with full
  paths, cwd, exit status, log file, what changed; tool versions once); `docs/replica_bias/SUMMARY.md` (at most one
  page: targets, blocks, current saved versus a divider, status, what migrates to the delivery repo later).
- On `claude/c4-replica-bias-sudel`: design notes and derivations in `sudelbuecher/design_considerations/replica_bias/`, tee'd logs of
  long runs in `sudelbuecher/logs/replica-bias/`.
- Chat log: `sudelbuecher/chatlog/<date>_claude_replica_bias.md` on `claude/c4-replica-bias-sudel`, the visible conversation verbatim,
  exported from this session's own transcript (`~/.claude/projects/*/<session-id>.jsonl`): user messages, your visible
  messages, one bracketed line per tool call; never reasoning, system text, reminders or tool output; no secrets. If
  the export is refused, record that and continue; do not work around it. Add a one-line entry to
  `sudelbuecher/chatlog/README.md`. Use `claude` in place of a model name in file names and pushed files.

Final chat message to the user (after the last phase, not after the survey): five lines or fewer: targets, blocks,
current versus a divider, status, branch names.
