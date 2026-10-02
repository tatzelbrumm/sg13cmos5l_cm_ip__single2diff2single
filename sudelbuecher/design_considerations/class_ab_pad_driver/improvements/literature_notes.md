<!--
SPDX-FileCopyrightText: 2026 Christoph Maier
SPDX-License-Identifier: Apache-2.0
-->
# Literature notes for the class-AB pad driver revision

This file indexes the sources and does not copy them (chatlog/ref rule). Paths are relative to
`~/DoNotLitter`. Thesis page numbers are the printed ones. For each source the note gives what
it contributes and how that held up against SG13CMOS5L simulation (`sim/results_improvements.txt`).
Text came from `pdftotext` on the linked computer. Sarpeshkar 1997 is a scan with no text layer,
so its chapter 3 was OCR'd locally with tesseract. The CaltechTHESIS copy
(thesis.caltech.edu/3063) is the same scan, so it did not help.

## Wide linear range and degeneration

**R. Sarpeshkar, *Efficient Precise Computation with Noisy Components: Extrapolating From an
Electronic Cochlea to the Brain*, PhD thesis, Caltech, 1997, ch. 3 "A Low-Power
Wide-Linear-Range Transconductance Amplifier"** (`Sarpeshkar_R_1997.pdf`, scan)

- pp. 24–33: the linear range is widened by four techniques that need no resistor: well (bulk)
  input, source degeneration by a diode, gate degeneration through the current-mirror diode,
  and bump linearization. Bump linearization with a ratio w = 2 cancels the cubic term (eq. 3.15).
  In 2 µm subthreshold the result is ±1.7 V.
- p. 25 makes the point for the strong-inversion case: above threshold, identities of the form
  (x − a)² − (x − b)² = (b − a)(2x − a − b) make a wide linear range easy to get. This is the
  square-law cancellation behind the ELIN discussion in the proposal.
- §3.3.1, p. 33: below about 1 V of input, the well input turns on the parasitic vertical
  bipolar. §3.7.1: κ depends on the well-to-gate voltage, so Gm depends on the input common
  mode.
- §3.3.4, pp. 36–38: the voltage offset equals the current mismatch divided by the
  transconductance, so a low Gm/I is offset-prone. The mirrors matter most and the input
  transistors least.
- §3.5, pp. 41–49: when thermal noise dominates, a wider linear range buys dynamic range at a
  proportional cost in power. Bump linearization does not add noise. §3.5.4: the well input is
  an implicit capacitive divider. Explicit dividers need floating-gate adaptation, and the
  parasitic capacitances hurt them.
- **In this design:** the well-input unit (`unit_w`) is linear, at 6.8 % compression at
  0.5 V. Its Gm changes by −27 %/V with the input common mode, though, which is exactly the
  §3.7.1 effect. In the matched-pair DDA that becomes a second-order error of +29 / +38 mV at
  ∓0.5 V. The offset analysis of §3.3.4 predicted the measured offset budget: the folding
  sinks were 11.5 mV of the 14.4 mV.

**P. Hasler, PhD thesis (Caltech), ch. 1–6** (`FloatingGate/Hasler/thesis_chapter*.ps`)

- Ch. 4 covers continuous-time feedback in floating-gate MOS circuits, including the
  source-degenerated pFET synapse. Ch. 5 is the autozeroing floating-gate amplifier (AFGA):
  capacitive feedback, with tunneling and pFET hot-electron injection setting the DC point.
- Ch. 5, eq. 5.27: the input linear range scales as U_T·(C1 + C2 + C_w)/C1 (times a correction
  factor B between ½ and 1), so it grows with the capacitive division.
- **In this design:** not applicable. It needs linear capacitors (MOM, which is what we are
  trying to avoid), charge control from tunneling and injection voltages that a 3.3 V slot
  does not have, and an AC-coupled signal, whereas the pad driver must be DC-coupled.

**E. Sánchez-Sinencio, "Floating Gate Techniques and Applications", lecture slides, TAMU**
(`FloatingGate/607-2005-Floating Gate Circuits.pdf`); **A. J. Montalvo, J. J. Paulos,
"Improved floating-gate devices using standard CMOS technology", IEEE EDL 14(8), 1993**
(`FloatingGate/225583.pdf`)

- Multiple-input floating-gate (MIFG) differential pairs widen the linear range at the price
  of a lower gm. They need the trapped charge handled, by UV or by programming.
  Montalvo/Paulos program by injection and FN tunneling below junction breakdown, in a
  double-poly process.
- **In this design:** not applicable, for the same reasons as Hasler's AFGA. SG13CMOS5L has no
  poly-poly capacitor either.

## Externally linear, internally nonlinear (ELIN)

**R. T. Edwards, PhD thesis (Johns Hopkins), §3.5–3.10** (`TimEdwards/thesis.pdf`);
**R. T. Edwards, G. Cauwenberghs, "Synthesis of log-domain filters from first-order building
blocks", Analog Integr. Circ. Sig. Process. 22, 177–186, 2000**
(`LogDomain/EdwardsCauwenberghs.AnalogIC_SigProc.2000.pdf`, `LogDomain/aicsp00_log.pdf`);
**R. T. Edwards, G. Cauwenberghs, "A second-order log-domain bandpass filter for audio
frequency applications", ISCAS 1998** (`TimEdwards/iscas98_log.pdf`)

- Thesis p. 72 defines ELIN and names two usable internal nonlinearities: the square law of
  strong inversion (ref. [37], Wiegerink, *Analysis and Synthesis of MOS Translinear
  Circuits*) and the exponential. Large-signal linearity holds as far as that nonlinearity
  dominates the device's other deviations.
- Thesis §3.9, p. 85: the MOSFET (subthreshold) log-domain versions had a noise floor the
  authors could not remove by design. The BiCMOS versions worked, with base-current
  compensation.
- Thesis §3.10, pp. 86–88: matching is dominated by "same surround" over a radius of 50–100 µm,
  more than by proximity or orientation.
- **In this design:** the matched-pair DDA is a static ELIN circuit. Its matching requirement
  is what makes §3.10 the layout rule for the four units. The exponential log-domain
  machinery itself is outside the brief, and the thesis's own MOS results argue against it.

**G. Efthivoulidis, Y. Tsividis, "Signal analysis of externally linear filters"**
(`LogDomain/EfthivoulidisTsividis.00780096.pdf`)

- Gives a test for external linearity: transform the nonlinear state equations into an
  externally equivalent linear system. Covers companding filters (instantaneous and syllabic).
  The examples are dynamic, not static.

**J. Mulder, A. C. van der Woerd, W. A. Serdijn, A. H. M. van Roermund, "General current-mode
analysis method for translinear filters", IEEE TCAS-I 44(3), 1997; "An RMS-DC converter based
on the dynamic translinear principle", IEEE JSSC 32(7), 1997** (`LogDomain/Mulder...pdf`);
**S. Hiseni, C. Sawigun, W. A. Serdijn, "Dynamic translinear nonlinear energy operator",
ECCTD 2009** (`LogDomain/HiseniSawigunSerdijn.ECCTD2009.pdf`)

- Dynamic translinear (exponential, bipolar or subthreshold) applied to filters and nonlinear
  ODEs. Relevant only as the dynamic counterpart of the static f⁻¹∘f principle used here.

## Multiple-input translinear elements, source followers

**B. A. Minch, *Analysis, Synthesis, and Implementation of Networks of Multiple-Input
Translinear Elements*, PhD thesis, Caltech, 1997** (`FloatingGate/Minch97.pdf`);
**B. A. Minch, "Multiple-input translinear element log-domain filters", IEEE TCAS-II 48(1),
2001** (`LogDomain/Minch.TCAS2.2001JAN.pdf`)

- The prolog lists "from negative feedback around a high-gain amplifier, we obtain function
  inversion". That is the static ELIN principle the matched-pair DDA uses.
- Ch. 7.2.1, pp. 197–199: a floating-gate source follower followed by an exponential element is
  a valid MITE even when the follower is biased above threshold, because a source follower's
  transfer does not depend on the form of the device's I–V law.
- **In this design:** that remark explains why the split-tail rhigh unit is the one unit that
  works in the matched-pair DDA. Each input device is a constant-current source follower, so
  the resistor sees gp − gn and nothing else. The MOS replacements fail because their element
  value depends on the absolute source voltage (`sim/results_improvements.txt`, section
  "DDA units").

## Read, not applicable to the pad driver

- `TimEdwards/jssc99_atp.pdf` (mixed-mode correlator for acoustic transient classification),
  `TimEdwards/defense.pdf`, `TimEdwards/potbox.pdf` (Pot Box Mark II test box, Stanford 1992),
  `TimEdwards/MEMS_pressure_sensor/`.
- `FloatingGate/Hasler/Energy-Efficient_Programable_Analog_Computing...pdf`,
  `FloatingGate/Hasler/jlpea-03-00073-with-cover.pdf` (dendritic wordspotting),
  `FloatingGate/Hasler/HaslerHistoryReflectionMay9_2020.pdf`: FPAA and floating-gate system
  context. They depend on the same programming infrastructure as above.
- `FloatingGate/tvhsac13.pdf` (Maliuk/Makris, analog ontogenic neural network for RF BIST).

## Cited from memory, not in DoNotLitter, not re-checked

- E. Säckinger, W. Guggenbühl, CMOS differential difference amplifier, JSSC 1987. The DDA's
  nonlinearities cancel when both pairs carry the same signal, which is the origin of the
  matched-pair idea.
- E. Seevinck, R. F. Wassenaar, square-law linear transconductor, JSSC 1987. Strong-inversion
  translinear (MOS square law).
- F. Krummenacher, N. Joehl, MOS-degenerated transconductor, JSSC 1988. Considered as a
  resistor replacement. It has the same source-voltage dependence as `unit_t`.
- A. Ahuja, indirect (current-buffer) compensation, JSSC 1983. Considered, not simulated; see
  the proposal.
