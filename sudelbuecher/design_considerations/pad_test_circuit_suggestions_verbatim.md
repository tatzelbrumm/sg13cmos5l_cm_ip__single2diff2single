Here's a set of building blocks for an on-chip "test DUT", all continuous-time. The only switching is static configuration from `dig_in`, held for each measurement; nothing toggles while you measure.

**Ground rule: switch only gates.** Every matched-pair unit input is a MOS gate. If all routing switches sit in series with gates, they carry no DC current, so their on-resistance adds no error. This lets you use a large routing matrix without degrading accuracy. Use thick-oxide transmission gates behind the level shifters you need anyway.

**1. Polarity-reversing pass-through (+1 / −1 / 0)**

This is a fully differential unity-gain stage built from the same four matched units (2:2), with a static cross-switch at its input gates.
- **+1, then −1:** with s for the input buffer, X for this stage and d for the output buffer, vout = d(X·s(vin)).
  - Adding the +1 and −1 results leaves 2·o_d, the output buffer's offset and its even-order terms.
  - Subtracting them leaves the input chain including o_s, the input buffer's offset.
  - So two static loopback measurements separate the two buffers' errors without the analog bus.
- **0:** the outputs sit at vcm, so you measure the output buffer's offset and noise directly (test 2).

**2. Common-mode readout mode in the output buffer**

Switch the gates of unit B from (vref, vinn) to (vinn, vref). The balance becomes f(vinp − vref) + f(vinn − vref) = 2f(vout − vref), so the pad shows the internal pair's common-mode error instead of half its difference. That gives you "measure V<sub>CM</sub>" in tests 3 and 9 through `vout` itself, so they no longer depend on the shared `analog_bus`. The same switch works on any internal pair the routing matrix can reach.

**3. Differential DC ladder**

This is a poly resistor string centred on vcm, with symmetric taps at vcm ± kΔ selected through gate switches. Its outputs only drive gates, so the string's impedance doesn't matter.
- It gives the output buffer known differential DC inputs, so you can measure its gain, offset and DC nonlinearity standalone (test 1) without `analog_bus`.
- One tap pair can also replace vin for the input buffer, as an internal reference input with no external source noise.
- The ladder depends only on resistor ratios. It doesn't need the PUDDING DAC, although that remains an option for finer steps.

**4. Input short for the input buffer**

Disconnect the input unit gates from `vin` and switch them to vref. The input buffer's offset and noise then appear at its outputs, which you read through the output buffer or the analog bus.

**5. Quiescent current monitor for the class-AB stage**

A sense device of about 1/1000 the output device size shares gates A or B and copies the output device's current. Bring that current out on an `analog_bus` line into an external resistor. This shows I_Q, its spread over corners and the class-AB current split under load, without relying on supply current that the harness gates and may share.

**6. Step source**

Switch a gate node between two ladder taps with a single `dig_in` transition. The edge timing is loose because it comes through SPI, but you only need the response shape relative to the edge at the pad. That gives you settling time, slew rate and phase margin with the internal load, and it needs no clock, so the gated `proj_clk` doesn't matter.

**How the configurations map onto your tests**

| Configuration | Measures | Replaces / adds |
|---|---|---|
| Ladder → output buffer | output buffer gain, offset, DC nonlinearity | test 1 without the bus |
| X = 0 → output buffer | output buffer offset, noise | test 2 |
| Input short → input buffer → CM readout | input buffer common-mode error | test 3 V<sub>CM</sub> without the bus |
| Input buffer → X = ±1 → output buffer | separates the two buffers' offsets and even-order terms | test 4, made separable |
| Step between taps → output buffer | settling, slew, phase margin | new |
| I_Q sense → bus | class-AB bias, current split | new |

The extra hardware is four matched units for the pass-through, plus the resistor ladder, the sense devices and switches. That's small next to the clamp frames. The g<sub>m</sub>C stage then becomes a separate thing to test rather than the only way to exercise the pads.
