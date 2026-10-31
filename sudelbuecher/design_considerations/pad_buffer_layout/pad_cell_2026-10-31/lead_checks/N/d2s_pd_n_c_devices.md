# d2s_pd_n_c: flat devices, extracted (layout) vs reference

| model | D | G | S | B | L µm | layout n / ΣW µm | reference n / ΣW µm |
|---|---|---|---|---|---|---|---|
| sg13_hv_nmos | b | en_3v3_b | vsso | vss | 0.45 | 0 / 0 | 1 / 1 |
| sg13_hv_nmos | vabn | en_3v3_b | vss | vss | 0.45 | 0 / 0 | 1 / 1 |
| sg13_hv_nmos | vss | en_3v3_b | vabn | vss | 0.45 | 1 / 1 | 0 / 0 |
| sg13_hv_nmos | vsso | en_3v3_b | b | vss | 0.45 | 1 / 1 | 0 / 0 |

| model | L µm | layout ΣW | reference ΣW |
|---|---|---|---|
| sg13_hv_nmos | 0.45 | 2 | 2 |
