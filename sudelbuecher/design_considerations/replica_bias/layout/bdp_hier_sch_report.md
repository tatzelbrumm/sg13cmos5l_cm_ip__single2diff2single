<!--
SPDX-FileCopyrightText: 2026 Christoph Maier
SPDX-License-Identifier: Apache-2.0
-->
# bias_dist_pd: layout hierarchy backannotated into the sheets (Claude, 2026-11-08)

Sources (truth): macros/hv_logic/netlist/source/hv_logic.spice (tg_hv), macros/bias_dist_pd/netlist/source/bias_dist_pd.spice
(bdp_slice; bias_dist_pd with Xsi0..3 / Xso0..3).

## New cells
- hv_logic/schematic/xschem/tg_hv.sch / .sym: wired as in inv_hv. P above N in one column with a between them; the b
  loop on the right; bulks leave by a 20-unit stub and go to the vdd / vss rails. Drawn as in the source (N d = a,
  P d = a), no D/S swap. Symbol: bow tie a - b, en on top, en_b with a bubble below, vdd / vss at the right corners. Pin
  order vdd vss en en_b a b.
- bias_dist_pd/schematic/xschem/bdp_slice.sch / .sym: nand2_hv XA -> inv_hv XB -> tg_hv XT, left to right. e runs from
  the inverter over into the TG's en; e_b runs from the NAND under the inverter into en_b. Gate and TG supplies join
  vdd / vss by label: wired, the a line would cross them, which is the same reasoning as before in bias_dist_pd.
  Symbol: en_3v3 / en / a on the left, b on the right at a's height, vdd on top, vss below, a small TG on the a-b line.
  Pin order vdd vss en_3v3 en a b.

## bias_dist_pd.sch (same file name, same .sym)
- The 8 flat legs (nand2_hv, inv_hv, TIN/TIP and TON/TOP) were replaced by Xsi0..3 and Xso0..3 (bdp_slice). Their
  internal wiring, labels, bulk trunks and iout junctions were removed. The [D] / [S] boxes became
  "[S] input slices (bdp_slice)" and "[S] output slices (bdp_slice)".
- Inputs: en_3v3 trunk -> en_3v3; en_in<k> / iin<k> ports straight in; b -> ni trunk. Outputs: po<j> lines straight into
  a, b -> iout<j> port; en_3v3 / en_out<j> by label as before. TDN, SVPD, the mirror, PD / PO and [DM] are unchanged.
  The rails were trimmed to their last connection; the header line about the legs was updated.

## Checks (netlisted with each macro's xschemrc)
- gen_sheet.py --check: tg_hv: ports equal, devices 2 = 2, 0 mismatches. bdp_slice: ports equal, devices 0 = 0,
  instances 3 = 3, 0 mismatches. bias_dist_pd: ports equal, devices 13 = 13, instances 8 = 8, 0 mismatches.
- --log: xschem exit 0 and 0 "Error:" lines for all three sheets; 0 "IS MISSING".
- sch_lint.py (--lib hv_logic, bias_dist_pd, devices): no group carries two names, 0 missing symbols. Crossings
  without a junction: tg_hv 2 (b over the bulk verticals), bdp_slice 1 (a over e_b), bias_dist_pd 9.
- Renders (looked at): hv_logic/schematic/tg_hv.png/.svg, bias_dist_pd/schematic/bdp_slice.png/.svg and
  bias_dist_pd.png/.svg.
- simulations/ removed in hv_logic and bias_dist_pd. One under bias_dist_pd/schematic/xschem (dated 2026-11-07 23:05,
  empty) was already there before this task; it was removed too.
