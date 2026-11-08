<!-- SPDX-FileCopyrightText: 2026 Christoph Maier / SPDX-License-Identifier: Apache-2.0 -->
# pad_ref_rb, placed and routed (Claude, agent F, C4, 2026-11-07, 22:24-22:45 CET)

[M] = tool result, [R] = reasoning. Placement and routing in one process (lead's messages): the grid router drove the
placement over four candidates. Rebuild: `sh src/all.sh <inputs> <out> <work>` (50 s, byte-identical rebuild [M]).

## Result [M] (`logs/summary.txt`)

| check | result |
|---|---|
| run_drc.py --no_density (pad_ref_rb) | No DRC violations detected, 0 "exception" lines |
| sg13cmos5l_maximal.drc -rd latchUpRules=true | 0 errors |
| LVS flat, --disable_tap_extraction, vs `pad_ref_rb.cdl` | Netlists match |
| negative LVS test (BA's gate moved m -> gh in the reference) | Netlists don't match: the comparison is not vacuous |
| metal-only connectivity (`metal_conn.py`; LVS joins vss rings through the substrate) | 16 nets, 0 split |
| rows vs delivered cells, all layers (`row_xor_vs_inputs.txt`) | 8 of 9 identical; bypass_rb replaced by bypass_rb_f |
| sym_check of every placed row (`sym_check.txt`) | 0, except rb_tree_p Cont 0.0384 (P's known PCell residual) |
| bypass_rb_f alone (`cells/logs/`; sym in `logs/sym_check.txt`) | DRC 0, maximal + LU 0, LVS match, sym 0 (both axes) |

`pad_ref_rb.cdl` is composed by script (`compose_cdl_rb.py`) from the circuit files `pad_ref_rb.spice`,
`vcm_rb.spice`, `vref_s2d_rb.spice` (bypass_rb ncm 4, ncr 9; vdd / vss -> vddh / vssh): 63 devices = 43 active (the 30
of the three blocks + 4 CBM + 9 CBR) + 20 dummies, the counts of `cdl_vs_circuit.txt` with ncr 9 [M].

## Area [M]

85.22 x 86.27 um = 7352 um2 (the 85 x 85 estimate: 7225). Cells 4788 um2 (65 %): the delivered 4772 with bypass_rb
2133 -> bypass_rb_f 2149. Candidate 2 (bypass 3 x 4) was 77.72 x 99.16 = 7707 um2 with an 18 x 40 um empty corner.

## Placement (bottom to top; orientations KLayout's; reasons in `routing_plan.md`)

- bypass_rb_f (R0) over the full width; rb_casc (M0: vref top left, xp top right, vbnc / vdd left).
- rb_tree_p (R180) abutting rb_tails (R180): the vbp stubs meet, one NWell [M]; rb_tails under rb_tubs, TR under MR,
  BT under BA / BB.
- rb_mirror (R180, bd / vcm low on its right edge) | rb_tubs (M90: D BB BA MR D) | rb_avg (R0, gh top, xp bottom).
- rb_cload (M0, pins down, over the mirror: vcm, en_3v3_b) | rb_tree_n (R180, pins down, gh over the tubs' gh).
- Pins: vref, vcm, en_3v3, en_3v3_b, iref on Metal2 at the right edge, bottom to top at 1.08 um pitch, y 77.76 ..
  82.08 (centres); vssh / vddh: Metal2 rails 1.0 um wide on the left edge, full height (`frame_f`).

## Changes to the rows

- **bypass_rb -> bypass_rb_f**: N's own generator (`inputs/N/build_rb_n.py --bypass 4 8 2 6`, unchanged), 2 rows x 6
  columns instead of 3 x 4. Same 12 capacitors (4 CBM on vcm, 8 CBR on vref, 12u/12u hv NMOS, S = D = B = vss), same
  unit, columns, ring and buses; 79.22 x 27.13 um. Why: as wide as rb_casc, 12.9 um lower, no empty corner. LU 2 rows.
- No other row changed (XOR 0 on every layer [M]); only the texts vdd / vss became vddh / vssh (`finalize.py`).
- No device added, removed or re-tied; the CDL is the circuit netlists as they stand: nothing to backannotate.
- Rule 9: the small switches stay in their rows' rings [R]: moving TGN / TDN / TGP out would not shorten any route
  here (their pins are at the row ends, next to the channels that carry ni / en_3v3_b / iref).

## Routing

- C2's grid router `generator.py`, copied unchanged from C3 F (`src/`); config `src/rb_cfg.py` + `src/rb_place.py`.
  Pitch 0.27, wire 0.29 um, M1 horizontal / M2 vertical preferred, M1 / M2 only, no metal over any gate (0 um2 [M]).
  All 16 nets routed in the first round [M]: M1 375 um, M2 265 um, 55 vias.
- Drawn by F: one Metal2 strap (x 2.6 .. 4.25, 0.29 um, the track's width) from the vddh rail to rb_casc's vdd pin.
  A router landing there had filled the gaps between rb_casc's vdd track and the three dummy tracks tied to it (same
  net) into one plate wider than 0.3 um, 0.21 um from vbnc: M2.e (first DRC round [M]).
- Port strips on the right edge, each open only to its own net (otherwise nets ran along the edge past the ports).
- Net lengths M1 / M2 in um [M]: ts 0 / 3.7, bt 0 / 3.9, gh 0.5 / 7.3, vbnc 6.3 / 5.3, bd 17.2 / 0.8, m 17.7 / 1.1,
  vbp 5.4 / 21.9, ni 11.3 / 20.2, xp 1.9 / 32.5, en_3v3 13.5 / 0.3, iref 54.3 / 24.1, en_3v3_b 68.6 / 34.9,
  vref 61.6 / 47.2, vcm 79.9 / 56.8, vddh 20.0 / 4.5, vssh 16.7 / 0.
- Supplies: each ring / vdd track is one router terminal, so each row is tapped once [R].

## Position in slot7 (`previews/context.png`)

Proposed lower left (446.78, 20.0): the cell spans x 446.78 .. 532.00, y 20.0 .. 106.27, 1.15 um left of the frame's
M2 vss_1v2 strip (x 533.15) and below y 112. Its pins then sit at x 531.70 .. 532.00, y 97.75 .. 102.08 [M], 10 .. 57
um below the S2D pins (vref 112.26 .. iref 159.51), in the same order; vcm also goes on to the D2S vref at 223.34.

## Open points [R]

1. vcm (137 um) and vref (109 um) are the longest nets: four cells each (bypass, cload, mirror / tubs; casc, tree_n),
   DC outputs with the bypass on them; the wire resistance (tens of ohms, not extracted) is far below their source
   impedance (vref about 20 kOhm). PEX not run.
2. The top-level routes to the S2D / D2S pins and the supply hook-up (slot vdd_3v3 / vss_3v3 or pad iovdd / iovss) are
   not in this cell; vddh / vssh rails are on the left edge, away from the signal pins.
3. bypass_rb_f's shape (2 x 6) is F's choice under the new latitude; N's 3 x 4 fits the same placement with a 13 um
   taller cell (candidate 2, also clean).
4. rb_tree_p's TGP and rb_tree_n's TGN / TDN stay in their rings (rule 9 optional).
