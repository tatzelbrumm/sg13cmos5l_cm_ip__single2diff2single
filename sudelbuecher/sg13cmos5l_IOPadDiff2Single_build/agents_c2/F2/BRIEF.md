<!--
SPDX-FileCopyrightText: 2026 Christoph Maier
SPDX-License-Identifier: Apache-2.0
-->
# Brief F2: assembly of the `sg13cmos5l_IOPadDiff2Single` amplifier block from the reviewed primitives (C2, 2026-11-03)

You are agent F2, the floorplan and assembly agent. You build the pad cell's amplifier block **bottom-up** from the
compact primitives that Christoph reviewed, place it in the pad cell above the output stage, and deliver a pad candidate
with its checks. A lead session starts you, checks what you deliver, and does the integration into the macro.

Paths below are relative to two checkouts of the design repository
(`tatzelbrumm/sg13cmos5l_cm_ip__single2diff2single`): `$D` = branch `claude/c2-pad-layout` (design), `$N` = branch
`claude/c2-pad-layout-sudel` (notes). The lead gives you their absolute paths and your workspace `$W` (with `work/` and
`out/`). Read-only: everything in `$D` and `$N`. Write only in `$W`.

## History you need (short)

- The first attempt (P / N on Sonnet, F on Opus, 2026-10-31) was rejected by Christoph: asymmetric rows and dummies,
  narrowed gate-contact poly, and a top-down floorplan that forced outlines on the primitive agents. Archived in
  `$N/sudelbuecher/sg13cmos5l_IOPadDiff2Single_build/agents_c2/rejected_v1/` (README with his words). Your predecessor
  F's work there (`rejected_v1/F/`: stage 1–3, `stage3/src/`, `report.md`) is reusable **for the pad-top parts** that
  were not criticized: CMA's guard ring, the `guard` tie to iovdd, the NWell isolator above the P frame, the edge stubs,
  the vfb Kelvin line, the a / b / dabp / dabn hops under the joins, the CMB-stage reserve analysis. Re-check each one.
  Its block assembly is not reusable (built from the rejected cells).
- The primitives were rebuilt by P2 / N2 (Opus) and passed the lead's checks (XOR against a rebuild, IHP DRC incl.
  latch-up, IHP LVS, device tables against the circuit, `sym_check.py` mirror symmetry). Christoph reviewed them on
  2026-11-02 / 03.

## Christoph's review of the primitives (verbatim; binding for you)

`$N/sudelbuecher/sg13cmos5l_IOPadDiff2Single_build/agents_c2/N2/out/d2s_n2_cells_human_review.txt`:

```
d2s_rhigh_c2 : in the completed layout, the substrate tap should become a ring, if space allows
sinks_6x6_c2 : why the metal1 poly contacts in the center? in the completed layout, the substrate tap should enclose the whole array, if space allows
d2s_pd_n_c2 : VERY BAD as layout primitive: substrate tap too long, b, vabn metal1 stubs too long, vsso shouldn't be metal2 for the primitive. passable if F completely overworks this primitive.
d2s_casc_n_c2 : looks decent, in context substrate tap should become a ring if space allows.
d2s_ab_n_c2 : may already be integrated in F layout, F should overwork this primitive.
d2s_n2_cells_c2 : TGN and TDN should be moved by F when assembling the entire circuit.
```

`$N/sudelbuecher/sg13cmos5l_IOPadDiff2Single_build/agents_c2/P2/out/d2s_p2_cells_human_review.txt`:

```
d2s_inputs_c2 : looks workable
bias_tree_p_c2 : looks workable if TGP is moved by F as pad layout requires
d2s_ab_p_c2 : looks workable if F revises well tap
d2s_casc_p_c2 : looks good as basis for F
d2s_p2_cells_c2 : looks good as basis for F
d2s_pd_p_c2 : looks workable for adaptation by F into pad layout context
d2s_tails_c2 : looks good as basis for F
```

What it means for you:
- **Rework completely:** `d2s_pd_n_c2` (short tap, short b / vabn stubs, vsso not on Metal2 inside the primitive), and
  `d2s_ab_n_c2` (may be merged into your layout).
- **Adapt in context:** `d2s_pd_p_c2`, `d2s_ab_p_c2` (revise the well tap); move TGP (bias_tree_p), TGN and TDN
  (bias_tree_n) where the pad layout needs them.
- **Taps as rings where space allows:** around `d2s_rhigh_c2`, `d2s_casc_n_c2`, and enclosing the whole `sinks_6x6_c2`.
- **Answer Christoph's question** in your report: why the sinks have Metal1 poly contacts in the centre (the columns
  beside BN / its twin), and whether they can go (keeping rule 2 below).
- **Use as they are:** `d2s_inputs_c2`, `d2s_tails_c2`, `d2s_casc_p_c2`, `d2s_loads_c2` (P2's notes: loads folded to
  two rows, BP at a row end with full twins in the other corners).
- Your changed copies get distinct names (`<cell>_f2`), each DRC clean and LVS-matched on its own; list every change.

## Layout rules (binding)

1. **Bottom-up.** Place the cells as drawn (rotate, mirror, regroup as needed) in the pad context; the floorplan follows
   the cells. No floorplan constraints go back to anyone.
2. **Symmetry and gate contacts** stay as P2 / N2 drew them in every copy you change: rows mirror-symmetric about the
   line dividing them, the same dummy at both ends of every row (or none), never dummies at one end only; gate contacts
   on poly as wide as the gate, no necked poly. Check every changed copy with `sym_check.py` (below).
3. Christoph's rules of 2026-10-28: no taps between rows of arrayed transistors; one NWell per rail (the input tubs
   keep their own wells); taps / rings optional and need not be rectangular; NWell polygonal where the rules allow.
4. **CMA and CMB stay separate**: each its own well, region and guard ring; never a shared well (Christoph,
   2026-10-31). CMB stays as in the sheet (gate on the pad) until Christoph decides; keep it local.
5. **CMB secondary-stage reserve** (Christoph: reserve it "as long as the bias tree fits comfortably"): room for rppd
   1 × 7.435 µm (≈ 2 kΩ) + `dantenna` 0.64 × 3.1 to the substrate + `dpantenna` 0.64 × 4.98 to iovdd, a short wide
   pad-side feed and a short line to CMB's gate, CMB's gate feed cuttable at one place. Not drawn. The bias tree first.
6. **Existing code first**: `scripts/pcells` (clamps, diodes; no changes there), the primitives, the router in
   `generator.py` of `$N/.../pad_buffer_layout/oa_core_pd_v2_2026-10-28/v2/` and `bg_core_pd_2026-10-28/`. Keep code
   small. Rule values only from the PDK decks / documents, cited with file and rule name.
7. **Style references** (what good looks like here): the assembled cores `$D/macros/oa_core_pd/layout/gds/oa_core_pd.gds`
   and `$D/macros/bg_core_pd/layout/gds/bg_core_pd.gds`, and their primitives in
   `$N/sudelbuecher/sg13cmos5l_IOPadDiff2Single_build/agents/A3_oa_nmos_primitives/out*/` and `A4_oa_pmos_primitives/out*/`
   (`oa_n10`, `oa_mcs_c`, `oa_pmir_c`, `bg_n4`, `bg_pmir_pcas_c`).

## The circuit and the pad context

- Netlists `$D/macros/sg13cmos5l_IOPadDiff2Single/netlist/source/*.spice` (`d2s_mpdda_pd`, `d2s_out`, `units`), the
  sheets in `schematic/xschem/`, `bias_tree_pd` in `$D/macros/bias_tree_pd/` (drawn to its present sheet; its four bias
  diodes sit in the tails, sinks and cascodes: check the tree alone against "sheet minus diodes", LVS the pad flat).
- Partition (phase 1 report §1.7, `$N/.../pad_buffer_layout/pad_cell_2026-10-31/report.md`): in the cell Xd, Xt, Xfp /
  Xfn, XCMA / XCMB, XDN / XDP; out Xg, Xc. Ports `iovdd iovss vdd vss pad vinp vinn vref iref en_3v3 en_3v3_b`; core-side
  pins `vinp vinn vref iref en_3v3 en_3v3_b` on Metal2 at the top edge.
- `vfb` = pad, Kelvin from the pad junction. `vddo` / `vsso` get their own taps; the tail and sink source buses tap the
  ring at one point each. SA / SB bulks are vdd / vss (decided 2026-10-31).
- Pad cell as drawn: `$D/macros/sg13cmos5l_IOPadDiff2Single/layout/klayout/sg13cmos5l_IOPadDiff2Single.klay.gds`
  (y 0–88: clamps, diodes, CMA / CMB, Metal2 combs, a / b joins at y 86.4–88.0). Ring rails: M3 / M4 everywhere, TM1 up to
  y 134; M3 free only at y 119–126 and 134–140; route in M1 / M2.
- Edge contract (phase 1 §1.2): at both edges Activ, Metal1, pSD, NWell, Substrate show IOPadAnalog's y intervals, each
  band tied to its rail. The 63/0 box in the top cell is TEXT.drawing and is deleted at integration.
- ESD (brief §ESD): guard ring around every pad-connected device; double guard rings between N / P output devices and
  towards the circuitry; LU.a / LU.b 20 µm; antenna rules for every gate on the pad net.

## Checks (each once, and once more after each fix; three rounds at most per cell, then report and leave it)

Scripts in `$N/sudelbuecher/design_considerations/pad_buffer_layout/pad_cell_2026-10-31/`: `sym_check.py`,
`row_check.py <gds> <cell> <outdir>`, `path_widths.py <gds> <cell> <y-list>`, `lead_check.py` (the lead's).
- DRC: `python3 $PDK_ROOT/ihp-sg13cmos5l/libs.tech/klayout/tech/drc/run_drc.py --path=<gds> --topcell=<cell> --no_density
  --mp=4 --run_dir=<dir>` — grep its log for "generated an exception" (it prints "Passed" even when tables crash).
- LVS: `.../lvs/run_lvs.py --layout=<gds> --netlist=<cdl> --topcell=<cell> --run_dir=<dir> --disable_tap_extraction`
  (`--run_mode=deep` for hierarchical cells such as `d2s_inputs_c2`).
- Extraction: count the capacitor-only nodes beside the rhigh segments (`pex_for_sim.py` method, magic PEX mode 2).
- Row check and path widths on the pad candidate; every path at least as wide as before (phase 1 §1.6).

## Work in two stages

**Stage A — placement (then stop and report).** Place the reviewed cells and your reworked copies in the pad context,
without routing. Deliver `out/previews/placement_A.png` (cells named, rails and gaps marked), the reworked cells
(`pd_n`, `ab_n`, moved TGN / TDN / TGP, tap rings), their DRC / LVS / sym_check, and a short note with the area per
block, the free area, and where the CMB-stage reserve would go. Reply with a summary of no more than 15 lines and wait:
Christoph reviews the placement.

**Stage B — routing and the pad candidate** (after the lead resumes you): route, pin, check, and deliver
`out/pad_candidate.gds` (top cell `sg13cmos5l_IOPadDiff2Single`), `out/cells/d2s_block.gds` + `.cdl`, the pad CDL,
re-runnable build scripts (`out/src/`), check logs, previews of the routed cell, `out/netlist_changes.md` (every change
the layout implies for the sheets and source netlists, for the backannotation), and `out/report.md` (under ~150 lines;
five-line summary first; the open points of 2026-10-28 each closed or open; every change to the primitives and to the
pad top's static cells).

## Hard rules

- Write only in `$W`. No git commands. No web searches. Facts measured vs. reasoning: say which. Times
  `TZ=Europe/Berlin date`. Background commands: keep each under 2 h, kill by PID, never `pkill -f`.
- If the harness refuses to let you write a report file, put its text in your reply.
