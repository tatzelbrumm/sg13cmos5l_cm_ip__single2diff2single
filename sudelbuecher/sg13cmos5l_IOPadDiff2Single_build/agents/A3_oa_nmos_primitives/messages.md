# A3 — oa NMOS primitives compact: everything the agent was told, verbatim

A subagent starts with no part of the conversation: it sees only the launch prompt, the brief file(s) it is
pointed to, the files in its own `inputs/` folder, and the later messages below. Times Europe/Berlin.
Messages of 02:51–04:00 come from the claude.ai record of the chat (the transcript lost them at the 04:02
compaction), timed by the user message they answered. Messages from 05:20 on come from the agent's own transcript, timed when it received them.

## 2026-10-28 02:39 — launch prompt

```text
You are the NMOS layout-primitive specialist for an analog IC block in IHP sg13cmos5l. Your complete brief is /tmp/claude-0/-home-claude/f5dc1779-0ee8-504e-923f-171069e08948/scratchpad/primN/BRIEF.md — read it first and follow it exactly, including its hard rules (cloud workspace only, no remote-devices tools, no git, inputs read-only, rule values only from the PDK decks with citations). Study how the earlier workers rotated sinks_6x6, d2s_casc_n, bg_nab and bias_tree_n (log entries named in the brief, cells in inputs/pad_buffer_cells.gds) before you draw. Deliverables go to /tmp/claude-0/-home-claude/f5dc1779-0ee8-504e-923f-171069e08948/scratchpad/primN/out/. When done, reply with the five-line summary, the report text, and the deliverable list with sha256 (first 12 hex). Report only what you checked.
```

## 2026-10-28 02:50 — message (“Add skill export deliverables (A3)”)

```text
Additional deliverable from the user (02:50): read /tmp/claude-0/-home-claude/f5dc1779-0ee8-504e-923f-171069e08948/scratchpad/SKILL_EXPORT.md and deliver out/skill/ as described there (pattern notation in symbol/score form, pictures rendered from your GDS, a reusable generator, rules with deck citations, a SKILL.md draft), alongside your cells. The cells come first; the skill material documents how you made them, so build it from what you actually did.
```

## 2026-10-28 02:58 — message (“User notice: no separate same-rail NWells”)

```text
Notice from the user (02:58, verbatim): "separate nwells connected to the same voltage rail are EXTREMELY wasteful. Avoid." For your NMOS cells this matters where you would draw n+ guard rings in NWell (iovdd / vdd-tied isolation rings) or any NWell at all: don't give each array its own NWell ring; if an n-well ring is needed at all (say why, with the deck rule), it is one shared structure for the whole NMOS group, drawn so the assembler can merge it with the PMOS group's vdd well. Prefer plain p+ substrate ties at the array periphery. Add this rule, with the spacing numbers it saves, to your rules.md and the skill material.
```

## 2026-10-28 03:01 — message (“User notice: tap rings optional, non-rectangular”)

```text
Notice from the user (03:01, verbatim): "contiguous tap ring is optional. tap ring doesn't have to be rectangular, in particular if that leaves empty space in a guard ring." So: p+ substrate tap segments only where the LU rules need them, at the array periphery, no closed rectangular ring; where a tap strip is needed it follows the cell outline (any rectilinear shape) instead of enclosing empty area. Put the LU numbers per tap segment in your report, and the rule into rules.md / the skill material.
```

## 2026-10-28 03:04 — message (“User notice: polygonal wells; process-agnostic skills”)

```text
Notice from the user (03:04, verbatim): "nwell doesn't have to be rectangular if polygonal shapes are allowed by the design rules. make sure that transferrable layout skills are process agnostic, in the sense that process specific design rules are very important, but the skills themselves must be adaptable to a different set of design, parasitic extraction, device model, and LvS rules." I appended "Addendum 2" to /tmp/claude-0/-home-claude/f5dc1779-0ee8-504e-923f-171069e08948/scratchpad/SKILL_EXPORT.md: read it. In short: any well / tap outline you draw is a polygon following the devices (within the deck's angle / grid rules, cited); your generator takes every rule value, layer and device cell from a process adapter (one file for sg13cmos5l, each value with its source), and the skill draft gets a "porting to another process" section.
```

## 2026-10-28 03:14 — message (“User notice: separate IHP vs generic skills”)

```text
Notice from the user (03:14, verbatim): "record both skills specific for IHP, and process agnostic skills, and clearly distinguish between them." Read "Addendum 3" at the end of /tmp/claude-0/-home-claude/f5dc1779-0ee8-504e-923f-171069e08948/scratchpad/SKILL_EXPORT.md: out/skill/ splits into generic/ (process-agnostic SKILL_draft, patterns, adapter-driven generators, porting section; no IHP names or values) and ihp_sg13cmos5l/ (IHP SKILL_draft: the adapter plus IHP know-how, quirks, deck gaps, pitfalls and workarounds); every rule / lesson tagged [generic] or [IHP].
```

## 2026-10-28 04:29 — message (“A3: bandgap NMOS primitives next”)

```text
New task: the bandgap's NMOS primitives. Read /tmp/claude-0/-home-claude/f5dc1779-0ee8-504e-923f-171069e08948/scratchpad/primN/BRIEF_bg.md; the new inputs are in primN/inputs_bg/ (read-only).

Your oa_n10 / oa_mcs_c went into the compact oa_core_pd that A2 assembled: 2355 µm² against 3856 for v1. The user called it "spectacularly compact" and your primitives "very well done".

Same pattern now for bg_core_pd: NA / NB (20/4 each, matched) plus MS2, MS3 and SKS go into one rotated NMOS block like oa_n10, with one periphery p+ tie and narrow end dummies. A4 does the PMOS cells, A2 the pnp / resistor arrays and the assembly.

Deliverables go in out_bg/, and your out/skill/ gets extended with the new lessons.
```

## 2026-10-28 04:33 — message (“Relay A2's floorplan requests to A3”)

```text
A2's pin and aspect requests for your bandgap NMOS block. The full text is in /tmp/claude-0/-home-claude/f5dc1779-0ee8-504e-923f-171069e08948/scratchpad/oaagent/out_bg/requests_for_A3_A4.md (read only). Short version:
- bg_n4 about 15–22 µm wide, height as needed.
- g, vpc and ks on the TOP edge, towards the PMOS group; mind NW.d1 / NW.f1 there.
- en_3v3_b on the top or right edge.
- ea / eb next to each other on the BOTTOM edge, towards bg_res_c / bg_pnp_c, symmetric about the cell's centre line.
- p+ tie at the bottom, plus one at the top if LU needs it.
- Dummy gates as in oa_n10; say which net.
- Metal1 / Metal2 only, pins as <metal>.pin + <metal>.text, pin coordinates in the report.
- The block floorplan is vdd on top, PMOS row, then the NMOS / bg_res_c / bg_pnp_c row, vss at the bottom, ports on the right, 40–50 µm wide.
```

## 2026-10-28 05:20 — message (“Rate limit reset: continue”)

```text
The rate limit has reset (05:20), so please continue from where you stopped: the bandgap NMOS block per primN/BRIEF_bg.md, with A2's pin / aspect requests from scratchpad/oaagent/out_bg/requests_for_A3_A4.md (bg_n4 15–22 µm wide; g / vpc / ks on top; ea / eb next to each other on the bottom, symmetric; p+ tie at the bottom). Deliverables go in out_bg/.
```

## 2026-10-28 05:43 — message (“Change to bg_n4: option 1”)

```text
Change to bg_n4, chosen by the user (05:43, "Try Option 1."): re-strap all bg_n4 dummies (the 8 × 2/4 in the NA / NB rows and the 2/1 next to MS2) so that D and S go to g instead of vss. The gate stays g, as now through the continuous poly, and the bulk stays vss.

Why (A2's analysis): with Vgs = 0 there is no inversion layer, so the roughly 66 µm² of inverted gate capacitance on g goes away. Only overlap and junction capacitance of the dummy islands remain.

Constraints:
- Same outline (18.12 × 22.80 µm) and the same pins and pin positions as delivered. A2 is building the floorplan on them.
- Keep the poly continuous; the dummy is still the matched devices' edge environment.
- If the g straps don't fit without growing the cell, stop and report what it would cost instead of growing it.

Deliver as bg_n4 in out_bg/bg_n_cells.gds (keep the first version as out_bg/bg_n_cells_v1.gds) and update the CDL so the dummies read D = S = G = g, B = vss. Re-run DRC / LVS and the render, and add a short "option 1" section to your report plus a rule to the skill (generic: dummy at Vgs = 0 by strapping D / S to the gate net when the poly must stay continuous; IHP: what it cost here). Reply with a three-line summary and the changed files with sha256.
```
