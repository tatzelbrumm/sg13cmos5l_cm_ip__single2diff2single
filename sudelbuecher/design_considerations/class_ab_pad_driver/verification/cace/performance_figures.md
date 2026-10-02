# d2s_miller: performance figures in the CACE characterization (draft)

DUT `d2s_miller_biased` (= `d2s_miller` + `d2s_bias` fixture). Default conditions: VDD 3.3 V,
vref = vicm = 1.65 V, 1 kΩ to 1.65 V ∥ 100 pF, tt / typ, 27 °C, ideal bias.

The **First run** column comes from the container (ngspice 42, IHP-Open-PDK dev branch). It
shows the tt/27 °C value where one was checked, otherwise the range over the group's
conditions. The **Spec** column holds proposals.

## Simulated

| # | Figure | Symbol (yaml) | Definition / method | Swept over (group) | Spec (proposal) | First run |
|---|---|---|---|---|---|---|
| 1 | Gain | Gain | (vout(+0.2) − vout(−0.2)) / 0.4 V, vd = vinp − vinn | PVT + R corner (dc), bias quality (dc_bias), load (dc_load), mismatch/process MC | 0.485 … 0.515 | 0.5013; PVT + R corners 0.476…0.554; process MC 0.41…0.61 |
| 2 | Output offset | Vos_out | vout − vref at vd = 0 | as 1 | ±5 mV systematic, ±10 mV MC | 0.19 mV; mismatch −32…+49 mV |
| 3 | Integral nonlinearity | INL | max deviation from the small-signal line, vd = ±1 V | as 1 | ≤ 10 mV | 5.5 mV; worst PVT/R corner 469 mV |
| 4 | Supply current | Idd | vdd current at vd = 0, incl. load, excl. fixture | dc, dc_bias | ≤ 600 µA | 426 µA; +40 % bias: 650 µA |
| 5 | Output quiescent current P / N | IqP, IqN | XOP / XON drain current at vd = 0 | dc, dc_bias, MC | 100 … 500 µA | 239 / 238 µA |
| 6 | Minimum output-device current | Imin | smaller of XOP/XON currents at vd = ±1 V (class AB, no cut-off) | dc, dc_bias, dc_load | ≥ 20 µA | 120 µA; worst 13.6 µA |
| 7 | DC loop gain | T0 | T = −v(vout)/v(fb) at 10 Hz, loop broken at the vfb gate | PVT (loop) | ≥ 40 dB | 66.5 dB |
| 8 | Crossover frequency | fc | \|T\| = 0 dB | loop, cload/rload (loop_load), bias/MOM corner (loop_bias) | ≥ 1 MHz | 1.62 MHz |
| 9 | Phase margin | PM | 180° + ∠T at fc | as 8 | ≥ 45° | 74.8°; 1 nF: 26.5° |
| 10 | Gain margin | GM | −\|T\| where ∠T = −180° | loop | ≥ 10 dB | 31 dB |
| 11 | Closed-loop gain | Acl_dB | at 1 kHz | ac (MOS corners) | −6.02 dB | −6.01 dB |
| 12 | Closed-loop bandwidth | f3dB | −3 dB from Acl | ac | ≥ 1 MHz | 2.23 MHz |
| 13 | PSRR (output-referred) | PSRR_1k, PSRR_100k | −20 log\|vout/vdd\| | ac | ≥ 40 dB at 1 kHz | 72.5 / 32.5 dB |
| 14 | CMRR | CMRR_1k | A_dm / A_cm, AC on vicm | ac | ≥ 50 dB | 100 dB |
| 15 | Output impedance, closed loop | Zout_1k, Zout_1M | 1 A AC into vout | ac | ≤ 1 Ω at 1 kHz | 0.48 Ω / 131 Ω |
| 16 | Slew rate rise / fall | SR_rise, SR_fall | 10–90 % of the step | vstep 0.5 / 2 V × MOS corners (tran) | ≥ 1 V/µs | 2.65 V/µs (rise, tt) |
| 17 | Overshoot | Overshoot | peak above final value | tran | ≤ 10 % | ≈ 0 % |
| 18 | Settling time to 1 % | ts_rise, ts_fall | last exit from the ±1 % band | tran | ≤ 1 µs | 306 ns (0.5 V step) |
| 19 | THD | THD | h2…h7 root-sum-square, 4 periods × 1024 points | fin 1 k/10 k/100 k × vd amplitude 1/2 V (thd) | ≤ −40 dB | −51 dB (10 kHz, 0.5 V out); −15 dB at 1.25 V out |
| 20 | Output noise density | En_1k, En_100k | onoise at the spot frequency | noise (ss/tt/ff) | — | 1.6 µV/√Hz / 200 nV/√Hz |
| 21 | Integrated output noise | Vn_int | 10 Hz … 10 MHz | noise | — | 278 µV rms |
| 22 | Output swing into load | Vout_max, Vout_min | vd = ±3 V (overdriven) | rload 50 Ω / 1 k / open × corners (drive) | ≥ 2.8 V / ≤ 0.5 V | 2.86…3.30 V / 0.35…0.39 V |
| 23 | Short-circuit current | Isc_src, Isc_snk | vout held at 1.65 V through 1 mΩ, full overdrive | drive | ≥ 5 mA | 60…80 mA / 74…92 mA |

Bias-source quality (conditions, not figures):

- `ibias_err`: a common error on all six reference currents, swept ±40 %.
- `va_bias`: an "Early voltage" of the reference sources, R_k = va_bias / I_k, swept 10 V,
  100 V and ideal.

## Candidates, not yet simulated (add / strike)

| Figure | How |
|---|---|
| Input common-mode range | sweep vicm, track Gain / Vos_out (condition exists, not swept yet) |
| Output reference range | sweep vref, track Gain / INL / Imin |
| Offset drift | dVos_out/dT from the dc temperature sweep (µV/K) |
| Input-referred noise | En / Gain |
| Max. load capacitance | cload where PM = 45° (loop_load, finer cload grid) |
| Max. output swing at THD = −40 dB | sweep the THD amplitude |
| Overload recovery | vd overdriven beyond the swing, time back into the 1 % band |
| 0.1 % settling, large-step settling with 1 nF | tran, tighter band / heavier load |
| PSRR from vss, PSRR vs frequency curve | ac with AC on vss / plot |
| Open-loop output impedance | ac with the loop broken |
| Pad-level items (later, in sg13cmos5l_IOPadDiff2Single) | bondwire L + pad C in the load, ESD clamp leakage, power-up / enable behaviour |
