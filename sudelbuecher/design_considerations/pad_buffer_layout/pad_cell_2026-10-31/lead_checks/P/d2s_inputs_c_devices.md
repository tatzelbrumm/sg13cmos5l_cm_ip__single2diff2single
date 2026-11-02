# d2s_inputs_c: flat devices, extracted (layout) vs reference

| model | D | G | S | B | L µm | layout n / ΣW µm | reference n / ΣW µm |
|---|---|---|---|---|---|---|---|
| sg13_hv_pmos | sa_A | vinp | y | sa_A | 1.0 | 1 / 20 | 0 / 0 |
| sg13_hv_pmos | sa_B | vref | y | sa_B | 1.0 | 1 / 20 | 0 / 0 |
| sg13_hv_pmos | sa_C1 | vref | y | sa_C1 | 1.0 | 1 / 20 | 0 / 0 |
| sg13_hv_pmos | sa_C2 | vref | y | sa_C2 | 1.0 | 1 / 20 | 0 / 0 |
| sg13_hv_pmos | sb_A | vref | x | sb_A | 1.0 | 1 / 20 | 0 / 0 |
| sg13_hv_pmos | sb_B | vinn | x | sb_B | 1.0 | 1 / 20 | 0 / 0 |
| sg13_hv_pmos | sb_C1 | vfb | x | sb_C1 | 1.0 | 1 / 20 | 0 / 0 |
| sg13_hv_pmos | sb_C2 | vfb | x | sb_C2 | 1.0 | 1 / 20 | 0 / 0 |
| sg13_hv_pmos | vdd | vdd | vdd | vdd | 1.0 | 1 / 40 | 4 / 40 |
| sg13_hv_pmos | x | vfb | sb_C1 | sb_C1 | 1.0 | 0 / 0 | 1 / 20 |
| sg13_hv_pmos | x | vfb | sb_C2 | sb_C2 | 1.0 | 0 / 0 | 1 / 20 |
| sg13_hv_pmos | x | vinn | sb_B | sb_B | 1.0 | 0 / 0 | 1 / 20 |
| sg13_hv_pmos | x | vref | sb_A | sb_A | 1.0 | 0 / 0 | 1 / 20 |
| sg13_hv_pmos | y | vinp | sa_A | sa_A | 1.0 | 0 / 0 | 1 / 20 |
| sg13_hv_pmos | y | vref | sa_B | sa_B | 1.0 | 0 / 0 | 1 / 20 |
| sg13_hv_pmos | y | vref | sa_C1 | sa_C1 | 1.0 | 0 / 0 | 1 / 20 |
| sg13_hv_pmos | y | vref | sa_C2 | sa_C2 | 1.0 | 0 / 0 | 1 / 20 |

| model | L µm | layout ΣW | reference ΣW |
|---|---|---|---|
| sg13_hv_pmos | 1.0 | 200 | 200 |
