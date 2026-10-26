<!--
SPDX-FileCopyrightText: 2026 Christoph Maier
SPDX-License-Identifier: Apache-2.0
-->
# Input-device bulks of `unit_r2`: own well, centre-tap well, or vdd

2026-10-26. Run by Claude (Opus 5.5) for Christoph Maier, on his question whether the input devices
can share wells: tie the well to a centre tap of the degeneration resistor, or put the bulks on vdd.
The question is whether that saves area without costing performance. The macros are untouched.
`d2s_mpdda_wells.spice` here holds the two unit variants and the matching `d2s_mpdda_ct` / `d2s_mpdda_vdd`;
`raw_wells.txt` is the unedited output.

| variant | bulks of Ma, Mb | wells per unit |
|---|---|---|
| `unit_r2` (now) | own source (sa, sb) | 2, plus well-to-well spacing |
| `unit_r2_ct` | centre tap c of rhigh, split into two halves of l/2 | 1, shared by Ma and Mb |
| `unit_r2_vdd` | vdd | 0: the input devices sit in the tails' well |

## Result: keep bulk = source

| d2s_mpdda, tt 27 °C, 1 kΩ ‖ 100 pF | bulk = source | well = centre tap | bulk = vdd |
|---|---:|---:|---:|
| unit Gm0 (5 µA tails) | 10.97 µS | 7.81 µS (−29 %) | 8.36 µS (−24 %) |
| unit Gm common-mode sensitivity | 0.4 %/V | 0.5 %/V | 4.8 %/V |
| unit compression at ±0.5 V | 1.2 % | 0.6 % | 7.1 % |
| unit-curve MP-DDA error at u = ±0.5 V | −1.25 / −1.21 mV | −0.88 / −0.87 mV | −16.8 / −13.2 mV |
| gain | 0.4999 | 0.4999 | 0.4999 |
| INL over vd = ±1 V | 1.24 mV | 0.88 mV | **16.85 mV** |
| INL, ss 27 °C / tt −40 °C | 3.50 / 2.15 mV | 2.12 / 1.17 mV | **30.3 / 24.1 mV** |
| THD 10 kHz / 100 kHz | −58.5 / −51.3 dB | −60.7 / −48.2 dB | **−35.9 / −35.4 dB** |
| loop T0 / fc / PM | 78.9 dB / 1.37 MHz / 72.4° | 76.0 dB / 0.99 MHz / 77.4° | 76.5 dB / 1.05 MHz / 76.5° |
| step, settling to 1 % | 327 ns | 555 ns | 499 ns |
| loop gain at tt 125 °C | 56.3 dB | 53.4 dB | 53.9 dB |
| output noise 1 kHz / 100 kHz | 676 / 152 nV/√Hz | **946 / 215 nV/√Hz** | 884 / 201 nV/√Hz |
| integrated noise 10 Hz–10 MHz | 231 µV | 277 µV | 267 µV |
| mismatch MC, 30 seeds: offset σ | 5.26 mV | **9.10 mV** (−19.1 … 18.4) | 6.93 mV |
| mismatch MC: gain σ | 1.11 % | 1.19 % | 1.16 % |
| INL at iovdd = 3.0 V (tt / ss 125 °C / ff −40 °C / ss 27 °C) | 43 / 35 / 35 / 53 mV | 55 / 47 / 41 / 78 mV | 84 / 67 / 76 / 88 mV |

Bold marks a CACE limit of `sg13cmos5l_IOPadDiff2Single` that the variant would break or come close to:
INL ≤ 10 mV, THD ≤ −35 dB, output noise ≤ 1000 nV/√Hz at 1 kHz and ≤ 200 nV/√Hz at 100 kHz, and an
offset of ±20 mV, i.e. 2.2σ at 9.1 mV.

## Why

- **Centre tap.** When a signal current flows through rhigh, Ma's source rises above the centre tap and
  Mb's falls below it by the same amount. The source-to-well junction of the device that should turn
  off is forward-biased, which lowers its |V_T|, and the other device sees the opposite. The body effect
  thus acts as extra degeneration:
  - Gm0 drops by 29 %, and the unit becomes slightly *more* linear (INL 0.88 mV);
  - everything that is referred to the input through Gm gets worse by about 1/0.71: noise (+40 %), offset
    from the sinks, tails and mirror (σ 5.3 → 9.1 mV), and the loop's crossover;
  - the signal also forward-biases the source-to-well junction, by up to I_tail·R/2 = 0.375 V at full
    current. That is harmless at 27 °C, but it is a vertical-PNP emitter at 125 °C.
  - Restoring Gm by lowering R would shrink the unit's linear range (±I·R) to about the ±0.5 V that the
    d2s units see; restoring it with more tail current costs power.
- **Bulk on vdd.** The body bias now depends on where the source sits (Vsb ≈ 0.8 V and more), so |V_T|
  rises with Vsb:
  - Gm depends on the common mode (4.8 %/V instead of 0.4 %/V);
  - the units of the MP-DDA see different common modes (A: vinp / vref, C: vref / vfb), so they no longer
    have the same f, and the cancellation that makes the gain independent of f breaks: INL 1.2 → 17 mV,
    THD −58 → −36 dB;
  - the higher |V_GS| also eats headroom, so at 3.0 V the INL reaches 84–88 mV.
- **Bulk = source** keeps each unit's f independent of the common mode (0.4 %/V). That is what the MP-DDA
  relies on.

## Area (hand estimate from the DRC rules, not drawn)

| | per | d2s (4 units) | s2d (6 units) |
|---|---|---:|---:|
| own wells, butted source ties, ≥ 1.8 µm apart (NW.b1) | ≈ 87 µm² per device | ≈ 700 µm² | ≈ 1050 µm² |
| centre tap: one well per unit, Ma Mb Mb Ma, one tie | ≈ 133 µm² per unit | ≈ 530 µm² | ≈ 800 µm² |
| bulk = vdd: input devices in the tails' well | ≈ 38 µm² per device + ≈ 60 | ≈ 360 µm² | ≈ 540 µm² |

The saving is 170–250 µm² (centre tap) or 340–510 µm² (vdd) per pad, against the ≈ 5000–5500 µm² of a
buffer front end. That is small next to the cost above.

The only well sharing that is electrically free: d2s's C1 and C2 have the same inputs and outputs, as do
s2d's A1 and A2. If their source nodes are joined (sa_C1 = sa_C2, sb_C1 = sb_C2), the two units become one
unit of double size, and the devices of the joined source nodes can share a well. That gives 6 instead of
8 wells (d2s), or 10 instead of 12 (s2d), roughly −100 µm². The nominal function is unchanged and the
mismatch of the two units averages. Not simulated.

## How it was run

As `../sink_6x6/results_sink_6x6.md`:
- same toolchain;
- a copy of `class_ab_pad_driver/` with `d2s_mpdda_wells.spice` added to the script's `FILES`;
- the script's own functions (`ri.header`, `ri.row`, `r.dc`, `r.loop`, `r.sim`, `ri.mm_files`).

The unit curves repeat `run_improvements.units()`, but biased like `unit_r2`: a 5 µA diode, 5/6, instead of
the 20 µA, 20/2 one of `unit_r`. The iovdd = 3.0 V runs only change `Vdd` in the header; vref stays at
1.65 V, as in `dc_3v0_params`. The bulk = source column reproduces `results_improvements.txt` (tt) and
README finding 1 (44 mV INL at 3.0 V).
