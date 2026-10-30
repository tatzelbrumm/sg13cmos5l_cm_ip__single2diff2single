<!--
SPDX-FileCopyrightText: 2026 Christoph Maier
SPDX-License-Identifier: Apache-2.0
-->
# en_ctrl_3v3: fail-safe enable and select bits for the 3.3 V pad circuits

```
en_3v3   = en_1v2  AND  (vdd_1v2 present)  AND  (vdd_3v3 present)
sel*_3v3 = sel*_1v2, level-shifted (gated with en_3v3 in d2s_bias_sel_pd)
en_3v3_b = NOT en_3v3 (XIB), for d2s_mpdda_pd and d2s_bias_sel_pd
```

Ports (order): `vddh vddl vss en_1v2 sel0_1v2 sel1_1v2 vdd1v2_sense vdd3v3_sense en_3v3 sel0_3v3 sel1_3v3 en_3v3_b`.

| port | in the custom pad cell | in the slot fallback |
|---|---|---|
| vddh | iovdd (pad ring) | vdd_3v3 |
| vddl | core ring vdd (1.2 V, always on with the chip) | vdd_1v2 |
| vss | iovss | vss_3v3 |
| vdd1v2_sense / vdd3v3_sense | the slot's gated vdd_1v2 / vdd_3v3 (two slot-to-pad wires) | vdd_1v2 / vdd_3v3 |
| en_1v2, sel0_1v2, sel1_1v2 | harness `enable` and two `dig_in` bits, through the slot | same |

## How it works

- Three `ls_up_1v2_3v3` (`macros/ls_up_1v2_3v3`) shift en, sel0, sel1 to vddh.
- Two `pg_det` cells detect the slot supplies without needing a 1.2 V supply themselves: an hv NMOS (2u / 0.45u)
  with its gate on the sensed supply pulls `pg_b` low against a weak hv PMOS (0.3u / 50u). RD (0.3u / 100u) pulls a
  floating, gated-off sense input low. PU and RD are gated by the level-shifted enable: with en_1v2 = 0 the cell
  draws leakage only.
- `nor3_hv(en_ls_b, pg1_b, pg3_b)` gives en_3v3. With vddl = 0 the ls_up latches are undefined; pg_det of vdd_1v2
  then forces en_3v3 low either way (if en_ls_b is high the NOR is low; if it is low, PU is on and pg1_b is high).
- `XIB` (inv_hv, 1u / 0.45u) makes `en_3v3_b` from en_3v3, once for the pad (since 2026-10-25; before, d2s_mpdda_pd
  and d2s_bias_sel_pd each had their own inverter). It adds one gate to the en_3v3 load: nominal (tt, 27 C, 50 fF)
  enable delay 1.74 -> 1.79 ns, disable 2.56 -> 2.58 ns; the results below were simulated without it.
- `hv_logic` (`macros/hv_logic`) supplies inv_hv and nor3_hv. IHP's `sg13cmos5l_LevelUp` can replace ls_up_1v2_3v3
  in the pad cell (same topology, foundry layout in the IO GDS).

## Files

```
netlist/source/en_ctrl_3v3.spice              source netlist (pg_det, en_ctrl_3v3)
schematic/xschem/en_ctrl_3v3.sch/.sym, pg_det.sch/.sym   label-style sheets, box symbols (pins in port order)
verification/cace/en_ctrl_3v3.yaml            CACE suite, groups below
verification/cace/templates/en_ctrl_3v3_tb_{dc,tran_en,tran_pg}.sch
verification/cace/results/en_ctrl_3v3/        CSV and CACE summaries of the last `make sim-cace`
```

| group | what | runs |
|---|---|---:|
| truth_params | 8 input states at tt, 27 C, nominal: all on; en = 0; vdd_1v2 sense off; vdd_3v3 sense off; vdd_1v2 gated off (vddl = sense = 0, en still high); vdd_1v2 sense floating; vdd_3v3 sense floating; sel swapped | 8 |
| pvt_params | enabled, 5 corners x -40 / 125 C x (vddl, vddh) = (1.08, 3.0) / (1.32, 3.6) V | 20 |
| vddl_off_params | vdd_1v2 gated off with en_1v2 still high, same PVT | 20 |
| float_params | floating sense inputs at ss / ff x -40 / 125 C, low supply | 8 |
| tran_en_params | enable / disable delay, 50 fF on en_3v3, 5 corners x -40 / 125 C x low / high supply | 20 |
| tran_pg_params | supply loss (1 -> 0 V in 1 us) with en_1v2 held high: vdd_1v2 sense, vdd_3v3 sense, vdd_1v2 = vddl and sense together; 5 corners x -40 / 125 C, low supply | 30 |

The current and timing limits are proposals (worst case of these runs + ~30 %); the output-error limits (0.1 V)
are functional requirements.

## Results (CACE, schematic netlist, 2026-10-20)

All 106 runs pass. Cloud run with the IIC-OSIC-TOOLS 2026.09 pins (xschem `ddc7344`, ngspice-47, IHP-Open-PDK
iic-jku `c271a7e9`), CACE 2.13.0.

| quantity | limit (proposal) | worst | where |
|---|---:|---:|---|
| en_3v3 / sel_3v3 error, every DC state and corner | <= 0.1 V | 3 uV | truth, pvt, vddl_off, float |
| vddh current, enabled | <= 2.5 uA | 1.94 uA | ff, -40 C, 3.6 V |
| vdd_1v2 sense / vdd_3v3 sense current, enabled | <= 1.9 / 2.3 uA | 1.43 / 1.73 uA | ff, -40 C, high supply |
| vddl current, enabled | <= 50 nA | 39 nA | ff, 125 C |
| en_1v2 input current | <= 0.3 nA | 0.2 nA | ff, 125 C |
| enable delay (50 fF on en_3v3) | <= 4.8 ns | 3.7 ns (1.1 at best) | |
| disable delay | <= 7 ns | 5.4 ns (1.7 at best) | |
| supply loss -> en_3v3 low (supply ramps 1 -> 0 V in 1 us) | <= 1.2 us | 0.92 us | vdd_3v3 sense lost: 0.80-0.92 us; vdd_1v2 sense lost: 0.40-0.69 us (same with vddl ramping too) |
| en_3v3 after the loss | <= 0.1 V | 0.7 uV | |

Truth table at tt, 27 C: en_3v3 high only for "all on" and "sel swapped"; low for en = 0, either sense off, vdd_1v2
gated off, and either sense floating. Full table: `make spec-table`. Plots: `make sim-cace` (not copied to this
folder; only CSV and the CACE summaries are).

**Finding, vddl_off_params:** with vddl = 0 and en_1v2 still at 1.08 V (the harness enable alive while the ls_up
input inverters are unpowered), en_3v3 is correctly low at every corner, but at ss, -40 C, low supply the ls_up
latch of `en_ls` settles in a ratioed state and draws 152 uA from vddh (0.33-0.97 uA elsewhere). In the pad cell
vddl is the always-on core ring, so this state does not occur; in the slot fallback en_1v2 comes from the same
gated vdd_1v2 domain and falls with it. Left as report-only (`any`).

**Enabled-state current:** the two sense inputs draw 0.4-1.7 uA each from the slot's vdd_1v2 / vdd_3v3 (RD), and
vddh 0.7-1.9 uA (the pg_det pull-ups). Disabled by en_1v2 = 0 the cell draws pA.

Not done: layout, extraction, Monte Carlo, and the transient of a slot vdd_1v2 that floats (rather than ramps) after
its power switch opens.
