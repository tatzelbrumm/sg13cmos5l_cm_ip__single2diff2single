# Brief F: floorplan and assembly of the `sg13cmos5l_IOPadDiff2Single` pad cell's amplifier block (C2, 2026-10-31)

Workspace (yours only): `/home/user/c2/F/` — `inputs/` read-only, `work/` scratch, `out/` deliverables. Called `$F`.
You are agent F (as A2 on 2026-10-28: `inputs/notes/agents/A2/`). Two primitive agents, P (PMOS) and N (NMOS), draw
the compact d2s primitives in parallel; the lead relays between you and them, checks every cell before you get it, and
integrates your result into the macro. Agent K investigates other capacitor types for CMA / CMB; the lead relays its
stages to you.

## Goal

The drawn pad cell `sg13cmos5l_IOPadDiff2Single` (80 × 180 µm, IHP sg13cmos5l IO ring): the amplifier `d2s_mpdda_pd`
and the bias tree `bias_tree_pd` in y 84–178, assembled from P's and N's compact cells and your own cells, wired to the
output stage that is already drawn in y 0–88 (clamp frames, DCN / DCP diodes, CMA / CMB, Metal2 combs, by A1 on
2026-10-28: `inputs/notes/m2_option_b_2026-10-28/report.md`).

## Work in stages (reply at the end of stage 1 and wait; the lead resumes you)

**Stage 1 — floorplan and requests (short; reply when done).**
- Read: `inputs/notes/C2_phase1_report.md` (the lead's phase 1: edge contract, partition, ports, budget),
  `inputs/notes/layout_primitives.md` §1–6, `inputs/notes/pad_buffer_klayout/README.md` and `cell_tree.md`,
  `inputs/notes/m2_option_b_2026-10-28/report.md`, A2's reports, and the circuit (below).
- At most two floorplan variants. For each block: outline, position, orientation, and the nets between blocks; the
  routing plan (M1 / M2; M3 only at y 119–126 and 134–140); where the band stubs, guard rings and ties go; where the
  six core-side pins go.
- Write `out/requests_for_P_N.md`: per cell of P and of N (lists below) the outline you want (maximum width × height),
  orientation, pin names, layer, side and position, the shapes at the cell edge you need (well edges, ties to share),
  and anything to leave out because you draw it (e.g. a ring). Write `out/floorplan_stage1.md` and a picture.
- Reply with a summary of no more than 15 lines.

**Stage 2 — your own cells, while P and N work** (after the lead resumes you):
- `d2s_rhigh`: the 4 × 150 kΩ unit resistors as rhigh chains, the way `bg_res_c` is drawn
  (`inputs/notes/bg_core_pd_2026-10-28/build_bg_res_c.py`, `bg_res_c.gds`), map of `layout_primitives.md` §5.
- CMA / CMB units (`d2s_cma` / `d2s_cmb`): hv PMOS MOS capacitors as in the sheet, with K's latest stage as the lead
  relays it. Without a result from K, lay them out as in the sheet, as hv PMOS units, each capacitor in its own region,
  so that a later change of type stays local. Each may be split into units of any shape and placed partly in y 0–84
  next to the output devices and clamps, where the frames leave room (high priority), partly above. Total gate area
  stays 7.96 × 32.16 = 256 µm² each; report the series channel resistance of the split (∝ L / W per unit, units in
  parallel) as a circuit effect.
- Guard rings and band ties (section "ESD and latch-up" below), and the edge stubs of phase 1.
- `bias_tree_pd`, drawn to its present sheet (`inputs/repo/macros/bias_tree_pd/schematic/xschem/bias_tree_pd.sch`,
  subckt `bias_tree_pd` in `netlist/source/bias_ref_pd.spice`), from the library primitives `bias_tree_n`, `bias_tree_p`,
  `bias_tree_sw`, `bias_tree_swp` in `inputs/repo/macros/IOPad/layout/klayout/pad_buffer_cells.gds` (compact them as
  you see fit; that macro's sheet is not changed).

**Stage 3 — assembly** (after the lead passes you P's and N's checked cells): place, route in M1 / M2 (M3 in the gaps),
pins. You may change copies of P's and N's cells if that makes the cell more compact; list every change.

## Circuit (read-only, in `inputs/repo/macros/sg13cmos5l_IOPadDiff2Single/`)

- `netlist/source/sg13cmos5l_IOPadDiff2Single.spice`, `d2s_mpdda_pd.spice`, `d2s_out.spice`, `units.spice` (`unit_r2`);
  sheets `schematic/xschem/*.sch`; `README.md`.
- The cell after the partition (phase 1 report §1.7): in the cell Xd, Xt, Xfp / Xfn, XCMA / XCMB, XDN / XDP; out
  (to the slot) Xg (`bias_gen_pd`) and Xc (`en_ctrl_3v3`). Ports: `iovdd iovss vdd vss pad vinp vinn vref iref en_3v3
  en_3v3_b`. Core-side pins on Metal2 at the top edge: `vinp vinn vref iref en_3v3 en_3v3_b`.
- `vfb` of Xd is the pad, Kelvin: a separate line from the pad junction, not sharing the output current's path.
- `vddo` / `vsso` (the output stage's sources) get their own taps to the ring and never share a bus with the front end
  (`layout_primitives.md` §6). The tail row's source bus taps iovdd at one point; the sink row's taps iovss at one point.
- Pad cell as drawn: `layout/klayout/sg13cmos5l_IOPadDiff2Single.klay.gds`. Connections waiting above the P frame:
  `a` join (M2, y 86.4–87.0), `b` join (M2, y 87.4–88.0), `dabp` / `dabn` pins (M2, y 85–86, x ≈ 38.2–39.6),
  `pad` lines. Open point of 2026-10-28: M2 from above can't reach `dabp`, `dabn` or `pad` without an M1 hop under the
  joins; you may redraw the static cells `gate_feeds`, `replica_lines`, `m2_comb_*`, `m2_junction`, `cap_cma`, `cap_cmb`
  of the pad top (list every change). The PCell instances (clamps, diodes) and `TopLayersTo4` / `Metal3ViasUp` /
  `contacts` stay; clamp / diode changes are changes to `scripts/pcells` with its tests, which you don't do (propose them).

## Rules (Christoph's, binding)

1. **Existing code first.** The primitives come from P / N (copies of `pad_buffer_cells`), the compaction code and
   rules from `inputs/notes/agents/A3/skill/` and `A4/skill/` (`generic/rules.md`, `ihp_sg13cmos5l/rules.md`), the router
   from `generator.py` in `inputs/notes/oa_core_pd_v2_2026-10-28/v2/` and `inputs/notes/bg_core_pd_2026-10-28/`. A2's
   scratch scripts carry cloud paths of 2026-10-28; point them at your copies. Keep code small: no "just in case"
   options, no script piled on script.
2. **The layout drives the design**, 2026-10-28: no substrate taps between rows of arrayed transistors; one NWell per
   rail, not separate wells; a tap ring is optional and needn't be rectangular; NWell polygonal where the rules allow;
   narrow dummies. Ratios that set the circuit stay unless you give the reason: I_Q ratio OP : RP1 = 82 : 2, the mirror
   ratios, the common-centroid maps of `layout_primitives.md` §5.
3. **Rule values only from the PDK's decks and documents**, each cited with file and rule name:
   `/foss/pdks/ihp-sg13cmos5l/libs.tech/klayout/tech/drc/rule_decks/*` (incl. `sg13cmos5l_tech_default.json`),
   `libs.doc/doc/SG13CMOS5L_os_layout_rules.pdf` (text: `inputs/notes/SG13CMOS5L_os_layout_rules.txt`),
   `SG13CMOS5L_os_process_spec.pdf` §3.5 (text: `inputs/notes/SG13CMOS5L_os_process_spec.txt`).
4. **Shared macros unchanged**: `bias_tree_pd`, `bias_gen_pd`, `en_ctrl_3v3`, `ls_*`, `hv_logic`, the cores. A shared
   block laid out here is drawn to its present sheet; if its layout implies a sheet change, write it as a proposal.
5. Measured facts as facts; reasoning and guesses marked. Times: `TZ=Europe/Berlin date`.

## ESD and latch-up (the brief of the session, condensed)

- Guard ring around every device tied to the pad, CMA included (its NWell is the pad net; its missing ring is an open
  point). Double guard rings (NWell isolator and P+ isolator) between the n- and p-channel output devices, and between
  them and the circuitry. LU.a / LU.b 20 µm, LU.c / LU.d 6 µm (layout rules §7.2.1 / §7.2.2).
- `guard` (the NWell rings of the N frames and of DCNDiode) is not tied inside the cell today (open point): tie it to
  iovdd.
- CMB has its gate on the pad (`XCMB b pad b b`): lay it out as in the sheet until Christoph decides. Check antenna
  rules §7.1 for every gate on the pad net (CMB, the vfb input gates).
- Edge contract (phase 1 report §1.2): at both cell edges the layers Activ, Metal1, pSD, NWell, Substrate must show
  IOPadAnalog's y intervals (bands NWell n+ iovdd 6–61; p+ iovss 65–84.4 and 84.5–140; n+ in NWell iovdd 148.35–148.65;
  p+ vss 156.85–157.15 (in IHP Metal1-only at the edge); n+ in NWell vdd 166.85–167.15), each tied there to its rail.
  Stubs at the edges suffice; the interior is yours. `inputs/notes/row_check.py <gds> <cell> <outdir>` checks it.
- Every pad / rail current path at least as wide as in IOPadAnalog (`inputs/notes/path_widths.py`, phase 1 §1.6).

## Checks (each once, and once more after each fix; a cell not clean after three rounds is reported and left)

- DRC: `python3 /foss/pdks/ihp-sg13cmos5l/libs.tech/klayout/tech/drc/run_drc.py --path=<gds> --topcell=<cell>
  --no_density --mp=4 --run_dir=<dir>` (main tables incl. `latchup` LU.b, plus the maximal deck with LU.a/c/c1/d/d1).
  Check its log for "generated an exception": the runner reports "Passed" even when tables crash.
- LVS: `python3 /foss/pdks/ihp-sg13cmos5l/libs.tech/klayout/tech/lvs/run_lvs.py --layout=<gds> --netlist=<cdl>
  --topcell=<cell> --run_dir=<dir> --disable_tap_extraction` against a reference netlist you write from the sheets
  (dummies as devices, devices as drawn).
- Extraction: count the nodes next to each rhigh segment that only capacitors touch (41 in `bg_core_pd`; LVS doesn't
  see them, a simulation goes singular); method: `inputs/notes/pex_for_sim.py`. Run a PEX in a copy of the repo
  (`cp -a inputs/repo work/repo`, `export PDK_ROOT=/foss/pdks; source .designinit`, put your GDS in the macro's layout,
  `make -C macros/sg13cmos5l_IOPadDiff2Single magic-pex EXT_MODE=2 SCRIPTS_DIR=../../scripts`; mode 3 is not
  reproducible).
- Row check (`row_check.py`) and path widths (`path_widths.py`) on your pad candidate.
- Background commands die after 2 h; keep runs short. Kill by PID, never `pkill -f`.

## Hard rules

- Work only in `$F`. No git (not even read-only), no web searches, no writes outside `$F`, `inputs/` untouched, no
  `mcp__*` tools.

## Deliverables in `$F/out/` (stage 3)

- `pad_candidate.gds`: the pad cell (top cell `sg13cmos5l_IOPadDiff2Single`) with your block and cells placed; the
  block also as its own cell (`d2s_block`, say) with its reference netlist; your cells (`d2s_rhigh`, `d2s_cma`,
  `d2s_cmb`, rings / ties, `bias_tree_pd`) each standalone-checkable; `*.cdl`; the build script(s), re-runnable.
- DRC / LVS / extraction / row-check logs; renders (whole cell and details).
- `netlist_changes.md`: every change the layout implies for the sheets and source netlists (finger counts and `ng` as
  drawn, rhigh chains as xschem vector instances, every dummy as a device, CMA / CMB as their units), for the lead's
  backannotation.
- `report.md` (under ~150 lines): five-line summary first; floorplan with coordinates; area per block; pins; routing
  layers; the open points of 2026-10-28 (a / b joins above the P frame, `guard` not tied, CMA's ring, rules at exactly
  their limit, the 63/0 GateDecode box), each closed or still open; the changes to P's / N's copies and to the pad
  top's static cells; deviations from this brief.
- When done, reply with the summary and the file list with sha256 (first 12 hex). Do not report success you have not
  checked.
