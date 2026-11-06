<!--
SPDX-FileCopyrightText: 2026 Christoph Maier
SPDX-License-Identifier: Apache-2.0
-->
# SUMMARY: slot 7 test platform for the bias references (2026-11-06)

**Stage reached: A complete (schematic, simulation, layout, DRC, LVS, delivery, harness flow). Stage B not started.**

**On the slot** (`macros/slot7_testplatform`, delivered as `slot_7.gds` on `sg13cmos5l_cm_slot7` branch `claude/c5-testplatform` f2c8501):
the Oguey–Aebischer core `oa_core_pd` and the Banba bandgap core `bg_core_pd` (cores, not the full references: they
have checked layouts); each output current (~5 uA, sourced) goes through a bare hv transmission gate (`xgate`) onto
`analog_bus0` (OA) / `analog_bus1` (BG). New cell `tp_en_ctrl` (43 hv devices): four fail-safe enables
`en = dig_in[k] AND enable AND (slot vdd_1v2 present)` (ratioed: weak hv PMOS against an hv NMOS stack, no latch, no
1.2 V supply needed), read-back on `dig_out[3:0]`, `dig_out[11:4]` held low. Pins: `dig_in[0]` OA, `dig_in[1]` BG,
`dig_in[2]` OA -> bus0, `dig_in[3]` BG -> bus1. Unused: `dig_in[23:4]`, `clk`, `reset`, `ibias0/1`, `vbias`,
`analog_bus2/3`, the custom-pad pins (`s7_an[*]`). The platform occupies x < 143 um, y < 197 um of the 537 x 273 um slot.

**How to measure** (PLAN.md section 5): SPI `0x50 = 7`; `0x20..0x37 = 0x0D` (**the reset route 0x0 follows pad io[0]**);
`0x51 = 0x06`, then `0x0E`, then `0x0F`. OA: `0x22 = 0x0E`, `0x51 = 0x1F`, SMU on `analog[0]` at 0.7 V, read I_leak; `0x20 = 0x0E`,
read I_on; I_OA = I_on - I_leak; reg 0x38 bits 2, 0 = 1. BG: the same with `0x23`, `0x21`, `0x51` bit 5, `analog[1]`,
bits 3, 1. Fail-safe: `0x51` bit 2 (1.2 V) or bit 0 (`enable`) to 0 -> back to I_leak. Before gating `vdd_3v3` off: bus
switches open, SMU at 0 V.

**Simulation** (schematic, 5 corners x -40 / 27 / 125 C x supplies 3.0/1.08, 3.3/1.2, 3.6/1.32 V; `results/summary.md`):

| | OA core | BG core |
|---|---|---|
| I_out at 0.7 V, all corners and temperatures | 3.04 .. 7.05 uA (tt: 3.26 / 4.99 / 6.66 at -40 / 27 / 125 C) | 3.83 .. 6.37 uA (tt: 4.87 / 4.96 / 4.88) |
| supply dependence 3.0 -> 3.6 V (max over corners) | 0.11 % | 0.37 % |
| compliance: change over bus 0 .. 2.0 V / at 2.5 V | < 0.002 % / -0.08 % | 0.014 % / -0.03 % |
| enable to 1 % / disable | 0.38 .. 0.69 us / 71 .. 100 ns | 0.43 .. 0.93 us / 68 .. 102 ns |

Off states (all 495 points correct, incl. `vdd_1v2` gated off with 1 uA injected into it): bus current <= 0.17 nA
(switch open), <= 2.2 nA (switch closed, core off; ff / 125 C). Open-switch leakage, bus 0 .. 3.3 V: <= 0.16 nA.
`vdd_3v3` gated off with 0.7 V on the bus: up to 87 nA flow into the slot (TG PMOS to n-well), `vdd_3v3` floats at
0.5 .. 0.67 V. Supplies: `vdd_3v3` 19 .. 30 uA (both on), <= 7 nA (off); `vdd_1v2` 2.2 .. 7.3 uA (pull-down NRD).
The extracted layout netlist gives the same currents to 4 digits (tt / ff, 27 / 125 C).

**Checks:** `tp_en_ctrl`: PDK KLayout DRC 0, magic + netgen LVS match (43 devices). `slot_7.gds`: KLayout DRC
(feol + beol) 0, also for the foundry-pad variant; LVS "netlists match uniquely" (104 devices, 72 nets), known port
errors only (stand-in `outp`/`vinp`, `outn`/`vinn` joins of the pad stubs; frame `vss_1v2` strip). Sheets: xschem netlist
= source netlist. Harness (`claude/c5-testplatform-test` 9981b94): `projects-clean / projects / projects-gds /
gds-prefill` exit 0; slot_7 in the pre-fill GDS = delivered GDS (XOR empty); net check of the pre-fill top: all 36 used
and 27 unused pins OK.

**Design change on the way:** with the harness `analog_switch_small` as bus switch, its `antennanp` diode let the harness
charge a gated-off `vdd_1v2` from `dig_in`, and the cores turned on at ff / fs 125 C. Replaced by `xgate` + two more
fail-safe channels.

**Pads:** the 13 custom-pad pins and stubs are the delivery's own shapes, unchanged (the GDS fits the custom-pad wrapper).
Fallback to foundry pads: `config.txt` `s7_an[0]:  sg13cmos5l_IOPadAnalog  s7_an_0`, `s7_an[1]:  sg13cmos5l_IOPadAnalog  s7_an_1`,
regenerate the wrappers, and build `slot_7.gds` with `make_slot_7.py <harness-test slot.klay.gds> <out> --pads foundry`
(frame pins `s7_an[0]`, `s7_an[1]`, `s7_an_0_esd`; DRC 0; no collision, the platform is at x < 143 um).

**For Tim:** slot 7 uses only standard slot resources; sub-cells are prefixed `slot7_` and the PCell text `sub!` is removed;
ports, `slot_7.lib` and `slot_7.vh` are unchanged; the right-edge Metal2 strip (`vss_1v2`) is still not connected inside the slot.

**Open:** stage B (trees, bias-voltage mux on `analog_bus2`, `ibias` comparison); back-feeding with `vdd_3v3` off
(procedure, or an NMOS-only switch); draft-style sheets; no slot-level PEX; chip-level DRC / LVS not run.
