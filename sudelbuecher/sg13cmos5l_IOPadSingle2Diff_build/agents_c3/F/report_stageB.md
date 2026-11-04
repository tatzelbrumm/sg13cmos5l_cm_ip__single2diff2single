<!--
SPDX-FileCopyrightText: 2026 Christoph Maier
SPDX-License-Identifier: Apache-2.0
-->
<!-- Saved by the lead from agent F's final reply (the harness refused F's own write of this file). Text as F sent it. -->
# F stage B: the routed pad candidate `sg13cmos5l_IOPadSingle2Diff` (C3, 2026-11-04, 13:08–14:10 CET)

1. **Checks.** `pad_candidate.gds` (template v4 + routed `s2d_block` at (0, 26)) and `pad_candidate.cdl` pass all of
   them [M]:
   - run_drc.py: "No DRC violations detected", 30 tables, 0 exceptions;
   - maximal deck with latch-up: 0;
   - LVS (deep, `--disable_tap_extraction`): "Netlists match";
   - circuit check: equal to the s2d circuit plus the protection, apart from the dummies;
   - row check: 25 / 25, 0 edges DIFFERENT;
   - template: 0 drawing layers changed.
2. **Edge reserve, kept in full** on both sides over the buffer's height: no buffer device layers and no Metal1 in
   x 1.8–4.3 or 75.7–78.2 above y 31.7. Only Metal2 (and one Via2 / Metal3 strap) runs there, along the edge [M].
3. **Placement:** stage A as reviewed. For the reserve, `sinks_cmfb` moved by 2.5 µm and five other cells by up to
   2.5 µm. Three primitives got Metal2-only copies (`s2d_casc_n_f`, `s2d_loads_f`, `s2d_casc_p_f`), each DRC / LVS /
   sym_check clean [M].
4. **Routing** is C2's two-metal grid router (`generator.py`, copied unchanged): 39 nets, M1 1177 µm, M2 1542 µm,
   173 vias, no metal over any gate. Drawn by F:
   - the 12 tail-to-tub links;
   - one tap per supply group (one each for the tail and the sink source bus);
   - the NWell bridges;
   - one strap joining the two iovdd rails.
5. **PEX** (magic, mode 2) finds 28 capacitor-only nodes [M]: 26 rhigh heads (one per segment, dummies included)
   and the 2 rppd heads of the template. No routed net floats.

[M] = measured by a tool run, [R] = reasoning.
- Rebuild: `sh src/run_B.sh <inputs> <out> <out>`, 1 min; byte-identical from `out/src` [M].
- Checks: `sh src/checks_B.sh <inputs> <inputs_B> <out> <tmp>`, 3 min.
- Summary: `logs/summary_B.txt`.

## 1. The edge reserve as built (`logs/reserve_check.md`) [M]

- **Buffer shapes in the reserve:** 0.0000 µm² on the device layers (Activ, GatPoly, Cont, nSD, pSD, NWell,
  ThickGateOx, SalBlock, EXTBlock, PolyRes) and on Metal1.
- **Width kept**, per 1 µm band of y, from the template's edge strips (x 1.8 / 78.2) to the nearest buffer device or
  Metal1 shape: ≥ 2.50 µm everywhere on both sides; 8.2 µm where no cell stands.
- **Metal2 in the reserve:** left 85 µm², right 39 µm². All of it runs vertically along the edge, except one short
  horizontal piece at y 162.7–163.0 on the left, into cload's ring.
  - Left: the output trunk outp / outn, vin = pad, vref / vcm.
  - Right: vbn / vbnc / vbpc, the iovdd_tp feed and tap, and the iovdd rail tie; also 0.22 µm² of Via2 and 1.44 µm²
    of Metal3 (tap pads).
- **What moved** (placement in `previews/placement_B.tsv`):
  - `sinks`: x 1.80 → 4.30. The vin channel C1 between sinks and casc_n narrows from 4.3 to 1.81 µm; it carries y.
  - `casc_n`: x 22.60 → 22.62.
  - `sinks_cmfb`: x 61.69 → 59.19 (right edge 78.2 → 75.7).
  - `tree_n`: x 53.90 → 51.49.
  - `cload`: x 2.30 → 4.30.
  - `pd_p`: x 33.0 → 35.0.
- **Keep-outs:** the router's M1 keeps out of the reserve. The reserve has no taps, wells or bridges; the tap pads
  there are M2 / Via2 / M3 only.

## 2. Changes to the primitives and to stage A

| cell | change | checks [M] (`cells/logs/`) |
|---|---|---|
| `s2d_tails_hi_f` / `_lo_f` (stage A) | unchanged since stage A (approved: "Great choice to split the tails!") | as stage A |
| `s2d_casc_n_f` | the xc (M2 y −1.44..−1.15) and yc (11.10..11.39) levels run on to the band end, with M2 pins. Under R270 the band end is at the top, so all of casc_n's nets leave at the top. Mn.b 0.21 to the neighbors | DRC 0, maximal + LU 0, LVS match, sym 0; XOR vs N: only 10/0, 10/2 |
| `s2d_loads_f` | the lp / dd / ln pin tracks (0.20 at 0.41 pitch) fan out beyond the pin edge: the middle one straight to −1.6, the outer two jog 0.6 out. Needed because the router's 0.29 landing could not reach the middle track (measured: loads.dd enclosed) | DRC 0, maximal 0, LVS match, sym 0; XOR: 10/0 only |
| `s2d_casc_p_f` | the same fan-out for dd / ln / lp and voutp / vcmfb / voutn (casc_p.voutp was enclosed) | DRC 0, maximal 0, LVS match, sym 0.2688 µm² (P's Cont residual, unchanged); XOR: 10/0 only |
| `sinks_6x6_s2d_c3_core`, `s2d_sinks_cmfb_c3_core` | N's unturned cores placed directly (R270 / R90 = N's R90 wrapper turned). The router reads pins of the placed cell only, and N's pins are in the cores | N's own |

No device layer of any primitive changed. P's tub labels are stripped in the router's copy (labels only, as in C2).

**Block-level wiring drawn by F** (`src/make_pwr.py`, cell `pwr_f`):
- **Tail-to-tub links.** All 12 have one shape (rule 2: short, equal).
  - Each tub source pin runs on 1.05 µm in M1, then one Via1 and an M2 jog onto the tail drain pin.
  - The tub pitch is 6.10 against a tail pitch of 5.25, so the jog offsets are −2.125 + 0.85 k µm.
  - The upper and lower junctions are mirror images about the tubs' center line (y 135.62).
- **Taps.** One per group; each is an M2 pad + 2 Via2 + an M3 pad into the rail above.

  | group | members | rail | tap at |
  |---|---|---|---|
  | `iovdd_t` | tail source bus (both rows) + the inputs' dummy tubs | iovdd 93.5–119 | (51.5, 112.0) |
  | `iovss_sk` | sink source bus | iovss 7–32.5 | (12.5, 32.15) |
  | `iovss_cn` | casc_n | iovss 34.5–60 | (39.6, 50.0) |
  | `iovdd_op` | casc_p, loads, CYC drains | iovdd 66–91.5 | (72.95, 70.0) |
  | `iovss_m` | sinks_cmfb, rhigh, tree_n, cload | iovss 126–134 | (65.5, 126.5) |
  | `iovdd_tp` | tree_p, pd_p | iovdd 93.5–119 | (76.95, 117.5), in the reserve, M2 / Via2 / M3 only |

- **NWell bridges.** Four, from the tail rows to the inputs' all-vdd dummy tubs. The tail rows thus share one iovdd
  well with the dummies, and stay NW.b1 1.80 from the active tubs.
- **iovdd rail tie.** One M2 strap (x 76.55–77.35, y 90.2–95.2) with two Via2 pairs joins the M3 iovdd rails 66–91.5
  and 93.5–119.
  - Without it, the cell holds two iovdd nets [M: LVS found the tails / inputs / tree_p group on a second iovdd net].
  - In the IO ring they meet anyway [R]. The schematic needs no change.
- **Post-route trim** (`src/fix_block.py`). The router's landing squares on the inputs' gate band stuck out 0.015 µm
  and left 0.205 µm (M2.b, measured). The trim clips the slivers inside the band gaps: 2 pieces, 0.0087 µm².

**Pad level** (`src/build_pad.py`):
- The template's drawing layers are untouched [M].
- Port texts on 10/25, with pin boxes on 10/2, for the seven core pins at y 180: vref 11.9, outp 17.5, outn 23.9,
  vcm 30.0, en_3v3 36.6, en_3v3_b 47.8, iref 53.5.
- iovdd / iovss / vdd / pad keep the template's texts and its rail pins.
- The template's two top `vss` texts (30/25, 50/25) are removed (C2's lesson).
- Inside the block, the local vdd / vss / group texts are renamed iovdd / iovss.

## 3. Floorplan and routing (pictures: `previews/pad_candidate*.png`, reserve hatched)

The placement is stage A's, routed bottom-up. Long nets [M] (`logs/route.txt`):

| net | M2 | M1 | why |
|---|---|---|---|
| vbp | 224 µm | | tree_n → both tail rows' right stubs and tree_p |
| vbnc | 150 µm | | top right → casc_n in the left pocket |
| vbn | 112 µm | | → sinks and sinks_cmfb |
| pad (vin) | 108 µm | 18 µm | strap → along y 30.6 → left reserve → the band's vin pin |
| outp / outn | 66 / 75 µm | 66 / 65 µm | band ends → inputs' vfbp / vfbn → cload, pd_p → pins |

- x / y and xc / yc are 50–70 µm in total.
- The router keeps metal off every gate (keep-out over Activ & GatPoly + 0.1 µm, as C2).
- It does run M1 / M2 over rings, source / drain stripes and rhigh bodies.

## 4. Checks [M] (`logs/`)

| check | result | log |
|---|---|---|
| run_drc.py --no_density (pad) | No DRC violations, 30 tables, 0 "exception" | pad_run_drc.log |
| sg13cmos5l_maximal.drc -rd latchUpRules=true (pad) | 0 errors | pad_maximal_lu.log |
| LVS deep --disable_tap_extraction vs pad_candidate.cdl | Netlists match; all 14 cell circuits match | pad_lvs.log, pad_lvs_report.txt, pad_candidate.lvsdb |
| circuit check (non-dummy devices vs s2d circuit + protection) | EQUAL apart from the dummies; a copy with one tub gate moved: DIFFERENT | circuit_check.txt |
| row_check.py | 25 of 25 bands / rails pass, 0 edge layers DIFFERENT | row_check_B_*.md |
| template part (XOR) | 0 drawing layers differ; 10/2 port pins added; two vss texts removed, seven core-pin texts added | template_unchanged_B.txt |
| reserve | 0 µm² of buffer device layers / M1 in it | reserve_check.md |
| PEX, capacitor-only nodes | 28 = 26 rhigh heads + 2 rppd heads | pex_capacitor_only_nodes.txt |
| changed cells | DRC 0, maximal 0, LVS match, sym as in section 2 | cells/logs/summary_B.txt |

**Rounds:**
- **Routing** failed at first on 4–7 nets per run, for three reasons:
  - enclosed pins, fixed by the fan-out copies;
  - congestion, fixed by the route order (one reorder round);
  - L-shaped link labels, whose bounding-box pin produced dangling vias, fixed by pin boxes.
- **The first pad DRC** found 4 × M2.b and 3 × M2.c1. The trim and the pin boxes fixed them. One intermediate trim was
  too wide (20 × M2.d) and was narrowed.
- **LVS** failed twice:
  - the block's supplies were split by hierarchy, so s2d_block is now flattened against the pad subckt;
  - then the second iovdd rail, fixed by the rail tie.

**PEX method,** as C2 F2: `sak-pex.sh -m 2`, then the repo's `scripts/cace/pex_for_sim.py --tie`. The 26 rhigh nodes
sit on the strips' top heads (R0 y 12.65), one per strip including the two dummies. Every rhigh device has both
terminals on routed nets [R, from the netlist lines].

## 5. Open points for the lead and Christoph [R]

1. **vbp is 224 µm of M2.** It is a DC bias line on the tail gates, routed by the grid router. A shorter dedicated path
   could follow the right channel. Not changed.
2. **vin (pad) runs about 125 µm** up the left reserve, beside the output trunk. Output and input lines run in
   parallel at ≥ 0.21 µm, which couples them by roughly 10 fF [R, estimate]. The straight C1 path would be shorter
   only by the detour around tails_lo.
3. **R feeders.** Their vertical parts are mirror-symmetric (R is centered on the tubs). The horizontal parts differ
   per unit, because of the common-centroid columns; equal lengths would need meanders.
4. **magic LVS** will show the accepted vss / iovss pin merge, as in d2s (C2_report §4.3).
5. **Secondary protection** is still left out. A free piece of 14 × 22.7 µm (x 4.3–18.3, y 82.7–105.4) lies near the
   start of vin.
6. **The router** came from the notes checkout (`oa_core_pd_v2_2026-10-28/v2/generator.py`, read-only, sha256
   cea21b865695), copied unchanged into `src/` (messages.md, point 6).
