<!--
SPDX-FileCopyrightText: 2026 Christoph Maier
SPDX-License-Identifier: Apache-2.0
-->
# slot.sch redrawn (Claude, 2026-11-07)

## What changed (drawing only)
- Two groups, each a dashed layer-10 box with a magenta title: "[S2D] single-to-differential pad xs2d with its own
  enable control xs2d_c and bias generator xs2d_g", and the same for [D2S]. Each row runs left to right:
  en_ctrl_3v3 -> bias_gen_pd -> pad macro.
- Real wires: enable (port, then a trunk to both en_ctrl_3v3), ibias1 -> xs2d_g and ibias0 -> xd2s_g (straight from
  the ports), en_3v3 / sel0 / sel1 from the control into the generator (risers), en_3v3 / en_3v3_b from the control
  under the generator to the pad, generator iref -> pad iref, vdiffp / vdiffn from S2D outp / outn through a channel
  between the groups into D2S vinp / vinn (nested, no crossing), s7_an_0_esd from the right-edge port over the top
  to the S2D pad input.
- Labels are kept for supplies, vbias (3 pins), the dig_in bits (taps of the dig_in[23:0] bus) and s7_an[1] (a bit of
  the s7_an[0:1] bus). Every internal net keeps its name through a lab_wire (s2d_/d2s_ en_3v3, en_3v3_b, sel0_3v3,
  sel1_3v3, iref, plus vdiffp, vdiffn). Labels: 61 lab_pin before, 30 lab_pin + 12 lab_wire + 81 wires now.
- Ports: harness pins in the left column (supplies at top/bottom, ibias at their wire height), pad pins s7_an_0_esd and
  s7_an[0:1] at the right edge; unused clk, reset, analog_bus[3:0] (left) and dig_out (right) at the bottom, captioned
  "not connected here". Port instance order is unchanged.
- Texts: all original texts kept unchanged; the header moved above the groups and each "outside the pad cell" note into
  its group. Added a two-line note "One generator per pad: ..." under the header.

## Checks
- Netlist (xschem -q -x -n -s, macro xschemrc): the slot subckt body is textually identical to the original
  (6 instances, same nets and net names; 0 "IS MISSING").
- sheet_equiv.py (original at HEAD in a scratch root vs the working tree): equivalent, 549 flattened devices,
  0 of 1 sheets differ, same ports. Negative control (one pad vss label changed to vss_3v3): DIFFERENT, as expected.
- Instance/port lines: same 24 symbols with identical properties (names, no other parameters).
- sch_lint.py with --lib for sg13cmos5l_IOPadSingle2Diff, sg13cmos5l_IOPadDiff2Single, en_ctrl_3v3, bias_gen_pd and
  xschem's devices/ (ipin/opin/iopin are referenced without the devices/ prefix): no group carries two names,
  0 missing symbols, 9 deliberate crossings without a junction (sel risers over en/en_b, ibias0 over the enable trunk).
- --log: 12 "Error:" lines, all "undriven node: dig_out[0..11]", identical to the original sheet's log. They come
  from the unused output port dig_out[11:0] and cannot go away without changing connectivity.
- Render: macros/slot/schematic/slot.png (3000 px) and slot.svg; checked at 7000 px for overlaps.

## Not kept / not fixable here
- The original sheet has no title.sym; the title text block is kept, no title.sym was added.
- Supply stubs still cross symbol-owned texts (en_ctrl_3v3 @name, bias_gen_pd @symname, pad @symname), because those
  texts sit over the pins in the .sym files; fixing that needs symbol edits (not touched).
- No simulations/ directory was created; the existing gitignored macros/slot/testbenches/xschem/simulations is untouched.
