<!--
SPDX-FileCopyrightText: 2026 Christoph Maier
SPDX-License-Identifier: Apache-2.0
-->
# ocd_ls_up_1v2_3v3: 1.2 V -> 3.3 V level shifter (non-inverting), from the Chipalooza harness

Added 2026-11-03. Same ports, same order and same function as `ls_up_1v2_3v3` (`vss vddl vddh out in`), so either can be
instantiated in its place. The circuit is the one the harness uses to drive its own analog switches: the two-inverter input
stage of `analog_switch_small` (`sg13cmos5l_inv_4` on the 1.2 V rail) followed by `sw_lvl_shift`
(`sg13cmos5l_ocd_ip__analog_switches`, copy in `../ocd_analog_switches`).

| | |
|---|---|
| ports (order) | `vss vddl vddh out in` |
| devices | 2 standard-cell inverters `sg13cmos5l_inv_4` on `vddl` + `sw_lvl_shift` (8 hv MOS on `vddh`) |
| polarity | non-inverting. Read from the harness netlist, not simulated: `in_p` high pulls `net1` low, `S1_N` goes high, `outn` low, `out` high. `in_p` is `in` through two inverters, `in_n` through one |
| unused output | `outn` of `sw_lvl_shift` (complementary) is left open |
| reference | `reference/sw_lvl_shift.harness.spice` (harness cell), `reference/level_shift.frame.harness.spice` (the frame's other up-shifter `level_shift`, 3 stages, w=4u/1u m=2; not used here) |

**Difference from `ls_up_1v2_3v3`** (sizes only, from the two netlists): latch pull-downs 2u/0.5u m=1 here against 2u/0.45u m=4;
latch pull-ups 0.5u/0.5u here against 2u/0.4u; the input stage is two standard-cell inverters here against one 1.2u/0.6u
`sg13_lv` inverter. `ls_up_1v2_3v3` has a CACE result (worst case at sf, -40 C, VDDL 1.08 V "at the edge of its working range");
this macro has none, so do not assume the two behave alike at that corner.

## Files

```
netlist/source/ocd_ls_up_1v2_3v3.spice          source subcircuit
schematic/xschem/ocd_ls_up_1v2_3v3.sch/.sym     sheet (geometry of the harness sheet analog_switch_small, switch removed); symbol = the ls_up buffer symbol
testbenches/xschem/tb_ocd_ls_up.sch              interactive testbench (copy of tb_ls_up)
verification/cace/ocd_ls_up_1v2_3v3.yaml         CACE suite, derived, not run; templates/ holds the transient testbench
reference/                                       harness netlists of the shifters
```

## Checked / not done

- Checked 2026-11-03 with `scripts/check_ocd_macros.py` (own text reader, **not xschem**): the sheet reproduces the source
  subcircuit device by device, `.sym` pin order = `.subckt` ports, `x1` is `sw_lvl_shift` with the harness port order. The same
  reader reproduces the xschem-checked sheets of `ls_up_1v2_3v3` and `ls_dn_3v3_1v2` (controls).
- Drafted, **not run**: `verification/cace/ocd_ls_up_1v2_3v3.yaml`, derived by script from `ls_up_1v2_3v3.yaml` (same pins, conditions, variables
  and the three groups `pvt_params`, `tr_params`, `cload_params`). Only the output-level limits are kept (Voh >= 2.85 V, Vol <= 0.05 V); every other limit is `any`
  until a first run gives worst cases. The template testbench adds an `.include` of the standard-cell spice,
  `$PDK_ROOT/$PDK/libs.ref/sg13cmos5l_stdcell/spice/sg13cmos5l_stdcell.spice`: that path is my assumption of the PDK's file layout, unconfirmed.
  Interactive testbench: `testbenches/xschem/tb_ocd_ls_up.sch`. Run (after `mv Makefile.new Makefile`): `make sim-cace`, `make spec-table`.
- Not done: xschem netlisting of this sheet, any simulation, layout,
  behaviour with `vddl` or `vddh` off, the antenna diode (`sg13cmos5l_antennanp`) and decaps that the harness switch carries at its input.
- `Makefile.new` = copy of `hv_logic`'s with the `CACE_GROUPS` of `ls_up_1v2_3v3`.
