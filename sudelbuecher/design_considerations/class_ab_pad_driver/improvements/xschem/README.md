<!--
SPDX-FileCopyrightText: 2026 Christoph Maier
SPDX-License-Identifier: Apache-2.0
-->
# xschem schematics of the class-AB pad driver revision

These are drafts, drawn from `../sim/*.spice` for hand editing.

Every sheet outlines its functional blocks with magenta dashed boxes tagged [1] to [9]. A number
means the same block on every sheet, and the legend under each sheet repeats the short
description.

`check_xschem.py` netlists every sheet with xschem and compares it device by device with the
`.spice` sources. Run it after any hand edit (it needs xschem and `$PDK_ROOT`).

## Files

| sheet | contents | pins |
|---|---|---|
| `d2s_mpdda_bias_flat` | the whole proposal on one sheet, all at transistor level: bias [8], DDA units [1], fold [2], mirror [3], class-AB control [4], [5], output [6], Miller capacitors [7] | vdd vss vinp vinn vref vout vfb |
| `d2s_mpdda_flat` | `d2s_mpdda` with the four units at transistor level | as `d2s_miller` (13) |
| `d2s_mpdda` | the proposed driver, with the units as `unit_r2` boxes | as `d2s_miller` (13) |
| `d2s_mpdda_biased` | CACE fixture: `d2s_mpdda` and `d2s_bias_lp` as two boxes, bias nets as pins, wired like `d2s_miller_biased` | 13 |
| `d2s_bias_lp` | the bias network [8] | vdd, vss, 6 bias outputs |
| `unit_r2` | one DDA unit | x y gp gn vdd vss vbp |
| `d2s_lc2`, `d2s_lc2_nc` | case (b): output devices in the slot, load-compensated, with and without output cascodes | 13 |
| `unit_r`, `unit_t`, `unit_w`, `unit_q` | the unit alternatives of the proposal, Section II | 7 |

In the flat sheets, each unit's devices and internal nets carry the unit's name: `Ta_A`, `Tb_A`,
`R_A`, `Ma_A`, `Mb_A`, `sa_A`, `sb_A`, and likewise for B, C1 and C2.

## Blocks of `d2s_mpdda`

Voltages and currents are the tt operating point (`../sim/results_improvements.txt`, proposal
Section IV).

| | block | devices | nets | function |
|---|---|---|---|---|
| [1] | DDA units A, B, C1, C2 | per unit: tails Ta, Tb 5u/6u (gate vbp); rhigh R 0.5u/50.6u between the sources sa, sb; pair Ma, Mb 20u/1u ng=2 | inputs gp, gn; outputs y (Ma drain) and x (Mb drain) | turns gp − gn into a current difference between y and x; 2 × 5 µA per unit |
| [2] | fold | sinks SX, SY 36u/6u (gate vbn); cascodes CX, CY 30u/3u (gate vbnc) | x, y (≈ 0.37 V) up to l1, b | each sink takes 30 µA: 20 µA from the four units and 10 µA from its cascode branch |
| [3] | cascoded PMOS mirror | PL, PR 24u/4u; PCL, PCR 30u/3u (gate vbpc) | input l2 (the mirror gates), pl, pr; output into a | copies the left branch (10 µA) into the right one |
| [4] | class-AB control | ABP 6.66u/0.6u (gate vabp), ABN 4.4u/1u (gate vabn) | between a (≈ 2.6 V) and b (≈ 0.7 V) | holds a − b; the right branch's 10 µA splits 5.2 / 4.8 µA; together with [8] it sets the output quiescent current |
| [5] | copy of [4] | FPL, FNL, same sizes | between l2 and l1 | gives the left branch the same element as the right one (FPL carries only ~1 nA, an open item) |
| [6] | output devices | OP 546.12u/0.6u ng=82; ON 290.4u/1u ng=66 | gates a, b; drains vout | the pad frames, which double as ESD clamps in case (a); 212 µA quiescent |
| [7] | Miller capacitors | CMA, CMB: hv PMOS 16u × 16u in accumulation | CMA: gate a, S/D/well vout; CMB: gate vout, S/D/well b | compensation without BEOL capacitors |

**Signal path.** Every unit has vref on one input:

- vinp sits on the gp side of unit A.
- vinn sits on the gn side of unit B.
- vfb sits on the gn side of C1 and C2.

A rising vinp makes Ma_A carry less, so less current reaches y. CY then carries more and pulls b
down. a follows, because [4] holds the two apart. OP turns on harder and vout rises. A rising vfb
acts on the x side instead, through CX, the mirror [3] and node a, with the opposite sign. With
vfb tied to vout, the loop settles where f(vinp − vref) + f(vref − vinn) = 2 f(vfb − vref), that
is, vout − vref = (vinp − vinn)/2 for any odd, monotonic unit law f (proposal, Section II).

## Bias [8] (`d2s_bias_lp`)

Ideal reference currents flow into diode-connected devices:

| net | reference | diode | feeds |
|---|---|---|---|
| vbp | IBP 5 µA | BP 5u/6u | the unit tails Ta, Tb (5u/6u, 1:1, 5 µA each) |
| vbn | IBN 5 µA | BN 6u/6u | the sinks SX, SY (36u/6u, 6:1, 30 µA each) |
| vbpc | IBPC 2 µA | BPC 1u/4u | the mirror cascodes PCL, PCR |
| vbnc | IBNC 2 µA | BNC 1u/8u | the fold cascodes CX, CY |
| vabp | IABP 5 µA | RP2 (size of ABP) on RP1 (2 × ABP) | ABP, FPL |
| vabn | IABN 5 µA | RN2 (size of ABN) on RN1 (2 × ABN) | ABN, FNL |

From vdd down to vabp, V_SG(OP) + V_SG(ABP) = V_SG(RP1) + V_SG(RP2). RP2 has ABP's size and
about ABP's current, so OP's V_SG follows RP1's. OP is 41 × RP1. The N side closes the same loop
through ON, ABN, RN1 and RN2, with ON = 33 × RN1. The two loops together settle at 212 µA.

## `d2s_lc2`, `d2s_lc2_nc`

[1] to [5] are as in `d2s_mpdda`. There is no Miller capacitor; the load capacitance is the
dominant pole.

- [6] OP 273.06u/0.6u ng=41 and ON 145.2u/1u ng=33: half frames in the slot, not the pad's clamps.
- [7] Output cascodes OPC, ONC with gates at vref (`d2s_lc2` only).
- [9] Diode replicas DP 6.66u/0.6u on a and DN 3.8u/1u on b, 1/41 and 1/38 of OP and ON. They
  make the gate nodes low-impedance.

## Unit alternatives

`unit_r` is `unit_r2` at the first version's sizing (tails 10u/2u, rhigh 36.4u). The other three
replace the resistor:

- `unit_t`: a triode hv PMOS.
- `unit_w`: well (bulk) inputs with the gates at vss.
- `unit_q`: no degeneration at all.

Only the rhigh units qualify for the matched-pair DDA. The others' output depends on the
absolute source voltage, not on gp − gn alone (proposal, Section II).
