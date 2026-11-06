
## static

| state | I(bus0) min .. max | I(bus1) min .. max | en_oa / en_bg / read-back as expected | worst point |
|---|---|---|---|---|
| all_off (dig_in 0000, en 1, 3v3 1, 1v2 1) | 1.94e-12 .. 6.45e-11 A | 1.94e-12 .. 1.57e-10 A | yes | ff 125 C high |
| tg_on_cores_off (dig_in 0011, en 1, 3v3 1, 1v2 1) | 2.14e-11 .. 2.9e-10 A | 2.95e-11 .. 2.31e-09 A | yes | ff 125 C high |
| oa_on (dig_in 1010, en 1, 3v3 1, 1v2 1) | 4.99e-06 .. 7.06e-06 A | 1.94e-12 .. 1.57e-10 A | yes | ff 125 C high |
| bg_on (dig_in 0101, en 1, 3v3 1, 1v2 1) | 1.94e-12 .. 6.31e-11 A | 4.88e-06 .. 6.37e-06 A | yes | ff 27 C high |
| both_on (dig_in 1111, en 1, 3v3 1, 1v2 1) | 4.99e-06 .. 7.06e-06 A | 4.88e-06 .. 6.37e-06 A | yes | ff 125 C high |
| cores_on_tg_off (dig_in 1100, en 1, 3v3 1, 1v2 1) | 2.03e-12 .. 1.9e-10 A | 2.03e-12 .. 1.9e-10 A | yes | ff 125 C high |
| enable_low (dig_in 1111, en 0, 3v3 1, 1v2 1) | 1.94e-12 .. 6.45e-11 A | 1.94e-12 .. 1.57e-10 A | yes | ff 125 C high |
| vdd1v2_off (dig_in 1111, en 1, 3v3 1, 1v2 0) | 1.94e-12 .. 6.45e-11 A | 1.94e-12 .. 1.57e-10 A | yes | ff 125 C high |
| vdd1v2_off_1uA (dig_in 1111, en 1, 3v3 1, 1v2 0) | 1.94e-12 .. 6.45e-11 A | 1.94e-12 .. 1.57e-10 A | yes | ff 125 C high |
| vdd3v3_off (dig_in 1111, en 1, 3v3 0, 1v2 1) | -6.14e-08 .. -1.54e-10 A | -8.83e-08 .. -3.91e-09 A | yes | tt 27 C high |
| both_supplies_off (dig_in 1111, en 1, 3v3 0, 1v2 0) | -1.79e-09 .. -2.22e-11 A | -2.87e-09 .. -3.16e-11 A | yes | ff 125 C nom |

tie-lows dig_out[4] / dig_out[11], vdd_1v2 on: max 0 / 0 V (into 1 Tohm)
supply currents, all_off: I(vdd_3v3) 2.79e-10 .. 1.44e-08 A, I(vdd_1v2) 2.91e-06 .. 5.42e-06 A
supply currents, both_on: I(vdd_3v3) 2.46e-05 .. 3.03e-05 A, I(vdd_1v2) 2.91e-06 .. 5.42e-06 A
floating vdd_1v2 when gated off: 0 .. 0 V
floating vdd_3v3, vdd3v3_off: 0.483 .. 0.665 V
floating vdd_3v3, both_supplies_off: 0.54 .. 0.589 V

| corner | T (C) | I_OA (uA) low / nom / high supply | I_BG (uA) low / nom / high |
|---|---|---|---|
| tt | 27 | - / 4.992 / 4.994 | - / 4.958 / 4.965 |
| tt | 125 | - / 6.662 / 6.664 | - / 4.883 / 4.891 |
| ff | 27 | - / 5.324 / 5.326 | - / 6.360 / 6.369 |
| ff | 125 | - / 7.054 / 7.056 | - / 6.305 / 6.315 |

logic-level failures: 0
