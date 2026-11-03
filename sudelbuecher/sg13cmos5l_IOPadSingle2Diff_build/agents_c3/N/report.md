<!--
SPDX-FileCopyrightText: 2026 Christoph Maier
SPDX-License-Identifier: Apache-2.0
-->
<!-- Saved by the lead from agent N's final reply (the harness refused N's own write of this file). Text as N sent it. -->
# N (C3): NMOS primitives and R block of IOPadSingle2Diff (s2d_mpdda_pd), 2026-11-03, 20:35–21:13 CET

Agent N (Claude Opus 5.5).
- **Build:** `python3 build_s2d_n3.py` in `out/` writes `s2d_n3_cells.gds` / `.cdl`. Two builds gave the same sha256
  (measured).
- **Sources:** the script is N2's `build_d2s_n2.py`, with N2's row, tab and band scheme; `render_png.py` is N2's.
- **Measured vs. reasoning:** "measured" means a tool result; everything else is reasoning.
- **Rule values** come from `sg13cmos5l_tech_default.json` (key) and `SG13CMOS5L_os_layout_rules.txt` (line):

  | rule | µm | line |
  |---|---:|---:|
  | Act.b | 0.21 | 883 |
  | Gat.b1 | 0.25 | 1018 |
  | Gat.d | 0.07 | 1020 |
  | Cnt.e | 0.14 | 1332 |
  | Cnt.f | 0.11 | 1333 |
  | M1.b | 0.18 | 1433 |
  | M1.e | 0.22 | 1437 |
  | V1.c1 | 0.05 | 1608 |
  | pSD.j1 | 0.40 | 1144 |
  | TGO.a | 0.27 | 971 |
  | EXTB.c | 0.31 | 1261 |
  | LU.b | 20 | 2358 |

## Common to all cells (rules 1–6)

- **Devices.** Each MOS is one unmodified SG13_dev `nmosHV` finger (ng=1), turned R270 as in N2's cells; the pd pair
  stays unturned. Fingers right of the vertical axis are mirrored. Each resistor segment is an unmodified `rhigh`
  PCell.
- **Dummies (rule 3).** S = D = vss, G by abutment. The outer stripe is plated into the ring. The inner stripe joins
  the ring through a 0.29 µm M1 lane beside the dummy, the library's lane of log 01:03. No metal lies over a channel,
  except the strap of the sinks' T (see the sinks).
- **Gate contacts (rule 2).** Contact columns on a poly fill as tall as the gate, at both row ends, 0.64 µm out to
  leave room for the lane. casc_n also has columns beside BNC. Measured: sym_check finds 0 narrow-poly hits in every
  cell.
- **Taps.** A closed p+ ring on every cell except `s2d_pd_n_c3` (Activ 0.30, pSD +0.03, M1 0.26, 0.21 from the rows).
  No tie between rows. One ThickGateOx rectangle covers all Activ + 0.27.
- **Pins** sit on the cell edges, on M2 crossing the ring; vss is on the ring M1.
- **Checks on the delivered GDS** (measured, `logs/`, round 3):
  - IHP `run_drc.py --no_density --mp=4`: all 31 tables ran in each run, no exception. 0 violations in 8 of 9 cells;
    `s2d_pd_n_c3` has 1 × LU.b, because it has no tap (see its section).
  - IHP `run_lvs.py --disable_tap_extraction`: 9 / 9 "Netlists match".
  - sym_check: 0 everywhere except the sinks' BN / T residual.
  - Earlier rounds and their fixes: `logs/checks_history.txt`.

| cell | size µm | area µm² | library cell, µm² | ratio | farthest N+ to tie (measured) |
|---|---|---:|---|---:|---:|
| sinks_6x6_s2d_c3 | 16.51 × 51.00 | 842.0 | sinks_6x6 967.3 | 0.870 | 6.89 |
| s2d_sinks_cmfb_c3 | 16.51 × 32.25 | 532.4 | s2d_sinks_cmfb 595.8 | 0.894 | 6.89 |
| s2d_casc_n_c3 | 72.74 × 14.37 | 1045.3 | s2d_casc_n 1010.8 | 1.034 | 6.62 |
| s2d_pd_n_c3 | 2.50 × 2.34 | 5.8 | s2d_pd_n 5.1 | 1.15 | no tie |
| s2d_cload_c3 (incl. TPN / TNN) | 29.56 × 14.24 | 420.9 | s2d_cload 387.2 (+ pd_n 5.1) | 1.087 (1.073) | 6.55 |
| s2d_rhigh_c3 | 19.24 × 20.09 | 386.5 | s2d_rhigh 402.0 | 0.962 | no N+ |
| bias_tree_noab_n_c3 | 24.21 × 9.21 | 223.1 | bias_tree_n + bias_tree_sw 309.7 (with NABP) | 0.720 | 4.04 |

LU.b is 20 µm everywhere.

sym_check results (measured, `logs/sym_check.txt`): 0 XOR and 0 narrow-poly hits in every cell except the sinks. The
sinks show X Cont 0.0768 µm² in (21.425, 0.07; 26.575, 14.88) of the core (the turned cell's Y axis): BN and T on the
axis, 2 × 0.0384, the 6/6 PCell's own asymmetry along W. N2 and F2 had the same residual. A device on the axis cannot
be mirrored onto itself without modifying the PCell (rule 4).

## sinks_6x6_s2d_c3 (core 51.00 × 16.51, turned R90; N2's c2 was 51.68 × 16.51)

```
row 2:  D | SY SX SX  T  SY SY SX | D     T = BN's twin (6/6 dummy), D = 2/6 dummy, all on vss, gates vbn
        --- band: x / vbn / y (M2) ---   mirror line
row 1:  D | SX SY SY BN  SX SX SY | D     section 5 map X Y Y X X Y / Y X X Y Y X, split at its center
```

**Checked against `s2d_mpdda.spice`:** SX / SY are `w=36u l=6u ng=6` = 6 × 6/6, gate vbn, source vss, drains x / y;
BN is the 6/6 diode of `bias_diodes`. This is the same netlist as N2's cell, so the map and the devices are kept.

Changes against N2's `sinks_6x6_s2d_c2` (all from rules 3 and 6):
1. The four center gate columns (17 contacts each) are gone, and the gaps beside BN and T close from 0.85 to 0.25 µm.
   This is F2's fix (Christoph 14:25). The row is 48.00 µm long (was 49.20).
2. Dummies: D = S = G = vbn becomes D = S = vss (outer stripe plate plus lane; was a bridge to the gate column).
3. T: D = S = G = vbn becomes D = S = vss (top plate, plus an M1 strap 0.29 µm wide across its own channel). Without
   the center column, the strap is the only path (F2's fix).
4. BN's drain, which was bridged to a center column, now has a 3-Via1 tab onto the vbn track (F2).
5. The end gate columns moved from 0.33 to 0.64 µm outside the row, to make room for the lanes.
6. The top / bottom tie strips and N2's two M1 joiners became one closed ring; its side legs replace the joiners.
7. The M2 tracks run to the cell edge, so the pins are on the edge (rule 8).

Unchanged: the map, BN and T in the middle, the tabs (row 1 0.75 left, row 2 0.75 right), the band, the row pitch,
the R90 turn, the single vss pin. The source bus is the ring, tapped by that one pin (section 6).

**Pins** (turned): y / vbn / x M2 at (−7.975 / −7.475 / −6.975, −1.25); vss M1 at (0.36, −0.96).

**Netlist:** SX / SY each as 6 × 6/6; BN moved here from `bias_diodes`; 4 × 2/6 dummies and T 6/6, D = S = B = vss,
G = vbn.

## s2d_sinks_cmfb_c3 (core 32.25 × 16.51, turned R90)

```
row 2:  D | SYC SXC SXC SYC | D       band xc / vbn / yc; no diode, so nothing sits on an axis
row 1:  D | SXC SYC SYC SXC | D       cross-coupled: each set's centroid at the center in x and y
```

Built the same way as the sinks: the same finger, lanes, end columns and ring. SXC / SYC `w=24u ng=4` become
4 × 6/6 each, and 4 × 2/6 dummies are added (vss, G vbn).

**Pins** (turned): yc / vbn / xc M2 at (−7.975 / −7.475 / −6.975, −1.25); vss M1 at (0.36, −0.96).

## s2d_casc_n_c3 (72.74 × 14.37)

```
        above row 2: k0  y (short) , xc (short) | k1  x | k2  yc        (M2 source levels)
row 2:  D | CYC  CY  [BNC]  CX  CXC | D      D = 2/3 dummy (vss, G vbnc); each device 2 × 15/3
        band (bottom to top): vcmfb voutp vbnc voutn vdd
row 1:  D | CXC  CX  [BNC]  CY  CYC | D      point-symmetric; BNC (1/8) spans both rows and the band
        below row 1: k0  x (short) , yc (short) | k1  y | k2  xc
```

- **Map.** N2's cross-quad, extended to four devices. Each pair is point-reflected about the center, so every
  device's centroid is there.
- **BNC.** It sits in the middle on both axes, so it needs no twin.
  - Its gate joins both row gates through the middle-column fills. The fills stop 0.25 µm short of BNC and join its
    gate only where they overlap in y; this removed the round-1 sym_check slivers.
  - BNC's drain bridges to the left middle column, and its source runs down to the ring.
- **Source wiring.** x / y have M1 verticals on the left, xc / yc on the right, inside the ring. The ring must be
  symmetric, so there are 3 levels on each side.
- **Metal over a channel:** only the 5 band tracks crossing BNC, as in N2's cell.
- **Pins:** vcmfb / voutp / vbnc / voutn / vdd M2 at (−2.27, 3.975 / 4.475 / 4.975 / 5.475 / 5.975); x / y M2 at
  (−2.27, −0.295 / −0.795); xc / yc M2 at (69.97, −1.295 / −0.295); vss M1 at (−1.98, −1.79).
- **Netlist:** CX / CY / CXC / CYC `w=30u l=3u ng=2` are drawn as 2 × 15/3 each (no change). BNC moved here from
  `bias_diodes`. 4 × 2/3 dummies are added, D = S = vss, G = vbnc.

## s2d_pd_n_c3 (2.50 × 2.34) and s2d_cload_c3 (29.56 × 14.24)

```
pd_n:   voutp | TPN | vcm | TNN | voutn        2 PCells 1/0.45 at 0.83 pitch, sharing the vcm stripe, no tap
cload:  ring | CLP 12×12 | col(voutp) [TPN vcm TNN] col(voutn) | CLN 12×12 | ring     mirror images
```

- **pd_n:** Christoph's compaction of the switch cells (log 17:30 / 17:43).
  - The gates are joined by one poly cap ("contact the gates with poly"). The contacts sit 0.18 µm above the Activ,
    and the M1 bar is 0.21 µm and Via1-ready.
  - The pins sit on the stripes, the vcm pad and the bar, with no stubs.
  - The cap reaches 0.55 µm above the Activ, so no poly piece is narrower than 0.30 µm. This makes the cell 0.30 µm
    taller than the library's.
- **cload:**
  - The pd pair sits inside the cell (rule 6, `messages.md` 1).
  - Each 12 × 12 gate has a full-height contact column on its inner side: 35 contacts on a 12 µm fill.
  - The S / D stripes are plated into the ring, and the pair's drains join the columns in M1.
- **Pins (cload):** M2 on the top edge, y 13.02: voutp 12.33, en_3v3_b 13.22, vcm 13.78, voutn 15.23; vss M1 at
  (−0.46, −0.36).
- **Pins (pd_n):** M1 voutp (0.15, 0.5), vcm (0.98, 0.5), voutn (1.81, 0.5), en_3v3_b (0.51, 1.285).
- **Netlist:**
  - CLP / CLN and TPN / TNN are unchanged.
  - In cload, the bulk of TPN / TNN is vss through the cload ring.
  - In `s2d_pd_n_c3` alone, LVS extracts the bulk as an internal net (measured), and the CDL agrees.

## s2d_rhigh_c3 (19.24 × 20.09)

`dummy A1 A2 F1 F2 M1 M2 M2 M1 F2 F1 A2 A1 A1 A2 F1 F2 M1 M2 M2 M1 F2 F1 A2 A1 dummy`

- **Strips:** rhigh 0.5 × 12.65 µm at 0.68 µm pitch, in the library's s2d sequence. Each resistor's segment positions
  sum to 46 (centroid 11.5 of 0–23), and the sequence is mirror-symmetric.
- **Wiring:** as in N2's d2s_rhigh_c2: Via1 on each head, M2 stubs, M1 links on 6 levels at the bottom and 6 at the
  top (N2's interval coloring gives this for the nested section 5 pattern). Each resistor enters and leaves at top
  heads.
- **Ring:** closed, as F2's.
  - The side legs are 0.54 µm from the strips (EXTB.c, as the library).
  - The top / bottom legs are 0.18 µm beyond the outermost link level, symmetric about the strip center.
  - The dummy heads are strapped into the side legs in M1.
- **Pins:** M2 on the top edge, y 16.17. sa_A1 … sa_M2 at x 0.93 / 1.61 / 2.29 / 2.97 / 3.65 / 4.33; sb_M2 … sb_A1 at
  x 13.17 / 13.85 / 14.53 / 15.21 / 15.89 / 16.57. vss M1 at (−0.69, 6.325).
- **Netlist:** each `unit_r2` XR `rl=50.6u` is drawn as 4 × 0.5/12.65 in series (nodes U_1..U_3), plus 2 dummy
  segments on vss. LVS reduces each chain to 0.5 / 50.6 µm (measured). Each extra head adds contact resistance, equal
  in all 6 units (reasoning, as N2).

## bias_tree_noab_n_c3 (24.21 × 9.21)

```
ring | [TGN] col | NBPC 2.4/6  NBP 6/6 | NI 6/6  D 2.4/6 | col [TDN] | ring       gate ni; axis between NBP and NI
```

- **Row.** NBPC has its twin D at the other end (rule 1). NBP and NI are a mirror pair, so nothing sits on the axis:
  sym_check 0, where N2's cell had 0.0384. D is S = D = vss: a bottom plate, and its top stripe tabs straight into the
  top ring leg under the ni track.
- **Switches.** TGN (left) and TDN (right) are mirror images, each with its own column on a fill as tall as its gate.
  TGN's source and TDN's drain (ni) bridge to the row's gate columns, and TDN's source goes down to the ring.
- **Wiring.** The ni M2 track above the row joins NI's 3-via tab and both columns. vbpc, vbp and iref rise in M1
  under it, then cross the top leg in M2.
- **Pins:**
  - vbpc / vbp / iref M2 on the top edge, at (1.20 / 5.65 / −1.46, 8.235);
  - en_3v3 M2 on the left, at (−3.08, 3.34);
  - en_3v3_b and ni M2 on the right, at (20.63, 3.34 / 7.06). ni also serves agent P's TGP;
  - vss M1 at (−2.79, −0.36).
- **Netlist:** NABP is gone (bias_tree_noab_pd). TGN / TDN / NI / NBP / NBPC are unchanged. Added: 1 × 2.4/6 dummy,
  D = S = vss, G = ni.

## Open points

1. Placement of the pd pair, the orientation of the sink blocks and the dummy-lane choice: see `messages.md`.
2. Not simulated: the dummy ties (vss instead of the gate net) and the BN / BNC moves. Devices and ratios are unchanged
   (reasoning).
