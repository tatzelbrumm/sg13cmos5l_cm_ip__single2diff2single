<!--
SPDX-FileCopyrightText: 2026 Christoph Maier
SPDX-License-Identifier: Apache-2.0
-->
# Before freezing device dimensions: review of the d2s verification and characterization suites

2026-10-27, Claude (configured model `claude-opus-5-5`). Christoph's request (18:19): "review the d2s_mpdda_pd.sch
verification and characterization suites, suggest where the specifications should be tightened or even improved,
to make sure that we can freeze device dimensions, as preparation for cramming in the layout primitives in the pad."

Reviewed: `macros/sg13cmos5l_IOPadDiff2Single/verification/cace/sg13cmos5l_IOPadDiff2Single.yaml` (17 groups on the
pad sheet, which contains `d2s_mpdda_pd`), `d2s_mpdda_pd_sel.yaml` (loop gain on the fixture), the macro README
(specification table, findings, "Not done"), `netlist/source/d2s_mpdda_pd.spice`, and the floorplan notes in
`sudelbuecher/design_considerations/pad_buffer_layout/layout_primitives.md`. Nothing was run; all numbers are the
README's (runs of 2026-10-20, schematic netlist, ON = 66 at the time).

The README calls every limit a proposal ("worst case of the first full run plus margin"). Freezing needs the opposite
order: a requirement per quantity first, then the sizes that meet it. The list below says, per quantity, which
devices it sizes, so the decisions can be taken in that order.

## 1. Decisions that move device sizes (take these before freezing)

| # | quantity | today | why it blocks a freeze | devices it sizes |
|---|---|---|---|---|
| 1 | offset from mismatch | `mm_params`: 30 Monte Carlo runs, tt only, limit ±20 mV; result −11.4 … +10.1 mV, σ ≈ 5 mV | ±20 mV is 4σ of a 30-run estimate, not a requirement; `mm_params.csv` is empty (`cace_to_csv.py` misses collated runs) | input pairs / tubs, tails, sinks, loads (matched arrays P1–P5); the notes give sinks at 4× area: 6.1 → 3.9 mV, which no longer fits |
| 2 | gain accuracy | 0.49 … 0.51 (±2 %); Monte Carlo 0.494 … 0.508; σ(gain) ≈ 0.77 % (layout_primitives) | 3σ = 2.3 % exceeds ±2 %: the spec passes 30 runs by luck | rhigh width: w = 1.0 µm gives σ ≈ 0.4 % for about +320 / +480 µm² |
| 3 | input common mode and supply range | suite at vref = vicm = 1.65 V; S2D proposes vcm = 1.2 V for both buffers; INL at iovdd = 3.0 V is report-only (11 … 87 mV) | headroom of the input stage depends on both; iovdd's own Vmin is 3.0 V | input-stage devices and their bias; possibly topology |
| 4 | maximum load and phase margin | specified 10 … 300 pF; PM ≥ 40° with worst 41.96° at 300 pF, but `loop_load_params` / `ac_load_params` run at tt, 27 °C, 3.3 V only | the worst corner is not known; 1 nF (PM 24–33°) is report-only | Miller capacitors CMA / CMB (which are about to be reshaped and split: their area is what has to be frozen), output-stage bias |
| 5 | PSRR from iovdd | ≥ 25 dB at 100 kHz, worst 30.7 dB | with everything on the shared IO ring, switching noise of the digital pads couples in at this level; improving it means a different compensation (Ahuja / cascode), i.e. topology | compensation network, possibly a quiet output-stage rail |
| 6 | noise | ≤ 1000 nV/√Hz at 1 kHz (718), ≤ 200 at 100 kHz (156), ≤ 300 µV integrated (235) | limits are worst case plus margin, not a requirement; a real (possibly looser) limit could free area | input pairs and loads (1/f), rhigh |
| 7 | THD | ≤ −35 dB at the worst amplitude (−38.9 dB at vdamp = 1.5 V; −57.8 dB at vd = 1 V, 10 kHz) | −35 dB is 1.8 %; if the pad is a measurement buffer, a per-amplitude requirement is needed | output-stage quiescent current (RP1 / RN1 ratio), front-end linearity |

## 2. Specification gaps that are cheap to close (no design change)

- **Short-circuit current has no maximum.** Only ≥ 20 mA is specified; the worst case is 49.7 mA source, 53.0 mA sink.
  The layout has to carry it in the M2 drain combs and the 0.2 µm source straps (electromigration, heating next to the
  replicas). A maximum (or a current-limit requirement) is what lets the metal widths be frozen.
- **Corners missing from groups that size the compensation:** `loop_load_params`, `ac_load_params`, `tran_params`
  (no temperature), `noise_params` and `thd_params` (tt only). Add corner_mos × temp × vdd (3.0 / 3.3 / 3.6) at least
  for the loop with 300 pF.
- **Resistor corner:** `corner_r` stays `typ` in every group except where set explicitly. The absolute rhigh value sets
  the front end's degeneration (loop gain, bandwidth) and the bias cores; add the resistor corners to `ac_params`,
  `loop_params` and `dc_sel_params`.
- **Mismatch coverage:** run Monte Carlo with enough iterations for a 3σ statement (a few hundred), at tt and at the
  ss / ff × −40 / 125 °C extremes, for offset, gain, I_Q and phase margin; fix the CSV export for collated runs.
- **Unpowered pad** (`testbenches/spice/tb_pd_unpowered.spice`) is not in CACE; the replicas and the antenna diodes
  change the gate nodes, so it belongs in the suite.

## 3. Netlist changes the layout forces (so that the freeze run sees the real devices)

- **DN / DP:** the pad sheet still uses IHP's `sg13cmos5l_DCNDiode` / `DCPDiode` (27.78 µm); the layout has the PCells
  at l = 63.78 µm, 2.3 × the area. Swap to the new `DCNDiode` / `DCPDiode` sheets (macros/IOPad, same pin
  positions). Diode leakage enters `pd_params` (pad leakage off, worst −36.8 nA at ff, 125 °C, limit ±100 nA).
- **OP / ON junctions:** `d2s_mpdda_pd.spice` gives no ad / as / pd / ps, so the model defaults apply. The clamp
  frames have 1.18 µm drains (ESD ballast), 0.64 µm inner and 0.47 µm end sources; IHP's own clamp netlists carry
  ad / as / pd / ps (e.g. `Clamp_N20N0D`). Computing them from the frame rules (`clamp_engine.py`: DRAIN, SOURCE,
  SOURCE_END, w_finger) puts the real drain area into the pad capacitance and the pad leakage at 125 °C.
- **Replicas in the frames** (agent prototype pending): finger counts 82 = OP 80 + RP1 2 and 68 = ON 66 + RN1 2, or
  frames grown by the replica fingers. I_Q ≈ (OP / RP1 fingers) × 5 µA, so the choice moves I_Q from 205 to 200 µA or
  keeps it. RP1 / RN1 (now in the bias sheets) then belong in `d2s_mpdda_pd` next to OP / ON, so that the schematic
  hierarchy follows the layout for LVS, as layout_primitives.md proposes for BP / BN / BPC / BNC.
- **Miller capacitors** reshaped / split: the netlist takes the drawn W / L (LVS compares W and L, not area); CMA's
  well (on the pad) and CMB's well (on `b`) add their well-to-substrate junctions to pad and `b`.
- **Antenna diodes** (`D` on `a` and `b`), if added: small junctions on the two gate nodes.

## 4. Suggested freeze procedure

1. Decide items 1–7 of section 1 (requirements, not run results).
2. Apply section 3 to the sheets, re-run the full suite (both yaml files) with the added corners of section 2, and keep
   the run as the reference ("frozen" netlist plus its results). The current results date from 2026-10-20 with
   ON = 66 and are stale already.
3. From then on, the layout primitives are drawn to those dimensions; any later size change re-opens the reference run.
