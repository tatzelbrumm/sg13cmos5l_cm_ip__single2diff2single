<!--
SPDX-FileCopyrightText: 2026 Christoph Maier
SPDX-License-Identifier: Apache-2.0
-->
# `sg13cmos5l_IOPadSingle2Diff` — what still has to be filled in

Scaffolded 2026-10-20 from the structure of `../sg13cmos5l_IOPadDiff2Single`. Everything around the
amplifier is real and shared with the output pad; the amplifier itself is a placeholder.

## Already in place (reused, not to be redone)

- Ports and symbol `schematic/xschem/sg13cmos5l_IOPadSingle2Diff.sym`, in this order:
  `iovdd iovss vdd vss pad outp outn vcm vref ibias en_1v2 sel0_1v2 sel1_1v2 vdd1v2_sense vdd3v3_sense`.
  Function: `outp - vcm = vcm - outn = pad - vref` (unity and negative-unity gain).
- `xc` = `en_ctrl_3v3` (fail-safe enable, level-shifted select bits) and `xb` = `d2s_bias_sel_pd`
  (harness ibias / Oguey–Aebischer / bandgap, the six bias lines vbp vbn vbpc vbnc vabp vabn).
- Input protection exactly as IHP's `sg13cmos5l_IOPadAnalog`: gate-tied clamp frames
  `Clamp_P20N0D` / `Clamp_N20N0D`, primary diodes `DCNDiode` / `DCPDiode`, and
  `SecondaryProtection` (587 Ω rppd + diodes) from `pad` to the amplifier input `padres`.
- Makefile (`make sim-cace`, `make spec-table`), CACE yaml and four templates (dc, range, ac, pd);
  they run end to end on the placeholder.

## To fill in

1. **The amplifier `xa`.** Replace `s2d_core_ideal` (two E sources) by the transistor-level buffer,
   keeping its port list `vdd vss padres vref vcm outp outn vbp vbn vbpc vbnc vabp vabn en_3v3`:
   - topology choice: a fully differential amplifier with CMFB around vcm, configured for +1 / −1
     from a single-ended input (e.g. two non-inverting / inverting followers, or a DDA like the
     driver's front end, which already exists as `unit_r2` in `../sg13cmos5l_IOPadDiff2Single`);
   - input range: the proposal demands it include iovss (vssio) and should include iovdd, so the
     input stage needs rail-to-rail inputs (complementary pairs or an input level shift);
   - power-down switches on its own nodes, the way `d2s_mpdda_pd` does it (gates of output devices
     to their rails, class-AB lines off);
   - which bias lines it uses; if it needs others than the six of `d2s_bias_sel_pd`, add outputs
     there rather than passing voltages between blocks.
2. **Its netlist** in `netlist/source/sg13cmos5l_IOPadSingle2Diff.spice` (the reference the sheet is
   checked against) and the sheet of `xa`.
3. **Spec limits** in `verification/cace/sg13cmos5l_IOPadSingle2Diff.yaml` (all `any` now): gain
   error, offset, CM error, input range, bandwidth, PSRR, noise, input leakage when unpowered.
4. **Missing CACE groups**, copy-and-adapt from `../sg13cmos5l_IOPadDiff2Single/verification/cace`:
   `noise_params`, `tran_params` (step, slew), `thd_params`, `enable_params`, `mm_params`, and
   `dc_sel_params` once the core uses the bias. The dc template's measurement points
   (vref ± 0.2 V) and the range template's 1 % gain-error criterion are first guesses.
5. **Load of the outputs**: the templates use 1 pF per output as a stand-in for the next internal
   stage (the gmC filter or the D2S input); set it from the real next stage.
6. **Fallback wiring**: in `../slot` the S2D input sits behind the harness IOPadAnalog's own
   protection (`s7_an_0_esd`), so this cell's protection is redundant there; decide whether the
   fallback gets a variant without `CP CN DN DP SP`.
7. **Layout**: none yet. As a custom padframe cell it must abut the IHP IO cells (ring rails,
   cell height, pitch); see `../slot/README.md`, "Priority: custom padframe cells".
