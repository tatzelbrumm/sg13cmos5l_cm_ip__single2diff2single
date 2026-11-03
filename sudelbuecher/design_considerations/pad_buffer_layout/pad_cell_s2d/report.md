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
