<!--
SPDX-FileCopyrightText: 2026 Christoph Maier
SPDX-License-Identifier: Apache-2.0
-->
# Brief F: floorplan and assembly of `pad_ref_rb` (cloud session C4, 2026-11-07) 

You are agent F, the floorplan and assembly agent of the replica bias `pad_ref_rb`. You build it **bottom-up** from
the rows of agents P, P3 and N (checked by the lead), as C3's F built the s2d pad's buffer. This brief covers
**stage A only**: placement and compaction, no routing. Christoph reviews your placement picture before any routing
(stage B). Model: Opus, effort high.

**Workspace:** yours only, `$WS` = `layout_rb/F` (`inputs/` read-only, `work/`, `out/`). Write nowhere else. Report to
`layout_rb/reports/F_report.md` (the lead copies it to the notes branch).

## Inputs (`$WS/inputs/`)

- **Rows** (each DRC 0, LVS match against its CDL, mirror-symmetric; reports in `reports/`):
  - `P/rb_p_cells.gds` / `.cdl`: `rb_tree_p`, `rb_tails`, `rb_tubs` (its `rb_avg` is superseded, do not use it).
  - `P3/rb_avg_v3.gds` / `.cdl`: `rb_avg` (two wells, gh and m; pins gh top, m both sides, xp bottom, M1).
  - `N/rb_n_cells.gds` / `.cdl`: `rb_tree_n`, `rb_casc`, `rb_mirror`, `rb_cload`, `bypass_rb` (pins in
    `N/build_stdout.txt`).
  - The build scripts `build_rb_p.py`, `build_s2d_p3.py`, `build_rb_avg_v3.py`, `build_rb_n.py` (C3's generators).
  - `inputs_overview.png`: the 9 cells at one scale, 4772 µm² of cell area in total.
- **Circuit:** `pad_ref_rb.spice` (bias_tree_rb, bypass_rb, pad_ref_rb), `vcm_rb.spice`, `vref_s2d_rb.spice`, with
  every layout dummy; the sheets' renders. `cdl_vs_circuit.txt`: the lead's check, 42 / 42 active devices drawn.
- **Precedent:** C3 F's brief, stage notes and code (`agents_c3/F/`: `BRIEF.md`, `stage_A_note.md`,
  `report_stageB*.md`, `out/src/`). **Reuse its code and approach.** The s2d pad cell it produced, for reference.
- **Slot context (read only):** `slot/slot.klay.gds` (the slot7 frame, 537.15 × 273 µm, top cell `slot`) and
  `slot/slot7_pins.md` (the 13 custom-pad pins on the slot's right edge, Metal3). The custom pads sit outside the
  slot's right edge.
- **Rules:** `BRIEF_common.md` (its section "Binding rules, verbatim from the briefs of the pads' layout agents" is
  binding for you as well), `NOTES_for_F.md`, `sym_check.py`, `SG13CMOS5L_os_layout_rules.txt`.

## What goes into the cell

- `pad_ref_rb` = `bias_tree_rb` + `vcm_rb` + `vref_s2d_rb` + `bypass_rb`, LVS'd **flat** against the source netlist.
  The rows mix subcells on purpose (they copy the pad's rows): `rb_tree_n` holds NI / NBP (tree), SH1 / SH2 / SY
  (vcm_rb), SF (vref_s2d_rb); `rb_casc` holds BNC (tree), CY (vcm_rb), F1–F4 (vref_s2d_rb); `rb_cload` holds CB
  (vcm_rb), the 9th CBR (bypass_rb), both SPD.
- Ports: `vddh vssh iref vcm vref en_3v3 en_3v3_b`. **Pin names `vddh` / `vssh`** (Christoph: "so they can be
  connected without conflict either way": to iovdd / iovss of the custom pads or to vdd_3v3 / vss_3v3 of the slot);
  the circuit netlists call them vdd / vss. `iref` is 5 µA sourced into the cell.
- Internal nets and who shares them (for the grouping):

  | net | cells |
  |---|---|
  | vbp | rb_tree_p (BP diode, PBNC gate) ↔ rb_tree_n (NBP drain) → rb_tails (TR, BT, dummies) |
  | ni | rb_tree_n (NI diode, all its gates, TGN, TDN) ↔ rb_tree_p (TGP) |
  | iref, en_3v3, en_3v3_b | ports → rb_tree_n (TGN, TDN), rb_tree_p (TGP); en_3v3_b also rb_cload (SPDC, SPDR) |
  | vbnc | rb_tree_p (PBNC drain) → rb_casc (BNC diode, all fingers) |
  | ts, bt | rb_tails → rb_tubs (TR → MR, BT → BA / BB tub sources) |
  | gh | rb_tubs (MR) ↔ rb_avg (SU, well gh) ↔ rb_tree_n (SH1, SH2) |
  | m | rb_avg (SU / SL, well m) → rb_tubs (BA gate) |
  | xp | rb_casc (CY) ↔ rb_tree_n (SY) ↔ rb_avg (SL1, SL2) |
  | bd | rb_tubs (BA) → rb_mirror (BD, BM gates) |
  | vcm | rb_tubs (BB) ↔ rb_mirror (BM) ↔ rb_cload (CB, SPDC) ↔ bypass_rb (CBM) → port |
  | vref | rb_casc (F1–F4) ↔ rb_tree_n (SF) ↔ rb_cload (CBR, SPDR) ↔ bypass_rb (CBR) → port |

## Rules (binding)

1–4 and 7 are C3 F's rules verbatim (Christoph's rules for the pad's assembly); the lead's additions for
pad_ref_rb are marked **[lead]**; 5, 6, 8 and 9 replace the pad-template rules (Christoph, 2026-11-07).

1. **Bottom-up** (Christoph, C2 17:55): "F should adapt its floorplan to compacted layout primitives (maybe put in
   context), not top down with an unrealistic floorplan cast in stone." Nothing goes back to P / N as a constraint.
2. **"adapt the floorplan for compact connection of the layout primitives, not the other way around"** (C2, 14:25).
   Group by signal flow. **[lead]** For pad_ref_rb: each tail under its tub (TR under MR, BT under BA / BB); rb_avg between
   rb_tubs and rb_tree_n / rb_casc (gh, m, xp); rb_mirror next to BA / BB; rb_tree_p next to rb_tails (vbp) and
   rb_casc (vbnc); rb_cload and bypass_rb on vcm / vref next to their drivers; short, equal wires.
3. **You may change your copies of the rows** to compact further (`<cell>_f`, each DRC clean and LVS-matched on its
   own; list every change). Symmetry and gate contacts stay as drawn: rows mirror-symmetric about the line dividing
   them; the same dummy at both ends of every row; no necked gate poly; dummies' source and drain on the rails, gate by
   abutment. Check every changed copy with `sym_check.py`. **[lead] Exception (Christoph): rb_casc stays as drawn (A), do not
   trim it.** The small switches may leave their rings (rule 9).
4. **Christoph's rules** of 2026-10-28 and of his C2 reviews: no taps between rows of arrayed transistors; one NWell
   per rail (the input tubs **[lead]** and rb_avg's wells keep their own) and no well notches; taps as rings where space allows;
   switches with the cells they serve; contact gates with poly; American English.
5. **Where the cell goes and its pins** (Christoph, 2026-11-07; **[lead]** geometry from `slot7_pins.md`):
   - "Look at where the voltages are needed by the custom pads. The replica bias block should end up close, and
     routing should be easy." The S2D pad takes `vref` at the slot's right edge at y 112.1 and `vcm` at y 135.9; the
     D2S pad takes the same `vcm` as its `vref` at y 223.2 (slot coordinates, the edge at x ≈ 535). slot7's bottom
     right is free except the frame's M2 vss_1v2 strip at x 533.15–535.15, y 11.6–71.1 and the edge keep-out
     x 535.15–537.15: place the cell there, below y 112, with its pin side toward those pins.
   - "Try to reproduce the connection sequence of the slot7 boundary to the custom pads." Along the boundary, bottom
     to top: vref, (outp, outn), vcm, en_3v3, en_3v3_b, iref. Put the cell's signal pins in that order:
     **vref, vcm, en_3v3, en_3v3_b, iref**, so that the routes to the boundary and the enable / iref lines run
     side by side without crossing.
   - "Don't stretch the connections out unnecessarily to match the slot-to-custom-pads boundaries." Keep the pins'
     pitch compact (routing pitch), not the boundary's 6–23 µm spacing.
   - `vddh` / `vssh` as rails or rings on the side away from the signal pins, or where the rows need them.
   - Show the cell in context: a picture of the slot's bottom-right corner with the cell placed, the boundary pins
     and straight-line sketches of the five connections. The slot files stay unchanged; the top-level routing is not
     yours.
6. **Metal: M1 / M2 only** (Christoph: "Pad structures are only routed M1/M2. Let's keep it that way for
   consistency."). No M3 or above inside the cell; reserve M1 / M2 wiring channels in the placement and say how wide
   and why. Each supply tapped at one point per row.
7. **Rule values only from the PDK decks and documents**, cited with file and rule name. Keep code small.
8. **Latch-up and area:** LU.a / LU.b 20 µm for every placed cell (bypass_rb is at 19.44 µm alone). slot7's bottom
   has room ("we have area to waste"), but keep the layout compact "if only for matching purposes"; report the area
   against the 4772 µm² of cells and the 85 × 85 µm estimate.
9. **The small switch transistors** (Christoph: "Might be a good idea to move the small transistors in rb_tree_n and
   rb_tree_p out of the main transistors' guard ring. Not a must."): TGN / TDN (rb_tree_n) and TGP (rb_tree_p) may
   leave their rows' rings, as `<cell>_f` copies, if that shortens the ring or the wiring; say what you did and why.

## Stage A deliverables (`out/`), then stop

- `placement_A.gds`, top cell `pad_ref_rb`: your placed cells and reworked copies, unrouted.
- `out/previews/placement_A.png` (cells and nets named, channels marked) and close-ups of the densest regions.
- Every changed cell `<cell>_f` in `out/cells/` (`.gds` + `.cdl`) with its DRC / LVS / sym_check logs.
- DRC on `placement_A.gds`: `run_drc.py --no_density` (grep for "exception") and `sg13cmos5l_maximal.drc -rd
  latchUpRules=true`.
- `out/previews/context_A.png`: the slot's bottom-right corner with the placed cell, the boundary pins and the
  connection sketches (rule 5).
- `out/stage_A_note.md` (under ~80 lines): area per block and in total, bounding box, the wiring channels, every
  change to the rows, the pin plan and the cell's proposed position in the slot, what stage B needs.
- Reply with a summary of no more than 15 lines and the `out/` file list with sha256 (first 12 hex), then stop.

## Checks and hard rules (as C3 F)

- DRC `run_drc.py --path --topcell --no_density --mp=4 --run_dir`; LVS `run_lvs.py ... --disable_tap_extraction`
  (`--run_mode=deep` for hierarchy); `sym_check.py`. Three rounds at most per cell, then report it.
- No git, no web, no `mcp__*` tools. Say which statements are measured and which are reasoning
  (`TZ=Europe/Berlin date` for times). Background commands under 2 h; kill by PID, never `pkill -f`.
