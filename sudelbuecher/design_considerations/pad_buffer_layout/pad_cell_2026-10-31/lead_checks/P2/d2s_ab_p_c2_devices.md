# d2s_ab_p_c2: flat devices, extracted (layout) vs reference

| model | D | G | S | B | L µm | layout n / ΣW µm | reference n / ΣW µm |
|---|---|---|---|---|---|---|---|
| sg13_hv_pmos | a | vabp | b | vdd | 0.6 | 1 / 6.66 | 0 / 0 |
| sg13_hv_pmos | b | vabp | a | vdd | 0.6 | 0 / 0 | 1 / 6.66 |
| sg13_hv_pmos | l1 | vabp | l2 | vdd | 0.6 | 0 / 0 | 1 / 6.66 |
| sg13_hv_pmos | l2 | vabp | l1 | vdd | 0.6 | 1 / 6.66 | 0 / 0 |
| sg13_hv_pmos | vabp | vabp | dabp | vdd | 0.6 | 1 / 6.66 | 1 / 6.66 |
| sg13_hv_pmos | vdd | vdd | vdd | vdd | 0.6 | 1 / 13.32 | 2 / 13.32 |

| model | L µm | layout ΣW | reference ΣW |
|---|---|---|---|
| sg13_hv_pmos | 0.6 | 33.3 | 33.3 |
