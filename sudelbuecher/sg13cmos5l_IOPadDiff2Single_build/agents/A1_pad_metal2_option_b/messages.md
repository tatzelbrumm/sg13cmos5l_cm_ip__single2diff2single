# A1 — Pad Metal2 rework (option B): everything the agent was told, verbatim

A subagent starts with no part of the conversation: it sees only the launch prompt, the brief file(s) it is
pointed to, the files in its own `inputs/` folder, and the later messages below. Times Europe/Berlin.
Messages of 02:51–04:00 come from the claude.ai record of the chat (the transcript lost them at the 04:02
compaction), timed by the user message they answered.

## 2026-10-28 00:50 — launch prompt

```text
You are drafting the Metal2 rework of an IHP SG13CMOS5L analog IO pad cell layout with KLayout's Python module. Your complete brief, with hard rules, inputs, geometry, decisions and the checks you must run, is in

/tmp/claude-0/-home-claude/f5dc1779-0ee8-504e-923f-171069e08948/scratchpad/m2agent/BRIEF.md

Read it first, in full, and follow it exactly. Summary of the hard rules (the brief has the details): work only inside /tmp/claude-0/-home-claude/f5dc1779-0ee8-504e-923f-171069e08948/scratchpad/m2agent/ (inputs/ read-only, work/ for scratch, out/ for deliverables); never use any mcp__remote-devices__ tool or write to the user's computer; never run any git command, not even read-only; do not modify the PCell code or the PCell instances; take every design-rule value from the IHP rule deck files named in the brief and cite them; measure, don't guess, and mark reasoning as reasoning.

The job: on the given pad cell (clamps and diodes are live PCells, drains currently unconnected), draw IHP's Metal2 comb scheme at two pitches (option B: pad lines on drain columns, supply straps on source columns, Via2 into the existing Metal3 rails, Metal2 pad junction in the gap with iovss crossing in the uncut Metal3 iovss rail, wide Metal2 over the diode side bars), route the replica nets dabp / dabn and the gate buses a / b (fed from the frame ends) to pins at the top, narrow the n+ band above DCNDiode to its own guard ring, place both Miller capacitors CMA / CMB in the gap, review the hand wiring, list design-note inconsistencies, and verify everything (flat extraction with expected nets and devices, rule checks from the deck, rails unchanged, PCells still live).

Deliver in out/: the candidate GDS, build_m2.py, check_m2.py, report.md, m2_full.png, m2_gap.png. When finished, reply with: the candidate's sha256, the check summary with counts, the drawn CMA / CMB W / L, the dabn track and why, and the open points. If you hit something the brief does not settle and that would change the design (not just a detail), stop there and report it instead of guessing.
```
