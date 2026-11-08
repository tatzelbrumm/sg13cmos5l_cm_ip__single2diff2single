<!--
SPDX-FileCopyrightText: 2026 Christoph Maier
SPDX-License-Identifier: Apache-2.0
-->
# Brief for the slot-7 hand-over session (2026-11-08, slot_7 v2)

From cloud session C4 (design repo `tatzelbrumm/sg13cmos5l_cm_ip__single2diff2single`, branch `claude/c4-replica-bias`)
to the session that maintains `tatzelbrumm/sg13cmos5l_cm_slot7`. Take only what is listed; nothing else from the design
repo goes into the hand-over repo. Christoph decides when; open checks are listed at the end.

## What changes in slot 7

The fallback's stage A (OA / BG cores, bus diagnostics, `tp_en_ctrl`) is replaced by the slot circuit for the custom
pads (`macros/slot_7/README.md`): harness `enable` and `dig_in[0..5]` → `s7_ctrl` (fail-safe shifters without a 1.2 V
supply, mode decode, switch matrix) → bandgap core → `bias_dist_pd` → `pad_ref_rb` and the two pads' `iref`; loop S2D →
D2S direct or swapped, S2D outputs to `analog_bus0/1` or the D2S fed from them, vcm / vref on `analog_bus2/3` (monitor,
or fed with pad_ref_rb disconnected); `dig_out[11:0]` held low as the fallback did. The pad cells are unchanged (already
in `pads/`); the 13 custom-pad nets replace `s7_an[0:1]` / `s7_an_0_esd`, pin shapes and labels identical to the
fallback's stubs.

## Files to take (source → destination)

| source (design repo, branch claude/c4-replica-bias) | destination (slot7 repo) |
|---|---|
| `macros/slot_7/layout/klayout/slot_7.klay.gds` (top cell `slot_7`, 537.15 × 273 µm, sha256 5f8fd14a722ec458…) | `final/gds/slot_7.gds` |
| `macros/slot_7/layout/klayout/slot_7.cdl` (sha256 af1e5f027f9f90c1…; self-contained: slot_7 and all 11 subcircuits) | `netlist/slot_7.cdl` (LVS reference) |
| `macros/slot_7/netlist/source/slot_7.spice` | `netlist/slot_7.spice` (source of the slot circuit) |
| `macros/slot_7/README.md` (mode table, default, register settings) | `docs/slot_7.md`, linked from `README.md` |
| `macros/slot_7/layout/klayout/slot_7.png` | `docs/` (picture for the README) |
| LEF / Liberty / Verilog stub of `slot_7` | `final/{lef,lib,vh}/`, regenerated the way stage A's were (new ports: dig_in[0..5] used, the 13 pad nets) |

## Checks to repeat in the hand-over repo (results in the design repo)

1. DRC of `final/gds/slot_7.gds`: `run_drc.py --no_density` → no violations, 0 "exception" lines; maximal deck with
   `-rd latchUpRules=true` → 0.
2. LVS against `netlist/slot_7.cdl` with `run_lvs.py --run_mode=deep --disable_tap_extraction` → match, 0 port
   mismatches, 497 devices. This is the strict run: pins that share one net (e.g. analog_bus2 = s7_an_0_vcm =
   s7_an_1_vref) are one CDL port named with KLayout's comma list. Flat mode reports 32 port mismatches (the blocks' own
   labels join the net names) and matches only with `--ignore_top_ports_mismatch`.
3. The harness flow with the custom pads (C6: `docs/custom_io/TIM_STEPS.md` on `sg13cmos5l_ocd_chipalooza` branch
   `claude/c6-submodule-pads`, or upstream's `setup_custom.sh`): netcheck of the 13 pad nets. Tim may run it on his side
   in parallel.

## README content for Tim (short)

- Supplies used: `vdd_3v3` / `vss_3v3`; `vdd_1v2` only for the dig_out pull-downs.
- `enable` = 1 turns the slot on in the default mode (bandgap → replica bias → pads, loop direct, vcm / vref on
  analog_bus2/3). `dig_in[0..5]` select modes only with the key `dig_in[3] = 1`, `dig_in[4] = 0`; route the dig_in
  registers to 0 (0x0D) first. Modes: dig_in[0] swap, [1] S2D outputs → bus0/1, [2] bus0/1 → D2S (loop off), [5] external
  vcm / vref on bus2/3.
- Close the harness's bus switches (reg 0x51 bits 4..7) for the buses in use; bus0/1 slow the S2D → D2S loop while
  closed (stable, 10-30× slower).
- Disable: `enable` = 0; with the slot's supplies off, the pads draw leakage only (≤ 67 nA at 125 °C).

## Open (Christoph decides whether they block the hand-over)

- S2D enable kick with the new vcm / vref switches between pad_ref_rb's bypass capacitors and the pads (being checked;
  fix if needed: MOS capacitors on the pads' side in the empty slot area).
- Mode simulations at ss / −40 °C: tt and ff pass all 8 modes; at ss −40 the default (DC), feed and ext (transient from
  power-up) pass; swap and mon stall at the bandgap's start-up node in the solver (rerun with a slower enable edge).
