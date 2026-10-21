<!--
SPDX-FileCopyrightText: 2026 Christoph Maier
SPDX-License-Identifier: Apache-2.0
-->
# ls_up_1v2_3v3: 1.2 V -> 3.3 V level shifter (non-inverting)

Moved here on 2026-10-20 from `chipalooza2/levelshifters/ls_pair` (built 2026-10-03/04), laid out like the other
macros of this repository.

| | |
|---|---|
| ports (order) | `vss vddl vddh out in` |
| devices | 2 LV (input inverter on vddl) + 6 HV (cross-coupled latch, output inverter on vddh) |
| source | netlist of `SAR_ADC_IHP` `level_shifter_1v2_to_3v3` (Apache-2.0, Arjun Ananth et al., github.com/arjun2000ananth/SAR_ADC_IHP); see `LICENSE` in `chipalooza2/levelshifters/ls_pair` |
| used by | `macros/en_ctrl_3v3` (three instances: en, sel0, sel1) |

**Drop-in alternative for the pad cells:** IHP's `sg13cmos5l_LevelUp` (`o i iovdd vdd vss`, in `sg13cmos5l_io`) has the
same topology (LV inverter on the core vdd, cross-coupled hv latch on iovdd, hv output inverter) and ships with
foundry layout inside the IO cells' GDS. It has no xschem symbol in the PDK.

**Undefined with vddl = 0.** With the input inverter unpowered, neither latch pull-down is driven and the output is
undefined. `en_ctrl_3v3` therefore gates its outputs with a vdd_1v2 presence detector that needs no 1.2 V supply.

## Files

```
netlist/source/ls_up_1v2_3v3.spice     source subcircuit (xschem netlist of the original sheet)
schematic/xschem/ls_up_1v2_3v3.sch/.sym  sheet (hand-edited in ls_pair) and symbol (buffer, adapted from IHP buf_1)
testbenches/xschem/tb_ls_up.sch          interactive testbench (ngspice); tb_ls_loop.sch: up + ls_dn_3v3_1v2 loopback
verification/cace/ls_up_1v2_3v3.yaml     CACE: pvt_params (135 runs), tr_params (7), cload_params (4)
verification/cace/results/ls_up_1v2_3v3/ CSV, plots and CACE summaries of the last `make sim-cace`
```

```sh
make sim-cace                        # all groups; results/ls_up_1v2_3v3/
make sim-cace CACE_GROUPS=tr_params  # one group
make spec-table                      # limit, worst case and verdict per quantity
```

## Results (CACE, schematic netlist, 2026-10-20)

Cloud run with the IIC-OSIC-TOOLS 2026.09 pins (xschem `ddc7344`, ngspice-47, OpenVAF `5ed9e63`, IHP-Open-PDK
iic-jku `c271a7e9`), CACE 2.13.0. All 146 runs pass. PVT: tt/ss/ff/sf/fs x -40/27/125 C x VDDL 1.08/1.2/1.32 V x
VDDH 3.0/3.3/3.6 V, input transition 100 ps, 20 fF load.

| quantity | limit (proposal) | worst over PVT |
|---|---:|---:|
| delay, input rising | <= 10 ns | 6.97 ns |
| delay, input falling | <= 14 ns | 10.4 ns |
| output high | >= 2.85 V | 3.0 V |
| output low | <= 0.05 V | 0.7 uV |
| Iq VDDL (input low / high) | <= 25 nA | 4.1 / 17.6 nA |
| Iq VDDH (input low / high) | <= 4 nA | 2.7 / 2.3 nA |
| charge from VDDH per edge (rise / fall) | <= 3 / 4 pC | 2.34 / 3.26 pC |
| peak current from VDDH (rise / fall) | <= 2.2 / 1.2 mA | 1.68 / 0.87 mA |
| energy per cycle | <= 26 pJ | 20.2 pJ |

At tt, 27 C, nominal supplies: 0.48 ns rise / 0.68 ns fall (`tb_ls_up`), 0.56 / 1.89 ns through the loopback with
ls_dn (`tb_ls_loop`). The worst case is the sf, -40 C, VDDL 1.08 V corner, where the cell is at the edge of its
working range. The limits are proposals (worst case + ~25-40 %), unchanged from ls_pair; the new numbers agree with
the 2026-10-04 run (CACE 2.11, ngspice 42, older PDK models) to within 1 %. Full table: `make spec-table`.

The plots (`*.png`) in `results/ls_up_1v2_3v3/` are still those of the 2026-10-04 ls_pair run (the cloud-generated ones were
not copied, to keep image files off the round trip); the CSV and summaries are from 2026-10-20. `make sim-cace`
regenerates all of them.

Not done: layout, extraction, Monte Carlo, behaviour with one supply off (see en_ctrl_3v3), ESD.
