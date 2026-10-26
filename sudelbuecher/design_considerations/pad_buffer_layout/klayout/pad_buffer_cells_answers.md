<!--
SPDX-FileCopyrightText: 2026 Christoph Maier
SPDX-License-Identifier: Apache-2.0
-->
# Answers to `pad_buffer_cells_questions.txt`  
  
## Superseded by [pad_buffer_cells_qa.md](./pad_buffer_cells_qa.md)  

2026-10-26, Claude (Opus 5.5). Short answers; the root causes come first, because most questions trace
back to them.

## Six shortcuts in the generator, behind most of the questions

| | what `pad_buffer_cells.py` does now | better |
|---|---|---|
| A | every finger is its own PCell and its own Activ, side by side along L, so the gates are parallel and nothing shares diffusion | common-gate groups stacked along W with collinear gates (one poly line through all fingers); neighbours on a shared node abut (shared S/D) |
| B | gates reach a poly bar above the row through stubs `min(L, 0.5 µm)` wide; the bar sits 0.42 µm up to avoid notches. That is where the "narrow poly connections" and "chokepoints" come from | with A no bar is needed; otherwise full-gate-width straps with several contacts |
| C | one tie strip per row (shared between mirrored rows); no rings | a well or substrate ring around every matched array, at the same distance from every device |
| D | dummies are members of the centroid map (pairs), so they end up on one side, in the middle, or single | dummies are edge treatment: one at each end of every row / column, outside the map. For odd counts, pick grid dimensions with a true centre cell |
| E | an M2 trunk spans only from its first to its last via | every trunk spans the whole array, dummies included (same metal over every device) |
| F | `block()` handles two rows, so a four-row array is split into two cells, and each row is its own cell (`_r1`, `_r2`) | one cell per array; row cells only where a row is repeated identically |

## Per question

- **bg_pcas, bg_pmir: dummies on one side only.** D: the dummy pair was point-reflected like a device pair,
  so it landed in opposite corners. One dummy at each end of both rows is the fix.
- **Separate `_r1` / `_r2`.** F: a construction artefact (each row built as a cell, the second placed
  mirrored). Not needed.
- **pnpMPA: 9 instances or an array? Abut the rings?** Nine separate instances of the same PCell variant;
  one 3 × 3 array instance would do. Each device has three rings in Activ / M1: emitter, base (n+ in its
  NWell), collector (p+ outside). All collectors are on vss, so neighbouring collector rings can be shared
  (overlapped) instead of standing 1.0 µm apart. Keep the NWells (bases) separate. Whether IHP's pnpMPA
  extraction accepts shared rings needs one LVS run.
- **bg_res: abut the resistors?** Yes, in principle: merge pSD / nSD / SalBlock / EXTBlock and keep PolyRes
  per resistor. The pitch then follows the poly-resistor spacing rules (Rhi / Sal in the rule table) instead
  of the PCell's 0.9 µm outline plus 0.5 µm. Not yet DRC-checked; the 1.4 µm pitch was a safe first guess.
  The same goes for d2s_rhigh / s2d_rhigh.
- **Cascodes (casc_n / casc_p): in the array or separate?** They need no matching, but in line with
  their device (same column) the x / y nodes get shorter and smaller. Shared diffusion with the sink
  needs equal finger widths: the cascode is 15 µm wide and the sink finger 6 µm, so cascodes of 12 or
  18 µm (2 or 3 fingers of 6/3) would be a schematic change.
- **Cascodes: rotate to abut gates?** Yes (A): all four share vbnc (or vbpc), one poly line.
- **Cascodes: M2 over the whole array?** Yes (E).
- **Cascodes: taps as a guard ring?** Yes (C).
- **bias_tree_sw: TDN by abutment?** Yes: TGN (iref → ni) and TDN (ni → vss) share ni, so make one Activ
  with ni in the middle and two gates.
- **pd blocks: flip to share a contact?** Yes, every pair has a common node: SB / SABN vss, SA / SABP vdd,
  TPN / TNN and TPP / TNP vcm.
- **pd blocks: identical?** Not now. `d2s_pd_n` and `s2d_pd_n` (and `_p`) are the same two devices,
  1/0.45 with one gate net, but wired differently: vss drops to the tie, vcm runs on an M2 trunk. An XOR
  of the cells shows different M1 / Via1 / M2. With the common node in the middle (A) they become one
  cell, "two switches, one gate, shared middle node", if the parent connects the middle node to the
  tie where needed. `bias_tree_sw` is the same pair with two gates (en_3v3 / en_3v3_b).
- **ab blocks: flip to share sources?** Partly. RP1, RP1 and RP2 fit one Activ: n1 | vdd | n1 | vabp
  (the RP1 pair shares vdd, RP1 and RP2 share n1). FPL and ABP share no node with these or with each
  other. The same for RN1, RN1, RN2 in `d2s_ab_n`.
- **d2s_cma / d2s_cmb as a PCell?** Yes, a good first PCell to write yourself. Parameters: area and aspect
  ratio, or C at a stated bias. C is bias dependent (0.32 … 0.87 pF for 14 × 14 µm from V_GW = −0.5 to
  +2 V, `results_improvements.txt`), so C can only be a target at a given V_GW.
- **Inputs: narrow poly connections.** B.
- **Inputs: rotate?** Possible; the one well per device stays.
- **Inputs: common-centroid the individual transistors?** Each device could be split into two
  single-finger halves in two wells on the same net, at point-reflected positions. That costs about 50 %
  more area (wells). The 2 × 4 map already centres every unit's pair; what remains is the gradient across
  a device's two adjacent fingers. Probably not worth it.
- **Loads.** B, A (all fingers share l2 / vcmfb) and E. Yes to all three.
- **rhigh: abut implants?** See bg_res.
- **rhigh: M2 above the poly resistors?** Metal over a poly resistor shifts it a little (stress, hydrogen
  passivation, capacitance). That matters for matching when the coverage differs between resistors.
  In these blocks no metal crosses a resistor body: the jumpers run above the top heads and below the
  bottom heads. Rule: no metal over bodies, or the same over every segment, dummies included.
- **rhigh: substrate ring around the array?** Yes (C); now it is a strip below.
- **tails, sinks: why only 3 dummies?** BP / BN take the fourth row end. That puts the bias diode at an
  edge, which shifts every tail (sink) current together: gain-neutral, but it scales the bias. Better:
  4 end dummies and BP / BN inside.
- **tails, sinks: rotate to abut poly? Well tap as a ring?** Yes (A); yes (C).
- **fit_* cells.** A fit check only. The primitive sets are shelf-packed into an 80 µm wide strip to see
  whether they fit the 94 µm above the clamp frames (d2s front end 94.2 µm, s2d 136.5 µm). They are not a
  floorplan and add no geometry.
- **oa_mcs: rotate?** Yes: two 3.4/30 devices side by side are 62.5 × 6 µm now, about 9 × 31 µm when
  turned.
- **oa_mcs: narrow contacts, guard ring.** B; C.
- **oa_misc_n.** Side by side only because of the row builder (A). Uncritical devices can be packed
  freely: stack MS3 and SKS, share vss. MS2 and SKS are in parallel (vss → ks); MC10 and MS2 share
  the gate vbr.
- **oa_misc_p: rotate?** Yes. Better still, make the MS1 chain one Activ with 8 gates in series and
  uncontacted diffusion between them, folded into two columns.
- **oa_nmir: dummy in the middle.** D: M11 has 9 fingers; the odd one was paired with a dummy at its
  reflection, which is the centre. A 3 × 9 grid has a real centre cell for the odd M11 and needs no inner
  dummy.
- **oa_nmir: taps outside, poly inside.** Yes: for a common-gate array the rows should face each other
  across a shared gate in the middle, with ties as a ring outside. `block()` does the opposite (shared
  tie in the middle, gate bars outside), because it saves one tie.
- **oa_pcas: rotate?** Yes (A).
- **oa_pmir_a / oa_pmir_b: rotate, ring, poly inside?** Yes (A, C, as oa_nmir).
- **oa_pmir_b: why one dummy? Difference from oa_pmir_a?** F and D: they are rows 1–2 and 3–4 of one
  4 × 8 point-symmetric array of 32 positions. The centre pair straddles the two cells: P0 sits in a, its
  reflection (a dummy) in b. There are no end dummies at all.
- **s2d_cload: chokepoint contacts.** B: a 0.5 µm stub on a 12 µm gate.
- **s2d_cload: abut sources?** Yes: S = D = B = vss on both capacitors, so one Activ with two gates
  (voutp, voutn).
- **s2d_cload: taps left and right?** Yes.
- **zone_80x94: where in the IHP pad?** In the 80 × 180 µm pad-cell frame (y = 0 at the pad side) it is
  x = 0 … 80, y = 84 … 178: from the top of the Clamp_P frame (84.4) to the top of the M3 / M4 rails
  (178). IHP's IOPadAnalog has its p+ substrate tap band there (84 … 140, under iovdd / iovss), and above
  it the band under the 1.2 V vdd / vss rails (140 … 178). In the GDS it is only an outline next to the
  fit cells, not placed in a pad.

## Patterns these add up to (candidates for a layout-pattern skill)

1. **Common-gate group.** Fingers stacked along W, gates collinear on one poly line, contacts at the line
   ends; no bars, no stubs.
2. **Shared diffusion.** Neighbours on a common node abut (mirror: S D S D …); series devices get uncontacted
   internal diffusion.
3. **Dummies are edge treatment.** One at each end of every row / column, same geometry, outside the
   centroid map. Odd counts: grid dimensions with a true centre cell.
4. **Rings.** A well ring (PMOS) or substrate ring (NMOS, resistors, PNPs) around every matched array, at
   the same distance from every device.
5. **Symmetric metal.** Trunks over the whole array, dummies included; no metal over resistor bodies.
6. **In-line cascodes.** The cascode in its device's column; equal finger W where diffusion is to be shared.
7. **Rows face their shared gate.** Two-row common-gate arrays: gate in the middle, ties outside.
8. **Uncritical devices** (switches, start-up, logic): pack freely, share diffusion, rotate.
9. **Same geometry, one cell.** Connections that differ go to the parent.
10. **Resistor arrays.** Merged SalBlock / EXTBlock / implants, PolyRes per resistor, pitch at the rule
    minimum, end dummies, ring.
11. **PNP arrays.** One array instance, shared collector rings, separate base wells.
