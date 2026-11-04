<!--
SPDX-FileCopyrightText: 2026 Christoph Maier
SPDX-License-Identifier: Apache-2.0
-->
# ocd_ls_dn_3v3_1v2: 3.3 V -> 1.2 V level shifter (INVERTING), from the Chipalooza harness

Added 2026-11-03. Same ports, order and polarity as `ls_dn_3v3_1v2` (`vss vddl out in`).

**The harness has no dedicated 3.3 V -> 1.2 V shifter.** Searched: the names of all `.subckt` lines in the harness's
`netlist/schematic/*.spice`, `netlist/layout/*.spice` and the dependencies' `netlist/*/*.spice`. The level-related cells are the
up-shifters `sw_lvl_shift` and `level_shift`, the hv inverter `hv_inv_1` (biasgen), and the IO-library cells `sg13cmos5l_LevelUp`,
`_LevelUpInv`, `_GateLevelUpInv`, `_LevelDown`. In `voltgen_v3` the frame uses `hv_inv_1` on that cell's `vdd` port
(`x3 vdd v0 v0b vss hv_inv_1`). Powering `hv_inv_1` from the 1.2 V rail makes a down-shifter: this macro. `sg13cmos5l_LevelDown`
(`core pad iovdd iovss vdd vss`) takes a pad plus `iovdd`/`iovss` and is not an internal cell.

| | |
|---|---|
| ports (order) | `vss vddl out in` |
| devices | 2 hv MOS: PMOS 2.0u/0.4u, NMOS 1.0u/0.45u = `hv_inv_1` with `vdd` -> `vddl` |
| source | `hv_inv_1` of `dependencies/sg13cmos5l_ocd_ip__biasgen` (submodule commit `0dbfff6c06732c5a0d9802bbdfa274ff7bc6fcfc`); `reference/hv_inv_1.harness.spice` |

**Difference from `ls_dn_3v3_1v2`:** PMOS 1u/0.45u -> 2.0u/0.4u, NMOS 0.8u/0.45u -> 1.0u/0.45u. Its README's cautions apply unchanged: the
output is inverted, the switching threshold is low (duty-cycle distortion), and the hv gates see the full 3.3 V input swing.
For a non-inverting result follow it with a 1.2 V inverter. No CACE result exists for this macro.

## Files

```
netlist/source/ocd_ls_dn_3v3_1v2.spice          source subcircuit
schematic/xschem/ocd_ls_dn_3v3_1v2.sch/.sym     sheet and symbol (copies of ls_dn_3v3_1v2 with the sizes changed)
testbenches/xschem/tb_ocd_ls_dn.sch              interactive testbench (copy of tb_ls_dn)
verification/cace/ocd_ls_dn_3v3_1v2.yaml         CACE suite, derived, not run; templates/ holds the transient testbench
reference/hv_inv_1.harness.spice                harness netlist of hv_inv_1
```

## Checked / not done

- Checked 2026-11-03 with `scripts/check_ocd_macros.py`: devices equal to `hv_inv_1` (names ignored, ports mapped), port order, sheet
  vs source (own text reader, not xschem; see `ocd_ls_up_1v2_3v3`).
- Drafted, **not run**: `verification/cace/ocd_ls_dn_3v3_1v2.yaml`, derived by script from `ls_dn_3v3_1v2.yaml` (same pins, conditions, variables
  and groups `pvt_params`, `tr_params`, `cload_params`; the testbench handles the inversion as in the source). Only the output-level limits are kept
  (Voh >= 1 V, Vol <= 0.05 V); every other limit is `any`. Interactive testbench: `testbenches/xschem/tb_ocd_ls_dn.sch`.
  Run (after `mv Makefile.new Makefile`): `make sim-cace`, `make spec-table`.
- Not done: xschem netlisting, any simulation, layout, behaviour with `vddl` or the 3.3 V domain off.
- `Makefile.new` = copy of `hv_logic`'s with the `CACE_GROUPS` of `ls_dn_3v3_1v2`.
