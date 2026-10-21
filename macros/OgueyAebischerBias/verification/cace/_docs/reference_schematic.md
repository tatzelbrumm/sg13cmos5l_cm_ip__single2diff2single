
# CACE Summary for reference

**netlist source**: schematic

|      Parameter       |         Tool         |     Result      | Min Limit  |  Min Value   | Typ Target |  Typ Value   | Max Limit  |  Max Value   |  Status  |
| :------------------- | :------------------- | :-------------- | ---------: | -----------: | ---------: | -----------: | ---------: | -----------: | :------: |
| PMOS mirror bias voltage | ngspice              | Vbp_val              |             any |          ​ |          any |          ​ |          any |          ​ |   Skip 🟧    |
| NMOS mirror bias voltage | ngspice              | Vbn_val              |             any |          ​ |          any |          ​ |          any |          ​ |   Skip 🟧    |
| Resistor-free reference voltage | ngspice              | Vbr_val              |             any |          ​ |          any |          ​ |          any |          ​ |   Skip 🟧    |
| Core reference current | ngspice              | Ibias_val            |          200 nA |          ​ |          any |          ​ |      1000 nA |          ​ |   Skip 🟧    |
| Start-up time        | ngspice              | t_startup            |             any |          ​ |     20000 ns |          ​ |     40000 ns |          ​ |   Skip 🟧    |
| Settled vbp          | ngspice              | Vbp_final            |             any |          ​ |          any |          ​ |          any |          ​ |   Skip 🟧    |
| Settled vbn          | ngspice              | Vbn_final            |             any |          ​ |          any |          ​ |          any |          ​ |   Skip 🟧    |
| Settled vbr          | ngspice              | Vbr_final            |             any |          ​ |          any |          ​ |          any |          ​ |   Skip 🟧    |
| PSRR of vbr at 1kHz  | ngspice              | PSRR_vbr             |           50 dB |          ​ |        60 dB |          ​ |          any |          ​ |   Skip 🟧    |
| Output current noise density | ngspice              | Ibias_noise          |             any | 0.521 nA/rtHz |  0.5 nA/rtHz | 0.521 nA/rtHz |    1 nA/rtHz | 0.521 nA/rtHz |   Pass ✅    |
| Turn-off time        | ngspice              | t_disable            |             any |          ​ |          any |          ​ |          any |          ​ |   Skip 🟧    |
| Quiescent supply current, enabled | ngspice              | Iq_enabled           |             any |          ​ |        10 uA |          ​ |        20 uA |          ​ |   Skip 🟧    |
| Quiescent supply current, disabled | ngspice              | Iq_disabled          |             any |          ​ |        10 nA |          ​ |        20 nA |          ​ |   Skip 🟧    |
| Core current accuracy - Mismatch | ngspice              | Ibias_accuracy       |            -2 % |          ​ |          0 % |          ​ |          2 % |          ​ |   Skip 🟧    |
| Leg-to-leg current matching - Mismatch | ngspice              | Leg_matching         |            -1 % |          ​ |          0 % |          ​ |          1 % |          ​ |   Skip 🟧    |


## Plots
