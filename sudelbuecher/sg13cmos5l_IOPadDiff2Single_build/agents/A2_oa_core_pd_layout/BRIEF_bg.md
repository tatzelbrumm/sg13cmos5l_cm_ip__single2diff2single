# Brief, part 2: layout of `bg_core_pd`, 2026-10-28

Same task and same hard rules as `BRIEF.md` (read it again): cloud workspace only, no `mcp__remote-devices__*` tools,
no git, inputs read-only, primitives copied unchanged (XOR-checked), rule values only from the PDK decks with file and
rule name, facts vs reasoning, `TZ=Europe/Berlin` times. Use what you built for `oa_core_pd` (build script structure,
DRC / LVS route, pin convention), so the two cores look alike and can sit side by side in `bias_gen_pd` / `bias_sel_pd`.

## Goal

A GDS with top cell `bg_core_pd`, the Banba current-mode bandgap core with power-down, as drawn in
`inputs_bg/bg_core_pd.sch` (ports in order `vdd vss iout en_3v3 en_3v3_b`), built from the bandgap primitives of
`inputs/pad_buffer_cells.gds`: `bg_pmir_pcas` (PMOS mirror + cascodes: PB, PBC, PA, PAC, PO, POC), `bg_nab` (NA / NB),
`bg_misc_n` (MS2, MS3, SKS), `bg_misc_p` (MS1 chain, SVPG; stays as delivered, the user's 08:45 decision covers it too),
`bg_pnp` (Q1 + 8 × Q2, pnpMPA), `bg_res` (R1A, R1B, R0, rhigh). The cell tree in `inputs/cell_tree.md` predates the
merge of bg_pmir / bg_pcas into `bg_pmir_pcas`; the log (`inputs/pad_buffer_layout_log.md`) is newer. Read the bg entries
there. `cell_tree.md` marks bg_pnp and bg_res as "placed only": find out what that means for their internal wiring
before you rely on them, and say in the report what you had to add.

## Inputs (new, in `inputs_bg/`)

| file | what |
|---|---|
| `bg_core_pd.sch`, `.sym` | the schematic |
| `bg_core_pd_xschem.spice` | xschem netlist of the sheet, made here |
| `bg_core_pd_README.md`, `bias_bg_pd_README.md` | what the core does: V_BE1 / R1 + U_T ln 8 / R0 = 2.5 µA per branch, PO / POC source about 5 µA out of `iout`; disabled = high-Z |
| `bg_misc_p.gds`, `bg_nab.gds`, `bg_pmir_pcas.gds`, `bg_pnp.gds`, `bg_res.gds` | the standalone exports; confirm by XOR that the library carries the same versions and use the library |
| `../inputs/bias_ref_pd.spice` | the hand source netlist, subckt `bg_core_pd` (compare with the sheet and report) |

## Specific points

- Matching: Q1 / Q2 (1 : 8, the 3 × 3 array with Q1 in the centre), R1A / R1B and R0 (one rhigh array), PA / PB / PO
  mirror ratios. Keep the primitives' common-centroid wiring intact; route the emitter and resistor nets (`ea`, `eb`,
  `e2`) short and symmetric, away from `iout` and the enable lines.
- Envelope: as for oa_core_pd after the 01:47 change, a compact block for the core side of slot 7 (macros/slot,
  537.15 × 273 µm), not the pad's 80 µm zone. Minimum area, aspect roughly square to 2:1, Metal1 / Metal2 wiring where
  possible (Metal3 and above free for slot routing; report every layer used), vdd / vss rails along the edges, ports
  on the block edge, and the same edge / pin conventions as oa_core_pd so the two blocks abut.

## Deliverables in `$A/out_bg/`

`bg_core_pd.gds`, `bg_core_pd_build.py`, `bg_core_pd.cdl`, DRC / LVS logs, `bg_core_pd.png`, and the report text
(aim for under 150 lines, five-line summary first). If the harness blocks writing `.md` files, put the report in your
final reply as you did before. Reply with the summary and the file list with sha256 (first 12 hex).
