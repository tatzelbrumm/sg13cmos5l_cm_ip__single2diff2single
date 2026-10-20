<!--
SPDX-FileCopyrightText: 2026 Christoph Maier
SPDX-License-Identifier: Apache-2.0
-->
# A Fully Differential Pad Input Buffer for SG13CMOS5L: the Mirror Image of the Matched-Pair DDA Driver, on the Same Bias

*Proposal. Companion to `../class_ab_pad_driver/` (`class_ab_pad_driver.md`,
`improvements/proposed_improvements.md`, `improvements/bias.md`, `power_down/log.md`). Simulation
only (ngspice-47, IHP-Open-PDK iic-jku `c271a7e9`, the IIC-OSIC-TOOLS 2026.09 pins of
`../../cloud_environment.md`), no layout, not reviewed. Prepared for C. H. Maier, drafted with
Claude (configured model `claude-opus-5-5`; the serving model may differ), 20 October 2026.
Running log: `log.md`. Every number: `sim/results_s2d.txt`, made by cloud-only scratch scripts; the
decks in `sim/tb/` reproduce one case of each test.*

**Summary.**

- **Topology.** `s2d_mpdda` takes the pad voltage `vin` and a pad reference `vref`, and delivers
  `voutp − voutn = 2 (vin − vref)` around an internal common mode `vcm`. It is the mirror image of
  `d2s_mpdda`, built from the same unit `unit_r2`:
  - four signal units, A1 = A2 on (vin, vref), F1 on (vcm, vfbp) and F2 on (vfbn, vcm);
  - one folded cascode stage, with the outputs as the only high-impedance nodes (load compensated);
  - two more units as the common-mode feedback (CMFB);
  - the gain is set by how the matched units are connected, not by a resistor ratio.

  This is the sketch of `../s2d_input_buffer_topology_verbatim.md`, now sized and simulated.
- **Shared bias.** It uses four of the driver's six bias lines (vbp, vbn, vbpc, vbnc), with the same
  diodes at the same currents. Following `bias.md`, bias crosses between blocks only as currents. The
  shared part is the root (`oa_core`, `bg_core` or the harness `ibias`) plus a fan-out with one 5 µA
  leg per consumer. Each buffer keeps its own small tree and diodes. The new cells are `s2d_bias_in`,
  `s2d_bias_out`, `bias_fanout_n` and `bias_fanout_p`. Nothing in `../class_ab_pad_driver/` changes.
- **Pad.** The Chipalooza harness accepts only IHP's 11 pad types, and it connects an analog slot pin
  to `padres` of a standard `sg13cmos5l_IOPadAnalog`, behind 586.9 Ω and the secondary clamps. The
  input buffer needs nothing else: its inputs are thick-oxide gates. It sits in the slot.
- **Performance, tt 27 °C, 0.5 pF of external load per output:**
  - gain 1.9991 (1.999 at all 11 corners);
  - DC nonlinearity over ±0.5 V: 1.4 mV at vcm = 1.65 V, 0.14 mV at 1.2 V;
  - loop gain 67.6 dB; f3dB 1.6 MHz; 1 % settling 0.49 µs;
  - input noise 0.67 µV/√Hz at 1 kHz;
  - input offset σ 5.9 mV, gain σ 1.1 %;
  - 99 µA, plus 19 µA for its own tree; 2680 µm² of drawn device area.
- **The internal common mode should be about 1.2 V, not 1.65 V.** The PMOS units need their gates at
  least about 1.3 V below vdd. At vdd = 3.0 V and vcm = 1.65 V the nonlinearity is 62 mV (tt) and
  140 mV (ss, −40 °C). At 1.2 V it stays at or below 0.7 mV at every corner. The driver's units have the
  same window, and its output reference must equal its input common mode, so this is a decision for both
  buffers.
- **Round trip** vin → `s2d_mpdda` → `d2s_mpdda` → vout, both on one shared `oa_core`: gain 0.9995,
  nonlinearity 0.02 mV, offset σ 8.0 mV (20 seeds, everything mismatched).
- **Enable.** `en_3v3` wrappers follow `../class_ab_pad_driver/power_down/`. Disabled, the cell draws
  0.14 nA at 27 °C and up to 5 nA at ff/3.6 V/125 °C, with both outputs tied to vcm. Enabled, it is
  unchanged. At enable, the output common mode swings by −1.6 / +1.1 V for about 1 µs. That glitch is
  open.
- **Verification.** There are eight ngspice decks and a CACE setup with ten parameter groups (514 runs).
  In the cloud, all 40 CACE results pass the proposed limits. Section VIII also maps every
  specification to a bench measurement, through the existing test configurations and the proposed
  test modes.

---

## I. Where the Buffer Sits

**Pad.** `sg13cmos5l_ocd_chipalooza/config.txt` lists the 11 pad types a user pad may take (`IOPadIn`,
`IOPadOut*`, `IOPadTriOut*`, `IOPadInOut*`, `IOPadAnalog`); the default is `IOPadAnalog`.
`scripts/parse_config.py` wires an analog pad's `padres` to the slot as `<name>_esd`, and
`verilog/gl/sg13cmos5l_padframe.v` shows the pad cells on the chip's `vdd3v3`/`vss3v3` as `iovdd`/`iovss`.
So the slot's `vin` is `padres`:

- behind `SecondaryProtection`'s 586.9 Ω rppd series resistor;
- with the `dantenna`/`dpantenna` secondary diodes to iovss/iovdd;
- and with the primary clamps (`Clamp_N20N0D`, `Clamp_P20N0D`, `DCNDiode`, `DCPDiode`) on the pad
  side (`claude/sg13cmos5l_pad_cell_internals.md`).

This is the node IHP's own `LevelDown` input feeds into thick-oxide gates. The buffer's input devices are
thick-oxide PMOS gates as well. No custom pad cell is needed, and none is allowed without the harness
maintainer.

> **For the output side.** `d2s_mpdda` case (a) reuses the clamp frames of a modified IO cell as output
> devices. That is a pad type outside the list above. Case (b), `d2s_lc2` in the slot behind
> `padres`, is the one the harness supports as it stands. Worth settling with Tim Edwards before any
> layout.

**Slot interface** (`TOP_LEVEL_MODULE.md` §2): `analog_pin[0]` = vin, `analog_pin[1]` = vout,
`analog_pin[2]` = vcm. Supplies `vdd_3v3`/`vss_3v3`, switched per slot; enables from 1.2 V `dig_in`
through level shifters (`macros/ls_up_1v2_3v3`). The buffer's ports:

| port | role |
|---|---|
| vdd, vss | slot vdd_3v3 / vss_3v3 |
| vin | `padres` of `analog_pin[0]` |
| vref | pad reference: gate only, from a pin, an internal divider or vcm |
| vcm | internal common mode, the same net as `d2s_mpdda`'s vref: gate only |
| voutp, voutn | internal differential signal |
| vfbp, vfbn | feedback sense; tied to voutp/voutn (separate only to break loops in simulation) |
| vbp, vbn, vbpc, vbnc | bias, from the buffer's own tree |
| en_3v3 | enable, `s2d_mpdda_pd` only, last in the list |

vin, vref and vcm drive only gates, so none of them carries DC current. The 587 Ω adds 3.1 nV/√Hz,
negligible against the buffer's own noise.

## II. Topology

**Signal DDA.** Each `unit_r2` delivers x += f(gp − gn), y −= f(gp − gn): a split-tail hv PMOS pair
(20/1 µm, 2 × 5 µA tails of 5/6 µm) with 150 kΩ of rhigh between the sources
(`../class_ab_pad_driver/improvements/sim/units.spice`). The fold nodes x and y sum four units:

```
   A1 = A2 :  gp = vin,  gn = vref   ─┐
   F1      :  gp = vcm,  gn = vfbp   ─┤   2 f(vin − vref) + f(vcm − vfbp) + f(vfbn − vcm) = 0
   F2      :  gp = vfbn, gn = vcm    ─┘
```

With vfbp = vcm + u and vfbn = vcm − u, the balance is 2 f(vin − vref) = 2 f(u), so u = vin − vref and
voutp − voutn = 2 (vin − vref) for any matched, odd, monotonic f. This is the driver's matched-pair
principle with the roles exchanged. Both cells have two input and two feedback units. In the driver,
each input unit sees half of the differential input and each feedback unit the whole single-ended
output, so the gain is ½. Here each input unit sees the whole single-ended input and each feedback unit
half of the differential output, so the gain is 2. The round trip is 1.

- Every unit has both gates near one common mode, the input units near vref and the feedback units near
  vcm. The `unit_r2` property that qualified it for the driver therefore still applies: its output
  depends only on gp − gn, through source followers (`proposed_improvements.md` §II).
- vref and vcm are separate inputs. A pad reference other than vcm costs 0.1–0.15 % of gain at
  vref = 0.5 V, vcm = 1.2 V (section IV), from the unit's 0.6 %/V transconductance-versus-common-mode
  dependence.

**Folded cascode, load compensated.**
- Main fold:
  - x and y each sink 30 µA through `SX`/`SY`, 36/6 µm as six fingers of the bias diode BN (6/6 at 5 µA).
  - The units deliver 20 µA to each node, so each branch carries 10 µA.
  - NMOS cascodes `CX`/`CY` and PMOS cascodes `LPC`/`LNC`, all 30/3 µm, as in the driver.
  - PMOS loads `LP`/`LN`, 24/4 µm, the same devices as the driver's mirror.
- The outputs are the only high-impedance nodes. The load capacitance sets the crossover, and the phase
  margin grows with it.
- **Built-in load:** two hv NMOS inversion capacitors `CLP`/`CLN`, 12 × 12 µm, gate on the output and
  S/D/B on vss. They give 0.53–0.62 pF each over 0.7–1.7 V. Without them, the common-mode loop has 40°
  at 0.2 pF per output (simulated before they were added). With them, it has 70° at no external load.

**Common-mode feedback** (after Duque-Carrillo's DDA-based CMFB [3]):
- Two more units, M1 on (vfbp, vcm) and M2 on (vfbn, vcm), summed with the same polarity:
  xc += f(vfbp − vcm) + f(vfbn − vcm). This is linear in the output common mode and second order in
  the differential signal. No resistive averaging loads the outputs.
- xc is folded like x: sink `SXC` is four BN fingers (20 µA), cascode `CXC`.
- `CXC` feeds a cascoded PMOS diode `D`/`DC`, a replica of a load and its cascode. Its gate `vcmfb`
  drives `LP`/`LN` 1 : 1.
- yc is folded the same way into vdd (`SYC`, `CYC`), so both CMFB drains sit at the same voltage.
- The sink ratios are finger counts of the same 6 µm finger. A first version used the driver's
  36/6 µm in four 9 µm fingers for SX/SY; its ratio error gave −22 mV of output common-mode error
  (now +11 mV).

**Loop gains** (section V): the differential and common-mode loops cross at the same frequency,
f_c ≈ 2 G_u / (2π C_out), with G_u ≈ 5.3 µS (the unit's one-sided transconductance, from the
simulated crossover). The common-mode loop has one more pole, at vcmfb, and with it less phase
margin: 17° less with no external load, 10° less at 0.5 pF, 4° less at 2 pF.

**Why not the textbook alternatives** (from the topology note): a follower plus an inverting amplifier
needs resistors that its outputs must drive, and turns differential signal into common mode at high
frequency. A resistive-feedback fully differential amplifier loads the pad and moves its input
common mode with the signal. Rail-to-rail input would need complementary NMOS units and break the
identical-unit cancellation, so the input range is a window (section IV), not the rails.

## III. Shared Bias Infrastructure

| line | current | diode | in `s2d_mpdda` | in `d2s_mpdda` |
|---|---|---|---|---|
| vbp | 5 µA out of | BP 5/6 | 6 × 2 unit tails | 4 × 2 unit tails |
| vbn | 5 µA into | BN 6/6 | SX, SY (6 fingers), SXC, SYC (4) | SX, SY |
| vbpc | 2 µA out of | BPC 1/4 | LPC, LNC, DC | PCL, PCR |
| vbnc | 2 µA into | BNC 1/8 | CX, CY, CXC, CYC | CX, CY |
| vabp, vabn | — | — | not used | class-AB loop |

**How it is shared** (`sim/s2d_bias.spice`). Gate lines are generated on the rail of the devices they
bias, and bias crosses from one block to another only as a current (`bias.md`). So:

```
 root, one per chip slot ──► fan-out ──► 5 uA ──► s2d tree ──► s2d diodes ──► s2d_mpdda
 (oa_core, bg_core,          (one leg   ├──► 5 uA ──► d2s tree ──► d2s diodes ──► d2s_mpdda
  or harness ibias)           per        └──► 5 uA ──► next consumer (gmC stage, vcm reference)
                              consumer)
```

- `bias_fanout_n`: an NMOS diode takes the root's 5 µA (`oa_core` and `bg_core` source it), and each leg
  sinks 5 µA out of a `*_bias_out` tree. `bias_fanout_p` is the mirror image, for a root that sinks.
- `s2d_bias_in` / `s2d_bias_out` are `d2s_bias_in` / `d2s_bias_out` without the class-AB legs: an
  input diode, four mirror legs, the four diodes. 200 µm², 19 µA including the 5 µA reference.
- `d2s_bias_out` is used as it is. `d2s_bias_oa` and `d2s_bias_bg` are already core + tree; in this
  scheme the core moves out into the root and the tree stays with the driver.
- One leg costs one 6/6 µm NMOS (36 µm²). Each consumer's current error is its own fan-out leg plus
  its own tree (σ about 1 % per mirror stage, `bias.md`), and does not correlate between consumers.

**Simulated** (`results_s2d.txt` §10, §11):
- `s2d_bias_out` fed by an ideal 5 µA sink, against the ideal fixture, at tt: the same gain,
  nonlinearity 1.7 mV instead of 1.4 mV, and an output common-mode error of 20 mV instead of 11 mV
  (15.6–21.9 mV over five corners).
- Round trip with one `oa_core` root, `bias_fanout_n`, `s2d_bias_out` and `d2s_bias_out`, at tt
  27 °C: gain 0.9995, offset 0.05 mV, nonlinearity 0.02 mV, 437 µA in all. That total includes the
  driver's 212 µA output stage.
- At ss 125 °C the root's +33 % current (`bias.md`, variant 3) costs the driver loop gain: round-trip
  gain 0.9977 and offset 1.4 mV (ideal references: 0.9988, 0.46 mV).

## IV. Signal Window and the Internal Common Mode

A PMOS unit needs its gate at most about vdd − 1.3 V. Above that, the tail leaves saturation at the
slow, cold corner. Nonlinearity over u = ±0.5 V, in mV, with vref = vcm (`results_s2d.txt` §3):

| vdd | corner | vcm 1.0 | 1.2 | 1.3 | 1.4 | 1.5 | 1.65 |
|---|---|---|---|---|---|---|---|
| 3.0 V | tt 27 °C | 0.47 | 0.31 | 0.70 | 3.22 | 16.5 | 62.5 |
| 3.0 V | ss −40 °C | 0.35 | 0.69 | 3.09 | 19.1 | 62.1 | 140 |
| 3.0 V | ff 125 °C | 2.00 | 0.17 | 0.19 | 0.39 | 1.55 | 12.2 |
| 3.3 V | ss −40 °C | 0.25 | 0.19 | 0.22 | 0.31 | 0.66 | 7.28 |
| 3.6 V | ss −40 °C | 0.23 | 0.13 | 0.13 | 0.14 | 0.16 | 0.25 |

- The top of the window: every unit gate (vin, vref, vcm ± 0.5 V) ≤ vdd − 1.3 V. That is ≤ 1.7 V at 3.0 V.
- The bottom: vin can reach 0 V (vref = 0.5 V). At the hot fast corner the input devices' drains come
  close to their sources there: 3.2 mV at ff/3.6 V/125 °C, against 0.3 mV at tt.
- **Proposal:** vcm = 1.2 V (window 0.7–1.7 V). The pad reference vref can sit anywhere in
  0.5–1.2 V. At vref = 0.5 V the pad range is 0–1 V, which includes vssio as `s2d_d2s_pinbuffers.md`
  asks. Gain at vref = 0.5 V, vcm = 1.2 V: 1.997–1.998.
- `d2s_mpdda` needs its own input common mode equal to its vref, because its matched-pair balance
  assumes it (`proposed_improvements.md` §II). So its output is centred on the same vcm, and its
  feedback units obey the same window. The power-down log already saw the effect: at ss/3.0 V/−40 °C
  the driver's output stopped at 2.08 V instead of 2.15 V.

## V. Simulated Performance

Unless stated: tt 27 °C, vdd 3.3 V, vref = vcm = 1.65 V (comparable with the driver's numbers),
0.5 pF external per output on top of `CLP`/`CLN`, ideal bias fixture `s2d_bias_lp`.

**TABLE I — DC over corners** (`results_s2d.txt` §2; offset and nonlinearity referred to the input)

| | gain | systematic offset | nonlinearity, vcm 1.65 / 1.2 V | output CM error | supply |
|---|---|---|---|---|---|
| tt 27 °C | 1.9991 (§6) | 0.004 mV | 1.41 / 0.14 mV | 10.9 mV | 98.7 µA |
| 11 corners | 1.999 | ≤ 0.008 mV | 0.21–7.28 / 0.09–0.20 mV | 7.1–16.1 mV | 98.5–99.1 µA |

**TABLE II — loop gain** (`results_s2d.txt` §5)

| external load per output | T0 dm / cm | f_c dm / cm | PM dm / cm | GM dm / cm |
|---|---|---|---|---|
| 0 | 67.6 / 67.8 dB | 2.67 / 2.62 MHz | 87.2° / 70.1° | 31.6 / 17.2 dB |
| 0.5 pF | 67.6 / 67.8 dB | 1.50 / 1.50 MHz | 88.4° / 78.6° | 36.6 / 22.2 dB |
| 2 pF | 67.6 / 67.8 dB | 0.65 / 0.65 MHz | 89.3° / 85.1° | 43.9 / 29.4 dB |
| 50 pF | 65.9 / 66.0 dB | 0.034 / 0.034 MHz | 90.0° / 89.8° | 69.5 / 55.1 dB |
| worst corner, 0 pF | 64.6 dB (3.0 V, ss −40 °C) | — | 86.3° / 63.3° (ff 125 °C, 3.0 V) | 29.6 / 14.5 dB |

Loaded only by `d2s_mpdda`'s unit gates, without any wiring, the differential loop has 87° (§5).

**TABLE III — closed loop** (`results_s2d.txt` §6, §7, §13)

| external load | f3dB | 10–90 % rise, ±0.25 V step | 1 % settling | overshoot | output CM during step |
|---|---|---|---|---|---|
| 0 | 2.75 MHz | 128 ns | 271 ns | 0 | 7.9…12.4 mV |
| 0.5 pF | 1.59 MHz | 230 ns | 485 ns | 0 | 9.1…11.9 mV |
| 2 pF | 0.66 MHz | 536 ns | 1127 ns | 0 | 10.1…11.6 mV |
| 10 pF | 0.17 MHz | 2010 ns | 3493 ns | 0.19 % | 10.2…11.4 mV |

- Noise, referred to u, with the 587 Ω pad resistor: 7.6 µV/√Hz at 10 Hz, 670 nV/√Hz at 1 kHz,
  151 nV/√Hz at 100 kHz; 156 µV rms from 10 Hz to 1 MHz. Flicker noise dominates at low frequency. The
  driver's is 1.35 µV/√Hz at 1 kHz referred to its differential input. The OSDI models give no
  per-device noise summary, so the contributors are not broken down.
- Input capacitance of vin: 17 fF (two gates, bootstrapped by their source followers), plus the pad
  cell and routing.

**TABLE IV — mismatch** (`results_s2d.txt` §9; 30 seeds; budget with one group at a time, 20 seeds)

| | input offset σ | gain σ | output CM σ |
|---|---|---|---|
| all, ideal bias | 5.9 mV | 1.07 % | 12.9 mV |
| all, with `s2d_bias_out` | 6.0 mV | 0.79 % | 13.4 mV |
| fold sinks SX, SY | 4.3 mV | — | 6.9 mV |
| unit pairs / unit tails | 1.7 / 1.4 mV | — | 0.8 / 2.2 mV |
| loads and their cascodes | 1.3 mV | — | 2.1 mV |
| unit rhigh | 0.06 mV | 0.84 % | — |
| CMFB fold and diode | — | — | 8.0 mV |

As in the driver, the folding sinks lead the offset (offset = current mismatch / transconductance,
`proposed_improvements.md` §I). Four times their area (72/12 µm, +1300 µm² for the pair) would halve
their share. The estimate from the budget is about 3.4 mV σ in total; not simulated. The gain spread is
the rhigh mismatch of the units.

**Rejection** (`results_s2d.txt` §8). Without mismatch the cell is symmetric and its differential
rejection is numerically infinite. With mismatch (20 seeds, tree mismatched too), referred to the
input, median / worst:

| source | 1 kHz | 100 kHz | 1 MHz |
|---|---|---|---|
| vdd | −83.5 / −76.4 dB | −83.2 / −76.1 dB | −77.6 / −71.2 dB |
| vss (references on the true ground) | −87.1 / −80.4 dB | −69.1 / −61.9 dB | −51.7 / −44.5 dB |
| vin and vref together | −92.6 / −85.3 dB | −92.5 / −85.2 dB | −89.0 / −82.4 dB |

Output common mode from vdd: −38.7 dB, flat to 100 kHz. It reaches the driver as an input
common-mode error, which the driver rejects to second order.

**Area** (drawn W·L, as in the driver's notes):

| part | units 6 × 125 | fold sinks | fold cascodes | loads + cascodes | CMFB fold + diode | output capacitors | total |
|---|---|---|---|---|---|---|---|
| µm² | 752 | 432 | 180 | 372 | 654 | 288 | 2678 |

Add 200 µm² for the tree and 36 µm² for the fan-out leg. `d2s_mpdda`'s front end is 2014 µm² by the
same measure. Wiring, wells and guard rings are not included. Six units must match: common-centroid
placement and the "same surround" rule apply, as for the driver.

## VI. Enable

`sim/s2d_pd.spice` wraps the unchanged cells, following `../class_ab_pad_driver/power_down/`. The
port is `en_3v3`, 0…3.3 V, active high, last in the port list:

| cell | switch | why |
|---|---|---|
| `s2d_bias_out_pd` | TG between the fan-out leg and PI; PI side pulled to vdd | the tree's only current root (decision 5 of the power-down log) |
| `s2d_bias_in_pd` | TG; NI side pulled to vss | the same, for a sinking root |
| `s2d_mpdda_pd` | TGs voutp → vcm and voutn → vcm | "input of next internal stage to VCM if off" (`s2d_d2s_pinbuffers.md`) |
| — | none on vbp, vbn, vbpc, vbnc, vcmfb | with the tree off they drift to their rails: tails, sinks, cascodes, CMFB diode and loads all off |

Results (`results_s2d.txt` §12; the fan-out leg stays on, as it would while the driver still runs):

- **Disabled**, both cells: 0.14 nA at tt 27 °C, 0.25 nA at ff/3.6 V/−40 °C, 1.3 nA at ss/3.0 V/125 °C
  and 5.0 nA at ff/3.6 V/125 °C, for any vin from 0 to 3.3 V. Outputs at vcm within 1.4 µV; vcm supplies
  at most 0.6 nA.
- **Enabled:** identical to `s2d_mpdda` (the wrappers add only switches that are off).
- **Enable:** vd is within 1 mV of its final value 1.2–1.5 µs after a 10 ns edge, and 2.2 µs after a
  1 µs edge, at every corner tried. **The output common mode swings by −1.6 / +1.1 V** in that time,
  because the ties release at once while the NMOS sinks come up before the CMFB-driven loads.
  The next stage sees a large common-mode step for about 1 µs. Options, not simulated:
  - hold the ties until the bias has settled (a second enable bit, or an RC delay on the tie gates);
  - start the loads from the diode side (pull vcmfb low briefly);
  - accept it, as the driver's enable glitch was accepted.
- **Disable:** vd is back at 0 (within 0.3 µV) 2 µs after the edge; no glitch.
- Unpowered: vin stays on gates only. The secondary diodes of `IOPadAnalog` clamp padres to the chip's
  vdd3v3, which is not switched with the slot. Not simulated.

## VII. Proposed Specification

Limits are proposals, set from the simulated numbers with margin. They are the limits the CACE
setup uses. Conditions: vdd 3.0–3.6 V, −40…125 °C, MOS and rhigh corners, vcm = vref = 1.2 V, 0.5 pF
external load, unless stated. The simulated column comes from sections IV–VI and from the first
CACE run (`verification/cace/first_run_summary.md`, all at vcm = 1.2 V). Section V's dynamic rows were
run at 1.65 V; the loop hardly depends on vcm (TABLE II's 3.0 V row is at 1.2 V, and CACE's loop and
step results at 1.2 V agree).

| parameter | proposed | simulated: tt / worst | CACE group | bench (section VIII) |
|---|---|---|---|---|
| gain (voutp − voutn)/(vin − vref) | 2 ± 0.5 % | 1.9991 / 1.9984 (CACE) | dc_params | B2 |
| gain mismatch σ | ≤ 1.5 % | 0.90 % (CACE, 100 seeds); 1.07 % (§9, 30 seeds, vcm 1.65 V) | mm_params | B2 over parts |
| input offset, systematic | ≤ ±1 mV | 0.002 / 0.004 mV (CACE: < 0.001 mV) | dc_params | B3 |
| input offset σ | ≤ 8 mV (≤ 20 mV over 100 seeds) | 6.7 mV, −16.9…+14.9 mV (CACE, 100 seeds); 5.9 mV (§9) | mm_params | B3 over parts |
| nonlinearity, u = ±0.5 V | ≤ 2 mV | 0.14 / 1.04 mV (CACE, 135 PVT points) | dc_params | B2 |
| signal window | unit gates ≤ vdd − 1.3 V; vin ≥ 0 V | §IV | range_params | B2 |
| output CM error | ≤ ±30 mV (σ ≤ 15 mV) | 12.4 / 21.1 mV (CACE); σ 11.0 mV (CACE), 12.9 mV (§9) | dc_params, mm_params | B4 |
| loop PM, external load 0…10 pF (50 pF at tt in §V) | dm ≥ 60°, cm ≥ 55° | dm 87.2° / 86.1°, cm 70.1° / 62.0° (CACE) | loop_params | B5 |
| closed-loop f3dB at 0.5 pF | ≥ 1 MHz | 1.59 / 1.36 MHz (CACE) | ac_params | B5 |
| 1 % settling, 1 V differential step | ≤ 1 µs | 0.49 / 0.54 µs (CACE) | tran_params | B5 |
| input noise at 1 kHz / 100 kHz | ≤ 1000 / 250 nV/√Hz | 670 / 151; worst 717 / 156 (CACE) | noise_params | B6 |
| PSRR vdd, vss, input-referred, 1 kHz | ≥ 60 dB (worst of 30) | ≥ 86 / 94 dB (CACE, worst of 30); ≥ 76 / 80 dB (§8, worst of 20, vcm 1.65 V) | ac_mm_params | B7 |
| CMRR (vin and vref together), 1 kHz | ≥ 70 dB | ≥ 88 dB (CACE); ≥ 85 dB (§8) | ac_mm_params | B7 |
| input capacitance, buffer only | ≤ 50 fF | 17 fF | (deck) | — |
| supply current incl. own tree | ≤ 130 µA | 118 µA | dc_params: cell + 14 µA fixture ≤ 125 µA (112.7 µA) | B1 |
| disabled supply current | ≤ 10 nA at 125 °C | 0.14 / 5.0 nA | (decks) | B1 |
| enable to 1 mV | ≤ 3 µs | 1.5 / 2.2 µs | (decks) | B8 |
| drawn device area | ≤ 3000 µm² | 2678 µm² | — | — |

Two rows are decisions rather than numbers: the internal common mode (1.2 V) and whether the enable
glitch is accepted.

## VIII. Verification and Characterization Suites

**Simulation, ngspice decks** (`sim/tb/`, run from that directory with the PDK `.spiceinit`; each names
its reference values):

| deck | checks |
|---|---|
| `tb_s2d_op` | operating point, saturation margin of every branch |
| `tb_s2d_dc` | gain, offset, nonlinearity, output CM, supply |
| `tb_s2d_loop` | differential and common-mode loop gain, loops broken at vfbp/vfbn |
| `tb_s2d_step` | rise, 1 % settling, output CM during a step |
| `tb_s2d_noise` | input-referred noise with the pad resistor |
| `tb_s2d_loopback` | vin → s2d → d2s → vout on one shared `oa_core` root |
| `tb_s2d_pd_leak`, `tb_s2d_pd_enable` | disabled current, outputs tied to vcm; enable and disable transients |

**Simulation, CACE** (`verification/cace/`, DUT `s2d_mpdda_biased` = `s2d_mpdda` + `s2d_bias_lp`, as
`d2s_miller_biased`; see its `README.md`):

| group | template | conditions | runs |
|---|---|---|---|
| dc_params | `_tb_dc` | vdd × MOS × rhigh × temperature | 135 |
| range_params | `_tb_dc` | vref × vcm × MOS × temperature, vdd 3.0 V | 96 |
| dc_bias_params | `_tb_dc` | ibias_err × va_bias | 15 |
| loop_params | `_tb_loop` | cload × MOS × temperature | 60 |
| ac_params | `_tb_ac` | MOS × temperature, 0.5 pF | 15 |
| ac_mm_params | `_tb_ac` | 30 mismatch iterations | 30 |
| tran_params | `_tb_tran` | cload (0, 0.5 pF) × MOS × temperature | 18 |
| noise_params | `_tb_noise` | MOS × temperature | 15 |
| mm_params / mc_params | `_tb_dc` | 100 mismatch / 30 process iterations (rhigh at typ, see the README) | 130 |

The enable is not in CACE, as for the driver: its DUT would be `s2d_mpdda_pd` with the tree, and the
decks cover it. The CACE run in the cloud (514 runs, 5 min on 2 cores) passes all 40 results; it is
summarized in `verification/cace/first_run_summary.md`, with what the first two runs got wrong.

**Bench.** With the buffer behind a pad, only vin, vout, vcm and the shared `analog_bus` are
observable. The plan uses the test configurations of `s2d_d2s_pinbuffers.md` and the test-mode blocks
of `../pad_test_circuit_suggestions_verbatim.md`:

| | measurement | configuration |
|---|---|---|
| B1 | supply current, enabled / disabled | slot supply current with en_3v3 toggled; difference against a slot with the buffer disabled |
| B2 | gain, nonlinearity, signal window | test 4 (input → output buffer): vout − vcm against vin − vref, DC sweep; the round-trip gain is 1, so the input buffer's gain error appears directly, plus the driver's |
| B3 | offset | test 4 at vin = vref; the polarity-reversing pass-through (+1 / −1, proposed there, not designed) would separate the two buffers' offsets |
| B4 | output common mode | test 3 through `analog_bus`; or the CM readout mode proposed there for the driver (unit B gates swapped, not designed), which puts (voutp + voutn)/2 − vcm at vout |
| B5 | loop, bandwidth, settling | small steps at vin (USB generator), response at vout; separate from the driver by also stepping the driver's ladder input |
| B6 | noise | vin tied to vref, spectrum at vout; subtract the driver's noise measured with the input buffer off (test 2) |
| B7 | PSRR, CMRR | AC injected on vdd_3v3 (transformer or capacitive, as in the original test plan) and on vin and vref together |
| B8 | enable timing | en_3v3 through the level shifter from a `dig_in` bit, vout on the scope |

`analog_bus` readout (test 3) needs a high-impedance instrument. A 1 MΩ scope input to ground takes
1.2 µA from a 10 µA branch and leaves only about 20 dB of loop gain. Use an instrumentation amplifier
on the PCB, as `s2d_d2s_pinbuffers.md` already plans.

## IX. Open Points

1. **Internal common mode** 1.2 V (section IV), for both buffers, and where it comes from: the vcm pin,
   an internal reference, or the harness `vbias`. It drives only gates.
2. **Pad reference.** There are three dedicated analog pins: vin, vout and vcm. The input buffer's vref
   can be the vcm pin (pad range 0.7–1.7 V), or an internal ~0.5 V reference so that the pad range
   includes vssio.
3. **Pad type for the driver** (section I): case (a) needs a twelfth pad type.
4. **Offset**: whether 5.9 mV σ is enough, or the sinks get 4× the area.
5. **Enable glitch** (section VI).
6. **Bias root** and the harness `ibias` direction decide between `bias_fanout_n` and `bias_fanout_p`.
7. **CMFB dump branch.** yc's 10 µA into vdd buys symmetric CMFB drain voltages. Folding yc straight to
   vss would save it, at a few mV of systematic CM error (estimate).
8. **Built-in output capacitors** (288 µm²) against relying on wiring capacitance.
9. **Schematics.** The sheets in `xschem/` are a generator-placed first pass (round trip
   MISMATCHES: 0). They are meant to be tidied by hand, as the driver's were.
10. **Move into the main repo.** Target: `macros/sg13cmos5l_IOPadSingle2Diff/`. That cell is now a
    stub with `in`, `vcm`, `outp`, `outn`, `vdd`, `vss`; it would gain `vref`, the bias or `iref`, and
    `en_3v3`.

## References

From memory and not re-checked, as in the driver's notes.

[1] E. Säckinger and W. Guggenbühl, "A versatile building block: The CMOS differential difference
amplifier," *IEEE J. Solid-State Circuits*, vol. SC-22, no. 2, pp. 287–294, Apr. 1987.

[2] B. A. Minch, *Analysis, Synthesis, and Implementation of Networks of Multiple-Input Translinear
Elements*, Ph.D. thesis, California Institute of Technology, 1997 (prolog: function inversion by
negative feedback around a high-gain amplifier).

[3] J. F. Duque-Carrillo, "Control of the common-mode component in CMOS continuous-time fully
differential signal processing," *Analog Integrated Circuits and Signal Processing*, vol. 4,
pp. 131–140, 1993.

[4] H. J. Oguey and D. Aebischer, "CMOS current reference without resistance," *IEEE J. Solid-State
Circuits*, vol. 32, no. 7, pp. 1132–1135, Jul. 1997.

## Appendix: Files

| file | content |
|---|---|
| `sim/s2d_mpdda.spice` | the buffer, subckt `s2d_mpdda` (parameters lcas, rl, wcl); needs `unit_r2` from `../class_ab_pad_driver/improvements/sim/units.spice` |
| `sim/s2d_bias.spice` | `s2d_bias_diodes`, `s2d_bias_lp` (fixture), `s2d_bias_in`, `s2d_bias_out`, `bias_fanout_n`, `bias_fanout_p` |
| `sim/s2d_pd.spice` | `s2d_mpdda_pd`, `s2d_bias_out_pd`, `s2d_bias_in_pd`, `inv_3v3_s2d` |
| `sim/tb/*.spice` | the eight decks of section VIII |
| `sim/results_s2d.txt` | every number in this note (sections 1–13) |
| `xschem/` | `s2d_mpdda`, `s2d_bias_lp`, `s2d_mpdda_biased` (`.sch`, `.sym`), `xschemrc` (adds `../../class_ab_pad_driver/improvements/xschem` for `unit_r2`) |
| `verification/cace/` | `s2d_mpdda_biased.yaml`, `templates/`, `README.md`, `first_run_summary.md`; CACE's own output `_docs/s2d_mpdda_biased.md` and `_docs/s2d_mpdda_biased_schematic.md` (plots not copied; CACE regenerates `netlist/` on every run) |
| `log.md` | running log |
