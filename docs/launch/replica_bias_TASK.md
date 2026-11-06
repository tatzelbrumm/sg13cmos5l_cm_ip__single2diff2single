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

1. Design repository: create branch **`replica-bias`** from `origin/toplevel` and push only that branch, plus notes to
   the orphan branch **`sudel_buecher`** through a separate worktree (`git worktree add ../sg13cmos5l_cm_ip__single2diff2single_sudelbuecher sudel_buecher`;
   never `git switch sudel_buecher` in the main checkout: it empties the working tree). On `sudel_buecher` write only
   under `sudelbuecher/design_considerations/replica_bias/` and `sudelbuecher/logs/replica-bias/`; before every push
   `git fetch` and rebase (the parallel task also pushes there, into other directories). Never push to `main`,
   `toplevel`, `harness-test` or any other branch.
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

## Phase 1: targets (evidence first)

Establish the target value and tolerance of each voltage from the pads' own data, not from guesses:
- Read `macros/sg13cmos5l_IOPadSingle2Diff/README.md` (input window: unit gates <= about iovdd - 1.3 V; vref and vcm
  default 1.2 V; with vref = 0.5 V the pad range is 0 ... 1 V) and `macros/sg13cmos5l_IOPadDiff2Single/README.md`
  (suite at vref = vicm = 1.65 V; headroom limits at iovdd = 3.0 V; the proposal vcm = 1.2 V for both buffers),
  their CACE yaml and results, and the design notes they cite on `sudel_buecher`.
- Simulate (ngspice / CACE, schematic) the range and linearity of each pad versus vref / vcm at iovdd 3.0, 3.3, 3.6 V,
  tt and the corners, -40 / 27 / 125 C, and find the optimum and the acceptable band. Write a short table.
- Decide which device's window each target follows (the replica) and state the tracking argument.
STOP and record if the data say a fixed (non-tracking) voltage is as good as a replica: then the task becomes a
low-current fixed reference built from the same primitives, and you say so.

## Phase 2: design and simulate

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

- On `replica-bias`: each macro's `README.md` (purpose, ports, results tables, limitations) in the style of
  `macros/oa_core_pd/README.md`; `docs/replica_bias/RUNLOG.md` (one entry per step: UTC time, exact command with full
  paths, cwd, exit status, log file, what changed; tool versions once); `docs/replica_bias/SUMMARY.md` (at most one
  page: targets, blocks, current saved versus a divider, status, what migrates to the delivery repo later).
- On `sudel_buecher`: design notes and derivations in `sudelbuecher/design_considerations/replica_bias/`, tee'd logs of
  long runs in `sudelbuecher/logs/replica-bias/`.
- Chat log: `sudelbuecher/chatlog/<date>_claude_replica_bias.md` on `sudel_buecher`, the visible conversation verbatim,
  exported from this session's own transcript (`~/.claude/projects/*/<session-id>.jsonl`): user messages, your visible
  messages, one bracketed line per tool call; never reasoning, system text, reminders or tool output; no secrets. If
  the export is refused, record that and continue; do not work around it. Add a one-line entry to
  `sudelbuecher/chatlog/README.md`. Use `claude` in place of a model name in file names and pushed files.

Final chat message to the user: five lines or fewer: targets, blocks, current versus a divider, status, branch names.
