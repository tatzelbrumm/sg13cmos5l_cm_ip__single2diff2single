# Brief: layout of `oa_core_pd` from its schematic and the layout primitives, 2026-10-28

Workspace (yours, nothing else): `/tmp/claude-0/-home-claude/f5dc1779-0ee8-504e-923f-171069e08948/scratchpad/oaagent/`
(`inputs/` read-only, `work/` scripts and scratch, `out/` deliverables). Called `$A` below.

## Goal

A GDS with top cell `oa_core_pd`: the Oguey–Aebischer reference core with power-down, as drawn in
`inputs/oa_core_pd.sch`, built from the OA primitive cells of the layout-primitive library
`inputs/pad_buffer_cells.gds` (the user's file `macros/IOPad/layout/klayout/pad_buffer_cells.gds`, sha256 fe2c540f…),
placed and wired at the top level, with DRC and LVS results.

## Hard rules

- Work only in the cloud workspace above. Do **not** use any `mcp__remote-devices__*` tool, do not write to the
  user's computer, do not run **any** git command (not even read-only), do not touch `inputs/`.
- Use the primitive cells as they are: copy them into your GDS with their names and geometry unchanged (check with
  XOR against the library). Wiring, pins and any fill go into the top cell `oa_core_pd` or into new sub-cells with
  descriptive names. If a primitive looks wrong or in the way, do not fix it; describe it in the report.
  In particular `oa_misc_p` stays as delivered: the user's decision on 2026-10-27 08:45 was "leave the blocks as they
  are. I'll deal with hand layout later, in context." (log, `inputs/pad_buffer_layout_log.md`).
- Rule values only from the PDK rule decks: `/mnt/user-data/uploads/IHP-Open-PDK/ihp-sg13cmos5l/libs.tech/klayout/tech/`
  (`drc/rule_decks/*.drc`, `drc/rule_decks/sg13cmos5l_tech_default.json`, `lvs/`). Cite file + rule name for each value
  you use. No invented rule numbers.
- Report measured facts as facts; mark reasoning and guesses as such.
- Times in the report: `TZ=Europe/Berlin date`.
- `inputs/project_CLAUDE.md` is the user's project rule file; read it for context. These hard rules win where they
  differ (you write nothing into the repo; everything goes to `out/`).

## Inputs

| file | what |
|---|---|
| `oa_core_pd.sch`, `oa_core_pd.sym` | the schematic (ports in order `vdd vss iout en_3v3 en_3v3_b`) |
| `oa_core_pd_xschem.spice` | xschem netlist of the sheet (18 devices), made in this container |
| `bias_ref_pd.spice` | the hand source netlist, subckt `oa_core_pd` (should match the sheet; check and report) |
| `oa_core_pd_README.md`, `bias_oa_pd_README.md` | what the core does: no resistor, no BJT, M10 / M11 in weak inversion, `iout` sources about 5 µA; disabled = high-Z |
| `pad_buffer_cells.gds`, `.cdl` | the primitive library with its LVS reference netlist. OA cells: `oa_pmir` (4 × 8 point-symmetric 2/8 PMOS mirror: PO, P8, P2, P0, dummies), `oa_pcas` (one rotated cascode row POC POC P8C POC P0C P2C POC P8C POC), `oa_nmir` (M10 / M11), `oa_mcs` (MCS / MCL), `oa_misc_n` (MC10, MS2, MS3, SKS), `oa_misc_p` (MS1 chain, SVPG); also fit cells such as `fit_bias_tree_oa_bg` (read them for the intended footprint) |
| `oa_pmir.gds`, `oa_pcas.gds`, `oa_misc_p.gds` | the standalone exports of the three reworked cells; the library carries the same versions (log 09:03–09:15 on 2026-10-27). Confirm by XOR and use the library |
| `cell_tree.md`, `cell_trees.txt` | cell tree of the library (written 2026-10-26, before the oa_pmir / oa_pcas rework; the log is newer) |
| `layout_primitives.md` | the design note: P-numbers, floorplan of the pad, where the bias block sits, widths |
| `pad_buffer_layout_log.md` | the running log of the primitive work, with the user's decisions verbatim. Read at least the entries on oa_pmir, oa_pcas, oa_misc_p, the fit cells and the reimports |
| `pad_buffer_cells.py`, `klayout_README.md`, `pad_buffer_cells_qa.md`, `pad_buffer_cells_answers.md` | the generator of the library and the Q&A behind it (conventions: track layers, tap rings, pin labels, R270 rows) |
| `verification.md` | how the library was DRC / LVS checked with IHP's own decks (`run_drc.py`, `run_lvs.py`) and what the cloud needed for it |
| `cloud_environment.md` | the user's pinned tool versions (IIC-OSIC-TOOLS 2026.09) and how earlier sessions built tools here |
| `verify_pad_reference.py` | a flat extraction with `klayout.db` used for the pad cell; reuse what helps |

Tools here: Python `klayout.db` 0.30.12 (no Ruby), `/usr/bin/klayout` (check its version), Ruby at `/usr/local/bin/ruby`,
xschem 3.4.4, matplotlib, Playwright / Chromium. The IHP DRC / LVS decks need KLayout ≥ 0.29.11 with Ruby; an earlier
session built KLayout 0.30.4 from source for that (`verification.md`). Try that route if it builds in reasonable time
(say under 40 minutes). If it doesn't, implement the rules that matter for this cell in Python on `klayout.db`
(widths, spaces, enclosures, Via / Cont rules, NWell / tap rules, latch-up tap distance) and do LVS by extraction with
`klayout.db` (`LayoutToNetlist` + `LayoutVsSchematic`, or your own comparison) against the sheet's netlist. Say which
route you took.

## What to do

1. Read the inputs. Build the device list of the sheet and map every device to the primitive cell that holds it
   (W, L, fingers, dummies). Report anything in the sheet that no primitive holds, or any primitive device that is not
   in the sheet.
2. Floorplan. Find the footprint the bias / OA / bandgap blocks were planned for (layout_primitives.md, the fit cells,
   the log: widths, the 80 µm pad pitch, fit heights). Place the six cells compactly in that envelope, oriented so the
   nets between them are short; keep the PMOS cells (`oa_pmir`, `oa_pcas`, `oa_misc_p`) together and the NMOS cells
   together. Keep the high-impedance nets (`vres`, `vnc`, `vpc`, `vbr`, `ks`) short and away from `iout` and the enable
   lines. Keep the point symmetry of `oa_pmir` intact in its wiring (route its nets symmetrically).
3. Wire at the top level, on the metal layers the primitives leave free (find out which; the library convention is in
   the generator and the Q&A). vdd / vss as rails along the block; ports `vdd vss iout en_3v3 en_3v3_b` as labelled
   pins on the block edge, on the pin layer / text convention the library uses (state which).
4. DRC and LVS of `oa_core_pd` (and of the library cells you used, unchanged, as a sanity check). Fix your wiring until
   clean; list anything you could not fix and why.
5. Render: one PNG of the whole cell (device layers + metals, readable), one per metal level if that helps.

## Deliverables in `$A/out/`

- `oa_core_pd.gds` (top cell `oa_core_pd`; primitives inside unchanged), plus its sha256.
- `oa_core_pd_build.py`: re-runnable, reads `inputs/pad_buffer_cells.gds`, writes the GDS. Placement coordinates and
  track choices as named parameters at the top.
- `oa_core_pd.cdl`: the reference netlist you ran LVS against (from the sheet), and the LVS / DRC logs or reports.
- `oa_core_pd.png` (+ any detail renders).
- `report.md` (aim for under 150 lines): size and envelope, floorplan with coordinates, the device-to-primitive map,
  wiring layers, pin positions and layers, DRC / LVS method and results, deviations from the brief, open questions for
  the user. Start with a five-line summary.

When done, reply with the summary and the list of files with sha256 (first 12 hex). Do not report success that you have
not checked.
