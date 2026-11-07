<!--
SPDX-FileCopyrightText: 2026 Christoph Maier
SPDX-License-Identifier: Apache-2.0
-->
# Replica bias, Phase 2b: one bias tree for both blocks (2026-11-07)

Notes for `macros/pad_ref_rb`, `macros/vcm_rb` and `macros/vref_s2d_rb` on design branch `claude/c4-replica-bias`.
Cloud session C4, day 2. Commands: `docs/replica_bias/RUNLOG.md` rows 35–43. Logs: `../../../logs/replica-bias/phase2b_*`.

## 1. The question and the choice

Christoph, inspecting the blocks: both expect an input current; could they share the bias voltage generation tree if
they sit close to the circuits that use the voltages?

- **Option A (chosen):** one tree for both replica blocks. Saves one 5 µA reference leg and two 2 µA line legs
  (33 → 24.1 µA for the pair), all inside the new cells, with no pad change. Cost: the blocks become one cell, and
  the lines cross from the tree to the blocks as gate voltages. That breaks the project rule that bias crosses
  between cells only as current. The rule protects against supply differences between a diode and its users; on one
  rail a few tens of µm apart that difference is negligible.
- **Option B (not taken):** use the pads' own trees. It needs new pad ports (layout, LVS, harness interface), and
  vcm cannot hang on a tree that switches off with its pad.

## 2. Why the DC results did not move at all

The tree's lines drive gates only, so the currents in the blocks are the same whether each block has its own tree
or both share one. rb_dc, the closed loops, the round trip and the S2D window reproduce the 2026-11-06 values to the
last printed digit (135 PVT points for rb_dc). What changed:
- **Current:** 19.1 µA in the cell + 5.0 µA reference = 24.1 µA (was 33).
- **Enable:** the vcm overshoot fell from +0.19 to ≤ +0.04 V (harness reference) and from +0.48 to ≤ +0.23 V (OA
  core). vref settles a little later (0.34 … 0.52 µs instead of 0.19 … 0.31 µs): one BNC diode at 2 µA now charges
  the gates of CY and F1–F4, five 15/3 fingers.
- **Mismatch:** vcm σ 6.5 → 5.3 mV, vref 3.8 → 3.7 mV (100 seeds each). The seeds fall on a different device set,
  so the samples are not paired; the vcm difference is not traced.
- **vref has no enable of its own any more:** pulling vref low while the tree runs would short the followers F from
  vbnc to vss. SPD stays, acting only while the whole cell is off.

## 3. Christoph's hand-compacted sheets, and a short

Christoph compacted both agent-drawn sheets by hand (`b4cd2288`) and asked for a sanity check ("I tend to sneak
shorts in as I compact schematics").
- `make check-sheet` against the netlists: in vref_s2d_rb only TGP differed, drain and source swapped on purpose. In
  vcm_rb BT, BA and BB had their tail node `bt` merged into `m`.
- **The short:** the `m` wire to BA's gate ran on along y −690 through BA's bulk pin into the jog that tied BA's
  bulk to `bt`. xschem joins every pin and wire end lying anywhere on a wire. Christoph fixed it (`d0638017`).
- The TGP swap was backannotated into the netlist (drain ni, source iref).
- The schematic agent then cut the sheets onto the shared tree from his versions and wrote what his edits teach into
  the skill (notes branch `Claude/skills/xschem-analog-schematic/`, with `sch_lint.py`, which finds this short by
  itself).

## 4. Questions answered on the way

- **xschem's "finger width / length is too big":** the PDK's `fet_drc` (hv w/ng ≤ 10 µm, l ≤ 10 µm) is the
  characterized range, not a model limit. CY / F1–F4 (15/3) and the 12×12 capacitors are the pads' own devices,
  whose sheets size them with expressions that `fet_drc` skips. Kept: the replica must match the pad.
- **Why the 12×12 capacitors:** CB is the 5T OTA's dominant pole and holds vcm against the S2D's enable kick (G6:
  ±70 mV through 10 kΩ); CB1 / CB2 bypass the 20 kΩ follower against the pad's input steps (G6: ≥ 1 pF above
  10 kΩ). They are the S2D's load-capacitor primitive. At vref they are barely inverted: 0.20 … 0.43 pF each, not the
  0.61 pF they give at 1.26 V. A PMOS to iovdd gives 0.64 pF at any voltage but couples iovdd in. Christoph: room at
  the bottom of slot 7 for PMOS capacitors to iovdd; open which rail. The answer: the pads' unit rail, which the cell
  must sit on anyway.
- **Bias distribution:** the OA and BG cores give one current. `bias_dist_pd` (3 in, 4 switchable 1 : 1 out) serves
  S2D, D2S and pad_ref_rb from one source, but is a sheet only and has never been simulated.

## 5. Layout primitives

`macros/pad_ref_rb/layout/primitives/`: every device of pad_ref_rb has a device cell of the same W / L / ng in the
s2d pad layout, and the pad's rows map almost one to one (tree rows, tails, tubs, cascode row with BNC, sink row,
load-capacitor row). Only the three 1/4 PMOS averaging diodes in their own wells need a new small tub. The pads'
floorplan and assembly agent was F of session C3 (`sg13cmos5l_IOPadSingle2Diff_build/agents_c3/F/`, building on F2
of C2); its brief is the model for the pad_ref_rb assembly.
