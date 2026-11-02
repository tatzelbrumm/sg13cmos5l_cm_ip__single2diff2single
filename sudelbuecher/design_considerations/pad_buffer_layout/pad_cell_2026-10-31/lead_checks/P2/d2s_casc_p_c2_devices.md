# d2s_casc_p_c2: flat devices, extracted (layout) vs reference

| model | D | G | S | B | L µm | layout n / ΣW µm | reference n / ΣW µm |
|---|---|---|---|---|---|---|---|
| sg13_hv_pmos | a | vbpc | pr | vdd | 3.0 | 0 / 0 | 2 / 30 |
| sg13_hv_pmos | l2 | vbpc | pl | vdd | 3.0 | 0 / 0 | 2 / 30 |
| sg13_hv_pmos | pl | vbpc | l2 | vdd | 3.0 | 1 / 30 | 0 / 0 |
| sg13_hv_pmos | pr | vbpc | a | vdd | 3.0 | 1 / 30 | 0 / 0 |
| sg13_hv_pmos | vbpc | vbpc | vdd | vdd | 4.0 | 1 / 1 | 1 / 1 |
| sg13_hv_pmos | vdd | vbpc | vdd | vdd | 4.0 | 1 / 1 | 1 / 1 |

| model | L µm | layout ΣW | reference ΣW |
|---|---|---|---|
| sg13_hv_pmos | 3.0 | 60 | 60 |
| sg13_hv_pmos | 4.0 | 2 | 2 |
