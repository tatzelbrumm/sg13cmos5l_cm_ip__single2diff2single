# A4 — oa PMOS primitives compact: everything the agent was told, verbatim

A subagent starts with no part of the conversation: it sees only the launch prompt, the brief file(s) it is
pointed to, the files in its own `inputs/` folder, and the later messages below. Times Europe/Berlin.
Messages of 02:51–04:00 come from the claude.ai record of the chat (the transcript lost them at the 04:02
compaction), timed by the user message they answered. Messages from 05:20 on come from the agent's own transcript, timed when it received them.

## 2026-10-28 02:39 — launch prompt

```text
You are the PMOS layout-primitive specialist for an analog IC block in IHP sg13cmos5l. Your complete brief is /tmp/claude-0/-home-claude/f5dc1779-0ee8-504e-923f-171069e08948/scratchpad/primP/BRIEF.md — read it first and follow it exactly, including its hard rules (cloud workspace only, no remote-devices tools, no git, inputs read-only, rule values only from the PDK decks with citations). Study how the earlier workers rotated oa_pmir, bg_misc_p and the narrow-dummy rows (log entries named in the brief, cells in inputs/pad_buffer_cells.gds) before you draw. Deliverables go to /tmp/claude-0/-home-claude/f5dc1779-0ee8-504e-923f-171069e08948/scratchpad/primP/out/. When done, reply with the five-line summary, the report text, and the deliverable list with sha256 (first 12 hex). Report only what you checked.
```

## 2026-10-28 02:50 — message (“Add skill export deliverables (A4)”)

```text
Additional deliverable from the user (02:50): read /tmp/claude-0/-home-claude/f5dc1779-0ee8-504e-923f-171069e08948/scratchpad/SKILL_EXPORT.md and deliver out/skill/ as described there (pattern notation in symbol/score form, pictures rendered from your GDS, a reusable generator, rules with deck citations, a SKILL.md draft), alongside your cells. The cells come first; the skill material documents how you made them, so build it from what you actually did.
```

## 2026-10-28 02:58 — message (“User notice: merge NWells on the same rail”)

```text
Notice from the user (02:58, verbatim): "separate nwells connected to the same voltage rail are EXTREMELY wasteful. Avoid." For your PMOS cells (oa_pmir successor, oa_misc_p successor): all their bulks are vdd, as are oa_pcas's. Draw each cell's NWell to the cell edge on the sides where it will abut another vdd-well cell, and leave the ntap / ring to the parent where the merged well gets one shared periphery tap; no per-cell ring around a well that will merge with its neighbour. Within a cell, never two separate NWells on vdd. Check LU with the taps the parent will provide (state your assumption: where the taps are), and list the pins / edges where the well must continue. Add this rule, with the NW.b1 / NW spacing numbers it saves, to your rules.md and the skill material.
```

## 2026-10-28 03:01 — message (“User notice: tap rings optional, non-rectangular”)

```text
Notice from the user (03:01, verbatim): "contiguous tap ring is optional. tap ring doesn't have to be rectangular, in particular if that leaves empty space in a guard ring." So: ntap segments only where the LU rules need them (with the parent's taps counted), no closed rectangular rings, and where you do need a tap strip, let it follow the cell outline (any rectilinear shape) instead of enclosing empty area. Put the LU numbers per tap segment in your report, and the rule into rules.md / the skill material.
```

## 2026-10-28 03:04 — message (“User notice: polygonal NWell; process-agnostic skills”)

```text
Notice from the user (03:04, verbatim): "nwell doesn't have to be rectangular if polygonal shapes are allowed by the design rules. make sure that transferrable layout skills are process agnostic, in the sense that process specific design rules are very important, but the skills themselves must be adaptable to a different set of design, parasitic extraction, device model, and LvS rules." I appended "Addendum 2" to /tmp/claude-0/-home-claude/f5dc1779-0ee8-504e-923f-171069e08948/scratchpad/SKILL_EXPORT.md: read it. In short: your NWell and ntap outlines are polygons following the devices (within the deck's angle / grid rules, cited), no bounding rectangles; your generator takes every rule value, layer and device cell from a process adapter (one file for sg13cmos5l, each value with its source), and the skill draft gets a "porting to another process" section.
```

## 2026-10-28 03:14 — message (“User notice: separate IHP vs generic skills”)

```text
Notice from the user (03:14, verbatim): "record both skills specific for IHP, and process agnostic skills, and clearly distinguish between them." Read "Addendum 3" at the end of /tmp/claude-0/-home-claude/f5dc1779-0ee8-504e-923f-171069e08948/scratchpad/SKILL_EXPORT.md: out/skill/ splits into generic/ (process-agnostic SKILL_draft, patterns, adapter-driven generators, porting section; no IHP names or values) and ihp_sg13cmos5l/ (IHP SKILL_draft: the adapter plus IHP know-how, quirks, deck gaps, pitfalls and workarounds); every rule / lesson tagged [generic] or [IHP].
```

## 2026-10-28 04:29 — message (“A4: bandgap PMOS primitives next”)

```text
New task: the bandgap's PMOS primitives. Read /tmp/claude-0/-home-claude/f5dc1779-0ee8-504e-923f-171069e08948/scratchpad/primP/BRIEF_bg.md; the new inputs are in primP/inputs_bg/ (read-only).

Your oa_pmir_c / oa_ms1 / oa_svpg went into the compact oa_core_pd that A2 assembled: 2355 µm² against 3856 for v1. The user called it "spectacularly compact" and your primitives "very well done".

Same pattern now for bg_core_pd:
- bg_pmir_pcas becomes a compact, tap-less, rotated 10/1 array. PB : PA : PO = 4 : 4 : 8 fingers, with the cascodes the same, matched / point-symmetric and XOR-checked, with narrow dummies and the NWell drawn to the edge.
- bg_misc_p becomes an oa_ms1-style MS1 chain (0.5/100) plus SVPG.

A3 does the NMOS cells, A2 the pnp / resistor arrays and the assembly. Deliverables go in out_bg/, and your out/skill/ gets extended with the new lessons.
```

## 2026-10-28 04:33 — message (“Relay A2's floorplan requests to A4”)

```text
A2's pin and aspect requests for your bandgap PMOS cells. The full text is in /tmp/claude-0/-home-claude/f5dc1779-0ee8-504e-923f-171069e08948/scratchpad/oaagent/out_bg/requests_for_A3_A4.md (read only). Short version:
- bg_pmir_pcas_c: 40–50 µm wide (rows of 4 fingers or whatever packs to that width), height free.
- g, vpc and vpg on the BOTTOM edge, towards the NMOS block and bipolar core below; vpg may go on the right edge instead, for svpg. iout on the RIGHT (port) edge. ca / co can stay inside.
- vdd plates on the top edge, under the block's rail.
- NWell = ThickGateOx to every edge, tap-less. State the LU tie segments you need inside your margins, as for oa_pmir_c.
- bg_misc_p: A2 will reuse oa_ms1 / oa_svpg unchanged (same devices and nets) unless you deliver a better shape. In that case ks and en_3v3_b go on the bottom edge, en_3v3 on the right, vdd on top.
- Metal1 / Metal2 only, pins as <metal>.pin + <metal>.text, pin coordinates in the report.
```

## 2026-10-28 05:20 — message (“Rate limit reset: continue”)

```text
The rate limit has reset (05:20), so please continue from where you stopped: the bandgap PMOS cells per primP/BRIEF_bg.md, with A2's pin / aspect requests from scratchpad/oaagent/out_bg/requests_for_A3_A4.md (bg_pmir_pcas_c 40–50 µm wide; g / vpc / vpg on the bottom, iout on the right, vdd plates on top, tap-less with the NWell to every edge; oa_ms1 / oa_svpg reused unless you do better). Deliverables go in out_bg/.
```
