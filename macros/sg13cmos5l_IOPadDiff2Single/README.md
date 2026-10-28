<!--
SPDX-FileCopyrightText: 2026 Christoph Maier
SPDX-License-Identifier: Apache-2.0
-->
# `sg13cmos5l_IOPadDiff2Single` — differential-in, single-ended-out class-AB buffered pad

`pad - vref = (vinp - vinn) / 2`. Consolidated 2026-10-20 from the class-AB pad-driver work in the
`_sudelbuecher` worktree (`design_considerations/class_ab_pad_driver/{improvements,power_down}`), with a
selectable bias, a fail-safe enable and a CACE suite whose output follows
`chipalooza2/levelshifters/ls_pair` (summaries, CSV and plots in `verification/cace/results/`).

## Structure

| instance | cell (macro) | function |
|---|---|---|
| `xc` | `en_ctrl_3v3` (`../en_ctrl_3v3`) | `en_3v3 = en_1v2 ∧ vdd_1v2 present ∧ vdd_3v3 present`; level-shifted `sel*`; `en_3v3_b` = NOT `en_3v3` for `xt` and `xd` |
| `xg` | `bias_gen_pd` (`../bias_gen_pd`) | the reference current `iref` (sourced), selected by `sel1 sel0` |
| `xt` | `bias_tree_pd` (`../bias_tree_pd`) | six bias lines from one mirror tree fed by `iref`. `xg` + `xt` are the former `xb` = `bias_sel_pd`, device for device (split 2026-10-28) |
| `xd` | `d2s_mpdda_pd` (here) | Miller-compensated class-AB driver without its output stage (MP-DDA front end, folded cascode, class-AB control): drives the output gates a / b; power-down switches; RP2 / RN2, the upper halves of the class-AB diode stacks (block [8], since 2026-10-27, formerly in the bias tree) |
| `xfp`, `xfn` | `d2s_out_p`, `d2s_out_n` (here) | the output stage = the pad's clamp frames: OP with its replica RP1 and the dummy RPD (P frame), ON with its replica RN1 (both N frames); RP1 / RN1 are the lower halves of the class-AB stacks (nets dabp / dabn). Since 2026-10-28 |
| `CMA`, `CMB` | hv PMOS in accumulation | Miller capacitors a–pad and pad–b, W 7.96 µm × L 32.16 µm as drawn between the diodes (256 µm², as the former 16 × 16 µm). Since 2026-10-28 |
| `DN`, `DP` | IHP `sg13cmos5l_DCNDiode` / `DCPDiode` | primary ESD diodes, as in `sg13cmos5l_IOPadAnalog` |

`schematic/xschem/sg13cmos5l_IOPadDiff2Single.sch` (drawn from `netlist/source/sg13cmos5l_IOPadDiff2Single.spice`),
`d2s_mpdda_pd.sch` and `unit_r2.sch` (Christoph's sheets from `power_down/xschem` and `improvements/xschem`),
`d2s_out_p.sch` / `d2s_out_n.sch` (the clamp frames, from `netlist/source/d2s_out.spice`),
and `d2s_mpdda_pd_sel.sch`, a CACE-only fixture (driver + bias with `vfb` as a pin, for the loop gain).

**Output stage at pad level (2026-10-28).** OP / ON with RP1 / RPD / RN1 left `d2s_mpdda_pd` for the frame sheets
`d2s_out_p` / `d2s_out_n`, which group the devices as the layout does (one P clamp frame, two N clamp frames); CMA /
CMB are devices of the top sheet. `d2s_mpdda_pd` lost the port `vout` and the parameters `wc`, `lc` and got `a b dabp
dabn` after `vfb`. The fixture `d2s_mpdda_pd_sel` and the `tb_pd_*` sheets and decks carry the same output stage.
Checked by flattening: every sheet gives the same devices on the same nets as before, CMA / CMB apart (their size
follows the layout, 7.96 × 32.16 µm instead of 16 × 16 µm, same area); the sources (`d2s_mpdda_pd.spice`,
`d2s_out.spice`, `sg13cmos5l_IOPadDiff2Single.spice`) match their sheets. Not re-simulated: the results further down
are from 16 × 16 µm capacitors.

**Enable complement (2026-10-25).** `en_3v3_b` is made once, by `XIB` (`inv_hv`) in `en_ctrl_3v3`, and goes to
`bias_sel_pd` (since 2026-10-28 `bias_tree_pd`) and `d2s_mpdda_pd` as a port; their own inverters (`Xi` = `inv_3v3_pd`, `XIP` / `XIN`) are gone.
In `d2s_mpdda_pd.sch` the PMOS switches SA, SABP hang from the top rails with their gates on an `en_3v3` line, the
NMOS switches SB, SABN from the bottom rails on an `en_3v3_b` line, all wired from the pins. The fixture
`d2s_mpdda_pd_sel` has `en_3v3_b` as a pin (its template ties it to 0); `tb_pd_*` (sheets and decks) carry the
inverter that used to sit inside `d2s_mpdda_pd`, on the same vdd / vss. The results further down are from before
this change. Nominal (tt, 27 °C) template runs before / after: dc and loop gain identical; enable settling within
0.5 ns, glitches within 0.1 mV (sel 0 / 1 / 2); power down identical except iovdd 55.8 → 55.5 pA (state 0) and
68.2 → 67.9 pA (state 3), one inverter fewer. The `tb_pd_*` decks reproduce their numbers (enable, unpowered
identical; leak, startup_oa within 5 ppm).

| port | dir | |
|---|---|---|
| iovdd, iovss | ring | front end, bias and output stage; OP / ON are the pad's clamp frames |
| vdd, vss | ring | 1.2 V core ring: only the input inverters of the three `ls_up_1v2_3v3` |
| pad | inout | bond pad: drains of OP / ON, DN / DP, and `vfb` (Kelvin tap at the pad) |
| vinp, vinn, vref | in | differential input and output reference, from the slot |
| ibias | in | harness `ibias0` / `ibias1`: a **sourced** current (iDAC, 250 nA steps, code 20 = 5 µA) |
| en_1v2, sel0_1v2, sel1_1v2 | in | 1.2 V logic: harness `enable` and two `dig_in` bits |
| vdd1v2_sense, vdd3v3_sense | in | the slot's gated supplies, only sensed |

**Bias selection** `sel1 sel0`: 00 harness `ibias` (through a TG), 01 Oguey–Aebischer core, 10 bandgap
core, 11 both cores (currents add: I_Q doubles). The harness sources current, so the `_in` topology
(NMOS input diode) is used; `bias_out_pd` is kept as a reference macro only.

**Power down.** `en_3v3` is low, and every current root is off (power-down switches of
`d2s_mpdda_pd` and the bias, `bias_gen_pd` + `bias_tree_pd`), whenever
- `en_1v2` is low, or
- the slot's `vdd_1v2` is gated off (the presence detector needs no 1.2 V supply, so it also works with
  the `ls_up` latches undefined), or
- the slot's `vdd_3v3` is gated off, or
- the chip's 1.2 V is off altogether.

The ring supply iovdd itself cannot be switched off from the slot; disabled, the cell draws leakage
only (state 0) or the presence detector's ~0.5 µA (states 1, 2).

## Routes

- **Priority: custom padframe cell** replacing the IOPadAnalog of `s7_an[1]`; harness changes listed
  in `../slot/README.md`.
- **Fallback: inside the slot**, `../slot/schematic/xschem/slot.sch`: iovdd = vdd_3v3,
  iovss = vss_3v3, vdd = vdd_1v2, vss = vss_1v2, pad = `s7_an[1]`.

## Running

```sh
make sim-cace                       # all groups (-s schematic), results/<cell>/: summary_<group>.md, <group>.csv, *.png
make sim-cace CACE_GROUPS=pd_params # one group
make spec-table                     # limit, worst case and verdict per quantity, from the yaml and the CSV
cd verification/cace && cace d2s_mpdda_pd_sel.yaml -s schematic   # loop gain (fixture), results in results/d2s_mpdda_pd_sel/
cd testbenches/spice && cp $PDK_ROOT/$PDK/libs.tech/ngspice/.spiceinit . && ngspice -b tb_pad_dc.spice   # plain decks
```

The Makefile arrives as `Makefile.new` (the remote tools may not write a file named `Makefile`): rename it.

## Specification (item 7 of 2026-10-20)

Requirements from the proposal (`sudelbuecher/description/s2d_d2s_pinbuffers.md`): class-AB output
current around 10 mA into 100 pF, low bandwidth (< 1 MHz signal, GBW in the "conservative" 1–5 MHz
tier), low noise, PSRR to be determined. Limits below are **proposals**: the worst case of the
2026-10-20 runs plus margin, tightened where a requirement exists. Conditions per group are in the
yaml; the specified load range is 10 … 300 pF.

| group | quantity | unit | limit | worst | runs | verdict |
|---|---|---|---:|---:|---:|---|
| dc_params | Gain |  | >= 0.49 | 0.4981 | 30 | pass |
| dc_params | Gain |  | <= 0.51 | 0.5 | 30 | pass |
| dc_params | Output offset | mV | >= -5 | 0.03487 | 30 | pass |
| dc_params | Output offset | mV | <= 5 | 1.947 | 30 | pass |
| dc_params | Integral nonlinearity | mV | <= 10 | 7.404 | 30 | pass |
| dc_params | IO ring supply current | uA | <= 400 | 314 | 30 | pass |
| dc_params | Core ring supply current | nA | <= 100 | 23.89 | 30 | pass |
| dc_params | Quiescent current OP | uA | >= 150 | 207.4 | 30 | pass |
| dc_params | Quiescent current OP | uA | <= 300 | 226.6 | 30 | pass |
| dc_params | Quiescent current ON | uA | >= 150 | 207 | 30 | pass |
| dc_params | Quiescent current ON | uA | <= 300 | 226.5 | 30 | pass |
| dc_params | Minimum output-device current | uA | >= 30 | 95.77 | 30 | pass |
| dc_3v0_params | Gain |  | >= 0.49 | 0.498 | 15 | pass |
| dc_3v0_params | Gain |  | <= 0.51 | 0.5002 | 15 | pass |
| dc_3v0_params | Output offset | mV | >= -5 | 0.03434 | 15 | pass |
| dc_3v0_params | Output offset | mV | <= 5 | 1.985 | 15 | pass |
| dc_3v0_params | Integral nonlinearity | mV |  any | 10.92 .. 87.36 | 15 | report |
| dc_3v0_params | IO ring supply current | uA | <= 400 | 298.2 | 15 | pass |
| dc_3v0_params | Core ring supply current | nA | <= 100 | 23.89 | 15 | pass |
| dc_3v0_params | Quiescent current OP | uA | >= 150 | 201.4 | 15 | pass |
| dc_3v0_params | Quiescent current OP | uA | <= 300 | 211.9 | 15 | pass |
| dc_3v0_params | Quiescent current ON | uA | >= 150 | 201.4 | 15 | pass |
| dc_3v0_params | Quiescent current ON | uA | <= 300 | 211.8 | 15 | pass |
| dc_3v0_params | Minimum output-device current | uA | >= 30 | 57.4 | 15 | pass |
| dc_sel_params | Gain |  | >= 0.49 | 0.498 | 9 | pass |
| dc_sel_params | Gain |  | <= 0.51 | 0.5 | 9 | pass |
| dc_sel_params | Output offset | mV | >= -5 | 0.02655 | 9 | pass |
| dc_sel_params | Output offset | mV | <= 5 | 2.706 | 9 | pass |
| dc_sel_params | Integral nonlinearity | mV | <= 10 | 4.094 | 9 | pass |
| dc_sel_params | IO ring supply current | uA | <= 500 | 400.9 | 9 | pass |
| dc_sel_params | Core ring supply current | nA | <= 100 | 7.038 | 9 | pass |
| dc_sel_params | Quiescent current OP | uA | >= 100 | 145.2 | 9 | pass |
| dc_sel_params | Quiescent current OP | uA | <= 350 | 276.3 | 9 | pass |
| dc_sel_params | Quiescent current ON | uA | >= 100 | 145.2 | 9 | pass |
| dc_sel_params | Quiescent current ON | uA | <= 350 | 273.6 | 9 | pass |
| dc_sel_params | Minimum output-device current | uA | >= 30 | 67 | 9 | pass |
| dc_sel3_params | Gain |  |  any | 0.4926 .. 0.5 | 3 | report |
| dc_sel3_params | Output offset | mV |  any | 0.07093 .. 13.55 | 3 | report |
| dc_sel3_params | Integral nonlinearity | mV |  any | 34.65 .. 52.27 | 3 | report |
| dc_sel3_params | IO ring supply current | uA |  any | 491.9 .. 687.3 | 3 | report |
| dc_sel3_params | Core ring supply current | nA |  any | 0.003347 .. 9.245 | 3 | report |
| dc_sel3_params | Quiescent current OP | uA |  any | 335.6 .. 469.8 | 3 | report |
| dc_sel3_params | Quiescent current ON | uA |  any | 335.5 .. 456.3 | 3 | report |
| dc_sel3_params | Minimum output-device current | uA |  any | 172 .. 253.8 | 3 | report |
| dc_ibias_params | Gain |  | >= 0.49 | 0.4999 | 3 | pass |
| dc_ibias_params | Gain |  | <= 0.51 | 0.5 | 3 | pass |
| dc_ibias_params | Output offset | mV |  any | 0.03924 .. 0.08597 | 3 | report |
| dc_ibias_params | Integral nonlinearity | mV |  any | 0.1953 .. 6.19 | 3 | report |
| dc_ibias_params | IO ring supply current | uA |  any | 228.2 .. 368.2 | 3 | report |
| dc_ibias_params | Core ring supply current | nA |  any | 0.1185 .. 0.1185 | 3 | report |
| dc_ibias_params | Quiescent current OP | uA | >= 120 | 163.1 | 3 | pass |
| dc_ibias_params | Quiescent current OP | uA | <= 350 | 260.8 | 3 | pass |
| dc_ibias_params | Quiescent current ON | uA | >= 120 | 163 | 3 | pass |
| dc_ibias_params | Quiescent current ON | uA | <= 350 | 260.7 | 3 | pass |
| dc_ibias_params | Minimum output-device current | uA |  any | 76.7 .. 129.1 | 3 | report |
| ac_params | Closed-loop gain | dB | >= -6.2 | -6.055 | 15 | pass |
| ac_params | Closed-loop gain | dB | <= -5.85 | -6.021 | 15 | pass |
| ac_params | Bandwidth | MHz | >= 1 | 1.778 | 15 | pass |
| ac_params | Gain peaking | dB | <= 1 | 1.532e-06 | 15 | pass |
| ac_params | PSRR iovdd 1 kHz | dB | >= 60 | 70.66 | 15 | pass |
| ac_params | PSRR iovdd 100 kHz | dB | >= 25 | 30.74 | 15 | pass |
| ac_params | CMRR 1 kHz | dB | >= 70 | 93.79 | 15 | pass |
| ac_params | Output impedance 1 kHz | Ω | <= 10 | 3.85 | 15 | pass |
| ac_params | Output impedance 1 MHz | Ω | <= 300 | 206.1 | 15 | pass |
| ac_load_params | Bandwidth | MHz | >= 1 | 1.582 | 6 | pass |
| ac_load_params | Gain peaking | dB | <= 4 | 2.899 | 6 | pass |
| ac_1nF_params | Bandwidth, 1 nF | MHz |  any | 1.336 .. 1.381 | 2 | report |
| ac_1nF_params | Gain peaking, 1 nF | dB |  any | 4.852 .. 7.593 | 2 | report |
| tran_params | Slew rate, rising | V/us | >= 1 | 1.76 | 9 | pass |
| tran_params | Slew rate, falling | V/us | >= 1 | 1.781 | 9 | pass |
| tran_params | Overshoot | % | <= 15 | 9.321 | 9 | pass |
| tran_params | Settling time, rising | us | <= 1 | 0.6892 | 9 | pass |
| tran_params | Settling time, falling | us | <= 1 | 0.6165 | 9 | pass |
| thd_params | THD | dB | <= -35 | -38.87 | 3 | pass |
| thd_params | Output amplitude | V |  any | 0.25 .. 0.7503 | 3 | report |
| noise_params | Output noise 1 kHz | nV/rtHz | <= 1000 | 718.5 | 3 | pass |
| noise_params | Output noise 100 kHz | nV/rtHz | <= 200 | 156.4 | 3 | pass |
| noise_params | Integrated output noise | uV | <= 300 | 235.1 | 3 | pass |
| drive_params | Max output | V | >= 3.0 | 3.266 | 10 | pass |
| drive_params | Min output | V | <= 0.9 | 0.7386 | 10 | pass |
| drive_params | Short-circuit source current | mA | >= 20 | 49.65 | 10 | pass |
| drive_params | Short-circuit sink current | mA | >= 20 | 53.03 | 10 | pass |
| pd_params | IO ring current, off | nA | <= 1000 | 642.2 | 48 | pass |
| pd_params | Core ring current, off | nA | <= 100 | 23.89 | 48 | pass |
| pd_params | Pad leakage, off | nA | >= -100 | -36.83 | 48 | pass |
| pd_params | Pad leakage, off | nA | <= 100 | 9.71 | 48 | pass |
| pd_params | vdd1v2_sense current | nA | <= 2000 | 905.5 | 48 | pass |
| pd_params | vdd3v3_sense current | nA | <= 2000 | 1114 | 48 | pass |
| pd_params | Internal enable | V | <= 0.1 | 7.104e-07 | 48 | pass |
| enable_params | Turn-on time | us | <= 5 | 1.228 | 3 | pass |
| enable_params | Enable glitch, positive | mV | <= 400 | 224.4 | 3 | pass |
| enable_params | Enable glitch, negative | mV | >= -400 | -187.4 | 3 | pass |
| enable_params | IO ring current after start-up | uA | >= 200 | 298.7 | 3 | pass |
| enable_params | IO ring current after start-up | uA | <= 400 | 309.1 | 3 | pass |

Loop gain (fixture `d2s_mpdda_pd_sel`, loop opened at vfb):

| group | quantity | unit | limit | worst | runs | verdict |
|---|---|---|---:|---:|---:|---|
| loop_params | Loop gain | dB | >= 40 | 48.07 | 15 | pass |
| loop_params | Unity-gain frequency | MHz | >= 1 | 1.288 | 15 | pass |
| loop_params | Phase margin | ° | >= 60 | 68.7 | 15 | pass |
| loop_params | Gain margin | dB | >= 15 | 21.49 | 15 | pass |
| loop_load_params | Loop gain | dB |  any | 78.91 .. 104.3 | 6 | report |
| loop_load_params | Unity-gain frequency | MHz | >= 0.8 | 1.204 | 6 | pass |
| loop_load_params | Phase margin | ° | >= 40 | 41.96 | 6 | pass |
| loop_load_params | Gain margin | dB | >= 15 | 19.2 | 6 | pass |
| loop_1nF_params | Loop gain | dB |  any | 78.91 .. 104.3 | 2 | report |
| loop_1nF_params | Unity-gain frequency | MHz |  any | 0.8274 .. 0.8683 | 2 | report |
| loop_1nF_params | Phase margin | ° |  any | 24.1 .. 33.25 | 2 | report |
| loop_1nF_params | Gain margin | dB |  any | 18.97 .. 21.66 | 2 | report |
| loop_sel_params | Loop gain | dB | >= 30 | 37.49 | 8 | pass |
| loop_sel_params | Unity-gain frequency | MHz | >= 1 | 1.189 | 8 | pass |
| loop_sel_params | Phase margin | ° | >= 60 | 69.82 | 8 | pass |
| loop_sel_params | Gain margin | dB | >= 15 | 22.24 | 8 | pass |

### Findings that bear on the specification

1. **Supply headroom.** At iovdd = 3.0 V the INL over vd = ±1 V (pad 1.15 … 2.15 V) is 11–87 mV at
   every corner (44 mV at tt, 27 °C): the input pairs run out of headroom at the top of the range (the
   power-down session saw the same at ss/−40 °C). At 3.3 V the worst case is 7.4 mV, at 3.6 V 0.5 mV.
   INL is therefore specified for iovdd ≥ 3.3 V; `dc_3v0_params` reports it at 3.0 V. Either the
   linear range at 3.0 V is ±0.6 V instead of ±1 V of vd, or the input stage needs more headroom.
2. **Load.** Phase margin 62–72° at 100 pF, 42–55° at 300 pF, 24–33° at 1 nF (peaking up to 7.6 dB):
   the specified load range is 10 … 300 pF; 1 nF is report-only. The proposal's "10 mA into 100 pF"
   is met with margin (short-circuit current ≥ 50 mA source, ≥ 53 mA sink).
3. **PSRR from iovdd** 71 dB at 1 kHz, 31 dB at 100 kHz. With everything on the shared IO ring
   (decision 2026-10-20: ring taps take precedence), switching noise of the digital IO pads couples in
   at that level. bias.md's options still apply: a quiet output-stage rail or cascode (Ahuja)
   compensation.
4. **125 °C loop gain** 48–63 dB at 10 Hz (78–82 dB at 27 °C), inherent to `d2s_mpdda`
   (`results_improvements.txt`: 56.3 dB at tt, 125 °C). Offset stays ≤ 2 mV systematic.
5. **Bias selection.** Harness, Oguey–Aebischer and bandgap give the same I_Q at 27 °C (212 µA); the OA
   core gives 145 µA at −40 °C and 276 µA at 125 °C (I ∝ μT²), still within limits. `sel = 11` (both
   cores) doubles I_Q and is a test mode only: INL 35–52 mV, offset up to 13.5 mV at 125 °C.
6. **Swing at full overdrive** (vd = ±3 V, 1 kΩ to 1.65 V): 3.27 V high but only 0.64–0.74 V low; the
   input common mode (vinp = 0.15 V) is far outside the front end's range there. Not a linear-range
   problem, but the asymmetry is worth knowing.
7. **Power down.** en_3v3 ≤ 1 µV in every off state. iovdd current: ≤ 51 nA with en_1v2 low or the
   chip core off; 0.45–0.64 µA when en_1v2 is high but a slot supply is gone (the presence detector's
   pull-up conducts then); sense inputs draw ≤ 1.1 µA from the slot supplies while the enable is
   requested. Pad leakage ≤ 37 nA (ff, 125 °C).
8. **Enable** settles in 0.8–1.2 µs (OA core: its 24–29 µs start-up is not in this group, which runs
   sel 0–2 at tt); the pad glitches by +112 … +224 / −108 … −187 mV, accepted for now (decision of
   2026-10-06).
9. **Mismatch** (30 Monte Carlo runs, tt): offset −11.4 … +10.1 mV (σ ≈ 5 mV, as in the 2026-10-03
   sizing), gain 0.494–0.508, I_Q 193–233 µA. `cace_to_csv.py` does not follow CACE's collated run
   folders, so `mm_params.csv` is empty; `summary_mm_params.md` has the numbers.

## Cross-checks

- Copied deck `testbenches/spice/tb_pd_leak.spice` and sheet `testbenches/xschem/tb_pd_leak.sch`
  reproduce the power-down reference (0.104 nA total, tt 27 °C).
- Against `improvements/sim/results_improvements.txt` (`d2s_mpdda` with ideal bias): gain 0.4999,
  I_Q 212 µA, loop 78.9 dB / 1.37 MHz / 72.4° at tt (identical), 125 °C loop gain 55.4 / 62.8 dB
  (56.3 / 62.0 at tt / ss), output noise 676 nV/√Hz at 1 kHz, 152 at 100 kHz, 231 µV integrated
  (identical), THD −57.8 dB at vd = 1 V, 10 kHz (0.119 %).
- Bias lines vbp 1.972 V, vbn 0.914 V within 0.7 mV for sel 0 / 1 / 2 at tt (`tb_pad_dc.spice`).
- The top sheet netlists to the five instance lines of `netlist/source/sg13cmos5l_IOPadDiff2Single.spice`
  in port order; the sub-sheets were checked device by device in their own macros.

## Results

`verification/cace/results/sg13cmos5l_IOPadDiff2Single/` and `.../results/d2s_mpdda_pd_sel/`:
`summary_<group>.md` (CACE's table per group), `<group>.csv` (every run, SI units). Run 2026-10-20 in the
cloud with the IIC-OSIC-TOOLS 2026.09 pins (sudelbuecher/cloud_environment.md), CACE 2.13.0,
schematic netlist. The plots are not shipped; `make sim-cace` regenerates them.

## Not done

- Layout: `layout/klayout/sg13cmos5l_IOPadDiff2Single.klay.gds` stands on the `SG13_cm_clamps` PCells since 2026-10-28
  (open it with `klayout -e -rm scripts/pcells/load_clamp_pcells.py ...` to keep them live): `Clamp_P_M1` ng 43 / 0.6u and
  2 x `Clamp_N_M1` ng 35 / 1u, all `wiring = external`, with their wiring cells (P roles `20:dummy 21:rep`, nets `a` /
  `dabp`; upper N `16:rep 17:rep`, `b` / `dabn`; lower N no roles, `b`), `DCNDiode` 67.6u and `DCPDiode` 65.8u centred.
  Devices: OP 546.12 / 0.6, RP1 and the dummy 13.32 / 0.6, ON 299.2 / 1, RN1 8.8 / 1. Since 2026-10-28 01:39 also the
  Metal2 comb (option B: pad lines on the drains, straps with Via2 into their own rails, pad junction in the gap), the
  gate-bus feeds (a / b joined above the P frame), dabp / dabn to pins at y 85–86, CMA / CMB (W 7.96 × L 32.16 µm,
  between the diodes) and the narrowed band above DCNDiode. Checked with a flat extraction and a Python subset of the
  deck (report: `_sudelbuecher/.../sg13cmos5l_IOPadDiff2Single_build/m2_option_b_2026-10-28/`); not with IHP's own
  DRC / LVS. Open: RP2 / RN2 placement, the `guard` net tie, the joins boxing in dabp / dabn. Before-states:
  `layout/klayout/backups/*_before_pcells_2026-10-28*`, `*_before_m2_2026-10-28*`.
- LVS, PEX, post-layout CACE; ESD and latch-up simulation; the unpowered-pad case of
  `testbenches/spice/tb_pd_unpowered.spice` is not in CACE.
- The S2D counterpart `../sg13cmos5l_IOPadSingle2Diff` has its input buffer since 2026-10-25; it proposes vcm = 1.2 V for both
  buffers (`s2d_input_buffer.md` section IV), and this suite still runs at vref = vicm = 1.65 V.
