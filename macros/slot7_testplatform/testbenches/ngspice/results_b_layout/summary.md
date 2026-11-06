## Tree bias voltages on analog_bus2 (V), min .. max over corners x temperatures x supplies

| reference | vbp | vbn | vbpc | vbnc | tree off, vbp selected |
|---|---|---|---|---|---|
| oa | 1.842 .. 2.015 | 0.869 .. 0.937 | 1.745 .. 1.956 | 1.163 .. 1.336 | 2.763 .. 2.990 |
| bg | 1.934 .. 1.976 | 0.868 .. 0.912 | 1.843 .. 1.916 | 1.205 .. 1.246 | 2.763 .. 2.990 |
| ib0 | 1.967 .. 2.037 | 0.819 .. 0.913 | 1.883 .. 1.979 | 1.145 .. 1.225 | 2.763 .. 2.990 |

| corner | T | supply | vbn with OA / BG / ibias0 (V) | vbp with OA / BG / ibias0 (V) |
|---|---|---|---|---|
| tt | 27 | nom | 0.913 / 0.912 / 0.913 | 1.973 / 1.976 / 1.973 |
| tt | 125 | nom | 0.937 / 0.869 / 0.874 | 1.842 / 1.976 / 1.967 |
| ff | 27 | nom | 0.869 / 0.900 / 0.858 | 2.015 / 1.952 / 2.037 |
| ff | 125 | nom | 0.893 / 0.868 / 0.819 | 1.883 / 1.934 / 2.032 |

## ibias1 -> analog_bus3 (bus at 0.7 V, harness source 5 uA)

on: 5.0000 .. 5.0009 uA; off: max 2.2e-11 A

## Fail-safe (every dig_in = 1)

| case | max V(bus2) into 1 Gohm | max |I(bus0)| | max |I(bus1)| | max |I(bus3)| |
|---|---|---|---|---|
| vdd1v2_off | 161.8 mV | 5.7e-11 A | 1.47e-10 A | 2.2e-11 A |
| vdd1v2_off_1uA | 161.8 mV | 5.7e-11 A | 1.47e-10 A | 2.2e-11 A |
| enable_low | 161.8 mV | 5.7e-11 A | 1.47e-10 A | 2.2e-11 A |
