<!--
SPDX-FileCopyrightText: 2026 Christoph Maier
SPDX-License-Identifier: Apache-2.0
-->
# vcm_rb: replica bias for the pads' internal common mode (S2D vcm = D2S vref)

One voltage for both custom pads:
- the internal common mode `vcm` of `sg13cmos5l_IOPadSingle2Diff` (S2D);
- the reference `vref` of `sg13cmos5l_IOPadDiff2Single` (D2S), which must equal the D2S input common mode. In the chain
  that common mode is the S2D output's, so one net serves both.

`vcm` sits at the centre of the band in which both pads stay linear (INL ≤ 2 mV with ±0.5 V on their unit gates). It
follows that band with process, temperature, iovdd and the reference current, by replicas of the devices that set
the band's two edges.

Since 2026-11-07 it hangs on the shared bias tree `bias_tree_rb`, which also feeds `vref_s2d_rb`; both sit in the cell
`pad_ref_rb` (`../pad_ref_rb`), made from one 5 µA reference current (bias_gen_pd's `iref`, a bias_dist_pd output, or a
core's `iout`) with one enable. Until then each block had its own copy of the tree and its own reference (the user's
option A of the question on sharing; the DC outputs are the same to the last printed digit, rb_dc).

Task: `docs/launch/replica_bias_TASK.md` (branch `harness-test`). Survey and run log: `docs/replica_bias/`. Design notes
on the notes branch (`sudelbuecher/design_considerations/replica_bias/`).

## Function

The band (gap runs G1, G3, G10; `testbenches/pad_char/results/`):

- **Top edge:** a `unit_r2` tail (hv PMOS 5u/6u at vbp) leaves saturation as the input follower (20u/1u ng=2) raises
  its source. It is the same in both pads, at about iovdd − 1.25 V on the top gate at ss / −40 °C.
- **Bottom edge:** the S2D fold cascode CX / CY (30u/3u at vbnc) leaves saturation above the fold node x. It is
  0.89 / 0.95 / 1.02 V at −40 / 27 / 125 °C, independent of corner and supply.
- **Band common to both pads:** 1.031 … 1.262 V at iovdd 3.0 V, 1.031 … 1.530 V at 3.3 V, 1.031 … > 1.65 V at 3.6 V.
  With the Oguey–Aebischer core at 125 °C (+33…42 % current) it shrinks to 1.126 … 1.244 V at 3.0 V.

The replicas, on the lines of the shared tree `bias_tree_rb`:

| node | replica | relation to the band (fits on the bias copies, `testbenches/spice/explore_edges.py`) |
|---|---|---|
| gh | TR (5u/6u at vbp) → MR (20u/1u ng=2, diode) → sink 2 × 2.4u/6u (4 µA = 0.8 of TR) | gh = top gate limit + 0.157 V (±18 mV) |
| xp | one CY finger (15u/3u at vbnc) on SY (6u/6u, 5 µA) | bottom edge = xp + 0.559 V (±34 mV) |
| m | three identical PMOS diodes 1u/4u in their own wells: one from gh to m, two in parallel from m to xp | m = centre of the band (−65 … +78 mV over all PVT and references, `explore_vcm_rb.py`, candidate G) |
| vcm | 5-transistor OTA in unity gain: pair = the unit input device 20u/1u ng=2, tail = the unit tail 5u/6u (5 µA), NMOS mirror 6u/6u; CB = 12u × 12u hv NMOS capacitor | vcm = m (offset −0.9 mV at tt) |

**Lines** (`bias_tree_rb` in `../pad_ref_rb`, as bias_tree_pd, at the pad devices' current densities):
- ni: NI, 6u/6u NMOS diode, the reference;
- vbp: BP, 2u/6u PMOS diode at 2 µA, fed from NBP 2.4u/6u;
- vbnc: BNC, 1u/8u NMOS diode at 2 µA, fed from PBNC 2u/6u.

Every device is an hv MOS of a size used in the pads. No resistor is used.

**Disabled** (`en_3v3` = 0 on `pad_ref_rb`): the tree's transmission gate TGN / TGP opens the reference and TDN pulls ni
to vss, so every current is off. SPD (gate `en_3v3_b`) pulls `vcm` to vss.

- `vcm` is the S2D's output level while it is off ("input of the next stage to VCM if off"). So this block must stay
  on as long as any user of `vcm` runs, and must not share the S2D pad's enable.

## Ports

| port | dir | |
|---|---|---|
| vdd, vss | inout | iovdd / iovss of the pads it serves. The top edge is referenced to the pads' unit rail, so place the block on the same rail. |
| ni, vbp, vbnc | in | the lines of `bias_tree_rb` (gates only) |
| vcm | out | to S2D `vcm` and D2S `vref` (gates only, plus the S2D's output ties while it is off) |
| en_3v3_b | in | complement of the 3.3 V enable (en_ctrl_3v3), gate of SPD |

`pad_ref_rb`'s ports: `vdd vss iref vcm vref en_3v3 en_3v3_b` (`iref`: 5 µA, **sourced** into the cell).

## Files

```
netlist/source/vcm_rb.spice        source netlist (mm_ok=1 on every device, as the pads' sheets)
schematic/xschem/vcm_rb.sch/.sym   sheet drawn by hand from the source netlist (2026-11-07, xschem-analog-schematic skill,
                                   compacted by hand by Christoph, then moved onto the shared tree); make check-sheet netlists
                                   it with xschem and compares it device by device (16 = 16, ports equal)
schematic/vcm_rb.png / .svg        render of the sheet
schematic/gen_sheet.py             only its --check mode is in use; generating would overwrite the hand-drawn sheet
../pad_ref_rb/verification/        CACE suite of pad_ref_rb (gen_cace.py), which covers this block; make sim-cace here runs it
verification/baseline/cace_own_tree/  CACE results of 2026-11-06, with the block's own tree
verification/baseline/             G7: D2S CACE on the current schematic at vref = vicm = 1.2 V and 1.65 V, loop fixture;
                                   run_cace_copy.py (temporary yaml copies; the pad macros stay unchanged), run_g7_g8.sh
testbenches/pad_char/              gap runs G1-G6, G9, G10 (run_pad_char.py, analyze_bands.py, results/*.tsv)
testbenches/rb_char/               block and closed-loop runs of pad_ref_rb (run_rb.py, results/*.tsv)
testbenches/spice/                 explorations: explore_edges.py, explore_vcm_rb.py (results/)
```

`make sim-cace`, `make check-sheet` and `make sim-char` run in the repo environment (`export PDK_ROOT=/foss/pdks; source
.designinit`).

## Results (schematic, ngspice-47, CACE 2.11.0; on the shared tree, 2026-11-07)

Every DC value is the same as with the block's own tree (2026-11-06) to the last printed digit: the tree's lines are
gates, so sharing them changes no current. CACE: `../pad_ref_rb/verification/cace/results/pad_ref_rb/`, 8 / 8 groups
pass.

| quantity | result | condition |
|---|---|---|
| vcm | 1.120 … 1.193 / 1.242 … 1.295 / 1.289 … 1.395 V | iovdd 3.0 / 3.3 / 3.6 V, 5 MOS corners, −40 / 27 / 125 °C, harness reference |
| margin to the band of both pads | ≥ +40 mV (Oguey–Aebischer core, ff, 125 °C, 3.0 V: band 1.126 … 1.244 V, vcm 1.204 V); ≥ +142 mV with the harness reference | every PVT point, references 0 / 1 / 2 (rb_dc against G1 / G3 / G10) |
| mismatch | σ 5.3 mV (1.248 … 1.275 V, 100 seeds; with the own tree 6.5 mV; the seeds fall on a different device set, so the two samples are not paired, and I have not traced the difference) | tt, 27 °C, 3.3 V |
| supply current | 13.5 … 13.7 µA in the block, plus the shared tree's 3.9 µA and the 5.0 µA reference (OA core: block 8.2 … 20.0 µA) | |
| output impedance | 22 … 35 kΩ (1 kHz and 1 MHz) | 3.0 … 3.6 V, ss / tt / ff, −40 … 125 °C |
| enable to 1 % | 0.31 … 1.00 µs (OA core: up to 20.5 µs, the core's start-up); overshoot ≤ +37 mV (OA: ≤ +0.23 V; with the own tree +0.19 / +0.48 V) | en_1v2 edge |
| start-up | settled ≤ 9.9 µs after a 10 µs iovdd ramp starts (OA: ≤ 23 µs) | |
| disabled | vcm 0.000 V, current ≤ 1 nA (DC) | 3.6 V, tt / ff, 27 / 125 °C |

**Closed loop** (pads with this block instead of an ideal source; `testbenches/rb_char/results/cl_*`):

| | with vcm_rb | with an ideal 1.2 V |
|---|---|---|
| S2D INL, u = ±0.5 V (vref from vref_s2d_rb) | ≤ 1.28 mV (OA: 1.73) | ≤ 3.65 mV at vref 0.5 V (ff, 125 °C) |
| D2S INL, vd = ±1 V | ≤ 0.64 mV (OA: 1.72) | ≤ 0.65 mV |
| round trip S2D → D2S | gain 0.995 … 0.999, INL ≤ 0.75 mV | INL ≤ 3.14 mV |
| S2D enable time | 1.39 … 1.44 µs | 1.40 … 1.42 µs |

**Against a divider.**
- **Current:** a resistive divider giving the same 1.26 V at the same output impedance (27 kΩ) draws 28.8 µA. Here:
  13.6 µA in the block plus its share of the tree and reference; for both references together see
  `../pad_ref_rb/README.md` (24.1 µA against 48.7 µA for two dividers).
- **Tracking:** a divider from iovdd is ratiometric and cannot follow the band. It gives 1.09 V at 3.0 V, below the
  band with the OA core at 125 °C (bottom edge 1.126 V).

## Not done, limitations

- **Layout:** not started. Primitives collected and a row plan in `../pad_ref_rb/layout/primitives/README.md`.
- **Overshoot at enable:** ≤ +37 mV on vcm, up to +0.23 V with the OA core (it was +0.19 / +0.48 V with the own
  tree). The buffer comes up before the average m. The pads enabled together with the block still meet their enable
  time. If the overshoot matters, enable the pads after the references.
- **D2S output offset:** with the OA core at ff / 125 °C / 3.0 V it is 5.5 mV (limit 5 mV). This is the same with an
  ideal 1.2 V reference, so it is a property of the D2S pad, not of this block.
- **Extracted views:** none.
- **Closed loop in CACE:** done in ngspice decks with the CACE templates' measurement code (validated to the last
  digit), not with CACE templates of the pads.
- **Round trip:** the deck with both blocks inside does not converge. The round trip uses ideal sources at the blocks'
  DC outputs, which is exact at DC because the pads draw no DC current from vref / vcm.
