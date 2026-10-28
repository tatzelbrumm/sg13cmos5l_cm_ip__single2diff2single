<!--
SPDX-FileCopyrightText: 2026 Christoph Maier
SPDX-License-Identifier: Apache-2.0
-->
# `bias_out_pd`: bias of the class-AB pad driver, with power-down

`bias_out_pd` is the bias of `d2s_mpdda_pd` from an **external reference current out of `iref`** (into an external NMOS sink). Mirror image of `bias_in_pd`: input diode PI (a copy of BP). Not usable with the harness `ibias` pins, which source current. Its tree without the inverter is
`bias_tree_out_pd` (2026-10-28), pin-compatible with `bias_tree_pd`.

It is one of the four bias variants of `d2s_mpdda_pd` (in, out, oa, bg). All four keep `d2s_bias_lp`'s six bias
diodes and so the bias voltages the driver sees: vbp 5 uA (BP, unit tails), vbn 5 uA (BN, fold sinks), vbpc 2 uA (BPC,
mirror cascodes), vbnc 2 uA (BNC, fold cascodes), vabp 5 uA (RP2 on RP1, class-AB P side), vabn 5 uA (RN2 on RN1, class-AB N side).
Since 2026-10-27 the class-AB stacks RP1 + RP2 / RN1 + RN2 are in the pad, in `d2s_mpdda_pd` (RP1 / RN1 are the
replicas of OP / ON inside its clamp frames, nets `dabp` / `dabn`, formerly `n1` / `n2`); this cell sinks the vabp
current and sources the vabn current and has no vddo / vsso. Its CACE templates attach the two stacks as fixtures on
vddo / vsso: the same devices on the same nets, so the circuit characterized, and the results below, are unchanged.
Everything else is on vdd / vss.
Design, sizing and every pre-CACE number: `~/EDA/sg13cmos5l_cm_ip__single2diff2single_sudelbuecher/sudelbuecher/design_considerations/class_ab_pad_driver/improvements/bias.md` (numbers from `improvements/sim/run_bias.py`,
`improvements/sim/results_bias.txt`); power-down: `~/EDA/sg13cmos5l_cm_ip__single2diff2single_sudelbuecher/sudelbuecher/design_considerations/class_ab_pad_driver/power_down/log.md`, `power_down/xschem/README.md`,
`power_down/sim/results_power_down.txt` (indexed here, not copied).

Source netlist: `../bias_tree_pd/netlist/source/bias_ref_pd.spice`, subckt `bias_out_pd`.

## Ports (symbol and subckt order)

`vdd vss iref vbp vbn vbpc vbnc vabp vabn en_3v3`

en_3v3: 0 / vdd, active high. The cell makes its own en_3v3_b (inverter IP / IN, 1u / 0.45u).

## Enabled and disabled

Enabled (en_3v3 = vdd), every switch is off (the transmission gate on) and the cell is its `improvements/` version
`d2s_bias_out`. Disabled (en_3v3 = 0), the root of every current is switched off:

- TGN / TGP: transmission gate between iref and pi (PI's gate line), open when disabled.
- TDP (gate en_3v3): pulls pi to vdd, so PI and the tree are off.

The other bias lines carry leakage only and get no switch. All switches are 1u / 0.45u hv devices.

## Schematic

`schematic/xschem/bias_out_pd.sch` / `.sym`. The sheet is a copy of `power_down/xschem/d2s_bias_out_pd.sch` as hand-edited on 2026-10-08 18:30. In that version TGN's iref-side terminal (-50,-560) was not connected (`net1`), so only the PMOS half of the transmission gate passed iref. Repaired in this copy with one wire, `N -60 -560 -50 -560 {lab=iref}`. The original in `power_down/xschem/` is unchanged.

Checked here: xschem's netlist of the sheet against the subckt `bias_out_pd` of `bias_ref_pd.spice`, device by device
(model, w / l / ng, terminal nets with the internal nets matched by name), and the port order: no difference,
no single-use internal net, no missing symbol.

## CACE (`verification/cace/`)

`bias_out_pd.yaml`, templates `templates/bias_out_pd_tb_{dc,psrr,startup,pd}.sch`. Each template is the cell's symbol with net labels on
its pins, one drawn source (Ven, the enable) and a code block with the other sources and the measurement.
The external reference is a 5 uA NMOS mirror sinking out of iref; `Iref` is the current at the iref pin through a 0 V sense source.

- The six bias currents are the drain currents of the six diodes inside the cell, `@n.x1.<diode>.nsg13_hv_[np]mos[ids]`
  (the quantity `run_bias.py` reports). Line sensitivity: dI / I per volt, vdd = vddo moved by +-0.1 V around the condition.
- PSRR (AC current needs a sense source): replicas of the six diodes in the testbench, gate on the bias line, drain held
  at the line voltage by an E source through a 0 V source. Their small-signal current equals the diode's. Reported per rail
  (vdd, vss, vddo, vsso): the largest |dI / I| of the six currents per volt of ripple, at 1 kHz, 100 kHz and 1 MHz.
- Start-up: every supply ramps from 0 V (uic, Gear) in 1 or 100 us, en_3v3 follows vdd. t_su90 = last crossing of 90 % of
  the final bn current, counted from the start of the ramp (so it includes the ramp). Rbn_end / Rabp_end = current 1 ms
  after the ramp relative to the dc operating point.
- Power-down: operating point with en_3v3 = 0 (supply current per rail, current at iref, largest diode current), then en_3v3
  rises at 10 us in 10 ns: t_en90 = from the edge until the bn / abp current stays within +-10 % of its settled value
  (the definition of the power-down log's start-up t90).
  vext follows vdd in this testbench: a reference supply above vdd forward-biases the open TG (0.3 uA at 125 C with vext = 3.3 V, vdd = 3.0 V).
- Mismatch: 30 iterations (seed 12345 + iteration), mos_tt_mismatch / res_typ_mismatch, schematic netlist only.
- Tolerances: dc and operating points gmin = abstol = 1e-15; transients 1e-12 (1e-15 makes the floating disabled nodes ~27x slower).

| group | conditions | runs |
|---|---|---:|
| dc_params | corner_mos ss/sf/tt/fs/ff x temp -40/27/125 x vdd 3.0/3.3/3.6 | 45 |
| mm_params | 30 mismatch iterations, tt 27 C 3.3 V | 30 |
| psrr_params | corner_mos ss/tt/ff x temp -40/27/125, 3.3 V | 9 |
| startup_params | corner_mos ss/tt/ff x temp -40/125 x vdd 3.0/3.6 x ramp 1/100 us | 24 |
| pd_params | corner_mos ss/sf/tt/fs/ff x temp -40/27/125 x vdd 3.0/3.6 | 30 |

Run (IIC-OSIC-TOOLS, after `source .designinit` in the repo root):

```sh
make sim-cace                               # every group: results/bias_out_pd/summary_<group>.md, <group>.csv, *.png (the PNGs are not committed: rerun to get them)
make sim-cace CACE_GROUPS=pd_params         # one group
make spec-table                             # limit and worst case per quantity (see the note on % units below)
```

The Makefile is `macros/inverter/Makefile` with TOP = bias_out_pd and the sim-cace / spec-table targets of the level-shifter
pair. It was delivered as `Makefile.new` (the file tool refuses files named Makefile): rename it to `Makefile`.

## Results (pre-layout, schematic netlist, 2026-10-20)

Simulated in the cloud with the pinned tools of `sudelbuecher/cloud_environment.md` (xschem 3.4.8RC `ddc7344`,
ngspice-47, OpenVAF `5ed9e63`, IHP-Open-PDK iic-jku `c271a7e9`) and CACE 2.13.0. Display units; `%/V` = percent per volt.
**The limits are proposals**: worst case of these runs plus about 30 % (two-sided currents: 30 % on the deviation from
nominal, 40 % for mismatch). Replace them by requirements.

| group | quantity | unit | limit (proposal) | min | max | runs | verdict |
|---|---|---|---|---:|---:|---:|---|
| dc_params | Bias current bp | uA | >= 4.93 <= 5.22 | 5.066 | 5.17 | 45 | pass |
| dc_params | Bias current bn | uA | >= 4.93 <= 5.12 | 5.036 | 5.09 | 45 | pass |
| dc_params | Bias current bnc | uA | >= 1.97 <= 2.14 | 2.048 | 2.104 | 45 | pass |
| dc_params | Bias current bpc | uA | >= 1.93 <= 2.03 | 1.945 | 1.981 | 45 | pass |
| dc_params | Bias current abp | uA | >= 4.93 <= 5.19 | 5.038 | 5.147 | 45 | pass |
| dc_params | Bias current abn | uA | >= 4.93 <= 5.11 | 5.029 | 5.086 | 45 | pass |
| dc_params | Supply current vdd | uA | <= 32 | 24.16 | 24.51 | 45 | pass |
| dc_params | Supply current vddo | uA | <= 6.7 | 5.038 | 5.147 | 45 | pass |
| dc_params | Reference current at the iref pin | uA | any | 5.029 | 5.078 | 45 | pass |
| dc_params | Line sensitivity bp | %/V | <= 2.7 | 1.357 | 2.042 | 45 | pass |
| dc_params | Line sensitivity bn | %/V | <= 1.5 | 0.7402 | 1.103 | 45 | pass |
| dc_params | Line sensitivity bnc | %/V | <= 1.5 | 0.758 | 1.124 | 45 | pass |
| dc_params | Line sensitivity bpc | %/V | <= 2.9 | 1.4 | 2.159 | 45 | pass |
| dc_params | Line sensitivity abp | %/V | <= 3.4 | 1.369 | 2.558 | 45 | pass |
| dc_params | Line sensitivity abn | %/V | <= 1.7 | 0.7844 | 1.237 | 45 | pass |
| mm_params | Bias current bp - mismatch | uA | >= 4.93 <= 5.28 | 5.014 | 5.198 | 30 | pass |
| mm_params | Bias current bn - mismatch | uA | >= 4.93 <= 5.15 | 5.02 | 5.104 | 30 | pass |
| mm_params | Bias current bnc - mismatch | uA | >= 1.97 <= 2.14 | 2.054 | 2.097 | 30 | pass |
| mm_params | Bias current bpc - mismatch | uA | >= 1.87 <= 2.04 | 1.908 | 2.028 | 30 | pass |
| mm_params | Bias current abp - mismatch | uA | >= 4.93 <= 5.25 | 5.048 | 5.18 | 30 | pass |
| mm_params | Bias current abn - mismatch | uA | >= 4.93 <= 5.15 | 5.002 | 5.106 | 30 | pass |
| mm_params | Supply current vdd - mismatch | uA | any | 24.16 | 24.52 | 30 | pass |
| mm_params | Supply current vddo - mismatch | uA | any | 5.048 | 5.18 | 30 | pass |
| mm_params | Reference current at the iref pin - mismatch | uA | any | 5.051 | 5.052 | 30 | pass |
| mm_params | Line sensitivity bp - mismatch | %/V | any | 1.635 | 1.657 | 30 | pass |
| mm_params | Line sensitivity bn - mismatch | %/V | any | 0.8904 | 0.8967 | 30 | pass |
| mm_params | Line sensitivity bnc - mismatch | %/V | any | 0.908 | 0.9136 | 30 | pass |
| mm_params | Line sensitivity bpc - mismatch | %/V | any | 1.711 | 1.742 | 30 | pass |
| mm_params | Line sensitivity abp - mismatch | %/V | any | 1.774 | 1.794 | 30 | pass |
| mm_params | Line sensitivity abn - mismatch | %/V | any | 0.9569 | 0.9636 | 30 | pass |
| psrr_params | Supply sensitivity vdd, 1kHz | %/V | <= 1.4 | 0.7947 | 1.065 | 9 | pass |
| psrr_params | Supply sensitivity vdd, 100kHz | %/V | <= 1.5 | 0.8207 | 1.085 | 9 | pass |
| psrr_params | Supply sensitivity vdd, 1MHz | %/V | <= 3.0 | 2.149 | 2.302 | 9 | pass |
| psrr_params | Supply sensitivity vss, 1kHz | %/V | <= 1.7 | 0.8344 | 1.276 | 9 | pass |
| psrr_params | Supply sensitivity vss, 100kHz | %/V | <= 1.7 | 0.8565 | 1.292 | 9 | pass |
| psrr_params | Supply sensitivity vss, 1MHz | %/V | <= 3.1 | 2.078 | 2.352 | 9 | pass |
| psrr_params | Supply sensitivity vddo, 1kHz | %/V | <= 2.1 | 0.9195 | 1.557 | 9 | pass |
| psrr_params | Supply sensitivity vddo, 100kHz | %/V | <= 2.1 | 0.9623 | 1.579 | 9 | pass |
| psrr_params | Supply sensitivity vddo, 1MHz | %/V | <= 4.1 | 2.95 | 3.087 | 9 | pass |
| psrr_params | Supply sensitivity vsso, 1kHz | %/V | <= 0.35 | 0.2068 | 0.2646 | 9 | pass |
| psrr_params | Supply sensitivity vsso, 100kHz | %/V | <= 0.41 | 0.2713 | 0.3089 | 9 | pass |
| psrr_params | Supply sensitivity vsso, 1MHz | %/V | <= 2.3 | 1.614 | 1.765 | 9 | pass |
| startup_params | Start-up time to 90 % bn current | us | <= 71 | 0.4212 | 54.23 | 24 | pass |
| startup_params | bn current after start-up / dc |  | >= 0.95 <= 1.05 | 1 | 1 | 24 | pass |
| startup_params | abp current after start-up / dc |  | >= 0.95 <= 1.05 | 1 | 1 | 24 | pass |
| pd_params | Supply current vdd, disabled | nA | <= 1.5 | 2.93e-05 | 1.147 | 30 | pass |
| pd_params | Supply current vddo, disabled | nA | <= 0.22 | 5.575e-06 | 0.168 | 30 | pass |
| pd_params | Current at the iref pin, disabled | nA | <= 0.49 | 3.051e-06 | 0.3736 | 30 | pass |
| pd_params | Largest bias current, disabled | nA | <= 0.22 | 6.155e-06 | 0.1685 | 30 | pass |
| pd_params | Enable time, bn current | us | <= 0.2 | 0.1225 | 0.1496 | 30 | pass |
| pd_params | Enable time, abp current | us | <= 0.2 | 0.1241 | 0.1516 | 30 | pass |

Mismatch, sigma / mean (mean deviation from nominal), N = 30: bp 1.05 % (+2.01 %)  bn 0.45 % (+1.24 %)  bnc 0.49 % (+3.77 %)  bpc 1.41 % (-1.75 %)  abp 0.69 % (+2.14 %)  abn 0.49 % (+1.03 %)

### Cross-check against the pre-CACE results

Bias currents, % deviation from nominal (5 / 5 / 2 / 2 / 5 / 5 uA); results_bias.txt (`d2s_bias_ref.spice` without enable, ideal iref) vs this CACE run (`_pd` sheet, 5 uA mirror as iref):

| corner | source | bp | bn | bnc | bpc | abp | abn |
|---|---|---:|---:|---:|---:|---:|---:|
| tt 27C | results_bias.txt | 1.24 | 0.19 | 2.73 | -2.78 | 0.87 | 0.08 |
| tt 27C | CACE | 2.27 | 1.22 | 3.78 | -1.78 | 1.90 | 1.11 |
| ss 3.0V -40C | results_bias.txt | 0.84 | 0.12 | 3.36 | -3.40 | 0.06 | -0.05 |
| ss 3.0V -40C | CACE | 1.54 | 0.82 | 4.08 | -2.73 | 0.76 | 0.65 |
| ff 3.6V 125C | results_bias.txt | 1.53 | 0.26 | 2.00 | -2.15 | 1.44 | 0.19 |
| ff 3.6V 125C | CACE | 2.78 | 1.51 | 3.27 | -0.94 | 2.69 | 1.44 |

The CACE reference is the 5 uA mirror, which delivers 5.0515 uA at the iref pin (tt 27 C 3.3 V): that accounts for the common offset of +1.03 % against the ideal 5 uA of results_bias.txt.

Line sensitivity at tt 27 C, %/V (results_bias.txt: secant 3.0 ... 3.6 V; CACE: +-0.1 V around 3.3 V): bp +0.90 / +1.65, bn +0.13 / +0.89, bnc +0.15 / +0.91, bpc +0.98 / +1.73, abp +1.03 / +1.78, abn +0.20 / +0.96.

Supply rejection at tt 27 C, largest |dI / I| of the six currents, %/V, results_bias.txt / CACE:

| rail | 1 kHz | 100 kHz | 1 MHz |
|---|---:|---:|---:|
| vdd | 0.97 / 0.97 | 0.98 / 0.99 | 1.63 / 2.23 |
| vss | 1.02 / 1.02 | 1.03 / 1.04 | 1.85 / 2.19 |
| vddo | 1.22 / 1.22 | 1.24 / 1.25 | 2.24 / 2.97 |
| vsso | 0.24 / 0.24 | 0.26 / 0.29 | 1.08 / 1.66 |

Mismatch sigma / mean, %, results_bias.txt (N = 100) / CACE (N = 30): bp 1.08 / 1.05, bn 0.41 / 0.45, bnc 0.54 / 0.49, bpc 1.43 / 1.41, abp 1.02 / 0.69, abn 0.38 / 0.49.

Disabled, ff 125 C 3.6 V: bias-cell current from vdd 1.192 nA in results_power_down.txt (section 2, "bias") / 1.147 nA here.
Enable, tt 27 C 3.6 V: bn current within +-10 % 0.13 us after the edge (the power-down log reports the driver I_Q: 0.5 - 0.9 us for in, out, bg).

`make spec-table` (`scripts/cace/spec_table.py`) does not scale `%` units: for the `%/V` rows it prints the raw fraction per
volt (0.0078 for 0.78 %/V). The table above was made with the correct scaling.
