# Metal2 rework (option B) of `sg13cmos5l_IOPadDiff2Single`, 2026-10-28

Background agent (Claude), cloud workspace only, 00:49–01:33 CET (`TZ=Europe/Berlin date`). No git, no writes to the user's computer, `inputs/` untouched. klayout.db 0.30.12 (Python), matplotlib.

| file | sha256 |
|---|---|
| start `inputs/pad_pcells_2026-10-28.klay.gds` | `8520e3150b14688c…` |
| **candidate `out/sg13cmos5l_IOPadDiff2Single.klay.gds`** | **`e270a2192a51860d47ebf3281bb5d44ec8bd6da286f77a36da54afd745f540ca`** |
| `out/build_m2.py` (start → candidate, rerunnable) | `7310f311…` |
| `out/check_m2.py` (all checks; log `out/check_m2.log`) | `93f54791…` |

Run with `python3 build_m2.py <start> <out>` and `python3 check_m2.py <start> <candidate> <outdir>`. The builder saves with `write_context_info = True`, keeps the top cell name, and writes no GDS timestamps, so a rerun gives the same sha256. Coordinates are absolute µm from the lower left of the 80 × 180 cell. "Measured" means read from the layout; reasoning is marked as such.

## 1. What was built

The new static cells are each placed once at (0, 0) in the top cell. The PCell instances, the PCell code and the rail cells are untouched.

| cell | contents | Via1 / Via2 |
|---|---|---|
| `m2_comb_n` | 17 pad lines, 0.61 wide, on the N drains x = 8.485 + 3.82k, from y 2.8 up into the junction (39.5). At x 39.045 only a stub from y 2.8 to 13.205 onto the lower frame's ON drain. 18 iovss straps, 0.2 wide, on the N sources x = 6.575 + 3.82k, y 6.2–39.0. DCNDiode side plates (iovss): x 3.45–6.675 (merged with the strap at 6.575) and x 74.0–76.55, both y 26.95–37.55 | Via1: 974 on the pad lines (N drains and DCNDiode cathode stripes); 630 on the straps (inner rings, N sources, DCNDiode anode bars); 195 on the plates. Via2 into the iovss rail: 900 on the straps, 60 on the plates |
| `m2_comb_p` | 22 pad lines, 0.61 wide, on the P drains x = 9.045 + 3.02k, from y 41.1 (inside the junction) to 81.45. At x 39.245 (the RP1/dummy drain) only a stub up to 61.6 onto the DCPDiode anode stripes. 22 iovdd straps, 0.2 wide, on the P sources x = 7.535 + 3.02k, y 53.0–84.2. DCPDiode side plates (iovdd): x 4.35–7.635, y 52.95–63.45 (merged with the strap at 7.535), and x 73.05–75.65, y 52.95–68.0 (reaches up into the iovdd rail) | Via1: 1546 on the pad lines (P drains, DCPDiode anode stripes, 22 onto CMB's gate head); 902 on the straps (DCPDiode cathode bars, inner ring, P sources); 210 on the plates. Via2 into the iovdd rail, only at y ≥ 66.05: 264 on the straps, 12 on the right plate |
| `m2_junction` | Pad junction at y 39.3–41.3, in two parts: x 3.0–37.88 and x 38.72–74.0 (a 0.84 µm cut for dabn). 22 iovss stubs on the DCPDiode guard ring: Metal2 at x_s ± 0.6 (x_s = the P source columns), y 51.2–52.2; the stub at k = 10 is x 37.135–37.88 | 332 Via1 from the junction onto CMA's S/D frame. Stubs: 65 Via1 on the guard ring (y 51.495) and 65 Via2 into the iovss rail (y 51.9) |
| `replica_lines` | dabn: Metal2 x 38.15–39.35, y 18.255–22.765 on the RN1 drain, then a line at x 38.15–38.45 up to y 86.0. dabp: a 0.61 line at x 38.94–39.55, y 67.805–86.0 on the RP1 drain. Pins (10/2) and labels (10/25) at y 85.0–86.0 | 22 + 60 Via1, same pattern as the clamp drains |
| `gate_feeds` | Every bus segment gets a Metal1 extension to a 0.8 × 0.8 landing beyond the array, with 2 × 2 Via1. Landings: N frames x 3.5–4.3 and 75.7–76.5; P frame x 5.0–5.8 and 74.2–75.0. **b:** Metal2 down the cell edges at x 0.5–1.0 and 79.0–79.5 from y 12.73, joined at y 87.4–88.0. **a:** x 3.2–3.7 from CMA's gate (y 50.49) and x 77.0–77.5 from y 81.09, joined at y 86.4–87.0. Pins for a (x 35.5–37.5) and b (x 40.5–42.5) on the joins. CMB: Metal2 x 73.61–74.50, y 42.2–49.8 on its right S/D + ntap column, with a tab at y 45.57–46.34 out to b | 58 Via1: 24 at the landings, 2 at CMA's gate, 32 at CMB |
| `cap_cma`, `cap_cmb` | the Miller capacitors (section 3) | – |

The band narrowing is done on the top cell and in the `contacts` cell (section 4).

How the scheme works:
- **Via2 only into the strap's own rail.** No pad or iovdd Metal2 has Via2 under the iovss rail. Measured Via2 by (Metal2 net, Metal3 net): pad/pad 858, iovss/iovss 1025, iovdd/iovdd 276.
- **iovss crosses the junction in the uncut Metal3 rail** (y 34.5–60). The N straps carry Via2 below the junction (up to y 38.95), the guard-ring stubs above it (y 51.9).
- **Wide Metal2 over the diode side bars** where the comb does not reach, with Via1 on every bar of the plate's net underneath.
  - On the left side, each plate merges with the outermost strap.
  - On the right side a pad line separates plate and straps. So the DCNDiode plate has its own Via2 into the iovss rail. The DCPDiode plate instead reaches up into the iovdd rail (Via2 at y 66.05–67.95, Via1 on the P frame's inner ring).

Renders: `m2_full.png` (y 0–92) and `m2_gap.png` (y 36–55, with Via1 and Via2).

## 2. dabn, a, b: routing and why

**dabn** runs on the track x 38.15–38.45 (0.3 wide). A 1.2-wide tab sits on the RN1 drain with Via1 2 × 11, the same as the ON drains. From there it goes straight up to its pin at y 85–86.
- **N side:** it uses the drain column x 39.045 that RN1 frees; that column is pad only in the lower frame. It keeps 0.915 µm to the iovss strap at x 37.135. Over DCNDiode it costs the cathode feed at x 39.045 (12 of 216 cathode Via1 positions). The neighbouring feeds at x 35.225 and 42.865 remain.
- **Gap:** it passes the junction through the 0.84 µm cut (0.27 µm each side). Both junction halves stay on pad through the N comb and the pad bar. It runs over the 1.80 µm space between the CMA and CMB wells, not over a capacitor.
- **P side:** it fits between the iovdd strap at x 37.735 (0.315 µm away) and dabp on the RP1 drain (0.49 µm away). So no strap is given up, and the pad stub at x 39.245 still feeds the DCPDiode anode stripes. In the P frame it runs above the dummy's gate strip, which is on iovdd.
- **Why not the frame ends** (reasoning): getting from x 39.045 to the ends would cross every pad line and strap of the comb in Metal2.

**dabp** is a 0.61 line on the RP1 drain with the same Via1 as the OP drains (2 × 30), straight up to y 86.0.

**b:**
- The lower N bus is whole and is fed from both ends. The upper N bus halves (gates 0–15 and 18–34) are each fed from their own end.
- All feeds use Metal1 extensions running 0.22 µm above the end source or end drain to landings left and right of the array. From there Metal2 runs down the cell edges (x 0.5–1.0 and 79.0–79.5).
- This joins the two N frames' buses. CMB's S/D + well frame is tapped from the right edge line at y 46.

**a:** each P bus half (gates 0–19 and 22–42) is fed from its own end, through landings at x 5.0–5.8 and 74.2–75.0, y 81.09–81.89. The left line also runs down to CMA's gate head, which is extended to x 3.0–4.34 and has 2 Via1 at y 50.545.

**Joins:** outside the comb, above the P frame, in Metal2.
- a at y 86.4–87.0 (x 3.2–77.5); b at y 87.4–88.0 (x 0.5–79.5).
- b runs outside a, and both are above the dabp/dabn pins.
- Consequence (open point 3): Metal2 coming from above cannot reach dabp, dabn or pad without a Metal1 hop under the joins.

## 3. Miller capacitors CMA, CMB

Built like `d2s_cma` / `d2s_cmb` (hv PMOS in accumulation), with the gate along x and W along y:
- p+ S/D strips 0.34 µm wide, each with one contact column placed 0.07 from the Activ edge and 0.11 from the gate, as in the template.
- pSD extends 0.18 beyond the S/D and 0.40 beyond the gate.
- The gate poly has a contacted head 0.42–0.78 above the Activ, as in `d2s_cma`. HeatTrans covers the gate.
- ThickGateOx equals the NWell outline. 0.36 µm n+ ntaps sit at both x ends, 0.30 from the S/D.

| | CMA | CMB |
|---|---|---|
| NWell / TGO | x 2.57–37.97, y 41.46–50.66 | x 39.77–75.17, y 41.46–50.66 |
| gate (poly over Activ) | x 4.19–36.35, y 42.08–50.04 | x 41.39–73.55, y 42.08–50.04 |
| **drawn W / L** | **W 7.96 µm, L 32.16 µm** (255.99 µm²) | **W 7.96 µm, L 32.16 µm** (255.99 µm²) |
| gate net | a (head Metal1 y 50.46–50.82, 94 contacts) | pad (22 Via1 from P pad lines k = 11…21 onto the head) |
| S / D / well | pad: Metal1 U (both S/D + ntap columns, bottom strip y 39.3–41.85) under the junction, 332 Via1 | b: Metal1 U (bottom strip y 41.5–41.85), Metal2 + 32 Via1 on the right column |

**How much room there is (measured):**
- In y, NW.b1 (1.80 µm) applies on both sides: to the DCNDiode guard-ring NWell (top 39.66) and to DCPDiode's own NWell (bottom 52.46). That limits the wells to y 41.46–50.66, 9.20 µm.
- The 22:01 log estimate of 9.72 µm counted only NW.f (0.24 µm) to the guard ring at y 51.42.
- With NW.c1 (0.62 µm enclosure) on both sides, W = 7.96 µm.
- In x: 0.77 + 1.80 = 2.57 to the band's side NWell, and 1.80 between the two wells.
- Both capacitors still reach the schematic's 256 µm² (16 × 16), so the schematic should take `wc = 7.96u`, `lc = 32.16u`.

**Well spacings (measured):** NW.b1 is exactly 1.80 at six places (by design, for the area). NW.f is 0.76 to the DCPDiode guard ring (p+, outside TGO). TGO.b is 0.76 and 2.42. NW.d is 2.17 to the band's n+.

## 4. Band above DCNDiode

- **Clipped:** top-level Activ and Metal1 minus x 0.4–79.6 × y 39.04–42.56; NWell minus x 0.77–79.23 × y 39.66–43.18.
- **Ring still continuous (checked):** the 6–61 ring is one polygon in Activ, Metal1 and NWell from x 0 to x 80, through the side bars and DCNDiode's guard ring. Its top inside the cell is now y 39.04 (Activ, Metal1) and 39.66 (NWell).
- **`contacts` cell, 2468 → 406.** Removed:
  - 1989 that are now outside the narrowed band;
  - 1 exact duplicate at (1.645, 33.6);
  - 72 band contacts 0.185 µm from DCNDiode's guard-ring contacts, which caused a Cnt.b1 error (section 6).
- **Net:** the band and the DCNDiode guard ring stay the separate net `guard`, with no supply inside the cell, as today.

## 5. Checks (numbers; details in `check_m2.log`)

**Unchanged:**
- `Metal3ViasUp` and `TopLayersTo4`: every shape identical.
- Flat Metal3, Via3, Metal4, TopVia1 and TopMetal1 (and their pins): XOR between start and candidate is empty.
- The pad bar's Metal2 and its 858 Via2: identical.
- All 7 PCell variant cells: identical stored geometry.

**PCells live:** I reopened the candidate with `SG13_cm_clamps` registered, using `inputs/reopen.py` and the same logic in a subprocess of `check_m2.py`. All 8 PCell instances are live, with cell, placement and parameters identical to the start. The geometry the library regenerates equals the stored geometry on all layers.

**Flat extraction.** Layers: Activ, GatPoly, pSD, NWell (tied through n+ in NWell), Cont, Metal1, Via1, Metal2, Via2, Metal3, and labels on 8/25, 10/25, 30/25.

| device | L | G | S / D | W | |
|---|---|---|---|---|---|
| ON | 1.0 | b | iovss / pad | 299.20 | as start |
| RN1 | 1.0 | dabn | iovss / dabn | 8.80 | as start |
| OP | 0.6 | a | iovdd / pad | 546.12 | as start |
| RP1 | 0.6 | dabp | iovdd / dabp | 13.32 | as start |
| dummy | 0.6 | iovdd | iovdd / dabp | 13.32 | as start |
| CMA | 32.16 | a | pad / pad | 7.96 | new |
| CMB | 32.16 | pad | b / b | 7.96 | new |

- **Devices:** 7 of 7 expected, none extra.
- **Nets:** 12 nets in total.
  - pad, iovss, iovdd, guard, a, b, dabp and dabn: all labels of each on one net. No net carries two names, and there are 0 unlabelled nets with metal or NWell.
  - 56 of 56 probe points land on the expected net. The log lists them: every drain and source kind, diode stripes, bars, side bars, guard rings, clamp rings, bus segments, capacitor terminals and wells, pins, junction halves and rails.
- **Diode pin labels:** the PCells' cathode/anode/guard labels are mapped to their pad-level net, and the check confirms each lands there:
  - DCNDiode: cathode → pad, anode → iovss, guard → guard.
  - DCPDiode: anode → pad, cathode → iovdd, guard → iovss.
  - The known `guard,iovss` merge is the DCPDiode guard going to iovss, as intended.
- **Rails without devices** (iovdd 93.5–119, iovss 126–134, vss, vdd) are separate nets in a cell-level extraction; the pad ring joins them.
- **`inputs/verify.py`** shows the same devices and W, with two differences:
  - It has no Via2 or Metal3, so the DCPDiode guard ring and P outer ring (`guard,iovss`) appear separate from the N-side iovss; their only tie is through the Metal3 rail.
  - It joins the diode pin names into the net names (`anode,cathode,pad`, `anode,iovss`, `cathode,iovdd`).

**Rules.** I ran them flat over the whole cell, on both the start and the candidate. **Result: 102 rules; the candidate has 0 violations; the start had 68 (all Cnt.b1, now fixed); 0 new.**
- Values come from `sg13cmos5l_tech_default.json`.
- Rule names and implementations come from `beol/5_17_metaln.drc`, `beol/5_19_via1.drc`, `beol/5_20_vian.drc`, `beol/5_21_topvia1.drc`, `feol/5_1_nwell.drc`, `feol/5_14_cont.drc` and `sg13cmos5l_maximal.drc`.
- Rules run:
  - NWell: NW.a, b, b1 (by well net), c, c1, d, d1, e, e1, f, f1.
  - FEOL: Act.a–e; Gat.a, a4, b, b1, c, d, e, f; TGO.a–e; pSD.a, b, c, d, d1, i, i1, j, j1, k, l.
  - Cont: Cnt.a, b, b1, c, d, e, f, g, g1, g2, h, j.
  - Metal: M1.a, b, e, d, c1; M2, M3 and M4 .a, b, e, f, d, c, c1.
  - Vias: V1, V2 and V3 .a, b, b1, c, c1; TV1.a–d; TM1.a, b.
  - Latch-up: LU.a, d, d1, using the deck's `ext_enlarge_inside` stepping with simplified layer derivations (see the docstring).
- No nSD is drawn.

**Checker self-test:** I planted 8 faults on a copy, and all 8 were reported:
1. a Metal2 spacing error;
2. a Via2 in a rail gap;
3. a Via2 from a pad line into the iovss rail (reported as the merged label `iovss,pad`);
4. an NWell 0.33 µm from CMA's well;
5. a contact 0.05 µm from a gate;
6. an untied p+ well;
7. a Metal1 spacing error;
8. a 4 × 4 Via1 array.

**Gap in the deck's wide-metal rule (measured with klayout.db 0.30.12):** the form `met.sep(wide, …, projection_limits)` reports nothing when both lines are wide. `check_m2.py` adds `wide.space` with the same limits. I did not test whether the KLayout DRC engine behaves the same way.

## 6. Review of the hand wiring

**Fixed:**
- 72 band contacts at x 1.645 and 78.195 (y 25.7–38.8). They sat 0.185 µm from DCNDiode's guard-ring contacts, so the merged array had less than 0.20 µm spacing in both directions: 68 Cnt.b1 markers.
- One exact duplicate contact.

**Kept and listed:**

| item | measured | assessment |
|---|---|---|
| near-miss M1.e 0.230 (rule 0.22) | 5 places: bus plus my extensions against the inner ring's top side (N frames y 13.53 / 23.09, P frame y 81.89) | the PCell's own bus has the same 0.23 over its whole length; my extensions follow it |
| near-miss NW.b1 1.800 (rule 1.80) | 6 places: capacitor wells to the DCNDiode guard NWell, the DCPDiode NWell, the band side NWell, and to each other | by design (room for 256 µm²) |
| near-miss Cnt.f 0.110 (rule 0.11) | 92 capacitor S/D contacts | as in the template (IHP pmosHV) |
| all other near-misses (M1.b, M2.b, M2.e, M3.b, Act.b, Gat.b, pSD.b, NW.f, NW.d, Cnt.e, Gat.d, pSD.d1, TGO.b) | 0 | contact and via arrays at IHP's rule pitch (0.34 / 0.41) are not counted |
| NWell band beyond the cell boundary | x −0.62 and 80.62, y 14.94–61.62 | pre-existing; overlaps the neighbour's band on abutment |
| TEXT 63/0 box (36.355, 147.73; 45.815, 180.62) | the `sg13cmos5l_GateDecode` footprint (log 17:28) | stray marker, left as is (open question to Christoph) |
| labels | every 30/25, 50/25 and 126/25 label sits on a rail shape of its own name. Metal3 has vss / vdd at 140–158 / 160–178; Metal4 has vdd / vss interlocked in the opposite order. Via3 joins them only where the names match (rows at y 157.805 and 160.005, 92 each). The top-level `pad` label is on the pad net | consistent |
| via fields against the rails | Via2 2159 (858 pad, 798 + 227 iovss, 276 iovdd), Via3 2087, TopVia1 1783: each inside one rail band, covered on both metals; V*.c/c1, M*.c/c1 and TV1.a–d clean | consistent |

## 7. Design-note statements that disagree with the delivered layout

`inputs/layout_primitives.md`:

| statement | corrected wording |
|---|---|
| §1 table, "MOS capacitor … d2s: hv PMOS acc. 16 × 16 (Miller)" | "… d2s: hv PMOS acc. W 7.96 × L 32.16 µm (256 µm², CMA and CMB, in the pad's ESD gap)" |
| P7, "RN1 … with gate and drain on n2 … the centre drain of the upper Clamp_N frame" | "… on dabn … the drain nearest the array centre (x 39.045, gates 16 and 17) of the upper Clamp_N frame" |
| P7, "RP1 … the centre column, gate and drain on n1" | "RP1 is gate 21, gate and drain on dabp (drain x 39.245). Gate 20, the other gate of that drain, is the dummy; its gate is jumpered to its source (iovdd)" |
| P7, "The PCell option (`rep`, `rep_at`, `rep_side`) is prototyped, not yet in `scripts/pcells`." | "Implemented as `Clamp_*_M1` with `wiring = external` plus `Clamp_*_M1_wiring` (roles `16:rep 17:rep` for the upper N frame, `20:dummy 21:rep` for P). Each bus segment is fed from its frame end in the pad cell" |
| §4 sketch, "DCPDiode (+ CMA, pad-connected well)" | "DCPDiode. Between DCNDiode's and DCPDiode's guard rings (y 41.46–50.66): CMA (well = pad) and CMB (well = b)" |
| §4 table, PMOS 84–119 "Miller caps 618 on top", and "The Miller capacitors are the first to move, up into the logic band or out of the cell" | "Miller caps are in the ESD gap (y 41.46–50.66); none in the PMOS zone" |
| §4, "M3 is usable only in the gaps between the bands: 119–126 and 134–140 µm" | "… gaps at 91.5–93.5, 119–126 and 134–140 (below 84: 3–7, 32.5–34.5, 60–66)" |
| §7 item 5, "RP1 / RN1 inside the clamp frames: prototyped …; mock-up …" | "In the pad cell on the PCells; dabp / dabn routed to pins at y 85–86" |
| §7 item 6, "CMA's pad-connected n-well: guard ring and latch-up rules" | "CMA sits between DCNDiode's n+ guard ring and DCPDiode's p+ guard ring, with no ring of its own; LU.a / LU.d / LU.d1 (Python, from the maximal deck) are clean" |

Netlist `d2s_mpdda_pd.spice`: `wc=16u lc=16u` should become `wc=7.96u lc=32.16u`, since the schematic follows the layout.

`inputs/replica_report.md` (superseded by the grown frames, ng 43 / 35, and by the pad wiring here):

| statement | corrected wording |
|---|---|
| §1, RN1 "gates 16 and 17 around drain column 8, at x = 40.000 µm" | "… drain column 8 at x 39.045 (ng 35, l 1 µm)" |
| §1, RP1 "column 20 at x = 39.865 µm"; "its drain partner, column 21, becomes a dummy" | "RP1 = gate 21 (x 39.835–40.435), dummy = gate 20, shared drain at x 39.245" |
| §1, "New M1 pin `rep`"; "The `gate` bus stays one piece …"; "M1 link at the bottom" | "The drain is labelled with `rep_net` (dabp / dabn). The bus is split into segments around the replica, each fed from its frame end. The jumpers are in the top 0.30 µm of the S/D strips" |
| §1 / §6, "the P comb line at x = 40.755 becomes n1 … from y = 67.865 … to y = 88" | "dabp: x 38.94–39.55, y 67.805–86.0 on the RP1 drain" |
| §1 / §6, "N comb line at x = 40.000 … pad stub y 0–13.145 … jogs … to x = 39.245" | "pad stub at x 39.045, y 2.8–13.205; dabn from the RN1 drain on x 38.15–38.45 up to y 86.0" |
| §1, "carved at today's ng: OP 78, ON 66 … I_Q ≈ 195 µA" | "frames grown: OP 82 (546.12 µm), ON 68 (299.2 µm), I_Q ≈ 205 µA by the 5 µA rule" |
| §2, "Why not a literal split … a/b would need two separate drops from the front end" | "split; the halves are joined above the P frame in Metal2 (a at y 86.4–87.0, b at y 87.4–88.0)" |
| §5, "At pad level the nets are n1 / n2" | "dabp / dabn" |
| §6, "DCN and DCP each lose 4 feeds around x ≈ 40" | "DCNDiode loses the cathode feed at x 39.045; DCPDiode keeps all 22 anode feeds" |
| §6, "If RN2 sits in the NMOS zone (119–140 µm), n2 runs about 100 µm up the cell" | "dabn ends at y 86, about 68 µm from RN1's drain, where RP2 / RN2 are to sit" |
| §8.8, "Pre-existing M2 near-misses … at x ≈ 32.0 and 47.2" | "None: Metal2 is rebuilt, and M2.b / M2.e and their near-misses are 0" |

## 8. Open points

1. **Schematic:** CMA and CMB need W 7.96 µm, L 32.16 µm (`wc`, `lc`).
2. **Band:** the 6–61 ring's horizontal Metal1 path above DCNDiode is now the guard ring's 0.34 µm; it was 3.86 µm. The band / DCNDiode guard (`guard`, iovdd in the netlist) is still not tied to a supply inside the cell.
3. **Joins block the way up:**
   - The a and b joins enclose the dabp/dabn pins.
   - The pad comb ends at the P drains (y 81.45), whereas IHP's comb runs to the core side.
   - So RP2/RN2 and any upward pad connection need Metal1 under the joins, or the joins move up. Decide when RP2/RN2 are placed.
4. **CMA's pad-connected well** has no guard ring of its own. LU.a, LU.d and LU.d1 are clean in my implementation; no ESD or latch-up review was done.
5. **Via counts at the capacitor taps:** CMA's gate has 2 Via1 at its landing, CMB's well 32. Current capacity is not evaluated.
6. **Exactly at the rule by construction:** NW.b1 = 1.80 at six places, Cnt.f = 0.11 at 92 contacts.
7. **63/0 GateDecode footprint box** in the top cell (open question from the log).

## 9. Not verified

- The IHP DRC deck itself (it needs the KLayout application ≥ 0.29.11); I used the Python subset above instead.
- PDK LVS: the diodes are not extracted as devices, and the diode and clamp sheets were not compared.
- Antenna rules, density and fill.
- Current density and electromigration in the junction, stubs, side plates and feeds.
- Coupling of dabn to pad at the junction cut and over the DCNDiode stripes.
- Simulation of the new capacitor shape.
- The GUI / cni PyCell path; only the Python module was used.
- Whether the KLayout DRC engine's `sep` has the same wide-to-wide gap noted in section 5.
