<!-- SPDX-FileCopyrightText: 2026 Christoph Maier / SPDX-License-Identifier: Apache-2.0 -->
# F report (C4): pad_ref_rb v2, after Christoph's review (Claude, agent F, 2026-11-07, 23:00-23:30 CET)

## Summary

- `out/pad_ref_rb.gds`, 73.80 x 76.26 um = 5628 um2 (v1 7352, ceiling 5700), M1 / M2 only [M].
- run_drc.py --no_density 0 (no "exception"), maximal + latch-up 0, flat LVS match against the circuit files with
  bypass_rb as drawn; a negative LVS test fails as it should; metal-only connectivity 0 splits [M].
- Rows unchanged (8 of 8 XOR 0). bypass_rb became four capacitor blocks used as filler (N's bypass code with W x L
  units). Gate area vcm 720.3 um2 (CB 144 in rb_cload, over BB), vref 1296.6 um2 [M]. Every capacitor is in the note.
- Position: right edge at slot x 535.0, y 169.1 .. 245.3. vcm pin at y 223.34, straight out to the D2S vref. vref
  pin at 179.06 runs down the right side to the S2D vref. Inputs en_3v3 / en_3v3_b / iref on the left edge, own
  enables. vddh / vssh are on the left edge.
- No action was refused or blocked. v1 is kept in `out/v1/`.

The note follows (`out/note.md`).


[M] = tool result, [R] = reasoning. v1 (7352 um2, pins bunched at slot7's bottom right) is kept in `v1/`.
Rebuild and check: `sh src/all.sh <inputs> <out> <work>` (2 min).

## Result [M] (`logs/summary.txt`)

| check | result |
|---|---|
| run_drc.py --no_density | No DRC violations detected, 0 "exception" lines |
| sg13cmos5l_maximal.drc -rd latchUpRules=true | 0 errors |
| flat LVS, --disable_tap_extraction, vs `pad_ref_rb.cdl` | Netlists match |
| negative LVS test (BA's gate moved m -> gh) | Netlists don't match: not vacuous |
| metal-only connectivity (LVS joins vss rings through the substrate) | 16 nets, 0 split |
| the 8 rows vs the delivered cells, all layers | 8 of 8 identical (texts vdd / vss -> vddh / vssh only) |
| sym_check, rows | 0; rb_tree_p Cont 0.0384 (P's known PCell residual) |
| capacitor blocks alone (`cells/logs/`) | DRC 0, maximal + LU 0, LVS match each; sym 0, capt 15.7 um2 (one column) |
| metal over transistor gates / over capacitor gates | 0 / 11.7 um2 M1 + 0.3 um2 M2 |

The CDL is composed from the circuit files with `bypass_rb` replaced by `bypass_rb_drawn.spice` (the drawn
capacitors): 58 devices = 38 active + 20 dummies.

## Area and place [M]

- **73.80 x 76.26 um = 5628 um2.** v1: 7352 um2. Ceiling: 5700. Cell and capacitor boxes: 4822 um2, 86 %.
- **Proposed position:** right edge at slot x 535.0, lower left (461.20, 169.07), spanning y 169.1 .. 245.3. This is
  between the S2D group (112-160) and the D2S group (222-262).
  - The vcm pin is at the D2S vref pin's height, 223.34, so it runs straight out.
- **Pins** (slot coordinates), Metal2, 0.29 um wide:
  - right edge: vref y 179.06 (runs down the right side to the S2D vref, 112.26); vcm y 223.34 (on to the S2D vcm,
    136.02, along the edge).
  - left edge, bottom to top: en_3v3 206.33, en_3v3_b 207.41, iref 208.49 (own enables and own iref leg); vssh 179.06,
    vddh 212.81.
- **vcm and vref are not crossed at the top level** [R]: the vcm route along the edge ends at 136, above the point
  where vref turns in at 112.

## Placement, bottom to top (signal flow; routing in `routing_plan.md`)

- **capr** (vref capacitors), the full width under **rb_casc** (R180: vref top right, xp top left, vbnc / vdd on the
  right edge). capr and rb_casc abut: one ThickGateOx.
- **rb_tree_n** (R0: pins up; en_3v3 on the left edge, at the input pins) | **rb_tails** (M0) | **rb_tree_p** (M0).
  rb_tails and rb_tree_p abut, so the vbp stubs meet; one NWell [M]. rb_tree_p's vbnc pin faces rb_casc's vbnc end.
- **rb_mirror** (M90: bd / vcm on its right edge) with **capm** on it | **rb_avg** (R0) | **rb_tubs** (R0, over the
  tails: TR under MR, BT under BA / BB) | **capt**.
- **capv** | **rb_cload** (M0: pins down, its vcm pin over BB's vcm pin). CB thus sits on the buffer output.

## Capacitors (bypass_rb as drawn: for the lead's backannotation)

All hv NMOS, gate = node, S = D = B = vssh, one finger each. Built by `src/capgen.py`: agent N's `bypass()` code with
the 12 um unit turned into W x L. Same finger, gate column, facing pairs, closed p+ ring and Metal2 gate bus.

| cell | node | count | W (um) | L (um) | gate (um2) | where |
|---|---|---:|---:|---:|---:|---|
| capr | vref | 2 | 34.1 | 16.9 | 1152.6 | full width under rb_casc |
| rb_cload CBR | vref | 1 | 12 | 12 | 144 | rb_cload (the pad's CLN slot), unchanged |
| capv | vcm | 2 | 19.24 | 12.66 | 487.2 | top left |
| capm | vcm | 2 | 8.18 | 3.25 | 53.2 | on rb_mirror |
| capt | vcm | 1 | 2.9 | 12.4 | 36.0 | right of rb_tubs |
| rb_cload CB | vcm | 1 | 12 | 12 | 144 | vcm_rb's CB, unchanged |

- **Totals:** vcm 576.3 + CB 144 = 720.3 um2 (target 720); vref 1152.6 + 144 = 1296.6 um2 (target 1296).
- **Netlist:** `bypass_rb_drawn.spice` holds the subcircuit as drawn: XCBR_cload, XCBR_capr m=2, XCBM_capm m=2,
  XCBM_capt, XCBM_capv m=2.
- **Re-simulation [R]:** capr's 34.1 / 16.9 lies outside the sizes simulated so far; the PSP model scales, but the
  bypass should be re-simulated.

## Changes to the rows

None: the 8 placed rows are XOR 0 against the delivered cells. bypass_rb (N's 3 x 4 array) is replaced by the four
capacitor blocks above. No transistor or dummy is added, removed or re-tied; only bypass_rb's capacitors change.

## Routing [M]

- C2's grid router, unchanged (`src/generator.py`, sha256 cea21b865695). Pitch 0.27 um, wire 0.29 um, M1 horizontal
  and M2 vertical preferred, M1 / M2 only.
- Every net routed, the second round. Totals: M1 469 um, M2 226 um, 76 vias.
- **Keep-outs:** every transistor gate (+0.1 um). The capacitor blocks are open to routing, because metal over a
  bypass gate only adds capacitance to a DC node [R]. Each pin owns its strip of the edge.
- **One strap drawn by F:** M2, 0.29 um, from rb_casc's vdd pin to a vddh terminal in the right channel. When the
  router landed on that pin, it filled the gaps between rb_casc's same-net vdd tracks into a plate wider than 0.3 um
  next to vbnc, which is an M2.e violation (measured in v1 and in v2a).
- **Net lengths M1 / M2 (um):** ts 0 / 3.3, bt 0 / 3.5, m 17.1 / 1.1, vbnc 19.8 / 1.6, xp 19.5 / 16.7, gh 25.1 / 11.6,
  ni 30.5 / 10.4, bd 29.2 / 14.4, vbp 39.1 / 27.0, iref 62.9 / 2.8, en_3v3 0 / 0.8, en_3v3_b 71.0 / 26.4,
  vcm 66.3 / 14.3, vref 48.1 / 65.8, vddh 37.6 / 17.0, vssh 3.0 / 9.6.

## Open points [R]

1. **Area:** 5628 um2 is 1.3 % under the ceiling. The rest is routing channels (1.5 / 3.23 / 1.0 um) and rb_casc's
   72 um length, which sets the width. capm and capt are thin fillers (49 % and 45 % gate per box).
2. **Supplies:** vddh and vssh are single edge pins (0.29 um wide) wired by the router. Supply currents are about
   25 uA. If rails are wanted at the top level, the left edge is free for them.
3. **Re-simulation:** the bypass, with the new capacitor sizes, and the enable settling.

## out/ files (sha256, first 12 hex; v1 in out/v1/)

- 4cdb45458c00 bypass_rb_drawn.spice
- f3ed2aa63034 cells/logs/capm_lvs.log
- 5d071e69f639 cells/logs/capm_maximal_lu.log
- ca93122c0c25 cells/logs/capm_run_drc.log
- 10c83140eb45 cells/logs/capr_lvs.log
- d081b4bd00b5 cells/logs/capr_maximal_lu.log
- 0be9ba553c0d cells/logs/capr_run_drc.log
- 257b72788c77 cells/logs/capt_lvs.log
- 25dfbc8ca981 cells/logs/capt_maximal_lu.log
- 81ace61f25b8 cells/logs/capt_run_drc.log
- 5bacb4acc6f6 cells/logs/capv_lvs.log
- c9e343b3f1a4 cells/logs/capv_maximal_lu.log
- 58f6f50def8d cells/logs/capv_run_drc.log
- 54529ad946be cells/logs/sym_caps.txt
- c35188ee5451 cells/rb_caps.cdl
- 8f84d6b5b3e7 cells/rb_caps.gds
- 881fe6befb74 logs/capgen.txt
- 381aad9fd061 logs/compose_cdl.txt
- 4f6e162ace96 logs/metal_conn.txt
- 1e64a20e2276 logs/pad_ref_rb_extracted.cir
- ad20f75c9ef1 logs/pad_ref_rb_lvs.log
- cf5aedf6b146 logs/pad_ref_rb_maximal_lu.log
- dbb5c68ae195 logs/pad_ref_rb_run_drc.log
- b144527d9ce0 logs/route.txt
- 3e9e18dae9f4 logs/row_xor_vs_inputs.txt
- 86c33a76f1b0 logs/summary.txt
- a11af85ca3b1 logs/sym_check.txt
- d02733b53a0e net_list.md
- f79b401d0fab netmap.gds
- 340a388d7abd note.md
- 2dc2d707ede0 pad_ref_rb.cdl
- 37b1cac0e9f1 pad_ref_rb.gds
- bee4f8f90217 pin_map.md
- 71fa28fcce01 previews/bottom.png
- 14b5d573419f previews/context.png
- 233b3a5c8d2d previews/core.png
- 34f50ab62205 previews/pad_ref_rb.png
- 19b96d46d3e4 previews/top.png
- 8429df59a6c8 routing_plan.md
- cb6f87896d62 src/all.sh
- fb6b1d3ea3c9 src/bypass_spice.py
- 099f907444aa src/capgen.py
- 3d4c2461ca3f src/check.sh
- 6d51d2d3e59e src/compose_cdl_rb.py
- a9022f36dd9e src/context.py
- e447e3ef2447 src/finalize.py
- cea21b865695 src/generator.py
- 3f5856db716f src/ihp_sg13cmos5l.py
- b3efe06f7c00 src/make_frame.py
- 3ae6b00a1736 src/metal_conn.py
- cda5c037462a src/pin_map.py
- eaa5721bf00a src/rb_cfg.py
- fe8d0f9d6697 src/rb_place.py
- 79a253941a11 src/render.py
- 15669a0404ee src/route_rb.py
- 288029b9b3a8 src/row_xor.py
- dec272a75847 src/run.sh
