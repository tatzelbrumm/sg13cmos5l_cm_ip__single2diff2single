<!--
SPDX-FileCopyrightText: 2026 Christoph Maier
SPDX-License-Identifier: Apache-2.0
-->
# Brief: slot 7 v2 through the harness flow in Christoph's ocd_chipalooza fork (2026-11-08)

For the session that wrote C6's `docs/custom_io/TIM_STEPS.md` (fork `tatzelbrumm/sg13cmos5l_ocd_chipalooza`, branch
`claude/c6-submodule-pads`), or whichever session Christoph picks.

## What is new

`tatzelbrumm/sg13cmos5l_cm_slot7` `main` (= branch `claude/slot7-pads-v2`, commit 454da6a2) now holds slot 7 v2: the
slot circuit for the two custom pads (`final/gds/slot_7.gds`, sha256 5f8fd14a722ec458…; `docs/FOR_TIM.md`,
`docs/slot_7.md`). The 13 custom-pad stubs have the same shapes and labels as the stand-in slot of your dry run; the
slot now uses `enable`, `dig_in[0..5]`, `analog_bus0..3`, `vdd_3v3` / `vss_3v3`, and `vdd_1v2` / `vss_1v2` / `dig_out[11:0]`
(pull-downs). Design source: `tatzelbrumm/sg13cmos5l_cm_ip__single2diff2single`, branch `claude/c4-replica-bias`,
`macros/slot_7/`.

## Do (on a new branch of the fork, e.g. `claude/slot7-v2-harness-test`; never on main)

1. Point the slot-7 submodule / `config.txt` `s7_version` at slot7 `main` 454da6a2 (the dry run used the stand-in).
2. Rerun the flow of TIM_STEPS.md for slot 7 (projects, setup, custom-io, wrappers, gds-slots, projects-gds,
   gds-prefill), and note any step that behaves differently from the dry run.
3. Checks, as far as the cloud machine allows (say which you could not run and why):
   - netcheck of the 13 custom-pad nets;
   - DRC of the assembled slot 7 area with the antenna rules and with density (our own DRC ran `--no_density`);
   - top-level LVS (`make lvs-top`) if feasible; otherwise LVS of the slot-7 wrapper;
   - whether upstream's `scripts/setup_custom.sh` (RTimothyEdwards main) handles the slot7 repo layout without
     the hand edits of TIM_STEPS (so Tim's own flow works).
4. Update `docs/custom_io/TIM_STEPS.md` if steps changed (e.g. no more merge of `claude/c6-pads-layout`: slot7 `main`
   is now the source).

## Report

Branch and commit, each step's result (exit code, warnings that matter), the check results with numbers, what was
not run. Stop and ask Christoph before working around a failure in the slot itself; harness-side fixes go only on
your fork branch.
