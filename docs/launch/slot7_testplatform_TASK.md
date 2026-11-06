# TASK FILE for a cloud agent: slot 7 as a stand-alone test platform for the bias references

Read this whole file before doing anything. Written 2026-11-06 on the user's request. It lives on branch `harness-test`
of `tatzelbrumm/sg13cmos5l_cm_ip__single2diff2single` (the design repository). A second task runs in parallel
(`docs/launch/replica_bias_TASK.md`); the branch and directory rules below keep the two apart.

## Goal

A real `slot_7.gds` that is useful on silicon even if the custom pads never make it into the harness (time, or Tim's
patience): the two bias references, the Oguey–Aebischer and the Banba bandgap (`bias_oa_pd` / `bias_bg_pd`, or at
least their cores `oa_core_pd` / `bg_core_pd`; decide and write down which), wired so that they can be enabled,
selected and measured through the harness resources a slot always has: the **shared analog bus** `analog_bus0..3`, the
**digital inputs** (`enable`, `dig_in[23:0]`, `clk`, `reset`; `dig_out[11:0]` for read-back if useful), the harness
bias `ibias0`, `ibias1`, `vbias`, and the gated supplies `vdd_3v3`, `vdd_1v2` with `vss_3v3`, `vss_1v2`. The dedicated
pads (`s7_an[0]`, `s7_an[1]`) are NOT used by this platform. It must stay easy to add the custom pads later.

Two stages; finish A before starting B:
- **A (must):** both cores, each with its own enable; their output currents (`iout`, about 5 uA, sourced) routed to the
  analog bus through transmission gates, so that an external SMU on the chip pin `analog[k]` measures each current;
  the 1.2 V control bits from `dig_in` / `enable` level-shifted to the 3.3 V domain (fail-safe like `en_ctrl_3v3`).
- **B (if time):** the bias trees behind the cores and a multiplexer of their bias voltages onto the bus; the harness
  `ibias0` / `ibias1` as a third reference for comparison.

## Hard rules

Create these branches yourself from the named starting points, push them, and work and push only on them. If a
branch of that name already exists on the remote, stop and tell the user.
1. Design repository: **`claude/c5-slot7-testplatform`** from `origin/toplevel` for the design, and
   **`claude/c5-slot7-testplatform-sudel`** from `origin/sudel_buecher` (an orphan branch) for notes, logs and the chat
   log, checked out in a separate worktree (`git worktree add -b claude/c5-slot7-testplatform-sudel ../sg13cmos5l_cm_ip__single2diff2single_sudelbuecher origin/sudel_buecher`;
   never switch the main checkout to it: an orphan branch empties the working tree).
2. Delivery repository `tatzelbrumm/sg13cmos5l_cm_slot7`: **`claude/c5-testplatform`** from `origin/main`, with the new
   `final/gds/slot_7.gds` and its views. Never push to `main`: the user decides the merge.
3. Harness fork `tatzelbrumm/sg13cmos5l_ocd_chipalooza`: only for verification, on **`claude/c5-testplatform-test`**
   from `origin/custom-pad-test`. Nothing in `RTimothyEdwards/*`.
Never push to any other branch (`main`, `toplevel`, `sudel_buecher`, `harness-test`, `custom-pad-test`, ...).
4. Environment: `export PDK_ROOT=/foss/pdks; source .designinit` in the design repo before any `make`; in the harness,
   `export PDK_ROOT=/foss/pdks PDK=ihp-sg13cmos5l` and, for magic 8.3.685, the PATH shim
   `docs/custom_pads/tools/shim/magic` of the harness fork for batch magic runs. Avoid `make all` in the design repo.
5. No spreadsheets, no Microsoft formats. Every command, assumption and number goes into the run log. Do not ask the
   user questions during the run: take the most reasonable reading, write it down, continue. Commit and push after
   each phase.

## Facts to start from (verify each)

- Slot frame: `macros/slot/layout/klayout/slot.klay.gds` (537.15 x 273 um; harness pins on the left edge, supplies on
  Metal5/TopMetal stripes; ungated supply areas become obstruction in the harness wrapper: do not route over them).
  Current delivery `slot_7.gds`: `tatzelbrumm/sg13cmos5l_cm_slot7` `main`, `final/gds/slot_7.gds` (13 custom-pad pins on
  the right edge at x 535.05..536.45 um, see `macros/slot/harness_test/slot7_pins.md` on `harness-test`).
- **Pad compatibility (the "easily extensible" requirement):** keep the right edge strip x >= 520 um free of anything
  but pin stubs. Keep the 13 custom-pad pins of the current delivery `slot_7.gds` (as labelled stubs, unconnected or
  tied as there) so the GDS fits the custom-pad wrapper; write down the exact swap for the fallback with foundry
  `sg13cmos5l_IOPadAnalog` pads (config.txt `s7_an[0]`, `s7_an[1]` as IOPadAnalog; pins `s7_an[0]`, `s7_an[1]`,
  `s7_an_0_esd` on the right edge as in `slot.klay.gds`) and check that it would not collide with the platform.
- Harness side of the bus and controls: read `verilog/rtl/chipalooza_frame.v` and `verilog/rtl/slot7_wrapper.v` of the
  harness fork (how `analog_bus0..3` reach the chip pins `analog[0..3]` and through which switches; what drives
  `enable`, `dig_in`, the gated supplies; voltage levels). State the measurement path for each observable.
- Existing layouts you may reuse: `macros/oa_core_pd/layout`, `macros/bg_core_pd/layout` (DRC/LVS clean per their
  READMEs), the harness dependency `sg13cmos5l_ocd_ip__analog_switches` (Apache-2.0: transmission gates with level
  shifter, `analog_switch_small`, `sw_lvl_shift`; magic views (`.mag`) in its `magic/` directory: write their GDS with
  magic and record the source commit), the IHP standard cells for 1.2 V logic.
  Schematics without layout (`en_ctrl_3v3`, `ls_up_1v2_3v3`, bias trees) need layout or a substitute; say which.

## Phases

1. **Plan:** pin map (which `dig_in` bit does what, which bus line carries what), measurement procedure per observable,
   power-up / enable sequence, floorplan sketch. Write it into `docs/slot7_testplatform/PLAN.md` on `claude/c5-slot7-testplatform`.
2. **Schematic + simulation:** xschem top cell (new macro, e.g. `macros/slot7_testplatform/`, pins = the slot pins it
   uses) with testbenches: enable / disable of each core, current into a voltage-held bus (SMU model) over corners and
   -40 / 27 / 125 C, bus leakage of disabled switches, behaviour with the gated supplies off (no current, no
   back-feeding into the bus). CACE yaml where it fits the macro style.
3. **Layout:** `slot_7` top cell on the slot frame, the cores and switches placed and routed (KLayout python or magic),
   PDK KLayout DRC clean (`libs.tech/klayout/tech/drc/ihp-sg13cmos5l.drc`, feol+beol), magic + netgen LVS against the
   schematic, views (`final/gds/slot_7.gds`, lef, lib, vh) as in the delivery repo. If layout is not finished, deliver
   stage A schematic + simulation and say exactly where layout stopped; do not push a broken `slot_7.gds`.
4. **Deliver and verify:** branch `claude/c5-testplatform` of the delivery repo with the new views; harness fork branch
   `claude/c5-testplatform-test`: `s7_version` = `claude/c5-testplatform <commit>`, `make projects-clean SLOTS=7`, `make projects SLOTS=7`,
   `make projects-gds SLOTS=7`, `make gds-prefill`; then a net-by-net extraction check of the pre-fill top for the slot
   7 nets you use (adapt `docs/custom_pads/tools/netcheck_slot7.py` of the harness fork to the left-edge nets).

## Records

- On `claude/c5-slot7-testplatform`: `docs/slot7_testplatform/RUNLOG.md` (one entry per step: UTC time, exact command with full
  paths, cwd, exit status, log file, what changed; tool versions once), `PLAN.md`, `SUMMARY.md` (at most one page:
  what is on the slot, how to measure it, check results, stage reached, the fallback swap, what Tim needs to know).
- On `claude/c5-slot7-testplatform-sudel`: design notes in `sudelbuecher/design_considerations/slot7_testplatform/`, tee'd logs of long runs
  in `sudelbuecher/logs/slot7-testplatform/`.
- Chat log: `sudelbuecher/chatlog/<date>_claude_slot7_testplatform.md` on `claude/c5-slot7-testplatform-sudel`, the visible conversation
  verbatim, exported from this session's own transcript (`~/.claude/projects/*/<session-id>.jsonl`): user messages,
  your visible messages, one bracketed line per tool call; never reasoning, system text, reminders or tool output; no
  secrets. If the export is refused, record that and continue; do not work around it. Add a one-line entry to
  `sudelbuecher/chatlog/README.md`. Use `claude` in place of a model name in file names and pushed files.

Messages to the user: when the user is talking with you interactively (questions, answers, the stop after a phase),
keep them short, one point at a time. The final report and everything written to files are for reconstruction after
the fact: complete and verbatim, no length limit.

Final report to the user (after the last phase): stage reached, check results, branch names, open points.
