# Brief P2: rebuild of the PMOS layout primitives of the IOPadDiff2Single pad (IHP sg13cmos5l), C2 2026-10-31

Workspace (yours only): `/home/user/c2/P2/` — `inputs/` read-only, `work/` scratch, `out/` deliverables.
You are the PMOS layout specialist. A first attempt at these cells was **rejected** by the designer (Christoph); it is
in `inputs/rejected_v1/` as a negative example. A second agent (N2) rebuilds the NMOS cells in parallel. After the
lead's check your cells go to **Christoph's manual review**; nothing is assembled before he accepts them.

## Why the first attempt was rejected (Christoph, 2026-10-31 18:55, verbatim)

> d2s_loads have asymmetric dummies. Best: symmetric rows along the line dividing the rows, symmetric dummies. Worse:
> symmetric rows along the line dividing the rows, no dummies
> ABSOLUTELY, UNACCEPTABLY WORST: dummies on only one (mismatching) side of each row.
> Applies also to sinks_6x6. d2s_tails, d2s_casc_n, d2s_casc_p look horrible, too. The input differential pairs have
> the kind of narrowed poly contacts already eliminated in other cells. Based on this, the entire layout is f$cked up
> from the bottom up.

Look at `inputs/rejected_v1/*.png` and run `inputs/sym_check.py` on `inputs/rejected_v1/d2s_p_cells.gds` to see what
went wrong before you start.

## Layout quality rules (binding; they come first, before compactness)

1. **Symmetry.** A two-row array is mirror-symmetric about the line dividing the rows. Within each row the device
   layers are mirror-symmetric about the row's centre line: the dummies at both ends of every row are the same
   device. Order of preference: (a) symmetric rows with symmetric dummies at both ends of every row; (b) symmetric
   rows with no dummies; **never** dummies at one end only, or different dummies at the two ends. A bias diode that
   takes an end position (BP in the tails) needs its twin at the other end (a dummy of the same W / L) or goes to the
   middle of the map; say which and why.
2. **Gate contacts on full-width poly.** No narrowed poly links ("necks") between a gate and its contact. The
   accepted ways, from Christoph's earlier decisions in `inputs/log.md`:
   - a gate-contact column along the full gate head, on a poly tab as wide as the gate (sinks_6x6, log entries
     "00:57: sinks_6x6 gate connection" ("isn't the gate contact through narrow poly VERY flimsy?") and "01:03–01:14"
     ("Don't mess with the drain contacts of the transistors. DON'T BREAK UP THE TRANSISTOR ARRAY!!!"), accepted at
     "01:20–01:30");
   - contacts on the gate heads themselves, no poly stubs or bars ("02:41: bg_pmir_pcas");
   - gate contacts close to the device so that a Via1 fits ("17:43: gate contacts closer to the devices").
   The library's `tub_p20x1` (input devices) has exactly the kind of narrowed poly contact Christoph means: redo it.
3. **Unmodified device cells.** Use the PDK's PCell transistors (as the library does); don't shorten drain or source
   contacts; don't break up a transistor array.
4. **Christoph's rules of 2026-10-28:** no substrate / well taps between rows of arrayed transistors (taps only at the
   periphery; check LU.a 20 µm, layout rules §7.2.2); one NWell per rail, not separate wells, NWell polygonal where the
   rules allow (exception: each input device has bulk = source and keeps its own NWell, `layout_primitives.md` §3 P1,
   identical in every copy); a tap ring is optional and needn't be rectangular; narrow dummies (but rule 1 first: the
   same narrow dummy at both ends).
5. **The circuit sets the maps and ratios:** common-centroid maps of `inputs/layout_primitives.md` §5 (tubs and tails
   `Aa C2b C1b Ba / Bb C1a C2a Ab`, each tail under its tub's column; loads `L R R L L R R L`); W / L / finger counts
   from the circuit. A change needs a reason in the report.
6. **No floorplan constraints.** Draw each cell on its own merits: compact, symmetric, with pins on its edges where
   they serve the cell's nets. The assembly agent adapts to your cells, not the other way round.

## Your cells

Circuit: `inputs/circuit/d2s_mpdda_pd.spice` (subckt `d2s_mpdda_pd`), `units.spice` (`unit_r2`), `d2s_mpdda_pd.sch`,
`unit_r2.sch`; `bias_ref_pd.spice` (subckt `bias_tree_pd`) and `bias_tree_pd.sch`.

| cell | devices |
|---|---|
| `d2s_inputs` (with its input-device cell) | 8 input devices hv PMOS 2 × 10/1, bulk = source, each in its own NWell; dummy tubs at both ends of both rows |
| `d2s_tails` | 8 tails hv PMOS 5/6 on vbp, BP (diode, 5/6), dummies; one NWell on vdd |
| `d2s_loads` | PL / PR hv PMOS 6/4 fingers (2 × 4), gate l2 |
| `d2s_casc_p` | PCL / PCR 15/3 (2 fingers each, gate vbpc), BPC 1/4 (diode) |
| `d2s_ab_p` | RP2 (diode, source dabp), FPL, ABP: single 6.66/0.6 fingers, gate vabp (RP1 is in the clamp frame) |
| `d2s_pd_p` | XSA (a ← vddo, gate en_3v3), XSABP (vabp ← vdd): hv PMOS 1/0.45, separate sources (vddo / vdd); bulk vdd |
| `bias_tree_p` | the PMOS of `bias_tree_pd` without BP / BN / BPC / BNC (those sit in the tails, sinks and cascodes): PBN, PBNC, PABN (on vbp) and the swp switch TGP; see the library cells `bias_tree_p`, `bias_tree_swp` |

Library sources: `inputs/pad_buffer_klayout/pad_buffer_cells.gds` / `.cdl` / `.py`, `cell_tree.md`, `README.md`, the
Q&A files. Compaction code and rules of the earlier PMOS specialist: `inputs/A4/out/` (`build_oa_p.py`,
`skill/generic/rules.md`, `skill/ihp_sg13cmos5l/rules.md`); its `oa_pmir_c` is a good example of rule 1 (point
symmetric, 0 mirror XOR with `sym_check.py`).

## Hard rules

- Work only in your workspace. No git, no web searches, no `mcp__*` tools, do not touch `inputs/`.
- Rule values only from the PDK's decks and documents: `/foss/pdks/ihp-sg13cmos5l/libs.tech/klayout/tech/drc/rule_decks/`
  (`sg13cmos5l_tech_default.json`, the `.drc` files) and `inputs/SG13CMOS5L_os_layout_rules.txt`; cite file and rule.
- Measured facts vs. reasoning: say which is which. Times: `TZ=Europe/Berlin date`.
- Keep code small: no "just in case" options, no script piled on script.
- Background commands die after 2 h; kill processes by PID, never `pkill -f`.

## Checks (each once, and once more after each fix; a cell not clean after three rounds is reported and left)

- `python3 inputs/sym_check.py <gds> <cell> [--x ..] [--y ..] [--no-y]`: mirror XOR of the device layers about the row
  axes, and necked gate-contact poly. Target 0; explain every residual in the report (with its location).
- DRC: `python3 /foss/pdks/ihp-sg13cmos5l/libs.tech/klayout/tech/drc/run_drc.py --path=<gds> --topcell=<cell>
  --no_density --mp=4 --run_dir=<dir>`; grep its log for "generated an exception" (the runner prints "Passed" even
  when a table crashes). 0 violations, or a list of what remains and why.
- LVS: `python3 /foss/pdks/ihp-sg13cmos5l/libs.tech/klayout/tech/lvs/run_lvs.py --layout=<gds> --netlist=<cdl>
  --topcell=<cell> --run_dir=<dir> --disable_tap_extraction`.
- One PNG per cell, readable at full-cell zoom (device layers, contacts, M1, M2, labels), plus a close-up of a row end
  and of a gate-contact region per cell type.

## Deliverables (`out/`)

- `d2s_p2_cells.gds` (cells named `<name>_c2`), `d2s_p2_cells.cdl` (one `.subckt` per cell, every dummy a device),
  `build_d2s_p2.py` (re-runnable from `out/`).
- PNGs; DRC / LVS / sym_check logs in `out/logs/`.
- `report.md` (under ~120 lines): per cell the size, the row / dummy / symmetry scheme (a small ASCII map of each row,
  e.g. `D | L R R L L R R L | D`, mirrored row below), the gate-contact scheme, taps and LU numbers, the netlist changes
  (every w / l / ng / dummy change), the pin list with coordinates, and the sym_check results.
- When done, reply with a five-line summary and the file list with sha256 (first 12 hex). Do not report success that
  you have not checked.
