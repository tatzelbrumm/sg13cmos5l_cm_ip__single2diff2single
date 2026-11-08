<!--
SPDX-FileCopyrightText: 2026 Christoph Maier
SPDX-License-Identifier: Apache-2.0
-->
# bias_dist_pd sheet and symbol brought in line with the source (Claude, 2026-11-07)

Source: macros/bias_dist_pd/netlist/source/bias_dist_pd.spice (4 inputs, vddh / vssh, [DM] dummies).

## Sheet (schematic/xschem/bias_dist_pd.sch)
- 4th input slice: XIA3 / XIB3 / TIN3 / TIP3, a copy of slice 2 moved down by the slice pitch (340), inside the
  existing [D] enable decode and [S] input switches groups. It has the same wiring as the other three slices: en_3v3
  trunk and vddh bulk trunk extended, ni onto the trunk at x 980, ports iin3 / en_in3 at the slice's height.
- To make room, the left part below the third slice moved down by 340: the [M] mirror bottom row (TDN, NI, NM),
  en_3v3_b, the vssh rail and the title block. The output side ([O], [D]/[S] outputs) was not moved; only its vssh
  trunk was stretched to the rail. en_out0..3 ports moved under the 4th slice, 40 apart.
- vdd -> vddh, vss -> vssh in the ports, every label and the wire hints. The header text now says 4 inputs, vddh / vssh.
- New group [DM] layout dummies (dashed box, magenta title, project style as in vcm_rb): MDP[1:0] (hv PMOS 5u/6u,
  gate vpd) and MDN[1:0] (hv NMOS 2u/6u, gate ni). D = S = B are joined on one vertical: MDP's goes to a vddh label,
  MDN's goes straight down onto the vssh rail. The gates take labels, because a gate wire would cross NM's
  source/bulk verticals. A note explains the convention.
- Pin instances in the .sch are in the source port order.

## Symbol (schematic/xschem/bias_dist_pd.sym)
- Pins in source port order: vddh vssh en_3v3 en_3v3_b iin0..3 en_in0..3 iout0..3 en_out0..3. Left column at a 20-unit
  pitch (-130..130), outputs on the right (-30..30), vddh at the top and vssh at the bottom (+-180), box +-160.
  Pins moved; no sheet places bias_dist_pd.sym, so no other sheet needs re-wiring.

## Checks
- gen_sheet.py --check: ports equal; devices source 29, sheet 29, 0 mismatches; gate instances source 16, sheet 16,
  0 mismatches.
- xschem --log: exit 0, 0 "Error:" lines, 0 "IS MISSING".
- sch_lint.py (--lib hv_logic, xschem devices): no group carries two names, 0 missing symbols, 53 crossings without a
  junction (the per-slice crossings of the existing drawing, plus the same ones for slice 3).
- Render: schematic/bias_dist_pd.png (3000 px) / .svg, checked at 7000 px. The simulations/ folder that xschem
  creates under schematic/xschem was removed after each run.

## Not changed
- The README still lists the ports as vdd / vss and says the sheet shows three inputs (README not in the allowed files).
