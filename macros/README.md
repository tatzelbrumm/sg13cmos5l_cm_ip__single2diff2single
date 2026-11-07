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
| `bias_tree_out_pd` | `bias_tree_pd` for a reference current *out of* iref (PMOS input diode PI; = `bias_out_pd` without its inverter), pin-compatible with `bias_tree_pd`; for a distribution with NMOS-sink outputs | sheet + source, 2026-10-28, netlist-checked; not used yet |
| `bias_sel_noab_pd`, `bias_tree_noab_pd` | the same without the class-AB branches, for the s2d pad (since 2026-10-28 the pad uses `bias_gen_pd` + `bias_tree_noab_pd`) | sheets, 2026-10-27; netlist-checked against `bias_sel_pd` / `bias_tree_pd` |
| `oa_core_pd`, `bg_core_pd` | the Oguey–Aebischer and the Banba bandgap core, sourced reference current out | sheets (from `bias_sel_pd`) |
| `bias_gen_pd` | `bias_sel_pd` without the tree: selectable reference current, in both pads (`xg`, next to the tree `xt`) since 2026-10-28, or in the slot's main area | sheet, 2026-10-27; on its own not simulated |
| `bias_dist_pd` | switchable distribution mirror, 3 inputs, 4 outputs, one per pad tree | sheet, 2026-10-27, not simulated |
| `pad_ref_rb` | replica bias of the custom pads' reference voltages in one cell: the shared bias tree `bias_tree_rb` (own sheet in this macro) feeding `vcm_rb` and `vref_s2d_rb`; one 5 µA reference (a `bias_dist_pd` leg), one enable | 2026-11-07: sheets + source, `make check-sheet`; CACE 8 / 8 groups pass (schematic); layout primitives collected from the s2d pad cell (`layout/primitives/`), no layout |
| `vcm_rb` | replica bias for the pads' internal common mode (S2D `vcm` = D2S `vref`), centred in the band where both pads stay linear; also holds the block / closed-loop / gap-run testbenches of the replica bias task (`testbenches/`, `docs/replica_bias/`) | 2026-11-06 / 07: sheet + source, `make check-sheet`; characterized through `pad_ref_rb` |
| `vref_s2d_rb` | replica bias for the S2D pad reference `vref`, about 0.5 V, rising with temperature as the S2D input edge does | 2026-11-06 / 07: sheet + source, `make check-sheet`; characterized through `pad_ref_rb` |
| `bias_in_pd`, `_out_pd`, `_oa_pd`, `_bg_pd` | the four reference circuits on their own (flat, with the tree), with power-down; class-AB stacks as CACE fixtures since 2026-10-27 | sheets (from `power_down/xschem`) + CACE |
| `en_ctrl_3v3` | `en_3v3 = en_1v2 ∧ vdd_1v2 present ∧ vdd_3v3 present`, level-shifted select bits | sheets + CACE |
| `ls_up_1v2_3v3`, `ls_dn_3v3_1v2` | level shifters (from `ls_pair`) | sheets + CACE |
| `ocd_ls_up_1v2_3v3`, `ocd_ls_dn_3v3_1v2` | level shifters taken from the chipalooza harness, port-compatible with the two above: up = harness `sw_lvl_shift` behind its two-inverter input stage, down = harness `hv_inv_1` on the 1.2 V rail (the harness has no dedicated down-shifter). Sizes differ from `ls_up_1v2_3v3` / `ls_dn_3v3_1v2` | 2026-11-03: sheets + source, text-checked; CACE suite and testbenches derived from the `ls_*` ones, **not run**; no layout |
| `ocd_analog_switches` | the harness's analog switches / transmission gates `analog_switch_small`, `analog_switch_med`, `analog_pswitch_small`, `xgate` (+ `sw_lvl_shift`, `gate_drive_med`): byte-identical copies of the harness sheets, for gating internal analog nodes and the `analog_bus` pins of slot 7 | 2026-11-03: copies + source netlist, text-checked against the harness; **KLayout layouts** (`layout/klayout/*.klay.gds`, from the harness's Magic layouts, device-checked); not simulated, no CACE, no KLayout DRC/LVS yet |
| `hv_logic` | 3.3 V gates inv / nand2 / nor2 / nor3 | sheets |
| `IOPad` | IHP IO GDS copies, Christoph's clamp / diode sheets, and symbols of IHP IO sub-cells | unchanged + 5 new symbols |
| `OgueyAebischerBias` | the unsized sky130 port (2026-09) | superseded by `bias_oa_pd` |
| `inverter`, `counter` | template examples | still to be torn out (CLAUDE.md §7) |

**Slot-7 gating and level shifting (prepared 2026-11-03, not yet wired into `slot.sch`):** `ocd_analog_switches` (enable = 1.2 V `dig_in` bit, switch levels 3.3 V),
`ocd_ls_up_1v2_3v3` / `ocd_ls_dn_3v3_1v2` for control and status signals between the 1.2 V and 3.3 V domains. Check of the copies, source netlists and sheets:
`python3 -I scripts/check_ocd_macros.py <path to sg13cmos5l_ocd_chipalooza>` (text only; neither xschem nor a simulator has run on these macros). Its layout checks need the python module `klayout`; `python3 -I` ignores a `pip install --user` copy, so drop `-I` then. New `Makefile.new` files as above.

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
