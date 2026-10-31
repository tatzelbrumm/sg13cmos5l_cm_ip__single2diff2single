# Brief P: compact PMOS primitives of `d2s_mpdda_pd` for the IOPadDiff2Single pad cell (IHP sg13cmos5l), C2 2026-10-31

Workspace (yours only): `/home/user/c2/P/` — `inputs/` read-only, `work/` scratch, `out/` deliverables.
You are the PMOS specialist (as A4 on 2026-10-28: `inputs/A4/BRIEF.md`, `report.md`, `out/` with its generator and
`out/skill/`). A second agent (N) does the NMOS cells; a third (F) assembles the pad cell's amplifier block from your
cells. The lead checks every cell you deliver (XOR against your GDS, its own DRC and LVS, a flat extraction of every
device's W / L / nets) before F gets it, and relays F's requests to you.

## Hard rules

- Work only in your workspace. No git (not even read-only), no web searches, no `mcp__*` tools, do not touch `inputs/`.
- Rule values only from the PDK's decks and documents: `/foss/pdks/ihp-sg13cmos5l/libs.tech/klayout/tech/drc/rule_decks/`
  (`sg13cmos5l_tech_default.json` and the `.drc` files) and the layout rules (`inputs/SG13CMOS5L_os_layout_rules.txt`);
  cite file and rule name for every value. No invented numbers.
- Measured facts vs. reasoning: say which is which. Times: `TZ=Europe/Berlin date`.
- Existing code first: start from the library cells (`inputs/pad_buffer_klayout/pad_buffer_cells.gds`, generator
  `pad_buffer_cells.py`, reference netlist `pad_buffer_cells.cdl`, `cell_tree.md`, `README.md`, the Q&A files) and from
  A4's compaction code and rules (`inputs/A4/out/build_oa_p.py`, `inputs/A4/out/skill/generic/rules.md`,
  `inputs/A4/out/skill/ihp_sg13cmos5l/rules.md`). No second generator for what those cover. Keep code small: no "just in
  case" options, no script piled on script.
- Background commands die after 2 h; keep runs short. Kill processes by PID, never `pkill -f`.

## Christoph's layout rules of 2026-10-28 (binding)

- No substrate taps between rows of arrayed transistors; taps only at the periphery. Check LU.a (20 µm, layout rules
  §7.2.2) with periphery taps only; if a cell is too big for that, report the numbers instead of adding an inner tap.
- One NWell per rail, not separate wells. NWell polygonal where the rules allow.
- A tap ring is optional and needn't be rectangular. Tap-less cells with bulk from the parent are fine ("NO ntap rings",
  2026-10-27 08:45).
- Narrow dummies.
- Ratios that set the circuit stay as they are unless your report gives the reason: the mirror ratios, the
  common-centroid maps of `inputs/layout_primitives.md` §5 (tubs / tails `Aa C2b C1b Ba / Bb C1a C2a Ab`, loads
  `L R R L L R R L`).
- Exception to "one NWell per rail": each input device has bulk = source and needs its own NWell (`layout_primitives.md`
  §3 P1); keep one well per device, identical in every copy, with a butted source tie.

## Your cells (library → circuit)

Circuit: `inputs/circuit/d2s_mpdda_pd.spice` (subckt `d2s_mpdda_pd`), `units.spice` (`unit_r2`: tails XTa / XTb 5/6,
input devices XMa / XMb 2 × 10/1, bulk = source), `d2s_mpdda_pd.sch`, `unit_r2.sch`. Nets: `layout_primitives.md` §5
and the library's notes (63/0 texts in `d2s_inputs`).

| library cell | devices | circuit |
|---|---|---|
| `d2s_inputs` / `tub_p20x1` (+ `tub_p20x1_dummy`) | 8 input devices hv PMOS 2 × 10/1 in their own wells, dummy tubs | XMa / XMb of XA, XB, XC1, XC2 |
| `d2s_tails` | 8 tails hv PMOS 5/6, BP at an end, dummies; gate vbp | XTa / XTb of the 4 units; BP (`bias_tree_pd`'s diode, moved into the row, `layout_primitives.md` §3 P2, P8) |
| `d2s_loads` | PL / PR hv PMOS 6/4, 2 × 4 fingers `L R R L L R R L` | XPL, XPR |
| `d2s_casc_p` | PCL / PCR 15/3 (lcas = 3), BPC (1/4) on the same gate line | XPCL, XPCR, BPC |
| `d2s_ab_p` | RP2, FPL, ABP single 6.66/0.6 fingers (RP1 is in the clamp frame now; drop the fall-back copy) | XRP2, XFPL, XABP |
| `d2s_pd_p` | the power-down switches XSA, XSABP (hv PMOS 1/0.45) | XSA, XSABP |

The tail row and the tub array share the column map, each tail directly above its tub (`layout_primitives.md` §2).

## F's requests (relayed by the lead)

F's requests of 16:58 CET, verbatim (F's floorplan picture and notes: `inputs/F_floorplan_stage1.png`, `inputs/F_floorplan_stage1.md`; variant 1 is the one being built). Where they and the rest of this brief differ, F's requests win on outline, orientation and pins; the rules above win on devices, ratios and rule values.

### Conventions for every cell

- **Orientation.** Draw each cell **as placed**: "upright" means the long side vertical. Edges are named as
  placed: bottom = towards the output frame (y 84), top = towards the core pins (y 180).
- **Outline.** The outline is the bounding box of all shapes, including NWell, ThickGateOx and pSD. I add the
  spacing between cells:
  - NW.b1 1.80 between wells on different nets;
  - NW.d1 / NW.f1 0.62 between a well and N+ or P+ of another cell;
  - iovdd wells are merged.
  The maxima below already leave room for that. Smaller is welcome. If a maximum is not reachable, tell me the
  size you get, and do not change the aspect: I move blocks, I don't squeeze them.
- **Pins.** Metal1.pin 8/2 + text 8/25, Metal2.pin 10/2 + text 10/25, as in the library.
  - Pins lie on the outline edge, inside it. The library's M2 stubs outside the cell (x −1.61) are not wanted.
  - Width ≥ 0.29 (one Via1 with M2.c1 endcaps).
  - Per pin, give the side, the layer and the position measured from the cell's lower-left corner.
- **Layers.** Metal1 / Metal2 only, and nothing on Via2 or above. Metal2 runs over your cells: tell me any part
  of the cell where I may not route Metal2 (matched arrays).
- **Ties and rings.**
  - No rings, and no tie between rows of one array (Christoph's rule 2).
  - Each cell must pass LU.a / LU.b on its own, with tie strips at the outline edges named below. If you would
    rather leave a tie to me, name the segment you need, as A4 did for oa_pmir_c.
  - I draw: the guard rings, the NWell isolator above the frame, the edge stubs, the NWell bridges between
    cells, and every Via2 / supply tap.
- **NWell.** In the iovdd PMOS cells (tails, loads, casc_p, ab_p, pd_p), take the NWell and ThickGateOx to the
  outline on the edges marked "merge"; I bridge the wells into one iovdd NWell.
- **Supply pin names** as in `d2s_mpdda_pd`:
  - `vdd` / `vss` for the front end (iovdd / iovss at the pad top);
  - `vddo` / `vsso` for the output-side pull-downs SA / SB, each with its own tap to the ring (`layout_primitives.md`
    §6).
- **Source buses.** The tails' and the sinks' source buses (with BP / BN) each tap the ring at **one** point.
  Give that bus as one Metal1 net and mark the tap point (a 0.6 × 0.6 Metal1 pad on the outline). I put the Via
  stack there.
- **Devices.** Keep the maps of `layout_primitives.md` §5 and the ratios. Narrow dummies are welcome. Every
  dummy is a device in your CDL. Report every finger / ng change as a netlist change.
- **Not in your cells** (I draw them, or they are elsewhere):
  - RP1 / RN1 (they are in the clamp frames);
  - rhigh, bias_tree_pd, CMA / CMB, rings, stubs.
  - The bias diodes stay where the library has them: BP in the tails, BPC in casc_p, BN in the sinks, BNC in
    casc_n.

### P (PMOS)

| cell | max outline W × H (as placed) | position (variant 1) |
|---|---|---|
| d2s_inputs (tub_p20x1 ×8 + dummies) | **34.0 × 27.0** | x 19.5–53.5, y 125.0–152.0 |
| d2s_tails (8 tails + BP + dummies) | **34.0 × 15.0** | x 19.5–53.5, y 108.2–123.2 |
| d2s_loads (PL / PR 2 × 4 + dummies), upright | **15.2 × 33.0** | x 2.5–17.7, y 123.2–156.2 |
| d2s_casc_p (PCL / PCR 2 × 2 × 15/3 + BPC + dummy), upright | **12.5 × 34.0** | x 2.5–15.0, y 88.6–122.6 |
| d2s_ab_p (RP2, FPL, ABP; no RP1) | **7.8 × 9.5** | x 39.6–47.4, y 88.6–98.1 |
| d2s_pd_p (SA, SABP) | **4.0 × 3.0** | x 47.9–51.9, y 88.6–91.6 |

**d2s_inputs**
- Wire it completely; the library cell has the tubs only.
- Tubs and tails share one column pitch, so each tail sits straight below its tub (§2, §5).
- Well = source for each tub (butted ties); the dummy tubs are on `vdd`. The wells stay ≥ NW.b1 inside the cell.
- Pins:
  - **top edge, M2:** `vinp`, `vref`, `vinn`, left to right, ≥ 2 µm apart;
  - **left edge, M2:** `vfb` (gates of C1b, C2b), in the lowest 3 µm. It arrives from the left over an M3 hop in the
    gap at y 119–126, and is the pad's Kelvin line;
  - **right edge, M2:** `x`, `y` (towards the sinks), within 13 µm of the bottom;
  - **bottom edge, M2:** `sa_A … sb_C2` (8), each at its tub's column;
  - **bottom edge, M1:** `vdd` (dummies).
- Tub shape: free inside the outline. ng = 4 × 5/1 instead of 2 × 10/1 is allowed if it saves height; report it as
  a netlist change.

**d2s_tails**
- NWell: merge on the left, right and bottom edges. The top edge faces the tubs' wells: NW.b1 is mine, so take the
  well to the outline there too.
- Pins:
  - **top edge, M2:** `sa_*` / `sb_*` (8) at the tub columns;
  - **bottom edge, M2:** the same 8 nets again (towards d2s_rhigh through my channel at y 104.7–107.9), either as
    through-columns or as separate pins;
  - **right edge, M2:** `vbp` (gates + BP), low;
  - **bottom edge, M1:** `vdd`, the source bus with BP, with its single tap pad at the bottom-left corner, under the
    M3 iovdd rail.

**d2s_loads** (upright; e.g. two columns of 5, ABBA as §5)
- NWell: merge on all edges except the right edge, which faces the tub wells (NW.b1 mine).
- Pins:
  - **bottom edge, M2:** `pl`, `pr`, `l2`, matching casc_p's top pins;
  - **left edge, M1:** `vdd` (sources + n tie strip).

**d2s_casc_p** (upright)
- NWell: merge on all edges.
- Pins:
  - **top edge, M2:** `pl`, `pr`, `l2`;
  - **bottom edge:** `a` on **M1** (it drops under the b join onto the a join at y 86.4–87.0), and `l2` on M2 near the
    right corner;
  - **right edge, M2:** `vbpc` (gates + BPC), within 3 µm of the bottom;
  - **left edge, M1:** `vdd` (BPC source, n tie strip).

**d2s_ab_p**
- Gates on `vabp`; RP2 is a diode with its source on `dabp`. Bulk is `vdd`, with no source on vdd.
- NWell: merge on the top edge (a bridge up to the tails) and on the right edge (pd_p).
- Pins:
  - **bottom edge:** `a` on **M1**, `b` on M2, and `dabp` on **M1** at the left end (it drops to the existing pin at
    x 38.94–39.55, y 85–86);
  - **top edge, M2:** `vabp`, `l1`, `l2`;
  - **left edge, M1:** `vdd` (n tie).

**d2s_pd_p**
- **Split the sources:** SA's source is `vddo`, SABP's source is `vdd`, as two separate pins. The library cell
  shares one diffusion between them.
- NWell: merge on the left edge.
- Pins:
  - **bottom edge, M1:** `a`, `vddo`;
  - **top edge, M1/M2:** `en_3v3`, `vabp`, `vdd`.
- You may merge pd_p into ab_p as one cell (≤ 12.3 × 9.5) if that is smaller; keep the pins.

### What I need back with each cell

- GDS + CDL.
- Outline, and the NWell / TGO / tie positions on each edge.
- Pin table with coordinates.
- DRC (run_drc incl. LU) and LVS results.
- Netlist changes.

## Checks and deliverables (`out/`)

- `d2s_p_cells.gds` with your cells (names: the library name with `_c`, e.g. `d2s_tails_c`), each standalone-checkable;
  `d2s_p_cells.cdl` with one `.subckt` per cell (devices as drawn, dummies included); `build_d2s_p.py` (re-runnable,
  reads `inputs/pad_buffer_klayout/pad_buffer_cells.gds` for the device cells).
- DRC per cell: `python3 /foss/pdks/ihp-sg13cmos5l/libs.tech/klayout/tech/drc/run_drc.py --path=<gds> --topcell=<cell>
  --no_density --mp=4 --run_dir=<dir>` (main tables with the latch-up table LU.b, plus the maximal deck with LU.a / c /
  c1 / d / d1). Grep its log for "generated an exception": the runner prints "Passed" even when a table crashes.
  0 violations per cell, or a list of what remains and why.
- LVS per cell: `python3 /foss/pdks/ihp-sg13cmos5l/libs.tech/klayout/tech/lvs/run_lvs.py --layout=<gds> --netlist=<cdl>
  --topcell=<cell> --run_dir=<dir> --disable_tap_extraction` (add `--implicit_nets=<nets>` only where a same-named pin
  pair is joined by the parent, and say so).
- One PNG per cell.
- Each check runs once, and once more after each fix. A cell not clean after three rounds is reported and left.
- `report.md` (under ~100 lines): per cell the size before / after (library bboxes: `d2s_inputs` 34.80 × 28.80,
  `d2s_tails` 35.29 × 21.76, `d2s_loads` 58.29 × 9.10, `d2s_casc_p` 36.64 × 13.58, `d2s_ab_p` 10.04 × 9.66, `d2s_pd_p`
  3.20 × 2.24 µm), device-to-finger map, tap / well scheme with the LU numbers, the netlist changes the cell implies
  (every w / l / ng / dummy change and its electrical effect, for the backannotation), pin list with coordinates.
- When done, reply with a five-line summary and the file list with sha256 (first 12 hex). Do not report success that
  you have not checked.
