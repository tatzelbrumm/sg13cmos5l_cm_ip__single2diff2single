# Brief N2: rebuild of the NMOS layout primitives of the IOPadDiff2Single pad (IHP sg13cmos5l), C2 2026-10-31

Workspace (yours only): `/home/user/c2/N2/` — `inputs/` read-only, `work/` scratch, `out/` deliverables.
You are the NMOS layout specialist. A first attempt at these cells was **rejected** by the designer (Christoph); it is
in `inputs/rejected_v1/` as a negative example. A second agent (P2) rebuilds the PMOS cells in parallel. After the
lead's check your cells go to **Christoph's manual review**; nothing is assembled before he accepts them.

## Why the first attempt was rejected (Christoph, 2026-10-31 18:55, verbatim)

> d2s_loads have asymmetric dummies. Best: symmetric rows along the line dividing the rows, symmetric dummies. Worse:
> symmetric rows along the line dividing the rows, no dummies
> ABSOLUTELY, UNACCEPTABLY WORST: dummies on only one (mismatching) side of each row.
> Applies also to sinks_6x6. d2s_tails, d2s_casc_n, d2s_casc_p look horrible, too. The input differential pairs have
> the kind of narrowed poly contacts already eliminated in other cells. Based on this, the entire layout is f$cked up
> from the bottom up.

Look at `inputs/rejected_v1/*.png` and run `inputs/sym_check.py` on `inputs/rejected_v1/d2s_n_cells.gds` (and `d2s_rhigh.gds`) to see what
went wrong before you start.

## Layout quality rules (binding; they come first, before compactness)

1. **Symmetry.** A two-row array is mirror-symmetric about the line dividing the rows. Within each row the device
   layers are mirror-symmetric about the row's centre line: the dummies at both ends of every row are the same
   device. Order of preference: (a) symmetric rows with symmetric dummies at both ends of every row; (b) symmetric
   rows with no dummies; **never** dummies at one end only, or different dummies at the two ends. A bias diode that
   takes an end position (BP in the tails) needs its twin at the other end (a dummy of the same W / L) or goes to the
   middle of the map; say which and why. (BN in the sinks, BNC in casc_n likewise.)
2. **Gate contacts on full-width poly.** No narrowed poly links ("necks") between a gate and its contact. The
   accepted ways, from Christoph's earlier decisions in `inputs/log.md`:
   - a gate-contact column along the full gate head, on a poly tab as wide as the gate (sinks_6x6, log entries
     "00:57: sinks_6x6 gate connection" ("isn't the gate contact through narrow poly VERY flimsy?") and "01:03–01:14"
     ("Don't mess with the drain contacts of the transistors. DON'T BREAK UP THE TRANSISTOR ARRAY!!!"), accepted at
     "01:20–01:30");
   - contacts on the gate heads themselves, no poly stubs or bars ("02:41: bg_pmir_pcas");
   - gate contacts close to the device so that a Via1 fits ("17:43: gate contacts closer to the devices").
3. **Unmodified device cells.** Use the PDK's PCell transistors (as the library does); don't shorten drain or source
   contacts; don't break up a transistor array.
4. **Christoph's rules of 2026-10-28:** no substrate taps between rows of arrayed transistors (taps only at the
   periphery; check LU.b 20 µm, layout rules §7.2.2); a tap ring is optional and needn't be rectangular; narrow dummies
   (but rule 1 first: the same narrow dummy at both ends). Your cells have no NWell (bulk = substrate = vss).
5. **The circuit sets the maps and ratios:** common-centroid maps of `inputs/layout_primitives.md` §5 (sinks
   `X Y Y X X Y / Y X X Y Y X` with BN and a dummy at the ends — which rule 1 now asks to make symmetric; R block
   `A B C1 C2 C2 C1 B A A B C1 C2 C2 C1 B A`). The sinks dominate the offset (5.4 of 6.1 mV, §1): keep their finger
   count a parameter (the 4× option), and their source bus with BN tapped to vss at one point (§6); W / L / finger counts
   from the circuit. A change needs a reason in the report.
6. **No floorplan constraints.** Draw each cell on its own merits: compact, symmetric, with pins on its edges where
   they serve the cell's nets. The assembly agent adapts to your cells, not the other way round.

## Your cells

Circuit: `inputs/circuit/d2s_mpdda_pd.spice` (subckt `d2s_mpdda_pd`), `units.spice` (`unit_r2`), `d2s_mpdda_pd.sch`,
`unit_r2.sch`; `bias_ref_pd.spice` (subckt `bias_tree_pd`) and `bias_tree_pd.sch`.

| cell | devices |
|---|---|
| `sinks_6x6` | SX / SY 6 + 6 fingers hv NMOS 6/6 on vbn (the sheet's `w=36u ng=4` becomes 6 × 6/6, `layout_primitives.md` §7 decision 1), BN (diode, 6/6), dummies; shared with the s2d pad: keep a variant for it |
| `d2s_casc_n` | CX (l1 ← x) / CY (b ← y) 15/3, 2 fingers each, gate vbnc; BNC 1/8 (diode) |
| `d2s_ab_n` | RN2 (diode, source dabn), FNL, ABN: single 4.4/1 fingers, gate vabn (RN1 is in the clamp frame) |
| `d2s_pd_n` | XSB (b → vsso, gate en_3v3_b), XSABN (vabn → vss): hv NMOS 1/0.45, separate sources (vsso / vss); bulk vss |
| `bias_tree_n` | the NMOS of `bias_tree_pd`: NI (diode, ni), NBP, NBPC (2.4/6), NABP on ni, and the switches TGN, TDN (1/0.45); see the library cells `bias_tree_n`, `bias_tree_sw` |
| `d2s_rhigh` | the four `unit_r2` resistors (rhigh 0.5 / 50.6 µm, 150 kΩ) each as 4 series segments of 0.5 / 12.65 µm, R map of §5, dummy strips at both ends; terminals sa_U / sb_U, body vss; the way `inputs/bg_res/bg_res_c.gds` is drawn (`build_bg_res_c.py`) |

Library sources: `inputs/pad_buffer_klayout/pad_buffer_cells.gds` / `.cdl` / `.py`, `cell_tree.md`, `README.md`, the
Q&A files. Compaction code and rules of the earlier NMOS specialist: `inputs/A3/out/` (`build_oa_n.py`,
`skill/generic/rules.md`, `skill/ihp_sg13cmos5l/rules.md`; its bandgap block in `report_bg*.md`). The library's
`sinks_6x6` (Christoph accepted it at log "01:20–01:30": "your solution is good … Keep it!") is the reference for the
sinks' gate contacts and drain wiring.

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

- `d2s_n2_cells.gds` (cells named `<name>_c2`), `d2s_n2_cells.cdl` (one `.subckt` per cell, every dummy a device),
  `build_d2s_n2.py` (re-runnable from `out/`).
- PNGs; DRC / LVS / sym_check logs in `out/logs/`.
- `report.md` (under ~120 lines): per cell the size, the row / dummy / symmetry scheme (a small ASCII map of each row,
  e.g. `D | X Y Y X X Y | D`, mirrored row below), the gate-contact scheme, taps and LU numbers, the netlist changes
  (every w / l / ng / dummy change), the pin list with coordinates, and the sym_check results.
- When done, reply with a five-line summary and the file list with sha256 (first 12 hex). Do not report success that
  you have not checked.
