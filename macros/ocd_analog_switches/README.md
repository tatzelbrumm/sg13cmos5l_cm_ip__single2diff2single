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
  (2026-11-07: done for `analog_pswitch_small` except `avdd` off, ESD and layout; see the next section.)
- The sheets need the `sg13cmos5l_stdcells` symbols (`sg13cmos5l_inv_4`, `_antennanp`, `_decap_4`) from the PDK's xschem library path,
  as in the harness; the netlist needs the standard-cell spice.
- `make` targets: `Makefile.new` is a copy of `hv_logic`'s (no CACE groups, no layout); `mv Makefile.new Makefile` as in `macros/README.md`.
- The large `analog_switch` (m=100) of the harness dependency is not copied.

## Characterization of `analog_pswitch_small` (CACE, 2026-11-07)

Question: is the harness PMOS switch fit as the per-leg switch of a bias-current distribution (1 ... 50 uA sourced into a
6u/6u hv NMOS diode at about 0.6 ... 1.5 V)? Schematic netlist only (no PEX, no layout), CACE 2.11.0, ngspice-47, IHP models of
the installed `ihp-sg13cmos5l`. 1225 runs, all of them through `make sim-cace`. **Limits: "F" = functional (the gate at the rail it
must be at, recovery after dvdd returns); "P" = proposal = worst simulated case + margin, set after the first run, not a
requirement; "-" = characterized only.** All F and P limits pass; the weak spots are in the "-" rows.

| group (runs) | swept | measured (min ... max over the sweep) | limit | verdict |
|---|---|---|---|---|
| `func_params` (135) | enable 0-1-0-1, dvdd 1.08/1.2/1.32 x avdd 3.0/3.3/3.6, 5 corners, -40/27/125 C, 2.5 V into 10k \|\| 1p | polarity right everywhere (gate within 0.5 uV of avss on, = avdd off); enable -> gate 0.46 ... 36.6 ns (tt nominal 0.93 / 1.15 ns); load 50 %: 1.1 ... 37.3 ns; V_load/2.5 V 0.949 ... 0.977; held 1 pF at turn-off: +27.8 ... +33.9 fC | F 0.1 V; P 50 / 40 / 50 / 50 ns, >= 0.9 | pass |
| `func_mm_params` (200) | mismatch MC at the slowest point (sf, -40 C, dvdd 1.08, avdd 3.6) | always toggles; enable -> gate on 17 ... 223 ns (median 37, 99 % 139), off 9 ... 109 ns | F; P 500 ns | pass |
| `func1v_params` (15) | the same with 1.0 V into 10k \|\| 1p, nominal supplies | V_load/1 V <= 0.13 % (ff 125 C), 1e-9 at ss -40 C: **does not pass 1 V** | - | - |
| `ron_params` (450) | out = 0.3 ... 3.0 V, in = out - 10 mV, avdd 3.0/3.3/3.6, 5 x 3 | R_sw: >= 2.0 V: 176 ... 803 ohm; 1.5 V: 0.97 ... 5.2 k; 1.3 V: 2.1 k ... 4.6 M; 1.2 V: 3.8 k ... 0.67 G; <= 0.9 V: >= 1.3 M (ff 125 C), 10 G at tt 27 C (open). tt 27 C 3.3 V: 262 / 541 / 1730 / 8.9 k / 107 k ohm at 3.0 / 2.0 / 1.5 / 1.3 / 1.2 V. I_dvdd <= 85 nA, I_avdd <= 1.2 nA, I_en <= 1.3 nA (tt 27 C: 1.0 nA, 1.3 pA, 0.18 nA) | F gate; P 120 nA / 2 nA / 2 nA | pass |
| `leak_params` (90) | off, in/out each 0 / 1.7 / 3.6 V, avdd 3.6, dvdd 1.32, 5 corners, 27/125 C | \|I_in\|, \|I_out\| <= 3.3 nA (ff 125 C, 3.6 V across), <= 0.1 nA at 27 C; with out <= 1.7 V, in = 0: <= 0.53 nA (n-well junction). I_dvdd <= 95 nA, I_avdd <= 2.0 nA, I_en >= -0.55 nA (tt 27 C: 1.7 nA, 17 pA, -0.10 nA) | F gate; P +-5 nA, 130 nA, 3 nA, -0.8 nA | pass |
| `bias_params` (135) | iDAC stand-in (1:1 hv PMOS mirror on avdd) -> switch -> 6u/6u diode, 1 / 5 / 50 uA, avdd 3.0/3.3/3.6, 5 x 3; one off neighbour on the iDAC node | diode 0.58 ... 0.80 / 0.82 ... 0.99 / 1.45 ... 1.79 V; drop 0.40 ... 0.65 / 0.23 ... 0.51 / 0.035 ... 0.13 V; iDAC node <= 1.84 V, headroom avdd - node >= 1.17 V; error (in - out)/out <= +0.025 % (1 uA, ff 125 C), <= 0.005 % at 5 uA; one off neighbour injects <= 176 pA, x 18 (harness: 19 switches per iDAC node) -> <= +0.34 % at 1 uA, 0.063 % at 5 uA, 0.004 % at 50 uA | F gate; P drop <= 0.8 V, headroom >= 1.0 V, +-0.05 %, +-250 pA, +-0.5 % | pass |
| `pwr_params` (90) | dvdd lost (1 us ramp) while on / while off, avdd up with dvdd = 0; 100 ms, then dvdd back; avdd 3.0/3.6, 5 x 3 | lost while on: stays on 100 ms everywhere. Lost while off: stays off for 100 ms at -40/27 C (gate >= 0.88 avdd), at 125 C turns on within 1 ... 10 ms (sf) or 10 ... 100 ms (ss), drifts to 0.73 ... 0.94 avdd (tt, ff), stays off (fs); a drifting level shifter draws up to **0.20 mA from avdd** (> 1 uA in 13 of these 30 runs and in 4 of the 30 power-up runs). avdd up without dvdd: **comes up on** at -40 and 27 C in all corners, at 125 C on (ss, sf) or drifting. After dvdd returns: correct state in all 90 | F 0.1 V (recovery) | pass |
| `pwr_mm_params` (50) | avdd up with dvdd = 0, mismatch MC, tt 27 C | all 50 come up on: systematic, not mismatch | F | pass |
| `dvdd_off_params` (60) | DC, dvdd = 0, latch preset on / off, R at 2.0 V | preset on: on (371 ... 803 ohm) in 30/30; preset off: the solver lands on "on" in 18/30, mid-rail latch nodes draw up to 0.23 mA from avdd (the DC end point, reached only slowly at <= 27 C, see `pwr_params`) | - | - |

**Fit as a bias-leg switch for 1 ... 50 uA into ~0.9 V: yes, with conditions** (measured above, reasoning here). The leg works
because the current is forced: the PMOS (gate at avss) conducts once its source (the iDAC side) is about one |Vth| above ground, so
the iDAC node rises to 1.0 ... 1.84 V and the switch drops 0.035 ... 0.65 V; the current reaches the diode to better than 0.03 %
(0.34 % with 18 off neighbours at 1 uA, 125 C). Conditions: (1) the source must be a sourcing current source with compliance to
about 1.9 V at avdd = 3.0 V (the harness iDAC and a PMOS mirror are; with avdd >= 3.0 V there is >= 1.17 V left for it);
(2) the switched node must not be a voltage that has to pass: below ~1.3 V (tt) / 1.5 V (worst) the cell is not a voltage switch
(R >= 2 k at 1.3 V, open at <= 0.9 V; 1 V does not reach a 10 k load), so a leg that must pull a node near ground, or an
NMOS-sink leg at a low node, does not work; (3) dvdd must be up whenever avdd is: without dvdd the state is undefined (comes up
on, an off switch can turn on at 125 C, and up to 0.2 mA crowbar from avdd per cell). In the harness, dvdd = `vdd1v2` (core
supply, not a slot's gated supply), so there this matters only for power sequencing; a copy inside a slot with dvdd = the slot's
gated `vdd_1v2` while `vdd_3v3` stays on hits all three effects. (4) The level shifter (1.2 V-driven 2u/0.5u hv NMOS against a
0.5u/0.5u hv PMOS latch) has little margin at sf, -40 C, dvdd 1.08 V, avdd 3.6 V: 37 ns at the corner, up to 223 ns with
mismatch; no failure in 200 MC runs, failure rate not quantified beyond that. For static bias selection the delay is irrelevant.
Not checked: layout parasitics / PEX, avdd = 0 with dvdd up, ESD, noise, settling of the bias node after switching.

Simulation notes. xschem netlists the sheet's standard cells as empty subcircuits; the templates include the PDK's
`sg13cmos5l_stdcell.spice` first, and ngspice keeps the first definition ("redefinition of .subckt ..., ignored" in the logs). The
PDK antenna diode `dantenna` (model `darea`, tt = 701 ns) stalls ngspice-47 transients at >= 85 C; the two transient templates
define `sg13cmos5l_antennanp` with tt = 0 (forward bias only; identical results at tt 27 C). The CACE DUT netlist is checked equal
to `netlist/source/ocd_analog_switches.spice`. The `Error: undriven node` lines in the log come from xschem's netlist check (the
sources are in code blocks) and are harmless. Transient delays are within ~3 % of a 0.02 ns max-step run.

Rerun (about 13 min on 4 cores; `gen_cace.py` writes the yaml and the templates, edit it rather than them):

```sh
export PDK_ROOT=/foss/pdks; source .designinit
python3 -I macros/ocd_analog_switches/verification/gen_cace.py
make -C macros/ocd_analog_switches sim-cace TOP=analog_pswitch_small CACE_JOBS=4 \
  CACE_GROUPS="ron_params leak_params dvdd_off_params bias_params func_params func1v_params func_mm_params pwr_params pwr_mm_params"
make -C macros/ocd_analog_switches spec-table TOP=analog_pswitch_small
```

Results: `verification/cace/results/analog_pswitch_small/` (`<group>.csv` in SI units, except the `%` errors and the ratios;
`summary_<group>.md`; plots).
