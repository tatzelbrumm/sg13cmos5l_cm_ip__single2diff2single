<!--
SPDX-FileCopyrightText: 2026 Christoph Maier
SPDX-License-Identifier: Apache-2.0
-->
# Proposed Revision of the Class-AB Pad Driver: Matched-Pair DDA, MOS Miller Capacitors, Resized Front End

*Companion to `../class_ab_pad_driver.md`. Simulation only (ngspice-42, IHP-Open-PDK `dev`,
tt 27 °C unless stated), no layout, not reviewed. Prepared for C. H. Maier, drafted with
Claude (configured model `claude-opus-5-5`; the serving model may differ), 2 October 2026.
Running log: `log.md`. Sources: `literature_notes.md`. Every number: `sim/results_improvements.txt`,
produced by `sim/run_improvements.py`.*

**Summary.** The first version's weaknesses trace back to four specific things, and only one
of them is a linear passive.

- **Area:** the two MOM Miller capacitors (1922 of 2387 µm² outside the frames).
- **Gain accuracy and linearity:** the gain was set by R1/R2 with a 2/gm term in each, so it
  moved by −2.6…+5.0 % over corners. The degenerated pairs' own nonlinearity sat outside the loop.
- **Offset:** the folding sinks, whose current is large compared with the front-end Gm.
- **Loop gain:** short internal cascodes. With resistive loads, the output stage's g_m·R_L also
  limits it, and that is structural.

The poly resistors themselves occupy 28 µm².

The revision `d2s_mpdda` keeps the clamp frames as output devices and the floating class-AB
control. It changes four things:

1. **Matched-pair DDA.** Four identical units in the arrangement f(vinp − vref) + f(vref − vinn)
   = 2 f(vfb − vref). This sets the gain ½ by the unit count, independent of R and gm, and
   cancels the units' nonlinearity, whatever it is, as far as they match. It is a static
   "externally linear, internally nonlinear" circuit.
2. **Miller capacitors.** Thick-oxide PMOS accumulation capacitors replace the MOM. They need
   3–3.75× less area and no metal.
3. **Currents.** Front-end currents are halved, the bias fixture is cut from 90 to 26 µA, and
   the sinks and mirror are resized for matching.
4. **Cascodes.** The internal cascodes are lengthened.

Result against the first version (1 kΩ ∥ 100 pF unless stated):

- current 427 → 296 µA
- loop gain +12 dB (66.5 → 78.9 dB; 50 Ω: 40.7 → 53.1 dB; capacitive: 96.5 → 104.3 dB)
- gain over 11 corners 0.4870…0.5249 → 0.4992…0.5000
- DC nonlinearity 5.5 → 1.2 mV; THD at 10 kHz −51 → −58.5 dB
- mismatch offset σ 14.4 → 5.3 mV
- output noise 1.6 → 0.68 µV/√Hz at 1 kHz

An area-lean variant that changes only the DDA and the capacitors halves the area (2387 →
1238 µm²) and leaves current and offset as they were. The resistor-free degenerations from
the literature were checked: a triode MOS, Sarpeshkar's well input, and an undegenerated
square-law pair. None of them fits this topology, for a reason the simulations make precise.
Cascoding the output devices is ruled out while they are the ESD clamps. With the output
devices in the slot, cascoding makes a capacitor-free, load-compensated driver with 74 dB of
loop gain, for capacitive loads only.

---

## I. Where the First Version's Numbers Come From

| quantity | first version | traced to |
|---|---|---|
| area outside the frames | 2387 µm² (gate 437, MOM 1922, rhigh 28) | MOM Miller capacitors on M1–M4 |
| supply current | 427 µA | output I_Q 240, bias fixture ≈ 90, front end ≈ 100 |
| gain over corners | 0.4870…0.5249 | Gm1/Gm2 = (R2 + 2/gm)/(R1 + 2/gm): R tracks R, gm does not |
| DC nonlinearity | 5.5 mV (12.7 mV at ss 27 °C) | the degenerated pairs, outside the loop |
| offset σ (30 MC seeds) | 14.4 mV | folding sinks 11.5 mV, tails 4.2, mirror 2.3, pairs 1.7 ² |
| loop gain, 1 kΩ ∥ 100 pF | 66.5 dB | A1 (short cascodes) × A2 = g_m,out (R_L ∥ r_o) ≈ 6 |

² Budget of the MP-DDA in the first version's sizing (fold, sinks and mirror identical),
one device group at a time, 20 seeds.

The offset budget follows Sarpeshkar's rule (1997, §3.3.4): the offset is the current mismatch
divided by the transconductance. A front end with a low Gm/I is offset-prone, and the
mirrors and sinks matter more than the input devices.

## II. Matched-Pair DDA

**Principle.** Four identical transconductance units, each delivering f(gp − gn) to the fold
nodes:

```
   unit A :  gp = vinp, gn = vref   ─┐
   unit B :  gp = vref, gn = vinn   ─┤   f(vinp − vref) + f(vref − vinn) = 2 f(vfb − vref)
   unit C1:  gp = vref, gn = vfb    ─┤   (C1, C2 subtract; the loop forces the balance)
   unit C2:  gp = vref, gn = vfb    ─┘
```

With the input common mode at vref, vinp − vref = vref − vinn = u, and the balance reads
2f(u) = 2f(v_out − vref). So v_out − vref = u = (vinp − vinn)/2 for any odd, monotonic f.
For an input common-mode error c, the two input units carry f(u + c) + f(u − c). The error is
second order in c. The gain ½ is the ratio 2 : 4 of unit counts. The units compress, and the
feedback units apply the inverse of the same law. This is the static form of ELIN: Minch's
"function inversion by negative feedback around a high-gain amplifier" (thesis, prolog), and
the cancellation Säckinger and Guggenbühl's DDA shows when both pairs carry the same signal.

**Requirement on a unit.** One input of every unit sits at vref. For the same differential
voltage x, the input common mode, and with it the source voltages, moves by +x/2 in A and C
and by −x/2 in B. So a unit qualifies only if
its output depends on gp − gn alone, not on where the sources sit. Its own linearity is
secondary. The test bench sweeps fA(x) = I(vref + x, vref) and fB(x) = I(vref, vref − x) and
solves fA(u) + fB(u) = 2 fA(v). For unit_r this gives −1.04 / −1.02 mV at u = ∓0.5 V; the full
driver's largest deviation from its small-signal line is 1.04 mV.

| unit | Gm0 | Gm vs input CM | own compression at 0.5 V | DDA error at u = −0.5 / +0.5 V |
|---|---|---|---|---|
| unit_r: split tails, rhigh between the sources | 15.6 µS | 0.6 %/V | 0.5 % | −1.0 / −1.0 mV |
| unit_t: same, triode hv-PMOS instead of rhigh | 15.5 µS | 77 %/V | 20 % | −191 / −72 mV |
| unit_w: well (bulk) input, gates at vss (Sarpeshkar) | 11.0 µS | −27 %/V | 6.8 % | +29 / +38 mV |
| unit_q: undegenerated square-law pair, 2/6 µm | 7.8 µS | −72 %/V | 22 % | +75 / +200 mV |

The split-tail resistor unit qualifies because each input device is a constant-current source
follower. A follower's transfer does not depend on the device law (Minch, thesis §7.2.1), so the
element between the sources sees exactly gp − gn. A triode MOS's resistance depends on its
V_SG, which is the absolute source voltage. The well input's κ depends on the well-to-gate
voltage (Sarpeshkar §3.3.1, §3.7.1). A single-tail pair's tail and channel-length modulation
see the source move. All three fail for the same reason. The poly resistor stays: the
design rule here is "no element whose value depends on the source voltage", not
"no resistor". In this topology a unit cannot be made symmetric in common mode, because the
feedback side has only vfb and vref; an inverted replica of the output would be needed.

**Result, nothing else changed** (`d2s_mp`: same fold, mirror, class-AB, frames, MOM caps,
bias, and same 80 µA of tail current as 8 × 10 µA):

| | first version | MP-DDA |
|---|---|---|
| gain, tt / 11 corners | 0.5005 / 0.4870…0.5249 | 0.4998 / 0.4983…0.4998 |
| nonlinearity ±1 V, tt / worst corner | 5.52 / 12.69 mV | 1.04 / 1.91 mV |
| THD 10 / 100 kHz, 1 kΩ ∥ 100 pF | −51.1 / −50.2 dB | −60.2 / −55.5 dB |
| THD 10 / 100 kHz, 100 pF | −51.0 / −51.0 dB | −60.0 / −59.8 dB |
| T0, fc, PM (1 kΩ ∥ 100 pF) | 66.5 dB, 1.62 MHz, 74.8° | 66.5 dB, 1.62 MHz, 74.7° |
| gain σ, offset σ (30 seeds) | 1.60 %, 14.4 mV | 1.33 %, 14.5 mV |

The gain σ is now the rhigh unit mismatch: 1.0 % for 0.5 × 36.4 µm units, and 0.84 % for the
0.5 × 50.6 µm units of `d2s_mpdda`. Four times the resistor area halves it, which costs about
75 µm² more per unit for the latter. The offset is untouched, because it lives in the fold (Section IV).

## III. Miller Compensation Without BEOL Capacitors

**Device.** Each Miller capacitor is an `sg13_hv_pmos` used as an accumulation capacitor, with
the gate above the n-well. On the A side the gate is node a (~2.6 V) and S/D/well is vout; on
the B side the gate is vout and S/D/well is node b (~0.7 V). Over the linear output range,
V_GW is 0.15…1.15 V (A) and 0.25…1.25 V (B). C_ox is ~5 fF/µm² (t_ox = 6.9 nm). In that
range the device delivers 0.38…0.76 of C_ox·A (C–V of a 14 × 14 µm device: 0.370 pF at
0.15 V, 0.648 pF at 1.0 V, 0.745 pF at 1.25 V; 31 × 31 µm MOM: 1.002 pF).

**Equivalence.** 18 × 18 µm per side reproduces the MOM pair's loop within a few degrees:

| C_L | 5 p | 20 p | 100 p | 300 p | 1 n |
|---|---|---|---|---|---|
| MOM 31 × 31 (fc / PM) | 2.18 MHz / 86.1° | 2.17 / 82.6° | 2.03 / 66.2° | 1.60 / 45.5° | 1.00 / 26.4° |
| MOS 18 × 18 | 2.14 / 86.4° | 2.14 / 82.9° | 2.00 / 67.0° | 1.59 / 46.3° | 1.00 / 26.9° |

That is 648 µm² of gate oxide instead of 1922 µm² of M1–M4 fingers. THD with capacitive
loads is unchanged (−60.0 / −60.0 dB at 100 pF). With 1 kΩ ∥ 100 pF, 100 kHz THD loses 2.3 dB
(−53.2 vs −55.5 dB): the C–V curvature modulates fc where the loop gain is lowest.

**Why the capacitor cannot simply be made small.** With Miller compensation the non-dominant
pole is ≈ g_m,out·C_M / (C_L·(C_g + C_M)). The gates of the frames carry C_g ≈ 0.86 pF (P) and
0.69 pF (N), so pole splitting needs C_M of the order of C_g whatever Gm1 is. Lowering Gm1
only lowers fc. Ways around that floor considered, but not simulated:
- **Source-follower buffers in front of the frame gates.** These make the high-impedance node
  small, so C_M could shrink to perhaps 0.2 pF (estimate), but the class-AB loop has to
  include the followers.
- **Indirect (current-buffer) compensation into the fold nodes.** Those nodes sit at ~0.37 V,
  which biases a MOS capacitor poorly. The a-side injection would also go through the mirror
  with the wrong sign unless injected at the mirror cascode's source.

Load compensation needs no capacitor at all, but it only works once the output can be
cascoded (Section V).

**ESD check item.** The A-side capacitor puts a p+/n-well junction, the n-well/p-sub diode and
7 nm of gate oxide between the pad and node a. The B-side capacitor puts gate oxide between
the pad and node b. The frames' own gate–drain overlaps already have the same oxide stress,
but the capacitors belong in the ESD review.

## IV. Currents, Offset, Noise: `d2s_mpdda`

Headroom fixes the sizing. Nodes a (~2.6 V) and b (~0.7 V) are the frame gates, which leaves
about 0.35 V each for the mirror and its cascode, and for the sinks and theirs. The
overdrive of the matching-critical devices therefore cannot be raised; their area can.

| block | first version | d2s_mpdda |
|---|---|---|
| unit tails | 2 pairs × 2 × 20 µA = 80 µA | 4 units × 2 × 5 µA = 40 µA (5/6 µm) |
| unit degeneration | rhigh 116 k / 51 k | rhigh 150 kΩ (I_t·R = 0.75 V) per unit |
| folding sinks | 2 × 50 µA, 25/2 | 2 × 30 µA, 36/6 |
| mirror / cascodes | 10/2, L = 1 µm cascodes | 24/4, L = 3 µm cascodes (W = 10 L) |
| bias fixture references | 90 µA | 26 µA |
| output I_Q (P/N) | 240 µA | 212 µA (class-AB devices now carry 5.2/4.8 µA) |
| I_DD | 427 µA | 296 µA |

All conducting devices are at least 80 mV clear of saturation at vd = 0 (listing in the results file).

| | first version | d2s_mpdda |
|---|---|---|
| T0: 1 kΩ ∥ 100 p / 50 Ω / 100 p | 66.5 / 40.7 / 96.5 dB | 78.9 / 53.1 / 104.3 dB |
| fc / PM: 100 p, 300 p, 1 n | 2.02 MHz/66.4°, 1.59/45.6°, 1.00/26.5° | 1.77 MHz/62.0°, 1.39/42.0°, 0.87/24.1° |
| gain over 11 corners | 0.4870…0.5249 | 0.4992…0.5000 |
| nonlinearity, tt / worst (ss 27 °C) | 5.52 / 12.69 mV | 1.24 / 3.50 mV |
| THD 10 / 100 kHz, 1 kΩ ∥ 100 p | −51.1 / −50.2 dB | −58.5 / −51.3 dB |
| THD 10 / 100 kHz, 50 Ω | −46.2 / −29.1 dB | −45.4 / −26.9 dB |
| t_1%, 1 kΩ ∥ 100 p | 307 ns | 327 ns |
| offset σ / gain σ (30 seeds) | 14.4 mV / 1.60 % | 5.3 mV / 1.11 % |
| output noise 1 kHz / 100 kHz / 10 Hz–10 MHz | 1599 / 200 nV/√Hz / 278 µV | 676 / 152 nV/√Hz / 231 µV |

Offset budget of `d2s_mpdda` (σ, mismatch on one group at a time, 20 seeds): sinks 4.3 mV,
unit pairs 1.7 mV, tails 1.4 mV, mirror 1.4 mV, the rest < 0.1 mV. The sinks still lead.

The halved front-end Gm lowers fc from 1.62 to 1.37 MHz (1 kΩ ∥ 100 pF). That costs the
100 kHz THD gain of Section II and makes 50 Ω slightly worse. 14 × 14 µm capacitors raise
fc to 2.12 MHz at 100 pF but leave 54° of PM; the choice belongs to the specification.
50 Ω stays what the first note called it: a DC and low-frequency case.

## V. Cascoding

**(a) Output devices are the pad's ESD clamps.** A cascode in series would put its own drain,
not the clamp's, on the pad. A stacked clamp frame would be a new ESD structure needing its
own qualification. So the output stays uncascoded, and the frames' r_o (V_A ≈ 26 V P,
L = 1.0 µm N) bounds the second stage. What can be cascoded are the internal high-impedance
nodes a and b:

| fold and mirror cascode L (W = 10 L) | T0, 1 kΩ ∥ 100 p | T0, 100 p | T0, 50 Ω | PM 100 p | gate area |
|---|---|---|---|---|---|
| 1 µm | 69.7 dB | 99.6 dB | 43.9 dB | 63.4° | 1081 µm² |
| 2 µm | 75.4 | 103.1 | 49.6 | 62.8° | 1201 |
| 3 µm (default) | 78.9 | 104.3 | 53.1 | 62.0° | 1401 |

Regulated (gain-boosted) cascodes do not fit. The ~0.35 V per device next to nodes a and b
leaves no room for an auxiliary amplifier's V_GS.

**(b) Output devices in the slot, pad through IOPadAnalog.** Then the output can be cascoded.
`d2s_lc2` is load-compensated, so it has no compensation capacitor at all. It uses the MP-DDA
front end and half-frame output devices; the cascode gates sit at vref, giving an output range
of ~1.0…2.4 V.

| | T0 | PM 5 p | 20 p | 100 p | 1 n | 1 kΩ ∥ 100 p | I_DD |
|---|---|---|---|---|---|---|---|
| uncascoded | 37.2 dB | 16° | 47° | 78° | 89° | no loop gain | 174 µA |
| cascoded | 74.0 dB | unstable | 39° | 77° | 89° | no loop gain | 169 µA |

Cascoding adds 37 dB. It does not help resistive loads, which collapse any single-stage
loop, and it does not remove the minimum load capacitance (~30–40 pF).

In the slot, the pad is reached through IOPadAnalog, where `padres` sits behind 586.9 Ω of
SecondaryProtection. Sensing the loop at `padres` (the near side) turns that resistor into an
isolation resistor: PM 39° → 62° at 20 pF, and 104° at 100 pF. The pad then sees a
587 Ω · C_L low-pass outside the loop, 2.7 MHz at 100 pF. Sensing at `pad` (the far side)
keeps the PM of the bare stage. 50 Ω cannot be driven through 587 Ω.

Two open points in `d2s_lc2`:
- **Offset.** 7.8 mV of systematic offset, because the diode replicas sit at a different V_DS
  than the cascoded output devices. Cascoding the replicas should remove it.
- **Area** (estimate, not simulated). For the same output pole at the same current, in-slot
  devices for topology A would need about the frames' W, because the frames' g_m/I of
  ~12.5 V⁻¹ at 240 µA is what sets the non-dominant pole. Moving the devices into the slot
  is therefore not an area saving.

## VI. Externally Linear Circuits With Non-Exponential Internal Nonlinearity

Edwards (thesis p. 72) names the square law of strong inversion and the exponential as the two
nonlinearities that ELIN circuits can exploit. The table covers what else the sources offer
and how each fares here.

| approach | internal law | sources | verdict for this driver |
|---|---|---|---|
| matched-nonlinearity feedback, f⁻¹∘f | any odd monotonic f (here: degenerated square law) | Minch prolog; Säckinger DDA | **used**; the unit must depend on gp − gn only (Section II) |
| MOS translinear loop | square law | Edwards [37] Wiegerink; Seevinck–Wassenaar | already present: the floating class-AB control is a square-law translinear loop |
| constant-sum square-law push-pull, I_P − I_N = 2β(V_Q − V_t)·δ exactly for \|I_out\| < 4 I_Q | square law | Sarpeshkar p. 25 identity | the frames run at g_m/I ≈ 12.5 V⁻¹ (moderate inversion); exact square law would need mA of I_Q; not pursued |
| √-domain / dynamic translinear filters | square law or exp | Mulder et al. 1997; Efthivoulidis–Tsividis | dynamic (filters); a static buffer has nothing to compand |
| triode MOSFET-C | triode quadratic, even orders cancel | (MOSFET-C literature) | needs balanced signals; the feedback side here is single-ended |
| capacitive dividers: FG input, MITE, AFGA, MIFG | capacitive + exp or law-independent follower | Minch ch. 6–7; Hasler ch. 4–5; Sánchez-Sinencio; Montalvo–Paulos | needs linear capacitors, charge control (tunneling, injection or UV) and AC coupling; none of these is available or acceptable here |
| well input, bump linearization | κ-scaled law; bump in subthreshold | Sarpeshkar ch. 3 | Gm depends on input CM: +29/+38 mV error (unit_w); bump range is subthreshold-sized |
| undegenerated strong-inversion pair | square law | — | linear enough, but sources move with the signal: +75/+200 mV error (unit_q) |

ELIN without the exponential is therefore feasible here in one form: function inversion by
matched units. Its precondition is not a particular law but source-voltage independence of the
unit, which the source-follower-plus-resistor unit provides. The square-law translinear
classics need either strong inversion at currents this driver doesn't spend, or balanced
signals that a single-ended pad doesn't have.

## VII. Options

| variant | area outside frames | I_DD | offset σ | T0 1 kΩ ∥ 100 p / 50 Ω / 100 p | gain over corners | THD 10 / 100 kHz (1 k ∥ 100 p) |
|---|---|---|---|---|---|---|
| first version (`d2s_miller`) | 2387 µm² | 427 µA | 14.4 mV | 66.5 / 40.7 / 96.5 dB | −2.6…+5.0 % | −51.1 / −50.2 dB |
| area-lean: `d2s_mp` + MOS 18 × 18 | 1238 µm² | 427 µA | 14.5 mV | 66.5 / 40.7 / 96.5 dB | −0.3…0 % | −60.1 / −53.2 dB |
| `d2s_mpdda`, lcas = 1 | 1694 µm² | 296 µA | 5.3 mV ¹ | 69.7 / 43.9 / 99.6 dB | not simulated | −58.7 / −51.4 dB ¹ |
| `d2s_mpdda`, lcas = 3 (default) | 2014 µm² | 296 µA | 5.3 mV | 78.9 / 53.1 / 104.3 dB | −0.16…0 % | −58.5 / −51.3 dB |

Area is drawn device area (W·L, resistor w·l, capacitor w·l) without the frames and the bias
fixture, as in the first note. The area-lean variant's corner gain is that of `d2s_mp`; the
capacitors do not enter the DC gain. ¹ From the intermediate run in `log.md` (`d2s_mp2`: the circuit of
`d2s_mpdda` with lcas = 1 except ng = 1 in the cascodes; its loop numbers agree with the
lcas = 1 row of `results_improvements.txt`), not from `results_improvements.txt` itself.

## VIII. Not Done

- xschem schematics and the CACE run for `d2s_mpdda`. The existing yaml should take it as a
  new DUT with `d2s_bias_lp` as fixture.
- Layout. The four units must match, so common-centroid placement and Edwards's "same surround"
  rule (thesis §3.10) apply. The PMOS input devices sit in separate wells (bulk = own source).
- PSRR, CMRR, input CM range, supply corners (3.0 / 3.6 V), process MC (`tt_stat`). Only
  mismatch MC was run.
- The ESD review of the pad-connected MOS capacitors (Section III).
- `d2s_lc2`: cascoded replicas, a real minimum-C_L specification, and whether a slot-side
  driver is wanted at all.
- Inherited from the first version, seen in the operating-point listing: the PMOS of the
  left floating replica (XFPL) carries 1 nA (bulk at vdd: |V_GS| = 0.78 V against a
  body-shifted |V_th| of 1.01 V),
  so only XFNL replicates the class-AB control. It works, but the replica is not one.

## Appendix: Files (in `sim/`)

| file | content |
|---|---|
| `d2s_mpdda.spice` | proposed driver, subckt `d2s_mpdda` (pins as `d2s_miller`; parameters wc, lc, lcas, rl) |
| `units.spice` | DDA units unit_r, unit_r2 (used by d2s_mpdda), unit_t, unit_w, unit_q |
| `d2s_bias_lp.spice` | bias fixture for d2s_mpdda (same pins as `d2s_bias`) |
| `d2s_mp.spice`, `ccomp.spice` | MP-DDA in the first version's sizing; MOM or MOS capacitors via a testbench wrapper |
| `d2s_lc2.spice` | in-slot, load-compensated, cascoded (`d2s_lc2`) and uncascoded (`d2s_lc2_nc`) |
| `run_improvements.py` | reproduces every number here; imports `../../run_d2s.py` unchanged |
| `results_improvements.txt` | its output (3 min 49 s on 2 cores) |
