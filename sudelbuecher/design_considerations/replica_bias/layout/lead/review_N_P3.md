<!--
SPDX-FileCopyrightText: 2026 Christoph Maier
SPDX-License-Identifier: Apache-2.0
-->
# Lead's review of N (NMOS rows, capacitors) and P3 (rb_avg redo), 2026-11-07

Claude, lead of C4. [M] = measured, [R] = reasoning.

## Netlists against the circuit [M]

`cdl_vs_circuit.py` compares the CDLs of P (without its rb_avg), P3 and N with the circuit netlists of pad_ref_rb
(bias_tree_rb, vcm_rb, vref_s2d_rb, bypass_rb with ncm = 4, ncr = 8). It matches the devices as a multiset of model,
{d, s}, g, b, W, L, ng, independent of the agents' names. Output: `cdl_vs_circuit_P_P3_N.txt`.

- 42 of 42 active devices are drawn, with the right nets and sizes.
- One extra: a 9th 12u/12u on vref. It is rb_cload's second capacitor slot (the pad's CLN), next to the full
  bypass_rb array of 8. N flagged it as an open question.
- 20 dummies are drawn. Each has S = D = B on one rail: vdd, vss, or for rb_avg the well's own net (gh, m). Their
  gates are the row's gate net.
- My first version of this check (row 59) took every MD... device for a mismatch: the regex had stripped the M. The
  version here classifies by name and compares by multiset.

## Pictures [R]

- rb_avg (P3): one NWell per bulk net. SU is between DU0 / DU1 in well gh; DL0 SL1 SL2 DL1 are in well m. The gate
  strip is continuous and contacted only by end columns, and the tie is open on the drain side. Accepted pending
  Christoph's two questions (translated rows; U-ring or strip).
- rb_tree_n: [TGN] SH2 SF NBP SY | NI SH1 D D [TDN], symmetric in widths (2.4 2 2.4 6 | 6 2.4 2 2.4).
- rb_casc: 5 active 15/3 fingers in 8 slots, so 3 spare 15/3 dummies. It is the least compact row: 159 µm² of extra
  gate on vbnc.
- rb_mirror, rb_cload, bypass_rb: as the pad's rows; bypass_rb 3 × 4, limited to 3 on the short side by LU.b.

## Open (Christoph)

From N: casc 8 or 6 slots; rb_cload's CLN slot; tree dummy position; extra end dummies. From P3: translated rows;
ring or strip. Backannotation of the dummies waits for these answers, since the casc and tree dummies depend on them.
