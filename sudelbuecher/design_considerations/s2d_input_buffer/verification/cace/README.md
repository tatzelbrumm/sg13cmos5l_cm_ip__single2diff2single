<!--
SPDX-FileCopyrightText: 2026 Christoph Maier
SPDX-License-Identifier: Apache-2.0
-->
# CACE characterization: s2d_mpdda (draft)

Characterizes the pad input buffer of `../../s2d_input_buffer.md`. The setup follows the
`d2s_miller` deck in `../../../class_ab_pad_driver/verification/cace`: one `.yaml`, one xschem
template per kind of analysis, and a wrapper cell as the DUT. The templates were written for this
setup; there is no generator to edit.

```
cd verification/cace
cace s2d_mpdda_biased.yaml -s schematic                       # everything (514 runs, 6 min on 2 cores)
cace s2d_mpdda_biased.yaml -s schematic -p dc_params loop_params
```

## DUT and fixture

| cell | role |
|---|---|
| `s2d_mpdda` | the buffer, `../../xschem/s2d_mpdda.sch` (six `unit_r2` from `../../../class_ab_pad_driver/improvements/xschem`) |
| `s2d_bias_lp` | test fixture: four ideal reference currents into the bias diodes |
| `s2d_mpdda_biased` | CACE DUT = `s2d_mpdda` + `s2d_bias_lp`, same 13 pins as `s2d_mpdda`; the bias nets are pins so the templates can perturb them |

`../../xschem/xschemrc` adds the driver's `improvements/xschem` to the library path for `unit_r2`.
CACE netlists the DUT with that file. It netlists the templates with the PDK's `xschemrc` and a
primitive copy of the DUT symbol.

## Conditions

| condition | typical | swept in | meaning |
|---|---|---|---|
| vdd | 3.3 V | dc | 3.0 / 3.6 |
| vref | 1.2 V | range | pad reference: 0.5 / 0.8 / 1.2 / 1.65 |
| vcm | 1.2 V | range | internal common mode: 1.0 / 1.2 / 1.4 / 1.65 |
| corner_mos | tt | dc, range, loop, ac, tran, noise | ss sf tt fs ff (range, tran: ss tt ff) |
| corner_r | typ | dc | bcs typ wcs (rhigh: unit degeneration) |
| temp | 27 °C | dc, range, loop, ac, tran, noise | −40 / 125 |
| cload | 0.5 pF | loop, tran | external load per output, on top of the built-in 2 × 12 × 12 µm MOS capacitors: 0.001 / 0.5 / 2 / 10 pF in loop, 0.001 / 0.5 pF in tran (the 1 µs settling limit is for ≤ 0.5 pF) |
| ibias_err | 0 | dc_bias | common error of the four reference currents, ±40 % |
| va_bias | 1e12 V | dc_bias | "Early voltage" of the reference sources, R_k = va_bias / I_k |
| umax, vstep | 0.5 V | dc, tran | sweep range of u = vin − vref; step size of u |

## Parameter groups

| group | template | quantities |
|---|---|---|
| dc_params, range_params, dc_bias_params | `_tb_dc` | Gain, Vos_in (referred to the input), INL (u = ±0.5 V, referred to the input), Vcm_err, Idd |
| loop_params | `_tb_loop` | T0, fc, PM, GM of the differential and of the common-mode loop (broken at vfbp / vfbn; injection +1/−1, then +1/+1) |
| ac_params | `_tb_ac` | Acl at 1 kHz, f3dB, output CM response to vdd |
| ac_mm_params | `_tb_ac` | PSRR (vdd, vss) and CMRR (vin and vref together), input-referred, with mismatch |
| tran_params | `_tb_tran` | rise 10–90 %, 1 % settling, overshoot, output CM deviation, for a ±0.25 V step through the 587 Ω pad resistor |
| noise_params | `_tb_noise` | input noise at 1 kHz and 100 kHz, differential output noise 10 Hz–10 MHz |
| mm_params, mc_params | `_tb_dc` | Vos_in, Gain, Vcm_err (mismatch: tt_mismatch; process: tt_stat) |

Spec limits are the proposals of `s2d_input_buffer.md` section VII, not requirements. The rejections
are in their own mismatch group: without mismatch the cell is symmetric, and its differential PSRR
and CMRR come out as several hundred dB.

**Process Monte Carlo keeps rhigh at `typ`.** The PDK's `res_stat` draws the "global" sheet-resistance
deviation of rhigh (`nsig_rsh = agauss(0,1,1)`, 5.1 % σ, `resistors_mod.lib`) in a `.model` inside the
`rhigh` subcircuit. In ngspice every instance then draws its own value, which acts as 5 % mismatch
between the units. With `corner_r: stat` the first run gave a gain of 1.83…2.36. The `d2s_miller`
setup's first run shows the same (gain 0.415…0.605 for 0.5). Real global rhigh spread is covered by
the `bcs` / `wcs` corners in dc_params.

The enable (`en_3v3`) is not in CACE. Its decks are `../../sim/tb/tb_s2d_pd_*.spice`.

## Template conventions (from the d2s_miller setup, kept)

- Data file name relative: `echo … > CACE{filename}_CACE{N}.data`.
- `CACE{simpath}` appears once, in a schematic text, so that CACE's plotting finds it.
- Scalars across analyses go through `set s_x = $&x` (loop and AC templates run several analyses).
- `.noise` uses `sparse`, not `klu`.
- Slow parallel runs: `export OMP_WAIT_POLICY=passive OMP_NUM_THREADS=1`.

## Readable output

CACE writes its datasheet to `_docs/` next to the yaml (`s2d_mpdda_biased.md` and plots), as the
`d2s_miller` and `OgueyAebischerBias` setups do. The level shifters' convention, CSV and plots in
`results/<cell>/`, also works with this yaml unchanged:

```
python3 <main repo>/scripts/cace/cace_to_csv.py s2d_mpdda_biased.yaml dc_params _runs/RUN_<date> results/s2d_mpdda_biased/dc_params.csv
```

Which of the two the project keeps is open (`../../../class_ab_pad_driver/improvements/log.md`,
2026-10-19).

## Moving into sg13cmos5l_IOPadSingle2Diff (later)

- In the yaml, change `paths.schematic` to `../schematic/xschem`.
- `s2d_bias_lp` (ideal currents) is replaced by the real tree, `s2d_bias_out` or `s2d_bias_in` from
  one 5 µA leg. Then `ibias_err` and `va_bias` act on that single input instead of four references.
