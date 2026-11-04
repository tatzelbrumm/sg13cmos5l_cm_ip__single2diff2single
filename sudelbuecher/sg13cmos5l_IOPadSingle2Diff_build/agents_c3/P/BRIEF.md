<!--
SPDX-FileCopyrightText: 2026 Christoph Maier
SPDX-License-Identifier: Apache-2.0
-->
# Brief P: compact PMOS layout primitives of the IOPadSingle2Diff pad (IHP sg13cmos5l), C3 2026-11-03

Workspace (yours only): `$WS` (the lead gives the absolute path), with `inputs/` read-only, `work/` scratch, `out/`
deliverables. You are the PMOS layout specialist for the **s2d** pad buffer `s2d_mpdda_pd`. Agent N draws the NMOS
cells in parallel. Agent F places and wires all cells afterwards in the pad and may still adapt your cells. After the
lead's check, your cells go to F; Christoph reviews F's placement.

This is the second pad. The first, `sg13cmos5l_IOPadDiff2Single` (C2), went through a rejected first attempt and an
accepted rebuild (P2 / N2, Opus). That rebuild is your starting point: `inputs/C2_P2/out/` (`build_d2s_p2.py`, the
cells, `report.md`) and `inputs/C2_N2/out/`. F2's later fixes of those cells are in
`inputs/C2_F2/report_stageB.md` and `out/cells/`. **Reuse their code and approach; do not start from scratch.**

## Christoph's rules (binding; they come before compactness)

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

## Your cells

Circuit: `inputs/circuit/s2d_mpdda.spice` (subckt `s2d_mpdda`), `s2d_pd.spice` (`s2d_mpdda_pd`), `units.spice`
(`unit_r2`), `bias_tree_noab_pd.spice`, `bias_ref_pd.spice` (`bias_diodes`), and the sheets. In the pad, the cell's
`vdd` is iovdd and `vss` is iovss.

| cell (deliver as `<name>_c3`) | devices |
|---|---|
| `tub_p20x1` + `s2d_inputs` | 12 input devices hv PMOS 2 × 10/1 (w=20u ng=2), bulk = source, each in its own NWell. Units A1 A2 (gp vin, gn vref), F1 (vcm, vfbp), F2 (vfbn, vcm) drain to x / y; M1 (vfbp, vcm), M2 (vfbn, vcm) drain to xc / yc; half a = gp device (drain y / yc), b = gn device (drain x / xc); sources sa_U / sb_U. Dummy tubs at both ends of both rows. Start from C2's `tub_p20x1_c2` / `d2s_inputs_c2` ("looks workable") |
| `s2d_tails` | 12 tails hv PMOS 5/6 on vbp (Ta / Tb of each `unit_r2`: sa_U / sb_U ← vdd), BP (diode vbp, 5/6) with its twin, dummies; one NWell on vdd |
| `s2d_loads` | LP (lp), LN (ln), D (dd): hv PMOS 6/4, 4 fingers each (w=24u ng=4), gate vcmfb, source vdd |
| `s2d_casc_p` | LPC (voutp ← lp), LNC (voutn ← ln), DC (vcmfb ← dd): hv PMOS 15/3, 2 fingers each (w=30u l=3u ng=2), gate vbpc; BPC (diode vbpc, 1/4) |
| `s2d_pd_p` | TPP (voutp – vcm), TNP (voutn – vcm): hv PMOS 1/0.45, gate en_3v3, bulk vdd |
| `bias_tree_noab_p` | PBN (vbn ← vdd, gate vbp, 5/6), PBNC (vbnc ← vdd, gate vbp, 2/6), TGP (iref – ni, gate en_3v3_b, 1/0.45, bulk vdd). This is C2's `bias_tree_p_c2` / F2's `bias_tree_p_f2` without PABN |

Library sources: `inputs/pad_buffer_klayout/` (`pad_buffer_cells.gds` / `.cdl` / `.py`, `cell_tree.md`, `README.md`,
Q&A). Earlier compaction rules: `inputs/A4/` (`skill/generic/rules.md`, `skill/ihp_sg13cmos5l/rules.md`).

## Hard rules

- Work only in your workspace. No git, no web searches, no `mcp__*` tools; do not touch `inputs/`.
- Rule values only from the PDK's decks and documents: `/foss/pdks/ihp-sg13cmos5l/libs.tech/klayout/tech/drc/rule_decks/`
  (`sg13cmos5l_tech_default.json`, the `.drc` files) and `inputs/SG13CMOS5L_os_layout_rules.txt`. Cite file and rule.
- Say which statements are measured facts and which are reasoning. Times: `TZ=Europe/Berlin date`.
- Keep code small: no "just in case" options, no script piled on script.
- Background commands die after 2 h. Kill processes by PID, never with `pkill -f`.

## Checks

Run each check once, and once more after each fix. A cell that is not clean after three rounds is reported and left.

- `python3 inputs/sym_check.py <gds> <cell> [--x ..] [--y ..] [--no-y]`. Target 0; explain every residual, with its
  location.
- DRC: `python3 /foss/pdks/ihp-sg13cmos5l/libs.tech/klayout/tech/drc/run_drc.py --path=<gds> --topcell=<cell>
  --no_density --mp=4 --run_dir=<dir>`. Grep its log for "exception": the runner prints "Passed" even when a table
  crashes. 0 violations.
- LVS: `python3 /foss/pdks/ihp-sg13cmos5l/libs.tech/klayout/tech/lvs/run_lvs.py --layout=<gds> --netlist=<cdl>
  --topcell=<cell> --run_dir=<dir> --disable_tap_extraction`.
- PNGs, one per cell, readable at full-cell zoom, plus a close-up of a row end and of a gate-contact region per cell
  type (see `inputs/C2_P2/out/` for the style).

## Deliverables (`out/`)

- `s2d_p3_cells.gds` (cells named `<name>_c3`), `s2d_p3_cells.cdl` (one `.subckt` per cell, every dummy a device),
  `build_s2d_p3.py` (re-runnable from `out/`).
- PNGs; DRC / LVS / sym_check logs in `out/logs/`.
- `report.md` (under ~120 lines). Per cell:
  - size, and area against the library cell;
  - the row / dummy / symmetry scheme, as an ASCII map per row;
  - the gate-contact scheme and the dummy ties;
  - taps and LU numbers;
  - the netlist changes;
  - the pins with coordinates;
  - the sym_check results.
- When done, reply with a five-line summary and the file list with sha256 (first 12 hex). Do not report success that
  you have not checked.
