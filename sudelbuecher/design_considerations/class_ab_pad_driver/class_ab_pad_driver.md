<!--
SPDX-FileCopyrightText: 2026 Christoph Maier
SPDX-License-Identifier: Apache-2.0
-->
# Two Proof-of-Concept Class-AB Analog Pad Drivers Built on ESD-Clamp Output Devices in IHP SG13CMOS5L

*Design note in the style of an IEEE JSSC paper. Simulation only, no layout, not reviewed.
Prepared for C. H. Maier, drafted with Claude (Opus 5.5), 30 September 2026.*

**Abstract** — Two differential-to-single-ended analog pad drivers are described for the
3.3-V thick-oxide devices of IHP's SG13CMOS5L 130-nm open-source process. Both reuse the IO
cell's ESD clamp frames as class-AB output devices: one `Clamp_P` frame (W = 546 µm,
L = 0.6 µm) and two `Clamp_N` frames re-drawn at L = 1.0 µm (W = 290 µm), so that the output
devices also remain the pad's primary ESD clamps. Both share a differential difference
amplifier (DDA) front end whose gain of ½ from the internal differential signal to the pad
is set by a ratio of two poly resistors, and whose inputs are high-impedance MOS gates.
Topology A is a two-stage amplifier with a floating class-AB control and plain Miller
compensation, intended for resistive loads. Topology B uses the same front end with
diode-loaded output gates, so that the pad node is the only high-impedance node and the load
capacitance compensates the loop. In typical-corner simulation, A settles to 1 % in 0.31 µs
into 1 kΩ ‖ 100 pF with 75° phase margin, drives ±10 mA into 50 Ω, and draws 427 µA.
B draws 359 µA and is stable for C_L ≥ 5 pF (47°) with phase margin increasing with C_L,
but has only 34 dB of loop gain and is unusable with resistive loads. The total harmonic
distortion of both is limited to about −46 dB by the open-loop linearity of the DDA front end.

**Index Terms** — Class-AB output stage, differential difference amplifier, ESD, Miller
compensation, load compensation, pad driver, SG13CMOS5L.

---

## I. Introduction

Shared-die platforms such as Chipalooza give each user slot a few single-ended analog pins,
while on-chip analog blocks are best built fully differential. The block proposed for the
`sg13cmos5l_cm_ip__single2diff2single` IP therefore needs a driver that takes an internal
differential signal and delivers a single-ended voltage at a pad, a function usually
provided by an op amp in a difference-amplifier connection [1].

Two constraints make this less routine than it sounds. First, SG13CMOS5L has no MIM
capacitor, so compensation capacitance must come from metal-oxide-metal (MOM) fingers on the
four thin metals, or be avoided altogether. Second, the output devices sit on the pad node and
must survive ESD; the cheapest way to guarantee that is to reuse IHP's own clamp frames, as
the digital `IOPadInOut30mA` cell already does, and to replace its `GateDecode` logic with
analog drive.

This note works out two topologies for that problem to the level of complete, simulated
ngspice netlists with realistic device sizes. Section II states the constraints, Section III
the output devices, Section IV the common front end. Sections V and VI describe topologies A
and B, Section VII gives simulated results, and Section VIII discusses limitations and next
steps.

## II. Constraints and Specification

All devices are the thick-oxide `sg13_hv_nmos` / `sg13_hv_pmos` (PSP103 models, identical to
SG13G2's), on a single 3.3-V supply. NMOS bulks are the common p-substrate, as the process
has no isolated NMOS; PMOS bulks are tied to their sources where this matters, since each can
sit in its own n-well.

The internal differential signal is taken as v_inp, v_inn = V_CM ± 0.5 V with
V_CM = 1.65 V, i.e. a differential swing v_d = v_inp − v_inn of ±1 V. With a gain of ½, the
pad voltage is v_out = V_ref ± 0.5 V, where V_ref = V_CM is also the reference of the output.
The inputs must be MOS gates, since the internal nodes (g_mC filter outputs, for example) are
high-impedance and could not tolerate resistive loading.

Loads considered: 50 Ω returned to V_ref (a terminated coaxial line; ±10 mA peak),
1 kΩ ‖ 100 pF returned to V_ref or to ground, and purely capacitive loads from 5 pF to 1 nF.

The available area is the 80 × 180 µm IO-cell outline. The primary ESD diodes (`DCNDiode`,
`DCPDiode`) and the P clamp frame occupy y < 85 µm. Removing `GateDecode` leaves roughly
80 × 95 µm (about 7600 µm²) for the second N frame and the drive circuitry.

## III. Output Devices

The companion note `../output_driver_sizing/README.md` characterizes the clamp frames as
output devices. Its conclusions are adopted here:

* **P:** one full `Clamp_P` frame at L = 0.6 µm, 41 fingers in two stacked rows
  (82 × 6.66 µm, W = 546 µm). Its Early voltage at 100 µA is about 26 V, so L is not
  lengthened.
* **N:** two `Clamp_N` frames at L = 1.0 µm, 33 fingers each (66 × 4.4 µm, W = 290 µm).
  At L = 0.6 µm the NMOS Early voltage is only 4 V, which makes a feedforward-controlled
  quiescent current depend on output voltage by ±30 %. At L = 1.0 µm, 1.55 frames suffice for
  10 mA at 0.3 V from the rail (mos_ss, 125 °C, 2.5-V gate drive).

At the chosen quiescent point (I_Q ≈ 240 µA, topology A) the simulated small-signal values are
g_mP = 2.93 mS, g_mN = 3.05 mS, g_dsP = 7.5 µS, g_dsN = 23 µS, C_ggP = 0.86 pF and
C_ggN = 0.69 pF.

These frames are far larger than the ±10-mA, ±0.5-V specification needs. They are kept at full
size because they are also the pad's ESD clamps, and because their size is what makes a class-AB
current gain I_out,peak / I_Q > 40 possible without leaving strong inversion.

## IV. Common Front End: Differential Difference Amplifier

A DDA [2] compares two differential voltages. Two transconductors with outputs summed in
opposite polarity drive a common high-gain stage, and negative feedback forces their output
currents to cancel:

```
Gm1 · (v_inp − v_inn) = Gm2 · (v_fb − v_ref)      ⇒      v_out − V_ref = (Gm1 / Gm2) · v_d       (1)
```

with v_fb = v_out. Unlike the resistive difference amplifier, all four inputs are gates.
Unlike a feedback network, however, both transconductors see large signals: pair 1 the full
±1 V, pair 2 the ±0.5 V output swing. Both must therefore be linear over their whole range,
which is obtained by source degeneration.

Each pair consists of two PMOS devices (W/L = 20/1 µm) with split 20-µA tail sources and a
`rhigh` resistor R_i between the sources. The differential output current of a pair is

```
Δi = 2 · v / (R_i + 2/g_m)        so        Gm_i = 2 / (R_i + 2/g_m)                            (2)
```

With g_m = 143 µS (2/g_m = 14 kΩ), R_1 = 115.6 kΩ (w = 0.5 µm, l = 39 µm) and
R_2 = 50.6 kΩ (l = 17 µm), this gives Gm_1 = 15.4 µS and Gm_2 = 31.0 µS, a ratio of 0.498.
The 2/g_m term is why R_1 is not simply 2 R_2. The gain therefore depends on the ratio of two
poly resistors plus a g_m term. It moves by about +2.5 % in the ss/125 °C corner, where g_m drops.

The pairs' drains are summed at the source nodes of an NMOS folded cascode (two 50-µA sinks).
A low-voltage PMOS cascode mirror converts the two branch currents (about 9 µA each) into a
single-ended current that drives the output-stage control nodes A and B. The linear range of a
degenerated pair is I_tail · R_i: 2.3 V for pair 1 and 1.0 V for pair 2, against required
swings of 1 V and 0.5 V. The residual nonlinearity, 5.5 mV maximum deviation from the best-fit
line over v_d = ±1 V, is outside any feedback loop. It sets the distortion floor of both
topologies.

## V. Topology A: Two-Stage, Floating Class-AB Control, Miller Compensation

**Class-AB control.** The output stage is the common-source push-pull of Section III, driven by
the floating class-AB control of Hogervorst et al. [3], a member of the feedforward
family that also contains Monticelli's floating-battery mesh [6]. Its PMOS and NMOS control devices
(MABp, MABn) sit in parallel between nodes A and B, in the right branch of the folded-cascode
summing circuit, so that they add neither noise nor offset. The left branch carries an
identical floating pair as a replica, as in [3].

The gate voltages of MABp and MABn come from two diode stacks in the bias block. Each stack
is a 1/41 (P) or 1/33 (N) replica of the output device in series with a replica of the control
device, fed by I_AB = 5 µA. The translinear loop on the P side,

```
V_SG(M_outP) + V_SG(MABp) = V_SG(M_refP1) + V_SG(M_refP2)                                       (3)
```

sets I_Q ≈ 41 · I_AB = 205 µA when MABp carries I_AB. The simulated value is 240 µA, because
MABp carries 4.5 µA, not 5 µA, and because the output devices sit at a higher V_DS than their
replicas. At full output current the non-conducting device keeps about 100 µA (50 Ω load),
which is what makes the stage class AB rather than class B.

**Compensation.** Two MOM capacitors (`cap_cmomi`, 31 × 31 µm, 1.0 pF each, 1.04 fF/µm² on
M1–M4) connect v_out to A and to B. For a second-stage gain well above one, the unity-gain
frequency of the loop is

```
f_c ≈ Gm_2 / (2π · 2 C_M) ≈ 31 µS / (2π · 2 pF) ≈ 2.5 MHz                                        (4)
```

(simulated: 2.2 MHz unloaded). The output pole lies at (g_mP + g_mN + 1/R_L)/(2π C_L): 11 MHz
for 1 kΩ ‖ 100 pF, and about 9.5 MHz for 100 pF alone. The two Miller capacitors add 2 pF to
the 0.9 pF + 0.7 pF of output-device gate capacitance on A and B. The pure Miller variant was
chosen over cascoded Miller, following the phase-margin comparison in [3] and because its
behavior does not depend on a precise pole–zero cancellation with a MOM capacitor of
unverified corner spread.

**Resistive-load limit.** Pole splitting requires the second stage to have gain. Its gain is
(g_mP + g_mN)(R_L ‖ r_o), which falls to about 0.3 at R_L = 50 Ω with I_Q = 240 µA. At that
point the Miller capacitors no longer split the poles. The crossover drops to 0.3 MHz, and the
loop gain available to suppress crossover distortion at 100 kHz is only a few times. Raising I_Q
helps only slowly (Table IV): the transconductance needed for real second-stage gain into 50 Ω
is of the order of 200 mS.

## VI. Topology B: Single-Stage, Load-Compensated

Topology B keeps the front end and the floating class-AB control of A, drops the Miller
capacitors, and connects diode-connected replicas of the output devices to A and B. The P diode
is 2 × 6.66 µm at L = 0.6 µm (1/41 of the output). The N diode is 2 × 3.8 µm at L = 1.0 µm,
about 1/38, trimmed from 1/33 to cancel a 19-mV systematic offset caused by the diode and output
devices running at different V_DS. The gates are then low-impedance
(1/g_m,diode ≈ 18 kΩ at 3.9 µA), and the pad node is the only high-impedance node. The loop
behaves as a current-mirror OTA with mirror ratio K ≈ g_m,out / g_m,diode ≈ 42:

```
T_0 ≈ Gm_2 · K / (g_dsP + g_dsN) ≈ 1.3 mS / 24 µS ≈ 35 dB,      f_c ≈ Gm_2 · K / (2π C_L)       (5)
```

The non-dominant poles are at the gate nodes, at g_m,diode / C_gg,out ≈ 10 MHz (P) and 14 MHz
(N). Stability therefore needs a minimum load capacitance, and the phase margin grows with C_L
(Table II). This is the inverse of topology A, where C_L has a maximum.

The DC loop gain is low because the output devices cannot be cascoded without giving up their
ESD role, and because the degenerated front end has a small Gm. For the same reason a resistive
load collapses the loop gain: 1.6 dB with 1 kΩ, −24 dB with 50 Ω.

A first attempt at topology B used two class-AB transconductors of the complementary
series-pair type [4], [5] as the DDA inputs, with current-mirror outputs. It was abandoned.
Each class-AB cell is linear only while both of its branches conduct, roughly ±0.2 V in
moderate inversion. Beyond that, the two cells work against each other: the balanced output
current is the small difference of two large branch currents. In simulation this raised the
output devices' current to 2.4 mA at v_d = ±1 V, with −20 dB THD. That netlist is not
included.

## VII. Simulated Results

All results are ngspice-42 simulations with the PDK models (tt, 27 °C unless stated). They were
produced by `run_d2s.py`; the full output is in `results.txt`. Bias reference currents are ideal
sources feeding transistor diodes, so corners vary the devices but not the references. The
MOM capacitors have no corner models and stay at their nominal value.

**TABLE I — Performance, tt 27 °C, I_AB = 5 µA**

| Load | Topology | Gain | Offset | I_Q (P/N) | I_DD | Loop gain T_0 | f_c | PM | 10–90 % rate | t_1% | THD 10 kHz / 100 kHz |
|---|---|---|---|---|---|---|---|---|---|---|---|
| 50 Ω ‖ 20 pF | A | 0.499 | 0.26 mV | 241/238 µA | 429 µA | 40.7 dB | 0.30 MHz | 90° | 0.83 V/µs | 873 ns | −40.1 / −23.8 dB |
| 1 kΩ ‖ 100 pF | A | 0.501 | 0.18 mV | 240/239 µA | 427 µA | 66.5 dB | 1.62 MHz | 75° | 2.64 V/µs | 307 ns | −46.0 / −45.3 dB |
| 1 kΩ to gnd ‖ 100 pF | A | 0.501 | −0.01 mV | 1754/104 µA | 1941 µA | 101.8 dB | 1.98 MHz | 81° | 2.75 V/µs | 321 ns | −46.0 / −45.9 dB |
| 20 pF | A | 0.501 | 0.18 mV | 240/240 µA | 427 µA | 96.5 dB | 2.17 MHz | 83° | 2.91 V/µs | 299 ns | −46.0 / −46.1 dB |
| 100 pF | A | 0.501 | 0.18 mV | 240/240 µA | 427 µA | 96.5 dB | 2.02 MHz | 66° | 3.78 V/µs | 311 ns | −46.0 / −46.0 dB |
| 1 nF | A | 0.501 | 0.18 mV | 240/240 µA | 427 µA | 96.5 dB | 1.00 MHz | 27° | 3.34 V/µs | 2307 ns | −46.0 / −43.9 dB |
| 1 kΩ ‖ 100 pF | B | 0.274 | 0.36 mV | 168/167 µA | 359 µA | 1.6 dB | 1.01 MHz | 140° | 2.49 V/µs | 177 ns | −44.9 / −44.9 dB |
| 20 pF | B | 0.491 | 0.58 mV | 167/167 µA | 359 µA | 34.3 dB | 6.45 MHz | 58° | 14.05 V/µs | 141 ns | −46.7 / −46.7 dB |
| 100 pF | B | 0.491 | 0.58 mV | 167/167 µA | 359 µA | 34.3 dB | 1.81 MHz | 79° | 2.69 V/µs | 307 ns | −46.7 / −46.6 dB |
| 1 nF | B | 0.491 | 0.58 mV | 167/167 µA | 359 µA | 34.3 dB | 0.20 MHz | 90° | 0.24 V/µs | 3195 ns | −46.7 / −45.2 dB |

Gain and offset are fitted over |v_d| ≤ 0.2 V. The step is v_d = −0.5 → +0.5 V
(v_out = V_ref − 0.25 V → V_ref + 0.25 V). THD is for a 1-V differential sine (0.5 V at the
output), harmonics 2–7. The "rate" column is the 10–90 % rise rate and includes linear settling,
so it is a slew rate only where the step is slew-limited. With 50 Ω the output of A reaches
−0.505 / +0.502 V at v_d = ∓1 V, i.e. ±10 mA, while the non-conducting device keeps 99 µA.
Topology B with 50 Ω or with 1 kΩ to ground has no loop gain and is omitted from the table
(see `results.txt`).

**TABLE II — Loop gain vs. load capacitance (no resistive load), tt 27 °C**

| C_L | 5 pF | 10 pF | 20 pF | 50 pF | 100 pF | 300 pF | 1 nF |
|---|---|---|---|---|---|---|---|
| A: f_c / PM | 2.18 MHz / 86° | 2.18 / 85° | 2.17 / 83° | 2.13 / 76° | 2.02 / 66° | 1.59 / 46° | 1.00 / 27° |
| B: f_c / PM | 13.6 MHz / 47° | 9.71 / 51° | 6.45 / 58° | 3.30 / 71° | 1.81 / 79° | 0.64 / 87° | 0.20 / 90° |

**TABLE III — Corners (ideal bias references)**

| Corner | A, 1 kΩ ‖ 100 pF: gain / offset / I_Q / PM | A, 100 pF: PM | B, 20 pF: gain / offset / I_Q / PM | B, 100 pF: PM |
|---|---|---|---|---|
| tt 27 °C | 0.501 / 0.18 mV / 240 µA / 75° | 66° | 0.491 / 0.58 mV / 167 µA / 58° | 79° |
| ss 125 °C (res wcs) | 0.512 / 1.30 mV / 226 µA / 74° | 63° | 0.505 / 3.17 mV / 162 µA / 54° | 77° |
| ff −40 °C (res bcs) | 0.497 / 0.12 mV / 254 µA / 75° | 68° | 0.487 / −1.00 mV / 174 µA / 59° | 79° |
| sf 27 °C | 0.500 / 0.17 mV / 240 µA / 75° | 66° | 0.491 / 1.31 mV / 167 µA / 58° | 79° |
| fs 27 °C | 0.501 / 0.20 mV / 239 µA / 75° | 66° | 0.492 / −0.17 mV / 167 µA / 58° | 79° |

**TABLE IV — Topology A into 50 Ω ‖ 20 pF vs. quiescent current, tt 27 °C**

| I_AB | I_Q | I_DD | I_min at ±10 mA | T_0 | f_c | THD 10 kHz | THD 100 kHz |
|---|---|---|---|---|---|---|---|
| 5 µA | 240 µA | 0.43 mA | 99 µA | 40.7 dB | 0.30 MHz | −40.1 dB | −23.8 dB |
| 10 µA | 748 µA | 0.95 mA | 423 µA | 49.5 dB | 0.52 MHz | −42.3 dB | −26.9 dB |
| 20 µA | 2.0 mA | 2.2 mA | 1.35 mA | 55.9 dB | 0.77 MHz | −44.5 dB | −31.3 dB |

**Area.** Excluding the output frames, topology A has about 440 µm² of front-end gate area plus
130 µm² in the bias block, and 1920 µm² of MOM capacitance. Topology B has no capacitors.
Without a layout, the estimate is that both fit in the ~7600 µm² freed above the P frame,
alongside the second N frame (80 × 10 µm). The Miller capacitors occupy M1–M4 and compete with
routing.

## VIII. Discussion

**Which topology.** For a pad that will see a probe, a scope input or a resistive termination,
topology A is the right starting point. It keeps 66–97 dB of loop gain for loads down to about
1 kΩ, is stable up to about 300 pF (46°), and holds its quiescent current within ±6 % over the
corners simulated.

Topology B demonstrates load compensation, but under these constraints it is weaker than
expected. The ESD role of the output devices rules out output cascodes, so the DC loop gain is
only 34 dB. That leaves a gain error of about 2 % (0.491 instead of 0.5 in Table I), and the
design fails completely with resistive loads. Its advantages are that it needs no capacitors,
and that it is fast and stable into large capacitive loads.

**50 Ω.** Topology A delivers the ±10 mA into 50 Ω, but with only 24 dB of distortion
suppression at 100 kHz. The second stage has no voltage gain into 50 Ω at any sensible
quiescent current (Section V). If 50-Ω operation matters beyond DC and low-frequency
characterization, one option is a series resistor inside the loop with the feedback taken
from its far side, so that the output stage works into a higher impedance; the simpler one is
to specify high-impedance instrumentation at the pad and treat 50 Ω as a DC and
low-frequency case.

**Distortion floor.** Both topologies stop at about −46 dB THD for 0.5 V at the output.
This is the open-loop nonlinearity of the degenerated DDA pairs (Section IV), not of the output
stage. It improves with more degeneration: a larger I_tail · R_i relative to the signal, at
the cost of current or resistor area. Linearizing the DDA pairs, or using them only as error
amplifiers inside a resistive feedback network, would be the next step if distortion matters.

**Not yet included:**

* Enable and power-down switches that hold the output gates off during ESD events and when the
  block is disabled.
* A real bias generator in place of the ideal references (the project's OgueyAebischerBias).
* Noise, PSRR and Monte Carlo mismatch simulations (the PDK has mismatch libraries; MOM
  capacitors have none).
* Layout parasitics, including the drain-strap resistance of the output frames.
* ESD simulation or qualification of the modified N frames.
* Which supply rails the output stage uses (slot `vdd_3v3` or the I/O rails), which also
  determines the ESD current paths.

## References

References are from memory and not re-checked for this note.

[1] J. H. Huijsing, *Operational Amplifiers: Theory and Design*, 2nd ed. Springer, 2011.

[2] E. Säckinger and W. Guggenbühl, "A versatile building block: The CMOS differential difference amplifier," *IEEE J. Solid-State Circuits*, vol. SC-22, no. 2, pp. 287–294, Apr. 1987.

[3] R. Hogervorst, J. P. Tero, R. G. H. Eschauzier, and J. H. Huijsing, "A compact power-efficient 3 V CMOS rail-to-rail input/output operational amplifier for VLSI cell libraries," *IEEE J. Solid-State Circuits*, vol. 29, no. 12, pp. 1505–1513, Dec. 1994.

[4] E. Seevinck and R. F. Wassenaar, "A versatile CMOS linear transconductor/square-law function circuit," *IEEE J. Solid-State Circuits*, vol. SC-22, no. 3, pp. 366–377, Jun. 1987.

[5] R. Castello and P. R. Gray, "A high-performance micropower switched-capacitor filter," *IEEE J. Solid-State Circuits*, vol. SC-20, no. 6, pp. 1122–1132, Dec. 1985.

[6] J. M. Monticelli, "A quad CMOS single-supply op amp with rail-to-rail output swing," *IEEE J. Solid-State Circuits*, vol. SC-21, no. 6, pp. 1026–1034, Dec. 1986.

## Appendix: Files

`d2s_miller.spice`
: Topology A, subcircuit `d2s_miller` (pins `vdd vss vinp vinn vref vout vfb` + six bias
  voltages). Tie `vfb` to `vout`; it is a separate pin only so that the loop can be broken in
  simulation.

`d2s_loadcomp.spice`
: Topology B, subcircuit `d2s_loadcomp`, same pins, parameters `wdp`, `wdn` (gate-diode widths).

`d2s_bias.spice`
: Bias block `d2s_bias` (ideal reference currents into transistor diodes), parameter `iab`
  (class-AB reference current, default 5 µA).

`tb_d2s_{miller,loadcomp}_{step,loop}.spice`
: Stand-alone ngspice decks (step response; loop gain via a 1-GH / 1-F break at `vfb`) using
  the PDK `.spiceinit` for model paths and OSDI. Interactive runs plot, batch runs print the
  measurements.

`run_d2s.py`, `results.txt`
: Script and output for every number in Section VII.

`xschem/d2s_{miller,loadcomp,bias}.{sch,sym}`, `xschem/xschemrc`
: xschem schematics and box symbols generated from the netlists above with the PDK's
  `sg13cmos5l_pr` symbols. Every device terminal carries a net label, so connectivity does
  not depend on wiring; placement follows signal flow and is meant to be tidied by hand.
  Parameters are frozen at their defaults (`wdp`, `wdn`, `iab = 5 µA`).

`gen_xschem.py`, `check_xschem.py`
: Generator for the schematics, and a device-by-device comparison (model, terminal nets in
  order, w / l / ng / value, port order) of xschem's netlist against the `.spice` source.
  After editing a schematic, `python3 check_xschem.py` netlists all three with xschem and
  compares them.
