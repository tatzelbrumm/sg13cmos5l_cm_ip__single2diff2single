<!--
SPDX-FileCopyrightText: 2026 Christoph Maier
SPDX-License-Identifier: Apache-2.0
-->
# ls_dn_3v3_1v2: 3.3 V -> 1.2 V level shifter (inverting)

Moved here on 2026-10-20 from `chipalooza2/levelshifters/ls_pair` (built 2026-10-03/04), laid out like the other
macros of this repository.

| | |
|---|---|
| ports (order) | `vss vddl out in` (no vddh: the 3.3 V domain only supplies the input signal) |
| devices | 2 HV MOS: an hv inverter on VDDL |
| source | the `MMP8` / `MMN9` pattern of `bidir-level-shifter` `bidir_channel` (github.com/rcyaon/bidir-level-shifter) |

**Inverting.** For a non-inverting down-shift follow it with an LV inverter (e.g. `sg13cmos5l_inv_1`) on VDDL.
The switching threshold is low (about 0.6 V at the input), so rising and falling delays differ by 1-2.5 ns: expect
duty-cycle distortion on clock-like signals. Its HV gates see the full input swing (3.0-3.6 V); check that against
IHP's gate-oxide rating for the supply tolerance.

## Files

```
netlist/source/ls_dn_3v3_1v2.spice     source subcircuit
schematic/xschem/ls_dn_3v3_1v2.sch/.sym  sheet and symbol (inverter with bubble, adapted from IHP inv_1)
testbenches/xschem/tb_ls_dn.sch          interactive testbench (ngspice); the loopback is in ../ls_up_1v2_3v3
verification/cace/ls_dn_3v3_1v2.yaml     CACE: pvt_params (135 runs), tr_params (7), cload_params (4)
verification/cace/results/ls_dn_3v3_1v2/ CSV and CACE summaries of the last `make sim-cace`
```

```sh
make sim-cace      # all groups; results/ls_dn_3v3_1v2/
make spec-table    # limit, worst case and verdict per quantity
```

## Results (CACE, schematic netlist, 2026-10-20)

Cloud run with the IIC-OSIC-TOOLS 2026.09 pins (xschem `ddc7344`, ngspice-47, OpenVAF `5ed9e63`, IHP-Open-PDK
iic-jku `c271a7e9`), CACE 2.13.0. All 146 runs pass. PVT: tt/ss/ff/sf/fs x -40/27/125 C x VDDL 1.08/1.2/1.32 V x
input high level (VDDH) 3.0/3.3/3.6 V, 100 ps input edges, 20 fF load.

| quantity | limit (proposal) | worst over PVT |
|---|---:|---:|
| delay, input rising (out falls) | <= 0.15 ns | 0.097 ns |
| delay, input falling (out rises) | <= 3.5 ns | 2.56 ns |
| output high | >= 1 V | 1.08 V |
| output low | <= 0.05 V | 23 nV |
| Iq VDDL (input low / high) | <= 100 pA | 74 / 10 pA |
| charge from VDDL per edge (rise / fall) | <= 300 / 50 fC | -3.0 / 36 fC |
| peak current from VDDL (rise / fall) | <= 110 uA | 88 / 77 uA |
| energy per cycle | <= 55 fJ | 41.3 fJ |

At tt, 27 C, nominal supplies, 500 ps input edges (`tb_ls_dn`): out falls 0.07 ns after in rises, rises 1.25 ns after in falls.
The limits are proposals (worst case + ~25-40 %), unchanged from ls_pair; the new numbers agree with the
2026-10-04 run (CACE 2.11, ngspice 42, older PDK models) to within 2 %. Full table: `make spec-table`.

The plots (`*.png`) in `results/ls_dn_3v3_1v2/` are still those of the 2026-10-04 ls_pair run (the cloud-generated ones were
not copied, to keep image files off the round trip); the CSV and summaries are from 2026-10-20. `make sim-cace`
regenerates all of them.

Not done: layout (no layout of this plain hv-inverter-on-VDDL structure was found), extraction, Monte Carlo, ESD.
