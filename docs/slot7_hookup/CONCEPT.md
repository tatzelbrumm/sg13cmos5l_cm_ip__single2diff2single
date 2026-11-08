<!--
SPDX-FileCopyrightText: 2026 Christoph Maier
SPDX-License-Identifier: Apache-2.0
-->
# Slot 7 hookup: pads, references, replica bias, bias distribution, harness buses (concept, 2026-11-08)

Concept only: nothing in layout, schematics or tests is changed by it. Written by cloud session C4 from its own
blocks and a read-only survey of the harness and the other slot-7 sessions (survey with every source: notes branch
`claude/c4-replica-bias-sudel`, `sudelbuecher/design_considerations/replica_bias/integration/research.md`).
**F** = fact with source in the survey, **P** = proposal, **O** = open.

## Decisions needed

1. **One owner of the slot-7 interface table** (slot pins, `dig_in` bit map, bus use per mode, default mode). P: the
   fallback session, which already allocated `dig_in[0..12]` and all four buses; this session supplies the pad side.
2. **Default by key** (below): all-equal `dig_in`, the harness's reset state, gives the default mode. OK?
3. **pad_ref_rb on the ring supply** (iovdd / iovss, as the pads) or on the slot's gated vdd_3v3? P: ring.
4. **S2D outputs on the buses in the default loop:** they then drive a shared chip pad. Accept after a load check, or
   monitor only vcm / vref by default?
5. **External vcm / vref** needs one change in pad_ref_rb (below). Later is fine.

## What the harness gives slot 7 (F)

| resource | behaviour |
|---|---|
| `vdd_3v3`, `vdd_1v2` | switched on the high side by the harness; **floating** when off (the fallback measured 0.5 … 0.67 V) |
| `vss_3v3`, `vss_1v2`, pad ring, core ring | never switched |
| `analog_bus0..3` | four chip pads shared by all 18 slots, one hv switch per slot (reg 0x51 bits 4..7), open by default |
| `ibias0/1`, `vbias` | iDAC currents / tapped voltage through per-slot switches on always-on supplies (can back-feed an off slot) |
| `dig_in[23:0]` | latched; 0 while slot 7 is not selected; **route registers reset to pad io[0]: all 24 bits follow one pad until written** |
| `enable` | valid 1.2 V level even when the slot's vdd_1v2 is off |
| custom pads | 13 core-side nets replace `s7_an*`: S2D `vref outp outn vcm en_3v3 en_3v3_b iref`, D2S `vinp vinn vref iref en_3v3 en_3v3_b` |

If the harness's SPI fails, the slot stays unpowered (0x51 = 0) and no slot design helps. "Digital control
malfunctions" below therefore means: supplies, `enable` and the bus switches are set, `dig_in` is not (or wrongly).

## Signal plan (P)

```
 iovdd ring ...............................................................................
  S2D pad --outp/outn--+--[Tsb0/1]---------------------------- analog_bus0 / bus1
                       +--[Tld0/1 direct]--+
                       +--[Tlx0/1 crossed]-+--> vinp/vinn -- D2S pad
          analog_bus0/1 --[Tbd0/1]---------+
  pad_ref_rb --vcm--+-- S2D vcm, D2S vref  --[Tvcm]------------ analog_bus2
             --vref-+-- S2D vref           --[Tvref]----------- analog_bus3
 ........................................................................................
 slot vdd_3v3 (gated):  BG core, OA core, ibias0, ibias1 --> bias_dist_pd --> iout0 pad_ref_rb
                                                                           --> iout1 S2D, iout2 D2S
                                                                           --> iout3 spare (monitor, mode B)
```

Ten hv transmission gates (`tg_hv` size or larger), all signals at or near vcm. Monitoring through a TG (on-resistance
some kΩ, an estimate, not simulated) into the bus and the meter is a DC / slow measurement (kΩ × tens of pF).

| mode | S2D | D2S | loop | bus0 / bus1 | bus2 | bus3 |
|---|---|---|---|---|---|---|
| **D: default** | on | on | direct | outp / outn (monitor) | vcm (monitor) | vref (monitor) |
| L-x: loop crossed | on | on | crossed (polarity flip) | outp / outn | vcm | vref |
| I: in | on | off | open | outp / outn | vcm | vref |
| O: out | off | on | open | drive vinp / vinn (around vcm) | vcm | free |
| E: external refs | as D, I or O | | | as that mode | **drive** vcm | **drive** vref |
| B: bias monitor | off | off | open | fallback diagnostics (core currents) | tree voltage mux | iout3 (5 µA copy of the pad reference) |

Reference into bias_dist_pd: BG core (default), OA core, ibias0, ibias1 (`en_in0..3`); outputs as assigned
(iout0 pad_ref_rb, iout1 S2D, iout2 D2S, iout3 spare). The default runs BG core → pad_ref_rb and both pads, as asked:
on-slot reference, on-slot replica bias monitored on the buses, single → diff → single looped and monitored.

## Default and the dig_in map (P, for the table owner)

- **Key:** manual modes only when `dig_in[23] = 1` and `dig_in[22] = 0`. Any all-equal `dig_in` (reset route: all
  bits follow pad io[0], or forced 0x0D) cannot match, so it gives mode D whatever io[0] does. The key must be written
  on purpose.
- Pad side in the free bits `dig_in[13..23]`: key 2, mode 3, reference select 2, bus taps 4 (disconnect a tap to
  measure unloaded) = 11 bits. The fallback's `dig_in[0..12]` stay as its diagnostics, valid only under the key
  (mode B); in mode D the BG core is on whatever `dig_in[1]` says.
- Decode in one place; each block gets one enable (pads, pad_ref_rb, cores, bias_dist_pd inputs / outputs, ten TGs).
  O: decode in the 1.2 V domain and shift only the decoded enables, or shift 11 bits and decode in hv_logic.

## Supplies and fail-safe (F, then P)

- What exists: `en_ctrl_3v3` (this repo, earlier session; schematic + CACE, no layout): en = en_1v2 AND vdd_1v2
  present AND vdd_3v3 present. Disabled: pA. **Enabled: ≈ 2 µA from vddh plus 1.4 / 1.7 µA into the two sense
  inputs** (ratioed pg_det). The fallback's `tp_en_ctrl*`: 1.2 … 1.75 µA per enabled channel. Neither draws current when
  off; both do when on.
- P, **fail-safe by starvation, no detector:** everything on the ring (both pads, pad_ref_rb) takes its bias only from
  `iref` (inferred from the port lists: iref is their only bias input; the testbench below checks it), which bias_dist_pd sources from the slot's gated vdd_3v3. Slot off → iref = 0 → no ring current, whatever
  the enable lines float to. Then the enables crossing from slot to ring carry state, not safety, and no quiescent
  detector is needed. To verify (later, one testbench): ring current with iref = 0, en_3v3 / en_3v3_b swept
  0 … 3.3 V independently, vcm / vref / vinp / vinn floating, slot vdd_3v3 at 0 V and floating 0.6 V, all corners;
  target ≤ 10 nA.
- Only if that fails somewhere: a static CMOS gate in the ring domain per pad (input: the slot's vdd_3v3 itself),
  long channels for the floating 0.5 … 0.67 V level; no ratioed pull-up, so no current when on.
- pad_ref_rb on the ring keeps the replica referenced to the pads' own iovdd (its vcm tracks the pads' top edge);
  on the slot's vdd_3v3 it would track a different rail. bias_dist_pd and the cores stay on the gated slot supply.
- Harness side (F, fallback PLAN): open the bus / ibias / vbias switches and set the SMUs to 0 V before gating the
  slot off (back-feed ≤ 87 nA otherwise).

## Changes this implies (later, none done)

1. **pad_ref_rb:** its disable pulls vcm and vref to vss (`SPD`, gate `en_3v3_b`, F). Mode E needs that pull-down on its
   own control (e.g. `pd_b = en_3v3_b AND NOT ext`), not a series switch in the reference path.
2. **S2D output load:** outp / outn were designed for the D2S gates plus the built-in 12 × 12 µm load capacitors;
   a monitored bus adds a shared chip pad. Check settling and stability with the bus load, or keep the taps open in D.
3. **Ten TGs and the decode** at slot level; `ocd_analog_switches` copies are not DRC / LVS checked here (F).
4. **Stale docs:** `macros/slot/README.md` lists 19 pad wires (en_1v2, sel, sense, ibias); the delivered pads have 13.
   `TOP_LEVEL_MODULE.md` still names `analog_pin[2:0]` and `select & clk`.

## Path to the hand-over

Fixed table → slot-level schematic (pads as black boxes, the blocks above, TGs, decode) → testbenches for modes D,
L-x, E and the starvation check → layout in slot 7 next to the pad stubs → `sg13cmos5l_cm_slot7` (session for the
hand-over repo) → smoke test with the harness fork (C6 flow: 13 pins OK in its dry run; upstream also has its own
`setup_custom.sh`, O which one Tim uses).
