<!--
SPDX-FileCopyrightText: 2026 Christoph Maier
SPDX-License-Identifier: Apache-2.0
-->
# F: stage 3 report (pad candidate)

Saved by the lead from F's final reply of about 18:43 CET (F dated it 18:50): the harness did not let the agent write
`out/report.md`. The text below is F's, unchanged except for this header; the lead's check follows in
`../../../design_considerations/pad_buffer_layout/pad_cell_2026-10-31/lead_checks/F_stage3/`.

## Stage 3 done (F)

1. **Assembly.** `out/pad_candidate.gds` (top cell `sg13cmos5l_IOPadDiff2Single`) contains `d2s_block`, which is
   d2s_mpdda_pd plus bias_tree_pd. It was built bottom up from P's and N's checked cells, used unchanged, and F's own
   cells. The block sits at y 89.2–169.1 above the P frame and is wired in Metal1/Metal2, with Metal3 only in the gaps
   at y 119–126 and 134–140.
2. **Checks** (log: `out/logs/stage3_checks.txt`):
   - DRC (`run_drc.py`, main + maximal decks incl. latch-up, plus antenna): 0 violations, no exceptions, on the pad, the
     block, each of F's cells and the abutment row.
   - LVS (`run_lvs.py`): the pad matches `pad_candidate.cdl`; the block and each of F's cells match their CDLs.
   - Net probes: all 23 expected nets land where they should, no shorts.
   - Row check: every edge layer equals IOPadAnalog's, and every band and rail is one net through the row.
   - Current paths: no pad or rail path is narrower than before.
3. **Open points of 2026-10-28.**
   - Closed: the a/b joins (Metal1 hops under them); `guard` is now tied to iovdd; CMA has a p+ guard ring, and so does CMB.
   - Still open: rules sitting exactly at their limit, all inherited, none new; and the 63/0 box, left for the lead to delete.
4. **Capacitor-only nodes.** Magic PEX (EXT_MODE=2) finds 19. Eighteen sit on the d2s_rhigh segments (16 plus 2
   dummies); the 19th is the 1.2 V vdd rail, which has no devices on it.
5. **CMB-stage reserve.** Not drawn; it does not crowd the bias tree.
   - Spot: x 54.0–66.6, y 89.3–98.6 (12.6 × 9.3 µm), free. Only l1's riser moved, from x 61.0 to 67.0. Estimate: the 2 kΩ
     stage (rppd 1 × 7.435 plus both diodes and ties) needs about 9 × 9 µm; the ESD zone has no room (3 µm beside CMB).
   - Pad feed: pad line k=16 (x 57.06–57.67) up through the Metal2 corridor (one isolator tap left out for it), then a
     Metal1 hop under the joins. About 8 µm, full width.
   - Gate-line path, kept free: from CMB's gate head (x 73.4, y 50.64) east to x 78.15, up the right edge channel
     x 78.0–78.3, Metal1 under the joins, west at y 88.25. About 55 µm, roughly 3 fF on the gate node.
   - Cut point: CMB's gate is now fed only from pad line k=21. Cutting means removing the 2 vias at (72.26 / 72.67, 50.64).

## Method

- Bottom up: cells as drawn, placed in the pad context. No tweaked copies of P's or N's cells were needed; the misfits
  were absorbed in routing:
  - the tails are shifted +2.47 µm under the inputs, so sa/sb run straight up;
  - pl/pr/l2 between casc_p and loads cross over on Metal1 tracks in a 1.46 µm gap;
  - the sinks abut casc_n at N's 7.0 µm offset, so x/y meet directly.
- bias_tree_pd is mirrored: vbp, vbn, vabn and vbnc leave on the right next to their loads; vbpc and vabp leave on the left.

## Floorplan (absolute µm, cells as placed)

| cell | x | y | note |
|---|---|---|---|
| casc_p | 2.50–13.82 | 89.20–122.84 | |
| loads | 2.50–13.82 | 124.30–154.32 | |
| d2s_rhigh | 15.20–29.12 | 89.20–104.61 | sa/sb channel above it, y 105.0–108.3 |
| ab_n | 31.00–37.86 | 89.20–94.64 | |
| ab_p | 38.60–44.61 | 89.20–97.10 | |
| pd_p | 45.30–49.01 | 89.20–92.17 | |
| pd_n | 49.70–53.22 | 89.20–91.24 | |
| tails | 18.07–50.34 | 109.00–123.81 | |
| inputs | 15.60–47.65 | 125.61–152.32 | |
| casc_n | 67.50–77.23 | 89.20–122.32 | |
| sinks | 60.50–76.03 | 122.32–169.11 | |
| bias_tree_pd (mirrored) | 2.60–54.96 | 154.70–166.52 | |

- Cell area 4038 µm²: P 2114, N 1093, rhigh 215, tree 619.
- Free besides the reserve: about 190 µm² at x 54.5–77.5, y 169.3–177.6.

## Wells

- One iovdd n-well covers casc_p, loads, tails, ab_p, pd_p and the inputs' dummy wells, joined by drawn bridges.
- The tree's PMOS well remains its own island, so "one n-well per rail" is not fully met. A bridge to the inputs' right
  dummy well failed the NW.d rule against the tree's n+ ring.
- The n-well isolator above the P frame is separate by design.

## Pins (Metal2, pin box y 179–180, centre x)

| pin | x |
|---|---|
| en_3v3_b | 30.815 |
| en_3v3 | 31.645 |
| iref | 33.105 |
| vinp | 57.80 |
| vref | 58.30 |
| vinn | 58.80 |

## Routing

- Metal2 vertical, Metal1 horizontal.
- Right channel: 10 Metal2 lines at x 55.3–59.8.
- Class-AB tracks: Metal1 at y 98.0–100.5.
- Metal3 hops: vfb at y 125.0–125.6; vbpc and vabp at y 135.3 / 136.3.
- vfb Kelvin line: from the junction's left end, up the left edge channel at x 1.90–2.20, about 110 µm in all, carrying
  gate current only. Antenna check is 0.
- Supply taps, each separate: tails one Via2 into iovdd; sinks one Via2 into iovss; loads and casc_p one tap; SA's vddo
  and pd_p's vdd Via2 in the corridor at y 85.95; SB's vsso, ab_n's vss and pd_n's vss onto the frame's p+ ring; casc_n to
  the right p+ stub; the bias tree its own iovdd and iovss lines.

## ESD

- A double ring towards the circuitry: the P frame's p+ ring plus the new n-well isolator.
- CMA and CMB each have a p+ (iovss) ring. They share the middle leg, because one 1.8 µm gap holds only one leg; their
  wells stay separate.
- Latch-up rules give 0 violations.

## Changes to the pad top's static cells (clamps, diodes, TopLayersTo4, Metal3ViasUp and contacts untouched)

- cap_cma → d2s_cma: bottom Metal1 strip removed; Metal2 tabs with 88 vias feed the two columns.
- m2_junction: 332 vias removed (they landed on that strip).
- cap_cmb → d2s_cmb: renamed, pins added.
- m2_comb_p: 20 vias on CMB's gate head removed.
- New cells: cm_rings, guard_tie, nw_isolator (18 taps), edge_stubs, vfb_kelvin, d2s_block.

## Deviations

- LVS flags: `--ignore_top_ports_mismatch` (in flat mode the sub-cells' own pin labels become extra top ports; the net
  and device cross-reference matches regardless); `--implicit_nets` limited to the supply rails, which the IO ring joins
  outside the cell. A negative test with one via removed fails LVS.
- PEX: `make magic-pex` stops at its port check, because the macro's symbol still has the old 14 ports; the netlist
  itself is written.
- Row DRC: one run crashed in the maximal deck (exit 11); the rerun was clean with no exceptions.
- Not done: simulation of the extracted pad, IR drop of the routing.

## Netlist changes (`netlist_changes.md`)

P's and N's dummies and finger counts; the rhigh chains, each with 2 dummy segments; the bias diodes moving into
d2s_mpdda_pd, with the bias_tree_pd sheet change as a proposal; the SA / SB bulk changes; the pad-level reference.

## Files (sha256, first 12 hex), in `/home/user/c2/F/out/` (copied to `out/` here)

- Pad: `pad_candidate.gds` 30643f891b33, `pad_candidate.cdl` 3c2b7884fdbe.
- Cells (`cells/`): `d2s_block` b6547923276a / c4867eca7c4a; `d2s_rhigh` 24aa5b631ac7 / b6c731d30058; `bias_tree_pd`
  ecbf649915a2 / c0845cee4555; `d2s_cma` 15a3c9337766 / e2bf0951ba9b; `d2s_cmb` 2616d7eda185 / 0ddde4fe4bdc; `cm_rings`
  6db8b70941ed; `guard_tie` 12437d9d078d; `nw_isolator` 505302ce1b54; `edge_stubs` ef314daa2ede; `vfb_kelvin` 1b04e9d710af.
- Notes: `netlist_changes.md` 2b05146c7df2, `stage2_notes.md` 029274279d52, `floorplan_stage1.md` 5be8afba0fff,
  `requests_for_P_N.md` 6b92d7c106fd.
- Logs: `stage3_checks.txt` 1b1ffdd81ccb, `pex_capacitor_only_nodes.txt` ad865342ab1e, `pad_candidate_magic_pex_2.spice`,
  `path_widths_pad_candidate.md` ae2a5bb01004, `path_widths_pad_before.md` 777a23e6b76a.
- Previews: `stage3_placement.png` 2c2eb75351fb, `stage3_routed_in_pad.png` 5cccfc4d2804 (reserves in red),
  `stage3_detail_bottom.png` 46de9f6cd8b5, `stage3_detail_right_channel.png` a6ed7fce5187, `stage3_detail_left_edge.png`
  6fd72889a1ef.
- Scripts (`src/`): `sh run_all.sh <out> <run>` rebuilds everything (two rebuilds give the same bytes); `sh run_checks.sh
  <out> <run>` reruns the checks. `build_block.py` c3e4ee9fcffa, `build_pad.py` 0a87a7bfebc7, `run_all.sh` 9af4bfbf6f31,
  `run_checks.sh` c28c441f085e.
- Superseded: `pad_stage2.gds` 5d8eebca2615.
