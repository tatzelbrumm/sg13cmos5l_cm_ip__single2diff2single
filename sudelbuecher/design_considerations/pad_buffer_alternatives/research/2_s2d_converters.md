# Search 2 — single-ended → differential pad input buffer, IHP SG13CMOS5L (agent report, verbatim)

## 0. Two things that frame every candidate

**Headroom arithmetic (my own analysis, not from a source).** With voutp − voutn = 2·(vin − vref) around 1.2 V CM and each output moving ±(vin − vref), the output stage can only swing to ~0.2 V and ~2.9 V on a 3.3 V rail, so |vin − vref| ≤ ~1.0–1.2 V. A "full 0–3.3 V pad range" is therefore unreachable at gain 2 and 1.2 V CM whatever the input stage does; the realistic target is "input stage tolerates any pad DC level (0–3.3 V) without latching or losing bias" plus a linear window of vref ± ~1.1 V. The candidates below are judged on that.

**IHP resistor spread (process spec page).** Rhigh sheet 1160/1360/1560 Ω/sq (±15 % absolute), TC1 −2300 ppm/K; Rppd 235/260/285 Ω/sq (±10 %), TC1 170 ppm/K; MIM 1.35/1.5/1.65 fF/µm² (sg13g2 only — not in your cmos5l flavour). HV-NMOS Vt 0.63/0.70/0.77 V, HV-PMOS −0.71/−0.65/−0.59 V, HV oxide ≈ 7.3–7.5 nm ([IHP process control params](https://ihp-open-pdk-docs.readthedocs.io/en/latest/process_specs/02_process_control_params.html)). Resistor *ratio* matching is not published there; the absolute spread only hurts resistor-defined bandwidths, not gain ratios.

---

## 1. Resistor-free (MOS-only) candidates — ranked first

### C1. Two unity-gain DDAs instead of one gain-2 FDDA (Säckinger/Guggenbühl DDA, Alzaher FBDDA)
**Topology.** A DDA with inputs (Vpp, Vpn, Vnp, Vnn) and feedback forces (Vpp − Vpn) = (Vnp − Vnn); Säckinger & Guggenbühl (JSSC 1987) showed gain is set purely by the two matched transconductors, and nonlinearity cancels when both pairs see the *same* differential swing. Alzaher/Elwan/Ismail's fully balanced DDA (1.2 µm CMOS, class AB, fabricated) extends this to differential outputs and claims "wide input range without complex extra circuitry" ([KFUPM record](https://eprints.kfupm.edu.sa/id/eprint/849), [IEEE 943332](https://ieeexplore.ieee.org/document/943332/)).
**Why it matters here (my analysis).** Your target is two unity-gain differences: voutp − vcm = vin − vref and voutn − vcm = vref − vin. Each is a textbook unity-gain DDA (2 pairs each → 4 pairs total, no CMFB because vcm is applied explicitly). Both pairs in each DDA see identical swings, so the 150 kΩ degeneration you used to linearize a gm *ratio* of 2 is no longer needed — only matching. That is the resistor-free route the DDA literature actually supports.
**Numbers.** 1987/2001 papers give no area/bandwidth usable for 130 nm; none of the fetched records state supply, power or area.
**Resistors:** no. **Large caps:** no.
**Main limitation.** Undegenerated pairs fully steer beyond ≈ √2·Vov; when |vin − vref| exceeds that, both pairs saturate equally (output error stays zero) but loop gain collapses → slow/unstable settling. Needs large Vov (strong inversion, low gm/I) or triode-MOS degeneration, and complementary pairs (see C9) for pad DC levels outside the PMOS window.

### C2. Inverter-based fully differential difference transconductor (FDDTA)
**Topology.** Eight CMOS inverters: four form the input DDA pairs, four control outputs; pseudo-differential, no tail, no CMFB, no calibration. Gain is Gm ratio of matched inverters.
**Numbers (MDPI Electronics 2023).** GF 130 nm, **0.25 V supply**, weak inversion, Gm 2.26 µS, open-loop 28.2 dB, GBW 480 Hz (30 pF), measured buffer cutoff 3.2 kHz, 75 nW; MC gain mean 27.78 dB; corners 22–29 dB; area not stated ([MDPI 12/4/963](https://www.mdpi.com/2079-9292/12/4/963)).
**Resistors:** no. **Large caps:** no.
**Limitation.** Everything scales to 3.3 V only in principle; inverter gm is set by supply and Vt (±0.07 V here), so the CM point and loop gain drift strongly; the paper's bandwidth numbers are irrelevant at 3.3 V. Pseudo-differential → CMRR 55 dB, PSRR 37.5 dB.

### C3. Pseudo-differential OTA with common-mode feed-forward + inherent CM detector (Mohieldin, Sánchez-Sinencio, Silva-Martínez, JSSC 2003)
**Topology.** No tail current; input currents are copied to build a CM feed-forward and the next stage's input serves as the CM detector. Fully balanced, transistor-only.
**Numbers.** 0.5 µm CMOS, 1.65 V, OTA CMRR 58 dB, HD3 −43 dB at 900 mVpp/30 MHz, 9.8 nV/√Hz; demonstrated in a 100 MHz filter at 42.9 mW/pole pair; per-OTA area not given ([ResearchGate abstract](https://www.researchgate.net/publication/2982201_A_fully_balanced_pseudo-differential_OTA_with_common-mode_feedforward_and_inherent_common-mode_feedback_detector)).
**Resistors:** none described. **Large caps:** no.
**Limitation.** CMRR only ~58 dB, and the input CM range is that of a tail-less pair (gate must be ≥ Vt above the source rail), so pad DC levels near the opposite rail cut the stage off.

### C4. Transistor-only CMFB (triode-MOS replaces the sense resistors)
**Topology.** Folded-cascode OTA where the CM-sense degeneration resistors R_S are replaced by triode MR1–MR4; no separate error amplifier.
**Numbers (MDPI Electronics 2021).** 0.18 µm, 1.2 V, post-layout. CMFB power 0 µW vs 0.6 µW for the DDA-CMFB; total amplifier 0.022 mm² vs 0.035 mm² (−37 %); one passive R_S alone needs ≈ 900 µm²; CM loop gain ≈ 100 dB; CM-loop BW 190–633 kHz; the equivalent R quoted inconsistently (550 kΩ / 275 kΩ). Table 1 lists a standalone CMFB at 0.003 mm² ([MDPI 10/2/145](https://www.mdpi.com/2079-9292/10/2/145)).
**General data.** Lecture notes classify detectors: resistive (linear, loads the amp), triode-MOS (upper limit Vdd − VT, replica-biased), differential-pair (does not load but linearity set by the pair), floating-cap ([IITM EE539](https://www.ee.iitm.ac.in/~nagendra/EE539/200601/lectures/20060418.pdf)). Duque's MC study of a folded-cascode with different CMFB loops: resistive degeneration gave CM-conversion mean/σ/worst 11.5/10.9/23.6 dB, current-steering variants up to 22/9.6/36 dB, THD 0.007–0.22 % ([TAMU CMFB detectors](https://people.engr.tamu.edu/s-sanchez/CMFB%20detectors%20Duque.pdf)).
**Resistors:** no. **Large caps:** no.
**Limitation.** Nonlinear detector → CM-to-DM conversion at your ±1.2 V output swing; the triode detector's range ends at Vdd − VT. Note: if you adopt C1, CMFB disappears entirely.

### C5. Switched-capacitor S2D (capacitor-ratio gain)
**Topology.** Fully differential integrator/amplifier where four extra switches route the single-ended input into both halves; gain = Cs/Ci (US 5,220,286) or ≈ 2·Cinn/Cintn (US 11,095,303, with explicit note that mismatch between the sampling caps gives offset and gain error; chopping/DEM proposed).
**Numbers.** Patents: 1 MHz+ clocks, 5 V switches; no area ([US5220286](https://patents.google.com/patent/US5220286), [US11095303](https://patents.google.com/patent/US11095303)).
**Resistors:** no. **Large caps:** moderate (two sampling + two integrating).
**Limitation.** Discrete-time only (settling per clock phase), needs a clock and non-overlap generator; with MOS caps only, the caps must stay in accumulation/strong inversion over the whole 0–3.3 V input swing, which they will not at the sampling node — linearity and gain accuracy collapse unless the input is pre-attenuated. No published MOS-cap-only S2D with figures was found.

### C6. Pseudo-differential: unity buffer + inverting path
**Topology.** voutp = vin level-shifted, voutn = 2·vcm − vin from a second, inverting cell (ADI's discrete recipe uses an op-amp inverter; Philips EP0601646 does it with four transistors, two diode-connected). Super-source-follower / FVF buffers give the non-inverting half MOS-only.
**Numbers.** EP0601646: no numbers ([EPO](https://data.epo.org/publication-server/rest/v1.2/patents/EP0601646NWA1/document.html)); ADI note is discrete-level ([ADI pseudo-differential](https://www.analog.com/en/resources/technical-articles/adc-driving-pseudo-differential-unipolar-inputs.html)).
**Resistors:** inverting half needs matched R or a gm-defined inverter. **Large caps:** no.
**Limitation.** Gain error = mismatch of two different signal paths (follower Vgs shift ±Vt spread vs. inverter gm), CM is not regulated, and the two paths' delays differ → phase error above a few MHz. A resistor-free variant exists (EP0601646) but is only accurate for small signals.

---

## 2. Active baluns / RF S2D (mostly AC-coupled; listed for completeness)

### C7. Two-stage NMOS-pair balun with balancing capacitor (US 6,566,961)
Diff pair M1/M2 with input AC-coupled to one gate, reference AC-coupled to the other; a capacitor C_D equal to the tail parasitic splits the input equally; second DC-coupled pair with cross-coupled feedback caps. 0.35 µm HSPICE only: 0.0002 dB/0.0007° at 100 kHz, 0.0128 dB/0.1475° at 1 GHz, 7.9 dB gain; load resistors R_L; **AC-coupled input** ([US6566961](https://patents.google.com/patent/US6566961)). Resistors: yes (loads, bias). Not DC; no resistor-free variant with these balance numbers.

### C8. Differential pair with CM-sensing feedback pair (Bologna, SiGe BiCMOS7)
Second pair senses the common-emitter node and drives the "grounded" input; >5 dB gain increase, measured −3 dB 7.2 GHz, DC feedback loop (tested with off-chip loop); collector resistors; no area/power ([amsacta 1302](https://amsacta.unibo.it/1302/1/GA051975.PDF)). Also a Twente SiGe cell with ~6 dB conversion-gain increase ([UTwente](https://research.utwente.nl/en/publications/single-to-differential-converter-3/)). The 0.0058 mm² inductor-less CMOS balun (DC–8 GHz, −0.1 ± 0.2 dB, −0.18 ± 1.17°) could not be fetched; numbers are from its title only ([ResearchGate listing](https://www.researchgate.net/publication/369428412_A_00058-mm_Inductor-Less_CMOS_Active_Balun_With_Gain_and_Phase_Errors_Within_-01_02_dB_and_-018_117_From_DC_to_8_GHz)). A 40 nm cross-coupled S2D TIA: core 39 × 26 µm (0.001 mm²), 4.15 GHz, 7.84 mW, uses R_F/C_F networks ([MDPI 10/23/3042](https://www.mdpi.com/2079-9292/10/23/3042)).
**Limitation for you.** A balun's "DC" rating means no coupling cap, not a 0–3.3 V input DC range; CG inputs sit at a fixed source bias; gains are gm·R_L. Rank last.

---

## 3. Current conveyors

### C9. FDCCII / DVCC-based S2D
Six-terminal fully differential CCII, 23 transistors, class-AB FD buffer core; 0.25 µm, ±1.5 V, DC range ±1 V, V_Zd/V_Yd −3 dB 82 MHz; power and area not stated; all demonstrated applications use kΩ resistors (1.3–10 kΩ) and nF caps ([JOS FDCCII](https://www.jos.ac.cn/article/shaid/73242e21716a8fe5ca7d1bb6ed6a79489074a3af1f558b425a2454bd848b52e7)). DVCC-based instrumentation amps set gain by R2/R1 ([IEEE 4633384](https://ieeexplore.ieee.org/document/4633384/)).
**Resistors:** yes for any V-out (X-node current must be converted at Z). **Resistor-free variant:** only with diode-connected (nonlinear) loads — none published with numbers. Rank below C1–C4.

---

## 4. Rail-to-rail input stages for the pad DC range at 3.3 V

### C10. Complementary N+P pairs with constant-gm control (Hogervorst et al., JSSC 1994)
1 µm BiCMOS, 3 V (2.5–6 V), Vt 0.64/−0.75 V (close to your HV devices); gm variation ≈ 15 % over CM range with 3× current-mirror switching (factor 2 without); GBW 2.6 MHz (Miller) / 6.4 MHz (cascoded Miller) at 10 pF; 180 µA, 0.5 mW; **die area 0.04 mm²** for the whole 2-stage op amp; 1 % settling 220/180 ns small-signal, 440/275 ns for 1 V step; CM range 0.4 V below VSS to 0.5 V above VDD ([TU Delft repository](https://repository.tudelft.nl/file/File_0fc107fa-6796-4bae-9159-8537a431f171)). Resistors: none essential. Large caps: Miller 10 pF-class loads. Cost in your design: doubling of input pairs (4 → 8 pairs in a C1 implementation) plus the current switch; the 15 % gm swing changes loop gain/settling, not closed-loop gain.

### C11. Single pair + switched level shifters (Valero et al., ISCAS 2015)
One differential pair; switched voltage followers add a DC shift when CM drops below headroom; tail current made CM-insensitive; 0.5 µm, ±1.65 V, <20 % extra power; gm variation and area not quantified ([Bath](https://researchportal.bath.ac.uk/en/publications/constant-gm-rail-to-rail-cmos-opamp-with-only-one-differential-pa/)). Resistor-free; fewer pairs than C10 but the shifted path adds noise/offset and a mode switch.

### C12. Bulk-driven FD input stages
All retrieved work targets 0.25–0.5 V supplies (0.3 V FD buffer; 0.3 V rail-to-rail OTA; comparative analysis) ([JLPEA 12/3/35](https://www.mdpi.com/2079-9268/12/3/35), [Electronics 14/10/2085](https://www.mdpi.com/2079-9292/14/10/2085)); page content for area/bandwidth was not retrievable. At 3.3 V the bulk node cannot follow a 0–3.3 V pad without forward-biasing the well junction, and gm_b is a fraction of gm. Not viable here; listed only because requested.

---

## 5. Resistor-based reference point

### C13. Resistive-feedback FDA (ADC-driver style)
Summing nodes sit at the amplifier's input CM regardless of the pad voltage (input range limited only by Rg/Rf divider → the only topology that truly accepts 0–3.3 V at the pad); gain = Rf/Rg ratio, immune to the ±15 % absolute Rhigh spread above. Commercial parts (AD8476 etc.) give no die area ([AD8476](https://www.analog.com/media/en/technical-documentation/data-sheets/AD8476.pdf)). Closest open implementation: **sg13cmos5l FD class-AB op amp** (same PDK) — 1.5 V, PMOS pair 2.5/2 µm m=8 (input gate area 320 µm²), Miller R_C 23.97 kΩ + MOScap 3.5 × 21.5 µm, resistive CMFB R1 = R2 = 29.89 kΩ + error OTA, 2.5 µA bias, 40 dB, GBW 40–50 MHz (0.1 pF), CM range 0.3–1.2 V, output 0.1–1.3 V, CMRR 97.5 ± 11.3 dB (100 MC); total layout area not given ([YacineSot repo](https://github.com/YacineSot/sg13cmos5l_yacinesot_ip__diff_opamp_cmfb)). Current-feedback IAs reduce but do not eliminate resistors: Martins 1998 (2.4 µm, 500 µA, 99 dB CMRR, gain 1/Rg·Rr) ([TU Wien](https://www.iue.tuwien.ac.at/pdf/ib_1999/JB1998_Martins_1.pdf)); 2020 CFIA 0.35 µm, 3 V, 9.6 µA, 34 dB, 8.8 kHz, few-kΩ degeneration ([Springer](https://link.springer.com/article/10.1007/s00034-020-01527-2)); Google patent US 9,806,703 does S2D with one op amp and six resistors, no caps ([US9806703](https://patents.google.com/patent/US9806703)).
**Resistor-free variant:** replace Rf/Rg by MOS caps (needs reset/DC servo → not DC) or by gm-ratio feedback → C1.

---

## 6. Open-source designs with layout data
- sg13cmos5l FD op amp (above) — closest match, Chipalooza-submitted, DRC/LVS clean, no area figure.
- NethmalWDI FD op amp: sky130 sim / IHP layout, folded cascode + CS, diff-pair CMFB on stage 1 and resistive CMFB on stage 2, targets 80–120 dB and 0.8–1.2 MHz; no current/area ([GitHub](https://github.com/NethmalWDI/Fully_differential_opamp)).
- 2AMLogic sky130 USB2 differential receiver (5 V devices, L = 0.5 µm): 9.7–80 µA over 45 PVT corners at 0.8/1.65/2.5 V CM, one xhigh poly bias resistor, no layout ([PR #122](https://github.com/2AMLogic/sky130-usb2-phy/pull/122)).
- TinyTapeout gf180 3.3 V folded-cascode OTA: single-ended, ~100 kHz GBW, ~15 µA, external 2 MΩ bias, no area ([TT](https://tinytapeout.com/chips/ttgf0p3/tt_um_LPCAS_TTGF0P3_TP1/)).
No open-source S2D with a published µm² figure was found.

---

## 7. Ranking against your targets (<6500 µm², >5 MHz, widest DC input, MOS-only)
1. **C1** two unity-gain DDAs (4 pairs, no CMFB, no resistors) — the only resistor-free scheme the literature supports for an accurate gain; add **C10** N+P pairs if pad levels outside vdd − 1.3 V must stay regulated.
2. **C4** transistor-only CMFB — if you keep an FDDA.
3. **C13** resistive FDA — best input range and accuracy, but resistors.
4. **C3**, **C11**, **C2** — compact but weak CMRR/PSRR or supply-sensitive gain.
5. **C5** SC, **C9** CCII, **C6** pseudo-diff, **C7/C8** baluns — not DC-accurate or not resistor-free.

Numbers not found anywhere: layout area for any CMOS S2D below 0.35 µm with DC input range; DDA S2D settling/bandwidth in a modern node; resistor ratio matching for IHP Rhigh.

## Sources
- https://ihp-open-pdk-docs.readthedocs.io/en/latest/process_specs/02_process_control_params.html
- https://eprints.kfupm.edu.sa/id/eprint/849
- https://ieeexplore.ieee.org/document/943332/
- https://www.mdpi.com/2079-9292/12/4/963
- https://www.researchgate.net/publication/2982201_A_fully_balanced_pseudo-differential_OTA_with_common-mode_feedforward_and_inherent_common-mode_feedback_detector
- https://www.mdpi.com/2079-9292/10/2/145
- https://www.ee.iitm.ac.in/~nagendra/EE539/200601/lectures/20060418.pdf
- https://people.engr.tamu.edu/s-sanchez/CMFB%20detectors%20Duque.pdf
- https://patents.google.com/patent/US5220286
- https://patents.google.com/patent/US11095303
- https://data.epo.org/publication-server/rest/v1.2/patents/EP0601646NWA1/document.html
- https://www.analog.com/en/resources/technical-articles/adc-driving-pseudo-differential-unipolar-inputs.html
- https://patents.google.com/patent/US6566961
- https://amsacta.unibo.it/1302/1/GA051975.PDF
- https://research.utwente.nl/en/publications/single-to-differential-converter-3/
- https://www.researchgate.net/publication/369428412_A_00058-mm_Inductor-Less_CMOS_Active_Balun_With_Gain_and_Phase_Errors_Within_-01_02_dB_and_-018_117_From_DC_to_8_GHz
- https://www.mdpi.com/2079-9292/10/23/3042
- https://www.jos.ac.cn/article/shaid/73242e21716a8fe5ca7d1bb6ed6a79489074a3af1f558b425a2454bd848b52e7
- https://ieeexplore.ieee.org/document/4633384/
- https://repository.tudelft.nl/file/File_0fc107fa-6796-4bae-9159-8537a431f171
- https://researchportal.bath.ac.uk/en/publications/constant-gm-rail-to-rail-cmos-opamp-with-only-one-differential-pa/
- https://www.mdpi.com/2079-9268/12/3/35
- https://www.mdpi.com/2079-9292/14/10/2085
- https://www.analog.com/media/en/technical-documentation/data-sheets/AD8476.pdf
- https://github.com/YacineSot/sg13cmos5l_yacinesot_ip__diff_opamp_cmfb
- https://www.iue.tuwien.ac.at/pdf/ib_1999/JB1998_Martins_1.pdf
- https://link.springer.com/article/10.1007/s00034-020-01527-2
- https://patents.google.com/patent/US9806703
- https://github.com/NethmalWDI/Fully_differential_opamp
- https://github.com/2AMLogic/sky130-usb2-phy/pull/122
- https://tinytapeout.com/chips/ttgf0p3/tt_um_LPCAS_TTGF0P3_TP1/
