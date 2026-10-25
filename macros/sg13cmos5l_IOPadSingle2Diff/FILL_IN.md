<!--
SPDX-FileCopyrightText: 2026 Christoph Maier
SPDX-License-Identifier: Apache-2.0
-->
# `sg13cmos5l_IOPadSingle2Diff` — what still has to be filled in

Scaffolded 2026-10-20 from the structure of `../sg13cmos5l_IOPadDiff2Single`; the placeholder
amplifier was replaced on 2026-10-25 by the input buffer of
`sudelbuecher/design_considerations/s2d_input_buffer` (see `README.md`). Items 1–5 of the 2026-10-20
list are done; how the scaffold was adapted where it conflicted with the design is in `README.md`,
"Changes against the scaffold".

## Done (2026-10-25)

- `xa` = `s2d_mpdda_pd` (wrapper around Christoph's `s2d_mpdda.sch` of 2026-10-23, plus the four
  output-to-vcm ties); its netlists in `netlist/source/` (`s2d_mpdda.spice`, `s2d_bias.spice` copied
  unchanged, `s2d_pd.spice` with `en_3v3_b` as a port).
- Spec limits: the buffer's from `s2d_input_buffer.md` section VII, the pad-level ones from the first
  full run.
- CACE groups dc, range, window, dc_sel, dc_sel3, dc_ibias, ac, ac_mm, tran, noise, pd, enable, mm, mc,
  and the loop fixture `s2d_mpdda_pd_sel` (loop_params).
- Output load 0.5 pF per output (the design's "wiring plus the next stage's unit gates"), on top of the
  buffer's built-in 2 × 12 × 12 µm MOS capacitors.

## Still open

1. **Bias sharing.** `xb` = `d2s_bias_sel_pd` makes all six of the driver's lines; the buffer uses
   four. The class-AB legs (NABP, PABN, about 10 µA with their diodes) run for nothing here. Options:
   an `s2d` variant of the tree without them, or one root per slot with a fan-out leg per consumer
   into `_out` trees (`d2s_bias_out_pd`, `s2d_bias_out_pd`), as `s2d_input_buffer.md` section III
   proposes and `testbenches/spice/tb_s2d_loopback.spice` simulates.
2. **Internal common mode** 1.2 V for both buffers (`s2d_input_buffer.md` section IV and open point 1):
   the output pad's CACE suite still uses vref = vicm = 1.65 V; and where vcm comes from (the vcm pin,
   an internal reference, the harness `vbias`).
3. **Pad reference** (open point 2): `vref` from the vcm pin (pad range about 0.7 … 1.7 V) or an
   internal ~0.5 V reference so that the pad range includes iovss.
4. **Offset**: whether 6–7 mV σ is enough, or the fold sinks SX / SY get 4× the area (open point 4).
5. **Enable glitch** (open point 5): the design saw −1.6 / +1.1 V of output common mode for about
   1 µs with its `s2d_bias_out_pd` tree; in this pad (en_ctrl_3v3 + d2s_bias_sel_pd) see
   `enable_params`.
6. **CMFB dump branch, built-in output capacitors** (open points 7, 8 of the design note).
7. **Sheets**: `s2d_mpdda_pd.sch` and `s2d_mpdda_pd_sel.sch` are generator-placed (2026-10-25) and may
   want tidying; `s2d_core_ideal.{sch,sym}` (the old placeholder) are no longer used.
8. **Unpowered pad**: the secondary diodes clamp padres to iovdd, which the slot cannot switch; not
   simulated.
9. **Fallback wiring**: in `../slot` the S2D input sits behind the harness IOPadAnalog's own
   protection (`s7_an_0_esd`), so this cell's protection is redundant there; decide whether the
   fallback gets a variant without `CP CN DN DP SP`.
10. **Layout**: none yet. As a custom padframe cell it must abut the IHP IO cells (ring rails, cell
    height, pitch); see `../slot/README.md`, "Priority: custom padframe cells". Six units must match
    (common centroid, same surround), as for the driver.
