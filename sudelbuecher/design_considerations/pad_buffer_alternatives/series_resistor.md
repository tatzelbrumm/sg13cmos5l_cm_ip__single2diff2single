<!--
SPDX-FileCopyrightText: 2026 Christoph Maier
SPDX-License-Identifier: Apache-2.0
-->
# What a Series Pad Resistor R_s Buys the Class-AB Driver

*Simulation note, 26 October 2026. `d2s_mpdda` as in `../class_ab_pad_driver/improvements/sim/`
(netlists unchanged), ngspice-47 with the pinned cloud toolchain of `../../cloud_environment.md`,
tt 27 °C. Decks: `sim/tb_rs_loop.tpl`, `sim/tb_rs_step.tpl` (the project's loop and step decks with
`Rs vout_a vout` inserted and the feedback node as a placeholder); all numbers: `sim/loop_results.txt`,
`sim/step_results.txt`. Running log: `log.md`.*

**Definitions.** R_s is *series* resistance inside the pad cell, between the clamp-frame drains
(node `vout_a`) and the pad (`vout`): ours. R_L is the *load* the bench hangs on the pad: theirs.
The feedback of the DDA can be taken before R_s (at `vout_a`, "out-of-loop R_s") or at the pad
("in-loop R_s"). The R_s = 0 rows reproduce `results_improvements.txt` exactly (loop and step).

## 1. Loop gain, feedback before R_s

T0 / f_c / PM; the load is on the pad, the loop sees R_s + load.

| load | R_s = 0 | 50 Ω | 200 Ω | 500 Ω |
|---|---|---|---|---|
| 50 Ω ‖ 20 pF | 53.1 dB / 0.23 MHz / 89° | 59.1 / 0.42 / 89° | 67.1 / 0.78 / 87° | 73.8 / 1.15 / 86° |
| 1 kΩ ‖ 100 pF | 78.9 / 1.37 / 72° | 79.3 / 1.38 / 73° | 80.4 / 1.41 / 76° | 82.3 / 1.48 / 79° |
| 20 pF | 104.3 / 1.90 / 78° | 104.3 / 1.89 / 78° | 104.3 / 1.89 / 79° | 104.3 / 1.88 / 79° |
| 100 pF | 104.3 / 1.77 / 62° | 104.3 / 1.74 / 63° | 104.3 / 1.68 / 66° | 104.3 / 1.61 / 70° |
| 1 nF | 104.3 / 0.87 / **24°** | 104.3 / 0.83 / **37°** | 104.3 / 0.88 / **63°** | 104.3 / 1.14 / **80°** |

## 2. Loop gain, feedback at the pad

| load | R_s = 0 | 50 Ω | 200 Ω | 500 Ω |
|---|---|---|---|---|
| 50 Ω ‖ 20 pF | 53.1 / 0.23 / 89° | 53.1 / 0.21 / 89° | 53.1 / 0.16 / 90° | 53.0 / 0.11 / 90° |
| 1 kΩ ‖ 100 pF | 78.9 / 1.37 / 72° | 78.9 / 1.31 / 72° | 78.8 / 1.18 / 71° | 78.8 / 0.99 / 71° |
| 20 pF | 104.3 / 1.90 / 78° | 104.3 / 1.89 / 78° | 104.3 / 1.89 / 76° | 104.3 / 1.87 / 72° |
| 100 pF | 104.3 / 1.77 / 62° | 104.3 / 1.74 / 60° | 104.3 / 1.65 / 54° | 104.3 / 1.49 / 46° |
| 1 nF | 104.3 / 0.87 / 24° | 104.3 / 0.82 / 23° | 104.3 / 0.71 / 19° | 104.3 / 0.58 / 16° |

Worse in every cell: R_s C_L adds a pole inside the loop and the zero it also creates sits at
`vout_a`, outside the feedback path. In-loop R_s is out.

## 3. Step at the pad, feedback before R_s (v_d −0.5 → +0.5 V)

| load | R_s | pad gain | overshoot | 10–90 % rate | 1 % settling |
|---|---|---|---|---|---|
| 50 Ω ‖ 20 pF | 0 / 50 / 200 / 500 | 0.500 / **0.250** / 0.100 / 0.045 | 0 / 0 / 0 / 0 % | 0.74 / 0.47 / 0.24 / 0.14 V/µs | 943 / 769 / 619 / 531 ns |
| 1 kΩ ‖ 100 pF | 0 / 50 / 200 / 500 | 0.500 / **0.476** / 0.417 / 0.333 | 0 / 0 / 0 / 0 | 2.44 / 2.25 / 1.81 / 1.30 | 327 / 335 / 357 / 397 |
| 20 pF | 0 / 50 / 200 / 500 | 0.500 all | 0 all | 2.83 / 2.83 / 2.80 / 2.73 | 309 / 309 / 311 / 315 |
| 100 pF | 0 / 50 / 200 / 500 | 0.500 all | 4.7 / 4.7 / 4.2 / 2.5 % | 3.67 / 3.43 / 2.86 / 2.14 | 361 / 383 / 445 / 545 |
| 1 nF | 0 / 50 / 200 / 500 | 0.500 all | **32.9 / 18.6 / 3.4 / 0** % | 3.14 / 2.11 / 0.95 / 0.39 | 2687 / 1929 / **1333** / 2135 |

## 4. A real line: 50 Ω, 1 m (5 ns) and 2 m (10 ns), far end open (1 MΩ ‖ 15 pF) or 50 Ω

| R_s | line, far end | pad gain | far-end gain | overshoot | 1 % settling | loop |
|---|---|---|---|---|---|---|
| 0 | 1 m, open | 0.500 | 0.500 | 6.3 % | 377 ns | 104 dB / 1.73 MHz / 60° |
| 50 Ω | 1 m, open | 0.500 | 0.500 | 6.1 % | 401 ns | 104 dB / 1.70 MHz / 61° |
| 0 | 2 m, open | 0.500 | 0.500 | 14.0 % | 679 ns | — |
| 50 Ω | 2 m, open | 0.500 | 0.500 | 12.3 % | 724 ns | — |
| 0 | 1 m, 50 Ω | 0.500 | 0.500 | 0 | 945 ns | 53 dB / 0.23 MHz / 89° |
| 50 Ω | 1 m, 50 Ω | 0.250 | 0.250 | 0 | 770 ns | 59 dB / 0.42 MHz / 89° |

The lines behave as their lumped capacitance (100 pF/m): the 10–90 % rise of the driver is about
170 ns against a 10–20 ns round trip, so a line is lumped below roughly 5 m, and R_s = 50 Ω
terminates nothing at this speed (overshoot 6.3 → 6.1 %). The terminated line is the 50 Ω load case.

## 5. What R_s buys, and what it costs

Mechanism. The output node of a Miller-compensated two-stage amplifier looks like 1/(g_mP + g_mN)
≈ 170 Ω at the frequencies that matter. R_s in series with C_L moves the pad pole from
g_m/(2π C_L) to g_m/(2π C_L (1 + g_m R_s)) and adds a zero at 1/(2π R_s C_L). With R_s = 50 Ω
(g_m R_s = 0.3) the pole moves 23 % down and the zero sits at 32 MHz for 100 pF, 3.2 MHz for 1 nF:
useless at 100 pF, worth 13° at 1 nF. With R_s ≥ 1/g_m (200–500 Ω) the zero reaches the crossover
for the large loads and the driver becomes unconditionally stable into any capacitance (1 nF: 24° → 63°
→ 80°). Into a resistive load the loop sees R_s + R_L, so the second-stage gain floor rises from
g_m R_L to g_m (R_s + R_L): 50 Ω → +6 dB and 1.8× the crossover per doubling.

| | R_s = 50 Ω | R_s = 200 Ω | R_s = 500 Ω |
|---|---|---|---|
| 1 nF phase margin | 37° (from 24°) | 63° | 80° |
| 1 nF overshoot / settling | 19 % / 1.9 µs | 3 % / 1.3 µs | 0 % / 2.1 µs (slew: 0.39 V/µs) |
| 100 pF | unchanged | +4° | +8°, settling 361 → 545 ns |
| 50 Ω load: loop | 0.42 MHz, 59 dB | 0.78 MHz, 67 dB | 1.15 MHz, 74 dB |
| 50 Ω load: pad amplitude | ½ (the double-terminated line) | 1/5 | 1/11 |
| 1 kΩ load: gain error | −4.8 % | −17 % | −33 % |
| 10 mA into 50 Ω: extra swing at `vout_a` | 0.5 V | 2 V (not available) | — |
| short-circuit current of the frames | limited to about 3.3 V / 50 Ω | | |
| line termination | none at this bandwidth | | |
| resistor | rppd 260 Ω/sq ± 10 %: 50 Ω = w 10 × l 2 µm; the pad cell already carries 587 Ω of it | | |

Reading:

- **R_s = 50 Ω with the feedback before it** is cheap and does three real things: it caps the
  frames' short-circuit current, it halves the pad voltage into a 50 Ω instrument input in the way
  every 50 Ω source does (the bench expects it), and it lifts the 1 nF margin from 24° to 37°. It does
  not make the driver faster, does not terminate a line at 2 MHz, and costs 4.8 % of gain into 1 kΩ.
- **R_s ≈ 200 Ω** is where the isolation works: stable into anything, 1 nF settles in 1.3 µs instead
  of 2.7, 50 Ω loads get a 3× faster loop. The price is a resistive divider the bench has to know
  (1 kΩ: −17 %), and a 50 Ω termination then sees one fifth of the signal. That is the LCD-driver
  "isolation resistor" regime (Itakura & Minamizaki 2002), good for capacitive bench loads, bad for a
  spec that promises a voltage into 50 Ω.
- **Feedback at the pad** (the only way to keep the DC accuracy into R_L) gives up every benefit and
  loses margin on top. If both accuracy into R_L and isolation are wanted, the feedback has to be
  split — DC from the pad, HF from `vout_a` — which needs a capacitor, or the output must become a
  current (the brainstorm's idea 1), where R_s is simply part of the load.
- Against the three targets of `alternatives.md`: R_s buys robustness, not area, speed or range.

## 6. Open

- The 50 Ω case with R_s = 50 Ω needs ±1 V at `vout_a` for ±0.5 V at a terminated pad; the 2 V
  drive window at the frames exists but the DDA feedback unit then sees ±1 V, outside its ±0.75 V
  linear range. Either the spec is "±0.25 V into 50 Ω" (what the table shows) or the units need
  the range `alternatives.md` §III is about.
- Corners, mismatch and the rppd tolerance (±10 %, into the 1 kΩ gain error) not run.
