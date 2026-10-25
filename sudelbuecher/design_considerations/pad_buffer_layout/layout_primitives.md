<!--
SPDX-FileCopyrightText: 2026 Christoph Maier
SPDX-License-Identifier: Apache-2.0
-->
# Layout primitives for the two pad buffers (`d2s_mpdda`, `s2d_mpdda`)

2026-10-26. A proposal written by Claude (Opus 5.5) for Christoph Maier. Nothing here is drawn yet.

Sources:
- devices: `macros/*/netlist/source/` (`units.spice`, `d2s_mpdda.spice`, `d2s_bias_lp.spice`,
  `s2d_mpdda.spice`, `s2d_bias.spice`);
- footprints: `macros/sg13cmos5l_IOPadDiff2Single/layout/klayout/size_mockup/d2s_mpdda_size_mockup.gds`
  (IHP PCell bounding boxes);
- rail bands: `macros/IOPad/layout/klayout/sg13cmos5l_IOPadAnalog.gds`;
- your class-AB cell: `macros/sg13cmos5l_IOPadDiff2Single/layout/klayout/sg13cmos5l_IOPadDiff2Single.klay.gds`;
- mismatch budget: `design_considerations/consolidation/mismatch_2026-10-25/README.md`.

## 1. What the two buffers share

Both buffers are built from the same `unit_r2`, the same folded cascode and the same bias diodes. Each
primitive below serves both pads; only the count differs.

| primitive | device (finger) | d2s | s2d | sets |
|---|---|---:|---:|---|
| unit input device | hv PMOS 2 × 10/1, bulk = source | 8 | 12 | offset (pairs ≈ 1.7 mV) |
| unit tail | hv PMOS 5/6, n-well on iovdd, gate vbp; same device as bias diode BP | 8 | 12 | offset (tails ≈ 1.4 mV) |
| unit resistor | rhigh 0.5 × 50.6 µm, 150 kΩ | 4 | 6 | gain (all of σ = 0.77 %) |
| fold sink | hv NMOS 6/6 (s2d), 9/6 (d2s); same device as BN (6/6) | 2 × 4 f | 2 × 6 f + 2 × 4 f | offset (sinks 5.4 of 6.1 mV) |
| PMOS load | hv PMOS 6/4 | 2 × 4 f | 3 × 4 f | offset (loads 1.7 / 1.3 mV) |
| cascode | hv NMOS / PMOS 15/3 (lcas = 3) | 4 × 2 f | 7 × 2 f | — (mismatch divided by the cascode gain) |
| bias + enable | `d2s_bias_sel_pd`, `en_ctrl_3v3`, 3 × `ls_up_1v2_3v3` | 1 | 1 | identical macro |
| MOS capacitor | d2s: hv PMOS acc. 16 × 16 (Miller); s2d: hv NMOS inv. 12 × 12 (load) | 2 | 2 | — |
| class-AB loop | hv PMOS 6.66/0.6, hv NMOS 4.4/1 = the output-device finger | 8 | — | I_Q (σ ≈ 10 µA) |

The Monte Carlo sees random mismatch only, and random mismatch falls only with area. Layout removes the
systematic part: gradients, stress, IR drop and temperature, none of which the MC sees. So the budget
says where area helps, and the sensitivities below say where layout care matters.

Input-referred sensitivities of a unit, with strong degeneration (g_m R ≫ 2):
- input device: its ΔV_T, directly;
- tail: V_os ≈ R·ΔI_T/2 = (g_m,T R/2)·ΔV, where ΔV is a tail's V_T or a difference in its source
  potential. g_m,T R/2 is of order 1, so a tail's V_T and the IR drop to its source count about as much
  as an input device's V_T;
- fold sink: a current error at x / y. The sinks carry 30 µA against a tail's 5 µA, so the same relative
  error weighs about six times more. This is why the sinks dominate the budget.

## 2. Group by component, not by pair

Agreed: give each component type its own compact array, not one cell per degenerated pair. Three
reasons:

1. Compact arrays of identical devices cancel gradients best. Each array gets its own dummies and
   identical surroundings.
2. The wells decide it anyway. The input devices have bulk = source, so every one of them needs its own
   n-well: 8 in d2s, 12 in s2d, ≥ 1.8 µm apart (NW.b1). The tails share one n-well on iovdd. rhigh sits
   on the substrate and needs no well. A per-unit cell would have to pack two source wells, an iovdd well
   and a resistor, so it would cover about 20 × 30 µm, and every unit would straddle its own gradient.
3. Each type has its own sensitivity (section 1), so each array can get the care, and the area,
   that it needs.

The cost is routing. Each unit has two internal nodes, sa and sb (tail drain, R end, input source and
well): 8 nodes in d2s, 12 in s2d. Use the same column map for tails and input devices, and put each tail
directly above its input device. Then every sa / sb wire is a short vertical M2 of the same length. The
R block sits beside them, and its wires go to the columns.

## 3. Primitives

**P1 `tub`: one input device in its own well.** hv PMOS 2 × 10/1 (as now) in an n-well, with an ntap
ring tied to the source (well = source = sa / sb).
- Every copy has identical geometry: the same gate-to-well-edge distance on all four sides (well
  proximity) and the same ring. Its position in the array then changes only its gradient.
- Dummies are the same tub, switched off (gate, source and well on iovdd).
- Pins g, d, s; parameters nf, W, L.
- The well-to-substrate capacitance lands on sa / sb, the same for every unit. Substrate noise
  then couples in as common mode, provided the wells are identical and cross-coupled.

**P2 `tail_row`.** hv PMOS 5/6 single devices in one n-well on iovdd, with a common gate (vbp) and a
common source bus.
- Same column map as the tubs (section 5).
- The bias diode BP is the same device and replaces an end dummy. Its mismatch to the tails moves all
  tail currents together, which leaves the gain unchanged, so BP does not need the centroid.
- The pattern of `JanteStroemSpejl/` (a source down the middle, a gate cross, the diode in the cross
  arm) is an already characterised layout of exactly this kind of block.
- The source bus taps iovdd at one point (section 6).

**P3 `rhigh_cc`: the resistor block.**
- Split each 150 kΩ into 4 series segments of about 12.7 µm. That gives 16 strips in d2s and 24 in
  s2d, interleaved common centroid, with one dummy strip at each end and heads joined in M1.
- Use the same segment count in every unit, so the head and contact resistance cancels in the ratio.
- For LVS, use either the PCell's bends or 4 series devices in the netlist.
- Surround the block with a p+ tap ring to iovss.
- Width option: the gain σ of 0.77 % is all resistor mismatch (1.03 % per resistor in the model,
  5 %·µm). With w = 1.0 µm at L ≈ 106 µm (W_eff = W − 0.04 µm; 1360 Ω/□ × 105.9 / 0.96 ≈ 150 kΩ,
  trim in simulation) the area quadruples and σ_gain halves to about 0.4 %. That costs +323 µm² in
  d2s and +484 µm² in s2d, cheap next to everything else here.

**P4 `nsink_row`.** hv NMOS 6/6 fingers on vbn, with a common source bus. BN is the same finger and
takes an end position.
- Harmonise d2s's SX / SY from 4 × 9/6 to 6 × 6/6 (the same 36/6). Both pads then use one primitive,
  and the ratio to BN is a finger count in both. This needs a re-simulation, because the fingers'
  diffusion and gate-edge parasitics change slightly.
- This is where the offset is: 5.4 of 6.1 mV, in both buffers. Only area reduces the random part.
  Four times the fingers takes the sinks to 2.7 mV and the total to about 3.9 mV (`FILL_IN.md` point
  4). Make the finger count a parameter, so that the 4× option is a parameter change.
- The 4× option needs 2 × 24 fingers × about 6.6 µm, i.e. 4 rows across the 80 µm width, about
  2500 µm². That is more than the whole NMOS zone of section 4, so with 4× the sinks leave the pad cell.

**P5 `pload_row`.** hv PMOS 6/4 fingers: PL / PR in d2s (2 × 4), LP / LN / D in s2d (3 × 4).
Interleave ABBA, with D in the middle in s2d.

**P6 cascodes.** 15/3 fingers next to the device they cascode, in the same orientation. They need no
centroid.

**P7 `ab_loop` (d2s only): replicas inside the clamp frames.** The output devices and the translinear
replicas are the same finger: OP = 82 × 6.66/0.6 and RP1 = 2 such fingers; ON = 66 × 4.4/1 and
RN1 = 2 such fingers. RP2, FPL and ABP are single 6.66/0.6 fingers; RN2, FNL and ABN single 4.4/1
fingers. I_Q ≈ (82/2) × 5 µA ≈ 205 µA (212 µA in simulation) relies on OP matching RP1.
- So put RP1 into the Clamp_P frame and RN1 into a Clamp_N frame. RP1's two fingers share one drain
  stripe, so they can be cut out of a row as one S-G-D-G-S group, with gate and drain on n1 and the
  sources shared with OP's neighbours.
- The output devices are the cell's heat source. A replica in the bias tree, 100 µm away, would not see
  their temperature or their stress; a replica inside the frame sees both.
- Cost: OP drops to 80 fingers (ratio 40, I_Q ≈ 200 µA), or the frame gets one extra drain stripe.
  Your `_manualPcell` variant could take a "split off k fingers" parameter.
- Place RP2, FPL and ABP as a 3-finger group directly next to the frame, and likewise for the NMOS side.

**P8 `bias_ctrl` hard macro.** `en_ctrl_3v3` + 3 × `ls_up_1v2_3v3` + `d2s_bias_sel_pd`, laid out once
and placed identically in both pads. It goes in the band under the 1.2 V vdd / vss rails, where IHP
places LevelUp / LevelDown and where the ls_up input inverters find their supply.
- The diodes BP, BN, BPC and BNC move into the arrays they bias (P2, P4, and next to the cascodes for
  BPC and BNC). The tree then sends currents, not voltages, to the arrays. That is the sharing rule of
  `s2d_bias.spice`: "bias crosses from one block to another only as currents".
- LVS consequence: the layout hierarchy no longer follows `d2s_bias_sel_pd`. Either flatten for LVS, or
  move the four diodes from `d2s_bias_sel_pd` into the buffer sheets (`d2s_mpdda_pd`, `s2d_mpdda_pd`).
  Moving them is cleaner.

**P9 MOS capacitors.** They need no matching; use them to fill left-over space. One exception:
the A-side Miller capacitor CMA has its n-well on vout = pad. That makes it a pad-connected n-well, i.e.
an extra diode from the pad to the substrate, and a latch-up injector when the pad undershoots. Put it
inside the ESD zone's guard rings, next to DCN / DCP, and check it against the latch-up rules. The s2d
load capacitors (hv NMOS, S/D/B on vss) do not have this issue.

## 4. Floorplan in the 80 × 180 µm cell

M3 and M4 carry the IO ring as horizontal bands across the full width from y = 0 to 178, and TM1 up to
y = 134. The analog blocks underneath therefore route in M1 / M2. M3 is usable only in the gaps between
the bands: 119–126 and 134–140 µm. Signals come in from the core side on M2.

```
 y (µm)                                                    ring rails above (M3/M4)
 180 ┌──────────────────────────────────────────────┐  core side: vinp vinn vref ibias en sel on M2
     │ P8 bias_ctrl (identical in both pads)        │  vdd / vss 1.2 V  140–178
 140 ├──────────────────────────────────────────────┤
     │ NMOS: P4 sinks + BN, NMOS cascodes,          │  iovss 126–134
     │       AB N-group (RN2 FNL ABN), P3 R block   │
 119 │ PMOS: P5 loads + PMOS cascodes,              │
     │       AB P-group (RP2 FPL ABP)               │  iovdd 93.5–119
     │ PMOS: P1 tubs 2×4 above P2 tails 2×4 (+BP)   │  iovdd 66–91.5
  84 ├── guard rings (latch-up rules) ──────────────┤
     │ Clamp_P frame: OP 80 f + RP1 2 f             │
     │ DCPDiode   (+ CMA, pad-connected well)       │  iovss 34.5–60
     │ DCNDiode                                     │  iovss 7–32.5
   5 │ 2 × Clamp_N frame: ON 64 f + RN1 2 f         │
   0 └──────────────────────────────────────────────┘  pad side
```

IHP's IOPadAnalog fills y = 84–140 (80 × 56 µm) with a p+ substrate tap, and y = 140–180 (80 × 40 µm)
with secondary protection and level shifting. This proposal takes both zones for the buffer and keeps
the latch-up protection as guard rings instead of the tap plate. Check that against the LU rules first.

Rough area, as the sum of device bounding boxes from the size mockup, without spacing. Spacing,
wells and guard rings make it 1.5–2× larger.

| zone | available | d2s contents (bbox sum) |
|---|---:|---|
| PMOS, 84–119 | 80 × 35 = 2800 µm² | tubs 387, tails + BP 445, loads 276, cascodes 270, AB ~100: ≈ 1480; Miller caps 618 on top |
| NMOS, 119–140 | 80 × 21 = 1680 µm² | sinks 529, cascodes 244, small ~100, R 187: ≈ 1060 |
| logic, 140–178 | 80 × 38 = 3040 µm² | bias_ctrl (not laid out yet) + overflow |

- d2s: plausible but tight. The Miller capacitors are the first to move, up into the logic band or
  out of the cell.
- s2d: it does not fit, because it has 1.5× the units, seven cascodes, three loads and the full input
  protection. Its input `padres` drives gates only, so moving parts of it out of the pad cell costs a
  wire, nothing electrical. Keep the protection and the signal units (A1, A2, F1, F2 with their tails,
  R and sinks) in the cell, and move the CMFB units M1 / M2, their sinks and the load capacitors out.

## 5. Common-centroid maps

Notation: unit half `a` is the device on gp (drain to y), `b` the device on gn (drain to x).

- **Tubs, k = 4 units** (d2s: A, B, C1, C2):

  ```
  Aa  C2b C1b Ba
  Bb  C1a C2a Ab
  ```

  The two halves of each unit are point reflections about the centre, so every unit's centroid is at
  the centre. The a set {Aa, Ba, C1a, C2a} and the b set are both centred too. Linear gradients in x
  and in y therefore cancel for offset (a against b) and for gain (unit against unit). The y gradient
  matters here: the heat comes from the output frames below.
- **s2d signal units:** the same block, with A1, A2, F1, F2 in place of A, B, C1, C2.
- **s2d CMFB units:** a cross-quad, `M1a M2b / M1b M2a`. The a set and the b set sit on the two
  diagonals, both centred.
- **Tails:** the same map as the tubs, each tail directly above its tub, with BP and a dummy at the
  ends.
- **Sinks** (d2s, 6 + 6 fingers): `X Y Y X X Y / Y X X Y Y X`, with BN and a dummy at the ends.
- **R block** (d2s, 4 R × 4 segments): `A B C1 C2 C2 C1 B A A B C1 C2 C2 C1 B A`. Each resistor's
  segments sit at positions summing to 34, i.e. centroid 8.5, the middle of 16.

## 6. Supplies and IR drop

- Tails: a source-potential difference ΔV between two tails gives V_os ≈ (g_m,T R/2)·ΔV, about 1 mV of
  offset per mV of difference. So the tail row's source bus (with BP) taps iovdd at one point and
  carries only front-end current.
- Sinks: the same holds for the sink row's source bus (with BN) to iovss.
- Output stage: up to ~50 mA when shorted, and tens of mA dynamically. Its sources (vddo / vsso,
  already separate pins in `d2s_mpdda`) get their own taps to the ring and never share a bus with the
  front end.

## 7. Decisions this needs

1. Harmonise d2s SX / SY to 6 × 6/6 (re-simulate).
2. rhigh at w = 1.0 µm: gain σ from 0.77 % to ≈ 0.4 %, about +320 / +480 µm².
3. Sinks at 4× area: offset ≈ 6.1 → 3.9 mV, but they no longer fit in the pad cell.
4. Move BP, BN, BPC and BNC from `d2s_bias_sel_pd` into the buffer sheets, so the layout and schematic
   hierarchies match for LVS.
5. RP1 / RN1 inside the clamp frames: a frame variant with a split-off drain stripe.
6. CMA's pad-connected n-well: guard ring and latch-up rules.
7. Custom padframe cell only: leave out M3 under part of the iovdd / iovss rails to gain a third
   routing layer. That needs the harness and IHP to agree, because it thins the ESD ring locally.
8. s2d: confirm what stays in the pad cell (section 4).
