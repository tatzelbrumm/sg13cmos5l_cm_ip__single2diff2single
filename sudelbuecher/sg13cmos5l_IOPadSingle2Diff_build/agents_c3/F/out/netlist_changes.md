<!--
SPDX-FileCopyrightText: 2026 Christoph Maier
SPDX-License-Identifier: Apache-2.0
-->
# Netlist changes the pad candidate implies (F, C3 stage B, 2026-11-04), for the backannotation

The reference is `pad_candidate.cdl`. KLayout's deep LVS (`logs/pad_lvs.log`) measures it equal to the layout.
`logs/circuit_check.txt` measures its non-dummy devices equal to the current sources (`netlist/source/s2d_mpdda.spice`,
`s2d_pd.spice`, `bias_tree_noab_pd.spice`, `bias_ref_pd.spice` bias_diodes) plus `s2d_pad_esd.sch`. A copy with one
tub gate moved fails the check [M]. The sources in `inputs_B/macro` are byte-equal to those circuit files [M].

So the circuit stays the same. What changes is how the sheets and source netlists write it down: the drawn fingers,
the moved diodes, every dummy, the protection as drawn, and the partitioned ports.

## 1. `s2d_mpdda` / `s2d_mpdda_pd` (sheets `s2d_mpdda.sch`, `s2d_mpdda_pd.sch`; `s2d_mpdda.spice`, `s2d_pd.spice`)

| device(s) | source now | drawn (CDL) |
|---|---|---|
| SX, SY | `w=36u l=6u ng=6` | 6 × 6/6 ng=1 each (`sinks_6x6_s2d_c3`) |
| SXC, SYC | `w=24u l=6u ng=4` | 4 × 6/6 each (`s2d_sinks_cmfb_c3`) |
| CX, CY, CXC, CYC | `w={10e-6*lcas} l={1e-6*lcas} ng=2` (30/3) | 2 × 15/3 each (`s2d_casc_n_f`) |
| LP, LN, D | `w=24u l=4u ng=4` | 4 × 6/4 each (`s2d_loads_f`) |
| LPC, LNC, DC | 30/3 ng=2 | 2 × 15/3 each (`s2d_casc_p_f`) |
| unit_r2 XR | `rhigh w=0.5u l={rl}` (50.6) | 4 × rhigh 0.5/12.65 in series (nodes `<U>_1.._3`), all six units (`s2d_rhigh_c3`) |
| unit_r2 XTa / XTb | 5/6 | unchanged, split into two rows: `s2d_tails_hi_f` (A1a F2b F1b A2a M1a M2b) above the tubs, `s2d_tails_lo_f` (A2b F1a F2a A1b M1b M2a) below |
| unit_r2 XMa / XMb | 20/1 ng=2, bulk = source | unchanged (one tub each, `tub_p20x1_c3`) |
| TPP, TNP | 1/0.45 each | one pmosHV ng=2 PCell sharing the vcm stripe; LVS sees two 1/0.45 devices |
| TPN, TNN | 1/0.45, bulk vss | unchanged, drawn inside `s2d_cload_c3` (its ring is their bulk tie) |
| CLP, CLN | 12/12 | unchanged (`s2d_cload_c3`) |

- **Bias diodes move from `bias_diodes` into `s2d_mpdda_pd`.**
  - BP 5/6 goes to the tails (`s2d_tails_hi_f`, at the row's left end).
  - BN 6/6 goes to the sinks (row 1 center).
  - BPC 1/4 goes to `casc_p` (row end).
  - BNC 1/8 goes to `casc_n` (center).
  - Nets and sizes are unchanged. Only the hierarchy moves (layout_primitives.md decision 4).
- **Dummies to add** (D = S on the rail, the gate by poly abutment). The circuit check lists the totals:
  - tubs: 4 × `tub` with d = g = s = vdd;
  - tails: 3 × 5/6 with g = vbp (tails_hi D7, tails_lo D0 and D7);
  - loads: 4 × 1/4 with g = vcmfb;
  - casc_p: 3 × 1/4 with g = vbpc;
  - sinks: 4 × 2/6 plus T 6/6 (BN's twin), D = S = vss, g = vbn;
  - sinks_cmfb: 4 × 2/6, D = S = vss, g = vbn;
  - casc_n: 4 × 2/3, D = S = vss, g = vbnc;
  - rhigh: 2 × 0.5/12.65, both ends on vss.
- **Ties at the buffer, unchanged:** vfbp = voutp = outp and vfbn = voutn = outn. The vdd / vss of `s2d_mpdda_pd`
  are the pad's iovdd / iovss.

## 2. `bias_tree_noab_pd` (`bias_tree_noab_pd.spice`)

- `Xd ... bias_diodes` goes (its four diodes now sit in `s2d_mpdda_pd`, section 1).
- Two dummies to add:
  - 2/6 pmos, D = S = vdd, g = vbp (`bias_tree_noab_p_c3`);
  - 2.4/6 nmos, D = S = vss, g = ni (`bias_tree_noab_n_c3`).
- TGP stays in `bias_tree_noab_p_c3` as P drew it; TGN / TDN stay in `bias_tree_noab_n_c3`.

## 3. The pad (`sg13cmos5l_IOPadSingle2Diff.sch` / `.sym` / `.spice`)

- **Ports.** The partitioned list of the layout: `iovdd iovss vdd vss pad outp outn vcm vref iref en_3v3 en_3v3_b`.
  - `Xc` (`en_ctrl_3v3`) and `Xg` (`bias_gen_pd`) leave the cell for the slot, as C2 did for d2s (option B).
  - So `ibias en_1v2 sel0_1v2 sel1_1v2 vdd1v2_sense vdd3v3_sense` leave the port list, and `iref en_3v3 en_3v3_b`
    join it.
  - vdd / vss are the 1.2 V ring rails, without devices. The layout has no top-level `vss` text (C2_report §4.3), so
    magic's pin check shows the same accepted vss / iovss merge as d2s.
- **Secondary protection: none for now** (brief). `XSP ... sg13cmos5l_SecondaryProtection` goes, and `padres`
  becomes `pad`: the tubs' vin gates sit directly on the pad.
- **Primary protection as drawn in the template** (`s2d_pad_esd.sch`, equal to the template's extraction). It replaces
  `XCP / XCN / XDN / XDP` (IHP's library subckts):
  - `XRP iovdd gp sub! rppd w=0.5u l=12.9u` and `XMCP pad gp iovdd iovdd sg13_hv_pmos w=266.4u l=0.6u ng=40`;
  - `XRN gn iovss sub! rppd w=0.5u l=3.54u` and `XMCN pad gn iovss iovss sg13_hv_nmos w=88u l=0.6u ng=20`;
  - two dpantenna (pad → iovdd) and two dantenna (iovss → pad) 1.26 × 27.78 µm each.

  In the LVS netlist the rppd bulk is iovss, the substrate.
- **Supplies.** iovdd and iovss reach the block through one Via2 tap per supply group (one each for the tail and
  sink source buses).
  - The two iovdd Metal3 rails (66–91.5, 93.5–119) are joined inside the cell by one Metal2 / Via2 strap (`pwr_f`).
    Without it they are two nets here; in the IO ring they meet anyway.
  - The schematic needs no change for this.

## 4. Not changed by the layout (stated so the backannotation can skip them)

- No device size, length, ratio or bulk connection of the circuit changes.
- `lcas = 3`, `rl = 50.6u` and `wcl = 12u` stay.
- The pins added by F's `_f` copies (`s2d_casc_n_f` xc / yc band-end exits; `s2d_loads_f` / `s2d_casc_p_f` fanned-out
  pin tracks; the vbp stubs at both ends of the tail rows) are Metal2 only and add no device or net.
