<!--
SPDX-FileCopyrightText: 2026 Christoph Maier
SPDX-License-Identifier: Apache-2.0
-->
# Roadmap for the next IHP sg13cmos5l Chipalooza run (written 2026-11-08, after the slot 7 hand-over)

What this run delivered, what it left open, and what the more ambitious ideas would take. Effort estimates are for
cloud sessions with agents, as worked this time; they are estimates, not measurements.

## Delivered in this run (slot 7, `macros/slot_7`, hand-over repo `sg13cmos5l_cm_slot7`)

- Custom pads S2D / D2S (earlier sessions), replica bias `pad_ref_rb` (vcm, S2D vref, bypass capacitors), bias
  distribution `bias_dist_pd`, bandgap core, fail-safe enable `en_ctrl_3v3` v2 / `ls_up_fs` (nA, no 1.2 V supply),
  switch matrix `s7_ctrl` (loop direct / swapped, S2D → bus0/1, bus0/1 → D2S, external vcm / vref on bus2/3, 2-bit key
  so that a harness reset gives the default mode).
- Checks: DRC (incl. maximal deck with latch-up rules), LVS (KLayout deep; magic + netgen in the harness flow),
  default mode at all corners, all modes at tt / ff, pad starvation (leakage only with the slot off), S2D enable kick,
  harness flow in Christoph's fork (netcheck 13 / 13, antenna 0, pad-frame LVS) with four harness-side patches.

## Open from this run (do first next time, or as an update if Tim accepts one)

1. Extraction (PEX) of the whole slot and the key modes again with parasitics (loop, swap, enable kick).
2. Tim's full chip flow: top-level LVS (`lvs-top`; the harness xschem sheets still have the old slot-7 pins),
   density with fill, and upstream support for custom pads in `parse_config.py` (C6's patches 0001-0004 on fork
   branch `claude/slot7-v2-harness-test`, `docs/slot7_v2_test/patches/`).
3. Power-up of the whole slot as the harness sequences it (supplies, enable, vdd_1v2 off / floating) with the
   bandgap's start-up; swap / mon at ss −40 °C (solver-limited in DC; a long transient).
4. Mismatch Monte Carlo of the shifter thresholds and of the loop offset (on the schematic: mismatch MC is vacuous on
   extracted netlists, docs/traps.md).
5. Clean-ups: v1 traces of en_ctrl_3v3 (the note in `ocd_pad_support.sch`, the D2S `tb_en_ctrl` deck, the unused
   sense pins in the `bias_sel_pd` sheets); symbols still off the 20 grid (bdp_slice, tg_hv, nand2_hv, nor2_hv,
   pad_ref_rb, bias_tree_rb, bypass_rb, vref_s2d_rb).

## The more ambitious ideas

| idea | what it requires | effort |
|---|---|---|
| Monitor internal bias voltages and currents on the analog buses (the fallback session's idea) | an analog mux onto a bus: tree voltages of pad_ref_rb / bias_dist_pd, bias_dist_pd's spare 5 µA output (iout3) into a bus held at a fixed voltage by an SMU; the fallback's stage B has a tree-voltage mux to reuse; the pads' own internal bias nodes need new pad pins (next pad revision); care with loading (bus capacitance, leakage into µA nodes) | ~1 day design + layout, plus dig_in bits in the decode |
| hv standard-cell set | first evaluate `sg13cmos5l_stdcell_hv` (IHP-Open-PDK, dev branch; agent R's survey on the notes branch); otherwise grow agent D's row: fixed row height and site grid, symbols on the 20 grid with off-center supplies, decap cells from the fillers, tap / endcap cells to close the guards, ls_up_fs as a cell, LEF / Liberty characterization if a digital flow is to place them | days to weeks; reused in every later slot |
| S2D outputs that can drive a bus | a stronger output stage or a buffer in the next pad revision, so monitoring on bus0/1 no longer slows the loop 10-30× | pad redesign: sheets, layout, characterization |
| Use the differential core signals for something other than each other | a project definition first (ADC, comparator, filter, differential amplifier between the pads); the s7_ctrl matrix already routes bus0/1 to the D2S, a new block attaches there | depends on the block |
| Oguey–Aebischer core as a selectable second reference | omitted from slot 7 tier 1 by Claude under time pressure (only the bandgap feeds bias_dist_pd; its inputs 1-3 are tied off). Christoph would have kept it, had he had the time to review the decision. Needs: oa_core_pd placed (layout exists, DRC / LVS clean) into bias_dist_pd input 1, the harness ibias0 / ibias1 on inputs 2 / 3, and dig_in bits for en_in1..3 in the s7_ctrl decode (the default stays the bandgap) | small: placement, routing, decode bits, LVS; the cell and the distribution exist |
| One reference / replica chain per pad | duplicate pad_ref_rb and the bias chain, a few decode bits | small, mostly layout |
| Lower start-up current of the reference cores | longer start-up pull-up chains in oa_core_pd / bg_core_pd (0.43-0.67 µA → about half) | small layout change in both cores |
| External vcm / vref without series switches | pad_ref_rb's pull-down (SPD) on its own control, so its outputs can be tri-stated instead of switched | small change in pad_ref_rb (netlist, layout) |

## How to work next time (lessons from this run)

- Decide the slot-level interface table (dig_in bits, bus use, default mode) and its owner before the blocks are laid
  out; most late changes this run came from it.
- Run the harness flow early with a stand-in slot (C6 did; it caught the missing custom-pad support in the harness).
- Parallel agents (sheets, a block layout, slot assembly) with a lead that releases each result as it lands worked
  well; give every agent a timebox, a workspace, cell-name prefixes, and the exact check commands.
- Keep the records as this run did: RUNLOG with commit times, chat log from the transcript, the skill updated from
  Christoph's hand edits.
