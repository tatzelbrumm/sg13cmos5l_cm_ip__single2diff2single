# sinks_6x6_c: flat devices, extracted (layout) vs reference

| model | D | G | S | B | L µm | layout n / ΣW µm | reference n / ΣW µm |
|---|---|---|---|---|---|---|---|
| sg13_hv_nmos | vbn | vbn | vss | vss | 6.0 | 0 / 0 | 1 / 6 |
| sg13_hv_nmos | vss | vbn | vbn | vss | 6.0 | 1 / 6 | 0 / 0 |
| sg13_hv_nmos | vss | vbn | vss | vss | 6.0 | 1 / 6 | 3 / 6 |
| sg13_hv_nmos | vss | vbn | y | vss | 6.0 | 1 / 36 | 0 / 0 |
| sg13_hv_nmos | x | vbn | vss | vss | 6.0 | 1 / 36 | 6 / 36 |
| sg13_hv_nmos | y | vbn | vss | vss | 6.0 | 0 / 0 | 6 / 36 |

| model | L µm | layout ΣW | reference ΣW |
|---|---|---|---|
| sg13_hv_nmos | 6.0 | 84 | 84 |
