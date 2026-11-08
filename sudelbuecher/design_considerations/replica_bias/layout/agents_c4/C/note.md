<!-- SPDX-FileCopyrightText: 2026 Christoph Maier / SPDX-License-Identifier: Apache-2.0 -->
# s7_ctrl layout: note (Claude, agent C, C4 2026-11-08)
[M] = measured (logs/summary.txt), [R] = reasoning. Rebuild: `python3 src/build_s7c.py <dir>` (LayoutDiff-identical; the GDS header holds a timestamp, so sha256 changes). Checks: `src/run_checks.sh`.

## Structure (s7_ctrl.png), 71.60 x 38.04 um = 2724 um2 [M]
- Bottom: 7 `efs_ls_core` (E's ls_up_fs core, unchanged), mirrored in y so that in / out / out_b face the channel; 0.40 um gaps, filled with NWell (one well) and bridged in M1 (vss strips, vddh rails). Left to right: XL0..XL5, XLE.
- Channel C1: 10 M1 tracks (pitch 0.39), assigned by left-edge with vertical constraints; M2 stubs only vertical.
- One row of D's cells (row height 5.99): 7 pairs nand2+inv (V, S, F, M, 1, 2, 3), 5 groups nand2+inv+TG+TG (LD, LX, SB, BD, RC), NE at the end. Offsets and glue are D's bdp_slice ones (nand->inv 1.66 shared diffusion, y->a M1 bar; inv->TG 1.38; TG->TG 1.36; TG->nand 1.34). In a group the e / e_b poly bars of D's slice run on over the second TG (no M1 for TG enables).
- Channel C2: 4 M1 tracks for outp, outn, vinp, vinn, bus0, bus1; vcm_* / vref_* go straight up from T9 / T10.
- Count [M]: 222 devices = 7 x 18 (ls_up_fs) + 13 x 4 + 12 x 2 + 10 x 2.

## Pins (s7_ctrl_pins.txt; origin lower left)
- Bottom edge, Metal2 0.20 wide: d0..d5, enable (each under its shifter, drop at x = LS + 0.395).
- Top edge, Metal2: outp, outn, bus0, vinp, bus1, vinn, vcm_rb, vcm_pad, vref_rb, vref_pad (0.29 wide), en, en_b (0.20 wide).
- vss: Metal1 strap on the left edge (x 0..0.30, y 26.72..31.40); vddh: Metal1 strap on the right edge (x 71.30..71.60, y 0.62..36.00).
- Each supply joined in metal: vss strap joins the LS vss strips and the row's vss strip, vddh strap the LS vddh rails and the row's vdd strip. Metal-only check: exactly 2 supply nets [M].

## Cells
- Copied unchanged with their names: bdp_nand2_hv, bdp_inv_hv, bdp_tg_hv (+ bdp_*mosHV children) from bias_dist_pd.klay.gds; efs_ls_core (+ efs_* children) from ls_up_fs.klay.gds. 14 / 14 identical in shapes, texts and instances [M]. No new subcells: routing, glue poly, NWell fill and one ThickGateOx box over the whole cell are top-level shapes of s7_ctrl. ls_up_fs (the labelled top of E's file) is not used, so its labels do not reach this cell.

## Checks [M]
- run_drc.py --no_density --mp=4: no violations, 0 "exception"; maximal deck + latchUpRules=true: 0.
- run_lvs.py --disable_tap_extraction vs s7_ctrl.cdl: Netlists match. Negative (XT1 en / en_b swapped): don't match.
- sym_check N: 0 narrow-poly hits; contacted poly outside Activ >= 0.45 um. Its mirror-XOR figure does not apply (no matched rows).
- s7_ctrl.cdl = s7_ctrl (slot_7.spice) + ls_up_fs (en_ctrl_3v3.spice) + hv_logic.spice; the X lines of sg13_hv_nmos / pmos are written as M lines (the KLayout CDL reader treats X sg13_hv_* as calls to subcircuits that do not exist: 0 schematic devices).

## Open points
1. Unused shifter outputs (sw_b, mon_b, fd_b, k1_b, k0, ex_b) end on their LS pins, as in the netlist. No PEX.
2. NWell reaches the bottom edge (LS wells): keep 0.62 um NWell spacing to other wells when the cell is placed, or abut a vddh well.
3. Logic row is 52.8 um long, the shifters 70.2 um; the space right of NE carries only en / en_b and the vddh strap.
