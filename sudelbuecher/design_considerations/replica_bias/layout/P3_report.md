<!-- SPDX-FileCopyrightText: 2026 Christoph Maier / SPDX-License-Identifier: Apache-2.0 -->
# P3 (C4): rb_avg with abutted gate poly (2026-11-07)

Claude, agent P3. [M] = measured by a tool run, [R] = reasoning. Files in `layout_rb/P3/out/`.

## Layout: two wells, one row each, gate poly abutted, gates contacted only at the row ends

```
upper row, NWell gh:   DU0 | SU | DU1          gate strip m    (SU  m m gh gh)
lower row, NWell m:    DL0 | SL1 SL2 | DL1     gate strip xp   (SL1, SL2  xp xp m m)
```

- **Rows.** Both rows are built by one function from C3's `rows()` and `gate_cols()` (`build_s2d_p3.py`, imported
  unchanged from `P/out`; no edits there).
  - The finger is the pad's 1/4 PCell, rotated (W along x). Neighbors' Activ are 0.25 apart (Gat.b1), so their end caps merge into one gate strip.
  - Each strip is contacted only by the full-width gate columns at its two ends, with no center contact.
  - Dummies are the same finger, extending the strip, so their gate is connected by abutment.
- **Wiring, per row:**
  - the sources go up under one M1 plate into the tie;
  - each dummy's drain goes up over its own channel into that plate, so dummy D = S = B = the well's net;
  - the active drains go down onto an M1 bar that runs into both gate columns (the diode);
  - the upper bar (m) drops straight onto the lower row's tie strip (m) across the 1.80 NWell gap (NW.b1).
  - M1 only: no M2 and no Via1.
- **Tie.** The ring is open on the drain side:
  - top strip 0.21 from the source Activ (pSD.c 0.18 + pSD.d1 0.03, as the pads' ring strips);
  - side strips at RG 0.80, the pads' ring distance.
  - The drain side stays open, so the bars leave without crossing a ring and no M2 is needed. The rules allow this: "a tap ring is optional and needn't be rectangular".
- **The butted tie (brief item 4)** is no longer an issue: with the fingers rotated as in the pads' rows, the tie sits 0.21 from the source end of the Activ. A butted tie would lengthen the source diffusion, which changes the finger's LOD and adds Activ to the PCell's device, so I did not use one.
- **Precedent followed:** the pads' `s2d_loads` / `s2d_casc_p` rows.
  - Their row ends already hold this exact 1/4 finger: the "X" end dummies, with gate by abutment and a gate column.
  - `casc_p`'s BPC is a 1/4 diode whose drain lane runs into its own gate column.
  - The tub supplied the rule of one well per bulk net, with bulk = source.
  - I did not use the OA-core layouts or the biasgen Magic layouts.
- **Rows translated, not mirrored, about the line between them [R].** This departs from rule 1's "two-row array mirror-symmetric".
  - SU is alone in its row. Mirroring would give SU the opposite current direction (source to drain) from SL1 / SL2, a systematic mismatch.
  - Translating also puts the shared net m in the gap: upper bar to lower tie.
- **Shared diffusion between SL1 and SL2 was not used [R].** The circuit would allow it (one drain xp), but SU cannot share diffusion with rail-tied dummies. Sharing would therefore give SL1 / SL2 a different LOD from SU, which defeats item 2.

## Checks [M] (round 1 had one finding, fixed in round 2; logs in `out/logs/`)

| check | result |
|---|---|
| DRC `run_drc.py --no_density --mp=4` | "No DRC violations detected", no "exception" |
| LVS `--disable_tap_extraction` against `rb_avg_v3.cdl` | PASS, 0 warnings |
| sym_check (X axis; rb_avg, rb_avg_u, rb_avg_l) | max mirror XOR 0, 0 narrow-poly hits, all three |
| LU (`lu.py`) | 3.07 µm (LU.a 20) |
| surround XOR, ±1 pitch (1.25 µm) | SL1 vs SU and SL2 vs SU: **0.0000 µm²** on every device layer (Activ, GatPoly, Cont, pSD, NWell, TGO), over the full row height |
| surround XOR, ±2 pitches | 11.12 µm², as expected: SU's second neighbor is the gate column, SL1's is a dummy or finger |
| finger vs pad `pmosHV_w1_l4$1` | XOR 0 on all layers |
| row ends (gate column + end dummy) vs pad `s2d_loads_f` lower row ends | XOR 0 on Activ, Cont and pSD. GatPoly 0.119 µm²: the pad's poly bridge between its two rows |
| reproducibility | two builds byte-identical (gds 58cfd3f1822d) |

- **Round 1 finding:** Cont XOR 0.178 µm² at ±1 pitch. The tie contacts had been centered over each strip, and the upper and lower strips have different lengths.
- **Round 2 fix:** three tie contacts placed over each finger's Activ.
- The LVS extraction merges the parallel devices; the CDL lists every finger.
  - extracted: SL1 ‖ SL2 `xp xp m m` W=2
  - extracted: SU `m m gh gh` W=1
  - extracted: DU0 ‖ DU1 `gh m gh gh` W=2
  - extracted: DL0 ‖ DL1 `m xp m m` W=2

## Size

| layout | size | area | relative to P r2 |
|---|---|---|---|
| this rb_avg | 8.19 × 14.66 µm | 120.1 µm² | 1.01 |
| P r2 (`D SL1 SU SL2 D`) | 36.80 × 3.23 µm | 118.9 µm² | 1.00 |
| README estimate | | 124 µm² | 1.04 |

- The pads have no counterpart cell.
- With the tie as a top strip only (no side strips) the cell would be 5.99 × 14.66 = 87.8 µm² (0.74 of P r2). I kept the ring because of "taps as rings where space allows".
- The cell can be rotated by 90° if F wants it flat (14.66 × 8.19 µm).

## Dummies for backannotation (they replace XMDA[1:0], all on vdd, in vcm_rb)

All four are hv PMOS 1u/4u, ng=1 (d g s b):

| CDL name | d g s b | position |
|---|---|---|
| MDU0, MDU1 | `gh m gh gh` | both ends of SU's row, in well gh |
| MDL0, MDL1 | `m xp m m` | both ends of the SL row, in well m |

Suggested netlist lines: `XMDAU[1:0] gh m gh gh` and `XMDAL[1:0] m xp m m`. The dummies conduct no DC current (S = D). They add gate capacitance:

- m to gh: 2 × 1u/4u;
- xp to m: 2 × 1u/4u.

No change of W, L, ng or device count for SU, SL1, SL2.

## Pins (cell frame, µm; ports `rb_avg gh m xp`; no vdd any more)

| net | layer | box | where |
|---|---|---|---|
| gh | M1 | (3.595,14.36; 4.595,14.66) | top edge, the upper tie |
| m | M1 | (0,5.51; 0.30,5.81) and (7.89,5.51; 8.19,5.81) | both side edges, the lower tie strip |
| xp | M1 | (3.595,0; 4.595,0.21) | bottom edge, the lower bar |

## Open questions for Christoph

1. Do you accept the translated row pair, with all three diodes in the same current direction, instead of the mirrored pair under rule 1?
2. Should the tie keep its side strips (U ring, 120 µm²), or be a top strip only (88 µm²)?

## Files (`P3/out/`, sha256 first 12)

- 58cfd3f1822d `rb_avg_v3.gds`: top cell rb_avg, subcells rb_avg_u, rb_avg_l and rb_pmosHV_w1_l4
- 71e5fe73e1a9 `rb_avg_v3.cdl`
- a92d81fedadf `build_rb_avg_v3.py`
- `rb_avg_v3.png`, `rb_avg_v3_lower_end.png`
- `logs/`:
  - `check.sh`
  - DRC / LVS logs and the extracted netlist
  - `sym_*.txt`, `lu_*.txt`
  - `surround_v3.py` and its output
  - `compare_pad_v3.py` and its output
  - `repro.txt`, `build_stdout.txt`
