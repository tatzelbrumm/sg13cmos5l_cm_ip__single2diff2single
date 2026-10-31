<!--
SPDX-FileCopyrightText: 2026 Christoph Maier
SPDX-License-Identifier: Apache-2.0
-->
# P2: PMOS primitives of d2s_mpdda_pd / bias_tree_pd, rebuilt (C2, 2026-10-31 20:08–20:30 CET)

Saved by the lead from P2's final reply (the harness did not let the agent write `out/report.md`); P2's text, unchanged
except for this header line. The lead's check: `design_considerations/pad_buffer_layout/pad_cell_2026-10-31/lead_checks/P2/`.

Claude (Opus 5.5), agent P2. `build_d2s_p2.py` (run in `out/`, needs the PDK) writes the gds, cdl and PNGs; it is
byte-reproducible. [M] = measured by a tool run, [R] = reasoning.

## Checks (final round 3, all cells, logs in `logs/`)

| cell | size µm | DRC | LVS | sym_check | LU farthest P+ to tie (µm) |
|---|---|---|---|---|---|
| tub_p20x1_c2 | 5.32×11.24 | 0 | match | X 0, --no-y, 0 necks | 1.76 |
| d2s_inputs_c2 | 40.92×26.44 | 0 | match (deep) | X 0, Y 0, 0 necks | 1.76 |
| d2s_tails_c2 | 34.69×14.81 | 0 | match | X 0, Y 0, 0 necks | 16.31 |
| d2s_loads_c2 | 30.69×13.67 | 0 | match | X 0, Y 0, 0 necks | 4.90 |
| d2s_casc_p_c2 | 35.66×13.67 | 0 | match | X 0, Y 0, 0 necks | 4.90 |
| d2s_ab_p_c2 | 8.48×9.00 | 0 | match | X 0, --no-y, 0 necks | 7.46 |
| d2s_pd_p_c2 | 3.71×2.97 | 0 | match | X 0, --no-y, 0 necks | 1.45 |
| bias_tree_p_c2 | 18.19×9.32 | 0 | match | X 0, --no-y, 0 necks | 8.18 |

- [M] **DRC:** `run_drc.py --no_density --mp=4`. Every log says "No DRC violations" with 0 × "generated an exception".
  LU.a is in the maximal deck and logs no line of its own; a probe on the library's tap-less `d2s_pd_p` flags LU.a, so
  the rule is active.
- [M] **LVS:** `run_lvs.py --disable_tap_extraction`. `d2s_inputs_c2` is hierarchical (12 × `tub_p20x1_c2`) and matches
  with `--run_mode=deep`. In flat mode the circuit matches, but the tub labels give net names like `s,sa_B`, which
  flag_missing_ports counts as an error.
- [M] **sym_check:** axes are the Activ bbox centres (the ties are symmetric). Single-row cells run with `--no-y`.
- [M] **LU column:** from `lu.py` (ties are grown until they cover all P+ in NWell). LU.a limit = 20 µm
  (sg13cmos5l_tech_default.json LU_a).
- [M] **Device cells:** fresh SG13_dev pmosHV PCells, copied flat and unchanged. XOR is 0 against the library's
  pmosHV$1/$2/$3/$4/$5/$7/$8 and pmosHV.
- **Check rounds:** round 1 all cells; round 2 after the fixes, all cells except casc_p (unchanged); round 3 final, all.
- **Fixes between rounds:** tub PCell w = 10 → 20 (w is the total width), the gate bar now covers the third head contact
  (Cnt.h / M1.c); tie ring 0.69 → 0.80 from the end Activ, and the ab_p tie 0.63 → 0.80 (sym_check counts tie Activ, so
  the poly tab left between the two 0.25 µm zones was only 0.19 / 0.13 wide); pd_p en_3v3 Metal2 pad widened (M2.d,
  Mn_d 0.144 µm²).

## Symmetry [R]

The right half of every row is the M90 image of its left half, and the upper row the M0 image of the lower row. The
PCell's 5 nm contact flooring (W = 5, 6, 15) is therefore mirrored too. Dummies only come in pairs of the same cell.
Metal is asymmetric only where pins leave and at BP.

## Gate contacts [R]

- **Rotated rows** (tails, loads, casc_p, bias_tree_p): sinks_6x6 style. At both row ends a poly tab as long as the gate
  (L = 6/4/3/6), 0.60 beyond the Activ. One contact column 0.30–0.46 from the Activ (Cnt_e 0.14). Metal1 column 0.26
  wide (Via1 fits), 0.25 from the Activ.
- **Upright fingers** (tub, ab_p, pd_p, TGP): contacts on the gate heads, at full gate width (1.0/0.6/0.45), 0.56 beyond
  the Activ. Contact 0.18 above the Activ (log 17:43). One M1 bar (0.22, Via1 fits). The tub has 3 contacts per head.

## Cells (left→right; upper row over lower row)

**tub + d2s_inputs**
- Map `D|Aa C2b C1b Ba|D` over `D|Bb C1a C2a Ab|D`: 12 identical tubs (2 × 10/1, ng=2), each in its own NWell, wells
  1.80 apart (NW_b1).
- Tub: N+ ties left and right, 0.21 from the Activ (Act_b, pSD_c + pSD_d1). Each source plate is tie + stripe in M1; the
  two plates are joined by an M2 strap. The drain tab has 3 Via1.
- Gate heads face the band between the rows, with 5 M2 tracks: vinn vref vdd vfb vinp. Gate tabs have 2 Via1: lower row
  at the right of the bar, upper row at the left.
- x / y drain tracks run outside each row, joined by one M1 line per side. Source plates run to the outer edges as pins.
- Dummy tubs: g = d = s = well = vdd. Ties exist only inside each tub (bulk = source).

**d2s_tails**
- Map `BP|Aa C2b C1b Ba|D` over `D|Bb C1a C2a Ab|D`, all 5/6. BP is at one end with a full twin at the other end.
- Why the end position: the four matched columns stay contiguous, BP's drain goes straight into its own gate column,
  and BP's mismatch only scales all tails together (layout_primitives §3 P2).
- The sources face each other under one vdd plate, which runs out between the gate columns to ties at both ends. Drains
  go straight to the top and bottom edges (M2 pins, 3 Via1). There is no track band. vbp: the two rows' gate columns
  are bridged in M2.

**d2s_loads**
- Map `D|L R R L|D` over `D|R L L R|D`, 6/4 devices, 1/4 dummies at all four ends.
- Map change [R]: the 1-D map `L R R L L R R L` is folded into two rows, the second half reversed. Each column then holds
  one L and one R, so gradients cancel in x and y. Size 30.7×13.7 instead of about 58×9.
- Drains face the band, which holds tracks pl vdd l2 pr. L and R each get two short and two long tabs (3 Via1). The
  dummy drains share one strap onto vdd.
- The gate columns of both rows are joined in M1, with Via1 onto l2. Closed N+ tie ring.

**d2s_casc_p**
- Map `PCL BPC PCR` over `PCR D PCL`: 15/3 devices, BPC and D are 1/4. The common-centroid arrangement is kept.
- BPC sits on the axis with its twin dummy below it (gate vbpc, D = S = vdd). No end dummies (rule 1b).
- Band tracks: l2 vdd vbpc a. The pl / pr tracks run outside the rows, joined by one M1 line per side. Tie ring.

**d2s_ab_p**
- Map `D FPL RP2 ABP D`, all 6.66/0.6. The dummies have all terminals on vdd.
- RP2 sits between its two replicas, and its drain rises into the vabp bar. The tie is above the heads.

**d2s_pd_p**
- `SA SABP` (1/0.45). Sources are outside: vddo to the left edge, vdd into the tie below.
- Drains are in the middle, each with 2 Via1 to an M2 pin. No dummies.

**bias_tree_p**
- Map `PBNC PBN PABN D` (2/6, 5/6, 5/6, 2/6: the narrow device and its twin, as decided at 02:44).
- TGP (1/0.45) is centred below the source plate, gate head down.
- Drains go straight to the top edge (M2 pins). Ties at both row ends. Because TGP forms a second "row", sym_check runs
  with --no-y.

## Netlist changes (in the .cdl)

- PL/PR: w=24 ng=4 → 4 × 6/4 ng=1 each. PCL/PCR: w=30 ng=2 → 2 × 15/3 ng=1 each.
- Dummies added: tubs 4 (vdd), tails 3 × 5/6 (vdd vbp vdd vdd), loads 4 × 1/4 (vdd l2 vdd vdd), casc_p 1 × 1/4 (vdd vbpc
  vdd vdd), ab_p 2 × 6.66/0.6 (all vdd), bias_tree_p 1 × 2/6 (vdd vbp vdd vdd).
- BP and BPC are in these cells (layout_primitives §7 decision 4).
- SA bulk vddo → vdd.
- The input devices are X instances of `tub_p20x1_c2` (pins d g s).

## Pins (µm, cell lower left = 0,0; the tub's origin is its Activ corner)

- **tub:** g M1 (1.33,10.18;1.73,10.40); s M1 (−0.51,−0.62;0.23,−0.32); d M1 (0.975,−0.62;2.085,−0.32).
- **inputs:** bottom M1 (0.74×0.30, y 0) at x0: sb_B 7.74, sa_C1 14.86, sa_C2 21.98, sb_A 29.10; top, same x, y 26.14:
  sa_A, sb_C2, sb_C1, sa_B; left M2 (x 0–0.5, 0.26 high) at y0: vinn 12.12, vref 12.60, vdd 13.09, vfb 13.57, vinp 14.05,
  x 0.14; y: M2 (40.42,0.62;40.92,0.88).
- **tails:** M2 1.11×0.445 at x0: sb_B 8.915, sa_C1 14.165, sa_C2 19.415, sb_A 24.665 (y 0); sa_A, sb_C2, sb_C1, sa_B at
  the same x (y 14.365); vbp M2 (0,7.255;0.5,7.555); vdd M1 (0.62,1.12;0.92,3.12).
- **loads:** M2 at x 0–0.5, y0: pl 5.985, l2 6.945, pr 7.425; vdd M1 (14.345,0.62;16.345,0.92).
- **casc_p:** M2 at x 0–0.5, y0: pl 1.25, pr 1.73, l2 5.985, vbpc 6.945, a 7.425; vdd M1 (16.83,0.62;18.83,0.92).
- **ab_p:** bottom M1 (0.16×0.4) at x0: l2 2.18, l1 3.16, dabp 4.65, a 5.16, b 6.14; vabp M2 (4.09,8.60;4.39,9.00); vdd M1
  (3.24,8.08;5.24,8.38).
- **pd_p:** a M2 (1.47,0;1.68,0.30); vabp M2 (2.03,0;2.24,0.30); en_3v3 M2 (1.705,2.67;2.005,2.97); vddo M1
  (0,1.70;0.30,2.00); vdd M1 (1.355,0.62;2.355,0.92).
- **bias_tree_p:** top M2 (1.11×0.5, y 8.82) at x0: vbnc 2.165, vbn 5.915, vabn 11.165; vbp M1 (1.21,8.92;1.47,9.32);
  bottom M1: iref 8.50–8.76, en_3v3_b 8.965–9.225, ni 9.43–9.69; vdd M1 (0.62,2.52;0.92,4.52).

## Open points [R]

- The tails' farthest P+ is 16.3 µm from a tie, which is within the LU.a limit of 20 µm. The parent may still add ties.
- `d2s_inputs_c2` needs deep-mode LVS, because the tub keeps its own labels for its own LVS.
- PNGs: `<cell>.png` shows the full cell; `_row_end`, `_gate` and `_tgp` are close-ups.
