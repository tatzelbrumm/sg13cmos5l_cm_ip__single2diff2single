<!--
SPDX-FileCopyrightText: 2026 Christoph Maier
SPDX-License-Identifier: Apache-2.0
-->
# `sg13cmos5l_IOPadSingle2Diff` — single-ended-in, differential-out buffered input pad

`outp − outn = 2 (pad − vref)`, `(outp + outn)/2 = vcm`, i.e. `outp − vcm = vcm − outn = pad − vref`.
The counterpart of `../sg13cmos5l_IOPadDiff2Single`, scaffolded 2026-10-20 on the same structure. On
2026-10-25 the placeholder amplifier was replaced by the input buffer of the `_sudelbuecher` worktree,
`design_considerations/s2d_input_buffer` (`s2d_input_buffer.md`, `log.md`, `sim/results_s2d.txt`):
the matched-pair DDA `s2d_mpdda`, the mirror image of the driver's `d2s_mpdda`, built from the same
unit `unit_r2`. Open points are in [`FILL_IN.md`](FILL_IN.md).

## Structure

| instance | cell (macro) | function |
|---|---|---|
| `xc` | `en_ctrl_3v3` (`../en_ctrl_3v3`) | `en_3v3 = en_1v2 ∧ vdd_1v2 present ∧ vdd_3v3 present`; level-shifted `sel*`; `en_3v3_b` for `xt` and `xa` |
| `xg` | `bias_gen_pd` (`../bias_gen_pd`) | the reference current `iref` (sourced), selected by `sel1 sel0` |
| `xt` | `bias_tree_noab_pd` (`../bias_tree_noab_pd`) | four bias lines vbp vbn vbpc vbnc from one mirror tree fed by `iref`. `xg` + `xt` replace `xb` = `bias_sel_noab_pd` (2026-10-27 to 2026-10-28; before that `bias_sel_pd`, whose class-AB legs stayed unused here), device for device |
| `xa` | `s2d_mpdda_pd` (here) | `s2d_mpdda` + four output-to-vcm ties; `vfbp` / `vfbn` tied to `outp` / `outn` on the top sheet |
| `CP`, `CN`, `DN`, `DP`, `SP` | IHP IO sub-cells | input protection exactly as `sg13cmos5l_IOPadAnalog`: gate-tied clamps, primary diodes, secondary protection (587 Ω rppd) from `pad` to `padres` |

`s2d_mpdda` (four signal units A1 = A2 on (vin, vref), F1 on (vcm, vfbp), F2 on (vfbn, vcm); one
folded cascode with the outputs as the only high-impedance nodes; two more units as the CMFB into a
cascoded PMOS diode that the loads mirror 1 : 1; two 12 × 12 µm hv NMOS capacitors as built-in load).
The gain is set by how the matched units are connected, not by a resistor ratio: for any matched,
odd, monotonic unit function the balance gives `voutp − voutn = 2 (vin − vref)`.

Sheets in `schematic/xschem/`:

| file | contents |
|---|---|
| `sg13cmos5l_IOPadSingle2Diff.{sch,sym}` | top sheet; symbol and port order unchanged since 2026-10-20 |
| `s2d_mpdda.{sch,sym}` | Christoph's sheet of 2026-10-23 from `s2d_input_buffer/xschem` (only the netlist-path text changed) |
| `s2d_mpdda_pd.{sch,sym}` | wrapper: `s2d_mpdda` + TPN / TPP, TNN / TNP (1 / 0.45 µm hv TGs, outputs to vcm while disabled) |
| `s2d_mpdda_pd_sel.{sch,sym}` | CACE-only fixture: `s2d_mpdda_pd` + `bias_gen_pd` + `bias_tree_noab_pd` (until 2026-10-28 `bias_sel_noab_pd`), `vfbp` / `vfbn` as pins (loop gain) |
| `s2d_core_ideal.{sch,sym}` | the 2026-10-20 placeholder (two E sources), no longer used |
| `xschemrc` | PDK + this folder + the sub-macros; `sg13cmos5l_IOPadDiff2Single` added for `unit_r2` |

`unit_r2` is not copied: the sheets use `../sg13cmos5l_IOPadDiff2Single/schematic/xschem/unit_r2.sym`,
the netlists and decks `../sg13cmos5l_IOPadDiff2Single/netlist/source/units.spice` (as the design did
with the driver's `improvements` folder).

Source netlists in `netlist/source/`:

| file | contents |
|---|---|
| `sg13cmos5l_IOPadSingle2Diff.spice` | the top cell (instance lines identical to the sheet's xschem netlist) |
| `s2d_mpdda.spice`, `s2d_bias.spice` | copied unchanged from `s2d_input_buffer/sim` (`s2d_bias.spice`: `s2d_bias_lp` fixture, `s2d_bias_in` / `_out` trees, `bias_fanout_n` / `_p`) |
| `s2d_pd.spice` | `s2d_input_buffer/sim/s2d_pd.spice` with `en_3v3_b` as a port of `s2d_mpdda_pd` (its inverter `Xi` removed); `s2d_bias_out_pd`, `s2d_bias_in_pd`, `inv_3v3_s2d` kept for the decks |

Decks in `testbenches/spice/`: the eight of `s2d_input_buffer/sim/tb` (`tb_s2d_{op,dc,loop,step,noise,loopback,pd_leak,pd_enable}`,
includes rewritten; the two `pd` decks make `en_3v3_b` with the design's inverter at the top level) and
`tb_pad_dc.spice` (the whole pad, operating point per bias selection).

## Ports

| port | dir | |
|---|---|---|
| iovdd, iovss | ring | buffer, bias, control and protection |
| vdd, vss | ring | 1.2 V core ring: only the input inverters of the three `ls_up_1v2_3v3` |
| pad | inout | bond pad; the buffer input is `padres`, behind the secondary protection |
| outp, outn | out | differential output to the next internal stage |
| vcm | in | internal common mode (gates of the feedback and CMFB units only) |
| vref | in | pad reference (gates of the input units only) |
| ibias | in | harness `ibias0` / `ibias1`: a **sourced** current (iDAC, 250 nA steps, code 20 = 5 µA) |
| en_1v2, sel0_1v2, sel1_1v2 | in | 1.2 V logic: harness `enable` and two `dig_in` bits |
| vdd1v2_sense, vdd3v3_sense | in | the slot's gated supplies, only sensed |

Bias selection and power down as in `../sg13cmos5l_IOPadDiff2Single/README.md`. Disabled, the bias tree
is off (every tail, sink, cascode and the CMFB diode with it), and `outp`, `outn` are tied to `vcm`.
`pad`, `vref` and `vcm` see gates only, enabled or not.

## Changes against the scaffold (where the design and the 2026-10-20 scaffold disagreed)

- `xa`'s ports: the scaffold had `vdd vss padres vref vcm outp outn vbp vbn vbpc vbnc vabp vabn en_3v3`;
  `s2d_mpdda_pd` has `vdd vss vin vref vcm voutp voutn vfbp vfbn vbp vbn vbpc vbnc en_3v3 en_3v3_b`.
  The symbol keeps the placeholder's pin positions, so the top-sheet wiring stayed; new are the
  `vfbp` / `vfbn` ties next to the outputs and the `en_3v3_b` wire from `xc`. The class-AB lines of
  `xb` end in labelled stubs.
- `en_3v3_b`: the design's `s2d_mpdda_pd` made it with its own inverter; here it comes from `xc`, as for
  `d2s_mpdda_pd` and `bias_sel_pd` since 2026-10-25.
- Bias: the design proposes a shared root with one 5 µA fan-out leg per buffer into its own small tree
  (`s2d_bias_out` / `_in`, four lines). The pads keep their `bias_sel_pd` (same four diodes at the
  same currents, plus the unused class-AB legs); see `FILL_IN.md`. Since 2026-10-27 the s2d pad has
  `bias_sel_noab_pd`, without those legs (10 uA less from iovdd; the CACE results here are older).
- Input range: the scaffold asked for rail-to-rail inputs including iovss; the design has a signal
  window instead (unit gates ≤ about iovdd − 1.3 V). With vref = 0.5 V the pad range is 0 … 1 V and
  includes iovss (`window_params`). vref and vcm default to 1.2 V (scaffold: 1.65 V).
- Load: 0.5 pF per output (scaffold: 1 pF stand-in).
- CACE: the scaffold's four groups (dc, range, ac, pd; limits `any`, ideal E sources) are replaced
  by the design's suite moved to the pad level (dc, range, dc_ibias for the design's dc_bias, ac,
  ac_mm, tran, noise, mm, mc), the pad-level groups window, dc_sel, dc_sel3, pd, enable, and the loop
  fixture. The scaffold's range template became `window_params` (pad swept 0 … iovdd, |gain − 2| < 1 %).

## Running

```sh
make sim-cace                       # all 14 groups (-s schematic), results/<cell>/: summary_<group>.md, <group>.csv, *.png
make sim-cace CACE_GROUPS=pd_params # one group
make spec-table                     # limit, worst case and verdict per quantity, from the yaml and the CSV
cd verification/cace && cace s2d_mpdda_pd_sel.yaml -s schematic   # loop gain (fixture), results in results/s2d_mpdda_pd_sel/
cd testbenches/spice && cp $PDK_ROOT/$PDK/libs.tech/ngspice/.spiceinit . && ngspice -b tb_s2d_dc.spice   # plain decks
```

## Specification

Limits are **proposals** (the requirements are in `sudelbuecher/description/s2d_d2s_pinbuffers.md`): the buffer's are those of `s2d_input_buffer.md` section VII, the pad-level ones (IO ring
current, pad range, power down, enable time) the worst case of the first full run plus margin. Run
2026-10-25/26 in the cloud with the IIC-OSIC-TOOLS 2026.09 pins (`sudelbuecher/cloud_environment.md`),
CACE 2.13.0, schematic netlist, 574 + 60 runs; all 65 results pass. Conditions per group are in the yaml;
defaults iovdd 3.3 V, vref = vcm = 1.2 V, 0.5 pF per output, rsrc 50 Ω, sel 00, harness ibias 5 µA.
The plots are not shipped; `make sim-cace` regenerates them.

| group | quantity | unit | limit | worst | runs | verdict |
|---|---|---|---:|---:|---:|---|
| dc_params | Gain |  | >= 1.99 | 1.998 | 135 | pass |
| dc_params | Gain |  | <= 2.01 | 1.999 | 135 | pass |
| dc_params | Input offset (systematic) | mV | >= -1 | -0.0004476 | 135 | pass |
| dc_params | Input offset (systematic) | mV | <= 1 | 0.0001623 | 135 | pass |
| dc_params | Integral nonlinearity | mV | <= 2 | 1.06 | 135 | pass |
| dc_params | Output common-mode error | mV | >= -30 | 4.974 | 135 | pass |
| dc_params | Output common-mode error | mV | <= 30 | 17.97 | 135 | pass |
| dc_params | IO ring current | uA | <= 135 | 127 | 135 | pass |
| range_params | Gain vs vref and vcm |  |  any | 1.95 .. 2.037 | 96 | report |
| range_params | Integral nonlinearity vs vref and vcm | mV |  any | 0.1869 .. 170.5 | 96 | report |
| range_params | Output common-mode error vs vref and vcm | mV |  any | 3.302 .. 15.37 | 96 | report |
| window_params | Input range, low end | V | <= 0.1 | 0.08697 | 27 | pass |
| window_params | Input range, high end | V | >= 1.0 | 1.059 | 27 | pass |
| dc_sel_params | Gain vs bias select |  | >= 1.99 | 1.999 | 45 | pass |
| dc_sel_params | Gain vs bias select |  | <= 2.01 | 1.999 | 45 | pass |
| dc_sel_params | Input offset (systematic) vs bias select | mV | >= -1 | -0.0003887 | 45 | pass |
| dc_sel_params | Input offset (systematic) vs bias select | mV | <= 1 | 8.147e-05 | 45 | pass |
| dc_sel_params | Integral nonlinearity vs bias select | mV | <= 2 | 0.4358 | 45 | pass |
| dc_sel_params | Output common-mode error vs bias select | mV | >= -30 | 6.35 | 45 | pass |
| dc_sel_params | Output common-mode error vs bias select | mV | <= 30 | 14.07 | 45 | pass |
| dc_sel_params | IO ring current vs bias select | uA | <= 220 | 187.9 | 45 | pass |
| dc_sel3_params | Gain, sel 11 |  |  any | 1.998 .. 1.999 | 15 | report |
| dc_sel3_params | Input offset (systematic), sel 11 | mV |  any | -0.0003887 .. 8.148e-05 | 15 | report |
| dc_sel3_params | Integral nonlinearity, sel 11 | mV |  any | 0.4044 .. 6.768 | 15 | report |
| dc_sel3_params | Output common-mode error, sel 11 | mV |  any | 6.616 .. 16.34 | 15 | report |
| dc_sel3_params | IO ring current, sel 11 | uA |  any | 214.2 .. 320 | 15 | report |
| dc_ibias_params | Gain vs ibias |  | >= 1.99 | 1.999 | 15 | pass |
| dc_ibias_params | Gain vs ibias |  | <= 2.01 | 1.999 | 15 | pass |
| dc_ibias_params | Input offset (systematic) vs ibias | mV | >= -1 | -6.618e-05 | 15 | pass |
| dc_ibias_params | Input offset (systematic) vs ibias | mV | <= 1 | -6.364e-05 | 15 | pass |
| dc_ibias_params | Integral nonlinearity vs ibias | mV |  any | 0.04071 .. 0.3496 | 15 | report |
| dc_ibias_params | Output common-mode error vs ibias | mV | >= -30 | 8.625 | 15 | pass |
| dc_ibias_params | Output common-mode error vs ibias | mV | <= 30 | 11.62 | 15 | pass |
| dc_ibias_params | IO ring current vs ibias | uA |  any | 75.79 .. 175.6 | 15 | report |
| ac_params | Closed-loop gain at 1 kHz | dB |  any | 6.015 .. 6.017 | 15 | report |
| ac_params | Closed-loop -3 dB bandwidth | MHz | >= 1 | 1.359 | 15 | pass |
| ac_params | Output common-mode response to iovdd at 1 kHz | dB | <= -30 | -53.9 | 15 | pass |
| tran_params | Rise time 10-90 % | ns |  any | 103.7 .. 257.9 | 18 | report |
| tran_params | Settling time to 1 % | ns | <= 1000 | 543.4 | 18 | pass |
| tran_params | Overshoot | % | <= 5 | 0.001001 | 18 | pass |
| tran_params | Largest output common-mode deviation during the step | mV | <= 50 | 15.51 | 18 | pass |
| noise_params | Input noise density at 1 kHz | nV/rtHz | <= 1000 | 722.6 | 15 | pass |
| noise_params | Input noise density at 100 kHz | nV/rtHz | <= 250 | 156.3 | 15 | pass |
| noise_params | Differential output noise, 10 Hz - 10 MHz | uV | <= 1000 | 439.4 | 15 | pass |
| pd_params | IO ring current, off | nA | <= 1000 | 597.1 | 24 | pass |
| pd_params | Core ring current, off | nA | <= 100 | 4.831 | 24 | pass |
| pd_params | Pad input leakage, off | nA | >= -100 | -7.64 | 24 | pass |
| pd_params | Pad input leakage, off | nA | <= 100 | 8.416 | 24 | pass |
| pd_params | Internal enable | V | <= 0.1 | 3.602e-07 | 24 | pass |
| pd_params | Differential output, off | mV | >= -1 | -0.0006531 | 24 | pass |
| pd_params | Differential output, off | mV | <= 1 | 1.11e-05 | 24 | pass |
| pd_params | Output common mode, off | mV | >= -1 | -1.055e-06 | 24 | pass |
| pd_params | Output common mode, off | mV | <= 1 | 0.0004664 | 24 | pass |
| enable_params | Enable time | us | <= 3 | 1.305 | 9 | pass |
| enable_params | Output CM glitch, high | V |  any | 0.2097 .. 0.2695 | 9 | report |
| enable_params | Output CM glitch, low | V |  any | -0.01744 .. -0.003461 | 9 | report |
| enable_params | Differential output at the end | V |  any | 0.4998 .. 0.4998 | 9 | report |
| enable_params | IO ring current, enabled | uA |  any | 125.3 .. 126.2 | 9 | report |

Loop gain, fixture `s2d_mpdda_pd_sel` (loops broken at vfbp / vfbn; cload 0.001 / 0.5 / 2 / 10 pF × MOS × temperature):

| group | quantity | unit | limit | worst | runs | verdict |
|---|---|---|---:|---:|---:|---|
| loop_params | DC loop gain, differential | dB | >= 60 | 64.54 | 60 | pass |
| loop_params | Crossover, differential | MHz |  any | 0.1461 .. 3.262 | 60 | report |
| loop_params | Phase margin, differential | ° | >= 60 | 86.08 | 60 | pass |
| loop_params | Gain margin, differential | dB | >= 10 | 29.41 | 60 | pass |
| loop_params | DC loop gain, common mode | dB | >= 50 | 64.73 | 60 | pass |
| loop_params | Crossover, common mode | MHz |  any | 0.1467 .. 3.131 | 60 | report |
| loop_params | Phase margin, common mode | ° | >= 55 | 62.06 | 60 | pass |
| loop_params | Gain margin, common mode | dB | >= 10 | 14.45 | 60 | pass |

Mismatch and process Monte Carlo (collated groups; `cace_to_csv.py` cannot read them, so their CSV files
are empty and the numbers come from the runs' data files; σ over the seeds):

| group | runs | input offset | gain | output CM error |
|---|---:|---|---|---|
| mm_params (tt_mismatch, rhigh typ_mismatch) | 100 | σ 6.19 mV, −17.3 … +18.2 mV (limit ±20) | σ 0.74 %, 1.959 … 2.038 (1.93 … 2.07) | mean 10.8 mV, σ 12.2 mV, −19.0 … +39.9 mV (±60) |
| mc_params (tt_stat, rhigh typ) | 30 | < 0.001 mV (±5) | 1.99895 … 1.99898 (1.99 … 2.01) | 10.1 … 10.9 mV (±30) |
| ac_mm_params (mismatch) | 30 | PSRR iovdd 1 kHz ≥ 79.1 dB (≥ 60), 100 kHz ≥ 77.3 dB | PSRR iovss 1 kHz ≥ 83.3 dB (≥ 60), 100 kHz ≥ 63.8 dB | CMRR 1 kHz ≥ 87.7 dB (≥ 70) |

Against the design's own CACE run (`s2d_input_buffer/verification/cace/first_run_summary.md`: `s2d_mpdda` with
the ideal bias fixture `s2d_bias_lp`, no pad cell): gain, loop gain, bandwidth and step response agree to within a
few tenths of a percent, INL within 3 % (worst 1.060 against 1.037 mV), noise within 1 % (rsrc and the pad cell);
the output CM error is lower
(5.0 … 18.0 mV against 6.2 … 21.1 mV); PSRR iovdd at 1 kHz is lower (worst 79.1 against 86.2 dB, real tree
instead of ideal references); the supply current is 125.6 µA at tt instead of 112.7 µA (the d2s tree with its
class-AB legs and the enable control, against the fixture's diodes).

Observations:

- **Pad range** (vref = 0.5 V, linear to 1 mV): from 0 V at −40 / 27 °C and 0.013 … 0.087 V at 125 °C (the
  input devices' drains come close to their sources there, `s2d_input_buffer.md` section IV) up to
  1.06 … 1.30 V. At vref = vcm = 1.2 V the nominal (tt, 27 °C, 3.3 V) range is 0.48 … 1.94 V by the same criterion.
- **Enable**: vd within 1 mV after 1.27 … 1.31 µs; the output common mode rises by +0.21 … +0.27 V and
  dips by at most −17 mV while enabling. The design's decks, with the `s2d_bias_out_pd` tree and a 10 ns edge
  on `en_3v3` directly, show −1.62 / +1.09 V (`tb_s2d_pd_enable.spice` reproduces that); here the edge comes
  through `en_ctrl_3v3` and the bias is `bias_sel_pd`. The difference is not analysed.
- **Power down**: iovdd 0.05 … 16 nA in states 0 and 3; 0.45 … 0.60 µA in states 1 and 2 (the presence
  detector, as in the output pad); pad leakage −7.6 … +8.4 nA (125 °C, 0 … 3.3 V); outputs at vcm within
  0.7 µV.
- **Bias select 11** (both cores, test mode): INL up to 6.8 mV, iovdd 214 … 320 µA.

## Not done

- Layout, LVS, PEX, post-layout CACE; ESD and latch-up simulation; the unpowered pad.
- The open points of `FILL_IN.md`.
- `testbenches/xschem/simulations/sg13cmos5l_IOPadSingle2Diff.spice` is the netlist generated on 2026-10-20
  (with the placeholder); it is regenerated when the top sheet is netlisted in xschem.
