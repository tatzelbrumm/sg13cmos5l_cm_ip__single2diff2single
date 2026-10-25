# Local-mismatch Monte Carlo of the pad buffers, 2026-10-25

Run in the cloud container on 25 Oct 2026, 12:56–13:20 CET.

## Viewing the results

- `pad_buffer_mismatch.html`: open it in any browser. It shows charts and tables of these runs and
  works without a network, because the charting library (d3 v7.9.0) and the data are inside the file.
- The same page on claude.ai, "Pad buffer mismatch": https://claude.ai/artifact/6sk3kKC9VuDHy8c9mS3YM7
  (private unless you share it).
- The per-seed data as plain tables, readable in any text editor: `pad_mc.csv` and `s2d_mc.csv`
  (columns `group`, `seed`, `offset_mV`, `gain`, then `iqp_uA` or `vcm_err_mV`). `budget_20seeds.csv`
  holds the earlier 20-seed budgets that the page shows as grey bars.

## What was simulated

- **Output pad** `sg13cmos5l_IOPadDiff2Single`: the macro schematics as they were on the computer at
  02:57 CET. No `.sch` or `.sym` in `macros/` has changed since.
- **Input buffer** `s2d_mpdda_biased`: the draft in
  `_sudelbuecher/sudelbuecher/design_considerations/s2d_input_buffer/`, including the 22/23 Oct edits
  of `s2d_bias_lp.sch` and `s2d_mpdda.sch`. `unit_r2` is byte-identical in
  `class_ab_pad_driver/improvements/xschem/` and `macros/sg13cmos5l_IOPadDiff2Single/schematic/xschem/`.

## Testbenches and conditions

- **Testbenches:** the CACE DC templates `sg13cmos5l_IOPadDiff2Single_tb_dc.sch` and
  `s2d_mpdda_biased_tb_dc.sch`, netlisted with xschem.
- **DC sweep:** reduced to the three points the measurements use, `vd` = −0.2, 0, +0.2 V (pad) and
  `u` = −0.1, 0, +0.1 V (input buffer). The `INL` values in the data are therefore meaningless.
- **Models:** `.lib cornerMOShv.lib mos_tt_mismatch` (pad also `cornerMOSlv.lib mos_tt_mismatch`),
  `.lib cornerRES.lib res_typ_mismatch`. IHP-Open-PDK dev of 21 Sep 2026, `ihp-sg13cmos5l`; ngspice-47.
- **Common conditions:** 27 °C, vdd = 3.3 V.
- **Pad:** vref = vicm = 1.65 V, vddl = 1.2 V, sel = 0 (harness bias: 5 µA through a PMOS mirror
  without mismatch), 1 kΩ to 1.65 V and 100 pF at the pad.
- **Input buffer:** vref = vcm = 1.2 V, 0.5 pF per output, bias from the internal `s2d_bias_lp`.
- **Seeds:** `.option SEED = 12345 + n`, n = 1…N, the same numbering as CACE's iterations. Every group
  reuses the same seed numbers.
- **Groups:** all devices keep `mm_ok=1` from their symbols. In a group run, `mm_ok` stays 1 only on
  the listed instances and is set to 0 on all others.

| group | instances with mismatch |
|---|---|
| `all` | every device with `mm_ok=1` |
| `R_unit` | `XR` (rhigh 0.5 × 50.6 µm) in every `unit_r2` |
| `sinks` | `XSX`, `XSY` in `d2s_mpdda_pd` (pad) or `s2d_mpdda` (input buffer) |
| `loads` | `XPL`, `XPR` in `d2s_mpdda_pd` |

## Measurements

- **Pad** (`*_tb_dc.sch` code block):
  - `Vos_out = v(pad) − v(vref)` at vd = 0 (output offset; gain 0.5);
  - `Gain = (vo(+0.2) − vo(−0.2)) / 0.4`;
  - `IqP` = output PMOS drain current at vd = 0.
- **Input buffer:**
  - `Gain = (vd(+0.1) − vd(−0.1)) / 0.2` with vd = voutp − voutn;
  - `Vos_in = vd(0) / Gain` (input offset; gain 2);
  - `Vcm_err = (voutp + voutn)/2 − vcm` at u = 0.

## Results

Mean / σ (min … max).

| buffer | group | seeds | offset | gain | third quantity |
|---|---|---|---|---|---|
| pad | all | 150 | −0.81 / 6.09 (−20.97 … 16.33) mV | 0.5000 / 0.0038 = 0.75 % (0.4899 … 0.5116) | IqP 212.9 / 10.2 µA |
| pad | R_unit | 60 | 0.057 / 0.000 mV | 0.5002 / 0.0038 = 0.77 % | IqP 212.4 / 0 µA |
| pad | sinks | 60 | −0.21 / 5.40 (−13.76 … 11.05) mV | 0.4999 / < 0.01 % | IqP 212.6 / 2.8 µA |
| pad | loads | 60 | 0.15 / 1.70 (−3.30 … 4.29) mV | 0.4999 / < 0.01 % | IqP 212.5 / 1.2 µA |
| input buffer | all | 100 | −0.54 / 6.73 (−16.90 … 14.86) mV | 2.000 / 0.018 = 0.90 % (1.956 … 2.042) | Vcm_err 11.9 / 11.0 mV |
| input buffer | R_unit | 60 | 0.007 / 0.077 mV | 2.000 / 0.015 = 0.77 % | Vcm_err 12.4 / 0.08 mV |
| input buffer | sinks | 60 | −0.26 / 5.30 (−13.56 … 10.79) mV | 1.999 / < 0.01 % | Vcm_err 14.0 / 4.7 mV |

Pad, against the CACE limits of `mm_params`: 1 of 150 seeds beyond ±20 mV offset, and 2 of 150
outside the 0.49–0.51 gain window. Input buffer: 0 of 100 outside ±20 mV and 1.93–2.07.

For the pad, the groups not run today (unit pairs, unit tails) account for about 2.3 mV, taken by
difference from the total. The 20-seed budget of 2 Oct
(`class_ab_pad_driver/improvements/sim/results_improvements.txt`, lines 118–134) has 1.7 mV for the
pairs and 1.4 mV for the tails. For the input buffer, the 20-seed budget of 20 Oct
(`s2d_input_buffer/sim/results_s2d.txt` §9) has pairs 1.72, tails 1.42 and loads 1.34 mV.

## Mismatch model behind the numbers (PDK, `libs.tech/ngspice/models/`)

- **rhigh:** `cornerRES.lib` `res_typ_mismatch`, lines 67–73: 5.0 %·µm per resistor, plus width and
  length terms of 0.009 µm^1.5. For the unit resistor that is 1.03 % per resistor and 1.45 % for a
  pair. IHP's process spec (SG13G2, §2.9, MATRHIGH = 48 nm) gives 0.95 % for a pair of that size,
  so the model is about 1.5× more pessimistic.
- **MOS:** `sg13g2_moshv_mismatch.lib`, lines 20–26:
  - HV PMOS: ΔVT 4.5 mV·µm, current factor 0.4 %·µm;
  - HV NMOS: 7 mV·µm, 0.5 %·µm;
  - all per device, so ×√2 for a pair.

## Files

- `pad_buffer_mismatch.html`, `pad_mc.csv`, `s2d_mc.csv`, `budget_20seeds.csv`: see Viewing the results.

Each `.json` maps a group name to a list of per-seed results in seed order (n = 1…N). Values are SI
(V, A).

- `IOPadDiff2Single_all.json`: group `all`, 150 seeds; keys `Gain`, `Vos_out`, `INL`, `Iio`,
  `Icore`, `IqP`, `IqN`, `Imin`.
- `IOPadDiff2Single_groups.json`: groups `R_unit`, `sinks`, `loads`, 60 seeds each; same keys.
- `s2d_mpdda_biased_all.json`: group `all`, 100 seeds; keys `Gain`, `Vos_in`, `INL`, `Vcm_err`,
  `Idd`.
- `s2d_mpdda_biased_groups.json`: groups `R_unit`, `sinks`, 60 seeds each; same keys.
