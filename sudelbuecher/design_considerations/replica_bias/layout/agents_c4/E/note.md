<!-- SPDX-FileCopyrightText: 2026 Christoph Maier / SPDX-License-Identifier: Apache-2.0 -->
# ls_up_fs / en_ctrl_3v3 v2 layout: note (Claude, agent E, C4 2026-11-08)
[M] = measured (logs/summary.txt), [R] = reasoning. Rebuild: `python3 src/build_efs.py <dir>` (byte-identical, gds sha256 32def911 / 2c9e48fd); checks: `cd ../work && sh run_checks.sh` (copy in src/).

## Size [M]
- **ls_up_fs** 9.68 x 27.29 um = 264.2 um2 (`ls_up_fs.gds`); **en_ctrl_3v3** 9.68 x 79.49 um = 769.5 um2 (`en_ctrl_3v3.gds`). Both place the label-free core `efs_ls_core` (so en_ctrl's flat LVS sees only its own labels). Cells: efs_ls_core, efs_inv_hv, efs_xn1, efs_pmosHV_w0p3_l20, efs_pmosHV_w0p3_l5, efs_pmosHV_w1_l0p45, efs_nmosHV_w1_l0p45.

## Reuse
- D's bdp_cells.py (inv_hv, frame/strips, gate_pad, cont_row, nmos) and C3's build_s2d_p3.py (box, fill, pin, tap, mos, place) copied unchanged to src/lib/. `efs_inv_hv` = D's inv_hv: all-layer XOR 0 against `bdp_inv_hv` in macros/bias_dist_pd/layout/klayout/bias_dist_pd.klay.gds [M].
- Row = D's row stack: p+ vss strip y 0..0.30, NMOS 0.73..1.73, NWell from 2.55, PMOS 3.17..4.17, N+ vddh strip 4.60..4.90, gate pads at L2 2.04 / L1 2.66. Left to right: XN1 (efs_xn1, D's single() pattern), XI1, XI2, XI3 at 1.40 pitch.

## Leaker (XPL10..XPL1) and XPF
- 10 separate pmosHV PCells 0.3u/20u, rotated (L along y), side by side, Activ 0.25 apart (Gat.b1): one block 5.25 x 20.68 um above the row, inside the same NWell. Gates on `in`: end caps merge into one plate; contacted only by a poly tab as long as the gate (20 um, 0.60 beyond strip 0, contact column 0.30..0.46 = Cnt.e) on the left. No necks: sym_check N 0, narrowest contacted poly 0.45 um [M].
- Serpentine by M1 jumpers at alternating ends (top (0,1)(2,3)..(8,9), bottom (1,2)..(7,8)): vddh enters at strip 0's bottom straight from the row's vddh strip, x leaves at strip 9's bottom. 18 devices extracted: 10 x 0.3/20, 1 x 0.3/5, 3 + 4 x 1/0.45 [M].
- XPF 0.3u/5u (rotated) right of strip 9: drain joined to x at the bottom, source to the right tie column at its top, gate tab (net y) on its right; poly gap to the plate 0.29 >= Gat.b1 0.25.
- Ties: closed N+ ring around the block (row vddh strip, two columns, top rail; one contact column each); one NWell rectangle x 0..9.68, y 2.55..27.02, no notch. Leaker P+ <= 4 um from a tie (LU.a 20) [R]. Tie-to-strip gap 0.82 keeps every tab 0.32 wide beyond both 0.25 endcap zones (N check counts tie Activ too).
- M2 only for: in (drop from the tab to XN1's gate line), x (XN1 drain riser, track under the block onto the strip-9/XPF jumper), y (XI1 riser, track over the vddh strip, rise to XPF's tab), out_b (over XI3, Via1 down to M1 at the edge). Metal1 / Metal2 only.

## Pins (Metal1 unless noted)
- ls_up_fs: in left (0,1.97;0.5,2.32); out right (9.18,1.97;9.68,2.23); out_b right (9.18,2.61;9.68,2.87); vddh top rail y 26.10..26.40; vss bottom strip y 0..0.30.
- en_ctrl_3v3: XE (bottom), XS0 (mirrored, shares XE's vddh rail), XS1 (shares XS0's vss strip): rails vss | vddh | vss | vddh. Inputs left: en_1v2 y 1.97, sel0_1v2 y 50.18, sel1_1v2 y 54.17; outputs right: en_3v3 / en_3v3_b y 1.97 / 2.61, sel0_3v3 y 50.27, sel1_3v3 y 54.17; vddh y 26.10 / 78.30, vss y 0 / 52.20. sel0_b / sel1_b internal, no labels.
- Supplies joined in metal: M2 vddh strap at the left (x 0.67..0.96, XE/XS0 rail to XS1's rail), M2 vss strap at the right (x 8.80..9.09, XE's strip to the XS0/XS1 strip). Metal-only check: exactly 2 supply nets, vddh and vss [M] (without the vss strap they met only through the substrate [R]).

## Unconnected ports (vddl, vdd1v2_sense, vdd3v3_sense)
- Labelled isolated Metal2 stubs 0.40 x 0.40 (Mn.d) at the left edge, y 12.0 / 13.0 / 14.0, no Via1. The deck's simplify drops pin-only nets on both sides, so LVS matches with the stubs and also without them [M]; the stubs only give the ports a physical pin for the abstract / hookup. No ignore option needed.

## Checks [M] (both top cells)
- run_drc.py --no_density --mp=4: no violations, 0 "exception"; maximal deck + latchUpRules=true: 0 / 0.
- run_lvs.py --disable_tap_extraction vs the xschem CDLs (ls_up_fs.cdl, en_ctrl_3v3.cdl, netlisted with the Makefile's klayout-lvs-netlist command into the workspace): Netlists match / match. Negative LVS (XPF gate y -> in; XS0/XS1 outputs swapped): both don't match.
- sym_check N: 0 narrow-poly hits on ls_up_fs, efs_ls_core, efs_inv_hv, efs_xn1, en_ctrl_3v3 (mirror XOR not applicable: no matched rows).
- Rules from sg13cmos5l_tech_default.json / sg13cmos5l_maximal.drc texts: Gat.b1 0.25, Gat.d 0.07, Cnt.e 0.14, pSD.d1 0.03, NW.e1 0.62, NW.c1 0.62, TGO.a 0.27, M1.b 0.18, Mn.b 0.21, Mn.d 0.144, LU.a 20, LU.c/d 6.

## Open points
1. en_ctrl_3v3 is tall (9.68 x 79.49); abutting the three side by side (28 x 27) would need the inputs of XS0 / XS1 routed across XE.
2. The row right of XI3 (x 6.2..9.4) is tie strip only; the width is set by the leaker block. No PEX.
