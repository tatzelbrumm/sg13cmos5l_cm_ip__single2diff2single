<!--
SPDX-FileCopyrightText: 2026 Christoph Maier
SPDX-License-Identifier: Apache-2.0
-->
# Design notes: slot 7 as a stand-alone test platform (stage A), 2026-11-06

Cloud session, Claude, after `docs/launch/slot7_testplatform_TASK.md` (`harness-test`). The design is on
`claude/c5-slot7-testplatform` (`macros/slot7_testplatform/`, `docs/slot7_testplatform/`); this folder keeps what does
not belong in the macro: the reasons, the rejected first version, intermediate results.

## Decisions and why

1. **Cores, not the full references.** `oa_core_pd` / `bg_core_pd` have checked layouts (DRC 0, LVS match); `bias_oa_pd`
   / `bias_bg_pd` have none. The core output current is itself the observable. The trees are stage B.
2. **One bus line per core** (OA -> `analog_bus0`, BG -> `analog_bus1`): both can be measured at once, and a fault on one
   line does not take both. `analog_bus2` / `analog_bus3` are left for stage B (bias-voltage mux, harness `ibias`).
3. **No `en_ctrl_3v3`, a simpler fail-safe cell.** In the pad cell `en_ctrl_3v3` has to detect both slot supplies from
   the pad ring. In the slot the 3.3 V logic runs on the gated `vdd_3v3` itself, and `dig_in` / `enable` are driven by
   harness logic on the always-on 1.2 V rail (latches in `user_project_control.v`, reset while the slot is not
   selected). So a ratioed stage (weak hv PMOS against an hv NMOS stack gated by `dig_in[k]`, `enable` and the slot's
   `vdd_1v2`) is a level shifter, an AND and a supply detector at once, without a latch, and the 3.3 V side needs no
   1.2 V supply. Sized by a prototype sweep: PU 0.3/20 against 3 x 2/0.45 gives <= 18 mV at 1.08 V gate drive.
4. **`xgate` instead of `analog_switch_small`** (first version, see below). Bare hv TG 2/0.5 of the harness biasgen,
   layout already in `macros/ocd_analog_switches` (DRC 0). Its gates come from two more channels of the enable cell.
5. **Read-back** `dig_out[3:0]` = the four 3.3 V enables, through hv inverters on the slot's 1.2 V rail: the enable
   path and the fail-safe can be checked over SPI (reg 0x38) without an SMU. `dig_out[11:4]`: hv NMOS pull-downs
   (gate `vdd_1v2`), so the harness mux inputs are defined, without tying a port to a supply (SPICE / LVS cannot join
   two ports, and a magic extraction would merge them).
6. **NRD** (hv NMOS 0.3/20, gate `vdd_3v3`) pulls a gated-off, floating `vdd_1v2` low (2.2 .. 7.3 uA from `vdd_1v2` when
   on). With 1 uA injected into the floating rail (off-leakage of the harness power gate) the fail-safe still holds.
7. **Layout from scripts**: rows of IHP PCells by `pbc_row.row()` (from `pad_buffer_cells.py`), a small channel router
   (each row: gate channel above, drain channel below; terminals drop on M2 into their own channel, so M2 verticals in
   a channel come from one side only and cannot overlap; M3 tracks; M4 columns for multi-channel and external nets).
   DRC and LVS clean on the first run of each version.
8. **Top level**: Metal3 horizontal, Metal4 vertical; the cores use only M1 / M2, so M3 / M4 cross them. Supplies:
   TopMetal1 bands from the four left-edge stubs (each band within its stub's y range at the edge), TopVia1 directly on
   the enable cell's M4 supply columns, M1 -> TM1 via stacks on 2 um M1 fingers from the core rails (not plates: a
   plate makes the rail "wide" metal and pulls the 0.6 um spacing rule M1.f into the cores). Every sub-cell gets the
   prefix `slot7_` (the harness reads all slots into one magic session); the PCell text `sub!` is removed (a name
   ending in `!` is global in magic).
9. **Pads**: the base of `slot_7.gds` is the current delivery `slot_7.gds` itself, so the 13 pins and stubs are the
   same shapes. The platform ends at x = 142.55 um; the right strip x >= 520 holds only pad shapes.

## The rejected first version (analog_switch_small)

`results_v1_analog_switch_small/static.csv`: with `analog_switch_small` as bus switches, enabled by `dig_in[2]` /
`dig_in[3]` directly, the state "vdd_1v2 gated off, dig_in = 1111, enable = 1" turned both cores ON at ff / fs, 125 C,
high supply (7.06 / 6.31 uA on the bus). The `sg13cmos5l_antennanp` cell inside the switch has a p+ / n-well diode from
`enable` to `dvdd`: the harness drives `dig_in` from its always-on rail, so it charges the slot's floating `vdd_1v2`
through that diode (0.37 V at 27 C, 0.62 V at 125 C), enough for the sense NMOS at 125 C. Found with ngspice
`show all` in the smoke test (0.37 V), confirmed by the PVT run. The fix removes the path (no 1.2 V circuit is driven
from `dig_in` except hv NMOS gates) instead of making the detector stiffer (the diode current rises exponentially
with the voltage, so a stronger pull-down buys little).

## Simulation notes

- `gmin` 1e-15 let ngspice settle on non-physical operating points at a few -40 C points (0.03 .. 1 uA through an open
  switch); `gmin` 1e-12 gives ~2 pA there. All final runs use 1e-12, so currents below ~10 pA are the simulation floor.
- A 10 ns enable edge stopped the transient (timestep too small in the bandgap's pnpMPA); 100 ns edges run.
- The harness side (analog_switch_med, pad, other slots' open switches) is not modelled; on chip, measure I_leak with
  the core off and subtract (PLAN.md section 5).

## Open points

- `vdd_3v3` gated off with a voltage on the bus: the TG PMOS (p+ / n-well) feeds the floating `vdd_3v3` (tens of nA,
  rail at ~0.6 V). Procedure: bus switches open and SMU at 0 V before gating `vdd_3v3` off. A PMOS-less switch (NMOS
  only, gate 3.3 V, bus <= ~2 V) would avoid it; not done.
- Sheets are drafts (one labelled stub per terminal), checked by netlisting; tidy by hand if wanted.
- No PEX of the slot (the cores' PEX is in their macros); the extracted (device-only) netlist was simulated at tt / 27 C.
- Stage B (trees, voltage mux, harness ibias as third reference) not started.

## Stage B (2026-11-06, evening)

Decisions:
1. **The S2D pad's tree** (`bias_tree_noab_pd`, four lines, no class-AB legs) rather than `bias_tree_pd`: it is the
   chain the pad actually uses, so measuring it on silicon characterizes the pad's bias, and it is smaller.
2. **One tree, three selectable references** (OA, BG, harness `ibias0`) by transmission gates into `iref`, rather than
   one tree per reference: the comparison is then made through one and the same mirror, so the tree's own mismatch
   cancels in the comparison. The cores keep their stage-A bus switches, so a core can be measured directly or into
   the tree (not both at once: the current would split).
3. **Bias voltages onto `analog_bus2`** through four xgates (a voltmeter on `analog[2]`); the tree's outputs are diode
   nodes (low impedance), so nA of switch / bus leakage moves them by < 1 mV.
4. **`ibias1` straight onto `analog_bus3`**: measures the harness current through slot 7's own path (pin, xgate, bus,
   harness bus switch) for comparison with the diagnostic path of project 0.
5. **New cells only** (`tp_en_ctrl_b`, the tree layout, a new top `slot7_testplatform_ab`): stage A's cells, sheets and
   pins stay as delivered, and the user's hand edits of the stage-A sheets are not touched.
6. **No read-back for stage B**: all 12 `dig_out` are stage A's.

Simulation note: the first harness-source model clamped the `ibias` pins 0.6 V above the 3.3 V rail; that fed current
through switches that were off (xgate PMOS junction). The harness source is a PMOS source on the same rail; the model now
clamps below the rail and leaves the pin floating where the harness switch would be open.

Layout: `routed_cell.py` = the tp_en_ctrl router generalized; one fix (tie Metal1 extension must overlap the ptap's own
Metal1). `slot_7.gds` with stage B was DRC clean on the first build and LVS clean on the first run.
