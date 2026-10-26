# Search 3 — wide-linear-range, resistor-free transconductors for a Gm-ratio DDA at 3.3 V / Vt ≈ 0.7 V (agent report, verbatim)

Scope note up front: the open-access sources I could reach are a mix of classic and recent papers; many flagship JSSC papers (Nauta 1992, Krummenacher 1988, Seevinck-Wassenaar 1987, Sackinger-Guggenbühl DDA 1987) are paywalled, so for those I quote what the reachable abstracts/surveys say and mark anything I derived myself as "my estimate". Numbers below are only those found in the fetched text; "not reported" means the source doesn't give it.

## 0. A framing result that constrains every candidate (my derivation, from the textbook large-signal pair formula)

For a class-A source-coupled pair the input turns one device off at Vid = √2·Vov (TAMU lecture slides, formula confirmed), and gm(0) = I_tail/Vov. So gm·V_range,peak ≈ √2·I_tail. For a resistor-degenerated pair, Gm ≈ 1/R and V_range ≈ I_tail·R, so Gm·V_range ≈ I_tail. **Any class-A pair, MOS-linearized or resistor-linearized, gives Gm ≈ (1…1.4)·I_tail / V_range.** With 5 µA per unit and ±0.75 V range, the ceiling is ≈ 7–10 µS; the existing 15 µS unit is already at the ceiling for split tails. Raising Gm at fixed range is a current decision, not a topology decision, **unless** the tail current grows with signal (class-AB / adaptive bias, candidates 5, 6, 10, 11). Linearization choice then decides *shape* (flatness of Gm), *headroom*, *area* and *noise*, not the Gm·range product.

Second framing point, specific to the DDA: the gain is Gm1/Gm2 from four matched units, so **absolute spread of Gm is harmless; only unit-to-unit mismatch and common-mode dependence matter.** That removes the main objection (bias spread) against triode-MOS degeneration and Nauta inverters in this application, and it makes the "CM-dependent Gm" error of the CFIA literature (Wu et al. 2012: 0.04 % with equal input/output CM vs 0.12 % with different CM) the thing to design against.

---

## 1. Resistor-free MOS linearization candidates

### C1. Plain source-coupled pair, strong inversion, large overdrive
- Principle: no linearization; choose Vov so that √2·Vov exceeds the needed ±range. Iout = Vid·√(βI_SS − β²Vid²/4), gm collapses to zero at Vid = √2·Vov ([TAMU ECEN474 lecture 9](https://people.engr.tamu.edu/spalermo/ecen474/lecture09_ee474_diff_amps.pdf)).
- Numbers: for ±1 V differential input you need Vov ≳ 0.7 V (at the edge gm is 0, so for ±10 % flatness you want Vov ≈ 1.5–2 V — my estimate, impractical). VGS = Vt + Vov ≈ 1.4–2.7 V.
- Resistors: no. Area: small (short L, modest W, since β must be *small* for large Vov).
- Limitation at 3.3 V/0.7 V: ±1 V at 10 % flatness is not reachable; ±0.5 V with Vov ≈ 0.5 V (VGS 1.2 V) is, leaving 3.3 − 1.2 − Vdsat,tail ≈ 1.8 V of CM range (not rail-to-rail). Noise is the best of all class-A options (no resistor, gm at full value). Mismatch of Vt is diluted by the large Vov (Pelgrom current-mismatch formula, below).

### C2. Cross-coupled quad / Seevinck–Wassenaar square-law transconductor (two pairs with fixed level shifts)
- Principle: two source-coupled pairs driven with input level-shifted by ±VB (floating sources or source-follower level shifters); the square-law terms cancel and Iout = K·VB·Vid, linear until a device cuts off. Nedungadi-Viswanathan (1984) and Seevinck-Wassenaar (1987) are the classic references; the IntechOpen survey ([Kuo 2010](https://cdn.intechopen.com/pdfs/9851.pdf)) lists them as "crossing-coupled multiple differential pairs" and notes they **work only for balanced input signals** and are "sensitive to PVT variations" ([Sánchez-Sinencio notes](https://people.engr.tamu.edu/s-sanchez/622%20OTA-C%20Filter%20Linearization.pdf)).
- Reported implementation with numbers — Klumperink/van der Zwan/Seevinck, EL 1989 ([PDF](https://icejive.el.utwente.nl/home/erick/Klumperink-CMOS%20Variable%20Transconductance%20Circuit%20with%20Constant%20Bandwidth-EL1989.pdf)): 5 µm CMOS, 5 V, tail 50 µA, THD < 0.2 % up to 1 V input swing, gm 620–930 µA/V tuned by a control voltage, bandwidth ≈ 9 MHz and independent of gm; input copied onto the square-law devices by matched pairs so VSB stays constant (no body-effect distortion). MOS-only; the 2 kΩ were only test loads.
- Resistors: no. Area: ≥ 2 pairs + level-shift pairs per unit.
- Limitation at 3.3 V: the level shift VB stacks on top of VGS (≈1.2 V) → input CM window shrinks by VB; "balanced input only" means the vout/vref port of the DDA (single-ended drive on one side) must be handled as a true differential pair, which it is in a DDA, so acceptable. Class-A, so the Gm·range ceiling of §0 applies.

### C3. Cross-coupled unbalanced pairs with compressive + expansive characteristics (Hill/Sun/Szczepanski 2000)
- Principle: two pairs, one with gain compression and one with gain expansion, biased so the sum is flat; a CMFB keeps CM ([Hertfordshire e-print](https://uhra.herts.ac.uk/id/eprint/12843/1/904239.pdf)).
- Numbers (2 µm MOSIS, simulated, 5 V): THD < 0.7 % at 1 Vpp differential across tuning, < 0.4 % at best bias; gm 166–575 µS; input range 1.2 V; -3 dB 373–435 MHz; integrated noise 253 µV (1–300 MHz); 8–41 mW.
- Resistors: no. Limitation: power-hungry in that version; the paper itself says cross-coupled schemes "pay a penalty in noise".

### C4. Multiple unbalanced pairs / "multi-tanh" in CMOS (three-pair, and the two-pair + adaptive bias variant)
- Principle: pairs with intentionally offset gm peaks are summed to flatten Gm (bipolar multi-tanh is the Gilbert version; in CMOS the offsets come from unequal W/L or unequal degeneration). Ibrahim & Onabajo ([NSF PAR](https://par.nsf.gov/servlets/purl/10519901)) use two pairs each with a resistor on one side plus adaptive tail bias: 0.13 µm, 0.6 V, gm 11.5 µA/V (reference pair 55.7 µA/V), HD3 −47.6 dB at 614 mVpp (reference −24.4 dB), range ≈ 4× the reference, 1.5 MHz unity gain, 184 µV integrated noise (reference 39.6 µV), 9.8 µW. They note the three-pair approach "needs more than two pairs, which raises power and creates multiple gm peaks".
- Resistors: that implementation yes (1 MΩ high-res poly, ≈ 50 × 25 µm each); the pure unbalanced-W/L version is resistor-free but then the peak spacing depends on √(β ratio) and Vt matching.
- Limitation: Gm penalty ≈ 5× and noise ≈ 4.6× in the reported version; flatness depends on matching the offsets. Headroom at 3.3 V is not the issue.

### C5. Adaptive biasing (tail current with a quadratic term in Vid)
- Principle: a squarer adds β·Vid²/4-type current to the tail so the √(…) term in C1 is cancelled; class-AB by construction (current rises with signal), which is the only way past the §0 ceiling.
- Numbers: Kuo's survey compares at equal Gm: adaptive bias 1.38 mW vs resistor degeneration 1.19 mW, and THD ≈ 31 dB worse than his triode design at 0.7 Vpp (my reading of his Fig. 15 ≈ −30 dB); he calls the square-law circuit "complicated and hard to implement" ([Kuo 2010](https://cdn.intechopen.com/pdfs/9851.pdf)). Thai journal paper reports only that it helps in weak inversion, no numbers ([CRMA J.](https://ph01.tci-thaijo.org/index.php/crma-journal/article/view/243140)).
- Resistors: no. Limitation: cancellation accuracy depends on squarer matching; residual HD3 of −30…−40 dB typical in reports.

### C6. Super class-AB / FVF-based pairs (López-Martín, Ramírez-Angulo, Carvajal)
- Principle: a flipped voltage follower makes a low-impedance node (≈ 1/(gm1·gm2·ro1)) that can source currents far above the bias current; pseudo-differential class-AB pairs and "super class-AB" (adaptive bias + local CMFB) are built on it ([Sánchez-Sinencio FVF lecture](https://people.engr.tamu.edu/s-sanchez/607%20Lect%205%20BB%20FVF.pdf), [Carvajal et al. FVF theory](https://observatorio-investigacion.unavarra.es/documentos/5f8e8e7a2999527b469fec5c?lang=eu)).
- Numbers (0.5 µm, ±1 V, IB 10 µA, CL 80 pF): THD at 0.9 Vpp/100 kHz −40 dB (class A) vs −56/−43/−41 dB for the three super-AB variants; GBW 200 kHz vs 725/410/470 kHz at 80–140 µW; another set: GBW 2.3–3.5 MHz, SR 10–20 V/µs, 140–220 µW, 0.054 mm². VDDmin = |Vtp| + 2·Vdsat.
- Resistors: the class-AB *pairs* no; the FVF-*degenerated* transconductor (§3) yes.
- Limitation at 3.3 V: none from headroom; the output current is a nonlinear (class-AB) function of input, so Gm is not flat — fine for an op-amp input stage inside a loop, poor as an accurate Gm unit for a Gm1/Gm2 ratio unless both ports use identical cells with identical CM.

### C7. Triode-MOS degeneration with tracking bias (Krummenacher–Joehl type)
- Principle: the degeneration "resistor" is one or two MOSFETs in triode whose gates follow the input gates, so their conductance tracks the input pair's bias. In Kuo's comparison the triode-degenerated pair (β1/β3 = 6.7) shows nonlinearity up to 1 % for Iout/I_SS < 80 %, 1.31 mW at equal Gm, THD ≈ 24 dB worse than his auxiliary-amplifier triode design at 0.7 Vpp ([Kuo 2010](https://cdn.intechopen.com/pdfs/9851.pdf)). The Krummenacher 1988 JSSC paper itself is paywalled; no further numbers obtained.
- The "spread problem": the degeneration conductance ∝ β(VGS − Vt) spreads with process. **For this DDA that spread cancels in Gm1/Gm2** as long as the four units are identical and sit at the same CM; it only moves loop bandwidth. What does not cancel is CM dependence (triode device Vds/Vgs shift with input CM), so port CMs should be equalized.
- Resistors: no. Area: much smaller than 150 kΩ of poly. Noise: like a resistor of the same conductance plus the pair's own.
- Limitation at 3.3 V: the triode devices need VGS − Vt > |Vds| across them; with Vt 0.7 V and a ±0.75 V source-to-source swing this forces Vov ≳ 0.8 V on the triode devices, i.e. VGS ≈ 1.5 V of CM headroom per side — fine at 3.3 V, not rail-to-rail.

### C8. Triode-input (constant-Vds) transconductor with auxiliary amplifier (Kuo 2009)
- Principle: input devices in triode, Vds pinned by a two-stage auxiliary amplifier, Gm ≈ β·Vds.
- Numbers (TSMC 0.18 µm, 1.8 V): linear input range 2.4 V (Table says 2.6 V), THD −60 dB at 0.7 Vpp/100 kHz, Gm 3.4–542 µS, 0.73–1.76 mW, 0.516 mm² chip; control voltage must stay in a 30 mV band ([Kuo 2010](https://cdn.intechopen.com/pdfs/9851.pdf)).
- Resistors: no. Limitation: large area and power for the auxiliary loops; Gm ∝ Vds is Vt-sensitive per Kuo; the extra loop adds a pole, bad for a 2 MHz Miller loop that you want to speed up.

### C9. Pseudo-differential pairs (no tail) with CM feed-forward cancellation
- Principle: each input device is a grounded-source square-law element; the CM square term is subtracted by a feed-forward path, the differential term is linear (square-law cancellation). Rezzi/Baschirotto/Castello: 1.2 µm BiCMOS, 3 V, THD −40 dB up to 1 Vpp at 10 MHz, 12–55 MHz filter, DR ≈ 60 dB ([IRIS Pavia](https://iris.unipv.it/handle/11571/104178)).
- Resistors: no. Area: small (no tail, no cascodes needed on the sources).
- Limitation: Gm ∝ (Vcm − Vt), so **Gm depends strongly on CM** — the worst property for a Gm-ratio DDA whose two ports sit at different CMs; CMRR is only as good as the feed-forward cancellation. At Vt 0.7 V, CM must be above ≈ 1 V.

### C10. Nauta inverter transconductor (and inverter-based DDTAs)
- Principle: a CMOS inverter is a transconductor with Gm ∝ (VDD − Vtn − |Vtp|) and, for βn = βp, square-law N/P cancellation gives a linear Vin→Iout law with no internal nodes; four more inverters set the CM and tune output resistance ([Nauta, EL 1990](https://ris.utwente.nl/ws/files/6511768/cmos_vhf.pdf)). Numbers from that paper (3 µm BiCMOS, CMOS part): Gm 0.35 / 1.06 / 1.38 mA/V at VDD 2.5 / 5 / 10 V; filter DR 68 dB (5 V) and 72 dB (10 V) at 1 % IM; a 0.5 % Gm mismatch gives DC gain ≥ 200. A 0.35 µm inverter-only OTA: 2.5 V, GBW 3.56 GHz (sim), THD 0.46 % at 2 Vpp differential output, 2.25 Vpp swing per output, Gm 72–108 µS for VDD 2–2.5 V, < 800 µW ([Barthélemy 2008](https://link.springer.com/doi/10.1007/s10470-008-9167-8)). An inverter-based fully-differential *difference* transconductance amplifier exists ([MDPI Electronics 2023](https://www.mdpi.com/2079-9292/12/4/963)): GF 130 nm, 0.25 V weak inversion, Gm 2.26 µS, THD 1.09 % at 175 mVpp, 75 nW — a topology proof, not a performance point. The Harish/Nauta LNTA paper states that inverter linearity relies on N/P derivative cancellation and is "sensitive to PVT variation", with sweet spots of limited benefit ([UTwente JSSC](https://ris.utwente.nl/ws/files/51806699/Harish_RF_Transconductor_Linearization_Robust_JSSC_main_final.pdf)).
- Resistors: no. Area: smallest of all (inverters only, no tails, no cascodes). Noise: best (gm of both N and P contribute).
- My estimate for 3.3 V / Vt 0.7 V: linear region until one device cuts off, ±(VDD/2 − Vt) ≈ ±0.95 V around VDD/2 — this is the only resistor-free candidate that naturally covers ±1 V per side at 3.3 V. Limitations: input CM is pinned near VDD/2 (not rail-to-rail); Gm tracks VDD (needs a clean, regulated supply or a replica loop); N/P β matching sets residual HD2; power is set by VDD, not by a tail.

### C11. Bulk-driven / bulk-degenerated pairs
- Principle: signal into the bulk with VGS fixed; η = gmb/gm ≈ 0.2–0.4; rail-to-rail CM is possible because the source node moves only part of the range; Gmb varies −16 % to +30 % across CM at 50 µA tail; fT ≈ fT,gate/3.8; input-referred noise ≈ 1/η times worse; VBS must stay below the ≈ 0.6–0.7 V junction turn-on ([Sánchez-Sinencio bulk-driven lecture](https://people.engr.tamu.edu/s-sanchez/607%20Lect%208%20Bulk%20driven%20circuits%202009.pdf)). Bulk-input OTA: 0.8 µm, Vt ≈ 0.7 V, linear range ±600 mV at 450 mV CM (vs ≈ 60 mV for a gate pair), 0.35 µm version ±350 mV, GBW ≈ 450 kHz, noise 0.8–2.2 µV/√Hz, CMRR falls 15 dB over 0–0.7 V CM, bulk leakage limits CM above 0.9 V ([Univ. Malta OTA](https://www.um.edu.mt/library/oar/bitstream/123456789/16537/1/OA%20-%20%20A%20low%20voltage%20wide-input-range%20bulk-input%20CMOS%20OTA.2-11.pdf)). Bulk *degeneration* (Uruguay group): resistor replaced by a bulk-linearized MOS, 180 nm, an HD3 "sweet spot" for SD+BD, 6.4 nS transconductors with > 1 V range at 6 nA ([IEEE 8702327](https://ieeexplore.ieee.org/abstract/document/8702327/figures), [LASCAS 2024](https://investigadores.ucu.edu.uy/es/publications/enhancing-an-ota-linearity-through-bulk-degeneration-a-comparativ/)).
- Resistors: no. Limitation for you: the whole family trades Gm (×0.2–0.4) and noise (×2.5–5) for range — opposite of the goal; PMOS bulk-driven in 130 nm needs separate n-wells (you already have them), NMOS needs triple-well. Ibrahim/Onabajo also note bulk degeneration "requires a triple-well process and creates device matching constraints".

### C12. Source-follower-fed (level-shifted) input pairs / Czarnul four-MOS cell with follower loops
- Principle: source followers with local feedback hold their source voltages and feed the transconductor core, extending the input window; Czarnul's 4-MOS cell gives Iout linear in (V1 − V2) with G = K(VC2 − VC1), both in triode and in saturation ([KoreaScience paper](https://koreascience.kr/article/JAKO200671242945043.pdf)). Numbers: 0.35 µm (PSpice), 1.5 V, IB 120 µA, linear range ≈ ±1 V, IM3 ≈ −30 dB at 1 Vpp (80/90 MHz), −3 dB 300 MHz; MOS-only.
- Resistors: no. Limitation: the follower loops add noise and a pole; the linear range claim is at 1.5 V with VC = −1.5/−1.2 V (dual-rail), so it does not translate directly to a single 3.3 V rail; linearity −30 dB only.

---

## 2. DDA / CFIA implementations where gain accuracy comes from matched Gm

### C13. Current-feedback IA, TU Delft family (the direct analogue of your four-unit DDA)
- Wu/Chae/Huijsing/Makinwa, JSSC 2012 ([TU Delft repository](https://repository.tudelft.nl/file/File_984aecdb-b67c-46b2-9ac3-ee29cea2cc15)): 0.7 µm, 5 V, 270 µA. Input and feedback Gm are **undegenerated PMOS pairs in weak inversion** with low-Vt cascodes ("degeneration would raise power for a given transconductance"). Gain error 0.04 % over 0–2.5 V CM with equal input/output CM, 0.12 % when they differ; DEM swapping of Gm3/Gm4 turns mismatch Δ into Δ²/2 (2 % → 0.02 %); impedance balancing (matched cascodes in pair and tail) cut CM-dependent Gm variation from 0.089 % to 0.033 %; bulk biasing raised output impedance 200 → 500 MΩ. Noise 15 nV/√Hz; bandwidth 5 Hz (target); 6 mm² whole chip.
- Wu/Makinwa/Huijsing, JSSC 2009 ([TU Delft repository](https://repository.tudelft.nl/file/File_c2d800fd-dc00-4f7e-8fa0-23e23e671caa)): same construction, Gm = 250 µA/V, "transconductors limit linear range, acceptable for bridge readout" (±40 mV range), 4 kHz at gain 200, 4.8 mm².
- Witte/Huijsing/Makinwa, JSSC 2008 ([TU Delft repository](https://repository.tudelft.nl/file/File_c36069c7-2ee1-48b7-a1f8-56a56a9ebec1)): the wide-CM (1.9–30 V) version — here the V-I converters are composite transistors whose Gm is set by **laser-trimmed resistors** with a high-gain local loop (your §3 reference point); gain error 0.1 % (0.2 % over CM and Vref), GBW 1 MHz at 100 pF, noise ≈ 136 nV/√Hz with an 18 nV/√Hz floor from the resistors, 2.5 mm², 0.8 µm BiCMOS.
- Wu 2011 "gain-error reduction loop, 0.06 % untrimmed" ([TU Delft listing](https://pure.tudelft.nl/portal/en/publications/a-currentfeedback-instrumentation-amplifier-with-a-gain-error-reduction-loop-and-006-untrimmed-gain-error(e419e385-cf11-41b8-a61a-b342cafac88d).html)): only the title number was reachable.
- Takeaways for a ±1 V DDA: the precision CFIAs keep the *signal* small (mV) and win accuracy by cascode/CM symmetry + DEM; none of them attempt ±1 V linear Gm units. Their lesson that transfers is the **impedance-balancing** one: make the tail and the pair see the same cascode structure so Gm(Vcm) is flat, and equalize port CMs.

### C14. Rail-to-rail-input DDAs with complementary pairs
- The complementary-pair rail-to-rail input stage: NMOS pair active from ≈ VGS,n + Vdsat above the negative rail upward, PMOS the mirror image; without correction gm varies ≈ 2× across CM, constant-gm schemes bring that to 5–28 % ([Gharbiya/Phang report](https://www.eecg.utoronto.ca/~kphang/papers/2002/gharbiya_constgmota.pdf)). Huang et al. 1996 "DDA with rail-to-rail fully-differential outputs" ([IEEE 518931](https://ieeexplore.ieee.org/document/518931)) and the fully-balanced DDA of Alzaher/Elwan/Ismail 2001 (1.2 µm, class AB, "wide input range without complex circuitry" — no numbers reachable, [KFUPM](https://pure.kfupm.edu.sa/en/publications/a-cmos-fully-balanced-differential-difference-amplifier-and-its-a/)) are the cited DDA implementations; no compact 3.3 V numbers were found open-access.
- Limitation for a Gm-ratio gain: at 3.3 V with Vt 0.7 V both pairs are on for CM ≈ 1.3–2.0 V and only one outside; a 5–28 % residual gm variation becomes a gain error unless both ports share the same CM. Rail-to-rail CM and 0.1 %-class Gm ratio are in tension; the CFIA literature above quantifies the penalty (0.04 % → 0.12 %).

---

## 3. Resistor-based reference point: FVF / super-source-follower degenerated Gm (ranked below, as requested)

- Principle: the resistor sits between two low-impedance FVF nodes (≈ 1/(gm1·gm2·ro1)) so Gm ≈ 1/R almost exactly, and the FVF can source currents far above IB (class AB). Witte 2008 is a silicon example of the "composite transistor + local loop + resistor" V-I converter: gain error 0.1 %, 1 MHz GBW, resistor noise floor 18 nV/√Hz per 50 nV/√Hz stage ([TU Delft](https://repository.tudelft.nl/file/File_c36069c7-2ee1-48b7-a1f8-56a56a9ebec1)). FVF building blocks: VDDmin = |Vtp| + 2·Vdsat; class-AB FVF follower 180 nm, THD 0.2 % at 0.5 Vpp/100 kHz, 14.6 MHz at 100 pF, 31.5 µW, 114 × 47 µm, but it uses Rbat 55 kΩ, Rc 75 kΩ (as MOS) and 2.6 pF of capacitors ([MDPI JLPEA 2023](https://mdpi.com/2263080)).
- Why it is below the MOS-only options for you: it keeps the resistor (area, spread), and Gm·range is still ≈ I_tail unless class-AB; what it buys is Gm accuracy and linearity that no MOS-only cell reaches (−60 dB class). If one resistor per unit were ever acceptable, a 10–20 kΩ FVF-degenerated cell at 50–100 µA is the fastest accurate option in this list.

---

## 4. Capacitively-coupled / chopper IAs at MHz bandwidth

- Not sensible for a 2–20 MHz loop. Rooijers et al., JSSC 2021 ([TU Delft](https://repository.tudelft.nl/file/File_eb3a1b59-7ef3-4d28-93e3-ee7af7f2a275)): chopper-induced IMD ≈ 20·log(4·F_CH/(2π·BW)) from finite amplifier delay; getting 28 dB more IMD suppression by bandwidth alone would need ≈ 25× the OTA bandwidth and power; input current scales linearly with F_CH (600 pA at 20 kHz); their chopped OTA already has 15 MHz bandwidth to serve a 79 kHz tone. For signal bandwidth in the MHz you would need F_CH well above 10 MHz with a > 100 MHz OTA, and the CCIA input capacitors would add exactly the large caps you want to avoid. The TU Delft CFIAs chop at 30–510 kHz for sub-10 kHz signal bands. Chopping solves offset/1/f, not gain linearity; your problem is linearity and speed, so skip it.

---

## 5. Reducing current-source / cascode area while keeping matching

- Pelgrom ([JSSC 1989](https://class.ece.iastate.edu/djchen/ee501/2015/MOS%20TransistorMatching%20pelgrom89.pdf)): σ²(ΔI/I) ≈ 4σ²(Vt)/(VGS − Vt)² + σ²(β)/β², with σ(Vt) = A_VT/√(WL), σ(β)/β = A_β/√(WL). Best current matching at **high overdrive**; Vt and β terms are equal at VGS ≈ Vt + 2·A_VT/A_β; spacing term negligible below ≈ 100 µm² device area; A_VT scales ≈ linearly with tox (so thick-oxide 3.3 V devices match worse per µm² than LV ones), A_β does not; reducing offset 1.6 → 0.6 mV cost 9× gate area in his bandgap example.
- Drennan/McAndrew ([JSSC 2003](https://class.ece.iastate.edu/djchen/EE501/2016/MOSFET%20mismatch%20for%20analog%20design%20-%20drennan%20mcandrew%20-%202003.pdf)): raising Vov at fixed current forces smaller W/L and the two effects "offset each other"; mismatch "does not blindly depend on area alone"; splitting into parallel units reduces mismatch ≈ √N, mostly from splitting the *output* device; PMOS often matches better at equal current because it needs more Vov.
- Series-parallel composites (Galup-Montoro/Arnaud group, [UFSC PDF](https://lci.ufsc.br/pdf/Series%20parallel%20association.pdf)): a composite of unit transistors behaves like one long-channel device with much lower gds; for equal gate area they report substantially lower normalized current variance than a single device; design example 120 units of 4/40 µm giving 0.33 % expected current mismatch at 20 nA in 0.05 mm²; measured OTA offset σ 7–8 mV vs 9 mV predicted; they budget gate-area/total-area ρ ≈ 30 % (typically 5–20 %) for the wiring overhead of common-centroid composites. Series stacking of short units therefore does not save area at equal matching (area is the lever), but it lets you use the PDK's best-characterized unit size, interdigitate, and reach long-L output resistance without the poorly modeled "very long channel" corner Pelgrom warns about.
- **IHP SG13G2 numbers (sibling PDK of sg13cmos5l; the cmos5l tree has no separate mismatch file that I could find — check your local PDK):** from `sg13g2_moshv_mismatch.lib` and `sg13g2_moshv_mod_mismatch.lib` (HV = 3.3 V thick oxide), per-instance σ scales as `param/sqrt(m·l·w·1e12)` i.e. per √µm²:

| Device | A_VT | A_β (factuo) | σ(W), σ(L) |
|---|---|---|---|
| HV NMOS | 7.0 mV·µm | 0.5 %·µm | 3 nm, 3 nm |
| HV PMOS | 4.5 mV·µm | 0.4 %·µm | 3 nm, 3 nm |
| LV NMOS | 3.9 mV·µm | 0.5 %·µm | 4 nm, 2 nm |
| LV PMOS | 2.2 mV·µm | 0.33 %·µm | 4 nm, 2 nm |

  Worked rule (my arithmetic with the Pelgrom formula): an HV NMOS current source with W·L = 20 µm² at Vov = 0.3 V has σ(Vt) = 1.57 mV → 1.04 % from Vt plus 0.11 % from β ≈ **1.05 % σ(ΔI/I)**; at Vov = 0.6 V the same area gives 0.53 %; to reach 0.3 % at Vov = 0.3 V you need ≈ 11× the area (≈ 220 µm²), at Vov = 0.6 V ≈ 55 µm². PMOS HV current sources need ≈ 2.4× less area than NMOS for the same σ. So: **choose L for ro/cascode headroom and W·L for matching; pushing Vov from 0.3 V to 0.6 V halves the required area** at 3.3 V where the headroom exists. Note the PDK applies mismatch only with `mm_ok=1`, which your CLAUDE.md already flags as absent on extracted netlists.

---

## Ranking for your constraints (3.3 V, Vt 0.7 V, ±0.5…±1 V per pair, higher Gm, less area, MOS-only)

1. **C10 Nauta inverter cells** — only MOS-only option covering ≈ ±0.95 V at 3.3 V, no tails/cascodes (smallest area), best noise, no internal nodes (fastest); costs: CM pinned at VDD/2, Gm ∝ VDD, N/P β matching sets HD2; absolute spread cancels in the Gm ratio.
2. **C7 triode-MOS tracking degeneration** — drop-in for the 150 kΩ with a fraction of the area; spread cancels in the ratio; needs Vov ≳ 0.8 V on the triode devices, fine at 3.3 V.
3. **C1 large-Vov pair** for the ±0.5 V case only — simplest, lowest noise, Vt mismatch diluted by Vov.
4. **C2/C3 cross-coupled quads** — ±1 V proven (0.2 % THD at 5 V), but 2–4× devices and the level shift eats CM range.
5. **C5/C6 class-AB (adaptive bias, super-AB)** — the only way to beat Gm·range ≈ I_tail, but Gm is not flat, so use only inside a loop, with identical cells on both ports.
6. **C14 complementary rail-to-rail** — pay 5–28 % Gm(CM) variation unless both ports share CM; the CFIA data (0.04 % → 0.12 %) quantifies why to avoid unequal CMs.
7. **C11 bulk-driven** — rail-to-rail but 2.5–5× worse Gm and noise; wrong direction for "faster".
8. **§3 FVF + resistor** — accurate and fast but keeps the resistor.
9. **§4 chopper/CCIA** — not applicable at MHz.

Sources:
- [Kuo, IntechOpen 2010 — CMOS transconductor linearization survey](https://cdn.intechopen.com/pdfs/9851.pdf)
- [Harish et al./Nauta, JSSC — inverter LNTA linearization, PVT sensitivity](https://ris.utwente.nl/ws/files/51806699/Harish_RF_Transconductor_Linearization_Robust_JSSC_main_final.pdf)
- [Nauta, Electronics Letters 1990 — inverter Gm-C filter](https://ris.utwente.nl/ws/files/6511768/cmos_vhf.pdf)
- [Barthélemy et al. 2008 — inverter-only OTA, 0.35 µm](https://link.springer.com/doi/10.1007/s10470-008-9167-8)
- [MDPI Electronics 2023 — inverter-based FDDTA](https://www.mdpi.com/2079-9292/12/4/963)
- [Arya et al., Radioengineering 2013 — 0.5 V Nauta-type gm-C filter](https://www.radioeng.cz/fulltexts/2013/13_01_0174_0178.pdf)
- [Klumperink/van der Zwan/Seevinck, EL 1989 — square-law variable Gm](https://icejive.el.utwente.nl/home/erick/Klumperink-CMOS%20Variable%20Transconductance%20Circuit%20with%20Constant%20Bandwidth-EL1989.pdf)
- [Hill/Sun/Szczepanski 2000 — compressive+expansive pairs](https://uhra.herts.ac.uk/id/eprint/12843/1/904239.pdf)
- [Ibrahim & Onabajo — unbalanced degeneration + adaptive bias, 0.13 µm](https://par.nsf.gov/servlets/purl/10519901)
- [Sánchez-Sinencio — OTA-C filter linearization notes](https://people.engr.tamu.edu/s-sanchez/622%20OTA-C%20Filter%20Linearization.pdf)
- [Sánchez-Sinencio — FVF lecture](https://people.engr.tamu.edu/s-sanchez/607%20Lect%205%20BB%20FVF.pdf)
- [Carvajal et al. — FVF theory and applications](https://observatorio-investigacion.unavarra.es/documentos/5f8e8e7a2999527b469fec5c?lang=eu)
- [Ramírez-Angulo et al., JLPEA 2023 — class-AB FVF follower/mirror](https://mdpi.com/2263080)
- [KoreaScience — Czarnul 4-MOS cell with follower loops](https://koreascience.kr/article/JAKO200671242945043.pdf)
- [NTU — COMFET/pseudo-PNP wide-range transconductor](https://scholars.lib.ntu.edu.tw/bitstream/123456789/149752/1/00539891.pdf)
- [Rezzi/Baschirotto/Castello 1995 — pseudo-differential filter](https://iris.unipv.it/handle/11571/104178)
- [Sánchez-Sinencio — bulk-driven circuits lecture](https://people.engr.tamu.edu/s-sanchez/607%20Lect%208%20Bulk%20driven%20circuits%202009.pdf)
- [Univ. Malta — bulk-input wide-range OTA](https://www.um.edu.mt/library/oar/bitstream/123456789/16537/1/OA%20-%20%20A%20low%20voltage%20wide-input-range%20bulk-input%20CMOS%20OTA.2-11.pdf)
- [IEEE 8702327 — Bulk linearization techniques](https://ieeexplore.ieee.org/abstract/document/8702327/figures)
- [LASCAS 2024 — bulk vs source degeneration OTAs](https://investigadores.ucu.edu.uy/es/publications/enhancing-an-ota-linearity-through-bulk-degeneration-a-comparativ/)
- [Wu/Chae/Huijsing/Makinwa, JSSC 2012 — 0.04 % gain-error CFIA](https://repository.tudelft.nl/file/File_984aecdb-b67c-46b2-9ac3-ee29cea2cc15)
- [Wu/Makinwa/Huijsing, JSSC 2009 — chopper CFIA](https://repository.tudelft.nl/file/File_c2d800fd-dc00-4f7e-8fa0-23e23e671caa)
- [Witte/Huijsing/Makinwa, JSSC 2008 — high-side CFIA](https://repository.tudelft.nl/file/File_c36069c7-2ee1-48b7-a1f8-56a56a9ebec1)
- [Wu et al. 2011 — CFIA with GER loop, 0.06 %](https://pure.tudelft.nl/portal/en/publications/a-currentfeedback-instrumentation-amplifier-with-a-gain-error-reduction-loop-and-006-untrimmed-gain-error(e419e385-cf11-41b8-a61a-b342cafac88d).html)
- [Gharbiya/Phang 2002 — constant-gm rail-to-rail input stages](https://www.eecg.utoronto.ca/~kphang/papers/2002/gharbiya_constgmota.pdf)
- [Huang et al. 1996 — rail-to-rail DDA (IEEE 518931)](https://ieeexplore.ieee.org/document/518931)
- [Alzaher/Elwan/Ismail 2001 — fully balanced DDA](https://pure.kfupm.edu.sa/en/publications/a-cmos-fully-balanced-differential-difference-amplifier-and-its-a/)
- [Rooijers et al., JSSC 2021 — chopper IMD / fill-in](https://repository.tudelft.nl/file/File_eb3a1b59-7ef3-4d28-93e3-ee7af7f2a275)
- [Pelgrom et al., JSSC 1989 — matching](https://class.ece.iastate.edu/djchen/ee501/2015/MOS%20TransistorMatching%20pelgrom89.pdf)
- [Drennan & McAndrew, JSSC 2003 — mismatch for analog design](https://class.ece.iastate.edu/djchen/EE501/2016/MOSFET%20mismatch%20for%20analog%20design%20-%20drennan%20mcandrew%20-%202003.pdf)
- [Boser, Berkeley EE240B — matching lecture (A_VT 5 mV·µm, A_β 1 %·µm at 180 nm)](https://people.eecs.berkeley.edu/~boser/courses/240B/lectures/M13%20Matching.pdf)
- [UFSC — series-parallel association of FETs / low-mismatch mirrors](https://lci.ufsc.br/pdf/Series%20parallel%20association.pdf)
- [TAMU ECEN474 lecture 9 — differential pair large-signal](https://people.engr.tamu.edu/spalermo/ecen474/lecture09_ee474_diff_amps.pdf)
- [TAMU ECEN474 lecture 6 — matching layout](https://people.engr.tamu.edu/spalermo/ecen474/lecture06_ee474_layout.pdf)
- [2AMLogic issue — SG13G2 LV mismatch model reading](https://github.com/2AMLogic/sg13g2-comparator/issues/6)
- IHP-Open-PDK `ihp-sg13g2/libs.tech/ngspice/models/sg13g2_moshv_mismatch.lib`, `sg13g2_moslv_mismatch.lib`, `sg13g2_moshv_mod_mismatch.lib` (fetched raw from github.com/IHP-GmbH/IHP-Open-PDK, main branch)
- [Seon 2008 — ±1 V analog computational circuits at 3.3 V, 0.25 µm](https://link.springer.com/doi/10.1007/s10470-007-9119-8)
- [Szczepanski/Schaumann/Pankiewicz 1996 — VHF transconductor, negative-resistance gain boost](https://link.springer.com/article/10.1007/BF00195560)
