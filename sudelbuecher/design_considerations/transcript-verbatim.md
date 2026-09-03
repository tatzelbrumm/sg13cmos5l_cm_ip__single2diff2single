# Verbatim transcript — analog pad buffer for IHP SG13CMOS5L

Unabridged, no summaries. Turns are reproduced as delivered. The only omission
is the body of the user-uploaded PDF in Turn 6 (a copyrighted IEEE paper);
it is identified by filename and citation instead of being reproduced.

Session date: 3 September 2026.

---

## Turn 1 — User

> figures of merit for a differential on chip input, analogue output pad driver for 130 nanometers CMOS, irrespective of bias current

## Turn 1 — Assistant

**The invariants under current scaling.** If you scale W and I together at fixed inversion level, gm, GBW, SR all scale ∝I and noise power ∝1/I. So the quantities that survive are exactly the dimensionless ratios and the per-current groups:

**Genuinely intensive (no current anywhere)**

- **gm/I_D** [V⁻¹] and the product **(gm/I_D)·f_T** — the only honest speed/efficiency invariant; peaks in moderate inversion (IC ≈ 0.1–1). Everything else you choose is downstream of where you sit on that curve.
- **Intrinsic gain gm·r_o** — sets static gain error 1/(βA₀). In 130 nm ≈ 25–30 at L_min, 100–300 at L ≈ 1 µm. This is the number that punishes you for wanting bandwidth from short channels.
- **Class-AB current gain I_out,peak/I_Q** — the figure that makes a pad driver worth building. Class A pins it at 1 (±I_tail). Decent AB output stages: 10–100.
- **Swing efficiency V_out,pp/V_DD** — i.e. ΣV_DSsat lost. Source follower forfeits a V_GS; CS push-pull only 2·V_DSsat. At 1.2 V core this is the dominant architectural fork; the 3.3 V thick-ox devices buy swing at the cost of f_T and A_VT.
- **Offset: A_VT = V_os·√(WL)** [mV·µm], ~3–5 mV·µm thin-ox — and its useful normalized form V_os/V_out,pp.
- **CMRR, PSRR** at the frequency of interest (relevant since your input is differential and your output reference is a noisy pad ring).
- **GBW/f_T** — technology utilization. Usually humiliating, and usefully so.
- **Slew factor SR/(GBW·V_step)** — >2π means settling is linear, not slew-limited. Dimensionless, and it tells you whether the SR FoM matters at all.
- **η = P_load/P_supply** — 25 % ceiling for class A into a resistive load.

**Per-current groups (Vittoz/Sansen survey form — invariant, but only comparable at equal C_L and equal swing)**

- FoM_SS = GBW·C_L/I_DD [MHz·pF/mA]
- FoM_LS = SR·C_L/I_DD [V·pF/(µs·mA)]
- NEF / PEF; or v_n,in²·I_DD as the raw invariant.
- HD3 or SFDR quoted at fixed V_out,pp/V_DD *and* fixed gm/I_D — otherwise it's a distortion measurement of your overdrive choice, not of the topology.

**Pad-specific, and where most such buffers actually fail**

- **Transparency: C_in/C_tapped-node**, plus kickback charge per unit input swing. For a monitor buffer on a nanoampere node this dominates every other number — the buffer that measures the DAC must not be the DAC's dominant load.
- **Stability across load corner**: phase margin over C_L from ~5 pF (bare pad + ESD) to ~50 pF + coax. A single-number GBW is meaningless without the load-range envelope.
- |Z_out(f)| and back-drive tolerance.
- Oxide field at the pad under ESD clamp turn-on.

The one that isn't a ratio and can't be made into one: **area**. Offset and matching drag it in through A_VT/√(WL), so any FoM table that omits area is quietly comparing a 40 µm² driver to a 4000 µm² one.

---

## Turn 2 — User

> compile me a sample of reference designs that are competitive nowadays

## Turn 2 — Assistant

**First, a de-scaling point:** a pad driver in 130 nm almost never uses 130 nm devices. On SG13G2 you'd build the output stage from the 3.3 V thick-oxide devices, whose t_ox, V_T, and A_VT put them electrically close to a 0.35 µm process. That's why the reference base for this problem is still the 0.35/0.18 µm literature and it transfers nearly one-for-one — only the digital-side control and the input stage benefit from the core devices.

**Class-AB output control — the canonical cells**

- **Monticelli floating-battery class AB** (JSSC 1986): two stacked level shifters holding the gate-source difference of the push-pull pair. Still the default in production op-amps; predictable I_Q, no positive feedback, well-behaved across corners. Costs headroom.
- **Ramírez-Angulo / Carvajal FVF and DFVF-based buffers** (TCAS-I 2005 review of the flipped voltage follower): the compactness champion. Class AB falls out of the topology rather than being bolted on; low quiescent current, very large current gain. Weakness is systematic offset and PSRR — read them before you commit.
- **Adaptive/dynamic tail biasing** (Degrauwe's dynamic biasing lineage, and the more recent FPD variants): an auxiliary tail current that rises only during transitions, sensed off the internal push-pull drive nodes. Buys slew without buying static power, at the cost of a settling tail that is hard to characterize.

**The flat-panel source-driver corpus** — this is where the competitive numbers actually live, because the industry optimizes exactly your FoM set (nF loads, µA quiescent, area per channel). Representative results: a 0.35 µm design settling a 1 nF load in 0.9 µs on 3 V full swing at 3.5 µA quiescent, and in 0.18 µm, a single-stage asymmetric rail-to-rail class-AB stage driving 250 pF to 15 nF using positive feedback loops and a dynamic floating node. Sawigun & Demosthenous's slew-enhancement paper (TCAS-II 2012) is the cleanest analysis of *why* the transconductor-based buffers current-starve on large steps — a +200 % speed gain for 1.25 % static power and 3 % area. Note the load-range spec in the 0.18 µm paper: that's the number to imitate, since your pad sees anything from a probe tip to a metre of coax.

**Compensation for the wide-C_L problem**

Leung & Mok's damping-factor-control and the Ho/Mok active-feedback families (JSSC ~2000–2003) are the reference points for driving loads that swing an order of magnitude. Anything quoting a single phase margin at a single C_L is not a competitive reference.

**Where I'd push back on the premise**

For a thermometer-coded nanoampere current DAC, the competitive "reference design" may not be a voltage buffer at all. Three alternatives that beat any of the above on the transparency FoM:

1. **Cascoded current output straight to the pad**, into an off-chip Keithley/TIA. Zero on-chip precision burden, ~fF of loading on the DAC node, and your measurement accuracy becomes an instrument spec rather than a design risk.
2. **On-chip regulated cascode / current conveyor**, holding the DAC drain at a fixed potential while the current leaves. Preserves output impedance, which for a nA source is the whole ballgame.
3. **Chopped or auto-zeroed unity-gain buffer** if you truly need a voltage at the pad — because at nA levels the offset and 1/f of any class-AB buffer will dominate the quantity you're trying to publish.

I've given topology families and the papers I'm confident of by name; I have not quoted numbers I couldn't verify, and the 1986/2005 attributions are from memory rather than from a source I just checked — worth confirming the volume/page before they go in a bibliography.

---

## Turn 3 — User

> this is not for the current duck they're putting on the high chips is already taped out and in fabrication this is for the next design which is probably chipalooza IHP 130 5L variant

## Turn 3 — Assistant

Then the constraint set changes materially. SG13CMOS5L is not SG13G2 minus HBTs — it carries the SG13CMOS front-end but drops isolated NMOS and the MIM capacitor, and the BEOL is only four thin metals plus a single 2 µm TopMetal. Three of those four omissions hit an output driver directly.

**No MIM.** Your compensation capacitor is now a thick-oxide MOS cap in accumulation or a MOM comb on M1–M4 — and with four thin metals, MOM density is poor and the cap sits low in the stack where it couples to substrate. A MOScap is voltage-dependent even in accumulation, so any topology whose stability depends on precise pole–zero cancellation (Miller with nulling resistor, nested Miller, active-feedback compensation) becomes a corner-analysis nightmare. This is the single strongest steer in the whole problem: **prefer load-compensated single-stage architectures**, where the dominant pole is C_L at the pad and C_c is either absent or non-critical. Folded cascode or current-mirror OTA with a class-AB output, not a two-stage Miller amp. It also kills the Leung/Mok multistage compensation literature I pointed at — those papers assume a well-characterized linear C_c.

**No deep n-well.** Every NMOS bulk is the global p-substrate, shared with whatever digital neighbor Chipalooza puts next to you. Consequences: (a) NMOS source followers take full body effect with no escape, so the PMOS-in-own-nwell devices become the preferred followers and level shifters; (b) substrate-coupled noise enters your output stage's NMOS side with no isolation, which argues for keeping the signal path PMOS-dominant where you can and for **carrying the signal off-chip differentially rather than single-ended** — you have a differential input already, so the cheap fix is not to collapse it. If the measurement setup allows a differential receiver, take it. If it must be single-ended at the pad, you need an on-chip reference pad routed alongside as a pseudo-differential return, and you should budget for the substrate noise you cannot filter.

**One TopMetal, 2 µm, no TM2.** Supply distribution to the output stage and the ESD return path are both thinner than in G2. This caps peak drive current and makes IR drop across the pad ring a real term in your swing budget. It also removes a shielding layer — with only four thin metals you will have to spend one of them on a shield plane over the input pair, which is expensive when M4 is also your best MOM plate and your best local supply mesh.

**Revised weighting of the figures of merit**

Given the above, the ones that discriminate between candidate topologies here are: swing efficiency V_out,pp/ΣV_DSsat on the 3.3 V thick-ox rail; phase margin across the full C_L envelope *with C_c at its ±30 % MOScap corner*; PSRR and substrate-coupling rejection (now a first-class spec, not an afterthought); and area, since MOM/MOScap compensation is area-hungry and Chipalooza slots are small. gm/I_D and intrinsic gain still set the design point, but they no longer differentiate — the compensation and isolation constraints do.

**Two things to resolve before any of this matters**

Whether `ihp-sg13cmos5l` ships an analog pad cell — an unbuffered pad with a characterized ESD network and known parasitic capacitance — or only digital I/O cells. If it's digital-only, you are either designing your own ESD structure (which on a shared shuttle you probably cannot get signed off) or living with a digital pad's diode clamps and input protection in your analog path. And what the Chipalooza floorplan gives you for pad allocation and whether an analog supply domain separate from IOVDD is available at all.

I'd check the PDK repo directly rather than trust my summary of the marketing page — the open-source variant was described as under development for early 2026, so the device and cell inventory may have moved since.

---

## Turn 4 — User

> table of links to the articles for the reference AB designs please

## Turn 4 — Assistant

Links verified from search; where I only have a bibliographic pointer from another paper's reference list, I've said so rather than manufacture a DOI.

| # | Design / paper | Venue | Link |
|---|---|---|---|
| 1 | Monticelli, *A quad CMOS single-supply op amp with rail-to-rail output swing* — the floating-battery AB mesh | JSSC SC-21(6), 1986, 1026–1034 | [free PDF (Iowa State)](http://class.ece.iastate.edu/djchen/ee501/2008/MonticelliRailToRailOutSwing.pdf) · [doi:10.1109/JSSC.1986.1052645](https://doi.org/10.1109/jssc.1986.1052645) |
| 2 | Carvajal, Ramírez-Angulo et al., *The flipped voltage follower* — FVF/DFVF taxonomy, the source cell for the compact AB buffers | TCAS-I 52, 2005, 1276–1291 | [doi:10.1109/TCSI.2005.851387](https://doi.org/10.1109/TCSI.2005.851387) · [ResearchGate](https://www.researchgate.net/publication/3451001_The_flipped_voltage_follower_A_useful_cell_for_low-voltage_low-power_circuit_design) |
| 3 | Sawigun & Demosthenous, *A compact rail-to-rail class-AB CMOS buffer with slew-rate enhancement* — the SR-starvation analysis | TCAS-II, 2012 | [IEEE Xplore](https://ieeexplore.ieee.org/document/6236111/) · [ResearchGate](https://www.researchgate.net/publication/230897337_A_compact_rail-to-rail_class-AB_CMOS_buffer_with_slew-rate_enhancement) |
| 4 | *High-speed rail-to-rail class-AB buffer with compact adaptive biasing for FPD* — transition-triggered auxiliary tail current | MDPI Electronics 9(12), 2020 | [open access](https://www.mdpi.com/2079-9292/9/12/2018) |
| 5 | Ramírez-Angulo/Carvajal et al., *Class-AB output stages … accurate quiescent current control by dynamic biasing* | Analog Integr. Circ. Sig. Process. | [Springer](https://link.springer.com/article/10.1023/A:1024453731969) |
| 6 | *Low-voltage class-AB output stages using floating capacitors* — the sub-2·V_GS alternative to Monticelli | Electron. Lett. lineage | [PDF via Academia](https://www.academia.edu/22725840/Low_voltage_class_AB_output_stages_for_CMOS_op_amps_using_floating_capacitors) |
| 7 | Hogervorst et al., *Rail-to-rail constant-gm input stage and class-AB output stage* | Analog Integr. Circ. Sig. Process. | [Springer](https://link.springer.com/article/10.1007/BF01239246) |
| 8 | *Rail-to-rail low-power high-slew-rate CMOS analogue buffer* — two complementary class-AB pairs, <32 fF input cap | — | [Academia](https://www.academia.edu/10744243/Rail_to_rail_low_power_high_slew_rate_CMOS_analogue_buffer) |
| 9 | *Rail-to-rail high-speed class-AB CMOS buffer with enhanced slew rate* — dual-path push-pull, 1 nF at 3.5 µA I_Q | — | [ResearchGate](https://www.researchgate.net/publication/274173822_A_Rail-To-Rail_Hign_Speed_Class-AB_CMOS_Buffer_with_Low_Power_and_Enhanced_Slew_Rate) |
| 10 | López-Martín et al., *The Flipped Voltage Follower: Theory and Applications* — book-chapter consolidation | Springer LNEE | [chapter](https://link.springer.com/chapter/10.1007/978-3-642-36329-0_12) |

**No link verified, bibliography only** (all appear in the reference lists of the above, so the citations are sound even though I didn't open them): You, Embabi & Sánchez-Sinencio, *Low-voltage class-AB buffers with quiescent current control*, JSSC 33(6), 1998, 915–920 — the other main branch of I_Q control; de Langen & Huijsing, JSSC 33(10), 1998, 1482–1496; Giustolisi & Palmisano, *1.2-V op-amp with a dynamically biased output stage*, JSSC 35(4), 2000, 632–636; Pardoen & Degrauwe, *A rail-to-rail CMOS input/output power amplifier*, JSSC 25(4), 1990, 501–504; Fisher & Koch, *A highly linear CMOS buffer amplifier*, JSSC 22, 1987, 330–334.

For SG13CMOS5L specifically, #1 and #6 are the ones to read against each other — Monticelli's mesh costs you >2·V_GS of headroom but needs no capacitor, while the floating-capacitor variants buy headroom back by spending exactly the component the 5L variant doesn't give you. #3 and #4 are the useful pair on slew enhancement, and #2 is the compactness reference whose offset and PSRR you'll have to characterize yourself, since the papers largely don't.

---

## Turn 5 — User

> Are Monticelli and Hogervorst&Huijsing essentially the same topology?

## Turn 5 — Assistant

No — and the confusion is worth pulling apart, because the two names sit on different axes.

**Different axes.** Monticelli's paper is about a class-AB *output* stage plus quiescent-current control; its input stage is a conventional single pair. Note what the abstract claims: an output swing extending to either rail, together with an input common-mode range that includes ground — that's ground-sensing, not rail-to-rail input. The Hogervorst/Huijsing headline contribution is precisely the thing Monticelli doesn't have: the **constant-g_m rail-to-rail input stage**, two complementary pairs with tail-current steering so that g_m,tot stays flat as the common mode sweeps. They also publish output stages, but the pairing in the literature is usually *Hogervorst input + some floating class-AB output*, and that output can perfectly well be Monticelli's mesh. They compose rather than compete.

**Where they do overlap, and how they differ.** On the output side both belong to Huijsing's *feedforward* class-AB control family — a floating voltage source (translinear loop) between the two output gates, as opposed to *feedback* control with an explicit minimum-current selector, which is the de Langen & Huijsing branch (JSSC 1998). So Monticelli and the Hogervorst compact output stage are cousins, not twins, and the Delft feedback-controlled stages are a genuinely different animal: they sense the smaller of the two output currents and regulate it, giving much tighter I_Q over corners at the cost of a loop that can ring.

**Two practical differences that matter for your 5L driver:**

*Headroom.* Monticelli's mesh needs roughly two V_GS plus two saturation voltages of stack. That's exactly the criticism levelled at it by the floating-capacitor school — their stated advantage is accurate quiescent control at supplies near one threshold, where Monticelli's requires more than two V_GS. On your 3.3 V thick-oxide rail with V_T ≈ 0.6–0.7 V this is affordable; it would not be on the 1.2 V core.

*Drive asymmetry.* The mesh is not symmetric in the small-signal path. One output device's gate is driven directly by the cascode current, while the complementary device is driven through the mesh, which behaves as an additional cascode stage with a pole set by 1/g_m of the mesh device and the capacitance at that node — contributing a non-dominant pole and extra delay on that path only. That asymmetry is exactly what shows up as unequal rising/falling settling and it interacts badly with a compensation capacitor whose value you can't pin down. Given no MIM, I'd treat that pole's location as a corner variable and simulate it explicitly rather than trusting a nominal phase margin.

One caveat on my own sourcing: I've cited Hogervorst & Huijsing from reference lists and the Springer abstract, not from having worked through the 1994 JSSC "compact power-efficient 3 V rail-to-rail I/O opamp" itself. If the feedforward-versus-feedback distinction is going to carry weight in a design justification, Huijsing's *Operational Amplifier Theory and Design* has the canonical taxonomy and is worth checking against my summary.

---

## Turn 6 — User

> *[attachment: `HogervorstRail2Rail1994.pdf` — R. Hogervorst, J. P. Tero, R. G. H. Eschauzier, J. H. Huijsing, "A Compact Power-Efficient 3 V CMOS Rail-to-Rail Input/Output Operational Amplifier for VLSI Cell Libraries," IEEE JSSC 29(12), Dec. 1994, 1505–1513. Body not reproduced here — copyrighted.]*
>
> Here's the Hogervorst&Huijsing. Good as generic-ish output pin driver for IHP sg13 5L?

## Turn 6 — Assistant

Yes — but as an **output-stage donor, not as a cell to copy**. Three things to separate.

**Keep: the output stage and its biasing (Figs. 5, 8, 11).** This is the genuinely good part and it ports cleanly. The floating class-AB control M19/M20 shifted *into* the folded-cascode summing circuit means the AB control contributes neither noise nor offset — the two bias sources I_b6/I_b7 that would otherwise sit in parallel with the cascodes M14/M16 are eliminated outright. Then the floating current source M27–M28, built with the *same* translinear structure as the AB control so its supply dependence cancels the control's, gives an I_Q that doesn't walk with VDD. That's a real solution to a real problem and it costs two transistors. Table I was measured at exactly 3.3 V — the same rail as IOVDD on the 5L shuttle — with two stacked V_GS in the output stage, which on IHP thick-oxide devices (V_T ≈ 0.5–0.7 V) leaves you room.

**Discard: the entire constant-g_m rail-to-rail input apparatus (Section II).** You said differential *on-chip* input. If the common mode is fixed and known, everything in Figs. 1–4 is pure cost: the complementary pairs, the two current switches, the 3× mirrors M6–M7 and M9–M10, plus M29–M31 whose only job is to keep the positive-feedback loop from arming below 2.9 V. And look at what it buys you in defects — CMRR collapsing to 43 dB in the take-over ranges (vs. 70 dB elsewhere), ~2 mV of offset shift per take-over range, and a slew rate that changes by a factor of two depending where the common mode sits. A single PMOS pair at a fixed CM gives you constant g_m, constant SR, no take-over artifacts, better CMRR, a bulk-tied-to-source device in its own n-well (which matters with no deep n-well available), and perhaps 40 % of the area back.

**The porting obstacle is C_M1/C_M2.** They're Miller caps tied from V_o to the output-device gates, so the *full output swing* stands across them. In a process with MIM that's free; in 5L you're building them from MOM fingers on four thin metals, or from a thick-ox MOScap that will traverse accumulation-to-depletion as the output swings — i.e. a compensation capacitor that changes value with the signal it is compensating. Two mitigations from the paper itself: the plain-Miller version has 66° phase margin versus 53° for cascoded-Miller, so take the Fig. 13 variant and spend the margin on capacitor uncertainty rather than on bandwidth. They also note cascoded-Miller can peak at high output current and recommend plain Miller above ~3 mA — which points the same way for a driver.

**Two numbers that won't survive the port.** The 85 dB open-loop gain came from 1 µm devices; on 130 nm thick-ox with the same cascoding, budget 60–70 dB, and their own pointer to Bult & Geelen gain boosting on M14/M16 becomes less optional. And the load: 10 kΩ ‖ 10 pF with 3 mA peak is a *chip-level* buffer. A metre of coax plus a scope front end is 100 pF and change. Scaling the output devices for that pushes C_GS,out up, drags the output pole down, and forces C_M up — straight back into the capacitor problem. Worth sizing that loop before committing.

Their FoM (6), B/P_sup at C_L = 10 pF, is supply-referred rather than current-referred; convert to GBW·C_L/I_DD if you want to compare it against anything modern.

One side benefit: the Fig. 6 → 8 → 9 → 10 → 11 progression, where each figure repairs one named defect of the previous, is unusually clean design-rationale writing. If Chipalooza wants documentation rather than just a GDS, that structure is worth stealing as a template.

---

## Turn 7 — User

> What's a reasonable (but not too aggressive) bandwidth for analog single ended pin to differential and differential to single ended pin buffer amplifiers in the IHP sg13 5L process?
> I have no idea what's conservative, aggressive, and impossible.

## Turn 7 — Assistant

Let me give you the arithmetic rather than a number, since the number falls out of two constraints you can check yourself.

**The load sets everything on the output side.** For a load-compensated single stage, GBW = g_m/(2π·C_L). Your C_L is not the pad — it's the pad (a few hundred fF) plus ESD (~1 pF) plus bond wire plus PCB trace plus whatever instrument you attach. A 10× scope probe alone is 10–15 pF. So budget **C_L ≈ 15 pF** as the honest bench number, and 50–100 pF if anyone ever hangs a length of coax on it un-terminated.

At C_L = 15 pF: 10 MHz needs g_m ≈ 0.94 mS, which at g_m/I_D = 10 V⁻¹ is ~95 µA. 100 MHz needs 9.4 mS and ~1 mA. Current is not the wall — **the non-dominant poles are.** A thick-oxide 3.3 V device at L ≈ 1 µm in moderate inversion has an f_T of maybe 1–3 GHz, and your mirror and cascode poles will land somewhere in the low hundreds of MHz. Pushing GBW to 100 MHz puts the unity-gain crossing uncomfortably close to them, and you're doing that with a compensation capacitor of uncertain value because 5L has no MIM.

**The second constraint is slew, and it usually binds first.** Full-power bandwidth needs SR = 2π·f·V_peak, i.e. peak current I = C_L·SR. For 1 V peak at 10 MHz into 15 pF that's ~0.94 mA of peak drive — fine for a class-AB stage running 50 µA quiescent. At 100 MHz it's 9.4 mA, which on a single 2 µm TopMetal supply route starts eating your swing budget in IR drop. Quote small-signal GBW and full-power bandwidth separately; they are not the same spec and the gap between them is the whole point of class AB.

**Calibration tiers, output buffer (differential in → single-ended pin):**

| | GBW | FPBW @1 V_pk | Risk |
|---|---|---|---|
| Conservative | 1–5 MHz | ~1–2 MHz | first silicon works, no drama |
| Reasonable | **10–30 MHz** | 5–10 MHz | the sweet spot; poles comfortably clear |
| Aggressive | 50–100 MHz | 20 MHz | pole management is now the whole design; MOScap C_c uncertainty becomes acute |
| Don't | >200 MHz | — | stop calling it a buffer |

Above roughly 100 MHz through a wire-bonded pad into an unknown board, the problem stops being "amplifier" and becomes "transmission line": you want an impedance-matched 50 Ω driver, the load turns resistive, and power goes up by an order of magnitude. Different project.

**The input buffer is a much easier problem and should not get the same spec.** Single-ended pin → differential on-chip drives only internal capacitance — call it 200–500 fF. 50 MHz needs under 100 µS of g_m. Here the limits are the ESD structure's series RC, the input pair's own matching and noise, and the fact that you probably *want* to band-limit deliberately for anti-aliasing and noise. **50–100 MHz is comfortable; 20 MHz is conservative.** The asymmetry is real: roughly a decade of headroom between the two directions.

**Two things that should pull you downward.** Noise scales as √BW, so if this path is for characterizing anything quiet, excess bandwidth is a direct loss of resolution. And keeping GBW modest lets you make C_L the dominant pole and drop the Miller capacitor entirely — which is the cleanest way out of the no-MIM problem I flagged earlier.

I'd put the reasonable-tier stake at **20 MHz out, 50 MHz in**, and note that the answer genuinely depends on what you're observing: DC bias characterization needs 1 MHz, and settling-transient observation needs whatever bandwidth resolves the settling constant you care about.

---

## Turn 8 — User

> What is FPBW anyhow?

## Turn 8 — Assistant

Full-Power Bandwidth. The highest frequency at which the amplifier can still deliver its *full rated output swing* without the waveform being distorted by slew-rate limiting.

The derivation is one line. Take a sine at the output, V_out = V_pk·sin(2πft). Its maximum rate of change is at the zero crossing:

dV/dt|_max = 2π·f·V_pk

The amplifier can only supply dV/dt up to its slew rate SR. Set them equal and solve:

**FPBW = SR / (2π·V_pk)**

Above that frequency the output stops being a sine and becomes a triangle wave — the amplifier is charging C_L with all the current it has and simply can't turn around fast enough. It's a hard, ugly, large-signal nonlinearity, not a gentle roll-off.

**Why it's a separate number from GBW.** GBW is a *small-signal* spec: it tells you how fast the amplifier responds to a wiggle small enough that everything stays linear. FPBW is *large-signal*: it tells you how fast it responds when you ask for the whole swing. A class-A stage with a fixed tail current I has SR = I/C_L, and its FPBW can be a factor of ten or more below its GBW — so it looks fast on a Bode plot and turns your 1 V sine into a triangle. That gap is exactly what class AB exists to close: on a large step the output devices deliver many times the quiescent current, so SR is no longer pinned to I_Q.

The ratio SR/(GBW·V_step) I mentioned in the first message is the same idea in dimensionless form. Above about 2π, the amplifier settles by linear exponential decay and the FPBW spec doesn't constrain you; below it, slewing dominates the settling time and GBW is a fiction.

Concretely, for the numbers in the table: 1 V peak at 10 MHz needs SR = 2π × 10⁷ × 1 ≈ 63 V/µs, and into 15 pF that's I = C·SR ≈ 0.94 mA of peak drive. Which is the same 0.94 mA I quoted — the peak-current and FPBW framings are one calculation wearing two hats.

---

## Turn 9 — User

> Make a report from this, markdown versions for ReText and for github/gitlab Plain TeX markup, also PDF.
> Also, a verbatim chat output, unabridged, no summaries.

## Turn 9 — Assistant

*[Tool use: read `/mnt/skills/public/pdf/SKILL.md`; probed the container toolchain; wrote `report-retext.md`, a conversion script `mk_gfm.py`, and `preamble.tex`; generated `report-github-gitlab.md`; built `report.tex` via pandoc and `report.pdf` via pdflatex after falling back from lualatex; wrote this transcript.]*

Five files. The report runs to 8 pages across ten sections: figures of merit, what 5L removes, the reference table, the Monticelli/Huijsing distinction, the donor analysis of the 1994 paper, the bandwidth budget, FPBW, and a closing list of open questions.

The two Markdown variants differ only in math handling. The ReText one uses `$…$` and `$$…$$` for MathJax. The GitHub/GitLab one uses fenced ` ```math ` blocks for display equations, which both platforms render, and drops inline math to Unicode code spans — GitHub writes inline as `$x$` while GitLab writes ``$`x`$``, so there is no portable inline form.

Two things to flag:

I read "Plain TeX markup" as LaTeX and produced an `article` document, since that's what compiles to the PDF and what a report wants. If you meant Knuth's plain TeX proper (`\font`, `\hbox`, no document classes), say so and I'll redo it. The `.tex` compiles standalone with `pdflatex` in two passes; it uses `mathptmx` rather than `lmodern`, and carries `\DeclareUnicodeCharacter` declarations for the arrows, Ω, ≈ and so on, because the container's TeX Live is missing `lmodern.sty`. On your own machine you can delete both workarounds.

In the transcript, the one thing not reproduced verbatim is the body of the Hogervorst PDF you uploaded — that's a copyrighted IEEE paper, so it appears as an attachment line with the full citation. Every conversational turn is complete and unedited.

---

## Turn 10 — User

> ok you confused the reports for retext and for github/gitlab. Trivial to fix though.

## Turn 10 — Assistant

*[Tool use: swapped the two files' contents and rewrote the rendering note in each; re-copied both to the output directory.]*

Swapped. The `$…$` version is now the GitHub/GitLab one, since GitHub parses dollar math natively and ReText's Python-Markdown does not without the MathJax extension. The math-free version — fenced `math` blocks and Unicode code spans — is now `report-retext.md`.

Each file's rendering note was rewritten to match. The GitHub one carries a `sed` one-liner for converting inline math to GitLab's ``$`x`$`` form, which is the one thing the two platforms genuinely disagree about. The PDF and `.tex` are unaffected.

---

## Turn 11 — User

> update the verbatim report

## Turn 11 — Assistant

*[This turn: appended Turns 9–11 to the transcript.]*

---

*End of transcript.*
