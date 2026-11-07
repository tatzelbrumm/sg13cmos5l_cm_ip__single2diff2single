<!--
SPDX-FileCopyrightText: 2026 Christoph Maier
SPDX-License-Identifier: Apache-2.0
-->
# N (C4): NMOS rows and capacitors of pad_ref_rb (2026-11-07, 20:40–21:25 CET)

Claude, agent N. [M] = measured by a tool run, [R] = reasoning. Files are in `layout_rb/N/out/`; the check rounds are in
`logs/checks_history.txt` and the pins in `build_stdout.txt` (each cell's pins sit on its edges, vss is M1 on its ring).

**Code.** `build_rb_n.py` is C3's `build_s2d_n3.py` (6dae1682ae51). The library, `drains()` and `ring_x()` are unchanged
[M]. The row functions take device lists and nets as arguments; C3's geometry code is kept, additions marked `C4:`.
- **Regression [M]:** `--pad` rebuilds bias_tree_noab_n_c3, sinks_6x6_s2d_c3_core and s2d_cload_c3 with XOR 0 on all
  layers against the S2D pad, and s2d_casc_n_c3 with XOR 0 against C3's cell (the pad's _f adds only F's M2 exits).
- **Reproducible [M]:** two builds are byte-identical (gds 1389784e8727).

## Checks [M] (round 4, final)

| cell | size µm | area µm² / pad counterpart | DRC | LVS | sym | LU µm |
|---|---|---|---|---|---|---|
| rb_tree_n | 34.01 × 9.71 | 330.4 / 223.1 bias_tree_noab_n_c3 = 1.48 (8 slots, not 4) | 0 | match | 0 | 4.30 |
| rb_casc | 71.72 × 12.37 | 887.2 / 1045.3 s2d_casc_n_f = 0.85 | 0 | match | 0 | 5.62 |
| rb_mirror | 19.75 × 9.17 | 181.1 / 842.0 sinks_6x6_s2d_c3_core (14 fingers) = 0.22 | 0 | match | 0 | 4.02 |
| rb_cload | 29.56 × 14.24 | 420.9 / 420.9 s2d_cload_c3 = 1.00 | 0 | match | 0 | 6.55 |
| bypass_rb 3×4 | 53.30 × 40.02 | 2133.1: 178 per capacitor / 210 in s2d_cload_c3 = 0.84 | 0 | match | 0 | 19.44 |

- **Total:** 3953 µm² (README estimate 3925). No DRC log mentions "exception".
- **sym_check:** taken from `pad_cell_2026-10-31`, because the brief's link is dangling.
- **LU:** C3's measure; it reproduces C3's 6.55 / 4.04 / 6.62 µm.
- **CDL vs. netlists** (`cdl_vs_netlist.py`): 32 devices, 0 mismatches; every N device is drawn.

## Identical to the pad / different (XORs [M], `logs/compare_pad.txt`)

- **rb_tree_n** `[TGN] | SH2 SF NBP SY | NI SH1 MDTN6 MDTN7 | [TDN]`, widths 2.4 2 2.4 6 | 6 2.4 2 2.4.
  - Identical (XOR 0 on Activ / GatPoly / Cont): the pad's four slots, which hold NBP, SY, NI and SH1 as briefed;
    TGN, TDN and their columns.
  - Added on the bar: a 2.4/6 pair at the ends (SH2 / MDTN7, so the row ends in 2.4/6 as in the pad), a 2/6 pair
    inside it (SF / MDTN6), and an M1 gh bar (+0.50 µm height).
  - SF is here because its gate is ni, not bd [R].
- **rb_casc** `D | F1 F2 [BNC] CY X | D` / `D | X X [BNC] F3 F4 | D` (X = 15/3 dummy).
  - Rows, BNC, columns and fills are XOR 0 inside the ring. CY sits in the pad's CY slot.
  - With BNC in the middle, 5 fingers need 8 slots [R].
  - The band keeps its 5 track places. One source level per side gives a ring 2.00 µm lower and 1.02 µm narrower.
- **rb_mirror** `D | BD BM | D`, row 1 of the pad's sinks: both ends XOR 0; one row, ring closed over the band.
- **rb_cload**: the pad cell with voutp → vcm (CB), voutn → vref (CBR), TPN / TNN → the SPDs, and the shared stripe →
  vss. Device layers are XOR 0. The vss stripe runs in M1 into the ring between a split gate bar (0.92 µm² metal XOR).
- **bypass_rb = bypass(ncm, ncr, rows, cols)**: the pad's CLP with its column, arrayed; one unit is XOR 0.
  - Columns in facing pairs (fills Gat.b 0.18 apart), pairs 0.54 apart (Gat.c + Gat.b), rows Act.b 0.21 apart.
  - An M1 vss bus runs between rows. vcm goes up and vref down on M2 buses; places fill column-wise, vcm first.
  - LU.b limits the short side to 3 (4×4: 25.78 µm). Also tried: 2×6, 6+6, 4×3, 3×3 with 7; all DRC / LVS clean [M].

## How the binding rules are met

1. **Symmetry** (sym 0 on every cell [M]): the same device at both row ends. Tree 2.4/6 SH2 / MDTN7 mirrors the pad's
   NBPC / MDBN. BNC is in the middle, NI beside the axis as in the pad, and BM is BD's twin.
2. **Gates:** poly-fill columns only at the row ends (and beside BNC, as in the pad), 0 narrow-poly hits [M]. Dummies
   are gated by abutment.
3. **Dummies:** S = D = vss. The outer stripe is plated into the ring. The inner stripe takes a lane, an M1 strap
   across its own channel (the casc spares, like the pad sinks' T), or a tab into the ring. No vss on M2.
4. **PCells:** unmodified, one finger each. 5. **Taps:** closed p+ rings, nothing between rows.
6. **Metal:** no center contacts, pins on the edges without stubs, M2 only for pins, band tracks and the bypass buses.
   Switches sit in the cell they serve.
7. **Sizes and area:** as the netlists; areas in the table.

## Netlist consequences

No W, L, ng or finger split changed. Dummies (MD + row + position; d g s b):
- rb_tree_n: MDTN6 2u/6u, MDTN7 2.4u/6u, both `vss ni vss vss`.
- rb_casc: MDC10, MDC15, MDC20, MDC25 2u/3u (the pad's end dummies) and MDC14, MDC21, MDC22 15u/3u (spare slots), all
  `vss vbnc vss vss`.
- rb_mirror: MDM0, MDM3 2u/6u `vss bd vss vss`.
- rb_cload's CLN slot is a 12/12 on vref: use bypass_rb with ncr = 7 (vref keeps 8), or keep 8 (9 on vref).
- The casc dummies add 159 µm² of gate on vbnc: re-simulate the enable settling [R].

## Open questions for Christoph

1. rb_casc: 8 slots, or 6 with a BNC twin at the ends (about 55 × 12.4 µm) [R]?
2. rb_cload's CLN slot: a vref capacitor, a vcm capacitor, or a dummy with its gate on vss?
3. rb_tree_n: keep the pad's dummy next to NI and put SH1 / SH2 at the ends? Same area, but it needs T straps.
4. Add true end dummies to rb_tree_n, or 6/6 dummies beside BD / BM?
