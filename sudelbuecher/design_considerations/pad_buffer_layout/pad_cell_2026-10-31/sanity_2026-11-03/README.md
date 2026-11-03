<!--
SPDX-FileCopyrightText: 2026 Christoph Maier
SPDX-License-Identifier: Apache-2.0
-->
# Sanity check of the backannotated pad cell (C2, 2026-11-03)

Christoph: "CMA and CMB, symmetric with 2kΩ stage, if it passes DRC, LvS, and verification (not the full CACE program,
but a short sanity check)", and "fold it into the sanity check for now" (the CACE swing-end loop check).

## What ran

- DUT: the xschem sheet `sg13cmos5l_IOPadDiff2Single.sch` as backannotated to the drawn cell (design commit 2abcca1),
  netlisted for simulation (`lvs_netlist 0`, `lvs_ignore 0`, so Rsub is in). `decks/pad_fb.spice` is that netlist
  with one change: `Xd`'s `vfb` pin is brought out as port `fb` of a copy named `pad_fb`. In the drawn cell vfb is the
  pad (Kelvin line); the loop decks close it through 1 GH and inject through 1 F (as agent K's decks), the step decks
  close it with a 0 V source. `decks/others.spice` is `bias_ref_pd.spice` without `bias_tree_pd` (the sheet's own
  tree is in `pad_fb.spice`); `en_ctrl_3v3` and `bias_gen_pd` sit next to the cell as in `tb_pad_dc.spice`.
- tt, 27 °C, selection 0 (s0 = s1 = 0), harness iDAC 5 µA. Pad = vref + vd/2, vref = 1.65 V; vd = −1.3 / 0 / +1.3 V
  gives pad 0.99 / 1.65 / 2.29 V (vref ± 0.65 V).
- Loads as agent K's stage 8: 1 kΩ to 1.65 V ‖ 100 pF, and unloaded (1 GΩ) ‖ 300 pF.
- Runs (ngspice, run in `decks/` with the PDK `.spiceinit`; the `.include` paths of the macro sources are absolute
  paths of the cloud container): `loop_<CL>_<vd>.spice` → `loop.dat`; `step_<CL>.spice` → `step_<CL>.dat`,
  evaluated by `steps.py` (K's `stepm`) → `steps.txt`, `steps.png`. Logs: `logs/claude/c2-pad-layout/sanity/`.
  No log has "Timestep too small" or a transient-op fallback.

## Simulator options

Agent K's option set (`method=gear`, `rshunt=1e10`, `gmin=1e-15`, …), which the former S-varicap CMA / CMB needed,
puts this netlist's operating point into a latched state (pad 3.28–3.30 V); those runs are kept in
`logs/.../sanity/latched_with_K_options/` and are not results. With ngspice's default options the op is correct
(pad 1.650 V, I_Q 308.4 µA, the same as `tb_pad_dc`). The decks use the defaults.

## Results (measured)

Loop gain T = −v(pad)/v(fb); K's numbers are his stage-8 v8 fixture (`d2s_mpdda_pd_sel` + v8 capacitors,
`agents_c2/K/out/logs/loop13.dat`; K's bottom point is vd = −1.4, pad 0.94 V).

| load | pad (V) | T0 (dB) | f_c (MHz) | PM (°) | GM (dB) | K v8: PM / GM |
|---|---|---|---|---|---|---|
| 1 kΩ ‖ 100 pF | 0.99 | 82.6 | 1.55 | 78.7 | 23.3 | 79.8 / 22.8 (0.94 V) |
| 1 kΩ ‖ 100 pF | 1.65 | 79.6 | 1.37 | 72.9 | 23.6 | 73.2 / 23.9 |
| 1 kΩ ‖ 100 pF | 2.29 | 91.5 | 1.80 | 75.7 | 16.5 | 76.2 / 16.8 |
| unloaded ‖ 300 pF | 0.99 | 103.4 | 1.32 | 44.3 | 20.4 | 44.7 / 21.2 (0.94 V) |
| unloaded ‖ 300 pF | 1.65 | 104.4 | 1.40 | 42.7 | 19.4 | 42.7 / 20.0 |
| unloaded ‖ 300 pF | 2.29 | 104.9 | 1.48 | 40.0 | 17.3 | 40.2 / 18.1 |

Steps (`steps.txt`): 1 kΩ ‖ 100 pF: no overshoot, 1 % settling 0.32–0.39 µs for the swing-end steps, 0.33 µs for
±0.1 V. Unloaded ‖ 300 pF: overshoot 10.3 / 12.7 / 14.4 % (mid→bottom, bottom→top, top→mid), settling 0.70–0.78 µs;
±0.1 V steps 25 % overshoot, 1.07 µs. K's v8: 10.2 / 12.1 / 14.3 %, 0.69–0.78 µs.

I_Q (`tb_pad_dc`, source netlists, selections 0–3 / disabled): 308.4 / 315.6 / 315.8 / 606.8 µA / 0.25 nA. The 2.2 %
rise over the pre-layout 301.8 µA comes from SX / SY at ng 6 (BA's finding); check it against the CACE I_Q limits.

## Reading

The backannotated cell behaves like K's v8 prediction: PM within 1.1°, GM 0.3–0.8 dB lower (reasoning: the added
drawn diode area and dummies; not separated). The 300 pF unloaded case keeps PM ≈ 40–44° over the swing, as
predicted; that is the driver's limit K described, not a layout effect.
