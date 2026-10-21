<!--
SPDX-FileCopyrightText: 2026 Christoph Maier
SPDX-License-Identifier: Apache-2.0
-->
# `slot` — slot7-compatible macro of `sg13cmos5l_cm_ip__single2diff2single`

Pin-compatible with `slot7_wrapper` of `sg13cmos5l_ocd_chipalooza` (branch `tatzelbranch`): the
layout frame `layout/klayout/slot.klay.gds` (537.15 × 273 µm) and `schematic/xschem/slot.sym` carry
exactly the wrapper's pins. `reference/` holds the harness views it was derived from
(`slot7_wrapper.{gds,mag,sym,v}`) and the harness pad `sg13cmos5l_IOPadAnalog.gds`.

Slot 7 has two dedicated pads, `s7_an[0]` and `s7_an[1]` (both `sg13cmos5l_IOPadAnalog` in
`config.txt`), plus `s7_an_0_esd` (the `padres` node of `s7_an[0]`, behind IHP's 587 Ω secondary
protection). Note: the wrapper exposes only `s7_an_0_esd`, while `gen_padframe.tcl` also labels
`s7_an_1_esd` — the inconsistency found in the 2026-09-04 pin-mapping session is still there.

## Two routes for the pad macros (decision 2026-10-20: custom padframe cells first)

### Priority: custom padframe cells (needs changes in the harness fork)

`sg13cmos5l_IOPadSingle2Diff` replaces the IOPadAnalog cell of `s7_an[0]`, and
`sg13cmos5l_IOPadDiff2Single` replaces the one of `s7_an[1]`. OP / ON of the driver are the pad's ESD
clamp frames on iovdd / iovss; front end and bias tap the ring rails iovdd / iovss; the level
shifters' input inverters use the 1.2 V core ring vdd / vss.

What has to change in `sg13cmos5l_ocd_chipalooza` (not done; Christoph's fork, in coordination with
the harness owner, as `config.txt` item 5 requires):

1. `config.txt`: `s7_an[0]: sg13cmos5l_IOPadSingle2Diff`, `s7_an[1]: sg13cmos5l_IOPadDiff2Single`.
   `scripts/parse_config.py` accepts only the 11 IHP pad types and derives the core signals per type;
   it needs a branch for the two cells and their core-side pin lists below.
2. Padframe: the two cells must abut the IHP IO cells exactly (cell height, ring metal positions of
   iovdd / iovss / vdd / vss, 80 µm pitch or a multiple), with GDS, LEF and a CDL/SPICE view where
   `gen_padframe.tcl`, `run_gen_padframe.sh` and the padframe LVS (`validate/run_lvs_padframe.sh`)
   pick up the IHP cells.
3. Core-side pins to route from each pad cell to the slot-7 wrapper edge (new wrapper ports):

   | cell | core-side pins |
   |---|---|
   | `sg13cmos5l_IOPadDiff2Single` | vinp vinn vref ibias en_1v2 sel0_1v2 sel1_1v2 vdd1v2_sense vdd3v3_sense |
   | `sg13cmos5l_IOPadSingle2Diff` | outp outn vcm vref ibias en_1v2 sel0_1v2 sel1_1v2 vdd1v2_sense vdd3v3_sense |

   19 wires in all; en_1v2 and the two sense lines could be shared by both cells (16). Bias crosses
   into the pad cells only as the harness current `ibias`, never as gate voltages (bias.md, "Rail
   referencing").
4. `slot7_wrapper` (`verilog/rtl/slot7_wrapper.v`, `xschem/slot7_wrapper.sym`, the wrapper GDS/MAG):
   the new ports; then `make gds-slots` and the chip-level rebuild described in the harness README (7).
5. The harness LVS treats IO cells as black boxes; the custom cells need the same treatment or a
   netlist that its LVS can compare.

### Fallback (this macro, now): both pad macros inside the slot

`schematic/xschem/slot.sch` (2026-10-20): Christoph's pin sheet plus two instances.

| | `xs2d` (IOPadSingle2Diff) | `xd2s` (IOPadDiff2Single) |
|---|---|---|
| iovdd / iovss | vdd_3v3 / vss_3v3 | vdd_3v3 / vss_3v3 |
| vdd / vss (core ring) | vdd_1v2 / vss_1v2 | vdd_1v2 / vss_1v2 |
| pad | s7_an_0_esd (behind the harness secondary protection) | s7_an[1] (bare pad node) |
| signal | outp / outn → vdiffp / vdiffn | vinp / vinn ← vdiffp / vdiffn |
| vref, vcm | vbias (harness voltage bias) | vref = vbias |
| ibias | ibias1 | ibias0 |
| en_1v2 | enable | enable |
| sel | dig_in[3:2] | dig_in[1:0] |
| sense | vdd_1v2, vdd_3v3 | vdd_1v2, vdd_3v3 |

The chain is the "filter off" configuration of the test plan (input buffer straight into the output
buffer). Unused: clk, reset, dig_out[11:0], analog_bus[3:0], dig_in[23:4]. The gmC stage, the V_CM
reference and the analog-bus taps of vdiffp / vdiffn are not designed yet.

In the fallback, the harness IOPadAnalog pads keep their own clamps, and the driver's OP / ON are
ordinary devices in the slot area (they can still be drawn with the clamp PCells of `scripts/pcells`).
The S2D cell's own input protection is then redundant behind the harness pad; dropping it in the
fallback is an open item.

## Verified

- `slot.sch` netlists with xschem 3.4.8RC to the two instances above, with no missing symbol
  (`xschemrc` now BOM-free and with the pad macros on the library path).
- Not done: layout of the two instances, slot-level DRC / LVS against `reference/slot7_wrapper.gds`,
  any slot-level simulation.
