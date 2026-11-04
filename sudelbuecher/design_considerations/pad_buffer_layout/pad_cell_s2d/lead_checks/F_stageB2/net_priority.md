<!--
SPDX-FileCopyrightText: 2026 Christoph Maier
SPDX-License-Identifier: Apache-2.0
-->
# Net priority, evaluated after the fact (C3, lead, 2026-11-04)

Christoph: "let F finish, then evaluate net priority ex post facto." Source: magic C-coupled PEX (`sak-pex.sh -m 2`) of
F's stage B (`pad_candidate_B_pex_m2.spice`) and stage B2 (`pad_candidate_B2_pex_m2.spice`). Tables: `net_coupling.md`
(script `net_coupling.py`). Values in fF, measured [M] unless marked as reasoning [R].

## Results

- **pad (vin):**
  - total 96.4 → 81.9 fF;
  - the coupling to vbnc, 12.4 fF in stage B (F had estimated about 10), is 0 in B2;
  - every other sensitive net couples less than 1.4 fF to pad, except outp, at 5.7 fF in both stages.
- **The 5.7 fF from pad to outp is inside P's `s2d_inputs_c3`, not in the routing.**
  - A PEX of the cell alone gives vin – vfbp 5.65 fF. The gate band's M2 tracks run vref vfbn vcm vdd vfbp vin at
    0.48 µm pitch, and neighboring tracks couple about 5.6 fF each: vfbn – vref 5.64, vcm – vfbn 5.56, vdd – vfbp 5.59.
  - [R] It is a capacitance from the output back to the input gate. With the pad driven from 50 Ω (CACE rsrc) it is
    negligible; from a 10 kΩ source it makes a pole near 3 GHz.
  - [R] If wanted, P's band order could put vdd between vin and vfbp (for example vref vfbn vcm vfbp vdd vin), leaving
    vin's only neighbor at a supply. That is a cheap change to one primitive.
- **vbp:** total 94.8 → 82.7 fF; its couplings to x and y fall from 0.9 to below 0.1 fF.
- **Pair balance**, total capacitance of each side:
  - outp / outn 70.2 / 76.0 (Δ −5.8, as in stage B). [R] That is about 0.5 % of the about 1.1 pF each output carries
    with s2d_cload and the 0.5 pF external load.
  - x / y 96.1 / 111.7 (Δ −15.5, stage B: −3.2). The fold nodes are low impedance; [R] the imbalance shifts the
    non-dominant pole of the two halves slightly and matters for high-frequency balance only.
  - xc / yc 134.4 / 93.3 (Δ +41, stage B: +29). [R] They do different jobs (xc feeds vcmfb, yc is dumped to vdd through
    CYC), so equal capacitance is not required. Only their DC levels should match, which is unaffected.
- **Enables (the only digital aggressors):** coupling to any sensitive net ≤ 2.6 fF (en_3v3 – outn), and en_3v3_b –
  vref 3.4 fF in stage B, 0 in B2. [R] They switch only at enable, so this is harmless in operation.

## Verdict

F's routing already does what a priority scheme would mainly buy: the one large coupling to the input (vbnc, 12 fF) is
gone, and the bias and enable lines stay small.

A stage B3 with explicit net classes would mainly help the fold pairs: routing x / y (and xc / yc) as mirror images
would bring Δ back towards stage B's −3 fF. [R] Electrically that is a high-frequency detail. The input coupling that
remains is a primitive matter (P's band order), not a routing one.
