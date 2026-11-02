# d2s_loads_c2: flat devices, extracted (layout) vs reference

| model | D | G | S | B | L µm | layout n / ΣW µm | reference n / ΣW µm |
|---|---|---|---|---|---|---|---|
| sg13_hv_pmos | pl | l2 | vdd | vdd | 4.0 | 0 / 0 | 4 / 24 |
| sg13_hv_pmos | pr | l2 | vdd | vdd | 4.0 | 0 / 0 | 4 / 24 |
| sg13_hv_pmos | vdd | l2 | pl | vdd | 4.0 | 1 / 24 | 0 / 0 |
| sg13_hv_pmos | vdd | l2 | pr | vdd | 4.0 | 1 / 24 | 0 / 0 |
| sg13_hv_pmos | vdd | l2 | vdd | vdd | 4.0 | 1 / 4 | 4 / 4 |

| model | L µm | layout ΣW | reference ΣW |
|---|---|---|---|
| sg13_hv_pmos | 4.0 | 52 | 52 |
