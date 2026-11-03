<!--
SPDX-FileCopyrightText: 2026 Christoph Maier
SPDX-License-Identifier: Apache-2.0
-->
# F stage A: the s2d buffer placed in pad template v4, unrouted (C3, 2026-11-03, 21:37–22:05 CET)

Agent F (Claude Opus 5.5). [M] = tool result, [R] = reasoning. Pictures in `previews/`, logs in `logs/`, `cells/logs/`.
Rebuild: `sh src/run_A.sh <inputs> <out>`, checks: `sh src/checks_A.sh <inputs> <out> <tmp>`; two builds are byte-identical [M].

## Arrangement (bottom up, from the drawn cells; `placement_A.tsv`)

- **Left pocket, NMOS fold:** `sinks` (R180, pins up) | channel C1 (above the pad pin strap) | `casc_n` (R270, band and x / y pins up).
- **Right pocket, PMOS output stage:** `casc_p` | `loads` (R270, pins up), abutted: one NWell.
- **Input group:** `tails_lo` (M0) / `inputs` / `tails_hi`, each tail row facing its own tub row (column map aligned);
  `rhigh` (R90) to the right, its pin bank centered on the tubs (both at y 135.62).
- **Fold and output links:** `sinks_cmfb` under R, at the tubs' xc / yc corner and above the loads.
- **Bias tree:** `tree_n` beside `tails_hi` (on its new right vbp stub), `tree_p` above it (on iref / ni).
- **Top:** `cload` + `pd_p` under outp / outn; the output trunk runs C2 → pins past them.

## Area per block (`logs/stats_A.md`) [M]

| block | cells as delivered µm² | as placed µm² | block bbox µm² |
|---|---:|---:|---:|
| input group (inputs, tails, rhigh) | 2360 | 2472 (tails split: +112) | 3619 |
| NMOS fold (sinks, casc_n) / sinks_cmfb | 1887 / 532 | 1887 / 532 | 2593 / 532 |
| PMOS output stage (casc_p, loads; one NWell) | 1201 | 1201 | 1313 |
| cload + pd_p / bias tree (tree_n, tree_p) | 430 / 357 | 430 / 357 | 483 / 542 |

Compaction is in the placement: abutted wells, both pockets used, channels sized to their nets [R]. No primitive got
smaller. The fit (variant A) needed 7689 µm² of library cells 2 µm apart, up to y 178.3; here the cells take 6881 µm²,
up to y 176.74, with the channels reserved.

**Bounding box and free area [M]:** the block spans x 1.80–78.20, y 31.70–176.74. The free region (template minus
keep-outs) is 10695 µm²; the cells cover 6881 (64 %). Of the 3814 µm² left, 2100 lie in the channels and 1714 elsewhere.
Largest pieces: x 4.3–18.3 × y 82.7–105.4 (319 µm²), x 31.9–60.0 × y 164.3–172.3 (225), x 55.5–75.6 × y 145.2–152.3 (142).

## Wiring channels (M1 / M2; dashed yellow in the pictures) [R]

Widths: nets × 0.48 µm (0.26 track + Mn.b 0.21, P's TP; rule line 1496); in M1 × 0.38 (0.20 + M1.b 0.18, line 1433).

| channel | where (µm) | width | carries (need) |
|---|---|---:|---|
| C1 | x 18.31–22.60, y 32.7–110.2 | 4.29 | vin (pad strap → tubs' vin track by M1 in a well gap), y (1.0; the rest is the packing gap) |
| C2 | x 1.80–4.30, y 82.7–176.7 | 2.50 | voutp / voutn trunk (band → vfbp / vfbn, cload, pd_p, outp / outn), x / y, vref / vcm (≤ 4 per level: 1.9) |
| C3 | y 105.4–110.2 over casc_n; x 37–61.7, y 97.8–105.4 | 4.8 / 7.6 | casc_p band ↔ casc_n band, x y xc yc, vbnc (≤ 8: 3.9) |
| C4 | x 58.31–61.69, y 88.8–122.4 | 3.38 | lp / ln / dd (loads ↔ casc_p tops), xc / yc (5: 2.4) |
| C5 | y 119.4–122.4 and 148.8–151.8 | 3.00 | 6 tail-to-tub verticals (M2 jogs ≤ 2.1: pitches 5.25 / 6.10) + 6 M1 feeders to R (2.3) |
| C6 | x 51.88–55.50, y 119.4–151.8 | 3.62 | R feeders, ≤ 6 in parallel between R's two banks (2.9) |
| C7 | x 75.59–78.20, y 91.3–164.3 | 2.61 | vbn, vbnc, vbpc from the tree down to sinks_cmfb, sinks, casc_n, casc_p (1.4) |
| C8 | y 176.74–180, full width | 3.26 | the 7 core-side M2 pins and their spread (≤ 6 tracks) |
| C9 | x 36.97–42.35, y 38.2–97.8 | 5.38 | casc_n's right long side (taps of its full-length x / yc levels), vbn to the sinks |

M3 is free only at y 119–126 and 134–140, both over the tubs: crossings for vref / vcm or the R feeders.

## Isolator (rule 5)

- [M] Sinks stand 1.6 µm and casc_n 2.6 µm above CN's outer NWell ring; the casc_p / loads NWell starts 6.6 µm above
  CP's outer p+ ring. LU.a / LU.b (lines 2356 / 2358, 20 µm): `sg13cmos5l_maximal.drc -rd latchUpRules=true` 0 and
  run_drc.py (30 tables, latchup among them) 0.
- [R] Guideline 7.2.1 items 3–5 (lines 2326–2334) ask for double rings (N-Well isolator + P+ isolator) between
  pad-connected devices and the internal circuit. CN and DN carry both (CN inner p+ / outer NWell, DN p+ anode frame /
  NWell guard); the left-pocket NMOS cells sit behind them with their own p+ rings. CP / DP carry their outer p+ ring,
  and the cells above them are PMOS in iovdd NWell with closed n+ rings (casc_p, loads): the N-Well isolator.
  So no extra isolator is needed and no room is reserved. For IOPadAnalog's p+ plate anyway, the pocket cells can rise
  2 µm (C3 keeps 2.8 µm; the top has 3.26 µm of slack).

## Changes to P's / N's cells (`cells/s2d_tails_f.*`, `src/build_f_tails.py`, built with P's own helpers)

- `s2d_tails_c3` → `s2d_tails_hi_f` (BP A1a F2b F1b A2a M1a M2b D) + `s2d_tails_lo_f` (D A2b F1a F2a A1b M1b M2a D),
  45.19 × 9.16 µm each; rule 2: every tail drain faces its tub.
- Unchanged: P's rows, PCells, gate columns, drain pads, BP lane, dummy ties; Activ and Cont XOR 0 against P's cell in
  the row windows [M] (`cells/logs/row_xor_vs_P.txt`).
- Changed: P's row-to-row poly bridge stubs go; each row gets its own vdd plate into the ring's top strip, 0.43 above
  the source Activ (pSD.i1 0.40 + pSD.d1 0.03, lines 1142 / 1134); one closed n+ ring and one NWell per row (NW.c1 /
  NW.e1 0.62, lines 774 / 779); vbp edge stubs at both row ends.
- [M] per cell: run_drc.py (--no_density, 0 exceptions) clean; maximal with latch-up 0; LVS
  (--disable_tap_extraction) "Netlists match"; sym_check (--no-y) XOR 0, 0 necks. The rows are M0 images about the
  tubs' center line [R]. Possible conflict with "no taps between rows": `messages.md`, point 2.
- No other cell changed. `s2d_pd_n_c3` is not placed: its devices are inside `s2d_cload_c3`.

## Checks of `placement_A.gds` (`logs/summary.txt`) [M]

Template part XORs empty against the input template on every layer. run_drc.py: "No DRC violations detected" (30 tables,
0 "exception" lines); maximal with latch-up 0. row_check: 25 of 25 bands / rails pass (as on the template alone), 0 edge
layers DIFFERENT (`messages.md`, point 1).

## What stage B needs [R]

- Taps at one point each (§6): strap the two tail rows' plates / rings together, tap iovdd once; the sinks' ring (sink
  source bus) to iovss once.
- casc_n exits: R270 puts its xc / yc pins at the bottom. Add M2 exits at the top of its long sides, where xc and yc
  have full-length levels (`casc_n_f`, with sym_check).
- NWell bridges from the tail rows to the inputs' all-vdd dummy tubs (NW.b1 1.80 to the active tubs, line 772).
- vin: pad strap → C1 → M1 in a tub well gap → vin track.
- Secondary protection: not reserved; the free piece x 4.3–18.3 × y 82.7–105.4 lies on vin's path and fits C2's
  7.86 × 14.72 µm stage.
- Then pad-level LVS (deep), PEX element counts, row DRC.
