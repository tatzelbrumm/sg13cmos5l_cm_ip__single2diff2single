<!--
SPDX-FileCopyrightText: 2026 Christoph Maier
SPDX-License-Identifier: Apache-2.0
-->
# Questions and answers on `pad_buffer_cells.gds`

2026-10-26.
- **Questions:** Christoph, verbatim from `pad_buffer_cells_questions.txt`. They are grouped by topic, so a line with
  several questions appears under more than one heading; `…` marks a cut.
- **Answers:** Claude (Opus 5.5), checked against `pad_buffer_cells.gds` and `pad_buffer_cells.py`.
- **GDS** names the cells of `pad_buffer_cells.gds` each answer is about: the cell, its subcells (`→`),
  and its devices and size as in `cell_tree.md`.
- This file replaces `pad_buffer_cells_answers.md`.

## 0. Six generator shortcuts behind most answers

| | what `pad_buffer_cells.py` does now | better |
|---|---|---|
| A | every finger is its own PCell and its own Activ, side by side along L: gates parallel, no shared diffusion | devices on one gate net side by side along W ("rotated"), gates on one continuous poly line; neighbours on a common node share the diffusion |
| B | each gate reaches a poly bar above the row through a stub `min(L, 0.5 µm)` wide; the bar sits 0.42 µm up, because a narrower stub left poly notches (Gat.b) | with A no bar is needed; otherwise full-width poly with several contacts |
| C | one tie strip under each row, shared by two mirrored rows | a well or substrate ring around every matched array |
| D | dummies are members of the centroid map (pairs), so they land on one side, in the middle, or alone | dummies at both ends of every row and column, outside the map; odd counts get a grid with a true centre cell |
| E | an M2 trunk runs from its first to its last via | every trunk over the whole array, dummies included |
| F | `block()` builds two rows as two cells (`_r1`, `_r2`); a four-row array becomes two blocks | one cell per array |

## 1. Cell structure: rows, halves, identical cells

**Q:** "Why separate bg_pcas_r1 _r2 and bg_pmir_r1 _r2?"

GDS: `bg_pmir` → `bg_pmir_r1`, `bg_pmir_r2`; `bg_pcas` → `bg_pcas_r1`, `bg_pcas_r2` (each row 21.2 × 13.0 µm,
9 × pmosHV 10/1, ntap1).

**A:** (F) `block()` builds each row as a cell and places the second one mirrored about the shared tie. The row
cells serve no other purpose; one cell per array is enough.

**Q:** "oa_pmir_b : … what's the difference between oa_pmir_a and oa_pmir_b, anyhow?"

GDS: `oa_pmir_a` → `oa_pmir_a_r1`, `oa_pmir_a_r2`; `oa_pmir_b` → `oa_pmir_b_r1`, `oa_pmir_b_r2` (each 76.8 × 8.0 µm;
rows 74.9 × 5.0 µm, 8 × pmosHV 2/8, ntap1).

**A:** (F) They are rows 1–2 and 3–4 of one 4 × 8 point-symmetric map of the OA-core PMOS mirror (P0, P2, P8, PO:
31 fingers and 1 dummy). Same outline and devices, different wiring: their XOR differs only in M1, Via1 and M2.
Stacked, a over b, they make the array.

**Q:** "d2s_ab_n , d2s_ab_p ; ds_pd_n , ds_pd_p, s2d_pd_n, s2d_pd_p : … are some of these layout blocks identical?"

GDS: `d2s_pd_n`, `s2d_pd_n`, `bias_tree_sw` (3.4 × 3.6 µm, 2 × nmosHV 1/0.45, ptap1); `d2s_pd_p`, `s2d_pd_p`
(4.1 × 4.0 µm, 2 × pmosHV 1/0.45, ntap1); `d2s_ab_p` (5 × pmosHV 6.66/0.6), `d2s_ab_n` (5 × nmosHV 4.4/1).
"ds_pd" is `d2s_pd`.

**A:** Not yet.
- `d2s_pd_n` and `s2d_pd_n` use the same two PCell instances, but their metal differs: vss drops to the tie, vcm
  runs on an M2 trunk. `bias_tree_sw` has two gate nets (en_3v3, en_3v3_b), so its poly differs as well. The same
  holds for the `_p` cells.
- With the common node between the two devices (section 4), `d2s_pd_n` and `s2d_pd_n` become one cell, if the
  parent connects that node to the tie where needed.
- The `ab` cells are different devices.
- Identical already, apart from labels: `d2s_cma` = `d2s_cmb`, and `oa_misc_p` = `bg_misc_p`.

## 2. Dummies

**Q:** "why do bg_pcas, bg_pmir in pad_buffer_cells have dummies only on one side each of the transistor arrays?"

GDS: `bg_pmir`, `bg_pcas` (rows `_r1`, `_r2`, 9 × pmosHV 10/1 each).

**A:** (D) `mirror_map()` placed the two dummies like a matched pair, at point-reflected positions. As the outermost
pair they landed in opposite corners: left end of one row, right end of the other. Fix: one dummy at each end of
both rows, outside the centroid map.

**Q:** "d2s_tails , s2d_tails , sinks_6x6 : why only 3 dummies?"

GDS: `d2s_tails` → `d2s_tails_r1`, `d2s_tails_r2` (6 × pmosHV 5/6 each); `s2d_tails` → `_r1`, `_r2` (8 each);
`sinks_6x6` → `sinks_6x6_r1`, `sinks_6x6_r2` (8 × nmosHV 6/6 each).

**A:** The bias diode (BP in the tails, BN in the sinks) takes the fourth row end. That does not touch the matching
between the units' tails or sinks. But at the edge the diode matches them worse, which scales all their currents
together: a bias error, nearly gain-neutral because rhigh sets the gain. Better: four end dummies, and the diode
inside, near the centre.

**Q:** "oa_nmir : why the dummy in the middle?"

GDS: `oa_nmir` → `oa_nmir_r1`, `oa_nmir_r2` (14 × nmosHV 10/1 each, 34.1 × 24.4 µm).

**A:** (D) M10 has 18 fingers and M11 9, 27 in 28 positions (2 × 14). M11's odd finger needed a partner at its
reflection, and the first pair placed is the one nearest the centre, so the dummy is there. A 3 × 9 grid has a true
centre cell for M11's odd finger and needs no inner dummy; end dummies go outside.

**Q:** "oa_pmir_b : … why one dummy?"

GDS: `oa_pmir_a`, `oa_pmir_b` (rows as in section 1).

**A:** Same cause: 31 fingers in 4 × 8 positions, and P0 (one finger) is paired with the dummy at the centre. The
centre lies between rows 2 and 3, i.e. between the two cells: P0 is in `oa_pmir_a`, the dummy in `oa_pmir_b`. The
array has no end dummies at all.

## 3. Gate orientation and poly connections

**Q** (each with its GDS cells):
- "d2s_inputs , s2d_inputs : why the narrow poly connections? could the transistors be rotated? …"
  `d2s_inputs` (8 × `tub_p20x1` + 4 × `tub_p20x1_dummy`), `s2d_inputs` (12 + 4); `tub_p20x1`: pmosHV 20/1 ng=2 and
  ntap1 in its own well, 4.3 × 13.0 µm.
- "d2s_loads , s2d_loads : why the narrow poly connections? should the transistors be rotated to abut gates? …"
  `d2s_loads` (10 × pmosHV 6/4), `s2d_loads` (14 ×).
- "s2d_sinks_cmfb : why the narrow poly connections? should the transistors be rotated to abut gates? …"
  `s2d_sinks_cmfb` → `_r1`, `_r2` (6 × nmosHV 6/6 each).
- "bias_tree_n, bias_tree_p ; d2s_casc_n, d2s_casc_p, s2d_casc_n, s2d_casc_p : … should the transistors be rotated
  by 90 deg to abut gates? …" `bias_tree_n`, `bias_tree_p`, `d2s_casc_n`, `d2s_casc_p`, `s2d_casc_n`, `s2d_casc_p`
  (devices in section 7).
- "d2s_tails , s2d_tails , sinks_6x6 : … can the transistors be rotated 90 deg to abut poly? …"
  `d2s_tails`, `s2d_tails`, `sinks_6x6` (section 2).
- "oa_pcas : can the transistors be rotated 90 deg to allow poly abutment?"
  `oa_pcas` (7 × pmosHV 2/2, 0.5/2, 1/2, ntap1).
- "oa_pmir_a : can the transistors be rotated 90 deg to allow poly abutment? … why not poly connections on the
  inside, by abutment?" (the same for oa_pmir_b) `oa_pmir_a`, `oa_pmir_b` (section 1).
- "oa_nmir : … why not poly connections on the inside, by abutment?" `oa_nmir` (section 2).
- "oa_mcs : why not rotate by 90 deg? why narrow poly contacts? …" `oa_mcs` (2 × nmosHV 3.4/30, ptap1,
  62.5 × 6.0 µm).
- "oa_misc_n : why narrow poly contacts? …" `oa_misc_n` (section 4).
- "oa_misc_p : can the transistors be rotated 90 deg?" `oa_misc_p` → `_r1`, `_r2` (8 × pmosHV 0.5/12.5 and
  1/0.45), identical to `bg_misc_p`.
- "s2d_cload: why the poly chokepoint contacts? …" `s2d_cload` (2 × nmosHV 12/12, ptap1).

**A:** The narrow connections are shortcut B, and rotating (A) removes their cause. So yes, rotate every matched
array: loads, tails, sinks, `s2d_sinks_cmfb`, cascodes, `bias_tree_n/p`, `oa_pmir`, `oa_nmir`, `oa_pcas`,
`bg_pmir`, `bg_pcas`. Devices on one gate net then share a continuous poly line, contacted at the ends with
full-width poly.

Poly connections inside, for two-row arrays (`oa_nmir`, `oa_pmir`, `bg_pmir`, …): the rows face each other across
their gates, or share their source diffusion (vdd or vss for every mirror device). The ties move outside and
become the ring. `block()` does the reverse, because a shared tie saves one tie.

Cell by cell:
- **Inputs:** each tub is one device (two 10/1 fingers sharing the drain) in its own well. Neighbouring tubs have
  different gates and wells, so nothing between them can abut. Rotated, a tub takes 14.8 µm of row pitch instead
  of 6.1 µm, so a d2s row of 6 tubs would be 87 µm wide, more than the 80 µm cell. Keep the orientation, and widen
  only the gate connection (B).
- **`oa_mcs`:** turned or stacked along W, the two gates become one poly rectangle 30 µm long. The block is then
  about 31 × 10 µm instead of 62.5 × 6 µm; both shapes fit, and the gain is the shared gate.
- **`oa_misc_p`:** yes. Better still, make the MS1 chain one Activ with 8 gates in series, with uncontacted
  diffusion between them (ms1 … ms7 have no other connection), folded into two columns.
- **`s2d_cload`:** a 0.5 µm stub feeds a 12 µm gate. Use full-width poly with several contacts.

## 4. Shared diffusion and stacking

**Q:** "bias_tree_sw : can TDN be connected by abutment, by abutting the drains? (orientation of digital or switch
transistors is uncritical)"

GDS: `bias_tree_sw` (TGN, TDN: 2 × nmosHV 1/0.45, ptap1).

**A:** Yes. TGN (iref → ni, gate en_3v3) and TDN (vss → ni, gate en_3v3_b) share ni: one Activ, iref | ni | vss,
two gates.

**Q:** "d2s_ab_n , d2s_ab_p ; ds_pd_n , ds_pd_p, s2d_pd_n, s2d_pd_p : can the transistors be flipped to abut source
contacts? …"

GDS: `d2s_ab_p` (RP1, RP1, RP2, FPL, ABP), `d2s_ab_n` (RN1, RN1, RN2, FNL, ABN), `d2s_pd_p`, `d2s_pd_n`,
`s2d_pd_p`, `s2d_pd_n`.

**A:**
- pd cells: yes. Each pair has a common node: SB / SABN on vss, SA / SABP on vdd, TPN / TNN and TPP / TNP on vcm.
- ab cells: partly. RP1, RP1 and RP2 fit one Activ, n1 | vdd | n1 | vabp: the two RP1 share vdd, and RP1 and RP2
  share n1. FPL and ABP share no node with them or with each other. The same holds for RN1, RN1, RN2.

**Q:** "s2d_cload: … can the source contacts be abutted? …"

GDS: `s2d_cload`.

**A:** Yes. S = D = B = vss on both capacitors, so one Activ: vss | CLP | vss | CLN | vss.

**Q:** "oa_misc_n : … why are the transistors side by side? MS3 and SKS could at least be stacked vertically."

GDS: `oa_misc_n` (MC10, MS2: nmosHV 10/1; MS3 0.5/2; SKS 1/0.45; ptap1; 9.5 × 12.6 µm); `bg_misc_n` is the same
without MC10.

**A:** (A) Only because the row builder puts everything in one row. These devices need no matching, so they can be
packed freely:
- stack MS3 and SKS, sharing vss;
- MS2 and SKS are in parallel (vss → ks) and can share vss;
- MC10 and MS2 share the gate vbr and can share one poly line.

## 5. Taps and guard rings

**Q** (each with its GDS cells):
- "bias_tree_n, bias_tree_p ; d2s_casc_n, … : … should the bulk taps be laid out as guard ring structure?"
  `bias_tree_n`, `bias_tree_p`, `d2s_casc_n`, `d2s_casc_p`, `s2d_casc_n`, `s2d_casc_p`.
- "d2s_rhigh , s2d_rhigh : … Substrate tap as guard ring around the resistor array?" `d2s_rhigh`, `s2d_rhigh`.
- "d2s_tails , s2d_tails , sinks_6x6 : … well tap as guard ring?" `d2s_tails`, `s2d_tails`, `sinks_6x6`.
- "oa_mcs : … why not substrate contact as guard ring?" `oa_mcs`.
- "oa_nmir : … why not substrate tap(s) on the outside as guard ring?" `oa_nmir`.
- "oa_pmir_a : … why not well tap(s) on the outside as guard ring?" (the same for oa_pmir_b) `oa_pmir_a`,
  `oa_pmir_b`.
- "s2d_cload: … can the substrate tap be left and right instead of at the bottom?" `s2d_cload`.

**A:** (C) Yes to all.
- A ring at the same distance from every device gives each one the same well or substrate potential and the same
  edge, and it helps against latch-up in the pad.
- The cost is a 0.78 µm tie plus spacing on every side. The d2s front end already needs 94.2 of the 94 µm, so the
  rings have to be paid for by rotation and shared diffusion.
- `s2d_cload`: left and right, or a ring, is fine; a MOS capacitor is uncritical.

## 6. Metal over the arrays

**Q:** "bias_tree_n, bias_tree_p ; d2s_casc_n, … : … should metal2 wires go over the entire transistor array, for
symmetry?", the same question for "d2s_loads , s2d_loads" and for "s2d_sinks_cmfb".

GDS: `bias_tree_n`, `bias_tree_p`, the four `*_casc_*`, `d2s_loads`, `s2d_loads`, `s2d_sinks_cmfb`.

**A:** (E) Yes. Every trunk should run over the whole array, dummies included, so that every finger sees the same
metal above it. Now each trunk ends at its last via.

**Q:** "d2s_rhigh , s2d_rhigh : … Does it hurt accuracy if the metal2 connections are above the poly resistors? …"

GDS: `d2s_rhigh` (18 × rhigh 0.5 × 12.65 µm, ptap1), `s2d_rhigh` (26 ×), `bg_res` (41 × rhigh 0.5 × 9.94 µm).

**A:** Metal over a poly resistor shifts its value a little (stress, hydrogen passivation, capacitance). For
matching, what counts is equal coverage on every segment. In these three cells no M1 or M2 crosses a resistor body
(checked: zero overlap with PolyRes). The jumpers run above the top heads and below the bottom heads. Keep it that
way, or cover every segment equally, dummies included.

## 7. Where the special devices go

**Q:** "bias_tree_n, bias_tree_p ; d2s_casc_n, d2s_casc_p, s2d_casc_n, s2d_casc_p : should the cascode transistors be
part of the array or be placed separately? …"

GDS:
- `bias_tree_n`: NBP, NI, NABP and 2 dummies (nmosHV 6/6), plus NBPC 2.4/6 beyond the right dummy.
- `bias_tree_p`: PBN, PABN and 2 dummies (pmosHV 5/6), plus PBNC 2/6.
- `d2s_casc_n` / `s2d_casc_n`: 4 / 8 × nmosHV 15/3, plus BNC 1/8.
- `d2s_casc_p` / `s2d_casc_p`: 4 / 6 × pmosHV 15/3, plus BPC 1/4.

**A:** I read this two ways.
- **The cascode bias devices** (NBPC and PBNC in the bias tree, BNC and BPC in the cascode rows): they share the
  row's gate line, so keeping them in the row saves wiring. Their matching is not critical: a few % of current
  error moves vbnc / vbpc by a few mV, which the cascode headroom absorbs. At the row end, as now, is fine.
- **The 15/3 cascodes themselves:** they could go next to the device they cascode (sinks, loads), in its column.
  The x / y nodes then get shorter and carry less capacitance. Sharing diffusion with the sink would need equal
  finger widths (15 µm against 6 µm), which is a schematic change.

**Q:** "d2s_inputs , s2d_inputs : … could the individual transistors be common centroided?"

GDS: `d2s_inputs`, `s2d_inputs`, `tub_p20x1`, `tub_p20x1_dummy`.

**A:** Possible, but not worth it. Each device could become two single-finger tubs at point-reflected positions,
which puts every device's centroid at the array centre. But a unit's offset depends on the difference between its a
and b halves, and that pair is already point-reflected; the gain is set by rhigh. Splitting would make the array
about 1.5× wider, because each finger then needs its own well and the 1.8 µm well spacing.

## 8. Poly resistors

**Q:** "bg_res : Can the resistors be abutted?" and "d2s_rhigh , s2d_rhigh : can the nSD, pSD, SalBlock, EXTBlock of
the resistors get abutted? (keep PolyRes separated) …"

GDS: `bg_res` (41 × rhigh 0.5 × 9.94 µm, 56.9 × 11.2 µm, placed only), `d2s_rhigh` (27.7 × 20.0 µm), `s2d_rhigh`
(38.9 × 22.4 µm).

**A:** Yes.
- Now: each rhigh PCell brings its own nSD / pSD (0.86 µm wide), SalBlock and EXTBlock (0.9 µm) around a 0.5 µm
  body and 0.5 µm heads. The 1.4 µm pitch leaves 0.5 µm between SalBlocks (Sal.b 0.42).
- Merged: with these layers merged and PolyRes kept per segment, the pitch is limited by the head contacts (M1 pads
  0.46 µm) and any rhigh-specific spacing rule, which I have not checked yet. That gives roughly 0.7 µm, about half
  the array width.
- Still to verify: DRC, and LVS (the extraction must still see separate resistors).

## 9. PNP array

**Q:** "pad_buffer_cells.gds : 9 instances or array instance of pnpMPA? could the guard ring TIEs be abutted?"

GDS: `bg_pnp` (25.7 × 21.6 µm, placed only) → 9 × `pnpMPA` (one PCell variant, 7.9 × 6.4 µm).

**A:**
- **Now:** nine single instances of the same variant, at a pitch of 8.9 × 7.42 µm. One 3 × 3 array instance would
  be the same geometry in one record.
- **Device:** a pnpMPA is a 2 × 2 µm emitter, a base n+ ring in its own NWell, and a collector p+ ring outside
  (substrate). The collector rings (Activ) are now 1.4 µm apart.
- **Abutting:** with the collector rings touching, `bg_pnp` shrinks to about 22.9 × 18.5 µm. Overlapping them
  (shared ring) saves more. But neighbouring NWells are then only 2.1 µm apart minus the overlap, so the NWell space
  rule (NW.b1, 1.8 µm, as for the input tubs) sets the limit.
- **Open:** whether IHP's LVS still extracts nine pnpMPA from shared rings needs one LVS run.

## 10. MOS capacitors

**Q:** "d2s_cma , d2s_cmb : make pcell with area and aspect ratio as parameters, maybe even with capacitance as
parameter?"

GDS: `d2s_cma`, `d2s_cmb` (17.9 × 19.0 µm each, pmosHV 16/16 and ntap1, identical geometry); related: `s2d_cload`
(2 × nmosHV 12/12).

**A:** Yes, a good first PCell to write yourself.
- **Parameters:** area and aspect ratio, which give W, L and the number of gate fingers; tap ring yes or no; gate
  contacts on one or both sides.
- **Capacitance:** only at a stated bias. The 14 × 14 µm hv PMOS gives 0.32 pF at V_GW = −0.5 V and 0.87 pF at
  +2 V (`../../class_ab_pad_driver/improvements/sim/results_improvements.txt`). So the PCell would carry a C(V_GW)
  table and solve for W·L.
- `s2d_cload` would be the NMOS variant of the same PCell.

## 11. Fit checks and the 80 × 94 µm zone

**Q:** "fit_bias_tree_oa_bg , fit_d2s_front , fit_d2s_front_caps, fit_s2d_front , fit_sd2_front_caps : what are these
fits for?"

GDS: `fit_d2s_front`, `fit_d2s_front_caps`, `fit_s2d_front`, `fit_s2d_front_caps` ("fit_sd2_front_caps"),
`fit_bias_tree_oa_bg`: instances of the cells above, nothing else.

**A:** An area check, not a floorplan. Each one packs a set of primitives into an 80 µm wide strip (first-fit shelf
packing, 2 µm apart) to see whether it fits the 94 µm above the clamp frames:

| set | packed height |
|---|---:|
| d2s front end | 94.2 µm |
| d2s front end with CMA / CMB | 98.8 µm |
| s2d front end | 136.5 µm |
| bias tree, OA core and bandgap core | 131.1 µm |

There is no new geometry, and the interconnect is not included.

**Q:** "zone_80x94 : where exactly in the IHP IO pad is this placed?"

GDS: `zone_80x94` (an outline only, no instances).

**A:** In the 80 × 180 µm IO cell (y = 0 at the pad side) it is x = 0 … 80 µm, y = 84 … 178 µm. That runs from the
top of the Clamp_P frame (84.4) to the top of the M3 / M4 vdd / vss rails (178). IHP's IOPadAnalog has its p+
substrate-tap band at 84 … 140 µm, under the iovdd / iovss rails, and the vdd / vss rails at 140 … 178 µm. In the GDS
the zone sits next to the fit cells, not in a pad.

## Patterns these add up to (seed for a layout-pattern skill)

1. **Common-gate group:** devices on one gate net side by side along W, one continuous poly line, contacts at the
   ends; no bars, no stubs.
2. **Shared diffusion:** neighbours on a common node abut. Series devices get uncontacted internal diffusion.
3. **Dummies are edge treatment:** one at each end of every row and column, outside the centroid map. Odd counts
   get a grid with a true centre cell.
4. **Rings:** a well ring (PMOS) or substrate ring (NMOS, resistors, PNPs) around every matched array.
5. **Symmetric metal:** trunks over the whole array, dummies included; no metal over resistor bodies.
6. **Rows face their shared gate (or source):** the ties go outside, as the ring.
7. **In-line cascodes:** the cascode in its device's column; equal finger W wherever diffusion is shared.
8. **Uncritical devices** (switches, start-up, logic): pack freely, share diffusion, rotate.
9. **Same geometry, one cell:** connections that differ go to the parent.
10. **Resistor arrays:** merged SalBlock / EXTBlock / implants, PolyRes per segment, pitch at the rule minimum, end
    dummies, ring.
11. **PNP arrays:** one array instance, shared collector rings, separate base wells.
12. **Check the cell width before rotating:** rotation must not push an array past the 80 µm cell, as it would for
    the input tubs.
