
## static

| state | I(bus0) min .. max | I(bus1) min .. max | en_oa / en_bg / read-back as expected | worst point |
|---|---|---|---|---|
| all_off (dig_in 0000, en 1, 3v3 1, 1v2 1) | 6.04e-14 .. 6.04e-14 A | 1.19e-13 .. 1.19e-13 A | yes | tt 27 C nom |
| tg_on_cores_off (dig_in 0011, en 1, 3v3 1, 1v2 1) | 1.69e-13 .. 1.69e-13 A | 1.88e-12 .. 1.88e-12 A | yes | tt 27 C nom |
| oa_on (dig_in 1010, en 1, 3v3 1, 1v2 1) | 4.99e-06 .. 4.99e-06 A | 1.19e-13 .. 1.19e-13 A | yes | tt 27 C nom |
| bg_on (dig_in 0101, en 1, 3v3 1, 1v2 1) | 6.04e-14 .. 6.04e-14 A | 4.96e-06 .. 4.96e-06 A | yes | tt 27 C nom |
| both_on (dig_in 1111, en 1, 3v3 1, 1v2 1) | 4.99e-06 .. 4.99e-06 A | 4.96e-06 .. 4.96e-06 A | yes | tt 27 C nom |
| cores_on_tg_off (dig_in 1100, en 1, 3v3 1, 1v2 1) | 1.3e-13 .. 1.3e-13 A | 1.3e-13 .. 1.3e-13 A | yes | tt 27 C nom |
| enable_low (dig_in 1111, en 0, 3v3 1, 1v2 1) | 6.04e-14 .. 6.04e-14 A | 1.19e-13 .. 1.19e-13 A | yes | tt 27 C nom |
| vdd1v2_off (dig_in 1111, en 1, 3v3 1, 1v2 0) | 6.04e-14 .. 6.04e-14 A | 1.19e-13 .. 1.19e-13 A | yes | tt 27 C nom |
| vdd1v2_off_1uA (dig_in 1111, en 1, 3v3 1, 1v2 0) | 6.04e-14 .. 6.04e-14 A | 1.19e-13 .. 1.19e-13 A | yes | tt 27 C nom |
| vdd3v3_off (dig_in 1111, en 1, 3v3 0, 1v2 1) | -1.94e-10 .. -1.94e-10 A | -3.85e-09 .. -3.85e-09 A | yes | tt 27 C nom |
| both_supplies_off (dig_in 1111, en 1, 3v3 0, 1v2 0) | -4.85e-13 .. -4.85e-13 A | -1.26e-12 .. -1.26e-12 A | yes | tt 27 C nom |

tie-lows dig_out[4] / dig_out[11], vdd_1v2 on: max 0 / 0 V (into 1 Tohm)
supply currents, all_off: I(vdd_3v3) 1.27e-11 .. 1.27e-11 A, I(vdd_1v2) 4.1e-06 .. 4.1e-06 A
supply currents, both_on: I(vdd_3v3) 2.46e-05 .. 2.46e-05 A, I(vdd_1v2) 4.1e-06 .. 4.1e-06 A
floating vdd_1v2 when gated off: 0 .. 0 V
floating vdd_3v3, vdd3v3_off: 0.635 .. 0.635 V
floating vdd_3v3, both_supplies_off: 0.621 .. 0.621 V

| corner | T (C) | I_OA (uA) low / nom / high supply | I_BG (uA) low / nom / high |
|---|---|---|---|
| tt | 27 | - / 4.992 / - | - / 4.958 / - |

logic-level failures: 0
