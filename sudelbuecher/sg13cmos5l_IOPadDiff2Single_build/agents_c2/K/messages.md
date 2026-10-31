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
