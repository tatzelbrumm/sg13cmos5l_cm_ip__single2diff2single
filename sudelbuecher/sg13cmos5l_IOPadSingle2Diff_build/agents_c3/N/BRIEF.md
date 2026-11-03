<!--
SPDX-FileCopyrightText: 2026 Christoph Maier
SPDX-License-Identifier: Apache-2.0
-->
# Brief N: compact NMOS and resistor layout primitives of the IOPadSingle2Diff pad (IHP sg13cmos5l), C3 2026-11-03

**Workspace (yours only):** `$WS` (the lead gives you the absolute path), with `inputs/` read-only, `work/` for
scratch and `out/` for deliverables.

**Your role:** you are the NMOS layout specialist for the **s2d** pad buffer `s2d_mpdda_pd`. Agent P draws the PMOS
cells in parallel. After the lead has checked your cells, agent F places and wires all cells in the pad, and may still
adapt them. Christoph then reviews F's placement.

**Start from C2's rebuild.** This is the second pad. The first, `sg13cmos5l_IOPadDiff2Single` (C2), had a rejected
first attempt and an accepted rebuild by P2 / N2 (Opus). Use:
- `inputs/C2_N2/out/`: `build_d2s_n2.py`, the cells, `report.md`; and `inputs/C2_P2/out/`;
- F2's later fixes of those cells: `inputs/C2_F2/report_stageB.md` and `out/cells/` (`d2s_f2b_n_cells.gds`, among
  them `sinks_6x6_f2`, `d2s_rhigh_f2`, `d2s_casc_n_f2`, `d2s_pd_n_f2` / `_fs`, `bias_tree_n_f2`, `d2s_tgsw_f2`).

**Reuse their code and approach; do not start from scratch.**

## Christoph's rules (binding; they come before compactness)

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

## Your cells

**Circuit:** `inputs/circuit/s2d_mpdda.spice` (subckt `s2d_mpdda`), `s2d_pd.spice` (`s2d_mpdda_pd`), `units.spice`
(`unit_r2`), `bias_tree_noab_pd.spice`, `bias_ref_pd.spice` (`bias_diodes`), and the sheets. In the pad, the cell's
`vdd` is iovdd and `vss` is iovss.

| cell (deliver as `<name>_c3`) | devices |
|---|---|
| `sinks_6x6_s2d` | SX (x) / SY (y): 6 + 6 fingers hv NMOS 6/6 on vbn (w=36u ng=6 each), BN (diode vbn, 6/6), dummies. **Start from N2's `sinks_6x6_s2d_c2`. Check it against the s2d circuit, and change only what rules 3 and 6 require (F2's `sinks_6x6_f2` shows the fix of the center contacts).** It is not a redraw: list every change. |
| `s2d_sinks_cmfb` | SXC (xc) / SYC (yc): 4 + 4 fingers hv NMOS 6/6 on vbn (w=24u ng=4 each); same finger and style as the sinks |
| `s2d_casc_n` | CX (voutp ← x), CY (voutn ← y), CXC (vcmfb ← xc), CYC (vdd ← yc): hv NMOS 15/3, 2 fingers each (w=30u l=3u ng=2), gate vbnc; BNC (diode vbnc, 1/8) |
| `s2d_pd_n` | TPN (voutp – vcm), TNN (voutn – vcm): hv NMOS 1/0.45, gate en_3v3_b, bulk vss |
| `s2d_cload` | CLP (gate voutp), CLN (gate voutn): hv NMOS 12 × 12 µm, S / D / B on vss (the built-in load). Keep them a matched pair |
| `s2d_rhigh` | the six `unit_r2` resistors (A1 A2 F1 F2 M1 M2; rhigh 0.5 / 50.6 µm, 150 kΩ each), each as 4 series segments of 0.5 / 12.65 µm. Terminals sa_U / sb_U, body vss; dummy strips at both ends. N2's / F2's `d2s_rhigh` (4 resistors) is the template; the tap becomes a ring where space allows |
| `bias_tree_noab_n` | NI (diode ni, 6/6), NBP (vbp ← ni-gated, 6/6), NBPC (vbpc, 2.4/6), and the switches TGN (iref – ni, gate en_3v3, 1/0.45) and TDN (ni → vss, gate en_3v3_b, 1/0.45). This is C2's `bias_tree_n_c2` / F2's `bias_tree_n_f2` + `d2s_tgsw_f2` without NABP; place the switches with the tree (rule 6) |

**Library sources:** `inputs/pad_buffer_klayout/` (`pad_buffer_cells.gds` / `.cdl` / `.py`, `cell_tree.md`,
`README.md`, Q&A). **Earlier compaction rules:** `inputs/A3/` (`skill/generic/rules.md`, `skill/ihp_sg13cmos5l/rules.md`).

## Hard rules

- Work only in your workspace. No git, no web searches, no `mcp__*` tools. Don't touch `inputs/`.
- Take rule values only from the PDK's decks and documents:
  `/foss/pdks/ihp-sg13cmos5l/libs.tech/klayout/tech/drc/rule_decks/` (`sg13cmos5l_tech_default.json`, the `.drc`
  files) and `inputs/SG13CMOS5L_os_layout_rules.txt`. Cite file and rule.
- Say which statements are measured facts and which are reasoning. Times: `TZ=Europe/Berlin date`.
- Keep code small: no "just in case" options, no script piled on script.
- Background commands die after 2 h. Kill processes by PID, never with `pkill -f`.

## Checks

Run each check once, and once more after each fix. A cell that is not clean after three rounds is reported and left.

- **Symmetry:** `python3 inputs/sym_check.py <gds> <cell> [--x ..] [--y ..] [--no-y]`. Target 0; explain every
  residual, with its location.
- **DRC:** `python3 /foss/pdks/ihp-sg13cmos5l/libs.tech/klayout/tech/drc/run_drc.py --path=<gds> --topcell=<cell>
  --no_density --mp=4 --run_dir=<dir>`. Grep its log for "exception": the runner prints "Passed" even when a table
  crashes. Target: 0 violations.
- **LVS:** `python3 /foss/pdks/ihp-sg13cmos5l/libs.tech/klayout/tech/lvs/run_lvs.py --layout=<gds> --netlist=<cdl>
  --topcell=<cell> --run_dir=<dir> --disable_tap_extraction`.
- **PNGs:** one per cell, readable at full-cell zoom, plus a close-up of a row end and of a gate-contact region per
  cell type (see `inputs/C2_N2/out/` for the style).

## Deliverables (`out/`)

- `s2d_n3_cells.gds` (cells named `<name>_c3`), `s2d_n3_cells.cdl` (one `.subckt` per cell, every dummy a device),
  `build_s2d_n3.py` (re-runnable from `out/`).
- The PNGs, and the DRC / LVS / sym_check logs in `out/logs/`.
- `report.md` (under ~120 lines), per cell:
  - size, and area against the library cell;
  - the row / dummy / symmetry scheme, as an ASCII map per row;
  - the gate-contact scheme and dummy ties;
  - taps and LU numbers;
  - the netlist changes;
  - pins with coordinates;
  - sym_check results.

  For `sinks_6x6_s2d`, also the list of changes against N2's cell.
- When done, reply with a five-line summary and the file list with sha256 (first 12 hex). Do not report success that
  you have not checked.
