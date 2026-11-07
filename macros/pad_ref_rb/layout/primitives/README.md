<!--
SPDX-FileCopyrightText: 2026 Christoph Maier
SPDX-License-Identifier: Apache-2.0
-->
# Layout primitives for pad_ref_rb

2026-11-07, Christoph's request: "start collecting layout primitives to assemble a replica bias from replicated
primitives". This is a collection and a plan, not a layout yet.

The replica bias copies the s2d pad's devices (`../../../vcm_rb/README.md`), so its layout copies the pad's layout
structures as well. The pad cell drawn in session C3 is DRC clean and LVS clean, and its rows hold every device size
that pad_ref_rb uses.

| file | what |
|---|---|
| `collect_primitives.py` | the collector. It reads the s2d pad cell (read only), keeps the rows below and their devices, checks them by XOR, and writes the three files below |
| `pad_ref_rb_primitives.gds` | top cell `pad_ref_rb_primitives`: rows on the left, leaf devices on the right, names on TEXT 63/0 |
| `pad_ref_rb_primitives.png` | its render |
| `primitives.tsv` | the 14 leaf device cells: type, W, L, ng (measured from Activ ∩ GatPoly), bbox, name in the pad cell |
| `mapping.tsv` | each of the 33 MOS devices of pad_ref_rb (32 + the dummy MDPBN) → its leaf primitive → the pad structure it replicates |

- **Naming:**
  - Every copied cell is prefixed `rbsrc_`.
  - Leaves get a name that says what they are, for example `rbsrc_nhv_w15_l3` (the pad cell calls it `nmosHV$3`;
    the d2s pad uses the same `$n` names for other devices).
  - Rows keep their pad names behind the prefix, for example `rbsrc_s2d_casc_n_f`.
  - The `rbsrc_` cells are unchanged copies. Cut or rewired versions get new names.
- **Check:** the XOR of every copied cell against its source is empty on all layers (`collect_primitives.py` prints
  it).
- **Regenerate:** `python3 -I collect_primitives.py` (klayout Python module).

## Source rows (s2d pad, session C3)

| row | size (µm) | holds in the pad |
|---|---|---|
| `bias_tree_noab_p_c3` | 12.94 × 10.37 | PBN 5/6, PBNC 2/6, dummy 2/6 (MDBP), TGP 1/0.45 |
| `bias_tree_noab_n_c3` | 24.21 × 9.21 | NI 6/6, NBP 6/6, NBPC 2.4/6, dummy 2.4/6 (MDBN), TGN / TDN 1/0.45 |
| `s2d_tails_hi_f` | 45.19 × 9.16 | 8 unit tails 5/6 on vbp in one iovdd well (BP among them) |
| `tub_p20x1_c3` | 4.30 × 11.97 | unit input device 20/1 ng=2 in its own well (bulk = source) |
| `s2d_inputs_c3` | 47.58 × 26.44 | 16 tubs: 12 units and 4 dummies, two rows of 8 |
| `s2d_casc_n_f` | 72.74 × 14.37 | 8 × 15/3 on vbnc (CX, CY, CXC, CYC), 4 dummies 2/3, BNC 1/8 in the middle |
| `sinks_6x6_s2d_c3_core` | 51.00 × 16.51 | 14 × 6/6 on vbn (SX, SY, BN, BN twin), 4 dummies 2/6 |
| `s2d_sinks_cmfb_c3_core` | 32.25 × 16.51 | 8 × 6/6 on vbn (SXC, SYC), 4 dummies 2/6 |
| `s2d_cload_c3` | 29.56 × 14.24 | CLP / CLN 12×12 hv NMOS capacitors, TPN / TNN 1/0.45 |
| `s2d_loads_f` | 44.79 × 12.32 | 12 × 6/4 in one iovdd well, 4 × 1/4 (the source of the 1/4 finger) |

## Where each replica goes

Every device of pad_ref_rb has a leaf primitive of the same W, L and ng (`mapping.tsv`). Taking the rows, not just the
leaves, gives each replica the same surroundings as the device it copies: neighbours, dummies, well edge, gate bar.

| assembled row | from | devices of pad_ref_rb | note |
|---|---|---|---|
| tree P | `bias_tree_noab_p_c3`, as drawn | TGP, PBNC; BP in the dummy 2/6 slot (as a diode); the 5/6 slot (the pad's PBN) a dummy, MDPBN | the pad's own tree row; rewiring only |
| tree N | `bias_tree_noab_n_c3` + one 2.4/6 slot | TGN, TDN, NI; NBP in the NBPC 2.4/6 slot; SH1 in the dummy 2.4/6 slot, SH2 in the new slot; SY in the 6/6 slot (NBP in the pad: 6/6 on ni) | every device on ni together, as in the pad tree |
| tails | `s2d_tails_hi_f`, cut to 4 | dummy, TR, BT, dummy | TR is the edge detector's copy of the unit tail: same row, same well |
| tubs | `s2d_inputs_c3`, one row cut to 5 | dummy, MR, BA, BB, dummy | MR copies the unit input device; BA / BB are the same device in the OTA |
| cascodes | `s2d_casc_n_f`, cut | CY, F1–F4 (5 × 15/3, all on vbnc), BNC 1/8 in the middle, 2/3 dummies at the ends | CY and the four followers copy CX / CY; BNC sits next to them as in the pad |
| mirror | `sinks_6x6_s2d_c3_core`, one row cut to 4 | SF (2/6) at one end in place of a 2/6 dummy, BD, BM, dummy 2/6 | BD / BM 6/6 are the sink finger; the pad's sink rows end in 2/6 |
| caps | `s2d_cload_c3` + one 12×12 | CB1, CB2, both SPD (vcm, vref) in the TPN / TNN slots; CB as an extra capacitor | the same row as the pad's load capacitors |
| small tubs | **new**, after `tub_p20x1_c3` | SU, SL1, SL2: 1/4 PMOS each in its own well (bulk = source) | the only structure the pad does not have |

**Area estimate** (sum of row bounding boxes, before routing):

| tree P | tree N | tails | tubs | cascodes | mirror | caps | small tubs | sum |
|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| 134 | 248 | 214 | 407 | 750 | 227 | 641 | 124 | ≈ 2750 µm² |

With routing, about 1.5×, so roughly 4100 µm², about 64 × 64 µm, for both references. The estimate in
`docs/replica_bias/SUMMARY.md` before the shared tree was 2 × 50 × 60 µm.
- **cascodes:** about 52 µm wide when the five fingers are folded 3 + 2 into the row's two levels; 72.7 µm as one
  full level.

## What replicating the layout implies for the schematics

Christoph, 2026-11-07: "feel free to tweak the schematics if required by replicating layout structures". These are the
changes the rows above call for. Each is applied when its row is assembled, with a re-simulation where it is not
purely a dummy.

1. **Dummies:**
   - The cut rows keep end dummies: 5/6 tails, tubs, 2/3 cascodes, 2/6 sinks.
   - They enter the netlists as `[DM]` devices, as in the pads' sheets (`s2d_mpdda_pd`). LVS needs them, and they
     are electrically off: gates at their rail.
2. **Layout hierarchy against schematic hierarchy:**
   - The rows mix devices of the three subcells. Tree N holds NI and NBP (bias_tree_rb) next to SY and SH (vcm_rb),
     and SF (vref_s2d_rb) sits at the end of the mirror row.
   - The cascode row holds BNC (bias_tree_rb), CY (vcm_rb) and F1–F4 (vref_s2d_rb).
   - Proposal: LVS pad_ref_rb flat, and keep the sheets functional (tree, vcm, vref). The other way is to regroup
     the sheets by row.
3. **The tree's spare 5/6 slot: a dummy** (Christoph, 2026-11-07: "Make it a dummy"). `XMDPBN vdd vbp vdd vdd`
   5u/6u in bias_tree_rb, in the pads' convention (D = S = B on the rail, gate by poly abutment); in the netlist and
   the sheet ([3] layout dummy). TR stays with BT in the tails row.
4. **xschem's "finger width is too big" / "length is too big"** (the PDK's `fet_drc`: hv w/ng ≤ 10 µm,
   l ≤ 10 µm):
   - CY and F1–F4 (15/3, ng=1) and CB, CB1, CB2 (12/12) trigger it.
   - These are the pad's own devices: CX / CY are 30/3 ng=2 = 15 µm fingers, CLP / CLN 12/12.
   - The pad sheets size them with expressions (`w={10e-6*lcas}`, `w={wcl}`), which `fet_drc` cannot read, so only
     the replica sheets warn.
   - Keep them: the replica has to match the pad, and the drawn 15/3 finger and 12×12 capacitor pass DRC and LVS in
     the pad.

## Not done yet

- Assembly of the rows (cut, rewire), routing, and pins.
- DRC of the `rbsrc_` cells on their own. They were checked only inside the pad cell; rows cut out of it may need
  their tie or ring closed.
- LVS, PEX.
- The small-tub primitive for SU / SL1 / SL2.
- The decision on 2 above (flat LVS or sheets regrouped by row).
