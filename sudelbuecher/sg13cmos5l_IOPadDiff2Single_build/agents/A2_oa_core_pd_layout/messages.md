# A2 — oa_core_pd layout from primitives: everything the agent was told, verbatim

A subagent starts with no part of the conversation: it sees only the launch prompt, the brief file(s) it is
pointed to, the files in its own `inputs/` folder, and the later messages below. Times Europe/Berlin.

## 2026-10-28 01:34 — launch prompt

```text
You are building a KLayout layout for an analog IC block. Your complete brief is in /tmp/claude-0/-home-claude/f5dc1779-0ee8-504e-923f-171069e08948/scratchpad/oaagent/BRIEF.md — read it first and follow it exactly, including its hard rules (cloud workspace only, no remote-devices tools, no git, inputs read-only, primitives unchanged, rule values only from the PDK decks with citations). Deliverables go to /tmp/claude-0/-home-claude/f5dc1779-0ee8-504e-923f-171069e08948/scratchpad/oaagent/out/. When done, reply with the brief's five-line summary and the deliverable list with sha256 (first 12 hex). Report only what you checked.
```

## 2026-10-28 01:46 — message (“Retarget oa_core_pd layout to slot7, compact”)

```text
Change of envelope for oa_core_pd: it goes into slot 7, not into the pad cell. The user wants a compact layout for the core side of the slot macro (macros/slot: slot.klay.gds, 537.15 x 273 um, the slot7_wrapper of the chipalooza harness), so the 80 um pad pitch and the fit_bias_tree_oa_bg zone are NOT the constraint. Aim for minimum area with a sensible aspect ratio (roughly square to 2:1), all six primitives unchanged, wiring on Metal1 / Metal2 where possible so Metal3 and above stay free for slot-level routing (report every layer you use), vdd / vss as rails along one or two block edges, and the five ports (vdd vss iout en_3v3 en_3v3_b) as pins on the block edge. Everything else in BRIEF.md stands. Afterwards there will be a second part (bg_core_pd, BRIEF_bg.md); don't start it until told.
```

## 2026-10-28 02:24 — message (“Start part 2: bg_core_pd layout”)

```text
Part 2, start now: the bg_core_pd layout. The brief is /tmp/claude-0/-home-claude/f5dc1779-0ee8-504e-923f-171069e08948/scratchpad/oaagent/BRIEF_bg.md (inputs in ../inputs_bg/, deliverables in ../out_bg/). Same hard rules as before, same slot-7 envelope rules as your oa_core_pd (minimum area, aspect 1:1 to 2:1, Metal1 / Metal2 only, ports on the block edge). Reuse your oa_core_pd build / DRC / LVS / verify scripts and keep the same conventions so the two blocks can abut: same rail layers and widths, vdd on top and vss at the bottom, and the same pin layers. Also, while you are at it, look at whether the bg block's height can match oa_core_pd's 50.74 µm so the two sit side by side on shared rails; if that costs a lot of area, say so and don't force it. Put the report text in your final reply again (the harness blocks .md files for you). Do not change anything in out/ (oa_core_pd).
```

## 2026-10-28 02:37 — message (“Stop bg; redo oa_core_pd compact, primitives may change”)

```text
Change of plan from the user (02:36): STOP the bg_core_pd work now (leave whatever you have in out_bg/ as it is, don't continue it). Redo oa_core_pd, and this time the primitives may and must change. The user's words: "oa_nmir, oa_mcs, oa_misc_n, oa_misc_p, need to be changed. in particular transistors in oa_nmir, oa_misc_n, oa_mcs rotated, transistors of same size in oa_nmir and oa_misc_n combined into one array, NEVER use substrate tap between rows of arrayed transistor, and completely revise the guard ring structures. They're too bulky as they are. There is WAY too much empty space in the oa_core_pd layout. Compactify. Use narrower dummy transistors in oa_pmir. Let the layout drive the design. backannotate if necessary. Hold off on the bandgap layout until there are lessons learned from compactifying oa_core_pd."

What that means for you (this replaces the "primitives unchanged" rule of BRIEF.md and the 08:45 oa_misc_p decision; all other hard rules stand: cloud only, no device tools, no git, inputs read-only, rule values from the decks with citations):
1. Rotate the transistors in oa_nmir, oa_misc_n and oa_mcs (the way oa_pmir / oa_pcas were rotated on 2026-10-27; read the log entries 04:01-04:14 and the generator / Q&A conventions for "rotated").
2. All transistors of the same size in oa_nmir and oa_misc_n go into ONE array: M10 (180/1), M11 (90/1), MC10 (10/1), MS2 (10/1) are all 10/1 fingers; plus whatever dummies the array needs. Keep M10:M11 matched (common-centroid or interdigitated as oa_pmir does) and keep the W ratios that set the OA current (M10:M11 = 2:1 and the PMOS mirror ratios); if the layout makes you change a size or finger count, say why and backannotate (point 6).
3. NEVER put a substrate (or well) tap between rows of an arrayed transistor block. Taps only at the array periphery; check LU (latch-up distance) from the deck with taps at the edge only; if an array is too large for that, report the numbers instead of adding an inner tap.
4. Completely revise the guard rings: they are too bulky. Thin rings (one contact row, minimum Activ / metal), shared between neighbouring arrays of the same type where the rules allow, no double rings, no ring where the deck doesn't need one. Note from the log, 2026-10-27 08:45, the user on split cells: "NO. NO ntap rings." (tap-less switch cells, bulk tied by the parent).
5. oa_misc_p changes too (MS1 chain 8 x 0.5/12.5 and SVPG): compact it under the same rules. oa_pmir: use narrower dummies (keep their L = 8 µm; the W is up to you, with the reason); keep the point symmetry of the real devices.
6. Let the layout drive the design: where the compact layout wants a different finger split, dummy size or series split, do it in the layout and backannotate: produce in out/ an updated copy of oa_core_pd.sch (and .sym only if ports change, which they should not) and the updated subckt oa_core_pd text for bias_ref_pd.spice, plus a short list of every device change with its electrical effect (W, L, ratio kept or not). Do not touch the inputs; I review and apply.
7. Compactify: aim for a block much smaller than 76 x 50.74 µm, with the same edge conventions (vdd rail top, vss rail bottom, Metal1 / Metal2 only, ports on the edge). Report utilization (device area / block area) before and after.
8. New cell versions: write the changed primitives under new names in your own GDS (e.g. oa_nmir_c, oa_mcs_c, ...), keep the old ones out of the new top cell, and deliver them so they can replace the library cells later (with a .cdl for each). Don't write to the library file.
9. Same checks as before (your DRC, LVS against the backannotated netlist, XOR of nothing needed now but report what changed), renders, and a report with a section "lessons learned for bg_core_pd". Put the report text in your final reply.
```

## 2026-10-28 02:38 — message (“Narrow scope: assembler only, primitives by specialists”)

```text
Amendment to my last message (the user, 02:37: "other agents may be more experienced rotating transistors within layout primitives."): the changed primitives will be made by two specialist agents, not by you. Agent N: oa_nmir + oa_misc_n merged into one rotated 10/1 array (plus small cells for MS3 / SKS) and oa_mcs rotated; agent P: oa_misc_p compacted and oa_pmir with narrow dummies. Their outputs will land in /tmp/claude-0/-home-claude/f5dc1779-0ee8-504e-923f-171069e08948/scratchpad/primN/out/ and .../primP/out/ (GDS + .cdl per cell). Your part: do NOT draw primitives. Prepare the compact assembly: (a) a placement / routing build script parameterized by the new cells' bounding boxes and pin positions, so you can drop them in when they arrive; oa_pcas stays as it is unless its ring is the bulk you need to remove, then say so; (b) the backannotation framework (sheet copy + subckt text + device-change list) as in point 6 of my last message; (c) a list of lessons learned so far for the floorplan (what made 76 x 50.74 large: empty areas, ring overhead, channel widths), with numbers. Then stop and report; I will resume you with the new primitives' paths. bg_core_pd stays on hold.
```

## 2026-10-28 02:50 — message (“Add skill export for assembly (A2)”)

```text
Additional deliverable from the user (02:50): read /tmp/claude-0/-home-claude/f5dc1779-0ee8-504e-923f-171069e08948/scratchpad/SKILL_EXPORT.md. For you the subject is block assembly, not primitives: floorplanning (how to pick placement / orientation so nets are short and space is not wasted), rail and pin conventions, channel routing on Metal1 / Metal2, symmetric routing of a point-symmetric mirror, and the checking flow (your Python DRC / LVS / verify scripts as reusable tools). Deliver out/skill/ in the three forms described (symbol / score form of the floorplan as a placement grammar, pictures from the GDS incl. a v1-vs-compact comparison once the compact version exists, generator = your build script made reusable), plus rules.md and SKILL_draft.md. Start with what v1 taught you; extend it after the compact assembly.
```
