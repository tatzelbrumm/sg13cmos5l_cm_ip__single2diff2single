<!--
SPDX-FileCopyrightText: 2026 Christoph Maier
SPDX-License-Identifier: Apache-2.0
-->
# Layout of pad_ref_rb: common brief for the row specialists P and N (cloud session C4, 2026-11-07)

You are a layout specialist for the replica bias cell `pad_ref_rb` of the custom pads (Chipalooza 2026, PDK
ihp-sg13cmos5l). Two specialists work in parallel: **P** (PMOS rows) and **N** (NMOS rows and capacitors). An assembly
agent **F** places and routes your cells afterwards; Christoph Maier reviews. This brief plus `BRIEF_P.md` /
`BRIEF_N.md` (in this folder) are your instructions.

## The one principle

Christoph, 2026-11-07: **"the replica bias must match their layout structures."** pad_ref_rb copies devices of the two
pads (`sg13cmos5l_IOPadSingle2Diff` = S2D, `sg13cmos5l_IOPadDiff2Single` = D2S) so that its voltages track theirs.
Each replica device must therefore look like the pad device it copies: the same PCell finger, orientation, row
neighbors, dummies, well and tie arrangement, gate bar and contact pattern. Where the pad has a row, build yours **with
the code that built the pad's row** (session C3's `build_s2d_p3.py` / `build_s2d_n3.py`), changing only the device
list and nets, not the geometry rules. The drawn S2D pad cell is the binding reference; the D2S pad is the reference
for devices both pads share (unit tails, input tubs).

## Sources of truth (read; do not edit)

Repo `R = /home/user/sg13cmos5l_cm_ip__single2diff2single` (branch `claude/c4-replica-bias`), notes worktree
`S = /home/user/sg13cmos5l_cm_ip__single2diff2single_sudelbuecher/sudelbuecher`.

- **Netlists** (the circuit; every device, net and size): `R/macros/pad_ref_rb/netlist/source/pad_ref_rb.spice`
  (`bias_tree_rb`, `bypass_rb` with parameters `ncm`, `ncr`, `pad_ref_rb`), `R/macros/vcm_rb/netlist/source/vcm_rb.spice`,
  `R/macros/vref_s2d_rb/netlist/source/vref_s2d_rb.spice`. Sheets and renders next to them (`schematic/`).
- **Layout plan and primitives:** `R/macros/pad_ref_rb/layout/primitives/` (`README.md`: which pad row each replica
  copies, the row plan, area estimate; `mapping.tsv`: device → pad structure; `pad_ref_rb_primitives.gds`: unchanged
  `rbsrc_*` copies of the S2D pad's rows and devices, XOR-identical).
- **The pad layouts (references, read only):** `R/macros/sg13cmos5l_IOPadSingle2Diff/layout/klayout/sg13cmos5l_IOPadSingle2Diff.klay.gds`,
  `R/macros/sg13cmos5l_IOPadDiff2Single/layout/klayout/sg13cmos5l_IOPadDiff2Single.klay.gds`; S2D layout report
  `S/design_considerations/pad_buffer_layout/pad_cell_s2d/report.md`.
- **The agents that built the S2D pad's rows (session C3):** `S/sg13cmos5l_IOPadSingle2Diff_build/agents_c3/P/` and `.../N/`
  (`BRIEF.md` with Christoph's binding rules, `report.md`, `out/build_s2d_p3.py` / `out/build_s2d_n3.py`, cells, CDLs, logs),
  and `.../F/` (assembly; `out/src/`). Their predecessors for the D2S pad: `S/sg13cmos5l_IOPadDiff2Single_build/agents_c2/`.
- **Earlier layout knowledge:** `S/design_considerations/pad_buffer_layout/layout_primitives.md`,
  `S/design_considerations/pad_buffer_layout/klayout/` (`pad_buffer_cells.py`, `README.md`),
  `S/design_considerations/pad_buffer_layout/oa_core_pd_v2_2026-10-28/skill/` (layout skill: generic + ihp_sg13cmos5l).
- **Check helpers:** `S/sg13cmos5l_IOPadSingle2Diff_build/agents_c3/F/work/B4/inputs/sym_check.py`, `.../SG13CMOS5L_os_layout_rules.txt`.

## Christoph's layout rules (binding; read the full text in the C3 P / N briefs)

1. Symmetry: rows mirror-symmetric about the line dividing them; the same dummy at both ends of every row; "dummies on
   only one (mismatching) side of each row" is unacceptable.
2. Gate contacts on full-width poly, no necked poly; contact gates with poly; where dummies extend abutted gate poly,
   the gate is contacted by abutment.
3. Dummies: source and drain to the rail, gate net by abutment. PMOS rail vdd, NMOS rail vss.
4. Unmodified PDK PCell transistors; do not shorten contacts or break up an array.
5. No well taps between rows of arrayed transistors (periphery only, LU.a 20 µm); one NWell per rail, no notches;
   taps as rings where space allows; a pair of switches shares its well and tap. Exception: a device with bulk =
   source (the input tubs, the averaging diodes) keeps its own NWell, identical in every copy.
6. Metal stubs no longer than needed; M1 inside a primitive, M2 only where the cell needs it; American English.
7. No floorplan constraints from F: draw each cell compact and symmetric, pins on its edges where they serve its nets.

## Netlist consequences you must report

- **Dummies:** every dummy you draw becomes a netlist device (`XMD<name>`, D = S = B on the rail, gate as drawn) when the
  lead backannotates. List each with its cell, size, terminals.
- **Any change of W, L, ng, finger split or device order** needs a reason and goes in the report.
- **LVS strategy (lead's default, Christoph may revise):** each of your cells must be LVS-clean against its own CDL
  (which you write, from the netlists, plus its dummies). The assembled pad_ref_rb will be compared flat, because your
  rows mix devices of bias_tree_rb, vcm_rb and vref_s2d_rb.

## Checks (each cell)

- DRC: `python3 /foss/pdks/ihp-sg13cmos5l/libs.tech/klayout/tech/drc/run_drc.py --path=<gds> --topcell=<cell> --no_density --mp=4 --run_dir=<dir>`
  (grep the log for "exception"); 0 violations.
- LVS: `python3 /foss/pdks/ihp-sg13cmos5l/libs.tech/klayout/tech/lvs/run_lvs.py --layout=<gds> --netlist=<cdl> --topcell=<cell> --run_dir=<dir> --disable_tap_extraction`.
- Symmetry: `python3 <sym_check.py> <gds> <cell>`.
- A comparison against the pad: for each copied row, a measured statement of what is identical to the pad's row
  (XOR of the shared part, or same generator call) and what differs.
Run each check once and again after each fix; three rounds at most per cell, then report it and leave it.

## Environment and hard rules

- `export PDK_ROOT=/foss/pdks; source /home/user/sg13cmos5l_cm_ip__single2diff2single/.designinit` before any tool.
- Write only in your workspace (`P/` or `N/` next to this file: `work/`, `out/`). Do not edit the repo or the notes
  worktree. No git, no web, no `mcp__*` tools.
- Rule values only from the PDK decks and documents; cite file and rule. Say what is measured and what is reasoning.
- Keep code small. Background commands under 2 h; kill processes by PID, never `pkill -f`.

## Deliverables (in `out/`), then stop

- `<prefix>_cells.gds` (all your cells, one top cell showing them), `<prefix>_cells.cdl`, the build script(s), PNG per
  cell, DRC / LVS / sym_check logs.
- `report.md` (≤ 80 lines): per cell size, area against the pad's counterpart, what is identical to the pad and what
  differs (with reasons), the dummies (for backannotation), open questions for Christoph.
- Reply with a summary of no more than 15 lines and the `out/` file list.

## Binding rules, verbatim from the briefs of the pads' layout agents (added 2026-11-07 after Christoph:
"look at the brief to the previous layout agents before you hallucinate garbage in garbage out")

These come before anything in this brief or in BRIEF_P / BRIEF_N / BRIEF_P3 that contradicts them. Where those
briefs paraphrase a rule, this text wins.

### From C3 N's brief (`agents_c3/N/BRIEF.md`, "Christoph's rules")


1. **Symmetry.** "Best: symmetric rows along the line dividing the rows, symmetric dummies. Worse: symmetric rows
   along the line dividing the rows, no dummies. ABSOLUTELY, UNACCEPTABLY WORST: dummies on only one (mismatching)
   side of each row. Applies also to sinks_6x6." (C2, 2026-10-31 18:55)
   - A two-row array is mirror-symmetric about the line dividing the rows.
   - Within each row, the device layers are mirror-symmetric about the row's center line: the dummies at both ends of
     every row are the same device.
   - A bias diode in an end position (BN in the sinks, BNC in casc_n) needs its twin at the other end, or goes to the
     middle.
2. **Gate contacts on full-width poly**, no narrowed poly necks (see `inputs/log.md` 00:57, 01:03–01:30, 02:41,
   17:43). Where dummies extend abutted gate poly, the gate is contacted by abutment: keep it.
3. **Dummies** (C3, Christoph 2026-11-03 18:34, verbatim): "Dummy source and drain to the rails, gate net by abutment
   where dummies extend abutted gate poly." For the NMOS cells, the rail is vss (= iovss in the pad).
   - N2 had tied NMOS dummies D = S = G to the gate net. That changes now: S / D go to vss.
4. **Unmodified device cells.** Use the PDK PCell transistors and resistors. Don't shorten drain or source contacts,
   and don't break up a transistor array.
5. **Christoph's rules of 2026-10-28:**
   - no substrate taps between rows of arrayed transistors: taps only at the periphery (LU.b 20 µm, layout rules §7.2.2);
   - a tap ring is optional and needn't be rectangular;
   - narrow dummies, but rule 1 comes first.
6. **Christoph's review of C2's primitives, applied from the start** (`inputs/C2_N2/out/d2s_n2_cells_human_review.txt`,
   `inputs/C2_P2/out/d2s_p2_cells_human_review.txt`, `inputs/C2_decisions.md` 2026-11-03 14:25 and 15:50):
   - the substrate tap becomes a ring around the array where space allows;
   - sinks: "why the metal1 poly contacts in the center?" and "get rid of the center contacts";
   - pd_n was "VERY BAD as layout primitive: substrate tap too long, b, vabn metal1 stubs too long, vsso shouldn't be
     metal2 for the primitive"; and "why not contact the gates with poly?";
   - switches belong with the cell they serve, not in a separate corner with their own taps;
   - American English in every file.
7. **The circuit sets the maps and ratios.** Use the common-centroid maps of `inputs/layout_primitives.md` §5:
   - sinks `X Y Y X X Y / Y X X Y Y X`, with BN, made symmetric under rule 1;
   - the R block as a mirror-symmetric sequence of the six resistors.

   Take W / L / finger counts from the circuit. A change needs a reason in the report. The fold sinks dominate the
   offset (5.4 of 6.1 mV, §1). Keep their source bus with BN tapped to vss at one point (§6).
8. **No floorplan constraints** (Christoph, C2 17:55). Draw each cell compact and symmetric, with its pins on its edges
   where they serve the cell's nets.
9. **Compact.** Christoph asked for compacted primitives. The library cells (`inputs/pad_buffer_klayout/`) are the
   uncompacted reference: report each cell's area against its library counterpart. On d2s, C2's N2 measured 0.88
   (sinks), 1.17 (casc_n) and 0.92 (rhigh) of the library. Do at least as well wherever rules 1–7 allow.

### From C3 P's brief (`agents_c3/P/BRIEF.md`, "Christoph's rules"; the PMOS-specific parts)


1. **Symmetry.** "Best: symmetric rows along the line dividing the rows, symmetric dummies. Worse: symmetric rows
   along the line dividing the rows, no dummies. ABSOLUTELY, UNACCEPTABLY WORST: dummies on only one (mismatching)
   side of each row." (C2, 2026-10-31 18:55)
   - A two-row array is mirror-symmetric about the line dividing the rows.
   - Within each row, the device layers are mirror-symmetric about the row's center line: the dummies at both ends
     of every row are the same device.
   - A bias diode at an end position (BP in the tails) needs its twin at the other end, or it goes to the middle.
2. **Gate contacts on full-width poly**, no narrowed poly necks (see `inputs/log.md` 00:57, 01:03–01:30, 02:41, 17:43).
   Where dummies extend abutted gate poly, the gate is contacted by abutment: keep it.
3. **Dummies (C3, Christoph 2026-11-03 18:34, verbatim):** "Dummy source and drain to the rails, gate net by abutment
   where dummies extend abutted gate poly." For the PMOS cells the rail is vdd (= iovdd in the pad).
4. **Unmodified device cells.** Use the PDK PCell transistors. Do not shorten drain or source contacts, and do not
   break up a transistor array.
5. **Christoph's rules of 2026-10-28:**
   - no well taps between rows of arrayed transistors, only at the periphery (LU.a 20 µm);
   - one NWell per rail and no well notches;
   - NWell polygonal where the rules allow;
   - narrow dummies, but rule 1 first.

   Exception: each input device has bulk = source and keeps its own NWell, identical in every copy
   (`layout_primitives.md` §3 P1).
6. **Christoph's review of C2's primitives, to apply from the start** (`inputs/C2_P2/out/d2s_p2_cells_human_review.txt`,
   `inputs/C2_N2/out/d2s_n2_cells_human_review.txt`, `inputs/C2_decisions.md` 2026-11-03 14:25 and 15:50):
   - taps as rings where space allows;
   - a "separate well tap" for a pair of switches "looks like bullshit": share the well and its tap;
   - devices on a notch in the NWell: extend the well or move the devices instead;
   - metal stubs no longer than needed, and no M2 inside a primitive unless the cell needs it;
   - contact gates with poly;
   - get rid of center contacts on gate bars where the gate is contacted at its ends;
   - American English in every file.
7. **The circuit sets the maps and ratios.**
   - Common-centroid maps of `inputs/layout_primitives.md` §5: for s2d, the signal units A1 A2 F1 F2 in the tub /
     tail map `Aa C2b C1b Ba / Bb C1a C2a Ab` (A → A1, B → A2, C1 → F1, C2 → F2), and the CMFB units M1 M2 as a
     cross-quad `M1a M2b / M1b M2a`. Each tail sits under its tub's column.
   - Loads `P N D D N P P N D D N P` (library).
   - W / L / finger counts come from the circuit. A change needs a reason in the report.
8. **No floorplan constraints** (Christoph, C2 17:55: "DO NOT FORCE FLOORPLAN CONSTRAINTS ON THE LAYOUT PRIMITIVE
   AGENTS"). Draw each cell compact and symmetric, with its pins on its edges where they serve the cell's nets.
9. **Compact.** Christoph asked for compacted primitives. The library cells (`inputs/pad_buffer_klayout/`) are the
   uncompacted reference. Report each cell's area against its library counterpart. C2's P2 measured 1.08 (inputs),
   0.67 (tails), 0.79 (loads) and 0.98 (casc_p) of the library on d2s; do at least as well wherever rules 1–7 allow.

### Christoph's reviews of the C2 primitives (verbatim)

```
d2s_inputs_c2 : looks workable
bias_tree_p_c2 : looks workable if TGP is moved by F as pad layout requires
d2s_ab_p_c2 : looks workable if F revises well tap
d2s_casc_p_c2 : looks good as basis for F
d2s_p2_cells_c2 : looks good as basis for F
d2s_pd_p_c2 : looks workable for adaptation by F into pad layout context
d2s_tails_c2 : looks good as basis for F


d2s_rhigh_c2 : in the completed layout, the substrate tap should become a ring, if space allows
sinks_6x6_c2 : why the metal1 poly contacts in the center? in the completed layout, the substrate tap should enclose the whole array, if space allows
d2s_pd_n_c2 : VERY BAD as layout primitive: substrate tap too long, b, vabn metal1 stubs too long, vsso shouldn't be metal2 for the primitive. passable if F completely overworks this primitive.
d2s_casc_n_c2 : looks decent, in context substrate tap should become a ring if space allows.
d2s_ab_n_c2 : may already be integrated in F layout, F should overwork this primitive.
d2s_n2_cells_c2 : TGN and TDN should be moved by F when assembling the entire circuit.

```

### Applied to pad_ref_rb (lead)

- A device whose bulk is its own source gets its own NWell only per distinct bulk net: devices with the same bulk
  net share a well and abut by gate poly where their gates are the same net (the pad tub: two fingers, one well).
- Dummies extend the abutted gate poly of their row (gate = the row's gate net by abutment), source and drain on
  the rail of that well / substrate (for a well at a bulk net other than vdd, that net is the rail).
- Report each cell's area against its pad counterpart (or library cell), as the C3 agents did; compactness counts.
- The lead checks every CDL against the circuit netlists (every non-dummy device, nets and sizes) before accepting
  an LVS match: an LVS match against a wrong CDL proves nothing.
