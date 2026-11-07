## Tree bias voltages on analog_bus2 (V), min .. max over corners x temperatures x supplies

| reference | vbp | vbn | vbpc | vbnc | tree off, vbp selected |
|---|---|---|---|---|---|
| oa | 1.861 .. 2.036 | 0.884 .. 0.955 | 1.725 .. 1.940 | 1.156 .. 1.329 | 2.769 .. 2.994 |
| bg | 1.952 .. 1.996 | 0.885 .. 0.927 | 1.824 .. 1.901 | 1.198 .. 1.239 | 2.769 .. 2.994 |
| ib0 | 1.983 .. 2.057 | 0.835 .. 0.928 | 1.866 .. 1.963 | 1.138 .. 1.220 | 2.769 .. 2.994 |

| corner | T | supply | vbn with OA / BG / ibias0 (V) | vbp with OA / BG / ibias0 (V) |
|---|---|---|---|---|
| tt | 27 | nom | 0.928 / 0.927 / 0.928 | 1.994 / 1.996 / 1.994 |
| tt | 125 | nom | 0.955 / 0.885 / 0.890 | 1.861 / 1.992 / 1.983 |
| ff | 27 | nom | 0.884 / 0.917 / 0.873 | 2.036 / 1.975 / 2.057 |
| ff | 125 | nom | 0.911 / 0.885 / 0.835 | 1.902 / 1.952 / 2.047 |

## ibias1 -> analog_bus3 (bus at 0.7 V, harness source 5 uA)

on: 5.0000 .. 5.0009 uA; off: max 2.2e-11 A

## Fail-safe (every dig_in = 1)

| case | max V(bus2) into 1 Gohm | max |I(bus0)| | max |I(bus1)| | max |I(bus3)| |
|---|---|---|---|---|
| vdd1v2_off | 162.4 mV | 5.7e-11 A | 1.47e-10 A | 2.2e-11 A |
| vdd1v2_off_1uA | 162.4 mV | 5.7e-11 A | 1.47e-10 A | 2.2e-11 A |
| enable_low | 162.4 mV | 5.7e-11 A | 1.47e-10 A | 2.2e-11 A |
