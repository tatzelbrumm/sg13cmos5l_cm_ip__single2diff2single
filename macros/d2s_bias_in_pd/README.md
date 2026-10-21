<!--
SPDX-FileCopyrightText: 2026 Christoph Maier
SPDX-License-Identifier: Apache-2.0
-->
# `d2s_bias_in_pd`: bias of the class-AB pad driver, with power-down

`d2s_bias_in_pd` is the bias of the class-AB pad driver `d2s_mpdda_pd` from an **external reference current into `iref`** (an external PMOS source, e.g. the harness iDAC `ibias0`/`ibias1`, which *sources* current: 250 nA per step, code 20 = 5 uA). Input diode NI (a copy of BN) drives three NMOS sinks (out of BP, BPC, RP2); BP drives three PMOS sources (into BN, BNC, RN2).

It is one of the four bias variants of `d2s_mpdda_pd` (in, out, oa, bg). All four keep `d2s_bias_lp`'s six bias
diodes and so the bias voltages the driver sees: vbp 5 uA (BP, unit tails), vbn 5 uA (BN, fold sinks), vbpc 2 uA (BPC,
mirror cascodes), vbnc 2 uA (BNC, fold cascodes), vabp 5 uA (RP2 on RP1, class-AB P side), vabn 5 uA (RN2 on RN1, class-AB N side).
The class-AB replicas RP1 / RN1 sit on the output-stage rails vddo / vsso (in the pad: iovdd / iovss), everything else on vdd / vss.
Design, sizing and every pre-CACE number: `~/EDA/sg13cmos5l_cm_ip__single2diff2single_sudelbuecher/sudelbuecher/design_considerations/class_ab_pad_driver/improvements/bias.md` (numbers from `improvements/sim/run_bias.py`,
`improvements/sim/results_bias.txt`); power-down: `~/EDA/sg13cmos5l_cm_ip__single2diff2single_sudelbuecher/sudelbuecher/design_considerations/class_ab_pad_driver/power_down/log.md`, `power_down/xschem/README.md`,
`power_down/sim/results_power_down.txt` (indexed here, not copied).

Source netlist: `../sg13cmos5l_IOPadDiff2Single/netlist/source/d2s_bias_ref_pd.spice`, subckt `d2s_bias_in_pd`.

## Ports (symbol and subckt order)

`vdd vss vddo vsso iref vbp vbn vbpc vbnc vabp vabn en_3v3`

en_3v3: 0 / vdd, active high. The cell makes its own en_3v3_b (inverter IP / IN, 1u / 0.45u).

## Enabled and disabled

Enabled (en_3v3 = vdd), every switch is off (the transmission gate on) and the cell is its `improvements/` version
`d2s_bias_in`. Disabled (en_3v3 = 0), the root of every current is switched off:

- TGN / TGP (gates en_3v3 / en_3v3_b): transmission gate between the port iref and ni (NI's gate line), open when disabled.
- TDN (gate en_3v3_b): pulls ni to vss, so NI and the whole mirror tree are off. The external reference is not relied on to switch off.

The other bias lines carry leakage only and get no switch. All switches are 1u / 0.45u hv devices.

## Schematic

`schematic/xschem/d2s_bias_in_pd.sch` / `.sym`. The sheet is a copy of `power_down/xschem/d2s_bias_in_pd.sch` as hand-edited on 2026-10-09 00:44. In that version TDN's gate wire (380,-300 ... 380,-240) ended in the air, so TDN's gate floated (`net1`) instead of being on en_3v3_b. Repaired in this copy with one wire, `N 240 -300 380 -300 {lab=en_3v3_b}` (to the en_3v3_b rail at x = 240). The original in `power_down/xschem/` is unchanged.

Checked here: xschem's netlist of the sheet against the subckt `d2s_bias_in_pd` of `d2s_bias_ref_pd.spice`, device by device
(model, w / l / ng, terminal nets with the internal nets matched by name), and the port order: no difference,
no single-use internal net, no missing symbol.

## CACE (`verification/cace/`)

`d2s_bias_in_pd.yaml`, templates `templates/d2s_bias_in_pd_tb_{dc,psrr,startup,pd}.sch`. Each template is the cell's symbol with net labels on
its pins, one drawn source (Ven, the enable) and a code block with the other sources and the measurement.
The external reference is a 5 uA PMOS mirror on its own supply vext (like the harness iDAC); `Iref` is the current at the iref pin through a 0 V sense source.

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
make sim-cace                               # every group: results/d2s_bias_in_pd/summary_<group>.md, <group>.csv, *.png (the PNGs are not committed: rerun to get them)
make sim-cace CACE_GROUPS=pd_params         # one group
make spec-table                             # limit and worst case per quantity (see the note on % units below)
```

The Makefile is `macros/inverter/Makefile` with TOP = d2s_bias_in_pd and the sim-cace / spec-table targets of the level-shifter
pair. It was delivered as `Makefile.new` (the file tool refuses files named Makefile): rename it to `Makefile`.

## Results (pre-layout, schematic netlist, 2026-10-20)

Simulated in the cloud with the pinned tools of `sudelbuecher/cloud_environment.md` (xschem 3.4.8RC `ddc7344`,
ngspice-47, OpenVAF `5ed9e63`, IHP-Open-PDK iic-jku `c271a7e9`) and CACE 2.13.0. Display units; `%/V` = percent per volt.
**The limits are proposals**: worst case of these runs plus about 30 % (two-sided currents: 30 % on the deviation from
nominal, 40 % for mismatch). Replace them by requirements.

| group | quantity | unit | limit (proposal) | min | max | runs | verdict |
|---|---|---|---|---:|---:|---:|---|
| dc_params | Bias current bp | uA | >= 4.93 <= 5.12 | 5.039 | 5.089 | 45 | pass |
| dc_params | Bias current bn | uA | >= 4.93 <= 5.13 | 5.046 | 5.102 | 45 | pass |
| dc_params | Bias current bnc | uA | >= 1.97 <= 2.14 | 2.052 | 2.109 | 45 | pass |
| dc_params | Bias current bpc | uA | >= 1.91 <= 2.03 | 1.933 | 1.956 | 45 | pass |
| dc_params | Bias current abp | uA | >= 4.93 <= 5.09 | 5.005 | 5.07 | 45 | pass |
| dc_params | Bias current abn | uA | >= 4.93 <= 5.13 | 5.039 | 5.097 | 45 | pass |
| dc_params | Supply current vdd | uA | <= 26 | 19.12 | 19.34 | 45 | pass |
| dc_params | Supply current vddo | uA | <= 6.6 | 5.005 | 5.07 | 45 | pass |
| dc_params | Reference current at the iref pin | uA | any | 5.008 | 5.011 | 45 | pass |
| dc_params | Line sensitivity bp | %/V | <= 1.3 | 0.6267 | 0.9498 | 45 | pass |
| dc_params | Line sensitivity bn | %/V | <= 1.5 | 0.7427 | 1.095 | 45 | pass |
| dc_params | Line sensitivity bnc | %/V | <= 1.5 | 0.7589 | 1.115 | 45 | pass |
| dc_params | Line sensitivity bpc | %/V | <= 1.4 | 0.671 | 1.065 | 45 | pass |
| dc_params | Line sensitivity abp | %/V | <= 2.0 | 0.6265 | 1.47 | 45 | pass |
| dc_params | Line sensitivity abn | %/V | <= 1.6 | 0.7868 | 1.227 | 45 | pass |
| mm_params | Bias current bp - mismatch | uA | >= 4.93 <= 5.23 | 4.947 | 5.164 | 30 | pass |
| mm_params | Bias current bn - mismatch | uA | >= 4.93 <= 5.25 | 4.949 | 5.176 | 30 | pass |
| mm_params | Bias current bnc - mismatch | uA | >= 1.97 <= 2.17 | 2.03 | 2.122 | 30 | pass |
| mm_params | Bias current bpc - mismatch | uA | >= 1.83 <= 2.03 | 1.88 | 2.016 | 30 | pass |
| mm_params | Bias current abp - mismatch | uA | >= 4.9 <= 5.18 | 4.926 | 5.13 | 30 | pass |
| mm_params | Bias current abn - mismatch | uA | >= 4.9 <= 5.25 | 4.929 | 5.177 | 30 | pass |
| mm_params | Supply current vdd - mismatch | uA | any | 18.8 | 19.63 | 30 | pass |
| mm_params | Supply current vddo - mismatch | uA | any | 4.926 | 5.13 | 30 | pass |
| mm_params | Reference current at the iref pin - mismatch | uA | any | 5.009 | 5.009 | 30 | pass |
| mm_params | Line sensitivity bp - mismatch | %/V | any | 0.7572 | 0.7664 | 30 | pass |
| mm_params | Line sensitivity bn - mismatch | %/V | any | 0.8838 | 0.8942 | 30 | pass |
| mm_params | Line sensitivity bnc - mismatch | %/V | any | 0.9028 | 0.9109 | 30 | pass |
| mm_params | Line sensitivity bpc - mismatch | %/V | any | 0.8358 | 0.8484 | 30 | pass |
| mm_params | Line sensitivity abp - mismatch | %/V | any | 0.8931 | 0.9044 | 30 | pass |
| mm_params | Line sensitivity abn - mismatch | %/V | any | 0.9512 | 0.9597 | 30 | pass |
| psrr_params | Supply sensitivity vdd, 1kHz | %/V | <= 1.4 | 0.8116 | 1.056 | 9 | pass |
| psrr_params | Supply sensitivity vdd, 100kHz | %/V | <= 1.4 | 0.8219 | 1.064 | 9 | pass |
| psrr_params | Supply sensitivity vdd, 1MHz | %/V | <= 2.3 | 1.589 | 1.713 | 9 | pass |
| psrr_params | Supply sensitivity vss, 1kHz | %/V | <= 1.5 | 0.7884 | 1.147 | 9 | pass |
| psrr_params | Supply sensitivity vss, 100kHz | %/V | <= 1.6 | 0.8106 | 1.158 | 9 | pass |
| psrr_params | Supply sensitivity vss, 1MHz | %/V | <= 2.8 | 1.985 | 2.101 | 9 | pass |
| psrr_params | Supply sensitivity vddo, 1kHz | %/V | <= 2.1 | 0.9201 | 1.557 | 9 | pass |
| psrr_params | Supply sensitivity vddo, 100kHz | %/V | <= 2.1 | 0.9629 | 1.58 | 9 | pass |
| psrr_params | Supply sensitivity vddo, 1MHz | %/V | <= 4.1 | 2.954 | 3.088 | 9 | pass |
| psrr_params | Supply sensitivity vsso, 1kHz | %/V | <= 0.35 | 0.2074 | 0.2653 | 9 | pass |
| psrr_params | Supply sensitivity vsso, 100kHz | %/V | <= 0.41 | 0.2706 | 0.3088 | 9 | pass |
| psrr_params | Supply sensitivity vsso, 1MHz | %/V | <= 2.3 | 1.597 | 1.744 | 9 | pass |
| startup_params | Start-up time to 90 % bn current | us | <= 70 | 0.4617 | 53.55 | 24 | pass |
| startup_params | bn current after start-up / dc |  | >= 0.95 <= 1.05 | 1 | 1 | 24 | pass |
| startup_params | abp current after start-up / dc |  | >= 0.95 <= 1.05 | 1 | 1 | 24 | pass |
| pd_params | Supply current vdd, disabled | nA | <= 0.91 | 3.053e-05 | 0.6974 | 30 | pass |
| pd_params | Supply current vddo, disabled | nA | <= 0.062 | 2.922e-06 | 0.04755 | 30 | pass |
| pd_params | Current at the iref pin, disabled | nA | <= 0.47 | 3.435e-06 | 0.3551 | 30 | pass |
| pd_params | Largest bias current, disabled | nA | <= 0.22 | 6.058e-06 | 0.1673 | 30 | pass |
| pd_params | Enable time, bn current | us | <= 0.21 | 0.1243 | 0.1604 | 30 | pass |
| pd_params | Enable time, abp current | us | <= 0.092 | 0.06197 | 0.07 | 30 | pass |

Mismatch, sigma / mean (mean deviation from nominal), N = 30: bp 1.16 % (+0.80 %)  bn 1.17 % (+1.04 %)  bnc 1.09 % (+3.56 %)  bpc 1.51 % (-2.92 %)  abp 0.97 % (+0.93 %)  abn 1.23 % (+0.83 %)

### Cross-check against the pre-CACE results

Bias currents, % deviation from nominal (5 / 5 / 2 / 2 / 5 / 5 uA); results_bias.txt (`d2s_bias_ref.spice` without enable, ideal iref) vs this CACE run (`_pd` sheet, 5 uA mirror as iref):

| corner | source | bp | bn | bnc | bpc | abp | abn |
|---|---|---:|---:|---:|---:|---:|---:|
| tt 27C | results_bias.txt | 1.05 | 1.24 | 3.80 | -2.96 | 0.68 | 1.13 |
| tt 27C | CACE | 1.24 | 1.43 | 3.99 | -2.78 | 0.86 | 1.32 |
| ss 3.0V -40C | results_bias.txt | 0.72 | 0.84 | 4.10 | -3.52 | -0.06 | 0.67 |
| ss 3.0V -40C | CACE | 0.88 | 1.00 | 4.27 | -3.36 | 0.10 | 0.83 |
| ff 3.6V 125C | results_bias.txt | 1.26 | 1.53 | 3.29 | -2.40 | 1.18 | 1.46 |
| ff 3.6V 125C | CACE | 1.49 | 1.75 | 3.52 | -2.18 | 1.40 | 1.68 |

The CACE reference is the 5 uA mirror, which delivers 5.0094 uA at the iref pin (tt 27 C 3.3 V): that accounts for the common offset of +0.19 % against the ideal 5 uA of results_bias.txt.

Line sensitivity at tt 27 C, %/V (results_bias.txt: secant 3.0 ... 3.6 V; CACE: +-0.1 V around 3.3 V): bp +0.78 / +0.76, bn +0.90 / +0.89, bnc +0.92 / +0.91, bpc +0.85 / +0.84, abp +0.91 / +0.90, abn +0.97 / +0.96.

Supply rejection at tt 27 C, largest |dI / I| of the six currents, %/V, results_bias.txt / CACE:

| rail | 1 kHz | 100 kHz | 1 MHz |
|---|---:|---:|---:|
| vdd | 0.95 / 0.95 | 0.96 / 0.96 | 1.57 / 1.61 |
| vss | 0.90 / 0.90 | 0.92 / 0.92 | 1.74 / 2.05 |
| vddo | 1.22 / 1.22 | 1.24 / 1.25 | 2.24 / 2.98 |
| vsso | 0.24 / 0.24 | 0.26 / 0.29 | 1.07 / 1.64 |

Mismatch sigma / mean, %, results_bias.txt (N = 100) / CACE (N = 30): bp 1.02 / 1.16, bn 1.16 / 1.17, bnc 1.18 / 1.09, bpc 1.39 / 1.51, abp 0.94 / 0.97, abn 1.06 / 1.23.

Disabled, ff 125 C 3.6 V: bias-cell current from vdd 0.743 nA in results_power_down.txt (section 2, "bias") / 0.697 nA here.
Enable, tt 27 C 3.6 V: bn current within +-10 % 0.14 us after the edge (the power-down log reports the driver I_Q: 0.5 - 0.9 us for in, out, bg).

`make spec-table` (`scripts/cace/spec_table.py`) does not scale `%` units: for the `%/V` rows it prints the raw fraction per
volt (0.0078 for 0.78 %/V). The table above was made with the correct scaling.
