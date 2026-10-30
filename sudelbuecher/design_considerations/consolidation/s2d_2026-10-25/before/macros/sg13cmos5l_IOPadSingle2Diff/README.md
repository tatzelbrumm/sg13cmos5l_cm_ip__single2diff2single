<!--
SPDX-FileCopyrightText: 2026 Christoph Maier
SPDX-License-Identifier: Apache-2.0
-->
# `sg13cmos5l_IOPadSingle2Diff` — single-ended-in, differential-out buffered input pad (SCAFFOLD)

`outp - vcm = vcm - outn = pad - vref`. The counterpart of `../sg13cmos5l_IOPadDiff2Single`, built
on the same structure (2026-10-20). **The amplifier is a behavioural placeholder**; what remains to
be designed is listed in [`FILL_IN.md`](FILL_IN.md).

| file | contents |
|---|---|
| `schematic/xschem/sg13cmos5l_IOPadSingle2Diff.{sch,sym}` | top sheet: `xc` en_ctrl_3v3, `xb` d2s_bias_sel_pd, `xa` s2d_core_ideal (placeholder), IHP input protection CP CN DN DP SP |
| `schematic/xschem/s2d_core_ideal.{sch,sym}` | the placeholder: two E sources |
| `schematic/xschem/xschemrc` | PDK + this folder + the sub-macros (`../../../<macro>/schematic/xschem`) |
| `netlist/source/sg13cmos5l_IOPadSingle2Diff.spice` | reference netlist of the sheet |
| `verification/cace/` | yaml (dc, range, ac, pd; limits `any`) and templates |
| `Makefile` | `make sim-cace`, `make spec-table` (scheme of `../ls_up_1v2_3v3`) |

Ports, control, bias and power-down behave as in `../sg13cmos5l_IOPadDiff2Single/README.md`
(same `en_ctrl_3v3` and `d2s_bias_sel_pd`, same ring rails). In the slot fallback
(`../slot/schematic/xschem/slot.sch`) the pad pin is `s7_an_0_esd`.

Verified: the sheet netlists with xschem 3.4.8RC to the reference netlist (no missing symbol); the
CACE scaffold's results are in `verification/cace/results/` and describe ideal E sources only.
