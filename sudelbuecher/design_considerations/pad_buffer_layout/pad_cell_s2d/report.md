<!--
SPDX-FileCopyrightText: 2026 Christoph Maier
SPDX-License-Identifier: Apache-2.0
-->
# C3: layout of the `sg13cmos5l_IOPadSingle2Diff` pad cell — report

Claude Code cloud session, brief `sudelbuecher/cloud_sessions/C3_s2d_pad_draft.md` (final; "(draft)" is part of its
name). Design branch `claude/c3-s2d-pad-layout` (from `toplevel` 8a72dd8), notes branch
`claude/c3-s2d-pad-layout-sudel` (from `sudel_buecher` 07e97f0, a fast-forward of the branch's start 659c173). Times
are `TZ=Europe/Berlin date`.

**Status (2026-11-03 19:05 CET): stopped after phase 1. The brief's stop condition is met.** Even compacted, `xa`
(`s2d_mpdda_pd`) does not fit the free core-side region of IOPadAnalog:
- its estimated compacted cells alone cover 96 % of the region, before any routing or spacing;
- at the density C2 achieved (0.68), it needs 1.41 times the region.

§1.4 lists the levers of `layout_primitives.md` §4 that would make it fit. Choosing them is Christoph's decision. No
agents were started. The design branch holds only the cleaned-out pad template (section after §1.4).

C2 is finished (its notes branch ends at 2d0fb2d, "verbatim chat log of cloud session C2"), so C3 did not run in
parallel with it (decision 1). C2's files and the shared macros are untouched.

## Phase 0: tools (18:54 CET)

`/foss/setup.log`: `APT_OK`, `PIP_OK`, `TOOLS_OK`, `PDK_OK`, `PDK_DANGLING_LINKS 1 (1 = README.md)`, `OSDI_OK`,
`CACE_OK`, `SETUP_DONE`; no `KLAYOUT_DEB_FAILED`. Because `PDK_DANGLING_LINKS` is 1, C2's PDK fix is in: `rule_decks/layers_def.drc`
resolves. The `run_drc.py` logs of this session contain no "exception" (§1.1).

| tool | version |
|---|---|
| klayout | 0.30.12 |
| magic | 8.3.685 |
| netgen | 1.5.324 |
| xschem | 3.4.8RC |
| ngspice | ngspice-47 |
| cace | 2.11.0 |
| PDK | `git -C /foss/pdks/IHP-Open-PDK rev-parse HEAD` = df4c5054ee8ca481c3eb873687274f28cdb50b1e (as C2) |
| machine | 4 cores, 15 GB RAM |

## Phase 1: frame, partition, budget

Scripts: C2's `../pad_cell_2026-10-31/row_check.py` (unchanged, run from there); `budget.py` (here). Results are in
`phase1/`. The row GDS is not committed: it is 9.2 MB, and `row_check.py` regenerates it in 3 s.

### 1.1 Frame from IOPadAnalog (measured on `libs.ref/sg13cmos5l_io/gds/sg13cmos5l_io.gds`)

Outline: prBoundary 189/4 0,0 – 80,180; geometry bbox −0.62,0 – 80.62,180 (C2 §1.1). Instances:

| instance | bbox (µm) | kept |
|---|---|---|
| `Clamp_N20N0D` (CN) | −0.62,5.38 – 80.62,16.52 | as is |
| `DCNDiode` (DN) | 21.19,15.28 – 58.81,30.10 | as is |
| `DCPDiode` (DP) | 21.63,51.24 – 58.37,65.18 | as is |
| `Clamp_P20N0D` (CP) | −0.18,64.82 – 80.18,84.44 | as is |
| `SecondaryProtection` (SP) | 51.53,139.99 – 59.39,149.27 | as is (the brief: IHP's protection as it is) |

IOPadAnalog's own shapes (merged, measured):
- y 0–84.4, full: NWell + n+ plate on iovdd (0–80 × 6–61, with holes for CN and DN), p+ / Substrate plate on iovss
  (0–80 × 51.42–84.26, with holes for DP and CP). **No free area in the ESD zone.** The gap between DN and DP is the
  iovdd n+ plate, not open substrate.
- y 84.51–139.92: p+ / Substrate plate on iovss, 0–80 wide, with two 1 µm slots (89.56–90.56, 114.62–115.62).
- Bands as C2 §1.2. The n+ band in NWell on iovdd at 146.37–148.65 leaves a hole around SP; the p+ band on vss is at
  156.85–157.15, the n+ band in NWell on vdd at 166.85–167.15.
- Metal2: one pad-net plate x 5–75, y 0–180, with 2.4 µm slots (y 3–179). It carries `pad` to the core side; IOPadAnalog has
  `pad` and `padres` as M2 pins at the top.

**Free core-side region** (reasoning from these and from C2's drawn cell):
- y 85.74–180, x 0.66–77.85, as F2's `d2s_block` in the C2 macro. Circuitry takes the place of the p+ plate. The
  double guard ring above the CP frame (NW isolator, C2: y 84.45–86.15) and the band edge stubs are C2's.
- minus SP with 1 µm around it (9.86 × 11.28 µm).
- That leaves **7165 µm²**.

The pad plate in M2 above y 84 is not needed for the s2d cell, because no core-side `pad` pin exists. One M2 strap
from the pad to SP's `pad` pin remains, and it crosses the region vertically: a routing obstacle, not an area cost.

**Row `Filler1000 | IOPadAnalog | IOPadAnalog | Filler200 | IOPadIOVdd | IOPadAnalog | Filler1000`.** IOPadAnalog
takes the pad cell's place, so this is the frame's starting point. It is the only thing that differs from C2's phase 1:
- `phase1/edges.md`: the pad cell's edges are IOPadAnalog's, the same on every layer, by construction.
- `phase1/nets.md`: every ring rail and every band is one net through the row, 0 failures. In C2 four bands failed,
  because its old cell lacked them.
- IHP's `sg13cmos5l_maximal.drc` with `-rd latchUpRules=true`, deep, 4 threads: 22 s, **0 items** in 271 categories;
  LU.a, LU.c, LU.c1, LU.d and LU.d1 each 0. Log `logs/claude/c3-s2d-pad-layout/phase1-row-maximal.out`.
- `run_drc.py --no_density --mp=4`: 34 s, "No DRC violations". 32 table logs, LU.b among them (`latchup` table), and
  no "exception" in any of them. Log `phase1-row-run_drc.out`, tables in `phase1/main_row/`.

The final cell has to keep this result once the p+ plate gives way to circuitry. C2 did that with edge stubs for the
bands and the NW isolator (C2 §1.2, §4.3). The same applies here, for phase 4.

### 1.2 Partition of `sg13cmos5l_IOPadSingle2Diff.sch`

| instance | cell | decision | reason |
|---|---|---|---|
| `xa` | `s2d_mpdda_pd` | in (the brief) | does not fit (§1.3) |
| `CP` `CN` `DN` `DP` `SP` | IHP's `Clamp_P20N0D`, `Clamp_N20N0D`, `DCNDiode`, `DCPDiode`, `SecondaryProtection` | in, as placed in IOPadAnalog | the brief |
| `xt` | `bias_tree_noab_pd` | in, if it fits | fits only after all levers of §1.4 and a density above C2's |
| `s2d_cload` (XCLP / XCLN in `s2d_mpdda`) | 2 × hv NMOS 12 × 12 | decision 2: in while unclear | It is clear now that `xa` does not fit with them, and they are §4's lever 3: out to the slot under decision 2, once the levers are chosen |
| `xg` | `bias_gen_pd` | out, to the slot | the brief |
| `xc` | `en_ctrl_3v3` | out, to the slot | the brief; no layout or primitives of it exist (C2 §1.7) |

**Ports follow the layout** (decision 4, C2's option B). With `xt` in, the cell would be:

```
.subckt sg13cmos5l_IOPadSingle2Diff iovdd iovss vdd vss pad outp outn vcm vref iref en_3v3 en_3v3_b
Xt iovdd iovss iref vbp vbn vbpc vbnc en_3v3 en_3v3_b bias_tree_noab_pd
Xa iovdd iovss padres vref vcm outp outn outp outn vbp vbn vbpc vbnc en_3v3 en_3v3_b s2d_mpdda_pd
XCP iovdd iovss pad sg13cmos5l_Clamp_P20N0D
XCN iovss pad sg13cmos5l_Clamp_N20N0D
XDN iovss pad iovdd sg13cmos5l_DCNDiode
XDP pad iovdd iovss sg13cmos5l_DCPDiode
XSP padres iovss pad iovdd sg13cmos5l_SecondaryProtection
.ends
```

Gone from the cell: `ibias`, `en_1v2`, `sel0_1v2`, `sel1_1v2`, `vdd1v2_sense`, `vdd3v3_sense`. New: `iref`
(sourced by `bias_gen_pd` in the slot), and `en_3v3` / `en_3v3_b` from `en_ctrl_3v3`. Seven core-side pins
(`outp outn vcm vref iref en_3v3 en_3v3_b`), against C2's six. If `xt` has to leave, `iref` is replaced by four bias
voltages `vbp vbn vbpc vbnc` from the slot. That breaks the rule of `s2d_bias.spice` that bias crosses between blocks
only as currents.

What C2 decided at 15:50–17:30, and where the s2d cell differs (reasoning; tested only in phase 4):
- **Option B:** the same. One difference in scope: the symbol is used by `macros/slot/schematic/xschem/slot.sch`
  (`xs2d`), by the project top `schematic/xschem/sg13cmos5l_cm_ip__single2diff2single.sch` and by the 7 pad templates
  in `verification/cace/templates/`. C3's design branch covers only `macros/sg13cmos5l_IOPadSingle2Diff/`. C2
  already changed `slot.sch` and the top sheet on its branch, and C3 may not touch C2's files or shared macros. In
  phase 4, Xc / Xg move next to `xs2d` in `slot.sch` and in the top sheet, after C2 is merged into `toplevel` and with
  Christoph's go.
- **vss / iovss tie 2(a), the accepted magic vss pin mismatch:** expected to be the same. The cell keeps
  IOPadAnalog's vss p+ band, which shares the substrate with the iovss ties. C2 found that the chip harness already
  shows this merge for IHP's IOPadAnalog.
- **LVS of IHP's protection cells** (new for C3: C2 used its own PCells): IHP's CDL describes the clamps as
  hv NMOS / PMOS with `GuardRing_*` subcells and `XRoff … sub! rppd`
  (`sudelbuecher/sg13cmos5l_IOPadAnalog/sg13cmos5l_IOPadAnalog_real_hierarchy.spi`). Whether IHP's KLayout LVS
  matches IOPadAnalog against that CDL was not tested. Phase 4 tests it first, on IOPadAnalog alone.

### 1.3 Budget (`budget.py`, output `phase1/budget.md`; estimates, marked as such)

Each estimate is the library bbox (`pad_buffer_cells.gds`) times the compaction ratio that C2's reviewed rebuild
(P2 / N2) measured on the d2s counterpart. These are measured ratios, not assumed factors. The rebuild grew some cells:
symmetric dummies and rings cost area (inputs 1.08, NMOS cascodes 1.17).

| block | library µm² | ratio from (C2 P2 / N2) | ratio | estimate µm² |
|---|---:|---|---:|---:|
| s2d_inputs (12 tubs + dummies) | 1354 | d2s_inputs | 1.08 | 1461 |
| s2d_tails | 1088 | d2s_tails | 0.67 | 728 |
| s2d_loads | 722 | d2s_loads | 0.79 | 571 |
| s2d_casc_p | 726 | d2s_casc_p | 0.98 | 712 |
| s2d_casc_n | 1011 | d2s_casc_n | 1.17 | 1184 |
| sinks_6x6 (N2's `sinks_6x6_s2d_c2`, drawn) | 967 | itself | 0.88 | 853 |
| s2d_sinks_cmfb | 596 | sinks_6x6 | 0.88 | 525 |
| s2d_rhigh | 402 | d2s_rhigh | 0.92 | 371 |
| s2d_pd_p × 2, s2d_pd_n × 2 | 24 | d2s_pd_p / _n | 1.5 / 2.7 | 50 |
| s2d_cload | 387 | none (gate area fixed) | 1.00 | 387 |
| **xa** | 7277 | | | **6842** |
| bias_tree_n + bias_tree_p (d2s tree, an upper bound for noab) | 524 | bias_tree_n / _p | 0.85 / 0.78 | 429 |

C2's achieved density, measured on F2's `d2s_block` (C2 notes branch): 4929 µm² of cell bboxes in its 7276 µm²
region = **0.68**, with routing in M1 / M2 and M3 in the gaps. C3's free region is 7165 µm², so at that density it
takes 4854 µm² of cells.

| set | cells µm² | share of the region, cells alone | needed at C2's density | to remove |
|---|---:|---:|---:|---:|
| xa | 6842 | 96 % | 10100 µm² = 1.41 × | 1988 |
| xa without cload | 6455 | 90 % | 9528 µm² = 1.33 × | 1601 |
| xa + xt | 7272 | 101 % | 10733 µm² = 1.50 × | 2418 |

A second measure agrees. The library's own packing check, `fit_s2d_front` in `pad_buffer_cells.gds` (the cell's note:
"skyline packing", no routing, 2 µm gaps), is 145.4 µm tall in 80 µm width. The library README's older shelf numbers
are 136.5 µm for s2d and 94.2 µm for d2s. The free height is 94.3 µm, and SP sits in it. The d2s set packs into
74.0 µm the same way, and C2 fitted it into 94 µm with routing and the tree.

**Stop condition met:** `xa` does not fit, even compacted. Phase 2 was not started.

### 1.4 Levers of `layout_primitives.md` §4 that would make `xa` fit

| # | lever | §4's saving | estimate from §1.3 (reasoning) | circuit cost |
|---|---|---:|---:|---|
| 1 | one bias root per slot, 5 µA leg per pad | — | already applied: `xg` and `xc` go to the slot. Only `xt` is left (−429 if it leaves too, with the bias-voltage objection of §1.2) | — |
| 2 | cascodes at L = 2 (`lcas` = 2: fingers 10/2 instead of 15/3) | −500 | −750 … −850: the cascode cells are 1896 µm² by §1.3, gate area −56 %, cell area about × 0.55–0.6 | loop gain: d2s lost 3.5 dB from L 3 → 2. s2d's worst case is 64.5 dB against a limit of 60 dB, so about 1 dB would remain. Re-simulate |
| 3 | load capacitors out of the cell | −400 | −387 | none in the cell. They become a load on `outp` / `outn` in the slot. Decision 2 allows it |
| 4 | half-size CMFB units | −500 | −500 (the tubs don't halve: well overhead) | more output common-mode error |
| 5 | smaller input pairs, W = 10 / 5 | −350 / −500 | −350 / −500 | headroom, possibly 1/f noise |

To remove for `xa` at C2's density: 1988 µm².
- **§4's own numbers, all of 2–5:** −1750 … −1900. That is not quite enough.
- **With the cascode estimate of §1.3:** 2 + 3 + 4 + 5 (W = 5) is about −2140 … −2240. `xa` fits with about
  150–250 µm² to spare.
- **`xt` as well** (−2418 needed) fits only with the same four levers and a density of about 0.71, above C2's 0.68.
- **Without lever 5:** 2 + 3 + 4 gives −1640 … −1740, so `xa` needs a density of about 0.72–0.74.

So `xa` fits only with **all of levers 2–5**. Without one of them, the layout has to be denser than C2's. `xt` comes
in only on top of that.

Levers 2, 4 and 5 change the circuit, so they need re-simulation (CACE `loop_params`, dc, noise) and Christoph's
choice. Lever 3 needs only decision 2, which applies once the others are chosen.

Not on §4's list (reasoning):
- The fold sinks (853 + 525 µm²) carry most of the offset budget (5.4 of 6.1 mV), so they are no lever.
- The ESD zone y 0–84.4 has no free area in IOPadAnalog (§1.1). Taking room there would mean changing IHP's iovdd /
  iovss plates, against the brief.
- Moving SP out of the region's middle would gain little: it takes 111 µm² with its spacing.

## After phase 1: cleaned-out pad template (Christoph's request, 2026-11-03 19:20 CET)

"Look at the diff2single I/O pad and how the plates got cleaned out. Draft me a cleaned out single2diff I/O pad
template for review."

- **The template:** design branch, `macros/sg13cmos5l_IOPadSingle2Diff/layout/klayout/template/`: the GDS, the
  generator `build_template.py`, renders before and after, and `README.md` with every change.
- **How it is built:**
  - It starts from IHP's IOPadAnalog: protection instances, the ESD zone y ≤ 84.44 and the ring rails unchanged.
  - Above the Clamp_P frame, the p+ plate, the three bands, the pad fingers and the core-side pins are cleared.
  - C2's `nw_isolator` and `edge_stubs` are reused from `agents_c2/F2/out/padctx/`, with two adaptations: one
    isolator stack is left out next to SP's pad finger, and the left iovdd stub is tied.
  - SecondaryProtection gets its own ties: pad finger, iovss stack, iovdd line, `padres` stub.
- **Checks (`template/`):**
  - DRC on the template alone (maximal deck with latch-up; `run_drc.py`, 32 tables, LU.b): 0;
  - C2's row check: edge intervals the same as IOPadAnalog's on every layer, every rail and band one net through the
    row, row DRC 0 (`template/row/`);
  - the template's LVS extraction identical to IOPadAnalog's (`template/lvs/`).
- **Found:** IHP's IOPadAnalog does not pass IHP's KLayout LVS against IHP's own spice, and the I/O CDL does not load
  (`template/lvs/IOPadAnalog_vs_ihp_spice.out`, the template's README). That answers §1.2's open LVS question: phase 4
  needs a reference netlist of its own for the protection cells.
- **Free region** in the template: y 86.15–180, x ≈ 1.8–78.2, less SP and its tie lines. That is the region §1.3
  counted.

### Version 2 (Christoph, 2026-11-03 19:35 CET)

"With the help of clamp and diode pcells, the protection structures, narrow the clamp cells and rearrange them so that
they fit entirely into the region adjacent to the narrow nwell paths at the botton (pad side) of the layout. For now,
eliminate the secondary protection structure."

- **What changed** (design branch, `layout/klayout/template/README.md`):
  - IHP's five protection cells are gone, and SecondaryProtection is not replaced.
  - CN / CP are `Clamp_N_M1` / `Clamp_P_M1` ng 20, l 0.6u, frame fit (36 µm wide instead of IHP's 80 µm frames);
    DN / DP are `DCNDiode` / `DCPDiode` l 27.78u.
  - They sit in two columns between the NWell legs, y 5.38–39.02: n-type left, p-type right, diode on clamp as in IHP.
  - The 0D gate ties are SG13_dev rppd (3.54u / 12.9u).
  - New M2 pad / iovss / iovdd wiring; a core-side `pad` pin at y 40; a p+ edge stub at y 65–84.26.
- **Checks (`template/`)**, version 1's in `template/superseded_v1_ihp_protection/` (replaced by version 2):
  - DRC alone: maximal with latch-up 0; `run_drc.py` 32 tables, 0, no exception.
  - Row: edge intervals the same as IOPadAnalog's, 25 / 25 rails and bands one net, row DRC 0.
  - Extraction (`template/lvs/template_extracted.cir`): IHP's protection values without SP (NMOS W 88, PMOS W 266.4,
    dantenna / dpantenna 2 × 35.0 µm², rppd 3.54u / 12.9u).
  - One difference to IHP: RP's bulk is the substrate, not iovdd.
- **Consequence for §1.3 (estimate):**
  - The free region grows from 7165 µm² to about 10 600–11 000 µm² (y ≈ 39–180, plus 30–39 above the N column).
  - At C2's density, `xa` (10 100 µm²) would fit with about 5 % to spare. `xa` + `xt` (10 700 µm²) would be at the
    limit.
  - Not yet counted: latch-up spacing or an isolator between the ESD zone and the buffer (IOPadAnalog's p+ plate),
    and the four iovdd M2 lines up to y 66.8.
  - The stop condition of phase 1 needs a fresh look on this frame before phase 2.

### Version 3 and the protection schematic (Christoph, 2026-11-03 about 19:50 CET)

"Diodes side by side closest to the pads. No long metal wires towards the core. Clamps side by side. make me a xschem
schematic of the components you left standing so I get an idea what the resistors are all about."

- **Layout** (design branch, `layout/klayout/template/README.md`):
  - DN | DP side by side at the pad exit (y 5.38–20.20); CN | CP side by side at the top of the leg region
    (y 41.4–61.44), mirrored in y so that the gate buses face the rppds in the gap.
  - pad straps from the pad bar over the diode stripes to the clamp drains.
  - iovdd: 9 + 1 straps from DP's frame through CP's inner ring straight up into M3 iovdd.
  - Nothing goes towards the core except the iovdd ties up to y 66.8 and the pad pin at y 61.6.
  - The four long iovdd lines through the core region of version 2 are gone, and so is its pad pin at y 40.
- **Checks (`template/`)**, version 2's in `template/superseded_v2_two_columns/`:
  - DRC alone: maximal with latch-up 0; `run_drc.py` 32 tables, 0, no exception.
  - Row check: edges the same, 25 / 25 nets, row DRC 0.
  - Extraction: the same devices as version 2.
- **Schematic** `schematic/xschem/s2d_pad_esd.sch` / `.sym` (design branch). Its notes explain the diodes, the
  clamps, the two rppd gate ties and the ptap1 "resistors" of IHP's spice. `template/lvs/cmp_esd.py`: the xschem
  netlist equals the layout extraction in all 6 device classes (`cmp_esd.out`); a copy with one terminal moved fails.
- **Free region (estimate):** the core side is now y ≈ 62–180, about 9000 µm². That is less than version 2's
  10 600–11 000 µm², because the protection fills the leg region and the gap row y 20–41 holds only straps. It is
  more than version 1's 7165 µm². At C2's density `xa` needs about 10 100 µm², so with version 3 it does not fit
  without levers (§1.4), about 1.12 × the region.

### Version 4 (Christoph, 2026-11-03 about 20:05 CET)

"Why is there so much distance between diodes and clamps in your latest ESD template? If there's no good reason for
keeping the wires that long, shorten them."

- **Why version 3 had the gap:** M3 / M4 / TM1 over the whole protection zone (y 7–60) are iovss rails, so iovdd
  has to climb on M2 to the M3 iovdd rail at y 66. I had put the clamps at the top so that CP sat under that rail.
  That does not justify the gap: DP's iovdd has to climb from the pad side anyway, and the gap only lengthened the
  pad straps to the clamp drains.
- **Version 4:**
  - CN / CP sit directly on DN / DP, rings abutting as in IHP's cells. The zone is y 5.38–41.6.
  - The pad straps are 24 / 33 µm long (version 3: 47 / 56).
  - The iovdd straps end in a 2.2 µm M2 bar just above CP. Two risers at the column's edges (x 42.6–45.2,
    75.5–78.4) take it into M3 iovdd, so the band above the clamps stays free.
  - The pad pin is 1.7 µm above CN.
- **Checks (`template/`)**, with version 3's in `template/superseded_v3_clamps_at_top/`:
  - DRC alone: maximal with latch-up 0; `run_drc.py`, 32 tables, 0, no exception.
  - Row: 25 / 25 nets, the edges the same, row DRC 0.
  - Extraction: the same devices.
  - `cmp_esd.py` (now naming the layout's gate nets by the clamp they drive): 6 / 6 equal against the unchanged
    schematic. A copy with one terminal moved fails.
- **Free region (estimate):** ≈ 10 600 µm² (version 3: 9000). At C2's density `xa` needs ≈ 10 100 µm², about
  0.95 × the region. That leaves no room for `xt`, and the latch-up spacing to the ESD zone is not counted.

### Version 4, iovdd Via2 (Christoph, 2026-11-03 about 20:15 CET: "Yes, go ahead.")

- **Checked first (L2N probes, M1–M3):** every long wire ends on its M3 rail. DP's cathode, CP's sources, the iovdd
  bar and both legs are one net with the M3 iovdd rail; DN's anode, DP's guard ring, CN's sources and CP's outer
  ring are one net with the M3 iovss rails.
- **Via2 into the M3 rails** (`template/via2_rails.py`, `via2_rails.out`):

  | rail | IOPadAnalog | version 4 before | now |
  |---|---:|---:|---:|
  | iovdd 66–91.5 | 495 | 14 | 151 |
  | iovss 7–32.5 | 242 | 306 | 306 |
  | iovss 34.5–60 | 0 | 9 | 9 |

  IHP's 495 come from 11 straps × 45 Via2, because its Clamp_P sits under the iovdd rail. The risers now run 6 µm
  under the rail with 13 × 5 + 13 × 6 Via2, and the leg ties have 4 each.
- **Matching IHP's count** would need the risers under the whole rail (to y ≈ 91, about 50 rows × 11). Not done:
  it costs M2 at two x positions in the buffer's region. Christoph's choice.
- **Checks**, with the predecessors in `superseded_v4_one_via2_row/`: DRC alone and in the row 0, 25 / 25 nets,
  `cmp_esd.py` 6 / 6.

### Tentative fit of the s2d blocks into template version 4 (Christoph, 2026-11-03 about 20:25 CET)

"No, tentatively fit the single2diff buffer circuit into the pad space. How much fits now?" (the risers stay at
6 µm.)

**Method** (`fit/fit_s2d.py`, results `fit/fit.md`, `fit/fit_A.gds` / `fit_B.gds` with renders):
- placement only, no wiring;
- the bounding boxes of the drawn s2d cells: library `pad_buffer_cells.gds`, plus N2's `sinks_6x6_s2d_c2`;
- bottom-left fill into the free region of version 4, 10 638 µm² (protection kept 1.5 µm off, risers 0.5 µm);
- 0 / 90° rotation, 64 block orders tried, the best one kept;
- checked: no placed box touches a template shape or another box.

| variant | boxes | gap | placed | left out | cells / free region |
|---|---|---|---|---|---:|
| A | drawn cells | 2 µm (library packing gap, no wiring room) | xa, cload, xt: all 15 blocks | none | 7689 µm², 72 % |
| B | drawn cells | 4 µm (rough wiring allowance, reasoning) | xa complete, part of xt | cload, bias_tree_n | 6997 µm², 66 % |
| C | C2-compacted estimates (budget.py) | 4 µm | all 15 | none | 7259 µm², 68 % |

**Reading:**
- `xa` itself fits in every variant.
- The load capacitors and the bias tree fit only with 2 µm gaps or with C2-style compaction.
- Against C2's routed density (0.68), the drawn cells need ≈ 11 300 µm² (1.06 × the region). The compacted
  estimate needs ≈ 10 700 µm² (1.00 ×). It is at the limit, no longer clearly out as in phase 1 (1.41 × on IHP's
  frame).
- The placement is a packer's, not a floorplan: the input tubs sit between the risers, away from their tails.
- A real floorplan (C2's stage A) would group by signal flow and needs the compacted primitives of phase 2.

## Phase 2: primitives (started 2026-11-03 20:33 CET)

Christoph chose fit variant A, so the cell holds all of `xa`, the load capacitors and `xt` (decisions.md).

| agent | model, effort | cells | brief |
|---|---|---|---|
| P | Opus, high | tub_p20x1 + s2d_inputs, s2d_tails, s2d_loads, s2d_casc_p, s2d_pd_p, bias_tree_noab_p | `agents_c3/P/BRIEF.md` |
| N | Opus, high | sinks_6x6_s2d (N2's cell checked, changed only where rules require), s2d_sinks_cmfb, s2d_casc_n, s2d_pd_n, s2d_cload, s2d_rhigh, bias_tree_noab_n | `agents_c3/N/BRIEF.md` |

Results (P finished 21:10, N 21:13; reports `agents_c3/{P,N}/report.md`; lead checks `lead_checks/{P,N}/`, about 21:15–21:20):

| cell | size µm | area / library | lead check |
|---|---|---:|---|
| tub_p20x1_c3 | 4.30 × 11.97 | 0.92 | rebuild identical, DRC clean, LVS match, = circuit, sym 0 |
| s2d_inputs_c3 (12 tubs + 4 dummies) | 47.58 × 26.44 | 0.93 | the same (LVS deep) |
| s2d_tails_c3 | 45.19 × 15.83 | 0.66 | the same |
| s2d_loads_c3 | 43.19 × 12.32 | 0.74 | the same |
| s2d_casc_p_c3 | 52.23 × 12.81 | 0.92 | the same; sym: Cont 0.27 µm² in the center device (PCell contact rounding) |
| s2d_pd_p_c3 | 3.20 × 2.97 | 1.33 (own tie) | the same |
| bias_tree_noab_p_c3 | 12.94 × 10.37 | 0.59 | the same; sym: Cont 0.04 µm² in the center device |
| sinks_6x6_s2d_c3 (+ `_core`) | 16.51 × 51.00 | 0.87 | the same; sym: Cont 0.08 µm² on BN / twin (PCell, as N2 / F2) |
| s2d_sinks_cmfb_c3 (+ `_core`) | 16.51 × 32.25 | 0.89 | the same, sym 0 |
| s2d_casc_n_c3 | 72.74 × 14.37 | 1.03 (dummies, ring) | the same, sym 0 |
| s2d_cload_c3 (with TPN / TNN inside) | 29.56 × 14.24 | 1.09 | the same, sym 0 (one row) |
| s2d_pd_n_c3 (standalone, tapless) | 2.50 × 2.34 | 1.15 | DRC: LU.b only (no tap, by design; the pad uses the pair inside cload) |
| s2d_rhigh_c3 | 19.24 × 20.09 | 0.96 | the same, sym 0 (LVS: 6 × 0.5/50.6) |
| bias_tree_noab_n_c3 | 24.21 × 9.21 | 0.72 | the same, sym 0 |

- **Sum of the cells (bounding boxes, cload with the pd pair):** 6769 µm², against 7689 µm² in fit A with the library cells (0.88).
- **Agent F**, stage A (placement and compaction; then Christoph's review), started 21:21, Opus, effort high. Brief:
  `agents_c3/F/BRIEF.md`.

The bias tree's cells are added to the brief's lists, because `xt` is in the cell. The lead checks each delivery with
C2's `lead_check.py` and `sym_check.py` before F gets the cells.

## Phase 3, stage A: placement and compaction by agent F (21:37–22:05 CET; lead check about 22:15)

F's note: `agents_c3/F/report_stageA.md`. Messages: `agents_c3/F/messages.md`. Picture: `agents_c3/F/out/previews/placement_A.png`.

- **Arrangement, bottom up from the drawn cells:**
  - left pocket above CN: the NMOS fold (`sinks` | channel C1 over the pad pin | `casc_n`);
  - right pocket above CP: `casc_p` and `loads`, abutted in one NWell;
  - above the pockets, the input group `tails_lo` / `inputs` / `tails_hi`, with `rhigh` beside it and its pin bank
    centered on the tubs;
  - `sinks_cmfb` at the tubs' xc / yc corner;
  - the bias tree beside / above `tails_hi`;
  - `cload` and `pd_p` under the outputs.
- **Area:** cells 6881 µm² placed (6769 as delivered, +112 for the tails split) in a block x 1.80–78.20, y 31.70–176.74.
  - The free region is 10695 µm²; the cells cover 64 %.
  - Of the 3814 µm² left, 2100 are reserved M1 / M2 channels C1–C9, sized as nets × 0.48 µm; 1714 are free.
- **The one change to a primitive:** P's two-row `s2d_tails_c3` becomes `s2d_tails_hi_f` / `s2d_tails_lo_f`, one row
  above and one below the tubs, so every tail drain faces its tub with short links of equal length. This is open for
  Christoph against "no taps between rows" (F's messages, point 2). The fallback is P's cell above the tubs, with
  half the links at about 45 µm.
- **Isolator:** F reasons that none is needed, from the existing double rings (CN / DN; CP's p+ ring + the PMOS cells'
  n+ rings), with latch-up DRC 0. Christoph's call; 2 µm of slack exists.
- **Lead check** (`lead_checks/F_stageA/summary.txt`):
  - rebuild byte-identical;
  - the template part unchanged (XOR empty);
  - all 13 cells placed once, no overlaps;
  - IHP DRC 0 (maximal deck with latch-up; `run_drc.py`, 32 tables, no exceptions);
  - row check 25 / 25 (the earlier "26 / 26" was the lead's miscount);
  - the split tail rows: DRC / LVS / symmetry clean, together equal to the circuit.
- **Stops here** for Christoph's review of the placement picture (the brief). Stage B (routing) after his go.

## Notes folder

| file | contents |
|---|---|
| `report.md` | this report |
| `decisions.md` | Christoph's decisions for C3 (verbatim) |
| `budget.py` | §1.3 |
| `phase1/edges.md`, `phase1/nets.md` | `row_check.py` on the IOPadAnalog row |
| `phase1/row_maximal.lyrdb`, `phase1/main_row/` | DRC of the row (maximal with latch-up; `run_drc.py` tables) |
| `phase1/budget.md` | `budget.py`'s output |
| `template/` | checks of the cleaned-out template: DRC, `row/`, `lvs/` |

Logs: `sudelbuecher/logs/claude/c3-s2d-pad-layout/` (+ rows in `sudelbuecher/MANIFEST.tsv`).
