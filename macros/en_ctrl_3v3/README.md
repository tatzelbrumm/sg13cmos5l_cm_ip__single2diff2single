<!--
SPDX-FileCopyrightText: 2026 Christoph Maier
SPDX-License-Identifier: Apache-2.0
-->
# en_ctrl_3v3: fail-safe enable and select bits for the 3.3 V circuits of slot 7

**v2 (2026-11-08)**: netlist, sheets (`ls_up_fs.sch/.sym` new, `en_ctrl_3v3.sch` redrawn, `pg_det` removed), simulation
and CACE suite. v1 is in git history (last commit before 2026-11-08 15:00 UTC).

```
en_3v3   = en_1v2 at 3.3 V     en_3v3_b = NOT en_3v3     sel*_3v3 = sel*_1v2 at 3.3 V (gated by en_3v3 downstream)
```

Ports (order, unchanged from v1 so the sheets that place the symbol stay valid): `vddh vddl vss en_1v2 sel0_1v2
sel1_1v2 vdd1v2_sense vdd3v3_sense en_3v3 sel0_3v3 sel1_3v3 en_3v3_b`. **`vddl` and the two sense inputs are no longer
connected inside.** `vddh` / `vss` = the slot's switched `vdd_3v3` / `vss_3v3`.

## Why v2

v1 sensed the slot supplies with two ratioed detectors (`pg_det`: hv NMOS against a weak hv PMOS, RD pulling a floating
sense input low) and shifted with `ls_up_1v2_3v3` (needs the slot's 1.2 V). Enabled it drew 0.7–1.9 µA from vddh plus
0.4–1.7 µA into each sense input; with the slot's 1.2 V off and en_1v2 high its shifter latch drew up to 152 µA
(ss, −40 °C), and a held select bit lets a latch node float and drift into a crowbar (64 µA at sf, 125 °C, in the
v2 testbench with v1's shifters).

## How v2 works

- The harness drives `enable` and `dig_in` from its **always-on** 1.2 V rail: they are valid 0 / 1.2 V levels even
  while the slot's own `vdd_1v2` is off, and 0 while the slot is not selected. So no 1.2 V supply is needed to read them.
- **`ls_up_fs`** (one per bit): `XN1` (hv NMOS 1u/0.45u, gate = the 1.2 V input) pulls node x low. A **leaker** of
  10 hv PMOS 0.3u/20u in series, gates on the same input, pulls x high when the input is 0 (full gate drive) and is
  2–5× weaker while the input is 1.2 V. `XPF` (0.3u/5u, gate y) latches x high once disabled: hysteresis, and it
  holds x against XN1's leakage. Three inv_hv: y = in, out, out_b. The leaker is the only static current, and it flows
  only while the input is high.
- **No supply sensing.** The cell sits on the slot's switched vdd_3v3 and is unpowered with it. The pads on the ring
  take all their bias from `iref`, which the slot sources from that same supply; with the slot off they get none, and
  draw leakage only whatever the enable lines float to (starvation check below). A pull-down, detector or quiescent
  fail-safe on the ring side is therefore not needed. The pads are unchanged.
- `vddl` is not needed at all: slot 7 works with only its 3.3 V switched on.
- The input must be a harness level (enable, dig_in) or another always-valid 1.2 V level: XN1 conducts 0.6–8 µA at a
  0.67 V gate, so an input that floats at the level of a half-discharged rail would read as 1.

## Results (ngspice, extracted pads, 2026-11-08)

`testbenches/spice/`: `run_states.py` → `results/states.txt`, `run_starve.py` → `results/starve.txt` (decks and logs in
`runs/`, not committed). 11 points: tt / ss / ff / fs / sf × −40 / 27 / 125 °C × vddh 3.0 / 3.3 / 3.6 V, en and sel at
1.08 / 1.2 / 1.32 V. Supplies behind PMOS power switches as in the harness; vdd_1v2 off (discharged) and floating at
0.62 V; vdd_3v3 floating at 0.6 V.

| quantity | result |
|---|---|
| logic, 8 states per point (enabled, disabled, select, each with vdd_1v2 on / off / floating) | all correct |
| power-up with enable already high, vdd_1v2 off (default mode) | comes up enabled at every point |
| vddh current, enabled | 26–92 nA (plus the same per select bit that is high: 49–184 nA with one) |
| vddh current, disabled (also with vdd_1v2 off or floating) | ≤ 2.4 nA (125 °C), 0.0 at ≤ 27 °C |
| enable / disable delay, 50 fF load | 9.5–31 ns / 94–315 ns |
| slot vdd_3v3 floating at 0.6 V, enable high | outputs follow the floating rail (0.62–0.71 V); 2 nA from it |
| **starvation:** pad ring current, iref open, en_3v3 / en_3v3_b each anywhere in 0 … 3.6 V (169 pairs), pad 0 / 1.8 / 3.6 V | S2D ≤ 0.4 nA (−40 / 27 °C), ≤ 25 nA (125 °C); D2S ≤ 4.3 nA / ≤ 67 nA. Leakage of the output and ESD devices, nearly independent of the enable levels |
| starvation of pad_ref_rb (if on the ring), same sweep | ≤ 1.0 nA (−40 / 27 °C), ≤ 10.6 nA (125 °C) |

Not done: Monte Carlo (the margins are ratios of 10× and more: XN1 vs XPF, the leaker vs XN1's leakage), layout,
the sheets and the CACE suite for v2.

## Files

```
netlist/source/en_ctrl_3v3.spice     ls_up_fs, en_ctrl_3v3 (v2)
testbenches/spice/                   tb_states / tb_powerup templates, run_states.py, run_starve.py, results/
schematic/xschem/                    en_ctrl_3v3.sch/.sym (symbol unchanged), ls_up_fs.sch/.sym; renders in schematic/
verification/cace/                   v1 suite and results: to be rewritten for v2
```
