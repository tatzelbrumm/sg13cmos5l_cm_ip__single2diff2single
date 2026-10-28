<!--
SPDX-FileCopyrightText: 2026 Christoph Maier
SPDX-License-Identifier: Apache-2.0
-->
# Macros of `sg13cmos5l_cm_ip__single2diff2single` — index (2026-10-20)

How the slot-7 design is put together, bottom up. Every macro folder has its own `README.md`;
those with a CACE suite run it with `make sim-cace` and print their limit table with
`make spec-table` (results in `verification/cace/results/<cell>/`, the scheme of
`chipalooza2/levelshifters/ls_pair`). New Makefiles arrive as `Makefile.new` (the remote tools may
not write a file named `Makefile`): `for f in macros/*/Makefile.new; do mv "$f" "${f%.new}"; done`.

```
slot  (slot7_wrapper-compatible; fallback wiring of both pads)
├── sg13cmos5l_IOPadSingle2Diff   (input pad: matched-pair DDA s2d_mpdda_pd, gain 2)
│   ├── s2d_mpdda_pd ── s2d_mpdda ── unit_r2 (in sg13cmos5l_IOPadDiff2Single)
│   ├── en_ctrl_3v3 ── ls_up_1v2_3v3, hv_logic
│   ├── bias_gen_pd ── hv_logic, oa_core_pd, bg_core_pd
│   ├── bias_tree_noab_pd
│   └── IOPad (IHP IO sub-cell symbols: clamps, diodes, secondary protection)
└── sg13cmos5l_IOPadDiff2Single   (output pad: class-AB driver d2s_mpdda_pd)
    ├── en_ctrl_3v3
    ├── bias_gen_pd ── hv_logic, oa_core_pd, bg_core_pd
    ├── bias_tree_pd
    └── IOPad (DCNDiode, DCPDiode)
```

| macro | what | status 2026-10-20 |
|---|---|---|
| `sg13cmos5l_IOPadDiff2Single` | differential in, single-ended out, class-AB pad, gain 1/2; selectable bias, fail-safe enable | sheets + CACE (13 groups + loop fixture), limits proposed; no layout (size mockup only) |
| `sg13cmos5l_IOPadSingle2Diff` | single-ended pad in, differential out, outp − outn = 2 (pad − vref) | 2026-10-25: input buffer of `s2d_input_buffer` consolidated; sheets + CACE (14 groups + loop fixture), limits proposed; open points in `FILL_IN.md`; no layout |
| `slot` | slot7_wrapper frame (layout = harness frame) with both pads, fallback wiring | sheet; `README.md` lists the harness changes for the custom-padframe route |
| `bias_sel_pd` | `bias_gen_pd` + `bias_tree_pd` in one cell: one mirror tree, reference = harness ibias / Oguey–Aebischer / bandgap. The pads' bias until 2026-10-28; since then the pads instantiate `bias_gen_pd` and the tree side by side (same devices), and this cell stays as the reference for its CACE results | sheets + CACE |
| `bias_tree_pd` | the mirror tree with four bias diodes and the class-AB currents vabp / vabn (their stacks are in `d2s_mpdda_pd` since 2026-10-27), one sourced reference in; also the home of the bias source netlists | sheets (from `bias_sel_pd`) |
| `bias_sel_noab_pd`, `bias_tree_noab_pd` | the same without the class-AB branches, for the s2d pad (since 2026-10-28 the pad uses `bias_gen_pd` + `bias_tree_noab_pd`) | sheets, 2026-10-27; netlist-checked against `bias_sel_pd` / `bias_tree_pd` |
| `oa_core_pd`, `bg_core_pd` | the Oguey–Aebischer and the Banba bandgap core, sourced reference current out | sheets (from `bias_sel_pd`) |
| `bias_gen_pd` | `bias_sel_pd` without the tree: selectable reference current, in both pads (`xg`, next to the tree `xt`) since 2026-10-28, or in the slot's main area | sheet, 2026-10-27; on its own not simulated |
| `bias_dist_pd` | switchable distribution mirror, 3 inputs, 4 outputs, one per pad tree | sheet, 2026-10-27, not simulated |
| `bias_in_pd`, `_out_pd`, `_oa_pd`, `_bg_pd` | the four reference circuits on their own (flat, with the tree), with power-down; class-AB stacks as CACE fixtures since 2026-10-27 | sheets (from `power_down/xschem`) + CACE |
| `en_ctrl_3v3` | `en_3v3 = en_1v2 ∧ vdd_1v2 present ∧ vdd_3v3 present`, level-shifted select bits | sheets + CACE |
| `ls_up_1v2_3v3`, `ls_dn_3v3_1v2` | level shifters (from `ls_pair`) | sheets + CACE |
| `hv_logic` | 3.3 V gates inv / nand2 / nor2 / nor3 | sheets |
| `IOPad` | IHP IO GDS copies, Christoph's clamp / diode sheets, and symbols of IHP IO sub-cells | unchanged + 5 new symbols |
| `OgueyAebischerBias` | the unsized sky130 port (2026-09) | superseded by `bias_oa_pd` |
| `inverter`, `counter` | template examples | still to be torn out (CLAUDE.md §7) |

Sources of the consolidated pieces (originals unchanged, in the `_sudelbuecher` worktree):
`sudelbuecher/design_considerations/class_ab_pad_driver/{improvements,power_down}`,
`sudelbuecher/design_considerations/s2d_input_buffer` and
`chipalooza2/levelshifters/ls_pair`. Record of the consolidation:
`sudelbuecher/design_considerations/consolidation/log.md`.

**Bias macros renamed 2026-10-27:** `d2s_bias_{in,out,oa,bg,sel}_pd` -> `bias_{in,out,oa,bg,sel}_pd` (the s2d pad uses
them too); the cores, the tree and the bias source netlists split off as above. Record:
`sudelbuecher/design_considerations/consolidation/bias_hierarchy_2026-10-27/`.

Not yet done at the repository level: the top cell `sg13cmos5l_cm_ip__single2diff2single` still has
its 2026-09 placeholder sheet; for the chip it has to become (or instantiate) `slot`, pin-compatible
with `slot7_wrapper`.
