<!--
SPDX-FileCopyrightText: 2026 Christoph Maier
SPDX-License-Identifier: Apache-2.0
-->
# `bias_bg_pd`: bias of the class-AB pad driver, with power-down

`bias_bg_pd` is the bias of `d2s_mpdda_pd` from a **self-contained current-mode bandgap** (Banba type, pnpMPA and rhigh, no op-amp), feeding the same mirror tree as `bias_in_pd`. Flat over temperature and MOS corners, but it follows the rhigh corners (about -20 % / +30 %).

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

Source netlist: `../bias_tree_pd/netlist/source/bias_ref_pd.spice`, subckt `bias_bg_pd`.

## Ports (symbol and subckt order)

`vdd vss vbp vbn vbpc vbnc vabp vabn en_3v3`

en_3v3: 0 / vdd, active high. The cell makes its own en_3v3_b (inverter IP / IN, 1u / 0.45u).

## Enabled and disabled

Enabled (en_3v3 = vdd), every switch is off (the transmission gate on) and the cell is its `improvements/` version
`d2s_bias_bg`. Disabled (en_3v3 = 0), the root of every current is switched off:

- MS1, the always-on start-up pull-up: gate on en_3v3_b (was vss), so it is off.
- SKS pulls ks to vss (start-up held off); SVPG pulls vpg to vdd (PMOS mirror of the core off).
- TGN / TGP cut the core output off the tree input ni; TDN pulls ni to vss.

The other bias lines carry leakage only and get no switch. All switches are 1u / 0.45u hv devices.

## Schematic

`schematic/xschem/bias_bg_pd.sch` / `.sym`. The sheet is a copy of `power_down/xschem/d2s_bias_bg_pd.sch` as hand-edited on 2026-10-09 00:12 (the transmission gate moved to y = -740). That version netlisted wrong in three places, repaired in this copy by wire edits only (no device moved): (1) the vss rail at y = -160 was open between x = 1280 and 1420, so the sources and bulks of NBP, NBPC, NABP, BN, BNC and RN2's bulk were on a floating net: added `N 1280 -160 1420 -160`; (2) TGP's iref-side terminal (1280,-770) was on vdd and its bulk on vss: removed `N 1280 -800 1280 -770`, `N 1260 -740 1280 -740` (vss) and `N 1260 -740 1260 -260`, added `N 1280 -790 1280 -770`, `N 1160 -790 1280 -790` (to POC's drain = iref) and `N 1260 -740 1280 -740`, `N 1260 -800 1260 -740` (bulk to the vdd row); (3) TGN's bulk was on vdd: removed `N 1160 -740 1180 -740` and `N 1180 -800 1180 -740`, added `N 1160 -740 1200 -740`, `N 1200 -740 1200 -160` (to vss). The lab_wire `iref` (l20) moved from (1200,-800) onto the new iref wire at (1220,-790). The original in `power_down/xschem/` is unchanged.

Checked here: xschem's netlist of the sheet against the subckt `bias_bg_pd` of `bias_ref_pd.spice`, device by device
(model, w / l / ng, terminal nets with the internal nets matched by name), and the port order: no difference (TGN has source and drain swapped, the same device),
no single-use internal net, no missing symbol.

## CACE (`verification/cace/`)

`bias_bg_pd.yaml`, templates `templates/bias_bg_pd_tb_{dc,psrr,startup,pd}.sch`. Each template is the cell's symbol with net labels on
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
  
- Mismatch: 30 iterations (seed 12345 + iteration), mos_tt_mismatch / res_typ_mismatch, schematic netlist only. pnpMPA has no mismatch model.
- Tolerances: dc and operating points gmin = abstol = 1e-15; transients 1e-12 (1e-15 makes the floating disabled nodes ~27x slower).

| group | conditions | runs |
|---|---|---:|
| dc_params | corner_mos ss/sf/tt/fs/ff x temp -40/27/125 x vdd 3.0/3.3/3.6 | 45 |
| dc_rp_params | corner_r wcs/typ/bcs x corner_pnp wcs/typ/bcs, tt 27 C 3.3 V | 9 |
| mm_params | 30 mismatch iterations, tt 27 C 3.3 V | 30 |
| psrr_params | corner_mos ss/tt/ff x temp -40/27/125, 3.3 V | 9 |
| startup_params | corner_mos ss/tt/ff x temp -40/125 x vdd 3.0/3.6 x ramp 1/100 us | 24 |
| pd_params | corner_mos ss/sf/tt/fs/ff x temp -40/27/125 x vdd 3.0/3.6 | 30 |

Run (IIC-OSIC-TOOLS, after `source .designinit` in the repo root):

```sh
make sim-cace                               # every group: results/bias_bg_pd/summary_<group>.md, <group>.csv, *.png (the PNGs are not committed: rerun to get them)
make sim-cace CACE_GROUPS=pd_params         # one group
make spec-table                             # limit and worst case per quantity (see the note on % units below)
```

The Makefile is `macros/inverter/Makefile` with TOP = bias_bg_pd and the sim-cace / spec-table targets of the level-shifter
pair. It was delivered as `Makefile.new` (the file tool refuses files named Makefile): rename it to `Makefile`.

## Results (pre-layout, schematic netlist, 2026-10-20)

Simulated in the cloud with the pinned tools of `sudelbuecher/cloud_environment.md` (xschem 3.4.8RC `ddc7344`,
ngspice-47, OpenVAF `5ed9e63`, IHP-Open-PDK iic-jku `c271a7e9`) and CACE 2.13.0. Display units; `%/V` = percent per volt.
**The limits are proposals**: worst case of these runs plus about 30 % (two-sided currents: 30 % on the deviation from
nominal, 40 % for mismatch). Replace them by requirements.

| group | quantity | unit | limit (proposal) | min | max | runs | verdict |
|---|---|---|---|---:|---:|---:|---|
| dc_params | Bias current bp | uA | >= 4.92 <= 5.12 | 4.941 | 5.092 | 45 | pass |
| dc_params | Bias current bn | uA | >= 4.93 <= 5.14 | 4.947 | 5.105 | 45 | pass |
| dc_params | Bias current bnc | uA | >= 1.97 <= 2.12 | 2.016 | 2.094 | 45 | pass |
| dc_params | Bias current bpc | uA | >= 1.86 <= 2.03 | 1.893 | 1.955 | 45 | pass |
| dc_params | Bias current abp | uA | >= 4.87 <= 5.1 | 4.903 | 5.078 | 45 | pass |
| dc_params | Bias current abn | uA | >= 4.92 <= 5.13 | 4.939 | 5.101 | 45 | pass |
| dc_params | Supply current vdd | uA | <= 39 | 28.88 | 29.98 | 45 | pass |
| dc_params | Supply current vddo | uA | <= 6.7 | 4.903 | 5.078 | 45 | pass |
| dc_params | Line sensitivity bp | %/V | <= 2.7 | 1.139 | 2.008 | 45 | pass |
| dc_params | Line sensitivity bn | %/V | <= 2.9 | 1.253 | 2.158 | 45 | pass |
| dc_params | Line sensitivity bnc | %/V | <= 2.9 | 1.272 | 2.181 | 45 | pass |
| dc_params | Line sensitivity bpc | %/V | <= 2.8 | 1.182 | 2.126 | 45 | pass |
| dc_params | Line sensitivity abp | %/V | <= 3.4 | 1.143 | 2.546 | 45 | pass |
| dc_params | Line sensitivity abn | %/V | <= 3.0 | 1.298 | 2.298 | 45 | pass |
| dc_rp_params | Bias current bp | uA | >= 3.7 <= 6.94 | 4.001 | 6.491 | 9 | pass |
| dc_rp_params | Bias current bn | uA | >= 3.71 <= 6.95 | 4.009 | 6.502 | 9 | pass |
| dc_rp_params | Bias current bnc | uA | >= 1.54 <= 2.87 | 1.644 | 2.667 | 9 | pass |
| dc_rp_params | Bias current bpc | uA | >= 1.4 <= 2.64 | 1.537 | 2.494 | 9 | pass |
| dc_rp_params | Bias current abp | uA | >= 3.68 <= 6.91 | 3.984 | 6.471 | 9 | pass |
| dc_rp_params | Bias current abn | uA | >= 3.71 <= 6.94 | 4.005 | 6.495 | 9 | pass |
| dc_rp_params | Supply current vdd | uA | <= 50 | 23.56 | 37.98 | 9 | pass |
| dc_rp_params | Supply current vddo | uA | any | 3.984 | 6.471 | 9 | pass |
| dc_rp_params | Line sensitivity bp | %/V | any | 1.234 | 1.282 | 9 | pass |
| dc_rp_params | Line sensitivity bn | %/V | any | 1.365 | 1.404 | 9 | pass |
| dc_rp_params | Line sensitivity bnc | %/V | any | 1.389 | 1.42 | 9 | pass |
| dc_rp_params | Line sensitivity bpc | %/V | any | 1.319 | 1.36 | 9 | pass |
| dc_rp_params | Line sensitivity abp | %/V | any | 1.377 | 1.408 | 9 | pass |
| dc_rp_params | Line sensitivity abn | %/V | any | 1.441 | 1.463 | 9 | pass |
| mm_params | Bias current bp - mismatch | uA | >= 4.49 <= 5.6 | 4.636 | 5.428 | 30 | pass |
| mm_params | Bias current bn - mismatch | uA | >= 4.51 <= 5.59 | 4.649 | 5.421 | 30 | pass |
| mm_params | Bias current bnc - mismatch | uA | >= 1.87 <= 2.32 | 1.905 | 2.232 | 30 | pass |
| mm_params | Bias current bpc - mismatch | uA | >= 1.68 <= 2.12 | 1.769 | 2.087 | 30 | pass |
| mm_params | Bias current abp - mismatch | uA | >= 4.44 <= 5.51 | 4.598 | 5.363 | 30 | pass |
| mm_params | Bias current abn - mismatch | uA | >= 4.5 <= 5.58 | 4.645 | 5.414 | 30 | pass |
| mm_params | Supply current vdd - mismatch | uA | any | 27.31 | 31.6 | 30 | pass |
| mm_params | Supply current vddo - mismatch | uA | any | 4.598 | 5.363 | 30 | pass |
| mm_params | Line sensitivity bp - mismatch | %/V | any | 1.183 | 1.428 | 30 | pass |
| mm_params | Line sensitivity bn - mismatch | %/V | any | 1.312 | 1.553 | 30 | pass |
| mm_params | Line sensitivity bnc - mismatch | %/V | any | 1.328 | 1.57 | 30 | pass |
| mm_params | Line sensitivity bpc - mismatch | %/V | any | 1.265 | 1.512 | 30 | pass |
| mm_params | Line sensitivity abp - mismatch | %/V | any | 1.325 | 1.564 | 30 | pass |
| mm_params | Line sensitivity abn - mismatch | %/V | any | 1.381 | 1.615 | 30 | pass |
| psrr_params | Supply sensitivity vdd, 1kHz | %/V | <= 2.2 | 1.191 | 1.665 | 9 | pass |
| psrr_params | Supply sensitivity vdd, 100kHz | %/V | <= 3.6 | 2.411 | 2.761 | 9 | pass |
| psrr_params | Supply sensitivity vdd, 1MHz | %/V | <= 27 | 17.8 | 20.14 | 9 | pass |
| psrr_params | Supply sensitivity vss, 1kHz | %/V | <= 2.3 | 1.303 | 1.759 | 9 | pass |
| psrr_params | Supply sensitivity vss, 100kHz | %/V | <= 3.7 | 2.418 | 2.793 | 9 | pass |
| psrr_params | Supply sensitivity vss, 1MHz | %/V | <= 27 | 18.24 | 20.73 | 9 | pass |
| psrr_params | Supply sensitivity vddo, 1kHz | %/V | <= 2.1 | 0.923 | 1.562 | 9 | pass |
| psrr_params | Supply sensitivity vddo, 100kHz | %/V | <= 2.1 | 0.9668 | 1.585 | 9 | pass |
| psrr_params | Supply sensitivity vddo, 1MHz | %/V | <= 4.1 | 2.947 | 3.13 | 9 | pass |
| psrr_params | Supply sensitivity vsso, 1kHz | %/V | <= 0.35 | 0.2067 | 0.2641 | 9 | pass |
| psrr_params | Supply sensitivity vsso, 100kHz | %/V | <= 0.41 | 0.271 | 0.3091 | 9 | pass |
| psrr_params | Supply sensitivity vsso, 1MHz | %/V | <= 2.3 | 1.621 | 1.765 | 9 | pass |
| startup_params | Start-up time to 90 % bn current | us | <= 120 | 0.8465 | 88.37 | 24 | pass |
| startup_params | bn current after start-up / dc |  | >= 0.95 <= 1.05 | 1 | 1 | 24 | pass |
| startup_params | abp current after start-up / dc |  | >= 0.95 <= 1.05 | 1 | 1 | 24 | pass |
| pd_params | Supply current vdd, disabled | nA | <= 5.6 | 5.156e-05 | 4.258 | 30 | pass |
| pd_params | Supply current vddo, disabled | nA | <= 0.062 | 2.946e-06 | 0.04755 | 30 | pass |
| pd_params | Largest bias current, disabled | nA | <= 0.22 | 6.034e-06 | 0.1673 | 30 | pass |
| pd_params | Enable time, bn current | us | <= 0.38 | 0.167 | 0.2881 | 30 | pass |
| pd_params | Enable time, abp current | us | <= 0.33 | 0.1385 | 0.2534 | 30 | pass |

Mismatch, sigma / mean (mean deviation from nominal), N = 30: bp 3.55 % (+1.59 %)  bn 3.44 % (+1.92 %)  bnc 3.60 % (+4.35 %)  bpc 3.56 % (-2.08 %)  abp 3.64 % (+1.18 %)  abn 3.53 % (+1.76 %)

### Cross-check against the pre-CACE results

Bias currents, % deviation from nominal (5 / 5 / 2 / 2 / 5 / 5 uA); results_bias.txt (`d2s_bias_ref.spice` without enable) vs this CACE run (`_pd` sheet):

| corner | source | bp | bn | bnc | bpc | abp | abn |
|---|---|---:|---:|---:|---:|---:|---:|
| tt 27C | results_bias.txt | 1.23 | 1.42 | 3.99 | -2.79 | 0.86 | 1.31 |
| tt 27C | CACE | 1.23 | 1.42 | 3.99 | -2.79 | 0.86 | 1.31 |
| ss 3.0V -40C | results_bias.txt | -1.18 | -1.06 | 2.15 | -5.34 | -1.95 | -1.23 |
| ss 3.0V -40C | CACE | -1.18 | -1.06 | 2.15 | -5.34 | -1.95 | -1.23 |
| ff 3.6V 125C | results_bias.txt | 0.19 | 0.46 | 2.20 | -3.43 | 0.11 | 0.39 |
| ff 3.6V 125C | CACE | 0.18 | 0.45 | 2.19 | -3.44 | 0.10 | 0.38 |
| res wcs | results_bias.txt | -19.91 | -19.75 | -17.72 | -23.10 | -20.25 | -19.83 |
| res wcs | CACE | -19.91 | -19.75 | -17.72 | -23.10 | -20.25 | -19.83 |
| res bcs | results_bias.txt | 29.83 | 30.05 | 33.34 | 24.69 | 29.41 | 29.89 |
| res bcs | CACE | 29.83 | 30.05 | 33.34 | 24.68 | 29.41 | 29.89 |
| pnp wcs | results_bias.txt | 1.22 | 1.42 | 3.98 | -2.79 | 0.85 | 1.30 |
| pnp wcs | CACE | 1.22 | 1.42 | 3.98 | -2.79 | 0.85 | 1.30 |
| pnp bcs | results_bias.txt | 1.13 | 1.33 | 3.89 | -2.88 | 0.76 | 1.21 |
| pnp bcs | CACE | 1.13 | 1.32 | 3.89 | -2.88 | 0.76 | 1.21 |

Line sensitivity at tt 27 C, %/V (results_bias.txt: secant 3.0 ... 3.6 V; CACE: +-0.1 V around 3.3 V): bp +1.27 / +1.25, bn +1.40 / +1.38, bnc +1.42 / +1.39, bpc +1.35 / +1.33, abp +1.40 / +1.39, abn +1.47 / +1.44.

Supply rejection at tt 27 C, largest |dI / I| of the six currents, %/V, results_bias.txt / CACE:

| rail | 1 kHz | 100 kHz | 1 MHz |
|---|---:|---:|---:|
| vdd | 1.44 / 1.44 | 2.47 / 2.48 | 18.54 / 18.54 |
| vss | 1.39 / 1.39 | 2.45 / 2.49 | 18.73 / 18.99 |
| vddo | 1.22 / 1.22 | 1.24 / 1.25 | 2.24 / 2.97 |
| vsso | 0.24 / 0.24 | 0.26 / 0.29 | 1.07 / 1.64 |

Mismatch sigma / mean, %, results_bias.txt (N = 100) / CACE (N = 30): bp 2.71 / 3.55, bn 2.72 / 3.44, bnc 2.70 / 3.60, bpc 2.65 / 3.56, abp 2.70 / 3.64, abn 2.68 / 3.53.

Start-up t90 from 0 V, us (results_bias.txt / CACE): ss 3.0V -40C 1 us ramp 1.3 / 1.2, ss 3.0V -40C 100 us ramp 88.4 / 88.4, ff 3.6V 125C 1 us ramp 1.7 / 1.2, ff 3.6V 125C 100 us ramp 47.3 / 47.3.

Disabled, ff 125 C 3.6 V: bias-cell current from vdd 4.326 nA in results_power_down.txt (section 2, "bias") / 4.258 nA here.
Enable, tt 27 C 3.6 V: bn current within +-10 % 0.23 us after the edge (the power-down log reports the driver I_Q: 0.5 - 0.9 us for in, out, bg).

`make spec-table` (`scripts/cace/spec_table.py`) does not scale `%` units: for the `%/V` rows it prints the raw fraction per
volt (0.0078 for 0.78 %/V). The table above was made with the correct scaling.
