<!--
SPDX-FileCopyrightText: 2026 Christoph Maier
SPDX-License-Identifier: Apache-2.0
-->
# ocd_analog_switches: the harness's transmission gates, for internal analog and analog-bus gating in slot 7

Added 2026-11-03. The sheets and symbols in `schematic/xschem/` are **byte-identical copies** of the harness originals
(`scripts/check_ocd_macros.py` compares sha256), so a harness LVS and this repository see the same cells under the same names.
Licence of the originals: Apache-2.0, Tim Edwards / Open Circuit Design (`reference/LICENSE.*`).

Sources (read from the local checkout `~/EDA/sg13cmos5l_ocd_chipalooza`):

| copied from | submodule commit | cells |
|---|---|---|
| `dependencies/sg13cmos5l_ocd_ip__analog_switches/xschem` | `d210467cf74b58de74cd48b3f676cd10194e8d33` | `analog_switch_small`, `analog_switch_med`, `analog_pswitch_small`, `sw_lvl_shift`, `gate_drive_med` |
| `dependencies/sg13cmos5l_ocd_ip__biasgen/xschem` | `0dbfff6c06732c5a0d9802bbdfa274ff7bc6fcfc` | `xgate` |

(The commits are the `HEAD` files of the submodules' git directories; read, not obtained from a git command.)

## Cells (ports in the harness order)

| cell | ports | what it is |
|---|---|---|
| `analog_switch_small` | `dvdd dvss avdd in avss enable out` | full transmission gate, NMOS 5u/0.45u m=4 + PMOS 5u/0.4u m=4 (hv), enable level-shifted inside |
| `analog_switch_med` | `dvdd dvss avdd in avss enable out` | same, 10u m=40 per device (hv), gate driver `gate_drive_med` |
| `analog_pswitch_small` | `dvdd dvss avdd in avss enable out` | PMOS-only switch 5u/0.4u m=4: conducts well only for in/out near `avdd` |
| `xgate` | `ena_b vdd in out vss ena` | bare hv transmission gate 2u/0.5u, no level shifter: `ena_b` (PMOS gate) and `ena` (NMOS gate) must be complementary and swing `vss..vdd` |
| `sw_lvl_shift`, `gate_drive_med` | see `netlist/source/` | sub-cells of the above, also used by `ocd_ls_up_1v2_3v3` |

For the three `analog_*switch*` cells: `enable` is **active high**, referenced to `dvdd`/`dvss` (1.2 V, from the two input
inverters `sg13cmos5l_inv_4` on `dvdd`); the signal path is switched with gates at `avdd`/`avss` (3.3 V). Bulks: NMOS to `avss`,
PMOS to `avdd`. So a `dig_in[k]` bit of the slot (1.2 V) can drive `enable` directly.

## Supply and signal mapping, as the harness uses it (from `netlist/schematic/chipalooza_frame.spice`)

```
x60    vdd1v2 vss1v2 vdd3v3 vbias7   vss3v3 net94     voltgen_vout analog_switch_small   (dvdd dvss avdd in avss enable out)
x26[k] vdd1v2 vss1v2 vdd3v3 ana7[k]  vss3v3 net92[k]  analog[k]     analog_switch_med     k = 3..0
```

so for slot 7: `dvdd = vdd_1v2`, `dvss = vss_1v2`, `avdd = vdd_3v3`, `avss = vss_3v3`. The frame puts one `analog_switch_small` between
`vbias7` and the shared `voltgen_vout` and four `analog_switch_med` between `ana7[3:0]` and the shared `analog[3:0]`.
`ana7[3:0]` is the net list order of the slot-7 instance; `slot7_wrapper` calls the same four ports `analog_bus3..analog_bus0`
(same order in `slot7_wrapper_lvs.v` and in the instance line of the frame netlist; matched by position, not by name).
These harness switches are therefore on the **harness side** of the slot pins. A switch from this macro placed inside the slot
isolates the slot's own nodes from the pins (extra series resistance and capacitance on the shared buses; not quantified).
`analog_pswitch_small` is defined in the frame netlist; I did not trace where, or whether, it is instantiated.

## Proposed use in slot 7 (a proposal, not wired into `slot.sch`)

| purpose | cell | enable |
|---|---|---|
| gate a slot node onto `analog_bus0..3` (high impedance, small current) | `analog_switch_small` | one `dig_in[k]` each (`dig_in[23:4]` are unused in the fallback `slot.sch`) |
| gate between blocks of the single2diff2single chain | `analog_switch_small`, or `_med` if the series resistance matters | `dig_in[k]` |
| switch controlled from a 3.3 V domain signal (e.g. a signal that is already `ocd_ls_up_1v2_3v3` output) | `xgate` with `ena` = signal, `ena_b` = its complement on `vdd_3v3` (e.g. `inv_hv` from `hv_logic`) | 3.3 V |

Which `dig_in` bits go where is a decision for you; nothing in this macro fixes it.

## Files

```
layout/klayout/*.klay.gds                  KLayout versions of the harness's Magic layouts (see Layout)
netlist/source/ocd_analog_switches.spice   the six harness subcircuits, text unchanged (extracted by script)
schematic/xschem/*.sch/.sym                harness sheets and symbols, byte-identical
reference/                                 harness licences; harness schematic netlists of the three switches
```

## Layout (added 2026-11-03): KLayout versions of the harness's Magic layouts

`layout/klayout/<cell>.klay.gds` for `analog_switch_small`, `analog_switch_med`, `analog_pswitch_small`, `sw_lvl_shift`, `gate_drive_med`, `xgate`
(the large `analog_switch` and the power stages are not imported). Written by `scripts/mag2klay.py`, from the harness's `.mag` files:

- **Magic** 8.3.678 (conda-forge), `gds write`, with the IHP `ihp-sg13cmos5l` technology files of IHP-GmbH/IHP-Open-PDK commit `0488153`
  (`.tech` c7d8b4b7, `-cifout` 828159a8, `-cifin` f3c452ee, `-drc` c2209171, `-extract` 58e141c6, `.tcl` 08d3940a, `.magicrc` 55c49b71; sha256 prefixes).
  Search paths as in the harness's own `run_extract_*.sh`.
- **Standard cells** (`sg13cmos5l_inv_4`, `_antennanp`, `_decap_4`): the harness `.mag` files are vendor-cell stubs and Magic wrote its own
  stub geometry (e.g. 80 shapes in `inv_4` against 70 in the PDK). The script replaces them with the cells of the PDK's `sg13cmos5l_stdcell.gds` (same commit).
- **KLayout** (python module 0.30.12) writes the file. The top cell name equals the file name. The files are static: no PCells and no library
  references, so there is no `.klay.klib`. The parametrized devices of the Magic layouts stay in as sub-cells (`sg13_hv_nmos_*`, `via_*`).

| file | bytes | sha256 (first 12) |
|---|---:|---|
| `analog_switch_small.klay.gds` | 132790 | 789d1d4cbc43 |
| `analog_switch_med.klay.gds` | 1096138 | 6e5dcdabf128 |
| `analog_pswitch_small.klay.gds` | 92370 | fd9108e7b6a3 |
| `sw_lvl_shift.klay.gds` | 38972 | dba02d3e3ec1 |
| `gate_drive_med.klay.gds` | 339256 | 227f1295bb9a |
| `xgate.klay.gds` | 12000 | 793096c07e73 |

Checked 2026-11-03 (cloud container, Magic + KLayout python; not the KLayout DRC/LVS decks):
1. Devices **extracted by Magic from the `.mag`** and **extracted from the final `.klay.gds` read back into Magic** are equal, subcircuit by subcircuit
   (model, w, l, m), for all six cells (e.g. `analog_switch_med`: 11 subcircuits, 176 devices).
2. Magic's extraction of `analog_switch_med.mag` is **byte-identical** to the harness's own `netlist/layout/analog_switch_med.spice`. For `analog_switch_small` and
   `analog_pswitch_small` it differs only in the position of the `sg13cmos5l_decap_4` subcircuit and of one instance line (reason not investigated).
3. The standard cells in the files equal the PDK's, layer by layer; everything else equals Magic's own output.
4. Top cell = file name; cell lists as in the Magic output.

**Known deviation, not resolved:** Magic warns `CIF error in cell sw_lvl_shift, layer THKOX: parent and child disagree on CIF` (also for the cells that contain it).
Magic's hierarchical `gds write` (used here) and Magic's own flattened output differ on THKOX (GDS 44/0) by 0.05 um2 (`sw_lvl_shift`), 88 um2 (`analog_switch_small`),
45 um2 (`analog_pswitch_small`) and 222 um2 (`gate_drive_med`); `analog_switch_med` and `xgate` show no difference. The other XOR differences between the two
outputs are the pin/text layers and the per-cell boundary (189/4), as expected. Which of the two THKOX results is right was not decided; watch the thick-oxide
rules in the KLayout DRC.

Not done: KLayout DRC and LVS of these layouts (need the IHP decks and the cloud tools): after `mv Makefile.new Makefile`, `make klayout-verify CELL=analog_switch_small`
(`klayout-verify-all` loops over the six cells; the LVS reads the copied sheets in `schematic/xschem`). Magic DRC/LVS/PEX likewise (`magic-verify`).
Regenerate: `python3 -I scripts/mag2klay.py --harness <harness checkout> --out macros/ocd_analog_switches/layout/klayout` (needs Magic, `pip install klayout`, the PDK).

## Checked / not done

- Checked 2026-11-03 with `scripts/check_ocd_macros.py`: copies identical to the harness originals; source netlist equal to the
  harness netlists for all six subcircuits.
- Not done: any simulation (no ngspice/xschem was available in the session), CACE suite, PVT of the switch resistance, leakage with
  `avdd` off, ESD on nodes connected to pads, KLayout DRC/LVS of the imported layouts (see Layout).
- The sheets need the `sg13cmos5l_stdcells` symbols (`sg13cmos5l_inv_4`, `_antennanp`, `_decap_4`) from the PDK's xschem library path,
  as in the harness; the netlist needs the standard-cell spice.
- `make` targets: `Makefile.new` is a copy of `hv_logic`'s (no CACE groups, no layout); `mv Makefile.new Makefile` as in `macros/README.md`.
- The large `analog_switch` (m=100) of the harness dependency is not copied.
