<!--
SPDX-FileCopyrightText: 2026 Christoph Maier
SPDX-License-Identifier: Apache-2.0
-->
# vref_s2d_rb: replica bias for the pad reference of the S2D pad

The pad reference `vref` of `sg13cmos5l_IOPadSingle2Diff`: the S2D gives `outp − outn = 2 (pad − vref)`.

**The user's choice (2026-11-06, answer 1a):** about 0.5 V, so that the pad range 0 … 1 V includes iovss.

Since 2026-11-07 it hangs on the shared bias tree `bias_tree_rb`, which also feeds `../vcm_rb`; both sit in the cell
`pad_ref_rb` (`../pad_ref_rb`), made from one 5 µA reference current with one enable. Until then the block had its own
copy of the tree (NI, BP, BNC) and its own reference. Task, survey and run log are in `docs/replica_bias/`.

## Function

- **Where the S2D input stays linear** (INL ≤ 2 mV, u = ±0.5 V): for vref above an edge (gap run G4, fit in
  `../vcm_rb/testbenches/spice/explore_edges.py`).
  - The edge is set by the input follower (hv PMOS 20u/1u) leaving saturation against the fold node x:
    `edge = x − V_SG(follower at 5 µA) + 0.676 V`, within 4 mV over corners and supplies at 125 °C.
  - It is below 0.4 V up to 27 °C and 0.46 … 0.54 V at 125 °C (fast PMOS highest).
  - So a fixed 0.5 V fails INL at 125 °C with tt / sf / ff PMOS (up to 3.6 mV, G4). "Pad range from 0 V" (≤ 0.5 V at
    room) and "linear at ff / 125 °C" (≥ 0.55 V) together need a positive temperature coefficient of at least
    +0.5 mV/K.
- **The block:** `vref = vbnc − V_GS(F)`, an x-node replica at low current density.
  - F is four fingers of the S2D fold cascode (15u/3u) at 1.67 µA, against the S2D's 30u/3u at 10 µA.
  - It rises with temperature as x does (+0.6 mV/K) and sits about 0.1 V above it.
  - Its output impedance is 1/gm(F), about 20 kΩ. CB1 / CB2 (2 × 12u × 12u hv NMOS to vss, not to iovdd, so supply
    ripple does not reach the pad's zero) hold the pin during the pad's own transients (G6).
- **Lines:** from `bias_tree_rb`: ni (NI 6u/6u, the reference) for the sink SF, vbnc (BNC 1u/8u at 2 µA from PBNC
  2u/6u) for the followers F.
- **Disabled** (`en_3v3` = 0 on `pad_ref_rb`): the tree cuts the reference and pulls ni to vss, vbnc decays to vss, and
  SPD pulls `vref` to vss (the S2D's vref drives gates only).
- **No own enable:** vref is on whenever `pad_ref_rb` is. Pulling vref low with the tree on would short the followers F
  from vbnc to vss.

## Ports

| port | dir | |
|---|---|---|
| vdd, vss | inout | iovdd / iovss |
| ni, vbnc | in | the lines of `bias_tree_rb` (gates only) |
| vref | out | to the S2D pad's `vref` (gates only) |
| en_3v3_b | in | complement of the 3.3 V enable (en_ctrl_3v3), gate of SPD |

## Files

```
netlist/source/vref_s2d_rb.spice        source netlist (mm_ok=1 on every device)
schematic/xschem/vref_s2d_rb.sch/.sym   sheet drawn by hand from the source netlist (2026-11-07, xschem-analog-schematic skill,
                                        compacted by hand by Christoph, then moved onto the shared tree); make check-sheet
                                        compares it device by device (8 = 8, ports equal)
schematic/vref_s2d_rb.png / .svg        render of the sheet
../vcm_rb/schematic/gen_sheet.py        only its --check mode is in use; generating would overwrite the hand-drawn sheet
../pad_ref_rb/verification/             CACE suite of pad_ref_rb, which covers this block (vref_room / hot / cold, pd, mm)
verification/baseline/cace_own_tree/    CACE results of 2026-11-06, with the block's own tree
verification/baseline/s2d_mc_vref0v5/   G8: S2D mismatch / process MC at vref 0.5 V (current schematic)
testbenches/spice/                      explore_ztc.py (zero-TC currents of the pads' diode sizes), explore_vref.py
```

The block and closed-loop decks run pad_ref_rb: `../vcm_rb/testbenches/rb_char/run_rb.py`.

## Results (schematic, 2026-11-06)

| quantity | result | condition |
|---|---|---|
| vref | 0.436 … 0.455 / 0.483 … 0.504 / 0.572 … 0.596 V | −40 / 27 / 125 °C; 5 MOS corners; iovdd 3.0 … 3.6 V; harness reference |
| vref, other references | OA core 0.376 … 0.668 V, bandgap core 0.432 … 0.592 V | |
| margin to the S2D INL edge | ≥ +31 mV at 125 °C (ff) | harness reference |
| S2D pad range with this vref (linear to 1 mV, ground-referenced source) | 0.000 … ≥ 1.09 V up to 27 °C; 0.015 … 0.095 to ≥ 1.215 V at 125 °C | `cl_s2d_win`; an ideal 0.5 V gives 0 … 1.057 V at 3.0 V ss −40 °C |
| S2D INL with this vref and vcm_rb | ≤ 1.28 mV (OA core: 1.73) | ideal 0.5 / 1.2 V: up to 3.65 mV |
| mismatch | σ 3.8 mV (0.486 … 0.501 V, 100 seeds); adds to the S2D's own offset σ 5.25 mV → 6.5 mV | tt, 27 °C, 3.3 V |
| supply current | 5.5 µA + 5.0 µA reference | |
| output impedance | 18 … 28 kΩ | |
| enable to 1 % | 0.19 … 1.07 µs (OA core: up to 25 µs) | |
| disabled | vref 0.000 V, current ≤ 10 nA | 3.6 V, tt / ff, 27 / 125 °C |

**Against a divider.**
- **Current:** a divider giving 0.494 V at the same 21 kΩ draws 19.9 µA, against 10.5 µA here (0.5×).
- **Supply:** a divider moves with iovdd (±45 mV over 3.0 … 3.6 V). For a ground-referenced input that is input
  offset.
- **Temperature:** it stays at 0.5 V when hot, where the S2D input needs ≥ 0.55 V.

## Not done, limitations

- **The S2D's zero follows temperature by design:** vref rises from 0.44 to 0.59 V between −40 and 125 °C (about
  +0.9 mV/K). For a ground-referenced external signal that is a temperature-dependent input offset of the same size,
  which the pad turns into twice that at its output. The alternative was a flat 0.5 V that is not linear at
  ff / 125 °C.
  - vref is not observable at a pin unless routed out (for example to the analog bus).
- **The process spread at 27 °C is ±11 mV, mismatch σ 3.8 mV:** comparable to the pad's own offset.
- **Layout:** not started (floorplan in `docs/replica_bias/SUMMARY.md`). Gate area 564 µm², half of it the two bypass
  capacitors.
- **Extracted views:** none.
