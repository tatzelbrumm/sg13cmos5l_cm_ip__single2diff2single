<!--
SPDX-FileCopyrightText: 2026 Christoph Maier
SPDX-License-Identifier: Apache-2.0
-->
# F2 stage B: the routed pad candidate (C2, 2026-11-03)

Saved by the lead from F2's stage-B reply (the harness refused to let the agent write `out/report.md`); F2's text,
unchanged except for this header. Stage B2 (15:57) afterwards renamed the block's `vdd` / `vss` / `vddo` / `vsso` texts to
`iovdd` / `iovss` (dropped `vsso`); `pad_candidate.gds` 8946d2a0c95e, `.cdl` b06a4f5ba6de. The lead's checks:
`design_considerations/pad_buffer_layout/pad_cell_2026-10-31/lead_checks/F2_stageB*/`.

**Summary**
1. `pad_candidate.gds` (top `sg13cmos5l_IOPadDiff2Single`) with the routed `d2s_block` at (0, 84). DRC (incl. latch-up and
   antenna) is clean, and LVS against `pad_candidate.cdl` matches.
2. CMA / CMB use the v8 polarity (`XCMA pa a pa pa`, `XCMB b pb b b`), each behind its own 2 kOhm stage (rppd 1/7.435 +
   dantenna + dpantenna).
3. The review is applied. The switches moved: TGP/TGN/TDN sit beside bias_tree_n's NI, SA/SABP inside ab_p, SB/SABN inside
   ab_n. That removes the NWell notch and both extra taps. Two of the stage cell's three rings are merged into one, and its
   iovss path is 1.0 um wide. The sinks have no center contacts.
4. row_check: 0 layers or bands fail. path_widths: every pad path is at least as wide as in phase 1. Router metal over
   gates: 0 um2. PEX: 21 capacitor-only nodes, all explained (F: 19).
5. Still open: CMA and CMB share one ring leg; the inherited rules at their limit were not re-audited; the
   stage-to-capacitor lines are about 55 um long (the P frame between them sets this, see 1.).

Facts marked (measured) come from the logs in out/logs; everything else is reasoning. Full rebuild:
`sh src/run_all_B.sh <dir>`, 24 s, byte-identical (measured, 15:26 CET). Checks: `sh src/run_checks_B.sh <dir> <logdir>`.

## 1. CMA / CMB, v8 polarity, 2 kOhm stages
- Netlist: netlist_changes.md item 1. The stage cell d2s_sp2k_f2 is placed twice: at (2.50, 88.60) R0 for CMA and at
  (69.99, 88.60) M90 for CMB. They are mirror images.
- CMA: in d2s_cma, removed the 88 Via1 and the left Metal2 tab; new tab with 2 x 19 Via1 on the left column; a Metal1 strap
  at y 45.0–45.6 joins the right column; a Metal2 line runs up the left edge channel (x 2.55–2.85), then Metal1 under the
  joins, into the stage's core node; CMA's own guard ring (F's cm_rings) stays on pa's well.
- CMB: in m2_comb_p, removed the gate's two Via1 to the pad; new route from the gate head: Via1 at (73.25, 50.64), Metal2
  east to x 78.3, up the right edge channel, then Metal1 under the joins, into the stage.
- Line length: pa 54.6 um, pb 54.9 um (from the drawn coordinates). Why not shorter: the P frame fills x 4–76 between the
  capacitors (y ≤ 51) and the joins (y 86.4–88.0); only the 2.5 um edge channels are free, and they already carry vfb and
  the pa/pb lines. The stages are the lowest block cells, directly above the joins at the channel ends, and each feed is
  one straight Metal2 line. Shorter lines need room inside the P frame; that is Christoph's call.
- Stage pad pins: they go down to the P frame's 0.61 um pad lines (x 8.74–9.35 and 72.16–72.77). For the left one one of
  nw_isolator's 19 taps (at x 9.045) is removed.
- The "turned" variant is dropped.

## 2. Switches
- TGP/TGN/TDN: new cell d2s_tgsw_f2 at (53.90, 166.55), directly under bias_tree_n, whose NI they switch. ni: a 1 um Metal2
  stub to NI's drain. iref and en_3v3/en_3v3_b: from the top ports at x 43.6–45.8, about 10 um away. TGP's well joins
  bias_tree_p's through a tongue at y 168.4–169.9.
- SA/SABP: inside d2s_ab_p_f2, above the U tap, in the same NWell rectangle. No notch, no tap of their own. Mirror images,
  gates joined by a poly bridge. d2s_pd_p is gone.
- SB/SABN: inside d2s_ab_n_f2, above its tie, which they share. Gates joined in poly; no separate substrate tap. d2s_pd_n is
  gone.
- d2s_sp2k_f2: rppd w 1 / l 7.435 (1991.6 Ohm), pad end at the bottom, core end at the top; dantenna 0.64 x 3.1 (n+ in the
  substrate, core to iovss); dpantenna 0.64 x 4.98 (p+ in an NWell, core to iovdd).
- Rings: IHP draws three (a p+ ring around the resistor, a p+ ring around dantenna joined by a narrow Metal2 strap, an n+
  ring around dpantenna). Merged here: one p+ ring (iovss) around the resistor and dantenna — the resistor's guard,
  dantenna's anode contact and the cell's iovss pin. Kept: the n+ ring — dpantenna's cathode and the NWell tie (LU.a /
  LU.b), a different net and implant, so it cannot be merged (reasoning). iovss path: Metal1 bridge 1.0 um wide from the
  ring to the edge stub's p+ (x 0.60–3.40 and 76.95–79.40, y 95.5–96.5). iovdd: Via1 + Via2 from the n+ ring to the Metal3
  rail.

## 3. Sinks
- The center gate-contact columns are removed; the gaps beside BN and T close from 0.85 to 0.25 um.
- BN's drain is tabbed onto vbn. T (D = S = G = vbn) is tied by a Metal1 strap across its own dummy channel.
- Gate contacts only at the row ends; ring legs have contacts only between the strips.
- sym_check (measured): 0.0768 um2 and 0 narrow-poly hits (PCell residue, as N2).

## 4. Floorplan, bottom-up
- Rows: bottom CMA stage, loads, ab_p, ab_n, CMB stage; middle casc_p, casc_n and sinks (both R90); upper middle inputs,
  rhigh; top tails and bias_tree_p, bias_tree_n and tgsw.
- Connections: a/b/dabp/dabn go straight down to the joins, and the bias nets climb one column each.
- Router (generator.py, unchanged; measured): Metal1 692 um, Metal2 1040 um, 146 vias. Every gate is a keep-out for all
  nets. One Metal3 tap per supply group; vsso has its own path to the P frame's p+ ring.
- Cell area: about 4929 um2 (PMOS 2760, NMOS/R 1938, stages 231).

## 5. Checks (measured)

| check | result | log |
|---|---|---|
| pad DRC (main + maximal + antenna) | Check Passed, 0 exceptions | pad_drc.log |
| pad LVS | match | pad_lvs.log |
| block LVS | match | block_lvs.log |
| row_check | 0 DIFFERENT, 0 FAIL | row_check/ |
| path_widths | pad M2 13.72 / 13.11 um at y 52.2 / 64.5 (phase 1: 13.42 / 12.81); nothing narrower | path_widths_pad_candidate.md |
| router metal over gates | 0 um2 | router_metal_over_gates.txt |
| PEX | 21 capacitor-only nodes | pex_capacitor_only_nodes.txt |

- The Via1 that left the 38.5–52.2 band were the CMA/CMB feeds, now moved to pa/pb (intended).
- Changed cells, all DRC and LVS clean: ab_n, ab_p, sinks, both bias trees, sp2k. sym_check: ab_n 0, ab_p 0, bias_tree_n
  0.0384, bias_tree_p 0, sinks 0.0768 um2. tgsw standalone shows only LU and an LVS fail (no ties of its own); in context it
  is clean. rhigh and casc_n: XOR 0 against stage A.

## 6. Changes to the primitives
- sinks: as in section 3.
- ab_n: SABN/SB folded in; dummies tied to vss (N2 tied them to vabn); one TGO rectangle; SB's b goes by Metal2 to ABN's b pin.
- ab_p: SA/SABP folded in; a symmetric NWell rectangle; Via1 added on the vabp bar.
- bias trees: the row only. d2s_tgsw_f2: new. sp2k: one p+ ring.
- P2's cells: unchanged (the router reads a copy with the tub_p20x1_c2 labels stripped, labels only). rhigh, casc_n: unchanged.

## 7. Changes to the static pad cells
- Top cell: 63/0 box deleted.
- d2s_cma: all Via1, the left Metal2 tab and the "pad" label removed. d2s_cmb: "pad" label removed.
- m2_comb_p: 2 Via1 at (72.2–72.8, 50.6) removed. nw_isolator: the tap at x 9.045 removed.
- New pad_wiring_f2: the vfb Kelvin line (F's, unchanged), the pa/pb lines, the stage pad feeds, the iovss bridges, and vsso
  to the P frame ring (Via1 at 64.10, 84.10).
- New in the block: pwr_f2 (taps and NWell bridges); padtop_ctx_f2 (routing context only, deleted in the pad).

## 8. Open points of 2026-10-28

| point | status | note |
|---|---|---|
| a/b joins | closed | |
| guard tie to iovdd | closed | |
| CMA ring | partly open | its middle leg is shared with CMB (accepted by Christoph 2026-11-03) |
| rules at the limit | open | inherited, not re-audited; DRC is clean |
| 63/0 box | closed | deleted |

## 9. Open decisions for Christoph (answered 2026-11-03, see decisions.md)
1. The dummy convention. 2. Where the stages go. 3. The shared ring leg. 4. The port changes to the symbol.
