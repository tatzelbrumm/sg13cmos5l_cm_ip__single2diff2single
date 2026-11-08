<!--
SPDX-FileCopyrightText: 2026 Christoph Maier
SPDX-License-Identifier: Apache-2.0
-->
# Brief for the slot-7 hand-over session (draft, 2026-11-08; finalized when slot_7.gds passes)

From cloud session C4 (design repo `tatzelbrumm/sg13cmos5l_cm_ip__single2diff2single`, branch `claude/c4-replica-bias`)
to the session that maintains `tatzelbrumm/sg13cmos5l_cm_slot7`. Take only what is listed; nothing else from the design
repo goes into the hand-over repo.

## What changes in slot 7

The fallback's stage A (OA / BG cores, bus diagnostics, `tp_en_ctrl`) is replaced by the slot circuit for the custom
pads (`macros/slot_7/README.md`): harness `enable` and `dig_in0..5` → `s7_ctrl` (fail-safe shifters, mode decode,
switch matrix) → bandgap core → `bias_dist_pd` → `pad_ref_rb` and the two pads' `iref`; loop S2D → D2S direct or
swapped, S2D outputs to `analog_bus0/1` or the D2S fed from them, vcm / vref on `analog_bus2/3` (monitor, or fed with
pad_ref_rb disconnected). The pad cells themselves are unchanged (already in `pads/`).

## Files to take (source → destination)

| source (design repo) | destination (slot7 repo) |
|---|---|
| `macros/slot_7/layout/klayout/slot_7.klay.gds` (top cell `slot_7`) | `final/gds/slot_7.gds` |
| `macros/slot_7/netlist/source/slot_7.spice` + the subcell netlists it needs (list in the final brief) | `netlist/` (for top-level LVS) |
| `macros/slot_7/README.md` (mode table, default, register settings) | `docs/slot_7.md`, linked from `README.md` |
| LEF / Liberty / Verilog stub of `slot_7` | `final/{lef,lib,vh}/`, regenerated the way stage A's were |

## Checks to repeat in the hand-over repo

1. DRC of `final/gds/slot_7.gds` (`run_drc.py --no_density`, and the maximal deck with latchUpRules), and LVS against
   the netlist (same results as in the design repo: numbers in the final brief).
2. The harness flow with the custom pads (C6's `docs/custom_io/TIM_STEPS.md` on `sg13cmos5l_ocd_chipalooza` branch
   `claude/c6-submodule-pads`, or upstream's `setup_custom.sh`): netcheck of the 13 pad nets. Tim may run it on his
   side in parallel.

## README content for Tim (short)

- Supplies used: `vdd_3v3` / `vss_3v3` only (the slot's `vdd_1v2` is not needed by the circuit).
- `enable` = 1 turns the slot on in the default mode; `dig_in0..5` select modes only with the key `dig_in3 = 1`,
  `dig_in4 = 0`; route the dig_in registers to 0 (0x0D) first.
- Close the harness's bus switches (reg 0x51 bits 4..7) for the buses in use; bus0/1 slow the S2D -> D2S loop while
  closed (stable, 10-30x slower).
- Disable: `enable` = 0; with the slot's supplies off, the pads draw leakage only (≤ 67 nA at 125 °C).
