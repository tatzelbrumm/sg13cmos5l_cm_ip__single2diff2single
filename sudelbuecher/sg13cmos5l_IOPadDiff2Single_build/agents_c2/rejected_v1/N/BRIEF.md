# Brief N: compact NMOS primitives of `d2s_mpdda_pd` for the IOPadDiff2Single pad cell (IHP sg13cmos5l), C2 2026-10-31

Workspace (yours only): `/home/user/c2/N/` — `inputs/` read-only, `work/` scratch, `out/` deliverables.
You are the NMOS specialist (as A3 on 2026-10-28: `inputs/A3/BRIEF.md`, `report.md`, `out/` with its generator and
`out/skill/`). A second agent (P) does the PMOS cells; a third (F) assembles the pad cell's amplifier block from your
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
  A3's compaction code and rules (`inputs/A3/out/build_oa_n.py`, `inputs/A3/out/skill/generic/rules.md`,
  `inputs/A3/out/skill/ihp_sg13cmos5l/rules.md`; A3's bandgap block `bg_n4` in `inputs/A3/report_bg*.md`). No second generator for what those cover. Keep code small: no "just in
  case" options, no script piled on script.
- Background commands die after 2 h; keep runs short. Kill processes by PID, never `pkill -f`.

## Christoph's layout rules of 2026-10-28 (binding)

- No substrate taps between rows of arrayed transistors; taps only at the periphery. Check LU.b (20 µm, layout rules
  §7.2.2: N+Activ to a substrate tie) with periphery taps only; if a cell is too big for that, report the numbers instead of adding an inner tap.
- One NWell per rail, not separate wells (your cells have none; bulk = substrate = iovss).
- A tap ring is optional and needn't be rectangular. Tap-less cells with bulk from the parent are fine ("NO ntap rings",
  2026-10-27 08:45).
- Narrow dummies.
- Ratios that set the circuit stay as they are unless your report gives the reason: the mirror ratios, the
  common-centroid maps of `inputs/layout_primitives.md` §5 (sinks `X Y Y X X Y / Y X X Y Y X`, BN and a dummy at the
  ends).
- The sinks dominate the offset budget (5.4 of 6.1 mV, `layout_primitives.md` §1, §3 P4): keep their finger count a
  parameter (the 4× option is a parameter change), and the source bus with BN tapped to iovss at one point (§6).

## Your cells (library → circuit)

Circuit: `inputs/circuit/d2s_mpdda_pd.spice` (subckt `d2s_mpdda_pd`), `d2s_mpdda_pd.sch`.

| library cell | devices | circuit |
|---|---|---|
| `sinks_6x6` | SX / SY 6 + 6 fingers hv NMOS 6/6 `X Y Y X X Y / Y X X Y Y X`, BN at an end, dummies; gate vbn | XSX, XSY (drawn 6 × 6/6; the sheet still says w=36u ng=4: a netlist change, `layout_primitives.md` §7 decision 1), BN (`bias_tree_pd`'s diode, moved into the row, §3 P4, P8) |
| `d2s_casc_n` | CX / CY 15/3 (lcas = 3), 2 fingers each, BNC (1/8) on the same gate line | XCX, XCY, BNC |
| `d2s_ab_n` | RN2, FNL, ABN single 4.4/1 fingers (RN1 is in the clamp frame now; drop the fall-back copy) | XRN2, XFNL, XABN |
| `d2s_pd_n` | the power-down switches XSB, XSABN (hv NMOS 1/0.45) | XSB, XSABN |

`sinks_6x6` is shared with the s2d pad (`s2d_mpdda`): keep a variant of it for s2d (same finger, same map rules), even
if the d2s copy changes shape for F.

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

### N (NMOS)

| cell | max outline W × H (as placed) | position (variant 1) |
|---|---|---|
| sinks_6x6 (SX / SY 6 + 6 × 6/6, BN, dummies), **upright** | **18.0 × 53.5** (wanted ≤ 17.5 × 52) | x 59.5–77.5, y 123.5–177.0 |
| d2s_casc_n (CX / CY 2 × 2 × 15/3 + BNC), upright | **11.0 × 34.0** | x 66.5–77.5, y 88.6–122.6 |
| d2s_ab_n (RN2, FNL, ABN; no RN1) | **7.5 × 9.5** | x 31.6–39.1, y 88.6–98.1 |
| d2s_pd_n (SB, SABN) | **3.5 × 2.5** | x 52.6–56.1, y 88.6–91.1 |

**sinks_6x6** (upright: the two library rows become two columns; the map `X Y Y X X Y / Y X X Y Y X` with BN and the
dummy at the ends is unchanged)
- Ties: strips on the long edges only, none between the columns. With an 18 µm width, one strip on the right edge
  meets LU.b (20 µm).
- Pins:
  - **bottom edge, M2:** `x`, `y` (to casc_n just below) and `vbn` (gates + BN; the tree is below-left);
  - **left edge, M2:** `x`, `y` again (towards the tubs), within 2–28 µm of the bottom;
  - **right edge, M1:** `vss`, the source bus with BN, with its single tap pad at 4–8 µm above the bottom (that is
    y 127.5–131.5, under the M3 iovss rail at 126–134).
- For variant 2 I place the same cell rotated R90 (left → bottom, bottom → right). You need not do anything for it.
- The cell is shared with s2d. If you would rather keep it native, deliver it native with the pins on the native
  bottom (= my left) and native right (= my bottom) edges; I rotate.

**d2s_casc_n** (upright)
- Pins:
  - **bottom edge, M2:** `b` (straight down onto the b join at y 87.4–88.0), and `l1` near the left corner;
  - **top edge, M2:** `x`, `y`, matching the sinks' bottom pins;
  - **left edge, M2:** `vbnc` (gates + BNC);
  - **right edge, M1:** `vss` (BNC source, p tie strip).

**d2s_ab_n**
- Gates on `vabn`; RN2 is a diode with its source on `dabn`. Bulk is `vss`.
- Its right outline edge faces ab_p's NWell: keep N+ Activ ≥ 0.62 inside that edge, or tell me the margin.
- Pins:
  - **bottom edge:** `a` on **M1**, `b` on M2, and `dabn` on **M1** at the right end (it drops to the existing pin at
    x 38.15–38.45, y 85–86);
  - **top edge, M2:** `vabn`, `l1`, `l2`;
  - **left edge, M1:** `vss` (p tie).

**d2s_pd_n**
- **Split the sources:** SB's source is `vsso`, SABN's source is `vss`.
- Pins:
  - **bottom edge, M1:** `b`, `vsso`;
  - **top edge, M1/M2:** `en_3v3_b`, `vabn`, `vss`.
- You may merge it into ab_n (≤ 11 × 9.5).

### What I need back with each cell

- GDS + CDL.
- Outline, and the NWell / TGO / tie positions on each edge.
- Pin table with coordinates.
- DRC (run_drc incl. LU) and LVS results.
- Netlist changes.

## Checks and deliverables (`out/`)

- `d2s_n_cells.gds` with your cells (names: the library name with `_c`, e.g. `sinks_6x6_c`), each standalone-checkable;
  `d2s_n_cells.cdl` with one `.subckt` per cell (devices as drawn, dummies included); `build_d2s_n.py` (re-runnable,
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
- `report.md` (under ~100 lines): per cell the size before / after (library bboxes: `sinks_6x6` 53.37 × 18.12,
  `d2s_casc_n` 36.12 × 11.94, `d2s_ab_n` 11.34 × 7.01, `d2s_pd_n` 2.50 × 2.04 µm), device-to-finger map, tap / well scheme with the LU numbers, the netlist changes the cell implies
  (every w / l / ng / dummy change and its electrical effect, for the backannotation), pin list with coordinates.
- When done, reply with a five-line summary and the file list with sha256 (first 12 hex). Do not report success that
  you have not checked.
