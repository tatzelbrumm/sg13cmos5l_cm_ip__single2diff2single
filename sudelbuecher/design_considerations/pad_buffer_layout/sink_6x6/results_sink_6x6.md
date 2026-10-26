<!--
SPDX-FileCopyrightText: 2026 Christoph Maier
SPDX-License-Identifier: Apache-2.0
-->
# d2s fold sinks SX / SY: 4 × 9/6 against 6 × 6/6

2026-10-26. Run by Claude (Opus 5.5) for Christoph Maier, as decision 1 of `../layout_primitives.md`
(one sink finger, 6/6, for both pads). The macros are untouched. The variant exists only here:
`d2s_mpdda.spice` in this folder is `class_ab_pad_driver/improvements/sim/d2s_mpdda.spice` (byte-identical to
`macros/sg13cmos5l_IOPadDiff2Single/netlist/source/d2s_mpdda.spice`) with XSX, XSY at `ng=6` instead of
`ng=4`, plus three comment lines. W/L stays 36/6.

## Result

Mismatch, noise, loop and linearity do not change. One thing does: the sink-to-BN current ratio, and with it
the fold-branch current and I_Q.

| tt 27 °C, 1 kΩ ‖ 100 pF unless noted | 4 × 9/6 (now) | 6 × 6/6 |
|---|---:|---:|
| XSX / XSY current | 29.96 µA | 29.60 µA (−1.2 %) |
| fold branch (XCX, XPL) | 9.99 µA | 9.63 µA (−3.6 %) |
| XSX saturation margin | 0.090 V | 0.093 V |
| I_Q (OP / ON) | 212 / 212 µA | 219 / 219 µA (+3.4 %) |
| Idd (with the bias fixture) | 296 µA | 302 µA |
| gain, offset (systematic), INL | 0.4999, 0.05 mV, 1.24 mV | 0.4999, 0.05 mV, 1.24 mV |
| loop T0 / fc / PM | 78.9 dB / 1.37 MHz / 72.4° | 79.5 dB / 1.38 MHz / 72.4° |
| PM at 100 pF / 300 pF / 1 nF | 62.0° / 42.0° / 24.1° | 62.2° / 42.2° / 24.3° |
| THD 10 kHz / 100 kHz | −58.5 / −51.3 dB | −58.5 / −51.7 dB |
| output noise 1 kHz / 100 kHz / 10 Hz–10 MHz | 676.0 / 152.1 nV/√Hz / 230.8 µV | 669.6 / 151.3 nV/√Hz / 230.7 µV |
| corners: I_Q range | 207 … 219 µA | 213 … 227 µA |
| corners: lowest loop gain (tt 125 °C) | 56.3 dB | 57.6 dB |
| corners: lowest PM at 100 pF (tt 125 °C) | 56.2° | 56.4° |
| mismatch MC, 30 seeds: offset σ | 5.26 mV (−9.20 … 12.19) | 5.20 mV (−9.11 … 12.02) |
| mismatch MC: gain σ | 1.11 % | 1.11 % |
| mismatch MC: I_Q | 210.6 ± 9.0 µA | 217.8 ± 9.2 µA |
| budget (20 seeds): folding sinks | 4.32 mV | 4.26 mV |
| budget: tails / pairs / mirror / rhigh gain | 1.42 / 1.72 / 1.37 mV / 0.84 % | 1.42 / 1.72 / 1.34 mV / 0.84 % |

The MC uses the same seeds in both runs. Per seed, the offsets differ by at most 0.17 mV. The original
column reproduces `class_ab_pad_driver/improvements/sim/results_improvements.txt` exactly (op, table, cload,
corners, noise, mc, budget for `d2s_mpdda`), so the cloud toolchain matches the image.

## Why the ratio moves

The ratio of the sink to the bias diode BN (6/6 at 5 µA), from a single-finger operating point:

| | Vds = V_GS(BN) = 0.911 V | Vds = 0.375 V (sinks' operating point) |
|---|---:|---:|
| 6 × 6/6 | 6.000 | 5.920 |
| 4 × 9/6 | 6.073 | 5.994 |

- With identical fingers the ratio is exactly 6 at equal Vds, i.e. by construction.
- Per µm of width, 9 µm fingers carry 1.2 % more current than 6 µm fingers (finger-width dependence of the model).
- The sinks run at |Vds| = 0.375 V and the diode at 0.911 V. That costs 1.3 %.
- In today's netlist the two errors cancel by coincidence (5.994). The variant keeps only the Vds error (5.920).
- A 0.36 µA change in the 30 µA sinks is 3.6 % of the 10 µA fold branch, and it reaches I_Q through the
  class-AB control currents (ABP 5.17 → 4.99 µA, ABN 4.82 → 4.64 µA).

`s2d_mpdda` already uses 6/6 fingers, so its sinks carry the same Vds error. Its results include it.

## Consequences

- I_Q 219 µA and the I_Q range 213–227 µA stay inside the CACE limits of `sg13cmos5l_IOPadDiff2Single`
  (150 … 300 µA at sel 00; 100 … 350 µA for dc_sel).
- Making the ratio exact is a job for the diode, not the fingers: bias BN at the sinks' Vds, e.g. with a
  cascode device that holds BN's drain at about 0.37 V. With identical fingers the ratio would then be 6
  in both pads, independently of the finger geometry. Not simulated.
- The layout argument of `../layout_primitives.md` (one finger for SX, SY, SXC, SYC and BN in both pads,
  BN inside the sink row) stands. The variant changes no other number that matters.

## How it was run

- Cloud container, toolchain built after `sudelbuecher/cloud_environment.md`: ngspice-47, OpenVAF
  5ed9e63, iic-jku/IHP-Open-PDK `c271a7e9`; OSDI from the PDK's `openvaf-compile-va.sh`.
- Two copies of `class_ab_pad_driver/` (`run_d2s.py`, `d2s_bias.spice`, `d2s_miller.spice`,
  `improvements/sim/`). They differ only in `d2s_mpdda.spice`.
- `run_improvements.py op` ran as is. Its other sections stop at the first `baseline A` row: that variant's
  MOM capacitor (`cap_cmomi`) fails in this PDK commit ("Parameter mmax is out of bounds", OSDI
  setup_instance).
- The `d2s_mpdda` rows of table, cload, corners, noise, mc (30 seeds) and budget (20 seeds) were
  therefore run through the script's own functions (`ri.row`, `ri.cload_row`, `r.dc`, `r.loop`, `r.sim`,
  `ri.mm_files`, `ri.header`), with the variant list reduced to `d2s_mpdda`. The MC line also prints I_Q and
  the per-seed offsets.
- The ratio check: one deck, `mos_tt`, 27 °C. IBN 5 µA into a 6/6 diode; 36/6 at ng = 6 and ng = 4 with the
  gate on vbn, drain at 0.375 V and at vbn.
