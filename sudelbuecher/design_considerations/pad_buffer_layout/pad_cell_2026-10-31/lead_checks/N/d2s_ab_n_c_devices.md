# d2s_ab_n_c: flat devices, extracted (layout) vs reference

| model | D | G | S | B | L µm | layout n / ΣW µm | reference n / ΣW µm |
|---|---|---|---|---|---|---|---|
| sg13_hv_nmos | a | vabn | b | vss | 1.0 | 0 / 0 | 1 / 4.4 |
| sg13_hv_nmos | b | vabn | a | vss | 1.0 | 1 / 4.4 | 0 / 0 |
| sg13_hv_nmos | l1 | vabn | l2 | vss | 1.0 | 1 / 4.4 | 0 / 0 |
| sg13_hv_nmos | l2 | vabn | l1 | vss | 1.0 | 0 / 0 | 1 / 4.4 |
| sg13_hv_nmos | vabn | vabn | dabn | vss | 1.0 | 1 / 4.4 | 1 / 4.4 |

| model | L µm | layout ΣW | reference ΣW |
|---|---|---|---|
| sg13_hv_nmos | 1.0 | 13.2 | 13.2 |
