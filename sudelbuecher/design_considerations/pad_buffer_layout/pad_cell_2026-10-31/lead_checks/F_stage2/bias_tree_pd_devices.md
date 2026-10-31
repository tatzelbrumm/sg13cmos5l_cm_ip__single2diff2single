# bias_tree_pd: flat devices, extracted (layout) vs reference

| model | D | G | S | B | L µm | layout n / ΣW µm | reference n / ΣW µm |
|---|---|---|---|---|---|---|---|
| sg13_hv_nmos | iref | en_3v3 | ni | vss | 0.45 | 1 / 1 | 1 / 1 |
| sg13_hv_nmos | ni | en_3v3_b | vss | vss | 0.45 | 1 / 1 | 1 / 1 |
| sg13_hv_nmos | ni | ni | vss | vss | 6.0 | 0 / 0 | 1 / 6 |
| sg13_hv_nmos | vabp | ni | vss | vss | 6.0 | 0 / 0 | 1 / 6 |
| sg13_hv_nmos | vbp | ni | vss | vss | 6.0 | 0 / 0 | 1 / 6 |
| sg13_hv_nmos | vbpc | ni | vss | vss | 6.0 | 0 / 0 | 1 / 2.4 |
| sg13_hv_nmos | vss | ni | ni | vss | 6.0 | 1 / 6 | 0 / 0 |
| sg13_hv_nmos | vss | ni | vabp | vss | 6.0 | 1 / 6 | 0 / 0 |
| sg13_hv_nmos | vss | ni | vbp | vss | 6.0 | 1 / 6 | 0 / 0 |
| sg13_hv_nmos | vss | ni | vbpc | vss | 6.0 | 1 / 2.4 | 0 / 0 |
| sg13_hv_nmos | vss | ni | vss | vss | 6.0 | 1 / 2.4 | 1 / 2.4 |
| sg13_hv_pmos | iref | en_3v3_b | ni | vdd | 0.45 | 1 / 1 | 1 / 1 |
| sg13_hv_pmos | vabn | vbp | vdd | vdd | 6.0 | 0 / 0 | 1 / 5 |
| sg13_hv_pmos | vbn | vbp | vdd | vdd | 6.0 | 0 / 0 | 1 / 5 |
| sg13_hv_pmos | vbnc | vbp | vdd | vdd | 6.0 | 0 / 0 | 1 / 2 |
| sg13_hv_pmos | vdd | vbp | vabn | vdd | 6.0 | 1 / 5 | 0 / 0 |
| sg13_hv_pmos | vdd | vbp | vbn | vdd | 6.0 | 1 / 5 | 0 / 0 |
| sg13_hv_pmos | vdd | vbp | vbnc | vdd | 6.0 | 1 / 2 | 0 / 0 |
| sg13_hv_pmos | vdd | vbp | vdd | vdd | 6.0 | 1 / 2 | 1 / 2 |

| model | L µm | layout ΣW | reference ΣW |
|---|---|---|---|
| sg13_hv_nmos | 0.45 | 2 | 2 |
| sg13_hv_nmos | 6.0 | 22.8 | 22.8 |
| sg13_hv_pmos | 0.45 | 1 | 1 |
| sg13_hv_pmos | 6.0 | 14 | 14 |
