<!--
SPDX-FileCopyrightText: 2026 Christoph Maier
SPDX-License-Identifier: Apache-2.0
-->
# K: messages

Agent K of session C2 (capacitors for CMA / CMB, with ngspice). Model Opus, effort medium (brief C2, table "Models").
Started by the lead on 2026-10-31 at about 16:22 CET, in the cloud session's container. Workspace `/home/user/c2/K/`
(`inputs/` read-only: a `git archive` of `toplevel` 8a72dd8 as `inputs/repo/`, and `inputs/notes/` with A5's brief,
A5's `inputs.md`, the two PDK PDFs as text from A5's `work/txt/`, `layout_primitives.md`, the ESD notes, C1's report).

## about 16:22, launch prompt (verbatim)

> You are agent K, an investigative agent for an analog IC designer working on the IHP sg13cmos5l process. Your whole task is in the brief file `/home/user/c2/K/BRIEF.md` — read it first and follow it exactly, including its rules (work only in `/home/user/c2/K/`, `inputs/` read-only, no git, no web searches, no mcp tools). The question is whether the Miller capacitors CMA and CMB of the output pad (two hv PMOS MOS capacitors, 256 µm² gate area each) can be replaced by, or split between, other capacitor types of the PDK so that capacitance remains over the whole output swing, with ngspice C(V), a DC swing of the pad, and the loop's phase margin for the best splits. Write results in four stages into `/home/user/c2/K/out/report.md` and announce each stage in `out/announcements.md` as the brief says. When done, reply with a summary of no more than 15 lines: the short answers, the recommended option with its area and phase margin, and the open points.

## 16:43, from the lead (verbatim)

> From the lead, relaying Christoph (2026-10-31, about 16:50 CET), verbatim: "Leave CMB as is for now. When task F reports back, discuss options what to do with CMB. Maybe it's advantageous to split CMB into different parallel capacitors that, combined, will be a linear-ish capacitor without the area requirements of an actual linear, passive, capacitor."
>
> For your stage 3 (splits) and stage 4 (phase margin): treat this as a design target for CMB in particular. Look for parallel combinations of MOS-type capacitors (e.g. hv PMOS in accumulation in both orientations, moscap_n / moscap_p, S-Varicap) whose C(V) curves complement each other, so that the sum is roughly flat over the voltage CMB sees across the whole pad swing. Compare them with a passive MOM capacitor of the same capacitance on area and flatness (max/min of C over the swing). Keep within your deck limit, and carry on with your stages as briefed. No reply needed.

## 17:33, K's final reply (summary)

All four stages in `report.md` (9 of 10 decks). Model files match A5's hashes. S-Varicap = the thick-oxide gate that does
not invert; the hv PMOS loses C in depletion, not inversion. MOM: only M1–M2, 1270 µm² per capacitor. Linear swing 0.94–2.31 V;
PM at 100 pF 72.6–78.4° (present), 71–80° for every variant; flattest CMB = S-Varicap 80 % ∥ turned 20 % (max / min 1.04,
≈ 400 µm²). Recommendation: CMA as is; CMB as is for now; first option "turn CMB around" (74.6° mid-rail, ≥ 40.4° at
300 pF, fits). Open: S-Varicap breaks CACE convergence (klu); 300 pF unloaded PM 39.7° at pad 2.29 V (driver); a second
stable state at the top rail.

## 17:3x, the lead's check

Logs grepped: `Transient op started` only in deck 9 v4 (S-Varicap pair at 300 pF), which K reports as invalid and leaves
out; no `Timestep too small`; the "gmin stepping failed" runs continue with completed source stepping (valid ops).

## about 18:05, from the lead (resume; summary — verbatim text in the session)

Christoph: "yes, resume K with 587 Ω and 2 kΩ". Stage 5: series R in front of CMB's gate (IHP's secondary stage: rppd
587 Ω + dantenna to sub + dpantenna to iovdd at the gate node), v5 = 587 Ω, v6 = 2 kΩ, CMB orientation unchanged; deck
limit raised by two (11 = loop as deck 7 / 9, 12 = step as deck 8); same log checks; append stage 5 to the report and
correct the "cannot be inserted without breaking the Miller path" statement.

## 18:07, K's stage 5 reply (summary)

IHP's secondary stage in front of CMB's gate (PDK rppd 1 × 2 µm = 587.0 Ω and 1 × 7.435 µm = 1991.6 Ω, plus dantenna and
dpantenna): PM at 100 pF 78.4 / 72.6 / 75.6° (587 Ω) and 78.5 / 72.9 / 76.1° (2 kΩ) against 78.4 / 72.6 / 75.4° now; 300 pF
worst case 39.8 / 40.1° against 39.7°; steps 0.3 % / 2 % slower, no overshoot; R·C 0.27–2.4 ns, pole ≥ 67 MHz. The earlier
"breaks the Miller path" statement corrected in the report.

## about 18:10, the lead's check

Logs of decks 11 and 12 grepped: no `Transient op started`, `Timestep too small` or failure; added devices named XK….

## about 18:25, from the lead (resume; summary — verbatim text in the session)

Christoph's symmetry remark verbatim and "yes, resume K with (1)". Stage 6: variants v0, v5 / v6 (CMB-only stage), v7 / v8
(the same rppd also in series with CMA's pad-side plate; optional dummy diodes at CMA), sweep of the pad over 0.94–2.31 V
(≈ 9 points) at 100 pF and 300 pF unloaded, pole–zero map (`.pz` or fitted), fc / PM / GM per point, symmetry of sourcing
and sinking; up to 3 more decks; plots `pz_vs_pad.png`, `pm_fc_gm_vs_pad.png`.

## 18:40, K's stage 6 reply (summary)

Deck 13 (`loop13_sweep.spice`), 108 runs: 9 pad points 0.94–2.29 V × 2 loads × 6 variants. `.pz` does not converge; poles /
zeros by vector fitting of T(jω) (≤ 0.06 dB at 103 of 108 points). The asymmetry is the driver's: on the sourcing half
(pad ≥ 2.17 V) an LHP zero falls to 7–9 MHz and the RHP zero from ≈ 250 to 56 MHz, GM 16.8 dB and PM 39.7° (300 pF) at
2.29 V; the sinking half stays flat. Series R (CMB only or symmetric) moves PM / GM by ≤ 0.6; best worst case symmetric 2 kΩ
73.2° / 40.2°; dummy diodes at CMA irrelevant (≤ 0.1°).

## 18:41, the lead's check

108 deck-13 logs: no `Transient op started`, no `Timestep too small`; added devices XK….

## about 13:45, from the lead (resume; summary — verbatim text in the session)

Christoph's two decisions (symmetric 2 kΩ stages; polarity for maximal capacitance). Stage 7, deck 14: C along the swing
for CMA turned and the total; loop (fc, PM, GM) for v9 = both turned + symmetric 2 kΩ against v0 and v8 at the 9 pad points,
100 pF and 300 pF unloaded; one step for v9; plot `pm_fc_gm_v9.png`.

## 2026-11-03, K's stage 7 reply (summary)

v9 (both turned, symmetric 2 kΩ): each cap +26 % at mid-rail but 25 % lower than today beyond ≈ 0.4 V on one side; both
together +26 % at mid-rail, −1 … −4 % elsewhere, +7 % average. 100 pF: worst PM 74.5° (v0 72.6, v8 73.2), worst GM 16.5 dB
(16.8). 300 pF unloaded: worst PM 39.3° at pad 2.29 V (v0 39.7, v8 40.2), dip 42.3° at 1.12 V, 50.1° at mid-rail. Step at
100 pF: no overshoot, mid-rail settling 0.44 vs 0.33 µs. Lead's check: no transient op / timestep failure in the v9 logs.

## about 14:10, from the lead (resume; summary — verbatim text in the session)

Christoph's worry about the output swing; stage 8 (decks 15–17): large steps to both swing ends and end to end at 100 pF /
300 pF, rail drive and recovery, THD at full swing, for v0 / v8 / v9; plots `steps_large.png`, `rail_recovery.png`.

## 2026-11-03, K's stage 8 reply (summary)

Decks 15–17, 18 runs: v8 = v0 in large steps (< 3 %), rail recovery and THD (−43.4 / −42.7 / −31.6 dB at 10 k / 100 k /
1 MHz); v9 worse: THD −38.2 dB at 100 kHz and −26.2 dB at 1 MHz, steps toward mid-rail 35–40 % slower at 100 pF. All recover
from the top rail within 0.8 µs; the stage-3 "second stable state" reread as a DC-op artefact. 300 pF unloaded rings in all
variants (PM ≈ 40°). Recommendation: v8 (present polarity + symmetric 2 kΩ stages): the two present-polarity caps
complement each other (total ±3 % over the swing), turned ±16 %.
