<!--
SPDX-FileCopyrightText: 2026 Christoph Maier
SPDX-License-Identifier: Apache-2.0
-->
# N2: NMOS primitives and R block of IOPadDiff2Single, rebuilt (C2, 2026-10-31, 19:05–20:20 CET)

Agent N2 (Claude Opus 5.5). `build_d2s_n2.py` (run in `out/`) writes `d2s_n2_cells.gds` / `.cdl`; byte-reproducible
(two builds, same sha256). `render_png.py` draws the PNGs. Logs in `logs/`. Measured = from a tool run; the rest is
reasoning and marked so.

## Common to every cell (answers to the 18:55 rejection)

- **Symmetry.** Every MOS is one unmodified SG13_dev `nmosHV` finger (ng=1), turned R270 (W along the row). Fingers
  right of the vertical axis are placed mirrored about their own centre: the PCell's contact column is not symmetric
  along W (0.005 µm grid steps; measured XOR with its own mirror: 6/6 0.0384, 4.4/1 0.0256, 15/3 0.1344 µm²), so
  mirrored placement makes each row an exact image. Two-row blocks: row 2 is row 1's image about the band.
- **Dummies.** The same narrow dummy (same L) at both ends of every row. Dummy D = S = G = gate net (Vgs = 0, no
  channel), both stripes bridged in M1 to the adjacent gate column: no strap and no metal over any matched channel.
- **Gate contacts.** Contact columns on a poly fill exactly as tall as the gate (L), at both row ends and, where the
  map needs gate access inside the row, in a 0.85 µm gap on both sides of the centre device. sym_check: 0 narrow-poly
  hits everywhere. Column M1 0.26 µm; Via1 sits on every column of the two-row blocks (DRC clean).
- **Drains:** 1.11 µm M1 tabs with 3 Via1 onto 0.29 µm M2 tracks in the band (row 1 tabs 0.75 µm left of the finger
  centre, row 2 0.75 right, so near and far tabs never meet; far tab to the other row's stripe = M1_e 0.22 exactly).
- **Taps:** p+ tie strips (Activ 0.30, one contact row) only at the periphery, 0.21 µm (Act_b) from the outer rows;
  none between rows; no NWell. ThickGateOx: one rectangle over all Activ + 0.27 (TGO_a).
- **Checks, all on the delivered GDS (logs/):** IHP `run_drc.py --no_density --mp=4`, 343 rules incl. LU.b and the
  maximal set: **0 violations in all 7 cells**, no "generated an exception". IHP `run_lvs.py
  --disable_tap_extraction`: **7 / 7 "Netlists match"** (extracted netlists in logs/: SX / SY 36/6, BN, BNC, chains
  50.6 µm). `sym_check.py`: three cells 0; residuals only on Cont of the one device sitting *on* the axis (table).
  One DRC finding during the work (Pin.e: pd_n gate pin box taller than its M1), fixed, everything re-run.

## sinks_6x6_c2 — 51.68 × 16.51 µm (v1 15.5 × 46.8; library 53.4 × 18.1)

```
row 2:  D | SY SX SX  T  SY SY SX | D        T = BN's twin (6/6 dummy), D = 2/6 dummy
        --- band: tracks y / vbn / x ---     mirror line
row 1:  D | SX SY SY BN  SX SX SY | D        map of §5 (X Y Y X X Y / Y X X Y Y X), split at its centre
```
- **BN in the middle of row 1** (rule 1, "middle"); its twin T, the same 6/6 device, mirrors it in row 2. Why: BN sits
  at the centroid of all 12 sink fingers, so linear gradients between BN and the sinks cancel (reasoning; at an end,
  as in v1 / the library, they don't). The 0.85 µm column gaps beside BN / T touch one X and one Y finger per row.
- Gate: 4 columns (2 ends, 2 centre), 17 contacts per row each, joined in M1 through the band, Via1 to the vbn track.
  BN's drain and T's stripes bridge to the left centre column, D's stripes to the end columns.
- Sources: M1 plates over the outer stripes into the bottom / top tie; the ties joined by two M1 joiners outside the
  end columns. Source bus = tie metal with **one vss pin** (bottom tie, left), the one point where the assembly
  connects vss (§6); it carries only the sink current. LU: farthest N+ Activ 6.89 µm from a tie (LU_b 20).
- Pins (left edge): x M2 (−0.72, 6.975), vbn M2 (−0.72, 7.475), y M2 (−0.72, 7.975), vss M1 (−0.61, −0.36).
- Finger count: `sinks(name, nf)` (nf per sink, even). nf = 24 (4×) builds, sym_check as for nf = 6 (one 162 µm row
  pair; not DRC'd). A real 4× layout would fold into 4 rows, and BN stays one finger (ratio 1:24): circuit decisions.
- **sinks_6x6_s2d_c2**: the same block turned R90 (16.51 × 51.68 µm, pins on the bottom edge), as v1's variant;
  DRC 0, LVS match. Assumption: the s2d pad uses the same netlist; a different one is an edit of `sinks()`.

## d2s_casc_n_c2 — 40.70 × 12.41 µm (v1 9.7 × 33.1; library 36.1 × 11.9; neither had dummies)

```
row 2:  D | CY  [ BNC ]  CX | D       D = 2/3 dummy; CX, CY one 15/3 finger each per row
        --- band: b / vbnc / l1 ---   BNC (1/8, turned like the rows, Activ 8.68 µm tall) spans both rows + band
row 1:  D | CX  [ BNC ]  CY | D       cross-quad CX CY / CY CX (Christoph 01:37)
```
- **BNC in the middle of the map**, on both symmetry axes, so it needs no twin: sym_check 0. Its gate merges with
  both rows' gate strips through the two centre column fills; drain bridged to the left centre column, source down
  to the bottom tie.
- Sources x / y on two M2 levels below row 1 and above row 2, joined by an M1 vertical left (x) and right (y). The
  band tracks l1 / vbnc / b cross BNC's channel in M2: the only metal over a channel in this delivery (l1 and b
  cross it equally). LU 5.64 µm.
- Pins: l1 / vbnc / b M2 (−1.23, 3.975 / 4.475 / 4.975), x M2 (−1.23, −0.295), y M2 (38.43, −0.795),
  vss M1 (−1.17, −1.31).

## d2s_ab_n_c2 — 20.68 × 4.02 µm (v1 6.9 × 5.4)

`D | FNL RN2 ABN | D` (4.4/1; D = 2/1 dummy). RN2 (diode) in the middle, FNL / ABN its mirror pair. Gate columns at
both ends (3 contacts each); a vabn M2 track above the row joins RN2's drain and both columns. Drains l2 / a up to M1
pins on the top edge; sources l1 / dabn / b down to M2 pins over the tie on the bottom edge. LU 2.33 µm. Pins: l2 M1
(4.45, 2.655), a M1 (13.75, 2.655), vabn M2 (−0.225, 2.06), l1 / dabn / b M2 (4.45 / 9.1 / 13.75, −0.85), vss M1
(−0.64, −0.795).

## d2s_pd_n_c2 — 4.73 × 2.95 µm

`SB SABN` (1/0.45, separate sources vsso / vss), no dummies (switches: rule 1 b). One gate strip, a contact column
at each end on a fill as tall as the gate (0.45). SABN's source plate into the tie; vsso drops in M2 over the tie.
LU 1.78 µm. Pins: b M1 (0.5, 1.58), vabn M1 (1.75, 1.58), en_3v3_b M1 (−0.33, 0.565), vsso M2 (0.5, −0.85), vss M1
(−0.625, −0.795). sym_check 0.

## bias_tree_n_c2 — 30.26 × 8.59 µm (library 27.4 × 11.1)

`[TGN] | NBPC NBP NI NABP D | [TDN]`: NI (diode) in the middle; NBPC (2.4/6) at one end, its twin D (2.4/6 dummy)
at the other (rule 1, twin at the other end; the library's choice of 02:44). TGN / TDN (1/0.45) are mirror images
outside the row's gate columns: TGN's ni stripe bridges to the left column, TDN's to the right one, TDN's source drops
to the tie; each switch has its own column on a fill as tall as its gate. ni M2 track above the row (NI's drain and
both columns). LU 6.89 µm. Pins: vbpc / vbp / vabp M1 (1.2 / 5.65 / 18.15, 7.655), iref M1 (−1.46, 7.655), ni M2
(24.025, 7.06; also needed by TGP in the PMOS cell), en_3v3 M1 (−2.29, 3.34), en_3v3_b M1 (26.09, 3.34), vss M1
(−2.6, −0.36).

## d2s_rhigh_c2 — 13.80 × 17.29 µm (library 14.76 × 17.50)

`dummy A B C1 C2 C2 C1 B A A B C1 C2 C2 C1 B A dummy` (§5), rhigh 0.5 × 12.65 µm at 0.68 µm pitch. Wired as bg_res_c:
Via1 on every head, M2 stub to a link level, M1 link along it; levels by interval colouring (4 top, 4 bottom). Each
resistor enters at the top head of its first segment and leaves at the top head of its last, so all 8 terminals are
M2 pins on the top edge: sa_A..sa_C2 (0.93 / 1.61 / 2.29 / 2.97, 14.74), sb_C2..sb_A (9.09 / 9.77 / 10.45 / 11.13,
14.74). Ties: one strip each side, Activ 0.54 µm from the strips (EXTB_c, as the library), as tall as the block and
centred on it; dummy heads strapped into them in M1 (Christoph 21:22). vss M1 (−0.69, 6.325). sym_check 0 in x and
y. No N+ Activ, so no LU distance. LVS reduces each chain to one 0.5 / 50.6 µm device.

## sym_check residuals (measured, logs/sym_check.txt)

| cell | residual | location (µm) | cause |
|---|---|---|---|
| sinks_6x6_c2 | X Cont 0.0768 µm² | (22.025, 0.07; 27.175, 14.88) | BN + T on the axis: 2 × 0.0384 = the 6/6 PCell's own asymmetry |
| sinks_6x6_s2d_c2 | Y Cont 0.0768 µm² | the same, turned | as above |
| d2s_ab_n_c2 | X Cont 0.0256 µm² | (7.31, 0.07; 10.89, 1.61) | RN2 on the axis (4.4/1 PCell, 0.0256) |
| bias_tree_n_c2 | X Cont 0.0384 µm² | (9.325, 0.07; 14.475, 6.61) | NI on the axis (6/6 PCell, 0.0384) |
| casc_n, pd_n, rhigh | 0 | | |

A device on the axis cannot be mirrored onto itself without modifying the PCell (rule 3), so these stay.

## Netlist changes against the sheets (d2s_mpdda_pd, bias_tree_pd, units.spice)

- sinks: SX / SY `w=36u ng=4` → 6 × 6/6 each (§7 decision 1); BN 6/6 moved here from `bias_diodes` (decision 4);
  new dummies 4 × 2/6 and 1 × 6/6 (T), all D = S = G = vbn, B = vss.
- casc_n: CX / CY `w=30u ng=2` = 2 × 15/3 as drawn (no change); BNC 1/8 moved here from `bias_diodes`; new dummies
  4 × 2/3, D = S = G = vbnc.
- ab_n: RN2 / FNL / ABN unchanged; new dummies 2 × 2/1, D = S = G = vabn. pd_n: none.
- bias_tree_n: NI / NBP / NABP 6/6, NBPC 2.4/6, TGN / TDN unchanged; new dummy 1 × 2.4/6, D = S = G = ni.
- rhigh: each `rl=50.6u` as 4 × 0.5/12.65 µm in series (nodes U_1..U_3); 2 dummy segments, all terminals on vss.
- Dummy terminals differ from v1 / library (D = S = vss there): here D = S = G. Reason: every dummy terminal lands on
  the adjacent gate column, so no strap over a channel and no extra track. Cost (reasoning): the dummies' junction
  and overlap capacitance load the gate net (vbn: 14 µm of dummy W) instead of vss. Reverting is a wiring change.

## Open points

1. sinks_6x6_s2d_c2 is a 90° turn of the d2s cell; the s2d netlist is assumed identical.
2. Not simulated: BN centred and D = S = G dummies leave the circuit's devices and ratios unchanged (reasoning).
3. The 4× sinks option exists as a parameter only (one long row pair); not DRC / LVS checked.
