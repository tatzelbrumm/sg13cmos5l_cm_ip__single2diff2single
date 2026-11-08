<!--
SPDX-FileCopyrightText: 2026 Christoph Maier
SPDX-License-Identifier: Apache-2.0
-->
# slot_7: slot 7 with the custom pads (tier 1, 2026-11-08, in progress)

The slot-7 circuit for the hand-over: harness enable and dig_in0..5 -> `s7_ctrl` (master enable, mode decode, switch
matrix) -> bandgap core -> `bias_dist_pd` -> `pad_ref_rb` and both custom pads; S2D -> D2S loop direct or swapped, the
S2D outputs on analog_bus0/1 or the D2S fed from them, vcm / vref on analog_bus2/3 (monitored, or fed with pad_ref_rb
disconnected). Concept and simulation: `docs/slot7_hookup/` (CONCEPT.md, tier1/).

| dig_in | function (only with the key dig_in3 = 1, dig_in4 = 0; otherwise the default) |
|---|---|
| 0 swap | loop S2D -> D2S crossed (polarity flip) |
| 1 mon | S2D outp / outn -> analog_bus0 / 1 (loop stays on) |
| 2 feed | analog_bus0 / 1 -> D2S vinp / vinn, loop off (wins over swap and mon) |
| 5 ext | pad_ref_rb disconnected; the pads take vcm / vref from analog_bus2 / 3 |

Default (enable = 1, any dig_in without the key): bandgap reference, replica bias on, loop direct, analog_bus0/1
disconnected, vcm / vref on analog_bus2 / 3 (close the harness's bus switches, reg 0x51 bits 6 / 7, to read them).

Files: `netlist/source/slot_7.spice` (s7_ctrl, slot_7; source of truth), sheets and layout to follow.
