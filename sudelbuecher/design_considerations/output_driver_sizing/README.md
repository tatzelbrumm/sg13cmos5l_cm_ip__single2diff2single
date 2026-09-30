<!--
SPDX-FileCopyrightText: 2026 Christoph Maier
SPDX-License-Identifier: Apache-2.0
-->
# Output driver sizing: clamp frames as class-AB output devices

30 September 2026. Question: how much current, conductance and capacitance can
`sg13_hv_nmos` / `sg13_hv_pmos` deliver inside the 80 × 180 µm IO cell outline
(`macros/sg13cmos5l_IOPadDiff2Single`), using the `Clamp_N` / `Clamp_P` PCell frames?

`output_driver_char.py`
: ngspice DC sweeps of one full frame per polarity, L = 0.6 µm.
  N: ng = 42, W = 184.8 µm (80 × 9.9 µm frame).
  P: ng = 41 × 2 rows, W = 546.1 µm (80 × 19.26 µm frame).
  Run in IIC-OSIC-TOOLS after `source .designinit`: `python3 output_driver_char.py > results.txt`.

`results.txt`
: Output of the first run (cloud container, not yet re-run in the toolchain container).

## Findings

* One frame each covers 10 mA at 0.3 V from either rail in mos_ss / 125 °C, given ≥ 2.5 V gate drive
  (N ≈ 30, P ≈ 35 fingers needed). The existing ng = 15 devices do not.
* Full drive, tt: R_on ≈ 10 Ω (N), 13 Ω (P); ss 125 °C: 16 / 19 Ω.
* IHP's P:N width ratio (≈ 3:1) gives nearly symmetric drive, but C_gg of P is ≈ 3.5 × N
  (≈ 0.8 vs 0.2 pF at 100 µA): the two gate poles differ.
* The drivers add ≈ 0.23 pF (C_jd + C_gd,ov) to the pad.
* Miller-compensated output, output pole (g_mN + g_mP)/C_L ≥ 3 × GBW:
  C_L,max ≈ 180 pF at 1 MHz / 18 pF at 10 MHz for I_Q = 100 µA;
  ≈ 800 / 80 pF for I_Q = 1 mA.

## Longer L (same 80 µm frame, finger pitch L + 0.91 µm)

* NMOS at L = 0.6 µm has V_A ≈ 4 V at 100 µA: with the gate held fixed, idle current moves
  73 / 100 / 132 µA for |V_DS| = 0.5 / 1.65 / 2.8 V. L = 1.0 µm: 87 / 100 / 112 µA, needs
  1.55 frames for 10 mA (two N frames ≈ 20 µm tall). L = 2.0 µm: 4.9 frames.
* PMOS at L = 0.6 µm is already fine (V_A ≈ 26 V, 95 / 100 / 104 µA); L = 1.0 µm doubles
  frames and C_gg. Keep P at 0.6 µm.
* Alternative: both at 0.6 µm with feedback class-AB control (de Langen / Huijsing minimum
  selector), which regulates the actual device current.
* Longer L departs from IHP's reference clamp geometry; its ESD qualification basis is unknown.

## Output devices as primary ESD clamps (GateDecode replaced by analog drive)

* Feasible: `IOPadInOut30mA` already uses the same frames as drivers in the ESD path.
* Keep IHP's finger geometry (1.18 µm drain, contact placement, guard rings).
* Output devices on the same rails as DCN/DCP and the rail clamps; a switched `vdd_3v3`
  puts ESD current into a switched domain and lets the pad back-power an off slot.
* Default-off gates during ESD / power-down: enable-controlled HV switches (N gate to vss,
  P gate to vdd) instead of the 0D cells' 2–7 kΩ rppd, which would load a µA predriver.
* Gate slew ≈ 1 V/µs per µA/pF of predriver current into C_gg (0.2 pF N, 0.8–1 pF P).
* Resistive load: output-stage gain ≈ (g_mN + g_mP)·R_L (≈ 3.5 at 1 kΩ, I_Q = 100 µA), so
  longer L buys defined I_Q, not gain. I_peak = V_pk / R_L; 10 mA at 1.5 V_pk means R_L ≥ 150 Ω.

## Not included

Strap and via resistance (matters at 10 Ω R_on), electromigration in the 0.61 µm M2 drain straps,
hot-carrier/impact-ionization reliability at 3.3 V, ESD adequacy, sf/fs corners.

## Open questions

1. Output stage supply: slot `vdd_3v3`/`vss_3v3` (through the harness pMOS power switch) or I/O rails?
2. Gate drive range the predriver can deliver (folded-cascode summing nodes: |V_GS| ≈ 2.5–2.8 V?).
3. Swing: 0.3 V or 0.5 V from each rail?
4. Load: resistive (stated 30 Sep) — value, and returned to ground, V_CM or mid-supply? Is 10 mA the peak spec?
5. Quiescent current budget for the output stage.
6. Output devices stay primary ESD clamps and `GateDecode` is replaced by analog drive (stated 30 Sep).
   Open: may the NMOS deviate from IHP's reference geometry (L = 1.0 µm, two frames)?
7. Compensation: Miller (Hogervorst) or load-compensated?
8. Sign-off corners.
