<!--
SPDX-FileCopyrightText: 2026 Christoph Maier
SPDX-License-Identifier: Apache-2.0
-->
# `d2s_bias_oa_pd`: bias of the class-AB pad driver, with power-down

`d2s_bias_oa_pd` is the bias of `d2s_mpdda_pd` from a **self-contained Oguey-Aebischer reference** (no resistor, no BJT; M10/M11 in weak inversion, vres = U_T ln 16), feeding the same mirror tree as `d2s_bias_in_pd`. Its current is proportional to mu T^2: about -35 % / +35 % over -40 ... 125 C.

It is one of the four bias variants of `d2s_mpdda_pd` (in, out, oa, bg). All four keep `d2s_bias_lp`'s six bias
diodes and so the bias voltages the driver sees: vbp 5 uA (BP, unit tails), vbn 5 uA (BN, fold sinks), vbpc 2 uA (BPC,
mirror cascodes), vbnc 2 uA (BNC, fold cascodes), vabp 5 uA (RP2 on RP1, class-AB P side), vabn 5 uA (RN2 on RN1, class-AB N side).
The class-AB replicas RP1 / RN1 sit on the output-stage rails vddo / vsso (in the pad: iovdd / iovss), everything else on vdd / vss.
Design, sizing and every pre-CACE number: `~/EDA/sg13cmos5l_cm_ip__single2diff2single_sudelbuecher/sudelbuecher/design_considerations/class_ab_pad_driver/improvements/bias.md` (numbers from `improvements/sim/run_bias.py`,
`improvements/sim/results_bias.txt`); power-down: `~/EDA/sg13cmos5l_cm_ip__single2diff2single_sudelbuecher/sudelbuecher/design_considerations/class_ab_pad_driver/power_down/log.md`, `power_down/xschem/README.md`,
`power_down/sim/results_power_down.txt` (indexed here, not copied).

Source netlist: `../sg13cmos5l_IOPadDiff2Single/netlist/source/d2s_bias_ref_pd.spice`, subckt `d2s_bias_oa_pd`.

## Ports (symbol and subckt order)

`vdd vss vddo vsso vbp vbn vbpc vbnc vabp vabn en_3v3`

en_3v3: 0 / vdd, active high. The cell makes its own en_3v3_b (inverter IP / IN, 1u / 0.45u).

## Enabled and disabled

Enabled (en_3v3 = vdd), every switch is off (the transmission gate on) and the cell is its `improvements/` version
`d2s_bias_oa`. Disabled (en_3v3 = 0), the root of every current is switched off:

- MS1, the always-on start-up pull-up: gate on en_3v3_b (was vss), so it is off.
- SKS pulls ks to vss (start-up held off); SVPG pulls vpg to vdd (PMOS mirror of the core off).
- TGN / TGP cut the core output off the tree input ni; TDN pulls ni to vss.

The other bias lines carry leakage only and get no switch. All switches are 1u / 0.45u hv devices.

## Schematic

`schematic/xschem/d2s_bias_oa_pd.sch` / `.sym`. The sheet is an unchanged copy of `power_down/xschem/d2s_bias_oa_pd.sch` (2026-10-06 18:45).

Checked here: xschem's netlist of the sheet against the subckt `d2s_bias_oa_pd` of `d2s_bias_ref_pd.spice`, device by device
(model, w / l / ng, terminal nets with the internal nets matched by name), and the port order: no difference,
no single-use internal net, no missing symbol.

## CACE (`verification/cace/`)

`d2s_bias_oa_pd.yaml`, templates `templates/d2s_bias_oa_pd_tb_{dc,psrr,startup,pd}.sch`. Each template is the cell's symbol with net labels on
its pins, one drawn source (Ven, the enable) and a code block with the other sources and the measurement.
No external reference.

- The six bias currents are the drain currents of the six diodes inside the cell, `@n.x1.<diode>.nsg13_hv_[np]mos[ids]`
  (the quantity `run_bias.py` reports). Line sensitivity: dI / I per volt, vdd = vddo moved by +-0.1 V around the condition.
- PSRR (AC current needs a sense source): replicas of the six diodes in the testbench, gate on the bias line, drain held
  at the line voltage by an E source through a 0 V source. Their small-signal current equals the diode's. Reported per rail
  (vdd, vss, vddo, vsso): the largest |dI / I| of the six currents per volt of ripple, at 1 kHz, 100 kHz and 1 MHz.
- Start-up: every supply ramps from 0 V (uic, Gear) in 1 or 100 us, en_3v3 follows vdd. t_su90 = last crossing of 90 % of
  the final bn current, counted from the start of the ramp (so it includes the ramp). Rbn_end / Rabp_end = current 1 ms
  after the ramp relative to the dc operating point.
- Power-down: operating point with en_3v3 = 0 (supply current per rail, largest diode current), then en_3v3
  rises at 10 us in 10 ns: t_en90 = from the edge until the bn / abp current stays within +-10 % of its settled value
  (the definition of the power-down log's start-up t90).
  
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
make sim-cace                               # every group: results/d2s_bias_oa_pd/summary_<group>.md, <group>.csv, *.png (the PNGs are not committed: rerun to get them)
make sim-cace CACE_GROUPS=pd_params         # one group
make spec-table                             # limit and worst case per quantity (see the note on % units below)
```

The Makefile is `macros/inverter/Makefile` with TOP = d2s_bias_oa_pd and the sim-cace / spec-table targets of the level-shifter
pair. It was delivered as `Makefile.new` (the file tool refuses files named Makefile): rename it to `Makefile`.

## Results (pre-layout, schematic netlist, 2026-10-20)

Simulated in the cloud with the pinned tools of `sudelbuecher/cloud_environment.md` (xschem 3.4.8RC `ddc7344`,
ngspice-47, OpenVAF `5ed9e63`, IHP-Open-PDK iic-jku `c271a7e9`) and CACE 2.13.0. Display units; `%/V` = percent per volt.
**The limits are proposals**: worst case of these runs plus about 30 % (two-sided currents: 30 % on the deviation from
nominal, 40 % for mismatch). Replace them by requirements.

| group | quantity | unit | limit (proposal) | min | max | runs | verdict |
|---|---|---|---|---:|---:|---:|---|
| dc_params | Bias current bp | uA | >= 2.51 <= 7.76 | 3.085 | 7.125 | 45 | pass |
| dc_params | Bias current bn | uA | >= 2.52 <= 7.78 | 3.09 | 7.141 | 45 | pass |
| dc_params | Bias current bnc | uA | >= 1.06 <= 3.18 | 1.277 | 2.907 | 45 | pass |
| dc_params | Bias current bpc | uA | >= 0.935 <= 2.97 | 1.181 | 2.745 | 45 | pass |
| dc_params | Bias current abp | uA | >= 2.47 <= 7.76 | 3.057 | 7.122 | 45 | pass |
| dc_params | Bias current abn | uA | >= 2.51 <= 7.78 | 3.085 | 7.135 | 45 | pass |
| dc_params | Supply current vdd | uA | <= 50 | 16.87 | 38.44 | 45 | pass |
| dc_params | Supply current vddo | uA | <= 9.3 | 3.057 | 7.122 | 45 | pass |
| dc_params | Line sensitivity bp | %/V | <= 1.7 | 0.6599 | 1.307 | 45 | pass |
| dc_params | Line sensitivity bn | %/V | <= 1.9 | 0.7799 | 1.424 | 45 | pass |
| dc_params | Line sensitivity bnc | %/V | <= 1.9 | 0.8039 | 1.423 | 45 | pass |
| dc_params | Line sensitivity bpc | %/V | <= 1.8 | 0.7111 | 1.356 | 45 | pass |
| dc_params | Line sensitivity abp | %/V | <= 2.3 | 0.6628 | 1.745 | 45 | pass |
| dc_params | Line sensitivity abn | %/V | <= 2.0 | 0.8199 | 1.478 | 45 | pass |
| mm_params | Bias current bp - mismatch | uA | >= 4.44 <= 5.73 | 4.598 | 5.523 | 30 | pass |
| mm_params | Bias current bn - mismatch | uA | >= 4.46 <= 5.76 | 4.615 | 5.545 | 30 | pass |
| mm_params | Bias current bnc - mismatch | uA | >= 1.85 <= 2.38 | 1.895 | 2.27 | 30 | pass |
| mm_params | Bias current bpc - mismatch | uA | >= 1.71 <= 2.2 | 1.791 | 2.143 | 30 | pass |
| mm_params | Bias current abp - mismatch | uA | >= 4.48 <= 5.68 | 4.627 | 5.488 | 30 | pass |
| mm_params | Bias current abn - mismatch | uA | >= 4.42 <= 5.75 | 4.589 | 5.537 | 30 | pass |
| mm_params | Supply current vdd - mismatch | uA | any | 24.97 | 29.95 | 30 | pass |
| mm_params | Supply current vddo - mismatch | uA | any | 4.627 | 5.488 | 30 | pass |
| mm_params | Line sensitivity bp - mismatch | %/V | any | 0.8663 | 0.9254 | 30 | pass |
| mm_params | Line sensitivity bn - mismatch | %/V | any | 0.9937 | 1.05 | 30 | pass |
| mm_params | Line sensitivity bnc - mismatch | %/V | any | 1.015 | 1.066 | 30 | pass |
| mm_params | Line sensitivity bpc - mismatch | %/V | any | 0.9493 | 1.002 | 30 | pass |
| mm_params | Line sensitivity abp - mismatch | %/V | any | 1.007 | 1.054 | 30 | pass |
| mm_params | Line sensitivity abn - mismatch | %/V | any | 1.064 | 1.116 | 30 | pass |
| psrr_params | Supply sensitivity vdd, 1kHz | %/V | <= 3.2 | 0.6897 | 2.395 | 9 | pass |
| psrr_params | Supply sensitivity vdd, 100kHz | %/V | <= 8.4 | 3.248 | 6.434 | 9 | pass |
| psrr_params | Supply sensitivity vdd, 1MHz | %/V | <= 8.5 | 3.302 | 6.467 | 9 | pass |
| psrr_params | Supply sensitivity vss, 1kHz | %/V | <= 2.0 | 0.8601 | 1.468 | 9 | pass |
| psrr_params | Supply sensitivity vss, 100kHz | %/V | <= 8.5 | 3.185 | 6.478 | 9 | pass |
| psrr_params | Supply sensitivity vss, 1MHz | %/V | <= 9.0 | 3.362 | 6.871 | 9 | pass |
| psrr_params | Supply sensitivity vddo, 1kHz | %/V | <= 2.3 | 0.8481 | 1.716 | 9 | pass |
| psrr_params | Supply sensitivity vddo, 100kHz | %/V | <= 2.4 | 0.8715 | 1.771 | 9 | pass |
| psrr_params | Supply sensitivity vddo, 1MHz | %/V | <= 6.1 | 2.178 | 4.678 | 9 | pass |
| psrr_params | Supply sensitivity vsso, 1kHz | %/V | <= 0.35 | 0.2064 | 0.2683 | 9 | pass |
| psrr_params | Supply sensitivity vsso, 100kHz | %/V | <= 0.46 | 0.2612 | 0.3507 | 9 | pass |
| psrr_params | Supply sensitivity vsso, 1MHz | %/V | <= 3.4 | 1.247 | 2.581 | 9 | pass |
| startup_params | Start-up time to 90 % bn current | us | <= 130 | 0.948 | 95.01 | 24 | pass |
| startup_params | bn current after start-up / dc |  | >= 0.95 <= 1.05 | 1 | 1 | 24 | pass |
| startup_params | abp current after start-up / dc |  | >= 0.95 <= 1.05 | 1 | 1 | 24 | pass |
| pd_params | Supply current vdd, disabled | nA | <= 1.4 | 5.16e-05 | 1.044 | 30 | pass |
| pd_params | Supply current vddo, disabled | nA | <= 0.062 | 2.932e-06 | 0.04755 | 30 | pass |
| pd_params | Largest bias current, disabled | nA | <= 0.22 | 6.029e-06 | 0.1673 | 30 | pass |
| pd_params | Enable time, bn current | us | <= 21 | 6.095 | 16 | 30 | pass |
| pd_params | Enable time, abp current | us | <= 21 | 6.084 | 16 | 30 | pass |

Mismatch, sigma / mean (mean deviation from nominal), N = 30: bp 4.35 % (+1.92 %)  bn 4.29 % (+2.16 %)  bnc 4.22 % (+4.70 %)  bpc 4.42 % (-1.96 %)  abp 4.38 % (+1.53 %)  abn 4.32 % (+1.99 %)

### Cross-check against the pre-CACE results

Bias currents, % deviation from nominal (5 / 5 / 2 / 2 / 5 / 5 uA); results_bias.txt (`d2s_bias_ref.spice` without enable) vs this CACE run (`_pd` sheet):

| corner | source | bp | bn | bnc | bpc | abp | abn |
|---|---|---:|---:|---:|---:|---:|---:|
| tt 27C | results_bias.txt | 1.04 | 1.23 | 3.79 | -2.97 | 0.67 | 1.12 |
| tt 27C | CACE | 1.04 | 1.23 | 3.79 | -2.97 | 0.67 | 1.12 |
| ss 3.0V -40C | results_bias.txt | -38.30 | -38.20 | -36.16 | -40.97 | -38.85 | -38.30 |
| ss 3.0V -40C | CACE | -38.30 | -38.20 | -36.16 | -40.97 | -38.85 | -38.30 |
| ff 3.6V 125C | results_bias.txt | 42.68 | 43.00 | 45.55 | 37.45 | 42.62 | 42.89 |
| ff 3.6V 125C | CACE | 42.49 | 42.81 | 45.36 | 37.27 | 42.44 | 42.71 |

Line sensitivity at tt 27 C, %/V (results_bias.txt: secant 3.0 ... 3.6 V; CACE: +-0.1 V around 3.3 V): bp +0.91 / +0.89, bn +1.04 / +1.02, bnc +1.06 / +1.04, bpc +0.99 / +0.97, abp +1.04 / +1.03, abn +1.11 / +1.08.

Supply rejection at tt 27 C, largest |dI / I| of the six currents, %/V, results_bias.txt / CACE:

| rail | 1 kHz | 100 kHz | 1 MHz |
|---|---:|---:|---:|
| vdd | 1.10 / 1.09 | 4.46 / 4.52 | 4.55 / 4.58 |
| vss | 1.05 / 1.05 | 4.42 / 4.43 | 4.58 / 4.69 |
| vddo | 1.22 / 1.22 | 1.24 / 1.25 | 2.24 / 2.98 |
| vsso | 0.24 / 0.24 | 0.26 / 0.29 | 1.07 / 1.64 |

Mismatch sigma / mean, %, results_bias.txt (N = 100) / CACE (N = 30): bp 5.12 / 4.35, bn 5.14 / 4.29, bnc 5.13 / 4.22, bpc 5.28 / 4.42, abp 5.21 / 4.38, abn 5.14 / 4.32.

Start-up t90 from 0 V, us (results_bias.txt / CACE): ss 3.0V -40C 1 us ramp 1.2 / 1.2, ss 3.0V -40C 100 us ramp 95.0 / 95.0, ff 3.6V 125C 1 us ramp 1.1 / 1.1, ff 3.6V 125C 100 us ramp 71.1 / 71.0.

Disabled, ff 125 C 3.6 V: bias-cell current from vdd 1.115 nA in results_power_down.txt (section 2, "bias") / 1.044 nA here.
Enable, tt 27 C 3.6 V: bn current within +-10 % 12.16 us after the edge (the power-down log reports the driver I_Q: 8 - 15 us for oa).

`make spec-table` (`scripts/cace/spec_table.py`) does not scale `%` units: for the `%/V` rows it prints the raw fraction per
volt (0.0078 for 0.78 %/V). The table above was made with the correct scaling.
