# Stream of consciousness: fully differential exercises behind the S2D/D2S pads

Written 3 October 2026 while you were away. Ideas only: no netlists, no simulations, nothing checked. References are from memory and unchecked.

## First, the socket

Before listing circuits, it helps to fix what a student block plugs into, the way TinyTapeout fixes a digital tile. Students then design against a contract, not against our buffers' internals. My first guess at that contract:

- **Differential input pair `inp`/`inn`:** comes from the S2D or the DC ladder, centred on vcm ≈ 1.65 V, ±0.5 V per side (±1 V differential). The block must present only MOS gates here.
- **Differential output pair `outp`/`outn`:** same range. It drives only gates (the D2S units, the CM readout, a comparator) plus routing, so a few hundred fF to about 1 pF. No resistive loads ever. That rules out resistive feedback in student blocks by construction, not just by advice.
- **`vcm`, `vbn`/`vbp` (mirror off your own matched device, Oguey–Aebischer style) or a raw `ibias`, `en`, `vdd_3v3`, `vss`.** When `en` is low, the outputs go to vcm through gate-only switches.
- **Bias currents of 10–100 nA per branch on 3.3 V thick-oxide devices.** That puts most transistors in weak or moderate inversion and bandwidths in the kHz to tens-of-kHz range. That's the right speed for USB instruments and beginners: parasitics barely matter, and the physics (exponential law, U_T, κ) is visible on the bench.

The no-bulky-passives rule then has teeth. Time constants come from gm/C with C as gate capacitance, gain from current or geometry ratios, and linearity from circuit structure. Never from an R that has to be accurate.

## Introductory exercises

**1. The gm/gm amplifier.** A differential pair loaded by a diode-connected pair, with no current-source load and no resistor. In weak inversion the gain is (I_in/n_in)/(I_load/n_load), so for matched devices it's just the ratio of the tail currents. Gain comes from a current ratio. That's the single most important on-chip lesson, and it fits on one page. Students measure gain against the current ratio through the pads and find it holds over decades. Then they find where it stops (the moderate-inversion transition) and why. Fully differential is natural here: the diode loads set the output common mode, so the first exercise needs no CMFB. The catch is the linear range. A plain subthreshold pair is linear only over about ±U_T·n, roughly ±40 mV, against ±0.5 V coming in. That isn't a reason to add an attenuator: it's the next exercise.

**2. Making a transconductor linear without a resistor.** This is where the ±0.5 V socket swing turns a nuisance into a curriculum. Several all-MOS answers, each a self-contained small project:
- Krummenacher–Joehl degeneration: two triode MOSFETs between the sources. Your improvements note shows triode degeneration fails in the DDA because its common mode moves. Inside a fully differential block whose input CM is held at vcm, it works. That makes a nice "same device, different context" lesson.
- Bump linearization (Delbrück): add a bump path in parallel with the pair to flatten tanh.
- Multi-tanh (Gilbert): two or three offset pairs whose tanh curves sum to a flatter one. The offsets come from W ratios, which is geometry again.
- Sarpeshkar–Lyon–Mead wide-linear-range OTA: well input, gate degeneration, bump linearization, about ±1 V of linear range at nanoamperes. Probably intermediate rather than introductory, but it's the classic answer to exactly this socket's swing.

Students compare these by sweeping vin through the S2D and reading the output current. The current needs an on-chip diode-connected load to turn it back into a voltage, which is exercise 1 again.

**3. First-order gm-C lowpass, current-tunable.** One linearized transconductor from exercise 2, with capacitance at the outputs and a CMFB. Corner frequency is f_c = gm/(2πC) with gm ∝ I in weak inversion. So f_c is linear in the bias current over decades: wire `igmc` to a DAC current (PUDDING is the obvious one) and you have a digitally tunable filter without a single resistor. On the capacitor (no MIM in this process):
- The cheapest flat-enough option is a thick-oxide NMOS from each output to vss, kept in strong inversion. The outputs never drop below about 1.15 V, which is well above V_th, so C ≈ C_ox within a few percent.
- PMOS caps from each output to vdd sit in inversion too. Their C(V) slope is opposite, so a mixed pair cancels some of the first-order variation. The price is that they couple vdd noise straight onto the signal, so NMOS to vss is the better default for PSRR.
- An anti-parallel pair across outp/outn cancels even-order distortion from the capacitor and leaves third-order.

Measuring f_c against current is a clean first-silicon experiment.

**4. Continuous-time comparator with hysteresis.** A differential pair into cross-coupled loads, with a positive-feedback ratio set by W ratios or current ratios. Hysteresis comes from geometry, not from a resistor network. Differential analog in, one digital bit out to `dig_out` through a level shifter (3.3 V to 1.2 V; also a small exercise). Sweep vin slowly through the S2D and you measure offset and hysteresis from the switching points. It's also the gentlest introduction to mismatch, which leads to the next idea.

**5. A Pelgrom array instead of a single circuit.** Sixteen or thirty-two identical small differential pairs, each selectable through gate-only switches, all feeding one comparator or one gm/gm stage. Students sweep the S2D input, record each pair's offset and plot σ(ΔV_th) against 1/√(WL) across two or three device sizes. They reproduce Pelgrom's plot on their own silicon. No passives at all, almost no design risk, and it teaches the thing beginners most underestimate. It's also directly useful to everyone else on the shuttle, because it's mismatch data for sg13cmos5l thick-oxide devices at nanoampere currents. I'm not aware of public data for that regime in this process.

## Intermediate exercises

**6. Current-mode signal processing between the pads.** Convert the differential input to a differential current once (exercise 2), then do everything with mirrors:
- Gain from W ratios.
- Summing at a node.
- Inversion by swapping wires.
- Full-wave rectification by steering the difference current |I₊ − I₋| through a mirror pair (an absolute-value circuit).

Convert back to voltage with a diode-connected load at the end. The rectifier is the gateway to on-chip envelope and amplitude measurement, with no diodes and no sample-and-hold.

**7. Quadrature oscillator with continuous amplitude control.** Your planned gm-C stage: two integrators in a loop, with a small negative-resistance gm (cross-coupled pair) to start it. Amplitude can be limited simply by the transconductors' own saturation, which is continuous-time and crude, with a lot of distortion. The intermediate version measures amplitude continuously: rectify both quadrature outputs with exercise 6, sum them, and compare against a reference current. The integrated error controls the negative-resistance current. That's an AGC loop with no clock and no chopper, and students meet loop stability, because amplitude loops oscillate in their own right.

The advanced version takes √(x² + y²) with a translinear circuit instead of the sum of rectified values. That gives a constant-amplitude measure with ripple at neither f nor 2f.

**8. Gilbert multiplier / modulator.** Two differential inputs, one differential output. On this die, one input comes from the pad through the S2D and the other from the internal oscillator. Output through the D2S is an AM or DSB-modulated version of whatever the student feeds in, visible on a USB scope as a spectrum, which is a satisfying first-silicon demo. In weak inversion the multiplier is exactly tanh·tanh, so exercise 2's linearization tricks apply again on both ports. A squarer variant (both inputs tied) plus a lowpass is an RMS detector, a second route to exercise 7's amplitude measurement.

**9. Current-ratio-controlled VGA.** An input transconductor gm₁ and a feedback or load transconductor gm₂, with gain gm₁/gm₂ = I₁/I₂ in weak inversion. Two DAC currents make a programmable-gain stage with no switched resistor ladder. Matched units on both sides, the way your DDA does it, make the gain insensitive to the linearization method, because the nonlinearity cancels. That's a deliberate echo of the pad buffers, so students see the same principle at both ends of the signal chain.

**10. Common-mode translator into the 1.2 V domain.** A differential stage whose input CM is 1.65 V on thick oxide and whose output CM is about 0.6 V for a thin-oxide 1.2 V block. Students design a thick-oxide/thin-oxide boundary and two CMFB loops at different references, and learn which devices may see which voltages. Useful in practice: it's the analog counterpart to the digital level shifters the harness already needs. Someone's later 1.2 V ADC or neuromorphic array could then sit behind the same pads.

## Into the advanced, and the neuromorphic corner

**11. Bump circuit and winner-take-all.** Delbrück's bump circuit takes two voltages and gives a current that peaks when they're equal: a similarity measure in a few transistors. Lazzaro's winner-take-all picks the largest of N input currents, with the losers' currents dropping exponentially. Both are weak-inversion translinear circuits with no passives, they connect directly to the Telluride lineage, and they read out naturally through the CM readout and D2S path. A two-input WTA driven differentially (inp vs inn) is a soft comparator whose sharpness students set with one bias current.

**12. Log-domain / companding integrator.** Frey's log-domain filters and Seevinck's companding current-mode integrator: compress, integrate on a capacitor, expand, so the capacitor sees a small voltage swing while the signal current spans decades. That sidesteps the MOS-cap linearity question from exercise 3, because the cap's voltage swing stays small. Hard: it lives entirely on the exponential law and matching. But it's the most on-chip-native filter imaginable, and the result is measurable through the same pads.

**13. Low-noise high-impedance front end.** The opposite end of the spectrum: an exercise in noise rather than linearity. Very high input impedance, a pseudo-resistor DC path (MOS-bipolar pseudo-resistors in the Harrison–Charles style, no linear R), and gain from a ratio of small capacitors. That last part brushes against the no-passives rule. Keep the total capacitance near 1 pF, and treat the cap ratio as the one place where matched on-chip capacitors (MOM or inversion-mode MOS) are the right tool rather than an off-chip habit. Input-referred noise measured through the S2D/D2S chain with an internal input short is the deliverable. You know this territory better than any exercise sheet could. It would make a good capstone.

## Loose threads

- Every exercise above has the same measurement story: static DC sweeps through the S2D or the ladder, slow sines from a USB generator, and readout through the D2S or a comparator bit. That consistency is the actual product. Students learn the socket once and move between exercises, and the pad buffers' own test circuit (the pass-through, the CM readout, the input short) doubles as the de-embedding fixture for every student block.
- The two numbers a student most needs on day one are the socket swing (±0.5 V per side) and the sub-µA bias regime. Both push them away from textbook strong-inversion square-law design, which is where the deeper lesson is: geometry and current ratios, the exponential law, matching. The things that are accurate on chip, rather than the things that are accurate on a breadboard.
- A gentle first-silicon kit would be exercises 1, 3, 4 and 5: a gain stage, a tunable filter, a comparator and a mismatch array. All four share one linearized transconductor cell and one CMFB, and together they cover gain, time constants, decisions and statistics.
- An open question for Tim and the Chipalooza crowd: does a standard analog socket definition belong in the harness documentation, alongside the XSPICE boundary stub already proposed in TOP_LEVEL_MODULE.md? Probably yes.

## References (from memory, not re-checked)

- F. Krummenacher and N. Joehl, "A 4-MHz CMOS continuous-time filter with on-chip automatic tuning," IEEE JSSC, 1988.
- T. Delbrück, "Bump circuits for computing similarity and dissimilarity of analog voltages," IJCNN, 1991.
- B. Gilbert, "The multi-tanh principle: a tutorial overview," IEEE JSSC, 1998.
- R. Sarpeshkar, R. F. Lyon and C. Mead, "A low-power wide-linear-range transconductance amplifier," Analog Integrated Circuits and Signal Processing, 1997.
- M. J. M. Pelgrom, A. C. J. Duinmaijer and A. P. G. Welbers, "Matching properties of MOS transistors," IEEE JSSC, 1989.
- J. Lazzaro, S. Ryckebusch, M. A. Mahowald and C. A. Mead, "Winner-take-all networks of O(N) complexity," NIPS, 1989.
- D. R. Frey, "Log-domain filtering: an approach to current-mode filtering," IEE Proceedings G, 1993.
- E. Seevinck, "Companding current-mode integrator: a new circuit principle for continuous-time monolithic filters," Electronics Letters, 1990.
- R. R. Harrison and C. Charles, "A low-power low-noise CMOS amplifier for neural recording applications," IEEE JSSC, 2003.
- E. Säckinger and W. Guggenbühl, "A versatile building block: the CMOS differential difference amplifier," IEEE JSSC, 1987.
