
## static

| state | I(bus0) min .. max | I(bus1) min .. max | en_oa / en_bg / read-back as expected | worst point |
|---|---|---|---|---|
| all_off (dig_in 0000, en 1, 3v3 1, 1v2 1) | 1.94e-12 .. 8.47e-11 A | 1.94e-12 .. 1.7e-10 A | yes | ff 125 C high |
| tg_on_cores_off (dig_in 0011, en 1, 3v3 1, 1v2 1) | 1.94e-11 .. 2.61e-10 A | 2.76e-11 .. 2.28e-09 A | yes | ff 125 C high |
| oa_on (dig_in 1010, en 1, 3v3 1, 1v2 1) | 4.99e-06 .. 7.06e-06 A | 1.94e-12 .. 1.7e-10 A | yes | ff 125 C high |
| bg_on (dig_in 0101, en 1, 3v3 1, 1v2 1) | 1.94e-12 .. 8.47e-11 A | 4.88e-06 .. 6.37e-06 A | yes | ff 27 C high |
| both_on (dig_in 1111, en 1, 3v3 1, 1v2 1) | 4.99e-06 .. 7.06e-06 A | 4.88e-06 .. 6.37e-06 A | yes | ff 125 C high |
| cores_on_tg_off (dig_in 1100, en 1, 3v3 1, 1v2 1) | 2.03e-12 .. 1.9e-10 A | 2.03e-12 .. 1.9e-10 A | yes | ff 125 C high |
| enable_low (dig_in 1111, en 0, 3v3 1, 1v2 1) | 1.94e-12 .. 8.47e-11 A | 1.94e-12 .. 1.7e-10 A | yes | ff 125 C high |
| vdd1v2_off (dig_in 1111, en 1, 3v3 1, 1v2 0) | 1.94e-12 .. 8.47e-11 A | 1.94e-12 .. 1.7e-10 A | yes | ff 125 C high |
| vdd1v2_off_1uA (dig_in 1111, en 1, 3v3 1, 1v2 0) | 1.94e-12 .. 8.47e-11 A | 1.94e-12 .. 1.7e-10 A | yes | ff 125 C high |
| vdd3v3_off (dig_in 1111, en 1, 3v3 0, 1v2 1) | -9.29e-09 .. -1.51e-10 A | -8.61e-08 .. -3.89e-09 A | yes | ff 125 C nom |
| both_supplies_off (dig_in 1111, en 1, 3v3 0, 1v2 0) | -6.33e-10 .. -9.34e-12 A | -1.52e-09 .. -1.53e-11 A | yes | ff 125 C high |

tie-lows dig_out[4] / dig_out[11], vdd_1v2 on: max 0 / 0 V (into 1 Tohm)
supply currents, all_off: I(vdd_3v3) 1.22e-10 .. 6.89e-09 A, I(vdd_1v2) 2.91e-06 .. 5.42e-06 A
supply currents, both_on: I(vdd_3v3) 2.46e-05 .. 3.03e-05 A, I(vdd_1v2) 2.91e-06 .. 5.42e-06 A
floating vdd_1v2 when gated off: 0 .. 0 V
floating vdd_3v3, vdd3v3_off: 0.635 .. 0.665 V
floating vdd_3v3, both_supplies_off: 0.559 .. 0.608 V

| corner | T (C) | I_OA (uA) low / nom / high supply | I_BG (uA) low / nom / high |
|---|---|---|---|
| tt | 27 | - / 4.992 / 4.994 | - / 4.958 / 4.965 |
| tt | 125 | - / 6.662 / 6.664 | - / 4.883 / 4.891 |
| ff | 27 | - / 5.324 / 5.326 | - / 6.360 / 6.369 |
| ff | 125 | - / 7.054 / 7.056 | - / 6.304 / 6.315 |

logic-level failures: 0
