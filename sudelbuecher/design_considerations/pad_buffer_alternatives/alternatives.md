<!--
SPDX-FileCopyrightText: 2026 Christoph Maier
SPDX-License-Identifier: Apache-2.0
-->
# Alternatives to the Source-Degenerated Pad Buffers: Less Area, More Bandwidth, Wider Range, Preferably Without Poly Resistors

*Literature survey and synthesis. No simulation, no layout, not reviewed. Prepared for C. H. Maier,
drafted with Claude (configured model `claude-fable-5-1`; the serving model may differ), 26 October 2026.
Companion to `../class_ab_pad_driver/` and `../s2d_input_buffer/`. The four search reports this draws
on are in `research/` (verbatim, with their sources); running log `log.md`.*

**Summary.**

- **The resistors are not where the area is.** In `d2s_mpdda` the four rhigh strips are about 100 µm²
  of 2014 µm² drawn; the long-L tails and sinks (≈ 670 µm²), the cascodes and loads (≈ 550 µm²) and the
  two MOS Miller capacitors (512 µm²) are. In `s2d_mpdda` the six units' tails plus the three fold
  branches and the two MOS load capacitors dominate the same way. Removing the resistors is a spread
  and gain-σ decision (0.84 % gain σ is all rhigh), not an area decision.
- **Three things govern the three targets** (§II): (1) for any class-A unit, MOS-linearized or
  resistor-linearized, Gm × linear range ≈ I_tail, so bandwidth at a given range is a current decision
  unless the unit is class AB; (2) in the matched-pair DDA the absolute Gm spread cancels, only
  unit-to-unit mismatch and the dependence of the unit's output on its common mode matter (the rule of
  `proposed_improvements.md` §II); (3) the d2s loop cannot cross above about a third of the pad pole,
  (g_mP + g_mN)/(2π C_L) ≈ 10 MHz at 100 pF, so "faster than 1 MHz" means 3 MHz at 100 pF and 10–15 MHz
  at 20 pF, whatever the front end.
- **MOS-only units that can replace `unit_r2`** (§III), to be tested with the existing unit bench:
  Krummenacher–Joehl triode degeneration whose gates follow the inputs (closest drop-in), the Nauta
  inverter pair (smallest, widest range at 3.3 V, common mode pinned near vdd/2), the large-overdrive
  pair with a cascoded tail (the `unit_q` idea done with the headroom it needs), and the cross-coupled
  square-law quad. Bulk-driven units stay rejected (`unit_w`). Class-AB units are the only way past
  Gm × range ≈ I_tail.
- **Architecture levers** (§IV): one bias root per slot (already in `FILL_IN.md`); current sources at
  V_ov ≈ 0.5–0.6 V instead of 0.3 V (halves the W·L for the same σ, from the PDK's own mismatch
  parameters); s2d as two unity-gain DDAs on an explicit vcm instead of a gain-2 FDDA with CMFB (four
  units instead of six, no CM loop); for the d2s, the two Miller capacitors go only if the pad load is
  specified as purely capacitive (topology B of the first note), otherwise they stay and the loop speeds
  up through Gm.
- **Range** (§V): the internal ±1 V around 1.2 V and the pad ±0.5 V are inside the PMOS window at
  vdd ≥ 3.0 V. A wider pad range needs units with a wider common-mode range, i.e. complementary N + P
  pairs; the CFIA literature puts the price at 3× the gain error when the two ports sit at different
  common modes. For the s2d, gain 2 around 1.2 V caps |vin − vref| at about 1 V on headroom alone.
- **No open-source precedent** solves this problem in sg13cmos5l thick-oxide devices (§VI). Edwards'
  `sky130_ef_ip__opamp` (1 941 µm², 2.4 MHz, rail-to-rail output, full CACE datasheet) is the closest
  open 3.3 V buffer with a layout number, and its CACE parameter set is worth copying.
- **Recommendation** (§VII): keep the matched-pair DDA, replace the unit, not the architecture; run
  the four candidate units through the `fA`/`fB` bench with the DDA-error and Gm-vs-CM criteria;
  take the area from the current sources and the bias sharing; fix the load specification before
  spending anything on bandwidth.

---

## I. Starting Point

From `../class_ab_pad_driver/improvements/proposed_improvements.md`, `../s2d_input_buffer/s2d_input_buffer.md`
and `../pad_buffer_layout/layout_primitives.md`:

| | `d2s_mpdda` | `s2d_mpdda` |
|---|---|---|
| units | 4 × `unit_r2` | 6 × `unit_r2` (4 signal + 2 CMFB) |
| unit | 20/1 PMOS pair, 2 × 5/6 tails, rhigh 0.5 × 50.6 µm (150 kΩ) | same |
| Gm per unit | 15.6 µS | 15.6 µS |
| fold | SX/SY 36/6 × 4, cascodes 30/3, loads 24/4 | SX/SY/SXC 6 × 6/6, cascodes 30/3, loads 24/4 |
| compensation | 2 MOS Miller caps 16 × 16 | 2 MOS load caps 12 × 12 |
| drawn area | 2014 µm² (3500 with spacing) | 2680 µm² (≈ 5500 with spacing) |
| I_DD | 296 µA | 99 µA (+ 19 µA tree) |
| loop | 1.5–2 MHz, 67–79 dB | 1.6 MHz, 67.6 dB |
| offset σ | 5.3 mV (sinks 4.3) | 5.9 mV |
| gain σ | 0.84 % (rhigh) | 1.1 % |
| input window | gates ≥ 1.3 V below vdd | same |

Drawn area of `d2s_mpdda` by group (W·L from the netlist): tails 8 × 5/6 = 240 µm²; sinks 2 × 36/6 = 432;
cascodes 4 × 30/3 = 360; loads 2 × 24/4 = 192; pairs 8 × 20/1 = 160; AB and replica 4 devices ≈ 40;
Miller caps 2 × 256 = 512; rhigh 4 × 25 = 100. The resistors are 5 %.

## II. What Governs Area, Speed and Range

**Gm × range ≈ I_tail (class A).** A source-coupled pair steers fully at v_id = √2·V_ov with
g_m(0) = I_tail/V_ov, so g_m × v_range ≈ √2·I_tail. A resistor-degenerated pair has Gm ≈ 1/R and
v_range ≈ I_tail·R, so Gm × v_range ≈ I_tail. `unit_r2`: 15.6 µS × 0.75 V = 11.7 µA ≈ its 10 µA of tail
current. Every class-A linearization sits on this line; what it chooses is the *shape* of Gm(v), the
headroom, the noise and the area. To get 10× the Gm at the same range, the unit needs 10× the current, or
it must be class AB (its tail current must grow with the signal). (`research/3_…` §0.)

**Only common-mode dependence and mismatch matter.** The gain ½ (d2s) and 2 (s2d) are unit counts, so the
absolute Gm of the unit, and its process and temperature spread, cancel. They move the loop bandwidth,
nothing else. This is the argument that removes the usual objection to triode-MOS degeneration and to
inverter transconductors (their Gm spreads ±30 % with process) in *this* circuit. What does not cancel is
the dependence of a unit's output on where its sources sit: the A and B units see the input common mode
move by ±u/2, the feedback units by +v/2. This is the rule `proposed_improvements.md` §II established, and
`unit_t` (77 %/V), `unit_w` (−27 %/V) and `unit_q` (−72 %/V) failed it while `unit_r` passed (0.6 %/V).
The CFIA literature measures the same effect on silicon: 0.04 % gain error with equal input and feedback
common modes, 0.12 % with unequal ones (Wu et al., JSSC 2012). So the test for any new unit is the
existing bench: sweep f_A(x) and f_B(x), solve f_A(u) + f_B(u) = 2 f_A(v), and read the DDA error at
u = ±0.5 V.

**The pad pole caps the d2s.** The output pole is (g_mP + g_mN + 1/R_L)/(2π C_L): 9.5 MHz at 100 pF,
48 MHz at 20 pF with I_Q ≈ 240 µA (`class_ab_pad_driver.md` §V). A two-stage loop crosses at most at
about a third of that with 60° margin. A faster d2s than ≈ 3 MHz at 100 pF needs more output-stage
quiescent current, not a better front end. At 20 pF, 10–15 MHz is open. The s2d, into 1.1 pF total, is
Gm-limited: f_c ≈ ½ × 2 Gm/(2π C) ≈ 2 MHz now, and scales with Gm directly.

**Headroom at gain 2.** With voutp − voutn = 2 (vin − vref) around vcm = 1.2 V on a 3.3 V rail, each
output moves ±(vin − vref) and the fold can swing to about 0.2 V and 2.9 V, so |vin − vref| ≤ 1.0–1.2 V
whatever the input stage does. "Wider range" for the s2d therefore means a wider *common-mode* window
for vref (and for vin's DC level), not a wider signal. (`research/2_…` §0.)

## III. Units Without Resistors

The candidates, with what the literature reports and what they would do here. All are to be judged by the
bench of §II, not by their own linearity. "Area" is relative to `unit_r2` (≈ 65 µm² drawn: 240/4 of tails,
40 of pair, 25 of rhigh).

| unit | principle | resistors | linear range at 3.3 V, V_t 0.7 | Gm per µA | CM dependence (risk) | area vs `unit_r2` | source |
|---|---|---|---|---|---|---|---|
| **K–J triode degeneration** | one or two triode PMOS between the split-tail sources, gates tied to the *input* gates so V_GS of the triode device follows the input device's V_GS | no | ±0.75 V needs V_ov ≈ 0.8 V on the triode device → gate about 1.5 V below the source; fine at 3.3 V | as `unit_r2` (class A) | low: the triode conductance follows the followers' V_GS, which the tail fixes; residual from V_DS/V_GS asymmetry — this is the difference from `unit_t`, whose gate sat at vss | about equal (the triode device replaces 25 µm² of rhigh) | Krummenacher & Joehl, JSSC 1988; Kuo 2010 survey (`research/3_…` C7) |
| **Nauta inverter pair** | two hv CMOS inverters as transconductors, N/P square-law cancellation, no tail, no internal node; four more inverters set the output CM in Nauta's filter, here the fold does it | no | ±(vdd/2 − V_t) ≈ ±0.95 V around vdd/2 | Gm ∝ (vdd − V_tn − |V_tp|); ≈ 2 I_Q/0.95 V, i.e. ≈ 2× a class-A pair at the same current, N and P both contribute | **high**: the input CM must sit near vdd/2 = 1.65 V (not 1.2 V), and Gm tracks vdd; no tail means no CM rejection — the matched-pair balance must absorb it, which the bench will show | smallest (4 short devices, no tails, no well per unit if all P in one well) | Nauta, EL 1990; Barthélemy 2008; MDPI 2023 FDDTA (`research/3_…` C10, `research/2_…` C2) |
| **large-V_ov pair, cascoded tail** | `unit_q` with the tail cascoded and the pair at V_ov ≈ 0.5 V | no | ±0.5 V per unit at 10 % flatness (±1 V would need V_ov 1.5–2 V: no) | 1/V_ov·I ≈ 2 µS/µA (same line) | medium: `unit_q` failed at −72 %/V, most of it the tail dropping out of saturation near vdd; a cascoded tail and V_GS ≈ 1.2 V leave 3.3 − 1.2 − 0.6 ≈ 1.5 V of CM window | smaller (no rhigh, short pair, one tail) | TAMU large-signal pair; Pelgrom (`research/3_…` C1) |
| **cross-coupled square-law quad** | two pairs with ±V_B level shifts, square terms cancel, I_out = K V_B v_id | no | ±1 V proven at 5 V with THD < 0.2 % (Klumperink 1989); at 3.3 V the shift V_B stacks on V_GS and eats CM window | class A | medium: "balanced inputs only" and PVT-sensitive per the surveys; with level-shift followers the sources are copied, so body effect is out | 2–4× | Seevinck & Wassenaar 1987; Klumperink 1989 (`research/3_…` C2) |
| **adaptive-bias / super class-AB pair** | tail current grows with v_id² (squarer) or FVF-fed pairs; the only way past Gm × range ≈ I_tail | no | ±1 V possible; Gm not flat | > class A, rises with signal | medium–high: Gm(v) is not flat, so the two ports must be identical cells at identical CMs; fine inside the loop, the balance does the rest | 1.5–2× | López-Martín et al., JSSC 2005; Kuo 2010 (`research/3_…` C5, C6) |
| **complementary N + P pair** | PMOS pair for low CM, NMOS pair for high CM, summed in the fold | no | rail-to-rail CM; linear range as the single pair | 1–2× (both on in 1.3–2.0 V) | **high**: gm varies 2× over CM without control, 5–28 % with constant-gm control; the CFIA data (0.04 % → 0.12 %) is this effect | 2× plus the current switch | Hogervorst 1994; Gharbiya & Phang 2002 (`research/3_…` C14, `research/1_…` #11) |
| bulk-driven | already `unit_w` | no | — | 0.2–0.4× | failed (−27 %/V) | — | rejected |
| FVF-degenerated (reference point) | resistor between two FVF nodes, Gm = 1/R exactly, class AB | **yes** | wide | class AB | low | 1–1.5× | Witte 2008; Carvajal 2005 (`research/3_…` §3) |

Three remarks:

- The K–J unit is the one to try first. It is `unit_t` with one change (the degeneration gates on the
  inputs instead of vss), it keeps the split tails and the follower argument of `proposed_improvements.md`,
  and its process spread is a bandwidth effect only. The one new requirement is V_ov ≈ 0.8 V on the triode
  devices, which costs about 0.3 V of input window against `unit_r2`.
- The Nauta unit is the only resistor-free unit that reaches ±1 V per side at 3.3 V, and the only one
  whose Gm per µA is clearly better than the class-A line. Its price is that the common mode is the
  supply's midpoint: the internal common mode would move from 1.2 V to about 1.65 V, which the s2d note
  rejected for `unit_r2` (nonlinearity 62 mV at vcm = 1.65 V) — but for a different reason, the PMOS
  headroom, which the inverter does not have. The second price is PSRR: Gm ∝ vdd, so the two ports see
  the same Gm change, and the balance cancels it to first order; the bench decides.
- Resistor-free does not shrink the cell. Every row above except the Nauta unit lands within ±50 % of
  `unit_r2`'s area, because the tails are the unit's area, not the strip of rhigh.

## IV. Architecture Levers (Where the Area Is)

1. **Bias sharing.** `bias_ctrl` with its own OA core and bandgap core in every pad is what breaks the s2d
   fit (`layout_primitives.md` §4). One root per slot, one 5 µA leg per pad. Already `FILL_IN.md` point 1.
2. **Current sources at higher overdrive.** From the PDK's `sg13g2_moshv_mismatch.lib` (the sg13cmos5l tree
   on this computer uses the same files): A_VT 7.0 mV·µm (hv NMOS) / 4.5 mV·µm (hv PMOS), A_β 0.5 / 0.4 %·µm.
   Pelgrom: σ²(ΔI/I) = 4 σ²(V_t)/V_ov² + σ²(β). An hv NMOS sink of 20 µm² at V_ov = 0.3 V has 1.05 % σ;
   at V_ov = 0.6 V, 0.53 %. Halving W·L at V_ov 0.6 V gives the σ of the full area at 0.3 V. The sinks
   (SX, SY, BN) carry 4.3 of the 5.3 mV offset, so this is where the offset budget and the area budget meet.
   At 3.3 V the headroom for 0.6 V overdrives exists on the NMOS side; the PMOS tails sit in the units'
   headroom and cannot go as far. The `sink_6x6` check of 26 Oct (one finger cell for both pads) is the
   same lever on the layout side.
3. **s2d as two unity-gain DDAs.** voutp − vcm = vin − vref and voutn − vcm = vref − vin are two unity-gain
   DDAs (Säckinger & Guggenbühl) with the common mode applied explicitly at vcm: 2 units each, 4 in all,
   no CMFB units, no CM loop, no CMFB dump branch (open point of the s2d note). The cost is two
   single-ended folds (4 branches) instead of one differential fold plus the CMFB branch (3), and the
   outputs are two independent single-ended nodes whose mismatch appears as output CM error directly
   (no loop to remove it). The output CM is then set by matching, not regulated — acceptable only if the
   d2s's input units tolerate a CM error of a few tens of mV, which the second-order argument of
   `proposed_improvements.md` §II says they do. (`research/2_…` C1.)
4. **Compensation.** The d2s's two 16 × 16 MOS caps (512 µm²) are the single largest item. They go only
   with topology B (load compensation), which `class_ab_pad_driver.md` §VI showed fails with resistive
   loads (1.6 dB loop gain at 1 kΩ). If the Chipalooza pad load is specified as capacitive only, B is back
   on the table and the LCD-driver literature (`research/1_…` tier 1: 625–2900 µm² for complete rail-to-rail
   class-AB buffers in 0.35 µm, no capacitor) says how small such a cell gets. Otherwise the caps stay
   and the bandwidth comes from Gm (§II).
5. **Transistor-only CMFB** (if the FDDA stays): triode-MOS sense devices instead of resistive averaging
   or DDA units, −37 % amplifier area in an 0.18 µm example; nonlinear detector, CM-to-DM conversion at
   ±1 V swing. (`research/2_…` C4.) Second to lever 3.
6. **Cascode length.** Already listed in `layout_primitives.md` (L 3 → 2, −500 µm², −3.5 dB).

## V. Range

- **d2s.** Inputs: internal v_d = ±1 V around 1.2 V puts the gates at 0.7–1.7 V, inside the PMOS window
  at vdd ≥ 3.0 V (limit 1.7 V). Output: pad ±0.5 V around 1.2 V, seen by the feedback units at the same
  window. The output stage itself swings rail to rail. A wider pad swing (say 0.3–3.0 V) is a wider
  common-mode range for the feedback units, which only complementary units give (§III), at the cost of
  the Gm(CM) dependence the matched-pair principle is most sensitive to. A MOS-only attenuator in the
  feedback (source-follower level shift) moves the window, it does not widen it. Recommendation: do not
  pay for rail-to-rail unless a slot pin needs it; the next step after `unit_r2` is a unit with the same
  window and higher Gm, not a wider one.
- **s2d.** The signal range is headroom-limited to about ±1 V by the gain of 2 (§II). The window that can
  widen is the DC level of vref and vin: PMOS units take 0 to about vdd − 1.5 V. A pad reference above
  2 V needs NMOS units (complementary again). The pad behind `padres` tolerates any DC level; the question
  is only whether the buffer stays in regulation there.

## VI. Precedents

`research/4_…` (summary table there). Nothing in sg13cmos5l / sg13g2 thick-oxide with area and bandwidth.
Closest open designs: Edwards `sky130_ef_ip__opamp` (3.3 V, 1 941 µm², 2.37 MHz GBW, 122 µA, output
0.000–3.300 V, CACE RCX datasheet); MarvinBrth RRIO class-AB op amp (sky130, 3.3 V, 3.1 MHz, ICMR
0.05–3.25 V, 259 µA, poly resistors and three MIM caps); YacineSot's Chipalooza #2 FD class-AB OTA in
sg13cmos5l (1.5 V LV devices, 40–50 MHz at 0.1 pF, MOScap compensation, resistive CMFB); Rodovalho
AICSP2022RAIL (sky130 5 V devices, bulk-driven input, class AB, no resistors in the netlist; numbers not on
GitHub). The LCD column-driver family (`research/1_…`) is the right literature for a small MOS-only
class-AB buffer with the dominant pole at the load: Marano 2010 625 µm², Arslan 2015 1380 µm², Osmani 2021
2904 µm² (11 transistors), Grasso 2018 5562 µm² — all 0.35 µm, 3–3.3 V, 1 nF, 1–8 µA; none above 2 MHz at
100 pF as published.

## VII. Recommendation and Next Steps

1. **Keep the matched-pair DDA.** It is what makes the gain independent of the absolute spread of whatever
   element linearizes the unit, which is the property the resistor-free units need most.
2. **Bench four units** with the existing `fA`/`fB` sweep and the DDA-error criterion (≤ 2 mV at ±0.5 V,
   Gm vs CM ≤ 1 %/V): `unit_k` (K–J, gates on the inputs), `unit_n` (two hv inverters), `unit_q2`
   (large V_ov, cascoded tail), and, if `unit_k` passes, its class-AB variant. One netlist each, the
   existing `run_improvements.py` functions, no new scripts.
3. **Area:** bias root per slot; sinks and tails at V_ov 0.5–0.6 V where the headroom allows, sized by
   σ from the PDK's A_VT; s2d as two unity-gain DDAs if the output CM error of an unregulated pair of
   outputs is acceptable to the d2s; cascodes at L = 2. These, not the resistors, are the 1000–2000 µm².
4. **Speed:** settle the pad load (20 pF or 100 pF; resistive or not) first — it caps the d2s at about
   3 MHz (100 pF) or 10–15 MHz (20 pF). Then raise the unit current or go class AB; the s2d scales
   with Gm directly.
5. **Range:** stay with the PMOS window unless a slot pin needs more; complementary units are the answer
   if it does, with the gain-error penalty measured, not assumed.

## References

The four reports in `research/` carry the full source lists. Named here: Säckinger & Guggenbühl, JSSC 1987;
Krummenacher & Joehl, JSSC 1988; Nauta, EL 1990 / JSSC 1992; Seevinck & Wassenaar, JSSC 1987; Klumperink et
al., EL 1989; Hogervorst et al., JSSC 1994; de Langen & Huijsing, JSSC 1998; Wu, Chae, Huijsing, Makinwa,
JSSC 2012; Witte, Huijsing, Makinwa, JSSC 2008; López-Martín et al., JSSC 2005; Carvajal et al., TCAS-I 2005;
Grasso, Palumbo, Pennisi, TCAS-II 2018; Marano, Palumbo, Pennisi, JCSC 2010; Osmani, Arslan, Kiyak, ICECET
2021; Kuo, IntechOpen 2010; Pelgrom et al., JSSC 1989; Drennan & McAndrew, JSSC 2003; IHP-Open-PDK
`sg13g2_moshv_mismatch.lib`; RTimothyEdwards/sky130_ef_ip__opamp (GitHub).
