<!--
SPDX-FileCopyrightText: 2026 Christoph Maier
SPDX-License-Identifier: Apache-2.0
-->
# Running log — improvements to the class-AB pad driver

Session 2026-10-02, Claude (configured model `claude-opus-5-5`; the serving model may differ).
Newest entries at the bottom. Times are Europe/Berlin, taken from the session transcript
(corrected 15:01: the first versions of several headings carried guessed times, up to 1¼ h too late).

Task as given: area, current and loop gain of `d2s_miller` / `d2s_loadcomp` are unsatisfactory,
probably because of the linear passives (rhigh degeneration, MOM Miller caps). Look in Edwards,
Minch, Cauwenberghs, Hasler (DoNotLitter/TimEdwards, LogDomain, FloatingGate) and
Sarpeshkar 1997 for (1) alternatives to resistor source degeneration in the DDA, (2) compensation
without linear BEOL capacitance, (3) cascoding with the output devices either doubling as ESD
clamps or as separate devices in the slot, (4) externally-linear / internally-nonlinear circuits
whose internal nonlinearity is not the subthreshold exponential. End result: proposed
improvements to `class_ab_pad_driver`.

Nothing is written to `~/DoNotLitter`. Papers are cited, not copied (chatlog/ref rule).

## 14:10 — baseline taken from the existing note and the first CACE run

What the CACE run (`verification/cace/first_run_summary.md`) adds to the design note:

- Gain spread 0.476…0.554 over PVT + rhigh corners, 0.41…0.61 in process MC. Cause: the gain
  is (R2 + 2/gm)/(R1 + 2/gm); R tracks R, but gm does not track R.
- Output offset in mismatch MC −32…+49 mV (4 degenerated pairs; offset referred through
  1/Gm of degenerated pairs is large).
- INL 469 mV worst corner; THD −15 dB at 1.25 V output (pairs run out of I_tail·R range).
- Output noise 1.6 µV/√Hz at 1 kHz (degeneration resistors + low Gm).
- Area: the two MOM Miller caps (2 × 31 × 31 µm) dominate the non-frame area (1920 of ~2500 µm²).
- Current: 427 µA, of which 240 µA output-stage quiescent, ~180 µA front end + bias.

## 14:25 — literature read so far (details in `literature_notes.md`)

- Sarpeshkar 1997 thesis (scanned, OCR'd locally on the linked computer), ch. 3 = the
  wide-linear-range OTA: well input, diode source degeneration, gate degeneration through
  the mirror diode, bump linearization (w = 2 cancels the cubic term). No resistors.
- Edwards thesis §3.5–3.10, Edwards & Cauwenberghs 2000: ELIN/log-domain; names the square law
  of strong inversion as the other usable internal nonlinearity; matching = "same surround".
- Minch thesis ch. 7: a source follower is linear whatever the device law (MITE via FG
  source follower, valid above threshold).
- Hasler thesis ch. 4–5, Sánchez-Sinencio FG slides: capacitive dividers / FG inputs widen
  linear range, but need linear caps and charge control (tunneling/injection or UV).

## 14:25 — simulation environment

Cloud container: ngspice-42 (Ubuntu), IHP-Open-PDK `dev` sparse checkout, OpenVAF-reloaded
built from source with LLVM 18 for psp103 / r3_cmc / cap_cmomi. (in progress)

## 14:28 — simulation environment ready, baseline reproduced

ngspice-42 + IHP-Open-PDK `dev` models + psp103 / r3_cmc / cap_cmomi compiled with OpenVAF-reloaded
(LLVM 18, OSDI minor version patched 4 → 3 for ngspice 42, as in the first session).
`run_d2s.py` functions reproduce `results.txt` exactly (A, 1 kΩ ∥ 100 pF: gain 0.5005,
0.18 mV, nonlin 5.52 mV, T0 66.5 dB, fc 1.62 MHz, PM 74.8°, THD 10 kHz −51.1 dB).

## 14:40 — DDA unit characterization (`sim/units.spice`; test bench now in `run_improvements.py units`)

Each unit is one split-tail PMOS pair; x = gp − gn swept ±0.8 V at input CM 1.40 / 1.65 / 1.90 V.

| unit | degeneration | Gm0 @ CM 1.40 / 1.65 / 1.90 | f(0.5)/(Gm0·0.5) | CM sensitivity of Gm |
|---|---|---|---|---|
| unit_r | rhigh 0.5 × 36.4 µm (108 kΩ), I_t = 2 × 10 µA | 15.54 / 15.55 / 15.58 µS | 0.996 | 0.5 %/V |
| unit_t | hv PMOS 0.5/3 in triode, gate at vss | 12.43 / 15.54 / 18.40 µS | 0.992 | 77 %/V |
| unit_w | Sarpeshkar well input, 4/4, gates at vss, 1 × 20 µA | 11.82 / 11.02 / 10.35 µS | 0.991 | −27 %/V |

The MOS alternatives are linear enough on their own; their problem is common-mode sensitivity
(triode R depends on V_SG = source − gate; well-input κ depends on well-to-gate voltage, as
Sarpeshkar's §3.3.1 reports). Why that matters for the next step: see 14:43 (a leftover "15:05"
from the guessed timestamps, corrected 16:15).

## 14:43 — matched-pair DDA (MP-DDA)

Idea: four identical units, A (vinp, vref), B (vref, vinn), C1 = C2 (vref, vfb):
f(vinp − vref) + f(vref − vinn) = 2 f(vfb − vref). With matched units the solution is
vout − vref = (vinp − vinn)/2 for *any* odd monotonic f (exact for input CM = vref; for a CM
error c the error is second order in c). Gain ½ = unit count ratio; no R1/R2, no gm term.
This is static ELIN: the input units compress, the feedback units invert the same law.
Caveat found analytically: A and C sit at CM vref + x/2, B at vref − x/2. A unit whose Gm
depends on CM (k per volt) gives v ≈ u − k u²/2 → unit_t ≈ 96 mV, unit_w ≈ 34 mV of
second-order error at u = 0.5 V, unit_r ≈ 0.6 mV. So in this topology the poly resistor
stays the right degenerator. Its area is ~18 µm² per unit, it never was the area problem.

First simulation, everything else unchanged (fold, mirror, class-AB, frames, MOM caps, bias):

| variant | load | gain | nonlin | T0 / fc / PM | THD 10 k / 100 kHz |
|---|---|---|---|---|---|
| baseline A | 1 k ∥ 100 p | 0.5005 | 5.52 mV | 66.5 dB / 1.62 MHz / 74.8° | −51.1 / −50.2 dB |
| MP-DDA, MOM | 1 k ∥ 100 p | 0.4998 | 1.04 mV | 66.5 dB / 1.62 MHz / 74.7° | −60.2 / −55.5 dB |
| MP-DDA, MOM | 100 p | 0.5000 | 1.02 mV | 96.5 dB / 2.03 MHz / 66.2° | −60.0 / −59.8 dB |
| MP-DDA, hv-PMOS accumulation cap 14 × 14 µm | 100 p | 0.5000 | 1.02 mV | 96.7 dB / 2.80 MHz / 53.4° | −60.0 / −59.9 dB |

Same current (427 µA) and tail budget (8 × 10 µA = baseline 4 × 20 µA). 9 dB better THD, 5×
lower DC nonlinearity. The MOS cap (196 µm² vs 961 µm² MOM) does not degrade THD despite a
2× C–V variation over 0.15…1.25 V (0.37 → 0.75 pF); it is just smaller than 1 pF on average,
so it needs resizing for the PM.

## 14:48 — MOS capacitor sizing, corners, mismatch

**MOS accumulation cap size** (MP-DDA, f_c / PM): 18 × 18 µm matches the 31 × 31 µm MOM pair
almost exactly (100 pF: 2.00 MHz / 67.0° vs 2.03 MHz / 66.2°; 300 pF: 46.3° vs 45.5°;
1 nF: 26.9° vs 26.4°). Area per side 324 µm² instead of 961 µm² (3.0×), no metal used.

**Corners** (dc gain fitted over |vd| ≤ 0.2 V, 1 kΩ ∥ 100 pF; nonlin = max deviation over ±1 V):

| corner | baseline A gain / nonlin | MP-DDA gain / nonlin |
|---|---|---|
| tt 27 | 0.5005 / 5.52 mV | 0.4998 / 1.04 mV |
| ss 125 (res wcs) | 0.5119 / 8.07 | 0.4988 / 1.56 |
| ff −40 (res bcs) | 0.4968 / 3.30 | 0.4998 / 0.66 |
| sf / fs 27 | 0.4998 / 4.11, 0.5013 / 8.07 | 0.4998 / 0.82, 0.4997 / 1.37 |
| ss 27 / ff 27 | 0.5022 / 12.69, 0.4990 / 3.30 | 0.4998 / 1.91, 0.4997 / 0.69 |
| tt res wcs / bcs | 0.4895 / 7.09, 0.5148 / 5.07 | 0.4997 / 1.48, 0.4998 / 0.66 |
| tt 125 / tt −40 | 0.5249 / 5.18, 0.4870 / 7.15 | 0.4983 / 1.10, 0.4998 / 1.53 |

Systematic gain spread −2.6…+5.0 % → −0.34…0 %. Loop gain / PM unchanged.
(Corrected 15:25: this line first said "±3.8 %", which was half the spread, not its range.)

**Mismatch MC** (30 seeds, `mos_tt_mismatch` + `res_typ_mismatch`, mm_ok=1 on all MOS and rhigh):
baseline offset σ 14.4 mV, MP-DDA σ 14.5 mV — the front-end change does not touch the offset.
Budget by device group (mismatch on one group at a time, 20 seeds): folding sinks 11.5 mV,
tails 4.2, mirror 2.3, pairs 1.7, everything else < 0.4. Same mechanism Sarpeshkar describes
(§3.3.4: current mismatch / transconductance; low Gm/I front ends are offset-prone, and the
mirrors, not the input devices, matter most).

## 14:53 — `d2s_mp2`: same topology, resized for current and offset

- units at 2 × 5 µA (long-L tails 5/6), R = 150 kΩ (rhigh 0.5 × 50.6 µm), I_t·R = 0.75 V
- folding sinks 30 µA, 36/6 (lower gm/I), mirror 24/4 at 10 µA
- bias fixture `d2s_bias_lp`: reference currents 5 + 5 + 2 + 2 + 5 + 5 µA instead of 20 + 50 + 5 + 5 + 5 + 5
- headroom limit found on the way: a ≈ 2.6 V and b ≈ 0.7 V are the output-device gates, so the
  mirror and the sinks each get only ~0.35 V; their overdrive can't be raised for matching,
  only their area.
- all devices ≥ 70 mV from saturation edge at vd = 0 (`oppoint.py`)

| | baseline A | d2s_mp2, MOS 16 × 16 |
|---|---|---|
| I_DD (incl. bias fixture) | 427 µA | 297 µA |
| I_Q P/N | 240 µA | 213 µA |
| compensation area | 2 × 961 µm² MOM (M1–M4) | 2 × 256 µm² hv-PMOS |
| T0 1 k ∥ 100 p / 100 p / 50 Ω | 66.5 / 96.5 / 40.7 dB | 69.7 / 99.6 / 43.9 dB |
| fc / PM, 100 p | 2.02 MHz / 66° | 1.76 MHz / 63° |
| THD 10 kHz (1 k ∥ 100 p) | −51.1 dB | −58.7 dB |
| THD 100 kHz (1 k ∥ 100 p) | −50.2 dB | −51.4 dB |
| nonlin (±1 V vd) | 5.52 mV | 1.24 mV |
| offset σ (mismatch, 30) | 14.4 mV | 5.3 mV |
| gain σ (mismatch, 30) | 1.6 % | 1.1 % (0.84 % from rhigh unit mismatch) |

Gain σ is now set by rhigh area (0.5 × 50.6 µm per unit): 4× the area halves it.

## 14:57 — the right figure of merit for a DDA unit (`sim/run_improvements.py units`)

The first unit test swept both inputs around a common CM. In the MP-DDA one input of every
unit sits at vref, so the relevant comparison is fA(x) = I(vref + x, vref) against
fB(x) = I(vref, vref − x): the same differential voltage, but the pair's sources sit x lower in B.
Solving fA(u) + fB(u) = 2 fA(v) from the unit curves alone predicts the whole driver's static
error; for unit_r it gives −1.04 / −1.02 mV at u = ∓0.5 V, which is the full-circuit 1.04 mV.

| unit | own compression at 0.5 V | MP-DDA error at u = −0.5 / +0.5 V |
|---|---|---|
| unit_r (split tails + rhigh) | 0.5 % | −1.0 / −1.0 mV |
| unit_t (triode PMOS) | 20 % | −191 / −72 mV |
| unit_w (well input) | 7 % | +29 / +38 mV |
| unit_q (undegenerated 2/6, square law, no R) | 22 % | +75 / +200 mV |

So the criterion for an ELIN unit here is not its linearity but that its output depends on
gp − gn only. The split-tail pair meets it because each device is a constant-current source
follower (Minch thesis ch. 7: a follower is linear whatever the device law) and the element
between the sources sees exactly gp − gn. Any element whose value depends on the absolute
source voltage (triode R, well κ, tail/CLM of a single-tail pair) fails.

## 14:56 — cascoding

**(a) output devices = ESD clamp frames.** A series cascode would put its drain, not the
clamp's, on the pad; a stacked-clamp frame would be a new ESD structure to qualify. So no
output cascode. What remains is cascoding the internal high-impedance nodes. Lengthening the
folded and mirror cascodes (L 1 → 3 µm, W scaled, same overdrive) in `d2s_mp2`:

| cascode L | T0 1 k ∥ 100 p | T0 100 p | T0 50 Ω | PM 100 p |
|---|---|---|---|---|
| 1 µm (d2s_mp2) | 69.7 dB | 99.6 dB | 43.9 dB | 63.4° |
| 2 µm | 75.4 | 103.1 | 49.6 | 62.8° |
| 3 µm (d2s_mp2c3) | 78.9 | 104.3 | 53.1 | 62.0° |

+9 dB for ~320 µm² of gate area. Regulated (gain-boosted) cascodes were not tried: node a sits
at ~2.6 V and b at ~0.7 V (the output gates), which leaves ~0.35 V per device for the mirror,
the sinks and their cascodes, so no headroom for an auxiliary amplifier's V_GS.

**(b) separate output devices in the slot.** Then they can be cascoded. Test case `d2s_lc2`:
load-compensated (topology B, no compensation capacitor at all), MP-DDA front end, half-frame
output devices, cascode gates simply at vref (output range ~1.0…2.4 V):

| | T0 | 5 p | 20 p | 100 p | 1 n | 1 k ∥ 100 p | I_DD |
|---|---|---|---|---|---|---|---|
| no cascode | 37.2 dB | 16° | 47° | 78° | 89° | no loop gain | 174 µA |
| cascoded | 74.0 dB | unstable | 39° | 77° | 89° | no loop gain | 169 µA |

Cascoding adds 37 dB; a resistive load still collapses a single-stage loop, and the minimum
load capacitance stays (~30–40 pF). In the slot, the pad goes through IOPadAnalog, whose
`padres` is behind 587 Ω (SecondaryProtection). Sensing at `padres` (near side) makes that
resistor an isolation resistor: PM at 20 pF 39° → 62°, 100 pF → 104°; the pad then sees a
587 Ω · C_L low-pass outside the loop (2.7 MHz at 100 pF). Sensing at `pad` keeps the PM of
the no-resistor case. 50 Ω through 587 Ω is not drivable at all.
Open point: the cascoded version has 7.8 mV systematic offset (diode replicas at a different
V_DS than the cascoded output devices); cascoding the diode replicas would fix it.

## 14:58 — noise (1 k ∥ 100 p, output-referred)

| | 1 kHz | 100 kHz | 10 Hz–10 MHz |
|---|---|---|---|
| baseline A | 1599 nV/√Hz | 200 nV/√Hz | 278 µV rms |
| MP-DDA (baseline sizing) | 1592 | 201 | 279 |
| d2s_mp2c3 | 676 | 152 | 231 |

## 14:59 — `d2s_mp2c3` (= d2s_mp2 with L = 3 µm cascodes, MOS caps 16 × 16 µm): full table

Renamed `d2s_mpdda` (`sim/d2s_mpdda.spice`); every number re-run in `sim/results_improvements.txt`. 296 µA (baseline 427), T0
78.9 dB at 1 k ∥ 100 p (66.5), 53.1 dB at 50 Ω (40.7), 104 dB capacitive (96.5), PM 62° at
100 pF, 42° at 300 pF. Gain 0.4992…0.5000 over 11 corners, nonlin ≤ 3.5 mV (ss 27 °C).
Offset σ 5.3 mV, gain σ 1.1 % (rhigh area). THD 10 kHz −58.5 dB; 100 kHz −51.3 dB
(1 k ∥ 100 p; lower fc than the MOM-MP version, 1.37 vs 1.62 MHz).

## 15:05–15:20 — consolidation

Intermediate netlists and scripts folded into one runner, `sim/run_improvements.py`, which reuses
`../run_d2s.py` unchanged and reproduces every number of this log and of
`proposed_improvements.md` in one run (3 min 49 s, `sim/results_improvements.txt`). The
re-run matches the numbers above. Files in `sim/`:

| file | content |
|---|---|
| `units.spice` | DDA units: unit_r (rhigh), unit_r2 (final, 2 × 5 µA), unit_t (triode MOS), unit_w (well input), unit_q (undegenerated) |
| `d2s_mp.spice` | MP-DDA in the baseline's sizing; compensation through the `ccomp` wrapper |
| `ccomp.spice` | ccomp_mom (as d2s_miller), ccomp_mos (hv PMOS accumulation caps) |
| `d2s_mpdda.spice` | the proposal (frames kept as output devices) |
| `d2s_bias_lp.spice` | bias fixture with 26 µA of reference current instead of 90 µA |
| `d2s_lc2.spice` | case (b): in-slot output devices, load-compensated, cascoded (and not) |
| `run_improvements.py`, `results_improvements.txt` | runner and its output |

## 15:18 — transfer check

Checksums of the committed files against the container copies: `proposed_improvements.md`,
`sim/results_improvements.txt` and `sim/run_improvements.py` did not match after the
first commits, although the tool reported "written". The device still held earlier
versions of them, 20530 / 16367 / 13939 bytes instead of 20571 / 18250 / 16300.
Re-committing from the same staged paths, with force, changed nothing. Committing copies
from a *new* staged directory (`outputs/xfer2/`) worked. All files now match by sha256.
This looks like the silent no-op described in the project CLAUDE.md, §6. Workaround: stage
every new version of a file under a new staged path.

## 15:20 — time and tokens used by this task

Wall clock: 14:08 → ~15:20, about 72 minutes, interrupted twice by questions. Of that, the
compute (not the model) took about 3 min for the OpenVAF build and model compile, about 6 min
for OCR on your computer, and about 10 min of ngspice in total, including the 3 min 49 s full
re-run.

Tokens, from this session's own transcript (`~/.claude/projects/-home-claude/<session>.jsonl`,
per API response, as of 15:19):

| phase | wall clock | API calls | output tokens | cache writes | cache reads |
|---|---|---|---|---|---|
| orientation: existing note, netlists, CACE results, CLAUDE.md | 14:08–14:12 | 14 | 20,138 | 106,368 | 1,958,053 |
| simulation environment + literature reading/OCR, interleaved | 14:12–14:27 | 49 | 23,126 | 122,848 | 12,499,286 |
| baseline reproduced; Caltech-thesis check | 14:27–14:31 | 6 | 2,887 | 13,684 | 1,960,595 |
| design reasoning + simulations | 14:31–15:00 | 40 | 125,771 | 157,464 | 17,134,286 |
| accounting, log timestamp correction | 15:00–15:02 | 5 | 10,264 | 17,604 | 2,485,393 |
| consolidated runner, re-run, notes, proposal, transfer checks | 15:02–15:19 | 37 | 60,208 | 98,924 | 21,839,596 |
| **total, main thread** | | 151 | 242,394 | 517,090 | 56,877,712 |
| subagent (Caltech PDF check) | 14:30–14:31 | 5 | 1,463 | 94,882 | 368,538 |

How to read it:

- **Output tokens** (~244 k): what the model wrote, including its reasoning. More than half
  of it falls in the design phase.
- **Cache reads** (~57 M): each API call re-reads the whole conversation so far from the
  prompt cache. The context grew from ~118 k tokens at the start (system prompt, tools,
  memory) to ~608 k at the end. The growth came mostly from tool output: paper text, OCR,
  netlists and simulation listings.
- **Cache writes** (~0.5 M): new context added to the cache.
- **Uncached input**: 302 tokens in all.

How cache reads, cache writes and output count against a specific plan's usage limits is not
something this log can state (not checked here); the plans' usage limits are documented at
support.claude.com. What this kind of task pushes is the context size and the number of
calls made over it.

What drove the size, for planning similar tasks:

- Reading papers as text into the conversation: Edwards, Minch and Hasler excerpts and the
  Sarpeshkar OCR, roughly 100–150 k tokens of context.
- Long simulation listings.
- A long reasoning phase before the first simulation.

A second session that starts from `proposed_improvements.md` and `log.md` instead of the
papers would begin with far less context.

## 15:55 — IEEEtran version

`proposed_improvements.tex` is `proposed_improvements.md` in IEEEtran journal style: the same
content and numbers, with equations and a references list taken from `literature_notes.md`.
`proposed_improvements.pdf` (5 pages) was built in the cloud with pdflatex, run twice, and
had no errors and no overfull boxes. The only packages it needs besides IEEEtran.cls are
amsmath, booktabs, tabularx, array, textcomp, url and cite; there is no siunitx. The sandbox
I reach on the linked computer has pdflatex but neither IEEEtran.cls nor siunitx. Building
there needs TeX Live's `texlive-publishers`, or a copy of IEEEtran.cls next to the file.

## 16:06 — time and tokens, updated through the LaTeX work

Same method as at 15:20, now including the report, the questions afterwards and the two LaTeX
conversions:

| phase | wall clock | API calls | output tokens | cache writes | cache reads |
|---|---|---|---|---|---|
| orientation | 14:08–14:12 | 14 | 20,138 | 106,368 | 1,958,053 |
| simulation environment + literature/OCR | 14:12–14:27 | 49 | 23,126 | 122,848 | 12,499,286 |
| baseline reproduced; Caltech-thesis check | 14:27–14:31 | 6 | 2,887 | 13,684 | 1,960,595 |
| design reasoning + simulations | 14:31–15:00 | 40 | 125,771 | 157,464 | 17,134,286 |
| accounting, log timestamp correction | 15:00–15:02 | 5 | 10,264 | 17,604 | 2,485,393 |
| runner, re-run, notes, proposal, transfer checks, report | 15:02–15:20 | 41 | 64,333 | 102,341 | 23,278,772 |
| questions about the spreadsheet button | 15:20–15:52 | 1 | 427 | 6,984 | 613,327 |
| IEEEtran LaTeX of the proposal | 15:52–16:04 | 16 | 32,152 | 45,403 | 10,226,268 |
| resource-log question; start of the log's LaTeX | 16:04–16:06 | 2 | 1,576 | 7,552 | 1,339,858 |
| **total, main thread** | | 174 | 280,674 | 580,248 | 71,495,838 |
| subagent (Caltech PDF check) | 14:30–14:31 | 5 | 1,463 | 94,882 | 368,538 |

The context is now ~674 k tokens per call. The LaTeX conversion of this log comes after this
table and is not in it.

## 16:15 — LaTeX version of this log

`log.tex` / `log.pdf` (article class, not IEEEtran, in the style of
`sudelbuecher/esd_protection/*.tex`). The body was converted from this file with pandoc 3.1.3,
and the tables were given widths weighted by their content. Builds with pdflatex using only
standard packages (booktabs, longtable, calc, hyperref, xurl, microtype, textcomp, geometry).
A snapshot: entries after 16:15 are only in `log.md`.

## 16:37 — testbench decks in `sim/tb/`

Nine stand-alone ngspice decks, so the results can be rerun without `run_improvements.py`:
`tb_mpdda_dc`, `tb_mpdda_loop`, `tb_mpdda_step`, `tb_mpdda_thd`, `tb_mpdda_noise`,
`tb_mpdda_op`, `tb_units`, `tb_moscv` and `tb_lc2_loop`. Each one names its reference value from `results_improvements.txt` in the header
and runs from its own directory (`ngspice -b <deck>` prints, `ngspice <deck>` plots). They need
the PDK `.spiceinit` (sourcepath to the models, OSDI for psp103, r3_cmc and cap_cmomi). Rerun in
the cloud, they reproduce the reference: gain 0.49994, offset 0.055 mV, nonlinearity 1.243 mV,
Idd 296 µA; loop 78.9 dB, 1.366 MHz, 72.4°; THD 0.119 %; noise 676 / 152 nV/√Hz at 1 / 100 kHz;
`d2s_lc2` near side 74.0 dB, 1.49 MHz, 104.3°.

## 17:00 — xschem schematics in `xschem/`

First drafts for hand editing, laid out like the hand-edited `../xschem/d2s_miller.sch`: ports
in one column on the left, output on the right, vdd and vss as wires across the sheet, one column
per current branch, bulks wired, and the input and bias nets as wire buses from the port column.
Internal nets carry `lab_wire` labels so that the netlist keeps the source's net names.

- `unit_r2` (the unit of `d2s_mpdda`), and `unit_r`, `unit_t`, `unit_w`, `unit_q`. All five share
  one box symbol: gp and gn on the left, vdd and vbp on top, x, y and vss at the bottom.
- `d2s_mpdda`: four `unit_r2` boxes; the fold, mirror, class-AB pair and output devices sit
  where they are in `d2s_miller.sch`. CMA and CMB are drawn as hv PMOS accumulation capacitors.
- `d2s_lc2` and `d2s_lc2_nc`: the same core. The output cascode gates reach vref through one
  `lab_pin`.
- `d2s_bias_lp`, and `d2s_mpdda_biased`, the CACE fixture, which is wired like
  `d2s_miller_biased.sch`.
- The symbols of `d2s_mpdda`, `d2s_lc2(_nc)`, `d2s_bias_lp` and `d2s_mpdda_biased` are copies
  of `d2s_miller.sym`, `d2s_bias.sym` and `d2s_miller_biased.sym`, which have the same port lists.

Parameters are frozen at the `.subckt` defaults:

- lcas = 3, so CX, CY, PCL and PCR are 30u / 3u with ng = 2.
- wc = lc = 16u.
- rl = 50.6u in `unit_r2` and 36.4u in `unit_r`.
- iab = 5u, ibnc = 2u, wdp = 6.66u, wdn = 3.8u.
- `unit_w` keeps `w=wwi l=lwi`, which the testbench defines.

Not drawn: `d2s_mp`, whose `ccomp` wrapper exists only in the testbench, and
`ccomp_mom` / `ccomp_mos`; `ccomp_mos` appears in `d2s_mpdda` as CMA and CMB.

`check_xschem.py` netlists every `.sch` with xschem and compares each subcircuit in the netlist
with `../sim/*.spice`, device by device. It checks model, nets in order, w / l / ng / value, and
the port order of both `.sch` and `.sym`. With xschem 3.4.4 it finds 0 mismatches over the 10
cells, including the `unit_r2` bodies inside the parents. It did report each deliberate error I
introduced: a changed port label, a resistor length, a current value and two swapped `.sym`
pins.

In the first draft, nets l2 and b came out split (net1, net2). A bus crossed the middle of a
column without a junction, and xschem connects a wire only at its end points. Hand edits can
break connectivity the same way, so rerun `check_xschem.py` after editing. Most of the 106 wire
crossings in `d2s_mpdda` are in the input and bias bus band under the four units; that band is
the obvious place for hand rearrangement or for labels. The script that drew the sheets stays
in the cloud, since the drafts are meant to be edited by hand from here on.

## 17:15 — LaTeX log brought up to date

`log.tex` and `log.pdf` were regenerated from this file through this entry, with the same steps
as at 16:15 (pandoc, then the table widths). They are still snapshots: entries after this one
are only in `log.md` until the next regeneration.

## 17:35 — block annotations, flat schematics, `xschem/README.md`

Every sheet now outlines its functional blocks with magenta dashed boxes tagged [1] to [9], with
a legend under the sheet. A number means the same block on every sheet: [1] DDA units, [2] fold,
[3] mirror, [4] class-AB control, [5] its copy in the mirror input branch, [6] output devices,
[7] Miller capacitors (cascodes in `d2s_lc2`), [8] bias, [9] diode replicas in `d2s_lc2`.
`xschem/README.md` explains the blocks with sizes, nets and tt currents, gives the signal path
and the bias network, and lists the files.

Two new sheets show everything at transistor level:

- `d2s_mpdda_flat`: `d2s_mpdda` with the four units drawn out. Unit devices and nets carry the
  unit's name (`Ta_A`, `sa_A`, ...). It has the same 13 pins.
- `d2s_mpdda_bias_flat`: `d2s_mpdda` and `d2s_bias_lp` on one sheet, with the bias columns
  between the port column and the units. It has 7 pins; the bias nets are internal.

`check_xschem.py` compares the flat sheets with the sources with the subcircuits expanded under
that naming. 0 mismatches over 12 cells. A swapped unit-net label and a changed rhigh body were
both reported.
